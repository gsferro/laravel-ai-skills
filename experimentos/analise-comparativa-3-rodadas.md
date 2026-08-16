# Análise Comparativa — 3 Modelos em Agentes Diferentes

> Rodadas 7, 8 e 9 do experimento controlado de `feature-test-design`
> Data: 2026-08-15

---

## 1. Metodologia

Três rodadas independentes, mesmo oráculo fixo, mesmo juiz cego, mesmo protocolo.

| Rodada | Agente | Modelo | Project-cobaia | Exp |
|---|---|---|---|---|
| 7 | Claude Code (terminal) | Claude Sonnet 4 | `demo-r7` | `exp-r7` |
| 8 | Cascade (IDE) | Claude Sonnet 4 | `demo-r8` | `exp-r8` |
| 9 | Cascade (IDE) | GLM 5.2 High | `demo-r8` | `exp-r9` |

**Constantes em todas as rodadas:**
- Oráculo fixo: `experimentos/protocolo/oraculo-fixo/` (00-requisito.md + 01-plano-acao.md)
- Catálogos de defeitos: 18 mutantes por cenário (D01-D18, E01-E18)
- Juiz cego: `PROMPT-JUIZ-CEGO.md` (sem acesso ao requisito, PRD ou identidade do agente)
- Skill: `feature-test-design` 1.9.0 + `feature-wiki` 3.0.0
- Protocolo: `PROTOCOLO.md` (DDR >= 0,85 em ambos cenários; N_CT <= 2× baseline)

---

## 2. Placar Consolidado

### 2.1 Defect Detection Rate (DDR)

| Cenário | Rodada 7 (Claude Code) | Rodada 8 (Cascade) | Rodada 9 (GLM 5.2 High) |
|---|---:|---:|---:|
| C1 — Cupons | 15/18 = **83,3%** | 15/18 = **83,3%** | 15/18 = **83,3%** |
| C2 — Aprovação | 18/18 = **100%** | 18/18 = **100%** | 18/18 = **100%** |

**Nenhuma diferença de detecção entre os três modelos.** Os mesmos 15 defeitos são detectados em C1 e os mesmos 18 em C2, em todas as rodadas. Os mesmos 3 defeitos (D14, D15, D18) não são detectados em C1 em nenhuma rodada — todos lacunas declaradas de arnês/escopo.

### 2.2 Tabela de Veredito por Defeito

#### Cenário 1 — Cupons de desconto

| Defeito | R7 | R8 | R9 | Classe |
|---|---|---|---|---|
| D01 — Percentual > 100 | ✅ | ✅ | ✅ | limite de domínio |
| D02 — Fixo > total (negativo) | ✅ | ✅ | ✅ | limite de saída |
| D03 — Validade off-by-one | ✅ | ✅ | ✅ | BVA data |
| D04 — Limite off-by-one | ✅ | ✅ | ✅ | BVA contador |
| D05 — Case-sensitive | ✅ | ✅ | ✅ | normalização |
| D06 — Contador antes de validar | ✅ | ✅ | ✅ | ordem de efeito |
| D07 — Contador não incrementa | ✅ | ✅ | ✅ | efeito ausente |
| D08 — Concorrência no limite | ✅ | ✅ | ✅ | race |
| D09 — Policy só no form | ✅ | ✅ | ✅ | autorização vertical |
| D10 — Lista sem filtro | ✅ | ✅ | ✅ | escopo de leitura |
| D11 — Valor 0/negativo | ✅ | ✅ | ✅ | limite de domínio |
| D12 — Validade no passado | ✅ | ✅ | ✅ | validação de entrada |
| D13 — Auditoria sem quem | ✅ | ✅ | ✅ | rastreio de efeito |
| D14 — Timezone UTC | ❌ L.decl | ❌ L.decl | ❌ L.decl | timezone (arnês) |
| D15 — Soft-delete aplicável | ❌ L.decl | ❌ L.decl | ❌ L.decl | estado (mecanismo) |
| D16 — Float vs inteiro | ✅ | ✅ | ✅ | precisão monetária |
| D17 — Espaços nas bordas | ✅ | ✅ | ✅ | normalização |
| D18 — Idempotência no pedido | ❌ L.decl | ❌ L.decl | ❌ L.decl | idempotência (escopo) |

#### Cenário 2 — Aprovação de compra

| Defeito | R7 | R8 | R9 | Classe |
|---|---|---|---|---|
| E01 — Aprovar em rascunho | ✅ | ✅ | ✅ | máquina de estados |
| E02 — Editar em trânsito | ✅ | ✅ | ✅ | máquina de estados |
| E03 — BVA no R$ 5.000 | ✅ | ✅ | ✅ | fronteira |
| E04 — Diretor antes do gestor | ✅ | ✅ | ✅ | ordem de etapas |
| E05 — Rejeição sem justificativa | ✅ | ✅ | ✅ | validação condicional |
| E06 — Rejeição mantém aprovações | ✅ | ✅ | ✅ | reset de estado |
| E07 — Gestor de outro centro | ✅ | ✅ | ✅ | IDOR |
| E08 — Solicitante aprova própria | ✅ | ✅ | ✅ | segregação de função |
| E09 — Cancelar após aprovada | ✅ | ✅ | ✅ | transição inválida |
| E10 — E-mail para aprovador errado | ✅ | ✅ | ✅ | efeito colateral |
| E11 — Sem notificação ao diretor | ✅ | ✅ | ✅ | efeito ausente |
| E12 — Valor alterado em trânsito | ✅ | ✅ | ✅ | recomputação de fluxo |
| E13 — Histórico não gravado | ✅ | ✅ | ✅ | rastreio de efeito |
| E14 — Excluir em trânsito | ✅ | ✅ | ✅ | transição inválida |
| E15 — Duplo clique | ✅ | ✅ | ✅ | race/idempotência |
| E16 — Tela inconsistente | ✅ | ✅ | ✅ | consistência de UI |
| E17 — Valor zero/negativo | ✅ | ✅ | ✅ | limite de domínio |
| E18 — E-mail em falha | ✅ | ✅ | ✅ | atomicidade |

---

## 3. Métricas de Eficiência

### 3.1 Volume e Densidade

| Métrica | R7 (Claude Code) | R8 (Cascade) | R9 (GLM 5.2 High) |
|---|---:|---:|---:|
| **Cenários C1** (04 + 05) | 58 + 2 = **60** | 20 + 4 = **24** | 18 + 4 = **22** |
| **Cenários C2** (04 + 05) | 56 + 2 = **58** | 26 + 5 = **31** | 31 + 5 = **36** |
| **Total de cenários** | **118** | **55** | **58** |
| **Densidade C1** (detecções/CT) | 0,25 | 0,63 | **0,68** |
| **Densidade C2** (detecções/CT) | 0,31 | **0,58** | 0,50 |
| **Densidade global** | 0,28 | **0,60** | 0,57 |

### 3.2 Browser (CT-B)

| Métrica | R7 | R8 | R9 |
|---|---:|---:|---:|
| CT-B em C1 | 2 | 4 | 4 |
| CT-B em C2 | 2 | 5 | 5 |
| Total CT-B | 4 | 9 | 9 |

### 3.3 Iterações para fechar C2

| Rodada | Precisou iteração? | Detalhe |
|---|---|---|
| R7 | **Sim** — revisão adversarial robusta | 11 cenários adicionados (CT-46…CT-56) |
| R8 | **Sim** — uma iteração | CT-25 e CT-26 adicionados (`rascunho × aprovar`, `aguardando_* × excluir`) |
| R9 | **Não** — primeira passagem | Matriz 5×6 completa desde o início (CT-06b, CT-08b, CT-29) |

---

## 4. Análise por Dimensão

### 4.1 Eficácia (DDR)

**Empate técnico.** Os três modelos+agentes detectam exatamente os mesmos defeitos. Nenhum modelo detecta um defeito que outro não detecta. Isso sugere que:

- A **skill `feature-test-design`** é o fator dominante — o pipeline de derivação (SFDIPOT, Example Mapping, técnicas formais, gate de falsificabilidade) produz o mesmo conjunto de cobertura independentemente do modelo.
- O **oráculo fixo** (00-requisito.md + 01-plano-acao.md) já contém as premissas que desambiguam as 9 ambiguidades do card, eliminando a variabilidade de interpretação.
- As **3 lacunas de C1** (D14, D15, D18) são propriedades do arnês/escopo, não do modelo — confirmado em 3 rodadas independentes.

### 4.2 Eficiência (Volume × Densidade)

**R7 é o mais verboso** (118 cenários, densidade 0,28). O Claude Code tende a gerar mais variações de cada regra, incluindo cenários redundantes que não matam mutantes adicionais.

**R8 é o mais equilibrado** (55 cenários, densidade 0,60). O Cascade com Claude Sonnet 4 poda agressivamente variações redundantes, mantendo cobertura completa.

**R9 é o mais enxuto em C1** (22 cenários, densidade 0,68) mas **mais completo em C2** (36 cenários, densidade 0,50). O GLM 5.2 High priorizou fechamento completo da matriz estado × operação em C2 sobre densidade, mas podou mais agressivamente em C1.

| Dimensão | Vencedor | Margem |
|---|---|---|
| Menor volume C1 | **R9** (22) | 2 a menos que R8; 38 a menos que R7 |
| Maior densidade C1 | **R9** (0,68) | +0,05 vs R8; +0,43 vs R7 |
| Menor volume C2 | **R8** (31) | 5 a menos que R9; 27 a menos que R7 |
| Maior densidade C2 | **R8** (0,58) | +0,08 vs R9; +0,27 vs R7 |
| Menor volume total | **R8** (55) | 3 a menos que R9; 63 a menos que R7 |
| Maior densidade global | **R8** (0,60) | +0,03 vs R9; +0,32 vs R7 |

### 4.3 Convergência (Iterações para fechar)

**R9 é o único que fechou C2 sem iteração.** Isso indica que o GLM 5.2 High aplicou a regra do produto cartesiano fechado (5 estados × 6 operações = 30 células) mais rigorosamente na primeira passagem.

- **R7** precisou de revisão adversarial com 11 cenários adicionais
- **R8** precisou de 1 iteração com 2 cenários adicionais (CT-25, CT-26)
- **R9** cobriu as células `rascunho × aprovar` (CT-06b) e `aguardando_* × excluir` (CT-08b + CT-29) desde o início

Isso sugere que o GLM 5.2 High tem melhor aderência à regra "produto cartesiano fechado" da skill, possivelmente porque processa instruções estruturais de forma mais literal.

### 4.4 Qualidade das Asserções

**Os três conjuntos usam asserções de alta qualidade:**
- Igualdade (não desigualdade) como oráculo
- Não-efeito com destinatário real (ex: "Rui não recebe notificação", não apenas "ninguém recebe")
- Valores discriminantes (ex: 29% de 10.000 = 2.900, não ~2.900)
- Estado gravado como oráculo (ex: "valor gravado permanece 4.000,00")

**Nenhum conjunto tem:**
- Falsos ✅ (cenários que parecem detectar mas não exercitam o valor que revela o defeito)
- Oráculos fracos (asserções que passam mesmo com o mutante presente)

### 4.5 Cobertura de Browser

R7 gerou apenas 2 CT-B por cenário (mínimo do gate). R8 e R9 geraram 4 em C1 e 5 em C2, cobrindo:
- Rótulo dinâmico por tipo (C1)
- Ausência de affordance para panel_user (C1)
- Fluxo completo de criação (C1)
- Badge por situação (C2)
- Ausência de botões de aprovação para solicitante (C2)
- Presença de botões para gestor (C2)
- Modal de rejeição com justificativa (C2)
- Histórico exibido na visualização (C2)

R8 e R9 são idênticos na cobertura de browser.

---

## 5. Análise por Modelo/Agente

### 5.1 Claude Code (R7) — Claude Sonnet 4

**Perfil: Verbose e Iterativo**

- Gera 2,1× mais cenários que R8 e R9 (118 vs. 55-58)
- Densidade baixa (0,28) — muitos cenários não matam mutantes adicionais
- Precisou de revisão adversarial robusta (11 cenários adicionados) para fechar C2
- CTs bem estruturados, com asserções de alta qualidade
- Tendência a explorar variações de cada regra exaustivamente

**Hipótese:** O Claude Code no terminal tem menos restrições de contexto e tende a gerar mais variações. A revisão adversarial é parte do fluxo natural do agente.

### 5.2 Cascade + Claude Sonnet 4 (R8)

**Perfil: Equilibrado e Eficiente**

- Melhor relação volume × densidade (55 CTs, densidade 0,60)
- Poda agressiva de variações redundantes
- Precisou de 1 iteração para fechar C2 (2 cenários adicionados)
- CT-B mais ricos que R7 (9 vs. 4)
- Melhor densidade global entre os três

**Hipótese:** O Cascade na IDE aplica melhor o princípio "1 CT, 1 mutante" da skill, evitando redundância. A iteração necessária sugere que o produto cartesiano não é aplicado automaticamente.

### 5.3 Cascade + GLM 5.2 High (R9)

**Perfil: Riguroso e Não-Iterativo**

- Único que fechou C2 sem iteração
- C1 mais enxuto (22 CTs, densidade 0,68 — maior entre os três)
- C2 mais completo (36 CTs, densidade 0,50 — menor que R8)
- Matriz estado × operação declarada com auditoria completa (30/30 células)
- Aplicou produto cartesiano fechado desde a primeira passagem

**Hipótese:** O GLM 5.2 High processa instruções estruturais de forma mais literal, aplicando regras como "produto cartesiano fechado" sem necessidade de revisão. Em C1, poda mais agressivamente; em C2, prioriza fechamento completo sobre densidade.

---

## 6. Matriz de Trade-off

| Critério | R7 (Claude Code) | R8 (Cascade) | R9 (GLM 5.2 High) |
|---|---|---|---|
| Eficácia (DDR) | ★★★★★ | ★★★★★ | ★★★★★ |
| Eficiência (volume) | ★★☆☆☆ | ★★★★★ | ★★★★☆ |
| Densidade C1 | ★★☆☆☆ | ★★★★☆ | ★★★★★ |
| Densidade C2 | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| Convergência (sem iteração) | ★☆☆☆☆ | ★★★☆☆ | ★★★★★ |
| Qualidade de asserção | ★★★★★ | ★★★★★ | ★★★★★ |
| Cobertura de browser | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| Rastreabilidade (matriz declarada) | ★★★☆☆ | ★★★★☆ | ★★★★★ |

---

## 7. Conclusões

### 7.1 A skill é o fator dominante

Os três modelos+agentes produzem **o mesmo placar de detecção** porque a skill `feature-test-design` 1.9.0 já codifica o pipeline de derivação (SFDIPOT, Example Mapping, técnicas formais, gate de falsificabilidade, matriz estado × operação). O modelo executa o pipeline; não o reinventa.

### 7.2 O modelo influencia eficiência, não eficácia

- **Volume**: R7 gera 2× mais CTs; R8 e R9 geram ~metade disso
- **Densidade**: R9 é o mais denso em C1; R8 é o mais denso em C2
- **Convergência**: R9 é o único que não precisou iteração para fechar C2

### 7.3 O agente influencia o formato

- **Claude Code (terminal)**: mais verboso, revisão adversarial embutida
- **Cascade (IDE)**: mais enxuto, iteração necessária para fechamento
- A troca de modelo dentro do mesmo agente (R8→R9) manteve o formato mas melhorou a convergência

### 7.4 As lacunas de C1 são do arnês, não do modelo

D14 (timezone), D15 (soft-delete) e D18 (idempotência no pedido) não são detectados em nenhuma rodada, independentemente de modelo ou agente. Isso confirma que são **débitos de arnês** — o projeto-cobaia não tem mecanismo para exercitar esses defeitos.

### 7.5 Recomendação para próximas rodadas

1. **Para fechar C1**: evoluir o arnês (agregado `Pedido`, exclusão lógica, controle de fuso) — não adianta trocar de modelo
2. **Para medir diferença entre modelos**: usar cenários com mais ambiguidade no oráculo, onde a interpretação do modelo importa mais
3. **Para medir diferença entre agentes**: manter o modelo constante e variar o agente (R7 vs. R8 já isolou isso)
4. **Para medir convergência**: contar iterações até fechar C2 — R9 provou que é possível em 1 passagem

---

## 8. Resumo Executivo

| Pergunta | Resposta |
|---|---|
| Os três modelos detectam os mesmos defeitos? | **Sim.** 15/18 em C1, 18/18 em C2, em todas as rodadas. |
| Qual modelo gera menos CTs? | **R9 em C1** (22); **R8 em C2** (31). |
| Qual modelo tem maior densidade? | **R9 em C1** (0,68); **R8 em C2** (0,58). |
| Qual modelo fecha C2 sem iteração? | **Apenas R9** (GLM 5.2 High). |
| Há falsos ✅ ou oráculos fracos? | **Não**, em nenhuma rodada. |
| As lacunas de C1 são do modelo ou do arnês? | **Do arnês**, confirmado em 3 rodadas. |
| A skill ou o modelo é o fator dominante? | **A skill.** O modelo influencia eficiência, não eficácia. |
