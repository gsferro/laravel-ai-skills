# Decisões Arquiteturais — FERRO-812

Nenhuma decisão passou nos três portões. As escolhas rotineiras ficam em **Decisões de Desenho** do plano. As escolhas de produto sobre escopo, papéis, organização, validade e histórico continuam perguntas ao solicitante; não são ADRs aceitas.

Este documento foi consolidado depois do PRD, ainda no step 4; a superfície permanece planejada e parcialmente não verificável.

A reutilização de Resource, Policy, transação de banco e traits existentes é convencional e reversível. A persistência de aplicações poderia produzir uma decisão durável, mas depende do contrato de pedido e da política de histórico ainda ausentes. Não foi tomada antecipadamente.

## Superfície Livewire

### Situação e limites da pesquisa

A feature tem UI, portanto esta seção é obrigatória. O quadro abaixo é **inventário planejado**, não certificação do código futuro. As classes de cupom ainda não existem. Os pacotes não estão instalados. As declarações completas, os atributos `#[Locked]` e os modelos alcançáveis do vendor não puderam ser conferidos; a lacuna impede afirmar que a fronteira está completamente protegida.

As [policies de Resources no Filament 5](https://filamentphp.com/docs/5.x/resources/overview#authorization) permitem separar acesso e ações. O filtro dos registros precisa acompanhar a autorização. A [segurança do Livewire 4](https://livewire.laravel.com/docs/4.x/security) exige tratar argumentos e propriedades públicas como entrada do cliente. Essas fontes não substituem a inspeção do vendor travado.

| Ponto de entrada / origem | Alcançável por | Fronteira a aplicar | Evidência / situação |
|---|---|---|---|
| Métodos públicos próprios de páginas de cupom | Chamadas `$wire` para métodos públicos de componentes | Não criar métodos públicos de escrita auxiliares; hooks de persistência protegidos. Cada método público real deve ser inventariado e validado. | Páginas futuras inexistentes; grep de métodos: exit 2. Irmã usa hooks protegidos: `app/Filament/Admin/Resources/AgentesIa/Pages/CreateAgenteIa.php:afterCreate():16` e `app/Filament/Admin/Resources/AgentesIa/Pages/EditAgenteIa.php:afterSave():21`. Não é prova sobre cupom. |
| Propriedades públicas próprias de páginas de cupom | `$wire.set()` entre requests | Não aceitar tenant, ator, contador ou horário de aplicação por estado do navegador. Identidade e destino da escrita resolvidos no servidor; inspecionar atributo e contexto de cada propriedade real. | Grep nas classes futuras: exit 2. Não declarar nenhuma propriedade como Locked sem fonte instalada. |
| `create()` herdado e formulário `$data` da página de criação | Request Livewire de criação, inclusive chamada forjada | Policy de criação, contrato de campos, unicidade no banco e lista explícita de atributos graváveis. Revalidar papéis no servidor. **Bloqueado no recorte Q3/Q4/Q7/Q8.** | [Criação no Filament 5](https://filamentphp.com/docs/5.x/resources/creating-records); vendor ausente, assinatura concreta herdada não verificada. Hook documentado: `protected function handleRecordCreation(array $data): Model`. |
| `save()`, estado `$data` e identificador do registro na edição | Request Livewire de edição ou URL com UUID de outro cupom | Resolver registro pela query autorizada; Policy de atualização; impedir alteração de contador/tenant/identificador técnico via payload. **Recortes Q3/Q4/Q12 pendentes.** | [Edição no Filament 5](https://filamentphp.com/docs/5.x/resources/editing-records); vendor ausente. Hook documentado: `protected function handleRecordUpdate(Model $record, array $data): Model`. |
| `mountAction` / `callMountedAction` e identificador da ação de exclusão | Ação de tabela ou header, chamada direta com outro registro | Mesma query de registros e Policy de exclusão. Botão oculto não substitui checagem. Sem delete em massa, restore ou force-delete planejados. **Q12 bloqueia a semântica de exclusão/histórico.** | Ações `Filament\Actions` observadas na irmã `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`; nomes e assinaturas internos do vendor ainda são candidatos a conferir, não APIs locais comprovadas. |
| `$tableSearch` e busca de coluna | Estado público da tabela | Busca somente em colunas declaradas. Aplicar recorte de visibilidade antes da busca. Não interpolar coluna ou operador recebidos do cliente. | [Resources Filament 5](https://filamentphp.com/docs/5.x/resources/overview); declaração pública instalada indisponível. |
| `$tableSortColumn` / `$tableSortDirection` | Ordenação por estado público | Somente colunas e direções permitidas pelo componente, sem SQL livre. Testar domínio inválido após derivação do step 7. | Vendor ausente; grep de propriedades: exit 2. |
| `$tableFilters` | Estado público de filtros, se gerado/configurado | Não planejar filtro livre de “ativo” nem parse de data até Q5/Q6. Rejeitar domínios inválidos se houver filtro; validar forma e valor antes de índice ou parse. | Vendor ausente; declaração e sanitização não verificadas. Nenhum widget ou dashboard de cupom foi proposto. |
| `$mountedActions`, argumentos e seleção de registros, conforme o vendor instalado | Chamadas diretas de ações montadas | Validar tipo, ID e ação; resolver Cupom no servidor e autorizar a operação para aquele registro. Não confiar em record/tenant vindo do browser. | Grep de `$arguments[` / `$data[` em vendor: exit 2; precisa confirmar nomes e shapes reais. |
| `Cupom`, model próprio persistido | Criação, edição e exclusão pelos pontos anteriores | Policy completa, query de leitura comum restrita a ativos, atributos técnicos fora de mass assignment. Se houver tenancy, fechar ausência de contexto em toda consulta alcançável. | Model futuro. A trait existente não fecha sem tenant: `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`. Decisão de domínio pendente Q4. |
| `OwenIt\Auditing\Models\Audit`, model do pacote potencialmente persistido pelos eventos CRUD | Efeitos dos eventos Eloquent; não se planeja nova ação pública de auditoria | Reutilização para alterações de cadastro depende de inspeção do pacote. Não assumir que esse evento registra aplicação do desconto. A consulta de auditoria existente não define o público autorizado de Q18. | `app/Traits/AuditsFillables.php:getAuditInclude():18` inclui somente fillable; `config/audit.php:'events':65` enumera eventos. Model vendor ausente, grep de modelos exit 2. Auditoria da aplicação permanece bloqueada por Q2/Q18. |
| Futura aplicação no pedido | Nenhum ponto chamável criado nesta entrega de planejamento | Não criar ação, endpoint ou método público que aceite valor total/ator do navegador. Reabrir inventário quando Q2 definir o domínio real. | **Bloqueado por**: RQ-11 (aberta — Q2), RQ-12 (aberta — Q2), RQ-13 (aberta — Q2), RQ-14 (aberta — Q2), RQ-15 (aberta — Q2), RQ-17 (aberta — Q2), RQ-18 (aberta — Q2). |

### Greps prescritos e resultados

Equivalentes com `rg`, executados na raiz durante a pesquisa. Exit 2 significa caminho indisponível, **não** ausência de pontos de entrada.

```powershell
rg -n 'public function ' app/Filament/Admin/Resources/Cupons app/Filament/App/Resources/Cupons
# project_methods_exit=2; ambos os diretórios inexistentes.
rg -n 'public\s+([^($;]*\s+)?\$[[:alpha:]_]' app/Filament/Admin/Resources/Cupons app/Filament/App/Resources/Cupons
# project_properties_exit=2; ambos os diretórios inexistentes.
rg -n '::find\(|whereKey\(|findOrFail\(' vendor/filament vendor/owen-it/laravel-auditing
# vendor_ids_exit=2; vendor ausente.
rg -n 'public\s+([^($;]*\s+)?\$[[:alpha:]_]' vendor/filament vendor/owen-it/laravel-auditing
# vendor_properties_exit=2; vendor ausente.
rg -n '\$arguments\[|\$data\[' vendor/filament vendor/owen-it/laravel-auditing
# vendor_arguments_exit=2; vendor ausente.
rg -n 'extends Model' vendor/owen-it/laravel-auditing/src/Models
# vendor_models_exit=2; vendor ausente.
```

Os greps gerais nos componentes existentes identificaram métodos e propriedades de autenticação, papéis e chat, mas não uma implementação de cupom. Não serão copiados para a feature sem necessidade.

### Pendências antes de qualquer implementação

Depois de restaurado o ambiente, confirmar todas as classes e traits efetivamente usadas, inclusive ações herdadas, assinatura, propriedade, atributos e lookup de registros. Produzir uma linha por ponto real e por model de pacote persistido. A futura especificação de testes deverá consumir esta superfície com as lacunas declaradas; este quadro não certifica cobertura nem deriva CTs nesta rodada.

