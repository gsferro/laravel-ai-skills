# Vereditos — Rodada 7 (demo-r7, exp-r7)

- Data: 2026-08-15
- Project-cobaia: `D:\PROJECTS\SKILLS\demo-r7`
- Conjuntos: `wikis/specs/exp-r7/{cupons-de-desconto,aprovacao-de-compra}/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`
- Versões medidas: `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0
- Juiz cego: `PROMPT-JUIZ-CEGO.md`

---

## Placar resumido

| Cenário | Detectados / 18 | DDR |
|---|---:|---:|
| C1 — Cupons de desconto | **15 / 18** | 83,3 % |
| C2 — Aprovação de solicitação de compra | **18 / 18** | 100 % |

A Rodada 7 **não fecha o critério de parada** do protocolo para C1 (`DDR >= 0,85` em ambos os cenários, sem achado novo de melhoria). C1 ainda carrega três lacunas declaradas do arnês/mecanismo.

---

## Cenário 1 — Cupons de desconto (FERRO-812)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| D01 | **DETECTA** | `CT-56` — “Então a gravação falha / E a Acme continua com exatamente 1 cupom” (por fora da tela); `CT-08` — “Então o total devolvido é 0 centavos” | O percentual 150 % é barrado na criação e, se existir no banco, o desconto é limitado ao total. |
| D02 | **DETECTA** | `CT-34` — “Então o total devolvido é 0 centavos / E o desconto registrado na trilha é exatamente 3.000 centavos” | Afirma o piso de zero para desconto fixo maior que o total. |
| D03 | **DETECTA** | `CT-27` — “Então `<resultado>`” com exemplos de validade na borda exata (15/08/2026 11:59:59, 12:00:00 e 12:00:01) | BVA 3-valores no instante de validade. |
| D04 | **DETECTA** | `CT-30` — “Então `<resultado>`” com exemplos de limite 1, 2 e 3 usos; `CT-31` — “E o contador de usos do cupom é 1” | A borda do limite é testada e a disputa do último uso força a contagem exata. |
| D05 | **DETECTA** | `CT-24` — “Então `<resultado>`” com linhas vazio, só espaços e `promo10`; `CT-13` — “Então a gravação é `<resultado>` / E o número de cupons da Acme é `<total>`” | A normalização de código (case/acento/espaço) é exercitada na criação e na busca. |
| D06 | **DETECTA** | `CT-37` — “Então a aplicação é recusada / E o contador de usos do cupom continua `<usos>` / E a trilha do cupom continua com `<usos>` linhas” | Cupom inválido não pode consumir uso nem gerar trilha. |
| D07 | **DETECTA** | `CT-36` — “Então o contador de usos do cupom é 3 / E a trilha do cupom tem 3 linhas” | A aplicação bem-sucedida força o consumo exato de um uso. |
| D08 | **DETECTA** | `CT-31` — “Então a primeira aplicação devolve 7.100 centavos / E a segunda aplicação é recusada / E a trilha do cupom tem exatamente 1 linha” | A disputa pelo último uso falha se o limite não for respeitado atomicamente. |
| D09 | **DETECTA** | `CT-50` — “Então a ação é recusada / E o cupom `PROMO10` continua existindo”; `CT-18` — “Então a resposta é 403/404” | A autorização é exercitada na ação e por fora do componente. |
| D10 | **DETECTA** | `CT-20` — “Então o cupom `ATIVO` aparece na lista / E os cupons `VENCIDO`, `CHEIO` e `VENCIDO-E-CHEIO` `<visibilidade>` na lista / E a lista tem `<total>` registros” | O operador só vê os cupons ativos. |
| D11 | **DETECTA** | `CT-06` — exemplos com `porcentagem`/`fixo` 0, 1, 100, 101; `CT-07` — mesma fronteira na edição | O valor 0 e acima de 100 são recusados para ambos os tipos. |
| D12 | **DETECTA** | `CT-09` — exemplos 15/08/2026 11:59:59, 12:00:00, 12:00:01; `CT-57` — “Então a gravação falha” para validade no passado | A validade deve estar no futuro na criação e por fora da tela. |
| D13 | **DETECTA** | `CT-40` — “Então a trilha do cupom tem 1 linha, atribuída à Marina e datada de ...”; `CT-49` — “E essa linha está atribuída a `<atribuida>`” | O autor e o instante da aplicação são gravados, não o usuário autenticado. |
| D14 | **NÃO DETECTA** | **Lacuna declarada L-03** — `config('app.timezone')` é `UTC`; três tentativas de arnês relatadas como infalsificáveis neste setup (fuso do app × fuso de quem digita). | Nenhum cenário muda o fuso do app e confronta o banco. |
| D15 | **NÃO DETECTA** | **Lacuna declarada L-04** — “o cupom ‘removido’ continuar aplicável, no mecanismo de exclusão lógica” declarado fora do mecanismo assumido (exclusão física). | A premissa é exclusão física; não há cenário para soft-delete. |
| D16 | **DETECTA** | `CT-33` — “Então o total devolvido é `<final>` centavos / E o desconto registrado na trilha é `<desconto>` centavos” com 29/10000, 9999 e 50 | Números discriminantes para float, arredondamento e truncamento. |
| D17 | **DETECTA** | `CT-13`, `CT-51`, `CT-53` — todos cobrem `trim` e normalização; `CT-24` linha vazio/só espaços | Código com espaços nas bordas é normalizado. |
| D18 | **NÃO DETECTA** | **Lacuna declarada L-05** — idempotência no agregado `Pedido` declarada inexpressável, pois o pedido está fora de escopo. | Não existe cenário que reaplique o mesmo cupom ao mesmo pedido. |

### Métricas C1

- **DDR**: 15 / 18 = **83,3 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 3 (D14, D15, D18)
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado; o conjunto evoluiu para asserções de igualdade e de não-efeito com destinatário real.
- **Total de cenários**: 58 no `04` + 2 no `05` = **60**
- **Densidade**: 15 detectados / 60 ≈ **0,25**

### Caracterização da técnica (C1)

O conjunto é derivado de **BVA 3-valores, partições de equivalência, matriz estado × operação e rastreio de efeito**, com uma revisão adversarial robusta. A classe estruturalmente fora do alcance é **timezone e mecanismos não assumidos** (soft-delete, idempotência externa, concorrência real entre processos), todas explicitamente declaradas como limites do arnês.

---

## Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

| ID | Veredito | Citação literal (CT + asserção) ou classe da lacuna | Justificativa |
|---|---|---|---|
| E01 | **DETECTA** | `CT-41` — “Então a operação é recusada / E a situação continua `rascunho`, o histórico continua com `<etapas>` etapa(s)” | Rascunho não aceita aprovar/rejeitar. |
| E02 | **DETECTA** | `CT-42` e `CT-43` — “Então a operação é recusada / E ... os três campos gravados continuam ...” | Em trânsito não se edita; o valor e centro gravados são os oráculos. |
| E03 | **DETECTA** | `CT-12` — “Então a solicitação fica em `<situacao>`” com 4.999,99 / 5.000,00 / 5.000,01 | BVA 3-valores na fronteira exata do limite. |
| E04 | **DETECTA** | `CT-13` — “Então a operação é recusada / E a solicitação continua em `aguardando gestor`” | Diretor não decide antes do gestor. |
| E05 | **DETECTA** | `CT-19` — “Então o resultado é `<resultado>`, a situação passa a ser `<situacao>` e o histórico ...”; `CT-48` (etapa irmã do diretor) | Justificativa obrigatória nas duas etapas. |
| E06 | **DETECTA** | `CT-21` — “Então a solicitação fica em `rascunho` / E o histórico tem uma etapa: gestor/Rui/rejeitada/...”; `CT-22` — “E o histórico continua com as duas etapas do ciclo anterior”; `CT-23` — “E o histórico tem três etapas” | Rejeição volta ao rascunho e o reenvio recomeça do gestor sem apagar histórico. |
| E07 | **DETECTA** | `CT-15` — “Então o resultado é `<resultado>`, a situação passa a ser `<situacao>` e o histórico ...” com Carla gestora de outro centro; `CT-53` troca de gestor após envio | Só o gestor do centro da solicitação decide; aprovador não é congelado. |
| E08 | **DETECTA** | `CT-17` — “Então a solicitação fica em `aguardando diretor`, e não em `aprovada` / E o histórico tem uma etapa: gestor/Ana/aprovada”; `CT-15`/`CT-16` rejeitam atores errados | A solicitante-gestora não pula a etapa do diretor. |
| E09 | **DETECTA** | `CT-44` — “Então a operação é recusada / E a situação continua `aprovada` ...” (linha cancelar); `CT-24` linha `aguardando diretor` × cancelar | Cancelar é recusado após aprovada e preserva o histórico. |
| E10 | **DETECTA** | `CT-28` — “Então o Rui recebe uma notificação ... pelo canal `mail` / E nem a Dora nem a Ana recebem notificação”; `CT-29` notificações por cardinalidade; `CT-30` não duplica e-mail | O e-mail vai só para o próximo aprovador e não se repete. |
| E11 | **DETECTA** | `CT-14` — “E ninguém é notificado — nem a Ana, nem o Rui, nem a Dora” (estado final); `CT-23` — “E a Dora recebe uma notificação por e-mail” (avanço para diretor) | O avanço para diretor notifica a Dora; a aprovação final não notifica ninguém. |
| E12 | **DETECTA** | `CT-42`/`CT-43` — “Então a operação é recusada / E ... os três campos gravados continuam ...” com `editar o valor para R$ 100,00`; `CT-46` — “E o centro gravado continua sendo `TI` ... e a Ana aprovando continua sendo recusada, enquanto o Rui aprovando é aceito” | Troca de campo decisivo em trânsito é recusada e o aprovador permanece o correto. |
| E13 | **DETECTA** | `CT-26` — “Então o histórico mostra três linhas, cada uma com o nome de quem decidiu ...”; `CT-27` — ordem com empate; `CT-52` — carimbo próprio da etapa | Histórico guarda quem, o quê, quando e por quê. |
| E14 | **DETECTA** | `CT-42`/`CT-43` — linha `excluir` recusada em trânsito; `CT-40` — “Então a solicitação deixa de existir / E as `<etapas>` etapa(s) dela também deixam de existir”; `CT-56` — “Então a operação é recusada / E nenhuma linha de solicitação é recriada” | Excluir em trânsito é recusado e a exclusão cascateia corretamente. |
| E15 | **DETECTA** | `CT-30` — “Então a segunda tentativa é recusada / E a solicitação persistida está em `aguardando diretor`, com exatamente uma etapa de gestor no histórico” | Decisão repetida não grava duas etapas. |
| E16 | **DETECTA** | `CT-25` — “Então a coluna de situação ... está com o estado `<estado>` / E o rótulo exibido ... não é vazio / E a coluna de situação está visível”; `CT-51` — rótulos distintos; `CT-14` — histórico confirma `aprovada` | Estado exibido é consistente com o estado real e os rótulos são distintos. |
| E17 | **DETECTA** | `CT-01` — linhas `-0,01`, `0,00` (recusado) e `0,01` (aceito); `CT-54` — “Então a solicitação fica em `aprovada` ... E o valor gravado é exatamente o mesmo número que foi comparado com o limite” | BVA na fronteira inferior e oráculo de valor persistido. |
| E18 | **DETECTA** | `CT-31` — “Então a operação falha / E a solicitação continua em `aguardando gestor`, o histórico continua vazio, e a Dora não recebe notificação” (com destinatário real e falha induzida depois do ponto do efeito) | O e-mail não sobrevive a uma gravação que falha. |

### Métricas C2

- **DDR**: 18 / 18 = **100 %**
- **Lacunas cegas**: 0
- **Lacunas declaradas**: 0
- **Falsos ✅**: nenhum identificado
- **Oráculos fracos**: nenhum identificado
- **Total de cenários**: 56 no `04` + 2 no `05` = **58**
- **Densidade**: 18 detectados / 58 ≈ **0,31**

### Caracterização da técnica (C2)

O conjunto usa **máquina de estados (matriz estado × operação em produto cartesiano fechado), BVA 3-valores, rastreio de efeito de notificação, 2-switch no ciclo de volta e cardinalidade de destinatário**. A revisão adversarial acrescentou 11 cenários (CT-46…CT-56) e fechou os três achados estruturais que mantinham E12, E15 e E18 vivos nas rodadas anteriores. Não restou lacuna declarada no catálogo.

---

## Impressões gerais

1. **C1 está em 83,3 %** — piora de 88,9 % na Rodada 6. Não é perda de capacidade: as três lacunas declaradas (D14, D15, D18) são **limites do arnês e do escopo**, não regressões. O conjunto continua muito denso e com poucos oráculos fracos, o que é positivo.

2. **C2 fechou em 100 %** — evolução clara sobre a Rodada 6 (94,4 %, onde E18 era cego). Os três achados que motivaram a 1.9.0 foram todos atendidos:
   - **CT-47** garante que rascunho reentrado é editável (E06/E14);
   - **CT-46** fecha a cadeia de troca de centro em trânsito (E12);
   - **CT-31** testa atomicidade da notificação com destinatário real (E18).

3. **A revisão adversarial é a diferença**. Os comentários do conjunto mostram um processo iterativo de correção de falsos ✅, `Então` fracos e suposições de mecanismo. Isso leva a CTs com **destinatário real** para não-efeito, **igualdade em vez de desigualdade** e **valores discriminantes**.

4. **Risco para o critério de parada**: C1 ainda precisa de `DDR >= 0,85`. Se as três lacunas forem aceitas como impossíveis de cobrir no arnês, o critério está tecnicamente satisfeito; caso contrário, a próxima rodada precisa de um arnês com fuso configurável, exclusão lógica e agregado `Pedido`.

5. **Recomendação**: registrar as lacunas D14, D15 e D18 como **débitos de arnês**, não de skill. Elas não são falhas da técnica de derivação, mas restrições do projeto-cobaia atual.

---

*Juiz cego concluído. Nenhuma alteração de código foi realizada.*
