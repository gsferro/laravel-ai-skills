# Decisões Arquiteturais — FERRO-830

Nenhuma decisão passou nos três portões.

As propostas de reutilizar Notification, componentes Filament e mutações concentradas no domínio são reversíveis e seguem precedentes existentes. Não há decisão persistente aceita que seja simultaneamente difícil de reverter, surpreendente sem contexto e resultado de trade-off real.

As decisões rotineiras estão no plano. Escopo, responsáveis, combinações de papéis, público, ciclos e retenção continuam perguntas de requisito. A indisponibilidade dos participantes não transforma recomendações em decisões.

## Superfície Livewire

Este inventário separa evidência existente, pontos propostos e limites de pesquisa. Nenhuma classe de compras foi criada. As fronteiras abaixo são objetivos de desenho condicionados às respostas, não controles já comprovados.

### Projeto: pontos de entrada propostos

| Ponto de entrada | Alcançável por | Fronteira aplicada pelo projeto / proposta | Evidência |
|---|---|---|---|
| Criar rascunho em CreateSolicitacaoCompra | Submit e estado de formulário manipulável | Servidor define autor, contexto e estado; valida somente descrição, valor e centro permitidos | Proposto no passo 3/5; classe ausente, sem assinatura herdada comprovada |
| Salvar rascunho em EditSolicitacaoCompra | Submit, estado do formulário e referência ao registro | Recarregar registro; exigir dono autorizado e estado atual rascunho; não permitir atribuição de aprovadores | Proposto; Q1/Q13/Q15/Q17 pendentes |
| Excluir rascunho | Ação de registro/ID enviado pelo cliente | Conferir dono, recorte e estado no domínio, além da policy; retenção depende de Q16 | Proposto; não há ação implementada |
| Enviar ou reenviar | Ação enviar e ID do registro | Exigir solicitante, rascunho e destinatário resolvido no servidor; sem confiar em estado recebido | Proposto; Q1/Q2/Q8 pendentes nos respectivos recortes |
| Aprovar como gestor | Ação aprovarComoGestor e ID do registro | Responsável da etapa, estado atual e regra de limiar verificados na unidade atômica | Proposto; Q2/Q4/Q6/Q17 pendentes |
| Rejeitar como gestor | Ação rejeitarComoGestor e justificativa | Validar identidade, etapa e justificativa obrigatória na gravação; retornar a rascunho | Proposto; domínio textual adicional pendente Q14 |
| Aprovar como diretor | Ação aprovarComoDiretor e ID do registro | Exigir gestor previamente aprovado, valor acima do limiar e responsável da segunda etapa | Proposto; Q2/Q5/Q6/Q17 pendentes |
| Cancelar | Ação cancelar e ID do registro | Exigir solicitante e ausência de aprovação final no estado atual, inclusive sob corrida | Proposto; sem regra de reabertura por Q9 |
| Consultar detalhe/status/aprovadores | Referência do registro e navegação | Público e recorte precisam de Q10/Q11/Q17; uma URL ou e-mail não concede autorização | Proposto; nada foi filtrado ou publicado nesta sessão |
| Callbacks de formulário/tabela | Requests Livewire, mesmo sem botão visível | Delegar às mesmas validações de domínio; não criar caminho de persistência paralelo | Proposto; hooks reais ainda precisam de API instalada |
| Novos métodos public de Page/Widget/componente | $wire com nome e argumentos forjados | Não criar métodos auxiliares públicos; validar ações efetivamente herdadas/chamáveis | Não há arquivo de compras para grep; inventário final de métodos permanece pendente |
| Novas propriedades public | $wire.set e hidratação entre requests | Não introduzir IDs/contexto autoritativo público; quando necessário, Locked e revalidação no servidor | Não há propriedade implementada; atributos de vendor não verificáveis |

Aprovar, rejeitar ou cancelar não pode depender apenas da query que exibe o registro. O Gate::before do superusuário exige tratar estado como invariante do domínio e resolver Q17 para exceções de identidade/visibilidade.

### Framework e pacote: estado e ações herdadas

| Ponto de entrada | Alcançável por | Fronteira aplicada pelo projeto / proposta | Evidência |
|---|---|---|---|
| Estado público do formulário ($data é candidato) | Hidratação/submit entre requests | Allowlist e validação no comando de gravação; nenhuma atribuição de campo de controle | Vendor ausente; nome, tipo e Locked não confirmados localmente |
| Registro da página de edit/view | Parâmetro de rota e hidratação | Resolver por query autorizada; revalidar no comando, sem aceitar troca de registro entre requests | Vendor ausente; propriedade e atributos herdados não confirmados |
| Busca da tabela ($tableSearch é candidato) | Atualização de busca | Colunas permitidas e consulta preservando recorte; texto nunca vira identificador SQL | Vendor ausente; inventário de declaração pendente |
| Ordenação ($tableSortColumn e direção são candidatos) | Atualização da ordenação | Allowlist de colunas/direções; recusar entrada fora do domínio antes da query | Vendor ausente; não alegar proteção implementada |
| Filtros ($tableFilters é candidato) | Atualização de filtro, se adicionado | Validar tipo, status e domínio antes de índice de array, parse ou where | Sem filtro adicional confirmado; vendor ausente |
| Paginação | Página/tamanho de página cliente | Limites do componente e recorte da query; não ampliar acesso com mudança de página | Vendor ausente; comportamento ainda não observado |
| Montagem/execução de ação Filament | Nome, argumentos, data e ID do cliente | Mesma verificação de ator, registro, etapa e organização em toda execução | Filament v5.7.6 no lock; fontes instaladas ausentes |
| Model persistido por pacote | Qualquer ação herdada que o alcance | Não assumir proteção por ser filho de outro registro; conferir entrada direta antes de reutilizar pacote | Plano não propõe persistir model de pacote; ausência de vendor impede prova completa |

As propriedades citadas como candidatas não foram inventariadas como declarações confirmadas. Não se afirma Locked por omissão, nem que filtro de UI bloqueia um método público.

### Evidência dos greps do step 3

No código atual, a pesquisa executou:

```powershell
rg -n 'public function |public\s+.*\$' app/Filament/App/Resources/Projetos app/Filament/App/Pages
```

Saída relevante:

```text
app/Filament/App/Pages/ConvitesRecebidos.php:58: public function getTitle(): string|Htmlable
app/Filament/App/Pages/ConvitesRecebidos.php:63: public function table(Table $table): Table
```

Evidências conferidas: `app/Filament/App/Pages/ConvitesRecebidos.php:getTitle():58` e `app/Filament/App/Pages/ConvitesRecebidos.php:table():63`.
Os métodos static form/table do Resource de Projetos também apareceram; eles não são ações de instância chamáveis por $wire.
A varredura ampliada de app/Filament e app/Livewire encontrou propriedades públicas em páginas administrativas de papéis, fora do recorte de compras; nenhuma foi reutilizada.
Nenhum resultado foi usado como prova de que a futura página não terá outros métodos públicos.

Na feature proposta, as buscas de métodos públicos e propriedades públicas só podem produzir inventário implementado quando houver arquivos. Até lá, as linhas propostas acima tornam a lacuna explícita.

Os quatro levantamentos prescritos no pacote permanecem não verificáveis:

| Levantamento | Caminho/expressão candidata | Resultado |
|---|---|---|
| Busca por ID cru | vendor/filament: ::find, whereKey, findOrFail | rg retornou erro de caminho inexistente; não equivale a ausência de pontos vulneráveis |
| Propriedades public e Locked | vendor/filament: declarações públicas e atributos anteriores | Não executável sem vendor; não presumir Locked |
| Argumentos/data de ação | vendor/filament: $arguments e $data | Não executável sem vendor; documentação pública foi fallback parcial |
| Models do pacote | vendor/filament: extends Model | Não executável sem vendor; não declarar cobertura completa |

`Test-Path vendor` retornou False. O fallback oficial foi a documentação Filament 5 e Livewire 4 citada no plano.
Esses levantamentos não foram substituídos por uma dedução de proteção transitiva.

