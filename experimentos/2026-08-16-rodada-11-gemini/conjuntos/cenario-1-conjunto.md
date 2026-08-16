# Conjunto — Cenário 1: Cupons de desconto (FERRO-812)

> Rodada 11 — Gemini 3.7 Flash High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r11/cupons-de-desconto/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — Caixa e espaços nas bordas são normalizados
- **Dado** que não existe cupom cadastrado na organização Acme
- **Quando** admin_organizacao cadastra o cupom com código " promo10 "
- **Então** o banco contém exatamente 1 cupom com código "PROMO10"
- E não existe registro com código " promo10 " nem "promo10"

## CT-02 — Código repetido na mesma organização é recusado
- **Dado** que a Acme já possui o cupom "PROMO10"
- **Quando** admin_organizacao da Acme tenta cadastrar "promo10"
- **Então** a gravação falha
- E a Acme permanece com exatamente 1 cupom

## CT-03 — Mesmo código em organização diferente é aceito
- **Dado** que a Acme possui o cupom "PROMO10"
- **Quando** admin_organizacao da organização Beta cadastra "PROMO10"
- **Então** a gravação é aceita
- E a Beta possui 1 cupom "PROMO10"

## CT-04 — Tipo inválido é recusado
- **Dado** um formulário de cupom preenchido com tipo "cashback"
- **Quando** admin_organizacao submete a gravação
- **Então** a gravação falha

## CT-05 — Limites do valor na criação (Esquema)
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

## CT-06 — Edição reaplica validação de domínio do valor (Esquema)
- **Dado** o cupom "P10" do tipo "<tipo_origem>" com valor 10
- **Quando** admin_organizacao altera para tipo "<tipo_final>" e valor <valor_final>
- **Então** o resultado é "<resultado>"
- E se recusado o cupom mantém tipo "<tipo_origem>" e valor 10

| tipo_origem | tipo_final | valor_final | resultado |
|---|---|---|---|
| porcentagem | porcentagem | 101 | recusado |
| porcentagem | fixo | 0 | recusado |
| porcentagem | porcentagem | 50 | aceito |

## CT-07 — BVA no instante exato de expiração (Esquema)
- **Dado** que o instante atual é "2026-08-15 12:00:00"
- **Quando** admin_organizacao cadastra cupom com expira_em "<expira_em>"
- **Então** o resultado é "<resultado>"

| expira_em | resultado |
|---|---|
| 2026-08-15 11:59:59 | recusado |
| 2026-08-15 12:00:00 | recusado |
| 2026-08-15 12:00:01 | aceito |

## CT-08 — Edição da validade para o passado é recusada
- **Dado** o cupom "PROMO10" com expira_em "2026-12-31 23:59:59"
- **Quando** admin_organizacao edita expira_em para "2026-01-01 00:00:01"
- **Então** a gravação falha
- E o cupom permanece com expira_em "2026-12-31 23:59:59"

## CT-09 — Limite zero é recusado
- **Dado** um formulário de cupom com limite_de_usos 0
- **Quando** admin_organizacao tenta gravar
- **Então** a gravação falha

## CT-10 — Matriz papel × operação fora da UI (Esquema)
- **Dado** um usuário com papel "<papel>" na Acme
- **Quando** tenta "<operacao>" um cupom diretamente na camada de serviço/HTTP
- **Então** o resultado é "<resultado>"

| papel | operacao | resultado |
|---|---|---|
| admin_organizacao | criar | aceito |
| admin_organizacao | editar | aceito |
| admin_organizacao | excluir | aceito |
| panel_user | criar | recusado |
| panel_user | editar | recusado |
| panel_user | excluir | recusado |

## CT-11 — panel_user visualiza somente cupons ativos
- **Dado** que a Acme possui os cupons "ATIVO" (válido, usos 1 de 3), "VENCIDO" (expirado) e "CHEIO" (usos 3 de 3)
- **Quando** panel_user lista os cupons
- **Então** a listagem exibe somente "ATIVO"
- E "VENCIDO" não aparece
- E "CHEIO" não aparece

## CT-12 — Tabela de decisão da aplicação (Esquema)
- **Dado** o cupom "<codigo>" na situação "<situacao>"
- **Quando** se tenta aplicar a um total de 10.000 centavos
- **Então** o resultado é "<resultado>"
- E o contador de usos resulta em <usos_final>
- E a trilha possui <trilha> linhas

| codigo | situacao | resultado | usos_final | trilha |
|---|---|---|---|---|
| PROMO10 | válido, usos 2 de 3 | aceito | 3 | 1 |
| INEXISTE | não cadastrado | recusado | 0 | 0 |
| VENCIDO | expirado, usos 0 de 3 | recusado | 0 | 0 |
| CHEIO | válido, usos 3 de 3 | recusado | 3 | 0 |

## CT-13 — Oráculo exato do desconto (Esquema)
- **Dado** um cupom válido do tipo "<tipo>" com valor <valor>
- **Quando** aplicado sobre o total de <total> centavos
- **Então** o desconto é exatamente <desconto> centavos
- E o valor final devolvido é exatamente <final> centavos

| tipo | valor | total | desconto | final |
|---|---|---|---|---|
| porcentagem | 29 | 10000 | 2900 | 7100 |
| porcentagem | 5 | 50 | 2 | 48 |
| porcentagem | 50 | 9999 | 4999 | 5000 |
| fixo | 5000 | 3000 | 3000 | 0 |
| fixo | 1000 | 10000 | 1000 | 9000 |

## CT-14 — Aplicação bem-sucedida incrementa contador e grava trilha
- **Dado** o cupom "PROMO10" válido com usos 1 de 3
- **Quando** Marina aplica sobre 10.000 centavos em "2026-08-15 14:30:00"
- **Então** o contador de usos é 2
- E a trilha contém 1 linha atribuída a Marina
- E a linha está datada de "2026-08-15 14:30:00"
- E a linha registra valor original de 10.000 e desconto de 1.000

## CT-15 — Duas requisições simultâneas disputando o último uso
- **Dado** o cupom "PROMO10" válido com limite 3 e usos 2
- **Quando** duas requisições simultâneas tentam aplicar o cupom
- **Então** exatamente uma é aceita e a outra é recusada
- E o contador de usos final é 3
- E a trilha possui exatamente 1 nova linha gravada

## CT-B01 — Rótulo do campo valor muda para percentual
- **Dado** que admin_organizacao está no formulário de criação de cupom
- **Quando** seleciona o tipo "Porcentagem"
- **Então** o campo valor exibe rótulo indicando percentual
- E não exibe rótulo de centavos

## CT-B02 — Rótulo do campo valor muda para centavos
- **Dado** que admin_organizacao está no formulário de criação de cupom
- **Quando** seleciona o tipo "Valor fixo"
- **Então** o campo valor exibe rótulo indicando centavos
- E não exibe rótulo de percentual

## CT-B03 — panel_user não possui affordances de escrita
- **Dado** que panel_user acessa a listagem de cupons
- E existem cupons ativos e inativos no banco
- **Quando** a página conclui o carregamento
- **Então** somente cupons ativos são visíveis
- E não há botão "Criar"
- E nenhuma linha possui botão "Editar" ou "Excluir"

## CT-B04 — Fluxo completo de criação de cupom
- **Dado** que admin_organizacao está na listagem de cupons
- **Quando** clica em "Criar", preenche código "BLACKFRIDAY", tipo "Porcentagem", valor 20, validade futura e limite 100
- E submete o formulário
- **Então** retorna à listagem
- E o cupom "BLACKFRIDAY" aparece com situação "Ativo"
