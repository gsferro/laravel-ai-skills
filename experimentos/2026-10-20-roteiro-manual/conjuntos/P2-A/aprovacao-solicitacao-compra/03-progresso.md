# Progresso — FERRO-830

**Estado**: em planejamento
**Data**: 2026-10-20
**Branch lógica / pasta**: saida-p2-a, conforme instrução do usuário; não há repositório Git.
**Base pretendida**: main, não verificável nesta cópia.
**Limite da sessão**: steps 0 a 4 da feature-wiki; parar antes do step 5. Nenhuma implementação autorizada.

## 1. Preparar channel da feature

- [ ] Resolver Q1 antes de criar configuração sem uso.
- [ ] Preparar somente o channel definido no passo 1 do PRD, após escopo implementável.
- [ ] Preservar channels existentes e confirmar retenção na versão instalada.

**Bloqueado por**: RQ-01 (aberta — Q1).

## 2. Integrar o domínio e sua persistência, após resolver Q1

- [ ] Receber resposta do solicitante sobre criação ou fornecimento do domínio.
- [ ] Incorporar resposta como Adendo, revisar schema, nomes e paths antes de gerar arquivos.
- [ ] Confirmar fonte de centro de custo e responsáveis, relações, tipos, nullable, índices e constraints.
- [ ] Planejar factories e identidade de rota conforme entidade efetivamente autorizada.

**Bloqueado por**: RQ-01 (aberta — Q1), RQ-15 (aberta — Q1), RQ-16 (aberta — Q1). Recortes de Q2/Q6/Q7/Q11/Q14–Q16 também pendentes.

## 3. Criar e manter rascunho na fronteira do solicitante

- [ ] Provar gravação por componente, não somente abertura de página.
- [ ] Aplicar identidade e estado na mutação de domínio.
- [ ] Preservar edição/exclusão em rascunho e imutabilidade final.
- [ ] Resolver limites de texto/valor sem truncamento ou arredondamento presumidos.
- [ ] Implementar logs seguros definidos no PRD, somente após autorização.

**Bloqueado por**: RQ-01 (aberta — Q1), RQ-02 (aberta — Q1), RQ-03 (aberta — Q1), RQ-11 (aberta — Q1), RQ-13 (aberta — Q1). Q6/Q7/Q12/Q14–Q16/Q19 pendentes nos respectivos recortes.

## 4. Aplicar envio, decisões, devolução e cancelamento atomicamente

- [ ] Preservar gestor primeiro e diretor adicional quando valor > R$ 5.000.
- [ ] Preservar rejeição do gestor com justificativa e retorno ao rascunho.
- [ ] Preservar reenvio e cancelamento pelo solicitante antes da aprovação final.
- [ ] Não preencher rejeição pelo diretor, acúmulo de papéis, ciclos ou substituição por recomendação.
- [ ] Persistir decisão e estado atomicamente, impedindo duplo resultado de corrida.
- [ ] Aplicar logs de sucesso, decisão e recusa com allowlist segura.

**Bloqueado por**: RQ-04 (aberta — Q1), RQ-05 (aberta — Q1), RQ-06 (aberta — Q1), RQ-07 (aberta — Q1), RQ-08 (aberta — Q1), RQ-09 (aberta — Q1), RQ-10 (aberta — Q1), RQ-12 (aberta — Q1), RQ-13 (aberta — Q1), RQ-14 (aberta — Q1). Recortes de Q2–Q5/Q7–Q13/Q15/Q16/Q18/Q19 pendentes.

## 5. Expor status e aprovadores nas telas autorizadas

- [ ] Criar ou integrar as telas somente quando o domínio estiver definido.
- [ ] Aplicar o mesmo escopo na lista, binding, busca global e execução das ações.
- [ ] Exibir autoria registrada da etapa e status, sem inferir autoria do cargo atual.
- [ ] Confirmar visibilidade histórica e destino de link com o solicitante.
- [ ] Atualizar inventário Livewire com métodos/estado efetivos e vendor real.
- [ ] Gerar e distribuir permissões sem dar poderes administrativos indevidos a panel_user.

**Bloqueado por**: RQ-15 (aberta — Q1), RQ-16 (aberta — Q1), além das cláusulas abertas das ações. Recortes Q3–Q7/Q10–Q13/Q17/Q19 pendentes.

## 6. Notificar o próximo aprovador por e-mail

- [ ] Reutilizar Notification enfileirada e despacho após commit.
- [ ] Distinguir enfileiramento de entrega nos logs.
- [ ] Definir com o solicitante destino do link, mensagem obsoleta e garantia de entrega.
- [ ] Verificar worker e transporte real em ambiente autorizado.
- [ ] Não criar job, evento/listener ou outbox redundantes sem necessidade confirmada.

**Bloqueado por**: RQ-04 (aberta — Q1), RQ-05 (aberta — Q1), RQ-17 (aberta — Q1). Q2/Q8/Q9/Q17/Q18 pendentes.

## 7. Validar e preparar entrega quando houver autorização futura

- [ ] Retomar no step 5, sem apresentar este planejamento como revisado.
- [ ] Derivar testes pela feature-test-design somente no step 7.
- [ ] Executar baseline no repositório e ambiente reais antes do primeiro commit.
- [ ] Validar somente o mínimo afetado, com regressão da infraestrutura compartilhada.
- [ ] Executar revisão independente, reconciliação e QA nas etapas próprias antes de PR.

**Bloqueado por**: todas as RQ abertas em Q1 e ausência de autorização para etapas posteriores nesta sessão.

## Testes

Seção reservada ao step 7. Nenhum CT, CT-B, arquivo de teste ou cenário Gherkin criado.

A pilha declarada/lock foi verificada: Pest v5.1.1 e browser plugin v5.0.1 no lock; Playwright ^1.62.1 no package.json. `tests/Pest.php` aplica RefreshDatabase, configura TIA local e timeout browser de 20.000 ms. `composer test:browser` inclui npm run build. O teste `tests/Browser/PerfisTest.php` foi lido para convenção de actingAs.

Não há vendor instalado. Testes de aplicação e baseline não foram executados. A existência do lock não prova instalação. Esta sessão não derivou costuras e não decidiu criar `05`.

## Tickets

Step 8 não executado. Não há decisão de fatiamento ou “não fatiado”. Nenhum arquivo `07-tickets/` foi criado.

## Verificação Final

Esta seção acompanha a entrega futura da feature; permanece aberta.

- [ ] Resolver bloqueios de requisito por resposta com fonte e Adendo.
- [ ] Executar steps 5 e 6 de revisão do planejamento.
- [ ] Derivar testes e confirmar costuras no step 7.
- [ ] Executar testes afetados e regressão contra baseline real.
- [ ] Formatar PHP alterado com `vendor/bin/pint --dirty --format agent`.
- [ ] Medir custo com volume acima de uma página.
- [ ] Executar revisão independente do diff antes da reconciliação.
- [ ] Reconciliar citações, IDs, docs e rules na etapa própria.
- [ ] Executar quality gate e registrar relatório/veredito.
- [ ] Abrir PR somente quando autorizado e com ambiente/repositório disponíveis.

Não rodar os scripts de reconciliação do step 10 agora: `04` e implementação ainda não existem. A verificação documental desta sessão fica registrada na Auditoria Pré-Implementação, sem se passar por execução desses gates.

## Revisão do Diff (step 9)

Não executada. Nenhum diff de aplicação produzido ou revisado. Não há achados, rejeições ou selo de independência.

## Conformidade com Rules

Avaliação de código reservada ao step 10; nenhuma conformidade de implementação declarada. Para planejar, o índice de rules e as regras Filament/testes/browser foram lidos. A wiki segue o limite de escrita informado pelo usuário.

## Quality Gate

Não executado. Nenhum ciclo, veredito ou relatório `06` emitido. A feature permanece em planejamento.

## Candidatos a Rule

Step 12 não executado. Não invocar requirement-to-rule ou record-rule nesta sessão; nenhuma rule foi criada.

## Auditoria Pré-Implementação

### Steps 0–4 e limite de parada

- Step 0: card capturado literalmente antes de pesquisa do projeto, com fonte e fidelidade no `00`.
- Step 1: `Test-Path .git` retornou False; usar saida-p2-a conforme autorização existente, sem criar branch ou repositório.
- Step 2: nome derivado do card: aprovacao-solicitacao-compra. O path alvo não existia antes da criação; não houve sobrescrita.
- Step 3: pesquisa de código, regras, rotas, configuração, lock, factories, testes existentes e wikis de produção. Fontes oficiais usadas por ausência de Boost.
- Step 4: somente `00`, `01`, `02` e `03`, com perguntas, bloqueios, decisões rotineiras e inventário Livewire proposto. Prosa normal nos documentos.
- **Parada**: antes do step 5. Nenhuma revisão profunda, classe irmã, Ponytail-review, derivação de testes, implementação, QA ou rule executada.
- A numeração dos passos de implementação do PRD não é a numeração dos steps da skill. Espelhar o passo “5. Expor status…” aqui não significa executar o step 5 da skill.

### Entrevista e ausência de resposta

**Entendimento confirmado: não — 2026-10-20 — desenvolvedor e solicitante indisponíveis; a autorização existente cobre planejamento até step 4, não confirmação de conteúdo nem implementação.**

Não fabricar a linha de confirmação exigida antes de avançar ao step 5. Registrar a falta de confirmação é a saída honesta desta execução limitada.

- Rodada 1: fronteira de requisito registrada em `00`; nenhuma resposta recebida.
- Perguntas ao desenvolvedor: nenhuma. As escolhas técnicas rotineiras têm convenção no projeto. As dúvidas materiais identificadas mudam comportamento observável e pertencem ao solicitante.
- Perguntas ao solicitante: Q1–Q19, todas na raia requisito. Fato e desenho não foram depositados no `00`.
- Sem pergunta de fato ao usuário: ausência do domínio, versão do lock, padrão de fila e limites do ambiente foram pesquisados.
- Q1 é dependência integral do escopo; manter RQ-01 a RQ-17 abertas, sem implementação. Obrigações explícitas continuam descritas nos passos condicionais.
- Q2–Q19 bloqueiam seus recortes dependentes; recomendações não viraram P-nn, decisões aceitas, CT ou regras.
- Acumulação de papéis considerada par a par: solicitante × gestor (Q3), solicitante × diretor (Q4), gestor × diretor (Q5).
- Sementes de visibilidade atual/histórica, destino de link e teto de cada texto livre consideradas em Q6/Q7/Q14/Q15/Q17.
- Sinal de mais de 30 perguntas de requisito não cruzado. Nenhuma sugestão ou execução antecipada do step 8.

### Registro por falta de resposta

Adotar a premissa de escopo mais estreita: não criar solicitação, centro de custo, cadastro de aprovadores ou motor isolado. Não reinterpretar Projeto ou Convite como domínio de compras. Isso bloqueia a entrega funcional e preserva o card integral.

Nenhuma autorização de implementação inferida do pedido de planejamento. Nenhuma resposta atribuída ao desenvolvedor ou solicitante. Nenhum Adendo criado sem resposta. Retomar somente a fronteira autorizada pelo usuário da próxima sessão.

### Degradações e desvios declarados

| Limitação / desvio | Evidência | Consequência |
|---|---|---|
| Sem repositório Git | Test-Path .git = False. | Pasta lógica saida-p2-a; sem git log/diff/base/baseline/commit. |
| Sem dependências PHP | Test-Path vendor = False; composer show --direct: “No dependencies installed. Try running composer install or update.” | Versões pelo lock, não instalação. Artisan falha por vendor/autoload.php ausente. |
| Boost não exposto | Filtro da lista de tools por boost e search.docs retornou []. | Sem search-docs/schema/query; documentação oficial e fontes locais como fallback declarado. |
| Banco não inspecionado | database-schema/query indisponíveis e app não inicializa. | Migrations não foram chamadas de schema real. Nenhuma SQL/tinker executada. |
| Superfície herdada sem código instalado | Test-Path vendor/filament e vendor/livewire = False. | Quatro greps de pacote não verificáveis; inventário é proposto, sem proteção certificada. |
| Sem Playwright MCP configurado para este projeto | Nenhum Playwright MCP exposto; app não inicializa. | Nenhuma navegação, locator ou prova de browser obtida. A referência foi lida; não há CT-B agora. |
| Glossário global não criado | Test-Path wikis/glossario.md = False; usuário proíbe escrita externa à feature. | Vocabulário do card mantido na wiki; criação de glossário global adiada. |
| Caveman ultra da referência não aplicado | Host impõe caveman; wiki exige prosa normal. | Comunicação terse e documentos completos; nenhuma alteração de modo alegada. |
| Controle do subagente contratual | Contexto herdado, ferramentas de execução expostas; sem hook/sandbox de leitura por path. | Não chamar investigação de revisão cega ou isolamento técnico. |
| Sem hash anterior ao despacho | Snapshot de conteúdo/hashes não foi capturado antes do primeiro despacho. | Auditoria de integridade retrospectiva incompleta; relato de ausência de escrita não é prova criptográfica. Pesquisa crítica foi conferida diretamente. |

Não instalar ferramentas nem mudar arquivos globais para compensar essas limitações nesta execução.

### Revisão profunda / classe irmã (step 5)

Não executadas. Conferir evidências ao construir citações no step 4 não equivale a revisar o plano inteiro.

### Auditoria Ponytail (step 6)

Não executada. A filosofia minimalista do PRD não equivale a invocar o gate.

### Conferência documental do step 4

Conferência executada em PowerShell, em memória, sem criar script: extrair o bloco Texto Original e comparar com o card por igualdade sensível a caracteres; comparar os títulos numerados de `01` e `03`; exigir sequência única Q1–Q19 e conjunto exato dos quatro nomes de arquivo. Resultado literal: `OK: card literal; sequência única Q1-Q19; espelho 01/03; somente arquivos 00-03.` Exit 0, 2026-10-20.

Contagens derivadas por comando, com `$wikiPath = 'wikis/specs/saida-p2-a/aprovacao-solicitacao-compra'`:

```powershell
rg -c '^\| RQ-' "$wikiPath/00-requisito.md" "$wikiPath/01-plano-acao.md"
# 00: 17; 01: 17
rg -c '^❓ Q[0-9]+ · raia: requisito' "$wikiPath/00-requisito.md"
# 19
rg -c '^### [1-7]\. ' "$wikiPath/01-plano-acao.md"
# 7
rg -c '^## [1-7]\. ' "$wikiPath/03-progresso.md"
# 7
```

Essa conferência documental não avalia APIs, premissas de implementação ou cumprimento funcional e não executa o step 5.

## Despachos

Host: Codex, família GPT-6 informada pelas instruções; identificador exato do modelo/esforço em execução não exposto. Nenhum alias Claude aplicado. Ferramentas reais: exec local, apply_patch, busca web e colaboração com contexto novo ou herdado. Sem Boost e sem isolamento técnico de leitura por path; aprovação automática “never”, escrita restrita por contrato do usuário.

| # | Step | Agente / tarefa | Modelo | Não recebeu | Resultado | Custo | Auditoria do retorno |
|---|---|---|---|---|---|---|---|
| 1 | 3 | mapear_dominio — mapeamento amplo, fallback de Explore por colaboração disponível | Herdado; identificador exato não exposto | Paths experimentais proibidos por contrato; recebeu histórico da sessão, sem cegueira exigida. | Ausência do domínio de compras; padrões User/Tenant/Convite; antecedentes técnicos; nenhum arquivo escrito segundo o retorno. | —, host não reportou tokens/duração do despacho. | Presença conferida; ausência de domínio reproduzida pela sessão; User, Notification e Gate/queue amostrados diretamente. Sem hash prévio, integridade não certificada retrospectivamente. |

**Sem despacho — motivos**: captura verbatim, decomposição, nome e entrevista pertencem à sessão; confirmação de trechos/citações é determinística e barata. Redação conjunta de `00`–`03` feita na sessão por forte interdependência dos bloqueios de escopo; espelho do progresso conferido mecanicamente. Nenhum julgamento independente foi substituído por autorrevisão.

### Auditoria da pesquisa delegada

O retorno trouxe comandos, saídas negativas e referências, não decisões de negócio. As evidências críticas foram lidas diretamente pela sessão:

- User com identidade de painel/tenant e Notifiable; methods e traits lidos.
- ConviteDeAcesso com via/mail, ShouldQueue e URL pelo painel; métodos via, toMail e url confirmados por rg.
- Gate::before em KitServiceProvider e after_commit false na conexão database confirmados por rg.
- Busca de termos do domínio reproduzida sem linhas. Não aceitar trechos de IA como domínio de compras.

O subagente não leu skills adicionais segundo seu retorno. Não houve redespacho ou correção de aplicação.

## Blockers

- [ ] Q1: definir escopo do domínio ausente com o solicitante.
- [ ] Q2–Q19: responder recortes materiais de regra, visibilidade, limites e notificação.
- [ ] Confirmar entendimento antes de eventual step 5, sem inferir aprovação do silêncio.
- [ ] Restaurar dependências e acesso às ferramentas/dados em sessão autorizada; não compensar agora com instalações.
- [ ] Esclarecer schema e fronteira real da UI antes de executar plano.

## Desvios do Plano

Nenhuma implementação ocorreu. Limitações do planejamento estão declaradas acima e no PRD. Nenhuma mudança funcional foi mascarada como desvio.

## Notas de Implementação

Não aplicável nesta sessão: implementação proibida pelo usuário.

## Referências Abertas

Todas abaixo foram abertas como arquivos específicos, sem carregar pasta inteira:

- `feature-wiki/references/hosts-e-subagentes.md` — início / steps 0–3 — 2026-10-20.
- `feature-wiki/references/ponytail-caveman.md` — início — 2026-10-20.
- `feature-wiki/references/pesquisa-step-3.md` — step 3 — 2026-10-20.
- `feature-wiki/references/roteamento-e-despacho.md` — step 3, antes do despacho — 2026-10-20.
- `feature-wiki/references/citacoes-de-codigo.md` — steps 3–4 — 2026-10-20.
- `feature-wiki/references/glossario.md` — steps 3–4 — 2026-10-20.
- `feature-wiki/references/playwright-mcp.md` — step 3 — 2026-10-20.
- `feature-wiki/references/pest-5.md` — step 3 — 2026-10-20.
- `feature-test-design/references/pest-plugin-browser.md` — step 3, conferência da pilha — 2026-10-20. Somente referência aberta; SKILL.md da feature-test-design não lido ou invocado.
- `feature-wiki/references/template-00-requisito.md` — step 4, antes da escrita — 2026-10-20.
- `feature-wiki/references/entrevista-tres-raias.md` — step 4, preparação da primeira rodada — 2026-10-20.
- `feature-wiki/references/template-01-plano.md` — step 4, antes da escrita — 2026-10-20.
- `feature-wiki/references/padrao-de-log.md` — step 4, antes da especificação dos logs — 2026-10-20.
- `feature-wiki/references/template-02-adr.md` — step 4, antes da escrita — 2026-10-20.
- `feature-wiki/references/template-03-progresso.md` — step 4, antes da escrita — 2026-10-20.
- `feature-wiki/references/estrutura-criada.md` — step 4, decisão de não criar extras — 2026-10-20.

Não abertos: casos-medidos, referências de steps posteriores e SKILL.md das skills de teste/QA/tickets/rules. Links de contexto histórico não foram tratados como ordem de carregar toda a coletânea.

## Retrospectiva

- **Funcionou bem**: ausência das entidades foi identificada antes de planejar sua criação como fato; recomendações ficaram separadas do oráculo.
- **Limite desta entrega**: plano condicionado, sem confirmação humana, execução de testes, revisão profunda ou prova funcional. Retomar sem considerar a wiki uma feature concluída.

