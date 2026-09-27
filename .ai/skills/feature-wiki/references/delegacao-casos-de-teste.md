> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de invocar a `feature-test-design`), implementação (antes de despachar o `executor-ct` ou de escrever o teste em linha) e step 7 (antes de despachar o `executor-ctb` ou de escrever o CT-B em linha). Fonte única de: justificativa e contrato da delegação do `04`/`05`, contrato do construtor de testes e ciclo dos CT-B.

# Delegação dos casos de teste

O gate do `05`, a regra de que o `01` não é fonte de comportamento esperado, a ordem com o step 6
e o que fazer com vermelho — no backend e nos CT-B — ficam no corpo do `SKILL.md`, seção
*Arquivos 04 e 05*. Os contratos completos dos executores estão nos arquivos dos agentes, em
`agents/`.

### Por que delegar

O `04` era escrito logo depois do `01`, pelo mesmo agente, para "validar os passos do PRD".
Isso é a direção invertida: o PRD é a **interpretação** do requisito, e testar a interpretação a
confirma. Medido sobre 318 métodos focais cobrindo 233 defeitos reais, com 11 modelos
(arXiv 2607.22883), derivar teste a partir do código/plano em vez da especificação multiplica por
~1,4 os testes que codificam o bug como comportamento esperado e corta por ~1,5 os que detectam o
defeito — a especificação mitiga o efeito, não o reverte.

É o mesmo princípio que criou o `00-requisito.md` como oráculo e que proíbe o
`feature-quality-gate` de corrigir o que julga: **quem escreve o plano não deriva o teste do
próprio plano**.

A auditoria das wikis reais que motivou a delegação está no README da `feature-test-design`
(`{skills}/feature-test-design/README.md`) — fonte única desses números.

### O contrato da delegação

```text
Invocar: feature-test-design

Entrada (nesta ordem de autoridade):
  1. 00-requisito.md            → ORÁCULO. É daqui que o comportamento esperado sai
  2. 01-plano-acao.md           → APENAS paths, rotas, stack e a tabela ## Superfície de UI
  3. 02-decisoes-arquiteturais.md → só ## Superfície Livewire
  4. .ai/rules/, tests/Pest.php → convenção de teste do projeto
  5. versões: Pest, Filament, Livewire, Laravel

Saída:
  - 04-casos-de-teste.md   (sempre)
  - 05-casos-de-teste-browser.md   (só se o gate do 05 passar — SKILL.md, seção "Gate do 05")
  - perguntas novas devolvidas para ## Ambiguidades do 00-requisito.md

Proibido passar como entrada:
  - implementação da feature (ela ainda não existe; se existir, não é fonte de comportamento)
```

### Contrato do construtor de testes (`executor-ct`)

O teste Pest de backend nasce do Gherkin do `04`, escrito por quem **não implementou** — no Claude
Code, o sub-agente `fw-executor-ct` (`sonnet`; definição em
[`agents/fw-executor-ct.md`](../agents/fw-executor-ct.md)). É a generalização do contrato dos CT-B para
o backend, medida em 5 lotes (2026-09-21): **todo vermelho que sobrou era defeito real**. O
contrato, em resumo — o arquivo do agente tem o texto completo:

- **Fonte é o `04`**: `## Setup Global` inteiro + só as regras/cenários do lote. Pode ler `app/`
  para descobrir nome de classe, método e rota que o cenário deixa em aberto; **nunca** para
  inferir o `Então`. Não lê `01` nem `02`
- **Fixture por transições reais**: a situação de partida se constrói chamando a máquina de
  estados do domínio (`enviar()`, `aprovar()`…), não gravando `situacao` à força — reimplementar a
  transição no teste esconde exatamente o defeito que o teste existe para pegar. O helper
  (`{entidade}Em('{situacao}')`) vive em `tests/Pest.php` e é dono de um lote `D0`, anterior aos
  outros
- **Um lote por arquivo, arquivos disjuntos** entre construtores paralelos; `tests/Pest.php` tem um
  único dono
- **Todo `Então` vira asserção; o nome do teste começa com `[CT-nn]`**; `Esquema do Cenário` vira
  `->with([...])`, uma linha por `Exemplos`; cenário `@obsoleto` não vira teste
- **Vermelho é classificado antes de qualquer edição** — a regra (causas a/b/c, 3 iterações,
  vermelho por (b) roteado pela sessão) está no corpo do `SKILL.md`, seção *Execução dos testes*
- **Proibido**: tocar `app/`, `database/`, `config/`; relaxar asserção; remover cenário; editar
  `00`/`01`/`02`/`04`
- **Saída em formato fixo**: arquivos e contagem; status por CT com a causa a/b/c; divergências
  (o que o `04` afirma / o que o código faz / `arquivo:símbolo:linha`); ambiguidades do `04` que
  teve de resolver; saída literal do `pest` e do `pint`
- **Interrompido no meio** (limite de sessão): reporta *"estado parcial"* com os arquivos tocados;
  a sessão confere `git status` antes de retomá-lo por `SendMessage`

### Ciclo de escrita e auditoria dos CT-B (loop + sub-agente)

A **especificação** dos CT-B é da `feature-test-design`. A **execução** deles contra a UI real é
desta skill, no step 7, e roda em loop delegado a um sub-agente — porque falha de browser
despeja HTML, snapshot e stack de Playwright no contexto, porque acertar seletor e timing é
tentativa e erro, e porque quem escreve o teste a partir do `05` não deve ser quem implementou.

**Contrato do sub-agente**:

```text
Entrada:
  - 05-casos-de-teste-browser.md   (os CT-B a implementar)
  - 01-plano-acao.md               (seção ## Superfície de UI — o que foi desenhado)

Tarefa:
  1. Escrever tests/Browser/{Feature}/{Nome}Test.php a partir dos CT-B
  2. Rodar: vendor/bin/pest tests/Browser --filter={Feature}   (ou --testsuite=Browser, se o phpunit.xml define a suíte; NUNCA com --parallel)
  3. Se falhar, classificar a causa ANTES de mexer em qualquer coisa:
     (a) CT-B especificado errado (seletor/rota/texto)  → corrigir o CT-B no arquivo 05
     (b) Implementação divergente do PRD                → NÃO corrigir; registrar divergência
     (c) Flake (timing/assíncrono)                      → rever a estratégia de espera e anotar
  4. Nas causas (a) e (c), se o Playwright MCP estiver disponível, observar a página ao vivo
     para descobrir o locator/estado real. Na causa (b): NÃO usar o MCP para contornar
  5. Repetir no máximo 3 iterações

PROIBIDO:
  - Alterar código de aplicação para o teste passar
  - Relaxar assertion para "ficar verde"
  - Remover CT-B que não passou

Saída (formato fixo):
  - Arquivos de teste criados/alterados
  - Status por CT-B: verde | vermelho + causa classificada (a/b/c)
  - Tabela "Desenhado × Implementado" preenchida
  - Lista de divergências para "Desvios do Plano" do 03-progresso.md
```

> **Sondagem rápida dentro do loop**: `vendor/bin/pest --agent='visit("/rota")->assertSee("...");'`
> confirma uma premissa de UI sem versionar nada. Serve para descobrir, não para provar.
