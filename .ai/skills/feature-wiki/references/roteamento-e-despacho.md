> Referência da feature-wiki 3.6.0. Lida em: antes de montar o quadro de despacho e antes do primeiro despacho de cada step (rota, ferramentas, o que o sub-agente não recebe). Fonte única de: tabela de rotas, formato do quadro de despacho e mapa de roteamento por step.

# Roteamento e despacho

As regras de roteamento — os dois eixos, a rota `mecânico`, como obter as rotas, paralelo,
quadro visível, o que roda em linha e a auditoria do retorno — ficam no corpo do `SKILL.md`, seção
*Execução e Delegação*. Aqui ficam as tabelas.

### Rotas

| Rota | Modelo | Uso nesta esteira | Ferramentas |
|---|---|---|---|
| **mecânico** | `haiku` | grep em lote com a tabela pronta (Superfície Livewire, classe irmã, factories, rotas, policies, config), conferência de citação `arquivo:símbolo:linha`, `diff` de IDs de CT, espelho `01` → `03`, contagens por `grep -c`, `search-docs` uma pergunta por consulta — devolve o artefato **como texto**; a sessão grava | leitura + Bash |
| **construtor** | `sonnet` | gerar artefato a partir de template e insumo: rascunho do `01`/`02` a partir do pacote de pesquisa, código de **um** passo do PRD guiado pelo plano e pelo `04`, arquivo de teste a partir do Gherkin | tudo |
| **analista** | `opus` | julgamento com contexto: revisão profunda do plano (step 5), ADR, derivação do `04` pela `feature-test-design`, os 4 gates de candidato a rule, classificação de achado — devolve o artefato **como texto**; a sessão grava | leitura + Bash |
| **revisor-diff** | `opus` | step 6.5, passe de eixos sobre o diff. **Cego ao PRD** | leitura + Bash; **sem** Edit/Write |
| **adversário-ct** | `opus` | revisão adversarial da `feature-test-design`. Recebe **só** `00` + `04`/`05` | leitura; **sem** Edit/Write/Bash |
| **qa-gate** | `opus` | step 8: roda a `feature-quality-gate` inteira e devolve o `06` **como texto**. Não grava nada | leitura + Bash + MCP herdado (Boost, Playwright); **sem** Edit/Write |
| **executor-ct** | `sonnet` | escrever e rodar os testes Pest de **backend** a partir do Gherkin do `04`, sob o [contrato do construtor de testes](delegacao-casos-de-teste.md#contrato-do-construtor-de-testes-executor-ct): classifica cada vermelho em a/b/c e **nunca toca `app/`** | tudo, sob o contrato |
| **executor-ctb** | `sonnet` | escrever e rodar os CT-B em loop, sob o [contrato dos CT-B](delegacao-casos-de-teste.md#ciclo-de-escrita-e-auditoria-dos-ct-b-loop--sub-agente) | tudo, sob o contrato |
| **sessão principal** | o da sessão | captura **verbatim** do requisito, decomposição em `RQ`, perguntas ao usuário, decisão de roteamento de achado, veredito final, auditoria de todo retorno | — |

## Formato do quadro de despacho

| # | Agente / tarefa | Modelo | Depende de | Não recebe (cegueira) | Por quê este modelo |
|---|---|---|---|---|---|
| 1 | `mecanico` — greps da Superfície Livewire, tabela pronta | haiku | — | — | transformação direta, sem julgamento |
| 2 | `fw-revisor-diff` — eixos sobre `main...HEAD` | opus | último construtor | `01`, `03`, raciocínio da sessão | julgamento crítico; cegueira exigida |

### Mapa de roteamento por step

| Step | Tarefa | Rota | Em paralelo com | Cegueira |
|---|---|---|---|---|
| 0, 2 | capturar requisito verbatim, decompor em `RQ`, nomear a feature | **sessão** | — | — |
| 3 | mapeamento amplo do código | `Explore` (built-in) | greps abaixo | — |
| 3 | greps de Superfície Livewire, classe irmã, factories, rotas, policies, config, `.env.example` — **tabelas prontas** | `mecânico` ×N | entre si e com o `Explore` | — |
| 3 | `search-docs` por stack, com a versão | `mecânico` | entre si | — |
| 4 | `00-requisito.md` | **sessão** | — | — |
| 4 | rascunho do `01` e do `02` a partir do pacote de pesquisa | `construtor` | — | — |
| 4 | `03` espelhando o `01` | `mecânico` | derivação do `04` | — |
| 4 | derivação do `04`/`05` — lê e segue `{skills}/feature-test-design/SKILL.md` | `analista` | `03` | recebe `00` inteiro; do `01`, **só** paths, rotas e `## Superfície de UI`; do `02`, **só** `## Superfície Livewire` (a própria skill delimita). Perguntas voltam como saída; a sessão as leva ao usuário |
| 4 | revisão adversarial do `04` | `adversário-ct` | — | recebe **só** `00` + `04`/`05` |
| 5 | levantar cada premissa do plano no código: existe? assinatura? linha? | `mecânico` | classe irmã | — |
| 5 | julgar as divergências e corrigir a wiki | `analista` ou **sessão** | — | — |
| 6 | `/ponytail:ponytail-review` | em linha (comando do plugin) | — | — |
| 6 | re-sincronização do `04` após corte que mude a `## Superfície de UI` | `mecânico` cruza índice × elementos cortados; **sessão** decide `@obsoleto` ou re-derivar | — | — |
| pré-6.5 | re-varrer a `## Superfície Livewire` do `02` sobre o **código final** | `mecânico` | — | — |
| impl. | cada passo do PRD, com o `04` como contrato | `construtor`, **sequencial** por padrão | só com arquivos disjuntos | não edita `00`, `04`, `05` |
| impl. | teste Pest a partir do Gherkin do `04` | `executor-ct` | passo seguinte, se disjunto | não lê `01`/`02`; lê `app/` só para nomes, nunca para o `Então`; **não toca `app/`** |
| **6.5** | `/code-review high {base}...HEAD` | o próprio comando (já roda em sub-agente isolado) | passe de eixos | — |
| **6.5** | passe de eixos sobre o diff | `revisor-diff` | `/code-review` | **não recebe** `01`, `03` nem o raciocínio da sessão; recebe diff, eixos, `## Superfície Livewire` do `02`, rules que casam o diff |
| 6.5 | roteamento do achado: Adendo → CT → correção | **sessão** decide; `construtor` corrige | — | — |
| 7 | citações, `diff` de IDs, checkbox sem evidência, docs pt/en × CHANGELOG | `mecânico` ×N | entre si | — |
| 7 | conformidade com rules — candidatos por glob, veredito por rule | `mecânico` levanta, `analista` julga | — | — |
| 7 | CT-B em loop | `executor-ctb` | — | contrato existente |
| **8** | `feature-quality-gate` inteira — lê e segue o `SKILL.md` dela | `qa-gate` | — | **não recebe** a conversa; só path da wiki, URL do app e `git diff --stat`. Devolve o `06` como texto; a **sessão** grava sem editar |
| 9 | 4 gates dos candidatos a rule | `analista` | — | — |
| 9 | decisão e `record-rule` | **sessão** + usuário | — | — |

> **Por que o step 8 é o maior ganho.** A `feature-quality-gate` pede *"por quem não escreveu a
> wiki"* e *"não corrige nada"*. Invocada em linha, ela roda na sessão que escreveu o `01` e
> implementou — a cegueira correlacionada que ela existe para quebrar. Em sub-agente **sem
> Edit/Write**, as duas exigências deixam de ser promessa: o juiz não viu a conversa e não
> consegue consertar.
