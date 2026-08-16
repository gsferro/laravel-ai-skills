# Vereditos — Rodada 13 (Cascade, DeepSeek V4 Pro Max, demo-r8, exp-r13)

- Data: 2026-08-16
- Modelo: DeepSeek V4 Pro Max
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r13\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

C1: mesmas 3 lacunas declaradas (D14 timezone, D15 soft-delete, D18 idempotência no pedido).
C2: 100 % na primeira passagem, matriz 5×6 completa, 0 iterações.

---

## Métricas

| Métrica | Valor |
|---|---|
| Cenários C1 (04 + 05) | 15 + 4 = **19** |
| Cenários C2 (04 + 05) | 31 + 5 = **36** |
| Total de cenários | **55** |
| Densidade C1 | 15/19 ≈ **0,79** |
| Densidade C2 | 18/36 = **0,50** |
| Iterações C2 | **0** |

---

## Comparação Consolidada — 7 Rodadas, 6 Famílias de Modelos

| # | Agente | Família | C1 DDR | C2 DDR | Iter. C2 | Vol. C1 | Vol. C2 | Dens. C1 | Dens. C2 |
|---|---|---|---|---|---|---|---|---|---|
| R7 | Claude Code | **Anthropic** (Claude Sonnet 4) | 83,3% | 100% | 2 | 60 | 58 | 0,25 | 0,31 |
| R8 | Cascade | **Anthropic** (Claude Sonnet 4) | 83,3% | 100% | 1 | 24 | 31 | 0,63 | 0,58 |
| R9 | Cascade | **Zhipu** (GLM 5.2 High) | 83,3% | 100% | 0 | 22 | 36 | 0,68 | 0,50 |
| R10 | Cascade | **Moonshot** (Kimi K3 High) | 83,3% | 100% | 0 | 19 | 37 | 0,79 | 0,49 |
| R11 | Cascade | **Google** (Gemini 3.7 Flash High) | 83,3% | 100% | 0 | 19 | 37 | 0,79 | 0,49 |
| R12 | Cascade | **OpenAI** (GPT‑5 High Thinking) | 83,3% | 100% | 0 | 19 | 37 | 0,79 | 0,49 |
| R13 | Cascade | **DeepSeek** (V4 Pro Max) | 83,3% | 100% | 0 | 19 | 36 | 0,79 | 0,50 |

---

## Análise

### Eficácia (DDR) — invariante entre famílias

**7 rodadas, 6 famílias, placar idêntico.** A skill `feature-test-design` 1.9.0 + oráculo fixo produzem o mesmo DDR em qualquer modelo testado. As 3 lacunas de C1 (D14, D15, D18) são débitos de arnês confirmados em todas as rodadas.

### Eficiência — dois clusters

| Cluster | Rodadas | Volume C1 | Volume C2 | Densidade C1 |
|---|---|---|---|---|
| **Verbose** (agente terminal) | R7 | 60 | 58 | 0,25 |
| **Enxuto** (agente IDE) | R8 | 24 | 31 | 0,63 |
| **Convergente** (modelos recentes) | R9–R13 | 19–22 | 36–37 | 0,68–0,79 |

Modelos de 2025+ (GLM 5.2, Kimi K3, Gemini 3.7, GPT‑5, DeepSeek V4) convergem em **0 iterações** e volumes ~19/36.

### DeepSeek V4 Pro Max — destaque

- Volume total mais baixo da série (55 cenários, empatado com R8).
- C2 com 36 cenários — 1 a menos que R10–R12, sugerindo leve compressão adicional.
- Mantém 0 iterações e 100% DDR em C2.

---

## Conclusão

A hipótese está confirmada: **a skill é o fator dominante**. O modelo influencia eficiência (volume, densidade), não eficácia (DDR). Qualquer modelo de fronteira (2025+) executa o pipeline sem iteração. O workflow "wiki/CTs em modelo pago → implementação em modelo local/grátis" é viável — o insumo gerado é de qualidade invariante entre famílias.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
