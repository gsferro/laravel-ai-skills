# Plano de Ação — FERRO-812: Cupons de desconto

> Requisito: [00-requisito.md](00-requisito.md). Planejamento produzido somente até o step 4 da feature-wiki 4.1.1. Não constitui autorização de implementação nem plano revisado pelo step 5.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma de cupons ou pedidos identificada nas wikis de produção pesquisadas.
- **Motivo**: o card introduz cadastro, permissões, aplicação e auditoria comercial ainda inexistentes.
- **Toca infra compartilhada?**: sim, configuração de logging e matriz de permissões. Isso exige regressão futura, mesmo sendo feature nova.
- **Branch de referência**: pasta `saida-p1-a`, informada pelo desenvolvedor. Não existe repositório Git; não há base ou histórico verificável.

## Cobertura do Requisito

“Planejado” não significa atendido. Bloqueios materiais não foram resolvidos por recomendação. Uma cláusula fechada pode ter recorte pendente sem perder suas obrigações determinadas.

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|---|---|---|---|
| RQ-01 | Cadastro no painel | 1, 2, 3, 4 | Painel e propriedade dependem de Q2/Q3. |
| RQ-02 | Código | 2, 4 | Campo determinado; formato e teto dependem de Q7. |
| RQ-03 | Porcentagem ou valor fixo | 2, 4 | Discriminante determinado, sem terceiro tipo. |
| RQ-04 | Valor do desconto | 2, 4 | Faixas Q6; moeda e precisão Q8. |
| RQ-05 | Data de validade | 2, 4 | Campo determinado; corte/fuso Q5. |
| RQ-06 | Limite de usos | 2, 4 | Limite determinado; domínio numérico Q6. |
| RQ-07 | Apenas admin cria | 3, 4 | Restrição determinada; persona e contexto Q2/Q3. |
| RQ-08 | Apenas admin edita | 3, 4 | Restrição determinada; persona e contexto Q2/Q3. |
| RQ-09 | Apenas admin exclui | 3, 4 | Restrição determinada; efeitos históricos Q12. |
| RQ-10 | Outros apenas listam | 3, 4 | Não conceder manutenção. Aplicação precisa Q9. |
| RQ-11 | Outros só veem ativos | 3, 4 | **Bloqueado por**: RQ-11 (aberta — Q4); fronteira Q3/Q13. |
| RQ-12 | Validar existência no pedido | 5 | **Bloqueado por**: RQ-12 (aberta — Q1). |
| RQ-13 | Validar validade no pedido | 5 | **Bloqueado por**: RQ-13 (aberta — Q1); corte Q5. |
| RQ-14 | Validar limite no pedido | 5 | **Bloqueado por**: RQ-14 (aberta — Q1); faixas Q6. |
| RQ-15 | Aplicar desconto ao total | 5 | **Bloqueado por**: RQ-15 (aberta — Q1); Q8/Q9/Q10. |
| RQ-16 | Incrementar usos | 5 | **Bloqueado por**: RQ-16 (aberta — Q1); Q10/Q11. |
| RQ-17 | Código não repetido | 2, 4 | Duplicata exata proibida; equivalência e reserva após exclusão Q7/Q12. |
| RQ-18 | Auditar quem aplicou | 5 | **Bloqueado por**: RQ-18 (aberta — Q1); desenho Q14, acesso histórico Q12/Q13. |
| RQ-19 | Auditar quando aplicou | 5 | **Bloqueado por**: RQ-19 (aberta — Q1); desenho Q14. |
| P-01 | Não criar domínio de pedidos sem resposta | 5 | Passo explicitamente bloqueado; motor isolado não substitui aplicação integrada. |

## Objetivo

Planejar o cadastro de cupons com seus campos expressos, proteção de manutenção por perfil e listagem restrita dos demais usuários. Preservar como obrigações a validação no pedido, o desconto no total, o contador de usos e a auditoria de ator e instante.

Não existe pedido ou checkout identificável no projeto. O planejamento não cria esse domínio e não transforma a entrega em “somente motor” por decisão técnica. Integração e auditoria da aplicação ficam bloqueadas até resposta do solicitante. As perguntas sobre limites, visibilidade e cálculo permanecem perguntas de requisito.

## Contexto

O projeto é um starter kit com três painéis, permissões Shield/Spatie, tenancy opcional e auditoria Eloquent. Há infraestrutura reutilizável, mas não há regra comercial de cupons. O padrão de permissões dos Resources pode conceder manutenção de uma entidade nova ao usuário comum; esconder botões não corrige essa concessão.

## Análise dos Arquivos Existentes

### Raia fato — descoberta pela sessão e pelo mapeamento delegado

| Fato confirmado | Evidência / efeito no plano |
|---|---|
| Não foram encontrados Pedido/Order/Checkout/Cupom/Venda nos locais estruturais de domínio. | `rg -n -i '\b(Pedido|Pedidos|Order|Orders|Checkout|Cupom|Cupons|Coupon|Coupons|Venda|Vendas)\b' app/Models app/Http routes database/migrations`: saída vazia, exit 1. Q1 bloqueia integração. |
| Busca ampliada encontrou palavras comuns, não domínio comercial. | Mesmo padrão em `app database routes config resources`: referências a pedidos de IA, `git checkout` e nome demonstrativo “App de vendas”. Não são models, totais ou fluxo de pedidos. |
| `admin` e `admin_organizacao` têm painéis e contextos distintos. | `database/seeders/PapeisSeeder.php:run():45`; atribuições globais e por organização não são intercambiáveis. Q2. |
| `panel_user` herda permissões de negócio não subtraídas. | `database/seeders/PapeisSeeder.php:run():45`; `database/seeders/PapeisSeeder.php:permissoesDeAdministracaoDoApp():117`. A lista atual cobre User e Convite; Cupom não estaria protegido. |
| Superadministrador vence gates antes da policy. | `app/Providers/KitServiceProvider.php:configureGates():86`, chamada `Gate::before` na linha 90. Não afirmar que uma policy negada barrará esse perfil sem resolver Q2. |
| Acesso ao painel não é acesso ao cupom. | `app/Models/User.php:canAccessPanel():74`, `app/Policies/ProjetoPolicy.php:viewAny():15`, `app/Policies/ProjetoPolicy.php:create():25`, `app/Policies/ProjetoPolicy.php:update():30`, `app/Policies/ProjetoPolicy.php:delete():35`. |
| Resource de negócio demonstra schema, UUID e scoping. | `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60`, `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`, `app/Filament/App/Resources/Projetos/ProjetoResource.php:getPages():91`. Não copiar unicidade por tenant para contrariar RQ-17. |
| Trait de tenant não fecha consulta sem contexto. | `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`. Não tratá-la como proteção suficiente para eventual fluxo fora do painel. |
| Existe exemplo de consulta que fecha sem tenant. | `app/Filament/App/Resources/Users/UserResource.php:getEloquentQuery():121`; aplicar o padrão à fronteira que Q3 confirmar, sem alterar a trait global. |
| Auditoria de preenchíveis não prova evento de aplicação. | `app/Traits/AuditsFillables.php:getAuditInclude():18`. Auditoria de CRUD e log técnico não substituem RQ-18/RQ-19. |
| Auditoria está configurada para eventos Eloquent e driver database. | `config/audit.php:'events':65`, `config/audit.php:'driver':160`, `config/audit.php:'console':203`. Ator do uso e persistência transacional ainda precisam desenho. |
| Não há channel da feature nem trait de logging encontrada. | `rg -n 'cupons-de-desconto' config/logging.php app`: saída vazia, exit 1; `rg -n 'trait.*Logging' app`: saída vazia, exit 1. Configurar primeiro; usar prefixo manual. |
| Infra compartilhada tem decisões de produção relevantes. | Lidas ADR-06 de `wikis/specs/main/admin-da-organizacao/02-decisoes-arquiteturais.md` e ADR-01/02 de `wikis/specs/feature/multi-tenancy/organizacoes/02-decisoes-arquiteturais.md`. Não ampliar papéis ou ativar tenancy por conveniência. |

### Ambiente e versões

`composer show --direct --no-interaction` retornou `No dependencies installed. Try running composer install or update.` Não há versões instaladas confirmadas. `Test-Path vendor` e `Test-Path .env` retornaram `False`. Não foi instalado pacote nem criado ambiente.

Versões **travadas**, obtidas de `composer.lock`: Laravel v13.25.0; Filament v5.7.6; Livewire v4.4.0; Pest v5.1.1; browser plugin v5.0.1; Boost v2.5.3; Spatie Permission 8.3.0; Owen Auditing v14.0.6. PHP local identificado como 8.4.10. Isso não prova inicialização do app ou compatibilidade operacional da instalação ausente.

`package.json` declara Playwright `^1.62.1`, Tailwind `^4.0.0`, Vite `^8.0.0`. `Test-Path node_modules/playwright` retornou `False`. Não foram confirmados browsers baixados.

`php artisan model:show User --no-interaction` e `php artisan route:list --except-vendor --no-interaction` falharam por ausência de `vendor/autoload.php`. Migrations e providers foram usados como evidência estática; não representam schema nem rotas efetivos de um app em execução. Boost `database-schema`, `database-query`, `search-docs` e `browser-logs` não estão expostos nesta sessão.

### Pesquisa de documentação e lacunas

A busca de ferramentas expostas por `boost|search_docs|database_schema|model.show` retornou lista vazia. A pesquisa oficial abaixo substitui a consulta indisponível, com degradação declarada. Não foi apresentada como resultado de `search-docs`.

- [Laravel 13 — autorização](https://laravel.com/docs/13.x/authorization): policies e precedência de `Gate::before`. Obriga conferir o superadministrador.
- [Laravel 13 — validação](https://laravel.com/docs/13.x/validation): unicidade e `Rule::unique()->ignore($record)` apenas com registro confiável; nunca ID enviado pelo cliente.
- [Laravel 13 — query builder](https://laravel.com/docs/13.x/queries#pessimistic-locking): transação e bloqueio são opções para proteger o limite de usos; prova no banco real permanece pendente.
- [Laravel 13 — logging](https://laravel.com/docs/13.x/logging): channel `daily`; o formato local seguirá os channels já existentes.
- [Filament 5 — Resources](https://filamentphp.com/docs/5.x/resources/overview): `getEloquentQuery(): Builder` participa das consultas de lista, registro e busca global. O filtro de ativos não pode existir apenas na tabela.
- [Filament 5 — criação](https://filamentphp.com/docs/5.x/resources/creating-records) e [edição](https://filamentphp.com/docs/5.x/resources/editing-records): hooks `handleRecordCreation(array $data): Model` e `handleRecordUpdate(Model $record, array $data): Model`. Criar redireciona; salvar edição não redireciona por padrão.
- [Livewire 4 — segurança](https://livewire.laravel.com/docs/4.x/security): parâmetros de ações e propriedades públicas são entradas não confiáveis. Revalidar e autorizar no servidor.
- [Pest 5 — lançamento oficial](https://pestphp.com/docs/pest5-now-available) e [browser testing](https://pestphp.com/docs/browser-testing): referências de versão e capacidades; não foram derivados cenários nesta etapa. A tentativa de abrir `/docs/test-impact-analysis` falhou; não validar flags desse recurso por essa tentativa.

Sem vendor, os greps de implementação de Filament, Shield e Auditing não podem confirmar detalhes internos. A superfície estática/proposta e a prova negativa estão no `02`; não há selo de fronteira comprovada.

## Decisões de Desenho

| # | Decisão | Pergunta / autorização | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Reutilizar policies, permissões e componentes nativos; não adicionar dependências nem outro painel. | Escopo de planejamento e convenções existentes. O painel existente escolhido ainda depende de Q2/Q3. | Não é surpreendente nem difícil de reverter. | Sessão, 2026-10-20. |
| D2 | Nomes candidatos: `Cupom`, `TipoDesconto`, `CupomPolicy`, `CupomResource`. Declarar tabela `cupons` explicitamente. | Escolha rotineira de nomenclatura; não define moeda ou fronteira. | Não há trade-off arquitetural durável. | Sessão, 2026-10-20. |
| D3 | Propor páginas separadas List/Create/Edit, compatíveis com Resources de cadastro do projeto. | Rotina de UI. O local das páginas está pendente do requisito. | Reversível e esperado. | Sessão, 2026-10-20. |
| D4 | Proposta: registro de uso dedicado, síncrono, na mesma transação da aplicação. Alternativa: evento customizado no Auditing existente com a mesma garantia. | Q14 — **sem resposta; proposta, não aceita**. Não instalar pacote nem implementar um caminho por silêncio. | Não avaliado como decisão aceita; falta conhecer o fluxo de pedido. | Recomendação da sessão, 2026-10-20; desenvolvedor indisponível. |
| D5 | Não criar cache, fila, abstração de repositório ou serviço genérico antes de existir necessidade. | Convenção de implementação mínima. | Reversível e esperado. | Sessão, 2026-10-20. |

### Rodada 1 — pergunta ao desenvolvedor

❓ Q14 · raia: desenho · afeta: RQ-18, RQ-19 · depende de: —
Para registrar o mesmo evento de aplicação com ator e instante, devemos usar um registro de uso dedicado ou customizar o Auditing existente?
➡️ Recomendação: registro `CupomUso` na mesma conexão e transação da aplicação, com ator obrigatório e instante do servidor. O Auditing atual cobre alterações de preenchíveis; sua configuração não prova um evento comercial por uso. A alternativa precisa demonstrar a mesma atomicidade e recuperação por aplicação antes de ser escolhida.

**Resposta**: ausente, desenvolvedor indisponível por instrução. D4 continua proposta. Esquema e APIs do histórico não estão aprovados. A recomendação não autoriza ampliar o comportamento de produto.

## Autorização

Criar `CupomPolicy` com assinaturas `viewAny(User $user): bool`, `view(User $user, Cupom $cupom): bool`, `create(User $user): bool`, `update(User $user, Cupom $cupom): bool` e `delete(User $user, Cupom $cupom): bool`. Políticas adicionais só se a UI expuser a ação; não habilitar restauração, replicação, reordenação ou exclusão em massa por geração automática.

As três operações de manutenção precisam negar não administradores, inclusive chamada direta de ação Livewire. A listagem exige autenticação e escopo permitido. Persona concreta, superadministrador, cumulação entre contextos e aplicação dependem de Q2/Q3/Q9; não alterar o `Gate::before` global sem resolver a exigência de produto.

Se o Resource estiver no painel `app`, ajustar a matriz em `PapeisSeeder` para não herdar mutações de Cupom em `panel_user`. Usar a entidade por FQCN e o mapa de ações de `Paineis`; preservar listagem, sem conceder `View` de histórico indevidamente. A lista de subtração integral de administração não deve eliminar a listagem exigida pelo card. Conferir se é necessário alterar `app/Support/Paineis.php` somente depois de ler sua API; não planejar refatoração global.

Após criar Resources, executar `ShieldPermissionsSeeder` antes de `PapeisSeeder`, com `--no-interaction`. Rever a policy gerada e a matriz final; não presumir que geração atende a restrição “só admin”. Guard e middleware permanecem os do painel existente (`web`/autenticação Filament), a confirmar em runtime após instalar o ambiente fora desta sessão.

## Rotas

Nenhuma rota foi registrada. São propostas de nomes gerados pelo Filament, condicionadas a Q2/Q3, não URLs verificadas.

| Método | URI candidata | Name candidato | Middleware |
|---|---|---|---|
| GET | `/app/cupons` ou `/app/{tenant}/cupons` | `filament.app.resources.cupons.index` | Pilha autenticada do painel; tenancy persistente quando habilitada. |
| GET | Mesma base, `/create` | `filament.app.resources.cupons.create` | Pilha do painel e autorização de criação. |
| GET | Mesma base, `/{record}/edit` | `filament.app.resources.cupons.edit` | Pilha do painel, resolução de registro autorizado e edição. |

Se Q2 exigir manutenção no painel `admin`, gerar seus nomes equivalentes sob `filament.admin.resources.cupons.*`, com URI `/admin/cupons`. Isso não permite deslocar os demais usuários para `/admin`; o desenho de listagem precisa ser revisto após a resposta. Não criar endpoint de aplicação, API ou checkout substituto. Usar named routes/`getUrl()` e consultar `get-absolute-url` quando disponível antes de compartilhar URL do app.

## Superfície de UI

| Tela / Componente | Tipo | Rota candidata | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| ListCupons | Filament / Livewire | `*.cupons.index`, painel pendente | Listar; admin acessa ações permitidas, demais somente ativos após Q4. | Sim |
| CreateCupom | Filament / Livewire | `*.cupons.create`, painel pendente | Preencher código, tipo, valor, validade e limite; submeter no servidor. | Sim |
| EditCupom | Filament / Livewire | `*.cupons.edit`, painel pendente | Editar campos permitidos; excluir conforme Q12. | Sim |
| Aplicação no pedido | Pendente de Q1 | Não definida | Aplicar e observar total somente depois de existir contrato de pedido. | Não confirmado |

No step 7, cada tela de escrita exigirá prova de gravação por componente, além de abertura. Não inferir necessidade de CT-B apenas porque há JS: a costura será decidida a partir do requisito. Nenhum `04` ou `05` foi criado. UI nativa simples não exige extra de design nesta etapa.

## Variáveis de Ambiente

Nenhuma chave nova proposta. Não ligar `KIT_TENANCY` nem alterar configuração de permissões como parte deste planejamento. `.env.example` tem default sem tenancy, mas não há `.env` para provar estado operacional.

## Eventos / Listeners / Observers

Nenhum evento customizado, listener ou observer novo confirmado. `AuditsFillables` pode cobrir CRUD após inspeção do pacote instalado, mas não será apresentado como prova de auditoria da aplicação. Q14 define como persistir esse evento sem depender de fila.

## Jobs / Queues

Nenhum job ou fila proposto. Aplicação, consumo e auditoria devem compartilhar uma unidade de sucesso; a estratégia técnica transacional é proposta para preservar os invariantes do card. Não emitir sucesso antes do commit.

## Modelo de Execução

| Pergunta | Resposta |
|---|---|
| Quantos requests a tela custa? | GET inicial e requests Livewire por submissão, busca, filtro ou paginação. Quantidade efetiva ainda não medida. |
| O que é adiado? | Nenhum polling, widget lazy ou processo em fila proposto. |
| O que é memoizado por request? | Nenhuma memoização nova. Não pressupor que estado de persona/tenant do request anterior permaneça válido. |
| O que é cacheado entre requests? | Nenhum cache novo da feature; não cachear elegibilidade ou saldo de usos. |
| Caminho da aplicação | Um comando transacional do futuro fluxo de pedido; request e classe chamadora dependem de Q1. |
| Custo em queries | Não medido. Listagem deve paginar e evitar N+1; medir acima de uma página após implementação. |

## Impacto em Features Existentes

Alterar `PapeisSeeder` exige regressão dos acessos a painéis, do papel comum, do administrador organizacional e do superadministrador. Referências de produção: perfil-e-acesso-ao-painel, admin-da-organizacao e organizacoes. A configuração de logging será aditiva. Não modificar scoping de User ou trait global para encaixar Cupom.

Auditoria existente possui configurações transversais de eventos, resolvers e console. Não mudá-las globalmente para produzir um evento de uso sem analisar impacto. O registro técnico rotativo não satisfaz retenção de negócio por si só.

## Rollback

Reverter registros de Resource e concessões de Cupom sem remover permissões de outras entidades; regenerar matrizes na ordem prevista. Migration do cadastro deve ter `down()` correspondente, mas remover tabelas apaga dados e não é restauração. Antes de qualquer rollback destrutivo, preservar cadastro e histórico conforme a resposta Q12. Não executar rollback nesta sessão. Não criar flag nem extra `05-rollback` para uma migração destrutiva ainda não autorizada.

## Dependências

Nenhuma adição ou atualização aprovada ou necessária no desenho atual. Restaurar dependências do lockfile será pré-requisito operacional de uma futura implementação, sob seu escopo próprio. O browser plugin já está declarado e travado; não planejar sua instalação como se estivesse ausente do projeto, nem chamá-lo instalado neste ambiente. `npm run build` precede browser conforme `composer test:browser`; `tests/Pest.php` usa RefreshDatabase e timeout de 20.000 ms. Factories existentes: User (estado `unverified`), Tenant (`comIdentidadeVisual`, `inativo`), Convite; nenhuma factory comercial localizada. CTs ainda não derivados.

## Riscos

- Integração de pedidos ausente: manter Q1 e todas as cláusulas dependentes bloqueadas; não declarar entrega parcial como card concluído.
- Excesso de permissões por seeder ou superadministrador: resolver Q2 e testar matriz efetiva, além da UI.
- Vazamento entre organizações ou de inativos por busca/badge/route binding: resolver Q3/Q4 e concentrar fronteira em consulta de Resource e aplicação no domínio.
- Concorrência no último uso e duplicação por reenvio: preservar limite sob escrita concorrente; Q10 define identidade/idempotência. SQLite de testes não prova bloqueio do banco de produção.
- Precisão, teto de texto e exclusão histórica indefinidos: nenhuma recomendação se torna implementação por falta de resposta.
- Ambiente sem dependências e sem Boost: APIs internas, schema efetivo, rotas e baseline não foram verificados. Não há resultado de teste verde.

## Channel de Log da Feature

Não foi encontrado channel `cupons-de-desconto`. O passo 1 o adicionará em `config/logging.php`: `daily`, arquivo `storage/logs/cupons-de-desconto.log`, nível `debug`, rotação de 14 dias, seguindo channels existentes. A duração do log técnico não decide retenção da auditoria Q12. Não criar trait genérica: nenhuma trait de logging foi localizada.

Todos os pontos abaixo usam `Log::channel('cupons-de-desconto')`. Mensagem `[Classe@Método] ação | identificador: valor - contexto: valor`. Allowlist: IDs internos necessários (`executor_id`, `cupom_id`, `pedido_id`, `tenant_id` quando existirem), operação, resultado, motivo enumerado seguro, contagem e correlação. Não copiar código do cupom, formulário, dados pessoais, exception bruta ou `getMessage()` para logs. Registro de ator da auditoria é requisito próprio, não dump de contexto.

## Estrutura de Implementação

Os passos abaixo são futuros. Suas partes bloqueadas são envelopes de trabalho, não especificação executável fechada. Reabrir o planejamento com respostas antes de fixar os elementos pendentes. Nenhum passo está autorizado a executar nesta sessão.

### 1. Configurar channel de log

- **Atende**: RQ-01, RQ-07, RQ-08, RQ-09, RQ-10, RQ-17, como infraestrutura da instrumentação dos passos de cadastro.
- **Path**: modificar `config/logging.php`, adicionando somente o channel descrito acima.
- **Lógica**: configuração aditiva, sem alterar o channel padrão ou as resoluções da auditoria.
- **Erros**: configuração inválida deve impedir a verificação; não trocar para log genérico silenciosamente.
- **Logs**: configuração não executa lógica de produto. Verificar resolução do channel na futura execução; mensagens são emitidas pelos métodos dos passos seguintes, nunca pelo carregamento do arquivo de config.
- **Skills futuras**: `ponytail`; guidance de logging Laravel disponível no host de execução. Não foram ativadas skills de implementação agora.

### 2. Modelar cadastro e unicidade de código

- **Atende**: RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-17.
- **Paths candidatos exatos**: `app/Models/Cupom.php`, `app/Enums/TipoDesconto.php`, `database/migrations/2026_10_20_000001_create_cupons_table.php`, `database/factories/CupomFactory.php`. Timestamp da migration é nome planejado; o gerador futuro deve reconciliar o nome real no plano.
- **Estrutura determinada**: classe `Cupom extends Model`, `$table = 'cupons'`; enum backed string `TipoDesconto` com cases TitleCase `Porcentagem` e `ValorFixo`; colunas para código, tipo, valor, validade, limite e contador. UUID técnico e chave numérica seguem `TemUuid`; `uuid` não entra em `$fillable`. Inicializar contador no servidor, não aceitá-lo do formulário.
- **Schema proposto e pendências**:

| Campo | Tipo / nulabilidade / constraint candidata | Condição |
|---|---|---|
| `id` | bigint autoincrement, PK, não nulo | Convenção de cadastro. |
| `uuid` | uuid não nulo, unique | Convenção `TemUuid`. |
| `codigo` | string não nula; índice unique no banco e validação no servidor | Tamanho/collation/canonicalização Q7; reserva após exclusão Q12. Não trocar por unique composto local sem decisão explícita. |
| `tipo` | string não nula, cast `TipoDesconto` e validação dos dois valores | Tokens internos `porcentagem` e `valor_fixo` são nomes técnicos propostos. |
| `valor` | número exato não nulo; não usar ponto flutuante binário | Inteiro escalado ou decimal e escala pendentes de Q6/Q8. Não fixar DECIMAL arbitrário. |
| `validade` | data ou timestamp não nulo | Tipo, fuso e corte dependem de Q5. |
| `limite_usos` | inteiro não nulo | Faixas, tamanho e possibilidade de ilimitado dependem de Q6. |
| `usos` | inteiro não nulo, default 0, fora de `$fillable` | Atualizado somente pela aplicação autorizada do passo 5. |
| `tenant_id` | FK/index, presença e nulabilidade pendentes | Não adicionar até Q3; se tenant obrigatório, nunca aceitar do cliente. |
| `created_at`, `updated_at` | timestamps Laravel | Convenção. |
| Exclusão | física ou lógica ainda não definida | Q12; não adicionar SoftDeletes por suposição. |

- **Recortes bloqueados**: persistência final por Q3/Q5/Q6/Q7/Q8/Q12. O discriminante de tipos e os campos obrigatórios permanecem no plano; não suspender ou excluir essas obrigações.
- **Validação**: campo por campo em camada reutilizável do cadastro, além do schema Filament; rejeitar tipo fora do enum. Unicidade precisa constraint para corrida, com erro tratável, sem aceitar identidade de `ignore()` do cliente. Nome e assinatura da camada reutilizável serão fixados quando os contratos de Q6/Q7/Q8 existirem; não gerar classe vazia agora.
- **Logs**: não logar accessor/cast/getter ou criação de factory. As gravações de cadastro serão instrumentadas em `CreateCupom::handleRecordCreation` e `EditCupom::handleRecordUpdate` do passo 4: início `debug`, sucesso `info`, validação `warning`, falha técnica `error`, no channel obrigatório.
- **Skills futuras**: `ponytail`, práticas Eloquent/PHP disponíveis na execução. Criar arquivos futuros com Artisan após `--help`, sem comandos de geração nesta sessão.

### 3. Proteger operações e ajustar permissões

- **Atende**: RQ-07, RQ-08, RQ-09, RQ-10, RQ-11.
- **Paths**: criar `app/Policies/CupomPolicy.php`; modificar `database/seeders/PapeisSeeder.php`. Reutilizar `database/seeders/ShieldPermissionsSeeder.php` e `app/Support/Paineis.php` sem alteração pré-decidida. A policy usa as assinaturas da seção Autorização.
- **Lógica determinada**: não administrador não cria, edita nem exclui. Não depender de `visible()`/menu. Conferir registro alcançado, persona e escopo a cada submissão. Remover concessão automática de mutação ao perfil de listagem preservando `ViewAny`.
- **Recortes bloqueados**: mapa de papéis/contextos Q2/Q3 e alcance histórico Q13. **Bloqueado por**: RQ-11 (aberta — Q4), especificamente a decisão de quais cupons um não administrador pode recuperar. Não implementar ramo “ativo” por recomendação.
- **Matriz determinada**: admin confirmado tem manutenção; demais não têm manutenção. Listagem dos demais é obrigação, mas seu conjunto depende de ativo e escopo. Permissões de aplicar não são inferidas dessa matriz.
- **Erros**: negar sem executar escrita e sem retornar registro fora da fronteira. Não converter falha em concessão genérica. Usar respostas nativas de autorização e entrada acessível de retorno ao painel permitido, sem ciclo de redirects.
- **Logs**: `CupomPolicy::create/update/delete/viewAny/view`, somente nas negativas e decisões relevantes, `warning` com `[CupomPolicy@{método}] Operação negada | executor: {id} - operação: {ação}`, contexto permitido `executor_id`, `cupom_id` quando conhecido, `reason`. Sucessos de escrita ficam no passo 4. Na alteração localizada de `PapeisSeeder::run`, `debug` `[PapeisSeeder@run] Iniciando concessão de cupons | painel: {painel}` e `info` `[PapeisSeeder@run] Sincronizando permissões de cupons | painel: {painel}`, com painel, contagem e resultado; `error` apenas em falha que interrompe a operação, propagada. Todos usam o channel da feature; não instrumentar globalmente outros recursos.
- **Skills futuras**: `ponytail`, práticas de autorização Laravel; especificação de testes somente no step 7.

### 4. Criar telas de cadastro e listagem

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07, RQ-08, RQ-09, RQ-10, RQ-11, RQ-17.
- **Paths candidatos se painel `app` for confirmado**: `app/Filament/App/Resources/Cupons/CupomResource.php`, `app/Filament/App/Resources/Cupons/Schemas/CupomForm.php`, `app/Filament/App/Resources/Cupons/Tables/CuponsTable.php`, `app/Filament/App/Resources/Cupons/Pages/ListCupons.php`, `app/Filament/App/Resources/Cupons/Pages/CreateCupom.php`, `app/Filament/App/Resources/Cupons/Pages/EditCupom.php`. Se Q2 mudar o painel, atualizar estes paths antes de gerar arquivos; não gerar ambas as árvores automaticamente.
- **Assinaturas propostas confirmadas em documentação**: `CupomResource::form(Schema $schema): Schema`, `table(Table $table): Table`, `getPages(): array`, `getEloquentQuery(): Builder`; `CreateCupom::handleRecordCreation(array $data): Model`; `EditCupom::handleRecordUpdate(Model $record, array $data): Model`. Usar namespaces de Filament 5 e tipos herdados, após confirmar contra dependências restauradas.
- **Formulário**: código, tipo, valor, validade e limite; sem campo de contador/ator/tenant. Enum determina as opções. Validar no servidor, não somente atributos HTML. Campos salvos não recebem `dehydrated(false)`.
- **Listagem**: mostrar os campos do cadastro e saldo/contador conforme público confirmado; implementar fronteira em `getEloquentQuery()` para abranger lista, resolução e busca. Ausência de contexto exigido fecha o conjunto. Filtros e ordenação têm lista fechada; datas e tipos inválidos não chegam a parse/índice de array cru. Não criar dashboard, exportação, notificação ou ativação manual.
- **Recortes bloqueados**: Q2/Q3 para localização e público; Q5/Q6/Q7/Q8 para campos/validação; Q12 para exclusão. **Bloqueado por**: RQ-11 (aberta — Q4), especificamente filtro de ativos. Não exibir tudo como fallback enquanto a definição está pendente.
- **Erros**: validação com mensagem do campo; colisão de código vira erro de domínio sem SQL bruto; acesso negado sem escrita. Exclusão não deve destruir histórico por conveniência técnica.
- **Logs no channel obrigatório**: início `debug` `[CreateCupom@handleRecordCreation] Iniciando cadastro de cupom | executor: {id}`; sucesso `info` `[CreateCupom@handleRecordCreation] Criando cupom | cupom: {id}`. Edição: mensagens equivalentes `[EditCupom@handleRecordUpdate] Iniciando edição de cupom | cupom: {id}` e `[EditCupom@handleRecordUpdate] Atualizando cupom | cupom: {id}`. Exclusão autorizada: `info` `[EditCupom@excluir] Excluindo cupom | cupom: {id}` no callback da ação, cujo método real será nomeado na implementação. Falhas de validação: `warning` `[CupomForm@validar] Recusando cadastro inválido | executor: {id}`, somente quantidade e motivo seguro; conectar ao ponto de validação real, sem criar método fictício apenas para log. Falha interrompida: `error` com método efetivo e código seguro. Listagem: `debug` `[CupomResource@getEloquentQuery] Aplicando fronteira de consulta | executor: {id}`, sem conteúdo dos registros; falta de contexto: `warning` no mesmo método. Nunca logar código ou estado inteiro.
- **Skills futuras**: `ponytail`, práticas Filament/Livewire e PHP disponíveis. Testes de gravação por componente serão derivados do `00`, não dos callbacks propostos.

### 5. Integrar aplicação, consumo e auditoria ao pedido

- **Atende**: RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18, RQ-19, P-01.
- **Bloqueado por**: RQ-12 (aberta — Q1), RQ-13 (aberta — Q1), RQ-14 (aberta — Q1), RQ-15 (aberta — Q1), RQ-16 (aberta — Q1), RQ-18 (aberta — Q1), RQ-19 (aberta — Q1).
- **Outras dependências**: Q5/Q6/Q8/Q9/Q10/Q11/Q12/Q13 e decisão técnica Q14. Não executar esse passo, nem um motor paralelo apresentado como sua implementação, antes de resolver o recorte dependente.
- **Paths**: integração e assinatura do método de aplicação **não definidos**, porque não existe pedido identificado. Não inventar `Pedido`, service, endpoint ou model comercial para preencher essa lacuna. Propostas condicionais de Q14: `app/Models/CupomUso.php` e `database/migrations/2026_10_20_000002_create_cupom_usos_table.php`; não são arquivos autorizados a criar.
- **Obrigações determinadas**: reconsultar cupom no servidor; verificar existência, validade e limite; calcular sobre total confiável do pedido; alterar total e incrementar contador apenas quando aplicação for efetivada; persistir ator autenticado e instante do servidor. Uma falha não pode deixar desconto sem consumo ou consumo sem auditoria.
- **Estratégia técnica proposta**: revalidar sob transação na mesma conexão; proteger saldo contra concorrência via lock suportado pelo banco ou escrita condicional que confira linhas afetadas. Unicidade do código é constraint, não apenas consulta anterior. Não prometer garantia de `lockForUpdate()` em SQLite. Q10 define a identidade da operação que evita consumo duplicado; não criar chave arbitrária por clique.
- **Histórico proposto de Q14**: tabela `cupom_usos` explicitamente declarada em `CupomUso`, ID, referências não nulas a cupom, ator e pedido confirmado, instante não nulo, índice de consulta por cupom/instante; vínculo de contexto se Q3 exigir. Tipo da chave de pedido, conexão, exclusão de FKs, snapshot de valor e constraint de idempotência dependem das respostas. Não usar cascade que apague a trilha por suposição. Não criar tela pública de histórico sem Q12/Q13.
- **Erros determinados**: inexistente, vencido ou sem saldo rejeitam aplicação sem desconto/consumo. Falha de gravação reverte unidade transacional. Valores numéricos, fronteira temporal, autorização, acumulação, cancelamento e respostas de UI dependem das respostas registradas.
- **Logs**: no futuro método real de aplicação, nome a fixar após Q1: `debug` `[{Classe}@{Método}] Iniciando aplicação de cupom | pedido: {id}`; `warning` `[{Classe}@{Método}] Recusando aplicação de cupom | pedido: {id} - motivo: {código}`; após commit, `info` `[{Classe}@{Método}] Aplicando cupom ao pedido | pedido: {id} - cupom: {id}`; em interrupção técnica, `error` `[{Classe}@{Método}] Revertendo aplicação de cupom | pedido: {id}`. Channel `cupons-de-desconto`; contexto permitido IDs internos, resultado, motivo enumerado, contagem de usos e correlação; erro somente classe/código seguro. Persistência de `CupomUso` e mudanças do pedido compartilham a unidade de sucesso; log não substitui a trilha.
- **Skills futuras**: `ponytail`, práticas transacionais/Eloquent; `feature-test-design` apenas no step 7, após revisão do plano.

## Filosofia de Implementação

Na futura implementação, ativar Ponytail e reutilizar código, APIs nativas e componentes existentes. Não criar abstrações especulativas, novos pacotes ou um domínio de pedidos por iniciativa técnica. Preservar segurança, validação e auditoria mesmo sob implementação mínima. Arquivos wiki usam prosa completa, sem compressão Caveman.

Antes de criar arquivos com Artisan, consultar comandos e `--help`, passando `--no-interaction`. Antes do primeiro commit, obter baseline no ambiente e base reais. Nesta cópia sem `.git` e sem dependências, baseline e comandos de Git não têm resultado disponível; não fabricar comparação contra `main`.

## Mapeamentos

| Campo do card | Representação candidata | Estado |
|---|---|---|
| Código | `codigo` | Obrigatório; Q7 define representação/equivalência. |
| Tipo | `tipo` / `TipoDesconto` | Somente porcentagem e valor fixo. |
| Valor | `valor` | Exato; escala/moeda pendentes. |
| Data de validade | `validade` | Obrigatória; sem corte implícito. |
| Limite de usos | `limite_usos` | Obrigatório; sem ilimitado implícito. |
| Contador | `usos` | Estado interno do servidor. |
| Quem / quando aplicou | Ator e instante por aplicação | Estrutura pendente Q1/Q14; não substituída por `updated_at` do cadastro. |

## Testes

Não há casos derivados, costuras confirmadas nem arquivos de teste nesta sessão. O `04-casos-de-teste.md` será responsabilidade do step 7, a partir do requisito; `05-casos-de-teste-browser.md` só existirá se uma costura exigir navegador. Leitura de `tests/Pest.php` confirmou RefreshDatabase global em Feature/Kit/Tenancy/Browser; helpers compartilhados já existem. Nenhum teste de `Exp*` foi lido ou executado.

## Verificação Final

Checklist para execução futura, sem marcar aprovação nesta sessão:

- [ ] Resolver perguntas e incorporar respostas como Adendo; preservar bloqueios remanescentes.
- [ ] Executar steps 5 e 6 antes de derivar testes no step 7.
- [ ] Confirmar APIs e schema efetivos com dependências restauradas e Boost quando disponível.
- [ ] Derivar testes de `00`; cobrir gravação por componente, matriz de permissões e invariantes determinados, sem cenários para RQ integralmente aberta.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` após modificar PHP.
- [ ] Rodar `php artisan test --compact` com arquivos/filtros afetados, definidos após o step 7.
- [ ] Comparar regressão de permissões e tenancy à baseline; sem Git, TIA não fornece prova do diff.
- [ ] Rodar browser em série somente se houver CT-B; build antes, sem iniciar servidor manual.
- [ ] Verificar concorrência e precisão no banco que exiba os riscos; mutation testing Windows usa o lançador da skill quando chegar a etapa própria.
- [ ] Medir queries com volume superior à página e confirmar ausência de N+1.
- [ ] Revisão independente do diff, reconciliação, QA e rules somente nas etapas futuras correspondentes.

## Commits

Não há `.git` nem commit nesta execução. Quando existir branch real e autorização de implementação, usar mensagens normais, por exemplo `:memo: cupons: documenta FERRO-812` e `:sparkles: cupons: adiciona cadastro autorizado`. Não afirmar commit, push ou PR realizados.
