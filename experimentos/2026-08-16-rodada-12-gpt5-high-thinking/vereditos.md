# Vereditos — Rodada 12 (Cascade, GPT‑5 High Thinking, demo-r8, exp-r12)

- Data: 2026-08-16
- Modelo: GPT‑5 High Thinking
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r12\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

C1 repete as **mesmas 3 lacunas declaradas** (D14, D15, D18). C2 fecha 100 % na primeira passagem, com matriz 5×6 completa e todos os efeitos cobertos (autorização, concorrência, notificação, UI e histórico).

---

## Observações do juiz

- C1 tem **densidade alta** (19 cenários → 0,79), alinhado com R10/R11. Os discriminantes monetários estão marcados como “exatamente”, evitando flutuação.
- C2 mantém o padrão R9–R11: 37 cenários, 0 iterações, cobrindo `rascunho × aprovar`, `aguardando_* × excluir`, e isolamento transacional de e-mail. A fronteira de R$ 5.000,00 é tratada com `>` estrito.

---

## Convergência entre famílias

| Família | Modelos testados | Eficácia (C1/C2) | Iterações C2 | Volume C1/C2 |
|---|---|---|---|---|
| Anthropic | Claude Sonnet 4 (R7/R8) | 83,3% / 100% | 2 e 1 | 60/58 e 24/31 |
| Zhipu | GLM 5.2 High (R9) | 83,3% / 100% | 0 | 22 / 36 |
| Moonshot | Kimi K3 High (R10) | 83,3% / 100% | 0 | 19 / 37 |
| Google | Gemini 3.7 Flash High (R11) | 83,3% / 100% | 0 | 19 / 37 |
| OpenAI | GPT‑5 High Thinking (R12) | 83,3% / 100% | 0 | 19 / 37 |

Conclusão: a skill + oráculo fixo são dominantes; as famílias só variam na eficiência (volume/densidade), não na eficácia (DDR), e os modelos recentes convergem sem iteração.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
