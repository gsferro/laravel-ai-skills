# Progresso — FERRO-812

**Estado**: em planejamento
**Data**: 2026-10-20.
**Limite desta execução**: steps 0–4 da feature-wiki; parada antes do step 5.
**Branch para pasta**: saida-p4, determinada pelo usuário porque não há .git.
**Base nominal**: main, sem branch/commit de base verificável nesta cópia.
**Feature**: cupons-de-desconto, derivada do requisito capturado.
**Host**: Codex; modelo informado pelas instruções da sessão: GPT-6. Variante exata e esforço efetivo não expostos.
**Skill lida integralmente**: `.ai/skills/feature-wiki/SKILL.md`, metadata.version **4.2.0**. Nenhum outro SKILL.md foi lido nesta execução.

## 1. Preparar channel de logs

- [ ] Adicionar o channel no ambiente de implementação, sem alterar defaults.
- [ ] Verificar resolução e formato seguro sem confundir logging operacional com auditoria de aplicação.

## 2. Modelar cadastro mínimo e unicidade

- [ ] Confirmar schema vivo, versões instaladas e comandos Artisan antes de gerar arquivos.
- [ ] Fechar Q2/Q6/Q7/Q8 e o recorte monetário de Q9 antes de concretizar schema pendente.
- [ ] Criar model, enum, migration, factory/seeder mínimos conforme PRD, com tabela explícita e UUID.
- [ ] Proteger código com unique no banco e manter contador fora da entrada editável.
- [ ] Não criar pedido ou aplicação de cupom; nenhuma migration parcial baseada em recomendação não respondida.

## 3. Proteger operações e ajustar permissões

- [ ] Fechar Q2/Q3/Q4 antes do mapeamento concreto de autorização.
- [ ] Criar policy e recortar permissões por ação sem retirar consulta permitida.
- [ ] Gerar permissões e depois atribuí-las, preservando policies existentes.
- [ ] Conferir interação com Gate::before; não considerar policy uma barreira que o before efetivamente pula.

## 4. Construir cadastro e consulta nos painéis definidos

- [ ] Confirmar painéis/rotas e criar Resources/páginas conforme respostas.
- [ ] Gravar e validar os campos determinados, sem expor contador, ator ou tenant ao cliente.
- [ ] Aplicar fronteira no servidor, inclusive URL direta, busca e actions forjadas.
- [ ] Resolver predicado ativo: **Bloqueado por**: RQ-11 (aberta — Q5).
- [ ] Resolver recortes históricos e domínios Q6–Q8/Q12 antes de entregar as respectivas ações.
- [ ] Conferir e completar Superfície Livewire no vendor instalado e no código efetivamente criado.
- [ ] Instrumentar início, sucesso, negação, validação e falha com dados seguros.

## 5. Verificar cadastro, autorização e limites do escopo

- [ ] Derivar CT no step 7 a partir do 00, após os steps 5/6; não derivar teste do PRD.
- [ ] Provar gravação por componente e banco, autorização direta, unicidade e isolamento conforme contratos respondidos.
- [ ] Executar testes afetados e regressões pertinentes, sem browser paralelo.
- [ ] Manter aplicação/auditoria explicitamente pendentes até resposta como Adendo; não declarar card completo com apenas cadastro.

## Testes

Preenchimento de CT, nomes finais e costuras reservado ao step 7, não executado. Nenhum teste criado, modificado ou excluído. Não existe 04 nem 05 de browser nesta pasta.

PHP 8.4.10 está disponível. Pest v5.1.1 e browser plugin v5.0.1 estão no lock, mas vendor está ausente. Não há baseline executada, resultado verde, contagem de testes ou lista comprovada de falhas pré-existentes.

Leituras do stack: tests/Pest.php usa RefreshDatabase em Feature e configura browser timeout de 20.000 ms; TIA local usa main. package.json declara Playwright ^1.62.1; node_modules/playwright está ausente. O script Composer test:browser inclui npm run build. Existe public/build/manifest.json, cuja atualidade não foi verificada. Não foi planejado CT-B nem lida a referência de plugin browser: ela será obrigatória antes dessa decisão.

## Tickets

Step 8 não executado. Nenhuma decisão de fatiamento, sugestão formal baseada em limiar ou arquivo 07 criado. Contar requisitos nesta etapa não equivale a executar o step 8.

## Verificação Final

Checklist de trabalho futuro; nenhum item foi fechado:
- [ ] Concluir pesquisa indisponível de schema, vendor, rotas e versões instaladas.
- [ ] Resolver requisitos materiais por Adendo, preservando texto original.
- [ ] Executar revisão profunda (step 5), auditoria Ponytail (step 6) e derivação/revisão de CT (step 7).
- [ ] Obter baseline em repositório/ambiente reais, com falhas pré-existentes nomeadas.
- [ ] Executar testes focalizados e regressões de autorização/tenancy.
- [ ] Formatar PHP com vendor/bin/pint --dirty --format agent somente após modificação de PHP.
- [ ] Executar browser em série apenas se CT-B for confirmado, após build.
- [ ] Executar mutation testing pertinente pelo lançador Windows e registrar duração/sobreviventes.
- [ ] Medir custo com população acima da página.
- [ ] Realizar revisão independente do diff no step 9, antes da reconciliação.
- [ ] Rodar checks de reconciliação no step 10 com saída e exit.
- [ ] Gerar artefato manual solicitado somente na etapa pós-10 e conferir roteiro-manual.sh.
- [ ] Obter quality gate do step 11 antes de declarar feature concluída ou abrir PR.

### Conferência documental desta entrega

A conferência desta sessão limita-se a fidelidade da captura, cobertura de IDs, estrutura/espelho e escrita dentro da pasta autorizada. Não é revisão profunda de premissas, execução de CT, reconciliação final nem quality gate.

Contagem por comando em 2026-10-20:
```powershell
$text = Get-Content -LiteralPath 'wikis/specs/saida-p4/cupons-de-desconto/00-requisito.md' -Raw
$clauses = [regex]::Matches($text, '(?m)^\| RQ-\d+ \|.*$')
$clauses.Count
@($clauses | Where-Object { $_.Value -match 'aberta —' }).Count
[regex]::Matches($text, '(?m)^❓ Q\d+ · raia: requisito').Count
[regex]::Matches(($text -split '### Perguntas preparadas')[0], '(?m)^❓ Q\d+').Count
```
Saída: 19 RQ; 8 abertas; 12 perguntas de requisito; 8 perguntas na fronteira atual e 4 dependentes de Q1. O plano tem 5 passos, contados por `[regex]::Matches($plano, '(?m)^### \d+\. ').Count`; o progresso os espelha. Nenhum número é contagem de testes.

Conferência documental executada em PowerShell e comparada em memória pela sessão, em 2026-10-20: extração do bloco text do 00 idêntica ao card recebido (normalizados apenas os terminadores CRLF/LF); conjunto de arquivos igual a 00/01/02/03; cobertura de RQ sem falta ou excesso; Q1–Q12 únicos; títulos dos cinco passos do 01 e 03 idênticos; citações PHP do 01/02 com símbolo na linha indicada. Resultado: originalMatches=true, Unexpected=[], Missing=[], MissingCoverage=[], ExtraCoverage=[], StepsEqual=true, CitationErrors=[]. Não foram executados scripts de reconciliação nem revisão de premissas do step 5.

Repetido o inventário/SHA256 documentado em Despachos ao terminar a escrita: filesBefore=237, filesAfter=237, changed=[]. As ferramentas de edição desta sessão escreveram somente os quatro documentos desta pasta.

## Revisão do Diff (step 9)

Não executada. Sem diff Git disponível e fora do limite desta execução. Nenhum achado/rejeição fictício nem selo de revisão independente.

## Conformidade com Rules

A tabela registra leitura para planejamento, não um veredito sobre código ainda inexistente. Sem diff, o script do step 10 não foi executado.

| Rule | Glob previsto | Situação no planejamento | Evidência |
|---|---|---|---|
| .ai/rules/filament.md | app/Filament/** | lida; conformidade de implementação pendente | PRD exige policy, recorte do seeder e fronteira no servidor; não grava roles por sync de relação. |
| .ai/rules/testes.md | tests/** | lida; conformidade de implementação pendente | PRD exige gravação por componente, helpers compartilhados apenas em Pest.php e sem clone de helper. |
| .ai/rules/testes-browser.md | tests/Browser/** | lida por contexto do stack; nenhuma costura browser definida | PRD preserva execução em série e build como pré-condição; CT-B ainda não existe. |
| .ai/rules/auth.md | app/Filament/Pages/Auth/** | fora do escopo de arquivos planejados | Só índice e resultado da busca por palavras-chave; conteúdo não ativado porque não há alteração em auth. |

O índice foi aberto antes de planejar; busca temática equivalente a grep-rin executada com rg. Não foi necessário gravar rule; step 12 não executado e escrever fora da wiki é proibido pelo usuário.

## Quality Gate

Não executado; nenhuma aprovação. Relatório 06 não criado. Estado permanece em planejamento.

## Candidatos a Rule

Step 12 não executado. Nenhum candidato coletado, nenhuma rule gravada.

## Auditoria Pré-Implementação

### Steps 0–4 e entrevista

| Step | Resultado / evidência |
|---|---|
| 0 | Card escrito capturado literalmente da mensagem do usuário, antes de investigar domínio; a sessão principal preservou texto e decompôs afirmações independentes em RQ. |
| 1 | Test-Path .git retornou False. Usada pasta saida-p4 por instrução explícita, sem criar branch, inicializar Git ou usar o Git de um diretório pai. |
| 2 | Nome cupons-de-desconto, sem alteração de escopo. Test-Path da pasta-alvo antes da criação retornou False; nenhuma wiki sobrescrita. |
| 3 | Arquivos locais, wikis de produção pontuais, versões do lock e documentação oficial consultados; lacunas de MCP/vendor/schema declaradas abaixo. |
| 4 | Criados 00, 01, 02 e 03, entrevista registrada com fronteira e recomendações. Nenhuma resposta simulada; nenhuma implementação ou arquivo posterior criado. |

Entendimento confirmado: **não** — 2026-10-20 — desenvolvedor e solicitante indisponíveis; autorização existente permite somente steps 0–4, não aprovação de comportamento ou implementação. Rodada 1 registrada sem respostas: perguntas ao desenvolvedor 0 fato, 0 desenho, 0 requisito; perguntas ao solicitante 8 de requisito na fronteira atual e 4 de requisito preparadas após Q1. Total de perguntas no 00: 12 requisito, 0 fato, 0 desenho.

Não há motivo para perguntar ao desenvolvedor fatos descobertos no repositório. Escolhas técnicas rotineiras foram documentadas por convenção/autorização existente. Escolhas de comportamento foram encaminhadas ao solicitante. A fronteira material não foi fechada; nenhuma linha de confirmação plena ou aceitação tácita foi registrada.

Roteiro manual: sim — 2026-10-20 — instrução explícita do desenvolvedor — “gere também o roteiro de teste manual”; há UI e aceite humano.

A instrução explícita dispensa a pergunta sobre roteiro; não consome Qn. Decisão registrada somente nesta seção. O 08 será escrito depois do step 10, antes do step 11; produzi-lo agora violaria o corte solicitado. Não há geração antecipada, questionário redundante nem registro “não — sem resposta” para decisão já fornecida.

### Sementes e ausência de respostas

- Papéis: Q3 trata par admin_organizacao + panel_user; Q4 trata master_global sem admin. Admin + panel_user já satisfaz admin sob leitura literal; a definição de admin continua pendente, sem criar exclusividade ou segregação não solicitada.
- Visibilidade: Q5 inclui usuário atual versus participante histórico, sem presumir exceção para quem já aplicou.
- Texto livre: Q6 pergunta teto e domínio do código, com recomendação sujeita à resposta.
- Notificação: card não pede notificação; nenhum link, canal ou fluxo externo inventado.
- P-01 registra o fallback mais estreito para ausência de pedidos. RQ-12–RQ-16/RQ-18/RQ-19 permanecem abertas; nenhum motor isolado foi tratado como entrega.
- Q5 mantém RQ-11 aberta. Q2–Q4 e Q6–Q8 bloqueiam somente os recortes materiais apontados; campos e proibições determinados continuam rastreados no PRD.
- Q9–Q12 aguardam Q1; não se fabricou uma segunda rodada respondida.
- Nenhuma recomendação monetária, temporal, de código, papel ou histórico foi promovida a requisito por falta de resposta.

### Confronto código × afirmação (step 5)

Não executado. O apontamento inicial de Gate::before e matriz de permissões pertence à pesquisa do step 3; não há rodada de revisão do PRD contra o código nesta execução.

### Revisão profunda (step 5)

Não executada, por instrução explícita de parar antes do step 5. Varredura de classe irmã para classes novas também não executada.

### Auditoria Ponytail (step 6)

Não executada. Nenhuma skill de auditoria foi lida ou ativada antecipadamente.

## Despachos

Ferramentas reais: execução PowerShell, apply_patch, web e subagente com fork_turns disponíveis. Boost e Playwright MCP específico não expostos. Subagente de pesquisa recebeu histórico por herança, sem requisito de cegueira; não é revisor independente. Contrato somente de leitura, sem sandbox de leitura por path, hooks Claude ou perfis instalados. Nenhum modelo alternativo escolhido.

| # | Step | Agente / tarefa | Modelo | Depende de / não recebeu | Resultado | Custo | Auditoria do retorno |
|---|---|---|---|---|---|---|---|
| 1 | 3 | mapear_contexto — mapeamento amplo do código, fallback de Explore | GPT-6 por herança; variante/esforço não expostos | requisito capturado; proibidos caminhos exp-* e testes Exp*, escrita, Artisan, outras skills/references e wiki nova | fatos de domínio, papéis, tenancy, auditoria, wikis de produção e negativas; nenhum arquivo escrito | —; host não forneceu tokens/duração | Presença conferida; Gate::before, PapeisSeeder e AuditsFillables amostrados diretamente; inventário e SHA256 de 237 arquivos permitidos de app/database/config/routes/tests idênticos antes/depois. |
| — | 0, 1, 2, 3, 4 | Sem despacho — captura verbatim, decisões da sessão, checagens determinísticas e edição interdependente de 00/01/02/03 | GPT-6 da sessão | 01/02 dependem da pesquisa e da entrevista; 03 depende dos passos finais do 01 | sessão escreveu os artefatos; não houve segundo escritor nos mesmos arquivos | — | Conferência documental apenas, sem julgamento cego. |

O subagente pesquisou em paralelo às leituras de referências e documentação oficial da sessão; a escrita dependeu do pacote de pesquisa. Não se delegaram requisito literal, perguntas, decomposição ou decisões finais. Não houve despacho de construtor para os rascunhos 01/02: edição cirúrgica/interdependente com cláusulas abertas e fronteira de entrevista, exceção declarada, sem alegar independência.

Comando do inventário/hash antes e depois do despacho:
```powershell
$paths = rg --files app database config routes tests -g '!tests/Feature/Exp*' -g '!tests/Feature/Exp*/**'
$result = foreach ($path in $paths) {
    $hash = Get-FileHash -LiteralPath $path -Algorithm SHA256
    [pscustomobject]@{ Path = $path; Hash = $hash.Hash }
}
$result | ConvertTo-Json -Compress
```
Comparação da sessão em memória: before=237; after=237; differences=[].
Esse controle detecta mudanças no conjunto inventariado; não prova ausência de leitura nem fiscalização técnica dos caminhos proibidos.

## Blockers

- [ ] Solicitante indisponível: resolver Q1–Q8 da fronteira atual e depois Q9–Q12; registrar respostas por Adendo, não pelo desenvolvedor.
- [ ] Domínio de pedido ausente: preservar RQ-12–RQ-16/RQ-18/RQ-19 abertas até definição de escopo.
- [ ] Definição de ativo ausente: RQ-11 aberta — Q5.
- [ ] Vendor e Boost não disponíveis: versões efetivamente instaladas, schema, assinaturas e superfície herdada ainda não verificados.
- [ ] Sem Git: baseline da base e histórico não verificáveis; não há diff, TIA ou commit válido nesta cópia.
- [ ] Nenhuma autorização de implementação nesta sessão.

## Desvios do Plano

Nenhuma implementação ocorreu. As limitações abaixo são degradações da pesquisa, registradas também no PRD e na Superfície Livewire.

| Limitação / desvio | Evidência e consequência | Tratamento |
|---|---|---|
| Sem Git | Test-Path -LiteralPath .git: False; branch/log não consultados em repositório pai | saida-p4 por instrução; main nominal; sem inventar histórico/baseline. |
| Sem dependências instaladas | Test-Path vendor: False; composer show --direct: “No dependencies installed. Try running composer install or update.” | Usar composer.lock como versão resolvida, nunca instalada; não instalar dependências nesta sessão. |
| Boost indisponível | Busca em ALL_TOOLS por boost, search-docs e database-schema não encontrou ferramentas do servidor | Documentação oficial via web, com links no PRD; declarar que search-docs obrigatório não pôde executar. |
| Sem schema vivo | database-schema/query não expostos; Test-Path database/database.sqlite: False | Leitura de migrations/config como evidência estática; nenhuma consulta ou criação de DB. |
| Artisan indisponível | model:show User e route:list --except-vendor falharam em vendor/autoload.php | Leitura de User, traits, providers e routes; rotas runtime não confirmadas. |
| APIs e greps de vendor incompletos | Test-Path vendor/filament e vendor/owen-it/laravel-auditing: False | Tabela Livewire prospectiva com lacunas; sem afirmar os quatro greps de cada pacote como executados. |
| Auditoria v14 sem fonte instalada | Lock v14.0.6; documentação pública consultada rotulada v13 | Não importar API da versão errada; apoiar proposta no uso local existente e deixar compatibilidade pendente. |
| Sem Playwright MCP dedicado / app executável | Ferramentas específicas não expostas; node_modules/playwright ausente | Sem navegador ou locators; nenhuma observação usada como cobertura. |
| Glossário global ausente | Test-Path wikis/glossario.md: False | Não criar arquivo global: usuário proíbe escrita fora da feature. Sentidos pendentes de admin/ativo estão nas perguntas. |
| Ultra recomendado pela referência | Host mantém Caveman em modo caveman; comandos de plugin não foram expostos | Preservar instrução ativa do host, sem fingir invocação; documentos escritos em prosa normal. |
| Templates de etapas posteriores | 04/05/06/07/08 e geração de índice pertencem a etapas fora do corte | Não criar esses arquivos, não executar checks/gates posteriores. |

Provas negativas de domínio comercial:
```powershell
rg --files app database routes -g '*Pedido*' -g '*Order*' -g '*Venda*' -g '*Carrinho*' -g '*Cupom*' -g '*Coupon*'
# sem saída; exit 1
rg -n -i '\b(class|interface|trait|enum)\s+(Pedido|Pedidos|Order|Orders|Venda|Vendas|Carrinho|Carrinhos|Cupom|Cupons|Coupon|Coupons)\b' app database routes
# sem saída; exit 1
rg -n -i '\b(cupom|cupons|coupon|coupons|carrinho|carrinhos|orders)\b' app database routes
# sem saída; exit 1
```
Busca ampla por pedido/order/venda encontrou homônimos em prompts/comentários e demonstração “App de vendas”; isso não constitui entidade ou fluxo comercial. As negativas não afirmam que essas palavras jamais apareçam.

Comandos auxiliares da pesquisa:
```powershell
rg -n -i 'cupom|cupons|pedido|order|desconto|discount|admin|auditoria|log' .ai/rules
rg -n 'trait.*Logging|Log::channel|cupons-de-desconto' app config/logging.php
rg -n -i 'cupom|cupons|coupon|coupons|desconto' wikis/specs/main wikis/specs/feature
php artisan model:show User --no-interaction
php artisan route:list --except-vendor --no-interaction
```
Resultados: rules tem orientações de auth/Filament/testes; logging tem channels existentes, sem trait Logging ou channel da feature; pesquisa temática nas wikis de produção sem ocorrência; ambos os comandos Artisan falham antes do bootstrap com “Failed opening required .../vendor/autoload.php”.

## Notas de Implementação

Nenhuma implementação, migration, model, service, Resource, config ou teste foi criado/modificado. Nenhuma dependência, ambiente, banco, build, seeder, mensagem externa ou ação de publicação foi executada.

## Referências Abertas

Todas relativas a `.ai/skills/feature-wiki/references/`, salvo indicação. A leitura de SKILL.md completo não significa execução de seus steps posteriores.

- hosts-e-subagentes.md — início / step 3 — 2026-10-20.
- ponytail-caveman.md — início — 2026-10-20.
- pesquisa-step-3.md — step 3 — 2026-10-20.
- citacoes-de-codigo.md — steps 3/4 — 2026-10-20.
- roteamento-e-despacho.md — step 3, antes do despacho — 2026-10-20.
- entrevista-tres-raias.md — step 4, antes da entrevista — 2026-10-20.
- template-00-requisito.md — step 4 — 2026-10-20.
- template-01-plano.md — step 4 — 2026-10-20.
- template-02-adr.md — step 4 — 2026-10-20.
- template-03-progresso.md — step 4 — 2026-10-20.
- padrao-de-log.md — step 4 — 2026-10-20.
- estrutura-criada.md — step 4 — 2026-10-20.
- playwright-mcp.md — step 3 — 2026-10-20.
- pest-5.md — step 3 — 2026-10-20.
- glossario.md — steps 3/4 — 2026-10-20; glossário ausente e escrita global vedada.
- casos-medidos.md — pesquisa dos steps 3/4 e regras de despacho/templates — 2026-10-20; lidas seções iniciais até Superfície Livewire, checkbox, modelo de execução, tabela explícita e perguntas-semente; demais seções não carregadas.

Não abertos: template-08-roteiro-manual.md (geração somente pós-10); delegacao-casos-de-teste.md e SKILL.md de feature-test-design (step 7); pest-plugin-browser.md da feature-test-design (nenhum CT-B planejado/escrito); referências de tickets, quality gate e rules (steps não executados). Nenhuma pasta inteira de references foi lida.

## Retrospectiva

- **Funcionou bem**: pesquisa expôs a falta de pedidos e os privilégios automáticos antes de prometer uma implementação completa.
- **Limite desta entrega**: dúvidas de produto não foram respondidas por quem planeja; documentação está pronta para continuação, mas entendimento e execução permanecem pendentes.

