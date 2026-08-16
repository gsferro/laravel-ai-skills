# Vereditos — Rodada 11 (Cascade, Gemini 3.7 Flash High, demo-r8, exp-r11)

- Data: 2026-08-16
- Modelo: Gemini 3.7 Flash High
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r11\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 11 **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários). C1 carrega as três lacunas declaradas de arnês/escopo presentes em todas as rodadas. C2 fechou 100 % na primeira passagem sem iteração, com matriz completa de 30 células.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-05` — "porcentagem / 101 → recusado"; `CT-06` — "altera para porcentagem/101 → recusado, mantém 10" | Teto de 100% na criação e na edição. |
| D02 | **DETECTA** | `CT-13` — "fixo 5000 sobre total 3000 → desconto exatamente 3000, final exatamente 0" | Piso de zero com oráculo exato. |
| D03 | **DETECTA** | `CT-07` — "2026-08-15 11:59:59 → recusado; 12:00:00 → recusado; 12:00:01 → aceito" | BVA 3-valores no instante de validade. |
| D04 | **DETECTA** | `CT-12` — "CHEIO válido usos 3 de 3 → recusado, contador 3, trilha 0" | Limite de usos respeitado na borda. |
| D05 | **DETECTA** | `CT-01` — " promo10  → gravado como PROMO10"; `CT-02` — "promo10 contra PROMO10 existente → falha, permanece 1" | Normalização e unicidade insensível a caixa. |
| D06 | **DETECTA** | `CT-12` — "VENCIDO e CHEIO recusam, contador e trilha inalterados" | Cupom inválido não consome uso nem gera trilha. |
| D07 | **DETECTA** | `CT-14` — "contador de usos é 2, trilha contém 1 linha" | Sucesso incrementa contador e trilha. |
| D08 | **DETECTA** | `CT-15` — "duas simultâneas no último uso → 1 aceita, 1 recusada, contador 3, 1 nova linha" | Disputa atômica sob concorrência. |
| D09 | **DETECTA** | `CT-10` — "panel_user tenta criar/editar/excluir diretamente na camada de serviço/HTTP → recusado" | Autorização testada fora do formulário. |
| D10 | **DETECTA** | `CT-11` — "listagem exibe somente ATIVO; VENCIDO e CHEIO não aparecem"; `CT-B03` na UI | Escopo de leitura restrito a ativos. |
| D11 | **DETECTA** | `CT-05` — "0 recusado em porcentagem e fixo"; `CT-06` — "edição para fixo 0 recusada" | Domínio de valor rejeita zero. |
| D12 | **DETECTA** | `CT-07` — passado recusado; `CT-08` — "edita para 2026-01-01 → falha, mantém 2026-12-31" | Validade futura na criação e edição. |
| D13 | **DETECTA** | `CT-14` — "trilha contém 1 linha atribuída a Marina, datada de 2026-08-15 14:30:00, com valor original 10.000 e desconto 1.000" | Quem, quando e valores auditados. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-01** — arnês em UTC fixo; sem controle de fuso em teste. | Débito de arnês. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-02** — mecanismo é exclusão física; "ativo" é estado derivado (P-03). | Fora do mecanismo assumido. |
| D16 | **DETECTA** | `CT-13` — "29% de 10.000 = exatamente 2.900; 5% de 50 = exatamente 2; 50% de 9.999 = exatamente 4.999" | Precisão monetária e truncamento discriminados. |
| D17 | **DETECTA** | `CT-01` — " promo10  → gravado como PROMO10; variantes não existem" | Espaços nas bordas normalizados. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-03** — agregado `Pedido` fora de escopo (P-01). | Inexpressável no arnês. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum
- **Oráculos fracos**: nenhum
- **Total de cenários**: 15 no `04` + 4 no `05` = **19**
- **Densidade**: 15 detectados / 19 ≈ **0,79**

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-07` — "Rui tenta aprovar/rejeitar em rascunho → recusado, permanece rascunho, histórico vazio" | Rascunho não aceita decisão. |
| E02 | **DETECTA** | `CT-09` — "editar em trânsito recusado, valor gravado 4.000,00 e centro TI persistem, histórico mantém etapas" | Edição em trânsito recusada com oráculo persistido. |
| E03 | **DETECTA** | `CT-08` — "4.999,99 → aprovada; 5.000,00 → aprovada; 5.000,01 → aguardando_diretor" | BVA 3-valores na fronteira exata com `>` estrito. |
| E04 | **DETECTA** | `CT-20` — "Dora tenta aprovar em aguardando_gestor → recusado, histórico continua vazio" | Diretor não decide antes do gestor. |
| E05 | **DETECTA** | `CT-12` — "rejeição sem justificativa recusada em gestor e diretor, sem nova etapa"; `CT-B04` na UI | Justificativa obrigatória nas duas etapas. |
| E06 | **DETECTA** | `CT-14` — "diretor rejeita com justificativa preservando etapa do gestor intacta"; `CT-15` — "reenvio recomeça do gestor com 2 etapas preservadas" | Reset para rascunho preservando histórico anterior. |
| E07 | **DETECTA** | `CT-21` — "Carla gestora de RH tenta aprovar TI → recusado"; `CT-27` — "troca de centro recusada, aprovador da vez permanece Rui" | Autorização horizontal de centro de custo. |
| E08 | **DETECTA** | `CT-22` — "Ana sem cargo de gestor tenta aprovar → recusado"; `CT-23` — "Ana gestora do próprio centro aprova 6.000 → aguardando_diretor e não aprovada" | Segregação e premissa A-09 cobertas. |
| E09 | **DETECTA** | `CT-17` — "cancelar aprovada recusado, situação permanece aprovada"; `CT-16` — cancelar em trânsito aceito | Cancelamento restrito a antes da aprovação final. |
| E10 | **DETECTA** | `CT-03` — "edição em rascunho: nenhuma notificação"; `CT-18` — "Dora e Eva recebem, Rui e Ana não"; `CT-26` — "rejeição: nenhuma notificação" | Notificação apenas ao próximo aprovador, sem e-mail em save. |
| E11 | **DETECTA** | `CT-18` — "avanço para diretor notifica Dora e Eva"; `CT-11`/`CT-19` — "aprovação final não notifica" | Notificação emitida estritamente quando há próxima etapa. |
| E12 | **DETECTA** | `CT-09` — "editar valor em trânsito recusado, valor gravado permanece 4.000,00"; `CT-27` — "trocar centro recusado" | Campo decisivo congelado em trânsito. |
| E13 | **DETECTA** | `CT-19` — "histórico tem 2 etapas com gestor/Rui e diretor/Dora"; `CT-30` — "visualização exibe etapas ordenadas com Rui, Dora e timestamps" | Histórico auditável e exibido. |
| E14 | **DETECTA** | `CT-09` — "excluir em aguardando_gestor e aguardando_diretor recusado, histórico preservado" | Exclusão em trânsito recusada. |
| E15 | **DETECTA** | `CT-24` — "duas do gestor simultâneas → 1 etapa"; `CT-25` — "duas de diretores simultâneas → 1 etapa de diretor" | Idempotência e concorrência nas duas etapas. |
| E16 | **DETECTA** | `CT-29` — "5 situações → 5 rótulos distintos"; `CT-B01` — badges distintos | Consistência entre estado interno e exibição de UI. |
| E17 | **DETECTA** | `CT-01` — "-0,01 e 0,00 recusados; 0,01 aceito" | BVA na fronteira inferior de valor. |
| E18 | **DETECTA** | `CT-28` — "falha na persistência da etapa após despacho → aguardando_gestor, sem etapa, Dora não recebe notificação" | Notificação isolada contra falha transacional. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum
- **Oráculos fracos**: nenhum
- **Total de cenários**: 32 no `04` + 5 no `05` = **37**
- **Densidade**: 18 detectados / 37 ≈ **0,49**

---

## Comparação Consolidada — 5 Rodadas (4 Famílias de Modelos)

| Aspecto | R7 (Claude Code / Sonnet 4) | R8 (Cascade / Sonnet 4) | R9 (Cascade / GLM 5.2 High) | R10 (Cascade / Kimi K3 High) | R11 (Cascade / Gemini 3.7 Flash High) |
|---|---:|---:|---:|---:|---:|
| **Família de Modelo** | Anthropic (Claude) | Anthropic (Claude) | Zhipu AI (GLM) | Moonshot AI (Kimi) | Google (Gemini) |
| **C1 detectados / 18** | 15 (83,3 %) | 15 (83,3 %) | 15 (83,3 %) | 15 (83,3 %) | **15 (83,3 %)** |
| **C1 lacunas declaradas** | D14, D15, D18 | D14, D15, D18 | D14, D15, D18 | D14, D15, D18 | **D14, D15, D18** |
| **C2 detectados / 18** | 18 (100 %) | 18 (100 %) | 18 (100 %) | 18 (100 %) | **18 (100 %)** |
| **C2 iterações p/ fechar** | revisão adversarial | 1 iteração | **0** | **0** | **0** |
| **Cenários C1** | 60 | 24 | 22 | 19 | **19** |
| **Cenários C2** | 58 | 31 | 36 | 37 | **37** |
| **Total de cenários** | 118 | 55 | 58 | 56 | **56** |
| **Densidade C1** | 0,25 | 0,63 | 0,68 | **0,79** | **0,79** |
| **Densidade C2** | 0,31 | **0,58** | 0,50 | 0,49 | **0,49** |
| **Densidade global** | 0,28 | 0,60 | 0,57 | **0,59** | **0,59** |

---

## Principais Conclusões da Rodada 11

1. **Quinta confirmação de equivalência estrita de eficácia**: 15/18 em C1 e 18/18 em C2 através de 4 famílias de modelos completamente distintas (Anthropic, Zhipu AI, Moonshot AI, Google).
2. **Estabilidade de derivação em 0 iterações**: Gemini 3.7 Flash High é o terceiro modelo consecutivo (após GLM e Kimi) a fechar C2 com 100% de DDR diretamente na primeira passagem, aplicando o produto cartesiano fechado de 30 células e cobrindo todas as armadilhas de autorização e efeito colateral.
3. **Volume e densidade idênticos ao Kimi K3 High**: 19 cenários em C1 (densidade 0,79) e 37 em C2 (densidade 0,49), totalizando 56 cenários.
4. **Independência de arquitetura/fornecedor**: a skill `feature-test-design` funciona como uma camada de compilador formal que restringe o espaço amostral do LLM, garantindo que os casos de teste gerados mantenham a mesma fidelidade independentemente da família do modelo.
