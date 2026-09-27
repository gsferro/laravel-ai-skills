# feature-quality-gate — QA no Agente

> **Status: implementada — [`SKILL.md`](SKILL.md) v1.6.0.**
> Requer `feature-wiki` ≥ **3.5.0** e `feature-test-design` ≥ **1.15.0** — o porquê de cada versão mínima, e o que degrada sem cada item, está em [Dependências](#dependências).
>
> **`SKILL.md` fala com o agente; este README fala com a pessoa**: por que a skill existe, quando usar, o que ela não faz e do que depende. Procedimento, dimensões, roteamento, convergência e o template do `06` estão só no [`SKILL.md`](SKILL.md) — aqui eles são explicados e apontados, não copiados.
>
> A segunda metade é o registro da pesquisa que precedeu a implementação (2026-08-14): qual problema ela resolve, o que já existe no mercado (incluindo alternativas MIT), qual lacuna sobra, e por que essa lacuna justificou uma skill nova em vez de instalar o que estava pronto.
>
> **Validado em campo (1.5.0, 2026-09-21).** Primeira execução como sub-agente cego (`fw-qa-gate`,
> `opus`, sem Edit/Write) numa feature completa: `REPROVADO → especificação`, 8 achados — duas
> perguntas de requisito que ninguém tinha feito e **dois achados contra o próprio orquestrador**
> (número da Verificação Final sem comando que o reproduza; degradação declarada com a ferramenta
> presente). A checagem **L6** e a regra de plausibilidade do `--mutate` na dimensão K nasceram daí.
>
> **Medição.** A skill ainda não tem rodada própria no protocolo de [`experimentos/`](https://github.com/gsferro/laravel-ai-skills/blob/main/experimentos/README.md), que mede a derivação dos casos de teste. A execução acima é uso real, não rodada controlada. A fonte das tabelas de medição da coletânea é [`experimentos/README.md`](https://github.com/gsferro/laravel-ai-skills/blob/main/experimentos/README.md).

---

## Índice

**Uso**
- [Quando usar](#quando-usar)
- [O que ela entrega](#o-que-ela-entrega)
- [Limites](#limites)
- [Dependências](#dependências)

**Motivação e estudo**
- [TL;DR do veredito](#tldr-do-veredito)
- [O problema: onde a coletânea para](#o-problema-onde-a-coletânea-para)
- [Estudo de mercado](#estudo-de-mercado-o-que-já-existe)
- [A lacuna verificada](#a-lacuna-verificada)
- [A objeção que quase matou a skill](#a-objeção-que-quase-matou-a-skill)
- [Ganho real 1: omissão silenciosa](#ganho-real-1--omissão-silenciosa-e-a-matriz-de-rastreabilidade)
- [Ganho real 2: as 12 dimensões](#ganho-real-2--as-12-dimensões-que-as-camadas-atuais-não-cobrem)
- [Ganho real 3: roteamento](#ganho-real-3--roteamento-de-achados)
- [Achado técnico: dark mode inverte a regra](#achado-técnico-dark-mode-inverte-a-regra-de-visão--estrutura)
- [Achado técnico: MCP como confronto](#achado-técnico-playwright-mcp-como-confronto-do-ct-b)
- [Regressão condicional](#regressão-condicional-por-natureza-da-wiki)
- [Construir × reusar](#construir--reusar)
- [Convergência e separação de poderes](#convergência-e-separação-de-poderes)
- [Riscos honestos](#riscos-honestos)
- [Critério eliminatório](#critério-eliminatório)
- [Fontes](#fontes)

---

## Quando usar

A skill é a **próxima estação da esteira** — roda no step 8 da [`feature-wiki`](../feature-wiki/README.md), depois de implementar e com os testes verdes, **antes de abrir o PR**. Dentro da esteira a `feature-wiki` a invoca sozinha. Fora dela, peça para "validar a feature", "revisar como QA" ou "conferir se atende ao requisito" — inclusive numa feature entregue há tempo.

Não é hora de usá-la com teste vermelho (primeiro fazer passar), num refactor puro já coberto por CT verde, nem antes de implementar (revisão de plano é o step 6). A lista completa está em [Quando Invocar](SKILL.md#quando-invocar).

O defeito que ela existe para pegar é a **omissão silenciosa**: cláusula do requisito que nunca virou passo do plano, nunca virou teste, nunca virou código. Tudo verde, feature incompleta — ver [Ganho real 1](#ganho-real-1--omissão-silenciosa-e-a-matriz-de-rastreabilidade).

## O que ela entrega

`06-relatorio-qa.md` na wiki, com veredito (`APROVADO` / `APROVADO COM DÉBITO` / `REPROVADO → destino`), achados com repro mínima e evidência, a Matriz de Rastreabilidade (**impressa só se houver lacuna**, para não virar métrica de vaidade) e uma seção **"Não Verificado"** declarando o alcance real da execução.

Cada achado sai com um destino — especificação, implementação, teste, infra ou não-defeito —, e a feature volta para a estação onde o defeito nasceu. O cabeçalho do `06` diz quem julgou: um sub-agente que não viu a conversa, ou a mesma sessão que escreveu a wiki.

## Limites

- **Não corrige nada.** Lê, reproduz e reporta. Quem corrige é a estação do destino, na volta do loop: a escrita da wiki (especificação; step 4 da `feature-wiki`), a execução do passo do PRD (implementação), a `feature-test-design` (teste). O texto defasado que a dimensão L acha é corrigido no step 7 da `feature-wiki`.
- **Não substitui teste.** Encontra a lacuna; quem prova é o CT/CT-B versionado.
- **Depende do `00-requisito.md`.** Sem ele, roda em modo degradado e declara que a omissão silenciosa não foi verificada — é o [critério eliminatório](#critério-eliminatório) do estudo.
- **Mutation score não enxerga omissão.** Só muta código que existe: score alto não prova que o requisito foi entregue.
- **Profundidade proporcional ao risco.** Feature de ajuste, sem UI e de domínio comum roda 5 dimensões, não 12. O que fica de fora é declarado no relatório, não verificado.
- **Sem app servido, sem MCP ou sem driver de cobertura**, as dimensões que dependem deles ficam estáticas ou vão para "Não Verificado" — ver [Dependências](#dependências).
- **Só no Claude Code, com o sub-agente instalado, parte da independência é construção**: o `fw-qa-gate` não tem Edit/Write e não recebe a conversa. `Bash` e a leitura do `03` seguem por instrução (último item abaixo). Em outro host, quem julga é quem escreveu, e o `06` diz isso.

Limites conhecidos, abertos no [roteiro do estudo de 2026-09-26](https://github.com/gsferro/laravel-ai-skills/blob/main/estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md) (§7.4; itens 8 e 9 do §8):

- parte das dimensões é julgamento, não checagem mecânica — inclusive a A;
- os perfis mínimo e padrão pulam dimensões e ainda podem emitir `APROVADO`;
- a dimensão I sobrepõe a revisão do diff do step 6.5 da `feature-wiki` e o `/code-review`;
- o sub-agente tem `Bash`, então "não altera a árvore" é instrução, não restrição de ferramenta; e ele lê o `03`, que guarda resíduo da conversa (`## Despachos`, `## Desvios`).

## Dependências

| Item | Versão mínima | Para quê | Sem ele |
|---|---|---|---|
| `feature-wiki` | **3.5.0** | produz as entradas (`00`–`03`) e despacha esta skill no step 8 | sem `01`, a skill não roda; sem `00`, [oráculo degradado](SKILL.md#oráculo-degradado) |
| `feature-test-design` | **1.15.0** | produz o `04`/`05` auditados e recebe todo achado de destino 3; a 1.15.0 é a que traz a referência do `pest-plugin-browser` que a seção de [dark mode](#achado-técnico-dark-mode-inverte-a-regra-de-visão--estrutura) deste README aponta | sem `04`, a skill não roda |
| Projeto Laravel com Pest | Pest 4 | rodar CT e CT-B existentes | — |
| App servido na `APP_URL` | — | dimensões dinâmicas | B, C, D, E, F, G, H e I ficam estáticas |
| Pest 5 | 5 | `--parallel --tia` para regressão por impacto medido | regressão sem impacto medido, declarada em "Não Verificado" |
| PCOV ou Xdebug | — | cobertura para o `--tia` e o `--mutate` | a dimensão K roda só o passo estático; a medição vai para "Não Verificado", depois de provar a ausência |
| `pest-plugin-agent` (`--agent`) | Pest 5 | sondagem efêmera durante a validação | leitura estática do código; o que não foi sondado é declarado |
| `pest-plugin-browser` | — | rodar e criar CT-B | dimensões G e H limitadas |
| Playwright MCP | — | inventário de elementos, tema/cor, console/rede | `screenshot()`, `content()` filtrado e leitura do Blade; o resto vai para "Não Verificado" |
| Boost MCP (`browser-logs`, `database-query`, `database-schema`, `search-docs`) | — | evidência de console e conferência de dados | o que dependia deles é declarado |
| Project Rules do Laravel Boost (`.ai/rules/index.md` e as rules) | `laravel/boost` 2.4.12 | L4: rules cujo glob casa o diff × tabela do `03` × código | L4 não roda — declarada em "Não Verificado" |
| Skills do [`qa-skills`](https://github.com/petrkindlmann/qa-skills) (MIT) | — | técnica de QA delegada (SBTM, triagem, repro) | fallback inline de cada uma, registrado no relatório — ver [Delegação](SKILL.md#delegação-a-skills-externas) |
| Claude Code com sub-agentes | — | a skill roda como `fw-qa-gate` (`opus`, **sem Edit/Write**), sem receber a conversa que escreveu a wiki; `Bash` e a leitura do `03` seguem por instrução (ver [Limites](#limites)) | roda em linha, e o `06` declara a independência degradada |

**Por que `feature-wiki` ≥ 3.5.0.** O `00-requisito.md`, oráculo desta skill, existe desde a 2.10.0. A `## Superfície Livewire` do `02`, que a dimensão I confere, desde a 3.3.0. A `## Despachos` do `03`, que a L6 confere junto com a `## Verificação Final`, desde a 3.4.0 — publicada só junto com a 3.5.0. E o lançador `.cmd` que a dimensão K manda usar no Windows está na seção *Pest 5* da `feature-wiki` desde a 3.5.0. Com uma versão anterior essas peças faltam: sem a `## Superfície Livewire`, a dimensão I roda os greps da `feature-wiki` (tabela de [Entradas](SKILL.md#entradas-e-gate-de-entrada)); sem a `## Despachos`, a L6 confere só a `## Verificação Final`; sem o lançador, o score do `--mutate` no Windows não passa na regra de plausibilidade da dimensão K e vai para "Não Verificado".

### Instalação do sub-agente (Claude Code)

A definição do agente vem nesta skill, em [`agents/fw-qa-gate.md`](agents/fw-qa-gate.md), para o
`boost:add-skill` instalá-la junto. **O Claude Code só lê `.claude/agents/`**, então depois de
instalar ou atualizar as skills copie os agentes de toda a esteira — uma vez, e de novo a cada
atualização:

```bash
mkdir -p .claude/agents
cp .ai/skills/*/agents/*.md .claude/agents/
```

No PowerShell:

```powershell
New-Item -ItemType Directory -Force .claude\agents | Out-Null
Copy-Item -Force .ai\skills\*\agents\*.md .claude\agents\
Get-ChildItem .claude\agents\fw-*.md        # cinco arquivos
```

Espelhar as skills em `.claude/skills/` só é preciso sem `boost.json`: com ele, o `boost:update` cria
cada `.claude/skills/<skill>` como symlink, e copiar por cima falha. Os dois casos estão em
[Como Instalar no Claude Code](https://github.com/gsferro/laravel-ai-skills/blob/main/README.md#-como-instalar-no-claude-code),
no README da coletânea.

Sem a cópia, a `feature-wiki` não encontra `fw-qa-gate` e despacha um `general-purpose` com
`model: opus` — funciona, mas com Edit/Write disponíveis: o "não corrige nada" passa a ser só instrução, também para a edição de arquivo.

---

# Motivação e Estudo de Viabilidade

## TL;DR do veredito

**Vale a pena — mas não pelo motivo óbvio.**

Técnica de QA é **commodity**: existem 50 skills MIT prontas cobrindo SBTM, risk-based testing, triagem de bug, repro mínima, exploratório e automação. Reescrever isso seria desperdício.

O que **não existe em nenhuma delas** é a camada de **controle de loop**: decidir se um achado volta para a *especificação*, para a *implementação* ou para o *teste*, e parar quando convergir. Foi verificado, não presumido.

E existe uma classe de defeito que **nenhuma** das três camadas de revisão atuais da coletânea consegue detectar: a **omissão silenciosa** — cláusula do requisito que nunca virou passo do plano, nunca virou teste, nunca virou código. Tudo verde, feature incompleta.

A skill se justifica por essas duas coisas. Todo o resto ela deve **delegar**.

---

## O problema: onde a coletânea para

Numa esteira de desenvolvimento — **requisitos → desenvolvimento → QA → deploy** — a coletânea hoje cobre as duas primeiras etapas:

| Etapa | Cobertura atual |
|---|---|
| Requisitos | `feature-wiki` — PRD, ADR |
| Desenvolvimento | `feature-wiki` + Ponytail — passos, CT, CT-B, log |
| **QA** | **descoberto** |
| Deploy | descoberto |

A `feature-wiki` já tem **três camadas de revisão**, e é importante reconhecer isso antes de propor uma quarta:

1. **Step 5** — revisão profunda pós-escrita: re-valida cada premissa do plano contra o código real
2. **Step 6** — `/ponytail:ponytail-review` audita o plano contra over-engineering
3. **Loop de CT-B** — sub-agente escreve, roda e classifica falha em (a) CT errado / (b) implementação divergente / (c) flake, preenchendo a tabela *Desenhado × Implementado*

Uma quarta camada só se justifica se cobrir algo que essas três são **estruturalmente incapazes** de ver. Esse foi o critério do estudo.

E há um limite comum às três: **todas tomam o PRD como verdade.** O step 5 valida o plano contra o código; o step 6 corta excesso do plano; o loop de CT-B compara PRD × tela. Nenhuma pergunta se o **PRD reflete o requisito**.

---

## Estudo de mercado: o que já existe

Pesquisa feita antes de qualquer linha de desenho (pesquisa feita em 2026-08-14).

| Fonte | O que é | Licença |
|---|---|---|
| [`petrkindlmann/qa-skills`](https://github.com/petrkindlmann/qa-skills) | **50 skills de QA** no Agent Skills Standard, drop-in no Claude Code / Codex / Cursor | **MIT** |
| [QASkills.sh](https://qaskills.sh/agents/claude-code) | diretório com 40+ skills de teste (Playwright, Cypress, k6, axe) | vários |
| [awesomeskill.ai — Testing & QA](https://awesomeskill.ai/category/testing-qa) | categoria inteira de skills de QA | vários |
| [QA Engineer Agent](https://mcpmarket.com/tools/skills/qa-engineer-agent-1) | "test planning, bug reporting, regression analysis" | — |
| [Playwright Test Agents](https://playwright.dev/docs/test-agents) | planner → generator → **healer** | MIT |
| Laravel Boost — skills | `pest-testing`, `infer-conventions`, `livewire-development`… — **nenhuma de QA** | MIT |

O `qa-skills` cobre praticamente todo o vocabulário técnico de um QA sênior:

| Categoria | Skills relevantes |
|---|---|
| Estratégia | `test-strategy`, `test-planning`, **`risk-based-testing`**, **`exploratory-testing`** (SBTM, charters, heurísticas) |
| Processo | `shift-left-testing`, **`release-readiness`** (go/no-go), `quality-postmortem`, `compliance-testing`, `test-case-management`, **`test-suite-curation`** |
| IA-aumentado | `ai-test-generation` (gera casos a partir de PRD), **`ai-bug-triage`** (severidade/componente/root cause + dedupe), **`test-reliability`** (flake), **`ai-qa-review`**, **`bug-reproduction`**, `agentic-browser-testing` |
| Automação | Playwright, Cypress, API, unit, mobile, visual, performance, recuperação de seletor |

**Conclusão parcial: se a skill nova fosse "como um QA sênior pensa", ela seria uma reescrita pior de 50 skills MIT.**

E o `healer` do Playwright merece nota: ele **repara o teste até passar**. Numa esteira de auditoria isso é o oposto do desejado — é exatamente o comportamento que o contrato do sub-agente de CT-B já proíbe ("alterar código para o teste passar destrói o instrumento de medição").

---

## A lacuna verificada

Todas as opções acima produzem **mais teste** ou **mais relatório**. Nenhuma fecha o ciclo. Um post do blog do QASkills.sh (ver [Fontes](#fontes)) é explícito ao descrever o estado da arte:

> "The article describes these as complementary layers of a testing pyramid rather than a **gated feedback loop**. **No skill routes findings back to specifications or implementation gates.**"

Ou seja: nenhuma decide *"este achado volta para a especificação"* × *"este volta para a implementação"* × *"este não é defeito"*. A decisão de roteamento continua sendo humana, informal e não registrada.

**O ganho real da skill não é QA. É roteamento e convergência — um *loop controller*.**

---

## A objeção que quase matou a skill

Vale registrar o argumento contra, porque ele define o desenho.

**Cegueira correlacionada.** Hoje o mesmo agente lê o requisito → escreve o PRD → escreve os CT → implementa → roda os CT. Se ele **entendeu o requisito errado**, erra coerentemente quatro vezes. Tudo verde. Nada detectado.

Um sub-agente de QA que leia **a wiki** não resolve: ele herda a mesma premissa errada e a confirma. Isolamento de contexto ajuda na *atenção*, não em *mal-entendido compartilhado*.

**A consequência de desenho é decisiva:** o quality-gate **não pode** ter o PRD como fonte de verdade. Precisa de um oráculo externo à cadeia.

E aqui estava o problema prático: a `feature-wiki` **não guarda o requisito bruto**. Ele entra na conversa, vira PRD, e desaparece.

**A solução é barata e é o habilitador de tudo: `00-requisito.md`.**

```
wikis/specs/{branch}/{feature}/
├── 00-requisito.md          ← requisito bruto, verbatim, imutável
├── 01-plano-acao.md         ← interpretação do requisito
├── ...
└── 06-relatorio-qa.md       ← saída do quality-gate
```

Com ele, o confronto passa a ser triangular:

```
00-requisito.md   ──►  o que foi PEDIDO
01-plano-acao.md  ──►  o que foi PROMETIDO
app rodando       ──►  o que EXISTE
```

O requisito chega colado no chat ou como arquivo no projeto (`pdf`/`docx`/`md`) — em qualquer caso é **persistido no `00`** no momento da criação da wiki, com duas seções: **texto original imutável** + **decomposição em cláusulas numeradas** (`RQ-01`, `RQ-02`…) citando o trecho literal de origem. O texto bruto nunca é editado; a decomposição é derivada e revisável.

Efeito colateral valioso: cláusula ambígua (*"precisa ser rápido"* sem SLA) é registrada como **pergunta aberta** antes de qualquer código, em vez de suposição silenciosa.

---

## Ganho real 1 — Omissão silenciosa e a Matriz de Rastreabilidade

A **Matriz de Rastreabilidade** amarra cada cláusula do requisito a tudo que dela derivou:

```
cláusula → passo do PRD → CT → CT-B → código → resultado → veredito
```

> **Nomenclatura.** O termo adotado nesta coletânea — em documentos, no `06-relatorio-qa.md` e no `SKILL.md` — é **Matriz de Rastreabilidade**. A sigla **RTM** (*Requirements Traceability Matrix*) fica disponível como referência quando o contexto pedir: vocabulário de QA formal (ISTQB), conversa com time de qualidade, ou auditoria de setor regulado, onde o artefato é conhecido por esse nome. Em prosa corrente, escrever por extenso.

O valor não está em documentar o que existe — está em **expor a célula vazia**. E ela é **bidirecional**:

- **Para frente** (requisito → código): *o que foi pedido e não foi entregue?*
- **Para trás** (código → requisito): *o que foi entregue e ninguém pediu?*

| RQ | Cláusula (`00`) | Passo PRD | CT (`04`) | CT-B (`05`) | Código | Resultado | Veredito |
|---|---|---|---|---|---|---|---|
| RQ-01 | gerar relatório por turma em lote | 3, 4 | CT-01, CT-02 | CT-B01 | `GerarRelatorioLoteJob` | ✅ | OK |
| RQ-02 | notificar coordenador ao concluir | — | — | — | — | — | ❌ **omissão silenciosa** |
| RQ-03 | só coordenador pode disparar | 2 | CT-03 | — | `RelatorioPolicy` | ✅ | ⚠️ papel não validado na UI |
| RQ-04 | — | 6 | CT-07 | — | `ExportCsvAction` | ✅ | ⚠️ **escopo extra** |

A linha **RQ-02** é a razão de existir da skill: **nenhum teste falhou porque nunca existiu teste** — e nunca existiu teste porque a cláusula nunca virou passo do plano. CT e CT-B só podem falhar no que foi especificado. O `ponytail-review` audita se o plano tem **excesso**, nunca se tem **falta**. O TIA mede impacto do diff, não cobertura do requisito.

**Nenhuma das três camadas atuais é capaz de ver isso, por construção.**

---

## Ganho real 2 — As 12 dimensões que as camadas atuais não cobrem

Cada dimensão precisou responder por que as três camadas de revisão existentes não a cobrem. Aqui fica o porquê e um exemplo do que ela pega; o "como verificar" de cada uma está em [As 12 Dimensões](SKILL.md#as-12-dimensões).

| # | Dimensão | Por que escapa hoje | Exemplo do que pega |
|---|---|---|---|
| **A** | Cobertura do requisito | CT só falha no especificado | cláusula sem plano/teste/código |
| **B** | Fronteiras e dados | CT cobre o caso do PRD, não os vizinhos | `-1`, string de 500 chars, upload de 0 byte, 29/02 |
| **C** | Matriz de permissão | o CT de autorização testa **1** papel | 3 papéis × 4 ações = 12 células; o CT cobre 1 |
| **D** | Observabilidade real | o PRD **manda** logar `[Classe@Método]` — **quem confere?** | log fora do padrão da `feature-wiki`; **PII vazando no context** |
| **E** | Performance | CT passa em 3 queries ou em 300 | N+1, query sem índice, `->get()` onde cabia paginação |
| **F** | UX de erro | `assertSee('erro')` passa com mensagem inútil | "Erro ao processar" em vez de "CPF já inscrito na turma X" |
| **G** | Tema e cor (dark mode) | **CT-B passa com texto invisível** — ver [achado técnico](#achado-técnico-dark-mode-inverte-a-regra-de-visão--estrutura) | **texto branco em fundo branco: `assertSee()` PASSA** |
| **H** | Acessibilidade | só se alguém escreveu o CT-B | teclado, foco, contraste, `alt` |
| **I** | Superfície nova de segurança | fora do escopo do CT | IDOR, mass assignment, rota sem `can:` |
| **J** | Regressão adjacente | TIA diz quais testes o diff afetou, não o que **não tinha teste** | regra antiga silenciada pela evolução — só em wiki de evolução/correção/ajuste |
| **K** | Adequação da suíte (a suíte pega defeito?) | ninguém pergunta se o teste **falharia** diante de implementação errada; 100% de linha é compatível com zero assertion útil | teste sem oráculo, `assertOk()` sozinho; mutante que sobrevive |
| **L** | Consistência documental (wiki × código × docs × rules) | quem escreveu o texto o lê como certo; o step 7 registra desvios só no `03` | PRD/ADR afirmando o que o código não faz; ID de CT só no teste; rule do projeto violada no diff; docs pt × en divergentes; frase em doc sem `RQ` de origem; número da Verificação Final que nenhum comando reproduz |

A dimensão **D** é auto-referente e reveladora: a `feature-wiki` exige log em toda etapa de execução, com channel dedicado e context estruturado — e **nada no ciclo atual verifica se isso aconteceu**. O quality-gate fecha o laço da própria skill principal.

A dimensão **L** (1.2.0) nasceu de uma medição: numa feature real, depois do step 7 da `feature-wiki` "concluído", uma revisão independente achou 31 itens, 27 deles texto defasado — PRD, ADR, `04`, docs e rules. Quem escreveu o texto o lê como certo; a auditoria tem de ser de quem não escreveu.

---

## Ganho real 3 — Roteamento de achados

A taxonomia que não existe no mercado. Cinco destinos, não dois: **especificação**, **implementação**, **teste**, **infra** e **não-defeito**. Achado que só diz "está errado" devolve o problema sem dizer em que estação ele nasceu; roteado, requisito ambíguo volta para a escrita da wiki, e não para o código.

**A Matriz de Rastreabilidade alimenta o roteamento.** O formato da lacuna determina o destino — deixa de ser opinião do agente e passa a ser consequência de uma célula vazia.

O destino **teste** é o mais valioso e o mais fácil de errar: invertida a ordem (corrigir antes de ter o CT que falha), perde-se a prova e o caso reaparece na feature seguinte.

E a decisão **bloquear × registrar** é por severidade, senão o loop nunca fecha por cosmética: o que não bloqueia entra num ledger de débito na wiki (mesma ideia do `ponytail-debt`).

A taxonomia completa — severidade, os cinco destinos com o que fazer em cada um, a prioridade entre eles e a tabela padrão da lacuna → destino — está em [Classificação e Roteamento](SKILL.md#classificação-e-roteamento).

---

## Achado técnico: dark mode inverte a regra de visão × estrutura

O `pest-plugin-browser` tem ferramentas para tema, screenshot e acessibilidade. O que cada uma faz e não faz — inclusive o alcance da regra de contraste do axe — está numa fonte só: `{skills}/feature-test-design/references/pest-plugin-browser.md`, onde `{skills}` é o diretório onde as skills estão instaladas: `.ai/skills/` (Boost), `.claude/skills/` (espelho local) ou `~/.claude/skills/` (global); use o primeiro que existir.

O que é da dimensão G é a consequência: dentro do plugin, nenhuma assertion barata prova cor. Os casos graves — texto invisível no tema escuro, classe sem par `dark:`, baseline de screenshot criado com o defeito — passam, e estão tabelados na referência.

A cobertura escolhida vai do mais barato ao mais caro: grep estático de classe de cor sem par `dark:` (o melhor custo-benefício), CT-B versionado no tema escuro e inspeção visual pelo Playwright MCP — o único caminho para "ilegível". Como o jeito de forçar o tema no teste muda com o projeto, a dimensão começa detectando o mecanismo de tema. Os comandos estão na [dimensão G](SKILL.md#g--tema-e-cor-dark-mode).

> **Correção de ênfase relevante.** Na análise do Playwright MCP a coletânea defende a árvore de acessibilidade contra o screenshot, pelo custo em token (os números estão na [dimensão G](SKILL.md#g--tema-e-cor-dark-mode)). **Para defeito de cor isso se inverte**: a árvore é justamente cega ao problema, porque o texto *está* lá. Cor é o caso em que a visão ganha da estrutura — e a skill precisa dizer isso explicitamente para o agente não aplicar a regra errada.

---

## Achado técnico: Playwright MCP como confronto do CT-B

A coletânea já define que **o `pest-plugin-browser` atesta e o Playwright MCP observa**. Para o quality-gate, o MCP habilita três confrontos: elementos interativos da tela × elementos que o CT-B exercita; UI renderizada × tabela `## Superfície de UI` do PRD; e tema, console e rede.

O primeiro é o mais valioso: elemento interativo que a tela oferece e nenhum CT-B exercita vira achado — é escopo ou scope creep? O exemplo está em [Playwright MCP como Confronto](SKILL.md#playwright-mcp-como-confronto).

Isso é literalmente "confronto do que entrou no CT-B", e nenhuma ferramenta de teste faz — teste só sabe o que você escreveu nele.

O que mantém a disciplina é que sessão MCP não é cobertura: todo achado do MCP vira CT-B novo ou achado roteado, nunca "fica no relatório". A configuração, o alvo permitido e o que nunca entra em teste estão em [Playwright MCP como Confronto](SKILL.md#playwright-mcp-como-confronto).

---

## Regressão condicional por natureza da wiki

Rodar regressão em toda feature é caro e desnecessário. O gatilho certo é a **natureza da wiki**, declarada no `01` (`## Natureza da Wiki`: nova, evolução, correção ou ajuste, com a wiki ancestral quando não é nova). Wiki nova valida só a feature; as outras medem o impacto por TIA, rodam por ID os CT/CT-B da ancestral e aplicam RCRCRC aos arquivos que as duas tocaram.

Rodar os CT da ancestral **por ID** é o que garante que a evolução não silenciou uma regra antiga — algo que o TIA só pega se o teste existir.

Os passos e comandos estão em [Regressão Condicional](SKILL.md#regressão-condicional).

---

## Construir × reusar

**Construir apenas a camada que é nossa; delegar a técnica ao que já existe em MIT.**

### Delegar ao [`qa-skills`](https://github.com/petrkindlmann/qa-skills)

O mapa necessidade → skill, com o fallback inline de cada uma, está em [Delegação a Skills Externas](SKILL.md#delegação-a-skills-externas). Aqui fica o papel que o estudo deu a cada delegação:

| Skill | Papel |
|---|---|
| `risk-based-testing` | define a profundidade por risco |
| `exploratory-testing` | SBTM, charters time-boxed, heurísticas |
| `ai-bug-triage` | **alimenta o roteamento** dos 5 destinos |
| `bug-reproduction` | achado sem repro não é reportável |
| `ai-qa-review` | "o CT-01 testa o que diz testar?" |
| `test-reliability` | evita roteamento errado da causa (c) |
| `test-suite-curation` | só quando tipo ≠ nova |
| `quality-postmortem` | defeito escapado: fora do loop, sob demanda |
| `release-readiness` | *(futuro)* gate de deploy; cobriria a 4ª etapa da esteira |

### Construir aqui

| Camada | Por que é nossa |
|---|---|
| Confronto `00-requisito` × PRD × app | só existe porque a `feature-wiki` produz esses artefatos |
| Taxonomia de 5 destinos + severidade | **verificado: não existe no mercado** |
| Convergência do loop (teto, sem-achado-novo, escalada) | idem |
| `06-relatorio-qa.md` com rastreabilidade por ID de CT/ADR | idem |
| Checks Laravel-específicos: log real × PRD, N+1, matriz de permissão, dark mode Tailwind | nenhuma skill genérica conhece o **nosso** padrão de log |
| Gate de regressão por natureza da wiki | idem |

### Duas ressalvas sobre a dependência

1. **Não instalar as 50.** A biblioteca inteira é inflação de contexto — o mesmo problema combatido nas Project Rules. O `SKILL.md` lista as que a skill usa; copie só essas pastas para `.ai/skills/`. *(A confirmar se o instalador permite seleção; se não, cópia manual.)*
2. **Degradar graciosamente.** O quality-gate precisa funcionar sem elas — mesmo padrão do Playwright MCP na `feature-wiki`. Cada delegação tem fallback inline em [Delegação a Skills Externas](SKILL.md#delegação-a-skills-externas).

---

## Convergência e separação de poderes

"Loop engineering" sem regra de parada é loop infinito. Por isso o desenho fixou, desde o estudo, um teto de ciclos, o critério "sem achado novo encerra", a escalada ao humano quando o teto estoura e um orçamento de dimensões por risco. E fixou a separação de poderes: o quality-gate **não corrige nada**, porque quem julga e conserta volta a ter cegueira correlacionada.

Os valores e o procedimento estão nos [Princípios Inegociáveis](SKILL.md#princípios-inegociáveis) e em [Convergência do Loop](SKILL.md#convergência-do-loop).

---

## Riscos honestos

| Risco | Mitigação |
|---|---|
| **Custo por ciclo** — 12 dimensões × 3 ciclos numa feature pequena é desproporcional | gate de esforço agressivo por risco |
| **Cegueira correlacionada residual** — requisito original já ambíguo pode ser interpretado igual duas vezes | forçar a listagem das **ambiguidades do `00`** como achado tipo 1 **antes** de validar qualquer coisa |
| **Relatório que ninguém lê** — `06` com 400 linhas morre | teto: veredito + tabela de achados + Matriz de Rastreabilidade. Detalhe vai em anexo ou não vai |
| **Matriz como métrica de vaidade** — "98% de cobertura" em planilha morta | ela existe só como **detector de lacuna**; ciclo sem lacuna não imprime tabela, só o veredito |
| **Quarta camada de revisão** virar burocracia | cada dimensão precisa justificar por que as 3 camadas atuais não a cobrem |

---

## Critério eliminatório

Registrado para evitar autoengano no futuro:

> **Se o quality-gate ler apenas a wiki, ele é teatro de qualidade** — gasta tokens confirmando o que já estava verde, e a recomendação passa a ser *não construir a skill* e apenas instalar 4-5 skills do `qa-skills`.
>
> A skill só se justifica **se** o `00-requisito.md` existir e for tratado como linha de base, com o PRD rebaixado a **alegação a ser testada**.

Por isso o `00-requisito.md` na `feature-wiki` é **pré-requisito**, não melhoria opcional.

**Como o `SKILL.md` honra o critério**, ponto por ponto:

| Exigência do estudo | Onde está implementada |
|---|---|
| Oráculo externo, PRD rebaixado a alegação | Princípio 1 — declarado como inegociável |
| Wiki antiga sem `00` não passa em silêncio | seção "Oráculo degradado" — pede o requisito ao usuário, proíbe derivar do PRD, e estampa o aviso no topo do relatório |
| Detectar omissão silenciosa | Dimensão A + Matriz de Rastreabilidade, marcada como **"nunca pular"** |
| Roteamento em 5 destinos | seção "Classificação e Roteamento", com a tabela padrão-da-lacuna → destino |
| Não corrigir o que julga | Princípio 2 + 11 proibições explícitas |
| Convergência | Princípio 3 + seção própria: teto de 3, sem-achado-novo, dedupe contra o `06` anterior |
| Teto por risco | Gate de esforço com 3 perfis (mínimo / padrão / completo) |
| Degradação graciosa | Princípio 5 + coluna "Fallback inline" na tabela de delegação + seção "Não Verificado" no relatório |
| Dark mode inverte a regra visão × estrutura | Dimensão G, com o aviso destacado e os 3 níveis de verificação |
| MCP como confronto, não como cobertura | seção "Playwright MCP como Confronto" — 3 confrontos + a regra dos dois destinos obrigatórios |
| Não reinventar técnica de QA | tabela de delegação ao `qa-skills`, com a ressalva de instalar só as usadas |
| Relatório que não morre de tamanho | teto de ~150 linhas; "cortar detalhe, não cortar achado" |
| Matriz não virar métrica de vaidade | matriz só é impressa **se houver lacuna** |

---

## Fontes

- [petrkindlmann/qa-skills — 50 QA skills, MIT](https://github.com/petrkindlmann/qa-skills)
- [qa-skills na discussão do agentskills](https://github.com/agentskills/agentskills/discussions/369)
- [5 Must-Have QA Skills for Claude Code — QASkills.sh](https://qaskills.sh/blog/must-have-qa-skills-claude-code-2026) *(origem da citação sobre nenhuma skill rotear achados)*
- [QASkills.sh — diretório Claude Code](https://qaskills.sh/agents/claude-code)
- [Awesome Skills — categoria Testing & QA](https://awesomeskill.ai/category/testing-qa)
- [QA Engineer Agent](https://mcpmarket.com/tools/skills/qa-engineer-agent-1)
- [Best QA and Testing Skills for Claude Code — Agensi](https://www.agensi.io/learn/best-qa-testing-skills-claude-code-2026)
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- [Playwright Test Agents (planner / generator / healer)](https://playwright.dev/docs/test-agents)
- [Playwright MCP — snapshots e custo de token](https://playwright.dev/mcp/snapshots)
- [Pest — Browser Testing](https://pestphp.com/docs/browser-testing)
- [Pest — TIA](https://pestphp.com/docs/tia)
- [Laravel Boost — skills e MCP tools](https://laravel.com/docs/13.x/boost)
