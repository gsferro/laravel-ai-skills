# Changelog

Histórico de evolução das skills desta coletânea.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); cada skill segue [Semantic Versioning](https://semver.org/lang/pt-BR/) de forma **independente**.

## Skills e versões atuais

| Skill | Versão | Tag |
|---|---|---|
| `feature-wiki` | 3.6.0 | `feature-wiki-v3.6.0` |
| `feature-test-design` | 1.15.0 | `feature-test-design-v1.15.0` |
| `feature-quality-gate` | 1.6.0 | `feature-quality-gate-v1.6.0` |
| `requirement-to-rule` | 1.3.0 | `requirement-to-rule-v1.3.0` |

**Onde a versão está, desde a release 1 do roteiro (2026-09-26).** O frontmatter segue o
[spec Agent Skills](https://agentskills.io/specification): a versão saiu do topo (`version:`) e
foi para `metadata.version`, indentada. Quem conferia com `grep '^version:'` passa a conferir
`metadata.version`:

```bash
grep -Hn '^[[:space:]]*version:' .ai/skills/*/SKILL.md
```

```powershell
Select-String -Path .ai\skills\*\SKILL.md -Pattern '^\s*version:'
```

As contagens de linhas de corpo citadas nas entradas da release 1 são as linhas do `SKILL.md`
depois do fechamento do frontmatter: `awk '/^---$/ && ++n==2 {next} n>=2' SKILL.md | wc -l`. Os
tamanhos de `description` são os do valor que o YAML entrega (a quebra final do bloco `>` conta),
o mesmo que o `skills-ref validate` compara com o limite de 1024.

## Convenção de tags

A partir da v2.7.0 da `feature-wiki`, as tags são **namespaced por skill**, porque a coletânea passou a ter mais de uma skill com versionamento próprio:

```
feature-wiki-v2.7.0
requirement-to-rule-v1.0.0
```

**Tags legadas** (`v1.0.0`, `v2.0.0`, `v2.1.0`, `v2.2.0`, `v2.4.0`) referem-se **exclusivamente à `feature-wiki`**, quando ela era a única skill do repositório. Elas foram preservadas; nada foi reescrito.

| Versão | Tag | Situação |
|---|---|---|
| 1.0.0 – 2.4.0 | `v1.0.0` … `v2.4.0` | série legada (só `feature-wiki`) |
| 2.3.0 | — | liberada sem tag |
| 2.5.0, 2.6.0 | — | versões intermediárias, nunca commitadas isoladamente — consolidadas na 2.7.0 |
| 2.7.0 em diante | `feature-wiki-vX.Y.Z` | série namespaced |
| `feature-wiki` 3.4.0 | — | liberada sem tag — consolidada na 3.5.0 (ver nota na entrada 3.5.0) |
| `feature-test-design` 1.13.0 · `feature-quality-gate` 1.4.0 | — | liberadas sem tag (o mesmo dia da versão seguinte); as entradas existem no CHANGELOG |
| patches de 2026-09-26 (3.5.2 · 1.14.1 · 1.5.2 · 1.2.1) | criadas | tag por skill, como as demais |
| release 1 do roteiro, 2026-09-26 (3.6.0 · 1.15.0 · 1.6.0 · 1.3.0) | a criar | tag por skill, no commit da release |

## Números de medição

A tabela única de medição da coletânea é [`experimentos/README.md`](experimentos/README.md#histórico).
As tabelas nas entradas abaixo são o registro do dia em que cada versão saiu e não são reescritas.
Onde divergem da tabela única, as notas de correção de 2026-09-26 dizem o que vale.

---

# feature-wiki

Cria a estrutura de documentação de uma feature **antes** de implementá-la: requisito bruto, PRD, ADR, tracking de progresso e padrão de log.

## [3.6.0] — 2026-09-26

Release 1 do roteiro do estudo
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md)
(§8, itens 1, 2, 3 e 11), "base limpa": **só empacotamento**. Nenhum gate, regra, template ou step
mudou. O único contrato de agente tocado é o do `fw-executor-ctb`, que troca a cópia dos fatos do
`pest-plugin-browser` por um ponteiro para a fonte única e para quando ela não existe. Por isso a
release é medível sozinha contra `feature-wiki-v3.5.2`.

O corpo do `SKILL.md` foi de 2.410 para **1.285 linhas**. O alvo do spec (< 500) **não foi
atingido**, e não se atinge sem tirar obrigação do corpo: 1.285 é o piso com todos os gates, as
obrigações, o que é NUNCA ou proibido, os critérios de parada, os steps 0–9 e o checklist no
próprio `SKILL.md`. Os blocos que seguram o piso são normativos: execução e delegação, step 3
(captura verbatim, lista obrigatória de verificações, Superfície Livewire), step 6.5, step 7, os obrigatórios dos
arquivos `00`–`03` e o checklist final. Resumir essas linhas seria mudar regra, e a release 1
não muda regra.

**Não medido**: a rodada que compara com a tag anterior (`feature-wiki-v3.5.2` +
`feature-test-design-v1.14.1`) está pendente em
[`experimentos/README.md`](experimentos/README.md#rodadas-pendentes) (Rodadas pendentes, item a).

### Alterado

- **Frontmatter no formato do [spec Agent Skills](https://agentskills.io/specification).**
  `version` sai do topo e vira `metadata.version: "3.6.0"`: quem conferia com `grep '^version:'`
  passa a conferir `metadata.version` (comando em [Skills e versões atuais](#skills-e-versões-atuais)).
  Entram `license: MIT` e uma `compatibility` com as exigências reais: projeto Laravel com git;
  Laravel Boost com MCP **recomendado** (`search-docs` no step 3, `record-rule` a partir do Boost
  2.4.12 no step 9); Pest 4 ou 5, assumindo o 5 (`--tia` e `--mutate` na Verificação Final,
  `--agent` na implementação) e caindo para `--filter` no 4; sub-agentes e plugins Ponytail e
  Caveman opcionais, com a degradação que o `SKILL.md` já declarava. `metadata.requires` passa a
  ser `feature-test-design>=1.15.0; feature-quality-gate>=1.5.0; laravel/boost>=2.4.12`.
  `npx skills-ref validate` passa
- **`description` de 3.636 para 999 caracteres**: o quê, quando e palavras-chave. Continuam o
  gatilho "Invoque SEMPRE…", o "de novo quando o pedido crescer no meio da implementação (vira
  Adendo no 00)" e a revisão do diff "assim que os testes passam". O que era release note foi para
  o README, e cada regra que só existia na `description` foi conferida no corpo
- **Corpo do `SKILL.md` de 2.410 para 1.285 linhas, com 15 arquivos em `references/`**, um tema
  por arquivo: templates `00`–`03`, padrão de log, pesquisa do step 3, roteamento e despacho,
  delegação dos casos de teste, Playwright MCP, Pest 5, citações de código, candidatos a rule,
  Ponytail/Caveman, estrutura criada e casos medidos. O corpo guarda linhas verbatim da 3.5.2; só
  os ponteiros foram reescritos. Continuam nele, entre outros, a auditoria do retorno dos
  sub-agentes (tem o gate que reprova retorno); do padrão de log, o "Por que este padrão", as 9
  regras de escrita e a trait `UnicoLogging`; e o vermelho separado por rota — backend (`(b)` do
  `fw-executor-ct` roteado Adendo → CT → correção) e CT-B (3 iterações → blocker no `03`)
- **Cada step que depende de uma reference manda lê-la antes da ação** ("Antes de X, leia
  `references/Y.md`"), também sem MCP e em host sem sub-agente; o pré-6.5 manda ler os greps de
  `references/pesquisa-step-3.md`. O índice lista as references com o step em que são lidas, e o
  checklist final ganhou o item *referências lidas: arquivo (step N)*, com o mínimo por step
- **Casos medidos fora do procedimento.** Todo "caso real", "medido em 2026-09-xx" e o *Validado
  em campo* foram para `references/casos-medidos.md`, com ponteiro curto no ponto da regra.
  Quando caso e regra estavam na mesma frase, a frase foi inteira, e o arquivo avisa que a regra
  em vigor é a do corpo
- **Fatos do `pest-plugin-browser` com fonte única**:
  `{skills}/feature-test-design/references/pest-plugin-browser.md` (entrada `feature-test-design`
  1.15.0). O `SKILL.md`, o README e o `fw-executor-ctb` viram ponteiro. No step 3 ficam, verbatim,
  os dois fatos duros: o plugin sobe o próprio servidor, sem `APP_URL`; e `npm run build` é
  pré-requisito (sem ele, `ViteException`)
- **`fw-executor-ctb` lê a fonte única antes do primeiro teste.** Se `pest-plugin-browser.md` não
  existir em nenhum dos três diretórios de `{skills}`, para e devolve *"pest-plugin-browser.md não
  encontrado"*, sem escrever teste. Com a `feature-test-design` abaixo da 1.15.0, o agente não
  escreve CT-B
- **Caminho para arquivo de outra skill usa `{skills}/<skill>/…`**, definido no Glossário:
  `.ai/skills/`, `.claude/skills/` ou `~/.claude/skills/`, o primeiro que existir
- **README reescrito** como por quê, quando, dependências, instalação, organização e limites (615
  → 354 linhas). Na tabela de dependências, a versão de `metadata.requires` é o mínimo **quando a
  dependência está presente**: nenhuma é obrigatória além de Laravel com git, exceto a
  `feature-quality-gate`, sem a qual o PR não abre. A `requirement-to-rule` aparece com mínimo
  1.1.0 (o `search-docs` do gate 4) e fica fora de `metadata.requires`, porque o step 9 só a
  invoca depois do "sim" do usuário. Saiu o procedimento que repetia o `SKILL.md` (Playwright
  MCP, `search-docs`, contrato dos CT-B, Pest 5, fatos do plugin, tabelas de campo)
- **A auditoria das 9 wikis e 125 casos que motivou a delegação do `04` saiu da `feature-wiki`.**
  A fonte única é o [README da `feature-test-design`](.ai/skills/feature-test-design/README.md#o-que-a-auditoria-mediu);
  as rodadas do protocolo ficam em [`experimentos/README.md`](experimentos/README.md#histórico)

### Corrigido

- **Versão mínima do Boost: 2.4.12**, a versão em que nasceram as Project Rules e a tool
  `record-rule` usada no step 9 (laravel/boost PR #852). A coletânea citava 2.5.0 — na entrada
  `requirement-to-rule` 1.2.1 e no estudo, §7.5 e §8; os dois ganharam errata datada
- README: o bloco PowerShell de instalação dos agentes copiava `.ai\skills\*` para `.claude\skills\`
  sem condição, ao contrário do bloco bash logo acima e do README da coletânea: com `boost.json`, o
  `boost:update` cria `.claude/skills/<skill>` como symlink e a cópia por cima falha. Fica igual ao
  bash (só agentes), com link para os dois casos em *Como Instalar no Claude Code*
- README: os links para `experimentos/` viram URL absoluta do repositório (o `boost:add-skill` copia
  o README para `.ai/skills/<skill>/` do projeto, onde `../../../` não leva ao repositório)
- `references/ponytail-caveman.md` mandava `php artisan boost:update` logo depois do `add-skill`,
  sem condição. Com `boost.json` o `add-skill` já o chama; sem `boost.json` ele falha. Vira
  comentário: só se o `add-skill` terminou com erro


## [3.5.2] — 2026-09-26

Patch de documentação e de coerência, sem step novo. Nasce da auditoria interna consolidada em
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md) (§7.2) — cinco auditores cegos, um por skill e um de consistência cruzada.

### Corrigido

- **Log não vira CT** (regra da 3.5.0) ainda estava contradita em duas linhas ("Incluir CTs de log
  no `04`" e a legenda da árvore final) — removidas
- `--parallel` com browser era **proibido** num lugar e **condicional** noutro (e no README) — só a
  proibição fica, alinhada à `feature-test-design` e ao `fw-executor-ctb`
- Rotas `mecânico` e `analista` têm "leitura + Bash" e o mapa por step mandava "espelhar 01 → 03",
  "derivar o 04/05", "corrigir a wiki" — agora, como a rota `qa-gate`, **devolvem texto e a sessão
  grava**
- Contrato de delegação à `feature-test-design` não entregava o `02` (`## Superfície Livewire`), que
  ela declara obrigatório e este próprio arquivo dizia ser "entrada obrigatória do step 4"
- Step 8 "pode pular" × checklist "`06` ausente é blocker do PR": ao pular, grava-se um `06` mínimo
  com veredito `NÃO APLICÁVEL`
- Duas âncoras do índice quebradas (Padrão de Log, Arquivo 02); "após escrever os 4 arquivos" (são
  5 desde a 2.10.0); `APP_URL` no checklist contra "nada de `APP_URL` a configurar"; rota
  `adversário-ct` sem o "sem Bash" do frontmatter real
- `tests/**/*{Feature}*.php` no `diff` de IDs não funciona sem `globstar` (o `**` vira `*`) —
  trocado por `find`; `--testsuite=Browser` × `tests/Browser --filter` unificados; `pest --arch`
  (não é flag) → `arch()`; `Browser Logs` → `browser-logs`
- `{base}` era usado cinco vezes sem definição — definido no Glossário (branch de destino do PR,
  registrada no cabeçalho do `03`)
- Citação do arXiv 2607.22883 corrigida (318 métodos focais / 233 defeitos, ≈1,4×, ≈1,5×, "mitiga")
  no SKILL e no README
- "Rules carregadas automaticamente por glob" → o Boost instrui o agente a consultar o índice; gate
  4 dos candidatos a rule agora cita o `search-docs`, como a `requirement-to-rule` exige
- Lista de "skills disponíveis para referenciar no PRD" não dizia que são skills do **Laravel
  Boost**, não desta coletânea
- README: degradações de Ponytail e `feature-quality-gate` diziam "step 6 fica manual" / "step 8 é
  pulado" contra o SKILL (obrigatórios); gate do `05` descrito de dois jeitos em 10 linhas; `wait()`
  "só isso existe" × "nunca use"; árvore final sem `00` e `06`; "Pest 3, 4 ou 5" (os comandos de
  Verificação Final assumem Pest 5); bloco PowerShell com bytes de controle (`\a` → BEL, `\f` → FF)
  que não rodava
- `fw-executor-ct`: dizia ao mesmo tempo "não crie o helper em `tests/Pest.php`" e "o helper vive
  em `tests/Pest.php` e é do lote D0" — o D0 cria; os outros devolvem `bloqueado`
- `fw-executor-ctb`: único agente sem bloco "você recebe do orquestrador", sem exigência de saída
  literal do `pest` e sem o caminho do blocker após 3 iterações — os três acrescentados
- `fw-revisor-diff`: proibição explícita de abrir `01-*.md`/`03-*.md` da pasta da wiki mesmo tendo
  o path do `02` (a cegueira era só "recuse o que receber")

### Adicionado

- Step 6 declara a degradação sem o plugin Ponytail (passe manual registrado no `03`)


## [3.5.1] — 2026-09-22

Número escrito à mão envelhece **dentro do próprio ciclo**, e a cópia dele em outro arquivo
sobrevive ao gate. Relatado por uma sessão que rodou a 3.5.0 num projeto real no mesmo dia.

### Adicionado

- **Step 7, item 5 — todo número da wiki é derivado por comando, e procurado na wiki inteira
  quando muda.** A regra de `grep -c` existia só para o `03`; passa a valer para `01`, `02` e `04`
  (contagem de CTs, regras, mutantes, permissions, linhas de varredura, total do cabeçalho). E o
  ponto cego nomeado: quando um achado corrige um número, a correção vai para o arquivo citado e a
  cópia em outro arquivo fica — fechar exige `grep -rn "{valor antigo}"` na pasta da wiki.
  Medido três vezes numa mesma wiki: nove citações `arquivo:linha` defasadas, uma varredura colada
  na `## Superfície Livewire` que o código já contradizia, e uma contagem corrigida no `01` que
  continuou errada na ADR do `02` — **a defasagem sobreviveu ao gate que existia para pegá-la**
- Checklist: contagens da wiki inteira por `grep -c`; número corrigido procurado na wiki inteira

### Alterado

- Itens 5–11 do step 7 renumerados para 6–12

## [3.5.0] — 2026-09-22

A 3.4.0 desenhou o roteamento por modelo e por cegueira; a 3.5.0 é o que uma **feature completa**
ensinou ao rodá-lo de ponta a ponta (fluxo de aprovação de compra em Laravel 13 / Filament 5,
`demo-wiki`, 2026-09-21: 18 `RQ`, 28 premissas, 79 CTs, 182 testes, 14 commits, 48 despachos,
~4,6 M tokens de sub-agente; quality gate ciclo 1 `REPROVADO → especificação` com 8 achados). As
duas versões saem juntas: nada da 3.4.0 chegou a ser publicado antes da medição.

### O que a medição confirmou (vira regra dura, com o caso registrado no `SKILL.md`)

| Confirmado | Evidência |
|---|---|
| **Cegueira vale mais que modelo** | adversário cego (`opus`) achou 5 implementações erradas sobre 60 CTs derivados por outro `opus`, e uma regra que eram duas; o 6.5 cego produziu 14 achados que mudaram código, `00` e `04` |
| **O juiz cego acusa a própria sessão** | o step 8 pegou duas alegações falsas da `## Verificação Final` — *"88 citações ok"* sem comando e *"sem PCOV / mutate não instalado"* sem `php -m`. Eram do orquestrador, não do código |
| **O juiz cego faz a pergunta que ninguém fez** | acumulação gestor × diretor na mesma pessoa; visibilidade de quem já decidiu; link do e-mail em 404 |
| **6.5 antes do 7** | os 14 achados deslocaram citações, IDs e frases de ADR; o 7 teria sido refeito inteiro |
| **Contrato a/b/c do executor** | 5 lotes; todo vermelho que sobrou era defeito real (CT-58, CT-59) |
| **Auditoria do retorno, sobretudo com `haiku`** | 3 de 8 retornos `haiku` com defeito; 1 de 5 itens feitos num lote misto, 3 reportados como feitos |

### Adicionado

- **`### Validado em campo`** na seção *Execução e Delegação*: a tabela acima, com o caso de cada
  linha, e a lista do que a medição **desmentiu** com o ponteiro para a correção
- **Rota `executor-ct`** e o agente **`agents/fw-executor-ct.md`** (`sonnet`): o construtor de
  testes Pest de backend a partir do Gherkin do `04`, generalização do contrato dos CT-B — fonte é
  o `04`, lê `app/` só para nomes, fixture por transições reais, classifica cada vermelho em
  a/b/c, **nunca toca `app/`**, saída em formato fixo, reporta "estado parcial" se interrompido.
  Seção nova **`### Contrato do construtor de testes (executor-ct)`**
- **Pré-requisitos do lote 6.5**: a sessão roda no repositório do projeto (o `/code-review` não
  alcança outro diretório; substituto é `analista` cego com degradação declarada) e a
  `## Superfície Livewire` do `02` foi **re-varrida sobre o código final** — a tabela do
  planejamento envelhece (negava superfície de vendor; as Pages herdavam trait com 4 métodos
  `$wire.` que recebem índice de array)
- **Ordem step 6 × step 4**: Ponytail sobre `01`/`02` **antes** de invocar a `feature-test-design`;
  se o `04` já existe quando um corte muda a `## Superfície de UI`, **re-sincronizar** no mesmo
  passo (CT atingido vira `@obsoleto` ou é re-derivado). Caso: CT-42 órfão de um filtro cortado,
  descoberto só no `diff` de IDs do step 7
- **Terceira saída da falsificabilidade**: *"não falsificável nesta pilha — guarda mantida, dívida
  declarada"* (SQLite ignora `VARCHAR(255)` e `RESTRICT`). 3 de 5 CTs novos caíram nela; lida como
  regra absoluta, *"decoração"* mandaria apagar guardas corretas
- **Sinais que reprovam o retorno antes da amostragem**: número sem comando; `git diff --stat`
  como prova de arquivo untracked; "não encontrado/não instalado" sem prova negativa; "sem
  ocorrências" em grep com FQCN; conclusão de custo sob paginação. **Auditoria reprovada é linha
  do quadro**; interrupção (429) → `git status` antes de retomar o **mesmo** agente por
  `SendMessage`
- **Regras da rota `mecânico`**: um item por despacho (lote misto → `construtor`); `grep -F` para
  FQCN; `Explore` só para feature grande (139 k tokens contra 40–60 k por `haiku`)
- **Verificação de agentes antes do primeiro despacho** (`ls .claude/agents/fw-*.md`): eles só
  carregam do diretório onde a sessão foi aberta; o fallback `general-purpose`/{model} vai na
  coluna *Modelo* do quadro. Segurou uma feature inteira
- **Tier abstrato** (econômico / intermediário / topo) como conceito portável para outro provedor;
  o alias Claude é a implementação
- **Perguntas obrigatórias do `00`** (comentário do template *Ambiguidades*): acumulação de papéis
  **par a par**; participante histórico × recorte de visibilidade; destino do link de toda
  notificação; teto de todo texto livre — as quatro que o juiz cego fez e a sessão não
- **Pest 5 — duas armadilhas medidas**: `--testsuite=A --testsuite=B` só honra o último; e
  **`pest --mutate` dá 100 % falso no Windows** — o plugin relança `argv[0]` (script sh) que o
  `cmd` não executa, e conta saída não-zero como mutante morto (*206 mutantes em 3 s*). Regra:
  score só vale com `Duration` plausível e lista de sobreviventes; lançador `.cmd` poliglota
  documentado. Medido de verdade: 206 mutantes, 196 mortos, 7 timeout, 3 sobreviventes, 98,54 %
  em 594 s
- **Templates do `01`/`03`**: baseline da suíte em `{base}` antes do primeiro commit (falhas
  pré-existentes por nome); linha do `--mutate` com score, duração e sobreviventes; custo medido
  com N acima da página; falsificabilidade com a terceira saída; e o comentário do `03` passa a
  exigir **o comando** ao lado de todo número e **a prova negativa** ao lado de toda degradação
- **Filosofia de Implementação**: model novo declara `$table` quando o nome não é o plural inglês
  inferido (nasceu como defeito: `centro_custos`)

### Alterado

- **Log não vira CT.** O checklist pedia *"CTs de log incluídos no `04`"* e a
  `feature-test-design` deriva só do `00` — conflito medido (helper de log morto, zero CT de log,
  17 logs conferidos pela dimensão D do gate). *Testando Logs em Pest* vira técnica opcional; quem
  confere log é a dimensão D
- Mapa de roteamento: linha de teste Pest passa de `construtor` para `executor-ct`; linhas novas
  para re-sincronização do `04` (step 6) e re-varredura da Superfície Livewire (pré-6.5)
- Checklist Final: +12 itens (perguntas obrigatórias do `00`, baseline, `$table`, ordem 6 × 4,
  Superfície re-varrida, número com comando, `--mutate` plausível, `ls .claude/agents`, `mecânico`
  um item, retorno reprovado registrado, falsificabilidade com terceira saída, log fora do `04`)

## [3.4.0] — 2026-09-21

O gate do diff muda de lugar, e a skill aprende a despachar. Duas motivações, ambas de uso real:

1. **O `/code-review` continua achando defeito** mesmo com a skill na 3.3.0 e tudo cumprido. Isso
   não é falha dos outros gates — é o que a medição de 2026-09-17 já dizia: ele é o único que lê
   o diff atrás de defeito de correção. Mas ele rodava como **step 7.5, depois da reconciliação**,
   e cada achado confirmado (Adendo no `00` → CT no `04` → correção) invalidava citações, IDs de CT
   e frases de doc que o step 7 tinha acabado de conferir. Reconciliar antes de revisar era
   reconciliar duas vezes.
2. **O modelo de roteamento do PO** — sessão principal orquestra, decide e audita; construção e
   volume vão para sub-agente com o modelo roteado pela complexidade (`haiku` mecânico, `sonnet`
   construtor, `opus` analista); paralelo é o padrão; todo disparo é visível num quadro; nunca
   `general-purpose` sem `model`. A coletânea já tinha três lugares que pediam *"por quem não
   implementou / não derivou / não escreveu"* e os executava **na mesma sessão**. Sub-agente
   resolve os dois problemas de uma vez: custo e independência.

### Onde o `/code-review` roda agora, e por quê

| Antes (3.3.0) | Agora (3.4.0) | Motivo |
|---|---|---|
| step **7.5**, depois da reconciliação (7) e antes do quality gate (8) | step **6.5**, logo após os testes passarem e **antes** da reconciliação | achado confirmado muda código, cláusula e CT; a reconciliação precisa ler o diff **pós-revisão**, e a dimensão L do step 8 precisa vir logo depois dela |
| `/code-review` "ou sub-agente equivalente", sem alvo, sem nível | **dois passes no mesmo lote**: `/code-review high {base}...HEAD` + passe de eixos por sub-agente `fw-revisor-diff` (`opus`, sem Edit/Write, cego ao PRD) | o comando genérico não conhece os eixos Laravel/Livewire/multi-tenant e **não aceita foco em texto livre** (o que vem depois do nível é lido como alvo); os eixos precisam de agente próprio |
| — | **alvo explícito obrigatório** | sem alvo, o comando compara com o merge-base do **upstream**: numa branch já pushada o "diff atual" é só o não-commitado, e a revisão sai vazia parecendo limpa |
| — | **`--fix` proibido** | quem julga não conserta; o roteamento exige Adendo → CT → correção, e o `--fix` entrega correção sem oráculo |
| — | nível `high` | achado incerto é bem-vindo porque o roteamento obriga a rejeitar com motivo |
| — | **checkpoint opcional** `/code-review medium` no diff não-commitado após passo do PRD que cria fronteira | achado aqui custa uma linha; no 6.5 custa Adendo, CT, correção e re-teste |
| — | re-revisão única se a correção tocou eixo de fronteira; teto 2 rodadas | correção é código novo do mesmo agente |

A ordem oficial passa a ser **6.5 → 7 → 8 → PR**. O conteúdo do gate (eixos, roteamento,
falsificabilidade por `git stash`) não mudou.

### Adicionado

- **`## Execução e Delegação (Claude Code) — roteamento por modelo e por cegueira`**, seção nova
  antes do Fluxo de Execução. Adapta o modelo do PO com **um segundo eixo**: além da complexidade
  (que escolhe o modelo), a **cegueira** — o que o executor não pode ter visto para o resultado
  valer como prova — que escolhe o contexto e proíbe rodar em linha. É a propriedade que a
  coletânea inteira persegue (cegueira correlacionada), e sub-agente a entrega **por construção**:
  ele nasce sem o contexto da sessão.
  - **Rotas**: `mecânico` (haiku), `construtor` (sonnet), `analista` (opus), e quatro rotas
    próprias da esteira que carregam cegueira e restrição de ferramenta — `revisor-diff`,
    `adversário-ct`, `qa-gate` (todas `opus`, sem Edit/Write) e `executor-ctb` (sonnet)
  - **Ordem de preferência para obter a rota**: agentes do projeto em `.claude/agents/` →
    agentes da esteira (pasta `agents/` de cada skill, copiados com
    `cp .ai/skills/*/agents/*.md .claude/agents/`) → `general-purpose` com `model` explícito.
    **Nunca `general-purpose` sem `model`**
  - **Paralelo é o padrão**, com duas restrições da esteira: nunca dois construtores no mesmo
    arquivo; o revisor do diff só dispara depois do último construtor
  - **Quadro de despacho** antes de todo lote e relatório contra o mesmo quadro no retorno, com a
    coluna *"Não recebe (cegueira)"*. O quadro vai para a seção nova **`## Despachos`** do
    `03-progresso.md` — o primeiro registro da coletânea de **qual modelo fez o quê**, e portanto o
    primeiro instrumento de custo de operar (lacuna apontada em `estudos/`, §3.5)
  - **Rodam em linha**: 1–2 passos, interação com o usuário, decisão de contexto imediato, edição
    cirúrgica, captura verbatim do requisito — com *"Sem despacho — motivo"* declarado. Exceção
    que **não** vale: *"é pequeno, reviso eu mesmo"* — tamanho não compra cegueira
  - **Auditoria do retorno**: presença, integridade (`git diff --stat` antes/depois do lote) e
    amostragem com `Read`/`grep` direto
  - **Mapa de roteamento por step**, do 0 ao 9, com rota, paralelismo e cegueira por tarefa
- **`agents/`** — quatro definições de sub-agente, **cada uma na skill dona do contrato** para o
  `boost:add-skill` instalá-la junto (inclusive na instalação seletiva): `fw-revisor-diff.md` e
  `fw-executor-ctb.md` aqui, `fw-adversario-ct.md` na `feature-test-design`, `fw-qa-gate.md` na
  `feature-quality-gate`. Cada uma fixa modelo, ferramentas permitidas/proibidas, o que recebe, o
  que recusa receber e o formato de saída. As três de julgamento **não têm Edit/Write**: *"não
  corrige nada"* vira propriedade. O Claude Code só lê `.claude/agents/`, então a instalação exige
  a cópia `cp .ai/skills/*/agents/*.md .claude/agents/` — documentada no README raiz, no README da
  skill e na própria seção de rotas
- **Step 5**: padrão *"levantar com `mecânico`, julgar com `analista`"* — o mesmo do
  `PM_Arquiteto` do PO
- **Step 8**: despacho do `fw-qa-gate` com só path da wiki, URL do app e `git diff --stat`; o `06`
  volta como texto e a sessão grava verbatim; cabeçalho com `Independência:`
- **Checklist**: grupo `### Delegação (Claude Code)` e itens de alvo/nível/`--fix` do 6.5
- **Skills Companheiras**: linha *Orquestração (Claude Code)*

### Alterado

- **Step 7.5 → step 6.5**, movido para antes do step 7, com a seção *"Quando rodado no Claude
  Code — dois passes, no mesmo lote"* e o bloco *"Fora do Claude Code"* (host com sub-agente usa
  `revisor-diff` com o mesmo contrato; host sem sub-agente roda em linha e declara a degradação)
- Bloco de abertura, índice, step 7 (*"A ordem é 6.5 → 7 → 8 → PR"*), templates de Verificação
  Final do `01` e do `03`, e checklist: todas as referências ao 7.5 apontam para o 6.5
- Step 3: os greps prescritos vão para `mecânico` em paralelo, tabela pronta

## [3.3.0] — 2026-09-17

O gate que lê o diff, a superfície que o cliente alcança, a classe irmã e o custo. Motivada por uma
feature real (dashboard de acompanhamento de aprendizagem sobre Filament 5, 2026-09-17) que rodou a
skill 3.2.0 com **tudo cumprido** — 43 CTs, revisão adversarial fechando cinco implementações
erradas, auditoria Ponytail com dez cortes aplicados, 61 testes verdes e 2.383 casos de regressão —
e ainda assim chegou ao step 7.5 com **sete defeitos**, dois deles produzindo 500 em produção.

A diferença para a 3.2.0 é que desta vez **o step 7.5 existia e rodou**. O que a rodada mediu foi
*quais gates tinham chance de pegar antes e por que não pegaram*.

### Onde cada gate acertou e errou, medido

| Gate | Achados de correção | Por quê |
|---|---|---|
| step 5 — revisão profunda | 2 | valida o que o plano **afirma**; nenhum dos sete era afirmação do plano, e ele roda antes do código existir |
| step 6 — `ponytail-review` | 0 | **por charter**: *"correctness bugs, security holes, and performance are explicitly out of scope"*. Além disso lê o plano, não o diff |
| revisão adversarial do `04` | 0 de correção, 5 de cobertura | recebe só `00` + `04`: enxerga o que o **requisito** descreve, e nenhum dos sete está no requisito |
| suíte verde, 2.383 casos | 1 | enforço de arquitetura do próprio projeto (Action nova sem declaração de autorização) |
| **step 7.5 — `/code-review` no diff** | **7** | é o único que lê o diff atrás de defeito de correção |

### O que a 3.2.0 deixou passar — e a causa na skill

| Falha observada | Causa na skill |
|---|---|
| `$rotulos[$situacao]` sem `??` e `Carbon::parse($filtro)` sem guarda → dois **500**, alcançáveis por payload de filtro | o gatilho da superfície do cliente dizia *"feature monta sobre pacote de terceiro"*; a feature montava sobre o **framework**, o agente declarou "não se aplica" e a tabela nunca foi preenchida |
| Método público de componente devolvendo coluna não exposta ao navegador, e 500 com nome inexistente | nenhum item tratava `public function` de Page/Widget como **ação chamável por `$wire.`** |
| Página nova ausente de `config/filament-shield.php` → permission gerada que não muda nada quando desmarcada | nenhum gate varre as **listas paralelas** que o projeto mantém à mão; a lista do teste foi atualizada, a do config não |
| Carga filtrada custando ~384 queries onde a ADR previa uma | a ADR era coerente e assumia *"uma tela = um request"*; com widgets `lazy` são **N requests**, e nenhum campo do PRD obrigava a declarar isso |
| Duas superfícies da mesma fronteira, uma fechando com log e a outra em silêncio | nenhum eixo de revisão perguntava por **simetria de guarda** |

### Adicionado

- **Bloco de abertura "O gate que mais pega defeito é o step 7.5, e ele vem por último"**, logo
  abaixo do título, com a tabela medida acima. O step 7.5 estava no fim de um documento de 1.800
  linhas e é o mais fácil de adiar — e é o mais produtivo.
- **`#### Varredura da classe irmã`** no step 5, obrigatória para toda classe nova: `grep` pelo FQCN
  de uma classe **irmã** já existente para achar as listas paralelas (`config/`, seeders,
  inventários de teste, `->pages()`/`->widgets()` dos providers). "Nenhuma ocorrência além das
  previstas" é resposta válida e precisa estar escrita no `03`.
- **`## Modelo de Execução`** no template do PRD: quantos requests a tela custa, o que é adiado e
  por qual gatilho, o que é memoizado **por request** e o que é cacheado **entre** requests, e o
  custo do caminho comum × do caminho filtrado. Premissa de custo não escrita produz ADR coerente
  e errada.
- **Quatro eixos novos no step 7.5**: método público de componente, valor de estado usado sem
  validar, lista paralela e simetria de guarda.
- **Itens de Verificação Final**: custo medido contra o `## Modelo de Execução`, e `/code-review`
  no diff como linha própria.

### Alterado

- **`#### Superfície do Pacote de Terceiro` → `#### Superfície Livewire`**, e o gatilho deixa de ser
  *"quando a feature monta sobre um pacote"* para ser **"em toda feature que cria página, widget ou
  componente"**. A tabela ganha três origens — o código do projeto, o framework (`$filters`,
  `$pageFilters`, `$tableFilters`) e o pacote —, e os greps do vendor viram uma das duas varreduras.
  A condição certa é a **superfície**, não a origem dela.
- Segunda regra dura da seção: todo valor que entra por um desses pontos e vira índice de array,
  argumento de `parse`, nome de coluna ou operador **é cenário de domínio inválido**.

## [3.2.0] — 2026-09-15

Superfície do pacote de terceiro e revisão de código do diff. Motivada por uma feature real
(dashboard dinâmico sobre `mddev31/filament-dynamic-dashboard`, 2026-09-15) que rodou a skill 3.1.0,
entregou **29 CTs, 11 regras, 38 mutantes, revisão adversarial e suíte verde** — e ainda assim
liberou **quatro defeitos**, dois deles de escrita cross-tenant. Os quatro moravam na superfície do
**pacote**, que nenhum step inventariava.

### O que a 3.1.0 deixou passar — e a causa na skill

| Falha observada | Causa na skill |
|---|---|
| Ação do pacote apagava widget de outra organização por id cru do cliente (`::find($arguments['widget'])`, guardada só por `canEdit()`) | step 3 varre `app/`, `routes/`, `config/` **do projeto**; a superfície do vendor nunca é inventariada |
| Propriedade pública Livewire do vendor (`currentDashboardId`) escrita pelo cliente redirecionava a gravação para o dashboard de outra organização | idem — e `#[Session]` foi lido como se travasse, sem conferir o vendor |
| Global scope falhava **aberto** quando o painel é tenant-aware e o tenant ainda não foi resolvido | nenhum item obrigava o caso **nulo** do discriminante |
| 403 do vendor na raiz do painel com o fallback devolvendo para ele — usuário sem tela de entrada | cenário de erro fechava sem declarar a saída |
| Um CT do `04` sem teste correspondente, com o checkbox "testes conforme 04/05" fechado | item 4 do step 7 era leitura, não comando |
| `06-relatorio-qa.md` inexistente e ninguém percebeu | checklist pedia "quality gate invocado", não a evidência verificável por `ls` |

### Adicionado

- **`#### Superfície do Pacote de Terceiro`** no step 3 (obrigatório quando a feature monta sobre um
  pacote): tabela `## Superfície do Pacote` no `02` com uma linha por ponto que o cliente alcança
  (ação com id, propriedade pública, model persistido), a fronteira aplicada e o `arquivo:linha` do
  vendor. Quatro greps prescritos. Regra dura: **todo model do pacote que a feature persiste tem
  linha própria**; *"é filho, logo está protegido"* exige o grep que prova
- **Step 7.5 — Revisão de Código do Diff**, por quem não implementou, antes do quality gate: cinco
  eixos obrigatórios (fronteira de dado, ponto de entrada do vendor, propriedade pública Livewire,
  saída do estado de erro, afirmação de comentário), roteamento do achado (Adendo no `00` → CT no
  `04` → correção) e **falsificabilidade por `git stash`** — CT que passa dos dois lados não é
  oráculo
- Checklist: `## Superfície do Pacote` preenchida, revisão do diff executada, falsificabilidade
  provada, contagens do `03` derivadas por `grep -c`, e **`06-relatorio-qa.md` existe** (blocker)

### Alterado

- **Step 7, item 4** vira comando: `diff` entre os IDs de CT do `04`/`05` e os dos arquivos de
  teste, saída vazia como critério, colada na `## Verificação Final`. Era "conferir nos dois
  sentidos" em prosa — e um CT ficou sem teste com o checkbox fechado

## [3.1.0] — 2026-09-05

Reconciliação pós-implementação e ordem dura: **quality gate antes do PR**. Motivada por uma
feature real (`feat/login-unificado` no projeto-cobaia, 2026-09-05) em que a skill 3.0.0 rodou
inteira, o `03` se declarou "concluída" com PR aberto e quality gate "para o passo seguinte", e
uma revisão independente achou **31 itens**: 4 quebras reais (teste vermelho, `group` errado em
teste de browser, chave de env fora do `phpunit.xml`, par de cenário exigido por rule ausente) e
27 afirmações defasadas na wiki e nas docs.

### O que a 3.0.0 deixou passar — e a causa na skill

| Falha observada | Causa na skill |
|---|---|
| PRD e ADR-03 descreviam a guarda antiga (`routeIs('login')`) e "0 painéis → login default"; o código fazia outra coisa | step 7 mandava registrar "Desvios" no `03`, não corrigir a fonte |
| `Login.php:165` citado; o código está na 169, e o vendor não mudou em nenhum commit | citação só com linha; nenhuma conferência ao escrever nem depois |
| CT-33…CT-40 só no teste; CT-05 com 4 cenários no teste e "5 linhas" no `04` | nenhuma sincronia `04` ↔ teste além de "índice atualizado" |
| Requisito novo ("carimbo do painel no log") entrou sem cláusula; cinco testes derivados do código | `00` imutável e só "sobrescrever / incrementar / retomar" — sem procedimento para pedido que chega no meio |
| Verificação Final fechada em lote; teste marcado verde estava vermelho | "em tempo real" era prosa sem verificação |
| `group('kit')` em teste de browser, `KIT_LOGIN_UNIFICADO` fora do `phpunit.xml`, par do `fi-auth-layout` ausente | step 3 lê rules antes de planejar; nenhum step confere se o **código** as cumpre |
| Quality gate nunca rodou; PR aberto antes | "linkar ao PR" no step 7, QG no step 8, checklist intitulado "após merge" |
| Docs pt/en, CHANGELOG e ADR-08 descrevendo consequência já invalidada | docs de usuário fora da lista de fontes a reconciliar |
| A rodada de correção acrescentou aviso sobre "SSO externo" em README/docs/CHANGELOG sem `RQ` nem ADR | nenhuma checagem de rastro para texto novo em doc de usuário |

### Adicionado

- **Step 7 reescrito — "Pós-Implementação e Reconciliação (antes do PR)"**, com a lista fechada
  de fontes a reconciliar (`01`, `02`, `04`, `05`, `03`, docs pt/en, CHANGELOG, README,
  `.ai/rules`) e seis itens novos: checkbox com evidência inline; desvio corrige a fonte
  (marca `*(alterado em {data})*`) e o `03` só aponta; reverificação de citações; sincronia
  `04` ↔ teste nos dois sentidos; tabela `## Conformidade com Rules`; docs × comportamento ×
  rastro
- **Step 8 — "Quality Gate e abertura do PR"**: o PR só abre depois do veredito, com o link da
  wiki e o veredito do `06` na descrição; o `03` só diz "concluída" com a seção `## Quality Gate`
  preenchida
- **Adendo ao requisito** (seção nova em Arquivo 00): `## Adendo N — {data}` com Texto Original
  verbatim (imutável), `RQ` em numeração contínua, `feature-test-design` reinvocada só para o
  adendo **antes** do código; critério adendo × wiki nova (mesma branch e PR → adendo)
- **Seção "Citações de código — `arquivo:símbolo:linha`"**: formato obrigatório com símbolo, as
  duas classes de erro (errada ao nascer × deslocada depois) e o grep que confere as duas
- **Template do `03`**: Verificação Final com evidência inline e os itens de reconciliação;
  seções `## Conformidade com Rules` e `## Quality Gate`
- Checklist Final reorganizado em "Pós-Implementação e Reconciliação (antes do PR)", "Quality
  Gate e PR" e "Após o merge"

### Alterado

- "Atualizar os checkboxes em tempo real" virou regra verificável: `[x]` sem ` — evidência, data`
  não conta, e há o grep que lista os que faltam
- "Linkar wiki ao PR" saiu do step 7 e passou a ser a última ação do step 8
- Step 4 "Wiki já existente" ganhou o caso "requisito novo no meio da implementação → Adendo"
- Skills Companheiras: a `feature-quality-gate` passa a auditar consistência documental
  (dimensão L) e a rodar antes do PR

### Princípio desta versão

Onde a 3.0.0 já tinha a instrução e ela foi ignorada ("em tempo real", "cite `arquivo:linha`"),
a 3.1.0 não acrescenta prosa: acrescenta o formato que torna a omissão visível e o comando que
a lista. O que continua sendo julgamento (PRD × código, docs × comportamento, rules × diff) vai
para quem não escreveu o texto — a dimensão L da `feature-quality-gate` 1.2.0.

## [3.0.0] — 2026-08-14

**Breaking.** A derivação dos casos de teste sai desta skill e passa para a
[`feature-test-design`](.ai/skills/feature-test-design/README.md).

### Motivação — medida, não suposta

Auditoria de 9 wikis reais produzidas por esta skill em produção (125 casos de teste, 164 testes Pest):

| Medida | Resultado |
|---|---|
| Casos nos 4 arquétipos que o próprio template nomeava (happy/falha/autz/log) | **52%**, e nada além |
| Análise de valor limite genuína | **1 em 125** |
| Tabela de decisão implementada · pairwise | **0** · **0** |
| Cláusulas `RQ` rastreáveis sem nenhum caso | **9 de 19** |
| Casos com oráculo fraco | **19 de 125**; 7 graves cobrindo 52 telas |
| Telas `create` cobertas só por `visit()` | **5** |

Duas causas estruturais, ambas dentro da própria skill:

1. **O `04` era derivado do PRD** ("os CTs validam os passos do PRD"). O PRD é a interpretação do
   requisito — testar a interpretação a confirma. Medido sobre 318 métodos focais / 233 defeitos reais com 11 modelos:
   derivar teste do código/plano em vez da especificação multiplica por ~1,4 os testes que codificam
   o bug como comportamento esperado e corta por ~1,5 os que o detectam *(números corrigidos em 2026-09-26 — a versão original desta entrada dizia "318 defeitos", "~8×" e "~3×"; ver `estudos/2026-09-04-spdd-x-coletanea.md` §3.4)*.
2. **O critério de suficiência era cobertura de código** ("todo método público tem 1 CT, cada
   branch tem um CT") — sobre um código que **ainda não existe** quando o `04` é escrito. Isso
   obriga o agente a imaginar a implementação e testá-la.

### Removido

- Seção "Arquivo 04: Casos de Teste (CT)" e seu template de 4 arquétipos
- Seção "Arquivo 05" com o template de CT-B
- Critério de suficiência por cobertura de método/branch
- ~455 linhas do `SKILL.md` (1.722 → 1.467)

### Adicionado

- Seção **"Arquivos 04 e 05 — delegados à `feature-test-design`"**, com o contrato da delegação:
  o `00-requisito.md` é o oráculo, e o `01-plano-acao.md` entra **apenas** para paths, rotas e
  `## Superfície de UI`
- **Gate de tela de escrita**: toda rota `create`/`edit` da `## Superfície de UI` exige um cenário
  de gravação por componente Livewire no `04` — *uma tela aberta não é uma tela que grava*
- Degradação declarada: sem a `feature-test-design` instalada, registrar no `03-progresso.md`
  antes de escrever o `04` à mão

### Alterado

- **Gate do `05` (browser)**: o critério deixa de ser "depende de JS?" e passa a ser
  **"só o navegador prova?"** — JavaScript executado, console/erro de JS, acessibilidade,
  cor/tema, layout. Formulário, gravação, tabela, filtro, ação, notificação e autorização na tela
  passam a ser **teste de componente Livewire**, no `04`
- Skills Companheiras ganha a camada **Especificação de teste**

### Corrigido — afirmações erradas sobre `pest-plugin-browser`

Três estavam no `SKILL.md` e no README, e levariam o agente a configurar ou escrever coisa errada:

- *"a doc não explicita se o plugin sobe o app ou exige servidor externo"* → **o plugin sobe o
  próprio servidor** (HTTP in-process, porta aleatória). Nada de Herd, `artisan serve`, Sail ou
  `APP_URL`. O template do `05` que pedia essa configuração foi removido
- *"`actingAs()` em teste de browser não está documentado"* → é o **mesmo processo**;
  `$this->actingAs($user)` antes do `visit()` funciona e é o caminho recomendado
- *"o plugin expõe `wait(segundos)`"* → certo sobre a API, errado sobre a conclusão: **nunca usar
  `wait()`**; o plugin reexecuta cada assertion até `pest()->browser()->timeout()`

E três armadilhas que não estavam documentadas: `assertPathIs` **antes** das asserções de
conteúdo; **nunca `--parallel` com browser** (e `--tia` exige run completo, então os dois não
convivem numa invocação); `npm run build` como pré-requisito duro.

## [2.10.0] — 2026-08-14

Habilita a etapa de QA: introduz o oráculo que faltava e aciona o `feature-quality-gate`.

### Adicionado

- **`00-requisito.md` — arquivo obrigatório, o primeiro da wiki.** Guarda o requisito **como ele chegou**, com dois regimes opostos: `## Texto Original` **imutável** e `## Decomposição em Cláusulas` (`RQ-##`) derivada e revisável. Mais `## Ambiguidades e Perguntas Abertas` e `## Fora de Escopo`
  - **Por quê**: o mesmo agente lê o requisito, escreve o PRD, escreve os CTs, implementa e valida. Se entendeu errado, erra coerentemente cinco vezes e tudo fica verde. O PRD não serve como linha de base porque **ele é a interpretação**
- **Bloco "Captura do Requisito" no step 3** — primeiro ato, antes de qualquer pesquisa. Tabela das 4 origens (texto colado, arquivo `.md`/`.pdf`/`.docx`, descrição verbal, ausente) com o que fazer em cada caso; requisito ausente **para o fluxo**; descrição verbal é marcada como fidelidade baixa
- **`## Natureza da Wiki` no PRD** — nova / evolução / correção / ajuste + wiki ancestral. **Decide se o quality gate roda regressão**
- **`## Cobertura do Requisito` no PRD** — tabela `RQ` → passos que atendem; cláusula sem passo é omissão
- **Step 8 — Quality Gate (obrigatório)**: invoca `feature-quality-gate` após os testes passarem, com a tabela do que o fluxo faz para cada veredito (`APROVADO`, `APROVADO COM DÉBITO`, `REPROVADO → especificação/implementação/teste`)
- Glossário: `RQ`
- `feature-quality-gate` na tabela de Skills Companheiras (camada nova: **Qualidade**) e na lista de skills do PRD

### Alterado

- **5 arquivos obrigatórios** (era 4); ordem de criação começa pelo `00`
- **Rastreabilidade obrigatória**: todo passo do PRD e todo CT/CT-B referencia o `RQ` de origem
- Ordem de leitura do agente implementador começa pelo `00` — *o que foi pedido*, antes de *o que foi planejado*
- O antigo step 8 (Candidatos a Rule) virou **step 9**
- Boundary do Caveman passa de "arquivos wiki (01-05)" para **(00-06)**, com nota explícita de que comprimir o `00` falsifica a fonte da verdade
- Checklist ganha a seção **Requisito** (6 itens) e 2 itens de quality gate na pós-implementação
- Exemplo de estrutura inclui `00-requisito.md` e `06-relatorio-qa.md`

## [2.9.0] — 2026-08-14

### Adicionado

- **Seção "Playwright MCP na validação (opcional)"** no Arquivo 05, com a regra que divide os papéis: **o `pest-plugin-browser` atesta, o Playwright MCP observa**
- **Tabela do porquê o plugin não cobre sozinho**: `debug()`, `tinker()`, `waitForKey()` e `--headed` **exigem um humano** — um agente autônomo travaria; sobram `screenshot()` (imagem: caro e impreciso) e `content()` (dump da página inteira)
- **3 pontos de uso do MCP**, todos opcionais: step 3 (extrair locators reais → tabela `### Seletores` do `05`), loop do CT-B nas falhas de tipo (a)/(c), step 7 (console e rede como evidência)
- **Configuração obrigatória** do MCP: `--isolated --headless --caps=testing --test-id-attribute=data-testid`, com a justificativa de `--isolated` (perfil persistente é o default e vaza login entre sessões)
- **7 regras de uso**: ref nunca entra em teste (é válido só até a próxima mudança de página), `browser_find` antes de `browser_snapshot` cru, proibido `browser_run_code_unsafe`, proibido `--caps=vision`, sessão MCP não é cobertura, na causa (b) o MCP é só leitura, sem screenshot versionado em feature com dado sensível
- **Fallback documentado sem MCP** — a skill funciona sem ele: `screenshot()` → `content()` filtrado com `Grep` → derivar seletor do Blade/componente → escalar ao usuário com `--headed`
- Nota apontando o `Browser Logs` do Boost MCP como alternativa já disponível para a evidência do step 7

### Alterado

- Contrato do sub-agente do loop de CT-B ganha o passo 4: nas causas (a) e (c), observar a página via MCP se disponível; na causa (b), **não** usar o MCP para consertar — a divergência é o achado
- Checklist de pós-implementação verifica o uso disciplinado do MCP

## [2.8.0] — 2026-08-14

### Adicionado

- **Seção "Documentation API do Boost (`search-docs`)"** no step 3 — a tool passa a ser fonte primária obrigatória, antes de vendor source e antes de doc na web
- **Tabela de cobertura oficial** da Documentation API (Laravel 10–13, Filament 2–5, Livewire 1–4, Inertia 1–2, Flux UI 2, Nova 4–5, Pest 3–4, Tailwind 3–4)
- **Mapa "o que vou escrever no PRD → o que consultar"**: rotas/policies → Laravel; componente de UI → Filament/Livewire/Flux; jobs/queues → Laravel; CTs do `04` → Pest; CT-B do `05` → Livewire/Filament + Pest browser
- 4 regras de como consultar bem: uma pergunta específica por consulta, citar a versão, confirmar no código antes de escrever no PRD (divergência vira ADR), citar a origem no plano
- **Tabela de lacunas com fallback**: Pest 5 (API cobre até 4.x — `--tia`/`--agent`/matchers novos ficam de fora), Playwright/`pest-plugin-browser`, pacotes de terceiros, código da própria aplicação
- 2 anti-padrões: escrever assinatura/opção de config/comportamento de componente sem confirmar em `search-docs`; usar `search-docs` para descobrir comportamento do próprio código
- Checklist: consulta por stack com origem citada, e lacunas cobertas por doc oficial

### Alterado

- O bullet genérico *"usar `search-docs` para tecnologias envolvidas"* virou instrução obrigatória com link para a seção nova

## [2.7.0] — 2026-08-14

Consolida as versões 2.5.0 e 2.6.0 (nunca commitadas isoladamente) e adiciona a etapa de geração de rules.

### Adicionado

- **Arquivo `05-casos-de-teste-browser.md` (condicional)** — casos de teste de navegador (`CT-B`) executáveis via `pest-plugin-browser` (Playwright), com duplo uso: especificação de teste **e** roteiro de auditoria *Desenhado × Implementado*
- **Seção `## Superfície de UI` no PRD (`01`)** — tabela obrigatória de telas/componentes que funciona como **gate** do arquivo `05`: só cria CT-B se houver linha na tabela **e** (`Depende de JS? = Sim` **ou** interação com ≥ 2 telas/etapas)
- **Ciclo de escrita e auditoria dos CT-B via sub-agente em loop** — contrato explícito com máximo de 3 iterações, classificação obrigatória de falha (CT-B errado / implementação divergente / flake) e proibição de alterar código de aplicação para o teste passar
- **Seção "Execução de Testes com Pest 5"** — TIA (`--parallel --tia`), Agent plugin (`--agent`), sharding por tempo, `--profile`, `--type-coverage`, `--mutate` e os 8 matchers novos
- **Step 8 — Candidatos a Rule de Projeto** — varre `01`/`02`/`03` por candidatos a Project Rule do Boost, aplica 4 gates (durável, escopável por path, não-inferível, não-redundante), respeita teto de 3 por feature e **submete a decisão ao usuário**; se aprovado, delega à skill `requirement-to-rule`
- **Bloco "Verificação do stack de testes" no step 3** — detecta versão do Pest, `pest-plugin-browser`, Playwright, `APP_URL` e traits em `tests/Pest.php`
- **Seção "Fronteira com os CT-B" no arquivo `04`** — separa "a regra está correta?" (backend) de "o usuário chega até a regra?" (browser), com regra de não-duplicação
- Glossário: `CT-B` e `TIA`
- `requirement-to-rule` na lista de skills do PRD e na tabela de Skills Companheiras (camada nova: **Memória de projeto**)

### Alterado

- **Caveman: modo padrão `full` → `ultra`** na comunicação agent ↔ usuário. Arquivos wiki (01-05) permanecem boundary
- **Invocação do Caveman corrigida para `/caveman:caveman {modo}`** (namespace de plugin), com nota espelhando a que já existia para o `/ponytail:ponytail`
- **Comando canônico de teste passa a ser `vendor/bin/pest --parallel --tia`** na Verificação Final, no template do `03` e no step 7
- **Step 7 ganha 2 itens**: preencher o roteiro *Desenhado × Implementado* e confirmar impacto real com TIA contra a seção `## Impacto em Features Existentes` do PRD
- Ordem de leitura do agente implementador inclui o `05` (entre o `04` e o `02`)
- Ordem de criação dos arquivos inclui o `05` como condicional
- Checklist final, tabela de arquivos extras e exemplo de estrutura atualizados

### Corrigido

- Numeração duplicada dos itens do step 7 (havia dois `5.` e dois `6.`)
- Documentação de instalação do Pest: **não existe `php artisan pest:install`** — o caminho oficial é `composer remove phpunit/phpunit` + `composer require pestphp/pest --dev --with-all-dependencies` + `./vendor/bin/pest --init`

## [2.4.0] — 2026-08-11

### Alterado

- Estrutura de pastas: `wikis/{branch}/` → **`wikis/specs/{branch}/`**, encapsulando as features da skill em subpasta dedicada e liberando `wikis/` para outros documentos

### Removido

- Todas as referências a `wikis/archive/` — sobrescrever wiki existente passa a exigir backup manual do usuário

## [2.3.0] — 2026-08-10

### Adicionado

- **Step 6 — Auditoria da Wiki com `/ponytail:ponytail-review`** (obrigatório): invocação automática após a revisão profunda, sem depender de pedido do usuário; aplica sugestões de corte nos arquivos da wiki e re-executa se houver mudança significativa
- Ordem de criação dos arquivos no step 4
- Tratamento de wiki já existente: retomar / sobrescrever / incrementar
- Caveman na "Filosofia de Implementação" do template do PRD
- "Arquitetar/analisar feature" no *Quando Invocar*

### Corrigido

- **Namespace dos comandos Ponytail**: `/ponytail-*` → `/ponytail:ponytail-*`

## [2.2.0] — 2026-07-03

### Removido

- Etapa de arquivamento `/archive` — o histórico já fica registrado no `03-progresso.md`

## [2.1.0] — 2026-07-02

### Adicionado

- **Integração com o Caveman** e boundary explícito: arquivos wiki (01-05), código, commits e PRs escapam da compressão terse
- Trio documentado: `feature-wiki` (planejar) + Ponytail (executar) + Caveman (comunicar)

## [2.0.0] — 2026-07-02

### Adicionado

- **Formato ADR** no `02-decisoes-arquiteturais.md` (Status, Contexto, Decisão, Alternativas, Consequências, Referências)
- **Step de pós-implementação**: desvios do plano, notas de implementação, retrospectiva, link no PR, limpeza do channel de log
- **CTs de log e de autorização** no `04-casos-de-teste.md`
- **Padrão de log obrigatório `[Classe@Método] mensagem`** com channel por feature, níveis por severidade e context estruturado (`array $context`) rico
- Níveis de log para `fail()` de Livewire (`warning`) e `catch` de exception (`error` / `warning`)
- `Log::shareContext`, driver JSON em produção e testes de log em Pest (`Log::spy()`)
- Pesquisa e contexto expandidos: rotas, policies, config, composer, wikis existentes, git log, scheduled tasks, eventos, observers, middleware, `.env.example`
- Seções novas no PRD: Autorização, Rotas, Variáveis de Ambiente, Eventos/Listeners/Observers, Jobs/Queues, Impacto em Features Existentes, Rollback, Dependências, Riscos
- Seções novas no `03-progresso.md`: Blockers, Desvios do Plano, Notas de Implementação, Retrospectiva
- Integração com Ponytail (escada de simplicidade durante a execução, `ponytail:` comment, review no diff)

## [1.0.0] — 2026-07-01

### Adicionado

- Release inicial da skill: cria `wikis/{branch}/{feature}/` com **4 arquivos obrigatórios** — `01-plano-acao.md` (PRD), `02-decisoes-arquiteturais.md`, `03-progresso.md` e `04-casos-de-teste.md`
- **Revisão profunda pós-escrita** — re-valida cada premissa do plano contra o código real antes de apresentar ao usuário
- Validações de pesquisa obrigatórias antes de escrever (`database-schema`, `search-docs`, `model:show`, leitura de arquivos existentes)
- Critérios de *Quando NÃO Invocar* (typo fix, mudança trivial, refactoring puro, bump de dependência)

---

# feature-test-design

Deriva casos de teste que **matam defeito**, a partir do requisito — nunca do plano e nunca do código.

## [1.15.0] — 2026-09-26

Release 1 do roteiro de
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md)
(§8, itens 1, 3 e 11): **só empacotamento**. Nenhuma regra, gate, proibição, técnica, template ou
contrato do `fw-adversario-ct` mudou. A única mudança deliberada de comando é o da suíte de
browser na reference nova (ver Adicionado). É a base que a rodada do protocolo vai medir contra a
1.14.1.

O corpo do `SKILL.md` foi de 1.547 para **732 linhas**. O alvo do spec (< 500) **não foi
atingido**: 732 é o piso com gates, proibições, checklist e obrigações no corpo. Chegar a 500
exigiria condensar texto normativo fora do passo 3 — fronteira com o plano, gate do passo 6, teto
do passo 7, assertion proibida, checklist —, e isso é resumir regra: decisão de desenho para a
release 2.

**Não medido**: a rodada que compara com a tag anterior (`feature-test-design-v1.14.1` +
`feature-wiki-v3.5.2`) está pendente em
[`experimentos/README.md`](experimentos/README.md#rodadas-pendentes) (Rodadas pendentes, item a).

### Alterado

- **Frontmatter conforme o [spec Agent Skills](https://agentskills.io/specification)**: `version`
  sai do topo e vira `metadata.version: "1.15.0"` — quem conferia com `grep '^version:'` passa a
  conferir `metadata.version`. Entram `license: MIT`, `compatibility` com as exigências reais
  (Pest; o `00-requisito.md` da `feature-wiki`; `pest-plugin-mutate` + PCOV/Xdebug, ausência só
  com prova negativa; lançador `.cmd` no Windows; `pest-plugin-browser` + Playwright + `npm run
  build`; sub-agente para a adversarial, e sem ele lacuna declarada, nunca autorrevisão) e
  `metadata.requires: "feature-wiki>=3.5.2"`. Esse é o mínimo real: `## Superfície Livewire` no
  `02` (3.3.0), `## Despachos` (3.4.0), `@obsoleto` e `fw-executor-ct` (3.5.0), `grep -c` (3.5.1)
  e o contrato de delegação que entrega o `02` (3.5.2). `npx skills-ref validate` passa
- **`description` de 2.245 para 927 caracteres**: o que a skill faz, quando invocar e
  palavras-chave. Toda regra que só aparecia nela já estava no corpo, e o que servia à pessoa foi
  para o README
- **Corpo do `SKILL.md` de 1.547 para 732 linhas.** Gates, proibições, checklist e obrigações
  ficam no corpo; desenvolvimento, exemplos, templates, tabelas de dados e casos medidos vão para
  `references/`. Cada regra de execução do passo 3 fica numa linha no corpo, com ponteiro; os
  bullets "Afirmação negativa" e "Estado de erro declara a saída" ficam com o texto integral da
  1.14.1. A tabela de regras de escrita do Gherkin fica no corpo, verbatim. Da revisão
  adversarial, o corpo mantém verbatim as linhas `Entrada`, `NÃO receber` e `PROIBIDO` do
  contrato, que valem também pela rota `general-purpose`, com o ponteiro para
  `references/revisao-adversarial.md` antes do Disparo
- **Cada passo diz qual reference abrir antes da ação**; os passos 5 e 7 apontam para
  `references/armadilhas-de-api.md`. O Índice lista as references, e o Checklist Final ganha o
  bloco "Saída da derivação", com a linha *references lidas: {arquivo} (passo N), …*
- **Glossário ganha `{skills}`.** O lançador `.cmd` do `pest --mutate` passa a ser apontado em
  `{skills}/feature-wiki/references/pest-5.md`. Esse arquivo existe desde a `feature-wiki` 3.6.0;
  com a 3.5.2 (o mínimo de `metadata.requires`), o mesmo texto está na seção *Execução de Testes
  com Pest 5* do `SKILL.md` dela — e o Glossário diz isso na própria linha de `{skills}`, como o da
  `feature-quality-gate`; o link do README (tabela de dependências) também
- **README**: as tabelas de rodada (C1/C2, materialização em Pest, 24/24) viram um link para
  [`experimentos/README.md`](experimentos/README.md#histórico), a fonte única. Os fatos do
  `pest-plugin-browser` viram ponteiro para a reference. A auditoria de 9 wikis e 125 casos passa
  a viver só aqui ([O que a auditoria mediu](.ai/skills/feature-test-design/README.md#o-que-a-auditoria-mediu)).
  A razão "Tamanho" não traz mais contagem escrita à mão (o "~2.450 linhas" ficou falso nesta
  mesma release). Entra no README o que só a `description` dizia: superfície Livewire na
  taxonomia, revisão adversarial com o conjunto inteiro, cenário por fora da UI e sincronia de IDs
  nos dois sentidos

### Adicionado

- **`references/`**, um tema por arquivo, cada um com o cabeçalho *"Lida em / Fonte única de"*:
  `tecnicas-por-regra`, `taxonomia-de-defeito`, `gherkin`, `template-04`, `template-05`,
  `escolha-de-camada`, `mutation-testing`, `armadilhas-de-api`, `revisao-adversarial` (resumo; a
  fonte continua sendo o agente), `casos-medidos` (os blocos *"Medido"* que estavam no meio do
  procedimento; só o caso, a regra fica no corpo) e `pest-plugin-browser`
- **`references/pest-plugin-browser.md` é a fonte única da coletânea** para os fatos do plugin,
  e outras skills dependem dele: a `feature-wiki` 3.6.0 (ciclo dos CT-B), o `fw-executor-ctb`
  (que para se o arquivo não existir) e a `feature-quality-gate` 1.6.0 (README e dimensão G do
  `SKILL.md`, que mantém em linha os dois fatos que motivam a dimensão — exceção declarada no
  cabeçalho da reference). Por isso as duas exigem `feature-test-design>=1.15.0`. O arquivo junta as cinco cópias que
  existiam (SKILL e README desta skill, SKILL da `feature-wiki`, `fw-executor-ctb`, README do gate)
  sem perder fato nem ressalva. Onde as cópias divergiam, ficou a forma mais restritiva: para cor,
  *"dentro do plugin nenhuma assertion barata prova cor"*; e o comando da suíte de browser
  unificado na forma condicional da `feature-wiki` 3.5.2 e do `fw-executor-ctb` —
  `vendor/bin/pest tests/Browser --filter={Feature}`, com `--testsuite=Browser` só se o
  `phpunit.xml` definir a suíte. É mudança deliberada de comando. O `references/template-05.md`
  mantém `--testsuite=Browser` sem condição até a release 2 (mudar template está fora da release
  1), e a reference declara que vale a forma condicional

### Corrigido

- A afirmação de que as duas suítes "mataram todos os mutantes" vira "reportaram o mesmo score",
  com a ressalva de [`experimentos/README.md`](experimentos/README.md#materialização-em-pest-rodada-1-cenário-1)
  (nota h: score medido no Windows, sem `Duration`). O argumento estrutural — mutação não gera
  mutante para código que não existe — não muda
- README: o bloco PowerShell de instalação dos agentes copiava `.ai\skills\*` para `.claude\skills\`
  sem condição, ao contrário do bloco bash logo acima e do README da coletânea: com `boost.json`, o
  `boost:update` cria `.claude/skills/<skill>` como symlink e a cópia por cima falha. Fica igual ao
  bash (só agentes), com link para os dois casos em *Como Instalar no Claude Code*
- README: os links para `experimentos/README.md` e para o `CHANGELOG.md` viram URL absoluta do
  repositório (o `boost:add-skill` copia o README para `.ai/skills/<skill>/` do projeto, onde
  `../../../` não leva ao repositório)


## [1.14.1] — 2026-09-26

Patch de documentação e de coerência, sem técnica nova. Nasce da auditoria interna consolidada em
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md) (§7.3).

### Corrigido

- Citação do arXiv 2607.22883 estava errada no SKILL, no README e na entrada 1.0.0 deste CHANGELOG
  ("318 defeitos", "~8×", "~3×", "reverte"): são **318 métodos focais / 233 defeitos, ≈1,4× e
  ≈1,5×, "mitiga"** — o estudo SPDD de 2026-09-04 já tinha apontado e a correção estava pendente
- "Sete passos" com oito (0 a 7); Proibições fora de ordem (10, 12, 11) — reordenadas sem mudar os
  números, que outras skills citam
- `Log::` ainda aparecia como efeito colateral a rastrear (passo 3) e como exemplo de mutante,
  contra a Proibição 12 ("não derivar CT de log") — trocado por outro efeito colateral
- Gatilho da revisão adversarial é "perfil completo **ou Impacto 3**": faltava o "ou Impacto 3" na
  Proibição 9, no checklist e no README
- "Host sem sub-agente: rodar em linha" contradizia "não autorrevisar": agora é **lacuna
  declarada** no cabeçalho do `04` (`Revisão adversarial: NÃO FEITA`), nunca autorrevisão
- Contrato do adversário existia em duas fontes já divergentes (7 itens no SKILL, 8 no agente): o
  agente é a fonte; o SKILL resume e ganhou o 8º item
- Quem despacha o adversário e fecha os achados é a **sessão principal** — sub-agente não despacha
  sub-agente; quando a derivação roda em sub-agente, as perguntas ao usuário voltam como saída
- Teste de arquitetura de sincronia de IDs só olhava teste → wiki; ganhou a direção wiki → teste
- "`covers()` → 0 %" rotulado "verificado" é **medido** (experimentos); `--mutate --path=` não
  consta na referência de CLI do Pest — ressalva com alternativa `--class=`
- Âncora quebrada desde a 1.9.0 (Premissa do passo 3); `## Ambiguidades` (a seção do `00` chama-se
  `## Ambiguidades e Perguntas Abertas`); "a skill sugere `--parallel --tia`" (é a `feature-wiki`);
  "são dois comandos" sem os comandos; contagem do cabeçalho "ou removida" contra o `grep -c`
  exigido pela `feature-wiki` 3.5.1; índice sem "Precedência: Project Rule" e "Skills Companheiras"
- README: "nenhuma dependência obrigatória" contra o README raiz e o próprio SKILL (o `00` da
  `feature-wiki ≥ 2.10.0` é obrigatório); "~1.700 linhas" da `feature-wiki` (são ~2.450); "quem
  materializa é o agente implementador" (é o `fw-executor-ct`, por construção quem **não**
  implementou); tabelas de medição sem nota de que param na v1.5.0; bloco PowerShell com bytes de
  controle que não rodava
- Agente `fw-adversario-ct`: formato de retorno sem seção para as sondas 6–8 e sem ID por achado
  (`ADV-nn`); "5 implementações erradas" vira piso, não teto


## [1.14.0] — 2026-09-22

O que a primeira feature completa com adversário cego ensinou. Acompanha a `feature-wiki` 3.5.0.

### Adicionado

- **Três sondas novas no contrato adversarial** (itens 5–7 e no `agents/fw-adversario-ct.md`):
  acumulação de papéis **par a par**; participante histórico × recorte de visibilidade e destino
  do link de toda notificação; teto de todo texto livre no model. São as perguntas que nem o
  adversário fez e o quality gate depois fez (gestor que acumula `diretor` assinava as duas etapas;
  aprovador perdia o registro de vista ao decidir; link do e-mail em 404)
- **Fixture por transições reais** no `## Setup Global`: helper `{entidade}Em('{situacao}')` que
  chama a máquina de estados do domínio em vez de gravar `situacao` à força — reimplementar a
  transição no teste esconde o defeito que o teste existe para pegar. Medido: expôs que a
  notificação real exigia contexto de painel
- **Medição registrada na Revisão Adversarial**: rodada 1 achou 5 implementações erradas sobre 60
  CTs derivados por `opus`; rodada 2 achou o estrutural (`R6` eram duas regras). Os dois lados eram
  `opus` — a cegueira pesou mais que o modelo
- **Mutation testing**: *"sem driver / plugin ausente"* só com a prova negativa colada (as duas
  afirmações estavam numa wiki real e eram falsas); **`pest --mutate` dá 100 % falso no Windows**
  (`argv[0]` sh não executa; score só vale com `Duration` plausível e sobreviventes listados;
  lançador `.cmd` na `feature-wiki`); `--testsuite` só honra o último
- **Checklist pós-implementação**: `--mutate` com duração plausível; CT cujo elemento foi cortado
  no step 6 da `feature-wiki` vira `@obsoleto` (não apagado, não órfão); CT que passa dos dois lados
  do `git stash` é reescrito **ou** declarado "não falsificável nesta pilha"
- **Proibição 12 — não derivar CT de log.** Log não é cláusula; é saída observável do plano,
  conferida pela dimensão D do quality gate. Exceção: requisito de trilha de auditoria, e aí é `RQ`

### Alterado

- Princípio 1 ganha o corolário *"log não é cláusula"*, fechando o conflito com o antigo template
  da `feature-wiki`

## [1.13.0] — 2026-09-21

A revisão adversarial ganha rota e modelo. Acompanha a `feature-wiki` 3.4.0.

### Alterado

- **Revisão Adversarial**: no Claude Code, a rota é `fw-adversario-ct` (`opus`, sem
  `Edit`/`Write`/`Bash`; definição em `agents/fw-adversario-ct.md` **desta skill**, copiada para
  `.claude/agents/` com `cp .ai/skills/*/agents/*.md .claude/agents/`) ou `general-purpose` com
  `model: opus` **explícito**. O modelo é o mais forte disponível porque classificar se um oráculo
  está correto é a tarefa em que modelos são comprovadamente piores do que em gerá-lo. A cegueira
  passa a vir da **construção** — o sub-agente recebe só o que a linha `Entrada` do contrato lista
  — e o disparo é registrado em `## Despachos` do `03`. Host sem sub-agente: rodar em linha e
  declarar no `04` *"Revisão adversarial: em linha, mesma sessão que derivou"*

## [1.12.0] — 2026-09-17

Superfície Livewire: o gatilho estava condicionado à origem, e não à exposição.

Mesma feature real que motivou a `feature-wiki` 3.3.0. O checklist de taxonomia tinha a linha
*"feature monta sobre pacote de terceiro"*; a feature montava sobre o **framework**, o agente leu
ao pé da letra, declarou *"nenhum pacote persiste entidade → não se aplica"* e o conjunto de 43 CTs
saiu **sem um único cenário de entrada inválida**. Três defeitos passaram e só apareceram no
`/code-review` do diff.

### Alterado

- A entrada obrigatória `## Superfície do Pacote` do `02` vira **`## Superfície Livewire`**, exigida
  **sempre** que a feature cria página, widget ou componente. Pacote de terceiro passa a ser uma das
  origens, não a condição de a seção existir.

### Adicionado

- **Três gatilhos no checklist de taxonomia**:
  - *a feature cria página, widget ou componente Livewire* → um cenário por ponto de entrada, com
    valor **fora do domínio** e com **tipo errado**;
  - *valor de estado do framework que vira índice, `parse`, coluna ou operador* → `$filters`,
    `$pageFilters`, `$tableFilters`, `$tableSearch`, `$tableSortColumn` são entrada de usuário não
    validada. O discriminante é que **a página sanitiza e o widget recebe cru** — o cenário precisa
    entrar pelo widget;
  - *método público de componente Livewire* → é ação chamável por `$wire.` e o retorno vai para o
    navegador; um cenário com argumento fora da lista fechada.
- Duas linhas novas no checklist do template do `04`.
- Bloco de evidência com o caso medido, ao lado da tabela de taxonomia.

## [1.11.0] — 2026-09-15

Quatro gatilhos novos no checklist de taxonomia e duas regras de derivação, todos vindos da mesma
feature real que motivou a `feature-wiki` 3.2.0: 29 CTs derivados por esta skill, quatro defeitos
entregues, **nenhum deles com cenário correspondente**.

### Adicionado

- **Gatilho "feature monta sobre pacote de terceiro"**: cada linha de `## Superfície do Pacote` do
  `02` exige um cenário disparando a ação do pacote **com id/argumento de outro tenant/usuário** e
  um escrevendo a **propriedade pública** do componente pelo cliente. A tabela do `02` passa a ser
  **entrada obrigatória** da skill
- **Gatilho "cada entidade que a feature persiste"**: IDOR e mass assignment **por tabela**, não por
  feature. Fechar a linha do checklist com o CT da tabela-pai é falso ✅ — foi assim que a tabela
  filha ficou sem fronteira
- **Gatilho "filtro de escopo"**: cenário do **discriminante nulo**, declarando se a query fecha ou
  abre (com o aviso de que `where('col', null)` vira `whereNull` e abre para os globais)
- **Gatilho "cenário cujo `Então` é 4xx/5xx/redirect"**: exige o par que declara a saída
- **`### Afirmação negativa é hipótese até um `grep` prová-la`**: negativa que dispensa controle de
  fronteira exige `arquivo:linha` **e** um cenário escrito como se ela fosse falsa. Motivo: a tabela
  de mutantes só cobre regras escritas, então o que a wiki declara desnecessário escapa do gate de
  falsificabilidade inteiro
- **`### Todo estado de erro declara a saída`**: o defeito "A devolve para B, B devolve para A" não
  aparece em cenário isolado — cada um está certo sozinho

## [1.10.0] — 2026-09-05

Dois ajustes medidos na mesma feature real que motivou a `feature-wiki` 3.1.0.

### Alterado

- **Gatilho da revisão adversarial**: obrigatória no perfil completo **ou** quando qualquer área
  tem **Impacto 3**, mesmo com P×I ≤ 6. A adversarial rodou "para a área C" (P×I 9) e o achado
  que importou — laço de redirecionamento com sessão viva — estava nas áreas D e F, Impacto 3,
  perfil padrão. A revisão recebe o `04` inteiro, então estender o gatilho custa zero; a saída
  passa a declarar as áreas/regras percorridas

### Adicionado

- **Proibição 11 — não escrever teste `[CT-nn]` sem o cenário no `04`/`05`.** Cenário
  descoberto na implementação nasce no `04` (Gherkin, regra, mutante) e depois vira teste;
  requisito novo entra pelo Adendo do `00`. Medido: oito IDs só no arquivo de teste, todos
  derivados do código — a Proibição 1 com outro nome
- **Checklist pós-implementação**: sincronia nos dois sentidos (`[CT-nn]` do teste ⊆ `04` e todo
  CT do índice aponta teste existente ou "fundido em"), linha de dataset nova como Exemplo no
  Gherkin, contagem do cabeçalho recalculada ou removida
- **Teste de arquitetura sugerido** (um por projeto): lê os `[CT-nn]` dos testes e dos `04`/`05`
  e falha com o ID que existe num lado só
- Comentário no template do `04`: a linha de contagem é derivada do índice, não mantida à mão

## [1.9.0] — 2026-08-15

**Rodada 6** — a primeira medida num projeto-cobaia **novo** (kit recriado do zero: Laravel 13.25,
Filament 5.6, **Pest 5.1**, com as suítes `Kit`/`Tenancy` que não existiam antes), com o oráculo
congelado desde o baseline. Testa também se as regras sobrevivem fora do projeto que as originou.
Material em [`experimentos/2026-08-15-rodada-6/`](experimentos/2026-08-15-rodada-6/vereditos.md).

| | Baseline | Rodada 5 (1.7.0) | **Rodada 6 (1.8.0)** |
|---|---|---|---|
| C1 · cupons (de 18) | 7 | 14 | **16 — zero lacuna cega** |
| C2 · aprovação (de 18) | 11 | 17 | **17** |
| C2 · células estado × evento | 9/21 | 17/21 | **21/21** |
| Total | 18 / 36 | 31 / 36 | **33 / 36 (91,7%)** |

> **Nota de correção (2026-09-26).** A tabela acima é a medição da 1.8.0 (rodada 6), que motivou
> a 1.9.0 — como nas entradas 1.1.0 a 1.8.0, cada entrada mostra a medição da versão anterior. A
> medição da própria 1.9.0 nunca entrou no CHANGELOG: as sete rodadas com a 1.9.0 reportaram
> 15/18 + 18/18; só a rodada 7 é auditável (ver
> [`experimentos/README.md`](experimentos/README.md#histórico), Histórico e notas g, i, k). Na
> rodada 7, o C1 deu **15 de 18**, abaixo dos 16 da rodada 6: D14 e D15 voltaram a lacuna
> declarada, e D12 passou a ser detectado. O C2 deu **18 de 18** (E18 fechado). O total ficou em
> 33 de 36, igual ao da rodada 6, e escondeu a troca. É observação de um braço, sem atribuição à
> 1.9.0: a ponta da rodada 6 é rejulgável, não auditável. Detalhe em
> [`experimentos/README.md`](experimentos/README.md#o-que-mudou-entre-as-rodadas-5-e-7-defeito-a-defeito).

As quatro regras da 1.8.0 mataram cada uma o seu alvo: o gate de camada matou *policy só no form*,
a premissa de mecanismo matou *cupom excluído ainda aplicável*, a matriz cartesiana fechou 21 de 21
células **com menos cenários** que a rodada anterior (49 contra 63), e o gate de oráculo invertido
barrou 5 cenários antes do juiz. De quebra, o **fuso horário morreu pela primeira vez em seis
rodadas** — lacuna declarada desde o baseline, agora com o instante escolhido dentro da janela de 3 h.

As regras abaixo passaram por **revisão adversarial dedicada**, que rejeitou a candidata mais óbvia:
bloquear o cenário quando a premissa decide o sinal derrubaria esta mesma rodada de 16/18 para
14/18, porque dois defeitos foram detectados justamente por cenários `@premissa` afirmativos.

### Adicionado

- **Premissa de comportamento: a direção é `falha fechado`.** A 1.8.0 separou premissa de escopo
  (apaga o cenário) de premissa de mecanismo (escolhe qual escrever). Falta o terceiro tipo: a que
  decide **se** o sistema aceita ou recusa algo que o requisito não decidiu. Ela **não** autoriza a
  não escrever o cenário — fixa a direção por regra: quando outra cláusula do mesmo requisito já
  trata aquele estado como inválido no uso, a gravação **recusa**. E o **invariante das duas
  leituras** é afirmado no mesmo cenário, porque nenhuma resposta à pergunta o inverte
- **Não-efeito só discrimina se o mundo tiver destinatário.** Afirmar "nenhuma notificação foi
  enviada" num centro sem gestor, "nenhuma linha de auditoria" sem entidade auditada ou "o saldo não
  foi debitado" com saldo zero é falso ✅: o mutante e a implementação correta produzem o mesmo
  observável. Substitui a regra de atomicidade, que julgava pelo **ponto da falha** e por isso não
  pegava o **mundo vazio** — as duas condições agora valem juntas. A partição de cardinalidade
  (0/1/N) é legítima e **não** substitui a exigência
- **A discriminância vale para o `Dado`, não só para os `Exemplos:`** — a configuração do mundo é o
  parâmetro esquecido
- **A legenda da matriz é uma asserção, e é auditada.** `❌ = recusa e não-efeito` obriga cada célula
  inválida a afirmar **todos** os efeitos que aquela operação dispara no caminho feliz — não um
  efeito qualquer, escolhido por coluna. Sem matriz nova: as direções são colunas do `Esquema`
  dentro da matriz única, então o custo é em colunas e não em teto de perfil
- Dois itens novos no gate do passo 6 (asserção de ausência auditada contra o `Dado`; legenda
  verificada célula a célula), uma linha no checklist de taxonomia, duas na tabela de discriminância
  e cinco no Checklist Final

### Alterado

- A regra de escrita do passo 5 passa a exigir que o cenário de recusa **nomeie** os efeitos:
  "nenhum registro" genérico deixa de ser asserção
- Princípio Inegociável 5 ganha a fronteira: a suposição não é livre, e não escrever o cenário nunca
  é a saída

## [1.8.0] — 2026-08-15

**Rodada 5** — a primeira que mede as quatro versões que tinham entrado sem medição (1.4.0 a
1.7.0), nos **dois** cenários, com o oráculo fixo desde o baseline e um juiz cego por cenário.
Material completo em [`experimentos/2026-08-15-rodada-5/`](experimentos/2026-08-15-rodada-5/vereditos.md).

| | Baseline | Melhor anterior | **Rodada 5** |
|---|---|---|---|
| C1 · cupons (de 18) | 7 | 16 | **14** |
| C2 · aprovação (de 18) | 11 | 17 | **17** |
| Total | 18 / 36 | 33 / 36 | **31 / 36** |
| Lacunas cegas | 17 | 2 | **3** |

**As quatro regras pendentes entregaram**: cada uma matou exatamente o mutante que a originou — a
1.4.0 a precisão de `float` (`29% de 10.000 → 7.100`), a 1.6.0 devolveu o fuso de lacuna cega para
**declarada**, a 1.7.0 matou a alçada não recomputada, e a 1.5.0 pegou o ramo `valor_fixo` sem
gravação pela própria revisão adversarial, antes do juiz.

**O que sobrou foi deslocamento de orçamento.** As três lacunas cegas são novas e vieram de dois
juízes independentes, em dois cenários, com a mesma leitura: *"o conjunto testa exaustivamente o
**valor** e o **estado**, e assume o **mecanismo**"* / *"o conjunto investiu quase todo o
orçamento no eixo **ator**"*. As quatro regras abaixo saem dali, uma por mutante.

### Adicionado

- **Gate de camada da regra.** Toda regra de **autorização** e de **validação de domínio** precisa
  de ≥1 cenário que exercite a escrita **por fora do componente de UI**. Teste de componente não
  distingue, por construção, *a regra existe* de *a tela chama a regra* — um conjunto de 51
  cenários fechou a matriz papel × ação inteira pela tela e deixou passar *policy só no form do
  Filament; request direto ao backend passa*. É o pedágio, agora medido, da regra da camada mais
  barata
- **Premissa sobre mecanismo escolhe qual cenário, nunca se ele existe.** Premissa de **escopo**
  torna o cenário inexpressável (lacuna declarada legítima); premissa de **mecanismo** ("a exclusão
  é física", "`ativo` é derivado") só decide **como** escrevê-lo. Usá-la para apagar o cenário é
  converter escolha de implementação em cobertura — foi assim que *entidade excluída continua
  aplicável* virou lacuna cega com o checklist marcando a linha como coberta
- **A matriz estado × evento é montada ANTES das regras, e é UMA tabela.** Produto cartesiano
  fechado `todos os estados × todas as operações`, derivado do enum e da lista de verbos, nunca do
  mapa de regras — decompô-la por regra de negócio faz cada operação aparecer só nos estados que a
  regra dela já pressupõe. **O total de células é declarado no `04`** e cada uma resolve para
  `CT-nn`, `não se aplica` ou lacuna declarada. Medido: 17 de 21 células inválidas executadas num
  conjunto de 63 cenários, e as 4 ausentes eram `aprovar`/`rejeitar` em `rascunho` e `cancelada`
- **Cenário sem situação de partida é oráculo invertido, e o gate o barra** (item 6 do passo 6).
  Não é oráculo fraco: materializado ao pé da letra, ele **certifica** a transição ilegal como
  comportamento esperado. É o único caso em que um cenário a mais deixa o conjunto pior que o
  conjunto vazio. Correção obrigatória — não vale podar pelo item 4
- Linha nova no checklist de taxonomia: **entidade removível ou desativável** → *o registro
  removido ainda funciona?*, sobre a operação de escrita e não sobre a ausência na listagem
- Itens correspondentes no Checklist Final (derivação, escrita e gate)

## [1.7.0] — 2026-08-15

Medição da v1.5.0 no **cenário 2** — a máquina de estados. 13 regras, 63 cenários, 98 mutantes,
matriz de 35 células (14 válidas + 21 inválidas); revisão adversarial com **41 achados** e mais 3
na segunda rodada, todos fechados.

| | Baseline | v1.0.0 | v1.5.0 |
|---|---|---|---|
| Defeitos detectados (de 18) | 11 | 15 | **17** |
| Taxa de detecção | 61,1% | 83,3% | **94,4%** |
| Lacunas cegas | 7 | 2 | **1** |
| Lacunas declaradas que custaram defeito | 0 | 1 | **0** |

> **Nota de correção (2026-09-26).** A coluna "v1.0.0" é a rodada 2, a primeira medição do
> cenário 2, feita com a 1.1.0 — a entrada 1.2.0 a rotula assim. O número (15 de 18) não muda.

**Os três defeitos que escapavam de todos os conjuntos anteriores caíram**, cada um pelo mecanismo
que a versão correspondente introduziu: o ciclo de volta pelo 2-switch com `Então` contrastivo
(*"passa a ser 'aguardando_gestor', **e não** 'aguardando_diretor'"*); a tela pela partição
exaustiva do enum na coluna formatada, 5 de 5; e a atomicidade pela **injeção de falha nas duas
direções** — falhar a gravação e exigir que nenhum e-mail saia, e falhar o e-mail e exigir que a
etapa continue gravada.

O único sobrevivente é de **dimensão, não de cláusula**: valor alterado depois do envio sem
reavaliar a alçada — a coluna `editar` foi percorrida por um campo representativo, e a reabertura
alegada acontecia em `rascunho`, onde a alçada ainda não foi decidida.

### Adicionado

- **A dimensão do campo tem de ser exercitada FORA do estado inicial.** Trocar o campo decisivo em
  `rascunho` não reabre a dimensão para os estados de trânsito, e a linha inválida de `editar`
  precisa afirmar o **valor gravado**, não só que a operação foi recusada
- **Célula só conta se a operação daquela célula for executada.** Apontar para um cenário que
  executa **outra** operação — a listagem no lugar do detalhe, o `rascunho` no lugar do estado em
  trânsito — é falso ✅. E **argumentar** que "uma implementação correta se comportaria igual" não
  é executar: o argumento pressupõe a corretude que a célula existe para testar
- **Verbo irmão não herda evidência.** "Aprova **ou** rejeita", "edita **ou** exclui": a
  autorização precisa ser falsificada em **cada verbo**. Uma implementação que confere o ator em
  `aprovar()` e esquece em `rejeitar()` passa em todo conjunto cuja evidência venha só do primeiro
- **O cenário do parâmetro entregue não pode depender do ambiente de teste.** `Dado a configuração
  de fábrica, sem ajuste do teste` é vácuo se o `phpunit.xml` ou o `.env.testing` definirem a
  chave: o cenário mede o ambiente, e o default errado sobrevive sem nada ficar vermelho

## [1.6.0] — 2026-08-15

Rodada de validação da v1.5.0 nos **dois** cenários, com o recorte para o juiz tirado só **depois**
da conclusão do agente — corrigindo a contaminação que tornava as medições anteriores um piso.

**Cenário 1 · cupons** — 13 regras, 47 cenários, 79 mutantes; revisão adversarial com **22 achados,
todos fechados**.

| | Baseline | v1.0.0 | v1.1.0 | v1.5.0 |
|---|---|---|---|---|
| Defeitos detectados (de 18) | 7 | 12 | 16 | **16** |
| Lacunas cegas | 10 | 2 | 1 (float) | **1 (fuso)** |
| Oráculos fracos | — | — | 7 de 41 | **3 de 47** |

> **Nota de correção (2026-09-26).** A coluna "v1.1.0" é a rodada 3, feita com a 1.3.0 vigente na
> data, medindo as regras da 1.1.0.

A taxa parou em 88,9%, mas a **composição** mudou: a precisão de ponto flutuante — lacuna cega da
rodada anterior — fechou pela regra do exemplo discriminante, com o juiz conferindo a aritmética
(`10000 * 0.29 = 2899,9999…` → `(int)` = 2899, contra 2900 no cálculo inteiro). E os oráculos
fracos caíram de 17% para 6% do conjunto.

**Em troca, o fuso horário regrediu de lacuna declarada para lacuna cega**: o conjunto escreveu um
cenário de fuso e escolheu `20:00` — fora da janela de 3 h em que o defeito é observável. Item ✅
no checklist com o defeito intacto.

### Adicionado

- **O parâmetro livre nem sempre é o dado de entrada.** Em defeito de contexto — fuso, relógio,
  locale, tenant — o que precisa cair na janela de divergência é o **instante ou o ambiente da
  observação**. Tabela por classe de defeito de contexto, com a janela em que cada um é observável
- **Fechar lacuna declarada sem discriminar é piorar.** Ao converter uma lacuna declarada em
  cenário, o gate é mais duro: provar em uma linha por que a implementação defeituosa produz
  resultado diferente ali. Sem isso, troca-se dívida conhecida por item ✅ com o defeito dentro
- **A matriz de estados não é bidimensional.** `persona` e `qual campo muda` são dimensões, não
  detalhes do exemplo. Percorrer estado × operação com o dono do registro e sempre o mesmo campo
  produz uma matriz "100% coberta" com a barreira de identidade e o campo que decide o fluxo sem
  um único cenário
- **Rastreio de efeito cobra o QUE antes das direções**: canal/tipo exato que o requisito nomeia e
  destinatário, **depois** aconteceu / não aconteceu / uma só vez / atomicidade. Achado medido:
  as quatro direções perfeitas, e o efeito entregue por `database` quando o requisito dizia *e-mail*
- **Três linhas não-numéricas na tabela de exemplos discriminantes**: persona colapsada (o mesmo
  usuário como dono, aprovador e chamador não exercita barreira de identidade nenhuma), canal do
  efeito, e valor do requisito parametrizado
- **O número do requisito é cláusula, mesmo quando o plano o parametrizou.** *Onde* ele mora
  (`config()`, coluna, constante) é implementação; injetar por `config()->set()` em **todos** os
  cenários deixa o único valor literal do card sem teste, e qualquer default errado passa
- **Mutante trazido pela revisão adversarial não conta para o teto** de 3–6 por regra: é achado
  medido, e desdobrar a regra no fechamento da revisão renumeraria toda a rastreabilidade por
  motivo cosmético

## [1.5.0] — 2026-08-15

A execução que produziu os 88,9% não parou no recorte que foi medido: a **revisão adversarial**
(sub-agente independente, com acesso só ao requisito e aos cenários) provou **6 implementações
erradas atravessando os 41 cenários originais**, e elas foram fechadas com 10 cenários e 11
mutantes novos. As regras abaixo generalizam esses 6 achados — o número medido é piso, não teto.

### Alterado — a regra de ouro ganhou um terceiro ponto

- **`entrada ≠ uso` vira `criação ≠ edição ≠ uso`.** Fechada a criação, quatro dos seis defeitos
  novos viviam **só na edição**: normalização, unicidade, autorização e domínio existiam no
  `create` e sumiam no `save`. A edição tem ainda duas armadilhas próprias que a criação não tem —
  **unicidade contra si mesmo** (salvar sem alterar o campo único deve passar) e **validação que
  só roda na criação**

### Adicionado

- **Toda partição de EP se repete em cada rastreio de efeito.** O campo discriminador
  (`tipo = percentual | valor_fixo`) não particiona só o domínio de valor — particiona também o
  **comportamento**: consumo, trilha, validação, notificação. Achado mais caro da revisão
  adversarial: **todos** os cenários de consumo e trilha usavam cupom de porcentagem, e um atalho
  no ramo `valor_fixo` — ignorando validade, limite e auditoria — ficava verde no conjunto inteiro
- **A matriz estado × operação cobra as duas metades.** "Toda célula vazia vira cenário negativo"
  é metade da regra; seguir só ela deixa colunas inteiras sem **nenhuma operação bem-sucedida** —
  a coluna `editar` fica com três recusas e nenhuma edição que funciona, e a armadilha da
  unicidade contra o próprio registro passa inteira. Cada coluna precisa de ao menos uma célula
  válida exercitada
- **Idempotência com o agregado fora de escopo**: o cenário é **inexpressável**, e escrevê-lo
  produz um caso tautológico que parece cobertura. O procedimento passa a ser não escrever,
  declarar a lacuna vinculada à premissa de escopo, e transformá-la em pergunta ao usuário
- **Rastreio de efeito consome o teto inteiro do perfil** — três cenários obrigatórios (quatro com
  atomicidade) contra teto de três por regra. Não é estouro, é o custo declarado da técnica; regra
  de efeito colateral que também tem domínio a particionar é **duas regras**

## [1.4.0] — 2026-08-15

Terceira medição do cenário 1, agora com a skill nova rodando de fato. A progressão completa,
mesmo requisito e mesmo catálogo de 18 defeitos:

| | Baseline | v1.0.0 | v1.1.0 |
|---|---|---|---|
| Defeitos detectados | 7 | 12 | **16** |
| Taxa de detecção | 38,9% | 66,7% | **88,9%** |
| Lacunas cegas | 10 | 2 | **1** |

> **Nota de correção (2026-09-26).** A coluna "v1.1.0" é a rodada 3, feita com a 1.3.0 vigente na
> data, medindo as regras da 1.1.0.

**Cinco dos seis fugitivos históricos fecharam** — e o juiz atribuiu cada um a um mecanismo
reprodutível, não a sorte: o teto do percentual e o piso do valor caíram pela regra
*entrada ≠ uso* combinada com *domínio condicionado*; a validade no passado, pela mesma regra
aplicada à gravação **e à edição**; o cupom excluído ainda aplicável, pela coluna *aplicar* da
tabela estado × operação.

### Adicionado — as duas cegueiras que sobraram

- **O exemplo tem de ser discriminante.** Um cenário só mata o mutante se os **valores escolhidos**
  distinguem a implementação certa da errada, e valor redondo é a forma mais comum de um cenário
  parecer cobrir e não cobrir. Medido: um conjunto marcou "precisão monetária" como coberta,
  citou dois cenários, e **nenhum dos cinco exemplos numéricos distinguia `float` de inteiro**
  (10% de 10.000 dá 1.000 nas duas implementações; é preciso 29% de 10.000, onde o float dá 2.899
  e o inteiro 2.900). Item ✅ no checklist com o defeito intacto é pior que lacuna declarada,
  porque ninguém volta a olhar. Entra tabela de valores que discriminam × valores que não
  discriminam, por classe de defeito
- **Idempotência: o agregado tem de ser o persistido**, não o retorno da chamada. Se o `Então`
  afirma sobre o valor devolvido por duas chamadas independentes, o cenário passa por construção
  quando o motor é função pura — o mutante "acumula" nem é expressável ali

## [1.3.0] — 2026-08-14

Contradições internas que só o uso revelou — relatadas pelos próprios agentes que executaram o
pipeline, não por revisão de escrivaninha.

### Adicionado

- **Um `Esquema do Cenário` conta como 1 cenário**, não como N linhas. Sem isso, o teto de
  cenários e a exigência de "100% das células inválidas da tabela de estados" ficam
  aritmeticamente incompatíveis — 21 células contra teto de 5 — e a regra puniria exatamente a
  técnica que a skill quer
- **Pós-processo da revisão adversarial**: fechar todos os achados; re-revisar **uma vez**, e só
  se o fechamento criou cenário novo; teto de 2 rodadas. Revisão cujos achados ninguém fecha é
  teatro caro
- **Desempate da camada**: ela sai do **observável que o requisito afirma**, não da estrutura
  provável do código. Decidir `Unit` ou `Feature` perguntando "existiria um predicado puro para
  isso?" é palpite de implementação — exatamente o que o princípio 1 proíbe
- Aviso para confirmar que `pestphp/pest-plugin-mutate` está **declarado no `composer.json`**: ele
  costuma vir como dependência transitiva do Pest 5, e o comando funciona por acidente da árvore
  de dependências

## [1.2.0] — 2026-08-14

Segundo cenário do experimento — uma **máquina de estados** (fluxo de aprovação em duas etapas),
escolhida para exercitar o que o cenário de cálculo não cobre. Mesmo protocolo: 18 defeitos
plantados antes, juiz cego, citação literal exigida.

| Métrica | Baseline | v1.1.0 |
|---|---|---|
| Defeitos detectados (de 18) | 11 | **15** |
| Taxa de detecção | 61,1% | **83,3%** |
| Células inválidas da matriz estado × evento **executadas** | 9 de 21 | **21 de 21** |
| Lacunas cegas | 7 | 2 |

Os três defeitos que ainda atravessaram os dois conjuntos viraram as regras abaixo.

### Adicionado

- **Ciclo de volta exige 2-switch** — quando um estado pode ser **reentrado** (rejeitado volta a
  rascunho, devolvido volta para correção, estornado volta a pendente), cobrir uma transição por
  vez não prova nada sobre o **segundo giro**, e é ali que mora o defeito: o ciclo novo herda o
  que o anterior deixou. O oráculo é sobre o destino do **segundo** evento
- **Estado exibido: partição exaustiva do enum** — quando o usuário vê um rótulo derivado de um
  enum de estado, toda partição é classe de equivalência obrigatória. Cobrir dois dos cinco
  estados permite exatamente o defeito que importa: a tela dizer "Aprovada" faltando uma etapa
- **Atomicidade exige injeção de falha** — `assertNothingSent()` num caminho de **pré-validação**
  parece cobrir "o e-mail não sai se a gravação falhar" e não distingue as duas implementações.
  É preciso falhar **depois** do ponto de notificação. Falso ✅ clássico; os dois conjuntos
  medidos caíram nele
- Duas regras novas de escrita de cenário: **cenário de recusa afirma o não-efeito** (recusar
  "depois de gravar" passa num cenário que só afirma a recusa) e **nenhum termo de domínio não
  definido no `Então`** (*"o aprovador da vez é o Rui"*, *"o acesso é concedido"* — que é
  `assertOk` com outro nome)

### Corrigido — a skill estava supervalorizando o `pest --mutate`

Medição direta, contra a **mesma** implementação: as duas suítes materializadas — a do gabarito e
a deste pipeline — obtiveram **100% de mutation score cada** (24 de 24 mutantes mortos), enquanto o
juiz cego as separava em 7 × 12 defeitos detectados. **A métrica saturou e não distinguiu nada.**

> **Nota de correção (2026-09-26).** O 100% (24/24) das duas suítes foi medido no Windows, com
> Pest 5.0.5. É o ambiente em que, em 2026-09-21, o `pest --mutate` foi medido dando 100% falso
> (entrada 1.14.0). A medição não registrou `Duration` nem sobreviventes, então o número fica não
> verificado. O argumento — mutação não gera mutante para código que não existe — não depende dele.

A causa é estrutural: mutation testing só muta **código que existe**. Os defeitos que separam as
duas são *comportamentos ausentes* — não há `if ($percentual > 100)` para mutar porque a validação
nunca foi escrita. **`pest --mutate` é cego à omissão.**

A skill passa a declarar isso: o mutation score é **piso de qualidade de assertion**, não
indicador de cobertura de requisito. Quem responde por omissão é a rastreabilidade `RQ` → cenário
e o gate de mutantes **de especificação** — que nascem do requisito, não do código.

Duas armadilhas verificadas na prática, agora documentadas:
- **`covers(X::class)` restringe o que conta como coberto**: mutante em classe fora do `covers()`
  é reportado como `uncovered` e o score vai a 0%, **mesmo com os testes executando aquele código
  em toda chamada** (verificado com `ResultadoDoCupom`, que é o retorno de todos os casos)
- **`--class=` não casa de forma confiável**; `--path=` é o filtro que funciona

## [1.1.0] — 2026-08-14

Correções vindas de **medição**, não de revisão. A v1.0.0 foi submetida a um experimento
controlado: mesmo requisito, mesmo projeto, mesmo `00-requisito.md`, dois agentes independentes —
um seguindo a `feature-wiki` 2.10.0 e outro a `feature-test-design` 1.0.0 —, e um juiz cego
pontuando os dois conjuntos contra um catálogo de **18 defeitos plantados antes** de qualquer
conjunto existir.

| Métrica | Baseline | v1.0.0 |
|---|---|---|
| Defeitos detectados (de 18) | 7 | **12** |
| Taxa de detecção | 38,9% | **66,7%** |
| Lacunas **cegas** (nem detecta nem menciona) | 10 | **2** |
| Lacunas **declaradas** | 1 | 4 |
| Casos de teste | 12 | 37 |

Veredito do juiz sobre o mecanismo: *"C1 deriva de fronteiras, C2 deriva de superfície de código —
organiza os casos por método público e declara cobertura quando todo método tem um caso. Isso
garante que nada fique sem teste e não garante nada sobre valores."*

**Seis defeitos atravessaram os dois conjuntos.** Cada regra abaixo fecha um deles.

### Adicionado

- **Regra "entrada ≠ uso"** — derivar partição e valor limite tanto no ponto de **gravação**
  quanto no de **uso**. Os dois conjuntos testaram exaustivamente o mesmo campo pelo lado do
  cálculo e deixaram passar três defeitos de cadastro (valor negativo, valor acima do teto, data
  no passado). O requisito costuma descrever só o ponto de uso, e é isso que induz o erro
- **Domínio condicionado** — quando o domínio válido de um campo depende de outro campo
  (`valor` depende de `tipo`), a fronteira é por combinação. Tratar como domínio único faz o teto
  de 100% desaparecer enquanto os cenários "cobrem o campo"
- **Estado × operação, não estado × visibilidade** — a tabela de estados leva **todas** as
  operações nas colunas. A célula que mais escapa é "entidade excluída × operação de escrita":
  provam que sumiu da listagem, não que deixou de funcionar
- **Idempotência ancorada no agregado afetado**, não no recurso consumido — o oráculo é "o total
  do pedido é o mesmo depois da segunda aplicação", não "o contador foi a 2"
- **Impossibilidade de arnês é hipótese, não conclusão** — antes de declarar mutante sem matador,
  tentar mudar o arnês (`config(['app.timezone'])`, `travelTo()`, gravar estado inválido direto).
  A lacuna só é real depois de tentada, e é declarada com **o que foi tentado**
- **Teto de mutantes por regra** (2–5 no padrão, 3–6 no completo) e **teste de plausibilidade**:
  *um dev competente, lendo só o requisito e sem má-fé, escreveria isso?* Impede inflar o gate
  com mutantes triviais
- **O gate vence o teto de cenários** — mutante vivo é pior que cenário a mais
- Seções `## Fronteira com o Plano` (o que veio do PRD e foi **recusado** como oráculo) e
  **cogitado e cortado** (candidatos além do teto, com o motivo do corte)
- **Precedência**: Project Rule do projeto vence a skill, com a divergência declarada
- Escape para `00-requisito.md` somente leitura: perguntas em bloco pronto para colagem no `04`

### Alterado

- **`sim` deixa de ser resposta válida no checklist de taxonomia.** Cada item recebe o ID do
  cenário que o mata, `não se aplica: {motivo}` ou `lacuna declarada: {o que foi tentado}`.
  No experimento, **os dois conjuntos marcaram itens como cobertos com o defeito intacto**
  (*"Idempotência: sim"*, *"Timezone: parcialmente coberto"*) — é o "falso ✅" que faz o requisito
  parecer verde
- **Perfil é orçamento, não teto de rigor**: escalar a técnica acima do perfil da área é permitido
  e declarado; rebaixar não. O mapeamento área → regra passa a ser explícito no Mapa de Regras
- **"Camada mais barata"** vira **"camada mais barata que existe no projeto"** — confirmar as
  ligações do `tests/Pest.php` antes de alocar; a escada teórica não vale se o arnês não a sustenta
- Novo item no checklist de taxonomia: **autorização exercida na ação**, não só `can()` — policy
  correta que o Resource nunca consulta passa em todo teste de `can()`

## [1.0.0] — 2026-08-14

Skill nova. Extrai da `feature-wiki` a responsabilidade de escrever o `04` e o `05`, e substitui o
preenchimento de gabarito por um pipeline de derivação com gate de auditoria.

### Adicionado

- **Pipeline de 7 passos**: perfil de esforço por risco (P×I) → varredura **SFDIPOT** →
  mapa de regras (**Example Mapping**) → técnica formal por regra → checklist de taxonomia de
  defeito → cenários em **Gherkin pt-BR** → alocação de camada e poda
- **Gate de falsificabilidade** — o passo que não existia. Toda `Regra:` declara as
  implementações erradas plausíveis (mutantes) e aponta o cenário que mata cada uma. Mutante sem
  matador é lacuna declarada, e cenário que não mata mutante nenhum é candidato a corte
- **Técnicas formais nomeadas**, escolhidas pelo tipo da regra: particionamento de equivalência,
  valor limite 3-valores (com o incremento do tipo certo), tabela de decisão colapsada,
  **tabela estado × evento** (matriz, não diagrama — as células vazias são os cenários negativos),
  matriz papel × ação, pairwise e rastreio de efeito colateral
- **Checklist de taxonomia** para o que a especificação nunca menciona: IDOR/autorização
  horizontal, idempotência, concorrência, ausente ≠ `null` ≠ `""`, paginação, ordenação por coluna
  nullable/inexistente, timezone/DST, unicode e limite de `varchar`, unicidade + soft delete, CRUD
  combinado, mass assignment, upload, precisão monetária. Tabela **viva**: defeito que escapa vira
  linha nova
- **Gherkin como linguagem de especificação, sem runner** — `Funcionalidade` → `Regra` →
  `Cenário`, com 10 regras de escrita, cada uma corrigindo um anti-padrão catalogado. Não há
  plugin Gherkin viável para Pest, e Behat exigiria uma ponte Laravel abandonada
- **Tabela de escolha de camada** para Laravel/Filament, com a **camada de componente Livewire**
  que faltava, e a **regra do par** (*uma tela aberta não é uma tela que grava*)
- **Lista de assertions proibidas como oráculo único**: `assertNoJavaScriptErrors()` sozinho,
  `assertOk()` sozinho, `assertSee` de texto de layout, `assertDatabaseHas` só com a chave,
  "não lança exceção", `->not->toBe()` sem valor esperado
- **Tabela de armadilhas de API** que invalidam CT: `Mail::assertSent` em mailable `ShouldQueue`,
  `Event::fake()` antes das factories, `Http::fake()` sem `preventStrayRequests`,
  `withoutExceptionHandling()` + `assertForbidden()`, `RefreshDatabase` + `afterCommit()`,
  `travel()` sem `travelBack()`, `Repeater::fake()` no Filament
- **Fechamento do ciclo com `pest --mutate`**: cada mutante sobrevivente é traduzido de volta para
  a lacuna de derivação que o deixou vivo, e vira cenário novo
- **Revisão adversarial** por sub-agente independente no perfil completo — proibida a
  autorrevisão, porque modelos são comprovadamente melhores em gerar oráculos do que em
  classificar se um oráculo está correto

---

# feature-quality-gate

## [1.6.0] — 2026-09-26

Release 1 do roteiro do estudo
[`2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md)
(§8, itens 1, 2 e 11): **só empacotamento**. Nenhuma dimensão, gate, regra, template ou contrato
de agente mudou; no `SKILL.md`, fora do frontmatter, mudaram só o Glossário (`{skills}`), cinco
ponteiros para a `feature-wiki`, um ponteiro na dimensão G para a fonte única do
`pest-plugin-browser` e o qualificador do mutation score na dimensão K (ver *Corrigido*).

O item 3 (`references/`) não cobre esta skill nesta release: o corpo segue com **800 linhas** (797
na 1.5.2, mais a linha de `{skills}` no Glossário e duas da ressalva do mutation score na dimensão
K). O alvo do spec (< 500) **não foi atingido**
nem tentado; os blocos candidatos para uma release futura são as dimensões K e L, o template do
`06` e as tabelas de delegação e do MCP. Os blocos "Medido em 2026-09-21" continuam no corpo.

**Não medido**: a comparação com a tag anterior não tem rodada — nem pendente. As
[Rodadas pendentes](experimentos/README.md#rodadas-pendentes) de `experimentos/README.md` medem a
derivação do `04`, e o gate não tem braço no protocolo. O que se confere é o diff:
`git diff feature-quality-gate-v1.5.2 -- .ai/skills/feature-quality-gate/SKILL.md` mostra só o
frontmatter, o Glossário, os ponteiros e a ressalva da dimensão K.

### Alterado

- **Frontmatter conforme o [spec Agent Skills](https://agentskills.io/specification)**
  (`skills-ref validate` verde): `version` sai do topo e vira `metadata.version: "1.6.0"` — quem
  conferia com `grep '^version:'` passa a conferir `metadata.version`. Entram `license: MIT`,
  `compatibility` (Laravel com Pest 4 ou 5; sub-agente `fw-qa-gate` no Claude Code, em linha em
  outro host; opcionais com a degradação declarada, entre eles `pest-plugin-agent` para o
  `--agent`) e `metadata.requires: "feature-wiki>=3.5.0; feature-test-design>=1.15.0"`. A
  `feature-test-design` 1.15.0 é a que traz `references/pest-plugin-browser.md`, para onde a
  seção de dark mode do README aponta: as duas saem juntas
- **`description` de 1.369 para 1.000 caracteres**: o quê, quando e palavras-chave de gatilho.
  Fica o gatilho sem pedido ("antes de abrir PR com UI ou regra de negócio sensível") e os termos
  das dimensões K (oráculo fraco, mutation score via `pest --mutate`) e L (PRD/ADR × código, rules
  × diff, docs pt × en × CHANGELOG). Saem a contagem "12 dimensões", o teto de 3 ciclos e a
  instalação do sub-agente, regras que já estavam no corpo
- **Ponteiros para a `feature-wiki` apontam para o arquivo onde o texto mora desde a 3.6.0**: os
  greps da Superfície Livewire (Entradas e dimensão I) em
  `{skills}/feature-wiki/references/pesquisa-step-3.md`; o lançador `.cmd` do `pest --mutate`
  (dimensão K, dois pontos) em `{skills}/feature-wiki/references/pest-5.md`; o comando da L2 em
  `{skills}/feature-wiki/references/citacoes-de-codigo.md` (o formato obrigatório continua no
  corpo da `feature-wiki`). O Glossário define `{skills}` e diz onde está o mesmo texto numa
  `feature-wiki` 3.5.x
- **Dimensão G aponta para a fonte única dos fatos do `pest-plugin-browser`**
  (`{skills}/feature-test-design/references/pest-plugin-browser.md`, §*Tema, cor e acessibilidade*).
  Os dois fatos que motivam a dimensão (`assertSee` passa com o texto invisível; o primeiro
  `assertScreenshotMatches()` cria o baseline com o bug) ficam em linha, como exceção declarada no
  cabeçalho da reference
- **README = por quê / quando / limites / dependências** (553 → 447 linhas). Sai a segunda cópia
  das 12 dimensões, dos 5 destinos com a tabela lacuna → destino, das regras de convergência e dos
  princípios, das regras do Playwright MCP e da tabela de regressão; o README explica e aponta
  para a seção do `SKILL.md`. O estudo de viabilidade fica
- README: **uma tabela de dependências** (versão mínima, para quê, o que degrada sem cada item)
  no lugar de duas listas que divergiam: `feature-test-design` ≥ 1.15.0, `pest-plugin-agent` com
  Pest 5, Project Rules do Boost (`laravel/boost` 2.4.12; sem elas a L4 fica em "Não Verificado").
  "App servido" deixa de constar como obrigatório, como o `SKILL.md` já dizia: sem app, B a I
  ficam estáticas
- README: seção **Limites**, com os limites abertos no roteiro (itens 8 e 9): dimensões de
  julgamento, `APROVADO` com dimensões puladas, sobreposição da I com o step 6.5 e o
  `/code-review`, `Bash` no sub-agente e leitura do `03`. "Quem corrige" é a estação do destino
- README: os fatos do `pest-plugin-browser` viram ponteiro para a fonte única
  `{skills}/feature-test-design/references/pest-plugin-browser.md`; fica só o que é da dimensão G
- README: nota de medição. O gate não tem rodada própria em `experimentos/`, a validação de
  2026-09-21 foi uso real, e as tabelas de medição vivem só em
  [`experimentos/README.md`](experimentos/README.md#histórico)

### Corrigido

- **Versão mínima da `feature-wiki` de 2.10.0 para 3.5.0**: `00-requisito.md` (2.10.0),
  `## Superfície Livewire` do `02` (3.3.0), `## Despachos` do `03` que a L6 confere (3.4.0,
  publicada só junto com a 3.5.0) e o lançador `.cmd` que a dimensão K manda usar (3.5.0)
- **Dimensão K afirmava "duas suítes com 100% de mutation score cada" como fato medido.** O 100%
  não está verificado: foi medido no Windows, sem `Duration` registrada (nota h da
  [tabela única](experimentos/README.md#materialização-em-pest-rodada-1-cenário-1), e nota de
  correção na entrada 1.1.0 abaixo). A frase passa a dizer que as duas suítes *reportaram o mesmo*
  score, com a ressalva e o link; o 7 × 12 do juiz está confirmado. A regra — score alto não
  absolve a dimensão A — não muda
- README: o bloco PowerShell de instalação dos agentes copiava `.ai\skills\*` para `.claude\skills\`
  sem condição, ao contrário do bloco bash logo acima e do README da coletânea: com `boost.json`, o
  `boost:update` cria `.claude/skills/<skill>` como symlink e a cópia por cima falha. Fica igual ao
  bash (só agentes), com link para os dois casos em *Como Instalar no Claude Code*
- README: os links para `experimentos/` e para o estudo viram URL absoluta do repositório (o
  `boost:add-skill` copia o README para `.ai/skills/<skill>/` do projeto, onde `../../../` não leva
  ao repositório)

### Registrado, não corrigido

- `SKILL.md` ("os princípios 1 e 2 são construção, não promessa") e `agents/fw-qa-gate.md`
  ("mecânico aqui, não uma promessa") contradizem o estudo, §7.1 (T7): o sub-agente tem `Bash`.
  Fica para a release 2 (item 9), porque corrigir é mudar regra


## [1.5.2] — 2026-09-26

Patch de documentação e de coerência, sem dimensão nova. Nasce da auditoria interna consolidada em
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md) (§7.4).

### Corrigido

- **Veredito era indecidível**: `APROVADO` ("nenhum Blocker ou Major") e `APROVADO COM DÉBITO`
  ("só Minor/Cosmético") se sobrepunham. Agora `APROVADO` = **nenhum achado aberto**;
  `COM DÉBITO` = ≥ 1 Minor/Cosmético e nenhum Blocker/Major
- "Piso 70 % → `REPROVADO → teste`" contradizia "o achado é sempre um mutante nomeado, nunca um
  percentual": o piso manda **investigar**; o achado registrado é o mutante
- "12 dimensões" eram **11** na `description` (faltava a A, cobertura do requisito), **10** num
  trecho do README (sem K e L) e "**3**" noutro (o perfil mínimo roda **5**: A, D, J, K, L)
- Modo degradado validava "B–K" (sem a L); template do `06` listava "L1…L5" (a L6 existe desde a
  1.5.0)
- Fluxo (passos 6 e 8) e checklist mandavam a skill **gravar** o `06` e o `03` — em sub-agente ela
  devolve texto e a sessão grava; agora os quatro pontos bifurcam
- Tabela de Entradas não listava `02`, `03`, o `06` do ciclo anterior, `.ai/rules/index.md`, docs
  e CHANGELOG — todos exigidos pelo corpo (L3, L6, convergência, dimensão L)
- Sem app "ficam estáticas" B, D, F, G, H, I — faltavam **C** e **E**
- Linha `Independência:` tinha dois valores no template e três no agente
  (`comprometida — recebeu {o quê}`); e o placeholder era `{rota}` num lugar e `fw-qa-gate`
  noutro
- Detecção de dark mode só olhava `tailwind.config.js` — cega ao Tailwind 4 (`@custom-variant dark`
  em CSS); comando acrescentado
- `XDEBUG_MODE=coverage vendor/bin/pest` (prefixo POSIX) num passo que manda usar o `.cmd` no
  Windows — alternativa PowerShell/`.cmd` ao lado
- `Browser Logs` → id real da tool: `browser-logs`; path do log `{feature}.log` →
  `{feature-name}-*.log` (driver `daily`)
- README: "v1.0.0", "na futura SKILL.md", "10 proibições" (são 11), destino 1 "(`01`/`02`)" (é
  `00`/`01`/`02`), heading `Dependências` duplicada, linha de tabela órfã (PCOV/Xdebug), estudo de
  viabilidade sem data (pesquisa de 2026-08-14) e citação atribuída a "doc" que as Fontes chamam de
  post; bloco PowerShell com bytes de controle (`\a` → BEL) que não rodava
- Agente `fw-qa-gate`: "executa as 12 dimensões" (são as do perfil: 5, 9 ou 12); pedia para
  **acrescentar** a linha `Independência:` que o template já tem; não recebia a branch base do PR;
  não listava `browser-logs` entre as tools do Boost


## [1.5.1] — 2026-09-22

O gate aprende a conferir número por `grep`, não por leitura. Acompanha a `feature-wiki` 3.5.1.

### Alterado

- **L3 confere afirmação com número por `grep -rn` do valor na wiki inteira**, não abrindo o
  arquivo onde a afirmação é esperada. Achado novo: número certo num arquivo e velho em outro
- **Todo achado de L2, L3 ou L6 que envolva um valor sai com o `grep -rn` colado**, e a ação
  exigida nomeia **todos** os arquivos que o repetem. Medido: este gate acusou uma contagem errada,
  o orquestrador corrigiu o `01` e a ADR do `02`, que repetia o número, ficou para trás
- Checklist: +1 item

## [1.5.0] — 2026-09-22

O juiz cego rodou pela primeira vez numa feature completa e acusou o orquestrador. Acompanha a
`feature-wiki` 3.5.0.

### Adicionado

- **Checagem L6 — alegações do `03`**: todo `[x]` da `## Verificação Final` com número é
  reproduzido pelo comando que o gera; toda degradação declarada ("sem PCOV", "plugin ausente",
  "MCP indisponível") é conferida com a prova negativa (`php -m`, `ls vendor/…`); toda `Duration`
  de `--mutate` é testada por plausibilidade. Severidade Major, destino 1 (e 3 quando a degradação
  pulou o passo medido da K). É a checagem que **acusa o orquestrador** — e só um juiz que não viu
  a conversa a faz sem viés. Nasceu de QA-03 (*"88 ok"* irreproduzível) e QA-04 (*"sem
  PCOV/mutate"* com os dois presentes) do ciclo 1 de 2026-09-21
- **Dimensão K — plausibilidade do score antes de lê-lo**: no Windows o plugin de mutação conta
  falha de spawn como mutante morto (*206 mutantes, 100 %, 3 s*); score sem `Duration` compatível
  com N × testes cobridores, ou sem sobreviventes listados, é **"Não Verificado"**, não 100 %.
  Este gate aceitou um *"2 mutantes, 100 %"* na primeira execução e não devia — está escrito
- **Proibição 11 — não aceitar número sem comando nem ausência sem prova**
- **Medição registrada no princípio 2**: `REPROVADO → especificação`, 8 achados, 2 perguntas de
  requisito inéditas e 2 achados contra a própria sessão
- **`agents/fw-qa-gate.md`**: seção *Duas checagens que só você consegue fazer sem viés* (L6 e
  plausibilidade da K)

### Alterado

- Piso da dimensão K: *"sem driver, declarar Não Verificado"* passa a exigir a prova da ausência
  antes da declaração
- Checklist Final: +2 itens (L6; K só com duração plausível e sobreviventes nomeados)

## [1.4.0] — 2026-09-21

Os princípios 1 e 2 viram construção no Claude Code. Acompanha a `feature-wiki` 3.4.0.

### Adicionado

- **Execução como sub-agente**: a `feature-wiki` despacha esta skill no step 8 como `fw-qa-gate`
  (`opus`), que **não tem `Edit`/`Write`** e recebe só o path da wiki, a URL do app e o
  `git diff --stat` — nunca a conversa que escreveu o `01` e implementou. O relatório volta como
  texto e a sessão o grava verbatim. *"Por quem não escreveu a wiki"* e *"não corrige nada"*
  deixam de ser promessa
- **`agents/fw-qa-gate.md`** nesta skill, para o Boost instalá-lo junto. O Claude Code só o enxerga
  em `.claude/agents/`: copiar com `cp .ai/skills/*/agents/*.md .claude/agents/` a cada atualização
- **Linha `Independência:` no cabeçalho do `06`**: `sub-agente {rota}/{modelo}, sem acesso à
  conversa` ou `mesma sessão que escreveu a wiki (degradado)`. O leitor precisa saber se quem
  julgou foi quem escreveu

## [1.3.0] — 2026-09-15

Dimensão I passa a cobrir a superfície que o projeto **não escreveu**.

### Adicionado

- **Dimensão I — Segurança da Superfície Nova**, quatro checagens novas: ação de pacote de terceiro
  alcançável por `$wire.mountAction` com id do cliente (conferida contra `## Superfície do Pacote`
  do `02`); propriedade pública Livewire sem `#[Locked]` que decide **onde** a escrita cai (com a
  nota de que `#[Session]` não tranca — só repõe no `mount()`); escopo com discriminante nulo
  (falha aberta × fechada); e estado de erro sem saída, com par de redirect mútuo classificado como
  **Blocker**

## [1.2.0] — 2026-09-05

### Adicionado

- **Dimensão L — Consistência Documental (wiki × código × docs × rules)**, nunca pulada em
  nenhum perfil. Cinco checagens estáticas: L1 IDs de CT teste × `04`/`05`; L2 citações
  `arquivo:símbolo:linha`; L3 PRD/ADR × código (afirmação sem marca `*(alterado em …)*`); L4
  rules cujo glob casa o diff × tabela `## Conformidade com Rules` do `03` × código; L5 docs
  pt × en × CHANGELOG × README × comportamento, com frase sem `RQ`/ADR de origem tratada como
  crescimento sem rastro. Tabela de severidade e destino por checagem: rule violada → Major ou
  Blocker, destino 2; CT só no teste → destino 3 via `feature-test-design`; texto defasado →
  destino 1
- Entradas novas: `.ai/rules/index.md` e as rules que casam o diff, docs de usuário e CHANGELOG
  tocados, e a declaração do implementador no `03`

### Motivação

O step 7 da `feature-wiki` manda registrar desvios, e o agente registra — no `03`. PRD e ADR
seguem afirmando o que o código não faz, e quem escreveu o texto o lê como certo. Medido numa
feature real: 31 achados de uma revisão independente pós-"concluída", 27 desta dimensão. A
autolimpeza fica no step 7 da `feature-wiki`; a auditoria por quem não escreveu fica aqui.

### Alterado

- Descrição, índice e gate de esforço: 12 dimensões; **L** em todos os perfis
- "Quando Invocar": explicitamente **antes de abrir o PR** e antes de o `03` dizer "concluída"
- Template do `06` e Checklist Final com a linha da dimensão L

## [1.1.0] — 2026-08-14

### Adicionado

- **Dimensão K — Adequação da Suíte**: as dimensões A–J perguntam se o **produto** está certo;
  esta pergunta se o **instrumento de medição** presta. Dois passos:
  1. **Estático** (nunca pulado, custa segundos): varrer os testes novos do diff procurando
     oráculo ausente ou fraco — teste sem assertion, `assertOk()` sozinho,
     `assertNoJavaScriptErrors()` como assertion única de um CT-B, `assertSee` de texto de layout,
     `assertDatabaseHas` só com a chave, "não lança exceção", `->not->toBe()` sem valor esperado
  2. **Medido** (perfil completo): `pest --mutate` nas classes que o diff introduziu, com cada
     mutante sobrevivente traduzido de volta para a lacuna de derivação que o deixou vivo
- Todo achado da dimensão K vai para o **destino 3**, e a correção é invocar a
  `feature-test-design` com o mutante como entrada — ela fecha a **classe** de lacuna, não só o caso
- Driver de cobertura entra na tabela de entradas, como dependência **opcional** com degradação declarada

### Alterado

- **Destino 3 deixa de terminar no CT que reproduz o achado.** O achado é um mutante que
  sobreviveu; a pergunta seguinte é qual lacuna de derivação o deixou vivo. Fechar só o caso
  garante que o vizinho dele volte na próxima feature
- Achado recorrente entre features vira **linha nova no checklist de taxonomia** da
  `feature-test-design`, e candidato a rule no step 9

### Corrigido

- A skill sugeria `--mutate --covered-only --class="App\\..."`. Medido no projeto de validação:
  **`--class=` não casa de forma confiável** (`--path=` funciona), e **`covers(X::class)` restringe
  o que conta como coberto** — mutante em classe fora do `covers()` vira `uncovered` e o score vai
  a 0% mesmo com os testes executando aquele código em toda chamada
- **Aviso obrigatório sobre o alcance da métrica**: mutation testing só muta código que existe, e
  por isso é **cego à omissão**. Medido: duas suítes com **100% de mutation score cada**
  detectaram 7 e 12 de 18 defeitos plantados. Score alto **não** absolve a dimensão A

> **Nota de correção (2026-09-26).** O 100% das duas suítes não está verificado (Windows, Pest
> 5.0.5, sem `Duration` registrada). O 7 × 12 do juiz está. Ver
> [`experimentos/README.md`](experimentos/README.md#materialização-em-pest-rodada-1-cenário-1).

Etapa de QA dentro do agente — a próxima estação da esteira depois de implementar e rodar os testes. Confronta requisito × plano × app rodando e roteia cada achado.

## [1.0.0] — 2026-08-14

### Adicionado

- Release inicial da skill. O [estudo de viabilidade](.ai/skills/feature-quality-gate/README.md) que a precedeu está no README da skill, com a tabela de como cada exigência do estudo foi honrada no `SKILL.md`
- **5 princípios inegociáveis**: oráculo externo (PRD é alegação, não verdade), separação de poderes (não corrige o que julga), convergência, teto por risco, degradação graciosa
- **Gate de entrada** com tratamento de **oráculo degradado**: wiki sem `00-requisito.md` pede o requisito ao usuário, **proíbe derivar do PRD**, e estampa o aviso no topo do relatório declarando que a dimensão A não foi verificada
- **Gate de esforço por risco** — 3 perfis (mínimo / padrão / completo) por natureza da wiki × superfície de UI × criticidade do domínio. Dimensão fora do perfil é **declarada com motivo**, nunca omitida em silêncio
- **Fluxo de 8 passos**, com a auditoria de ambiguidades do requisito **antes** de validar comportamento (validar contra requisito ambíguo produz achado inválido)
- **Matriz de Rastreabilidade** para detectar **omissão silenciosa** — cláusula sem passo, sem teste e sem código, com tudo verde. Confere o mapa declarado no PRD contra a realidade do diff
- **10 dimensões** com verificação concreta cada uma: cobertura do requisito, fronteiras/dados, matriz de permissão, observabilidade real (**inclui PII vazando no context do log**), performance/N+1, UX de erro, tema e cor, acessibilidade, segurança da superfície nova, regressão adjacente
- **Taxonomia de roteamento em 5 destinos** — especificação / implementação / teste / infra / não-defeito — com tabela severidade (Blocker, Major, Minor, Cosmético), prioridade de destino (**especificação > teste > implementação**) e a tabela "padrão da lacuna → destino", que transforma roteamento em consequência em vez de opinião
- **Convergência**: teto de 3 ciclos, encerramento por ausência de achado novo, dedupe contra o `06` anterior (e não contra os corrigidos, senão achado rejeitado reaparece e o loop nunca fecha), numeração de ciclos no relatório
- **Template do `06-relatorio-qa.md`** com veredito, achados (esperado × observado × repro × evidência × destino × ação exigida), matriz **impressa só se houver lacuna**, tabela de dimensões com status, débitos aceitos, suspeitas não confirmadas e **"Não Verificado"**
- **Delegação ao [`qa-skills`](https://github.com/petrkindlmann/qa-skills) (MIT)** — 7 skills mapeadas, cada uma com **fallback inline** para quando não está instalada; ressalva explícita de **não instalar as 50** (inflação de contexto)
- **Playwright MCP como confronto** — 3 confrontos, com destaque para o **inventário de elementos × cobertura do CT-B** (elemento na tela que nenhum CT-B exercita = lacuna mensurável), sob a regra dos dois destinos obrigatórios: lacuna vira CT-B, defeito vira achado roteado
- **Regressão condicional** pela natureza da wiki: impacto medido via `--parallel --tia`, CT/CT-B da ancestral rodados **por ID**, e heurística **RCRCRC**
- **10 proibições** explícitas, incluindo não alterar código nem teste, não editar o `00`, não reportar achado sem repro mínima e não aprovar com Blocker/Major aberto
- Nota de nomenclatura: **Matriz de Rastreabilidade** por extenso em prosa; sigla **RTM** só em contexto de QA formal / auditoria

### Achados técnicos registrados no desenho

- **Dark mode inverte a regra visão × estrutura da coletânea.** `assertSee('Salvar')` **passa** com texto branco em fundo branco — está no DOM e na árvore de acessibilidade, apenas invisível. E `assertScreenshotMatches()` detecta mudança, não erro: em feature nova ele **cria** o baseline com o bug dentro. Por isso a dimensão G usa 3 níveis (grep estático de classe sem par `dark:` → CT-B com `inDarkMode()` → screenshot via MCP) e traz aviso explícito de que aqui a visão ganha da estrutura
- **A dimensão D é auto-referente**: a `feature-wiki` exige log `[Classe@Método]` com channel e context em toda etapa — e nada no ciclo verificava se isso acontecia

# requirement-to-rule

Transforma decisões e restrições de um requisito em **Project Rules do Laravel Boost** (`.ai/rules/`), com aprovação explícita do usuário.

## [1.3.0] — 2026-09-26

Release 1 do roteiro de
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md)
(§8, itens 1, 2 e 11), "base limpa": **só empacotamento**, sem mudança de comportamento, gate ou
procedimento. O corpo do `SKILL.md` segue com 388 linhas, abaixo das 500 do spec, sem
`references/`.

**Não medido**: esta skill não tem nenhuma execução registrada. A primeira está pendente em
[`experimentos/README.md`](experimentos/README.md#rodadas-pendentes) (Rodadas pendentes, item c),
com partida em `requirement-to-rule-v1.3.0`.

### Alterado

- **Frontmatter conforme o [spec Agent Skills](https://agentskills.io/specification).** `version`
  sai do topo e vira `metadata.version: "1.3.0"` — quem conferia com `grep '^version:'` passa a
  conferir `metadata.version`. Entram `license: MIT`, `compatibility` (Boost ≥ 2.4.12 com Project
  Rules ativas e agente com MCP; o fallback sem `record-rule` que o SKILL já declara; sem MCP, o
  gate 4 — `search-docs` — não é verificado e não há alternativa) e `metadata.requires:
  "laravel/boost>=2.4.12; feature-wiki>=3.1.0"`, sem "opcional" dentro da string, para não quebrar
  um parser futuro; que a `feature-wiki` só conta quando os candidatos vêm da wiki está dito na
  `compatibility` e no README. `npx skills-ref validate` passa
- **`description` reescrita** para o quê + quando + palavras-chave (728 → 788 caracteres). O que
  era procedimento (4 gates, aprovação explícita, índice com uma linha por glob) já estava no corpo
  e saiu da `description`
- **README de 252 para 106 linhas**: por quê (wiki da feature × Project Rule × guideline do
  Boost), quando usar e quando não usar, o que a skill entrega com ponteiro para a seção do
  `SKILL.md` que faz cada coisa, limites e dependências. Gates, escada de enforcement, formato de
  apresentação, modelo e regras do índice, modelo da rule, anti-padrões e o exemplo do
  `search-docs` ficam só no `SKILL.md`

### Corrigido

- **Versão mínima do Boost é 2.4.12, não 2.5.0**: Project Rules e a tool MCP `record-rule`
  entraram na v2.4.12 do laravel/boost (PR #852; ausentes na v2.4.11). O README dizia 2.5.0 desde a
  1.2.1 — a entrada 1.2.1 ganhou nota de correção
- Passo 8, só o parêntese (regra inalterada): os arquivos que o Boost regenera, e que por isso não
  se commitam como as rules, são o `.mcp.json`, os arquivos de guidelines (`CLAUDE.md`,
  `AGENTS.md` etc.) e o `boost.json`, conforme a doc do Boost. Desde o Boost 2.10.0, as guidelines
  do Claude Code vão para o `AGENTS.md`
- README: o link para `experimentos/` vira URL absoluta do repositório (o `boost:add-skill` copia o
  README para `.ai/skills/<skill>/` do projeto, onde `../../../` não leva ao repositório)

### Adicionado

- README, seção **Limites**:
  - não há poda de rule, e o Boost não oferece tool nem comando de remoção; o único gatilho de
    revisão é a tabela `## Conformidade com Rules` do `03`;
  - a escada de enforcement sugere e não prova;
  - o gate 4 depende de `search-docs` (MCP), que a rota `analista` da `feature-wiki` não tem;
  - vindo do step 9, a aprovação é pedida duas vezes;
  - só alcança agentes que leem `.ai/rules/`;
  - nenhuma execução medida em `experimentos/`
- README, dependências com versão mínima: `laravel/boost` 2.4.12; `feature-wiki` 3.1.0, opcional
  (step 9 desde a 2.10.0, `## Conformidade com Rules` do `03` desde a 3.1.0); `feature-test-design`
  em qualquer versão, opcional


## [1.2.1] — 2026-09-26

Patch de documentação, sem mudança de comportamento. Nasce da auditoria interna consolidada em
[`estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md`](estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md) (§7.5).

### Corrigido

- `description` do frontmatter dizia **step 8** da `feature-wiki`; é o **step 9** (o corpo já dizia
  9 desde a 1.2.0 — a `description` é o que o agente lê para decidir invocar)
- README estava em **1.1.0** e também dizia "step 8"
- `pest --arch` não é flag do Pest: em 8 lugares (SKILL e README) virou "teste de arquitetura
  `arch()` do Pest"; o exemplo de código já estava certo
- Passo 7 mandava **editar o índice à mão** com o `record-rule` disponível — a própria skill chama
  isso de anti-padrão e avisa que o Boost regenera o `index.md`. Agora: não editar; conferir depois
  da última chamada
- `record-rule` recebe **um** `glob` por chamada e o `title` é parâmetro próprio: candidato com dois
  globs vira duas chamadas; o `note` leva só o corpo, sem frontmatter nem `#` (issue
  laravel/boost#1034 documenta que uma segunda chamada pode anexar glob à rule existente)
- "Rules carregadas automaticamente por glob" → o Boost **instrui o agente a consultar o índice**;
  o custo de um glob largo é a leitura, não um carregamento
- Cursor listado como agente "sem suporte a `.ai/rules`" — o Boost o suporta; removido
- "3 rules por feature" × "3 candidatos": unificado em **3 candidatos apresentados**
- Passo 1 não lia a tabela `## Conformidade com Rules` do `03` nem o checklist de taxonomia do
  `04`, que a entrada 1.2.0 dizia ter adicionado como fonte

### Adicionado

- URL da doc do Boost (Project Rules) nos dois lugares que a citavam sem link; dependência
  `laravel/boost ≥ 2.5.0` declarada no README

> **Errata (2026-09-26, release 1 do roteiro).** O mínimo declarado acima está errado: Project
> Rules e a tool MCP `record-rule` existem desde a **v2.4.12** do laravel/boost (PR #852; fonte: o
> código e o CHANGELOG do laravel/boost), não desde a 2.5.0. A 1.3.0 declara
> `laravel/boost>=2.4.12`. O mesmo erro está no estudo, §7.5 e §8, que ganhou errata no fim do §7.5.


## [1.2.0] — 2026-08-15

### Adicionado

- **`feature-test-design` como fonte de candidatos**, e a de evidência mais forte: linha nova do
  **checklist de taxonomia de defeito**, nascida de defeito que escapou para produção. Se
  generaliza além da feature, é rule — de preferência com enforcement em `pest --arch`

### Corrigido

- Referência ao step da `feature-wiki` que invoca esta skill: era **step 8**, é **step 9** desde a
  `feature-wiki` 2.10.0, quando o quality gate assumiu o 8

## [1.1.0] — 2026-08-14

### Adicionado

- **Seção "Índice de Rules (`.ai/rules/index.md`)"** com o modelo oficial do Boost reproduzido literalmente (cabeçalho + frase de instrução preservados) — rule fora do índice existe no disco e é **invisível** para os agentes
- **Criação do índice quando não existe**, no modelo oficial, substituindo as linhas de exemplo pelas rules reais do projeto
- **Atualização do índice após a aprovação** do usuário: uma linha por glob, apontando para o arquivo da área
- **Diagnóstico de 3 cenários no passo 2**: índice existe / `.ai/rules/` existe sem índice (rules órfãs e invisíveis) / nada existe — com a regra de **não escrever nada antes do "sim"** do usuário
- **Passo 7 dedicado ao índice** (o antigo passo 7 virou 8), com matriz de ação conforme `record-rule` estar disponível e o índice estar consistente
- 6 regras de manutenção do índice: uma linha por glob, path relativo começando em `.ai/rules/`, ordenação por especificidade, sem linha órfã, sem duplicata, índice não recebe conteúdo de rule
- Verificação final do índice em 4 itens
- 3 anti-padrões novos: não conferir o índice após gravar, deixar as linhas de exemplo do modelo, traduzir/reescrever a frase de instrução
- Fallback ampliado: inclui criar o índice, recuperar rules órfãs e registrar no commit que a gravação foi manual — porque `record-rule` regenera o índice e sobrescreve edição manual
- **`search-docs` como teste empírico do gate 4** (não-redundante): consultar a Documentation API do Boost com a afirmação do candidato — se a doc oficial já responde, é guideline do ecossistema e o candidato reprova
- Exemplo lado a lado de reprovação (`authorize()` de Form Request) e aprovação (scope global de tenant em model específico)
- Nota de cobertura: fora de Laravel 10–13 / Filament 2–5 / Livewire 1–4 / Inertia / Flux / Nova / Pest ≤ 4.x / Tailwind, o gate 4 é avaliado contra a doc oficial do pacote — e restrição sobre pacote de terceiro **pode** legitimamente virar rule
- Anti-padrão novo: avaliar o gate 4 "de cabeça" em vez de verificar com `search-docs`

## [1.0.0] — 2026-08-14

### Adicionado

- Release inicial da skill
- **Tabela das três camadas** — Guidelines (ecossistema, upfront) × Skills (domínio, on-demand) × Rules (a sua aplicação, por glob) — com a regra de ouro: conhecimento de ecossistema nunca vira rule
- **Os 4 gates**: durável, escopável por path, não-inferível, não-redundante — candidato só vira rule se passar em todos, e descarte é comunicado com o gate que falhou
- **Escada de enforcement** (Ponytail aplicado a rules): teste de arquitetura (`pest --arch`) → PHPStan → Rector → Pint → só então prosa
- **Modelo base do conteúdo da rule** com anatomia obrigatória: título imperativo + restrição + **consequência concreta** + escape hatch + enforcement/origem
- Fluxo de 7 passos: coletar candidatos → ler `.ai/rules/index.md` → aplicar gates → subir a escada de enforcement → apresentar e esperar decisão → gravar via `record-rule` → verificar índice e commitar
- **Gravação exclusiva via a tool MCP `record-rule` do Boost** — escrever o arquivo à mão não regenera o `.ai/rules/index.md` e produz rule invisível
- 8 áreas sugeridas de agrupamento com globs (`models`, `controllers`, `requests`, `jobs`, `migrations`, `testing`, `livewire`, `filament`)
- Fallback documentado para `BOOST_RULES_ENABLED=false` ou projeto sem Boost, incluindo atualização manual do índice
- 8 anti-padrões, com destaque para glob `**`, rule sem consequência e inflação de rules
- Teto de **3 rules por feature** e preferência explícita por atualizar rule existente em vez de criar nova
- Delimitação em relação ao `infer-conventions` do Boost: aquele varre o **código existente** (rodar uma vez), este parte do **requisito** (incremento contínuo)

---

# Repositório

Mudanças que não pertencem a uma skill específica.

## 2026-09-26 — release 1 do roteiro

- **CI: [`.github/workflows/skills-ref.yml`](.github/workflows/skills-ref.yml)** roda
  `npx -y skills-ref@0.1.5 validate` em cada `.ai/skills/*/` com `SKILL.md`, em push e pull
  request. Valida todas, acumula as falhas e reprova no fim (estudo, §1 e §8, item 1). Não confere
  o corpo < 500 linhas, que é recomendação do spec, não regra do validador. O pacote npm é um port
  não oficial, em TypeScript, do `skills-ref` — a biblioteca de referência do spec é a Python de
  `agentskills/agentskills`; constantes e campos permitidos conferidos iguais em 2026-09-26. A
  versão fixada não fixa as dependências transitivas (`commander` ^12.1.0, `js-yaml` ^4.1.0)
- **`experimentos/README.md` passa a ser a única tabela de medição da coletânea**: uma linha por
  rodada, com versões, host · modelo, C1/C2 (detectados · cegas · declaradas), total, fonte e a
  coluna **Registro** (auditável / rejulgável / relato / contaminada). READMEs, `SKILL.md` e
  CHANGELOG linkam em vez de copiar
  - rodada 1 corrigida: mediu só o C1, com 12/18; o 17/18 do C2 era da rodada 4. A rodada 2 ganhou
    o resultado real (C2 15/18, `ftd` 1.1.0, piso) e a rodada 4 ganhou número (16/18 e 17/18)
  - rodada 8 contaminada (os conjuntos citam os IDs e as descrições do catálogo), fora de toda
    contagem; rodadas 9 a 11 viram relato (conjunto arquivado em extrato; a 11 é paráfrase, CT a
    CT, da 10); rodadas 12 e 13 só têm placar; a 6 é rejulgável. Das sete rodadas com a
    `feature-test-design` 1.9.0, só a 7 é auditável, e sai "modelos 2025+ convergem em 0
    iterações"
  - tabela defeito a defeito das rodadas 5 a 7: o C1 caiu de 16 para 15 com o total igual,
    reportado como observação de um braço, sem atribuição à 1.9.0
  - o 100% (24/24) de mutation score da materialização fica não verificado (Windows, Pest 5.0.5)
  - nova seção **Rodadas pendentes**: (a) a release de `references/` sem regressão, (b) o perfil
    mínimo da `feature-test-design`, (c) a primeira execução real da `requirement-to-rule` — com
    tags de partida e de chegada e critério de pronto
- **Protocolo**: o prompt reutilizável saiu do README (fixava 1.9.0/3.0.0 e trazia pistas do
  catálogo); [`protocolo/PROMPT-BRACO.md`](experimentos/protocolo/PROMPT-BRACO.md) é a fonte
  única, não fixa versão, pede o `metadata.version` e executa os passos que o perfil de cada área
  manda. [`PROTOCOLO.md`](experimentos/protocolo/PROTOCOLO.md) ganha a rodada de regressão entre
  tags, "sem regressão" definida defeito a defeito, o conjunto conferido contra o catálogo (`grep`
  dos IDs) antes do juiz, o projeto-cobaia limpo de rodadas anteriores e o registro obrigatório
  por rodada (inclusive o modelo do juiz). Errata no `relatorio.html` das rodadas 1 a 4.
  *Como repetir*, passo 2: no Claude Code a skill carregada vem de `.claude/skills/`, e nas cobaias
  esses diretórios são cópias antigas (em 2026-09-26, `demo-wiki` com a `feature-wiki` 3.4.0 e
  `demo-r8` com a 2.10.0). O passo passa a apagar e espelhar também `.claude/skills/<skill>` e a
  conferir, antes do braço, a mesma versão nos dois diretórios
- **README raiz**: versões da release 1; exemplo de frontmatter conforme o spec, com
  `references/`, `{skills}` e `npx -y skills-ref@0.1.5 validate` (a versão do CI); a conferência
  pós-instalação procura `metadata.version` com um padrão que também acha `version:` no topo de
  uma skill antiga (`^\s*version:` no PowerShell, `^[[:space:]]*version:` no bash); instalação no
  Claude Code com o comportamento do Boost 2.10 (o `boost:update` cria `.claude/skills/<skill>`
  como symlink); números de medição trocados por link para a tabela única
  - `ProcessTimedOutException`: o `php artisan test --list-tests` que estoura roda **dentro** do
    `boost:update` que o `add-skill` chama, antes de gravar guidelines e skills (Boost 2.10,
    `InstallCommand::determineTestEnforcement`, timeout padrão de 60 s). Rodar o `boost:update` de
    novo repete o erro; o remédio documentado é definir `enforce_tests` em `config/boost.php`
    (override não documentado na doc do Boost, laravel/boost PR #767) ou espelhar à mão. A Opção 1
    do Claude Code só dá o `.claude/skills/` como pronto se o `add-skill` terminou sem exceção
  - Opção 2 (global, PowerShell): `Copy-Item` com `-Force`; sem ele, a segunda execução — a
    atualização — sai com um erro por diretório
  - Ponytail, passo 1: sai o `php artisan boost:update` incondicional depois do `add-skill` (com
    `boost.json` o `add-skill` já o chama; sem `boost.json` ele falha)
- **Errata do Boost mínimo** (2.4.12, não 2.5.0) na entrada `requirement-to-rule` 1.2.1 e no
  estudo, fim do §7.5

## 2026-08-14

- **Migração da documentação para READMEs por skill.** O `README.md` principal caiu de **1.150 para ~555 linhas** e passou a ser índice da coletânea; o detalhe migrou para o `README.md` de cada skill
  - `feature-wiki/README.md` **novo** — como informar o requisito, os 6 arquivos, testes de browser (Pest + Playwright), Pest 5, Playwright MCP, `search-docs`, dependências e limitações
  - `requirement-to-rule/README.md` **novo** — três camadas, 4 gates, escada de enforcement, índice de rules, modelo base, anti-padrões
  - `feature-quality-gate/README.md` — ganhou a seção **Uso da skill** acima do estudo de viabilidade
  - Convenção documentada: **`SKILL.md` fala com o agente, `README.md` fala com a pessoa** — procedimento vive só no `SKILL.md`, e o `README.md` da skill custa **zero contexto** porque o Boost e o Claude Code leem apenas o `SKILL.md`
- **Instalação com `--all`** no README: `php artisan boost:add-skill gsferro/laravel-ai-skills --all` instala as três skills sem prompt. Documentadas também as demais opções confirmadas no source do Boost (`--list`, `--skill=*`, `--force`, `--skip-audit`) e o aviso de que a `feature-quality-gate` exige a `feature-wiki` ≥ 2.10.0
- **`CHANGELOG.md`** criado, com histórico das duas skills e convenção de tags namespaced
- **Estudo de viabilidade do `feature-quality-gate`** em `.ai/skills/feature-quality-gate/README.md` — skill **ainda não implementada**. Registra a pesquisa de mercado (50 skills MIT do `qa-skills`, QASkills.sh, Playwright Test Agents, ausência de skill de QA no Boost), a lacuna verificada (nenhuma skill do mercado roteia achado de volta para especificação × implementação × teste), os 3 ganhos reais (omissão silenciosa via matriz de rastreabilidade, 10 dimensões não cobertas pelas camadas atuais, taxonomia de roteamento), 2 achados técnicos (dark mode inverte a regra visão × estrutura; MCP como confronto de inventário de elementos × cobertura do CT-B), o mapa construir × reusar e o **critério eliminatório** da skill

## 2026-08-11

- Banner gerado pelo [beyondco.de](https://banners.beyondco.de/) adicionado ao README, com o comando de instalação correto

## 2026-07-02

- Padrão de commit para instalar/atualizar skills documentado no README
- `.idea/` no `.gitignore`

## 2026-06-25

- Commit inicial, documentação de instalação (Laravel Boost e Claude Code) e padrão de estrutura de pastas para novas skills
