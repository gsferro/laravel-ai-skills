# Requisito — FERRO-812: Cupons de desconto

## Fonte

- **Origem**: card FERRO-812 colado no chat pelo desenvolvedor.
- **Data**: 2026-10-20.
- **Autor / solicitante**: solicitante do card; nome não informado.
- **Fidelidade**: alta (texto escrito, preservado literalmente, inclusive quebras de linha).
- A instrução do desenvolvedor sobre roteiro manual é meta-processo e está registrada somente no `03-progresso.md`.

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

A decomposição é revisável. `fechada` significa obrigação determinada pelo texto, não implementação concluída. As perguntas abaixo bloqueiam apenas seus recortes; não suspendem todas as obrigações da mesma cláusula.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | Criar cadastro de cupons no painel. | "Criar cupons de desconto no painel." | funcional | fechada |
| RQ-02 | Cupom possui código. | "O cupom tem um código" | funcional | fechada |
| RQ-03 | Cupom possui tipo porcentagem ou valor fixo. | "um tipo (porcentagem ou" / "valor fixo)" | funcional | fechada |
| RQ-04 | Cupom possui valor do desconto. | "o valor do desconto" | funcional | fechada |
| RQ-05 | Cupom possui data de validade. | "uma data de validade" | funcional | fechada |
| RQ-06 | Cupom possui limite de usos. | "um limite de quantas vezes" / "pode ser usado." | funcional | fechada |
| RQ-07 | Somente admin pode criar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-08 | Somente admin pode editar cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-09 | Somente admin pode excluir cupom. | "Só quem é admin pode criar, editar e excluir cupom." | autorização | fechada |
| RQ-10 | Outros usuários podem somente listar cupons. | "Os outros usuários podem apenas" / "listar os cupons ativos." | autorização | fechada |
| RQ-11 | Listagem dos outros usuários contém somente cupons ativos. | "listar os cupons ativos." | autorização | aberta — Q5 |
| RQ-12 | Ao aplicar no pedido, validar existência do cupom. | "o sistema valida se o cupom existe" | funcional | aberta — Q1 |
| RQ-13 | Ao aplicar no pedido, validar validade do cupom. | "se ainda está dentro" / "da validade" | funcional | aberta — Q1 |
| RQ-14 | Ao aplicar no pedido, validar limite de usos do cupom. | "se não estourou o limite de usos." | funcional | aberta — Q1 |
| RQ-15 | Aplicar desconto no total do pedido quando as validações passarem. | "Se estiver tudo certo, aplica o desconto" / "no valor total do pedido" | funcional | aberta — Q1 |
| RQ-16 | Incrementar contador de usos na aplicação bem-sucedida. | "incrementa o contador de usos." | funcional | aberta — Q1 |
| RQ-17 | Código do cupom não pode se repetir. | "O código do cupom não pode se repetir." | restrição | fechada |
| RQ-18 | Registrar quem aplicou o cupom para auditoria. | "Precisa registrar quem aplicou o cupom" | não-funcional | aberta — Q1 |
| RQ-19 | Registrar quando o cupom foi aplicado para auditoria. | "e quando, pra gente conseguir auditar depois." | não-funcional | aberta — Q1 |

## Perguntas ao Solicitante

Somente o solicitante responde às perguntas desta seção. Nenhuma recomendação é autorização. Respostas futuras entram como Adendo com fonte e texto literal. Solicitante e desenvolvedor estão indisponíveis nesta execução.

| ID | Pergunta / recorte | Afeta | Recomendação | Estado |
|----|-------------------|-------|--------------|--------|
| Q1 | Falta o domínio de pedidos: qual escopo autorizar? | RQ-12–RQ-16, RQ-18, RQ-19 | Não criar pedidos nem substituir a entrega por motor isolado enquanto aguarda definição. | aberta |
| Q2 | Painel e fronteira global ou por organização. | RQ-01, RQ-07–RQ-11, RQ-17 | Administração global e consulta autenticada no painel de negócio, sem compartilhamento entre organizações sem autorização. | aberta |
| Q3 | Quais perfis existentes significam admin? | RQ-07, RQ-08, RQ-09 | Considerar somente admin global; não promover admin de organização implicitamente. | aberta |
| Q4 | Superusuário sem papel admin pode alterar cupons? | RQ-07, RQ-08, RQ-09 | Não conceder exceção implícita à expressão "Só quem é admin". | aberta |
| Q5 | Definição de ativo e visibilidade histórica. | RQ-10, RQ-11 | Exibir a não admins somente cupons válidos e com usos disponíveis, mesmo se já utilizados pela pessoa. | aberta |
| Q6 | Domínio textual e equivalência dos códigos. | RQ-02, RQ-17 | Rejeitar código vazio ou fora de 1–64 caracteres ASCII alfanuméricos, hífen e sublinhado; comparar sem distinguir caixa e sem espaços externos. | aberta |
| Q7 | Instante de expiração, fuso e fronteira. | RQ-05, RQ-11, RQ-13 | Usar instante explícito com fuso; negar no instante do vencimento e depois dele. | aberta |
| Q8 | Faixas dos valores e do limite de usos. | RQ-04, RQ-06, RQ-14, RQ-15 | Porcentagem maior que zero e até 100; fixo positivo; limite inteiro positivo; rejeitar valores inválidos e desconto maior que total. | aberta |
| Q9 | Precisão monetária, base de cálculo e arredondamento. | RQ-15 | Usar total persistido do pedido na moeda dele, sem float; não efetivar aplicação sem regra de arredondamento explícita. | aberta; próxima fronteira após Q1 |
| Q10 | Quem pode aplicar e em quais pedidos/estados? | RQ-10, RQ-12–RQ-16, RQ-18 | Negar aplicação sem autorização específica e sem vínculo legítimo com o pedido. | aberta; próxima fronteira após Q1 |
| Q11 | Reenvio, reaplicação, combinação e cancelamento. | RQ-15, RQ-16, RQ-18, RQ-19 | Reenvio não consome outro uso; recusar nova aplicação/combinação e não restituir usos automaticamente sem regra expressa. | aberta; próxima fronteira após Q1 |
| Q12 | Edição/exclusão depois de haver aplicação. | RQ-08, RQ-09, RQ-18, RQ-19 | Preservar histórico; bloquear alterações destrutivas em cupom utilizado até definição. | aberta; próxima fronteira após Q1 |

### Rodada 1 — fronteira disponível, sem respostas

❓ Q1 · raia: requisito · afeta: RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18, RQ-19 · depende de: —
O projeto não contém entidade nem fluxo de pedidos. Devemos limitar esta entrega ao cadastro/listagem existente no painel e aguardar pedidos, ou incluir um domínio de pedidos neste card?
➡️ Recomendação: seguir provisoriamente com o recorte mais estreito, sem criar pedidos nem um motor isolado como substituto — cadastro/listagem tem custo menor; criar pedidos exige definir itens, total, estados, moeda, autorização e integração, ampliando substancialmente o card. As cláusulas dependentes ficam abertas, não atendidas.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-07, RQ-08, RQ-09, RQ-10, RQ-11, RQ-17 · depende de: —
Os cupons pertencem à instalação ou a cada organização? Em qual painel administradores gerenciam e os demais usuários consultam? O código deve continuar único em toda a instalação?
➡️ Recomendação: manter a proibição literal de códigos repetidos em toda a instalação; propor gestão global e consulta no painel de negócio, sem liberar consulta entre organizações até confirmar o recorte — evita vazamento e não enfraquece a unicidade escrita. Estrutura e rotas por organização ficam pendentes.

❓ Q3 · raia: requisito · afeta: RQ-07, RQ-08, RQ-09 · depende de: —
"Admin" significa somente o papel global admin ou inclui admin_organizacao? Quem acumula admin_organizacao e panel_user pode criar, editar e excluir sem possuir admin global?
➡️ Recomendação: somente admin global; a combinação admin_organizacao + panel_user não concede CRUD — falha fechado e não transforma administração local em administração da instalação. Quem possui admin e panel_user já satisfaz o papel admin; não se presume exclusividade de papéis.

❓ Q4 · raia: requisito · afeta: RQ-07, RQ-08, RQ-09 · depende de: —
Quem tem master_global sem possuir admin pode criar, editar e excluir cupons, como ocorre nos gates atuais, ou vale a restrição literal do card?
➡️ Recomendação: exigir admin também nessa combinação — negar a exceção enquanto não for autorizada, sem alterar silenciosamente o contrato global dos demais módulos.

❓ Q5 · raia: requisito · afeta: RQ-10, RQ-11 · depende de: —
"Ativo" significa estar válido e ainda ter usos disponíveis, ou existe ativação manual? Um não admin que já aplicou cupom continua vendo esse cupom depois de vencer ou esgotar?
➡️ Recomendação: considerar ativo apenas o válido com saldo de usos; ocultar vencidos/esgotados também de participantes históricos — preserva "apenas listar os cupons ativos". Não criar flag de ativação manual por suposição.

❓ Q6 · raia: requisito · afeta: RQ-02, RQ-17 · depende de: —
Qual o tamanho máximo e o conjunto permitido para o código? "PROMO", "promo" e um código com espaços externos representam o mesmo cupom?
➡️ Recomendação: aceitar 1–64 caracteres ASCII alfanuméricos, hífen e sublinhado; tratar caixa e espaços externos como equivalentes, recusando duplicatas e demais entradas — limita texto livre e evita equivalências inesperadas. Teto e normalização são propostas, não regras aprovadas.

❓ Q7 · raia: requisito · afeta: RQ-05, RQ-11, RQ-13 · depende de: —
A validade é um dia civil inteiro ou um instante? Qual o fuso, e o cupom ainda vale exatamente no limite informado?
➡️ Recomendação: cadastrar instante explícito com fuso e recusar a partir dele, inclusive na igualdade — não prolonga validade por interpretação. Não converter uma data em final de dia sem confirmação.

❓ Q8 · raia: requisito · afeta: RQ-04, RQ-06, RQ-14, RQ-15 · depende de: —
São permitidos desconto zero, porcentagem acima de 100, valor fixo maior que o total ou limite de usos zero/ilimitado? Quais os tetos e casas decimais aceitos?
➡️ Recomendação: porcentagem em (0, 100], fixo positivo, limite inteiro positivo; recusar descontos maiores que total e valores fora das faixas — não gerar total negativo nem usos ilimitados por convenção implícita. Precisão e tetos finais permanecem pendentes.

### Perguntas preparadas para próxima fronteira — não simulam rodada respondida

As perguntas seguintes dependem de Q1. Ficam registradas para não inventar comportamento de um pedido inexistente; não foram tratadas como decisões de desenho.

❓ Q9 · raia: requisito · afeta: RQ-15 · depende de: Q1
Qual é o total monetário oficial do pedido, a moeda e a regra de arredondamento do desconto percentual? O total inclui frete, tributos e outros descontos?
➡️ Recomendação: usar o total persistido e a moeda do pedido, com aritmética decimal exata; suspender aplicação sem política explícita de arredondamento e composição — não assumir subtotal, arredondamento ou moeda inexistentes.

❓ Q10 · raia: requisito · afeta: RQ-10, RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18 · depende de: Q1
Quem pode aplicar cupom, sobre quais pedidos e em quais estados, dado que os outros usuários "podem apenas listar"?
➡️ Recomendação: negar aplicação sem autorização específica, vínculo legítimo com o pedido e estado permitido — não transformar direito de consulta em direito de aplicar desconto.

❓ Q11 · raia: requisito · afeta: RQ-15, RQ-16, RQ-18, RQ-19 · depende de: Q1
Reenvio da mesma operação pode consumir outro uso? O pedido aceita mais de um cupom, substituição/reaplicação ou devolução do uso após cancelamento?
➡️ Recomendação: reenvio não produz consumo nem desconto adicionais; recusar novas combinações/substituições e não restituir usos automaticamente até definição — mantém consistência sem inventar um ciclo de estorno.

❓ Q12 · raia: requisito · afeta: RQ-08, RQ-09, RQ-18, RQ-19 · depende de: Q1
Depois de um uso, admin pode mudar código, desconto, validade e limite abaixo do contador, ou excluir o cupom? Como preservar a identificação de quem aplicou e quando se cupom ou usuário forem excluídos?
➡️ Recomendação: preservar registro histórico de aplicação e bloquear edição/exclusão destrutiva de cupom utilizado até definir retenção e referências — não apagar auditoria exigida pelo card nem reescrever desconto já aplicado.

### Recortes bloqueados e obrigações preservadas

- Q1 bloqueia integralmente RQ-12–RQ-16 e RQ-18–RQ-19: não há pedido no qual aplicar ou auditar. Nenhum passo implementa essas cláusulas antes de resposta como Adendo.
- Q5 bloqueia integralmente RQ-11: falta definir o predicado ativo. O direito de listagem de RQ-10 continua no plano, sem entregar filtro presumido.
- Q2–Q4 bloqueiam o recorte material de painel, posse e mapeamento de papéis. Mantêm-se as obrigações de oferecer cadastro e de impedir CRUD por não admins.
- Q6–Q8 bloqueiam somente normalização/teto textual, fronteira temporal e domínio numérico. Existência dos campos, os dois tipos e a rejeição de código exatamente repetido continuam determinados.
- Q9–Q12 detalham o recorte já dependente de pedidos. Ausência de resposta não autoriza nenhuma das recomendações.

## Premissas

| ID | Premissa | Origem | Data | Afeta | Estado |
|----|----------|--------|------|-------|--------|
| P-01 | Enquanto falta resposta sobre pedidos, planejar somente cadastro e consulta apoiados no domínio existente, sem criar pedidos nem considerar um motor isolado como entrega da aplicação. | step 4 — fallback de escopo prescrito pela feature-wiki, Q1 | 2026-10-20 | RQ-12, RQ-13, RQ-14, RQ-15, RQ-16, RQ-18, RQ-19 | vigente |

P-01 não revoga nem declara fora de escopo as obrigações de aplicação/auditoria. Elas permanecem abertas. Nenhuma premissa aprova recomendações de comportamento.

## Fora de Escopo (declarado)

Nenhum item foi explicitamente excluído pelo solicitante. Pedidos e auditoria de aplicação estão bloqueados, não excluídos. As restrições desta sessão são de execução do planejamento, não mudanças no produto solicitado.

