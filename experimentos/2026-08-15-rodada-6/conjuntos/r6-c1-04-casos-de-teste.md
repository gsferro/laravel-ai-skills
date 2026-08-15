# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> ela ainda não existe. O `01-plano-acao.md` entrou apenas para paths, rotas, nomes de método e a
> tabela `## Superfície de UI`; o que ele determina e o requisito não, está listado em
> [`## Fronteira com o Plano`](#fronteira-com-o-plano) e **não** virou `Então`.
>
> **Versão 2** — depois da [revisão adversarial](#revisão-adversarial), que produziu 18 lacunas e 6
> achados de matriz. Os CT-01 a CT-46 mantêm a numeração da versão 1 de propósito: renumerar por
> motivo cosmético destruiria a rastreabilidade. Os cenários novos são **CT-47 a CT-57**.

---

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Justificativa da nota |
|---|---|---|---|---|---|
| **A1 — Cálculo do desconto** | 3 | 3 | **9** | completo | domínio condicionado pelo `tipo`, arredondamento e limite inferior; dinheiro |
| **A2 — Aplicação e consumo do uso** | 3 | 3 | **9** | completo | concorrência sobre contador; dinheiro; irreversível (uso consumido não volta) |
| **A3 — Autorização** | 3 | 3 | **9** | completo | 6 personas × 6 verbos; altera `PapeisSeeder`, infra compartilhada; autorização |
| **A4 — Unicidade do código** | 3 | 3 | **9** | completo | três pontos de entrada, normalização, escopo por organização; código duplicado torna o desconto ambíguo |
| **A5 — Cadastro (criar/editar pela tela)** | 2 | 3 | 6 | padrão | integra com Filament/Shield; grava o dado que vira dinheiro (validade, valor, limites) |
| **A6 — Trilha de quem aplicou** | 3 | 3 | **9** | completo | **elevado na v2**: a revisão adversarial mostrou que a trilha tem ciclo de vida próprio (sobreviver à exclusão do cupom) e que o conjunto v1 não o cobria. Auditoria/compliance |
| **A7 — Listagem** | 2 | 2 | 4 | padrão | estado derivado de duas colunas; impacto é ruído operacional, não dinheiro |

**Perfil da feature: `completo`** (cinco áreas em 9) → **revisão adversarial obrigatória**, executada
e registrada em [`## Revisão Adversarial`](#revisão-adversarial).

- **Técnicas aplicadas**: EP · BVA 3-valores (`datetime` com incremento de 1 s; contadores com
  incremento de 1) · tabela de decisão (domínio condicionado `tipo` × `valor`) · matriz
  estado × operação (produto cartesiano fechado) · matriz papel × ação (produto cartesiano fechado) ·
  rastreio de efeito · **ciclo de vida da entidade de efeito colateral** · normalização de identidade
  (colisão **e** forma persistida) · concorrência check-then-act · registro-testemunha.
- **Contagem, conferida célula a célula**: **15 regras** · **57 cenários** no `04` · **1 CT-B** no
  `05` · **97 mutantes previstos** · **1 sem matador** (M-R14.9, declarado com o motivo) ·
  **5 lacunas declaradas** (L-02, L-03, L-04, L-05, L-07).

> **Como estes números foram obtidos**: contados nas próprias tabelas, não estimados —
> `grep -cE "^\| M-R[0-9]+\.[0-9]+ \|"` para os mutantes, `grep -o "\[CT-…\]"` para os cenários, e
> conferência de que **todo** `CT-nn` citado em matriz, checklist ou tabela de mutantes tem um
> `Cenário:`/`Esquema do Cenário:` correspondente. A primeira redação da v2 declarava
> "93 mutantes · 2 sem matador" e a contagem real era **97 · 1** — os dois mutantes que ela listava
> como órfãos (M-R8.6 e M-R14.7) haviam ganhado matador no próprio fechamento da revisão. Contagem
> declarada que não bate com as células é o defeito que a revisão adversarial apontou em
> [M-4](#achados-da-revisão), e ele reapareceu; fica registrado em vez de corrigido em silêncio.

### Técnica escalada acima do perfil da área

- **R11 (cálculo)** já é `completo`, mas o BVA foi levado a valores **discriminantes de
  representação** (29 % sobre 10 000 centavos) e não só de fronteira — é o único jeito de separar
  `float` de inteiro.
- **R8 (listagem, área `padrão`)** recebeu partição **exaustiva** das quatro situações derivadas
  **e** BVA de fronteira (`expira_em` no dia corrente, `usos = limite − 1`). O motivo está em
  [B-04](#achados-da-revisão): listagem e aplicação são **dois leitores diferentes da mesma regra
  derivada**, e a fronteira precisa ser exercitada em cada um. Partição exaustiva de *combinação*
  não substitui fronteira de *valor*.
- **R4 (edição, área `padrão`)** recebeu replicação de EP/BVA de valor e de limite, além do teto
  de 3 cenários da área. Motivo: [I-4 e B-07](#achados-da-revisão) — a regra declarava a técnica e
  não a executava, e a implementação que valida só na criação é o defeito mais barato de cometer.

---

## Arnês Confirmado no Código (não presumido)

Tudo abaixo foi lido neste projeto, hoje. A alocação de camada do passo 7 depende disto.

| Fato | Onde foi confirmado | Consequência para os CT |
|---|---|---|
| Pest **5.1.1**; `pest-plugin-browser` **5.0.1**; `pest-plugin-laravel` **5.0.1** | `composer.json:78-80`, `composer.lock` | matchers e API de Pest 5 valem |
| **`pestphp/pest-plugin-mutate` (5.0.2) está em `vendor/` mas NÃO está no `composer.json`** | `composer.json:68-82` × `composer.lock` | `pest --mutate` funciona **por acidente da árvore de dependências**, e some num `composer update`. Declarar `composer require pestphp/pest-plugin-mutate --dev` antes do fechamento do ciclo |
| **`pest-plugin-agent` não está instalado** | `vendor/pestphp/` | `vendor/bin/pest --agent='…'`, que a `feature-wiki` sugere como sondagem, **não existe aqui**. Sondagem é `pest --filter` num teste descartável |
| Filament **5.7.6**, Livewire **4.4.0**, Laravel **13.25.0**, PHP `^8.3` | `composer.lock`, `composer.json:20,31,44` | helpers de Filament 5 (abaixo) |
| Suítes: `Unit`, `Feature`, `Tenancy`, `Kit`, `Browser` (= `tests/Browser` + `tests/BrowserTenancy`) | `phpunit.xml:8-40` | — |
| `tests/Kit` → `Tests\TestCase` + `RefreshDatabase` + grupo `kit` | `tests/Pest.php:43-46` | single-tenant (`KIT_TENANCY=false`) |
| `tests/Tenancy` → `Tests\TenancyTestCase` + `RefreshDatabase` + grupo `kit` | `tests/Pest.php:67-70` | multi-tenant; `permission.teams` fixado **antes** das migrations (`tests/TestCase.php::createApplication`) |
| `tests/Browser` → `Tests\TestCase`, grupo `browser`; `tests/BrowserTenancy` → `Tests\TenancyTestCase`, grupo `browser` | `tests/Pest.php:101-104,142-145` | fora do `composer test:kit` |
| **`tests/Unit` NÃO tem `pest()->extend(TestCase::class)->in('Unit')`** | `tests/Pest.php` inteiro — só `Feature`, `Kit`, `Tenancy`, `Browser`, `BrowserTenancy` | **não existe camada `Unit` utilizável nesta feature.** Um caso em `tests/Unit` roda sob `PHPUnit\Framework\TestCase`, sem container: `config()`, `now()`, `DB` e o boot de `BelongsToTenant` não resolvem. A escada real começa em `tests/Kit` |
| `pest()->browser()->timeout(20_000)` | `tests/Pest.php:170` | teto, não espera |
| `pest()->tia()->defaultBranch('main')->locally()` | `tests/Pest.php:126` | TIA ligado localmente, desligado em CI |
| DB de teste: `sqlite` `:memory:`; `QUEUE_CONNECTION=sync`; `MAIL_MAILER=array` | `phpunit.xml:53-57` | ver as duas linhas seguintes |
| **`foreign_key_constraints` é `true` por default e `DB_FOREIGN_KEYS` não é sobrescrito no `phpunit.xml`** | `config/database.php:40`, `phpunit.xml:47-62` | **as chaves estrangeiras são aplicadas no SQLite de teste** — CT-38 pode forçar a falha da trilha por FK, sem pragma à mão. O arnês foi confirmado **antes** de a lacuna ser considerada |
| **`config/app.php:68` fixa `'timezone' => 'UTC'` — não lê `env()`. E `.env:10` declara `APP_TIMEZONE=America/Sao_Paulo`** | `config/app.php:68`, `.env:10`, `.env.example:10` | divergência real entre o que o operador configura e o fuso em que o app compara datas → **CT-29 existe por causa disto**. Não existe `.env.testing`, então o teste roda em UTC |
| **`BelongsToTenant`: "sem tenant, sem escopo"** — fora de um request de painel (job, comando, seeder, tinker) `Filament::getTenant()` é nulo e a query **volta a ser global** | `app/Traits/BelongsToTenant.php:48-52` (docblock) e `:63-71` (o `addGlobalScope`) | **o ponto de integração do PRD é exatamente esse chamador.** → **CT-56** |
| `master_global` recebe `syncPermissions([])` — **zero permissions**; ele atravessa pelo `Gate::before` | `database/seeders/PapeisSeeder.php:53-54` | CT-16 linha 1 e CT-20 dependem disso |
| `admin_organizacao` **só é semeado com `config('kit.tenancy.enabled')`**, e o default é **desligado** | `PapeisSeeder.php:70`, `config/kit.php:59`, `.env:76` | CT-20 e as linhas `admin_organizacao` só existem em `tests/Tenancy` |
| **`tests/Kit/PaineisTest.php` NÃO afirma contagem numérica de permissões** — o "38 permissions" vive em prosa | `.ai/rules/filament.md:48`, `wikis/convencoes.md` | **corrige o `01-plano-acao.md`**: nenhum teste existente vai ficar vermelho pela contagem. O único guarda do recorte de escrita são **CT-16, CT-21 e CT-22/CT-23/CT-24** deste arquivo |
| Tabelas do kit usam `deferLoading` (via `ConfiguraFilamentGlobal`) — **`->loadTable()` é obrigatório** antes de `assertCanSeeTableRecords` | `tests/Tenancy/AdminDaOrganizacaoTest.php:129-132`, `tests/Tenancy/ConviteUsuarioExistenteTest.php:255,271` | sem ele o HTML não tem os registros e a asserção falha sem defeito |
| Teste de componente exige `Filament::setCurrentPanel('app')` | `tests/Kit/ConviteTest.php:67` | obrigatório em todo CT de Livewire deste conjunto |
| Ação de tabela é chamada pelo **nome**, não pelo FQCN | `tests/Kit/ConviteTest.php:285` (`TestAction::make('delete')->table($convite)`), `tests/Tenancy/AdminDaOrganizacaoTest.php:498` | usar essa forma |
| Factories existentes: `ConviteFactory`, `TenantFactory` (`comIdentidadeVisual`, `inativo`), `UserFactory` (`unverified`) | `database/factories/` | **`CupomFactory` não existe** — é o passo 9 do PRD. Ver `## Setup Global` |
| Não existe `app/Enums/`; models são `AgenteIa`, `Convite`, `Projeto`, `Role`, `Tenant`, `User` | `ls app/Enums` (ausente), `app/Models/` | `Cupom`, `CupomUso` e `TipoDeDesconto` nascem nesta entrega |
| `TestCase::seed()` foi sobrescrito para usar `Artisan::call`, porque `$this->seed()` padrão devolvia **0 permissions** em silêncio | `tests/TestCase.php` (docblock de `seed()`) | semear sempre por `$this->seed([...])` desta base |
| Helpers globais: `tenant()`, `usuario()`, `usuarioCom(?string)`, `usuarioDoKit()`, `usuarioComPapel()`, `papelNaOrganizacao()`, `noPainelDa()`, `duasOrganizacoes()`, `fronteiraDeRequest()`, `pivotDePapeis()`, `espiarAutenticacao()` | `tests/Pest.php:185-353` | helper novo usado por 2+ arquivos vai para `tests/Pest.php` (`.ai/rules/testes.md`) |
| Helpers de Filament 5 **não-deprecados**, conferidos no vendor | `vendor/filament/*/.stubs.php` | usar `fillForm`, `assertSchemaStateSet`, `assertHasFormErrors`, `callAction(TestAction::make('nome')->table($r))`, `assertActionExists/DoesNotExist`, `assertCanSeeTableRecords`, `assertCanNotSeeTableRecords`, `assertCountTableRecords`, `searchTable`, `assertNotified`. **Não** usar `callTableAction`, `assertTableActionExists`, `assertFormSet`, `setTableActionData` — todos `@deprecated` e silenciosos |
| `Select` do Filament nasce **nativo** (`protected bool\|Closure $isNative = true`) e só deixa de sê-lo com `searchable`/`multiple`/`htmlAllowed` | `vendor/filament/forms/src/Components/Concerns/CanBeNative.php:9`, `Select.php:1838` | o `select()` do plugin de browser funciona no CT-B01 |
| API do browser conferida no vendor | `vendor/pestphp/pest-plugin-browser/src/` | `assertPathIs`, `assertSee`, `assertSeeIn`, `assertDontSee`, `assertValue`, `assertNoJavaScriptErrors`, `assertNoSmoke`, `assertNoAccessibilityIssues`, `select`, `press`, `click`, `type`, `fill`, `attach` existem. **`waitForText` e `waitForEvent` existem nesta versão** (a `feature-wiki` afirma que não); `waitForSelector` e `waitUntil` **não** existem |

### Divergência declarada: Project Rule vence a skill

`.ai/rules/testes-browser.md` mede que **`--parallel` derruba 4 de 11 cenários de browser** e que,
**sem PCOV, o `--tia` não termina** (abortado após 35 min com Xdebug em série). A `feature-test-design`
sugere `pest --parallel --tia` como padrão. **A rule vence.** Os comandos desta feature são dois:

```bash
vendor/bin/pest --parallel --group=kit    # CT-01..CT-57
composer test:browser                     # CT-B01 — já embute `npm run build`, em série
```

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | duas tabelas (`cupons`, `cupom_usos`), dois models, um enum, uma policy, um Resource com 3 páginas, uma factory, um channel de log, **e uma alteração no `PapeisSeeder`, que é infra compartilhada dos cinco papéis do kit**. **A segunda tabela tem ciclo de vida próprio** e é o que a v1 esquecera | CT-16…CT-20, CT-47, CT-51 |
| **F**unction | cadastrar · abrir · editar · excluir · listar · validar (existência, validade, limite) · calcular desconto · consumir uso · registrar quem aplicou. Função escondida: nenhuma — não há comando artisan nem endpoint público nesta entrega | CT-01…CT-57 |
| **D**ata | `codigo` (texto humano: caixa, espaços nas bordas, **forma persistida**, comprimento) · `tipo` (2 partições) · `valor` (**domínio condicionado pelo `tipo`**) · `expira_em` (`datetime`) · **`limite_de_usos`** e `usos` (dois contadores, com fronteiras próprias) · `valorTotal` de entrada (centavos: 0, 1, maior e menor que o desconto) · `aplicado_por` (**opcional**: ausente ≠ `null`) · **dado de outra organização** · **registro-testemunha (o segundo cupom que não pode se mover)** | CT-02…CT-15, CT-24…CT-37, CT-42, CT-48…CT-52 |
| **I**nterfaces | (a) tela do painel `/app` — 3 rotas; (b) **o motor de aplicação, chamável de controller/job/comando/tinker sem passar pela tela — e aí o escopo de organização é inerte** (`BelongsToTenant:48-52`); (c) seeders. **Não há**: API pública, webhook, import, comando artisan | CT-03, CT-13, CT-17…CT-19, CT-24…CT-46, CT-53…CT-56 |
| **P**latform | **SQLite `:memory:` em teste, MySQL em produção** — e os dois tratam `NULL` como distinto num índice `UNIQUE`, o que faz `unique(['tenant_id','codigo'])` **não barrar nada em modo single-tenant**. Colação: SQLite é *case-sensitive* em `=`, MySQL `utf8mb4_unicode_ci` não é → `promo10` = `PROMO10` num banco e não no outro. **FKs aplicadas no teste** (`config/database.php:40`). **`config/app.php:68` fixa UTC ignorando `APP_TIMEZONE`** | CT-13, CT-14, CT-29, CT-38 |
| **O**perations | seis personas (`master_global`, `admin`, `admin_organizacao`, `panel_user`, `infra`, **sem papel nenhum**) × dois modos do kit (single-tenant, que é o **default**, e multi-tenant). Uso indevido esperado: usuário comum emitindo desconto para si; administradora de uma organização alcançando o cupom de outra pela URL | CT-16…CT-23, CT-53, CT-54 |
| **T**ime | expiração · **virada da validade entre a consulta e o consumo** · fuso do app × fuso do operador · **a mesma fronteira lida por dois leitores diferentes (listagem × aplicação)** · concorrência sobre o contador · idempotência ancorada num agregado que **não existe** nesta entrega | CT-22, CT-27…CT-32, CT-38, lacuna L-04 |

Nenhuma dimensão vazia.

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — O cupom só é gravado com os cinco atributos presentes | A5 (padrão) | RQ-01…RQ-06 | EP (partição inválida isolada por cenário) | CT-01, CT-02, CT-03 |
| **R2** — O `tipo` admite exatamente dois valores | A5 (padrão) | RQ-03 | EP exaustiva de domínio fechado | CT-04, CT-05 |
| **R3** — O domínio de `valor` e o de `limite_de_usos` têm fronteiras próprias | A1 (completo) | RQ-03, RQ-04, RQ-06 | tabela de decisão + BVA por partição, **na tela e fora dela** | CT-06, CT-07, CT-51, CT-55 |
| **R4** — A edição está sujeita às mesmas restrições da criação | A5 (padrão, técnica escalada) | RQ-02…RQ-06 | replicação **executada** de EP/BVA no ponto de edição | CT-08, CT-09, CT-10, CT-49, CT-52, CT-57 |
| **R5** — O código do cupom não se repete, e é gravado na forma canônica | A4 (completo) | RQ-02, RQ-14 | normalização de identidade nas **duas** direções (colisão + forma persistida) | CT-11…CT-15, CT-50 |
| **R6** — Só o admin cria, edita e exclui cupom | A3 (completo) | RQ-07 | matriz papel × ação + gate de camada da regra + IDOR por identificador | CT-16…CT-20, CT-53 |
| **R7** — Quem não é admin consegue listar cupons | A3 (completo) | RQ-08 | matriz papel × ação (leitura) | CT-21 |
| **R8** — A quem não é admin, o sistema só entrega os cupons ativos | A7 (padrão, técnica escalada) | RQ-08 | partição exaustiva do estado derivado **+ BVA no leitor da listagem** | CT-22, CT-23, CT-54 |
| **R9** — Aplicar exige que o cupom exista, e seja da organização certa | A2 (completo) | RQ-09 | EP + normalização + escopo, **inclusive fora do painel** | CT-24, CT-25, CT-26, CT-56 |
| **R10** — Aplicar exige estar dentro da validade | A2 (completo) | RQ-10 | BVA 3-valores (`datetime`, incremento 1 s) + fuso | CT-27, CT-28, CT-29 |
| **R11** — Aplicar exige não ter estourado o limite de usos | A2 (completo) | RQ-06, RQ-11 | BVA 3-valores (contador) + concorrência | CT-30, CT-31, CT-32 |
| **R12** — O desconto corresponde ao tipo e ao valor do cupom | A1 (completo) | RQ-03, RQ-04, RQ-12 | tabela de decisão + BVA com valores discriminantes de representação | CT-33, CT-34 |
| **R13** — Cada aplicação bem-sucedida consome exatamente um uso, e só do cupom aplicado | A2 (completo) | RQ-13 | rastreio de efeito (4 direções) + **registro-testemunha** | CT-35…CT-38, CT-48 |
| **R14** — Cada aplicação bem-sucedida deixa um registro auditável, que sobrevive ao cupom | A6 (completo) | RQ-15 | rastreio de efeito (4 direções) + **ciclo de vida da entidade de efeito** | CT-39…CT-43, CT-47 |
| **R15** — O cadastro é operável pela tela, e só os campos do formulário chegam ao banco | A5 (padrão) | RQ-01, RQ-13 | gate de tela de escrita + mass assignment | CT-44, CT-45, CT-46 |

Toda `RQ` do `00-requisito.md` gerou ao menos uma regra **e ao menos um cenário que a falsifica**:

| RQ | Regra(s) | Cenário que falsifica a cláusula |
|---|---|---|
| RQ-01 | R1, R15 | CT-01, CT-44 |
| RQ-02 | R1, R5 | CT-02, **CT-50** (a forma persistida, não só a colisão) |
| RQ-03 | R2, R3, R12 | CT-04, CT-05, CT-06, CT-07, CT-33 |
| RQ-04 | R3, R12 | CT-06, CT-07, **CT-49**, **CT-55**, CT-33 |
| RQ-05 | R1, R4, R10 | CT-02, CT-27, CT-29 |
| RQ-06 | R1, R3, R4, R11 | CT-02, **CT-51** (fronteira do limite), **CT-52** (reduzir abaixo dos usos), CT-30 |
| RQ-07 | R6 | CT-16, CT-17, CT-18, CT-19, **CT-53** (IDOR por identificador) |
| RQ-08 | R7, R8 | CT-21, CT-22, CT-23, **CT-54** (o "apenas" — nenhuma via alcança o não-ativo) |
| RQ-09 | R9 | CT-24, CT-25, CT-26, **CT-56** (fora do painel) |
| RQ-10 | R10 | CT-27, CT-28, CT-29 |
| RQ-11 | R11 | CT-30, CT-31, CT-32 |
| RQ-12 | R12 | CT-33, CT-34 |
| RQ-13 | R13, R15 | CT-35…CT-38, **CT-48** (o cupom-testemunha), CT-46 |
| RQ-14 | R5 | CT-11, CT-12, CT-13, CT-14, CT-15 |
| RQ-15 | R14 | CT-39…CT-43, **CT-47** (a trilha sobrevive à exclusão — o *"auditar depois"*) |

---

## Fronteira com o Plano

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| Nomes `Cupom::valido()`, `aplicarEm()`, `descontoSobre()`, `scopeAtivos()`, `situacao()` | escolha de implementação | **detalhe do cenário** |
| Nomes de tabela/coluna (`cupons`, `cupom_usos`, `expira_em`, `limite_de_usos`, `usos`) | escolha de implementação | detalhe do cenário |
| `cascadeOnDelete` em `cupom_usos.cupom_id` | escolha de implementação — **mas a consequência dela contradiz RQ-15** | **CT-47**. O oráculo não é a cláusula da FK; é *"pra gente conseguir auditar depois"* |
| `maxValue(100)` no percentual e `minValue(1)` em `valor`/`limite_de_usos` | só o PRD determina, e é comportamento visível ao usuário | **pergunta P-A** + cenários `@premissa` CT-06, CT-07, CT-49, CT-51, CT-55 |
| `minDate(now())` no `expira_em` | idem — o card não proíbe cadastrar cupom já vencido | **pergunta P-B** + CT-02 (linha `validade no passado`) |
| `->live()` no `Select` de tipo e o rótulo do campo `valor` mudando com ele | idem — o card não fala de rótulo nem de unidade na tela | **pergunta P-C** + CT-B01 `@premissa` |
| Rótulos "Ativo"/"Esgotado"/"Expirado" e a ordem de precedência entre eles | idem — o card diz "ativos", nunca nomeia os outros dois | **pergunta P-D**. Os cenários afirmam **inclusão/alcance**, nunca o texto do badge |
| `string('codigo', 40)` | escolha de implementação; o card não dá comprimento | detalhe. A borda de 40 chars **não** é oráculo — lacuna **L-05** |
| `RuntimeException` como forma da recusa no consumo | escolha de implementação | detalhe. Os cenários afirmam **o não-efeito**, não a classe |
| Padrão de log `[Classe@metodo]` e channel `cupom` | convenção do projeto, não requisito | **aceito como cenário de convenção** (CT-43), declarado como tal |
| Recorte `escritaVedadaAoUsuarioComum()` no `PapeisSeeder` | mecanismo | detalhe. O oráculo de R6 é **o que a pessoa consegue fazer** |
| Afirmação do PRD de que `tests/Kit/PaineisTest.php` "vai ficar vermelho" na contagem de permissões | **verificado como falso**: o teste não afirma número nenhum | registrado no `## Arnês` — nenhuma regressão automática existe, o guarda é CT-16/CT-21 |

**O valor literal do requisito não foi parametrizado.** O card não traz nenhum número — nem
percentual, nem limite, nem prazo. Não há "valor do requisito" a proteger de injeção por `config()`,
e nenhum cenário depende de chave de ambiente. Os números dos `Exemplos:` são **escolhidos para
discriminar**, e a coluna `# o que a linha revela` diz o que cada um separa.

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` desta feature está **fechado para edição** (linha de base
> imutável desta execução). A skill manda devolver as perguntas novas para `## Ambiguidades` do `00`;
> como isso não é possível, elas ficam aqui, **em bloco pronto para colagem**, no formato da seção de
> destino. Cada uma continua **bloqueando** o que depende dela.

```markdown
### P-A — o valor e o limite de usos têm domínio?

RQ-04 dá "o valor do desconto" e RQ-06 dá "um limite de quantas vezes pode ser usado", os dois sem
domínio. O card não diz se um percentual de 150 é erro a barrar ou desconto a conceder, nem se um
limite de 0 (cupom que nunca pode ser usado) é gravável.

- **Assumido**: percentual válido de **1 a 100**; valor fixo de **1 em diante, sem teto**;
  `limite_de_usos` de **1 em diante**; `0` e negativos recusados nos três, **na criação, na edição
  e por qualquer via de escrita**.
- **Se negado**: R3 e R4 mudam de fronteira; CT-06, CT-07, CT-49, CT-51 e CT-55 são refeitos.

### P-B — cadastrar cupom já vencido é erro?

RQ-05 dá "uma data de validade"; RQ-10 diz que a aplicação recusa o vencido. O card não diz o que
acontece ao **cadastrar** ou **editar** para uma data já passada.

- **Assumido**: é permitido gravar, e o cupom nasce inaplicável.
- **Se negado**: CT-02 (linha "validade no passado") inverte, e a célula `E2 × editar` da matriz de
  estados muda de válida para inválida.

### P-C — a tela precisa dizer a unidade do campo de valor?

RQ-03 e RQ-04 põem duas grandezas na mesma coluna (ver A-05 do `00`). O card não fala da tela.

- **Assumido**: a tela **precisa** distinguir as duas unidades no momento da digitação.
- **Se negado**: CT-B01 é cortado e o `05-casos-de-teste-browser.md` deixa de existir.

### P-D — "ativo" tem rótulo, e qual estado vence quando dois valem?

RQ-08 fala em "cupons ativos". O card nunca nomeia "expirado" nem "esgotado", e nunca diz o que
mostrar num cupom que é as duas coisas.

- **Assumido**: "ativo" é estado derivado (P-03 do `00`), e os cenários afirmam **alcance** — nunca
  o texto do rótulo.
- **Se negado**: R8 ganha cenários de rótulo.

### P-E — quem pode aplicar um cupom?

RQ-09 a RQ-13 dizem "o sistema valida" e "aplica", sem sujeito. RQ-07 e RQ-08 normatizam cadastro e
listagem, nunca a aplicação. Isso deixa 6 das 36 células da matriz papel × ação sem regra.

- **Assumido**: a aplicação é chamada por quem opera a venda, e **esta entrega não tem barreira de
  autorização no motor**. CT-42 confirma metade da premissa (aplicação sem usuário identificado
  funciona); a outra metade — que nenhum papel é barrado — **não tem cenário de propósito**: um
  cenário afirmando "qualquer papel consegue aplicar" **fixaria a ausência de barreira como
  comportamento esperado**, e é o oráculo invertido que o gate proíbe.
- **Se negado**: R6 ganha uma sétima ação e 6 cenários.

### P-F — quando o desconto é maior que o total, o que fica registrado?

P-07 do `00` decide que o **resultado** é zero. Não decide o que a trilha de RQ-15 guarda: o desconto
**prometido** pelo cupom ou o **concedido**.

- **Assumido**: o **concedido** (limitado ao total).
- **Se negado**: CT-34 e CT-40 mudam de valor esperado.

### P-G — e quando não há usuário identificado aplicando?

RQ-15 pede "quem aplicou". Uma aplicação por comando, job ou integração não tem usuário.

- **Assumido**: o registro é criado **mesmo assim**, com o aplicador ausente.
- **Se negado**: CT-42 inverte, e R14 ganha uma pré-condição de autenticação.

### P-H — a unicidade de RQ-14 vale onde a organização não existe?

P-04 do `00` decide unicidade **por organização**. Em single-tenant — o **default** do kit
(`config/kit.php:59`, `.env:76`) — não há organização, `tenant_id` é nulo, e **nenhum banco considera
dois `NULL` iguais num índice `UNIQUE`**: a barreira de banco não barra nada.

- **Assumido**: RQ-14 vale **também** em single-tenant, e **também** fora da tela.
- **Se negado**: CT-13 sai do conjunto. Até lá, **CT-13 é o cenário que falseia o mecanismo do
  plano**, e é esperado que fique vermelho.

### P-I — a trilha de RQ-15 sobrevive à exclusão do cupom?

RQ-07 dá ao admin o direito de excluir; RQ-15 pede o registro "pra gente conseguir auditar
**depois**". As duas colidem: se a exclusão do cupom levar a trilha junto, RQ-15 é decorativa —
some exatamente o que alguém iria auditar.

- **Assumido**: a trilha **sobrevive**. "Auditar depois" só significa alguma coisa se o registro
  durar mais que o registro-pai.
- **Se negado**: CT-47 inverte, e RQ-15 passa a valer só enquanto o cupom existir — o que precisa
  estar escrito, porque é uma decisão de retenção, não um detalhe de chave estrangeira.

### P-J — reduzir o limite abaixo dos usos já feitos é permitido?

RQ-06 dá "um limite de quantas vezes pode ser usado" e RQ-07 permite editar. O card não previu a
combinação: um cupom com 5 usos feitos, editado para limite 2, fica com `usos > limite`.

- **Assumido**: a edição é **permitida**, e o cupom fica permanentemente inaplicável (a comparação
  de RQ-11 continua valendo). O que **não** pode acontecer é o cupom voltar a ser aplicável, nem o
  contador ser "corrigido" para o novo limite — isso apagaria trilha.
- **Se negado**: CT-52 inverte para "recusado", e R4 ganha uma validação cruzada entre dois campos.
```

---

## Setup Global

### Personas

| Persona | Como criar | Onde |
|---|---|---|
| `master_global` | `usuarioDoKit('master_global')` — **zero permissions no banco**, atravessa pelo `Gate::before` (`PapeisSeeder.php:53-54`) | `Kit` e `Tenancy` |
| `admin` (instalação) | `usuarioCom('admin')` | idem |
| `admin_organizacao` | `usuarioComPapel('admin_organizacao', $acme)` | **só `Tenancy`** — o papel só é semeado com a tenancy ligada (`PapeisSeeder.php:70`) |
| `panel_user` | `usuarioComPapel('panel_user', $acme)` / `usuarioDoKit('panel_user')` | ambos |
| `infra` | `usuarioCom('infra')` | ambos |
| **sem papel** | `usuarioCom(null)` | ambos — persona própria |

> **Três pessoas distintas** em todo cenário de autorização: quem cadastrou o cupom, quem tenta a
> ação, e o dono do registro na outra organização. Persona colapsada deixa a barreira de identidade
> sem nenhum cenário.

### Fixtures — e a armadilha que a revisão adversarial pegou

`CupomFactory` **não existe** (`database/factories/` tem só `Convite`, `Tenant`, `User`). Ela é o
passo 9 do PRD. Estados necessários:

```php
Cupom::factory()->create()                          // Ativo
Cupom::factory()->expirado()->create()              // fora da validade, com uso disponível
Cupom::factory()->comUsos(2)->create()              // 2 usos E 2 linhas em `cupom_usos`
Cupom::factory()->esgotado()->create()              // usos == limite E as linhas de trilha correspondentes
Cupom::factory()->expirado()->esgotado()->create()  // E4
Cupom::factory()->fixo(1_000)->create()             // tipo = valor fixo, 1000 centavos
```

> ⚠️ **`usos` e `cupom_usos` têm de nascer coerentes.** A primeira versão deste arquivo especificava
> o state `esgotado()` como um `forceFill(['usos' => …])` puro — o contador subia e **nenhuma linha
> de trilha era criada**. Consequência, apontada pela revisão: os cenários que afirmam sobre a trilha
> anterior (CT-09) e sobre a contagem de registros (CT-31) ficariam **insatisfazíveis contra uma
> implementação correta**, e seriam "consertados" por enfraquecimento na materialização — que é
> exatamente como um oráculo morre sem ninguém notar. E a linha "a exclusão é bloqueada por FK da
> trilha" (M-R15.3) não teria FK nenhuma a violar.
>
> **Especificação correta**: `comUsos(int $n)` e `esgotado()` criam as `n` linhas de `cupom_usos`
> **e** sincronizam o contador, no mesmo `afterCreating`. `usos` fica fora do `$fillable` (é
> contador), então `state(['usos' => …])` é **descartado em silêncio** — o caminho é
> `forceFill()->save()` dentro do `afterCreating`, depois de criar as linhas.

### Seeders

Os dois, **nesta ordem**, pelo `seed()` sobrescrito de `Tests\TestCase`:

```php
$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
```

Obrigatório em **todo** cenário de autorização e de tela: Resource novo nasce sem permission e
responde 403 para quem não seja `master_global` (`.ai/rules/filament.md`).

### Componente Livewire

- `Filament::setCurrentPanel('app')` **antes** de `livewire(...)` (`tests/Kit/ConviteTest.php:67`).
- Em `tests/Tenancy`, `noPainelDa($acme)` — que também fixa o `PermissionRegistrar`.
- **`->loadTable()` antes de qualquer asserção de tabela**: as tabelas do kit carregam adiadas
  (`deferLoading`), e sem ele o HTML não tem os registros — a asserção falha sem defeito
  (`tests/Tenancy/AdminDaOrganizacaoTest.php:129-132`).

### Fakes e controle de tempo

- `freezeTime()` em todo cenário que afirma sobre "quando" (R10, R14).
- `travelTo()` para a virada da validade; **sempre com closure ou `travelBack()`**, senão vaza.
- `config(['app.timezone' => …])` em CT-29 — é o parâmetro livre daquele cenário.
- Log: generalizar `espiarAutenticacao()` (`tests/Pest.php:253-261`) para
  `espiarCanal(string $canal)` e manter a chamada existente. **Não** criar `espiarCupom()` ao lado:
  `.ai/rules/testes.md` proíbe o clone com outro nome.
- **Nenhum** `Queue::fake()`, `Mail::fake()` ou `Http::fake()`: a feature não enfileira, não envia e
  não chama serviço externo.

### Estratégia de DB e de camada

- `RefreshDatabase` já é global nas cinco pastas. Nada a acrescentar.
- **Não existe camada `Unit` utilizável** (ver `## Arnês`). A camada mais barata que o arnês deste
  projeto sustenta é `tests/Kit`.

| Arquivo | Suíte | Modo | O que cobre |
|---|---|---|---|
| `tests/Kit/CupomTest.php` | `Kit` (grupo `kit`) | single-tenant | domínio: gravação direta, cálculo, validação, consumo, trilha, unicidade com `tenant_id` nulo |
| `tests/Kit/CupomPainelTest.php` | `Kit` (grupo `kit`) | single-tenant | componente Livewire: formulário, tabela, ações, autorização na tela |
| `tests/Tenancy/CupomTenancyTest.php` | `Tenancy` (grupo `kit`) | multi-tenant | isolamento, unicidade por organização, IDOR, matriz com `admin_organizacao`, escopo fora do painel |
| `tests/Browser/CupomTest.php` | `Browser` (grupo `browser`) | single-tenant | CT-B01 — ver `05-casos-de-teste-browser.md` |

---

## Matriz Estado × Operação

**Montada do ciclo de vida, não do mapa de regras.** Os estados saem das duas condições
independentes que o card define (RQ-05 validade, RQ-06 limite), mais a existência do registro.

**6 estados × 6 operações = 36 células.** Válidas (a operação deve funcionar / o registro deve ser
alcançado): **16**. Inválidas (deve ser recusada / não alcançado): **16**. Não se aplica: **4**.
Lacunas declaradas nesta matriz: **0**. *(Somatório conferido célula a célula: 16 + 16 + 4 = 36.)*

| | **criar** com este código | **listar** (usuário comum) | **abrir** para edição | **editar** | **excluir** | **aplicar** |
|---|---|---|---|---|---|---|
| **E1** Ativo | ❌ CT-11 L1 | ✅ CT-22 L1 | ✅ CT-57 L1 | ✅ CT-08 | ✅ CT-45 L1 | ✅ CT-30 L1 |
| **E2** Expirado (validade vencida, uso disponível) | ❌ CT-11 L2 | ❌ CT-22 L2 | ✅ CT-57 L2 | ✅ CT-09 L1 | ✅ CT-45 L2 | ❌ CT-27 L3 |
| **E3** Esgotado (dentro da validade, usos = limite) | ❌ CT-11 L3 | ❌ CT-22 L3 | ✅ CT-57 L3 | ✅ CT-09 L2 | ✅ CT-45 L3 | ❌ CT-30 L3 |
| **E4** Expirado **e** esgotado | ❌ CT-11 L4 | ❌ CT-22 L4 | ✅ CT-57 L4 | ✅ CT-09 L3 | ✅ CT-45 L4 | ❌ CT-32 |
| **E5** Excluído do cadastro | ✅ CT-15 | ❌ CT-45 † | ❌ CT-10 | ❌ CT-10 | ❌ CT-45 L5 | ❌ CT-26 |
| **E6** Inexistente (código nunca cadastrado) | ✅ CT-01 | *n/a: nada a listar* | *n/a: sem registro* | *n/a: sem registro* | *n/a: sem registro* | ❌ CT-24 L5 |

**Leitura das duas metades**, que é onde a matriz costuma mentir:

- **Cada coluna tem ao menos uma célula válida exercitada.** `abrir` tem CT-57 (o formulário carrega
  os valores gravados, nos quatro estados) — na v1 essa coluna inteira apontava para um cenário que
  executava **outra** operação, e portanto tinha **zero** células válidas. `editar` tem CT-08 (edição
  que funciona e grava). `excluir` tem CT-45 L1..L4.
- **A dimensão do `campo alterado` é aberta fora do estado inicial.** CT-09 altera **o `tipo` e o
  `valor`** — os campos que decidem o cálculo — em cupons que **já têm uso registrado**, e o `Então`
  afirma **o valor gravado** e a **imutabilidade da trilha anterior**. CT-49 e CT-52 alteram os
  mesmos campos para valores **inválidos**, que é a metade que a v1 declarava e não executava.
- **A dimensão da `persona`** é aberta pela matriz papel × ação abaixo. O cruzamento das duas —
  persona comum × estado não-ativo — é CT-22 (listagem) e **CT-54** (nenhuma outra via alcança).
- **A entidade do efeito colateral tem ciclo de vida próprio**, e a v1 não o modelava: `CupomUso`
  aparece em `E1..E4 × excluir` através de **CT-47**, que é o único cenário que afirma o que
  acontece com a trilha quando o cupom-pai morre.
- **Verbo irmão não herda evidência**: em R6 a autorização é falseada em cada um dos três verbos de
  escrita (CT-17, CT-18, CT-19), não só no primeiro.

† `E5 × listar`: a assertion de CT-45 é *"o cupom deixa de existir"*, **mais forte** que "não aparece
na lista". Marcado com † para que a substituição fique visível, e não escondida atrás de um ✅.

---

## Matriz Papel × Ação

**6 personas × 6 ações = 36 células.** Determinadas pelo requisito: **30**.
**Não determinadas: 6** (a coluna `aplicar` inteira → **pergunta P-E**).
*(Somatório: 30 + 6 = 36.)*

> Cada célula nomeia o cenário **e** a linha que a executa. Em CT-16 a linha é o par
> ⟨papel, verbo⟩ da própria célula — 6 papéis × 4 verbos = **24 linhas de `Exemplos`**, uma por
> célula desta tabela nas quatro colunas de escrita/abertura.

| Persona | criar | abrir | editar | excluir | listar | aplicar |
|---|---|---|---|---|---|---|
| `master_global` | ✅ CT-16 | ✅ CT-16 · CT-57 | ✅ CT-16 | ✅ CT-16 | ✅ CT-21 | ⬜ P-E |
| `admin_organizacao` (só multi-tenant) | ✅ CT-16 | ✅ CT-16 | ✅ CT-16 | ✅ CT-16 | ✅ CT-21 | ⬜ P-E |
| `panel_user` | ❌ CT-16 · **CT-17** | ❌ CT-16 · **CT-54** | ❌ CT-16 · **CT-18** | ❌ CT-16 · **CT-19** | ✅ CT-21 | ⬜ P-E |
| `admin` (instalação) | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-21 ‡ | ⬜ P-E |
| `infra` | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-16 ‡ | ❌ CT-21 ‡ | ⬜ P-E |
| sem papel nenhum | ❌ CT-16 | ❌ CT-16 | ❌ CT-16 | ❌ CT-16 | ❌ CT-21 | ⬜ P-E |

> **Correção de auditoria própria, depois da revisão**: a primeira redação da v2 acrescentou a coluna
> `abrir` à matriz (achado B-18) mas apontou as seis células para **CT-16**, cujo `Quando` só tinha os
> verbos `criar`, `editar` e `excluir`. Era o **mesmo defeito de M-1 reintroduzido em outra coluna** —
> célula apontando para um cenário que não executa a operação dela. CT-16 passou a ter o verbo
> `abrir` nas seis personas. Registrado, e não corrigido em silêncio: a facilidade com que este erro
> reaparece é o argumento de existir a contagem por célula.

- **CT-17, CT-18 e CT-19 disparam os três verbos de escrita por fora do componente de UI** — é o
  gate de camada da regra. Sem eles, a matriz fecharia inteira na camada onde *"a regra existe"* e
  *"a tela chama a regra"* são indistinguíveis por construção.
- **‡ — limitação declarada, não coberta por rodeio.** As linhas `admin` e `infra` são recusadas por
  um mecanismo **diferente** do que RQ-07 normatiza: `roles.painel` não é `app`, então elas nem
  alcançam o painel (`.ai/rules/filament.md` → "Papel novo precisa declarar o painel"). **Essas 10
  células provam inacessibilidade de painel, não autorização sobre a ação** — com a policy
  inteiramente ausente, elas continuariam recusadas. Quem falsifica RQ-07 é a linha `panel_user`
  (CT-16 L3 + CT-17/18/19) e, entre organizações, **CT-53**. Estava implícito na v1 e a revisão
  adversarial cobrou o registro.
- **A coluna `aplicar` não tem célula exercitada**, e é deliberado — ver **P-E**. Escrever "qualquer
  papel consegue aplicar" **fixaria a ausência de barreira como comportamento esperado**, que é o
  oráculo invertido que o gate proíbe. **CT-42** confirma a metade segura da premissa (a aplicação
  funciona sem usuário identificado). O que fica declarado é: **se alguém acrescentar uma barreira
  de autorização no motor, nada neste conjunto fica vermelho.**
- **A matriz cruza papel × ação; ela não cruza papel × dono do registro.** Essa terceira dimensão é
  **CT-53** — a administradora de uma organização alcançando o cupom de outra pelo identificador.

---

# Regras e Cenários

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
```

---

## Regra R1 — O cupom só é gravado com os cinco atributos presentes

> `RQ-01`…`RQ-06` · área **A5**, perfil **padrão** · técnica: **EP**, cada partição inválida isolada

```gherkin
  Regra: um cupom sem código, tipo, valor, validade ou limite de usos não é gravado

    Esquema do Cenário: [CT-01] a administradora cadastra um cupom completo
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora cadastra um cupom com código "PROMO10", tipo "<tipo>",
             valor <valor>, validade em 30/09/2026 18:00 e limite de 5 usos
      Então existe um cupom com esses cinco valores exatos e com 0 usos consumidos

      Exemplos:
        | tipo        | valor | # o que a linha revela                                        |
        | porcentagem | 10    | partição do discriminador — a gravação do ramo percentual      |
        | fixo        | 1000  | partição do discriminador — o ramo de valor fixo NÃO é atalho |

    Esquema do Cenário: [CT-02] cada atributo ausente impede a gravação, isoladamente
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora tenta cadastrar um cupom com "<campo>" no estado "<estado>"
             e os outros quatro atributos preenchidos
      Então o cadastro é recusado e nenhum cupom existe

      Exemplos:
        | campo          | estado             | # o que a linha revela                             |
        | codigo         | ausente            | campo obrigatório omitido do payload               |
        | codigo         | vazio              | ausente ≠ vazio                                    |
        | codigo         | só espaços         | a normalização não pode transformar isto em válido |
        | tipo           | ausente            |                                                    |
        | valor          | ausente            | 0 não é ausente — o 0 é CT-06                      |
        | expira_em      | ausente            |                                                    |
        | expira_em      | validade no passado| ⚠️ **`@premissa` P-B: o resultado esperado é ACEITO** — ver a nota abaixo |
        | limite_de_usos | ausente            |                                                    |

    Esquema do Cenário: [CT-03] a obrigatoriedade também vale fora do formulário   @premissa
      Dado que não existe nenhum cupom cadastrado
      Quando o sistema tenta gravar um cupom direto no domínio, sem "<campo>"
      Então a gravação é recusada e nenhum cupom existe

      Exemplos:
        | campo          |
        | codigo         |
        | tipo           |
        | valor          |
        | expira_em      |
        | limite_de_usos |
```

> **A linha `validade no passado` de CT-02 tem resultado invertido** — é a única linha da tabela cujo
> `Então` é *aceito, e o cupom nasce inaplicável*, e ela está aqui em vez de num cenário próprio para
> que a partição fique ao lado das irmãs. Ela é `@premissa` **P-B**: o card só normatiza a aplicação
> do vencido (RQ-10), nunca o cadastro dele.
>
> **CT-03 é o gate de camada da regra aplicado a R1.** É o único cenário capaz de separar *"a regra
> existe"* de *"o formulário chama a regra"*: uma implementação com `->required()` no `TextInput` e
> nada no banco fica **verde em CT-01 e CT-02 e vermelha aqui**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R1.1 | `required` só no formulário; o banco aceita nulo | **CT-03** |
| M-R1.2 | `trim` aplicado depois da validação — código só com espaços passa e vira vazio | CT-02 (linha "só espaços") |
| M-R1.3 | validação escrita para o ramo `porcentagem` e o ramo `fixo` cai fora dela | CT-01 (linha `fixo`) |
| M-R1.4 | `limite_de_usos` sem obrigatoriedade e com default no banco | CT-02 (linha `limite_de_usos`) |
| M-R1.5 | `usos` nasce em 1 (o cadastro conta como uso) | CT-01 (`Então … 0 usos consumidos`) |

---

## Regra R2 — O `tipo` admite exatamente dois valores

> `RQ-03` · área **A5**, perfil **padrão** · técnica: **EP exaustiva de domínio fechado**

```gherkin
  Regra: porcentagem e valor fixo são os únicos tipos de desconto

    Cenário: [CT-04] um terceiro tipo é recusado no cadastro
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora tenta cadastrar um cupom com tipo "frete_gratis"
      Então o cadastro é recusado e nenhum cupom existe

    Cenário: [CT-05] um terceiro tipo é recusado também fora do formulário
      Dado um cupom "PROMO10" ativo, do tipo porcentagem e valor 10
      Quando o sistema tenta gravar o tipo "frete_gratis" nesse cupom, direto no domínio
      Então a gravação é recusada e o cupom continua com tipo porcentagem e valor 10
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R2.1 | `tipo` é `string` livre, validado só por uma lista no formulário | CT-05 |
| M-R2.2 | tipo desconhecido cai num ramo `default` que trata como porcentagem | CT-04 (o cadastro não pode ser aceito) e CT-33 |
| M-R2.3 | a validação existe no cadastro e some na edição | CT-05 |

---

## Regra R3 — O domínio de `valor` e o de `limite_de_usos` têm fronteiras próprias

> `RQ-03`, `RQ-04`, `RQ-06` · área **A1**, perfil **completo** · técnica: **tabela de decisão**
> (discriminador × dependente) + **BVA**, incremento 1, **na tela e fora dela**
> **Todo este bloco é `@premissa`** — ver **P-A**.

```gherkin
  Regra: o valor admissível de um campo numérico do cupom depende do tipo dele    @premissa

    Esquema do Cenário: [CT-06] a fronteira do valor percentual é 1 e 100
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora tenta cadastrar um cupom de tipo porcentagem com valor <valor>
      Então o resultado é "<resultado>" e "<efeito>"

      Exemplos:
        | valor | resultado | efeito                                     | # borda                                   |
        | -1    | recusado  | nenhum cupom existe                        | abaixo do piso                            |
        | 0     | recusado  | nenhum cupom existe                        | piso−1 — desconto de nada não é desconto  |
        | 1     | aceito    | existe um cupom com valor exatamente 1     | piso                                      |
        | 99    | aceito    | existe um cupom com valor exatamente 99    | teto−1                                    |
        | 100   | aceito    | existe um cupom com valor exatamente 100   | teto — 100 % é desconto total, não erro   |
        | 101   | recusado  | nenhum cupom existe                        | teto+1 — é aqui que `<` e `<=` se separam |

    Esquema do Cenário: [CT-07] o valor fixo tem piso e não tem teto
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora tenta cadastrar um cupom de tipo fixo com valor <valor>
      Então o resultado é "<resultado>" e "<efeito>"

      Exemplos:
        | valor  | resultado | efeito                                       | # borda                                              |
        | -1     | recusado  | nenhum cupom existe                          | abaixo do piso                                       |
        | 0      | recusado  | nenhum cupom existe                          | piso−1                                               |
        | 1      | aceito    | existe um cupom com valor exatamente 1       | piso — 1 centavo                                     |
        | 101    | aceito    | existe um cupom com valor exatamente 101     | **o teto de 100 NÃO se aplica aqui** — o par de CT-06|
        | 500000 | aceito    | existe um cupom com valor exatamente 500000  | R$ 5.000,00 — nenhum teto superior                   |

    Esquema do Cenário: [CT-51] a fronteira do limite de usos           @premissa
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora tenta cadastrar um cupom com limite de <limite> usos
      Então o resultado é "<resultado>" e "<efeito>"

      Exemplos:
        | limite | resultado | efeito                                          | # borda                                        |
        | -1     | recusado  | nenhum cupom existe                             | abaixo do piso                                 |
        | 0      | recusado  | nenhum cupom existe                             | piso−1 — cupom que nunca pode ser usado        |
        | 1      | aceito    | existe um cupom com limite exatamente 1         | piso — o cupom de uso único                    |
        | 3      | aceito    | existe um cupom com limite exatamente 3         | dentro — é o limite usado pela BVA de CT-30    |

    Esquema do Cenário: [CT-55] as mesmas fronteiras valem fora do formulário     @premissa
      Dado que não existe nenhum cupom cadastrado
      Quando o sistema tenta gravar, direto no domínio, um cupom de tipo "<tipo>"
             com valor <valor> e limite de <limite> usos
      Então a gravação é recusada e nenhum cupom existe

      Exemplos:
        | tipo        | valor | limite | # a fronteira violada           |
        | porcentagem | 101   | 3      | teto do percentual              |
        | porcentagem | 0     | 3      | piso do valor                   |
        | fixo        | 0     | 3      | piso do valor no ramo fixo      |
        | porcentagem | 10    | 0      | piso do limite de usos          |
```

> **A linha `101 → aceito` de CT-07 é o par obrigatório da linha `101 → recusado` de CT-06.** Sem
> ela, uma implementação que aplica o teto de 100 aos **dois** tipos fica verde no conjunto inteiro,
> e o cupom de R$ 10,00 (valor `1000`) passa a ser impossível de cadastrar.
>
> **A coluna `efeito` existe porque `"aceito"`/`"recusado"` sozinho não é oráculo** — foi achado da
> revisão adversarial ([B-01](#achados-da-revisão)). Sem ela, as linhas `recusado` passariam com uma
> implementação que **grava e depois** exibe erro, e as linhas `aceito` passariam com uma
> implementação que **satura** o valor (`min($valor, 100)`): `500000` viraria `100` e ninguém veria.
>
> **CT-55 fecha a lacuna L-01 da v1.** Ela havia sido recusada com o argumento de que testaria a
> premissa P-A e não RQ-04 — argumento que, se valesse, apagaria também CT-06, CT-07 e CT-51, que
> testam a mesma premissa e foram escritos. Inconsistência apontada pela revisão
> ([B-16](#achados-da-revisão)) e corrigida: a premissa é a mesma, o rigor tem de ser o mesmo, e é
> este o único cenário que impede a fronteira de viver só no formulário.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R3.1 | o teto de 100 é aplicado a `valor` sem olhar o `tipo` | CT-07 (linhas 101 e 500000) |
| M-R3.2 | `<= 100` virou `< 100` | CT-06 (linha 100) |
| M-R3.3 | piso escrito como `>= 0` em vez de `>= 1` | CT-06, CT-07 e CT-51 (linha 0) |
| M-R3.4 | o campo é `unsignedInteger` e o `-1` chega ao banco como valor enorme, sem validação em PHP | CT-06, CT-07 e CT-51 (linha −1) |
| M-R3.5 | a fronteira existe no formulário e não na gravação direta | **CT-55** (era lacuna na v1) |
| M-R3.6 | o valor é saturado no teto em vez de recusado (`min($valor, 100)`) | CT-06 (linha 101, coluna `efeito`) e CT-07 (linha 500000) |
| M-R3.7 | `limite_de_usos` não tem fronteira nenhuma — só `valor` a tem | **CT-51** e CT-55 (última linha) |

---

## Regra R4 — A edição está sujeita às mesmas restrições da criação

> `RQ-02`…`RQ-06` no ponto de **edição** · área **A5**, perfil **padrão** com **técnica escalada** ·
> técnica: replicação **executada** de EP/BVA no segundo ponto de decisão

```gherkin
  Regra: as restrições de cadastro valem também ao salvar um cupom existente

    Cenário: [CT-08] salvar um cupom sem alterar nada é aceito
      Dado um cupom "PROMO10" ativo, de tipo porcentagem e valor 10, com 0 usos
      Quando a administradora abre esse cupom e salva sem alterar nenhum campo
      Então o cupom continua com código "PROMO10", tipo porcentagem, valor 10 e 0 usos

    Esquema do Cenário: [CT-57] o formulário de edição carrega os valores gravados
      Dado um cupom "PROMO10" no estado "<estado>", de tipo porcentagem, valor 10
            e limite de 3 usos
      Quando a administradora abre esse cupom para edição
      Então o formulário apresenta código "PROMO10", tipo porcentagem, valor 10
            e limite de 3 usos

      Exemplos:
        | estado              | # célula da matriz de estados |
        | Ativo               | E1 × abrir                    |
        | Expirado            | E2 × abrir                    |
        | Esgotado            | E3 × abrir                    |
        | Expirado e esgotado | E4 × abrir                    |

    Esquema do Cenário: [CT-09] o tipo e o valor podem ser alterados em cupom já usado
      Dado um cupom "PROMO10" no estado "<estado>", de tipo porcentagem e valor 10,
            com 2 usos já registrados e as 2 linhas de trilha correspondentes
      Quando a administradora altera o tipo para fixo e o valor para 1500, e salva
      Então o cupom passa a ter tipo fixo e valor 1500, e continua com 2 usos
      E os 2 registros de uso anteriores continuam com os valores com que foram gravados

      Exemplos:
        | estado                | # célula da matriz de estados |
        | Expirado              | E2 × editar                   |
        | Esgotado              | E3 × editar                   |
        | Expirado e esgotado   | E4 × editar                   |

    Esquema do Cenário: [CT-49] a fronteira do valor vale também na edição     @premissa
      Dado um cupom "PROMO10" ativo, de tipo "<tipo>", valor <valor_atual>
            e limite de 3 usos
      Quando a administradora altera o "<campo>" para <novo> e salva
      Então a alteração é recusada e o cupom continua com "<campo>" igual a <valor_atual>

      Exemplos:
        | tipo        | campo          | valor_atual | novo | # a fronteira violada        |
        | porcentagem | valor          | 10          | 101  | teto do percentual, na edição|
        | porcentagem | valor          | 10          | 0    | piso do valor, na edição     |
        | fixo        | valor          | 1000        | -1   | abaixo do piso, na edição    |
        | porcentagem | limite_de_usos | 10          | 0    | piso do limite, na edição    |

    Cenário: [CT-52] reduzir o limite abaixo dos usos já feitos    @premissa
      Dado um cupom "PROMO10" ativo, com limite de 5 usos e 5 usos já registrados
      Quando a administradora reduz o limite para 2 e salva
      Então o cupom passa a ter limite 2 e continua com 5 usos registrados
      E o cupom continua inaplicável, e as 5 linhas de trilha continuam existindo

    Cenário: [CT-10] um cupom excluído não pode ser aberto nem editado
      Dado um cupom "PROMO10" que foi excluído do cadastro
      Quando a administradora tenta abrir esse cupom para edição pela URL dele
      Então a operação é recusada e nenhum cupom com o código "PROMO10" existe
```

> **CT-49 e CT-52 fecham [I-4, B-07 e B-10](#achados-da-revisão).** A v1 declarava a técnica
> "replicação de EP/BVA no ponto de edição" em R4 e **não replicava um único par**: CT-08 salvava sem
> mudar nada, CT-09 editava para valores válidos, CT-10 era registro excluído e CT-12 editava o
> código. Uma implementação com `minValue`/`maxValue` só no caminho de criação — ou num `form()` que
> a página de edição sobrescreve — passava no conjunto inteiro e deixava editar um percentual para
> 500 %.
>
> **CT-52 é `@premissa` P-J** e afirma **três** coisas de propósito: o limite novo foi gravado, o
> contador **não** foi "corrigido" para caber nele, e a trilha não foi truncada. Um contador
> silenciosamente reduzido para 2 tornaria o cupom aplicável de novo e apagaria a evidência de 3 usos.
>
> **CT-57 fecha [M-1](#achados-da-revisão)**: na v1 a coluna `abrir` da matriz de estados apontava,
> nas seis células, para um cenário que executava **outra** operação — nenhum cenário abria um cupom
> expirado ou esgotado e afirmava que o formulário carregava os valores gravados.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R4.1 | a validação de unicidade acusa colisão do registro com ele próprio | **CT-08** |
| M-R4.2 | salvar zera `usos` (o `save()` reescreve o registro inteiro) | CT-08, CT-09 e CT-52 |
| M-R4.3 | alterar o `valor` do cupom reescreve retroativamente os registros de uso | CT-09 (última cláusula) |
| M-R4.4 | a edição é bloqueada em cupom expirado/esgotado, contradizendo RQ-07 | CT-09 e CT-57 (todas as linhas) |
| M-R4.5 | um registro já removido continua editável por rota direta | CT-10 |
| M-R4.6 | a fronteira de domínio vive só no caminho de criação | **CT-49** |
| M-R4.7 | reduzir o limite "conserta" o contador para caber, apagando usos | **CT-52** |
| M-R4.8 | o formulário de edição nasce com os defaults em vez dos valores gravados | **CT-57** |

---

## Regra R5 — O código do cupom não se repete, e é gravado na forma canônica

> `RQ-02`, `RQ-14` · área **A4**, perfil **completo** · técnica: **normalização de identidade nas
> duas direções** — o que colide **e** o que fica no banco

```gherkin
  Regra: dois cupons da mesma organização não têm o mesmo código

    Esquema do Cenário: [CT-11] o segundo cupom com o mesmo código é recusado
      Dado um cupom já cadastrado com o código "PROMO10", no estado "<estado>"
      Quando a administradora tenta cadastrar um segundo cupom com o código "<codigo>"
      Então o cadastro é "<resultado>" e existem <total> cupons cadastrados

      Exemplos:
        | estado              | codigo        | resultado | total | # o que a linha revela                           |
        | Ativo               | PROMO10       | recusado  | 1     | colisão exata — E1                               |
        | Expirado            | PROMO10       | recusado  | 1     | E2: cupom vencido continua ocupando o código     |
        | Esgotado            | PROMO10       | recusado  | 1     | E3                                                |
        | Expirado e esgotado | PROMO10       | recusado  | 1     | E4                                                |
        | Ativo               | promo10       | recusado  | 1     | caixa — é aqui que a normalização se prova       |
        | Ativo               | " PROMO10 "   | recusado  | 1     | espaços nas bordas                                |
        | Ativo               | BLACKFRIDAY   | aceito    | 2     | código distinto — a regra não barra demais       |

    Esquema do Cenário: [CT-50] o código é gravado exatamente na forma canônica
      Dado que não existe nenhum cupom cadastrado
      Quando a administradora cadastra um cupom com o código "<digitado>"
      Então existe 1 cupom, e o código gravado é exatamente "<gravado>"

      Exemplos:
        | digitado      | gravado       | # o que a linha revela                                        |
        | PROMO10       | PROMO10       | entrada já canônica — a normalização não pode estragá-la      |
        | promo10       | PROMO10       | caixa é normalizada                                            |
        | " PROMO10 "   | PROMO10       | espaços das bordas são removidos                               |
        | PROMO 10      | PROMO 10      | **o espaço INTERNO é preservado** — normalizar não é higienizar|
        | BLACK-FRIDAY  | BLACK-FRIDAY  | o hífen é preservado — não colapsa em BLACKFRIDAY             |

    Cenário: [CT-12] editar o código de um cupom para o de outro é recusado
      Dado dois cupons ativos, "PROMO10" e "BLACKFRIDAY"
      Quando a administradora altera o código de "BLACKFRIDAY" para "promo10" e salva
      Então a alteração é recusada e o segundo cupom continua com o código "BLACKFRIDAY"

    Cenário: [CT-13] a unicidade vale fora do formulário          @premissa
      Dado um cupom ativo com o código "PROMO10", numa instalação sem organizações
      Quando o sistema tenta gravar, direto no domínio, um segundo cupom com o código "PROMO10"
      Então a gravação é recusada e existe apenas 1 cupom com esse código

    Cenário: [CT-14] duas organizações podem ter o mesmo código     @premissa
      Dado duas organizações, Acme e Globex, cada uma com a sua administradora
      Quando a administradora da Globex cadastra um cupom "PROMO10", já existente na Acme
      Então o cadastro é aceito, e cada organização enxerga apenas o seu cupom "PROMO10"

    Cenário: [CT-15] o código de um cupom excluído volta a ficar disponível
      Dado um cupom "PROMO10" que foi excluído do cadastro
      Quando a administradora cadastra um novo cupom com o código "PROMO10"
      Então o cadastro é aceito e existe 1 cupom com esse código, com 0 usos consumidos
```

> **CT-50 fecha [I-5 e B-08](#achados-da-revisão), e corrige um falso ✅.** Na v1, o mutante
> *"normalização aplicada na leitura e não na escrita — os espaços vão para o banco"* era dado como
> morto por CT-11 linha `" PROMO10 "`; mas o `Então` daquela linha afirma apenas *recusado / 1
> cupom*, que é o **mesmo resultado nas duas implementações**. A norma é observável em duas direções
> — o que **colide** e o que **fica gravado** — e a v1 cobria só a primeira. As duas últimas linhas
> de CT-50 (espaço interno, hífen) são as que separam normalizar de **higienizar**: um
> `preg_replace('/[^A-Z0-9]/i','')` bem-intencionado faz `BLACK-FRIDAY` colidir com `BLACKFRIDAY` e
> transforma `PROMO 10` em outro código sem avisar ninguém.
>
> **CT-13 é o cenário que falseia o mecanismo do plano**, e é esperado que fique vermelho até a
> barreira existir fora do formulário. Em single-tenant `tenant_id` é nulo e **nenhum banco considera
> dois `NULL` iguais num índice `UNIQUE`**. Ver **P-H**.
>
> **CT-15 é a célula `E5 × criar`** e o item "unicidade + exclusão" do checklist. A premissa de
> mecanismo do plano (exclusão física) fixa **como** escrever o cenário — não dispensa escrevê-lo.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R5.1 | comparação sensível a caixa — `promo10` e `PROMO10` coexistem | CT-11 (linha `promo10`) |
| M-R5.2 | normalização aplicada na leitura e não na escrita — os espaços vão para o banco | **CT-50** (linha `" PROMO10 "`) — na v1 este era um **falso ✅** apontado para CT-11 |
| M-R5.3 | a unicidade ignora cupons expirados ou esgotados ("já não valem mesmo") | CT-11 (linhas E2, E3, E4) |
| M-R5.4 | `->unique()` do Laravel no lugar de `->scopedUnique()`: o código de **outra** organização bloqueia o cadastro | **CT-14** |
| M-R5.5 | a unicidade existe só no formulário | **CT-13** |
| M-R5.6 | a regra barra qualquer segundo cupom, não só o de código igual | CT-11 (linha `BLACKFRIDAY`) |
| M-R5.7 | normalização destrutiva: remove tudo que não é letra ou dígito | **CT-50** (linhas `PROMO 10` e `BLACK-FRIDAY`) |

---

## Regra R6 — Só o admin cria, edita e exclui cupom

> `RQ-07` · área **A3**, perfil **completo** · técnica: **matriz papel × ação** + **gate de camada da
> regra** (≥1 cenário por fora da UI, em **cada** verbo) + **IDOR por identificador**

```gherkin
  Regra: criar, editar e excluir cupom são ações restritas ao administrador

    Esquema do Cenário: [CT-16] a matriz de escrita, pela tela
      Dado uma organização com um cupom "PROMO10" ativo, de valor 10, cadastrado pela
            administradora
      E uma segunda pessoa com o papel "<papel>"
      Quando essa pessoa tenta "<verbo>" um cupom pela tela do painel de negócio
      Então o resultado é "<resultado>" e "<efeito>"

      Exemplos:
        | papel               | verbo   | resultado | efeito                                          |
        | master_global       | abrir   | aceito    | o formulário apresenta "PROMO10" com valor 10   |
        | admin_organizacao   | abrir   | aceito    | o formulário apresenta "PROMO10" com valor 10   |
        | panel_user          | abrir   | recusado  | o cupom "PROMO10" continua com valor 10         |
        | admin               | abrir   | recusado  | o cupom "PROMO10" continua com valor 10         |
        | infra               | abrir   | recusado  | o cupom "PROMO10" continua com valor 10         |
        | (sem papel nenhum)  | abrir   | recusado  | o cupom "PROMO10" continua com valor 10         |
        | master_global       | criar   | aceito    | existe um cupom "NOVO"                          |
        | master_global       | editar  | aceito    | o cupom "PROMO10" passa a ter valor 20          |
        | master_global       | excluir | aceito    | o cupom "PROMO10" deixa de existir              |
        | admin_organizacao   | criar   | aceito    | existe um cupom "NOVO"                          |
        | admin_organizacao   | editar  | aceito    | o cupom "PROMO10" passa a ter valor 20          |
        | admin_organizacao   | excluir | aceito    | o cupom "PROMO10" deixa de existir              |
        | panel_user          | criar   | recusado  | nenhum cupom "NOVO" existe                      |
        | panel_user          | editar  | recusado  | o cupom "PROMO10" continua com valor 10         |
        | panel_user          | excluir | recusado  | o cupom "PROMO10" continua existindo            |
        | admin               | criar   | recusado  | nenhum cupom "NOVO" existe                      |
        | admin               | editar  | recusado  | o cupom "PROMO10" continua com valor 10         |
        | admin               | excluir | recusado  | o cupom "PROMO10" continua existindo            |
        | infra               | criar   | recusado  | nenhum cupom "NOVO" existe                      |
        | infra               | editar  | recusado  | o cupom "PROMO10" continua com valor 10         |
        | infra               | excluir | recusado  | o cupom "PROMO10" continua existindo            |
        | (sem papel nenhum)  | criar   | recusado  | nenhum cupom "NOVO" existe                      |
        | (sem papel nenhum)  | editar  | recusado  | o cupom "PROMO10" continua com valor 10         |
        | (sem papel nenhum)  | excluir | recusado  | o cupom "PROMO10" continua existindo            |

    Cenário: [CT-17] o usuário comum não cria cupom por fora da tela
      Dado uma organização sem nenhum cupom cadastrado
      E um usuário com o papel panel_user
      Quando esse usuário requisita a criação de um cupom sem passar pelo formulário
      Então a requisição é recusada e nenhum cupom existe

    Cenário: [CT-18] o usuário comum não edita cupom por fora da tela
      Dado um cupom "PROMO10" ativo, de valor 10, cadastrado pela administradora
      E um usuário com o papel panel_user
      Quando esse usuário requisita a alteração do valor desse cupom para 90,
             sem passar pelo formulário
      Então a requisição é recusada e o cupom continua com valor 10

    Cenário: [CT-19] o usuário comum não exclui cupom por fora da tela
      Dado um cupom "PROMO10" ativo, cadastrado pela administradora
      E um usuário com o papel panel_user
      Quando esse usuário requisita a exclusão desse cupom sem passar pelo formulário
      Então a requisição é recusada e o cupom "PROMO10" continua existindo

    Cenário: [CT-20] no modo padrão do kit, quem cria cupom é o dono da instalação  @premissa
      Dado uma instalação com a multi-organização desligada
      E um usuário master_global e um usuário panel_user
      Quando cada um deles tenta cadastrar um cupom "PROMO10"
      Então o master_global consegue e o panel_user é recusado, e existe 1 cupom cadastrado

    Esquema do Cenário: [CT-53] a administradora de uma organização não alcança o cupom de outra
      Dado duas organizações, Acme e Globex
      E um cupom "PROMO10" ativo, de valor 10, cadastrado na Acme
      E a administradora da Globex
      Quando ela requisita "<verbo>" sobre o cupom da Acme, pelo identificador dele
      Então a requisição é recusada e "<efeito>"

      Exemplos:
        | verbo   | efeito                                              |
        | abrir   | o cupom da Acme continua com valor 10               |
        | editar  | o cupom da Acme continua com valor 10               |
        | excluir | o cupom da Acme continua existindo                  |
```

> **CT-16 foi reescrito na v2 por dois defeitos que a revisão apontou**
> ([B-02](#achados-da-revisão)), e ganhou o verbo `abrir` numa auditoria posterior
> ([B-18](#achados-da-revisão) + correção própria registrada na matriz): o `Quando` da v1 disparava
> **três operações num passo só**
> (*"tenta criar, editar e excluir"*), e o `Então` era condicional (*"quando o resultado é
> recusada…"*) — de modo que as duas linhas positivas, `master_global` e `admin_organizacao`,
> **não afirmavam nada**: passavam com uma tela que responde 200 e não persiste. Agora o verbo é
> coluna, cada linha tem um `Quando` só, e **toda** linha afirma um efeito concreto.
>
> **CT-17, CT-18 e CT-19 são o gate de camada da regra**, e são **três** porque verbo irmão não
> herda evidência. Sem eles, a matriz fecharia inteira na camada do componente.
>
> **CT-53 fecha [B-15](#achados-da-revisão) e corrige um falso ✅ do checklist.** Na v1, o item
> *"IDOR / autorização horizontal"* apontava para CT-25 e CT-14 — mas CT-25 é *apresentar um código*
> (busca por string) e CT-14 é unicidade + escopo de listagem: **nenhum dos dois acessa um registro
> de outra organização por identificador**, que é o ataque real. A matriz papel × ação cruza papel ×
> ação e nunca papel × **dono do registro**; CT-53 é essa terceira dimensão.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R6.1 | o recorte do `panel_user` tira a entidade inteira e ele perde a listagem | CT-21 (linha `panel_user`) |
| M-R6.2 | o `CupomResource` não entra em recorte nenhum e todo usuário comum emite desconto | CT-16 (linhas `panel_user`) |
| M-R6.3 | a policy é aplicada só no formulário do Filament | **CT-17, CT-18, CT-19** |
| M-R6.4 | a permissão é conferida em `create` e esquecida em `delete` | **CT-19** |
| M-R6.5 | o recorte casa por substring do nome da permission e derruba permissão de quem devia ter | CT-16 (linhas `admin_organizacao`) e CT-21 |
| M-R6.6 | a recusa acontece **depois** de a gravação já ter ocorrido | a coluna `efeito` de CT-16, e CT-17…CT-19 |
| M-R6.7 | a tela responde 200 e simplesmente não persiste, para todo mundo | a coluna `efeito` de CT-16, **linhas positivas** |
| M-R6.8 | a autorização confere o papel e não o escopo — a administradora de uma organização alcança a outra | **CT-53** |

---

## Regra R7 — Quem não é admin consegue listar cupons

> `RQ-08` · área **A3**, perfil **completo** · técnica: **matriz papel × ação** (leitura)

```gherkin
  Regra: os demais usuários do negócio conseguem listar os cupons

    Esquema do Cenário: [CT-21] a matriz de leitura
      Dado uma organização com um cupom ativo "PROMO10" cadastrado
      E uma pessoa com o papel "<papel>"
      Quando essa pessoa abre a listagem de cupons do painel de negócio
      Então a listagem é "<resultado>" e o cupom "PROMO10" "<visibilidade>"

      Exemplos:
        | papel               | resultado   | visibilidade  | # o que a linha revela        |
        | master_global       | acessível   | aparece       |                                |
        | admin_organizacao   | acessível   | aparece       | só multi-tenant                |
        | panel_user          | acessível   | aparece       | **a linha que o card escreve** |
        | admin               | inacessível | não se aplica | painel `admin`, não `app` ‡    |
        | infra               | inacessível | não se aplica | painel `infra` ‡               |
        | (sem papel nenhum)  | inacessível | não se aplica |                                |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R7.1 | o `panel_user` perde `ViewAny:Cupom` junto com as permissões de escrita | **CT-21** (linha `panel_user`) |
| M-R7.2 | a listagem é liberada a qualquer autenticado, inclusive fora do painel de negócio | CT-21 (linhas `admin`, `infra`, sem papel) |
| M-R7.3 | `getEloquentQuery()` falha aberto sem organização corrente e devolve a base inteira | CT-14 (segunda cláusula) e CT-53 |

---

## Regra R8 — A quem não é admin, o sistema só entrega os cupons ativos

> `RQ-08` · área **A7**, perfil **padrão** com **técnica escalada** · técnica: **partição exaustiva
> do estado derivado** + **BVA no leitor da listagem**, que é código diferente do leitor da aplicação

```gherkin
  Regra: para quem não administra, o sistema só entrega os cupons que ainda podem ser usados

    Esquema do Cenário: [CT-22] as situações derivadas, por persona, com as bordas
      Dado um cupom "<codigo>" com a validade "<validade>" e "<uso>"
      Quando "<persona>" abre a listagem de cupons
      Então o cupom "<visibilidade>" na listagem

      Exemplos:
        | codigo    | validade                     | uso                | persona          | visibilidade | # o que a linha revela |
        | ATIVO     | futura                       | 1 de 3 usos        | o usuário comum  | aparece      | E1 — partição          |
        | VENC      | passada                      | 1 de 3 usos        | o usuário comum  | não aparece  | E2 — partição          |
        | ESGOT     | futura                       | 3 de 3 usos        | o usuário comum  | não aparece  | E3 — partição          |
        | AMBOS     | passada                      | 3 de 3 usos        | o usuário comum  | não aparece  | E4 — partição          |
        | QUASE     | futura                       | 2 de 3 usos        | o usuário comum  | aparece      | **borda−1 do contador**|
        | HOJE0800  | hoje às 08:00, agora são 18h | 1 de 3 usos        | o usuário comum  | não aparece  | **borda do instante**  |
        | AGORA     | daqui a 1 segundo            | 1 de 3 usos        | o usuário comum  | aparece      | **borda+1 s**          |
        | ATIVO     | futura                       | 1 de 3 usos        | a administradora | aparece      | @premissa P-D          |
        | VENC      | passada                      | 1 de 3 usos        | a administradora | aparece      | @premissa P-D          |
        | ESGOT     | futura                       | 3 de 3 usos        | a administradora | aparece      | @premissa P-D          |
        | AMBOS     | passada                      | 3 de 3 usos        | a administradora | aparece      | @premissa P-D          |

    Cenário: [CT-23] o cupom sai da lista ao esgotar, sem ninguém editar o cadastro
      Dado um cupom "ULTIMO" com limite de 1 uso, 0 usos feitos e validade futura
      E que o usuário comum enxerga esse cupom na listagem
      Quando o último uso disponível do cupom é consumido
      Então o cupom deixa de aparecer na listagem do usuário comum
      E nenhum campo do cadastro do cupom foi alterado, além do contador de usos

    Esquema do Cenário: [CT-54] nenhuma outra via entrega um cupom não-ativo ao usuário comum
      Dado um cupom "<codigo>" no estado "<estado>" e um usuário com o papel panel_user
      Quando esse usuário requisita esse cupom pelo identificador dele
      Então a requisição é recusada

      Exemplos:
        | codigo | estado              |
        | VENC   | Expirado            |
        | ESGOT  | Esgotado            |
        | AMBOS  | Expirado e esgotado |
```

> **A linha `HOJE0800` de CT-22 é a que fecha [I-3 e B-04](#achados-da-revisão).** A v1 parametrizava
> a validade como `futura`/`passada` — **dias inteiros**, nunca o instante — e deixava a BVA de 1
> segundo existir apenas no caminho de **aplicação** (CT-27). Listagem e aplicação são **dois
> leitores diferentes da mesma regra derivada**: um `whereDate('expira_em','>=',today())` na
> listagem (natural para quem pensa "data de validade") convive com um `> now()` na aplicação, e o
> cupom que venceu hoje às 08:00 fica visível o dia inteiro e é recusado ao ser aplicado. Partição
> exaustiva de *combinação* não substitui fronteira de *valor*.
>
> **CT-22 foi separado por persona na v2** ([B-03](#achados-da-revisão)): a v1 tinha *"Quando o
> usuário comum **e** a administradora abrem a listagem"* — duas execuções num passo, com o `Então`
> misturando dois oráculos. Materializado, viraria um teste com dois `actingAs` cuja falha não diria
> qual metade quebrou.
>
> **CT-54 fecha a lacuna L-06 da v1 e o buraco do "apenas"** ([B-16, B-18](#achados-da-revisão)). A
> v1 recusava esse cenário como "testar o PRD"; não é. RQ-08 diz que os demais podem **apenas listar
> os cupons ativos**, e o oráculo derivável do card é *o usuário comum não alcança um cupom não-ativo
> por nenhuma via* — não apenas *não aparece na tabela*. Um filtro aplicado só na `table()`, e não na
> consulta que alimenta rota, route binding e busca, deixa a via aberta.
>
> **CT-23 é o cenário que a premissa de mecanismo P-03 não dispensa.** O plano decide que "ativo" é
> derivado; isso fixa **como** escrever o cenário, não **se** ele existe.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R8.1 | o filtro olha só a validade e ignora o limite de usos | CT-22 (linha E3) |
| M-R8.2 | o filtro olha só o limite e ignora a validade | CT-22 (linha E2) |
| M-R8.3 | o filtro é `AND` onde deveria ser `OR`, ou vice-versa — a combinação E4 escapa | CT-22 (linha E4) |
| M-R8.4 | o filtro é aplicado à administradora também, e ela perde o acesso ao que precisa editar | CT-22 (linhas `a administradora`) |
| M-R8.5 | o estado é uma coluna gravada e só muda quando alguém edita | **CT-23** |
| M-R8.6 | a listagem compara por **data** e a aplicação por **instante** | **CT-22 (linhas `HOJE0800` e `AGORA`)** — na v1 este mutante não existia e o defeito não tinha matador |
| M-R8.7 | o filtro é aplicado só na `table()` e não na consulta que alimenta rota e route binding | **CT-54** (era lacuna L-06 na v1) |
| M-R8.8 | o filtro usa `<=` no contador e entrega o cupom já esgotado | CT-22 (linhas `QUASE` e `ESGOT`) |

---

## Regra R9 — Aplicar exige que o cupom exista, e seja da organização certa

> `RQ-09` · área **A2**, perfil **completo** · técnica: **EP** (cada partição inválida isolada) +
> normalização + escopo, **inclusive no chamador que não é o painel**

```gherkin
  Regra: um código que não corresponde a um cupom da organização não é aplicável

    Esquema do Cenário: [CT-24] o código apresentado é procurado por igualdade normalizada
      Dado um cupom "PROMO10" ativo, de tipo porcentagem e valor 10, com 0 usos
      Quando o comprador apresenta o código "<apresentado>" sobre um total de 10000 centavos
      Então o resultado é "<resultado>", o total a cobrar é <total> centavos
        e o contador de usos do cupom "PROMO10" fica em <usos>

      Exemplos:
        | apresentado  | resultado | total | usos | # partição                           |
        | PROMO10      | aceito    | 9000  | 1    | igual                                 |
        | promo10      | aceito    | 9000  | 1    | caixa diferente                       |
        | " PROMO10 "  | aceito    | 9000  | 1    | espaços nas bordas                    |
        | PROM010      | recusado  | 10000 | 0    | parecido e diferente (zero × letra O) |
        | NAOEXISTE    | recusado  | 10000 | 0    | inexistente                           |
        | (vazio)      | recusado  | 10000 | 0    | vazio                                 |
        | (ausente)    | recusado  | 10000 | 0    | ausente ≠ vazio                       |

    Cenário: [CT-25] o código de outra organização não é encontrado, dentro do painel
      Dado duas organizações, Acme e Globex
      E um cupom "PROMO10" ativo, de valor 10, com 0 usos, cadastrado apenas na Acme
      Quando um comprador da Globex apresenta o código "PROMO10"
      Então o resultado é recusado, o total a cobrar não muda
        e o contador de usos do cupom da Acme continua em 0

    Cenário: [CT-56] a aplicação fora do painel não atravessa organizações
      Dado duas organizações, Acme e Globex, cada uma com um cupom "PROMO10" ativo
        e valores de desconto diferentes, ambos com 0 usos
      Quando uma rotina do sistema, fora de qualquer painel, aplica "PROMO10" para a Globex
        sobre um total de 10000 centavos
      Então o desconto aplicado é o do cupom da Globex, o contador dela fica em 1
        e o contador da Acme continua em 0

    Cenário: [CT-26] o código de um cupom excluído não é aplicável
      Dado um cupom "PROMO10" que foi excluído do cadastro depois de 1 uso
      Quando o comprador apresenta o código "PROMO10" sobre um total de 10000 centavos
      Então o resultado é recusado e o total a cobrar continua sendo 10000 centavos
```

> **CT-56 nasce de um fato verificado no código do kit, não de hipótese.**
> `app/Traits/BelongsToTenant.php:48-52` documenta, no próprio arquivo, que *"sem tenant, sem escopo:
> fora de um request de painel (job, comando, seeder, tinker) `Filament::getTenant()` é null e a
> query volta a ser global"*. O `## Ponto de Integração` do PRD declara que o motor é *"chamável de
> controller, job, comando ou Livewire"* — ou seja, **o chamador previsto é exatamente aquele em que
> o escopo é inerte**. Combinado com a premissa P-04 (o mesmo código pode existir legitimamente em
> duas organizações), uma busca por código sem filtro explícito devolve **um cupom arbitrário**, e o
> desconto de um cliente é debitado do cupom de outro. CT-25 não pega isso: ele roda dentro do painel,
> onde o escopo está ativo.
>
> **A partição `PROM010`** está aqui porque uma busca "gentil" — `LIKE`, `soundex`, comparação após
> remover caracteres — é um erro plausível, e nenhum dos outros exemplos a distingue de igualdade
> estrita. É a irmã de CT-50 do lado da leitura.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R9.1 | a busca é sensível a caixa e `promo10` não acha `PROMO10` | CT-24 (linha `promo10`) |
| M-R9.2 | a normalização é aplicada só na gravação, e o código apresentado vai cru para o `where` | CT-24 (linhas `promo10` e `" PROMO10 "`) |
| M-R9.3 | a busca usa `LIKE` ou comparação frouxa | CT-24 (linha `PROM010`) |
| M-R9.4 | código vazio devolve o primeiro cupom da tabela | CT-24 (linhas `(vazio)` e `(ausente)`) |
| M-R9.5 | o escopo por organização não é aplicado na consulta de aplicação | **CT-25** |
| M-R9.6 | a consulta ignora a exclusão porque busca por código num histórico | CT-26 |
| M-R9.7 | a busca confia no escopo global e é chamada de onde ele é inerte | **CT-56** |

---

## Regra R10 — Aplicar exige estar dentro da validade

> `RQ-10` · área **A2**, perfil **completo** · técnica: **BVA 3-valores** em `datetime`, incremento
> de **1 segundo**; o parâmetro livre do defeito de contexto é **o fuso efetivo**

```gherkin
  Regra: um cupom fora da validade não é aplicável

    Esquema do Cenário: [CT-27] a fronteira da validade é o instante gravado    @premissa
      Dado um cupom "PRAZO" ativo, com validade até 30/09/2026 18:00:00 e 0 usos
      Quando o comprador aplica o cupom em "<instante>" sobre um total de 10000 centavos
      Então o resultado é "<resultado>", o total a cobrar é <total> centavos
        e o contador de usos fica em <usos>

      Exemplos:
        | instante            | resultado | total | usos | # borda                      |
        | 30/09/2026 17:59:59 | aceito    | 9000  | 1    | borda−1 s                    |
        | 30/09/2026 18:00:00 | recusado  | 10000 | 0    | **borda exata** — `>` × `>=` |
        | 30/09/2026 18:00:01 | recusado  | 10000 | 0    | borda+1 s                    |

    Cenário: [CT-28] a validade que vira entre a consulta e o consumo é respeitada
      Dado um cupom "PRAZO" ativo, com validade até 30/09/2026 18:00:00 e 0 usos
      E que o sistema consultou e aprovou esse cupom às 17:59:59
      Quando o consumo desse mesmo cupom acontece às 18:00:01
      Então o consumo é recusado, o contador de usos fica em 0
        e nenhum registro de uso é criado

    Esquema do Cenário: [CT-29] a validade digitada vale no fuso em que foi digitada  @premissa
      Dado que o fuso efetivo da aplicação é "<fuso>"
      E que a administradora cadastra, pelo formulário, um cupom "PRAZO" válido até
        "19/08/2026 23:00" e com 0 usos
      Quando o comprador aplica o cupom no instante absoluto 2026-08-20T01:30:00Z
      Então o resultado é "<resultado>" e o contador de usos fica em <usos>

      Exemplos:
        | fuso              | resultado | usos | # o que a linha revela                                |
        | America/Sao_Paulo | aceito    | 1    | 01:30Z são 22:30 em SP — meia hora antes do limite     |
        | UTC               | recusado  | 0    | 01:30Z já passou das 23:00Z — 3 h a menos de validade  |
```

> **CT-29 existe por um defeito verificado no projeto.** `config/app.php:68` fixa
> `'timezone' => 'UTC'` **sem ler `env()`**, enquanto `.env:10` e `.env.example:10` declaram
> `APP_TIMEZONE=America/Sao_Paulo`, e não existe `.env.testing`. Quem opera acredita numa coisa e o
> sistema compara noutra. O instante `01:30Z` foi escolhido **dentro da janela de 3 h em que as duas
> implementações divergem** — às 20:00Z as duas linhas dariam o mesmo resultado e o cenário seria
> decorativo.
>
> **A coluna `total` de CT-27 foi acrescentada na v2** ([B-11](#achados-da-revisão)): a v1 afirmava
> só o contador nas linhas `recusado`, e uma implementação que **devolve o total com desconto** e
> recusa apenas o consumo passava nas três linhas. Recusar tem duas metades — o desconto não vale
> **e** o uso não é consumido.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R10.1 | `>=` no lugar de `>` — o instante exato é aceito | CT-27 (linha borda exata) |
| M-R10.2 | a comparação é por **data**, não por instante | CT-27 (as três linhas no mesmo dia), CT-29 e CT-22 (linha `HOJE0800`) |
| M-R10.3 | a validade é conferida só na consulta e não no consumo | **CT-28** |
| M-R10.4 | o instante gravado é interpretado num fuso e comparado noutro | **CT-29** |
| M-R10.5 | a validade é comparada contra uma data fixa em cache | CT-27 (três instantes na mesma execução) |
| M-R10.6 | o desconto é concedido e só o consumo é recusado | **CT-27 (coluna `total`, linhas recusadas)** |

---

## Regra R11 — Aplicar exige não ter estourado o limite de usos

> `RQ-06`, `RQ-11` · área **A2**, perfil **completo** · técnica: **BVA 3-valores** no contador
> (incremento 1) + **concorrência check-then-act**

```gherkin
  Regra: um cupom que atingiu o limite de usos não é aplicável

    Esquema do Cenário: [CT-30] a fronteira do limite é o último uso disponível
      Dado um cupom "<codigo>" ativo, do tipo "<tipo>", com limite de 3 usos
        e <ja_usado> usos já feitos
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então o resultado é "<resultado>", o total a cobrar é <total> centavos
        e o contador de usos fica em <usos_depois>

      Exemplos:
        | codigo | tipo        | ja_usado | resultado | total | usos_depois | # borda                       |
        | P3     | porcentagem | 1        | aceito    | 9000  | 2           | dentro                        |
        | P3     | porcentagem | 2        | aceito    | 9000  | 3           | borda−1 — o último uso        |
        | P3     | porcentagem | 3        | recusado  | 10000 | 3           | **borda — `<` × `<=`**        |
        | P3     | porcentagem | 4        | recusado  | 10000 | 4           | borda+1 — contador estourado  |
        | F3     | fixo        | 2        | aceito    | 9000  | 3           | a borda no ramo de valor fixo |
        | F3     | fixo        | 3        | recusado  | 10000 | 3           | **o ramo fixo não é atalho**  |

    Cenário: [CT-31] duas aplicações que partem da mesma leitura não furam o limite
      Dado um cupom "ULTIMO" ativo, com limite de 3 usos, 2 usos já feitos
        e as 2 linhas de trilha correspondentes
      E que dois atendimentos leram e aprovaram esse cupom antes de qualquer consumo
      Quando o segundo atendimento consome o cupom depois de o primeiro já o ter consumido
      Então o segundo consumo é recusado, o contador de usos fica em 3
        e existem exatamente 3 registros de uso

    Cenário: [CT-32] o cupom expirado e esgotado ao mesmo tempo é recusado
      Dado um cupom "AMBOS" com a validade vencida e o limite de usos atingido
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então o resultado é recusado, o total a cobrar continua sendo 10000 centavos,
        o contador de usos não muda e nenhum registro de uso é criado
```

> **A linha `F3` de CT-30 usa `total` de 9000 no aceite** porque o cupom `F3` é de valor fixo de
> 1000 centavos — a mesma redução do percentual de 10 %, de propósito: se um dos dois ramos calcular
> errado, CT-33 aponta a linha exata.
>
> **CT-31 separa `UPDATE ... WHERE` de check-then-act**, e é expressável em processo único: o defeito
> não é o paralelismo, é a **janela entre a leitura e a escrita**, reproduzida com duas instâncias
> lidas antes do primeiro consumo. Duas execuções verdadeiramente simultâneas não são montáveis neste
> arnês — **tentado**: `pcntl` indisponível no ambiente; `--parallel` isola por worker, não por
> conexão; e `sqlite :memory:` é por processo. O que fica de fora é a corrida no nível do banco:
> **lacuna L-04**.
>
> **A coluna `total` de CT-30 foi acrescentada na v2** pelo mesmo motivo de CT-27
> ([B-11](#achados-da-revisão)).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R11.1 | `<=` no lugar de `<` — o cupom aceita um uso a mais | CT-30 (linha `ja_usado = 3`) |
| M-R11.2 | o contador é incrementado **antes** da comparação | CT-30 (linha `ja_usado = 3`, `usos_depois = 3`) |
| M-R11.3 | ler, comparar em PHP e salvar `usos + 1` (check-then-act) | **CT-31** |
| M-R11.4 | o limite é lido do cupom e nunca comparado | CT-30 (linhas recusadas) |
| M-R11.5 | o limite é conferido no ramo percentual e não no de valor fixo | CT-30 (linha `F3 / 3`) |
| M-R11.6 | o contador é corrigido para o limite quando já está acima | CT-30 (linha `ja_usado = 4`) e **CT-52** |
| M-R11.7 | o desconto é concedido e só o consumo é recusado | **CT-30 (coluna `total`, linhas recusadas)** |

---

## Regra R12 — O desconto corresponde ao tipo e ao valor do cupom

> `RQ-03`, `RQ-04`, `RQ-12` · área **A1**, perfil **completo** · técnica: **tabela de decisão** com
> valores escolhidos para discriminar **representação**, não só fronteira

```gherkin
  Regra: o total a cobrar é o total original menos o desconto do cupom

    Esquema do Cenário: [CT-33] o desconto calculado, por tipo e por valor
      Dado um cupom ativo do tipo "<tipo>" com valor <valor>
      Quando o comprador aplica o cupom sobre um total de <total> centavos
      Então o total a cobrar passa a ser <cobrar> centavos

      Exemplos:
        | tipo        | valor | total | cobrar | # o que a linha discrimina                                     |
        | porcentagem | 29    | 10000 | 7100   | **inteiro × float**: em float o desconto dá 2899 e o total 7101 |
        | porcentagem | 10    | 9999  | 9000   | **truncar × arredondar**: arredondando o desconto é 1000 → 8999 |
        | porcentagem | 5     | 50    | 48     | resto ≠ 0 num total pequeno: desconto 2,5 → 2                   |
        | porcentagem | 1     | 99    | 99     | desconto 0,99 → 0 — o piso do truncamento                       |
        | porcentagem | 100   | 12345 | 0      | 100 % é desconto total, não erro                                |
        | porcentagem | 10    | 0     | 0      | total zero — borda inferior da entrada                          |
        | fixo        | 1000  | 12990 | 11990  | subtração direta, em centavos                                   |
        | fixo        | 12990 | 12990 | 0      | desconto exatamente igual ao total                              |
        | fixo        | 1     | 1     | 0      | borda de 1 centavo                                              |

    Cenário: [CT-34] o desconto maior que o total não gera valor negativo   @premissa
      Dado um cupom ativo do tipo fixo com valor 5000
      Quando o comprador aplica o cupom sobre um total de 3000 centavos
      Então o total a cobrar passa a ser 0 centavos
      E o registro de uso guarda 3000 centavos de valor original e 3000 de desconto concedido
```

> **Nenhum valor deste bloco é redondo por acaso.** A linha `29 % de 10000` é a única que separa
> aritmética inteira de `float`: `(int)(10000 * 0.29)` dá **2899** porque `0.29` não é representável
> em binário, enquanto `10000 * 29 / 100` dá **2900**. A linha `10 % de 9999` é a única que separa
> truncar de arredondar. Isso importa aqui mais do que em qualquer outra regra: é dinheiro, e a
> implementação errada **acerta a maioria dos valores por acidente**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R12.1 | percentual calculado em ponto flutuante | CT-33 (linha 29 %) |
| M-R12.2 | arredondar em vez de truncar | CT-33 (linhas 10 %/9999 e 5 %/50) |
| M-R12.3 | os dois tipos caem no mesmo ramo | CT-33 (linhas `fixo`) |
| M-R12.4 | o desconto é devolvido no lugar do total a cobrar | CT-33 (toda linha) |
| M-R12.5 | valor negativo quando o desconto excede o total | **CT-34** |
| M-R12.6 | `valor` é lido como reais e não como centavos no ramo fixo | CT-33 (linha `fixo / 1000 / 12990`) |

---

## Regra R13 — Cada aplicação bem-sucedida consome exatamente um uso, e só do cupom aplicado

> `RQ-13` · área **A2**, perfil **completo** · técnica: **rastreio de efeito**, quatro direções, mais
> **registro-testemunha**. Consome o teto inteiro do perfil — é o custo declarado da técnica.

```gherkin
  Regra: aplicar um cupom com sucesso consome um, e apenas um, dos usos daquele cupom

    Esquema do Cenário: [CT-35] o uso é consumido nos dois tipos de cupom
      Dado um cupom "<codigo>" ativo, do tipo "<tipo>", com limite de 5 usos e 2 usos feitos
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então o contador de usos do cupom passa a ser 3

      Exemplos:
        | codigo | tipo        |
        | P5     | porcentagem |
        | F5     | fixo        |

    Cenário: [CT-48] a aplicação move o contador do cupom aplicado, e só dele
      Dado dois cupons ativos da mesma organização, "ALVO" e "TESTEMUNHA",
        ambos com limite de 5 usos e 0 usos feitos
      Quando o comprador aplica "ALVO" sobre um total de 10000 centavos
      Então "ALVO" fica com 1 uso, "TESTEMUNHA" continua com 0
      E existe exatamente 1 registro de uso, e ele aponta para "ALVO"

    Esquema do Cenário: [CT-36] o uso não é consumido em nenhuma das três recusas
      Dado um cupom com 2 usos feitos, na situação "<situacao>"
      Quando o comprador apresenta o código correspondente a "<apresentado>"
      Então o resultado é recusado e o contador de usos do cupom continua em 2

      Exemplos:
        | situacao  | apresentado              | # a recusa de qual RQ |
        | ativo     | um código que não existe | RQ-09                 |
        | expirado  | o código do cupom        | RQ-10                 |
        | esgotado  | o código do cupom        | RQ-11                 |

    Cenário: [CT-37] uma aplicação consome um uso, não dois
      Dado um cupom "PROMO10" ativo, com limite de 5 usos e 0 usos feitos
      Quando o comprador aplica o cupom uma única vez
      Então o contador de usos do cupom passa a ser exatamente 1

    Cenário: [CT-38] o uso não fica consumido quando o registro de auditoria falha
      Dado um cupom "PROMO10" ativo, com limite de 5 usos, 1 uso feito
        e a linha de trilha correspondente
      E que a gravação do registro de quem aplicou vai falhar
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então a aplicação falha, o contador de usos continua em 1
        e continua existindo exatamente 1 registro de uso
```

> **CT-48 fecha [I-2 e B-06](#achados-da-revisão), e é a lacuna mais silenciosa que a revisão
> encontrou.** O conjunto v1 aplicava a regra do não-colapso a **personas** ("três pessoas
> distintas") e nunca ao **registro de controle**: em nenhum cenário de aplicação bem-sucedida
> existia um segundo cupom cujo contador fosse afirmado inalterado. Uma implementação com
> `Cupom::query()->increment('usos')` sem `whereKey($this->id)` — ou um
> `CupomUso::create(['cupom_id' => Cupom::first()->id, …])` — movia **todos** os cupons e ficava
> verde no conjunto inteiro. CT-11, CT-12 e CT-14 têm dois cupons mas nunca aplicam; CT-25 tem dois
> e a aplicação é **recusada**, então nenhum incremento ocorre em implementação nenhuma e a linha não
> discrimina nada.
>
> **CT-38 é atomicidade de verdade**, não o falso ✅ clássico: a falha é injetada **depois** do ponto
> em que o efeito acontece, não numa pré-validação onde nada seria gravado de qualquer forma.
> **Arnês, confirmado antes de a lacuna ser considerada**: `config/database.php:40` deixa
> `foreign_key_constraints` em `true` e o `phpunit.xml` não sobrescreve `DB_FOREIGN_KEYS`, então
> apontar o autor da aplicação para um usuário inexistente faz a chave estrangeira falhar de verdade
> no SQLite de teste. Alternativa: um ouvinte no evento `creating` do registro de uso que lança.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R13.1 | o incremento some (chamada removida) | CT-35 |
| M-R13.2 | o incremento acontece antes da validação | CT-36 |
| M-R13.3 | o incremento acontece duas vezes (observer + chamada explícita) | **CT-37** |
| M-R13.4 | o incremento salta 2 ou usa `+= 2` | CT-37 |
| M-R13.5 | o incremento fica fora da transação da trilha | **CT-38** |
| M-R13.6 | o incremento existe no ramo percentual e não no de valor fixo | CT-35 (linha `F5`) |
| M-R13.7 | o `UPDATE` não filtra por chave e move o contador de todos os cupons | **CT-48** |
| M-R13.8 | o registro de uso aponta para o cupom errado (o primeiro da tabela) | **CT-48** (última cláusula) |

---

## Regra R14 — Cada aplicação bem-sucedida deixa um registro auditável, que sobrevive ao cupom

> `RQ-15` · área **A6**, perfil **completo** (elevado na v2) · técnica: **rastreio de efeito**, quatro
> direções, mais **ciclo de vida da entidade de efeito colateral**

```gherkin
  Regra: toda aplicação de cupom deixa registrado quem a fez e quando, e o registro dura

    Esquema do Cenário: [CT-39] o registro é criado, com quem e quando, nos dois tipos
      Dado um cupom "<codigo>" ativo, do tipo "<tipo>", com 0 usos
      E que o instante corrente é 30/09/2026 14:35:12
      Quando a compradora Beatriz aplica o cupom sobre um total de 10000 centavos
      Então existe exatamente 1 registro de uso desse cupom, com Beatriz como autora
        e com 30/09/2026 14:35:12 como instante

      Exemplos:
        | codigo | tipo        |
        | P5     | porcentagem |
        | F5     | fixo        |

    Esquema do Cenário: [CT-40] o registro guarda sobre quanto o desconto incidiu
      Dado um cupom ativo do tipo "<tipo>" com valor <valor> e 0 usos
      Quando a compradora Beatriz aplica o cupom sobre um total de <total> centavos
      Então o registro de uso guarda <total> de valor original e <desconto> de desconto

      Exemplos:
        | tipo        | valor | total | desconto | # o que a linha revela               |
        | porcentagem | 29    | 10000 | 2900     | o registro guarda o valor calculado  |
        | fixo        | 1000  | 12990 | 1000     | o ramo de valor fixo também registra |

    Esquema do Cenário: [CT-41] nenhuma recusa deixa registro
      Dado um cupom com 0 usos, na situação "<situacao>"
      Quando o comprador apresenta o código correspondente a "<apresentado>"
        sobre um total de 10000 centavos
      Então o resultado é recusado e não existe nenhum registro de uso

      Exemplos:
        | situacao  | apresentado              | # a recusa de qual RQ |
        | ativo     | um código que não existe | RQ-09                 |
        | expirado  | o código do cupom        | RQ-10                 |
        | esgotado  | o código do cupom        | RQ-11                 |

    Cenário: [CT-42] uma aplicação sem autor identificado ainda é registrada   @premissa
      Dado um cupom "PROMO10" ativo, com 0 usos
      Quando o cupom é aplicado por uma rotina do sistema, sem usuário identificado
      Então existe exatamente 1 registro de uso desse cupom, com o instante da aplicação
        e sem autor

    Cenário: [CT-47] a trilha sobrevive à exclusão do cupom      @premissa
      Dado um cupom "PROMO10" ativo, com 2 aplicações já registradas
      Quando a administradora exclui esse cupom pela tela
      Então o cupom deixa de existir
      E os 2 registros de uso continuam consultáveis, com o autor e o instante de cada um

    Cenário: [CT-43] a recusa deixa rastro operacional      (convenção do projeto, não do card)
      Dado um cupom "VENC" com a validade vencida
      Quando o comprador apresenta o código "VENC"
      Então o canal de log da feature recebe um registro de nível informativo
        no formato "[Classe@metodo] mensagem", com o código e o motivo no contexto
```

> **CT-47 fecha [I-1, B-05 e B-17](#achados-da-revisão), e é o achado mais caro da revisão.**
> `cupom_usos.cupom_id` com `constrained()->cascadeOnDelete()` é o default mental de quem cria tabela
> filha — e excluir um cupom com 40 aplicações apaga as 40 linhas de auditoria. RQ-15 pede o registro
> *"pra gente conseguir auditar **depois**"*, e a trilha que morre com o registro-pai torna a cláusula
> decorativa: some exatamente o que alguém iria auditar. O conjunto v1 não tinha **nenhum** cenário
> que excluísse um cupom **com trilha** — pior, a fixture especificada criava `usos` sem criar linhas,
> de modo que CT-45 excluía cupons sem trilha nenhuma. É `@premissa` **P-I**: o card não decide a
> política de retenção, e a decisão precisa estar escrita porque é de retenção, não de chave
> estrangeira.
>
> **CT-41 virou `Esquema` na v2** ([B-13](#achados-da-revisão)): o título dizia "nenhuma recusa deixa
> registro" e o corpo testava **uma** recusa. Uma implementação que grava trilha na recusa por limite
> ou por código inexistente passava. CT-36 cobria as três recusas, mas só para o **contador**.
>
> **`exatamente 1` em CT-39 e CT-42** fecha [B-12](#achados-da-revisão): a v1 dizia "existe um
> registro", e o mutante irmão de M-R13.3 — trilha duplicada por observer + `create` explícito, com o
> contador incrementado uma vez só — ficava sem matador.
>
> **CT-43 é declaradamente derivado da convenção do projeto, não do requisito.** Está em
> [`## Fronteira com o Plano`](#fronteira-com-o-plano) para que ninguém o leia como cobertura de
> RQ-15: quem cobre RQ-15 é CT-39 a CT-42 e CT-47. O arnês é `espiarCanal('cupom')`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R14.1 | o registro sai pela trilha de auditoria genérica e nasce vazio, porque o consumo não dispara evento de model | **CT-39** |
| M-R14.2 | o autor é gravado como o dono do cupom, não como quem aplicou | CT-39 (três pessoas distintas no setup) |
| M-R14.3 | o instante gravado é o do cadastro do cupom, não o da aplicação | CT-39 (instante congelado) |
| M-R14.4 | a recusa também registra | **CT-41** (as três linhas) |
| M-R14.5 | o registro só é criado quando há usuário autenticado | **CT-42** |
| M-R14.6 | o registro guarda o valor do cupom em vez do desconto calculado | CT-40 (linha 29 %) |
| M-R14.7 | a trilha é apagada junto com o cupom (`cascadeOnDelete`) | **CT-47** — na v1 este mutante **não existia** |
| M-R14.8 | o registro é criado duas vezes por aplicação | **CT-39** (`exatamente 1`) e CT-48 |
| M-R14.9 | o campo `usos` fica fora da trilha de auditoria genérica e ninguém percebe | ⚠️ **sem matador — lacuna L-07**. É afirmação sobre o mecanismo descartado, não sobre o comportamento pedido. Registrada porque a premissa P-08 do `00` depende dela |

---

## Regra R15 — O cadastro é operável pela tela, e só os campos do formulário chegam ao banco

> `RQ-01`, `RQ-13` · área **A5**, perfil **padrão** · técnica: **gate de tela de escrita** +
> mass assignment

```gherkin
  Regra: o cadastro de cupons é operado por uma tela do painel de negócio

    Cenário: [CT-44] a listagem abre e mostra os cupons cadastrados
      Dado três cupons ativos cadastrados na organização
      Quando a administradora abre a listagem de cupons do painel de negócio
      Então a tela responde com sucesso e os três cupons aparecem na tabela

    Esquema do Cenário: [CT-45] excluir pela tela remove o cupom
      Dado um cupom "PROMO10" no estado "<estado>", com as linhas de trilha
            correspondentes aos usos que ele tem
      Quando a administradora exclui esse cupom pela ação da tabela
      Então o resultado é "<resultado>" e o cupom "<situacao_final>"

      Exemplos:
        | estado              | resultado | situacao_final         | # célula     |
        | Ativo               | aceito    | deixa de existir       | E1 × excluir |
        | Expirado            | aceito    | deixa de existir       | E2 × excluir |
        | Esgotado            | aceito    | deixa de existir       | E3 × excluir |
        | Expirado e esgotado | aceito    | deixa de existir       | E4 × excluir |
        | já excluído         | recusado  | continua não existindo | E5 × excluir |

    Cenário: [CT-46] campos fora do formulário não chegam ao cadastro
      Dado uma organização sem cupons cadastrados
      Quando a administradora cadastra um cupom "PROMO10" e o envio carrega também
             um contador de usos igual a 99 e uma organização diferente da corrente
      Então o cupom é criado com 0 usos e na organização corrente
```

> **CT-01, CT-09 e CT-49 são a metade "grava" do gate de tela de escrita** (rotas `create` e `edit`
> da `## Superfície de UI`); CT-44 e CT-57 são a metade "abre". *Uma tela aberta não é uma tela que
> grava* — `.ai/rules/testes.md` registra o caso medido em que `GET /admin/users` seguiu verde com o
> salvamento quebrado por um `Select::make('roles')`.
>
> **As linhas `Esgotado` e `Expirado e esgotado` de CT-45 só matam M-R15.3 com a fixture corrigida**:
> na v1 elas excluíam cupons cujo contador havia subido por `forceFill()` **sem nenhuma linha em
> `cupom_usos`** — não existia chave estrangeira a violar, e o mutante sobrevivia. O `Dado` agora
> exige as linhas de trilha.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-R15.1 | `usos` entra no `$fillable` e é gravável pelo formulário | **CT-46** |
| M-R15.2 | a organização vem do payload em vez do contexto | CT-46 (segunda cláusula) |
| M-R15.3 | a exclusão é bloqueada pela chave estrangeira da trilha | CT-45 (linhas Esgotado e E4, **com trilha real**) |
| M-R15.4 | a listagem abre mas não traz registro nenhum | CT-44 |
| M-R15.5 | excluir duas vezes derruba a tela com erro de sistema | CT-45 (linha `já excluído`) |

---

## Lacunas Declaradas

| # | O que fica sem cenário | O que foi tentado | Bloqueado por |
|---|---|---|---|
| **L-02** | o mecanismo descartado de exclusão **lógica**, em que o código continuaria ocupado após excluir | escrever CT-15 no mecanismo assumido (exclusão física) e registrar o outro; a **durabilidade** da trilha, que a v1 também havia absorvido nesta lacuna, virou **CT-47** | premissa de mecanismo do PRD |
| **L-03** | o mecanismo descartado de coluna booleana `ativo`, e a divergência entre ela e as duas colunas de origem | escrever CT-23 no mecanismo assumido; a divergência só é observável se as três fontes existirem | premissa **P-03** do `00` |
| **L-04** | **idempotência** ancorada no agregado que sofre o efeito, e a corrida real no nível do banco | o agregado (`Pedido`) está fora de escopo por P-01: o oráculo *"o total do pedido é o mesmo depois da segunda aplicação"* é **inexpressável**, e ancorá-lo no contador provaria contabilidade, não idempotência. Para a corrida: `pcntl` indisponível, `--parallel` isola por worker e `sqlite :memory:` é por processo; a janela check-then-act **foi** reproduzida em CT-31 | premissa **P-01** do `00` → pergunta ao usuário |
| **L-05** | limite de comprimento e alfabeto do código (40 chars, acento, emoji de 4 bytes) | derivar do card — ele não dá comprimento nem alfabeto. A normalização, que **é** derivável, está coberta em CT-50 e CT-24 | requisito silencioso |
| **L-07** | a trilha de auditoria genérica não alcançar o contador de usos | é afirmação sobre o mecanismo descartado, não sobre o comportamento pedido | premissa **P-08** do `00` |

> **L-01 e L-06 da v1 deixaram de ser lacunas** e viraram **CT-55** e **CT-54**. As duas haviam sido
> recusadas com argumentos que a revisão adversarial mostrou serem inconsistentes com o resto do
> conjunto — L-01 porque testaria a premissa P-A, que CT-06/CT-07 já testam; L-06 porque testaria o
> PRD, quando o *"apenas listar"* de RQ-08 é literal do card. Fechar uma lacuna sem discriminar é
> piorar; **ambas discriminam**, e a nota de cada uma diz por quê.

**Nenhuma lacuna foi convertida em item ✅ do checklist.** Uma lacuna declarada é dívida que alguém
conhece; um ✅ com o defeito dentro é dívida que ninguém volta a olhar.

---

## Checklist de Taxonomia

> Resposta válida: um ID de cenário, `não se aplica: {motivo}` ou `lacuna declarada: {o que foi
> tentado}`. **Nunca "sim".**

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal (acesso ao recurso de outro **pelo identificador**) | **CT-53** — na v1 este item apontava CT-25 e CT-14, e era **falso ✅**: nenhum dos dois acessa registro alheio por identificador |
| Autorização **exercida na ação**, não só consultada por `can()` | **CT-17, CT-18, CT-19** — os três verbos, por fora do componente de UI |
| Idempotência ancorada no agregado afetado | **lacuna declarada L-04** — o agregado está fora de escopo (P-01) |
| Concorrência sobre contador | **CT-31**; a corrida no nível do banco é parte da L-04 |
| Fronteira **no ponto de entrada** (gravação), não só no uso | **CT-06, CT-07, CT-51** (criação, pela tela) · **CT-55** (criação, fora da tela) · **CT-49, CT-52** (edição) · CT-02 (obrigatoriedade) |
| Domínio condicionado (tipo × valor) | **CT-06 + CT-07** — o par, não um deles |
| Estado × operação de **escrita**: o registro removido ainda funciona? | **CT-26** (aplicar), **CT-10** (abrir/editar), **CT-45 linha `já excluído`** (excluir) |
| **Ciclo de vida da entidade de efeito colateral** | **CT-47** — a trilha sobrevive ao cupom |
| **Registro-testemunha** (o efeito não vaza para o vizinho) | **CT-48** |
| Ausente ≠ `null` ≠ vazio | **CT-24** (linhas `(vazio)`/`(ausente)`), **CT-02**, **CT-42** (autor ausente) |
| Paginação | `não se aplica: o card não normatiza volume nem paginação; o oráculo de RQ-08 é o conjunto entregue (CT-22, CT-54), não a página` |
| Ordenação (coluna inexistente, nullable, empate) | `não se aplica: o card não determina ordem; ordenar é escolha do PRD` |
| Timezone / DST / `date` × `datetime` | **CT-29** (fuso, nascido de divergência verificada) e **CT-22 linha `HOJE0800`** (`date` × `datetime` entre dois leitores). DST: `não se aplica: America/Sao_Paulo não observa horário de verão desde 2019` |
| Virada de meia-noite / janela entre validar e consumir | **CT-28** |
| Unicode / limite de `varchar` | **lacuna declarada L-05** |
| **Normalização: a forma persistida**, não só a colisão | **CT-50** — na v1 este item não existia e M-R5.2 era falso ✅ |
| Unicidade + exclusão (recriar com o mesmo código) | **CT-15** |
| CRUD combinado: excluir duas vezes; editar sem alterar nada; agir sobre ID inexistente | **CT-45** (linha `já excluído`), **CT-08**, **CT-10** |
| Mass assignment | **CT-46** |
| Precisão monetária (inteiro em centavos, nunca `float`) | **CT-33 linha `29 % de 10000`** — a única que separa as duas representações |
| Efeito colateral entregue pelo canal certo | **CT-39** (o registro durável) e **CT-43** (o canal de log, declarado como convenção) |
| **Escopo de tenant no chamador que não é o painel** | **CT-56** |
| Upload | `não se aplica: a feature não recebe arquivo` |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|---|---|---|---|---|---|---|
| CT-01 | cadastro completo, nos dois tipos | R1 | EP | Livewire | `tests/Kit/CupomPainelTest.php` | M-R1.3, M-R1.5 |
| CT-02 | cada atributo ausente, isolado | R1 | EP | Livewire | `tests/Kit/CupomPainelTest.php` | M-R1.2, M-R1.4 |
| CT-03 | obrigatoriedade fora do formulário | R1 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R1.1 |
| CT-04 | terceiro tipo recusado no cadastro | R2 | EP exaustiva | Livewire | `tests/Kit/CupomPainelTest.php` | M-R2.2 |
| CT-05 | terceiro tipo recusado fora da tela | R2 | EP exaustiva | Kit | `tests/Kit/CupomTest.php` | M-R2.1, M-R2.3 |
| CT-06 | fronteira do valor percentual (1, 100) | R3 | BVA | Livewire | `tests/Kit/CupomPainelTest.php` | M-R3.2…M-R3.4, M-R3.6 |
| CT-07 | valor fixo tem piso e não tem teto | R3 | tabela de decisão | Livewire | `tests/Kit/CupomPainelTest.php` | M-R3.1, M-R3.6 |
| CT-08 | salvar sem alterar nada | R4 | unicidade contra si | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.1, M-R4.2 |
| CT-09 | alterar tipo e valor em cupom já usado | R4 | matriz estado × operação | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.3, M-R4.4 |
| CT-10 | cupom excluído não é aberto nem editado | R4 | matriz estado × operação | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.5 |
| CT-11 | segundo cupom com o mesmo código | R5 | normalização (colisão) | Livewire | `tests/Kit/CupomPainelTest.php` | M-R5.1, M-R5.3, M-R5.6 |
| CT-12 | editar o código para o de outro | R5 | normalização | Livewire | `tests/Kit/CupomPainelTest.php` | M-R5.1 |
| CT-13 | unicidade fora do formulário | R5 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R5.5 |
| CT-14 | duas organizações, o mesmo código | R5 | escopo | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M-R5.4, M-R7.3 |
| CT-15 | recriar o código após a exclusão | R5 | unicidade + exclusão | Kit | `tests/Kit/CupomTest.php` | — (célula E5 × criar) |
| CT-16 | matriz de escrita (6 papéis × 4 verbos) | R6 | matriz papel × ação | Livewire + Tenancy | `tests/Kit/CupomPainelTest.php` + `tests/Tenancy/CupomTenancyTest.php` | M-R6.1, M-R6.2, M-R6.5…M-R6.7 |
| CT-17 | usuário comum não cria fora da tela | R6 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R6.3 |
| CT-18 | usuário comum não edita fora da tela | R6 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R6.3 |
| CT-19 | usuário comum não exclui fora da tela | R6 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R6.4 |
| CT-20 | single-tenant: quem cria é o master_global | R6 | matriz papel × ação | Kit | `tests/Kit/CupomTest.php` | M-R6.2 |
| CT-21 | matriz de leitura | R7 | matriz papel × ação | Livewire + Tenancy | `tests/Kit/CupomPainelTest.php` + `tests/Tenancy/CupomTenancyTest.php` | M-R7.1, M-R7.2 |
| CT-22 | situações derivadas por persona, com bordas | R8 | partição exaustiva + BVA | Livewire | `tests/Kit/CupomPainelTest.php` | M-R8.1…M-R8.4, M-R8.6, M-R8.8 |
| CT-23 | sai da lista ao esgotar, sem edição | R8 | premissa de mecanismo | Livewire | `tests/Kit/CupomPainelTest.php` | M-R8.5 |
| CT-24 | igualdade normalizada do código | R9 | EP + normalização | Kit | `tests/Kit/CupomTest.php` | M-R9.1…M-R9.4 |
| CT-25 | código de outra organização, no painel | R9 | escopo | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M-R9.5 |
| CT-26 | código de cupom excluído | R9 | estado × operação | Kit | `tests/Kit/CupomTest.php` | M-R9.6 |
| CT-27 | fronteira da validade (−1 s, 0, +1 s) | R10 | BVA `datetime` | Kit | `tests/Kit/CupomTest.php` | M-R10.1, M-R10.2, M-R10.5, M-R10.6 |
| CT-28 | validade que vira entre validar e consumir | R10 | BVA temporal | Kit | `tests/Kit/CupomTest.php` | M-R10.3 |
| CT-29 | a validade no fuso em que foi digitada | R10 | parâmetro livre = fuso | Livewire | `tests/Kit/CupomPainelTest.php` | M-R10.4 |
| CT-30 | fronteira do limite, nos dois tipos | R11 | BVA contador | Kit | `tests/Kit/CupomTest.php` | M-R11.1, M-R11.2, M-R11.4…M-R11.7 |
| CT-31 | duas leituras, um uso disponível | R11 | concorrência | Kit | `tests/Kit/CupomTest.php` | M-R11.3 |
| CT-32 | expirado e esgotado ao mesmo tempo | R11 | célula E4 × aplicar | Kit | `tests/Kit/CupomTest.php` | M-R8.3 |
| CT-33 | o desconto calculado, por tipo e valor | R12 | tabela de decisão + BVA | Kit | `tests/Kit/CupomTest.php` | M-R12.1…M-R12.4, M-R12.6 |
| CT-34 | desconto maior que o total | R12 | BVA | Kit | `tests/Kit/CupomTest.php` | M-R12.5 |
| CT-35 | o uso é consumido, nos dois tipos | R13 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R13.1, M-R13.6 |
| CT-36 | nenhuma recusa consome uso | R13 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R13.2 |
| CT-37 | uma aplicação, um uso | R13 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R13.3, M-R13.4 |
| CT-38 | atomicidade: falha depois do efeito | R13 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R13.5 |
| CT-39 | registro com quem e quando, nos dois tipos | R14 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R14.1…M-R14.3, M-R14.8 |
| CT-40 | o registro guarda original e desconto | R14 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R14.6 |
| CT-41 | nenhuma das três recusas deixa registro | R14 | rastreio de efeito | Kit | `tests/Kit/CupomTest.php` | M-R14.4 |
| CT-42 | aplicação sem autor identificado | R14 | ausente ≠ null | Kit | `tests/Kit/CupomTest.php` | M-R14.5 |
| CT-43 | rastro operacional da recusa | R14 | convenção do projeto | Kit | `tests/Kit/CupomTest.php` | — (convenção) |
| CT-44 | a listagem abre e traz os cupons | R15 | gate de tela | Livewire | `tests/Kit/CupomPainelTest.php` | M-R15.4 |
| CT-45 | excluir pela tela, nos cinco estados | R15 | matriz estado × operação | Livewire | `tests/Kit/CupomPainelTest.php` | M-R15.3, M-R15.5 |
| CT-46 | campos fora do formulário são ignorados | R15 | mass assignment | Livewire | `tests/Kit/CupomPainelTest.php` | M-R15.1, M-R15.2 |
| **CT-47** | **a trilha sobrevive à exclusão do cupom** | R14 | ciclo de vida do efeito | Livewire | `tests/Kit/CupomPainelTest.php` | M-R14.7 |
| **CT-48** | **o cupom-testemunha não se move** | R13 | registro-testemunha | Kit | `tests/Kit/CupomTest.php` | M-R13.7, M-R13.8 |
| **CT-49** | **a fronteira do valor vale na edição** | R4 | BVA no 2º ponto | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.6 |
| **CT-50** | **o código gravado na forma canônica** | R5 | normalização (persistência) | Livewire | `tests/Kit/CupomPainelTest.php` | M-R5.2, M-R5.7 |
| **CT-51** | **a fronteira do limite de usos** | R3 | BVA | Livewire | `tests/Kit/CupomPainelTest.php` | M-R3.3, M-R3.4, M-R3.7 |
| **CT-52** | **reduzir o limite abaixo dos usos** | R4 | validação cruzada | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.7, M-R11.6 |
| **CT-53** | **IDOR entre organizações, por identificador** | R6 | papel × dono do registro | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M-R6.8, M-R7.3 |
| **CT-54** | **nenhuma via entrega o não-ativo ao comum** | R8 | o "apenas" de RQ-08 | Livewire | `tests/Kit/CupomPainelTest.php` | M-R8.7 |
| **CT-55** | **as fronteiras valem fora do formulário** | R3 | gate de camada | Kit | `tests/Kit/CupomTest.php` | M-R3.5 |
| **CT-56** | **aplicação fora do painel não atravessa organizações** | R9 | escopo no chamador real | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M-R9.7 |
| **CT-57** | **o formulário de edição carrega os valores gravados** | R4 | matriz estado × operação | Livewire | `tests/Kit/CupomPainelTest.php` | M-R4.8 |
| **CT-B01** | o campo de valor muda de unidade com o tipo | R3 | só o navegador prova | **Browser** | `tests/Browser/CupomTest.php` | ver `05` |

**Ordem obrigatória de implementação**: **CT-31 antes de qualquer CT-B.** Se a barreira de
concorrência não estiver de pé, todo cenário de tela mede outra coisa.

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| "o cupom é gravado com os dois tipos" como cenário próprio de R2 | é a tabela de `Exemplos` de CT-01 |
| "o desconto é subtraído do total" isolado | é toda linha de CT-33; um cenário genérico não discrimina |
| paginação da listagem com 0, 1, N e N+1 cupons | o card não normatiza volume; seria teste do padrão do Filament |
| ordenação por código e por validade | idem — escolha do PRD (`defaultSort`) |
| "o badge mostra Ativo / Expirado / Esgotado" | o card nunca nomeia esses rótulos; virou a pergunta **P-D** |
| cenário afirmando que **qualquer** papel consegue aplicar cupom | **cortado por ser oráculo invertido**: fixaria a ausência de barreira como comportamento esperado. Vira a pergunta **P-E** e a limitação declarada da matriz papel × ação |
| CT-B de criação atravessando listagem → formulário → volta | ver `05` |
| CT-B do modal de confirmação da exclusão | é CT-45, por componente |
| CT-B de acessibilidade das três telas | é auditoria de painel, e o kit já tem a wiki `regressao-de-telas` |
| teste de log em cada ponto do PRD | log não é oráculo de requisito; **um** cenário de convenção (CT-43) satisfaz o checklist da `feature-wiki` |
| cenário afirmando `RuntimeException` como classe da recusa | classe de exceção é escolha de implementação |

---

## Revisão Adversarial

Executada por sub-agente independente, que **não** derivou os cenários e recebeu apenas
`00-requisito.md` + a versão 1 deste `04` — sem o PRD, sem o código e sem o raciocínio de quem
derivou. Contrato: *provar que o conjunto deixa passar defeito*; proibido elogiar ou reescrever.

**Resultado: 5 implementações erradas plausíveis que passavam pelo conjunto inteiro, 18 lacunas
numeradas, 6 achados sobre as matrizes e 4 falsos ✅ no checklist.** Uma rodada; a segunda não foi
executada porque o teto são 2 rodadas e a primeira já foi fechada integralmente — **regra: re-revisar
só se o fechamento criar superfície nova**, e criou (11 cenários novos). **Registrado como dívida:
uma segunda rodada sobre a v2 é devida antes de a feature ir para implementação.**

### Achados da revisão

| # | Achado | Técnica que faltava | O que virou |
|---|---|---|---|
| **I-1 / B-05 / B-17** | `cascadeOnDelete` apaga a trilha junto com o cupom — RQ-15 vira decorativa | ciclo de vida da **entidade de efeito colateral**; as 36 células eram todas de `Cupom` | **CT-47** + pergunta **P-I** + M-R14.7 + área A6 elevada a `completo` |
| **I-2 / B-06** | `increment()` sem filtro por chave move o contador de **todos** os cupons; nenhum cenário tinha um segundo cupom cujo contador fosse afirmado inalterado | não-colapso aplicado ao **registro**, e não só à persona | **CT-48** + M-R13.7, M-R13.8 |
| **I-3 / B-04** | listagem e aplicação são dois leitores da mesma regra derivada; a BVA existia só no leitor da aplicação | BVA replicada **em cada leitor** | 3 linhas novas em **CT-22** + M-R8.6 |
| **I-4 / B-07** | piso e teto vivendo só no caminho de criação; R4 declarava a técnica e não a executava | replicação **executada** de EP/BVA na edição | **CT-49** + M-R4.6 |
| **I-5 / B-08** | normalização destrutiva (`preg_replace`) — `BLACK-FRIDAY` colide com `BLACKFRIDAY` | normalização observada nas **duas** direções (colisão + forma persistida) | **CT-50** + M-R5.7; e M-R5.2 deixou de ser falso ✅ |
| **I-6 / B-09 / B-10** | `limite_de_usos` sem nenhuma fronteira; reduzir o limite abaixo dos usos sem cenário | BVA no **segundo** contador do card + validação cruzada | **CT-51**, **CT-52** + M-R3.7, M-R4.7 + pergunta **P-J** |
| **B-01** | `Então` de CT-06/CT-07 era `"aceito"`/`"recusado"` nu — passava com saturação e com gravar-e-depois-recusar | rastreio de efeito na fronteira | coluna `efeito` em CT-06, CT-07, CT-51 + M-R3.6 |
| **B-02** | CT-16 tinha `Quando` triplo e `Então` condicional; as linhas positivas não afirmavam nada | um `Quando` por cenário + efeito no ramo positivo | **CT-16 reescrito** (18 linhas) + M-R6.7 |
| **B-03** | CT-22 tinha duas personas num `Quando` | um `Quando` por cenário | **CT-22 reescrito** com `persona` como coluna |
| **B-11** | CT-27 e CT-30 não afirmavam o não-efeito **monetário** nas recusas | recusa tem duas metades | coluna `total` + M-R10.6, M-R11.7 |
| **B-12** | "existe um registro" não distingue de "existem dois" | contagem exata no rastreio de efeito | `exatamente 1` em CT-39/CT-42 + M-R14.8 |
| **B-13** | CT-41 dizia "nenhuma recusa" e testava uma | `Esquema` sobre as três recusas | **CT-41 virou Esquema** |
| **B-14** | a fixture subia `usos` por `forceFill()` **sem criar linhas de trilha** — CT-09 e CT-31 eram insatisfazíveis e seriam "consertados" por enfraquecimento | coerência entre contador e efeito na fixture | `## Setup Global` reescrito: `comUsos(n)` e `esgotado()` criam as linhas |
| **B-15** | IDOR era falso ✅ — nenhum cenário acessava registro alheio **por identificador** | papel × **dono do registro**, a terceira dimensão | **CT-53** + M-R6.8 |
| **B-16** | L-01 e L-06 eram lacunas que o arnês permitia escrever, recusadas com argumentos inconsistentes | — | **CT-55** e **CT-54** + M-R3.5, M-R8.7 |
| **B-18** | o "apenas" de "apenas listar" não tinha cenário; a matriz papel × ação não tinha a ação `abrir` | matriz cartesiana completa | **CT-54** + coluna `abrir` (matriz passou a 6 × 6) |
| **M-1** | a coluna `abrir` inteira apontava para um cenário de **outra** operação — 6 falsos ✅, e zero célula válida | célula só conta se a operação for executada | **CT-57** + ponteiros corrigidos |
| **M-2 / M-3** | `E6 × aplicar` apontava um cenário sem tabela de `Exemplos`; `E5 × listar` apontava uma transição não relacionada | idem | ponteiros corrigidos (achados também na auditoria própria) |
| **M-4** | o somatório declarado (14/17/5) não batia com as células (16/16/4) | conferência célula a célula | contagens refeitas e conferidas |
| **M-5** | 10 células de `admin`/`infra` provam inacessibilidade de painel, não autorização sobre a ação | — | **limitação declarada com ‡** na matriz, em vez de ✅ silencioso |
| **M-6** | a premissa "não há barreira no motor" não tinha cenário que a confirmasse | — | **declarado**, com o motivo de **não** escrever o cenário (seria oráculo invertido) + CT-42 como confirmação parcial |
| **Contagens** | o cabeçalho declarava 58 mutantes / 6 sem matador; a soma real era 80 / 3, e as lacunas eram 7 | — | recontado por `grep` nas próprias tabelas: **97 mutantes, 1 sem matador, 5 lacunas**. A primeira redação da v2 errou de novo (declarou 93 / 2) — registrado no `## Perfil de Derivação` |

**Rastreabilidade que a revisão mostrou ser só aparente, e o que fechou**: RQ-06 (só presença, sem
domínio) → CT-51, CT-52; RQ-15 (só criação, sem durabilidade) → CT-47; RQ-08 (o "apenas") → CT-54;
RQ-02 (só colisão, sem forma persistida) → CT-50.

---

## Fechamento do Ciclo (pós-implementação)

```bash
# 1. declarar o plugin, que hoje está em vendor/ só por herança da árvore do Pest 5
composer require pestphp/pest-plugin-mutate --dev

# 2. medir, escopado — mutar o projeto inteiro devolve ruído
XDEBUG_MODE=coverage vendor/bin/pest tests/Kit/CupomTest.php --mutate --path=app/Models/Cupom.php
```

> **O mutation score não responde pela omissão.** Ele só muta código que existe: se a fronteira de
> `limite_de_usos` nunca virar `if`, nenhum mutante nasce e o score não cai. Quem responde por
> omissão é a rastreabilidade `RQ` → regra → cenário deste arquivo e o gate de mutantes **de
> especificação** — que nascem do card, não do código. Foi exatamente essa a classe dos 6 achados
> mais caros da revisão adversarial: **comportamento ausente**, sem linha para mutar.

| Mutante sobreviveu | Lacuna | O que escrever |
|---|---|---|
| `>` → `>=` em `expira_em` | BVA faltando | cenário na borda exata |
| `<` → `<=` em `usos` | BVA faltando | cenário na borda exata |
| `intdiv` → divisão comum | oráculo fraco em CT-33 | linha com resto ≠ 0 |
| chamada de registro removida | efeito não verificado | cenário de rastreio de efeito |
| filtro por chave removido no `UPDATE` | registro-testemunha faltando | cenário com um segundo registro imóvel |
</content>
