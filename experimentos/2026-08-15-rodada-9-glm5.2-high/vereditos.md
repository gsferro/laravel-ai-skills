# Vereditos — Rodada 9 (Cascade, GLM 5.2 High, demo-r8, exp-r9)

- Data: 2026-08-15
- Modelo: GLM 5.2 High
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r9\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 9 **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários). C1 carrega três lacunas declaradas do arnês/mecanismo. C2 fechou 100 % com a matriz estado × operação completa cobrindo todas as 30 células.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-05` — "porcentagem / 101 → recusado"; `CT-17` — "edita valor para 101 → gravação falha" | Percentual acima de 100 recusado na criação e edição. |
| D02 | **DETECTA** | `CT-12` — "fixo / 5000 / total 3000 → desconto 3000, resultado 0" | Piso de zero quando desconto fixo supera o total. |
| D03 | **DETECTA** | `CT-06` — "2026-08-14 12:00:00 → recusado; 2026-08-15 12:00:00 → recusado; 2026-08-16 12:00:00 → aceito" | BVA 3-valores no timestamp de expiração. |
| D04 | **DETECTA** | `CT-11` — "CHEIO / usos = limite → recusado, contador 2" | Limite de usos respeitado no consumo. |
| D05 | **DETECTA** | `CT-01` — "promo10 → gravado como PROMO10; promo10 não existe no banco" | Case normalizado. |
| D06 | **DETECTA** | `CT-14` — "VENCIDO / usos 0 → recusado, contador permanece 0, não existe linha em cupom_usos" | Contador não avança para cupom inválido. |
| D07 | **DETECTA** | `CT-13` — "PROMO10 / limite 3 / usos 1 → contador é 2, existe 1 linha em cupom_usos" | Sucesso incrementa contador e trilha. |
| D08 | **DETECTA** | `CT-15` — "limite 3 / usos 2 / duas simultâneas → uma aceita, outra recusada, contador 3, 1 nova linha" | Disputa atômica pelo último uso. |
| D09 | **DETECTA** | `CT-09` — "panel_user / criar → recusado; panel_user / editar → recusado; panel_user / excluir → recusado" | Autorização exercitada fora do formulário. |
| D10 | **DETECTA** | `CT-10` — "só ATIVO aparece; VENCIDO e CHEIO não aparecem"; `CT-B03` repete na tela | Escopo de listagem filtra cupons ativos. |
| D11 | **DETECTA** | `CT-05` — "porcentagem / 0 → recusado; fixo / 0 → recusado" | Domínio do valor rejeita zero. |
| D12 | **DETECTA** | `CT-06` — "2026-08-14 12:00:00 → recusado"; `CT-07` — "edita expira_em para 2026-01-01 → gravação falha, mantém original" | Validade futura exigida na criação e edição. |
| D13 | **DETECTA** | `CT-13` — "existe 1 linha em cupom_usos com aplicado_por_id = Marina"; `CT-16` — "linha tem created_at = 2026-08-15 14:30:00, valor_original = 10.000 e valor_desconto = 1.000" | Quem aplicou e quando são gravados. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-02** — fuso UTC no arnês; nenhum CT altera timezone do app e confronta o banco. | Oráculo de fuso infalsificável sem arnês de timezone. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-03** — mecanismo é exclusão física; não existe coluna `ativo`/`deleted_at`. | Fora do mecanismo assumido. |
| D16 | **DETECTA** | `CT-12` — "P29 / 29% de 10.000 → desconto 2.900"; "P5 / 5% de 50 → desconto 2"; "P50 / 50% de 9.999 → desconto 4.999" | Números discriminantes para float vs. inteiro e truncamento. |
| D17 | **DETECTA** | `CT-01` — "promo10 com espaços nas bordas → gravado como PROMO10" | Espaços nas bordas normalizados. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-01** — agregado `Pedido` fora de escopo; idempotência no pedido não ancorável. | Declarado no `## Fronteira com o Plano`. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 18 no `04` + 4 no `05` = **22**
- **Densidade**: 15 detectados / 22 ≈ **0,68**

### Caracterização da técnica (C1)

O conjunto deriva de **BVA 3-valores, partição de equivalência, tabela de decisão, normalização, matriz papel × ação e concorrência**. As três lacunas declaradas são limites do arnês/escopo, não da técnica. O conjunto é menor que o da Rodada 8 (22 vs. 24) e mantém o mesmo placar.

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-06b` — "Rui tenta aprovar em rascunho → recusada, situação permanece rascunho, histórico vazio" | Rascunho não aceita aprovação. |
| E02 | **DETECTA** | `CT-08` — "editar valor em aguardando_gestor → recusada, valor gravado permanece 4.000,00"; `CT-08b` — "excluir em aguardando_gestor → recusada" | Editar/excluir em trânsito é recusado e campos gravados são oráculos. |
| E03 | **DETECTA** | `CT-07` — "4.999,99 → aprovada; 5.000,00 → aprovada; 5.000,01 → aguardando_diretor" | BVA 3-valores na fronteira exata do limite. |
| E04 | **DETECTA** | `CT-18` — "Dora tenta aprovar em aguardando_gestor → recusada, situação permanece aguardando_gestor" | Diretor não decide antes do gestor. |
| E05 | **DETECTA** | `CT-11` — "rejeitar com justificativa vazia → recusada, situação permanece aguardando_gestor, histórico vazio"; `CT-B04` repete na UI | Justificativa obrigatória. |
| E06 | **DETECTA** | `CT-12` — "rejeição → rascunho, histórico tem 1 etapa"; `CT-21` — "reenvio → aguardando_gestor, histórico do ciclo anterior sobrevive" | Rejeição volta ao rascunho e reenvio não apaga histórico. |
| E07 | **DETECTA** | `CT-19` — "Carla gestora do RH tenta aprovar TI → recusada"; `CT-27` — "trocar centro em trânsito mantém aprovador Rui" | Só o gestor do centro decide. |
| E08 | **DETECTA** | `CT-20` — "Ana é gestora do próprio centro e aprova → recusada"; `CT-B02` — solicitante não vê botões | Solicitante não aprova própria solicitação. |
| E09 | **DETECTA** | `CT-14` — "cancelar aprovada → recusada, situação permanece aprovada"; `CT-13` — "cancelar em aguardando_gestor → aceito" | Cancelar só antes da aprovação final. |
| E10 | **DETECTA** | `CT-24` — "Rui aprova 6.000 → Dora recebe, Rui não recebe, Ana não recebe"; `CT-10` — "aprovação final → nenhuma notificação" | E-mail vai só para o próximo aprovador. |
| E11 | **DETECTA** | `CT-15` — "gestor aprova 6.000 → aguardando_diretor, Dora recebe notificação"; `CT-25` — "diretor aprova → nenhuma notificação" | Notificação acontece exatamente quando há próxima etapa. |
| E12 | **DETECTA** | `CT-26` — "editar valor para 6.000 em trânsito → recusada, valor gravado permanece 4.000,00"; `CT-27` — troca de centro mantém Rui como aprovador | Alteração de campo decisivo em trânsito não reavalia fluxo. |
| E13 | **DETECTA** | `CT-16` — "histórico tem 2 etapas: gestor/aprovada e diretor/aprovada/Dora"; `CT-31` — "primeira etapa mostra gestor, aprovada, Rui, data/hora; segunda mostra diretor, aprovada, Dora, data/hora"; `CT-B05` repete na UI | Histórico de aprovação é gravado e exibido. |
| E14 | **DETECTA** | `CT-08b` — "excluir em aguardando_gestor → recusada"; `CT-29` — "excluir em aguardando_gestor e aguardando_diretor → recusada, situação e histórico preservados" | Excluir em trânsito é recusado. |
| E15 | **DETECTA** | `CT-22` — "duas aprovações simultâneas do gestor → uma recusada, histórico 1 etapa"; `CT-23` — "dois diretores simultâneos → uma recusada, histórico 1 etapa" | Concorrência não grava etapas duplicadas. |
| E16 | **DETECTA** | `CT-30` — "cada situação exibe rótulo distinto: Rascunho, Aguardando gestor, Aguardando diretor, Aprovada, Cancelada"; `CT-B01` — badges na listagem | Tela reflete estado real. |
| E17 | **DETECTA** | `CT-01` — "-0,01/0,00 recusado; 0,01 aceito" | BVA na fronteira inferior do valor. |
| E18 | **DETECTA** | `CT-28` — "aprovação falha depois da notificação → situação permanece aguardando_gestor, histórico vazio, nenhuma notificação entregue" | E-mail não sobrevive a gravação que falha. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 31 no `04` + 5 no `05` = **36**
- **Densidade**: 18 detectados / 36 ≈ **0,50**

### Caracterização da técnica (C2)

O conjunto usa **máquina de estados (matriz 5×6 = 30 células), BVA 3-valores, 2-switch, rastreio de efeito de notificação, concorrência e partição exaustiva do enum**. A matriz estado × operação é declarada com total de células e auditoria completa. O conjunto cobre desde o início as células `rascunho × aprovar` (CT-06b) e `aguardando_* × excluir` (CT-08b, CT-29), que a Rodada 8 precisou de uma iteração para adicionar.

---

## Comparação com Rodadas 7 e 8

| Aspecto | Rodada 7 (Claude Code) | Rodada 8 (Cascade) | Rodada 9 (GLM 5.2 High) |
|---|---|---|---|
| C1 detectados / 18 | 15 / 18 (83,3 %) | 15 / 18 (83,3 %) | 15 / 18 (83,3 %) |
| C1 lacunas declaradas | D14, D15, D18 | D14, D15, D18 | D14, D15, D18 |
| C1 lacunas cegas | 0 | 0 | 0 |
| C2 detectados / 18 | 18 / 18 (100 %) | 18 / 18 (100 %) | 18 / 18 (100 %) |
| C2 lacunas | 0 | 0 | 0 |
| Cenários C1 (`04` + `05`) | 60 | 24 | 22 |
| Cenários C2 (`04` + `05`) | 58 | 31 | 36 |
| Densidade C1 | 0,25 | 0,63 | 0,68 |
| Densidade C2 | 0,31 | 0,58 | 0,50 |

### Diferenças de detecção

- **Placar final idêntico nas três rodadas**: 15/18 em C1 e 18/18 em C2. Nenhum defeito do catálogo passa em um modelo e não no outro.
- **C1**: as mesmas três lacunas declaradas em todos (D14, D15, D18), todas de arnês/escopo.
- **C2**: a Rodada 7 fechou 100 % com revisão adversarial; a Rodada 8 precisou de uma iteração para adicionar CT-25/CT-26; a **Rodada 9 fechou 100 % sem iteração**, cobrindo desde o início as células `rascunho × aprovar` (CT-06b) e `aguardando_* × excluir` (CT-08b + CT-29).

### Gaps, oráculos fracos e falsos ✅

- **Gaps**: C1 continua 0,167 abaixo do critério de parada. Os gaps são os mesmos: fuso (D14), exclusão lógica (D15) e agregado `Pedido` (D18). Para fechar C1 é preciso evoluir o arnês, não a técnica de derivação.
- **Oráculos fracos**: nenhum identificado. Os conjuntos usam asserções de igualdade, não-efeito com destinatário real e valores discriminantes.
- **Falsos ✅**: nenhum identificado.

### Destaques do conjunto GLM 5.2 High

1. **C1 ainda mais enxuto** (22 vs. 24 na Rodada 8; 22 vs. 60 na Rodada 7) com **densidade maior** (0,68 vs. 0,63 vs. 0,25). O conjunto GLM 5.2 High alcança o mesmo placar com menos cenários, indicando poda mais agressiva de variações redundantes.
2. **C2 fechou 100 % sem iteração**. A Rodada 8 precisou de uma revisão adversarial para descobrir as células `rascunho × aprovar` e `aguardando_* × excluir`; a Rodada 9 cobriu ambas desde a primeira passagem, indicando que o modelo aplicou a regra do produto cartesiano fechado mais rigorosamente.
3. **C2 maior que a Rodada 8** (36 vs. 31 cenários), mas ainda muito menor que a Rodada 7 (58). A densidade é menor (0,50 vs. 0,58), indicando que o conjunto GLM 5.2 High priorizou fechamento completo da matriz sobre densidade.
4. **Browser**: 4 cenários em C1 e 5 em C2, mesmo padrão da Rodada 8 e mais que a Rodada 7 (2 em cada).
5. **Itens não cobertos em C1**: exatamente os mesmos três. Isso confirma que as lacunas são **propriedades do arnês**, não do agente ou do modelo.

---

## Impressões gerais

1. **C1 está em 83,3 %** — mesmo patamar das Rodadas 7 e 8. As três lacunas declaradas (D14, D15, D18) são limites de arnês/escopo, não regressões de técnica.

2. **C2 fechou em 100 %** — alcançado sem iteração, com a matriz estado × operação completa desde a primeira passagem. O GLM 5.2 High aplicou a regra do produto cartesiano fechado mais rigorosamente que a Rodada 8.

3. **O GLM 5.2 High derivou um conjunto estruturalmente equivalente**, com o mesmo placar das rodadas anteriores. Em C1 foi mais enxuto (maior densidade); em C2 foi mais completo (menor densidade, mas sem lacunas).

4. **Risco para o critério de parada**: C1 ainda precisa de `DDR >= 0,85`. Como as três lacunas são de arnês/escopo, o critério depende de aceitar as lacunas declaradas como inevitáveis ou de evoluir o projeto-cobaia.

5. **Recomendação**: registrar D14, D15 e D18 como **débitos de arnês**. Se o experimento quiser fechar C1, o projeto-cobaia precisaria de: (a) agregado `Pedido`; (b) mecanismo de exclusão lógica; (c) controle de fuso aplicável em teste.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
