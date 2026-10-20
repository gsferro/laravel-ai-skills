# Requisito — FERRO-812: Cupons de desconto

## Fonte

- **Origem**: card FERRO-812 colado literalmente no chat pelo desenvolvedor.
- **Data**: 2026-10-20.
- **Autor / solicitante**: solicitante do card, nome não informado; desenvolvedor e solicitante indisponíveis nesta rodada.
- **Fidelidade**: alta, texto escrito. A captura ocorreu no step 0, antes de pesquisar o projeto.
- O texto original e esta fonte são imutáveis. Cláusulas, perguntas e premissas são derivadas e revisáveis.

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

“Fechada” significa obrigação determinada pelo texto; não significa implementada ou aprovada. Quando uma pergunta afeta somente um recorte, a obrigação determinada permanece fechada e o recorte está explicitamente bloqueado.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|---|---|---|---|---|
| RQ-01 | Permitir criar cupons no painel. | "Criar cupons de desconto no painel." | funcional | fechada |
| RQ-02 | O cupom possui código. | "O cupom tem um código" | funcional | fechada |
| RQ-03 | O tipo do cupom é porcentagem ou valor fixo. | "um tipo (porcentagem ou\nvalor fixo)" | restrição | fechada |
| RQ-04 | O cupom possui valor do desconto. | "o valor do desconto" | funcional | fechada |
| RQ-05 | O cupom possui data de validade. | "uma data de validade" | funcional | fechada |
| RQ-06 | O cupom possui limite de usos. | "um limite de quantas vezes\npode ser usado." | funcional | fechada |
| RQ-07 | Somente admin pode criar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-08 | Somente admin pode editar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-09 | Somente admin pode excluir cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-10 | Os demais usuários podem listar cupons, sem criar, editar ou excluir. | "Os outros usuários podem apenas\nlistar os cupons ativos." | autorização | fechada |
| RQ-11 | A aplicação no pedido valida a existência do cupom. | "Na hora de aplicar no pedido, o sistema valida se o cupom existe" | funcional | aberta — Q2 |
| RQ-12 | A aplicação no pedido valida se o cupom está dentro da validade. | "se ainda está dentro\nda validade" | funcional | aberta — Q2 |
| RQ-13 | A aplicação no pedido valida se o limite de usos não foi estourado. | "se não estourou o limite de usos." | funcional | aberta — Q2 |
| RQ-14 | Com as validações satisfeitas, aplicar o desconto no total do pedido. | "Se estiver tudo certo, aplica o desconto\nno valor total do pedido" | funcional | aberta — Q2 |
| RQ-15 | Com aplicação bem-sucedida, incrementar o contador de usos. | "e incrementa o contador de usos." | funcional | aberta — Q2 |
| RQ-16 | O código do cupom não pode se repetir. | "O código do cupom não pode se repetir." | restrição | fechada |
| RQ-17 | Registrar quem aplicou o cupom para auditoria posterior. | "Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q2 |
| RQ-18 | Registrar quando o cupom foi aplicado para auditoria posterior. | "Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q2 |
| RQ-19 | A listagem dos demais usuários contém somente cupons ativos. | "listar os cupons ativos." | autorização | aberta — Q5 |

Nos trechos literais da tabela, `\n` representa exclusivamente a quebra de linha do original, sem mudar palavras. A separação de RQ-10 e RQ-19 preserva a permissão de listar enquanto se esclarece o significado de “ativos”.

## Perguntas ao Solicitante

Todas as perguntas abaixo são da **raia requisito**, não são transferidas ao desenvolvedor. Estão registradas para encaminhamento; nenhum contato externo foi feito. Uma recomendação não equivale a resposta. Rodada inicial: perguntas sem dependência; perguntas dependentes permanecem em fila para a rodada seguinte.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| ❓ Q2 | raia: requisito · depende de: —<br>Não existe entidade ou fluxo de pedido no projeto. O card deve aguardar esse domínio, entregando antes somente o cadastro/listagem possível, ou incluir a criação do domínio de pedidos? | RQ-11–RQ-15, RQ-17, RQ-18 | ➡️ Recomendação: seguir somente com o que existe e manter aplicação/auditoria bloqueadas. Criar pedidos exige definir total, moeda, estados, acesso e telas; altera substancialmente o custo. Não criar um “motor” isolado e declará-lo entrega da aplicação no pedido. | aberta |
| ❓ Q3 | raia: requisito · depende de: —<br>“Admin” significa o papel global admin, admin_organizacao ou ambos? O master_global sem papel admin também pode criar, editar e excluir? Em quais painéis o cadastro e a listagem devem aparecer? | RQ-01, RQ-07–RQ-10, RQ-19 | ➡️ Recomendação: não conceder escrita a perfis adicionais nem abrir novos painéis antes da definição; usar admin global como candidato literal, sem equipará-lo a admin_organizacao ou master_global. A exceção global existente precisa de decisão explícita. | aberta |
| ❓ Q4 | raia: requisito · depende de: —<br>Os cupons, o limite de usos e a unicidade do código valem na instalação inteira ou por organização? Quem de uma organização pode ver cupons de outra? | RQ-01, RQ-06, RQ-10, RQ-13, RQ-16, RQ-19 | ➡️ Recomendação: não permitir visibilidade nem aplicação entre organizações; não adotar unicidade por organização como se fosse global. Bloquear o recorte e o índice definitivo até a resposta. | aberta |
| ❓ Q5 | raia: requisito · depende de: —<br>“Ativo” significa estar dentro da validade e ainda ter usos disponíveis, ou existe também ativação/desativação manual? | RQ-05, RQ-06, RQ-19 | ➡️ Recomendação: considerar candidato ativo apenas cupom vigente e com saldo de usos, ocultando os demais; não criar flag manual sem pedido. A direção ainda depende de resposta. | aberta |
| ❓ Q6 | raia: requisito · depende de: —<br>A validade termina em qual horário e fuso? O instante exatamente igual ao vencimento ainda permite uso? | RQ-05, RQ-12, RQ-19 | ➡️ Recomendação: recusar no instante de vencimento ou depois; esclarecer se a data representa fim do dia em America/Sao_Paulo antes de convertê-la para armazenamento. | aberta |
| ❓ Q7 | raia: requisito · depende de: —<br>O código distingue maiúsculas/minúsculas e espaços? Quais caracteres e comprimento máximo são aceitos, inclusive nas chamadas diretas? | RQ-02, RQ-11, RQ-16 | ➡️ Recomendação: rejeitar código fora do contrato; propor de 1 a 50 caracteres ASCII alfanuméricos ou hífen, sem espaços, com comparação canônica em maiúsculas. Não normalizar nem liberar variantes antes da confirmação. | aberta |
| ❓ Q8 | raia: requisito · depende de: —<br>Quais faixas e casas decimais são aceitas para porcentagem, valor fixo e limite de usos? Zero ou vazio significam ilimitado? | RQ-03–RQ-06, RQ-13, RQ-14 | ➡️ Recomendação: rejeitar desconto não positivo, porcentagem acima de 100 e limite não inteiro positivo; não tratar zero/nulo como ilimitado sem autorização. Confirmar precisão e teto do fixo. | aberta |
| ❓ Q9 | raia: requisito · depende de: Q2<br>Qual moeda, precisão, regra de arredondamento e composição do total serão usadas? O que ocorre se o desconto fixo superar o total? | RQ-04, RQ-14 | ➡️ Recomendação: recusar aplicação sem total monetário autoritativo, com moedas incompatíveis ou desconto superior ao total. Não gerar total negativo nem escolher silenciosamente limitar o desconto a zero final. | aberta |
| ❓ Q10 | raia: requisito · depende de: Q2<br>Quem pode aplicar cupom em pedido e em quais pedidos/estados, considerando que os demais usuários “podem apenas listar”? | RQ-10–RQ-15, RQ-17 | ➡️ Recomendação: não liberar aplicação a usuário comum nem em pedido sem autorização/estado definido; decidir essa permissão separadamente do CRUD. | aberta |
| ❓ Q11 | raia: requisito · depende de: Q2<br>Repetir a aplicação no mesmo pedido ou combinar cupons é permitido? Cancelamento, remoção ou falha posterior devolve uso e desconto? | RQ-13–RQ-15, RQ-17, RQ-18 | ➡️ Recomendação: recusar reaplicação e acúmulo enquanto não definidos; não alterar contador por cancelamento sem regra explícita. Tentativa malsucedida não deve deixar desconto ou consumo parcial. | aberta |
| ❓ Q12 | raia: requisito · depende de: —<br>É permitido editar código, desconto, validade ou limite de cupom já usado e excluir esse cupom? Código excluído pode voltar a ser cadastrado? | RQ-08, RQ-09, RQ-16–RQ-18 | ➡️ Recomendação: recusar alterações/exclusão que apaguem ou desfigurem aplicações anteriores e não reutilizar código já usado até definir preservação do histórico. Não converter exclusão em desativação silenciosamente. | aberta |
| ❓ Q13 | raia: requisito · depende de: Q3<br>Quem tem admin e panel_user ao mesmo tempo conserva os poderes de admin sobre cupons? | RQ-07–RQ-10 | ➡️ Recomendação: não usar o papel de leitura para ampliar a autoridade ou o alcance organizacional do admin; até a definição, não liberar o caso misto automaticamente. | aberta |
| ❓ Q14 | raia: requisito · depende de: Q3<br>Quem acumula admin e admin_organizacao pode operar cupons globais e de qualquer organização? | RQ-07–RQ-10, RQ-19 | ➡️ Recomendação: não unir alcances globais/organizacionais; exigir contexto explícito e manter o recorte indefinido bloqueado. | aberta |
| ❓ Q15 | raia: requisito · depende de: Q3<br>Quem acumula admin e infra pode operar cupons pelo painel de infraestrutura? | RQ-01, RQ-07–RQ-10 | ➡️ Recomendação: não expor operações comerciais em infra por acumulação de papéis; a permissão de observabilidade não autoriza CRUD comercial. | aberta |
| ❓ Q16 | raia: requisito · depende de: Q3<br>Quem acumula admin e master_global mantém acesso irrestrito aos cupons independentemente do contexto? | RQ-07–RQ-10, RQ-19 | ➡️ Recomendação: não deixar o bypass global decidir essa fronteira silenciosamente; bloquear a exceção da feature até a resposta, sem modificar o gate compartilhado por conta própria. | aberta |
| ❓ Q17 | raia: requisito · depende de: —<br>Quem já aplicou cupom continua vendo esse cupom depois de inativo ou de perder o papel/vínculo que lhe dava acesso? | RQ-10, RQ-17–RQ-19 | ➡️ Recomendação: ocultar cupom inativo da listagem comum e não manter acesso por participação histórica; eventual acesso ao histórico deve ter autorização própria definida. | aberta |
| ❓ Q18 | raia: requisito · depende de: Q2<br>Quem consulta a auditoria das aplicações, por quanto tempo ela é mantida e o que deve permanecer se o autor ou cupom for excluído? | RQ-09, RQ-17, RQ-18 | ➡️ Recomendação: não expor auditoria a usuários comuns nem apagar registros de aplicação automaticamente. Preservar ator, momento e vínculo com a aplicação; retenção e consulta precisam de definição. | aberta |

Sementes consideradas: papéis e acumulação par a par (Q13–Q16); visibilidade histórica (Q17); texto livre do código (Q7). Notificações não aparecem no requisito, portanto não foram inventadas.

## Premissas

| ID | Premissa | Origem | Data | Afeta | Estado |
|---|---|---|---|---|---|
| P-01 | Sem resposta sobre a entidade ausente, planejar o cadastro/listagem disponível e não criar pedidos, simuladores ou um motor independente apresentado como aplicação real. | step 0/3 — ausência confirmada; regra de escopo mais estreito; Q2 | 2026-10-20 | RQ-11–RQ-15, RQ-17, RQ-18 | vigente |

Não foram promovidas recomendações de comportamento a premissas aceitas. A premissa acima limita a atuação provisória, sem retirar obrigações do card.

## Fora de Escopo (declarado)

Nenhuma exclusão funcional foi declarada pelo solicitante. Aplicação no pedido, consumo e auditoria continuam requeridos, com bloqueio explícito. O pedido desta sessão autoriza somente o planejamento até o step 4.

