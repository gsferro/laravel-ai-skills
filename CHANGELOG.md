# Changelog

Histórico de evolução das skills desta coletânea.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); cada skill segue [Semantic Versioning](https://semver.org/lang/pt-BR/) de forma **independente**.

## Skills e versões atuais

| Skill | Versão | Tag |
|---|---|---|
| `feature-wiki` | 3.0.0 | `feature-wiki-v3.0.0` |
| `feature-test-design` | 1.8.0 | `feature-test-design-v1.8.0` |
| `feature-quality-gate` | 1.1.0 | `feature-quality-gate-v1.1.0` |
| `requirement-to-rule` | 1.2.0 | `requirement-to-rule-v1.2.0` |

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

---

# feature-wiki

Cria a estrutura de documentação de uma feature **antes** de implementá-la: requisito bruto, PRD, ADR, tracking de progresso e padrão de log.

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
   requisito — testar a interpretação a confirma. Medido sobre 318 defeitos reais com 11 modelos:
   derivar teste do código/plano em vez da especificação multiplica por ~8 os testes que codificam
   o bug como comportamento esperado e corta por ~3 os que o detectam.
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
