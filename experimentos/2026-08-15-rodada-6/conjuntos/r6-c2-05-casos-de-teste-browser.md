# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md` · Backend: `04-casos-de-teste.md`
> Runtime: `pest-plugin-browser` ^5.0 (Playwright). **O plugin sobe o próprio servidor**,
> HTTP in-process, em porta aleatória — nada de Herd, `artisan serve`, Sail ou `APP_URL`.
> Comando: `vendor/bin/pest --testsuite=Browser` (em série — **nunca** `--parallel`)

---

## Por que este arquivo existe — o gate, aplicado

A tabela `## Superfície de UI` do `01-plano-acao.md` tem seis linhas, todas com
`Depende de JS? = Sim`. **Isso é o gatilho, não o critério.** O critério é: o cenário afirma sobre
algo que **só o navegador prova**?

Aplicado linha a linha:

| Linha da `## Superfície de UI` | Só o navegador prova? | Onde ficou |
|---|---|---|
| listagem com a situação em badge | **não** — `assertCanSeeTableRecords` + `assertSee` do rótulo | `04`, CT-28 |
| ações Enviar / Aprovar / Cancelar (confirmação nativa) | **não** — `callAction(TestAction::make(...))` | `04`, CT-22…CT-27 |
| visibilidade das ações por persona | **não** — `assertActionHidden` / `assertActionVisible` | `04`, CT-33 |
| formulário de criação e edição | **não** — `fillForm` → `call('create'\|'save')` | `04`, CT-01, CT-02, CT-16 |
| infolist com o histórico | **não** — `assertSee` no componente | `04`, CT-29 |
| **modal "Rejeitar" com formulário dentro** | **sim** | **CT-B01, CT-B02** |
| autorização na tela (403) | **não** — `livewire(...)->assertForbidden()` | `04`, CT-15a, CT-39 |

**Sobra uma coisa, e é a modal de formulário.** `callAction(TestAction::make('rejeitar'), [...])`
entrega o `$data` direto ao `->action()` do Filament: ele prova que a **ação** funciona e
**não abre modal nenhuma**. A modal do Filament 5 é Alpine + Livewire — ela monta, faz o
`wire:model` dos campos do `->schema()`, e é ela que o gestor vê. Uma modal que não abre por erro
de JS deixa `callAction` **verde** e a tela **inutilizável**, que é exatamente o par de falhas que
o `tests/Pest.php` deste projeto descreve para justificar a existência da suíte de browser
(*"o corpo do HTML pode vir íntegro e a tela estar inutilizável porque um `x-on:click` estourou"*).

**Gate: passa.** Dois CT-B, que é o teto do perfil `completo` (1 happy path + 1 erro visível).

---

## Suíte, e por que não é `tests/Browser`

**`tests/BrowserTenancy/`**, não `tests/Browser/`.

`tests/Browser` roda sob `Tests\TestCase`, que força `KIT_TENANCY=false`. Sem organização no
contexto, `BelongsToTenant` não preenche `tenant_id`
(`app/Traits/BelongsToTenant.php:72-78`) — e `solicitacoes_compra.tenant_id` é NOT NULL e está
fora do `$fillable`. **Toda fixture desta feature falharia no insert**, por um motivo que não é o
do cenário.

`tests/BrowserTenancy` já existe, já está registrada em `phpunit.xml` (dentro da testsuite
`Browser`) e em `tests/Pest.php:142-145` com `TenancyTestCase` — nada de infra nova é necessário
para os CT-B. Com tenancy ligada, as rotas do painel ganham o segmento da organização:
`/app/{slug}/…` (`AppPanelProvider.php:287`, `slugAttribute: 'slug'`).

---

## Pré-requisitos

- [ ] `npm run build` executado — **pré-requisito duro**: sem `public/build/manifest.json` toda
      tela responde `ViteException` e os dois cenários falham por um motivo que não é o deles. O
      `composer test:browser` já embute o build.
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por `$this->actingAs($user)` **antes** do `visit()` — nunca login pela tela.
      O servidor do plugin é in-process, então a sessão do teste vale dentro do navegador.
      (`.ai/rules/testes-browser.md`; medido no kit: login pela UI custa ~20 s por cenário)
- [ ] `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach` — sem
      os dois, as telas respondem 403 e o cenário mede a ausência de permission
      (padrão de `tests/BrowserTenancy/IdentidadeVisualTest.php:23-27`)
- [ ] `pest()->browser()->timeout(20_000)` já está no `tests/Pest.php:170` — **não** mexer.
      Rodar um arquivo isolado com as views frias falha por compilação, não por comportamento;
      rodar a suíte inteira resolve (docblock do próprio `tests/Pest.php:157-168`)

---

## Seletores

O kit **não tem `data-testid`** — dívida conhecida, registrada em `.ai/rules/testes-browser.md`.
O disponível hoje:

| Elemento | Seletor | Já existe? |
|---|---|---|
| ação "Rejeitar" na linha da tabela | texto visível `Rejeitar` | não — nasce com esta feature |
| campo da justificativa na modal | `#mountedActionsData\.0\.justificativa` (id gerado pelo Filament, o `.` escapado em CSS) — **confirmar na primeira execução**; o fallback é o rótulo visível `Motivo da rejeição` | não |
| botão de submissão da modal | texto visível `Rejeitar` (é o `modalSubmitActionLabel` do PRD) | não |
| situação na tela | texto visível do rótulo: `Rascunho`, `Aguardando gestor`, … | não |
| mensagem de campo obrigatório | texto do Laravel-Lang em pt-BR para `required` | sim (o kit tem `laravel-lang/common`) |

> **Dívida a registrar**: o botão da ação e o botão de submissão da modal têm o **mesmo texto**
> (`Rejeitar`). Na materialização, desambiguar pelo escopo da modal ou dar `->label()` distinto ao
> submit. É o tipo de detalhe que só aparece com o navegador aberto — e por isso está aqui, e não
> descoberto na terceira iteração do loop.

---

## CT-B01 — a modal de rejeição abre, aceita o motivo e devolve a solicitação ao rascunho

**Por que browser e não Livewire**: a asserção é sobre **JavaScript executado**. `callAction` (o
caminho do `04`) entrega o `$data` diretamente ao `->action()` e nunca renderiza a modal. Aqui o
gestor **clica**, a modal do Filament **monta** (Alpine + `wire:model` do `->schema()`), ele
digita e submete. Uma modal quebrada por erro de JS — o caso concreto do kit: um `x-on:click` que
estoura — deixa todos os cenários do `04` verdes e a tela inoperante.

```gherkin
# language: pt
  Cenário: [CT-B01] o gestor rejeita pela modal, escrevendo o motivo
    Dado uma solicitação de 3.200,50 da Solange aguardando o gestor Gustavo, na organização Acme
    Quando o Gustavo aciona "Rejeitar" na tela, escreve "Sem verba neste trimestre" e confirma
    Então a tela mostra a situação "Rascunho"
    E a solicitação gravada está na situação de rascunho, com a rejeição do Gustavo registrada
    E o console do navegador não acusa erro de JavaScript
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar como o gestor | `$this->actingAs($gustavo);` | — |
| 2 | abrir a listagem da organização | `visit("/app/{$acme->slug}/solicitacoes-de-compra")` | a linha da solicitação |
| 3 | conferir o estado de partida | `->assertSee('Aguardando gestor')` | badge da situação |
| 4 | acionar a rejeição | `->click('Rejeitar')` | a modal monta |
| 5 | **provar que a modal abriu** | `->assertSee('Rejeitar solicitação')` | o `modalHeading` do PRD |
| 6 | escrever o motivo | `->type('#mountedActionsData\\.0\\.justificativa', 'Sem verba neste trimestre')` | texto no campo |
| 7 | confirmar | `->press('Rejeitar')` | a modal fecha |
| 8 | esperar o estado final visível | `->assertSee('Rascunho')` | badge mudou |
| 9 | console | `->assertNoJavaScriptErrors();` | — |
| 10 | **âncora de persistência** | `expect($solicitacao->fresh()->situacao)->toBe(SituacaoSolicitacao::Rascunho);` e o histórico com a rejeição do Gustavo e o motivo | — |

**Assertions**: sem navegação de página, **não** cabe `assertPathIs` aqui — a modal é in-place e o
path não muda. Onde houver navegação (não é o caso deste roteiro), ela viria **antes** de qualquer
`assertSee`. `assertNoJavaScriptErrors()` e **não** `assertNoSmoke()`: a tela é um painel Filament
cheio de plugins de terceiro, e `assertNoSmoke` deixaria a suíte vermelha por `console.log` alheio
(`.ai/rules/testes-browser.md`).

**O console nunca é o oráculo único.** O passo 5 (a modal abriu), o passo 8 (a situação na tela) e
o passo 10 (o registro e o histórico) são os oráculos; o console é apoio.

> **Correção da revisão adversarial (achado D6, o mesmo que reescreveu o CT-28 do `04`).**
> `assertSee('Rascunho')` é asserção **de página**, não de linha: um `SelectFilter` de situação
> põe os cinco rótulos no HTML e o passo 8 fica verde com a coluna de situação inexistente. Aqui o
> risco é menor que no `04` — o passo 10 ancora no registro —, mas o oráculo **de tela** ficaria
> vazio. Mitigação, sem custo: o `Dado` monta **uma única** solicitação nesta listagem, e o passo 3
> assere `Aguardando gestor` **antes** da ação. Com um só registro e a transição observada de um
> rótulo para o outro na mesma página, `assertSee` volta a discriminar. Se a tela vier com filtro
> de situação, trocar os passos 3 e 8 por asserção ancorada na linha do registro.

**Nunca `wait($segundos)`** — o plugin reexecuta cada assertion até o teto de
`pest()->browser()->timeout()`. `waitForText`, `waitForSelector` e `waitUntil` **não existem**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB1 | a ação "Rejeitar" é declarada com `requiresConfirmation()` **e** `->schema()` — a modal de confirmação engole o formulário e o campo do motivo nunca aparece | CT-B01, passo 6 (o seletor não existe) |
| MB2 | a modal monta mas o `wire:model` da justificativa não liga — o campo é digitável e chega vazio ao `->action()` | CT-B01, passo 10 (o histórico sem o motivo) |
| MB3 | um erro de JS na tela (Alpine, Livewire, plugin) impede a modal de abrir; todos os cenários do `04` continuam verdes | CT-B01, passos 5 e 9 |
| MB4 | a ação executa mas a tela não reflete a situação nova (falta o refresh do componente) | CT-B01, passo 8 |
| MB5 | o `->visible()` da ação usa uma cópia da regra que diverge da barreira do model — o gestor não encontra o botão | CT-B01, passo 4 |

---

## CT-B02 — a modal recusa o motivo em branco, na tela, sem perder o que foi escrito

**Por que browser e não Livewire**: o `04` já prova que o **domínio** recusa a justificativa vazia
(CT-09, chamando o model direto). O que ele **não** prova é que o usuário **vê** a recusa: a
mensagem de campo obrigatório dentro de uma modal do Filament é renderizada por Livewire+Alpine
depois do submit, com a modal permanecendo aberta. Uma implementação em que a modal **fecha** ao
falhar, ou em que a mensagem não aparece, é indistinguível de uma correta para qualquer teste de
componente — e é a diferença entre "o gestor corrige" e "o gestor acha que rejeitou".

Este é o **erro visível** que o teto do perfil `completo` reserva.

```gherkin
# language: pt
  Cenário: [CT-B02] a rejeição sem motivo é recusada na própria modal
    Dado uma solicitação de 3.200,50 da Solange aguardando o gestor Gustavo, na organização Acme
    Quando o Gustavo aciona "Rejeitar" e confirma com o motivo em branco
    Então a modal continua aberta, mostrando que o motivo é obrigatório
    E a situação da solicitação continua "Aguardando gestor"
    E o console do navegador não acusa erro de JavaScript
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar como o gestor | `$this->actingAs($gustavo);` | — |
| 2 | abrir a listagem | `visit("/app/{$acme->slug}/solicitacoes-de-compra")` | a linha da solicitação |
| 3 | acionar a rejeição | `->click('Rejeitar')` | a modal monta |
| 4 | submeter em branco | `->press('Rejeitar')` | — |
| 5 | **a recusa é visível** | `->assertSee('Motivo da rejeição')` **e** a mensagem de obrigatoriedade | a modal continua aberta |
| 6 | a situação na tela não mudou | `->assertSee('Aguardando gestor')` | badge inalterado |
| 7 | console | `->assertNoJavaScriptErrors();` | — |
| 8 | **âncora de não-efeito** | `expect($solicitacao->fresh()->situacao)->toBe(SituacaoSolicitacao::AguardandoGestor);` e o histórico ainda **sem** nenhuma decisão | — |

**A âncora de não-efeito é obrigatória** (passo 8): "a modal continua aberta" sozinho passaria com
uma implementação que **grava a rejeição** e ainda assim mostra o erro. Cenário de recusa afirma o
não-efeito.

**O texto exato da mensagem de obrigatoriedade** vem do `laravel-lang/common` e não do requisito —
por isso o passo 5 assere a permanência da modal (`Motivo da rejeição` ainda na tela) **e** a
mensagem, mas o oráculo do cenário é o par "modal aberta + nada gravado", não a string.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB6 | a modal fecha ao falhar a validação e o gestor não vê motivo nenhum | CT-B02, passo 5 |
| MB7 | a validação vive só no model: a modal fecha, estoura exceção e a tela mostra erro genérico | CT-B02, passos 5 e 7 |
| MB8 | o `->required()` do `Textarea` foi esquecido; a rejeição é gravada com motivo vazio | CT-B02, passo 8 |
| MB9 | a rejeição é gravada **antes** da validação e depois "desfeita" só na tela | CT-B02, passo 8 (histórico sem decisão) |

---

## Cogitado e Cortado

O gate do browser é generoso e o teto é apertado. Sem esta tabela, "só há 2 CT-B" é
indistinguível de "só pensamos em 2".

| Cenário cogitado | Por que foi cortado |
|---|---|
| o fluxo inteiro entre três personas no navegador (Solange envia → Gustavo aprova → Diana aprova) | já provado por CT-06 e pelos Esquemas de CT-25, mais baratos em ordens de magnitude. O navegador não acrescentaria oráculo nenhum — nenhum passo depende de JS que o `callAction` não exercite |
| o solicitante **não** encontra os botões Aprovar/Rejeitar | é `assertActionHidden` — componente Livewire, milissegundos, sem Node. Está no `04` como CT-33 |
| a listagem abre sem erro de JavaScript | `visit([...])` em lote já é o padrão do kit em `tests/Browser/TelasDoKitTest.php`; acrescentar as duas rotas novas **àquele** arquivo é mais barato que um CT-B próprio — e `visit([...])` aborta na primeira falha, então um cenário por painel continua sendo a regra. **Recomendado como uma linha lá, não como CT-B aqui** |
| a modal de confirmação de "Enviar" e "Cancelar" | `requiresConfirmation()` é modal nativa do Filament, sem `->schema()` e sem campo — o mesmo mutante que ela mataria (a modal não abre) já é morto por CT-B01, que exercita a mesma mecânica de modal na mesma tela |
| o histórico do infolist renderizado no navegador (`RepeatableEntry`) | mata o mesmo mutante que CT-29 (componente). O `RepeatableEntry` de infolist é renderização Blade, não Alpine |
| tema escuro nas telas novas | `tests/Browser/TemaEscuroTest.php` já cobre o painel; e `assertSee` **não valida tema** — passa com texto branco em fundo branco. Defeito de cor não tem saída barata, e o card não pede nada de cor |
| acessibilidade das telas novas | não pedido pelo card e não coberto por regra nenhuma do `04`. Candidato legítimo a uma auditoria própria, **fora** desta entrega |

---

## Loop de execução (step 7 da `feature-wiki`)

A **especificação** destes dois CT-B é deste arquivo. A **execução** contra a UI real é do step 7
da `feature-wiki`, delegada a sub-agente. O contrato relevante para quem os materializar:

1. Escrever `tests/BrowserTenancy/Compras/RejeicaoNaTelaTest.php`
2. Rodar `vendor/bin/pest --testsuite=Browser` — **nunca** com `--parallel`
3. Falhou? **classificar a causa antes de mexer em qualquer coisa**:
   - **(a)** CT-B especificado errado (seletor, rota, texto) → corrigir **este arquivo**
   - **(b)** implementação divergente do PRD → **não corrigir**; registrar a divergência
   - **(c)** flake de timing → rever a estratégia de espera (estado final visível, nunca `wait(n)`)
4. Máximo 3 iterações. Vermelho por causa **(b)** é resultado válido — é a divergência que se
   queria capturar. Sub-agente que "conserta" a aplicação para ficar verde destrói o instrumento.

**Proibido**: alterar código de aplicação para o teste passar; relaxar assertion; remover CT-B que
não passou.

O seletor do campo da justificativa (`#mountedActionsData\.0\.justificativa`) é o candidato nº 1 a
causa **(a)** na primeira execução — ele é o `id` que o Filament gera, e o caminho depende de a
ação estar montada na tabela ou na página.

---

## Roteiro de Validação: Desenhado × Implementado

> Preenchido no step 7 da `feature-wiki`, rodando os CT-B contra a tela real. Divergências vão
> para "Desvios do Plano" no `03-progresso.md`.

| # | O que o PRD desenhou (`## Superfície de UI`) | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | listagem com a situação em badge e as ações Enviar / Aprovar / Rejeitar / Cancelar | | | |
| 2 | formulário de criação e edição com descrição, valor e centro de custo | | | |
| 3 | página de visualização com situação + histórico (quem decidiu, quando, por quê) | | | |
| 4 | modal "Rejeitar" com a justificativa obrigatória | | | CT-B01, CT-B02 |
| 5 | modais de confirmação de "Enviar" e "Cancelar" | | | |
| 6 | tela de centros de custo com a escolha do gestor | | | |
