# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md` · Backend: `04-casos-de-teste.md`
> Runtime: `pest-plugin-browser` ^5.0 (Playwright). **O plugin sobe o próprio servidor** — HTTP
> in-process, porta aleatória. Nada de Herd, `artisan serve`, Sail ou `APP_URL`.
> Comando: `composer test:browser` (embute o `npm run build`) ou
> `vendor/bin/pest --testsuite=Browser` — **em série, nunca `--parallel`**.
> Suíte: `tests/BrowserTenancy/CupomTest.php` (`Tests\TenancyTestCase`, grupo `browser`).

---

## Gate do `05` — por que este arquivo existe, e por que só com dois cenários

A tabela `## Superfície de UI` do PRD tem **4 linhas, todas com `Depende de JS? = Sim`**. Isso é o
**gatilho**, não o critério. O critério é: *o cenário afirma sobre algo que **só o navegador
prova***.

Aplicado linha a linha:

| Linha da `## Superfície de UI` | O que precisaria ser provado | Só o navegador prova? | Onde ficou |
|---|---|---|---|
| `CuponsTable` — listagem, ordenação, busca, badge de situação | os registros certos aparecem para a persona certa | **não** — `assertCanSeeTableRecords` / `assertCanNotSeeTableRecords` | `04` → **CT-20, CT-21, CT-23** |
| `CupomForm` — criar | os campos gravam; a validação recusa | **não** — `fillForm` → `call('create')` → banco | `04` → **CT-01, CT-06, CT-09, CT-11, CT-13** |
| `CupomForm` — criar | **o rótulo do campo de valor muda quando o tipo muda, sem recarregar a página** | **SIM** | **CT-B01** |
| `CupomForm` — editar | os campos gravam; a fronteira vale no `save` | **não** | `04` → **CT-02, CT-07, CT-12, CT-14, CT-44** |
| `DeleteAction` na linha | a exclusão remove o cupom e a trilha | **não** — `callAction(TestAction::make('delete')->table($c))` | `04` → **CT-45** |
| `DeleteAction` na linha | **o clique em "Excluir" abre um modal e NÃO exclui antes da confirmação** | **SIM** | **CT-B02** |

**Duas linhas passam no critério; as outras quatro pertencem ao `04`** e já estão lá. Empurrar
validação, gravação, listagem e ação de tabela para o navegador é a decisão que mais destrói o
orçamento de teste de uma feature Filament — e nenhuma delas ficaria mais bem provada ali.

### Teto do perfil e o desvio declarado

O perfil `completo` prevê **1 happy path + 1 erro visível**. Os dois cenários escolhidos **não** são
"happy path + erro visível": são **os dois únicos cenários browser-only** desta feature. O desvio é
deliberado — o gate vence o teto, e gastar um dos dois slots num happy path que o componente já prova
seria pagar o instrumento mais caro da esteira por nada.

### Por que **não** há CT-B de cor, tema ou acessibilidade

O PRD desenha badges `success` / `warning` / `danger` para a situação. **Nenhuma cláusula `RQ`
determina cor.** Um CT-B de cor seria testar o PRD com o instrumento mais caro disponível — é a
pergunta **Q-05/Q-06** do `04`, não um caso de teste. Acessibilidade e tema escuro pertencem à tela
do kit, já cobertos por `tests/Browser/TemaEscuroTest.php` e `tests/Browser/TelasDoKitTest.php`; esta
feature não altera nem tema nem layout.

---

## Cogitado e cortado

Sem esta tabela, "só há 2 CT-B" é indistinguível de "só pensamos em 2".

| Cenário cogitado | Por que foi cortado |
|---|---|
| criar um cupom inteiro pela tela, do zero ao registro na listagem | já provado por CT-01 (gravação) + CT-20 (listagem), **mais barato** e sem Playwright |
| a validação de código duplicado mostra a mensagem na tela | mata o mesmo mutante que CT-13 e CT-51, que são teste de componente |
| a trilha órfã depois da exclusão | coberto por CT-46 no `04` (recriar o código não herda a trilha do excluído), mais barato. Aqui sobra só o que o navegador acrescenta: que o **primeiro clique não exclui** — CT-B02, passo 5 |
| o `maxValue` do campo de valor muda de 100 para "sem teto" ao escolher o tipo fixo | mata **o mesmo mutante** de CT-B01 (o `->live()` do `Select`); manter dois cenários para a mesma família de mutante é poda |
| as três telas de cupom sobem sem erro de JavaScript | `assertNoJavaScriptErrors()` **sozinho não é oráculo** — página em branco e 403 renderizado passam. Absorvido como asserção **de apoio** dentro de CT-B01 e CT-B02 |
| os badges de situação têm cores diferentes | a cor é escolha do PRD, não do requisito → pergunta Q-06, não cenário |
| o painel `/app` continua acessível depois de a feature entrar | regressão do kit, já coberta por `tests/Browser/TelasDoKitTest.php` |
| login pela tela antes de cada cenário | custa ~20 s por cenário; `$this->actingAs()` vale dentro do navegador porque o servidor roda **no mesmo processo** |

---

## Pré-requisitos

- [ ] `npm run build` executado — **pré-requisito duro**. Sem `public/build/manifest.json` toda tela
      responde `ViteException` e os dois cenários falham por um motivo que não é o deles.
      `composer test:browser` já embute o build.
- [ ] `tests/BrowserTenancy/` já existe e já está na testsuite `Browser` (`phpunit.xml:39`) —
      **nenhuma infra de teste nova**.
- [ ] `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach` — sem os
      dois, a tela responde 403 para todo mundo que não seja `master_global`.
- [ ] Autenticação por `$this->actingAs($usuario)` **antes** do `visit()` — nunca login pela tela.
- [ ] `pest()->browser()->timeout(20_000)` já configurado (`tests/Pest.php:170`). **Ao rodar este
      arquivo isolado com as views frias**, o primeiro cenário paga a compilação dos componentes
      Livewire sozinho (~25 s medidos) e falha **por tempo, não por comportamento** — subir o teto
      não resolve. Rodar a suíte inteira uma vez antes, ou rodar sempre `--testsuite=Browser`.
- [ ] `tests/Browser/Screenshots` no `.gitignore` — **nenhum destes cenários versiona screenshot**.
- [ ] `fronteiraDeRequest()` **não é necessária aqui**: os dois cenários ficam dentro do painel
      `/app`, e ela existe para a travessia entre painéis (`tests/Pest.php:321`).

## Seletores

O kit **não tem `data-testid`** — dívida conhecida, registrada em `.ai/rules/testes-browser.md`. O
disponível:

| Elemento | Seletor | Já existe? |
|---|---|---|
| campo Código | `#form\.codigo` (`id` gerado pelo Filament; o `.` precisa de escape em CSS) | sim, pelo padrão do kit |
| campo Tipo | `#form\.tipo` — e a classe `.fi-fo-select-native`. **Confirmado no vendor**: o `Select` do Filament 5 renderiza um `<select>` **nativo** quando não é `searchable`, nem `multiple`, nem `allowHtml` (`vendor/filament/forms/src/Components/Select.php:1838`) — que é exatamente o caso deste campo. Por isso a interação é `->select(...)`, e não o roteiro de um combobox JS | sim, pelo padrão do kit |
| campo Valor | `#form\.valor` | sim, pelo padrão do kit |
| campo Válido até | `#form\.expira_em` | sim, pelo padrão do kit |
| campo Limite de usos | `#form\.limite_de_usos` | sim, pelo padrão do kit |
| rótulo do campo Valor | **texto visível traduzido** — o rótulo é o que o cenário observa | ver **Q-04** do `04` |
| ação "Excluir" na linha | **texto visível traduzido** da `DeleteAction` | pt-BR do Filament |
| modal de confirmação | `.fi-modal` (classe do próprio Filament) | sim |

> **Confirmar os textos traduzidos no HTML real durante a implementação.** O kit já pagou este
> pedágio: o `<h1>` do dashboard é `Painel de Controle`, não `Dashboard`. Texto errado no CT-B produz
> vermelho **sem defeito no código**, que é a causa (a) do loop de execução.

> **Divergência declarada**: a `feature-test-design` afirma que `waitForText` não existe no plugin.
> Conferido em `vendor/pestphp/pest-plugin-browser/src/Api/`: **existe** (junto de `wait`,
> `waitForEvent`, `waitForKey` e `pressAndWaitFor`); `waitForSelector` e `waitUntil` **não**. A
> orientação de fundo continua valendo e é seguida: **nenhum cenário aqui usa espera por segundos
> fixos** — as asserções são reexecutadas até o teto de `timeout()`.

---

## CT-B01: o rótulo do campo de valor muda quando o tipo muda

**Por que browser e não Livewire**: o defeito é o `Select` de tipo **sem** `->live()`. Num teste de
componente, `fillForm(['tipo' => 'fixo'])` altera o estado e a leitura seguinte **força uma nova
renderização do schema** — a closure do rótulo é reavaliada e o teste fica **verde com o `->live()`
ausente**. No navegador, sem o `->live()` não há requisição ao servidor: o rótulo **continua dizendo
a unidade errada** enquanto a pessoa digita o valor. O registro sai **correto no banco e mentiroso na
tela**, e é o risco nº 1 da tabela `## Riscos` do PRD.

Esta é a única classe de defeito desta feature que **nenhum** teste HTTP ou de componente enxerga:
o HTML inicial é idêntico nos dois casos.

```gherkin
# language: pt
  Cenário: [CT-B01] o rótulo do campo de valor acompanha o tipo escolhido, sem recarregar a página
    Dado a administradora Helena autenticada no painel da organização Acme
    E o formulário de novo cupom aberto, com o tipo porcentagem pré-selecionado
    Quando ela escolhe o tipo "Valor fixo" e preenche o código, o valor, a validade e o limite
    Então o rótulo do campo de valor deixa de anunciar percentual e passa a anunciar centavos
    E, ao salvar, o cupom gravado é do tipo fixo com o valor exatamente como digitado
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir o formulário | `$this->actingAs($helena);`<br>`$pagina = visit('/app/acme/cupons/create');` | tela de criação |
| 2 | conferir o estado inicial | `->assertSee('{rótulo de percentual}')`<br>`->assertDontSee('{rótulo de centavos}')` | o rótulo do tipo pré-selecionado |
| 3 | **trocar o tipo** — a única ação do cenário | `->select('#form\\.tipo', 'fixo')` | o `Select` muda |
| 4 | **o oráculo browser-only** | `->assertSee('{rótulo de centavos}')`<br>`->assertDontSee('{rótulo de percentual}')` | o rótulo trocou **sem recarregar** — reexecutado até o teto de `timeout()`, sem `wait()` |
| 5 | preencher o resto | `->fill('#form\\.codigo', 'FIXO10')`<br>`->fill('#form\\.valor', '1000')`<br>`->fill('#form\\.expira_em', '30/09/2026 23:59')`<br>`->fill('#form\\.limite_de_usos', '5')` | |
| 6 | salvar e **esperar a navegação primeiro** | `->press('{rótulo de criar}')`<br>`->assertPathIs('/app/acme/cupons')` | volta à listagem |
| 7 | apoio | `->assertNoJavaScriptErrors()` | console limpo |
| 8 | **âncora de persistência** — o rótulo exibido corresponde ao que foi gravado | `$this->assertDatabaseHas('cupons', ['codigo' => 'FIXO10', 'tipo' => 'fixo', 'valor' => 1000]);` | o banco confirma a unidade que a tela anunciou |

**Assertions**: `assertPathIs` **antes** de qualquer asserção de conteúdo pós-navegação (passo 6) ·
`assertNoJavaScriptErrors()` como **apoio**, nunca como oráculo · a **âncora de persistência** do
passo 8 é o que liga o texto visível ao registro — sem ela, o cenário provaria que um texto muda, não
que a tela diz a verdade sobre o que grava.

> **`assertNoSmoke()` não é usado**: a tela é um painel Filament cheio de plugin de terceiro, e a
> suíte ficaria vermelha por `console.log` alheio (`.ai/rules/testes-browser.md`).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB1.1 | `Select` de tipo **sem `->live()`** — o rótulo só muda depois de salvar e reabrir | **CT-B01** (passo 4) |
| MB1.2 | o rótulo é fixo ("Valor") e nunca declara a unidade — a pessoa digita 10 querendo R$ 10,00 e grava 10% | **CT-B01** (passos 2 e 4) |
| MB1.3 | o rótulo muda, mas a gravação usa o tipo **anterior** (o `Get` lê estado obsoleto) | **CT-B01** (passo 8) |
| MB1.4 | a troca de tipo derruba o formulário com erro de JavaScript e a página fica inerte | **CT-B01** (passos 6 e 7) |

---

## CT-B02: excluir exige confirmação, e o cupom sobrevive ao primeiro clique

**Por que browser e não Livewire**: `callAction(TestAction::make('delete')->table($cupom))`
**executa a ação diretamente** — o modal de confirmação nunca entra no caminho. Um teste de
componente fica verde tanto com `DeleteAction` (que confirma por padrão) quanto com um
`Action::make('excluir')` cru que apaga no clique. A diferença só existe **no navegador**, e a
consequência é destrutiva e irreversível: a exclusão do cupom leva junto **toda a trilha de
`cupom_usos`** em cascata — a evidência de RQ-15 desaparece com um clique errado.

O requisito dá ao admin o direito de excluir (RQ-07). Não é uma barreira de autorização; é a última
coisa entre um clique acidental e a perda da trilha de auditoria.

```gherkin
# language: pt
  Cenário: [CT-B02] o cupom não é excluído antes da confirmação
    Dado a administradora Helena autenticada no painel da organização Acme
    E um cupom "PROMO10" já aplicado três vezes, com três linhas de trilha
    Quando ela aciona a exclusão desse cupom na listagem
    Então um pedido de confirmação aparece na tela
    E o cupom "PROMO10" e as três linhas de trilha dele continuam existindo
    E somente depois de ela confirmar é que o cupom e a trilha desaparecem
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir a listagem | `$this->actingAs($helena);`<br>`$pagina = visit('/app/acme/cupons');` | a lista com `PROMO10` |
| 2 | conferir a situação de partida | `->assertSee('PROMO10')` | o cupom está lá |
| 3 | **acionar a exclusão** — a única ação do cenário | `->click('{rótulo de excluir}')` | o modal deve abrir |
| 4 | **o oráculo browser-only, lado do elemento** | `->assertPresent('.fi-modal')` | o pedido de confirmação está na tela |
| 5 | **o oráculo browser-only, lado do dado** | `$this->assertDatabaseHas('cupons', ['codigo' => 'PROMO10']);`<br>`expect(CupomUso::count())->toBe(3);` | **nada foi excluído pelo primeiro clique** |
| 6 | confirmar | `->click('{rótulo de confirmação do modal}')`<br>`->assertMissing('.fi-modal')` | o modal fecha |
| 7 | **o efeito, e só agora** | `->assertDontSee('PROMO10')`<br>`$this->assertDatabaseMissing('cupons', ['codigo' => 'PROMO10']);`<br>`expect(CupomUso::count())->toBe(0);` | o cupom e a trilha se foram |
| 8 | apoio | `->assertNoJavaScriptErrors()` | console limpo |

**Assertions**: o passo 5 é o que separa este cenário de CT-45 do `04` — ele afirma o **não-efeito
num mundo com destinatário real** (o cupom existe **e** tem três linhas de trilha que o caminho feliz
apagaria). O passo 7 afirma o efeito, para que o cenário não passe com um botão que simplesmente não
funciona. Console é apoio.

> **"Recusada" aqui não é o mesmo que em CT-50 do `04`.** CT-50 exige **403** de propósito: com a
> barreira só em `->visible()`, um arnês de componente recusa a chamada *porque a ação está
> escondida*, e a asserção vaga ficaria verde. Este CT-B02 é o caso oposto — a ação **existe e é
> autorizada**, e o que se prova é que ela **não age antes da confirmação**. Os dois cenários usam
> verbos parecidos e provam coisas diferentes; o [vocabulário de recusa](04-casos-de-teste.md#vocabulário-de-recusa--forma-observável-fixada-para-cada-operação)
> do `04` é o que os mantém separados.

> **Um único `Quando`.** Os passos 6 e 7 são a continuação do mesmo comportamento — "exige
> confirmação" só é verificável mostrando as duas metades: **não excluiu antes** e **excluiu depois**.
> Um cenário que parasse no passo 5 ficaria verde com um botão quebrado.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB2.1 | `Action::make('excluir')` cru, sem confirmação — o clique apaga o cupom e a trilha | **CT-B02** (passos 4 e 5) |
| MB2.2 | o modal abre mas o botão de confirmação não dispara nada (erro de Alpine) | **CT-B02** (passos 6 e 7) |
| MB2.3 | a exclusão remove o cupom e **deixa a trilha órfã** | **CT-B02** (passo 7) |
| MB2.4 | a exclusão estoura por restrição de chave estrangeira no primeiro cupom já usado | **CT-B02** (passo 7) — e **CT-45** no `04` |

---

## Fatos do arnês que mudam o que se escreve aqui

Confirmados no projeto, não de memória:

1. **O plugin sobe o próprio servidor**, in-process, em porta aleatória (`tests/Pest.php:95-98`).
2. Como é o **mesmo processo**, valem dentro do navegador: `DB_DATABASE=:memory:`
   (`phpunit.xml:54`), `RefreshDatabase`, `$this->actingAs()` **antes** do `visit()`,
   `assertDatabaseHas` e as demais asserções do Laravel. Os passos 5, 7 e 8 dos roteiros dependem
   disso.
3. **`assertPathIs` antes das asserções de conteúdo**, depois de qualquer ação que navegue — é ela
   que espera a navegação. Invertido, o `assertSee` roda contra o snapshot da página anterior e falha
   **com a ação tendo funcionado**.
4. **Nunca `--parallel`**: medido no kit, derruba 4 de 11 cenários.
5. **`assertNoSmoke()` só em tela de autoria própria**; painel Filament usa
   `assertNoJavaScriptErrors()`.
6. **`assertSee` não valida tema nem cor** — passa com texto branco em fundo branco. Mais uma razão
   para não haver CT-B de cor aqui.
7. `visit([...])` em lote **aborta na primeira falha** — não é usado nestes dois cenários, que são
   uma URL cada.
8. **`assertNoJavaScriptErrors()` nunca é o oráculo único.** Nos dois cenários ele é a última linha,
   depois de uma asserção sobre o que o cenário afirma.

---

## Roteiro de Validação: Desenhado × Implementado

Preenchido no **step 7 da `feature-wiki`**, depois de rodar os CT-B contra a tela real. Divergência
vai para "Desvios do Plano" no `03-progresso.md`, **não** para uma correção do CT-B.

| # | O que o PRD desenhou (`## Superfície de UI`) | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | `CuponsTable` em `/app/{tenant}/cupons` — lista, ordena, busca por código, badge de situação | | ⬜ | |
| 2 | `CupomForm` criar em `/app/{tenant}/cupons/create` — cinco campos | | ⬜ | |
| 3 | `CupomForm` criar — **o campo de valor muda de rótulo com o tipo** | | ⬜ | CT-B01 |
| 4 | `CupomForm` editar em `/app/{tenant}/cupons/{record}/edit` | | ⬜ | |
| 5 | `DeleteAction` na linha — **com modal de confirmação** | | ⬜ | CT-B02 |
| 6 | `{record}` na URL é o **uuid**, não o id (`TemUuid::getRouteKeyName()`) | | ⬜ | |
| 7 | rótulos e mensagens em **pt-BR** (`wikis/convencoes.md` → Idioma) | | ⬜ | Q-04 |
| 8 | as ações de escrita **não aparecem** para o usuário comum | | ⬜ | CT-19 do `04` |

## Contrato do sub-agente que vai escrever estes CT-B

Conforme o loop da `feature-wiki` (step 7). Repetido aqui porque é onde ele será lido:

- Escrever `tests/BrowserTenancy/CupomTest.php` a partir de CT-B01 e CT-B02.
- Rodar `vendor/bin/pest --testsuite=Browser` — **nunca** com `--parallel`.
- Se falhar, **classificar a causa antes de mexer em qualquer coisa**:
  **(a)** CT-B especificado errado (seletor, rota, texto traduzido) → corrigir **este arquivo**;
  **(b)** implementação divergente do PRD → **não corrigir**; registrar a divergência;
  **(c)** flake de timing → rever a estratégia de espera pelo **estado final visível**, nunca com
  `wait()` de segundos fixos.
- Máximo de **3 iterações**. Vermelho por causa **(b)** é resultado válido — é exatamente a
  divergência que se queria capturar.
- **Proibido**: alterar código de aplicação para o teste passar, relaxar asserção, remover CT-B que
  não passou.

> Os seletores marcados `{rótulo …}` nos roteiros são a causa (a) mais provável. Resolvê-los é
> trabalho legítimo do sub-agente; **os oráculos dos passos 4, 5, 7 e 8 não são negociáveis**.
