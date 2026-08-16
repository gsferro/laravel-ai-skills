# Conjunto — Cenário 1: Cupons de desconto (FERRO-812)

> Rodada 9 — GLM 5.2 High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r9/cupons-de-desconto/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — Código com espaços e caixa mista é normalizado
- **Dado** que não existe cupom com código "PROMO10"
- **Quando** admin_organizacao cadastra cupom com código " promo10 "
- **Então** o cupom é gravado com código "PROMO10"
- E não existe cupom com código "promo10" no banco

## CT-02 — Código duplicado na mesma organização é recusado
- **Dado** que existe cupom "PROMO10" na organização Acme
- **Quando** admin_organizacao da Acme tenta cadastrar "PROMO10"
- **Então** a gravação falha

## CT-03 — Mesmo código em organização diferente é aceito
- **Dado** que existe cupom "PROMO10" na organização Acme
- **Quando** admin_organizacao da organização Beta cadastra "PROMO10"
- **Então** o cupom é gravado com sucesso

## CT-04 — Tipo inválido é recusado
- **Dado** um formulário de criação de cupom
- **Quando** admin_organizacao envia tipo "cashback"
- **Então** a gravação falha

## CT-05 — Domínio de valor por tipo (Esquema)
- **Dado** que admin_organizacao cadastra um cupom com tipo "<tipo>" e valor "<valor>"
- **Então** o resultado é "<resultado>"

| tipo | valor | resultado |
|---|---|---|
| porcentagem | 0 | recusado |
| porcentagem | 1 | aceito |
| porcentagem | 100 | aceito |
| porcentagem | 101 | recusado |
| fixo | 0 | recusado |
| fixo | 1 | aceito |

## CT-06 — BVA na validade na criação (Esquema)
- **Dado** que o instante atual é "2026-08-15 12:00:00"
- **Quando** admin_organizacao cadastra cupom com expira_em "<expira_em>"
- **Então** o resultado é "<resultado>"

| expira_em | resultado |
|---|---|
| 2026-08-14 12:00:00 | recusado |
| 2026-08-15 12:00:00 | recusado |
| 2026-08-16 12:00:00 | aceito |

## CT-07 — Editar validade para o passado é recusado
- **Dado** que existe cupom "PROMO10" com expira_em "2026-12-31 23:59:59"
- **Quando** admin_organizacao edita expira_em para "2026-01-01 00:00:01"
- **Então** a gravação falha
- E o cupom mantém expira_em "2026-12-31 23:59:59"

## CT-08 — Limite zero é recusado
- **Dado** um formulário de criação de cupom
- **Quando** admin_organizacao envia limite_de_usos 0
- **Então** a gravação falha

## CT-09 — Matriz papel × ação (Esquema)
- **Dado** um usuário com papel "<papel>"
- **Quando** tenta "<acao>" um cupom
- **Então** o resultado é "<resultado>"

| papel | acao | resultado |
|---|---|---|
| admin_organizacao | criar | aceito |
| admin_organizacao | editar | aceito |
| admin_organizacao | excluir | aceito |
| panel_user | criar | recusado |
| panel_user | editar | recusado |
| panel_user | excluir | recusado |

## CT-10 — panel_user lista apenas cupons ativos
- **Dado** que existem cupons "ATIVO" (válido e com usos), "VENCIDO" (expirado) e "CHEIO" (usos = limite) na organização Acme
- **Quando** panel_user lista cupons
- **Então** só "ATIVO" aparece na lista
- E "VENCIDO" e "CHEIO" não aparecem

## CT-11 — Validação na aplicação (Esquema)
- **Dado** um cupom "<cupom>" com situação "<situacao>"
- **Quando** se tenta aplicar a um total de 10.000 centavos
- **Então** o resultado é "<resultado>"
- E o contador de usos é "<contador>"

| cupom | situacao | resultado | contador |
|---|---|---|---|
| PROMO10 | válido e usos 0 | aceito | 1 |
| INEXIST | não existe | recusado | 0 |
| VENCIDO | expirado | recusado | 0 |
| CHEIO | usos = limite | recusado | 2 |

## CT-12 — Cálculo do desconto (Esquema)
- **Dado** um cupom "<codigo>" com tipo "<tipo>" e valor "<valor>"
- **Quando** aplicado a um total de "<total>" centavos
- **Então** o desconto é "<desconto>" centavos
- E o total com desconto é "<resultado>" centavos

| codigo | tipo | valor | total | desconto | resultado |
|---|---|---|---|---|---|
| P29 | porcentagem | 29 | 10000 | 2900 | 7100 |
| P5 | porcentagem | 5 | 50 | 2 | 48 |
| P50 | porcentagem | 50 | 9999 | 4999 | 5000 |
| F5000 | fixo | 5000 | 3000 | 3000 | 0 |
| F1000 | fixo | 1000 | 10000 | 1000 | 9000 |

## CT-13 — Aplicação bem-sucedida incrementa contador e trilha
- **Dado** cupom "PROMO10" com limite 3 e usos 1
- **Quando** Marina aplica a um total de 10.000 centavos
- **Então** o contador de usos é 2
- E existe 1 linha em cupom_usos com aplicado_por_id = Marina

## CT-14 — Cupom inválido não incrementa contador nem trilha
- **Dado** cupom "VENCIDO" com usos 0
- **Quando** se tenta aplicar
- **Então** o contador de usos permanece 0
- E não existe linha em cupom_usos

## CT-15 — Duas requisições simultâneas não furam o limite
- **Dado** cupom "PROMO10" com limite 3 e usos 2
- **Quando** duas requisições simultâneas tentam aplicar
- **Então** uma é aceita e a outra é recusada
- E o contador de usos é 3
- E existe exatamente 1 nova linha em cupom_usos

## CT-16 — Trilha registra identidade e momento
- **Dado** cupom "PROMO10" válido
- **Quando** Marina aplica em "2026-08-15 14:30:00"
- **Então** existe linha em cupom_usos com aplicado_por_id = Marina
- E a linha tem created_at = "2026-08-15 14:30:00"
- E a linha tem valor_original = 10.000 e valor_desconto = 1.000

## CT-17 — Editar valor para acima do teto percentual é recusado
- **Dado** cupom "P10" tipo porcentagem valor 10
- **Quando** admin_organizacao edita valor para 101
- **Então** a gravação falha
- E o cupom mantém valor 10

## CT-18 — Editar tipo para fixo mantém validação de domínio
- **Dado** cupom "P10" tipo porcentagem valor 10
- **Quando** admin_organizacao edita tipo para fixo e valor para 0
- **Então** a gravação falha

## CT-B01 — Trocar tipo para porcentagem mostra rótulo de percentual
- **Dado** que admin_organizacao está no formulário de criação de cupom
- **Quando** seleciona o tipo "Porcentagem"
- **Então** o campo valor exibe rótulo indicando percentual

## CT-B02 — Trocar tipo para valor fixo mostra rótulo de centavos
- **Dado** que admin_organizacao está no formulário de criação de cupom
- **Quando** seleciona o tipo "Valor fixo"
- **Então** o campo valor exibe rótulo indicando centavos

## CT-B03 — panel_user vê apenas a listagem de ativos
- **Dado** que panel_user está autenticado no painel /app
- E existem cupons ativos e inativos na organização
- **Quando** acessa a listagem de cupons
- **Então** vê apenas cupons ativos
- E não vê botão "Criar"
- E não vê ação "Editar" em nenhuma linha
- E não vê ação "Excluir" em nenhuma linha

## CT-B04 — Fluxo completo de criação
- **Dado** que admin_organizacao está na listagem de cupons
- **Quando** clica em "Criar cupom"
- E preenche código "BLACKFRIDAY", tipo "Porcentagem", valor 20, validade futura, limite 100
- E submete o formulário
- **Então** volta à listagem
- E "BLACKFRIDAY" aparece na lista com situação "Ativo"
