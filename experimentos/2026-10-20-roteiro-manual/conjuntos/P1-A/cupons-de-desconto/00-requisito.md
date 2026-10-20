# Requisito — FERRO-812: Cupons de desconto

## Fonte

- **Origem**: card FERRO-812 colado no chat pelo desenvolvedor, atribuído ao solicitante.
- **Data**: 2026-10-20.
- **Autor / solicitante**: não identificado no card.
- **Fidelidade**: alta, texto escrito reproduzido integralmente abaixo.
- **Regime**: Fonte e Texto Original são imutáveis. Decomposição, perguntas e premissas são derivadas e revisáveis.

## Texto Original

<!-- IMUTÁVEL. Não editar, corrigir, resumir ou reordenar. -->

```text
CARD FERRO-812 — Cupons de desconto

Criar cupons de desconto no painel. O cupom tem um código, um tipo (porcentagem ou
valor fixo), o valor do desconto, uma data de validade e um limite de quantas vezes
pode ser usado.

Só quem é admin pode criar, editar e excluir cupom. Os outros usuários podem apenas
listar os cupons ativos.

Na hora de aplicar no pedido, o sistema valida se o cupom existe, se ainda está dentro
da validade e se não estourou o limite de usos. Se estiver tudo certo, aplica o desconto
no valor total do pedido e incrementa o contador de usos.

O código do cupom não pode se repetir.

Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois.
```

## Decomposição em Cláusulas

Uma cláusula fechada preserva a obrigação determinada pelo texto; não significa que todos os seus parâmetros estejam esclarecidos. Os recortes dependentes estão discriminados nas perguntas. As permissões de criar, editar e excluir foram separadas porque podem falhar independentemente.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|---|---|---|---|---|
| RQ-01 | Permitir cadastrar cupons no painel. | "Criar cupons de desconto no painel." | funcional | fechada |
| RQ-02 | O cupom possui código. | "O cupom tem um código" | funcional | fechada |
| RQ-03 | O cupom possui tipo porcentagem ou valor fixo. | "um tipo (porcentagem ou" / "valor fixo)" | funcional | fechada |
| RQ-04 | O cupom possui valor de desconto. | "o valor do desconto" | funcional | fechada |
| RQ-05 | O cupom possui data de validade. | "uma data de validade" | funcional | fechada |
| RQ-06 | O cupom possui limite de usos. | "um limite de quantas vezes" / "pode ser usado." | funcional | fechada |
| RQ-07 | Somente admin pode criar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-08 | Somente admin pode editar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-09 | Somente admin pode excluir cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-10 | Outros usuários podem listar cupons, sem poderes de manutenção. | "Os outros usuários podem apenas" / "listar os cupons ativos." | autorização | fechada |
| RQ-11 | A listagem dos outros usuários contém somente cupons ativos. | "listar os cupons ativos." | autorização | aberta — Q4 |
| RQ-12 | Ao aplicar em pedido, validar a existência do cupom. | "Na hora de aplicar no pedido, o sistema valida se o cupom existe" | funcional | aberta — Q1 |
| RQ-13 | Ao aplicar em pedido, validar a validade do cupom. | "se ainda está dentro" / "da validade" | funcional | aberta — Q1 |
| RQ-14 | Ao aplicar em pedido, validar o limite de usos. | "se não estourou o limite de usos." | funcional | aberta — Q1 |
| RQ-15 | Com as validações satisfeitas, descontar do total do pedido. | "Se estiver tudo certo, aplica o desconto" / "no valor total do pedido" | funcional | aberta — Q1 |
| RQ-16 | Aplicar o cupom incrementa seu contador de usos. | "incrementa o contador de usos." | funcional | aberta — Q1 |
| RQ-17 | Impedir código de cupom repetido. | "O código do cupom não pode se repetir." | restrição | fechada |
| RQ-18 | Registrar a identidade de quem aplicou o cupom para auditoria. | "Precisa registrar quem aplicou o cupom" | não-funcional | aberta — Q1 |
| RQ-19 | Registrar quando o cupom foi aplicado para auditoria. | "e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q1 |

A ausência do domínio de pedidos bloqueia integralmente a aplicação integrada e sua auditoria. Os invariantes de existência, validade, limite, alteração do total e registro de ator/data permanecem obrigações do card. Um cadastro ou motor isolado não atende essas cláusulas. A definição de ativo está integralmente pendente. As demais cláusulas preservam suas partes determinadas; as respostas abaixo não foram presumidas.

## Perguntas ao Solicitante

Somente a raia requisito aparece nesta seção. Todas permanecem sem resposta. Recomendações não autorizam comportamento. Respostas devem entrar como Adendo com fonte e texto literal. A numeração é compartilhada com a pergunta de desenho Q14 do plano.

### Rodada 1 — fronteira disponível

❓ Q1 · raia: requisito · afeta: RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18, RQ-19 · depende de: —
O projeto não contém domínio ou fluxo de pedidos identificável. A entrega deve limitar-se ao cadastro/motor sem integração, aguardando o domínio de pedidos, ou incluir a criação desse domínio?
➡️ Recomendação: seguir com o recorte mais estreito, sem criar pedidos. Cadastro e eventual motor isolado têm custo menor, mas não entregam aplicação no pedido nem sua auditoria; criar pedidos exige especificar total, moeda, estados, itens e fluxo, ampliando significativamente o escopo. Manter essas obrigações bloqueadas, sem declarar o card atendido.
**Estado**: aberta. **Recorte bloqueado**: aplicação integrada e auditoria de aplicação.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-07, RQ-08, RQ-09, RQ-10 · depende de: —
“Admin” significa administrador global, administrador da organização ou ambos? O superadministrador também está incluído? Quais perfis existentes entram em “outros usuários” e em qual painel devem listar?
➡️ Recomendação: permitir manutenção apenas ao perfil explicitamente confirmado, sem conceder exceções por nome parecido ou pelo superadministrador. Preservar a proibição de manutenção aos demais. Não ampliar acesso aos painéis administrativos para viabilizar uma listagem.
**Estado**: aberta. **Recorte bloqueado**: mapeamento de personas e painel; as três restrições de manutenção continuam determinadas.

❓ Q3 · raia: requisito · afeta: RQ-01, RQ-10, RQ-11, RQ-17 · depende de: —
Os cupons são globais ou pertencem à organização corrente? Um usuário vinculado a mais de uma organização pode listar cupons das outras durante a operação atual?
➡️ Recomendação: quando houver organizações, limitar acesso à organização corrente e recusar contexto ausente ou divergente. Não abrir leitura entre organizações. A proibição expressa de código repetido permanece; não substituí-la silenciosamente por unicidade apenas local.
**Estado**: aberta. **Recorte bloqueado**: propriedade e fronteira de dados; código exatamente repetido continua proibido.

❓ Q4 · raia: requisito · afeta: RQ-11 · depende de: —
O que define um cupom ativo: validade não vencida e usos disponíveis, ou também existe ativação/desativação manual?
➡️ Recomendação: mostrar aos demais apenas cupons com validade e saldo de usos comprovadamente disponíveis. Não adicionar ativação manual sem pedido; situações indefinidas permanecem ocultas.
**Estado**: aberta. **Recorte bloqueado**: RQ-11 integralmente.

❓ Q5 · raia: requisito · afeta: RQ-05, RQ-11, RQ-13 · depende de: —
A validade termina em um instante ou ao fim do dia informado? Qual fuso vale e o instante exatamente igual ao vencimento ainda permite uso?
➡️ Recomendação: definir um instante explícito e seu fuso; recusar uso a partir desse instante, inclusive na igualdade. Não liberar datas sem interpretação inequívoca.
**Estado**: aberta. **Recorte bloqueado**: regra de fronteira temporal, não a existência do campo.

❓ Q6 · raia: requisito · afeta: RQ-03, RQ-04, RQ-06, RQ-14, RQ-15 · depende de: —
Quais valores são válidos para percentual, desconto fixo e limite de usos? Zero, negativos, percentual acima de 100 e uso ilimitado são permitidos?
➡️ Recomendação: recusar desconto não positivo, percentual acima de 100, limite não inteiro ou não positivo e limite indefinido. Não interpretar zero como ilimitado.
**Estado**: aberta. **Recorte bloqueado**: faixas e precisão de entrada; tipos, valor e limite continuam obrigatórios.

❓ Q7 · raia: requisito · afeta: RQ-02, RQ-17 · depende de: —
Qual o tamanho máximo e o alfabeto do código? Maiúsculas/minúsculas e espaços diferenciam códigos ou devem ser normalizados?
➡️ Recomendação: aceitar somente 1–64 caracteres ASCII maiúsculos, números, hífen e sublinhado; recusar entrada fora do formato e duplicata da chave canônica. Não truncar nem normalizar silenciosamente valores conflitantes. O teto precisa valer além do formulário.
**Estado**: aberta. **Recorte bloqueado**: teto, alfabeto e equivalência; duplicatas exatas continuam proibidas.

❓ Q9 · raia: requisito · afeta: RQ-10, RQ-12, RQ-15, RQ-18 · depende de: —
“Outros usuários podem apenas listar” também impede aplicar cupom a pedido? Quem pode aplicar e sobre pedidos de quem?
➡️ Recomendação: não conceder aplicação aos usuários limitados à listagem e recusar aplicação sem ator e escopo autorizados. Não equiparar permissão de listar à de aplicar.
**Estado**: aberta. **Recorte bloqueado**: autorização da aplicação, preservando a proibição de manutenção.

❓ Q12 · raia: requisito · afeta: RQ-09, RQ-17, RQ-18, RQ-19 · depende de: —
A exclusão de cupom usado deve preservar a auditoria e reservar seu código? Por quanto tempo o histórico precisa existir e quem poderá consultá-lo?
➡️ Recomendação: não apagar usos já auditados nem liberar código usado para reutilização. Negar consulta do histórico a quem só pode listar ativos. Definir retenção e público antes de autorizar expurgo ou uma nova tela de auditoria.
**Estado**: aberta. **Recorte bloqueado**: exclusão com histórico, reutilização e consulta; a obrigação de registrar ator/data permanece.

### Fronteira futura — não antecipar respostas

Estas perguntas estão registradas, mas a rodada dependente não foi executada, pois faltam respostas aos pré-requisitos.

❓ Q8 · raia: requisito · afeta: RQ-04, RQ-15 · depende de: Q1
Qual total do pedido recebe desconto, qual moeda/precisão e qual arredondamento? O total inclui frete e tributos? O que ocorre se o desconto fixo superar o total?
➡️ Recomendação: usar total confiável calculado no servidor e a moeda do pedido; recusar base inválida, moeda incompatível e desconto que produza total negativo. Não escolher arredondamento ou componentes do total sem o contrato do pedido.
**Estado**: aberta, rodada dependente não iniciada.

❓ Q10 · raia: requisito · afeta: RQ-15, RQ-16 · depende de: Q1
Pode haver mais de um cupom por pedido ou reaplicação do mesmo cupom? Um reenvio da mesma operação pode consumir outro uso?
➡️ Recomendação: recusar acumulação e nova aplicação ao mesmo pedido; um reenvio identificado da mesma operação não deve causar novo desconto nem novo consumo. Não escolher a identidade dessa operação antes do fluxo de pedidos.
**Estado**: aberta, rodada dependente não iniciada.

❓ Q11 · raia: requisito · afeta: RQ-14, RQ-16, RQ-18, RQ-19 · depende de: Q1
Quando o uso é consumido: aplicação, fechamento ou pagamento? Cancelamento, remoção ou troca de cupom devolvem uso?
➡️ Recomendação: registrar apenas aplicação efetivada, sem consumo em falha; não devolver uso nem substituir aplicação automaticamente sem regra expressa. O card associa incremento à aplicação; qualquer mudança desse momento exige confirmação.
**Estado**: aberta, rodada dependente não iniciada.

❓ Q13 · raia: requisito · afeta: RQ-10, RQ-11, RQ-18, RQ-19 · depende de: Q3, Q4
Quem aplicou um cupom no passado continua vendo esse cupom após expirar, esgotar usos ou perder vínculo com a organização?
➡️ Recomendação: não abrir exceção à listagem de ativos nem à fronteira atual por participação histórica. Auditoria preservada não implica direito de visualizar o cupom ou o histórico.
**Estado**: aberta, rodada dependente não iniciada.

Sementes consideradas: papéis (o par admin × usuário de listagem já não autoriza manutenção de não admin; coexistência entre organizações depende de Q2/Q3), visibilidade histórica (Q13) e texto livre (Q7). Não há notificação solicitada; não foi criada pergunta sobre links.

## Premissas

| ID | Premissa | Origem | Data | Afeta | Estado |
|---|---|---|---|---|---|
| P-01 | Enquanto não houver resposta sobre pedidos, o planejamento não acrescenta um domínio de pedidos e não considera a aplicação integrada entregue por um motor isolado. | step 3 — ausência confirmada; procedimento da skill para premissa de escopo; Q1 | 2026-10-20 | RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18, RQ-19 | vigente |

Nenhuma recomendação de comportamento das perguntas foi promovida a requisito ou premissa vigente. A futura derivação de testes deverá manter abertas as cláusulas dependentes.

## Fora de Escopo (declarado)

Nenhuma exclusão funcional foi declarada pelo solicitante. A falta de domínio de pedidos é bloqueio, não exclusão definitiva das obrigações do card.

Nesta sessão, o desenvolvedor autorizou somente planejamento até o step 4. Implementação e steps seguintes estão fora da execução autorizada, sem reduzir o requisito de produto.
