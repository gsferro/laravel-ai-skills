# Decisões Arquiteturais — FERRO-830

Nenhuma decisão passou nos três portões.

O domínio está ausente e a criação dele depende de Q1. As escolhas rotineiras propostas estão em “Decisões de Desenho” do PRD; elas não justificam ADR nem autorizam uma implementação. Persistência de histórico por ciclo, garantias de notificação e fonte de responsáveis ainda dependem de respostas de requisito. Não transformar recomendações em ADR aceita.

Reutilizar o painel app, User, permissões Spatie e o padrão Notification do kit é uma escolha reversível e esperada. A adoção dessas convenções não decide quem aprova, quem vê ou que entidades serão criadas.

## Superfície Livewire

**Estado**: inventário proposto, bloqueado por Q1. Não há Resource, Page, Widget ou componente de compras na árvore atual. Não se afirma que as guardas abaixo já existem. O inventário serve de entrada futura à feature-test-design, após atualizar os pontos reais no código e confirmar o vendor.

A fronteira deverá cobrir código próprio, estado herdado do framework e ações de pacote. Todos os argumentos e propriedades alcançáveis pelo cliente serão considerados não confiáveis, inclusive quando a página inicialmente os preencher com valores válidos.

| Origem / ponto de entrada | Alcançável por | Fronteira a aplicar pelo projeto | Evidência / estado |
|---|---|---|---|
| Próprio / criação do rascunho | Gravação de CreateSolicitacaoCompra, pelo cliente Livewire. | Validar descrição, valor e centro; derivar dono/tenant no servidor; conferir fonte e organização do centro. | Proposto; página inexistente. RQ-01, Q1/Q2/Q6/Q14/Q16. |
| Próprio / gravação do rascunho | Gravação de EditSolicitacaoCompra. | Reconsultar registro, conferir dono e rascunho na mutação, permitir somente campos editáveis. | Proposto; página inexistente. RQ-02/RQ-11/RQ-13, Q12/Q19. |
| Próprio / exclusão | Action de exclusão com identidade de registro enviada pelo cliente. | Conferir dono, organização e estado no domínio; não confiar no registro montado no request anterior. | Proposto; RQ-03, Q12/Q19. |
| Próprio / enviar | Action com identificador da solicitação. | Verificar dono, estado e centro/responsável autorizado; decisão atômica. Não aceitar aprovador do formulário. | Proposto; RQ-04/RQ-12, Q2–Q5/Q8/Q9/Q11. |
| Próprio / aprovar | Action com identificador da solicitação/etapa. | Reconsultar etapa atual, conferir identidade elegível, ordem gestor-diretor e estado/ciclo esperado; persistir autoria no servidor. | Proposto; RQ-05/RQ-06/RQ-07/RQ-13, Q3–Q5/Q8/Q9/Q19. |
| Próprio / rejeitar | Action com identificador e justificativa. | Conferir gestor e etapa atual; validar justificativa no domínio; retornar ao rascunho atomicamente. Rejeição pelo diretor continua indecidida. | Proposto; RQ-08/RQ-09/RQ-10, Q10/Q11/Q15. |
| Próprio / cancelar | Action com identificador da solicitação. | Conferir solicitante e ausência de aprovação final no instante da escrita; impedir corrida com decisão final. | Proposto; RQ-14, Q12/Q13/Q19. |
| Próprio / leitura de detalhe | Navegação da lista e link do e-mail; binding do Resource. | Mesmo recorte autorizado da listagem, inclusive UUID válido de outra pessoa/organização. Revalidar acesso ao clicar. | Proposto; RQ-15/RQ-16, Q6/Q7/Q17. |
| Framework / estado do formulário | Escrita de propriedades públicas e dados do form entre requests. | Allowlist dos campos de negócio; não persistir dono, tenant, status, etapa ou autoria vindos do cliente. Validar valores na camada de domínio. | Nome e tipo das propriedades herdadas ainda não inspecionáveis; vendor ausente. Não afirmar Locked herdado. |
| Framework / identidade do registro | Troca do ID/UUID ou estado hidratado do registro entre requests. | Reconsultar por chave estável dentro do recorte autorizado. Se houver identificador escalar próprio, Locked e autorização de cada ação; Locked isolado não basta. | Proposto. Conferir declaração efetiva após vendor disponível. |
| Framework / busca e ordenação | Estados públicos de tabela, candidatos tableSearch e tableSortColumn. | Usar mecanismo nativo e colunas permitidas; não passar entrada como nome de coluna, operador ou SQL livre. | Proposto; nomes/tipos reais pendentes de vendor. Não criar busca ou ordenação adicional sem utilidade. |
| Framework / filtros | Candidato tableFilters, caso seja introduzido filtro. | Nenhum filtro customizado está previsto. Se necessário, enumerar domínio válido antes de índice/parse/where; atualizar a tabela e a especificação futura. | Não configurado no desenho mínimo. filters e pageFilters não são consumidos nesta feature. |
| Pacote / montagem e execução de Actions | Identificadores, argumentos e dados das ações Filament, inclusive chamadas diretas pelo cliente. | Aplicar guardas no domínio em cada execução, além da Policy e da query de tabela. A montagem não faz mutação. | [Documentação Filament 5](https://filamentphp.com/docs/5.x/actions/overview); assinaturas locais ainda não confirmadas. |
| Pacote / models persistidos | Ações nativas de create/edit/delete sobre a futura entidade de solicitação. | Toda escrita passa pelo agregado autorizado; nenhuma permissão é herdada apenas por ser “filho” de outro registro. | Nenhum model de pacote adicional será persistido pelo fluxo no desenho mínimo; User existente é referência de identidade. Confirmar todas as entradas reais antes de implementar. |

### Greps e provas negativas do step 3

Adaptação para PowerShell com rg. Os comandos abaixo são pesquisa inicial, sem varredura de implementação final e sem execução do step 5.

```powershell
Test-Path 'app/Filament/App/Resources/SolicitacoesCompra'
# False
rg -n 'public function ' app/Filament/App/Pages app/Filament/App/Widgets
# app/Filament/App/Pages/ConvitesRecebidos.php:58: public function getTitle(): string|Htmlable
# app/Filament/App/Pages/ConvitesRecebidos.php:63: public function table(Table $table): Table
# Widgets inexistente: erro de path; não interpretar como grep limpo.
rg -n 'public\s+([^($;]*\s)?\$[[:alpha:]_]' app/Filament app/Livewire -g '*.php'
# Candidatas existentes: propriedades do AssistenteChatWidget, RegistroPorConvite,
# CreateRole e EditRole. Nenhuma pertence a compras.
Test-Path 'vendor/filament'
# False
Test-Path 'vendor/livewire'
# False
```

Os pontos existentes acima pertencem a outras features e não serão alterados. Seus nomes não provam que as futuras páginas de compras terão os mesmos campos. Os atributos de proteção precisam ser confirmados no contexto da declaração, nunca com grep-v de Locked.

Os quatro greps de pacote exigidos não puderam rodar sobre código instalado, porque o diretório está ausente:

| Busca exigida | Alvo futuro | Resultado nesta sessão |
|---|---|---|
| ::find / whereKey / findOrFail | Código Filament/Livewire efetivamente usado pelas páginas. | Não verificado: vendor ausente. |
| Propriedades públicas tipadas ou sem tipo e seus atributos | Pages/traits de formulários, tabelas e Actions usadas. | Não verificado: vendor ausente. |
| arguments / data em ações | Montagem/execução das ações Filament. | Não verificado: vendor ausente. |
| extends Model | Models de pacote que o fluxo eventualmente persistir. | Não verificado: vendor ausente; nenhum model adicional de pacote foi proposto. |

**Lacuna declarada**: este inventário identifica os pontos pretendidos e suas guardas necessárias, mas não certifica cobertura de métodos herdados. Repetir os dois greps próprios e os quatro greps de pacote com código real, antes da implementação e novamente antes do step 9. Não tratar ausência de vendor como ausência de entrada.

## Decisões ainda não tomadas

- Origem e propriedade do domínio, centros de custo e responsáveis: Q1/Q2.
- Separação dos três papéis, falta/troca de aprovador e poderes administrativos: Q3–Q5/Q8/Q9/Q19.
- Visibilidade atual/histórica, rejeição pelo diretor, ciclos e cancelamento: Q6/Q7/Q10–Q13.
- Limites de texto/valor e destino/validade da notificação: Q14–Q18.

Nenhuma recomendação dessas perguntas é uma restrição aceita. Não há ADR “Proposta” usada para contornar a falta de resposta.

