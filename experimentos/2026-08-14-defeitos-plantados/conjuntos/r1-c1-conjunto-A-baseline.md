# Casos de Teste — FERRO-812: Cupons de desconto

## Setup Global

### Factories / Fixtures

- `Cupom::factory()->create()` — 10%, válido por 30 dias, limite 100. O caso comum.
- `Cupom::factory()->fixo(1_000)->create()` — R$ 10,00 em centavos.
- `Cupom::factory()->expirado()->create()` — `expira_em` no passado.
- `Cupom::factory()->esgotado()->create()` — `usos === limite_de_usos`.
  > **Atenção**: `usos` está **fora do `$fillable`** (passo 4 do PRD), então este state precisa de
  > `->afterCreating(fn (Cupom $c) => $c->forceFill(['usos' => $c->limite_de_usos])->save())`.
  > `state(['usos' => …])` seria **descartado em silêncio** e o state ficaria mentindo — o cupom
  > nasceria com `usos = 0` e os CTs que dependem dele passariam pelo motivo errado.
- `usuario()`, `usuarioDoKit($papel)`, `usuarioCom($papel)`, `usuarioComPapel($papel, $tenant)`,
  `papelNaOrganizacao()`, `tenant($nome, $slug)`, `noPainelDa($tenant)` — todos já existem em
  `tests/Pest.php` (`:170-338`). **Nenhum helper novo é criado**; helper cruzado entre arquivos é o
  defeito que `tests/Kit/HelpersDeTesteTest.php` guarda.
- Seeders: `ShieldPermissionsSeeder` + `PapeisSeeder`, o par que `tests/Kit/PaineisTest.php:20-22`
  já usa. Só nos CTs de autorização (CT-07, CT-08, CT-10) — os de regra de negócio não precisam.

### Estratégia de Mock

- `Log::spy()` nos CTs de log (CT-11), **ou** o helper de espionagem por channel. `tests/Pest.php:239`
  traz `espiarAutenticacao()`, que espia **só** o channel `autenticacao` e deixa os outros reais.
  **Não** generalizar aquele helper: um `espiarCupom()` novo, se for usado por mais de um arquivo,
  entra em `tests/Pest.php`; se for usado por um só, fica no arquivo (`.ai/rules/testes.md`).
- **Nenhum `Http::fake()`, `Queue::fake()` ou `Storage::fake()`**: a feature não chama serviço externo,
  não enfileira e não toca disco.
- **Nenhum mock do banco.** CT-05 mede concorrência real; mock de banco mediria o mock.

### Estratégia de DB

- **`RefreshDatabase`**, já aplicado globalmente em `tests/Pest.php` para `Kit`, `Tenancy`, `Browser` e
  `BrowserTenancy`. Não declarar de novo.
- **`DatabaseTransactions` é proibido em CT-05.** O caso mede o comportamento de um `UPDATE`
  condicional sob concorrência; envolver tudo numa transação aberta pelo teste mudaria a semântica que
  se quer medir.
- **Divisão por suíte** — a regra do kit é "teste em par" (`.ai/rules/testes.md`,
  `.ai/rules/filament.md`):

| Suíte | Arquivo | Por quê |
|---|---|---|
| `Kit` (single-tenant) | `tests/Kit/CupomTest.php` | regra de negócio pura: cálculo, validação, consumo, trilha, logs. Não precisa de tenant |
| `Tenancy` | `tests/Tenancy/CupomTenancyTest.php` | isolamento entre organizações, unicidade por tenant, matriz de permissões. `Tests\TenancyTestCase` fixa `permission.teams` em `createApplication()`, antes das migrations — ligar num `beforeEach` seria tarde (`tests/Pest.php:44-61`) |

### Cobertura esperada

Todo método público de `Cupom` tem ao menos um CT, e os que ramificam têm um por ramo:

| Método | CTs |
|---|---|
| `descontoSobre()` | CT-01 (porcentagem), CT-02 (fixo), CT-03 (truncamento e piso em zero) |
| `valido()` | CT-04 (achado), CT-04a/b/c (os três motivos de recusa) |
| `aplicarEm()` | CT-05 (concorrência), CT-06 (trilha), CT-03 (resultado) |
| `situacao()` | CT-09 |
| `scopeAtivos()` | CT-09, CT-12 |
| `CupomPolicy` (12 métodos) | CT-07, CT-08 — pela permission, não método a método |

---

## CT-01: Desconto percentual sobre o total

**Tipo**: `Unit`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('calcula o desconto percentual sobre o total')`
**Cobre**: RQ-03, RQ-04, RQ-12

### Precondições

- `Cupom::factory()->create(['tipo' => TipoDeDesconto::Porcentagem, 'valor' => 10])`

### Dados de Entrada

```php
$cupom->descontoSobre(10_000);   // R$ 100,00 em centavos
```

### Resultado Esperado

- Devolve `1_000` (R$ 10,00)
- **Não** consome uso: `$cupom->fresh()->usos === 0`. O método é puro de propósito — é o que permite
  mostrar o desconto na tela antes de o usuário confirmar, sem gastar o cupom

---

## CT-02: Desconto de valor fixo ignora o total

**Tipo**: `Unit`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('aplica o desconto fixo independente do total')`
**Cobre**: RQ-03, RQ-04, RQ-12

### Precondições

- `Cupom::factory()->fixo(1_500)->create()` — R$ 15,00

### Dados de Entrada

`descontoSobre(10_000)` e `descontoSobre(50_000)`.

### Resultado Esperado

- Os dois devolvem `1_500` — o valor fixo não escala com o total
- **É o CT que prova a tabela de `## Mapeamentos` do PRD.** Se alguém trocar os dois ramos do `match`
  de `descontoSobre()`, CT-01 e CT-02 ficam vermelhos juntos e a causa é óbvia; sem CT-02, um cupom
  fixo de `1_500` devolveria 15% e ninguém veria

---

## CT-03: Truncamento da fração e piso em zero

**Tipo**: `Unit`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('trunca a fracao do desconto e nunca devolve total negativo')`
**Cobre**: RQ-12 — e as premissas **P-06** e **P-07** do `00-requisito.md`

### Dados de Entrada

```php
// (a) truncamento: 10% de 9_999 = 999,9
$percentual->descontoSobre(9_999);

// (b) piso em zero: cupom fixo de R$ 50,00 sobre um total de R$ 30,00
$fixo50->aplicarEm(3_000, $usuario);
```

### Resultado Esperado

- (a) `999`, **não** `1_000` — `intdiv` trunca. Premissa P-06: nunca conceder mais desconto do que o
  cupom promete
- (b) `aplicarEm()` devolve **`0`**, nunca negativo. Premissa P-07: total negativo não é desconto, é
  crédito, e crédito é feature que ninguém pediu
- (b) o uso **é consumido mesmo assim** (`usos === 1`) e a trilha grava `valor_desconto = 5_000` —
  o cupom foi resgatado; o fato de o desconto exceder o total é do pedido, não do cupom

> **Este CT é o mais provável de virar discussão de negócio.** As duas decisões foram tomadas por falta
> de resposta e estão listadas como pergunta aberta em `00-requisito.md`. Se a resposta mudar, é este
> arquivo que muda primeiro — e o teste diz exatamente qual linha.

---

## CT-04: `valido()` acha o cupom ativo e recusa os três casos, sem distinguir o motivo para fora

**Tipo**: `Feature`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('valida existencia, validade e limite de usos')`
**Cobre**: RQ-09, RQ-10, RQ-11

### Precondições

Quatro cupons: um ativo (`BEMVINDO10`), um expirado, um esgotado, e nenhum para o código inexistente.

### Dados de Entrada

```php
Cupom::valido('BEMVINDO10');   // ativo
Cupom::valido('bemvindo10');   // mesmo cupom, caixa diferente
Cupom::valido('NAOEXISTE');
Cupom::valido($expirado->codigo);
Cupom::valido($esgotado->codigo);
Cupom::valido(null);
```

### Resultado Esperado

- Os **dois primeiros** devolvem o mesmo registro — `valido()` normaliza a caixa antes de consultar,
  como o mutator normaliza na gravação. Sem isso, um cliente que digita minúsculas recebe "cupom
  inválido" para um cupom que existe
- Os **quatro últimos** devolvem **`null`**
- **`null` é a mesma resposta para os quatro**, e é decisão, não preguiça: distinguir "não existe" de
  "expirado" de "esgotado" numa resposta ao cliente final é oráculo de enumeração de códigos. Quem
  opera vê a distinção no log (CT-11) e na coluna Situação da tela (CT-09)

---

## CT-05: O limite de usos não é furado por consumo concorrente

**Tipo**: `Feature`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('nao permite estourar o limite de usos')`
**Cobre**: RQ-11, RQ-13 — **e é o CT mais importante deste arquivo**

### Precondições

- `Cupom::factory()->create(['limite_de_usos' => 3])`
- **Sem `DatabaseTransactions`** — ver Estratégia de DB

### Dados de Entrada

Cinco chamadas sequenciais a `aplicarEm(10_000, $usuario)` sobre o **mesmo** cupom, sendo que as duas
últimas devem falhar:

```php
$aceitos = 0;
$recusados = 0;

for ($i = 0; $i < 5; $i++) {
    try { $cupom->aplicarEm(10_000, $usuario); $aceitos++; }
    catch (RuntimeException) { $recusados++; }
}
```

### Resultado Esperado

- `$aceitos === 3` e `$recusados === 2`
- `$cupom->fresh()->usos === 3` — **exatamente o limite, nunca 4 ou 5**
- `CupomUso::count() === 3` — a trilha acompanha o contador, sem linha órfã das tentativas recusadas
- A 4ª chamada lança `RuntimeException`, e o log traz `motivo` = `esgotado_ou_expirado`

### Por que este CT vale, mesmo sem paralelismo real

Ele **não** reproduz duas requisições simultâneas — a suíte é sequencial. O que ele prova é que a
condição de parada vive **no `WHERE` do `UPDATE`** e não num `if` em PHP: uma implementação
check-then-act **passa neste teste em execução sequencial**, e é por isso que o caso vem acompanhado
da verificação abaixo, que é o que realmente distingue as duas.

**Verificação obrigatória junto do CT** (fica no mesmo caso, não é cerimônia): depois das 5 chamadas,
afirmar que `usos` **nunca** excedeu `limite_de_usos`, e revisar no diff que
`aplicarEm()` usa `->increment()` do **Query Builder** com `whereColumn('usos', '<', 'limite_de_usos')`.
Se alguém trocar por `$cupom->increment('usos')` (o do model, que dispara eventos e não tem o `WHERE`),
**CT-05 continua verde e CT-06 fica vermelho** — porque a trilha e o contador se separam. Os dois CTs
juntos fecham o buraco que nenhum deles fecha sozinho.

> É a mesma limitação que `Convite::aceitarComoUsuarioExistente()` tem, e o projeto conviveu com ela:
> o valor do `UPDATE` condicional está no **desenho**, e o teste guarda o desenho, não a corrida.
> Registrado como limite conhecido em vez de fingir cobertura de concorrência.

---

## CT-06: A trilha registra quem aplicou, quando e quanto

**Tipo**: `Feature`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('registra quem aplicou o cupom e quanto foi de desconto')`
**Cobre**: **RQ-15**

### Precondições

- Um cupom de 10%, limite 5; `$ana = usuario('ana@example.com')`

### Dados de Entrada

```php
$cupom->aplicarEm(10_000, $ana);
```

### Resultado Esperado

- Existe **uma** linha em `cupom_usos` com `cupom_id` = o do cupom, `aplicado_por_id` = `$ana->id`,
  `valor_original` = `10_000`, `valor_desconto` = `1_000`
- `created_at` preenchido — é o "quando" de RQ-15
- `$cupom->fresh()->usos === 1` — contador e trilha andam juntos

### Por que este CT não é redundante com a auditoria do kit

`Cupom` implementa `Auditable` via `AuditsFillables`, e é tentador supor que `/infra/audits` já cobre
RQ-15. **Não cobre**, por dois motivos que este CT torna observáveis:

1. `usos` está fora do `$fillable`, e `getAuditInclude()` devolve o `$fillable`.
2. `->increment()` do Query Builder **não dispara eventos de model** — nenhum registro de auditoria é
   criado pelo consumo.

**Assertion complementar**, no mesmo caso: `Audit::where('auditable_type', Cupom::class)->count() === 0`
depois de `aplicarEm()`. É ela que documenta, em código executável, por que a tabela `cupom_usos`
existe (ADR-07). Sem esta linha, o próximo leitor tenta "simplificar" removendo a tabela.

---

## CT-07: O usuário comum lista, mas não cria, edita nem exclui cupom

**Tipo**: `Feature`
**Arquivo**: `tests/Tenancy/CupomTenancyTest.php`
**Método**: `it('mantem o usuario comum fora da escrita de cupons')`
**Cobre**: **RQ-07 e RQ-08** — e é o CT que protege o passo mais perigoso do PRD

### Precondições

- Seeders `ShieldPermissionsSeeder` **e** `PapeisSeeder`, nesta ordem
- Tenancy ligada (é o `TenancyTestCase`)
- `$comum = usuarioComPapel('panel_user', $acme)`
- `$admin = usuarioComPapel('admin_organizacao', $acme)`

### Resultado Esperado

**As duas metades no mesmo caso, e isso é deliberado:**

| Persona | `ViewAny:Cupom` | `View:Cupom` | `Create:Cupom` | `Update:Cupom` | `Delete:Cupom` |
|---|---|---|---|---|---|
| `panel_user` | ✅ **tem** | ✅ tem | ❌ **não tem** | ❌ não tem | ❌ não tem |
| `admin_organizacao` | ✅ | ✅ | ✅ | ✅ | ✅ |

> **Um CT que só afirmasse a ausência ficaria verde com a entidade inteira subtraída** — ou seja, com
> RQ-08 quebrado. É exatamente o erro que ADR-08 descreve, e é por isso que presença e ausência vivem
> no mesmo caso, com o mesmo nome. Espelha
> `it('mantem o usuario comum fora da administracao da organizacao')`, que já existe no kit.

**Segunda camada, obrigatória**: além da permission, afirmar pela **policy**, que é o que a tela
consulta — `$comum->can('create', Cupom::class)` é `false` e `$admin->can('create', Cupom::class)` é
`true`. Permission sem policy é matriz que ninguém lê.

---

## CT-08: Em single-tenant, quem cria cupom é o `master_global`

**Tipo**: `Feature`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('deixa a escrita de cupons com o master global sem tenancy')`
**Cobre**: RQ-07 (o recorte do modo single-tenant)

### Precondições

- `kit.tenancy.enabled` **desligada** (o default de `tests/Kit`)
- Seeders rodados
- `usuarioDoKit('master_global')` e `usuarioDoKit('panel_user', 'comum@example.com')`

### Resultado Esperado

- `master_global` → `can('create', Cupom::class)` é `true` (pelo `Gate::before`, sem permission no
  banco)
- `panel_user` → `can('create', …)` é `false`, e `can('viewAny', …)` é `true`

> A primeira versão deste CT tinha uma terceira assertion —
> `Role::where('name','admin_organizacao')->exists() === false`. O `/ponytail:ponytail-review` a
> cortou: ela testa o `PapeisSeeder` do kit (que só cria o papel sob `kit.tenancy.enabled`), não o
> cupom. O fato continua registrado em ADR-02, que é onde ele pertence.

> **Este CT fixa um comportamento que não foi pedido e que ninguém escolheu conscientemente** — ele é
> consequência da ADR-02 encontrando o kit como ele é. Fixá-lo em teste é a diferença entre "decidido"
> e "aconteceu". Se a resposta a A-02 mudar, é aqui que a mudança aparece.

---

## CT-09: A listagem do usuário comum mostra só os ativos, e a Situação bate com o filtro

**Tipo**: `Feature`
**Arquivo**: `tests/Tenancy/CupomTenancyTest.php`
**Método**: `it('lista apenas os cupons ativos para quem nao edita')`
**Cobre**: **RQ-08**

### Precondições

- Três cupons na organização: um ativo, um expirado, um esgotado
- `noPainelDa($acme)` — o helper de `tests/Pest.php:210` que faz o que o middleware do painel faria

### Dados de Entrada

`CupomResource::getEloquentQuery()->get()`, uma vez autenticado como `panel_user` e outra como
`admin_organizacao`.

### Resultado Esperado

- Como `panel_user`: **1** registro (o ativo)
- Como `admin_organizacao`: **3** registros — quem administra precisa ver o expirado para renová-lo e o
  esgotado para saber que acabou
- **Coerência entre as duas expressões da mesma regra** (ADR-03): para cada um dos três,
  `situacao() === 'Ativo'` se e somente se ele aparece na listagem do `panel_user`. É esta assertion
  que pega `scopeAtivos()` e `situacao()` divergindo — o risco nomeado em ADR-03

---

## CT-10: Duas organizações podem ter o mesmo código, e uma não enxerga o cupom da outra

**Tipo**: `Feature`
**Arquivo**: `tests/Tenancy/CupomTenancyTest.php`
**Método**: `it('isola os cupons por organizacao e permite o mesmo codigo nas duas')`
**Cobre**: **RQ-14** (premissa P-04) e o isolamento que ADR-02 exige

### Precondições

- `duasOrganizacoes()` — o helper de `tests/Pest.php:272`, que já devolve `acme`, `globex` e um usuário
  com papel nas duas

### Dados de Entrada

Criar `BLACKFRIDAY` na Acme e `BLACKFRIDAY` na Globex; depois, dentro do contexto da Acme, chamar
`Cupom::valido('BLACKFRIDAY')`.

### Resultado Esperado

- **As duas criações passam** — se a segunda falhar, alguém trocou `scopedUnique()` por `unique()`, ou
  o índice do banco não é composto. RQ-14 seria cumprido ao preço de vazar a existência do cupom
  alheio (ADR-04)
- `Cupom::valido('BLACKFRIDAY')` dentro da Acme devolve **o cupom da Acme**, e o `tenant_id` dele é o
  da Acme. É o CT que prova que o escopo global de `BelongsToTenant` está de pé — sem ele, uma
  organização gastaria o limite da outra
- Criar `BLACKFRIDAY` **duas vezes na mesma** organização **falha** — a unicidade não sumiu, só mudou
  de escopo

---

## CT-11: O log explica por que um código foi recusado

**Tipo**: `Feature`
**Arquivo**: `tests/Kit/CupomTest.php`
**Método**: `it('registra o motivo da recusa e o desconto aplicado')`
**Cobre**: rastreabilidade (não há RQ — é a convenção de log do projeto)

### Precondições

- Espionagem do channel `cupom`, no molde de `espiarAutenticacao()` (`tests/Pest.php:239`), que espia
  **só** o channel alvo e deixa os demais reais

### Resultado Esperado

- Recusa por código inexistente → `info` com mensagem começando em `[Cupom@valido]` e context com
  `motivo` ∈ `{codigo_vazio, nao_encontrado}`
- Aplicação bem-sucedida → `info` com `[Cupom@aplicarEm]` e context contendo `cupom_id`, `codigo`,
  `valor_original`, `valor_desconto`, `aplicado_por`, `usos_apos`
- Corrida perdida → **`warning`**, não `error`: é condição esperada de disputa, tratada e devolvida ao
  chamador. Mesma severidade de `Convite::exigirDono()` (`Convite.php:715`)
- **Assertion por prefixo e por chave**, no formato que o kit já usa
  (`tests/Tenancy/TenancyTest.php`):

```php
$canal->shouldHaveReceived('warning')
    ->withArgs(fn (string $mensagem, array $contexto): bool
        => str_starts_with($mensagem, '[Cupom@aplicarEm]')
        && $contexto['motivo'] === 'esgotado_ou_expirado')
    ->once();
```

- **Não asserir a mensagem inteira**: ela contém ids e valores, e o teste passaria a quebrar a cada
  mudança cosmética de texto

---

## CT-12: Regressão — a matriz de permissões e o recorte por organização continuam de pé

**Tipo**: `Feature`
**Arquivo**: **os que já existem** — nenhum arquivo novo
**Cobre**: `## Impacto em Features Existentes` do PRD

A natureza da wiki é **nova**, então não há regressão de ancestral. Mas o passo 7 altera
`PapeisSeeder`, que é infraestrutura compartilhada, e isso obriga:

| # | Suíte | O que protege | Expectativa |
|---|---|---|---|
| CT-12a | `tests/Kit/PaineisTest.php` | a matriz de permissões por painel | **vai mudar de número** — o painel `app` sai de 38 permissions. Atualizar a contagem com o valor **medido** faz parte do passo 7 |
| CT-12b | `tests/Kit/AdminDaOrganizacaoTest.php` + `tests/Tenancy/AdminDaOrganizacaoTest.php` | as barreiras da persona `admin_organizacao` | **verde sem alteração** |
| CT-12c | `tests/Tenancy/TenancyTest.php` | o recorte por organização | **verde sem alteração** — `Cupom` é a segunda model com `BelongsToTenant` |

> **CT-12a é o que mais provavelmente quebra, e quebrar é o comportamento certo.** O perigo não é o
> vermelho: é alguém afrouxar a asserção para "pelo menos N" em vez de atualizar o número. Uma matriz
> afirmada por desigualdade não afirma nada — foi o que permitiu, até a 0.11.0, duas permissions de
> Page ficarem inalcançáveis na subtração.

---

## Fronteira com os CT-B

| Pergunta | Arquivo | Por quê |
|---|---|---|
| O desconto calculado está certo? | este arquivo (CT-01 a CT-03) | aritmética pura, sem navegador |
| O limite de usos aguenta consumo repetido? | este arquivo (CT-05) | é `UPDATE` no banco, inspecionável sem tela |
| O `panel_user` **tem** ou **não tem** a permission? | este arquivo (CT-07) | é linha na tabela `model_has_roles` |
| O botão "Novo cupom" **aparece** para o usuário comum? | `05-*-browser.md` (CT-B02) | é render de Livewire consultando a policy — o HTTP devolve 200 nos dois casos |
| O campo `valor` muda de rótulo ao trocar o tipo? | `05-*-browser.md` (CT-B01) | depende do `->live()` fazer round-trip de Livewire; o HTML inicial é idêntico nos dois tipos |
| O cupom criado aparece na listagem? | `05-*-browser.md` (CT-B01) | atravessa duas telas |

> **Regra**: se um CT-B falha e nenhum CT deste arquivo falha, o defeito é de UI. Se ambos falham,
> corrigir o backend primeiro.

## Sem CT-B para

- **A aplicação do cupom** (RQ-09 a RQ-13, RQ-15): não há tela. Ver ADR-01 — a entrega é o motor, e o
  motor é coberto por CT unitário. **Um CT-B aqui seria falsa cobertura de uma superfície que não
  existe.**
- **A trilha de `cupom_usos`**: idem — não há tela que a exiba nesta entrega.

## Índice de Casos

| ID | Cenário | Tipo | Arquivo | RQ |
|----|---------|------|---------|-----|
| CT-01 | desconto percentual | Unit | `tests/Kit/CupomTest.php` | RQ-03, RQ-04, RQ-12 |
| CT-02 | desconto fixo ignora o total | Unit | `tests/Kit/CupomTest.php` | RQ-03, RQ-04, RQ-12 |
| CT-03 | trunca a fração e não fica negativo | Unit | `tests/Kit/CupomTest.php` | RQ-12 (P-06, P-07) |
| CT-04 | valida existência, validade e limite | Feature | `tests/Kit/CupomTest.php` | RQ-09, RQ-10, RQ-11 |
| CT-05 | **não estoura o limite de usos** | Feature | `tests/Kit/CupomTest.php` | RQ-11, RQ-13 |
| CT-06 | trilha de quem aplicou, quando e quanto | Feature | `tests/Kit/CupomTest.php` | **RQ-15** |
| CT-07 | **usuário comum lista mas não escreve** | Feature | `tests/Tenancy/CupomTenancyTest.php` | **RQ-07, RQ-08** |
| CT-08 | single-tenant: escrita com `master_global` | Feature | `tests/Kit/CupomTest.php` | RQ-07 |
| CT-09 | listagem só com ativos, coerente com a Situação | Feature | `tests/Tenancy/CupomTenancyTest.php` | RQ-08 |
| CT-10 | mesmo código em duas organizações; isolamento | Feature | `tests/Tenancy/CupomTenancyTest.php` | **RQ-14** |
| CT-11 | logs de recusa e de aplicação | Feature | `tests/Kit/CupomTest.php` | — |
| CT-12 | regressão da matriz e do recorte por organização | Feature | arquivos existentes | — |

**12 casos, 15 cláusulas, nenhuma sem CT** — exceto RQ-01 (o CRUD em si), que é coberto pelos CT-B do
`05-casos-de-teste-browser.md`, porque é a única cláusula cuja evidência é a tela.
