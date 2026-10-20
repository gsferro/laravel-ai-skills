# Plano de Ação — FERRO-812: Cupons de desconto

> Requisito: [00-requisito.md](00-requisito.md).
> Planejamento dos steps 0–4, em 2026-10-20. Nenhuma implementação autorizada nesta sessão.
> As propostas condicionais abaixo não resolvem perguntas abertas do solicitante.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma de cupons encontrada nas árvores de produção pesquisadas.
- **Motivo**: introduzir cadastro de cupons; aplicação depende de domínio de pedidos ausente.
- **Toca infra compartilhada?**: sim, futuramente `config/logging.php` e `database/seeders/PapeisSeeder.php`.
- A mudança de matriz força regressão dos consumidores de permissões, independentemente do tipo “nova”.
- Referências de produção: `wikis/specs/main/perfil-e-acesso-ao-painel/`, `wikis/specs/main/admin-da-organizacao/` e `wikis/specs/feature/multi-tenancy/organizacoes/`. São contexto, não requisito novo de cupons.

## Cobertura do Requisito

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | Disponibilizar criação de cupons no painel. | 2, 4 | Obrigação preservada; painel/escopo pendentes Q2. |
| RQ-02 | Cupom deve possuir código. | 2, 4 | Unicidade obrigatória; recortes Q2/Q11/Q12 pendentes. |
| RQ-03 | Cupom deve permitir os tipos porcentagem e valor fixo. | 2, 4 | Tipos expressos no card; nenhuma terceira opção. |
| RQ-04 | Cupom deve possuir valor de desconto. | 2, 4 | Campos obrigatórios preservados; fronteiras Q8–Q10 pendentes. |
| RQ-05 | Cupom deve possuir data de validade. | 2, 4 | Campos obrigatórios preservados; fronteiras Q8–Q10 pendentes. |
| RQ-06 | Cupom deve possuir limite de usos. | 2, 4 | Campos obrigatórios preservados; fronteiras Q8–Q10 pendentes. |
| RQ-07 | Somente admin pode criar cupom. | 3, 4 | Permissões separadas; recortes Q2–Q5/Q15/Q16 pendentes. |
| RQ-08 | Somente admin pode editar cupom. | 3, 4 | Permissões separadas; recortes Q2–Q5/Q15/Q16 pendentes. |
| RQ-09 | Somente admin pode excluir cupom. | 3, 4 | Permissões separadas; recortes Q2–Q5/Q15/Q16 pendentes. |
| RQ-10 | Outros usuários podem listar cupons, sem gestão de cupons. | 3, 4 | Direito à listagem preservado; recortes Q2/Q7/Q13 pendentes. |
| RQ-11 | Listagem dos outros usuários deve conter somente cupons ativos. | 4 | **Bloqueado por**: RQ-11 (aberta — Q6) |
| RQ-12 | Aplicação no pedido deve validar a existência do cupom. | 5 | **Bloqueado por**: RQ-12 (aberta — Q1) |
| RQ-13 | Aplicação no pedido deve validar a validade do cupom. | 5 | **Bloqueado por**: RQ-13 (aberta — Q1) |
| RQ-14 | Aplicação no pedido deve validar o limite de usos. | 5 | **Bloqueado por**: RQ-14 (aberta — Q1) |
| RQ-15 | Com as validações satisfeitas, aplicar desconto no total do pedido. | 5 | **Bloqueado por**: RQ-15 (aberta — Q1) |
| RQ-16 | Aplicação bem-sucedida deve incrementar contador de usos. | 5 | **Bloqueado por**: RQ-16 (aberta — Q1) |
| RQ-17 | Código do cupom não pode se repetir. | 2, 4 | Unicidade obrigatória; recortes Q2/Q11/Q12 pendentes. |
| RQ-18 | Registrar quem aplicou o cupom para auditoria. | 6 | **Bloqueado por**: RQ-18 (aberta — Q1) |
| RQ-19 | Registrar quando o cupom foi aplicado para auditoria. | 6 | **Bloqueado por**: RQ-19 (aberta — Q1) |
| P-01 | Não inventar domínio de pedidos enquanto Q1 estiver aberta. | 5, 6 | Restrição do planejamento; passos bloqueados. |

O passo 1 é infraestrutura dos logs dos passos 3–6 e atende indiretamente suas RQ.
Nenhuma obrigação aberta foi marcada “fora desta entrega” ou atendida por um motor desacoplado.
Os passos 5/6 são reservas bloqueadas: não especificam uma entidade fictícia de pedido nem autorizam implementá-la.
As partes determinadas dos campos, tipos, unicidade e permissões permanecem especificadas mesmo quando há recortes pendentes.

## Objetivo

Planejar cupons com código único, tipo, desconto, validade e limite de usos. Separar criação, edição e exclusão exclusivas de admin da listagem de ativos dos demais usuários.

O card também exige validar e descontar no pedido, incrementar usos e registrar ator/instante. Essas obrigações permanecem integrais, mas bloqueadas pela ausência de pedidos e pelas perguntas do `00`. Cadastro isolado não equivale à entrega do card completo.

## Contexto

O projeto é um starter kit com painéis de negócio, administração e infraestrutura. Existe `Projeto`, uma demonstração de tenancy com campo `nome`; não é um pedido, não tem total nem fluxo comercial. Não será renomeado nem usado como pedido.

`rg --files app/Models database/migrations routes app/Filament` e busca de palavras inteiras `cupom|cupons|coupon|coupons|pedido|pedidos|order|orders` nesses caminhos não localizaram domínio comercial; a ocorrência de “pedido” em comentário de convites é linguagem comum. A ausência foi confrontada também com os nomes das migrations. Q1 registra a fronteira de escopo.

## Análise dos Arquivos Existentes

### Versões e ambiente observados

`composer show --direct` retornou **“No dependencies installed. Try running composer install or update.”**.
Não há versões instaladas verificáveis. `composer.lock` registra Laravel v13.25.0, Filament v5.7.6, Livewire v4.4.0, Pest v5.1.1, browser plugin v5.0.1, plugin Laravel v5.0.1, PHPUnit 13.3.0, Boost v2.5.3, Shield 4.3.1, spatie/laravel-permission 8.3.0 e Auditing v14.0.6.
São versões **travadas**, não pacotes carregados nesta sessão.
`package.json` declara Playwright ^1.62.1; `package-lock.json` trava 1.62.1.
`Test-Path vendor` e `Test-Path node_modules` retornaram False. Não instalar dependências nesta execução.

### Padrões internos conferidos

- `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:form():54`, `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:table():59` e `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:getPages():64`: Resource com Schema/Table separados e páginas index/create/edit.
- `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60`: cadastro em modal para a demonstração; não prova equivalência com pedidos.
- `app/Models/User.php:canAccessPanel():74`: acesso ao painel pelo papel e contexto; autenticar não garante acesso a todos os painéis.
- `app/Providers/KitServiceProvider.php:configureGates():86`: `Gate::before` concede acesso geral ao master_global. Uma policy retornando false sozinha não desfaz esse bypass; Q3 precisa resolver a semântica do card.
- `database/seeders/PapeisSeeder.php:run():45` e `database/seeders/PapeisSeeder.php:permissoesDeAdministracaoDoApp():117`: panel_user recebe permissões de negócio por discovery. Registrar cupom sem recorte pode conceder escrita ao perfil comum.
- `database/seeders/ShieldPermissionsSeeder.php:gerarPara():58`: geração por painel, preservando policies existentes. A implementação futura deve verificar o resultado antes de sincronizar papéis.
- `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`: sem tenant a consulta é **global**, não uma barreira que falha fechado.
- `app/Filament/App/Resources/Users/UserResource.php:getEloquentQuery():121`: precedente de query que fecha sem tenant e cobre listagem, vínculo de rota e busca. Não copiar o model User nem seu relacionamento de posse para Cupom.
- `app/Traits/AuditsFillables.php:getAuditInclude():18`: auditoria só inclui fillable. Não prova registro de cada aplicação nem autoria de incremento feito por query.
- `database/migrations/2026_08_12_164915_create_audits_table.php:up():12`: estrutura de auditoria genérica com ator e timestamps; sem vínculo semântico próprio de aplicação de cupom.
- `config/logging.php:'autenticacao':101`: channel daily existente. Busca por `cupons-de-desconto` não encontrou channel da feature; busca por `trait.*Logging` em `app/Traits` não encontrou trait de formatação.
- `tests/Pest.php`: RefreshDatabase por suíte, helpers compartilhados de usuário/contexto, TIA local com base main e timeout browser de 20.000 ms.
- `database/factories/UserFactory.php:unverified():39`: estado disponível. `database/factories/TenantFactory.php:inativo():47` e `database/factories/TenantFactory.php:comIdentidadeVisual():39`: estados disponíveis. Não há factory de Cupom/Pedido no inventário.
- `routes/web.php` contém a página inicial; as rotas de painel vêm dos providers. `bootstrap/app.php` registra web/console/health, não API comercial.
- `routes/console.php` agenda saúde, expurgo de acesso e lembretes de convite. Nenhum fluxo existente aplica descontos.

### Limitações da pesquisa

Ferramentas Boost `search-docs`, `database-schema`, `database-query` e `browser-logs` não estão expostas no catálogo desta sessão. Não foram simuladas.
Schema real não foi consultado; migrations são evidência de estrutura prevista, não de banco migrado.
`php artisan route:list --except-vendor --no-interaction`, `php artisan model:show User --no-interaction` e `php artisan test --compact --no-interaction` falharam no bootstrap por ausência de `vendor/autoload.php`.
Não existe baseline verde nem lista validada de falhas de testes individuais. Nenhum teste chegou a carregar.
A ausência de `.git` impede histórico e baseline em checkout de main. `saida-p1` é pasta determinada pelo usuário, não branch criada.
`wikis/glossario.md` não existe. Nenhum termo ambíguo foi decidido; o significado de admin/ativo permanece nas perguntas. Nenhum glossário global será criado.

### Fontes oficiais usadas como fallback

Ausência de Boost é degradação da pesquisa, não dispensa de pesquisar a stack.
Documentação consultada em 2026-10-20:

- Laravel 13: [autorização](https://laravel.com/framework/docs/13.x/authorization), [validação](https://laravel.com/framework/docs/13.x/validation), [migrations](https://laravel.com/framework/docs/13.x/migrations), [transações](https://laravel.com/framework/docs/13.x/database) e [locks](https://laravel.com/framework/docs/13.x/queries). Fundamentam policies explícitas, validação de unicidade, constraints e escrita transacional.
- [Logging Laravel 13](https://laravel.com/framework/docs/13.x/logging): channel daily e contexto estruturado.
- Filament 5: [Resources](https://filamentphp.com/docs/5.x/resources/overview), [criação](https://filamentphp.com/docs/5.x/resources/creating-records), [edição](https://filamentphp.com/docs/5.x/resources/editing-records), [ações](https://filamentphp.com/docs/5.x/actions/overview) e [testes](https://filamentphp.com/docs/5.x/testing/testing-resources). Sustentam as assinaturas e os pontos de extensão abaixo.
- [Segurança Livewire 4](https://livewire.laravel.com/docs/4.x/security): estado público é entrada não confiável; autorizar ações no servidor.
- [Pest browser](https://pestphp.com/docs/browser-testing), [Pest TIA](https://pestphp.com/docs/tia) e [browsers Playwright](https://playwright.dev/docs/browsers): pesquisa do stack, sem derivar CT ou planejar CT-B nesta sessão.
- Source oficial do Filament na tag **v5.7.6**, consultado em memória, sem gravar vendor: CreateRecord, EditRecord, InteractsWithRecord, InteractsWithActions, CanSearchRecords, CanSortRecords e HasFilters. Links e linhas estão no inventário Livewire do `02`. Não equivalem à execução de pacote instalado.

## Decisões de Desenho

| # | Decisão | Pergunta / autorização | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Usar nomenclatura Cupom/cupons, tabela explícita e lista fechada porcentagem/valor_fixo, sem criar pasta de enums. | Card, convenções do projeto e autorização para planejar. | Surpreendente; é convenção rotineira. | Sessão, 2026-10-20. |
| D2 | Usar Resource/Schema/Table e páginas nativas, sem biblioteca adicional ou motor genérico. | Convenções conferidas; rotas/painéis condicionais a Q2. | Difícil de reverter. | Sessão, 2026-10-20. |
| D3 | Propor gravação síncrona e transacional de desconto, uso e auditoria quando houver contrato de pedido. | RQ-14–RQ-16/RQ-18/RQ-19; implementação bloqueada por Q1. | Surpreendente. | Sessão, proposta técnica em 2026-10-20. |
| D4 | Propor registro relacional de cada uso, separado do log operacional e da auditoria dos campos editáveis. Não criar ainda. | RQ-18/RQ-19; Q1/Q15 pendentes. | Surpreendente: evento de negócio exige persistência própria quando CRUD não o representa. | Sessão, proposta técnica em 2026-10-20. |
| D5 | Channel cupons-de-desconto com daily/14 dias e allowlist de contexto, sem trait nova. | Convenção de logs e padrão obrigatório da skill. | Surpreendente; sem trade-off de arquitetura. | Sessão, 2026-10-20. |
| D6 | Priorizar testes de componente para formulário, gravação e autorização; decidir browser somente no step 7. | Convenção dos testes e gate de CT-B da skill. | Difícil de reverter. | Sessão, 2026-10-20. |

Nenhuma decisão técnica altera respostas de domínio pendentes. Não há escolha material adicional de desenho a enviar ao desenvolvedor nesta rodada.

## Autorização

- Criar futuramente `app/Policies/CupomPolicy.php`, com `viewAny(User $user): bool`, `view(User $user, Cupom $cupom): bool`, `create(User $user): bool`, `update(User $user, Cupom $cupom): bool`, `delete(User $user, Cupom $cupom): bool` e negativa explícita dos métodos de escrita não oferecidos.
- Direitos determinados: admin cria/edita/exclui; demais usuários apenas listam ativos. Definir os recortes Q2–Q7 antes de ligar as superfícies.
- Não confiar só em menu oculto, UUID, papel do painel ou filtro da tabela. A query de Resource e a autorização precisam cobrir acesso direto e requests Livewire subsequentes.
- Preservar guard web e middleware de autenticação/CSRF dos providers. Não alterar Gate global para uma pergunta ainda aberta.
- Recalcular permissões dos cupons no seeder por entidade e método, sem comparação por substring. Não retirar todas as permissões do cupom de panel_user: preservar ViewAny e a leitura autorizada; retirar apenas escrita.
- Se admin_organizacao continuar fora do significado de admin, também recortar sua matriz, que hoje herda tudo no app. Não equiparar papéis pelo nome.
- Aplicar cupom exige autorização do ator e do pedido, ainda indefinida em Q13; não registrar endpoint aberto.

## Rotas

São propostas condicionais a Q2; nenhum endpoint foi registrado ou validado por route:list.

| Método | URI proposta | Name previsto | Middleware / barreira |
|---|---|---|---|
| GET | /admin/cupons | filament.admin.resources.cupons.index | Painel admin, auth web, viewAny e query autorizada. |
| GET | /admin/cupons/create | filament.admin.resources.cupons.create | Painel admin, auth web, create. |
| GET | /admin/cupons/{record}/edit | filament.admin.resources.cupons.edit | Painel admin, auth web, update e vínculo de registro escopado. |
| GET | /app/cupons ou /app/{tenant}/cupons | filament.app.resources.cupons.index | Painel app, auth web, tenant quando habilitado, viewAny e somente ativos para não admin. |

Gravação/exclusão usam ações Livewire nativas, sem criar POST/DELETE REST em paralelo.
Aplicação no pedido: **sem rota proposta enquanto Q1/Q13 estiverem abertas**.
Não são links de app servido; compartilhar URL efetiva exige `get-absolute-url` quando disponível.

## Superfície de UI

| Tela / Componente | Tipo | Rota proposta | Interação | Depende de JS? |
|---|---|---|---|---|
| ListCupons da gestão | Filament | /admin/cupons | Listar registros permitidos, abrir criação/edição e excluir conforme policy. | Sim. |
| CreateCupom | Filament | /admin/cupons/create | Informar os campos exigidos e gravar. | Sim. |
| EditCupom | Filament | /admin/cupons/{record}/edit | Editar e gravar; exclusão com autorização. | Sim. |
| ListCupons da operação | Filament | /app[/tenant]/cupons | Listar somente ativos; sem ações de escrita para perfil comum. | Sim. |
| Aplicação no pedido | Ainda indefinido | Não definida | Bloqueada por Q1/Q13; não criar tela de pedido. | A definir. |

O step 7 deverá derivar testes de gravação por componente para ambas as rotas create/edit.
Esta tabela não cria automaticamente CT-B: não há requisito explícito de layout, tema ou JavaScript cujo oráculo exija navegador.
Nenhum arquivo 04/05 é criado agora.

## Variáveis de Ambiente

Nenhuma chave nova proposta. `KIT_TENANCY`, `DB_CONNECTION` e `APP_TIMEZONE` são configuração existente, não decisões de negócio.
`.env.example` mostra tenancy false e America/Sao_Paulo; isso não prova configuração efetiva nem responde Q2/Q8.

## Eventos / Listeners / Observers

Sem evento, listener, notificação ou observer próprios novos planejados para executar desconto.
Reutilizar auditoria CRUD do projeto quando apropriado; ela não substitui registro de cada aplicação.
Não depender de evento Eloquent para detectar incremento por query, pois esse caminho pode não dispará-lo.
As notificações efêmeras de salvamento do Filament não criam uma nova comunicação de negócio.

## Jobs / Queues

Nenhum job novo. Aplicação de desconto, contador e trilha não serão eventualmente consistentes entre jobs.
Nenhum requisito pede sincronização externa, envio de e-mail ou scheduler de expiração.

## Modelo de Execução

Proposta: um request de gravação por comando de usuário, sem trabalho adiado.
O GET inicial renderiza a página e ações subsequentes geram requests Livewire; não se promete que toda a navegação ocorre num único request.
Sem polling, widget lazy, cache de elegibilidade ou memoização entre requests acrescentados.
Listagem usa paginação; busca/filtro preservam o mesmo recorte da query base. Não hidratar a coleção inteira.
A aplicação futura deve reler saldo e validade na transação, nunca confiar em resultado da listagem.
Custo real de queries e N+1 ainda não medido: app não inicializa. Medir com volume acima da página antes de concluir implementação.
Nenhuma contagem numérica de consultas foi inventada.

## Impacto em Features Existentes

- Matriz de papéis: risco de conceder escrita a panel_user/admin_organizacao por discovery. Regressão obrigatória de acesso a painéis e administração da organização.
- Tenancy: a trait existente abre consulta global quando não há tenant. Se Q2 escolher isolamento, adicionar guarda explícita no caminho que recebe o usuário, sem mudar a trait global por conveniência.
- Spotlight e badge: consultas devem usar o Resource escopado; cupons inativos de usuário comum não podem reaparecer na busca/contagem.
- Auditoria: alteração de fillable não pode expor formulário, código promocional ou dados pessoais em log operacional.
- Pedido: integração não pode ser dimensionada sem Q1; nenhum módulo comercial existente foi encontrado.

## Rollback

Na implementação futura, retirar descoberta/rotas da feature e recompor a matriz de permissões antes de remover estrutura.
Migration de cupons só deve ter down destrutivo em ambiente descartável ou sem dados: após usos reais, exportar/preservar trilha e avaliar Q15 antes de qualquer drop.
Não usar cascade que apague ator/histórico por conveniência. Não alterar totais de pedidos retroativamente como “rollback de código”.
Sem feature flag adicional proposta; a ausência de integração enquanto bloqueada já impede efeitos comerciais.
Nenhum rollback foi executado.

## Dependências

Nenhuma dependência nova proposta e nenhuma instalação autorizada nesta sessão.
Antes de implementar, restaurar o ambiente conforme locks sob autorização adequada e confirmar versões com `composer show --direct`.
Browser plugin e Playwright já constam nos manifests/locks; não propor `composer require` como se estivessem ausentes do contrato.
Se uma costura browser for confirmada no step 7, verificar browsers baixados, build Vite e referência do plugin nessa etapa.
Antes de testes, obter baseline num checkout válido sem ler/executar os testes proibidos desta rodada.

## Riscos

- Pedidos ausentes: não “resolver” entregando apenas um motor; manter Q1 aberta.
- Fronteira de tenant e admin não decidida: não registrar telas que abram dados/permissões por padrão.
- Último uso concorrente: validação seguida de incremento fora de transação permite exceder limite; mecanismo futuro no passo 5.
- SQLite de teste não prova locking do banco de produção. Verificação concorrente deve usar motor apropriado quando definido.
- Dinheiro: não escolher float, arredondamento, moeda ou total-base sem Q9/Q10.
- Edição/exclusão após uso: risco de destruir trilha; Q15/Q16 pendentes.
- Pesquisa sem ambiente instalado: assinaturas remotas são apoio, não prova de compatibilidade executada.

## Channel de Log da Feature

`rg -n -F 'cupons-de-desconto' config/logging.php` não retornou ocorrência.
Criar futuramente esse channel antes de instrumentar métodos.
Driver daily, path `storage/logs/cupons-de-desconto.log`, level debug, days 14 e replace_placeholders true.
Essa retenção refere-se somente ao log operacional; não responde retenção de auditoria em Q15.
Não foi encontrada trait de logging; usar Facade Log diretamente com prefixo.
Todos os logs dos passos abaixo usam `Log::channel('cupons-de-desconto')`.

Allowlist comum: `cupom_id`, `pedido_id`, `executor_id`, `tenant_id` quando definidos, `operation`, `result`, `reason`, `error_code`, `exception_type` e contagens.
Não registrar código em claro, formulário, total bruto de model, nome/e-mail, tokens, payload ou exceção bruta.
Mensagem usa placeholders dos IDs seguros, resolvidos pelo logger.

## Estrutura de Implementação

### 1. Configurar channel de log da feature

- **Atende**: RQ-07–RQ-19, infraestrutura de observação dos passos 3–6.
- **Path futuro**: `config/logging.php`.
- Acrescentar somente o channel descrito acima; não alterar defaults dos demais.
- **Skills futuras**: `ponytail`; não ativada para codificar nesta sessão.
- **Logs**: configuração estática, sem emissão durante carregamento de config. Verificar o destino com execução real dos métodos instrumentados nos passos 3–6; não inventar classe de serviço só para logar config.

### 2. Preparar persistência e contrato do cupom

- **Atende**: RQ-01–RQ-06, RQ-17.
- **Paths futuros**: `app/Models/Cupom.php`, `database/factories/CupomFactory.php` e `database/migrations/2026_10_20_000001_create_cupons_table.php`.
- Não criar pasta de enums para duas opções; usar a lista fechada na validação e no Select, com uma definição compartilhada no model.
- Gerar arquivos com comandos Artisan e `--no-interaction` após conferir `--help`; timestamp de migration acima é nome planejado, ajustar ao gerador antes da execução.
- `Cupom extends Model`; `protected $table = 'cupons'`; seguir UUID público com `TemUuid` e factories de teste. Definir as opções porcentagem e valor_fixo no model e validar com lista fechada Laravel.
- Fillable só para os campos editáveis do card; contador e tenant/autor nunca aceitos do cliente.
- Contrato proposto de schema:

| Campo | Tipo proposto | Nulo / default | Índice ou restrição |
|---|---|---|---|
| id | big integer auto incremento | não | PK |
| uuid | uuid | não | unique |
| codigo | string, comprimento a confirmar Q12 | não | unique; escopo Q2 e equivalência Q11 pendentes |
| tipo | string de domínio fechado | não | porcentagem ou valor_fixo |
| valor | decimal, precisão/escala pendentes Q9/Q10 | não | limites confirmados no servidor |
| validade | date, ou instante caso Q8 assim defina | não | comparação temporal única |
| limite_usos | unsigned big integer | não | domínio positivo/zero pendente Q9 |
| usos | unsigned big integer | não, default 0 | alterado somente pela aplicação confirmada |
| created_at / updated_at | timestamps | conforme convenção Laravel | técnicos |
| tenant_id | somente se Q2 definir posse | a definir | FK/índice conforme fronteira confirmada |

- **Recortes bloqueados**: Q2/Q8–Q12. Não executar migration/model final com collation, campo de posse ou precisão escolhidos por suposição.
- Unicidade deve ser validada no servidor e garantida por índice, inclusive na corrida de duas criações. Na edição, ignorar somente o próprio registro resolvido pelo servidor.
- **Skills futuras**: `ponytail`; ativar domínio Eloquent/Laravel disponível no ambiente de implementação.
- **Logs**: migration/model declarativos não geram eventos operacionais próprios; gravações CRUD são instrumentadas no passo 4. Se houver rejeição no contrato compartilhado, warning `[Cupom@validarDados] Dados do cupom recusados | cupom_id: {cupom_id}`, contexto `cupom_id,reason,error_code`; esse método só será necessário se existir caminho de escrita além do componente. Não adicionar camada abstrata sem chamador.

### 3. Definir autorização e matriz de permissões

- **Atende**: RQ-07–RQ-10.
- **Paths futuros**: `app/Policies/CupomPolicy.php`, `database/seeders/PapeisSeeder.php` e eventuais registros estritamente necessários no provider já existente, sem mudar Gate global.
- Usar os métodos explicitados em Autorização. Admin canônico é caso determinado; equivalência dos demais papéis e combinações aguardam Q3–Q5.
- **Recortes bloqueados**: Q2–Q5. Não sincronizar concessões de cupom por herança genérica.
- Gerar permissions com ShieldPermissionsSeeder e depois sincronizar PapeisSeeder, como a rule do projeto manda; revisar o recorte antes de disponibilizar o Resource.
- Preservar leitura autorizada do usuário comum e bloquear escrita, inclusive chamadas diretas. Não classificar cupom como administração de usuários para excluir toda a sua leitura.
- **Skills futuras**: `ponytail`; domínio de autorização Laravel/Filament disponível no ambiente.
- **Logs**: na negativa dos métodos create/update/delete da CupomPolicy, warning `[CupomPolicy@{metodo}] Operação em cupom negada | executor_id: {executor_id}`, contexto `executor_id,cupom_id,operation,reason`. Explicitar cada prefixo real ao implementar. Não logar cada consulta de listagem em nível info; apenas a decisão de fronteira inválida no passo 4.

### 4. Construir gestão e listagem no painel

- **Atende**: RQ-01–RQ-11, RQ-17.
- **Bloqueado por**: RQ-11 (aberta — Q6). Isso bloqueia o predicado de ativos e sua publicação para usuário comum, não os campos/permissões determinados.
- **Outros recortes bloqueados**: Q2–Q5/Q7–Q12/Q15/Q16, conforme cada operação.
- **Paths futuros propostos**, condicionais ao aceite de Q2:
  - `app/Filament/Admin/Resources/Cupons/CupomResource.php`;
  - `app/Filament/Admin/Resources/Cupons/Schemas/CupomForm.php`;
  - `app/Filament/Admin/Resources/Cupons/Tables/CuponsTable.php`;
  - `app/Filament/Admin/Resources/Cupons/Pages/ListCupons.php`;
  - `app/Filament/Admin/Resources/Cupons/Pages/CreateCupom.php`;
  - `app/Filament/Admin/Resources/Cupons/Pages/EditCupom.php`;
  - `app/Filament/App/Resources/Cupons/CupomResource.php`;
  - `app/Filament/App/Resources/Cupons/Pages/ListCupons.php`.
- Usar gerador Filament após confirmar opções; Resources são descobertos pelos providers existentes. Não criar painel novo.
- Assinaturas: `form(Schema $schema): Schema`, `table(Table $table): Table`, `getPages(): array` e `getEloquentQuery(): Builder`; Schema/Table auxiliares com `configure` estático.
- Formulário: TextInput codigo; Select tipo com lista fechada; TextInput valor; DatePicker/DateTimePicker conforme Q8; TextInput limite_usos inteiro. Sem campo editável usos, executor, tenant ou total de pedido.
- Criação/edição usam classes CreateRecord/EditRecord, com `handleRecordCreation(array $data): Model` e `handleRecordUpdate(Model $record, array $data): Model` apenas quando a validação/gravação exigir adaptação. Evitar sobrescrever método público create/save só para log.
- Listar código, tipo, valor, validade e saldo/contador autorizado. Não inventar filtro com parse livre de datas. Em todos os caminhos, aplicar query base autorizada; o cliente não escolhe colunas ou operadores.
- Se Q2 confirmar tenancy, recusar ausência de tenant no caminho de usuário; não confiar no comportamento aberto da trait. Se confirmar cupons globais, configurar explicitamente o escopo compatível do Resource no app.
- Erros: validação mantém formulário com erro de campo; duplicidade do índice vira erro de codigo sem SQL bruto; autorização negada usa resposta legível do painel, com saída para listagem/painel autorizado.
- **Skills futuras**: `ponytail`; domínio Filament/Livewire disponível no ambiente.
- **Logs**:
  - beforeCreate/beforeSave: debug `[CreateCupom@beforeCreate] Iniciando cadastro do cupom | executor_id: {executor_id}` e `[EditCupom@beforeSave] Iniciando edição do cupom | cupom_id: {cupom_id}`.
  - afterCreate/afterSave: info `[CreateCupom@afterCreate] Cupom cadastrado | cupom_id: {cupom_id}` e `[EditCupom@afterSave] Cupom atualizado | cupom_id: {cupom_id}`.
  - ação delete após sucesso: info `[EditCupom@excluir] Cupom excluído | cupom_id: {cupom_id}`; ligar ao callback real da ação, sem criar método público desnecessário.
  - query sem contexto obrigatório: warning `[CupomResource@getEloquentQuery] Consulta de cupons recusada | executor_id: {executor_id}`, reason `contexto_ausente`.
  - validação/rejeição: warning `[CreateCupom@onValidationError] Cadastro do cupom recusado | executor_id: {executor_id}`, reason/error_code; confirmar hook disponível antes de instrumentar.
  - catch que interrompe gravação: error `[CreateCupom@handleRecordCreation] Falha ao gravar cupom | executor_id: {executor_id}`; equivalente da edição com EditCupom@handleRecordUpdate.
  - contexto por evento: `executor_id,cupom_id,tenant_id,operation,result,reason,error_code,exception_type`, somente chaves aplicáveis. Nunca formulário/código bruto.

### 5. Integrar aplicação ao pedido

- **Atende**: RQ-12–RQ-16, P-01.
- **Bloqueado por**: RQ-12 (aberta — Q1).
- **Bloqueado por**: RQ-13 (aberta — Q1).
- **Bloqueado por**: RQ-14 (aberta — Q1).
- **Bloqueado por**: RQ-15 (aberta — Q1).
- **Bloqueado por**: RQ-16 (aberta — Q1).
- Q8–Q10/Q13/Q14/Q16 acrescentam recortes de validade, dinheiro, ator, repetição e edição.
- **Paths**: nenhum caminho de pedido existente encontrado; não criar migration/model/resource de pedido. Reserva condicional de orquestração em `app/Support/AplicarCupom.php` somente após Q1, com nome, parâmetros, retorno e chamadores preenchidos a partir do contrato real.
- **Não executar**: não construir um motor que receba “total qualquer” e alegar integração ao pedido.
- Depois da resposta, registrar Adendo antes de completar o plano. Localizar total oficial, relação de proprietário, conexão de DB e ponto de autorização; só então definir assinatura.
- Restrição determinada: consultar cupom existente, verificar validade e saldo atuais; sucesso altera total e incrementa exatamente um uso. Falha não pode produzir parte desses efeitos.
- Proposta técnica para a futura especificação: transação única, lock do pedido e do cupom em ordem consistente, releitura antes do desconto, gravação do total/contador/trilha e commit único. Alternativa de update condicional só se mantiver a mesma atomicidade. Último uso não pode ser concedido a duas operações.
- Nenhuma escolha de retentativa/cancelamento vira comportamento aceito sem Q14.
- **Skills futuras**: `ponytail`; domínio de transações Laravel disponível no ambiente.
- **Logs futuros condicionais**, no channel da feature: debug `[AplicarCupom@executar] Iniciando aplicação do cupom | pedido_id: {pedido_id}`; warning `[AplicarCupom@executar] Aplicação do cupom recusada | pedido_id: {pedido_id}` com reason seguro; info após commit `[AplicarCupom@executar] Cupom aplicado | pedido_id: {pedido_id}`; error após rollback `[AplicarCupom@executar] Falha ao aplicar cupom | pedido_id: {pedido_id}`. Contexto `pedido_id,cupom_id,executor_id,tenant_id,result,reason,error_code,exception_type`. São rascunhos vinculados ao método ainda bloqueado, não implementação.

### 6. Registrar aplicação para auditoria

- **Atende**: RQ-18, RQ-19, P-01.
- **Bloqueado por**: RQ-18 (aberta — Q1).
- **Bloqueado por**: RQ-19 (aberta — Q1).
- Q15 bloqueia ciclo de vida/acesso da trilha; Q13 bloqueia definição do ator autorizado.
- **Paths futuros condicionais**: `app/Models/UsoCupom.php` e `database/migrations/2026_10_20_000002_create_usos_cupons_table.php`. Nenhum arquivo será criado antes de resolver relação de pedido e retenção.
- Propor `UsoCupom extends Model` com `$table = 'usos_cupons'`; PK, cupom_id, pedido_id com tipo/chave do domínio ainda ausente, executor_id e aplicado_em com timezone coerente. Actor/time são obtidos no servidor.
- Registrar cada aplicação confirmada dentro da mesma transação do passo 5. Não sobrescrever o usuário/data “do último uso” no cupom como se fosse histórico.
- Constraints, FKs e snapshots estritamente necessários dependem de Q1/Q15; não configurar cascade de histórico por padrão. Não criar tela de auditoria comercial porque o card só pede registrar.
- Auditoria genérica de criação/edição de Cupom pode reutilizar AuditsFillables; ela não prova esta trilha de uso. Não adicionar outro pacote.
- **Skills futuras**: `ponytail`; domínio Eloquent/auditoria disponível no ambiente.
- **Logs condicionais**: debug `[AplicarCupom@registrarUso] Registrando aplicação do cupom | cupom_id: {cupom_id}`; info de conclusão fica após commit no passo 5. Falha ao persistir trilha deve propagar rollback e error `[AplicarCupom@registrarUso] Falha ao registrar aplicação | cupom_id: {cupom_id}`, contexto `cupom_id,pedido_id,executor_id,error_code,exception_type`. Não capturar e ignorar erro de auditoria.

## Filosofia de Implementação

Na execução futura, ativar Ponytail full e reutilizar recursos nativos antes de adicionar abstrações.
Não há execução de Ponytail-review nesta rodada: esse passe é step 6 da skill e está fora do limite autorizado.
Arquivos desta wiki usam prosa completa; a compressão de conversa não se aplica aos documentos.
Não criar repositório, contrato genérico de pedido, cache, fila ou pacote para mascarar requisito em aberto.
Propostas bloqueadas devem ser completadas por resposta documentada, nunca por inferência do implementador.

## Mapeamentos

Campos do card correspondem a codigo, tipo, valor, validade e limite_usos.
Contador usos, ator e instante não vêm do formulário.
Mapa definitivo de total/desconto/pedido/usuário/organização depende de Q1/Q2/Q10/Q13.
Tipo de desconto permanece uma lista fechada com as duas opções literais do card.

## Testes

Nenhum caso ou código de teste é derivado nesta rodada. `04-casos-de-teste.md` pertence ao step 7, ainda não executado.
A derivação futura recebe o 00 como oráculo e a superfície Livewire do 02; RQ aberta não gera cenário.
O stack do projeto suporta componente Livewire e testes de banco, mas não foi executado por ausência de vendor.
No futuro, usar factories de usuário/tenant já existentes e criar factory de Cupom; não criar helper global duplicado.
A verificação da trilha é requisito do card; log operacional não deve virar oráculo substituto dessa trilha.

## Verificação Final

Todos os itens a seguir são futuros e permanecem pendentes:
- Conferir APIs e versões instaladas; obter schema e rotas reais.
- Completar perguntas, baseline e steps seguintes dentro de autorização nova.
- Derivar testes no step 7; executar mínimo afetado com `php artisan test --compact`.
- Rodar `vendor/bin/pint --dirty --format agent` quando houver PHP alterado.
- Verificar gravação por componente das páginas create/edit, autorização direta e persistência da trilha.
- Regressão de matriz de papéis/tenancy; respeitar escopo de leitura permitido.
- TIA só num repositório válido com driver de cobertura; suíte completa no CI, nunca TIA como substituta.
- Mutation no Windows somente via lançador da skill, se exigido pelos casos derivados e ambiente.
- Revisão independente, reconciliação e QA apenas nas etapas próprias, ainda não executadas.

## Commits

Não existe repositório Git nesta cópia. Não inicializar Git nem executar commit nesta rodada.
Quando houver checkout válido: `:memo: cupons: documenta planejamento de cupons de desconto`; commits de código somente após implementação autorizada.

