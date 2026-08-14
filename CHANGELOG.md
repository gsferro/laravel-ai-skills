# Changelog

Histórico de evolução das skills desta coletânea.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); cada skill segue [Semantic Versioning](https://semver.org/lang/pt-BR/) de forma **independente**.

## Skills e versões atuais

| Skill | Versão | Tag |
|---|---|---|
| `feature-wiki` | 2.10.0 | `feature-wiki-v2.10.0` |
| `feature-quality-gate` | 1.0.0 | `feature-quality-gate-v1.0.0` |
| `requirement-to-rule` | 1.1.0 | `requirement-to-rule-v1.1.0` |

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

Cria a estrutura de documentação de uma feature **antes** de implementá-la: requisito bruto, PRD, ADR, tracking de progresso, casos de teste e padrão de log.

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

# feature-quality-gate

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
