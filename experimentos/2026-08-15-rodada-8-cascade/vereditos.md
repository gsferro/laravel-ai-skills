# Vereditos — Rodada 8 (Cascade, demo-r8, exp-r8)

- Data: 2026-08-15
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r8`
- Conjuntos: `D:\PROJECTS\SKILLS\demo-r8\wikis\specs\exp-r8\{cupons-de-desconto,aprovacao-de-compra}\04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 8 **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários). C1 carrega três lacunas declaradas do arnês/mecanismo. C2 fechou 100 % após adição dos CT-25 e CT-26 que cobrem as células `rascunho × aprovar` e `aguardando_* × excluir`.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-02b` — “porcentagem / 101 → a gravação falha”; `CT-19` — “edita tipo para porcentagem e valor 101 → gravação falha” | Percentual acima de 100 recusado na criação e edição. |
| D02 | **DETECTA** | `CT-12b` — “cupom fixo 5.000 / total 3.000 → total devolvido 0 e desconto 3.000” | Piso de zero quando desconto fixo supera o total. |
| D03 | **DETECTA** | `CT-04a/b/c` e `CT-08a/b/c` — exemplos no instante exato de validade | BVA 3-valores no timestamp de expiração. |
| D04 | **DETECTA** | `CT-09a/b/c` — “limite 3 / usos 2/3/4 → aceita/recusada/contador” | BVA 3-valores no limite de usos. |
| D05 | **DETECTA** | `CT-05` — “` promo10 ` → gravação falha, Acme continua com 1 `PROMO10`” | Case e espaços normalizados. |
| D06 | **DETECTA** | `CT-14` — “cupom expirado → recusada, contador continua 0, trilha vazia” | Contador não avança para cupom inválido. |
| D07 | **DETECTA** | `CT-13` — “aplicação bem-sucedida → contador 2, trilha tem 1 linha” | Sucesso incrementa contador e trilha. |
| D08 | **DETECTA** | `CT-15` — “duas requisições simultâneas → uma aceita, outra recusada, trilha 1 linha” | Disputa atômica pelo último uso. |
| D09 | **DETECTA** | `CT-16b/c/d/e` — “panel_user tenta criar/editar/excluir → 403” | Autorização exercitada fora do formulário. |
| D10 | **DETECTA** | `CT-17` — “panel_user lista → só `ATIVO` aparece, `VENCIDO` e `CHEIO` somem”; `CT-B03` repete na tela | Escopo de listagem filtra cupons ativos. |
| D11 | **DETECTA** | `CT-02a/c/d/e` — “valor 0 ou negativo para porcentagem e fixo → gravação falha” | Domínio do valor rejeita zero/negativo. |
| D12 | **DETECTA** | `CT-04a/b` — “expira_em no passado ou agora → gravação falha”; `CT-20` — edição para validade no passado recusada | Validade futura exigida na criação e edição. |
| D13 | **DETECTA** | `CT-13` — “trilha tem 1 linha atribuída à Marina e datada de ...” | Quem aplicou e quando são gravados. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-03** — fuso `UTC` no arnês; nenhum CT altera timezone do app e confronta o banco. | Oráculo de fuso infalsificável sem arnês de timezone. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-04** — mecanismo é exclusão física; não existe coluna `ativo`/`deleted_at`. | Fora do mecanismo assumido. |
| D16 | **DETECTA** | `CT-11b/c/e` — “29% de 10.000 → 7.100/2.900”; “5% de 50 → desconto 2”; “50% de 9.999 → 4.999” | Números discriminantes para float vs. inteiro e truncamento. |
| D17 | **DETECTA** | `CT-05` — “` promo10 ` normalizado e barrado” | Espaços nas bordas normalizados. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-05** — agregado `Pedido` fora de escopo; idempotência no pedido não ancorável. | Declarado no `## Fronteira com o Plano`. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 20 no `04` + 4 no `05` = **24**
- **Densidade**: 15 detectados / 24 ≈ **0,63**

### Caracterização da técnica (C1)

O conjunto deriva de **BVA 3-valores, partição de equivalência, tabela de decisão, rastreio de efeito, matriz papel × ação e concorrência**. As três lacunas declaradas são limites do arnês/escopo, não da técnica. A densidade é alta porque o conjunto é focado e não inflou com variações redundantes.

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-25` — “solicitação em rascunho → Rui tenta aprovar → recusada, situação continua rascunho, histórico vazio” | Rascunho não aceita aprovação. |
| E02 | **DETECTA** | `CT-21` — “editar valor em trânsito → recusada e valor gravado continua 4.000,00”; `CT-22` — “trocar centro em trânsito → recusada” | Editar/excluir em trânsito é recusado e campos gravados são oráculos. |
| E03 | **DETECTA** | `CT-04a/b/c` — “4.999,99 → aguardando_gestor; 5.000,00 → aguardando_gestor; 5.000,01 → aguardando_diretor” | BVA 3-valores na fronteira exata do limite. |
| E04 | **DETECTA** | `CT-07` — “Dora tenta aprovar antes de Rui → recusada e continua aguardando_gestor” | Diretor não decide antes do gestor. |
| E05 | **DETECTA** | `CT-09a` — “rejeitar com justificativa vazia → recusada”; `CT-B02` repete na UI | Justificativa obrigatória. |
| E06 | **DETECTA** | `CT-12` — “rejeição → rascunho, histórico com 1 etapa; reenvio → aguardando_gestor, histórico do ciclo anterior sobrevive” | Rejeição volta ao rascunho e reenvio não apaga histórico. |
| E07 | **DETECTA** | `CT-05` — “Carla gestora de outro centro tenta aprovar → recusada”; `CT-22` — “trocar centro em trânsito mantém aprovador Rui” | Só o gestor do centro decide. |
| E08 | **DETECTA** | `CT-06` — “Ana é gestora do próprio centro e aprova → aguardando_diretor (não aprovada)”; `CT-B03` — solicitante não vê botões de aprovação | Solicitante não aprova própria solicitação sem passar pelo fluxo. |
| E09 | **DETECTA** | `CT-14d` — “cancelar aprovada → recusada”; `CT-15/16` — cancelar em trânsito é aceito | Cancelar só antes da aprovação final. |
| E10 | **DETECTA** | `CT-10` — “Rui aprova R$ 6.000 → notificação para Dora, nenhuma para Rui/Ana”; `CT-11` — aprovação final não notifica | E-mail vai só para o próximo aprovador. |
| E11 | **DETECTA** | `CT-10` — avanço para diretor notifica Dora; `CT-11` — estado final não notifica | Notificação acontece exatamente quando há próxima etapa. |
| E12 | **DETECTA** | `CT-21` — “editar valor para 6.000 em trânsito → recusada e valor gravado continua 4.000,00”; `CT-22` — troca de centro mantém Rui como aprovador | Alteração de campo decisivo em trânsito não reavalia fluxo. |
| E13 | **DETECTA** | `CT-18` — “histórico mostra 4 etapas com quem, o quê, quando e justificativa”; `CT-B05” | Histórico de aprovação é gravado e exibido. |
| E14 | **DETECTA** | `CT-26a/b` — “Ana tenta excluir em aguardando_gestor e aguardando_diretor → recusada, situação e histórico preservados” | Excluir em trânsito é recusado. |
| E15 | **DETECTA** | `CT-19` — “duas aprovações simultâneas do gestor → uma recusada, histórico 1 etapa”; `CT-20` — mesmo para dois diretores | Concorrência não grava etapas duplicadas. |
| E16 | **DETECTA** | `CT-17` — “cada situação exibe rótulo distinto”; `CT-B01` — passo a passo com badges | Tela reflete estado real. |
| E17 | **DETECTA** | `CT-02a/b/c` — “-0,01/0,00 recusado; 0,01 aceito” | BVA na fronteira inferior do valor. |
| E18 | **DETECTA** | `CT-23` — “aprovação falha depois da notificação → solicitação continua aguardando_gestor, histórico vazio, nenhuma notificação entregue” | E-mail não sobrevive a gravação que falha. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 26 no `04` + 5 no `05` = **31**
- **Densidade**: 18 detectados / 31 ≈ **0,58**

### Caracterização da técnica (C2)

O conjunto usa **máquina de estados (matriz 5×6), BVA 3-valores, 2-switch, rastreio de efeito de notificação e concorrência**. O ciclo de revisão identificou duas lacunas iniciais (E01 e E14) e adicionou CT-25/CT-26, fechando o produto cartesiano. O conjunto final não deixa célula inválida sem execução.

---

## Comparação com Rodada 7 (Claude Code, demo-r7, exp-r7)

| Aspecto | Rodada 7 | Rodada 8 (Cascade) |
|---|---|---|
| C1 detectados / 18 | 15 / 18 (83,3 %) | 15 / 18 (83,3 %) |
| C1 lacunas declaradas | D14, D15, D18 | D14, D15, D18 |
| C1 lacunas cegas | 0 | 0 |
| C2 detectados / 18 | 18 / 18 (100 %) | 18 / 18 (100 %) |
| C2 lacunas | 0 | 0 |
| Cenários C1 (`04` + `05`) | 60 | 24 |
| Cenários C2 (`04` + `05`) | 58 | 31 |
| Densidade C1 | 0,25 | 0,63 |
| Densidade C2 | 0,31 | 0,58 |

### Diferenças de detecção

- **Placar final idêntico**: 15/18 em C1 e 18/18 em C2. Nenhum defeito do catálogo passa em um modelo e não no outro.
- **C1**: as mesmas três lacunas declaradas em ambos (D14, D15, D18), ambas de arnês/escopo.
- **C2**: a Rodada 7 fechou 100 % com revisão adversarial robusta; a Rodada 8 precisou de uma iteração para adicionar CT-25/CT-26 e cobrir as células `rascunho × aprovar` e `aguardando_* × excluir`.

### Gaps, oráculos fracos e falsos ✅

- **Gaps**: C1 continua 0,167 abaixo do critério de parada. Os gaps são os mesmos: fuso (D14), exclusão lógica (D15) e agregado `Pedido` (D18). Para fechar C1 é preciso evoluir o arnês, não a técnica de derivação.
- **Oráculos fracos**: nenhum identificado. Os conjuntos usam asserções de igualdade, não-efeito com destinatário real e valores discriminantes.
- **Falsos ✅**: nenhum identificado.

### Destaques do conjunto Cascade

1. **Conjunto muito menor** (24 vs. 60 em C1; 31 vs. 58 em C2) com **densidade maior** (0,63 vs. 0,25 em C1; 0,58 vs. 0,31 em C2). O conjunto do Cascade alcança o mesmo placar com menos cenários, indicando poda mais agressiva de variações redundantes.
2. **Browser**: mais cenários de superfície (4 em C1, 5 em C2) versus Rodada 7 (2 em cada). A Rodada 8 prioriza a camada de UI para D09/D10 (cupons) e E16 (aprovacão).
3. **Itens não cobertos em C1**: exatamente os mesmos três. Isso confirma que as lacunas são **propriedades do arnês**, não do agente.

---

## Impressões gerais

1. **C1 está em 83,3 %** — mesmo patamar da Rodada 7. As três lacunas declaradas (D14, D15, D18) são limites de arnês/escopo, não regressões de técnica.

2. **C2 fechou em 100 %** — alcançado após iteração para preencher o produto cartesiano. A revisão adversarial mostrou-se necessária para descobrir as células `rascunho × aprovar` e `aguardando_* × excluir`.

3. **O agente Cascade derivou um conjunto estruturalmente equivalente**, significativamente menor e mais denso. A eficiência é maior; a eficácia é a mesma.

4. **Risco para o critério de parada**: C1 ainda precisa de `DDR >= 0,85`. Como as três lacunas são de arnês/escopo, o critério depende de aceitar as lacunas declaradas como inevitáveis ou de evoluir o projeto-cobaia.

5. **Recomendação**: registrar D14, D15 e D18 como **débitos de arnês**. Se o experimento quiser fechar C1, o projeto-cobaia precisaria de: (a) agregado `Pedido`; (b) mecanismo de exclusão lógica; (c) controle de fuso aplicável em teste.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
