# Decisões Arquiteturais — FERRO-812

Nenhuma decisão passou nos três portões.

As escolhas técnicas rotineiras e propostas condicionais estão em **Decisões de Desenho** do plano.
Escopo de pedidos, organização, papéis, validade, dinheiro e ciclo de vida continuam sendo perguntas de requisito.
Não há ADR aceita por ausência de resposta. A persistência de usos é proposta condicionada ao contrato de pedido e à retenção; não é autorização para criar esse domínio.

## Superfície Livewire

Inventário de planejamento, não comprovação de componentes implementados.
A feature propõe páginas nativas do Filament; por isso a tabela é necessária mesmo sem plugin específico de cupons.
Os componentes de cupons ainda não existem. A ausência de métodos/propriedades próprios não dispensa inventariar o estado herdado.
A coluna “fronteira” descreve o controle planejado; nenhum deles foi exercitado nesta sessão.

### Origem: código do projeto

| Ponto de entrada | Alcançável por | Fronteira aplicada pelo projeto | Evidência / estado |
|---|---|---|---|
| ListCupons da gestão: sem método público novo planejado. | Ações herdadas e navegação de Resource. | Query de Resource com autorização e recorte a confirmar Q2/Q3. | Páginas ainda não criadas; irmã de padrão: `app/Filament/App/Resources/Projetos/Pages/ListProjetos.php:$resource:19`. |
| CreateCupom e EditCupom: apenas hooks protegidos planejados. | create/save herdados, não os hooks diretamente. | Reautorizar operação e usar apenas dados validados. | `app/Filament/Admin/Resources/AgentesIa/Pages/CreateAgenteIa.php:afterCreate():16`; `app/Filament/Admin/Resources/AgentesIa/Pages/EditAgenteIa.php:afterSave():21`. |
| ListCupons da operação: sem propriedade pública própria planejada. | Estado de tabela herdado. | Somente ativos, sem mutação, consulta restrita pelo mesmo Resource. | Componente ausente; predicado de ativos **bloqueado por RQ-11 (aberta — Q6)**. |
| Futuro ponto de aplicar cupom. | Ainda indefinido; nenhum endpoint/componente criado. | Ator e pedido verificados no servidor; não aceitar executor, total ou contador do cliente. | **Bloqueado por RQ-12–RQ-16 (abertas — Q1)** e Q13. Não é superfície liberada. |

Greps do projeto executados no step 3, adaptados a PowerShell/rg:

```text
rg -n 'public function ' app/Filament/App/Resources/Projetos/Pages app/Filament/Admin/Resources/AgentesIa/Pages
rg -n 'public\s+[^;]*\$' app/Filament/App/Resources/Projetos/Pages app/Filament/Admin/Resources/AgentesIa/Pages
Resultado: sem correspondências nessas páginas irmãs; leitura direta confirmou métodos protegidos e $resource protegido.
```

Esses greps são evidência dos padrões irmãos, não uma varredura de cupons já implementados.
Na implementação será necessário executá-los nos paths reais de Cupons; essa revarredura não foi feita nem antecipada como step 5.

### Origem: framework e ações herdadas

| Ponto de entrada | Alcançável por | Fronteira aplicada pelo projeto | Evidência / estado |
|---|---|---|---|
| CreateRecord::create(bool $another = false). | `$wire.create()`, inclusive chamada forjada. | canCreate e validação; não confiar em botão oculto. Definição de admin aguarda Q3–Q5. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L92); autorização na própria ação. |
| CreateRecord::createAnother(). | Ação nativa de nova criação. | Mesmo contrato de create; não considerar isCreating barreira de segurança. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L210). |
| CreateRecord::$data. | `$wire.set('data.…', …)`. | Allowlist dos campos editáveis, required e domínio fechado; contador, tenant e ator não vêm daqui. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L43); não Locked na declaração observada. |
| CreateRecord::$record. | Propriedade pública da página de criação. | Não usar registro ou ID fornecido pelo cliente para escolher alvo de escrita; criação pelo estado validado. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L38). |
| CreateRecord::$isCreating. | Cliente pode alterar flag entre requests. | Proteção contra clique duplicado é conveniência; unicidade fica no DB e aplicação segue contrato próprio. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L57); comentário oficial declara desbloqueio deliberado. |
| CreateRecord::$previousUrl. | Estado público de navegação. | Não usar esse estado para redirecionamento livre em customização; gerar destino do Resource. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/CreateRecord.php#L45). |
| EditRecord::mount(int|string $record). | Vínculo de registro na rota. | Resource resolve registro autorizado, com recorte de organização e update. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/EditRecord.php#L87). |
| EditRecord::$record herdado de InteractsWithRecord. | Referência hidratada do registro. | #[Locked] no source consultado; isso não substitui policy e query autorizada. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/Concerns/InteractsWithRecord.php#L16). |
| EditRecord::$data. | `$wire.set('data.…', …)`. | Mesma allowlist de criação; ignorar só o próprio ID resolvido na validação unique; manter usos intocáveis no CRUD. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/EditRecord.php#L57). |
| EditRecord::save(bool $shouldRedirect = true, bool $shouldSendSavedNotification = true). | `$wire.save()` com argumentos adulteráveis. | Reautorizar update e validar no servidor; flags de UI não mudam permissão. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/EditRecord.php#L159). |
| EditRecord::saveFormComponentOnly(Component $component). | Método público herdado. | Mesma autorização de update; confirmar caminho alcançável e hidratação da versão instalada antes de expor componentes parciais. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/panels/src/Resources/Pages/EditRecord.php#L206); checagem de autorização observada no método. |
| InteractsWithActions::mountAction(name, arguments, context). | `$wire.mountAction()`, incluindo delete. | Ação nomeada, registro reconsultado pelo Resource e policy da operação; nenhum lookup global por ID cru. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/actions/src/Concerns/InteractsWithActions.php#L138); negativa usa autorização da ação. |
| InteractsWithActions::callMountedAction(arguments). | Execução da ação montada. | Revalidar operação e dados; estado prévio de montagem não é autorização permanente. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/actions/src/Concerns/InteractsWithActions.php#L232). |
| InteractsWithActions::$mountedActions. | Array público com nome, arguments e context. | Resolver somente ações registradas e registro permitido; não aceitar executor_id, tenant_id, usos ou destino de escrita daqui. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/actions/src/Concerns/InteractsWithActions.php#L39). |
| CanSearchRecords::$tableSearch. | Busca e escrita direta do estado. | Validar tipo/domínio; busca por código preserva query de visibilidade, sem SQL raw. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/tables/src/Concerns/CanSearchRecords.php#L22). |
| CanSortRecords::$tableSort e sortTable(column, direction). | Escrita do estado e método público herdado. | Colunas e direção permitidas pela tabela; não interpolar estado como coluna SQL em código próprio. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/tables/src/Concerns/CanSortRecords.php#L9) e [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/tables/src/Concerns/CanSortRecords.php#L11). O nome observado é tableSort, não tableSortColumn. |
| HasFilters::$tableFilters. | Array público herdado, mesmo que não haja filtro customizado. | Não consumir como índice/parse sem validação. O predicado obrigatório de ativos não pode ser desligado por filtro. | [source oficial v5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/tables/src/Concerns/HasFilters.php#L23). |

Nenhuma tabela de rótulos será indexada diretamente por tipo/estado do cliente sem domínio fechado.
Nenhuma data de filtro livre será passada a parse; Q8 define o contrato temporal antes de existir esse consumo.
Adulteração de tipo, coluna, operador, enum ou estado não deve causar escrita fora de escopo ou erro de servidor não tratado.
A derivação dos cenários pertence ao step 7, não foi executada aqui.

### Origem: pacote de terceiro e persistência

| Model / ponto | Alcançável por | Fronteira aplicada pelo projeto | Evidência / limite |
|---|---|---|---|
| Cupom, model do projeto. | CRUD nativo e futuro comando de aplicação. | Policy + query autorizada; contador somente no fluxo transacional confirmado. | Model ainda ausente. O controle não é comprovado por escopo de outro model. |
| UsoCupom, proposta do projeto. | Somente futura aplicação confirmada, sem CRUD de usuário comum. | Ator do servidor e gravação na transação do pedido; retenção/acesso pendentes Q15. | **Bloqueado por RQ-18/RQ-19 (abertas — Q1)**. Não alegar proteção por ser filho de Cupom. |
| Audit do pacote OwenIt, caso reutilizada auditoria CRUD. | Eventos do model, não ID de trilha enviado pelo formulário. | Reutilizar contrato de auditoria dos campos editáveis; acesso de infra existente não é autorização para abrir histórico comercial no app. | `app/Traits/AuditsFillables.php:getAuditInclude():18`; vendor ausente impede varredura local do pacote. Não afirmar que o CRUD registra cada uso. |
| Models de plugins globais do painel. | Superfícies já existentes do kit. | Nenhuma gravação direta adicional planejada pela feature. | Não foram inventariados como persistência de cupons; se a implementação passar a gravá-los, a tabela precisa crescer. |

Os greps de vendor exigidos foram tentados; todos falharam por diretório ausente:

```text
rg -n '::find\(|whereKey\(|findOrFail\(' vendor/filament/filament/src
rg -n 'public\s+[^;]*\$' vendor/filament/filament/src
rg -n '\$arguments\[|\$data\[' vendor/filament/filament/src
rg -n 'extends Model' vendor/filament/filament/src/Models

rg: vendor/filament/filament/src: IO error ... (os error 3)
rg: vendor/filament/filament/src/Models: IO error ... (os error 3)
```

Falha de grep não significa ausência de ponto de entrada. O fallback consultou source oficial remoto da tag travada, sem instalar nem escrever dependências.
O pacote de auditoria tampouco está disponível localmente; sua API não foi ampliada por suposição.
A segurança da superfície permanece **não verificada em runtime**. Executar o inventário sobre a versão instalada e o código final será obrigação de etapa futura, não prova já produzida.

