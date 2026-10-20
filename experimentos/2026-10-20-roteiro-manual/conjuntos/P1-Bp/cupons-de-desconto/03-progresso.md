# Progresso — FERRO-812

**Estado**: em planejamento

- **Data**: 2026-10-20.
- **Branch/pasta**: saida-p1-bp, por instrução explícita; não há repositório Git nesta cópia.
- **Base pretendida**: main, convenção da skill; sem branch/base real verificável.
- **Wiki**: `wikis/specs/saida-p1-bp/cupons-de-desconto/`.
- **Limite da invocação**: steps 0 a 4. Parada antes do step 5. Nenhuma implementação ou instalação autorizada.
- **Skill lida integralmente**: `.ai/skills/feature-wiki/SKILL.md`, metadata.version **4.2.0**. Não foi lido outro SKILL.md; a referência de browser da feature-test-design não equivale a ativar sua derivação.
- **Host**: Codex, Windows, PowerShell. **Modelo informado**: família GPT-6, conforme identidade da sessão; identificador exato e esforço efetivo não expostos. Subagente herdou o modelo, sem aliases de outro provedor.

## 1. Preparar channel de diagnóstico

- [ ] Adicionar somente o channel cupons-de-desconto no arquivo previsto no passo 1 do PRD.
- [ ] Conferir consumidores futuros sem alterar canais existentes.

Nenhum arquivo de configuração foi alterado.

## 2. Definir persistência do cadastro

- [ ] Resolver os recortes de schema bloqueados por Q4/Q6–Q9/Q12/Q18 antes de executá-los.
- [ ] Gerar model, enum, factory, seeder e migration somente na futura etapa de implementação.
- [ ] Preservar obrigatoriedade dos campos, tipos pedidos e unicidade de RQ-02–RQ-06/RQ-16.
- [ ] Impedir edição de atributos técnicos pelo formulário.

Não existem novos arquivos PHP ou migration desta feature.

## 3. Aplicar Policy e matriz de permissões

- [ ] Resolver persona, painel, alcance e acumulação de Q3/Q4/Q13–Q16.
- [ ] Implementar Policy completa e recortar apenas permissões de Cupom na matriz.
- [ ] Impedir escrita comum sem remover a permissão determinada de listar.
- [ ] Gerar Shield e resemear papéis na ordem prevista, conferindo eventual sobrescrita de Policy.

Somente planejamento; nenhuma permissão foi concedida.

## 4. Construir Resources, formulário e listagens

- [ ] Definir localização e visibilidade antes de gerar os Resources candidatos.
- [ ] Preservar obrigações determinadas de RQ-01–RQ-10/RQ-16.
- [ ] Resolver Q5 para a listagem ativa. **Bloqueado por**: RQ-19 (aberta — Q5).
- [ ] Aplicar validação, autorização e tratamento de erro no servidor.
- [ ] Completar inventário real da superfície Livewire quando houver vendor e código.
- [ ] Cumprir contrato de exclusão/histórico após Q12/Q18.

Não existe implementação de listagem que antecipe a resposta sobre ativo.

## 5. Resolver dependência de aplicação real no pedido

- [ ] Receber decisão de escopo do solicitante e registrá-la como Adendo literal.
- [ ] Detalhar o contrato real de pedido e os passos dependentes somente após a resposta.
- [ ] Manter validação, desconto, consumo e trilha no escopo; não substituir por cálculo isolado.
- [ ] Definir persistência de ator/momento e fechamento consistente da operação quando o contrato existir.

**Bloqueado por**: RQ-11 (aberta — Q2), RQ-12 (aberta — Q2), RQ-13 (aberta — Q2), RQ-14 (aberta — Q2), RQ-15 (aberta — Q2), RQ-17 (aberta — Q2), RQ-18 (aberta — Q2).

Cadastro/listagem parciais não concluem o card.

## Testes

Não preenchido: derivação de CT/CT-B pertence ao step 7, fora desta invocação. Nenhum teste foi criado, modificado ou executado.

## Tickets

Não avaliado: step 8 não executado. Nenhum ticket, índice global ou arquivo de fatiamento foi criado.

## Verificação Final

Itens futuros, sem fechamento antecipado:

- [ ] Concluir revisões e derivação nas etapas previstas, com respostas materiais registradas.
- [ ] Restaurar ambiente executável e registrar baseline real antes do primeiro commit.
- [ ] Rodar testes afetados e regressão das permissões compartilhadas.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` quando houver edição de PHP.
- [ ] Executar browser em série, somente se a derivação confirmar sua necessidade.
- [ ] Medir queries/requests reais; não usar estimativa como evidência de custo.
- [ ] Executar revisão independente do diff, reconciliação, scripts e quality gate nas etapas próprias.
- [ ] Provar o fluxo de aplicação/auditoria quando Q2 e demais recortes permitirem sua implementação.

Não foram rodados scripts dos steps 5–12. Não há evidência de cobertura, score de mutação, baseline, QA, commit ou PR.

## Revisão do Diff (step 9)

Não executada; fora do limite solicitado. Não há diff Git disponível nesta cópia.

## Conformidade com Rules

Sem avaliação de diff ou veredito de conformidade nesta rodada. Foram lidos no contexto de pesquisa: índice, filament.md, testes.md e testes-browser.md; busca textual por cupom/coupon/pedido/order/admin/audit/log/wiki/desconto. O índice não aponta regra específica para a pasta desta wiki. A regra de autenticação não corresponde a arquivos previstos no plano.

A leitura não equivale à execução da conferência do step 10. Nenhuma rule foi criada ou alterada.

## Quality Gate

Não executado; step 11 fora do limite. Nenhum relatório 06 nem veredito de QA foi produzido.

## Candidatos a Rule

Não avaliado; step 12 fora do limite. Nenhuma invocação de requirement-to-rule ou gravação de rule.

## Auditoria Pré-Implementação

Entendimento confirmado: **pendente quanto às lacunas de requisito** — 2026-10-20 — a instrução existente autoriza exclusivamente planejar os steps 0–4; não confirma recomendações nem autoriza implementar. Rodada documentada: 1; perguntas formuladas: 0 de fato ao desenvolvedor, 1 de desenho ao desenvolvedor e 17 de requisito ao solicitante.

O desenvolvedor e o solicitante estão indisponíveis por instrução do usuário. Não foram feitas chamadas de solicitação de resposta nem contato com terceiros. A pergunta ao desenvolvedor será apresentada no retorno; as perguntas ao solicitante estão no 00. Perguntas dependentes permanecem em fila, sem simular rodadas respondidas.

### Pergunta ao desenvolvedor — raia desenho

```text
❓ Q1 · raia: desenho · afeta: — · depende de: —
Quer gerar o roteiro de teste manual (`08`) depois da implementação?
➡️ Recomendação: sim — RQ-01 pede cadastro no painel; há superfície de UI a conferir.
```

Roteiro manual: não — 2026-10-20 — sem resposta a Q1 — sinal de UI em RQ-01; ausência de resposta encerra a decisão provisória, sem bloquear o entendimento ou gerar 08 nesta etapa.

Essa pergunta é de meta-processo, isenta do filtro de oráculo, e existe somente aqui. Não houve outra escolha material de desenho que justificasse pergunta ao desenvolvedor. Escolhas rotineiras constam do 01.

### Fronteira e falta de resposta

- Q2–Q8, Q12 e Q17 não dependem de outra resposta; são a fronteira de requisito registrada.
- Q9–Q11, Q13–Q16 e Q18 dependem de Q2 ou Q3; permanecem em fila para uma rodada posterior.
- Nenhuma recomendação foi promovida a requisito fechado.
- P-01 registra a premissa mais estreita: não criar pedidos nem um motor substituto; as obrigações dependentes continuam abertas.
- RQ-11–RQ-15/RQ-17/RQ-18 estão abertas por Q2. RQ-19 está aberta por Q5. Os demais requisitos preservam suas obrigações determinadas e têm somente os recortes ambíguos bloqueados.
- Respostas posteriores do solicitante devem entrar como Adendo com fonte e texto literal; não reescrever o card.
- O sinal de mais de 30 perguntas de requisito não foi cruzado; nenhum step de fatiamento foi executado.
- O entendimento funcional das lacunas não está confirmado. A indisponibilidade não foi tratada como aprovação. O pedido determina a parada antes do step 5, independentemente de Q1.

### Conferências determinísticas do step 4

A captura literal foi mantida; permissões de criar, editar e excluir são cláusulas separadas. Listar e restringir a ativos foram separados para não bloquear a permissão determinada de listar por uma definição ainda ausente.

Contagens produzidas por PowerShell, usando regex ancorada nas linhas das tabelas e títulos:

```text
(Get-Content 00-requisito.md -Raw) com regex (?m)^\| RQ-\d+ \|: 19
(Get-Content 00-requisito.md -Raw) com regex (?m)^\| ❓ Q\d+ \|: 17
Linhas RQ com estado aberta — Qn: 8
(Get-Content 01-plano-acao.md -Raw) com regex (?m)^### [1-5]\. : 5
```

A conferência de espelho e do texto original, restrita aos artefatos desta wiki, é preparação do step 4; não constitui revisão profunda nem auditoria dos steps posteriores.

Resultado da conferência final dos artefatos: comparação literal do bloco original com a captura do step 0 = true; títulos dos passos do 01 e do 03 idênticos = true; arquivos presentes somente 00, 01, 02 e 03; perguntas 17 no 00 e 1 ao desenvolvedor no 03; referências abertas 16. A leitura e contagem foram feitas por Get-Content, Get-ChildItem e regex em PowerShell, com comparação dos valores na sessão. Nenhum teste da aplicação foi carregado.

### Revisão profunda (step 5)

Não executada. Nenhuma varredura da classe irmã ou confronto pós-escrita foi apresentado como gate concluído.

### Auditoria Ponytail (step 6)

Não executada. A integração descreve uso futuro; não foi ativada auditoria para ultrapassar o limite.

## Despachos

Host Codex com ferramentas de execução e colaboração expostas. Contexto novo disponível; sem sandbox de leitura por path nem hooks Claude efetivos. Os contratos limitaram a leitura e proibiram escrita; os hashes detectam mudanças no conjunto observado, não provam ausência de leitura fora do contrato.

| # | Step | Agente / tarefa | Modelo | Não recebeu | Resultado | Custo | Auditoria do retorno |
|---|---|---|---|---|---|---|---|
| 1 | 3 | pesquisa_dominio — mapeamento amplo; fallback de Explore por colaboração disponível | Herdado da sessão; ID/esforço não expostos | Histórico da sessão, paths experimentais proibidos | Tabela de domínio, ausência de pedidos, matriz de papéis, traits e wikis de produção. | —, host não reportou tokens/duração do agente | Presença conferida; amostras diretas de form/table, gate e trait de auditoria. Hashes SHA-256 iguais antes/depois em app, config, database, routes e .ai/rules. Referência de linha run do seeder ajustada na elaboração para 45, conforme fonte direta. |
| 2 | 4 | pesquisa_dominio — continuação como construtor de rascunho 01/02, texto sem escrita | Herdado da sessão; ID/esforço não expostos | Paths experimentais proibidos | Rascunho recebido; sessão completou seções, logs, bloqueios e superfície; nenhum arquivo escrito pelo agente. | —, host não reportou tokens/duração do agente | Presença e escopo conferidos; preserva Q2 e separa auditoria CRUD/aplicação. Amostras apoiadas na pesquisa direta anterior; hashes do mesmo conjunto permaneceram iguais. Não é revisão independente. |
| — | 0–4 | Sem despacho — captura literal, decomposição, nome, entrevista, decisões e escrita final pela sessão | Família GPT-6; ID não exposto | — | Fontes preservadas; artefatos consolidados pela responsável pela entrevista. | — | Captura e decisões dependem da conversa; conferências mecânicas baratas em linha, inclusive contagens e espelho. |

Os despachos foram sequenciais porque o rascunho depende da pesquisa e do 00. Não houve escritores concorrentes. As consultas oficiais e leituras independentes da sessão ocorreram durante a pesquisa do agente.

## Blockers

- [ ] Domínio de pedidos ausente: Q2 ao solicitante; aplicação e auditoria integralmente bloqueadas.
- [ ] Significado de ativo: Q5; restrição de listagem bloqueada.
- [ ] Persona, painel e alcance: Q3/Q4 e casos mistos; não conceder escrita nem modificar gate global por hipótese.
- [ ] Contratos de código, validade, valor, usos e histórico: Q6–Q12/Q17/Q18; executar somente recortes determinados após continuação autorizada.
- [ ] Vendor e node_modules ausentes: APIs instaladas, runtime e testes não verificáveis nesta cópia; nenhuma instalação autorizada.
- [ ] Boost MCP indisponível: search-docs, database-schema e database-query não foram executados.
- [ ] Sem .git: base, histórico e baseline por branch não verificáveis.

## Desvios do Plano

Não há implementação que possa divergir do PRD. Desvios/degradações do procedimento desta invocação:

- **Ordem interna do step 4**: um rascunho do 02 foi salvo antes do 01. A consolidação final seguiu 01, 02 e 03, sem iniciar o step 5. O 00 e a entrevista precederam os rascunhos.
- **Branch**: usada saida-p1-bp por instrução explícita; não foi criado repositório.
- **Boost**: lista de ferramentas expostas não contém Boost/search-docs/schema/query. Fallback para fontes oficiais e inspeção estática de código/migrations, sem afirmar inspeção do banco real.
- **Dependências**: `composer show --direct --no-ansi` retornou `No dependencies installed. Try running composer install or update.` `Test-Path vendor` e `Test-Path node_modules` retornaram False. Versões são do lock, não da instalação.
- **Artisan**: tentativas read-only de model:show User e route:list falharam por vendor/autoload.php ausente. Nenhum make, seeder, migration ou teste foi executado.
- **Superfície Livewire**: dois greps nos paths futuros e quatro no vendor retornaram exit 2; inventário está planejado/degradado, nunca “limpo”. A documentação oficial não substitui verificação do vendor travado.
- **Baseline/testes**: não executados, por falta de ambiente e pelo escopo de planejamento com paths de teste proibidos. Não há falhas pré-existentes por nome que possam ser afirmadas.
- **Documentação externa**: URL inicial de TIA indisponível; corrigida para o link oficial /docs/tia. Documentação de Auditing consultada indisponível; APIs novas não especificadas como verificadas.
- **Glossário**: `Test-Path wikis/glossario.md` retornou False. Nenhum arquivo global criado, respeitando a escrita restrita; significados novos continuam perguntas, sem definição silenciosa.
- **Comunicação**: mantido Caveman vigente do host; não executado comando de plugin para alterar modo. Prosa da wiki não foi comprimida.
- **Referências posteriores**: não abertas referências exclusivas dos steps 5–12; não lidas outras skills, salvo a referência específica do browser exigida na pesquisa.

## Notas de Implementação

Nenhuma: implementação não iniciada.

## Referências Abertas

Cada entrada é arquivo efetivamente lido; nomes abaixo são relativos à respectiva skill.

- feature-wiki/references/hosts-e-subagentes.md — início, antes do despacho — 2026-10-20.
- feature-wiki/references/ponytail-caveman.md — início — 2026-10-20.
- feature-wiki/references/pesquisa-step-3.md — step 3 — 2026-10-20.
- feature-wiki/references/citacoes-de-codigo.md — steps 3/4, antes de citar — 2026-10-20.
- feature-wiki/references/roteamento-e-despacho.md — antes dos despachos dos steps 3/4 — 2026-10-20.
- feature-wiki/references/playwright-mcp.md — step 3 — 2026-10-20.
- feature-wiki/references/pest-5.md — step 3 — 2026-10-20.
- feature-test-design/references/pest-plugin-browser.md — step 3, antes de planejar eventual browser — 2026-10-20.
- feature-wiki/references/template-00-requisito.md — step 4, antes do 00 — 2026-10-20.
- feature-wiki/references/entrevista-tres-raias.md — step 4, antes da entrevista — 2026-10-20.
- feature-wiki/references/template-01-plano.md — step 4, antes do 01 — 2026-10-20.
- feature-wiki/references/template-02-adr.md — step 4, antes do 02 — 2026-10-20.
- feature-wiki/references/template-03-progresso.md — step 4, antes do 03 — 2026-10-20.
- feature-wiki/references/padrao-de-log.md — step 4, antes de especificar logs — 2026-10-20.
- feature-wiki/references/estrutura-criada.md — step 4, antes de decidir extras — 2026-10-20.
- feature-wiki/references/glossario.md — step 4, antes de decidir tratamento dos termos — 2026-10-20.

As referências do step 7 em diante não foram abertas porque a invocação termina no step 4. Nenhum arquivo 04/05/06/07/08 foi criado.

## Retrospectiva

- **Funcionou bem**: pesquisa confirmou ausência do domínio comercial e o risco de permissões automáticas antes de fixar desenho implementável.
- **Limites preservados**: card literal, decisões sem resposta explicitamente bloqueadas e nenhuma escrita fora da wiki.
- **Próximo ponto de retomada**: respostas materiais e complementação das lacunas de pesquisa; step 5 permanece não executado.

