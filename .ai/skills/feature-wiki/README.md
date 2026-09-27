# feature-wiki — Documentação Antes de Implementar

> **Skill**: [`SKILL.md`](SKILL.md) · versão **3.6.0** · referências sob demanda em [`references/`](references/)
> Este README fala com a **pessoa**: por que a skill existe, quando usar, dependências e limites. O
> procedimento que o agente segue está no `SKILL.md` e nas `references/`, e não é repetido aqui.

## Índice

- [Por que a skill existe](#por-que-a-skill-existe)
- [Os arquivos que ela cria](#os-arquivos-que-ela-cria)
- [Quando usar — e quando não](#quando-usar--e-quando-não)
- [Dependências](#dependências)
- [Instalação](#instalação)
- [Como a skill está organizada](#como-a-skill-está-organizada)
- [Limites](#limites)
- [Por que ela funciona assim](#por-que-ela-funciona-assim)

---

## Por que a skill existe

Força o agente a **documentar antes de codar**. Em vez de sair implementando a partir de um card, ele produz uma wiki versionada da feature: o requisito bruto, um plano de ação minucioso o suficiente para outro agente executar sem ambiguidade, as decisões arquiteturais com alternativas descartadas, os casos de teste **antes** do código, e o tracking do progresso.

**O ganho central** não é documentação bonita — é que **escrever o caso de teste antes de implementar força a pesquisa das APIs envolvidas na fase de planejamento, não na fase de debug**. Nome de método errado, FK obrigatória em fixture, restrição de schema de biblioteca externa: tudo isso aparece ao escrever o CT, quando custa uma linha de correção, em vez de aparecer no meio da implementação.

### O que ela entrega

| Vantagem | Como |
|---|---|
| Plano executável por outro agente | passos numerados com path exato, assinatura, lógica e logs especificados |
| Premissa validada antes de codar | step 3 obriga `search-docs`, leitura de vendor source, `Grep` no código real |
| Plano auditado contra over-engineering | step 6 invoca `/ponytail:ponytail-review` **automaticamente** |
| Teste como especificação, não como sobra | `04` e `05` escritos antes da implementação |
| Log padronizado e rastreável | formato `[Classe@Método]` + channel por feature + context estruturado |
| Decisão que não se perde | ADR com contexto, alternativas e consequências |
| Retomada sem reler tudo | `03-progresso.md` com evidência inline em cada item fechado |
| Validação por quem não implementou | CT-B escritos em loop por sub-agente, e QA pela [`feature-quality-gate`](../feature-quality-gate/README.md) |
| **Defeito de correção pego antes do PR** | step 6.5 roda `/code-review high` **no diff** mais um passe de eixos, logo após os testes passarem e **antes** da reconciliação — o único gate que lê o diff, e o mais produtivo de todos numa feature medida |
| **Juiz que não é o autor** | no Claude Code, revisão do diff, revisão adversarial e quality gate rodam em **sub-agentes cegos** (`opus`, sem Edit/Write); o resto vai para `haiku`/`sonnet` conforme a complexidade, com quadro de despacho no `03` |
| **Superfície do cliente inventariada** | `## Superfície Livewire` no `02`: método público (ação por `$wire.`), propriedade pública sem `#[Locked]` e estado do framework usado sem validar |
| **Lista paralela não esquecida** | varredura da classe irmã no step 5: `grep` pelo FQCN de uma irmã acha `config/`, seeders e inventários que nenhuma rule enumera |
| **Premissa de custo falsificável** | `## Modelo de Execução` no PRD — quantos requests a tela custa, o que é adiado e o que é cacheado |
| **Wiki que não mente depois do código** | step 7 reconcilia wiki, docs de usuário, CHANGELOG e rules com o código: checkbox só fecha com evidência, desvio corrige o `01`/`02` de origem, citação `arquivo:símbolo:linha` conferida por grep, IDs de CT sincronizados nos dois sentidos |
| **Pedido que cresce no meio da implementação** | vira Adendo numerado no `00`, com a `feature-test-design` reinvocada só para ele — o teste do pedido novo não nasce do código |

### O gate que mais pega defeito

Numa feature medida em 2026-09-17, com todos os outros gates cumpridos, a revisão de código do
diff (step 6.5) achou os defeitos de correção que nenhum gate anterior tinha como ver — dois deles
produzindo 500 em produção. A tabela gate × achados está em
[`references/casos-medidos.md`](references/casos-medidos.md#topo--o-65-é-o-gate-mais-produtivo-2026-09-17).
Foi essa medição que levou o gate para o topo do `SKILL.md` (3.3.0), para **antes** da
reconciliação (3.4.0) e para as mãos de um sub-agente cego ao plano.

## Os arquivos que ela cria

```text
wikis/specs/{branch}/{feature}/
├── 00-requisito.md               ← requisito bruto IMUTÁVEL + cláusulas RQ-##
├── 01-plano-acao.md              ← PRD: passos, rotas, autorização, logs, riscos
├── 02-decisoes-arquiteturais.md  ← ADRs
├── 03-progresso.md               ← checklist + blockers + desvios + retrospectiva
├── 04-casos-de-teste.md          ← delegado à feature-test-design
├── 05-casos-de-teste-browser.md  ← delegado (condicional: só o que exige navegador)
├── 05-*.md                       ← extras: api-contract, rollback, security, performance
└── 06-relatorio-qa.md            ← saída do feature-quality-gate
```

Os **cinco primeiros são obrigatórios** (o `05` de browser é condicional a um gate). Os `05-*` extras e o `06` são criados conforme necessidade.

> **A partir da v3.0.0 o `04` e o `05` não são escritos por esta skill.** Ela invoca a
> [`feature-test-design`](../feature-test-design/README.md) no step 4, passando o
> `00-requisito.md` como oráculo. O motivo é medido (arXiv 2607.22883: 318 métodos focais cobrindo
> 233 defeitos, 11 modelos): derivar teste do código/plano em vez da especificação multiplica por
> ~1,4 os testes que codificam o bug como comportamento esperado e corta por ~1,5 os que detectam
> o defeito — a especificação mitiga o efeito, não o reverte. Testar o plano confirma o plano.

## Quando usar — e quando não

**Sempre** que começar uma feature nova, um card, um ticket — antes de qualquer `php artisan make:*`.

**Não** invocar para: correção de texto, ajuste de config trivial, refactoring sem mudança de comportamento, bump de dependência, seeder isolado. O critério: se a mudança não adiciona lógica de negócio, não altera fluxo de dados e não cria arquivo de código, não precisa de wiki. Bug fix **com nova regra de negócio** precisa.

## Dependências

As três primeiras linhas são as que o `SKILL.md` declara em `metadata.requires`, e a versão é o
mínimo **quando a dependência está presente**. Nenhuma é obrigatória além de um projeto Laravel com
git: sem cada uma, a skill degrada e declara no `03-progresso.md` o que não pôde fazer. A exceção é
a `feature-quality-gate` — sem ela o PR não abre.

| Dependência | Versão mínima | O que habilita | Sem ela |
|---|---|---|---|
| [`feature-test-design`](../feature-test-design/README.md) | 1.15.0 | step 4: derivação do `04`/`05` a partir do requisito, com técnica formal e gate de mutantes. A 1.15.0 é a que traz `feature-test-design/references/pest-plugin-browser.md`, a fonte única dos fatos do plugin que esta skill consulta | o `04` volta a ser gabarito preenchido a partir do PRD — a degradação mais cara da lista, declarada no `03`. Abaixo da 1.15.0 falta o `pest-plugin-browser.md`: o `fw-executor-ctb` para sem escrever CT-B, e no step 3 restam só os dois fatos que o `SKILL.md` guarda (servidor próprio, `npm run build`) |
| [`feature-quality-gate`](../feature-quality-gate/README.md) | 1.5.0 | step 8: QA confrontando requisito × plano × app, com a checagem L6 (alegações da Verificação Final do `03`) | o PR não abre: o `06-relatorio-qa.md` é blocker |
| `laravel/boost` (MCP) | 2.4.12 | `search-docs`, `database-schema`, `database-query`, `browser-logs` e `record-rule` — a tool que o step 9 usa nasceu na 2.4.12 | a pesquisa cai para doc oficial e `Grep`; o step 9 não grava rule |
| [`requirement-to-rule`](../requirement-to-rule/README.md) | 1.1.0 | step 9: grava a rule aprovada e regenera o índice. A 1.1.0 é a que traz o `search-docs` como teste do gate 4, que o step 9 manda usar. Fica fora de `metadata.requires` porque o step 9 só a invoca depois do "sim" do usuário | o step 9 para na apresentação; a decisão continua na ADR |
| `pestphp/pest` | 4 (5 recomendado) | no 5: `--parallel --tia`, `--agent`, `--mutate`, sharding, matchers novos | no 4: `pest --filter` |
| `pest-plugin-browser` + Playwright | — | CT-B executáveis | o `05` fica como roteiro manual |
| PCOV ou Xdebug | — | `--tia` e `--mutate` | suíte completa, sem mutação |
| Playwright MCP | — | observar a página no loop de correção do CT-B | `screenshot()`, `content()` filtrado, leitura do Blade |
| Ponytail (plugin) | — | escada de simplicidade na execução e auditoria do plano no step 6 | step 6 vira passe manual, registrado no `03` |
| Caveman (plugin) | — | prosa terse na conversa (nunca nos arquivos wiki) | — |
| Claude Code com sub-agentes | — | roteamento por modelo e juiz independente no 6.5, na revisão adversarial e no step 8 | tudo roda em linha, na sessão que implementou; a degradação vai no `03` e no cabeçalho do `06` |

## Instalação

O `boost:add-skill` copia o diretório **inteiro** da skill — `SKILL.md`, `README.md`,
`references/` e `agents/` — para `.ai/skills/feature-wiki/`, e o `boost:update` o espelha em
`.claude/skills/`. As `references/` precisam estar lá: o `SKILL.md` manda o agente abri-las antes de
cada ação que depende delas.

### Os agentes

As cinco rotas que carregam **cegueira e restrição de ferramenta** vêm prontas, cada uma na
pasta `agents/` da skill que define o contrato dela — assim o `boost:add-skill` instala o agente
junto com a skill, inclusive na instalação seletiva:

| Agente | Skill dona | Papel |
|---|---|---|
| `fw-revisor-diff` | `feature-wiki` | passe de eixos do step 6.5 |
| `fw-executor-ct` | `feature-wiki` | testes Pest de backend a partir do Gherkin do `04`, sob contrato a/b/c (3.5.0) |
| `fw-executor-ctb` | `feature-wiki` | loop dos CT-B no step 7 |
| `fw-adversario-ct` | `feature-test-design` | revisão adversarial do `04` |
| `fw-qa-gate` | `feature-quality-gate` | step 8 inteiro, sem Edit/Write |

**O Claude Code não lê `.ai/skills/*/agents/`.** Depois de instalar ou atualizar as skills pelo
Boost, copie os agentes para onde ele procura — uma vez, e de novo a cada `boost:add-skill`:

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

Sem essa cópia a skill cai no `general-purpose` com `model` explícito — funciona, mas perde a
restrição de ferramenta. O que o agente confere antes do primeiro despacho está no `SKILL.md`.

## Como a skill está organizada

| Onde | O que tem | Quando o agente lê |
|---|---|---|
| `SKILL.md` | gates, obrigações, a sequência de steps 0–9 e o checklist final | sempre, ao ativar a skill |
| `references/` | templates dos arquivos `00`–`03`, padrão de log, tabelas de roteamento, greps e `search-docs` do step 3, contratos dos executores de teste, Playwright MCP, Pest 5, citações de código, candidatos a rule, Ponytail/Caveman, arquivos extras, casos medidos | só quando um step manda — "antes de X, leia" o arquivo de `references/` daquele tema |
| `agents/` | `fw-revisor-diff`, `fw-executor-ct`, `fw-executor-ctb` | pelo Claude Code, depois de copiados para `.claude/agents/` |

A lista das `references/`, com o step em que cada uma é lida, está no índice do `SKILL.md`.

## Limites

- **Não é para mudança trivial.** Typo, config, refactor sem mudança de comportamento, bump de
  dependência e seeder isolado ficam fora — o critério está em [Quando usar](#quando-usar--e-quando-não)
- **O corpo do `SKILL.md` ainda passa das 500 linhas** que a especificação Agent Skills recomenda.
  Na 3.6.0 saíram para `references/` os templates, as tabelas, os comandos, os fatos de ferramenta e
  os casos; os gates e as obrigações ficaram no corpo de propósito, porque regra escrita num arquivo
  que precisa ser aberto tem mais chance de ser ignorada
- **Uma reference só vale se o agente a abrir.** Cada step diz qual abrir antes da ação, e o
  checklist final exige declarar as referências lidas. Se isso basta ainda não foi medido — a
  comparação 3.5.2 × 3.6.0 é uma rodada do protocolo de [`experimentos/`](https://github.com/gsferro/laravel-ai-skills/blob/main/experimentos/README.md)
- **Fora do Claude Code** (Windsurf, Cursor, Copilot) não há sub-agente: tudo roda em linha, o juiz
  volta a ser o autor, e a skill declara isso no `03` e no cabeçalho do `06`
- **A cegueira dos agentes é por instrução, não por construção.** O `fw-revisor-diff` tem `Read` e
  `Glob` sem restrição de path e `Bash` liberado: *"não abra o `01`/`03`"* e *"não edite"* dependem
  de o agente obedecer. O fallback `general-purpose` perde também a restrição de ferramenta
- **`search-docs` cobre Pest até 4.x.** Em projeto com Pest 5 a consulta pode devolver a versão
  anterior; a skill manda confirmar na doc oficial
- **Rule gravada não tem remoção por ferramenta.** O Boost tem `record-rule` (desde a 2.4.12), mas
  nenhuma tool nem comando para remover rule
- **Números medidos têm uma fonte cada.** Os casos que originaram as regras estão em
  [`references/casos-medidos.md`](references/casos-medidos.md); as rodadas do protocolo experimental,
  na tabela única de [`experimentos/README.md`](https://github.com/gsferro/laravel-ai-skills/blob/main/experimentos/README.md)

## Por que ela funciona assim

### Por que despachar sub-agentes no Claude Code

Dois motivos, e o segundo é o que importa para esta coletânea:

1. **Custo.** Grep em lote, tabela pronta, espelho do `01` no `03`, conferência de citação — nada
   disso precisa do modelo mais caro. O princípio é o do PO que motivou a mudança: *gerar barato,
   raciocinar sob demanda, auditar caro.*
2. **Independência.** A coletânea inteira existe para quebrar a **cegueira correlacionada**: o
   mesmo agente lê o requisito, escreve o plano, o teste, o código e o veredito, e erra
   coerentemente. Três gates já pediam *"por quem não implementou / não derivou / não escreveu"*
   — e rodavam **na mesma sessão**. Um sub-agente nasce sem o contexto da sessão: a cegueira vem
   de graça. Por isso a skill roteia por **dois eixos**: complexidade escolhe o modelo; cegueira
   escolhe o contexto e proíbe rodar em linha.

Todo disparo aparece num **quadro** antes de rodar e é reportado contra o mesmo quadro depois; o
quadro vai para a seção `## Despachos` do `03-progresso.md`. É também o primeiro registro da
coletânea de **qual modelo fez o quê** — o custo de operar, que nunca tinha sido medido.

O procedimento (rotas, quadro, mapa por step, auditoria do retorno) está no `SKILL.md`, seção
*Execução e Delegação*, e as tabelas em [`references/roteamento-e-despacho.md`](references/roteamento-e-despacho.md).
A validação em campo (2026-09-21, feature completa) está em
[`references/casos-medidos.md`](references/casos-medidos.md#validado-em-campo--2026-09-21-feature-completa-no-demo-wiki).

### Por que o requisito entra verbatim — e como passá-lo

O mesmo agente lê o requisito, escreve o PRD, escreve os testes, implementa e roda os testes. Se ele **entendeu o requisito errado**, erra coerentemente cinco vezes e tudo fica verde. O PRD não serve como linha de base porque **ele é a interpretação** — validar contra o PRD confirma o erro em vez de expô-lo.

O `00-requisito.md` é a única linha de base independente do agente. É também o oráculo do [`feature-quality-gate`](../feature-quality-gate/README.md): sem ele, a etapa de QA não tem contra o que confrontar.

**Como passar o requisito:**

| Forma | O que você faz |
|---|---|
| **Colar o texto no chat** (card do Jira/Azure/GitHub, e-mail, mensagem) | cole o texto do card **como está** — sem editar antes |
| **Arquivo no projeto** (`.md`, `.pdf`, `.docx`) | aponte o caminho e as páginas: *"o requisito está em `docs/requisitos/RF-231.pdf`, páginas 3 e 4"* |
| **Descrever na conversa** | funciona, mas vale como fonte de baixa fidelidade: espere um pedido de confirmação |
| **Não informar** | a skill não começa sem ele — sem requisito não há linha de base |

Exemplo de invocação:

```text
/feature-wiki

Card FERRO-579:
"Precisamos gerar os relatórios de MBA em lote, por turma. Apenas o coordenador
da turma pode disparar. Avisar o coordenador quando terminar. Precisa ser rápido."
```

**O que volta para você.** O texto fica guardado como chegou, e cada exigência vira uma cláusula
`RQ-##` com o trecho de origem. Para o card acima:

| ID | Cláusula | Trecho literal | Tipo |
|----|----------|----------------|------|
| RQ-01 | gerar relatório por turma em lote | "em lote, por turma" | funcional |
| RQ-02 | só coordenador da turma dispara | "Apenas o coordenador da turma pode disparar" | autorização |
| RQ-03 | notificar coordenador ao concluir | "Avisar o coordenador quando terminar" | funcional |
| RQ-04 | ⚠️ "rápido" sem número | "Precisa ser rápido" | não-funcional |

A RQ-04 já entrega valor **antes de qualquer código**: *"rápido" não é testável; qual o SLA?* Vira
pergunta para você em vez de suposição silenciosa do agente. Daí em diante cada passo do plano e
cada caso de teste aponta a cláusula que atende — é por essa amarração que o quality gate acha
cláusula sem plano, sem teste ou sem código.

O procedimento está no `SKILL.md`, seção *Captura do Requisito*, e o formato do arquivo em
[`references/template-00-requisito.md`](references/template-00-requisito.md).

> **Wiki antiga sem `00`** (anterior à v2.10.0): ao retomá-la, espere que o agente peça o
> requisito original a você. Ele não o reconstrói a partir do PRD.

### Por que existe um arquivo só para teste de browser

Até a v2.5.0 o `04-casos-de-teste.md` era 100% backend: `RefreshDatabase`, `Queue::fake()`, `Http::fake()`, `Log::spy()`, factories. Uma feature Filament/Livewire saía da wiki com CTs provando que o Job despachou e o log saiu — e **nada** provando que o botão renderiza, que o `wire:model` persiste ou que o modal fecha. O arquivo `05` fecha essa lacuna.

Ele tem **duplo uso**:

1. **Especificação de teste** — CT-B executáveis via `pest-plugin-browser`
2. **Roteiro de auditoria** — tabela *Desenhado × Implementado*, preenchida na pós-implementação, que confere linha por linha o que o PRD prometeu contra a tela que existe de fato

A fronteira antiga — *"backend no `04`, tela no `05`"* — tinha um efeito colateral caro: como o
`05` tem teto de 1 happy path + 1 erro, **a superfície de UI ficava praticamente sem cobertura**.
O teto do browser virou o teto de toda a tela.

A fronteira correta não é *backend × tela*, é **o que só o navegador prova × todo o resto**:

| O cenário afirma sobre… | Arquivo | Camada |
|---|---|---|
| regra de negócio, persistência, autorização, efeito colateral | `04` | `Unit` / `Feature` |
| formulário Filament, gravação, tabela, filtro, ação, notificação, autorização na tela | `04` | **componente Livewire** |
| JavaScript executado, console/erro de JS, acessibilidade, cor/tema, layout | `05` | `Browser` |

Em Laravel + Filament, a maior parte do que parece exigir navegador é **teste de componente
Livewire** — milissegundos, sem Node e sem Playwright.

O gate que decide se o `05` existe e o gate de tela de escrita estão no `SKILL.md`, seção
*Gate do `05`*. Feature sem tela — job, webhook, command, import de CSV — não gera CT-B, e isso é
deliberado, para o `05` não virar burocracia morta.

**O que o projeto precisa ter para os CT-B** — a skill não assume que está instalado; se faltar,
ela inclui a instalação como passo numerado no `## Dependências` do PRD:

```bash
# 1. Plugin de browser do Pest
composer require pestphp/pest-plugin-browser --dev

# 2. Playwright + browsers
npm install playwright@latest
npx playwright install
```

E adicione ao `.gitignore`:

```gitignore
tests/Browser/Screenshots
```

Para rodar os CT-B em outro navegador: `vendor/bin/pest --browser firefox`.

**Opcional, mas recomendado (Pest 5):**

```bash
# Verificação pontual de mudança pelo próprio agente de IA
composer require pestphp/pest-plugin-agent --dev

# Driver de cobertura — pré-requisito do --tia
pecl install pcov     # ou Xdebug
```

**CI (GitHub Actions)** — os CT-B exigem Node e browsers no runner:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: lts/*
- run: npm ci
- name: Install Playwright Browsers
  run: npx playwright install --with-deps
```

Os fatos do plugin (servidor próprio, `actingAs()`, esperas, `npm run build`, `--parallel`) têm uma
fonte única, na `feature-test-design`:
[`feature-test-design/references/pest-plugin-browser.md`](../feature-test-design/references/pest-plugin-browser.md).
A instalação do Pest 5 e o uso de `--tia`, `--agent` e `--mutate` estão em
[`references/pest-5.md`](references/pest-5.md). O TIA é o que torna viável rodar a suíte a cada
passo do PRD: o suite de 19.000+ testes do Laravel Cloud caiu de ~3 minutos para ~5 segundos.

Os CT-B são o único ponto da wiki onde o teste **é** o instrumento de auditoria — ele executa o que o PRD desenhou contra a UI que existe de fato. Por isso a skill delega a escrita deles a um **sub-agente em loop**, em vez de escrever inline:

1. **Ruído**: falha de browser despeja HTML, snapshot, stack do Playwright e path de screenshot. O sub-agente absorve isso e devolve só o veredito — o contexto principal fica limpo (e o Caveman `ultra` continua fazendo sentido).
2. **Iteração**: acertar seletor e timing de UI é tentativa e erro. Loop isolado, no máximo 3 iterações.
3. **Independência**: quem escreve o CT-B a partir do `05` não deve ser quem escreveu a implementação — reduz o viés de "testar o que eu fiz" em vez de "testar o que foi especificado".

O contrato do sub-agente está em [`references/delegacao-casos-de-teste.md`](references/delegacao-casos-de-teste.md).

**Por que o Playwright MCP entra, e só como observador.** O `pest-plugin-browser` roda e atesta o
CT-B; as ferramentas de debug dele exigem um humano na frente.
Para **rodar e atestar**, o plugin basta e é o único caminho. Para o agente **investigar sozinho** por que o seletor não casou, as opções nativas são um PNG ou um dump de HTML. É aí que o MCP ganha: `browser_snapshot` devolve a árvore de acessibilidade (~200–400 tokens de texto estruturado, contra ~3.000–5.000 de um screenshot) e `browser_generate_locator` converte o elemento observado em locator estável.

Três lacunas concretas: **descobrir o locator verdadeiro** numa falha de seletor; **observar
quando o elemento realmente aparece** em UI assíncrona (sem observar, o agente não sabe qual estado
final esperar); e **extrair seletores de tela existente** antes de escrever o CT-B. Configuração,
regras e fallback: [`references/playwright-mcp.md`](references/playwright-mcp.md).

### Por que `search-docs` é a primeira fonte

O Boost expõe a tool MCP **`search-docs`**, que consulta a Documentation API hospedada da Laravel, filtrada pelos pacotes instalados no projeto. A skill trata isso como fonte primária, antes de vendor source e antes de doc na web.

Isso é importante justamente porque a skill agora **recomenda** Pest 5: consultar `search-docs` sobre `--tia` devolveria informação de Pest 4. A skill declara essa lacuna em vez de deixar o agente confiar numa resposta desatualizada.

Cobertura por versão, lacunas e como consultar: [`references/pesquisa-step-3.md`](references/pesquisa-step-3.md#documentation-api-do-boost-search-docs).
