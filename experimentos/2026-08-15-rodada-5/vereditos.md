# Rodada 5 — vereditos dos juízes cegos

**Data**: 2026-08-15
**Versões medidas**: `feature-wiki` 3.0.0 · `feature-test-design` 1.7.0 · `feature-quality-gate` 1.1.0 · `requirement-to-rule` 1.2.0
**Braços**: um por cenário, agentes independentes, sem contexto compartilhado, entrando no step 4 da `feature-wiki` sobre o oráculo fixo (`00-requisito.md` e `01-plano-acao.md` de `exp-a`, inalterados desde o baseline).
**Recorte**: tirado **após** a conclusão de cada braço, incluindo a revisão adversarial — a correção de protocolo da rodada 4.
**Conjuntos julgados**: `conjuntos/` nesta pasta.

---

## Placar

| Métrica | Baseline | Melhor rodada anterior | **Rodada 5** |
|---|---|---|---|
| C1 · cupons — detectados de 18 | 7 (38,9%) | 16 (88,9%) | **14 (77,8%)** |
| C1 · lacunas cegas · declaradas | 10 · 1 | 1 · 1 | **2 · 2** |
| C1 · cenários | 22 | 41 | **51** |
| C2 · aprovação — detectados de 18 | 11 (61,1%) | 17 (94,4%) | **17 (94,4%)** |
| C2 · lacunas cegas · declaradas | 7 · 0 | 1 · 0 | **1 · 0** |
| C2 · células inválidas estado × evento | 9 de 21 | 21 de 21 | **17 de 21** |
| C2 · cenários | 27 | — | **63** |
| **Total** | **18 / 36 (50%)** | **33 / 36 (91,7%)** | **31 / 36 (86,1%)** |

Densidade de detecção: 0,27 detectados por cenário nos dois cenários.

---

## Cenário 1 — FERRO-812 (cupons) · DDR 14/18

| ID | Defeito | Veredito |
|---|---|---|
| D01 | percentual > 100 aceito | DETECTA — `CT-05`, linha `percentual \| 101 \| recusado \| nenhum cupom existe` |
| D02 | total final negativo | DETECTA — `CT-26`, linha `5000 \| 3000 \| 0` |
| D03 | `<` vs `<=` na validade | DETECTA — `CT-21`, borda ao segundo (`10:00:00` e `10:00:01`) |
| D04 | `<` vs `<=` no limite | DETECTA — `CT-22`, linha `3 \| 10000 \| 3` |
| D05 | unicidade case-sensitive | DETECTA — `CT-10`, linhas `promo10` e `Promo10` |
| D06 | contador antes de validar | DETECTA — `CT-29` |
| D07 | contador não incrementado | DETECTA — `CT-28` |
| D08 | concorrência estoura o limite | DETECTA — `CT-30` |
| **D09** | **policy só no form; request direto passa** | **NÃO DETECTA — lacuna cega (falso ✅)** |
| D10 | usuário comum vê expirados | DETECTA — `CT-17`, células `CHEIO \| não` e `VENCIDO \| não` |
| D11 | valor 0 ou negativo | DETECTA — `CT-05`, nos dois ramos do discriminador |
| D12 | validade no passado na criação | DETECTA — `CT-07`, borda −1 min |
| D13 | auditoria sem autor / autor errado | DETECTA — `CT-32`, "o autor é Marina, e não Bruno" |
| D14 | validade em UTC × São Paulo | NÃO DETECTA — **lacuna declarada** (arnês; 3 tentativas registradas) |
| **D15** | **cupom excluído/desativado ainda aplicável** | **NÃO DETECTA — lacuna cega (falso ✅)** |
| D16 | percentual em `float` | DETECTA — `CT-25`, `29% de 10.000 → 7.100` |
| D17 | espaços nas bordas | DETECTA — `CT-10` e `CT-13` |
| D18 | mesmo cupom duas vezes | NÃO DETECTA — **lacuna declarada** (agregado `Pedido` fora de escopo) |

**Diagnóstico do juiz**: *"os dois erros não declarados têm a mesma assinatura: o conjunto testa
exaustivamente o **valor** e o **estado**, e assume o **mecanismo**."*

- **D09** — todo cenário de escrita (CT-14, CT-15, CT-16, CT-42, CT-B02) entra pelo componente
  Livewire/Filament. Nenhum alcança a escrita por fora da tela, então uma regra que vive só no
  formulário fica verde. O checklist marca "**Autorização exercida na ação**, não só consultada"
  como coberto.
- **D15** — o conjunto fixou "a exclusão é física" como premissa e, com isso, **eliminou por
  decisão** o cenário que revelaria soft delete. O checklist marca "**Estado × operação de
  escrita** (o inativo ainda funciona?)" como coberto e "Unicidade + exclusão lógica" como
  "não se aplica".

**Oráculos fracos apontados**: CT-37 (presença simples, subsumida), CT-25 linha `33/101` (o próprio
conjunto declara que não discrimina), CT-B01 passo 5 (`assertNoJavaScriptErrors` como apoio),
CT-B02 passo 5 (seletor não confirmado), CT-33 (não-efeito em pré-validação).

---

## Cenário 2 — FERRO-830 (aprovação) · DDR 17/18

| ID | Defeito | Veredito |
|---|---|---|
| **E01** | **aprovar solicitação em rascunho** | **NÃO DETECTA — lacuna cega (falso ✅)** |
| E02 | editar enviada | DETECTA — `CT-07`, afirma o valor gravado, não só a recusa |
| E03 | R$ 5.000,00 exatos | DETECTA — `CT-14`/`CT-15`, borda exata com limite injetado |
| E04 | diretor antes do gestor | DETECTA — `CT-16`/`CT-18`, estado + contagem de etapas |
| E05 | rejeição sem justificativa | DETECTA — `CT-25`, vazio ≠ espaços ≠ ausente, nas duas etapas |
| E06 | rejeitada mantém aprovações | DETECTA — `CT-26` |
| E07 | gestor de outro centro | DETECTA — `CT-18` + `CT-60` (centro não-primeiro, mata `::first()`) |
| E08 | solicitante aprova a própria | DETECTA — `CT-18`, linhas `solicitante \| aprovar` e `\| rejeitar` |
| E09 | cancelar após aprovada | DETECTA — `CT-33` + `CT-29` |
| E10 | e-mail ao aprovador errado / a cada save | DETECTA — `CT-49` (mundo fechado) + `CT-42` |
| E11 | sem aviso ao avançar para o diretor | DETECTA — `CT-41`, "exatamente dois avisos no total" |
| E12 | valor alterado não reavalia a alçada | DETECTA — `CT-27` |
| E13 | histórico não gravado/sobrescrito | DETECTA — `CT-17` + `CT-37`, oráculo pareado por bloco |
| E14 | excluir enviada | DETECTA — `CT-07`, o verbo irmão fechado |
| E15 | duplo clique avança duas etapas | DETECTA — `CT-19` + `CT-30` |
| E16 | tela mente o estado | DETECTA — `CT-35` + `CT-51`, enum exaustivo nas duas telas |
| E17 | valor zero ou negativo | DETECTA — `CT-04`, contagem de gravadas |
| E18 | e-mail fora da transação | DETECTA — `CT-43`, falha injetada **depois** do ponto de disparo |

**Células inválidas da matriz estado × evento: 17 de 21.** As 4 ausentes são o mesmo par de verbos
(`aprovar`/`rejeitar`) nos dois estados sem etapa pendente (`rascunho`, `cancelada`) — a mesma raiz
do único defeito não detectado.

**Diagnóstico do juiz**: *"as matrizes deste conjunto são organizadas por **regra de negócio**
(R2: editar/excluir; R3: enviar; R7: o terminal; R8: cancelar; R5: quem decide a etapa
**corrente**), nunca como produto cartesiano estado × evento fechado. […] é um buraco de
**enquadramento**, não de rigor: o mesmo conjunto que fecha 10 células de `papel × verbo` e afirma
o não-efeito em cada uma nunca se perguntou o que acontece se alguém apertar 'Aprovar' antes do
envio. […] o conjunto investiu quase todo o orçamento no eixo **ator**."*

**Agravante**: `CT-22` não declara a situação de partida e, materializado ao pé da letra, **afirma
como correto** o comportamento do defeito E01 — é o inverso de um oráculo. O próprio índice do
conjunto o marca com "Mata: —".

**Oráculo fraco adicional**: CT-62 (`assertOk` puro).

---

## O que as regras não medidas entregaram

| Regra | Alvo | Resultado na rodada 5 |
|---|---|---|
| 1.4.0 — o exemplo tem de ser discriminante | D16 (precisão monetária), que era **falso ✅** na 3ª medição | ✅ morto por `29% de 10.000 → 7.100` |
| 1.6.0 — cegueira de dimensão / fechar lacuna declarada sem discriminar é piorar | D14 (fuso), que **regrediu para cega** na 4ª rodada | ✅ de volta a **lacuna declarada**, com as tentativas de arnês registradas |
| 1.7.0 — dimensão fixa na matriz | E12 (valor alterado após envio sem reavaliar alçada), que sobrou na 4ª rodada | ✅ morto por `CT-27` |
| 1.5.0 — criação ≠ edição ≠ uso | ramo `valor_fixo` sem gravação pela tela | ✅ achado pela **revisão adversarial** do próprio braço, antes do juiz |

Cada regra matou o defeito que a originou. **Nenhuma delas endereça as três lacunas cegas novas.**

## O achado da rodada — deslocamento de orçamento

As três lacunas cegas (D09, D15, E01) vieram de **dois juízes independentes, em dois cenários
diferentes**, e receberam a mesma leitura: o conjunto gasta o orçamento nos eixos **valor** e
**ator**, e assume o eixo **mecanismo/estado**.

- **D09** — a regra da *camada mais barata* empurra todo cenário de escrita para o componente
  Livewire/Filament. Um teste de componente **não consegue**, por construção, distinguir uma regra
  que vive no formulário de uma que vive abaixo dele. Fechar a autorização por papel × verbo na
  tela e nunca por fora dela deixa a autorização vertical intacta.
- **D15** — premissa sobre **mecanismo** ("a exclusão é física") apagou o cenário em vez de
  escolher qual cenário escrever.
- **E01** — a matriz estado × evento foi **decomposta por regra de negócio** em vez de
  materializada como produto cartesiano fechado. Os verbos `aprovar`/`rejeitar` só existem em
  cenários que já pressupõem etapa pendente.

**Ressalva honesta**: um braço por cenário, um juiz por cenário. A queda de 16 → 14 em C1 está
dentro do que a variância explicaria sozinha. O que **não** é variância é as três lacunas terem a
mesma assinatura estrutural, nomeada de forma independente pelos dois juízes — e ela é acionável
como regra.

## Candidatos a regra da próxima versão

1. **Toda regra de autorização e de validação precisa de pelo menos um cenário que exercite a
   escrita por fora do componente de UI** (model/service/rota direta). Teste de componente não
   falsifica "a regra vive só no form".
2. **Premissa sobre mecanismo escolhe qual cenário escrever, nunca se ele existe.** Fixar "a
   exclusão é física" não elimina a pergunta "o registro removido ainda funciona?" — ela vira
   cenário no mecanismo assumido, mais lacuna declarada no outro.
3. **A matriz estado × evento é um produto cartesiano fechado, materializado em uma tabela só.**
   Decompô-la por regra de negócio deixa fora justamente as células cujo evento não tem "estado
   dono" — e é a classe de defeito mais barata de plantar.
4. **Cenário sem situação de partida declarada é oráculo invertido**, não oráculo fraco (`CT-22`):
   materializado, ele **certifica** o defeito. Deveria ser barrado no gate de falsificabilidade.
