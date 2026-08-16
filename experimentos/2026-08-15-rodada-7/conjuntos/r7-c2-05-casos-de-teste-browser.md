# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Backend: `04-casos-de-teste.md`
> Runtime: `pest-plugin-browser` ^5.0 (Playwright). **O plugin sobe o próprio servidor** —
> HTTP in-process, porta aleatória. Nada de Herd, `artisan serve`, Sail ou Vite dev server.
> Comando: `vendor/bin/pest --testsuite=Browser` — **em série, nunca `--parallel`**.

## Por que existem só dois CT-B

A tabela `## Superfície de UI` do PRD tem **6 linhas**, todas com `Depende de JS? = Sim`. Isso é
o **gatilho** do gate, não o critério. O critério é outro: o cenário só vai ao navegador quando
afirma sobre algo que **só o navegador prova** — JavaScript executado, console/erro de JS,
acessibilidade, cor, tema, layout.

Aplicado o critério, quase toda a superfície ficou no `04`, como teste de componente Livewire —
milissegundos, sem Node, sem Playwright:

| O que parecia CT-B | Onde ficou de verdade | Por quê |
|---|---|---|
| validação do formulário de solicitação | CT-01, CT-03, CT-05 | `fillForm` → `assertHasFormErrors` |
| gravação pelo formulário (create e edit) | CT-01, CT-05, CT-38, CT-39 | `->call('create'\|'save')` + asserção no banco |
| listagem e badge de situação | CT-25 | `assertTableColumnStateSet` |
| ações Enviar / Aprovar / Rejeitar / Cancelar | CT-15…CT-18, CT-24 | `callAction(TestAction::make(...)->table(...))` |
| affordance por persona (quem vê qual botão) | CT-09, CT-18 | `assertActionVisible` / `assertActionHidden` |
| autorização na tela (403) | CT-33, CT-35 | `livewire(...)->assertForbidden()` |
| infolist com o histórico de etapas | CT-26, CT-27 | componente, com `freezeTime` |

Sobraram **dois**, e os dois são a mesma coisa que só o navegador prova: **a modal de rejeição
existe porque o Alpine a monta**. Um teste de componente chama `callAction('rejeitar', [...])` e
prova que a *ação* funciona — ele **nunca** abre a modal, nunca renderiza o `<textarea>` e nunca
descobre que o botão que a dispara não responde ao clique.

**Teto do perfil**: as áreas centrais são `completo` → 1 happy path + 1 erro visível. Os dois
cenários abaixo são exatamente esses dois. Nada foi cortado por estouro; o que foi cogitado e
recusado está na tabela do fim.

---

## Pré-requisitos

- [ ] **`npm run build` executado** — pré-requisito **duro**. Sem `public/build/manifest.json`
      toda tela responde `ViteException` e todo cenário falha por um motivo que não é o dele.
      O script `composer test:browser` já embute o build (`composer.json:129-134`).
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por **`$this->actingAs($user)` antes do `visit()`** — funciona porque o
      servidor do plugin roda **in-process** (`tests/Pest.php:95-98`). Login pela tela custa ~20 s
      por cenário, e o kit já reserva o único cenário de login real em
      `tests/Browser/PerfisTest.php`.
- [ ] `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach`, pelo
      `seed()` sobrescrito de `Tests\TestCase` — o `seed()` do Laravel grava **0 permissions**.
- [ ] Suíte: `tests/Browser/Compras/RejeicaoTest.php`. A pasta `tests/Browser` já está registrada
      em `tests/Pest.php:101-104` (grupo `browser`, `TestCase`, `RefreshDatabase`) e em
      `phpunit.xml:32-40`. **Nada de infra nova é necessário para estes dois cenários** — ao
      contrário de CT-36/CT-37 do `04`, que dependem da suíte `FeatureTenancy` inexistente.
- [ ] Teto de espera já configurado: `pest()->browser()->timeout(20_000)` (`tests/Pest.php:170`).
      **Nunca `wait($segundos)`** — o plugin reexecuta cada assertion até o teto. `waitForText`,
      `waitForSelector` e `waitUntil` **não existem**.

## Seletores

O kit **não tem `data-testid`** — dívida conhecida e registrada em `.ai/rules/testes-browser.md`.
O que existe hoje:

| Elemento | Seletor | Já existe? |
|---|---|---|
| botão de ação de linha "Rejeitar" | texto visível `Rejeitar` | não — nasce com o `SolicitacaoCompraResource` (PRD passo 9b) |
| campo da modal de rejeição | `#form\.justificativa` — `id` gerado pelo Filament, com o `.` escapado em CSS | não — nasce com o `->schema([Textarea::make('justificativa')])` |
| rótulo do campo | `Motivo da rejeição` (texto **traduzido**, PRD passo 9b) | não |
| botão de submit da modal | texto `Rejeitar` (`modalSubmitActionLabel`) | não |
| badge de situação na listagem | texto do rótulo do enum | não |

> **Dívida registrada**: se o PRD acrescentar `->extraAttributes(['data-testid' => ...])` às duas
> ações, estes CT-B ficam imunes a mudança de rótulo. Enquanto não houver, o seletor é o texto
> traduzido — e ele **é** parte do que quebra quando alguém muda o label.

---

## CT-B01: a modal de rejeição abre, aceita o motivo e conclui a rejeição

**Por que browser e não Livewire**: a asserção depende de **JavaScript executado**. A modal do
Filament é montada pelo Alpine no clique; ela não existe no DOM antes disso. `callAction()` do
teste de componente pula essa etapa inteira — ele injeta os dados e executa o handler, e fica
verde com o botão morto, com o `<textarea>` que não renderiza e com um erro de JS que impede a
modal de abrir. Este é o único cenário do conjunto que prova que **um humano consegue rejeitar**.

```gherkin
# language: pt
  Cenário: [CT-B01] o gestor rejeita pela tela, escrevendo o motivo na modal
    Dado o Rui autenticado como gestor do centro "TI"
    E uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", nesse centro, e a modal
      "Rejeitar" já aberta sobre ela
    Quando o Rui escreve "Fornecedor não homologado" no motivo e confirma
    Então a linha daquela solicitação passa a mostrar a situação "Rascunho"
    E a página de visualização dela mostra "Fornecedor não homologado" no histórico
    E o console do navegador não acusa erro de JavaScript
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir a listagem | `$this->actingAs($rui);` → `visit('/app/solicitacoes-de-compra')` | a linha da solicitação |
| 2 | **âncora de partida, na linha** | `->assertSeeIn('tr:has-text("Notebooks")', 'Aguardando gestor')` | a situação **daquela linha** |
| 3 | abrir a modal (`Dado`) | `->click('Rejeitar')` | a modal monta (Alpine) |
| 4 | confirmar que ela **abriu** | `->assertSee('Motivo da rejeição')` | o rótulo do campo, que só existe dentro da modal |
| 5 | escrever o motivo | `->fill('#form\\.justificativa', 'Fornecedor não homologado')` | o texto no `textarea` |
| 6 | submeter (o `Quando`) | `->press('Rejeitar')` | a modal fecha, a tabela recarrega |
| 7 | **a âncora de chegada** | `->assertSeeIn('tr:has-text("Notebooks")', 'Rascunho')` | a situação nova, **na linha certa** |
| 8 | **o motivo persistiu** | `visit('/app/solicitacoes-de-compra/{uuid}')` → `->assertSee('Fornecedor não homologado')` | o texto no histórico |
| 9 | console | `->assertNoJavaScriptErrors()` | — |

**Assertions e a ordem delas**

- O passo 4 é o que separa *"a modal abriu"* de *"o clique não fez nada"*. Sem ele, o `fill()` do
  passo 5 falharia por seletor ausente e o erro apontaria o campo, não a causa.
- ⚠️ **Os passos 2 e 7 usam `assertSeeIn`, e não `assertSee` — correção da revisão adversarial
  (achado nº 16).** A versão anterior ancorava em `assertSee('Rascunho')`, e a listagem do Filament
  **renderiza o `SelectFilter` de situação com os cinco rótulos no DOM** antes de qualquer clique.
  A âncora casava com a **opção do filtro**, não com a linha: o cenário ficava verde com o clique
  não tendo feito nada. Era exatamente o anti-padrão que o `04` critica em CT-25 — *"o texto
  aparece em qualquer estado da página se estiver no layout"* — usado três parágrafos depois.
  `assertSeeIn(seletor, texto)` existe em
  `vendor/pestphp/pest-plugin-browser/src/Api/Concerns/MakesElementAssertions.php:93` e restringe
  a busca ao escopo da linha.
- ⚠️ **O passo 8 é o vínculo motivo↔etapa, e ele faltava.** O texto digitado na modal nunca era
  verificado em lugar nenhum do CT-B: uma implementação que rejeitasse **sem persistir a
  justificativa vinda da modal** passava, e o quadro de mutantes admitia isso na própria linha de
  MB3. Como este é o único caminho fim a fim que existe — humano digita → Livewire recebe → model
  grava → tela exibe —, é aqui que ele se fecha.
- **Não há navegação até o passo 8** — a modal e o recarregamento da tabela são Livewire na mesma
  URL. Por isso **não** há `assertPathIs` nos passos 1-7: ele é obrigatório **depois de ação que
  navega**, e aqui não há nenhuma. Usá-lo por hábito não prova nada e esconde que a espera real é
  pelo estado visível.
- `assertNoJavaScriptErrors()` e **não** `assertNoSmoke()`: a tela é um Resource do Filament, com
  plugins de terceiro carregados no painel `/app`, e `assertNoSmoke()` deixaria a suíte vermelha
  por `console.log` alheio (`.ai/rules/testes-browser.md`).
- **O console nunca é o oráculo único.** As âncoras deste cenário são os passos 7 e 8. Uma página
  em branco, um 403 renderizado e uma tabela vazia passam por `assertNoJavaScriptErrors()` sozinho.

#### Mutantes previstos — CT-B01

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB1 | a ação "Rejeitar" é declarada com `requiresConfirmation()` **e** `->schema()`, e as duas modais brigam — o campo nunca aparece | CT-B01 (passo 3) |
| MB2 | o `Textarea` é declarado fora do `->schema()` da ação e não renderiza na modal | CT-B01 (passo 3/4) |
| MB3 | a ação é montada, mas o handler não recebe o `$data` da modal e rejeita **sem o motivo** | CT-B01 (**passo 8**) — antes da revisão adversarial este mutante **não tinha matador**, e o quadro admitia isso |
| MB4 | o painel `/app` carrega um asset quebrado e a tabela renderiza sem as ações de linha | CT-B01 (passo 3) + `assertNoJavaScriptErrors()` |
| MB9 | o clique não faz nada, e o cenário passa porque o rótulo "Rascunho" já está no DOM pelo `SelectFilter` | CT-B01 (passos 2 e 7, com `assertSeeIn` na linha) — achado nº 16 |

---

## CT-B02: a modal recusa o envio sem motivo, e o erro aparece para o usuário

**Por que browser e não Livewire**: CT-20 do `04` já prova que o **erro existe** — `assertHasActionErrors(['justificativa'])`
afirma o error bag. O que ele **não** prova é que a mensagem **chega aos olhos de quem está na
tela**, e esse é o defeito real e comum: o campo tem `->required()`, o Livewire recusa
corretamente, e o usuário vê a modal piscar sem entender por quê — porque a mensagem foi
renderizada fora da modal, escondida por overflow, ou não renderizada de todo.

Este é o **erro visível** que o teto do perfil `completo` reserva.

```gherkin
# language: pt
  Cenário: [CT-B02] a modal aponta o motivo faltante sem fechar nem recarregar a página
    Dado o Rui autenticado como gestor do centro "TI"
    E uma solicitação da Ana de R$ 7.500,00, em "aguardando gestor", nesse centro, e a modal
      "Rejeitar" já aberta sobre ela
    Quando o Rui confirma com o motivo em branco
    Então a modal continua aberta e mostra a mensagem de campo obrigatório
    E a linha daquela solicitação continua mostrando "Aguardando gestor"
    E o console do navegador não acusa erro de JavaScript
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir a listagem | `$this->actingAs($rui);` → `visit('/app/solicitacoes-de-compra')` | a linha da solicitação |
| 2 | abrir a modal (`Dado`) | `->click('Rejeitar')` | a modal monta |
| 3 | submeter vazio (o `Quando`) | `->press('Rejeitar')` | a validação dispara no Livewire |
| 4 | **o erro é visível** | `->assertSee('Motivo da rejeição')` **e** a mensagem de obrigatoriedade | a modal **continua aberta**, com o erro |
| 5 | **nada mudou atrás** | `->assertSeeIn('tr:has-text("Notebooks")', 'Aguardando gestor')` | a situação intacta **na linha** |
| 6 | console | `->assertNoJavaScriptErrors()` | — |

**Assertions**

- O passo 4 é o oráculo do cenário: **a modal continua aberta** (é o `assertSee` do rótulo, que
  só existe dentro dela) **e** a mensagem de erro está na tela.
- O passo 5 é o não-efeito, e ele usa **`assertSeeIn` na linha** pela mesma razão de CT-B01: o
  `SelectFilter` da listagem já traz "Aguardando gestor" no DOM, e um `assertSee` global passaria
  **mesmo com a solicitação tendo sido rejeitada**. Sem essa correção, o cenário era vacuamente
  verde no exato defeito que ele existe para pegar — uma implementação que rejeitasse e **depois**
  mostrasse o erro.
- ⚠️ **O texto exato da mensagem de obrigatoriedade vem do `laravel-lang/common`**
  (`composer.json:71`), não do PRD. Ao materializar, **confirmar a string traduzida** em
  `lang/pt_BR/validation.php` antes de escrever o `assertSee` — a alternativa é asserir o rótulo
  do campo mais a permanência da modal, que já discrimina e não depende de tradução.

#### Mutantes previstos — CT-B02

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB5 | o `->required()` é esquecido no `Textarea`, e a modal fecha submetendo vazio | CT-B02 (passos 4 e 5) |
| MB6 | a validação dispara, mas a mensagem é renderizada fora da modal e some no `overflow` | CT-B02 (passo 4) |
| MB7 | a modal fecha ao submeter vazio, e o erro aparece como notificação que some | CT-B02 (passo 4: o rótulo do campo não estaria mais visível) |
| MB8 | a ação recusa **depois** de transicionar, e a tela volta com a situação já alterada | CT-B02 (passo 5, **com `assertSeeIn` na linha**) |

---

## Fechamento da Revisão Adversarial

O `05` recebeu **dois** dos dezessete achados da revisão (o ledger completo está no `04`, em
`## Revisão Adversarial`). Os dois eram do mesmo tipo, e o mais desconfortável possível: **os dois
CT-B estavam ancorados em texto de layout**.

| Achado | O que estava errado | O que virou |
|---|---|---|
| nº 16 | `assertSee('Rascunho')` e `assertSee('Aguardando gestor')` casavam com as opções do `SelectFilter` de situação, que a listagem do Filament renderiza no DOM **antes de qualquer clique**. Os dois cenários passavam com o clique não tendo feito nada | `assertSeeIn('tr:has-text(…)', …)` — escopo na linha, nos passos 2, 5 e 7 |
| nº 17 | `Quando` com três ações em CT-B01 e duas em CT-B02 | a abertura da modal foi para o `Dado`; o `Quando` ficou com a ação única que o cenário afirma |

E o achado nº 16 trouxe junto uma lacuna que ninguém tinha notado: **o motivo digitado na modal
nunca era verificado**. O quadro de mutantes de CT-B01 chegava a admitir, em MB3, que o mutante
*"o handler não recebe o `$data` da modal"* não morria ali — e ninguém fechou. Virou o **passo 8**,
que é o único ponto do conjunto inteiro onde o caminho fim a fim se fecha: humano digita → Livewire
recebe → model grava → tela exibe.

> A ironia que vale registrar: o `04` critica explicitamente o `assertSee` de texto de layout —
> *"o texto aparece em qualquer estado da página se estiver no layout"* — ao justificar por que
> CT-25 usa `assertTableColumnStateSet`. Três seções depois, o `05` fazia exatamente isso. **É o
> argumento de por que a revisão adversarial é delegada a quem não derivou**: quem escreveu a
> crítica não a aplicou ao próprio texto, e não teria aplicado numa autorrevisão.

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| o fluxo completo entre as três personas no navegador (Ana envia → Rui aprova → Dora aprova) | provado por CT-12, CT-14 e CT-28 no `04`, em milissegundos. O que o browser acrescentaria é a troca de sessão, que `actingAs()` faz sem navegador |
| a cor do badge de situação (verde para aprovada, vermelho para cancelada) | `assertSee` **não valida tema nem cor** — passa com texto branco em fundo branco. Provar cor exige screenshot e olho humano. **Dívida declarada**, não lacuna de derivação: a cor está recusada como oráculo no `04` (pergunta A-19) |
| affordance por persona vista no navegador (o Bruno não encontra "Aprovar") | CT-09 e CT-18 provam por componente, com cinco personas. O browser provaria as mesmas cinco, ~200× mais caro |
| as telas de centro de custo no navegador | CRUD declarativo, área de perfil `mínimo`, sem JS próprio. `assertNoJavaScriptErrors` genérico das telas do `/app` já é coberto por `tests/Browser/TelasDoKitTest.php` do kit |
| tema escuro nas telas novas | já coberto por `tests/Browser/TemaEscuroTest.php` do kit, e `->inDarkMode()->assertSee(...)` **não testa dark mode** |
| auditoria de acessibilidade (`assertNoAccessibilityIssues()`) nas duas telas novas | **lacuna declarada por teto**: o perfil reserva 1 happy path + 1 erro visível, e nenhum mutante previsto morre só com ela. Candidata natural à próxima rodada, e barata de acrescentar — um cenário por tela |
| a modal de confirmação de "Enviar" e de "Cancelar" (`requiresConfirmation`) | mata o mesmo mutante que CT-B01 (modal do Alpine que não monta), pelo componente mais simples dos dois. Mantido um só, o que tem formulário — que é o caso difícil |

---

## Roteiro de Validação: Desenhado × Implementado

Preenchido no **step 7 da `feature-wiki`**, depois de rodar os CT-B contra a UI real. Cada linha
confronta a tabela `## Superfície de UI` do PRD com a tela que existe. Divergência vai para
"Desvios do Plano" no `03-progresso.md` — e **não** vira correção silenciosa do CT-B.

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | `SolicitacoesCompraTable` — situação em badge, ações Enviar/Aprovar/Rejeitar/Cancelar | | ⬜ | |
| 2 | `SolicitacaoCompraForm` (create/edit) — descrição, valor, centro de custo | | ⬜ | |
| 3 | `ViewSolicitacaoCompra` — situação + histórico com quem decidiu, quando e por quê | | ⬜ | |
| 4 | Modal "Rejeitar" — `->schema()` com justificativa obrigatória, sem `requiresConfirmation()` | | ⬜ | CT-B01, CT-B02 |
| 5 | Modais "Enviar" / "Cancelar" — `requiresConfirmation()` | | ⬜ | |
| 6 | `CentrosCustoTable` + form — nome e gestor | | ⬜ | |

> **Regra do loop de execução** (`feature-wiki`, step 7): ao falhar, classificar a causa **antes**
> de mexer em qualquer coisa — (a) CT-B especificado errado → corrigir o CT-B aqui; (b)
> implementação divergente do PRD → **não corrigir**, registrar a divergência; (c) flake de
> timing → rever a estratégia de espera. **Teste vermelho por causa (b) é resultado válido.**
> Nunca alterar código de aplicação nem relaxar assertion para ficar verde.
