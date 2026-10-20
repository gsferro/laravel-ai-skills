# Plano de Ação — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: [00-requisito.md](00-requisito.md). Plano condicionado às respostas; não é autorização de implementar.
> Escopo desta sessão: steps 0–4. O step 5 não foi iniciado.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma de compras; as wikis de organização, acesso e convites são referências de integração.
- **Motivo**: domínio de compras e centros de custo não localizado no projeto.
- **Toca infra compartilhada?**: sim, configuração de logging e eventual geração de permissões/matriz de papéis. Isso exige regressão dos consumidores da infraestrutura alterada, mesmo sendo feature nova.
- **Prontidão**: planejamento parcial por informações de negócio e ambiente ausentes. Paths de classes novas são candidatos condicionados a Q1, não uma decisão de criar as entidades.

## Cobertura do Requisito

Cada linha preserva a obrigação determinada. Os bloqueios de recorte não tornam uma recomendação parte do requisito.

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|---|---|---|---|
| RQ-01 | Criar solicitação | 2, 3, 5 | **Bloqueado por**: RQ-01 (aberta — Q1). |
| RQ-02 | Descrição | 3, 5 | Integração depende de Q1; teto/momento obrigatório, de Q13. |
| RQ-03 | Valor | 2, 3, 5 | Integração depende de Q1; domínio monetário, de Q15. |
| RQ-04 | Centro de custo | 2, 3, 5 | **Bloqueado por**: RQ-04 (aberta — Q1); designação de responsáveis, Q2. |
| RQ-05 | Editar rascunho | 3, 5 | Direito determinado; exceções administrativas, Q17. |
| RQ-06 | Excluir rascunho | 3, 5 | Direito determinado; retenção após exclusão, Q16. |
| RQ-07 | Enviar ao gestor | 4, 5, 6 | Encaminhamento determinado; resolver pessoa, Q2; substituição, Q3. |
| RQ-08 | Diretor acima de R$ 5.000 | 4, 5, 6 | Comparação estrita determinada; pessoas acumulando papéis, Q5/Q6. |
| RQ-09 | Diretor depois do gestor | 4, 5 | Ordem determinada; dupla função, Q6. |
| RQ-10 | Gestor aprova | 4, 5 | Direito determinado; autoaprovação, Q4. |
| RQ-11 | Gestor rejeita | 4, 5 | Não estender ao diretor enquanto Q7 estiver aberta. |
| RQ-12 | Justificativa obrigatória | 4, 5 | Obrigatoriedade determinada; teto e texto válido, Q14. |
| RQ-13 | Rejeição volta ao rascunho | 4, 5 | Retorno determinado; validade das aprovações anteriores, Q8. |
| RQ-14 | Corrigir após rejeição | 3, 5 | Direito determinado; domínio de campos, Q13/Q15. |
| RQ-15 | Reenviar após rejeição | 4, 5, 6 | Direito determinado; sem reutilizar ou apagar aprovações por decisão tácita, Q8. |
| RQ-16 | Imutabilidade após aprovação | 2, 3, 4, 5 | Aprovação final impede mutações; eventual exceção administrativa, Q17. |
| RQ-17 | Cancelar antes da aprovação final | 4, 5 | Inclui espera do diretor; reabertura após cancelar, Q9. |
| RQ-18 | Mostrar status | 5 | Conteúdo determinado; público autorizado e acesso histórico, Q10/Q11. |
| RQ-19 | Mostrar aprovador por etapa | 2, 4, 5 | Identidade determinada; ciclos e público, Q8/Q10/Q11. |
| RQ-20 | E-mail ao próximo aprovador | 4, 6 | Canal determinado; destinatário, Q2; link, Q12; falha/obsolescência, Q18. |

O passo 1 fornece infraestrutura para os logs dos passos vinculados a RQ-01–RQ-20.
Não há P-nn. Nenhuma obrigação foi marcada como fora desta entrega. Toda integração concreta depende da resolução do escopo de Q1; isso não elimina as partes determinadas acima.

## Objetivo

Planejar o fluxo de solicitação de compra com rascunho, envio ao gestor, segunda aprovação acima do limiar, retorno para correção, cancelamento, consulta de status/aprovadores e e-mail ao próximo responsável.

Preservar a diferença entre requisito explícito e recomendação. Não substituir o card por um motor isolado nem criar cadastros pressupostos sem resposta sobre o escopo.

## Contexto

O projeto é um starter kit com painéis, usuários, organizações, permissões e notificações de convite. Projeto é uma demonstração de tenancy, sem semântica de compra. Não há domínio de centro de custo ou designação de aprovadores para reutilizar.

A ausência foi investigada em app, database, routes e wikis de produção. Comando e resultado estão no progresso. Não há conexão de banco validada, vendor nem MCP Boost exposto. O desenho persistente permanece candidato.

## Análise dos Arquivos Existentes

### Domínio, identidade e autorização

- `app/Models/Projeto.php`, classe Projeto: exemplo de composição de traits, explicitamente descartável; não converter Projeto em solicitação de compra.
- `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`: escopo depende de tenant corrente. A documentação da própria trait alerta que jobs sem tenant fazem query global.
- `app/Providers/KitServiceProvider.php:configureGates():86`: o Gate::before do master_global antecede policies. Proteger invariantes de estado também no método de mutação.
- `database/seeders/PapeisSeeder.php:run():45`: matriz de papéis do painel. Atribuições a admin_organizacao e panel_user podem herdar novas permissões; isso não designa gestor ou diretor.
- `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60`: Schema e formulário no padrão atual.
- `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`: ações em Filament Actions e tabela no Resource.
- `app/Providers/Filament/AppPanelProvider.php:panel():56`: /app e descoberta de Resources; tenancy é opt-in. Nomes e URI efetivos precisam de route:list quando o app voltar a inicializar.

### E-mail, operação e testes

- `app/Notifications/ConviteDeAcesso.php:via():43` e `app/Notifications/ConviteDeAcesso.php:toMail():48`: precedente de Notification com mail, Queueable e ShouldQueue.
- `config/queue.php:'default':16`: default database; `config/queue.php:'after_commit':44`: falso. Não presumir commit diferido por configuração global.
- `config/mail.php:'default':17`: default log. Esse default não comprova entrega externa; .env.example também usa log.
- `config/logging.php:'autenticacao':101`: channel específico já existente, sem channel de compras.
- `tests/Pest.php`: Feature usa RefreshDatabase; Tenancy usa TenancyTestCase; browser usa servidor do plugin e timeout de 20.000 ms; TIA local está configurado.
- Factories encontradas: User, Tenant e Convite; estados verificados incluem User::unverified e Tenant::inativo/comIdentidadeVisual. Nenhuma factory de compras existe.
- `phpunit.xml`: SQLite em memória, mail array e fila sync nos testes. Essa pilha não comprova concorrência do banco de produção nem entrega em worker real.

### Fontes de produção

Consultadas as wikis `wikis/specs/main/convite-de-usuario/`, `wikis/specs/main/admin-da-organizacao/` e `wikis/specs/feature/multi-tenancy/organizacoes/`. O precedente é Notification enfileirada sem Job adicional; administração da organização usa matriz recortada. A wiki de tenancy conserva nomenclatura histórica Organizacao, enquanto o código atual usa Tenant. Não criar um segundo model para acomodar esse nome antigo.

## Pesquisa de APIs e versões

`composer show --direct` retornou “No dependencies installed”. As versões abaixo são as resolvidas no lock, não uma instalação executável:

| Pacote | composer.lock |
|---|---|
| laravel/framework | v13.25.0 |
| filament/filament e filament/actions | v5.7.6 |
| livewire/livewire | v4.4.0 |
| pestphp/pest | v5.1.1 |
| pestphp/pest-plugin-browser | v5.0.1 |
| laravel/boost | v2.5.3 |

PHP CLI observado: 8.4.10. package.json declara Playwright ^1.62.1; node_modules está ausente. Não instalar nem atualizar dependências nesta sessão.

**Degradação de pesquisa**: search-docs, database-schema e database-query não estão expostos. O fallback foi leitura de código/migrations e documentação oficial, sem alegar consulta ao banco ou ao vendor.
Fontes abertas em 2026-10-20:

- Policies e validação: [Laravel 13 — authorization](https://laravel.com/docs/13.x/authorization), [validation](https://laravel.com/docs/13.x/validation).
- Notificação em fila após commit: [Laravel 13 — notifications](https://laravel.com/docs/13.x/notifications#queued-notifications-and-database-transactions). A API afterCommit existe; adotá-la na notificação evita alterar todas as filas.
- Unidade atômica e bloqueio: [Laravel 13 — query builder](https://laravel.com/docs/13.x/queries#pessimistic-locking). A adequação ao banco real ainda depende de schema e ambiente.
- Configuração operacional: [Laravel 13 — queues](https://laravel.com/docs/13.x/queues), [logging](https://laravel.com/docs/13.x/logging).
- Composição da UI e URLs: [Filament 5 — resources](https://filamentphp.com/docs/5.x/resources/overview), [actions](https://filamentphp.com/docs/5.x/actions/overview), [tenancy](https://filamentphp.com/docs/5.x/users/tenancy).
- Entradas do cliente: [Livewire 4 — security](https://livewire.laravel.com/docs/4.x/security). Parâmetros de ações e propriedades públicas precisam de validação e autorização no servidor.
- Stack de verificação: [Pest 5](https://pestphp.com/docs/pest5-now-available), [TIA](https://pestphp.com/docs/tia), [browser](https://pestphp.com/docs/browser-testing). Nenhum cenário foi derivado nesta etapa.

## Decisões de Desenho

| # | Decisão | Pergunta | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Reutilizar padrão de Notification enfileirada; sem evento/listener/Job intermediário apenas para despachar mail. Aplicação concreta condicionada ao domínio. | Convenção de ConviteDeAcesso; RQ-20 | Difícil de reverter e surpreendente | Sessão, 2026-10-20 |
| D2 | Propor uma única camada de mutação no model, com transação e revalidação. Não criar framework genérico de workflow. | RQ-05–RQ-17, convenção do model Convite | Difícil de reverter | Sessão, 2026-10-20 |
| D3 | Reutilizar componentes nativos Filament e URLs do Resource. Os paths abaixo só valem se Q1 confirmar criação. | RQ-01–RQ-20 | Difícil de reverter e surpreendente | Sessão, 2026-10-20 |
| D4 | Não criar channel de logging genérico nem trait nova; usar formato manual, pois a busca por trait de Logging não encontrou resultado. | Infra de RQ-01–RQ-20 | Difícil de reverter | Sessão, 2026-10-20 |

Q1–Q18 continuam requisitos pendentes. Nenhuma decisão de desenho autoriza mudar público, pessoas, limite, validade de aprovação ou conteúdo de notificação.

## Autorização

Propor `app/Policies/SolicitacaoCompraPolicy.php` somente após Q1.
Contratos candidatos, todos retornando bool: viewAny(User $user), create(User $user), e view/update/delete/enviar/aprovarComoGestor/rejeitarComoGestor/aprovarComoDiretor/cancelar(User $user, SolicitacaoCompra $solicitacao).

A camada de domínio também deve conferir autor, responsável da etapa, estado atual e fronteira organizacional, conforme as respostas. Não confiar apenas em policy, filtro da tabela ou botão oculto. A invariância de RQ-16 não pode ser vencida pelo Gate::before.

Sem novo guard ou middleware global. Herdar autenticação, sessão e proteção contra falsificação de request do painel. Em tenancy, a proteção persistente dos requests Livewire já é configurada pelo provider. Q2/Q10/Q11/Q17 bloqueiam seus recortes.

Se surgir Resource, gerar permissões conforme a rule Filament: ShieldPermissionsSeeder antes de PapeisSeeder, revisar a matriz gerada e impedir que permission genérica substitua designação nominal de aprovador. Se a resposta pedir um cadastro administrativo novo, sua classificação na lista de administração exige revisão específica; isso não foi autorizado implicitamente.

## Rotas

Propostas após Q1, com slug `solicitacoes-compra`; confirmar nomes pelo route:list, sem registrar nada agora.

| Método | URI sem tenancy | Nome candidato | Middleware |
|---|---|---|---|
| GET | /app/solicitacoes-compra | filament.app.resources.solicitacoes-compra.index | Pilha do painel, auth, policy |
| GET | /app/solicitacoes-compra/create | filament.app.resources.solicitacoes-compra.create | Pilha do painel, auth, policy |
| GET | /app/solicitacoes-compra/{record}/edit | filament.app.resources.solicitacoes-compra.edit | Pilha do painel, auth, policy e rascunho próprio |
| GET | /app/solicitacoes-compra/{record} | filament.app.resources.solicitacoes-compra.view | Pilha do painel, auth, regra de leitura |

Com tenancy habilitada, inserir /{tenant} depois de /app, como no provider. O recurso de negócio não assume que centro de custo é Tenant.
As mutações usam ações do componente Livewire, sem endpoints próprios de API planejados. Não fixar o URI interno do Livewire sem inspeção.
Gerar links por getUrl do Resource/named route. Não compartilhar URL de execução sem get-absolute-url; a ferramenta não está disponível nesta sessão.

## Superfície de UI

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| ListSolicitacoesCompra | Filament | index da tabela de rotas | Listar status, abrir registro e ações permitidas | Sim |
| CreateSolicitacaoCompra | Filament | create | Informar descrição, valor e centro; salvar rascunho | Sim |
| EditSolicitacaoCompra | Filament | edit | Corrigir rascunho próprio; excluir quando permitido | Sim |
| ViewSolicitacaoCompra | Filament | view | Ver status/aprovadores; enviar, aprovar, rejeitar ou cancelar conforme etapa | Sim |

Público de leitura pendente Q10/Q11. Destino do e-mail pendente Q12.
A descrição das telas não afirma existência de implementação. A superfície alcançável está no 02.
Validação, gravação e autorização de Filament são verificáveis por componente. A necessidade de browser será decidida apenas na derivação posterior; nenhuma decisão de criar 05 foi antecipada.

## Variáveis de Ambiente

Nenhuma chave nova proposta. Reutilizar QUEUE_CONNECTION, MAIL_MAILER e configuração de transporte existente.
O default database requer worker; MAIL_MAILER=log não envia para o destinatário. Não copiar credenciais para a wiki nem afirmar ambiente efetivo a partir de .env.example.

## Eventos / Listeners / Observers

Nenhum evento, listener ou observer novo planejado. Disparo da Notification sai da transição confirmada.
Auditoria técnica por AuditsFillables não substitui a identificação de quem aprovou cada etapa.
Caso respostas exijam uma trilha de ciclos, revisitar a persistência e só então decidir mecanismo. Não adicionar outbox genérica sem necessidade confirmada.

## Jobs / Queues

Notification candidata ProximaAprovacaoDeCompra implementa ShouldQueue e usa Queueable/afterCommit.
Conexão e fila herdadas da instalação, sem nome de fila fixo adicional. Não alterar after_commit global.
Timeout, tentativas e backoff serão definidos no recorte de Q18, considerando retry_after e transporte reais; não existe valor operacional confirmado.
Falha de despacho, entrega e repetição são eventos distintos. O card não promete entrega exatamente uma vez.

## Modelo de Execução

| Pergunta | Resposta proposta |
|---|---|
| Quantos requests? | GET de entrada e requests Livewire de interação; não medido nem fixado como número contratual. |
| O que é adiado? | Apenas transporte de mail em fila após commit; sem polling ou widgets lazy propostos. |
| Memoização por request? | Nenhuma nova. |
| Cache entre requests? | Nenhum novo; permissões continuam com cache existente. |
| Escrita principal? | Uma unidade atômica por comando, recarregando registro e estado. |
| Custo de queries? | Não medido. Projetar relações carregadas em lote para status/aprovadores; medir com conjunto maior que a página posteriormente. |

Transações e lock de linha são candidatos no banco que os suportar. SQLite em memória não será usado como prova de corrida de produção. Não introduzir cache de autorização ou de estado de aprovação.

## Impacto em Features Existentes

- Papéis e permissões: geração pode ampliar matriz do painel. Regressão de acesso e administração da organização é obrigatória se essa infraestrutura mudar.
- Tenancy: não deixar consultas em worker dependentes de Filament::getTenant(); transportar e filtrar contexto explícito quando aplicável.
- Convites/notificações: reutilizar fila sem alterar comportamento ou nomes globais.
- Logging: acrescentar channel sem alterar channels atuais.
- Domínio de demonstração Projeto: não reutilizar seus registros como compras.

## Rollback

Não há migration autorizada ou aplicada. O down definitivo depende de schema e retenção ainda abertos.
Planejar reversão de código e retirada das permissões da feature sem apagar dados aprovados. Não supor que rollback de código desfaz decisões humanas ou e-mails já enviados.
Qualquer reversão destrutiva de compras/histórico dependerá de decisão específica, cópia de segurança e retenção confirmada; não está prevista como execução automática.

## Dependências

Nenhuma dependência nova proposta. Composer e NPM não foram instalados porque isso alteraria arquivos externos à wiki.
Pest/browser estão declarados e no lock, mas ausentes em runtime. Não incluir instalação redundante de pacote já declarado.
Antes de implementação futura, restabelecer o ambiente em um checkout autorizado e confirmar APIs instaladas/schema por Boost. Isso não será feito nesta sessão.

## Riscos

- Escopo Q1: não existe domínio para integrar; implementação persistente bloqueada.
- Papéis Q2–Q6/Q17: não equiparar master, admin_organizacao ou panel_user a aprovador.
- Reciclagem Q8/Q16: não apagar decisões nem reutilizá-las silenciosamente.
- Entrada cliente: formulário, IDs, busca, filtros e ordenação não são confiáveis.
- Corrida: cancelar, aprovar, rejeitar e editar precisam verificar o mesmo estado atual atomicamente.
- Mail Q18: afterCommit não garante entrega nem resolve indisponibilidade entre commit e despacho.
- Ambiente: sem vendor/MCP/DB validado, inventário herdado e desempenho não foram comprovados.

## Channel de Log da Feature

Busca por `aprovacao-solicitacao-compra` em config/logging.php e por `trait.*Logging` em app não encontrou ocorrências. O primeiro passo futuro acrescenta channel daily chamado aprovacao-solicitacao-compra, path storage/logs/aprovacao-solicitacao-compra.log, level debug e retenção de 14 dias.

Usar `Log::channel('aprovacao-solicitacao-compra')` em todos os pontos abaixo.
Allowlist: solicitacao_id, ator_id, tenant_id quando aplicável, etapa, estado_anterior, estado_atual, reason, error_code, exception_type e correlation_id.
Não logar descrição, justificativa, valor da compra, nome, e-mail, payload, atributos completos, mensagem/trace bruto de exceção ou URLs.
Nenhum log operacional substitui os aprovadores mostrados pela UI.

## Estrutura de Implementação

Todos os passos são futuros e não executáveis nesta sessão. Paths abaixo são exatos como candidatos de model/resource; se Q1 apontar módulo existente, revisar o plano para reutilizá-lo em vez de criar duplicata.
Não criar pastas base novas nem arquivo de migration com timestamp inventado. A lista exata de migrations só será definida após Q1 e inspeção de schema.

### 1. Canal de log

> Skills futuras: ponytail; convenções de logging da feature-wiki.

- **Path**: config/logging.php.
- **Atende**: RQ-01–RQ-20 como infraestrutura.
- Acrescentar somente o channel descrito acima; não criar configuração alternativa de negócio.
- Sem método ou log próprio: alteração declarativa. Seus consumidores são os passos 3–6.
- Não executar nesta sessão.

### 2. Persistência e autorização

> Skills futuras: ponytail; diretrizes Laravel/Eloquent disponíveis no host.

- **Atende**: RQ-01, RQ-03, RQ-04, RQ-16, RQ-19; infraestrutura de RQ-02–RQ-20.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-04 (aberta — Q1) e inspeção de schema. Q2, Q8, Q10/Q11, Q16/Q17 bloqueiam somente suas decisões.
- **Paths candidatos**: app/Models/SolicitacaoCompra.php e app/Policies/SolicitacaoCompraPolicy.php.
- CentroCusto e registros de decisões/ciclos não ganham arquivos prometidos enquanto Q1/Q8/Q16 não definirem se existem, se precisam ser criados e qual sua retenção.
- Campos lógicos necessários: descrição, valor exato, referência ao centro, solicitante, estado e identidade de quem decidiu cada etapa.
- UUID e contexto organizacional seguem o módulo confirmado. Proteger IDs de controle contra mass assignment; declarar $table explicitamente para nome pt-BR.
- Não fixar tipo, nullable, FK, cascade ou índices como schema aprovado. Candidatos: descrição textual; valor monetário decimal ou inteiro de centavos; FKs para usuário/centro; índice pelo recorte organizacional/estado. Tipos e cardinalidades dependem de schema e Q1/Q2/Q15.
- Métodos de policy listados em Autorização são candidatos, não APIs existentes. Rejeitar por domínio o que a UI ocultar; não alterar Gate::before global.
- Logs das negativas de escrita ficam no comando de domínio correspondente para evitar duplicação. Consultas de leitura não recebem log de sucesso por linha.
- A ausência de migrations, factories e seeders definitivos é um bloqueio declarado de planejamento, não autorização para improvisar schema na implementação.

### 3. Operações de rascunho

> Skills futuras: ponytail; diretrizes Laravel/Eloquent.

- **Atende**: RQ-01–RQ-06, RQ-14, RQ-16.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-04 (aberta — Q1); recortes de campos Q13/Q15, retenção Q16 e exceções Q17.
- **Path candidato**: app/Models/SolicitacaoCompra.php.
- Contratos candidatos: public static function criarRascunho(User $solicitante, array $dados): self; public function editarRascunho(User $solicitante, array $dados): void; public function excluirRascunho(User $solicitante): void.
- Array shape provisório de entrada: array{descricao: string, valor: string, centro_custo_id: int}; revisar ID/tipo após Q1. Não usar float nem aceitar autor, estado, aprovador ou tenant vindos do formulário.
- Carimbar solicitante/contexto no servidor. Editar/excluir exigem rascunho atual e dono autorizado. Recusa de estado deve acontecer antes de gravar.
- RQ-06 inclui rascunho devolvido; Q16 decide retenção, não retira o direito de exclusão.
- Limites sugeridos nas perguntas não são regras adotadas. Erros de campos voltam como validação; falta de autorização não revela registro de outro recorte.
- Logs por método, na tabela de mensagens abaixo: início debug, sucesso info após persistência confirmada, validação/autorização/estado warning e falha que interrompe error.

### 4. Transições de aprovação, correção e cancelamento

> Skills futuras: ponytail; diretrizes Laravel/Eloquent e filas.

- **Atende**: RQ-07–RQ-17, RQ-19, RQ-20.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-04 (aberta — Q1). Resolver responsáveis depende de Q2; combinações Q4–Q6, substituição Q3 e ciclos Q8 permanecem bloqueados nos seus casos.
- **Path candidato**: app/Models/SolicitacaoCompra.php.
- Contratos candidatos: public function enviar(User $solicitante): void; public function aprovarComoGestor(User $gestor): void; public function rejeitarComoGestor(User $gestor, string $justificativa): void; public function aprovarComoDiretor(User $diretor): void; public function cancelar(User $solicitante): void.
- Reenvio usa enviar a partir de rascunho; a validade de decisões prévias aguarda Q8. Não bloquear o direito determinado de reenviar por uma escolha silenciosa de reaproveitamento.
- Recarregar registro e verificar ator, estado e vínculo na mesma transação. Estado entregue pelo cliente ou carregado antes da disputa não prova estado atual.
- Gravar identidade da aprovação junto com a transição; não gravar aprovação do diretor antes da do gestor.
- Aplicar o mapeamento semântico abaixo. A rejeição do gestor exige justificativa e volta para rascunho; Q14 define domínio textual adicional.
- Não implementar rejeição de diretor enquanto Q7 estiver aberta. Não permitir reabertura de cancelada com base em recomendação; Q9 continua pendente.
- A disputa não pode concluir simultaneamente cancelamento e aprovação final. Depois da transição vencedora, a outra deve falhar por estado incompatível; exposição do resultado depende da permissão de leitura, Q11.
- Enfileirar próximo aprovador somente quando há próxima etapa confirmada; conclusão final não inventa um próximo aprovador.
- Logs completos na tabela abaixo, incluindo decisão de encaminhar ao diretor ou concluir.

### 5. Telas e ações Filament

> Skills futuras: ponytail; diretrizes Filament/Livewire do projeto.

- **Atende**: RQ-01–RQ-20 nas operações indicadas na cobertura.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-04 (aberta — Q1); leitura Q10/Q11 e link Q12 bloqueiam seus recortes.
- **Paths candidatos**:
  - app/Filament/App/Resources/SolicitacoesCompra/SolicitacaoCompraResource.php
  - app/Filament/App/Resources/SolicitacoesCompra/Schemas/SolicitacaoCompraForm.php
  - app/Filament/App/Resources/SolicitacoesCompra/Tables/SolicitacoesCompraTable.php
  - app/Filament/App/Resources/SolicitacoesCompra/Pages/ListSolicitacoesCompra.php
  - app/Filament/App/Resources/SolicitacoesCompra/Pages/CreateSolicitacaoCompra.php
  - app/Filament/App/Resources/SolicitacoesCompra/Pages/EditSolicitacaoCompra.php
  - app/Filament/App/Resources/SolicitacoesCompra/Pages/ViewSolicitacaoCompra.php
- Proposta de Resource: form(Schema $schema): Schema e table(Table $table): Table; delegates configure(Schema $schema): Schema e configure(Table $table): Table, no padrão atual.
- Campos descrição/valor/centro e modal de justificativa; status/aprovadores apenas de leitura. Toda seleção de centro precisa ser revalidada no servidor.
- Ações nomeadas enviar, aprovarComoGestor, rejeitarComoGestor, aprovarComoDiretor e cancelar chamam os contratos do passo 4.
- Usar Filament Actions, Forms e Schemas nos namespaces da versão 5. Sem bulk action nova, parâmetro para escolher aprovador ou propriedade pública extra de controle.
- Não presumir que hooks de persistência padrão atendam a imutabilidade. Confirmar na API instalada como Create/Edit invocam os comandos de domínio, sem caminho de gravação paralelo.
- Filtros e ordenação devem usar domínios fechados; nenhuma coluna/operador livre passa à query. Não renderizar texto livre como HTML.
- Falha de campo exibida sem perder conteúdo permitido do rascunho; negativa de acesso não revela dados. Uma operação já logada pelo domínio não é logada novamente pela tela.
- Validação antecipada da tela, quando não chegar ao domínio: warning com prefixo do método real de gravação conferido no vendor. Nome do hook, contexto e mensagem específicos continuam pendentes da inspeção; não inventar assinatura para preencher o plano.

### 6. Notificação ao próximo aprovador

> Skills futuras: ponytail; diretrizes Laravel de notifications/queues.

- **Atende**: RQ-07–RQ-09 e RQ-20.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-04 (aberta — Q1), resolução Q2. Link Q12 e falhas/obsolescência Q18 permanecem recortes pendentes.
- **Path candidato**: app/Notifications/ProximaAprovacaoDeCompra.php.
- Contratos propostos: public function via(object $notifiable): array; public function toMail(object $notifiable): MailMessage.
- Usar Notification/ShouldQueue/Queueable e afterCommit; canal mail. Não adicionar Job wrapper nem novo evento só para transportar o e-mail.
- Payload com identificadores persistidos de solicitação/etapa/destinatário, resolvidos no servidor. Contexto de tenant explícito se aplicável, inclusive quando o worker não tem painel corrente.
- Enviar após envio/reenvio ao gestor e após aprovação do gestor que demanda diretor. Não notificar diretor antecipadamente.
- toMail compõe mensagem, não comprova entrega. Link autenticado só após Q12; não conceder acesso pelo recebimento do e-mail.
- Não afirmar entrega exatamente uma vez. Não implementar descarte de e-mail obsoleto nem política de retry como requisito sem Q18; shouldSend é uma API disponível documentada, mas sua regra de negócio ainda não foi aprovada.
- Logs de enfileiramento na transição: debug antes do despacho, info quando o despacho é aceito, error se o despacho falha. Não rotular esse info como entrega.
- Sem log com corpo/endereço no toMail. Auditoria de envio real e callback de falha precisam da operação definida em Q18 e de API instalada; são lacunas declaradas, não passos ocultos já concluídos.

## Mensagens de log por método

Todas as mensagens usam o channel da feature e contexto da allowlist. O sufixo “| solicitacao_id: {id}” usa o ID interno depois de conhecido; na criação inicial, usar “| ator_id: {id}”.
A tabela especifica mensagens completas por combinação, substituindo apenas identificadores seguros.

| Método | Início — debug | Sucesso — info |
|---|---|---|
| criarRascunho | [SolicitacaoCompra@criarRascunho] Iniciando criação do rascunho | [SolicitacaoCompra@criarRascunho] Rascunho criado |
| editarRascunho | [SolicitacaoCompra@editarRascunho] Iniciando edição do rascunho | [SolicitacaoCompra@editarRascunho] Rascunho atualizado |
| excluirRascunho | [SolicitacaoCompra@excluirRascunho] Iniciando exclusão do rascunho | [SolicitacaoCompra@excluirRascunho] Exclusão de rascunho concluída |
| enviar | [SolicitacaoCompra@enviar] Iniciando envio para aprovação | [SolicitacaoCompra@enviar] Solicitação enviada ao gestor |
| aprovarComoGestor | [SolicitacaoCompra@aprovarComoGestor] Iniciando decisão do gestor | [SolicitacaoCompra@aprovarComoGestor] Aprovação do gestor registrada |
| rejeitarComoGestor | [SolicitacaoCompra@rejeitarComoGestor] Iniciando rejeição do gestor | [SolicitacaoCompra@rejeitarComoGestor] Rejeição registrada e solicitação devolvida ao rascunho |
| aprovarComoDiretor | [SolicitacaoCompra@aprovarComoDiretor] Iniciando decisão do diretor | [SolicitacaoCompra@aprovarComoDiretor] Aprovação final registrada |
| cancelar | [SolicitacaoCompra@cancelar] Iniciando cancelamento | [SolicitacaoCompra@cancelar] Solicitação cancelada |

Para cada método M da tabela, especificar também:
- warning: [SolicitacaoCompra@M] Operação recusada | solicitacao_id: {id}; contexto reason com código seguro de validação, autorização ou estado.
- error: [SolicitacaoCompra@M] Falha ao concluir operação | solicitacao_id: {id}; contexto error_code, exception_type e correlation_id. Não passar a exceção bruta.
- Em criarRascunho antes de haver registro, substituir solicitacao_id por ator_id nos dois casos.
- Decisões de fluxo em aprovarComoGestor: info “[SolicitacaoCompra@aprovarComoGestor] Solicitação encaminhada ao diretor | solicitacao_id: {id}” ou “[SolicitacaoCompra@aprovarComoGestor] Aprovação final concluída | solicitacao_id: {id}”, somente para o ramo efetivado.
- Despacho em enviar/aprovarComoGestor: debug “[SolicitacaoCompra@M] Iniciando despacho da notificação | solicitacao_id: {id}”; info “[SolicitacaoCompra@M] Despacho da notificação aceito | solicitacao_id: {id}”; error “[SolicitacaoCompra@M] Falha ao despachar notificação | solicitacao_id: {id}”.
- Não logar sucesso de persistência antes do commit. Catch tratado é warning; catch que interrompe é error. Nova mensagem operacional de transporte dependerá de Q18.

## Mapeamentos

### Entradas e controle

Descrição/valor/centro vêm do formulário validado. Solicitante vem da sessão autenticada. Estado, identidade do aprovador, organização e transição vêm do servidor.
Valor de tela é normalizado para representação exata confirmada, sem float ou arredondamento silencioso. R$ 5.000 é a fronteira literal do card.
Aprovadores exibidos são identidades persistidas pela etapa, não o gestor atual consultado retroativamente. A visibilidade e conservação de ciclos anteriores continuam em Q8/Q11/Q16.

### Fluxo determinado

| Origem semântica | Ação | Destino semântico |
|---|---|---|
| Rascunho | Enviar | Aguardando gestor |
| Aguardando gestor | Gestor aprova, valor até R$ 5.000 | Aprovada final |
| Aguardando gestor | Gestor aprova, valor acima de R$ 5.000 | Aguardando diretor |
| Aguardando gestor | Gestor rejeita com justificativa | Rascunho |
| Aguardando diretor | Diretor aprova | Aprovada final |
| Rascunho devolvido | Solicitante corrige e reenvia | Aguardando gestor; decisões anteriores pendentes Q8 |
| Antes da aprovação final | Solicitante cancela | Cancelada; comportamento posterior pendente Q9 |
| Aprovada final | Editar, excluir ou cancelar | Recusar mutação |

Os rótulos são semânticos, não enum/schema aprovado. Rejeitada não deve virar uma fila terminal que impeça a correção pedida.

## Filosofia de Implementação

Execução futura mínima: reutilizar o domínio indicado em Q1, recursos nativos e padrões existentes, sem pacote de workflow, repositório genérico ou camada de eventos especulativa.
Ponytail será a skill de execução futura. Não foi executada auditoria do step 6 nesta sessão.
Prosa dos arquivos wiki permanece completa; o modo conciso da conversa não altera texto original ou decisões.
Baseline de testes no checkout base será necessária antes de código/commit; não existe baseline executável aqui.

## Testes

O arquivo 04 será derivado do 00 exclusivamente na etapa apropriada da feature-test-design, depois da revisão de planejamento. Nenhum CT, CT-B, teste, costura confirmada ou mutante foi criado nesta sessão.
A derivação deverá preservar obrigações fechadas e listar recortes abertos, usando a Superfície de UI e a Superfície Livewire. Não derivar esperado a partir deste PRD.
Factories de domínio só serão planejadas concretamente após Q1; não inventar estados de factory existentes.

## Verificação Final

Itens para execução futura, sem fechamento nesta sessão:
- [ ] Confirmar ambiente, versões instaladas, schema e rotas reais.
- [ ] Resolver Q1 e os recortes necessários por Adendo; não implementar RQ aberta.
- [ ] Executar a baseline em checkout base autorizado e registrar falhas por nome.
- [ ] Derivar testes pela etapa própria; incluir gravação por componente para create/edit.
- [ ] Executar testes afetados com php artisan test --compact e caminho específico.
- [ ] Executar vendor/bin/pint --dirty --format agent se houver PHP alterado.
- [ ] Verificar concorrência na pilha que reproduza o bloqueio real.
- [ ] Rodar regressão dos consumidores de infraestrutura modificada.
- [ ] Executar browser em série apenas se houver costura browser; npm run build é pré-requisito.
- [ ] Aplicar TIA somente com checkout git/driver e seleção compatível com as rules do projeto; não usar TIA como substituto da suíte de CI.
- [ ] Em mutation testing no Windows, usar .ai/skills/feature-wiki/scripts/pestw.cmd; registrar duração e sobreviventes.
- [ ] Medir queries com conjunto acima da paginação.
- [ ] Executar revisão independente, reconciliação e QA nas etapas autorizadas posteriormente.

## Commits

Nenhum commit possível ou solicitado aqui, pois .git está ausente.
Mensagens futuras candidatas: “:memo: compras: documenta fluxo de aprovação de solicitação”; “:sparkles: compras: adiciona fluxo de aprovação confirmado”.
A criação da wiki não representa aprovação de implementação.

