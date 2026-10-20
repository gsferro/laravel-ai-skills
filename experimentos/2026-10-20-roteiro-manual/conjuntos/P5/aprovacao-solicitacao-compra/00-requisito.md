# Requisito — FERRO-830: Fluxo de aprovação de solicitação de compra

## Fonte

- **Origem**: card FERRO-830 escrito pelo solicitante e colado no chat pelo desenvolvedor.
- **Data**: 2026-10-20.
- **Autor / solicitante**: não identificado no card; não houve contato com o solicitante nesta execução.
- **Fidelidade**: alta (texto escrito, transcrito integralmente).
- **Captura**: step 0, em memória antes de descobrir branch, nomear a feature ou pesquisar o projeto. Persistido no step 4 após leitura do template.

## Texto Original

<!-- IMUTÁVEL. Não editar, não corrigir ortografia, não resumir, não reordenar. -->

```text
CARD FERRO-830 — Fluxo de aprovação de solicitação de compra

O solicitante cria uma solicitação de compra com descrição, valor e centro de custo.
Enquanto está em rascunho ele pode editar e excluir.

Quando envia, a solicitação vai para o gestor do centro de custo aprovar. Se o valor
for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor.

O gestor pode aprovar ou rejeitar. Na rejeição a justificativa é obrigatória.
Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo.
Depois de aprovada não pode mais mexer.

O solicitante pode cancelar a qualquer momento antes da aprovação final.

Mostrar na tela o status atual e quem aprovou cada etapa.
Notificar por e-mail o próximo aprovador.
```

## Decomposição em Cláusulas

Derivada e revisável. “Fechada” identifica a obrigação determinada pelo card; não significa implementação ou aceite. Perguntas que atingem apenas uma situação particular bloqueiam somente esse recorte. O encaminhamento integral e a associação ao centro de custo dependem da fonte inexistente no projeto, por isso RQ-02 e RQ-05 ficam abertas.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | Criar solicitação com descrição e valor. | “O solicitante cria uma solicitação de compra com descrição, valor e centro de custo.” | funcional | fechada |
| RQ-02 | Associar a solicitação a um centro de custo. | “O solicitante cria uma solicitação de compra com descrição, valor e centro de custo.” | funcional | aberta — Q1 |
| RQ-03 | Permitir ao solicitante editar sua solicitação enquanto estiver em rascunho. | “Enquanto está em rascunho ele pode editar e excluir.” | autorização | fechada |
| RQ-04 | Permitir ao solicitante excluir sua solicitação enquanto estiver em rascunho. | “Enquanto está em rascunho ele pode editar e excluir.” | autorização | fechada |
| RQ-05 | Ao enviar, encaminhar ao gestor do centro de custo para aprovação. | “Quando envia, a solicitação vai para o gestor do centro de custo aprovar.” | funcional | aberta — Q1 |
| RQ-06 | Exigir também aprovação do diretor quando o valor for acima de R$ 5.000. | “Se o valor<br>for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor.” | funcional | fechada |
| RQ-07 | Exigir que a aprovação do diretor ocorra depois da aprovação do gestor. | “Se o valor<br>for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor.” | restrição | fechada |
| RQ-08 | Permitir ao gestor aprovar a solicitação encaminhada. | “O gestor pode aprovar ou rejeitar.” | autorização | fechada |
| RQ-09 | Permitir ao gestor rejeitar a solicitação encaminhada. | “O gestor pode aprovar ou rejeitar.” | autorização | fechada |
| RQ-10 | Exigir justificativa na rejeição. | “Na rejeição a justificativa é obrigatória.” | restrição | fechada |
| RQ-11 | Devolver a solicitação rejeitada ao estado de rascunho para correção pelo solicitante. | “Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo.” | funcional | fechada |
| RQ-12 | Permitir ao solicitante enviar novamente após rejeição e correção. | “Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo.” | funcional | fechada |
| RQ-13 | Impedir alterações depois da aprovação final. | “Depois de aprovada não pode mais mexer.” | restrição | fechada |
| RQ-14 | Permitir ao solicitante cancelar a qualquer momento antes da aprovação final. | “O solicitante pode cancelar a qualquer momento antes da aprovação final.” | autorização | fechada |
| RQ-15 | Mostrar o status atual na tela. | “Mostrar na tela o status atual e quem aprovou cada etapa.” | funcional | fechada |
| RQ-16 | Mostrar quem aprovou cada etapa na tela. | “Mostrar na tela o status atual e quem aprovou cada etapa.” | funcional | fechada |
| RQ-17 | Notificar por e-mail o próximo aprovador. | “Notificar por e-mail o próximo aprovador.” | funcional | fechada |

“Aprovada” em RQ-13 é a aprovação final, lendo a frase junto da condição de diretor e do direito expresso de cancelar antes da aprovação final. Para R$ 5.000 exatos, “acima” não exige diretor. A edição após rejeição já está coberta por RQ-03; RQ-11 especifica o retorno de estado, sem duplicar essa permissão.

## Perguntas ao Solicitante

Somente raia requisito. Não houve resposta nem autorização para o desenvolvedor decidir pelo solicitante. Respostas futuras entram como Adendo, com fonte e texto literal. Recomendações não são requisitos confirmados. RQ-02 e RQ-05 não podem ser implementadas até resposta a Q1; as demais obrigações determinadas permanecem no plano, com seus recortes indecididos discriminados.

| ID | Pergunta | Afeta | Recomendação | Estado |
|----|----------|-------|--------------|--------|
| Q1 | O projeto não contém cadastro de centro de custo nem vínculo de gestor/diretor. Esta entrega deve criar esses cadastros e sua administração, ou consumir uma fonte autorizada fornecida por outra entrega? | RQ-02, RQ-05; recortes de RQ-06 e RQ-17 | Manter esses cadastros fora da execução atual e aguardar identificação da fonte autorizada. Criar cadastro adiciona persistência, UI e autorização; integrar outra fonte exige contrato e disponibilidade. Não reduzir silenciosamente o card a um motor nem inventar cadastros. | aberta; fronteira |
| Q2 | O solicitante pode ser também o gestor que aprova a própria solicitação? | RQ-08, RQ-05 | Não permitir autoaprovação pelo gestor; manter a operação bloqueada nesse caso até definir aprovador distinto. | aberta; fronteira |
| Q3 | O solicitante pode ser também o diretor que aprova a própria solicitação? | RQ-06, RQ-07 | Não permitir autoaprovação pelo diretor; exigir pessoa distinta. | aberta; fronteira |
| Q4 | Uma mesma pessoa pode aprovar como gestor e como diretor na mesma solicitação? | RQ-06, RQ-07, RQ-08 | Não acumular as duas aprovações; bloquear a segunda etapa quando não houver pessoa distinta. | aberta; fronteira |
| Q5 | Quem pode consultar cada solicitação e seus aprovadores: solicitante, aprovador atual, todos do centro de custo ou administradores? Quem já participou continua vendo depois de perder o papel ou depois de outra pessoa concluir a etapa? | RQ-15, RQ-16 | Restringir ao solicitante e ao aprovador atual, no contexto organizacional permitido. Não conceder acesso por participação histórica ou perfil administrativo sem definição explícita. Revalidar acesso após qualquer corrida. | aberta; fronteira |
| Q6 | Para onde deve levar o link do e-mail e o que mostrar quando o destinatário já não tiver acesso ou a etapa já tiver terminado? | RQ-17, RQ-15, RQ-16 | Levar ao detalhe autenticado da solicitação, com autorização novamente verificada. Sem acesso, mostrar retorno seguro para a lista permitida, sem expor os dados nem executar aprovação pelo link. | aberta; posterior; depende de Q5 |
| Q7 | Qual é o limite de caracteres da descrição, inclusive em chamadas fora do formulário? | RQ-01, RQ-03 | Limitar a 2.000 caracteres após remover espaços nas extremidades, tanto no domínio quanto no formulário; recusar excesso sem truncar. | aberta; fronteira |
| Q8 | Qual é o limite de caracteres da justificativa da rejeição, inclusive fora do formulário? Texto só com espaços deve contar como vazio? | RQ-10 | Exigir conteúdo após trim e limitar a 1.000 caracteres no domínio e no formulário; recusar vazio ou excesso sem truncar. | aberta; fronteira |
| Q9 | O valor deve ser positivo, em reais com até duas casas decimais? Qual é o maior valor permitido? | RQ-01, RQ-06 | Aceitar somente BRL positivo com até duas casas e teto de R$ 999.999.999,99; recusar entradas fora desse domínio. O limite de aprovação já é determinado: diretor somente acima de R$ 5.000. | aberta; fronteira |
| Q10 | O diretor também pode rejeitar? O card só atribui rejeição expressamente ao gestor. | RQ-06, RQ-09, RQ-10, RQ-11 | Não oferecer rejeição ao diretor enquanto isso não for autorizado; manter somente a aprovação dessa etapa expressamente pedida. | aberta; fronteira |
| Q11 | Ao reenviar após rejeição, o ciclo de aprovações recomeça? Aprovações e justificativas de tentativas anteriores devem continuar visíveis, e para quem? | RQ-12, RQ-16 | Não reutilizar aprovações anteriores. Reter a evidência existente sem apagá-la, mas não exibir tentativas anteriores sem recorte de visibilidade autorizado. | aberta; fronteira |
| Q12 | Se o gestor ou o diretor mudar enquanto a solicitação aguarda decisão, mantém-se o destinatário original ou o novo assume a etapa? | RQ-05, RQ-06, RQ-17 | Não transferir poderes automaticamente. Bloquear nova decisão diante de divergência entre atribuição e responsável atual até definir a substituição autorizada. | aberta; posterior; depende de Q1 |
| Q13 | O que fazer quando a fonte não indicar aprovador válido ou indicar alguém inativo ou fora do contexto autorizado? | RQ-05, RQ-06, RQ-17 | Recusar envio ou avanço que dependa desse aprovador, sem pular etapa nem escolher substituto automaticamente. | aberta; posterior; depende de Q1 |
| Q14 | Depois de cancelar, a solicitação fica encerrada ou o solicitante pode reabrir e reenviar? | RQ-14 | Encerrar o registro cancelado; não permitir reabertura sem autorização expressa. | aberta; fronteira |
| Q15 | Se o e-mail ainda estiver na fila quando a solicitação for cancelada ou a etapa for concluída, ele ainda deve ser enviado? | RQ-17, RQ-14 | Não enviar notificação obsoleta; verificar etapa e destinatário antes de entregar ao transporte. | aberta; fronteira |
| Q16 | Se o envio de e-mail falhar, o encaminhamento permanece pendente para nova tentativa ou a transição deve ser recusada? | RQ-17, RQ-05, RQ-06 | Não considerar notificação entregue nem liberar aprovação por falha de comunicação. Preservar a transição registrada e uma pendência de entrega para tentativa controlada, sem autoaprovação; confirmar esse comportamento antes de implementá-lo. | aberta; fronteira |

### Q1

❓ Q1 · raia: requisito · afeta: RQ-02, RQ-05; recortes de RQ-06 e RQ-17 · depende de: —
O projeto não contém cadastro de centro de custo nem vínculo de gestor/diretor. Esta entrega deve criar esses cadastros e sua administração, ou consumir uma fonte autorizada fornecida por outra entrega?
➡️ Recomendação: Manter esses cadastros fora da execução atual e aguardar identificação da fonte autorizada. Criar cadastro adiciona persistência, UI e autorização; integrar outra fonte exige contrato e disponibilidade. Não reduzir silenciosamente o card a um motor nem inventar cadastros.

Recorte dependente: escopo integral de RQ-02 e RQ-05; resolução de aprovadores nas demais. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q2

❓ Q2 · raia: requisito · afeta: RQ-08, RQ-05 · depende de: —
O solicitante pode ser também o gestor que aprova a própria solicitação?
➡️ Recomendação: Não permitir autoaprovação pelo gestor; manter a operação bloqueada nesse caso até definir aprovador distinto.

Recorte dependente: sobreposição solicitante × gestor. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q3

❓ Q3 · raia: requisito · afeta: RQ-06, RQ-07 · depende de: —
O solicitante pode ser também o diretor que aprova a própria solicitação?
➡️ Recomendação: Não permitir autoaprovação pelo diretor; exigir pessoa distinta.

Recorte dependente: sobreposição solicitante × diretor. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q4

❓ Q4 · raia: requisito · afeta: RQ-06, RQ-07, RQ-08 · depende de: —
Uma mesma pessoa pode aprovar como gestor e como diretor na mesma solicitação?
➡️ Recomendação: Não acumular as duas aprovações; bloquear a segunda etapa quando não houver pessoa distinta.

Recorte dependente: sobreposição gestor × diretor. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q5

❓ Q5 · raia: requisito · afeta: RQ-15, RQ-16 · depende de: —
Quem pode consultar cada solicitação e seus aprovadores: solicitante, aprovador atual, todos do centro de custo ou administradores? Quem já participou continua vendo depois de perder o papel ou depois de outra pessoa concluir a etapa?
➡️ Recomendação: Restringir ao solicitante e ao aprovador atual, no contexto organizacional permitido. Não conceder acesso por participação histórica ou perfil administrativo sem definição explícita. Revalidar acesso após qualquer corrida.

Recorte dependente: visibilidade, participação histórica e consulta após conflito. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q6

❓ Q6 · raia: requisito · afeta: RQ-17, RQ-15, RQ-16 · depende de: Q5
Para onde deve levar o link do e-mail e o que mostrar quando o destinatário já não tiver acesso ou a etapa já tiver terminado?
➡️ Recomendação: Levar ao detalhe autenticado da solicitação, com autorização novamente verificada. Sem acesso, mostrar retorno seguro para a lista permitida, sem expor os dados nem executar aprovação pelo link.

Recorte dependente: destino do link e retorno sem acesso. Estado: aberta; rodada posterior, não apresentada enquanto a dependência permanecer aberta.

### Q7

❓ Q7 · raia: requisito · afeta: RQ-01, RQ-03 · depende de: —
Qual é o limite de caracteres da descrição, inclusive em chamadas fora do formulário?
➡️ Recomendação: Limitar a 2.000 caracteres após remover espaços nas extremidades, tanto no domínio quanto no formulário; recusar excesso sem truncar.

Recorte dependente: teto e normalização da descrição. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q8

❓ Q8 · raia: requisito · afeta: RQ-10 · depende de: —
Qual é o limite de caracteres da justificativa da rejeição, inclusive fora do formulário? Texto só com espaços deve contar como vazio?
➡️ Recomendação: Exigir conteúdo após trim e limitar a 1.000 caracteres no domínio e no formulário; recusar vazio ou excesso sem truncar.

Recorte dependente: teto e definição de justificativa vazia. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q9

❓ Q9 · raia: requisito · afeta: RQ-01, RQ-06 · depende de: —
O valor deve ser positivo, em reais com até duas casas decimais? Qual é o maior valor permitido?
➡️ Recomendação: Aceitar somente BRL positivo com até duas casas e teto de R$ 999.999.999,99; recusar entradas fora desse domínio. O limite de aprovação já é determinado: diretor somente acima de R$ 5.000.

Recorte dependente: domínio monetário; não reabre a comparação expressa no card. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q10

❓ Q10 · raia: requisito · afeta: RQ-06, RQ-09, RQ-10, RQ-11 · depende de: —
O diretor também pode rejeitar? O card só atribui rejeição expressamente ao gestor.
➡️ Recomendação: Não oferecer rejeição ao diretor enquanto isso não for autorizado; manter somente a aprovação dessa etapa expressamente pedida.

Recorte dependente: ação de rejeitar pelo diretor. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q11

❓ Q11 · raia: requisito · afeta: RQ-12, RQ-16 · depende de: —
Ao reenviar após rejeição, o ciclo de aprovações recomeça? Aprovações e justificativas de tentativas anteriores devem continuar visíveis, e para quem?
➡️ Recomendação: Não reutilizar aprovações anteriores. Reter a evidência existente sem apagá-la, mas não exibir tentativas anteriores sem recorte de visibilidade autorizado.

Recorte dependente: validade e histórico entre tentativas. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q12

❓ Q12 · raia: requisito · afeta: RQ-05, RQ-06, RQ-17 · depende de: Q1
Se o gestor ou o diretor mudar enquanto a solicitação aguarda decisão, mantém-se o destinatário original ou o novo assume a etapa?
➡️ Recomendação: Não transferir poderes automaticamente. Bloquear nova decisão diante de divergência entre atribuição e responsável atual até definir a substituição autorizada.

Recorte dependente: troca de aprovador durante etapa. Estado: aberta; rodada posterior, não apresentada enquanto a dependência permanecer aberta.

### Q13

❓ Q13 · raia: requisito · afeta: RQ-05, RQ-06, RQ-17 · depende de: Q1
O que fazer quando a fonte não indicar aprovador válido ou indicar alguém inativo ou fora do contexto autorizado?
➡️ Recomendação: Recusar envio ou avanço que dependa desse aprovador, sem pular etapa nem escolher substituto automaticamente.

Recorte dependente: ausência ou invalidade de aprovador. Estado: aberta; rodada posterior, não apresentada enquanto a dependência permanecer aberta.

### Q14

❓ Q14 · raia: requisito · afeta: RQ-14 · depende de: —
Depois de cancelar, a solicitação fica encerrada ou o solicitante pode reabrir e reenviar?
➡️ Recomendação: Encerrar o registro cancelado; não permitir reabertura sem autorização expressa.

Recorte dependente: transições posteriores ao cancelamento. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q15

❓ Q15 · raia: requisito · afeta: RQ-17, RQ-14 · depende de: —
Se o e-mail ainda estiver na fila quando a solicitação for cancelada ou a etapa for concluída, ele ainda deve ser enviado?
➡️ Recomendação: Não enviar notificação obsoleta; verificar etapa e destinatário antes de entregar ao transporte.

Recorte dependente: notificação que ficou obsoleta na fila. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

### Q16

❓ Q16 · raia: requisito · afeta: RQ-17, RQ-05, RQ-06 · depende de: —
Se o envio de e-mail falhar, o encaminhamento permanece pendente para nova tentativa ou a transição deve ser recusada?
➡️ Recomendação: Não considerar notificação entregue nem liberar aprovação por falha de comunicação. Preservar a transição registrada e uma pendência de entrega para tentativa controlada, sem autoaprovação; confirmar esse comportamento antes de implementá-lo.

Recorte dependente: resultado observável da falha de comunicação. Estado: aberta; fronteira da rodada 1, registrada para encaminhamento ao solicitante.

## Premissas

Nenhuma premissa de comportamento vigente. As recomendações acima não foram promovidas a premissas por falta de resposta. A fonte de centro de custo e de aprovadores não foi inventada; a execução desse recorte fica bloqueada, sem suprimir a obrigação pedida.

## Fora de Escopo (declarado)

Nenhum item de produto foi explicitamente excluído pelo solicitante. O escopo dos cadastros faltantes aguarda Q1. A limitação desta sessão a planejamento não altera o requisito do produto.

