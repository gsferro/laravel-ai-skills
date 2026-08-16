# Vereditos — Rodada 8 (Cascade, demo-r7, exp-r8)

- Data: 2026-08-15
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r7`
- Conjuntos: `wikis/specs/exp-r8/{cupons-de-desconto,aprovacao-de-compra}/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---:|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 8 (Cascade) **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários). C1 carrega três lacunas declaradas do arnês/mecanismo, idênticas à Rodada 7.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-06` — porcentagem 101/150 recusada; `CT-16` — porcentagem 101/150 inserido direto → aplicação recusada OU total devolvido 0; `CT-32` — 150% → total 0 | Percentual > 100 é barrado na criação e, se existir no banco, o desconto limita-se ao total. |
| D02 | **DETECTA** | `CT-34` — “Então o total devolvido é 0 centavos / E o desconto registrado na trilha é 3000 centavos” | Afirma o piso de zero para desconto fixo maior que o total. |
| D03 | **DETECTA** | `CT-27` — exemplos 15/08/2026 11:59:59 (aceito), 12:00:00 (recusado), 12:00:01 (recusado) | BVA 3-valores no instante de validade. |
| D04 | **DETECTA** | `CT-30` — exemplos limite 3 × usos 1/2/3/4; `CT-31` — “exatamente uma é aceita” | Borda do limite inclusiva e disputa do último uso. |
| D05 | **DETECTA** | `CT-03` — acento normalizado; `CT-13` — criação/edição com maiúsculas/minúsculas e espaços; `CT-04` — unicidade por tenant | Normalização de case e acentos na criação e na busca. |
| D06 | **DETECTA** | `CT-37` — “Então a aplicação é recusada / E o contador de usos do cupom continua 1 / E a trilha do cupom continua com 1 linha” | Cupom inválido não consome uso nem gera trilha. |
| D07 | **DETECTA** | `CT-35` — “Então o contador de usos do cupom é 1 / E a trilha cupom_usos tem 1 linha”; `CT-36` | A aplicação bem-sucedida força o consumo exato. |
| D08 | **DETECTA** | `CT-31` — “exatamente uma é aceita / E o contador final é 1 / E a trilha tem exatamente 1 linha” | Disputa atômica pelo último uso. |
| D09 | **DETECTA** | `CT-41` — matriz papel × ação; `CT-42` — POST direto recusado com 403; `CT-43` — PUT/PATCH direto recusado com 403 | Autorização exercitada na ação e por fora do componente de UI. |
| D10 | **DETECTA** | `CT-20` — “o cupom ATIVO aparece / VENCIDO, CHEIO e VENCIDO_E_CHEIO não aparecem” | `panel_user` só vê cupons ativos. |
| D11 | **DETECTA** | `CT-06` — exemplos 0 e negativo recusados para ambos os tipos; `CT-11`, `CT-12`, `CT-54` | Valor 0 e negativo barrados na criação e edição. |
| D12 | **DETECTA** | `CT-09` — “15/08/2026 11:59:59 é recusado na criação”; `CT-57` — validade no passado inserida direto → aplicação recusada | Validade futura exigida na criação e na aplicação. |
| D13 | **DETECTA** | `CT-35` — “a trilha cupom_usos tem 1 linha atribuída a Carlos”; `CT-39` — “a linha da trilha está atribuída a Carlos”; `CT-49` — `aplicado_por_id` não é nulo | Quem aplica é gravado corretamente. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-03** — `CT-59` tenta divergir fuso do app e banco, mas o arnês não consegue produzir diferença observável. | Nenhum cenário consegue fixar fuso do app × banco de forma a fazer a borda de 3h divergir. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-04** — `CT-60` assume exclusão física; soft-delete está fora do mecanismo escolhido. | O mecanismo de exclusão é físico, então “cupom removido ainda aplica” não se aplica. |
| D16 | **DETECTA** | `CT-33` — “Então o total devolvido é 7100 centavos / E o desconto registrado é 2900 centavos” para 29% de 10000 | Oráculo exato sobre arredondamento/truncamento de percentual. |
| D17 | **DETECTA** | `CT-13` — criação/edição com `"  promo10 "`, `"PROMO 10"`, `"  PROMO10 "`; `CT-24`, `CT-51`, `CT-53` | `trim` e normalização de código nas bordas. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-05** — `CT-58`: agregado `Pedido` não existe no escopo, então idempotência no pedido é inexpressável. | Não existe cenário que reaplique o mesmo cupom ao mesmo pedido. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 60 no `04` + 2 no `05` = **62**
- **Densidade**: 15 detectados / 62 ≈ **0,24**

### Caracterização da técnica (C1)

O conjunto deriva de **BVA 3-valores, partição de equivalência, matriz papel × ação e rastreio de efeito**. As lacunas declaradas são limites do arnês (fuso, soft-delete, agregado externo), não da técnica de derivação.

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-09` — “operações sobre aprovada são recusadas” com linhas `aprovar`/`rejeitar` sobre rascunho | Rascunho não aceita aprovação nem rejeição. |
| E02 | **DETECTA** | `CT-46` — “Quando ela tenta editar o centro ... Então a operação é recusada / E o centro gravado continua TI / E o valor gravado continua 6.000,00” | Editar campos decisivos após envio é recusado e os valores gravados não mudam. |
| E03 | **DETECTA** | `CT-06` — exemplos 4.999,99 / 5.000,00 / 5.000,01; `CT-07` — “5.000,00 passa a aprovada; 5.000,01 passa a aguardando_diretor” | BVA 3-valores na fronteira exata do limite. |
| E04 | **DETECTA** | `CT-11` — “Quando Dora tenta aprovar antes de Ana / Então a operação é recusada / E a situação continua aguardando_gestor” | Diretor não decide antes do gestor. |
| E05 | **DETECTA** | `CT-08` — exemplos justificativa vazia recusada; `CT-18` — chama `rejeitar()` diretamente com justificativa vazia e uma exceção é lançada | Justificativa obrigatória no formulário e no model. |
| E06 | **DETECTA** | `CT-21` — “rejeição volta a rascunho / E Beatriz pode reenviar”; `CT-22` — “histórico tem 4 etapas” (ciclo completo preservado) | Rejeição volta ao rascunho sem apagar o histórico. |
| E07 | **DETECTA** | `CT-16` — “Rui (gestor de RH) tenta aprovar solicitação do TI / Então a operação é recusada”; `CT-53` — mudança de centro em rascunho recalcula gestor | Só o gestor do centro da solicitação pode aprovar. |
| E08 | **DETECTA** | `CT-14` — “Beatriz tenta aprovar a própria solicitação / Então a operação é recusada”; `CT-52` — solicitante = gestora ainda precisa de diretor para valores acima do limite | Solicitante não aprova a própria solicitação; segregação de função respeitada. |
| E09 | **DETECTA** | `CT-24` — “cancelar depois de aprovada é recusado”; `CT-25` — exemplos de cancelar em diferentes estados | Cancelar só é aceito em trânsito, nunca depois de aprovada. |
| E10 | **DETECTA** | `CT-10` — “notificação por e-mail é enviada para Ana / E nem Beatriz nem Dora recebem”; `CT-14` — “Dora recebe notificação / E Beatriz não recebe” | E-mail vai só para o próximo aprovador. |
| E11 | **DETECTA** | `CT-14` — “aprovação do gestor notifica o diretor”; `CT-30` — “aprovação final não notifica ninguém” | Avanço para diretor notifica diretor; aprovação final não notifica. |
| E12 | **DETECTA** | `CT-46` — tentativa de editar valor/centro em trânsito é recusada; `CT-53` — mudança de centro só possível em rascunho | Campos decisivos não mudam depois de enviados, então reavaliação é impossível. |
| E13 | **DETECTA** | `CT-22` — “histórico tem 4 etapas”; `CT-28` — “histórico mostra quem decidiu, quando e justificativa”; `CT-49` | Histórico append-only e completo. |
| E14 | **DETECTA** | `CT-03` — “Ana não exclui rascunho de Beatriz”; `CT-09` — “excluir aprovada recusada”; `CT-43` — DELETE direto em rascunho de outro recusado | Excluir só permitido em rascunho e pelo solicitante. |
| E15 | **DETECTA** | `CT-12` — “duas diretoras aprovam simultaneamente / exatamente uma é aceita / histórico tem 2 etapas”; `CT-15` — “duplo clique gestor / histórico tem 1 etapa” | Concorrência não grava etapas duplicadas. |
| E16 | **DETECTA** | `CT-51` — “badge mostra Aguardando diretor / E não mostra Aprovada” quando Ana aprovou 6.000,00; `CT-20` — badges distintos | Tela reflete o estado real. |
| E17 | **DETECTA** | `CT-54` — exemplos -0,01 (falha), 0,00 (falha), 0,01 (aceito); `CT-01` — criação com valor válido | BVA na fronteira inferior do valor. |
| E18 | **DETECTA** | `CT-31` — “falha forçada após o ponto da notificação / a operação falha / a solicitação continua aguardando_gestor / Ana não recebe notificação” | E-mail não sobrevive a uma gravação que falha. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 58 no `04` + 3 no `05` = **61**
- **Densidade**: 18 detectados / 61 ≈ **0,30**

### Caracterização da técnica (C2)

O conjunto usa **máquina de estados (tabela estado × evento), BVA 3-valores, rastreio de efeito de notificação, matriz papel × ação e heurística de race**. Não restou lacuna declarada no catálogo.

---

## Comparação com Rodada 7

| Aspecto | Rodada 7 (Claude Code) | Rodada 8 (Cascade) |
|---|---|---|
| C1 detectados / 18 | 15 / 18 (83,3 %) | 15 / 18 (83,3 %) |
| C1 lacunas declaradas | D14, D15, D18 | D14, D15, D18 |
| C1 lacunas cegas | 0 | 0 |
| C2 detectados / 18 | 18 / 18 (100 %) | 18 / 18 (100 %) |
| C2 lacunas declaradas | 0 | 0 |
| C2 lacunas cegas | 0 | 0 |
| Cenários C1 (`04` + `05`) | 60 | 62 |
| Cenários C2 (`04` + `05`) | 58 | 61 |
| Densidade C1 | 0,25 | 0,24 |
| Densidade C2 | 0,31 | 0,30 |

### Diferenças de detecção

- **Nenhuma diferença no placar final**. Os mesmos 15/18 em C1 e 18/18 em C2 foram alcançados.
- Os três itens não detectados em C1 são **idênticos** entre as rodadas: D14 (timezone), D15 (soft-delete) e D18 (idempotência no `Pedido`, fora de escopo).

### Gaps, oráculos fracos e falsos ✅

- **Gaps**: C1 continua 0,167 abaixo do critério de parada. Os gaps são os mesmos da Rodada 7: arnês incapaz de medir fuso (D14), mecanismo de exclusão física (D15) e agregado `Pedido` inexistente (D18).
- **Oráculos fracos**: nenhum identificado. Ambos os conjuntos usam asserções de igualdade, não-efeito com destinatário real e valores discriminantes.
- **Falsos ✅**: nenhum identificado.

### Destaques do conjunto Cascade

1. Cenários adicionais em C1 (`CT-51`, `CT-52`, `CT-53`, `CT-56`, `CT-57`) aumentam a superfície de normalização e fronteiras por fora da tela.
2. C2 acrescenta `CT-52` (solicitante = gestora precisa de diretor) e `CT-53` (mudança de centro em rascunho recalcula gestor), ambos com oráculos claros sobre E07/E08.
3. O número de cenários cresceu levemente sem melhorar o placar, o que reduz a densidade. Isso sugere que o conjunto adicionou redundância no ponto de entrada, mas não encontrou matadores para as três lacunas declaradas.

---

## Impressões gerais

1. **C1 está em 83,3 %** — mesmo patamar da Rodada 7. As três lacunas declaradas são **limites do arnês e do escopo**, não regressões de técnica.

2. **C2 fechou em 100 %** — igual à Rodada 7. O conjunto cobre todos os mutantes do catálogo com asserções explícitas.

3. **O agente Cascade derivou um conjunto estruturalmente equivalente** ao da Rodada 7, com pequenas diferenças na granularidade e no número de cenários. Não houve ganho nem perda na DDR.

4. **Risco para o critério de parada**: C1 ainda precisa de `DDR >= 0,85`. Como as três lacunas são de arnês/escopo, o critério depende de aceitar as lacunas declaradas como inevitáveis.

5. **Recomendação**: como na Rodada 7, registrar D14, D15 e D18 como **débitos de arnês**. Se o experimento quiser fechar C1, o projeto-cobaia precisaria de: (a) agregado `Pedido` para D18; (b) mecanismo de exclusão lógica para D15; (c) controle de fuso aplicável em teste para D14.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
