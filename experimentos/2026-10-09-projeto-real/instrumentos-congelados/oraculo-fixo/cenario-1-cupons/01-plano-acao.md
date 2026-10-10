# Plano de Ação — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md`

## Natureza da Wiki

- **Tipo**: **nova**
- **Wiki ancestral**: não há. `Cupom` é entidade nova; nenhuma wiki anterior a descreve.
- **Motivo**: primeira entrega do domínio de desconto.

> **Ressalva que o tipo "nova" não captura, e que vale como se fosse regressão**: o passo 7 altera
> `database/seeders/PapeisSeeder.php`, que é **infraestrutura compartilhada** — ele define a matriz de
> autorização dos cinco papéis do kit. `tests/Kit/PaineisTest.php` afirma essa matriz e **precisa
> continuar verde**. Está na `## Verificação Final` como item obrigatório, e não como cortesia.

## Cobertura do Requisito

<!-- Toda cláusula do 00-requisito.md aparece aqui. Cláusula sem passo é omissão. -->

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | CRUD de cupons no painel | 8 | painel `/app` — premissa **P-09**, ver ADR-02 |
| RQ-02 | Código | 2, 4, 8 | `codigo`, string 40, normalizado em maiúsculas |
| RQ-03 | Tipo: porcentagem ou valor fixo | 2, 3, 4, 8 | `enum` PHP nativo — os dois únicos valores, garantidos pelo tipo |
| RQ-04 | Valor do desconto | 2, 4, 5, 8 | `unsignedInteger`, unidade decidida pelo tipo — premissa **P-05**, ADR-05 |
| RQ-05 | Data de validade | 2, 4, 5, 8 | `expira_em`, `timestamp` |
| RQ-06 | Limite de usos | 2, 4, 5, 8 | `limite_de_usos` + contador `usos` |
| RQ-07 | Só admin cria, edita e exclui | 6, 7 | policy por permission + recorte de escrita do `panel_user` — ADR-08 |
| RQ-08 | Os demais apenas listam os ativos | 5, 7, 8 | `scopeAtivos()` + `getEloquentQuery()` — "ativo" é derivado, premissa **P-03**, ADR-03 |
| RQ-09 | Valida que o cupom existe | 5 | `Cupom::valido()` devolve `null` |
| RQ-10 | Valida a validade | 5 | mesmo método, e **de novo** no consumo atômico |
| RQ-11 | Valida o limite de usos | 5 | idem — o `WHERE` do consumo é a barreira real, ADR-06 |
| RQ-12 | Aplica o desconto no total | 5 | `Cupom::aplicarEm()`. **O `Pedido` não existe** — premissa **P-01**, ADR-01 |
| RQ-13 | Incrementa o contador de usos | 5 | `UPDATE ... WHERE usos < limite_de_usos`, atômico |
| RQ-14 | Código não se repete | 2, 8 | `unique(['tenant_id','codigo'])` + `scopedUnique()` — premissa **P-04**, ADR-04 |
| RQ-15 | Registrar quem aplicou e quando | 2, 4, 5 | tabela `cupom_usos` — a auditoria genérica **não** alcança, premissa **P-08**, ADR-07 |

**Nenhuma cláusula sem passo.** As cinco premissas assumidas (P-01, P-03, P-04, P-05, P-08) estão
declaradas no `00-requisito.md` e defendidas em ADR — não estão escondidas dentro de um passo.

## Objetivo

Dar à organização um cupom de desconto que ela mesma cadastra, com código, tipo, valor, validade e
limite de usos, e uma regra de aplicação que **não deixa o limite ser furado** quando dois pedidos
chegam ao mesmo tempo.

A entrega é deliberadamente cortada em dois: o **cadastro**, que é tela de painel completa, e o
**motor de aplicação**, que é uma regra de model chamável por qualquer coisa — controller, job,
comando ou uma futura tela de checkout. O `Pedido` que o card cita **não existe neste projeto** (ver
`00-requisito.md` → A-01), e inventá-lo a partir de uma frase subordinada custaria mais do que a
feature inteira, entregando algo que ninguém especificou.

## Contexto

### O que existe, e o que falta

| Peça | Onde | Estado |
|---|---|---|
| Entidade de pedido / carrinho / venda | — | **Não existe.** Grep amplo em `app/`, `database/`, `routes/`, `resources/`: nenhum model, migration ou coluna monetária no projeto inteiro |
| Molde de model de negócio com tenancy | `app/Models/Projeto.php` | `TemUuid` + `BelongsToTenant` + `AuditsFillables`, `tenant_id` fora do `$fillable`. **É o molde exato do `Cupom`** |
| Molde de migration de negócio | `database/migrations/0001_01_01_000022_create_projetos_table.php:20-30` | `id` → `uuid unique` → `foreignId('tenant_id')->constrained()->cascadeOnDelete()` → colunas → `timestamps` → índice composto começando por `tenant_id` |
| Molde de FK opcional de tenant | `database/migrations/2026_08_13_000002_create_convites_table.php:39` | `$table->foreignId('tenant_id')->nullable()->constrained();` — *"Só preenchida com a tenancy ligada. A tabela `tenants` existe nos dois modos"* |
| Molde de FK de autoria | mesma migration, `:42-43` | `convidado_por_id` nullable + `nullOnDelete` — *"apagar o admin não apaga o histórico"* |
| Consumo atômico de recurso de uso limitado | `app/Models/Convite.php:622-631` | **o precedente central desta feature** — `UPDATE ... WHERE` condicional em vez de check-then-act |
| Padrão de log | `app/Models/Convite.php:172`, `:387`, `:580` | `Log::channel(...)->nivel("[Classe@metodo] Frase | chave: valor", [contexto])` |
| Channels de log | `config/logging.php:85-107` | `ai`, `tenancy`, `autenticacao`. **Nenhum de negócio** |
| Policy de model de negócio | `app/Policies/ProjetoPolicy.php` | 12 métodos, cada um `$authUser->can('{Affix}:{Model}')`. **Gerada** pelo `shield:generate` |
| Matriz de autorização | `database/seeders/PapeisSeeder.php:87-93` | subtração do `panel_user` por **FQCN inteiro** — e é justamente onde esta feature não cabe (ADR-08) |
| Resource de negócio no `/app` | `app/Filament/App/Resources/Projetos/ProjetoResource.php` | Filament 5: `form(Schema $schema): Schema`, `Filament\Actions\*`, `recordActions()`, descoberta automática |
| Factory de negócio | — | **Não existe `ProjetoFactory`.** Os testes de tenancy criam o registro à mão (`tests/Tenancy/TenancyTest.php:319`) |

### O precedente que decide o desenho: `Convite::aceitarComoUsuarioExistente()`

`app/Models/Convite.php:612-631`, lido e citado literalmente porque é a razão de ADR-06 existir:

```php
/*
 * Consumo ATÔMICO, e é aqui que esta via difere da de conta nova.
 * ...
 * O `UPDATE ... WHERE aceito_em IS NULL` é atômico no banco — a segunda recebe 0 e para
 * antes de vincular. É o defeito do `laravel-invite-only`, cujo `accept()` é
 * check-then-act puro. Ver ADR-04.
 */
$consumido = static::query()
    ->whereKey($this->getKey())
    ->whereNull('aceito_em')
    ->whereNull('recusado_em')
    ->update(['aceito_em' => now(), 'token_lembrete' => null]);

if ($consumido !== 1) {
    throw new RuntimeException('Este convite já foi usado.');
}
```

RQ-11 e RQ-13 são **exatamente o mesmo problema**, e um grau pior: convite tem limite 1; cupom tem
limite N. Ler `usos`, comparar com `limite_de_usos` e salvar `usos + 1` deixa uma janela entre a
leitura e a escrita em que outra requisição faz o mesmo — e o cupom de 100 usos é resgatado 103 vezes,
sem erro nenhum, sem log, e só descoberto na conciliação. Ver **ADR-06**.

### O que o Shield faz com um Resource novo — e o que ele **não** faz

Confirmado em `.ai/rules/filament.md:31-42` e em `database/seeders/PapeisSeeder.php:87-123`:

1. Resource novo **nasce sem permission no banco**: a tela responde 403 para todo mundo que não seja
   `master_global` (que entra pelo `Gate::before`). Rodar os dois seeders, nesta ordem, é passo do
   plano — não é "lembrar depois".
2. O `panel_user` recebe a matriz do painel `app` **menos** `permissoesDeAdministracaoDoApp()`, e essa
   subtração é **por FQCN inteiro** (`Paineis::permissoesDe()` → `->only($fqcns)`).

O ponto 2 é o achado que muda o passo 7: **a subtração existente é tudo-ou-nada**. Pôr
`CupomResource` na lista tira também `ViewAny:Cupom`, e RQ-08 exige que os demais usuários
**consigam listar**. Deixar fora da lista dá `Create:Cupom` e `Delete:Cupom` a todo usuário comum, e
RQ-07 diz que **só admin** cria e exclui. Nenhuma das duas opções existentes atende o card. Ver
**ADR-08**.

### O modo single-tenant expõe uma lacuna de papel

`PapeisSeeder.php:70-73`: o papel **`admin_organizacao` só é criado quando
`config('kit.tenancy.enabled')` está ligado**. Com a tenancy desligada — que é o default do kit
(`config/kit.php:59`) — os únicos papéis com acesso ao `/app` são `panel_user` e `master_global`.

Consequência para RQ-07, e ela precisa estar escrita: **em modo single-tenant, quem cria cupom é o
`master_global`**, pelo `Gate::before`. O `panel_user` fica com leitura, exatamente como RQ-08 pede.
Não se cria papel novo para tapar isso: papel novo é decisão de produto, não de feature, e o card não
pediu nenhum. Registrado em ADR-02 e coberto por CT-08.

## Autorização

Modelo: **permission-driven**, como todo o kit — a policy pergunta ao spatie, e quem preenche o spatie
é o `PapeisSeeder`.

- **Policy**: `app/Policies/CupomPolicy.php` — **gerada** por `shield:generate` no passo 6, no molde
  exato de `ProjetoPolicy` (12 métodos, cada um `$authUser->can('{Affix}:Cupom')`). Não escrever à
  mão: o seeder roda com `--ignore-existing-policies`, e uma policy manual seria preservada mas
  divergiria do padrão na primeira mudança do Shield.
- **Gates**: nenhum novo. O `Gate::before` do `master_global` continua sendo a exceção que atravessa
  tudo (`config/filament-shield.php` → `super_admin`).
- **Middleware**: nenhum novo. O `/app` já tem o dele, e a tenancy acrescenta
  `DefinirTenantDePermissoes` via `tenantMiddleware` (`AppPanelProvider.php:285-289`).
- **Matriz de papéis** (o que o passo 7 produz):

| Papel | Painel | `ViewAny`/`View:Cupom` | `Create`/`Update`/`Delete:Cupom` | Origem |
|---|---|---|---|---|
| `master_global` | todos | ✅ | ✅ | `Gate::before` — sem permission no banco |
| `admin_organizacao` | `app` | ✅ | ✅ | matriz inteira do painel `app` (só existe com tenancy ligada) |
| `panel_user` | `app` | ✅ | ❌ | matriz do `app` **menos as chaves de escrita de `Cupom`** — passo 7 |
| `admin` | `admin` | — | — | não alcança o `/app` (`roles.painel = 'admin'`) |
| `infra` | `infra` | — | — | idem |

- **Escopo não é autorização** (`wikis/convencoes.md`): o `BelongsToTenant` impede ver cupom de outra
  organização; a policy impede o usuário comum de escrever. As duas coisas são necessárias e nenhuma
  substitui a outra.

## Rotas

Nenhuma rota escrita à mão. Todas são geradas pelo Resource, e o painel `/app` já descobre resources
sozinho (`AppPanelProvider.php:70`):

| Método | URI | Name | Middleware |
|--------|-----|------|------------|
| GET | `/app/{tenant}/cupons` | `filament.app.resources.cupons.index` | o do painel `app` + `tenantMiddleware` |
| GET | `/app/{tenant}/cupons/create` | `…cupons.create` | idem |
| GET | `/app/{tenant}/cupons/{record}/edit` | `…cupons.edit` | idem |

Com `kit.tenancy.enabled = false` as mesmas rotas existem sem o segmento `{tenant}`
(`/app/cupons`) — é o painel `/app` no modo single-tenant.

> `{record}` é o **uuid**, não o id: `TemUuid::getRouteKeyName()` devolve `'uuid'`. Isso vale para os
> CT-B, que montam URL.

## Superfície de UI

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| `CuponsTable` (listagem) | Filament Table | `/app/{tenant}/cupons` | lê a lista, ordena, busca por código, vê a situação em badge | **Sim** (Livewire) |
| `CupomForm` — criar | Filament Schema | `/app/{tenant}/cupons/create` | digita código, **escolhe o tipo e o campo de valor muda de rótulo/sufixo**, escolhe validade e limite | **Sim** |
| `CupomForm` — editar | Filament Schema | `/app/{tenant}/cupons/{record}/edit` | idem | **Sim** |
| `DeleteAction` na linha | Filament Action | `/app/{tenant}/cupons` | exclui com modal de confirmação | **Sim** |

**Gate de CT-B**: 4 linhas na tabela, todas `Depende de JS? = Sim`, **e** a interação de criar
atravessa 2 telas (listagem → formulário → volta com o registro na lista) → **criar
`05-casos-de-teste-browser.md`**. ✅

E há um motivo específico desta feature, além do gate: o campo `valor` **muda de significado conforme
o `Select` de tipo** (ADR-05). Um `->live()` mal ligado deixa o rótulo dizendo "R$" enquanto o valor é
gravado como porcentagem — o registro fica **correto no banco e mentiroso na tela**, e nenhum teste
HTTP vê isso, porque o HTML inicial é idêntico nos dois casos.

## Variáveis de Ambiente

| Key | Default | Descrição |
|-----|---------|-----------|
| `LOG_CUPOM_LEVEL` | herda `LOG_LEVEL` (`debug`) | nível do channel `cupom`, no molde de `LOG_AI_LEVEL` e `LOG_TENANCY_LEVEL` (`config/logging.php:88,96`) |

Nenhuma outra. **Em particular, nada de `CUPOM_DESCONTO_MAXIMO` ou afins**: o card não pede teto, e
config sem requisito é opção que ninguém sabe ajustar.

> Acrescentar a chave ao `.env.example` junto do bloco `LOG_*` (`:19-22`) — o kit documenta as chaves
> lá, e chave sem entrada no exemplo é chave que ninguém descobre.

## Eventos / Listeners / Observers

**Nenhum.** A normalização do código (maiúsculas, sem espaços) vive no *mutator* do model, que é uma
linha e roda em qualquer via de escrita — tela, seeder, tinker, teste. Um Observer para isso seria um
arquivo, um registro e um lugar a mais para procurar.

## Jobs / Queues

**Nenhum.** Validar e consumir cupom é síncrono por natureza: quem chama precisa da resposta para
saber o valor a cobrar. Enfileirar seria devolver "talvez" para uma pergunta que exige "sim ou não".

## Impacto em Features Existentes

| Feature | O que pode quebrar e por quê |
|---|---|
| **Matriz de permissões** (`tests/Kit/PaineisTest.php`) | o `CupomResource` acrescenta ~12 permissions ao painel `app`. A contagem medida hoje é **38 (36 de Resource + 2 de Page)** e vai mudar. Se o teste afirma número absoluto, ele **vai ficar vermelho e está certo** — atualizar o número é parte do passo 7, não conserto de teste |
| **`PapeisSeeder`** | o passo 7 acrescenta um segundo recorte ao `panel_user`. Errar aqui tem o custo já nomeado em `.ai/rules/filament.md`: *"todo usuário comum do negócio vira administrador da organização — sem migration, sem 403, sem log"*. É o risco mais caro do plano |
| **`tests/Tenancy/TenancyTest.php`** | afirma o recorte por organização. `Cupom` é a segunda model com `BelongsToTenant`; se o escopo global regredir, quebra aqui antes de quebrar no cupom |
| **Navegação do painel `/app`** | o painel hoje tem `Projetos` (demo), `Usuários` e `Convites`. O item novo entra por descoberta automática — nada a registrar, mas a ordem do menu muda |
| **Trilha de auditoria** (`/infra/audits`) | `Cupom` implementa `Auditable`, então criar/editar/excluir cupom passa a gerar registro. Volume novo na tabela `audits`, sem mudança de esquema |
| **`composer test:kit`** | ganha os CT novos. O tempo do grupo `kit` cresce; nenhum teste existente depende de contagem total de cenários |

## Rollback

- **Migration down**: `dropIfExists('cupom_usos')` e depois `dropIfExists('cupons')` — **nesta ordem**,
  porque `cupom_usos.cupom_id` tem FK para `cupons`. Duas migrations separadas, então o `migrate:rollback`
  de um passo já as desfaz na ordem inversa da criação; o `down()` de cada uma cuida só da sua tabela.
- **Reversão do `PapeisSeeder`**: reverter o arquivo e rodar `db:seed --class=PapeisSeeder` de novo. O
  seeder é idempotente e usa `syncPermissions()`, que **substitui** a matriz — não sobra permission
  órfã.
- **Desligar sem reverter**: não há feature flag, e é deliberado — a feature é inerte por construção.
  Sem nenhum cupom cadastrado, `Cupom::valido()` devolve `null` para qualquer código, e a tela mostra
  a lista vazia. Uma flag serviria para esconder o menu, o que `canAccess()` já faz por permissão.
- **Dados**: cupons e usos ficam. `cupom_usos` é trilha (RQ-15) — apagar trilha em rollback é apagar a
  evidência de que a feature rodou.

## Dependências

**Nenhum pacote novo.** Tudo já está instalado:

| Peça | Origem |
|---|---|
| `Filament\Forms\Components\{TextInput, Select, DateTimePicker}` | `filament/forms` ^5.6 |
| `Filament\Tables\Columns\TextColumn` (com `->badge()`) | `filament/tables` ^5.6 |
| `->scopedUnique()` | `filament/forms`, exigido por `wikis/convencoes.md` em modo tenancy |
| `App\Traits\{TemUuid, BelongsToTenant, AuditsFillables}` | já no projeto |
| `pestphp/pest` ^5.1 + `pest-plugin-browser` ^5.0 | `composer.json:78-79` |
| `enum` nativo com `Filament\Support\Contracts\HasLabel` | PHP 8.3 + `filament/support` |

## Riscos

| Risco | Mitigação |
|---|---|
| **O limite de usos ser furado por concorrência** — dois resgates simultâneos passando pelo mesmo `if` | consumo por `UPDATE ... WHERE usos < limite_de_usos`, atômico no banco (ADR-06). CT-05 é escrito para falhar sem ele |
| **`panel_user` herdar `Create:Cupom`** e todo usuário comum passar a emitir desconto | recorte explícito no passo 7 + **CT-07, que afirma a ausência da permission**. É o CT que não pode faltar |
| **A tela mentir sobre a unidade do valor** (rótulo "R$" com valor em porcentagem) | `Select` de tipo `->live()`, rótulo e sufixo do campo derivados dele; CT-B01 confere o texto visível após trocar o tipo |
| **Código duplicado entre organizações ser barrado** por `unique()` em vez de `scopedUnique()` | ADR-04; CT-04 cria o mesmo código em duas organizações e exige que **passe** |
| **A trilha de RQ-15 nascer vazia** porque o `increment()` do Query Builder não dispara evento de model | tabela própria `cupom_usos`, gravada explicitamente na mesma transação (ADR-07). CT-06 assere a linha |
| **`PaineisTest` quebrar e alguém "consertar"** afrouxando a asserção | o passo 7 diz explicitamente que a contagem **deve** ser atualizada, e por quê |
| **Cupom expirado continuar listado** para o usuário comum | `scopeAtivos()` no `getEloquentQuery()` de quem não tem `Update:Cupom`; CT-09 |
| **Modo single-tenant sem papel administrador do `/app`** | documentado em ADR-02; CT-08 fixa o comportamento em vez de deixá-lo por acaso |

## Channel de Log da Feature

### Verificação de Channel Existente

`config/logging.php` lido inteiro. Channels do kit hoje: **`ai`** (`:85`), **`tenancy`** (`:93`) e
**`autenticacao`** (`:101`). Não há channel de negócio. `Grep` por `Log::channel(` em `app/`: só esses
três.

O comentário de bloco do próprio arquivo (`:76-83`) declara a política: *"um canal por camada
transversal (padrão: **um canal por feature**, sempre daily/14 dias, visíveis no Logs Explorer do
/infra)"*.

### Decisão

**Channel novo: `cupom`.** Nenhum dos três existentes serve — desconto não é IA, não é tenancy e não é
autenticação. Primeiro passo de implementação, em `config/logging.php`, no molde exato dos vizinhos:

```php
'cupom' => [
    'driver'               => 'daily',
    'path'                 => storage_path('logs/cupom.log'),
    'level'                => env('LOG_CUPOM_LEVEL', env('LOG_LEVEL', 'debug')),
    'days'                 => 14,
    'replace_placeholders' => true,
],
```

> `env('LOG_CUPOM_LEVEL', env('LOG_LEVEL', 'debug'))` — o duplo default é o que `ai` e `tenancy` fazem
> (`:88`, `:96`). O `autenticacao` **não** tem env própria (`:104`); é inconsistência do kit, e o molde
> a seguir é o da maioria.

Todos os logs desta feature usam `Log::channel('cupom')`, no formato `[Classe@metodo] mensagem` com
context estruturado, conforme `wikis/convencoes.md` → "Padrão de log".

## Ponto de Integração (P-01 — o `Pedido` que não existe)

Esta seção existe porque RQ-12 fala de um agregado ausente. Ela é o **contrato** que o dia do `Pedido`
vai consumir, e é o que torna a premissa P-01 auditável em vez de conveniente.

```php
// Assinatura pública, estável, chamável de controller, job, comando ou Livewire:
$total = 12_990;                                  // R$ 129,90 em centavos
$cupom = Cupom::valido($request->string('codigo')); // null = não existe, expirado ou esgotado

if ($cupom === null) {
    // RQ-09 / RQ-10 / RQ-11 — quem chama decide a mensagem para o usuário final
}

$totalComDesconto = $cupom->aplicarEm($total, $request->user()); // RQ-12 + RQ-13 + RQ-15
```

**O que esta entrega NÃO faz** e está fora de escopo por declaração do `00-requisito.md`: não existe
tela onde alguém digita o código, não existe `Pedido` para guardar o `cupom_id`, e não existe endpoint
público. O que existe é a regra, com a assinatura acima, coberta por CT unitário.

## Estrutura de Implementação

### 1. Channel de log `cupom`

> Skills: `laravel-best-practices`

- **Path**: `config/logging.php` — acrescentar o bloco `'cupom' => [...]` **depois** de `autenticacao`
  (`:107`), mantendo o agrupamento dos channels do kit.
- **Path**: `.env.example` — `LOG_CUPOM_LEVEL=` no bloco `LOG_*` (`:19-22`), com comentário de uma
  linha dizendo que vazio herda `LOG_LEVEL`.
- **Critério de aceite**: `Log::channel('cupom')->debug('teste')` cria `storage/logs/cupom-*.log`.
- **Logs**: nenhum — configuração.

### 2. Migrations — `cupons` e `cupom_usos`

> Skills: `laravel-best-practices`

**Path**: `database/migrations/2026_08_14_000004_create_cupons_table.php`

```php
Schema::create('cupons', function (Blueprint $table): void {
    $table->id();
    $table->uuid('uuid')->unique();

    // Nullable, como em `convites`: a tabela `tenants` existe nos dois modos, mas
    // `tenant_id` só é preenchida com a tenancy ligada (quem preenche é BelongsToTenant).
    $table->foreignId('tenant_id')->nullable()->constrained()->cascadeOnDelete();

    // 40 chars: código de cupom é humano — digitado, ditado ao telefone, colado de e-mail.
    // Sem `->unique()` isolado: a unicidade é COMPOSTA com tenant_id (RQ-14, ADR-04).
    $table->string('codigo', 40);

    // String, não enum de banco: enum nativo do MySQL exige ALTER para um valor novo, e o
    // SQLite (usado nos testes, phpunit.xml:53-54) nem o tem. Quem garante os dois únicos
    // valores é o enum do PHP no cast (ADR-05).
    $table->string('tipo', 20);

    // unsignedInteger, unidade decidida pelo `tipo`: centavos quando fixo, pontos
    // percentuais inteiros (1..100) quando porcentagem. Ver ADR-05.
    $table->unsignedInteger('valor');

    // timestamp e não date: a comparação é `> now()`, e uma date compararia contra
    // meia-noite, encurtando a validade em um dia inteiro sem ninguém pedir.
    $table->timestamp('expira_em');

    $table->unsignedInteger('limite_de_usos');

    // Contador. FORA do $fillable: quem o move é o UPDATE atômico de aplicarEm().
    $table->unsignedInteger('usos')->default(0);

    $table->timestamps();

    // RQ-14: unicidade POR ORGANIZAÇÃO. Em single-tenant, tenant_id é NULL e a maioria
    // dos bancos NÃO considera dois NULLs iguais — a barreira real do modo single-tenant
    // é o scopedUnique() do formulário. Anotado como limite conhecido em ADR-04.
    $table->unique(['tenant_id', 'codigo']);

    // Sem índice adicional. `valido()` consulta por (tenant_id, codigo) e cai no unique
    // acima; a listagem ordena dezenas de linhas. Um `index(['tenant_id','expira_em'])`
    // estava aqui e foi cortado pelo /ponytail:ponytail-review — índice para volume que
    // esta tabela não tem. Acrescentar quando houver medição dizendo que falta.
});
```

**Path**: `database/migrations/2026_08_14_000005_create_cupom_usos_table.php`

```php
Schema::create('cupom_usos', function (Blueprint $table): void {
    $table->id();

    // cascadeOnDelete: apagar o cupom apaga a trilha dele. A alternativa (restrict) faria
    // o DeleteAction da tela falhar com erro de FK no primeiro cupom já usado — e RQ-07
    // dá ao admin o direito de excluir.
    $table->foreignId('cupom_id')->constrained('cupons')->cascadeOnDelete();

    // RQ-15 — QUEM. nullOnDelete no molde de `convites.convidado_por_id`: apagar o usuário
    // não apaga o registro do desconto concedido.
    $table->foreignId('aplicado_por_id')->nullable()->constrained('users')->nullOnDelete();

    // O valor sobre o qual o desconto incidiu e o desconto concedido, ambos em centavos.
    // Sem eles a trilha diz "alguém usou" e não "quanto se deu de desconto" — que é a
    // pergunta que faz alguém auditar cupom. Ver ADR-07.
    $table->unsignedInteger('valor_original');
    $table->unsignedInteger('valor_desconto');

    // `foreignId()->constrained()` já cria índice em `cupom_id`, que é a única coluna por
    // onde esta tabela é consultada. Nenhum índice a mais.
    $table->timestamps();   // RQ-15 — QUANDO (created_at)
});
```

- **`down()`**: `Schema::dropIfExists('cupom_usos')` / `Schema::dropIfExists('cupons')`, cada um na sua
  migration.
- **Sem `uuid` em `cupom_usos`**: `TemUuid` existe para não expor id sequencial **em rota**, e esta
  tabela não tem rota. Coluna única a mais sem uso é índice a mais em toda inserção.
- **Logs**: nenhum — migration.

### 3. Enum `TipoDeDesconto`

> Skills: `laravel-best-practices`

- **Path**: `app/Enums/TipoDeDesconto.php` (pasta nova — não há `app/Enums/` hoje; confirmado por
  `ls app/`)

```php
enum TipoDeDesconto: string implements HasLabel
{
    case Porcentagem = 'porcentagem';
    case Fixo        = 'fixo';

    /** Rótulo em pt-BR, como manda `wikis/convencoes.md` → Idioma. */
    public function getLabel(): string
    {
        return match ($this) {
            self::Porcentagem => 'Porcentagem',
            self::Fixo        => 'Valor fixo',
        };
    }

}
```

> **Sem método `sufixo()`**: a primeira versão do plano tinha um, para alimentar `->suffix()` no
> formulário. O `/ponytail:ponytail-review` cortou o par — o **rótulo** do campo já diz a unidade
> ("Percentual de desconto" × "Valor do desconto (centavos)"), e um sufixo ao lado repetia a mesma
> informação. Método sem chamador saiu junto.

- **`TitleCase` nos nomes dos cases**, como cobra o Boost (`wikis/convencoes.md` → "Estilo e
  ferramentas").
- **`HasLabel`** faz o `Select` do Filament renderizar o rótulo sozinho, sem array de opções
  duplicado na tela — é o que evita o rótulo divergir do enum.
- **RQ-03 fica garantido pelo tipo**: um valor fora dos dois estoura no cast, não numa validação que
  alguém pode esquecer de aplicar.
- **Logs**: nenhum.

### 4. Models `Cupom` e `CupomUso`

> Skills: `eloquent-best-practices`

**Path**: `app/Models/Cupom.php` — molde exato de `Projeto` (`app/Models/Projeto.php:27-35`):

```php
class Cupom extends Model implements Auditable
{
    use AuditsFillables;
    use BelongsToTenant;
    use HasFactory;
    use TemUuid;

    protected $table = 'cupons';   // o plural do Eloquent para "Cupom" seria "cupoms"

    protected $fillable = [
        'codigo',
        'tipo',
        'valor',
        'expira_em',
        'limite_de_usos',
    ];

    protected function casts(): array
    {
        return [
            'tipo'      => TipoDeDesconto::class,
            'expira_em' => 'datetime',
        ];
    }
}
```

- **`usos`, `uuid` e `tenant_id` ficam FORA do `$fillable`**, cada um por um motivo diferente:
  `tenant_id` porque quem o preenche é a trait; `uuid` por convenção do kit; **`usos` porque ele é
  contador, e mass assignment num contador é o caminho para alguém "corrigir" o valor pela tela**. É a
  mesma razão que mantém `Convite::$token` fora (`wikis/convencoes.md` → Armadilhas).
- **Consequência em RQ-15**: `AuditsFillables::getAuditInclude()` devolve o `$fillable`, então `usos`
  **não** entra na trilha de `/infra/audits`. Isso é intencional e é metade do argumento de ADR-07.
- **Mutator do código** — normalização numa via só:

```php
/**
 * Código sempre em maiúsculas e sem espaços nas pontas.
 *
 * Mutator e não Observer: roda em QUALQUER via de escrita (tela, seeder, tinker, teste),
 * e é o que faz `unique(['tenant_id','codigo'])` significar o que o usuário espera —
 * `bemvindo` e `BEMVINDO` seriam duas linhas num índice sensível a caixa.
 */
protected function codigo(): Attribute
{
    return Attribute::set(fn (string $valor): string => mb_strtoupper(trim($valor)));
}
```

**Path**: `app/Models/CupomUso.php` — model magro, **sem** `BelongsToTenant` e **sem** `Auditable`:

```php
class CupomUso extends Model
{
    protected $table = 'cupom_usos';

    protected $fillable = ['cupom_id', 'aplicado_por_id', 'valor_original', 'valor_desconto'];
}
```

- **Sem relações `cupom()` e `aplicadoPor()`**: cortadas pelo `/ponytail:ponytail-review`. Nenhuma tela
  exibe a trilha nesta entrega e nenhum CT navega por elas — os casos consultam por
  `CupomUso::count()` e `assertDatabaseHas`. Acrescentar no dia em que existir o primeiro leitor, que
  é quando se saberá qual das duas ele precisa.

- **Por que sem `BelongsToTenant`**: `cupom_usos` não tem `tenant_id` — o recorte vem do `cupom_id`,
  e o cupom já é escopado. Duplicar a coluna criaria duas fontes para o mesmo fato, e a segunda
  poderia divergir.
- **Por que sem `Auditable`**: a tabela **é** a trilha. Auditar a trilha é registrar que se registrou.
- **Logs**: nenhum — os dois models não têm lógica de fluxo neste passo.

### 5. A regra de negócio — `valido()` e `aplicarEm()`

> Skills: `eloquent-best-practices`, `ponytail`

**Path**: `app/Models/Cupom.php` (mesmo arquivo do passo 4). É o passo central: RQ-08 a RQ-13 e RQ-15.

#### 5.1 `scopeAtivos()` — a definição única de "ativo" (RQ-08)

```php
/**
 * Cupom ativo: dentro da validade E com uso disponível.
 *
 * Não existe coluna `ativo`, de propósito: ela seria uma TERCEIRA fonte de verdade ao lado
 * de `expira_em` e `limite_de_usos`, e as três divergiriam. Ver ADR-03 — é a mesma razão
 * de `Convite::situacao()` ser derivado.
 */
public function scopeAtivos(Builder $query): Builder
{
    return $query
        ->where('expira_em', '>', now())
        ->whereColumn('usos', '<', 'limite_de_usos');
}
```

#### 5.2 `situacao()` — o rótulo da tela, derivado da mesma regra

```php
/** Ordem importa: esgotado vence expirado, porque quem esgotou cumpriu o seu papel. */
public function situacao(): string
{
    return match (true) {
        $this->usos >= $this->limite_de_usos   => 'Esgotado',
        $this->expira_em->isPast()             => 'Expirado',
        default                                => 'Ativo',
    };
}
```

#### 5.3 `valido()` — RQ-09, RQ-10, RQ-11

```php
/**
 * O cupom deste código, se existir e estiver ativo. `null` para os três motivos de recusa.
 *
 * Espelha `Convite::valido()` (`app/Models/Convite.php:453`): uma consulta só, com todos
 * os filtros, em vez de buscar e depois testar em PHP — o que deixaria três caminhos
 * diferentes de "não vale" espalhados por quem chama.
 *
 * O escopo global de `BelongsToTenant` continua ativo aqui: código de OUTRA organização
 * não é encontrado, e isso é isolamento, não validação.
 */
public static function valido(?string $codigo): ?self
{
    if (blank($codigo)) {
        return null;
    }

    return static::query()
        ->where('codigo', mb_strtoupper(trim($codigo)))
        ->ativos()
        ->first();
}
```

- **Logs** (motivo sempre no context — é a pergunta que alguém vai fazer):

```php
Log::channel('cupom')->info(
    "[Cupom@valido] Código recusado | codigo: {$codigo} - motivo: {$motivo}",
    ['codigo' => $codigo, 'motivo' => $motivo, 'tenant_id' => $tenantId],
);
```
  com `motivo` ∈ `{codigo_vazio, nao_encontrado}`. **`nao_encontrado` cobre as três recusas de
  propósito**: distinguir "não existe" de "expirado" de "esgotado" numa mensagem devolvida ao cliente
  final é oráculo de enumeração de códigos. O log **interno** guarda a distinção via `situacao()`
  quando o registro existe mas não está ativo — quem opera precisa saber, quem digita não.

#### 5.4 `aplicarEm()` — RQ-12, RQ-13, RQ-15 e a barreira de concorrência

```php
/**
 * Aplica o desconto a um total e CONSOME um uso. Devolve o total já com desconto, em centavos.
 *
 * Consumo ATÔMICO, pelo mesmo motivo e no mesmo formato de
 * `Convite::aceitarComoUsuarioExistente()` (`Convite.php:622-631`): ler `usos`, comparar
 * com `limite_de_usos` e salvar `usos + 1` deixa uma janela entre a leitura e a escrita.
 * Convite tem limite 1 e o `unique` do e-mail o salvaria; cupom tem limite N e **não há
 * unique que salve** — duas requisições simultâneas passariam as duas. O
 * `WHERE usos < limite_de_usos` é resolvido pelo banco dentro do próprio UPDATE. Ver ADR-06.
 *
 * A validade é reconferida AQUI, e não só em `valido()`: entre uma chamada e outra pode ter
 * passado a meia-noite. Custa uma cláusula no WHERE que já existe.
 *
 * @throws RuntimeException quando o cupom expirou ou esgotou entre a validação e o consumo
 */
public function aplicarEm(int $valorTotalEmCentavos, ?User $aplicadoPor = null): int
{
    return DB::transaction(function () use ($valorTotalEmCentavos, $aplicadoPor): int {
        $consumido = static::query()
            ->whereKey($this->getKey())
            ->where('expira_em', '>', now())
            ->whereColumn('usos', '<', 'limite_de_usos')
            ->increment('usos');

        if ($consumido !== 1) {
            // log warning + throw
        }

        $desconto = $this->descontoSobre($valorTotalEmCentavos);

        // RQ-15 — a trilha, na MESMA transação do consumo: contador movido sem trilha é
        // pior que os dois ausentes, porque some sem deixar vestígio.
        CupomUso::create([
            'cupom_id'        => $this->getKey(),
            'aplicado_por_id' => $aplicadoPor?->getKey(),
            'valor_original'  => $valorTotalEmCentavos,
            'valor_desconto'  => $desconto,
        ]);

        return max(0, $valorTotalEmCentavos - $desconto);
    });
}
```

- **`->increment('usos')` no Query **Builder**, não no model**: o do model dispara eventos; o do builder
  não. É o que garante o UPDATE único — e é também o que **impede a trilha de auditoria de registrar
  o uso**, o que fecha o argumento de ADR-07 e é a razão de `cupom_usos` existir.
- **`DB::transaction`**: o UPDATE já é atômico sozinho; a transação existe para que a **trilha** não
  se separe dele. Sem ela, uma falha na inserção deixaria o contador movido sem registro de quem usou.
- **`max(0, ...)`** — premissa P-07: desconto maior que o total resulta em zero, nunca negativo.

#### 5.5 `descontoSobre()` — o cálculo, isolado e testável (RQ-12)

```php
/**
 * O desconto em centavos, para um total em centavos.
 *
 * `intdiv` TRUNCA — premissa P-06 do `00-requisito.md`: o card não disse para onde vai a
 * fração, e truncar nunca concede mais do que o cupom promete. 10% de 9.999 = 999, não 1.000.
 * Público para ser testável direto, sem consumir uso.
 */
public function descontoSobre(int $valorTotalEmCentavos): int
{
    return match ($this->tipo) {
        TipoDeDesconto::Porcentagem => intdiv($valorTotalEmCentavos * $this->valor, 100),
        TipoDeDesconto::Fixo        => $this->valor,
    };
}
```

- **`match` sobre o enum, sem `default`**: se um terceiro tipo nascer, o PHP estoura
  `UnhandledMatchError` em vez de aplicar silenciosamente o ramo errado.

- **Logs do passo 5** (todos em `Log::channel('cupom')`, formato `[Cupom@metodo]`):

| Ponto | Nível | Mensagem | Context |
|---|---|---|---|
| `valido()` recusa | `info` | `[Cupom@valido] Código recusado \| codigo: {codigo} - motivo: {motivo}` | `codigo`, `motivo`, `tenant_id` |
| `aplicarEm()` sucesso | `info` | `[Cupom@aplicarEm] Desconto aplicado \| cupom: {id} - desconto: {centavos}` | `cupom_id`, `codigo`, `tipo`, `valor_original`, `valor_desconto`, `aplicado_por`, `usos_apos`, `limite_de_usos`, `tenant_id` |
| `aplicarEm()` corrida perdida | `warning` | `[Cupom@aplicarEm] Consumo recusado no UPDATE atômico \| cupom: {id} - motivo: esgotado_ou_expirado` | `cupom_id`, `codigo`, `usos`, `limite_de_usos`, `expira_em` (ISO-8601), `motivo` |

  **`warning` e não `error`** na corrida perdida: é condição esperada de disputa, tratada e devolvida
  ao chamador — a mesma severidade que `Convite::exigirDono()` usa ao recusar (`Convite.php:715`).

### 6. Policy e permissões

> Skills: `laravel-best-practices`

- **Path**: `app/Policies/CupomPolicy.php` — **gerada**, não escrita à mão, pelo passo abaixo. O
  resultado tem os mesmos 12 métodos de `ProjetoPolicy`, com `declare(strict_types=1)` e
  `Illuminate\Foundation\Auth\User as AuthUser`.
- **Ordem obrigatória** (`.ai/rules/filament.md:33-38`), **depois** de o Resource do passo 8 existir:

```bash
php artisan db:seed --class=Database\\Seeders\\ShieldPermissionsSeeder
php artisan db:seed --class=Database\\Seeders\\PapeisSeeder
```

> **A dependência de ordem entre os passos 6, 7 e 8 é real**: o Shield descobre o Resource, não o
> model. Rodar o seeder antes do passo 8 gera zero permission de `Cupom`, sem erro nenhum. Na
> execução, **o passo 8 vem antes destes dois comandos** — o passo 6 está numerado aqui porque a
> policy é decisão de autorização, e a autorização se lê antes da tela.

- **Critério de aceite**: `Permission::where('name','like','%:Cupom')->count()` ≈ 12, e
  `/app/{tenant}/cupons` abre para `admin_organizacao`.
- **Logs**: nenhum.

### 7. Recorte de escrita do `panel_user` — RQ-07 × RQ-08

> Skills: `laravel-best-practices`, `ponytail`

**É o passo mais perigoso do plano** e o único que altera arquivo compartilhado.

- **Path**: `database/seeders/PapeisSeeder.php`

O mecanismo existente (`:87-93`) subtrai **entidades inteiras** por FQCN: `Paineis::permissoesDe('app',
[UserResource::class, ConviteResource::class])`. Ele não consegue expressar o que o card pede — RQ-07
tira a escrita, RQ-08 mantém a leitura. Acrescentar `CupomResource` à lista existente tiraria também
`ViewAny:Cupom` e quebraria RQ-08. Ver **ADR-08**.

- **Acrescentar um segundo recorte**, ao lado do primeiro e sem tocar nele:

```php
/**
 * Permissões de ESCRITA que o usuário comum do negócio não tem, em entidades que ele PODE ver.
 *
 * Diferente de `permissoesDeAdministracaoDoApp()`, que subtrai a entidade inteira: aqui a
 * entidade continua visível e só a escrita sai. É o que RQ-07 e RQ-08 de FERRO-812 pedem
 * juntas — "só admin cria, edita e exclui" + "os outros podem listar".
 *
 * Recorte por afixo sobre o FQCN, nunca por substring do nome: `str_contains($p, 'Cupom')`
 * pegaria um `CupomUsoResource` futuro por acidente, e numa subtração o erro é o espelhado —
 * tirar permissão de quem deveria tê-la.
 *
 * @return list<string>
 */
private function escritaVedadaAoUsuarioComum(): array
{
    // Allowlist de LEITURA, não denylist de escrita: afixo novo do Shield nasce negado.
    // Numa subtração, falhar fechado é a direção segura — o erro vira "faltou permissão a
    // quem devia ter" (visível, reclamado na hora) em vez de "sobrou permissão a quem não
    // devia" (invisível, e é o cenário caro que .ai/rules/filament.md descreve).
    $leitura = ['ViewAny', 'View'];

    return Paineis::permissoesDe('app', [CupomResource::class])
        ->reject(fn (string $p): bool => in_array(Str::before($p, ':'), $leitura, true))
        ->values()
        ->all();
}
```

- E no `run()`, aplicar junto do recorte que já existe:

```php
$administracao = $this->permissoesDeAdministracaoDoApp();
$escritaVedada = $this->escritaVedadaAoUsuarioComum();

$this->papel(config('filament-shield.panel_user.name', 'panel_user'), $guard, 'app')
    ->syncPermissions(
        $this->permissoesDoPainel('app', $guard)
            ->reject(fn (string $p): bool => in_array($p, $administracao, true)
                || in_array($p, $escritaVedada, true))
    );
```

- **`admin_organizacao` continua com a matriz inteira** do painel `app` (`:70-73`) — nada a mudar
  nele; é ele quem cumpre RQ-07 no modo multi-tenant.
- **`tests/Kit/PaineisTest.php` vai mudar de número** (o painel `app` sai de 38 permissions). A
  contagem **deve ser atualizada com o valor medido**, e o teste do recorte (CT-07) é o que garante
  que a atualização não escondeu um vazamento.
- **Logs**: nenhum — seeder.

### 8. `CupomResource` no painel `/app` — RQ-01 a RQ-06, RQ-08, RQ-14

> Skills: `laravel-best-practices`, `livewire-development`

- **Criar com**:
  `php artisan make:filament-resource Cupom --panel=app --generate --no-interaction`
- **Estrutura resultante** (molde de `Projetos/`, com form e table inline no Resource — o kit só separa
  em `Schemas/`/`Tables/` no painel `admin`):

```text
app/Filament/App/Resources/Cupons/
├── CupomResource.php
└── Pages/
    ├── ListCupons.php     (use HasResizableColumn, como ListProjetos)
    ├── CreateCupom.php
    └── EditCupom.php
```

- **Registro no painel**: **nenhum** — `AppPanelProvider.php:70` já faz
  `discoverResources(in: app_path('Filament/App/Resources'), …)`.
- **Propriedades estáticas** (molde de `ProjetoResource.php:41-49`):

```php
protected static ?string $model = Cupom::class;
protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedTicket;
protected static ?string $modelLabel = 'cupom';
protected static ?string $pluralModelLabel = 'cupons';
protected static ?string $recordTitleAttribute = 'codigo';
use BadgeContagemNavegacao;   // o concern que todo resource do kit usa
```

- **`$isScopedToTenant` NÃO é declarado**: o default `true` é o correto, porque `Cupom` tem a relação
  `tenant()` vinda de `BelongsToTenant`. Declarar `false` aqui seria copiar o `UserResource` do `/app`
  sem o motivo dele (`.ai/rules/filament.md` → "Resource de model sem relação de posse").

- **Import obrigatório do `Get`**: `use Filament\Schemas\Components\Utilities\Get;` — é o namespace que
  `ConviteForm.php:8` usa. **Não** é `Filament\Forms\Get`, que é o do Filament 3 e não existe aqui.
- **Formulário** — os cinco campos de RQ-02 a RQ-06:

```php
TextInput::make('codigo')
    ->label('Código')
    ->required()
    ->maxLength(40)
    // scopedUnique, NUNCA unique: a regra do Laravel não passa pelo Eloquent e ignoraria
    // o tenant, deixando o código de OUTRA organização bloquear o cadastro aqui (ADR-04).
    ->scopedUnique(ignoreRecord: true),

Select::make('tipo')
    ->label('Tipo')
    ->options(TipoDeDesconto::class)   // rótulos vêm do HasLabel do enum
    ->required()
    ->default(TipoDeDesconto::Porcentagem)
    // `->live()` é o que impede a tela de MENTIR a unidade do campo abaixo. Precedente no
    // kit: `ConviteForm.php:56` (Select que alimenta um campo dependente) e
    // `TenantForm.php:39` (`->live(onBlur: true)`).
    ->live(),

TextInput::make('valor')
    // O rótulo é o ÚNICO lugar que declara a unidade. A primeira versão tinha também um
    // `->suffix()`, cortado pelo /ponytail:ponytail-review: dizia a mesma coisa ao lado.
    ->label(fn (Get $get): string => $get('tipo') === TipoDeDesconto::Fixo->value
        ? 'Valor do desconto (centavos)'
        : 'Percentual de desconto')
    ->numeric()
    ->required()
    ->minValue(1)
    // Teto só faz sentido em porcentagem: 100% é o desconto total.
    ->maxValue(fn (Get $get): ?int => $get('tipo') === TipoDeDesconto::Porcentagem->value ? 100 : null),

DateTimePicker::make('expira_em')
    ->label('Válido até')
    ->required()
    ->seconds(false)
    ->minDate(now())
    ->helperText('Depois deste instante o cupom deixa de ser aceito.'),

TextInput::make('limite_de_usos')
    ->label('Limite de usos')
    ->numeric()
    ->required()
    ->minValue(1)
    ->helperText('Quantas vezes este cupom pode ser resgatado no total.'),
```

- **Tabela**:

```php
->defaultSort('expira_em', 'desc')
->columns([
    TextColumn::make('codigo')->label('Código')->searchable()->sortable(),
    TextColumn::make('tipo')->label('Tipo')->badge(),            // usa o HasLabel do enum
    TextColumn::make('valor')->label('Desconto')
        ->formatStateUsing(fn (Cupom $record): string => $record->tipo === TipoDeDesconto::Fixo
            ? 'R$ '.number_format($record->valor / 100, 2, ',', '.')
            : "{$record->valor}%"),
    TextColumn::make('usos')->label('Usos')
        ->formatStateUsing(fn (Cupom $record): string => "{$record->usos}/{$record->limite_de_usos}"),
    TextColumn::make('expira_em')->label('Válido até')->dateTime('d/m/Y H:i')->sortable(),
    TextColumn::make('situacao')->label('Situação')->badge()
        ->state(fn (Cupom $record): string => $record->situacao())
        ->color(fn (string $state): string => match ($state) {
            'Ativo' => 'success', 'Esgotado' => 'warning', default => 'danger',
        }),
])
```

- **RQ-08 — os demais usuários só veem os ativos**:

```php
/**
 * Quem não pode editar cupom só enxerga os ATIVOS (RQ-08 de FERRO-812).
 *
 * `Update:Cupom` é a permission que separa as duas personas, e não o nome do papel:
 * papel é configurável pelo cliente na tela de Funções; permission é o que a policy
 * consulta. Ver ADR-08.
 *
 * Isto é recorte de LISTAGEM, não barreira de segurança — a barreira de escrita é a
 * policy (`.ai/rules/filament.md` → "Asserção de identidade vive no model"). Cupom
 * expirado não é segredo; é ruído.
 */
public static function getEloquentQuery(): Builder
{
    $query = parent::getEloquentQuery();

    return Auth::user()?->can('Update:Cupom')
        ? $query
        : $query->ativos();
}
```

- **Nada de affordance sem permissão** (`wikis/convencoes.md` → Autorização): `CreateAction`,
  `EditAction` e `DeleteAction` consultam a policy sozinhos e somem para o `panel_user`. **Não**
  acrescentar `->visible()` manual — seria uma segunda regra que pode divergir da policy.
- **Logs**: nenhum no Resource. A tela é declarativa; o que se registra é a **aplicação** do cupom
  (passo 5) e as alterações de cadastro, que a auditoria de `/infra/audits` já pega via
  `AuditsFillables`.

### 9. `CupomFactory`

> Skills: `pest-testing`

- **Path**: `database/factories/CupomFactory.php` — molde de `TenantFactory` (`definition()` +
  states nomeados em pt-BR):

```php
public function definition(): array
{
    return [
        'codigo'         => mb_strtoupper(fake()->unique()->bothify('CUPOM###')),
        'tipo'           => TipoDeDesconto::Porcentagem,
        'valor'          => 10,
        'expira_em'      => now()->addDays(30),
        'limite_de_usos' => 100,
        // `usos` fica no default 0 da coluna; `tenant_id` é preenchido pela trait.
    ];
}

public function expirado(): static      // expira_em no passado
public function esgotado(): static      // usos === limite_de_usos
public function fixo(int $centavos = 1_000): static
```

- **`usos` está fora do `$fillable`**, então o state `esgotado()` precisa de
  `->afterCreating(fn (Cupom $c) => $c->forceFill(['usos' => $c->limite_de_usos])->save())` —
  `state(['usos' => …])` seria **descartado em silêncio**. É a armadilha mais provável deste passo.
- **Factory é só para teste** (`wikis/convencoes.md` → Banco e seeders): `fakerphp/faker` é
  `require-dev` e a imagem Docker roda `--no-dev`. **Nenhum seeder do kit pode usá-la.**
- **Logs**: nenhum.

### 10. Testes

> Skills: `pest-testing`

- Especificação completa em `04-casos-de-teste.md` e `05-casos-de-teste-browser.md`.
- **Distribuição pelas suítes** (a regra do kit é "teste em par", `.ai/rules/testes.md`):

| Arquivo | Suíte | O que cobre |
|---|---|---|
| `tests/Kit/CupomTest.php` | `Kit` (single-tenant) | regra de negócio pura: cálculo, validação, consumo atômico, trilha, logs |
| `tests/Tenancy/CupomTenancyTest.php` | `Tenancy` | isolamento entre organizações, unicidade por tenant, matriz de permissões |
| `tests/BrowserTenancy/CupomTest.php` | `Browser` (grupo) | CT-B — a pasta já existe e já está na testsuite `Browser` do `phpunit.xml:39` |

- **Ordem obrigatória**: **CT-05 (consumo atômico) antes de qualquer CT-B.** Se a barreira de
  concorrência não estiver de pé, todo cenário de tela mede a coisa errada.
- **Nenhuma infra de teste nova** — ao contrário da wiki `identidade-visual`, `tests/BrowserTenancy/`
  já existe (`tests/Pest.php:142-145`) e já está registrada no `phpunit.xml`. Verificado.
- **Logs**: nenhum.

### 11. Commits

Um por passo entregável — lista em `## Commits`, no fim deste arquivo. (A lista estava escrita duas
vezes; o `/ponytail:ponytail-review` cortou a duplicata.)

## Filosofia de Implementação

> **Ponytail ativo em modo `full`** durante toda a implementação. A escada, aplicada aqui:
>
> 1. **Reutilizar antes de criar**: o consumo atômico é o `UPDATE ... WHERE` de
>    `Convite::aceitarComoUsuarioExistente()`; o model é o molde de `Projeto`; a migration é o molde
>    de `projetos` + `convites`; a policy é **gerada** pelo Shield, não escrita.
> 2. **Feature nativa antes de código**: `->increment()` do Query Builder em vez de ler-somar-salvar;
>    `enum` do PHP em vez de constantes + validação; `scopedUnique()` do Filament em vez de rule
>    custom; `HasLabel` em vez de array de opções duplicado.
> 3. **Uma coluna, não uma tabela**: "ativo" é derivado de duas colunas que já existem (ADR-03).
> 4. **Mínimo que funciona**: nenhum Service, nenhum DTO, nenhum Repository, nenhum Observer, nenhum
>    Job. Dois models, um enum, um resource, dois recortes.
>
> **O que o Ponytail NÃO corta aqui, e por quê**: a tabela `cupom_usos` (RQ-15 é requisito explícito e
> a auditoria genérica não a alcança — ADR-07), a transação em `aplicarEm()` (contador sem trilha é
> pior que os dois ausentes) e o recorte de escrita do `panel_user` (ADR-08 — sem ele todo usuário
> comum emite desconto). Ponytail corta complexidade, não corta autorização nem trilha.
>
> Atalhos deliberados marcados com `ponytail:` comment. Depois de implementar,
> `/ponytail:ponytail-review` no diff.
>
> **Caveman ativo em modo `ultra`** na conversa agent ↔ usuário. Os arquivos desta wiki (00–06) são
> boundary do Caveman — prosa normal.

## Mapeamentos

**Unidade de `valor` por `tipo`** (a tabela que evita o erro mais provável desta feature):

| `tipo` | Unidade de `valor` | Exemplo gravado | Significado | Cálculo |
|---|---|---|---|---|
| `porcentagem` | pontos percentuais inteiros, 1–100 | `10` | 10% | `intdiv($total * 10, 100)` |
| `fixo` | **centavos** | `1000` | R$ 10,00 | `1000` |

**Situação derivada** (nenhuma coluna a mais):

| `usos` vs `limite_de_usos` | `expira_em` | `situacao()` | Aparece para `panel_user`? |
|---|---|---|---|
| `<` | futuro | `Ativo` | ✅ |
| `>=` | qualquer | `Esgotado` | ❌ |
| `<` | passado | `Expirado` | ❌ |

## Testes

> Ver `04-casos-de-teste.md` — backend: cálculo, validação, **consumo concorrente**, trilha de RQ-15,
> logs, isolamento entre organizações e a matriz de permissões.
> Ver `05-casos-de-teste-browser.md` — CT-B: o CRUD de RQ-01 na tela e o campo `valor` que muda de
> unidade com o `Select` de tipo.

## Verificação Final

- [ ] `/ponytail:ponytail-review` no diff
- [ ] `vendor/bin/pint --dirty`
- [ ] `composer types:check` (PHPStan/larastan)
- [ ] `vendor/bin/pest --parallel --group=kit` — os CT novos **e** `PaineisTest` verde com a contagem
      atualizada
- [ ] `vendor/bin/pest --testsuite=Browser` — **em série**, nunca com `--parallel`
      (`.ai/rules/testes-browser.md`)
- [ ] `php artisan db:seed --class=Database\\Seeders\\ShieldPermissionsSeeder` seguido de
      `…\\PapeisSeeder`, nesta ordem
- [ ] **Conferência manual da matriz**: `panel_user` **não** tem `Create:Cupom`; **tem** `ViewAny:Cupom`
- [ ] Roteiro *Desenhado × Implementado* do `05` preenchido
- [ ] `feature-quality-gate` invocado (step 8 da skill)

> **`--parallel --tia` não entra nesta lista**, ao contrário do que o template da skill sugere:
> `.ai/rules/testes-browser.md` registra que o ambiente não tem **PCOV** e que o `--tia` com Xdebug em
> série **não termina** (medido: abortado após 35 min). Os dois comandos acima são o equivalente
> local. Degradação documentada, não esquecimento.

## Commits

- `:sparkles: cupons: channel de log, migrations e enum de tipo`
- `:sparkles: cupons: model, regra de aplicacao e consumo atomico`
- `:sparkles: cupons: resource no painel de negocio`
- `:lock: cupons: recorte de escrita do usuario comum`
- `:white_check_mark: cupons: CT e CT-B`
- `:memo: wiki: cupons de desconto`
