# Plano de Ação — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md`

## Natureza da Wiki

- **Tipo**: **nova**
- **Wiki ancestral**: — (não se aplica)
- **Motivo**: primeira feature de negócio do painel `/app`. O que existe ali hoje é o
  `ProjetoResource`, que o próprio docblock declara **descartável, de demonstração**
  (`app/Models/Projeto.php:12-16`).

> **Efeito no `feature-quality-gate`**: tipo `nova` valida **só esta feature** — não dispara
> regressão contra CT de wiki ancestral. Mas a feature **cria dois Resources no painel `app`**, e
> isso muda a matriz de permissões que `tests/Kit/PaineisTest.php` afirma. Essa regressão específica
> está no plano como CT-18, e é obrigatória apesar da natureza `nova`.

## Cobertura do Requisito

<!-- Toda cláusula do 00-requisito.md aparece aqui. Cláusula sem passo é omissão. -->

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | Cria solicitação com descrição, valor e centro de custo | 2, 4, 5, 9 | `CentroCusto` é entidade nova — ver `00` → A-01 |
| RQ-02 | Edita em rascunho | 5, 7, 9 | barreira no model (`exigirRascunho`) **e** affordance na policy |
| RQ-03 | Exclui em rascunho | 7, 9 | idem |
| RQ-04 | Envio vai para o gestor do centro de custo | 5, 6, 9 | falha fechado sem gestor — `00` → A-10 |
| RQ-05 | Acima de R$ 5.000 exige o diretor, **depois** do gestor | 1, 3, 5, 6 | limite configurável, comparação `>` — `00` → A-04 |
| RQ-06 | Gestor aprova ou rejeita | 5, 9 | o diretor também rejeita — `00` → A-07 |
| RQ-07 | Justificativa obrigatória na rejeição | 5, 9 | obrigatória **no model**, não só no formulário |
| RQ-08 | Rejeitada volta para rascunho | 3, 5 | **não existe estado `rejeitada`** — ver ADR-01 |
| RQ-09 | Solicitante corrige e envia de novo | 5 | o histórico do ciclo anterior **sobrevive** — ADR-03 |
| RQ-10 | Aprovada não se mexe mais | 5, 7, 9 | estado terminal — `00` → A-05 |
| RQ-11 | Cancela antes da aprovação final | 5, 9 | em `rascunho` o verbo é excluir — `00` → A-06 |
| RQ-12 | Mostrar o status atual | 3, 9 | badge na listagem + infolist |
| RQ-13 | Mostrar quem aprovou cada etapa | 2, 4, 9 | tabela de etapas append-only — ADR-03 |
| RQ-14 | Notificar por e-mail o próximo aprovador | 6 | só o próximo aprovador — `00` → A-11 |

## Objetivo

Dar ao painel `/app` o primeiro fluxo de negócio de verdade do kit: uma solicitação de compra que
nasce em rascunho, atravessa uma ou duas mãos de aprovação conforme o valor, e termina aprovada,
cancelada — ou de volta ao rascunho com o motivo escrito, para o solicitante corrigir.

A entrega é o **fluxo**, não um módulo de compras. Três tabelas, uma máquina de cinco estados, duas
telas e um e-mail. Tudo que o card não pediu — anexos, cotação, fornecedor, alçadas múltiplas, SLA —
está declarado fora de escopo no `00` e recusado explicitamente em ADR-04, porque é exatamente aqui
que uma feature de aprovação vira um ERP.

## Contexto

### O que existe, e o que falta

| Peça | Onde | Estado |
|---|---|---|
| Painel `/app` | `app/Providers/Filament/AppPanelProvider.php:57-88` | existe, com tenancy opcional. Descobre Resources em `app/Filament/App/Resources` |
| Único resource do `/app` | `app/Filament/App/Resources/Projetos/ProjetoResource.php:19-37` | **demonstração descartável**, por declaração própria. Serve de molde, não de dependência |
| Model de negócio com tenant | `app/Traits/BelongsToTenant.php` | pronto: relação `tenant()`, escopo global e preenchimento de `tenant_id` |
| Enums | — | **não existe `app/Enums/`**. Este é o primeiro |
| Notificação por e-mail | `app/Notifications/ConviteDeAcesso.php` | o único molde do projeto: `ShouldQueue`, `via mail`, URL montada pelo painel |
| Channels de log | `config/logging.php:85-107` | `ai`, `tenancy`, `autenticacao`. **Nenhum de compras** |
| Papéis | `database/seeders/PapeisSeeder.php:53-93` | `master_global`, `admin`, `infra`, `admin_organizacao`, `panel_user`. **Nenhum `diretor`** |
| Subtração do `panel_user` | `PapeisSeeder.php:117-123` | lista de FQCN de administração do `/app`: hoje `UserResource` e `ConviteResource` |
| Policies | `app/Policies/ProjetoPolicy.php` | molde gerado pelo Shield: um método por ação, cada um um `can('Acao:Model')` |
| Transição atômica de estado | `app/Models/Convite.php:622-631` | **precedente do projeto**: `UPDATE … WHERE <estado esperado>` + conferência do número de linhas |
| Barreira de identidade no model | `app/Models/Convite.php:709-727` | **precedente e regra**: `exigirDono()`, cobrada por `.ai/rules/filament.md` |
| Ação com formulário em modal | `app/Filament/Concerns/ConvidaEmMassa.php:36-128` | molde exato para a rejeição com justificativa: `->schema([...])` + `->action(fn (array $data) …)` |
| Suíte de teste com tenancy | `tests/Tenancy/`, `tests/BrowserTenancy/` | existem, mas **ambas no grupo `kit`** — ver passo 10 |

### A descoberta que muda o modelo: **não existe o estado "rejeitada"**

O card diz, literalmente: *"Solicitação rejeitada **volta para rascunho** pro solicitante corrigir e
enviar de novo."*

Se ela volta para rascunho, então depois da rejeição a situação **é** `rascunho`. Uma coluna de
status com o valor `rejeitada` seria um estado por onde nada passa, ou um estado que mente sobre o
que o solicitante pode fazer. Os estados que sobram são cinco:

```
rascunho ──enviar──▶ aguardando_gestor ──aprovar──▶ aguardando_diretor ──aprovar──▶ aprovada
   ▲                      │       │                        │      │                (terminal)
   └──────rejeitar────────┘       │                        │      │
   └──────────────rejeitar────────┼────────────────────────┘      │
                                  ▼                               ▼
                              cancelada  ◀───────cancelar─────────┘
                              (terminal)
```

O salto `aguardando_gestor → aprovada` (sem diretor) existe e é o caminho comum: só valores acima do
limite atravessam `aguardando_diretor`. Ver ADR-01.

**Consequência prática**: a rejeição não pode viver numa coluna da própria solicitação, porque o
reenvio a apagaria. Ela vive no histórico de etapas — ADR-03, e é o que também entrega RQ-13.

### A armadilha de autorização desta feature

`.ai/rules/filament.md` e `wikis/convencoes.md` descrevem a mesma falha, com as mesmas palavras:
entidade de administração registrada no painel `app` **sem entrar em
`PapeisSeeder::permissoesDeAdministracaoDoApp()`** é herdada por `panel_user`, e **nada acusa** —
os dois seeders rodam, os testes ficam verdes, e todo usuário comum vira administrador da
organização.

Aqui isso tem uma consequência específica e pior que a genérica: quem edita `centros_custo` edita
`gestor_id`. **Quem edita `gestor_id` se nomeia gestor e aprova as próprias compras.** É a escalada
de privilégio desta entrega, e ela custa uma linha para evitar e nenhum erro para cometer. Passo 7,
ADR-06, CT-14.

### Como o projeto já resolve as duas mecânicas difíceis

Nenhuma das duas precisa ser inventada — as duas têm precedente lido e citado:

1. **Transição concorrente**: `Convite::aceitarComoUsuarioExistente()` (`Convite.php:622-631`) faz
   `UPDATE … WHERE aceito_em IS NULL` e confere o retorno, em vez de `get()` + `save()`. O docblock
   explica por que: `attach`/`assignRole` são idempotentes, então check-then-act deixaria duas
   requisições simultâneas passarem. Aqui o análogo é **dois diretores clicando "Aprovar" ao mesmo
   tempo** — sem o UPDATE condicional, as duas etapas seriam gravadas.
2. **Barreira de identidade**: `Convite::exigirDono()` (`Convite.php:709-727`), chamada na primeira
   linha dos métodos públicos. A regra correspondente
   (`.ai/rules/filament.md` → *"Asserção de identidade vive no model, não na query da tela"*) diz
   por que a policy não substitui: **policy não é consultada por job, comando, seeder nem rota de
   API**, e é o primeiro chamador novo que passa por cima.

## Autorização

### Policies

Duas policies novas, no molde de `ProjetoPolicy` (um método por ação, cada um um `can()`), com
**dois métodos que ganham condição extra de registro**:

| Policy | Método | Regra |
|---|---|---|
| `SolicitacaoCompraPolicy` | `viewAny`, `view`, `create` | `can('…:SolicitacaoCompra')` puro |
| `SolicitacaoCompraPolicy` | `update`, `delete` | `can(…)` **e** `situacao === Rascunho` **e** `solicitante_id === $user->id` |
| `CentroCustoPolicy` | todos | `can('…:CentroCusto')` puro |

> A condição extra em `update`/`delete` é **affordance**, não barreira: é ela que faz o Filament
> esconder os botões Editar e Excluir de quem não pode usá-los (`wikis/convencoes.md` →
> *"Nada de affordance sem permissão… Encontrar na UI algo que resulta em 403 é considerado bug"*).
> A **barreira** é `SolicitacaoCompra::exigirRascunho()` + `exigirSolicitante()`, no model —
> passo 5. **As duas existem, e não são redundantes**: a regra do projeto é explícita sobre isso.

### Gates

Nenhum novo. `master_global` continua entrando por `Gate::before`.

### Papéis

**Um papel novo**: `diretor`, com `roles.painel = 'app'` — sem a coluna ele autentica e leva 403 nos
três painéis (`wikis/convencoes.md`, e `.ai/rules/filament.md` → *"Papel novo precisa declarar o
painel"*). A matriz dele é **a mesma do `panel_user`** (matriz do `app` menos administração): a
autoridade de aprovação **não é permissão**, é o par situação × identidade resolvido no model. Ver
ADR-05.

**Gestor não é papel**: é `centros_custo.gestor_id`. Quem é gestor de um centro é um `panel_user`
apontado por uma FK.

### Middleware

Nenhum novo. O `/app` já aplica `DefinirTenantDePermissoes`.

### Permissions — passo obrigatório, não opcional

Dois Resources novos ⇒ os dois seeders, nesta ordem
(`.ai/rules/filament.md`, `wikis/convencoes.md`):

```bash
php artisan db:seed --class=Database\\Seeders\\ShieldPermissionsSeeder
php artisan db:seed --class=Database\\Seeders\\PapeisSeeder
```

Sem eles, as duas telas respondem **403 para todo mundo que não seja `master_global`**.

## Rotas

Nenhuma rota escrita à mão — todas geradas pelos Resources do painel `app`. Com tenancy ligada, o
prefixo é `/app/{tenant}`.

| Método | URI | Name | Middleware |
|--------|-----|------|------------|
| GET | `/app/solicitacoes-de-compra` | `filament.app.resources.solicitacoes-de-compra.index` | o do painel `app` |
| GET | `/app/solicitacoes-de-compra/create` | `….create` | idem |
| GET | `/app/solicitacoes-de-compra/{record}` | `….view` | idem |
| GET | `/app/solicitacoes-de-compra/{record}/edit` | `….edit` | idem |
| GET | `/app/centros-de-custo` | `filament.app.resources.centros-de-custo.index` | idem |
| GET | `/app/centros-de-custo/create` | `….create` | idem |
| GET | `/app/centros-de-custo/{record}/edit` | `….edit` | idem |

> `{record}` é o **uuid**, não o id — `TemUuid::getRouteKeyName()` (`app/Traits/TemUuid.php:35-38`).

## Superfície de UI

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| `SolicitacoesCompraTable` (listagem) | Filament Table | `/app/solicitacoes-de-compra` | vê a **situação** em badge; dispara Enviar / Aprovar / Rejeitar / Cancelar | **Sim** |
| `SolicitacaoCompraForm` (create/edit) | Filament Schema | `…/create`, `…/{record}/edit` | preenche descrição, valor e centro de custo | **Sim** |
| `ViewSolicitacaoCompra` (infolist) | Filament Page (`ViewRecord`) | `…/{record}` | lê situação + **histórico: quem decidiu cada etapa, quando e por quê** | Sim |
| Modal "Rejeitar" | Filament Action + `->schema()` | mesma rota | escreve a **justificativa obrigatória** e confirma | **Sim** |
| Modal "Enviar" / "Cancelar" | Filament Action `requiresConfirmation` | mesma rota | confirma a transição | **Sim** |
| `CentrosCustoTable` + form | Filament Resource | `/app/centros-de-custo` | cadastra centro e escolhe o **gestor** | Sim |

**Gate de CT-B**: 6 linhas na tabela, todas com `Depende de JS? = Sim`, **e** a interação atravessa
≥ 2 telas e ≥ 2 personas (solicitante → gestor → diretor). Passa nas duas condições →
**criar `05-casos-de-teste-browser.md`**. ✅

E há um motivo próprio desta feature: **o fluxo só existe entre pessoas diferentes**. Um teste HTTP
prova que `aprovar()` transiciona; só o navegador prova que o gestor **encontra o botão** e que o
solicitante **não o encontra** — que é a metade do requisito escrita como "mostrar na tela" (RQ-12,
RQ-13) e a regra de affordance do projeto.

## Variáveis de Ambiente

| Key | Default | Descrição |
|-----|---------|-----------|
**Uma chave nova, e só uma:**

| Key | Default | Descrição |
|-----|---------|-----------|
| `KIT_COMPRAS_LIMITE_DIRETOR` | `5000.00` | Valor **acima do qual** a aprovação do diretor é exigida (RQ-05). Lido em `config/kit.php` |

**Nenhuma chave de log própria.** O channel `compras` lê `env('LOG_LEVEL', 'debug')` direto, como o
`autenticacao` (`config/logging.php:104`), e **não** um `LOG_COMPRAS_LEVEL`. O arquivo tem os dois
padrões — `ai` e `tenancy` têm chave própria, `autenticacao` não — e aqui vale o mais curto: ninguém
liga o log de compras sem ligar o do resto.

Nenhuma chave de e-mail nova: a notificação usa o `MAIL_MAILER` que o kit já configura.

> **Atenção operacional**, idêntica à do convite: `QUEUE_CONNECTION=database` é o default do kit e a
> notificação é `ShouldQueue` — **sem worker rodando, o e-mail do aprovador não sai**. A fila parada
> aparece no monitor do `/infra`. Em teste, `phpunit.xml` fixa `QUEUE_CONNECTION=sync`, então os CTs
> não sofrem disso — o que é justamente por que a armadilha precisa estar escrita aqui.

## Eventos / Listeners / Observers

**Nenhum.** As transições são métodos explícitos do model (`enviar`, `aprovar`, `rejeitar`,
`cancelar`), e cada uma sabe quem notificar. Um observer de `updated` teria de reconstruir, a partir
de `getChanges()`, qual transição ocorreu — informação que o método já tem em mãos. Ver ADR-07.

## Jobs / Queues

Nenhum job próprio. A única coisa enfileirada é a notificação, embrulhada pelo Laravel em
`SendQueuedNotifications`, exatamente como `ConviteDeAcesso` (`app/Notifications/ConviteDeAcesso.php:27`).

- **Connection/queue**: os defaults do projeto. Sem `->onQueue()` próprio — fila nomeada só se
  justifica quando há disputa medida, e não há.

## Impacto em Features Existentes

| Feature | O que pode quebrar e por quê |
|---|---|
| **Matriz de permissões por painel** | dois Resources novos no `app` ⇒ a contagem de permissions muda. `tests/Kit/PaineisTest.php` afirma essa matriz e **vai ficar vermelho** até rodar os dois seeders e ajustar o número. **É a regressão mais provável desta entrega** — CT-18 |
| **`panel_user`** | recebe as permissões de `SolicitacaoCompra` (correto) e **não pode** receber as de `CentroCusto` (ADR-06). Se `permissoesDeAdministracaoDoApp()` não for atualizada, nada falha e a escalada de A-08 fica no ar — CT-14 |
| **`Paineis::permissoesDe()`** | casa por **FQCN exato**, nunca substring (`app/Support/Paineis.php:93-97`). `CentroCustoResource::class` inteiro, nada de `str_contains` |
| **Navegação do `/app`** | dois itens novos no menu. O `ProjetoResource` de demonstração continua ali; esta wiki **não o remove** — apagá-lo é decisão de quem usa o kit, e não está no card |
| **`tests/Pest.php` e `phpunit.xml`** | ganham a suíte `FeatureTenancy` (passo 10). Mudança em arquivo que **toda** suíte carrega: rodar `composer test:kit` depois, para confirmar que nada mais se moveu |
| **Auditoria (`/infra/audits`)** | três models auditáveis novos. Cresce o volume da trilha; nenhum comportamento existente muda |

## Rollback

- **Migration down**: `dropIfExists` nas três tabelas, na ordem inversa da criação
  (`etapas_aprovacao_compra` → `solicitacoes_compra` → `centros_custo`), por causa das FKs.
- **Permissions órfãs**: as permissions dos dois Resources **sobrevivem** ao rollback das tabelas.
  Rodar os dois seeders de novo depois de remover os Resources — os dois são idempotentes.
- **Papel `diretor`**: fica no banco. Papel sem Resource é inofensivo (só carrega permissões que não
  existem mais); remover exige `Role::findByName('diretor')->delete()` à mão.
- **Reversão de dados**: não há migração de dados. Nada a reverter além das tabelas.
- **Feature flag**: nenhuma. As telas aparecem para quem tem a permission — e é o seeder que a dá.
  Não desligar por config: seria uma segunda chave de acesso ao lado da matriz de permissões, que já
  é a chave.

## Dependências

**Nenhum pacote novo.** Tudo já está instalado — confirmado em `composer.json`:

| Peça | Origem |
|---|---|
| `Filament\Forms\Components\{TextInput, Textarea, Select}` | `filament/forms` ^5.6 — `Textarea.php` presente em `vendor/filament/forms/src/Components/` |
| `Filament\Support\Contracts\{HasLabel, HasColor}` | `filament/support` — presentes em `vendor/filament/support/src/Contracts/` |
| `TextColumn::money()` | `vendor/filament/tables/src/Columns/Concerns/CanFormatState.php:221` |
| `Filament\Actions\Action::schema()` | `vendor/filament/actions/src/Concerns/HasSchema.php:26` |
| `Resource::getUrl()` | `vendor/filament/filament/src/Resources/Resource/Concerns/CanGenerateUrls.php:16` |
| Notificação por e-mail | `Illuminate\Notifications\Notification` + `ShouldQueue` — molde em `ConviteDeAcesso` |
| `pestphp/pest-plugin-browser` ^5.0 | já em `composer.json` (require-dev), e `tests/Browser/` já existe |

## Riscos

| Risco | Mitigação |
|---|---|
| **`CentroCustoResource` esquecido na subtração do `panel_user`** → escalada de privilégio silenciosa (A-08) | passo 7 + ADR-06 + **CT-14**, que assere a ausência da permission. Não gera erro se esquecido: só o CT acusa |
| **Duas aprovações simultâneas** (dois diretores, ou duas abas) gravarem duas etapas | `UPDATE … WHERE situacao = <esperada>` + conferência do número de linhas, no precedente de `Convite.php:622-631`. **CT-12** |
| **Borda do limite** — R$ 5.000,00 exatos exigirem diretor por engano | comparação `>` explícita, limite em config, e **CT-04 com dataset dos dois lados** |
| **Justificativa validada só no formulário** | `rejeitar()` exige a justificativa **no model** e lança sem ela. **CT-11** chama o método direto |
| **Rejeição apagar o histórico no reenvio** | histórico append-only em tabela própria (ADR-03). **CT-08** reenvia e confere que o ciclo anterior sobreviveu |
| **Papel `diretor` resolvido no contexto errado** com tenancy — `model_has_roles.team_id` | destinatários resolvidos **no request**, com o contexto já fixado pelo `DefinirTenantDePermissoes`, e passados prontos para a notificação. **CT-17** (suíte com tenancy) |
| **`PaineisTest` vermelho** por causa dos Resources novos | previsto, não surpresa: CT-18 é o primeiro a rodar |
| **E-mail não sair por falta de worker** | não é defeito da feature (é o default do kit). Documentado em Variáveis de Ambiente; os CTs usam `Notification::fake()` e o `sync` do `phpunit.xml` |
| **`decimal` como tipo de valor** | não há aritmética nesta feature (nenhuma soma, total ou rateio), só comparação. ADR-02 registra o **gatilho** para migrar a centavos |

## Channel de Log da Feature

### Verificação de Channel Existente

`config/logging.php` lido por inteiro. Os channels do kit são `ai` (`:85`), `tenancy` (`:93`) e
`autenticacao` (`:101`) — todos `daily`, 14 dias, com o comentário do bloco declarando a convenção:
*"um canal por feature, sempre daily/14 dias, visíveis no Logs Explorer do /infra"*. `Grep` por
`Log::channel(` em `app/` confirma que só esses três são usados. **Nenhum serve a compras**: o fluxo
de aprovação não é autenticação, não é tenancy e não é IA.

### Decisão

**Criar o channel `compras`**, no formato exato dos vizinhos:

```php
'compras' => [
    'driver'               => 'daily',
    'path'                 => storage_path('logs/compras.log'),
    'level'                => env('LOG_LEVEL', 'debug'),
    'days'                 => 14,
    'replace_placeholders' => true,
],
```

Todos os logs da feature usam `Log::channel('compras')`, no formato `[Classe@Método]`, com context
estruturado. Os pontos exatos estão em cada passo abaixo.

> **Regra LGPD do bloco de channels** (`config/logging.php:80-81`): identificadores sempre
> mascarados, nunca conteúdo em claro. Aqui isso significa: **e-mail do aprovador vai mascarado**
> (`Str::mask($email, '*', 3)`, como `Convite@enviar` faz) e **a justificativa de rejeição NÃO vai
> para o log** — ela é texto livre escrito por uma pessoa sobre outra. No context vai só o
> comprimento, que é o que serve para diagnosticar "veio vazia?".

## Estrutura de Implementação

### 1. Config — o channel de log e o limite do diretor

> Skills: `laravel-best-practices`

- **Path**: `config/logging.php` — acrescentar o channel `compras` **depois** de `autenticacao`
  (`:107`), mantendo a ordem do bloco comentado do kit.
- **Path**: `config/kit.php` — bloco novo, no padrão dos blocos `tenancy` e `convites`, com o
  comentário explicando a decisão de borda:

```php
/*
|--------------------------------------------------------------------------
| Compras
|--------------------------------------------------------------------------
| Valor ACIMA do qual a solicitação exige, além do gestor do centro de custo,
| a aprovação de um diretor. A comparação é estritamente maior: uma
| solicitação de exatamente este valor NÃO passa pelo diretor.
|
| Em reais, com centavos — o mesmo formato da coluna `valor`. Trocar aqui é
| mudar política de alçada sem tocar em código.
*/

'compras' => [
    'limite_diretor' => (float) env('KIT_COMPRAS_LIMITE_DIRETOR', 5000.00),
],
```

- **Path**: `.env.example` — acrescentar `KIT_COMPRAS_LIMITE_DIRETOR=5000.00` junto das demais
  chaves `KIT_*`, que hoje ocupam as linhas 76-94 (`KIT_TENANCY`, `KIT_CONVITE_*`).
- **Logs**: nenhum — config.

### 2. Migrations — três tabelas

> Skills: `laravel-best-practices`

Três arquivos, criados na ordem das FKs. Nomes seguindo o padrão de data do projeto
(`2026_08_14_000003_add_identidade_visual_to_tenants_table.php`).

Toda tabela nova segue os invariantes de `wikis/convencoes.md`: `id()` + `uuid()->unique()`, e
`tenant_id` nas models de negócio.

**a) `…_create_centros_custo_table.php`**

```php
Schema::create('centros_custo', function (Blueprint $table): void {
    $table->id();
    $table->uuid('uuid')->unique();
    $table->foreignId('tenant_id')->constrained();
    $table->string('nome', 120);

    // Sem cascadeOnDelete e sem nullOnDelete: apagar quem é gestor de um centro
    // tem de DOER na hora. nullOnDelete deixaria o centro sem gestor em silêncio,
    // e o próximo envio falharia fechado (A-10) sem ninguém saber por quê.
    $table->foreignId('gestor_id')->nullable()->constrained('users');

    $table->timestamps();

    // Nome único DENTRO da organização, nunca global.
    $table->unique(['tenant_id', 'nome']);
});
```

**b) `…_create_solicitacoes_compra_table.php`**

```php
Schema::create('solicitacoes_compra', function (Blueprint $table): void {
    $table->id();
    $table->uuid('uuid')->unique();
    $table->foreignId('tenant_id')->constrained();

    $table->foreignId('solicitante_id')->constrained('users');
    $table->foreignId('centro_custo_id')->constrained('centros_custo');

    $table->string('descricao', 255);

    // decimal, não float e não centavos. Não há aritmética nesta feature — só a
    // comparação com o limite do diretor. Ver ADR-02, que nomeia o gatilho para
    // migrar a integer em centavos: a primeira soma, total ou rateio.
    $table->decimal('valor', 12, 2);

    // String e não enum de banco: o conjunto de valores é do PHP (App\Enums\
    // SituacaoSolicitacao), e enum nativo obriga migration a cada valor novo —
    // em SQLite, que é o banco dos testes, nem existe.
    $table->string('situacao', 30);

    $table->timestamps();

    // Um índice só, e composto: a pergunta que a tela faz é "o que está esperando
    // MIM, NESTA organização" — toda query da feature é escopada por tenant, pelo
    // escopo global de BelongsToTenant. Um índice avulso em `situacao` ao lado
    // deste não teria consulta que o usasse.
    $table->index(['tenant_id', 'situacao']);
});
```

**c) `…_create_etapas_aprovacao_compra_table.php`**

```php
Schema::create('etapas_aprovacao_compra', function (Blueprint $table): void {
    $table->id();

    /*
     * SEM `uuid`, e é a única tabela desta entrega que abre exceção à invariante de
     * `wikis/convencoes.md` ("toda tabela nova ganha uuid"). A invariante existe por
     * um motivo declarado — route key, para que id numérico na URL devolva 404 e
     * ninguém enumere registros por sequência. Esta tabela NÃO tem rota: não há
     * Resource, não há route binding, e `TemUuid::getRouteKeyName()` não teria a quem
     * responder. A coluna, o trait e o unique index seriam três coisas para uma URL
     * que não existe.
     *
     * No dia em que a etapa ganhar tela própria, a invariante volta a valer e a
     * migration de acréscimo é de uma linha.
     */

    // A etapa morre com a solicitação: cascade aqui é correto, ao contrário das
    // FKs de pessoa acima. Histórico de uma linha apagada não tem a quem servir.
    $table->foreignId('solicitacao_compra_id')
        ->constrained('solicitacoes_compra')->cascadeOnDelete();

    // `gestor` | `diretor`  — string simples, sem Enum. Ver ADR-05.
    $table->string('etapa', 20);
    // `aprovada` | `rejeitada`
    $table->string('decisao', 20);

    $table->foreignId('decidido_por_id')->constrained('users');

    // Obrigatória na rejeição, sempre nula na aprovação. NOT NULL condicional não
    // existe em schema; quem exige é `SolicitacaoCompra::rejeitar()` (passo 5).
    $table->text('justificativa')->nullable();

    $table->timestamps();

    // Sem índice próprio: a FK já indexa `solicitacao_compra_id`, e são unidades de
    // linhas por solicitação. Um índice composto com `created_at` para ordenar três
    // registros é custo de escrita sem ganho de leitura.
});
```

- **`down()`**: `dropIfExists` nas três, **na ordem inversa**.
- **Logs**: nenhum — migrations.

### 3. Enum `SituacaoSolicitacao` — os cinco estados

> Skills: `laravel-best-practices`

- **Path**: `app/Enums/SituacaoSolicitacao.php` — **primeiro enum do projeto**, e por isso a pasta
  `app/Enums/` nasce aqui.
- Backed enum de string, implementando os dois contratos do Filament (confirmados em
  `vendor/filament/support/src/Contracts/`), o que faz badge, filtro e select lerem o rótulo e a cor
  sem `match` espalhado por três telas:

```php
namespace App\Enums;

use Filament\Support\Contracts\HasColor;
use Filament\Support\Contracts\HasLabel;

/**
 * As cinco situações de uma solicitação de compra.
 *
 * NÃO existe `Rejeitada`, e a ausência é o achado central do requisito: o card diz que a
 * solicitação rejeitada "volta para rascunho", então depois da rejeição a situação É
 * `Rascunho`. Um valor `rejeitada` aqui seria um estado por onde nada passa — e mentiria
 * sobre o que o solicitante pode fazer. A rejeição é um EVENTO, gravado em
 * `etapas_aprovacao_compra`. Ver ADR-01.
 *
 * Chaves em TitleCase, valores em snake_case (guideline de Enum do Boost).
 */
enum SituacaoSolicitacao: string implements HasColor, HasLabel
{
    case Rascunho = 'rascunho';
    case AguardandoGestor = 'aguardando_gestor';
    case AguardandoDiretor = 'aguardando_diretor';
    case Aprovada = 'aprovada';
    case Cancelada = 'cancelada';

    public function getLabel(): string { /* pt-BR: 'Rascunho', 'Aguardando gestor', … */ }

    public function getColor(): string
    {
        return match ($this) {
            self::Rascunho          => 'gray',
            self::AguardandoGestor,
            self::AguardandoDiretor => 'warning',
            self::Aprovada          => 'success',
            self::Cancelada         => 'danger',
        };
    }

    /**
     * Em trânsito = já enviada e ainda não decidida. É onde cancelar vale (RQ-11).
     *
     * Único predicado do enum, e de propósito. Um `terminal()` simétrico seria
     * bonito e não teria chamador: RQ-10 se cobra por `exigirSituacao()`, que
     * compara com o estado ESPERADO da transição, não com "é terminal?". Quando
     * aparecer o primeiro `if` que precise dele, ele nasce em uma linha.
     */
    public function emTransito(): bool
    {
        return in_array($this, [self::AguardandoGestor, self::AguardandoDiretor], true);
    }
}
```

> **Por que Enum aqui e `match` de string em `etapa`/`decisao`** (passo 2c): a situação é comparada
> em quatro lugares independentes — policy, visibilidade de ação, transição do model e roteamento da
> notificação — e um literal digitado errado num deles **falha em silêncio**. `etapa` e `decisao` são
> lidos só para exibir; é o mesmo critério que o docblock de
> `ConvidaEmMassa::motivoLegivel()` (`:158-161`) usa para **não** criar Enum. Ver ADR-05.

- **Logs**: nenhum — enum puro.

### 4. Models `CentroCusto` e `EtapaAprovacao`

> Skills: `eloquent-best-practices`

**a) `app/Models/CentroCusto.php`**

- Traits: `AuditsFillables`, `BelongsToTenant`, `TemUuid` — o trio de `Projeto`
  (`app/Models/Projeto.php:28-31`), que é o exemplo canônico do kit.
- `implements Auditable`.
- `$fillable = ['nome', 'gestor_id']` — **`tenant_id` fica fora**, quem preenche é a trait
  (`BelongsToTenant.php:72-78`).
- Relação: `gestor(): BelongsTo<User>`. **Só ela** — um `solicitacoes(): HasMany` só teria como
  consumidor uma coluna de contagem que ninguém pediu.
- **Logs**: nenhum — model sem lógica de fluxo.

**b) `app/Models/EtapaAprovacao.php`**

- **Sem trait nenhuma.** `BelongsToTenant` não entra porque a etapa pertence à solicitação, que já é
  da organização — um segundo escopo global sobre a mesma pergunta seria filtro repetido, e a coluna
  `tenant_id` nem existe na tabela. `TemUuid` não entra porque a tabela não tem rota (ver passo 2c).
- **Sem `AuditsFillables`**: a tabela **é** a trilha. Auditar um registro append-only que ninguém
  edita é gravar o mesmo dado duas vezes, em dois lugares, com dois formatos.
- `$fillable = ['etapa', 'decisao', 'decidido_por_id', 'justificativa']`.
- Relações: `solicitacao(): BelongsTo`, `decididoPor(): BelongsTo<User>`.
- **Logs**: nenhum.

### 5. Model `SolicitacaoCompra` — a máquina de estados (o passo central)

> Skills: `eloquent-best-practices`, `laravel-best-practices`, `ponytail`

- **Path**: `app/Models/SolicitacaoCompra.php`
- Traits: `AuditsFillables`, `BelongsToTenant`, `TemUuid`; `implements Auditable`.
- `$fillable = ['descricao', 'valor', 'centro_custo_id']` — **`situacao`, `solicitante_id` e
  `tenant_id` ficam de fora**, e não é estilo: são as três coisas que o formulário **não pode**
  mandar. `situacao` só muda por transição; `solicitante_id` vem do usuário autenticado;
  `tenant_id` vem da trait. Mass assignment de qualquer uma delas é o furo clássico.
- `casts()`: `['valor' => 'decimal:2', 'situacao' => SituacaoSolicitacao::class]`.
- Relações: `solicitante()`, `centroCusto()`, `etapas(): HasMany` (ordenada por `created_at`).

#### 5.1 As consultas de decisão

```php
/** Acima do limite — estritamente maior. R$ 5.000,00 exatos NÃO exigem diretor (RQ-05, A-04). */
public function exigeDiretor(): bool
{
    return (float) $this->valor > (float) config('kit.compras.limite_diretor', 5000.00);
}

/** Quem tem de decidir AGORA: 'gestor', 'diretor' ou null (nada pendente). */
public function etapaPendente(): ?string { … }

/**
 * Esta pessoa decide a etapa corrente?
 *
 * UM predicado público, e é ele que a barreira `exigirAprovador()` consulta — não uma
 * segunda cópia da regra. É a mesma pergunta feita em dois lugares (o `->visible()` da ação
 * e a barreira do model), e duas cópias divergem: a que divergisse seria um botão visível
 * que estoura ao ser clicado, ou o contrário.
 */
public function podeSerDecididaPor(?User $user): bool { … }

/**
 * As pessoas que decidem a etapa corrente.
 *
 * Resolvido AQUI, no request, e nunca dentro da notificação enfileirada: com
 * `permission.teams` ligado, o `role('diretor')` do spatie filtra pelo team fixado no
 * PermissionRegistrar, e quem o fixa é o middleware `DefinirTenantDePermissoes` — que não
 * roda num worker de fila. Resolver no job devolveria os diretores da organização errada,
 * ou nenhum. Ver ADR-08 e CT-17.
 *
 * @return Collection<int, User>
 */
public function aprovadoresDaVez(): Collection { … }
```

#### 5.2 As transições

Todas com a mesma anatomia, e a ordem importa: **(1) barreira → (2) UPDATE condicional → (3) refresh
→ (4) efeito colateral → (5) log**.

```php
/**
 * Rascunho → aguardando gestor (RQ-04).
 *
 * @throws RuntimeException quando não está em rascunho, quem chama não é o solicitante,
 *                          ou o centro de custo está sem gestor (A-10)
 */
public function enviar(User $autor): void
```

- Barreiras: `exigirSolicitante($autor, 'enviar')` e `exigirSituacao(Rascunho, 'enviar')`.
- **Falha fechado sem gestor** (A-10): se `centroCusto->gestor_id` é nulo, `warning` no log e
  `RuntimeException` — a solicitação **fica em rascunho**. Nunca pular a etapa, nunca enviar para
  ninguém.
- Transição para `AguardandoGestor`; notifica o gestor (passo 6).

```php
/** Aprova a etapa corrente. Gestor → (diretor, se exigido) → aprovada (RQ-05, RQ-06). */
public function aprovar(User $aprovador): void
```

- Barreira: `exigirAprovador($aprovador, 'aprovar')` — confere que `$aprovador` é **o gestor do
  centro de custo** (etapa `gestor`) ou **tem o papel `diretor`** (etapa `diretor`).
- Grava a etapa (`decisao = 'aprovada'`, `justificativa = null`).
- Próxima situação: `AguardandoDiretor` se `etapaPendente() === 'gestor'` **e** `exigeDiretor()`;
  senão `Aprovada`.
- Notifica os aprovadores da próxima etapa — **e só há notificação se houver próxima etapa** (A-11).

```php
/**
 * Rejeita a etapa corrente e devolve a solicitação ao rascunho (RQ-06, RQ-07, RQ-08).
 *
 * @throws RuntimeException quando a justificativa vem vazia
 */
public function rejeitar(User $aprovador, string $justificativa): void
```

- Barreira: `exigirAprovador(...)`.
- **`if (blank($justificativa)) throw`** — a exigência vive **aqui**, não só no `->required()` do
  campo. O formulário protege a tela; o model protege o dado, e é ele que um job, comando ou rota de
  API futura vai chamar. É o mesmo raciocínio de `.ai/rules/filament.md` para `exigirDono()`.
- Grava a etapa com a justificativa e transiciona para `Rascunho`.
- **Nenhuma notificação** — não pedido (A-11).

```php
/** Cancelamento pelo solicitante, só em trânsito (RQ-11, A-06). */
public function cancelar(User $autor): void
```

- Barreiras: `exigirSolicitante($autor, 'cancelar')` e situação `emTransito()`.
- Transição para `Cancelada`. Sem etapa gravada: cancelar não é decisão de aprovador.

#### 5.3 O UPDATE condicional — por que não `save()`

```php
/**
 * Troca a situação de forma ATÔMICA, ou falha.
 *
 * `UPDATE … WHERE situacao = <esperada>` e não `get()` + `save()`, pelo mesmo motivo que
 * `Convite::aceitarComoUsuarioExistente()` (Convite.php:622-631): a leitura e a escrita de um
 * check-then-act têm uma janela entre elas, e nada aqui é idempotente — dois diretores
 * clicando "Aprovar" ao mesmo tempo gravariam DUAS etapas para a mesma decisão, e a segunda
 * transição partiria de um estado que já não era o lido.
 *
 * O banco resolve a corrida: a segunda chamada recebe 0 linhas e para antes de gravar
 * qualquer coisa. Ver ADR-09 e CT-12.
 */
private function transicionar(SituacaoSolicitacao $de, SituacaoSolicitacao $para, string $metodo): void
{
    $mudou = static::query()
        ->whereKey($this->getKey())
        ->where('situacao', $de->value)
        ->update(['situacao' => $para->value, 'updated_at' => now()]);

    if ($mudou !== 1) {
        // … warning no log … 
        throw new RuntimeException('Esta solicitação já mudou de situação. Recarregue a tela.');
    }

    // `update()` do Builder NÃO toca a instância em memória — sem o refresh, o log abaixo e
    // o retorno para a tela sairiam com a situação velha. Mesma linha, mesmo motivo, em
    // Convite.php:635.
    $this->refresh();
}
```

> **A etapa é gravada depois do UPDATE vencer, nunca antes.** Invertido, a corrida perdida deixaria
> uma etapa órfã no histórico — uma aprovação que o sistema registra e não aplica. Como as duas
> escritas precisam ser um bloco, `aprovar()` e `rejeitar()` rodam dentro de `DB::transaction()`.

#### 5.4 As barreiras

`exigirSolicitante()`, `exigirSituacao()` e `exigirAprovador()` — privadas, chamadas na **primeira
linha** dos métodos públicos, cada uma logando `warning` antes de lançar. Molde exato:
`Convite::exigirDono()` (`Convite.php:709-727`).

`exigirAprovador()` **não reimplementa a regra**: ela chama `podeSerDecididaPor()` (5.1), que é o
mesmo predicado que o `->visible()` da ação consulta. Uma regra, dois chamadores — a alternativa
(uma cópia na tela, outra no model) é como a tela passa a mostrar um botão que o model recusa.

> **Não são redundantes com a policy.** A regra do projeto (`.ai/rules/filament.md` → *"Asserção de
> identidade vive no model"*) diz por quê: policy é autorização de ação por perfil e **não é
> consultada por job, comando, seeder nem rota de API**. Enquanto a tela for o único chamador,
> funciona; o primeiro chamador novo passa por cima sem nada acusar. **CT-11 chama os métodos
> direto, com a pessoa errada** — é o teste que a regra exige, e sem ele a barreira não é barreira.

#### 5.5 Logs

Todos em `Log::channel('compras')`, formato `[SolicitacaoCompra@metodo]`, com context estruturado.
E-mail mascarado; **justificativa nunca em claro** (só o comprimento).

```php
Log::channel('compras')->info(
    "[SolicitacaoCompra@enviar] Solicitação enviada para aprovação | solicitacao: {$this->id} - etapa: gestor",
    [
        'solicitacao_id'  => $this->id,
        'tenant_id'       => $this->tenant_id,
        'solicitante_id'  => $this->solicitante_id,
        'centro_custo_id' => $this->centro_custo_id,
        'valor'           => (string) $this->valor,
        'exige_diretor'   => $this->exigeDiretor(),
        'de'              => SituacaoSolicitacao::Rascunho->value,
        'para'            => $this->situacao->value,
        'aprovadores'     => $this->aprovadoresDaVez()->pluck('id')->all(),
    ],
);
```

| Método | Nível | Quando |
|---|---|---|
| `enviar` | `info` | sucesso, com `exige_diretor` no context — é a decisão de fluxo que explica o resto |
| `enviar` | `warning` | centro de custo sem gestor (`motivo: 'centro_sem_gestor'`) — A-10 |
| `aprovar` | `info` | sucesso, com `etapa`, `de`, `para` e `final` (bool) |
| `rejeitar` | `warning` | sempre. Rejeição não é falha de sistema, mas é o fim de um fluxo e é no nível de aviso que se procura por isso. Context leva `justificativa_tamanho`, **nunca o texto** |
| `cancelar` | `warning` | mesmo raciocínio da rejeição |
| `transicionar` | `warning` | corrida perdida (`motivo: 'situacao_mudou'`), com `esperada` e `encontrada` |
| barreiras | `warning` | recusa, com `motivo` ∈ `{nao_e_solicitante, situacao_invalida, nao_e_aprovador, justificativa_vazia}` |

> **Anti-padrão evitado**: nenhum `error`. Nada aqui é falha de sistema — recusa de regra de negócio
> é `warning` pela tabela de severidade de `wikis/convencoes.md`. `error` fica reservado para
> exception que interrompe, e não há nenhuma prevista nesta feature.

### 6. Notification `AprovacaoPendente` — o e-mail do próximo aprovador

> Skills: `laravel-specialist`

- **Path**: `app/Notifications/AprovacaoPendente.php`
- Molde: `ConviteDeAcesso` (`app/Notifications/ConviteDeAcesso.php`) — `extends Notification
  implements ShouldQueue`, `use Queueable`, `via(): ['mail']`.
- Construtor: `public readonly SolicitacaoCompra $solicitacao` e `public readonly string $etapa`.
- Destinatários: `Notification::send($this->aprovadoresDaVez(), new AprovacaoPendente(...))` — os
  `User` são `Notifiable` (`app/Models/User.php:37`), então o envio é direto, **sem** a rota
  on-demand que o convite precisa usar por notificar quem ainda não é usuário.
- Corpo em pt-BR: quem solicitou, descrição, **valor formatado em R$**, centro de custo, e a
  indicação de que é a etapa de gestor ou de diretor.
- **A URL, montada pelo painel e nunca por literal** — mesma razão do `ConviteDeAcesso::url()`
  (`:92-103`), e com o tenant explícito:

```php
/**
 * `getUrl(name, parameters, isAbsolute, panel, tenant)` — assinatura confirmada em
 * vendor/filament/filament/src/Resources/Resource/Concerns/CanGenerateUrls.php:16.
 *
 * O `tenant:` nomeado é obrigatório aqui: a notificação é enfileirada e roda fora do
 * request, onde `Filament::getTenant()` é null — sem ele a URL nasce sem o segmento da
 * organização e o link cai no seletor de tenant, ou em 404.
 */
private function url(): string
{
    return SolicitacaoCompraResource::getUrl(
        'view',
        ['record' => $this->solicitacao],
        tenant: $this->solicitacao->tenant,
    );
}
```

- **Zero log nesta classe**, de propósito e pelo mesmo motivo declarado em `ConviteDeAcesso:23-25`:
  quem loga o envio é o método do model, com o contexto todo. Um log aqui só duplicaria — e é
  justamente o escopo por onde passa o texto do e-mail.
- **Logs**: nenhum (ver acima).

### 7. Autorização — policies, papel `diretor` e a subtração do `panel_user`

> Skills: `laravel-best-practices`

- **Path**: `app/Policies/SolicitacaoCompraPolicy.php` e `app/Policies/CentroCustoPolicy.php` —
  gerar com `php artisan make:policy` e ajustar ao molde de `ProjetoPolicy` (um `can()` por método).
- Em `SolicitacaoCompraPolicy::update()` e `::delete()`, acrescentar a condição de registro:

```php
public function update(AuthUser $authUser, SolicitacaoCompra $solicitacao): bool
{
    // A condição de registro é AFFORDANCE: é ela que faz o Filament esconder o botão.
    // A BARREIRA é `exigirRascunho()`/`exigirSolicitante()` no model — policy não é
    // consultada por job, comando nem rota de API. Ver .ai/rules/filament.md.
    return $authUser->can('Update:SolicitacaoCompra')
        && $solicitacao->situacao === SituacaoSolicitacao::Rascunho
        && $solicitacao->solicitante_id === $authUser->getAuthIdentifier();
}
```

- **Path**: `database/seeders/PapeisSeeder.php` — papel novo, **com o painel declarado**, ao lado dos
  demais (`:89-93`):

```php
// diretor: o segundo par de olhos acima do limite de alçada. A matriz é a MESMA do
// panel_user — a autoridade de aprovação não é permissão, é o par situação × identidade
// resolvido em SolicitacaoCompra::exigirAprovador(). Ver ADR-05.
$this->papel('diretor', $guard, 'app')
    ->syncPermissions($this->permissoesDoPainel('app', $guard)->reject(/* … administração … */));
```

- **Path**: `PapeisSeeder::permissoesDeAdministracaoDoApp()` (`:117-123`) — **acrescentar
  `CentroCustoResource::class`** à lista:

```php
return Paineis::permissoesDe('app', [
    UserResource::class,
    ConviteResource::class,
    CentroCustoResource::class,   // ← quem edita gestor_id se nomeia aprovador (A-08, ADR-06)
])->all();
```

> **`SolicitacaoCompraResource` NÃO entra nesta lista.** Solicitar compra é o negócio, e é o
> `panel_user` que solicita. Entrar aqui deixaria o usuário comum sem a própria feature.

- **Rodar**, nesta ordem, e é passo executável e não observação:

```bash
php artisan db:seed --class=Database\\Seeders\\ShieldPermissionsSeeder
php artisan db:seed --class=Database\\Seeders\\PapeisSeeder
```

- **Critério de aceite**: `panel_user` **tem** `Create:SolicitacaoCompra` e **não tem**
  `Update:CentroCusto`; `diretor` abre `/app` e enxerga as solicitações.
- **Logs**: nenhum — seeder.

### 8. `CentroCustoResource` no painel `/app`

> Skills: `laravel-11-12-app-guidelines`, `tailwindcss-development`

- **Path**: `app/Filament/App/Resources/CentrosCusto/` — estrutura do `ProjetoResource`
  (`Pages/`, `Schemas/`, `Tables/`), que é o molde vivo do painel.
- `protected static ?string $slug = 'centros-de-custo';` e rótulos em pt-BR (`$modelLabel = 'centro
  de custo'`, `$pluralModelLabel = 'centros de custo'`).
- Form:
  - `TextInput::make('nome')->required()->maxLength(120)->scopedUnique(ignoreRecord: true)` —
    **`scopedUnique`, não `unique`**: a regra do Laravel não passa pelo Eloquent e ignoraria o tenant
    (`wikis/convencoes.md` → *"Validação em resource com tenancy"*, e `ProjetoResource.php:67-68`).
  - `Select::make('gestor_id')->relationship('gestor', 'name')->searchable()->preload()`.
- Table: **nome e gestor**, só. `EditAction` + `DeleteAction`. Sem coluna de contagem de
  solicitações: ninguém pediu o número, e ela arrastaria uma relação `HasMany` e um `withCount` para
  decorar a tela.
- **Logs**: nenhum — CRUD declarativo. As mudanças de gestor ficam na trilha de `/infra/audits` via
  `AuditsFillables`, que é onde uma auditoria de "quem se nomeou gestor" seria procurada.

### 9. `SolicitacaoCompraResource` no painel `/app` — telas, ações e histórico

> Skills: `laravel-11-12-app-guidelines`, `livewire-development`

- **Path**: `app/Filament/App/Resources/SolicitacoesCompra/`
- `$slug = 'solicitacoes-de-compra'`; páginas `index`, `create`, `view`, `edit`.

**a) Form** (`Schemas/SolicitacaoCompraForm.php`) — RQ-01

- `TextInput::make('descricao')->required()->maxLength(255)`
- `TextInput::make('valor')->required()->numeric()->minValue(0.01)->prefix('R$')` — `numeric()` em
  `vendor/filament/forms/src/Components/TextInput.php:135`, `prefix()` em
  `vendor/filament/forms/src/Components/Concerns/HasAffixes.php:56`.
- `Select::make('centro_custo_id')->relationship('centroCusto', 'nome')->required()->searchable()->preload()`
- **`situacao` e `solicitante_id` não são campos.** Preenchidos no `CreateSolicitacaoCompra::mutateFormDataBeforeCreate()`
  com `SituacaoSolicitacao::Rascunho` e `Auth::id()` — estado de formulário é do cliente, e as duas
  já estão fora do `$fillable` (passo 5) como segunda camada.

**b) Table** (`Tables/SolicitacoesCompraTable.php`) — RQ-12 e as ações

- Colunas: descrição, `valor` com `->money('BRL')`
  (`vendor/filament/tables/src/Columns/Concerns/CanFormatState.php:221` — `divideBy` fica no default
  `0`, porque o valor está em reais e não em centavos), centro de custo, solicitante,
  `TextColumn::make('situacao')->badge()`.

> **O badge não precisa de `->color(fn …)`**: o `SituacaoSolicitacao` implementa `HasColor` e
> `HasLabel`, e o Filament os consulta sozinho. É a diferença de escrever o enum em vez do `match`
> que `ConvitesTable.php:43-49` precisou fazer para um estado derivado.

- Filtro `SelectFilter::make('situacao')->options(SituacaoSolicitacao::class)`.

> **Premissa verificada na revisão pós-escrita, porque as duas APIs divergem.** `Select::options()`
> do **form** detecta o enum no próprio setter e chama `enum()`
> (`vendor/filament/forms/src/Components/Concerns/HasOptions.php:20-28`); o `options()` do **filtro**
> só atribui (`vendor/filament/tables/src/Filters/Concerns/HasOptions.php:26-31`) — a expansão
> acontece depois, em `getOptions()` (`:36-63`), que **usa `getLabel()` quando o enum implementa
> `HasLabel`**. Funciona nos dois casos, e nos dois os rótulos saem em pt-BR — mas por caminhos
> diferentes, e só um deles falharia se o enum deixasse de implementar o contrato.
- **Ações de registro** — cada uma com `->visible()` pela situação **e** `->authorize()`/policy, para
  não haver botão que resulte em 403:

| Ação | Visível quando | Confirmação | Chama |
|---|---|---|---|
| `Enviar` | `situacao === Rascunho` **e** é o solicitante | `requiresConfirmation()` | `enviar(Auth::user())` |
| `Aprovar` | há etapa pendente **e** o usuário é o aprovador da vez | `requiresConfirmation()` | `aprovar(Auth::user())` |
| `Rejeitar` | idem `Aprovar` | **modal com formulário** | `rejeitar(Auth::user(), $data['justificativa'])` |
| `Cancelar` | `situacao->emTransito()` **e** é o solicitante | `requiresConfirmation()` | `cancelar(Auth::user())` |
| `EditAction` / `DeleteAction` | pela policy (rascunho + dono) | nativa | — |

- A modal de rejeição, no molde de `ConvidaEmMassa` (`:49,56-61`) — `->schema()` confirmado em
  `vendor/filament/actions/src/Concerns/HasSchema.php:26`:

```php
Action::make('rejeitar')
    ->label('Rejeitar')
    ->icon(Heroicon::OutlinedXMark)
    ->color('danger')
    ->modalHeading('Rejeitar solicitação')
    ->modalDescription('A solicitação volta para rascunho e o solicitante vê o motivo.')
    ->modalSubmitActionLabel('Rejeitar')
    ->schema([
        Textarea::make('justificativa')
            ->label('Motivo da rejeição')
            ->required()          // ← protege a TELA
            ->rows(4)
            ->helperText('O solicitante lê este texto para corrigir e enviar de novo.'),
        // Sem `->minLength(n)`: o card exige que a justificativa EXISTA (RQ-07), não
        // que ela tenha um tamanho. Um mínimo inventado rejeita "Sem verba", que é
        // uma justificativa perfeitamente válida — e política de negócio arbitrada
        // pelo desenvolvedor é o tipo de regra que ninguém sabe de onde veio.
    ])
    // Sem `requiresConfirmation()`: a modal de formulário JÁ é a confirmação — a mesma
    // decisão comentada em ConvidaEmMassa.php:75.
    ->visible(fn (SolicitacaoCompra $record): bool => $record->podeSerDecididaPor(Auth::user()))
    ->action(fn (SolicitacaoCompra $record, array $data) => $record->rejeitar(Auth::user(), $data['justificativa']))
    ->successNotificationTitle('Solicitação rejeitada');
```

**c) Infolist da página `view`** (`Schemas/SolicitacaoCompraInfolist.php`) — RQ-12 e **RQ-13**

- `Section::make('Solicitação')`: descrição, valor (`->money('BRL')`), centro de custo, solicitante,
  situação em badge.
- `Section::make('Histórico de aprovação')` com um `RepeatableEntry` sobre `etapas`: **etapa, decisão,
  quem decidiu, quando e a justificativa**. É esta seção, e só ela, que entrega RQ-13 por inteiro —
  a listagem mostra o *status*, esta mostra *quem*.
- Molde de infolist do projeto: `app/Filament/Infra/Resources/AiRuns/Schemas/AiRunInfolist.php:21-48`.

- **Logs**: nenhum nas telas. **Todos os logs da feature vivem no model** (passo 5), que é o que
  todas as ações chamam — logar também aqui duplicaria cada linha do arquivo. A única exceção do
  projeto a essa regra (`ConvitesTable.php:86-95`) existe porque ali a ação é um `DeleteAction`
  nativo, sem método de model para logar; aqui não é o caso.

### 10. Infra de teste — a suíte `FeatureTenancy`

> Skills: `pest-testing`

**Este passo nasceu ao escrever o `04` e o `05`, não do plano original.**

Dois CTs desta feature (isolamento por organização e resolução do papel `diretor` no contexto certo)
precisam de `permission.teams` ligado — ou seja, de `Tests\TenancyTestCase`, que fixa a flag em
`createApplication()`, **antes** das migrations (`tests/Pest.php:48-65`). E o Pest **não permite dois
TestCases na mesma pasta**, então `tests/Feature` (registrada com `TestCase`, `tests/Pest.php:22-24`)
não pode recebê-los.

As duas pastas com `TenancyTestCase` que já existem — `tests/Tenancy` e `tests/BrowserTenancy` —
estão no **grupo `kit`** e na testsuite `Tenancy`. Pôr testes de negócio ali quebra um contrato
documentado: `wikis/convencoes.md` diz *"Suíte do kit isolada em `tests/Kit/`; a sua em
`tests/Feature` e `tests/Unit`"*, e `tests/Pest.php:30-40` explica que `composer test:kit` é o
**comando de resposta rápida depois de um `kit:update`**.

- **Path**: `tests/Pest.php` — bloco novo, depois do de `Feature`, **sem `->group('kit')`**:

```php
/*
| Testes do SEU projeto que precisam de multi-tenancy.
|
| Pasta própria pela MESMA razão que separa tests/Tenancy de tests/Kit: o TenancyTestCase
| fixa `permission.teams` em createApplication(), antes das migrations, e o Pest não permite
| dois TestCases na mesma pasta.
|
| E separada de tests/Tenancy porque AQUELA é do kit (grupo `kit`, dentro do
| `composer test:kit`). Esta é do negócio.
*/
pest()->extend(TenancyTestCase::class)
    ->use(RefreshDatabase::class)
    ->in('FeatureTenancy');
```

- **Path**: `phpunit.xml` — testsuite nova ao lado de `Feature`:

```xml
<testsuite name="FeatureTenancy">
    <directory>tests/FeatureTenancy</directory>
</testsuite>
```

  **Sem isso a pasta não é varrida e os CTs passam por não existirem** — foi exatamente o que a wiki
  `identidade-visual-da-organizacao` registrou em Desvios do Plano ao criar `tests/BrowserTenancy`.
- **Critério de aceite**: `php artisan test` inclui a pasta nova; `vendor/bin/pest --group=kit`
  **não** a inclui e continua com a mesma contagem de antes.
- **Logs**: nenhum.

### 11. Testes

> Skills: `pest-testing`

- Especificação completa em `04-casos-de-teste.md` e `05-casos-de-teste-browser.md`.
- **Ordem obrigatória**, e cada item tem razão própria:
  1. **CT-18 primeiro** (`tests/Kit/PaineisTest.php`). Os dois Resources novos mudam a matriz de
     permissões, e escrever CT novo sobre suíte quebrada não mede nada.
  2. **CT-14 logo depois** — a subtração do `panel_user`. É a única barreira contra a escalada de
     A-08, e é a que não dá erro quando esquecida.
  3. **CT-11 e CT-12** (barreira chamada direto, e corrida) antes dos CT de fluxo feliz: são os que
     o caminho pela tela **nunca** exercita.
  4. Os CT-B vão delegados a sub-agente, conforme a skill.
- **Comandos** (o `.ai/rules/testes-browser.md` proíbe `--parallel` com browser, e o `--tia` exige
  run completo — logo, dois comandos, nunca um):

```bash
vendor/bin/pest --parallel --tia          # backend
vendor/bin/pest --testsuite=Browser       # telas, em série
```

### 12. Commits

Um commit por passo entregável, com gitmoji e escopo, no padrão do repositório:

- `:sparkles: compras: centro de custo e solicitacao com maquina de estados`
- `:sparkles: compras: aprovacao do gestor e do diretor por alcada`
- `:sparkles: compras: notificacao por e-mail do proximo aprovador`
- `:lock: compras: centro de custo fora da matriz do usuario comum`
- `:sparkles: compras: telas do painel app com historico de aprovacao`
- `:white_check_mark: compras: CT e CT-B do fluxo de aprovacao`
- `:memo: wiki: fluxo de aprovacao de solicitacao de compra`

## Filosofia de Implementação

> **Ponytail ativo em modo `full`.** A escada, aplicada aqui:
>
> 1. **Reutilizar**: o UPDATE condicional e a barreira de identidade são **cópias declaradas** de
>    `Convite` (`:622-631`, `:709-727`), com o `arquivo:linha` citado no comentário. O trio de traits
>    de model vem de `Projeto`. A notificação vem de `ConviteDeAcesso`. A modal com formulário vem de
>    `ConvidaEmMassa`. **Nada nesta feature é mecânica nova.**
> 2. **Feature nativa antes de código**: `HasLabel`/`HasColor` do enum entregam badge e filtro sem um
>    `match` por tela; `->money('BRL')` formata; `->scopedUnique()` valida com tenant. Nenhum dos três
>    é reimplementado.
> 3. **Sem abstração especulativa**: nenhum `ApprovalService`, nenhum `StateMachine`, nenhum pacote de
>    workflow, nenhuma tabela de configuração de fluxo. Dois níveis, porque o card tem dois — a
>    generalização para N está recusada em ADR-04, com o gatilho nomeado.
> 4. **Mínimo que funciona**: três tabelas, um enum, quatro métodos públicos de transição, uma
>    notificação, duas telas.
>
> Atalhos deliberados marcados com `ponytail:` comment. Depois, `/ponytail:ponytail-review` no diff.
>
> **Caveman ativo em modo `ultra`** na comunicação agent ↔ usuário. Os arquivos wiki (00-06), o
> código, os commits e os PRs são boundary do Caveman — prosa normal.

## Mapeamentos

### Situação × o que cada persona pode fazer

| Situação | Solicitante | Gestor do centro | Diretor | RQ |
|---|---|---|---|---|
| `rascunho` | editar, excluir, **enviar** | — | — | RQ-02, RQ-03, RQ-09 |
| `aguardando_gestor` | **cancelar** | **aprovar**, **rejeitar** | — | RQ-04, RQ-06, RQ-11 |
| `aguardando_diretor` | **cancelar** | — (já decidiu) | **aprovar**, **rejeitar** | RQ-05, RQ-11 |
| `aprovada` | — | — | — | RQ-10 |
| `cancelada` | — | — | — | RQ-11 |

### Valor × caminho

| Valor | Caminho | Nº de aprovações |
|---|---|---|
| R$ 4.999,99 | gestor → aprovada | 1 |
| **R$ 5.000,00** | **gestor → aprovada** | **1** — "acima de" é estritamente maior (A-04) |
| R$ 5.000,01 | gestor → diretor → aprovada | 2 |

## Testes

> `04-casos-de-teste.md` — backend: transições, alçada, barreiras chamadas direto, corrida,
> notificação, autorização, logs e o isolamento por organização.
> `05-casos-de-teste-browser.md` — CT-B: o fluxo entre três personas, a modal de justificativa e a
> ausência de affordance para quem não pode agir.

## Verificação Final

- [ ] `/ponytail:ponytail-review` no diff
- [ ] `vendor/bin/pint --dirty`
- [ ] `composer types:check` (PHPStan/larastan)
- [ ] `vendor/bin/pest --parallel --tia` — backend, incluindo `FeatureTenancy`
- [ ] `vendor/bin/pest --testsuite=Browser` — **em série**, nunca com `--parallel`
- [ ] `composer test:kit` — a fundação não se moveu (mexeu-se em `tests/Pest.php` e `phpunit.xml`)
- [ ] Os dois seeders rodados, nesta ordem: `ShieldPermissionsSeeder` → `PapeisSeeder`
- [ ] Roteiro *Desenhado × Implementado* do `05` preenchido
- [ ] `feature-quality-gate` invocado e veredito registrado no `03-progresso.md`

## Commits

Ver passo 12.
