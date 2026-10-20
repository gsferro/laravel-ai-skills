# Plano de Ação — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md`. Planejamento limitado aos steps 0–4; nada deste plano foi implementado.
> As recomendações abertas do `00` não são decisões aprovadas. Este PRD é executável somente nos recortes determinados.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma feature de cupons encontrada nas wikis de produção permitidas.
- **Motivo**: introduzir cadastro e regras de desconto solicitados pelo FERRO-812.
- **Toca infra compartilhada?**: sim, futuramente configuração de logging e seeder de permissões; possível impacto no gate global depende de Q4.
- **Regressão obrigatória**: acesso aos painéis, matriz de papéis e isolamento da organização. Referências de produção: `wikis/specs/main/perfil-e-acesso-ao-painel/`, `wikis/specs/main/admin-da-organizacao/` e `wikis/specs/feature/multi-tenancy/organizacoes/`.
- A ausência de pedidos não torna aplicação/auditoria dispensáveis. Elas permanecem bloqueadas, com P-01, e não recebem um motor isolado substituto.

## Cobertura do Requisito

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | Cadastro no painel | 2, 4, 5 | Recorte de painel depende de Q2. |
| RQ-02 | Código | 2, 4, 5 | Presença determinada; domínio textual depende de Q6. |
| RQ-03 | Porcentagem ou fixo | 2, 4, 5 | Lista fechada determinada pelo card. |
| RQ-04 | Valor | 2, 4, 5 | Faixas/precisão dependem de Q8. |
| RQ-05 | Validade | 2, 4, 5 | Semântica temporal depende de Q7. |
| RQ-06 | Limite de usos | 2, 4, 5 | Domínio numérico depende de Q8. |
| RQ-07 | Só admin cria | 3, 4, 5 | Mapeamento e exceção de superusuário dependem de Q3/Q4. |
| RQ-08 | Só admin edita | 3, 4, 5 | Q3/Q4 e recorte histórico Q12. |
| RQ-09 | Só admin exclui | 3, 4, 5 | Q3/Q4 e recorte histórico Q12. |
| RQ-10 | Demais usuários só listam | 3, 4, 5 | Não concede aplicação; Q2 e Q10 pendentes. |
| RQ-11 | Apenas ativos | — | **Bloqueado por**: RQ-11 (aberta — Q5); nenhum predicado ativo implementado por suposição. |
| RQ-12 | Validar existência na aplicação | — | **Bloqueado por**: RQ-12 (aberta — Q1). |
| RQ-13 | Validar validade na aplicação | — | **Bloqueado por**: RQ-13 (aberta — Q1); também Q7. |
| RQ-14 | Validar usos na aplicação | — | **Bloqueado por**: RQ-14 (aberta — Q1); também Q8. |
| RQ-15 | Descontar total do pedido | — | **Bloqueado por**: RQ-15 (aberta — Q1); também Q8–Q11. |
| RQ-16 | Incrementar contador | — | **Bloqueado por**: RQ-16 (aberta — Q1); também Q11. |
| RQ-17 | Código único | 2, 4, 5 | Repetição exata vedada; equivalência textual depende de Q6. |
| RQ-18 | Auditar autor da aplicação | — | **Bloqueado por**: RQ-18 (aberta — Q1); também Q10/Q12. |
| RQ-19 | Auditar instante da aplicação | — | **Bloqueado por**: RQ-19 (aberta — Q1); também Q12. |
| P-01 | Não inventar pedidos nem motor substituto | 5 | Controle de escopo; não satisfaz as RQ abertas. |

Passo 1 é infraestrutura de logs dos passos 3 e 4, portanto vinculado às mesmas RQ. A coluna “—” significa bloqueio, nunca dispensa de requisito nem “fora desta entrega” decidido unilateralmente.

## Objetivo

Planejar um cadastro de cupons com código único, dois tipos de desconto, valor, validade e limite de usos, acompanhado de autorização efetiva no servidor. Preservar o direito de consulta dos demais usuários e explicitar a definição pendente de ativo.

O card também exige aplicar descontos em pedidos e registrar autor/data de cada aplicação. O projeto não contém esse domínio. As obrigações permanecem visíveis e bloqueadas até resposta do solicitante sobre escopo e regras; não se promete a feature completa apenas com o cadastro.

## Contexto

O repositório oferece infraestrutura de três painéis, permissões, tenancy opcional e auditoria de alterações Eloquent. Não oferece carrinho, venda, pedido, total monetário, serviço de precificação ou integração de aplicação de cupom.

## Análise dos Arquivos Existentes

| Fato descoberto, sem pergunta ao desenvolvedor | Evidência |
|---|---|
| O superusuário passa antes das policies. Não basta escrever uma policy para restringi-lo a admin. | `app/Providers/KitServiceProvider.php:configureGates():86`; `app/Models/User.php:isMasterGlobal():116`. |
| Entrada no painel depende do painel do papel e de contexto global/tenant. Dar acesso ao /admin a panel_user violaria separação existente. | `app/Models/User.php:canAccessPanel():74`, `app/Models/User.php:temPapelDoPainel():110`. |
| admin recebe matriz /admin; admin_organizacao recebe toda matriz /app; panel_user recebe /app menos Users/Convites. Cupons sem recorte herdariam CRUD indevido. | `database/seeders/PapeisSeeder.php:run():45`, `database/seeders/PapeisSeeder.php:permissoesDeAdministracaoDoApp():117`. |
| A geração de permissões é por painel e preserva policies existentes. | `database/seeders/ShieldPermissionsSeeder.php:run():36`, `database/seeders/ShieldPermissionsSeeder.php:gerarPara():58`. |
| Resource pode usar Schema, form e tabela separados, com rotas index/create/edit. | `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:form():54`, `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:table():59`, `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:getPages():64`. |
| Domínio de negócio demonstra UUID e tenancy; não demonstra pedidos. | `app/Models/Projeto.php`; `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60`, `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`. |
| UUID é chave de rota, PK permanece inteira. | `app/Traits/TemUuid.php:uniqueIds():30`, `app/Traits/TemUuid.php:getRouteKeyName():35`. |
| Trait de tenancy não restringe consulta sem tenant corrente; precisa guarda adicional se Q2 aprovar fronteira por organização. | `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`. |
| Auditoria existente inclui somente fillable; não comprova consumo de cupom nem pedido associado. | `app/Traits/AuditsFillables.php:getAuditInclude():18`; `database/migrations/2026_08_12_164915_create_audits_table.php:up():12`. |
| Channels atuais são transversais e não há channel cupons-de-desconto nem trait de Logging. | `config/logging.php:'autenticacao':101`; buscas registradas no 03. |
| UserFactory não tem estado admin, apenas unverified; papel precisa atribuição explícita nos testes. | `database/factories/UserFactory.php:definition():25`, `database/factories/UserFactory.php:unverified():39`. |
| Tenancy default é desligada, não há prova do estado em runtime. | `config/kit.php:'enabled':59`; `config/permission.php:'teams':154`. |
| RefreshDatabase cobre Feature; há browser e TIA configurados. | `tests/Pest.php`, `tests/Pest.php:locally():126`, `tests/Pest.php:timeout():170`. |

Ausências foram verificadas por inventário e busca de declarações, não apenas nomes de arquivos. Rotas explícitas: `routes/web.php` contém a página inicial; `routes/api.php` não existe; painéis descobrem Resources. `routes/console.php` contém saúde, limpeza de log de autenticação e lembrete de convites; nenhuma rotina de cupons. Não há motivo determinado para novo scheduler, middleware global, observer, evento ou fila.

### Documentação e versões

`composer show --direct` retornou “No dependencies installed”. As versões abaixo são **resolvidas no lock**, não instalação comprovada: Laravel v13.25.0, Filament v5.7.6, Livewire v4.4.0, Pest v5.1.1, browser plugin v5.0.1, Boost v2.5.3, Shield 4.3.1, Spatie Permission 8.3.0 e Owen Auditing v14.0.6. PHP CLI disponível: 8.4.10. `package.json` declara Playwright ^1.62.1; não há node_modules/playwright.

Boost MCP não foi exposto: a descoberta por nomes/descrições não encontrou search-docs, database-schema ou database-query. Consultou-se documentação oficial como fallback, em 2026-10-20, sem afirmar execução de search-docs:

- [Laravel 13 — autorização](https://laravel.com/framework/docs/13.x/authorization): policy e Gate::before.
- [Laravel 13 — validação](https://laravel.com/framework/docs/13.x/validation): unique e ignore com registro confiável.
- [Laravel 13 — migrations](https://laravel.com/framework/docs/13.x/migrations): unique no banco.
- [Laravel 13 — transações](https://laravel.com/framework/docs/13.x/database) e [bloqueio pessimista](https://laravel.com/framework/docs/13.x/queries): alternativas de consistência para a integração futura, sem implementar pedido ausente.
- [Filament 5 — Resources](https://filamentphp.com/docs/5.x/resources/overview): form/table, autorização e páginas.
- [Criação](https://filamentphp.com/docs/5.x/resources/creating-records) e [edição](https://filamentphp.com/docs/5.x/resources/editing-records): hooks de persistência.
- [Filament 5 — testes de Resources](https://filamentphp.com/docs/5.x/testing/testing-resources): persistência por componente.
- [Livewire 4 — segurança](https://livewire.laravel.com/docs/4.x/security) e [testes](https://livewire.laravel.com/docs/4.x/testing): entradas não confiáveis e teste pelo core.
- [Pest — instalação](https://pestphp.com/docs/installation) e [filtros](https://pestphp.com/docs/filtering-tests): PHP 8.4+ e execução focal.

A página pública de [model setup do Auditing](https://laravel-auditing.com/guide/model-setup) identificou-se como v13, embora o lock seja v14. Não foi usada para inferir API v14. A proposta limita-se à trait já usada no projeto; sem vendor, sua compatibilidade continua não verificada.

## Decisões de Desenho

Nenhuma pergunta material de desenho foi encaminhada ao desenvolvedor. As escolhas abaixo seguem convenções existentes e não respondem requisitos por ele.

| # | Decisão | Pergunta | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Resource Filament nativo, Schema e tabela conforme os irmãos; não introduzir front-end ou pacote novo. | convenção existente; implantação nos painéis pendente de Q2 | difícil de reverter | sessão, 2026-10-20 |
| D2 | Cupom declara tabela cupons explicitamente e usa TemUuid para rotas. | convenção existente, RQ-01/RQ-02 | surpreendente | sessão, 2026-10-20 |
| D3 | Unicidade protegida por constraint no banco e validação na entrada; normalização só após Q6. | RQ-17 e documentação Laravel | surpreendente | sessão, 2026-10-20 |
| D4 | Evitar services genéricos, adapters de pedido, interfaces de dinheiro e entidades comerciais especulativas. | P-01 | difícil de reverter | sessão, 2026-10-20 |
| D5 | Testar gravação e autorização por componente com Livewire::test; não exigir plugin Pest Livewire adicional. | convenção/autorizações existentes; seleção final no step 7 | difícil de reverter | sessão, 2026-10-20 |
| D6 | Contador, identidade do ator, tenant e instante oficial são dados de servidor, nunca campos editáveis pelo navegador. | RQ-06/RQ-07 e obrigações bloqueadas RQ-16/RQ-18/RQ-19 | surpreendente | sessão, 2026-10-20 |
| D7 | Reutilizar auditoria de cadastro existente; ela não substitui registro semântico de aplicação. Estrutura desse registro será decidida após Q1/Q12. | convenção existente; nenhuma decisão de armazenamento de aplicação tomada | difícil de reverter, pois ainda não há decisão de aplicação | sessão, 2026-10-20 |
| D8 | Logging manual no channel próprio, com allowlist segura; não criar trait genérica. | padrão da skill e logging existente | difícil de reverter | sessão, 2026-10-20 |

Nenhum cache, evento ou job é necessário para o cadastro. Não foi escolhido implicitamente decimal versus centavos, timezone, arredondamento, política histórica ou exceção ao superusuário.

## Autorização

Criar futuramente `App\Policies\CupomPolicy`, com métodos tipados `viewAny(User $user): bool`, `view(User $user, Cupom $cupom): bool`, `create(User $user): bool`, `update(User $user, Cupom $cupom): bool`, `delete(User $user, Cupom $cupom): bool`. Não habilitar bulk delete, exportação, replicação, restore nem edição inline automaticamente.

Preservar as proibições de CRUD por não admins. O mapeamento concreto de papéis e contexto é **recorte bloqueado por Q2/Q3/Q4**. Não copiar policy baseada apenas em permission e presumir que implementa “só admin”. O Gate::before existente pode antecipar a policy. Não alterar esse gate nem enfraquecer as demais features sem fechar Q4.

Acesso à listagem não exige dar /admin aos usuários comuns. Filtro de dados deve residir na query central do Resource, alcançando URL direta, busca e ações, não apenas a tabela visível. Em tenancy, exigir contexto e posse; a trait sozinha falha aberta sem tenant. Usar guard web e middleware atual do painel; nenhuma rota pública.

## Rotas

Todas as linhas abaixo são **propostas bloqueadas por Q2**, não rotas registradas ou URLs confirmadas. Se Q2 escolher outra superfície, substituir a proposta antes de implementar.

| Método | URI proposta | Name proposto | Middleware |
|--------|--------------|---------------|------------|
| GET | /admin/cupons | filament.admin.resources.cupons.index | stack autenticada do painel admin; CupomPolicy |
| GET | /admin/cupons/create | filament.admin.resources.cupons.create | idem; create |
| GET | /admin/cupons/{record}/edit | filament.admin.resources.cupons.edit | idem; update e route key UUID |
| GET | /app/cupons, ou /app/{tenant}/cupons com tenancy | filament.app.resources.cupons.index | stack autenticada atual do app; viewAny e fronteira confirmada |

Persistência ocorre pelos requests Livewire do framework, com autorização reavaliada em cada ação. Não criar endpoint de aplicação de cupom ou rota de pedidos. Nomes de rota deverão ser conferidos com route:list quando o app puder iniciar; não há URL compartilhável nesta etapa.

## Superfície de UI

| Tela / Componente proposto | Tipo | Rota proposta | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| ListCupons de gestão | Filament | /admin/cupons | Listar, abrir criação/edição, excluir conforme papel; recorte Q2/Q3/Q4/Q12 pendente | Sim |
| CreateCupom | Filament | /admin/cupons/create | Preencher os campos exigidos e salvar; limites Q6–Q8 pendentes | Sim |
| EditCupom | Filament | /admin/cupons/{record}/edit | Editar e salvar; nunca editar contador; recorte histórico Q12 pendente | Sim |
| ListCupons de consulta | Filament | /app[/tenant]/cupons | Somente listar; predicado ativo ainda não definido, Q5 | Sim |

Esta tabela não autoriza concretizar rotas pendentes. Não há UI de pedidos a desenhar. O step 7 deve derivar casos de gravação por componente para cada create/edit, além de autorização real e consulta. JS na infraestrutura não obriga CT-B: browser somente para asserções exclusivas de navegador. Não definir CT, CT-B ou locators nesta etapa.

**Bloqueado por**: RQ-11 (aberta — Q5), somente no recorte do predicado ativo. O restante do cadastro segue determinado, mas a tela de consulta não será entregue sem resolver esse filtro.

## Variáveis de Ambiente

Nenhuma chave nova determinada. Não alterar KIT_TENANCY, APP_URL ou configurações de banco. O channel proposto usa debug localmente conforme padrão; redução após estabilização/merge é tarefa posterior.

## Eventos / Listeners / Observers

Nenhum novo evento, listener ou observer. Reutilizar mecanismos Eloquent já presentes apenas para auditoria de cadastro, após compatibilidade confirmada. Não usar observer de contador como falsa prova de autor/pedido da aplicação.

## Jobs / Queues

Nenhum job, conexão, retry ou backoff novo. Cadastro e listagem são síncronos. Aplicação permanece bloqueada; não movê-la para fila por suposição.

## Modelo de Execução

| Pergunta | Resposta proposta para cadastro |
|---|---|
| Quantos requests? | Um GET inicial; cada interação Livewire necessária adiciona um request. Sem widgets, polling ou carregamento adiado novos. |
| O que é adiado? | Nada. Não adicionar deferLoading. |
| O que é memoizado por request? | Nenhum cache customizado. |
| O que é cacheado entre requests? | Nada novo; respeitar cache de permissões do pacote e invalidá-lo pelo seeder existente. |
| Custo do caminho principal | Tabela paginada, sem consulta por registro; medir contagem, consulta da página e consultas de autorização. Valor exato não medido. |
| Custo filtrado | Mesmo número de consultas em ordem de grandeza, com parâmetros vinculados e índice compatível com o predicado definido; medir com N acima da página. |
| Escrita | Uma operação de cadastro, validação e auditoria existente. Quantidade de queries não medida. |
| Aplicação | Não existe caminho executável no projeto; custo/transação não declarados como fatos. |

## Impacto em Features Existentes

- Seeders e matriz de papéis: impedir que panel_user herde Create/Update/Delete de Cupom por descoberta automática.
- Dois Resources do mesmo model podem compartilhar nomes de permissions. Recortar ações explicitamente por entidade/ação; não usar substring nem retirar ViewAny junto de CRUD.
- Se Q4 exigir mudança no gate, revisar regressão das features de acesso ao painel; não aplicar mudança global nesta sessão.
- Tenancy: não usar falta de tenant como autorização global nem alterar trait compartilhada sem necessidade.
- Auditoria: cadastro auditado não demonstra RQ-18/RQ-19; não modificar esquema audits para encaixar pedido inexistente.
- Nenhuma alteração autorizada agora em config, seeders, app ou testes.

## Rollback

Planejar rollback reversível do cadastro antes do uso em produção. O down da migration de cupons removeria tabela e dados; nunca executá-lo em banco com histórico a preservar sem backup e decisão de retenção. Reverter Resources e recortes do seeder em conjunto. Não introduzir feature flag ou pacote para este card. Rollback de aplicações monetárias depende do domínio de pedidos e de Q11/Q12; não existe operação de estorno definida.

## Dependências

Não adicionar nem atualizar dependências. Vendor e node_modules ausentes impedem execução; restauração do ambiente é pré-condição de outra sessão e está fora da escrita autorizada aqui. Versões de referência constam acima. Browser plugin já está declarado e no lock: não propor instalação duplicada. Páginas do Filament podem ser testadas pelo core Livewire sem adicionar pest-plugin-livewire.

## Riscos

- Entregar só cadastro como se o card estivesse completo: cobertura mantém aplicação/auditoria bloqueadas.
- Confundir admin global, admin de organização e superusuário: Q3/Q4, com guarda no servidor.
- Contagem de usos concorrente e efeitos parciais: quando Q1 liberar aplicação, desenho terá de garantir total, contador e registro de aplicação consistentes, com transação e controle concorrente verificados no banco real. Não há prova disso em SQLite de teste.
- Repetição de requisição consumir duas vezes: Q11 precisa fechar comportamento antes do desenho da integração.
- Instante, moeda, precisão, normalização e histórico escolhidos silenciosamente: Q6–Q12 permanecem propostas.
- APIs do vendor, schema vivo e rotas não verificados: concluir essas leituras antes de executar qualquer passo de código.
- Sem baseline: não há suíte verde comprovada nem falhas pré-existentes identificadas.

## Channel de Log da Feature

Busca em config/logging.php e app não encontrou cupons-de-desconto; busca por trait.*Logging não encontrou trait reutilizável. Criar futuramente channel daily próprio, com path storage/logs/cupons-de-desconto.log, level debug, retenção de 14 dias e replace_placeholders habilitado. Reutilizar estrutura do channel autenticacao.

Todo ponto de lógica usa `Log::channel('cupons-de-desconto')`, mensagens em português com `[Classe@Método]`, pipe e contexto permitido. Allowlist: cupom_id, usuario_id, operation, result, reason, error_code, exception_type e nomes seguros de campos alterados. Sem código digitado, e-mail, nome, IP, formulário, atributos completos ou mensagem/trace bruto de exceção. Logger operacional não substitui histórico de aplicação.

## Estrutura de Implementação

Os cinco passos abaixo são uma proposta futura, não autorização de execução. Requisitos abertos não têm implementação escondida. Nenhum passo cria pedido, aplica desconto, incrementa usos ou registra aplicação.

### 1. Preparar channel de logs

> Skills na implementação: ponytail; guidelines Laravel disponíveis no host. Nenhuma ativada agora para editar código.

- **Atende**: RQ-01, RQ-07, RQ-08, RQ-09, RQ-10, RQ-17, como infraestrutura dos passos 3/4.
- **Path a modificar**: `config/logging.php`.
- Adicionar somente o channel descrito acima, sem mudar defaults.
- Não há execução de domínio neste passo; nenhum log adicional apenas por carregar configuração. Verificar resolução do channel com teste apropriado ao ambiente, sem script/tinker novo.

### 2. Modelar cadastro mínimo e unicidade

> Skills na implementação: ponytail; orientação Eloquent/Laravel do projeto, se disponível.

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-17.
- **Paths futuros**: `app/Models/Cupom.php`, `app/Enums/TipoCupom.php`, `database/migrations/{timestamp}_create_cupons_table.php`, `database/factories/CupomFactory.php`, `database/seeders/CupomSeeder.php`.
- Usar make:model com factory/seeder e make:enum após consultar list/help do Artisan disponível; passar --no-interaction. Timestamp final é fornecido pelo gerador, não arquivo já existente.
- `Cupom extends Model`, `protected $table = 'cupons'`, TemUuid, factory e auditoria restrita ao cadastro como os irmãos. Não tratar cupom usado como modificável até Q12.
- `TipoCupom: string`, casos TitleCase `Porcentagem` e `ValorFixo`, valores internos `porcentagem` e `valor_fixo`; rótulos em português. Não armazenar valor de enum desconhecido.
- Colunas determinadas: id bigint autoincrement, uuid único não nulo, tipo não nulo com cast de enum, timestamps. Os demais campos existem no contrato, mas os detalhes abaixo são propostas pendentes.
- Código: string não nula + índice unique; largura e collation/equivalência dependem de Q6. Não reduzir unicidade a uma validação de formulário.
- Valor: decimal exato ou unidades monetárias inteiras; escolha física somente após precisão/moeda serem definidas em Q8/Q9. Não criar coluna float.
- Validade: coluna não nula, date ou timestamp segundo Q7. Não escolher conversão de fim de dia implicitamente.
- Limite: inteiro não nulo; largura/teto e semântica de zero dependem de Q8. Contador técnico de usos, se criado para preparar schema, é inteiro não nulo com zero inicial, fora do fillable e sem qualquer rotina de incremento neste recorte.
- tenant_id e seus índices dependem de Q2; se adotado, fora do fillable, nunca preencher com entrada do cliente. Inspecionar schema real antes da migration.
- Factory: dados coerentes com respostas; seeder não cria cupom real utilizável por padrão nem é ligado ao DatabaseSeeder automaticamente. Não usar factory em seeder de produção.
- **Recortes bloqueados**: Q2, Q6, Q7, Q8 e, para representação monetária aplicada ao pedido, Q9. Não executar migration parcial nem preencher esses contratos com defaults inventados.
- **Logs**: model/enum/schema sem método de operação novo; instrumentar as escritas nos pontos do passo 4. Não criar observer só para duplicar logs.

### 3. Proteger operações e ajustar permissões

> Skills na implementação: ponytail; orientação de autorização do projeto.

- **Atende**: RQ-07, RQ-08, RQ-09, RQ-10.
- **Paths futuros**: `app/Policies/CupomPolicy.php`, `database/seeders/PapeisSeeder.php`. `app/Providers/KitServiceProvider.php` é somente ponto de análise até Q4, não alteração decidida.
- Criar policy com assinaturas da seção Autorização, via make:policy e --no-interaction.
- Ajustar atribuição de permissions de Cupom por ação; preservar ViewAny de consulta e negar operações de escrita a não admins, inclusive chamada direta sem botão.
- Após registrar Resource, rodar ShieldPermissionsSeeder e depois PapeisSeeder, ambos --no-interaction, somente no ambiente próprio de implementação. Conferir policy após geração.
- **Recortes bloqueados**: Q2/Q3/Q4 para painel, contexto e fronteira de papéis; Q10 não é autorização adicional embutida neste passo.
- **Logs de negação**, nos métodos create/update/delete quando a decisão for realmente da feature: warning `[CupomPolicy@create] Criação de cupom negada | usuario_id: {id}`, correspondentes `@update` e `@delete`; contexto usuario_id, cupom_id quando existente, reason=not_authorized, result=denied.
- No fluxo permitido, debug `[CupomPolicy@create] Autorização de criação avaliada | usuario_id: {id}`, e equivalentes update/delete, contexto operation/result; sucesso da gravação é registrado no passo 4, não antecipado pela policy.
- Falta de identidade ou contexto fecha acesso; não aceitar papel ou tenant fornecido pelo formulário. O ponto correto de guarda precisa respeitar a resposta a Q4, pois um before global não chama policy.

### 4. Construir cadastro e consulta nos painéis definidos

> Skills na implementação: ponytail; orientação Filament/Livewire pertinente instalada no projeto.

- **Atende**: RQ-01–RQ-10 e RQ-17. Não implementa RQ-11 até Q5.
- **Paths propostos, condicionados a Q2**: `app/Filament/Admin/Resources/Cupons/CupomResource.php`; `Schemas/CupomForm.php`, `Tables/CuponsTable.php` e `Pages/ListCupons.php`, `Pages/CreateCupom.php`, `Pages/EditCupom.php` dentro desse Resource.
- Consulta proposta: `app/Filament/App/Resources/Cupons/CupomResource.php` e `app/Filament/App/Resources/Cupons/Pages/ListCupons.php`. Não duplicar formulário de escrita para usuários de consulta. Painel definitivo só depois de Q2.
- `form(Schema $schema): Schema` e `table(Table $table): Table` delegam configure tipado como AgenteIaResource. Rotas registradas por `getPages(): array`.
- Formulário contém código, tipo (lista fechada), valor, validade e limite; nunca contador, tenant ou autor. Validações reais do servidor e do formulário equivalentes, de acordo com Q6–Q8.
- Repetição de código: validar na criação e atualização ignorando somente o model resolvido pelo servidor; tratar violação concorrente da constraint como erro de validação seguro, sem exibir SQL.
- Query central restringe visibilidade para não admin conforme respostas; não aceitar parâmetro do cliente que remova restrição. Sem detalhes/edit/export por URL ou action para usuário de consulta.
- `CreateCupom extends CreateRecord` e `EditCupom extends EditRecord`; hooks protegidos afterCreate(): void e afterSave(): void conforme irmãos, sem transformar hook em método público. Usar DeleteAction somente no recorte autorizado de exclusão.
- **Recortes bloqueados**: Q2–Q4, Q6–Q8 e Q12. **Bloqueado por**: RQ-11 (aberta — Q5), no predicado de ativos; não há código planejado desse predicado antes da resposta.
- **Logs**: debug no início de tentativa, info após gravação/exclusão confirmada, warning para validação/negação esperada, error para falha interrompida; não logar sucesso se transação não tiver sido efetivada.
- Mensagens completas propostas: `[CreateCupom@beforeCreate] Iniciando cadastro de cupom | usuario_id: {id}`; `[CreateCupom@afterCreate] Cupom criado | cupom_id: {id}`; `[EditCupom@beforeSave] Iniciando edição de cupom | cupom_id: {id}`; `[EditCupom@afterSave] Cupom atualizado | cupom_id: {id}`.
- Exclusão no callback protegido da action: info `[EditCupom@excluir] Cupom excluído | cupom_id: {id}`; falha esperada warning `[EditCupom@excluir] Exclusão de cupom recusada | cupom_id: {id}`; contexto somente cupom_id, usuario_id, operation, result, reason.
- Validação: warning `[CreateCupom@validar] Cadastro de cupom recusado | usuario_id: {id}`, razão segura e nomes de campos, sem valores. Exceção que interrompe: error `[CreateCupom@gravar] Falha ao cadastrar cupom | usuario_id: {id}`, exception_type e error_code=coupon_write_failed; correspondentes para edição.
- Consulta: debug `[ListCupons@consultar] Consulta de cupons autorizada | usuario_id: {id}`; falta de contexto, se aplicável: warning `[ListCupons@consultar] Consulta de cupons recusada | usuario_id: {id}`, reason=missing_context. Não criar método público consultar apenas para logging; instrumentar hook/query protegido confirmado no vendor.
- Os rótulos @validar/@gravar/@excluir identificam o ponto lógico proposto; não são APIs do Filament. Na implementação, ajustar prefixo ao método real confirmado no vendor. APIs de lifecycle não inspecionadas ficam pendentes, não assinaturas inventadas.

### 5. Verificar cadastro, autorização e limites do escopo

> Skills posteriores: feature-test-design no step 7; ponytail na implementação; gates posteriores somente em nova execução autorizada.

- **Atende**: RQ-01–RQ-10, RQ-17 e P-01.
- **Paths futuros dos testes**: `tests/Feature/CuponsDeDesconto/`; nomes e CT serão definidos no step 7, sem criar testes agora. Regressão utiliza arquivos pertinentes já existentes em `tests/Kit/` e `tests/Tenancy/`.
- Usar UserFactory e atribuição de papéis real; actingAs antes dos componentes. Sem estado admin fictício.
- Gravação deve ser provada por componente e banco, não apenas GET. Usar record do model como parâmetro da edição e chamar save; não exigir redirect em edição.
- Cobrir autorização direta e recorte de dados conforme respostas. Repetição exata de código deve continuar barrada por constraint, mesmo se formulário for contornado.
- **Bloqueado por**: RQ-11 (aberta — Q5) apenas para comprovar filtro ativo; nenhum teste de aplicação das RQ-12–RQ-16/RQ-18/RQ-19 enquanto Q1 estiver aberta.
- Não declarar concluído o card com aplicação/auditoria pendentes. Não escrever teste que valide a recomendação no lugar da resposta.
- **Logs**: este passo somente verifica; não adicionar lógica, channel auxiliar ou helper de log sem uso.

## Integração de pedidos — lacuna bloqueada, sem passo executável

**Bloqueado por**: RQ-12 (aberta — Q1), RQ-13 (aberta — Q1), RQ-14 (aberta — Q1), RQ-15 (aberta — Q1), RQ-16 (aberta — Q1), RQ-18 (aberta — Q1), RQ-19 (aberta — Q1).

Não há migration de pedidos/aplicações, model, service, rota ou assinatura de aplicarCupom planejados como implementação aprovada. Após resposta a Q1 e às perguntas dependentes, criar Adendo, completar cobertura, decidir ligação pedido/cupom/ator/instante, precisão, autorização e idempotência, e só então derivar CT. Validar atomicidade/concorrência e vínculo da auditoria ao ato; mera alteração de contador não prova quem aplicou. Não escolher tabela própria, evento ou auditoria genérica como armazenamento definitivo antes dessa definição.

## Filosofia de Implementação

Executar futuramente com Ponytail, reutilizando recursos existentes e o mínimo de código que cumpra requisito. Não ativar nem executar auditoria do step 6 neste recorte. Prosa dos arquivos permanece completa; Caveman aplica-se à conversa conforme instrução ativa do host.

Antes do primeiro commit real, obter baseline completa em main em ambiente executável. Não há git nesta cópia; main é somente base nominal. Não usar --tia/--dirty como se houvesse histórico Git. Não instalar dependências, criar banco ou construir assets nesta sessão.

## Mapeamentos

| Campo de domínio | Destino proposto | Situação |
|---|---|---|
| código | cupons.codigo | obrigatório; equivalência e largura Q6 |
| tipo | cupons.tipo | Porcentagem / ValorFixo; valores internos descritos no passo 2 |
| valor do desconto | cupons.valor | obrigatório; representação/faixas Q8/Q9 |
| data de validade | cupons.validade_em | obrigatória; tipo físico e fuso Q7 |
| limite de usos | cupons.limite_usos | obrigatório; faixa/teto Q8 |
| contador técnico | cupons.usos | somente servidor; incremento bloqueado por Q1 |
| quem/quando aplicou | sem destino físico definido | RQ-18/RQ-19 abertas; não usar updated_at do cupom como substituto |

## Testes

A especificação será `04-casos-de-teste.md`, exclusivamente no step 7. Não existe nesta entrega. O `05-casos-de-teste-browser.md` só será criado se a costura browser for confirmada; nenhuma necessidade exclusiva de navegador foi decidida agora.

O projeto declara browser plugin e Playwright. Há manifest Vite existente, mas não foi reconstruído nem validado; a presença não comprova compatibilidade. tests/Pest.php configura timeout de 20.000 ms e RefreshDatabase. Para CT-B futuro, ler a referência do plugin na skill feature-test-design antes de planejar cenários. A regra local proíbe browser paralelo: não copiar --parallel --tia sobre toda suíte.

## Verificação Final

Itens para sessão futura, não executados nem marcados como aprovados:
- [ ] Restabelecer ambiente, confirmar versões instaladas, schema vivo, APIs e rotas, sem ignorar lacunas do step 3.
- [ ] Resolver perguntas materiais e registrar respostas do solicitante por Adendo.
- [ ] Executar steps 5 e 6 antes de derivar o 04 no step 7.
- [ ] Obter baseline em repositório real e anotar falhas pré-existentes por nome.
- [ ] Rodar testes focalizados com `php artisan test --compact tests/Feature/CuponsDeDesconto --no-tia`, após confirmar opções do runner.
- [ ] Rodar regressões de matriz de acesso e tenancy afetadas, com seleção por arquivo.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` após qualquer PHP modificado.
- [ ] Browser, somente se houver CT-B, em série e após npm run build, conforme regra local.
- [ ] TIA somente com Git e driver funcional, sem browser paralelo; suíte completa no CI sem TIA.
- [ ] Mutation testing pertinente pelo pestw.cmd no Windows, com duração e sobreviventes, sem afirmar resultado agora.
- [ ] Medir custo com N acima da página; cumprir gates 9–11 antes de declarar feature concluída.

## Commits

Somente quando houver repositório Git e execução autorizada:
- `:memo: cupons: documentar requisito e plano do FERRO-812`.
- `:sparkles: cupons: adicionar cadastro e consulta autorizados`, quando todos os recortes dessa entrega estiverem definidos e testados.
- Não há commit, branch real ou PR criados nesta cópia.

