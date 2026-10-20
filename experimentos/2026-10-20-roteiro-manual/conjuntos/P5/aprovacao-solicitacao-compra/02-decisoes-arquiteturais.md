# Decisões Arquiteturais — FERRO-830

Nenhuma decisão passou nos três portões.

As escolhas técnicas rotineiras estão em “Decisões de Desenho” do plano. Falta de resposta não transforma alternativa em ADR aceita. Fonte de centro de custo, associação de aprovadores, público de consulta e política entre tentativas continuam nas perguntas ao solicitante.

## Superfície Livewire

Inventário de planejamento: a feature ainda não tem código. Cada linha descreve uma fronteira proposta para inspeção na implementação; não é evidência de guarda já aplicada. As entradas herdadas do framework não puderam ser conferidas em vendor ausente. A pesquisa oficial de Filament 5 e Livewire 4 confirma os conceitos gerais, mas não substitui o levantamento das declarações da versão travada.

| Ponto de entrada / origem | Alcançável por | Fronteira a aplicar | Evidência ou lacuna |
|---|---|---|---|
| CreateSolicitacaoCompra::create(), herdado de CreateRecord | Chamada de método pelo cliente | Solicitação sempre nasce como rascunho do ator autenticado; referência de centro autorizada; validação no domínio; nenhuma identidade recebida do form | Proposto, classe ainda inexistente; padrão de páginas em `app/Filament/App/Resources/Users/Pages/CreateUser.php`; assinatura herdada pendente no vendor |
| CreateSolicitacaoCompra::$data ou estado equivalente de formulário | Hidratação entre requests | Allowlist de descrição, valor e referência de centro; dados fora dela recusados; centro Q1 e limites Q7/Q9 pendentes | Nome/tipo exato de propriedade pendente de vendor; não declarar que está Locked |
| EditSolicitacaoCompra::save(), herdado de EditRecord | Chamada de método pelo cliente | Relê registro com recorte; confere dono e rascunho no domínio, inclusive payload forjado após carregamento | Proposto; referência de página em `app/Filament/App/Resources/Users/Pages/EditUser.php`; assinatura herdada pendente |
| EditSolicitacaoCompra::$data ou estado equivalente | Hidratação de campos entre requests | Mesma allowlist; jamais aceitar status, solicitante, organização ou aprovador como atributos editáveis | Pendente de implementação e declaração real |
| Edit/ViewSolicitacaoCompra::$record e qualquer ID/contexto interno adicionado | Identidade do registro entre requests | Confirmar proteção do framework; usar Locked se declarar propriedade própria determinante de escrita; reconsultar com contexto e autorização a cada comando | Atributos/declaração herdados não conferidos; não deduzir proteção pelo mount inicial |
| ViewSolicitacaoCompra::mountAction()/callMountedAction() ou equivalentes da versão | Cliente monta/chama ação com argumentos | Buscar registro autorizado; revalidar etapa, ator, versão e estado; argumentos não escolhem aprovador nem estado | Métodos candidatos do framework; nomes/assinaturas devem ser confirmados no vendor antes de usar |
| Ação enviar | Botão ou chamada direta ao dispatcher | Comando do model confere solicitante/rascunho e resolve responsável; encaminhamento integral bloqueado por Q1 | Proposto; nenhuma busca por ID cru autorizada |
| Ação aprovarComoGestor | Botão ou chamada direta ao dispatcher | Comando confere gestor da solicitação, etapa atual e estado; limiar exato; casos de sobreposição Q2/Q4 pendentes | Proposto; autenticação não substitui identidade do aprovador |
| Ação aprovarComoDiretor | Botão ou chamada direta ao dispatcher | Confere diretor e aprovação anterior do gestor; nenhuma aprovação fora de ordem; Q3/Q4 pendentes | Proposto |
| Ação rejeitarComoGestor, com $data['justificativa'] | Formulário/modal ou argumento forjado | Justificativa obrigatória validada no domínio; recusa fora da etapa; teto/vazio Q8 pendentes; não criar rejeição do diretor antes de Q10 | Schema de ação confirmado conceitualmente na documentação; callback da feature ainda não existe |
| Ação cancelar | Botão ou chamada direta ao dispatcher | Solicitante e estado anterior à aprovação final; update condicional; pós-cancelamento Q14 pendente | Proposto |
| Ação excluir | Ação de página ou chamada direta | Somente dono em rascunho; desabilitar ações em massa que contornem a mesma guarda | Proposto |
| ListSolicitacoesCompra::$tableFilters | Estado público de tabela | Lista fechada dos status conhecidos; nenhum valor direto como operador/coluna/índice sem validação | Nome conhecido do framework; declaração na versão travada pendente |
| ListSolicitacoesCompra::$tableSearch | Estado público de busca | String validada, query parametrizada e sempre dentro do recorte de visibilidade Q5; não usar entrada como expressão SQL | Declaração herdada pendente; não há parse de data ou índice de array proposto |
| ListSolicitacoesCompra::$tableSortColumn / direção / paginação | Estado público de tabela | Allowlist de colunas da tabela e direções; nenhuma coluna/operador arbitrário; paginação não remove recorte | Declarações herdadas pendentes; enumeração final depende da UI implementada |
| Listagem, binding de record e busca global do Resource | GET de UUID/consulta e atualizações Livewire | Mesmo getEloquentQuery e policy; audiência Q5 pendente; contexto ausente não pode abrir dados do negócio por acidente | Padrão local `app/Filament/App/Resources/Users/UserResource.php:getEloquentQuery():121`; comportamento de compras ainda proposto |
| SolicitacaoCompra, model local persistido pelo Resource | Criação, edição e ações | Métodos de domínio validam identidade, contexto, estado e atributos, sem confiar só em policy ou filtros da tela | Nenhuma classe da feature existe. Referência de guarda local: `app/Models/Convite.php:exigirDono():709` |

**Framework e pacotes**: a feature usa Resources e Actions do Filament, mas não propõe persistir nenhum model pertencente a pacote de terceiro pelo formulário. Solicitação é model local; centros de custo ainda não têm origem definida. Papéis/permissões eventualmente gravados por seeders são infraestrutura existente e não um formulário novo desta feature. Não há autorização para gravar pivots pelo relacionamento do form.

**Métodos públicos novos**: não propor métodos genéricos como executarAcao(string $nome, array $dados) no componente. Preferir os dispatchers nativos com ações de nomes fechados e comandos específicos do domínio. Renderização não deve expor método auxiliar de negócio como public.

### Levantamento executado no step 3

Adaptação para Windows: rg equivalente aos greps prescritos, com paths explícitos. As saídas de ausência são falhas de acesso ao caminho, não “nenhuma vulnerabilidade”.

```text
rg -n 'public function ' app/Filament/App/Resources/SolicitacoesCompra/Pages
caminho inexistente (os error 3)

rg -n 'public\s+.*\$' app/Filament/App/Resources/SolicitacoesCompra app/Livewire
caminho da feature inexistente (os error 2)
ocorrências em AssistenteChatWidget, fora do escopo da feature

rg -n '::find\(|whereKey\(|findOrFail\(' vendor/filament/filament/src
caminho inexistente (os error 3)

rg -n 'public\s+.*\$' vendor/filament/filament/src
caminho inexistente (os error 3)

rg -n '\$arguments\[|\$data\[' vendor/filament/actions/src
caminho inexistente (os error 3)

rg -n 'extends Model' vendor/filament/filament/src/Models
caminho inexistente (os error 3)
```

Os dois greps no código existente confirmaram candidatos públicos no app; nenhum deles implementa compras. Arquivos de exemplo sem declarações próprias não significam que a herança deixou de expor ações. Os quatro greps de pacote não produziram inventário verificável porque não existe vendor local. Repetir o levantamento quando houver código e dependências; manter a lacuna explícita até lá. Não executar a revarredura pré-step 9 nesta rodada.

### Fontes consultadas

- [Filament 5, query de Resource](https://filamentphp.com/docs/5.x/resources/overview#customizing-the-resource-eloquent-query).
- [Filament 5, schema de ação](https://filamentphp.com/docs/5.x/actions/modals).
- [Livewire 4, segurança de ações e propriedades](https://livewire.laravel.com/docs/4.x/security).

