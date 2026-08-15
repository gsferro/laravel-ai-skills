# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> ela não existe: nenhuma das três tabelas, nenhum dos dois Resources e nenhum dos models
> desta feature estão no repositório no momento desta derivação.
>
> **Versão 3** — incorpora as **duas** rodadas da revisão adversarial (ver `## Revisão Adversarial`).
> A rodada 2 trouxe um **achado estrutural**, e por isso R3 virou duas regras (R3 e **R13**). O
> teto de 2 rodadas foi atingido: não há rodada 3 — ver `## Escalada`.

## Numeração dos cenários — leia antes de procurar um ID

O `01-plano-acao.md` é **imutável** e já cita oito casos por número: `CT-04` (borda do limite),
`CT-08` (reenvio preserva o histórico), `CT-11` (barreira chamada direto), `CT-12` (corrida),
`CT-13` (centro sem gestor), `CT-14` (subtração do `panel_user`), `CT-17` (papel `diretor` no
contexto certo) e `CT-18` (regressão da matriz de painéis). Esses oito IDs foram **honrados**.

O preço é que a numeração **não é contígua por regra**: a rodada 1 da revisão adversarial
acrescentou `CT-34`…`CT-44`, a rodada 2 acrescentou `CT-45`…`CT-47` e **retirou `CT-43`**, e
`CT-15` está desdobrado em `CT-15a`/`CT-15b`. **O `## Índice de Cenários` é a autoridade**, não a
ordem de leitura. ID retirado **não é reaproveitado**.

---

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| Máquina de estados (enviar, aprovar, rejeitar, cancelar, terminalidade) | 3 | 3 | **9** | **completo** |
| Alçada por valor (o limite de R$ 5.000 e a ordem gestor → diretor) | 3 | 3 | **9** | **completo** |
| Autorização — quem decide a etapa, e quem cadastra centro de custo | 3 | 3 | **9** | **completo** |
| Isolamento por organização | 3 | 3 | **9** | **completo** |
| Gravação da solicitação (criação e edição em rascunho) | 2 | 3 | 6 | padrão |
| Cadastro de centro de custo (o campo `gestor_id`) | 2 | 3 | 6 | padrão |
| Notificação por e-mail do próximo aprovador | 2 | 2 | 4 | padrão |
| Exibição da situação e do histórico | 2 | 2 | 4 | padrão |

**Justificativa dos 9**: a feature decide **dinheiro** (impacto 3 por definição), tem **regra com
muitas condições** e **concorrência real** — dois diretores podem clicar "Aprovar" no mesmo
segundo — e a autorização é o par situação × identidade, que é irreversível quando erra. O
`00-requisito.md` → A-08 descreve uma **escalada de privilégio** explícita: quem edita
`centros_custo.gestor_id` se nomeia aprovador das próprias compras.

**Perfil da feature: `completo`** → revisão adversarial obrigatória, BVA 3-valores, 100% das
células inválidas da matriz de estados, 3 a 6 mutantes por regra.

- Técnicas aplicadas: **EP**, **BVA 3-valores** (incremento `0,01`, o do `decimal(12,2)`),
  **tabela de decisão**, **tabela estado × operação** (cartesiana fechada), **matriz persona ×
  verbo**, **matriz persona × tela**, **rastreio de efeito** (4 direções + **cardinalidade do
  destinatário**), **2-switch**, **concorrência por transição**, **normalização de texto**.
- **Pairwise: não aplicado** — nenhuma regra desta feature tem ≥3 parâmetros independentes. O
  fluxo é `situação × persona × valor`, e `valor` só entra por uma fronteira binária, que a tabela
  de decisão já fecha sem redutor combinatório.
- Cenários: **47** · Regras: **13** · Mutantes previstos: **81** · Sem matador: **0**
  (4 lacunas declaradas, todas com o que foi tentado)
- **A aritmética da contagem**, porque ela é o oráculo de si mesma: os IDs vão de `CT-01` a
  `CT-47` (47 números), **menos** `CT-43`, retirado por subsunção (46), **mais** o desdobramento de
  `CT-15` em `CT-15a`/`CT-15b` (47).

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | 3 tabelas (`centros_custo`, `solicitacoes_compra`, `etapas_aprovacao_compra`), 1 enum de 5 situações, 3 models, 2 policies, 1 notification, 2 Resources no painel `app`, 1 papel novo (`diretor`), 1 subtração no `PapeisSeeder`, 1 chave de config, 1 channel de log, 1 suíte de teste nova | CT-14, CT-18, CT-36 |
| **F**unction | criar, editar, excluir, enviar, aprovar, rejeitar, cancelar, exibir situação, exibir histórico, notificar. **Função administrativa escondida**: o cadastro de centro de custo, que define quem aprova | CT-01…CT-13, CT-22…CT-27, CT-39 |
| **D**ata | `descricao` (texto livre), `valor` (`decimal(12,2)` — a fronteira dos R$ 5.000), `centro_custo_id` (FK cujo `gestor_id` **pode ser nulo**), `situacao` (5 partições), `justificativa` (texto livre, obrigatória só na rejeição), **histórico multi-ciclo**, **dado de outra organização**, **cardinalidade de aprovadores (0/1/N)** | CT-02, CT-04, CT-09, CT-13, CT-28…CT-31, CT-34, CT-35, CT-37, CT-42 |
| **I**nterfaces | tela Filament (form, ações de tabela, modal com formulário, infolist), **o model chamado direto** (job, comando, seeder, rota de API futura — o chamador que a policy não vê), seeders de permissão, notification enfileirada | CT-03, CT-09, CT-11, CT-14, CT-22…CT-27, CT-31, CT-38, CT-39 |
| **P**latform | SQLite `:memory:` nos testes (`decimal` volta como **string**, e comparar `'5000.00' > 5000` em PHP é armadilha), Filament 5.6, Pest 5.1, `QUEUE_CONNECTION=sync` e `MAIL_MAILER=array` fixados no `phpunit.xml`, Playwright para os CT-B. **`tests/Unit` não tem `TestCase` ligado** — ver `## Setup Global` | CT-04, CT-19 |
| **O**perations | 6 personas reais (solicitante, gestor do centro, gestor de **outro** centro, diretor, usuário comum sem relação, admin da organização), **cada uma diante da tela e por fora dela**. **Uso indevido previsto**: aprovar a própria solicitação, se nomear gestor, decidir a etapa do outro, ler a solicitação do colega | CT-11, CT-14, CT-15, CT-32, CT-36, CT-39, CT-41 |
| **T**ime | **concorrência** nas **quatro** transições de decisão, **ordem** (o diretor só depois do gestor), **2-switch** (rejeitar → corrigir → reenviar), `updated_at` na transição, e a **data exibida** de cada etapa. **Timezone/DST: não se aplica** — nenhum campo desta feature tem prazo, validade, expiração ou agendamento; o único carimbo é `created_at` da etapa, exibido (CT-29, com o relógio congelado) e nunca comparado | CT-05, CT-08, CT-12, CT-21, CT-29, CT-40 |

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — a solicitação nasce em rascunho com descrição, valor e centro de custo, e o domínio de cada campo vale na criação **e** na edição | gravação (padrão) | RQ-01, RQ-02 | EP + BVA + mass assignment + normalização | CT-01, CT-02, CT-03, CT-37, CT-38 |
| **R2** — valor **acima** de R$ 5.000 exige o diretor, **depois** do gestor | alçada (completo) | RQ-05 | **BVA 3-valores** + sequência | CT-04, CT-05, CT-06 |
| **R3** — a rejeição exige justificativa e devolve a solicitação ao rascunho | estados (completo) | RQ-06, RQ-07, RQ-08 | EP | CT-09, CT-10 |
| **R13** — o reenvio reinicia o fluxo **a partir do gestor**, com a alçada recalculada pelo valor do momento, **qualquer que tenha sido a etapa que rejeitou** | estados + alçada (completo) | RQ-08, RQ-09, RQ-05 | **2-switch** + produto `etapa que rejeitou × direção do valor` | CT-07, CT-08, CT-45, CT-46 |
| **R4** — só o aprovador da etapa corrente decide, e isso vale para aprovar **e** para rejeitar | autorização (completo) | RQ-04, RQ-05, RQ-06 | matriz persona × verbo | CT-11, CT-32 |
| **R5** — duas decisões simultâneas produzem uma única etapa e uma única transição, **em qualquer das quatro transições de decisão** | estados (completo) | RQ-06 | concorrência × transição | CT-12, CT-40 |
| **R6** — sem aprovador para a etapa que vai ficar pendente, a transição é recusada e a solicitação fica onde está | estados (completo) | RQ-04 (`00` → A-10) | tabela de decisão + cardinalidade | CT-13, CT-35 |
| **R7** — o cadastro de centro de custo é administração da organização; o usuário comum não o alcança, **por nenhuma das operações nem por fora da tela** | autorização (completo) | RQ-04 (`00` → A-08) | matriz papel × **operação** + gate de camada | CT-14, CT-15a, CT-15b, CT-16, CT-39, CT-42, CT-47 |
| **R8** — cada transição que deixa uma etapa pendente notifica **por e-mail** **todos** os aprovadores dessa etapa, sobre **aquela** solicitação, uma vez, e ninguém mais | notificação (padrão) | RQ-14 | **rastreio de efeito** (4 direções) + **cardinalidade** | CT-17, CT-19, CT-20, CT-21, CT-34 |
| **R9** — as entidades e o papel novos entram na matriz do painel `app`, e o papel novo **alcança a tela** | autorização (completo) | RQ-04, RQ-05 | matriz papel × ação + **persona × tela** | CT-18, CT-36 |
| **R10** — cada operação só existe nas situações em que o requisito a autoriza | estados (completo) | RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-10, RQ-11 | **tabela estado × operação** | CT-22…CT-27, CT-44 |
| **R11** — a tela mostra a situação atual e quem decidiu cada etapa, para quem tem direito de ler | exibição (padrão) | RQ-12, RQ-13 | **EP exaustiva do enum** + persona | CT-28, CT-29, CT-33, CT-41 |
| **R12** — solicitação de outra organização é invisível e intocável | isolamento (completo) | — (taxonomia: IDOR) | IDOR / autorização horizontal | CT-30, CT-31 |

**Técnica escalada acima do perfil da área** — três, cada uma com motivo:

1. **R1 é área `padrão` e recebeu BVA** na fronteira inferior do valor (CT-02, CT-37). EP sozinha
   não distingue "recusa negativo" de "recusa ≤ 0", e é o campo que decide alçada.
2. **R1 recebeu também normalização de texto** (CT-02 e CT-37, linha `"   "`). Sem ela, `required`
   do Laravel aceita uma descrição que é só espaço em branco.
3. **R8 é área `padrão` e recebeu as 4 direções do rastreio de efeito + a partição de
   cardinalidade** (0 / 1 / N destinatários). Motivo: o card diz "**o** próximo aprovador", no
   singular, e o `00` → A-03 diz que a etapa do diretor tem **N** destinatários. O singular do
   card é a leitura que um dev competente faria — e ela é o defeito.

**Toda cláusula `RQ` do `00` gerou regra**: RQ-01→R1 · RQ-02→R1/R10 · RQ-03→R10 ·
RQ-04→R4/R6/R7/R9 · RQ-05→R2/R4/R9/**R13** · RQ-06→R3/R4/R5 · RQ-07→R3 · RQ-08→R3/**R13** ·
RQ-09→**R13** · RQ-10→R10 · RQ-11→R10 · RQ-12→R11 · RQ-13→R11 · RQ-14→R8.

> **RQ-09 era a cláusula sem dono**, e foi isso que a rodada 2 achou. Na v2 ela aparecia repartida
> entre R2 (*"a alçada é reavaliada"*) e R3 (*"o histórico sobrevive"*), e **cada uma derivava o
> reenvio a partir do único ponto de rejeição que ela conhecia — o gestor**. Ninguém era dono da
> pergunta inteira, e por isso o produto `{quem rejeitou} × {direção da mudança de valor}` nunca
> foi montado: das 4 células, a v2 executava **uma**. R13 existe para ter esse dono.

---

## Fronteira com o Plano

O `01-plano-acao.md` entrou aqui **apenas** para paths, rotas, nomes de tela e a tabela
`## Superfície de UI`. O que ele determina e o requisito não determina foi **recusado como
oráculo** — o cenário pode usá-lo como detalhe, nunca como `Então`.

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| Enum `SituacaoSolicitacao` e os valores `aguardando_gestor` / `aguardando_diretor` | escolha de implementação. O requisito nomeia **duas** situações: "rascunho" e "aprovada" | detalhe do cenário — os `Então` falam da **situação observável** |
| Nomes dos métodos `enviar()`, `aprovar()`, `rejeitar()`, `cancelar()`, `exigirAprovador()` | escolha de implementação | detalhe do roteiro, nunca `Então` |
| `config('kit.compras.limite_diretor')` — **onde** o número mora | escolha de implementação | detalhe. **O número R$ 5.000 é cláusula do requisito**, e CT-04 o usa **literal** |
| Tabela `etapas_aprovacao_compra` append-only | mecanismo (ADR-03). O requisito pede "quem aprovou cada etapa", não uma tabela | os `Então` de CT-08 e CT-29 afirmam o **histórico observável**, não a linha da tabela |
| Papel spatie `diretor` × FK `diretor_id` | mecanismo (`00` → A-03) | detalhe. CT-11, CT-17, CT-34 e CT-36 falam de "pessoas com autoridade de diretor" |
| `UPDATE … WHERE situacao = <esperada>` | escolha de implementação (ADR-09) | detalhe de CT-12 e CT-40. O `Então` é sobre **uma etapa e uma transição** |
| `varchar(255)` da descrição | número **do plano**, não do requisito | ⚠️ **lacuna declarada** — A-18 |
| Texto `"Esta solicitação já mudou de situação. Recarregue a tela."` | comportamento **visível ao usuário** que só o PRD determina | ⚠️ **pergunta** — A-16 |
| `Log::channel('compras')` com `motivo` no context, e a regra LGPD de mascaramento | o card **não pede log nenhum** | **nenhum CT de log neste conjunto.** Ver a nota abaixo |
| `BelongsToTenant` / isolamento por organização | o card não menciona organização | R12 existe, com origem declarada **taxonomia (IDOR)**, não `RQ` |
| `->money('BRL')`, badge com `HasColor`, `RepeatableEntry` | escolha de implementação | detalhe. CT-28 afirma o **rótulo da situação na linha do registro**, não o componente |

> **Por que não há CT de log.** O requisito FERRO-830 não menciona log em lugar nenhum, então um
> `Então o log registra …` seria o conjunto testando o **plano**. Se o time quiser log como
> requisito verificável, ele precisa virar cláusula no `00` — e aí ganha rastreio de efeito, como
> a notificação (R8) ganhou.

**Perguntas em aberto** — ver `## Perguntas para o 00-requisito.md`, no fim deste arquivo.

---

## Setup Global

### Personas — nove pessoas distintas, e a distinção é o ponto

Persona colapsada (o mesmo usuário sendo dono, aprovador e chamador) faz **toda** barreira de
identidade passar com a autorização removida.

| Persona | Quem é | Como criar (helper real do projeto, `tests/Pest.php`) |
|---|---|---|
| **Solange** | a solicitante | `usuarioComPapel('panel_user', $acme, 'solange@example.com')` |
| **Gustavo** | gestor do centro de custo **TI** | `usuarioComPapel('panel_user', $acme, …)` + `centros_custo.gestor_id` |
| **Gilda** | gestora de **outro** centro (Marketing) — prova que a autoridade é **por centro** | `usuarioComPapel('panel_user', $acme, …)` |
| **Diana** | diretora | `usuarioComPapel('diretor', $acme, …)` |
| **Dora** | **segunda** diretora — existe porque "o próximo aprovador" no singular do card é o defeito D1 | `usuarioComPapel('diretor', $acme, …)` |
| **Otávio** | usuário comum sem relação nenhuma com a solicitação | `usuarioComPapel('panel_user', $acme, …)` |
| **Alice** | administradora da organização **Acme** | `usuarioComPapel('admin_organizacao', $acme, …)` |
| **Bianca** | administradora da organização **Globex** — existe porque a Alice **não alcança** a Globex (CT-15b), e sem ela a linha discriminante de CT-42 seria inmaterializável | `usuarioComPapel('admin_organizacao', $globex, …)` |
| **Décio** | **diretor da Globex** — a persona estrangeira do **tipo certo**. Na v2 ele só aparecia como destinatário de e-mail; o único ator estrangeiro era o Gunther, que é *gestor*, e por isso a metade "diretor de outra organização" do IDOR ficava sem cenário | `usuarioComPapel('diretor', $globex, …)` |
| **Gunther** | gestor de um centro de custo da **Globex** | `usuarioComPapel('panel_user', $globex, …)` + `gestor_id` |

`usuarioComPapel()`, `papelNaOrganizacao()`, `noPainelDa()`, `tenant()` e `usuarioCom()` já existem
em `tests/Pest.php` (linhas 185-353) — **confirmados por leitura**, nenhum inventado. Helper novo
desta feature vai para `tests/Pest.php` e não para o arquivo de teste (`.ai/rules/testes.md`,
enforçado por `tests/Kit/HelpersDeTesteTest.php`).

### Fixtures — **não há factory para nada desta feature**

`database/factories/` tem exatamente três arquivos: `ConviteFactory`, `TenantFactory`,
`UserFactory`. **Não existe `CentroCustoFactory` nem `SolicitacaoCompraFactory`**, e o kit sequer
tem `ProjetoFactory` — o precedente do projeto é criar por `Model::create([...])`.

| Fixture | Como criar |
|---|---|
| organização | `tenant('Acme', 'acme')` — helper existente |
| centro de custo | `CentroCusto::create(['nome' => 'TI', 'gestor_id' => $gustavo->id])` |
| centro **sem gestor** (CT-13) | `CentroCusto::create(['nome' => 'Compras', 'gestor_id' => null])` |
| solicitação em rascunho | `SolicitacaoCompra::create([...])` — **`situacao`, `solicitante_id` e `tenant_id` estão fora do `$fillable`** |
| solicitação num estado adiante | montada **pelas transições**, nunca por `update(['situacao' => …])` |

> **Fixtures e `$fillable`** — achado do arnês. `situacao`, `solicitante_id` e `tenant_id` estão
> fora do `$fillable` **de propósito** (é a defesa de CT-03). Consequência: `::create()` **não
> consegue** montar uma solicitação de outra pessoa nem num estado adiante. As duas saídas
> honestas são (a) uma factory com `forceFill`/`state` que grava as três colunas, declarada como
> fixture de teste; ou (b) montar pelo caminho real. **Preferir (b) sempre que o número de passos
> for ≤ 3**; cair em (a) para os estados terminais. Cravar o estado por `DB::table()->update()`
> está **proibido** aqui: cria estados que o sistema nunca produz.

### Fakes

- `Notification::fake()` em todo cenário de R8 e em **todo cenário que afirma não-efeito**
  (CT-13, CT-20, CT-21, CT-24, CT-35). O projeto usa `Notification::assertSentTo`,
  `assertNothingSent` e `assertSentOnDemandTimes` — confirmados em
  `tests/Kit/ConviteEmMassaTest.php`.
- **`Mail::fake()` não** — a notificação é `ShouldQueue` e o canal é `mail`; a asserção de canal
  **e de assunto** se faz no closure do `assertSentTo`. `Mail::assertSent` em mailable enfileirado
  **nunca passa** (armadilha catalogada).
- Sem `Queue::fake()`: o `phpunit.xml` já fixa `QUEUE_CONNECTION=sync` (linha 57).
- Sem `Http::fake()`: a feature não fala com serviço externo nenhum.
- **`freezeTime()`** em CT-29, que é o único cenário com oráculo sobre **data exibida** — e
  congelando um **instante no fuso da aplicação**, não um dia. Com o app em `America/Sao_Paulo` e
  `created_at` em UTC, congelar em "14/08" cairia em 15/08 se o instante escolhido fosse 23:00
  local. Achado da rodada 2 (L11): o *"timezone: não se aplica"* foi escrito antes de existir
  oráculo de data, e passou a valer só para **comparação**, nunca para **exibição**.

### Precondição de organização — o que o CT-35 passou a exigir de todo mundo

CT-35 institui **falha fechado sem nenhum diretor**. A partir dele, todo cenário com solicitação
**acima do limite** cuja transição deixa a etapa do diretor pendente depende de uma precondição que
antes era irrelevante: **existir ao menos uma pessoa com autoridade de diretor na organização**.

Sem isso, materializados ao pé da letra, `CT-04` (linha `5.000,01`), `CT-05`, `CT-06`, `CT-11`,
`CT-25` e `CT-40` produziriam uma organização sem diretor, a aprovação do gestor seria **recusada**,
e o cenário ficaria vermelho **pelo motivo errado** — ou alguém "consertaria" relaxando a asserção.
A linha `E que existe ao menos uma pessoa com autoridade de diretor na organização` foi acrescentada
ao `Dado` dos seis.

> É a superfície nova clássica: o cenário novo mudou o contrato dos antigos. Achado da rodada 2 (L5).

### Estratégia de DB e **suíte** — o achado de arnês mais importante deste conjunto

Três fatos do repositório, todos confirmados por leitura:

1. **`tests/Unit` não tem `TestCase` ligado.** `tests/Pest.php` liga `TestCase` a `Feature`,
   `Kit`, `Browser` e `TenancyTestCase` a `Tenancy`, `BrowserTenancy` (linhas 22-145). `Unit`
   **não aparece**. Um caso ali roda **sem container**: `config()`, cast de enum e Eloquent não
   resolvem. → **zero cenários alocados a `Unit`.** A camada mais barata que este arnês sustenta é
   `Feature`.
2. **`tenant_id` é NOT NULL, fica fora do `$fillable` e só é preenchido quando
   `Filament::getTenant()` devolve um `Tenant`** (`app/Traits/BelongsToTenant.php:72-78`). Sem
   organização no contexto, **toda fixture desta feature falha no insert**.
3. `noPainelDa()` fixa também o `setPermissionsTeamId`, que só tem sentido com
   `permission.teams` — decidida em `createApplication()`, antes das migrations
   (`tests/TestCase.php`). Quem a liga é `Tests\TenancyTestCase`.

**Conclusão, e ela diverge do PRD**: o passo 10 do `01-plano-acao.md` cria a suíte
`tests/FeatureTenancy` para **dois** casos. Pela leitura do arnês, **o conjunto inteiro pertence a
`tests/FeatureTenancy`** — o item 2 vale para toda fixture.

> **Isto é achado, não correção.** O `01` é imutável nesta entrega e não foi alterado.
> **O que foi tentado antes de concluir**: `Grep` por criação de model com `BelongsToTenant` em
> `tests/` (nenhum precedente — o kit não tem `ProjetoFactory` nem caso que crie `Projeto`);
> leitura de `ConviteFactory`, que grava `tenant_id` diretamente **porque `Convite` não usa a
> trait** e a coluna dele é nullable (`…create_convites_table.php:39`) — o precedente **não** se
> aplica aqui.

- `RefreshDatabase` vem do `pest()->extend(...)->use(RefreshDatabase::class)` da suíte.
- Permissões: `$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])`, nesta ordem —
  o padrão de `tests/Kit/PaginasInfraTest.php:18`. **Obrigatório em todo cenário de autorização.**
- **`$this->seed()` do `Tests\TestCase` está sobrescrito** para usar `Artisan::call` — o
  `$this->seed()` nativo passa por `PendingCommand` e o `ShieldPermissionsSeeder` grava **zero**
  permissions em silêncio (medido no docblock: 0 × 186).

### Divergências declaradas — Project Rule do projeto vence a skill

1. A skill sugere `pest --parallel --tia` como padrão. **Vence a rule**
   (`.ai/rules/testes-browser.md`): `--parallel` derruba os CT-B (medido: 4 de 11), e sem **PCOV**
   o `--tia` não termina (medido: abortado após 35 min com Xdebug).
2. `pestphp/pest-plugin-mutate` **existe em `vendor/`** mas **não está declarado no
   `composer.json`** — é transitivo do Pest 5. Antes de rodar `--mutate`:
   `composer require pestphp/pest-plugin-mutate --dev`.
3. **O PRD prevê que `tests/Kit/PaineisTest.php` fique vermelho pela contagem de permissions.**
   Lido o arquivo: ele **não assere contagem nenhuma** de painel — usa `toContain` /
   `not->toContain` (`:117-119`, `:126-129`, `:143-155`), e o único `toHaveCount` é
   `master_global → 0` (`:123`), que os Resources novos não alteram. **CT-18 foi escrito sobre as
   asserções que o arquivo realmente faz**, não sobre a contagem que o plano supõe.

```bash
vendor/bin/pest --testsuite=FeatureTenancy    # os CT deste arquivo
vendor/bin/pest --testsuite=Browser           # os CT-B do 05, em série
composer test:kit                             # a regressão de CT-18
```

---

## Regra R1 — o domínio de cada campo vale na criação e na edição

> `RQ-01`, `RQ-02` · área **gravação** (padrão) · técnica: **EP** + **BVA** na fronteira inferior
> do valor + **normalização de texto** + **mass assignment**, derivadas nos **três pontos**:
> criação, edição e uso

```gherkin
# language: pt
Funcionalidade: Solicitação de compra

  Regra: uma solicitação tem descrição, valor e centro de custo válidos em qualquer ponto de
         gravação, nasce em rascunho, e pertence a quem a criou

    Cenário: [CT-01] a solicitação criada pelo formulário nasce em rascunho, com os três campos
      Dado que a Solange está na tela de nova solicitação da organização Acme
      E que existe o centro de custo "TI"
      Quando a Solange informa "Notebooks para o time de suporte", 3.200,50 e o centro "TI" e salva
      Então existe uma solicitação com descrição "Notebooks para o time de suporte",
            valor 3.200,50 e o centro de custo "TI"
      E a situação dela é "rascunho"
      E o solicitante dela é a Solange

    Esquema do Cenário: [CT-02] a solicitação sem dados válidos não é criada
      Dado que a Solange está na tela de nova solicitação da organização Acme
      Quando a Solange tenta salvar com <campo> igual a <valor>
      Então a gravação é recusada com erro no campo <campo>
      E nenhuma solicitação é gravada

      Exemplos:
        | campo           | valor      | # partição                          |
        | descricao       | ""         | inválida — texto obrigatório        |
        | descricao       | "   "      | inválida — só espaços (normalização) |
        | valor           | ausente    | inválida — ausente ≠ vazio          |
        | valor           | 0,00       | borda inferior — zero               |
        | valor           | -1,00      | borda inferior − 0,01               |
        | centro_custo_id | ausente    | inválida — sem centro não há gestor |

    Esquema do Cenário: [CT-37] o mesmo domínio vale na EDIÇÃO em rascunho
      Dado uma solicitação de 4.200,00 da Solange em rascunho, com descrição "Cadeiras"
      Quando a Solange tenta alterar <campo> para <valor>
      Então a gravação é recusada com erro no campo <campo>
      E o valor gravado continua 4.200,00 e a descrição gravada continua "Cadeiras"

      Exemplos:
        | campo     | valor   | # partição                           |
        | valor     | 0,00    | borda inferior — só existe no create? |
        | valor     | -1,00   | borda inferior − 0,01                |
        | descricao | ""      | inválida — texto obrigatório         |
        | descricao | "   "   | inválida — só espaços                |

    Cenário: [CT-38] o domínio é recusado também fora da tela
      Dado uma solicitação de 4.200,00 da Solange em rascunho
      Quando a alteração do valor para -1,00 é feita chamando o sistema diretamente,
             sem passar pelo formulário
      Então a alteração é recusada
      E o valor gravado continua 4.200,00

    Cenário: [CT-03] a situação e o solicitante não vêm do formulário
      Dado que a Solange está na organização Acme e o Otávio também
      Quando a solicitação é criada com um payload que também traz situação "aprovada"
           e solicitante igual ao Otávio
      Então a situação da solicitação gravada é "rascunho"
      E o solicitante dela é a Solange
```

**Alocação**: CT-01, CT-02 e CT-37 são **componente Livewire** (`CreateSolicitacaoCompra` e
`EditSolicitacaoCompra` — **duas páginas distintas**, e é essa distinção que CT-37 existe para
cobrar). CT-03 e CT-38 são **`Feature`, por fora do componente**, e são eles que satisfazem o gate
de camada da regra.

> **Achado da revisão adversarial (D3), fechado aqui.** A v1 tinha CT-02 só no `create` e CT-03
> como único cenário "fora da UI" — e CT-03 assere apenas mass assignment. A validação de domínio
> vivendo só em `CreateSolicitacaoCompra` passava no conjunto inteiro: criar com 3.200,50 (verde),
> editar para −1,00, enviar, aprovar. **CT-37 e CT-38 são o fechamento**, e discriminam: a
> implementação defeituosa (regras só no `create`) fica **vermelha** nos dois e verde em todo o
> resto.

**Gate de tela de escrita**: `create` satisfeito por CT-01; `edit` satisfeito por CT-22 (linha
`rascunho/Solange/aceito`, que afirma o valor gravado) e por CT-37.

**Estouro de teto declarado**: R1 é área `padrão` (teto 3) com 5 cenários. Justificativa: dois
deles (CT-37, CT-38) vieram da revisão adversarial fechando o ponto de **edição** e o gate de
camada — e o gate vence o teto.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a situação inicial é `aguardando_gestor` (pula o rascunho) | CT-01 |
| M2 | `solicitante_id` vem do formulário em vez do usuário autenticado | CT-03 |
| M3 | `situacao` entra no `$fillable` e o payload a sobrescreve | CT-03 |
| M4 | o `valor` aceita zero (`>= 0` no lugar de `> 0`) | CT-02 e CT-37, linhas `0,00` |
| M5 | a descrição vazia é aceita | CT-02, linha `""` |
| M6 | `centro_custo_id` opcional — a solicitação nasce sem centro | CT-02, linha `centro_custo_id ausente` |
| M60 — *revisão adversarial* | a validação de domínio vive só na página de criação; a edição não a repete | CT-37 (as quatro linhas), CT-38 |
| M61 — *revisão adversarial* | `required` sem `trim` — descrição com só espaços é aceita | CT-02 e CT-37, linhas `"   "` |
| M62 — *revisão adversarial* | a validação vive só no `->rules()` do formulário; a chamada direta grava | CT-38 |

---

## Regra R2 — valor acima de R$ 5.000 exige o diretor, depois do gestor

> `RQ-05` · área **alçada** (completo) · técnica: **BVA 3-valores**
> (fronteira: `valor`, granularidade `0,01`) + **sequência**

```gherkin
# language: pt
Funcionalidade: Alçada por valor

  Regra: acima de R$ 5.000,00 a solicitação precisa também do diretor, e a etapa dele vem
         depois da do gestor

    Esquema do Cenário: [CT-04] o limite de R$ 5.000,00 é exclusivo — "acima de" não inclui o valor
      Dado uma solicitação de <valor> criada pela Solange, enviada por ela,
           e aguardando o gestor Gustavo
      E que existe ao menos uma pessoa com autoridade de diretor na organização
      E que o limite vigente é o de fábrica, R$ 5.000,00, sem nenhum ajuste do teste
      Quando o Gustavo aprova a solicitação
      Então a situação dela é "<situacao>"

      Exemplos:
        | valor     | situacao            | # borda    |
        | 4.999,99  | aprovada            | borda−0,01 |
        | 5.000,00  | aprovada            | borda      |
        | 5.000,01  | aguardando diretor  | borda+0,01 |

    Cenário: [CT-05] o diretor não decide antes do gestor
      Dado uma solicitação de 7.480,25 criada pela Solange, enviada por ela,
           e aguardando o gestor Gustavo
      E que a Diana é diretora na organização
      Quando a Diana tenta aprovar a solicitação
      Então a aprovação é recusada
      E a situação dela continua "aguardando gestor"
      E o histórico dela continua sem nenhuma decisão registrada

    Cenário: [CT-06] acima do limite, a solicitação só fica aprovada depois das duas mãos
      Dado uma solicitação de 7.480,25 aguardando o diretor,
           já aprovada pelo gestor Gustavo
      E que a Diana é diretora na organização
      Quando a Diana aprova a solicitação
      Então a situação dela é "aprovada"
      E o histórico dela tem exatamente duas decisões de aprovação,
        a do Gustavo e a da Diana, nesta ordem
```

**Alocação**: `Feature` nos três — o `Então` afirma **situação persistida** e **histórico**.
CT-04 não passa por componente de propósito: é a fronteira do requisito, e ela precisa ser
falsificável sem a tela.

> **O reenvio saiu daqui.** Na v2, `CT-07` e `CT-43` moravam nesta regra e derivavam o reenvio a
> partir do único ponto de rejeição que R2 enxergava. A rodada 2 mostrou que isso deixava três das
> quatro células do produto `{quem rejeitou} × {direção do valor}` vazias. Os dois foram para
> **R13**, que é a dona da pergunta — e `CT-43` foi **retirado** por subsunção (ver
> `## Cogitado e Cortado`).

**O valor do requisito não é injetado.** CT-04 usa `5.000,00` **literal** e o `Dado` afirma que o
limite lido é o de fábrica. Confirmado por leitura: `KIT_COMPRAS_LIMITE_DIRETOR` **não existe** em
`.env`, `.env.example` nem `phpunit.xml`, e não há `.env.testing` no repositório — o cenário mede
o default do `config/kit.php`, não o ambiente.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M7 | `>=` no lugar de `>` — R$ 5.000,00 exatos passam a exigir diretor | CT-04, linha `borda` |
| M8 | `<` invertido — só valores **abaixo** do limite vão ao diretor | CT-04, linhas `borda−0,01` e `borda+0,01` |
| M9 | a comparação usa o `decimal` que o SQLite devolve como string | CT-04, linha `borda+0,01` — a única em que a comparação textual e a numérica divergem no dígito dos centavos |
| M10 | a ordem é invertida: o diretor decide primeiro | CT-05, CT-06 |
| M12 | aprovada pelo gestor, a solicitação acima do limite já vai a "aprovada" | CT-04 linha `borda+0,01`, CT-06 |

> `M11` (alçada congelada no primeiro envio) e `M63` (o reenvio pula o gestor) migraram para
> **R13** junto com os cenários que os matam.

---

## Regra R3 — a rejeição exige justificativa e devolve ao rascunho

> `RQ-06`, `RQ-07`, `RQ-08` · área **estados** (completo) ·
> técnica: **EP** (ausente ≠ vazio ≠ só espaços)

```gherkin
# language: pt
Funcionalidade: Rejeição

  Regra: a solicitação rejeitada volta ao rascunho, e o motivo escrito é obrigatório

    Esquema do Cenário: [CT-09] a rejeição sem motivo escrito não acontece
      Dado uma solicitação de 3.200,50 aguardando o gestor Gustavo
      Quando o Gustavo tenta rejeitar a solicitação com a justificativa <justificativa>
      Então a rejeição é recusada
      E a situação dela continua "aguardando gestor"
      E o histórico dela continua sem nenhuma decisão registrada

      Exemplos:
        | justificativa | # partição                       |
        | ausente       | inválida — campo não enviado     |
        | ""            | inválida — string vazia          |
        | "   "         | inválida — só espaços            |

    Cenário: [CT-10] a rejeição do diretor devolve ao rascunho, não ao gestor
      Dado uma solicitação de 7.480,25 aguardando o diretor,
           já aprovada pelo gestor Gustavo
      Quando a Diana rejeita a solicitação com o motivo "Cotação única, faltam concorrentes"
      Então a situação dela é "rascunho"
      E o histórico dela mostra a rejeição da Diana com esse motivo
```

**Alocação**: `Feature` nos dois. CT-09 chama o **model direto** — é ele que satisfaz o gate de
camada de R3. A versão pela tela está no `05` (CT-B02), porque lá ela prova outra coisa: que o
usuário **vê** a recusa.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M13 | a rejeição grava a etapa e **depois** valida a justificativa | CT-09 |
| M14 | a validação usa `isset()` / `!== null` — a string vazia passa | CT-09, linha `""` |
| M15 | a validação usa `!== ''` sem `trim` — só espaços passa | CT-09, linha `"   "` |
| M18 | a rejeição do diretor devolve ao gestor em vez do rascunho | CT-10 |

> `M16` (estado "rejeitada" próprio) e `M17` (o reenvio apaga o histórico) migraram para **R13**.

---

## Regra R13 — o reenvio reinicia o fluxo a partir do gestor, venha de onde vier a rejeição

> `RQ-08`, `RQ-09`, `RQ-05` · área **estados + alçada** (completo) ·
> técnica: **2-switch** + o produto `{quem rejeitou} × {direção da mudança de valor}`
>
> **Regra nascida do achado estrutural da rodada 2.** RQ-09 (*"pro solicitante corrigir e enviar
> de novo"*) não tinha dono: o comportamento do reenvio estava repartido entre R2 e R3, e cada uma
> o derivava a partir do único ponto de rejeição que conhecia — o gestor. O eixo inteiro
> (*rejeitado pelo diretor* × *valor que desce*) só aparece quando alguém é dono da pergunta.

```gherkin
# language: pt
Funcionalidade: Correção e reenvio

  Regra: a solicitação corrigida e reenviada recomeça pela etapa do gestor e é reavaliada
         pelo valor daquele momento, qualquer que tenha sido a etapa que a rejeitou, e o
         que já foi decidido continua registrado

    Cenário: [CT-07] o reenvio depois da rejeição do gestor recomeça pelo gestor
      Dado uma solicitação de 4.200,00 que voltou ao rascunho depois de rejeitada pelo gestor
      E que a Solange já corrigiu o valor para 8.900,00, ainda em rascunho
      Quando a Solange envia a solicitação de novo
      Então a situação dela é "aguardando gestor"
      E o valor gravado dela é 8.900,00

    Cenário: [CT-08] o reenvio não apaga o ciclo anterior
      Dado uma solicitação de 3.200,50 aguardando o gestor Gustavo
      E que o Gustavo a rejeitou com o motivo "Sem verba neste trimestre"
      E que a Solange já corrigiu a descrição, com a solicitação em rascunho
      Quando a Solange envia a solicitação de novo
      Então a situação dela é "aguardando gestor"
      E o histórico dela ainda mostra a rejeição do Gustavo com o motivo "Sem verba neste trimestre"
      E o histórico dela tem exatamente uma decisão

    Cenário: [CT-45] o reenvio depois da rejeição do DIRETOR também recomeça pelo gestor
      Dado uma solicitação de 7.480,25 que o gestor Gustavo aprovou
      E que a diretora Diana a rejeitou com o motivo "Cotação única", voltando ao rascunho
      E que a Solange já corrigiu a descrição, com a solicitação em rascunho
      Quando a Solange envia a solicitação de novo
      Então a situação dela é "aguardando gestor"
      E o histórico dela tem exatamente duas decisões, a aprovação do Gustavo
        e a rejeição da Diana, nesta ordem

    Esquema do Cenário: [CT-46] a alçada do reenvio é a do valor de agora, nas duas direções
      Dado uma solicitação de <valor_antes> que voltou ao rascunho depois de rejeitada
           por <quem_rejeitou>
      E que a Solange já corrigiu o valor para <valor_depois> e reenviou,
           deixando-a aguardando o gestor Gustavo
      E que existe ao menos uma pessoa com autoridade de diretor na organização
      Quando o Gustavo aprova a solicitação
      Então a situação dela é "<situacao_final>"

      Exemplos:
        | quem_rejeitou | valor_antes | valor_depois | situacao_final      | # célula do produto      |
        | o gestor      | 4.200,00    | 8.900,00     | aguardando diretor  | gestor × sobe            |
        | o gestor      | 8.900,00    | 3.000,00     | aprovada            | gestor × **desce**       |
        | a diretora    | 7.480,25    | 9.900,00     | aguardando diretor  | diretora × sobe          |
        | a diretora    | 7.480,25    | 3.000,00     | aprovada            | diretora × **desce**     |
```

**Alocação**: `Feature` nos quatro — os `Então` afirmam **situação persistida** e **histórico**.

> **Os dois defeitos que a rodada 2 provou atravessarem a v2, fechados aqui:**
>
> **`enviar()` deriva a próxima etapa do histórico** (*"já tem aprovação de gestor, então vai pro
> diretor"*) — o desenho mais natural com tabela append-only. Sobrevivia porque **todos** os
> ciclos de reenvio da v2 partiam de rejeição **do gestor**, onde não há aprovação de gestor no
> histórico e a derivação acerta. CT-45 e as duas linhas `a diretora` de CT-46 o matam: ali há
> aprovação de gestor no histórico e o destino correto continua sendo o gestor.
>
> **Alçada monotônica** (`$exigeDiretor ||= $valor > $limite`) — sobrevivia porque a v2 só testava
> a direção de **subida** (4.200 → 8.900). As linhas `desce` de CT-46 a matam: uma compra corrigida
> de R$ 8.900 para R$ 3.000 não pode exigir diretor, e numa organização sem diretor ficaria presa.

**As quatro células são o eixo inteiro**: a v2 executava **uma** (gestor × sobe).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11 | a alçada é avaliada uma vez, no primeiro envio, e congelada | CT-46, linha `gestor × sobe` |
| M16 | a rejeição leva a um estado "rejeitada" próprio, do qual o solicitante não sai | CT-07, CT-45 |
| M17 | o reenvio apaga o histórico do ciclo anterior | CT-08, CT-45 |
| M63 | o reenvio pula a etapa do gestor e vai direto ao diretor quando o valor subiu | CT-07 |
| M76 — *revisão adversarial, rodada 2* | `enviar()` deriva a etapa seguinte do **histórico** em vez do valor — rejeitada pelo diretor, a solicitação reenviada pula o gestor | CT-45, CT-46 linhas `a diretora` |
| M77 — *revisão adversarial, rodada 2* | a alçada é **monotônica** (`||=`) — uma vez exigido, o diretor nunca deixa de ser exigido | CT-46, linhas `desce` |

---

## Regra R4 — só o aprovador da etapa corrente decide, e isso vale para os dois verbos

> `RQ-04`, `RQ-05`, `RQ-06` · área **autorização** (completo) ·
> técnica: **matriz persona × verbo**, exercitada **por fora da UI**

```gherkin
# language: pt
Funcionalidade: Autoridade de decisão

  Regra: quem decide a etapa corrente é o gestor daquele centro de custo (etapa do gestor)
         ou uma pessoa com autoridade de diretor (etapa do diretor); mais ninguém

    Esquema do Cenário: [CT-11] quem não é o aprovador da vez não decide, por nenhum dos verbos
      Dado uma solicitação de 7.480,25 na situação "<situacao>", cujo centro de custo "TI"
           tem o Gustavo como gestor
      E que existe ao menos uma pessoa com autoridade de diretor na organização
      Quando <pessoa> tenta <verbo> a solicitação chamando o sistema diretamente,
             sem passar pela tela
      Então a ação é recusada
      E a situação dela continua "<situacao>"
      E o histórico dela continua sem nenhuma decisão registrada

      Exemplos:
        | situacao            | pessoa                            | verbo    | # célula persona × verbo       |
        | aguardando gestor   | a Solange (a solicitante)         | aprovar  | dono aprovando a si mesmo      |
        | aguardando gestor   | a Solange (a solicitante)         | rejeitar | verbo irmão da linha acima     |
        | aguardando gestor   | a Gilda (gestora de outro centro) | aprovar  | autoridade é por centro        |
        | aguardando gestor   | a Gilda (gestora de outro centro) | rejeitar | verbo irmão                    |
        | aguardando gestor   | o Otávio (usuário comum)          | aprovar  | sem relação nenhuma            |
        | aguardando gestor   | a Diana (diretora)                | aprovar  | etapa errada — cobre também R2 |
        | aguardando diretor  | o Gustavo (gestor, já decidiu)    | aprovar  | não decide duas vezes          |
        | aguardando diretor  | o Gustavo (gestor, já decidiu)    | rejeitar | verbo irmão                    |
        | aguardando diretor  | o Otávio (usuário comum)          | rejeitar | sem relação nenhuma            |

    Esquema do Cenário: [CT-32] a autoridade é do gestor de agora, não do gestor de então @premissa
      Dado uma solicitação de 3.200,50 aguardando o gestor, no centro de custo "TI"
      E que a Alice trocou o gestor do centro "TI" do Gustavo para a Gilda
      Quando <pessoa> tenta aprovar a solicitação
      Então o resultado é "<resultado>"
      E a situação dela é "<situacao_final>"
      E o histórico dela tem <decisoes> decisões

      Exemplos:
        | pessoa      | resultado | situacao_final      | decisoes | # lado da troca         |
        | o Gustavo   | recusado  | aguardando gestor   | 0        | perdeu a autoridade     |
        | a Gilda     | aceito    | aprovada            | 1        | **ganhou a autoridade** |
```

**Alocação**: `Feature`, chamando o sistema **por fora do componente**. É o que o
`.ai/rules/filament.md` cobra literalmente: *"Barreira sem teste direto não é barreira — o caso
que passa pela tela continuaria verde com a asserção removida."*

> **Achado da revisão adversarial (D8), fechado aqui.** A v1 de CT-32 tinha só o lado negativo (o
> Gustavo recusado). Uma implementação em que a troca de gestor deixa a solicitação **inaprovável
> por qualquer um** passava inteira. O par positivo (a Gilda aprova) é o que discrimina — e o
> `E o histórico tem <decisoes> decisões` fecha o não-efeito na linha negativa, que a v1 também
> omitia.

**`@premissa`**: o card não diz o que acontece quando o gestor do centro muda entre o envio e a
decisão. Premissa: **vale o gestor atual**. Ver A-15.

**Por que nove linhas e não três** em CT-11: **verbo irmão não herda evidência**. Uma
implementação que confere o ator em `aprovar` e esquece em `rejeitar` passa em todo conjunto cuja
evidência de autorização venha só do primeiro verbo.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M19 | a barreira existe em `aprovar` e falta em `rejeitar` | CT-11, linhas de `rejeitar` |
| M20 | a barreira confere que a pessoa é gestor de **algum** centro, não daquele | CT-11, linhas da Gilda |
| M21 | a barreira confere só a permissão (`can()`), e todo `panel_user` decide | CT-11, linhas do Otávio e da Solange |
| M22 | a barreira aceita o gestor na etapa do diretor (ou o contrário) | CT-11, linhas de etapa errada |
| M23 | a autoridade é resolvida a partir de uma cópia gravada no envio | CT-32, linha do Gustavo |
| M24 | a regra vive só no `->visible()` da ação; a chamada direta passa | **todo** CT-11 |
| M64 — *revisão adversarial* | a troca de gestor invalida a solicitação para todo mundo | CT-32, linha da Gilda |

---

## Regra R5 — duas decisões simultâneas produzem uma etapa e uma transição

> `RQ-06` · área **estados** (completo) · técnica: **concorrência × transição** —
> as **quatro** transições de decisão, não uma · idempotência ancorada no agregado persistido

```gherkin
# language: pt
Funcionalidade: Decisão concorrente

  Regra: a mesma solicitação não recebe duas decisões para a mesma etapa

    Cenário: [CT-12] duas aprovações simultâneas da etapa do diretor gravam uma decisão só
      Dado uma solicitação de 7.480,25 aguardando o diretor,
           e duas diretoras, a Diana e a Dora, com a tela aberta
      Quando as duas aprovam a solicitação a partir do mesmo estado lido
      Então a solicitação tem exatamente uma decisão de aprovação de diretor no histórico
      E a situação dela é "aprovada"

    Esquema do Cenário: [CT-40] a guarda de corrida vale nas outras três transições de decisão
      Dado uma solicitação de 7.480,25 na situação "<situacao>",
           lida em duas instâncias a partir do mesmo estado
      E que existe ao menos uma pessoa com autoridade de diretor na organização
      Quando <pessoa> <verbo> a solicitação pelas duas instâncias
      Então a solicitação tem exatamente uma decisão <da_etapa> no histórico
      E o histórico dela tem <decisoes_totais> decisões ao todo
      E a situação dela é "<situacao_final>"

      Exemplos:
        | situacao            | pessoa    | verbo                      | da_etapa                | decisoes_totais | situacao_final     | # transição      |
        | aguardando gestor   | o Gustavo | aprova                     | de aprovação de gestor  | 1               | aguardando diretor | aprovar/gestor   |
        | aguardando gestor   | o Gustavo | rejeita com motivo escrito | de rejeição de gestor   | 1               | rascunho           | rejeitar/gestor  |
        | aguardando diretor  | a Diana   | rejeita com motivo escrito | de rejeição de diretor  | **2**           | rascunho           | rejeitar/diretor |
```

> **Achado da rodada 2 (L4), fechado aqui — e era um oráculo invertido.** A v2 afirmava
> `exatamente **uma** decisão no histórico` nas três linhas. Mas para estar em `aguardando
> diretor` o gestor **já aprovou** — é o que CT-06, CT-25 e CT-26 estabelecem —, logo o total
> correto naquela linha é **duas**. Como estava, a linha só ficaria verde com uma implementação
> que **apaga o histórico anterior** (M17): ela premiava justamente o mutante que CT-08 e CT-45
> existem para matar. CT-12 tinha preservado o qualificador (*"decisão de aprovação **de
> diretor**"*); CT-40 o perdeu ao generalizar. Agora a contagem é **por etapa** e **total**,
> separadas.

**Alocação**: `Feature`. O `Então` é sobre o **agregado persistido** (a solicitação e o histórico
dela), nunca sobre o retorno das duas chamadas.

> **Achado da revisão adversarial (D5), fechado aqui.** A v1 tinha **uma** célula de concorrência
> (`aprovar × aguardando_diretor`) das **quatro** transições de decisão, e o `Então` era literal
> sobre *"decisão de aprovação **de diretor**"*. Uma guarda atômica só na transição do diretor,
> com check-then-act na do gestor, passava — e o duplo clique do gestor gravava duas etapas,
> fazendo a tela de histórico (RQ-13) mentir. A v1 também usava `E a segunda aprovação é recusada`
> como `Então`, que é **oráculo no retorno da chamada** — removido; o oráculo agora é só o estado
> persistido.

**Como materializar sem thread**: carregar **duas instâncias** do mesmo registro (duas queries),
agir pela primeira e depois pela segunda. A segunda continua com a situação lida antes, que é
exatamente o que a requisição concorrente teria em mãos. É a forma do precedente do projeto
(`Convite.php:622-631`) e não exige processo paralelo.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M25 | check-then-act (`if situacao === X` seguido de `save()`) — as duas passam | CT-12, CT-40 |
| M26 | a etapa é gravada **antes** de a transição vencer — sobra etapa órfã | CT-12, CT-40 |
| M27 | a segunda chamada é silenciosamente aplicada, duplicando a transição | CT-12, CT-40 (`a situação é <situacao_final>`) |
| M65 — *revisão adversarial* | a guarda atômica existe só na transição do diretor | CT-40, linhas `aprovar/gestor` e `rejeitar/gestor` |
| M66 — *revisão adversarial* | a guarda existe em `aprovar` e falta em `rejeitar` | CT-40, linhas de `rejeita` |

---

## Regra R6 — sem aprovador para a etapa que vai ficar pendente, a transição é recusada

> `RQ-04` (`00` → A-10) · área **estados** (completo) ·
> técnica: **tabela de decisão** + **cardinalidade do aprovador (0 / 1 / N)**

```gherkin
# language: pt
Funcionalidade: Endereçamento da etapa pendente

  Regra: a transição precisa de alguém a quem endereçar a etapa seguinte; sem ninguém,
         ela é recusada e a solicitação fica onde está

    Cenário: [CT-13] a solicitação de um centro de custo sem gestor não é enviada
      Dado uma solicitação de 3.200,50 em rascunho, no centro de custo "Compras",
           que está sem gestor definido
      Quando a Solange tenta enviar a solicitação
      Então o envio é recusado
      E a situação dela continua "rascunho"
      E nenhuma notificação é enviada

    Cenário: [CT-35] a solicitação acima do limite não avança sem nenhum diretor @premissa
      Dado uma solicitação de 7.480,25 aguardando o gestor Gustavo,
           numa organização que não tem nenhuma pessoa com autoridade de diretor
      Quando o Gustavo aprova a solicitação
      Então a aprovação é recusada
      E a situação dela continua "aguardando gestor"
      E o histórico dela continua sem nenhuma decisão registrada
      E nenhuma notificação é enviada
```

**Alocação**: `Feature` nos dois. O `Então` do não-efeito de notificação é o que separa "recusou"
de "recusou **depois** de avisar alguém" — e a atomicidade aqui é real: a falha acontece **no
mesmo ponto** em que a transição bem-sucedida notificaria, não numa pré-validação distante.

> **Achado da revisão adversarial (D1, metade), fechado aqui.** A v1 protegia a etapa do gestor
> (CT-13) e **não protegia a do diretor**. Uma organização sem nenhum diretor faria a solicitação
> acima do limite ir para `aguardando diretor`, ninguém seria avisado, `?->notify()` não estouraria
> e a solicitação ficaria presa para sempre. CT-35 é o espelho de CT-13 na segunda etapa.

**`@premissa`** em CT-35: o card não trata o caso de zero diretores. Premissa: **falha fechado**,
pelo mesmo raciocínio que o `00` → A-10 aplica ao gestor ausente — as alternativas são piores
(aprovar sem aprovador, ou prender a solicitação sem sinal). Ver A-20.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M28 | sem gestor, a etapa é **pulada** e a solicitação vai direto ao diretor ou a "aprovada" | CT-13 |
| M29 | sem gestor, a solicitação transiciona mesmo assim e fica presa sem aprovador | CT-13 |
| M30 | a notificação é disparada antes da checagem do aprovador | CT-13, CT-35 |
| M67 — *revisão adversarial* | `$diretor?->notify(...)` engole o caso de zero diretores em silêncio | CT-35 |

---

## Regra R7 — o cadastro de centro de custo é administração da organização

> `RQ-04` (`00` → A-08) · área **autorização** (completo) ·
> técnica: **matriz papel × operação** — as operações do Resource, não só a listagem

Esta é a regra que o `00-requisito.md` chama de escalada de privilégio **real e silenciosa**: quem
edita `gestor_id` se nomeia aprovador das próprias compras, e esquecer a subtração **não gera erro
nenhum**.

```gherkin
# language: pt
Funcionalidade: Cadastro de centro de custo

  Regra: definir o gestor de um centro de custo é ato de administração da organização,
         e o usuário comum do negócio não o alcança por operação nenhuma

    Cenário: [CT-14] o usuário comum não recebe as permissões de centro de custo
      Dado a organização Acme com as permissões e os papéis semeados
      Quando a matriz de permissões do papel do usuário comum é consultada
      Então ela não contém nenhuma permissão sobre centro de custo
      E ela contém a permissão de criar solicitação de compra

    Cenário: [CT-15a] a listagem de centros de custo é recusada ao usuário comum
      Dado a organização Acme com as permissões e os papéis semeados
      Quando o Otávio abre a listagem de centros de custo
      Então o acesso dele é recusado com 403

    Cenário: [CT-15b] a administradora enxerga os centros de custo da organização dela
      Dado a organização Acme com o centro de custo "TI", e a organização Globex com "Vendas"
      Quando a Alice abre a listagem de centros de custo da Acme
      Então a linha do centro "TI" aparece na tabela
      E a linha do centro "Vendas" não aparece

    Esquema do Cenário: [CT-39] o usuário comum não cria nem edita centro de custo
      Dado a organização Acme com o centro de custo "TI", cujo gestor é o Gustavo
      Quando o Otávio abre a tela de <operacao> de centro de custo
      Então o acesso dele é recusado com 403
      E o gestor gravado do centro "TI" continua sendo o Gustavo

      Exemplos:
        | operacao | # célula papel × operação |
        | criação  | create                    |
        | edição   | edit                      |

    Cenário: [CT-16] a administradora cadastra o centro e define o gestor
      Dado que a Alice está na tela de novo centro de custo da organização Acme
      Quando a Alice informa o nome "Infraestrutura" e escolhe o Gustavo como gestor, e salva
      Então existe um centro de custo "Infraestrutura" na Acme cujo gestor é o Gustavo

    Esquema do Cenário: [CT-42] o nome do centro de custo é único dentro da organização
      Dado a organização Acme com o centro de custo "TI",
           e a organização Globex sem nenhum centro
      Quando <administradora> tenta cadastrar um centro chamado "TI" na organização dela
      Então o resultado é "<resultado>"
      E a Acme continua com exatamente um centro chamado "TI"
      E a Globex tem <centros_globex> centro chamado "TI"

      Exemplos:
        | administradora        | resultado | centros_globex | # partição                     |
        | a Alice, da Acme      | recusado  | zero           | duplicado na mesma organização |
        | a Bianca, da Globex   | aceito    | um             | mesmo nome, outra organização  |

    Cenário: [CT-47] o usuário comum não troca o gestor nem por fora da tela
      Dado a organização Acme com o centro de custo "TI", cujo gestor é o Gustavo
      Quando o Otávio tenta apontar o gestor do centro "TI" para si mesmo,
             chamando o sistema diretamente, sem passar pelo formulário
      Então a alteração é recusada
      E o gestor gravado do centro "TI" continua sendo o Gustavo
```

**Alocação**: CT-14 é `Feature` **por fora da UI** — lê a matriz de permissões diretamente, e é o
único cenário que falha quando `CentroCustoResource::class` é esquecido na lista de subtração.
CT-15a, CT-15b, CT-39, CT-16 e CT-42 são componente Livewire
(`livewire(...)->assertForbidden()`, `assertCanSeeTableRecords`, `fillForm` → `call('create')` →
asserção sobre o **`gestor_id` gravado**).

> **Achados da rodada 2, fechados aqui.**
> **L10 — falso ✅ do checklist.** A v2 citava **CT-14** como o cenário "fora do componente de UI"
> de R7. Mas CT-14 **consulta a matriz de permissões**, e a lição inteira de D4 foi que consulta
> não é exercício; CT-39, que exerce, é **componente Livewire**. Resultado: R7 — a regra da
> escalada de privilégio de A-08 — não tinha **nenhum** exercício de barreira por fora da tela,
> contrariando a regra que o próprio conjunto cita (*"barreira sem teste direto não é barreira"*).
> **CT-47** é esse exercício, e ele ancora no `gestor_id` gravado.
> **L6 — CT-42 se contradizia com CT-15b.** A linha discriminante (`Globex/aceito`) tinha a
> **Alice** como atriz — e CT-15b, no mesmo arquivo, estabelece que a Globex é alheia a ela. A
> linha passaria ou falharia por contexto de organização, não por unicidade. A persona virou a
> **Bianca**, administradora da Globex, e o `Então` ganhou as âncoras de persistência que todos os
> Esquemas de R10 já tinham — sem elas, uma implementação que mostra o erro **e grava assim mesmo**
> (M50) ficava verde.

> **Achado da revisão adversarial (D4), fechado aqui — e é o mais caro do conjunto.** A v1 tinha
> CT-14 (que **consulta** a matriz) e CT-15 (que abre **a listagem**). Uma implementação que
> protege `canViewAny()` e herda o default `true` em `canCreate()`/`canEdit()` passava no conjunto
> inteiro — e o Otávio navegava direto para a tela de edição, gravava `gestor_id` apontando para
> si mesmo e passava a aprovar as próprias compras. **É literalmente a escalada de A-08, para a
> qual a v1 declarava "CT-14 existe só para isso".** CT-39 é o cenário que a **exerce**, com
> âncora de não-efeito no `gestor_id` gravado.
>
> **Achado D7, também fechado**: a v1 citava CT-16 como cobertura de unicidade, e CT-16 nunca
> tentava um nome duplicado. CT-42 é a partição de duplicidade × escopo de organização — e a linha
> `Globex/aceito` é a que discrimina `unique` de `scopedUnique`.

**Gate de tela de escrita**: `create` satisfeito por CT-16, `edit` por CT-39 (lado negativo) e
CT-42 (gravação com colisão). A edição bem-sucedida do centro está coberta pela troca de gestor de
CT-32.

**Gate de camada da regra**: satisfeito por **CT-47**, não por CT-14 — ver o achado L10 acima.

**Estouro de teto declarado**: 7 cenários contra teto 5 do perfil `completo`. Justificativa: três
(CT-39, CT-42, CT-47) vieram das duas rodadas da revisão adversarial fechando defeitos que
atravessavam intactos, e o gate vence o teto.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M31 | `CentroCustoResource` esquecido na lista de subtração | CT-14, CT-15a, CT-39 |
| M32 | a subtração casa por **substring** do nome da permission | CT-14 (as duas asserções) |
| M33 | `SolicitacaoCompraResource` entra na lista por engano | CT-14 |
| M34 | o `gestor_id` não é gravado (o `Select` de relação salva nulo) | CT-16 |
| M35 | a tela é aberta a qualquer autenticado (Resource sem policy) | CT-15a |
| M68 — *revisão adversarial* | a barreira vive só em `canViewAny()`; `create` e `edit` herdam `true` | CT-39 |
| M69 — *revisão adversarial* | a unicidade do nome é global, não por organização (`unique` em vez de `scopedUnique`) | CT-42, linha da Bianca |
| M78 — *revisão adversarial, rodada 2* | a barreira de escrita do `gestor_id` vive só no Resource; a gravação direta passa | CT-47 |
| M79 — *revisão adversarial, rodada 2* | a validação de nome duplicado recusa na tela **e grava assim mesmo** | CT-42 (as âncoras de persistência) |

---

## Regra R8 — a transição notifica por e-mail todos os aprovadores da etapa pendente

> `RQ-14` · área **notificação** (padrão) · técnica: **rastreio de efeito**, quatro direções +
> **partição de cardinalidade do destinatário (0 / 1 / N)**

Antes das direções, **o quê**: o requisito nomeia o canal (*"Notificar por e-mail"*) e o
destinatário (*"o próximo aprovador"*). Os dois são oráculo. "Uma notificação foi enviada" não é.

E o **quantos**: o card usa o singular, mas o `00` → A-03 estabelece que a etapa do diretor tem
**N** destinatários e que a primeira decisão resolve. **O singular do card é a leitura que um dev
competente faria — e é o defeito.**

```gherkin
# language: pt
Funcionalidade: Aviso ao próximo aprovador

  Regra: todos os que podem decidir a etapa que acabou de ficar pendente recebem um e-mail
         sobre aquela solicitação, uma vez, e mais ninguém recebe

    Cenário: [CT-19] o envio avisa o gestor do centro de custo, por e-mail, sobre aquela solicitação
      Dado uma solicitação de 3.200,50 em rascunho, no centro de custo "TI", cujo gestor é o Gustavo
      E outra solicitação da Solange, também em rascunho
      Quando a Solange envia a primeira solicitação
      Então o Gustavo recebe, pelo canal de e-mail, um aviso que se refere à primeira solicitação
      E nem a Solange nem a Gilda nem a Diana recebem aviso nenhum

    Cenário: [CT-34] todos os diretores da organização são avisados, cada um uma vez, e mais ninguém
      Dado uma solicitação de 7.480,25 da organização Acme, aguardando o gestor Gustavo
      E outra solicitação da Acme, também de 7.480,25, ainda em rascunho
      E que a Diana e a Dora são, as duas, diretoras na Acme
      Quando o Gustavo aprova a primeira solicitação
      Então a Diana e a Dora recebem, cada uma, exatamente um aviso pelo canal de e-mail
      E o aviso de cada uma se refere à primeira solicitação
      E nem a Solange, nem o Gustavo, nem a Alice recebem aviso nenhum

    Cenário: [CT-17] os avisados são os diretores da organização da solicitação
      Dado uma solicitação de 7.480,25 da organização Acme, aguardando o gestor Gustavo
      E que a Diana é diretora na Acme e o Décio é diretor na organização Globex
      Quando o Gustavo aprova a solicitação
      Então a Diana recebe um aviso pelo canal de e-mail
      E o Décio não recebe aviso nenhum

    Esquema do Cenário: [CT-20] transição que não deixa etapa pendente não avisa ninguém
      Dado uma solicitação de <valor> na situação "<situacao_inicial>"
      Quando <pessoa> <acao> a solicitação
      Então a situação dela passa a ser "<situacao_final>"
      E nenhuma notificação é enviada

      Exemplos:
        | valor    | situacao_inicial    | pessoa    | acao                        | situacao_final | # direção do não-efeito       |
        | 3.200,50 | aguardando gestor   | o Gustavo | rejeita, com motivo escrito | rascunho       | rejeição não foi pedida       |
        | 3.200,50 | aguardando gestor   | a Solange | cancela                     | cancelada      | cancelamento não foi pedido   |
        | 7.480,25 | aguardando diretor  | a Diana   | aprova                      | aprovada       | aprovação final: fim do fluxo |
        | 3.200,50 | aguardando gestor   | o Gustavo | aprova                      | aprovada       | abaixo do limite: fim do fluxo |

    Cenário: [CT-21] o envio repetido não avisa duas vezes
      Dado uma solicitação de 3.200,50 em rascunho, no centro de custo "TI"
      Quando a Solange envia a solicitação duas vezes, a partir do mesmo estado lido
      Então o Gustavo recebeu exatamente um aviso pelo canal de e-mail
      E a situação da solicitação é "aguardando gestor"
```

**Alocação**: `Feature` nos cinco. CT-17 e CT-34 moram obrigatoriamente na suíte com
`permission.teams` ligado: com `teams` on, o filtro de papel do spatie usa
`model_has_roles.team_id`, e o contexto é fixado pelo middleware do painel — que não roda em worker
de fila.

> **Achados da revisão adversarial, fechados aqui.**
> **D1** — a v1 montava **uma** diretora por organização, então `->first()` e `->get()` eram
> indistinguíveis. CT-34 introduz a Dora e mata o mutante do singular.
> **L7 e L8, da rodada 2** — CT-34 nasceu na rodada 1 já com dois defeitos herdados: (a) tinha
> **uma só** solicitação, então *"o aviso se refere àquela solicitação"* era verdadeiro em qualquer
> implementação, inclusive na que notifica "a última criada" — a atribuição de M71 a CT-34 era
> falsa, e a segunda solicitação no `Dado` a torna verdadeira; (b) **não tinha a direção "e
> ninguém mais"** — CT-19 a tem para a etapa do gestor, e ninguém a tinha para a transição
> gestor→diretor. Uma implementação que avisa os diretores **e o solicitante** ("para mantê-lo
> informado") atravessava, contra A-11 e `## Fora de Escopo` do `00`.
> **Então fraco de CT-19/CT-17** — *"recebe um aviso de aprovação pendente"* não afirmava **a qual
> solicitação** o aviso se refere. Uma implementação que notifica com o registro errado passava.
> Os `Então` agora afirmam a referência, e CT-19 tem uma segunda solicitação no `Dado` para que a
> afirmação tenha o que discriminar.
> **CT-20 puramente negativo** — as quatro linhas afirmavam só o não-efeito; se a ação falhasse em
> silêncio, o cenário ficaria verde. Agora cada linha tem **âncora positiva** (`situacao_final`).

**Como materializar a referência**:
`Notification::assertSentTo($gustavo, AprovacaoPendente::class, fn ($n, $canais) =>
$n->solicitacao->is($solicitacao) && in_array('mail', $canais, true))` — o closure de dois
argumentos é a API do Laravel, e `$canais` é o retorno de `via()`.

**Estouro de teto declarado**: R8 é área `padrão` (teto 3) com 5 cenários. Não é excesso: rastreio
de efeito exige três direções, a quarta (atomicidade) é exigida por R6, e a quinta (cardinalidade)
veio da revisão adversarial. Regra de efeito colateral **não divide o teto**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M36 | a chamada de notificação é removida | CT-19, CT-17, CT-34 |
| M37 | a notificação sai pelo canal `database` (sino do Filament) e não por e-mail | CT-19, CT-17, CT-34 |
| M38 | quem é avisado é o solicitante, não o aprovador | CT-19 |
| M39 | são avisados os diretores de **todas** as organizações | CT-17 |
| M40 | a aprovação final também dispara aviso | CT-20, linhas de aprovação |
| M41 | a rejeição avisa o solicitante — não pedido, acrescentado por conta própria | CT-20, linha da rejeição |
| M70 — *revisão adversarial* | só o **primeiro** diretor é notificado (`->first()`, leitura do singular do card) | CT-34 |
| M71 — *revisão adversarial* | a notificação carrega a solicitação errada (a última criada, ou um id de outro contexto) | CT-19, CT-34 |
| M80 — *revisão adversarial, rodada 2* | a transição gestor→diretor avisa os diretores **e o solicitante** | CT-34 (`nem a Solange … recebem aviso`) |

---

## Regra R9 — as entidades e o papel novos entram na matriz do painel, e o papel alcança a tela

> `RQ-04`, `RQ-05` · área **autorização** (completo) ·
> técnica: **matriz papel × ação** + **persona × tela**

```gherkin
# language: pt
Funcionalidade: Matriz de permissões dos painéis

  Regra: as entidades novas entram na matriz do painel do negócio, o papel novo declara o
         painel em que vale, e quem tem esse papel alcança a tela de verdade

    Cenário: [CT-18] a fundação continua íntegra com as duas entidades novas
      Dado a instalação com as permissões e os papéis semeados
      Quando a matriz de permissões do painel do negócio é conferida
      Então ela inclui as permissões das duas entidades novas
      E o papel do diretor declara que vale no painel do negócio
      E o papel do usuário comum continua com a permissão da página de perfil
        e continua sem a permissão de criar convite
      E o papel de administração da instalação continua com a permissão de ver usuários

    Cenário: [CT-36] a diretora alcança a solicitação que ela precisa decidir
      Dado uma solicitação de 7.480,25 da Acme aguardando o diretor,
           já aprovada pelo gestor Gustavo
      Quando a Diana abre a listagem de solicitações da Acme
      Então a linha da solicitação aparece na tabela
      E a tela oferece a ela as ações de aprovar e de rejeitar
```

**Alocação**: CT-18 é `Feature` / `tests/Kit/PaineisTest.php` — **o primeiro CT a rodar**. CT-36 é
componente Livewire (`assertCanSeeTableRecords` + `assertActionVisible`).

> **Achado da revisão adversarial (D2), fechado aqui — e é o segundo mais caro.** Na v1, **nenhum
> cenário colocava a Diana diante de uma tela**: ela só aparecia chamando o sistema por fora da UI
> e recebendo e-mail. Um papel `diretor` criado com a coluna `painel` correta mas **sem nenhuma
> permission de `SolicitacaoCompra`** passava em CT-18 e no conjunto inteiro. Em produção: a Diana
> recebe o e-mail, clica, autentica e leva 403 (ou vê listagem vazia). **A segunda etapa de
> aprovação — metade da regra de alçada — seria inalcançável, com tudo verde.**
>
> **Então fraco de CT-18, também fechado**: *"os papéis do kit continuam com as permissões que já
> tinham"* não era quantificado nem nomeado. Agora as asserções são as mesmas que
> `tests/Kit/PaineisTest.php:143-155` já faz — nomeadas, e capazes de acusar a subtração por
> substring (M32).

**Por que "declara que vale no painel do negócio"**: `roles.painel` é o que dá acesso
(`User::canAccessPanel`), e **nulo não é coringa** (`.ai/rules/filament.md`).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M42 | o papel `diretor` é criado sem declarar o painel | CT-18 |
| M43 | os seeders não são rodados — as telas respondem 403 para todos | CT-18, CT-15a, CT-36 |
| M44 | o papel `diretor` recebe a matriz de administração junto | CT-18, CT-14 |
| M72 — *revisão adversarial* | o papel `diretor` é criado com o painel certo e **sem nenhuma permission** de solicitação | CT-36 |

---

## Regra R10 — cada operação só existe nas situações em que o requisito a autoriza

> `RQ-02`, `RQ-03`, `RQ-04`, `RQ-05`, `RQ-06`, `RQ-10`, `RQ-11` · área **estados** (completo) ·
> técnica: **tabela estado × operação** — uma só, produto cartesiano fechado

### A matriz — contagem declarada

Montada a partir das **cinco situações do ciclo de vida** e dos **oito verbos** que a entidade
aceita, e **não** a partir do mapa de regras.

> **5 situações × 8 operações = 40 células · 19 válidas · 21 inválidas.**
> Perfil completo ⇒ **100% das 21 inválidas** exercitadas, e **cada coluna com ao menos uma
> célula válida** também exercitada.

**`criar` está fora da matriz, com motivo**: ela não parte de situação nenhuma. Coberta por R1.

| Situação ↓ / Operação → | editar | excluir | enviar | aprovar | rejeitar | cancelar | ver detalhe | listar |
|---|---|---|---|---|---|---|---|---|
| **rascunho** | ✅ CT-22 | ✅ CT-23 | ✅ CT-24 | ❌ CT-25 | ❌ CT-26 | ❌ CT-27 | ✅ CT-44 | ✅ CT-28 |
| **aguardando gestor** | ❌ CT-22 | ❌ CT-23 | ❌ CT-24 | ✅ CT-25 | ✅ CT-26 | ✅ CT-27 | ✅ CT-44 | ✅ CT-28 |
| **aguardando diretor** | ❌ CT-22 | ❌ CT-23 | ❌ CT-24 | ✅ CT-25 | ✅ CT-26 | ✅ CT-27 | ✅ CT-44 | ✅ CT-28 |
| **aprovada** | ❌ CT-22 | ❌ CT-23 | ❌ CT-24 | ❌ CT-25 | ❌ CT-26 | ❌ CT-27 | ✅ CT-44, CT-29 | ✅ CT-28 |
| **cancelada** | ❌ CT-22 | ❌ CT-23 | ❌ CT-24 | ❌ CT-25 | ❌ CT-26 | ❌ CT-27 | ✅ CT-44 | ✅ CT-28 |

✅ = célula válida, exercitada com sucesso · ❌ = célula inválida, **recusa e não-efeito**
afirmados. **Nenhuma célula ficou como "não se aplica" ou lacuna, e nenhuma é resolvida por
citação de cenário que executa outra operação.**

> **Achado da revisão adversarial, fechado aqui.** Na v1 as cinco células de `ver detalhe`
> apontavam todas para CT-29, um cenário **único** cuja solicitação termina em `aprovada` — ou
> seja, **4 de 40 células (10%) eram argumentadas, não executadas**. CT-44 é o `Esquema` que as
> executa, e CT-29 volta ao papel dele: o histórico (RQ-13).

### A matriz não é bidimensional — as outras duas dimensões

| Dimensão | Onde ela varia |
|---|---|
| **persona** | CT-22 (o solicitante × outra pessoa), CT-27 (o solicitante × o gestor), CT-44 (o solicitante × o gestor lendo), CT-41 (o colega lendo), e a matriz persona × verbo inteira em CT-11 |
| **campo alterado** | CT-22 troca o **valor** — o campo que decide a alçada — e não a descrição, e o faz **fora do rascunho**, que é onde mora o defeito de recomputação. CT-37 fecha a fronteira **dentro** do rascunho |

```gherkin
# language: pt
Funcionalidade: Ciclo de vida da solicitação

  Regra: cada operação só existe nas situações em que o requisito a autoriza

    Esquema do Cenário: [CT-22] a edição existe só no rascunho, e só para quem solicitou
      Dado uma solicitação de 4.200,00 da Solange na situação "<situacao>"
      Quando <pessoa> tenta alterar o valor para 9.100,00
      Então o resultado é "<resultado>"
      E o valor gravado da solicitação é <valor_final>
      E a situação dela continua "<situacao>"

      Exemplos:
        | situacao            | pessoa      | resultado | valor_final | # célula                    |
        | rascunho            | a Solange   | aceito    | 9.100,00    | válida — dono em rascunho   |
        | rascunho            | o Otávio    | recusado  | 4.200,00    | persona — não é o dono      |
        | aguardando gestor   | a Solange   | recusado  | 4.200,00    | inválida — já enviada       |
        | aguardando diretor  | a Solange   | recusado  | 4.200,00    | inválida — já enviada       |
        | aprovada            | a Solange   | recusado  | 4.200,00    | inválida — terminal         |
        | cancelada           | a Solange   | recusado  | 4.200,00    | inválida — terminal         |

    Esquema do Cenário: [CT-23] a exclusão existe só no rascunho
      Dado uma solicitação de 3.200,50 da Solange na situação "<situacao>"
      Quando a Solange tenta excluir a solicitação
      Então o resultado é "<resultado>"
      E a solicitação <persistencia>

      Exemplos:
        | situacao            | resultado | persistencia                                | # célula            |
        | rascunho            | aceito    | não existe mais                             | válida              |
        | aguardando gestor   | recusado  | continua com a situação "aguardando gestor" | inválida            |
        | aguardando diretor  | recusado  | continua com a situação "aguardando diretor"| inválida            |
        | aprovada            | recusado  | continua com a situação "aprovada"          | inválida — terminal |
        | cancelada           | recusado  | continua com a situação "cancelada"         | inválida — terminal |

    Esquema do Cenário: [CT-24] o envio existe só no rascunho
      Dado uma solicitação de 3.200,50 da Solange na situação "<situacao>",
           num centro de custo com gestor definido
      Quando a Solange tenta enviar a solicitação
      Então o resultado é "<resultado>"
      E a situação dela é "<situacao_final>"
      E o número de notificações enviadas é <notificacoes>

      Exemplos:
        | situacao            | resultado | situacao_final      | notificacoes | # célula            |
        | rascunho            | aceito    | aguardando gestor   | 1            | válida              |
        | aguardando gestor   | recusado  | aguardando gestor   | 0            | inválida            |
        | aguardando diretor  | recusado  | aguardando diretor  | 0            | inválida            |
        | aprovada            | recusado  | aprovada            | 0            | inválida — terminal |
        | cancelada           | recusado  | cancelada           | 0            | inválida — terminal |

    Esquema do Cenário: [CT-25] a aprovação existe só nas situações em que há etapa pendente
      Dado uma solicitação de 7.480,25 na situação "<situacao>"
      E que existe ao menos uma pessoa com autoridade de diretor na organização
      Quando <pessoa> tenta aprovar a solicitação
      Então o resultado é "<resultado>"
      E a situação dela é "<situacao_final>"
      E o histórico dela tem <decisoes> decisões

      Exemplos:
        | situacao            | pessoa    | resultado | situacao_final      | decisoes | # célula                    |
        | rascunho            | o Gustavo | recusado  | rascunho            | 0        | **inválida — a que escapa** |
        | aguardando gestor   | o Gustavo | aceito    | aguardando diretor  | 1        | válida                      |
        | aguardando diretor  | a Diana   | aceito    | aprovada            | 2        | válida                      |
        | aprovada            | a Diana   | recusado  | aprovada            | 2        | inválida — terminal         |
        | cancelada           | o Gustavo | recusado  | cancelada           | 0        | **inválida — a que escapa** |

    Esquema do Cenário: [CT-26] a rejeição existe só nas situações em que há etapa pendente
      Dado uma solicitação de 7.480,25 na situação "<situacao>"
      Quando <pessoa> tenta rejeitar a solicitação com o motivo "Fora do orçamento"
      Então o resultado é "<resultado>"
      E a situação dela é "<situacao_final>"
      E o histórico dela tem <decisoes> decisões

      Exemplos:
        | situacao            | pessoa    | resultado | situacao_final | decisoes | # célula                    |
        | rascunho            | o Gustavo | recusado  | rascunho       | 0        | **inválida — a que escapa** |
        | aguardando gestor   | o Gustavo | aceito    | rascunho       | 1        | válida                      |
        | aguardando diretor  | a Diana   | aceito    | rascunho       | 2        | válida                      |
        | aprovada            | a Diana   | recusado  | aprovada       | 2        | inválida — terminal         |
        | cancelada           | o Gustavo | recusado  | cancelada      | 0        | **inválida — a que escapa** |

    Esquema do Cenário: [CT-27] o cancelamento existe entre o envio e a aprovação final,
                                e é do solicitante
      Dado uma solicitação de 7.480,25 da Solange na situação "<situacao>"
      Quando <pessoa> tenta cancelar a solicitação
      Então o resultado é "<resultado>"
      E a situação dela é "<situacao_final>"

      Exemplos:
        | situacao            | pessoa      | resultado | situacao_final      | # célula                        |
        | rascunho            | a Solange   | recusado  | rascunho            | inválida — em rascunho, exclui  |
        | aguardando gestor   | a Solange   | aceito    | cancelada           | válida                          |
        | aguardando diretor  | a Solange   | aceito    | cancelada           | válida                          |
        | aguardando gestor   | o Gustavo   | recusado  | aguardando gestor   | persona — não é o solicitante   |
        | aprovada            | a Solange   | recusado  | aprovada            | inválida — terminal             |
        | cancelada           | a Solange   | recusado  | cancelada           | inválida — terminal             |

    Esquema do Cenário: [CT-44] o detalhe abre em qualquer situação e mostra a situação daquele registro
      Dado uma solicitação de 3.200,50 da Solange na situação "<situacao>"
      Quando a Solange abre o detalhe dessa solicitação
      Então o campo de situação do registro aberto mostra "<rotulo>"
      E o valor 3.200,50 do registro aberto aparece na tela

      Exemplos:
        | situacao            | rotulo              | # partição do enum |
        | rascunho            | Rascunho            | 1 de 5             |
        | aguardando gestor   | Aguardando gestor   | 2 de 5             |
        | aguardando diretor  | Aguardando diretor  | 3 de 5             |
        | aprovada            | Aprovada            | 4 de 5             |
        | cancelada           | Cancelada           | 5 de 5             |
```

> **Achado da rodada 2 (L9), fechado aqui.** CT-44 nasceu na rodada 1 usando exatamente a forma de
> oráculo que o achado D6 tinha acabado de condenar: `assertSee` **de página**, sem âncora no
> registro — um detalhe que renderize a situação no cabeçalho ou no breadcrumb e **não tenha** o
> campo de situação no infolist passaria, e o cenário existe justamente para executar 4 células
> antes argumentadas. Além disso a **persona mudava a cada linha** (Solange/Gustavo/Diana), o que
> confundia a dimensão *situação* com a dimensão *persona*: nenhuma pessoa percorria as 5
> situações. A persona foi fixada na Solange (a dona, que lê em qualquer situação), a asserção foi
> ancorada no campo do registro aberto, e a dimensão persona da leitura vive onde é dela — CT-41.

**Alocação**: CT-22…CT-27 são `Feature`, com a operação disparada **por fora do componente** — é a
camada que distingue "a regra existe" de "a tela chama a regra". CT-44 é componente (é sobre a
tela). A affordance correspondente é provada em CT-33 e CT-36.

> **Achados da revisão adversarial, fechados aqui.**
> A legenda *"❌ = recusa **e** não-efeito"* era **falsa** em CT-24 e CT-26 na v1: CT-26 não tinha
> coluna de histórico (o irmão CT-25 tinha) e CT-24 não tinha coluna de notificação. Isso
> **invalidava a atribuição de M50** nessas duas colunas — uma implementação que grava a etapa de
> rejeição e só depois recusa a transição passava, e um `enviar × aprovada` podia disparar o
> e-mail antes de recusar. As duas colunas foram acrescentadas.
> A linha `rascunho/Solange/aceito` de CT-22 não afirmava que a situação continuava rascunho — uma
> edição que também transicionasse passava. Coluna acrescentada.

**Estouro de teto declarado**: 7 cenários contra teto 5. Justificativa: a matriz é **uma** e tem 8
colunas; cada `Esquema` cobre uma coluna inteira. Cortar um deixaria uma operação sem nenhuma
célula executada — e a contagem declarada é o oráculo da própria matriz.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M45 | a barreira de situação existe em `editar` e falta em `excluir` (ou vice-versa) | CT-22 e CT-23, linhas não-rascunho |
| M46 | "aprovada" não é terminal | CT-22, CT-25, CT-27, linhas `aprovada` |
| M47 | a aprovação é aceita a partir do rascunho ou da cancelada | CT-25 e CT-26, linhas `rascunho` e `cancelada` |
| M48 | o cancelamento é aceito em rascunho — duas portas para o mesmo lugar | CT-27, linha `rascunho` |
| M49 | o cancelamento é aceito de qualquer pessoa | CT-27, linha do Gustavo |
| M50 | a operação é recusada **depois** de gravar | as colunas `valor gravado`, `situação final`, `persistência`, `decisões` e `notificações` de CT-22…CT-27 |
| M73 — *revisão adversarial* | o envio dispara o e-mail antes de conferir a situação | CT-24, coluna `notificacoes` |

---

## Regra R11 — a tela mostra a situação atual e quem decidiu cada etapa

> `RQ-12`, `RQ-13` · área **exibição** (padrão) · técnica: **EP exaustiva do enum** + persona

```gherkin
# language: pt
Funcionalidade: Leitura do andamento

  Regra: a tela mostra em que situação cada solicitação está e, no detalhe, quem decidiu cada
         etapa, quando e com que motivo

    Esquema do Cenário: [CT-28] a listagem mostra a situação na linha de cada solicitação
      Dado duas solicitações da Solange na Acme: uma na situação "<situacao>"
           e outra sempre em "rascunho"
      Quando a Solange abre a listagem de solicitações
      Então as duas linhas aparecem na tabela
      E a linha da primeira solicitação mostra o rótulo "<rotulo>"

      Exemplos:
        | situacao            | rotulo              | # partição do enum |
        | rascunho            | Rascunho            | 1 de 5             |
        | aguardando gestor   | Aguardando gestor   | 2 de 5             |
        | aguardando diretor  | Aguardando diretor  | 3 de 5             |
        | aprovada            | Aprovada            | 4 de 5             |
        | cancelada           | Cancelada           | 5 de 5             |

    Cenário: [CT-29] o detalhe mostra quem decidiu cada etapa, quando e por quê
      Dado o relógio congelado em 14/08/2026 às 10:00 no fuso da aplicação
      E uma solicitação de 7.480,25 que foi rejeitada pelo Gustavo com o motivo
           "Sem verba neste trimestre", corrigida e reenviada, aprovada pelo Gustavo
           e aprovada pela Diana
      Quando a Solange abre o detalhe da solicitação
      Então a tela mostra a situação "Aprovada"
      E mostra exatamente três decisões, com os nomes Gustavo, Gustavo e Diana, nesta ordem
      E mostra a data 14/08/2026 em cada uma delas
      E mostra o motivo "Sem verba neste trimestre" na decisão de rejeição

    Esquema do Cenário: [CT-33] a tela oferece as ações de decisão só a quem pode usá-las
      Dado uma solicitação de 3.200,50 da Solange aguardando o gestor Gustavo
      Quando <pessoa> abre a listagem de solicitações
      Então a linha da solicitação aparece na tabela
      E a tela <oferece> as ações de aprovar e de rejeitar

      Exemplos:
        | pessoa      | oferece     | # persona                          |
        | a Solange   | não oferece | a solicitante não decide           |
        | o Gustavo   | oferece     | o gestor da vez decide             |
        | a Diana     | não oferece | a diretora, mas não é a etapa dela |

    Cenário: [CT-41] o colega da mesma organização lê, mas não age @premissa
      Dado uma solicitação de 3.200,50 da Solange aguardando o gestor Gustavo
      Quando o Otávio abre o detalhe da solicitação
      Então a tela mostra a situação "Aguardando gestor"
      E a tela não oferece a ele ação nenhuma de decisão, de edição ou de exclusão
```

**Alocação**: componente Livewire nos quatro — `assertCanSeeTableRecords`, `assertSee` do rótulo,
`assertActionHidden` / `assertActionVisible`. Os helpers estão em uso no projeto
(`tests/Kit/ConviteEmMassaTest.php:345`, `tests/Tenancy/AdminDaOrganizacaoTest.php:133,498`) e
todos foram confirmados como **não-deprecated** nos `.stubs.php` do Filament 5.

> **Achados da revisão adversarial, fechados aqui.**
> **D6** — a v1 de CT-28 afirmava `assertSee('<rotulo>')`, que é texto **de página**. Um
> `SelectFilter::make('situacao')` renderiza os cinco rótulos no HTML **sem nenhuma linha da
> tabela mostrar situação nenhuma**: as cinco linhas do Esquema ficariam verdes com **RQ-12 não
> implementado**. Agora o `Dado` põe **duas** solicitações e o `Então` afirma o rótulo **na linha
> da primeira**, ancorado no registro.
> **CT-29** ganhou contagem exata (`exatamente três decisões`), a ordem dos nomes e a data com
> valor esperado, sob `freezeTime()` — sem isso, um histórico com decisões duplicadas (D5) passava.
> **CT-33** era `Quando` único com um segundo `Quando` embutido no `Então`; virou `Esquema`, e a
> linha da Diana fecha de quebra o eixo persona × tela da diretora.
> **CT-41 é novo**: a v1 não tinha **nenhum** cenário de IDOR **intra**-organização — o Otávio
> abrindo a solicitação da colega era comportamento indefinido e não testado.

**`@premissa`** em CT-41: o card não decide se o colega lê a solicitação alheia. Premissa:
**lê, e não age** — RQ-12/RQ-13 dizem "mostrar na tela" sem restringir a quem, e a organização já
é a fronteira que o `00` reconhece. Ver A-21.

**Partição exaustiva, não amostrada**: as cinco situações são cinco classes obrigatórias.

**Estouro de teto declarado**: 4 cenários contra teto 3 do perfil `padrão`. Justificativa: CT-41
veio da revisão adversarial fechando um eixo de autorização inteiro.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M51 | o rótulo de "aguardando diretor" cai no mesmo de "aprovada" | CT-28 e CT-44, linha 3 de 5 |
| M52 | a coluna mostra o valor cru do banco (`aguardando_gestor`) | CT-28, todas as linhas |
| M53 | o histórico mostra a decisão mas não quem a tomou | CT-29 |
| M54 | o histórico mostra só o ciclo mais recente | CT-29 (`exatamente três decisões`) |
| M55 | a justificativa não é exibida — o solicitante não sabe o que corrigir | CT-29 |
| M56 | as ações de aprovar/rejeitar aparecem para todo mundo e estouram 403 ao clicar | CT-33, CT-41 |
| M74 — *revisão adversarial* | não há coluna de situação; os rótulos vêm do filtro | CT-28 (`a linha … mostra o rótulo`) |
| M75 — *revisão adversarial* | qualquer um da organização edita ou decide a solicitação do colega | CT-41 |

---

## Regra R12 — solicitação de outra organização é invisível e intocável

> origem: **taxonomia (IDOR / autorização horizontal)** — o card não menciona organização ·
> área **isolamento** (completo)

```gherkin
# language: pt
Funcionalidade: Isolamento entre organizações

  Regra: uma solicitação pertence a uma organização, e quem está noutra não a vê nem age sobre ela

    Cenário: [CT-30] a solicitação de outra organização não aparece nem abre
      Dado uma solicitação de 3.200,50 aguardando o gestor, na organização Globex
      E uma solicitação de 1.500,00 aguardando o gestor, na organização Acme
      E que a Solange opera a organização Acme
      Quando a Solange abre a listagem de solicitações da Acme
      Então a linha da solicitação da Acme aparece na tabela
      E a linha da solicitação da Globex não aparece
      E o endereço de detalhe da solicitação da Globex responde "não encontrado"

    Esquema do Cenário: [CT-31] ninguém de outra organização decide, seja gestor ou diretor
      Dado uma solicitação da organização Acme na situação "<situacao>"
      E <pessoa>, da organização Globex
      Quando essa pessoa tenta aprovar a solicitação da Acme,
             chamando o sistema diretamente, sem passar pela tela
      Então a aprovação é recusada
      E a situação dela continua "<situacao>"
      E o histórico dela tem <decisoes> decisões

      Exemplos:
        | situacao            | pessoa                                        | decisoes | # tipo de aprovador estrangeiro |
        | aguardando gestor   | o Gunther, gestor de um centro de custo       | 0        | gestor                          |
        | aguardando diretor  | o Décio, com autoridade de diretor            | 1        | **diretor**                     |
```

**Alocação**: CT-30 é componente + rota (`assertCanSeeTableRecords` / `assertCanNotSeeTableRecords`
e `get(...)->assertNotFound()`); CT-31 é `Feature`, **por fora da UI**.

> **Achado da revisão adversarial, fechado aqui.** A v1 de CT-30 não declarava a **situação de
> partida** da solicitação da Globex, e não tinha nenhuma solicitação visível na Acme. Se a
> fixture caísse em `rascunho` e a listagem escondesse rascunhos alheios por qualquer motivo, o
> cenário ficaria verde **sem que o isolamento por organização existisse** — oráculo negativo que
> passa pelo motivo errado. Agora a situação está fixada e há uma solicitação irmã visível.

> **Achado da rodada 2 (L3), fechado aqui.** A v2 tinha **uma** persona estrangeira, o Gunther, e
> ele é **gestor** — logo CT-31 cobria só a metade `gestor` do IDOR. A metade `diretor` ficava
> vazia: nas linhas `aguardando diretor` de CT-11 os atores eram Gustavo e Otávio (ambos da Acme),
> e o Décio aparecia apenas como **destinatário de e-mail** em CT-17, nunca como ator. Uma barreira
> escrita como `hasRole('diretor')` — a armadilha que o próprio `04` documenta para o spatie com
> `permission.teams` — deixaria qualquer diretor de qualquer organização aprovar qualquer
> solicitação em `aguardando diretor` **da base inteira**, por fora da UI. CT-31 virou `Esquema`
> com os dois tipos de aprovador estrangeiro.

**O parâmetro livre aqui é o contexto, não o dado**: o que precisa cair na janela de divergência é
**a organização do ator**, e o recurso tem de existir **na outra**. E o **tipo** do ator
estrangeiro é uma segunda dimensão: gestor e diretor passam por barreiras diferentes.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M57 | o recorte vive só na `table()` do Resource, e o route binding traz o registro alheio | CT-30 |
| M58 | sem organização no contexto, a consulta **falha aberta** e devolve a base inteira | CT-30 (`a linha da Globex não aparece`) |
| M59 | a barreira de aprovação confere só "é gestor de algum centro", sem o recorte por organização | CT-31, linha do Gunther |
| M81 — *revisão adversarial, rodada 2* | a barreira da etapa do diretor é `hasRole('diretor')` **sem recorte de organização** — qualquer diretor aprova qualquer solicitação da base | CT-31, linha do Décio |

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| **IDOR / autorização horizontal — entre organizações** | CT-30, CT-31 (**as duas linhas**: gestor e diretor estrangeiros) |
| **IDOR / autorização horizontal — dentro da organização** | CT-41 (`@premissa`) |
| **Autorização exercida na ação, não só consultada** | solicitação: CT-11, CT-31, CT-22…CT-27 · **centro de custo: CT-39** (tela) **e CT-47** (fora dela) |
| **Autorização por fora do componente de UI** (gate de camada) | CT-38 (R1), CT-09 (R3), CT-11 (R4), **CT-47 (R7)**, CT-22…CT-27 (R10), CT-31 (R12) — **não CT-14**, que consulta a matriz em vez de exercer a barreira (falso ✅ da v2, achado L10) |
| **Idempotência**, ancorada no agregado persistido | CT-12 e **CT-40** (as quatro transições de decisão), CT-21 (dois envios → um e-mail), CT-25 linha `aprovada` |
| **Concorrência** | CT-12, CT-40 |
| **Fronteira no ponto de entrada** (gravação) | criação: CT-02 (`0,00`, `-1,00`) · **edição: CT-37** (a v1 só alterava para valor válido) · fora da UI: CT-38 |
| **Criação ≠ edição ≠ uso** | criação CT-01/CT-02 · edição CT-37/CT-22 · uso CT-04 — o campo `valor` com a **fronteira** nos três pontos |
| **Cardinalidade do destinatário do efeito (0 / 1 / N)** | CT-35 (zero), CT-19 (um), **CT-34** (N) |
| **Domínio condicionado** (o valor de um campo muda a fronteira de outro) | não se aplica **entre campos**: o `valor` tem um único domínio (`> 0`), e a fronteira dos R$ 5.000 é de roteamento de fluxo. **Por operação** há um: `justificativa` é obrigatória em `rejeitar` e indefinida em `aprovar` → **lacuna declarada**, A-22 |
| **Estado × operação de escrita** (o registro terminal ainda funciona?) | CT-22…CT-27, linhas `aprovada` e `cancelada` — 12 células |
| **Ausente ≠ `null` ≠ `""`** | CT-02 (`valor` ausente × `descricao` vazia), CT-09 (justificativa ausente × `""` × `"   "`) |
| **Paginação / ordenação** | **lacuna declarada** — tentado derivar borda de paginação e critério de ordenação; o requisito não fixa tamanho de página nem ordem, e qualquer valor viria do plano. Vira pergunta **A-17** |
| **Timezone / DST — comparação** | não se aplica: nenhum campo tem prazo, validade, expiração ou agendamento; não há data comparada em lugar nenhum |
| **Timezone / DST — exibição** | CT-29, com o relógio congelado num **instante no fuso da aplicação** (14/08/2026 10:00), e não num dia. Achado L10 da rodada 2: o *"não se aplica"* foi escrito antes de CT-29 ganhar oráculo de data, e congelar "14/08" sem hora exibiria 15/08 se o instante caísse às 23:00 locais com `created_at` em UTC |
| **Texto livre: espaços nas bordas** | `justificativa` CT-09 linha `"   "` · **`descricao` CT-02 e CT-37 linhas `"   "`** (a v1 aplicava a normalização só à justificativa) |
| **Unicode / acento / limite de varchar** | **lacuna declarada** — tentado derivar a borda do `varchar(255)`, mas 255 é número **do plano**; usá-lo como oráculo seria testar o PRD. Vira pergunta **A-18** |
| **Unicidade + soft delete** | soft delete: não se aplica — nenhuma entidade desta feature (nem do kit) usa `SoftDeletes`. **Unicidade: CT-42** — nome duplicado na mesma organização recusado, mesmo nome noutra aceito (a v1 citava CT-16, que nunca tentava duplicar) |
| **Entidade removível/desligada ainda funciona?** | CT-23 (a excluída deixa de existir) · **premissa de mecanismo declarada**: a exclusão é física, então "o excluído aceita escrita?" é inexpressável para a solicitação. Os **análogos expressáveis foram escritos**: o centro **sem gestor** (CT-13) e a organização **sem diretor** (CT-35) são os registros "desligados", e os dois cenários provam que eles **deixaram de funcionar**, não que sumiram de uma lista |
| **Entidade cuja chave muda por baixo** | **CT-32** — a troca de gestor, nos **dois** lados: quem perdeu e quem ganhou a autoridade |
| **CRUD combinado** (editar sem alterar nada, excluir duas vezes) | **lacuna declarada** — os dois casos degenerados não têm cenário próprio. Tentado: derivar do requisito; o card não os trata, e o comportamento esperado seria inventado. Vira pergunta **A-19** |
| **Mass assignment** | CT-03 |
| **Upload** | não se aplica: anexos estão em `## Fora de Escopo` do `00` |
| **Precisão monetária** | CT-04 — e os valores **discriminam**: `4.999,99` / `5.000,00` / `5.000,01` distinguem `>` de `>=` **e** comparação numérica de comparação de string (M9). CT-01 e CT-22 afirmam o valor gravado, não a chave |
| **Ordem de eventos / 2-switch** | CT-08 e CT-07 (rejeitar → corrigir → reenviar), **CT-45** (o mesmo partindo da rejeição do **diretor**), **CT-46** (o produto `quem rejeitou × direção do valor`, 4 células), CT-10 |
| **Cardinalidade do ator estrangeiro** (gestor × diretor) | CT-31, as duas linhas — a v2 só tinha a de gestor |

**As quatro lacunas declaradas (A-17, A-18, A-19, A-22) são dívida que alguém conhece**, cada uma
com o que foi tentado e por que o oráculo viria do plano e não do requisito. Nenhuma delas está
marcada como coberta.

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo previsto | Mata |
|----|---------|-------|---------|--------|------------------|------|
| CT-01 | a solicitação criada nasce em rascunho com os três campos | R1 | EP | componente | `SolicitacaoCompraFormTest` | M1 |
| CT-02 | sem dados válidos não é criada | R1 | EP + BVA + normalização | componente | idem | M4, M5, M6, M61 |
| CT-03 | situação e solicitante não vêm do formulário | R1 | mass assignment | Feature (fora da UI) | `SolicitacaoCompraTest` | M2, M3 |
| CT-04 | o limite de R$ 5.000,00 é exclusivo | R2 | **BVA 3-valores** | Feature | `AlcadaTest` | M7, M8, M9, M12 |
| CT-05 | o diretor não decide antes do gestor | R2 | sequência | Feature | idem | M10 |
| CT-06 | acima do limite exige as duas mãos | R2 | sequência | Feature | idem | M10, M12 |
| CT-07 | o reenvio depois da rejeição do gestor recomeça pelo gestor | **R13** | 2-switch | Feature | `ReenvioTest` | M16, M63 |
| CT-08 | o reenvio preserva o histórico do ciclo anterior | **R13** | **2-switch** | Feature | idem | M17 |
| CT-09 | a rejeição sem motivo não acontece | R3 | EP | Feature (fora da UI) | idem | M13, M14, M15 |
| CT-10 | a rejeição do diretor devolve ao rascunho | R3 | EP | Feature | idem | M18 |
| CT-11 | quem não é o aprovador da vez não decide, por nenhum verbo | R4 | **persona × verbo** | Feature (fora da UI) | `AutoridadeTest` | M19…M22, M24 |
| CT-12 | duas aprovações simultâneas do diretor gravam uma só | R5 | concorrência | Feature | `ConcorrenciaTest` | M25, M26, M27 |
| CT-13 | centro sem gestor não envia | R6 | tabela de decisão | Feature | `EnvioTest` | M28, M29, M30 |
| CT-14 | o usuário comum não recebe as permissões de centro de custo | R7 | papel × ação | Feature (fora da UI) | `CentroCustoAutorizacaoTest` | M31, M32, M33 |
| CT-15a | a listagem de centros de custo é recusada ao usuário comum | R7 | papel × operação | componente | idem | M35, M43 |
| CT-15b | a administradora enxerga os centros da organização dela | R7 | papel × operação | componente | idem | M31 |
| CT-16 | a administradora cadastra o centro e define o gestor | R7 | EP | componente | `CentroCustoFormTest` | M34 |
| CT-17 | os avisados são os diretores da organização da solicitação | R8 | rastreio de efeito | Feature | `NotificacaoTest` | M36, M37, M39 |
| CT-18 | a fundação continua íntegra com as entidades novas | R9 | papel × ação | Feature | `tests/Kit/PaineisTest.php` | M42, M43, M44 |
| CT-19 | o envio avisa o gestor por e-mail, sobre aquela solicitação | R8 | rastreio de efeito | Feature | `NotificacaoTest` | M36, M37, M38, M71 |
| CT-20 | transição sem etapa pendente não avisa ninguém | R8 | rastreio de efeito | Feature | idem | M40, M41 |
| CT-21 | o envio repetido não avisa duas vezes | R8 | rastreio de efeito | Feature | idem | M36 |
| CT-22 | editar × 5 situações × 2 personas × campo decisivo | R10 | **estado × operação** | Feature (fora da UI) | `CicloDeVidaTest` | M45, M46, M50 |
| CT-23 | excluir × 5 situações | R10 | estado × operação | Feature | idem | M45, M50 |
| CT-24 | enviar × 5 situações, com o não-efeito de notificação | R10 | estado × operação | Feature | idem | M50, M73 |
| CT-25 | aprovar × 5 situações | R10 | estado × operação | Feature | idem | M46, M47, M50 |
| CT-26 | rejeitar × 5 situações, com o não-efeito de histórico | R10 | estado × operação | Feature | idem | M47, M50 |
| CT-27 | cancelar × 5 situações × 2 personas | R10 | estado × operação | Feature | idem | M46, M48, M49, M50 |
| CT-28 | a listagem mostra a situação **na linha** de cada solicitação | R11 | **EP exaustiva** | componente | `AndamentoTest` | M51, M52, M74 |
| CT-29 | o detalhe mostra as decisões, os autores, as datas e o motivo | R11 | EP | componente | idem | M53, M54, M55 |
| CT-30 | a solicitação de outra organização não aparece nem abre | R12 | IDOR | componente + rota | `IsolamentoTest` | M57, M58 |
| CT-31 | ninguém de outra organização decide, seja gestor ou diretor | R12 | IDOR | Feature (fora da UI) | idem | M59, M81 |
| CT-32 | a autoridade é do gestor de agora — os dois lados da troca | R4 | persona | Feature | `AutoridadeTest` | M23, M64 |
| CT-33 | a tela oferece as ações só a quem pode usá-las | R11 | affordance × persona | componente | `AndamentoTest` | M56 |
| CT-34 | **todos** os diretores são avisados, cada um uma vez | R8 | cardinalidade | Feature | `NotificacaoTest` | M70, M71 |
| CT-35 | sem nenhum diretor, a solicitação não avança | R6 | cardinalidade | Feature | `EnvioTest` | M67, M30 |
| CT-36 | a diretora alcança a solicitação que precisa decidir | R9 | persona × tela | componente | `AndamentoTest` | M72, M43 |
| CT-37 | o domínio de valor e texto vale também na edição | R1 | BVA + normalização | componente | `SolicitacaoCompraFormTest` | M60, M61, M4 |
| CT-38 | o domínio é recusado também fora da tela | R1 | gate de camada | Feature (fora da UI) | `SolicitacaoCompraTest` | M62 |
| CT-39 | o usuário comum não cria nem edita centro de custo | R7 | papel × operação | componente | `CentroCustoAutorizacaoTest` | M68 |
| CT-40 | a guarda de corrida vale nas outras três transições | R5 | concorrência × transição | Feature | `ConcorrenciaTest` | M65, M66, M25, M26 |
| CT-41 | o colega da organização lê, mas não age | R11 | IDOR intra-organização | componente | `AndamentoTest` | M75, M56 |
| CT-42 | o nome do centro é único dentro da organização | R7 | EP + escopo | componente | `CentroCustoFormTest` | M69, M79 |
| ~~CT-43~~ | **retirado** — subsumido pela linha `gestor × sobe` de CT-46 | — | — | — | — | — |
| CT-44 | o detalhe abre em qualquer situação e mostra a do registro | R10, R11 | estado × operação | componente | `AndamentoTest` | M51 |
| CT-45 | o reenvio depois da rejeição do **diretor** recomeça pelo gestor | **R13** | 2-switch | Feature | `ReenvioTest` | M16, M17, M76 |
| CT-46 | a alçada do reenvio, nas duas direções e nas duas origens de rejeição | **R13** | produto 2×2 | Feature | idem | M11, M76, M77 |
| CT-47 | o usuário comum não troca o gestor nem por fora da tela | R7 | gate de camada | Feature (fora da UI) | `CentroCustoAutorizacaoTest` | M78 |

**47 cenários · 13 regras · 81 mutantes previstos (M1…M81, sem lacuna na numeração) ·
0 sem matador · 4 lacunas declaradas · 1 cenário retirado por subsunção (CT-43).**

Todos os arquivos previstos ficam em `tests/FeatureTenancy/Compras/`, exceto CT-18
(`tests/Kit/PaineisTest.php`). Ver `## Setup Global` para o porquê da suíte.

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| a modal de rejeição recusa o campo vazio pela tela | mora no `05` (CT-B02), onde prova outra coisa: que o usuário **vê** a recusa. Como cobertura de domínio, CT-09 é mais barato e mais forte |
| aprovar uma solicitação inexistente / com id de outro registro | mata o mesmo mutante que CT-30 (route binding), pela mesma via |
| o solicitante consegue ver a própria solicitação | caminho feliz de leitura já exercitado como precondição de CT-28, CT-29 e CT-44 |
| o log de cada transição sai no channel `compras` | oráculo do **plano**, não do requisito. Ver `## Fronteira com o Plano` |
| um cenário `Unit` para a comparação `valor > limite` | a camada não existe neste arnês: `tests/Unit` não tem `TestCase` ligado. CT-04 cobre em `Feature` |
| cancelar depois de aprovada por outra pessoa que não a solicitante | dupla célula inválida (situação **e** persona) no mesmo cenário — a primeira barreira mascara a segunda. Separadas em CT-27 |
| a Dora também é notificada quando ela mesma já aprovou | a etapa deixa de estar pendente na mesma transição; nenhum mutante previsto sobrevive a ele que CT-34 e CT-20 não matem |
| **CT-43 — "a alçada é reavaliada com o valor do momento do envio"** | **retirado na rodada 2 por subsunção**: a linha `gestor × sobe` de CT-46 mata exatamente o mesmo mutante (M11), dentro de um `Esquema` que também cobre as outras três células do produto. Dois cenários que matam o mesmo conjunto de mutantes → mantém-se um, e mantém-se o mais forte. O ID fica **retirado** e não é reaproveitado, para não quebrar as referências |
| um `Esquema` de reenvio percorrendo também `aprovada` e `cancelada` | não são estados de onde se reenvia — a matriz de R10 (CT-24, linhas terminais) já prova que o envio é recusado ali |

---

## Revisão Adversarial

**Executada por sub-agente independente**, que recebeu apenas `00-requisito.md`, `04` e `05`, e
**não** recebeu o `01-plano-acao.md`, o código nem o raciocínio da derivação (a proibição de
autorrevisar é dura: modelos são melhores em **gerar** oráculo do que em **classificar** se um
oráculo está correto).

### Rodada 1 — o que ela achou

| # | Defeito que atravessava intacto | Regra | Técnica que faltava | Fechamento |
|---|---|---|---|---|
| **D1** | só o **primeiro** diretor é notificado (`->first()`, a leitura do singular do card); e **zero** diretores é silencioso, prendendo a solicitação para sempre | R8, R6 | **cardinalidade do destinatário (0/1/N)** | **CT-34** e **CT-35** |
| **D2** | o papel `diretor` existe na matriz e **não alcança tela nenhuma** — nenhum cenário punha a diretora diante de uma tela; a segunda etapa de aprovação seria inalcançável com tudo verde | R9, R11 | **persona × tela** | **CT-36**, e a linha da Diana em **CT-33** |
| **D3** | a validação de domínio mora só na página de criação; editar para −1,00 ou descrição em branco passa. E `required` sem `trim` aceita `"   "` na descrição | R1, R10 | **fronteira no ponto de edição** + **normalização assimétrica** | **CT-37** e **CT-38** |
| **D4** | `CentroCustoResource` com barreira só em `canViewAny()`; `create`/`edit` herdam `true` → **a escalada de privilégio de A-08, intacta** | R7 | **papel × operação** (a "ação" tinha colapsado em "abrir a listagem") | **CT-39** |
| **D5** | a guarda de corrida existe só na transição do diretor; o duplo clique do gestor grava duas etapas e o histórico de RQ-13 mente | R5, R3, R11 | **concorrência × transição** (1 de 4 células) | **CT-40**, e a contagem em CT-08 |
| **D6** | a listagem sem coluna de situação passa: o `SelectFilter` põe os cinco rótulos no HTML e o `assertSee` de página fica verde com **RQ-12 não implementado** | R11 | **asserção ancorada no registro** | **CT-28** reescrito |
| **D7** | o nome do centro de custo único **global** em vez de por organização — CT-16 nunca tentava duplicar | R7, R12 | partição de duplicidade × escopo | **CT-42** |
| **D8** | a troca de gestor deixa a solicitação inaprovável por **qualquer um** — CT-32 só afirmava quem perdeu a autoridade | R4, R6 | par positivo do cenário de premissa | **CT-32** virou `Esquema` com os dois lados |

**Oráculos fracos apontados e reescritos**: CT-12 (oráculo no **retorno** da chamada — removido),
CT-14/CT-15 (dividido em CT-15a/CT-15b, com o positivo ancorado no registro), CT-17/CT-19 (não
afirmavam **a qual solicitação** o aviso se refere), CT-18 (não quantificado), CT-20 (só negativo,
sem âncora de que a ação aconteceu), CT-22 linha `rascunho` (não afirmava a situação final), CT-24
(sem não-efeito de notificação), CT-26 (sem não-efeito de histórico — o que **invalidava a
atribuição de M50** naquela coluna), CT-29 (sem contagem e sem data esperada), CT-30 (sem situação
de partida e sem registro irmão visível), CT-32 (sem não-efeito de histórico).

**`Quando` composto**: CT-07 (dividido em CT-07 + CT-43 — este último depois **retirado** na
rodada 2, por subsunção em CT-46), CT-08 (a correção foi para o `Dado`), CT-15 (dividido em
CT-15a/CT-15b), CT-33 (virou `Esquema`).

**Auditoria da matriz**: a aritmética (**40 / 19 / 21**) estava **correta**, mas 4 das 40 células
(`ver detalhe` fora de `aprovada`) eram **argumentadas, não executadas** — fechadas por **CT-44**.
A coluna `ver detalhe` não tinha dimensão de persona — fechada por CT-44 e CT-41.

**Falsos ✅ do checklist**: dez itens estavam marcados como cobertos ou dispensados com o defeito
correspondente atravessando. Todos reescritos acima, com o cenário que de fato os mata. As três
lacunas declaradas originais (A-17, A-18, A-19) foram confirmadas como **honestas** pela revisão —
não são falsos ✅ —, e uma quarta (A-22) foi acrescentada.

**Eixos confirmados como limpos pela revisão**: nenhum cenário sem `Então`; nenhum **oráculo
invertido** (todo cenário positivo fixa a situação de partida) — exceto CT-30, que era negativo e
foi corrigido.

### Rodada 2 — a superfície nova que a rodada 1 criou

O fechamento da rodada 1 criou **11 cenários novos**, e cenário novo introduz superfície nova. A
rodada 2 foi disparada por isso, com o mesmo contrato e sem o PRD. **É a última — teto de 2.**

| # | Achado | Onde | Fechamento |
|---|---|---|---|
| **L1** | o conjunto **nunca reenviava depois de uma rejeição do diretor** — todos os ciclos partiam do gestor | R3 + R2 | **CT-45**, e a regra **R13** |
| **L2** | a reavaliação da alçada só era derivada na direção de **subida**; a variante monotônica (`||=`) atravessava | R2 | **CT-46**, linhas `desce` |
| **L3** | a persona estrangeira existia só como **gestor**; "diretor de outra organização" não tinha cenário | R12 | **CT-31** virou `Esquema` |
| **L4** | **CT-40 tinha oráculo invertido**: afirmava "exatamente uma decisão" numa célula em que o correto são duas — só ficava verde com a implementação que apaga o histórico | R5 | contagem separada por etapa e total |
| **L5** | **CT-35 mudou o contrato de seis cenários antigos** ao instituir falha-fechado sem diretor | R2/R6/R10 | precondição no `Dado` de CT-04, CT-05, CT-06, CT-11, CT-25, CT-40 |
| **L6** | **CT-42 contradizia CT-15b** (a Alice não alcança a Globex) e não tinha âncora de persistência | R7 | persona Bianca + âncoras |
| **L7** | **CT-34 herdou o oráculo fraco** que a rodada 1 corrigira em CT-19: uma só solicitação, então "se refere àquela" era verdade sempre | R8 | solicitação-irmã no `Dado` |
| **L8** | a direção "**e ninguém mais**" existia só na etapa do gestor | R8 | exclusão explícita em CT-34 |
| **L9** | **CT-44 usava a forma de oráculo que D6 condenou** (`assertSee` de página) e misturava as dimensões situação e persona | R10/R11 | persona fixada + âncora no registro |
| **L10** | **falso ✅**: o item "fora do componente de UI" de R7 citava CT-14, que **consulta** a matriz em vez de exercer a barreira | R7 | **CT-47** |
| **L11** | *"timezone: não se aplica"* ficou meio-falso depois que CT-29 ganhou oráculo de data | R11 | instante no fuso da aplicação, e o item dividido em comparação × exibição |

**Três implementações erradas que a rodada 2 provou atravessarem a v2 inteira**, todas fechadas:
`enviar()` derivando a etapa seguinte do **histórico** (M76), alçada **monotônica** (M77), e a
barreira do diretor como `hasRole('diretor')` **sem recorte de organização** (M81).

**Eixos confirmados limpos na rodada 2**: nenhum cenário sem `Então`; nenhum `Quando` composto
sobreviveu; a aritmética da matriz de R10 (**40 / 19 / 21**) continua correta depois de CT-44,
com as 21 células inválidas executadas, nenhuma coluna sem célula válida e nenhuma resolvida por
citação; A-17, A-18, A-19 e A-22 continuam **honestas** — nenhuma virou falso ✅.

---

## Escalada

A skill fixa **teto de 2 rodadas** de revisão adversarial, e o critério para parar é explícito:
*"se a segunda rodada ainda trouxer achado estrutural, o problema não é o conjunto — é a regra, que
provavelmente deveria ser duas. Registrar e escalar."*

**A rodada 2 trouxe um achado estrutural**, e ele foi resolvido exatamente assim:

> **RQ-09 não tinha dono.** O comportamento do reenvio estava repartido entre R2 (a alçada) e R3 (o
> histórico), e **cada uma o derivava a partir do único ponto de rejeição que conhecia** — o
> gestor. Nenhuma das duas enxergava o eixo inteiro, e por isso o produto
> `{quem rejeitou} × {direção da mudança de valor}` nunca foi montado: das 4 células, a v2
> executava **uma**. Nenhuma quantidade de revisão sobre R2 e R3 como estavam geraria as outras
> três.

**R3 foi separada em R3 (rejeição) e R13 (reenvio)**, e as quatro células passaram a existir por
construção, em CT-46.

**Não há rodada 3.** O teto foi atingido, e o que ele protege é real: iterar uma terceira vez sobre
o mesmo conjunto tem retorno decrescente e custo de contexto crescente. **O que fica aberto e vai
para o usuário**, sem que este conjunto o resolva sozinho:

1. **Cinco premissas** (`@premissa`: A-13, A-15, A-20, A-21, e a de mecanismo de A-14) sustentam
   nove cenários. Nenhuma delas foi confirmada por ninguém — o usuário não estava disponível nesta
   execução, e cada uma traz o "se negado" que diz o que muda.
2. **Quatro lacunas declaradas** (A-17, A-18, A-19, A-22) continuam dívida conhecida, por decisão:
   fechá-las exigiria números e comportamentos que só o **plano** determina, e um cenário derivado
   do plano não é oráculo.
3. **Duas divergências de arnês** com o `01-plano-acao.md`, que é imutável nesta entrega: a suíte
   de destino dos CT e a natureza da regressão de `PaineisTest`.

Se a terceira rodada for feita algum dia, o lugar de começar é o **produto de R13** (as quatro
células ainda não têm nenhum cenário de **notificação** cruzando com elas) e a **matriz de R7**
(o `delete` do centro de custo com solicitações pendentes apontando para ele).

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` desta feature é **imutável nesta entrega** (é linha de
> base de comparação). A skill manda devolver as perguntas novas para `## Ambiguidades` do `00`;
> como o arquivo está fechado, elas ficam aqui, **em bloco pronto para colagem**, no mesmo formato
> da seção de destino. Cada uma continua bloqueando o que depende dela.

```markdown
### A-13 — a alçada é reavaliada quando o valor muda entre um envio e outro? (RQ-05, RQ-09)

**Assumido**: **sim** — a alçada é lida a cada envio. Congelá-la criaria um caminho para escapar
do diretor: enviar barato, ser rejeitado, corrigir para caro.
**Se negado**: CT-46 muda de oráculo nas quatro linhas e M11 deixa de ser mutante.

### A-14 — a rejeição do diretor devolve ao rascunho ou ao gestor? (RQ-08)

**Assumido**: **volta ao rascunho, e o ciclo recomeça pelo gestor** — leitura literal, e a única
que não inventa um estado que o card não nomeia.
**Se negado**: CT-08 e CT-10 mudam de oráculo, e a matriz de R10 ganha uma situação.

### A-15 — quem decide quando o gestor do centro de custo muda depois do envio? (RQ-04)

**Assumido**: **o gestor atual**. Congelar o gestor no envio exigiria uma coluna que o card não
pede e prenderia a solicitação quando o gestor sai da empresa.
**Se negado**: CT-32 inverte nos dois lados.

### A-16 — qual o texto que o usuário lê quando a ação é recusada?

**Assumido**: nenhum cenário usa texto de erro como oráculo — os `Então` afirmam a **situação** e
o **não-efeito**. Se o texto for requisito, precisa virar cláusula.

### A-17 — a listagem tem ordem e tamanho de página definidos? (RQ-12)

**Assumido**: os defaults do painel. **Lacuna declarada** no checklist.

### A-18 — há limite de tamanho para a descrição e para a justificativa? (RQ-01, RQ-07)

**Assumido**: sem limite declarado pelo requisito. **Lacuna declarada** — a borda do `varchar` não
virou cenário porque 255 é número do plano.

### A-19 — editar sem alterar nada, e excluir duas vezes: qual o comportamento? (RQ-02, RQ-03)

**Assumido**: salvar sem alterar é aceito e não muda nada; excluir a segunda vez encontra um
registro que não existe. **Lacuna declarada** — nenhum dos dois tem cenário próprio.

### A-20 — e se a organização não tiver nenhum diretor no momento da aprovação do gestor? (RQ-05)

Caso de borda simétrico ao de A-10, e não coberto por ele: A-10 trata o **gestor** ausente; este
trata a etapa do **diretor** sem ninguém que a possa decidir.

**Assumido**: **falha fechado** — a aprovação do gestor é recusada e a solicitação fica em
"aguardando gestor", pelo mesmo raciocínio de A-10. As alternativas são piores: aprovar sem
aprovador, ou prender a solicitação em "aguardando diretor" sem sinal nenhum.
**Se negado**: CT-35 muda de oráculo.

### A-21 — o colega da mesma organização pode LER a solicitação alheia? (RQ-12, RQ-13)

O card diz "mostrar na tela o status atual" sem restringir a quem. A organização já é a fronteira
que o requisito reconhece implicitamente.

**Assumido**: **lê e não age** — a solicitação é visível dentro da organização, e nenhuma ação de
decisão, edição ou exclusão é oferecida a quem não é o dono nem o aprovador da vez.
**Se negado** (visibilidade restrita ao dono e aos aprovadores): CT-41 inverte, e CT-28/CT-30
ganham uma dimensão de persona.

### A-22 — o que acontece se uma justificativa for enviada junto de uma APROVAÇÃO? (RQ-06, RQ-07)

RQ-07 exige a justificativa **na rejeição** e o card nada diz sobre a aprovação.

**Assumido**: indefinido. **Lacuna declarada** — nenhum cenário passa justificativa numa aprovação,
porque o comportamento esperado (ignorar? recusar? gravar no histórico da aprovação?) viria do
plano e não do requisito.
```

**Perguntas que bloqueiam algo**:

- **A-13** bloqueia **R13**/CT-46 · **A-14** bloqueia **R13**/CT-45 · **A-15** bloqueia R4/CT-32 ·
  **A-20** bloqueia R6/CT-35 · **A-21** bloqueia R11/CT-41 — os cinco cenários estão marcados
  `@premissa`
- **A-16**, **A-17**, **A-18**, **A-19**, **A-22** não bloqueiam cenário: elas **são** as lacunas
  declaradas do checklist

**Fora do `00`, para o time** — duas divergências de arnês:

1. o passo 10 do `01-plano-acao.md` prevê `tests/FeatureTenancy` para dois casos; pela leitura de
   `app/Traits/BelongsToTenant.php:72-78` e de `tests/Pest.php`, **o conjunto inteiro pertence a
   essa suíte**, porque `tenant_id` é NOT NULL e só é preenchido com organização no contexto;
2. o `01` prevê `tests/Kit/PaineisTest.php` vermelho por **contagem** de permissions; o arquivo
   **não assere contagem de painel nenhuma** (só `master_global → 0`), então a regressão será
   estrutural, não numérica.

---

## Fechamento do Ciclo — depois de implementar

```bash
composer require pestphp/pest-plugin-mutate --dev     # hoje é só transitivo
vendor/bin/pest --testsuite=FeatureTenancy --mutate --path=app/Models/SolicitacaoCompra.php
```

**O que o mutation score deste conjunto NÃO vai responder**: ele só muta código que existe. As
cláusulas que ninguém implementou — a etapa do diretor que nunca foi escrita, a barreira de
identidade que nunca foi chamada, o `canEdit()` do `CentroCustoResource` que herdou `true` — não
geram mutante e não derrubam o score. **Cinco dos oito defeitos que a revisão adversarial achou
são exatamente dessa espécie: comportamento ausente, sem linha para mutar.** Quem responde por
omissão aqui é a rastreabilidade `RQ` → regra → cenário e os 75 mutantes **de especificação**,
que nasceram do requisito e não do código.

Mutante sobrevivente vira lacuna de derivação e volta como cenário novo, com a técnica que faltou
nomeada.

---

## Achados da Rodada 2

Registrados em `## Revisão Adversarial` → *Rodada 2*, e o desfecho estrutural em `## Escalada`.
Esta seção fica aqui só como âncora dos links internos.
