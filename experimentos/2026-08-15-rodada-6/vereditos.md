# Rodada 6 — vereditos dos juízes cegos

**Data**: 2026-08-15
**Versões medidas**: `feature-wiki` 3.0.0 · `feature-test-design` **1.8.0** · `feature-quality-gate` 1.1.0 · `requirement-to-rule` 1.2.0
**Projeto-cobaia**: **novo**, criado do zero com `composer create-project gsferro/starter-kit-easy` (Laravel 13.25 · Filament 5.6 · **Pest 5.1**, com as suítes `Kit`, `Tenancy` e `BrowserTenancy` que não existiam na cobaia anterior).
**Oráculo**: o mesmo `00-requisito.md` / `01-plano-acao.md` congelado desde o baseline.
**Recorte**: após a conclusão de cada braço, revisão adversarial incluída.

> Esta é a primeira rodada em que o **projeto por baixo mudou**. O oráculo é o mesmo, as skills são
> as novas, e o kit é outro — então ela também mede se as regras sobrevivem fora do projeto que as
> originou.

---

## Placar

| Métrica | Baseline | Rodada 5 (1.7.0) | **Rodada 6 (1.8.0)** |
|---|---|---|---|
| C1 · cupons — detectados de 18 | 7 (38,9%) | 14 (77,8%) | **16 (88,9%)** |
| C1 · lacunas cegas · declaradas | 10 · 1 | 2 · 2 | **0 · 2** |
| C1 · cenários | 22 | 51 | 58 |
| C2 · aprovação — detectados de 18 | 11 (61,1%) | 17 (94,4%) | **17 (94,4%)** |
| C2 · lacunas cegas · declaradas | 7 · 0 | 1 · 0 | **1 · 0** |
| C2 · células inválidas estado × evento | 9 de 21 | 17 de 21 | **21 de 21** |
| C2 · cenários | 27 | 63 | 49 |
| **Total** | **18 / 36 (50%)** | 31 / 36 (86,1%) | **33 / 36 (91,7%)** |
| Densidade (C1 · C2) | 0,32 · 0,41 | 0,27 · 0,27 | **0,28 · 0,35** |

**Zero lacunas cegas no cenário 1** — inédito. E o cenário 2 fechou a matriz inteira com **menos**
cenários que na rodada 5 (49 contra 63): a matriz cartesiana declarada substituiu volume por
cobertura dirigida.

## As quatro regras da 1.8.0, medidas

| Regra | Alvo | Resultado |
|---|---|---|
| **R1** — cenário por fora da UI | D09 · policy só no form (era lacuna **cega**) | ✅ morto por CT-17/18/19, um por verbo. No C2 pegou antes do juiz: a validação de domínio de R1 vivia só na página `create`, e a barreira do `gestor_id` só na tela |
| **R2** — premissa de mecanismo não apaga cenário | D15 · cupom excluído ainda aplicável (era lacuna **cega**) | ✅ morto por CT-26. No C2 forçou a escrever os análogos expressáveis (centro sem gestor, organização sem diretor) |
| **R3** — matriz cartesiana fechada com total declarado | E01 · aprovar em rascunho (era lacuna **cega**) e as 4 células ausentes | ✅ **21 de 21 células**, todas com recusa **e** âncora de não-efeito. Pegou 4 células "argumentadas e não executadas" e 3 falsos ✅ na v1 do próprio braço C1 |
| **R4** — cenário sem situação de partida é oráculo invertido | CT-22 da rodada 5 | ✅ barrou 4 cenários no C1 e 1 no C2. O juiz do C2 varreu explicitamente e não achou **nenhum** oráculo invertido |

**Bônus não previsto**: **D14 (fuso) morreu pela primeira vez em seis rodadas.** Era lacuna
declarada desde o baseline, com quatro tentativas de arnês registradas. O braço divergiu
`config(['app.timezone'])` e escolheu `01:30Z` — dentro da janela de 3 h — cumprindo a regra da
1.6.0 (*"o parâmetro livre é o instante, não o valor do formulário"*) somada à da 1.4.0
(*"o exemplo tem de ser discriminante"*).

---

## Cenário 1 — cupons · DDR 16/18 · 0 lacunas cegas

Detectados: D01, D02, D03, D04, D05, D06, D07, D08, **D09**, D10, D11, D13, **D14**, **D15**, D16, D17.

| Não detectado | Classe | Por quê |
|---|---|---|
| **D12** — validade no passado aceita na criação | **lacuna declarada** — e uma classe nova | O braço fixou a premissa **P-B** (*"cadastrar cupom já vencido é permitido"*) e escreveu o cenário **afirmando essa suposição**: `⚠️ @premissa P-B: o resultado esperado é ACEITO`. Na rodada 5 o braço assumiu o contrário e detectou |
| **D18** — mesmo cupom duas vezes | lacuna declarada (L-04) | o agregado `Pedido` está fora de escopo por P-01; o oráculo é inexpressável e ancorá-lo no contador provaria contabilidade, não idempotência |

> **Juiz cego, cenário 1**: *"a classe do requisito silencioso resolvido por premissa: onde o card
> não decide, o conjunto fixa uma suposição e escreve o cenário em cima dela. Quando a suposição
> coincide com o defeito, o cenário não só deixa passar o mutante, como ficaria **vermelho contra a
> implementação correta**. Nenhuma quantidade de BVA alcança esse defeito: ele mora na escolha do
> oráculo, não na escolha do valor."*

## Cenário 2 — aprovação · DDR 17/18 · 21 de 21 células

Detectados: E01…E17. **Nenhum oráculo invertido** encontrado na varredura dedicada.

| Não detectado | Classe | Por quê |
|---|---|---|
| **E18** — e-mail sai com a gravação da aprovação falhando | **lacuna cega (falso ✅)** | A coluna de não-efeito de notificação existe em `enviar` (CT-24) e nas recusas por falta de aprovador (CT-13, CT-35), mas **não** no `Esquema` de aprovação (CT-25) nem no da corrida (CT-40) — os dois únicos pontos onde uma aprovação que falha teria destinatário real. E CT-35 **não discrimina**: ali não existe diretor nenhum, então o mutante notificaria zero pessoas e o cenário ficaria verde igual |

> **Juiz cego, cenário 2**: *"os cenários que 'provam' atomicidade o fazem em configurações de zero
> destinatários, onde o mutante e a implementação correta produzem o mesmo observável."*

O conjunto marcava o item como coberto em dois lugares do texto (R8 e R6), o que o torna falso ✅.

---

## Critério de parada do protocolo

| Critério | Situação |
|---|---|
| DDR ≥ 0,85 em dois cenários distintos | ✅ 88,9% e 94,4% |
| `N_CT` não mais que dobrou em relação ao baseline | ❌ 58 e 49, contra 22 e 27 |
| O ciclo não produziu achado novo de melhoria | ❌ dois achados, um por cenário |

**Não fecha.** Segue para a rodada 7 com as regras abaixo.

## Melhorias derivadas — entram na 1.9.0 após revisão adversarial

1. **Premissa que decide o comportamento esperado não vira oráculo afirmativo.** A 1.8.0 tratou a
   premissa de **mecanismo**; falta a premissa de **comportamento** — a que decide se o sistema
   aceita ou recusa. Escrever o cenário afirmando a direção assumida produz um teste que fica
   **vermelho contra a implementação correta**, que é pior que não ter cenário.
2. **Não-efeito só discrimina se houver destinatário real.** Afirmar "nenhuma notificação foi
   enviada" numa configuração onde **não existe ninguém para notificar** é falso ✅ — o mutante e a
   implementação correta produzem o mesmo observável. É a irmã da regra já existente sobre
   `assertNothingSent()` em pré-validação.
3. **A coluna de não-efeito pertence a todas as operações que disparam o efeito**, não só às mais
   baratas de montar. A assimetria (notificação afirmada em `enviar`, ausente em `aprovar`) é o que
   deixou E18 vivo.
