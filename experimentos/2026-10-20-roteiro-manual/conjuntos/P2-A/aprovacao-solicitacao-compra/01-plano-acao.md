# Plano de Ação — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: [00-requisito.md](00-requisito.md). Planejamento limitado aos steps 0–4 em 2026-10-20.
> Este PRD não está liberado para implementação. As obrigações explícitas estão preservadas, mas o domínio pressuposto pelo card não existe na árvore pesquisada. Os pontos candidatos abaixo não autorizam criá-lo.

## Natureza da Wiki

- **Tipo**: nova.
- **Wiki ancestral**: nenhuma do domínio de compras foi encontrada.
- **Motivo**: introdução de fluxo de aprovação de compras.
- **Toca infra compartilhada?**: sim, se a feature for autorizada: channel em `config/logging.php` e geração/distribuição de permissões Shield. Essas alterações exigem regressão dos painéis e permissões existentes, mesmo com natureza nova.
- **Antecedentes técnicos, sem herança de requisito**: `wikis/specs/feature/multi-tenancy/organizacoes/02-decisoes-arquiteturais.md`, `wikis/specs/main/admin-da-organizacao/02-decisoes-arquiteturais.md`, `wikis/specs/main/lembretes-de-convite/01-plano-acao.md`.

## Cobertura do Requisito

Os passos representam o trabalho futuro condicionado à resolução do escopo, não implementação das cláusulas abertas. Nenhuma obrigação foi marcada como atendida ou fora desta entrega.

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | O solicitante cria solicitação com descrição, valor e centro de custo. | 2, 3 | **Bloqueado por**: RQ-01 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-02 | O solicitante pode editar a solicitação em rascunho. | 3 | **Bloqueado por**: RQ-02 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-03 | O solicitante pode excluir a solicitação em rascunho. | 3 | **Bloqueado por**: RQ-03 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-04 | O envio encaminha a solicitação ao gestor do centro de custo para aprovação. | 4 | **Bloqueado por**: RQ-04 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-05 | Valor acima de R$ 5.000 exige também aprovação do diretor. | 4 | **Bloqueado por**: RQ-05 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-06 | Quando a aprovação do diretor é exigida, ela ocorre depois da aprovação do gestor. | 4 | **Bloqueado por**: RQ-06 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-07 | O gestor pode aprovar a solicitação. | 4 | **Bloqueado por**: RQ-07 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-08 | O gestor pode rejeitar a solicitação. | 4 | **Bloqueado por**: RQ-08 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-09 | Rejeição exige justificativa. | 4 | **Bloqueado por**: RQ-09 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-10 | Solicitação rejeitada volta para rascunho. | 4 | **Bloqueado por**: RQ-10 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-11 | O solicitante pode corrigir a solicitação que voltou ao rascunho após rejeição. | 3, 4 | **Bloqueado por**: RQ-11 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-12 | O solicitante pode reenviar solicitação que voltou ao rascunho após rejeição. | 4 | **Bloqueado por**: RQ-12 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-13 | Solicitação aprovada não pode mais ser alterada. | 3, 4 | **Bloqueado por**: RQ-13 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-14 | O solicitante pode cancelar a qualquer momento antes da aprovação final. | 4 | **Bloqueado por**: RQ-14 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-15 | A tela mostra o status atual. | 5 | **Bloqueado por**: RQ-15 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-16 | A tela mostra quem aprovou cada etapa. | 5 | **Bloqueado por**: RQ-16 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |
| RQ-17 | O próximo aprovador recebe notificação por e-mail. | 6 | **Bloqueado por**: RQ-17 (aberta — Q1). Q2–Q19 refinam somente seus recortes dependentes. |

O passo 1 fornece observabilidade aos demais. O passo 7 verifica o conjunto quando o fluxo puder ser implementado. Não existe passo de entrega de “motor isolado”: isso substituiria o card por outro escopo.

## Objetivo

Permitir que o solicitante mantenha um rascunho, envie ao gestor do centro de custo, percorra a etapa adicional de direção quando o valor for estritamente superior a R$ 5.000 e acompanhe status e aprovadores. Preservar rejeição com justificativa e retorno ao rascunho, cancelamento antes da aprovação final e imutabilidade após aprovação.

Antes de materializar esse objetivo, resolver Q1 sobre a criação ou o fornecimento das entidades ausentes. Até essa resposta, somente a pesquisa e a documentação são executáveis. Os demais detalhes de comportamento estão em Q2–Q19 do requisito, sem respostas presumidas.

## Contexto

A árvore contém um starter kit com painéis app, admin e infra, permissões, organizações, convites e um Projeto demonstrativo. Não há solicitação de compra, centro de custo ou vínculo de gestor/diretor que possa receber o fluxo. Projeto e Convite não serão renomeados ou adaptados para fingir que esse domínio existe.

### Evidência de ausência e limites do ambiente

Pesquisa reproduzida pela sessão:
```powershell
rg -n -i '\b(solicitacao|solicitação|solicitacoes|solicitações|compra|compras|centro.?de.?custo|centros.?de.?custo|purchase|requisition|cost.?cent(er|re)|gestor|diretor|aprovador|approver)\b' app/Models app/Policies app/Filament database/migrations database/seeders/PapeisSeeder.php routes config
# nenhuma linha; exit 1
```

O subagente também pesquisou as wikis de produção e não encontrou antecedente desse domínio. Os termos de aprovação em IA, atualizador do kit e convites eram falsos positivos.

- `Test-Path vendor`: `False`.
- `composer show --direct`: `No dependencies installed. Try running composer install or update.`
- `php -v`: PHP 8.4.10, Xdebug 3.4.4.
- `php artisan route:list --except-vendor --no-interaction` e `php artisan model:show User --no-interaction`: falham antes do bootstrap por ausência de `vendor/autoload.php`.
- `Test-Path .git`: `False`; pasta lógica `saida-p2-a` imposta pelo usuário. Não há branch real, histórico, diff ou baseline em main verificáveis.
- Boost `search-docs`, `database-schema` e `database-query` não estão expostos na lista de ferramentas desta sessão. Nenhuma consulta ao banco ocorreu. Migrations são evidência do schema esperado, não prova de um banco em execução.
- Não instalar dependências, inicializar Git ou iniciar aplicação nesta execução.
- `Test-Path wikis/glossario.md`: `False`. Não criar o glossário global porque só a pasta da feature pode ser alterada.

## Análise dos Arquivos Existentes

| Arquivo / símbolo | Fato confirmado | Uso futuro / cuidado |
|---|---|---|
| `app/Models/Projeto.php:$fillable:33` | Demo com nome; não é compra ou centro de custo. | Referência técnica de organização; não reutilizar como entidade de negócio. |
| `app/Models/User.php:canAccessPanel():74` e `app/Models/User.php:canAccessTenant():231` | Acesso a painel e a organização são verificações distintas. User usa Notifiable e HasRoles. | Reutilizar identidade e permissões; não inferir gestor/diretor dos papéis administrativos. |
| `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62` | O escopo só filtra quando há tenant corrente. | Jobs e métodos de domínio exigirão organização explícita; não confiar no contexto ausente. |
| `app/Traits/TemUuid.php:getRouteKeyName():35` | UUID nas rotas, chave primária numérica. | Reusar convenção se Q1 autorizar novos models; UUID não é autorização. |
| `app/Filament/App/Resources/Projetos/ProjetoResource.php:form():60`, `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`, `app/Filament/App/Resources/Projetos/ProjetoResource.php:getPages():91` | Schema e tabela no Resource, páginas no diretório Pages; demo usa modal. | Herança de organização de arquivos, sem copiar regras de negócio. |
| `app/Providers/Filament/AppPanelProvider.php:panel():56` | Painel app em /app, descoberta de Resources, autenticação e tenancy opt-in. | Registrar feature pelo diretório existente; não criar outro painel. |
| `app/Models/Convite.php:aceitarComoUsuarioExistente():608` | Atualização condicional evita duplo consumo; identidade conferida no model. | Reusar princípio de decisão atômica, não o model de convite. |
| `app/Notifications/ConviteDeAcesso.php:via():43`, `app/Notifications/ConviteDeAcesso.php:toMail():48`, `app/Notifications/ConviteDeAcesso.php:url():100` | Notification enfileirada, canal mail, URL do painel. | Criar conteúdo específico se autorizado, sem reaproveitar tokens de convite. |
| `app/Providers/KitServiceProvider.php:configureGates():86` | Gate::before concede acesso a master_global. | Não colocar identidade e imutabilidade apenas na Policy: o bypass não pode remover invariantes do domínio. Recorte administrativo pendente de Q19. |
| `config/queue.php:'after_commit':44` | after_commit está false na conexão database. | Enfileiramento futuro precisa aguardar commit explicitamente. |
| `tests/Pest.php:timeout():170` | Browser com teto de 20.000 ms; RefreshDatabase nas suítes; TIA local. | Reutilizar configuração; nenhum teste foi criado ou executado. |

Não existe trait de logging: `rg -n 'trait.*Logging' app` não retornou linhas. Usar chamadas explícitas ao channel, sem criar abstração genérica. Factories lidas: UserFactory com `unverified()`; TenantFactory com `inativo()` e `comIdentidadeVisual()`; ConviteFactory existe. Não há factory de domínio de compras. Seu desenho só poderá ser definido depois de Q1 e no step 7.

Rotas lidas: `routes/web.php` contém welcome; `routes/api.php` não existe; painel app vem do provider. Policies existentes e a matriz de papéis não contêm compras. `routes/console.php` agenda lembretes de convites, não aprovação de compras. Não há evento, observer ou middleware de compras a reaproveitar. O bootstrap global não será alterado.

### Regras de projeto carregadas

Índice de `.ai/rules` e busca por compra, aprovação, solicitação, wiki, logs e notificações executados antes das escritas. Regras lidas: `filament.md`, `testes.md` e `testes-browser.md`. A regra de auth não cobre os arquivos candidatos desta feature; páginas de autenticação não serão tocadas.

Aplicar identidade no método que faz a mutação, permissões Shield ao Resource, contexto de team da API Spatie e escopo que falha fechado. Para telas create/edit, exigir teste de gravação por componente no step 7. A regra local manda browser em série; a orientação mais geral da referência não autoriza ignorar essa restrição do projeto.

## Pesquisa de Documentação

Sem Boost exposto, pesquisa degradada com documentação oficial nas versões do lock. Não foi apresentada como `search-docs` executado.

| Stack / versão do composer.lock | Origem consultada | Conclusão usada |
|---|---|---|
| Laravel v13.25.0 | [Authorization](https://laravel.com/framework/docs/13.x/authorization) | Policies e Gate::before são mecanismos distintos; invariantes precisam sobreviver ao bypass. |
| Laravel 13 | [Database transactions](https://laravel.com/framework/docs/13.x/database#database-transactions) | Agrupar mudança de estado e registro de decisão em transação; falha deve desfazer o conjunto. |
| Laravel 13 | [Notifications](https://laravel.com/framework/docs/13.x/notifications#queued-notifications-and-database-transactions) | Notification pode usar afterCommit; isso não é garantia de entrega exatamente uma vez. |
| Laravel 13 | [Logging](https://laravel.com/framework/docs/13.x/logging) | Channel daily e retenção; a documentação atual usa max_files. Confirmar API no vendor instalado antes de executar. |
| Filament v5.7.6 | [Resources](https://filamentphp.com/docs/5.x/resources/overview), [Actions](https://filamentphp.com/docs/5.x/actions/overview) | Resource, Schema e Actions nativos; reconsultar e autorizar o registro dentro da ação. |
| Filament 5 | [Testing resources](https://filamentphp.com/docs/5.x/testing/testing-resources) | fillForm + create/save prova gravação por componente. |
| Livewire v4.4.0 | [Security](https://livewire.laravel.com/docs/4.x/security) | Propriedades e argumentos públicos são entrada não confiável; Locked não substitui autorização. |
| Pest v5.1.1 | [TIA](https://pestphp.com/docs/tia) | TIA não substitui baseline ou suíte de CI; sem Git e vendor não há execução válida aqui. |

Browser plugin v5.0.1 consta no lock, Playwright ^1.62.1 no package.json. Não são instalações verificadas. Não há necessidade de instalar pacote de browser por suposição: antes, restaurar dependências existentes. `composer test:browser` já faz build; o teste existente `tests/Browser/PerfisTest.php` foi lido e usa actingAs. O `05` não nasce por haver UI: depende de uma costura browser confirmada no step 7.

## Decisões de Desenho

Não há escolha material de desenho que possa ser legitimamente fechada pelo desenvolvedor enquanto Q1 estiver pendente. A sessão resolveu somente opções técnicas rotineiras amparadas no projeto. Nenhuma pergunta de fato foi transferida ao desenvolvedor; nenhuma pergunta de requisito foi respondida por ele.

| # | Decisão | Pergunta | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Planejar integração no painel app existente, com Schema e Actions nativos, sem novo painel ou pacote de workflow. | Convenção existente; não é resposta a Q1. | Surpreendente e difícil de reverter. | Sessão, 2026-10-20. |
| D2 | Se houver fluxo, preferir métodos de domínio junto à entidade e Policy na borda, como o padrão Convite; não criar service genérico de aprovação. | Convenção existente. | Surpreendente. | Sessão, 2026-10-20; condicionada à entidade fornecida em Q1. |
| D3 | Estado e decisão devem persistir atomicamente; utilizar atualização condicionada ao estado/ciclo, dentro de transação quando houver múltiplas escritas. | Convenção de consumo atômico já existente; mecanismo detalhado depende do schema. | Surpreendente. | Sessão, 2026-10-20; proposta técnica condicionada. |
| D4 | Reutilizar Notification mail enfileirada, com despacho após commit; sem evento/listener ou job adicional sem necessidade. | Convenção existente e API oficial. | Difícil de reverter. | Sessão, 2026-10-20. Garantias observáveis dependem de Q18. |
| D5 | Validar gravação em componente Filament e autorização no domínio; browser apenas para asserção que exija navegador. | Convenções de teste existentes. | Difícil de reverter. | Sessão, 2026-10-20. Costuras só serão confirmadas no step 7. |

As decisões acima não definem quem pode aprovar, quem vê histórico, limites de conteúdo ou quem pode cadastrar o domínio. Esses assuntos são Q1–Q19, raia requisito.

## Autorização

- **Policies candidatas**: `app/Policies/SolicitacaoCompraPolicy.php`, se a entidade for criada com esse nome, com `viewAny(User $user): bool`, `view(User $user, SolicitacaoCompra $solicitacao): bool`, `create(User $user): bool`, `update(User $user, SolicitacaoCompra $solicitacao): bool`, `delete(User $user, SolicitacaoCompra $solicitacao): bool` e habilidades de enviar, aprovar, rejeitar e cancelar. Contrato proposto, não API existente.
- **Camada de domínio**: revalidar identidade, organização, estado e etapa em cada mutação. Nunca aceitar solicitante, tenant, aprovador, status ou aprovações do formulário como autoridade.
- **Gates**: não modificar Gate::before global nem presumir que master_global é aprovador. Q19 decide poderes de negócio.
- **Middleware/guard**: reutilizar autenticação do painel app e contexto persistente de organização quando habilitado. Nenhum endpoint público de decisão.
- **Permissões**: se houver Resource novo, gerar permissões Shield e distribuir pelo PapeisSeeder no contexto adequado. Não adicionar papéis gestor/diretor nem conceder poderes enquanto Q2–Q5 e Q19 estiverem abertos.
- A tabela que lista registros não substitui a verificação no método de mutação. A mesma barreira precisa valer em componente, job e chamada direta.

## Rotas

Rotas candidatas, ainda não registradas. Seu prefixo depende de tenancy; não emitir URL absoluta sem `get-absolute-url`.

| Método | URI candidata | Name candidato | Middleware |
|---|---|---|---|
| GET | /app/[{tenant}/]solicitacoes-compra | filament.app.resources.solicitacoes-compra.index | Pilha do painel app, auth, tenant quando habilitado. |
| GET | /app/[{tenant}/]solicitacoes-compra/create | filament.app.resources.solicitacoes-compra.create | Idem e autorização de criar. |
| GET | /app/[{tenant}/]solicitacoes-compra/{record}/edit | filament.app.resources.solicitacoes-compra.edit | Idem e autorização de editar rascunho. |
| GET | /app/[{tenant}/]solicitacoes-compra/{record} | filament.app.resources.solicitacoes-compra.view | Idem e autorização de visualizar. |
| POST | Endpoint de atualização Livewire do framework; descobrir após bootstrap. | Nenhum endpoint próprio. | Middleware persistente e autorização em toda ação. |

`[{tenant}/]` é notação descritiva, não sintaxe a registrar. Não congelar prefixo ou nome gerado: confirmar por route:list e getPages após resolver Q1.

## Superfície de UI

Tudo abaixo está proposto e bloqueado pela ausência de domínio. A tabela não declara que essas páginas já existem.

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| ListSolicitacoesCompra | Filament | index | Listar somente registros visíveis, status atual e acesso ao detalhe. | Sim. |
| CreateSolicitacaoCompra | Filament | create | Preencher descrição, valor e centro de custo; gravar rascunho. | Sim. |
| EditSolicitacaoCompra | Filament | edit | Corrigir rascunho e salvar; excluir quando permitido. | Sim. |
| ViewSolicitacaoCompra | Filament | view | Mostrar status e identidade dos aprovadores por etapa; ações de enviar, aprovar, rejeitar e cancelar conforme estado e identidade. | Sim. |

Q6/Q7 decidem visibilidade; Q11 decide histórico de ciclos; Q17 decide destino do link. Telas create/edit terão cenário de gravação por componente no futuro `04-casos-de-teste.md`. Nenhum cenário ou arquivo de teste foi derivado agora. Não incluir bulk actions, exportação, polling, filtros por datas ou dashboard sem requisito.

## Variáveis de Ambiente

Nenhuma chave nova necessária para o desenho mínimo. Reutilizar:

| Key | Default no projeto | Descrição |
|---|---|---|
| QUEUE_CONNECTION | database | Worker necessário para Notification enfileirada. |
| MAIL_MAILER | log | Configurar transporte real no ambiente para enviar e-mail; log não entrega. |
| MAIL_HOST / MAIL_PORT | 127.0.0.1 / 1025 em .env.example | Transporte local de exemplo; não são configuração de produção. |
| MAIL_FROM_ADDRESS / MAIL_FROM_NAME | hello@example.com / APP_NAME | Remetente existente. |
| KIT_TENANCY | false | Tenancy opt-in existente; não ligá-la por esta feature. |

Não modificar `.env.example`, config de mail ou queue só para introduzir o fluxo. Contrato de isolamento de compras depende de Q2/Q6.

## Eventos / Listeners / Observers

Nenhum evento/listener/observer novo previsto no desenho mínimo. A mutação do domínio é a origem da Notification após commit; não usar observer genérico para adivinhar mudança de etapa. Reutilizar auditoria do kit se a entidade for criada, mas não apresentar logs técnicos como histórico de aprovação exigido por RQ-16.

## Jobs / Queues

Notification candidata: `app/Notifications/AprovacaoCompraPendente.php`. `ShouldQueue` já produz o trabalho enfileirado; não criar job redundante. Connection configurada no ambiente e fila default existente. Proposta de orçamento técnico: tries 3, timeout 30 s e backoff [10, 60, 300] s, sempre abaixo de retry_after (90 s no default database). Confirmar propriedades e suporte no vendor restaurado antes de executar.

A quantidade de tentativas não resolve Q18. afterCommit evita envio antes do commit, mas há janela de falha entre commit e despacho; não prometer entrega exatamente uma vez nem criar outbox sem decisão material após esclarecer a garantia de negócio.

## Modelo de Execução

| Pergunta | Resposta proposta, ainda não medida |
|---|---|
| Quantos requests a tela custa? | GET inicial do painel e atualização Livewire por interação; quantidade de requests de bootstrap do Filament ainda não observada. Uma mutação de negócio por envio da ação. |
| O que é adiado? | Somente entrega do e-mail após commit, via fila. Sem lazy widgets, polling ou carregamento diferido customizado. |
| O que é memoizado por request? | Nada adicional ao framework. |
| O que é cacheado entre requests? | Nada nesta feature; não cachear permissão, aprovador ou estado mutável. |
| Custo principal | Uma leitura autorizada do agregado, uma decisão atômica e gravação da decisão dentro da transação; total de SQL depende do schema e não foi medido. |
| Custo da listagem | Paginar e carregar aprovadores/centro necessários de uma vez; proibir consulta por linha na renderização. Medir com conjunto maior que uma página depois da implementação. |

Não declarar número exato de queries sem execução. Comparar/cancelar/aprovar simultaneamente deve serializar sobre o mesmo estado/ciclo; o resultado de negócio para a requisição que perdeu depende de Q7, preservando que ela não grava outra decisão.

## Impacto em Features Existentes

- Painel app, descoberta de Resources e busca global: a nova entidade precisa respeitar o mesmo recorte da listagem e do binding.
- Shield/PapeisSeeder: regressão obrigatória contra acesso a painéis, papéis por organização e administração da organização. Não promover panel_user a administrador por efeito indireto.
- KitServiceProvider: o Gate::before permanece; invariantes do fluxo não podem depender exclusivamente dele.
- Logging: acrescentar somente o channel da feature; não alterar channels de autenticação, tenancy ou IA.
- Convites e seus lembretes: nenhuma mudança prevista; o reuso é do padrão de Notification.
- Testes globais e middleware: sem alteração prevista. Se for necessária, revisar este plano antes de expandir escopo.

## Rollback

Não há alteração de aplicação a reverter nesta entrega documental.

Depois de Q1, planejar migrations somente aditivas. O `down()` específico dependerá de quem fornece o domínio e das relações confirmadas; não inventar remoção de tabelas ausentes. Após uso real, não apagar solicitações ou decisões como rollback automático: desabilitar entrada da feature e preservar dados até decidir reversão. Reverter código e permissões de forma delimitada, sem remover papéis usados por outras features. E-mails já enviados não podem ser desfeitos.

## Dependências

Nenhuma dependência nova autorizada ou necessária no desenho mínimo. Versões abaixo são do lock, não instalação efetiva:

- Laravel v13.25.0; Filament v5.7.6; Livewire v4.4.0; Spatie Permission 8.3.0.
- Laravel Boost v2.5.3; Pest v5.1.1; pest-plugin-browser v5.0.1.
- Playwright ^1.62.1, Tailwind ^4.0.0 e Vite ^8.0.0 declarados no package.json.
- `pest-plugin-livewire` não foi encontrado no lock; não assumir `Pest\Livewire\livewire`. Verificar a API de `Livewire\Livewire::test()` na instalação restaurada antes dos CT de componente; não adicionar plugin sem autorização.
- Não executar composer install, npm install ou playwright install nesta sessão.

## Riscos

1. **Domínio ausente**: Q1 bloqueia toda integração; não criar models como interpretação silenciosa do card.
2. **Papéis sobrepostos e bypass administrativo**: Q3–Q5/Q19; separar permissões de invariantes.
3. **Diretor, rejeição e ciclos**: Q10/Q11; não reutilizar decisão antiga como autorização atual.
4. **Concorrência**: aprovação, cancelamento e reenvio não podem produzir estado e histórico divergentes.
5. **Notificação obsoleta ou perdida**: Q17/Q18; confirmar escopo e garantia antes de criar infraestrutura extra.
6. **Limites não declarados**: Q14–Q16; não transformar sugestão de tamanho ou precisão em requisito.
7. **Pesquisa degradada**: sem Boost, vendor, banco ou baseline; nenhuma API local do framework foi executada.
8. **Viés de planejamento**: step 5 não executado, sem revisão profunda ou auditoria Ponytail; este documento é a saída do step 4.

## Channel de Log da Feature

Channel `aprovacao-solicitacao-compra` não existe na configuração lida. Acrescentá-lo será o primeiro passo técnico, somente se houver escopo implementável. Driver daily, path `storage/logs/aprovacao-solicitacao-compra.log`, level debug durante desenvolvimento e retenção de 14 arquivos (`max_files`, conforme documentação Laravel 13; validar no vendor antes de criar). Não copiar cegamente `days` dos channels antigos.

Todos os logs de execução da feature usarão `Log::channel('aprovacao-solicitacao-compra')` e o prefixo `[Classe@Método]`. Não há trait de logging a reaproveitar.

**Allowlist**: IDs internos estritamente necessários, tenant_id, etapa, ciclo, status anterior/atual, código de resultado/erro e correlation_id. Não registrar descrição, justificativa, valor de compra, nomes, e-mails, formulário, tokens, payload bruto, mensagem/trace de exception ou atributos completos. Não duplicar os dados do histórico nos logs.

Mensagens especificadas nos passos seguintes são contratos propostos de logging, não evidência de execução. O nome do método precisa acompanhar o desenho finalmente autorizado.

## Estrutura de Implementação

Nenhum passo abaixo está autorizado nesta sessão. Q1 pode substituir nomes, schema e paths; replanejar antes de qualquer make. Arquivos candidatos só serão criados se o solicitante confirmar a criação do domínio. Se outra entrega o fornecer, integrar nela, sem duplicação.

### 1. Preparar channel da feature

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07, RQ-08, RQ-09, RQ-10, RQ-11, RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-17.
- **Bloqueado por**: RQ-01 (aberta — Q1). Sem domínio autorizado, não adicionar configuração sem uso.
- **Path candidato**: `config/logging.php`; preservar channels existentes.
- **Detalhe**: definição descrita em Channel de Log, sem novas chaves de ambiente ou formatter.
- **Logs**: configuração declarativa não executa operação de negócio; nenhum log no bootstrap para anunciar o próprio channel.
- **Skills na execução futura**: ponytail e orientação Laravel pertinente já instalada; não instalar skills por este plano.

### 2. Integrar o domínio e sua persistência, após resolver Q1

- **Atende**: RQ-01, RQ-15, RQ-16.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-15 (aberta — Q1), RQ-16 (aberta — Q1).
- **Recortes adicionais bloqueados**: Q2, Q6/Q7, Q11 e Q14–Q16.
- **Paths candidatos se a criação for autorizada**: `app/Models/SolicitacaoCompra.php`, `app/Models/CentroCusto.php`, `database/factories/SolicitacaoCompraFactory.php`, `database/factories/CentroCustoFactory.php`; migrations geradas por Artisan somente depois do schema e da decisão de escopo. O model de decisão/histórico só será nomeado depois de Q11.
- **Schema**: não existe schema de compras aprovado. Atributos mínimos a mapear: descrição, valor, centro de custo, solicitante, estado, etapa e autoria da aprovação. Definir então tipos monetários exatos, nullable, FK, índices, constraints, política de exclusão e vínculo de organização. Não fornecer migration com valores inventados.
- **Assinaturas e relações**: dependem do agregado entregue. Se novo model em português for autorizado, declarar `$table` explicitamente quando não coincidir com o plural inglês inferido; usar as traits do kit sem pôr tenant_id ou uuid no fillable.
- **Erros**: entidade ou centro inexistente não vira seleção livre ou centro padrão. A fonte do responsável depende de Q2/Q8.
- **Logs**: schemas/factories não produzem logs de negócio. Falha de mapeamento, no futuro método que consome o centro, gera warning com motivo seguro, sem conteúdo do cadastro.
- **Skills futuras**: ponytail; orientação Eloquent/Laravel disponível. A ausência de qualquer skill deverá ser declarada, sem inventar que foi lida.

### 3. Criar e manter rascunho na fronteira do solicitante

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-11, RQ-13.
- **Bloqueado por**: RQ-01 (aberta — Q1), RQ-02 (aberta — Q1), RQ-03 (aberta — Q1), RQ-11 (aberta — Q1), RQ-13 (aberta — Q1).
- **Recortes adicionais bloqueados**: Q6/Q7, Q12, Q14–Q16, Q19.
- **Paths candidatos**: model de solicitação fornecido no passo 2; `app/Policies/SolicitacaoCompraPolicy.php`; `app/Filament/App/Resources/SolicitacoesCompra/Pages/CreateSolicitacaoCompra.php` e `EditSolicitacaoCompra.php`.
- **Assinaturas candidatas de domínio**: `atualizarRascunho(User $solicitante, array $dados): void`, `excluirRascunho(User $solicitante): void`. Especificar PHPDoc de array shape após confirmação dos campos; não aceitar status, tenant, solicitante ou aprovador do cliente.
- **Lógica determinada**: permitir ao dono editar e excluir rascunho, inclusive após rejeição. Nunca alterar solicitação com aprovação final. Não deduzir permissão apenas pela visibilidade do botão.
- **Erros**: validação sem escrita parcial; identidade errada ou estado vencido não altera registro. A mensagem e a navegação devem preservar apenas informações que o usuário ainda pode ver.
- **Logs**: início debug `[SolicitacaoCompra@atualizarRascunho] Iniciando atualização de rascunho | solicitacao_id: {id}`; sucesso info `[SolicitacaoCompra@atualizarRascunho] Rascunho atualizado | solicitacao_id: {id}`; exclusão info `[SolicitacaoCompra@excluirRascunho] Rascunho excluído | solicitacao_id: {id}`. Recusa de identidade/estado/validação: warning `[SolicitacaoCompra@atualizarRascunho] Atualização recusada | solicitacao_id: {id}`, com reason seguro. Exception que aborta: error com classe/código sanitizados.
- **Skills futuras**: ponytail; PHP/Laravel e Filament pertinentes; feature-test-design apenas no step 7, antes da implementação.

### 4. Aplicar envio, decisões, devolução e cancelamento atomicamente

- **Atende**: RQ-04, RQ-05, RQ-06, RQ-07, RQ-08, RQ-09, RQ-10, RQ-12, RQ-13, RQ-14.
- **Bloqueado por**: RQ-04 (aberta — Q1), RQ-05 (aberta — Q1), RQ-06 (aberta — Q1), RQ-07 (aberta — Q1), RQ-08 (aberta — Q1), RQ-09 (aberta — Q1), RQ-10 (aberta — Q1), RQ-12 (aberta — Q1), RQ-13 (aberta — Q1), RQ-14 (aberta — Q1).
- **Recortes adicionais bloqueados**: Q2–Q5, Q7–Q13, Q15/Q16, Q18/Q19.
- **Paths candidatos**: model de solicitação, model de decisão se confirmado no passo 2 e policy do passo 3. Não adicionar engine genérica de estados ou novo pacote.
- **Assinaturas candidatas**: `enviar(User $solicitante): void`, `aprovar(User $aprovador): void`, `rejeitar(User $gestor, string $justificativa): void`, `cancelar(User $solicitante): void`. Nenhuma dessas APIs existe hoje; amarrá-las ao agregado depois de Q1.
- **Regras determinadas**: enviar ao gestor do centro; diretor depois do gestor quando valor > R$ 5.000; gestor aprova ou rejeita; rejeição exige justificativa e retorna ao rascunho; reenvio é permitido; cancelamento pelo solicitante antes da aprovação final; aprovação final impede alteração.
- **Não determinado**: rejeição pelo diretor, acúmulo de papéis, falta/troca de responsável, reaproveitamento/histórico de ciclos e reabertura de cancelada. Não implementar recomendações de Q3–Q13 como regra.
- **Atomicidade**: reconsultar agregado autorizado e conferir estado/ciclo esperado. Em transação, uma única mudança concorrente vence, persistindo estado e autoria da etapa juntos. Não enviar e-mail antes do commit. Zero linhas atualizadas encerra a mutação sem duplicar decisão.
- **Logs por método**: debug `[SolicitacaoCompra@enviar] Iniciando envio | solicitacao_id: {id}`; info `[SolicitacaoCompra@enviar] Solicitação encaminhada | solicitacao_id: {id} - etapa: gestor`; info `[SolicitacaoCompra@aprovar] Aprovação registrada | solicitacao_id: {id} - etapa: {etapa}`; debug da decisão de ramificação com reason `exige_diretor` ou `aprovacao_final`; info `[SolicitacaoCompra@rejeitar] Solicitação devolvida ao rascunho | solicitacao_id: {id}`; info `[SolicitacaoCompra@cancelar] Solicitação cancelada | solicitacao_id: {id}`.
- **Falhas**: warning `[SolicitacaoCompra@aprovar] Decisão recusada | solicitacao_id: {id}` com reason de estado/identidade/corrida; rejeição sem justificativa também warning, nunca texto da justificativa. Exception que interrompe: error `[SolicitacaoCompra@aprovar] Falha ao registrar decisão | solicitacao_id: {id}`, com classe/código sanitizados; rollback integral.
- **Skills futuras**: ponytail; Laravel/Eloquent pertinentes. Derivação formal e concorrência serão especificadas pela feature-test-design no step 7; não criar CT aqui.

### 5. Expor status e aprovadores nas telas autorizadas

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-07, RQ-08, RQ-12, RQ-14, RQ-15, RQ-16.
- **Bloqueado por**: RQ-15 (aberta — Q1), RQ-16 (aberta — Q1), além das cláusulas abertas das ações que a tela encaminha.
- **Recortes adicionais bloqueados**: Q3–Q7, Q10–Q13, Q17/Q19.
- **Paths candidatos**: `app/Filament/App/Resources/SolicitacoesCompra/SolicitacaoCompraResource.php`; diretório `Pages/` com ListSolicitacoesCompra, CreateSolicitacaoCompra, EditSolicitacaoCompra e ViewSolicitacaoCompra. Nenhuma Blade customizada prevista.
- **Assinaturas candidatas**: Resource `form(Schema $schema): Schema`, `table(Table $table): Table`, `getPages(): array`; métodos de gravação e ações das Pages encaminham ao domínio. Respeitar namespaces/union types da versão 5. Confirmar hooks no vendor restaurado.
- **Lógica**: mostrar estado atual e identidade registrada de cada aprovador; a lista não calcula aprovação a partir de quem hoje ocupa o cargo. Q11 decide como distinguir ciclos. Input do cliente nunca grava “quem aprovou”.
- **Autorização**: escopo no Resource e na busca/binding, Policy e guarda do domínio. Sem tenant necessário, falhar fechado. Reconsultar cada registro antes da ação. Estado desconhecido não vira índice de array sem guarda.
- **Logs**: debug `[SolicitacaoCompraResource@getEloquentQuery] Consulta de solicitações preparada | painel: app`, sem consulta duplicada só para contar. warning `[SolicitacaoCompraResource@getEloquentQuery] Consulta recusada por contexto inválido | painel: app`; ações usam logs do domínio para evitar duplicação; validação recusada no componente gera warning com nomes/códigos seguros, sem valores.
- **Permissões**: após geração do Resource, rodar os seeders ShieldPermissionsSeeder e PapeisSeeder, nessa ordem, somente com autorização de implementação e matriz de negócio resolvida; verificar efeitos sobre panel_user e teams.
- **Skills futuras**: ponytail; orientação Filament/Livewire disponível; não escrever CSS/Tailwind sem necessidade.

### 6. Notificar o próximo aprovador por e-mail

- **Atende**: RQ-04, RQ-05, RQ-17.
- **Bloqueado por**: RQ-04 (aberta — Q1), RQ-05 (aberta — Q1), RQ-17 (aberta — Q1).
- **Recortes adicionais bloqueados**: Q2/Q8/Q9, Q17/Q18.
- **Path candidato**: `app/Notifications/AprovacaoCompraPendente.php`.
- **Assinaturas candidatas**: `via(object $notifiable): array` e `toMail(object $notifiable): MailMessage`, Notification com Queueable/ShouldQueue; construtor tipado conforme identidade do agregado autorizado. Inspecionar a versão instalada antes de adicionar revalidação por shouldSend.
- **Lógica determinada**: avisar o gestor no envio; avisar o diretor quando se torna o próximo aprovador. Aprovação final não tem próximo aprovador. Reenvio usa a regra de responsáveis/ciclos que vier a ser respondida.
- **Destino**: URL do detalhe gerada pelo Resource/painel, sem string de host fixa ou ação de decisão por GET; só liberar conteúdo/link depois de Q17.
- **Falhas**: SMTP ou fila indisponível não podem deixar estado e histórico incoerentes. Política de retentativa e tratamento de aviso obsoleto dependem de Q18. Não adicionar notificações de rejeição, aprovação final ou cancelamento que o card não pediu.
- **Logs**: debug `[SolicitacaoCompra@enviar] Preparando aviso de aprovação | solicitacao_id: {id}`; info `[SolicitacaoCompra@enviar] Aviso de aprovação enfileirado | solicitacao_id: {id} - etapa: {etapa}`. Enfileirado não será logado como entregue. warning para adiamento/retry seguro; error `[AprovacaoCompraPendente@toMail] Falha ao preparar aviso | solicitacao_id: {id}` somente quando houver falha que interrompe, sem mensagem/trace bruto ou e-mail. Se Q18 determinar supressão, registrar warning com reason seguro, sem enviar.
- **Skills futuras**: ponytail; orientação Laravel queues/notifications existente.

### 7. Validar e preparar entrega quando houver autorização futura

- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07, RQ-08, RQ-09, RQ-10, RQ-11, RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-17.
- **Bloqueado por**: todas as RQ abertas em Q1; somente planejamento até step 4 autorizado agora.
- **Paths futuros, ainda sem conteúdo ou IDs de CT**: `tests/Feature/AprovacaoSolicitacaoCompra/`; `tests/Tenancy/AprovacaoSolicitacaoCompra/` se isolamento for aplicável. Browser somente após costura correspondente confirmada; nenhum path Exp faz parte do escopo.
- **Ordem futura**: step 5 de revisão profunda, step 6 Ponytail, step 7 feature-test-design a partir do requisito, depois autorização/implementação conforme escopo. O step 8 não foi decidido. Revisão independente do diff (9), reconciliação (10), QA (11) e rules (12) permanecem futuros.
- **Verificação**: mínimo afetado por arquivo, gravação real em componentes create/edit, regressão dos painéis/permissões, concorrência e custo acima da página. Não reproduzir cenários neste PRD.
- **Logs**: comandos de teste/formatter não geram logs de negócio novos; observar os logs dos métodos descritos nos passos 3–6 na validação futura.
- **Skills futuras**: feature-test-design, ponytail, feature-quality-gate e requirement-to-rule nas etapas próprias, sem invocá-las nesta entrega.

## Mapeamentos

| Conceito do card | Fonte/autoridade futura | Destino proposto | Situação |
|---|---|---|---|
| Descrição | Entrada validada do solicitante. | Atributo de descrição da solicitação. | Teto e formato pendentes de Q14. |
| Valor | Entrada monetária validada. | Representação exata, sem float para comparar o limiar. | Domínio/precisão/teto pendentes de Q16; não fixar schema. |
| Centro de custo | Chave estável de cadastro autorizado. | Relação para centro; nunca título como identidade. | Entidade/fonte pendentes de Q1/Q2. |
| Solicitante | Usuário autenticado. | Identidade definida no servidor. | Não confiar em ID do formulário. |
| Gestor / diretor | Fonte de responsabilidade confirmada. | Designação da etapa e identidade da decisão. | Q2–Q5/Q8/Q9. |
| Status | Resultado da transição autorizada. | Estado persistido no agregado. | Nunca mass assignment de estado vindo do cliente. |
| Quem aprovou | Decisão gravada na etapa. | Identidade apresentada na tela. | Histórico/ciclos e visibilidade dependem de Q7/Q11. |

Fluxo determinado para preservar após Q1: rascunho admite edição/exclusão do solicitante; envio abre etapa do gestor; valor acima do limiar exige etapa posterior do diretor; rejeição do gestor exige justificativa e volta ao rascunho; aprovação final é imutável; cancelamento é permitido antes dela. A grafia técnica dos estados e as transições não descritas serão fechadas sem substituir essas obrigações.

## Filosofia de Implementação

Reutilizar o kit, Laravel e Filament nativos antes de introduzir abstrações ou dependências. Ponytail será aplicado na execução futura; nenhum passe de revisão foi feito agora. Manter prosa completa nos arquivos wiki, sem compressão Caveman. A sessão permanece no modo de comunicação imposto pelo host; a referência sugerir ultra não muda configuração do host.

## Testes

A especificação completa nascerá em `04-casos-de-teste.md` no step 7 pela feature-test-design. Não existe `04` nesta entrega. `05-casos-de-teste-browser.md` só existirá se alguma costura browser for confirmada; UI Filament por si só não é justificativa. Nenhum teste foi criado, alterado, rodado ou declarado verde. Baseline em main não verificável sem Git/vendor.

## Verificação Final

Itens de execução futura, todos pendentes:

- [ ] Resolver Q1 e revisar paths/schema antes de gerar qualquer arquivo.
- [ ] Incorporar respostas do solicitante como Adendos e manter bloqueios dos recortes ainda abertos.
- [ ] Executar revisão profunda e auditoria da wiki nos steps 5 e 6.
- [ ] Derivar testes no step 7 e confirmar costuras sem criar browser por reflexo.
- [ ] Restaurar ambiente autorizado e obter baseline completa na base real antes do primeiro commit.
- [ ] Rodar `php artisan test --compact {arquivo-afetado}` por arquivo implementado.
- [ ] Rodar `vendor/bin/pint --dirty --format agent` após alterações PHP.
- [ ] Rodar regressão de painéis, permissões e teams afetados; browser em série se necessário.
- [ ] Conferir TIA somente no ambiente apto; não usar como substituto da suíte completa de CI.
- [ ] Executar mutação com o lançador Windows da skill quando aplicável, registrando runner e sobreviventes.
- [ ] Medir queries da listagem e do detalhe acima de uma página.
- [ ] Revisão independente do diff, reconciliação e QA antes de PR; nenhum veredito emitido agora.

## Commits

Não executar commit nesta sessão: não há Git nem autorização de implementação. Quando existir repositório e autorização, separar alteração documental e execução de negócio conforme convenção:

- `:memo: compras: documenta fluxo de aprovação de solicitações`
- `:sparkles: compras: adiciona aprovação sequencial de solicitações`

