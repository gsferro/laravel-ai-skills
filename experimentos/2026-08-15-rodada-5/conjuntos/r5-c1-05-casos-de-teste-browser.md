# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Casos de backend: `04-casos-de-teste.md`
> Runtime: `pest-plugin-browser` ^5.0 (Playwright). **O plugin sobe o próprio servidor** — HTTP
> in-process, porta aleatória. Nada de Herd, `artisan serve`, Sail ou `APP_URL`.
> Comando: `composer test:browser` (que embute o `npm run build`) ou
> `vendor/bin/pest --testsuite=Browser` — **em série, nunca `--parallel`**
> (`.ai/rules/testes-browser.md`: medido, `--parallel` derruba 4 dos 11 cenários).

## Por que este arquivo existe (gate do `05`)

A tabela `## Superfície de UI` do `01-plano-acao.md` tem quatro linhas, todas `Depende de JS? = Sim`
— o painel é Filament, ou seja Livewire + Alpine. O gate, porém, **não é a tabela**: é a pergunta
*"este cenário afirma sobre algo que só o navegador prova?"*.

O que sobrevive a essa pergunta é apenas **o cadastro funcionando com JavaScript executando**. Um
painel Filament pode devolver 200 com o corpo íntegro e estar inutilizável: um `x-on:click` que
estourou, um asset do Vite que não subiu, um componente que registrou erro no console — nenhuma
dessas três falhas move o status HTTP, e nenhuma delas é visível para o teste de componente
Livewire, que **não executa JavaScript nenhum**.

Tudo o mais da feature ficou no `04`, na camada em que se prova mais barato:

| Cenário | Onde ficou | Por quê |
|---|---|---|
| validação dos campos do formulário | `04` — CT-02, CT-05, CT-07, CT-08 | `fillForm` → `assertHasFormErrors` prova sem navegador |
| gravação pelo formulário | `04` — CT-01, CT-36 | `->call('create'/'save')` + verificação do registro |
| listagem, e o recorte de cupons ativos | `04` — CT-17, CT-18, CT-37 | `assertCanSeeTableRecords` |
| exclusão pelo botão da linha | `04` — CT-14, CT-15 | `callAction(TestAction::make('delete')->table(...))` |
| autorização na tela | `04` — CT-14, CT-16 | componente Livewire responde negado |
| unicidade do código | `04` — CT-10, CT-11, CT-12 | validação de formulário |

## Pré-requisitos

- [ ] `npm run build` executado — **pré-requisito duro**. Sem `public/build/manifest.json` toda
      tela responde `ViteException` e os dois cenários falham por um motivo que não é o deles
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por `$this->actingAs($user)` **antes** do `visit()` — o servidor é in-process,
      então sessão, `RefreshDatabase` e `:memory:` continuam valendo dentro do navegador. Login pela
      tela custa ~20 s por cenário e o kit já tem um cenário dedicado a ele
      (`tests/Browser/TelasDoKitTest.php`)
- [ ] `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach` — sem
      isso a tela responde 403 e os dois cenários medem o barramento em vez do formulário
- [ ] Arquivo: `tests/BrowserTenancy/CupomTest.php` (a pasta já existe e já está na testsuite
      `Browser` do `phpunit.xml`; o `TenancyTestCase` fixa `permission.teams` antes das migrations)

## Seletores

O kit **não tem `data-testid`** — dívida conhecida, registrada em `.ai/rules/testes-browser.md`. O
disponível hoje, e é o que estes cenários usam:

| Elemento | Seletor | Já existe? |
|---|---|---|
| campo de texto do Filament | `#data\.codigo` — `id` gerado, o `.` precisa de escape em CSS | padrão do Filament 5, confirmado no kit para `#form\.email` |
| botão de submissão do formulário | texto visível **traduzido**: `Criar` | sim |
| ação de criar na listagem | texto visível: `Novo cupom` (rótulo derivado do `modelLabel`) | depende do passo 8 do PRD |
| linha da tabela | texto do código do cupom | sim |
| mensagem de erro de campo | texto visível abaixo do campo | sim |

> **Dívida declarada**: enquanto não houver `data-testid`, os dois cenários dependem do **texto
> traduzido** dos botões. Se o rótulo mudar, eles quebram sem que a feature tenha quebrado. É o
> preço conhecido, e é menor que o de não ter nenhum cenário de navegador sobre uma tela que é
> inteiramente JavaScript.

**API confirmada no vendor, não de memória** (`vendor/pestphp/pest-plugin-browser/src/Api/Concerns/InteractsWithElements.php`):
`fill()`, `type()`, `select()`, `check()`, `click()`, `press()` existem. Os roteiros usam `fill()`,
que é o que o kit já usa (`tests/Browser/PerfisTest.php:50-51`) e é mais rápido que `type()`.
O prefixo do `id` é `data.` — `CreateRecord` e `EditRecord` declaram `->statePath('data')`
(`vendor/filament/filament/src/Resources/Pages/CreateRecord.php:323`,
`EditRecord.php:221`), ao contrário da tela de login do kit, cujo statePath é `form`.

> **Risco de arnês, declarado antes de custar tempo**: o campo de validade é um seletor de data do
> Filament, controlado por Alpine. `fill()` num campo assim pode não disparar o evento que o
> componente escuta, e o cenário falharia por um motivo que não é o dele. Se isso acontecer, a
> saída é preencher o campo pelo teclado (`fill()` + `press('Enter')`) ou aceitar a data default —
> **não** é transformar o CT-B em teste de componente, que devolveria a lacuna que ele existe para
> fechar.

---

## CT-B01: o cadastro completo funciona com JavaScript executando

**Por que browser e não Livewire**: o `04` prova que o **componente** grava (CT-01). Isso não prova
que a **tela** grava: o componente é exercitado por chamada direta de método, sem Alpine, sem o
bundle do Vite e sem o navegador. O caminho `listagem → formulário → volta com o registro na lista`
é o único que atravessa os três, e é o que RQ-01 pede — *"criar cupons de desconto no painel"*.

```gherkin
# language: pt
  Cenário: [CT-B01] a administradora cadastra um cupom pela tela e ele aparece na lista
    Dado a administradora autenticada na organização Acme, sem nenhum cupom cadastrado
    E ela na lista de cupons
    Quando ela abre o formulário, preenche código "BLACKFRIDAY", tipo percentual, valor 25,
      validade futura e limite de 40 usos, e confirma a criação
    Então a lista de cupons exibe "BLACKFRIDAY"
    E existe um cupom de código "BLACKFRIDAY" na organização Acme, com tipo percentual, valor 25,
      validade 2026-12-31 23:59, limite 40 e contador de usos 0
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir a lista | `$this->actingAs($administradora);` `visit("/app/{$acme->slug}/cupons")` | lista vazia |
| 2 | abrir o formulário | `->click('Novo cupom')->assertPathIs("/app/{$acme->slug}/cupons/create")` | formulário na tela |
| 3 | preencher | `->fill('#data\\.codigo', 'BLACKFRIDAY')->select('#data\\.tipo', 'porcentagem')->fill('#data\\.valor', '25')->fill('#data\\.expira_em', '31/12/2026 23:59')->fill('#data\\.limite_de_usos', '40')` | campos preenchidos |
| 4 | confirmar | `->press('Criar')->assertPathIs("/app/{$acme->slug}/cupons")` | volta para a lista |
| 5 | conferir na tela | `->assertSee('BLACKFRIDAY')->assertNoJavaScriptErrors()` | o registro aparece |
| 6 | conferir a persistência | `expect(Cupom::where('codigo', 'BLACKFRIDAY')->first())` → **tipo percentual**, valor 25, **validade 2026-12-31 23:59**, limite 40, contador 0 | — |

> **Por que o passo 6 confere os cinco atributos, e não três** *(achado L09/L12 da revisão
> adversarial)*: `tipo` e `expira_em` são justamente os dois campos renderizados por **widget
> JavaScript** (`Select` e seletor de data) — os únicos cuja gravação este CT-B existe para provar.
> A versão anterior conferia valor, limite e contador, e declarava o mutante M4 ("o campo de tipo
> nasce sem opção selecionável") como morto por um passo que **não lia o tipo**. Era um mutante sem
> matador não declarado, e era o mutante que só o navegador prova.

**Assertions**: `assertPathIs` **primeiro** depois de cada ação que navega — é ela que espera a
navegação. Invertida, a asserção de conteúdo é avaliada contra o snapshot da página anterior e falha
**com a ação tendo funcionado**. `assertNoJavaScriptErrors()` é assertion **de apoio**, nunca o
oráculo: uma página em branco passaria nela sozinha. A âncora de verdade é o par
*"o código aparece na lista"* + *"o registro existe com os campos que importam"*.

`assertNoJavaScriptErrors()` e não `assertNoSmoke()`: a tela é Filament (plugin de terceiro), e
`assertNoSmoke()` deixaria a suíte vermelha por `console.log` alheio.

**Nada de `wait()` com segundos fixos.** O plugin reexecuta cada assertion até
`pest()->browser()->timeout()` (20 s, `tests/Pest.php:155`). Espere pelo estado final visível.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o formulário não submete no navegador (Alpine/Livewire quebrado) embora o componente grave em teste | CT-B01 (passo 4: a URL não volta para a listagem) |
| M2 | a criação grava e a listagem não se atualiza | CT-B01 (passo 5) |
| M3 | o asset do Vite não sobe e a tela responde `ViteException` | CT-B01 (passo 1) |
| M4 | o campo de tipo é renderizado sem opção selecionável e o registro nasce sem tipo | CT-B01 (passo 6, o registro tem valor e limite conferidos) |

---

## CT-B02: o código repetido é recusado com o erro visível na tela

**Por que browser e não Livewire**: o `04` prova que a **validação existe** (CT-10). O que ele não
prova é que o erro **chega aos olhos de quem digitou**: em Filament, a mensagem de campo é
renderizada por Livewire após uma ida ao servidor, e um erro de JS nesse ciclo produz o pior
resultado possível — o formulário volta ao estado inicial, sem mensagem nenhuma, e a administradora
conclui que gravou. RQ-14 (*"o código do cupom não pode se repetir"*) é a única cláusula do card cuja
violação o usuário precisa **ver** para não repetir a tentativa.

```gherkin
# language: pt
  Cenário: [CT-B02] cadastrar um código já usado mostra o erro e não cria o cupom
    Dado a administradora autenticada na organização Acme, com um cupom "PROMO10" já cadastrado
    E ela no formulário de cadastro de cupons
    Quando ela preenche o código "PROMO10" com os demais campos válidos e confirma a criação
    Então a tela continua no formulário de cadastro
    E a tela exibe uma mensagem de erro associada ao campo de código
    E a organização Acme continua com exatamente 1 cupom, de código "PROMO10"
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar com um cupom já cadastrado | `$this->actingAs($administradora);` `visit("/app/{$acme->slug}/cupons/create")` | formulário na tela |
| 2 | preencher com o código repetido | `->fill('#data\\.codigo', 'PROMO10')->select('#data\\.tipo', 'porcentagem')->fill('#data\\.valor', '25')->fill('#data\\.expira_em', '31/12/2026 23:59')->fill('#data\\.limite_de_usos', '40')` | campos preenchidos |
| 3 | confirmar | `->press('Criar')` | permanece no formulário |
| 4 | conferir a tela | `->assertPathIs("/app/{$acme->slug}/cupons/create")->assertNoJavaScriptErrors()` | não navegou |
| 5 | **conferir a mensagem** | `->assertVisible('[data-validation-error]')` — ou o seletor do bloco de erro do campo de código, confirmado na tela real | o erro aparece sob o campo |
| 6 | conferir o não-efeito | `expect(Cupom::count())->toBe(1)` e o código do único cupom é `PROMO10` | nada foi criado |

**Assertions**: a âncora é a tripla *"não navegou"* + *"a mensagem aparece"* + *"nada foi criado"*.

> **Por que o passo 5 existe** *(achado L11 da revisão adversarial)*: sem ele, este cenário
> **prometia** "erro visível na tela" e media tudo menos isso. Uma validação que recusa em silêncio
> — o resultado mais comum de uma regra que devolve erro num campo fora do schema — deixa o
> formulário parado, sem navegar, sem criar nada e **sem mensagem**, e passava nos passos 4 e 6
> inteiros. Pior: o mutante M3 declarava `assertNoJavaScriptErrors` como seu matador, promovendo
> uma **assertion de apoio a oráculo único** — exatamente o que este arquivo proíbe dois parágrafos
> acima.
>
> **O texto da mensagem continua não sendo afirmado**, só a sua **presença**: o card não determina
> mensagem nenhuma, e afirmar o texto do PRD faria deste cenário um teste do plano. A pergunta
> **Q-04** é sobre **rótulo de campo**, não sobre a existência de um erro — as duas coisas são
> distintas, e só a segunda é falsificável sem resposta do usuário.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a validação de unicidade existe no componente e não é acionada pelo botão da tela | CT-B02 (passo 4: navegaria) |
| M2 | a tela grava o segundo cupom e volta para a listagem como se tudo estivesse certo | CT-B02 (passos 4 e 6) |
| M3 | a validação recusa em silêncio: o formulário fica parado e nenhuma mensagem é renderizada | CT-B02 (**passo 5**) — *revisão adversarial, L11* |
| M4 | o ciclo de validação estoura no console e o formulário volta limpo | CT-B02 (passos 4 e 5) |
| M5 | a segunda gravação **substitui** o cupom existente em vez de ser recusada | CT-B02 (passo 6, identidade do único cupom) |

---

## Cogitado e Cortado

O gate de CT-B é generoso e o teto do perfil `completo` é apertado (1 happy path + 1 erro visível).
Sem esta tabela, *"só há 2 CT-B"* é indistinguível de *"só pensamos em 2"*.

| Cenário cogitado | Por que foi cortado |
|---|---|
| trocar o `Select` de tipo e conferir que o rótulo do campo de valor muda de unidade | **é o corte mais doloroso e o mais defensável**: só o navegador prova (o rótulo troca por JavaScript), mas o **oráculo só existe no PRD** — o card nunca descreve rótulo de campo nenhum. Afirmar o texto seria teste do plano. Registrado como pergunta **Q-04** no `04`; enquanto ela não for respondida, o risco fica declarado e descoberto |
| a listagem exibe o rótulo de situação (`Ativo`/`Esgotado`/`Expirado`) em cada cupom | as três palavras são do PRD, não do card. O comportamento que o card determina — *quem vê o quê* — é CT-17/CT-18, no `04`, mais barato |
| exclusão pelo modal de confirmação da linha | o modal é JavaScript, mas o que o card pede (RQ-07, "excluir") é provado por CT-15; o modal em si é escolha de UI que o requisito não determina |
| o usuário comum não vê o botão de criar | *nada de affordance sem permissão* é convenção do kit, não cláusula do card. A cláusula (RQ-07) é a **ação negada**, e ela é CT-14, no `04` |
| percorrer as três rotas de cupom com `visit([...])` em lote | `visit([...])` **aborta na primeira falha** e as rotas seguintes não são verificadas naquele run; e cobertura de rota por si só (`assertNoJavaScriptErrors` sozinho) é assertion proibida como oráculo único — página em branco e 403 renderizado passariam |
| o formulário em tema escuro | `assertSee` não valida tema: passa com texto branco em fundo branco. Para defeito de cor não há saída barata, e o card não fala em tema |

---

## Roteiro de Validação: Desenhado × Implementado

Preenchido no step 7 da `feature-wiki`, depois de rodar os CT-B contra a tela real. Cada linha da
tabela `## Superfície de UI` do PRD é conferida contra o que existe; divergência vai para
`## Desvios do Plano` no `03-progresso.md`.

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | listagem com código, tipo, desconto, usos, validade e situação | | | |
| 2 | formulário de criação com os cinco campos | | | |
| 3 | formulário de edição com os mesmos campos | | | |
| 4 | ação de exclusão na linha, com confirmação | | | |
| 5 | campo de valor muda de rótulo com o tipo escolhido | | ⚠️ **sem CT-B** — oráculo pendente da pergunta Q-04 | verificação manual |
