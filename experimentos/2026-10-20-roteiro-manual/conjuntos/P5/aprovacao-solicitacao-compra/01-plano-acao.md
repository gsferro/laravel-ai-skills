# Plano de Ação — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: [00-requisito.md](00-requisito.md). Planejamento produzido somente até o step 4. Este documento não autoriza implementação.
> Perguntas abertas delimitam o que ainda não pode ser executado. Recomendações no requisito não são decisões aceitas.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma para compras. As wikis de organizações e administração da organização são contexto de infraestrutura, não fonte do comportamento deste card.
- **Motivo**: não existe domínio de compras, centro de custo ou roteamento de aprovadores no código consultado.
- **Toca infra compartilhada?**: sim, se implementada: channel em `config/logging.php`, descoberta de permissões e se necessário matriz em `database/seeders/PapeisSeeder.php`. Isso força regressão das permissões e do painel, mesmo sendo feature nova.
- **Limite atual**: persistência e contratos propostos; integração do centro de custo integralmente bloqueada. Nenhum cadastro faltante será criado por inferência.

## Cobertura do Requisito

Os logs do passo 1 são infraestrutura de todas as linhas abaixo; o passo 9 verifica essas mesmas obrigações, após derivação de testes no step 7. “Fechada” não remove bloqueios específicos de situações ainda indecididas.

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | Criar solicitação com descrição e valor. | 2, 5, 7 | Descrição e valor determinados; limites e normalização aguardam Q7 e Q9. |
| RQ-02 | Associar a solicitação a um centro de custo. | 3, 5, 7 | **Bloqueado por**: RQ-02 (aberta — Q1). |
| RQ-03 | Permitir ao solicitante editar sua solicitação enquanto estiver em rascunho. | 4, 5, 7 | Só o solicitante em rascunho; recortes de dados aguardam Q7/Q9. |
| RQ-04 | Permitir ao solicitante excluir sua solicitação enquanto estiver em rascunho. | 4, 5, 7 | Só o solicitante em rascunho; nenhuma exclusão em lote que contorne a guarda. |
| RQ-05 | Ao enviar, encaminhar ao gestor do centro de custo para aprovação. | 3, 6, 8 | **Bloqueado por**: RQ-05 (aberta — Q1). |
| RQ-06 | Exigir também aprovação do diretor quando o valor for acima de R$ 5.000. | 2, 4, 6, 8 | Comparação > 500000 centavos determinada; resolução de diretor depende de Q1; sobreposições Q3/Q4. |
| RQ-07 | Exigir que a aprovação do diretor ocorra depois da aprovação do gestor. | 2, 4, 6 | Ordem determinada; caso de pessoa acumulando etapas aguarda Q4. |
| RQ-08 | Permitir ao gestor aprovar a solicitação encaminhada. | 4, 6, 7 | Gestor da etapa, sem presumir autorização para autoaprovação (Q2). |
| RQ-09 | Permitir ao gestor rejeitar a solicitação encaminhada. | 4, 6, 7 | Rejeição do gestor determinada; rejeição do diretor é recorte não autorizado (Q10). |
| RQ-10 | Exigir justificativa na rejeição. | 5, 6, 7 | Obrigatoriedade determinada; teto e espaços aguardam Q8. |
| RQ-11 | Devolver a solicitação rejeitada ao estado de rascunho para correção pelo solicitante. | 2, 6, 7 | Retorno a rascunho determinado; histórico entre ciclos aguarda Q11. |
| RQ-12 | Permitir ao solicitante enviar novamente após rejeição e correção. | 3, 6, 7, 8 | Reenvio determinado; validade e apresentação de aprovações antigas aguardam Q11. |
| RQ-13 | Impedir alterações depois da aprovação final. | 2, 4, 5, 6, 7 | Imutabilidade final determinada; guardas são aplicadas também fora de UI. |
| RQ-14 | Permitir ao solicitante cancelar a qualquer momento antes da aprovação final. | 4, 6, 7 | Cancelamento pré-final determinado; reabertura pós-cancelamento aguarda Q14. |
| RQ-15 | Mostrar o status atual na tela. | 2, 7 | Status deve aparecer; recorte de quem consulta aguarda Q5. |
| RQ-16 | Mostrar quem aprovou cada etapa na tela. | 2, 7 | Aprovador de cada etapa deve aparecer; público e ciclos anteriores aguardam Q5/Q11. |
| RQ-17 | Notificar por e-mail o próximo aprovador. | 3, 6, 8 | Canal e próximo destinatário determinados; origem Q1; link Q6; substituição Q12; ausência Q13; obsolescência Q15; falha Q16. |

Nenhuma P-nn vigente. Nenhuma RQ foi marcada fora desta entrega para esconder a dependência dos cadastros ausentes.

## Objetivo

Permitir registrar uma solicitação, corrigi-la em rascunho e submetê-la à aprovação do gestor do centro de custo. Valores acima de R$ 5.000 seguem ao diretor somente depois da aprovação do gestor. Exibir o estado e os aprovadores, permitir rejeição justificada com retorno a rascunho e cancelamento pelo solicitante antes da aprovação final.

O plano preserva essas obrigações, mas não completa regras que o card omite. Fonte de centro de custo, associação de aprovadores, visibilidade e casos especiais precisam das respostas registradas no requisito.

## Contexto

O projeto é um kit com usuários, organizações, papéis, permissões e notificações. O painel `app` é o ponto de extensão de negócio. Não foram encontrados cadastros de centro de custo, gestor, diretor ou solicitação de compra. Isso é dependência de escopo (Q1), não autorização para criar um subsistema administrativo.

## Análise dos Arquivos Existentes

| Referência conferida | Fato e consequência |
|---|---|
| `app/Models/Projeto.php` | Molde de negócio com `TemUuid`, `BelongsToTenant` e `AuditsFillables`; não reutilizar a entidade de demonstração como solicitação. |
| `app/Traits/TemUuid.php:getRouteKeyName():35` | Rotas usam UUID; PK interna continua numérica. UUID não substitui autorização. |
| `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62` | Sem tenant corrente, a trait não filtra. Consultas e comandos fora do painel precisam contexto explícito. Não alterar a trait global para esta feature. |
| `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60` e `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72` | Form e tabela usam schema/componentes nativos. O exemplo usa modais; compras terá páginas de criação, edição e detalhe para acomodar estado e etapas. |
| `app/Filament/App/Resources/Users/UserResource.php:getEloquentQuery():121` | Exemplo local de recorte no Resource, incluindo binding e busca. Política de audiência de compras depende de Q5. |
| `app/Models/Convite.php:exigirDono():709` e `app/Models/Convite.php:recusar():670` | Identidade e estado são conferidos no domínio; atualização condicional evita reaplicar decisão. |
| `app/Notifications/ConviteDeAcesso.php:via():43` e `app/Notifications/ConviteDeAcesso.php:toMail():48` | Convenção de Notification enfileirável com canal mail. Criar mensagem própria de compras; não reutilizar tokens ou texto de convite. |
| `app/Providers/Filament/AppPanelProvider.php:panel():56` | Descoberta automática de Resources/Pages. Não precisa registrar nova classe em lista do provider. |
| `database/seeders/PapeisSeeder.php:run():45` | Matriz de permissões ampla para negócio; permissões geradas não bastam para ator e estado. Papel novo não nasce sem `painel`. |
| `database/seeders/ShieldPermissionsSeeder.php:run():36` | Regerar permissões antes de reaplicar papéis quando o Resource existir; conferir policies geradas para não perder guardas de negócio. |
| `tests/Pest.php:noPainelDa():225` | Helper de contexto para testes de componente. `Feature` e `Kit` usam RefreshDatabase; `Tenancy` usa TestCase próprio. |
| `database/factories/UserFactory.php:unverified():39` e `database/factories/TenantFactory.php:inativo():47` | Factories disponíveis. States de tenant também incluem identidade visual. Ainda não existem factory de compra ou de centro de custo. |
| `config/queue.php`, `config/mail.php`, `.env.example` | Defaults de fila database, after_commit=false e mailer log. SMTP e worker reais não foram confirmados. |

**Busca negativa reproduzida pela sessão**: `rg -n -i '\b(compra[s]?|solicita[cç][aã]o|solicita[cç][oõ]es|centro[s]?[_ ]?(de[_ ]?)?custo[s]?|cost[_ ]?cent(er|re)|purchase[s]?|procurement|aprovador(es)?|diretor(a|es)?|gestor(es)?)\b' app/Models app/Filament app/Policies database/migrations routes config` retornou saída vazia, exit 1. Busca ampla adicional devolve textos de IA sem entidade correspondente.

**Inventário de rotas/configuração**: `routes/web.php` contém somente a home; `routes/api.php` não existe. Bootstrap encaminha rotas web/console e health. Não há evento, observer ou agendamento de aprovação. `routes/console.php` agenda tarefas do kit e lembretes de convites; nenhuma alteração de scheduler é necessária para notificar o próximo aprovador. Não há dado externo/ID fornecido pelo usuário a validar contra o banco.

**Limitações verificadas**: `composer show --direct` respondeu “No dependencies installed”. `Test-Path vendor`, `node_modules`, `.env` e `database/database.sqlite` retornaram false. Schema real não foi inspecionado; as migrations são evidência estática, não prova do banco implantado. Artisan, model:show e baseline não iniciam sem autoload. Sem Boost MCP exposto, `search-docs` e `database-schema` foram substituídos por docs oficiais e leitura estática, com perda de verificação.

### Pesquisa de documentação

Consultas realizadas antes de escrever o PRD, em 2026-10-20. Fallback explícito, não consultas simuladas ao Boost:

- [Laravel 13: autorização](https://laravel.com/docs/13.x/authorization#policy-methods): policies por ação e autorização no servidor.
- [Laravel 13: transações](https://laravel.com/docs/13.x/database#database-transactions): agrupar persistência de uma transição.
- [Laravel 13: notificações](https://laravel.com/docs/13.x/notifications#queued-notifications-and-database-transactions): Notification com ShouldQueue e afterCommit.
- [Laravel 13: filas](https://laravel.com/docs/13.x/queues): operação de tentativas e backoff; limites técnicos abaixo são proposta de desenho.
- [Filament 5: Resources](https://filamentphp.com/docs/5.x/resources/overview#customizing-the-resource-eloquent-query): o recorte de getEloquentQuery alcança tabela, páginas e busca.
- [Filament 5: modais de ações](https://filamentphp.com/docs/5.x/actions/modals): schema de ação para justificativa.
- [Filament 5: testes de Resource](https://filamentphp.com/docs/5.x/testing/testing-resources): gravação por componente; cenários somente no step 7.
- [Livewire 4: segurança](https://livewire.laravel.com/docs/4.x/security): argumentos e propriedades públicas são entradas não confiáveis.
- [Pest 5](https://pestphp.com/docs/pest5-now-available) e [browser testing](https://pestphp.com/docs/browser-testing): confirmar stack e separar costuras antes de criar CT-B. A URL consultada `/docs/test-impact-analysis` não abriu; não atribuir a ela prova de TIA.

As versões são do lockfile, não de pacotes instalados. APIs herdadas do vendor continuam pendentes de inspeção quando o ambiente for restaurado. Não pressupor suporte confirmado a toda assinatura com base só na major.

## Decisões de Desenho

Nenhuma pergunta material de desenho precisou ser enviada ao desenvolvedor. As escolhas abaixo são rotineiras sob o pedido de planejamento e as convenções existentes. Questões sobre o que o usuário observa foram encaminhadas à raia requisito.

| # | Decisão | Pergunta | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Resource nativo no painel app; métodos de domínio no model, sem motor genérico de workflow. | autorização existente; RQ-01 a RQ-17 | surpreendente | sessão, 2026-10-20 |
| D2 | Dinheiro em centavos inteiros, comparação com 500000; parsing sem float. Não decide limites de negócio de Q9. | autorização existente; RQ-01/RQ-06 | surpreendente | sessão, 2026-10-20 |
| D3 | Persistir estados e identidades das etapas; transporte nunca aceita solicitante, aprovador ou status como campo editável. | convenções e RQ-08/RQ-13/RQ-16 | trade-off não trivial | sessão, 2026-10-20 |
| D4 | Notification nativa ShouldQueue, disparada após commit; sem evento/listener/Job próprio para duplicar o mesmo envio. Resultado em falha continua em Q16. | convenção de ConviteDeAcesso; RQ-17 | difícil de reverter | sessão, 2026-10-20 |
| D5 | Atualização condicional por versão/estado e transação curta para comandos; sucesso só após persistência. | convenção de Convite; RQ-07/RQ-13/RQ-14 | surpreendente | sessão, 2026-10-20 |
| D6 | Channel daily próprio, seguindo o padrão local. | convenção; infraestrutura das RQ | difícil de reverter | sessão, 2026-10-20 |
| D7 | Sem novos pacotes ou abstrações de permissão. Usa Livewire::test, disponível na stack, sem exigir pest-plugin-livewire. | convenções; infraestrutura das RQ | trade-off não trivial | sessão, 2026-10-20 |

Não há desenho aceito para origem dos centros de custo, histórico de tentativas, transferência de aprovador ou tratamento observável de falha de entrega. Esses assuntos dependem de requisito; não viram ADR aceita por falta de resposta.

## Autorização

- Criar `app/Policies/SolicitacaoCompraPolicy.php`: viewAny/view/create/update/delete e ações enviar/aprovar/rejeitar/cancelar. As ações combinam permissão do painel, identidade, contexto e estado.
- A barreira no model é obrigatória e independente de Gate::before ou perfil privilegiado: papéis amplos não autorizam alterar solicitação finalizada nem agir como outra pessoa.
- O público de consulta está bloqueado em Q5. Recortes de sobreposição de papéis dependem de Q2/Q3/Q4; não usar recomendações como regra implementada.
- Usar guard e middleware já aplicados ao painel app. Quando tenancy estiver habilitada, conferir organização tanto no Resource quanto no domínio. Fora do painel, carregar contexto explícito; a trait não fecha sozinha no nulo.
- Não ativar tenancy nesta feature. Modo efetivo não confirmado, pois não existe ambiente local. A integração precisa respeitar o modo real do kit, em single e em multi-tenancy.
- Sem API pública ou acesso anônimo ao registro.

## Rotas

Rotas propostas para o Resource; assinatura final e parâmetros de tenant devem ser confirmados por route:list após restauração do ambiente. Não há conflito estático identificado. Não compartilhar URL absoluta sem get-absolute-url.

| Método | URI relativa ao Resource | Name proposto | Middleware |
|---|---|---|---|
| GET | /solicitacoes-compra | filament.app.resources.solicitacoes-compra.index | grupo app autenticado, acesso ao painel e tenant quando ativo |
| GET | /solicitacoes-compra/create | filament.app.resources.solicitacoes-compra.create | mesmo grupo + create |
| GET | /solicitacoes-compra/{record} | filament.app.resources.solicitacoes-compra.view | mesmo grupo + view |
| GET | /solicitacoes-compra/{record}/edit | filament.app.resources.solicitacoes-compra.edit | mesmo grupo + update |
| POST | endpoint de atualização do Livewire já registrado | framework; não criar rota por decisão | middleware persistente do painel + autorização no comando |

Prefixo app e segmento de organização são gerados pelo painel; não concatenar URL. `record` usa UUID conforme TemUuid. Link de e-mail e destino no acesso obsoleto aguardam Q6.

## Superfície de UI

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| ListSolicitacoesCompra | Filament/ListRecords | index | Consultar descrição, valor, centro de custo e status; abrir detalhe. Audiência pendente Q5. | Sim |
| CreateSolicitacaoCompra | Filament/CreateRecord | create | Gravar rascunho com descrição, valor e centro de custo. Integração do centro bloqueada Q1. | Sim |
| EditSolicitacaoCompra | Filament/EditRecord | edit | Corrigir rascunho; exclusão e envio por ações autorizadas. | Sim |
| ViewSolicitacaoCompra | Filament/ViewRecord | view | Ver estado e aprovadores; aprovar, rejeitar com justificativa ou cancelar conforme ator/estado. | Sim |
| Modal de rejeição | Filament/Action schema | ação no detalhe | Informar justificativa obrigatória. Limites dependem Q8; diretor rejeitar depende Q10. | Sim |

Os nomes de páginas são propostas, não classes existentes. Usar componentes nativos, labels em pt-BR e datas no padrão do projeto. Não há motivo confirmado para dashboard, polling ou widget adicional.

O gate futuro do step 7 exige gravação por componente nas rotas create/edit. UI por si só não determina CT-B: formulário, gravação, ações e autorização cabem em componente. Somente asserção dependente de navegador autoriza criar arquivo de CT-B, com costura confirmada. Nenhum cenário ou seletor foi derivado nesta rodada.

## Variáveis de Ambiente

Não adicionar chave de feature. Reutilizar configuração existente:

| Key | Default do exemplo | Descrição |
|---|---|---|
| QUEUE_CONNECTION | database | Worker precisa processar notificações; testes usam sync. |
| MAIL_MAILER | log | Não entrega e-mail real; implantação precisa transporte real. |
| MAIL_HOST / MAIL_PORT / MAIL_USERNAME / MAIL_PASSWORD | 127.0.0.1 / 1025 / null / null | Infra de e-mail existente; não copiar segredos para wiki. |
| MAIL_FROM_ADDRESS / MAIL_FROM_NAME | hello@example.com / APP_NAME | Remetente já configurável. |
| KIT_TENANCY | false | Preservar modo existente; não ativar por editar .env. |
| LOG_LEVEL | debug | Channel próprio usa esse padrão enquanto em desenvolvimento. |

## Eventos / Listeners / Observers

Sem evento/listener/observer novo. Comandos do model acionam a notificação após commit. Não adaptar os listeners de IA, nem incluir aprovação no agendamento de lembrete de convite. Se Q16 exigir garantia durável diferente, revisar o desenho antes de codificar; não prometer entrega exatamente uma vez.

## Jobs / Queues

Notification própria `SolicitacaoCompraAguardandoAprovacao`, via mail, ShouldQueue + Queueable, afterCommit explícito porque a conexão existente usa after_commit=false. O Laravel cria o job de notificação; não criar wrapper próprio.

Proposta técnica: conexão padrão existente, fila default; timeout 30 s, até 3 tentativas e backoff 60/300 s, sempre timeout menor que retry_after (default 90 s). Confirmar propriedades suportadas no vendor restaurado. A falha final e eventual recuperação não podem ser implementadas sem Q16. Supressão de e-mail obsoleto aguarda Q15. Não registrar corpo de e-mail ou endereço no log.

## Modelo de Execução

| Pergunta | Resposta |
|---|---|
| Quantos requests a tela custa? | Um GET inicial; navegação e cada ação geram requests próprios. Quantidade exata do framework ainda não medida. |
| O que é adiado? | Somente entrega de e-mail após commit. Sem lazy widget, deferLoading ou polling planejados. |
| O que é memoizado por request? | Nenhum cache adicional proposto. Reutilizar relações carregadas durante renderização; não considerar isso cache entre ações. |
| O que é cacheado entre requests? | Nenhum cache de estado de aprovação ou autorização. Cada comando relê registro e contexto. |
| Custo principal | Lista paginada com relações carregadas em lote, evitando consulta por linha para solicitante/etapas. Uma transação curta por comando. Contagens de queries não medidas; medir com N acima da página antes de concluir. |

## Impacto em Features Existentes

Permissões de Resources novos podem chegar automaticamente a panel_user. Reaplicar seeders sem guardas próprias seria autorização excessiva. Mudança em logging e matriz exige regressão de Kit/Tenancy, especialmente administração da organização e acesso ao painel. Nenhuma alteração nos fluxos de convite está prevista; reutiliza-se somente o padrão de Notification.

## Rollback

Código ainda não existe. Ao implementar, permitir rollback de código e ocultação do Resource sem apagar solicitações. Migration down só em ambiente sem dados de negócio ou com restauração previamente preparada; não propor exclusão automática de histórico aprovado. Backups e recuperação dos dados precedem qualquer rollback destrutivo. Como Q1 e Q11 estão abertas, constraints e retenção definitivas não estão decididas.

## Dependências

`composer show --locked --direct` conferiu Laravel 13.25.0, Filament 5.7.6, Pest 5.1.1, plugin Laravel 5.0.1, browser 5.0.1, PHPUnit 13.3.0 e Boost 2.5.3. Lockfile também contém Livewire 4.4.0 e Spatie Permission 8.3.0. PHP CLI observado: 8.4.10. Package.json pede Playwright ^1.62.1; package-lock registra 1.62.1.

Não estão instalados localmente. Restaurar dependências e ambiente seria pré-requisito de uma sessão de implementação autorizada; esta sessão não instala nada e não altera dependências. Não planejar instalação adicional do browser plugin, pois já está declarado e travado; confirmar sua presença física após restore. Navegadores baixados não foram verificados. Manifest do Vite existe, mas não prova build atual. Baseline em main permanece pendente; não há .git nem autoload.

## Riscos

- Q1 impede concluir seleção do centro e roteamento; não criar substituto fictício.
- Q2–Q4 impedem decidir sobre acúmulo de funções; permissões genéricas não respondem ao caso.
- Q5/Q6 impedem liberar consulta e destino do e-mail sem ampliar visibilidade.
- Q7–Q9 impedem decidir novos limites; armazenamento proposto não os autoriza.
- Q10/Q11/Q14 impedem inventar rejeição pelo diretor, validade histórica e reabertura.
- Q12/Q13/Q15/Q16 impedem decidir substituição, aprovador ausente, mensagem obsoleta e resultado da falha de transporte.
- Não há schema real nem vendor: APIs herdadas, FKs, assinatura de formulários e concorrência no banco de produção precisam confirmação.
- SQLite em testes não prova bloqueio/conflito do banco de produção. Usar comando condicional por versão/estado e comprovar concorrência no banco efetivo antes de prometer atomicidade completa.
- SMTP oferece no máximo garantia compatível com o transporte; não presumir exatamente uma entrega.

## Channel de Log da Feature

`rg -n 'trait.*Logging' app` não encontrou trait de logging. `config/logging.php` já tem canais ai, tenancy e autenticacao, mas nenhum de compras. Usar chamadas explícitas sem criar trait nova:

`Log::channel('aprovacao-solicitacao-compra')`, driver daily, arquivo `storage/logs/aprovacao-solicitacao-compra.log`, level `env('LOG_LEVEL', 'debug')`, days 14 e replace_placeholders true.

Cada log abaixo usa mensagem completa `[Classe@Método] ação | identificador: {id} - detalhe: {valor}` e contexto com allowlist. Campos possíveis: solicitacao_id, actor_id interno, tenant_id quando aplicável, status_anterior, status_atual, etapa, versao, error_code seguro e exception_type. Não incluir descrição, justificativa, e-mail, nome, valor monetário, corpo de formulário, URL, token ou mensagem/trace bruto de exception. Logs de sucesso somente após commit.

## Estrutura de Implementação

### 1. Preparar channel da feature

- **Skills futuras**: ponytail; PHP/Laravel conforme skills efetivamente disponíveis na execução.
- **Path**: `config/logging.php`.
- **Atende**: RQ-01 a RQ-17, como infraestrutura dos passos com lógica.
- Adicionar somente o channel especificado acima. Sem chave nova de ambiente e sem alterar canais existentes.
- **Logs**: configuração não executa lógica de domínio; não emitir log ao carregar config. O primeiro ponto de uso é o passo 2.
- **Verificação futura**: config resolve o channel; sem criar teste de comportamento do config que espelhe sua declaração.

### 2. Definir persistência e invariantes determinadas

- **Skills futuras**: ponytail; Eloquent/PHP conforme disponibilidade.
- **Paths propostos**: `app/Models/SolicitacaoCompra.php`, `app/Models/StatusSolicitacaoCompra.php`, `database/migrations/2026_10_20_000001_create_solicitacoes_compra_table.php`, `database/factories/SolicitacaoCompraFactory.php`.
- **Atende**: RQ-01, RQ-03, RQ-04, RQ-06, RQ-07, RQ-10 a RQ-16.
- Usar Artisan --no-interaction para gerar artefatos em futura implementação; conferir timestamp da migration gerada antes de atualizar path. Declarar `$table = 'solicitacoes_compra'`; não depender de plural inglês para model pt-BR.
- Proposta de núcleo: id bigint PK; uuid unique obrigatório; solicitante_id FK users obrigatório; descricao text obrigatória; valor_centavos bigint obrigatório; status string(40) obrigatório; versao unsignedInteger default 0; timestamps. UUID, solicitante, status e aprovações ficam fora do preenchimento pelo cliente.
- Estados propostos do enum, chaves TitleCase: Rascunho, AguardandoGestor, AguardandoDiretor, Aprovada e Cancelada. Valores persistidos em snake_case. Não criar estado Rejeitada permanente: a rejeição retorna a rascunho.
- Identidades aprovadas por etapa e instante precisam persistir para RQ-16. Proposta de campos internos nullable: gestor_aprovado_por, gestor_aprovado_em, diretor_aprovado_por, diretor_aprovado_em. Não apagar evidência existente nem definir sua reutilização sem Q11. Persistência histórica adicional depende de resposta, não está decidida.
- Índices propostos: solicitante_id/status; quando houver tenancy, prefixar índices por tenant_id. FKs, nulabilidade e formato de centro de custo/atribuição e tratamento de exclusão de referências só podem ser finalizados após Q1 e inspeção do schema real. Não copiar cascade de demonstração sem avaliar imutabilidade.
- **Recorte bloqueado**: integração completa da tabela com centro de custo e aprovadores (Q1), limites Q7–Q9 e história Q11. O núcleo e os invariantes podem ser especificados sem escolher esses valores; a migration completa ainda não é executável.
- **Logs**: nos comandos que usarão este núcleo, debug `[SolicitacaoCompra@executarTransicao] Iniciando transição | solicitacao_id: {id} - etapa: {etapa}`; warning `[SolicitacaoCompra@executarTransicao] Recusando estado incompatível | solicitacao_id: {id} - error_code: stale_state`; error no catch que interrompe `[SolicitacaoCompra@executarTransicao] Falha ao persistir transição | solicitacao_id: {id} - error_code: persistence_failed`. Contexto permitido: id, etapa, versão, estados e classe segura da exceção.

### 3. Integrar fonte de centro de custo e aprovadores

- **Skills futuras**: ponytail; Laravel/PHP conforme contrato decidido.
- **Paths conhecidos**: integração em `app/Models/SolicitacaoCompra.php` e campos do Resource no passo 7. Path da fonte e eventual migration dependem da resposta; não inventar tabela ou serviço externo.
- **Atende**: RQ-02, RQ-05; resolução para RQ-06 e RQ-17.
- **Bloqueado por**: RQ-02 (aberta — Q1).
- **Bloqueado por**: RQ-05 (aberta — Q1).
- Depois da resposta: documentar chave estável do centro, relação com organização, forma de resolver gestor e diretor e disponibilidade da fonte. Se forem pedidos novos cadastros, registrar o Adendo de escopo antes de detalhar novas migrations/Resources.
- A entidade que falta não será criada nesta etapa por recomendação sem resposta. Nenhum passo de envio pode tratar roteamento não implementado como atendido.
- Recortes Q12/Q13 aguardam sua fronteira; não executar transferência ou fallback.
- **Logs propostos após resposta**: debug `[SolicitacaoCompra@resolverAprovador] Consultando responsável da etapa | solicitacao_id: {id} - etapa: {etapa}`; warning `[SolicitacaoCompra@resolverAprovador] Recusando responsável inválido | solicitacao_id: {id} - error_code: invalid_approver`. Contexto: id, etapa e código; não logar dados da fonte. O comportamento de recusa ainda depende de Q13.

### 4. Aplicar autorização no domínio e no painel

- **Skills futuras**: ponytail; PHP/Laravel; observar .ai/rules/filament.md.
- **Paths**: `app/Policies/SolicitacaoCompraPolicy.php`, `app/Models/SolicitacaoCompra.php`; avaliar `database/seeders/PapeisSeeder.php` somente após saber quais permissões serão necessárias.
- **Atende**: RQ-03, RQ-04, RQ-07 a RQ-09, RQ-13, RQ-14; consulta de RQ-15/RQ-16.
- Assinaturas propostas: métodos de policy com `User $user, SolicitacaoCompra $solicitacao` e retorno bool; métodos privados de domínio `exigirSolicitante(User $actor): void`, `exigirAprovador(User $actor, string $etapa): void`, `exigirEstado(StatusSolicitacaoCompra $estado): void`.
- Revalidar ator, contexto e estado dentro do comando, inclusive se a chamada vier de job/CLI. Nunca confiar em hidden/disabled, UUID ou query de tabela como única guarda.
- **Recortes bloqueados**: sobreposições Q2/Q3/Q4, audiência Q5 e vínculo Q1. Regras determinadas do solicitante e da imutabilidade permanecem; nenhum bypass automático a master_global.
- Depois de existir Resource, gerar permissões com ShieldPermissionsSeeder e depois PapeisSeeder, conforme rule; revisar policy gerada e impedir permissões amplas de substituírem guardas do model.
- **Logs**: warning `[SolicitacaoCompra@exigirSolicitante] Recusando ator sem autorização | solicitacao_id: {id} - error_code: actor_denied`; `[SolicitacaoCompra@exigirAprovador] Recusando decisão sem autorização | solicitacao_id: {id} - etapa: {etapa}`. Contexto: id, actor_id interno, tenant_id quando definido, etapa, error_code. Sem exceção bruta.

### 5. Criar, editar e excluir rascunhos

- **Skills futuras**: ponytail; Eloquent/PHP; testes derivados posteriormente.
- **Paths**: `app/Models/SolicitacaoCompra.php` e páginas Create/Edit indicadas no passo 7.
- **Atende**: RQ-01 a RQ-04, RQ-10, RQ-13.
- Assinaturas propostas: `criarRascunho(User $actor, array $dados): self`, `editarRascunho(User $actor, array $dados): void`, `excluirRascunho(User $actor): void`. PHPDoc de `$dados` terá array shape de descricao, valor_centavos e referência de centro somente após Q1.
- Validar no domínio; recusar atributos inesperados de identidade, status, aprovação ou organização. Request não escolhe solicitante. Edição/exclusão relê estado e confere dono na mesma operação protegida.
- **Recorte bloqueado**: centro de custo **Bloqueado por**: RQ-02 (aberta — Q1); limites Q7/Q9. Não tratar criação sem centro como entrega completa. A obrigatoriedade da justificativa será aplicada à rejeição no passo 6; seu teto depende de Q8.
- **Logs**: debug no início de cada método; info após persistência: `[SolicitacaoCompra@criarRascunho] Criando rascunho | solicitacao_id: {id} - status: rascunho`, `[SolicitacaoCompra@editarRascunho] Salvando rascunho | solicitacao_id: {id} - status: rascunho`, `[SolicitacaoCompra@excluirRascunho] Excluindo rascunho | solicitacao_id: {id} - status: rascunho`. Warning em validação com mensagem `[SolicitacaoCompra@editarRascunho] Recusando dados inválidos | solicitacao_id: {id} - error_code: invalid_input`, adaptando método ao ponto real. Contexto somente IDs, status e códigos; error em falha de persistência conforme passo 2.

### 6. Executar transições e decisões

- **Skills futuras**: ponytail; Laravel/Eloquent/PHP; integração com testes após step 7.
- **Path**: `app/Models/SolicitacaoCompra.php`.
- **Atende**: RQ-05 a RQ-14, RQ-16, RQ-17.
- Assinaturas propostas: `enviar(User $actor): void`, `aprovarComoGestor(User $actor): void`, `aprovarComoDiretor(User $actor): void`, `rejeitarComoGestor(User $actor, string $justificativa): void`, `cancelar(User $actor): void`. Reenvio usa enviar; não criar método de rejeição do diretor antes de Q10.
- Para cada comando, reler registro, executar guardas e atualização condicional por versão/estado em transação. Persistir decisão e estado juntos; zero linhas afetadas indica conflito, sem repetir efeitos ou notificação. O usuário pode recarregar o detalhe autorizado, preservando o estado já salvo.
- Transições determinadas: rascunho enviado encaminha gestor; gestor aprova valor até R$ 5.000 para aprovada; gestor aprova acima desse valor para aguardando_diretor; diretor só aprova após gestor e conclui; gestor rejeita com justificativa obrigatória e retorna a rascunho; solicitante pode cancelar em qualquer estado anterior à aprovação final.
- Não interpretar a aprovação intermediária do gestor como estado final de pedido acima do limiar. Comando após aprovação final não altera descrição, valor, centro, decisões nem status.
- **Bloqueado por**: RQ-05 (aberta — Q1), no encaminhamento completo.
- **Recortes bloqueados**: Q2–Q4, Q8, Q10–Q14. Regras determinadas acima não autorizam preencher esses ramos. Cancelar após final é negado pelo card; reabrir cancelada não é decidido.
- **Logs**: debug no início, info após commit com prefixo do método real: `[SolicitacaoCompra@enviar] Encaminhando solicitação | solicitacao_id: {id} - etapa: gestor`; `[SolicitacaoCompra@aprovarComoGestor] Registrando aprovação do gestor | solicitacao_id: {id} - status: {status}`; `[SolicitacaoCompra@aprovarComoDiretor] Registrando aprovação final | solicitacao_id: {id} - status: aprovada`; `[SolicitacaoCompra@rejeitarComoGestor] Devolvendo solicitação para correção | solicitacao_id: {id} - status: rascunho`; `[SolicitacaoCompra@cancelar] Cancelando solicitação | solicitacao_id: {id} - status: cancelada`. Warning para conflito/validação e error para catch interruptivo. Contexto: id, actor_id, estados, etapa e versão; nunca justificativa.

### 7. Entregar Resource e leitura das etapas

- **Skills futuras**: ponytail; Filament/Livewire/PHP conforme disponibilidade.
- **Paths**: `app/Filament/App/Resources/SolicitacoesCompra/SolicitacaoCompraResource.php`; páginas em `app/Filament/App/Resources/SolicitacoesCompra/Pages/ListSolicitacoesCompra.php`, `CreateSolicitacaoCompra.php`, `EditSolicitacaoCompra.php`, `ViewSolicitacaoCompra.php`.
- **Atende**: RQ-01 a RQ-04, RQ-08 a RQ-16.
- Usar Resource form(Schema): Schema, table(Table): Table, getEloquentQuery(): Builder e getPages(): array, seguindo convenção. Formulário só entrega descrição, valor e referência autorizada do centro. Status e identidades são leitura.
- CreateRecord e EditRecord devem delegar persistência ao domínio através dos hooks documentados na versão restaurada. Não sobrescrever assinatura herdada por memória. Modal de rejeição usa Action::make()->schema([...]); justificativa é required e passa à guarda do domínio. Campos salvos não recebem dehydrated(false).
- Tabela com status e relações carregadas em lote; detalhe com etapa, pessoa que aprovou e instante. Não inventar timeline de tentativas antes de Q11.
- Ações de envio/aprovação/rejeição/cancelamento chamam os comandos do passo 6, sem update direto no callback. Falha de autorização/estado aparece como mensagem legível e opção de recarregar detalhe/lista permitida. Não criar redirecionamento circular.
- **Bloqueado por**: RQ-02 (aberta — Q1), na seleção do centro.
- **Recortes bloqueados**: consulta Q5, link Q6, limites Q7/Q8/Q9, acúmulo Q2/Q3/Q4 e história Q11. A especificação das colunas de status e aprovadores continua determinada.
- **Logs**: success fica nos comandos, sem duplicar emissão a cada renderização. Warning no ponto de falha da ação: `[ViewSolicitacaoCompra@{acao}] Recusando ação da solicitação | solicitacao_id: {id} - error_code: {codigo}`; validação de Create/Edit usa seus prefixos reais e código invalid_input. Contexto: id, nome de ação de allowlist e código seguro. Não logar estado completo do componente.

### 8. Notificar próximo aprovador após persistência

- **Skills futuras**: ponytail; Laravel Notifications/Queues/PHP.
- **Path**: `app/Notifications/SolicitacaoCompraAguardandoAprovacao.php`; pontos de disparo em `app/Models/SolicitacaoCompra.php`.
- **Atende**: RQ-05, RQ-06, RQ-12, RQ-17.
- Proposta de assinatura: construtor com IDs internos de solicitação e contexto organizacional, etapa e versão, nunca aceitos do navegador; `via(object $notifiable): array`, `toMail(object $notifiable): MailMessage`. Conferir necessidade/assinatura de shouldSend no vendor antes de depender dele.
- Destino resolve a partir do centro/etapa. Envio ao gestor no encaminhamento e ao diretor após aprovação do gestor para valores acima do limiar. Aprovação final não tem próximo aprovador; não criar e-mail extra de resultado por inferência.
- Identidade do ator que executou o comando não substitui destinatário. Recarregar registro com contexto explícito no worker; não depender do tenant em memória de um request anterior.
- **Bloqueado por**: RQ-05 (aberta — Q1), no encaminhamento completo.
- **Recortes bloqueados**: Q6, Q12, Q13, Q15, Q16. Não assumir supressão, troca de destinatário, rollback ou garantia durável sem resposta.
- **Logs**: info após enfileirar `[SolicitacaoCompra@notificarProximoAprovador] Enfileirando notificação da etapa | solicitacao_id: {id} - etapa: {etapa}`. Este log prova enfileiramento, não entrega. Error no ponto de falha interruptiva `[SolicitacaoCompraAguardandoAprovacao@failed] Falha ao notificar aprovador | solicitacao_id: {id} - error_code: mail_delivery_failed`, após conferir assinatura real. Contexto: IDs, etapa, attempt quando disponível, código e classe segura de erro; sem corpo/endereço de e-mail. Política de recuperação aguarda Q16.

### 9. Verificar automaticamente e conferir regressão

- **Skills futuras**: feature-test-design no step 7; ponytail na execução; revisão e QA somente em seus steps autorizados.
- **Paths planejados, ainda sem testes ou CTs**: `tests/Feature/AprovacaoSolicitacaoCompra/` e `tests/Tenancy/AprovacaoSolicitacaoCompraTest.php`. Não criar diretório/arquivo nesta rodada. Se os helpers forem compartilhados, reutilizar `tests/Pest.php`; não duplicar.
- **Atende**: RQ-01 a RQ-17; somente recortes determinados podem receber testes antes das respostas.
- A derivação futura recebe o requisito, não este plano como oráculo. RQ-02/RQ-05 abertas não geram cenário; recortes determinados das demais RQ não são descartados.
- Factories confirmadas: UserFactory, TenantFactory; criar factory da solicitação junto ao model. Não supor factory de centro de custo inexistente.
- Após casos derivados e implementação autorizada: executar testes afetados com `php artisan test --compact {arquivo}`, gravação real por componente nas páginas create/edit e pares de isolamento Single/Tenancy. Os testes do domínio chamam métodos diretamente para provar a barreira independente da UI.
- `tests/Pest.php` ativa TIA localmente. Baseline completa somente após restaurar ambiente e base; não executar suíte que alcance caminhos proibidos nesta sessão. Para futura seleção, respeitar .ai/rules/testes-browser.md: browser em série e TIA não usado como atalho de CI.
- Pint obrigatório se houver PHP alterado: `vendor/bin/pint --dirty --format agent`. Mutation testing futuro usa lançador Windows da skill e prova discriminante, sem declarar score por mera saída não zero.
- **Logs**: este passo não adiciona lógica de produção; conferir os logs dos passos anteriores no gate apropriado. Não derivar CT de log sem RQ de auditoria.

## Filosofia de Implementação

Ponytail full na futura implementação: reutilizar código existente, framework nativo e o mínimo de métodos necessários. Não criar pacote de workflow, camada de serviço genérica, evento/listener redundante, scheduler de aprovação ou cache de autorização.

O Caveman vale para conversa; esta wiki usa prosa completa. Model em português declara tabela explicitamente. Dependências não mudam sem autorização. Nenhum artefato de código ou teste será criado nesta sessão.

## Mapeamentos

| Entrada / fato | Persistência ou resultado determinado | Situação |
|---|---|---|
| descrição | descricao | obrigação determinada; limite Q7 |
| valor | valor_centavos, conversão decimal exata | representação D2; domínio Q9 |
| centro de custo | referência ainda indefinida | RQ-02 aberta — Q1 |
| solicitante | usuário autenticado no contexto permitido | nunca recebido como atributo editável |
| valor > 500000 centavos | exige etapa diretor depois do gestor | RQ-06/RQ-07 |
| valor = 500000 centavos | aprovação do gestor conclui | consequência literal de “acima” |
| rejeição do gestor com justificativa | rascunho | RQ-09/RQ-10/RQ-11 |
| aprovador da etapa | identidade persistida e mostrada | RQ-16; audiência Q5 e tentativas Q11 |
| aprovação final | imutabilidade | RQ-13 |
| cancelamento antes da final | status Cancelada | RQ-14; destino posterior Q14 |

## Testes

Ainda não derivados. O `04-casos-de-teste.md` será criado somente no step 7 após as revisões autorizadas; `05-casos-de-teste-browser.md` somente se houver costura browser confirmada. Não há IDs CT inventados no PRD.

## Verificação Final

Checklist futuro; nada executado além da pesquisa do step 3:

- [ ] Restaurar ambiente autorizado, inspecionar schema real e confirmar APIs no vendor.
- [ ] Baseline na base main e falhas pré-existentes por nome, sem acessos a caminhos proibidos nesta rodada.
- [ ] Respostas como Adendo e desbloqueio somente do recorte respondido.
- [ ] Pint e testes afetados; gravação por componente e regressão de permissões/tenancy.
- [ ] Caso browser somente se costura exigir; execução em série.
- [ ] Medir queries com N acima da página; confirmar modelo de execução.
- [ ] Mutation testing com lançador correto, duração, sobreviventes e prova discriminante.
- [ ] Revisão independente do diff antes de reconciliação, no step próprio.
- [ ] Reconciliação e scripts na etapa própria, depois QA; sem antecipação nesta execução.

## Commits

Não há .git; nenhum commit nesta sessão. Pasta lógica de branch é saida-p5, por instrução. Base de referência é main, não verificável neste checkout. Em repositório real e com autorização futura: `:memo: compras: wiki do fluxo de aprovação`; `:sparkles: compras: fluxo de aprovação de solicitação`. Não executar git init nem fabricar histórico.

