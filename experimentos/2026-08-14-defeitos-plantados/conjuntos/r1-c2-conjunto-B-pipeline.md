# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> a feature ainda não existe. O `01-plano-acao.md` foi lido **apenas** para nomes de rota, paths
> de arquivo, a tabela `## Superfície de UI` e a stack; nenhuma linha dele foi usada como oráculo
> de comportamento.

## Nota de execução

O usuário **não estava disponível** nesta derivação. Toda pergunta que a skill manda escalar está
registrada em `## Perguntas em Aberto`, com a premissa adotada, e **todo cenário que depende de uma
premissa está marcado `@premissa`**, com o identificador da pergunta.

**Desvio declarado da skill**: a skill manda replicar as perguntas em `00-requisito.md` →
`## Ambiguidades`. Isso **não foi feito**: o `00-requisito.md` desta feature é compartilhado com
outra derivação em curso e alterá-lo mudaria a entrada de quem já derivou a partir dele. As
perguntas estão aqui, no formato que o `00` espera, prontas para serem coladas quando a derivação
paralela terminar. Nenhum outro item do pipeline foi omitido.

## Versões confirmadas (`composer.json`)

| Peça | Versão | O que isso muda no CT |
|---|---|---|
| `laravel/framework` | `^13.17` | `assertDatabaseHas`, `travelTo`, `Notification::fake` |
| `filament/filament` | `^5.6` | **`assertSchemaStateSet`**, não `assertFormSet` (v3). `callAction(TestAction::make(...)->table())`, não `callTableAction` |
| `pestphp/pest` | `^5.1` | datasets nomeados, `--tia`, `--mutate` (via `pest-plugin-mutate`, presente em `vendor/`) |
| `pestphp/pest-plugin-browser` | `^5.0` | servidor in-process; `visit()`, `assertPathIs`, `assertNoJavaScriptErrors` |
| `bezhansalleh/filament-shield` | `^4.2` | matriz de permissões por painel; os dois seeders |
| `spatie/laravel-permission` | via shield | `permission.teams` — exige `Tests\TenancyTestCase` |

Todas as assertions citadas neste arquivo foram conferidas em `vendor/filament/**/Testing/`:
`assertSchemaStateSet`, `assertHasFormErrors`, `assertHasActionErrors`, `assertActionHidden`,
`assertActionVisible`, `assertCanSeeTableRecords`, `assertCanNotSeeTableRecords`,
`assertTableColumnStateSet`, `assertTableColumnFormattedStateSet`, `filterTable`, `callAction`,
`assertNotified`, `assertMountedActionModalSee`, `TestAction::make()->table()`.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Justificativa da nota |
|---|---|---|---|---|---|
| Máquina de estados (enviar / aprovar / rejeitar / cancelar) | 3 | 3 | **9** | **completo** | concorrência real (dois diretores) + regra com muitas condições; autorização e irreversibilidade |
| Alçada do diretor (R$ 5.000) | 3 | 3 | **9** | **completo** | decisão de fluxo sobre valor monetário na fronteira; erra silencioso e vira compliance |
| Autorização (quem decide + matriz de permissão do centro de custo) | 3 | 3 | **9** | **completo** | integra shield + spatie + tenancy; escalada de privilégio (A-08) |
| Isolamento por organização | 3 | 3 | **9** | **completo** | dado de terceiro; falha aberta é vazamento entre clientes |
| Rejeição e justificativa | 2 | 3 | **6** | padrão→**completo** | elevado a completo: RQ-07 é a única restrição dura do card e a exigência tem duas moradas (tela e model) |
| Notificação do próximo aprovador | 2 | 2 | **4** | padrão | integra com a fila existente; o fluxo para, não corrompe |
| Nascimento e edição do rascunho | 2 | 2 | **4** | padrão | CRUD sobre componente existente; reversível pelo próprio solicitante |
| Exibição de situação e histórico | 2 | 2 | **4** | padrão | Resource novo, mas leitura; erro é visível e reversível |

- **Técnicas aplicadas**: EP, BVA 3-valores (incremento `0,01`), **tabela estado × evento (30 células,
  100% das inválidas cobertas)**, matriz papel × ação, rastreio de efeito colateral, normalização de
  ausente/nulo/vazio, teste de concorrência.
- **Pairwise: não aplicado.** Nenhuma regra desta feature tem ≥3 parâmetros independentes — a única
  combinação com mais de dois eixos (situação × papel × etapa) é a tabela estado × evento e a matriz
  papel × ação, cobertas integralmente. Pairwise ali seria redutor de um conjunto que não precisa
  ser reduzido.
- **Regras**: 13 · **Cenários**: 45 (`CT-01`…`CT-45`) + 2 `CT-B` · **Mutantes previstos**: **69**
  neste arquivo + **7** no `05` = **76** · **Sem matador**: **2** (M46, M51 — lacunas declaradas,
  com motivo e mitigação).
- **Nenhum cenário sem mutante morto.** Todo `CT` do índice aparece na coluna "Cenário que mata" de
  ao menos um mutante — o critério de corte do passo 7 da skill.

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | 3 tabelas (`centros_custo`, `solicitacoes_compra`, `etapas_aprovacao_compra`), enum de 5 situações, 2 policies, 1 notification, papel `diretor`, 2 Resources no painel `app`, channel de log, chave de config do limite | CT-15, CT-37, CT-41 |
| **F**unction | criar / editar / excluir rascunho; enviar; aprovar (2 etapas); rejeitar com justificativa; cancelar; rotear por alçada; exibir situação e histórico; notificar. **Função administrativa escondida**: cadastrar centro de custo é o que define *quem aprova* — é privilégio disfarçado de CRUD | CT-01…CT-36, CT-37…CT-41 |
| **D**ata | descrição (texto livre), valor (`decimal(12,2)`), centro de custo (FK, **gestor pode ser nulo**), situação (5 valores), justificativa (texto livre, nula na aprovação), etapas (0…N, append-only). **Dado de outro tenant**: solicitação e centro de custo de outra organização. **Cardinalidade**: 0, 1 e 2 etapas | CT-04, CT-10, CT-13, CT-20, CT-22, CT-42…CT-45 |
| **I**nterfaces | UI Filament (listagem, form create/edit, view, 4 ações), rotas do painel `/app/{tenant}`, **os métodos públicos do model chamados direto** (job, comando, seeder, rota de API futura — o chamador que a policy não vê), e-mail, log | CT-11, CT-16, CT-20, CT-29 |
| **P**latform | SQLite `:memory:` no teste × MySQL/Postgres em produção — **`decimal` volta como string no SQLite**, e comparar string com número inverte a ordem em `10.000,00`; fila `database` em produção × `sync` no `phpunit.xml`; `permission.teams` exige `TenancyTestCase`, que fixa a flag antes das migrations | CT-13 (linha lexicográfica), CT-42…CT-45 |
| **O**perations | 5 personas: solicitante (`panel_user`), gestor (um `panel_user` apontado por `gestor_id`), diretor (papel `diretor`), administrador da organização, `master_global`. **Uso indevido previsto**: aprovar a própria solicitação, decidir fora da vez, editar `gestor_id` para se nomear aprovador. Volume: listagem com filtro por situação | CT-16, CT-36, CT-37…CT-40 |
| **T**ime | **concorrência**: dois diretores decidindo ao mesmo tempo, duplo clique em Enviar; **ordem**: diretor antes do gestor; `updated_at` na transição; histórico ordenado por `created_at`, com empate possível dentro do mesmo segundo | CT-12, CT-24, CT-29, CT-30, CT-35 |

**Dimensões sem cenário próprio, declaradas:**

- **Timezone / DST**: sem cenário. A feature não tem prazo, agendamento, expiração nem comparação de
  datas — `created_at` das etapas é só exibido. O `00` declara SLA e escalonamento fora de escopo.
  Se um prazo de aprovação entrar, esta linha vira cenário obrigatório.
- **Upload**: sem cenário. Anexos estão fora de escopo por declaração do `00`.

---

## Mapa de Regras

| Regra | Origem (`RQ` / `A`) | Técnica formal | Cenários |
|---|---|---|---|
| **R1** — A solicitação nasce em rascunho com os três campos obrigatórios; situação e solicitante não vêm do formulário | RQ-01 | EP + mass assignment + BVA de domínio | CT-01…CT-04 |
| **R2** — Rascunho é a única situação editável e excluível, e só pelo solicitante dono | RQ-02, RQ-03, RQ-10 | matriz papel × ação + estado × evento (recorte) | CT-05…CT-08 |
| **R3** — Enviar move rascunho → aguardando gestor; sem gestor no centro de custo o envio é recusado e a solicitação **fica em rascunho** | RQ-04, A-10 | EP + idempotência | CT-09…CT-12 |
| **R4** — Valor **estritamente acima** do limite exige a etapa do diretor, **depois** da do gestor | RQ-05, A-04 | **BVA 3-valores** (fronteira `valor`, incremento `R$ 0,01`) | CT-13…CT-15 |
| **R5** — Decide quem é o aprovador **da vez**: o gestor do centro na etapa de gestor, quem tem o papel `diretor` na etapa de diretor | RQ-06, A-03, A-07, A-09 | **matriz papel × ação** | CT-16…CT-18 |
| **R6** — Rejeitar exige justificativa não vazia, devolve a solicitação a rascunho e **preserva o histórico** | RQ-06, RQ-07, RQ-08, RQ-09 | EP (ausente ≠ nulo ≠ vazio) + rastreio de efeito | CT-19…CT-23 |
| **R7** — Todo par (situação, evento) fora do desenho é recusado **sem alterar a situação** | RQ-10, RQ-11, A-05, A-06 | **tabela estado × evento** (30 células) | CT-24, CT-25 |
| **R8** — Cancelar é do solicitante e só enquanto a solicitação está em trânsito | RQ-11, A-06 | matriz papel × ação + estado × evento (recorte) | CT-26…CT-28 |
| **R9** — A decisão é atômica: duas decisões simultâneas produzem **uma** transição e **uma** etapa | RQ-06 + taxonomia (concorrência) | teste de concorrência | CT-29, CT-30 |
| **R10** — O e-mail vai ao **próximo aprovador**, uma única vez, e a mais ninguém | RQ-14, A-11 | **rastreio de efeito colateral** (aconteceu / não aconteceu / uma só vez) | CT-31…CT-33 |
| **R11** — A tela mostra a situação atual e o histórico de quem decidiu cada etapa, quando e por quê | RQ-12, RQ-13, A-12 | EP sobre estado de exibição | CT-34…CT-36 |
| **R12** — Centro de custo é entidade de **administração da organização**: o usuário comum não recebe a permissão de mexer nele | RQ-04, A-08 | matriz papel × ação | CT-37…CT-41 |
| **R13** — Solicitação e centro de custo de outra organização não são visíveis nem alcançáveis | A-01, A-03 + taxonomia (IDOR) | matriz papel × ação + IDOR | CT-42…CT-45 |

**Cobertura das cláusulas** — toda `RQ` do `00` gerou ao menos uma regra:

| RQ | Regra(s) | RQ | Regra(s) |
|---|---|---|---|
| RQ-01 | R1 | RQ-08 | R6 |
| RQ-02 | R2 | RQ-09 | R6 |
| RQ-03 | R2 | RQ-10 | R2, R7 |
| RQ-04 | R3, R5, R12 | RQ-11 | R7, R8 |
| RQ-05 | R4 | RQ-12 | R11 |
| RQ-06 | R5, R6, R9 | RQ-13 | R11 |
| RQ-07 | R6 | RQ-14 | R10 |

**Leitura do mapa** (sinais que a skill manda conferir antes de seguir):

- **Nenhuma regra ficou sem exemplo.** Todas as 13 têm ao menos 2 cenários.
- **Nenhum exemplo ficou sem regra.**
- **Perguntas vermelhas: 8.** Está no limite do aceitável. Sete delas são de **borda**, não de
  desenho — respondê-las muda linhas de cenário, não a estrutura da feature. A oitava (P-03: para
  onde volta a rejeição do diretor) **muda o desenho** e é a que deve subir primeiro ao usuário.

---

## Perguntas em Aberto

> Formato pronto para colar em `00-requisito.md` → `## Ambiguidades`. Cada uma tem premissa adotada,
> os cenários que dependem dela (marcados `@premissa`) e o que muda se a premissa for negada.

### P-01 — Valor zero ou negativo é uma solicitação válida? (RQ-01)

O card diz "com descrição, valor e centro de custo" e não define o domínio de `valor`.

**Premissa**: **valor tem de ser maior que zero**. Uma compra de R$ 0,00 não tem o que aprovar, e um
valor negativo é um estorno — coisa que o card não descreve.
**Se negado**: cai a metade inválida de CT-04; a fronteira do diretor (R4) não muda.
**Depende**: CT-04.

### P-02 — Os três campos são todos obrigatórios? (RQ-01)

"cria uma solicitação **com** descrição, valor e centro de custo" — a leitura literal é que os três
compõem a solicitação.

**Premissa**: **os três são obrigatórios**.
**Se negado** (descrição opcional, por exemplo): a linha correspondente de CT-02 vira caso positivo.
**Depende**: CT-02.

### P-03 — A rejeição do **diretor** devolve a rascunho ou volta ao gestor? (RQ-06, RQ-08, A-07)

RQ-08 diz "solicitação rejeitada volta para rascunho", numa frase que o card escreve logo depois de
falar do **gestor**. A-07 estende a rejeição ao diretor sem dizer para onde ela devolve. As duas
leituras são defensáveis: voltar a rascunho descarta a aprovação do gestor; voltar ao gestor mantém
uma aprovação que talvez não valha mais para um pedido corrigido.

**É a pergunta de maior impacto desta derivação** — muda o desenho, não uma borda.
**Premissa**: **volta para rascunho**, como qualquer rejeição. O card não distingue as duas etapas,
e reaproveitar a aprovação do gestor sobre um pedido que ainda vai ser editado seria decidir por ele.
**Se negado**: R6 ganha uma transição nova (`aguardando_diretor → aguardando_gestor`), a tabela de
R7 ganha uma célula válida, e CT-23 inverte o resultado esperado.
**Depende**: CT-23, e a linha `aguardando_diretor × rejeitar` de CT-24.

### P-04 — No reenvio, o ciclo recomeça pelo gestor? (RQ-09)

**Premissa**: **sim** — RQ-04 diz "quando envia, a solicitação vai para o gestor", sem ressalva para
o reenvio.
**Se negado**: CT-22 muda o resultado esperado do segundo ciclo.
**Depende**: CT-22.

### P-05 — A alçada é reavaliada no reenvio? (RQ-05, RQ-09)

Uma solicitação de R$ 6.000 rejeitada e corrigida para R$ 4.000 exige diretor de novo?

**Premissa**: **a alçada é avaliada com o valor corrente, a cada aprovação de gestor**. Congelar a
decisão no primeiro envio faria o valor corrigido não valer para nada.
**Se negado**: CT-13 precisa de uma linha de reenvio com valor alterado.
**Depende**: CT-22 (segundo ciclo), CT-13.

### P-06 — Cancelada é estado terminal? (RQ-11)

O card não descreve saída de `cancelada`; o `00` recusa "reabertura de solicitação cancelada" em
Fora de Escopo, o que é evidência indireta.

**Premissa**: **sim, terminal**, como `aprovada`.
**Se negado**: 6 células da tabela de R7 mudam de inválidas para válidas.
**Depende**: as 6 linhas de `cancelada` em CT-24.

### P-07 — Alguém que é gestor **e** diretor recebe dois e-mails? (RQ-14, A-03)

**Premissa**: **um e-mail por etapa**. Ao aprovar como gestor uma solicitação acima do limite, a
mesma pessoa é notificada da etapa de diretor — porque a notificação é da *etapa*, não da pessoa.
**Se negado**: CT-32 ganha uma linha de supressão.
**Depende**: CT-32.

### P-08 — Um empate de `created_at` no histórico tem desempate determinístico? (RQ-13)

Duas etapas gravadas no mesmo segundo (gestor e diretor sendo a mesma pessoa, com o clique seguido)
podem sair fora de ordem numa ordenação só por `created_at`.

**Premissa**: **a ordem do histórico é por `id` crescente**, que é monotônico e não empata.
**Se negado**: CT-35 precisa de tolerância na ordem.
**Depende**: CT-35.

---

## Setup Global

### Personas

Todas montadas com os helpers **que já existem** em `tests/Pest.php` — nenhum helper novo é criado
dentro de arquivo de teste, porque helper usado por mais de um arquivo tem de viver no `Pest.php`
(`.ai/rules/testes.md`, enforçado por `tests/Kit/HelpersDeTesteTest.php`).

| Persona | Como criar | Papel |
|---|---|---|
| `solicitante` | `usuarioCom('panel_user')` (ou `usuarioComPapel('panel_user', $acme)` com tenancy) | quem cria, envia e cancela |
| `gestor` | `usuarioCom('panel_user')` **apontado por** `centros_custo.gestor_id` | gestor **não é papel**: é uma FK |
| `outroGestor` | idem, gestor de **outro** centro de custo | persona da matriz papel × ação |
| `diretor` | `usuarioCom('diretor')` (papel novo, painel `app`) | segundo par de olhos acima do limite |
| `comum` | `usuarioCom('panel_user')` sem vínculo nenhum com a solicitação | o "usuário B" do IDOR |
| `adminDaOrganizacao` | `usuarioCom('admin_organizacao')` | quem cadastra centro de custo |

### Fixtures (factories novas)

- `CentroCusto::factory()` — `nome` do faker, `gestor_id` **explícito em todo CT**. Um `->semGestor()`
  para A-10.
- `SolicitacaoCompra::factory()` com um state por situação: `->rascunho()`, `->aguardandoGestor()`,
  `->aguardandoDiretor()`, `->aprovada()`, `->cancelada()`; e `->valor('4999.99')` recebendo **string
  ou `decimal`, nunca `float`**.
- `EtapaAprovacao::factory()` — usada só nos CT que precisam de histórico pré-existente (CT-35).

> **Armadilha herdada do projeto**: a `ConviteFactory` tem um default que concede o papel
> guarda-chuva (`role_id` = primeiro papel da tabela). As factories novas **não podem** repetir o
> padrão: `gestor_id`, `solicitante_id` e `centro_custo_id` sempre explícitos no CT, nunca sorteados.

### Fakes

- `Notification::fake()` em CT-10, CT-12, CT-31…CT-33, CT-45.
- **`Notification::fake()`, nunca `Mail::fake()` + `Mail::assertSent`**: a notificação é
  `ShouldQueue`, e `Mail::assertSent` nunca passa nesse caso — seria `assertQueued`. Com o fake de
  notificação a questão desaparece.
- `Log::partialMock()` no molde de `espiarAutenticacao()` para o channel `compras`, em CT-10 e CT-29
  — os únicos dois cenários em que o log é a evidência de que a recusa foi *diagnosticada*, e não
  engolida.
- Nada de `Http::fake()`: a feature não faz chamada externa.

### Estratégia de DB

`RefreshDatabase`, global pelo `tests/Pest.php`. Seeders no `beforeEach` de todos os arquivos, nesta
ordem — sem eles as duas telas respondem 403 para todo mundo que não seja `master_global`:

```php
beforeEach(function (): void {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
});
```

### Suítes

| Arquivo | TestCase | Por quê |
|---|---|---|
| `tests/Feature/SolicitacaoCompraFluxoTest.php` | `Tests\TestCase` | máquina de estados chamada no model |
| `tests/Feature/SolicitacaoCompraAutorizacaoTest.php` | `Tests\TestCase` | matriz papel × ação, policies, permissões |
| `tests/Feature/SolicitacaoCompraNotificacaoTest.php` | `Tests\TestCase` | rastreio de efeito |
| `tests/Feature/SolicitacaoCompraTelasTest.php` | `Tests\TestCase` | componentes Livewire do painel `app` |
| `tests/FeatureTenancy/SolicitacaoCompraTenancyTest.php` | `Tests\TenancyTestCase` | **R13**: `permission.teams` tem de estar ligado **antes** das migrations |
| `tests/Browser/SolicitacaoCompraBrowserTest.php` | `Tests\TestCase` | os 2 CT-B — ver `05-casos-de-teste-browser.md` |

> `tests/FeatureTenancy` **não existe ainda**: precisa de um bloco em `tests/Pest.php` e de uma
> testsuite em `phpunit.xml`. **Sem os dois, a pasta não é varrida e os CT-42…CT-45 passam por não
> existirem** — que é o pior modo de falha possível para um conjunto de teste. E a pasta **não pode**
> entrar no grupo `kit`: `composer test:kit` é o comando de resposta rápida do kit, e estes são
> testes de negócio.

---

## Regra R1 — A solicitação nasce em rascunho, com os três campos, e nem a situação nem o solicitante vêm do formulário

> `RQ-01` · perfil **padrão** · técnica: **EP** (campos obrigatórios, uma partição inválida por
> cenário) + **mass assignment** (taxonomia) + fronteira de domínio do valor

```gherkin
# language: pt
Funcionalidade: Fluxo de aprovação de solicitação de compra

  Regra: A solicitação nasce em rascunho, com descrição, valor e centro de custo, e o
         solicitante é quem a criou

    Cenário: [CT-01] a solicitação criada pelo formulário nasce em rascunho no nome de quem a criou
      Dado o solicitante autenticado no painel de negócio
      E um centro de custo "TI" com gestor definido
      Quando o solicitante grava uma solicitação de "Notebooks" no valor de R$ 3.200,00 para o centro "TI"
      Então a solicitação persistida tem descrição "Notebooks", valor "3200.00" e o centro "TI"
      E a situação dela é "rascunho"
      E o solicitante registrado é o usuário autenticado

    @premissa (P-02)
    Esquema do Cenário: [CT-02] a solicitação não é gravada sem um dos três campos
      Dado o solicitante autenticado no painel de negócio
      Quando ele tenta gravar uma solicitação com <campo> ausente
      Então o formulário acusa erro no campo "<campo>"
      E nenhuma solicitação é persistida

      Exemplos:
        | campo           | # partição inválida, isolada |
        | descricao       | texto obrigatório            |
        | valor           | número obrigatório           |
        | centro_custo_id | relação obrigatória          |

    Cenário: [CT-03] o formulário não decide a situação nem o dono da solicitação
      Dado o solicitante autenticado no painel de negócio
      Quando ele envia, junto do formulário, os campos "situacao" com "aprovada" e "solicitante_id" com o id de outra pessoa
      Então a solicitação persistida está em "rascunho"
      E o solicitante registrado continua sendo o usuário autenticado

    @premissa (P-01)
    Esquema do Cenário: [CT-04] o valor de uma compra é maior que zero
      Dado o solicitante autenticado no painel de negócio
      Quando ele tenta gravar uma solicitação no valor de <valor>
      Então o resultado é "<resultado>"

      Exemplos:
        | valor    | resultado | # borda (incremento R$ 0,01) |
        | -0,01    | recusado  | abaixo do domínio            |
        | 0,00     | recusado  | borda excluída               |
        | 0,01     | aceito    | borda+1, menor valor válido  |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `situacao` incluída no `$fillable` — o payload do formulário grava a situação que quiser | CT-03 |
| M2 | `solicitante_id` lido do payload em vez do usuário autenticado | CT-03 |
| M3 | a situação inicial não é atribuída na criação (coluna vazia ou default do banco) | CT-01 |
| M4 | `->required()` ausente no `Select` de centro de custo — um select com `->relationship()` *parece* obrigatório e não é | CT-02 (linha `centro_custo_id`) |
| M5 | nenhum piso no valor — R$ 0,00 e negativos entram | CT-04 (linhas `0,00` e `-0,01`) |

---

## Regra R2 — Rascunho é a única situação editável e excluível, e só pelo solicitante dono

> `RQ-02`, `RQ-03`, `RQ-10` · perfil **completo** · técnica: **matriz papel × ação** (ação destrutiva
> é obrigatória na matriz) + recorte da tabela estado × evento

```gherkin
# language: pt
  Regra: Enquanto está em rascunho, e só então, o solicitante dono edita e exclui a própria
         solicitação

    Cenário: [CT-05] o solicitante corrige o próprio rascunho e a correção persiste
      Dado um rascunho de "Notebooks" no valor de R$ 3.200,00 criado pelo solicitante
      Quando o solicitante grava a descrição "Notebooks e docks" e o valor R$ 3.800,00
      Então a solicitação persistida tem descrição "Notebooks e docks" e valor "3800.00"
      E a situação continua "rascunho"

    Cenário: [CT-06] o solicitante exclui o próprio rascunho
      Dado um rascunho criado pelo solicitante
      Quando o solicitante exclui a solicitação
      Então a solicitação não existe mais

    Cenário: [CT-07] o rascunho de uma pessoa não é editável por outra
      Dado um rascunho criado pelo solicitante
      E outro usuário do mesmo painel, autenticado
      Quando o outro usuário abre a listagem e a tela de edição desse rascunho
      Então as ações "Editar" e "Excluir" não lhe são oferecidas
      E a tela de edição responde 403

    Esquema do Cenário: [CT-08] editar e excluir só existem em rascunho
      Dado uma solicitação na situação "<situacao>", cujo solicitante é o usuário autenticado
      Quando ele procura a ação "<acao>" na listagem e abre a tela de edição
      Então a ação "<acao>" não lhe é oferecida
      E a tela de edição responde 403

      Exemplos:
        | situacao           | acao    | # célula inválida da tabela de R7 |
        | aguardando_gestor  | Editar  | já saiu das mãos do solicitante   |
        | aguardando_gestor  | Excluir | idem                              |
        | aguardando_diretor | Editar  | idem                              |
        | aguardando_diretor | Excluir | idem                              |
        | aprovada           | Editar  | RQ-10: não pode mais mexer        |
        | aprovada           | Excluir | RQ-10                             |
        | cancelada          | Editar  | terminal (P-06)                   |
        | cancelada          | Excluir | terminal (P-06)                   |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6 | a policy de `update` confere só a permissão, sem a situação — edita-se uma solicitação já enviada | CT-08 (linhas `Editar`) |
| M7 | a policy confere a situação mas não a identidade — qualquer um edita o rascunho alheio | CT-07 |
| M8 | `===` trocado por `!==` na comparação de situação — o dono deixa de mexer no próprio rascunho e passa a mexer no que já saiu das mãos dele | CT-05, CT-06, CT-08 |
| M9 | a condição extra entra em `update` e é esquecida em `delete` (copiar-e-colar incompleto) | CT-08 (linhas `Excluir`) |
| M10 | o botão é escondido pela policy mas a **rota** `edit` continua aberta — affordance sem barreira | CT-07 (a metade do 403) e CT-08 |

---

## Regra R3 — Enviar move o rascunho para a mão do gestor, e falha fechado quando não há gestor

> `RQ-04`, `A-10` · perfil **completo** · técnica: **EP** + **idempotência** (taxonomia)

```gherkin
# language: pt
  Regra: Ao ser enviada, a solicitação passa a aguardar o gestor do centro de custo; sem gestor
         no centro, o envio é recusado e a solicitação permanece em rascunho

    Cenário: [CT-09] o envio coloca a solicitação na mão do gestor do centro de custo
      Dado um rascunho de R$ 3.200,00 no centro "TI", cujo gestor é a Marina
      Quando o solicitante envia a solicitação
      Então a situação passa a ser "aguardando_gestor"
      E a Marina é a aprovadora da vez

    Cenário: [CT-10] centro de custo sem gestor não recebe solicitação nenhuma
      Dado um rascunho no centro "Novo", que está sem gestor definido
      Quando o solicitante tenta enviar a solicitação
      Então o envio é recusado com a mensagem de que o centro de custo está sem gestor
      E a situação continua "rascunho"
      E nenhuma notificação é enviada a ninguém
      E o canal de log "compras" registra um aviso com o motivo "centro_sem_gestor"

    Cenário: [CT-11] quem não é o solicitante não envia a solicitação dele
      Dado um rascunho criado pelo solicitante
      Quando o gestor do centro de custo chama o envio diretamente, sem passar por tela nenhuma
      Então o envio é recusado
      E a situação continua "rascunho"

    Cenário: [CT-12] enviar duas vezes não reenvia
      Dado uma solicitação já enviada, aguardando o gestor
      Quando o solicitante dispara o envio uma segunda vez
      Então o segundo envio é recusado
      E a situação continua "aguardando_gestor"
      E o gestor recebeu exatamente uma notificação
```

> **Por que CT-11 chama o método direto, sem tela**: é a exigência de `.ai/rules/filament.md` —
> *"asserção de identidade vive no model, não na query da tela"*. Um cenário que passa pela tela
> continuaria verde com a barreira removida, porque a ação já está escondida. **Sem este cenário a
> barreira não é barreira**, e o primeiro job, comando ou rota de API a chamar `enviar()` passa por
> cima dela sem nada acusar.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11 | `enviar()` sem conferir a situação de partida — reenvia o que já foi enviado | CT-12, CT-24 |
| M12 | `enviar()` sem conferir a identidade — o gestor envia o rascunho alheio | CT-11 |
| M13 | a etapa do gestor é **pulada** — o envio vai direto para o diretor (quando o valor exige) ou direto para aprovada | CT-09, CT-10 |
| M14 | centro sem gestor: a solicitação transiciona e o e-mail não sai — ela fica presa em `aguardando_gestor` sem aprovador | CT-10 (situação continua `rascunho`) |
| M15 | a verificação do gestor roda **depois** do UPDATE — a exceção deixa a situação já alterada | CT-10 (a assertion de situação **após** a recusa) |

---

## Regra R4 — A alçada: acima do limite, e só acima, entra o diretor — depois do gestor

> `RQ-05`, `A-04` · perfil **completo** · técnica: **BVA 3-valores**
> (fronteira: `valor`, tipo `decimal(12,2)`, **incremento R$ 0,01**)

```gherkin
# language: pt
  Regra: Uma solicitação de valor estritamente acima do limite exige, além da aprovação do
         gestor, a aprovação de um diretor — nessa ordem

    Esquema do Cenário: [CT-13] o limite do diretor é exclusivo do próprio valor
      Dado uma solicitação de <valor> aguardando o gestor, com o limite do diretor em R$ 5.000,00
      Quando o gestor aprova a solicitação
      Então a situação passa a ser "<situacao>"

      Exemplos:
        | valor        | situacao           | # borda (incremento R$ 0,01)                  |
        | 0,01         | aprovada           | menor valor válido                            |
        | 4.999,99     | aprovada           | borda−1                                       |
        | 5.000,00     | aprovada           | borda — "acima de" é estritamente maior       |
        | 5.000,01     | aguardando_diretor | borda+1                                       |
        | 10.000,00    | aguardando_diretor | ordem lexicográfica ≠ ordem numérica          |
        | 50.000,00    | aguardando_diretor | partição válida, bem acima                    |

    Cenário: [CT-14] acima do limite são duas aprovações, na ordem gestor e depois diretor
      Dado uma solicitação de R$ 8.000,00 aguardando o gestor
      Quando o gestor aprova e, em seguida, o diretor aprova
      Então a situação final é "aprovada"
      E o histórico tem duas etapas, a de gestor antes da de diretor, ambas com decisão "aprovada"

    Cenário: [CT-15] o limite é política, não literal
      Dado que o limite do diretor está configurado em R$ 100,00
      E uma solicitação de R$ 150,00 aguardando o gestor
      Quando o gestor aprova a solicitação
      Então a situação passa a ser "aguardando_diretor"
```

> **A linha `10.000,00` de CT-13 não é redundante com `50.000,00`.** Ela existe por causa de uma
> propriedade da plataforma: no SQLite — o banco dos testes — uma coluna `decimal` volta como
> **string**, e `'10000.00' > '5000.00'` é **falso** em comparação lexicográfica. Uma implementação
> que compare sem converter passa em todas as outras linhas e falha exatamente nesta. É o tipo de
> defeito que só aparece em produção com um pedido caro.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M16 | `>=` no lugar de `>` — R$ 5.000,00 exatos passam pelo diretor | CT-13 (linha `5.000,00`) |
| M17 | comparação invertida (`<`) — a alçada roda ao contrário e só os pedidos baratos vão ao diretor | CT-13 (linhas `4.999,99` e `5.000,01`) |
| M18 | comparação sem conversão numérica, sobre o `decimal` que o driver devolve como string | CT-13 (linha `10.000,00`) |
| M19 | limite `5000.00` cravado no código, com a chave de config ignorada | CT-15 |
| M20 | a etapa do diretor é criada **antes** da do gestor, ou a ordem do histórico não é garantida | CT-14 |
| M21 | `valor` tratado como `float` — R$ 5.000,00 vira `5000.0000000001` e exige diretor sem motivo | CT-13 (linha `5.000,00`) |

---

## Regra R5 — Decide quem é o aprovador da vez, e mais ninguém

> `RQ-06`, `A-03`, `A-07`, `A-09` · perfil **completo** · técnica: **matriz papel × ação**

```gherkin
# language: pt
  Regra: Na etapa do gestor decide o gestor daquele centro de custo; na etapa do diretor decide
         quem tem o papel de diretor

    Esquema do Cenário: [CT-16] só o aprovador da etapa corrente decide
      Dado uma solicitação de R$ 8.000,00 na situação "<situacao>"
      Quando <quem> chama a aprovação diretamente, sem passar por tela nenhuma
      Então o resultado é "<resultado>"

      Exemplos:
        | situacao           | quem                              | resultado | # célula da matriz            |
        | aguardando_gestor  | o gestor do centro de custo       | aceito    | a vez dele                    |
        | aguardando_gestor  | o gestor de outro centro de custo | recusado  | gestor não é papel global     |
        | aguardando_gestor  | o diretor                         | recusado  | ordem invertida               |
        | aguardando_gestor  | o próprio solicitante             | recusado  | ninguém aprova o que pediu    |
        | aguardando_gestor  | um usuário comum do painel        | recusado  | permissão não é autoridade    |
        | aguardando_diretor | o diretor                         | aceito    | a vez dele                    |
        | aguardando_diretor | o gestor do centro de custo       | recusado  | já decidiu                    |
        | aguardando_diretor | um usuário comum do painel        | recusado  | permissão não é autoridade    |

    @premissa (A-09)
    Cenário: [CT-17] quem é gestor do próprio centro de custo aprova a própria solicitação
      Dado uma solicitação de R$ 1.000,00 aguardando o gestor
      E o solicitante é ele mesmo o gestor daquele centro de custo
      Quando o solicitante aprova a solicitação
      Então a situação passa a ser "aprovada"
      E o histórico registra uma etapa de gestor decidida por ele

    Cenário: [CT-18] quem não decide a vez não vê o botão de decidir
      Dado uma solicitação de R$ 8.000,00 aguardando o gestor
      Quando o diretor abre a listagem de solicitações
      Então as ações "Aprovar" e "Rejeitar" não lhe são oferecidas naquela solicitação
      E as mesmas ações são oferecidas ao gestor do centro de custo
```

> **CT-17 é o cenário mais fácil de escrever errado do conjunto.** Ele documenta uma premissa que
> pode ser rejeitada em auditoria (segregação de funções, A-09). Está marcado `@premissa` justamente
> para que a resposta "não, o solicitante nunca aprova" tenha um endereço: este cenário inverte, e
> nasce uma linha nova na matriz de CT-16.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M22 | a barreira confere só a permissão do painel (`can('Update:SolicitacaoCompra')`), e não a identidade | CT-16 (linhas `usuário comum`, `solicitante`) |
| M23 | a etapa corrente não entra na conta — o diretor decide enquanto a vez é do gestor | CT-16 (linha `diretor` em `aguardando_gestor`) |
| M24 | "gestor" tratado como papel global em vez de `gestor_id` daquele centro | CT-16 (linha `gestor de outro centro`) |
| M25 | a barreira vive só no `->visible()` da ação e na policy — o método chamado por job ou comando passa | CT-16 (que chama o método direto, sem tela) |
| M26 | o `->visible()` da ação não confere o aprovador — botão que resulta em 403 | CT-18 |
| M69 | uma segregação de funções que ninguém pediu é inventada — quem é gestor do próprio centro fica sem poder aprovar, e a solicitação trava sem aprovador possível | CT-17 |

---

## Regra R6 — Rejeitar exige justificativa, devolve a rascunho e preserva o histórico

> `RQ-06`, `RQ-07`, `RQ-08`, `RQ-09` · perfil **completo** (elevado: RQ-07 é a única restrição dura
> do card) · técnica: **EP com ausente ≠ nulo ≠ vazio** + **rastreio de efeito**

```gherkin
# language: pt
  Regra: A rejeição só acontece com justificativa preenchida, devolve a solicitação ao rascunho e
         registra no histórico quem rejeitou e por quê

    Cenário: [CT-19] a rejeição devolve a solicitação ao rascunho com o motivo registrado
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor rejeita com a justificativa "Falta cotação de dois fornecedores"
      Então a situação volta a ser "rascunho"
      E o histórico registra uma etapa de gestor com decisão "rejeitada", o nome do gestor e a justificativa "Falta cotação de dois fornecedores"

    Esquema do Cenário: [CT-20] justificativa em branco não rejeita nada
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor chama a rejeição diretamente com a justificativa <justificativa>
      Então a rejeição é recusada
      E a situação continua "aguardando_gestor"
      E nenhuma etapa é registrada no histórico

      Exemplos:
        | justificativa    | # partição inválida, isolada |
        | ausente          | argumento não informado      |
        | nula             | null                         |
        | vazia            | string ""                    |
        | só espaços       | "   " — três espaços         |

    Cenário: [CT-21] a tela também exige o motivo antes de rejeitar
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor confirma a rejeição pela tela sem escrever o motivo
      Então o campo "Motivo da rejeição" acusa erro de obrigatoriedade
      E a situação continua "aguardando_gestor"

    @premissa (P-04, P-05)
    Cenário: [CT-22] o reenvio de uma solicitação rejeitada não apaga o ciclo anterior
      Dado uma solicitação de R$ 8.000,00 rejeitada pelo gestor com o motivo "Falta cotação"
      Quando o solicitante corrige o valor para R$ 4.000,00 e envia de novo, e o gestor aprova
      Então a situação final é "aprovada"
      E o histórico tem duas etapas: a rejeição anterior, com o motivo "Falta cotação", e a aprovação nova

    @premissa (P-03)
    Cenário: [CT-23] a rejeição do diretor também devolve a solicitação ao rascunho
      Dado uma solicitação de R$ 8.000,00 aguardando o diretor, já aprovada pelo gestor
      Quando o diretor rejeita com a justificativa "Fora do orçamento do trimestre"
      Então a situação volta a ser "rascunho"
      E o histórico tem duas etapas: a aprovação do gestor e a rejeição do diretor
```

> **CT-22 prova RQ-09 e a decisão de que o histórico é append-only ao mesmo tempo**, e prova também
> a premissa P-05: o valor corrigido para R$ 4.000,00 dispensa o diretor no ciclo novo, ainda que o
> ciclo anterior o exigisse. Se a alçada fosse congelada no primeiro envio, este cenário terminaria
> em `aguardando_diretor` e falharia.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M27 | `is_null()` no lugar de uma checagem de "em branco" — `""` e `"   "` passam como justificativa | CT-20 (linhas `vazia`, `só espaços`) |
| M28 | a exigência vive só no `->required()` do campo — o método chamado direto aceita vazio | CT-20 (que chama o método sem tela) |
| M29 | a rejeição transiciona para `cancelada`, ou não transiciona, em vez de voltar a `rascunho` | CT-19 |
| M30 | a gravação da etapa é removida — a rejeição acontece e o motivo se perde | CT-19, CT-22 |
| M31 | o reenvio "limpa" o histórico do ciclo anterior | CT-22 |
| M32 | a rejeição do diretor devolve à etapa do gestor em vez de a rascunho | CT-23 |
| M33 | `->required()` ausente no campo da modal — a tela deixa confirmar sem motivo e o erro só aparece como exceção | CT-21 |

---

## Regra R7 — Toda célula vazia da tabela de estados é uma recusa que não move a situação

> `RQ-10`, `RQ-11`, `A-05`, `A-06` · perfil **completo** · técnica: **tabela estado × evento**,
> 30 células, **100% das inválidas cobertas**

### A tabela

Cinco situações × seis eventos. **Tabela, e não diagrama**: o diagrama mostra só as 9 transições
válidas, e por isso só produz teste positivo. São as **21 células vazias** que expõem dupla
aprovação, transição ilegal aceita e ordem invertida.

| Situação \ Evento | editar | excluir | enviar | aprovar | rejeitar | cancelar |
|---|---|---|---|---|---|---|
| **rascunho** | ✅ segue `rascunho` — CT-05 | ✅ registro removido — CT-06 | ✅ → `aguardando_gestor` — CT-09 | ❌ CT-24 | ❌ CT-24 | ❌ CT-24 `@premissa` A-06 |
| **aguardando_gestor** | ❌ CT-08 | ❌ CT-08 | ❌ CT-24 (via CT-12) | ✅ → `aguardando_diretor` ou `aprovada` — CT-13 | ✅ → `rascunho` — CT-19 | ✅ → `cancelada` — CT-26 |
| **aguardando_diretor** | ❌ CT-08 | ❌ CT-08 | ❌ CT-24 | ✅ → `aprovada` — CT-14 | ✅ → `rascunho` — CT-23 `@premissa` P-03 | ✅ → `cancelada` — CT-27 |
| **aprovada** | ❌ CT-08 | ❌ CT-08 | ❌ CT-24 | ❌ CT-24, CT-25 | ❌ CT-24 | ❌ CT-24 |
| **cancelada** `@premissa` P-06 | ❌ CT-08 | ❌ CT-08 | ❌ CT-24 | ❌ CT-24 | ❌ CT-24 | ❌ CT-24 |

- Células válidas: **9**. Células inválidas: **21**.
- Das 21, **8** (editar/excluir fora do rascunho) são cobertas por CT-08, porque ali a recusa é de
  policy e de rota, não de método de transição.
- As **13** restantes são as linhas de CT-24.

```gherkin
# language: pt
  Regra: Uma transição que não existe no fluxo é recusada, e a solicitação continua exatamente
         na situação em que estava

    Esquema do Cenário: [CT-24] transição inexistente é recusada sem efeito
      Dado uma solicitação na situação "<situacao>"
      Quando a pessoa autorizada para aquele evento chama "<evento>"
      Então a chamada é recusada
      E a situação continua "<situacao>"
      E nenhuma etapa nova é registrada no histórico

      Exemplos:
        | situacao           | evento   | # célula vazia                        |
        | rascunho           | aprovar  | não há o que aprovar                  |
        | rascunho           | rejeitar | não há o que rejeitar                 |
        | rascunho           | cancelar | o verbo do rascunho é excluir (A-06)  |
        | aguardando_gestor  | enviar   | já enviada                            |
        | aguardando_diretor | enviar   | já enviada                            |
        | aprovada           | enviar   | terminal (A-05)                       |
        | aprovada           | aprovar  | dupla aprovação                       |
        | aprovada           | rejeitar | terminal                              |
        | aprovada           | cancelar | RQ-11: só antes da aprovação final    |
        | cancelada          | enviar   | terminal (P-06)                       |
        | cancelada          | aprovar  | terminal (P-06)                       |
        | cancelada          | rejeitar | terminal (P-06)                       |
        | cancelada          | cancelar | terminal (P-06)                       |

    Cenário: [CT-25] a solicitação aprovada não muda mais
      Dado uma solicitação de R$ 8.000,00 já aprovada pelo gestor e pelo diretor
      Quando o diretor tenta aprovar de novo
      Então a tentativa é recusada
      E a situação continua "aprovada"
      E o histórico continua com exatamente duas etapas
      E o momento da última alteração da solicitação não muda
```

> **A última linha de CT-25 é o oráculo que a linha correspondente de CT-24 não tem.** "A situação
> continua a mesma" passa também quando o UPDATE roda e grava o mesmo valor; `updated_at` intacto é
> o que prova que **nada** foi escrito.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M34 | a transição não filtra pela situação de partida — qualquer estado transiciona para qualquer outro | CT-24 (a maioria das linhas), CT-29 |
| M35 | a situação terminal não é conferida no cancelamento — cancela-se o que já foi aprovado | CT-24 (linha `aprovada × cancelar`) |
| M36 | "em trânsito" definido incluindo o rascunho — cancelar em rascunho passa | CT-24 (linha `rascunho × cancelar`) |
| M37 | a exceção é lançada **depois** da escrita — a recusa deixa a situação alterada | CT-24 (a assertion "situação continua"), CT-25 |
| M38 | a etapa é gravada antes de a transição vencer — uma aprovação registrada e não aplicada | CT-25 (contagem de etapas) |

---

## Regra R8 — Cancelar é do solicitante, e só enquanto a solicitação está em trânsito

> `RQ-11`, `A-06` · perfil **completo** · técnica: **matriz papel × ação** + recorte da tabela de R7

```gherkin
# language: pt
  Regra: O solicitante cancela a própria solicitação enquanto ela aguarda uma decisão, e o
         cancelamento não é uma decisão de aprovador

    Cenário: [CT-26] o solicitante cancela enquanto aguarda o gestor
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o solicitante cancela a solicitação
      Então a situação passa a ser "cancelada"
      E o histórico continua sem nenhuma etapa

    Cenário: [CT-27] o solicitante cancela até a véspera da aprovação final
      Dado uma solicitação de R$ 8.000,00 aguardando o diretor, já aprovada pelo gestor
      Quando o solicitante cancela a solicitação
      Então a situação passa a ser "cancelada"
      E o histórico continua com a única etapa de aprovação do gestor

    Cenário: [CT-28] o aprovador não cancela a solicitação de outra pessoa
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor do centro de custo chama o cancelamento diretamente
      Então o cancelamento é recusado
      E a situação continua "aguardando_gestor"
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M39 | o cancelamento não confere a identidade — o aprovador cancela em vez de rejeitar, e sem justificativa | CT-28 |
| M40 | o cancelamento só é permitido em `aguardando_gestor`, esquecendo `aguardando_diretor` | CT-27 |
| M41 | o cancelamento grava uma etapa de decisão (cópia do método de aprovação) | CT-26 (histórico sem etapa) |
| M42 | o cancelamento transiciona para `rascunho` em vez de `cancelada` | CT-26 |

---

## Regra R9 — A decisão é atômica: duas decisões simultâneas viram uma

> `RQ-06` + taxonomia (**concorrência**) · perfil **completo** · técnica: teste de concorrência

```gherkin
# language: pt
  Regra: Duas decisões disparadas ao mesmo tempo sobre a mesma etapa produzem uma única
         transição e uma única etapa no histórico

    Cenário: [CT-29] dois diretores decidindo ao mesmo tempo registram uma decisão só
      Dado uma solicitação de R$ 8.000,00 aguardando o diretor
      E dois diretores com a mesma solicitação carregada na tela
      Quando os dois aprovam sem que nenhum tenha recarregado a página
      Então a situação final é "aprovada"
      E o histórico tem exatamente uma etapa de diretor
      E o segundo diretor recebe o aviso de que a solicitação já mudou de situação

    Cenário: [CT-30] o duplo clique em Aprovar não gera duas etapas
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor dispara a ação "Aprovar" duas vezes seguidas pela tela
      Então a situação final é "aprovada"
      E o histórico tem exatamente uma etapa de gestor
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M43 | leitura seguida de gravação (`get()` + `save()`) em vez de escrita condicionada à situação — as duas decisões passam | CT-29, CT-30 |
| M44 | a escrita é condicionada mas o número de linhas afetadas não é conferido — a segunda decisão segue como se tivesse vencido | CT-29 |
| M45 | a etapa é gravada **antes** de a transição vencer — a corrida perdida deixa uma etapa órfã | CT-29 (contagem de etapas) |
| M46 | a gravação da etapa e a transição não estão no mesmo bloco atômico — a etapa sobrevive à falha da transição | ⚠️ **sem matador** — ver lacuna abaixo |

> **Lacuna declarada (M46)**: com `RefreshDatabase`, **todo o teste já roda dentro de uma transação**,
> e em SQLite as transações aninhadas viram savepoints. Um bloco atômico ausente no código de
> produção fica mascarado pelo arnês: o cenário passaria com e sem ele. Não há cenário barato que
> falsifique isto.
> **Mitigação, em duas frentes**: (1) `pest --mutate --class="App\Models\SolicitacaoCompra"` mede o
> que o cenário não vê, e este mutante deve aparecer como sobrevivente esperado, com este parágrafo
> como justificativa registrada; (2) item explícito de revisão de código no PR — *"a gravação da
> etapa e a transição estão no mesmo bloco atômico?"*. É lacuna conhecida, não esquecimento.

---

## Regra R10 — O e-mail vai ao próximo aprovador, uma vez, e a mais ninguém

> `RQ-14`, `A-11` · perfil **padrão** · técnica: **rastreio de efeito colateral** — os três cenários
> canônicos: aconteceu / **não** aconteceu quando não devia / aconteceu **uma só vez**

```gherkin
# language: pt
  Regra: A cada etapa que se abre, e só então, o aprovador daquela etapa é notificado por e-mail

    Cenário: [CT-31] o envio notifica o gestor, e só ele
      Dado um rascunho de R$ 3.200,00 no centro "TI", cujo gestor é a Marina
      E um diretor cadastrado na mesma organização
      Quando o solicitante envia a solicitação
      Então a Marina recebe exatamente uma notificação de aprovação pendente, com a etapa de gestor
      E o diretor não recebe notificação nenhuma
      E o solicitante não recebe notificação nenhuma

    @premissa (P-07)
    Esquema do Cenário: [CT-32] só há e-mail quando há próxima etapa
      Dado uma solicitação de <valor> aguardando o gestor
      Quando o gestor aprova a solicitação
      Então o diretor recebe <notificacoes> notificação de aprovação pendente

      Exemplos:
        | valor    | notificacoes | # a etapa que se abre                      |
        | 5.000,01 | 1            | abre a etapa do diretor                    |
        | 4.999,99 | 0            | aprovação final: não há próximo aprovador  |

    Cenário: [CT-33] rejeição e cancelamento não notificam ninguém
      Dado uma solicitação de R$ 3.200,00 aguardando o gestor
      Quando o gestor a rejeita com justificativa, ou o solicitante a cancela
      Então nenhuma notificação é enviada a ninguém
```

> **Uso de `Notification::fake()` e não de `Mail::fake()`**: a notificação é `ShouldQueue`, e
> `Mail::assertSent` **nunca** passa com mailable enfileirado — a assertion correta seria
> `assertQueued`. Com o fake de notificação o cenário afirma sobre o destinatário e a etapa, que é o
> que RQ-14 diz, em vez de afirmar sobre o mecanismo de entrega.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M47 | a chamada de notificação some do envio (remoção de chamada — o operador mais comum) | CT-31 |
| M48 | notifica-se **todo mundo** que pode aprovar em algum momento, já no envio | CT-31 (o diretor não recebe) |
| M49 | notifica-se também na aprovação final, quando não há próximo aprovador | CT-32 (linha `4.999,99`) |
| M50 | notifica-se também na rejeição e no cancelamento — efeito que ninguém pediu (A-11) | CT-33 |
| M51 | os destinatários são resolvidos **dentro** da notificação enfileirada, e não no request | ⚠️ **sem matador** — ver lacuna abaixo |

> **Lacuna declarada (M51)**: o `phpunit.xml` fixa `QUEUE_CONNECTION=sync`, então a notificação roda
> no **mesmo processo**, com o contexto de permissão ainda fixado pelo middleware. Um código que
> resolva os diretores dentro do job passa em todos os cenários e devolve a lista errada — ou vazia —
> no worker de produção, onde o middleware não roda. **Nenhum cenário barato falsifica isso**: seria
> preciso um worker real, fora do processo do teste. CT-45 cobre a parte observável (a organização
> certa é notificada), não o **momento** da resolução.
> **Mitigação**: item explícito na revisão do PR — *"os destinatários são resolvidos no request e
> passados prontos para a notificação?"*.

---

## Regra R11 — A tela mostra a situação atual e quem decidiu cada etapa

> `RQ-12`, `RQ-13`, `A-12` · perfil **padrão** · técnica: EP sobre estado de exibição

```gherkin
# language: pt
  Regra: A listagem mostra a situação atual de cada solicitação, e a tela de visualização mostra o
         histórico completo de decisões

    Cenário: [CT-34] a listagem mostra a situação em português
      Dado uma solicitação aguardando o gestor e outra já aprovada
      Quando o solicitante abre a listagem de solicitações
      Então ele vê as duas solicitações
      E a coluna de situação mostra "Aguardando gestor" e "Aprovada"

    @premissa (P-08)
    Cenário: [CT-35] a tela de visualização mostra o histórico inteiro, na ordem em que aconteceu
      Dado uma solicitação de R$ 8.000,00 rejeitada pelo gestor com "Falta cotação", reenviada, aprovada pelo gestor e aprovada pelo diretor
      Quando o solicitante abre a tela de visualização dessa solicitação
      Então ele vê as três etapas na ordem em que aconteceram
      E vê, em cada uma, quem decidiu, quando e a decisão
      E vê a justificativa "Falta cotação" na etapa de rejeição

    Cenário: [CT-36] o filtro de situação separa as duas esperas
      Dado uma solicitação aguardando o gestor e outra aguardando o diretor
      Quando o solicitante filtra a listagem pela situação "aguardando_gestor"
      Então ele vê apenas a solicitação que aguarda o gestor
```

> **CT-36 não é cerimônia de filtro.** `aguardando_gestor` e `aguardando_diretor` compartilham
> prefixo: um filtro escrito com comparação parcial casa os dois, e a tela passa a mostrar como "sua"
> uma solicitação que já não é. É a única forma de o filtro errar de um jeito que ninguém percebe.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M52 | a situação é exibida crua (`aguardando_gestor`) em vez do rótulo em português | CT-34 |
| M53 | o histórico mostra só a **última** etapa — RQ-13 pede "cada etapa" | CT-35 |
| M54 | a justificativa não é exibida no histórico, e o solicitante não sabe o que corrigir (RQ-09 fica sem meio) | CT-35 |
| M55 | o filtro de situação usa comparação parcial e casa `aguardando_gestor` com `aguardando_diretor` | CT-36 |

---

## Regra R12 — Centro de custo é administração da organização, não CRUD de negócio

> `RQ-04`, `A-08` · perfil **completo** · técnica: **matriz papel × ação**

O centro de custo aponta quem aprova. **Quem edita o centro se nomeia aprovador e aprova as próprias
compras.** É a escalada de privilégio desta feature, e ela não gera erro nenhum quando esquecida:
os seeders rodam, a suíte fica verde e todo usuário comum vira administrador da organização
(`.ai/rules/filament.md`).

```gherkin
# language: pt
  Regra: A permissão de mexer em centro de custo é da administração da organização; a de solicitar
         compra é de todo usuário do painel

    Esquema do Cenário: [CT-37] o usuário comum não alcança o centro de custo, e alcança a própria feature
      Dado os papéis semeados no painel de negócio
      Quando se pergunta se o papel "<papel>" tem a permissão "<permissao>"
      Então a resposta é "<resposta>"

      Exemplos:
        | papel      | permissao                 | resposta | # o que a linha protege        |
        | panel_user | ViewAny:CentroCusto       | não      | escalada de privilégio (A-08)  |
        | panel_user | Create:CentroCusto        | não      | idem                           |
        | panel_user | Update:CentroCusto        | não      | idem — a chave que nomeia gestor |
        | panel_user | Delete:CentroCusto        | não      | idem                           |
        | panel_user | Create:SolicitacaoCompra  | sim      | a feature é do usuário comum   |
        | panel_user | ViewAny:SolicitacaoCompra | sim      | idem                           |
        | diretor    | Update:CentroCusto        | não      | quem aprova não escolhe quem aprova |
        | diretor    | ViewAny:SolicitacaoCompra | sim      | precisa ver o que vai decidir  |

    Cenário: [CT-38] a tela de centros de custo não abre para o usuário comum
      Dado um usuário comum autenticado no painel de negócio
      Quando ele abre a listagem de centros de custo
      Então a tela responde 403

    Cenário: [CT-39] o administrador da organização cadastra o centro com o gestor
      Dado o administrador da organização autenticado no painel de negócio
      E a Marina cadastrada como usuária da organização
      Quando ele grava um centro de custo "TI" com a Marina como gestora
      Então o centro "TI" persistido tem a Marina como gestora

    Cenário: [CT-40] trocar o gestor troca quem aprova a próxima solicitação
      Dado um centro de custo "TI" com a Marina como gestora
      E o administrador da organização autenticado no painel de negócio
      Quando ele grava o Rui como gestor do centro "TI" e o solicitante envia uma solicitação daquele centro
      Então o centro "TI" persistido tem o Rui como gestor
      E o aprovador da vez da solicitação é o Rui

    Cenário: [CT-41] o papel de diretor abre o painel de negócio
      Dado um usuário com o papel de diretor
      Quando ele tenta acessar o painel de negócio
      Então o acesso é concedido
```

> **CT-41 existe por causa de um modo de falha documentado do projeto**: `roles.painel` nulo **não é
> coringa** — um papel novo sem painel declarado autentica e leva 403 nos três painéis. O papel
> `diretor` é o primeiro papel novo desde a fundação, e é exatamente onde isso acontece.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M56 | o Resource de centro de custo não entra na lista de subtração do usuário comum — a falha silenciosa de A-08 | CT-37 (linhas `panel_user × CentroCusto`) |
| M57 | a subtração casa por substring do nome em vez de identidade exata, e deixa passar as chaves de afixo diferente | CT-37 (que assere **cada** chave, não uma amostra) |
| M58 | o Resource de solicitação entra na lista por engano — o usuário comum fica sem a própria feature | CT-37 (linhas `Create:` e `ViewAny:SolicitacaoCompra`) |
| M59 | o papel de diretor é criado sem declarar o painel | CT-41 |
| M60 | o papel de diretor recebe a matriz completa do painel, inclusive administração | CT-37 (linha `diretor × Update:CentroCusto`) |
| M61 | a policy de centro de custo não confere permissão nenhuma — a tela abre para qualquer sessão | CT-38 |
| M62 | o campo de gestor não persiste (relação declarada e não gravada) — o centro nasce sem gestor e todo envio falha fechado | CT-39 |
| M63 | o aprovador é congelado no envio a partir de uma cópia, e trocar o gestor não muda quem decide | CT-40 |

---

## Regra R13 — Solicitação e centro de custo de outra organização não existem para você

> `A-01`, `A-03` + taxonomia (**IDOR**) · perfil **completo** · técnica: matriz papel × ação + IDOR
> · suíte `tests/FeatureTenancy` (`Tests\TenancyTestCase`)

```gherkin
# language: pt
  Regra: Uma solicitação pertence à organização em que foi criada, e nada dela é visível ou
         alcançável de fora dela

    Cenário: [CT-42] a listagem de uma organização não mostra a solicitação da outra
      Dado uma solicitação "Notebooks" na organização Acme e uma solicitação "Cadeiras" na Globex
      Quando um usuário da Acme abre a listagem de solicitações
      Então ele vê "Notebooks"
      E não vê "Cadeiras"

    Cenário: [CT-43] pedir a solicitação da outra organização pelo endereço não funciona
      Dado uma solicitação "Cadeiras" na organização Globex
      E um usuário da Acme autenticado no painel de negócio
      Quando ele abre a tela de visualização daquela solicitação pelo identificador dela
      Então o acesso é negado

    Cenário: [CT-44] o formulário só oferece os centros de custo da própria organização
      Dado o centro "TI" na Acme e o centro "Frota" na Globex
      Quando um usuário da Acme abre o formulário de nova solicitação
      Então o campo de centro de custo oferece "TI"
      E não oferece "Frota"

    Cenário: [CT-45] o diretor notificado é o da organização da solicitação
      Dado um diretor na Acme e outro diretor na Globex
      E uma solicitação de R$ 8.000,00 da Acme aguardando o gestor
      Quando o gestor aprova a solicitação
      Então o diretor da Acme recebe a notificação de aprovação pendente
      E o diretor da Globex não recebe notificação nenhuma
```

> **CT-43 é o cenário de IDOR**, e a razão de ele existir separado de CT-42: a listagem pode filtrar
> corretamente enquanto a resolução do registro pelo endereço não filtra nada. Um recorte escrito só
> onde a tabela lê deixa a rota, a busca e a contagem abertas — três portas com a mesma chave. Dois
> usuários no setup, em organizações diferentes, como a taxonomia exige.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M64 | o model de solicitação não é escopado pela organização — a listagem mistura clientes | CT-42 |
| M65 | o recorte existe onde a tabela lê, mas não na consulta que resolve o registro pelo endereço | CT-43 |
| M66 | o campo de centro de custo consulta o model sem escopo | CT-44 |
| M67 | os diretores são resolvidos sem o contexto da organização — traz os de todas | CT-45 |
| M68 | sem organização corrente o recorte falha **aberto** e devolve a base inteira, em vez de nada | CT-43 |

---

## Checklist de Taxonomia de Defeito

Percorrido item a item. Dispensa sempre com motivo escrito — "não se aplica" em silêncio não conta.

| Item | Aplicável? | Cenário / motivo da dispensa |
|---|---|---|
| **IDOR / autorização horizontal** | sim | CT-07 (mesma organização), **CT-43** (organizações diferentes). Dois usuários no setup nos dois |
| **Idempotência** | sim | CT-12 (enviar duas vezes), CT-30 (duplo clique em Aprovar), CT-25 (aprovar o já aprovado) |
| **Concorrência** | sim | CT-29 — duas decisões simultâneas sobre a mesma etapa |
| **Ausente ≠ `null` ≠ `""`** | sim | CT-20 — as quatro partições da justificativa, uma por linha, nunca combinadas |
| **Paginação** | **não** | dispensa com prazo: a listagem usa a paginação nativa do Filament, não escrita nesta feature, e o `00` não especifica volume. Vira cenário obrigatório no dia em que houver ordenação ou agrupamento próprios |
| **Ordenação por coluna** | parcial | CT-35 cobre a ordem do histórico (e P-08 registra o empate de `created_at`). Ordenação da listagem é nativa — mesma dispensa da paginação |
| **Timezone / DST** | **não** | a feature não tem prazo, agendamento, expiração nem comparação de datas. `created_at` é só exibido. SLA está fora de escopo por declaração do `00` |
| **Texto livre: acento, emoji, limite de `varchar`, espaços nas bordas** | parcial | CT-20 cobre "só espaços" na justificativa, que é o caso com consequência de **regra** (rejeição sem motivo). Acento, emoji e limite de coluna são comportamento do banco e não da feature — dispensados, com a ressalva de que a justificativa é texto de pessoa sobre pessoa e nunca deve ir ao log |
| **Unicidade + soft delete** | **não** | nenhum dos três models usa exclusão lógica, e a única restrição de unicidade (nome do centro dentro da organização) não convive com exclusão lógica. Se `SoftDeletes` entrar em `CentroCusto`, esta linha vira cenário |
| **CRUD combinado** (ID inexistente, excluir duas vezes, editar sem alterar) | parcial | CT-06 e CT-08 cobrem excluir; "editar sem alterar nada" é coberto de fato por CT-25 (`updated_at` intacto na recusa). ID inexistente é comportamento nativo do route binding do Filament, dispensado |
| **Mass assignment** | sim | **CT-03** — `situacao` e `solicitante_id` enviados no payload e provados ignorados |
| **Upload** | **não** | anexos estão fora de escopo por declaração do `00` |
| **Precisão monetária** | sim | CT-13 — `decimal`, nunca `float`; o incremento do BVA é R$ 0,01; a linha `10.000,00` cobre a comparação de `decimal` devolvido como string pelo driver; nenhum exemplo deste arquivo usa `float` |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | criação nasce em rascunho no nome de quem criou | R1 | EP | Livewire | `tests/Feature/SolicitacaoCompraTelasTest.php` | M3 |
| CT-02 | os três campos são obrigatórios | R1 | EP | Livewire | idem | M4 |
| CT-03 | situação e solicitante não vêm do formulário | R1 | mass assignment | Livewire | idem | M1, M2 |
| CT-04 | valor de compra é maior que zero | R1 | BVA | Livewire | idem | M5 |
| CT-05 | o dono corrige o próprio rascunho | R2 | matriz papel×ação | Livewire | idem | M8 |
| CT-06 | o dono exclui o próprio rascunho | R2 | matriz papel×ação | Livewire | idem | M8 |
| CT-07 | rascunho alheio não é editável | R2 | IDOR | Livewire + Feature | `tests/Feature/SolicitacaoCompraAutorizacaoTest.php` | M7, M10 |
| CT-08 | editar/excluir só em rascunho (8 células) | R2 | estado × evento | Livewire + Feature | idem | M6, M8, M9, M10 |
| CT-09 | envio vai ao gestor do centro | R3 | EP | Feature | `tests/Feature/SolicitacaoCompraFluxoTest.php` | M13 |
| CT-10 | centro sem gestor falha fechado | R3 | EP | Feature | idem | M13, M14, M15 |
| CT-11 | só o solicitante envia (método direto) | R3 | matriz papel×ação | Feature | idem | M12 |
| CT-12 | enviar duas vezes não reenvia | R3 | idempotência | Feature | idem | M11 |
| CT-13 | fronteira do limite do diretor (6 linhas) | R4 | **BVA 3-valores** | Feature | idem | M16, M17, M18, M21 |
| CT-14 | duas aprovações na ordem certa | R4 | estado × evento | Feature | idem | M20 |
| CT-15 | o limite vem da configuração | R4 | EP | Feature | idem | M19 |
| CT-16 | só o aprovador da vez decide (8 linhas) | R5 | **matriz papel×ação** | Feature | `tests/Feature/SolicitacaoCompraAutorizacaoTest.php` | M22, M23, M24, M25 |
| CT-17 | gestor do próprio centro aprova a própria | R5 | matriz papel×ação | Feature | idem | M69 `@premissa` A-09 |
| CT-18 | sem a vez, sem botão | R5 | matriz papel×ação | Livewire | `tests/Feature/SolicitacaoCompraTelasTest.php` | M26 |
| CT-19 | rejeição devolve a rascunho com motivo | R6 | rastreio de efeito | Feature | `tests/Feature/SolicitacaoCompraFluxoTest.php` | M29, M30 |
| CT-20 | justificativa em branco não rejeita (4 linhas) | R6 | EP ausente≠null≠vazio | Feature | idem | M27, M28 |
| CT-21 | a tela exige o motivo | R6 | EP | Livewire | `tests/Feature/SolicitacaoCompraTelasTest.php` | M33 |
| CT-22 | reenvio preserva o ciclo anterior | R6 | rastreio de efeito | Feature | `tests/Feature/SolicitacaoCompraFluxoTest.php` | M31 |
| CT-23 | rejeição do diretor devolve a rascunho | R6 | estado × evento | Feature | idem | M32 |
| CT-24 | transição inexistente é recusada (13 células) | R7 | **estado × evento** | Feature | idem | M34, M35, M36, M37 |
| CT-25 | a aprovada não muda mais | R7 | estado × evento | Feature | idem | M37, M38 |
| CT-26 | cancelar aguardando o gestor | R8 | matriz papel×ação | Feature | idem | M41, M42 |
| CT-27 | cancelar aguardando o diretor | R8 | matriz papel×ação | Feature | idem | M40 |
| CT-28 | o aprovador não cancela | R8 | matriz papel×ação | Feature | idem | M39 |
| CT-29 | duas decisões simultâneas = uma | R9 | concorrência | Feature | idem | M43, M44, M45, M34 |
| CT-30 | duplo clique não duplica etapa | R9 | idempotência | Livewire | `tests/Feature/SolicitacaoCompraTelasTest.php` | M43 |
| CT-31 | o envio notifica só o gestor | R10 | rastreio de efeito | Feature | `tests/Feature/SolicitacaoCompraNotificacaoTest.php` | M47, M48 |
| CT-32 | e-mail só quando há próxima etapa | R10 | rastreio de efeito | Feature | idem | M49 |
| CT-33 | rejeição e cancelamento não notificam | R10 | rastreio de efeito | Feature | idem | M50 |
| CT-34 | situação em português na listagem | R11 | EP | Livewire | `tests/Feature/SolicitacaoCompraTelasTest.php` | M52 |
| CT-35 | histórico completo na tela de visualização | R11 | EP | Livewire | idem | M53, M54 |
| CT-36 | filtro separa as duas esperas | R11 | EP | Livewire | idem | M55 |
| CT-37 | matriz de permissões dos papéis (8 linhas) | R12 | matriz papel×ação | Feature | `tests/Feature/SolicitacaoCompraAutorizacaoTest.php` | M56, M57, M58, M60 |
| CT-38 | centro de custo não abre para o comum | R12 | matriz papel×ação | Livewire | idem | M61 |
| CT-39 | administrador cadastra o centro com gestor | R12 | matriz papel×ação | Livewire | idem | M62 |
| CT-40 | trocar o gestor troca quem aprova | R12 | matriz papel×ação | Livewire + Feature | idem | M63 |
| CT-41 | o papel de diretor abre o painel | R12 | matriz papel×ação | Feature | idem | M59 |
| CT-42 | listagem não mistura organizações | R13 | IDOR | Livewire | `tests/FeatureTenancy/SolicitacaoCompraTenancyTest.php` | M64 |
| CT-43 | endereço da outra organização não abre | R13 | **IDOR** | Feature | idem | M65, M68 |
| CT-44 | centros de custo só os da organização | R13 | IDOR | Livewire | idem | M66 |
| CT-45 | diretor notificado é o da organização | R13 | rastreio de efeito | Feature | idem | M67 |

---

## Alocação de Camada e Poda

### Por que nada caiu em `Unit`

Derivando do requisito, **nenhuma cláusula do card afirma sobre um cálculo puro**. Todas afirmam
sobre estado persistido, autoridade de quem age, efeito colateral ou o que aparece na tela. A
tentação era escrever um `Unit` para o predicado da alçada — mas RQ-05 não fala de um predicado,
fala de o que acontece **depois que o gestor aprova**. Testar o predicado seria testar a
implementação imaginada, que é o teste tautológico que a skill proíbe. CT-13 fica em `Feature`.

### O que foi podado

| Cenário cortado | Por quê |
|---|---|
| "a aprovada é terminal para todo evento" (cenário próprio) | mata exatamente o mesmo conjunto de mutantes que as 4 linhas `aprovada` de CT-24. Mantido só na tabela |
| "cancelar em rascunho é recusado" (cenário próprio) | é uma linha de CT-24; um cenário separado não mata nenhum mutante a mais |
| "a visita à tela de criação responde 200" | `assertOk()` sozinho é assertion proibida como oráculo único. O que importa é a **gravação**, e é CT-01 que a prova |
| "a listagem abre sem erro" | idem. CT-34 prova o conteúdo, que é o que RQ-12 pede |

### Gate de tela de escrita — obrigatório

Toda rota `create`/`edit` da tabela `## Superfície de UI` tem cenário de **gravação por componente**
(preencher → gravar → conferir no banco os campos que importam), e não só de visita:

| Rota de escrita | Cenário de gravação |
|---|---|
| `/app/solicitacoes-de-compra/create` | **CT-01** |
| `/app/solicitacoes-de-compra/{record}/edit` | **CT-05** |
| `/app/centros-de-custo/create` | **CT-39** |
| `/app/centros-de-custo/{record}/edit` | **CT-40** |

Nenhuma tela de escrita ficou coberta apenas por visita. Esta é a linha que, medida num kit real,
deixou 5 telas `create` sem gravação testada em lugar nenhum.

### Teto por perfil

| Regra | Perfil | Teto | Cenários | Situação |
|---|---|---|---|---|
| R1 | padrão | 3 | **4** | **estouro justificado**: R1 carrega dois eixos independentes — obrigatoriedade dos três campos e o domínio do valor. Separá-la em duas regras deixaria uma delas com uma cláusula só; o estouro é a opção mais honesta |
| R2, R3 | completo | 5 | 4 | dentro |
| R4, R5, R8, R10, R11 | completo/padrão | 5/3 | 3 | dentro |
| R6, R12 | completo | 5 | 5 | no teto |
| R7, R9 | completo | 5 | 2 | dentro — as duas usam esquema com muitas linhas em vez de muitos cenários |
| R13 | completo | 5 | 4 | dentro |

---

## Fechamento do Ciclo com Mutation Testing

Este arquivo **prevê** 69 mutantes. Depois de implementar, o Pest **mede**:

```bash
vendor/bin/pest --mutate --covered-only --class="App\\Models\\SolicitacaoCompra"
vendor/bin/pest --mutate --covered-only --class="App\\Policies\\SolicitacaoCompraPolicy"
```

- Exige `covers(SolicitacaoCompra::class)` no arquivo de teste e driver de cobertura (PCOV ou
  Xdebug). `.ai/rules/testes-browser.md` registra que, sem PCOV, o `--tia` é inviável neste
  ambiente — o mesmo vale aqui.
- **Escopar por `--class`**: mutar o projeto inteiro devolve ruído dos plugins de vendor.
- **Sobreviventes esperados**: M46. Qualquer outro sobrevivente é lacuna de derivação e volta para
  cá como cenário novo, pela tabela de tradução da skill (`>` → `>=` = falta BVA; `&&` → `||` = falta
  linha da tabela de decisão; chamada removida = falta rastreio de efeito).
- **A meta não é cobertura de linha.** 100% de linha é compatível com zero assertion útil.

---

## Revisão Adversarial

Executada por sub-agente independente, que recebeu **apenas** `00-requisito.md` e este arquivo — sem
o plano, sem código e sem o raciocínio desta derivação. O resultado está em
`## Achados da Revisão Adversarial`, ao fim do arquivo.

---

## Com CT-B

O gate do `05` **passa**: a tabela `## Superfície de UI` do plano tem 6 linhas, todas dependentes de
JavaScript, **e** dois cenários afirmam sobre algo que só o navegador prova — que a modal de
rejeição **abre** e que o erro de validação dela **aparece**. Um teste de componente chama a ação
com os dados prontos e nunca atravessa a modal: uma modal que não abre deixa a suíte inteira verde
com a rejeição inutilizável. Ver `05-casos-de-teste-browser.md`.

Tudo o mais da superfície — visibilidade de ação, validação de formulário, filtro, gravação,
histórico — é provado por componente Livewire e **fica neste arquivo**, que é a camada barata.
