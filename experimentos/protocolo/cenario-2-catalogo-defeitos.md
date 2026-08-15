# Catálogo de Defeitos — Cenário 2 (FERRO-830, aprovação de solicitação de compra)

> Escrito **antes** de qualquer execução da skill. Cenário escolhido para exercitar
> máquina de estados, autorização horizontal e efeitos colaterais (notificação) —
> exatamente o que o cenário 1 (regra de cálculo) não cobre.

| ID | Defeito plantado (mutante) | Classe | Técnica que o revela |
|----|---------------------------|--------|----------------------|
| E01 | Aprovar solicitação ainda em rascunho (pula o envio) | transição inválida | máquina de estados |
| E02 | Editar solicitação já enviada | transição inválida | máquina de estados |
| E03 | Valor exatamente R$ 5.000,00 roteado errado (com/sem diretor) | fronteira | BVA 3-valores |
| E04 | Diretor aprova antes do gestor | ordem de etapas | máquina de estados 1-switch |
| E05 | Rejeição aceita sem justificativa | validação condicional | tabela de decisão |
| E06 | Rejeitada volta a rascunho mantendo as aprovações anteriores | reset de estado | máquina de estados |
| E07 | Gestor de **outro** centro de custo consegue aprovar | autorização horizontal (IDOR) | matriz de permissão |
| E08 | Solicitante aprova a própria solicitação | segregação de função | matriz de permissão |
| E09 | Cancelar depois de aprovada | transição inválida | máquina de estados |
| E10 | E-mail disparado para o aprovador errado, ou a cada save | efeito colateral | rastreio de efeito |
| E11 | Nenhuma notificação quando a solicitação avança para o diretor | efeito ausente | tabela de decisão |
| E12 | Valor alterado de 4.000 para 6.000 após envio não reavalia a etapa do diretor | recomputação de fluxo | tabela de decisão |
| E13 | Histórico de quem aprovou cada etapa não gravado ou sobrescrito | efeito ausente | rastreio de efeito |
| E14 | Excluir solicitação já enviada | transição inválida | máquina de estados |
| E15 | Duplo clique do gestor avança duas etapas de uma vez | idempotência / race | heurística de idempotência |
| E16 | Tela mostra "Aprovada" enquanto ainda falta a etapa do diretor | consistência de exibição | teste de UI/estado |
| E17 | Valor zero ou negativo aceito | limite de domínio | BVA |
| E18 | E-mail sai mesmo quando a gravação da aprovação falha (efeito fora da transação) | atomicidade | heurística de falha |

**Total: 18 mutantes.**

## Ambiguidades do card que deveriam virar pergunta no `00-requisito.md`

| ID | Ambiguidade | Defeito(s) que ela esconde |
|----|-------------|----------------------------|
| B01 | "acima de R$ 5.000" — o próprio 5.000 entra? | E03 |
| B02 | "gestor do centro de custo" — como se determina? um por CC? | E07 |
| B03 | "volta para rascunho" — descarta as aprovações já dadas? | E06 |
| B04 | "antes da aprovação final" — cancelar depois do gestor e antes do diretor pode? | E09 |
| B05 | o solicitante pode ser o gestor do próprio centro de custo? | E08 |
| B06 | valor alterado após envio reavalia o fluxo? | E12 |
| B07 | rejeição notifica o solicitante? o card só fala em "próximo aprovador" | E10 |
| B08 | faixa e moeda do valor (mínimo, máximo, casas decimais) | E17 |
| B09 | "não pode mais mexer" — inclui excluir? | E14 |

**Total: 9 ambiguidades.**
