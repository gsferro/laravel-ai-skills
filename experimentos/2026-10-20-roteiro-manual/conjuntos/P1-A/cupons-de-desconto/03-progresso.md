# Progresso — FERRO-812

**Estado**: em planejamento

- **Data**: 2026-10-20.
- **Wiki**: `wikis/specs/saida-p1-a/cupons-de-desconto/`.
- **Branch/pasta**: `saida-p1-a`, por instrução; `Test-Path .git` retornou `False`.
- **Base**: não disponível; `main` é somente a convenção da skill, não uma branch comprovada nesta cópia.
- **Limite desta execução**: steps 0, 1, 2, 3 e 4; parada antes do step 5. Não houve implementação, geração Artisan, config alterada ou teste criado.
- **Skill lida integralmente**: `.ai/skills/feature-wiki/SKILL.md`, `metadata.version: "4.1.1"`. Nenhum outro `SKILL.md` foi aberto. A referência de browser da feature-test-design foi lida por instrução, sem ativar o step 7 ou inferir a versão da skill dona a partir do cabeçalho da referência.

## 1. Configurar channel de log

- [ ] Adicionar channel `cupons-de-desconto` somente na futura implementação autorizada.
- [ ] Verificar configuração aditiva e instrumentação dos passos consumidores.

## 2. Modelar cadastro e unicidade de código

- [ ] Preservar campos e dois tipos determinados no requisito.
- [ ] Resolver recortes Q3/Q5/Q6/Q7/Q8/Q12 antes de fixar schema/validação dependentes.
- [ ] Criar model, enum, migration e factory somente depois das etapas e autorizações próprias.
- [ ] Garantir unicidade no banco e no servidor sem confiar apenas no formulário.

## 3. Proteger operações e ajustar permissões

- [ ] Mapear personas e contexto após Q2/Q3, preservando veto de manutenção aos demais usuários.
- [ ] Ajustar concessões do seeder sem eliminar listagem nem conceder aplicação implicitamente.
- [ ] Resolver Q4 para RQ-11 e rever superadministrador antes de afirmar proteção da policy.
- [ ] Executar geração de permissões na ordem ShieldPermissionsSeeder, PapeisSeeder e conferir matriz final.

## 4. Criar telas de cadastro e listagem

- [ ] Fixar paths e rotas do painel após respostas, sem gerar painéis paralelos por conveniência.
- [ ] Criar telas e validações de gravação por componente.
- [ ] Aplicar fronteira também a busca, resolução de registro e demais acessos.
- [ ] Não implementar filtro de ativos de RQ-11 enquanto Q4 estiver aberta.
- [ ] Instrumentar sucesso, negativa e falha sem copiar entrada sensível.

## 5. Integrar aplicação, consumo e auditoria ao pedido

- [ ] Resolver Q1 antes de criar qualquer integração, método de aplicação ou domínio substituto.
- [ ] Manter bloqueadas RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18 e RQ-19.
- [ ] Resolver regras de cálculo, ator, repetição, consumo e histórico e decidir proposta Q14.
- [ ] Implementar validação, desconto, contador e ator/instante na mesma unidade de sucesso.
- [ ] Provar concorrência e recuperação no ambiente e banco adequados; motor isolado não encerra o card.

## Testes

Não preenchida: step 7 não executado. Não existem `04`, `05`, IDs CT ou arquivos de teste desta feature. Leitura de exemplos de browser e da configuração não constitui cobertura. Nenhum arquivo de `tests/Feature/Exp*` foi lido ou executado.

Baseline não executada: sem vendor/autoload, sem repositório/base Git, e suíte completa poderia alcançar os testes proibidos. Não instalar dependências, executar essa suíte ou criar exceções nesta sessão. Não há falhas preexistentes por nome verificadas, nem resultado verde.

## Tickets

Não avaliado: step 8 fora do escopo autorizado. Não foram criados tickets, índice global ou proposta de fatiamento como se essa etapa tivesse ocorrido.

## Verificação Final

Verificações de implementação e reconciliação permanecem futuras. Nenhum item abaixo tem resultado aprovado nesta sessão.

- [ ] Concluir entrevista material, revisão profunda do step 5 e auditoria do step 6.
- [ ] Derivar e confirmar casos de teste somente no step 7.
- [ ] Restaurar ambiente em escopo autorizado e confirmar versões efetivamente instaladas, APIs e schema.
- [ ] Obter baseline reproduzível sem acessar caminhos proibidos nesta execução.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` quando houver edição de PHP.
- [ ] Rodar testes afetados, regressão de permissões e eventual browser conforme as costuras futuras.
- [ ] Conferir concorrência, precisão e falsificabilidade onde a pilha possa exibir o defeito.
- [ ] Medir consultas com N superior à página.
- [ ] Executar revisão independente do diff antes da reconciliação.
- [ ] Executar scripts de rastreabilidade, evidência, citações, IDs e conformidade na etapa própria.
- [ ] Reconciliar fontes e docs e executar quality gate antes de qualquer conclusão ou PR.
- [ ] Commit apenas em repositório real e sob escopo autorizado.

## Revisão do Diff (step 9)

Não executada. Sem implementação ou diff. Nenhum achado ou veredito de revisão foi inventado.

## Conformidade com Rules

Não avaliada sobre código: seção reservada à etapa própria. No step 3, foram lidos `.ai/rules/index.md`, `.ai/rules/filament.md`, `.ai/rules/testes.md` e `.ai/rules/testes-browser.md`, considerando os caminhos futuros e exemplos pesquisados. Busca temática `rg -n -i 'cupom|cupon|coupon|pedido|order|admin|monet|descont|audit' .ai/rules` executada. Não foi preciso entrar na área de autenticação; nenhuma alteração em tela de auth foi planejada.

## Quality Gate

Não executado: step 11 fora do escopo. Nenhum `06` foi criado; não há veredito e a feature não está concluída.

## Candidatos a Rule

Não coletados: step 12 fora do escopo. Não houve `record-rule`, alteração de `.ai/rules` ou memória externa.

## Auditoria Pré-Implementação

**Entendimento confirmado: não — 2026-10-20.** Desenvolvedor e solicitante indisponíveis por instrução. A autorização existente cobre somente planejamento até o step 4; não confirma respostas nem autoriza implementação. Não se usa a linha afirmativa do template para simular aceite.

### Registro da entrevista do step 4

Rodada 1 registrada e não concluída por ausência de respostas. Perguntas de fato ao desenvolvedor: nenhuma; foram resolvidas por busca/leitura, ou ficaram como limitações verificáveis. Pergunta de desenho ao desenvolvedor: Q14, com recomendação no `01`, sem resposta. Perguntas de requisito ao solicitante: Q1–Q13 no `00`, sem respostas; Q8/Q10/Q11 dependem de Q1 e Q13 depende de Q3/Q4, portanto sua rodada futura não foi iniciada. Contagens são conferidas por comando no fechamento documental desta sessão.

### Conferência documental do step 4

Em 2026-10-20, comando Python inline enviado por stdin (`@' ... '@ | python -`), sem criar script, comparou o bloco literal do card com `00`, extraiu linhas de cláusulas/cobertura com `re.findall(r'^\| (RQ-\d+) \|', texto, re.M)`, perguntas com `re.findall(r'^❓ (Q\d+) · raia: (\w+)', texto, re.M)` e títulos numerados de `01`/`03`. Também verificou o conjunto exato de arquivos, a ausência de checkbox concluído e de paths de código no `00`.

Saída: `verbatim: OK; arquivos: 00, 01, 02, 03; RQ: 19; cobertura: OK; perguntas_no_00: requisito 13, fato 0, desenho 0; perguntas_desenvolvedor: 1; espelho_passos: 5; checkboxes_concluidos: 0`. Exit 0. Esta conferência cobre os documentos recém-escritos; não revisa premissas contra código, não executa step 5 e não substitui teste da futura aplicação.

Não houve pergunta de nome: `cupons-de-desconto` é derivação direta do card, e `Test-Path wikis/specs/saida-p1-a/cupons-de-desconto` retornou `False` antes da criação. Não houve pergunta de branch: o desenvolvedor já forneceu `saida-p1-a`.

### Ausência de resposta: registros efetivos

- P-01 registra recorte mais estreito, sem criação silenciosa de pedido e sem declarar motor isolado como cumprimento da integração.
- RQ-11 fica `aberta — Q4`; aplicação e auditoria integrada ficam `aberta — Q1`, com cobertura e passos bloqueados no `01`.
- Partes determinadas das demais RQ continuam no plano: campos, tipos, código sem duplicata exata e proibição de manutenção a não admin. Parâmetros pendentes aparecem como recortes bloqueados, sem suspender toda a obrigação.
- Q14/D4 permanece proposta, sem ADR aceita, schema aprovado ou criação de `CupomUso`.
- Recomendações de validade, faixas, código, visibilidade e consumo não foram promovidas a regra.
- Nenhum Adendo foi criado: não houve resposta ou novo pedido do solicitante.

### Confronto código × afirmação (step 5)

Não executado. Os fatos acima pertencem à pesquisa inicial do step 3, não à revisão profunda do plano.

### Revisão profunda e classe irmã (step 5)

Não executadas por limite explícito. Não há alegação de plano validado contra todas as premissas ou de varredura de classe irmã concluída.

### Auditoria Ponytail (step 6)

Não executada. Nenhuma skill Ponytail foi aberta ou invocada. Implementação mínima foi descrita como orientação futura, sem apresentar a auditoria como realizada.

## Despachos

**Host**: Codex, ferramentas `functions.exec` e `collaboration` expostas. **Modelo informado na sessão**: GPT-6; identificador exato/variante e esforço não expostos. Subagentes herdaram modelo/esforço, sem aliases Claude. Ferramentas permitem contexto novo, mas estes despachos não exigiam julgamento cego; receberam histórico compartilhado. Não foi usado um perfil TOML como se tivesse sido carregado automaticamente.

**Controles**: contrato somente leitura, diretório explícito e exclusões explícitas de caminhos proibidos. Ambiente tem acesso amplo e não há hook/sandbox de leitura por path comprovado. Os agentes retornaram texto; a sessão escreveu os documentos. Não houve efeitos externos ou mensagens a terceiros.

| # | Step | Agente / tarefa | Modelo | Não recebeu | Resultado | Custo | Auditoria do retorno |
|---|---|---|---|---|---|---|---|
| 1 | 3 | `mapear_dominio` — mapeamento amplo; fallback de Explore por ferramenta `spawn_agent` | Herdado; GPT-6, variante não exposta | Nenhuma restrição de contexto por cegueira; proibidos caminhos `exp-*`/`Exp*` | Domínio de pedidos ausente, mapa de papéis/tenancy/auditoria e referências de produção | —, host não informou tokens/duração | Conferidos diretamente PapeisSeeder, configureGates e AuditsFillables, além da ausência estrutural. Agente declarou nenhuma escrita. Não se capturaram hashes antes do despacho; integridade por comparação antes/depois não foi provada. Limitação declarada, sem selo de auditoria independente. |
| 2 | 4 | Mesmo agente, rota construtor — rascunho textual do `01`/`02` | Herdado; GPT-6, variante não exposta | Sem cegueira exigida; mesmos caminhos proibidos | Estrutura de passos, paths condicionais e lacunas Livewire; sem novas perguntas | —, host não informou tokens/duração | Sessão confrontou rascunho com pacote de pesquisa/template ao redigir. Rejeitada qualquer leitura de “proposto” como “aprovado”; nenhuma decisão de requisito delegada. Sem hashes prévios; agente declarou nenhuma escrita. |

Dependência que forçou sequência: rascunho do step 4 precisava da pesquisa e da decomposição do requisito. Não havia duas tarefas disjuntas do mesmo step para executar em paralelo nesse despacho. Buscas e leituras independentes locais foram agrupadas quando possível.

**Sem despacho — motivo**: captura literal, decomposição e entrevista são responsabilidade da sessão; comandos determinísticos baratos rodaram localmente. Redação final de `00`–`03` ficou na sessão por forte interdependência de perguntas, bloqueios e rastreabilidade, após receber o rascunho do construtor. Não se apresentou essa atividade como revisão independente.

## Blockers

- [ ] Obter respostas de produto, especialmente domínio de pedidos, admin, fronteira e ativo.
- [ ] Resolver proposta de desenho Q14 sem inferir aprovação pelo silêncio.
- [ ] Confirmar ambiente de execução: `Test-Path vendor`, `Test-Path vendor/filament`, `Test-Path .env`, `Test-Path node_modules/playwright` retornaram `False`.
- [ ] Revalidar schema e APIs quando houver ambiente; `composer show --direct --no-interaction` informou dependências não instaladas, e Artisan falhou ao carregar `vendor/autoload.php`.

## Desvios do Plano

Não houve implementação; nenhum desvio de código para reconciliar. Limitações da execução do planejamento:

- Boost MCP indisponível: descoberta em `ALL_TOOLS` para nomes/descrições `boost|search_docs|database_schema|model.show` retornou `[]`. Usadas fontes oficiais e leitura estática, sem declarar `search-docs` ou `database-schema` executados.
- Vendor ausente: dois greps do código novo e quatro do vendor retornaram exit 2; resultados estão no `02`. Falha de ferramenta não foi contada como ausência de superfície.
- `composer.lock` informa versões travadas, não instaladas. Não se alterou dependência para satisfazer o ambiente.
- Git ausente: pasta de branch fornecida pelo desenvolvedor; não executados histórico, diff, commit, TIA ou comparação contra base inexistente.
- Glossário global ausente (`Test-Path wikis/glossario.md`: `False`). Não criado, pois o usuário proibiu escrita fora desta pasta. Termos ambíguos permanecem em Q2/Q3/Q4; nenhuma definição comercial nova foi assentada globalmente.
- Referência sugere Caveman ultra, mas a sessão recebeu modo caveman obrigatório. Mantida concisão na conversa; wiki escrita em prosa completa. Não foi invocado comando de plugin inexistente para simular mudança de modo.
- Cabeçalhos internos das referências dizem feature-wiki 4.0.0 e browser 1.16.0. Foram usados os arquivos empacotados com a skill lida, cujo metadata é 4.1.1; nenhum cabeçalho de referência foi tratado como metadata de outra skill.
- Linha afirmativa de entendimento do template não foi preenchida falsamente; ausência de confirmação está declarada acima.
- Hashes antes dos despachos não foram capturados; não se afirma prova de integridade ou isolamento por leitura.

Extras do step 4 avaliados: nenhum necessário para este cadastro nativo simples. Não há API externa, layout próprio significativo, migração destrutiva aprovada, batch ou fluxo assíncrono. Esquema de integração/histórico está bloqueado. Nenhum `05-*`, `04`, `06` ou ticket foi criado, e o glossário global foi preservado.

## Notas de Implementação

Nenhuma: implementação não iniciada. Os paths e assinaturas candidatos são propostas do plano, não novos arquivos de aplicação.

## Referências Abertas

Paths relativos a `.ai/skills/feature-wiki/references/`, salvo indicação. Foram abertas somente referências exigidas ou apontadas pelas etapas executadas; nenhuma pasta de referências foi carregada em bloco.

- `hosts-e-subagentes.md` — início/step 3 — 2026-10-20.
- `ponytail-caveman.md` — início — 2026-10-20.
- `pesquisa-step-3.md` — step 3 — 2026-10-20.
- `roteamento-e-despacho.md` — steps 3 e 4, antes dos despachos — 2026-10-20.
- `citacoes-de-codigo.md` — steps 3 e 4 — 2026-10-20.
- `glossario.md` — step 3 — 2026-10-20.
- `playwright-mcp.md` — step 3 — 2026-10-20.
- `pest-5.md` — step 3 — 2026-10-20.
- `.ai/skills/feature-test-design/references/pest-plugin-browser.md` — step 3, por referência explícita — 2026-10-20; não foi lido seu `SKILL.md`.
- `template-00-requisito.md` — step 4 — 2026-10-20.
- `entrevista-tres-raias.md` — step 4 — 2026-10-20.
- `template-01-plano.md` — step 4 — 2026-10-20; sessão e construtor.
- `template-02-adr.md` — step 4 — 2026-10-20; sessão e construtor.
- `template-03-progresso.md` — step 4 — 2026-10-20.
- `estrutura-criada.md` — step 4 — 2026-10-20.
- `padrao-de-log.md` — step 4 — 2026-10-20.

Não abertas: casos medidos, delegação de CT e referências de etapas posteriores; nenhum procedimento dependente delas foi executado.

## Retrospectiva

Não realizada como encerramento da feature; etapa futura. Nota desta sessão de planejamento: separar cadastro determinado, lacunas de comportamento e integração ausente impede transformar silêncio em aprovação. A wiki permanece em planejamento, com perguntas e limitações explícitas.
