# Requisito — FERRO-812: Cupons de desconto

## Fonte

- **Origem**: card FERRO-812 colado no chat pelo desenvolvedor, atribuído ao solicitante.
- **Data**: 2026-10-20.
- **Autor / solicitante**: identidade não informada.
- **Fidelidade**: alta (texto escrito, transcrição literal).
- O desenvolvedor e o solicitante estão indisponíveis nesta execução. Ausência de resposta não é aprovação.

## Texto Original

<!-- IMUTÁVEL. Não editar, não corrigir ortografia, não resumir, não reordenar. -->

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

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | Disponibilizar criação de cupons no painel. | "Criar cupons de desconto no painel." | funcional | fechada |
| RQ-02 | Cupom deve possuir código. | "O cupom tem um código" | funcional | fechada |
| RQ-03 | Cupom deve permitir os tipos porcentagem e valor fixo. | "um tipo (porcentagem ou<br>valor fixo)" | funcional | fechada |
| RQ-04 | Cupom deve possuir valor de desconto. | "o valor do desconto" | funcional | fechada |
| RQ-05 | Cupom deve possuir data de validade. | "uma data de validade" | funcional | fechada |
| RQ-06 | Cupom deve possuir limite de usos. | "um limite de quantas vezes<br>pode ser usado." | funcional | fechada |
| RQ-07 | Somente admin pode criar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-08 | Somente admin pode editar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-09 | Somente admin pode excluir cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-10 | Outros usuários podem listar cupons, sem gestão de cupons. | "Os outros usuários podem apenas<br>listar os cupons ativos." | autorização | fechada |
| RQ-11 | Listagem dos outros usuários deve conter somente cupons ativos. | "listar os cupons ativos." | autorização | aberta — Q6 |
| RQ-12 | Aplicação no pedido deve validar a existência do cupom. | "Na hora de aplicar no pedido, o sistema valida se o cupom existe" | funcional | aberta — Q1 |
| RQ-13 | Aplicação no pedido deve validar a validade do cupom. | "se ainda está dentro<br>da validade" | funcional | aberta — Q1 |
| RQ-14 | Aplicação no pedido deve validar o limite de usos. | "se não estourou o limite de usos." | funcional | aberta — Q1 |
| RQ-15 | Com as validações satisfeitas, aplicar desconto no total do pedido. | "Se estiver tudo certo, aplica o desconto<br>no valor total do pedido" | funcional | aberta — Q1 |
| RQ-16 | Aplicação bem-sucedida deve incrementar contador de usos. | "incrementa o contador de usos." | funcional | aberta — Q1 |
| RQ-17 | Código do cupom não pode se repetir. | "O código do cupom não pode se repetir." | restrição | fechada |
| RQ-18 | Registrar quem aplicou o cupom para auditoria. | "Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q1 |
| RQ-19 | Registrar quando o cupom foi aplicado para auditoria. | "Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q1 |

Os saltos de linha nos trechos da tabela aparecem como `<br>`; o Texto Original acima preserva a fonte integral.
“Fechada” indica a obrigação determinada do card, não aprovação dos recortes ainda abertos.
RQ-01, RQ-07–RQ-10 e RQ-17 preservam suas obrigações, com implantação dependente da fronteira de organização/painel em Q2.
Os limites e a apresentação do código continuam pendentes em Q11/Q12, sem suspender a obrigação de existir código único.
RQ-04–RQ-06 preservam os campos exigidos; suas fronteiras dependem de Q8–Q10.
RQ-07–RQ-09 preservam as três permissões separadas; a equivalência e a acumulação de papéis dependem de Q3–Q5.
RQ-08/RQ-09 preservam edição/exclusão, mas o tratamento de cupons já usados depende de Q15/Q16.
A existência de um domínio de pedidos é dependência integral de RQ-12–RQ-16/RQ-18/RQ-19 nesta aplicação; não se declara motor genérico como entrega dessas cláusulas.

## Perguntas ao Solicitante

Todas são da raia requisito e estão **abertas**, sem resposta e sem Adendo.
São perguntas a encaminhar ao solicitante, não ao desenvolvedor. Recomendações não autorizam comportamento.
A primeira rodada contém a fronteira sem dependências; Q5 e Q14 ficam reservadas para rodada posterior, pois dependem de respostas.
Somente o recorte dependente fica bloqueado. Não há envio externo nesta sessão.

❓ Q1 · raia: requisito · afeta: RQ-12–RQ-16, RQ-18, RQ-19 · depende de: —
A aplicação pressupõe pedidos, mas a pesquisa não encontrou essa entidade nem equivalente comercial. Devemos limitar esta entrega ao cadastro/listagem, deixando a aplicação bloqueada, ou incluir também o domínio e o fluxo de pedidos?
➡️ Recomendação: Manter o escopo mais estreito: planejar cadastro/listagem, sem criar pedidos nem anunciar aplicação entregue. Criar pedidos inclui totalização, estados, propriedade e autorização; essa ampliação exige requisito próprio.

**Estado**: aberta.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-07–RQ-11, RQ-17 · depende de: —
Os cupons pertencem à instalação inteira ou a uma organização? Em quais painéis devem ocorrer gestão e listagem?
➡️ Recomendação: Não expor cupons entre organizações. Propor gestão no painel admin e leitura no painel app, mas bloquear a escolha global/por organização e suas rotas até a resposta.

**Estado**: aberta.

❓ Q3 · raia: requisito · afeta: RQ-07, RQ-08, RQ-09 · depende de: —
O termo admin inclui somente o papel admin, também admin_organizacao, ou também master_global sem admin? O projeto concede acesso geral a master_global.
➡️ Recomendação: Reconhecer a obrigação explícita de admin; não estender escrita aos outros papéis sem confirmação. Não alterar o acesso geral do projeto para resolver esta feature.

**Estado**: aberta.

❓ Q4 · raia: requisito · afeta: RQ-07–RQ-11 · depende de: —
Uma pessoa pode acumular admin e panel_user? Nesse par, a escrita de admin prevalece ou o acesso ao cupom deve ficar somente para leitura?
➡️ Recomendação: Não criar concessão por acumulação. Manter bloqueado o recorte do par até confirmar a precedência; exigir admin no contexto autorizado.

**Estado**: aberta.

❓ Q5 · raia: requisito · afeta: RQ-07–RQ-11 · depende de: Q3
Se admin_organizacao entrar na definição de admin, uma pessoa pode acumulá-lo com panel_user na mesma organização? Nesse par, qual regra prevalece?
➡️ Recomendação: Não ampliar escrita pela combinação. Manter somente a leitura expressamente autorizada até confirmar esse par; pergunta reservada para a rodada seguinte à Q3.

**Estado**: aberta.

❓ Q6 · raia: requisito · afeta: RQ-11 · depende de: —
O que torna um cupom ativo: apenas validade, validade com saldo de usos, ou também um controle explícito de ativação?
➡️ Recomendação: Listar somente cupons não vencidos e com usos disponíveis; não criar um controle de ativação sem pedido. A recomendação não autoriza implementar esse predicado enquanto a pergunta estiver aberta.

**Estado**: aberta.

❓ Q7 · raia: requisito · afeta: RQ-10, RQ-11, RQ-18, RQ-19 · depende de: —
Quem já aplicou um cupom continua podendo vê-lo após vencer, esgotar os usos ou perder acesso à organização? Admin pode listar os inativos?
➡️ Recomendação: Não manter acesso histórico para usuário comum nem ampliar sua listagem além dos ativos. Não abrir consulta de inativos ou auditoria sem autorização expressa.

**Estado**: aberta.

❓ Q8 · raia: requisito · afeta: RQ-05, RQ-13 · depende de: —
A validade termina no início ou no fim da data informada, em qual fuso, e o instante exatamente igual ao vencimento ainda é válido?
➡️ Recomendação: Usar America/Sao_Paulo para a data de negócio e converter para instante inequívoco; recusar no instante de vencimento. A fronteira temporal permanece pendente.

**Estado**: aberta.

❓ Q9 · raia: requisito · afeta: RQ-04, RQ-06, RQ-15 · depende de: —
Quais valores são permitidos para porcentagem, desconto fixo e limite de usos? Como tratar desconto fixo maior que o total?
➡️ Recomendação: Recusar desconto não positivo, porcentagem acima de 100, limite não positivo/não inteiro e desconto que deixe total negativo. Não interpretar zero como ilimitado sem confirmação.

**Estado**: aberta.

❓ Q10 · raia: requisito · afeta: RQ-04, RQ-15 · depende de: —
Qual moeda, precisão e regra de arredondamento devemos usar? O total inclui frete, impostos e descontos anteriores?
➡️ Recomendação: Não aplicar desconto sem base monetária e arredondamento definidos. Propor cálculo decimal exato, sem float, sobre o total oficial do pedido; não inventar componentes desse total.

**Estado**: aberta.

❓ Q11 · raia: requisito · afeta: RQ-02, RQ-17 · depende de: —
Códigos com diferenças de maiúsculas/minúsculas, acentos ou espaços são considerados iguais? A proibição de repetição vale inclusive após exclusão?
➡️ Recomendação: Rejeitar colisões após trim e uniformização de caixa; não reciclar código excluído até confirmar a regra. Não escolher collation, índice ou normalização definitiva por suposição.

**Estado**: aberta.

❓ Q12 · raia: requisito · afeta: RQ-02 · depende de: —
Qual o teto e o conjunto de caracteres do código do cupom? A mesma restrição deve valer fora do formulário?
➡️ Recomendação: Propor código de até 64 caracteres ASCII alfanuméricos e hífen, validado também no servidor. Rejeitar entradas fora do contrato confirmado; o teto proposto ainda não é requisito.

**Estado**: aberta.

❓ Q13 · raia: requisito · afeta: RQ-10, RQ-12–RQ-16, RQ-18 · depende de: —
A frase outros usuários podem apenas listar restringe somente a gestão dos cupons ou também proíbe esses usuários de aplicá-los? Quem pode aplicar e em quais pedidos?
➡️ Recomendação: Não conceder aplicação a perfil nem pedido não autorizados. Manter o ponto de aplicação fechado até definir ator e propriedade do pedido.

**Estado**: aberta.

❓ Q14 · raia: requisito · afeta: RQ-14, RQ-15, RQ-16 · depende de: Q1
Um pedido pode receber mais de um cupom ou o mesmo cupom novamente? Retentativa e cancelamento devolvem ou consomem usos?
➡️ Recomendação: Não acumular cupons, não descontar nem incrementar novamente em retentativa e não devolver usos automaticamente. Essas direções de comportamento dependem do solicitante.

**Estado**: aberta.

❓ Q15 · raia: requisito · afeta: RQ-09, RQ-18, RQ-19 · depende de: —
A trilha deve sobreviver à exclusão de cupom/usuário? Por quanto tempo, quem pode consultá-la e registrar tentativas recusadas também faz parte do pedido?
➡️ Recomendação: Preservar autoria e instante dos usos bem-sucedidos, sem cascata de exclusão nem exposição a usuário comum. Não instituir expurgo nem ampliar o conteúdo da trilha antes da resposta.

**Estado**: aberta.

❓ Q16 · raia: requisito · afeta: RQ-08, RQ-14, RQ-16, RQ-18, RQ-19 · depende de: —
Depois do primeiro uso, admin pode alterar código, tipo, valor, validade ou reduzir o limite abaixo do contador já consumido?
➡️ Recomendação: Não reescrever histórico nem zerar o contador em edição; bloquear alterações que invalidem usos registrados até confirmar a política de edição.

**Estado**: aberta.


### Sementes consideradas

- Papéis: Q4 examina admin × panel_user; Q5 examina admin_organizacao × panel_user, condicionada a Q3. Outros pares só entram se Q3 criar uma distinção observável; não se altera a atribuição de papéis já existente no projeto.
- Visibilidade atual e participação histórica: Q6/Q7. Aplicação e disputa pelo último uso não criam direito histórico de listagem.
- Texto livre: código em Q11/Q12, inclusive validação fora do formulário.
- Notificação: o card não pede envio de notificação; não foi inventado link, destinatário ou fluxo.

## Premissas

| ID | Premissa | Origem | Data | Afeta | Estado |
|----|----------|--------|------|-------|--------|
| P-01 | Enquanto Q1 não for respondida, o planejamento mantém o escopo mais estreito e não cria domínio de pedidos nem declara sua aplicação entregue. | step 0 — procedimento de entidade pressuposta e ausente, confirmado na pesquisa do step 3 | 2026-10-20 | RQ-12–RQ-16, RQ-18, RQ-19 | vigente |

Nenhuma recomendação aberta foi promovida a requisito ou a premissa de comportamento aceita.

## Fora de Escopo (declarado)

- Nenhum escopo funcional foi explicitamente excluído pelo solicitante.
- A limitação desta sessão a planejamento não elimina as obrigações de aplicação e auditoria do card.

