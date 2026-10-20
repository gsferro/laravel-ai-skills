# Requisito — FERRO-830: Fluxo de aprovação de solicitação de compra

## Fonte

- **Origem**: CARD FERRO-830 colado no chat pelo desenvolvedor, apresentado como texto do solicitante.
- **Data**: 2026-10-20.
- **Autor / solicitante**: não informado; desenvolvedor e solicitante indisponíveis nesta execução.
- **Fidelidade**: alta (texto escrito, transcrição literal).
- **Regime**: Fonte e Texto Original imutáveis. Respostas futuras entram como Adendo, com fonte e texto literal.

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

A decomposição é derivada e revisável. “Fechada” significa obrigação determinada pelo texto, não implementada nem homologada.
A inexistência das entidades pressupostas deixa RQ-01 e RQ-04 abertas por Q1. As demais obrigações permanecem especificadas; sua integração depende da resolução de Q1.
Perguntas sobre casos não definidos bloqueiam somente esses recortes, sem apagar o comportamento determinado de cada cláusula.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | O solicitante cria uma solicitação de compra. | "O solicitante cria uma solicitação de compra" | funcional | aberta — Q1 |
| RQ-02 | A solicitação contém descrição. | "com descrição, valor e centro de custo." | funcional | fechada |
| RQ-03 | A solicitação contém valor. | "com descrição, valor e centro de custo." | funcional | fechada |
| RQ-04 | A solicitação contém centro de custo. | "com descrição, valor e centro de custo." | funcional | aberta — Q1 |
| RQ-05 | O solicitante pode editar enquanto a solicitação está em rascunho. | "Enquanto está em rascunho ele pode editar e excluir." | autorização | fechada |
| RQ-06 | O solicitante pode excluir enquanto a solicitação está em rascunho. | "Enquanto está em rascunho ele pode editar e excluir." | autorização | fechada |
| RQ-07 | Ao enviar, a solicitação vai para o gestor do centro de custo aprovar. | "Quando envia, a solicitação vai para o gestor do centro de custo aprovar." | funcional | fechada |
| RQ-08 | Valor acima de R$ 5.000 exige aprovação do diretor. | "Se o valor<br>for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor." | funcional | fechada |
| RQ-09 | A aprovação do diretor sucede a aprovação do gestor. | "precisa também da aprovação do diretor, depois do gestor." | restrição | fechada |
| RQ-10 | O gestor pode aprovar a solicitação. | "O gestor pode aprovar ou rejeitar." | autorização | fechada |
| RQ-11 | O gestor pode rejeitar a solicitação. | "O gestor pode aprovar ou rejeitar." | autorização | fechada |
| RQ-12 | A rejeição exige justificativa. | "Na rejeição a justificativa é obrigatória." | restrição | fechada |
| RQ-13 | A solicitação rejeitada volta para rascunho. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | funcional | fechada |
| RQ-14 | O solicitante pode corrigir a solicitação rejeitada. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | autorização | fechada |
| RQ-15 | O solicitante pode reenviar a solicitação rejeitada. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | funcional | fechada |
| RQ-16 | A solicitação aprovada fica imutável. | "Depois de aprovada não pode mais mexer." | restrição | fechada |
| RQ-17 | O solicitante pode cancelar a qualquer momento antes da aprovação final. | "O solicitante pode cancelar a qualquer momento antes da aprovação final." | autorização | fechada |
| RQ-18 | A tela mostra o status atual. | "Mostrar na tela o status atual e quem aprovou cada etapa." | funcional | fechada |
| RQ-19 | A tela mostra quem aprovou cada etapa. | "Mostrar na tela o status atual e quem aprovou cada etapa." | funcional | fechada |
| RQ-20 | O próximo aprovador recebe notificação por e-mail. | "Notificar por e-mail o próximo aprovador." | funcional | fechada |

Em RQ-08, o trecho literal preserva a quebra de linha da origem, representada por `<br>` apenas na tabela.
O valor exatamente igual a R$ 5.000 não está “acima”; a segunda etapa é exigida quando o valor o ultrapassa.
RQ-16 conserva a imutabilidade após aprovação final. A aprovação do gestor em fluxo que ainda exige diretor não elimina o direito de cancelar de RQ-17.

## Perguntas ao Solicitante

**Raia: requisito em todas as linhas abaixo.** Recomendações não são respostas e não autorizam implementação do recorte indefinido.
Nenhuma pergunta foi respondida ou entregue externamente ao solicitante; estão preparadas para encaminhamento pelo desenvolvedor.

| ID | Pergunta | Afeta | Recomendação | Estado |
|----|----------|-------|--------------|--------|
| Q1 | Não localizamos solicitações de compra, centros de custo nem vínculos de aprovadores. Devemos integrar um módulo existente a ser indicado ou incluir sua criação e seus cadastros neste card? Integrar exige identificar o contrato; criar amplia schema, telas e gestão dos responsáveis. | RQ-01, RQ-04; integração de RQ-02–RQ-20 | manter o escopo mais estreito e aguardar a indicação do módulo; não criar as entidades ausentes nem substituir a entrega por um motor isolado. | aberta |
| Q2 | Como são designados gestor do centro e diretor, em qual organização atuam, e o que acontece quando faltam, estão inativos ou há mais de um candidato? | RQ-04, RQ-07–RQ-11, RQ-20 | exigir um responsável ativo e explicitamente designado por etapa na mesma organização; bloquear o envio ou avanço sem atribuição inequívoca, sem usar permissões administrativas como substituto. | aberta |
| Q3 | Se o responsável mudar durante uma aprovação, as solicitações pendentes ficam com o anterior ou passam ao substituto? Quem pode efetuar essa substituição? | RQ-07–RQ-11, RQ-20 | não transferir nem permitir decisão por pessoa diferente da designada sem uma regra explícita de substituição. | aberta — depende de Q2 |
| Q4 | O solicitante pode também atuar como gestor aprovador da própria solicitação? | RQ-07, RQ-10, RQ-11 | não permitir autoaprovação; bloquear o avanço que dependa dela até indicar outro gestor autorizado. | aberta |
| Q5 | O solicitante pode também atuar como diretor aprovador da própria solicitação? | RQ-08, RQ-09 | não permitir autoaprovação; bloquear a etapa sem outro diretor autorizado. | aberta |
| Q6 | A mesma pessoa pode aprovar como gestor e como diretor na mesma solicitação? | RQ-08–RQ-10, RQ-19 | exigir pessoas distintas nas duas etapas; não dispensar nem concluir automaticamente a etapa do diretor. | aberta |
| Q7 | O diretor também pode rejeitar? Nesse caso, exige justificativa e devolve ao rascunho como na rejeição do gestor? | RQ-08, RQ-12, RQ-13 | não habilitar rejeição do diretor sem confirmação; manter determinada a rejeição do gestor com justificativa e retorno ao rascunho. | aberta |
| Q8 | No reenvio após rejeição, todas as aprovações anteriores perdem validade? A tela mostra apenas o ciclo atual ou também os anteriores? | RQ-13–RQ-15, RQ-19 | não reutilizar aprovações anteriores; propor novo ciclo integral e manter o passado separado, sem apagar decisões ou apresentá-las como aprovações atuais. | aberta |
| Q9 | Uma solicitação cancelada pode ser reaberta ou editada, ou o cancelamento encerra seu fluxo? | RQ-17, RQ-18 | não permitir reabertura nem edição após cancelar até existir regra explícita; não impedir o cancelamento antes da aprovação final. | aberta |
| Q10 | Quem pode listar e abrir cada solicitação: apenas o solicitante e o aprovador atual, todos do centro, diretor ou administradores? Qual o recorte por organização? | RQ-18, RQ-19 | restringir a leitura ao solicitante e ao responsável atual explicitamente autorizado no recorte da organização; não conceder leitura ampla por papel genérico. | aberta |
| Q11 | Um aprovador que já participou ou perdeu uma disputa de decisão continua vendo a solicitação após avanço, rejeição, cancelamento ou troca de responsável? O que ele vê? | RQ-18, RQ-19 | não manter acesso por participação histórica nem revelar resultado após perda de autorização sem permissão explícita; quando ainda autorizado, recarregar o estado atual. | aberta — depende de Q10 |
| Q12 | O e-mail deve incluir um link? Para qual tela ele leva, inclusive quando o usuário clica após cancelamento, avanço de etapa ou perda de acesso? | RQ-20; leitura de RQ-18, RQ-19 | se houver link, usar detalhe autenticado e revalidar o acesso no clique; negar conteúdo quando a autorização tiver expirado, com saída para a lista permitida. | aberta |
| Q13 | Qual o tamanho máximo da descrição e ela deve ser preenchida já no rascunho ou somente no envio? | RQ-02, RQ-05, RQ-14 | propor texto simples de até 2.000 caracteres, com validação também na camada de gravação; não aceitar valores fora do limite que vier a ser confirmado. | aberta |
| Q14 | Qual o tamanho máximo da justificativa e texto contendo somente espaços deve ser recusado? | RQ-12 | propor até 2.000 caracteres e recusar justificativa vazia após remover espaços nas bordas; exigir o conteúdo na camada de domínio. | aberta |
| Q15 | Quais valores mínimo e máximo são permitidos? Aceita zero, negativo ou mais de duas casas decimais? O valor é sempre em reais? | RQ-03, RQ-08 | recusar zero, negativos e precisão excedente; propor BRL com centavos exatos e teto explícito, sem arredondamento silencioso. | aberta |
| Q16 | A exclusão de um rascunho que já teve rejeição deve apagar definitivamente as decisões ou apenas retirar a solicitação da operação preservando seu histórico? | RQ-06, RQ-13, RQ-19 | não apagar decisões históricas sem confirmação; propor retirada da operação com preservação da trilha, mantendo o direito de excluir rascunhos. | aberta |
| Q17 | As regras de dono, aprovador designado e imutabilidade valem também para master_global e administradores, ou existe alguma exceção de negócio? | RQ-05–RQ-11, RQ-16, RQ-17–RQ-19 | não permitir que privilégios administrativos dispensem dono, etapa ou imutabilidade; não alterar o superusuário global para os demais módulos. | aberta |
| Q18 | Após falha de entrega, por quanto tempo tentar novamente e quem deve saber da falha? Um e-mail ainda pendente deve sair se a etapa já mudou ou a solicitação foi cancelada? | RQ-20 | não enviar convocação de etapa obsoleta; propor tentativas limitadas, falha visível na operação e nenhuma reversão silenciosa da decisão de compra. | aberta |

### Rodadas e recortes bloqueados

Rodada 1 preparada: perguntas sem dependência. Q3 depende de Q2; Q11 depende de Q10 e ficam para a rodada seguinte, sem simular respostas.
A numeração é única entre as raias; perguntas de desenho não são respondidas nem registradas nesta seção.

- **Q1** — Criação da solicitação e origem do centro; toda integração persistente depende deste escopo.
- **Q2** — Resolução concreta de responsáveis e tratamento de configuração inválida; a sequência gestor/diretor permanece determinada.
- **Q3** — Troca de aprovador com etapa pendente; pergunta da rodada seguinte, ainda não apresentada como fronteira respondida.
- **Q4** — Par solicitante × gestor; não altera o direito de criar rascunho.
- **Q5** — Par solicitante × diretor.
- **Q6** — Par gestor × diretor; ordem e necessidade das duas etapas acima do limiar continuam determinadas.
- **Q7** — Rejeição pelo diretor; não bloquear a aprovação do diretor por esta pergunta.
- **Q8** — Validade das decisões e apresentação por ciclo; direito de corrigir e reenviar continua determinado.
- **Q9** — Comportamento posterior ao cancelamento.
- **Q10** — Público e escopo da leitura; mostrar status e identidade de aprovadores aos leitores autorizados permanece determinado.
- **Q11** — Visibilidade histórica e resposta ao participante que perdeu a corrida; rodada seguinte.
- **Q12** — Link e destino da notificação; o envio por e-mail em si não depende da escolha de incluir link.
- **Q13** — Teto e momento de obrigatoriedade da descrição; não escolher 2.000 como requisito aprovado.
- **Q14** — Teto e definição de conteúdo válido; justificativa obrigatória permanece determinada.
- **Q15** — Domínio monetário; a comparação estrita acima de R$ 5.000 não é ambígua.
- **Q16** — Retenção após exclusão; não retirar silenciosamente a permissão de excluir rascunhos devolvidos.
- **Q17** — Exceções administrativas; invariantes de estado determinados devem ser protegidos fora do Gate::before.
- **Q18** — Obsolescência e experiência de falha de notificação; não prometer entrega exatamente uma vez ou rollback por falha de e-mail.

As respostas devem ser incorporadas como Adendo antes de remover qualquer bloqueio. Nenhuma recomendação foi promovida a requisito.
A falta de Q1 não autoriza entregar um motor isolado como cumprimento do card, nem criar cadastros pressupostos sem delimitar o escopo.

### Entrevista preparada no formato da skill

❓ Q1 · raia: requisito · afeta: RQ-01, RQ-04; integração de RQ-02–RQ-20 · depende de: —
Não localizamos solicitações de compra, centros de custo nem vínculos de aprovadores. Devemos integrar um módulo existente a ser indicado ou incluir sua criação e seus cadastros neste card? Integrar exige identificar o contrato; criar amplia schema, telas e gestão dos responsáveis.
➡️ Recomendação: manter o escopo mais estreito e aguardar a indicação do módulo; não criar as entidades ausentes nem substituir a entrega por um motor isolado.

❓ Q2 · raia: requisito · afeta: RQ-04, RQ-07–RQ-11, RQ-20 · depende de: —
Como são designados gestor do centro e diretor, em qual organização atuam, e o que acontece quando faltam, estão inativos ou há mais de um candidato?
➡️ Recomendação: exigir um responsável ativo e explicitamente designado por etapa na mesma organização; bloquear o envio ou avanço sem atribuição inequívoca, sem usar permissões administrativas como substituto.

❓ Q3 · raia: requisito · afeta: RQ-07–RQ-11, RQ-20 · depende de: Q2
Se o responsável mudar durante uma aprovação, as solicitações pendentes ficam com o anterior ou passam ao substituto? Quem pode efetuar essa substituição?
➡️ Recomendação: não transferir nem permitir decisão por pessoa diferente da designada sem uma regra explícita de substituição.

❓ Q4 · raia: requisito · afeta: RQ-07, RQ-10, RQ-11 · depende de: —
O solicitante pode também atuar como gestor aprovador da própria solicitação?
➡️ Recomendação: não permitir autoaprovação; bloquear o avanço que dependa dela até indicar outro gestor autorizado.

❓ Q5 · raia: requisito · afeta: RQ-08, RQ-09 · depende de: —
O solicitante pode também atuar como diretor aprovador da própria solicitação?
➡️ Recomendação: não permitir autoaprovação; bloquear a etapa sem outro diretor autorizado.

❓ Q6 · raia: requisito · afeta: RQ-08–RQ-10, RQ-19 · depende de: —
A mesma pessoa pode aprovar como gestor e como diretor na mesma solicitação?
➡️ Recomendação: exigir pessoas distintas nas duas etapas; não dispensar nem concluir automaticamente a etapa do diretor.

❓ Q7 · raia: requisito · afeta: RQ-08, RQ-12, RQ-13 · depende de: —
O diretor também pode rejeitar? Nesse caso, exige justificativa e devolve ao rascunho como na rejeição do gestor?
➡️ Recomendação: não habilitar rejeição do diretor sem confirmação; manter determinada a rejeição do gestor com justificativa e retorno ao rascunho.

❓ Q8 · raia: requisito · afeta: RQ-13–RQ-15, RQ-19 · depende de: —
No reenvio após rejeição, todas as aprovações anteriores perdem validade? A tela mostra apenas o ciclo atual ou também os anteriores?
➡️ Recomendação: não reutilizar aprovações anteriores; propor novo ciclo integral e manter o passado separado, sem apagar decisões ou apresentá-las como aprovações atuais.

❓ Q9 · raia: requisito · afeta: RQ-17, RQ-18 · depende de: —
Uma solicitação cancelada pode ser reaberta ou editada, ou o cancelamento encerra seu fluxo?
➡️ Recomendação: não permitir reabertura nem edição após cancelar até existir regra explícita; não impedir o cancelamento antes da aprovação final.

❓ Q10 · raia: requisito · afeta: RQ-18, RQ-19 · depende de: —
Quem pode listar e abrir cada solicitação: apenas o solicitante e o aprovador atual, todos do centro, diretor ou administradores? Qual o recorte por organização?
➡️ Recomendação: restringir a leitura ao solicitante e ao responsável atual explicitamente autorizado no recorte da organização; não conceder leitura ampla por papel genérico.

❓ Q11 · raia: requisito · afeta: RQ-18, RQ-19 · depende de: Q10
Um aprovador que já participou ou perdeu uma disputa de decisão continua vendo a solicitação após avanço, rejeição, cancelamento ou troca de responsável? O que ele vê?
➡️ Recomendação: não manter acesso por participação histórica nem revelar resultado após perda de autorização sem permissão explícita; quando ainda autorizado, recarregar o estado atual.

❓ Q12 · raia: requisito · afeta: RQ-20; leitura de RQ-18, RQ-19 · depende de: —
O e-mail deve incluir um link? Para qual tela ele leva, inclusive quando o usuário clica após cancelamento, avanço de etapa ou perda de acesso?
➡️ Recomendação: se houver link, usar detalhe autenticado e revalidar o acesso no clique; negar conteúdo quando a autorização tiver expirado, com saída para a lista permitida.

❓ Q13 · raia: requisito · afeta: RQ-02, RQ-05, RQ-14 · depende de: —
Qual o tamanho máximo da descrição e ela deve ser preenchida já no rascunho ou somente no envio?
➡️ Recomendação: propor texto simples de até 2.000 caracteres, com validação também na camada de gravação; não aceitar valores fora do limite que vier a ser confirmado.

❓ Q14 · raia: requisito · afeta: RQ-12 · depende de: —
Qual o tamanho máximo da justificativa e texto contendo somente espaços deve ser recusado?
➡️ Recomendação: propor até 2.000 caracteres e recusar justificativa vazia após remover espaços nas bordas; exigir o conteúdo na camada de domínio.

❓ Q15 · raia: requisito · afeta: RQ-03, RQ-08 · depende de: —
Quais valores mínimo e máximo são permitidos? Aceita zero, negativo ou mais de duas casas decimais? O valor é sempre em reais?
➡️ Recomendação: recusar zero, negativos e precisão excedente; propor BRL com centavos exatos e teto explícito, sem arredondamento silencioso.

❓ Q16 · raia: requisito · afeta: RQ-06, RQ-13, RQ-19 · depende de: —
A exclusão de um rascunho que já teve rejeição deve apagar definitivamente as decisões ou apenas retirar a solicitação da operação preservando seu histórico?
➡️ Recomendação: não apagar decisões históricas sem confirmação; propor retirada da operação com preservação da trilha, mantendo o direito de excluir rascunhos.

❓ Q17 · raia: requisito · afeta: RQ-05–RQ-11, RQ-16, RQ-17–RQ-19 · depende de: —
As regras de dono, aprovador designado e imutabilidade valem também para master_global e administradores, ou existe alguma exceção de negócio?
➡️ Recomendação: não permitir que privilégios administrativos dispensem dono, etapa ou imutabilidade; não alterar o superusuário global para os demais módulos.

❓ Q18 · raia: requisito · afeta: RQ-20 · depende de: —
Após falha de entrega, por quanto tempo tentar novamente e quem deve saber da falha? Um e-mail ainda pendente deve sair se a etapa já mudou ou a solicitação foi cancelada?
➡️ Recomendação: não enviar convocação de etapa obsoleta; propor tentativas limitadas, falha visível na operação e nenhuma reversão silenciosa da decisão de compra.

## Premissas

Nenhuma premissa de comportamento foi aprovada ou adotada. Não existe autorização tácita por indisponibilidade dos participantes.
A contenção temporária de escopo de Q1 é um bloqueio, não uma nova promessa de produto.

## Fora de Escopo (declarado)

O card não declarou exclusões de produto. Nenhuma lacuna foi marcada como “fora desta entrega” para eliminar obrigação.
Nesta execução, o usuário autorizou somente planejamento nos steps 0 a 4 e proibiu implementação e alterações externas à pasta desta wiki.

