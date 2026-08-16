# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> a feature ainda não existe. O PRD entrou só para paths, rotas, stack e a tabela
> `## Superfície de UI`.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| **A** — máquina de estados e alçada (transições, limite do diretor, ciclo de volta) | 3 | 3 | 9 | **completo** |
| **B** — autorização e identidade (quem decide, subtração do `panel_user`, isolamento por organização) | 3 | 3 | 9 | **completo** |
| **C** — notificação do próximo aprovador | 3 | 2 | 6 | padrão |
| **D** — exibição (situação atual e histórico de etapas) | 2 | 2 | 4 | padrão |
| **E** — CRUD de centro de custo | 1 | 2 | 2 | mínimo |

**Justificativa das pontuações**: A e B têm P=3 por regra com muitas condições (5 estados × 7
operações) somada a concorrência declarada como risco no `00`/PRD, e I=3 por dinheiro e
autorização — A-08 descreve uma escalada de privilégio silenciosa. C tem P=3 (integra com
spatie/teams e fila, resolvidos fora do request) e I=2 (o e-mail não sair é retrabalho manual,
não perda de dado). D é P=2/I=2: a tela mentir sobre a situação leva alguém a agir errado, mas o
dado permanece correto. E é código novo isolado; a parte perigosa do centro de custo (quem edita
`gestor_id`) está na área **B**, não aqui.

- Técnicas aplicadas: **EP**, **BVA 3-valores** (incremento `0,01`), **tabela de decisão**,
  **tabela estado × operação** (produto cartesiano fechado), **matriz papel × verbo**,
  **rastreio de efeito**, **2-switch** no ciclo de volta, **cardinalidade de destinatário**.
- **Regras: 16 · Cenários: 56 · CT-B: 2 · Mutantes previstos: 82 · Sem matador: 3 (lacunas declaradas)**
- Revisão adversarial: **obrigatória** (duas áreas em perfil `completo`) — **executada**, 17
  achados, todos fechados. Ledger completo em [`## Revisão Adversarial`](#revisão-adversarial).
  Onze cenários deste conjunto (CT-46…CT-56) nasceram dela, e a matriz passou de 35 para 42
  células por causa de um achado estrutural.

### Escalada de técnica acima do perfil da área

| Onde | Técnica usada | Por quê |
|---|---|---|
| R1 (área A) — casas decimais do valor | BVA com incremento de **milésimo**, não de centavo | é a única granularidade que distingue truncar de arredondar, e o arredondamento para cima cruza a alçada de R$ 5.000,00 sem o usuário saber |
| R15 (área E, `mínimo`) | 2 cenários em vez de 1 | o **gate de tela de escrita** cobra gravação por componente nas rotas `create` **e** `edit`, e são duas linhas da `## Superfície de UI` |

---

## Fatos do arnês — confirmados no código deste projeto

Nada aqui foi presumido de outro projeto. Cada linha tem o arquivo que a comprova.

| Fato | Onde foi confirmado | Consequência para os CT |
|---|---|---|
| Pest **5.1**, `pest-plugin-browser` **^5.0**, `pest-plugin-laravel` **^5.0**, PHPUnit ^13.3 | `composer.json:78-81` | vale `--tia`, `pest()->browser()`, `visit()` |
| Laravel **^13.17**, Filament **^5.6** | `composer.json:31,44` | helpers de teste da API 5.x (ver tabela de depreciados abaixo) |
| `pestphp/pest-plugin-mutate` está em `vendor/pestphp/` mas **não** em `composer.json` | `vendor/pestphp/pest-plugin-mutate` presente; ausente do `require-dev` | ⚠️ **dependência transitiva**: `pest --mutate` funciona por acidente da árvore e some num `composer update`. Devolvido ao PRD como passo (`composer require pestphp/pest-plugin-mutate --dev`) |
| `tests/Unit` **não** está ligado a nenhum `TestCase` da aplicação | `tests/Pest.php:22-104` liga só `Feature`, `Kit`, `Tenancy`, `Browser`, `BrowserTenancy` | **nenhum cenário foi alocado em `Unit`**: sem container não há `config()`, nem Eloquent, nem banco. A camada mais barata que este arnês sustenta é `Feature` |
| Suítes existentes | `phpunit.xml:7-41` — `Unit`, `Feature`, `Tenancy`, `Kit`, `Browser`(+`BrowserTenancy`) | **não existe `FeatureTenancy`**: os CT-36 e CT-37 dependem do passo 10 do PRD (pasta + testsuite + bloco no `tests/Pest.php`). Sem ele, **a pasta não é varrida e os dois passam por não existirem** |
| Ambiente de teste | `phpunit.xml:53-57` — `sqlite :memory:`, `MAIL_MAILER=array`, `QUEUE_CONNECTION=sync` | `Notification::fake()` intercepta mesmo com `ShouldQueue`; nenhum worker é necessário |
| `KIT_COMPRAS_LIMITE_DIRETOR` **não** é definida em `phpunit.xml` nem em `.env.testing` | `phpunit.xml:47-62` lido por inteiro | **CT-12 pode afirmar o valor de fábrica**: o cenário do valor literal do requisito não estará medindo o ambiente |
| Factories existentes: **só** `Convite`, `Tenant`, `User` | `database/factories/` | ⚠️ **não há factory para `CentroCusto`, `SolicitacaoCompra` nem `EtapaAprovacao`**. Ver `## Setup Global` — devolvido ao PRD |
| Helpers globais | `tests/Pest.php:185-353` — `tenant()`, `usuario()`, `usuarioCom()`, `usuarioDoKit()`, `usuarioComPapel()`, `papelNaOrganizacao()`, `noPainelDa()`, `fronteiraDeRequest()` | helper novo usado por mais de um arquivo **tem** de nascer em `tests/Pest.php` (`.ai/rules/testes.md`, enforçado por `tests/Kit/HelpersDeTesteTest.php`) |
| `TestCase::seed()` foi sobrescrito para usar `Artisan::call` | `tests/TestCase.php` (docblock de `seed()`) | usar **sempre** `$this->seed([...])` desta base. O `seed()` do Laravel grava **0 permissions** e a suíte roda sem matriz nenhuma |
| Papéis semeados: `master_global`, `admin`, `infra`, `admin_organizacao` (só multi-tenant), `panel_user` | `database/seeders/PapeisSeeder.php:53-93` | **não existe `diretor`** — é criado por esta feature (passo 7 do PRD) e é o que CT-32/CT-35 cobram |
| Padrão de teste de componente | `tests/Kit/PaginasInfraTest.php:86-104` — `Filament::setCurrentPanel()` + `actingAs()` + `Livewire::test(...)->fillForm()->call('save')` | herdado tal e qual |
| Padrão de CT-B | `tests/Browser/PerfisTest.php` — `actingAs()` + `visit()` + `assertPathIs` antes do conteúdo + `assertNoJavaScriptErrors()` | herdado tal e qual |

### Helpers do Filament 5 — o que escrever, e o que não

Confirmado por `grep -n "@deprecated" vendor/filament/*/.stubs.php`. Os antigos **continuam
existindo e não avisam nada** — o CT escrito com eles passa hoje e quebra no upgrade.

| Escrever | Em vez de (`@deprecated` no vendor) |
|---|---|
| `assertSchemaStateSet` | `assertFormSet` (`forms/.stubs.php:11`) |
| `callAction(TestAction::make('rejeitar')->table($registro), [...])` | `callTableAction` (`tables/.stubs.php:101-103`) |
| `assertActionExists` / `assertActionHidden` / `assertActionVisible` | `assertTableActionExists` (`:113-115`), `assertTableActionHidden` (`:134-136`) |
| `assertHasActionErrors([...])` | `assertHasTableActionErrors` |

**Não depreciados e usados aqui** (confirmados em `vendor/filament/tables/.stubs.php`):
`assertCanSeeTableRecords`, `assertCanNotSeeTableRecords`, `assertCountTableRecords`,
`assertTableColumnStateSet`, `assertTableColumnVisible`; e em `notifications/.stubs.php:8`:
`assertNotified`.

### Divergência entre esta skill e as rules do projeto

A `feature-test-design` sugere `pest --parallel --tia` como padrão. **A rule vence**:
`.ai/rules/testes-browser.md` mediu que `--parallel` derruba 4 de 11 cenários de browser e que,
sem **PCOV**, o `--tia` não termina (abortado após 35 min com Xdebug). Comandos desta feature:

```bash
vendor/bin/pest --parallel --group=kit     # a fundação não se moveu
vendor/bin/pest tests/Feature/Compras      # os CT de negócio
vendor/bin/pest --testsuite=Browser        # os CT-B, em série — nunca --parallel
```

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | 3 tabelas (`centros_custo`, `solicitacoes_compra`, `etapas_aprovacao_compra`), 1 enum de 5 estados, 3 models, 2 policies, 1 notification, 2 Resources no painel `/app`, **1 papel novo (`diretor`)**, 1 channel de log, 1 chave de config, 1 suíte de teste nova | CT-32, CT-35, CT-38, CT-39 |
| **F**unction | criar, editar, excluir, enviar, aprovar, rejeitar, cancelar, listar, visualizar; decidir a alçada; notificar. **Função administrativa escondida**: editar `centros_custo.gestor_id` é *nomear quem aprova* — quem pode fazê-lo aprova as próprias compras | CT-32, CT-33, CT-34 |
| **D**ata | `valor` decimal (domínio, borda de R$ 5.000,00, casas decimais); `descricao` e `justificativa` como texto livre (acento, emoji de 4 bytes, limite); `gestor_id` **nulo**; **dado de outra organização**; histórico append-only; cardinalidade **0/1/N** de diretores | CT-01…CT-05, CT-10, CT-12, CT-19, CT-31, CT-36 |
| **I**nterfaces | as telas do `/app` (Livewire+Alpine) e **os métodos do model chamados direto** — job, comando, seeder ou rota de API futura. **Não há rota HTTP de escrita própria**: em Filament toda escrita passa pelo componente, o que limita o gate de camada em R13 (ver a lacuna declarada lá). O e-mail é a terceira interface, de saída | CT-02, CT-08, CT-15, CT-16, CT-19, CT-28, CT-34 |
| **P**latform | sqlite `:memory:` no teste × MySQL/Postgres em produção: em sqlite `decimal` é `NUMERIC` e a precisão pode divergir — **mas a comparação com o limite acontece em PHP, não no banco**, então a divergência não muda a alçada; o que ela pode mudar é o **valor gravado** (CT-02). `permission.teams` só está ligado sob `TenancyTestCase`. Fila em `sync`. Navegador só nos 2 CT-B | CT-02, CT-36, CT-37 |
| **O**perations | três personas distintas **por desenho** (solicitante ≠ gestor ≠ diretor); duplo clique e duas abas; gestor removido do centro depois do cadastro; organização sem nenhum diretor; solicitação parada quando o aprovador some (declarado fora de escopo no `00`) | CT-11, CT-31, CT-32 |
| **T**ime | **não há prazo, SLA, expiração, agendamento nem DST nesta feature** — nenhuma decisão lê a data. O tempo entra por um único lugar: o carimbo das etapas, cuja **ordem** é metade de RQ-13. Duas etapas no mesmo segundo empatam. E a concorrência é temporal por natureza | CT-29, CT-32 |

Nenhuma dimensão ficou vazia.

---

## Mapa de Regras

| Regra | Área (perfil) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — a solicitação nasce em rascunho com descrição, valor e centro de custo | A (completo) | RQ-01 | EP + BVA na **gravação** + mass assignment | CT-01…CT-05, **CT-50**, **CT-54** |
| **R2** — em rascunho, só o solicitante edita e exclui | B (completo) | RQ-02, RQ-03 | matriz papel × verbo | CT-06…CT-09 |
| **R3** — o envio endereça a solicitação ao gestor do centro de custo, ou falha fechado | A (completo) | RQ-04 (A-10) | tabela de decisão + cardinalidade do destinatário | CT-10, CT-11, **CT-53** |
| **R4** — acima de R$ 5.000 a aprovação do diretor vem **depois** da do gestor | A (completo) | RQ-05 (A-04) | BVA 3-valores, incremento `0,01` | CT-12…CT-14 |
| **R5** — só quem decide a etapa corrente aprova ou rejeita | B (completo) | RQ-06 (A-07, A-09, A-03) | matriz papel × verbo, **verbo a verbo** + cardinalidade do decisor | CT-15…CT-18, **CT-49** |
| **R6** — rejeição sem justificativa é recusada | A (completo) | RQ-07 (A-07) | EP (vazia / só espaços / ausente no form / válida), **nas duas etapas** | CT-19, CT-20, **CT-48** |
| **R7** — a rejeição devolve ao rascunho preservando o histórico, e o reenvio recomeça pelo gestor | A (completo) | RQ-08, RQ-09 | estado × evento **2-switch** | CT-21…CT-23, **CT-47** |
| **R8** — `aprovada` é estado terminal | A (completo) | RQ-10 (A-05) | estado × operação (matriz única) | CT-44 |
| **R9** — o solicitante cancela enquanto a solicitação está em trânsito | A (completo) | RQ-11 (A-06) | estado × operação | CT-24, CT-45 |
| **R10** — a tela mostra a situação atual de cada solicitação | D (padrão) | RQ-12 (A-12) | **EP exaustiva do enum** (5 de 5) | CT-25, **CT-51** |
| **R11** — a tela mostra quem decidiu cada etapa, quando e por quê | D (padrão) | RQ-13 (A-12) | rastreio de efeito + ordenação com empate | CT-26, CT-27, **CT-52** |
| **R12** — só o próximo aprovador é notificado, e por e-mail | C (padrão) | RQ-14 (A-11) | rastreio de efeito (4 direções) + cardinalidade 0/1/N | CT-28…CT-31 |
| **R13** — centro de custo é entidade de administração: o usuário comum não escolhe quem aprova | B (completo) | RQ-04 (A-08) | matriz papel × ação | CT-32…CT-35 |
| **R14** — solicitação de uma organização não é vista nem operada de outra | B (completo) | **sem `RQ` de origem** — taxonomia (IDOR / dado de outro tenant) | IDOR | CT-36, CT-37, **CT-55** |
| **R15** — o centro de custo é cadastrado com nome e gestor | E (mínimo) | RQ-04 (A-01) | CRUD + unicidade contra o próprio registro | CT-38, CT-39 |
| **R16** — nenhuma operação fora do ciclo de vida altera a solicitação | A (completo) | RQ-02, RQ-03, RQ-05, RQ-06, RQ-10, RQ-11 | **matriz estado × operação**, produto cartesiano fechado | CT-40…CT-45, **CT-46**, **CT-56** |

**R14 não tem `RQ` de origem e isso é deliberado**: o isolamento por organização não está no card.
Ele entra pelo checklist de taxonomia da própria skill (IDOR / dado de outro tenant) e pela
premissa de mecanismo do PRD (`BelongsToTenant`). Está registrado assim para o
`feature-quality-gate` não procurar a cláusula que não existe.

### Cobertura `RQ` → Regra

| RQ | Regra(s) | Cenários | Metade da cláusula que estava sem oráculo antes da revisão |
|---|---|---|---|
| RQ-01 | R1 | CT-01…CT-05, **CT-50**, **CT-54** | *"com descrição, valor e centro de custo"* — nenhum cenário afirmava um campo **persistido** |
| RQ-02 | R2, R16 | CT-06…CT-09, CT-42…CT-46 | *"pode editar"* — só o rascunho **virgem** era editado |
| RQ-03 | R2, R16 | CT-08, CT-09, CT-40, CT-42…CT-45, CT-56 | — |
| RQ-04 | R3, R13, R15, R14 | CT-10, CT-11, **CT-53**, CT-32…CT-35, CT-38, CT-39, **CT-55** | *"o gestor do centro de custo"* — ninguém trocava o gestor nem o centro depois do envio |
| RQ-05 | R4, R16 | CT-12…CT-14, CT-41, **CT-49** | *"aprovação do diretor"* — só exercitada com **um** diretor |
| RQ-06 | R5, R16 | CT-15…CT-18, **CT-49**, CT-40…CT-45 | — |
| RQ-07 | R6 | CT-19, CT-20, **CT-48** | *"justificativa é obrigatória"* — falsificada só na etapa de **gestor** |
| RQ-08 | R7 | CT-21 | — |
| RQ-09 | R7 | CT-22, CT-23, **CT-47** | **"corrigir"** — o verbo não era executado por cenário nenhum |
| RQ-10 | R8, R16 | CT-44 | — |
| RQ-11 | R9, R16 | CT-24, CT-45 | — |
| RQ-12 | R10 | CT-25, **CT-51** | *"mostrar o status"* — 3 dos 5 rótulos nunca eram observados |
| RQ-13 | R11 | CT-26, CT-27, **CT-52**, CT-24 | *"quando"* — a data era afirmada como presença, nunca como valor |
| RQ-14 | R12 | CT-28…CT-31 | — |

Nenhuma `RQ` ficou sem regra. **A coluna da direita é o saldo da revisão adversarial**: sete das
catorze cláusulas estavam marcadas como cobertas por cenários que não as falsificavam por
inteiro — quase sempre porque **metade do verbo da cláusula não era executada**.

---

## Fronteira com o Plano

O que veio do `01-plano-acao.md` e foi **recusado como oráculo**, para o cenário não virar teste
do PRD.

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| `exigeDiretor()`, `podeSerDecididaPor()`, `exigirAprovador()`, `transicionar()` | nomes de método — escolha de implementação | detalhe do cenário; nenhum `Então` os cita |
| `config('kit.compras.limite_diretor')` | **onde** o número mora é escolha de implementação | o `Dado` de CT-12 afirma o **valor efetivo lido**; o `Então` usa **R$ 5.000,00**, o número literal do card |
| `UPDATE … WHERE situacao = <esperada>` (ADR-09) | mecanismo de atomicidade | CT-32 afirma o **observável** (uma etapa, uma notificação), não o `UPDATE` |
| `decimal(12,2)`, `varchar(255)` na descrição, `varchar(120)` no nome | mecanismo (schema) | cenários escritos **no mecanismo assumido**, marcados `@premissa-mecanismo`; o mecanismo descartado (centavos em `integer`, ADR-02) vira lacuna declarada abaixo |
| valores do enum `aguardando_gestor` / `aguardando_diretor` | o card nomeia só "rascunho" e "aprovada"; os outros três são **nomes do plano** | usados como rótulo de estado nos cenários, nunca como string afirmada; **pergunta P-07** |
| rótulo e cor do badge (`HasLabel` / `HasColor`) | comportamento visível ao usuário que **só o PRD** determina | **pergunta P-08**. CT-25 afirma o **estado da coluna** (`assertTableColumnStateSet`), não o texto |
| `scopedUnique(ignoreRecord: true)` no nome do centro | o requisito não pede unicidade de nome | CT-39 escrito de forma **neutra**: edita sem alterar o nome, e o oráculo é a gravação — vale exista ou não a regra de unicidade |
| mascaramento de e-mail no log e omissão da justificativa (regra LGPD do PRD) | comportamento que só o PRD determina | **recusado**; **pergunta P-09** |
| níveis de log por método (`info`/`warning`), channel `compras`, formato `[Classe@Método]` | escolha de implementação inteira | **nenhum CT de log neste conjunto** — ver a nota abaixo |
| `tests/FeatureTenancy` e a testsuite nova (passo 10) | infra de teste | usada como **onde** o CT roda, nunca como oráculo |

> **Por que não há CT de log.** O template do `feature-wiki` sugere CTs de log (channel, nível,
> formato, context). Nenhuma cláusula do `00-requisito.md` menciona log — nem o channel, nem o
> nível, nem o mascaramento. Um CT que afirma `Log::channel('compras')` estaria testando o PRD, e
> testar a interpretação confirma a interpretação. Se o log for requisito de auditoria (e a regra
> LGPD do PRD sugere que alguém o considera assim), ele precisa **estar no requisito** — é a
> **pergunta P-09**. Isto está registrado aqui para o `feature-quality-gate` ler a ausência como
> decisão, não como omissão.

### Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` é **imutável nesta execução** (fechado para edição
> por instrução do fluxo). A skill manda devolver as perguntas novas para `## Ambiguidades` do
> `00`; como não é possível, elas ficam aqui, **em bloco pronto para colagem**, no mesmo formato
> da seção de destino. Cada uma continua **bloqueando** o que depende dela.

```markdown
### A-13 — e se não houver NENHUM diretor na organização? (RQ-05)

O `00` cobre o gestor ausente (A-10) e não cobre o simétrico: a solicitação acima do limite
chega à etapa de diretor e não existe ninguém com o papel.

**Assumido**: **falha fechado** — a aprovação do gestor é **recusada**, a solicitação **fica em
`aguardando_gestor`** e ninguém é notificado. É a mesma direção que A-10 já fixou para o gestor,
e a coerência interna do requisito é o que decide: as duas alternativas repetem os erros que
A-10 recusou — pular a etapa aprovaria sem o segundo par de olhos que RQ-05 exige, e avançar
para `aguardando_diretor` deixaria a solicitação presa sem sinal.

**Invariante (vale em qualquer resposta)**: uma solicitação de valor acima do limite **nunca**
chega a `aprovada` sem uma etapa de diretor gravada.

**Se negado**: CT-31 (linha "0 diretores") inverte — o `Então` passa a "aceito, situação
aguardando diretor", e o invariante acima vira o único oráculo da linha.

### A-14 — quem, dentro da organização, pode LER uma solicitação alheia? (RQ-12, RQ-13)

O card manda "mostrar na tela" e não diz a quem. A-12 escolheu **quais** telas, não **quem**.

**Assumido**: qualquer pessoa com a permission do painel — o fluxo **exige** que terceiros em
relação ao solicitante (gestor, diretor) leiam antes de decidir, e distinguir "aprovador da vez"
de "leitor" seria inventar uma regra que o card não tem.

**Invariante (vale em qualquer resposta)**: **ler nunca autoriza agir** — quem abre a
solicitação sem ser o solicitante nem o aprovador da vez não recebe as ações Enviar, Aprovar,
Rejeitar e Cancelar, e chamá-las direto é recusado.

**Se negado**: CT-09 e CT-18 ganham uma linha de leitura recusada; o invariante não muda.

### A-15 — valor menor ou igual a zero, e valor com mais de duas casas decimais (RQ-01, RQ-05)

O card diz que a solicitação tem "valor" e não delimita o domínio.

**Assumido**: **recusa** nos dois casos, por falha fechado. Valor ≤ 0 cria uma solicitação de
compra que não compra nada e que o fluxo de alçada teria de saber tratar; e um valor de três
casas decimais só pode ser gravado arredondando ou truncando — as duas coisas mudam o número que
o usuário digitou, e **uma delas cruza a alçada** (R$ 4.999,995 → R$ 5.000,00, ou
R$ 5.000,005 → R$ 5.000,01).

**Invariante (vale em qualquer resposta)**: o valor **gravado** e o valor que **decide a alçada**
são o mesmo número — nenhuma solicitação atravessa uma etapa a mais ou a menos por causa de um
arredondamento que o usuário não viu.

**Se negado**: CT-01 (linhas `0,00` e `-0,01`) e CT-02 invertem o `Então`; o invariante fica.

### A-16 — a validação de domínio do valor vive no formulário ou no model? (RQ-01)

Não é ambiguidade do card: é uma lacuna do plano que só apareceu ao derivar. O PRD põe
`->required()->numeric()->minValue(0.01)` no `TextInput` (passo 9a) e **não** põe nada
equivalente no model — ao contrário do que fez com a justificativa da rejeição (passo 5.2), onde
a exigência foi deliberadamente duplicada no model com a justificativa escrita.

**Consequência medida na derivação**: **CT-02 nasce vermelho contra o plano como está.** Ele
grava pelo model, por fora do formulário, e uma regra que vive só no `->rules()` não o barra.

**Se confirmado que a validação deve viver só na tela**: CT-02 vira lacuna declarada e o
`00` ganha a cláusula que diz que o valor só é validado pela interface.

### A-17 — teto do valor (RQ-01)

`decimal(12,2)` é escolha do PRD (passo 2b). O card não tem teto. O comportamento acima do teto
do tipo (R$ 10.000.000.000,00) não está determinado por ninguém.

**Assumido**: **recusa**, por falha fechado — gravar um valor que o tipo não representa produz
truncamento silencioso no banco.

**Se negado**: a linha correspondente de CT-01 inverte.

### A-18 — os nomes dos estados intermediários (RQ-04, RQ-05)

`aguardando_gestor` e `aguardando_diretor` são invenção do PRD (ADR-01). O card nomeia só
"rascunho" e "aprovada". Os nomes aparecem na tela (RQ-12).

**Assumido**: os nomes do PRD. Nenhum cenário afirma a **string**; CT-25 afirma o **estado** da
coluna.

### A-19 — rótulo e cor do badge de situação (RQ-12)

Comportamento visível ao usuário determinado só pelo PRD (passo 3: `HasLabel`, `HasColor`).
Nenhum cenário o afirma. **Se o negócio tiver texto ou semáforo preferido, ele é requisito.**

### A-21 — o aprovador é o gestor ATUAL do centro, ou o do momento do envio? (RQ-04)

Descoberta ao derivar, não ao ler: RQ-04 diz "o gestor do centro de custo" no **presente**, e não
diz o que acontece quando esse gestor muda com a solicitação já em trânsito. Também não diz o que
acontece se a solicitação for movida para **outro centro** depois do envio.

**Assumido**: o aprovador é o gestor **atual**, lido no momento da decisão; e **a solicitação não
muda de centro depois do envio** (falha fechado — mover a solicitação escolhe o aprovador, e é a
escalada de A-08 por outra porta).

**Invariante (vale em qualquer resposta)**: **exatamente uma** pessoa decide a etapa de gestor, e
o histórico registra o nome de quem decidiu. Nenhuma troca de gestor ou de centro faz uma
solicitação ser aprovada por duas pessoas, nem por ninguém.

**Se negado** (o aprovador é congelado no envio): CT-53 troca as duas metades entre si. A recusa
de mudar de centro em trânsito (CT-46) **não** muda — ela não depende desta resposta.

### A-22 — a solicitação pode referenciar centro de custo de outra organização? (RQ-01, RQ-04)

O card não trata de organizações — o multi-tenant é do kit. Mas a combinação é perigosa: se o
recorte por organização viver só na consulta do `Select` do formulário, uma solicitação da Acme
pode nascer apontando para um centro da Globex, e o gestor da Globex passa a aprovar compra da
Acme por dentro de todas as barreiras.

**Assumido**: **recusa** (falha fechado). **Invariante**: nenhuma solicitação é decidida por quem
está fora da organização dela. **CT-55** cobre.

### A-20 — o log é requisito? (transversal)

O PRD dedica uma seção inteira ao channel `compras`, aos níveis por método e a uma regra LGPD
(e-mail mascarado, justificativa nunca em claro). Nada disso está no card.

**Assumido**: **não é requisito** — nenhum CT de log foi escrito. Se a trilha de decisão for
exigência de auditoria, ela precisa virar cláusula, e aí ganha rastreio de efeito próprio.
```

---

## Setup Global

### Personas — seis, e cada uma existe para quebrar uma colapsagem

A persona colapsada é o erro mais barato de cometer aqui: com solicitante = gestor = chamador na
mesma pessoa, **nenhuma barreira de identidade é exercitada** e todo cenário passa com a
autorização removida.

| Persona | Papel | Vínculo | Existe para |
|---|---|---|---|
| **Ana** | `panel_user` na Acme | solicitante | ser a dona do registro |
| **Rui** | `panel_user` na Acme | `centros_custo.gestor_id` do centro "TI" | ser gestor **sem papel de gestor** — se a implementação resolver o aprovador por papel em vez da FK, ele some |
| **Dora** | **`diretor`** na Acme | nenhum centro | ser aprovadora da segunda etapa e **destinatária real** de todo não-efeito de notificação |
| **Bruno** | `panel_user` na Acme | nenhum | ser o terceiro sem vínculo nenhum |
| **Carla** | `panel_user` na Acme | gestora do centro **"RH"** | distinguir *"é gestor de algum centro"* de *"é gestor **deste** centro"* |
| **Téo** | `panel_user` na **Globex** | — | o outro tenant (só `FeatureTenancy`, CT-36 e CT-37) |

Criadas com `User::create([...])` e nome explícito, como faz `tests/Kit/PaginasInfraTest.php:82-92`
— e **não** com `usuarioCom()`, que gera `name = 'Teste'` para todos: CT-26 afirma **o nome de
quem decidiu**, e seis "Teste" no histórico não distinguem nada.

Papéis: `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach`,
depois `->assignRole(...)`. Na suíte `FeatureTenancy`, `papelNaOrganizacao($user, $papel, $tenant)`
— papel gravado no contexto global fica invisível dentro do `/app`.

### Fixtures — **as factories não existem** (devolvido ao PRD)

`database/factories/` tem `ConviteFactory`, `TenantFactory` e `UserFactory`. Não há factory para
`CentroCusto`, `SolicitacaoCompra` nem `EtapaAprovacao`.

**Recomendação devolvida ao PRD** (passo novo, antes do passo 11): criar
`SolicitacaoCompraFactory` com um state por situação e `CentroCustoFactory`.

```php
SolicitacaoCompra::factory()->emRascunho()->create([...]);
SolicitacaoCompra::factory()->aguardandoGestor()->create([...]);
SolicitacaoCompra::factory()->aguardandoDiretor()->comEtapaDeGestor($rui)->create([...]);
SolicitacaoCompra::factory()->aprovada()->create([...]);
SolicitacaoCompra::factory()->cancelada()->create([...]);
```

Não é conveniência: **este conjunto tem 56 cenários e uma matriz de 42 células**, e montar cada
situação de partida à mão é a razão prática pela qual matriz de estado deixa de ser escrita. E o
state funciona apesar de `situacao` estar fora do `$fillable` (passo 5 do PRD) porque
`Factory::make()` roda dentro de `Model::unguarded()`.

Se o PRD recusar as factories, o Setup Global usa `SolicitacaoCompra::create([...])` seguido de
`->forceFill(['situacao' => …])->save()` — e o custo é 45 blocos de setup à mão.

### Fakes

| Fake | Onde | Armadilha evitada |
|---|---|---|
| `Notification::fake()` | todo cenário com efeito de e-mail | ⚠️ **`Mail::assertSent` não serve**: o efeito é uma `Notification`, não um `Mailable`. E como ela é `ShouldQueue`, `Mail::assertSent` **nunca** passaria — seria `assertQueued` |
| — | nunca `Event::fake()` **antes** das factories | eventos de model (`uuid` em `creating`, via `TemUuid`) não rodariam e a fixture nasceria sem uuid |
| — | nunca `Http::fake()` | não há chamada externa nesta feature |

O canal é afirmado explicitamente, sempre:

```php
Notification::assertSentTo(
    $rui,
    AprovacaoPendente::class,
    fn ($notification, array $channels): bool => in_array('mail', $channels, true),
);
```

`Notification::assertSentTo($rui, AprovacaoPendente::class)` **sozinho não discrimina**: passa com
a notificação saindo por `database`, e RQ-14 diz **"por e-mail"**.

### Estratégia de DB

`RefreshDatabase` global, aplicado por `tests/Pest.php` a cada suíte. sqlite `:memory:`
(`phpunit.xml:53-54`). Sem `DatabaseTransactions` — os dois seeders precisam rodar por suíte.

### Onde cada cenário mora

| Suíte / pasta | `TestCase` | Cenários | Situação |
|---|---|---|---|
| `tests/Feature/Compras/` | `Tests\TestCase` | os de model, autorização e efeito | pasta a criar; a suíte `Feature` **já existe** |
| `tests/Feature/Compras/` (componente) | idem | os de Livewire/Filament | idem |
| `tests/FeatureTenancy/Compras/` | `Tests\TenancyTestCase` | **CT-36, CT-37** | ⚠️ **pasta, bloco no `tests/Pest.php` e testsuite no `phpunit.xml` a criar** — passo 10 do PRD. Sem os três, os dois cenários **passam por não existirem** |
| `tests/Browser/Compras/` | `Tests\TestCase`, grupo `browser` | CT-B01, CT-B02 | ver `05-casos-de-teste-browser.md` |
| `tests/Unit/` | — | **nenhum** | `tests/Pest.php` não liga `Unit` a `TestCase` nenhum: sem container, `config()` e Eloquent não resolvem |

### Contexto comum dos cenários

Quatro linhas, só `Dado`, e **todas as quatro são discriminantes** — não são cenário, são o mundo
em que o não-efeito significa alguma coisa:

```gherkin
# language: pt
  Contexto:
    Dado a organização "Acme" com o centro de custo "TI", cujo gestor é o Rui
    E a Dora com o papel "diretor" na Acme, e nenhum centro sob a gestão dela
    E a Ana como solicitante, que não é diretora nem gestora de centro nenhum
    E o limite efetivo lido da configuração de fábrica é R$ 5.000,00
```

> A terceira linha é o que impede a persona colapsada. A segunda é o que faz **toda** asserção de
> ausência de notificação discriminar: a Dora existe, e no caminho feliz de uma solicitação acima
> do limite ela **seria** notificada. A quarta é afirmada, e não pressuposta, porque um cenário
> que diz "a configuração de fábrica" sem afirmar o valor lido mede o ambiente:
> confirmado que `phpunit.xml` **não** define `KIT_COMPRAS_LIMITE_DIRETOR`.

Salvo indicação em contrário, **a solicitação dos cenários vale R$ 7.500,00** — acima do limite.
Não é detalhe: é o que garante que exista uma **segunda etapa** e, portanto, um destinatário real
para o não-efeito de notificação em toda célula recusada.

---

## Matriz Estado × Operação — uma só, produto cartesiano fechado

> Montada **antes** das regras e **a partir do enum e da lista de verbos**, não do mapa de
> regras. Decompô-la em matrizes por regra de negócio — uma para `editar/excluir`, outra para
> `enviar`, outra para o estado terminal — parece organização e é perda de cobertura: cada
> operação apareceria só nos estados que a regra dela já pressupõe, e as células que nenhuma
> regra menciona sumiriam sem deixar buraco para alguém notar.

### Contagem — o oráculo da própria matriz

**6 estados × 7 operações = 42 células.** 18 válidas, 24 inválidas. Nenhuma célula sem resolução.

- **Estados** (6): `rascunho (virgem)`, `rascunho (reentrado)`, `aguardando_gestor`,
  `aguardando_diretor`, `aprovada`, `cancelada`.
- **Operações** (7): `editar`, `excluir`, `enviar`, `aprovar`, `rejeitar`, `cancelar`, `visualizar`.

`visualizar` é coluna porque RQ-12 e RQ-13 pedem leitura em **todo** estado — e porque uma matriz
só de verbos de escrita esconderia que a tela precisa saber exibir os cinco rótulos.

> **Por que `rascunho` são duas linhas, e não uma — achado da revisão adversarial.**
> O enum tem cinco casos, mas **`rascunho` é reentrante**: R7 o declara como destino da rejeição.
> Um rascunho **virgem** (zero etapas) e um rascunho **reentrado** (com o histórico de um ciclo
> anterior) são situações de partida diferentes, e uma implementação que barre a edição por
> `$this->etapas()->exists()` — leitura ingênua e natural de RQ-10, "depois de aprovada não pode
> mais mexer" — **aceita o primeiro e recusa o segundo**. Enquanto a matriz tinha uma linha só de
> `rascunho`, as três células de escrita dela eram lidas como inteiras cobrindo metade: a
> contagem dizia 35/35 e o defeito passava justamente em RQ-09, *"o solicitante corrige e envia
> de novo"* — cuja metade "corrigir" não era executada por cenário nenhum.
>
> Desdobrar a linha é o que torna a contagem honesta. Foi o achado mais caro da revisão, e é
> estrutural: **uma matriz montada a partir do enum não enxerga reentrância**, porque o enum não
> a codifica. Quem a codifica é o grafo de transições.

### Legenda — auditada célula a célula

`✅` = a operação é aceita e produz **todos** os efeitos da coluna.
`❌` = a operação é **recusada** e **nenhum** efeito da coluna acontece.

A legenda só é verdadeira se cada `❌` afirmar **todos** os efeitos que **aquela** operação
dispara no caminho feliz — não um efeito genérico escolhido por conveniência. A tabela abaixo é o
que torna a legenda auditável, e cada linha dela foi conferida contra as células:

| Operação | Efeitos no caminho feliz | O que **toda** célula `❌` desta coluna afirma |
|---|---|---|
| `editar` | grava `descricao`, `valor` **e `centro_custo_id`** — **três** campos | situação inalterada **e os três campos gravados inalterados**. Não só o valor: `centro_custo_id` decide **quem aprova**, e é a porta da escalada de A-08 |
| `excluir` | remove a linha **e**, em cascata, as etapas dela | situação inalterada, o registro **ainda existe** **e** o histórico continua com as etapas que tinha |
| `enviar` | situação → `aguardando_gestor` **e** notifica o gestor | situação inalterada **e** o **Rui não é notificado** |
| `aprovar` | situação avança, grava etapa **e** notifica o próximo aprovador — **quando há um** | situação inalterada **e** **nenhuma etapa gravada**; **e** a **Dora não é notificada** *somente nas células em que o caminho feliz teria próximo aprovador* (ver a ressalva abaixo) |
| `rejeitar` | situação → `rascunho` **e** grava etapa com a justificativa | situação inalterada **e** **nenhuma etapa gravada** **e** o histórico anterior intacto. *(sem asserção de notificação: rejeitar **não** notifica no caminho feliz — A-11. Exigi-la seria asserção de vácuo)* |
| `cancelar` | situação → `cancelada` **e o histórico existente sobrevive** (RQ-13 continua valendo depois do cancelamento) | situação inalterada **e** o histórico continua com as etapas que tinha |
| `visualizar` | nenhum efeito | — (a coluna não tem célula inválida) |

> **Três correções da revisão adversarial nesta tabela**, e as três eram do mesmo tipo — a legenda
> era falsa por **sub-declarar o caminho feliz**, que é a metade que ninguém confere:
>
> 1. **`editar` listava três campos e cobrava um.** As células `❌` afirmavam só o `valor`, e
>    `centro_custo_id` ficava editável em trânsito — a Ana move a solicitação para um centro do
>    qual é gestora e se aprova, com CT-17 abençoando solicitante = gestor por A-09. É a escalada
>    de A-08 por uma porta que A-08 não olhou. Agora as células afirmam os três (CT-42, CT-43,
>    CT-44, CT-45), e a cadeia inteira é CT-46.
> 2. **`cancelar` declarava um único efeito** e concluía que "não havia nada além a afirmar". O
>    cancelamento a partir de `aguardando_diretor` tem um segundo efeito obrigatório: o histórico
>    **sobrevive**, porque RQ-13 não deixa de valer quando a solicitação é cancelada. Sem isso, um
>    `cancelar()` que fizesse `$this->etapas()->delete()` atravessava a matriz inteira.
> 3. **`excluir` não declarava a cascata**, e por isso a célula `❌` não tinha como afirmar o
>    não-efeito correspondente.
>
> **Ressalva honesta na coluna `aprovar`**: nas células de `aprovada` e `cancelada` não existe
> próximo aprovador, então "a Dora não é notificada" ali é **vácuo** — o mutante e a implementação
> correta produzem o mesmo observável. A asserção continua escrita nessas células por simetria de
> leitura, mas **não é ela que resolve a célula**: quem resolve são a situação e o histórico, e é
> assim que a tabela de mutantes as credita. Marcar isso é o que impede a legenda de voltar a ser
> uma promessa não auditada.

> **Isto não cria matriz nova**: as direções do rastreio de efeito são **colunas do `Esquema`** de
> cada cenário de linha, dentro da matriz única. Um `Esquema` conta como 1 cenário, então o custo
> é em colunas, não em teto de perfil.
>
> **E cada asserção de ausência tem destinatário real**: o Rui existe (é o gestor do centro), a
> Dora existe (é diretora da Acme) e a solicitação vale R$ 7.500,00 — acima do limite, portanto
> **com segunda etapa**. Numa fixture sem gestor ou sem diretor, o mutante e a implementação
> correta produziriam o mesmo observável, e a coluna inteira seria decorativa.

### A matriz

Nas células `❌`, o ator é **quem teria direito àquele verbo em algum estado** — o solicitante
para `editar`/`excluir`/`enviar`/`cancelar`, o aprovador da etapa para `aprovar`/`rejeitar`.
Isso isola a dimensão **estado**; a dimensão **persona** é isolada separadamente pelas matrizes
papel × verbo de R2, R5 e R13.

| estado \ operação | `editar` | `excluir` | `enviar` | `aprovar` | `rejeitar` | `cancelar` | `visualizar` |
|---|---|---|---|---|---|---|---|
| **rascunho (virgem)** | ✅ CT-06 | ✅ CT-40 | ✅ CT-10 | ❌ CT-41 | ❌ CT-41 | ❌ CT-24 ⚑ | ✅ CT-25 |
| **rascunho (reentrado)** | ✅ **CT-47** | ✅ CT-40 | ✅ CT-22 | ❌ CT-41 | ❌ CT-41 | ❌ CT-24 ⚑ | ✅ CT-25 |
| **aguardando_gestor** | ❌ CT-42 | ❌ CT-42 | ❌ CT-42 | ✅ CT-12 | ✅ CT-21 | ✅ CT-24 | ✅ CT-25 |
| **aguardando_diretor** | ❌ CT-43 | ❌ CT-43 | ❌ CT-43 | ✅ CT-14 | ✅ CT-16 | ✅ CT-24 | ✅ CT-25 |
| **aprovada** | ❌ CT-44 | ❌ CT-44 | ❌ CT-44 | ❌ CT-44 | ❌ CT-44 | ❌ CT-44 | ✅ CT-25 |
| **cancelada** | ❌ CT-45 | ❌ CT-45 | ❌ CT-45 | ❌ CT-45 | ❌ CT-45 | ❌ CT-45 | ✅ CT-25 |

⚑ `cancelar` em `rascunho` é `@premissa` (A-06): o `00` decidiu que ali o verbo é **excluir**.
Se negado, essas duas células viram ✅ e CT-24 inverte as duas linhas correspondentes.

**As células novas da linha reentrada**, e o que cada uma custou: `editar` é **CT-47** (cenário
novo, achado nº 2 da revisão — a metade "corrigir" de RQ-09 não era executada em lugar nenhum);
`excluir` virou a segunda linha do `Esquema` de **CT-40**; `enviar` já era **CT-22**, o 2-switch;
`aprovar`, `rejeitar` e `cancelar` ganharam linha própria nos `Esquema` de **CT-41** e **CT-24**.
Nenhuma célula nova exigiu um cenário inteiro além de CT-47 — o custo real foi em **linhas de
`Exemplos`**, que não consomem teto de perfil.

**Cada coluna de escrita tem ao menos uma célula válida exercitada** — `editar` CT-06 e CT-47,
`excluir` CT-40, `enviar` CT-10 e CT-22, `aprovar` CT-12, `rejeitar` CT-21, `cancelar` CT-24. Sem
essa metade da regra, a coluna `editar` ficaria com recusas e nenhuma edição que funciona, e a
armadilha da unicidade contra o próprio registro passaria inteira.

### As duas dimensões que a matriz não mostra

`estado × operação` é a face visível. **Quem** executa e **qual campo** muda são dimensões, não
detalhes do exemplo — percorrer a matriz com persona e campo fixos produz uma matriz "100%
coberta" com duas dimensões intocadas.

| Dimensão | Onde é exercitada | Se ficasse fixa, perderia |
|---|---|---|
| **persona** | R2 (CT-08, CT-09), R5 (CT-15, CT-16, CT-18, CT-49), R13 (CT-32…CT-35) | a autorização inteira — a barreira de identidade |
| **campo alterado** | CT-06 (os três campos, em `rascunho`) · CT-42/CT-43/CT-44/CT-45, que alteram **o valor e o centro de custo** fora do estado inicial · CT-46, a cadeia completa | a recomputação de alçada **e** a escolha do aprovador |
| **cardinalidade do decisor** | CT-49 (três diretores, a primeira resolve) | a regra de A-03: com uma diretora só, *"a primeira que decidir resolve"* e *"todas precisam decidir"* são indistinguíveis |

**A dimensão do campo é exercitada fora do estado inicial de propósito.** Trocar o campo decisivo
em `rascunho`, onde tudo é editável, não reabre a dimensão para os estados de trânsito — e é
exatamente ali que mora o defeito. Por isso as linhas `editar` de CT-42…CT-45 alteram **o valor**
(R$ 7.500,00 → R$ 100,00) **e o centro de custo**, e afirmam **os dois campos gravados**, não só
que a operação foi recusada.

> **O achado nº 1 da revisão adversarial mora exatamente aqui.** Na primeira versão, esta seção
> nomeava a dimensão "campo alterado", declarava que ela era exercitada fora do estado inicial —
> e a exercitava com **um** campo só, o `valor`. O centro de custo, que decide **quem aprova**, só
> era trocado em `rascunho` (CT-06), que é precisamente o caso que este parágrafo diz não bastar.
> Nomear a dimensão e cobrir metade dela é pior que não nomear: o texto certifica uma cobertura
> que a matriz não tem.

**Célula só conta se a operação daquela célula for executada.** Nenhuma célula desta matriz
aponta para um cenário que executa outro verbo, e nenhuma é justificada por argumento do tipo
"uma implementação correta se comportaria igual nas duas linhas" — o argumento pressupõe a
corretude que a célula existe para testar.

---

## Regra R1 — a solicitação nasce em rascunho com descrição, valor e centro de custo

> `RQ-01` · área **A**, perfil **completo** · técnicas: **EP** + **BVA na gravação**
> (incremento `0,01`, e `0,001` na linha de precisão) + **mass assignment**
> Pontos cobertos: **criação** (CT-01…CT-04) e **edição** (CT-05). O ponto de **uso** do valor é R4.

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: uma solicitação nasce em rascunho, com descrição, valor e centro de custo

    Cenário: [CT-50] a criação persiste os três campos que o requisito nomeia
      Dado a Ana no formulário de nova solicitação, sem nenhuma solicitação criada
      Quando a Ana grava "Notebooks para o time de suporte", R$ 4.000,00, no centro "TI"
      Então existe uma solicitação da Ana com descrição "Notebooks para o time de suporte",
        valor R$ 4.000,00 e o centro "TI"
      E ela está em "rascunho", com o histórico vazio

    Esquema do Cenário: [CT-01] o domínio do valor é conferido na gravação da criação
      Dado a Ana no formulário de nova solicitação, sem nenhuma solicitação criada
      Quando a Ana grava uma solicitação de "Notebooks" no centro "TI" com valor <valor>
      Então o resultado é "<resultado>"
      E o número de solicitações da Ana é <gravadas>, e o valor gravado é <gravado>

      Exemplos:
        | valor              | resultado | gravadas | gravado          | # borda                                     |
        | -0,01              | recusado  | 0        | —                | abaixo do mínimo — @premissa A-15           |
        | 0,00               | recusado  | 0        | —                | borda inferior — @premissa A-15             |
        | 0,01               | aceito    | 1        | 0,01             | borda+0,01 — o menor valor válido           |
        | 9.999.999.999,99   | aceito    | 1        | 9.999.999.999,99 | teto de decimal(12,2) — @premissa-mecanismo |
        | 10.000.000.000,00  | recusado  | 0        | —                | acima do teto — @premissa A-17              |

    Cenário: [CT-02] valor com mais de duas casas decimais é recusado na gravação
      Dado a Ana criando uma solicitação diretamente pelo model, por fora do formulário
      Quando a Ana grava uma solicitação de R$ 4.999,995 no centro "TI"
      Então a gravação é recusada
      E o número de solicitações da Ana é zero

    Cenário: [CT-54] o valor gravado é o mesmo que decide a alçada
      Dado uma solicitação da Ana gravada com R$ 4.999,995 por qualquer via — factory,
        seeder ou escrita direta no banco — e enviada
      Quando o Rui aprova a etapa de gestor
      Então a solicitação fica em "aprovada", sem passar pelo diretor
      E o valor gravado é exatamente o mesmo número que foi comparado com o limite
```

**CT-50 é o oráculo positivo de RQ-01, e ele faltava.** A cláusula diz *"o solicitante cria uma
solicitação de compra **com descrição, valor e centro de custo**"* — e a primeira versão deste
conjunto gastou EP, BVA e mass assignment inteiramente no que **não** deve ser gravado, sem nunca
afirmar que os três campos submetidos chegaram ao banco. Uma `descricao` fora do `$fillable`, um
`Select` que grava sem a relação ou um truncamento do banco atravessavam CT-01 (que só contava
linhas), CT-03 (cujas linhas aceitas não afirmavam nada) e CT-04 (que afirma justamente os campos
que **não** vêm do formulário). Achado nº 5 da revisão adversarial.

**CT-01 agora afirma o valor gravado, e não a contagem.** A linha do teto de `decimal(12,2)`
existia para pegar truncamento silencioso — e o truncamento **grava a linha**, então a contagem
dava 1 e a linha passava. `assertDatabaseHas` só com a chave primária passa com todos os outros
campos errados; contar registros é a mesma falha com outra roupa.

**CT-02 e CT-54 eram um cenário só, e ele era autocontraditório.** A versão original dizia
*"a gravação é recusada"* e, nas duas linhas seguintes, pressupunha a solicitação gravada para
afirmar o invariante. Materializado ao pé da letra, o invariante era **inexecutável** — ou seja,
o invariante das duas leituras que a premissa A-15 exige **não existia**, apesar de o texto
afirmar que existia. Agora são dois: CT-02 é a direção por falha fechado (`@premissa` A-15);
**CT-54 é o invariante**, escrito no ramo em que a gravação aconteceu, e por isso ele vale
**qualquer que seja** a resposta a A-15 — inclusive se ela for negada e CT-02 inverter. Achado
nº 10 da revisão.

**CT-01 — por que estes valores.** `0,00` e `0,01` são a fronteira real do domínio, e o
incremento é o do tipo (`decimal(12,2)` → `0,01`). O teto e o teto+1 existem porque
`decimal(12,2)` não representa dez bilhões: sem a linha, o truncamento silencioso do banco passa.
Um `Esquema` conta como **1 cenário**.

**CT-02 — duas coisas, e cada uma tem razão.**

1. **É o cenário por fora da UI de R1** (gate de camada da regra de validação de domínio). Ele
   grava pelo model, não pelo formulário — e é o único que distingue *"a regra existe"* de
   *"a tela chama a regra"*.
2. **O valor é discriminante, e um valor redondo não seria.** R$ 4.999,995 é um ponto em que
   truncar (→ R$ 4.999,99) e arredondar (→ R$ 5.000,00) produzem **números gravados diferentes**
   na fronteira exata da alçada; e o simétrico R$ 5.000,005, arredondado a R$ 5.000,01, passaria
   a **exigir diretor** por causa de um dígito que o usuário não viu. O incremento aqui é o
   **milésimo**, escalado acima do perfil, e a justificativa está em `## Escalada de técnica`.

> ⚠️ **CT-02 nasce vermelho contra o plano como está** — ver a pergunta **A-16**. O PRD põe a
> validação de domínio só no `TextInput` (passo 9a). Isso é resultado do gate, não defeito do
> cenário: teste vermelho por divergência entre desenhado e implementado é exatamente o que ele
> existe para capturar.

```gherkin
    Esquema do Cenário: [CT-03] a solicitação exige descrição e centro de custo
      Dado a Ana no formulário de nova solicitação
      Quando a Ana grava uma solicitação com <campo> igual a "<entrada>"
      Então o resultado é "<resultado>"
      E, nas recusas, nenhuma solicitação é gravada e o campo apontado é "<campo>"
      E, nas aceitações, o <campo> gravado é lido de volta **idêntico** à entrada

      Exemplos:
        | campo           | entrada                          | resultado | # partição                     |
        | descricao       | (vazia)                          | recusado  | vazia                          |
        | descricao       | "   "                            | recusado  | só espaços                     |
        | descricao       | 255 caracteres                   | aceito    | limite — @premissa-mecanismo   |
        | descricao       | 256 caracteres                   | recusado  | limite+1 — @premissa-mecanismo |
        | descricao       | "Servidor de bancó de dados 🖥️" | aceito    | acento + emoji de 4 bytes      |
        | centro_custo_id | (ausente)                        | recusado  | ausente                        |

    Cenário: [CT-04] o formulário não escolhe a situação, o solicitante nem a organização
      Dado a Ana no formulário de nova solicitação, e o Bruno como outro usuário da Acme
      Quando a Ana envia o formulário acrescentando situação "aprovada", solicitante Bruno
        e organização "Globex"
      Então a solicitação nasce em "rascunho", com a Ana como solicitante, na Acme
      E o histórico da solicitação está vazio

    Esquema do Cenário: [CT-05] o domínio do valor também é conferido na edição
      Dado uma solicitação da Ana em "rascunho", de R$ 4.000,00, no centro "TI"
      Quando a Ana altera o valor para <valor> e salva
      Então o resultado é "<resultado>", e o valor gravado é <gravado>

      Exemplos:
        | valor    | resultado | gravado  | # partição                   |
        | 0,00     | recusado  | 4.000,00 | borda inferior — @premissa   |
        | -0,01    | recusado  | 4.000,00 | abaixo do mínimo — @premissa |
        | 0,01     | aceito    | 0,01     | borda+0,01                   |
        | 7.500,00 | aceito    | 7.500,00 | partição válida acima        |
```

**CT-05 fecha a armadilha da edição**: *validação escrita no `create` e esquecida no `save` é
invisível para qualquer cenário que só crie*. É também a **gravação por componente da rota
`edit`** de `SolicitacaoCompra` — metade do gate de tela de escrita (a outra metade é CT-01, na
rota `create`).

**CT-04 afirma o histórico vazio de propósito**: uma implementação que aceitasse `situacao` do
formulário poderia nascer em `aprovada` **sem nenhuma etapa** — e a asserção de situação sozinha
não distinguiria isso de uma aprovação legítima mal gravada.

#### Mutantes previstos — R1

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1.1 | `>= 0` no lugar de `> 0` no valor mínimo | CT-01 (linha `0,00`) |
| M1.2 | `situacao` incluída no `$fillable` | CT-04 |
| M1.3 | `solicitante_id` vem do formulário, não do usuário autenticado | CT-04 |
| M1.4 | a validação de domínio existe no `create` e some no `save` | CT-05 |
| M1.5 | `valor` sem o cast `decimal:2` (fica `float`): a terceira casa sobrevive gravada e decide a alçada | CT-02, CT-54 |
| M1.6 | `descricao` validada por `!== null`, e `"   "` passa | CT-03 (linha só espaços) |
| M1.7 | `descricao` fora do `$fillable`, ou `centro_custo_id` gravado nulo pelo `Select` sem relação — a solicitação nasce incompleta e ninguém percebe | **CT-50** |
| M1.8 | o valor acima do teto é **truncado** pelo banco em vez de recusado — a linha é gravada, e a contagem de registros não acusa | **CT-01** (coluna `gravado`) |
| M1.9 | `Str::ascii()` ou `substr()` de saneamento na descrição — acento e emoji são perdidos na gravação | **CT-03** (linha unicode, lida de volta) |

> **M1.7, M1.8 e M1.9 vieram da revisão adversarial** (achados 5 e 2 da lista de `Então` fraco).
> Os três atravessavam a versão anterior porque **nenhum cenário de R1 afirmava um campo
> persistido** — a regra inteira media contagem de linhas e recusas. Pelo teto do perfil
> `completo`, R1 estouraria com 9 mutantes; a exceção da skill vale aqui: **mutante trazido pela
> revisão adversarial não conta para o teto**, porque é achado medido, e não enchimento.

---

## Regra R2 — em rascunho, só o solicitante edita e exclui

> `RQ-02`, `RQ-03` · área **B**, perfil **completo** · técnica: **matriz papel × verbo**
> As células de **estado** desta regra vivem na matriz única (CT-42, CT-43, CT-44, CT-45).

```gherkin
  Regra: em rascunho, o solicitante — e só ele — edita e exclui a própria solicitação

    Esquema do Cenário: [CT-06] a Ana edita o próprio rascunho, campo a campo
      Dado uma solicitação da Ana em "rascunho", "Notebooks", R$ 4.000,00, no centro "TI"
      Quando a Ana altera <campo> para <novo> e salva
      Então o <campo> gravado é <novo>, e a situação continua "rascunho"

      Exemplos:
        | campo           | novo         | # dimensão do campo              |
        | descricao       | "Monitores"  | campo neutro                     |
        | valor           | 7.500,00     | **campo que decide a alçada**    |
        | centro_custo_id | "RH" (Carla) | **campo que decide quem aprova** |

    Cenário: [CT-07] a alçada é recomputada sobre o valor editado, não sobre o original
      Dado uma solicitação da Ana criada por R$ 4.000,00, editada em rascunho para
        R$ 7.500,00 e depois enviada
      Quando o Rui aprova a etapa de gestor
      Então a solicitação fica em "aguardando diretor"
      E o valor gravado é R$ 7.500,00

    Esquema do Cenário: [CT-08] quem não é o solicitante não edita nem exclui, nem por fora da tela
      Dado uma solicitação da Ana em "rascunho", "Notebooks", R$ 7.500,00, no centro "TI"
      Quando o <ator> executa "<verbo>" sobre ela chamando o model diretamente
      Então a operação é recusada
      E a solicitação ainda existe, com descrição "Notebooks", valor R$ 7.500,00 e
        situação "rascunho"

      Exemplos:
        | ator  | verbo   | # persona                               |
        | Bruno | editar  | terceiro sem vínculo                    |
        | Bruno | excluir | **verbo irmão — não herda a evidência** |
        | Rui   | editar  | gestor do centro: aprova, mas não edita |
        | Rui   | excluir | idem                                    |
        | Dora  | editar  | diretora: aprova, mas não edita         |
        | Dora  | excluir | idem                                    |

    Esquema do Cenário: [CT-09] a tela não oferece o que a pessoa não pode fazer
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro "TI"
      Quando o <ator> abre a listagem de solicitações
      Então a solicitação aparece na listagem para ele
      E a ação "Editar" está <editar> e a ação "Excluir" está <excluir>

      Exemplos:
        | ator  | editar  | excluir | # persona                           |
        | Ana   | visível | visível | dona do rascunho                    |
        | Bruno | oculta  | oculta  | terceiro                            |
        | Rui   | oculta  | oculta  | gestor — lê para decidir, não edita |
        | Dora  | oculta  | oculta  | diretora — idem                     |
```

**CT-08 é o cenário por fora do componente de UI de R2** (gate de camada da regra de
autorização). CT-09 prova a **affordance**; CT-08 prova a **barreira**. Os dois existem porque um
teste de componente **não consegue, por construção**, distinguir *"a regra vive no domínio e a
tela a chama"* de *"a regra vive só no `->visible()`"*.

**CT-08 cobre os dois verbos, e isso não é redundância.** Uma implementação que confere a
identidade em `editar()` e esquece em `excluir()` passa em qualquer conjunto cuja evidência venha
só do primeiro verbo — e o checklist lê ✅ cobrindo metade da regra.

**CT-09 é também o cenário de leitura de A-14**: o Rui e a Dora **veem** a solicitação e **não**
recebem as ações. É o invariante *"ler nunca autoriza agir"* afirmado onde ele é observável.

#### Mutantes previstos — R2

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M2.1 | a barreira de identidade vive só na policy (affordance) e o model aceita qualquer chamador | CT-08 |
| M2.2 | a identidade é conferida em `editar` e esquecida em `excluir` | CT-08 (linhas `excluir`) |
| M2.3 | a alçada é decidida na criação e congelada — editar o valor não a recomputa | CT-07 |
| M2.4 | a policy filtra por permission e não por dono do registro | CT-09 (o Bruno veria os botões) |
| M2.5 | a policy filtra por dono e ignora a situação — a Ana continuaria editando depois de enviar | CT-42, CT-43 (matriz) |
| M2.6 | a edição do rascunho é permitida só quando ele nunca teve etapa — o rascunho reentrado fica travado | **CT-47** — revisão adversarial |

---

## Regra R3 — o envio endereça a solicitação ao gestor do centro de custo, ou falha fechado

> `RQ-04` (A-10) · área **A**, perfil **completo** · técnicas: **tabela de decisão** +
> **cardinalidade do destinatário**

```gherkin
  Regra: o envio endereça a solicitação ao gestor do centro de custo — e falha fechado sem ele

    Esquema do Cenário: [CT-10] o envio depende de haver um gestor no centro de custo
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro <centro>
      Quando a Ana envia a solicitação
      Então o resultado é "<resultado>" e a situação passa a ser "<situacao>"
      E as notificações enviadas são: <notificados>

      Exemplos:
        | centro               | resultado | situacao          | notificados                         |
        | "TI" (gestor: Rui)   | aceito    | aguardando gestor | o Rui, por e-mail, uma vez          |
        | "Obras" (sem gestor) | recusado  | rascunho          | ninguém — **nem a Dora, nem a Ana** |

    Cenário: [CT-11] o duplo clique no envio não reenvia nem duplica
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro "TI"
      E que a Ana já enviou essa solicitação uma vez
      Quando a Ana envia a mesma solicitação de novo
      Então a segunda tentativa é recusada
      E a solicitação persistida está em "aguardando gestor", com o histórico vazio
      E o Rui recebeu exatamente uma notificação

    Cenário: [CT-53] trocar o gestor do centro troca quem decide a etapa pendente
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI",
        cujo gestor era o Rui quando ela foi enviada
      E que o gestor do centro "TI" passou a ser a Carla depois do envio
      Quando o Rui aprova a etapa de gestor
      Então a operação é recusada, a situação continua "aguardando gestor" e o histórico
        continua vazio
      E a Carla aprovando a mesma etapa é aceita, e o histórico registra gestor/Carla/aprovada
```

**CT-53 fecha o achado nº 13 da revisão adversarial.** A varredura SFDIPOT declarava, na linha
`Operations`, o risco *"gestor removido do centro depois do cadastro"* — e mapeava para três
cenários que não faziam nem uma coisa nem outra. Zero cenários trocavam o gestor com a
solicitação **já em trânsito**, e é aí que a pergunta tem consequência: o aprovador da vez é
resolvido **no momento da decisão** (pela FK atual) ou **congelado no envio**? O requisito não
decide, e a diferença é observável.

> **`@premissa` de comportamento, direção por falha fechado**: o aprovador é o gestor **atual** do
> centro, lido na hora da decisão — o mesmo mecanismo de RQ-04, *"o gestor do centro de custo"*,
> no presente. Assumir o congelamento no envio criaria uma autoridade que **não existe mais** na
> organização, e é a leitura que erra para o lado caro. **Invariante das duas leituras, afirmado
> na última linha**: seja qual for a resposta, **exatamente uma** pessoa decide a etapa de gestor,
> e a decisão dela é registrada com o nome de quem decidiu. **Se negado**, as duas metades de
> CT-53 se invertem entre si e o invariante permanece. **Pergunta A-21**, no bloco de perguntas.

**CT-10, linha "sem gestor" — por que ela discrimina.** Um cenário de zero destinatários é
partição legítima e **não** vale como prova de não-efeito. Por isso o `Então` dela não afirma
"nenhuma notificação": afirma que **a Dora e a Ana**, que existem no mundo do `Contexto`, não são
notificadas. É o que mata o mutante *"sem gestor, pula a etapa e endereça direto ao diretor"* —
que num mundo sem diretora produziria exatamente o mesmo observável da implementação correta.

**CT-11 ancora a idempotência no agregado persistido**, não no retorno da chamada: o oráculo é o
estado da solicitação no banco, a contagem de etapas e a contagem de notificações. Afirmar sobre
o valor devolvido por duas chamadas passaria por construção.

#### Mutantes previstos — R3

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M3.1 | `gestor_id` nulo: envia mesmo assim, e a solicitação fica esperando ninguém | CT-10 (linha sem gestor: a situação continua "rascunho") |
| M3.2 | `gestor_id` nulo: pula a etapa de gestor e endereça ao diretor | CT-10 (linha sem gestor: **a Dora não é notificada**) |
| M3.3 | o aprovador é resolvido por **papel** em vez da FK `centros_custo.gestor_id` | CT-10 (linha "TI": o destinatário afirmado é o **Rui**, que não tem papel de aprovador nenhum) |
| M3.4 | o envio usa `get()` + `save()`: a segunda chamada regrava e reenvia o e-mail | CT-11 |
| M3.5 | o aprovador é **congelado no envio** (gravado numa coluna), e o gestor atual do centro não decide mais | **CT-53** — revisão adversarial |

---

## Regra R4 — acima de R$ 5.000 a aprovação do diretor vem depois da do gestor

> `RQ-05` (A-04) · área **A**, perfil **completo** · técnica: **BVA 3-valores**,
> incremento `0,01` (o tipo do campo)

```gherkin
  Regra: acima de R$ 5.000 a solicitação exige também a aprovação do diretor, depois da do gestor

    Esquema do Cenário: [CT-12] a fronteira da alçada é estritamente maior que o limite
      Dado que a configuração é lida de fábrica, sem nenhum ajuste do teste, e o limite
        efetivo é R$ 5.000,00
      E uma solicitação da Ana de <valor>, em "aguardando gestor", no centro "TI"
      Quando o Rui aprova a etapa de gestor
      Então a solicitação fica em "<situacao>"
      E as notificações enviadas são: <notificados>

      Exemplos:
        | valor    | situacao           | notificados        | # borda                          |
        | 4.999,99 | aprovada           | ninguém            | borda−0,01                       |
        | 5.000,00 | aprovada           | ninguém            | **borda exata — "acima de" exclui o próprio valor (A-04)** |
        | 5.000,01 | aguardando diretor | a Dora, por e-mail | borda+0,01                       |

    Cenário: [CT-13] o diretor não decide antes do gestor
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI",
        com o histórico vazio
      Quando a Dora aprova a solicitação
      Então a operação é recusada
      E a solicitação continua em "aguardando gestor", o histórico continua vazio, e nem o
        Rui nem a Dora recebem notificação

    Cenário: [CT-14] a aprovação do diretor encerra o fluxo
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando diretor", com a etapa de
        gestor já decidida pelo Rui como "aprovada"
      Quando a Dora aprova a solicitação
      Então a solicitação fica em "aprovada"
      E o histórico tem duas etapas, na ordem: gestor/Rui/aprovada, depois diretor/Dora/aprovada
      E ninguém é notificado — nem a Ana, nem o Rui, nem a Dora
```

**CT-12 usa o número literal do card, e o `Dado` afirma o valor efetivo lido.** Injetar o limite
por `config()->set()` em todo cenário deixaria o único valor literal do requisito sem nenhum
teste, e qualquer default errado passaria. Mas escrever *"a configuração de fábrica"* sem afirmar
o valor lido também é vácuo — o cenário passaria medindo o ambiente. Foi confirmado que
`phpunit.xml` **não** define `KIT_COMPRAS_LIMITE_DIRETOR` (arquivo lido por inteiro,
`phpunit.xml:47-62`), então o cenário mede a política, não o `.env`.

**A coluna `notificados` na borda não é decoração.** Nas duas linhas em que a situação final é
`aprovada`, o `Então` afirma que **a Dora não é notificada** — e a Dora existe. Sem isso, o
mutante *"cria a etapa de diretor e notifica, mas marca como aprovada"* atravessaria as três
linhas com a asserção de situação intacta.

**CT-13 e CT-14 são a ordem, que a fronteira não prova.** Um conjunto que só testa o limite
mostra *quantas* aprovações a solicitação precisa e nada sobre *em que ordem* — e "depois do
gestor" é metade literal de RQ-05.

#### Mutantes previstos — R4

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M4.1 | `>=` no lugar de `>` na comparação com o limite | CT-12 (linha `5.000,00`) |
| M4.2 | comparação invertida — abaixo do limite é que exige diretor | CT-12 (linha `4.999,99`) |
| M4.3 | a etapa corrente não é verificada, e o diretor pode decidir antes do gestor | CT-13 |
| M4.4 | a etapa de diretor é criada mas a situação vai direto para "aprovada" | CT-12 (linha `5.000,01`) |
| M4.5 | a aprovação do diretor não fecha o fluxo — a situação continua "aguardando diretor" | CT-14 |
| M4.6 | a segunda etapa é gravada com `etapa = 'gestor'` (o rótulo da etapa não acompanha a fase) | CT-14 |

> **Mutante recusado por implausibilidade**: *"o limite vem de um literal `5000` no código, não da
> configuração"*. Com a configuração de fábrica ele produz **exatamente** o mesmo observável — não
> há valor que o distinga. Onde o número mora é escolha de implementação, e a skill é explícita:
> isso não vira oráculo. O que **é** oráculo é o número, e ele está em CT-12.

---

## Regra R5 — só quem decide a etapa corrente aprova ou rejeita

> `RQ-06` (A-07, A-09) · área **B**, perfil **completo** · técnica: **matriz papel × verbo**,
> aplicada **verbo a verbo** e em **cada etapa**

```gherkin
  Regra: só quem decide a etapa corrente aprova ou rejeita a solicitação

    Esquema do Cenário: [CT-15] na etapa de gestor, só o gestor daquele centro decide
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      E a Carla como gestora de um outro centro, o "RH"
      Quando o <ator> executa "<verbo>" chamando o model diretamente
      Então o resultado é "<resultado>", a situação passa a ser "<situacao>" e o histórico
        tem <etapas> etapa(s)
      E, nas recusas, a Dora não recebe notificação

      Exemplos:
        | ator  | verbo    | resultado | situacao           | etapas | # persona                      |
        | Rui   | aprovar  | aceito    | aguardando diretor | 1      | gestor do centro               |
        | Rui   | rejeitar | aceito    | rascunho           | 1      | gestor do centro               |
        | Carla | aprovar  | recusado  | aguardando gestor  | 0      | **gestora de OUTRO centro**    |
        | Carla | rejeitar | recusado  | aguardando gestor  | 0      | idem, verbo irmão              |
        | Dora  | aprovar  | recusado  | aguardando gestor  | 0      | diretora — etapa dela é depois |
        | Dora  | rejeitar | recusado  | aguardando gestor  | 0      | idem, verbo irmão              |
        | Ana   | aprovar  | recusado  | aguardando gestor  | 0      | solicitante                    |
        | Ana   | rejeitar | recusado  | aguardando gestor  | 0      | idem, verbo irmão              |
        | Bruno | aprovar  | recusado  | aguardando gestor  | 0      | terceiro sem vínculo           |
        | Bruno | rejeitar | recusado  | aguardando gestor  | 0      | idem, verbo irmão              |

    Esquema do Cenário: [CT-16] na etapa de diretor, o gestor que já decidiu não decide de novo
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando diretor", com a etapa de
        gestor já decidida pelo Rui como "aprovada"
      Quando o <ator> executa "<verbo>" chamando o model diretamente
      Então o resultado é "<resultado>", a situação passa a ser "<situacao>" e o histórico
        tem <etapas> etapa(s)

      Exemplos:
        | ator  | verbo    | resultado | situacao           | etapas | # persona                    |
        | Dora  | aprovar  | aceito    | aprovada           | 2      | diretora                     |
        | Dora  | rejeitar | aceito    | rascunho           | 2      | diretora — A-07              |
        | Rui   | aprovar  | recusado  | aguardando diretor | 1      | **gestor: a etapa dele já foi** |
        | Rui   | rejeitar | recusado  | aguardando diretor | 1      | idem, verbo irmão            |
        | Ana   | aprovar  | recusado  | aguardando diretor | 1      | solicitante                  |
        | Ana   | rejeitar | recusado  | aguardando diretor | 1      | idem, verbo irmão            |

    Cenário: [CT-17] a solicitante que é gestora do próprio centro decide a etapa de gestor
      Dado o centro "Compras", cuja gestora é a própria Ana
      E uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "Compras"
      Quando a Ana aprova a etapa de gestor
      Então a solicitação fica em "aguardando diretor", e não em "aprovada"
      E o histórico tem uma etapa: gestor/Ana/aprovada

    Cenário: [CT-49] com vários diretores, a primeira decisão resolve a etapa
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando diretor", com a etapa de
        gestor já decidida pelo Rui
      E a Acme com três diretores: a Dora, a Elis e o Fábio
      Quando a Elis aprova a solicitação
      Então a solicitação fica em "aprovada"
      E o histórico tem exatamente duas etapas, sendo a segunda diretor/Elis/aprovada
      E o Fábio aprovando a mesma solicitação é recusado, sem gravar terceira etapa

    Esquema do Cenário: [CT-18] a tela só oferece decidir a quem decide a etapa corrente
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      Quando o <ator> abre a listagem de solicitações
      Então a solicitação aparece na listagem para ele
      E as ações "Aprovar" e "Rejeitar" estão <acoes>

      Exemplos:
        | ator  | acoes   | # persona                       |
        | Rui   | visíveis | gestor do centro, etapa corrente |
        | Dora  | ocultas | diretora — a vez dela é depois   |
        | Ana   | ocultas | solicitante                      |
        | Carla | ocultas | gestora de outro centro          |
        | Bruno | ocultas | terceiro                         |
```

**CT-15 e CT-16 são os cenários por fora do componente de UI de R5.** Chamam o model direto, com
a pessoa errada. É o que a regra do projeto cobra literalmente
(`.ai/rules/filament.md` → *"Barreira sem teste direto não é barreira — o caso que passa pela
tela continuaria verde com a asserção removida"*), e é a única forma de distinguir
*"a regra vive no domínio"* de *"a regra vive no `->visible()` da ação"*.

**A Carla existe só para uma coisa**: distinguir *"é gestor de algum centro"* de *"é gestor
**deste** centro". Sem ela, uma implementação que consulta
`CentroCusto::where('gestor_id', $user->id)->exists()` fica verde no conjunto inteiro.

**Todo verbo aparece com todo ator.** Verbo irmão não herda evidência: uma implementação que
confere o ator em `aprovar()` e esquece em `rejeitar()` passaria em qualquer conjunto que só
falsificasse o primeiro — e o checklist leria ✅ cobrindo metade da regra.

**CT-17 é `@premissa` de A-09**, e o invariante está afirmado na mesma frase: mesmo com a Ana
acumulando os dois papéis, a solicitação **não** salta para `aprovada`. Seja qual for a resposta
sobre segregação de funções, ninguém pula a etapa de diretor por ser as duas pessoas ao mesmo
tempo. **Se A-09 for negada**, a primeira linha do `Então` inverte para "a operação é recusada e
a situação continua em aguardando gestor", e o invariante segue valendo.

#### Mutantes previstos — R5

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M5.1 | a autorização é conferida em `aprovar()` e esquecida em `rejeitar()` | CT-15, CT-16 (linhas `rejeitar`) |
| M5.2 | qualquer pessoa com a permission do painel decide | CT-15 (Bruno), CT-16 (Ana) |
| M5.3 | a verificação é *"é gestor de algum centro"*, não *"é o gestor deste centro"* | CT-15 (Carla) |
| M5.4 | o gestor continua podendo decidir na etapa de diretor | CT-16 (Rui) |
| M5.5 | a regra vive só no `->visible()` da ação; a chamada direta passa | CT-15, CT-16 (são chamadas diretas) |
| M5.6 | o solicitante que também é gestor faz a solicitação saltar para "aprovada" | CT-17 |
| M5.7 | a etapa de diretor só fecha quando **todos** os diretores decidem (`count(etapas) >= count(diretores)`) | **CT-49** — revisão adversarial |
| M5.8 | só o **primeiro** diretor devolvido pela consulta pode decidir; os demais são recusados | **CT-49** (quem decide é a Elis, a segunda) |

> **CT-49 fecha o achado nº 4 da revisão adversarial**, e a lacuna era de enquadramento, não de
> rigor: **todo** cenário que exercitava a decisão do diretor (CT-14, CT-16, CT-27, CT-35, CT-44)
> tinha exatamente **uma** diretora. A cardinalidade 0/1/N tinha sido aplicada ao *destinatário da
> notificação* (R12, CT-29) e nunca ao **ato de decidir** — e a única linha com N=3 parava na
> notificação da transição, sem chegar a nenhuma decisão. Com uma diretora só, *"a primeira que
> decidir resolve"* (A-03) e *"todas precisam decidir"* são **indistinguíveis**.
>
> A dimensão da cardinalidade do decisor está agora registrada em
> [`## As duas dimensões que a matriz não mostra`](#as-duas-dimensões-que-a-matriz-não-mostra).

---

## Regra R6 — rejeição sem justificativa é recusada

> `RQ-07` · área **A**, perfil **completo** · técnica: **EP** — ausente ≠ `null` ≠ `""` ≠ só espaços

```gherkin
  Regra: a rejeição exige justificativa

    Esquema do Cenário: [CT-19] a justificativa é exigida pelo domínio, não só pelo formulário
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      Quando o Rui rejeita a solicitação com a justificativa <justificativa>
      Então o resultado é "<resultado>", a situação passa a ser "<situacao>" e o histórico
        tem <etapas> etapa(s)
      E, nas recusas, a Dora não recebe notificação
      E, nas aceitações, a justificativa gravada na etapa, **lida de volta do banco**, é
        idêntica caractere a caractere à justificativa enviada

      Exemplos:
        | justificativa                                         | resultado | situacao          | etapas | # partição                |
        | ""                                                    | recusado  | aguardando gestor | 0      | vazia                     |
        | "   "                                                 | recusado  | aguardando gestor | 0      | só espaços                |
        | "Sem verba"                                           | aceito    | rascunho          | 1      | a menor válida            |
        | "Verba insuficiente — remanejar p/ o 2º trimestre 🙂" | aceito    | rascunho          | 1      | acento + emoji de 4 bytes |

    Esquema do Cenário: [CT-48] a etapa de diretor exige a justificativa pelas mesmas regras
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando diretor", com a etapa de
        gestor já decidida pelo Rui como "aprovada"
      Quando a Dora rejeita a solicitação com a justificativa <justificativa>
      Então o resultado é "<resultado>", a situação passa a ser "<situacao>" e o histórico
        tem <etapas> etapa(s)
      E, nas recusas, nenhuma etapa de diretor é gravada

      Exemplos:
        | justificativa            | resultado | situacao           | etapas | # partição     |
        | ""                       | recusado  | aguardando diretor | 1      | vazia          |
        | "   "                    | recusado  | aguardando diretor | 1      | só espaços     |
        | "Fora do orçamento anual"| aceito    | rascunho           | 2      | a menor válida |

    Cenário: [CT-20] a modal de rejeição não fecha sem o motivo
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      Quando o Rui confirma a modal "Rejeitar" sem preencher o motivo
      Então a modal aponta o erro no campo "justificativa"
      E a solicitação continua em "aguardando gestor", o histórico continua vazio, e a Dora
        não recebe notificação
```

**CT-19 é o cenário por fora do componente de UI de R6** (gate de camada da regra de validação de
domínio). O PRD é explícito sobre isso no passo 5.2 — *"a exigência vive aqui, não só no
`->required()` do campo"* —, e este é o cenário que a torna falsificável.

**"Ausente" e `null` não são expressáveis nesta camada**: a assinatura do método recebe `string`,
e omitir o argumento produz `ArgumentCountError`, que é erro de programação, não comportamento.
A partição existe onde ela é real — **no formulário**, e é CT-20.

**A linha unicode não é enfeite**: a justificativa é o único texto livre que uma pessoa escreve
sobre a decisão de outra, e ela vai para a tela (RQ-13). O `Então` afirma que o texto é gravado
**íntegro**, com acento e com o emoji de 4 bytes — uma coluna com colação errada ou um
`substr()` de saneamento aparecem aqui e em lugar nenhum mais.

> ⚠️ **A asserção de integridade foi acrescentada pela revisão adversarial** (achado nº 8), e o
> defeito era do tipo mais traiçoeiro: **a prosa mentia sobre o próprio Gherkin.** O parágrafo
> acima já dizia que o texto era afirmado íntegro; o `Então` afirmava resultado, situação e
> contagem de etapas, e **nunca o texto gravado**. O mutante M6.5 constava como morto por um
> cenário que não o matava — um falso ✅, que é pior que lacuna declarada, porque ninguém volta a
> olhar. A linha "lida de volta do banco" é o que fecha.

**CT-48 fecha o achado nº 3.** A-07 diz que o diretor também rejeita *"com a mesma exigência de
justificativa"* — e a versão anterior falsificava a exigência **só na etapa de gestor**. A única
rejeição por diretora era a linha `Dora | rejeitar | aceito` de CT-16, que fornece a justificativa
e afirma apenas resultado, situação e contagem. Uma implementação em que `rejeitar()` do gestor
valida e o ramo do diretor chama um `registrarEtapa()` genérico sem validação passava inteira.

> O conjunto aplicava **verbo irmão** (aprovar/rejeitar) em R5 e nunca aplicou **etapa irmã** a
> R6. R5 duplicou a matriz papel × verbo nas duas etapas (CT-15 e CT-16); R6 não duplicou nada.
> A regra generalizada, que vale para o resto deste arquivo: **onde há duas etapas, toda regra que
> vale "na decisão" precisa ser falsificada nas duas** — a segunda não herda a evidência da
> primeira, exatamente como o verbo irmão não herda a do outro verbo.

#### Mutantes previstos — R6

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6.1 | a exigência vive só no `->required()` do campo, e o model aceita `""` | CT-19 (linha vazia) |
| M6.2 | a validação usa `!== null` ou `isset()`, e `"   "` passa | CT-19 (linha só espaços) |
| M6.3 | a recusa acontece **depois** de gravar a etapa | CT-19 (asserção `etapas = 0` nas recusas) |
| M6.4 | a recusa acontece depois de transicionar para "rascunho" | CT-19 (asserção de situação nas recusas) |
| M6.5 | a justificativa é truncada ou saneada e perde acento e emoji | CT-19 (linha unicode, **lida de volta**) |
| M6.6 | a exigência de justificativa existe no ramo do gestor e não no do diretor | **CT-48** — revisão adversarial |
| M6.7 | o ramo do diretor recusa **depois** de gravar a etapa | **CT-48** (asserção `etapas = 1` nas recusas) |

---

## Regra R7 — a rejeição devolve ao rascunho preservando o histórico, e o reenvio recomeça pelo gestor

> `RQ-08`, `RQ-09` · área **A**, perfil **completo** · técnica: **tabela estado × evento,
> sequência de dois eventos (2-switch)**

```gherkin
  Regra: a solicitação rejeitada volta ao rascunho, o histórico sobrevive, e o reenvio
         recomeça pela etapa de gestor

    Cenário: [CT-21] a rejeição devolve a solicitação ao rascunho, com o motivo registrado
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI",
        com o histórico vazio
      Quando o Rui rejeita a solicitação com "Sem verba neste trimestre"
      Então a solicitação fica em "rascunho"
      E o histórico tem uma etapa: gestor/Rui/rejeitada/"Sem verba neste trimestre"
      E ninguém é notificado — nem a Ana, nem a Dora

    Cenário: [CT-47] o rascunho que voltou por rejeição continua editável
      Dado uma solicitação da Ana de "Notebooks", R$ 7.500,00, que o Rui rejeitou com
        "Sem verba neste trimestre" e que por isso está em "rascunho" com uma etapa
      Quando a Ana altera a descrição para "Notebooks (modelo mais barato)" e o valor para
        R$ 4.200,00, e salva
      Então a descrição e o valor gravados são os novos
      E a situação continua "rascunho", e o histórico continua com a etapa da rejeição

    Cenário: [CT-22] o reenvio recomeça pelo gestor, e o ciclo anterior continua no histórico
      Dado uma solicitação da Ana de R$ 7.500,00 que passou por "aguardando gestor" (Rui
        aprovou) e por "aguardando diretor" (Dora rejeitou com "Fornecedor não homologado"),
        e por isso está em "rascunho" com duas etapas
      Quando a Ana envia a solicitação de novo
      Então a solicitação fica em "aguardando gestor", e não em "aguardando diretor"
      E o histórico continua com as duas etapas do ciclo anterior
      E o Rui recebe uma notificação por e-mail

    Cenário: [CT-23] o segundo giro percorre as duas etapas de novo
      Dado a mesma solicitação de R$ 7.500,00 no segundo ciclo, em "aguardando gestor",
        com as duas etapas do ciclo anterior no histórico
      Quando o Rui aprova a etapa de gestor
      Então a solicitação fica em "aguardando diretor"
      E o histórico tem três etapas, em ordem cronológica, sendo a terceira gestor/Rui/aprovada
      E a Dora recebe uma notificação por e-mail
```

**Por que 2-switch e não uma transição por vez.** Quando um estado pode ser **reentrado**, cobrir
uma transição isolada não prova nada sobre o segundo giro — e é ali que mora o defeito, porque o
ciclo novo herda o que o anterior deixou. A sequência derivada é
`aguardando_diretor → rejeitar → rascunho → enviar → ?`, e o oráculo de CT-22 é sobre o **destino
do segundo envio** (`aguardando gestor`, não `aguardando diretor`) **e** sobre **quais registros
do ciclo anterior ainda contam** (as duas etapas continuam).

**CT-23 fecha o que CT-22 abre.** CT-22 prova que o reenvio volta ao gestor; CT-23 prova que a
etapa de gestor do primeiro ciclo **não é reaproveitada** — o Rui decide de novo, e a solicitação
volta a passar pelo diretor. Uma implementação que perguntasse *"já existe alguma etapa de
gestor aprovada?"* em vez de *"a etapa corrente foi decidida neste ciclo?"* passa em CT-22 e
morre em CT-23.

**CT-21 afirma o não-efeito de notificação com destinatário real**: a Ana e a Dora existem, e no
caminho feliz de uma aprovação a Dora seria notificada. A-11 é explícita — a rejeição não
notifica ninguém —, e sem essa asserção o mutante *"avisa o solicitante da rejeição"* fica vivo.

#### Mutantes previstos — R7

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M7.1 | a rejeição grava um estado `rejeitada` em vez de voltar a `rascunho` | CT-21 |
| M7.2 | o reenvio parte da etapa em que a solicitação estava (volta a `aguardando_diretor`) | CT-22 |
| M7.3 | o reenvio apaga o histórico do ciclo anterior | CT-22 |
| M7.4 | a rejeição notifica o solicitante | CT-21 |
| M7.5 | a etapa de gestor do ciclo anterior é reaproveitada, e o gestor não decide de novo | CT-23 |
| M7.6 | a justificativa é gravada na solicitação, não na etapa — e o reenvio a apaga | CT-22 (as duas etapas, com o motivo, continuam) |
| M7.7 | a guarda de "não mexer" é `$this->etapas()->exists()` em vez de `situacao === aprovada` — o rascunho **reentrado** fica travado e a correção é impossível | **CT-47** — revisão adversarial |
| M7.8 | a edição do rascunho reentrado apaga o histórico do ciclo anterior | **CT-47** |

> **CT-47 fecha o achado nº 2, que era o mais caro da revisão.** RQ-09 diz *"pro solicitante
> **corrigir** e enviar de novo"* — e a versão anterior marcava a cláusula como coberta por CT-22
> e CT-23, dos quais **um só reenvia e o outro só aprova**. O verbo "corrigir" não era executado
> por cenário nenhum do conjunto: a única edição testada (CT-06) partia de um rascunho **virgem**,
> com zero etapas.
>
> M7.7 é a implementação que isso deixava passar, e ela é a leitura **natural** de RQ-10 para quem
> quer barrar mexida depois que alguém já decidiu. Ela recusa exatamente o caso que RQ-09 exige, e
> ficava verde no conjunto inteiro. É também o achado que forçou a matriz a desdobrar `rascunho`
> em duas linhas — ver [a nota da contagem](#contagem--o-oráculo-da-própria-matriz).

---

## Regra R8 — `aprovada` é estado terminal

> `RQ-10` (A-05) · área **A**, perfil **completo** · técnica: **estado × operação**

Esta regra é coberta pela linha `aprovada` da matriz única — **CT-44**, um `Esquema` com as seis
operações de escrita. Não há cenário próprio, de propósito: escrever aqui uma segunda tabela para
o estado terminal é exatamente a decomposição que a skill proíbe, e ela custa cobertura (a
operação só apareceria nos estados que a regra dela já pressupõe).

#### Mutantes previstos — R8

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M8.1 | `aprovada` aceita nova aprovação — dupla aprovação | CT-44 (linha `aprovar`) |
| M8.2 | `aprovada` continua editável pelo dono | CT-44 (linha `editar`, que afirma o **valor gravado** inalterado) |
| M8.3 | `aprovada` pode ser cancelada | CT-44 (linha `cancelar`) |
| M8.4 | `aprovada` pode ser excluída | CT-44 (linha `excluir`) |
| M8.5 | `aprovada` pode ser reenviada, reabrindo o fluxo | CT-44 (linha `enviar`) |

---

## Regra R9 — o solicitante cancela enquanto a solicitação está em trânsito

> `RQ-11` (A-06) · área **A**, perfil **completo** · técnica: **estado × operação** + persona

```gherkin
  Regra: o solicitante cancela a própria solicitação enquanto ela está em trânsito

    Esquema do Cenário: [CT-24] o cancelamento depende do estado e de quem cancela
      Dado uma solicitação da Ana de R$ 7.500,00, no centro "TI", em "<estado>", cujo
        histórico tem <etapas_antes> etapa(s)
      Quando o <ator> cancela a solicitação
      Então o resultado é "<resultado>" e a situação passa a ser "<situacao>"
      E o histórico continua com <etapas_antes> etapa(s) — as que existiam **sobrevivem** e
        nenhuma nova é criada
      E ninguém é notificado — nem o Rui, nem a Dora

      Exemplos:
        | estado                | ator  | etapas_antes | resultado | situacao              | # célula                                   |
        | aguardando gestor     | Ana   | 0            | aceito    | cancelada             | em trânsito, solicitante                   |
        | aguardando diretor    | Ana   | **1** (Rui)  | aceito    | cancelada             | **em trânsito COM histórico**              |
        | rascunho (virgem)     | Ana   | 0            | recusado  | rascunho              | **@premissa A-06** — ali o verbo é excluir |
        | rascunho (reentrado)  | Ana   | 1            | recusado  | rascunho              | **@premissa A-06**, estado reentrante      |
        | aguardando gestor     | Rui   | 0            | recusado  | aguardando gestor     | gestor não cancela                         |
        | aguardando gestor     | Dora  | 0            | recusado  | aguardando gestor     | diretora não cancela                       |
        | aguardando gestor     | Bruno | 0            | recusado  | aguardando gestor     | terceiro                                   |
```

> ⚠️ **A coluna `etapas_antes` é o achado nº 6 da revisão adversarial, e ela conserta um falso ✅.**
> Na versão anterior, a linha `aguardando diretor` não declarava que a etapa do gestor existia, e
> o `Então` dizia *"o histórico não ganha nenhuma etapa"*. Contra um fixture de histórico vazio,
> **"não ganhou etapa" e "apagou o histórico" produzem o mesmo `count() === 0`** — a asserção era
> vácuo. Um `cancelar()` que fizesse `$this->etapas()->delete()` (raciocínio plausível: *"solicitação
> cancelada não tem trilha válida"*) atravessava a célula, e com ela a metade de RQ-13 que diz
> respeito a solicitações canceladas.
>
> O estado de partida agora é **alcançável pelo fluxo**: `aguardando_diretor` só existe depois de o
> gestor ter decidido, então uma fixture desse estado **com histórico vazio** era, além de cega,
> inconsistente com o próprio ciclo de vida.

**A linha `rascunho` é `@premissa` (A-06)**, e o invariante das duas leituras é afirmado na linha
seguinte do `Então` e na linha `cancelada` da matriz: **seja qual for a decisão sobre cancelar em
rascunho, a solicitação cancelada não volta ao fluxo** — nenhuma operação a reabre (CT-45). Se
A-06 for negada, essa linha inverte para "aceito / cancelada" e o invariante fica de pé.

**O `Então` afirma "nenhuma etapa" mesmo nas linhas aceitas.** Cancelar não é decisão de
aprovador, e uma implementação que registrasse o cancelamento como etapa poluiria o histórico que
RQ-13 exibe — sem que a asserção de situação percebesse.

**A linha `cancelada` da matriz é CT-45**, e não se repete aqui.

#### Mutantes previstos — R9

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M9.1 | cancelar é aceito em qualquer estado, inclusive `aprovada` | CT-24 (linha `rascunho`), CT-44 (linha `cancelar`) |
| M9.2 | qualquer pessoa da organização cancela | CT-24 (Rui, Dora, Bruno) |
| M9.3 | o aprovador da vez pode cancelar (confunde cancelar com rejeitar) | CT-24 (Rui) |
| M9.4 | o cancelamento grava uma etapa de decisão | CT-24 (a contagem **não sobe**) |
| M9.5 | a solicitação cancelada é reaberta pelo envio | CT-45 (linha `enviar`) |
| M9.6 | o cancelamento **apaga** o histórico ("cancelada não tem trilha válida") | **CT-24** (linha `aguardando diretor`, com `etapas_antes = 1`) — revisão adversarial |

---

## Regra R10 — a tela mostra a situação atual de cada solicitação

> `RQ-12` (A-12) · área **D**, perfil **padrão** · técnica: **EP exaustiva do enum** — 5 de 5

```gherkin
  Regra: a listagem mostra a situação atual de cada solicitação

    Esquema do Cenário: [CT-25] a listagem mostra a situação, qualquer que ela seja
      Dado uma solicitação da Ana de R$ 7.500,00, no centro "TI", em "<estado>", alcançada
        pelo fluxo e com <etapas> etapa(s) no histórico
      Quando a Ana abre a listagem de solicitações
      Então a coluna de situação daquela linha está com o estado <estado>
      E o rótulo **exibido** naquela linha não é vazio
      E a coluna de situação está visível

      Exemplos:
        | estado             | etapas | # partição do enum |
        | rascunho           | 0      | 1 de 5             |
        | aguardando gestor  | 0      | 2 de 5             |
        | aguardando diretor | 1      | 3 de 5             |
        | aprovada           | 2      | 4 de 5             |
        | cancelada          | 1      | 5 de 5             |

    Cenário: [CT-51] os cinco rótulos de situação são distintos entre si
      Dado cinco solicitações da Ana na mesma listagem, uma em cada situação do enum
      Quando a Ana abre a listagem de solicitações
      Então os cinco rótulos exibidos na coluna de situação são **distintos dois a dois**
```

**CT-51 existe porque `assertTableColumnStateSet` não observa a tela** — achado nº 7 da revisão
adversarial. Ele afirma o **estado que alimenta** a coluna, e o mutante que importa vive um
degrau depois: um `getLabel()` que devolva o mesmo texto — ou vazio — para "Aguardando gestor" e
"Aguardando diretor" mantém os estados distintos e **colapsa o que o usuário lê**. M10.2 constava
como morto por CT-25 e sobrevivia. Na versão anterior, três dos cinco rótulos ("Aguardando
diretor", "Aprovada", "Cancelada") **não eram vistos por olho nenhum em lugar algum do conjunto**,
e RQ-12 ficava sem cenário que a falsificasse.

**A distinção dois a dois é o oráculo certo aqui, e a escolha é deliberada.** Afirmar os textos
literais ("Aguardando diretor") adotaria como oráculo uma escolha que só o PRD determina —
recusada na `## Fronteira com o Plano`, pergunta A-19. Mas *"cinco situações produzem cinco
rótulos diferentes e nenhum vazio"* é consequência direta de RQ-12: se a tela mostra o status
atual, dois status distintos não podem parecer o mesmo. É falsificável, mata o colapso, e não
depende de tradução. **Se o negócio fixar os textos**, eles viram cláusula e CT-51 ganha os
valores literais.

**As fixtures agora são alcançáveis pelo fluxo** (coluna `etapas`): `aguardando_diretor` sem
etapa de gestor e `aprovada` sem etapa nenhuma eram estados que o ciclo de vida não produz, e
fixture inconsistente é oráculo que mede um mundo que não existe.

**A partição do enum é exaustiva, não amostrada.** Quando o usuário vê um rótulo derivado de um
enum de estado, **toda** partição é classe de equivalência obrigatória. Cobrir "Aguardando
gestor" e "Aprovada" e deixar "Aguardando diretor" de fora permite exatamente o defeito que
importa aqui: **a tela dizer "Aprovada" enquanto falta uma etapa**. O enum tem cinco casos, a
tabela tem cinco linhas — e um `Esquema` conta como 1 cenário.

**Os dois cenários são complementares, e nenhum basta sozinho**: CT-25 prova que **cada linha
carrega o estado certo** (o mapeamento registro → situação); CT-51 prova que **os estados chegam
distintos aos olhos** (o mapeamento situação → rótulo). O primeiro sem o segundo deixa o colapso
de rótulo vivo; o segundo sem o primeiro passaria com as cinco linhas trocadas entre si.

**Um `assertSee('Aprovada')` continua proibido como oráculo**, e por dois motivos: adota o texto
do PRD, e é frágil — o rótulo aparece em qualquer estado da página se estiver no layout. É
exatamente a armadilha que derrubou a âncora dos dois CT-B na primeira versão do `05`, onde o
`SelectFilter` de situação já renderiza os cinco rótulos no DOM antes de qualquer clique.

**`visualizar` da matriz é esta coluna** — as cinco células `✅` da última coluna são estas cinco
linhas, mais o detalhe de CT-26.

#### Mutantes previstos — R10

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M10.1 | a coluna lê um campo derivado desatualizado e mostra o estado anterior | CT-25 |
| M10.2 | o `getLabel()` devolve o mesmo texto para dois estados — "Aguardando diretor" vira "Aguardando gestor", ou vira "Aprovada" | **CT-51** (não CT-25: o estado continua distinto, só o rótulo colapsa) |
| M10.3 | a coluna existe mas nasce escondida (`toggleable` desligada por padrão) | CT-25 (`assertTableColumnVisible`) |
| M10.4 | o `getLabel()` devolve string vazia para os casos que ninguém olhou | **CT-51**, e CT-25 (rótulo não vazio) |

---

## Regra R11 — a tela mostra quem decidiu cada etapa, quando e por quê

> `RQ-13` (A-12) · área **D**, perfil **padrão** · técnica: **rastreio de efeito** (o histórico)
> + **ordenação com empate**

```gherkin
  Regra: a tela de visualização mostra o histórico completo das etapas de aprovação

    Cenário: [CT-26] o histórico mostra quem decidiu, o que decidiu, quando e por quê
      Dado uma solicitação da Ana de R$ 7.500,00 em "aguardando diretor", cujo histórico tem
        a rejeição da Dora com "Fornecedor não homologado" no primeiro ciclo e a aprovação
        do Rui nos dois ciclos
      Quando a Ana abre a página de visualização da solicitação
      Então a página mostra a situação atual "aguardando diretor"
      E o histórico mostra três linhas, cada uma com o nome de quem decidiu (Rui, Dora, Rui),
        a decisão, a data da decisão e, na linha da Dora, o texto "Fornecedor não homologado"

    Cenário: [CT-27] duas etapas gravadas no mesmo instante saem na ordem em que ocorreram
      Dado o tempo congelado num único instante
      E uma solicitação da Ana de R$ 7.500,00, aprovada pelo Rui e depois pela Dora nesse
        mesmo instante, com as duas etapas carimbadas com a mesma data e hora
      Quando a Ana abre a página de visualização da solicitação
      Então o histórico mostra a etapa de gestor (Rui) antes da etapa de diretor (Dora)

    Cenário: [CT-52] cada etapa exibe o próprio carimbo, não o da solicitação
      Dado uma solicitação da Ana criada em 03/08/2026
      E que o Rui aprovou a etapa de gestor em 05/08/2026 e a Dora aprovou a de diretor em
        11/08/2026
      Quando a Ana abre a página de visualização da solicitação
      Então a linha do Rui mostra 05/08/2026 e a linha da Dora mostra 11/08/2026
```

**CT-52 fecha o achado nº 11 da revisão adversarial.** CT-26 afirmava "a data da decisão" como
**presença**, nunca como valor — e CT-27, o único outro cenário temporal, **congela o tempo** e
portanto iguala todos os carimbos. O conjunto inteiro nunca exercitava etapas em instantes
**distintos**, e um infolist que exibisse `$solicitacao->created_at` (ou `now()`) em toda linha
passava nos dois. *"Quando"* é uma das três coisas que RQ-13 pede, ao lado de *"quem"* e do
motivo, e era a única sem oráculo de valor.

As datas escolhidas são discriminantes: **três** datas diferentes (criação, etapa 1, etapa 2), de
modo que exibir o carimbo da solicitação, exibir `now()` ou exibir sempre o carimbo da primeira
etapa produzem, cada um, um resultado diferente do esperado.

**CT-26 exige o nome, não a contagem.** *"O histórico tem três etapas"* é oráculo de banco e já
está em R7; o que RQ-13 pede é **quem aprovou cada etapa**, e isso só é observável com o nome na
tela. É também por isso que as personas são criadas com `User::create([...])` e nome explícito, e
não com `usuarioCom()` — seis pessoas chamadas "Teste" no histórico não distinguem nada.

**CT-27 — o parâmetro livre aqui é o instante, não o dado do formulário.** A janela em que as
duas implementações divergem é o **empate de carimbo**: com `timestamps()` gravando no segundo,
duas decisões próximas caem no mesmo valor, e uma ordenação por `created_at` sem desempate
determinístico devolve as etapas em ordem arbitrária. Escolher dois instantes distantes é o
equivalente temporal do valor redondo — o cenário passaria sem provar nada. `freezeTime()` põe o
teste dentro da janela de propósito.

> Esta é a **única** entrada do tempo nesta feature, e é por isso que a linha "Timezone / DST" do
> checklist de taxonomia é `não se aplica` em vez de lacuna: não há prazo, expiração nem
> agendamento; nenhuma decisão lê a data. O que o tempo decide aqui é **ordem**, e ordem é CT-27.

#### Mutantes previstos — R11

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11.1 | o histórico mostra só a última etapa | CT-26 |
| M11.2 | o histórico mostra a decisão sem quem decidiu | CT-26 |
| M11.3 | a justificativa da rejeição não é exibida | CT-26 |
| M11.4 | a ordenação é por `created_at` sem desempate, e etapas do mesmo segundo saem invertidas | CT-27 |
| M11.5 | o histórico é ordenado do mais recente para o mais antigo, invertendo a leitura do fluxo | CT-26, CT-27 |
| M11.6 | cada linha do histórico exibe `$solicitacao->created_at` ou `now()` em vez do carimbo da própria etapa | **CT-52** — revisão adversarial |

---

## Regra R12 — só o próximo aprovador é notificado, e por e-mail

> `RQ-14` (A-11) · área **C**, perfil **padrão** · técnica: **rastreio de efeito**, quatro
> direções + **cardinalidade do destinatário (0/1/N)**
>
> **Teto**: 4 cenários numa área `padrão` cujo teto é 3. **Não é estouro**: a técnica de rastreio
> de efeito exige três cenários obrigatórios — aconteceu, não aconteceu quando não devia,
> aconteceu uma só vez — e um quarto quando a atomicidade importa. É o custo declarado da técnica,
> e ela não divide o teto com fronteira nem com partição.

```gherkin
  Regra: ao mudar de etapa, só o próximo aprovador é notificado — e por e-mail

    Cenário: [CT-28] o envio notifica o gestor, e só ele
      Dado uma solicitação da Ana de R$ 7.500,00, em "rascunho", no centro "TI"
      Quando a Ana envia a solicitação
      Então o Rui recebe uma notificação de aprovação pendente pelo canal "mail"
      E nem a Dora nem a Ana recebem notificação

    Esquema do Cenário: [CT-29] o número de diretores decide se a etapa pode ser aberta
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      E a Acme com <diretores> pessoa(s) no papel "diretor"
      Quando o Rui aprova a etapa de gestor
      Então o resultado é "<resultado>" e a situação passa a ser "<situacao>"
      E o histórico tem <etapas> etapa(s), e nenhuma delas é de diretor
      E as notificações enviadas são: <notificados>

      Exemplos:
        | diretores            | resultado | situacao           | etapas | notificados                              |
        | 1 (Dora)             | aceito    | aguardando diretor | 1      | a Dora, pelo canal "mail", uma vez       |
        | 3 (Dora, Elis, Fábio)| aceito    | aguardando diretor | 1      | os três, pelo canal "mail", uma vez cada |
        | 0                    | recusado  | aguardando gestor  | **0**  | ninguém — **e a Ana também não**         |

    Cenário: [CT-30] a decisão repetida não grava duas etapas nem reenvia o e-mail
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      E o Rui com duas cópias da mesma solicitação carregadas, uma em cada aba, ambas lidas
        antes de qualquer decisão
      E que o Rui já aprovou pela primeira cópia
      Quando o Rui aprova pela segunda cópia
      Então a segunda tentativa é recusada
      E a solicitação persistida está em "aguardando diretor", com exatamente uma etapa de
        gestor no histórico
      E a Dora recebeu exatamente uma notificação

    Cenário: [CT-31] o e-mail não sobrevive a uma gravação que falha
      Dado uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      E a Dora como diretora da Acme, que seria notificada no caminho feliz
      E a gravação da etapa de aprovação configurada para falhar
      Quando o Rui aprova a etapa de gestor
      Então a operação falha
      E a solicitação continua em "aguardando gestor", o histórico continua vazio, e a Dora
        não recebe notificação
```

**CT-28 e CT-29 afirmam o canal, e isso é o que discrimina.** *"Uma notificação foi enviada"*
passa com o efeito saindo por `database` — e RQ-14 diz **"notificar por e-mail"**. A asserção
carrega o predicado de canal:
`fn ($notification, array $channels) => in_array('mail', $channels, true)`.

**CT-29, linha `0` — e por que ela não serve de prova de nada além dela mesma.** É a partição de
zero destinatários, é `@premissa` de comportamento nova (**A-13**), e a direção vem de falha
fechado — a mesma que o próprio `00` já fixou em A-10 para o gestor ausente. O `Então` dela **não
é citado em lugar nenhum** como prova de não-efeito ou de atomicidade: num mundo sem diretores, o
mutante e a implementação correta produzem o mesmo observável quanto à Dora. O que essa linha
afirma é que **a Ana** — que existe — também não é notificada, e que a situação **não avança**.
**O invariante de A-13 agora está no `Então`, e não só na prosa da pergunta** — achado nº 12 da
revisão adversarial. Nenhuma das três linhas afirmava o histórico, e é a coluna `etapas` que
carrega o invariante: *uma solicitação acima do limite nunca chega a `aprovada` sem uma etapa de
diretor gravada*. Sem ela, duas implementações defeituosas passavam: com 0 diretores, recusar
**depois** de gravar a etapa de gestor; e, com 1 diretora, gravar **duas** etapas de gestor. O
invariante escrito em prosa e ausente do cenário é exatamente o que a auditoria de premissas
proíbe. **Se A-13 for negada, CT-29 (linha 0) inverte** para "aceito / aguardando diretor /
1 etapa / ninguém", e o invariante permanece de pé.

**CT-30 ancora no agregado persistido.** O oráculo é o estado no banco, a contagem de etapas e a
contagem de notificações — não o retorno das duas chamadas. Duas cópias lidas antes de qualquer
decisão é a forma de reproduzir, em processo único, a leitura obsoleta que o `UPDATE` condicional
existe para barrar: com `get()` + `save()`, a segunda cópia venceria e gravaria a segunda etapa.

> **Limite declarado de CT-30**: a corrida **real** (dois processos simultâneos) não é reprodutível
> no arnês deste projeto — sqlite `:memory:` vive dentro do processo do teste, `--parallel`
> distribui arquivos e não requisições ao mesmo registro, e `pcntl_fork` não existe no ambiente
> Windows do projeto. Foi tentado antes de declarar. O que CT-30 falsifica é o **check-then-act**,
> que é o mecanismo do defeito; o que ele não falsifica é o isolamento transacional do banco real.

**CT-31 é a atomicidade, e cumpre as duas condições juntas.** A falha é induzida **depois do ponto
do efeito** — depois das barreiras e depois da transição de situação, na gravação da etapa, por um
evento de model que lança — e **o destinatário é real**: a Dora existe e seria notificada no
caminho feliz. Afirmar ausência num caminho de pré-validação (justificativa vazia, ator errado)
seria falso ✅ pelo outro lado, e é por isso que esse cenário não reaproveita nenhuma das recusas
já escritas.

#### Mutantes previstos — R12

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M12.1 | a notificação sai por `database` (sino do Filament) em vez de `mail` | CT-28, CT-29 (canal afirmado) |
| M12.2 | todos os aprovadores do fluxo são notificados de uma vez no envio; ou o solicitante é notificado a cada passo | CT-28, CT-21, CT-14 |
| M12.3 | a notificação é despachada antes da gravação e sobrevive ao rollback | CT-31 |
| M12.4 | a segunda decisão reenvia a notificação ao próximo aprovador | CT-30 |
| M12.5 | com zero diretores, a solicitação vai a "aprovada" sem etapa de diretor | CT-29 (linha `0`) |

---

## Regra R13 — centro de custo é entidade de administração: o usuário comum não escolhe quem aprova

> `RQ-04` (A-08) · área **B**, perfil **completo** · técnica: **matriz papel × ação**
>
> Esta regra existe por uma escalada de privilégio concreta: **quem edita
> `centros_custo.gestor_id` se nomeia gestor e aprova as próprias compras.** E ela não gera erro
> nenhum quando esquecida — os dois seeders rodam, a suíte fica verde, e todo usuário comum vira
> administrador da organização (`.ai/rules/filament.md`, `wikis/convencoes.md`).

```gherkin
  Regra: administrar centros de custo é privilégio de administração, não do usuário comum

    Esquema do Cenário: [CT-32] a matriz de permissões separa o negócio da administração
      Dado os seeders de permissões e de papéis executados
      Quando se consultam as permissões do papel <papel>
      Então ele <tem_solicitacao> a permissão "Create:SolicitacaoCompra"
      E ele <tem_centro> a permissão "Update:CentroCusto"

      Exemplos:
        | papel             | tem_solicitacao | tem_centro | # papel                          |
        | panel_user        | tem             | não tem    | usuário comum do negócio         |
        | diretor           | tem             | não tem    | papel novo, mesma matriz         |
        | admin_organizacao | tem             | tem        | administra a organização inteira |

    Cenário: [CT-33] o usuário comum é barrado na tela de centros de custo
      Dado o Bruno com o papel "panel_user" na Acme
      Quando o Bruno abre a listagem de centros de custo
      Então o acesso é negado com 403
      E a Ana, também "panel_user", abre a listagem de solicitações sem ser barrada

    Cenário: [CT-34] o usuário comum é barrado também por fora do componente
      Dado o Bruno com o papel "panel_user" na Acme
      Quando o Bruno requisita a rota de edição do centro "TI"
      Então a resposta é 403

    Cenário: [CT-35] o papel diretor entra no painel e enxerga o que precisa decidir
      Dado a Dora com o papel "diretor" na Acme
      E uma solicitação da Ana de R$ 7.500,00 em "aguardando diretor"
      Quando a Dora abre a listagem de solicitações no painel /app
      Então a solicitação aparece na listagem
      E as ações "Aprovar" e "Rejeitar" estão visíveis para ela
```

**CT-32 é o cenário que o `00` nomeia em A-08** e o PRD em CT-14/ADR-06. A linha
`panel_user / tem / não tem` é a barreira contra a escalada; a coluna `tem_solicitacao` é o
espelho dela, e existe porque **numa subtração o erro do substring é invertido**: casar por
`str_contains($p, 'Custo')` ou por um FQCN errado tiraria de quem deveria ter. A linha `diretor`
cobre o papel novo, que herda a mesma matriz — a autoridade de aprovar **não é permissão**.

> ⚠️ **Correção da revisão adversarial (achado nº 15).** As duas versões anteriores de CT-33 e
> CT-34 terminavam com *"E o gestor do centro 'TI' continua sendo o Rui"* — uma **asserção de
> ausência sem alvo**. Abrir uma listagem e requisitar uma rota `GET` **não escrevem `gestor_id`
> em implementação nenhuma**, correta ou defeituosa: a asserção não distinguia nada e vestia os
> cenários de rastreio de efeito sem sê-lo. Era o mesmo falso ✅ que a própria skill descreve, na
> versão mais fácil de cometer — o não-efeito parece rigor. O oráculo real desses dois cenários é
> o **403**, e agora é só ele.
>
> CT-33 ganhou em troca um **controle positivo**: a Ana, com o **mesmo papel** `panel_user`, não é
> barrada na tela de solicitações. Sem ele, um 403 causado por qualquer motivo — permission
> ausente para todo mundo, painel mal registrado, policy negando tudo — passaria como se fosse a
> subtração funcionando.

**CT-34 é o cenário por fora do componente de UI de R13** — o que é possível neste stack. E aqui
há uma **lacuna declarada**, porque o gate pede mais do que o Filament oferece:

> **Lacuna declarada — a escrita em `CentroCusto` por fora do componente.** Em Filament toda
> escrita passa pelo componente Livewire: não existe rota `PUT`/`POST` própria a que se possa
> requisitar diretamente. Tentado antes de declarar: (a) requisição HTTP à rota de edição — é `GET`,
> e prova o 403 mas não a escrita, e é o que CT-34 faz; (b) `Livewire::test(EditCentroCusto::class)`
> como Bruno — continua sendo o componente; (c) chamar `CentroCusto::update(['gestor_id' => …])`
> direto — **passa**, porque a proteção de `CentroCusto` é inteiramente de permissão (policy +
> subtração no seeder) e **não há asserção de identidade no model**, ao contrário de
> `SolicitacaoCompra`. Isso não é falha do cenário: é a superfície real. **Pergunta ao usuário**:
> um comando, job ou seeder futuro que altere `gestor_id` deve ser barrado pelo domínio, como
> `Convite::exigirDono()` faz? Se sim, é uma cláusula nova e um cenário novo.

#### Mutantes previstos — R13

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M13.1 | `CentroCustoResource` esquecido em `permissoesDeAdministracaoDoApp()` | CT-32 (linha `panel_user`), CT-33 |
| M13.2 | a subtração casa por substring e remove também as permissões de `SolicitacaoCompra` | CT-32 (coluna `tem_solicitacao`) |
| M13.3 | o papel `diretor` recebe a matriz inteira do painel, sem a subtração | CT-32 (linha `diretor`) |
| M13.4 | o papel `diretor` nasce sem `roles.painel = 'app'` e leva 403 nos três painéis | CT-35 |
| M13.5 | `SolicitacaoCompraResource` entra na lista de administração por engano, e o usuário comum fica sem a própria feature | CT-32 (coluna `tem_solicitacao`) |

---

## Regra R14 — solicitação de uma organização não é vista nem operada de outra

> **Sem `RQ` de origem** — vem do checklist de taxonomia (IDOR / dado de outro tenant) e da
> premissa de mecanismo do PRD (`BelongsToTenant`) · área **B**, perfil **completo**
>
> Suíte **`FeatureTenancy`** — ⚠️ **a pasta, o bloco no `tests/Pest.php` e a testsuite no
> `phpunit.xml` não existem** (passo 10 do PRD). Sem os três, estes dois cenários **passam por
> não serem varridos**.

```gherkin
  Regra: solicitação de uma organização não é acessível de outra

    Esquema do Cenário: [CT-36] o dado de outra organização não é lido nem operado
      Dado a Ana com uma solicitação de R$ 7.500,00 na Acme, em "aguardando gestor"
      E o Téo com o papel "panel_user" na Globex
      E uma solicitação do Téo de R$ 3.000,00 na Globex, em "aguardando gestor"
      Quando o Téo <operacao>
      Então o resultado é "<resultado>"
      E a solicitação da Acme continua em "aguardando gestor", com o histórico vazio

      Exemplos:
        | operacao                                              | resultado                                            |
        | abre a listagem de solicitações da Globex             | **vê a solicitação da Globex e não vê a da Acme**    |
        | abre a URL da solicitação da Acme pelo uuid           | 404                                                  |
        | abre a URL da solicitação da Globex pelo uuid         | **200, e a página é a da solicitação dele**          |
        | aprova a solicitação da Acme chamando o model direto  | recusado                                             |

    Cenário: [CT-55] a solicitação não referencia centro de custo de outra organização
      Dado o centro "Suprimentos" pertencente à Globex
      Quando a Ana, da Acme, grava uma solicitação de R$ 7.500,00 apontando para esse centro
      Então a gravação é recusada
      E nenhuma solicitação da Acme referencia um centro da Globex

    Cenário: [CT-37] os diretores são resolvidos na organização da solicitação
      Dado a Dora com o papel "diretor" apenas na Acme
      E a Elza com o papel "diretor" apenas na Globex
      E uma solicitação de R$ 7.500,00 na Globex, em "aguardando gestor", cujo gestor é o Téo
      Quando o Téo aprova a etapa de gestor
      Então só a Elza recebe a notificação, pelo canal "mail"
      E a Dora não recebe notificação
```

**CT-36, última linha, é o que a rota não prova.** O 404 do route binding vem do escopo global de
`BelongsToTenant`; a chamada direta ao model é o caminho que um job, comando ou rota de API futura
tomaria — e é ali que o escopo global pode não estar aplicado.

> ⚠️ **As linhas de controle positivo são o achado nº 14 da revisão.** A versão anterior afirmava
> *"a solicitação não aparece"* numa listagem onde **não existia nenhuma solicitação da Globex** —
> uma listagem vazia por qualquer motivo passava: escopo filtrando pelo `tenant_id` errado, policy
> negando tudo, 403 renderizado como página em branco. É a mesma família do não-efeito sem
> destinatário, aplicada a leitura em vez de escrita. Agora o Téo **tem** uma solicitação, e o
> `Então` afirma o par: **vê a dele, não vê a da Acme**. O mesmo vale para o uuid — 404 no alheio,
> 200 no próprio.

**CT-55 protege a referência, e não o registro** — achado nº 9. CT-36 e CT-37 protegem o
**registro** contra leitura e operação de fora; ninguém testava a **chave estrangeira**. Se o
recorte por organização viver na consulta do `Select` do formulário e não no model, uma
solicitação da Acme pode nascer apontando para um centro da Globex — e aí **o gestor da Globex
passa a aprovar compra da Acme**, por dentro de todas as barreiras, porque o registro é
legitimamente da Acme e o aprovador é legitimamente o gestor do centro que ela referencia. É a
mesma escalada de A-08 por uma terceira porta.

**CT-37 é o risco que o PRD nomeia em ADR-08.** Com `permission.teams` ligado, `role('diretor')`
filtra pelo team fixado no `PermissionRegistrar`, e quem o fixa é o middleware — que **não roda
num worker de fila**. Resolver os destinatários dentro da notificação enfileirada devolveria os
diretores da organização errada, ou nenhum. As duas diretoras existem, em organizações
diferentes: é essa configuração que torna o defeito observável, e não uma diretora só.

#### Mutantes previstos — R14

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M14.1 | o escopo por organização não é aplicado, e a listagem mostra a base inteira | CT-36 (primeira linha) |
| M14.2 | a rota resolve pelo uuid sem o escopo, e devolve o registro de outra organização | CT-36 (segunda linha) |
| M14.3 | o escopo existe na query da tela e não no model — a chamada direta atravessa | CT-36 (terceira linha) |
| M14.4 | os diretores são resolvidos sem contexto de organização (todos os da instalação) | CT-37 |
| M14.5 | os diretores são resolvidos dentro do job enfileirado, fora do contexto do request | CT-37 |
| M14.6 | o escopo por organização é aplicado ao **registro** e não à **FK**: a solicitação aponta para um centro de outra organização, e o gestor de lá aprova | **CT-55** — revisão adversarial |
| M14.7 | o escopo filtra por um `tenant_id` errado e **todo mundo vê zero registros** — a listagem vazia parece isolamento funcionando | **CT-36** (controle positivo) — revisão adversarial |

---

## Regra R15 — o centro de custo é cadastrado com nome e gestor

> `RQ-04` (A-01) · área **E**, perfil **mínimo** · técnica: CRUD + **unicidade contra o próprio
> registro**
>
> **Teto estourado com justificativa**: 2 cenários numa área de teto 1. O gate de tela de escrita
> cobra gravação por componente para **toda** rota `create`/`edit` da `## Superfície de UI`, e são
> duas. Uma tela aberta não é uma tela que grava.

```gherkin
  Regra: o centro de custo é cadastrado com nome e gestor

    Cenário: [CT-38] o cadastro grava o nome, o gestor e a organização
      Dado a administradora da organização Acme no formulário de novo centro de custo
      Quando ela grava o centro "Marketing" com a Carla como gestora
      Então existe um centro chamado "Marketing", com a Carla como gestora, na Acme

    Cenário: [CT-39] salvar sem alterar o nome continua funcionando
      Dado o centro "TI" da Acme, cujo gestor é o Rui
      Quando a administradora da organização salva o mesmo centro trocando só o gestor para
        a Carla, sem tocar no nome
      Então o centro "TI" é gravado com a Carla como gestora
```

**CT-39 é a armadilha da edição**, e está escrito de forma **neutra quanto à unicidade**: o
requisito não pede que o nome do centro seja único, e a regra `scopedUnique(ignoreRecord: true)`
é escolha do PRD, recusada como oráculo na `## Fronteira com o Plano`. O oráculo aqui é só a
gravação — que **vale exista ou não** a regra de unicidade. Se ela existir e for ingênua, o save
acusa colisão do registro com ele próprio e o cenário fica vermelho; se não existir, ele fica
verde. Nos dois casos o cenário mede a coisa certa.

**CT-38 afirma a organização gravada**, e não só nome e gestor: `tenant_id` vem da trait
`BelongsToTenant`, não do formulário, e `assertDatabaseHas` só com a chave primária passaria com
todos os outros campos errados.

#### Mutantes previstos — R15

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M15.1 | a unicidade do nome não ignora o próprio registro, e salvar sem alterar acusa colisão | CT-39 |
| M15.2 | o `gestor_id` não é gravado (o `Select` salva sem a relação) | CT-38, CT-39 |
| M15.3 | o `tenant_id` vem do formulário em vez da trait | CT-38 |

---

## Regra R16 — nenhuma operação fora do ciclo de vida altera a solicitação

> `RQ-02`, `RQ-03`, `RQ-05`, `RQ-06`, `RQ-10`, `RQ-11` · área **A**, perfil **completo** ·
> técnica: **matriz estado × operação**, produto cartesiano fechado
>
> **Teto estourado com justificativa**: 8 cenários contra um teto de 5. A matriz tem **24 células
> inválidas** e o perfil `completo` exige 100% delas; a alternativa a estes `Esquema` seriam 24
> cenários avulsos. Um `Esquema` conta como 1 cenário, e sem esta regra o teto e a exigência de
> cobertura seriam aritmeticamente incompatíveis. Dois dos oito (CT-46 e CT-56) vieram da revisão
> adversarial, e um terceiro (CT-40) foi desdobrado por ela.

Todos os cenários abaixo compartilham o mundo do `Contexto`: solicitação de **R$ 7.500,00**
(acima do limite, portanto **com segunda etapa**), centro "TI" com o Rui como gestor, a Dora como
diretora da Acme. É essa configuração que faz cada asserção de ausência discriminar.

```gherkin
  Regra: nenhuma operação fora do ciclo de vida altera a solicitação

    Esquema do Cenário: [CT-40] o rascunho é excluído, virgem ou reentrado
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro "TI", com
        <etapas> etapa(s) no histórico
      Quando a Ana exclui a solicitação
      Então a solicitação deixa de existir
      E as <etapas> etapa(s) dela também deixam de existir

      Exemplos:
        | etapas | # célula da matriz                                     |
        | 0      | rascunho (virgem) × excluir                            |
        | 1      | rascunho (reentrado) × excluir — rejeitado pelo Rui    |

    Cenário: [CT-56] a solicitação excluída não volta a operar
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro "TI", já excluída
      E a cópia dela ainda carregada em memória
      Quando a Ana envia a solicitação a partir dessa cópia
      Então a operação é recusada
      E nenhuma linha de solicitação é recriada, e o Rui não recebe notificação

    Esquema do Cenário: [CT-41] rascunho não se aprova nem se rejeita
      Dado uma solicitação da Ana em "rascunho", de R$ 7.500,00, no centro "TI", com
        <etapas> etapa(s) no histórico
      Quando o <ator> executa "<operacao>" sobre ela
      Então a operação é recusada
      E a situação continua "rascunho", o histórico continua com <etapas> etapa(s), e a Dora
        não recebe notificação

      Exemplos:
        | ator | operacao | etapas | # célula da matriz                 |
        | Rui  | aprovar  | 0      | rascunho (virgem) × aprovar        |
        | Rui  | rejeitar | 0      | rascunho (virgem) × rejeitar       |
        | Rui  | aprovar  | 1      | **rascunho (reentrado) × aprovar** |
        | Rui  | rejeitar | 1      | **rascunho (reentrado) × rejeitar**|

    Cenário: [CT-46] mudar o centro de custo em trânsito não troca quem aprova
      Dado o centro "Compras", cuja gestora é a própria Ana
      E uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", no centro "TI"
      Quando a Ana altera o centro de custo da solicitação para "Compras"
      Então a operação é recusada
      E o centro gravado continua sendo "TI", a situação continua "aguardando gestor" e o
        histórico continua vazio
      E a Ana aprovando essa solicitação continua sendo recusada, enquanto o Rui aprovando
        é aceito

    Esquema do Cenário: [CT-42] em "aguardando gestor" não se edita, não se exclui, não se reenvia
      Dado uma solicitação da Ana em "aguardando gestor", "Notebooks", R$ 7.500,00, no centro "TI"
      Quando a Ana executa "<operacao>" sobre ela
      Então a operação é recusada
      E a situação continua "aguardando gestor", a solicitação ainda existe, e os três campos
        gravados continuam "Notebooks", R$ 7.500,00 e o centro "TI"
      E <nao_efeito>

      Exemplos:
        | operacao                              | nao_efeito                        | # célula                     |
        | editar o valor para R$ 100,00         | —                                 | aguardando_gestor × editar   |
        | **editar o centro para "Compras"**    | —                                 | aguardando_gestor × editar   |
        | editar a descrição para "Cadeiras"    | —                                 | aguardando_gestor × editar   |
        | excluir                               | —                                 | aguardando_gestor × excluir  |
        | enviar                                | o Rui não recebe nova notificação | aguardando_gestor × enviar   |

    Esquema do Cenário: [CT-43] em "aguardando diretor" não se edita, não se exclui, não se reenvia
      Dado uma solicitação da Ana em "aguardando diretor", "Notebooks", R$ 7.500,00, no centro
        "TI", com a etapa de gestor já decidida pelo Rui
      Quando a Ana executa "<operacao>" sobre ela
      Então a operação é recusada
      E a situação continua "aguardando diretor", a solicitação ainda existe, os três campos
        gravados continuam "Notebooks", R$ 7.500,00 e o centro "TI", e o histórico continua
        com uma etapa
      E <nao_efeito>

      Exemplos:
        | operacao                              | nao_efeito                   | # célula                      |
        | editar o valor para R$ 100,00         | —                            | aguardando_diretor × editar   |
        | **editar o centro para "Compras"**    | —                            | aguardando_diretor × editar   |
        | editar a descrição para "Cadeiras"    | —                            | aguardando_diretor × editar   |
        | excluir                               | —                            | aguardando_diretor × excluir  |
        | enviar                                | o Rui não recebe notificação | aguardando_diretor × enviar   |

    Esquema do Cenário: [CT-44] a solicitação aprovada não aceita mais nada
      Dado uma solicitação da Ana em "aprovada", "Notebooks", R$ 7.500,00, no centro "TI",
        com as duas etapas decididas (Rui e Dora)
      Quando o <ator> executa "<operacao>" sobre ela
      Então a operação é recusada
      E a situação continua "aprovada", a solicitação ainda existe, os três campos gravados
        continuam "Notebooks", R$ 7.500,00 e o centro "TI", e o histórico continua com as
        duas etapas
      E <nao_efeito>

      Exemplos:
        | ator | operacao                            | nao_efeito                   | # célula            |
        | Ana  | editar o valor para R$ 100,00       | —                            | aprovada × editar   |
        | Ana  | **editar o centro para "Compras"**  | —                            | aprovada × editar   |
        | Ana  | excluir                             | —                            | aprovada × excluir  |
        | Ana  | enviar                              | o Rui não recebe notificação | aprovada × enviar   |
        | Dora | aprovar                             | ⚑ ver ressalva               | aprovada × aprovar  |
        | Dora | rejeitar                            | —                            | aprovada × rejeitar |
        | Ana  | cancelar                            | —                            | aprovada × cancelar |

    Esquema do Cenário: [CT-45] a solicitação cancelada não volta ao fluxo
      Dado uma solicitação da Ana de "Notebooks", R$ 7.500,00, no centro "TI", que passou por
        "aguardando diretor" (o Rui aprovou) e foi cancelada pela Ana — portanto em
        "cancelada", com uma etapa no histórico
      Quando o <ator> executa "<operacao>" sobre ela
      Então a operação é recusada
      E a situação continua "cancelada", a solicitação ainda existe, os três campos gravados
        continuam "Notebooks", R$ 7.500,00 e o centro "TI", e o histórico continua com a
        etapa que tinha
      E <nao_efeito>

      Exemplos:
        | ator | operacao                            | nao_efeito                   | # célula             |
        | Ana  | editar o valor para R$ 100,00       | —                            | cancelada × editar   |
        | Ana  | **editar o centro para "Compras"**  | —                            | cancelada × editar   |
        | Ana  | excluir                             | —                            | cancelada × excluir  |
        | Ana  | enviar                              | o Rui não recebe notificação | cancelada × enviar   |
        | Rui  | aprovar                             | ⚑ ver ressalva               | cancelada × aprovar  |
        | Rui  | rejeitar                            | —                            | cancelada × rejeitar |
        | Ana  | cancelar                            | —                            | cancelada × cancelar |
```

**A legenda foi conferida célula a célula, e é isso que a torna uma asserção e não um enfeite.**
Cada `❌` afirma **todos** os efeitos que **aquela** operação dispara no caminho feliz, e nada
além:

- as células de **`aprovar`** afirmam **três** coisas — situação, histórico e a notificação à
  Dora —, porque aprovar dispara as três. Uma coluna de `aprovar` sem o não-efeito de notificação
  tornaria a legenda falsa e a contagem de células não auditável;
- as células de **`enviar`** afirmam situação **e** a notificação ao Rui, porque enviar notifica;
- as células de **`rejeitar`** afirmam situação **e** histórico, e **não** afirmam notificação —
  a rejeição não notifica ninguém no caminho feliz (A-11), e exigi-lo seria asserção de vácuo;
- as células de **`cancelar`** afirmam situação **e o histórico que já existia**;
- as células de **`editar`** afirmam **os três campos gravados** — descrição, valor **e centro de
  custo**, este último porque decide **quem aprova**;
- as células de **`excluir`** afirmam que o registro **ainda existe** e que as etapas dele também.

⚑ **Ressalva das células `aprovada × aprovar` e `cancelada × aprovar`**: ali não há próximo
aprovador, então "a Dora não é notificada" seria **vácuo** — o mutante e a implementação correta
produzem o mesmo observável. Essas duas células são resolvidas por **situação e histórico**, e é
assim que a tabela de mutantes as credita. Escrever a asserção de notificação ali por simetria
seria decorativa; deixá-la implícita e contá-la como cobertura seria a legenda voltando a mentir.

**A dimensão do campo é exercitada fora do estado inicial**, e agora com **dois** campos decisivos:
CT-42…CT-45 alteram o **valor** (que decide a alçada) **e o centro de custo** (que decide o
aprovador). Trocar o campo decisivo só em `rascunho`, onde tudo é editável, deixaria os dois
defeitos sem cenário justamente nos estados em que eles importam.

**CT-46 é a cadeia inteira, e é o achado nº 1 da revisão adversarial.** A célula
`aguardando_gestor × editar` recusar a troca de centro é uma coisa; a **consequência** de ela não
recusar é outra, e é ela que o cenário exibe: a Ana move a solicitação para um centro do qual é
gestora e **aprova a si mesma** — com CT-17 abençoando solicitante = gestor por A-09, o que torna a
etapa resultante indistinguível de uma legítima. É a escalada de privilégio que A-08 descreve, por
uma porta que A-08 não olhou: não é preciso editar `centros_custo.gestor_id` se dá para mover a
solicitação para um centro cujo gestor já se é. A última linha do `Então` é o que fecha a cadeia —
recusar a edição **e** continuar recusando a aprovação pela Ana.

**CT-40 e CT-56 eram um cenário só, e ele tinha dois `Quando`.** O segundo `E` do `Então` original
executava uma **operação nova** ("enviar a partir da cópia em memória é recusado") — um `Quando`
disfarçado de asserção, achado nº 17. Separados: **CT-40** é a célula válida da coluna `excluir`,
agora nas duas proveniências de `rascunho`; **CT-56** é o item de taxonomia *"o registro removido
ainda funciona?"*. A premissa de mecanismo do PRD é que a exclusão é **física** — sem `SoftDeletes`
—, e ela fixa **como** o cenário é escrito, não dispensa escrevê-lo. Com `save()`, uma transição
sobre um registro apagado afeta zero linhas e **não acusa nada**; com o `UPDATE` condicional, ela
falha. É a diferença que CT-56 mede.

#### Mutantes previstos — R16

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M16.1 | aprovar/rejeitar não verificam a situação de partida, e um rascunho é aprovado | CT-41 |
| M16.2 | a policy barra a edição pela tela, mas o model aceita editar depois do envio | CT-42, CT-43 |
| M16.3 | o valor é alterado durante o trânsito sem que a alçada seja reavaliada | CT-42, CT-43 (o **valor gravado** é o oráculo, não só a recusa) |
| M16.4 | o reenvio é aceito em qualquer estado e reabre o fluxo | CT-42, CT-43, CT-44, CT-45 (linhas `enviar`) |
| M16.5 | a transição é recusada **depois** de gravar a etapa — uma aprovação registrada e não aplicada | CT-41, CT-44, CT-45 (asserção de histórico) |
| M16.6 | a transição é recusada depois de notificar o próximo aprovador | CT-41, CT-42 (asserções de notificação com destinatário real) |
| M16.7 | a exclusão física deixa a cópia em memória operante, e a transição recria a linha | **CT-56** |
| M16.8 | o guard de edição em trânsito filtra só o `valor`, e `centro_custo_id` continua mutável | **CT-42, CT-43, CT-46** — revisão adversarial |
| M16.9 | a guarda de "não mexer" usa `$this->etapas()->exists()`, e o rascunho reentrado é aprovável | **CT-41** (linhas com `etapas = 1`) — revisão adversarial |
| M16.10 | a exclusão não cascateia, e as etapas ficam órfãs apontando para uma solicitação inexistente | **CT-40** (linha `etapas = 1`) — revisão adversarial |

---

## Checklist de Taxonomia

> Resposta válida: **um ID de cenário**, **`não se aplica: {motivo}`** ou
> **`lacuna declarada: {o que foi tentado}`**. Nunca "sim", nunca "parcialmente coberto".

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | CT-36 (registro), **CT-55** (chave estrangeira) |
| Autorização exercida **na ação**, não só consultada por `can()` | CT-08, CT-15, CT-16, CT-19, CT-34, CT-46 |
| **Cenário por fora do componente de UI** (gate de camada) | CT-02 (R1), CT-08 (R2), CT-15/CT-16 (R5), CT-19 e **CT-48** (R6), CT-34 (R13, com lacuna declarada) |
| **Verbo irmão** — a autorização falsificada em cada verbo | CT-08 (editar/excluir), CT-15 e CT-16 (aprovar/rejeitar) |
| **Etapa irmã** — a regra falsificada nas duas etapas, não só na primeira | **CT-48** (justificativa no diretor), CT-16 (papel × verbo no diretor), CT-49 (cardinalidade do decisor) |
| **Estado reentrante** — a operação exercitada nas duas proveniências | **CT-47** (editar), CT-40 (excluir), CT-22 (enviar), CT-41 (aprovar/rejeitar), CT-24 (cancelar) |
| **Controle positivo** em toda asserção de ausência de leitura | CT-33 (a Ana passa onde o Bruno é barrado), CT-36 (o Téo vê a dele e não vê a alheia) |
| Idempotência, ancorada no **agregado persistido** | CT-11 (envio), CT-30 (decisão) |
| Concorrência | CT-30 — **e o limite está declarado ali**: a corrida real (dois processos) não é reprodutível neste arnês. Tentado: sqlite `:memory:` vive no processo do teste; `--parallel` distribui arquivos, não requisições ao mesmo registro; `pcntl_fork` indisponível no ambiente. CT-30 falsifica o **check-then-act**, que é o mecanismo do defeito |
| **Fronteira no ponto de entrada** (na gravação, não só no uso) | CT-01 (criação), CT-05 (edição) |
| **Criação ≠ edição ≠ uso** | criação CT-01/CT-03/CT-04/**CT-50** · edição CT-05/CT-06/**CT-47** · uso CT-12/**CT-54** |
| **Persistência positiva** — os campos submetidos chegam ao banco | **CT-50** (criação), CT-06 e CT-47 (edição), CT-19 (texto livre lido de volta) |
| **Unicidade contra o próprio registro** (armadilha da edição) | CT-39 |
| Domínio condicionado (a fronteira de um campo depende de outro) | não se aplica: o domínio de `valor` não depende de nenhum outro campo. O que depende do valor é o **fluxo**, e isso é CT-12 |
| **Estado × operação de escrita** — o registro removido ainda funciona? | **CT-56**. A premissa de mecanismo do PRD ("a exclusão é física, sem `SoftDeletes`") fixa **como** o cenário é escrito e **não** dispensa escrevê-lo |
| **Ordenação — o carimbo exibido é o da própria linha** | **CT-52** (instantes distintos), CT-27 (empate) |
| Ausente ≠ `null` ≠ vazio | CT-19 (vazia, só espaços — no domínio), CT-20 (não preenchida — no formulário), CT-10 (gestor ausente), CT-03 (centro ausente) |
| Ordenação — empate sem desempate determinístico | CT-27 |
| Paginação | não se aplica: nenhuma cláusula do requisito fala em listagem paginada, e a paginação é a nativa do Filament, não configurada nem alterada por esta entrega |
| Ordenação por coluna arbitrária (injeção via `orderBy`) | não se aplica: nenhuma ordenação é escolhida pelo usuário nesta feature; a única ordem afirmada é a do histórico (CT-27) |
| **Timezone / DST / virada de dia** | não se aplica: **nenhuma decisão desta feature lê a data** — não há prazo, SLA, expiração, agendamento nem comparação temporal. Tentado antes de declarar: `config(['app.timezone' => 'UTC'])` divergente do banco, e `travelTo()` na virada do dia — nos dois, alçada, transições e histórico produzem observável idêntico. O que o tempo decide aqui é **ordem** (CT-27) e **exibição** (CT-52) |
| Unicode / limite de `varchar` | CT-19 (acento + emoji de 4 bytes na justificativa), CT-03 (descrição no limite, acima do limite, com acento e emoji) |
| Unicidade + `SoftDeletes` | não se aplica: nenhum model desta entrega usa `SoftDeletes` (premissa de mecanismo do PRD). O que essa premissa **não** dispensa — *"o registro removido ainda funciona?"* — é CT-40 |
| CRUD combinado — editar sem alterar nada; excluir e operar depois | CT-39, CT-40 |
| CRUD — ler/editar/excluir ID inexistente | não se aplica: o route binding por uuid é do kit (`TemUuid::getRouteKeyName()`) e já é coberto por `tests/Kit/FundacaoTest.php`; reescrevê-lo aqui testaria o kit, não a feature |
| **Mass assignment** | CT-04 |
| Upload | não se aplica: anexos declarados fora de escopo no `00` |
| **Precisão monetária** | CT-02 (três casas decimais na fronteira da alçada) e CT-12 (borda de `0,01`). **Lacuna declarada** para `float` × `decimal` na comparação pura: não há aritmética nesta feature — nenhuma soma, total ou rateio —, e nenhum valor testado distingue as duas representações. Tentado: teto de `decimal(12,2)`, centavo ímpar (R$ 5.000,01) e a borda exata; os três produzem o mesmo observável nas duas representações. O gatilho para migrar a centavos está em ADR-02 |
| **Cardinalidade do destinatário (0 / 1 / N)** | CT-29. O cenário de **zero** não é citado como prova de não-efeito nem de atomicidade em lugar nenhum deste arquivo — o não-efeito ali é afirmado sobre a **Ana**, que existe |
| **Atomicidade do efeito colateral** | CT-31 — falha induzida **depois** do ponto do efeito (na gravação da etapa, por evento de model que lança) **e** com destinatário real (a Dora existe e seria notificada no caminho feliz). As duas condições, juntas |
| **Canal do efeito** | CT-28, CT-29, CT-37 — o predicado de canal `mail` é afirmado, e não só "uma notificação foi enviada" |
| Dado de outro tenant | CT-36, CT-37 |
| Contador / saldo / limite de uso | não se aplica: esta feature não tem contador, saldo nem limite de uso. O único número comparado é o valor contra a alçada (CT-12) |
| Campo opcional | CT-19 (`justificativa`, obrigatória na rejeição e nula na aprovação), CT-10 (`gestor_id` nulo) |

### As três lacunas declaradas, reunidas

| # | Lacuna | O que foi tentado | Pergunta que a acompanha |
|---|---|---|---|
| **L1** | `float` × `decimal` na comparação pura | teto de `decimal(12,2)`, centavo ímpar, borda exata — nenhum distingue as representações sem aritmética | nenhuma: é consequência de a feature não somar nada. ADR-02 nomeia o gatilho |
| **L2** | corrida real de dois processos | sqlite `:memory:` in-process; `--parallel` não isola o mesmo registro; sem `pcntl_fork` | vale a pena um teste de integração contra MySQL para o `UPDATE` condicional? |
| **L3** | escrita em `CentroCusto` por fora do componente Livewire | rota HTTP (é `GET`, e é CT-34); `Livewire::test` (é o componente); `CentroCusto::update()` direto **passa** — não há asserção de identidade no model | um job/comando futuro que altere `gestor_id` deve ser barrado pelo **domínio**, como `Convite::exigirDono()`? Se sim, é cláusula nova |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|---|---|---|---|---|---|---|
| CT-01 | domínio do valor na criação | R1 | BVA | componente (create) | `tests/Feature/Compras/TelasTest.php` | M1.1, M1.8 |
| CT-02 | valor com 3 casas decimais é recusado | R1 | BVA `0,001` · **fora da UI** | Feature | `tests/Feature/Compras/SolicitacaoCompraTest.php` | M1.5 |
| CT-03 | descrição e centro de custo obrigatórios | R1 | EP + unicode | componente (create) | `TelasTest.php` | M1.6, M1.9 |
| CT-04 | o formulário não escolhe situação, solicitante nem organização | R1 | mass assignment | componente (create) | `TelasTest.php` | M1.2, M1.3 |
| CT-05 | domínio do valor na edição | R1 | BVA | componente (edit) | `TelasTest.php` | M1.4 |
| CT-06 | a Ana edita o próprio rascunho, campo a campo | R2 | matriz (célula válida) | componente (edit) | `TelasTest.php` | — (célula válida de `editar`) |
| CT-07 | alçada recomputada sobre o valor editado | R2 | estado × campo | Feature | `SolicitacaoCompraTest.php` | M2.3 |
| CT-08 | terceiro não edita nem exclui, **fora da UI** | R2 | papel × verbo | Feature | `tests/Feature/Compras/AutorizacaoTest.php` | M2.1, M2.2 |
| CT-09 | affordance de Editar/Excluir por persona | R2 | papel × verbo | componente | `TelasTest.php` | M2.4 |
| CT-10 | o envio depende de haver gestor no centro | R3 | tabela de decisão + cardinalidade | Feature | `SolicitacaoCompraTest.php` | M3.1, M3.2, M3.3 |
| CT-11 | duplo clique no envio | R3 | idempotência (agregado) | Feature | `SolicitacaoCompraTest.php` | M3.4 |
| CT-12 | a fronteira da alçada | R4 | **BVA 3-valores** | Feature | `SolicitacaoCompraTest.php` | M4.1, M4.2, M4.4 |
| CT-13 | o diretor não decide antes do gestor | R4 | estado × evento | Feature | `SolicitacaoCompraTest.php` | M4.3 |
| CT-14 | a aprovação do diretor encerra o fluxo | R4 | estado × evento | Feature | `SolicitacaoCompraTest.php` | M4.5, M4.6, M12.2 |
| CT-15 | papel × verbo na etapa de gestor, **fora da UI** | R5 | matriz papel × verbo | Feature | `AutorizacaoTest.php` | M5.1, M5.2, M5.3, M5.5 |
| CT-16 | papel × verbo na etapa de diretor, **fora da UI** | R5 | matriz papel × verbo | Feature | `AutorizacaoTest.php` | M5.1, M5.4, M5.5 |
| CT-17 | solicitante que é gestora do próprio centro | R5 | `@premissa` A-09 | Feature | `SolicitacaoCompraTest.php` | M5.6 |
| CT-18 | affordance de Aprovar/Rejeitar por persona | R5 | matriz papel × verbo | componente | `TelasTest.php` | M5.5 (affordance) |
| CT-19 | justificativa exigida pelo domínio, **fora da UI** | R6 | EP + unicode | Feature | `SolicitacaoCompraTest.php` | M6.1, M6.2, M6.3, M6.4, M6.5 |
| CT-20 | a modal não fecha sem o motivo | R6 | EP (ausente) | componente | `TelasTest.php` | M6.1 (tela) |
| CT-21 | a rejeição devolve ao rascunho | R7 | estado × evento | Feature | `SolicitacaoCompraTest.php` | M7.1, M7.4, M12.2 |
| CT-22 | **2-switch**: o reenvio recomeça pelo gestor | R7 | 2-switch | Feature | `SolicitacaoCompraTest.php` | M7.2, M7.3, M7.6 |
| CT-23 | o segundo giro percorre as duas etapas | R7 | 2-switch | Feature | `SolicitacaoCompraTest.php` | M7.5 |
| CT-24 | cancelamento por estado e por ator | R9 | estado × operação + persona | Feature | `SolicitacaoCompraTest.php` | M9.1, M9.2, M9.3, M9.4 |
| CT-25 | a listagem mostra a situação — **5 de 5 do enum** | R10 | EP exaustiva | componente | `TelasTest.php` | M10.1, M10.2, M10.3 |
| CT-26 | o histórico mostra quem decidiu, o quê, quando e por quê | R11 | rastreio de efeito | componente | `TelasTest.php` | M11.1, M11.2, M11.3, M11.5 |
| CT-27 | etapas com carimbo empatado saem na ordem certa | R11 | ordenação (empate) | componente + `freezeTime` | `TelasTest.php` | M11.4 |
| CT-28 | o envio notifica o gestor, e só ele | R12 | rastreio de efeito (aconteceu) | Feature | `tests/Feature/Compras/NotificacaoTest.php` | M12.1, M12.2 |
| CT-29 | cardinalidade dos diretores (0/1/N) | R12 | cardinalidade | Feature | `NotificacaoTest.php` | M12.1, M12.5 |
| CT-30 | decisão repetida não duplica etapa nem e-mail | R12 | idempotência (agregado) | Feature | `NotificacaoTest.php` | M12.4 |
| CT-31 | o e-mail não sobrevive à gravação que falha | R12 | **atomicidade** | Feature | `NotificacaoTest.php` | M12.3 |
| CT-32 | a matriz de permissões por papel | R13 | matriz papel × ação | Feature | `AutorizacaoTest.php` | M13.1, M13.2, M13.3, M13.5 |
| CT-33 | usuário comum barrado na tela de centros | R13 | matriz papel × ação | componente | `AutorizacaoTest.php` | M13.1 |
| CT-34 | usuário comum barrado **fora do componente** | R13 | matriz papel × ação | Feature (HTTP) | `AutorizacaoTest.php` | M13.1 |
| CT-35 | o papel diretor entra no painel e decide | R13 | matriz papel × ação | componente | `AutorizacaoTest.php` | M13.4 |
| CT-36 | dado de outra organização não é lido nem operado | R14 | **IDOR** | FeatureTenancy | `tests/FeatureTenancy/Compras/IsolamentoTest.php` | M14.1, M14.2, M14.3 |
| CT-37 | diretores resolvidos na organização da solicitação | R14 | contexto de tenant | FeatureTenancy | `IsolamentoTest.php` | M14.4, M14.5 |
| CT-38 | cadastro do centro de custo | R15 | CRUD (create) | componente (create) | `tests/Feature/Compras/CentroCustoTest.php` | M15.2, M15.3 |
| CT-39 | salvar o centro sem alterar o nome | R15 | unicidade contra si | componente (edit) | `CentroCustoTest.php` | M15.1, M15.2 |
| CT-40 | rascunho excluído — virgem e reentrado | R16 | matriz (célula válida) | Feature | `SolicitacaoCompraTest.php` | M16.10 |
| CT-41 | rascunho não se aprova nem se rejeita — nas duas proveniências | R16 | matriz | Feature | `SolicitacaoCompraTest.php` | M16.1, M16.5, M16.6, M16.9 |
| CT-42 | `aguardando_gestor` × editar/excluir/enviar | R16 | matriz | Feature | `SolicitacaoCompraTest.php` | M2.5, M16.2, M16.3, M16.4, M16.8 |
| CT-43 | `aguardando_diretor` × editar/excluir/enviar | R16 | matriz | Feature | `SolicitacaoCompraTest.php` | M2.5, M16.2, M16.3, M16.4, M16.8 |
| CT-44 | `aprovada` × as seis operações | R16, **R8** | matriz | Feature | `SolicitacaoCompraTest.php` | M8.1…M8.5, M16.4, M16.5 |
| CT-45 | `cancelada` × as seis operações | R16, R9 | matriz | Feature | `SolicitacaoCompraTest.php` | M9.5, M16.4, M16.5 |
| **CT-46** | mudar o centro em trânsito não troca quem aprova | R16, R2 | matriz (dimensão do campo) | Feature | `SolicitacaoCompraTest.php` | M16.8 |
| **CT-47** | o rascunho reentrado continua editável | R7, R2 | 2-switch em `editar` | componente (edit) | `TelasTest.php` | M7.7, M7.8, M2.6 |
| **CT-48** | justificativa exigida também na etapa de diretor | R6 | EP · **etapa irmã** · fora da UI | Feature | `SolicitacaoCompraTest.php` | M6.6, M6.7 |
| **CT-49** | com vários diretores, a primeira decisão resolve | R5 | cardinalidade do decisor | Feature | `AutorizacaoTest.php` | M5.7, M5.8 |
| **CT-50** | a criação persiste os três campos do requisito | R1 | rastreio de efeito da gravação | componente (create) | `TelasTest.php` | M1.7 |
| **CT-51** | os cinco rótulos de situação são distintos | R10 | EP exaustiva (exibição) | componente | `TelasTest.php` | M10.2, M10.4 |
| **CT-52** | cada etapa exibe o próprio carimbo | R11 | ordenação/exibição temporal | componente | `TelasTest.php` | M11.6 |
| **CT-53** | trocar o gestor troca quem decide | R3 | `@premissa` A-21 | Feature | `SolicitacaoCompraTest.php` | M3.5 |
| **CT-54** | o valor gravado é o que decide a alçada | R1 | invariante de A-15 | Feature | `SolicitacaoCompraTest.php` | M1.5 |
| **CT-55** | a FK não cruza organizações | R14 | IDOR na referência | FeatureTenancy | `IsolamentoTest.php` | M14.6 |
| **CT-56** | a solicitação excluída não volta a operar | R16 | taxonomia (removido ainda funciona?) | Feature | `SolicitacaoCompraTest.php` | M16.7 |

**O único cenário sem mutante próprio é CT-06**, e ele fica: é a **célula válida obrigatória** da
coluna `editar` na linha do rascunho virgem. Sem ela, a coluna teria só recusas, a metade positiva
da matriz sumiria, e CT-47 (o rascunho reentrado) não teria contra o que ser comparado — é o par
virgem/reentrado que torna M2.6 e M7.7 falsificáveis. Célula válida obrigatória é a exceção
declarada à regra *"cenário que não mata mutante nenhum é candidato a corte"*.

### Helper compartilhado — onde ele nasce

O bloco de personas e fixtures é usado por **cinco** arquivos de teste. Pela rule do projeto
(`.ai/rules/testes.md`, enforçada por `tests/Kit/HelpersDeTesteTest.php`), helper usado por mais
de um arquivo **tem** de ser declarado em `tests/Pest.php` — declarado num arquivo de teste, ele
estoura `Call to undefined function` em `--parallel`, em `--tia` e ao rodar o arquivo isolado.

Sugestão devolvida ao PRD: um único `mundoDeCompras(): array` em `tests/Pest.php`, devolvendo as
seis personas e os centros. **Não** criar clones com outro nome para escapar de colisão — a rule
é explícita sobre isso.

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| a tela de visualização mostrando a situação atual, em cenário próprio | mata os mesmos mutantes de CT-25 (listagem); a leitura de detalhe entra em CT-26, junto do histórico |
| CT de log: channel `compras`, nível por método, e-mail mascarado, justificativa fora do log | **testaria o PRD** — nenhuma cláusula do `00` menciona log. Recusado como oráculo na `## Fronteira com o Plano`, e virou a pergunta **A-20** |
| CT afirmando os rótulos em pt-BR e as cores do badge | comportamento visível que só o PRD determina — pergunta **A-19**. CT-25 afirma o **estado** da coluna |
| CT do filtro por situação na listagem | não há cláusula de filtro no `00`; é `SelectFilter` nativo do Filament, e o enum já é exercitado por CT-25 |
| CT do `->money('BRL')` na coluna de valor | formatação de exibição escolhida pelo PRD; nenhuma cláusula do `00` fala em formato |
| CT verificando `exigeDiretor()` como predicado isolado | nome de método é escolha de implementação; o comportamento observável é CT-12, e um teste de predicado seria teste do plano |
| CT de "excluir duas vezes" | o segundo `excluir` sobre um registro apagado é a mesma mecânica de CT-40 (a cópia em memória não volta a operar), e mata o mesmo mutante |
| CT em `tests/Unit` para o enum (`emTransito`, rótulo, cor) | `tests/Pest.php` não liga `Unit` a `TestCase` nenhum, e `emTransito` só é observável através de CT-24; o rótulo e a cor estão recusados como oráculo |
| CT de regressão de `tests/Kit/PaineisTest.php` (contagem de permissions) | é **regressão do kit**, não derivação desta feature. Continua obrigatório e está no PRD (passo 11, CT-18 do plano); este arquivo não o duplica |

---

## Gate do `05` — passou

A tabela `## Superfície de UI` do PRD tem 6 linhas, todas com `Depende de JS? = Sim`. Mas a tabela
é **gatilho**, não critério: o cenário só vai ao browser quando afirma sobre algo que **só o
navegador prova**. Aplicado o critério, **quase tudo ficou no `04`** — validação de formulário,
gravação, listagem, filtro, ação de tabela, notificação e autorização na tela são teste de
componente Livewire, rodam em milissegundos e não precisam de Node.

Sobraram **dois** cenários que só o navegador prova, e eles estão em
[`05-casos-de-teste-browser.md`](05-casos-de-teste-browser.md): a **modal de rejeição**, que só
existe com o JavaScript executando, no caminho feliz e no erro visível.

---

## Fechamento do Ciclo com Mutation Testing

Depois de implementar:

```bash
vendor/bin/pest tests/Feature/Compras --mutate --path=app/Models/SolicitacaoCompra.php
vendor/bin/pest tests/Feature/Compras --mutate --path=app/Models --min=70
```

Três avisos que valem para **este** projeto:

1. **`pestphp/pest-plugin-mutate` não está declarado no `composer.json`** — está em `vendor/` como
   dependência transitiva do Pest 5. O comando funciona por acidente da árvore de dependências e
   some num `composer update`. Devolvido ao PRD: `composer require pestphp/pest-plugin-mutate --dev`.
2. **Exige driver de cobertura** (PCOV ou Xdebug com `XDEBUG_MODE=coverage`). A rule
   `.ai/rules/testes-browser.md` registra que, sem PCOV, coisas dependentes de cobertura não
   terminam neste ambiente — medir mutação vai custar o mesmo.
3. **O mutation score é cego à omissão.** Ele só muta código que existe: se uma cláusula do
   requisito nunca virou código, não há `if` para mutar e o score **não cai**. Quem responde por
   omissão aqui é a rastreabilidade `RQ` → regra → cenário e o gate de mutantes **de
   especificação** do passo 6 — não o `--mutate`. Mutante sobrevivente é traduzido de volta em
   lacuna de derivação e vira cenário novo; score alto **não** encerra a análise.

---

## Revisão Adversarial

Executada por **sub-agente independente**, que não derivou os cenários. Contrato cumprido: recebeu
o `00-requisito.md`, o `04` e o `05`, e **não** recebeu o `01-plano-acao.md`, nem o código, nem o
raciocínio de quem derivou. Tarefa: *provar que o conjunto deixa passar um defeito*.

**17 achados. Todos fechados.** Onze viraram cenário novo (CT-46…CT-56), seis viraram oráculo
reescrito, e um forçou uma mudança estrutural na matriz.

### O ledger

| # | Achado | Gravidade | Virou |
|---|---|---|---|
| 1 | `centro_custo_id` continuava mutável em trânsito: a Ana move a solicitação para um centro do qual é gestora e se aprova. A legenda listava três campos e cobrava um | **crítica** — escalada de privilégio | legenda corrigida + linhas de `editar` em CT-42…CT-45 + **CT-46** (cadeia completa) |
| 2 | o rascunho **reentrado por rejeição** nunca era editado: "corrigir", metade literal de RQ-09, não era executado por cenário nenhum | **crítica** — cláusula sem oráculo | **CT-47** + a matriz desdobrada em 6 estados |
| 3 | a justificativa era falsificada só na etapa de **gestor**; o ramo do diretor passava sem validação | **crítica** | **CT-48** |
| 4 | a decisão do diretor só era exercitada com **um** diretor: "a primeira que decidir resolve" (A-03) era indistinguível de "todas precisam decidir" | **crítica** | **CT-49** |
| 5 | **nenhum cenário afirmava um campo persistido na criação** — R1 media contagem de linhas e recusas | **crítica** — RQ-01 sem oráculo positivo | **CT-50** + CT-01 com `valor gravado` + CT-03 lido de volta |
| 6 | CT-24 afirmava "não ganha etapa" contra fixture de histórico **vazio**: `cancelar()` que apagasse a trilha passava | alta — falso ✅ | CT-24 com coluna `etapas_antes` + legenda de `cancelar` corrigida |
| 7 | `assertTableColumnStateSet` não observa a tela: o colapso de rótulo (M10.2) sobrevivia, e 3 de 5 rótulos nunca eram vistos | alta — falso ✅ | **CT-51** |
| 8 | a prosa de CT-19 afirmava integridade unicode que o `Então` **não** tinha: M6.5 constava morto por um cenário que não o matava | alta — falso ✅ | CT-19 com "lida de volta do banco" |
| 9 | IDOR protegia o **registro** e nunca a **chave estrangeira**: solicitação da Acme apontando para centro da Globex | alta | **CT-55** |
| 10 | CT-02 era autocontraditório — dizia "recusado" e as linhas do invariante pressupunham a gravação. O invariante de A-15 era **inexecutável** | alta | separado em CT-02 + **CT-54** |
| 11 | o carimbo por etapa nunca era afirmado como **valor**: CT-26 media presença e CT-27 congela o tempo | média | **CT-52** |
| 12 | CT-29 não afirmava histórico em nenhuma linha: o invariante de A-13 vivia só na prosa da pergunta | média | coluna `etapas` nas três linhas |
| 13 | o SFDIPOT declarava "gestor removido depois do cadastro" e mapeava para três cenários que não o exercitavam | média | **CT-53** + pergunta A-21 |
| 14 | CT-36 afirmava "não aparece" numa listagem **sem nenhum registro da Globex**: listagem vazia por qualquer motivo passava | média — falso ✅ | controle positivo em CT-36 e CT-33 |
| 15 | CT-33/CT-34 terminavam com "o gestor continua sendo o Rui" — asserção de ausência sem alvo, num `GET` que não escreve nada | média — falso ✅ | asserção removida; oráculo é o 403 |
| 16 | CT-B01/CT-B02 ancorados em `assertSee('Rascunho')`, texto que o `SelectFilter` já renderiza antes de qualquer clique | média | âncoras reescritas no `05` |
| 17 | ações escondidas no `Então` (CT-40, CT-02) e múltiplos `Quando` (CT-30, CT-B01, CT-B02) | baixa — estrutural | CT-40 → CT-40 + **CT-56**; CT-02 → CT-02 + CT-54; CT-30 com a 1ª aprovação no `Dado`; CT-B01/B02 reescritos |

### O padrão por trás dos achados

Onze dos dezessete são a mesma falha em roupas diferentes: **cobrir metade do verbo da cláusula e
marcar a cláusula inteira como coberta.**

- "editar e excluir" → só `editar` falsificado fora da UI (fechado antes, em CT-08)
- "corrigir e enviar de novo" → só `enviar` executado (nº 2)
- "aprovar ou rejeitar" com **duas etapas** → justificativa exigida só na primeira (nº 3)
- "com descrição, valor e centro de custo" → só o que **não** deve ser gravado (nº 5)
- "quem aprovou cada etapa, quando" → "quando" só como presença (nº 11)

O conjunto **já tinha** a regra do verbo irmão e a aplicava em R5. O que faltava era generalizá-la:
**etapa irmã**, **estado reentrante**, **campo irmão** e **cardinalidade do decisor** são a mesma
regra em outros eixos, e cada eixo esquecido produziu exatamente um defeito plausível que
atravessava o conjunto inteiro. As três linhas novas do checklist de taxonomia existem para isso.

O segundo padrão, com cinco ocorrências (nº 6, 7, 8, 14, 15), é o **falso ✅**: asserção que
parece rigorosa e não discrimina — ausência sem alvo, ausência sem destinatário, prosa que promete
o que o `Então` não tem. Todas foram corrigidas **pela fixture ou pelo oráculo**, nunca por poda.

### Segunda rodada — não executada, e por quê

A skill permite **uma** re-revisão, e só se o fechamento tiver criado cenário novo — o que foi o
caso (onze). O teto é de duas rodadas. **A segunda rodada não foi executada nesta sessão**, e isso
é dívida declarada, não decisão de que o conjunto está pronto: onze cenários novos introduzem
superfície nova, e é aí que mora a lacuna de segunda ordem.

**Recomendação ao próximo agente**: rodar a segunda rodada antes de materializar os testes,
apontando-a especialmente para os cenários CT-46…CT-56 e para a matriz de 42 células, que é a
parte que mudou de estrutura e não só de conteúdo.
