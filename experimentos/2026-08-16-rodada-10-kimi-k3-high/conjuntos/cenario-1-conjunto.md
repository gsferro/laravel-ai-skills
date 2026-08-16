# Conjunto — Cenário 1: Cupons de desconto (FERRO-812)

> Rodada 10 — Kimi K3 High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r10/cupons-de-desconto/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — Caixa e espaços são normalizados na gravação
- **Dado** que não existe cupom algum na organização Acme
- **Quando** admin_organizacao cadastra o cupom com código " promo10 "
- **Então** o banco contém exatamente 1 cupom com código "PROMO10"
- E não existe cupom com código " promo10 " nem "promo10" no banco

## CT-02 — Repetição na mesma organização é recusada, mesmo com caixa diferente
- **Dado** que a Acme já tem o cupom "PROMO10"
- **Quando** admin_organizacao da Acme tenta cadastrar "promo10"
- **Então** a gravação falha
- E a Acme continua com exatamente 1 cupom

## CT-03 — O mesmo código é aceito em outra organização
- **Dado** que a Acme já tem o cupom "PROMO10"
- **Quando** admin_organizacao da organização Beta cadastra "PROMO10"
- **Então** a gravação é aceita
- E a Beta tem 1 cupom "PROMO10"

## CT-04 — Tipo fora do conjunto é recusado
- **Dado** um cadastro de cupom com tipo "cashback"
- **Quando** admin_organizacao tenta gravar
- **Então** a gravação falha

## CT-05 — Fronteiras do valor na criação (Esquema)
- **Quando** admin_organizacao cadastra cupom do tipo "<tipo>" com valor <valor>
- **Então** o resultado é "<resultado>"

| tipo | valor | resultado |
|---|---|---|
| porcentagem | 0 | recusado |
| porcentagem | 1 | aceito |
| porcentagem | 100 | aceito |
| porcentagem | 101 | recusado |
| fixo | 0 | recusado |
| fixo | 1 | aceito |

## CT-06 — A edição reaplica o domínio (Esquema)
- **Dado** o cupom "P10" do tipo "<tipo_origem>" com valor 10
- **Quando** admin_organizacao edita para tipo "<tipo_final>" e valor <valor_final>
- **Então** o resultado é "<resultado>"
- E o cupom permanece com tipo "<tipo_origem>" e valor 10 se recusado

| tipo_origem | tipo_final | valor_final | resultado |
|---|---|---|---|
| porcentagem | porcentagem | 101 | recusado |
| porcentagem | fixo | 0 | recusado |
| porcentagem | porcentagem | 50 | aceito |

## CT-07 — BVA no instante de expiração (Esquema)
- **Dado** que agora é "2026-08-15 12:00:00"
- **Quando** admin_organizacao cadastra cupom com expira_em "<expira_em>"
- **Então** o resultado é "<resultado>"

| expira_em | resultado |
|---|---|
| 2026-08-15 11:59:59 | recusado |
| 2026-08-15 12:00:00 | recusado |
| 2026-08-15 12:00:01 | aceito |

## CT-08 — Editar a validade para o passado é recusado
- **Dado** o cupom "PROMO10" com expira_em "2026-12-31 23:59:59"
- **Quando** admin_organizacao edita expira_em para "2026-01-01 00:00:01"
- **Então** a gravação falha
- E o cupom permanece com expira_em "2026-12-31 23:59:59"

## CT-09 — Limite zero é recusado
- **Dado** um cadastro de cupom com limite_de_usos 0
- **Quando** admin_organizacao tenta gravar
- **Então** a gravação falha

## CT-10 — Papel × operação fora da tela (Esquema)
- **Dado** um usuário com papel "<papel>" na organização Acme
- **Quando** ele executa "<operacao>" sobre um cupom, sem passar pelo formulário
- **Então** o resultado é "<resultado>"

| papel | operacao | resultado |
|---|---|---|
| admin_organizacao | criar | aceito |
| admin_organizacao | editar | aceito |
| admin_organizacao | excluir | aceito |
| panel_user | criar | recusado |
| panel_user | editar | recusado |
| panel_user | excluir | recusado |

## CT-11 — panel_user enxerga somente cupons ativos
- **Dado** que a Acme tem os cupons "ATIVO" (válido, usos 1 de 3), "VENCIDO" (expirado) e "CHEIO" (usos 3 de 3)
- **Quando** panel_user lista os cupons
- **Então** a lista contém somente "ATIVO"
- E "VENCIDO" não aparece
- E "CHEIO" não aparece

## CT-12 — Tabela de decisão da aplicação (Esquema)
- **Dado** o cupom "<codigo>" em situação "<situacao>"
- **Quando** se tenta aplicar a um total de 10.000 centavos
- **Então** o resultado é "<resultado>"
- E o contador de usos fica em <usos_final>
- E a trilha tem <trilha> linhas

| codigo | situacao | resultado | usos_final | trilha |
|---|---|---|---|---|
| PROMO10 | válido, usos 2 de 3 | aceito | 3 | 1 |
| INEXISTE | não cadastrado | recusado | 0 | 0 |
| VENCIDO | expirado, usos 0 de 3 | recusado | 0 | 0 |
| CHEIO | válido, usos 3 de 3 | recusado | 3 | 0 |

## CT-13 — Oráculo exato do cálculo (Esquema)
- **Dado** um cupom válido do tipo "<tipo>" com valor <valor>
- **Quando** aplicado sobre o total de <total> centavos
- **Então** o desconto é exatamente <desconto> centavos
- E o valor devolvido é exatamente <final> centavos

| tipo | valor | total | desconto | final |
|---|---|---|---|---|
| porcentagem | 29 | 10000 | 2900 | 7100 |
| porcentagem | 5 | 50 | 2 | 48 |
| porcentagem | 50 | 9999 | 4999 | 5000 |
| fixo | 5000 | 3000 | 3000 | 0 |
| fixo | 1000 | 10000 | 1000 | 9000 |

## CT-14 — Aplicação bem-sucedida incrementa e audita
- **Dado** o cupom "PROMO10" válido com usos 1 de 3
- **Quando** Marina aplica sobre 10.000 centavos em "2026-08-15 14:30:00"
- **Então** o contador de usos é 2
- E a trilha tem 1 linha atribuída a Marina
- E a linha está datada de "2026-08-15 14:30:00"
- E a linha registra valor original 10.000 e desconto 1.000

## CT-15 — Duas aplicações simultâneas no último uso
- **Dado** o cupom "PROMO10" válido com usos 2 de 3
- **Quando** duas aplicações simultâneas disputam o uso restante
- **Então** exatamente uma é aceita
- E a outra é recusada
- E o contador de usos é 3
- E a trilha tem exatamente 1 linha

## CT-B01 — O rótulo do valor acompanha o tipo "Porcentagem"
- **Dado** que admin_organizacao abriu o formulário de novo cupom
- **Quando** escolhe o tipo "Porcentagem"
- **Então** o campo de valor passa a indicar percentual
- E não indica centavos

## CT-B02 — O rótulo do valor acompanha o tipo "Valor fixo"
- **Dado** que admin_organizacao abriu o formulário de novo cupom
- **Quando** escolhe o tipo "Valor fixo"
- **Então** o campo de valor passa a indicar centavos
- E não indica percentual

## CT-B03 — panel_user não tem affordance de escrita
- **Dado** que panel_user abriu a listagem de cupons
- E existem cupons ativos e inativos
- **Quando** a página termina de carregar
- **Então** somente cupons ativos aparecem
- E não existe botão de criação
- E nenhuma linha oferece editar ou excluir

## CT-B04 — Criar um cupom de ponta a ponta
- **Dado** que admin_organizacao está na listagem de cupons
- **Quando** abre o formulário, preenche código "BLACKFRIDAY", tipo "Porcentagem", valor 20, validade futura e limite 100
- E confirma
- **Então** retorna à listagem
- E "BLACKFRIDAY" aparece marcado como ativo
