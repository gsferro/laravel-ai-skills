# Decisões Arquiteturais — FERRO-812

Nenhuma decisão passou nos três portões.

As escolhas rotineiras estão em Decisões de Desenho do plano. A persistência dedicada de usos é proposta pendente de Q14, não uma ADR aceita. A falta de resposta não demonstra aceitação. O domínio de pedidos, a fronteira organizacional e a definição de admin são pendências de requisito, não decisões arquiteturais que a sessão possa tomar pelo solicitante.

O padrão de policies e os componentes nativos são reutilizáveis. Uma transação para preservar aplicação, consumo e auditoria é estratégia técnica proposta; o fluxo de pedido e a conexão efetiva ainda não existem como fatos confirmados. Nenhuma API de pedido foi inventada para completar o template.

## Superfície Livewire

**Estado**: inventário de projeto e superfície proposta, com evidência incompleta por ausência de código da feature e de vendor. A coluna “fronteira” expressa controles exigidos no desenho; não afirma que estejam implementados ou provados. A integração futura permanece bloqueada.

### Evidência de pesquisa

Equivalentes em `rg` dos dois greps obrigatórios do projeto:

```text
rg -n 'public function ' app/Filament/App/Resources/Cupons
rg -n 'public\s+([^($;]*\s+)?\$[a-zA-Z_]' app/Filament/App/Resources/Cupons
```

Ambos retornaram exit 2: diretório inexistente (`os error 2`). Isso não é varredura limpa. A feature ainda não foi implementada. O caminho é candidato e depende de Q2/Q3. Pesquisa das Pages/Widgets existentes mostrou outros componentes, sem componente de Cupom ou pedido reutilizável identificado. Métodos estáticos de Resource não são, por si, ações Livewire públicas; o risco chamável é dos componentes e ações que os utilizam.

Os quatro greps de pacote, adaptados ao Filament sobre o qual a feature pretende montar:

```text
rg -n '::find\(|whereKey\(|findOrFail\(' vendor/filament
rg -n 'public\s+([^($;]*\s+)?\$[a-zA-Z_]' vendor/filament
rg -n '\$arguments\[|\$data\[' vendor/filament
rg -n 'extends Model' vendor/filament
```

Todos retornaram exit 2: `vendor/filament` inexistente (`os error 3`). `Test-Path vendor` e `Test-Path vendor/filament` retornaram `False`. Não existe prova local de `#[Locked]`, resolução interna de registros, inventário completo de propriedades ou models persistidos pelo pacote. Os mesmos limites atingem Shield e Auditing. Documentação oficial foi consultada, sem apresentá-la como inspeção do vendor instalado.

### Pontos de entrada e fronteiras

| Ponto de entrada (projeto / framework / pacote) | Alcançável por | Fronteira aplicada pelo projeto | Evidência / pendência |
|---|---|---|---|
| `ListCupons`, tabela herdada | Busca, ordenação, filtros e paginação vindos do navegador | Exigir autenticação, escopo de Q3 e ativos de Q4 antes da busca/paginação; não confiar em filtros enviados para garantir visibilidade. | Classe nova ausente. Referência de API: [Filament 5 — consulta do Resource](https://filamentphp.com/docs/5.x/resources/overview#customizing-the-resource-eloquent-query). Implementação e assinaturas internas pendentes. |
| Estado público herdado de tabela: candidatos `$tableSearch`, `$tableSortColumn`, `$tableFilters` | Atualizações Livewire entre requests | Tratar como entrada não confiável; allowlist de coluna/operador/tipo; não usar valor cru como parse ou índice. | Nomes são candidatos de inventário prescritos pela skill, sem declaração local confirmada. Grep vendor falhou, exit 2; confirmar campos efetivamente herdados antes de implementar. |
| `CreateCupom`, submissão `create` e estado de formulário herdados | Chamada direta da ação e alteração do estado | Policy de criação antes da escrita; validar campos permitidos; não aceitar contador, ator ou tenant do cliente; constraint única no banco. | [Filament 5 — criação](https://filamentphp.com/docs/5.x/resources/creating-records). Hook servidor documentado `handleRecordCreation`; componente e proteção herdada não verificados em vendor. |
| `EditCupom`, submissão `save`, identidade do registro e estado herdados | Requisição Livewire com estado/identificador adulterado | Resolver novamente o registro pela consulta autorizada e conferir update; atributos técnicos não são graváveis; bloqueio de identidade não substitui policy. | [Filament 5 — edição](https://filamentphp.com/docs/5.x/resources/editing-records) e [Livewire 4 — segurança](https://livewire.laravel.com/docs/4.x/security). Não presumir `#[Locked]` sem ler declaração real. |
| Ação de exclusão de Cupom | Montagem/chamada da ação e seu argumento de registro | Policy de delete a cada execução; fronteira de dados igual à de edição; sem ação em massa/forceDelete/restore implícita. Efeito histórico depende de Q12. | Ação nova ausente; [Filament 5 — ações](https://filamentphp.com/docs/5.x/actions/overview). IDs e autorização interna exatos pendentes da instalação. |
| Consulta de `Cupom` por lista, busca global, binding ou badge | Rotas do Resource e chamadas de componente | Centralizar em `getEloquentQuery` e conferir no domínio ao aplicar. Não vazar inativos ou outra organização em um acesso alternativo. | Padrão do projeto: `app/Filament/App/Resources/Users/UserResource.php:getEloquentQuery():121`; `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62` não fecha sem tenant. Q2/Q3/Q4 pendentes. |
| Modelo de cadastro `Cupom` | Formulário/ações do Resource; futura aplicação | Permissões de manutenção e campos permitidos; constraint de código; exclusão histórica conforme resposta. | Model novo não existe. Não é model do pacote; não há autorização provada por geração de policy. |
| Modelo de uso proposto `CupomUso` | Somente futura aplicação do domínio de pedido | Sem formulário de escrita; ator e instante do servidor; contexto e referências confiáveis; mesma unidade transacional. | Proposta Q14. Q1 bloqueia aplicação; não foi persistido nem exposto. |
| `Audit`, model do pacote Auditing, se reutilizado para CRUD ou escolhido em Q14 | Eventos Eloquent ou futura instrumentação explícita; consulta existente de auditoria | Conferir actor resolver, eventos, conexão, persistência e público de leitura. Não assumir que ser efeito do CRUD registra aplicação. | `config/audit.php:'implementation':21`, `config/audit.php:'events':65`, `app/Traits/AuditsFillables.php:getAuditInclude():18`; vendor ausente, sem fronteira interna comprovada. |
| Aplicação no pedido | Ponto de entrada ainda não identificado | Nenhum acesso novo definido; ator, pedido, total, contexto e autorização têm de vir de contrato confirmado. | Não inventariado como componente existente. Bloqueado por Q1/Q9; não há ação genérica “aplicar” autorizada. |

Nenhum método público customizado de Page foi criado. Não é possível afirmar que essa tabela é inventário completo de métodos/propriedades herdados. A instalação futura deve completar os greps e as evidências; pré-step 9 ainda exigirá nova varredura sobre o código final. Não foi executado esse step nesta sessão.

### Limites do inventário

Nenhum model do pacote foi declarado “protegido por ser filho”. A única persistência de pacote considerada é `Audit`, explicitamente listada e ainda sem prova de fronteira. Outros models que a restauração do vendor revelar precisam de linha própria antes de autorizar persistência pela feature. O eventual `CupomUso` é model de aplicação, separado da auditoria genérica por proposta, não por decisão aceita.

As roles `admin` e `admin_organizacao`, a passagem antecipada de `master_global` e a ausência de tenant fora do painel são fatos do código. O significado comercial deles para este card continua em Q2/Q3. Não corrigir esses fatos como se o requisito já tivesse escolhido outra regra.
