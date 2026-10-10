# Contrato público do laboratório

Fonte: somente os requisitos `wikis/specs/oraculo/{cupons-de-desconto,aprovacao-de-compra}/00-requisito.md` e a arquitetura pública dos respectivos `01-plano-acao.md`. Nenhum conjunto derivado foi lido pelo implementador. Essa declaração descreve as ações executadas; o filesystem do host é irrestrito e não impõe isolamento de leitura.

## Ambiente

PHP 8.4.10; Laravel 13.25.0; Filament 5.7.6; Livewire 4.4.0. `Composer\\InstalledVersions` e `vendor/composer/installed.json` registram Pest 5.1.1; o CLI mostra 5.0.5 porque `vendor/pestphp/pest/src/Pest.php::version()` retorna esse literal. SQLite testing; sem alteração de dependências. MCP Boost e PhpStorm indisponíveis: APIs verificadas no vendor instalado e nas documentações oficiais Laravel 13 e Filament 5.

## Cupons

- `App\\Enums\\TipoDeDesconto`: `Porcentagem = 'porcentagem'`, `Fixo = 'fixo'`; `getLabel(): string`.
- `App\\Models\\Cupom`: tabela `cupons`; `id`, `uuid`, `tenant_id` nullable, `codigo` string(40), `tipo` string(20), `valor` inteiro, `expira_em` timestamp, `limite_de_usos` inteiro, `usos` inteiro default 0, timestamps. Índice unique `(tenant_id,codigo)`. Route key `uuid`; código normalizado `mb_strtoupper(trim(...))`.
- Fillable: `codigo`, `tipo`, `valor`, `expira_em`, `limite_de_usos`. `tipo` enum; `expira_em` datetime. `usos`, `uuid`, `tenant_id` protegidos do mass assignment.
- `scopeAtivos(Builder $query): Builder`: validade estritamente futura e `usos < limite_de_usos`.
- `situacao(): string`: `Esgotado`, `Expirado` ou `Ativo`.
- `static valido(?string $codigo): ?self`: código normalizado, dentro do contexto de tenant; vazio/inexistente/inativo retorna null.
- `descontoSobre(int $valorTotalEmCentavos): int`: fixo em centavos; percentual inteiro 1..100, truncado. Valores totais negativos são recusados.
- `aplicarEm(int $valorTotalEmCentavos, ?User $aplicadoPor = null): int`: total final em centavos, mínimo zero; reconfere existência/validade/limite no UPDATE atômico e grava o uso na mesma transação. Falha de consumo lança `RuntimeException`.
- `App\\Models\\CupomUso`: tabela `cupom_usos`; `id`, `cupom_id` FK cascade, `aplicado_por_id` nullable FK users nullOnDelete, `valor_original`, `valor_desconto`, timestamps. Sem rota.
- `Database\\Factories\\CupomFactory`: default percentual 10%, validade +30 dias, limite100; estados `expirado()`, `esgotado()`, `fixo(int $centavos = 1000)`.
- Resource `App\\Filament\\App\\Resources\\Cupons\\CupomResource`; páginas `ListCupons`, `CreateCupom`, `EditCupom`. Slug `cupons`; rotas `filament.app.resources.cupons.{index,create,edit}`. URLs `/app/cupons` ou `/app/{tenant}/cupons`, criação `/create`, edição `/{uuid}/edit`.
- Policy pelas permissões Shield `ViewAny:Cupom`, `View:Cupom`, `Create:Cupom`, `Update:Cupom`, `Delete:Cupom` etc. `panel_user` e `diretor` recebem só leitura do cupom; listagem desses perfis contém só ativos. `admin_organizacao` recebe escrita no modo tenancy; `master_global` e `admin` mantêm herança Gate existente.

## Aprovação de compra

- `App\\Enums\\SituacaoSolicitacao`: `Rascunho`, `AguardandoGestor`, `AguardandoDiretor`, `Aprovada`, `Cancelada`, valores snake_case. `getLabel(): string`, `getColor(): string`, `emTransito(): bool` (apenas aguardando gestor/diretor). Rejeição é evento; retorna ao rascunho.
- `App\\Models\\CentroCusto`: tabela `centros_custo`; `id`, `uuid`, `tenant_id` FK obrigatório, `nome` string120, `gestor_id` nullable FK users restrict, timestamps; unique `(tenant_id,nome)`. Fillable nome/gestor_id; `gestor(): BelongsTo`.
- `App\\Models\\SolicitacaoCompra`: tabela `solicitacoes_compra`; `id`, `uuid`, `tenant_id`, `solicitante_id`, `centro_custo_id` FKs obrigatórias, `descricao` string255, `valor` decimal(12,2), `situacao` string30, timestamps; index `(tenant_id,situacao)`. Fillable `descricao`, `valor`, `centro_custo_id`. Casts valor decimal:2 e situação enum. Route key uuid. Relações `solicitante(): BelongsTo`, `centroCusto(): BelongsTo`, `etapas(): HasMany`, ordenadas por created_at/id.
- `App\\Models\\EtapaAprovacao`: tabela `etapas_aprovacao_compra`; `id`, `solicitacao_compra_id` FK cascade, `etapa` string20 (`gestor`/`diretor`), `decisao` string20 (`aprovada`/`rejeitada`), `decidido_por_id` FK users, `justificativa` nullable text, timestamps. Fillable etapa/decisao/decidido_por_id/justificativa. Relações `solicitacao(): BelongsTo`, `decididoPor(): BelongsTo`. Sem rota.
- `exigeDiretor(): bool`: valor estritamente maior que config `kit.compras.limite_diretor` (default5000.00).
- `etapaPendente(): ?string`: gestor/diretor/null.
- `podeSerDecididaPor(?User $user): bool`: gestor do centro na etapa gestor; diretor com papel atribuído na organização da solicitação na etapa diretor.
- `aprovadoresDaVez(): Collection`: gestor ou todos os diretores da organização da solicitação; resolve no request, restaura o contexto anterior de permissões.
- `enviar(User $autor): void`: exige solicitante+rascunho+gestor; aguarda gestor e notifica por e-mail o gestor. Sem gestor, RuntimeException e fica rascunho.
- `aprovar(User $aprovador): void`: exige aprovador atual; grava etapa aprovada; aguarda diretor se acima do limite, senão aprova final; notifica só se houver próxima etapa.
- `rejeitar(User $aprovador, string $justificativa): void`: exige aprovador atual e justificativa não vazia; grava rejeição e volta ao rascunho; histórico preservado.
- `cancelar(User $autor): void`: exige solicitante e estado em trânsito; cancela sem etapa de aprovação.
- `editar(array $dados, User $autor): void` e `excluir(User $autor): void`: exigem rascunho e solicitante; usados pelas páginas e ação de exclusão. UPDATE/DELETE condicionais e transições vencem só uma vez; recusa lança RuntimeException. Models também recusam save/delete de registro fora do rascunho.
- `Database\\Factories\\CentroCustoFactory`, `SolicitacaoCompraFactory`: defaults válidos; podem receber tenant_id/solicitante_id/situacao explicitamente como fixtures, pois Factory é unguarded. Centro de custo default cria gestor e tenant; solicitação default cria solicitante+centro e herda o tenant desse centro, em rascunho.
- Resource `App\\Filament\\App\\Resources\\CentrosCusto\\CentroCustoResource`: páginas `ListCentrosCusto`, `CreateCentroCusto`, `EditCentroCusto`; slug `centros-de-custo`; routes `filament.app.resources.centros-de-custo.{index,create,edit}`.
- Resource `App\\Filament\\App\\Resources\\SolicitacoesCompra\\SolicitacaoCompraResource`: páginas `ListSolicitacoesCompra`, `CreateSolicitacaoCompra`, `ViewSolicitacaoCompra`, `EditSolicitacaoCompra`; schemas `SolicitacaoCompraForm`, `SolicitacaoCompraInfolist`; table `SolicitacoesCompraTable`. Slug `solicitacoes-de-compra`; routes `filament.app.resources.solicitacoes-de-compra.{index,create,view,edit}`. View `/{uuid}`, edit `/{uuid}/edit`; com tenancy, prefixo `/app/{tenant}`.
- Ações de tabela `enviar`, `aprovar`, `rejeitar`, `cancelar`; rejeitar recebe `justificativa`. Form só descrição/valor/centro de custo. Histórico na view mostra etapa/decisão/decididoPor.name/created_at/justificativa.
- `App\\Notifications\\AprovacaoPendente` implements ShouldQueue: `__construct(public readonly SolicitacaoCompra $solicitacao, public readonly string $etapa)`, `via(object $notifiable): array` = mail, `toMail(object $notifiable): MailMessage`. URL via Resource::getUrl com panel app e tenant explícito. Resolvem-se destinatários antes de enfileirar; afterCommit.
- Policies `SolicitacaoCompraPolicy` e `CentroCustoPolicy` usam permissões Shield; update/delete solicitação exigem rascunho+dono. `panel_user`/`diretor` têm solicitação, sem administração de centro de custo. `diretor` tem roles.painel='app'.

## Fixtures e execução

Use os helpers existentes em tests/Pest.php, sem redefini-los: `tenant(...)`, `usuario(...)`, `usuarioCom(...)`, `papelNaOrganizacao(...)`, `usuarioComPapel(...)`, `noPainelDa(...)`. Para tenancy, use Tests\\TenancyTestCase antes das migrations, e fixe Filament::setCurrentPanel('app'), Filament::setTenant($tenant,isQuiet:true), PermissionRegistrar::setPermissionsTeamId($tenant->id). Associe usuários com `$tenant->users()->attach(...)` quando a tela exigir acesso ao tenant. Factories podem receber tenant_id, pois ignoram fillable; em model normal use forceFill para fixtures protegidas. Notificações podem ser observadas por Notification::fake, sem SMTP real.

Comandos (exclusivamente neste runtime descartável): a .env mantém DB_DATABASE=:memory:. Para Artisan em processos CLI separados use o arquivo SQLite de validação, com variáveis somente do processo PowerShell; isso não altera .env nem interfere com os testes em :memory:.

```powershell
$env:DB_CONNECTION = 'sqlite'
$env:DB_URL = ''
$env:DB_DATABASE = Join-Path (Resolve-Path '.').Path 'validation/artisan-validacao.sqlite'
if (-not (Test-Path -LiteralPath $env:DB_DATABASE)) { New-Item -ItemType File -Path $env:DB_DATABASE | Out-Null }
php artisan migrate --force --no-interaction
php artisan db:seed --class=Database\\Seeders\\ShieldPermissionsSeeder --no-interaction
php artisan db:seed --class=Database\\Seeders\\PapeisSeeder --no-interaction
php artisan route:list --path=app --except-vendor
php vendor/bin/pest tests/Feature/LaboratorioContratoTest.php --no-coverage --compact
php vendor/bin/pest tests/Kit/PaineisTest.php --no-coverage --compact
```

Suíte de contrato própria usa tests/Feature/LaboratorioContratoTest.php; logs de execução ficam validation/. Para os materializadores, use tests/ExperimentoReal ligada explicitamente a TenancyTestCase+RefreshDatabase em tests/Pest.php; a sessão root administra esse registro único. A pasta Feature continua usando TestCase singletenant do kit. O smoke próprio usa BrowserTenancy, já ligada ao TenancyTestCase. `KIT_TENANCY` deve estar decidido antes do bootstrap da aplicação; config permission.teams antes de migrar. Channels cupom e compras daily14; envs LOG_CUPOM_LEVEL, LOG_COMPRAS_LEVEL, KIT_COMPRAS_LIMITE_DIRETOR.

Limites: unicidade SQL `(NULL,codigo)` em singletenant não evita concorrência de duplicação fora do formulário; o formulário aplica scopedUnique. Smoke Chromium real executado somente para listagem ativa e histórico, inclusive ausência de erros JavaScript. Criação, edição e envio foram testados por Livewire. SMTP real e concorrência multiprocesso continuam não medidos. A integração do cupom deve passar User para identificar o ator: a assinatura nullable do 01 permite aplicação com ator nulo. Nenhum resultado comportamental DDR/tokens foi medido por esta implementação.

Fontes de API consultadas: vendor instalado, [Eloquent Laravel13](https://laravel.com/framework/docs/13.x/eloquent) e [Resources Filament5](https://filamentphp.com/docs/5.x/resources/overview).
