# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Runtime: `pest-plugin-browser` ^5.0 (Playwright). **O plugin sobe o próprio servidor** — HTTP
> in-process, porta aleatória. Nada de Herd, `artisan serve`, Sail ou `APP_URL`.
> Comando: `composer test:browser` (embute o `npm run build`) ou
> `vendor/bin/pest --testsuite=Browser` — **em série, nunca `--parallel`**.
> Backend e derivação completa: `04-casos-de-teste.md`.

## Por que este arquivo existe — o gate, aplicado

A tabela `## Superfície de UI` do PRD tem 6 linhas, todas com `Depende de JS? = Sim`. Isso é o
**gatilho**, não o critério. O critério é outro: *o cenário afirma sobre algo que só o navegador
prova?*

Aplicado linha a linha, o resultado é quase todo negativo — e isso é o resultado certo:

| Linha da `## Superfície de UI` | Vai para o browser? | Onde é provado |
|---|---|---|
| Listagem com badge de situação | **não** | teste de componente Livewire — CT-35 |
| Formulário create/edit | **não** | componente: `fillForm` → `create`/`save` — CT-01, CT-05 |
| Tela de visualização (histórico) | **não** | componente — CT-36..CT-39 |
| Ações Enviar / Aprovar / Cancelar (`requiresConfirmation`) | **não** | componente: `callAction(TestAction::…)` — CT-10, CT-18, CT-32 |
| Visibilidade condicional das ações | **não** | componente: ação ausente para quem não decide — CT-21 |
| **Modal "Rejeitar" com formulário dentro** | **sim** | CT-B01, CT-B02 |
| Cadastro de centro de custo | **não** | componente — CT-44, CT-45, CT-47 |

**Só a modal de rejeição sobrou**, e a razão é específica: `callAction(TestAction::make('rejeitar'),
['justificativa' => …])` **injeta os dados direto no ciclo do Livewire e nunca renderiza a modal**.
Ou seja, o cenário mais barato prova que a ação funciona quando recebe a justificativa — e não prova
nada sobre a modal abrir, o `<textarea>` existir e o botão de confirmação submeter. Esse par é
Alpine + Livewire executando de verdade, e é a única afirmação deste requisito que o componente não
alcança.

RQ-07 ("na rejeição a justificativa é obrigatória") é a única cláusula do card cuja entrega ao
usuário passa obrigatoriamente por uma **modal com campo**. Se ela não abrir, RQ-06 e RQ-07 estão
inacessíveis com todo o backend verde.

**Teto do perfil `completo`**: 1 happy path + 1 erro visível = **2 CT-B**. É o que há aqui.

---

## Pré-requisitos

- [ ] `npm run build` executado — sem `public/build/manifest.json` **toda** tela responde
      `ViteException` e o cenário falha por um motivo que não é o dele. `composer test:browser` já
      embute o build.
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por `$this->actingAs($user)` **antes** do `visit()` — o servidor roda
      in-process, então sessão, `RefreshDatabase` e `:memory:` continuam valendo dentro do
      navegador. Login pela tela custa ~20 s por cenário e **não é o que estes cenários afirmam**.
- [ ] Suíte: `tests/Browser/Compras/RejeicaoTest.php` — pasta `Browser`, ligada a `TestCase` +
      `RefreshDatabase` + grupo `browser` (`tests/Pest.php:101-104`), já varrida pelo
      `phpunit.xml`. **Nenhuma infra nova é necessária para estes dois cenários** — eles não
      precisam de tenancy, o que é deliberado: `tests/BrowserTenancy` existe, mas atravessar
      `/app/{tenant}` acrescentaria uma variável que nenhum dos dois afirma.
- [ ] Seeders no `beforeEach`: `ShieldPermissionsSeeder` → `PapeisSeeder`, nessa ordem. Sem eles a
      tela responde 403 e o cenário mede a permission, não a modal.

## Seletores

O kit **não tem `data-testid`** — dívida conhecida e registrada em `.ai/rules/testes-browser.md`.
O disponível é o texto traduzido e o `id` gerado pelo Filament.

| Elemento | Seletor | Já existe? |
|---|---|---|
| Ação "Rejeitar" na linha da tabela | texto visível `Rejeitar` | **não** — nasce com esta feature (passo 9 do PRD) |
| Campo da justificativa dentro da modal | `#mountedActionsData\.0\.justificativa` — `id` gerado pelo Filament para o schema de uma ação montada; o `.` precisa de escape em CSS | **não** — nasce com esta feature |
| Botão de confirmação da modal | texto visível `Rejeitar` (rótulo do submit da modal) | **não** — ⚠️ **colide com o rótulo da ação na linha**, ver abaixo |
| Rótulo da situação na linha | texto visível `Rascunho` / `Aguardando gestor` | **não** |

> **Colisão de rótulo — a armadilha destes dois cenários.** O PRD dá à ação da linha o rótulo
> `Rejeitar` **e** ao botão de submit da modal o rótulo `Rejeitar`
> (`modalSubmitActionLabel('Rejeitar')`). Depois que a modal abre, existem **dois elementos com o
> mesmo texto** na página, e um `press('Rejeitar')` cru pode resolver para o errado — o sintoma
> seria a modal reabrindo em vez de submeter, com o teste falhando por um motivo que não é o dele.
>
> Ordem de tratamento, e nesta ordem: **(1)** escopar o clique ao contêiner da modal (o submit vive
> dentro dela, a ação da linha não); **(2)** se o plugin não oferecer escopo suficiente, um
> `data-testid` no submit resolve de vez. **(3)** Renomear o rótulo da modal para desempatar é a
> saída que **não** se toma sem falar com quem escreveu o PRD: o texto da tela é decisão dele, e
> mudá-lo para o teste passar é o teste dirigindo o produto.
>
> **Dívida a registrar no `03-progresso.md`**: o seletor do campo depende do `id` que o Filament
> gera para o schema da ação montada. Se ele divergir na implementação, a correção é do **CT-B**
> (causa (a) do loop), nunca da aplicação. Um `data-testid` no `Textarea` da justificativa e outro
> no submit eliminariam as duas dependências — proposta, não pré-requisito.

---

## CT-B01: o gestor rejeita pela modal e a solicitação volta para rascunho

**Por que browser e não Livewire**: a asserção é sobre **a modal abrir e submeter** — Alpine
montando o overlay, o `<textarea>` sendo renderizado dentro dele e o submit disparando a ação. O
teste de componente (`callAction` com o array de dados) entrega a justificativa por dentro e
**pula a modal inteira**: ele ficaria verde com a modal que não abre. É o único ponto desta feature
em que o caminho do usuário e o caminho do teste barato divergem.

```gherkin
# language: pt
  Cenário: [CT-B01] o gestor rejeita a solicitação escrevendo o motivo na modal
    Dado uma solicitação de valor 8.000,00 aguardando a decisão da gestora Beatriz
    E a Beatriz autenticada na listagem de solicitações
    Quando ela aciona "Rejeitar", escreve "Sem verba neste trimestre" e confirma
    Então a linha daquela solicitação passa a mostrar "Rascunho" e deixa de mostrar
      "Aguardando gestor"
    E a solicitação registrada está em rascunho, com uma etapa rejeitada pela Beatriz e a
      justificativa "Sem verba neste trimestre"
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar como a gestora e abrir a listagem | `$this->actingAs($gestora);` → `visit('/app/solicitacoes-de-compra')` | a linha da solicitação, com "Aguardando gestor" |
| 2 | acionar a rejeição | `->click('Rejeitar')` | a modal abre |
| 3 | conferir que a modal renderizou de verdade | `->assertSee('Rejeitar solicitação')` | título da modal |
| 4 | escrever o motivo | `->type('#mountedActionsData\\.0\\.justificativa', 'Sem verba neste trimestre')` | texto no campo |
| 5 | confirmar | `->press('Rejeitar')` | a modal fecha |
| 6 | oráculo visível, ancorado | `->assertSee('Rascunho')->assertDontSee('Aguardando gestor')` | a situação **daquela linha** mudou |
| 7 | console | `->assertNoJavaScriptErrors()` | apoio, nunca oráculo único |
| 8 | oráculo persistido, ancorado na solicitação | `$this->assertDatabaseHas('etapas_aprovacao_compra', ['solicitacao_compra_id' => $s->id, 'decisao' => 'rejeitada', 'decidido_por_id' => $gestora->id, 'justificativa' => 'Sem verba neste trimestre']);` **e** `expect($s->etapas()->count())->toBe(1);` | a decisão foi gravada com **quem**, **por quê** e **em qual solicitação** — uma só vez |

**Assertions**: sem navegação de página (a modal é in-place), então **não há `assertPathIs` a fazer
aqui** — o que espera é o `assertSee('Rascunho')`, que o plugin reexecuta até o teto de
`pest()->browser()->timeout()` (20 s, `tests/Pest.php:155`). **Nunca `wait($segundos)`**;
`waitForText` e `waitForSelector` não existem neste plugin.

`assertNoJavaScriptErrors()` e **não** `assertNoSmoke()`: a listagem é uma tela do Filament, e o
`assertNoSmoke` deixaria a suíte vermelha por `console.log` de plugin de terceiro
(`.ai/rules/testes-browser.md`).

**Âncora de persistência com quatro campos e uma contagem, não com a chave**: `assertDatabaseHas`
só com o `id` da etapa passaria com a decisão, o decisor e a justificativa todos errados. E a
segunda rodada da revisão adversarial apontou o que faltava: **sem `solicitacao_compra_id` e sem a
contagem**, uma etapa duplicada — ou gravada na solicitação errada, num banco com dois registros —
passa. O `04` exige *"o número de etapas **daquela** solicitação"* em toda parte; este arquivo não
seguia a própria regra.

> **Correção da revisão adversarial.** O passo 6 era um `assertSee('Rascunho')` solto — e a
> listagem do Filament tende a ter **filtro e legenda de situação com os mesmos rótulos**, de modo
> que o texto pode estar na página sem estar na linha do registro. Com **uma única solicitação em
> banco** (que é o setup deste cenário), o par `assertSee('Rascunho')` +
> `assertDontSee('Aguardando gestor')` volta a discriminar: a situação antiga tem de **sumir** da
> tela. Se a implementação vier com um filtro cujo rótulo contenha "Aguardando gestor" de forma
> permanente, o `assertDontSee` fica impossível — e aí a saída é ancorar a assertion à linha
> (`data-testid` no badge), **nunca** relaxar o oráculo de volta ao `assertSee` sozinho.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB1 | a ação de rejeitar é declarada com `requiresConfirmation()` em vez do schema com campo — a modal abre, mas **não tem onde escrever o motivo** | CT-B01 (passo 4 falha: o campo não existe) |
| MB2 | o campo é declarado no schema mas o valor não chega à ação, e a rejeição grava justificativa vazia | CT-B01 (a âncora afirma o **texto** gravado) |
| MB3 | a modal não abre — erro de JS, Alpine não inicializado, ação sem `->schema()` registrada | CT-B01 (passo 2/3) |
| MB4 | a rejeição funciona e a listagem não reflete a nova situação sem recarregar a página | CT-B01 (passo 6, dentro do mesmo ciclo Livewire) |

---

## CT-B02: a modal recusa a rejeição sem motivo, e a solicitação não se move

**Por que browser e não Livewire**: é o **erro visível dentro da modal**. `assertHasFormErrors`
num teste de componente prova que a validação existe no schema; não prova que a mensagem aparece
para quem está com a modal aberta, nem que a modal **permanece aberta** em vez de fechar engolindo
o erro. Este é o cenário de erro visível que o teto do perfil `completo` reserva.

```gherkin
# language: pt
  Cenário: [CT-B02] confirmar a rejeição sem escrever o motivo não rejeita nada
    Dado uma solicitação de valor 8.000,00 aguardando a decisão da gestora Beatriz
    E a Beatriz com a modal de rejeição aberta
    Quando ela confirma sem escrever nenhum motivo
    Então a modal continua aberta, apontando o campo obrigatório
    E a solicitação continua aguardando a decisão do gestor, sem nenhuma etapa registrada
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | autenticar e abrir a listagem | `$this->actingAs($gestora);` → `visit('/app/solicitacoes-de-compra')` | a linha da solicitação |
| 2 | abrir a modal | `->click('Rejeitar')->assertSee('Rejeitar solicitação')` | modal aberta |
| 3 | confirmar sem preencher | `->press('Rejeitar')` | — |
| 4 | o erro aparece **na tela** | `->assertSee('É obrigatória a indicação de um valor')` | mensagem de validação. **String confirmada em `lang/pt_BR/validation.php:135`** (`'required' => 'É obrigatória a indicação de um valor para o campo :attribute.'`), não escrita de memória. O trecho é parcial de propósito: o `:attribute` interpolado depende do rótulo do campo, e fixar a frase inteira faria o CT-B quebrar ao se renomear o rótulo — o que não é o defeito que ele procura |
| 5 | a modal **continua montada** | `->assertPresent('#mountedActionsData\\.0\\.justificativa')` | oráculo **estrutural**, não textual: o campo da ação montada ainda está no DOM |
| 6 | console | `->assertNoJavaScriptErrors()` | apoio |
| 7 | oráculo do não-efeito | `expect($solicitacao->fresh()->situacao)->toBe(SituacaoSolicitacao::AguardandoGestor);` e `$this->assertDatabaseCount('etapas_aprovacao_compra', 0);` | nada se moveu |

> **O passo 7 é o que faz este cenário valer.** Sem ele, CT-B02 seria um `assertSee` de mensagem —
> e uma implementação que mostra o erro **e mesmo assim grava** passaria. Cenário de recusa afirma
> o não-efeito, sempre.

> **Correção da revisão adversarial no passo 5.** Ele era `assertSee('Rejeitar solicitação')` — ou
> seja, o **mesmo texto** do passo 2, e um título de modal genérico o satisfaz. Pior: é string de
> i18n, então uma mudança de tradução deixaria o CT-B vermelho **sem defeito nenhum**. A afirmação
> real é *"a modal continua montada"*, e o que prova isso é a presença do campo da ação montada no
> DOM — estrutura, não texto. O passo 4 continua textual porque ali o texto **é** o que se afirma
> (a mensagem de erro chegou ao usuário), e a string está confirmada no `lang/` do projeto.
>
> **`assertPresent` existe no plugin instalado** — confirmado em
> `vendor/pestphp/pest-plugin-browser/src/Api/Concerns/MakesElementAssertions.php:510`, ao lado de
> `assertVisible` (`:498`) e `assertMissing` (`:532`). Não foi escrito de memória. Se a modal
> renderizar o campo oculto em vez de removê-lo, o par certo é `assertVisible`/`assertMissing` —
> **nunca** o retorno ao `assertSee` do título.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| MB5 | o campo da justificativa não é obrigatório no schema — a modal submete vazia e a rejeição acontece | CT-B02 (passos 4 e 7) |
| MB6 | a validação existe, a modal fecha e o erro aparece como notificação que some — o usuário perde o texto que já tinha digitado | CT-B02 (passo 5) |
| MB7 | a validação é só do formulário e a solicitação é rejeitada mesmo assim (ordem invertida: grava e depois valida) | CT-B02 (passo 7) |

---

## Cogitado e Cortado

O gate do `05` é generoso e o teto é apertado. Sem esta tabela, "só há 2 CT-B" é indistinguível de
"só pensamos em 2".

| Cenário cogitado | Por que foi cortado |
|---|---|
| O fluxo inteiro entre três personas (solicitante envia → gestor aprova → diretor aprova) no navegador | provado mais barato por CT-10, CT-14 e CT-17. Atravessar três logins no browser custa dezenas de segundos e não acrescenta nenhuma afirmação sobre JS |
| A ação "Aprovar" com `requiresConfirmation()` | a modal de confirmação é componente nativo do Filament, sem campo e sem lógica própria. Mata o mesmo mutante que CT-18, mais caro |
| As ações **não aparecerem** para quem não pode decidir | `assertActionHidden` / ação ausente por componente resolve (CT-21). Provar ausência no DOM é o caso em que o browser é mais frágil, não mais forte |
| A **cor** do badge de situação (verde para aprovada, vermelho para cancelada) | `assertSee` **não valida cor** — passa com texto branco em fundo branco. Provar exige screenshot e olho humano, e **a cor não é cláusula do requisito**. Lacuna declarada, não cortada por descuido |
| Acessibilidade da modal (foco preso, `aria-*`, fechar com Esc) | `assertNoAccessibilityIssues()` existe e seria um bom cenário — mas nenhuma cláusula do `00-requisito.md` fala de acessibilidade. Candidato a rule de projeto, não a CT desta feature |
| Tela em modo escuro | mesma razão: nenhuma cláusula. E `->inDarkMode()->assertSee('…')` prova que a tela abre, nada sobre legibilidade |
| Formulário de criação da solicitação no navegador | é tela de escrita, e o gate dela é cumprido por componente (CT-01). Nenhuma afirmação de JS ali |
| Login pela tela para chegar a cada persona | `actingAs()` resolve; o kit já tem um cenário dedicado ao formulário de login (`tests/Browser/`), e duplicá-lo aqui custaria ~20 s por cenário sem provar nada novo |

---

## Roteiro de Validação: Desenhado × Implementado

Preenchido **no step 7 da `feature-wiki`**, depois de rodar os CT-B contra a UI real. Divergência
entre o desenhado e o implementado vai para "Desvios do Plano" no `03-progresso.md` — e **não** se
conserta calando o CT-B.

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | Listagem com a situação em badge e as ações Enviar/Aprovar/Rejeitar/Cancelar | | | |
| 2 | Modal "Rejeitar" com `Textarea` obrigatório de justificativa | | | |
| 3 | Modal "Enviar" / "Cancelar" com confirmação | | | |
| 4 | Formulário de criação com descrição, valor (prefixo R$) e centro de custo | | | |
| 5 | Tela de visualização com situação + histórico de etapas | | | |
| 6 | Cadastro de centro de custo com seleção de gestor | | | |

**Regra do loop** (contrato do sub-agente da `feature-wiki`, step 7): ao falhar, classificar a
causa **antes** de mexer em qualquer coisa — (a) CT-B especificado errado → corrigir **aqui**;
(b) implementação divergente do PRD → **não corrigir**, registrar a divergência; (c) flake de
timing → rever a estratégia de espera. Máximo de 3 iterações. **Proibido** alterar código de
aplicação para o teste passar, relaxar assertion ou remover CT-B que não passou.
