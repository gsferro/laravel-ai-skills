# Correções factuais na feature-wiki v2.10.0

Cada linha abaixo é uma afirmação que a skill faz hoje e que está **errada ou desatualizada**.
Um agente que segue a skill produz plano/CT errado por causa delas.

## Browser (arquivo 05)

| Afirmação atual | Realidade verificada | Fonte |
|---|---|---|
| "Servidor: a doc não explicita se o plugin sobe o app ou exige servidor externo. Obriga a registrar no `05` como o projeto serve o app" + template com `App acessível em {APP_URL} — servido por: {Herd \| artisan serve \| Sail \| Vite}` | O plugin sobe **servidor HTTP próprio in-process (amphp), porta aleatória**. Nada de Herd/serve/Sail, nada de `APP_URL` a configurar | `.ai/rules/testes-browser.md:3-5` do starter-kit; doc do Pest: "the server binds to 127.0.0.1 for all browser tests" |
| "`actingAs()` em teste de browser **não** está documentado — não inventar" | Como é o **mesmo processo**, `$this->actingAs($user)` antes do `visit()` funciona e é o recomendado. Login pela UI custa ~20 s por cenário | `.ai/rules/testes-browser.md:7-10`; anúncio do Pest v4 mostra `actingAs()` |
| "o plugin expõe `wait(segundos)`; não há `waitFor(seletor)`" (deixa o agente achar que `wait()` é a saída) | O correto é **nunca usar `wait()`**. O plugin reexecuta cada assertion até `pest()->browser()->timeout()`. Espere pelo estado final visível | `.ai/rules/testes-browser.md:27`; doc do Pest (auto-wait, default 5 s) |
| — (ausente) | **`assertPathIs` antes das asserções de conteúdo.** Invertido, o `assertSee` roda contra o snapshot da página anterior e falha com a ação tendo funcionado | `.ai/rules/testes-browser.md:17-25` |
| "**Cuidado** com `--parallel` + CT-B" | **Nunca** `--parallel` com browser. Medido no kit: derruba 4 de 11 cenários. E `--tia` exige run completo (`--group` o desliga), então `--parallel --tia` e CT-B não convivem numa invocação | `.ai/rules/testes-browser.md:29-40` |
| "`assertNoSmoke()` em **todo** CT-B" | Só em tela de autoria própria. Em tela de plugin de terceiro use `assertNoJavaScriptErrors()`, senão a suíte fica vermelha por `console.log` alheio | `.ai/rules/testes-browser.md:58` |
| — (ausente) | `npm run build` é **pré-requisito duro**: sem `public/build/manifest.json` toda tela responde `ViteException` | `.ai/rules/testes-browser.md:13-15` |
| — (ausente) | `visit([...])` em lote **aborta na primeira falha** — as rotas seguintes não são verificadas naquele run | `.ai/rules/testes-browser.md:42-44` |
| Nome de API para upload | É `attach()`, não `upload()` | doc Pest browser-testing |

## Camada de teste (o buraco central do 04)

| Afirmação atual | Realidade verificada |
|---|---|
| O `04` é "100% backend (Feature/Unit)" e todo cenário de UI vai para o `05` (browser), com teto de 1 happy + 1 erro | Em Laravel+Filament, **~85% dos casos testáveis são teste de componente Livewire** — milissegundos, sem Node/Playwright, e cobrem validação de form, tabela, filtro, ação, notificação e autorização. Browser só se justifica quando a asserção depende de **JavaScript executado, pixel ou acessibilidade** |
| — (ausente) | Regra do projeto: **"uma tela aberta não é uma tela que grava"** — `GET /admin/users` seguiu verde com o salvamento quebrado. Cobrir em par: a visita **e** a gravação por componente |

## APIs do Filament que a skill levaria o agente a escrever erradas

| Skill induz | Correto em Filament 4/5 |
|---|---|
| (genérico "componente de UI") | `livewire(ListUsers::class)`, `fillForm([...])`, `assertHasFormErrors([...])`, `assertSchemaStateSet([...])`, `assertCanSeeTableRecords([...])`, `searchTable`, `sortTable`, `filterTable`, `assertNotified()` |
| `callTableAction` / `assertTableActionExists` (padrão v2/v3 que a doc antiga espalha) | `callAction(TestAction::make(CreateAction::class)->table(), [...])` com `Filament\Actions\Testing\TestAction` |
| `assertFormSet` (v3) | `assertSchemaStateSet` (v4/v5) |
| — | Autorização em Filament **não é documentada** pelo Filament; o caminho real é `livewire(...)->assertForbidden()` (helper do Livewire) ou `$this->actingAs($u)->get(Resource::getUrl('index'))->assertForbidden()` |

## Armadilhas de fake/mocking que o `04` deveria carregar e não carrega

| Armadilha | Consequência se ignorada |
|---|---|
| `Mail::assertSent` **nunca** passa para mailable `ShouldQueue` — é `assertQueued` | CT escrito, teste vermelho sem defeito no código |
| `Event::fake()` **depois** das factories, senão eventos de model (uuid em `creating`) não rodam | fixture nasce quebrada |
| `Http::fake()` sem stub devolve 200 vazio → teste passa sem provar nada. Use `Http::preventStrayRequests()` | falsa cobertura |
| `withoutExceptionHandling()` transforma 403/404/422 em exceção → `assertForbidden()` nunca roda | CT de autorização inútil |
| `RefreshDatabase` roda tudo em transação → job com `->afterCommit()` **não despacha** | CT de fila falha sem defeito |
| `travel()` sem `travelBack()`/closure vaza para os testes seguintes | flake em `--parallel` |
| `Repeater::fake()` / `Builder::fake()` no Filament, senão UUID aleatório quebra `assertSchemaStateSet` | flake |
| `Log::spy()` **não** é API documentada — é o mecanismo genérico de Facade Spy | citar como padrão derivado, não como doc |

## Mutation testing — disponível e não usado

`pestphp/pest-plugin-mutate` está instalado no starter-kit. `vendor/bin/pest --mutate` existe, com
`--min`, `--covered-only`, `--class`, `--bail`. Exige `covers()` ou `mutates()` no arquivo de teste,
e driver de cobertura. **`pest()->mutate()` em `Pest.php` NÃO existe** — a skill não deve inventá-lo.

É a única ferramenta do ecossistema que responde objetivamente à pergunta do usuário
("meus testes pegam defeito?"), e a skill hoje só a cita de passagem numa tabela.
