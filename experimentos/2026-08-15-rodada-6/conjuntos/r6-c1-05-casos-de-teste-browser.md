# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Backend: `04-casos-de-teste.md`
> Runtime: `pest-plugin-browser` **5.0.1** (Playwright). **O plugin sobe o próprio servidor** —
> HTTP in-process, porta aleatória. Nada de Herd, `artisan serve`, Sail ou `APP_URL`.
> Comando: `composer test:browser` (embute `npm run build` e roda `--testsuite=Browser` **em série**).

---

## Por que este arquivo existe — o gate, e o que ele barrou

A tabela `## Superfície de UI` do `01-plano-acao.md` é o **gatilho**, não o critério. O critério é:
**o cenário afirma sobre algo que só o navegador prova?** Em Filament, quase tudo que parece "de
tela" é teste de componente Livewire — validação, gravação, listagem, busca, filtro, ação de tabela,
notificação e autorização na tela rodam em milissegundos, sem Node e sem Playwright, e estão no `04`.

Sobrou **um** cenário, e ele passa no gate por um motivo preciso:

> **`fillForm()` num teste de componente não distingue um `Select` reativo de um `Select` inerte.**
> O helper escreve o estado no componente e o Livewire re-renderiza do lado do servidor — o rótulo
> do campo dependente muda **mesmo que a reatividade não esteja declarada**. No navegador, sem a
> reatividade, trocar o tipo não dispara requisição nenhuma: o rótulo continua o antigo, o operador
> digita `1000` lendo "Percentual de desconto" e grava um desconto de 1000 % — ou digita `10` lendo
> "Valor do desconto (centavos)" e grava R$ 0,10.
>
> Nesse defeito o registro fica **correto no banco e mentiroso na tela**. Nenhum teste HTTP o vê,
> porque o HTML inicial é idêntico nos dois casos; nenhum teste de componente o vê, porque o
> re-render acontece de qualquer forma. É **JavaScript executado**, que é exatamente o que o gate
> reserva para o navegador.

**Todo o resto do CRUD ficou no `04`** — ver a tabela [`## Cogitado e Cortado`](#cogitado-e-cortado).

---

## Perfil e teto

| Área | Perfil | Teto de CT-B | Usado |
|---|---|---|---|
| A5 — Cadastro (criar/editar pela tela) | padrão | 1 | **1** |

Teto respeitado; nenhum estouro a justificar. O gate do passo 6 do pipeline vence o teto quando um
mutante só morre num CT-B além dele — não é o caso aqui: os demais candidatos morrem no `04`, mais
barato.

---

## Pré-requisitos

- [ ] `npm run build` executado — sem `public/build/manifest.json` **toda** tela responde
      `ViteException` e o cenário falha por um motivo que não é o dele. `composer test:browser` já
      embute o build.
- [ ] `tests/Browser/Screenshots` no `.gitignore` (se algum screenshot de diagnóstico for tirado).
- [ ] Os dois seeders no `beforeEach`, nesta ordem — Resource novo nasce sem permission e a tela
      responde 403 para quem não seja `master_global` (`.ai/rules/filament.md`):
      `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);`
- [ ] Autenticação por **`$this->actingAs($user)` antes do `visit()`**, nunca login pela tela —
      logar pela UI custa ~20 s por cenário (`.ai/rules/testes-browser.md`). O único cenário de
      login pela tela do kit já existe em `tests/Browser/RoteiroDoKitTest.php`.

**Arquivo**: `tests/Browser/CupomTest.php` — suíte `Browser`, `Tests\TestCase`, grupo `browser`
(`tests/Pest.php:101-104`), **modo single-tenant**.

> **Por que `tests/Browser` e não `tests/BrowserTenancy`**: o comportamento que este cenário prova
> não depende de organização nenhuma, e `tests/BrowserTenancy` paga o custo do `TenancyTestCase`
> (que refaz as migrations na virada de modo, `tests/TestCase.php`). Em single-tenant a rota é
> `/app/cupons/create`, sem o segmento `{tenant}`. Os dois diretórios estão na mesma testsuite
> `Browser` (`phpunit.xml:32-40`), então `composer test:browser` continua sendo o comando.
>
> **Cuidado ao rodar este arquivo isolado com as views frias**: `tests/Pest.php:157-168` registra que
> o primeiro cenário de um arquivo de browser paga a compilação inteira dos componentes Livewire
> sozinho (~25 s medidos) e **falha por tempo, não por comportamento**. Subir o teto de 20 s não
> resolve — foi reproduzido igual com 40 s e 60 s. Rode a suíte inteira uma vez antes.

---

## Seletores

O kit **não tem `data-testid`** — dívida conhecida, registrada em `.ai/rules/testes-browser.md`.
O disponível hoje:

| Elemento | Seletor | Já existe? |
|---|---|---|
| `Select` de tipo | `#form\.tipo` — `id` gerado pelo Filament; o `.` precisa de escape em CSS | nasce com o Resource |
| Campo de valor | `#form\.valor` | nasce com o Resource |
| Rótulo do campo de valor | texto visível — `Percentual de desconto` / `Valor do desconto (centavos)` | nasce com o Resource |

**Risco de seletor, verificado no vendor e não presumido**: o `Select` do Filament nasce nativo —
`protected bool | Closure $isNative = true` em
`vendor/filament/forms/src/Components/Concerns/CanBeNative.php:9` —, e o Blade só renderiza o
`<select>` nativo quando o campo **não** é `searchable`, `multiple` nem `htmlAllowed`
(`vendor/filament/forms/src/Components/Select.php:1838`). O `select()` do plugin mapeia para
`selectOption()` do Playwright (`.../Api/Concerns/InteractsWithElements.php:124`), que exige o
elemento nativo. **Com o campo como está desenhado, funciona.** Se a implementação acrescentar
`->native(false)`, `->searchable()` ou `->multiple()`, o Filament troca por um widget de JavaScript
e o `select()` deixa de funcionar — a interação passa a ser `click()` no gatilho e `click()` na
opção. **Isso é causa (a) do loop de CT-B** (CT-B especificado errado), não divergência de
implementação: corrigir o roteiro deste arquivo, não a tela.

**Os textos dos rótulos são `@premissa`** — ver pergunta **P-C** no `04`. O card não fala de rótulo.
Se a implementação escolher outras palavras, isto é causa (a) e o CT-B é corrigido; o que **não**
pode mudar é a exigência de que os dois rótulos sejam **mutuamente exclusivos** e distingam a
unidade.

---

## CT-B01: o campo de valor anuncia a unidade do tipo escolhido

**Por que browser e não Livewire**: a asserção depende de **JavaScript executado** — de a troca no
`Select` disparar a atualização do campo dependente no navegador. `fillForm()` produz o mesmo
re-render com e sem reatividade declarada, e portanto não falsifica nada aqui.

**Cobre**: `RQ-03` + `RQ-04` no ponto de **entrada de dados** — a unidade que o operador acredita
estar digitando. `@premissa P-C`.

```gherkin
# language: pt
  Esquema do Cenário: [CT-B01] o campo de valor anuncia a unidade do tipo escolhido
    Dado que a administradora abriu o formulário de cadastro de cupom
    E que o tipo de desconto selecionado é "<de>"
    Quando ela troca o tipo de desconto para "<para>"
    Então o formulário anuncia "<rotulo_novo>" para o campo de valor
    E não anuncia mais "<rotulo_antigo>"

    Exemplos:
      | de          | para        | rotulo_novo                  | rotulo_antigo                | # direção        |
      | porcentagem | fixo        | Valor do desconto (centavos) | Percentual de desconto       | ida              |
      | fixo        | porcentagem | Percentual de desconto       | Valor do desconto (centavos) | **volta**        |
```

> **As duas direções são obrigatórias, e a de volta é a que discrimina.** Um formulário que renderiza
> estaticamente o rótulo de valor fixo passa na linha de ida e **falha na de volta**; um que renderiza
> estaticamente o de porcentagem faz o inverso. Só o par prova que o rótulo **acompanha** o tipo em
> vez de acertar por acidente. É a mesma razão pela qual valor redondo não discrimina no `04`.
>
> **O `Dado` fixa a situação de partida** — inclusive na linha de ida, onde o estado inicial é o
> default do formulário. Sem isso, o cenário não diz de onde parte, e o `Então` de "não anuncia mais"
> ficaria sem referência.

### Roteiro executável

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar sem passar pela tela de login | `$this->actingAs(usuarioDoKit('master_global'));` | — |
| 2 | abrir o formulário de cadastro | `visit('/app/cupons/create')` | formulário renderizado |
| 3 | confirmar a rota **antes** de qualquer asserção de conteúdo | `->assertPathIs('/app/cupons/create')` | — |
| 4 | fixar a situação de partida (linha `de`) | `->select('#form\\.tipo', '<de>')` | tipo de partida selecionado |
| 5 | confirmar que a partida é a esperada | `->assertSee('<rotulo_antigo>')` | rótulo de partida visível |
| 6 | **a única ação do cenário** | `->select('#form\\.tipo', '<para>')` | requisição do Livewire disparada pelo navegador |
| 7 | o oráculo | `->assertSee('<rotulo_novo>')` | rótulo novo visível |
| 8 | o oráculo, outra metade | `->assertDontSee('<rotulo_antigo>')` | rótulo antigo sumiu |
| 9 | apoio | `->assertNoJavaScriptErrors();` | console sem erro |

```php
// Esboço — a materialização é do agente implementador, e o Esquema vira ->with([...])
$this->actingAs(usuarioDoKit('master_global'));

visit('/app/cupons/create')
    ->assertPathIs('/app/cupons/create')
    ->select('#form\\.tipo', $de)
    ->assertSee($rotuloAntigo)
    ->select('#form\\.tipo', $para)
    ->assertSee($rotuloNovo)
    ->assertDontSee($rotuloAntigo)
    ->assertNoJavaScriptErrors();
```

**Assertions**

- `assertPathIs` **antes** das asserções de conteúdo — é ela que espera a navegação. Invertida, o
  `assertSee` roda contra o snapshot da página anterior e falha **com a ação tendo funcionado**
  (`.ai/rules/testes-browser.md`).
- **Nada de `wait($segundos)`.** O plugin reexecuta cada asserção até o teto de
  `pest()->browser()->timeout(20_000)` (`tests/Pest.php:170`). `waitForText()` **existe** nesta
  versão do plugin (conferido em `vendor/pestphp/pest-plugin-browser/src/Api/Concerns/`), ao
  contrário do que a documentação da `feature-wiki` afirma — e mesmo assim não é usada aqui:
  esperar pelo **estado final visível** já é o que `assertSee` faz. `waitForSelector` e `waitUntil`
  **não** existem; não inventar.
- `assertNoJavaScriptErrors()` e **não** `assertNoSmoke()`: a tela é de plugin de terceiro
  (Filament), e `assertNoSmoke()` fica vermelho por `console.log` alheio
  (`.ai/rules/testes-browser.md`).
- **Console nunca é o oráculo.** `assertNoJavaScriptErrors()` sozinho passa com página em branco,
  com 403 renderizado e com a tela sem conteúdo. O oráculo deste cenário é o par
  `assertSee` + `assertDontSee` dos dois rótulos.

### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M-B1 | o campo de tipo não é reativo — a tela só recalcula o rótulo ao recarregar | **CT-B01, as duas linhas** (e nenhum cenário do `04`, por construção) |
| M-B2 | o rótulo é fixo no de porcentagem | CT-B01, linha **ida** |
| M-B3 | o rótulo é fixo no de valor fixo | CT-B01, linha **volta** |
| M-B4 | a condição do rótulo compara o objeto do tipo com a string do estado do Livewire e nunca casa — o rótulo cai sempre no ramo `else` | CT-B01, a linha cujo `rotulo_novo` é o do ramo `if` |
| M-B5 | o rótulo troca, mas a tela dispara erro de JavaScript no caminho | `assertNoJavaScriptErrors()` — **assertion de apoio**, nunca o oráculo |
| M-B6 | o rótulo troca na tela e o **valor gravado** é interpretado com a outra unidade | ⚠️ **sem matador aqui, e de propósito**: quem mata é **CT-01** do `04` (gravação por componente nos dois tipos) e **CT-33** (o cálculo por tipo). Empurrar essa asserção para o navegador seria repetir na camada cara o que a barata prova |

---

## Cogitado e Cortado

O gate do `05` é generoso e o teto é apertado — sem esta tabela, "só há 1 CT-B" é indistinguível de
"só pensamos em 1", e a próxima pessoa refaz a análise do zero.

| Cenário cogitado | Por que foi cortado |
|---|---|
| criar um cupom pelo navegador, atravessando listagem → formulário → volta com o registro na lista | o que ele provaria a mais que **CT-01** é a navegação (padrão do Filament, não desta feature) e o console (já em CT-B01). Repetir caminho feliz na camada cara sem provar nada a mais é exatamente o que o passo 7 manda podar |
| o modal de confirmação da exclusão | modal do Filament é renderizado pelo servidor; `callAction(TestAction::make('delete')->table($cupom))` prova em milissegundos — é **CT-45**. A forma com o **nome** da ação, e não o FQCN, é a que o projeto usa (`tests/Kit/ConviteTest.php:285`) |
| a mensagem de erro de validação aparecendo abaixo do campo | validação de formulário Filament é `assertHasFormErrors()` — **CT-02, CT-06, CT-07** |
| a listagem escondendo os cupons não-ativos do usuário comum | `assertCanNotSeeTableRecords()` prova em milissegundos — **CT-22**. O que só o navegador provaria seria a coluna estar *visualmente* oculta, e o card não fala de layout |
| as ações de criar/editar/excluir sumindo para o usuário comum | `assertActionDoesNotExist(TestAction::make('delete')->table($cupom))` prova por componente, no molde de `tests/Tenancy/AdminDaOrganizacaoTest.php:498` — parte de **CT-16** |
| auditoria de acessibilidade das três telas de cupom (`assertNoAccessibilityIssues()`) | vale a pena e **não é desta feature**: é auditoria de painel, e o kit já tem a wiki `regressao-de-telas` para isso. Aqui seria orçamento de CT-B gasto fora do que o card pede |
| tema escuro nas telas de cupom | `assertSee` **não valida tema** — passa com texto branco em fundo branco (`.ai/rules/testes-browser.md`). Para defeito de cor não há saída barata, e o card não fala de cor |
| busca por código na tabela | `searchTable()` prova por componente; e o card não normatiza busca |

---

## Roteiro de Validação: Desenhado × Implementado

> Preenchido no **step 7 da `feature-wiki`**, depois de os CT-B rodarem contra a tela real. Cada
> linha confronta a tabela `## Superfície de UI` do `01-plano-acao.md` com o que existe.
> Divergência vai para "Desvios do Plano" no `03-progresso.md`.

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | `CuponsTable` em `/app/cupons` — lista, ordena, busca por código, situação em badge | | ⬜ | |
| 2 | `CupomForm` — criar em `/app/cupons/create`, com o campo de valor mudando de rótulo com o tipo | | ⬜ | CT-B01 |
| 3 | `CupomForm` — editar em `/app/cupons/{uuid}/edit` (a chave de rota é o **uuid**, não o id — `TemUuid::getRouteKeyName()`) | | ⬜ | |
| 4 | `DeleteAction` na linha, com modal de confirmação | | ⬜ | CT-45 |

**Classificação obrigatória de cada CT-B vermelho, antes de mexer em qualquer coisa:**

| Causa | O que fazer |
|---|---|
| **(a)** CT-B especificado errado (seletor, rota, texto do rótulo) | corrigir **este arquivo**, não a tela |
| **(b)** implementação divergente do PRD | **NÃO corrigir**. Registrar a divergência em "Desvios do Plano" — vermelho por causa (b) é resultado válido, é a medição que se queria |
| **(c)** instabilidade de tempo | rever a estratégia de espera (estado final visível, nunca `wait(n)`) e anotar |

**Proibido**: alterar código de aplicação para o teste passar; relaxar assertion para ficar verde;
remover CT-B que não passou. Após 3 iterações com vermelho, parar e registrar como blocker no
`03-progresso.md`.
