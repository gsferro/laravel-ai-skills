# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

## Setup Global

### Onde cada CT vive, e por quê

| Arquivo | TestCase | Suíte | O que vai ali |
|---|---|---|---|
| `tests/Feature/AprovacaoDeCompraTest.php` | `TestCase` (single-tenant) | `Feature` | o fluxo, as barreiras, a corrida, a notificação, os logs |
| `tests/FeatureTenancy/AprovacaoDeCompraTenancyTest.php` | `TenancyTestCase` | `FeatureTenancy` (**criada no passo 10**) | o que **só existe** com `permission.teams`: isolamento por organização e contexto do papel `diretor` |
| `tests/Kit/PaineisTest.php` | existente | `Kit` | a regressão da matriz de permissões |

> O kit nasce **single-tenant** (`kit.tenancy.enabled` default `false`, `config/kit.php:59`), e o
> fluxo de aprovação não depende de tenancy para estar correto. Por isso a maior parte dos CTs roda
> em `tests/Feature`, que é onde `wikis/convencoes.md` manda os testes do projeto viverem. Só o que
> **muda de comportamento** com tenancy sobe para a suíte com tenancy. Ver ADR-10.

### Factories / Fixtures

Três factories novas, no passo 11 do PRD. `wikis/convencoes.md` é explícito: **seeder nunca usa
factory nem faker** (`fakerphp/faker` é `require-dev`) — factory é só para teste.

- `CentroCusto::factory()->create(['nome' => 'TI', 'gestor_id' => $gestor->id])`
- `CentroCusto::factory()->create(['gestor_id' => null])` — o centro sem gestor de **CT-13** (A-10).
  **Sem state `semGestor()`**: um state com um consumidor é um nome novo para um atributo que já
  cabe na chamada
- `SolicitacaoCompra::factory()->create([...])` — nasce em `rascunho`
- States de situação: `->aguardandoGestor()`, `->aguardandoDiretor()`, `->aprovada()`
- `EtapaAprovacao` **sem factory**: quem a cria é sempre uma transição do model. Uma factory dela
  permitiria montar um histórico que o fluxo não produziria — e o CT passaria a testar a factory.

Helpers já existentes em `tests/Pest.php`, reaproveitados sem cópia (`.ai/rules/testes.md`):
`usuarioCom(?string $papel)`, `usuarioDoKit()`, `usuarioComPapel()`, `papelNaOrganizacao()`,
`noPainelDa()`, `tenant()`.

**Um helper novo**, e ele vai em `tests/Pest.php` porque **dois arquivos o usam** — é literalmente a
regra de `.ai/rules/testes.md`, enforçada por `tests/Kit/HelpersDeTesteTest.php`:

```php
/**
 * O elenco mínimo do fluxo: solicitante, gestor, diretor e um centro de custo.
 *
 * Em tests/Pest.php e não no arquivo de teste porque a suíte com tenancy usa o mesmo elenco
 * com um argumento a mais. Helper cruzado declarado num arquivo estoura
 * `Call to undefined function` em `--parallel`, em `--tia` e ao rodar um arquivo sozinho.
 *
 * @return array{solicitante: User, gestor: User, diretor: User, centro: CentroCusto}
 */
function elencoDeCompras(?Tenant $tenant = null): array
```

### Estratégia de Mock

- `Notification::fake()` — em todos os CTs de fluxo. Assertions por **`assertSentTo()` com o objeto
  da notificação**, nunca por `preg_match` no corpo renderizado: `tests/Kit/ConviteTest.php` já
  registra que a URL num e-mail sofre quebra de linha do quoted-printable e o teste falharia por
  formatação, não por comportamento.
- **`Log::spy()` NÃO é usado; e `Log::partialMock()` tampouco.** O desvio da wiki
  `identidade-visual-da-organizacao` registrou que `Log::partialMock()` (o desenho de
  `espiarAutenticacao()` em `tests/Pest.php:239-246`) **mascara o erro original** quando outro
  channel escreve no mesmo request. CT-15 usa `Monolog\Handler\TestHandler` empurrado no channel
  `compras` real — prova mais (o registro chega ao channel) e não mascara nada.
- Sem `Http::fake()` e sem `Queue::fake()`: a feature não chama serviço externo, e `phpunit.xml` já
  fixa `QUEUE_CONNECTION=sync`.

### Estratégia de DB

- **`RefreshDatabase`**, já aplicado globalmente em `tests/Pest.php` para `Feature`, e a aplicar no
  bloco novo de `FeatureTenancy` (passo 10). Isolamento total é obrigatório: os CTs mexem em
  permissions e papéis, que são estado global.
- `DatabaseTransactions` **não serve**: as migrations de `permission` dependem de
  `config('permission.teams')` em tempo de migração, e o `TenancyTestCase` fixa a flag antes disso.
- **Seeders no `beforeEach`**: `ShieldPermissionsSeeder` + `PapeisSeeder`, nesta ordem — o mesmo par
  de `tests/Kit/ConviteTest.php:36-38`.

> **Armadilha já catalogada**: `Tests\TestCase::seed()` usa `Artisan::call`, e **não** o `seed()` do
> Laravel, porque o `PendingCommand` faz `shield:generate` terminar com exit 0 e gravar **zero**
> permissions (`wikis/convencoes.md` → Armadilhas já resolvidas). Usar `$this->seed([...])` como os
> testes existentes fazem — não inventar outra forma.

---

## CT-01: O solicitante cria uma solicitação em rascunho

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('cria solicitacao de compra em rascunho')`
**Cobre**: RQ-01

### Precondições

- Elenco criado; `actingAs($solicitante)`; painel `app` corrente.

### Dados de Entrada

`Livewire::test(CreateSolicitacaoCompra::class)->fillForm([...])->call('create')`, com descrição,
valor `1500.00` e `centro_custo_id`.

### Resultado Esperado

- Registro persistido com `situacao = 'rascunho'`, `solicitante_id = $solicitante->id`,
  `valor = '1500.00'`, `centro_custo_id` correto.
- **`assertHasNoFormErrors()`** — sem ele, um erro de validação faria o `create` não gravar e o
  `assertDatabaseHas` seguinte falharia por um motivo que não é o dele.
- **É o CT que prova as três colunas fora do `$fillable`**: a tela **não** manda `situacao` nem
  `solicitante_id`, e o registro tem os dois corretos mesmo assim. Se alguém puser `situacao` no
  `$fillable` "para simplificar", nada aqui quebra — por isso CT-09 existe.

---

## CT-02: Editar e excluir valem em rascunho, e só em rascunho

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('permite editar e excluir apenas em rascunho')`
**Cobre**: RQ-02, RQ-03, RQ-10

### Precondições

- Uma solicitação em `rascunho` e outra em `aguardando_gestor`, do mesmo solicitante.

### Resultado Esperado

- Em `rascunho`: `SolicitacaoCompraPolicy::update()` e `::delete()` devolvem **`true`** para o
  solicitante.
- Em `aguardando_gestor`: **`false`** para o mesmo usuário.
- Em `rascunho`, mas para **outro** usuário: **`false`** — a terceira persona é o que separa "está no
  estado certo" de "é o dono", e sem ela a policy passaria checando só a situação.

> Aqui se testa a **affordance** (o Filament esconde os botões). A **barreira** é CT-11.

---

## CT-03: O envio leva a solicitação ao gestor e notifica só ele

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('envia a solicitacao para o gestor do centro de custo')`
**Cobre**: RQ-04, RQ-14

### Precondições

- `Notification::fake()`; solicitação em `rascunho` com valor **abaixo** do limite.

### Dados de Entrada

`$solicitacao->enviar($solicitante)`

### Resultado Esperado

- `situacao === SituacaoSolicitacao::AguardandoGestor`
- `Notification::assertSentTo($gestor, AprovacaoPendente::class)`, com `etapa === 'gestor'`
- **`Notification::assertNotSentTo($diretor, AprovacaoPendente::class)`** — a asserção negativa é o
  que prova RQ-14 ("**o próximo** aprovador", singular). Sem ela, notificar todo mundo passaria.
- **`Notification::assertNotSentTo($solicitante, …)`** — A-11: nada foi pedido para ele.
- Nenhuma etapa gravada: enviar não é uma decisão de aprovador.

---

## CT-04: A borda do limite de R$ 5.000 — os dois lados

**Tipo**: `Unit`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('decide a exigencia de diretor pelo limite')->with('valores_de_alcada')`
**Cobre**: RQ-05

### Dados de Entrada

```php
dataset('valores_de_alcada', [
    'bem abaixo'          => ['1000.00', false],
    'um centavo abaixo'   => ['4999.99', false],
    'exatamente o limite' => ['5000.00', false],   // ← "acima de" é ESTRITAMENTE maior (A-04)
    'um centavo acima'    => ['5000.01', true],
    'bem acima'           => ['99999.99', true],
]);
```

### Resultado Esperado

- `$solicitacao->exigeDiretor()` devolve o booleano esperado para cada linha.

> **É o CT mais barato e o mais fácil de perder do arquivo.** A linha *"exatamente o limite"* é a
> única leitura do requisito que ninguém confere depois de escrita, e trocar `>` por `>=` é uma
> tecla. Ela também é a que documenta A-04 em forma executável: se o usuário responder que R$ 5.000
> exatos **devem** passar pelo diretor, é esta linha que muda — e o resto do plano fica de pé.
>
> A dataset usa **string**, não float, porque é assim que o cast `decimal:2` devolve o valor
> (ADR-02) — testar com float testaria uma conversão que a aplicação não faz.

---

## CT-05: Acima do limite, o gestor aprova e a vez passa ao diretor

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('encaminha ao diretor quando o valor exige')`
**Cobre**: RQ-05, RQ-14

### Precondições

- `Notification::fake()`; solicitação em `aguardando_gestor` com valor `7500.00`.

### Dados de Entrada

`$solicitacao->aprovar($gestor)`

### Resultado Esperado

- `situacao === AguardandoDiretor` — **e não `Aprovada`**
- Uma etapa gravada: `etapa = 'gestor'`, `decisao = 'aprovada'`,
  `decidido_por_id = $gestor->id`, `justificativa = null`
- `Notification::assertSentTo($diretor, AprovacaoPendente::class)` com `etapa === 'diretor'`
- **`assertNotSentTo($gestor, …)`** — ele acabou de decidir; renotificá-lo seria ruído

---

## CT-06: Abaixo do limite, a aprovação do gestor é final

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('aprova em definitivo quando o valor nao exige diretor')`
**Cobre**: RQ-05

### Precondições

- `Notification::fake()`; solicitação em `aguardando_gestor` com valor `1500.00`.

### Resultado Esperado

- `situacao === Aprovada`
- **Uma** etapa (`gestor`), não duas
- **`Notification::assertNothingSent()`** — não há próximo aprovador, e A-11 diz que ninguém mais é
  notificado. É o CT que impede alguém "melhorar" a feature com um e-mail de conclusão que o card não
  pediu, e que o quality gate acusaria como escopo extra

---

## CT-07: A aprovação do diretor fecha o fluxo

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('conclui o fluxo com a aprovacao do diretor')`
**Cobre**: RQ-05

### Precondições

- Solicitação em `aguardando_diretor`, já com a etapa do gestor no histórico.

### Resultado Esperado

- `situacao === Aprovada`
- **Duas** etapas, na ordem `gestor` → `diretor`, ambas `aprovada` — a **ordem** é RQ-05 escrito
  ("depois do gestor") e é o que a leitura por `created_at` tem de devolver
- `Notification::assertNothingSent()`

---

## CT-08: Rejeição devolve ao rascunho, exige justificativa e preserva o histórico no reenvio

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('rejeita com justificativa e devolve ao rascunho preservando o historico')`
**Cobre**: RQ-06, RQ-07, RQ-08, RQ-09

### Precondições

- Solicitação em `aguardando_gestor`.

### Dados de Entrada

1. `$solicitacao->rejeitar($gestor, 'Faltou a cotação de três fornecedores.')`
2. `$solicitacao->enviar($solicitante)` — o reenvio de RQ-09
3. `$solicitacao->aprovar($gestor)`

### Resultado Esperado

- Após (1): `situacao === Rascunho` — **e não um estado `rejeitada`**, que não existe (ADR-01). Uma
  etapa com `decisao = 'rejeitada'` e a justificativa gravada.
- Após (2): `situacao === AguardandoGestor`, e o histórico **continua com a etapa de rejeição**.
- Após (3): **duas** etapas — a rejeição do primeiro ciclo **e** a aprovação do segundo.

> **É o CT que justifica ADR-03 inteira.** Com as sete colunas na solicitação, o passo (2) teria de
> zerar `rejeitado_por`/`justificativa` — e o assert de "duas etapas" após (3) seria impossível de
> escrever. Se alguém "simplificar" o histórico para colunas, **este é o único teste que fica
> vermelho**, e a mensagem de falha precisa dizer isso.

---

## CT-09: `aprovada` é terminal

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('nao aceita acao nenhuma depois de aprovada')`
**Cobre**: RQ-10

### Precondições

- Solicitação em `aprovada`.

### Resultado Esperado

Cada uma destas chamadas lança `RuntimeException`, e **nenhuma** altera a situação:

| Chamada | Por quem |
|---|---|
| `enviar()` | solicitante |
| `aprovar()` | gestor |
| `rejeitar()` | gestor |
| `cancelar()` | solicitante — **RQ-11 diz "antes da aprovação final"** |

- E a policy: `update()` e `delete()` devolvem `false` para o solicitante.
- `$solicitacao->fresh()->situacao === Aprovada` ao final — o estado sobreviveu a quatro tentativas.

---

## CT-10: O cancelamento é do solicitante, e só em trânsito

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('cancela em transito, e so pelo solicitante')`
**Cobre**: RQ-11

### Resultado Esperado

| Situação | Quem chama | Resultado |
|---|---|---|
| `aguardando_gestor` | solicitante | ✅ vira `cancelada` |
| `aguardando_diretor` | solicitante | ✅ vira `cancelada` |
| `aguardando_gestor` | gestor | ❌ `RuntimeException` — cancelar é do solicitante |
| `rascunho` | solicitante | ❌ `RuntimeException` — em rascunho o verbo é **excluir** (A-06) |

- Nenhuma etapa gravada no cancelamento: cancelar não é decisão de aprovador.

> A última linha é a **premissa A-06 em forma executável**. Se o usuário responder que o rascunho
> também cancela, é esta linha que muda — e nada mais no plano.

---

## CT-11: As barreiras chamadas **direto**, com a pessoa errada

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('recusa transicao chamada por quem nao e a pessoa da vez')`
**Cobre**: RQ-02, RQ-06, RQ-07, RQ-11 — e a regra de `.ai/rules/filament.md`

### Precondições

- Elenco completo, mais um `$estranho` sem relação nenhuma com a solicitação.

### Dados de Entrada

**Chamada direta ao método do model** — sem passar por Livewire, sem passar por policy:

| Chamada | Esperado |
|---|---|
| `$emAguardandoGestor->aprovar($diretor)` | `RuntimeException` — não é a vez dele |
| `$emAguardandoGestor->aprovar($solicitante)` | `RuntimeException` |
| `$emAguardandoDiretor->aprovar($gestor)` | `RuntimeException` — ele já decidiu |
| `$emAguardandoGestor->rejeitar($estranho, 'qualquer')` | `RuntimeException` |
| `$emAguardandoGestor->rejeitar($gestor, '')` | `RuntimeException` — **justificativa vazia** (RQ-07) |
| `$emAguardandoGestor->rejeitar($gestor, '   ')` | `RuntimeException` — `blank()`, não `empty()` |
| `$rascunho->enviar($estranho)` | `RuntimeException` |
| `$emTransito->cancelar($estranho)` | `RuntimeException` |

### Resultado Esperado

- Todas lançam; **nenhuma situação muda**; **nenhuma etapa é gravada**.
- Um `warning` no channel `compras` por recusa, com `motivo` preenchido.

> **É o CT que a regra do projeto exige, e o único que exercita o caminho que a tela nunca toma.**
> `.ai/rules/filament.md`: *"Barreira sem teste direto não é barreira — o caso que passa pela tela
> continuaria verde com a asserção removida."* As duas últimas linhas de justificativa vazia são
> aqui, e não no `->required()` do Textarea, porque **o formulário protege a tela e o model protege o
> dado** — o primeiro job ou comando que chamar `rejeitar()` não passa por formulário nenhum.

---

## CT-12: Duas aprovações simultâneas — só uma vence

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('resolve a corrida entre dois aprovadores da mesma etapa')`
**Cobre**: integridade — ADR-09

### Precondições

- Solicitação em `aguardando_diretor`; **dois** usuários com papel `diretor`.
- **Duas instâncias do mesmo registro, carregadas antes de qualquer transição** — é isso que simula
  duas requisições concorrentes num teste síncrono:

```php
$a = SolicitacaoCompra::find($id);
$b = SolicitacaoCompra::find($id);   // ambas leem 'aguardando_diretor'

$a->aprovar($diretor1);              // vence
expect(fn () => $b->aprovar($diretor2))->toThrow(RuntimeException::class);
```

### Resultado Esperado

- A primeira chamada transiciona para `Aprovada` e grava **uma** etapa.
- A segunda **lança** e grava **zero** etapas — `EtapaAprovacao::count() === 2` no total
  (a do gestor + a do diretor vencedor), nunca 3.
- `warning` no log com `motivo: 'situacao_mudou'`, `esperada` e `encontrada` no context.

> **Este CT fica verde com `get()` + `save()` se o assert de contagem de etapas não existir** — as
> duas gravariam, e a situação final ainda seria `Aprovada`. É a contagem que acusa, não a situação.
> Sem `lockForUpdate` de propósito: SQLite (`phpunit.xml`) não o suporta, e ADR-09 explica por que o
> `UPDATE` condicional é a solução, não o contorno.

---

## CT-13: Envio recusado quando o centro de custo está sem gestor

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('recusa o envio quando o centro de custo nao tem gestor')`
**Cobre**: RQ-04 — A-10

### Precondições

- `CentroCusto::factory()->create(['gestor_id' => null])`; solicitação em `rascunho` nele.
- `Notification::fake()`.

### Resultado Esperado

- `enviar()` lança `RuntimeException`.
- **`situacao` continua `Rascunho`** — a solicitação não fica presa em `aguardando_gestor` sem
  ninguém para aprová-la, e não é aprovada por falta de aprovador. **As duas alternativas erradas
  precisam estar assertadas**, não só a exceção.
- `Notification::assertNothingSent()`.
- `warning` no log com `motivo: 'centro_sem_gestor'` e `centro_custo_id` no context.

---

## CT-14: `panel_user` solicita, mas não administra centro de custo

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('mantem o centro de custo fora da matriz do usuario comum')`
**Cobre**: autorização — A-08, ADR-06

### Precondições

- Os dois seeders rodados (`ShieldPermissionsSeeder` → `PapeisSeeder`).
- `$comum = usuarioDoKit('panel_user')`.

### Resultado Esperado

| Permission | `panel_user` |
|---|---|
| `Create:SolicitacaoCompra` | ✅ **tem** |
| `Update:SolicitacaoCompra` | ✅ **tem** |
| `ViewAny:CentroCusto` | ❌ **não tem** |
| `Update:CentroCusto` | ❌ **não tem** |
| `Create:CentroCusto` | ❌ **não tem** |

- E o outro lado: `admin_organizacao` **tem** as de `CentroCusto` (ele recebe a matriz inteira do
  painel `app`).

> **Os dois lados são obrigatórios.** Um CT que só assere a ausência passaria também com a matriz
> inteira vazia — que é o cenário em que os seeders não rodaram, e nada estaria funcionando. É a
> mesma forma de `it('mantem o usuario comum fora da administracao da organizacao')`, citada em
> `.ai/rules/filament.md`.
>
> **Este é o CT de segurança da entrega.** Se ele ficar vermelho, o defeito é a linha ausente em
> `PapeisSeeder::permissoesDeAdministracaoDoApp()` — e enquanto ele estiver vermelho, qualquer
> usuário comum pode se nomear gestor e aprovar as próprias compras (A-08).

---

## CT-15: Os logs saem no channel `compras`, no formato do projeto

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/AprovacaoDeCompraTest.php`
**Método**: `it('registra as transicoes no channel de compras')`
**Cobre**: rastreabilidade

### Precondições

- `Monolog\Handler\TestHandler` empurrado no logger **real** do channel `compras`:

```php
$handler = new TestHandler;
Log::channel('compras')->pushHandler($handler);
```

> **Não usar `Log::spy()` nem `Log::partialMock()`.** O desvio registrado pela wiki
> `identidade-visual-da-organizacao` (`03-progresso.md` → Desvios do Plano) mediu o custo: com outro
> channel escrevendo no mesmo request, o `partialMock` cai no método real de um `LogManager`
> construído sem construtor e morre em *"Trying to access array offset on null"* — **mascarando o
> erro original**. O `TestHandler` prova mais (o registro chega ao channel de verdade) e não mascara
> nada.

### Dados de Entrada

Um ciclo completo: `enviar()` → `rejeitar()` → `enviar()` → `aprovar()`.

### Resultado Esperado

- Um registro por transição, todos com prefixo `[SolicitacaoCompra@{metodo}]`.
- Níveis conforme a tabela do PRD: `enviar`/`aprovar` → `info`; `rejeitar`/`cancelar` → `warning`.
- Context com `solicitacao_id`, `de`, `para` e — no envio — `exige_diretor`.
- **`justificativa` NÃO aparece no context de `rejeitar`**, só `justificativa_tamanho`. A asserção é
  negativa e é a razão do CT existir: `config/logging.php:80-81` declara a regra LGPD do bloco de
  channels, e a justificativa é texto livre escrito por uma pessoa **sobre outra**.
- **Nenhum registro de nível `error`** em todo o ciclo — recusa de regra de negócio é `warning` pela
  tabela de severidade de `wikis/convencoes.md`.

---

## CT-16: Uma organização não enxerga a solicitação da outra

**Tipo**: `Feature`
**Arquivo**: `tests/FeatureTenancy/AprovacaoDeCompraTenancyTest.php`
**Método**: `it('isola solicitacoes e centros de custo por organizacao')`
**Cobre**: `wikis/convencoes.md` → "Model de negócio pertence a um tenant"

### Precondições

- Duas organizações (`acme`, `globex`), cada uma com centro de custo e solicitação próprios.
- `noPainelDa($acme)` — o helper de `tests/Pest.php:210-215`, que faz o que o middleware do painel
  faria num request real.

### Resultado Esperado

- Com a Acme corrente: `SolicitacaoCompra::count() === 1` e `CentroCusto::count() === 1`, e são os
  dela.
- Trocando para a Globex: os da Globex.
- `tenant_id` preenchido sozinho no `create()`, **sem** estar no `$fillable`.

> **Não** se assere aqui o "sem tenant, a query volta a ser global". É comportamento **da trait**
> `BelongsToTenant`, declarado no docblock dela (`app/Traits/BelongsToTenant.php:47-53`) e já coberto
> pela suíte de tenancy do kit. Um CT de negócio que o repete testa o kit, não a feature — e ficaria
> vermelho por uma mudança que não é desta wiki.

---

## CT-17: O papel `diretor` é resolvido no contexto da organização

**Tipo**: `Feature`
**Arquivo**: `tests/FeatureTenancy/AprovacaoDeCompraTenancyTest.php`
**Método**: `it('notifica apenas os diretores da organizacao da solicitacao')`
**Cobre**: RQ-14 — ADR-08

### Precondições

- `Notification::fake()`.
- Duas organizações. `$diretorAcme` com papel `diretor` **na Acme**, `$diretorGlobex` **na Globex** —
  atribuídos com `papelNaOrganizacao()` (`tests/Pest.php:323-338`), que é o helper que existe
  **exatamente** porque papel gravado em `Tenant::CONTEXTO_GLOBAL` fica invisível dentro do `/app`.
- Solicitação da **Acme**, acima do limite, em `aguardando_gestor`.

### Dados de Entrada

`$solicitacao->aprovar($gestorDaAcme)`

### Resultado Esperado

- `Notification::assertSentTo($diretorAcme, AprovacaoPendente::class)`
- **`Notification::assertNotSentTo($diretorGlobex, …)`** — a asserção negativa **é** o CT
- E o caso vazio: sem nenhum diretor na organização, a transição **acontece do mesmo jeito** (para
  `aguardando_diretor`) e um `warning` com `motivo: 'sem_aprovadores'` é registrado. ADR-08: o e-mail
  que não sai não pode desfazer a transição que já ocorreu, e ninguém deve descobrir isso só quando
  reclamarem.

> **Este CT só existe com tenancy** — sem `permission.teams` não há `model_has_roles.team_id` e a
> pergunta não faz sentido. É metade da justificativa de ADR-10.

---

## CT-18: Regressão — a matriz de permissões por painel

**Tipo**: `Feature`
**Arquivo**: **`tests/Kit/PaineisTest.php`** — arquivo existente, ajuste de contagem
**Cobre**: `## Impacto em Features Existentes` do PRD

Dois Resources novos no painel `app` mudam a matriz que `PaineisTest` afirma. Não é CT novo: é o CT
existente, que **vai ficar vermelho** e precisa do número ajustado depois de rodar os dois seeders.

**Rodar este primeiro**, antes de escrever qualquer CT novo — escrever teste sobre suíte quebrada não
mede nada.

> `wikis/convencoes.md` registra a contagem histórica (`admin 91, app 38, infra 96 — 199`). O painel
> `app` cresce com as permissions de `SolicitacaoCompra` e `CentroCusto`; a subtração do `panel_user`
> cresce só com as de `CentroCusto` (ADR-06). **Confirmar o número medindo, nunca calculando** — o
> Shield gera as chaves a partir de `config('filament-shield')`, e supor a quantidade por Resource é
> como o número anterior envelheceu.

---

## Fronteira com os CT-B

| Pergunta | Arquivo | Por quê |
|---|---|---|
| A transição está correta? | este arquivo (CT-03, 05, 06, 07, 08) | é estado de PHP e de banco |
| A regra de alçada está certa na borda? | este arquivo (CT-04) | aritmética pura, sem navegador |
| A barreira recusa quem não é da vez? | este arquivo (CT-11) | **só** por chamada direta ao model |
| A corrida é resolvida? | este arquivo (CT-12) | duas instâncias, um processo |
| O gestor **encontra** o botão Aprovar? | `05-*-browser.md` (CT-B01) | é affordance, e afforda ou não no DOM |
| O solicitante **não** vê o botão Aprovar? | `05-*-browser.md` (CT-B03) | idem, e é a regra de affordance do projeto |
| A modal exige a justificativa **na tela**? | `05-*-browser.md` (CT-B02) | validação de formulário Livewire, com JS |
| O histórico aparece com quem decidiu? | `05-*-browser.md` (CT-B01) | RQ-13 é literalmente "mostrar na tela" |

## Índice de Casos

| ID | Cenário | Tipo | Arquivo | RQ |
|----|---------|------|---------|-----|
| CT-01 | cria em rascunho, com `situacao`/`solicitante` fora do form | Feature | `tests/Feature/AprovacaoDeCompraTest.php` | RQ-01 |
| CT-02 | editar/excluir só em rascunho e só pelo dono (affordance) | Feature | idem | RQ-02, RQ-03, RQ-10 |
| CT-03 | envio → gestor, e **só** o gestor notificado | Feature | idem | RQ-04, RQ-14 |
| CT-04 | **borda do limite**, dataset dos dois lados | Unit | idem | RQ-05 |
| CT-05 | acima do limite → diretor, notificado | Feature | idem | RQ-05, RQ-14 |
| CT-06 | abaixo do limite → aprovada, **ninguém notificado** | Feature | idem | RQ-05 |
| CT-07 | diretor conclui; duas etapas **na ordem** | Feature | idem | RQ-05 |
| CT-08 | rejeição → rascunho, e **histórico sobrevive ao reenvio** | Feature | idem | RQ-06, RQ-07, RQ-08, RQ-09 |
| CT-09 | `aprovada` é terminal para as quatro ações | Feature | idem | RQ-10 |
| CT-10 | cancelar em trânsito, só pelo solicitante | Feature | idem | RQ-11 |
| CT-11 | **barreiras chamadas direto**, com a pessoa errada | Feature | idem | RQ-02, RQ-06, RQ-07, RQ-11 |
| CT-12 | **corrida** entre dois aprovadores | Feature | idem | — |
| CT-13 | envio recusado sem gestor no centro (falha fechado) | Feature | idem | RQ-04 |
| CT-14 | **`panel_user` fora de `CentroCusto`**, e dentro de `SolicitacaoCompra` | Feature | idem | — |
| CT-15 | logs no channel `compras`, **sem a justificativa em claro** | Feature | idem | — |
| CT-16 | isolamento por organização | Feature | `tests/FeatureTenancy/AprovacaoDeCompraTenancyTest.php` | — |
| CT-17 | diretores **da organização certa** | Feature | idem | RQ-14 |
| CT-18 | regressão da matriz de permissões | Feature | `tests/Kit/PaineisTest.php` | — |
