# Plano de Ação — FERRO-812: Cupons de desconto

> Fonte da verdade: `00-requisito.md`.
> Planejamento até o step 4. Nenhuma implementação, instalação, alteração de banco ou execução de teste autorizada nesta rodada.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma; domínio de cupons não existe.
- **Toca infra compartilhada?**: sim, channel em `config/logging.php` e matriz de permissões de `database/seeders/PapeisSeeder.php`. A futura implementação exige regressão das features que consomem essa matriz, mesmo sendo feature nova.
- **Wikis relacionadas**: `wikis/specs/main/perfil-e-acesso-ao-painel/`, `wikis/specs/main/admin-da-organizacao/` e `wikis/specs/feature/multi-tenancy/organizacoes/`.

## Cobertura do Requisito

“Passo” indica destino do planejamento, não atendimento comprovado. As partes determinadas permanecem no plano. Nenhuma recomendação de Qn será executada como se fosse resposta.

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|---|---|---|---|
| RQ-01 | Criar no painel | 1, 2, 3, 4 | Painel/alcance bloqueados por Q3/Q4. |
| RQ-02 | Código | 2, 4 | Presença determinada; formato/comprimento bloqueados por Q7. |
| RQ-03 | Porcentagem ou fixo | 2, 4 | Conjunto de tipos determinado; faixas/precisão bloqueadas por Q8. |
| RQ-04 | Valor | 2, 4 | Campo determinado; precisão e contrato monetário bloqueados por Q8/Q9. |
| RQ-05 | Validade | 2, 4 | Campo determinado; representação e fronteira bloqueadas por Q6. |
| RQ-06 | Limite | 2, 4 | Campo determinado; domínio e alcance bloqueados por Q4/Q8. |
| RQ-07 | Só admin cria | 1, 3, 4 | Identificação da persona e acumulação bloqueadas por Q3/Q13–Q16. |
| RQ-08 | Só admin edita | 1, 3, 4 | Persona e histórico bloqueados por Q3/Q12–Q16. |
| RQ-09 | Só admin exclui | 1, 3, 4 | Persona, preservação e reutilização bloqueadas por Q3/Q12/Q18. |
| RQ-10 | Demais usuários apenas listam | 1, 3, 4 | Sem escrita comum; definição de público/painel bloqueada por Q3/Q4 e casos mistos. Q10 trata somente aplicação. |
| RQ-11 | Validar existência ao aplicar | 5 | **Bloqueado por**: RQ-11 (aberta — Q2). |
| RQ-12 | Validar validade ao aplicar | 5 | **Bloqueado por**: RQ-12 (aberta — Q2). Q6 também afeta a fronteira. |
| RQ-13 | Validar saldo de usos ao aplicar | 5 | **Bloqueado por**: RQ-13 (aberta — Q2). Q4/Q8/Q11 são pendências posteriores. |
| RQ-14 | Descontar total do pedido | 5 | **Bloqueado por**: RQ-14 (aberta — Q2). Q8/Q9/Q11 também pendentes. |
| RQ-15 | Incrementar no sucesso | 5 | **Bloqueado por**: RQ-15 (aberta — Q2). Q11 também pendente. |
| RQ-16 | Código único | 2, 4 | Garantia de banco e validação; alcance/comparação/reuso bloqueados por Q4/Q7/Q12. |
| RQ-17 | Registrar autor da aplicação | 5 | **Bloqueado por**: RQ-17 (aberta — Q2). Não é auditoria CRUD. |
| RQ-18 | Registrar momento da aplicação | 5 | **Bloqueado por**: RQ-18 (aberta — Q2). Não é horário do log de diagnóstico. |
| RQ-19 | Somente ativos na leitura comum | 3, 4 | **Bloqueado por**: RQ-19 (aberta — Q5). Q4/Q6/Q17 também afetam o recorte. |
| P-01 | Não criar domínio substituto | 5 | Premissa provisória de escopo estreito; não exclui obrigações do card. |

## Objetivo

Planejar cadastro e manutenção de cupons, com código único, tipo percentual ou fixo, valor, validade e limite de usos. As permissões precisam separar criação, edição e exclusão administrativas da listagem dos demais usuários.

A aplicação real no pedido deve validar existência, validade e saldo, descontar o total, consumir uso e registrar autor/momento. O projeto não oferece domínio de pedidos; esse trecho permanece integralmente bloqueado por Q2. Entregar somente cadastro ou um serviço de cálculo isolado não conclui o FERRO-812.

## Contexto

O projeto é um starter-kit com painéis de negócio, administração e infraestrutura. O model Projeto é demonstração descartável, sem total monetário; não representa pedido. Não foi encontrado contrato comercial que possa ser reutilizado como pedido, carrinho ou checkout.

O card não determina o significado de ativo, a equivalência entre os papéis existentes, a abrangência organizacional nem detalhes monetários. As perguntas correspondentes estão no requisito. O plano conserva as obrigações determinadas sem transformar recomendações em regras.

## Análise dos Arquivos Existentes

| Fonte conferida | Fato e consequência |
|---|---|
| `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:form():54`, `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:table():59`, `app/Filament/Admin/Resources/AgentesIa/AgenteIaResource.php:getPages():64` | Resource delega formulário/tabela e declara páginas separadas. Reutilizar estrutura, sem copiar a exclusão lógica de agentes como regra de cupons. |
| `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72` | Exemplo de ações `Filament\Actions`; não implica permissão de escrita de cupom no painel app. |
| `app/Traits/TemUuid.php:getRouteKeyName():35` | Convenção de UUID público, com chave interna numérica. |
| `app/Traits/AuditsFillables.php:getAuditInclude():18` | Só audita atributos fillable. Contador técnico fora de fillable não vira trilha de aplicação por consequência. |
| `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62` | Escopa quando há tenant; sem contexto, não filtra. Se Q4 exigir posse, acrescentar fechamento explícito nas superfícies alcançáveis; não copiar a trait como garantia de falha fechada. |
| `app/Models/User.php:canAccessPanel():74` e `app/Models/User.php:isMasterGlobal():116` | Acesso por painel e exceção global já existem; autenticado não significa acesso a qualquer painel. |
| `database/seeders/PapeisSeeder.php:run():45` | admin recebe matriz admin; admin_organizacao recebe matriz app com tenancy; panel_user recebe matriz app menos administração. Descoberta automática de Cupom não pode conceder escrita comum. |
| `app/Providers/KitServiceProvider.php:configureGates():86` | `Gate::before` na linha 90 permite master_global. Policy que retorne false não neutraliza esse bypass. Q3 precisa resolver a exceção antes de expor escrita. |
| `database/migrations/0001_01_01_000022_create_projetos_table.php:up():18` | Exemplo de id, UUID, timestamps e FK de tenant. O cascade da demonstração não decide preservação comercial. |
| `config/logging.php:'autenticacao':101` | Exemplo de channel daily. Não existe channel cupons-de-desconto. |
| `database/factories/UserFactory.php:definition():25` e `database/factories/UserFactory.php:unverified():41` | User tem factory e estado de e-mail não verificado. Tenant e Convite também têm factories. Não existem factories de Cupom nem de Pedido. |
| `tests/Pest.php` e `phpunit.xml` | RefreshDatabase em Feature/Kit/Tenancy/Browser; helpers compartilhados centralizados; tenancy com TestCase próprio. Browser tem timeout 20.000 ms; TIA local configurado. |
| `routes/web.php`, `routes/console.php`, `bootstrap/app.php` | Rota web própria é a página inicial; sem integração comercial. Agendamentos existentes não incluem cupons; não é necessário job para calcular validade na consulta. |

Provas negativas reproduzidas na raiz:

```powershell
rg -n -i '\b(cupom|cupons|coupon|coupons|desconto|discount|subtotal|carrinho)\b' app database routes resources config
# commerce_exit=1; nenhuma ocorrência.
rg -n -i 'class\s+(Pedido|Order|Cart|Checkout)\b' app
# order_exit=1; nenhuma ocorrência.
rg -n 'trait.*Logging' app
# exit 1; nenhuma trait de logging.
Test-Path vendor
# False
Test-Path node_modules
# False
Test-Path .git
# False
Test-Path wikis/glossario.md
# False
```

A pesquisa do agente também procurou nomes comerciais nos arquivos e migrations e nas wikis de produção permitidas; não encontrou domínio de pedido. Nenhuma pasta experimental foi lida.

## Decisões de Desenho

| # | Decisão | Pergunta / autorização | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Model Cupom, tabela explícita cupons e enum PHP nativo com os tipos já pedidos. | RQ-02–RQ-06; convenções de domínio. | Surpreendente sem contexto. | Sessão, 2026-10-20. |
| D2 | Resource, Schema, Table e Pages nativos com Policy completa; sem camada de repositório ou CRUD genérico. | Convenção dos Resources existentes. | Difícil de reverter. | Sessão, 2026-10-20. |
| D3 | id interno e UUID técnico pela trait TemUuid; contador/contexto fora de fillable. | Convenção; RQ-07–RQ-10 e integridade de RQ-15. | Trade-off surpreendente. | Sessão, 2026-10-20. |
| D4 | Fluxo síncrono; sem novo pacote, cache, evento próprio, fila ou scheduler para cadastro/listagem. | Autorização de planejar o card, reaproveitando a stack. | Difícil de reverter. | Sessão, 2026-10-20. |
| D5 | Diagnóstico em channel próprio; mensagens manuais porque não há trait de logging. | Contrato da feature-wiki e padrão local. | Surpreendente sem contexto. | Sessão, 2026-10-20. |

As posições candidatas nos painéis não são decisões aceitas de produto. Não há pergunta material de desenho além da pergunta de processo registrada no progresso. Moeda, histórico, papéis e visibilidade são requisito.

## Autorização

Criar futuramente `app/Policies/CupomPolicy.php`, seguindo a policy irmã e o gerador instalado: `viewAny(User $user): bool`, `view(User $user, Cupom $cupom): bool`, `create(User $user): bool`, `update(User $user, Cupom $cupom): bool` e `delete(User $user, Cupom $cupom): bool`. Métodos adicionais gerados devem negar operações não pedidas, após resolver Q3.

As abilities candidatas são `ViewAny:Cupom`, `View:Cupom`, `Create:Cupom`, `Update:Cupom` e `Delete:Cupom`; confirmar com Shield instalado antes de gravar nomes. Usuário comum não pode receber abilities de escrita pelo simples registro do Resource. Permissão de visualização não permite ver registros inativos.

Reutilizar guard web e middleware autenticado dos painéis. Se houver tenancy, reutilizar contexto persistente de permissões, sem aceitar tenant do formulário. Não alterar globalmente o bypass master_global nem ampliar acesso a painel para acomodar cupons. Q3/Q4 e Q13–Q16 bloqueiam decisões de alcance; Q10 bloqueia autorização de aplicar em pedidos.

## Rotas

**Candidatas, não registradas; dependem de Q3/Q4.** A gestão em admin e a leitura em app são hipóteses de localização. Não gerar URLs de aplicação nem prometer acesso comum a admin.

| Método | URI candidata | Name candidato | Middleware / acesso |
|---|---|---|---|
| GET | /admin/cupons | filament.admin.resources.cupons.index | Stack autenticada admin + viewAny da policy. |
| GET | /admin/cupons/create | filament.admin.resources.cupons.create | Stack autenticada admin + create. |
| GET | /admin/cupons/{record}/edit | filament.admin.resources.cupons.edit | Binding autorizado + update. |
| GET | /app/cupons ou /app/{tenant}/cupons | filament.app.resources.cupons.index | Stack autenticada app, contexto tenant quando ligado, viewAny e query somente ativos. |

Persistência pelo mecanismo Livewire/Filament; sem endpoints REST próprios. Confirmar nomes, middleware e rotas reais com `php artisan route:list --except-vendor --no-interaction` após disponibilidade do ambiente. Nenhuma URL absoluta foi gerada.

## Superfície de UI

| Tela / componente candidato | Tipo | Rota candidata | Interação | Depende de JS? |
|---|---|---|---|---|
| ListCupons administrativo | Filament / Livewire | /admin/cupons | Listagem de gestão; abertura de criação/edição conforme policy. | Sim |
| CreateCupom | Filament / Livewire | /admin/cupons/create | Preencher os campos pedidos e salvar. | Sim |
| EditCupom | Filament / Livewire | /admin/cupons/{record}/edit | Editar ou excluir conforme policy e contrato de histórico. | Sim |
| ListCupons de leitura | Filament / Livewire | /app/cupons ou /app/{tenant}/cupons | Listar somente ativos, sem escrita. | Sim |

Não foi planejado um botão de aplicar em uma tela de pedido inexistente. Sem alteração visual custom significativa, contrato externo, schema complexo definido ou pagamento externo, não há necessidade de extras 05-* nesta rodada.

A futura derivação do 04 precisa cobrir gravação por componente nas telas create/edit. O 05 só nascerá no step 7 se houver costura browser confirmada e um resultado que dependa de navegador. UI por si só não basta. Nenhum CT ou CT-B foi derivado aqui.

## Variáveis de Ambiente

Nenhuma chave nova. `APP_TIMEZONE=America/Sao_Paulo`, `DB_CONNECTION=sqlite` e `KIT_TENANCY=false` constam em `.env.example`; são exemplos de configuração, não evidência do ambiente efetivo nem resposta a Q4/Q6.

## Eventos / Listeners / Observers

Nenhum evento, listener ou observer próprio proposto para cupons. A trait AuditsFillables reutiliza eventos de Eloquent para alterações de cadastro, após inspeção do pacote. Isso não especifica a trilha exigida de aplicação no pedido. Não mudar configurações globais de auditoria por hipótese.

## Jobs / Queues

Nenhum job novo. Validade e saldo são condições de consulta e validação síncrona; não exigem tarefa que altere flag de ativo periodicamente.

## Modelo de Execução

| Pergunta | Resposta planejada |
|---|---|
| Requests da tela | GET do painel e requests do lifecycle Livewire para suas interações. Quantidade concreta não medida; depende do vendor ausente. |
| Caminho de escrita | Uma submissão Livewire por ação do usuário, síncrona; validar e autorizar antes da persistência. |
| Trabalho adiado | Nenhum polling, lazy custom ou tarefa de fila proposta. |
| Memoização por request | Nenhuma própria; não presumir comportamento de pacote não inspecionado. |
| Cache entre requests | Nenhum cache novo de cupons, validade ou saldo. |
| Custo em queries | Não medido. Na implementação, medir listagem comum e busca/ordenação com volume acima da paginação e comparar com o plano. |

Consumo e aplicação futuros precisam tratar concorrência no banco real. A opção técnica candidata é transação com bloqueio da linha ou atualização condicional, seguida da gravação consistente de desconto, contador e trilha. Isso detalhará obrigações de RQ-13–RQ-18 quando Q2 permitir; não existe serviço implementável aprovado agora. SQLite isolado não prova concorrência de produção.

## Impacto em Features Existentes

- Perfil/acesso: nova matriz pode ampliar permissões comuns ou depender de bypass global. Regressão das suítes Kit e Tenancy obrigatória.
- Administração da organização: manter permissões administrativas existentes e contexto de team; não usar subtração de todo o Resource se isso também remover a leitura solicitada.
- Multi-tenancy: listagem, busca, binding e contagem precisam da mesma fronteira, inclusive sem tenant corrente.
- Auditoria e logging: não confundir retenção técnica diária com trilha de aplicação; não ampliar a consulta infra para usuários comuns.
- Não alterar Projeto, convites, chat ou regras de autenticação como substituto do domínio comercial ausente.

## Rollback

Reverter registro das novas páginas e somente as permissões específicas de Cupom; regenerar Shield e reexecutar a matriz sem apagar grants de outras features. Remover o channel somente depois de preservar o diagnóstico necessário.

O `down()` da nova migration removeria cupons; isso é perda de dados e não deve ser executado em produção sem preservação/restauração definida. Não há migração destrutiva de tabela existente planejada. FK, hard/soft delete e preservação de aplicações serão definidos após Q2/Q12/Q18; nenhum cascade comercial foi escolhido. Nesta sessão não existe rollback a executar, pois somente documentação foi escrita.

## Dependências

| Componente | Versão observada | Origem / limite |
|---|---|---|
| PHP CLI | 8.4.10 | `php --version`; PCOV e Xdebug aparecem em `php -m`. |
| Laravel | v13.25.0 | composer.lock; vendor ausente. |
| Filament (forms, schemas, tables, actions) | v5.7.6 | composer.lock; vendor ausente. |
| Livewire | v4.4.0 | composer.lock; vendor ausente. |
| Shield / Permission | 4.3.1 / 8.3.0 | composer.lock; APIs instaladas não verificadas. |
| Laravel Auditing | v14.0.6 | composer.lock; não presume contrato de auditoria da aplicação. |
| Pest / browser / PHPUnit | v5.1.1 / v5.0.1 / 13.3.0 | composer.lock, sem runner instalado. |
| Boost | v2.5.3 | composer.lock, sem ferramentas MCP expostas. |
| Playwright | 1.62.1 | package-lock.json; package.json exige ^1.62.1; node_modules ausente. |

`composer show --direct --no-ansi` retornou `No dependencies installed. Try running composer install or update.` Versão travada não é versão instalada. Não instalar ou atualizar dependências nesta sessão. Não propor nova dependência para os cupons.

### Documentação consultada — fallback declarado

Boost `search-docs` e `database-schema` não estão expostos. Foram usadas fontes oficiais, com versões explícitas, e migrations como visão estática do schema; banco real não foi inspecionado.

- [Laravel 13 — autorização](https://laravel.com/docs/13.x/authorization), [validação](https://laravel.com/docs/13.x/validation) e [queries/bloqueio pessimista](https://laravel.com/docs/13.x/queries#pessimistic-locking): policies, unicidade e transação/bloqueio. O modelo passado a `Rule::unique()->ignore()` deve vir do servidor.
- [Filament 5 — Resources](https://filamentphp.com/docs/5.x/resources/overview), [criação](https://filamentphp.com/docs/5.x/resources/creating-records), [edição](https://filamentphp.com/docs/5.x/resources/editing-records) e [testes de Resources](https://filamentphp.com/docs/5.x/testing/testing-resources): estrutura e hooks protegidos de persistência.
- [Livewire 4 — segurança](https://livewire.laravel.com/docs/4.x/security): argumentos e propriedades públicas não estabelecem autorização; Locked não substitui autorização.
- [Pest — escrita](https://pestphp.com/docs/writing-tests), [browser](https://pestphp.com/docs/browser-testing) e [TIA](https://pestphp.com/docs/tia): guia atual identifica Pest 5; TIA deve ser desligado com `--no-tia` onde não houver Git/baseline válido.
- A tentativa de abrir a documentação oficial de Auditing falhou. Não foi assumida assinatura nova desse pacote; a reutilização futura exige confirmar a versão instalada. A primeira URL de TIA estava indisponível; o link oficial /docs/tia foi localizado e lido.

## Riscos

- Q2 pode ampliar significativamente o escopo; cadastro/listagem não substituem a aplicação no pedido.
- Q3/Q4 podem mudar localização das telas, posse e constraints. Não executar migration ou grants definitivos antes dessas respostas.
- Q5–Q9 podem mudar a representação e os limites de campos. Não adotar automaticamente as recomendações do requisito.
- Q12/Q18 podem mudar exclusão, índices e retenção. Não apagar rastros existentes.
- Vendor ausente impede confirmar assinaturas, declarações herdadas e superfície completa. Resolver lacunas antes de implementar, sem afirmar proteção já verificada.
- Não existe .git; não há histórico, diff, baseline de branch ou commit a produzir nesta rodada.

## Channel de Log da Feature

As buscas em `config/logging.php` e `app/` não encontraram channel de cupons nem trait de logging. Criar o channel é o primeiro passo futuro, sem criar uma trait genérica.

- **Nome**: cupons-de-desconto.
- **Driver**: daily.
- **Path**: `storage/logs/cupons-de-desconto.log`.
- **Level**: debug no desenvolvimento.
- **Days**: 14, seguindo os channels específicos existentes; não define retenção de auditoria.
- **Uso**: `Log::channel('cupons-de-desconto')` em todo log da feature.
- **Allowlist**: cupom_id, user_id interno, tenant_id interno quando aplicável, operation, result, reason/error_code seguros, exception_type e nomes de campos alterados. Não incluir código do cupom, formulário, atributos completos, dados pessoais nem mensagem/trace bruto da exception.
- **Níveis**: início/detalhe debug; sucesso info; validação/autorização rejeitada warning; exception que interrompe error; banco indisponível critical. Exceção tratada sem interrupção usa warning.

## Estrutura de Implementação

Os passos abaixo são planejamento futuro, sem autorização de execução nesta sessão. Além dos bloqueios explicitados, todos dependem do prosseguimento da esteira após o step 4.

### 1. Preparar channel de diagnóstico

> Skills futuras: ponytail e orientação Laravel instalada; não invocadas para escrever código nesta rodada.

- **Path**: `config/logging.php`, chave `channels.cupons-de-desconto`.
- **Atende**: RQ-01, RQ-07, RQ-08, RQ-09, RQ-10, como infraestrutura dos logs dos passos 3 e 4.
- Adicionar somente o channel descrito acima, sem mudar canais existentes, dependências ou formatter.
- **Logs**: configuração não executa lógica de negócio; não emite log próprio. Consumidores dos próximos passos devem usar esse channel.
- **Verificação futura**: conferir configuração resolvida e testar consumidores com a especificação futura, sem tinker ou script descartável.

### 2. Definir persistência do cadastro

> Skills futuras: ponytail; orientação de Eloquent/PHP disponível no host; pest-testing na execução dos cenários derivados.

- **Paths propostos**: `database/migrations/2026_10_20_000001_create_cupons_table.php`, `app/Enums/TipoCupom.php`, `app/Models/Cupom.php`, `database/factories/CupomFactory.php` e `database/seeders/CupomSeeder.php`.
- **Atende**: RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-16.
- Criar arquivos futuramente por comandos Artisan compatíveis, consultando `--help`, sempre com `--no-interaction`. A migration recebe o timestamp real gerado; atualizar este path no plano se mudar. Nenhum comando make foi executado.
- **Assinaturas**: `enum TipoCupom: string`, cases `Porcentagem = 'porcentagem'` e `ValorFixo = 'valor_fixo'`; `class Cupom extends Model implements Auditable`, `protected $table = 'cupons'`, `protected function casts(): array`; factory `definition(): array`; seeder `run(): void`.
- Reutilizar HasFactory e TemUuid. Auditoria de alterações de cadastro por AuditsFillables, depois de inspecionar o pacote; não usar isso para satisfazer RQ-17/RQ-18. Seeder útil somente para ambiente local/teste, sem distribuição automática de cupons em produção.
- **Schema determinado**: `id` big integer não nulo PK; `uuid` não nulo único; `tipo` string não nulo mapeado ao enum; timestamps Laravel. Não usar float para dinheiro.
- **Schema com recortes pendentes**:

| Campo | Obrigação determinada | Contrato ainda bloqueado |
|---|---|---|
| codigo | Campo obrigatório; validação e constraint de unicidade no banco. | Tipo textual/comprimento/collation/normalização Q7; índice único global ou composto Q4; reutilização pós-exclusão Q12. |
| valor | Valor obrigatório associado ao tipo. | Inteiro de unidade mínima versus decimal de precisão/escala definida por Q8/Q9; limites por tipo Q8. |
| validade | Data de validade obrigatória. | date versus datetime, fuso/conversão e fronteira Q6. |
| limite_usos | Limite obrigatório. | Tipo inteiro/capacidade, teto, zero/nulo Q8 e alcance Q4. |
| usos | Contador técnico exigido pela aplicação futura, nunca editável pelo formulário. | Incremento e ciclo de vida pertencem ao passo 5 bloqueado; não expor setter ou consumo antecipado. |
| tenant_id | Não existe obrigação de posse já resolvida. | FK, nullability, índice e relação somente após Q4; nunca fillable se usado. |
| deleted_at / ativo | Não adicionar por conveniência. | Política de exclusão Q12/Q18; flag manual somente se Q5 a exigir. |

- As recomendações de comprimento, faixas e validade no 00 são propostas ao solicitante, não defaults autorizados. Não executar os recortes da migration/factory dependentes dessas respostas.
- **Logs**: definições de enum/schema/factory não emitem log de negócio; o seeder local, se executado futuramente, deve registrar `debug('[CupomSeeder@run] Iniciando cadastro de exemplo | operation: seed')` e `info('[CupomSeeder@run] Concluindo cadastro de exemplo | operation: seed')`, com contexto operation/result e contagem; falha interrompida: error com exception_type/error_code seguros. Tudo no channel da feature. Não criar logs em casts.
- **Erros esperados**: rejeição de tipo fora do enum e duplicidade no banco deve virar erro de campo no chamador; nunca responder sucesso após falha da constraint.

### 3. Aplicar Policy e matriz de permissões

> Skills futuras: ponytail, orientação Filament/Shield instalada e pest-testing.

- **Paths**: `app/Policies/CupomPolicy.php`, `database/seeders/PapeisSeeder.php`; reutilizar `database/seeders/ShieldPermissionsSeeder.php`.
- **Atende**: RQ-07, RQ-08, RQ-09, RQ-10.
- **Bloqueado no recorte de persona/painel/tenancy**: Q3/Q4/Q13–Q16. A obrigação de negar escrita comum continua determinada e não pode desaparecer da matriz.
- Depois das respostas, implementar os métodos e abilities descritos em Autorização. Não modificar grants compartilhados por substring. Se a escolha for app, retirar apenas as operações de escrita indevidas para Cupom e preservar a leitura pedida.
- Após gerar o Resource, rodar futuramente `php artisan db:seed --class=ShieldPermissionsSeeder --no-interaction` e depois `php artisan db:seed --class=PapeisSeeder --no-interaction`. O primeiro gera policies; conferir que a geração não sobrescreveu a decisão aprovada de Cupom antes de resemear os papéis.
- **Logs**: cada método de Policy que rejeitar a operação deverá usar warning `[CupomPolicy@{método concreto}] Negando operação de cupom | operation: {ability fixa}`, contexto user_id, cupom_id quando houver, operation, reason. O prefixo e a ability serão literais em cada método, sem infraestrutura de logs genérica. Não emitir info para cada bool positivo; o sucesso da operação é registrado no passo 4.
- **Erros esperados**: acesso não autorizado resulta em resposta nativa 403/ação negada, com retorno à listagem autorizada; não redirecionar em ciclo para uma tela também proibida.

### 4. Construir Resources, formulário e listagens

> Skills futuras: ponytail, orientação Filament/Livewire instalada; feature-test-design somente na etapa própria antes da implementação.

- **Paths candidatos de gestão**:
  - `app/Filament/Admin/Resources/Cupons/CupomResource.php`.
  - `app/Filament/Admin/Resources/Cupons/Schemas/CupomForm.php`.
  - `app/Filament/Admin/Resources/Cupons/Tables/CuponsTable.php`.
  - `app/Filament/Admin/Resources/Cupons/Pages/ListCupons.php`.
  - `app/Filament/Admin/Resources/Cupons/Pages/CreateCupom.php`.
  - `app/Filament/Admin/Resources/Cupons/Pages/EditCupom.php`.
- **Paths candidatos de leitura**: `app/Filament/App/Resources/Cupons/CupomResource.php` e `app/Filament/App/Resources/Cupons/Pages/ListCupons.php`. Reutilizar configuração de colunas sem extrair componente genérico; separar configuração local apenas se necessário.
- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07, RQ-08, RQ-09, RQ-10, RQ-16, RQ-19.
- **Bloqueado por**: RQ-19 (aberta — Q5). Nenhuma listagem “ativa” implementada até a definição. Recortes adicionais: Q3/Q4 localização/público; Q6 validade; Q7/Q8 validação; Q12 exclusão/histórico; Q17 acesso histórico. Manter a possibilidade de listar de RQ-10 no plano, sem afirmar que o recorte pendente foi entregue.
- **Assinaturas**: Resource `form(Schema $schema): Schema`, `table(Table $table): Table`, `getPages(): array`, `getEloquentQuery(): Builder`; configuradores `public static function configure(Schema $schema): Schema` e `public static function configure(Table $table): Table`. Preservar tipos de propriedades do Filament 5.
- Formulário com codigo, tipo, valor, validade e limite_usos; somente os campos pedidos são editáveis. Não desidratar campos necessários à persistência. Validar no servidor conforme os contratos respondidos; enum fechado para tipo. Não aceitar actor, tenant, usos, preço ou total por formulário.
- Nas páginas de escrita, hooks documentados `protected function handleRecordCreation(array $data): Model` e `protected function handleRecordUpdate(Model $record, array $data): Model` permitem tratar duplicidade e controlar lista de atributos. Os hooks `afterCreate(): void` e `afterSave(): void` seguem as irmãs. Confirmar versão instalada antes de sobrescrever.
- Nas listagens comuns, aplicar visibilidade na query do Resource para alcançar binding, busca global e contagem, não somente na tabela. Se houver tenancy, ausência de contexto fecha a consulta com warning e não devolve base global. Não criar filtros que ampliem o predicado de ativo.
- Exclusão é ação nativa Filament autorizada; confirmar assinatura de callback/hook no vendor antes de configurá-la. Sem bulk delete, restore, exportação ou notificações externas novos.
- **Logs**, sempre no channel cupons-de-desconto, com a allowlist já definida:

| Método/ponto | Nível | Mensagem e contexto |
|---|---|---|
| CreateCupom::handleRecordCreation, antes da gravação | debug | `[CreateCupom@handleRecordCreation] Iniciando cadastro de cupom | operation: create`; user_id, operation. |
| CreateCupom::afterCreate | info | `[CreateCupom@afterCreate] Cadastrando cupom com sucesso | operation: create`; cupom_id, user_id, result. |
| EditCupom::handleRecordUpdate, antes da gravação | debug | `[EditCupom@handleRecordUpdate] Iniciando edição de cupom | operation: update`; cupom_id, user_id, nomes de campos da allowlist. |
| EditCupom::afterSave | info | `[EditCupom@afterSave] Salvando cupom com sucesso | operation: update`; cupom_id, user_id, result. |
| Validação na criação/edição | warning | `[CreateCupom@handleRecordCreation] Rejeitando cadastro inválido | reason: invalid_input` ou prefixo EditCupom@handleRecordUpdate; error_code, sem valores do formulário. Falhas anteriores ao handler exigem identificar hook nativo no vendor, ainda não verificado. |
| Constraint de unicidade | warning | `[CreateCupom@handleRecordCreation] Rejeitando código repetido | reason: duplicate_code`, ou equivalente no update; operation, error_code, sem código bruto. |
| Callback de exclusão, assinatura a confirmar | debug / info | `[EditCupom@delete] Iniciando exclusão de cupom | operation: delete` / `[EditCupom@delete] Excluindo cupom com sucesso | operation: delete`; cupom_id, user_id, result. Se o callback ficar na tabela, usar a classe/método reais, sem fingir método delete público. |
| Query de listagem, início | debug | `[CupomResource@getEloquentQuery] Consultando cupons autorizados | operation: list`; user_id, tenant_id se aplicável, result. |
| Falta de tenant, se Q4 exigir posse | warning | `[CupomResource@getEloquentQuery] Bloqueando consulta sem organização | reason: missing_tenant`; user_id, operation, reason. |
| Exception que interrompe persistência | error | `[CreateCupom@handleRecordCreation] Interrompendo cadastro de cupom | reason: persistence_failed`, ou método real de edição/exclusão; exception_type, error_code. Banco indisponível usa critical. |

- **Erros esperados**: manter formulário e mensagem de validação após rejeição; não mostrar notificação de sucesso nem consumir usos. Referência a registro fora da query deve resultar em 404/negação, sem revelar seus dados.
- Não introduzir helpers públicos de componente para cálculo ou autorização. Inventário no 02 é planejado e deve ser completado contra código real antes de implementar.

### 5. Resolver dependência de aplicação real no pedido

> Skill futura: feature-wiki para incorporar resposta como Adendo e detalhar o contrato; feature-test-design somente no step próprio. Nenhum motor paralelo será construído.

- **Paths e assinaturas de aplicação**: não definidos porque a entidade e o fluxo de pedido estão ausentes. Não criar nomes fictícios de endpoint, model ou service para simular integração.
- **Atende**: RQ-11, RQ-12, RQ-13, RQ-14, RQ-15, RQ-17, RQ-18 e P-01.
- **Bloqueado por**: RQ-11 (aberta — Q2), RQ-12 (aberta — Q2), RQ-13 (aberta — Q2), RQ-14 (aberta — Q2), RQ-15 (aberta — Q2), RQ-17 (aberta — Q2), RQ-18 (aberta — Q2).
- Nenhum subpasso implementa essas cláusulas enquanto Q2 estiver aberta. Após resposta, incorporar Adendo literal e definir fonte autoritativa do total, persistência, moeda, estado, usuário e fronteira organizacional com Q4/Q6–Q12/Q17/Q18.
- O contrato futuro deve preservar as validações já pedidas e impedir consumo acima do limite por concorrência. Desconto, consumo e registro auditável devem ter sucesso consistente ou falhar sem escrita parcial; a transação/atualização condicional é candidata técnica, não entrega de serviço isolado.
- Registrar autor autenticado no servidor e momento do servidor na aplicação real, ligados ao cupom e ao pedido. Auditoria CRUD ou log técnico rotativo não substituem essa trilha. Não escolher consulta, retenção ou exclusão da trilha antes de Q18.
- **Logs futuros**: início debug, motivo de rejeição warning, sucesso somente após commit info, falha interrompida error e banco indisponível critical; channel da feature e contexto mínimo cupom_id/pedido_id/user_id internos, operation, result, reason. Prefixos de classe/método só serão especificados quando existir contrato real; esta lacuna é bloqueio declarado, não omissão silenciosa.
- O FERRO-812 não será declarado entregue enquanto a aplicação e a trilha requeridas permanecerem bloqueadas.

## Filosofia de Implementação

Aplicar Ponytail full quando houver autorização de implementar: reutilização, PHP/Laravel nativos e menor alteração completa. Não inventar abstrações para contornar requisitos abertos. Models em português declaram tabela explicitamente.

A comunicação desta sessão segue Caveman; os arquivos da wiki mantêm prosa normal. Não foi iniciado o step 6 nem invocada auditoria de simplicidade. Nenhuma rotina de testes, tinker ou migração foi criada.

## Mapeamentos

| Conceito do card | Nome candidato interno | Situação |
|---|---|---|
| Cupom | Cupom / cupons | Nome técnico, sem resolver posse. |
| Porcentagem | TipoCupom::Porcentagem / porcentagem | Tipo explicitamente pedido. |
| Valor fixo | TipoCupom::ValorFixo / valor_fixo | Tipo explicitamente pedido. |
| Código | codigo | Formato, comparação e unicidade ainda condicionados. |
| Valor, validade e limite | valor, validade, limite_usos | Representação condicionada às respostas. |
| Admin / ativo / pedido | Sem redefinição silenciosa | Termos pendentes no 00; glossário global ausente e não autorizado para escrita nesta sessão. |

## Testes

O `04-casos-de-teste.md` será derivado no step 7, não nesta rodada. Nenhum ID ou cenário foi criado. `05-casos-de-teste-browser.md` dependerá de costura browser confirmada. As telas create/edit precisam de gravação por componente, além de visita HTTP.

Factories existentes de User, Tenant e Convite foram verificadas; Cupom receberá factory no passo próprio. Não criar factory de Pedido antes da decisão de escopo. Helpers compartilhados futuros pertencem a tests/Pest.php, sem duplicação; não é necessária modificação desse arquivo agora.

O plugin browser e Playwright estão declarados/travados, mas não instalados. O projeto usa `composer test:browser` com build prévio; manifest já existe, mas isso não prova execução. Não configurar servidor externo. Browser em série por regra local, com backend em comando separado.

## Verificação Final

Lista futura; nenhum item executado nesta invocação.

- [ ] Completar pesquisa de vendor/schema e superfície real sem tratar lacuna como resultado limpo.
- [ ] Registrar respostas materiais como Adendo e retirar somente os bloqueios efetivamente respondidos.
- [ ] Executar os steps 5 em diante somente em nova continuação autorizada.
- [ ] Derivar o 04/05 antes de implementar; executar os testes afetados com `php artisan test --compact` e path específico.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` após futura edição de PHP.
- [ ] Rodar regressão da matriz compartilhada em Kit e Tenancy; Browser separado, em série quando aplicável.
- [ ] Registrar baseline completa na base real, com falhas pré-existentes por nome. Nesta cópia sem Git/vendor, baseline não produzida.
- [ ] Usar TIA somente com ambiente/Git/baseline válidos; desligar com --no-tia quando não houver suporte. Nenhuma suíte foi executada nesta sessão, inclusive para evitar leitura dos paths proibidos.
- [ ] Planejar e medir concorrência no banco de produção compatível quando a aplicação existir; executar mutação pelo lançador Windows da skill na etapa própria.
- [ ] Medir custo com volume acima da paginação; executar revisão independente do diff, reconciliação e QA nas etapas previstas.

## Commits

Somente quando existir repositório e autorização de continuação. Sugestões de mensagens, não comandos executados:

- `:memo: cupons: documenta o planejamento do FERRO-812`.
- `:sparkles: cupons: adiciona cadastro e permissões aprovadas`.
- A mensagem da integração de pedido dependerá do escopo resolvido. Não criar Git nem commit nesta rodada.

