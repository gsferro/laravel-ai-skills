# SPDD × coletânea de skills — análise, autocrítica e proposta de integração

> Estudo de 2026-09-04. Objetos analisados: `gszhangwei/open-spdd` (v0.4.18, MIT),
> `geckhardtfiocruz/spdd-lab` (privado, 9 commits), a *Esteira SPDD* (`esteiraspdd.html`,
> design à frente do repositório) e esta coletânea (`feature-wiki` 3.0.0 +
> `feature-test-design` 1.9.0 + `feature-quality-gate` 1.1.0 + `requirement-to-rule` 1.2.0).
>
> Contexto: o `spdd-lab` é conduzido pelo gerente do autor desta coletânea. Este documento
> existe para decidir **o que juntar**, não para eleger um vencedor.

---

## Sumário executivo

**SPDD e a coletânea não competem. Elas são as duas metades do mesmo problema, e cada uma é
cega exatamente onde a outra enxerga.**

O SPDD resolve o problema **organizacional**: quem decide, quando trava, o que fica registrado,
como o conhecimento sobrevive à saída de uma pessoa. Ele tem elicitação a partir da reunião,
proveniência no nível da fala, papéis com limite de decisão explícito e portões com dono
nomeado. Não tem nenhuma verificação mecânica, nenhum critério de suficiência de teste e
**nenhuma medição**.

A coletânea resolve o problema **epistêmico**: como saber que o que foi entregue é o que foi
pedido, quando o mesmo agente leu o requisito, escreveu o plano, escreveu o teste, implementou e
rodou o teste. Ela tem derivação formal de caso de teste, gate de falsificabilidade por mutante,
matriz de rastreabilidade contra omissão silenciosa e 13 rodadas de experimento com juiz cego.
Não tem elicitação, não tem papéis, não tem portão com dono, **e não tem reparo de deriva**.

O ponto de encaixe mais forte é preciso e verificável: **os passos 2 e 7 do SPDD — casos de teste
e validação — são os únicos dois sem comando, e são justamente os do QA**, o papel que o método
declara ser o mais beneficiado. É exatamente onde a `feature-test-design` e o
`feature-quality-gate` vivem.

E há um prêmio maior. O levantamento do estado da arte mostra que **a lacuna nº 1 admitida pelo
campo inteiro** — Spec Kit, Kiro, BMAD, Tessl, OpenSpec — é a mesma: *ninguém tem mecanismo que
falhe o build quando um requisito não tem teste correspondente.* A junção proposta aqui entrega
exatamente isso.

**Recomendação: Opção B — duas camadas com contrato de interface** (§7.2). SPDD é o processo do
squad; a coletânea é o motor de engenharia. O contrato entre elas é o **arquivo de história** e o
**ID de cláusula**.

---

## 1. O mapa do terreno — quatro objetos, não dois

Antes de comparar, é preciso separar coisas que estão sendo tratadas como uma só.

| # | Objeto | O que é | Estado |
|---|---|---|---|
| 1 | **OpenSPDD** (`gszhangwei/open-spdd`) | CLI em Go + 10 templates de comando. O método bruto | v0.4.18 (jul/2026), 737 ★, MIT, **sem commit há ~3,5 meses** |
| 2 | **spdd-lab** (`geckhardtfiocruz/spdd-lab`) | Camada de governança sobre o OpenSPDD: acordo do squad, normas, portões, papéis, tradução Java→PHP | Privado, 9 commits, **tudo em um dia** (02/09/2026), 1 contribuidor, sem licença |
| 3 | **Esteira SPDD** (`esteiraspdd.html`) | **Design à frente do repositório.** Descreve uma versão que ainda não existe | 03/09/2026 — 1 dia depois do último commit do lab |
| 4 | **Esta coletânea** | 4 skills + protocolo experimental + 13 rodadas medidas | `feature-wiki` 3.0.0, ativa |

### 1.1 A esteira é um design, não o repositório

Confirmei por clone e `git log`. A esteira introduz o que o `spdd-lab` **não tem**:

| Novidade da esteira | No repo? |
|---|---|
| `config/project.yml` com os 4 aprovadores nomeados | ❌ |
| `config/stack-profiles/` (.NET, Laravel, Java, `generic.yml`) | ❌ |
| `config/tool-profiles/` (GitHub, GitLab, Azure DevOps) | ❌ |
| `scripts/bootstrap.sh` / `.ps1` | ❌ |
| `/spdd-gate N ... aprovador:"<nome>"` como **comando** | ❌ — portões eram texto no acordo |
| `/spdd-evidence` — dá comando ao passo 7 | ❌ |
| `/spdd-contract` (renomeia `/spdd-reasons-canvas`) | nome antigo |
| `pendencias/Q-XX.md` e `contradicoes/CTR-XX.md` como **arquivos** | eram seções na história |

O próprio rodapé admite: *"A documentação de apoio do repositório ainda está sendo atualizada
para refletir esta versão."*

**Isso é bom.** A esteira corrige, sozinha, três das lacunas mais graves do lab: portão sem
mecanismo, passo do QA sem comando, e método preso a uma stack. Ela também externaliza pendência
e contradição em arquivos — o que as torna rastreáveis por `grep` e traváveis por script, em vez
de seções que alguém precisa lembrar de reler.

### 1.2 O problema arquitetural da esteira

> *"Cada squad clona sua própria cópia deste repositório — **é a esteira em si, não uma
> biblioteca instalada dentro do repositório do produto**."*

Se a esteira mora **fora** do repo do produto, então:

- `/spdd-analysis` precisa explorar um código que não está na pasta em que o agente foi aberto;
- `/spdd-generate` gera código onde?
- `/spdd-code-review` compara contra qual árvore?
- a rastreabilidade requisito → código perde a âncora do git: não há branch, não há diff, não há PR
  que amarre a história ao commit.

A `feature-wiki` resolve isso por construção: a wiki vive em `wikis/specs/{branch}/{feature}/`
**dentro** do produto, com o caminho **derivado do branch** (`git rev-parse --abbrev-ref HEAD`).
Requisito, plano, teste, progresso e código viajam no mesmo commit, no mesmo PR, na mesma
revisão.

**Recomendação imediata, independente de qualquer integração**: a esteira deve ser distribuída
como **template instalável dentro do repo do produto** (o que o `openspdd init` já faz para
`.claude/commands/`), não como repositório paralelo. Os `config/*.yml` e `templates/` vão junto.
O que pode ser repositório separado é o *pacote de método* (`[GENÉRICO]`), que se copia; não o
espaço de trabalho.

---

## 2. As duas filosofias, frente a frente

### 2.1 SPDD — o prompt é o contrato

SPDD = **Structured Prompt-Driven Development**. Não é *Spec*-Driven, e o `spdd-lab` faz questão
de dizer isso: *"Não confundir com SDD, em que o artefato mantido é a especificação."*

Tese literal do OpenSPDD:

> **The core insight**: Plans are "suggestions", REASONS Canvas is a "contract".

E o princípio operacional:

> *"When reality diverges, fix the prompt first — then update the code."*

O ensaio (`docs/design-philosophy.md`, 39 KB) é a melhor peça do repositório e merece leitura
integral. A distinção fundadora:

> **Capability dimension** — Can AI understand requirements, generate correct code…? This
> dimension is continuously improving with model evolution.
> **Control dimension** — How to ensure AI's understanding aligns with your intent, how to pick
> the one you want among multiple 'correct' solutions, how to define what must not be done.

> *"when multiple 'correct' solutions exist, choosing which one is a **human trade-off decision,
> not an AI logical inference**."*

O argumento mais forte é o da "IA perfeita":

> *"Suppose AI reaches 'perfection' — infinite context, zero hallucination… a truly 'perfect'
> AI's most likely response wouldn't be generating code directly, but **asking follow-up
> questions**. But this precisely proves the point: even if AI is smart enough to know what to
> ask, these decisions still need to be made by humans, **and they need to be recorded**. AI's
> questions don't produce decisions; human answers do."*

E o conceito de **negative space**, que é a contribuição conceitual central:

> *"You: 'Implement this Service' / AI: [Added a caching layer you didn't ask for] [Decided on an
> exception retry strategy on its own] [Placed the transaction boundary at the caller instead of
> the service]. Each item individually seems 'reasonable,' but together they diverge from your
> design intent… **AI lacks this sense of boundaries**."*

Daí o REASONS Canvas em três camadas:

```
R Requirements  · E Entities · A Approach     → camada estratégica (por quê / o quê)
S Structure     · O Operations                → camada de implementação (como)
N Norms         · S Safeguards                → camada de restrição (o que NÃO)
```

> *"**All three are essential: without N+S, AI improvises; without S+O, AI restructures
> arbitrarily; without R+E+A, AI lacks context.**"*

### 2.2 Coletânea — o requisito bruto é o oráculo, e o plano é alegação

A tese da coletânea está no `feature-quality-gate`:

> **1. Oráculo externo — o PRD é alegação, não verdade.**
> *"o mesmo agente leu o requisito, escreveu o PRD, escreveu os CTs, implementou e rodou os
> testes. Se entendeu errado, errou coerentemente cinco vezes e tudo está verde. Validar contra
> o PRD confirma o erro; validar contra o requisito o expõe."*

E na `feature-test-design`:

> **1. O caso de teste deriva do requisito, nunca do código.**
> **2. Cenário sem mutante morto não é caso de teste.**

O `00-requisito.md` é **verbatim e imutável**; a decomposição em `RQ-##` é derivada e revisável.
A ambiguidade é achado, não algo a "melhorar" na transcrição.

### 2.3 O desacordo, formulado com precisão

Aqui está a divergência real, e ela não é de estilo:

> **Um artefato não pode simultaneamente (a) ser atualizado para descrever o que o código faz e
> (b) servir de oráculo para julgar se o código está certo.**

O SPDD faz (a) explicitamente. Princípio literal do `/spdd-sync`:

> *"The structured prompt should always reflect the **actual** implementation, not just the
> **planned** implementation."*

E supõe (b) no `/spdd-code-review`, que compara código × contrato nas 7 dimensões.

Depois de um `/spdd-sync`, o `/spdd-code-review` está comparando o código com um documento que
acabou de ser ajustado para descrevê-lo. **O desvio some por construção.**

O SPDD tem uma defesa, e ela é boa: existe uma âncora **acima** do contrato — a história — e o
sync é proibido de tocar duas seções:

> *"Do NOT change **Requirements** section unless user explicitly requests (business goals
> shouldn't change from code refactoring)"*
> *"Do NOT change error messages in Safeguards unless they **actually changed in code**"*

Isso é o desenho certo. **O problema é que nada re-verifica história ↔ contrato depois do sync.**
O Portão 2 (contrato aprovado) já passou; o sync acontece no passo 8, depois do Portão 3. Não há
retorno ao Portão 2. A cadeia `insumo → história → contrato → código` tem reparo só no último
elo.

E a defesa é **textual, dirigida a um LLM**. O próprio ensaio admite:

> *"they are **fundamentally soft constraints: AI can reference them and may also deviate from
> them**… what truly makes AI output controllable is not just 'more structured expression' but
> also a **machine-verifiable validation loop**."*

O OpenSPDD entrega apenas a camada do meio. Ele diz isso de si mesmo.

**E o espelho:** a coletânea não tem `/spdd-sync` **nenhum**. A wiki é um retrato do momento da
implementação. Depois do merge, o `01-plano-acao.md` começa a envelhecer e nada o repara. A
defesa da coletânea é que a parte viva deve migrar para `.ai/rules/` via `requirement-to-rule` —
o que é uma resposta legítima, mas **está implícita e não declarada**, e cobre convenção de
código, não desenho de feature.

**Cada um tem metade da resposta.** O SPDD sabe reparar e não sabe verificar. A coletânea sabe
verificar e não sabe reparar.

---

## 3. Autocrítica — onde esta coletânea é fraca

Esta seção é o item que foi explicitamente pedido. Sem atenuação.

### 3.1 A coletânea não tem montante. Começa depois da parte mais cara

A `feature-wiki` começa em *"o requisito chegou"*. O `00-requisito.md` manda colar o texto do
card *"como está"*. Mas **o card já é uma interpretação** — de uma conversa, de uma reunião, de
um e-mail. A coletânea trata o card como fonte da verdade de alta fidelidade quando ele pode ser
a compressão com perda mais cara da cadeia.

O SPDD começa um passo antes, e o resultado é mensurável no exemplo real do lab. O
`/spdd-story` leu 41 minutos de transcrição e:

- classificou cada item em RF / RNF / RN / P / R / Q / CTR;
- registrou **origem no nível da fala**: `Marta · 04:40`, `Paulo Serra · 11:58`;
- pegou uma **contradição a 28 minutos de distância** (`Marta · 12:30` × `Marta · 40:15`);
- recusou-se a inventar o número de um RNF: *"tem que ser rápido"* saiu como `[A CONFIRMAR]` e
  virou a pendência Q-01;
- reprovou a própria saída na análise INVEST.

**Nada disso existe na coletânea.** E o `00-requisito.md` não tem campo de origem: a `RQ-01` cita
o "trecho literal" do card, mas não *quem disse, quando*. Se o card estiver errado, a wiki fica
coerentemente errada e a rastreabilidade não tem para onde apelar.

> **Autocrítica dura**: o `00-requisito.md` chama a si mesmo de *"a única linha de base
> independente do agente"*. Isso é verdade em relação ao **agente**, e falso em relação à
> **cadeia**. Ele é independente do agente que escreve o PRD, mas não é independente de quem
> escreveu o card. A coletânea trocou uma cegueira correlacionada por outra, menor, e declarou
> vitória.

### 3.2 Os portões da coletânea não têm dono

O `feature-quality-gate` é executado **pelo agente**. O step 9 pergunta ao usuário. O checklist
diz *"Confirmar com usuário se o plano está correto"*.

Quem é "o usuário"? Quem estiver no teclado.

O `spdd-lab` acerta em cheio nessa crítica, e a frase é boa demais para não citar:

> *"Portão sem dono não é portão: é sugestão."*

Numa squad com PO, QA, líder técnico e DEV, "confirmar com o usuário" é indefinido. A coletânea
foi desenhada para **um dev com um agente** — e nesse contexto está certa. Para squad, não
serve como está.

### 3.3 O experimento mede um elo, e o número é apresentado como se medisse a esteira

Este é o ponto mais sério.

Todas as 13 rodadas medem **o step 4** — a derivação de caso de teste — contra um **oráculo
fixo** (`00-requisito.md` e `01-plano-acao.md` congelados em `protocolo/oraculo-fixo/`). O
protocolo é rigoroso: braços independentes, catálogo escrito antes, juiz cego com citação
literal obrigatória, ônus da prova no conjunto. Isso é ciência de verdade e não tem equivalente
em nenhum dos concorrentes.

**Mas o que ele não mede:**

| Elo da esteira | Medido? |
|---|---|
| Captura do requisito (`00`) a partir de um card real | ❌ — o `00` é dado pronto |
| Qualidade do PRD (`01`) | ❌ — o `01` é dado pronto |
| Derivação de CT (`04`/`05`) | ✅ **13 rodadas** |
| Implementação | ❌ |
| `feature-quality-gate` — as 11 dimensões, o roteamento, a matriz | ❌ **nunca medido** |
| `requirement-to-rule` | ❌ |
| Ganho de ponta a ponta (defeito em produção, retrabalho, tempo) | ❌ |

O `README.md` apresenta "83,3% / 100%" logo abaixo do título da coletânea. Um leitor razoável
entende que isso qualifica **a coletânea**. Qualifica **uma skill, num passo, com as entradas
congeladas**.

> A convergência entre 6 famílias de modelos (R7–R13) é um resultado forte e honesto — mostra
> que a técnica domina o modelo. Mas ela também expõe o outro lado: os **mesmos 3 defeitos**
> (D14 fuso horário, D15 soft-delete, D18 idempotência) morrem em nenhuma rodada, em nenhum
> modelo. São lacunas *declaradas*, o que é honesto — mas são exatamente as que um QA humano
> pegaria. **Zero variância entre modelos significa zero chance de um deles pegar o que os
> outros perdem.** A parceria humana do SPDD é uma fonte de variância que a coletânea não tem.

### 3.4 A citação-fundamento está superestimada

Verifiquei o artigo diretamente. `arXiv 2607.22883` é real, correto no tema e no sentido do
efeito — *"Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit
Tests"* (Zhao, Zhou & Cohen, 24/07/2026). Mas os números foram lidos errado.

| Condição no prompt | Testes enganados | Testes eficazes |
|---|---:|---:|
| Código **corrigido** | 0,46% | 8,51% |
| Código **defeituoso** | 3,84% | 2,98% |
| **Especificação** (*Only Doc.*) | **2,69%** | **4,50%** |

O `README.md` e o `SKILL.md` afirmam que derivar do código em vez da especificação *"multiplica
por ~8"* (0,46% → 3,84%) e *"derruba por ~3"* (8,51% → 2,98%), e que a especificação *"reverte os
dois números"*.

`0,46%` e `8,51%` são a condição de **código corrigido**, não de especificação. O contraste real
código-defeituoso × especificação é **3,84% → 2,69%** (≈1,4× menos enganados) e **2,98% → 4,50%**
(≈1,5× mais eficazes). A especificação **mitiga** o efeito; não o reverte.

Também: o artigo usa **318 métodos focais cobrindo 233 defeitos**, não *"318 defeitos"*.

**O princípio nº 1 sobrevive** — a direção do efeito está confirmada com 11 modelos de 6
fornecedores, e o Konstantinou et al. (`arXiv:2607.05139`) mede o mesmo com números maiores
(14% × 25% de eficácia de detecção). Mas a evidência que de fato sustenta a skill é **o
experimento interno**, não a citação externa. A citação está carregando mais peso do que aguenta.

**Correções a aplicar** no `README.md` e no `.ai/skills/feature-test-design/SKILL.md`:
`~8×` → **~1,4×**; `~3×` → **~1,5×**; *"reverte"* → **"mitiga"**; *"318 defeitos"* → **"318
métodos focais cobrindo 233 defeitos"**.

### 3.5 O custo de operar nunca foi medido

O protocolo mede `DDR`, `N_CT`, `DDR/N_CT`, `AMB`, `TAUT`, `FALSO_OK`. Todas são métricas de
**eficácia de teste**. Nenhuma mede o custo da wiki.

Não sabemos: tokens por feature, tempo de parede até o primeiro commit, quantas features foram
abandonadas no meio da wiki, quantas vezes o step 6 (ponytail-review) reprovou o plano, quantos
ciclos o quality gate consome na prática.

Isso importa porque a `feature-wiki` é **pesada**: 9 steps, ~10 arquivos, `SKILL.md` de 1.563
linhas, 4 skills companheiras, mais Ponytail, Caveman, Boost, Pest 5, Playwright e MCP. A
documentação oficial do Claude Code é explícita sobre o risco:

> *"**Bloated CLAUDE.md files cause Claude to ignore your actual instructions!**"*

E a própria Anthropic define bom contexto como *"the smallest possible set of high-signal tokens"*,
invocando **context rot** — a acurácia de recall **cai** conforme os tokens sobem.

> **A contradição não resolvida no coração de todo SDD, e a coletânea não escapa dela**: o método
> pressupõe que mais especificação escrita melhora a saída; a evidência de engenharia de contexto
> diz o contrário. Ninguém publicou a curva de onde o retorno vira negativo. A coletânea tem o
> instrumento para medir isso — o protocolo — e nunca apontou para si mesma.

O `spdd-lab` é mais maduro aqui, e devia envergonhar um pouco: ele tem **poda obrigatória** na
semana 5 (*"Corte o que virou burocracia. Um processo que ninguém pode podar vira um processo que
todos contornam."*) e uma **cláusula de parada** na semana 6 (*"Piloto que só pode dar certo não é
piloto, é encenação."*). A coletânea não tem ritual de poda nem critério de morte.

### 3.6 Não há reparo de deriva

Já desenvolvido em §2.3. A wiki é um retrato. `/spdd-sync` e `/spdd-prompt-update` não têm
equivalente. Depois do merge, o `01-plano-acao.md` é documentação que envelhece — e o ensaio do
OpenSPDD tem a frase certa para isso:

> *"if the code changes but the Canvas doesn't get updated, it transforms from a 'design guide'
> into '**misleading outdated documentation**', which is **more dangerous than no documentation at
> all**."*

### 3.7 A coletânea não viaja entre stacks

Todo o conteúdo concreto é Laravel/Filament/Livewire/Pest. A esteira do SPDD já prevê
`config/stack-profiles/` com .NET, Java, Laravel e um `generic.yml`. Para um departamento com
mais de uma stack — que é o caso — a coletânea, como está, não é adotável fora do PHP.

A separação está mal feita: a **técnica de derivação** (SFDIPOT, partição, valor limite, tabela
de decisão, matriz estado × operação, gate de mutantes) é agnóstica de stack; a **alocação de
camada** e os comandos são específicos. Hoje as duas vivem no mesmo arquivo.

### 3.8 Sem enforcement mecânico

As skills são markdown lido por um agente. Não há hook, não há CI, não há check de PR. Se o
agente pular o step 8, nada acontece. É a mesma crítica que se faz ao SPDD, e ela vale para os
dois — com a diferença de que a coletânea *podia* ter isso hoje: Claude Code tem hooks
`PreToolUse` e `Stop`, e a documentação oficial classifica o **Stop hook** como o degrau
determinístico da escada de verificação.

### 3.9 Duas coisas que a coletânea tem e o SPDD não tem, e que valem registro

Para não ser injusto na direção contrária:

1. **O critério de suficiência.** *"Toda regra tem seus mutantes previstos mortos"* — contra
   *"todo AC tem CT"*, que mede existência. É a diferença entre 7/18 e 16/18.
2. **A proibição de autorrevisão** e o contrato do sub-agente de CT-B: *"Alterar código de
   aplicação para o teste passar"*, *"Relaxar assertion para ficar verde"*, *"Remover CT-B que não
   passou"* — tudo proibido, com a classificação obrigatória da falha em (a) CT errado / (b)
   implementação divergente / (c) flake, e a regra de que **(b) vermelho é resultado válido**.
   Kent Beck relata exatamente a falha oposta como o modo de falha mais comum de agentes:
   *"agentes apagam ou reescrevem testes que falham para fingir aprovação"*. Nenhum framework do
   levantamento traz proteção contra isso. Esta traz.

---

## 4. Crítica ao SPDD

### 4.1 O contrato é gerativo — então testar contra ele é tautológico

`/spdd-generate` gera o código **a partir** do contrato. `/spdd-code-review` compara o código
**contra** o contrato. É a cegueira correlacionada em forma pura: o mesmo documento é a fonte da
geração e o oráculo da verificação.

O SPDD tem uma defesa, e é engenhosa: **o passo 2 (casos de teste do QA) é declaradamente
paralelo ao passo 3**, derivado da **história**, não do contrato. O acordo diz:

> *"Os passos 2 e 3 são paralelos. O 2 **nunca** vem depois do 5 — é o que tira o teste do fim da
> fila."*

Isso é o desenho certo, e é a mesma intuição do `00-requisito.md`.

**O problema**: esse é o passo **sem comando, sem técnica e inteiramente dependente da
disciplina humana**. O mecanismo antitautológico mais importante do método é também o menos
apoiado dele.

### 4.2 O caso de teste do QA é bom para um artefato sem técnica — e é insuficiente

Li o exemplo real (`tests/casos-de-teste/aprovacao-solicitacao-compra.md`). Ele pega, por
instinto:

- **CT-06** motivo só com espaços → normalização (≈ D17 do catálogo da coletânea);
- **CT-09** acesso direto por URL → IDOR (≈ E07);
- **CT-07** decisão concorrente em duas abas → race (≈ E15);
- **CT-04** estado vazio explícito — *"área em branco reprova o caso"*.

E a seção **"Cenários que o QA acrescentou"** é uma invenção que a coletânea não tem, com uma
frase que devia ser copiada: *"Se esta seção estiver vazia, o QA leu a história mas não a
interrogou."*

O que falta é exatamente o que foi medido:

| Elemento do pipeline `feature-test-design` | No CT do lab? |
|---|---|
| Rastreio AC → CT | ✅ e bem feito |
| Estado vazio, race, IDOR, normalização | ✅ por instinto |
| Análise de valor limite (BVA 3 valores) | ❌ |
| Matriz estado × operação em produto cartesiano **fechado** | ❌ |
| Tabela de decisão · pairwise | ❌ · ❌ |
| **Mutante previsto por cenário** | ❌ — nenhum CT declara o que mata |
| Alocação de camada (Unit / Feature / componente / Browser) | ❌ — só *"Automatizável: sim"* |
| Oráculo forte | ⚠️ CT-10 é declaradamente fraco (*"continua utilizável"*) |

E o critério de suficiência é **"todo AC tem CT"**: 10 CTs para 7 ACs, razão 1,43. É a mesma
família da patologia medida na auditoria das 9 wikis reais (razão CT/RQ = 1,11, DDR 7/18). Sem
catálogo de mutantes plantados não dá para afirmar o número, mas a **assinatura estrutural é a
mesma**: cobertura determinada pelo gabarito, não pela estrutura do problema.

### 4.3 Zero verificação mecânica, e o próprio ensaio sabe disso

- Sem hooks, sem CI (o `open-spdd` tem **142 funções de teste e nenhum workflow que as rode** —
  só `release.yaml`);
- sem lint de canvas, sem schema;
- **nenhum teste unitário no fluxo core** — não existe `/spdd-unit-test`;
- o único teste automatizado (`/spdd-api-test`, opcional) **só compara status HTTP**. O corpo da
  resposta é impresso para inspeção humana e nunca asserido, porque o template proíbe
  dependências externas (`Do NOT use external tools like jq, yq, or python`). Os valores de
  negócio esperados vivem em **comentários** no topo do script.

> Ou seja: o único gate de teste automatizado do método verifica que a API respondeu `201`, não
> que ela calculou `R$ 1,50`. É um caso quase caricatural de suíte que passa sem verificar o que
> importa — exatamente o `TAUT` do protocolo da coletânea.

### 4.4 Rastreabilidade canvas → código não existe

Não há ID estável de requisito nos canvases do OpenSPDD (verificado por grep nos 7 canvases
reais: nenhum `RF-`, `REQ-`, `AC-N`). A amarração é **por nome de arquivo**
(`{JIRA}-{TIMESTAMP}-[{ACTION}]-{escopo}-{desc}.md`). Nenhum comentário, tag ou anotação no
código aponta de volta ao canvas.

Pior: `/spdd-generate` manda cruzar com a *"Acceptance Criteria Traceability table (**if
present**)"* — e **nenhum template produz essa tabela**. É referência a um artefato que o método
não gera.

**O `spdd-lab` corrige isso e é a melhor contribuição dele**: a história tem IDs tipados estáveis
(`P-`, `R-`, `RN-`, `RF-`, `RNF-`, `Q-`, `CTR-`), com regra de numeração (*"Item removido deixa a
lacuna na numeração — número não se reaproveita"*). Isso é superior ao `RQ-##` plano da
coletânea (§7.3).

### 4.5 Sem ciclo de vida de artefato — confirmado pelo autor

Issue #12 do OpenSPDD, resposta literal do autor:

> *"At the moment, however, **there is no formal lifecycle mechanism to mark an older analysis or
> prompt as stale, superseded, or deprecated**… I also would not rely on timestamp alone… So this
> is more of a **semantic lifecycle problem** than a simple date-ordering problem."*

Sem índice, sem `supersedes`/`superseded-by`, sem status. Com o tempo, `spdd/prompt/` acumula
documentos que podem se contradizer.

### 4.6 Zero medição, e o repositório upstream está parado

O OpenSPDD não tem uma única métrica reprodutível. A única alegação do ensaio é auto-hedgeada:

> *"some features that previously required days of iterative adjustment can be completed in hours…
> Of course, **this efficiency difference is highly dependent on project type and task complexity
> and should not be generalized**."*

O artigo do martinfowler.com traz um *"intent alignment (~99%)"* **sem definição operacional nem
procedimento de medição**.

E a atividade caiu: 18 commits em mar/2026 → 0 em jun → 5 em jul → 2 em ago → 0 em set. Último
release v0.4.18 em 02/07/2026. **~3,5 meses sem commit**, 41 de 45 commits de um único autor.

O `spdd-lab` já mitiga isso com honestidade: *"A ferramenta é jovem (v0.4.x, um mantenedor). O
processo não depende dela: se a CLI sumir, os documentos e os portões continuam valendo."* Está
certo — mas vale dimensionar quanto se quer investir em customizar templates de um upstream
parado.

### 4.7 O `spdd-lab` está em estado "Semana 0"

Autocrítica que o lab merece ouvir, e que ele em boa parte já declara:

- **Todos** os campos `[POR PROJETO]` estão vazios. `CLAUDE.md` diz literalmente *"Nada
  específico ainda."* Nenhum aprovador nomeado, nenhum banco, nenhum prefixo de ticket.
- **Sem licença** (`"license": null`) — num repositório cuja mecânica `[GENÉRICO]`/`[POR PROJETO]`
  pressupõe ser copiado por outros squads. É um bloqueio formal à própria tese.
- **Item 5 da Definição de Pronto ainda é placeholder** (`<homologação do usuário? script de
  rollback?>`). A DoD está literalmente incompleta.
- `/spdd-code-review` (623 linhas, o maior arquivo), `/spdd-generate` e `/spdd-sync` **nunca foram
  customizados** — seguem 100% em inglês e não referenciam o acordo do squad, as normas do
  projeto, os portões nem a DoD.
- A tabela de tradução Java→PHP é **manual e não verificável**. Nada trava um canvas que a
  ignore.
- A simulação é ficcional e o relatório diz isso em destaque, o que é exemplar: *"nenhuma pessoa
  real decidiu nada nesta simulação."*

### 4.8 A lacuna mais grave, e ela não está declarada: dados pessoais em `insumos/`

Transcrições de reunião com cliente da Fiocruz/Fundep entram **inteiras** num agente de IA. O
repositório não menciona LGPD, anonimização, classificação da informação, nem retenção de
`requirements/insumos/`.

E o próprio exemplo simulado contém um requisito de *"não exibir dado pessoal de bolsista"* e uma
restrição de política de segurança da informação — ou seja, o método já sabe que o domínio tem
dado sensível, e não protege o insumo que o carrega.

Num contexto institucional público, isso não é detalhe de conformidade: é o item que pode parar
o piloto. **Deve virar Portão 0**, antes do Portão 1. Ver §7.6.

---

## 5. Onde os dois estão, no estado da arte

Usando a taxonomia de Birgitta Böckeler (Thoughtworks, no site do Martin Fowler): *spec-first*
(descartada depois) → *spec-anchored* (persiste e é refinada) → *spec-as-source* (humanos só
editam spec).

| | Nível | Unidade | Gate humano | Enforcement duro | Rastreio req→**teste** | Medição |
|---|---|---|---|---|---|---|
| **Spec Kit** | spec-first | feature (branch) | ❌ nenhum formal | templates + `/analyze` | ❌ | ❌ |
| **Kiro** | spec-first | spec | ✅ **bloqueante** entre fases | **hooks** (`PreToolUse` bloqueia) | ❌ | ❌ |
| **BMAD** | spec-first | story | ✅ vários | workflows restringem campos | ⚠️ fraca (issue #1930) | ❌ |
| **Tessl** | **spec-as-source** | arquivo de código | revisão da spec | **testes via `@test`** | ✅ **único** | ❌ |
| **OpenSpec** | **spec-anchored** | change proposal | ✅ antes de codar | `validate --strict` | ❌ | ❌ |
| **SPDD** | spec-anchored (aspira) | história/canvas | ✅ 4 portões nomeados | ❌ **nenhum** | ❌ | ❌ |
| **Coletânea** | spec-first (retrato) | feature (branch) | ⚠️ sem dono | ❌ nenhum | ✅ **`RQ`→CT→mutante** | ✅ **13 rodadas** |

Três leituras:

**(1) A coletânea é, com o Tessl, uma das duas únicas com rastreabilidade requisito → teste.** E
é a única com **critério de falsificabilidade** (mutante previsto morto), o que é mais forte que
o `@test` do Tessl — que amarra teste a capability sem exigir que o teste discrimine. O Tessl,
além disso, está há ~9 meses em beta fechado.

**(2) A coletânea é a única com medição.** Zero estudos revisados por pares ou metodologicamente
transparentes sobre Spec Kit, Kiro ou BMAD até set/2026. Os números que circulam ("3–10× de
sucesso de primeira passada") são marketing sem metodologia. Enquanto isso, a evidência **contra**
o cenário amplo é robusta: METR (RCT, 16 devs, 246 tarefas, **−19% de velocidade** com IA);
*SWE-Bench Illusion* (ICSE-SEIP 2026 — 76% → ~53% de acurácia fora do benchmark, ~32,67% dos
patches com vazamento de solução); GitClear (duplicação de blocos +81% de 2023 a 2026;
copy/paste superou refatoração pela primeira vez em 2024); DORA 2025 (relação negativa com
estabilidade de entrega persiste).

**(3) O SPDD é o mais forte em governança de squad, e é o único com portão nomeado por papel.**
O Kiro tem gate bloqueante, mas é *"do the requirements look good?"* dirigido a quem está no
teclado. Portão com **aprovador nomeado em arquivo de configuração** é uma ideia que não aparece
em nenhum outro framework do levantamento.

### 5.1 A lacuna que ninguém fechou — e que a junção fecharia

Do levantamento, a lacuna nº 1 do campo, literal:

> Nenhum framework tem mecanismo que **prove** que todo requisito foi implementado *e testado*. O
> que existe são aproximações: `/speckit.analyze` (LLM checando LLM), `_Requirements: 1.1_` do
> Kiro (declaração de intenção, não verificação), `/speckit.converge` (LLM julgando LLM). E as
> métricas usadas são estruturalmente cegas: **cobertura mede linhas que existem; mutation score
> mede mutantes de código que existe.** Um requisito nunca implementado é invisível às duas. Não
> há *requirements coverage* automatizada em nenhuma ferramenta SDD — algo que o **DO-178C** exige
> há décadas na aviação.

Isso é literalmente a razão de existir do `feature-quality-gate` (dimensão A — omissão silenciosa)
e é o achado registrado em `MEMORY.md` desta coletânea: *mutation score saturou em 100% para duas
suítes de qualidade muito diferente*.

E o campo também admite a lacuna nº 7:

> Ninguém resolve o auto-conluio. **Nenhum framework SDD impõe estruturalmente que os testes
> sejam derivados da spec e não da implementação** — o Article III do Spec Kit ("Test-First,
> NON-NEGOTIABLE") é a tentativa mais próxima, mas é regra em prosa num markdown, sem enforcement
> mecânico.

**SPDD + coletânea + os hooks do Claude Code resolvem as duas.** Isso não é integração
incremental — é a coisa mais adiantada que existe nesse eixo específico. Vale dizer isso ao
gerente com todas as letras.

---

## 6. Prós e contras, lado a lado

### 6.1 SPDD (esteira + lab + OpenSPDD)

**Prós**

| # | O quê |
|---|---|
| 1 | **Elicitação a partir da reunião** — `/spdd-story` lê `.vtt` inteiro, classifica RF/RNF/RN/P/R, com origem no nível da fala |
| 2 | **Proveniência** — `Marta · 04:40`. Contradição a 28 min de distância detectada |
| 3 | **"Nenhum número sai da máquina"** — RNF sem critério mensurável vira pendência, nunca valor inventado |
| 4 | **IDs tipados e estáveis**, com regra de não-reaproveitamento de número |
| 5 | **Pendência e contradição como objetos de primeira classe** (`Q-XX`, `CTR-XX`) — com dono, status, e que **travam** |
| 6 | **Papéis com limite de decisão explícito** — inclusive a coluna *"o que NÃO decide"* |
| 7 | **Portões com aprovador nomeado** em `config/project.yml` |
| 8 | **Reparo de deriva** — `/spdd-sync` e `/spdd-prompt-update`, com mapa mudança → seção |
| 9 | **Distinção RN × RF** — regra que existe com ou sem sistema × requisito que a cita |
| 10 | **Sistema `[GENÉRICO]`/`[POR PROJETO]`** — mecanismo de reuso entre squads |
| 11 | **Perfis de stack e de ferramenta de gestão** (esteira) — o método viaja |
| 12 | **Roteiro de implantação com métricas, poda e cláusula de parada** |
| 13 | **`Context Integrity Guardrails`** — `Do NOT summarize or truncate`; `Verify all references resolved — report error immediately` |
| 14 | **Exploração *concept-driven* com orçamento de hops** — "não leia o codebase inteiro, isso não escala"; 1 hop, com válvula de escape declarada |
| 15 | **Safeguards escritos à mão** nos canvases reais: `File-touch Discipline`, `Verification Gate`, `Non-goals` |
| 16 | **Autocrítica honesta** — o relatório da simulação documenta os erros da própria IA |

**Contras**

| # | O quê |
|---|---|
| 1 | **Contrato gerativo usado como oráculo** — tautologia estrutural (§4.1) |
| 2 | **Passos 2 e 7 (QA) sem comando e sem técnica** — o mecanismo antitautológico é o menos apoiado |
| 3 | **Critério de suficiência é "todo AC tem CT"** — existência, não suficiência |
| 4 | **Zero verificação mecânica** — sem hook, sem CI, sem schema. Portões são markdown para um LLM |
| 5 | **`/spdd-api-test` só assere status HTTP** |
| 6 | **Sem teste unitário no fluxo core** |
| 7 | **Rastreabilidade canvas → código inexistente**; tabela de rastreio de AC referenciada e nunca gerada |
| 8 | **Sem ciclo de vida de artefato** (confirmado pelo autor, issue #12) |
| 9 | **Zero medição** |
| 10 | **Upstream parado** (~3,5 meses), 1 mantenedor |
| 11 | **REASONS Canvas com idiomas Java/Spring** no formato de saída; tradução manual e não verificável |
| 12 | **Lab em estado "Semana 0"** — `[POR PROJETO]` vazios, sem licença, DoD incompleta |
| 13 | **Esteira em repo separado do produto** (§1.2) |
| 14 | **LGPD/`insumos/` não endereçado** |
| 15 | **Custo de operar não medido** — as 5 métricas cobrem retrabalho e tempo, nenhuma cobre custo |

### 6.2 Coletânea

**Prós**

| # | O quê |
|---|---|
| 1 | **Oráculo externo declarado** — o PRD é alegação; a fonte é o requisito e o app rodando |
| 2 | **Derivação formal do caso de teste** — SFDIPOT, example mapping, EP, BVA 3 valores, tabela de decisão, matriz estado × operação, pairwise, rastreio de efeito |
| 3 | **Gate de falsificabilidade** — mutante previsto sem matador é lacuna declarada, não detalhe |
| 4 | **Critério de suficiência real** — *"toda regra tem seus mutantes previstos mortos"* |
| 5 | **Matriz de rastreabilidade contra omissão silenciosa** (dimensão A) — a lacuna nº 1 do campo |
| 6 | **Roteamento de achado para 5 destinos**, com a regra dura do destino 3: escrever o CT que falha **primeiro** |
| 7 | **Convergência com regra de parada** — teto de 3 ciclos, deduplicação contra o relatório anterior |
| 8 | **Proibição de autorrevisão e de "consertar para ficar verde"** — protege contra a falha que Kent Beck relata |
| 9 | **Alocação pela camada mais barata que prova** — Livewire antes de browser |
| 10 | **13 rodadas medidas, juiz cego, 6 famílias de modelos** — a técnica domina o modelo |
| 11 | **Protocolo repetível publicado** — catálogos, oráculo fixo, prompt do juiz |
| 12 | **Regra da casa**: skill não evolui por releitura, evolui por defeito medido |
| 13 | **Fronteira Caveman explícita** — compressão nunca nos arquivos wiki |
| 14 | **`requirement-to-rule` com 4 gates e teto de 3 candidatos** — evita inflação de contexto |
| 15 | **Escada de enforcement** — preferir `pest --arch`/PHPStan/Rector à prosa |
| 16 | **Honestidade sobre o mutation score** — declara a cegueira à omissão em vez de vender o 100% |

**Contras**

| # | O quê |
|---|---|
| 1 | **Sem montante** — começa depois da elicitação, e trata o card como alta fidelidade |
| 2 | **Sem proveniência** — `RQ` cita trecho, não quem disse e quando |
| 3 | **Portões sem dono** — "confirmar com o usuário" |
| 4 | **`RQ` plano** — sem distinção RN × RF × RNF × premissa × restrição |
| 5 | **Ambiguidade não trava** — na ausência do usuário, assume a premissa mais estreita e segue |
| 6 | **Sem reparo de deriva** — a wiki é retrato do momento |
| 7 | **Experimento mede um elo**, e o número é apresentado como se qualificasse a esteira |
| 8 | **`feature-quality-gate` nunca foi medido** |
| 9 | **Citação-fundamento superestimada** (§3.4) |
| 10 | **Custo de operar nunca medido**; sem ritual de poda, sem critério de morte |
| 11 | **Peso alto** — contradiz a orientação de context engineering da própria Anthropic |
| 12 | **Presa ao Laravel** — técnica agnóstica e comandos específicos no mesmo arquivo |
| 13 | **Sem enforcement mecânico** — apesar de hooks estarem disponíveis hoje |
| 14 | **Zero variância entre modelos** — os mesmos 3 defeitos morrem em nenhuma rodada |
| 15 | **Desenhada para um dev + um agente** — não para squad com 4 papéis |

---

## 7. Proposta de integração

### 7.1 Mapa de encaixe

Antes das opções, o mapeamento peça a peça. É o que torna a decisão concreta.

| Esteira SPDD | Coletânea | Veredito |
|---|---|---|
| `insumos/` + `/spdd-story` | — | **SPDD preenche lacuna.** A coletânea não tem elicitação |
| `historias/[Historia-N].md` | `00-requisito.md` | Mesmo papel de oráculo. **SPDD é mais rico** (origem, tipagem, INVEST, glossário) |
| `pendencias/Q-XX.md`, `contradicoes/CTR-XX.md` | `## Ambiguidades` | **SPDD superior** — objeto com dono e status, que trava |
| **passo 2 — QA escreve CT do template** | **`feature-test-design`** | **★ Encaixe principal.** Coletânea preenche a lacuna |
| `/spdd-analysis` + `A-XX` | step 3 (Pesquisa e Contexto) | Equivalentes. **`A-XX` é melhor** (dúvida técnica formal que trava); o *concept-driven com orçamento de hops* é melhor que a lista de 20 verificações |
| `/spdd-contract` (REASONS, 7 dimensões) | `01-plano-acao.md` + `02-ADR` | Equivalentes com ênfases diferentes: canvas é mais arquitetural (**Safeguards = negative space**), PRD é mais operacional (passos, logs, rollback, impacto) |
| `/spdd-generate` | implementação + Ponytail | Equivalentes. Ponytail acrescenta a escada de simplicidade |
| `/spdd-code-review` (código × contrato) | step 5 + step 6 | Equivalentes — **e ambos tomam o contrato/PRD como verdade** |
| — | **`feature-quality-gate`** (11 dimensões, 5 destinos, requisito × plano × **app rodando**) | **★ Coletânea preenche lacuna.** SPDD não confronta contra o requisito nem contra o app |
| `/spdd-evidence` + passo 7 | step 7 + `06-relatorio-qa.md` | **SPDD é melhor** no registro formal de evidência por CT |
| `/spdd-gate N` com aprovador nomeado | "confirmar com usuário" | **SPDD superior** |
| `acordo-do-squad.md` + `normas-do-projeto.md` | `.ai/rules/` + `requirement-to-rule` | **Complementares** — acordo é método (durável, entre squads); rules são convenção de código (por glob, carregada automaticamente) |
| `/spdd-sync`, `/spdd-prompt-update` | — | **SPDD preenche lacuna.** A coletânea não repara deriva |
| `config/stack-profiles/`, `tool-profiles/` | — (Laravel fixo) | **SPDD superior** para departamento multi-stack |
| `experimentos/` com juiz cego | — | **Coletânea superior.** Método que evolui por medição |

### 7.2 Opção B — duas camadas com contrato de interface **(recomendada)**

```
┌─────────────────────────────────────────────────────────────────────┐
│  CAMADA 1 — PROCESSO DO SQUAD (SPDD)                                │
│  quem decide · quando trava · o que fica registrado                 │
│  insumos → história → portões nomeados → evidência → sync           │
└────────────────────────────┬────────────────────────────────────────┘
                             │  contrato de interface:
                             │  (a) o arquivo de história
                             │  (b) o ID de cláusula
┌────────────────────────────┴────────────────────────────────────────┐
│  CAMADA 2 — MOTOR DE ENGENHARIA (coletânea)                         │
│  como derivar teste · como falsificar · como auditar · como rotear  │
│  feature-test-design · feature-quality-gate · requirement-to-rule   │
└─────────────────────────────────────────────────────────────────────┘
```

Por que essa e não a fusão: **cada camada precisa poder evoluir sozinha.** O processo do squad
muda por decisão do departamento; o motor de engenharia muda por defeito medido em experimento.
São relógios diferentes. Fundir os dois num artefato só amarra a cadência de um à do outro — e a
primeira coisa que se perde é a capacidade de rodar uma rodada de medição sem mexer no acordo do
squad.

### 7.3 As pontes técnicas

Cinco mudanças concretas. Nenhuma é grande; juntas são o que faz a coisa funcionar.

#### Ponte 1 — Namespace de cláusula declarado *(a mais barata e a de maior alavanca)*

Hoje `feature-test-design` e `feature-quality-gate` exigem `RQ-##` e param sem ele. O SPDD tem
IDs tipados **melhores**. A mudança: aceitar um **namespace de cláusula declarado uma vez**.

| Tipo SPDD | Papel na derivação de teste |
|---|---|
| `RF-##` | **cláusula testável** — vira regra no Mapa de Regras |
| `RNF-##` | **cláusula testável** — com a coluna *"Como verificar"* já preenchida pelo QA |
| `RN-##` | **invariante** — testar em **todos** os pontos de entrada, não em um |
| `P-##` (premissa) | contexto do Setup; o par *"Se não for verdade"* vira `@premissa` |
| `R-##` (restrição) | vira Safeguard / dimensão I (segurança) do quality gate |
| `Q-##`, `CTR-##` | **bloqueiam** — pendência aberta impede a derivação, como hoje |

> A distinção **RN × RF é uma melhoria genuína que a coletânea deve adotar**, e não é só
> taxonomia: uma `RN` ("compra acima de R$ 5.000,00 exige duas assinaturas") é uma regra que vale
> em **todo** ponto de entrada — tela, API, importação em lote, comando de console. Uma `RF` é
> **um** comportamento. Hoje o `RQ` plano faz as duas virarem um cenário só, e o defeito clássico
> — regra aplicada na tela e esquecida na API — nasce exatamente aí. O `D09 — Policy só no form`
> do catálogo de cupons é esse defeito.

#### Ponte 2 — A rastreabilidade enraíza no insumo, não na história

A história é **gerada por IA** e aprovada por humano. Usá-la como oráculo reintroduz, em escala
menor, a cegueira que o `00-requisito.md` existe para quebrar.

A solução já está no SPDD e é elegante: **o campo de origem é a âncora.** Cada `RF`/`RNF`/`RN`
cita `Marta · 04:40`. A matriz de rastreabilidade do quality gate ganha uma coluna à esquerda:

```
origem (falante · minuto) → RF-## → passo do contrato → CT → CT-B → código → evidência
```

Com isso, o insumo (`.vtt`) vira o `00-requisito.md` verdadeiro — verbatim, imutável, humano — e
a história vira a decomposição revisável. **É exatamente a arquitetura que a coletânea já tem,
com um nível a mais acima dela.** Ganho: quando um achado do quality gate for roteado ao destino
1 (defeito de especificação), há para onde voltar — a fala original.

#### Ponte 3 — Os portões ganham as duas metades

Hoje o portão do SPDD trava por **pendência aberta**. Ele não pergunta se a cobertura é
suficiente. Proposta — cada portão passa a exigir **(a)** pendência fechada, **(b)** suficiência
provada, **(c)** aprovador nomeado, **(d)** achado roteado:

| Portão | Hoje bloqueia se… | **Acrescentar** |
|---|---|---|
| **1 — História pronta** (PO+QA) | `Q-XX`/`CTR-XX` aberta; RNF sem critério mensurável | Toda `RF`/`RNF` tem ≥1 cenário derivado pela `feature-test-design`, **com mutante previsto declarado**. `RN` tem cenário em cada ponto de entrada |
| **2 — Contrato aprovado** (líder técnico) | `A-XX` aberta; ramo de exceção vago | **Cobertura do requisito**: toda `RF` mapeia a uma dimensão do canvas **ou** está declarada fora de escopo. Cláusula sem passo = destino 1 |
| **3 — Código aceito** (líder técnico) | desvio crítico do `/spdd-code-review` | **`feature-quality-gate`** — dimensões A (omissão), D (log real), I (segurança da superfície nova), K (adequação da suíte). Achados roteados aos 5 destinos |
| **4 — Entrega validada** (QA) | CT sem resultado; falha sem correção | Mutation score na classe crítica como **piso** — com a ressalva escrita no relatório de que ele é **cego à omissão**, e que quem responde por omissão é a matriz |

> **Cuidado deliberado no Portão 4**: colocar mutation score como meta sem a ressalva reintroduz
> exatamente o erro que o `MEMORY.md` desta coletânea registra — duas suítes com qualidade muito
> diferente saturaram em 100%. O piso é de **qualidade de assertion**, nunca de cobertura de
> requisito.

#### Ponte 4 — O `/spdd-sync` não fecha sem re-verificar a história

O reparo mais importante, e o mais barato. Hoje o sync repara contrato ↔ código. Acrescentar um
passo final obrigatório:

```
/spdd-sync  →  seções atualizadas
            →  ❶ quais RF/RNF/RN foram afetadas por esta mudança?
            →  ❷ os CTs dessas cláusulas ainda valem?
               · valem            → registrar e fechar
               · não valem        → destino 3: reescrever o CT que falha PRIMEIRO
               · a cláusula mudou → destino 1: volta ao Portão 1 (PO+QA)
            →  ❸ registrar o ciclo no progresso
```

Isso resolve a tautologia de §2.3 sem abrir mão do reparo de deriva: o contrato continua podendo
descrever o sistema real, mas **não pode fazê-lo em silêncio**. Toda vez que ele se move, a
amarração com a história é reafirmada ou o portão reabre.

#### Ponte 5 — Enforcement mecânico, hoje

Os dois métodos declaram portões e nenhum os torna inevitáveis. Está disponível agora:

| Mecanismo | O que trava |
|---|---|
| **Hook `PreToolUse`** | bloquear `Write`/`Edit` em `app/**`, `src/**` enquanto o Portão 2 não estiver aprovado em `config/project.yml` |
| **Hook `PreToolUse`** | bloquear deleção de arquivo em `tests/**` — a falha que Kent Beck relata |
| **Hook `Stop`** | não encerrar o turno enquanto houver `Q-XX` com `Status: aberta` ligada à história em curso |
| **Check de PR** (via `tool-profiles/`) | falhar quando existir `RF-##` na história sem CT correspondente — **é a lacuna nº 1 do campo, e é um `grep` mais uma tabela** |
| **Check de PR** | falhar quando a contagem de testes **diminuir** no diff |
| **CODEOWNERS** | o aprovador do Portão 3 vira revisor obrigatório do PR — o portão deixa de ser texto |

> O check de PR "`RF` sem CT" é a peça de maior valor simbólico e prático do pacote inteiro.
> Nenhuma ferramenta do levantamento tem isso. É um script de poucas dezenas de linhas.

### 7.4 As outras duas opções, e por que não

**Opção A — absorção pontual (menor risco, menor ganho).** O `spdd-lab` fica como está; troca
apenas os passos 2 e 7 pelas skills. ~2 semanas. Ganho: o passo do QA passa a ter técnica e
critério de suficiência, e a validação passa a ter matriz de rastreabilidade.
*Quando escolher*: se o piloto de 6 semanas já está com data marcada e não se quer mexer no
acordo do squad. **É um bom primeiro movimento e não é excludente com a Opção B** — pode ser a
fase 1 dela.

**Opção C — fusão total.** Um método só, um conjunto de comandos, um vocabulário.
*Por que não*: custo alto, destrói a independência de cadência das duas camadas (§7.2), e obriga
a escolher entre `RQ` e `RF`/`RNF` num momento em que a resposta certa é *"os dois, com
tradução"*. Também amarra a coletânea a um upstream (`open-spdd`) parado há ~3,5 meses.

### 7.5 Dimensionamento — o degrau que falta nos dois

A lacuna nº 4 do campo é *right-sizing*, e nenhum framework tem critério objetivo. Böckeler
mediu um bugfix virando **4 user stories com 16 critérios de aceite** no Kiro; Zaninotto mediu
**8 arquivos e ~1.300 linhas** de spec no Spec Kit para exibir a data atual.

A heurística mais honesta é a da própria Anthropic:

> *"If you could describe the diff in one sentence, skip the plan."*

Os dois métodos já têm a fronteira certa em prosa — o SPDD tem *"correção de defeito sem mudança
de regra de negócio não passa pelo fluxo"*, a coletânea tem o *"Quando NÃO Invocar"*. Falta o
degrau do meio.

Proposta: **estender o perfil de esforço por risco (P×I), que a `feature-test-design` e o
`feature-quality-gate` já usam, para a esteira inteira** — decidido no Portão 1, registrado na
história, e governando quantos artefatos a feature gera:

| Perfil | Quando | Artefatos | Portões |
|---|---|---|---|
| **Mínimo** | correção sem nova regra; ajuste de config; texto | nenhum — só o teste de regressão | nenhum |
| **Padrão** | feature comum, 1–5 dias, sem dado sensível nem dinheiro | história + contrato + CT + evidência | 1, 2, 4 |
| **Completo** | dinheiro, dado pessoal, autorização, máquina de estados, integração externa | tudo, com ADR, CT-B e quality gate completo | 1, 2, 3, 4 |

Isso é o que impede a esteira de virar o que o `spdd-lab` já teme em voz alta: *"Um processo que
ninguém pode podar vira um processo que todos contornam."*

### 7.6 Portão 0 — dado pessoal no insumo *(bloqueante, e sem alternativa)*

Antes de qualquer `/spdd-story`, num contexto Fiocruz/Fundep:

1. **Classificar** o insumo — a reunião tratou de dado pessoal, dado pessoal sensível, ou nenhum?
2. **Pseudonimizar** antes de o arquivo entrar no agente: nomes de terceiros (bolsistas,
   pacientes, servidores) viram papéis (`[coordenadora]`, `[bolsista-1]`). Os **participantes da
   reunião** podem permanecer, porque a proveniência depende deles e eles são parte do processo —
   essa distinção precisa ser explícita.
3. **Declarar retenção** de `requirements/insumos/`: quanto tempo o `.vtt` fica versionado, e
   quem apaga.
4. **Nomear o responsável** pela decisão — é papel do PO ou do líder técnico? Hoje não é de
   ninguém.
5. **Registrar** o destino do dado: qual provedor de IA, sob qual contrato, com qual política de
   retenção do lado dele.

Não é conformidade decorativa. É o item que pode parar o piloto depois de ele ter começado — o
que é o pior momento possível.

### 7.7 Roteiro sugerido

| Fase | Duração | O quê | Sai com |
|---|---|---|---|
| **0** | 1 semana | Portão 0 (LGPD). Licença no `spdd-lab`. `[POR PROJETO]` preenchidos. Aprovadores nomeados. Esteira movida para dentro do repo do produto | squad operável e conforme |
| **1** | 2 semanas | Ponte 1 (namespace de cláusula) + substituição do passo 2 pela `feature-test-design`. **Rodar o protocolo de medição sobre os CTs do QA** — baseline real | número, não impressão |
| **2** | 2 semanas | `feature-quality-gate` no Portão 3. Ponte 2 (origem na matriz). Ponte 4 (sync re-verifica) | omissão silenciosa detectável |
| **3** | 1 semana | Ponte 5 (hooks + check de PR "RF sem CT" + CODEOWNERS) | portão deixa de ser texto |
| **4** | contínuo | Perfil de esforço por risco. Poda. Medição de **custo** | método que se defende sozinho |

**A fase 1 tem um ganho que vale por si**: rodar o protocolo de juiz cego sobre os casos de teste
que o QA escreve hoje dá ao piloto de 6 semanas a **linha de base dura** que o próprio roteiro do
`spdd-lab` admite não ter (*"Hoje não medimos nada disso. Estabelecer a linha de base é parte do
piloto — sem ela, qualquer ganho que eu prometesse aqui seria chute."*).

O protocolo desta coletânea é exatamente o instrumento que falta ali. **Emprestá-lo é a
contribuição mais imediata e menos invasiva que se pode fazer ao lab.**

---

## 8. O que importar em cada direção, sem integrar nada

Se nada da §7 for adiante, estas trocas valem sozinhas.

### 8.1 Da esteira SPDD → para a coletânea

| # | O quê | Onde |
|---|---|---|
| 1 | **Campo de origem** em cada `RQ` (fonte · localizador) | `feature-wiki`, arquivo `00` |
| 2 | **Tipagem de cláusula** — separar `RN` (invariante) de `RF` (comportamento) de `RNF` (com "como verificar") | `feature-wiki` + `feature-test-design` |
| 3 | **Pendência e contradição como arquivos com dono e status**, que travam | `feature-wiki` |
| 4 | **Aprovador nomeado por gate** em vez de "o usuário" | `feature-wiki` + `feature-quality-gate` |
| 5 | **`Context Integrity Guardrails`** — `Do NOT summarize or truncate`; referência não resolvida vira **erro**, não degradação silenciosa | todas as 4 skills |
| 6 | **Exploração *concept-driven* com orçamento de 1 hop** — substitui a lista de ~20 verificações do step 3, que é cara e não escala | `feature-wiki` step 3 |
| 7 | **`Non-goals` com justificativa** e **`File-touch Discipline`** (*"any other file change indicates scope creep"*) | `01-plano-acao.md` |
| 8 | **`Verification Gate`** — comandos executáveis concretos como definição de pronto | `01-plano-acao.md` |
| 9 | **Ritual de poda + cláusula de parada** | `experimentos/README.md` |
| 10 | **Seção "Cenários que o QA acrescentou"** — *"se estiver vazia, o QA leu a história mas não a interrogou"* | `04-casos-de-teste.md`, na revisão adversarial |
| 11 | **Reparo de deriva** — um `/wiki-sync` | skill nova |

### 8.2 Da coletânea → para a esteira SPDD

| # | O quê | Onde |
|---|---|---|
| 1 | **Pipeline de derivação de 7 passos** | passo 2 |
| 2 | **Gate de falsificabilidade** — mutante previsto por cenário | passo 2 + Portão 1 |
| 3 | **Critério de suficiência** — *"toda regra tem seus mutantes mortos"* no lugar de *"todo AC tem CT"* | Portão 1 |
| 4 | **Matriz estado × operação em produto cartesiano fechado** — 5 × 6 = 30 células, cada inválida com CT que afirma recusa **e não-efeito** | passo 2 |
| 5 | **Matriz de rastreabilidade contra omissão silenciosa** | Portão 3 |
| 6 | **Roteamento em 5 destinos**, com o destino 3 escrevendo o CT que falha primeiro | Portões 3 e 4 |
| 7 | **Alocação pela camada mais barata que prova** — evita empurrar para browser o que um teste de componente prova | passo 2 |
| 8 | **Contrato do sub-agente**: proibido alterar código para o teste passar, relaxar assertion, remover teste que não passou | passo 5 |
| 9 | **Regra do par**: *"uma tela aberta não é uma tela que grava"* — toda rota `create`/`edit` precisa de cenário de gravação | passo 2 |
| 10 | **Protocolo experimental com juiz cego** | linha de base do piloto |
| 11 | **Escada de enforcement** — preferir verificação automática à prosa | normas do projeto |
| 12 | **Honestidade sobre mutation score** — piso de assertion, nunca cobertura de requisito | Portão 4 |

---

## 9. Riscos da integração

| Risco | Gravidade | Mitigação |
|---|---|---|
| **Somar dois métodos pesados e produzir cerimônia insuportável** | **Alta** | §7.5 — perfil de esforço por risco decidido no Portão 1. Sem isso, não começar |
| **Medir eficácia e nunca medir custo** — os dois métodos têm esse vício | **Alta** | Instrumentar na fase 1: tokens/história, tempo entre portões, taxa de abandono |
| **Portão vira carimbo** — aprovação sem leitura | **Alta** | O sinal de alerta já está escrito no lab: *"os documentos ficarem prontos rápido demais e todos concordarem com tudo"*. Medir taxa de reprovação por portão; portão que nunca reprova é decorativo |
| **Upstream parado** — customizar templates de projeto sem commit há 3,5 meses | Média | Vendorizar os templates no repo do squad; tratar o OpenSPDD como fonte de inspiração, não dependência |
| **Namespace de cláusula gera confusão `RQ`/`RF`** | Média | Um único mapa de tradução, num só lugar, versionado. Não manter os dois vocabulários vivos |
| **Zero variância entre modelos** — o ponto cego é compartilhado | Média | É o argumento a favor de manter o QA humano escrevendo cenários **em paralelo**, não de substituí-lo. A skill amplia o QA; não o aposenta |
| **LGPD** | **Alta** | §7.6 — Portão 0 bloqueante |
| **Esteira fora do repo do produto** | Média | §1.2 — mover para dentro antes da fase 1 |

---

## 10. Ações imediatas

### Nesta coletânea

- [ ] Corrigir a citação `arXiv 2607.22883` em `README.md` e `feature-test-design/SKILL.md`:
      `~8×` → **~1,4×**, `~3×` → **~1,5×**, *"reverte"* → **"mitiga"**,
      *"318 defeitos"* → **"318 métodos focais cobrindo 233 defeitos"**
- [ ] Qualificar o número do `README.md`: dizer que 83,3%/100% medem **a derivação de caso de
      teste com oráculo fixo**, não a esteira de ponta a ponta
- [ ] Registrar em `experimentos/README.md` os elos **não medidos** (§3.3)
- [ ] Adicionar campo de **origem** ao `00-requisito.md`
- [ ] Adicionar **tipagem de cláusula** (`RN` invariante × `RF` comportamento × `RNF` com "como
      verificar")
- [ ] Adotar os **`Context Integrity Guardrails`** nas 4 skills
- [ ] Substituir a lista de ~20 verificações do step 3 pela exploração **concept-driven com
      orçamento de 1 hop**
- [ ] Abrir issue: **medir o custo de operar** — tokens, tempo, taxa de abandono
- [ ] Abrir issue: **medir o `feature-quality-gate`** — nunca foi

### No `spdd-lab` (para levar ao gerente)

- [ ] **Portão 0 — LGPD/`insumos/`** (§7.6). Bloqueante
- [ ] **Licença** — sem ela, `[GENÉRICO]` não pode ser copiado formalmente
- [ ] Preencher os `[POR PROJETO]`; completar o item 5 da DoD
- [ ] Mover a esteira para **dentro** do repo do produto (§1.2)
- [ ] Customizar `/spdd-code-review`, `/spdd-generate` e `/spdd-sync` para citarem o acordo, as
      normas e os portões — hoje ignoram tudo isso
- [ ] Substituir o passo 2 pela `feature-test-design` (Opção A, 2 semanas)
- [ ] **Rodar o protocolo de juiz cego sobre os CTs atuais do QA** — é a linha de base dura que o
      roteiro admite não ter
- [ ] Acrescentar o passo de re-verificação ao `/spdd-sync` (Ponte 4)
- [ ] `/spdd-gate` como check de PR + CODEOWNERS (Ponte 5)

---

## 11. SDD × SPDD — a comparação que faltava

### 11.1 O `sdd-lab` ainda não existe

O `spdd-lab` cita duas vezes um repositório irmão:

> *"Não confundir com SDD (Spec-Driven Development), em que o artefato mantido é a especificação.
> O repositório irmão `sdd-lab` trata daquele outro método."*

Verificado: **404** em `geckhardtfiocruz/sdd-lab` e em `gsferro/sdd-lab`. Ele foi anunciado, não
construído.

Isso muda a natureza da pergunta. Não se trata de conciliar dois laboratórios existentes — trata-se
de decidir **se o segundo deve ser construído**. E a resposta desta análise é: **não como
laboratório separado.**

### 11.2 A distinção que o lab faz — e o que ela realmente separa

A distinção declarada é sobre **qual artefato é mantido**:

| | Artefato mantido |
|---|---|
| **SDD** | a **especificação** — o que o sistema deve fazer |
| **SPDD** | o **contrato de desenho** — como ele está organizado, até a assinatura do método |

Ela é real, e a consequência mais importante dela não é de processo. É de **falsificabilidade**:

> **Uma especificação é falsificável por um teste. Um contrato de desenho não é.**

Dá para escrever um teste que falha quando a spec é violada: *"WHEN o motivo vier vazio THE SYSTEM
SHALL recusar"* vira um cenário com oráculo. Não dá para escrever um teste que falha quando a seção
`Approach` do canvas é violada — só dá para **revisar**.

É por isso que o `/spdd-code-review` é uma **revisão** (um LLM lendo dois textos), enquanto um gate
baseado em spec pode ser um **teste** (uma máquina executando). E é por isso que o SPDD, apesar de
um ensaio conceitualmente superior, termina sem camada de verificação — ele escolheu manter o
artefato que não se deixa verificar por máquina.

### 11.3 O achado: são três camadas, não dois métodos

Ao alinhar todos os frameworks do levantamento, aparece uma estrutura que nenhum deles nomeia:
**todos têm as mesmas três camadas.** O que muda é qual delas cada um chama de "o artefato".

| Framework | Camada 1 — oráculo comportamental | Camada 2 — contrato de desenho | Camada 3 — spec executável |
|---|---|---|---|
| **Kiro** | `requirements.md` (EARS) | `design.md` | tarefas — teste não é 1ª classe |
| **Spec Kit** | `spec.md` | `plan.md` + `data-model.md` + `contracts/` | `tasks.md` — *Test-First* sem enforcement |
| **OpenSpec** | `specs/` canônicas **+ delta** | `design.md` | `tasks.md` |
| **BMAD** | PRD | Architecture | *story files* |
| **Tessl** | capabilities no `.spec.md` | — (código é artefato gerado) | **`@test`** |
| **SPDD** | **`historias/`** — RF/RNF/RN + AC em Dado/Quando/Então | **REASONS Canvas** | — *(QA manual, sem comando)* |
| **Coletânea** | **`00-requisito.md`** — cláusulas RQ | **`01` + `02`** | **`04`/`05` com mutantes previstos** |

Duas leituras que decidem a questão:

**(1) A história do SPDD *é* uma especificação.** Ela tem requisitos funcionais numerados, regras de
negócio, requisitos não funcionais com critério mensurável e critérios de aceite em Dado/Quando/Então.
Isso é uma spec pelos padrões de qualquer framework SDD do levantamento — melhor que a maioria,
porque tem proveniência.

**(2) O `design.md` do Kiro *é* um contrato de desenho.** Arquitetura, diagramas de sequência,
interfaces, schemas, endpoints. É o REASONS Canvas com outro nome.

> **SPDD e SDD não são dois métodos. São a mesma pilha de três camadas, com a autoridade declarada
> em andares diferentes.**

E há uma confirmação forte disso no estado da arte: **o Kiro já entrega os dois modos.**
*Requirements-First* (Requirements → Design → Tasks) e *Design-First* (Design → Requirements →
Tasks) — literalmente a escolha SDD × SPDD, dentro de uma ferramenta só, com a ressalva de que
**não dá para trocar no meio**: cria-se uma spec nova.

### 11.4 O que muda de verdade: autoridade e ponto de entrada do reparo

Se as camadas são as mesmas, o que resta de diferença é exatamente duas coisas — e são as duas que
importam operacionalmente:

| | Quem vence no conflito | Onde o reparo entra | Sobrevive a uma reescrita? |
|---|---|---|---|
| **SDD** | camada 1 — a spec | spec → desenho → código | **sim** |
| **SPDD** | camada 2 — o contrato | contrato → código (`/spdd-prompt-update`, `/spdd-sync`) | **não** — o contrato *é* o desenho |
| **Coletânea** | camada 1 + **o app rodando** | não tem reparo | `00` sim; `01` não |

A terceira coluna é o critério prático mais útil que saiu deste estudo: **o contrato de desenho morre
junto com a implementação que ele descreve.** Trocar Filament por Inertia, ou Laravel por .NET,
invalida o canvas inteiro e não invalida uma linha da história. Já a spec sobrevive — é ela que
permite dizer *"o novo sistema faz o mesmo que o antigo"*.

### 11.5 O buraco de governança que a comparação revela

Esta é a consequência mais concreta, e ela é interna ao `spdd-lab`.

Regra 7 do `CLAUDE.md`, literal:

> *"Quando a realidade divergir, conserte o contrato primeiro. **Requisito mudou →
> `/spdd-prompt-update`.** Código tomou outro rumo → `/spdd-sync`. Depois o código."*

O `/spdd-prompt-update` atualiza **o canvas**. A tabela de seções afetadas dele lista apenas
seções do canvas (R, E, A, S, O, N, S). **A história não é mencionada em lugar nenhum.**

Mas o princípio I do acordo do squad diz:

> *"**Nada vira código sem história aprovada.** Toda demanda começa em `/spdd-story`."*

E o Portão 1 é aprovado por **PO e QA**; o Portão 2, pelo **líder técnico**.

> **Consequência**: um requisito novo que entra por `/spdd-prompt-update` vira código **sem passar
> pelo Portão 1**. Ele entra na esteira no andar do líder técnico, contornando PO e QA — que são os
> donos declarados do escopo e dos critérios de aceite. O princípio I é violado pela regra 7 do
> mesmo arquivo.

Não é erro de digitação: é a consequência direta de colocar a autoridade na camada 2. **O SDD não
tem esse problema por construção** — mudança de comportamento entra na spec, e a spec é a camada
que o PO e o QA governam.

**Correção sugerida, de uma linha:**

```
Comportamento pedido mudou   → entra na HISTÓRIA → reabre o Portão 1 (PO + QA)
                             → depois /spdd-prompt-update propaga ao contrato
Desenho mudou por decisão    → entra no CONTRATO → reabre o Portão 2 (líder técnico)
técnica, comportamento igual
Código tomou outro rumo      → /spdd-sync, e re-verifica a história (Ponte 4)
```

### 11.6 O que o SDD tem e ninguém mais tem: canônica × delta

Esta é a peça que **nem o SPDD nem a coletânea têm**, e a mais barata de adotar.

Os dois produzem **ilhas**:

- **SPDD** — `spdd/prompt/` acumula documentos que podem se contradizer. O autor do OpenSPDD
  confirma na issue #12 que não há ciclo de vida: nada marca um artefato como superado.
- **Coletânea** — `wikis/specs/{branch}/{feature}/` é por branch. A feature 2 não sabe o que a
  feature 1 estabeleceu. A única coisa que acumula é `.ai/rules/` via `requirement-to-rule`, e isso
  é **convenção de código**, não comportamento do sistema.

O **OpenSpec** (`Fission-AI/OpenSpec`) resolve isso estruturalmente, e é a única solução de *spec
drift* do levantamento que não é slogan:

```
openspec/
├── specs/                    ← CANÔNICA: o estado atual acordado do sistema
└── changes/<id>/
    ├── proposal.md
    └── specs/                ← DELTA: ADDED / MODIFIED / REMOVED / RENAMED
```

No `archive`, a delta é **mesclada** na canônica. A spec canônica sempre reflete o acordado; a spec
da mudança é **efêmera por desenho**. Não há dois documentos disputando a verdade porque só um
persiste.

**O ganho para a coletânea vai além de arrumar a casa.** Com uma spec canônica:

| Problema atual | O que a canônica resolve |
|---|---|
| `## Impacto em Features Existentes` é especulativo — o TIA responde **depois** | *"quais cláusulas canônicas esta delta toca?"* é respondível **antes** de implementar |
| Wiki antiga sem `00` | a canônica é o `00` de tudo que já existe |
| Feature 2 não conhece as decisões da feature 1 | as cláusulas da feature 1 estão na canônica |
| Regressão é heurística (RCRCRC) | o escopo de regressão vira **computável**: as cláusulas vizinhas na canônica |

Custo: um diretório e um passo de merge no Portão 4.

### 11.7 EARS — o mapeamento 1:1 com as técnicas de derivação

**EARS** (*Easy Approach to Requirements Syntax*, Mavin et al., Rolls-Royce, RE'09) é a única
notação de requisito do levantamento com pedigree real. O Kiro usa **um** dos seis padrões; o Spec
Kit não usa nenhum (há *feature request* aberta).

Alinhando os seis padrões com o pipeline da `feature-test-design`, o mapeamento é **direto**:

| Padrão EARS | Forma literal | O que obriga a nomear | Técnica de derivação |
|---|---|---|---|
| **Ubiquitous** | `The <sys> shall <resp>` | invariante sem gatilho | testar em **todo** ponto de entrada — é a `RN` do SPDD |
| **State-driven** | `While <precond>, the <sys> shall <resp>` | o estado como precondição | linha da **matriz estado × operação** |
| **Event-driven** | `When <trigger>, the <sys> shall <resp>` | o gatilho | cenário de caminho principal |
| **Unwanted behaviour** | `If <trigger>, then the <sys> shall <resp>` | **o que não pode acontecer** | cenário de **recusa + não-efeito** |
| **Optional feature** | `Where <feature included>, the <sys> shall <resp>` | a variante / flag | partição, **pairwise** |
| **Complex** | `While <precond>, When <trigger>, the <sys> shall <resp>` | combinação estado × gatilho | linha da **tabela de decisão** |

Vale parar no quarto:

> **`If/Then` — *unwanted behaviour* — é o nome que a EARS dá para o que o ensaio do SPDD chama de
> *negative space* e o que a `feature-test-design` chama de *cenário de recusa e não-efeito*.**
> Três vocabulários, uma ideia. E a EARS é a única das três que lhe dá **sintaxe** — o que a torna
> enumerável em vez de dependente de julgamento.

A consequência prática ataca uma fraqueza medida da própria coletânea. A auditoria das 9 wikis
diagnosticou que *"o gabarito determinava a cobertura"* — o número de casos convergia para o número
de linhas do modelo, **independente da complexidade do requisito**. A EARS inverte isso: **a
gramática do requisito passa a gerar a quantidade de cenários.** Cada `While` é uma linha de matriz;
cada `If/Then` é um cenário de recusa; cada `Where` é uma partição. A derivação deixa de ser
julgamento e vira consulta.

E é diferencial competitivo: **usar os seis padrões coloca a coletânea à frente do próprio Kiro**,
que usa um.

### 11.8 Quadro consolidado

| Dimensão | **SDD** (Kiro / Spec Kit / OpenSpec) | **SPDD** | **Coletânea** |
|---|---|---|---|
| Artefato autoritativo | especificação | contrato de desenho | requisito bruto + **app rodando** |
| Sobrevive a reescrita | **sim** | não | `00` sim |
| Falsificável por máquina | **sim, em princípio** | não | **sim, e com mutante declarado** |
| Notação | **EARS** (Kiro), prosa (Spec Kit) | prosa + Mermaid | Gherkin pt-BR + mutantes |
| Elicitação a montante | ❌ | ✅ **transcrição com proveniência** | ❌ |
| Gate humano | ✅ Kiro bloqueante; ❌ Spec Kit | ✅ **4 portões com aprovador nomeado** | ⚠️ sem dono |
| Enforcement | ✅ hooks (Kiro) | ❌ nenhum | ❌ nenhum |
| Acúmulo entre features | ✅ **OpenSpec: canônica + delta** | ❌ ilhas | ❌ ilhas por branch |
| Reparo de deriva | ✅ delta/merge; sync bidirecional | ✅ `/spdd-sync` | ❌ |
| Critério de suficiência de teste | ❌ | ❌ *"todo AC tem CT"* | ✅ **mutante previsto morto** |
| Detecção de omissão silenciosa | ❌ | ❌ | ✅ **matriz de rastreabilidade** |
| Medição | ❌ nenhuma | ❌ nenhuma | ✅ **13 rodadas, juiz cego** |

### 11.9 Quando cada autoridade é a certa

Não é questão de gosto. É propriedade do **sistema**, não da feature:

| Autoridade na camada 1 (**SDD**) | Autoridade na camada 2 (**SPDD**) |
|---|---|
| O comportamento é estável e a implementação vai mudar | O desenho é o valor, e precisa ser conservado entre iterações |
| Migração, reescrita, troca de stack | Arquitetura nova sendo estabelecida |
| Múltiplos consumidores dependem do contrato externo | Legado sendo domado, onde o desenho é a entrega |
| Domínio regulado — a spec é o compromisso auditável | Time grande onde a deriva de desenho é o risco nº 1 |
| **Exemplo aqui**: sistema Fundep que vai trocar de front | **Exemplo aqui**: módulo novo com padrão a estabelecer |

E o ponto que fecha: **as duas não são exclusivas por sistema.** Manter uma spec canônica *e* um
contrato de desenho é exatamente o que a coletânea já faz — `00` (spec) + `01`/`02` (contrato). O
erro é tratá-las como métodos concorrentes em vez de camadas com ordem de precedência.

---

## 12. O caminho para atender aos dois cenários

### 12.1 Uma esteira, com autoridade declarada — não dois laboratórios

**Recomendação: não construir o `sdd-lab`.**

Três razões, todas verificadas neste estudo:

1. **As camadas são as mesmas** (§11.3). Um `sdd-lab` reescreveria acordo do squad, papéis,
   portões, normas e roteiro de implantação — 80% do `spdd-lab` — para mudar **uma linha**: qual
   camada vence no conflito.
2. **O Kiro já provou que cabe numa ferramenta só**, com *Requirements-First* e *Design-First*
   como modos.
3. **Dois laboratórios dividem a evidência.** Um piloto de 6 semanas com N pequeno já é frágil;
   dois pilotos paralelos produzem duas amostras pela metade e nenhuma conclusão. E o próprio
   roteiro do lab prevê a decisão de **parar** — que exige um número, não dois meios-números.

Em vez disso: **um campo declarado em `config/project.yml`.**

```yaml
autoridade: especificacao   # SDD — a história vence; o contrato é derivado
# autoridade: contrato      # SPDD — o canvas vence; a história é o pedido original
```

O campo governa três coisas, e só essas três:

| O que muda com a autoridade | `especificacao` | `contrato` |
|---|---|---|
| Onde entra a mudança de comportamento | história → **Portão 1** | história → **Portão 1** *(corrige o buraco de §11.5 nos dois modos)* |
| Onde entra a mudança de desenho | contrato → Portão 2 | contrato → Portão 2 |
| O que é mesclado na **canônica** no Portão 4 | as cláusulas da história | as cláusulas da história **e** as normas do canvas |
| O que o `/spdd-code-review` toma como oráculo | **a história** | o contrato, **e depois** a história |

Repare que, na versão corrigida, a diferença entre os dois modos encolheu para quase nada — e isso
é o resultado, não um efeito colateral. **A maior parte do que parece divergência metodológica era
o buraco de governança de §11.5.**

### 12.2 O contrato do oráculo — uma coisa só, declarada onde já existe

Para o motor da coletânea funcionar sob qualquer dos dois (e sob Spec Kit, Kiro ou nenhum), ele
precisa de **uma** coisa: saber ler o oráculo. Isso não pede arquivo novo — pede um bloco de
*front-matter* no arquivo que já existe:

```yaml
---
oraculo: true
prefixos_clausula:  [RF, RNF, RN]     # SPDD · ou [RQ] · ou [FR, NFR]
prefixos_bloqueio:  [Q, CTR, A]       # pendência aberta trava a derivação
campo_origem:       Origem            # a coluna de proveniência, se houver
canonica:           spec/canonica/    # onde a delta é mesclada no fechamento
notacao:            EARS              # EARS | gherkin | prosa
---
```

Com isso, `feature-test-design` e `feature-quality-gate` param de exigir o arquivo chamado
`00-requisito.md` e passam a exigir **um oráculo comportamental declarado, escrito por alguém que
não é quem vai implementar**. É a única coisa que elas de fato precisam — o resto sempre foi
convenção de nome.

### 12.3 A ordem de precedência

Quatro linhas, e resolvem a tautologia (§2.3), o buraco de governança (§11.5) e a deriva (§11.6):

```
1. A CANÔNICA e o APP RODANDO são a verdade sobre o que o sistema faz hoje.
2. A HISTÓRIA (delta) é a verdade sobre o que foi pedido nesta mudança.
3. O CONTRATO é alegação sobre como fazer — revisável, e não é oráculo de teste.
4. Nada é mesclado na canônica sem passar pelos quatro portões.
```

O item 3 é o que o SPDD precisa ouvir, e o item 1 é o que a coletânea precisa construir.

---

## 13. O melhor método para as skills da coletânea

### 13.1 O que a coletânea realmente é

> **A coletânea não é SDD nem SPDD. É o motor de falsificação que os dois precisam e nenhum dos
> dois tem.**

Isso não é posicionamento retórico — **já foi demonstrado experimentalmente, sem intenção.** As 13
rodadas congelaram o `00` e o `01` e mediram só a derivação. Isso é, literalmente, um experimento
que mostra que o motor funciona **independente de como o oráculo foi produzido**. E a convergência
de 6 famílias de modelos mostra que ele funciona independente do modelo.

A skill já é agnóstica. O que não é agnóstico é **o pacote em volta dela**.

### 13.2 A separação: motor × hospedeiro × perfil de stack

Hoje três coisas de naturezas diferentes vivem nos mesmos arquivos:

| Camada | O que é | Muda quando | Onde está hoje |
|---|---|---|---|
| **Motor** | pipeline de derivação, gate de mutantes, 11 dimensões, roteamento, matriz | um defeito atravessa os dois braços de um experimento | espalhado em `feature-test-design` e `feature-quality-gate` |
| **Hospedeiro** | os 9 steps, a estrutura `00`–`06`, o padrão de log, o channel, a ordem de leitura | o time muda de método | `feature-wiki` |
| **Perfil de stack** | Laravel/Filament/Pest, alocação de camada, comandos, armadilhas de API | o projeto muda de stack | dentro das duas skills, misturado |

**A proposta é separar as três** — e o modelo já foi inventado pela esteira, em
`config/stack-profiles/`:

```
motor/
  feature-test-design/SKILL.md      ← agnóstico: técnica, gate, taxonomia, suficiência
  feature-quality-gate/SKILL.md     ← agnóstico: 11 dimensões, 5 destinos, convergência
hospedeiros/
  feature-wiki/SKILL.md             ← o hospedeiro do dev solo (o de hoje)
  spdd/SKILL.md                     ← adaptador: história → oráculo, portões → gates
  spec-kit/SKILL.md                 ← adaptador: spec.md → oráculo
perfis/
  laravel.md   dotnet.md   java.md   generic.md
```

O que cada arquivo responde:

- **motor** — *"como derivar um cenário que mata mutante, e como provar que a cláusula virou teste"*
- **hospedeiro** — *"onde mora o oráculo, quem aprova o quê, onde vai a evidência"*
- **perfil** — *"qual é a camada mais barata que prova, nesta stack, e com qual comando"*

### 13.3 O que fazer com cada skill

| Skill | Veredito | Ação |
|---|---|---|
| **`feature-test-design`** | **É o produto.** É a peça que ninguém no estado da arte tem | Extrair o Laravel para perfil. Trocar `RQ-##` por namespace declarado. Adotar EARS como notação de entrada preferida |
| **`feature-quality-gate`** | **É o segundo produto**, e é o que fecha a lacuna nº 1 do campo | Idem. Acrescentar a dimensão de **regressão computável** contra a canônica |
| **`feature-wiki`** | **É um hospedeiro, não o método.** Excelente para dev solo; não viaja para squad | Manter, e renomear mentalmente: deixa de ser "a esteira" e passa a ser "o hospedeiro mais simples". Ganha aprovador nomeado e campo de origem |
| **`requirement-to-rule`** | **Ortogonal** — funciona sob qualquer hospedeiro | Manter. Acrescentar a canônica como destino possível, ao lado de `.ai/rules/` |

Um efeito colateral honesto: **o nome `laravel-ai-skills` vira restrição** no momento em que o
motor deixar de ser Laravel. Não é urgente, mas é uma decisão que vai chegar.

### 13.4 Por que essa é a jogada certa

**(1) Competir na superfície de framework é perder.** O Spec Kit tem ~72 mil estrelas e o
patrocínio do GitHub; o Kiro é um IDE da AWS. Reescrever `/specify` e `/plan` em português com
sabor Laravel não ganha de nenhum dos dois. **Já ser dono da camada que os dois não têm, ganha.**

**(2) Um motor tem cinco hospedeiros, um método tem um.** Spec Kit, Kiro, BMAD, OpenSpec e SPDD têm
exatamente o mesmo buraco — nenhum prova que a cláusula virou teste, nenhum impõe que o teste derive
da spec e não da implementação. Um motor que pluga em todos serve cinco públicos.

**(3) A medição é o fosso.** Não há um único estudo revisado por pares ou metodologicamente
transparente sobre Spec Kit, Kiro ou BMAD até setembro de 2026. Os números que circulam são
marketing. **O `experimentos/` desta coletânea é o único ativo do gênero na categoria** — e é
reprodutível por terceiros, o que é a única forma de ele valer alguma coisa. Isso é mais defensável
que qualquer feature.

**(4) A orientação da própria Anthropic aponta para lá.** A documentação do Claude Code recomenda,
como o degrau mais alto da escada de verificação, *"a fresh model try to refute the result, so the
agent doing the work isn't the one grading it"*, e o padrão *"have one Claude write tests, then
another write code to pass them"*. **A coletânea é a versão produtizada disso**, com técnica formal
e critério de suficiência por trás. É a direção que o fornecedor do modelo está apontando.

### 13.5 O que fazer primeiro

Se for para escolher uma ordem, é esta — cada passo é útil sozinho, e nenhum depende do seguinte:

1. **Namespace de cláusula declarado** (Ponte 1 + §12.2). Destrava tudo, custa pouco, e é o que
   torna o motor plugável no `spdd-lab` **sem** mexer no acordo do squad.
2. **Rodar o protocolo sobre os casos de teste atuais do QA.** Dá ao piloto a linha de base que ele
   admite não ter, e valida a tese de encaixe com número em vez de argumento.
3. **Corrigir o buraco de governança de §11.5** no `spdd-lab` — mudança de comportamento reabre o
   Portão 1. Uma linha, e resolve a maior parte da divergência SDD × SPDD.
4. **Spec canônica + delta** (§11.6). É o que transforma a regressão de heurística em cálculo, e o
   que impede as ilhas de se contradizerem.
5. **Extrair o perfil de stack.** Só então o motor viaja — e só então faz sentido oferecê-lo a
   outro squad do departamento.

---

## 14. Fecho

O `spdd-lab` acerta uma frase que a coletânea devia ter escrito primeiro:

> *"A skill lê e preenche. As pessoas revisam e decidem."*

E a coletânea acerta um princípio que o SPDD precisa e não tem:

> *"O PRD é alegação, não verdade. Validar contra a interpretação confirma a interpretação."*

As duas frases dizem a mesma coisa em registros diferentes: **o artefato produzido pela máquina
não pode ser a autoridade que julga a máquina.** O SPDD resolve isso colocando uma pessoa no
portão. A coletânea resolve colocando o requisito bruto e o app rodando como oráculo. **As duas
soluções são certas e nenhuma das duas é suficiente sozinha** — a pessoa no portão não tem
técnica para saber se a cobertura é suficiente; o oráculo automático não tem autoridade para
decidir escopo.

Juntas, elas fecham a lacuna que o estado da arte inteiro admite não ter fechado: **provar que
todo requisito virou teste, e travar quando não virou.**

Isso não é integração incremental. É a coisa mais adiantada que existe nesse eixo — e está a um
`grep`, uma tabela e um check de PR de distância.

---

## Fontes

**Repositórios** · [gszhangwei/open-spdd](https://github.com/gszhangwei/open-spdd) ·
[design-philosophy.md](https://github.com/gszhangwei/open-spdd/blob/main/docs/design-philosophy.md) ·
`geckhardtfiocruz/spdd-lab` (privado) · `esteiraspdd.html` (local)

**Método SPDD** ·
[Structured-Prompt-Driven Development — martinfowler.com](https://martinfowler.com/articles/structured-prompt-driven/)
(Wei Zhang & Jessie Jie Xia, Thoughtworks, 28/04/2026)

**Estado da arte** ·
[Böckeler — SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) ·
[github/spec-kit](https://github.com/github/spec-kit) ·
[Kiro specs](https://kiro.dev/docs/specs/) ·
[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ·
[Tessl](https://tessl.io/blog/tessl-launches-spec-driven-framework-and-registry) ·
[Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) ·
[agents.md](https://agents.md/) ·
[EARS — Mavin](https://alistairmavin.com/ears/)

**Orientação oficial** ·
[Claude Code best practices](https://code.claude.com/docs/en/best-practices) ·
[Anthropic — effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Evidência** ·
[arXiv 2607.22883 — Misguidance Effect of Buggy Code](https://arxiv.org/abs/2607.22883) ·
[arXiv 2607.05139 — On the risk of coding before testing](https://arxiv.org/abs/2607.05139) ·
[arXiv 2410.21136 — actual vs expected behaviour oracles](https://arxiv.org/abs/2410.21136) ·
[METR RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) ·
[SWE-Bench Illusion](https://arxiv.org/abs/2506.12286) ·
[GitClear — Maintainability Gap](https://www.gitclear.com/the_ai_code_quality_maintainability_gap) ·
[DORA 2025](https://dora.dev/dora-report-2025/)

**Crítica** ·
[Zaninotto — SDD: The Waterfall Strikes Back](https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html) ·
[Gonzalez — A sufficiently detailed spec is code](https://haskellforall.com/2026/03/a-sufficiently-detailed-spec-is-code) ·
[Kent Beck — TDD, AI agents and coding](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) ·
[Willison — Vibe engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
