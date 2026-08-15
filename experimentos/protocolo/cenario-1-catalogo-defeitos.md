# Catálogo de Defeitos — Cenário 1 (FERRO-812, cupons de desconto)

> Escrito **antes** de qualquer execução da skill. Cada item é uma implementação
> plausível e defeituosa que um dev (ou um agente) produziria de boa-fé lendo o card.
> Um conjunto de CTs só vale se **mata** o mutante.

| ID | Defeito plantado (mutante) | Classe | Técnica que o revela |
|----|---------------------------|--------|----------------------|
| D01 | Percentual aceita valor > 100 → desconto maior que o total | limite de domínio | BVA / partição |
| D02 | Valor fixo maior que o total do pedido → total final negativo em vez de zero | limite de saída | BVA |
| D03 | Validade avaliada com `<` em vez de `<=` → cupom morre 1 dia antes (ou vive 1 a mais) | off-by-one em data | BVA 3-valores |
| D04 | Limite de usos com `<` em vez de `<=` → permite 1 uso além do limite | off-by-one em contador | BVA 3-valores |
| D05 | Unicidade de código case-sensitive → `PROMO10` e `promo10` coexistem | normalização | partição de string |
| D06 | Contador incrementado **antes** da validação → cupom inválido consome uso | ordem de efeito | tabela de decisão |
| D07 | Contador **não** incrementado no sucesso → cupom vira infinito | efeito ausente | tabela de decisão |
| D08 | Dois pedidos simultâneos estouram o limite (sem lock / increment atômico) | concorrência | heurística de race |
| D09 | Policy aplicada só no form do Filament; request direto ao backend passa | autorização vertical | matriz de permissão |
| D10 | Usuário comum enxerga cupons expirados/inativos na listagem | escopo de leitura | matriz de permissão |
| D11 | Valor do desconto aceita `0` ou negativo | limite de domínio | BVA |
| D12 | Data de validade no passado aceita na criação | validação de entrada | partição |
| D13 | Auditoria não grava quem aplicou (fica nulo) ou grava o usuário errado | efeito ausente | rastreio de efeito |
| D14 | Validade avaliada em UTC com app em `America/Sao_Paulo` → 3h de janela errada | timezone | heurística de data |
| D15 | Cupom desativado / soft-deleted continua aplicável | estado | transição de estado |
| D16 | Percentual em `float` → centavo perdido no arredondamento | precisão monetária | BVA / oráculo exato |
| D17 | Código com espaço nas bordas não normalizado → `" PROMO10"` vira outro cupom | normalização | partição de string |
| D18 | Mesmo cupom aplicado duas vezes no mesmo pedido acumula desconto | idempotência | heurística de idempotência |

**Total: 18 mutantes.**

## Ambiguidades do card que deveriam virar pergunta no `00-requisito.md`

| ID | Ambiguidade | Defeito(s) que ela esconde |
|----|-------------|----------------------------|
| A01 | "porcentagem" sem teto declarado | D01 |
| A02 | desconto maior que o total — zera ou fica negativo? | D02 |
| A03 | "dentro da validade" — inclui o próprio dia? qual hora? qual timezone? | D03, D14 |
| A04 | limite de usos é global ou por usuário? | D04, D18 |
| A05 | "cupons ativos" — o card nunca definiu o campo/estado `ativo` | D10, D15 |
| A06 | "não pode se repetir" — case-sensitive? com espaços? | D05, D17 |
| A07 | "registrar quem aplicou" — tabela de auditoria, campo no pedido ou log? | D13 |
| A08 | "os outros usuários" — autenticados quaisquer? anônimos também? | D09, D10 |
| A09 | o mesmo cupom pode ser reaplicado no mesmo pedido? | D18 |

**Total: 9 ambiguidades.**
