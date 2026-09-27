---
name: feature-wiki
description: >
  Cria a wiki de uma feature Laravel antes de implementá-la. Invoque SEMPRE ao iniciar
  implementação de qualquer feature nova — card, ticket, requisito ou PRD —, antes de qualquer
  php artisan make:*, e de novo quando o pedido crescer no meio da implementação (vira Adendo
  no 00). Grava em wikis/specs/{branch}/{feature}/ o requisito bruto imutável decomposto em
  cláusulas RQ (00), o plano de ação (PRD) executável por outro agente (01), as decisões
  arquiteturais em ADR (02) e o progresso com evidência (03). Os casos de teste (04/05) são
  delegados à feature-test-design, que os deriva do requisito, não do plano. Conduz a feature até
  o PR: pesquisa com search-docs do Laravel Boost, revisão do plano, revisão do diff por quem não
  implementou assim que os testes passam, reconciliação wiki × código, quality gate
  (feature-quality-gate) e candidatos a Project Rule (requirement-to-rule).
  Para Laravel, Livewire, Filament e Pest; no Claude Code, despacha sub-agentes roteados por
  modelo e por cegueira.
license: MIT
compatibility: >-
  Projeto Laravel com git. Laravel Boost com MCP recomendado: search-docs no step 3 e
  record-rule (Boost >= 2.4.12) no step 9. Pest 4 ou 5; assume Pest 5 (--tia e --mutate na
  Verificação Final, --agent na implementação) e cai para --filter no Pest 4. Sub-agentes do Claude Code opcionais: sem eles tudo
  roda em linha e a perda de independência é declarada no 03. Plugins Ponytail e Caveman
  opcionais; sem Ponytail o step 6 vira passe manual registrado no 03.
metadata:
  version: "3.6.0"
  requires: "feature-test-design>=1.15.0; feature-quality-gate>=1.5.0; laravel/boost>=2.4.12"
---

# Feature Wiki — Documentação Antes de Implementar

> ## O gate que mais pega defeito é o step 6.5 — e ele roda assim que os testes passam
>
> Esta skill tem oito gates. Sete deles leem **o plano, o requisito ou a tela**. Um só lê **o
> diff**, e é o [step 6.5 — Revisão de Código do Diff](#65-revisão-de-código-do-diff-obrigatório-logo-após-os-testes-passarem-e-antes-da-reconciliação),
> com `/code-review` por quem não implementou.
>
> Por que ele está no topo — a medição de 2026-09-17: [`references/casos-medidos.md`](references/casos-medidos.md#topo--o-65-é-o-gate-mais-produtivo-2026-09-17).
>
> **Não trate o 6.5 como formalidade.** Se o orçamento apertar, corte cenário redundante, não este
> gate. E ele roda **antes** da reconciliação (step 7), não depois: cada achado confirmado muda
> código, cláusula e CT — reconciliar antes de revisar é reconciliar duas vezes.
>
> **Quem revisa não pode ser quem implementou.** No Claude Code isso é construção, não intenção:
> o `/code-review` já roda em sub-agente isolado, e o passe de eixos vai para um sub-agente que
> não recebe o PRD. Ver [Execução e Delegação](#execução-e-delegação-claude-code--roteamento-por-modelo-e-por-cegueira).

## Glossário

| Sigla | Significado |
|-------|-------------|
| **RQ** | Cláusula de requisito — unidade numerada da decomposição do `00-requisito.md` |
| **PRD** | Product Requirements Document — plano de ação detalhado |
| **ADR** | Architecture Decision Record — registro de decisão arquitetural |
| **CT** | Caso de Teste — especificação de um cenário de teste (backend) |
| **CT-B** | Caso de Teste de Browser — cenário E2E validado em navegador real |
| **DB** | Database — banco de dados |
| **FK** | Foreign Key — chave estrangeira |
| **TIA** | Test Impact Analysis — engine do Pest 5 que roda só os testes afetados |
| **`{base}`** | Branch de destino do PR (`main`, salvo indicação do usuário); registrada no cabeçalho do `03` |
| **`{skills}`** | Diretório onde as skills estão instaladas: `.ai/skills/` (Boost), `.claude/skills/` (espelho local) ou `~/.claude/skills/` (global); use o primeiro que existir |

## Índice

- [Quando Invocar](#quando-invocar) · [Execução e Delegação (Claude Code)](#execução-e-delegação-claude-code--roteamento-por-modelo-e-por-cegueira)
- **Fluxo**: [0. Requisito](#0-capturar-o-requisito--primeiro-ato) · [1. Branch](#1-descobrir-branch-e-estrutura-de-pasta) · [2. Nome](#2-definir-nome-da-feature) · [3. Pesquisa](#3-pesquisa-e-contexto-obrigatório-antes-de-escrever) ([Superfície Livewire](#superfície-livewire-obrigatório-em-toda-feature-que-cria-página-widget-ou-componente), [`search-docs`](#documentation-api-do-boost-search-docs)) · [4. Arquivos](#4-criar-os-arquivos) · [5. Revisão profunda](#5-revisão-profunda-pós-escrita-obrigatório) ([classe irmã](#varredura-da-classe-irmã-obrigatória-para-toda-classe-nova)) · [6. Ponytail](#6-auditoria-da-wiki-com-ponytail-review-obrigatório) · [6.5. Revisão do diff](#65-revisão-de-código-do-diff-obrigatório-logo-após-os-testes-passarem-e-antes-da-reconciliação) · [7. Reconciliação](#7-pós-implementação-e-reconciliação-obrigatório-antes-do-pr) · [8. Quality gate e PR](#8-quality-gate-e-abertura-do-pr-obrigatório-antes-do-pr) · [9. Rules](#9-candidatos-a-rule-de-projeto-decisão-do-usuário)
- **Arquivos**: [00](#arquivo-00-requisito--fonte-da-verdade) ([Adendo](#adendo-ao-requisito--quando-o-pedido-cresce-durante-a-implementação)) · [01](#arquivo-01-plano-de-ação-prd) · [Padrão de Log](#padrão-de-log--classemétodo-mensagem) · [02](#arquivo-02-decisões-arquiteturais-adr) · [03](#arquivo-03-progresso--tracking) · [04 e 05](#arquivos-04-e-05-casos-de-teste--delegados-à-feature-test-design) ([Playwright MCP](#playwright-mcp-na-validação-opcional--ferramenta-de-observação))
- [Pest 5](#execução-de-testes-com-pest-5) · [Citações de código](#citações-de-código--arquivosímbololinha) · [Checklist Final](#checklist-final-da-skill) · [Skills Companheiras](#skills-companheiras)

**`references/`** — só entram no contexto quando lidas. Cada step diz qual abrir, **antes** da ação;
o checklist final exige declarar quais foram abertas.

| Arquivo | Lida em | Fonte única de |
|---|---|---|
| [`template-00-requisito.md`](references/template-00-requisito.md) | step 4; Adendo | template do `00` e do Adendo |
| [`template-01-plano.md`](references/template-01-plano.md) | step 4 | template do `01` e skills citáveis no PRD |
| [`template-02-adr.md`](references/template-02-adr.md) | step 4 | template do `02` |
| [`template-03-progresso.md`](references/template-03-progresso.md) | step 4 | template do `03` |
| [`padrao-de-log.md`](references/padrao-de-log.md) | step 4 (logs do `01`) | anatomia, contexto estruturado, exemplos de log |
| [`pesquisa-step-3.md`](references/pesquisa-step-3.md) | step 3; pré-6.5 | greps da Superfície Livewire; cobertura e lacunas do `search-docs` |
| [`roteamento-e-despacho.md`](references/roteamento-e-despacho.md) | todo despacho | tabela de rotas, quadro de despacho, mapa por step |
| [`delegacao-casos-de-teste.md`](references/delegacao-casos-de-teste.md) | step 4; implementação; step 7 | contrato da delegação, do `executor-ct` e dos CT-B |
| [`playwright-mcp.md`](references/playwright-mcp.md) | step 3; loop do CT-B; step 7 | configuração, tools e fallback do Playwright MCP |
| [`pest-5.md`](references/pest-5.md) | step 3; implementação; step 7 | instalação, TIA, `--agent`, `.cmd` do Windows |
| [`citacoes-de-codigo.md`](references/citacoes-de-codigo.md) | steps 3, 5 e 7 | classes de erro, exemplos e comando de conferência |
| [`candidatos-a-rule.md`](references/candidatos-a-rule.md) | step 9 | fontes de candidatos e formato de apresentação |
| [`ponytail-caveman.md`](references/ponytail-caveman.md) | início da sessão | fronteira do Caveman, ativação do trio |
| [`estrutura-criada.md`](references/estrutura-criada.md) | step 4 | arquivos extras `05-*` e árvore de exemplo |
| [`casos-medidos.md`](references/casos-medidos.md) | quando um step aponta | os casos que originaram as regras do corpo |

Os fatos do `pest-plugin-browser` não têm cópia nesta skill, fora os dois que o step 3 confere: a fonte única é
`{skills}/feature-test-design/references/pest-plugin-browser.md`.

## Ordem de Leitura para o Agente Implementador

Ao implementar, o agente deve ler os arquivos nesta ordem:
1. **`00-requisito.md`** — entende o que foi **pedido** (fonte da verdade, não o plano)
2. **`01-plano-acao.md`** — entende o que fazer e em que ordem
3. **`04-casos-de-teste.md`** — entende como validar cada passo
4. **`05-casos-de-teste-browser.md`** — se existir: entende como validar a UI e o fluxo do usuário
5. **`02-decisoes-arquiteturais.md`** — entende as restrições e justificativas
6. **`03-progresso.md`** — marca o que já foi feito e retoma de onde parou

---

## Quando Invocar

- Sempre que o usuário pedir para implementar uma feature nova
- Ao iniciar qualquer card/ticket/task de desenvolvimento
- Antes de qualquer `php artisan make:*` ou criação de código
- Quando o usuário pedir para arquitetar ou analisar uma feature antes de implementá-la

### Quando NÃO Invocar

- **Typo fixes**: correções de texto, mensagens, labels
- **Mudanças triviais**: ajustes de config simples, tweak de CSS isolado, mudança de 1-2 linhas sem nova lógica
- **Refactoring puro**: renomear variáveis, extrair método, sem mudança de comportamento
- **Bump de dependência**: atualizar versão de package sem mudança de API
- **Adição de seeders/migrations isoladas**: sem lógica de negócio associada

> **Critério**: se a mudança não adiciona nova lógica de negócio, não altera fluxo de dados e não cria novos arquivos de código → não precisa de wiki.
> **Bug fix com nova lógica**: se o fix introduz nova regra de negócio, novo estado ou novo fluxo → invocar a wiki.

## Execução e Delegação (Claude Code) — roteamento por modelo e por cegueira

> Vale quando o host expõe sub-agentes (Claude Code: ferramenta `Agent`, agentes em
> `.claude/agents/`). Em host sem sub-agente (Windsurf, Cursor, Copilot) tudo roda em linha, e a
> degradação é **declarada** no `03-progresso.md` → `## Despachos`: *"Sem despacho — host sem
> sub-agente"*. O que se perde não é só custo: perde-se a **independência** dos gates, e o leitor
> do PR precisa saber disso.

A sessão principal **orquestra, decide e audita**. Tarefa de volume e tarefa de julgamento
independente **não rodam em linha** — vão para sub-agente pela ferramenta `Agent`, com o modelo
roteado. Delegar é o padrão; rodar em linha é exceção declarada.

Princípio: **gerar barato, raciocinar sob demanda, auditar caro — e julgar às cegas.**

A validação em campo deste modelo (2026-09-21, feature completa): [`references/casos-medidos.md`](references/casos-medidos.md#validado-em-campo--2026-09-21-feature-completa-no-demo-wiki).

### Dois eixos de roteamento, não um

| Eixo | Pergunta | Decide |
|---|---|---|
| **Complexidade** | quanto raciocínio a tarefa exige? | o **modelo** (`haiku` → `sonnet` → `opus`) |
| **Cegueira** | o que o executor **não pode ter visto** para o resultado valer como prova? | o **contexto** que o sub-agente recebe — e, por consequência, que a tarefa **não pode** rodar em linha |

O segundo eixo é o que esta esteira tem de específico. A coletânea inteira existe para quebrar a
**cegueira correlacionada**: o mesmo agente lê o requisito, escreve o plano, o teste, o código e o
veredito, e erra coerentemente. Sub-agente é o instrumento mais barato contra isso — ele nasce
**sem** o contexto da sessão, então *"por quem não implementou"* (step 6.5), *"por quem não
derivou"* (revisão adversarial da `feature-test-design`) e *"por quem não escreveu a wiki"*
(step 8) deixam de ser intenção e viram **construção**. Tarefa cuja validade depende de cegueira
**nunca** roda em linha, mesmo que caiba em dois passos.

### Rotas

Antes de montar o quadro de despacho, leia [`references/roteamento-e-despacho.md`](references/roteamento-e-despacho.md#rotas):
a tabela de rotas — modelo, uso nesta esteira e ferramentas de `mecânico`, `construtor`, `analista`,
`revisor-diff`, `adversário-ct`, `qa-gate`, `executor-ct`, `executor-ctb` e sessão principal.

**Tier é o conceito portável; o alias é a implementação Claude.** `haiku` = **econômico**,
`sonnet` = **intermediário**, `opus` = **topo**. Em outro provedor o projeto mapeia os três tiers
para os modelos que tiver (um "mini", um padrão, um de raciocínio) e o resto da esteira fica
intacto; a coluna *Modelo* de `## Despachos` registra sempre o modelo **efetivamente** usado.

**Regras da rota `mecânico`** (casos em [`references/casos-medidos.md`](references/casos-medidos.md#rota-mecânico--2026-09-21)):

- **Um item por despacho** — um grep em lote com a tabela pronta, uma conversão, um espelho. Lote
  misto (converter + mover + preencher tabela) vai para `construtor`
- **FQCN em grep vai com `grep -F`** — o escape das barras produziu um *"sem ocorrências"* falso
- **`Explore` (built-in) só para feature grande.** Para o resto, `mecânico` com **trechos**, não
  arquivos

Como obter as rotas, em ordem de preferência:

1. **Agentes do projeto** em `.claude/agents/` — se o projeto já tem `mecanico`/`construtor`/
   `analista` (ou equivalentes), usá-los pelo `subagent_type`
2. **Agentes da esteira** — cada skill é dona do seu, na pasta `agents/` dela, para o Boost
   instalá-lo junto com a skill: `feature-wiki/agents/fw-revisor-diff.md`, `fw-executor-ct.md` e `fw-executor-ctb.md`,
   `feature-test-design/agents/fw-adversario-ct.md`, `feature-quality-gate/agents/fw-qa-gate.md`.
   O Claude Code **não lê `.ai/skills/*/agents/`** — os arquivos precisam ser copiados uma vez para
   `.claude/agents/`, e de novo a cada atualização das skills:

   ```bash
   cp .ai/skills/*/agents/*.md .claude/agents/
   ```

   Sem a cópia, `subagent_type: "fw-…"` falha e a rota cai no item 3. São os cinco que carregam
   **cegueira e restrição de ferramenta**; as rotas genéricas não precisam de arquivo.
   **Os agentes só carregam de `.claude/agents/` do diretório onde a sessão foi aberta** — sessão
   aberta num diretório pai ou noutro repositório não os vê. Antes do primeiro despacho,
   `ls .claude/agents/fw-*.md`; se faltar, a rota cai no item 3 e a linha de `## Despachos`
   registra *"fallback `general-purpose`/{model} — agente `fw-…` indisponível"*. O fallback
   segurou uma feature inteira (2026-09-21): perde a **restrição de ferramenta**, não a cegueira,
   porque o contrato e o que o agente não recebe vão no prompt
3. **`general-purpose` com `model` explícito** — funciona em qualquer projeto sem instalar nada.
   **NUNCA despachar `general-purpose` sem `model`**: ele herda o modelo caro da sessão e o
   roteamento deixa de existir

O parâmetro `model` da chamada `Agent` sobrepõe o modelo do arquivo do agente quando a tarefa fugir
do padrão — e a sobreposição vai no quadro, com o motivo. Sub-agente que precisa seguir uma skill
companheira recebe o **path do `SKILL.md`** dela para ler e seguir; não se resume a skill no prompt.

### Paralelo é o padrão, sequência é exceção

Tarefas independentes disparam **juntas, no mesmo lote**. Sequência só quando a saída de uma é
entrada da outra — e aí o quadro declara qual dependência forçou a fila.

Duas restrições desta esteira ao paralelo:

- **Nunca dois construtores no mesmo arquivo.** Passos do PRD que tocam o mesmo arquivo rodam em
  sequência; paralelo só com conjuntos de arquivos **disjuntos**, declarados no quadro
- **Cegueira vence paralelo.** O revisor do diff só dispara depois que o último construtor
  entregou — não por dependência de saída, mas porque o diff que ele lê tem de ser o diff final

### Todo disparo é visível — o quadro de despacho

Antes de despachar (mesmo um agente só), mostrar o quadro; no retorno, reportar **contra o mesmo
quadro**: o que cada agente entregou, o que falhou, o que foi refeito. Nada de delegação silenciosa.

Formato do quadro (colunas e exemplo): [`references/roteamento-e-despacho.md`](references/roteamento-e-despacho.md#formato-do-quadro-de-despacho).

O quadro **vai para o `03-progresso.md`**, seção `## Despachos`, uma linha por disparo com o
resultado e a auditoria do retorno. É o único registro de **qual modelo** fez o quê nesta feature
— e é o primeiro instrumento desta coletânea que mede **custo de operar**, não só eficácia.

### Rodam em linha, sem despacho

Tarefa de 1–2 passos; interação direta com o usuário; decisão que depende do contexto imediato da
conversa; edição cirúrgica em arquivo com forte interdependência; captura **verbatim** do requisito
(copiar não é tarefa, e passar a fonte por um resumo de sub-agente seria alterá-la). Nesses casos,
declarar **"Sem despacho — motivo"**, citando a exceção.

Exceção que **não** vale: *"a tarefa é pequena, então reviso eu mesmo."* Tamanho não compra
cegueira. O passe de eixos do 6.5, a revisão adversarial e o step 8 vão para sub-agente **sempre**.

### Auditoria do retorno

A sessão principal confere o retorno de **todo** lote antes de usá-lo:

- **presença** — o agente entregou tudo o que o quadro pedia, no formato fixo?
- **integridade** — nenhuma proibição do contrato violada: código de aplicação intacto, `00`
  intacto, `04` intacto (`git status` e `git diff --stat` antes e depois do lote)
- **amostragem** — 2–3 itens conferidos com `Read`/`grep` direto. O step 3 já manda *"confirmar os
  trechos críticos com `Read` direto"* para o `Explore`; a regra vale para todo retorno

**Sinais que reprovam o retorno antes da amostragem** (casos em [`references/casos-medidos.md`](references/casos-medidos.md#sinais-que-reprovam-o-retorno--2026-09-21)):

- **número sem comando** — *"88 ok"*, *"32 convertidas"*: se o retorno não traz o comando e a
  saída literal, o número não existe
- **`git diff --stat` como prova de arquivo untracked** — a wiki nova não aparece no diff; retorno
  que a "prova" por ele não a conferiu
- **"não encontrado" / "não instalado" sem a prova negativa** — `ls vendor/…`, `php -m`, `grep -c`
  colados
- **"sem ocorrências" em grep com FQCN** — conferir o escape (`grep -F`) antes de aceitar
- **conclusão de custo sob paginação** — *"nada cresce com N"* medido com página de 10 linhas não
  mede nada; pedir N acima da página

Retorno reprovado é refeito pelo mesmo agente com o achado, ou escalado de modelo — e o quadro
registra os dois casos: **auditoria reprovada é linha do quadro**, com o redespacho ao lado, não
apagão. **Interrupção no meio do lote** (limite de sessão, 429): o construtor pode ter deixado a
árvore meio-editada. Antes de retomar, `git status` e `git diff --stat`; retomar o **mesmo** agente
por `SendMessage` (o contexto dele sobrevive) em vez de despachar um novo sobre o estado parcial.

### Mapa de roteamento por step

Antes do primeiro despacho de cada step, confira a linha dele no mapa em
[`references/roteamento-e-despacho.md`](references/roteamento-e-despacho.md#mapa-de-roteamento-por-step):
rota, o que roda em paralelo e o que cada sub-agente **não recebe**.

## Fluxo de Execução

### 0. Capturar o Requisito — PRIMEIRO ATO

**Antes de descobrir branch, antes de nomear a feature, antes de qualquer pesquisa.**
O procedimento está em [Captura do Requisito](#captura-do-requisito-primeiro-ato--antes-de-qualquer-pesquisa),
dentro do step 3, porque é lá que ele convive com o resto da pesquisa — mas **a execução dele é aqui**.

> Por que a ordem importa: o step 2 manda nomear a feature, e nome de feature não se decide bem
> antes de ler o que foi pedido. Nomear primeiro é fixar uma interpretação antes de ter o requisito.

### 1. Descobrir Branch e Estrutura de Pasta

```bash
git rev-parse --abbrev-ref HEAD
```

Branch `ferro/501` → pasta base: `wikis/specs/ferro/501/`
Branch `feature/user-auth` → pasta base: `wikis/specs/feature/user-auth/`
Branch `fix/boleto-juros` → pasta base: `wikis/specs/fix/boleto-juros/`

### 2. Definir Nome da Feature

Derivar **do requisito capturado no step 0**, e confirmar com o usuário:
- Nome deve ser `kebab-case`
- Deve descrever a feature, não o ticket
- Exemplos: `envio-progresso`, `unico-jobs-progress-tracking`, `api-webhook-payments`

Pasta final: `wikis/specs/{branch}/{feature-name}/`

### 3. Pesquisa e Contexto (OBRIGATÓRIO antes de escrever)

#### Captura do Requisito (PRIMEIRO ATO — antes de qualquer pesquisa)

O requisito é a **fonte da verdade** de toda a wiki e o oráculo do `feature-quality-gate`. Ele precisa ser capturado **verbatim** antes de o agente interpretar qualquer coisa.

**Como o requisito chega** — identificar qual dos casos e registrar a origem:

| Origem | O que fazer |
|---|---|
| **Texto colado no chat** (card do Jira/Azure/GitHub, e-mail, mensagem) | copiar **exatamente** como veio, sem corrigir ortografia, sem resumir, sem reordenar |
| **Arquivo no projeto** (`.md`, `.pdf`, `.docx`) | `Read` o arquivo; registrar o **path + páginas/seções** e transcrever os trechos normativos literalmente |
| **Descrição verbal do usuário na conversa** | transcrever o que foi dito literalmente e **marcar como fonte de baixa fidelidade** — pedir confirmação antes de seguir |
| **Nenhuma das anteriores** (só "implementa X") | **parar e pedir o requisito.** Sem requisito não há oráculo, e a wiki nasce sem linha de base |

**Regra dura**: o texto original é **imutável**. Se estiver ambíguo, incompleto ou contraditório, a ambiguidade é **achado**, não algo a "melhorar" na transcrição. Corrigir o requisito na captura destrói a única linha de base independente do agente.

**Caso especial — o requisito pressupõe algo que não existe no projeto.** É comum: o card fala em
"aplicar o desconto no pedido" e **não existe `Pedido`** — nem model, nem tabela. Isso não é
ambiguidade de redação, é **premissa de escopo**, e escolher sozinho entre *"entrego só o motor"* e
*"crio a entidade que falta"* é decidir o tamanho da entrega no lugar do usuário.

Procedimento:

1. `Grep`/`Glob` para **confirmar a ausência** antes de declará-la — pode existir com outro nome
2. Listar quais `RQ` dependem da entidade ausente
3. **Perguntar ao usuário**, com as duas opções e o custo de cada uma
4. Se o usuário não estiver disponível: seguir com a premissa **mais estreita** (entregar o que
   existe, não criar a entidade), registrá-la em `## Ambiguidades` e marcar as `RQ` dependentes
   como **fora desta entrega** em `## Cobertura do Requisito` — nunca como atendidas

Premissa de escopo tomada em silêncio é a forma mais cara de erro da wiki inteira: tudo fica
coerente, verde, e entrega outra coisa.

Em seguida, **decompor em cláusulas numeradas** (`RQ-01`, `RQ-02`, …), cada uma citando o trecho literal de origem. A decomposição é derivada e revisável; o texto bruto não.

**Granularidade da cláusula — o critério.** Não é uma por frase nem uma por verbo. É:

> **Uma `RQ` = uma afirmação que pode ser verdadeira ou falsa sozinha, e cuja violação é
> observável.**

Testes práticos, nesta ordem:

1. **Consigo imaginar um sistema que atende tudo, menos esta cláusula?** Se não, ela está grudada
   em outra — funda as duas
2. **A cláusula tem dois "e" que podem falhar separadamente?** ("só admin cria **e** edita **e**
   exclui" são três permissões) — separe, porque a matriz de rastreabilidade vai marcar ✅ com
   duas das três implementadas
3. **A cláusula sobrevive sem contexto?** Se ela só faz sentido lida junto da anterior, funda

Grosso demais **esconde omissão** (uma `RQ` marcada ✅ com metade entregue); fino demais vira
ruído e a matriz fica ilegível. Na dúvida, **separe** — fundir depois é barato, e a omissão
escondida não aparece nunca.

**Quando não há usuário para responder a ambiguidade.** A skill manda perguntar antes de
implementar. Se não houver ninguém disponível, a ambiguidade **não vira silêncio**: registre em
`## Ambiguidades` no par obrigatório

```markdown
- **RQ-04** — o limite de usos é global ou por usuário?
  - **Assumido**: global (o card fala em "limite de quantas vezes pode ser usado", sem sujeito)
  - **Se negado**: RQ-04 muda de escopo; o passo 6 do PRD e os cenários CT-09..CT-11 são refeitos
```

e propague a premissa para `## Cobertura do Requisito`, marcando a `RQ` como **atendida sob
premissa**. Premissa sem "Se negado" é suposição disfarçada de decisão: ninguém sabe o custo de
descobrir que ela estava errada.

> **Por que isso existe**: sem o `00-requisito.md`, o único registro do que foi pedido é o PRD — que é a **interpretação** do agente. Se a interpretação estiver errada, ela contamina plano, testes, código e validação de forma coerente, e nada no ciclo detecta. Ver [Arquivo 00](#arquivo-00-requisito--fonte-da-verdade).

Antes de escrever qualquer documento:
- Usar `database-schema` se a feature envolve novas tabelas ou alterações
- **Usar `search-docs` para toda stack envolvida** — obrigatório antes de escrever o PRD (ver [Documentation API](#documentation-api-do-boost-search-docs) para cobertura e como consultar)
- Ler arquivos existentes relevantes com `Read` ou `Grep`
- Executar `php artisan model:show ModelName` para models relacionados
- Examinar padrões existentes com `Glob "**/[padrão]/**/*.php"`
- **Inspecionar APIs de terceiros** antes de escrever CTs — verificar vendor source ou docs oficiais para confirmar nomes de métodos, assinaturas e restrições de schema. E isso nunca basta sozinho: **toda** feature que cria página, widget ou componente preenche a [Superfície Livewire](#superfície-livewire-obrigatório-em-toda-feature-que-cria-página-widget-ou-componente)
- Para features médias/grandes: delegar o mapeamento amplo a um agent `Explore` e depois **confirmar os trechos críticos com `Read` direto** (linhas exatas, imports, assinaturas) — não confiar apenas no resumo do agent. No Claude Code, os greps prescritos nesta lista e na Superfície Livewire vão para `mecânico` (`haiku`) **em paralelo**, cada um devolvendo a tabela pronta — ver [Execução e Delegação](#execução-e-delegação-claude-code--roteamento-por-modelo-e-por-cegueira)
- **Validar dados fornecidos pelo usuário** (CSV, listas, IDs) contra o banco via `database-query` — detectar divergências de título/chave, escolher chave estável (ID) para mapeamentos e documentar as divergências no plano
- **Verificar existência de factories** (`Glob "database/factories/{Model}*"`) e states disponíveis antes de escrever CTs; se não houver factory, especificar `Model::create([...])` no Setup Global
- **Confirmar padrões internos citados** no plano com grep/read (ex: seeder-em-migration, guards de environment, `$casts` property vs `casts()`) — citar `arquivo:linha` de referência no plano
- **Verificar rotas existentes** — `Grep` em `routes/web.php` e `routes/api.php` para evitar conflito de endpoints e entender naming conventions
- **Verificar Policies/Gates** — `Glob "app/Policies/*.php"` e `Grep` por `Gate::define` para entender o padrão de autorização do projeto
- **Verificar config files** — `Read` em `config/*.php` relevantes à feature (services, logging, queue, auth)
- **Verificar composer.json** — `Read` em `composer.json` para pacotes instalados que poderiam ser reutilizados em vez de criar do zero
- **Verificar wikis existentes** — `Glob "wikis/specs/**/*.md"` para features relacionadas que já foram documentadas e podem ter decisões relevantes
- **Verificar git log do branch** — `git log --oneline -20` para contexto do que já foi feito no branch
- **Verificar scheduled tasks** — `Grep` em `app/Console/Kernel.php` ou `routes/console.php` se a feature envolve cron/scheduling
- **Verificar eventos/listeners** — `Glob "app/Events/*.php"` e `Glob "app/Listeners/*.php"` se a feature emite ou escuta eventos
- **Verificar observers** — `Glob "app/Observers/*.php"` para hooks de model existentes
- **Verificar middleware** — `Grep` em `app/Http/Middleware/` e em `bootstrap/app.php` (Laravel 11+) para middleware stack
- **Verificar variáveis de ambiente** — `Read` em `.env.example` para chaves existentes e padrão de naming

#### Superfície Livewire (OBRIGATÓRIO em toda feature que cria página, widget ou componente)

Tudo o que o **cliente** pode escrever ou chamar entre requests. Não é uma seção sobre pacotes —
é sobre a **fronteira que o navegador alcança**, e o pacote de terceiro é só uma das origens dela.

> Casos que fixaram esta seção (2026-09-15 e 2026-09-17): [`references/casos-medidos.md`](references/casos-medidos.md#step-3--superfície-livewire).

Produzir a tabela `## Superfície Livewire` no `02-decisoes-arquiteturais.md`, uma linha por ponto
que o **cliente** alcança — de qualquer origem:

| Origem | O que inventariar | Por que |
|---|---|---|
| **o código do projeto** | todo `public function` de Page, Widget ou componente Livewire; toda `public $` sem `#[Locked]` | método público de componente Livewire **é ação chamável pelo cliente**, e o retorno vai para o navegador; propriedade pública é escrita pelo cliente **entre requests** |
| **o framework** | os arrays de estado que o framework publica e o seu código consome — `$filters` (`HasFilters`), `$pageFilters` (`InteractsWithPageFilters`), `$tableFilters`, `$tableSearch`, `$tableSortColumn` | são **entrada de usuário não validada** que vira `where`, índice de array e parse de data. O framework os declara `public` |
| **o pacote de terceiro** | ações que recebem id/argumento do cliente, propriedades públicas e models que a feature persiste | ver a varredura abaixo |

Varredura mínima — os greps, com o resultado colado na tabela.

Antes de varrer, leia [`references/pesquisa-step-3.md`](references/pesquisa-step-3.md#superfície-livewire--formato-e-greps):
o formato da linha da tabela e os greps — dois no código que a feature escreve (**sempre**) e quatro
no pacote de terceiro (quando a feature monta sobre um).

**Regra dura**: **todo model do pacote que a feature persiste aparece na tabela com a própria
fronteira.** *"É filho do outro, logo está protegido"* só vale com a evidência de que **nenhum**
ponto de entrada o alcança direto — e essa evidência é um `grep`, não uma dedução.

**Segunda regra dura**: **todo valor que entra por um desses pontos e vira
índice de array, argumento de `parse`, nome de coluna ou operador é um cenário de domínio
inválido.** Público sem validação não é "detalhe de framework": `$rotulos[$situacao]` sem `??` e
`Carbon::parse($filtro)` sem guarda são 500 que nenhum teste de caminho feliz vê, porque a tela
sanitiza o valor **na página** e os widgets o recebem **direto**.

A tabela é **entrada obrigatória da `feature-test-design`** (step 4): cada linha vira gatilho do
checklist de taxonomia, e a linha sem cenário correspondente é lacuna declarada, não silêncio.

#### Verificação do stack de testes (define se haverá CT-B)

- **Versão do Pest** — `Grep "pestphp/pest" composer.json`. Pest 5 habilita `--tia`, `--agent` e sharding por tempo; Pest 4 tem browser plugin mas não TIA
- **Browser plugin instalado?** — `Grep "pest-plugin-browser" composer.json` e `Glob "tests/Browser/**"`
  - Se a feature tem UI e o plugin **não** está instalado: incluir a instalação como passo explícito no PRD (`## Dependências`), não assumir que existe
  - Se `tests/Browser/` já existe: ler 1-2 testes para herdar o padrão do projeto (helper de login, traits no `Pest.php`, seletores usados)
- **Playwright instalado?** — `Grep "playwright" package.json`; browsers baixados via `npx playwright install`
- **Como o app é servido em teste** — o `pest-plugin-browser` **sobe o próprio servidor** (HTTP in-process, porta aleatória): não há Herd, `php artisan serve`, Sail nem `APP_URL` a configurar. O que confirmar é outra coisa: se o projeto roda `npm run build` antes da suíte de browser (pré-requisito duro — sem o manifest do Vite toda tela responde `ViteException`) e qual o teto em `pest()->browser()->timeout()`
  - Antes de planejar CT-B, leia os demais fatos do plugin (`actingAs()`, esperas, ordem das asserções) em `{skills}/feature-test-design/references/pest-plugin-browser.md`
- **Traits globais** — `Read tests/Pest.php` para ver se `RefreshDatabase` está aplicado globalmente e se há `pest()->browser()` ou `pest()->tia()` configurado

#### Documentation API do Boost (`search-docs`)

O Boost expõe a tool MCP **`search-docs`**, que consulta a Documentation API hospedada da Laravel — 17.000+ trechos com busca semântica por embeddings, **filtrada pelos pacotes que o projeto realmente tem instalados**. É a primeira fonte a consultar, antes de vendor source e antes de doc na web.

Antes de escrever o PRD, leia [`references/pesquisa-step-3.md`](references/pesquisa-step-3.md#documentation-api-do-boost-search-docs):
cobertura por versão, a tabela de quando a consulta é obrigatória (trecho do PRD × stack), como
consultar bem e as lacunas com o fallback de cada uma (Pest 5, `pest-plugin-browser`, pacotes de
terceiros, código da aplicação).

> **Anti-padrão**: escrever no PRD assinatura de método, nome de opção de config ou comportamento de componente **sem** confirmar em `search-docs` (ou, nas lacunas listadas em `references/pesquisa-step-3.md`, na doc oficial). É a causa nº 1 de plano que não sobrevive à implementação.
>
> **Anti-padrão**: usar `search-docs` para descobrir comportamento do **seu** código. Ele documenta o ecossistema; o seu código é `Grep`, e as suas convenções são `.ai/rules/`.

### 4. Criar os Arquivos

Criar os **5 arquivos obrigatórios** + extras se necessário.

**Ordem de criação**:
1. **`00-requisito.md`** — requisito bruto + decomposição em `RQ-##`; é a linha de base de tudo
2. **`01-plano-acao.md`** — PRD deriva do `00`; cada passo deve citar quais `RQ` atende
3. **`02-decisoes-arquiteturais.md`** — ADRs justificam escolhas do PRD
4. **`04-casos-de-teste.md`** e, condicionalmente, **`05-casos-de-teste-browser.md`** —
   **invocar a skill `feature-test-design`**. Ela deriva os cenários do **`00-requisito.md`**;
   o PRD entra só para paths, rotas e a tabela `## Superfície de UI`; o `02-decisoes-arquiteturais.md`
   entra só pela `## Superfície Livewire`
5. **`03-progresso.md`** — espelha os passos do PRD (por isso é o último; se houver CT-B, o progresso também os lista)

Antes de escrever cada arquivo, leia o template dele: [`references/template-00-requisito.md`](references/template-00-requisito.md),
[`references/template-01-plano.md`](references/template-01-plano.md), [`references/template-02-adr.md`](references/template-02-adr.md)
e [`references/template-03-progresso.md`](references/template-03-progresso.md). Antes de especificar os
logs do `01`, leia [`references/padrao-de-log.md`](references/padrao-de-log.md). Antes de invocar a
`feature-test-design`, leia [`references/delegacao-casos-de-teste.md`](references/delegacao-casos-de-teste.md#o-contrato-da-delegação).
Antes de decidir arquivos extras (`05-*`), leia [`references/estrutura-criada.md`](references/estrutura-criada.md).

> **Não escrever o `04` inline.** O caso de teste derivado do plano confirma o plano — é a
> mesma cegueira correlacionada que o `00-requisito.md` existe para quebrar. Ver
> [Arquivos 04 e 05](#arquivos-04-e-05-casos-de-teste--delegados-à-feature-test-design).
> Se a skill `feature-test-design` não estiver instalada, **declarar a degradação no
> `03-progresso.md`** antes de escrever o `04` à mão.

> **Rastreabilidade obrigatória**: todo passo do PRD e todo CT/CT-B referencia o `RQ` de origem. É isso que permite ao `feature-quality-gate` montar a Matriz de Rastreabilidade e detectar cláusula sem plano, sem teste ou sem código.

**Wiki já existente**: se `wikis/specs/{branch}/{feature}/` já existe:
- **Perguntar ao usuário** se deseja sobrescrever, incrementar (v2) ou retomar
- Se retomar: ler `03-progresso.md` para ver o que já foi feito e continuar de onde parou
- Se sobrescrever: backup manual pelo usuário antes de criar a nova (a skill não arquiva automaticamente)
- **Requisito novo no meio da implementação** (mesma branch, mesmo PR): não é wiki nova nem "incrementar" — é **Adendo** ao `00`. Ver [Adendo ao requisito](#adendo-ao-requisito--quando-o-pedido-cresce-durante-a-implementação). Sem isso o pedido vai direto para o código e os testes dele nascem do código

### 5. Revisão Profunda Pós-Escrita (OBRIGATÓRIO)

Após escrever os 5 arquivos, **re-validar cada premissa do plano contra o código real** antes de apresentar ao usuário:

- Reler os pontos exatos citados no plano: imports dos arquivos a editar, assinaturas de métodos, relações de models, padrão das migrations-referência, factories/states usados nos CTs
- **Corrigir a wiki imediatamente** quando a revisão contradisser o plano (ex: plano diz "adicionar import X" → import já existe; plano cita guard genérico → padrão real é `! app()->environment('testing')`)
- **Registrar cada correção** em `03-progresso.md` → `## Auditoria Pré-Implementação` → *Revisão profunda*. Correção aplicada e não registrada some: a próxima pessoa refaz a verificação e o histórico não mostra que a premissa original estava errada
- Só então avançar para o step 6 (Auditoria da Wiki)

**Padrão de despacho (Claude Code)** — o mesmo do `PM_Arquiteto`: **levantar com `mecânico`,
julgar com `analista`**. Um `haiku` por bloco de premissas devolve a tabela *premissa do plano ×
o que o código diz* (`arquivo:símbolo:linha` conferido por grep, assinatura real, import
existente); a sessão — ou um `analista`, quando a divergência exige decisão — julga cada linha e
corrige a wiki. Levantar é volume; julgar é raciocínio. Misturar os dois num só agente caro é o
desperdício que o roteamento existe para evitar.

> Exemplo real: [`references/casos-medidos.md`](references/casos-medidos.md#step-5--revisão-profunda-e-classe-irmã).

#### Varredura da classe irmã (OBRIGATÓRIA para toda classe nova)

A revisão acima confere o que o plano **afirma**. Este item confere o que o plano **não sabe que
existe**: as listas paralelas que o projeto mantém à mão e que nenhuma rule enumera por completo.

Procedimento, uma linha por classe nova:

```bash
# Onde uma classe IRMÃ já existente é citada? É onde a nova também precisa aparecer.
grep -rn "App\\\\Filament\\\\Admin\\\\Pages\\\\Dashboard" --include=*.php app config database tests
```

Escolher como irmã a classe **mais parecida em papel** (outra Page de dashboard, outro Resource do
mesmo painel, outro Widget da mesma família) e conferir **todos** os lugares onde ela aparece:
`config/*.php`, seeders, listas de exclusão, inventários de teste, `->pages()`/`->widgets()` dos
providers, matrizes de permissão. Cada ocorrência é uma pergunta: *a classe nova entra aqui também?*

> Caso que originou a varredura (2026-09-17, o "checkbox que mente"): [`references/casos-medidos.md`](references/casos-medidos.md#step-5--revisão-profunda-e-classe-irmã).

Registrar o resultado em `03-progresso.md` → `## Auditoria Pré-Implementação`, com a irmã escolhida
e as ocorrências encontradas. "Nenhuma ocorrência além das previstas" é resposta válida e precisa
estar escrita.

### 6. Auditoria da Wiki com Ponytail-review (OBRIGATÓRIO)

Após a revisão profunda (step 5), **invocar automaticamente** `/ponytail:ponytail-review` para auditar a wiki criada. Este step é função direta da skill — o agente NÃO deve esperar o usuário pedir.

**Por que auditar a wiki**: O plano de ação pode conter over-engineering — passos desnecessários, abstrações prematuras, complexidade que não agrega valor. A auditoria com Ponytail-review identifica esses pontos **antes** da implementação começar, economizando tempo de desenvolvimento.

**Sem o plugin Ponytail instalado**: a sessão faz o passe de over-engineering manualmente com a escada de simplicidade e registra *'Ponytail indisponível — passe manual'* em `## Auditoria Pré-Implementação` do `03`.

**Como executar**:
1. Invocar `/ponytail:ponytail-review` apontando para os arquivos da wiki criada em `wikis/specs/{branch}/{feature}/`
2. Analisar cada sugestão de corte/simplificação retornada
3. **Aplicar as sugestões relevantes** diretamente nos arquivos da wiki:
   - Passos desnecessários → remover do `01-plano-acao.md` e `03-progresso.md`
   - Abstrações prematuras → simplificar ou marcar como YAGNI
   - Complexidade excessiva → quebrar em passos menores ou simplificar
   - Over-engineering em CTs → simplificar setup, reduzir mocks desnecessários
4. **Re-executar** `/ponytail:ponytail-review` se houver mudanças significativas (>3 arquivos alterados)
5. Só então apresentar ao usuário para aprovação / iniciar implementação

**Ordem com o step 4** (caso em [`references/casos-medidos.md`](references/casos-medidos.md#step-6--ordem-com-o-step-4-2026-09-21)): o `04` derivado
**antes** dos cortes do Ponytail herda os elementos cortados. Duas regras:

1. **Preferir** rodar este step sobre `01`/`02` **antes** de invocar a `feature-test-design`: a
   derivação recebe do `01` só paths, rotas e `## Superfície de UI` — exatamente o que os cortes
   mudam
2. Se o `04` já existe quando um corte muda rota, ação, filtro ou coluna da `## Superfície de UI`,
   **re-sincronizar o `04` no mesmo passo**: um `mecânico` cruza o `## Índice de Cenários` com os
   elementos cortados; cada CT atingido vira `@obsoleto` com o motivo (e sai do índice com `~~`)
   ou é re-derivado pela `feature-test-design`. Registrar em `### Auditoria Ponytail (step 6)` do
   `03`. CT órfão descoberto só no step 7 é sinal de que este item foi pulado

> **Importante**: Esta auditoria revisa o **plano** (a wiki), não o código implementado. A auditoria do código implementado acontece no step 7 (Pós-Implementação) e nos templates de Verificação Final.
>
> **Comando correto**: `/ponytail:ponytail-review` (com namespace `ponytail:`). NUNCA usar `/ponytail-review` sem o namespace — o comando não será encontrado.

### 6.5. Revisão de Código do Diff (OBRIGATÓRIO, logo após os testes passarem e antes da reconciliação)

**Quando**: a suíte da feature está verde e o último passo do PRD foi entregue — **antes** do
step 7. A ordem é **6.5 → 7 → 8 → PR**, e o motivo é mecânico: cada achado confirmado aqui vira
Adendo no `00`, CT no `04` e correção no código, e isso desloca linha citada, cria ID de CT e muda
frase de doc e de ADR. Reconciliar (7) antes de revisar é reconciliar duas vezes. E a dimensão L do
step 8 repete a reconciliação por quem não a fez, então ela precisa ser a **última** coisa antes
dele. Até a 3.3.0 este step era o 7.5 e rodava depois do 7; mudou só a posição — o gate é o mesmo.

**Por quem não implementou** — sobre o **diff completo** da feature contra a base
(`git diff {base}...HEAD` mais o não-commitado), não sobre os arquivos que o agente lembra de ter
tocado.

**Pré-requisitos do lote** (casos em [`references/casos-medidos.md`](references/casos-medidos.md#step-65--revisão-do-diff)):

- **A sessão roda no repositório do projeto.** O `/code-review` só alcança o diretório onde a
  sessão foi aberta; sessão aberta noutro repositório não consegue apontá-lo para o projeto. Nesse
  caso o passe 1 é substituído por um `analista` (`opus`) **cego**, com o mesmo alvo
  (`{base}...HEAD`) e sem os eixos, e a linha de `## Despachos` declara *"passe genérico por
  sub-agente — `/code-review` fora de alcance"*. Vale menos: o comando nativo tem heurísticas
  próprias que o substituto não tem
- **A `## Superfície Livewire` do `02` foi re-varrida sobre o código final.** A tabela nasce no
  planejamento e **envelhece** durante a implementação. Um `mecânico` refaz os quatro greps sobre o diff final **antes** de despachar o
  revisor; a tabela atualizada é o que ele recebe — a antiga é insumo do plano, não prova.
  Antes de despachar o `mecânico`, leia os greps em
  [`references/pesquisa-step-3.md`](references/pesquisa-step-3.md#superfície-livewire--formato-e-greps)
  e passe-os literais no prompt

**Por que existe, e por que nenhum outro step cobre**: o step 6 audita o **plano**
(`ponytail-review`, over-engineering); o step 8 confronta **requisito × app rodando** (omissão
silenciosa). Nenhum dos dois lê o diff atrás de **defeito de correção**. Entre um e outro passa
uma classe inteira: escrita cross-tenant, propriedade pública que o cliente escreve, gate que
falha aberto no caso nulo, estado de erro sem saída. Nada disso é visível para quem pergunta *"o
requisito foi atendido?"* nem para quem pergunta *"o plano é simples demais?"* — e tudo isso passa
com a suíte verde, porque os testes foram derivados da mesma leitura que produziu o defeito.

#### Quando rodado no Claude Code — dois passes, no mesmo lote

| Passe | Ferramenta | O que pega | Como |
|---|---|---|---|
| **1. Genérico** | `/code-review high {base}...HEAD` | defeito de correção que qualquer revisor competente vê: nulo não tratado, condição invertida, exceção engolida, N+1, uso errado de API | o comando já roda em sub-agente isolado — a cegueira ao contexto da sessão vem de graça |
| **2. Eixos** | sub-agente `fw-revisor-diff` (`opus`, sem Edit/Write) | os eixos da tabela abaixo — são de Laravel, Livewire e multi-tenant, e o passe genérico **não os conhece** | recebe: o diff, a tabela de eixos, a `## Superfície Livewire` do `02` e as rules cujos globs casam o diff. **Não recebe**: `01`, `03`, nem o raciocínio da sessão |

Os dois disparam **juntos** — são independentes. Regras dos passes:

- **Alvo explícito, sempre.** Sem alvo, o `/code-review` compara com o merge-base do **upstream**
  da branch: numa branch já pushada o "diff atual" vira só o não-commitado, e a revisão sai vazia
  parecendo limpa. Escrever `main...HEAD` (ou a base real do PR)
- **Nível `high`.** `low`/`medium` devolvem só achado de alta confiança; aqui o achado incerto é
  bem-vindo, porque o roteamento **obriga a rejeitar com motivo** — e relatório sem rejeição
  parece que só procurou onde achou
- **`--fix` é proibido.** Quem julga não conserta (princípio 2 da `feature-quality-gate`), e o
  roteamento exige Adendo → CT → correção **nessa ordem**; o `--fix` pula os dois primeiros e
  entrega correção sem oráculo
- **O comando não aceita foco em texto livre** — o que vier depois do nível é lido como alvo. Por
  isso os eixos vão num sub-agente próprio, não num argumento do `/code-review`
- **Re-revisar uma única vez**, e só se alguma correção tocou eixo de fronteira (dado, superfície,
  estado de erro) — correção é código novo do mesmo agente. Teto de 2 rodadas; se a segunda ainda
  trouxer achado estrutural, o problema é o plano: registrar e escalar

**Checkpoint opcional durante a implementação**: depois de um passo do PRD que cria query com
discriminante, `public function`/`public $` em componente, ou estado de erro novo, rodar
`/code-review medium` sobre o diff não-commitado. Achado aqui custa uma linha; o mesmo achado no
6.5 custa Adendo, CT, correção e re-teste. O checkpoint **não substitui** o passe completo — ele
não enxerga simetria de guarda entre superfícies que ainda não existem.

**Fora do Claude Code**: o passe 2 é o gate inteiro. Host com sub-agente: `revisor-diff` com o
mesmo contrato. Host sem sub-agente: em linha, com a degradação declarada no `03` —
*"6.5 em linha — mesma sessão que implementou"* — porque o resultado vale menos, e o leitor do PR
precisa saber.

**Eixos obrigatórios da revisão** (além do que o revisor achar por conta):

| Eixo | Pergunta |
|---|---|
| Fronteira de dado | toda query que o usuário alcança filtra pelo discriminante? e quando o discriminante é **nulo**, ela **fecha** ou **abre**? |
| Ponto de entrada do vendor | as ações do pacote que recebem id/argumento do cliente estão cobertas pela mesma fronteira? conferir contra `## Superfície Livewire` do `02` |
| Propriedade pública Livewire | o que o cliente pode escrever **entre requests**? `#[Locked]` em toda propriedade que decide **onde** a escrita cai |
| **Método público de componente** | todo `public function` de Page/Widget é **ação chamável por `$wire.`**, e o retorno vai para o navegador. Tem lista fechada de argumentos, ou aceita qualquer string? |
| **Valor de estado usado sem validar** | todo valor vindo de `$filters`, `$pageFilters`, `$tableFilters` ou `$tableSearch` que vira **índice de array**, argumento de **`parse`**, nome de **coluna** ou **operador** tem guarda? A página pode sanitizar e o widget receber cru |
| **Lista paralela** | nasceu classe nova? o FQCN de uma classe **irmã** aparece em quantos lugares (`config/`, seeders, inventários de teste, providers)? a nova entrou em todos? |
| **Simetria de guarda** | duas superfícies da mesma fronteira se comportam igual? uma fecha com log e a outra fecha em silêncio? |
| Estado de erro | todo 4xx/redirect novo tem saída — para onde o usuário vai depois? par "A devolve para B, B devolve para A" é blocker |
| Afirmação de comentário | comentário que justifica a **ausência** de um controle tem `arquivo:linha` do vendor provando? |

> Os quatro eixos em negrito vieram de um caso medido: [`references/casos-medidos.md`](references/casos-medidos.md#step-65--revisão-do-diff).

**Roteamento do achado** — igual ao do quality gate, e nesta ordem:

1. Achado confirmado vira **Adendo numerado no `00`** (`## Adendo N`, premissas `Pnn`) — porque ele
   muda o que a feature promete, não só o código
2. Vira **CT novo no `04`** (regra, cenário Gherkin e os mutantes que ele mata), **antes** da
   correção
3. Só então a correção
4. Achado **rejeitado** fica registrado com o motivo. Relatório sem rejeição parece que só procurou
   onde achou

**Falsificabilidade da correção (duro)**: antes de fechar, provar que o CT novo **falha sem** a
correção — `git stash push -- app/`, rodar o CT, `git stash pop`. CT que passa dos dois lados não é
oráculo, é decoração — **salvo quando a pilha de teste não consegue exibir o defeito**. Três saídas,
e a terceira precisa estar escrita:

| Sem a correção, o CT… | Veredito | Registro na `## Verificação Final` |
|---|---|---|
| falha | oráculo válido | `n de m falham sem o fix` |
| passa, e a pilha exibiria o defeito | decoração — reescrever o CT | — |
| passa porque a pilha **não exibe** o defeito (SQLite ignora `VARCHAR(255)`; `RESTRICT` sem `PRAGMA foreign_keys`; cascata só em memória) | **"não falsificável nesta pilha — guarda mantida, dívida declarada"** | linha com o motivo e o que exibiria (MySQL/Postgres em CI) |

> Casos da falsificabilidade e da revisão do diff "verde e concluído" (2026-09-15, 2026-09-21): [`references/casos-medidos.md`](references/casos-medidos.md#step-65--revisão-do-diff).

### 7. Pós-Implementação e Reconciliação (OBRIGATÓRIO, antes do PR)

Após a implementação, os testes passarem e o **step 6.5 ter rodado** — e **antes de abrir o PR e
antes de escrever "concluída" no `03`**. A ordem é **6.5 → 7 → 8 → PR**: o diff que se reconcilia
aqui é o diff **pós-revisão**.

Os casos que fixaram essa ordem e os itens 4, 5 e 6 abaixo estão em
[`references/casos-medidos.md`](references/casos-medidos.md#step-7--reconciliação). Antes dos itens 3 e 4,
leia [`references/citacoes-de-codigo.md`](references/citacoes-de-codigo.md).

**Fontes a reconciliar** — a lista é fechada; o que não está nela não é reconciliado por acidente:
`01`, `02`, `04`, `05`, `03`, docs de usuário (pt **e** en), `CHANGELOG.md`, `README`, e as rules
de `.ai/rules/` cujos globs casam com o diff.

1. **Checkbox só fecha com evidência inline.** Formato `- [x] {item} — {evidência}, {data}`
   (ex.: `— 677/677 verdes, 2026-09-05`). Item sem evidência continua `[ ]`. É proibido fechar a
   `## Verificação Final` por substituição em lote: cada linha fecha quando o comando dela roda.
   Conferência: `grep -n '^- \[x\]' 03-progresso.md | grep -v ' — '` tem de voltar vazio
2. **Desvio corrige a fonte; o `03` só aponta.** Cada item de "Desvios do Plano" exige a edição
   correspondente no `01`, `02`, `04` ou `05` de origem, marcada inline com
   `*(alterado em {data}: {motivo curto})*`. Registrar o desvio só no `03` deixa o PRD e a ADR
   afirmando o que o código não faz — e é o PRD que a próxima pessoa lê. Critério de saída:
   **nenhuma afirmação do `01`/`02` contradiz o código**
3. **Reverificar toda citação `arquivo:símbolo:linha`** com o grep de
   [Citações de código](#citações-de-código--arquivosímbololinha). Pint e imports novos deslocam
   linhas; a conferência é mecânica e o resultado (`— 14/14 ok`) vai para a Verificação Final
4. **Sincronizar `04`/`05` com o teste real, nos dois sentidos — por comando, não por leitura.**
   Todo `[CT-nn]`/`[CT-Bnn]` do arquivo de teste existe no `04`/`05`; todo CT do índice aponta um
   teste existente ou declara "fundido em CT-nn"; linha de dataset nova no teste existe como
   Exemplo no Gherkin. Cenário que nasceu durante a implementação **nasce no `04` primeiro**
   (Proibição 11 da `feature-test-design`).

   ```bash
   diff <(grep -oh 'CT-B\?[0-9]\+' wikis/specs/{branch}/{feature}/0[45]-*.md | sort -u) \
        <(find tests -name "*{Feature}*.php" -exec grep -oh 'CT-B\?[0-9]\+' {} + | sort -u)
   ```

   **Saída vazia é o critério**; linha com `<` é CT sem teste, linha com `>` é teste sem CT. A
   saída vai colada na `## Verificação Final` — sem ela o checkbox não fecha.
5. **Todo número da wiki é derivado por comando — e procurado na wiki inteira quando muda.**
   Número escrito à mão envelhece **dentro do próprio ciclo**: contagem de CTs, de regras, de
   mutantes, de permissions, de linhas de uma varredura, total de cenários no cabeçalho. A regra
   vale para o `01`, o `02` e o `04`, não só para o `03` — e a conferência é `grep -c` contra o
   código, ao fim, nunca leitura.

   O ponto cego é a **duplicação**: quando um achado corrige um número, a correção vai para o
   arquivo que o achado citou e a **cópia do mesmo número em outro arquivo sobrevive**. Antes de
   fechar, procurar o valor antigo na wiki inteira:

   ```bash
   grep -rn "{valor antigo}" wikis/specs/{branch}/{feature}/
   ```
6. **Conformidade com as rules do projeto.** Para cada rule em `.ai/rules/index.md` cujo glob
   casa com um arquivo do diff, uma linha na tabela `## Conformidade com Rules` do `03`:
   `rule → aplicada / n.a. / violada`, com evidência (`arquivo:símbolo:linha` ou nome do CT).
   Rule violada é blocker do PR. O step 3 manda **ler** as rules antes de planejar; este item
   confere se o **código** as cumpre — são coisas diferentes, e a segunda nunca era feita
7. **Docs de usuário e CHANGELOG × comportamento × rastro.** Toda consequência que a wiki
   descreveu e depois mudou (ex.: "o log registra o painel `app`") é procurada nas docs pt/en, no
   CHANGELOG, no README e na ADR que a originou. Frase nova em doc de usuário **sem `RQ` nem ADR
   de origem** é crescimento sem rastro: vira Adendo no `00` ou sai da doc
8. **Notas de Implementação** no `03`: descobertas durante o código que não estavam no plano
   (ex.: "`Enrollment::find()` aplica scope global de tenant — documentado em `02`")
9. **Roteiro "Desenhado × Implementado"** em `05-casos-de-teste-browser.md` (se existir): rodar os
   CT-B, conferir cada linha da `## Superfície de UI` do PRD contra a tela real, marcar ✅/⚠️/❌;
   divergência vai para "Desvios do Plano" **e** para a fonte (item 2)
10. **Confirmar impacto real com TIA**: `vendor/bin/pest --parallel --tia` × `## Impacto em
   Features Existentes` do PRD — divergência é nota de implementação
11. **Retrospectiva breve** no `03`: o que funcionou no planejamento e o que faltou
12. **Limpeza de channel de log** — só **depois do merge** e da estabilização: reduzir o level de
    `debug` para `info` ou remover o channel

> **Autolimpeza não é auditoria.** Os itens 2, 6 e 7 são julgamento sobre texto que o mesmo
> agente escreveu, e ele tende a lê-lo como certo. Por isso a `feature-quality-gate` (step 8)
> repete os três como **dimensão L — Consistência Documental**, por quem não escreveu a wiki.
> Fazer só um dos dois não basta: sem o 7 o quality gate afoga em defasagem trivial; sem o 8
> ninguém confere quem escreveu.

### 8. Quality Gate e abertura do PR (OBRIGATÓRIO, antes do PR)

Após os testes passarem e o step 7 estar concluído, **invocar a skill `feature-quality-gate`**. Este step é função direta da skill — o agente NÃO deve esperar o usuário pedir. **O PR não abre antes do veredito**, e o `03` não diz "concluída" antes de a seção `## Quality Gate` estar preenchida.

**O que ela faz que os steps 5, 6 e 7 não fazem**: os três tomam o PRD como verdade. O quality gate confronta **`00-requisito.md` × PRD × app rodando** e detecta a classe de defeito que nenhum teste pode pegar — a **omissão silenciosa**: cláusula `RQ` que nunca virou passo, nunca virou CT, nunca virou código. Tudo verde, feature incompleta. E a **dimensão L** dela repete, por quem não escreveu a wiki, o que o step 7 declarou reconciliado: PRD/ADR × código, rules × diff, docs × comportamento, citações e IDs de CT.

**Entrada que a skill espera**:

- `00-requisito.md` com as cláusulas `RQ-##`
- `01`–`05` da wiki
- app servido e acessível
- `## Natureza da Wiki` do PRD (decide se roda regressão)

**Saída**: `06-relatorio-qa.md` + veredito.

**Quando rodado no Claude Code — despachar, não invocar em linha.** A skill exige *"por quem não
escreveu a wiki"*, e invocá-la na mesma sessão que escreveu o `01` e implementou entrega o
contrário disso. Despachar o sub-agente `fw-qa-gate` (`opus`, sem Edit/Write) com **só**: o path
da wiki, a URL do app servido, o `git diff --stat` e a instrução de ler e seguir
`{skills}/feature-quality-gate/SKILL.md`. Ele devolve o `06-relatorio-qa.md` **como texto**, e a
sessão grava o arquivo **sem editar** — a ausência de Edit/Write no agente é o que torna *"não
corrige nada"* uma propriedade, não uma promessa. O cabeçalho do `06` leva a linha
`Independência: sub-agente fw-qa-gate/opus, sem acesso à conversa` — ou `mesma sessão`, quando
degradado. As dimensões que exigem Playwright MCP ou Boost rodam no próprio sub-agente: ele herda
as ferramentas MCP quando o arquivo do agente não restringe `tools`.

| Veredito | O que o fluxo faz |
|---|---|
| `APROVADO` | segue para o step 9 |
| `APROVADO COM DÉBITO` | segue para o step 9; débito fica registrado no `03-progresso.md` |
| `REPROVADO → especificação` | volta ao step 4: corrigir `01`/`02`, depois reimplementar |
| `REPROVADO → implementação` | volta à execução do passo do PRD indicado |
| `REPROVADO → teste` | volta ao `04`/`05`: escrever o CT que falha **primeiro**, depois corrigir |

**Quando pular**: feature sem nenhuma superfície validável (ex.: só refactor interno já coberto por CT verde) — registrar o motivo no `03-progresso.md`, gravando mesmo assim um `06-relatorio-qa.md` mínimo com veredito `NÃO APLICÁVEL` e o motivo; o arquivo continua obrigatório. Não pular por pressa.

> **Teto do loop**: no máximo **3 ciclos** de quality gate por feature. Ao estourar, escalar ao usuário com o que ficou aberto. Ver a skill `feature-quality-gate` para as regras de convergência.

**Depois do veredito, e só então**:

1. Registrar ciclo, veredito e data na seção `## Quality Gate` do `03-progresso.md`
2. **Abrir o PR** com o link da wiki e o veredito do `06-relatorio-qa.md` na descrição
3. Marcar o `03` como "concluída"

> Por que a ordem é dura (caso real): [`references/casos-medidos.md`](references/casos-medidos.md#step-8--por-que-a-ordem-é-dura). O veredito é parte do PR, não um passo depois dele.

### 9. Candidatos a Rule de Projeto (DECISÃO DO USUÁRIO)

**O problema que este step resolve**: hoje uma decisão registrada em `02-decisoes-arquiteturais.md` só é lida por quem abrir aquela wiki. Na sessão seguinte, em outra feature, o agente não sabe que ela existe e repete o erro que a ADR já resolveu. **Project Rules do Laravel Boost** (`.ai/rules/`) fecham esse ciclo: o agente é instruído pelo Boost a consultar o índice antes de planejar ou editar arquivos que casam o glob — qualquer agente, em qualquer sessão.

Após o step 7, **varrer a wiki em busca de candidatos** e **apresentar ao usuário para decisão**. A skill nunca grava rule sem aprovação explícita.

Antes de varrer, leia [`references/candidatos-a-rule.md`](references/candidatos-a-rule.md#fontes-de-candidatos-dentro-da-wiki):
as fontes de candidatos dentro da wiki (`02`, Notas de Implementação do `03`, `01`), com exemplo de cada uma.

**Os 4 gates — candidato só passa se cumprir TODOS**:

1. **Durável** — vale além desta feature e desta sprint? (decisão de fluxo/negócio pontual → não é rule)
2. **Escopável por path** — dá para expressar em glob (`app/Models/**`, `app/Http/Controllers/**`)? Se não se consegue nomear os paths, não é rule — é ADR.
3. **Não-inferível** — um agente competente, lendo o código ao redor, erraria? Se ele acertaria sozinho, a rule é só imposto de contexto.
4. **Não-redundante** — não é default do framework, não é coberto por Pint/Rector/PHPStan, não está nas guidelines do Boost (conferido com `search-docs` — ver `requirement-to-rule`) e não duplica rule existente em `.ai/rules/index.md`.

**Antes de propor**: `Read .ai/rules/index.md` e as rules dos globs afetados. **Atualizar rule existente é sempre preferível a criar uma nova.**

**Teto**: no máximo **3 candidatos por feature**. Cada rule é imposto permanente de contexto em todo arquivo que casa com o glob — inflação de rules degrada o agente em vez de ajudar.

**Preferir enforcement automático à prosa** (escada do Ponytail aplicada a rules): se a restrição pode ser verificada por teste de arquitetura `arch()` do Pest, PHPStan ou Rector, implementar a verificação **e** deixar a rule curta apontando para ela. Prosa só onde a máquina não alcança.

**Como apresentar**: antes de apresentar, leia o formato em [`references/candidatos-a-rule.md`](references/candidatos-a-rule.md#como-apresentar)
— um bloco por candidato (fonte, glob, evidência, os 4 gates) e a pergunta final (`1, 2, ambos, nenhum`).

**Se aprovado**: invocar a skill `requirement-to-rule`, que grava via a tool MCP `record-rule` do Boost (nunca escrevendo o arquivo à mão — o Boost regenera o `.ai/rules/index.md`, e rule criada manualmente não é descoberta até a próxima regeneração).

**Se recusado**: não insistir. A decisão continua registrada na ADR, que é o comportamento atual e já é válido.

---

## Arquivo 00: Requisito — Fonte da Verdade

**Path**: `wikis/specs/{branch}/{feature}/00-requisito.md`

**Propósito**: guardar o requisito **como ele chegou**, sem interpretação, e decompô-lo em cláusulas rastreáveis. É a única linha de base independente do agente — todo o resto da wiki é derivado e, portanto, contaminável por interpretação errada.

**Três seções, dois regimes**:

| Seção | Regime |
|---|---|
| `## Texto Original` | **imutável.** Nunca editar, corrigir, resumir ou reordenar |
| `## Decomposição em Cláusulas` | derivada e revisável. Pode ser corrigida se a leitura estiver errada |
| `## Adendo N — {data}` | **imutável** como o Texto Original; um por pedido novo que chegou durante a implementação, com fonte e data. A numeração de `RQ` continua da última. Ver [Adendo ao requisito](#adendo-ao-requisito--quando-o-pedido-cresce-durante-a-implementação) |

**Obrigatório incluir**:

- Origem (card, arquivo + página, conversa) com data e autor
- Texto original verbatim, ou os trechos literais normativos quando a fonte é longa
- Decomposição em `RQ-##` com: cláusula, trecho literal de origem, tipo (funcional / autorização / não-funcional / restrição)
- **Ambiguidades e perguntas abertas** — cláusula não-testável é achado, não detalhe

Antes de escrever o `00`, leia o template em [`references/template-00-requisito.md`](references/template-00-requisito.md) —
ele traz, em comentário, as perguntas obrigatórias quando o requisito tem papéis, visibilidade,
notificação ou texto livre.

> **Wiki antiga sem `00`**: wikis criadas antes da v2.10.0 não têm o arquivo. Ao retomar uma delas, reconstruir o `00` **pedindo o requisito original ao usuário** — não derivar do PRD. PRD derivado de PRD não é oráculo, e o `feature-quality-gate` vai marcar o relatório como *oráculo degradado*.

### Adendo ao requisito — quando o pedido cresce durante a implementação

O `## Texto Original` é imutável, e a skill só previa "sobrescrever / incrementar / retomar" a
wiki inteira. Entre os dois cabia o caso mais comum: o usuário pede **mais uma coisa** no meio da
implementação, na mesma branch e no mesmo PR. Sem procedimento, o pedido novo vai direto para o
código, e os testes dele nascem **do código** — a inversão exata que a `feature-test-design`
existe para proibir (caso em [`references/casos-medidos.md`](references/casos-medidos.md#adendo-ao-requisito)).

**Procedimento**, na ordem:

1. **Registrar no `00`** uma seção `## Adendo N — {YYYY-MM-DD}` com Fonte (quem, como chegou,
   fidelidade), o Texto Original **verbatim** do pedido novo (mesmo regime de imutabilidade) e a
   decomposição em `RQ` novos, **continuando a numeração** (`RQ-09`, `RQ-10`…). Nunca reescrever
   `RQ` existente para "acomodar" o adendo: se ele muda uma cláusula antiga, a antiga fica e o
   adendo declara qual ela substitui
2. **`## Cobertura do Requisito` do `01`** ganha as linhas dos `RQ` novos; o PRD ganha os passos
   novos ao final (`N+1`…), citando o adendo. Passo antigo que muda por causa do adendo é marcado
   inline com `*(alterado em {data}: adendo N)*`
3. **Reinvocar a `feature-test-design` só para o adendo**: entrada é o `00` (com o adendo) e o
   `04` existente; saída são cenários `CT` novos, em numeração contínua, com mutantes.
   **Antes** de escrever qualquer linha de código do adendo
4. **`03`** ganha a seção do passo novo e o item "Adendo N incorporado" na Verificação Final
5. Só então implementar

**Critério adendo × wiki nova**: mesma branch e mesmo PR → adendo. Branch nova ou PR novo → wiki
nova com `## Natureza da Wiki: evolução` e a ancestral apontada.

Antes de registrar o adendo, leia o template dele em [`references/template-00-requisito.md`](references/template-00-requisito.md#template-do-adendo).

---

## Arquivo 01: Plano de Ação (PRD)

**Path**: `wikis/specs/{branch}/{feature}/01-plano-acao.md`

**Propósito**: PRD completo — deve ser detalhado o suficiente para um agente implementar sem ambiguidade.

**Obrigatório incluir**:
- **Natureza da Wiki**: nova / evolução / correção / ajuste + wiki ancestral — **decide se o quality gate roda regressão**
- **Cobertura do requisito**: tabela `RQ` → passos que o atendem; toda cláusula do `00` precisa aparecer
- Objetivo claro em 1-2 parágrafos
- Contexto e problema que resolve
- Análise dos arquivos/código existente que será tocado
- **Channel de log da feature** (ver seção "Padrão de Log" abaixo)
- **Autorização**: policies, gates, middleware, guards — quais serão criados/modificados
- **Rotas**: endpoints a registrar, middleware aplicado, naming convention
- **Superfície de UI**: telas/componentes que o usuário vê ou opera (Filament, Livewire, Blade, Inertia) — **é esta seção que decide se haverá `05-casos-de-teste-browser.md`**. Se não houver UI, declarar explicitamente "Sem superfície de UI"
- **Variáveis de Ambiente**: `.env` keys necessárias, config publish, defaults
- **Eventos/Listeners/Observers**: se a feature emite ou escuta eventos, hooks de model
- **Jobs/Queues**: queue connection, timeout, retries, backoff — quando aplicável
- **Impacto em Features Existentes**: regression risk, o que pode quebrar
- **Rollback**: como reverter se algo der errado (migration down, feature flag, etc.)
- **Dependências**: composer/npm packages necessários, versões mínimas
- **Riscos**: áreas de incerteza, dependências externas, prazos apertados
- Passos de implementação numerados com:
  - Path exato de cada arquivo a criar/modificar
  - Assinatura de classes, métodos, interfaces
  - Lógica de negócio detalhada
  - **Logs em todas as etapas de execução** — cada passo que executa lógica deve especificar quais logs emitir (ver seção "Padrão de Log" abaixo)
  - Campos de DB com tipos, nullable, índices, constraints
  - Mapeamentos de campos (ex: API → DB)
  - Tratamento de erros esperados
- Skills a invocar em cada passo (lista em [`references/template-01-plano.md`](references/template-01-plano.md#skills-disponíveis-para-referenciar-no-prd))
- Referência ao `04-casos-de-teste.md` (não duplicar cenários aqui)
- Passos de verificação (pint, tests, artisan commands)
- Passos de commit (gitmoji + escopo + mensagem)

> **Integração com Ponytail**: Após a wiki ser aprovada, o Ponytail deve ser a skill de execução ativa durante toda a implementação. Ele garante que cada passo do plano seja executado com o mínimo de código necessário (reutilização → stdlib → feature nativa → uma linha → mínimo que funciona). Após implementar, rodar `/ponytail:ponytail-review` no diff para validar contra over-engineering. Atalhos deliberados devem ser marcados com `ponytail:` comment. Ver o README do repositório para o passo a passo completo da integração.

Antes de escrever o `01`, leia o template em [`references/template-01-plano.md`](references/template-01-plano.md) —
`## Natureza da Wiki` (com a exceção da infra compartilhada, que força regressão), `## Cobertura do
Requisito`, `## Superfície de UI` (com os gates de CT-B e de tela de escrita), `## Modelo de
Execução`, `## Channel de Log da Feature`, `## Filosofia de Implementação` e `## Verificação Final`.

---

## Padrão de Log — `[Classe@Método] mensagem`

Antes de especificar os logs de cada passo do PRD, leia [`references/padrao-de-log.md`](references/padrao-de-log.md):
anatomia da mensagem, contexto estruturado, exemplos,
`Log::shareContext`, driver JSON e teste de log em Pest.

### Por que este padrão

O formato `[Classe@Método] mensagem` é obrigatório em **todos os logs** do projeto. Ele resolve três problemas:

1. **Rastreabilidade**: ao ler um log, sabe-se imediatamente qual classe e método o gerou — sem precisar buscar no código
2. **Filtragem**: permite `grep` por classe ou método para isolar fluxos específicos
3. **Consistência**: padroniza a leitura em qualquer nível (info, warning, error) e em qualquer channel

### Formato Obrigatório

```
[{Classe}@{Método}] {mensagem descritiva} | {parâmetro principal}: {valor} - {contexto adicional}
```

### Regras de Escrita

1. **Prefixo sempre entre colchetes**: `[Classe@Método]` — sem espaços dentro dos colchetes
2. **Mensagem em português**: descrever a **ação executada**, não o estado (use "Membro associado com sucesso" em vez de "Membro foi associado")
3. **Pipe `|` como separador**: entre a mensagem e os parâmetros/contexto
4. **Hífen `-` como separador secundário**: entre múltiplos parâmetros de contexto
5. **Incluir parâmetro principal sempre que possível**: IDs, slugs, status — valores que identificam o registro manipulado
6. **Nível de log apropriado**:
   - `debug` → detalhe intermediário para rastreabilidade
   - `info` → sucesso de operação esperada
   - `notice` → evento significativo mas normal (ex: queue retry agendado)
   - `warning` → condição anormal mas não fatal — **usar em `fail()` de Livewire**, fallback, retry, dado ausente
   - `error` → falha que interrompe o fluxo — **usar em `catch` de exceptions** que quebram a execução
   - `critical` → erro de sistema que exige intervenção imediata (ex: DB inacessível, API crítica fora do ar)
   - `emergency` → sistema indisponível, intervenção humana urgente
7. **Máximo de contexto estruturado**: SEMPRE passar o segundo parâmetro `array $context` do Laravel com todos os dados relevantes — IDs, payloads, snapshots de estado, dados do modelo (ver seção "Contexto Estruturado" em `references/padrao-de-log.md`)
8. **Exceptions no contexto**: ao logar uma exception, incluir `'exception' => $e` no array de contexto — o Laravel serializa automaticamente stack trace, mensagem e código
9. **Nível do log = severidade da ação**: `fail()` → `warning`; `catch` de exception que interrompe → `error`; `catch` de exception tratada/ignorada → `warning`

### Como Implementar no Plano

Para **cada passo de implementação** no PRD, especificar:

1. **Quais métodos terão logs** — listar cada método e os pontos exatos (início, sucesso, falha, decisão de fluxo, catch de exception, fail de validação)
2. **Qual channel usar** — `Log::channel('{feature-name}')` em todos os logs da feature
3. **Qual nível** — debug/info/notice/warning/error/critical conforme a regra de severidade:
   - `fail()` de Livewire → `warning`
   - `catch` de exception que **interrompe** o fluxo → `error`
   - `catch` de exception **tratada/ignorada** → `warning`
   - Sistema/API indisponível → `critical`
4. **Qual mensagem** — já escrever a string completa no plano, seguindo o formato
5. **Qual context** — listar o array de contexto com todos os campos relevantes (IDs, payloads, snapshots, `exception`)

> **Anti-padrão**: NUNCA usar `Log::info('...')` sem channel — sempre especificar o channel da feature.
> **Anti-padrão**: NUNCA usar mensagens genéricas como "Processando..." ou "Erro ocorrido" — sempre incluir `[Classe@Método]` e parâmetro principal.
> **Anti-padrão**: NUNCA logar apenas em `catch` — logar também no sucesso e nos pontos de decisão de fluxo.
> **Anti-padrão**: NUNCA passar context vazio — incluir o máximo de informação estruturada possível (IDs, payloads, snapshots, exception).
> **Anti-padrão**: NUNCA usar `error` para `fail()` de validação — `fail()` é uma condição esperada de interrupção, usar `warning`.
> **Anti-padrão**: NUNCA usar `info` para exceptions — exceptions são anomalias, usar no mínimo `warning` (tratada) ou `error` (interrompe).

### Trait UnicoLogging (se aplicável)

Se o projeto possuir uma trait de logging (ex: `UnicoLogging`), verificar:

- `Grep` por `trait UnicoLogging` ou `trait.*Logging` em `app/`
- Se existir, usar a trait nos classes da feature — ela formata automaticamente o prefixo `[Classe@Método]`
- Se não existir, implementar o formato manualmente via `Log::channel(...)->info('[Classe@metodo] ...')`
- Documentar no plano qual abordagem será usada

---

## Arquivo 02: Decisões Arquiteturais (ADR)

**Path**: `wikis/specs/{branch}/{feature}/02-decisoes-arquiteturais.md`

**Propósito**: Registrar o "porquê" das escolhas — não o "o quê". Usa formato **ADR (Architecture Decision Record)** para padronizar e facilitar consulta futura.

**Incluir**:
- Cada decisão não-óbvia com justificativa
- Alternativas consideradas e por que foram descartadas
- Trade-offs aceitos
- Restrições externas (APIs, limites de parceiros, compliance)
- Padrões reutilizados de outras partes do sistema
- Link entre decisões relacionadas (ex: "Refine ADR-01")
- Decisões overridden (quando uma ADR substitui outra)

Antes de escrever o `02`, leia o template em [`references/template-02-adr.md`](references/template-02-adr.md).

---

## Arquivo 03: Progresso / Tracking

**Path**: `wikis/specs/{branch}/{feature}/03-progresso.md`

**Propósito**: Checklist de implementação para rastrear o que foi feito e retomar de onde parou.

**Estrutura**: Seções com checkboxes `- [ ]` agrupadas pelos mesmos passos do `01-plano-acao.md`.

**Checkbox só fecha com evidência inline.** Formato `- [x] {item} — {evidência}, {data}`; item sem evidência continua `[ ]`. A evidência inline é o que torna o lote impossível — não há o que colar (caso em [`references/casos-medidos.md`](references/casos-medidos.md#arquivo-03--checkbox-com-evidência-inline)). Conferência: `grep -n '^- \[x\]' 03-progresso.md | grep -v ' — '` tem de voltar vazio na Verificação Final.

**Duas seções que só existem para o step 7 e o step 8**: `## Conformidade com Rules` (uma linha por rule cujo glob casa o diff) e `## Quality Gate` (ciclo, veredito, data). Enquanto a segunda estiver vazia, a feature **não** está concluída e o PR não abre.

**Validação de espelho**: verificar que a estrutura de seções do `03-progresso.md` espelha exatamente os passos do `01-plano-acao.md` — se o plano tem 8 passos, o progresso tem 8 seções correspondentes.

Antes de escrever o `03`, leia o template em [`references/template-03-progresso.md`](references/template-03-progresso.md) —
seções por passo do plano, `## Testes`, `## Verificação Final`, `## Conformidade com Rules`,
`## Quality Gate`, `## Auditoria Pré-Implementação`, `## Despachos`, `## Blockers`, `## Desvios do
Plano`, `## Notas de Implementação` e `## Retrospectiva`.

---

## Arquivos 04 e 05: Casos de Teste — delegados à `feature-test-design`

**Paths**: `wikis/specs/{branch}/{feature}/04-casos-de-teste.md` e `05-casos-de-teste-browser.md`

A **derivação e a escrita dos casos de teste não pertencem a esta skill**. Ela delega à skill
`feature-test-design` (`{skills}/feature-test-design/SKILL.md`), invocada no step 4 desta wiki.

Antes de invocar a `feature-test-design`, leia [`references/delegacao-casos-de-teste.md`](references/delegacao-casos-de-teste.md#o-contrato-da-delegação):
por que delegar e o contrato da delegação — entrada em ordem de autoridade, saída e o que é
proibido passar como entrada.

**O `01-plano-acao.md` não é fonte de comportamento esperado.** Se a única forma de saber o que
o sistema deve fazer é ler o PRD, o `00-requisito.md` está incompleto — e isso é achado, não
atalho.

**Ordem**: sempre que possível, o step 6 (Ponytail) roda sobre `01`/`02` **antes** desta invocação;
se o `04` já existir quando um corte mudar a `## Superfície de UI`, ele é re-sincronizado no mesmo
passo (ver step 6). O `04` derivado de uma superfície que depois foi cortada fica com CT órfão.

### Gate do `05` (browser)

A tabela `## Superfície de UI` do PRD continua sendo o gatilho, mas o critério mudou: **o cenário
vai para o browser somente quando afirma sobre algo que só o navegador prova** — JavaScript
executado, console/erro de JS, acessibilidade, cor/tema, layout.

Tudo o mais que parece "de tela" em Filament é **teste de componente Livewire**, roda em
milissegundos, sem Node e sem Playwright, e pertence ao `04`: validação de formulário,
gravação, listagem, busca, filtro, ação de tabela, notificação e autorização na tela.

> **Gate de tela de escrita**: para toda rota `create`/`edit` da `## Superfície de UI`, o `04`
> precisa ter um cenário de **gravação por componente**. *Uma tela aberta não é uma tela que
> grava* — um `GET` fica verde com o salvamento quebrado.

Se nenhum cenário exigir navegador: **não criar o `05`** e registrar no `04` a seção
`## Sem CT-B` com o motivo.

### Execução dos testes — `executor-ct` e CT-B

O teste Pest de backend nasce do Gherkin do `04`, escrito por quem **não implementou** — no Claude
Code, o sub-agente `fw-executor-ct` ([`agents/fw-executor-ct.md`](agents/fw-executor-ct.md)). A
**execução** dos CT-B contra a UI real é desta skill, no step 7, em loop pelo `fw-executor-ctb`
([`agents/fw-executor-ctb.md`](agents/fw-executor-ctb.md)). Antes de escrever teste a partir do
`04` ou do `05` — despachando um dos dois ou, em host sem sub-agente, em linha —, leia
[`references/delegacao-casos-de-teste.md`](references/delegacao-casos-de-teste.md#contrato-do-construtor-de-testes-executor-ct):
os dois contratos — entrada, classificação de todo vermelho em a/b/c antes de qualquer edição,
proibições e saída em formato fixo.

O vermelho tem regra própria em cada contrato.

**Backend (`executor-ct`):**

- **Vermelho é classificado antes de qualquer edição**: (a) teste errado → corrige o teste;
  (b) **implementação divergente da especificação → não corrige**, deixa vermelho e registra com
  a saída literal; (c) flake → anota. Máximo 3 iterações por arquivo. **Vermelho por (b) é
  resultado válido** e é o que a sessão roteia (Adendo → CT → correção)

**CT-B (`executor-ctb`, loop do step 7):**

**Teste vermelho por causa (b) é resultado válido, não falha do ciclo** — é exatamente a
divergência entre desenhado e implementado que se queria capturar. Sub-agente que "conserta" a
aplicação para ficar verde destrói o instrumento de medição. Após 3 iterações com vermelho,
parar e registrar como blocker no `03-progresso.md`.

### Fatos do `pest-plugin-browser`

Não há cópia nesta skill além dos dois fatos que o step 3 confere (servidor próprio, `npm run build`).
Antes de escrever, rodar ou revisar qualquer CT-B, leia
`{skills}/feature-test-design/references/pest-plugin-browser.md` — a fonte única dos fatos do plugin.

**Assertion de console ou de status nunca é o oráculo único de um CT-B.** Todo cenário precisa de
pelo menos uma assertion sobre o que ele afirma — o elemento, o valor ou o registro.

### Playwright MCP na validação (OPCIONAL — ferramenta de observação)

> **O `pest-plugin-browser` atesta. O Playwright MCP observa.**
>
> O CT-B é sempre um teste Pest versionado. O MCP nunca produz cobertura, nunca entra no `05`
> como evidência e nunca substitui um CT-B — ele existe para o agente **ver** a página quando o
> teste falha.

No step 3, no loop do CT-B e no step 7 — com ou sem o MCP disponível —, leia
[`references/playwright-mcp.md`](references/playwright-mcp.md): por que o MCP e não as ferramentas
de debug do plugin, onde ele entra, a configuração e o fallback sem ele. As regras duras ficam
aqui:

- **`--isolated` é obrigatório.** O default do MCP é perfil persistente: o login sobrevive entre
  sessões e, com uma URL errada, o agente pode clicar em produção autenticado.
- **Somente `localhost`.** Apontar para staging ou produção é proibido pela skill.

**Regras de uso**:

1. **Ref nunca entra em teste.** `ref=e5` é válido "until the next page change". Só o resultado
   de `browser_generate_locator` vai para o CT-B.
2. **`browser_find` antes de `browser_snapshot` cru** — snapshot em loop acumula contexto.
3. **Proibido `browser_run_code_unsafe`.** Se o cenário exige, ele exige um CT-B.
4. **Proibido `--caps=vision`.** Clique por coordenada XY destrói o determinismo.
5. **Sessão MCP não é cobertura.** Nada de "validado via MCP" sem CT-B correspondente.
6. **Na causa (b), o MCP é só leitura** — serve para descrever a divergência, nunca para contorná-la.
7. **Feature com dado sensível** (PII, pagamento): sem `browser_take_screenshot` versionado.

---

## Execução de Testes com Pest 5

Detectar a versão do Pest no step 3. Se o projeto está em **Pest 5** (requer **PHP 8.4+** e PHPUnit 13), usar os recursos abaixo; em Pest 4, cair para `vendor/bin/pest --filter`.

Com Pest 5 detectado, antes de implementar o primeiro passo do PRD — e antes de instalar ou
atualizar o Pest, ou de rodar a suíte com `--tia`, `--agent` ou `--mutate` —, leia
[`references/pest-5.md`](references/pest-5.md): instalação, TIA (onde encaixa em cada passo e o
watch dos CT-B), agent plugin, o lançador `.cmd` do Windows e os demais recursos. As regras duras
ficam aqui:

- **`--testsuite=A --testsuite=B` só honra o último.** Uma suíte por comando, as duas saídas coladas
- **`pest --mutate` dá 100 % falso no Windows.** Regra: **score só vale com `Duration` compatível com N × tempo dos testes cobridores e com a lista de sobreviventes.** No Windows, lançar pelo `.cmd` poliglota de [`references/pest-5.md`](references/pest-5.md#pest---mutate-no-windows--o-lançador-cmd)

**Forma canônica: `--parallel --tia`.** O `--parallel` **não** é pré-requisito técnico do `--tia` (o `--tia` funciona sozinho), mas é a invocação que a doc oficial usa, e os dois são complementares: o TIA corta **quanto** roda, o parallel corta **quanto tempo** o que sobrou leva. Usar sempre juntos como padrão da skill.

**Cuidado com `--parallel` + CT-B**: browser em paralelo multiplica processos de navegador e exige DB por worker. Nunca `--parallel` no comando de browser (fatos do plugin em `{skills}/feature-test-design/references/pest-plugin-browser.md`): rodar os CT-B em série (`vendor/bin/pest tests/Browser`) e deixar o `--parallel --tia` para o suite de backend.

> ⚠️ **Nunca usar `--tia` no comando que roda o suite em CI.** A doc do Pest é explícita: o pipeline deve rodar o suite completo. O TIA em CI existe só num job dedicado de baseline (`--tia --coverage --fresh`, artefato `pest-tia-baseline`).

Sobre o `--agent` (agent plugin):
**Onde encaixa**: durante a implementação de um passo do PRD, para confirmar uma premissa antes de escrever o teste definitivo. **Não substitui** os CTs do `04`/`05` — o `--agent` é efêmero e não fica versionado. Uma verificação via `--agent` que se mostre valiosa deve virar CT no arquivo correspondente.

---

## Citações de código — `arquivo:símbolo:linha`

Antes de escrever ou reverificar uma citação (steps 3, 5 e 7), leia [`references/citacoes-de-codigo.md`](references/citacoes-de-codigo.md):
as duas classes de erro medidas, exemplos do formato e o comando de conferência.

**Formato obrigatório**: `{path relativo à raiz do projeto}:{símbolo}():{linha}` ou, para
intervalo, `:{inicial}-{final}`. O símbolo é o método, função, constante ou chave de array que a
linha (ou a primeira linha do intervalo) contém — é ele que sobrevive ao deslocamento e que
permite conferir sem abrir o arquivo.

Path curto (`Login.php:172`) é aceito só depois de o path completo ter aparecido no mesmo
documento. Citação sem símbolo não passa no step 5 nem no step 7.

**Conferência mecânica** — rodar na raiz do projeto; toda linha `ERRO` é uma citação a corrigir
na fonte, nunca a apagar para "passar":
o comando está em [`references/citacoes-de-codigo.md`](references/citacoes-de-codigo.md#conferência-mecânica).

Registrar o resultado na Verificação Final do `03` (`— 14/14 ok, {data}`). A dimensão L da
`feature-quality-gate` roda o mesmo comando e compara.

---

## Checklist Final da Skill

Antes de encerrar a invocação:

### Requisito
- [ ] `00-requisito.md` criado com Fonte, Texto Original **verbatim** e Fidelidade declarada
- [ ] Requisito decomposto em cláusulas `RQ-##`, cada uma citando o trecho literal de origem
- [ ] Ambiguidades e perguntas abertas listadas — e perguntadas ao usuário antes de implementar
- [ ] Fora de escopo declarado (evita o quality gate acusar omissão indevida)
- [ ] Perguntas obrigatórias do `00` feitas: acumulação de papéis **par a par**, participante histórico × recorte de visibilidade, destino do link de toda notificação, teto de todo texto livre
- [ ] `## Natureza da Wiki` preenchida no PRD (+ wiki ancestral se não for "nova")
- [ ] `## Cobertura do Requisito` no PRD mapeia **toda** cláusula `RQ` a passo(s) ou justificativa

### Planejamento
- [ ] Branch lida e estrutura de pasta criada
- [ ] Wiki existente verificada (retomar/sobrescrever/incrementar se já existe)
- [ ] Nome da feature confirmado com usuário
- [ ] Pesquisa feita (`search-docs`, `database-schema`, leitura de arquivos)
- [ ] `search-docs` consultado para **cada stack** que o PRD toca (Laravel, Filament, Livewire, Inertia, Pest, Tailwind) e origem citada no plano
- [ ] Lacunas do `search-docs` cobertas por doc oficial: Pest 5, Playwright/`pest-plugin-browser`, pacotes de terceiros
- [ ] Rotas, policies, config, composer, wikis existentes verificados
- [ ] APIs de terceiros inspecionadas (vendor source ou docs) — métodos e schema confirmados
- [ ] Tabela `## Superfície Livewire` no `02` preenchida — **sempre** que a feature cria página, widget ou componente: métodos públicos, propriedades públicas sem `#[Locked]` e os arrays de estado do framework que o código consome. Pacote de terceiro acrescenta os quatro greps do vendor, com um model por linha
- [ ] Dados fornecidos pelo usuário validados contra o DB (quando aplicável)
- [ ] Factories confirmadas (existência + states) para todos os CTs
- [ ] Stack de testes verificado: versão do Pest, `pest-plugin-browser`, Playwright, traits em `tests/Pest.php`
- [ ] **Baseline** da suíte completa em `{base}` registrada antes do primeiro commit, falhas pré-existentes por nome
- [ ] Model novo cujo nome de tabela não é o plural inglês inferido declara `$table`

### Documentação
- [ ] `01-plano-acao.md` escrito com passos numerados + skills referenciadas + logs em todas as etapas
- [ ] `01-plano-acao.md` inclui seções: Autorização, Rotas, Variáveis de Ambiente, Eventos, Jobs, Impacto, Rollback, Dependências, Riscos
- [ ] `02-decisoes-arquiteturais.md` escrito em formato ADR (Status, Contexto, Decisão, Alternativas, Consequências)
- [ ] `03-progresso.md` escrito com checkboxes espelhando o plano + seções Blockers, Desvios, Notas, Retrospectiva
- [ ] **`feature-test-design` invocada** (step 4) com o `00-requisito.md` como entrada primária — o `04` **não** foi escrito inline a partir do PRD
- [ ] `04-casos-de-teste.md` recebido com: perfil de risco, varredura SFDIPOT, mapa de regras, técnica nomeada por regra e **mutantes previstos com o cenário que mata cada um**
- [ ] Toda rota `create`/`edit` da `## Superfície de UI` tem cenário de **gravação por componente** no `04`
- [ ] Perguntas devolvidas pela `feature-test-design` incorporadas em `## Ambiguidades` do `00-requisito.md`
- [ ] `01-plano-acao.md` tem a seção `## Superfície de UI` preenchida (ou "Sem superfície de UI" declarado)
- [ ] Gate de CT-B avaliado → `05-casos-de-teste-browser.md` criado **ou** motivo da ausência registrado no `04`
- [ ] Se houver CT-B: dependências (`pest-plugin-browser`, Playwright) confirmadas ou incluídas como passo no PRD
- [ ] Arquivos extras (`05-*`) criados se necessário (rollback, performance, security)

### Log
- [ ] Channel de log da feature verificado/criado e referenciado em todos os passos do PRD
- [ ] Padrão de log `[Classe@Método] mensagem` especificado em cada passo de execução do PRD
- [ ] Context estruturado (array `$context`) especificado em cada log do PRD
- [ ] Log **não** vira CT no `04` (log não é cláusula do requisito) — quem o confere é a dimensão D do quality gate; exceção: requisito que pede trilha de auditoria, e aí é `RQ`

### Validação
- [ ] Revisão profunda pós-escrita executada — premissas do plano re-validadas contra o código
- [ ] **Varredura da classe irmã** executada para toda classe nova, com a irmã escolhida e as ocorrências registradas no `03`
- [ ] `## Modelo de Execução` preenchido no PRD (ou "um request, sem trabalho adiado" declarado)
- [ ] **Auditoria da wiki executada** — `/ponytail:ponytail-review` invocado e sugestões aplicadas
- [ ] Step 6 rodou sobre `01`/`02` **antes** da derivação do `04` — ou o `04` foi re-sincronizado após os cortes (CT órfão declarado `@obsoleto`)
- [ ] `03-progresso.md` espelha exatamente os passos do `01-plano-acao.md`
- [ ] Filosofia de Implementação (Ponytail) incluída no PRD
- [ ] Confirmar com usuário se o plano está correto antes de implementar

### Pós-Implementação e Reconciliação (antes do PR)
- [ ] Todo `[x]` do `03-progresso.md` tem evidência inline (`— {resultado}, {data}`); nenhum fechado em lote
- [ ] Cada desvio do `03` tem a edição correspondente no `01`/`02`/`04`/`05` de origem, marcada `*(alterado em …)*` — nenhuma afirmação do `01`/`02` contradiz o código
- [ ] Toda citação `arquivo:símbolo:linha` da wiki reverificada pelo grep — resultado no `03`
- [ ] IDs `[CT-nn]`/`[CT-Bnn]` do teste ⊆ `04`/`05` e vice-versa — **saída do `diff` colada na Verificação Final, vazia**
- [ ] **Revisão de código do diff executada** (step 6.5) **antes** da reconciliação, por quem não implementou; cada achado confirmado virou Adendo no `00` + CT no `04` + correção, nessa ordem
- [ ] No Claude Code: `/code-review` rodou com alvo explícito (`{base}...HEAD`), nível `high`, sem `--fix` — e o passe de eixos rodou em sub-agente cego ao `01`/`03`
- [ ] Falsificabilidade dos CTs novos provada por `git stash` — cada um falha sem a correção **ou** está declarado "não falsificável nesta pilha", com o motivo
- [ ] `## Superfície Livewire` do `02` re-varrida sobre o código final **antes** do 6.5
- [ ] Todo número da `## Verificação Final` tem o comando que o gerou; toda degradação declarada tem a prova negativa (`php -m`, `ls vendor/…`)
- [ ] `pest --mutate` com duração plausível e sobreviventes listados (no Windows, via lançador `.cmd`)
- [ ] Contagens da wiki inteira (`01`, `02`, `03`, `04`: nº de CTs, regras, mutantes, permissions, linhas de varredura) derivadas por `grep -c`, nunca digitadas — número digitado envelhece no primeiro adendo
- [ ] Todo número **corrigido** durante o ciclo foi procurado na wiki inteira (`grep -rn "{valor antigo}"`) — a cópia em outro arquivo é o que sobrevive ao gate
- [ ] Requisito que cresceu virou `## Adendo N` no `00`, com `RQ` novos, e a `feature-test-design` foi reinvocada para ele **antes** do código
- [ ] Tabela `## Conformidade com Rules` do `03` preenchida para toda rule cujo glob casa o diff — nenhuma `violada`
- [ ] Docs de usuário (pt **e** en), CHANGELOG e README reconciliados; nenhuma frase neles sem `RQ` ou ADR de origem
- [ ] Roteiro "Desenhado × Implementado" do `05-*-browser.md` preenchido, com divergências replicadas em "Desvios do Plano" e na fonte
- [ ] Notas de implementação e retrospectiva breve escritas
- [ ] CT-B escritos e rodados via sub-agente; divergências classificadas (CT errado / implementação divergente / flake)
- [ ] Se o Playwright MCP foi usado: só como observação (`--isolated --headless --caps=testing`), nenhum ref em arquivo de teste, nenhuma sessão MCP registrada como cobertura

### Delegação (Claude Code)
- [ ] Todo disparo de sub-agente está em `## Despachos` do `03`, com modelo, cegueira e auditoria do retorno; tarefa em linha por exceção tem "Sem despacho — motivo"
- [ ] Nenhum `general-purpose` despachado sem `model` explícito
- [ ] Passe de eixos do 6.5, revisão adversarial e step 8 rodaram em sub-agente **cego** — ou a degradação está declarada no `03` e no cabeçalho do `06`
- [ ] Todo retorno auditado: presença, integridade (`git diff --stat` antes/depois do lote) e amostragem
- [ ] `ls .claude/agents/fw-*.md` conferido antes do primeiro despacho; fallback `general-purpose`/{model} registrado no quadro quando o agente faltou
- [ ] Rota `mecânico` só com **um item por despacho**; lote misto foi para `construtor`
- [ ] Retorno com número sem comando, `git diff --stat` de untracked ou "não encontrado" sem prova negativa foi **reprovado e refeito** — e a reprovação está no quadro

### Quality Gate e PR
- [ ] **`feature-quality-gate` invocado** (step 8) — no Claude Code, via `fw-qa-gate` sem Edit/Write, `06` gravado verbatim pela sessão — e ciclo/veredito/data registrados na seção `## Quality Gate` do `03-progresso.md`
- [ ] `06-relatorio-qa.md` **existe** no diretório da wiki (`ls wikis/specs/{branch}/{feature}/06-relatorio-qa.md`) — a ausência dele é blocker do PR, e é a evidência de que o step 8 rodou
- [ ] Se `REPROVADO`: achado roteado para o destino correto (especificação / implementação / teste) e reciclado
- [ ] **Só depois do veredito**: PR aberto com link da wiki e veredito do `06` na descrição; `03` marcado "concluída"
- [ ] Candidatos a rule avaliados nos 4 gates e **apresentados ao usuário** — gravados via `requirement-to-rule` só se aprovados

### Referências
- [ ] Referências abertas declaradas no relatório final da invocação — uma linha *"referências lidas: {arquivo} (step N), …"*, com cada arquivo de `references/` aberto e o step em que foi aberto
  - A linha cobre o mínimo da tabela do Índice ou diz por que pulou: todo despacho → `roteamento-e-despacho`; step 3 → `pesquisa-step-3`; step 4 → `template-00-requisito` a `template-03-progresso`, `padrao-de-log`, `delegacao-casos-de-teste`, `estrutura-criada`; pré-6.5 → `pesquisa-step-3`; step 7 → `citacoes-de-codigo`; teste escrito a partir do `04`/`05` → `delegacao-casos-de-teste`; step 9 → `candidatos-a-rule`

### Após o merge
- [ ] Channel de log ajustado (level reduzido ou removido)

## Skills Companheiras

A feature-wiki é a primeira estação de uma esteira de skills que cobrem o ciclo completo:

| Camada | Skill | Responsabilidade | Boundary |
|--------|-------|------------------|----------|
| **Comunicação** (agent ↔ usuário) | [Caveman](https://github.com/JuliusBrussee/caveman) — modo padrão `ultra` | Prosa terse — corta ~75% dos tokens removendo fluff, artigos, fillers | **NÃO aplica em arquivos wiki** (00-06), código, commits, PRs |
| **Planejamento** (estrutura de documentação) | feature-wiki | requisito + PRD + ADR + tracking + padrão de log | não deriva caso de teste — testar o próprio plano confirma o plano |
| **Especificação de teste** | `feature-test-design` | deriva o `04`/`05` do **`00-requisito.md`**, com técnica formal e gate de mutantes | não escreve código nem corrige implementação |
| **Execução** (código) | [Ponytail](https://github.com/DietrichGebert/ponytail) | Mínimo código que funciona — escada de simplicidade | Não corta validação, segurança, tratamento de erros |
| **Qualidade** (QA no agente) | `feature-quality-gate` | Confronta `00-requisito` × PRD × app rodando; audita a consistência wiki × código × docs × rules (dimensão L); roteia achado para especificação / implementação / teste. Roda **antes do PR** | Não corrige nada — só lê, reproduz e reporta |
| **Memória de projeto** (rules) | `requirement-to-rule` | Decisão da wiki vira Project Rule do Boost em `.ai/rules/` | Só o que é específico da aplicação; ecossistema é guideline do Boost |
| **Orquestração** (Claude Code) | sub-agentes por rota — pasta `agents/` de cada skill, instalados com `cp .ai/skills/*/agents/*.md .claude/agents/` | Modelo por complexidade, contexto por cegueira; quadro de despacho no `03` | A sessão nunca delega captura verbatim do requisito, perguntas ao usuário nem veredito final |

No início da sessão de planejamento, leia [`references/ponytail-caveman.md`](references/ponytail-caveman.md):
ativação do Caveman em `ultra`, fronteira dele com os arquivos wiki, onde ele é bem-vindo e como
ativar o trio.

> **Comando correto**: `/caveman:caveman {modo}` (com namespace `caveman:`, igual ao `/ponytail:ponytail`). NUNCA usar `/caveman` sem o namespace — o comando não será encontrado.
> Modos disponíveis: `lite` | `full` | `ultra` | `off`.
