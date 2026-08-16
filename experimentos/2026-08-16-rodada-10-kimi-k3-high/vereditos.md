# Vereditos — Rodada 10 (Cascade, Kimi K3 High, demo-r8, exp-r10)

- Data: 2026-08-16
- Modelo: Kimi K3 High
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r10\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 10 **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários). C1 carrega as mesmas três lacunas declaradas de arnês/mecanismo das rodadas anteriores. C2 fechou 100 % na primeira passagem, com a matriz estado × operação completa (30 células) e cobertura explícita das células que exigiram iteração na Rodada 8.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-05` — "porcentagem / 101 → recusado"; `CT-06` — "edita para porcentagem/101 → recusado, permanece 10" | Teto de 100% na criação e na edição. |
| D02 | **DETECTA** | `CT-13` — "fixo 5000 sobre total 3000 → desconto exatamente 3000, valor devolvido exatamente 0" | Piso de zero com oráculo exato. |
| D03 | **DETECTA** | `CT-07` — "2026-08-15 11:59:59 → recusado; 12:00:00 → recusado; 12:00:01 → aceito" | BVA 3-valores no segundo exato da fronteira. |
| D04 | **DETECTA** | `CT-12` — "CHEIO válido usos 3 de 3 → recusado, contador fica 3, trilha 0" | Limite respeitado na borda exata. |
| D05 | **DETECTA** | `CT-01` — " promo10  → gravado como PROMO10"; `CT-02` — "promo10 contra PROMO10 existente → falha, Acme continua com 1" | Caixa normalizada e unicidade case-insensitive. |
| D06 | **DETECTA** | `CT-12` — "VENCIDO → recusado, contador 0, trilha 0"; "CHEIO → recusado, contador 3, trilha 0" | Inválido não consome uso nem gera trilha. |
| D07 | **DETECTA** | `CT-14` — "contador de usos é 2, trilha tem 1 linha" | Sucesso incrementa contador. |
| D08 | **DETECTA** | `CT-15` — "duas simultâneas no último uso → uma aceita, outra recusada, contador 3, trilha 1 linha" | Disputa atômica. |
| D09 | **DETECTA** | `CT-10` — "panel_user executa criar/editar/excluir **sem passar pelo formulário** → recusado" | Autorização exercitada fora da UI. |
| D10 | **DETECTA** | `CT-11` — "lista contém somente ATIVO; VENCIDO não aparece; CHEIO não aparece"; `CT-B03` na tela | Escopo de leitura. |
| D11 | **DETECTA** | `CT-05` — "porcentagem 0 → recusado; fixo 0 → recusado"; `CT-06` — "edição fixo 0 → recusado" | Zero recusado nos dois tipos. |
| D12 | **DETECTA** | `CT-07` — passado recusado na criação; `CT-08` — "edita para 2026-01-01 → falha, permanece 2026-12-31" | Validade futura na criação e edição. |
| D13 | **DETECTA** | `CT-14` — "trilha tem 1 linha atribuída a Marina, datada de 2026-08-15 14:30:00, com valor original 10.000 e desconto 1.000" | Quem, quando e quanto gravados. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-01** — arnês não troca o fuso do app entre cenários. | Oráculo de fuso infalsificável no arnês. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-02** — mecanismo é exclusão física; "ativo" é estado derivado (P-03). | Fora do mecanismo assumido. |
| D16 | **DETECTA** | `CT-13` — "29% de 10.000 = exatamente 2.900"; "5% de 50 = exatamente 2"; "50% de 9.999 = exatamente 4.999" | Discriminantes de float/truncamento com a palavra "exatamente". |
| D17 | **DETECTA** | `CT-01` — " promo10  → PROMO10; variantes não existem no banco" | Espaços nas bordas normalizados. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-03** — agregado `Pedido` fora de escopo (P-01). | Inexpressável no arnês. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 15 no `04` + 4 no `05` = **19**
- **Densidade**: 15 detectados / 19 ≈ **0,79**

### Caracterização da técnica (C1)

Conjunto derivado de **BVA 3-valores, partição de equivalência, tabela de decisão, normalização, matriz papel × ação e concorrência**. É o conjunto de C1 mais enxuto das quatro rodadas (19 cenários) e o de maior densidade (0,79). Destaque para o uso sistemático da palavra "exatamente" nos oráculos monetários e para a não-ordenação implícita de efeitos no CT-12 (contador + trilha declarados por situação).

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-07` — "Rui tenta aprovar/rejeitar em rascunho → recusado, rascunho, histórico vazio" | Rascunho não aceita decisão. |
| E02 | **DETECTA** | `CT-09` — "editar em aguardando_gestor/diretor → recusado, valor gravado permanece 4.000,00, centro permanece TI, histórico preservado" | Edição em trânsito recusada com oráculo de valor persistido. |
| E03 | **DETECTA** | `CT-08` — "4.999,99 → aprovada; 5.000,00 → aprovada; 5.000,01 → aguardando_diretor" | BVA 3-valores na fronteira; `>` estrito conforme A-04. |
| E04 | **DETECTA** | `CT-20` — "Dora tenta aprovar em aguardando_gestor → recusado, histórico vazio" | Ordem das etapas. |
| E05 | **DETECTA** | `CT-12` — "rejeitar com justificativa \"\" recusado nas duas etapas, histórico não ganha etapa"; `CT-B04` na UI | Justificativa obrigatória em gestor e diretor. |
| E06 | **DETECTA** | `CT-14` — "etapa do gestor intacta após rejeição do diretor"; `CT-15` — "reenvio → aguardando_gestor, 2 etapas do ciclo anterior continuam, nenhuma etapa nova pelo envio" | Reset sem apagar histórico. |
| E07 | **DETECTA** | `CT-21` — "Carla, gestora do RH, tenta aprovar TI → recusado"; `CT-27` — "troca de centro recusada, Carla continua recusada, Rui continua aceito" | Autorização horizontal. |
| E08 | **DETECTA** | `CT-22` — "Ana sem papel de gestor tenta aprovar → recusado"; `CT-23` — "Ana gestora do próprio centro aprova 6.000 → aguardando_diretor, **não aprovada**, etapa gestor/aprovada/Ana" | Segregação coberta nos dois lados da premissa A-09. |
| E09 | **DETECTA** | `CT-17` — "cancelar aprovada → recusado, situação permanece aprovada"; `CT-16` — cancelar em trânsito aceito | Cancelar só antes da aprovação final. |
| E10 | **DETECTA** | `CT-03` — "edição em rascunho: nenhuma notificação"; `CT-18` — "Dora e Eva recebem; Rui não; Ana não"; `CT-26` — "rejeição: nenhuma notificação — nem Ana, nem Dora, nem Rui" | Destinatário único e sem e-mail a cada save. |
| E11 | **DETECTA** | `CT-18` — "avanço ao diretor notifica Dora e Eva"; `CT-11`/`CT-19` — "aprovação final: nenhuma notificação" | Notificação exatamente quando há próxima etapa. |
| E12 | **DETECTA** | `CT-09` — "editar valor em trânsito recusado, valor gravado permanece 4.000,00"; `CT-27` — "troca de centro recusada, aprovador da vez inalterado" | Campo decisivo congelado em trânsito. |
| E13 | **DETECTA** | `CT-19` — "histórico 2 etapas: gestor/aprovada/Rui e diretor/aprovada/Dora, cada uma com carimbo"; `CT-30` — "visualização exibe Gestor/Aprovada/Rui/data-hora e Diretor/Aprovada/Dora/data-hora" | Histórico gravado e exibido. |
| E14 | **DETECTA** | `CT-09` — "excluir em aguardando_gestor e aguardando_diretor → recusado, histórico preservado" | Exclusão em trânsito recusada. |
| E15 | **DETECTA** | `CT-24` — "duas simultâneas de Rui → uma aceita, outra recusada, 1 etapa"; `CT-25` — "Dora e Eva simultâneas → 1 etapa de diretor" | Idempotência sob disputa nas duas etapas. |
| E16 | **DETECTA** | `CT-29` — "5 situações → 5 rótulos distintos"; `CT-B01` — badges na listagem | Tela reflete estado real. |
| E17 | **DETECTA** | `CT-01` — "-0,01 e 0,00 recusados; 0,01 aceito" | BVA na fronteira inferior. |
| E18 | **DETECTA** | `CT-28` — "gravação falha depois do ponto de notificação → aguardando_gestor, histórico sem etapa, **Dora não recebe notificação**" | Destinatário real nomeado no Dado e no Então. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 32 no `04` + 5 no `05` = **37**
- **Densidade**: 18 detectados / 37 ≈ **0,49**

### Caracterização da técnica (C2)

Conjunto usa **máquina de estados (matriz 5×6 = 30 células declaradas), BVA 3-valores, 2-switch, rastreio de efeito, concorrência nas duas etapas e partição exaustiva do enum**. Fechou 100 % na primeira passagem. Dois diferenciais em relação às rodadas anteriores: (1) cobriu E10 também pelo lado do "e-mail a cada save" com CT-03 (edição em rascunho sem notificação); (2) derivou corretamente a premissa A-09 (solicitante-gestora permitida) com CT-23 afirmando o destino `aguardando_diretor` — não `aprovada` — e CT-22 recusando a solicitante sem papel de gestor, cobrindo E08 nos dois lados da fronteira.

---

## Comparação com Rodadas 7, 8 e 9

| Aspecto | R7 (Claude Code) | R8 (Cascade/Sonnet 4) | R9 (Cascade/GLM 5.2 High) | R10 (Cascade/Kimi K3 High) |
|---|---:|---:|---:|---:|
| C1 detectados / 18 | 15 (83,3 %) | 15 (83,3 %) | 15 (83,3 %) | 15 (83,3 %) |
| C1 lacunas declaradas | D14, D15, D18 | D14, D15, D18 | D14, D15, D18 | D14, D15, D18 |
| C2 detectados / 18 | 18 (100 %) | 18 (100 %) | 18 (100 %) | 18 (100 %) |
| C2 iterações para fechar | revisão adversarial | 1 iteração (CT-25/26) | 0 | 0 |
| Cenários C1 | 60 | 24 | 22 | **19** |
| Cenários C2 | 58 | 31 | 36 | 37 |
| Densidade C1 | 0,25 | 0,63 | 0,68 | **0,79** |
| Densidade C2 | 0,31 | 0,58 | 0,50 | 0,49 |
| Total de cenários | 118 | 55 | 58 | 56 |

### Diferenças de detecção

- **Placar idêntico nas quatro rodadas**: 15/18 em C1 e 18/18 em C2. Nenhum defeito do catálogo distingue os quatro modelos.
- **C1**: as três lacunas (D14, D15, D18) repetem-se pela quarta vez — são débitos de arnês, não de modelo.
- **C2**: R9 e R10 fecharam sem iteração; R7 e R8 precisaram de revisão. A regra do produto cartesiano fechado já está internalizada nos dois modelos mais recentes.

### Gaps, oráculos fracos e falsos ✅

- **Gaps**: idênticos aos das rodadas anteriores (arnês).
- **Oráculos fracos**: nenhum.
- **Falsos ✅**: nenhum.

### Destaques do conjunto Kimi K3 High

1. **C1 é o conjunto mais enxuto e mais denso da série** (19 cenários, 0,79) — 3 a menos que R9 mantendo o mesmo placar.
2. **C2 fechou 100 % sem iteração** e com dois acréscimos técnicos inéditos: CT-03 (edição em rascunho sem e-mail — cobre o braço "a cada save" de E10) e CT-23/CT-22 (dois lados da fronteira de A-09 para E08).
3. **Fidelidade ao oráculo**: a Rodada 9 recusava a solicitante-gestora (contrariando A-09); a Rodada 10 derivou A-09 corretamente — permitida quando gestora do próprio centro, recusada quando não — sem perder a detecção de E08.
4. **C2 ligeiramente maior** (37 cenários) porque cobre ambos os lados de A-09 e a ausência de e-mail em edição — cenários que matam mutantes, não redundância.

---

## Impressões gerais

1. **C1 em 83,3 % pela quarta vez consecutiva**, com as mesmas três lacunas declaradas. A convergência é total: nenhum modelo novo muda o placar, o que confirma que o teto é do arnês.

2. **C2 em 100 % sem iteração pela segunda vez consecutiva** (R9 e R10). A skill 1.9.0 estabilizou: modelos de famílias diferentes (GLM, Kimi) executam o pipeline sem precisar de revisão adversarial.

3. **A qualidade dos insumos é suficiente para modelos de famílias distintas**: o oráculo fixo (00 + 01) + a skill produzem conjuntos equivalentes em eficácia em Claude Sonnet 4, GLM 5.2 High e Kimi K3 High. Isso sustenta a hipótese do workflow proposto: wiki/CTs gerados por modelo forte podem guiar implementação por modelos mais leves.

4. **Recomendação mantida**: D14, D15 e D18 são débitos de arnês. Para fechar C1, o projeto-cobaia precisa de (a) agregado `Pedido`, (b) exclusão lógica, (c) controle de fuso em teste.

5. **Próximos passos sugeridos**: rodar com Gemini para completar o mapa de famílias, e depois com um modelo leve/local para medir o piso da skill — se um modelo leve mantiver DDR alto, o workflow "wiki em modelo pago, implementação em modelo local/grátis" está validado.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
