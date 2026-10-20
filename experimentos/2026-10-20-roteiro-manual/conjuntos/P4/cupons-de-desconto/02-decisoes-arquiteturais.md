# Decisões Arquiteturais — FERRO-812

Nenhuma decisão passou nos três portões.

As escolhas rotineiras estão em “Decisões de Desenho” do 01. Não houve decisão de criar pedidos, motor de desconto, histórico próprio de aplicação ou exceção de superusuário. As perguntas de requisito permanecem no 00; uma recomendação não é ADR aceita.

A decisão sobre persistência da aplicação depende do domínio de pedidos e da retenção do histórico. Reaproveitar a auditoria de alterações do cadastro não significa registrar semanticamente a aplicação do desconto.

## Superfície Livewire

Inventário **prospectivo e parcial**, produzido no step 3 e registrado no step 4. A feature ainda não tem código. Não há evidência local dos métodos/propriedades herdados porque vendor está ausente; a documentação oficial de Filament 5/Livewire 4 confirma as categorias de fronteira, não uma varredura do código instalado. Deve ser completado no ambiente executável, antes de derivar casos que dependam dessas APIs.

As rotas e classes propostas estão condicionadas às respostas de painel, papéis e visibilidade. A tabela não implementa nem presume RQ aberta. Campos exibidos no formulário não são proteção contra escrita pelo cliente entre requests.

| Ponto de entrada / origem | Alcançável por | Fronteira prevista no projeto | Evidência / estado |
|---|---|---|---|
| CreateCupom::create, herdado do framework | Request Livewire, mesmo sem botão visível | Reavaliar autorização, validar allowlist de campos e constraint de código; Q2/Q3/Q4/Q6–Q8 pendentes | Sem classe da feature nem vendor para confirmar assinatura. [Criação Filament 5](https://filamentphp.com/docs/5.x/resources/creating-records); irmão usa hook protegido: `app/Filament/Admin/Resources/AgentesIa/Pages/CreateAgenteIa.php:afterCreate():16`. |
| EditCupom::save, herdado do framework | Request Livewire e tentativa de trocar record | Resolver UUID no escopo confirmado e reavaliar autorização no servidor; Q2/Q3/Q4/Q12 pendentes | [Edição Filament 5](https://filamentphp.com/docs/5.x/resources/editing-records); irmão `app/Filament/Admin/Resources/AgentesIa/Pages/EditAgenteIa.php:afterSave():21`; implementação herdada não inspecionada. |
| Estado público de formulário da página ($data e equivalentes a confirmar) | Alteração de snapshot/propriedades entre requests | Aceitar somente código/tipo/valor/validade/limite segundo contratos respondidos; recusar tipo fora da lista; não confiar em validação do navegador | [Segurança Livewire 4](https://livewire.laravel.com/docs/4.x/security); nomes/tipos/Locked no vendor pendentes. |
| Identidade do record e contexto organizacional da edição | URL direta, snapshot adulterado, argumento de action | Query central e guarda de posse; propriedades próprias que determinarem destino devem ser Locked; Locked não substitui autorização | Padrão de UUID: `app/Traits/TemUuid.php:getRouteKeyName():35`. Escopo sem tenant não basta: `app/Traits/BelongsToTenant.php:bootBelongsToTenant():62`. |
| Estado de contador, ator, tenant e instante oficial | Campos extras enviados pelo cliente | Fora da allowlist editável; ator/contador/instante de aplicação nem têm rotina implementada enquanto Q1 aberta | Fronteira planejada. Não criar propriedades públicas próprias para esses dados nem model de aplicação nesta etapa. |
| Actions de edição/exclusão: montagem, argumentos e execução herdadas | Request Livewire com nome de action/identificador forjados | Lista fechada de actions, nova resolução escopada do registro e autorização; não confiar na linha visível da tabela | [Autorização de Resources](https://filamentphp.com/docs/5.x/resources/overview). Métodos concretos do pacote sem confirmação local; inventário pendente. |
| $tableSearch | Escrita de estado do framework | Somente texto no contrato do framework, vinculado como parâmetro; formato inválido gera erro controlado, não query arbitrária | Nome citado como candidato da referência da skill; declaração/tipo vendor ainda não lidos. |
| $tableSortColumn / direção | Estado do framework enviado pelo cliente | Somente colunas/direções explicitamente permitidas; não usar string crua como coluna | Declarações reais pendentes; nenhuma ordenação da feature implementada. |
| $tableFilters e filtros de validade | Snapshot Livewire / querystring | Não criar filtros adicionais por suposição. Caso sejam adicionados após autorização, validar estrutura, enum e data antes de índice/parse | Nenhum filtro próprio determinado. RQ-11 aberta — Q5; não há filtro “ativo” aprovado. |
| Query da listagem de consulta, busca global e badge | GET do painel, consulta Livewire, busca, contagem | Aplicar mesma fronteira no Resource; não implementar ativo sem Q5, nem abrir dados sem contexto de Q2 | Sibling centraliza form/table em Resource: `app/Filament/App/Resources/Projetos/ProjetoResource.php:table():72`; não comprova filtro de cupons. |
| OwenIt Auditing Models Audit, persistido indiretamente pelo cadastro proposto | Eventos Eloquent do Cupom e tela existente de auditoria, sem nova action de escrita direta | Reutilizar configuração/policy existente para alterações de cadastro; não expor evento de aplicação ou model Audit gravável pelo navegador | Inclusão somente fillable: `app/Traits/AuditsFillables.php:getAuditInclude():18`; schema existente: `database/migrations/2026_08_12_164915_create_audits_table.php:up():12`. Vendor do pacote ausente. |

Cupom é model de domínio proposto, não model de pacote. Audit é o model de pacote que o cadastro pode persistir indiretamente. Não se afirma que um registro de auditoria filho esteja protegido por herdar a fronteira de outro model. As entradas diretas do pacote de auditoria não puderam ser varridas; nenhuma nova tela/action de Audit foi proposta.

### Levantamento prescrito — resultados e lacunas

| Varredura | Comando / resultado | Interpretação |
|---|---|---|
| Existência de código de cupons no projeto | `rg --files app database routes -g '*Cupom*' -g '*Coupon*'`: sem saída, exit 1; busca de declarações de domínio comercial também sem saída, exit 1 | Não há métodos/propriedades da feature a enumerar ainda. Não significa que o framework não exponha ações. |
| Métodos públicos nos irmãos do código projetado | `rg -n 'public function ' app/Filament/Admin/Resources/AgentesIa/Pages app/Filament/App/Resources/Projetos/Pages`: sem saída, exit 1 | Hooks locais desses irmãos são protegidos; métodos herdados continuam expostos. |
| Propriedades públicas nos mesmos irmãos | `rg -n 'public\s+([^($;]*\s+)?\$[A-Za-z_]' app/Filament/Admin/Resources/AgentesIa/Pages app/Filament/App/Resources/Projetos/Pages`: sem saída, exit 1 | Não há estado público local nesses irmãos. Não é prova sobre novas classes ou vendor. |
| Pacote Filament | `Test-Path -LiteralPath 'vendor/filament'`: False | As buscas por find/whereKey/findOrFail, propriedades públicas, argumentos/data e Models não executaram sobre fonte instalada. |
| Pacote Auditing | `Test-Path -LiteralPath 'vendor/owen-it/laravel-auditing'`: False | Mesmas quatro buscas indisponíveis; fronteiras concretas do pacote não verificadas. |

No ambiente restaurado, repetir os dois greps prescritos sobre **todo arquivo efetivamente criado** da feature, incluindo métodos públicos e propriedades tipadas/multilinha com atributos no contexto. Para cada pacote realmente persistido/exposto, executar as quatro buscas:

```bash
grep -rn "::find(\|whereKey(\|findOrFail(" vendor/{vendor}/{pkg}/src
grep -rnE 'public[[:space:]]+([^($;]*[[:space:]])?\$[[:alpha:]_]' vendor/{vendor}/{pkg}/src
grep -rn '\$arguments\[\|\$data\[' vendor/{vendor}/{pkg}/src
grep -rn "extends Model" vendor/{vendor}/{pkg}/src/Models
```

Nenhum resultado desses comandos futuros foi inventado. A tabela tem débito explícito de pesquisa, não selo de fronteira validada. As linhas determinadas alimentam a feature-test-design no step 7; as dependentes de RQ aberta não autorizam cenário nem implementação antes da resposta.

