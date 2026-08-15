# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> a feature ainda não existe no projeto. O `01-plano-acao.md` foi lido apenas para paths, rotas
> e a tabela `## Superfície de UI`; o que dele foi recusado como oráculo está em
> [Fronteira com o Plano](#fronteira-com-o-plano).

## Perfil de Derivação

| Área | O que abrange | P | I | P×I | Perfil |
|---|---|---|---|---|---|
| **A1 — Motor de aplicação** | validar código, validade e limite; calcular o desconto; consumir o uso | 3 (concorrência sobre contador + regra com muitas condições) | 3 (dinheiro; uso consumido é irreversível) | **9** | **completo** |
| **A2 — Cadastro do cupom** | domínio dos cinco atributos na criação e na edição; unicidade do código | 3 (domínio condicionado `tipo`×`valor`; três pontos de decisão) | 3 (valor mal gravado vira desconto errado — dinheiro) | **9** | **completo** |
| **A3 — Autorização e visibilidade** | quem cria/edita/exclui; o que o usuário comum enxerga | 2 (integra com Shield/policy já existentes) | 3 (autorização) | **6** | **padrão** |
| **A4 — Trilha de auditoria** | registrar quem aplicou e quando | 2 (integra com o consumo) | 3 (dado de auditoria; perda é irreversível) | **6** | **padrão** |
| **A5 — Superfície de cadastro** | a tela do painel abre, grava e lista | 2 (Filament/Livewire existente) | 2 (retrabalho manual) | **4** | **padrão** |

- **Técnicas aplicadas**: EP (partição de equivalência), BVA 3-valores, tabela de decisão,
  tabela estado × operação, matriz papel × ação, rastreio de efeito, normalização de identidade.
- **Cenários**: 49 (`CT-01`…`CT-49`) · **CT-B**: 2 · **Regras**: 11 ·
  **Mutantes previstos**: 89 (80 no `04`, 9 no `05`) · **Sem matador**: 2 (declarados: idempotência
  ancorada e divergência de fuso app × operador).
- **Revisão adversarial**: **2 rodadas executadas**, por sub-agente independente. **25 lacunas
  reais**, todas fechadas — 12 cenários novos (`CT-38`…`CT-49`), 11 oráculos reescritos, 2 perguntas
  novas. A 2ª rodada ainda trouxe achado estrutural: o teto de rodadas da skill foi atingido e a
  escalação está registrada em [Revisão Adversarial](#revisão-adversarial). **26 dos 89 mutantes
  vieram da revisão** — ou seja, quase um terço do gate não existia na primeira derivação.

### Divergência declarada: rule do projeto vence a skill

`.ai/rules/testes-browser.md` mede que **`--parallel` derruba os CT-B** e que, **sem PCOV, o `--tia`
não termina** (abortado após 35 min). A skill sugere `pest --parallel --tia` como comando padrão;
aqui **a rule vence**, e os comandos desta feature são dois:

```bash
vendor/bin/pest --parallel --group=kit      # CT-01…CT-37
vendor/bin/pest --testsuite=Browser         # CT-B01, CT-B02 — em série
```

### Fato do arnês que muda a alocação de camada

`tests/Pest.php` **não liga o `TestCase` da aplicação a `tests/Unit`** — só `Feature`, `Kit`,
`Tenancy`, `Browser` e `BrowserTenancy` recebem `pest()->extend(TestCase::class)`. Um caso escrito
em `tests/Unit` roda **sem container, sem banco e sem casts do Eloquent**. Logo, **a camada mais
barata que existe neste projeto é `Feature`**, e nenhum cenário foi alocado a `Unit`, inclusive os
de cálculo puro. Isto é fato do arnês, não preferência.

### Fato do ferramental que o pós-implementação precisa

`pestphp/pest-plugin-mutate` está em `vendor/pestphp/`, mas **não é declarado em `composer.json`** —
está lá como dependência transitiva do Pest 5 e some num `composer update`. Antes de rodar o
fechamento com `--mutate`, `composer require pestphp/pest-plugin-mutate --dev`.

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | entidade `Cupom` (código, tipo, valor, validade, limite, contador de usos); registro de uso (quem/quando); tela de cadastro no painel; regra de autorização por papel | CT-01, CT-36, CT-37 |
| **F**unction | cadastrar / editar / excluir / listar cupom; validar código na aplicação; calcular o desconto; consumir um uso; registrar o uso | CT-01…CT-37 |
| **D**ata | `codigo` (texto livre — caixa, espaços, acento); `tipo` (dois valores, discriminador de unidade); `valor` (**domínio condicionado pelo tipo**); `expira_em` (temporal); `limite_de_usos` e `usos` (contadores); **dado de outra organização** (P-04) | CT-05, CT-10, CT-12, CT-17, CT-24, CT-25 |
| **I**nterfaces | tela do painel (criação, edição, exclusão, listagem); chamada programática da regra de aplicação (P-01 — não há tela de resgate nem endpoint nesta entrega) | CT-14, CT-20, CT-36, CT-B01 |
| **P**latform | SQLite `:memory:` nos testes (`phpunit.xml`) — colação e comparação de string **case-sensitive** por padrão, o que torna a normalização do código observável; app em `UTC` (`config/app.php:68`) enquanto o operador é pt-BR | CT-10, CT-21 (e lacuna de fuso, declarada) |
| **O**perations | quem opera é administrador da organização (P-02); o usuário comum apenas consulta; uso indevido esperado: usuário comum tentando emitir desconto, e resgate concorrente do último uso | CT-14, CT-15, CT-30 |
| **T**ime | validade expira; a fronteira é o instante gravado (`00` → A-09); um cupom pode expirar **entre** duas leituras; o registro do uso precisa do instante ("quando", RQ-15) | CT-07, CT-09, CT-19, CT-21, CT-32 |

Nenhuma dimensão ficou vazia.

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R01** — Um cupom só passa a existir com código, tipo, valor, validade e limite de usos, e o tipo é um dos dois admitidos | A2 (completo) | RQ-02, RQ-03, RQ-04, RQ-05, RQ-06 | EP + partição exaustiva do discriminador | CT-01…CT-04 |
| **R02** — O domínio de `valor` depende do `tipo`: percentual vai de 1 a 100; valor fixo não tem teto superior e é gravado em centavos | A2 (completo) | RQ-03, RQ-04 | tabela de decisão + BVA 3-valores + discriminador na gravação | CT-05, CT-06, CT-43, CT-44 |
| **R03** — Validade e limite de usos só admitem valores que deixam o cupom utilizável, **na criação e na edição** | A2 (completo) | RQ-05, RQ-06 | BVA 3-valores em dois pontos de entrada + granularidade de entrada | CT-07, CT-08, CT-09, CT-49 |
| **R04** — O código identifica o cupom de forma única dentro da organização, sem depender de caixa nem de espaços | A2 (completo) | RQ-02, RQ-14 | normalização de identidade nos dois sentidos + unicidade em dois pontos | CT-10…CT-13, CT-38, CT-39 |
| **R05** — Só o administrador cria, edita e exclui cupom — cada verbo por si | A3 (padrão) | RQ-07 | matriz papel × ação, exaustiva no eixo do papel | CT-14…CT-16, CT-42 |
| **R06** — O usuário não-administrador lista, e a lista contém exatamente os cupons ativos | A3 (padrão) | RQ-08 | tabela estado × operação + partição exaustiva do estado (5 células) | CT-17…CT-19, CT-41, CT-46, CT-48 |
| **R07** — A aplicação recusa código inexistente, vencido ou esgotado, e a recusa não deixa efeito | A1 (completo) | RQ-09, RQ-10, RQ-11 | EP (inválidas isoladas) + BVA 3-valores + fixture colidente | CT-20…CT-24, CT-40, CT-47 |
| **R08** — Passando as validações, o total recebe o desconto do tipo e do valor do cupom, truncado para baixo e limitado em zero | A1 (completo) | RQ-12 | tabela de decisão + BVA + valores discriminantes | CT-25…CT-27 |
| **R09** — Cada aplicação bem-sucedida consome exatamente um uso, e o limite nunca é ultrapassado | A1 (completo) | RQ-11, RQ-13 | rastreio de efeito + concorrência | CT-28…CT-31 |
| **R10** — Toda aplicação bem-sucedida registra quem aplicou, em qual cupom e quando; nenhuma recusa registra, e o registro sobrevive ao cupom | A4 (padrão) | RQ-15 | rastreio de efeito (4 direções) + identidade + durabilidade | CT-32…CT-35, CT-45 |
| **R11** — O cadastro é operável pela tela do painel: ela cria, edita e lista o cupom | A5 (padrão) | RQ-01 | gate de tela de escrita | CT-36, CT-37, CT-B01 |

> **Dívida declarada de modelagem** (ver a escalação da revisão adversarial): **R10 deveria ser
> duas regras** — *"o uso é registrado"* e *"o registro identifica e sobrevive"*. Seis cenários numa
> regra de perfil `padrão` é sintoma, não coincidência. Não foi desdobrada porque renumerar toda a
> rastreabilidade no fechamento da revisão trocaria um problema real por um cosmético.

### Técnicas escaladas acima do perfil da área

- **R10 está em área `padrão` e usa rastreio de efeito com 4 cenários** (o teto do perfil é 3). A
  quarta direção é a **atomicidade** (CT-35): sem ela, "o uso foi consumido mas a trilha sumiu" fica
  indistinguível de "os dois aconteceram". Estouro justificado, conforme o passo 7 da skill.
- **R06 está em área `padrão` e usa BVA na fronteira `usos = limite − 1`** (CT-17), que o perfil
  `padrão` não exigiria. Motivo: sem a linha da borda, um `<=` no lugar de `<` esconde o último uso
  do cupom e ninguém percebe — é a diferença entre "esgotado" e "quase esgotado", que é a única que
  importa aqui.

### Toda `RQ` gerou regra

| RQ | Regra(s) | RQ | Regra(s) |
|---|---|---|---|
| RQ-01 | R11 | RQ-09 | R07 |
| RQ-02 | R01, R04 | RQ-10 | R07 |
| RQ-03 | R01, R02 | RQ-11 | R07, R09 |
| RQ-04 | R02 | RQ-12 | R08 |
| RQ-05 | R01, R03, R07 | RQ-13 | R09 |
| RQ-06 | R01, R03, R07, R09 | RQ-14 | R04 |
| RQ-07 | R05 | RQ-15 | R10 |
| RQ-08 | R06 | | |

Nenhuma `RQ` sem regra.

---

## Fronteira com o Plano

O `00-requisito.md` traz nove premissas assumidas (**P-01 a P-09**) na seção `## Ambiguidades`.
Elas são **do requisito**, não do plano — foram registradas no arquivo que é a linha de base — e
por isso **podem ser oráculo**, com os cenários marcados `@premissa`. O que segue é o que veio
**apenas** do `01-plano-acao.md` e foi recusado.

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| nomes `Cupom::valido()`, `aplicarEm()`, `descontoSobre()`, `scopeAtivos()` | escolha de implementação | detalhe do cenário — o `Quando` fala em "aplicar o cupom", não no método |
| tabelas `cupons` / `cupom_usos`, coluna `usos`, coluna `expira_em` | escolha de implementação | detalhe do cenário — o `Então` afirma *"o contador de usos do cupom"* e *"existe um registro de quem aplicou e quando"* |
| strings `'Ativo'` / `'Expirado'` / `'Esgotado'` de `situacao()` | escolha de implementação, e é **rótulo visível** que o card não determina | detalhe — CT-17 afirma **presença/ausência na lista**, nunca a palavra |
| rótulos `'Percentual de desconto'` / `'Valor do desconto (centavos)'` que trocam com o `Select` | comportamento **visível ao usuário** que só o PRD determina | **pergunta Q-04**; nenhum CT ou CT-B afirma esse texto |
| `->minDate(now())` no campo de validade | comportamento visível que só o PRD determina — o card nunca diz que um cupom não pode nascer vencido | **pergunta Q-01**; CT-07 e CT-09 marcados `@premissa` |
| `->minValue(1)` em `limite_de_usos` | idem — o card não dá piso ao limite | **pergunta Q-02**; CT-08 marcado `@premissa` |
| `->minValue(1)` em `valor` **do tipo fixo** | o `00` (P-05) fixa 1–100 só para o percentual; o piso do fixo é do PRD | **pergunta Q-03**; a linha "fixo, 0" de CT-05 marcada `@premissa` |
| `->maxValue(100)` para percentual | **não recusado** — vem de P-05 no `00` ("de 1 a 100"), que é o requisito | oráculo legítimo, `@premissa P-05` |
| painel `/app`, papel `admin_organizacao`, unicidade por organização, centavos, truncar, limitar em zero | **não recusados** — são P-02, P-04, P-05, P-06, P-07 e P-09 do `00` | oráculos legítimos, cenários `@premissa` |
| `Log::channel('cupom')` e o formato das mensagens | escolha de implementação; o card não pede log | **nenhum CT afirma log** — declarado, não esquecido |

> **Sobre o número literal do requisito**: o único valor numérico que o card escreve é o par
> "porcentagem / valor fixo" (qualitativo). Os números concretos (1, 100, centavos) vêm de P-05 no
> `00`. **CT-05 usa `100` e `1` escritos literalmente**, sem injeção por `config()`, e CT-27 usa
> `100%` literal — é o que impede um teto errado de sobreviver por o teste medir o ambiente.

### Perguntas para o `00-requisito.md`

O `00-requisito.md` desta feature é **somente leitura** (linha de base fechada da execução `exp-a`).
Conforme a skill, as perguntas ficam aqui, **em bloco pronto para colagem** em
`00-requisito.md → ## Ambiguidades`, e a lacuna continua bloqueando o que depende dela.

```markdown
### Q-01 — a gravação recusa um cupom que já nasce vencido?
- **Assumido**: sim — validade no passado é recusada na criação **e** na edição. Um cupom que nasce
  vencido é dado morto, e RQ-10 o recusaria em toda aplicação.
- **Se negado**: CT-07 e CT-09 invertem o `Então` (passa a gravar), e R06 ganha uma linha —
  cupom vencido cadastrado precisa sumir da lista do usuário comum desde o primeiro instante.

### Q-02 — o limite de usos aceita 0?
- **Assumido**: não; o mínimo é 1. Limite 0 é cupom que nunca pode ser resgatado.
- **Se negado**: CT-08 inverte a linha `0`, e R06 ganha um estado novo — "esgotado desde a criação".

### Q-03 — o desconto de valor fixo aceita 0 (R$ 0,00)?
- **Assumido**: não; o mínimo é 1 centavo. P-05 fixa 1..100 para o percentual e cala sobre o fixo.
- **Se negado**: a linha "fixo, 0" de CT-05 passa de recusado a aceito, e R08 ganha a borda
  "desconto zero não altera o total".

### Q-04 — a tela precisa declarar a unidade do campo de valor ao trocar o tipo?
- **Assumido**: nada. Nenhum CT nem CT-B afirma rótulo de campo — o card não descreve a tela.
- **Consequência declarada**: o risco de a tela dizer "R$" enquanto grava porcentagem fica
  **descoberto**. É lacuna de requisito, não de derivação: sem resposta, qualquer oráculo seria
  cópia do PRD.

### Q-05 — reduzir o limite de usos abaixo dos usos já feitos é permitido?
- **Assumido**: sim, é permitido, e o cupom passa a se comportar como esgotado.
- **Se negado**: R03 ganha um cenário de recusa na edição.

### Q-07 — excluir um cupom que já foi usado apaga a trilha dele?
- **Contexto**: RQ-07 dá ao administrador o direito de excluir, e RQ-15 pede o registro *"pra gente
  conseguir auditar **depois**"*. As duas cláusulas colidem e o card não arbitra.
- **Assumido**: a trilha **sobrevive** à exclusão do cupom, e continua identificando o código usado.
  Trilha que some com o agregado não serve ao "depois" que RQ-15 nomeia.
- **Se negado** (a alternativa defensável é recusar a exclusão de cupom com uso): CT-45 inverte o
  `Então` para *"a exclusão é recusada e o cupom continua existindo"*, e R05 ganha uma linha na
  célula `excluir`.

### Q-06 — de quem é a idempotência da aplicação? (bloqueia o item do checklist)
- **Contexto**: P-01 tirou o `Pedido` do escopo. Sem o agregado que sofre o desconto, *"aplicar o
  mesmo cupom duas vezes ao mesmo pedido"* é **inexpressável**: o único estado persistido é o
  contador do cupom, e afirmar sobre ele prova contabilidade, não idempotência.
- **Assumido**: a idempotência é responsabilidade do chamador. **Nenhum cenário de idempotência foi
  escrito** — escrevê-lo produziria um caso tautológico com cara de cobertura.
- **Se negado**: entra uma regra nova ("a segunda aplicação do mesmo cupom ao mesmo pedido não
  altera o total nem consome uso") e o `Pedido` volta ao escopo.
```

---

## Setup Global

### Personas

Três pessoas **distintas** em todo cenário de autorização — persona colapsada não exercita barreira
nenhuma.

| Persona | Como criar | Onde vale |
|---|---|---|
| `administradora` | `usuarioComPapel('admin_organizacao', $acme)` (`tests/Pest.php:255`) | `tests/Tenancy`, `tests/BrowserTenancy` |
| `usuarioComum` | `usuarioComPapel('panel_user', $acme, 'comum@example.com')` | `tests/Tenancy` |
| `administradoraDaOutra` | `usuarioComPapel('admin_organizacao', $globex, 'outra@example.com')` | `tests/Tenancy` — a persona do cenário de isolamento |
| `master` | `usuarioDoKit('master_global')` (`tests/Pest.php:229`) | `tests/Kit` — em single-tenant, `admin_organizacao` **não é criado** pelo `PapeisSeeder` (`:70-73`), e quem escreve é o `master_global` pelo `Gate::before` |
| `comumSingle` | `usuarioDoKit('panel_user', 'comum@example.com')` | `tests/Kit` |

> **Por que as duas suítes**: o papel `admin_organizacao` só existe com a tenancy ligada. Cenário de
> autorização escrito só em `tests/Kit` mediria uma matriz que não é a de produção; escrito só em
> `tests/Tenancy` deixaria o modo default do kit (`config/kit.php:59` → `false`) sem nenhum caso.

### Fixtures

Não existe factory de cupom no projeto (nem `ProjetoFactory` existe — os testes de tenancy criam o
registro à mão, `tests/Tenancy/TenancyTest.php:319`). O `01-plano-acao.md` prevê `CupomFactory` com
os states `expirado()`, `esgotado()` e `fixo()`; **os cenários assumem esses três states**.

| Fixture | Estado que ela produz |
|---|---|
| `Cupom::factory()->create([...])` | percentual, valor 10, validade futura, limite 100, `usos` 0 |
| `->expirado()` | validade no passado |
| `->esgotado()` | `usos === limite_de_usos` |
| `->fixo(int $centavos)` | tipo valor fixo, valor em centavos |

> **Armadilha do state `esgotado()`**: o contador **não é campo de formulário** e fica fora do
> `$fillable`, então `state(['usos' => …])` é **descartado em silêncio**. O state precisa de
> `afterCreating` com escrita forçada. Se ele nascer errado, CT-17, CT-22 e CT-30 passam medindo um
> cupom que nunca esteve esgotado — falso ✅ na regra mais cara da feature.

### Fakes

Nenhum. A feature não envia e-mail, não despacha job e não chama HTTP externo. `Queue::fake()`,
`Mail::fake()` e `Http::fake()` seriam ruído — e `Http::fake()` sem stub devolve 200 vazio e faz o
teste passar sem provar nada.

### Tempo

`freezeTime()` nos cenários que afirmam sobre o instante (CT-21, CT-32) e `travelTo()` nos que
afirmam sobre a passagem do tempo (CT-19). **Sempre em closure ou com `travelBack()`** — `travel()`
solto vaza para os testes seguintes e produz flake em `--parallel`.

### Estratégia de DB

`RefreshDatabase` global, aplicado por `tests/Pest.php` a `Feature`, `Kit`, `Tenancy`, `Browser` e
`BrowserTenancy`. SQLite `:memory:` (`phpunit.xml:53-54`), inclusive dentro do navegador — o
`pest-plugin-browser` sobe servidor **in-process**.

### Permissões

Todo cenário de autorização e toda tela do painel exigem
`$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` no `beforeEach` — Resource novo
nasce sem permission no banco e a tela responde 403 para quem não é `master_global`
(`.ai/rules/filament.md:31-42`).

---

## Regra R01 — Um cupom só passa a existir com os cinco atributos, e o tipo é um dos dois admitidos

> `RQ-02`, `RQ-03`, `RQ-04`, `RQ-05`, `RQ-06` · área A2, perfil **completo**
> Técnica: **EP** (uma partição inválida isolada por linha) + **partição exaustiva do discriminador**

```gherkin
# language: pt
Funcionalidade: Cadastro de cupons de desconto

  Regra: um cupom só passa a existir com código, tipo, valor, validade e limite de usos

    Cenário: [CT-01] o cadastro completo grava os cinco atributos e o cupom nasce sem nenhum uso
      Dado a administradora na tela de cadastro de cupons
      Quando ela cadastra o código "BLACKFRIDAY" do tipo percentual, valor 25, válido até
        2026-12-31 23:59 e limite de 40 usos
      Então existe um cupom cujo código é "BLACKFRIDAY", cujo tipo é percentual, cujo valor é 25,
        cuja validade é 2026-12-31 23:59 e cujo limite de usos é 40
      E o contador de usos desse cupom é 0

    Esquema do Cenário: [CT-02] falta um dos cinco atributos e o cupom não é gravado
      Dado a administradora na tela de cadastro de cupons
      Quando ela tenta cadastrar um cupom sem informar <atributo>
      Então o cadastro é recusado com erro no campo <atributo>
      E nenhum cupom existe

      Exemplos:
        | atributo         | # partição inválida isolada |
        | codigo           | ausência do identificador   |
        | tipo             | ausência do discriminador   |
        | valor            | ausência da grandeza        |
        | expira_em        | ausência do limite temporal |
        | limite_de_usos   | ausência do limite de uso   |

    Cenário: [CT-03] um tipo fora dos dois admitidos não é gravado
      Dado a administradora na tela de cadastro de cupons
      Quando ela tenta cadastrar o código "BRINDE10" com o tipo "brinde"
      Então o cadastro é recusado com erro no campo tipo
      E nenhum cupom existe

    Cenário: [CT-04] o contador de usos não é aceito como dado de entrada do cadastro
      Dado a administradora na tela de cadastro de cupons
      Quando ela cadastra o código "PROMO10" enviando também o contador de usos com o valor 99
      Então existe um cupom de código "PROMO10" cujo contador de usos é 0
```

> **Nota de derivação — CT-02**: as cinco linhas são partições inválidas **isoladas**, uma por
> linha. Combinar duas ausências no mesmo cenário faria a primeira validação a disparar mascarar a
> segunda, e o cenário provaria menos do que aparenta.
>
> **Nota de derivação — CT-04**: é o item *mass assignment* do checklist de taxonomia. O contador é
> a única grandeza da feature que o sistema move sozinho; aceitá-lo do formulário é o caminho para
> alguém "corrigir" o número de usos pela tela e furar RQ-11 sem nenhum log.
>
> **Por que o `Então` de CT-01 lista os cinco campos**: `assertDatabaseHas` só com o código passa
> com os outros quatro errados — inclusive com `valor` e `limite_de_usos` trocados entre si, que é
> um erro plausível de mapeamento de formulário.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o contador entra na lista de campos preenchíveis pelo formulário | CT-04 |
| M2 | um dos cinco campos não é obrigatório e grava nulo | CT-02 (a linha correspondente) |
| M3 | o tipo é gravado como texto livre, sem restrição aos dois valores | CT-03 |
| M4 | o contador nasce em 1 (ou nulo) em vez de 0 | CT-01 |
| M5 | `valor` e `limite_de_usos` são gravados trocados entre si | CT-01 |

---

## Regra R02 — O domínio de `valor` depende do `tipo`

> `RQ-03`, `RQ-04` · área A2, perfil **completo** · premissa **P-05** do `00-requisito.md`
> Técnica: **tabela de decisão** (`tipo` × faixa de `valor`) + **BVA 3-valores** (incremento 1, o
> tipo do campo é inteiro)

O card dá **dois tipos** e **um** valor. `10` significa "10%" num cupom e "R$ 0,10" no outro — logo
`valor` não tem um domínio, tem dois, e cada um com fronteiras próprias:

| `tipo` | Fronteira inferior | Fronteira superior |
|---|---|---|
| percentual | 0 (fora) · 1 (dentro) | 100 (dentro) · 101 (fora) |
| valor fixo | 0 (fora, `@premissa Q-03`) · 1 (dentro) | **não há** — 5.000 é válido |

```gherkin
# language: pt
  Regra: o percentual vai de 1 a 100; o valor fixo não tem teto superior

    Esquema do Cenário: [CT-05] a fronteira de valor muda com o tipo escolhido
      Dado a administradora na tela de cadastro de cupons, sem nenhum cupom cadastrado
      Quando ela tenta cadastrar o código "TESTE10" do tipo <tipo> com o valor <valor>
      Então o resultado é "<resultado>", e <evidencia>

      Exemplos:
        | tipo       | valor | resultado | evidencia                                              | # borda                                    |
        | percentual | 0     | recusado  | nenhum cupom existe                                    | borda inferior − 1                         |
        | percentual | 1     | aceito    | o cupom "TESTE10" tem tipo percentual e valor 1        | borda inferior                             |
        | percentual | 100   | aceito    | o cupom "TESTE10" tem tipo percentual e valor 100      | borda superior (número literal de P-05)    |
        | percentual | 101   | recusado  | nenhum cupom existe                                    | borda superior + 1                         |
        | fixo       | 0     | recusado  | nenhum cupom existe                                    | borda inferior − 1 (@premissa Q-03)        |
        | fixo       | 1     | aceito    | o cupom "TESTE10" tem tipo valor fixo e valor 1        | borda inferior — R$ 0,01                   |
        | fixo       | 5000  | aceito    | o cupom "TESTE10" tem tipo valor fixo e valor 5000     | acima de 100: o teto do percentual não vale aqui |

    Esquema do Cenário: [CT-43] o valor é reavaliado quando só ele muda na edição
      Dado um cupom percentual de valor 25 gravado
      E a administradora na tela de edição desse cupom
      Quando ela altera apenas o valor para <novo_valor> e salva
      Então o resultado é "<resultado>", e o valor gravado desse cupom é <valor_final>

      Exemplos:
        | novo_valor | resultado | valor_final | # borda                        |
        | 101        | recusado  | 25          | borda superior + 1, na edição  |
        | 100        | aceito    | 100         | borda superior, na edição      |

    Cenário: [CT-44] o valor fixo cadastrado pela tela é gravado em centavos e desconta o mesmo   @premissa P-05
      Dado a administradora na tela de cadastro de cupons, sem nenhum cupom cadastrado
      Quando ela cadastra o código "CINQUENTA" do tipo valor fixo com o desconto de R$ 50,00,
        validade futura e limite de 40 usos
      Então o valor gravado desse cupom é 5000
      E aplicar "CINQUENTA" sobre um total de 12990 centavos devolve 7990 centavos

    Cenário: [CT-06] trocar o tipo na edição reavalia o domínio do valor já gravado
      Dado um cupom de valor fixo com o valor 5000 gravado
      E a administradora na tela de edição desse cupom
      Quando ela troca o tipo para percentual sem alterar o valor
      Então a alteração é recusada com erro no campo valor
      E o tipo do cupom continua sendo valor fixo e o valor continua 5000
```

> **Nota de derivação — CT-05, linha `fixo / 5000`**: é a linha que distingue "teto de 100 aplicado
> ao campo" de "teto de 100 aplicado ao percentual". Sem ela, um `->maxValue(100)` incondicional
> passa em todas as outras linhas e limita todo cupom fixo a R$ 1,00 — defeito que só aparece no dia
> em que alguém tenta cadastrar um desconto de R$ 50,00.
>
> **Nota de derivação — CT-06**: é o ponto **edição** do trio criação ≠ edição ≠ uso. A validação
> condicionada escrita no cadastro e esquecida no salvamento é invisível para qualquer cenário que
> só crie — e aqui ela produz o pior resultado possível: um cupom de "5.000%".
>
> **Por que o `Então` de CT-06 afirma o valor gravado**: "recusado" sozinho passa com uma
> implementação que grava e depois reclama. **A mesma exigência vale para cada linha de CT-05 e
> CT-43**: a linha `recusado` afirma que **nada foi gravado**, e a linha `aceito` afirma **o valor
> persistido**. Sem as duas metades, um teto que **corta** o valor para 100 em vez de recusar — ou
> um piso que grava 1 no lugar do 0 enviado — passa na tabela inteira. *(achado L8 da revisão
> adversarial.)*
>
> **Nota de derivação — CT-43**: CT-06 muda o **tipo** e mantém o valor; CT-43 mantém o tipo e
> empurra o **valor** para fora do domínio. São dois pontos de edição diferentes, e fechar um não
> fecha o outro. *(achado L9.)*

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o teto de 100 é aplicado ao campo, valendo também para o valor fixo | CT-05 (linha `fixo / 5000`) |
| M2 | não há teto nenhum: percentual 101 é aceito | CT-05 (linha `percentual / 101`) |
| M3 | `<` no lugar de `<=` no teto: percentual 100 é recusado | CT-05 (linha `percentual / 100`) |
| M4 | o domínio é validado no cadastro e não no salvamento da edição, para o **tipo** | CT-06 |
| M5 | não há piso: valor 0 é aceito nos dois tipos | CT-05 (linhas `0`) |
| M6 | o valor fora do domínio é **cortado** para a borda em vez de recusado | CT-05 (`evidencia` das linhas `recusado`) — *revisão adversarial, L8* |
| M7 | o domínio do **valor** é validado no cadastro e não no salvamento da edição | CT-43 — *revisão adversarial, L9* |
| M8 | a tela grava o valor fixo em **reais** enquanto o motor o lê em centavos (ou multiplica por 100 onde não devia) | CT-44 — *revisão adversarial (2ª rodada), L01* |

> **Nota de derivação — CT-44** *(achado L01 da 2ª rodada, e o mais caro do conjunto)*: CT-01 e
> CT-B01 são os únicos cenários que afirmam valor persistido **a partir da tela**, e ambos usam
> tipo **percentual**, onde não existe conversão de unidade. Todo cupom de valor fixo do conjunto
> nascia por factory, escrevendo direto no banco. A costura formulário → banco → motor no ramo
> `fixo` não tinha **nenhum** cenário: um cupom de "R$ 50,00" cadastrado pela tela concederia
> R$ 0,50 de desconto com o conjunto inteiro verde. É a aplicação de *toda partição do
> discriminador se repete em cada efeito* ao efeito que faltava — o da **gravação**.

---

## Regra R03 — Validade e limite de usos só admitem valores que deixam o cupom utilizável

> `RQ-05`, `RQ-06` · área A2, perfil **completo** · `@premissa Q-01`, `@premissa Q-02`
> Técnica: **BVA 3-valores** em **dois pontos de entrada** (criação e edição). Incremento: 1 minuto
> para a validade (o campo é datado ao minuto), 1 para o limite (inteiro).

```gherkin
# language: pt
  Regra: um cupom não é gravado com validade já vencida nem com limite de usos que o inutiliza

    Esquema do Cenário: [CT-07] a validade gravada tem de estar no futuro   @premissa Q-01
      Dado o instante congelado em 2026-08-15 10:00
      E a administradora na tela de cadastro de cupons, sem nenhum cupom cadastrado
      Quando ela tenta cadastrar o código "TESTE10" com validade em <validade>
      Então o resultado é "<resultado>", e <evidencia>

      Exemplos:
        | validade         | resultado | evidencia                                                  | # borda        |
        | 2026-08-15 09:59 | recusado  | nenhum cupom existe                                        | borda − 1 min  |
        | 2026-08-15 10:01 | aceito    | a validade gravada de "TESTE10" é 2026-08-15 10:01         | borda + 1 min  |
        | 2026-08-14 10:00 | recusado  | nenhum cupom existe                                        | um dia atrás   |

    Esquema do Cenário: [CT-08] o limite de usos tem piso, e ele vale nos dois pontos de escrita   @premissa Q-02
      Dado a administradora operando o cadastro de cupons, e um cupom "PROMO10" de limite 40
        quando a operação for de edição
      Quando ela informa o limite de usos <limite> na operação de <ponto>
      Então o resultado é "<resultado>", e <evidencia>

      Exemplos:
        | ponto   | limite | resultado | evidencia                                          | # borda            |
        | criação | 0      | recusado  | nenhum cupom novo existe                           | borda − 1          |
        | criação | 1      | aceito    | o limite gravado do cupom novo é 1                 | borda              |
        | edição  | 0      | recusado  | o limite de "PROMO10" continua 40                  | a regra sobrevive ao salvamento |
        | edição  | 2      | aceito    | o limite de "PROMO10" passa a ser 2                | célula válida da coluna edição  |

    Cenário: [CT-49] informar só a data de validade guarda o fim do dia, não o começo   @premissa 00/pergunta-5
      Dado a administradora na tela de cadastro de cupons
      Quando ela cadastra o código "VIRADA" informando apenas a data de validade 2026-12-31
      Então a validade gravada desse cupom é 2026-12-31 23:59:59
      E aplicar "VIRADA" em 2026-12-31 às 18:00 sobre um total de 10000 centavos devolve 9000 centavos

    Cenário: [CT-09] a validade não pode ser empurrada para o passado pela edição   @premissa Q-01
      Dado o instante congelado em 2026-08-15 10:00
      E um cupom com validade em 2026-09-30 10:00
      Quando a administradora tenta alterar a validade desse cupom para 2026-08-14 10:00
      Então a alteração é recusada com erro no campo de validade
      E a validade do cupom continua sendo 2026-09-30 10:00
```

> **Nota de derivação — CT-08**: a coluna `edição` tem uma linha **inválida** e uma **válida**. Só a
> inválida deixaria a operação de edição sem nenhuma célula bem-sucedida exercitada, e é assim que a
> armadilha de "a edição nunca grava" passa inteira.
>
> **Nota de derivação — CT-09**: é o irmão de CT-06 no eixo temporal. A pergunta Q-01 bloqueia os
> dois; se a resposta for "pode nascer vencido", os dois invertem o `Então` — e **nada mais** muda,
> que é o custo declarado da premissa.
>
> **Por que cada linha de CT-07 e CT-08 tem uma coluna `evidencia`**: as linhas `recusado` afirmam
> o **não-efeito** e as linhas `aceito` afirmam **o valor persistido**. Uma implementação que
> **substitui** a validade inválida pelo instante corrente, ou que grava 1 quando recebe 0, é
> indistinguível de uma correta num oráculo de uma palavra. *(achado L8 da revisão adversarial.)*

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a validade no passado é aceita na gravação | CT-07 (linha `borda − 1 min`) |
| M2 | a validade é validada na criação e não na edição | CT-09 |
| M3 | a comparação da gravação usa o **dia** e não o instante: 09:59 do mesmo dia passa | CT-07 (linha `borda − 1 min`) |
| M4 | o piso do limite não existe: 0 é aceito | CT-08 (linha `criação / 0`) |
| M5 | o piso do limite existe na criação e não na edição | CT-08 (linha `edição / 0`) |
| M6 | a validação de validade recusa também o futuro próximo (`>=` invertido) | CT-07 (linha `borda + 1 min`) |
| M7 | o valor inválido é **substituído** pelo permitido em vez de recusado (validade vira "agora", limite vira 1) | CT-07 e CT-08 (coluna `evidencia`) — *revisão adversarial, L8* |
| M8 | a data informada sem hora é gravada como `00:00:00`, encurtando a campanha em um dia | CT-49 — *revisão adversarial (2ª rodada), L14* |

> **Nota de derivação — CT-49** *(achado L14 da 2ª rodada)*: a quinta pergunta aberta do
> `00-requisito.md` fixa a premissa — *"se a tela oferecer só a data, o valor gravado é 23:59:59 do
> dia"*. É premissa **do `00`**, portanto oráculo legítimo pela própria regra da seção
> `## Fronteira com o Plano`, e nenhum cenário a exercia: CT-07 e CT-09 sempre informam hora
> explícita, e CT-21 exerce a fronteira no motor, com o valor já gravado. Um seletor só de data
> mata a campanha à meia-noite do dia que o operador digitou como **último dia válido**, e o
> conjunto ficava verde. É BVA aplicada à tradução entrada → armazenamento, não ao uso.

---

## Regra R04 — O código identifica o cupom de forma única dentro da organização

> `RQ-02`, `RQ-14` · área A2, perfil **completo** · premissa **P-04** do `00-requisito.md`
> Técnica: **normalização de identidade** (caixa, espaços nas bordas) + **unicidade contra o próprio
> registro**

```gherkin
# language: pt
  Regra: dentro de uma organização, dois cupons não têm o mesmo código, e caixa e espaços não criam códigos diferentes

    Esquema do Cenário: [CT-10] variações de caixa e de espaço são o mesmo código
      Dado um cupom de código "PROMO10", percentual de 25, com limite de 40 usos na organização Acme
      E a administradora da Acme na tela de cadastro de cupons
      Quando ela tenta cadastrar o código <codigo_digitado>
      Então o cadastro é recusado com erro no campo código
      E o único cupom da Acme continua sendo "PROMO10", com valor 25 e limite 40

      Exemplos:
        | codigo_digitado | # variação           |
        | promo10         | caixa baixa          |
        | Promo10         | caixa mista          |
        | "  PROMO10  "   | espaços nas bordas   |
        | " promo10 "     | caixa e espaço juntos|

    Cenário: [CT-38] renomear um cupom para o código de outro é recusado
      Dado dois cupons na organização Acme: "PROMO10" percentual de 25 e "BEMVINDO" percentual de 10
      E a administradora na tela de edição de "BEMVINDO"
      Quando ela altera o código de "BEMVINDO" para "promo10" e salva
      Então a alteração é recusada com erro no campo código
      E o código desse cupom continua "BEMVINDO"
      E a Acme continua com exatamente um cupom de código "PROMO10", de valor 25

    Cenário: [CT-39] o código entra normalizado pela porta de escrita e é aplicável depois
      Dado a administradora na tela de cadastro de cupons, sem nenhum cupom cadastrado
      Quando ela cadastra o código "  promo10 " como percentual de 10, com validade futura e
        limite de 40 usos
      Então o código gravado é "PROMO10"
      E aplicar o código "PROMO10" sobre um total de 10000 centavos devolve 9000 centavos
      E o contador de usos desse cupom passa a ser 1

    Cenário: [CT-11] salvar um cupom sem alterar o código não acusa colisão consigo mesmo
      Dado um cupom de código "PROMO10" com limite de 40 usos
      E a administradora na tela de edição desse cupom
      Quando ela altera apenas o limite de usos para 60 e salva
      Então o limite de usos desse cupom passa a ser 60
      E o código dele continua sendo "PROMO10"

    Cenário: [CT-12] o mesmo código em outra organização é aceito   @premissa P-04
      Dado um cupom de código "BEMVINDO" cadastrado na organização Acme
      E a administradora da organização Globex na tela de cadastro de cupons
      Quando ela cadastra o código "BEMVINDO"
      Então existe um cupom de código "BEMVINDO" na Globex
      E existe um cupom de código "BEMVINDO" na Acme

    Esquema do Cenário: [CT-13] o código digitado na aplicação encontra o cupom independentemente da forma
      Dado um cupom de código "PROMO10" válido e com uso disponível
      Quando o sistema aplica o código <codigo_digitado> sobre um total de 10000 centavos
      Então o total resultante é 9000 centavos

      Exemplos:
        | codigo_digitado | # variação         |
        | PROMO10         | forma canônica     |
        | promo10         | caixa baixa        |
        | "  PROMO10 "    | espaços nas bordas |
```

> **Nota de derivação — CT-13**: é o ponto **uso** do trio. A normalização aplicada só na escrita
> deixa o cupom gravado em maiúsculas e a busca sensível à caixa: quem digita `promo10` recebe
> "cupom não existe". O SQLite dos testes é case-sensitive por padrão, então o defeito é
> **observável** aqui — em MySQL com colação `_ci` ele ficaria escondido, e é por isso que a linha
> `caixa baixa` importa mais neste projeto do que pareceria.
>
> **Nota de derivação — CT-12**: exige duas organizações e **duas administradoras distintas**. Se a
> mesma pessoa cadastrasse nas duas, o cenário mediria unicidade e não escopo.
>
> **Nota de derivação — CT-38** *(achado L1)*: CT-11 prova que a colisão **não** acontece quando o
> código não muda; ele é a célula **positiva** da edição. A célula **negativa** — mudar o código
> para um que já existe — estava vazia, e a forma mais curta de fazer CT-11 passar é **desligar a
> regra de unicidade na edição**. Essa implementação passava nos quatro cenários anteriores e matava
> RQ-14 por inteiro.
>
> **Nota de derivação — CT-39** *(achado L2)*: em CT-10 e CT-13 as variações de caixa e espaço são
> sempre **entradas de consulta** — o registro gravado nasce canônico, plantado por factory. Logo, a
> implementação espelho ("normaliza na leitura, grava como digitado") passava em tudo. CT-39 é o
> único cenário em que a forma não-canônica atravessa a **porta de escrita**, e o `Então` fecha o
> ciclo de ida e volta: grava, encontra e aplica. A leitura no `Então` é deliberada — a
> findability do que foi gravado **é** o resultado observável, e separá-la em dois cenários
> devolveria a lacuna.
>
> **Nota de derivação — CT-10** *(achado L14)*: o `Então` afirma **qual** cupom sobrou, não quantos.
> `"continua com exatamente 1 cupom"` não distingue "a segunda gravação foi recusada" de "a segunda
> gravação substituiu a primeira" — um `updateOrCreate` no caminho de criação mantém a contagem em 1
> e passa nas quatro linhas.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a unicidade é sensível a caixa | CT-10 (linhas de caixa) |
| M2 | os espaços nas bordas não são removidos antes de comparar | CT-10 (linhas de espaço) |
| M3 | a unicidade é global à instalação, não por organização | CT-12 |
| M4 | a unicidade não ignora o próprio registro na edição | CT-11 |
| M5 | a normalização vale na leitura e não na escrita | CT-39 — *revisão adversarial, L2* |
| M6 | a normalização destrói o código (grava vazio ou truncado) | CT-11, CT-39 |
| M7 | a unicidade é desligada na edição para fazer o salvamento sem alteração passar | CT-38 — *revisão adversarial, L1* |
| M8 | a segunda gravação **substitui** a primeira em vez de ser recusada | CT-10 (`Então` de identidade) — *revisão adversarial, L14* |

---

## Regra R05 — Só o administrador cria, edita e exclui cupom

> `RQ-07` · área A3, perfil **padrão** · premissa **P-02** do `00-requisito.md`
> Técnica: **matriz papel × ação**, com a persona como dimensão e **cada verbo falsificado por si**

O card diz "criar, edita **e** exclui". São **três** permissões que podem falhar separadamente: uma
implementação que confere o ator na criação e esquece na exclusão passa em todo conjunto cuja
evidência venha só do primeiro verbo.

**A matriz é exaustiva no eixo do papel.** O `00-requisito.md` (A-02) tabula **cinco** papéis, e
RQ-07 é a única cláusula do card com a palavra *"só"* — que é uma afirmação sobre **todos os
outros**. Cobrir apenas o usuário comum deixa passar uma permissão anexada por engano a `infra` ou
ao `admin` da instalação (erro corriqueiro na geração de permissões para um Resource novo), e
deixa passar uma policy escrita como *nega o usuário comum* em vez de *permite o administrador*.

| Persona \ Ação | criar | editar | excluir | listar |
|---|---|---|---|---|
| `admin_organizacao` (a administradora) | CT-15 | CT-15 | CT-15 | CT-18 |
| `panel_user` (usuário comum) | CT-14 | CT-14 | CT-14 | CT-17 (**permitido**) |
| `admin_organizacao` de **outra** organização | — (não alcança o registro) | CT-16 | CT-16 | CT-41 |
| `admin` da instalação | CT-42 | — (implicado por criar/excluir) | CT-42 | — |
| `infra` | CT-42 | — | CT-42 | — |
| autenticado **sem papel** na organização | CT-42 | — | CT-42 | — |
| `master_global` | variante single-tenant de CT-15 | idem | idem | — |

> **Amostragem declarada**: nas três últimas personas de recusa, CT-42 exercita `criar` e `excluir`
> — o verbo de entrada e o destrutivo — e **não** `editar`. Uma implementação que barrasse os dois e
> liberasse o `editar` para o papel `infra` passaria. É amostragem consciente, não cobertura: o
> custo de fechá-la é uma linha na tabela de `Exemplos`, e ela entra no dia em que a matriz do
> Shield deixar de gerar os três afixos juntos.

```gherkin
# language: pt
  Regra: criar, editar e excluir cupom são operações do administrador

    Esquema do Cenário: [CT-14] o usuário comum é barrado em cada uma das três operações de escrita
      Dado um cupom de código "PROMO10" com limite de 40 usos na organização Acme
      E o usuário comum autenticado nessa organização
      Quando ele dispara a operação de <operacao> sobre o cadastro de cupons
      Então a operação é negada
      E a organização Acme continua com exatamente 1 cupom, de código "PROMO10" e limite 40

      Exemplos:
        | operacao | # verbo do card |
        | criar    | "criar"         |
        | editar   | "editar"        |
        | excluir  | "excluir"       |

    Esquema do Cenário: [CT-15] a administradora executa cada uma das três operações de escrita
      Dado um cupom "PROMO10", percentual de 25, com validade futura e limite de 40 usos na Acme
      E a administradora autenticada nessa organização
      Quando ela executa a operação de <operacao>
      Então <evidencia>

      Exemplos:
        | operacao | evidencia                                                                          |
        | criar    | a Acme tem 2 cupons, e o novo é "NOVO10" com tipo, valor, validade e limite exatamente como informados |
        | editar   | a Acme tem 1 cupom, "PROMO10", cujo limite de usos passou de 40 para 60            |
        | excluir  | a Acme tem 0 cupom, e nenhum de código "PROMO10" existe                            |

    Esquema do Cenário: [CT-16] a administradora de outra organização não alcança o cupom em nenhum verbo
      Dado um cupom "PROMO10", percentual de 25, com limite de 40 usos na organização Acme
      E a administradora da organização Globex autenticada
      Quando ela submete a operação de <operacao> sobre esse cupom, pelo identificador do registro alheio
      Então a operação resulta em registro não encontrado
      E a Acme continua com exatamente 1 cupom, de código "PROMO10", valor 25 e limite 40

      Exemplos:
        | operacao                        | # verbo                        |
        | alterar o limite para 999       | célula `editar` da matriz      |
        | excluir                         | célula `excluir` da matriz     |

    Esquema do Cenário: [CT-42] nenhum outro papel escreve cupom
      Dado um cupom "PROMO10", percentual de 25, com limite de 40 usos na organização Acme
      E uma pessoa autenticada cujo papel é <papel>
      Quando ela dispara a operação de <operacao> sobre o cadastro de cupons dessa organização
      Então a operação é negada
      E a Acme continua com exatamente 1 cupom, de código "PROMO10", valor 25 e limite 40

      Exemplos:
        | papel                              | operacao | # célula da matriz                    |
        | infra                              | criar    | papel de observabilidade              |
        | infra                              | excluir  | idem, verbo destrutivo                |
        | admin da instalação                | criar    | administra a instalação, não o negócio|
        | admin da instalação                | excluir  | idem, verbo destrutivo                |
        | nenhum papel na organização        | criar    | autenticado sem papel de negócio      |
        | nenhum papel na organização        | excluir  | idem, verbo destrutivo                |
```

> **Nota de derivação — CT-14**: o `Quando` **dispara a operação**, não consulta a permissão.
> Afirmar `can()` deixa passar a implementação em que a policy está certa e a tela nunca a consulta
> — o defeito real do checklist de taxonomia. E o `Então` afirma o **não-efeito** (o cupom intacto),
> porque "negado" sozinho passa com uma implementação que grava antes de reclamar.
>
> **Nota de derivação — CT-16**: é o item IDOR / autorização horizontal. As duas administradoras
> têm o **mesmo papel**; o que as separa é a organização, e é exatamente essa barreira que o cenário
> falsifica. Persona colapsada (a mesma pessoa nas duas organizações) não exercitaria nada.
> **Os dois verbos são exercitados** *(achado L6)*: a matriz escrevia CT-16 nas células `editar` e
> `excluir`, e o cenário fazia só a abertura da edição — a célula destrutiva estava vazia enquanto o
> checklist a lia como ✅. Vale aqui o mesmo argumento de CT-14: verbo irmão não herda evidência.
>
> **Nota de derivação — CT-15** *(achado L13)*: o `Dado` fixa o cupom inicial com **todos** os
> atributos. Antes ele dizia só "a administradora autenticada", e as linhas `editar` e `excluir`
> pressupunham um `PROMO10` de limite 40 que nada criava — o cenário não era executável como
> escrito. E a evidência da linha `criar` afirma os cinco atributos, não só o código: é o mesmo
> defeito de mapeamento de formulário que a nota de CT-01 existe para pegar.
>
> **Modo single-tenant**: os mesmos três verbos, com `master_global` no lugar da administradora e
> `panel_user` no lugar do usuário comum, rodam em `tests/Kit/CupomTest.php`. Sem isso, o modo
> default do kit fica sem nenhum caso de autorização.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o ator é conferido na criação e não na edição | CT-14 (linha `editar`) |
| M2 | o ator é conferido na criação e na edição, e não na exclusão | CT-14 (linha `excluir`) |
| M3 | a autorização só esconde o botão; a operação continua chamável | CT-14 (o `Quando` dispara a operação) |
| M4 | a recusa acontece depois de gravar | CT-14 (`Então` afirma o cupom intacto) |
| M5 | a escrita é vedada a todos, inclusive à administradora | CT-15 |
| M6 | o recorte é por organização e não por papel: a administradora de outra organização edita | CT-16 (linha `editar`) |
| M7 | a barreira entre organizações existe na edição e não na exclusão | CT-16 (linha `excluir`) — *revisão adversarial, L6* |
| M8 | a policy é escrita como *nega o usuário comum* em vez de *permite o administrador*, e todo papel não previsto passa | CT-42 — *revisão adversarial, L7* |

---

## Regra R06 — O usuário não-administrador lista exatamente os cupons ativos

> `RQ-08` · área A3, perfil **padrão** · premissa **P-03** do `00-requisito.md` ("ativo" é derivado
> da validade **e** do limite, sem coluna própria)
> Técnica: **tabela estado × operação** + **partição exaustiva do estado derivado**

O estado de um cupom não é um enum gravado: é a combinação de duas condições. A partição é
exaustiva e tem quatro células, e a de borda (`usos = limite − 1`) é a única que distingue `<` de
`<=`.

| `usos` vs `limite` | validade | estado derivado | usuário comum vê? |
|---|---|---|---|
| `<` (folga) | futura | ativo | sim |
| `= limite − 1` | futura | ativo (borda) | **sim** |
| `= limite` | futura | esgotado | não |
| **`> limite`** | futura | esgotado | **não** — célula alcançável pela premissa Q-05 |
| `<` | passada | vencido | não |

> **A quinta célula não é hipotética** *(achado L04 da 2ª rodada)*: a pergunta **Q-05** assume que
> reduzir o limite abaixo dos usos já feitos **é permitido**. Essa premissa não tinha nenhum
> cenário, nem de escrita nem de leitura — e é o único caminho que produz `usos > limite`. Sem
> ela, um `usos != limite_de_usos` (a tradução literal e ingênua de *"não estourou o limite"*)
> satisfaz as quatro células originais, e o cupom **reaparece como ativo** na lista depois da
> redução. No motor, CT-22 (linha `borda + 1`) já cobre a recusa, então o defeito ficava confinado
> à listagem, onde nada o via.

```gherkin
# language: pt
  Regra: a lista do usuário comum contém os cupons dentro da validade e com uso disponível, e nenhum outro

    Esquema do Cenário: [CT-17] a lista do usuário comum reflete o estado derivado de cada cupom
      Dado quatro cupons na organização Acme: "FOLGA" com 0 de 40 usos e validade futura,
        "ULTIMO" com 39 de 40 usos e validade futura, "CHEIO" com 40 de 40 usos e validade futura,
        e "VENCIDO" com 0 de 40 usos e validade no passado
      E o usuário comum autenticado nessa organização
      Quando ele abre a lista de cupons
      Então ele vê o cupom <codigo> na lista: "<visivel>"

      Exemplos:
        | codigo  | visivel | # célula da partição            |
        | FOLGA   | sim     | dentro da validade, com folga   |
        | ULTIMO  | sim     | borda: último uso disponível    |
        | CHEIO   | não     | limite atingido                 |
        | VENCIDO | não     | fora da validade                |

    Cenário: [CT-18] a administradora vê também os cupons que não estão ativos
      Dado os mesmos quatro cupons "FOLGA", "ULTIMO", "CHEIO" e "VENCIDO" na organização Acme
      E a administradora autenticada nessa organização
      Quando ela abre a lista de cupons
      Então ela vê os quatro cupons na lista

    Cenário: [CT-19] o cupom que vence entre duas consultas desaparece da lista do usuário comum
      Dado um cupom "RELAMPAGO" com validade em 2026-08-15 10:00 na organização Acme
      E o usuário comum autenticado nessa organização
      Quando ele abre a lista em 2026-08-15 09:59 e de novo em 2026-08-15 10:01
      Então na primeira consulta ele vê "RELAMPAGO"
      E na segunda ele não vê "RELAMPAGO"

    Cenário: [CT-46] reduzir o limite abaixo dos usos já feitos esgota o cupom   @premissa Q-05
      Dado um cupom "PROMO10" com 7 de 40 usos e validade futura na organização Acme
      Quando a administradora reduz o limite de usos desse cupom para 5
      Então o limite gravado passa a ser 5
      E o usuário comum não vê "PROMO10" na lista
      E aplicar "PROMO10" sobre 10000 centavos é recusado, e o contador continua 7

    Cenário: [CT-48] o usuário comum não alcança um cupom não-ativo pelo endereço direto
      Dado um cupom "VENCIDO" fora da validade na organização Acme
      E o usuário comum autenticado nessa organização
      Quando ele tenta abrir esse cupom pelo endereço direto
      Então o acesso resulta em registro não encontrado

    Cenário: [CT-41] a lista nunca contém cupom de outra organização
      Dado o cupom "ACME10" ativo na organização Acme e o cupom "GLOBEX10" ativo na Globex
      E o usuário comum e a administradora, ambos da Acme
      Quando cada um deles abre a lista de cupons da Acme
      Então os dois veem "ACME10"
      E nenhum dos dois vê "GLOBEX10"
```

> **Nota de derivação — CT-17**: a partição do estado é **exaustiva**, não amostrada. Cobrir só
> "ativo" e "vencido" deixaria o esgotado de fora, que é a metade da definição de "ativo" que P-03
> escreveu — e é a que um `where('expira_em', '>', now())` sozinho esquece.
>
> **Nota de derivação — CT-18**: é a **célula válida** da outra linha da matriz. Sem ela, o recorte
> aplicado a todo mundo (inclusive à administradora, que precisa ver o vencido para prorrogá-lo)
> ficaria verde.
>
> **Nota de derivação — CT-19**: distingue "estado derivado a cada leitura" de "estado calculado uma
> vez e gravado". Um estado persistido só divergiria com a passagem do tempo, e nenhum outro cenário
> a exercita. O instante escolhido cai **dentro da janela de divergência** (um minuto ao redor da
> fronteira), não num ponto conveniente. **As duas leituras são passos do cenário** *(achado L15)*:
> antes, a primeira leitura e a primeira observação estavam escondidas no `Dado`, e o cenário
> passava **por vacuidade** — um recorte que nunca devolvesse nada satisfaria o único `Então`
> escrito, e o cenário existe justamente para matar o mutante do estado persistido.
>
> **Nota de derivação — CT-41** *(achado L5)*: CT-17, CT-18, CT-19 e CT-37 montam cupons de **uma
> organização só**, e a varredura SFDIPOT declarava "dado de outra organização" como coberto por
> eles. Não estava: com um tenant só no ambiente, um `getEloquentQuery()` que **descarta** o builder
> escopado para aplicar o recorte de ativos fica verde — e o usuário comum passa a ler a carteira de
> cupons do outro cliente, que é o vazamento entre tenants que o `00` (A-04) chama de motivo de
> existir do kit. CT-16 prova 404 na **edição direta**; recorte de **coleção** é outra coisa.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o recorte de ativos é aplicado a todo mundo, inclusive à administradora | CT-18 |
| M2 | "ativo" considera só a validade e ignora o limite de usos | CT-17 (linha `CHEIO`) |
| M3 | "ativo" considera só o limite e ignora a validade | CT-17 (linha `VENCIDO`) |
| M4 | `<=` no lugar de `<` na comparação de usos: o cupom no último uso já some | CT-17 (linha `ULTIMO`) |
| M5 | o estado é calculado na gravação e persistido, em vez de derivado na leitura | CT-19 |
| M6 | o ramo do usuário comum **reconstrói** a consulta e perde o escopo de organização | CT-41 — *revisão adversarial, L5* |
| M7 | o recorte esconde tudo (a lista volta sempre vazia) | CT-19 (primeira leitura), CT-41 |
| M8 | `usos != limite_de_usos` no lugar de `usos < limite_de_usos`: o cupom com o limite reduzido volta a aparecer | CT-46 — *revisão adversarial (2ª rodada), L04* |
| M9 | o recorte existe na listagem e a leitura de um registro isolado fica aberta | CT-48 — *revisão adversarial (2ª rodada), L13* |

> **Nota de derivação — CT-48** *(achado L13 da 2ª rodada)*: RQ-08 diz *"podem **apenas** listar os
> cupons ativos"*. O conjunto cobria o "apenas" no eixo de **escrita** (CT-14) e o "ativos" no eixo
> da **listagem** (CT-17), e deixava de fora a terceira superfície: ler **um** registro por endereço
> direto. Uma policy que restringe `create`/`update`/`delete` e deixa `view` aberta — o default
> quando se marcam só os três afixos de escrita — viola RQ-08 e passava nos dois. Listar não é a
> mesma operação que visualizar, nem a mesma permission.

---

## Regra R07 — A aplicação recusa código inexistente, vencido ou esgotado, sem deixar efeito

> `RQ-09`, `RQ-10`, `RQ-11` · área A1, perfil **completo**
> Técnica: **EP** com partições inválidas isoladas + **BVA 3-valores** (incremento 1 segundo para o
> instante, 1 para o contador)

```gherkin
# language: pt
Funcionalidade: Aplicação do cupom sobre um total

  Regra: a aplicação recusa o cupom que não existe, que venceu ou que esgotou, e a recusa não consome nada

    Esquema do Cenário: [CT-20] código que não identifica cupom nenhum é recusado
      Dado os cupons "PROMO10" e "NATAL50" válidos e sem uso na organização
      Quando o sistema tenta aplicar o código <codigo> sobre um total de 10000 centavos
      Então a aplicação é recusada
      E o total continua 10000 centavos
      E o contador de usos de "PROMO10" e o de "NATAL50" continuam 0

      Exemplos:
        | codigo      | # partição inválida isolada          |
        | INEXISTENTE | código que não existe                |
        | ""          | vazio                                |
        | ausente     | nulo / não informado                 |
        | "   "       | só espaços                           |
        | "%"         | metacaractere de padrão              |
        | "_"         | metacaractere de caractere único     |
        | "PROMO_0"   | metacaractere embutido em código real|
        | "PROM%"     | prefixo com metacaractere            |

    Cenário: [CT-40] a aplicação encontra o cupom do código pedido, e não outro
      Dado os cupons "PROMO10" percentual de 10% e "NATAL50" percentual de 50%, válidos e sem uso
      Quando o sistema aplica "PROMO10" sobre um total de 10000 centavos
      Então o total resultante é 9000 centavos
      E o contador de usos de "PROMO10" é 1
      E o contador de usos de "NATAL50" continua 0

    Cenário: [CT-47] códigos homônimos em organizações diferentes não se confundem   @premissa P-04
      Dado o cupom "BEMVINDO" percentual de 10% na organização Acme e o cupom "BEMVINDO"
        percentual de 50% na Globex, ambos válidos e sem uso
      Quando o sistema, no contexto da Acme, aplica "BEMVINDO" sobre um total de 10000 centavos
      Então o total resultante é 9000 centavos
      E o contador de usos do cupom da Acme é 1, e o do cupom da Globex continua 0
      E o registro de uso aponta para o cupom da Acme

    Esquema do Cenário: [CT-21] a validade é conferida contra o instante gravado
      Dado o instante congelado em 2026-08-15 10:00:00
      E um cupom "PROMO10" com uso disponível e validade em <validade>
      Quando o sistema tenta aplicar "PROMO10" sobre um total de 10000 centavos
      Então o total resultante é <total> centavos
      E o contador de usos de "PROMO10" é <usos>

      Exemplos:
        | validade            | total | usos | # borda      |
        | 2026-08-15 10:00:01 | 9000  | 1    | borda + 1 s  |
        | 2026-08-15 10:00:00 | 10000 | 0    | borda exata  |
        | 2026-08-15 09:59:59 | 10000 | 0    | borda − 1 s  |

    Esquema do Cenário: [CT-22] o limite de usos é conferido antes de consumir
      Dado um cupom "PROMO10" válido, com limite de 3 usos e <ja_usado> usos já feitos
      Quando o sistema tenta aplicar "PROMO10" sobre um total de 10000 centavos
      Então o total resultante é <total> centavos
      E o contador de usos de "PROMO10" é <usos_depois>

      Exemplos:
        | ja_usado | total | usos_depois | # borda      |
        | 1        | 9000  | 2           | dentro       |
        | 2        | 9000  | 3           | borda − 1    |
        | 3        | 10000 | 3           | borda        |
        | 4        | 10000 | 4           | borda + 1    |

    Esquema do Cenário: [CT-23] as três recusas valem igualmente para o cupom de valor fixo
      Dado um cupom de valor fixo de 1000 centavos, com limite de 3 usos e <ja_usado> usos feitos,
        na situação <situacao>
      Quando o sistema tenta aplicar o código desse cupom sobre um total de 10000 centavos
      Então a aplicação é recusada
      E o total continua 10000 centavos
      E o contador de usos desse cupom continua <ja_usado>
      E não existe registro de uso desse cupom

      Exemplos:
        | situacao                | ja_usado | # partição do discriminador × recusa |
        | validade no passado     | 1        | vencido, tipo fixo                   |
        | usos iguais ao limite   | 3        | esgotado, tipo fixo                  |

    Cenário: [CT-24] o código de outra organização não é encontrado
      Dado um cupom "BEMVINDO" válido cadastrado apenas na organização Globex
      E o sistema operando no contexto da organização Acme
      Quando ele tenta aplicar o código "BEMVINDO" sobre um total de 10000 centavos
      Então a aplicação é recusada
      E o total continua 10000 centavos
      E o contador de usos de "BEMVINDO" na Globex continua 0
```

> **Nota de derivação — CT-20**: `""`, ausente e `"   "` são **três** casos, não um. É o item
> *ausente ≠ null ≠ vazio* do checklist, e aqui ele tem consequência concreta: uma consulta que
> recebe vazio sem guarda devolve o **primeiro cupom da tabela**, e o cliente ganha desconto sem
> digitar código nenhum.
>
> **Nota de derivação — CT-21**: a borda exata (`validade == agora`) é a linha que distingue `>` de
> `>=`. O `Então` afirma o **total** e o **contador**, não "recusado": a implementação que consome o
> uso e depois recusa passa em qualquer oráculo mais fraco.
>
> **Nota de derivação — CT-23**: é a aplicação direta de *toda partição de EP se repete em cada
> rastreio de efeito*. Todos os demais cenários de recusa usam cupom percentual; um atalho no ramo
> de valor fixo — que ignorasse validade e limite e aplicasse direto — ficaria **verde no conjunto
> inteiro** sem esta linha.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | código vazio ou nulo devolve o primeiro cupom da tabela | CT-20 (linhas `""`, `ausente`, `"   "`) |
| M2 | a validade é comparada com `>=`: o cupom vale no instante exato do vencimento | CT-21 (linha `borda exata`) |
| M3 | o limite é comparado com `<=`: o uso além do limite é aceito | CT-22 (linha `borda`) |
| M4 | a recusa acontece **depois** de consumir o uso | CT-21 e CT-22 (`Então` afirma o contador) |
| M5 | validade e limite são conferidos só no ramo percentual | CT-23 |
| M6 | a busca por código ignora a organização corrente | CT-24, CT-47 |
| M7 | a busca usa `LIKE` para ser insensível a caixa, e `%`/`_` viram curingas | CT-20 (linhas de metacaractere) — *revisão adversarial, L3* |
| M8 | a busca devolve **algum** cupom em vez do cupom do código pedido | CT-40 — *revisão adversarial, L3* |
| M9 | o consumo atômico é escrito no Query Builder e **perde o escopo de organização**, resgatando o homônimo do outro cliente | CT-47 — *revisão adversarial (2ª rodada), L05* |

> **Nota de derivação — CT-40 e CT-20** *(achado L3)*: todo cenário de R07 a R10 tinha **um cupom
> só** no ambiente, e com um cupom só *"achou o certo"* e *"achou algum"* são indistinguíveis. Os
> metacaracteres entram porque `LIKE` é a saída mais provável de quem lê "a busca precisa ser
> insensível a caixa" — e no SQLite ele resolve isso numa linha, abrindo `%` como curinga: aplicar
> o código `%` devolveria o primeiro cupom da tabela, que é exatamente o buraco que CT-20 declara
> querer fechar.
>
> **Nota de derivação — CT-47** *(achado L05 da 2ª rodada, e o mais sutil)*: CT-24 monta o cupom em
> **uma** organização só — com fixture não colidente, "buscou na organização certa" e "achou o
> primeiro que casa o código" produzem o mesmo resultado. A configuração que discrimina as duas é o
> **homônimo**, que CT-12 declara legal e nenhum cenário de aplicação montava. E o alvo é preciso:
> o consumo atômico **tem** de ser escrito no Query Builder (é o que o torna atômico), e o Query
> Builder **não aplica escopo global de organização** — o mesmo fato que o `00` (A-08) registra
> quando diz que ele não dispara eventos de model, visto por outro ângulo.

---

## Regra R08 — O total recebe o desconto do tipo e do valor do cupom, truncado e limitado em zero

> `RQ-12` · área A1, perfil **completo** · premissas **P-05** (unidade), **P-06** (truncar),
> **P-07** (nunca negativo) do `00-requisito.md`
> Técnica: **tabela de decisão** (`tipo` × relação desconto/total) + **valores discriminantes**

Os valores abaixo foram escolhidos para **discriminar**, não por serem redondos. Um percentual
calculado em ponto flutuante e um percentual calculado em inteiro dão o **mesmo** resultado em
"10% de 10.000"; divergem em "29% de 10.000".

```gherkin
# language: pt
  Regra: o desconto percentual incide sobre o total e é truncado; o desconto fixo é subtraído; o resultado nunca fica negativo

    Esquema do Cenário: [CT-25] o desconto percentual é calculado em inteiro e truncado para baixo   @premissa P-06
      Dado um cupom percentual de <percentual>% válido e com uso disponível
      Quando o sistema aplica esse cupom sobre um total de <total> centavos
      Então o total resultante é <resultado> centavos

      Exemplos:
        | percentual | total | resultado | # o que discrimina                                       |
        | 29         | 10000 | 7100      | inteiro dá 2900 de desconto; ponto flutuante dá 2899     |
        | 10         | 9999  | 9000      | truncar dá 999; arredondar dá 1000 e o total seria 8999  |
        | 5          | 50    | 48        | truncar dá 2; arredondar 2,5 dá 3 e o total seria 47     |
        | 33         | 101   | 68        | truncar dá 33; arredondar 33,33 dá o mesmo — controle    |

    Esquema do Cenário: [CT-26] o desconto de valor fixo é subtraído em centavos e nunca deixa o total negativo   @premissa P-07
      Dado um cupom de valor fixo de <fixo> centavos, válido e com uso disponível
      Quando o sistema aplica esse cupom sobre um total de <total> centavos
      Então o total resultante é <resultado> centavos

      Exemplos:
        | fixo | total | resultado | # borda                                       |
        | 1000 | 12990 | 11990     | desconto menor que o total                    |
        | 3000 | 3000  | 0         | desconto igual ao total                       |
        | 5000 | 3000  | 0         | desconto maior que o total — nunca −2000      |

    Cenário: [CT-27] o percentual máximo zera o total   @premissa P-05
      Dado um cupom percentual de 100% válido e com uso disponível
      Quando o sistema aplica esse cupom sobre um total de 12990 centavos
      Então o total resultante é 0 centavos
```

> **Nota de derivação — CT-25, linha `33 / 101`**: é uma linha de **controle**, e está declarada
> como tal. Ela não discrimina truncamento de arredondamento (33,33 arredonda para 33); serve para
> que a leitura da tabela não sugira que qualquer valor com resto discrimina.
>
> **Nota de derivação — CT-26, linha `3000 / 3000`**: a borda exata do limite em zero. Sem ela, uma
> implementação com `max(1, …)` ou com a comparação invertida sobreviveria à linha `5000 / 3000`.
>
> **Por que o `Então` afirma o total e não o desconto**: uma implementação que devolve o **desconto**
> no lugar do total com desconto é um erro plausível de retorno, e um oráculo sobre o desconto não o
> distingue.
>
> **Nenhum exemplo usa ponto flutuante.** Todos os valores são inteiros em centavos, conforme P-05.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o percentual é calculado em ponto flutuante e depois convertido a inteiro | CT-25 (linha `29 / 10000`) |
| M2 | a fração é arredondada em vez de truncada | CT-25 (linhas `10 / 9999` e `5 / 50`) |
| M3 | o valor do cupom fixo é tratado como percentual (ou o percentual como centavos) | CT-26 (linha `1000 / 12990`) |
| M4 | o resultado negativo é devolvido quando o desconto excede o total | CT-26 (linha `5000 / 3000`) |
| M5 | o método devolve o desconto em vez do total com desconto | CT-25 e CT-26 (todas as linhas) |
| M6 | o teto de 100% não zera (multiplicação ou divisão trocadas) | CT-27 |

---

## Regra R09 — Cada aplicação bem-sucedida consome exatamente um uso, e o limite nunca é ultrapassado

> `RQ-11`, `RQ-13` · área A1, perfil **completo**
> Técnica: **rastreio de efeito** (aconteceu / não aconteceu quando não devia / uma só vez) +
> **concorrência**

```gherkin
# language: pt
  Regra: a aplicação bem-sucedida consome um uso, e nem duas aplicações simultâneas passam do limite

    Cenário: [CT-28] a aplicação bem-sucedida consome exatamente um uso
      Dado um cupom "PROMO10" válido, com limite de 40 usos e 7 usos já feitos
      Quando o sistema aplica "PROMO10" sobre um total de 10000 centavos
      Então o contador de usos de "PROMO10" passa a ser 8

    Esquema do Cenário: [CT-29] a aplicação recusada não consome uso, em cada tipo de cupom
      Dado um cupom "PROMO10" do tipo <tipo>, vencido, com limite de 40 usos e 7 usos já feitos
      Quando o sistema tenta aplicar "PROMO10" sobre um total de 10000 centavos
      Então o contador de usos de "PROMO10" continua 7
      E o total continua 10000 centavos

      Exemplos:
        | tipo       | # partição do discriminador |
        | percentual | ramo de porcentagem         |
        | fixo       | ramo de valor fixo          |

    Cenário: [CT-30] duas aplicações concorrentes sobre o último uso consomem um só
      Dado um cupom "PROMO10" válido, com limite de 3 usos e 2 usos já feitos
      E duas execuções que leram esse cupom antes de qualquer consumo
      Quando as duas tentam aplicar "PROMO10" sobre um total de 10000 centavos
      Então o contador de usos de "PROMO10" é 3, e não 4
      E exatamente uma das duas aplicações resultou em total 9000 centavos, e a outra foi recusada

    Esquema do Cenário: [CT-31] o consumo acontece em cada tipo de cupom
      Dado um cupom válido do tipo <tipo>, com limite de 40 usos e 7 usos já feitos
      Quando o sistema aplica esse cupom sobre um total de 10000 centavos
      Então o contador de usos desse cupom passa a ser 8
      E existe exatamente 1 registro de uso desse cupom

      Exemplos:
        | tipo       | # partição do discriminador |
        | percentual | ramo de porcentagem         |
        | fixo       | ramo de valor fixo          |
```

> **Nota de derivação — CT-30, e o arnês que o torna expressável**: concorrência real não existe num
> processo único com SQLite `:memory:`. O que **é** expressável, e é o que distingue as duas
> implementações, é a **leitura obsoleta**: carregar duas referências ao mesmo cupom **antes** de
> qualquer consumo, e só então aplicar as duas. Uma implementação que lê o contador em memória,
> compara com o limite e grava `contador + 1` deixa as duas passarem e o contador vai a 4; uma que
> resolve a comparação **dentro da própria escrita** deixa a segunda sem linha afetada e a recusa.
> O `Então` afirma o contador **persistido** e afirma que **uma** das duas foi recusada — sem a
> segunda metade, uma implementação que recusa as duas também passaria.
>
> **Nota de derivação — CT-31**: mesma razão de CT-23, do lado do sucesso. Sem ele, um consumo
> escrito só no ramo percentual deixa o cupom de valor fixo **ilimitado** — resgatável para sempre,
> sem nada ficar vermelho.
>
> **Sobre idempotência**: a quarta direção do rastreio de efeito (*"aconteceu uma só vez"* para a
> **mesma** requisição repetida) é **inexpressável** nesta entrega — ver a pergunta **Q-06**. Ela
> está registrada como lacuna, não como item coberto.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o contador não é incrementado no sucesso | CT-28 |
| M2 | o contador é incrementado antes de validar: a recusa consome | CT-29 |
| M3 | ler o contador, comparar com o limite e gravar `contador + 1` (janela entre leitura e escrita) | CT-30 |
| M4 | o incremento é de 2, ou acontece duas vezes por aplicação | CT-28 |
| M5 | o consumo existe só no ramo percentual | CT-31 |
| M6 | as duas execuções concorrentes são recusadas (barreira boa demais) | CT-30 (`Então` exige que uma tenha sido aceita) |

---

## Regra R10 — Toda aplicação bem-sucedida registra quem aplicou e quando

> `RQ-15` · área A4, perfil **padrão** (teto 3, **estourado para 4** — a quarta direção é a
> atomicidade, justificada abaixo)
> Técnica: **rastreio de efeito** — primeiro *o quê* (o registro nomeado pelo card: quem e quando),
> depois as direções

O card pede o registro *"pra gente conseguir auditar depois"*. As duas grandezas que ele nomeia são
**quem** e **quando**; um registro sem uma delas não atende RQ-15.

```gherkin
# language: pt
  Regra: cada aplicação bem-sucedida deixa um registro com quem aplicou e quando

    Cenário: [CT-32] a aplicação bem-sucedida registra o autor, o cupom e o instante
      Dado os cupons "PROMO10" e "BEMVINDO", ambos criados em 2026-08-10 08:00, válidos e sem uso
      E as compradoras Marina e Bruno autenticadas, e o instante corrente 2026-08-15 10:00:00
      Quando o sistema aplica "BEMVINDO" por Marina sobre um total de 10000 centavos
      Então existe exatamente 1 registro de uso, e ele aponta para "BEMVINDO"
      E o autor desse registro é Marina, e não Bruno
      E o instante desse registro é 2026-08-15 10:00:00, e não 2026-08-10 08:00
      E o contador de usos de "PROMO10" continua 0

    Cenário: [CT-33] a aplicação recusada não registra nada
      Dado um cupom "PROMO10" esgotado
      E a compradora Marina autenticada
      Quando o sistema tenta aplicar "PROMO10" por Marina sobre um total de 10000 centavos
      Então não existe nenhum registro de uso de "PROMO10"

    Cenário: [CT-34] duas aplicações bem-sucedidas deixam dois registros, um por aplicação
      Dado um cupom "PROMO10" válido, com limite de 40 usos
      E as compradoras Marina e Bruno autenticadas
      Quando o sistema aplica "PROMO10" por Marina em 2026-08-15 10:00:00 e por Bruno em
        2026-08-15 11:00:00
      Então existem exatamente 2 registros de uso de "PROMO10"
      E o registro de 2026-08-15 10:00:00 tem Marina como autora
      E o registro de 2026-08-15 11:00:00 tem Bruno como autor

    Cenário: [CT-35] a falha ao registrar não consome uso nem concede desconto
      Dado um cupom "PROMO10" válido, com limite de 40 usos e 7 usos já feitos
      E o armazenamento do registro de uso indisponível
      Quando o sistema tenta aplicar "PROMO10" sobre um total de 10000 centavos
      Então o contador de usos de "PROMO10" continua 7
      E não existe nenhum registro de uso de "PROMO10"
      E o chamador observa a falha e o total dele continua 10000 centavos

    Cenário: [CT-45] excluir o cupom não apaga a trilha de quem já o usou   @premissa Q-07
      Dado um cupom "PROMO10" com dois usos registrados, por Marina e por Bruno
      Quando a administradora exclui esse cupom
      Então os dois registros de uso continuam existindo
      E um deles tem Marina como autora e o outro tem Bruno
      E os dois ainda identificam o código "PROMO10"
```

> **Nota de derivação — CT-32**: **três** pessoas distintas existem no conjunto (Marina, Bruno e a
> administradora), e o `Então` nomeia **qual** delas ficou no registro. "Existe um registro de uso"
> sem o autor passa com uma implementação que grava sempre o mesmo usuário — ou o usuário errado.
>
> **Nota de derivação — CT-34**: é a direção *"uma só vez por aplicação"*. Uma implementação que
> atualiza o mesmo registro em vez de criar um novo mantém o contador certo e a trilha com **uma**
> linha: quem auditar vai ver o último uso e concluir que houve um só.
>
> **Nota de derivação — CT-35, e por que ele não é um falso ✅**: a falha é forçada **depois** do
> ponto em que o uso seria consumido — o armazenamento do registro é derrubado dentro do próprio
> cenário (a tabela de registros é removida antes da chamada), de modo que a gravação falhe com o
> consumo já tentado. Afirmar "nenhum registro foi gravado" num caminho de **pré-validação** (CT-33)
> não prova atomicidade nenhuma: ali nada seria gravado de qualquer forma. Os dois cenários existem
> porque provam coisas diferentes.
>
> **Justificativa do estouro do teto**: o perfil `padrão` dá 3 cenários por regra e o rastreio de
> efeito já consome os 3 nas direções básicas. A quarta (atomicidade) entra porque, sem ela,
> *"o uso foi consumido e a trilha sumiu"* é indistinguível de *"os dois aconteceram"* — e é o
> cenário em que o dado de auditoria some **sem deixar vestígio**, que é o motivo pelo qual RQ-15
> existe.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | o registro de uso não é gravado (a chamada some) | CT-32 |
| M2 | o registro é gravado sem o autor, ou sempre com o mesmo autor | CT-32, CT-34 |
| M3 | o registro é gravado também nas recusas | CT-33 |
| M4 | o registro é atualizado em vez de criado: uma linha por cupom, não por aplicação | CT-34 |
| M5 | o registro é gravado fora da transação do consumo | CT-35 |
| M6 | o registro é gravado só no ramo percentual | CT-31 (`Então` afirma 1 registro em cada tipo) |
| M7 | a falha ao registrar é **engolida** e o desconto é devolvido assim mesmo | CT-35 (terceira ponta) — *revisão adversarial, L4 / 2ª rodada L08* |
| M8 | o registro carimba o instante de **criação do cupom** em vez do da aplicação | CT-32 — *revisão adversarial (2ª rodada), L07* |
| M9 | o registro aponta para o cupom errado (resolvido por "o primeiro", ou com vínculo nulo) | CT-32, CT-47 — *revisão adversarial (2ª rodada), L15* |
| M10 | a exclusão do cupom **apaga em cascata** a trilha de quem o usou | CT-45 — *revisão adversarial (2ª rodada), L03* |

> **Nota de derivação — CT-32** *(achados L07 e L15 da 2ª rodada)*: o cenário anterior congelava o
> tempo e **criava o cupom dentro do instante congelado** — toda gravação do cenário valia o mesmo
> número, e um registro que carimbasse o `created_at` do cupom passava. Agora há **dois instantes
> distintos**, e o `Então` diz qual dos dois é o certo. Pelo mesmo motivo há **dois cupons** e
> **duas pessoas**: com um cupom só no banco, uma implementação que resolve o alvo do registro por
> "o primeiro que achar" fica verde; com uma pessoa só, o autor não é falsificável. As três
> coordenadas do registro — qual cupom, qual autor, qual instante — são todas nomeadas.
>
> **Nota de derivação — CT-45, e a pergunta que ele abre** *(achado L03 da 2ª rodada)*: nenhum
> cenário exercitava exclusão **com histórico de uso**. Um vínculo em cascata — o default que se
> escreve sem pensar — faz a trilha desaparecer junto com o cupom, e RQ-15 existe exatamente para o
> *"depois"*. **O requisito não determina o desfecho**: preservar a trilha e recusar a exclusão são
> os dois defensáveis. O cenário adota a preservação como premissa e abre a pergunta **Q-07**; o
> que não é defensável é o conjunto não ter nenhum dos dois.

---

## Regra R11 — O cadastro é operável pela tela do painel

> `RQ-01` · área A5, perfil **padrão** · premissa **P-09** do `00-requisito.md` (painel de negócio)
> Técnica: **gate de tela de escrita** — *uma tela aberta não é uma tela que grava*
> (`.ai/rules/testes.md`)

A tabela `## Superfície de UI` do PRD tem **duas rotas de escrita**: `create` e `edit`. O gate exige
um cenário de gravação por componente para **cada uma**.

| Rota da Superfície de UI | Gravação coberta por |
|---|---|
| `/app/{tenant}/cupons/create` | **CT-01** (e CT-15, linha `criar`) |
| `/app/{tenant}/cupons/{record}/edit` | **CT-36** (e CT-11, CT-15 linha `editar`) |
| `/app/{tenant}/cupons` (listagem) | CT-37, CT-17, CT-18 |

```gherkin
# language: pt
Funcionalidade: Cadastro de cupons pelo painel

  Regra: a tela do painel cria, edita e lista o cupom

    Cenário: [CT-36] a tela de edição grava a alteração no cupom existente
      Dado um cupom "PROMO10" com limite de 40 usos na organização Acme
      E a administradora na tela de edição desse cupom
      Quando ela altera o limite de usos para 60 e salva
      Então a organização Acme continua com exatamente 1 cupom
      E o limite de usos de "PROMO10" é 60

    Cenário: [CT-37] a listagem exibe o cupom cadastrado
      Dado dois cupons "PROMO10" e "BEMVINDO" ativos na organização Acme
      E a administradora autenticada nessa organização
      Quando ela abre a lista de cupons
      Então ela vê "PROMO10" e "BEMVINDO" na lista
```

> **Nota de derivação — CT-36**: o `Então` afirma **um** cupom, não só o valor novo. A edição que
> cria um registro em vez de atualizar deixaria o limite 60 gravado em algum lugar e passaria num
> oráculo mais fraco.
>
> **Nota de derivação — CT-37**: é a metade *"abre"* do par. A metade *"grava"* é CT-01 e CT-36 —
> nenhuma das duas foi coberta apenas por visita.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | a tela de edição abre e o salvamento quebra | CT-36 |
| M2 | a edição cria um registro novo em vez de atualizar o existente | CT-36 (`Então` afirma 1 cupom) |
| M3 | a listagem não exibe os registros da organização corrente | CT-37 |

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| **Fixture de uma instância só** *(linha nova — vinda da 2ª rodada da revisão adversarial, e candidata a rule do projeto)*: todo cenário de identidade, escopo ou efeito precisa de **duas** instâncias indistinguíveis pela chave de busca | CT-40 (dois cupons na aplicação), CT-47 (código homônimo em duas organizações), CT-41 (duas organizações na listagem), CT-32 (dois cupons e duas pessoas na trilha), CT-44 (o segundo tipo na gravação), CT-34 (dois instantes) |
| **IDOR / autorização horizontal** | CT-16 (editar **e** excluir o cupom de outra organização), CT-24 e CT-47 (aplicação do código de outra organização) |
| **Autorização exercida na ação**, não só consultada | CT-14 e CT-16 — o `Quando` **dispara/submete** a operação; nenhum cenário afirma `can()` |
| **Verbo irmão**: cada verbo do card falsificado por si | CT-14 (três linhas), CT-15 (três linhas), CT-16 (duas linhas), CT-42 (duas por persona) |
| **Matriz exaustiva no eixo do papel** ("só admin" é afirmação sobre todos os outros) | CT-42 — amostragem residual declarada na nota da matriz de R05 |
| **Leitura de registro isolado ≠ listagem** | CT-48 |
| **Durabilidade do efeito registrado** (sobrevive ao ciclo de vida do pai?) | CT-45 — `@premissa Q-07` |
| **Identidade do alvo do efeito** (o registro aponta para o recurso certo?) | CT-32, CT-47 |
| **Metacaractere do mecanismo de busca** no domínio do identificador | CT-20 (linhas `%`, `_`, `PROMO_0`, `PROM%`) |
| **Granularidade da tradução entrada → armazenamento** | CT-49 — `@premissa 00/pergunta-5` |
| **Idempotência ancorada no agregado** | **lacuna declarada** — o agregado (`Pedido`) está fora de escopo por P-01. Tentado: ancorar no contador do cupom (prova contabilidade, não idempotência) e no valor devolvido por duas chamadas (tautológico com motor puro). Ver **Q-06** |
| **Concorrência** | CT-30 — arnês de leitura obsoleta (duas referências carregadas antes do consumo), descrito na nota de derivação |
| **Fronteira no ponto de entrada (gravação)** | CT-05 (valor), CT-07 e CT-49 (validade), CT-08 (limite) |
| **Domínio condicionado** (`tipo` × `valor`) | CT-05 na criação, CT-06 e CT-43 na edição, **CT-44 na unidade gravada** |
| **Criação ≠ edição ≠ uso** | criação: CT-01, CT-05, CT-07, CT-08, CT-39, CT-44, CT-49 · edição: CT-06, CT-08 (linhas de edição), CT-09, CT-11, **CT-38** (unicidade), **CT-43** (valor), **CT-46** (limite), CT-36 · uso: CT-13, CT-21, CT-22, CT-39, CT-44 |
| **Unicidade nos dois pontos de escrita** | contra o próprio registro: CT-11 · contra **outro** registro na edição: **CT-38** |
| **Estado × operação de escrita** (o inativo ainda funciona?) | CT-21 (vencido não aplica), CT-22 (esgotado não aplica), CT-23 (nos dois tipos), CT-46 (limite reduzido esgota e recusa). O cupom **excluído** não tem operação a exercer: a exclusão é física (CT-15, linha `excluir`), e o efeito dela sobre a trilha é CT-45 |
| **Ausente ≠ null ≠ vazio** | CT-20 (linhas `""`, `ausente`, `"   "`) |
| **Partição do discriminador × cada efeito** | gravação: **CT-44** · recusa: CT-23, CT-29 · consumo e registro: CT-31 · cálculo: CT-25, CT-26. *(A célula da **gravação** estava vazia até a 2ª rodada da revisão — era a lacuna mais cara do conjunto.)* |
| **Paginação** | **não se aplica**: o card não descreve listagem paginada e não há volume declarado. A listagem tem cenários de conteúdo (CT-17, CT-18, CT-37) e nenhum de página. Se um teto de página for definido, entra uma regra nova |
| **Ordenação por coluna** | **não se aplica**: nenhuma cláusula do `00` fala em ordem. Ordem padrão é escolha do PRD (`defaultSort`), recusada como oráculo |
| **Timezone / DST / virada de dia** | **lacuna declarada**. O app roda em `UTC` (`config/app.php:68`) e o banco de teste é SQLite `:memory:` — não há divergência app × banco a explorar. Tentado: (a) `config(['app.timezone' => 'America/Sao_Paulo'])` dentro do cenário — não altera `date_default_timezone_get()`, já fixado no boot, então a comparação não diverge; (b) `travelTo()` sobre a virada da meia-noite — **funciona e virou CT-19**, mas prova estado derivado, não fuso; (c) gravar `expira_em` com deslocamento explícito — mediria o driver, não a regra. **A parte observável está coberta** (CT-07, CT-19, CT-21); o que fica descoberto é a divergência entre o fuso do app e o do operador, que só aparece quando o app deixar de ser `UTC` |
| **Unicode / limite de tamanho do código** | **lacuna declarada**: o `00` não dá tamanho máximo ao código (o limite de 40 é do PRD, recusado como oráculo). CT-10 cobre caixa e espaço, que são o que o card implica ao dizer que o código não se repete. Acento e emoji ficam sem cenário até haver regra |
| **Unicidade + exclusão lógica** | **não se aplica**: não há exclusão lógica nesta feature. O card diz "excluir", e P-03 recusou a coluna de ligar/desligar |
| **CRUD combinado**: excluir duas vezes, editar sem alterar nada | editar sem alterar: CT-11 · excluir inexistente: CT-16 (registro não encontrado) · **excluir duas vezes: lacuna declarada** — a segunda exclusão recai no mesmo caminho de CT-16 e não distingue nenhum mutante previsto |
| **Mass assignment** | CT-04 (o contador de usos enviado no formulário é ignorado) |
| **Upload** | **não se aplica**: a feature não recebe arquivo |
| **Precisão monetária** | CT-25 (linha `29 / 10000` distingue inteiro de ponto flutuante; linhas `10 / 9999` e `5 / 50` distinguem truncar de arredondar), CT-26 (borda do limite em zero), CT-27. **Nenhum exemplo do conjunto usa ponto flutuante** |

---

## Alocação de Camada e Poda

### Camada por cenário

A camada sai do que o `Então` afirma, não da estrutura provável do código. Como `tests/Unit` **não
tem o `TestCase` da aplicação** (ver o cabeçalho), a camada mais barata disponível é `Feature`.

| O que o `Então` afirma | Camada | Cenários |
|---|---|---|
| valor calculado, contador persistido, registro de uso, isolamento por organização | `Feature` | CT-13, CT-20…CT-35 |
| campo do formulário recusado, gravação pelo formulário, conteúdo da tabela | componente Livewire/Filament | CT-01…CT-12, CT-14…CT-19, CT-36, CT-37 |
| a tela funciona com JavaScript executando | Browser | CT-B01, CT-B02 (ver `05-casos-de-teste-browser.md`) |

### Distribuição por arquivo

| Arquivo | Suíte | Cenários |
|---|---|---|
| `tests/Kit/CupomTest.php` | `Kit` — single-tenant, grupo `kit` | CT-01…CT-11, CT-13, CT-20…CT-23, CT-25…CT-40, CT-43, CT-44, CT-45, CT-49, e a variante single-tenant de CT-14/CT-15 (com `master_global` e `panel_user`) |
| `tests/Tenancy/CupomTenancyTest.php` | `Tenancy` — multi-tenant, grupo `kit` | CT-12, CT-14…CT-19, CT-24, CT-41, CT-42, CT-46, CT-47, CT-48 |
| `tests/BrowserTenancy/CupomTest.php` | `Browser` — em série | CT-B01, CT-B02 |

> **Por que CT-14 a CT-19 vivem na suíte de tenancy**: o papel `admin_organizacao` só é criado com a
> tenancy ligada (`PapeisSeeder.php:70-73`). Rodá-los em single-tenant mediria uma matriz de papéis
> que não é a de produção. A contrapartida — o modo default do kit — é a variante single-tenant de
> CT-14/CT-15 declarada acima.

### Teto por perfil — o que estourou, e por quê

O passo 7 dá teto de 5 cenários por regra no perfil `completo` e 3 no `padrão`. Um
`Esquema do Cenário` conta como **1**, não como N linhas.

| Regra | Perfil | Teto | Cenários | Estouro justificado por |
|---|---|---|---|---|
| R01 | completo | 5 | 4 | — |
| R02 | completo | 5 | 4 | — |
| R03 | completo | 5 | 4 | — |
| R04 | completo | 5 | **6** | o gate vence o teto: CT-38 e CT-39 são os únicos matadores de R04-M5 e R04-M7, ambos trazidos pela revisão |
| R05 | padrão | 3 | **4** | CT-42 é o único matador de R05-M8, e RQ-07 é a única cláusula com a palavra *"só"* |
| R06 | padrão | 3 | **6** | a partição do estado tem 5 células e três superfícies de leitura distintas (lista, registro isolado, motor). **É sintoma de regra que deveria ser duas** — registrado junto com a dívida de R10 |
| R07 | completo | 5 | **7** | CT-40 e CT-47 são os únicos matadores de R07-M8 e R07-M9; ambos vieram da revisão |
| R08 | completo | 5 | 3 | — |
| R09 | completo | 5 | 4 | — |
| R10 | padrão | 3 | **5** | rastreio de efeito consome o teto inteiro nas 4 direções; CT-45 acrescenta a durabilidade. **Dívida declarada: deveria ser duas regras** |
| R11 | padrão | 3 | 2 (+1 CT-B) | — |

**Cinco das seis regras que estouraram o teto o fizeram por achado da revisão adversarial**, não por
derivação frouxa. É o comportamento que a skill prescreve — *mutante vivo é pior que cenário a mais*
—, e é também o sinal de que R06 e R10 estão modeladas grossas demais.

### Cogitado e cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| aplicar sobre um total de 0 centavos | o limite em zero já é provado por CT-26 (linha `5000 / 3000`), e o total zero não distingue nenhum mutante previsto a mais |
| o desconto gravado no registro de uso é igual ao aplicado ao total | as colunas de valor do registro são do PRD, não do card (RQ-15 pede **quem** e **quando**) — seria teste do plano |
| excluir o mesmo cupom duas vezes | recai no mesmo caminho de CT-16; não distingue mutante previsto. Registrado como lacuna no checklist |
| a lista ordena por validade | ordem é escolha do PRD; nenhuma cláusula do `00` a determina |
| o log da recusa contém o motivo | o card não pede log; afirmar formato de mensagem é teste do plano |
| o cupom excluído deixa de ser aplicável | a exclusão é física; o cupom deixa de existir e CT-20 (código inexistente) já cobre o efeito observável |
| um cenário por variação de caixa em cenários separados | `Esquema do Cenário` de CT-10 expressa a mesma partição em 1 cenário, conforme o passo 7 |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|---|---|---|---|---|---|---|
| CT-01 | cadastro completo grava os cinco atributos, contador em 0 | R01 | EP | Livewire | `tests/Kit/CupomTest.php` | R01-M4, M5 |
| CT-02 | atributo ausente recusa a gravação (5 linhas) | R01 | EP inválidas isoladas | Livewire | `tests/Kit/CupomTest.php` | R01-M2 |
| CT-03 | tipo fora dos dois admitidos é recusado | R01 | partição exaustiva | Livewire | `tests/Kit/CupomTest.php` | R01-M3 |
| CT-04 | contador de usos não é dado de entrada | R01 | mass assignment | Livewire | `tests/Kit/CupomTest.php` | R01-M1 |
| CT-05 | fronteira de `valor` por `tipo` (7 linhas) | R02 | tabela de decisão + BVA | Livewire | `tests/Kit/CupomTest.php` | R02-M1, M2, M3, M5 |
| CT-06 | trocar o tipo na edição reavalia o domínio | R02 | BVA na edição | Livewire | `tests/Kit/CupomTest.php` | R02-M4 |
| CT-07 | validade gravada tem de estar no futuro | R03 | BVA 3-valores | Livewire | `tests/Kit/CupomTest.php` | R03-M1, M3, M6 |
| CT-08 | piso do limite de usos, na criação e na edição | R03 | BVA em 2 pontos | Livewire | `tests/Kit/CupomTest.php` | R03-M4, M5 |
| CT-09 | edição não empurra a validade para o passado | R03 | BVA na edição | Livewire | `tests/Kit/CupomTest.php` | R03-M2 |
| CT-10 | caixa e espaço não criam códigos diferentes | R04 | normalização | Livewire | `tests/Kit/CupomTest.php` | R04-M1, M2 |
| CT-11 | salvar sem alterar o código não acusa colisão | R04 | unicidade contra si | Livewire | `tests/Kit/CupomTest.php` | R04-M4, M6 |
| CT-12 | mesmo código em outra organização é aceito | R04 | escopo de unicidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R04-M3 |
| CT-13 | código digitado em qualquer forma encontra o cupom | R04 | normalização no uso | Feature | `tests/Kit/CupomTest.php` | R04-M5 |
| CT-14 | usuário comum barrado em criar, editar e excluir | R05 | matriz papel×ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R05-M1, M2, M3, M4 |
| CT-15 | administradora executa os três verbos | R05 | célula válida | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R05-M5 |
| CT-16 | administradora de outra organização não alcança | R05 | IDOR | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R05-M6 |
| CT-17 | lista do usuário comum reflete o estado derivado | R06 | estado × operação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R06-M2, M3, M4 |
| CT-18 | administradora vê também os não-ativos | R06 | célula válida | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R06-M1 |
| CT-19 | cupom que vence entre consultas some da lista | R06 | tempo | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R06-M5 |
| CT-20 | código inexistente, vazio, nulo ou em branco | R07 | EP inválidas isoladas | Feature | `tests/Kit/CupomTest.php` | R07-M1 |
| CT-21 | validade conferida contra o instante | R07 | BVA 3-valores (1 s) | Feature | `tests/Kit/CupomTest.php` | R07-M2, M4 |
| CT-22 | limite conferido antes de consumir | R07 | BVA 3-valores | Feature | `tests/Kit/CupomTest.php` | R07-M3, M4 |
| CT-23 | as recusas valem no cupom de valor fixo | R07 | discriminador × efeito | Feature | `tests/Kit/CupomTest.php` | R07-M5 |
| CT-24 | código de outra organização não é encontrado | R07 | IDOR | Feature | `tests/Tenancy/CupomTenancyTest.php` | R07-M6 |
| CT-25 | percentual em inteiro, truncado | R08 | valores discriminantes | Feature | `tests/Kit/CupomTest.php` | R08-M1, M2, M5 |
| CT-26 | valor fixo subtraído, nunca negativo | R08 | BVA | Feature | `tests/Kit/CupomTest.php` | R08-M3, M4, M5 |
| CT-27 | 100% zera o total | R08 | borda superior | Feature | `tests/Kit/CupomTest.php` | R08-M6 |
| CT-28 | consome exatamente um uso | R09 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | R09-M1, M4 |
| CT-29 | recusa não consome uso | R09 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | R09-M2 |
| CT-30 | duas aplicações concorrentes consomem um só | R09 | concorrência | Feature | `tests/Kit/CupomTest.php` | R09-M3, M6 |
| CT-31 | consumo e registro em cada tipo | R09/R10 | discriminador × efeito | Feature | `tests/Kit/CupomTest.php` | R09-M5, R10-M6 |
| CT-32 | registra autor e instante | R10 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | R10-M1, M2 |
| CT-33 | recusa não registra nada | R10 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | R10-M3 |
| CT-34 | duas aplicações, dois registros | R10 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | R10-M2, M4 |
| CT-35 | registro indisponível não deixa o uso ser consumido | R10 | atomicidade | Feature | `tests/Kit/CupomTest.php` | R10-M5 |
| CT-36 | a tela de edição grava a alteração | R11 | gate de tela de escrita | Livewire | `tests/Kit/CupomTest.php` | R11-M1, M2 |
| CT-37 | a listagem exibe o cupom cadastrado | R11 | gate do par | Livewire | `tests/Kit/CupomTest.php` | R11-M3 |
| **CT-38** | renomear um cupom para o código de outro é recusado | R04 | unicidade na edição | Livewire | `tests/Kit/CupomTest.php` | R04-M7 |
| **CT-39** | o código entra normalizado pela porta de escrita e é aplicável | R04 | normalização na escrita | Livewire+Feature | `tests/Kit/CupomTest.php` | R04-M5, M6 |
| **CT-40** | a aplicação encontra o cupom pedido, e não outro | R07 | oráculo de identidade | Feature | `tests/Kit/CupomTest.php` | R07-M8 |
| **CT-41** | a lista nunca contém cupom de outra organização | R06 | escopo em coleção | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R06-M6, M7 |
| **CT-42** | nenhum outro papel escreve cupom | R05 | matriz exaustiva no papel | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R05-M8 |
| **CT-43** | o valor é reavaliado quando só ele muda na edição | R02 | BVA na edição | Livewire | `tests/Kit/CupomTest.php` | R02-M7 |
| **CT-44** | valor fixo cadastrado pela tela é gravado em centavos e desconta o mesmo | R02/R08 | discriminador na gravação | Livewire+Feature | `tests/Kit/CupomTest.php` | R02-M8 |
| **CT-45** | excluir o cupom não apaga a trilha | R10 | durabilidade do efeito | Feature | `tests/Kit/CupomTest.php` | R10-M10 |
| **CT-46** | reduzir o limite abaixo dos usos esgota o cupom | R06/R03 | 5ª célula do estado | Livewire+Feature | `tests/Tenancy/CupomTenancyTest.php` | R06-M8 |
| **CT-47** | códigos homônimos em organizações diferentes não se confundem | R07/R09/R10 | fixture colidente | Feature | `tests/Tenancy/CupomTenancyTest.php` | R07-M9, R10-M9 |
| **CT-48** | o usuário comum não alcança cupom não-ativo pelo endereço direto | R06 | superfície de leitura isolada | Livewire | `tests/Tenancy/CupomTenancyTest.php` | R06-M9 |
| **CT-49** | data sem hora guarda o fim do dia | R03 | granularidade de entrada | Livewire+Feature | `tests/Kit/CupomTest.php` | R03-M8 |

**Mutantes sem matador**: 2, ambos declarados —
idempotência ancorada no agregado (Q-06, escopo) e divergência de fuso app × operador (app em
`UTC`, sem divergência explorável no arnês atual).

> **Cenários que atravessam duas camadas** (`Livewire+Feature`): CT-39, CT-44, CT-46 e CT-49
> gravam **pela tela** e depois afirmam sobre o **motor**. É deliberado, e é o que a 2ª rodada da
> revisão adversarial mostrou faltar: separá-los em dois cenários — um que grava, outro que aplica —
> devolve exatamente a lacuna, porque cada metade continuaria usando a fixture canônica da outra.
> A costura **é** o objeto do teste.

---

## API de Teste — o que escrever e o que **não** escrever

Confirmado nos testes existentes do projeto, não de memória.

| Escrever | Onde já é usado | Em vez de |
|---|---|---|
| `Livewire::test(CreateCupom::class)->fillForm([...])->call('create')->assertHasNoFormErrors()` | `tests/Kit/ConviteTest.php:117-118` | montar `POST` HTTP para uma rota de Filament |
| `->call('save')` na página de edição | `tests/Kit/PaginasInfraTest.php:98-101` | `->call('update')` |
| `->assertHasFormErrors(['valor'])` | `tests/Tenancy/AdminDaOrganizacaoTest.php:270` | `assertSessionHasErrors` |
| `->callAction(TestAction::make('delete')->table($cupom))` | `tests/Kit/ConviteTest.php:284-285` | `callTableAction` (`@deprecated` no Filament 5) |
| `->assertCanSeeTableRecords([...])` / `->assertCanNotSeeTableRecords([...])` | `tests/Tenancy/AdminDaOrganizacaoTest.php:133` | `assertSee` do HTML |
| `assertSchemaStateSet` | — | `assertFormSet` (`@deprecated`) |
| `assertActionExists` | `tests/Kit/ConviteEmMassaTest.php:342` | `assertTableActionExists` (`@deprecated`) |
| `noPainelDa($tenant)` antes de todo componente Livewire em tenancy | `tests/Pest.php:210` | `Filament::setTenant()` solto — sem `setPermissionsTeamId` o papel some |
| `usuarioComPapel($papel, $tenant)` / `usuarioCom($papel)` | `tests/Pest.php:188,255` | criar `User` e `assignRole` à mão (grava no contexto global e o papel fica invisível no `/app`) |
| helper novo em `tests/Pest.php`, nunca no arquivo de teste | `.ai/rules/testes.md` | helper local usado por dois arquivos → `Call to undefined function` em `--parallel` |

**Armadilhas que invalidariam estes CT**, verificadas contra a lista da skill:

- **`assertDatabaseHas` só com o código** passa com os outros quatro campos errados — por isso o
  `Então` de CT-01 nomeia os cinco.
- **`travel()` sem `travelBack()`** vaza para os cenários seguintes e produz flake em `--parallel`;
  CT-07, CT-09, CT-19, CT-21 e CT-32 usam closure ou `freezeTime()`.
- **`withoutExceptionHandling()` junto de asserção de acesso negado** transforma o 403 em exceção
  lançada e a asserção nunca roda — nenhum cenário de CT-14/CT-16 o usa.
- **`state(['usos' => …])` na factory** é descartado em silêncio (campo fora do `$fillable`); o
  state `esgotado()` precisa de `afterCreating` com escrita forçada.
- **`Event::fake()` antes das factories** desligaria o evento que gera o `uuid` do registro; nenhum
  cenário usa `Event::fake()`.

---

## Revisão Adversarial

Obrigatória (há duas áreas em perfil `completo`). Delegada a um **sub-agente que não derivou** os
cenários, recebendo apenas o `00-requisito.md` e os arquivos `04` e `05` — **sem** o PRD, sem o
código e sem o raciocínio de derivação. O contrato entregue foi o da skill, literal: *provar que
este conjunto deixa passar um defeito*, com proibição explícita de elogiar ou reescrever.

> **Nota de honestidade sobre o processo**: a primeira versão desta seção foi escrita pelo próprio
> agente que derivou, antes de a revisão rodar, listando os achados que ele já havia considerado ao
> derivar. Isso é **autorrevisão disfarçada de revisão** — o item 9 das Proibições. A seção foi
> apagada, o arquivo entregue ao revisor sem ela, e o que segue são os achados reais.

### Rodada 1 — 15 lacunas. Todas fechadas.

| # | Achado | O que virou |
|---|---|---|
| L1 | A unicidade do código não tinha ponto de **edição**. CT-11 é a célula *positiva* (salvar sem mudar o código); a célula negativa estava vazia — e a forma mais curta de fazer CT-11 passar é **desligar a regra na edição**, o que mata RQ-14 com o conjunto verde | **CT-38** |
| L2 | Nenhum código entrava no sistema em forma **não-canônica**: todas as variações de CT-10 e CT-13 são entradas de *consulta*, e o gravado nascia canônico por factory. A implementação espelho ("normaliza na leitura, grava como digitado") passava em tudo | **CT-39**, e o mutante R04-M5 reapontado |
| L3 | Nenhum cenário de aplicação tinha **mais de um cupom** no ambiente, nem código com metacaractere. Com um cupom só, "achou o certo" e "achou algum" são indistinguíveis; e um `LIKE` (a saída óbvia para "insensível a caixa") abre `%` como curinga | **CT-40** e 4 linhas novas em **CT-20** |
| L4 | CT-35 afirmava **uma coisa só** (o contador). Uma implementação que engole a falha e devolve o total com desconto passava — o pior desfecho da atomicidade, invisível ao cenário que existe para prová-la | 3ª ponta no `Então` de **CT-35** |
| L5 | Nenhuma listagem era montada com dado de **duas organizações**. O SFDIPOT declarava "dado de outro tenant" coberto por CT-17/CT-18, e não estava: um `getEloquentQuery()` que reconstrói a consulta e perde o escopo ficava verde | **CT-41** |
| L6 | CT-16 exercitava **um verbo**, e a matriz declarava três. A célula `excluir` estava vazia enquanto o checklist a lia como ✅ | **CT-16** virou `Esquema` com `editar` e `excluir` |
| L7 | A matriz papel × ação tinha **5 papéis e exercitava 2**. RQ-07 é a única cláusula com a palavra *"só"*, que é afirmação sobre **todos os outros** | **CT-42** (`infra`, `admin` da instalação, sem papel) |
| L8 | CT-05, CT-07 e CT-08 — 14 linhas de fronteira com oráculo de **uma palavra**. Nenhuma linha `recusado` afirmava o não-efeito; nenhuma `aceito` afirmava o valor gravado. O arquivo enunciava a doutrina em duas notas e não a aplicava às três tabelas | coluna `evidencia` nos três `Esquema` |
| L9 | O campo `valor` não tinha ponto de **edição isolado**: CT-06 troca o tipo e mantém o valor; nada mantinha o tipo e empurrava o valor para fora do domínio | **CT-43** |
| L10 | CT-23 (recusa no ramo fixo) afirmava total e ausência de registro, **não o contador**; e CT-29 usava só a fixture percentual. Um ramo `fixo` que incrementa antes de validar ficava verde | contador em **CT-23**; **CT-29** virou `Esquema` por tipo |
| L11 | CT-B02 **prometia** "erro visível na tela" e nada no cenário afirmava visibilidade — o mutante M3 declarava `assertNoJavaScriptErrors` como matador, promovendo assertion de apoio a oráculo único | passo 5 de **CT-B02** |
| L12 | CT-B01 não afirmava **tipo** nem **validade** — os dois únicos campos renderizados por widget JavaScript, e portanto os únicos que o CT-B existe para provar | `Então` e passo 6 de **CT-B01** |
| L13 | CT-15 tinha `Dado` incompleto: as linhas `editar` e `excluir` pressupunham um cupom que nada criava — o cenário não era executável como escrito | `Dado` e evidências de **CT-15** |
| L14 | CT-10 usava **contagem sem identificação**: "continua com 1 cupom" não distingue "recusou" de "substituiu" | `Então` de identidade em **CT-10** |
| L15 | CT-19 tinha ação e asserção dentro do `Dado`. O cenário passava **por vacuidade**: um recorte que nunca devolvesse nada satisfazia o único `Então` escrito | duas leituras promovidas a passos em **CT-19** |

### Rodada 2 — executada, e **ainda trouxe achado estrutural**. 10 lacunas novas, todas fechadas.

A rodada 2 é obrigatória porque o fechamento criou cenário novo (CT-38 a CT-43), e cenário novo é
superfície nova. Ela foi rodada pelo mesmo revisor, **sobre a versão anterior ao fechamento** —
logo é uma segunda leitura independente, não uma conferência do que foi corrigido.

| # | Achado | O que virou |
|---|---|---|
| L01 | **O mais caro do conjunto.** CT-01 e CT-B01 eram os únicos cenários que afirmavam valor persistido *a partir da tela*, e ambos usavam tipo **percentual** — onde não há conversão de unidade. Todo cupom de valor fixo nascia por factory. A costura formulário → banco → motor no ramo `fixo` não tinha **nenhum** cenário: um cupom de "R$ 50,00" cadastrado pela tela concederia R$ 0,50 com tudo verde | **CT-44** |
| L03 | Nenhum cenário exercitava **exclusão com histórico de uso**. Um vínculo em cascata — o default que se escreve sem pensar — apaga a trilha junto com o cupom, e RQ-15 existe exatamente para o *"depois"* | **CT-45** + pergunta **Q-07** |
| L04 | A partição "exaustiva" do estado derivado tinha **4 células e faltava a quinta** (`usos > limite`). Ela é alcançável pela premissa **Q-05**, que não tinha cenário nenhum. Um `usos != limite` satisfaz as quatro originais e faz o cupom **reaparecer** na lista depois da redução do limite | **CT-46** + célula nova na tabela de R06 |
| L05 | CT-24 montava o cupom em **uma organização só** — fixture não colidente, com a qual "buscou na certa" e "achou o primeiro" são indistinguíveis. O consumo atômico **tem** de ser escrito no Query Builder, que **não aplica escopo global de organização** | **CT-47** |
| L07 | CT-32 congelava o tempo e **criava o cupom dentro do instante congelado**: toda gravação valia o mesmo número, e um registro que carimbasse o `created_at` do cupom passava | dois instantes distintos em **CT-32** |
| L08 | (confirma L4 por outro caminho) CT-35 não afirmava o que o **chamador** recebe | já fechado por L4 |
| L09 | (confirma L12) CT-B01 omitia `tipo` e `expira_em` | já fechado por L12 |
| L10 | CT-16 **abria** a edição em vez de **submetê-la** — o `Quando` contrariava a regra que a nota do CT-14 estabelece ("dispara a operação, não consulta a permissão") | `Quando` de **CT-16** passou a submeter |
| L13 | RQ-08 diz *"podem **apenas** listar"*. O conjunto cobria o "apenas" na **escrita** e o "ativos" na **listagem**, e deixava a terceira superfície de fora: ler **um** registro por endereço direto | **CT-48** |
| L14 | A quinta pergunta aberta do `00` fixa que a data sem hora vale `23:59:59` — premissa **do `00`**, portanto oráculo legítimo, e **sem nenhum cenário**. Um seletor só de data mata a campanha à meia-noite do dia que o operador digitou como último dia válido | **CT-49** |
| L15 | Nenhum cenário obrigava o registro de uso a apontar para o **cupom certo**: CT-32 a CT-35 tinham um cupom só. O autor estava bem coberto; o alvo do registro, não | dois cupons em **CT-32**, e **CT-47** |

### Escalação obrigatória: o teto de rodadas foi atingido com achado estrutural aberto

A skill fixa **teto de 2 rodadas** e manda escalar se a segunda ainda trouxer achado estrutural.
Trouxe — dez, dos quais seis são estruturais (L01, L03, L04, L05, L13, L14). **O conjunto não foi
re-revisado uma terceira vez**, e isso é declarado, não omitido. A leitura do que aconteceu:

1. **O padrão dos achados de segunda rodada é um só**: *fixture de uma instância*. Cupom de um tipo
   só na escrita, cupom de uma organização só na aplicação, um cupom só na trilha, um instante só no
   tempo congelado. Não são dez defeitos independentes de derivação — são **uma** lacuna de método,
   aplicada em quatro eixos. Está registrada como linha nova do checklist de taxonomia.
2. **Duas regras provavelmente deveriam ser três.** R10 (trilha) absorveu, além das quatro direções
   do rastreio de efeito, a **durabilidade** do registro (CT-45) e a sua **identidade** (CT-32) —
   seis cenários numa regra de perfil `padrão`. É sintoma de regra que virou duas: *"o uso é
   registrado"* e *"o registro sobrevive e identifica"*. Não foi desdobrada porque renumerar toda a
   rastreabilidade no fechamento da revisão trocaria um problema real por um cosmético; fica como
   **dívida declarada** para a próxima iteração da wiki.
3. **Um achado virou pergunta em vez de certeza** (Q-07): a colisão entre RQ-07 ("pode excluir") e
   RQ-15 ("auditar depois") não é arbitrada pelo card, e nenhum conjunto de teste pode decidi-la
   sozinho.

> **Mutantes trazidos pela revisão e que estouram o teto de 6 por regra**: R02-M6/M7/M8,
> R03-M7/M8, R04-M5/M7/M8, R05-M7/M8, R06-M6/M7/M8/M9, R07-M7/M8/M9, R10-M7/M8/M9/M10. Registrados
> com a origem, conforme a exceção do passo 6 — mutante trazido pela revisão adversarial é achado
> medido, não enchimento, e não conta para o teto.

---

## Fechamento do Ciclo (pós-implementação)

```bash
composer require pestphp/pest-plugin-mutate --dev     # hoje é só transitivo
vendor/bin/pest tests/Kit/CupomTest.php --mutate --path=app/Models
```

> **O que o mutation score não responde**: ele só muta código que **existe**. Se uma cláusula do
> card nunca virar código — se não houver comparação de limite para mutar —, nenhum mutante é
> gerado e o score não cai. Quem responde por omissão é a rastreabilidade `RQ` → regra → cenário
> deste arquivo, não o `--mutate`.

Cada mutante sobrevivente é traduzido de volta em lacuna de derivação:

| Mutante sobreviveu | Lacuna | O que escrever |
|---|---|---|
| `>` → `>=` na validade | BVA faltando | cenário na borda exata (já previsto: CT-21) |
| `<` → `<=` no limite | BVA faltando | CT-22, linha `borda` |
| chamada de gravação do registro removida | efeito colateral não verificado | CT-32 |
| retorno trocado por nulo | oráculo fraco | assertion sobre o **valor** do total |
