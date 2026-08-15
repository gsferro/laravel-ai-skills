# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> a feature ainda não existe. Do `01` vieram apenas paths, rotas, superfície de UI e stack.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| **Fluxo e máquina de estados** (enviar, aprovar, rejeitar, cancelar, reentrada em rascunho) | 3 | 3 | 9 | **completo** |
| **Alçada por valor** (o limite de R$ 5.000 e a ordem gestor → diretor) | 3 | 3 | 9 | **completo** |
| **Autorização** (quem decide cada etapa, quem edita, quem define o gestor) | 3 | 3 | 9 | **completo** |
| **CRUD da solicitação** (criação e edição em rascunho) | 2 | 3 | 6 | **padrão** |
| **Notificação do próximo aprovador** | 2 | 3 | 6 | **padrão** |
| **Exibição** (situação atual e histórico de etapas na tela) | 2 | 2 | 4 | **padrão** |

Justificativa das notas, porque nota sem motivo é número decorativo:

- **P=3 no fluxo**: duas pessoas diferentes agem sobre o mesmo registro, e o card descreve um estado
  reentrante (rejeitada volta para rascunho). Concorrência real — dois diretores, duas abas.
- **I=3 em fluxo, alçada e autorização**: dinheiro e autorização. Uma aprovação a menos é uma compra
  liberada sem o segundo par de olhos; uma aprovação por quem não devia é escalada de privilégio.
- **I=3 na notificação**: o destinatário errado é dado de terceiro (valor, descrição e centro de
  custo de outra organização num e-mail) — LGPD, não só retrabalho.
- **I=2 na exibição**: a tela dizer "Aprovada" com uma etapa faltando induz decisão errada, mas é
  reversível e não altera o registro.

**Revisão adversarial**: obrigatória (há áreas em perfil `completo`) — ver
[Revisão Adversarial](#revisão-adversarial).

- Técnicas aplicadas: **EP**, **BVA 3-valores** (incremento `0,01` — coluna `decimal(12,2)`),
  **tabela de decisão**, **tabela estado × evento** (com persona e campo como dimensões),
  **matriz papel × ação**, **rastreio de efeito**, **2-switch** (ciclo de volta).
- Regras: **12** · Cenários: **63** (61 neste arquivo + 2 CT-B no `05`) · Mutantes previstos:
  **95** (88 aqui + 7 no `05`) · **Sem matador pleno: 3** — R4-M5, R10-M4 e R11-M6, os três com
  lacuna declarada e com o que foi tentado escrito.

> Os números acima são **pós-duas rodadas de revisão adversarial**, e a progressão é o dado mais
> informativo deste cabeçalho:
>
> | | Cenários | Mutantes | Lacunas declaradas | Mutantes com matador que **não matava** |
> |---|---|---|---|---|
> | derivação inicial | 47 | 69 | 3 | **6** (descobertos na rodada 1) |
> | após a rodada 1 | 55 | 80 | 2 | **6** (descobertos na rodada 2 — **3 deles em cenários criados pela rodada 1**) |
> | após a rodada 2 | **61** | **88** | 3 | — |
>
> O que mudou e por quê está em [Revisão Adversarial](#revisão-adversarial); cada matador corrigido
> está marcado na própria tabela de mutantes da regra.

**Estouro do teto de mutantes, declarado**: o gate pede de 3 a 6 mutantes por regra no perfil
completo, e **R5 (11), R6 (10), R10 (9), R11 (9), R12 (8), R3 (7) e R4 (7) estouram**. Duas causas
distintas, e a skill trata cada uma de um jeito:

1. **Agregação de cláusulas.** R5 e R6 cobrem quatro cláusulas cada (R5: RQ-04, RQ-05, RQ-06 e a
   premissa A-07; R6: RQ-06, RQ-07, RQ-08, RQ-09) — pelo critério da skill, cada uma "quase sempre
   é duas regras". Desdobrá-las renumeraria toda a rastreabilidade `RQ` → regra → cenário por um
   motivo de contagem, e a decisão foi **registrar** em vez de esconder.
2. **Mutante trazido pela revisão adversarial não conta para o teto** — é a exceção que a própria
   skill abre, porque é achado medido e não enchimento. Da rodada 1: R3-M7, R5-M8, R5-M9, R5-M10,
   R6-M9, R9-M4, R9-M5, R10-M6, R10-M7, R12-M6, R12-M7, R12-M8. Da rodada 2: R4-M7, R5-M11, R6-M10,
   R10-M11, R10-M12, R11-M7, R11-M8, R11-M9.

Nenhum dos 88 é enchimento: todos passam no teste de plausibilidade (*um dev competente, lendo só o
requisito e sem má-fé, escreveria isso?*). **Vinte deles vieram de revisão independente**, e é o
melhor argumento disponível a favor da regra de não autorrevisar.

### Técnica escalada acima do perfil da área

- **R1** é área `padrão` (CRUD) e recebeu **BVA na criação** (CT-04), não só EP. Motivo: o
  checklist de taxonomia exige fronteira **no ponto de entrada** para todo campo, e `valor` é o
  campo que decide o fluxo inteiro. EP sozinho não distingue "recusa negativo" de "recusa tudo
  abaixo de 1".
- **R11** é área `padrão` (notificação) e recebeu **rastreio de efeito com atomicidade** (4
  cenários, CT-40..CT-43). Motivo declarado na própria técnica: rastreio de efeito consome o teto
  inteiro, e a quarta direção entra quando a atomicidade importa — aqui importa, porque a
  notificação e a gravação da etapa acontecem no mesmo método.

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | três tabelas (solicitação, centro de custo, etapas de aprovação), um enum de situação, duas policies, dois Resources no painel `/app`, uma notificação, um papel novo (`diretor`), uma chave de configuração para o limite | CT-44, CT-45 |
| **F**unction | criar / editar / excluir em rascunho; enviar; aprovar; rejeitar com justificativa; cancelar; decidir a alçada pelo valor; exibir situação e histórico; notificar o próximo aprovador. **Função administrativa escondida**: definir quem é o gestor de um centro de custo — quem a alcança se nomeia aprovador | CT-01..CT-47 |
| **D**ata | `descricao` (texto livre), `valor` (`decimal`, fronteira em R$ 5.000,00), `centro_custo_id`, `situacao` (5 valores — partição exaustiva obrigatória), `justificativa` (obrigatória só na rejeição; vazia ≠ espaços ≠ ausente), **gestor do centro nulo** (A-10), **dado de outra organização** | CT-03, CT-04, CT-14, CT-25, CT-11, CT-09, CT-23, CT-35, CT-41 |
| **I**nterfaces | telas do painel `/app` (listagem, formulário de criação/edição, tela de visualização, ações de registro e modal de rejeição) **e** os métodos do model chamados **fora da tela** — job, comando, seeder, rota de API futura, que é por onde a policy não é consultada | CT-20, CT-21, CT-01, CT-05, CT-45 |
| **P**latform | SQLite em memória nos testes (`phpunit.xml`), então `decimal` volta como **string** e a comparação de alçada não pode depender do tipo devolvido pelo driver; fila em `sync` no teste, mas a notificação é `ShouldQueue`; papéis do spatie com `permission.teams` — o papel `diretor` só é visível dentro do contexto da organização, e o contexto quem fixa é o middleware do painel, que **não roda em worker de fila** | CT-14, CT-41 |
| **O**perations | cinco personas reais: solicitante, gestor do centro, diretor, administrador da organização e usuário comum sem relação nenhuma com o registro. **Uso indevido previsto**: aprovar a própria solicitação (A-09), decidir a etapa do outro, aprovar duas vezes no duplo clique | CT-18, CT-19, CT-22, CT-30, CT-44 |
| **T**ime | concorrência entre dois aprovadores da mesma etapa; **ordem** entre as etapas (diretor depois do gestor, nunca antes); **reentrada** em rascunho e o segundo giro do ciclo; empate de `created_at` entre duas etapas gravadas no mesmo segundo | CT-31, CT-16, CT-26, CT-27, CT-38 |

Nenhuma dimensão ficou vazia. **Fuso horário**: não há cláusula temporal no requisito — nenhum
prazo, nenhuma expiração, nenhuma janela. A única data exibida é a de cada etapa, e ela é lida no
mesmo fuso em que foi escrita. Registrado como `não se aplica` no checklist de taxonomia, com o
motivo, e não como lacuna.

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — A solicitação nasce em rascunho, com descrição, valor e centro de custo, e nem a situação nem o solicitante vêm do formulário | CRUD (padrão) | RQ-01 | EP + BVA na gravação + mass assignment | CT-01..CT-04 |
| **R2** — Em rascunho, e só nele, o solicitante edita e exclui a própria solicitação | autorização (completo) | RQ-02, RQ-03, RQ-10 | estado × operação × persona × campo | CT-05..CT-09 |
| **R3** — O envio encaminha a solicitação ao gestor do centro de custo; sem gestor, ela não sai do rascunho | fluxo (completo) | RQ-04, A-10 | tabela estado × evento | CT-10..CT-13 |
| **R4** — Valor **acima** de R$ 5.000 exige a aprovação do diretor, e ela vem **depois** da do gestor | alçada (completo) | RQ-05 | BVA 3-valores + ordem de eventos | CT-14..CT-17 |
| **R5** — Só o aprovador da etapa corrente decide, e a recusa vale para **aprovar e rejeitar** | autorização (completo) | RQ-04, RQ-05, RQ-06, A-03, A-07, A-09 | matriz papel × ação (verbo como dimensão) | CT-18..CT-23 |
| **R6** — A rejeição exige justificativa, devolve a solicitação ao rascunho e preserva o histórico do ciclo anterior | fluxo (completo) | RQ-06, RQ-07, RQ-08, RQ-09 | EP de texto + **2-switch** | CT-24..CT-28 |
| **R7** — Aprovada é estado terminal: nenhuma operação a altera | fluxo (completo) | RQ-10, A-05 | estado × operação + idempotência + concorrência | CT-29..CT-31 |
| **R8** — O solicitante cancela enquanto a solicitação está em trânsito, e só ele | fluxo (completo) | RQ-11, A-06 | estado × operação × persona | CT-32..CT-34 |
| **R9** — A tela mostra a situação atual da solicitação | exibição (padrão) | RQ-12, A-12 | partição **exaustiva** do enum | CT-35, CT-36 |
| **R10** — A tela mostra quem decidiu cada etapa, quando e com qual justificativa | exibição (padrão) | RQ-13, A-12 | EP + ordenação com empate | CT-37..CT-39 |
| **R11** — Cada transição que deixa uma etapa pendente notifica por **e-mail** exatamente os aprovadores da vez, uma vez, e ninguém mais | notificação (padrão) | RQ-14, A-11 | rastreio de efeito (4 direções) | CT-40..CT-43 |
| **R12** — Quem define o gestor de um centro de custo é a administração da organização, não o usuário comum do negócio | autorização (completo) | RQ-04 via A-08 | matriz papel × ação + CRUD | CT-44..CT-47 |

Toda cláusula `RQ-01` a `RQ-14` gerou ao menos uma regra. Nenhuma ficou sem cenário — a
rastreabilidade completa está no [Índice de Cenários](#índice-de-cenários).

---

## Fronteira com o Plano

O `01-plano-acao.md` é minucioso, e essa é exatamente a razão de esta seção existir: quanto mais
detalhado o plano, mais fácil é confundir a decisão dele com o comportamento pedido.

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| nomes `enviar()`, `aprovar()`, `rejeitar()`, `cancelar()`, `exigeDiretor()`, `transicionar()` | escolha de implementação | detalhe do cenário; o oráculo é a **situação gravada** e o registro da etapa |
| os cinco valores do enum (`rascunho`, `aguardando_gestor`, …) e a ausência de `rejeitada` | nomenclatura de implementação. O requisito determina os **estados**, não as strings | usados só como âncora de banco; o `Então` fala do comportamento observável |
| tabela `etapas_aprovacao_compra` append-only | escolha de modelagem | o oráculo de RQ-13 é **o que a tela mostra** (CT-37..CT-39); a tabela é âncora secundária |
| `config('kit.compras.limite_diretor')` | *onde* o número mora é implementação | **CT-15 usa o número literal do requisito**, sem injetar config |
| `minValue(0.01)` no campo valor | comportamento visível ao usuário que o **requisito não determina** | **pergunta P-01**; CT-04 marcado `@premissa` |
| `scopedUnique` no nome do centro de custo | idem | **pergunta P-02**; CT-47 cobre só a metade universal (salvar sem alterar) |
| textos de erro, rótulos de botão, títulos de modal, mensagem de sucesso | comportamento visível que o requisito não determina | não viram oráculo; os cenários afirmam estado e registro |
| **os logs no channel `compras`**, com nível e context especificados passo a passo | o requisito **não pede log nenhum**. Derivar CT de log daqui seria testar o PRD | **nenhum CT de log neste conjunto** — divergência declarada abaixo |
| suíte `FeatureTenancy`, paths de arquivo, rotas `/app/solicitacoes-de-compra` | infraestrutura e endereço | usados como path, nunca como oráculo |
| papel `diretor` global × diretor por centro de custo (A-03), cancelar não valer em rascunho (A-06), o diretor também rejeitar (A-07) | **vêm do `00-requisito.md`**, seção Ambiguidades — são premissas da linha de base, não do plano | **viram oráculo**, com os cenários marcados `@premissa` |

### Divergência declarada: `feature-wiki` × `feature-test-design`

A `feature-wiki` manda *"incluir CTs de log no `04` para validar channel, nível, formato e
context"*. Aqui isso **não foi feito**, e a razão é o princípio 1 desta skill: log não aparece em
nenhuma das 14 cláusulas do `00-requisito.md`. Um CT de log seria derivado exclusivamente do PRD —
teste que confirma a interpretação. Se o log for requisito de auditoria do projeto, ele precisa
virar cláusula no `00`, e aí ganha cenário.

### Precedência de rules do projeto sobre a skill

- `.ai/rules/testes-browser.md` proíbe `--parallel` com browser e registra que, **sem PCOV**, o
  `--tia` é inviável (medido: abortado após 35 min com Xdebug). A skill sugere
  `pest --parallel --tia` como padrão — **a rule vence**. Os comandos deste conjunto estão em
  [Comandos](#comandos), e são dois, nunca um.
- `.ai/rules/testes.md` exige que helper usado por mais de um arquivo viva em `tests/Pest.php`.
  Todos os helpers do [Setup Global](#setup-global) seguem essa regra, e há um teste do próprio kit
  (`tests/Kit/HelpersDeTesteTest.php`) que a cobra.

---

## Perguntas para o `00-requisito.md`

O `00-requisito.md` desta feature está **fechado para edição** (linha de base imutável desta
execução). Pelo procedimento da skill, as perguntas ficam aqui, em bloco pronto para colagem em
`## Ambiguidades e Perguntas Abertas`. **Elas continuam bloqueando o que dependem delas** — cada
cenário afetado está marcado `@premissa`.

```markdown
### A-13 — o requisito não determina o domínio de `valor` (RQ-01)

**Pergunta**: valor zero e valor negativo podem ser gravados? Há teto?

**Assumido**: **recusados na criação e na edição** — uma solicitação de compra de R$ 0,00 ou de
R$ -100,00 não é uma compra. Sem teto, porque o card não menciona nenhum.

**Se negado**: CT-04 muda de sinal (passa a exigir que o valor seja aceito) e o passo do
formulário perde a restrição.

### A-14 — dois centros de custo podem ter o mesmo nome? (RQ-01)

**Assumido**: **não dentro da mesma organização**, e **sim** entre organizações diferentes — é a
leitura que não deixa duas linhas indistinguíveis na mesma lista.

**Se negado**: CT-47 perde a metade da unicidade; a metade universal (salvar sem alterar nada não
pode falhar) permanece.

### A-15 — o histórico dos ciclos anteriores continua visível depois do reenvio? (RQ-13)

**Pergunta**: "quem aprovou cada etapa" inclui as etapas de um ciclo que já foi rejeitado e
corrigido?

**Assumido**: **sim**. Uma rejeição apagada no reenvio deixaria RQ-13 mentindo sobre o que
aconteceu, e é justamente o motivo pelo qual o solicitante corrigiu.

**Se negado**: CT-26 e CT-39 mudam de oráculo.

### A-16 — a alçada é reavaliada quando o valor muda depois de uma rejeição? (RQ-05, RQ-09)

**Pergunta**: o solicitante corrige o valor de R$ 8.000 para R$ 3.000 e reenvia. Ainda precisa do
diretor?

**Assumido**: **não** — a alçada é avaliada **no envio**, com o valor daquele momento. É a leitura
literal de "se o valor for acima de R$ 5.000", que fala do valor, não da história dele.

**Se negado**: CT-27 inverte, e o caminho passa a depender do maior valor já solicitado.

### A-17 — quem pode LER a solicitação de outra pessoa? (RQ-12, RQ-13)

**Pergunta**: o card diz "mostrar na tela" sem dizer para quem. Um solicitante vê as solicitações
dos colegas da mesma organização?

**Assumido**: **nada foi assumido** — este conjunto não escreve nenhum cenário sobre leitura de
registro alheio dentro da mesma organização, porque não há oráculo. Os cenários de autorização
afirmam apenas sobre **escrever e decidir** (CT-08, CT-18), onde o requisito é explícito.

**Impacto de não responder**: a regra de leitura fica **sem cobertura declarada**. É lacuna de
requisito, não de derivação.

### A-18 — trocar o gestor do centro alcança a solicitação já enviada? (RQ-04)

**Pergunta**: uma solicitação foi enviada quando a gestora era a Beatriz. A administradora troca a
gestora do centro para a Carla. Quem decide aquela solicitação agora?

**Assumido**: **a gestora atual do centro** — o vínculo é lido no momento da decisão, não congelado
no envio. É a leitura literal de "o gestor **do** centro de custo", que é uma propriedade do centro
e não da solicitação. E é a que não deixa a solicitação presa quando o gestor sai da empresa, que é
o caso real por trás da troca.

**Se negado** (o aprovador é congelado no envio): CT-55 inverte, e a feature ganha uma coluna nova
na solicitação — decisão de modelagem que muda o passo 2 do PRD, não só o teste.

> Esta pergunta **não existia** antes da segunda rodada da revisão adversarial: ela apareceu quando
> um cenário que dizia matar o mutante do "vínculo congelado" foi examinado e não o matava.
> Ambiguidade descoberta pelo gate, e não pela leitura do card.
```

---

## Setup Global

### Personas

Cinco pessoas distintas, e a distinção é **discriminante**: colapsar solicitante, gestor e diretor
no mesmo usuário faz todo cenário passar com a autorização removida.

| Persona | Como criar | Papel |
|---|---|---|
| `$solicitante` | `usuarioCom('panel_user')` | usuário comum do negócio; dono da solicitação |
| `$gestor` | `usuarioCom('panel_user')`, apontado por `centros_custo.gestor_id` | **gestor não é papel** — é a FK do centro |
| `$diretor` | `usuarioCom('diretor')` — nos cenários de histórico, chamada **Ana** | papel novo, painel `app` (A-03). **O nome é escolha discriminante**: com a gestora **B**eatriz decidindo primeiro e a diretora **A**na depois, a ordem cronológica é o **inverso** da alfabética, e uma ordenação por nome do decisor fica vermelha (R10-M11) |
| `$outroDiretor` | `usuarioCom('diretor')` | prova "a primeira que decidir resolve" e o alcance da notificação |
| `$adminOrg` | `usuarioComPapel('admin_organizacao', $tenant)` | quem cadastra centro de custo (A-08) — **só existe em modo multi-tenant**, ver a ressalva abaixo |
| `$estranho` | `usuarioCom('panel_user')` | nenhuma relação com o registro — a persona da barreira |

> **Ressalva verificada no seeder, não presumida.** `admin_organizacao` é criado **dentro de um
> `if (config('kit.tenancy.enabled'))`** (`database/seeders/PapeisSeeder.php:70-73`), e a tenancy
> vem **desligada por default** (`config/kit.php:59`, `KIT_TENANCY=false`). Em `tests/Feature`,
> `usuarioCom('admin_organizacao')` estoura `RoleDoesNotExist`. Consequência para a alocação de
> camada: **CT-45, CT-46 e CT-47 vão para `tests/FeatureTenancy/`**, e só CT-44 fica em
> `tests/Feature` — a subtração do `panel_user` roda nos dois modos, como o próprio comentário do
> seeder declara (`PapeisSeeder.php:80-83`). Usar `master_global` como a persona administradora em
> single-tenant seria mais barato e **mediria menos**: ele entra por `Gate::before`, **sem
> permission nenhuma no banco**, e o cenário passaria com a matriz de permissões inteira quebrada.

`usuarioCom()` já existe em `tests/Pest.php:188` e gera e-mail único, que é indispensável aqui:
quase todo cenário cria mais de um usuário.

**Seeders no `beforeEach`**: `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])`,
nessa ordem — molde de `tests/Kit/PaginasInfraTest.php:16-26`. Sem eles, toda tela responde 403 e o
cenário mede a ausência da permission em vez do que ele afirma.

### Fixtures

**Não há factory para os models novos** (`database/factories/` tem apenas `Convite`, `Cupom`,
`Tenant` e `User`). Duas saídas, e a escolha importa:

1. **Criar as factories** (`SolicitacaoCompraFactory`, `CentroCustoFactory`) como passo do PRD — é o
   caminho preferido, e `TenantFactory` já dá o molde de *state* nomeado (`comIdentidadeVisual()`).
2. Enquanto não existirem: `CentroCusto::create([...])` e `SolicitacaoCompra::create([...])`.

**Armadilha de fixture desta feature**: `situacao`, `solicitante_id` e `tenant_id` ficam **fora do
`$fillable`** — é o que impede o mass assignment de CT-02. Logo, `create([...])` **não** consegue
nascer com uma situação arbitrária. Duas formas de chegar num estado de trânsito, e cada uma tem
seu uso:

| Forma | Quando usar |
|---|---|
| **atravessar as transições** (`enviar()`, `aprovar()`) | sempre que o estado anterior fizer parte do que o cenário afirma — cenários de fluxo, 2-switch e histórico |
| `->forceFill(['situacao' => …])->save()` | matrizes de estado × operação, onde o caminho até o estado é irrelevante e atravessá-lo tornaria o cenário dependente de outra regra |

Um helper `solicitacaoEm(SituacaoSolicitacao $situacao, ...)` resolve as duas — e, por ser usado
por mais de um arquivo, **vive em `tests/Pest.php`**, nunca dentro de um `*Test.php`
(`.ai/rules/testes.md`, cobrado por `tests/Kit/HelpersDeTesteTest.php`).

### Fakes

- `Notification::fake()` **no início do cenário, antes de criar as fixtures** que disparam
  transição. É o fake certo: a notificação é `ShouldQueue`, e `Mail::assertSent` **nunca passaria**
  nela (armadilha catalogada). O molde é `tests/Kit/ConviteTest.php:111`.
- **Um cenário sem `Notification::fake()`** — CT-40 — para que `toMail()` **realmente renderize**.
  O `MAIL_MAILER=array` do `phpunit.xml` garante que nada sai da máquina, e um erro no corpo do
  e-mail ou na URL montada pelo painel aparece ali em vez de num job falhado. Precedente declarado
  em `tests/Kit/ConviteTest.php:313-316`.
- **Sem `Event::fake()`** em nenhum cenário: os models do kit dependem de eventos de `creating`
  (uuid, `tenant_id`), e fingi-los faz a fixture nascer quebrada.
- **Sem `Http::fake()`**: a feature não chama serviço externo nenhum.

### Estratégia de DB

`RefreshDatabase` global, aplicado por `tests/Pest.php` a todas as suítes. Banco SQLite em memória
(`phpunit.xml`). **Consequência que muda assertion**: `decimal` volta como **string** —
`assertDatabaseHas(['valor' => '5000.01'])`, e comparação de valor com `(string)` ou
`bccomp`, nunca com `===` sobre float.

### Suítes

| Suíte | Quando | Por quê |
|---|---|---|
| `tests/Feature/Compras/` | quase tudo | `TestCase` + `RefreshDatabase` (`tests/Pest.php:22-24`) |
| `tests/FeatureTenancy/Compras/` | CT-09, CT-23, CT-41, CT-45, CT-46, CT-47, CT-50, CT-55, CT-61 | precisam de `permission.teams` ligado **antes** das migrations — só o `TenancyTestCase` faz isso, e o Pest não permite dois `TestCase` na mesma pasta. A pasta e a testsuite são criadas no passo 10 do PRD |
| `tests/Browser/Compras/` | CT-B01, CT-B02 | ver `05-casos-de-teste-browser.md` |

> **`tests/Unit` está fora, e não por preferência.** O `tests/Pest.php` deste projeto **não liga
> nenhum `TestCase` à pasta `Unit`** — ela existe no `phpunit.xml` mas não é estendida em
> `tests/Pest.php`. Um caso "unitário" ali roda **sem container**: `config()`, cast de enum e
> Eloquent não resolvem. A regra da skill é a camada mais barata **que o arnês do projeto
> sustenta**; aqui essa camada é `Feature`.

---

## Regra R1 — A solicitação nasce em rascunho, e a situação não vem do formulário

> `RQ-01` · área **CRUD** (padrão) · técnicas: **EP** nos campos obrigatórios, **BVA na gravação**
> (escalada, ver justificativa no cabeçalho), **mass assignment**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: uma solicitação nasce em rascunho, com descrição, valor e centro de custo, e nem a
         situação nem o solicitante são escolhidos por quem preenche o formulário

    Cenário: [CT-01] o solicitante cria a solicitação pelo formulário
      Dado o solicitante autenticado no painel da organização
      E um centro de custo "Infraestrutura" com gestor definido
      Quando ele preenche descrição "Notebooks para o time", valor 7.200,55 e o centro
             "Infraestrutura", e confirma a criação
      Então existe uma solicitação com essa descrição, valor 7200.55 e o centro "Infraestrutura"
      E ela está em rascunho
      E o solicitante registrado é o usuário autenticado

    Cenário: [CT-02] os campos que o formulário não controla são ignorados no envio
      Dado o solicitante autenticado e um outro usuário na mesma organização
      Quando ele submete a criação incluindo, além dos três campos, uma situação "aprovada" e o
             identificador do outro usuário como solicitante
      Então a solicitação gravada está em rascunho
      E o solicitante gravado é o próprio autor do envio, não o outro usuário

    Esquema do Cenário: [CT-03] os três campos do requisito são obrigatórios
      Dado o solicitante autenticado no formulário de criação
      Quando ele submete a criação com "<campo>" em branco e os demais preenchidos
      Então a criação é recusada com erro no campo "<campo>"
      E nenhuma solicitação é gravada

      Exemplos:
        | campo           | # partição inválida isolada |
        | descricao       | um campo por linha          |
        | valor           | um campo por linha          |
        | centro_custo_id | um campo por linha          |

    Esquema do Cenário: [CT-04] @premissa (A-13) o valor gravado é estritamente positivo
      Dado o solicitante autenticado no formulário de criação
      Quando ele submete a criação com valor <valor>
      Então o número de solicitações gravadas é <gravadas>
      E, quando gravada, o valor dela é exatamente <persistido>

      Exemplos:
        | valor  | gravadas | persistido | # borda   |
        | -0.01  | 0        | —          | abaixo    |
        | 0.00   | 0        | —          | borda     |
        | 0.01   | 1        | 0.01       | borda+1   |
```

**Camada**: `Feature`, por componente Livewire (`CreateSolicitacaoCompra`) — é o
[gate de tela de escrita](#gate-de-tela-de-escrita) para a rota `create`. Molde:
`tests/Kit/PaginasInfraTest.php:86-104`.

**Nota de discriminação**: CT-01 usa **7.200,55** — e o centavo não-nulo é o ponto, não enfeite.
Com `7.200,00` (a primeira versão deste cenário), uma implementação que **trunca os centavos na
entrada** — máscara de moeda que devolve inteiro, `(int)` no `mutateFormDataBeforeCreate` — grava
`7200` e o cenário fica **verde**. O único jeito de o formulário ser exercitado contra a perda de
escala é um valor cujo centavo sobrevive na assertion. Os valores de centavo de CT-14 (`4999.99`,
`5000.01`) **não servem para isso**: eles entram por fixture, não pelo formulário, e portanto não
passam pela máscara. Mesma razão para a linha `0.01` de CT-04 afirmar agora o **valor persistido**,
e não só "aceito".

O `Então` de CT-01 afirma os **três** campos, nunca só a chave primária.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `situacao` inicial não é definida (fica nula) ou é definida como a primeira do enum por acidente | CT-01 |
| M2 | `solicitante_id` lido do payload em vez do usuário autenticado | CT-02 |
| M3 | `situacao` dentro do `$fillable`, aceitando o valor do formulário | CT-02 |
| M4 | `required` esquecido em um dos três campos (o mais provável: `centro_custo_id`, que tem valor default no `Select`) | CT-03 |
| M5 | valor truncado para inteiro **na entrada do formulário** (máscara de moeda, `(int)`), perdendo os centavos | CT-01 (`7200.55` gravado) e CT-04 (linha `0.01`, que afirma o persistido) — **corrigido na revisão adversarial**: a versão anterior usava `7.200,00` e não matava nada |
| M6 | nenhuma restrição de domínio no valor: negativo e zero gravam | CT-04 (linhas `-0.01` e `0.00`, pela contagem de gravadas) |

---

## Regra R2 — Em rascunho, e só nele, o solicitante edita e exclui a própria solicitação

> `RQ-02`, `RQ-03`, `RQ-10` · área **autorização** (completo) · técnica: **tabela estado ×
> operação**, com **persona** e **campo alterado** como dimensões próprias

A matriz que este bloco cobre — e as quatro dimensões que ela cruza:

| Situação \ operação | editar (campo `valor`) | excluir |
|---|---|---|
| `rascunho`, pelo solicitante | ✅ CT-05 | ✅ CT-06 |
| `rascunho`, por outra pessoa | ❌ CT-08 | ❌ CT-08 |
| `rascunho`, de outra organização | ❌ CT-09 | ❌ CT-09 |
| `aguardando_gestor` | ❌ CT-07 | ❌ CT-07 |
| `aguardando_diretor` | ❌ CT-07 | ❌ CT-07 |
| `aprovada` | ❌ CT-07 e CT-29 | ❌ CT-07 e CT-29 |
| `cancelada` | ❌ CT-07 | ❌ CT-07 |

**Cada coluna tem ao menos uma célula válida exercitada** (CT-05 e CT-06), que é a metade da regra
que a matriz costuma perder — e é o que faz a coluna `editar` não ficar só com recusas.

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: enquanto está em rascunho, e só enquanto está, o solicitante edita e exclui a própria
         solicitação

    Cenário: [CT-05] o solicitante corrige a própria solicitação em rascunho
      Dado uma solicitação em rascunho do solicitante, com descrição "Notebooks para o time",
            valor 7.200,55 e o centro "Infraestrutura"
      Quando ele salva a edição com descrição "Notebooks e docks", valor 4.850,25 e o centro
             "Operações"
      Então a solicitação gravada tem descrição "Notebooks e docks", valor 4850.25 e o centro
        "Operações"
      E ela continua em rascunho

    Cenário: [CT-06] o solicitante exclui a própria solicitação em rascunho
      Dado uma solicitação em rascunho do solicitante
      Quando ele exclui a solicitação
      Então a solicitação não existe mais

    Esquema do Cenário: [CT-07] depois de enviada, a solicitação não se edita nem se exclui
      Dado uma solicitação do solicitante na situação "<situacao>", com valor 7.200,00
      Quando o solicitante tenta "<operacao>" a solicitação
      Então a operação é recusada
      E a solicitação continua na situação "<situacao>" com valor 7200.00

      Exemplos:
        | situacao            | operacao |
        | aguardando_gestor   | editar   |
        | aguardando_gestor   | excluir  |
        | aguardando_diretor  | editar   |
        | aguardando_diretor  | excluir  |
        | aprovada            | editar   |
        | aprovada            | excluir  |
        | cancelada           | editar   |
        | cancelada           | excluir  |

    Esquema do Cenário: [CT-08] rascunho alheio não se edita nem se exclui
      Dado uma solicitação em rascunho do solicitante, com valor 7.200,00
      E um outro usuário da mesma organização, autenticado
      Quando o outro usuário tenta "<operacao>" a solicitação
      Então a operação é recusada
      E a solicitação continua existindo, em rascunho, com valor 7200.00

      Exemplos:
        | operacao |
        | editar   |
        | excluir  |

    Esquema do Cenário: [CT-09] solicitação de outra organização não é alcançável
      Dado uma solicitação em rascunho na organização "Acme", com valor 7.200,00
      E um usuário autenticado no painel da organização "Globex"
      Quando ele tenta "<operacao>" aquela solicitação pelo identificador dela
      Então a operação é recusada
      E a solicitação da Acme continua existindo, em rascunho, com valor 7200.00

      Exemplos:
        | operacao |
        | ler      |
        | editar   |
        | excluir  |
```

**Camada**: `Feature` por componente Livewire (`EditSolicitacaoCompra`, ação de exclusão da
listagem) para CT-05..CT-08 — é onde a policy é de fato consultada. CT-09 vai para
`tests/FeatureTenancy/`, porque o escopo por organização só existe com `Filament::getTenant()`
resolvido (`app/Traits/BelongsToTenant.php:64-71`: *sem tenant, sem escopo*).

**Nota de discriminação**: CT-05 altera **os três campos**, e o `Então` afirma os três. A primeira
versão alterava só o `valor` — escolha defensável (é o campo que decide o fluxo) que deixava
RQ-02 provado para **um** dos três campos: um formulário de edição com schema parcial, ou com
`descricao` e `centro_custo_id` em `disabled`, passaria inteiro. O campo decisivo continua na
edição, agora acompanhado.

Nos cenários de recusa (CT-07, CT-08), o `Então` afirma **o valor gravado**, não só que a operação
foi recusada: uma implementação que recusa **depois** de gravar passaria no "recusado" sozinho.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a condição de rascunho existe só na policy (esconde o botão) e não na barreira do model — a edição por outro caminho passa | CT-07 (chamando a operação diretamente, ver CT-20 para o padrão) |
| M2 | a condição de identidade (`solicitante_id === $user->id`) é esquecida; qualquer um edita rascunho alheio | CT-08 |
| M3 | a restrição vale para `editar` e é esquecida em `excluir` (verbo irmão) | CT-07 e CT-08, linhas `excluir` |
| M4 | a solicitação é gravada e **depois** a regra é conferida (recusa tardia) | CT-07, pelo `E ... com valor 7200.00` |
| M5 | `aprovada` e `cancelada` são tratadas como editáveis porque a checagem é `!== aguardando_*` em vez de `=== rascunho` | CT-07, linhas `aprovada` e `cancelada` |
| M6 | a listagem filtra por organização mas o acesso por identificador não (route binding sem escopo) | CT-09 |

---

## Regra R3 — O envio encaminha ao gestor do centro de custo; sem gestor, não sai do rascunho

> `RQ-04`, premissa A-10 · área **fluxo** (completo) · técnica: **tabela estado × evento**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: ao enviar, a solicitação passa a aguardar a decisão do gestor do centro de custo; se o
         centro não tem gestor, o envio é recusado e ela permanece em rascunho

    Cenário: [CT-10] o envio coloca a solicitação sob a decisão do gestor do centro
      Dado uma solicitação em rascunho do solicitante, no centro "Infraestrutura", cuja gestora é
            a Beatriz
      Quando o solicitante envia a solicitação
      Então a solicitação passa a aguardar a decisão do gestor
      E o aviso de aprovação pendente daquela solicitação é endereçado à Beatriz
      E nenhuma etapa de aprovação foi registrada ainda

    Cenário: [CT-49] o aviso do envio vai para a gestora daquele centro, e só para ela
      Dado o centro "Infraestrutura", criado primeiro, cuja gestora é a Beatriz
      E o centro "Operações", criado depois, cuja gestora é a Carla
      E uma solicitação em rascunho no centro "Operações"
      Quando o solicitante envia a solicitação
      Então foi enviado exatamente um aviso de aprovação pendente no total
      E ele foi para a Carla

    Esquema do Cenário: [CT-60] quem decide é a gestora daquele centro, e só ela
      Dado o centro "Infraestrutura", criado primeiro, cuja gestora é a Beatriz
      E o centro "Operações", criado depois, cuja gestora é a Carla
      E uma solicitação do centro "Operações" aguardando a decisão do gestor
      Quando "<pessoa>" tenta aprovar a solicitação
      Então a situação da solicitação passa a ser "<situacao_final>"
      E o número de etapas daquela solicitação é <etapas>

      Exemplos:
        | pessoa  | situacao_final    | etapas |
        | Carla   | aprovada          | 1      |
        | Beatriz | aguardando_gestor | 0      |

    Cenário: [CT-11] @premissa (A-10) centro de custo sem gestor não recebe envio
      Dado uma solicitação em rascunho no centro "Novo Centro", que está sem gestor
      Quando o solicitante envia a solicitação
      Então o envio é recusado
      E a solicitação continua em rascunho
      E nenhuma etapa de aprovação foi registrada
      E nenhum e-mail de aprovação pendente foi enviado

    Esquema do Cenário: [CT-12] só o rascunho se envia
      Dado uma solicitação do solicitante na situação "<situacao>"
      Quando o solicitante envia a solicitação
      Então o envio é recusado
      E a solicitação continua na situação "<situacao>"
      E o número de etapas daquela solicitação não mudou
      E nenhum aviso de aprovação pendente foi enviado

      Exemplos:
        | situacao            |
        | aguardando_gestor   |
        | aguardando_diretor  |
        | aprovada            |
        | cancelada           |

    Cenário: [CT-13] quem não é o solicitante não envia
      Dado uma solicitação em rascunho do solicitante
      E o gestor do centro autenticado
      Quando o gestor tenta enviar a solicitação
      Então o envio é recusado
      E a solicitação continua em rascunho
      E nenhum e-mail de aprovação pendente foi enviado
```

**Camada**: `Feature`. CT-10, CT-12, CT-49 e CT-60 pela ação de tabela
(`callAction(TestAction::make('enviar')->table($solicitacao))`, molde de
`tests/Kit/ConviteTest.php:262`); CT-11 e CT-13 chamando a operação **fora da tela**, porque é lá
que a barreira precisa existir (`.ai/rules/filament.md` → *asserção de identidade vive no model*).

**Nota de discriminação — CT-49 e CT-60 existem por causa do "do"**. RQ-04 diz "o gestor **do**
centro de custo", e um conjunto com **um único centro em banco** não distingue isso de "qualquer
gestor da organização". A 1ª rodada da revisão adversarial trouxe o segundo centro; a 2ª mostrou
que **isso não bastava**: a solicitação estava no centro **criado primeiro**, e `CentroCusto::first()`
devolve exatamente a gestora certa. O cenário parecia discriminante e não era. Agora a solicitação
nasce no **segundo** centro — a técnica de registro vizinho só vale quando o registro sob teste
**não é o primeiro**.

A 2ª rodada também apontou que CT-49 tinha **uma ação dentro do `Então`** ("ao tentar aprovar…"),
o que mistura dois comportamentos. Foram separados: **CT-49** afirma o efeito (o aviso) e **CT-60**
afirma a autoridade (quem decide). E o `Então` de CT-49 passou a ser de **mundo fechado** — *"foi
enviado exatamente um aviso no total"* —, porque enumerar quem não recebeu deixa de fora todo
destinatário que ninguém pensou em nomear.

O `Então` de CT-10 também foi reescrito: dizia *"a Beatriz é quem pode decidi-la"*, que é termo de
domínio não observável e delegava o oráculo a outro cenário. Agora afirma o destinatário do aviso,
que é observável ali mesmo.

CT-11 afirma **três** não-efeitos, e CT-12 passou a afirmar dois: "recusado" sozinho passa numa
implementação que recusa depois de transicionar ou depois de gravar a etapa.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o envio pula a etapa do gestor e vai direto para o diretor (ou direto para aprovada) quando o valor é baixo | CT-10 |
| M2 | gestor nulo é tratado como "não precisa de aprovação" e a solicitação é aprovada de imediato | CT-11 |
| M3 | gestor nulo passa: a solicitação avança e fica presa sem aprovador possível | CT-11 |
| M4 | a solicitação transiciona **antes** de a verificação do gestor rodar | CT-11 (`continua em rascunho`) |
| M5 | qualquer pessoa da organização pode enviar a solicitação de outra | CT-13 |
| M6 | reenviar o que já está em trânsito grava uma segunda vez / volta a etapa | CT-12, linhas `aguardando_*` |
| M7 | o destinatário/decisor é resolvido como "todos os gestores da organização" ou "o gestor do primeiro centro", sem amarrar ao centro da solicitação | **CT-49** — trazido pela revisão adversarial |

---

## Regra R4 — Acima de R$ 5.000 exige o diretor, e depois do gestor

> `RQ-05`, premissa A-04 · área **alçada** (completo) · técnica: **BVA 3-valores** (fronteira R$
> 5.000,00, incremento **0,01** — `decimal(12,2)`) + **ordem de eventos**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: uma solicitação de valor acima de R$ 5.000,00 exige, além da aprovação do gestor, a
         aprovação de um diretor — e ela vem depois

    Esquema do Cenário: [CT-14] o limite é estritamente maior
      Dado um limite de alçada configurado em R$ 1.000,00
      E uma solicitação enviada, de valor <valor>, aguardando a decisão do gestor
      Quando o gestor aprova a solicitação
      Então a solicitação fica "<resultado>"
      E o valor gravado continua sendo <valor>

      Exemplos:
        | valor   | resultado           | # borda   |
        | 999.99  | aprovada            | borda−1   |
        | 1000.00 | aprovada            | borda     |
        | 1000.01 | aguardando_diretor  | borda+1   |

    Esquema do Cenário: [CT-56] a alçada compara números, não texto
      Dado uma solicitação enviada, de valor <valor>, aguardando a decisão do gestor
      Quando o gestor aprova a solicitação
      Então a solicitação fica "<resultado>"

      Exemplos:
        | valor    | resultado           | # ordem de grandeza          |
        | 900.00   | aprovada            | menos dígitos que o limite   |
        | 12000.00 | aguardando_diretor  | mais dígitos que o limite    |

    Esquema do Cenário: [CT-15] o limite de R$ 5.000,00 vale sem nenhum ajuste do teste
      Dado uma solicitação de valor <valor> aguardando a decisão do gestor, num ambiente em que o
            teste não tocou em nenhuma configuração de limite
      Quando o gestor aprova a solicitação
      Então a solicitação fica "<resultado>"

      Exemplos:
        | valor   | resultado           | # lado do limite do card |
        | 4999.99 | aprovada            | abaixo de R$ 5.000,00    |
        | 5000.01 | aguardando_diretor  | acima de R$ 5.000,00     |

    Cenário: [CT-16] o diretor não decide antes do gestor
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor
      E um diretor autenticado
      Quando o diretor aprova a solicitação
      Então a aprovação é recusada
      E a solicitação continua aguardando a decisão do gestor
      E nenhuma etapa de aprovação foi registrada

    Cenário: [CT-17] acima do limite, a segunda mão conclui — e só ela
      Dado uma solicitação de valor 8.000,00 que a gestora Beatriz já aprovou, e que por isso
            aguarda a decisão do diretor
      Quando a diretora Ana aprova a solicitação
      Então a solicitação fica aprovada
      E há duas etapas daquela solicitação, nesta ordem: a etapa de gestor aprovada pela Beatriz e
        a etapa de diretor aprovada pela Ana
```

**Camada**: `Feature`. **Não `Unit`**, e o motivo não é estilo: o cálculo lê `config()` e o valor
passa por cast de model — `tests/Unit` não está ligado a nenhum `TestCase` neste projeto e roda sem
container.

**Nota de discriminação — a mais importante deste conjunto**:

- os três valores de CT-14 usam o incremento do tipo (`0,01`), não 4.000 / 5.000 / 6.000. Um
  conjunto com valores redondos não distingue `>` de `>=`, que é exatamente a ambiguidade que A-04
  resolveu no requisito. **CT-14 injeta um limite de R$ 1.000,00**, deliberadamente **diferente do
  default**: a segunda rodada da revisão adversarial mostrou que, com o limite injetado igual ao de
  fábrica, CT-15 vira subconjunto estrito de CT-14 e o mutante "o default está errado" fica sem
  matador de verdade. Com números distintos, CT-14 mede **só o operador** e CT-15 mede **só o
  número do card**;
- **CT-56 mede o tipo da comparação, que a BVA não vê.** Todos os valores do conjunto anterior
  tinham 4 dígitos inteiros ou menos (3.000, 4.999,99, 5.000,01, 7.200,55, 8.000). Uma comparação
  **lexicográfica** — que é o erro natural quando o próprio SFDIPOT deste arquivo avisa que
  `decimal` volta do SQLite como **string** — acerta todos eles e erra `'12000.00' > '5000.00'`,
  que é **falso** em texto. O resultado seria uma compra de R$ 12.000 aprovada só pelo gestor: o
  defeito de maior impacto financeiro possível nesta feature, invisível para uma BVA impecável. A
  linha `900.00` fecha o outro sentido (`'900.00' > '5000.00'` é **verdadeiro** em texto);
- **CT-15 não toca em configuração nenhuma** — é o cenário do número literal do card. E ele é
  **bilateral**, corrigido pela revisão adversarial: a versão anterior tinha uma linha só
  (`5.000,01 → diretor`) precedida de um `Dado` que *afirmava* o limite em vez de exercitá-lo. Como
  oráculo isso não vale nada: **qualquer default abaixo de 5.000,01** — R$ 500, R$ 1.000 — passaria.
  Com as duas linhas, o default só passa se estiver entre 4.999,99 e 5.000,01, que é o intervalo
  onde só cabe o número do requisito;
- CT-14 afirma **o valor gravado** junto com a situação, o que mata a implementação que compara
  `(int) $valor`: `(int) 5000.01 === 5000` não exigiria diretor, e a linha `borda+1` fica vermelha;
- **CT-17 teve a primeira aprovação movida para o `Dado`**. Antes, o `Quando` tinha duas ações
  ("o gestor aprova e, em seguida, o diretor aprova") e o **estado intermediário nunca era
  afirmado** — que é justamente o que separa a implementação correta da permissiva quanto à ordem.
  Quem afirma o intermediário agora é CT-14 (linha `borda+1`) e CT-15 (linha de cima do limite).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `>=` no lugar de `>` — R$ 5.000,00 exatos exigem diretor | CT-14 (linha `borda`) |
| M2 | `<` invertido — só valores **abaixo** do limite exigem diretor | CT-14 (linhas `borda−1` e `borda+1`) |
| M3 | o valor é comparado como inteiro (`(int)` / `floor`), perdendo os centavos da fronteira | CT-14 (linha `borda+1`) |
| M4 | o limite fica cravado com outro número (R$ 500, R$ 50.000) ou o default do config está errado | **CT-15**, agora bilateral. *(A revisão adversarial mostrou que a versão unilateral não matava — e que quem matava de fato era a linha `4999.99` de CT-14, com o limite injetado. A rastreabilidade estava errada, e está corrigida.)* |
| M5 | a ordem se inverte: o diretor decide primeiro e o gestor confirma depois | CT-16 mata a implementação que **exige** o diretor primeiro. ⚠️ **Lacuna declarada** para a implementação **permissiva** (aceita qualquer ordem): ela produz o mesmo resultado final de CT-17. Tentado: (1) afirmar a ordem e o **tipo** de cada etapa em CT-17 — mata a permissiva se e somente se ela gravar a etapa com o tipo de quem decidiu; (2) afirmar o estado intermediário `aguardando_diretor` em CT-14/CT-15 — fecha o caminho "gestor decide e já finaliza". O resíduo é a permissiva que grava tipos corretos: **inexpressável sem um segundo diretor decidindo antes do gestor**, que é CT-16 com outro nome |
| M6 | a etapa do diretor é exigida sempre, independentemente do valor | CT-14 (linhas `borda−1` e `borda`) |
| M7 | a comparação é **lexicográfica** (`decimal` chega como string do SQLite, `strcmp`/`bccomp` mal usado): acerta toda a vizinhança do limite e libera R$ 12.000 sem diretor | **CT-56** — trazido pela 2ª rodada da revisão adversarial |

---

## Regra R5 — Só o aprovador da etapa corrente decide, e a recusa vale para os dois verbos

> `RQ-04`, `RQ-05`, `RQ-06`, premissas A-03, A-07, A-09 · área **autorização** (completo) ·
> técnica: **matriz papel × ação**, com o **verbo** como dimensão

A matriz, com a etapa corrente como linha e a persona como coluna. Cada célula é exercitada nos
**dois verbos** — "aprova **ou** rejeita" é uma regra sobre dois verbos, e uma implementação que
confere o ator em `aprovar` e esquece em `rejeitar` passa em todo conjunto que só testa o primeiro.

| Etapa corrente \ persona | gestor do centro | outro gestor | diretor | solicitante | estranho |
|---|---|---|---|---|---|
| **gestor** | ✅ CT-18 | ❌ CT-18 | ❌ CT-18 | ❌ CT-18 | ❌ CT-18 |
| **diretor** | ❌ CT-19 | ❌ CT-19 | ✅ CT-19 | ❌ CT-19 | ❌ CT-19 |

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: a decisão da etapa corrente cabe apenas a quem a etapa endereça — o gestor do centro de
         custo na primeira, um diretor na segunda — e isso vale tanto para aprovar quanto para
         rejeitar

    Esquema do Cenário: [CT-18] na etapa do gestor, só o gestor daquele centro decide
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor, e a justificativa
            "Sem verba neste trimestre" quando o verbo for rejeitar
      Quando "<persona>" tenta "<verbo>" a solicitação
      Então a situação da solicitação passa a ser "<situacao_final>"
      E o número de etapas daquela solicitação é <etapas>

      Exemplos:
        | persona            | verbo    | situacao_final      | etapas | # célula |
        | gestor do centro   | aprovar  | aguardando_diretor  | 1      | válida   |
        | gestor do centro   | rejeitar | rascunho            | 1      | válida   |
        | gestor de outro    | aprovar  | aguardando_gestor   | 0      | recusa   |
        | gestor de outro    | rejeitar | aguardando_gestor   | 0      | recusa   |
        | diretor            | aprovar  | aguardando_gestor   | 0      | recusa   |
        | diretor            | rejeitar | aguardando_gestor   | 0      | recusa   |
        | solicitante        | aprovar  | aguardando_gestor   | 0      | recusa   |
        | solicitante        | rejeitar | aguardando_gestor   | 0      | recusa   |
        | estranho           | aprovar  | aguardando_gestor   | 0      | recusa   |
        | estranho           | rejeitar | aguardando_gestor   | 0      | recusa   |

    Esquema do Cenário: [CT-19] na etapa do diretor, só um diretor decide
      Dado uma solicitação de valor 8.000,00 já aprovada pela gestora Beatriz, aguardando a
            decisão do diretor, e a justificativa "Fornecedor não homologado" quando o verbo for
            rejeitar
      Quando "<persona>" tenta "<verbo>" a solicitação
      Então a situação da solicitação passa a ser "<situacao_final>"
      E o número de etapas daquela solicitação é <etapas>

      Exemplos:
        | persona                | verbo    | situacao_final      | etapas | # célula |
        | diretor                | aprovar  | aprovada            | 2      | válida   |
        | diretor                | rejeitar | rascunho            | 2      | válida   |
        | outro diretor          | aprovar  | aprovada            | 2      | válida   |
        | outro diretor          | rejeitar | rascunho            | 2      | válida   |
        | gestor que já decidiu  | aprovar  | aguardando_diretor  | 1      | recusa   |
        | gestor que já decidiu  | rejeitar | aguardando_diretor  | 1      | recusa   |
        | solicitante            | aprovar  | aguardando_diretor  | 1      | recusa   |
        | solicitante            | rejeitar | aguardando_diretor  | 1      | recusa   |
        | estranho               | aprovar  | aguardando_diretor  | 1      | recusa   |
        | estranho               | rejeitar | aguardando_diretor  | 1      | recusa   |

    Esquema do Cenário: [CT-20] a barreira também vale fora da tela
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor
      Quando a operação "<verbo>" é executada diretamente pelo solicitante, sem passar pela tela
      Então a operação falha com erro
      E a solicitação continua aguardando a decisão do gestor
      E nenhuma etapa de aprovação foi registrada

      Exemplos:
        | verbo    |
        | aprovar  |
        | rejeitar |

    Cenário: [CT-21] a tela não oferece a decisão a quem não pode decidir
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor
      Quando o solicitante abre a listagem de solicitações
      Então a ação de aprovar não existe na linha daquela solicitação
      E a ação de rejeitar não existe na linha daquela solicitação

    Cenário: [CT-54] a tela retira a decisão de quem já decidiu
      Dado uma solicitação de valor 8.000,00 que a gestora Beatriz já aprovou, e que por isso
            aguarda a decisão do diretor
      Quando a Beatriz abre a listagem de solicitações
      Então a ação de aprovar não existe na linha daquela solicitação
      E a ação de rejeitar não existe na linha daquela solicitação

    Cenário: [CT-22] @premissa (A-09) o gestor do próprio centro aprova a própria solicitação
      Dado uma solicitação de valor 3.000,00 criada pela Beatriz, que é a gestora do centro dela
      Quando a Beatriz aprova a solicitação
      Então a solicitação fica aprovada
      E há exatamente uma etapa daquela solicitação: a de gestor, aprovada pela Beatriz

    Cenário: [CT-23] diretor de outra organização não decide
      Dado uma solicitação de valor 8.000,00 da organização "Acme", aguardando a decisão do
            diretor
      E um diretor da organização "Globex", autenticado no painel da Globex
      Quando ele tenta aprovar aquela solicitação pelo identificador dela
      Então a aprovação é recusada
      E a solicitação da Acme continua aguardando a decisão do diretor
      E continua havendo exatamente uma etapa registrada
```

**Camada**: `Feature`. CT-18, CT-19, CT-21, CT-22 e CT-54 por componente Livewire (ação de tabela);
**CT-20 chamando a operação diretamente**, que é o cenário que `.ai/rules/filament.md` cobra
textualmente (*"barreira sem teste direto não é barreira — o caso que passa pela tela continuaria
verde com a asserção removida"*). CT-23 vai para `tests/FeatureTenancy/`, porque o papel `diretor`
só é visível dentro do contexto da organização (`model_has_roles.team_id`).

**Estouro de teto declarado**: R5 tem **7 cenários** contra o teto de 5 do perfil `completo`. Os
excedentes são CT-23 e CT-54, e os dois ficam porque o gate vence o teto: nenhum outro mata o
mutante *"o papel `diretor` é resolvido sem o contexto da organização"* (todos os demais rodam
single-tenant, onde ele é indistinguível do correto), e nenhum outro mata *"a ação some para
todo mundo"*, que CT-21 sozinho não pega.

### O que a revisão adversarial corrigiu aqui

Três coisas, e as três eram falso ✅:

1. **`Então` condicional é `Então` ausente.** Os dois Esquemas diziam *"E, **quando recusado**, a
   solicitação continua… e nenhuma etapa foi registrada"* — o que deixava as linhas `aceito`
   **sem oráculo nenhum**. Uma implementação em que `rejeitar` pelo gestor devolve sucesso e não
   faz nada passava. Agora o `Então` é **incondicional**: toda linha declara a situação final e a
   contagem de etapas, aceita ou recusada.
2. **A matriz prometia dois verbos e entregava um e meio.** CT-19 tinha 7 linhas, só **duas** no
   verbo `rejeitar`. Faltavam `solicitante | rejeitar`, `estranho | rejeitar` e
   `outro diretor | rejeitar` — e a implementação cuja guarda de `rejeitar` na etapa do diretor é
   *"quem ainda não decidiu esta solicitação"* liberava o **solicitante** e o **estranho** para
   rejeitar, passando nas duas linhas que existiam. As 10 células dos dois verbos estão fechadas.
3. **"Há exatamente uma etapa" não dizia de quem.** Agora é *"o número de etapas **daquela
   solicitação**"* — uma contagem global fica verde com a etapa certa apagada e uma etapa errada
   gravada.

**Nota de discriminação**: as personas são **cinco pessoas distintas**. Colapsar solicitante,
gestor e diretor num só usuário — a tentação óbvia, porque encurta o setup — faria todos os
cenários passarem com a barreira de identidade inteiramente removida.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a identidade do aprovador é conferida em `aprovar` e esquecida em `rejeitar` | CT-18, **CT-19** e CT-20, linhas `rejeitar`. *(Antes da revisão adversarial, CT-19 cobria `rejeitar` em duas células só, e o mutante sobrevivia na etapa do diretor.)* |
| M8 | a guarda de `rejeitar` na etapa do diretor é "quem ainda não decidiu esta solicitação", liberando solicitante e estranho | **CT-19**, linhas `solicitante \| rejeitar` e `estranho \| rejeitar` — trazido pela revisão adversarial |
| M9 | a decisão é aceita e **não faz nada** (retorna sucesso sem transicionar nem gravar) | CT-18 e CT-19, linhas `válida` — só matáveis desde que o `Então` deixou de ser condicional |
| M2 | qualquer pessoa com permissão de ver a tela decide (permission em vez de identidade) | CT-18, linhas `estranho` e `solicitante` |
| M3 | qualquer gestor decide, sem conferir se é o gestor **daquele** centro | CT-18, linha `gestor de outro` |
| M4 | o gestor que já decidiu decide também a etapa do diretor | CT-19, linhas `gestor que já decidiu` |
| M5 | a regra vive só na visibilidade da ação, e a chamada direta passa | CT-20 |
| M6 | há botão para quem não pode agir (a ação aparece e resulta em erro) | CT-21 |
| M10 | a ação é escondida de **todo mundo** (o `visible()` nunca devolve verdadeiro) | **CT-18, linhas `válida`** — `callAction` sobre ação oculta ou desabilitada falha, então a célula válida já prova a presença. *(A 2ª rodada mostrou que o CT-54 original era redundante com isso; ele foi **reespecificado**, não cortado.)* |
| M11 | a visibilidade olha só a situação e não **quem já decidiu**: o gestor continua vendo Aprovar/Rejeitar na etapa do diretor | **CT-54**, na nova especificação — a célula de affordance que nenhum outro cenário exercitava |
| M7 | o papel `diretor` é resolvido fora do contexto da organização e um diretor de outra decide | CT-23 |

---

## Regra R6 — A rejeição exige justificativa, devolve ao rascunho e preserva o histórico

> `RQ-06`, `RQ-07`, `RQ-08`, `RQ-09`, premissas A-07, A-15, A-16 · área **fluxo** (completo) ·
> técnicas: **EP de texto** (vazio ≠ espaços ≠ ausente) + **2-switch** (ciclo de volta)

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: rejeitar exige uma justificativa, devolve a solicitação ao rascunho para correção e não
         apaga o que já aconteceu

    Cenário: [CT-24] a rejeição devolve a solicitação ao rascunho com o motivo registrado
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor
      Quando a gestora Beatriz rejeita a solicitação com a justificativa "Sem verba neste
             trimestre"
      Então a solicitação volta a ficar em rascunho
      E há uma etapa de gestor, rejeitada pela Beatriz, com a justificativa "Sem verba neste
        trimestre"

    Esquema do Cenário: [CT-25] rejeição sem justificativa é recusada, em qualquer etapa
      Dado uma solicitação de valor 8.000,00 aguardando a decisão de "<etapa>"
      Quando quem decide aquela etapa rejeita a solicitação com a justificativa <justificativa>
      Então a rejeição é recusada
      E a solicitação continua aguardando a decisão de "<etapa>"
      E o número de etapas daquela solicitação não mudou

      Exemplos:
        | etapa   | justificativa           | # partição                          |
        | gestor  | a string vazia          | vazia                               |
        | gestor  | três espaços em branco  | só espaços                          |
        | gestor  | a chave não é enviada   | campo ausente do payload            |
        | diretor | a string vazia          | vazia, na segunda etapa             |
        | diretor | três espaços em branco  | só espaços, na segunda etapa        |
        | diretor | a chave não é enviada   | campo ausente, na segunda etapa     |

    Cenário: [CT-26] @premissa (A-15) corrigida e reenviada, a solicitação recomeça pelo gestor
      Dado uma solicitação de valor 8.000,00 que foi aprovada pelo gestor e rejeitada pelo diretor
      Quando o solicitante a envia novamente
      Então ela passa a aguardar a decisão do gestor, e não a do diretor
      E as duas etapas do ciclo anterior continuam registradas: a aprovação do gestor e a
        rejeição do diretor

    Cenário: [CT-53] a solicitação rejeitada volta a ser editável nos três campos
      Dado uma solicitação rejeitada pelo gestor e de volta ao rascunho, com descrição "Notebooks
            para o time", valor 8.000,00 e o centro "Infraestrutura"
      Quando o solicitante salva a edição com descrição "Notebooks e docks", valor 5.000,00 e o
             centro "Operações"
      Então a solicitação gravada tem descrição "Notebooks e docks", valor 5000.00 e o centro
        "Operações"
      E ela continua em rascunho, com a etapa de rejeição ainda registrada

    Cenário: [CT-27] @premissa (A-16) corrigido o valor para dentro do limite, o diretor não entra
      Dado uma solicitação rejeitada pelo gestor, já corrigida de 8.000,00 para 5.000,00 pelo
            solicitante e reenviada, aguardando a decisão do gestor
      Quando o gestor aprova a solicitação
      Então a solicitação fica aprovada

    Cenário: [CT-28] @premissa (A-07) o diretor também rejeita, com as mesmas exigências
      Dado uma solicitação de valor 8.000,00 aprovada pelo gestor, aguardando o diretor
      Quando a diretora Ana rejeita a solicitação com a justificativa "Fornecedor não homologado"
      Então a solicitação volta a ficar em rascunho
      E há uma etapa de diretor, rejeitada pela Ana, com a justificativa "Fornecedor não
        homologado"
```

**Camada**: `Feature`. CT-24, CT-26, CT-27, CT-28 e CT-53 por componente (a ação de rejeitar com o
formulário da modal — `callAction(TestAction::make('rejeitar')->table($s), ['justificativa' => …])`,
molde de `tests/Kit/ConviteEmMassaTest.php:39`). **A linha `ausente` de CT-25 vai pelo model**, com
a chamada direta, porque o formulário não deixa o campo faltar — e a exigência precisa existir onde
um job ou uma rota de API futura chegaria.

**Nota de discriminação**: a justificativa de CT-24 é `"Sem verba neste trimestre"` e o `Então`
afirma **o texto**, não a existência de uma etapa. Uma implementação que grava a etapa com
justificativa vazia (ou que grava a do cenário anterior) passa em "há uma etapa rejeitada". E
**"Sem verba"** é deliberadamente curta: o requisito exige que a justificativa **exista**, não que
tenha tamanho — um mínimo inventado rejeitaria uma justificativa perfeitamente válida.

**CT-53 e CT-27 são o que a revisão adversarial separou.** Havia um cenário só, com **três ações
num `Quando`** ("altera o valor, envia de novo **e** o gestor aprova") e nenhuma afirmação sobre a
correção ter sido gravada. Duas consequências: se a edição falhasse em silêncio, o cenário só
quebraria por efeito indireto; e **RQ-09 ("o solicitante corrige e envia de novo") ficava com
cobertura aparente** — nenhum cenário afirmava que a correção persistia. CT-53 fecha o "corrige"
(e mata a policy que trava a edição de uma solicitação que já tem etapas); CT-27 fecha o
"envia de novo" com a alçada reavaliada, que é o **2-switch com a dimensão do campo exercitada
fora do estado inicial** — onde mora o defeito de recomputação.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a justificativa é exigida só no formulário e não na regra de negócio | CT-25, linha `ausente` |
| M2 | a exigência usa `empty()`/`!== null` e aceita `"   "` | CT-25, linha `só espaços` |
| M3 | a rejeição leva a solicitação a um estado próprio ("rejeitada") em vez de devolvê-la ao rascunho | CT-24, CT-28 |
| M4 | o reenvio depois de uma rejeição do diretor volta a aguardar o **diretor**, pulando o gestor | CT-26 |
| M5 | o reenvio apaga as etapas anteriores (ou o histórico é uma coluna sobrescrita na solicitação) | CT-26 |
| M6 | a alçada é decidida uma vez, no primeiro envio, e não é reavaliada com o valor corrigido | CT-27 |
| M7 | a rejeição do diretor não é implementada | CT-28 |
| M10 | a exigência de justificativa existe no ramo do **gestor** e é esquecida no ramo do **diretor** | **CT-25, linhas `diretor`** — a 2ª rodada mostrou que CT-28 (que rejeita **com** justificativa) não cobria essa metade de M7, e que a **etapa** precisava ser dimensão do Esquema |
| M8 | a etapa é gravada antes da validação da justificativa (recusa tardia) | CT-25 (`nenhuma etapa foi registrada`) |
| M9 | a solicitação devolvida ao rascunho **não volta a ser editável** (a policy de edição exige zero etapas), e o solicitante não consegue corrigir | **CT-53** — trazido pela revisão adversarial |

---

## Regra R7 — Aprovada é estado terminal

> `RQ-10`, premissa A-05 · área **fluxo** (completo) · técnicas: **estado × operação** +
> **idempotência ancorada no agregado** + **concorrência**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: depois de aprovada, a solicitação não muda mais — nenhuma operação a altera

    Esquema do Cenário: [CT-29] nenhuma operação altera a solicitação aprovada
      Dado uma solicitação aprovada, de valor 8.000,00, com duas etapas registradas
      Quando "<quem>" tenta "<operacao>" a solicitação
      Então a operação é recusada
      E a solicitação continua aprovada, com valor 8000.00
      E continua havendo exatamente duas etapas daquela solicitação

      Exemplos:
        | quem            | operacao  |
        | o solicitante   | editar    |
        | o solicitante   | excluir   |
        | o solicitante   | enviar    |
        | o solicitante   | cancelar  |
        | a diretora Ana  | aprovar   |
        | a diretora Ana  | rejeitar  |

    Cenário: [CT-30] aprovar duas vezes não aprova duas vezes
      Dado uma solicitação de valor 3.000,00 aguardando a decisão do gestor
      Quando o gestor aprova a solicitação e, em seguida, aprova de novo
      Então a segunda aprovação é recusada
      E a solicitação está aprovada
      E há exatamente uma etapa daquela solicitação

    Cenário: [CT-31] duas decisões simultâneas produzem uma só
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do diretor
      E dois diretores que carregaram a mesma solicitação antes de qualquer decisão
      Quando os dois aprovam, um após o outro, cada um a partir do que carregou
      Então a primeira aprovação é aceita e a segunda é recusada
      E há exatamente uma etapa de diretor registrada
      E a solicitação está aprovada
```

**Camada**: `Feature`. CT-31 usa o arnês de **duas instâncias carregadas antes da decisão** — não
há como rodar dois processos num teste Pest, e essa é a forma honesta de expor o check-then-act: a
segunda instância tem em memória a situação antiga, exatamente como a segunda aba do navegador. A
implementação que faz `if ($this->situacao === …) { … $this->save(); }` passa nas duas chamadas; a
que faz a troca condicional no banco recusa a segunda.

**Nota de discriminação — idempotência ancorada**: o `Então` de CT-30 afirma **o estado do registro
persistido** (uma etapa, situação aprovada), não o retorno da segunda chamada. Ancorar no retorno
faria o cenário passar por construção.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `aprovada` não é tratada como terminal para **cancelar** (o card só a proíbe explicitamente "antes da aprovação final") | CT-29, linha `cancelar` |
| M2 | `aprovada` bloqueia edição mas não bloqueia nova aprovação — a etapa é gravada de novo | CT-29 (linha `aprovar`) e CT-30 |
| M3 | a decisão é `ler → comparar em memória → salvar`, e duas chamadas concorrentes gravam as duas | CT-31 |
| M4 | a etapa é gravada **antes** de a transição vencer, deixando etapa órfã na corrida perdida | CT-31 (`exatamente uma etapa`) |
| M5 | `enviar` a partir de `aprovada` reinicia o fluxo | CT-29, linha `enviar` |

---

## Regra R8 — O solicitante cancela enquanto a solicitação está em trânsito

> `RQ-11`, premissa A-06 · área **fluxo** (completo) · técnica: **estado × operação × persona**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: o solicitante cancela a própria solicitação a qualquer momento antes da aprovação final,
         e ninguém mais a cancela

    Esquema do Cenário: [CT-32] em trânsito, o solicitante cancela
      Dado uma solicitação do solicitante na situação "<situacao>"
      Quando o solicitante cancela a solicitação
      Então a solicitação fica cancelada
      E nenhuma etapa de aprovação foi acrescentada

      Exemplos:
        | situacao            |
        | aguardando_gestor   |
        | aguardando_diretor  |

    Esquema do Cenário: [CT-33] fora do trânsito, não há o que cancelar
      Dado uma solicitação do solicitante na situação "<situacao>"
      Quando o solicitante cancela a solicitação
      Então o cancelamento é recusado
      E a solicitação continua na situação "<situacao>"
      E o número de etapas daquela solicitação não mudou

      Exemplos:
        | situacao   | # observação                                            |
        | rascunho   | @premissa (A-06) — em rascunho o caminho é excluir       |
        | aprovada   | estado terminal (RQ-10)                                 |
        | cancelada  | estado terminal                                         |

    Esquema do Cenário: [CT-34] só o solicitante cancela
      Dado uma solicitação do solicitante aguardando a decisão do gestor
      Quando "<persona>" cancela a solicitação
      Então o cancelamento é recusado
      E a solicitação continua aguardando a decisão do gestor

      Exemplos:
        | persona          |
        | gestor do centro |
        | diretor          |
        | estranho         |
```

**Camada**: `Feature` — CT-32 e CT-34 por componente (ação de tabela); CT-33 pelo model, porque a
tela esconde a ação e o cenário afirma sobre a **regra**, não sobre a affordance.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o cancelamento vale em qualquer situação, inclusive `aprovada` — "a qualquer momento" lido ao pé da letra | CT-33, linha `aprovada` |
| M2 | o cancelamento grava uma etapa de aprovação (com decisão "cancelada"), poluindo o histórico de RQ-13 | CT-32 |
| M3 | o cancelamento vale só em `aguardando_gestor`, e a solicitação já com o diretor fica presa | CT-32, linha `aguardando_diretor` |
| M4 | qualquer aprovador cancela — o cancelamento é confundido com a rejeição | CT-34 |
| M5 | cancelar duas vezes é aceito e a situação "avança" de novo | CT-33, linha `cancelada` |

---

## Regra R9 — A tela mostra a situação atual

> `RQ-12`, premissa A-12 · área **exibição** (padrão) · técnica: **partição exaustiva do enum**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: a tela mostra em que situação cada solicitação está

    Esquema do Cenário: [CT-35] cada situação aparece com o seu próprio rótulo na listagem
      Dado uma solicitação na situação "<situacao>"
      Quando o solicitante abre a listagem de solicitações
      Então a linha daquela solicitação mostra "<rotulo>"

      Exemplos:
        | situacao            | rotulo              |
        | rascunho            | Rascunho            |
        | aguardando_gestor   | Aguardando gestor   |
        | aguardando_diretor  | Aguardando diretor  |
        | aprovada            | Aprovada            |
        | cancelada           | Cancelada           |

    Esquema do Cenário: [CT-36] a tela da solicitação mostra a situação corrente
      Dado uma solicitação na situação "<situacao>"
      Quando o solicitante abre a solicitação
      Então o campo de situação da tela mostra "<rotulo>"

      Exemplos:
        | situacao            | rotulo              |
        | rascunho            | Rascunho            |
        | aguardando_gestor   | Aguardando gestor   |
        | aguardando_diretor  | Aguardando diretor  |
        | aprovada            | Aprovada            |
        | cancelada           | Cancelada           |

    Cenário: [CT-51] cada linha mostra a situação da sua própria solicitação
      Dado a solicitação "Notebooks" em rascunho e a solicitação "Cadeiras" aguardando o diretor
      Quando o solicitante abre a listagem de solicitações
      Então o estado da coluna de situação, no registro "Notebooks", é "Rascunho"
      E o estado da coluna de situação, no registro "Cadeiras", é "Aguardando diretor"
```

**Camada**: `Feature`, por componente Livewire (`ListSolicitacoesCompra`, `ViewSolicitacaoCompra`) — CT-35, CT-36 e CT-51.
Nada aqui exige navegador: rótulo em badge é HTML renderizado pelo Livewire.

**Nota de discriminação — a partição é exaustiva de propósito**. Amostrar duas situações e deixar
`aguardando_diretor` de fora permitiria exatamente o defeito que importa: a tela dizer "Aprovada"
enquanto ainda falta uma etapa. Com cinco casos no enum, a tabela tem cinco linhas.

**CT-51 é o cenário do registro vizinho, trazido pela revisão adversarial.** CT-35 diz *"a linha
**daquela** solicitação mostra o rótulo"* — só que, com **um único registro em banco**, essa frase
não é falsificável: uma coluna que lê a situação de qualquer linha, ou da primeira, é
indistinguível do correto. O mutante R9-M4 estava declarado morto e era **inmatável por
construção**. Duas solicitações em situações diferentes, na mesma listagem, fecham isso.

**E o oráculo dele é por registro, não por texto** — correção da 2ª rodada. Materializado como
`assertSee('Rascunho')->assertSee('Aguardando diretor')`, CT-51 passaria com os **rótulos trocados
entre as duas linhas**, que é exatamente a conjunção de substrings que este arquivo condena em
CT-37. A tradução para Pest é a assertion de estado de coluna **com o registro alvo**
(`assertTableColumnStateSet('situacao', …, record: $notebooks)`), nunca `assertSee`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | um rótulo faltando no mapeamento, e a coluna mostra o valor cru (`aguardando_diretor`) | CT-35 (a linha correspondente) |
| M2 | `aguardando_diretor` cai no mesmo rótulo de `aprovada` (o `match` agrupa os dois) | CT-35, CT-36 |
| M3 | a listagem mostra a situação e a tela de detalhe não, **ou a mapeia para só alguns valores** | CT-36, agora com a partição **exaustiva** nas duas telas. *(A 2ª rodada apontou que a tela de detalhe tinha um caso só — `aguardando_diretor` — e que "mostra o valor cru" sobrevivia ali para as outras quatro situações.)* |
| M4 | a coluna lê a situação da primeira linha / de qualquer solicitação | **CT-51**. *(CT-35 era o matador declarado e, com um único registro em banco, era **inmatável por construção** — achado da revisão adversarial.)* |
| M5 | o "Aguardando diretor" da tela de detalhe vem do rótulo de um filtro ou de uma legenda, não do campo do registro | CT-36, agora ancorado no **campo de situação** e não em texto solto na página |

---

## Regra R10 — A tela mostra quem decidiu cada etapa

> `RQ-13`, premissas A-12, A-15 · área **exibição** (padrão) · técnicas: EP + **ordenação com
> empate**

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: a tela da solicitação mostra, para cada etapa, quem decidiu, o que decidiu e o motivo

    Cenário: [CT-37] cada etapa mostra o seu próprio decisor, a sua decisão e o seu motivo
      Dado uma solicitação de valor 8.000,00 aprovada pela gestora Beatriz e depois rejeitada
            pela diretora Ana, com a justificativa "Fornecedor não homologado"
      Quando o solicitante abre a solicitação
      Então o primeiro bloco do histórico traz, juntos, "Gestor", "Beatriz" e "Aprovada", sem
        nenhuma justificativa
      E o segundo bloco traz, juntos, "Diretor", "Ana", "Rejeitada" e "Fornecedor não homologado"

    Cenário: [CT-48] o histórico é o daquela solicitação, e só o dela
      Dado a solicitação "Notebooks" rejeitada pela gestora Beatriz com a justificativa "Sem verba
            neste trimestre"
      E a solicitação "Cadeiras" rejeitada pela diretora Ana com a justificativa "Fornecedor não
        homologado"
      Quando o solicitante abre "Notebooks"
      Então o histórico tem exatamente um bloco, com "Beatriz" e "Sem verba neste trimestre"
      E não mostra "Ana" nem "Fornecedor não homologado"

    Cenário: [CT-38] as etapas aparecem na ordem em que aconteceram
      Dado uma solicitação cujas duas etapas foram registradas no mesmo instante e com a mesma
            decisão: primeiro a aprovação da gestora Beatriz, depois a aprovação da diretora Ana
      Quando o solicitante abre a solicitação
      Então a etapa da Beatriz aparece antes da etapa da Ana

    Cenário: [CT-39] @premissa (A-15) o motivo da rejeição sobrevive ao reenvio
      Dado uma solicitação rejeitada pela gestora Beatriz com a justificativa "Sem verba neste
            trimestre", já reenviada pelo solicitante
      Quando o solicitante abre a solicitação
      Então a tela continua mostrando a rejeição da Beatriz com a justificativa "Sem verba neste
        trimestre"
```

**Camada**: `Feature`, por componente (`ViewSolicitacaoCompra`) — CT-37, CT-38, CT-39 e CT-48.

**Nota de discriminação**: CT-37 usa **duas pessoas distintas com decisões opostas**. Com uma etapa
só, ou com as duas decididas pela mesma pessoa, a implementação que mostra sempre o último decisor
(ou sempre o solicitante) passa. CT-38 força o **empate de `created_at`** — com timestamps
diferentes, qualquer ordenação acerta por acidente; empatados, só um desempate determinístico
mantém a ordem.

### O oráculo de CT-37 é pareado, e isso foi achado da revisão adversarial

A versão anterior afirmava os tokens **soltos** — "Beatriz", "aprovada", "Ana", "rejeitada",
"Fornecedor não homologado" — cada um com o seu `assertSee`. Isso passa com o **pareamento
invertido** (Beatriz–rejeitada, Ana–aprovada) e com a justificativa colada na etapa errada, que é
literalmente o mutante R10-M3 declarado morto ali. A implementação que produz isso é banal e
tentadora: um infolist com `TextEntry::make('etapas.decidido_por.name')->listWithLineBreaks()` ao
lado de `TextEntry::make('etapas.decisao')` — **duas listas paralelas**, que a tela renderiza lado a
lado e que ninguém garante estarem alinhadas.

O `Então` agora afirma **blocos**: cada entrada do histórico com o seu trio junto, na ordem. Na
tradução para Pest, isso é assertion por entrada do repeater ou `assertSeeInOrder` sobre a
sequência inteira — nunca conjunção de substrings.

**CT-48 é a segunda metade do mesmo achado**: nenhum cenário do conjunto tinha **duas solicitações
em banco**, então um histórico que lista todas as etapas da organização (relação sem escopo, ou
`EtapaAprovacao::all()`) era indistinguível do correto — e vaza a justificativa que uma pessoa
escreveu sobre a compra de outra.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a tela mostra o nome do solicitante em vez do decisor | CT-37 |
| M2 | a tela mostra só a última etapa (ou só a primeira) | CT-37 |
| M3 | a justificativa não é exibida, ou é exibida na etapa errada | CT-37, **com o oráculo pareado**. *(Com os tokens soltos da versão anterior, o mutante sobrevivia — achado da revisão adversarial.)* |
| M6 | decisores e decisões saem em **listas paralelas** desalinhadas (pareamento invertido) | CT-37 |
| M7 | o histórico lista as etapas de todas as solicitações, sem filtrar pela que está aberta | **CT-48** — trazido pela revisão adversarial |
| M4 | a ordenação é por chave primária decrescente / sem cláusula de ordem | CT-38 — ⚠️ **matador parcial**. **Lacuna declarada**: distinguir "ordenado por `created_at` com desempate" de "ordenado por `id`" exigiria gravar as etapas com `id` fora de ordem, o que o arnês não produz sem `forceFill` de chave primária. Tentado: `freezeTime()` para empatar `created_at` (feito, e mata a ordenação por `created_at` **sem** desempate) |
| M11 | a ordenação é **alfabética pelo nome do decisor** | CT-37 e CT-38, com a diretora batizada **Ana** e a gestora **Beatriz**: a ordem cronológica passou a ser o **inverso** da alfabética. *(Custo zero, e a 2ª rodada mostrou que com "Rui" depois de "Beatriz" as duas ordens coincidiam e o mutante sobrevivia sem estar declarado.)* |
| M12 | a ordenação é pela **decisão** (`aprovada` antes de `rejeitada`) | CT-38, cujas duas etapas passaram a ter a **mesma** decisão |
| M5 | o histórico é apagado no reenvio | CT-39 |

---

## Regra R11 — Só o próximo aprovador é notificado, por e-mail, uma vez

> `RQ-14`, premissa A-11 · área **notificação** (padrão) · técnica: **rastreio de efeito** —
> primeiro o *quê* (canal `mail`, destinatário), depois as direções

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: cada transição que deixa uma etapa pendente avisa por e-mail quem tem de decidi-la, e
         ninguém mais

    Cenário: [CT-40] o envio avisa o gestor do centro por e-mail
      Dado uma solicitação em rascunho no centro cujo gestor é a Beatriz
      Quando o solicitante envia a solicitação
      Então a Beatriz recebe, pelo canal de e-mail, um aviso de aprovação pendente referente a
        essa solicitação
      E o solicitante não recebe nenhum aviso

    Cenário: [CT-41] só os aprovadores da vez são avisados, uma vez cada
      Dado uma solicitação de valor 8.000,00 da organização "Acme", aguardando a decisão do gestor
      E na Acme há dois diretores e um usuário comum, e na "Globex" há um terceiro diretor
      Quando o gestor aprova a solicitação
      Então foram enviados exatamente dois avisos no total
      E os destinatários deles são, exatamente, os dois diretores da Acme

    Cenário: [CT-58] reenviada depois da rejeição, a solicitação avisa a gestora de novo
      Dado uma solicitação rejeitada pela gestora Beatriz e de volta ao rascunho, cujo aviso do
            primeiro envio já havia sido enviado
      Quando o solicitante envia a solicitação de novo
      Então a Beatriz recebe um segundo aviso de aprovação pendente daquela solicitação

    Cenário: [CT-59] cada gestora é avisada da solicitação dela
      Dado a solicitação "Notebooks", de 7.200,55, em rascunho no centro cuja gestora é a Beatriz
      E a solicitação "Cadeiras", de 3.000,00, já enviada no centro cuja gestora é a Carla
      Quando o solicitante envia "Notebooks"
      Então a Beatriz recebe um aviso cuja solicitação referida é "Notebooks", com o valor 7200.55
      E nenhum aviso novo é enviado à Carla

    Esquema do Cenário: [CT-42] sem próxima etapa, ninguém é avisado
      Dado uma solicitação de valor <valor> na situação "<situacao_inicial>"
      Quando "<quem>" executa "<acao>"
      Então a solicitação fica "<situacao_final>"
      E nenhum aviso de aprovação pendente é enviado

      Exemplos:
        | valor   | situacao_inicial    | quem         | acao      | situacao_final |
        | 3000.00 | aguardando_gestor   | o gestor     | aprovar   | aprovada       |
        | 8000.00 | aguardando_diretor  | o diretor    | aprovar   | aprovada       |
        | 8000.00 | aguardando_gestor   | o gestor     | rejeitar  | rascunho       |
        | 8000.00 | aguardando_diretor  | o diretor    | rejeitar  | rascunho       |
        | 8000.00 | aguardando_gestor   | o solicitante| cancelar  | cancelada      |

    Cenário: [CT-43] o aviso não sai se a decisão não se completa
      Dado uma solicitação de valor 8.000,00 aguardando a decisão do gestor
      E que o registro da etapa de aprovação falhará ao ser gravado
      Quando o gestor aprova a solicitação
      Então a operação falha
      E a solicitação continua aguardando a decisão do gestor
      E nenhum aviso de aprovação pendente é enviado
```

**Camada**: `Feature` — CT-40, CT-42, CT-43, CT-58 e CT-59. CT-41 vai para `tests/FeatureTenancy/`: só com `permission.teams` ligado o
papel `diretor` fica preso a uma organização, e sem isso o diretor da Globex seria indistinguível
dos da Acme — o cenário mediria nada.

**Arnês de CT-43, declarado**: a falha é injetada por um listener de `creating` na etapa de
aprovação que lança exceção. É a forma de **falhar depois do ponto em que a notificação seria
disparada** — afirmar `nenhum aviso enviado` num caminho de pré-validação (justificativa vazia,
pessoa errada) não distinguiria implementação nenhuma, porque ali nada seria enviado de qualquer
forma. Alternativa avaliada e descartada: derrubar a tabela por DDL, que funciona em SQLite mas
acopla o cenário ao banco de teste.

**Estouro de teto declarado**: **7 cenários** numa área `padrão` (teto 3). Três são o custo
declarado da técnica de rastreio de efeito, mais a atomicidade (CT-40 a CT-43); os outros três
vieram da 2ª rodada da revisão adversarial e cada um fecha uma direção que faltava:

- **CT-58 — a direção do tempo.** Todo o 2-switch do conjunto (CT-26, CT-27, CT-39, CT-53) afirmava
  **estado e histórico**, nunca o **efeito**. Um guard de idempotência banal — `if
  ($this->notificado_em === null)` — passa em todos os cenários de notificação e faz a solicitação
  corrigida e reenviada **nunca mais avisar ninguém**. RQ-14 quebrando exatamente no ciclo que
  RQ-08 e RQ-09 descrevem.
- **CT-59 — o registro vizinho aplicado ao *payload*.** CT-40 dizia *"um aviso **referente a essa
  solicitação**"* com **uma única solicitação em banco**: a frase não era falsificável, pelo mesmo
  argumento que justificou CT-48 e CT-51. Uma notificação que monta valor e descrição a partir de
  `SolicitacaoCompra::first()` era indistinguível do correto — e o impacto é o I=3 desta área:
  valor e descrição da compra de outra pessoa dentro de um e-mail.
- **CT-41 passou a mundo fechado.** Enumerar não-destinatários ("o usuário comum", "o diretor da
  Globex") deixa passar todo destinatário que ninguém pensou em nomear — inclusive o gestor que
  acabou de aprovar e o próprio solicitante. A contagem total fecha o conjunto.

**Correção da revisão adversarial em CT-42**: o `Dado` dizia *"uma solicitação na situação de
partida de `<transicao>`"* — a situação inicial ficava **indefinida** nas linhas de rejeição e de
cancelamento, e cenário cuja precondição não é reproduzível não é cenário. Agora cada linha declara
valor, situação inicial, ator, ação e situação final, e a rejeição pelo **diretor** entrou como
linha própria: era a única transição sem próxima etapa que ninguém exercitava.

**Nota de discriminação**: o `Então` de CT-40 nomeia **o canal**. "Uma notificação foi enviada"
passa com a notificação indo para o banco, para o Slack, para qualquer lugar — e RQ-14 diz
"notificar **por e-mail**". A assertion é sobre o canal `mail` e sobre o destinatário, junto.
CT-40 roda **sem** `Notification::fake()`, para que o corpo do e-mail e a URL montada pelo painel
sejam de fato renderizados (`MAIL_MAILER=array` no `phpunit.xml` garante que nada sai).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o aviso é enviado ao solicitante em vez do aprovador | CT-40 |
| M2 | o aviso vai por outro canal (`database`, notificação de tela) e nenhum e-mail sai | CT-40 |
| M3 | o aviso é enviado a **todos** os diretores da instalação, não só aos da organização | CT-41 |
| M4 | o aviso é enviado também na aprovação final, na rejeição ou no cancelamento | CT-42 |
| M5 | o disparo acontece antes da gravação da etapa e escapa quando ela falha | CT-43 |
| M6 | o aviso é enviado duas vezes (uma por aprovador encontrado, dentro de um laço que reenvia a todos) | CT-41, agora por **contagem total** e não por enumeração. ⚠️ **Lacuna declarada**: a duplicação que só aparece com a fila real (job reenfileirado após falha parcial) não é observável com `QUEUE_CONNECTION=sync` no `phpunit.xml`. Tentado: `Queue::fake()` para contar despachos — mede o despacho, não a entrega, e não distingue o retry |
| M7 | um guard de idempotência (`notificado_em`, flag booleana, `firstOrCreate`) impede o **segundo** aviso: a solicitação corrigida e reenviada nunca chega ao gestor | **CT-58** — trazido pela 2ª rodada |
| M8 | o aviso é montado a partir da solicitação errada (`SolicitacaoCompra::first()`, a última criada) | **CT-59** — trazido pela 2ª rodada |
| M9 | o laço de destinatários inclui quem já decidiu e/ou o solicitante | CT-41, pela contagem total. *(A enumeração anterior nomeava só o usuário comum e o diretor de outra organização — todo destinatário não nomeado passava.)* |

---

## Regra R12 — Quem define o gestor de um centro de custo é a administração da organização

> `RQ-04` pela premissa **A-08** do `00-requisito.md` · área **autorização** (completo) ·
> técnicas: **matriz papel × ação** + CRUD

Esta regra não está na letra do card, e está na linha de base: A-08 declara a premissa e nomeia a
consequência — **quem edita quem é o gestor se nomeia aprovador das próprias compras**. É a
escalada de privilégio desta entrega, e ela não gera erro nenhum quando esquecida.

```gherkin
# language: pt
Funcionalidade: Centro de custo

  Regra: definir quem é o gestor de um centro de custo é operação de administração da
         organização, fora do alcance do usuário comum do negócio

    Cenário: [CT-62] o usuário comum do negócio opera a própria feature
      Dado um usuário comum do negócio, autenticado no painel da organização
      Quando ele abre a listagem de solicitações de compra
      Então a listagem é exibida

    Esquema do Cenário: [CT-44] @premissa (A-08) o usuário comum não alcança o cadastro
      Dado um usuário comum do negócio, autenticado no painel da organização
      Quando ele tenta "<operacao>" no cadastro de centros de custo
      Então o acesso àquela tela é recusado com 403

      Exemplos:
        | operacao                      |
        | abrir a listagem              |
        | abrir o formulário de criação |
        | abrir o formulário de edição  |

    Cenário: [CT-52] @premissa (A-08) o usuário comum não grava a troca de gestor
      Dado um centro "Infraestrutura" cuja gestora é a Beatriz
      E um usuário comum do negócio que conseguiu montar o formulário de edição daquele centro
      Quando ele submete o salvamento nomeando a si mesmo como gestor
      Então o salvamento é recusado
      E a gestora gravada do centro continua sendo a Beatriz

    Cenário: [CT-45] a administração cadastra o centro e define o gestor
      Dado a administradora da organização "Acme" autenticada no painel da Acme
      E a Beatriz, que pertence à Acme
      Quando ela cria um centro de custo "Infraestrutura" com a Beatriz como gestora
      Então existe um centro "Infraestrutura" na organização Acme, cuja gestora é a Beatriz

    Cenário: [CT-61] o gestor escolhido tem de ser da própria organização
      Dado a administradora da organização "Acme" autenticada no painel da Acme
      E o Daniel, que pertence apenas à organização "Globex"
      Quando ela cria um centro de custo "Infraestrutura" indicando o Daniel como gestor pelo
             identificador dele
      Então a criação é recusada
      E nenhum centro de custo é gravado

    Cenário: [CT-46] a troca de gestor é gravada no mesmo registro
      Dado um centro "Infraestrutura" cuja gestora é a Beatriz, e nenhum outro centro na
            organização
      Quando a administradora salva o centro com a Carla como gestora
      Então continua havendo um único centro na organização, com o mesmo identificador
      E a gestora gravada dele é a Carla

    Esquema do Cenário: [CT-55] @premissa (A-18) a troca alcança a solicitação JÁ enviada
      Dado uma solicitação enviada enquanto a gestora do centro ainda era a Beatriz
      E que a gestora do centro foi trocada para a Carla depois disso
      Quando "<pessoa>" tenta aprovar a solicitação
      Então a situação da solicitação passa a ser "<situacao_final>"
      E o número de etapas daquela solicitação é <etapas>

      Exemplos:
        | pessoa               | situacao_final    | etapas |
        | Carla, gestora atual | aprovada          | 1      |
        | Beatriz, ex-gestora  | aguardando_gestor | 0      |

    Cenário: [CT-50] centro de custo de outra organização não é alcançável
      Dado um centro "Infraestrutura" da organização "Acme", cuja gestora é a Beatriz
      E a administradora da organização "Globex", autenticada no painel da Globex
      Quando ela abre o formulário de edição daquele centro pelo identificador dele
      Então o registro não é encontrado
      E a gestora gravada do centro da Acme continua sendo a Beatriz

    Cenário: [CT-47] salvar o centro sem alterar nada mantém o mesmo registro
      Dado um centro de custo "Infraestrutura" já cadastrado, e nenhum outro centro na organização
      Quando a administradora salva o centro sem alterar nenhum campo
      Então nenhum erro de validação é apresentado
      E continua havendo um único centro na organização, com o mesmo identificador, o mesmo nome
        e a mesma gestora
```

**Camada**: componente Livewire, e a suíte se divide por uma razão de arnês, não de gosto —
**CT-44 e CT-52 em `tests/Feature`** (a subtração do `panel_user` roda nos dois modos) e **CT-45,
CT-46, CT-47, CT-50 e CT-55 em `tests/FeatureTenancy`**, porque a persona administradora da
organização só existe com a tenancy ligada (ver a ressalva no [Setup Global](#personas)). CT-45 e
CT-47 são o [gate de tela de escrita](#gate-de-tela-de-escrita) para as rotas `create` e `edit` de
centros de custo.

**Estouro de teto declarado**: R12 tem **7 cenários** contra o teto de 5. Quatro deles vieram da
revisão adversarial, e cada um fecha um caminho distinto para a mesma escalada de privilégio de
A-08 — que é a consequência mais cara desta entrega e a que não gera erro nenhum quando esquecida.

### O que a revisão adversarial corrigiu aqui

1. **`Então` vácuo.** CT-44 afirmava *"e o gestor do centro continua sendo a pessoa que era"* nas
   linhas `abrir a listagem` e `abrir o formulário` — onde **nada foi tentado alterar**. Não-efeito
   só vale onde havia efeito possível. A afirmação de não-efeito foi para **CT-52**, que de fato
   submete a troca; e CT-44 ganhou um oráculo que **discrimina a causa do 403**: o mesmo usuário,
   na mesma sessão, abre outra tela do painel. Sem isso, um 403 do painel inteiro (papel sem
   `roles.painel`, sessão perdida) seria indistinguível da subtração que o cenário existe para
   provar.
2. **A escalada de A-08 é cross-tenant, e toda a regra rodava single-tenant.** `centros_custo` era
   a única das três tabelas sem nenhum cenário de isolamento — apesar de as três estarem na linha
   **S** do SFDIPOT. **CT-50** fecha: a administradora da Globex abrindo o centro da Acme pelo
   identificador e se nomeando gestora é exatamente *"quem edita `gestor_id` aprova as próprias
   compras"*, agora atravessando organizações. E **CT-45 passou a afirmar a organização** do centro
   criado e a origem da gestora escolhida.
3. **CT-46 tinha a ação sob teste escondida no `Dado`.** A troca de gestor é o comportamento de
   R12-M4 e estava numa precondição, sem oráculo; o `Quando` era o envio, e o `Então` só falava da
   notificação. Foram separados: **CT-46** afirma a troca gravada e **CT-55** afirma a consequência
   dela.
4. **E a 2ª rodada mostrou que CT-55 ainda não matava R12-M4.** A solicitação era **enviada depois
   da troca** — e uma implementação que **congela o gestor na solicitação no momento do envio**
   grava a Carla e passa nas duas linhas. A ordem entre o evento administrativo (a troca) e o
   evento de negócio (o envio) **é uma dimensão**, e estava fixa no valor conveniente. CT-55 foi
   invertido: a solicitação é enviada **antes** da troca. Isso levantou uma ambiguidade nova do
   requisito — **A-18**, registrada em
   [Perguntas para o `00-requisito.md`](#perguntas-para-o-00-requisitomd) — porque congelar o
   aprovador no envio é uma leitura defensável que o card não exclui.
4. **CT-47 não afirmava identidade.** "Continua se chamando Infraestrutura, com a mesma gestora"
   fica verde se o salvamento **duplicar** o registro. Agora afirma o mesmo identificador e a
   contagem.

CT-47 fecha o item de taxonomia *"editar sem alterar nada"*: uma validação de unicidade ingênua
acusa o registro colidindo com ele próprio, e é o defeito que só aparece na edição.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o cadastro de centro de custo entra na matriz do usuário comum (a subtração é esquecida) | CT-44 |
| M2 | a listagem é bloqueada mas a gravação não (barreira só na tela de lista) | **CT-52** — o matador declarado antes era uma linha de CT-44 cujo `Então` era vácuo |
| M3 | o gestor não é gravado na criação (o campo existe no formulário e não persiste) | CT-45 |
| M4 | quem decide a etapa é resolvido por um vínculo congelado no envio anterior, e a troca de gestor não tem efeito sobre a autoridade | **CT-55**. *(CT-46 era o matador declarado e afirmava só a notificação — o congelamento na autorização sobrevivia. Achado da revisão adversarial.)* |
| M5 | a validação de unicidade do nome não ignora o próprio registro e a edição sem alteração falha | CT-47 |
| M6 | `CentroCusto` sem escopo de organização: o cadastro de uma organização é alcançável por outra pelo identificador | **CT-50** — trazido pela revisão adversarial |
| M7 | o campo de gestor oferece (ou aceita) usuários de outra organização | **CT-61**. *(CT-45 era o matador declarado e é **tautológico** para isso: escolher alguém da Acme e afirmar que a gestora é da Acme não falsifica nada. Achado da 2ª rodada.)* |
| M8 | o salvamento sem alteração **duplica** o registro em vez de atualizá-lo | CT-47, pela contagem e pelo identificador |

---

## Gate de tela de escrita

Para **toda** rota `create`/`edit` da tabela `## Superfície de UI` do PRD, existe um cenário de
**gravação por componente** — não basta a tela abrir.

| Rota | Cenário de gravação | Cenário de leitura |
|---|---|---|
| `/app/solicitacoes-de-compra/create` | **CT-01** (`fillForm` → `create` → registro com os três campos) | CT-35, CT-51 |
| `/app/solicitacoes-de-compra/{record}/edit` | **CT-05** (`fillForm` → `save` → os três campos gravados) e **CT-53** (a rejeitada volta a ser editável) | CT-07, CT-08 |
| `/app/solicitacoes-de-compra/{record}` (view) | — (tela de leitura) | CT-36, CT-37, CT-38, CT-39, CT-48 |
| `/app/centros-de-custo/create` | **CT-45** | CT-44 |
| `/app/centros-de-custo/{record}/edit` | **CT-46** (troca gravada) e **CT-47** (salvar sem alterar) | CT-44, CT-50, CT-52 |

---

## Checklist de Taxonomia

Resposta válida: um ID de cenário, `não se aplica: {motivo}` ou
`lacuna declarada: {o que foi tentado}`. Nunca "sim".

| Item | Cenário que mata |
|---|---|
| **IDOR / autorização horizontal** | CT-09 (solicitação de outra organização), **CT-50** (centro de custo de outra organização), CT-08 (outra pessoa, mesma organização), CT-23 (papel resolvido no contexto errado) |
| **Autorização exercida na ação**, não só declarada | CT-20 (operação chamada fora da tela), CT-18, CT-19, **CT-52** (gravação, não só a tela) |
| **Autorização em cada verbo irmão** | CT-18 **e CT-19**, linhas `rejeitar`; CT-20, linhas `rejeitar`; CT-07 e CT-08, linhas `excluir` |
| **Registro vizinho** (a afirmação "daquele registro" é falsificável?) | **CT-48** (histórico), **CT-51** (listagem), **CT-49** e **CT-60** (roteamento por centro, com a solicitação no centro **não-primeiro**), **CT-59** (payload do aviso), CT-18 linha `gestor de outro` |
| **Ordem de grandeza / tipo da comparação** | **CT-56** (R$ 900 e R$ 12.000 contra um limite de R$ 5.000) |
| **Ordem entre evento administrativo e evento de negócio** | **CT-55** (troca de gestor depois do envio) |
| **Efeito colateral no segundo giro do ciclo** | **CT-58** (o reenvio avisa de novo) |
| **Idempotência** (ancorada no agregado persistido) | CT-30 |
| **Concorrência** | CT-31 |
| **Fronteira no ponto de entrada** (gravação, não só uso) | CT-04 (criação), CT-05 + CT-27 (edição) |
| **Criação ≠ edição ≠ uso** | criação CT-01/CT-03/CT-04/CT-45 · edição CT-05/CT-46/CT-47/CT-53 · uso CT-14/CT-27 |
| **Domínio condicionado** (o valor válido depende de outro campo) | não se aplica: nenhum campo desta feature muda o domínio de outro. O `valor` decide o **fluxo**, não o domínio de outro campo — e isso está coberto por CT-14 |
| **Estado × operação de escrita** (o terminal ainda funciona?) | CT-29 (aprovada), CT-33 (cancelada), CT-07, CT-12 |
| **Ausente ≠ `null` ≠ `""`** | CT-25 (justificativa: vazia, só espaços, ausente), CT-11 (gestor nulo) |
| **Paginação / ordenação** | ordenação: CT-38 (empate de `created_at`). Paginação: não se aplica: nenhuma cláusula do requisito fala de listagem paginada, e o volume é de unidades por solicitação |
| **Timezone / DST** | não se aplica: o requisito não tem cláusula temporal — nenhum prazo, expiração ou janela. A única data exibida (a de cada etapa) é lida no mesmo fuso em que foi escrita |
| **Unicode / limite de varchar** | lacuna declarada: o requisito não determina limite nem normalização para `descricao` e `justificativa`. Tentado enquadrar em CT-24 usando justificativa com acento (`"Sem verba neste trimestre"` já a traz) — o que não é o mesmo que um cenário de borda de `varchar`. Depende de P-01/P-02 serem respondidas |
| **Unicidade + soft delete** | não se aplica: nenhuma das três tabelas usa `SoftDeletes`, e o requisito não pede lixeira |
| **CRUD combinado** (editar sem alterar; excluir duas vezes) | CT-47 (salvar sem alterar), CT-29 e CT-33 (operar duas vezes sobre o terminal) |
| **Mass assignment** | CT-02 (`situacao` e `solicitante_id` no payload) |
| **Upload** | não se aplica: anexo está em Fora de Escopo declarado no `00` |
| **CRUD: duplicação no salvamento** | CT-47 (contagem + identificador inalterado) |
| **Precisão monetária** | **CT-01** (7.200,55 **pelo formulário**, que é o único caminho que passa pela máscara de entrada) e CT-04 (linha `0.01`, valor persistido); CT-14 (fronteira com incremento de centavo); **CT-56** (comparação numérica, não lexicográfica). Nenhum exemplo usa `float` |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | criação pelo formulário | R1 | EP | Feature (Livewire) | `tests/Feature/Compras/SolicitacaoCompraFormTest.php` | R1-M1, M5 |
| CT-02 | mass assignment ignorado | R1 | taxonomia | Feature (Livewire) | idem | R1-M2, M3 |
| CT-03 | campos obrigatórios | R1 | EP | Feature (Livewire) | idem | R1-M4 |
| CT-04 | valor estritamente positivo `@premissa` | R1 | BVA | Feature (Livewire) | idem | R1-M6, M5 |
| CT-05 | edita o valor em rascunho | R2 | estado × operação (célula válida) | Feature (Livewire) | `tests/Feature/Compras/EdicaoDaSolicitacaoTest.php` | R2 (célula válida) |
| CT-06 | exclui em rascunho | R2 | estado × operação (célula válida) | Feature (Livewire) | idem | R2 (célula válida) |
| CT-07 | não edita nem exclui fora do rascunho | R2 | estado × operação | Feature | idem | R2-M1, M3, M4, M5 |
| CT-08 | não mexe em rascunho alheio | R2 | persona | Feature | idem | R2-M2, M3 |
| CT-09 | isolamento entre organizações | R2 | IDOR | **FeatureTenancy** | `tests/FeatureTenancy/Compras/IsolamentoTest.php` | R2-M6 |
| CT-10 | envio vai para o gestor | R3 | estado × evento | Feature (Livewire) | `tests/Feature/Compras/EnvioTest.php` | R3-M1 |
| CT-11 | centro sem gestor `@premissa` | R3 | EP (nulo) | Feature (model) | idem | R3-M2, M3, M4 |
| CT-12 | só o rascunho se envia | R3 | estado × evento | Feature | idem | R3-M6 |
| CT-13 | só o solicitante envia | R3 | persona | Feature (model) | idem | R3-M5 |
| CT-14 | limite estritamente maior | R4 | BVA 3-valores | Feature | `tests/Feature/Compras/AlcadaTest.php` | R4-M1, M2, M3, M6 |
| CT-15 | limite literal do requisito, bilateral | R4 | valor do requisito | Feature | idem | R4-M4 |
| CT-16 | diretor não decide antes | R4 | ordem de eventos | Feature | idem | R4-M5 |
| CT-17 | a segunda mão conclui, e as etapas na ordem | R4 | ordem de eventos | Feature | idem | R4-M5 (parcial) |
| CT-18 | matriz da etapa do gestor | R5 | papel × ação × verbo | Feature (Livewire) | `tests/Feature/Compras/DecisaoTest.php` | R5-M1, M2, M3, M9 |
| CT-19 | matriz da etapa do diretor | R5 | papel × ação × verbo | Feature (Livewire) | idem | R5-M1, M4, M8, M9 |
| CT-20 | barreira fora da tela | R5 | taxonomia | Feature (model) | idem | R5-M5, M1 |
| CT-21 | affordance ausente para quem não decide | R5 | papel × ação | Feature (Livewire) | idem | R5-M6 |
| CT-22 | gestor aprova a própria `@premissa` | R5 | premissa A-09 | Feature | idem | — (cenário-testemunha de A-09) |
| CT-23 | diretor de outra organização | R5 | IDOR | **FeatureTenancy** | `tests/FeatureTenancy/Compras/IsolamentoTest.php` | R5-M7 |
| CT-24 | rejeição com motivo | R6 | EP | Feature (Livewire) | `tests/Feature/Compras/RejeicaoTest.php` | R6-M3 |
| CT-25 | rejeição sem motivo | R6 | EP de texto | Feature (Livewire + model) | idem | R6-M1, M2, M8 |
| CT-26 | 2-switch: recomeça pelo gestor `@premissa` | R6 | 2-switch | Feature | idem | R6-M4, M5 |
| CT-27 | reenvio com valor corrigido `@premissa` | R6 | 2-switch + campo | Feature | idem | R6-M6 |
| CT-28 | diretor também rejeita `@premissa` | R6 | persona | Feature (Livewire) | idem | R6-M7 |
| CT-29 | aprovada é terminal | R7 | estado × operação | Feature | `tests/Feature/Compras/TerminalTest.php` | R7-M1, M2, M5 |
| CT-30 | duplo clique | R7 | idempotência | Feature | idem | R7-M2 |
| CT-31 | duas decisões simultâneas | R7 | concorrência | Feature | idem | R7-M3, M4 |
| CT-32 | cancela em trânsito | R8 | estado × operação | Feature (Livewire) | `tests/Feature/Compras/CancelamentoTest.php` | R8-M2, M3 |
| CT-33 | não cancela fora do trânsito `@premissa` | R8 | estado × operação | Feature (model) | idem | R8-M1, M5 |
| CT-34 | só o solicitante cancela | R8 | persona | Feature (Livewire) | idem | R8-M4 |
| CT-35 | as cinco situações na listagem | R9 | EP exaustiva | Feature (Livewire) | `tests/Feature/Compras/TelaDaSolicitacaoTest.php` | R9-M1, M2, M4 |
| CT-36 | situação na tela de detalhe | R9 | EP | Feature (Livewire) | idem | R9-M3, M2 |
| CT-37 | cada etapa e o seu decisor, pareados | R10 | EP + oráculo pareado | Feature (Livewire) | idem | R10-M1, M2, M3, M6 |
| CT-38 | ordem com empate | R10 | ordenação | Feature (Livewire) | idem | R10-M4 (parcial) |
| CT-39 | motivo sobrevive ao reenvio `@premissa` | R10 | 2-switch | Feature (Livewire) | idem | R10-M5 |
| CT-40 | e-mail ao gestor | R11 | rastreio de efeito | Feature | `tests/Feature/Compras/NotificacaoTest.php` | R11-M1, M2 |
| CT-41 | só os da vez, uma vez | R11 | rastreio de efeito | **FeatureTenancy** | `tests/FeatureTenancy/Compras/NotificacaoTest.php` | R11-M3, M6 (parcial) |
| CT-42 | sem próxima etapa, sem aviso | R11 | rastreio de efeito | Feature | `tests/Feature/Compras/NotificacaoTest.php` | R11-M4 |
| CT-43 | aviso não escapa da falha | R11 | atomicidade | Feature | idem | R11-M5 |
| CT-44 | usuário comum fora do cadastro `@premissa` | R12 | papel × ação | Feature (Livewire) | `tests/Feature/Compras/CentroCustoTest.php` | R12-M1 |
| CT-45 | administração cadastra e define gestor | R12 | CRUD | **FeatureTenancy** (Livewire) | `tests/FeatureTenancy/Compras/CentroCustoTest.php` | R12-M3, M7 |
| CT-46 | a troca de gestor é gravada | R12 | CRUD | **FeatureTenancy** (Livewire) | idem | R12-M3 |
| CT-47 | salvar sem alterar | R12 | CRUD | **FeatureTenancy** (Livewire) | idem | R12-M5, M8 |
| **CT-48** | histórico só daquela solicitação | R10 | registro vizinho | Feature (Livewire) | `tests/Feature/Compras/TelaDaSolicitacaoTest.php` | R10-M7 |
| **CT-49** | o aviso vai para a gestora daquele centro | R3 | rastreio de efeito, mundo fechado | Feature | `tests/Feature/Compras/EnvioTest.php` | R3-M7 |
| **CT-50** | centro de custo de outra organização | R12 | IDOR | **FeatureTenancy** | `tests/FeatureTenancy/Compras/IsolamentoTest.php` | R12-M6 |
| **CT-51** | rótulo por linha, com registro vizinho | R9 | registro vizinho | Feature (Livewire) | `tests/Feature/Compras/TelaDaSolicitacaoTest.php` | R9-M4 |
| **CT-52** | usuário comum não grava a troca de gestor | R12 | papel × ação (no submit) | Feature (Livewire) | `tests/Feature/Compras/CentroCustoTest.php` | R12-M2 |
| **CT-53** | a rejeitada volta a ser editável nos três campos | R6 | 2-switch + campo | Feature (Livewire) | `tests/Feature/Compras/RejeicaoTest.php` | R6-M9 |
| **CT-54** | a ação some de quem já decidiu | R5 | papel × ação | Feature (Livewire) | `tests/Feature/Compras/DecisaoTest.php` | R5-M11 |
| **CT-55** | a troca alcança a solicitação já enviada `@premissa` | R12 | efeito + ordem temporal | **FeatureTenancy** | `tests/FeatureTenancy/Compras/CentroCustoTest.php` | R12-M4 |
| **CT-56** | a alçada compara números, não texto | R4 | EP por ordem de grandeza | Feature | `tests/Feature/Compras/AlcadaTest.php` | R4-M7 |
| **CT-57** | *(reservado — ver nota de numeração)* | — | — | — | — | — |
| **CT-58** | o reenvio avisa a gestora de novo | R11 | 2-switch aplicado ao efeito | Feature | `tests/Feature/Compras/NotificacaoTest.php` | R11-M7 |
| **CT-59** | cada gestora é avisada da solicitação dela | R11 | registro vizinho no payload | Feature | idem | R11-M8 |
| **CT-60** | quem decide é a gestora daquele centro | R3 | registro vizinho (não-primeiro) | Feature | `tests/Feature/Compras/EnvioTest.php` | R3-M7 |
| **CT-61** | gestor tem de ser da própria organização | R12 | isolamento no campo | **FeatureTenancy** | `tests/FeatureTenancy/Compras/CentroCustoTest.php` | R12-M7 |
| **CT-62** | o usuário comum opera a própria feature | R12 | contraste do 403 | Feature | `tests/Feature/Compras/CentroCustoTest.php` | discrimina a causa do 403 de CT-44 |

> **Nota de numeração**: **CT-57 não existe**. O identificador foi consumido e descartado durante o
> fechamento da 2ª rodada, quando o cenário "envio antes da troca" foi absorvido pela reescrita de
> CT-55 em vez de virar caso novo. Reaproveitar o número deslocaria a rastreabilidade já citada nas
> tabelas de mutantes; deixá-lo vago custa uma linha e não custa mais nada.
| **CT-B01** | rejeição pela modal real | R6 | JS executado | **Browser** | `tests/Browser/Compras/RejeicaoTest.php` | ver `05` |
| **CT-B02** | erro visível na modal | R6 | JS executado | **Browser** | idem | ver `05` |

**Cenários `@premissa`** (mudam se a resposta vier diferente): CT-04 (A-13), CT-11 (A-10), CT-22
(A-09), CT-26 e CT-39 (A-15), CT-27 (A-16), CT-28 (A-07), CT-33 linha `rascunho` (A-06), CT-44 e
CT-52 (A-08), **CT-55 (A-18)**.

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| CT de log: channel `compras`, nível e formato `[Classe@Método]` | o requisito não pede log. Seria derivado só do PRD — ver [Fronteira com o Plano](#fronteira-com-o-plano) |
| filtro por situação na listagem | o filtro é decisão do PRD; RQ-12 pede **mostrar** a situação, e isso é CT-35 |
| coluna de valor formatada em R$ na listagem | formatação de exibição que o requisito não determina; nenhum mutante plausível de negócio morre com ela |
| badge de situação com a **cor** certa | `assertSee` não valida cor, e provar cor exige screenshot. Lacuna declarada: a cor não é cláusula do requisito |
| solicitação sem centro de custo (centro excluído depois do envio) | o requisito não descreve exclusão de centro de custo; inventaria política de negócio |
| e-mail de rejeição ao solicitante | Fora de Escopo declarado no `00` (A-11) |
| teste de que a solicitação aprovada aparece em relatório | Fora de Escopo declarado no `00` |
| N níveis de aprovação / segunda faixa de alçada | Fora de Escopo declarado no `00` |
| CT de regressão sobre a contagem da matriz de permissões em `tests/Kit/PaineisTest.php` | não é derivado de cláusula nenhuma do requisito: é manutenção da suíte do kit diante de dois Resources novos. **Continua sendo obrigatório rodar** (`composer test:kit`, ver [Comandos](#comandos)) — mas é ajuste de suíte existente, não caso de teste desta feature. O comportamento que **importa** para o requisito é a subtração em si, e essa é CT-44 |

---

## Comandos

`.ai/rules/testes-browser.md` **vence a sugestão da skill** (`pest --parallel --tia`): sem PCOV
neste ambiente o `--tia` é inviável (medido: abortado após 35 min com Xdebug), e `--parallel`
derruba os CT-B. São dois comandos, nunca um:

```bash
vendor/bin/pest --parallel --compact             # backend: Feature + FeatureTenancy
vendor/bin/pest --testsuite=Browser              # CT-B, em série (composer test:browser embute o npm run build)
composer test:kit                                # a fundação não se moveu (tests/Pest.php e phpunit.xml foram tocados)
```

**Mutation testing, depois de implementar** — e com uma ressalva de dependência:

```bash
XDEBUG_MODE=coverage vendor/bin/pest tests/Feature/Compras --mutate --path=app/Models
```

O `pestphp/pest-plugin-mutate` está em `vendor/` como **dependência transitiva do Pest 5**, e
**não** está declarado no `composer.json` deste projeto. O comando funciona hoje por acidente da
árvore de dependências e some num `composer update`. Se o mutation testing for parte do ciclo,
`composer require pestphp/pest-plugin-mutate --dev` precisa entrar como passo do PRD.

> **E o score não responde pela omissão.** Mutation testing só muta código que existe: se uma
> cláusula do requisito nunca virou código, nenhum mutante é gerado e o score não cai. Quem
> responde por omissão aqui é a rastreabilidade `RQ` → regra → cenário e o gate de mutantes de
> **especificação** deste arquivo.

---

## Armadilhas de API que Invalidariam Estes CT

Confirmadas **no vendor deste projeto**, não de memória:
`grep -n "deprecated" vendor/filament/tables/.stubs.php`.

Em Filament 5 os helpers antigos **continuam existindo** e marcados `@deprecated` nos `.stubs.php`.
Eles funcionam, não avisam nada, e o CT escrito com eles passa hoje e quebra no upgrade.

| Escrever | Em vez de (`@deprecated` no vendor) | Onde importa aqui |
|---|---|---|
| `callAction(TestAction::make('aprovar')->table($s), [...])` | `callTableAction` (`.stubs.php:189`) | CT-18, CT-19, CT-24, CT-32 |
| `assertActionDoesNotExist(TestAction::make('aprovar')->table($s))` | `assertTableActionDoesNotExist` (`:204`) | **CT-21** |
| `assertActionHidden(...)` | `assertTableActionHidden` (`:219`) | CT-21 |
| `assertSchemaStateSet([...])` | `assertFormSet` / `assertTableActionDataSet` (`:96`, `:184`) | CT-47 |
| `assertHasFormErrors([...])` | `assertHasTableActionErrors` (`:164`) | CT-03, CT-04, CT-25 |
| `fillForm([...])` | `setTableActionData` (`:91`, `:179`) | CT-01, CT-05, CT-45 |

O molde vivo do projeto já usa a API nova — `tests/Kit/ConviteTest.php:262` e
`tests/Tenancy/AdminDaOrganizacaoTest.php:498` usam `TestAction` e `assertActionDoesNotExist`.

E as que invalidariam por outro caminho:

| Armadilha | Consequência aqui |
|---|---|
| `Mail::assertSent` na notificação | **nunca passa** — ela é `ShouldQueue`. CT-40..CT-43 usam `Notification` |
| `Event::fake()` antes das fixtures | os `creating` de uuid e `tenant_id` não rodam e a fixture nasce quebrada. **Nenhum cenário usa** |
| `assertDatabaseHas` só com a chave primária | passa com todos os outros campos errados. Todo `Então` deste conjunto nomeia os campos |
| `RefreshDatabase` + `travel()` sem `travelBack()` | CT-38 usa `freezeTime()` **dentro de closure**, para não vazar para o cenário seguinte |
| helper de teste declarado num `*Test.php` e usado por dois arquivos | `Call to undefined function` em `--parallel`, `--tia` ou arquivo isolado. Todos os helpers vão para `tests/Pest.php` |

---

## Revisão Adversarial

Executada por **sub-agente independente**, que recebeu apenas o `00-requisito.md`, o `04` e o `05`
— **sem o PRD, sem o código e sem o raciocínio de quem derivou** —, com a tarefa de *provar que
este conjunto deixa passar um defeito* e a proibição explícita de elogiar, reescrever ou dizer
"está bom".

**Resultado: 6 implementações erradas que passavam no conjunto inteiro, 17 oráculos fracos, 6
cenários com mais de um `Quando`, 10 cláusulas `RQ` com cobertura aparente e 6 mutantes declarados
mortos que não morriam.** O conjunto anterior tinha 47 cenários e afirmava 3 lacunas; a revisão
mostrou que eram **9**.

> Este é o valor da regra de não autorrevisar. Os seis defeitos abaixo passariam por 47 cenários
> escritos com técnica formal, gate de mutantes e checklist de taxonomia preenchido — e o
> checklist teria lido ✅ em todos eles.

### O padrão por trás de quase tudo: **o conjunto não tinha vizinhos**

Quatro dos seis defeitos têm a mesma raiz, e vale nomeá-la porque ela não aparece em nenhuma
técnica formal: **cada cenário criava exatamente um registro de cada coisa** — uma solicitação, um
centro de custo, uma organização com centro. Toda afirmação do tipo *"a linha **daquela**
solicitação"*, *"as etapas **dela**"*, *"o gestor **do** centro"* fica **inmatável por construção**
quando não existe outro registro para o sistema confundir. O oráculo parece específico e não é.

### Rodada 1 — os seis defeitos que passavam

| # | Implementação errada que passava no conjunto todo | Regra | Técnica que faltou | O que virou |
|---|---|---|---|---|
| **DI-1** | O formulário **trunca os centavos** do valor (máscara de moeda que devolve inteiro). Todo valor digitado por formulário no conjunto era redondo — `7.200,00`, `4.850,00`, `5.000,00` — e os valores com centavo de CT-14 entram por *fixture*, não pelo formulário. A linha `0.01` de CT-04, declarada "matador forte", afirmava só "aceito" | R1, R4 | BVA de **escala decimal** no ponto de entrada, com assertion sobre o persistido | CT-01 passou a `7.200,55`; CT-04 passou a afirmar o valor persistido; R1-M5 reescrito |
| **DI-2** | A tela lista as etapas **sem filtrar pela solicitação** (relação sem escopo). Nenhum cenário tinha duas solicitações em banco; as contagens `assertDatabaseCount` eram globais | R9, R10 | registro vizinho / dado de ruído | **CT-48** e **CT-51** criados; todas as contagens passaram a dizer "daquela solicitação" |
| **DI-3** | O destinatário do aviso não é amarrado ao centro (`todos os gestores da organização`). Todo cenário de notificação tinha **um centro só**; CT-18 tinha dois, mas só afirmava decisão recusada, nunca roteamento | R3, R11 | rastreio de efeito com **par discriminante** de centros | **CT-49** criado; R3-M7 criado |
| **DI-4** | Na etapa do diretor, `rejeitar` **não confere a identidade**. CT-19 tinha 7 linhas e só duas no verbo `rejeitar`: uma guarda do tipo *"quem ainda não decidiu"* liberava solicitante e estranho | R5 | fechamento da matriz com o **verbo** como dimensão — aplicada em CT-18 e abandonada em CT-19 | 3 linhas acrescentadas a CT-19; R5-M8 criado |
| **DI-5** | `CentroCusto` **sem escopo de organização**: a administradora da Globex abre o centro da Acme e se nomeia gestora. Toda a R12 rodava single-tenant, e `centros_custo` era a única das três tabelas sem cenário de isolamento | R12 | matriz de isolamento aplicada a **todas** as tabelas do SFDIPOT | **CT-50** criado; CT-45 passou a afirmar a organização; R12-M6 e M7 criados |
| **DI-6** | O histórico renderiza decisores e decisões em **listas paralelas** desalinhadas. CT-37 afirmava tokens soltos, o que passa com o pareamento invertido — literalmente o mutante R10-M3, declarado morto | R10 | oráculo **pareado** em vez de conjunção de substrings | `Então` de CT-37 reescrito em blocos; R10-M6 criado |

### Rodada 1 — oráculos fracos e cenários mal formados

Todos fechados. Os de maior impacto:

| Cenário | O que estava errado | Correção |
|---|---|---|
| **CT-18, CT-19** | `Então` **condicional** ("quando recusado, …") deixava as linhas `aceito` **sem oráculo nenhum** — uma decisão que retorna sucesso e não faz nada passava | `Então` incondicional: toda linha declara situação final e contagem de etapas |
| **CT-15** | o `Dado` **afirmava** o limite em vez de exercitá-lo, e a única linha (`5.000,01 → diretor`) passava com **qualquer** default abaixo disso | virou `Esquema` bilateral (`4999.99` e `5000.01`) sem tocar em config |
| **CT-27** | **três ações num `Quando`** e nenhuma afirmação de que a correção foi gravada — RQ-09 ficava com cobertura aparente | dividido em **CT-53** (a correção grava) e CT-27 (o reenvio reavalia a alçada) |
| **CT-46** | a ação sob teste (a troca de gestor) estava escondida no `Dado`, e o `Então` só falava da notificação | CT-46 afirma a troca gravada; **CT-55** afirma a consequência sobre quem decide |
| **CT-44** | não-efeito **vácuo** em linhas onde nada era alterado; e o 403 não distinguia "recurso subtraído" de "painel inacessível" | não-efeito foi para **CT-52**; CT-44 ganhou o contraste "abre outra tela do painel" |
| **CT-17** | dois `Quando` e **estado intermediário nunca afirmado** — o que separa a implementação correta da permissiva quanto à ordem | primeira aprovação foi para o `Dado`; etapas afirmadas com tipo e ordem |
| **CT-42** | `Dado` com situação inicial **indefinida** para rejeição e cancelamento — cenário não reproduzível | `Exemplos` com valor, situação inicial, ator, ação e situação final |
| **CT-21** | dois atores no mesmo cenário, e "não está disponível" não distinguia ausente de desabilitado | dividido em CT-21 (ausente) e **CT-54** (existe e habilitada) |
| **CT-05** | editava **só o `valor`**: RQ-02 ficava provado para 1 de 3 campos | passou a editar e afirmar os três |
| **CT-30, CT-33, CT-12, CT-47, CT-36, CT-04** | não-efeito incompleto, ancoragem ausente ou termo não observável | oráculos reforçados, um a um |
| **CT-B01, CT-B02** | `assertSee` de texto que pode vir de filtro/legenda; passo 5 repetia o texto do passo 2 e era string de i18n | CT-B01 ganhou `assertDontSee` da situação antiga; CT-B02 passou a oráculo **estrutural** (`assertPresent`, confirmado no vendor) |

### Rodada 2 — 5 defeitos novos, e três cenários da rodada 1 que não matavam o que diziam matar

Disparada porque o fechamento da rodada 1 criou **cenário novo** (CT-48 a CT-55), que é a condição
que a skill exige. Mesmo contrato, sub-agente novo, sem o PRD e sem este raciocínio.

**O achado mais importante da rodada 2 não é um defeito da feature — é um defeito do gate**: três
dos oito cenários criados para matar mutantes da rodada 1 **não os matavam**. Corrigir um conjunto
não é o mesmo que corrigi-lo bem, e nada além de outra revisão independente teria mostrado isso.

| # | Implementação errada que passava | Regra | Técnica que faltou | O que virou |
|---|---|---|---|---|
| **E-1** | **A alçada compara texto, não número.** `decimal` volta do SQLite como *string* — o próprio SFDIPOT deste arquivo avisa. Em comparação lexicográfica, `'12000.00' > '5000.00'` é **falso**: uma compra de R$ 12.000 é aprovada só pelo gestor. Todos os valores do conjunto tinham 4 dígitos inteiros ou menos, então a BVA impecável era **cega ao tipo** | R4 | EP com **ordem de grandeza** como dimensão | **CT-56**; R4-M7 |
| **E-2** | **"O gestor do primeiro centro".** CT-49 tinha dois centros, mas a solicitação estava no centro **criado primeiro** — `CentroCusto::first()` devolve a gestora certa e o cenário fica verde | R3 | registro vizinho só vale se o registro sob teste **não for o primeiro** | CT-49 invertido; **CT-60** separou a autoridade do efeito |
| **E-3** | **O gestor é congelado na solicitação no envio.** CT-55 enviava **depois** da troca, então o snapshot gravava a gestora nova e as duas linhas passavam. O mutante R12-M4 estava declarado morto pela segunda vez | R12 | **ordem entre o evento administrativo e o de negócio** como dimensão | CT-55 invertido; **A-18** registrada como ambiguidade nova |
| **E-4** | **Guard de idempotência mata o segundo aviso.** `if ($this->notificado_em === null)` passa em CT-40..CT-43 e faz a solicitação corrigida e reenviada **nunca mais avisar ninguém** — RQ-14 quebrando dentro do ciclo de RQ-08/RQ-09. Todo o 2-switch do conjunto afirmava estado, nunca efeito | R11 | **2-switch aplicado ao efeito** | **CT-58**; R11-M7 |
| **E-5** | **O aviso é montado da solicitação errada**, e a negação de destinatários era por enumeração. CT-40 dizia "referente a **essa** solicitação" com **um registro em banco** — a mesma não-falsificabilidade que justificou CT-48 e CT-51 | R11 | registro vizinho no **payload** + oráculo de **mundo fechado** | **CT-59**; CT-41 passou a contar o total; R11-M8, M9 |
| **E-6** | O formulário de edição libera só `valor` depois de uma rejeição (`disabled` quando há etapas). CT-53 afirmava **um** campo; CT-05 (três campos) rodava em rascunho virgem | R6 | campo como dimensão **dentro** do 2-switch | CT-53 passou a editar e afirmar os três |
| **E-7** | O histórico é ordenado **pelo nome do decisor** ou **pela decisão** — em todos os cenários a ordem cronológica coincidia com a alfabética (Beatriz → Rui) e com `aprovada → rejeitada` | R10 | valores discriminantes em **dimensões não-numéricas** | diretor rebatizado **Ana**; CT-38 com as duas etapas na mesma decisão; R10-M11, M12 |

**Mutantes cujo matador declarado não matava** (além dos acima): **R12-M7** — CT-45 era
tautológico (escolher uma gestora da Acme e afirmar que ela é da Acme não falsifica nada) → **CT-61**;
**R6-M7** — a metade *"não exige justificativa"* só era exercitada na etapa do gestor → a **etapa**
virou dimensão de CT-25; **R9-M4** — CT-51 só mata com assertion **por registro**, não com
`assertSee`, que passa com os rótulos trocados entre as linhas.

**Oráculos e formas corrigidos**: CT-44 tinha uma **ação dentro do `Então`** (e amarrava o cenário a
outro Resource) → o contraste virou **CT-62**; CT-46 não afirmava identidade nem contagem, e um
`save()` que duplica passava; CT-50 tinha duas ações num `Quando`; CT-22 não afirmava a ausência de
segunda etapa; CT-25 escrevia `ausente` sem aspas, o que materializado vira a string `"ausente"` —
uma justificativa **válida** — e deixaria o cenário vermelho sem defeito; CT-29 tinha uma coluna de
`Exemplos` que nenhum placeholder consumia; a cláusula final de CT-27 era decorativa (`aprovada` já
exclui `aguardando_diretor`) e foi cortada; CT-B01 gravava sem ancorar na solicitação nem contar.

**Poda**: **CT-54** era redundante — `callAction` sobre ação oculta já falha, então as linhas
válidas de CT-18 provavam a presença da ação. Em vez de cortá-lo, ele foi **reespecificado** para a
célula que ninguém exercitava: a ação some para o gestor **depois** que ele decidiu (R5-M11).

### Um falso achado, e por que ele está registrado

A rodada 2 apontou que **12 mutantes citados no índice não tinham linha nas tabelas**. Não é
verdade no arquivo: é artefato do meu preparo da entrada. Para não contaminar o revisor, filtrei do
arquivo enviado as linhas que mencionavam "revisão adversarial" — e **exatamente os 12 mutantes
trazidos pela rodada 1 tinham essa expressão na coluna do matador**. O arquivo tem 80 linhas de
mutante; a cópia enviada tinha 68.

Fica registrado porque é uma armadilha reutilizável: **higienizar a entrada do revisor para evitar
viés pode fabricar achados**. O filtro correto é por seção (remover o bloco da revisão anterior),
nunca por palavra.

### Teto de rodadas atingido — o que fica aberto

A skill fixa o teto em **2 rodadas** e manda **registrar e escalar** quando a segunda ainda traz
achado estrutural. Foi o caso: E-1 (comparação de texto) e E-4 (guard de idempotência) são
estruturais, e as três correções da rodada 1 que não mataram o que diziam matar indicam que o
padrão *"cada cenário cria um registro de cada coisa"* é sistêmico neste conjunto, não pontual.

**Não há rodada 3.** O que está escalado, para decisão de quem conduz a feature:

1. **R11 tem 7 cenários contra teto de 3** e cobre notificação em quatro direções mais tempo e
   payload. Pelo critério da skill, ela **deveria ser duas regras** ("o aviso alcança quem deve" e
   "o aviso não alcança quem não deve"). Não foi desdobrada aqui para não renumerar a
   rastreabilidade; é a candidata número um a desdobramento na próxima revisão do arquivo.
2. **A-18 é ambiguidade de requisito, não de teste**, e a resposta dela muda modelagem (uma coluna
   nova na solicitação). Bloqueia CT-55.
3. **As lacunas declaradas que permanecem**: R4-M5 (ordem permissiva), R10-M4 (ordenação por `id`)
   e R11-M6 (duplicação por retry de fila). As três têm o que foi tentado escrito, e nenhuma foi
   convertida em ✅.

---

## Checklist Final da Derivação

- [x] Perfil por área, com P×I e a justificativa de cada nota
- [x] SFDIPOT preenchida; nenhuma dimensão vazia, e a única dispensa (fuso) está no checklist com motivo
- [x] Toda `RQ-01`..`RQ-14` gerou ao menos uma regra
- [x] Perguntas novas registradas (P/A-13..A-17), em bloco pronto para colagem, com o desvio declarado
- [x] Técnica nomeada por regra; escalada de técnica declarada em R1 e R11
- [x] BVA com incremento `0,01` (`decimal(12,2)`)
- [x] Tabela estado × operação com **persona** e **campo** como dimensões; toda coluna com ao menos uma célula válida
- [x] Partições inválidas isoladas, uma por linha de `Exemplos`
- [x] Cenários de recusa afirmam o **não-efeito** (situação intacta, nenhuma etapa, nenhum e-mail)
- [x] Toda regra declara ≥3 mutantes (perfil completo) / ≥2 (padrão)
- [x] Todo mutante tem matador **ou** lacuna declarada com o que foi tentado (3 lacunas: R4-M5, R10-M4, R11-M6)
- [x] Cada cenário na camada mais barata **que o arnês deste projeto sustenta** (`tests/Unit` não está ligado a `TestCase`)
- [x] Tetos de cenário e de mutante estourados **com justificativa escrita**, nunca em silêncio
- [x] Gate de tela de escrita fechado para as quatro rotas `create`/`edit`
- [x] Revisão adversarial por sub-agente independente — **2 rodadas, teto atingido** — ver
      [Revisão Adversarial](#revisão-adversarial)
- [x] Achado estrutural remanescente **escalado**, não fechado à força (R11 candidata a virar duas
      regras; A-18 bloqueia CT-55)
- [ ] `pest --mutate` executado — **pós-implementação**
- [ ] Índice de cenários atualizado com o arquivo de teste real — **pós-implementação**
