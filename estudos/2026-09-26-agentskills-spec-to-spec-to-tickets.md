# Spec Agent Skills × `/to-spec` × `/to-tickets` × coletânea — análise, crítica e roteiro

> Estudo de 2026-09-26. Objetos analisados: a especificação [Agent Skills](https://agentskills.io/specification)
> (validada com `skills-ref` 0.x via `npx skills-ref validate`), as skills `to-spec` e `to-tickets` de
> `mattpocock/skills` (lidas no fonte, `skills/engineering/*/SKILL.md`, 2026-09-26) e as páginas que as
> explicam em aihero.dev, o vídeo *"meu fluxo de trabalho com IA"* (transcrição fornecida pelo usuário) e
> esta coletânea (`feature-wiki` 3.5.1, `feature-test-design` 1.14.0, `feature-quality-gate` 1.5.1,
> `requirement-to-rule` 1.2.0, cinco sub-agentes `fw-*`).
>
> Este documento existe para decidir **o que importar, o que recusar e o que consertar** — não para
> eleger vencedor. A parte interna (§7) consolida a auditoria de cinco revisores independentes sobre
> as quatro skills e os cinco agentes.

---

## Sumário executivo

**1. Contra o spec, as quatro skills reprovam — e por dois motivos mecânicos, não de mérito.**
`skills-ref validate` reprova as quatro: o campo `version` não é permitido no frontmatter (o lugar
dele é `metadata.version`), e três das quatro `description` estouram o teto de 1024 caracteres
(3636, 2245 e 1369). Nenhuma usa `compatibility`, `license` nem `references/`. O corpo do
`SKILL.md` da `feature-wiki` tem 2453 linhas (~39 k tokens) contra os 500 / 5 k recomendados; a
`feature-test-design`, 1561 (~25 k). O spec funciona em três camadas — metadados sempre carregados,
corpo carregado na ativação, recursos sob demanda — e a coletânea usa só a segunda, com a primeira
inflada e a terceira ausente.

**2. `/to-spec` e `/feature-wiki` discordam no oráculo, e a coletânea está certa.** A `to-spec`
sintetiza *a conversa* ("não entrevista, só sintetiza o que já foi decidido") numa spec de user
stories "extremamente extensas", sem rastreio para a fonte. A `feature-wiki` guarda o **texto
bruto imutável** e decompõe em cláusulas `RQ` com citação literal. O quality gate desta coletânea
classificaria a spec da `to-spec` como *oráculo degradado*. O que a `to-spec` tem e a coletânea
não tem: **costuras de teste** (seams) declaradas e confirmadas com o usuário antes de escrever,
proibição de path e snippet no artefato durável (porque envelhecem — o CHANGELOG da `feature-wiki`
3.5.1 registra exatamente esse defeito), e 60 linhas em vez de 2453.

**3. `/to-tickets` resolve um problema que a coletânea tem e ainda não nomeou: a unidade de
planejamento.** O `01-plano-acao.md` fatia por **camada** (migration → model → service → UI, path
por passo). É a fatia horizontal que a `to-tickets` argumenta contra com um caso medido (26 tickets,
~20 rodadas por ticket, três quartos retrabalho). A coletânea fatia paralelismo por *arquivo
disjunto*, não por *comportamento demonstrável*, e não tem regra de dimensionamento: a feature medida
em 2026-09-21 rodou numa sessão com 48 despachos e ~4,6 M tokens. A proposta é uma quinta skill,
`feature-tickets`, onde o ticket é **um subconjunto de `RQ` do `00` mais os `CT` do `04` que ele
faz passar** — o que dá dimensionamento, aresta de bloqueio e critério de aceite falsificável de
graça, porque o `04` já existe.

**4. O vídeo acrescenta a tese do gestor: visibilidade por estado (todo / doing / review) que
sobrevive à compactação e à troca de ferramenta.** A coletânea tem o `03-progresso.md` com evidência
inline — sobrevive à compactação — mas por feature, sem estado "em revisão" e sem quadro entre
features. O outro ponto do vídeo, *"regra determinística que roda antes de me pedir review"*, a
coletânea já tem em prosa (greps do step 7, `pest --arch` na escada da `requirement-to-rule`) e
ainda não tem em `scripts/`.

**Recomendação, em ordem:** (a) conformidade ao spec — barata, sem risco; (b) `references/` e
`scripts/` na `feature-wiki` e na `feature-test-design`, **medindo** com o protocolo de
`experimentos/` antes e depois, porque a regra desta coletânea de que "regra nasce de defeito
medido" vale para ela mesma; (c) `feature-tickets`; (d) costuras declaradas; (e) quadro de estado.
O que **não** importar: user stories geradas, spec publicada fora do repositório, `to-spec` sem
`00`, "número ideal de costuras é um".

---

## 1. A especificação Agent Skills — o que ela pede e o que a coletânea faz

### 1.1 O que o spec define

| Item | Regra | Fonte |
|---|---|---|
| Diretório | `skill-name/SKILL.md` obrigatório; `scripts/`, `references/`, `assets/` opcionais; qualquer outro arquivo permitido | §Directory structure |
| `name` | 1–64, `a-z0-9-`, sem hífen nas pontas nem duplo, **igual ao nome do diretório** | §name |
| `description` | 1–1024 caracteres; **o que faz e quando usar**, com palavras-chave de gatilho | §description |
| `license`, `compatibility` (≤ 500), `metadata` (mapa string→string), `allowed-tools` (experimental) | opcionais; `compatibility` só se há exigência de ambiente | §Frontmatter |
| Corpo | sem restrição de formato; recomendado passo a passo, exemplos, edge cases; **< 500 linhas, < 5 000 tokens**; o resto vai para arquivos referenciados | §Body, §Progressive disclosure |
| Referências | caminho relativo à raiz da skill, **um nível de profundidade** | §File references |
| Validação | `skills-ref validate ./skill` | §Validation |

O modelo mental é **progressive disclosure** em três camadas: metadados (~100 tokens, sempre
carregados, para todas as skills), instruções (carregadas na ativação), recursos (sob demanda).

### 1.2 O que a coletânea faz hoje — medido

`npx skills-ref validate` em 2026-09-26:

| Skill | `name` = dir | `version` no topo | `description` | Corpo (linhas / tokens est.) | `references/` | `scripts/` |
|---|---|---|---|---|---|---|
| `feature-wiki` | ✅ | ❌ campo não permitido | ❌ 3636 chars | 2453 / ~39 k | — | — |
| `feature-test-design` | ✅ | ❌ | ❌ 2245 chars | 1561 / ~25 k | — | — |
| `feature-quality-gate` | ✅ | ❌ | ❌ 1369 chars | 810 / ~11 k | — | — |
| `requirement-to-rule` | ✅ | ❌ | ✅ 757 chars | 398 / ~5,6 k | — | — |

Saída literal do validador para a `feature-wiki`:

```text
Validation failed for .ai/skills/feature-wiki:
  - Unexpected fields in frontmatter: version. Only allowed-tools, compatibility, description, license, metadata, name are allowed.
  - Description exceeds 1024 character limit (3636 chars)
```

Custo concreto da primeira camada: as quatro descrições somam ~8 k caracteres (~2 k tokens)
carregados **em toda sessão, mesmo quando nenhuma skill é ativada**. A descrição da `feature-wiki`
lê como release note (cita Pest 5, Caveman, Ponytail, step 7, adendo, quality gate). O spec pede
o que faz + quando usar + palavras-chave; o resto é conteúdo de README.

### 1.3 O que já aplicamos, sem chamar pelo nome

| Técnica do spec | Já temos? | Onde | Observação |
|---|---|---|---|
| Diretório por skill com `SKILL.md` | ✅ | `.ai/skills/*/` | conforme |
| `name` igual ao diretório | ✅ | os quatro | conforme |
| Arquivos extras além do `SKILL.md` | ✅ | `README.md` (pessoa), `agents/` (sub-agentes) | o spec permite; `agents/` é convenção nossa, não do spec |
| Separação "para o agente × para a pessoa" | ✅ | README × SKILL | é progressive disclosure **para o humano**; para o agente não há camada 3 |
| Versionamento por skill | ✅, no campo errado | `version:` no topo | mover para `metadata.version` — o spec cita exatamente esse uso |
| Índice no `SKILL.md` | ✅ | `feature-wiki` §Índice | um índice não economiza token: o arquivo inteiro é carregado |
| `compatibility` | ❌ | — | é o caso de uso exato: Laravel Boost MCP, Pest 5, sub-agentes do Claude Code |
| `license` | ❌ | `LICENSE` na raiz é MIT | `license: MIT` |
| `references/` (camada 3) | ❌ | — | maior ganho disponível |
| `scripts/` | ❌ | — | os greps do step 7 e do gate são candidatos |
| Validação em CI | ❌ | — | `npx skills-ref validate` por skill |

### 1.4 Onde evoluir — e o risco de evoluir

**Conformidade (sem risco, uma tarde):** `version` → `metadata.version`; `description` ≤ 1024 com
o quê / quando / palavras-chave (`feature`, `wiki`, `PRD`, `ADR`, `requisito`, `Laravel`,
`Livewire`, `Filament`); `compatibility: Claude Code ou Laravel Boost 2 com MCP; Pest 5; sub-agentes
opcionais em .claude/agents/`; `license: MIT`; um job de CI que roda o validador nas quatro.

**Camada 3 (ganho grande, risco real):** a `feature-wiki` tem pelo menos seis blocos que são
referência, não procedimento — templates dos arquivos 00–03, padrão de log (~260 linhas), Pest 5
(~110), roteamento e quadro de despacho (~210), citações de código (~45), Playwright MCP (~60),
integração Ponytail/Caveman (~85). Tirá-los para `references/` deixa o corpo perto do teto do spec
e reduz o custo por ativação em ~60–70 %.

O risco é conhecido e é o oposto do que o spec promete: o agente **não abre** o arquivo de
referência e a regra deixa de valer. Esta coletânea mediu (README raiz, *Validado em campo*) que
regras escritas no `SKILL.md` já são ignoradas às vezes ("atualizar em tempo real, não em lote" foi
ignorado; a evidência inline nasceu disso). Uma regra num arquivo que precisa ser aberto tem menos
chance ainda. Mitigação: o corpo mantém **todos os gates e proibições**; `references/` recebe só
templates, tabelas e comandos; cada step que depende de uma referência diz "leia `references/X.md`
antes" e o checklist final tem o item "referências lidas: X, Y". E a mudança é **medida** com uma
rodada do protocolo de `experimentos/` — sem medição é troca de fé por fé.

**Tensão que o spec não resolve:** o Claude Code lê campos fora do spec (`disable-model-invocation`,
usado pela `to-spec`) no topo do frontmatter, não em `metadata`. Conformidade estrita ao spec e
uso das extensões do host são incompatíveis por construção; a coletânea deve decidir por skill.
Para a `feature-wiki` a resposta é fácil: ela **deve** ser invocada pelo modelo ("Invoque SEMPRE"),
então não precisa do campo. Para uma futura `feature-tickets`, invocação só pelo usuário faz
sentido, e aí o campo entra mesmo fora do spec — com o validador em CI configurado para tolerá-lo.

---

## 2. `/grill-me` e `/grill-with-docs` × o montante da coletânea

### 2.1 Como funcionam (fonte lido)

São quatro arquivos, e a composição importa mais do que cada um:

| Skill | Linhas | Invocação | O que faz |
|---|---|---|---|
| `grilling` | 30 | pelo modelo ("stress-test", "grill") | a primitiva: a entrevista |
| `grill-me` | 6 | só pelo usuário | `Call the Skill tool with "grilling"` — sem repositório, sem arquivo |
| `domain-modeling` | 70 | pelo modelo (terminologia, `CONTEXT.md`, ADR) | a disciplina de escrever glossário e ADR **enquanto** se decide |
| `grill-with-docs` | 6 | só pelo usuário | `Call the Skill tool twice, for "grilling" and "domain-modeling"` |

**A entrevista (`grilling`)** modela a conversa como uma **árvore de decisões**: cada decisão ramifica
nas que dependem dela. Trabalha em **rodadas**: a **fronteira** é o conjunto de perguntas cujos
pré-requisitos já estão decididos; a rodada pergunta a fronteira inteira, cada pergunta numerada
**com a resposta recomendada** (`❓ Q1 … ➡️ recomendação`), e espera. Pergunta que depende de outra
ainda aberta vai para a rodada seguinte. Duas regras de ouro: **fatos são trabalho do agente**
(despacha sub-agente para olhar o filesystem; nunca pergunta ao usuário o que pode descobrir
sozinho) e **decisões são do usuário**. Termina quando a fronteira está vazia — "nada assumido em
silêncio" — e **não age até o usuário confirmar** o entendimento compartilhado.

**A escrita (`domain-modeling`)**: desafia termo que conflita com o glossário existente
("seu glossário define 'cancelamento' como X, você parece dizer Y — qual?"); afia termo vago
("'conta' é Customer ou User?"); inventa cenários concretos para forçar fronteira entre conceitos;
**cruza com o código** ("seu código cancela o pedido inteiro, você disse que cancelamento parcial
existe — qual está certo?"); grava o termo em `CONTEXT.md` **no momento em que resolve**, nunca em
lote; `CONTEXT.md` é glossário e **só** glossário — "sem detalhe de implementação, sem spec, sem
rascunho". ADR **só** quando as três condições valem ao mesmo tempo: difícil de reverter,
surpreendente sem contexto, resultado de trade-off real. "Se falta uma, pule a ADR."

**Onde cai o que foi decidido** (a página do autor é explícita):

| O que resolveu | Onde aterrissa |
|---|---|
| um termo | `CONTEXT.md`, na hora |
| uma decisão que passa nos três portões | ADR em `docs/adr/` |
| **todo o resto** | **a conversa, e mais nenhum lugar** |

O autor chama isso de "a reclamação substantiva mais aberta sobre a skill": *"não há um livro-razão
ligando cada resposta resolvida a uma spec, um ticket e um teste. Respostas precisas (garantias de
ordenação, requisitos negativos, defaults numéricos) são amolecidas em prosa mais fraca a jusante,
e o resultado pode parecer completo enquanto perde a coisa que você de fato decidiu."* A mitigação
oferecida: não limpar o contexto, passar a mesma conversa para a `to-spec` e **reler a spec contra
as próprias respostas**.

Outras admissões da página e da `grill-me`: o defeito nº 1 reportado é a **delegação de uma linha
não carregar as dependências** (a entrevista vira "despejo indiferenciado de perguntas", sem
recomendação, sem `CONTEXT.md`); dentro de um orquestrador (wrapper SDD, framework multi-agente)
a metade que escreve arquivos "silenciosamente não acontece"; sessão típica de **46 perguntas em 4
rodadas**, e 200+ é sinal de escopo grande demais; "perguntas ingrilháveis" (como deve *parecer*
uma interação) precisam de protótipo, não de diálogo; o modo de falha do usuário é a
**passividade** ("concordo, concordo, concordo" por quarenta perguntas, e sai um plano que o agente
escreveu e você assentiu); e "dê o seu melhor modelo — mais do que para a maioria das skills".

### 2.2 O que a coletânea tem no lugar disso — conferido no `SKILL.md`

| Mecanismo da grilling | Equivalente na `feature-wiki` | Estado |
|---|---|---|
| Fatos são do agente | step 3 (Superfície Livewire, classe irmã, `search-docs`, stack de testes), step 5 (revisão profunda contra o código real) | ✅ **mais forte**: é obrigatório e tem tabela de greps; a grilling só diz "despache um sub-agente" |
| Cruzar afirmação com o código | step 5 "re-validar cada premissa" | ✅ equivalente, sem o formato de confronto ("você disse X, o código faz Y — qual?") |
| Perguntas ao usuário em rodadas, com recomendação | `## Ambiguidades e Perguntas Abertas` do `00`, com 4 perguntas obrigatórias | ⚠️ **uma rodada, reativa, sem recomendação, sem fronteira**. `grep -n 'entrevist\|grill\|rodada'` no `SKILL.md`: zero. As perguntas são listadas; **onde a resposta aterrissa não está escrito** (`grep -n resposta`: só ocorrências sobre `search-docs` e o Modelo de Execução) |
| Não agir até confirmação explícita | "confirmar com o usuário" (step 2, nome da feature) e checklist "perguntas feitas ao usuário" | ⚠️ sem artefato: a confirmação não fica registrada em lugar nenhum da wiki |
| Glossário do projeto (`CONTEXT.md`) | **nenhum**. O `## Glossário` do `SKILL.md` é das siglas da skill (`RQ`, `CT`, `PRD`); a wiki tem `## Mapeamentos` (campos, status), que é tabela de dados, não vocabulário | ❌ **lacuna real**. Termo de domínio decidido numa feature ("solicitante", "aprovador de etapa") não sobrevive para a próxima; a `requirement-to-rule` não o aceita (gate 2: rule é escopada por path; glossário é global) |
| ADR com três portões | `02` "cada decisão não-óbvia com justificativa" + template `ADR-01`, `ADR-02`… | ⚠️ **sem portão**: o template convida a preencher; a `domain-modeling` diz "a maioria das sessões não produz ADR nenhuma, e isso é funcionar como desenhado". A coletânea tem gates para **rule** (4, na `requirement-to-rule`) e nenhum para **ADR** |
| Livro-razão resposta → spec → ticket → teste | `RQ` → passo do `01` → `CT` do `04` → código, com Matriz de Rastreabilidade no gate | ✅ **é exatamente o que falta na grilling** — mas só para o que está no `00`. Resposta a pergunta aberta não tem `RQ`, então **fica de fora do livro-razão**: o mesmo buraco, em miniatura |
| Escopo: quando a sessão é grande demais | `feature-wiki` não tem regra de tamanho | ❌ a grilling ao menos nomeia o sintoma (200+ perguntas → fatiar antes) |

### 2.3 A diferença que nenhuma comparação de mecanismo captura: **quem responde**

A grilling assume que **o usuário é o dono da decisão**. Ela pergunta ao desenvolvedor, e o que ele
responde vira verdade. Na coletânea, o usuário é o desenvolvedor, mas o requisito chega de um
**card, de um documento ou de uma reunião** — o `00` tem `Fonte`, `Autor / solicitante` e
`Fidelidade: baixa (descrição verbal — confirmar antes de implementar)` exatamente porque quem
está na sessão **não é** quem pediu.

Importar a grilling inteira para a `feature-wiki` faria o desenvolvedor **responder pelo PO**.
Quarenta e seis respostas do dev sobre acumulação de papéis, visibilidade histórica e destino de
notificação são quarenta e seis requisitos inventados — com a mesma cara de requisito confirmado.
O próprio autor tem uma skill para o caso ("decisão bloqueada em conhecimento na cabeça de outra
pessoa" → `to-questionnaire`), e a página da `grill-with-docs` a lista como alternativa, não como
parte do fluxo principal.

A regra que a coletânea precisa, e que a grilling dá o vocabulário para escrever, é uma
**entrevista em três raias**:

| Raia | Pergunta sobre | Quem responde | Onde aterrissa |
|---|---|---|---|
| **fato** | o código, o schema, a config, a doc do framework | o agente (step 3/5, `mecânico`) | `01` (Análise dos Arquivos Existentes) |
| **desenho** | como implementar dado o requisito: costura de teste, cache, evento × observer | o desenvolvedor, em rodadas com recomendação | `02` — só se passar os três portões; senão, a linha da decisão no `01` |
| **requisito** | o que o sistema deve fazer quando o texto não diz | **o solicitante**, via pergunta registrada no `00`; até a resposta chegar, a cláusula é `RQ` **aberta** e nenhum passo do `01` a implementa | `00`, como **Adendo com fonte** (o procedimento já existe) |

Hoje as três raias estão misturadas na seção `Ambiguidades` do `00`, e a terceira raia não tem
regra de bloqueio: um `RQ` ambíguo pode virar passo do `01` com a interpretação do dev.

### 2.4 Crítica à grilling que a página não faz

- **É gerativa por construção.** "Entreviste implacavelmente até a fronteira esvaziar" produz
  perguntas que o requisito não pediu; o próprio autor reconhece o balão (200+). Não há oráculo
  que diga quais ramos da árvore **importam**. Na coletânea, o oráculo existe: um ramo importa se
  toca um `RQ`. Sem esse filtro, a entrevista otimiza para completude da árvore, não para
  cobertura do pedido.
- **Sem medição.** "Sharper idea in your own head" não é mensurável; nenhuma rodada, nenhum
  defeito plantado, nenhum juiz. A coletânea é o oposto: mede o elo que tem e não tem o elo que a
  grilling cobre. Nenhuma das duas mediu **o efeito de perguntar antes** no defeito entregue —
  seria a rodada mais valiosa do protocolo de `experimentos/`.
- **A composição por uma linha é o ponto mais frágil do sistema**, e é a mesma fragilidade que
  o spec Agent Skills empurra com `references/`: instrução que precisa ser carregada de outro
  arquivo às vezes não é. Vale como aviso para o §1.4: quando a `feature-wiki` migrar para
  `references/`, a falha de "carregou a metade" é a esperada, e precisa de verificação explícita
  ("liste as referências que abriu").
- **`CONTEXT.md` "só glossário"** é dogma útil e incompleto: o autor mesmo registra o contra-argumento
  público de que o modelo não ganha nada com o termo em vez da expansão em prosa, e que o valor é
  entre humanos. Para a coletânea, o valor de um glossário é outro: é o **único lugar durável e
  global** para vocabulário — o que a `requirement-to-rule` recusa por desenho.
- **ADR com três portões** está certo, e a coletânea deveria adotá-lo tal qual. O `02` sem portão
  vira o que o `04` de gabarito era: preenchimento de template.

### 2.5 O que importar

1. **Formato de pergunta** — numerada, com resposta recomendada, em rodadas pela fronteira. Vale
   para as perguntas do `00` e para as decisões de desenho do `01`/`02`. Custo: um bloco de 15
   linhas no `SKILL.md`; a `grilling` inteira tem 30.
2. **Raia de requisito com bloqueio** — pergunta ao solicitante fica no `00` como `RQ` aberta;
   passo do `01` que depende dela é marcado `bloqueado por RQ-nn`; a resposta entra como Adendo com
   fonte. Fecha o buraco do livro-razão que o autor da grilling admite e que a coletânea repete.
3. **Três portões para ADR** no `02` — e "zero ADR" como resultado válido.
4. **Glossário do projeto** — um `CONTEXT.md` (ou `.ai/glossario.md`) fora da wiki, alimentado no
   step 3/5 quando um termo é decidido, e lido pela `feature-test-design` (Gherkin com o vocabulário
   do projeto) e pelo gate (dimensão L, consistência documental). É a primeira peça de
   **montante** que a coletânea ganha desde o estudo SPDD.
5. **Confronto explícito código × afirmação** no step 5, no formato da `domain-modeling`: "o `01`
   diz X; `app/...` faz Y; qual vale?" — com a resposta registrada.

**Não importar:** a entrevista sem oráculo (o `00` filtra os ramos); a entrevista como substituta
do solicitante; `grill-me` sem repositório (não há caso de uso na esteira).

---

## 3. `/to-spec` × `/feature-wiki`

### 3.1 Como a `to-spec` funciona (fonte lido)

60 linhas. `disable-model-invocation: true` — só o usuário invoca. Três passos:

1. Explorar o repositório, usar o glossário do `CONTEXT.md` e respeitar as ADRs da área.
2. **Esboçar as costuras de teste** (*seams*) antes de escrever uma palavra; preferir costuras que
   já existem; "a mais alta possível"; "quanto menos, melhor — o ideal é uma"; **confirmar com o
   usuário**.
3. Escrever a spec pelo template e **publicar no issue tracker** com a label `ready-for-agent`.

Template: *Problem Statement* → *Solution* → *User Stories* ("uma lista LONGA, numerada,
extremamente extensa") → *Implementation Decisions* (módulos, interfaces, schema, contratos de API;
**"NÃO inclua paths de arquivo nem snippets — ficam desatualizados muito rápido"**, exceção para
snippet de protótipo que codifica uma decisão) → *Testing Decisions* (o que é um bom teste, quais
módulos, prior art) → *Out of Scope* → *Further Notes*.

Princípio declarado na página: *"não entrevista você, porque quando você chega nela a decisão já
foi tomada"* — a elicitação é da `grill-with-docs` (a montante), que também gera ADRs e glossário.
Limitações que o autor admite: não linka as ADRs que leu; não busca issues sobrepostas no tracker;
o template "se apoia em user stories" e serve mal a refatoração; a label `ready-for-agent`
disparou execução automática indevida ("a aresta mais reportada").

### 3.2 Comparação — onde discordam e quem está certo

| Eixo | `to-spec` | `feature-wiki` | Veredito |
|---|---|---|---|
| **Oráculo** | a conversa. User stories geradas pelo modelo, sem rastreio para a fonte | `00-requisito.md`: texto original **imutável** + `RQ-##` com citação literal + ambiguidades + fora de escopo | **Coletânea.** Story gerada é interpretação; o gate desta coletânea a chamaria de *oráculo degradado*. A `to-spec` não tem seção de ambiguidade — assume que a grilling resolveu tudo e não registra nada |
| **Montante** | `grill-with-docs` elicita, decide, escreve ADR e glossário **antes** | começa com o card colado; não há elicitação (achado 3.1 do estudo SPDD, ainda aberto) | **`to-spec`.** A coletânea continua sem montante. As 4 perguntas obrigatórias do `00` são um remendo, não uma elicitação |
| **Volatilidade** | proíbe path e snippet no artefato durável | exige path exato, assinatura, coluna de DB, log por passo, citação `arquivo:símbolo:linha` conferida por grep | **Os dois, em artefatos diferentes.** Decisão (02-ADR) não deve ter path; execução (01, passos) precisa. A coletânea já pagou o preço: 3.5.1 *"número escrito a mão envelhece no próprio ciclo"*. Regra a importar: **path e número só onde há reconciliação (step 7) cobrindo** |
| **Costuras** | declaradas e confirmadas antes de escrever; existente > nova; ideal = 1 | nenhum conceito nomeado; a costura é escolhida CT a CT pela `feature-test-design` (Pest feature / Livewire / browser) e o gate do `05` decide browser | **Importar a declaração, recusar o "ideal = 1".** Declarar onde cada grupo de CT se prende, confirmado com o usuário, reduz duplicação CT/CT-B. Mas "uma costura" é meta de custo de manutenção, sem medição; os 33/36 mutantes mortos vieram de derivação por regra, não de minimizar costuras |
| **Tamanho** | 60 linhas; o conhecimento vive em `CONTEXT.md`, ADRs e conversa | 2453 linhas; o conhecimento de stack (Livewire, Pest 5, log) vive dentro | **`to-spec`,** com a ressalva de que ela terceiriza o que a coletânea embute. É a separação *motor × hospedeiro × perfil de stack* (estudo SPDD §13.2), ainda não feita |
| **Destino** | issue no tracker, label, visível num board | `wikis/specs/{branch}/{feature}/` versionado com o código, no PR | **Coletânea para o artefato, `to-spec` para a visibilidade.** Wiki no PR é o que permite o step 7 reconciliar por diff. Falta o espelho no board (§5) |
| **Invocação** | só pelo usuário | pelo modelo, sempre que há feature nova | correto para cada uma |
| **Depois da spec** | `implement` (11 linhas: TDD nas costuras, typecheck, `code-review`, commit) | steps 5–9: revisão profunda, auditoria Ponytail, revisão de diff cega, reconciliação, quality gate, rules | **Coletânea.** A cadeia da `to-spec` não tem rastreabilidade, omissão silenciosa, mutantes nem regressão por wiki ancestral |

### 3.3 Crítica à `to-spec` que a página não faz

- **"Lista LONGA e extremamente extensa de user stories"** é instrução para gerar volume. Cada
  story sem fonte é uma cláusula que ninguém pediu, e a `to-tickets` depois deriva critérios de
  aceite dela. O erro que a própria `to-tickets` admite — critério "que reafirma o pedido em vez de
  derivar do artefato" — nasce aqui.
- **Sem seção de ambiguidade nem de perguntas abertas.** A `grill-with-docs` é opcional na prática
  (o vídeo mostra o autor pulando-a quando "já sabe"), e a `to-spec` não tem como saber se foi feita.
- **Não busca issues sobrepostas** e **não linka as ADRs** — admitido pelo autor. Sem link, a
  decisão e a spec divergem sem que ninguém perceba; a coletânea resolve isso com a ADR dentro da
  wiki e o step 7 reconciliando.
- **Testing Decisions** é prosa ("o que é um bom teste, quais módulos, prior art"). Não há técnica,
  não há critério de suficiência, não há oráculo. É o `04` de gabarito que esta coletânea mediu em
  52 % de arquétipo e 1 valor-limite em 125 casos.

### 3.4 O que importar da `to-spec`

1. **Costuras declaradas** — seção `## Costuras de teste` no `04` (ou no `01`), uma linha por grupo
   de CT: costura (Pest feature HTTP · componente Livewire · browser · unit de regra), existente ou
   nova, confirmada com o usuário. O gate do `05` passa a ser consequência da costura, não uma regra
   à parte.
2. **Path só onde há reconciliação** — na `02` (ADR) e no `00`, proibir path e número; no `01`,
   manter (o step 7 cobre). Já é o espírito da 3.5.1; falta virar regra explícita por arquivo.
3. **Montante** — não é da `to-spec`, mas a comparação expõe de novo: a coletânea precisa de uma
   etapa de elicitação ou de um contrato com quem a faz (SPDD, grilling, reunião). Fica registrado
   como dependência do roteiro, não como item deste estudo.

---

## 4. `/to-tickets` — como funciona e como evolui a coletânea

### 4.1 Mecânica (fonte lido, 5,6 kB)

1. **Entrada**: a conversa, ou uma referência (`/to-tickets #42`, path de spec).
2. **Explorar o código** (opcional) e procurar **prefactoring** — *"torne a mudança fácil, depois
   faça a mudança fácil"* — que vem sempre primeiro.
3. **Fatias verticais** (*tracer bullets*): cada ticket corta um caminho estreito mas **completo**
   por todas as camadas (schema, API, UI, testes); é demonstrável sozinho; **cabe numa janela de
   contexto nova**; declara as **arestas de bloqueio**. Exceção: **refatoração larga** (renomear
   coluna, retipar símbolo compartilhado) → *expand → migrate em lotes → contract*, cada lote um
   ticket bloqueado pelo expand, CI verde entre lotes.
4. **Quiz ao usuário**: lista numerada com título, *Blocked by* e *o que entrega*; perguntas fixas —
   granularidade, arestas corretas, fundir ou dividir. Itera até aprovação.
5. **Publicar**: local em `.scratch/<slug>/issues/NN-slug.md` (um por ticket, numerado em ordem de
   dependência) ou no tracker com bloqueio nativo. Template: *What to build* (comportamento
   ponta-a-ponta, não lista por camada) · *Acceptance criteria* · *Blocked by* · *Status:
   ready-for-agent*. Sem path, sem snippet. **Fronteira**: qualquer ticket cujos bloqueadores estão
   feitos pode ser pego; despacho é **manual** — uma sessão nova por ticket, `/implement 03`.

Justificativas na página: fatia horizontal "não funciona até a última camada aterrissar"; caso
medido de 26 tickets horizontais, ~20 rodadas de agente por ticket fechado, três quartos retrabalho;
critérios de aceite que "não avaliam nada" em três formas — já verdadeiro no commit base, satisfeito
só por trabalho de outro ticket, reafirma o pedido em vez de derivar do artefato. *"Se cabe numa
janela de contexto, você não precisa desta skill."*

### 4.2 Onde a coletânea está hoje — honestamente

| Conceito da `to-tickets` | Equivalente na coletânea | Lacuna |
|---|---|---|
| Ticket = fatia vertical demonstrável | passo do `01` = **camada** com path (`### 1. Migration`, `### 2. Model`…) | O agente implementa camada a camada numa sessão; nada é demonstrável até o último passo. É a fatia horizontal que a `to-tickets` mede como pior |
| Cabe numa janela de contexto | sem regra de dimensionamento; a feature inteira roda numa sessão | 48 despachos e ~4,6 M tokens numa feature (2026-09-21). A recuperação após compactação é o `03` com evidência inline — funciona, mas retoma um **passo**, não uma fatia verificável |
| Arestas de bloqueio persistidas | coluna *Depende de* no quadro de despacho, por disparo | a dependência existe por sub-agente, não por entregável; não é plano, é log |
| Paralelismo | "paralelo é o padrão"; **nunca dois construtores no mesmo arquivo**; conjuntos disjuntos declarados | paralelismo por *arquivo*, não por *comportamento*. Dois construtores em camadas diferentes da mesma fatia produzem partes que só se provam juntas |
| Prefactoring primeiro | *Varredura da classe irmã* (step 5) e *Análise dos arquivos existentes* (01) descobrem, mas não sequenciam | não há passo "prepare o terreno" separado e ordenado antes |
| Critério de aceite falsificável | **mais forte**: `04` derivado do `00` com gate de mutantes; CT vermelho no commit base por construção | a coletânea tem a falsificabilidade, mas não a **aloca por entregável** |
| Refatoração larga (expand–contract) | *"Quando NÃO invocar: refactoring puro"* — a coletânea sai de cena | lacuna real, prioridade baixa em feature Laravel; existe (renomear coluna = migration + model + factories + views + testes) |
| Fronteira e despacho manual | orquestrador único numa sessão | sem fronteira porque sem tickets |
| Setup do tracker (`docs/agents/issue-tracker.md`) | nada; a wiki é o tracker | ver §5 |

### 4.3 A proposta: `feature-tickets`, com o ticket ancorado no `00` e no `04`

A `to-tickets` deriva o ticket da spec e inventa critérios de aceite. A coletânea pode fazer melhor
porque **já tem o `04` antes de implementar**: o ticket é definido por *quais `RQ` ele satisfaz
ponta-a-ponta* e *quais `CT` ele faz passar*. Isso resolve de uma vez os três problemas de critério
que a `to-tickets` descreve — o CT é vermelho no base por construção (gate de mutantes), pertence a
um ticket só (alocação explícita) e deriva do requisito, não do pedido.

**Contrato proposto**

- **Entrada**: `00`, `01`, `04` (e `05` se houver). Invocação pelo usuário (`disable-model-invocation`),
  ou sugerida pela `feature-wiki` num step 4.5 quando o `01` tem mais de N passos ou toca mais de M
  arquivos — a regra de corte da `to-tickets` vale aqui: *se cabe numa sessão, não fatie*.
- **Saída**: `wikis/specs/{branch}/{feature}/07-tickets/NN-slug.md`, um por ticket, com:

  ```markdown
  # 03: Aprovador vê a fila e aprova um pedido

  **Entrega** (o que dá para demonstrar): {comportamento ponta-a-ponta, da perspectiva do usuário}
  **RQ cobertas**: RQ-02, RQ-05
  **CT que ficam verdes**: CT-04, CT-05, CT-07 · **CT-B**: CTB-02
  **Passos do 01 envolvidos**: 3, 4, 6  (link, não cópia)
  **Bloqueado por**: 01, 02 · **Bloqueia**: 05
  **Prefactoring**: não | sim → {o quê}
  **Costura**: {da seção Costuras do 04}
  **Status**: pronto | em execução | em revisão | concluído — {data, evidência}
  ```

- **Regras**: fatia vertical (toda camada que o `RQ` exige, ou o ticket não fecha); cabe numa sessão
  nova; prefactoring é ticket próprio e vem primeiro; **todo `RQ` do `00` pertence a exatamente um
  ticket** (RQ sem ticket = omissão silenciosa no nível do plano — um achado novo que o gate pode
  cobrar); **todo `CT` do `04` pertence a exatamente um ticket**; sem path no corpo (o `01` tem);
  quiz de granularidade e arestas antes de gravar.
- **Execução**: um ticket por sessão nova ou por `construtor` despachado com **só** o `00`, o `02`,
  os passos do `01` e os `CT` do ticket. Isso é também um instrumento de **cegueira** que a
  coletânea ainda não tinha: o construtor da fatia 03 não vê o raciocínio da fatia 02.
- **Fechamento**: os `CT` do ticket verdes + `pest --parallel --tia` contra a baseline; o `03`
  ganha uma linha por ticket em vez de espelhar os passos do `01`. O quality gate por feature
  continua no fim, com a Matriz de Rastreabilidade estendida à coluna *ticket*.
- **Espelho opcional** no tracker (`gh issue create` com *Blocked by*), configurado num arquivo
  do projeto, como a `setup-matt-pocock-skills` faz em `docs/agents/issue-tracker.md`.

**Por que skill nova, não step da `feature-wiki`:** o spec e a medição de custo dizem o mesmo — a
`feature-wiki` já tem oito vezes o tamanho recomendado; um step 4.5 com template e regras de fatia a
faria pior. E a `feature-tickets` tem gatilho diferente (só quando não cabe numa sessão).

### 4.4 O que **não** importar da `to-tickets`

- **Critério de aceite em prosa por ticket.** Já temos coisa melhor no `04`; duplicar em prosa
  reintroduz o critério que "reafirma o pedido".
- **Tickets em `.scratch/` fora do controle de versão.** A wiki vai no PR; o ticket também.
- **`ready-for-agent` como label automática** — o autor mesmo reporta que disparou execução
  indevida. Estado é campo do arquivo, e a transição para "em execução" é de quem despacha.

---

## 5. O vídeo — o que ele acrescenta, e o que ele não sustenta

### 5.1 Teses que valem para a coletânea

| Tese do vídeo | Onde a coletânea está | O que muda |
|---|---|---|
| **"Eu virei o gestor da IA; preciso ver todo / doing / review"**; board se paga há 25 anos | `03-progresso.md` por feature, checkbox com evidência; `## Despachos` registra quem fez o quê | Não há estado **em revisão** (o humano nunca é chamado a revisar um entregável, só o PR inteiro no fim) e não há quadro **entre** features. Com `feature-tickets`, `Status` por ticket e um `wikis/specs/INDEX.md` gerado (ou espelho no tracker) fecham os dois |
| **"Na primeira compactação você começa a perder; o artefato é o que sobrevive"**; trocar de ferramenta (Claude ↔ Antigravity) sem perder a tarefa | a wiki é markdown no repositório — sobrevive e viaja; o `03` com evidência foi desenhado para retomada | A retomada é por passo horizontal; o ticket vertical é a unidade que sobrevive **com algo demonstrável** |
| **"Regra determinística que a IA roda antes de me pedir review"** (ex.: controller não importa outra camada) | step 7 tem greps (checkbox sem evidência, IDs de CT, citações); `requirement-to-rule` tem a escada `pest --arch` → PHPStan → Rector → Pint → prosa | Tudo em prosa. `scripts/` da skill (spec §scripts) com os greps do step 7 e do gate; e a `requirement-to-rule` **gerar** o teste `arch()` quando a rule é mecânica, não só sugerir |
| **"Se eu tiver que escrever demais, era melhor fazer sozinho"** — mínimo de texto, máximo de contexto | entrada humana mínima (card colado); saída do agente máxima (wiki) | Vale para o **agente** também: 39 k tokens por ativação é "escrever demais" na direção contrária. É o argumento do spec por outro ângulo |
| **"Foco a energia no review, não na execução"** | os gates cegos (6.5, adversário, 8) são revisão **pelo agente**; o humano aprova a wiki e o PR | A coletânea mede o review do agente; o review do humano não tem ponto de entrada entre a wiki e o PR. O ticket "em revisão" é esse ponto |
| **Saber a stack evita queimar token** (Next.js num build estático) | `## Modelo de Execução` do `01` e a ADR existem para tornar a premissa falsificável | coincidem; a coletânea já tem o instrumento |

### 5.2 O que o vídeo afirma sem sustentar

- **"Não chego a ler todas as tasks... do Opus 4.8 em diante"** contradiz a tese central do
  review como garantia de qualidade. O board dá visibilidade; qualidade **é afirmada, não medida**.
  A coletânea tem o contrário: mede (13 rodadas, juiz cego) e tem pouca visibilidade.
- **Grilling → spec** sem oráculo. O vídeo pula a grilling "quando já sei", e a spec vira o que a
  conversa decidiu. Nenhum ponto do fluxo guarda o que foi **pedido**.
- **"Regras determinísticas"** aparecem como exemplo, não como sistema: não há catálogo, não há quem
  as revoga, não há medição de quanto erro cada uma evitou. A `requirement-to-rule` com os 4 gates
  e aprovação explícita é o sistema que falta ali.

---

## 6. Quadro consolidado — técnica × já temos × onde evoluir

| # | Técnica | Origem | Já temos? | Evolução proposta | Custo | Prioridade |
|---|---|---|---|---|---|---|
| 1 | Frontmatter conforme (`metadata.version`, `description` ≤ 1024, `compatibility`, `license`) | spec | ❌ | corrigir as quatro; CI com `skills-ref validate` | horas | **alta** |
| 2 | `description` = o quê + quando + palavras-chave | spec | ❌ (release notes) | reescrever as quatro; mover o resto para o README | horas | **alta** |
| 3 | Corpo < 500 linhas; `references/` | spec | ❌ | extrair 6 blocos da `feature-wiki`, taxonomias da `feature-test-design`; **medir** com rodada do protocolo | dias + rodada | **alta** |
| 4 | `scripts/` para verificação determinística | spec + vídeo | ❌ (prosa) | greps do step 7 e do gate como scripts; `requirement-to-rule` gera `arch()` | dias | média |
| 5 | Costuras de teste declaradas e confirmadas | `to-spec` | ❌ | seção `## Costuras` no `04`; gate do `05` derivado dela | horas | média |
| 6 | Path/número só onde há reconciliação | `to-spec` + 3.5.1 | parcial | regra explícita por arquivo (00/02 sem; 01 com) | horas | média |
| 7 | Fatias verticais com bloqueio e dimensionamento por sessão | `to-tickets` | ❌ | skill `feature-tickets` ancorada em `RQ` + `CT` | semana | **alta** |
| 8 | Prefactoring como ticket primeiro | `to-tickets` | parcial (varredura irmã) | ticket `00-prefactor` na `feature-tickets` | dentro de 7 | média |
| 9 | Fronteira e despacho por ticket com cegueira de fatia | `to-tickets` | ❌ | construtor recebe só a fatia | dentro de 7 | média |
| 10 | Expand–contract para refatoração larga | `to-tickets` | ❌ (sai de cena) | seção na `feature-tickets`; `feature-wiki` deixa de recusar refactor | dias | baixa |
| 11 | Estado todo / doing / review e quadro entre features | vídeo | parcial (`03`) | `Status` por ticket; `wikis/specs/INDEX.md`; espelho opcional no tracker | dias | média |
| 12 | Elicitação a montante | `grill-with-docs` | ❌ (SPDD §3.1) | fora deste estudo; dependência declarada | — | registrada |
| 13 | User stories extensas; spec fora do repo; `ready-for-agent` automática; "ideal = 1 costura" | `to-spec`/`to-tickets` | — | **não importar** | — | — |

---

## 7. Auditoria interna — as quatro skills e os cinco sub-agentes

> Consolidação dos relatórios de cinco auditores independentes (um por skill, um de consistência
> cruzada), cada um despachado **sem** o contexto desta sessão — o mesmo instrumento de cegueira que
> a esteira usa, aplicado à esteira. Cada auditor recebeu o mesmo roteiro: contradições internas,
> referências quebradas, documentado ≠ implementado, instruções inexecutáveis, agentes, crítica de
> desenho, top 10. Achados citados aqui com `arquivo:linha` no estado **anterior** à correção de
> hoje; o que foi corrigido está marcado ✅ e consta no CHANGELOG (patches 3.5.2 / 1.14.1 / 1.5.2 /
> 1.2.1). O que é decisão de desenho ficou aberto e está no roteiro (§8).

### 7.1 Achados transversais — o padrão importa mais do que a lista

| # | Padrão | Onde apareceu | Estado |
|---|---|---|---|
| T1 | **Bytes de controle no comando PowerShell** — `\a` virou BEL (0x07) e `\f` virou FF (0x0C) no commit `b6f43ae`; o bloco publicado não roda | `README.md` raiz, e os READMEs das 4 skills | ✅ corrigido nos 5 arquivos, conferido por `od -c` |
| T2 | **Citação científica errada em 5 lugares vivos** — arXiv 2607.22883 citado com "318 defeitos / ~8× / ~3× / reverte"; o estudo SPDD (§3.4) já tinha provado que é 318 métodos focais / 233 defeitos / ≈1,4× / ≈1,5× / "mitiga" e deixado a correção pendente | `feature-test-design` SKILL e README, `feature-wiki` SKILL e README, CHANGELOG | ✅ corrigido nos 4 arquivos das skills; o CHANGELOG ganha nota |
| T3 | **`description` acima do limite do spec** (3636 / 2245 / 1369 chars) e `version` fora de `metadata` | as 4 skills | ⏳ roteiro (item 1) — exige reescrever o gatilho de cada skill |
| T4 | **Mesma regra em três ou mais lugares, já divergindo** — `--parallel` com browser (proibido no `feature-test-design`, condicional na `feature-wiki`); "log vira CT" (proibido na 3.5.0, mantido em duas linhas); sondas do adversário (SKILL 7 itens × agente 8 itens); fatos do `pest-plugin-browser` (verbatim em 4 arquivos) | `feature-wiki` × `feature-test-design` × agentes × READMEs | ✅ divergências alinhadas; ⏳ a redundância em si é o item 3 do roteiro (`references/` com **uma** fonte) |
| T5 | **README que promete não duplicar o procedimento e duplica** — `requirement-to-rule` ~160 de 251 linhas; `feature-quality-gate` os 5 destinos e as regras de convergência (duas vezes no mesmo README); `feature-wiki` Playwright MCP e `search-docs` (idênticos ao SKILL) | os 3 READMEs | ⏳ roteiro (item 2): README = por quê, quando, limites, dependências |
| T6 | **Cegueira por prompt, não por construção** — os agentes `fw-revisor-diff`, `fw-adversario-ct` e `fw-qa-gate` têm `Read`/`Glob` sem restrição de path; `01`/`03` estão na mesma pasta do `00`/`04` que recebem. "Recuse ler" depende de obediência. O `fw-qa-gate` lê o `03`, que contém `## Despachos`, `## Desvios`, `## Retrospectiva` — o resíduo escrito da conversa que ele "não recebe" | 3 agentes; README raiz afirma "cegueira vem da construção" | ⏳ roteiro (item 9): pasta isolada com só o que o agente pode ver, ou hook `PreToolUse` negando `01-*`, `03-*`, `app/` |
| T7 | **"Não corrige nada, mecânico" é falso** — `Bash` fica liberado em `fw-revisor-diff` e `fw-qa-gate`; `>`, `tee`, `sed -i`, `git commit` são só proibidos por prompt | 2 agentes; `feature-wiki` SKILL:954 e `fw-qa-gate.md:39` chamam isso de "mecânico, não promessa" | ⏳ roteiro (item 9): `git status` antes/depois exigido no retorno **ou** `Bash` em `disallowedTools` |
| T8 | **Rotas sem `Write` que produzem arquivos** — `mecânico` "espelha 01 → 03", `analista` "deriva o 04/05 e corrige a wiki", ambos "leitura + Bash" | `feature-wiki` tabela de Rotas × mapa por step | ✅ declarado "devolve como texto; a sessão grava", como já era na rota `qa-gate` |
| T9 | **Skill em sub-agente que precisa despachar sub-agente** — a derivação do `04` roda no `analista`, e o `SKILL.md` da `feature-test-design` manda a derivação despachar o adversário e "fechar todos os achados"; sub-agente não despacha sub-agente, e ninguém era dono do fechamento | `feature-wiki` :346 × `feature-test-design` :1401, :1439 | ✅ dono declarado (a sessão principal despacha e fecha) |
| T10 | **Diário de bordo dentro do procedimento** — 25 linhas com "caso real / medido em 2026-09-xx" na `feature-wiki`, 19 blocos "Medido" na `feature-test-design`, 9 anedotas datadas no `feature-quality-gate`; regras de um caso único (`$table` pt-BR, 4 perguntas de um domínio de aprovação impostas a toda feature, `grep -F` por um FQCN, "2 mutantes 100 %") | as 3 skills grandes + `fw-adversario-ct` (o caso de 2026-09-21 vai no prompt de **todo** despacho) | ⏳ roteiro (item 3): a regra fica, o caso vai para `references/casos-medidos.md` ou CHANGELOG |
| T11 | **Versões e steps envelhecidos** — `requirement-to-rule` README em 1.1.0 e "step 8" na `description` (o que o agente lê para decidir invocar); README raiz com v3.1.0 / v1.10.0 / v1.2.0 no resumo da integração; "rodada 6 é a mais recente" com 7 rodadas posteriores; diagrama do README raiz sem o step 6.5 e linkando o PR **antes** do quality gate | README raiz, `requirement-to-rule`, `experimentos/README.md` | ✅ corrigido |
| T12 | **Comandos que não existem ou não funcionam como escritos** — `pest --arch` (não é flag; é `arch()` em teste) em 10 lugares; `tests/**/*.php` sem `globstar`; `XDEBUG_MODE=… pest` em passo que manda usar `.cmd`; `--mutate --path=` fora da referência de CLI; `/plugin marketplace add` sem manifesto no repositório; `-Recururse` | 4 skills + README raiz | ✅ corrigidos (o `--path` ganhou ressalva, não troca: funcionou nas medições) |
| T13 | **Instalação em três versões diferentes** — Opção 1 com agentes, passo 3 da integração Ponytail sem agentes, Opção 2 global sem `~/.claude/agents/` | README raiz | ✅ unificadas |
| T14 | **A `requirement-to-rule` nunca foi exercitada** — três versões, 398 linhas, zero execuções em `experimentos/`; todos os exemplos são da doc do Boost ou hipotéticos | `experimentos/`, estudo SPDD §3 (tabela "medida: ❌") | ⏳ roteiro (item 11) |

### 7.2 `feature-wiki` 3.5.1 → 3.5.2

O que o auditor mediu: 2453 linhas / 156 KB; procedimento executável (steps 0–9 + mapa) ≈ 660
linhas; ≈ 1.300 linhas movíveis para `references/`; checklist final com ~75 itens; 9
"OBRIGATÓRIO" em headings; 37 menções a Ponytail e 17 a Caveman numa skill cujo objeto é a wiki.

Contradições internas encontradas e resolvidas hoje ✅: "5 arquivos" × "4 arquivos"; log vira CT
× não vira; `--parallel` com browser; `APP_URL` no checklist × "nada a configurar"; rota
`adversário-ct` sem "sem Bash"; `--testsuite=Browser` × `tests/Browser`; step 8 "pode pular" ×
"`06` ausente é blocker"; duas âncoras do índice quebradas; `{base}` usado 5 vezes sem definição;
o contrato de delegação não entregava o `02` que a `feature-test-design` declara obrigatório;
skills do Boost listadas como se fossem da coletânea; "rules carregadas automaticamente" (o Boost
instrui a consultar); `Browser Logs` → `browser-logs`.

Contradições que são **decisão de desenho** e ficaram abertas ⏳:

- **Step 6 antes ou depois do step 4.** O step 4 cria o `04` (item 4) e manda "só então avançar
  para o 6"; o step 6 manda "preferir rodar sobre `01`/`02` **antes** de invocar a
  `feature-test-design`". O checklist aceita as duas ordens. A segunda é a certa (o Ponytail pode
  mudar o `01`, e o `04` referencia passos do `01`), mas exige renumerar: o `04` passa a ser
  derivado depois da auditoria. Roteiro, item 6.
- **Adendo = pedido verbatim do solicitante × Adendo = achado do revisor.** O step 6.5 manda o
  achado do `/code-review` virar "Adendo N, premissas `Pnn`" — o Adendo tem regime imutável, fonte
  e texto original; um achado de revisor não tem nenhum dos três, e o esquema `P-nn` nunca é
  definido (aparece só no relato de campo, `00 (P-24, P-25)`). Roteiro, item 6.
- **Dependência de Claude Code sem fallback declarado** — `SendMessage`, `Explore`; só o
  `/code-review` tem substituto. Roteiro, item 10.
- **`.cmd` poliglota** ("`<?php /*` como primeira linha do `.cmd`"): "medido de verdade" sem o
  arquivo no repositório. Roteiro, item 4 (`scripts/`).
- **Overfitting** listado em T10.

### 7.3 `feature-test-design` 1.14.0 → 1.14.1

O que o auditor mediu: 99,5 KB / ~25–28 k tokens; `description` com 2.343 chars; 19 blocos
"Medido"; 20 ocorrências de "obrigat"; ~400 linhas só nas 15 subseções do passo 3; núcleo
procedural estimado em ~400 linhas se o resto for para `references/` (tabela com 14 faixas no
relatório).

Resolvido hoje ✅: "sete passos" com oito; Proibições fora de ordem (10, 12, 11); `Log::` no passo
3 e na tabela de mutantes contra a Proibição 12; âncora quebrada desde a 1.9.0; "a skill sugere
`--parallel --tia`" (é a `feature-wiki`); gatilho da adversarial (faltava "ou Impacto 3" em dois
lugares); "host sem sub-agente: rodar em linha" × "não autorrevisar" (agora: lacuna declarada,
nunca autorrevisão); `## Ambiguidades` (nome errado da seção do `00`); contrato do adversário em
duas fontes (o agente é a fonte; o SKILL resume); `covers() → 0 %` rotulado "verificado" (é
medido); `--mutate --path=` sem ressalva; teste de arquitetura de IDs que só olhava uma direção;
"são dois comandos" sem os comandos; contagem do cabeçalho "ou removida" × `grep -c` da 3.5.1;
quem despacha o adversário e fecha achados; README dizendo "nenhuma dependência obrigatória"
contra o README raiz e o próprio SKILL; formato de retorno do agente sem seção para as sondas 6–8 e
sem ID por achado.

Abertos ⏳ — e são os mais sérios desta skill:

- **Gate de mutantes autocertificado** nos perfis mínimo e padrão sem Impacto 3: a "prova" de que
  `CT-nn` mata `M-nn` é afirmação do mesmo agente que derivou os dois. A correção é conhecida (já
  existe para lacuna convertida, :583): exigir por mutante a asserção/valor que diverge. Roteiro,
  item 7.
- **Perfil mínimo = gabarito antigo com nome novo** (1 cenário por regra, só EP, sem taxonomia,
  sem gate de camada) e **nenhuma rodada o mediu** — o protocolo diz "aplique o pipeline completo".
  Roteiro, item 11.
- **Passo 0 circular**: "área" decide os passos, e é definida no passo 2.
- **Checklist de taxonomia com 26 linhas e "não se aplica" como resposta válida** — a skill nasceu
  para matar o gabarito e está reconstruindo um; já mediu "não se aplica" apagando cobertura e
  respondeu adicionando linhas.
- **Números públicos inconsistentes**: `README:212` v1.0.0 C2 = 15/18 × `experimentos:64` rodada 1
  = 17/18; a **regressão** 16 → 15 no C1 da 1.9.0 (rodada 7) não é reportada em lugar nenhum; a
  entrada 1.9.0 do CHANGELOG mostra a tabela da 1.8.0. Roteiro, item 11 (uma tabela, uma fonte).
- **Instrumento de medição defasado**: o prompt reutilizável de `experimentos/` fixa 1.9.0 /
  3.0.0, sem camada Livewire, sem revisão adversarial, sem Impacto 3. Medir a 1.14 com o protocolo
  da 1.9 não mede a 1.14.

### 7.4 `feature-quality-gate` 1.5.1 → 1.5.2

Resolvido hoje ✅: "12 dimensões" que eram 11 na `description`, 10 num trecho do README e "3" em
outro (são 5 no perfil mínimo); modo degradado "B–K" sem a L; template "L1…L5" sem a L6; veredito
indecidível (`APROVADO` = "nenhum Blocker/Major" **e** `COM DÉBITO` = "só Minor" se sobrepunham;
agora `APROVADO` = nenhum achado aberto); reprova por percentual × "o achado é sempre um mutante"
(agora: percentual manda investigar, o achado é o mutante); fluxo e checklist mandando a skill
gravar `06` e `03` quando em sub-agente ela não grava; tabela de Entradas sem `02`, `03`, `06`
anterior, `.ai/rules`, docs e CHANGELOG que a própria skill exige; `Independência:` com três valores
no agente e dois no template; `qa-gate` × `fw-qa-gate` na mesma linha; `Browser Logs` →
`browser-logs`; detecção de dark mode cega ao Tailwind 4; `XDEBUG_MODE=` POSIX em passo Windows;
README com "v1.0.0", "futura", "10 proibições", heading `Dependências` duplicada, linha de tabela
órfã, estudo de viabilidade sem data e com citação atribuída a "doc" que as Fontes chamam de post.

Abertos ⏳:

- **Metade das dimensões é opinião sem regra** — o auditor separou: mecânicas de verdade são K1,
  L1, L2, L6, G nível 1, I "rota sem `can:`", D leitura do log, E contagem de queries; **A** (a
  razão de existir da skill, RQ → código) não tem âncora no código — a única ponte é
  `## Cobertura do Requisito` do `01` + `Origem (RQ)` do `04`; B, C, F, H, J, L3/L5 são julgamento.
  O veredito é binário sobre esse julgamento. Roteiro, item 8.
- **Falso APROVADO por omissão**: perfis mínimo e padrão pulam B, C, E–I e ainda emitem `APROVADO`;
  sem app, seis dimensões "ficam estáticas" e nada rebaixa o veredito; modo degradado deixa a A de
  fora. Falta a regra "com N dimensões não verificadas o teto é `COM DÉBITO`". Roteiro, item 8.
- **Sobreposição não declarada**: a dimensão I repete os 4 eixos do step 6.5 (`fw-revisor-diff`,
  outro `opus` cego, minutos antes); IDOR/mass assignment/N+1 são o charter do `/code-review`;
  L1/L2/L4 reexecutam os greps do step 7 num `opus` (um `haiku` faria). Das 12, só A, D, F, G, K,
  L3/L5/L6 são exclusivas. Roteiro, item 8.
- **Retorno sem delimitador**: "grava verbatim" + "`## Para o orquestrador` depois do relatório"
  → a seção vai parar dentro do `06`, ou a sessão edita o que devia gravar sem editar. Roteiro,
  item 9.
- **Regressão sem comando** (RCRCRC é tabela de "foco" sem ação); **oráculo degradado** só quando o
  `00` não existe (com `00` sem `RQ` ou derivado do PRD, nada dispara); `06` de mais de ~150 linhas
  proibido por um template que estoura com 8 achados.

### 7.5 `requirement-to-rule` 1.2.0 → 1.2.1

O auditor verificou os fatos externos na doc do Boost 13.x: `record-rule` existe (`glob`, `title`,
`note`); o índice é **regenerado** de template fixo a cada chamada e uma segunda chamada pode
**anexar** glob a uma rule existente (issue laravel/boost#1034); rules existem desde o Boost 2.5.0;
a doc diz "agentes são instruídos a consultar" o índice, não "carregamento automático"; o Cursor é
agente suportado.

Resolvido hoje ✅: `description` dizia "step 8" (o que o agente lê para decidir invocar); README
em 1.1.0 e "step 8"; `pest --arch` em 8 lugares; passo 7 mandando editar o índice à mão com o
Boost ativo, coisa que a própria skill chama de anti-padrão e diz que será sobrescrita; multi-glob
e `title` dentro do `note` inexecutáveis via `record-rule`; "3 rules" × "3 candidatos"; Cursor
listado como sem suporte; doc do Boost citada sem URL; fontes do passo 1 sem a tabela
`## Conformidade com Rules` do `03` nem o `04` (que o CHANGELOG 1.2.0 dizia ter adicionado);
dependência `laravel/boost ≥ 2.5.0` não declarada.

Abertos ⏳:

- **Gate 4 exige `search-docs` (MCP) e a `feature-wiki` roda os gates na rota `analista`, que não
  tem MCP.** Onde a esteira executa os gates, o gate mais empírico é impossível. Roteiro, item 10.
- **Dupla coleta / dupla aprovação**: o step 9 da `feature-wiki` coleta, aplica os gates e
  pergunta ("1, 2, ambos, nenhum"); a skill recebe "candidatos já aprovados" e recoleta, regateia
  e pergunta de novo ("número, todos, nenhum"). Ou a `feature-wiki` delega tudo, ou a skill vira só
  gravar + índice + commit. Roteiro, item 10.
- **Gate 3 "não-inferível" é o mais decisivo e o menos decidível**: "um agente competente, lendo o
  código ao redor, erraria?" — sem dizer quais arquivos, quantos, nem que evidência registrar.
- **Três definições de "vale virar rule"**: gate 1 mede tempo ("além desta sprint"); o gate 3
  reprova o `$table` pt-BR que a `feature-wiki` chama de "candidato natural"; o `feature-quality-gate`
  usa "recorrente entre features", critério que não existe em nenhum gate.
- **Sem poda**: a única menção a remoção é "tirar a linha do índice" — que o Boost regenera. Não há
  gatilho de revisão, expiração, dono, nem procedimento de revogação compatível com o Boost. O
  ciclo é só de crescimento; com 20 features são 60 rules e "glob estreito" vira letra morta.
- **A escada de enforcement só sugere**: ninguém é dono de escrever o `arch()`, configurar o
  PHPStan, rodar a suíte; a rule diz "enforçado em `tests/Arch/X.php`" apontando para arquivo que
  pode não existir. É exatamente o ponto do vídeo (§5.1) — regra determinística que **roda**, não
  que é descrita. Roteiro, item 4.

> **Errata (2026-09-26, release 1 do roteiro).** "Rules existem desde o Boost 2.5.0", acima, e a
> dependência "`laravel/boost ≥ 2.5.0`" deste parágrafo e dos itens 1 e 2 do roteiro (§8, "Boost
> 2.5+" e "`laravel/boost ≥ 2.5`") estão errados: Project Rules e a tool MCP `record-rule` entraram
> na **v2.4.12** do laravel/boost (PR #852; fonte: o código e o CHANGELOG do laravel/boost). As
> skills da release 1 declaram `laravel/boost>=2.4.12`. O texto acima fica como foi escrito.

### 7.6 Os cinco sub-agentes

| Agente | Frontmatter | Autossuficiente | Cegueira | Ferramenta × promessa | Retorno auditável |
|---|---|---|---|---|---|
| `fw-revisor-diff` | ✅ (`tools` explícito + `disallowedTools`, redundante e inofensivo) | ⚠️ precisa que o orquestrador cole a tabela de eixos; o SKILL não diz que cola | ⚠️ prompt: recebe o path do `02` e pode abrir `01`/`03` na mesma pasta — ✅ hoje ganhou a proibição explícita | ⚠️ `Bash` liberado (`sed -i`, `git checkout` só por prompt) | ✅ |
| `fw-executor-ct` | ✅ (sem `tools`: herda tudo, conforme "sob contrato") | ✅ o melhor dos cinco (path, IDs, arquivo-alvo, versões, cwd) | n/a (não é agente de julgamento) | ✅ "nunca toca `app/`" é prompt, coerente com "sob contrato" | ✅ exige saída literal do `pest` |
| `fw-executor-ctb` | ✅ | ❌ era o único sem bloco "você recebe" — ✅ ganhou hoje | n/a; recebe o `01` (Superfície de UI) — o README raiz generaliza "cegos" para todos | ✅ | ❌ não exigia saída literal nem tinha o caminho do blocker — ✅ ganhou hoje |
| `fw-adversario-ct` | ✅ (`Read, Grep, Glob`, sem Bash) | ✅ | ⚠️ prompt: `Read`/`Glob` sem restrição de path; README diz "vem da construção" — **falso** | ✅ sem Bash bastam as 8 tarefas; o teto "no model" só é sabível se o `00` declarar | ⚠️ 5 seções sem lugar para as sondas 6–8 e sem ID por achado — ✅ ganhou hoje; ⏳ "5 implementações" fixas viram gabarito; o caso de 2026-09-21 no prompt enviesa todo despacho |
| `fw-qa-gate` | ✅ (sem `tools` para herdar MCP; a diferença para o `fw-revisor-diff`, que tem `tools` e **não** herda MCP, não estava documentada) | ⚠️ a base do PR não era insumo — ✅ ganhou hoje | ⚠️ "não recebe a conversa" é verdade nominal: lê o `03` (Despachos, Desvios, Retrospectiva) | ❌ `Bash` liberado e o arquivo diz "mecânico, não promessa" | ❌ sem delimitador entre o `06` e `## Para o orquestrador` |

Nenhum dos cinco declara `permissionMode` nem `maxTurns`; o loop "3 iterações" do CT-B não tem teto
mecânico. E nenhum é executável fora do Claude Code: os agentes carregam a cegueira e a restrição de
ferramenta, e o fallback `general-purpose` + `model` (documentado e testado em campo) perde a
restrição, não a cegueira.

### 7.7 Consistência cruzada — o que o conjunto contava de diferente

Além de T1, T2 e T11: o README raiz dizia "as **quatro** skills são encadeadas pelo `00`" (a
`requirement-to-rule` lê `01`/`02`/`03`); o README da `feature-test-design` dizia "nenhuma
dependência obrigatória" enquanto o raiz dizia "isolada não funciona"; nenhuma skill declara versão
mínima das outras além de "`feature-wiki` ≥ 2.10.0" — mas a `feature-wiki` 3.5 depende de
`@obsoleto`, do helper `{entidade}Em` e do `fw-adversario-ct` (`feature-test-design` ≥ 1.14) e da
checagem L6 (`feature-quality-gate` ≥ 1.5); a Opção 3 de instalação (`/plugin marketplace add`) não
tem manifesto no repositório; o exemplo de frontmatter do README raiz ensinava `name: Form Requests
Padronizados`, violando o spec; três versões do CHANGELOG (3.4.0, 1.13.0, 1.4.0) não têm tag, e só a
primeira tem justificativa; `experimentos/README.md` não listava as rodadas 6–13, apontava para
`PROMPT-AGENTE.md` (o arquivo é `PROMPT-BRACO.md`), pulava a rodada 2 e falava em "7 rodadas" com
13 na tabela; `estudos/` era invisível no README raiz. Tudo ✅, exceto as versões mínimas cruzadas
(⏳ roteiro, item 2) e as tags ausentes (nota adicionada na convenção do CHANGELOG).

---

## 8. Roteiro

Ordenado por **alavanca ÷ custo**, não por gravidade isolada. Cada item diz o que é (mudança de
texto, de estrutura ou de desenho), a skill, e como se prova que ficou pronto. Nada aqui foi
feito hoje além do que está marcado ✅ em §7.

| # | O quê | Skill(s) | Tipo | Pronto quando | Custo |
|---|---|---|---|---|---|
| 1 | **Conformidade ao spec**: `version` → `metadata.version`; `description` ≤ 1024 (o quê + quando + palavras-chave; o resto vai ao README); `compatibility` (Boost 2.5+, Pest 5, sub-agentes opcionais); `license: MIT`; job de CI com `npx skills-ref validate` nas quatro | as 4 | texto | validador verde nas 4; tamanho das 4 `description` somadas ≤ 4 k chars | horas |
| 2 | **README = por quê / quando / limites / dependências com versão mínima** — tirar os ~160 + ~100 + ~150 linhas de procedimento duplicado; declarar `feature-test-design ≥ 1.14`, `feature-quality-gate ≥ 1.5`, `laravel/boost ≥ 2.5` | `requirement-to-rule`, `feature-quality-gate`, `feature-wiki` | texto | `grep` de qualquer regra do SKILL não acha cópia no README | dias |
| 3 | **`references/` com uma fonte por tema** — `feature-wiki`: templates 00–03, padrão de log, Pest 5, roteamento/despacho, citações, Playwright, Ponytail/Caveman, casos medidos; `feature-test-design`: as 14 faixas do relatório (técnicas por regra, taxonomia, Gherkin, templates 04/05, mutation, camadas). Os fatos do `pest-plugin-browser` passam a existir em **um** arquivo, referenciado pelos 4 lugares que hoje os copiam. Corpo ≤ 500 linhas com **todos** os gates e proibições; cada step diz qual referência abrir; checklist final ganha "referências abertas: …" | `feature-wiki`, `feature-test-design` | estrutura | **uma rodada do protocolo de `experimentos/` antes e depois**, mesmo kit, mesmo juiz; sem regressão em C1/C2 | dias + rodada |
| 4 | **`scripts/`** — os greps do step 7 (checkbox sem evidência, RQ sem passo, IDs de CT nos dois sentidos, citação `arquivo:símbolo:linha`), a detecção de dark mode, K1, L1/L2/L6 do gate, o lançador `.cmd`; a `requirement-to-rule` passa a **gerar** o `arch()`/config quando a rule é mecânica, e roda a suíte para provar que pega | `feature-wiki`, `feature-quality-gate`, `requirement-to-rule` | estrutura | cada script tem saída vazia = OK e exemplo de falha; o `fw-qa-gate` chama scripts, não reescreve greps | dias |
| 5 | **Costuras de teste declaradas** — seção `## Costuras` no `04`: uma linha por grupo de CT (Pest feature HTTP · componente Livewire · browser · unit de regra), existente ou nova, confirmada com o usuário; o gate do `05` vira consequência | `feature-test-design` | desenho | toda linha da taxonomia aponta para uma costura; o `05` só existe se uma costura for "browser" | horas |
| 6 | **Ordem e regimes do `00`/`01`**: step 6 (Ponytail sobre `01`/`02`) antes da derivação do `04`, renumerado; Adendo só para pedido do solicitante (fonte + verbatim); achado de revisão vira **premissa** (`P-nn`, seção própria no `00`, regime revisável), esquema definido; path e número proibidos no `00` e no `02`, permitidos no `01` porque o step 7 cobre | `feature-wiki` | desenho | checklist com uma ordem só; `P-nn` no template | horas |
| 7 | **Gate de mutantes falsificável em todo perfil** — por mutante, a asserção/valor do CT que diverge (como já se exige para lacuna convertida); teto "5 implementações" do adversário vira piso; o caso de 2026-09-21 sai do prompt do agente para `references/casos-medidos.md`; medir o perfil **mínimo** numa rodada | `feature-test-design`, `fw-adversario-ct` | desenho | rodada com perfil mínimo no protocolo; coluna "asserção que mata" obrigatória na tabela de mutantes | dias + rodada |
| 8 | **Veredito do gate com teto por cobertura** — "com N dimensões não verificadas (perfil, app ausente, oráculo degradado) o teto é `APROVADO COM DÉBITO`"; dimensão I deixa de repetir os 4 eixos do 6.5 (referencia o `03`); L1/L2/L4 vão para `mecânico` (`haiku`) e o `opus` recebe só o resultado; A ganha âncora mecânica: `Cobertura do Requisito` (RQ → passo) × `Origem (RQ)` do `04` × `git diff` por passo | `feature-quality-gate` | desenho | tabela "mecânica × julgamento" no SKILL, uma linha por dimensão; custo do gate medido antes/depois em `## Despachos` | dias |
| 9 | **Cegueira e não-edição por construção** — o orquestrador copia só o que o agente pode ver para uma pasta temporária e passa esse path (ou hook `PreToolUse` negando `01-*`, `03-*`, `app/` para `fw-revisor-diff`/`fw-adversario-ct`); `fw-qa-gate` e `fw-revisor-diff` devolvem `git status --porcelain` antes/depois, ou `Bash` entra em `disallowedTools` com os comandos necessários em `scripts/`; retorno do `fw-qa-gate` com delimitadores (`<<<06` … `>>>06`) e `## Para o orquestrador` **fora**; `maxTurns` nos executores; o README raiz para de dizer "cegueira vem da construção" até que venha | 5 agentes, `feature-wiki` | desenho | teste: despachar o `fw-revisor-diff` com o `01` na pasta e pedir que o cite — precisa falhar | dias |
| 10 | **Step 9 com um dono e MCP** — a `feature-wiki` delega a coleta e os gates à `requirement-to-rule` (apaga o bloco duplicado) **ou** a skill vira só gravar + índice + commit; a rota que roda o gate 4 tem MCP (sessão principal ou `qa-gate`), nunca `analista`; gate 3 ganha evidência mínima (N arquivos irmãos por `ls`/`grep`, citação); uma definição de "vale rule" (tempo **e** não-inferível **e** recorrência declarada); procedimento de **poda** compatível com o Boost (rule `n.a.`/`violada` em N features → atualizar/remover); `Explore`/`SendMessage` com fallback declarado | `feature-wiki`, `requirement-to-rule` | desenho | um prompt de aprovação, não dois; primeira execução real registrada em `experimentos/` | dias |
| 11 | **Uma tabela de medição, uma fonte** — `experimentos/README.md` é a única tabela; READMEs linkam; a regressão 16 → 15 da 1.9.0 reportada; `README:212` × `experimentos:64` resolvido; o prompt reutilizável atualizado para o pipeline 1.14 (camada Livewire, adversarial, Impacto 3); a `requirement-to-rule` e o perfil mínimo ganham a primeira rodada | `experimentos/`, READMEs | texto + medição | nenhum número aparece em dois lugares com valores diferentes | dias |
| 12 | **`feature-tickets`** (§4.3) — ticket = `RQ` + `CT` + passos do `01` + bloqueio + status; `RQ` sem ticket é achado; construtor recebe só a fatia; `wikis/specs/INDEX.md` como quadro; espelho opcional no tracker | nova skill + hook na `feature-wiki` | nova | feature de 2 sessões entregue por tickets, com o gate no fim cruzando a coluna *ticket* | semana |
| 13 | **Entrevista em três raias** (§2.3, §2.5) — formato ❓/➡️ em rodadas pela fronteira; raia de requisito com `RQ` aberta bloqueando passo do `01`; três portões para ADR no `02`; glossário do projeto fora da wiki, lido pela `feature-test-design` e pela dimensão L | `feature-wiki`, `feature-test-design`, `feature-quality-gate` | desenho | `RQ` aberta sem resposta ⇒ passo marcado `bloqueado`; `02` com zero ADR é resultado válido | dias |
| 14 | **Expand–contract para refatoração larga** — a `feature-wiki` deixa de "sair de cena" em refactor; a `feature-tickets` sequencia expand → migrate em lotes → contract | `feature-tickets` | desenho | — | baixa prioridade |

**O que não entra** (decidido neste estudo): user stories geradas; spec publicada fora do
repositório como artefato primário; `ready-for-agent` automática; "ideal = 1 costura"; entrevista
sem oráculo ou no lugar do solicitante; `grill-me` sem repositório; critério de aceite em prosa por
ticket quando o `04` existe.

**Ordem sugerida**: 1 → 11 → 2 → 3 (com rodada) → 4 → 9 → 7 → 8 → 10 → 6 → 5 → 13 → 12 → 14. Os
quatro primeiros são texto e medição; nada de desenho muda antes de a base estar limpa e medida.

---

## Fontes

- Agent Skills — Specification: https://agentskills.io/specification (lida 2026-09-26; validador `skills-ref` via `npx skills-ref validate`)
- `mattpocock/skills` — `skills/engineering/to-spec/SKILL.md`, `to-tickets/SKILL.md`, `implement/SKILL.md`, `setup-matt-pocock-skills/SKILL.md`, `wayfinder/SKILL.md` (lidos via API do GitHub em 2026-09-26)
- aihero.dev — *The /to-spec skill* (https://www.aihero.dev/skills-to-spec) e *The /to-tickets skill* (https://www.aihero.dev/skills-to-tickets)
- Vídeo *"meu fluxo de trabalho com IA"* — https://www.youtube.com/watch?v=1bmO4BaVclY (transcrição fornecida pelo usuário)
- Estudo anterior: [`2026-09-04-spdd-x-coletanea.md`](2026-09-04-spdd-x-coletanea.md) (§3.1 montante, §13.2 motor × hospedeiro × perfil de stack)
- Medições desta coletânea: `README.md` raiz (*Validado em campo*, *Por que a derivação do teste virou skill própria*), `experimentos/README.md`
