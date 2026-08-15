# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `wikis/specs/exp-a/cupons-de-desconto/00-requisito.md` · Plano: `…/01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> `app/Models/Cupom.php`, `app/Services/*`, `app/Enums/*`, a migration, a factory e as suítes
> existentes da feature **não foram lidos**. O `01-plano-acao.md` entrou apenas para paths, rotas,
> `## Superfície de UI` e stack; o que dele foi recusado como oráculo está em
> [`## Fronteira com o Plano`](#fronteira-com-o-plano).

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| **A1** — Cadastro (criação e edição: domínio, unicidade, normalização) | 3 | 3 | 9 | **completo** |
| **A2** — Cálculo do desconto (tipo × valor, truncamento, piso zero) | 2 | 3 | 6 | **padrão** |
| **A3** — Aplicação (existência, validade, limite, consumo, trilha) | 3 | 3 | 9 | **completo** |
| **A4** — Autorização e isolamento por organização | 2 | 3 | 6 | **padrão** |
| **A5** — Listagem e situação exibida | 1 | 2 | 2 | **mínimo** |

Justificativa dos fatores, para o perfil não ser opinião:

- **A1 = P3**: o domínio de `valor` é **condicionado** pelo `tipo`, a unicidade é **escopada** por
  organização e o código é **normalizado** — três condições acopladas na mesma gravação. **I3**:
  cupom mal cadastrado é dinheiro concedido errado.
- **A2 = P2**: código novo e isolado (aritmética inteira sobre dois ramos), mas com arredondamento.
  **I3**: dinheiro.
- **A3 = P3**: concorrência explícita (contador com limite). **I3**: dinheiro, irreversível.
- **A4 = P2**: integra com componentes existentes (spatie + Shield + `PapeisSeeder`). **I3**:
  autorização e dado de terceiro.
- **A5 = P1/I2**: leitura; cupom inativo listado é ruído e retrabalho manual, não perda.

### Técnicas escaladas acima do perfil da área

| Regra | Perfil da área | Técnica usada | Por quê |
|---|---|---|---|
| **R5** (percentual truncado) | A2 — padrão (BVA 2-valores) | **BVA 3-valores + exemplos discriminantes de representação** | BVA 2-valores e valor redondo não distinguem truncar de arredondar nem inteiro de `float`: `10% de 10.000` dá `1.000` nas três implementações. O perfil é orçamento de *quantidade*, não licença para técnica cega |
| **R12** (situação exibida) | A5 — mínimo (EP simples) | **EP exaustiva do enum de situação** | o rótulo é derivado de estado. Amostrar duas das quatro combinações permite exatamente o defeito que importa — a tela dizer "Ativo" num cupom esgotado |
| **R13** (estado × operação) | A3+A5 | herda o **maior** (completo) | regra atravessa duas áreas |

- Técnicas aplicadas: **EP**, **BVA 3-valores** (incremento por tipo: 1 no inteiro, 1 s no
  `timestamp`, 1 caractere na string), **tabela de decisão**, **tabela estado × operação**,
  **matriz papel × ação**, **rastreio de efeito**, **normalização**.
- **Regras: 13 · Cenários: 47 · Mutantes previstos: 79 · Sem matador: 3** (M28, M29, M41)
- CT-B: **2**, no `05-casos-de-teste-browser.md` (+3 mutantes previstos lá).

### Revisão adversarial — executada, e o que ela mudou

Delegada a um sub-agente que **não derivou** os cenários e recebeu apenas o `00-requisito.md`, o
`04` e o `05` — sem o PRD, sem o código e sem o raciocínio de quem derivou.

**22 achados. Nenhum ficou aberto:**

| Destino | Qtd. | Quais |
|---|---|---|
| **Cenário novo** | 9 | CT-40 (troca do discriminador na edição), CT-41 (segundo uso), CT-42 (domínio do limite), CT-43 (vínculo forjado), CT-44 (rótulo na fronteira de instante), CT-45 (administrador global), CT-46 (reentrada por limite), CT-47 (edição disparada), CT-48 (tela do excluído) |
| **Oráculo reescrito** | 9 | não-efeito nas recusas de CT-18/CT-19/CT-20; persistência afirmada em CT-13; CT-30 dispara em vez de conferir o botão; CT-35 e CT-34 separados por persona; CT-24, CT-37 e CT-46 com o segundo evento no `Quando`; CT-08 com a precondição das linhas de edição |
| **Exemplo trocado por um discriminante** | 6 | CT-22 e CT-25 (as duas partições convergiam no mesmo valor); CT-11 (placeholders → 40 caracteres acentuados); CT-34 (`futuro`/`passado` → instantes); CT-15 (linha redundante fora, piso percentual dentro); CT-17 e CT-26/CT-27 (partição `fixo` acrescentada) |
| **Cenário cortado** | 1 | CT-10 — matava o mesmo mutante que CT-09 e sustentava um falso ✅ no checklist |
| **Pergunta nova ao requisito** | 1 | **Q-09** — a linha `admin` de CT-28 contradiz um dos três argumentos com que o `00` defende a premissa P-02 |
| **Item de checklist corrigido** | 6 | idempotência, autorização exercida, célula válida por coluna, mass assignment, `date × datetime`, partição × efeito — todos eram ✅ com o defeito intacto |

**Mutantes que a revisão trouxe à tona: 15** (M65…M79). Os dois mais caros:

- **M67** — um cupom de **1000%** era gravável trocando o tipo de fixo para percentual sem mexer no
  valor, devolvendo um total **negativo**. Escapou porque a coluna `tipo` existia no `Exemplos:` de
  CT-05 e **nunca mudava de linha para linha**.
- **M72** — a trilha de RQ-15 podia registrar só o **primeiro** uso de cada comprador, porque
  **nenhum cenário do conjunto aplicava o mesmo cupom duas vezes com sucesso**: todo contador maior
  que zero chegava por fixture, nunca pela operação.

Uma segunda rodada **não foi disparada**: o teto é de 2 rodadas, e ela só se justifica quando o
fechamento cria superfície nova de risco. Os 9 cenários novos são recombinações de partições e
técnicas já auditadas nesta rodada (discriminador na edição, segundo giro, domínio do terceiro
campo numérico, direção de escrita do isolamento) — nenhum introduz mecanismo novo. Registrado
como decisão, não como esquecimento.

### Divergências declaradas (rule do projeto e arnês vencem a skill)

1. **`.ai/rules/testes-browser.md` vence** a sugestão de `pest --parallel --tia` da skill: o
   ambiente não tem PCOV, o `--tia` com Xdebug em série não termina (medido: abortado após 35 min)
   e `--parallel` derruba os CT-B. Os comandos desta feature são **dois**:
   `vendor/bin/pest --parallel --group=kit` e `vendor/bin/pest --testsuite=Browser`.
2. **A camada `Unit` não existe neste projeto.** `tests/Pest.php` liga `TestCase` a `Feature`,
   `Kit`, `Browser` e `TenancyTestCase` a `Tenancy`/`BrowserTenancy` — **nunca a `Unit`**
   (`tests/Unit/` só tem `ExampleTest.php`, sem `TestCase`). Um "CT unitário" de cálculo rodaria
   sem container e o cast de enum de `tipo` não resolveria. **A escada real deste projeto começa em
   `tests/Kit`** (single-tenant, `TestCase` + `RefreshDatabase`). Todo cenário de cálculo está
   alocado ali e não em `Unit`. *(Achado de infra: se `Unit` deve ser uma camada de verdade,
   `tests/Pest.php` precisa de `pest()->extend(TestCase::class)->in('Unit')` — decisão fora do
   escopo desta feature.)*
3. **`pestphp/pest-plugin-mutate` está em `vendor/` mas não em `composer.json`** — é dependência
   transitiva do Pest 5 e some num `composer update`. Antes de rodar o fechamento do ciclo:
   `composer require pestphp/pest-plugin-mutate --dev`. Sem isso o gate de mutação funciona por
   acidente da árvore de dependências.

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | model do cupom (tabela própria, plural irregular), model da trilha de uso, 2 migrations, enum de tipo, Resource + 3 páginas no painel `/app`, policy gerada pelo Shield, recorte no `PapeisSeeder` (arquivo **compartilhado**), factory, channel de log. Nenhum job, observer, command ou config nova | CT-02, CT-28 |
| **F**unction | cadastrar / editar / excluir / listar; calcular desconto em 2 ramos; validar código (existe, validade, limite); consumir uso; registrar trilha; derivar situação; normalizar código; unicidade escopada. **Função administrativa escondida**: o recorte de escrita do usuário comum, que não tem tela | CT-01…CT-16, CT-22…CT-30 |
| **D**ata | entram: `codigo` (texto livre, 40), `tipo` (2 valores), `valor` (inteiro, **unidade decidida pelo tipo**), validade (`timestamp`), limite (inteiro), total em centavos, usuário aplicador. Já existem: usuários, papéis, organizações. **Nulo/vazio**: código `null`, `''`, `'   '`; aplicador sem identidade. **Dado grande**: total alto, `valor` além do range de `unsignedInteger`. **Dado de outra organização**: cupom da Globex não pode ser visto, aplicado nem bloquear o código na Acme. **Dado temporal**: validade no passado, no instante exato e no futuro | CT-01, CT-03, CT-11, CT-20, CT-31…CT-33 |
| **I**nterfaces | 3 rotas do Resource no `/app` (`index`, `create`, `{record}/edit`, `{record}` = **uuid**); chamada direta ao motor por controller/job/comando; os dois seeders de permissão. **Não há** rota HTTP pública, comando artisan, webhook nem import nesta entrega | CT-02, CT-17, CT-33 |
| **P**latform | SQLite `:memory:` nos testes × MySQL em produção — e a diferença **importa**: unicidade composta com `tenant_id` **NULL** não barra duplicata na maioria dos bancos (modo single-tenant, que é o default do kit). Colação/case-sensitivity do índice do código. `unsignedInteger` estoura acima de 4.294.967.295. Navegador + `npm run build` para os CT-B. Fuso do app é `UTC` (`config/app.php:68`) | CT-12, CT-21, M29 (sem matador) |
| **O**perations | personas: `master_global` (escreve nos dois modos), `admin_organizacao` (só existe com tenancy ligada), `panel_user` (só lê), `admin` e `infra` (não alcançam o `/app`). **Uso indevido**: usuário comum disparando criação, edição e exclusão; aplicar cupom de outra organização; **gravar cupom dentro da organização alheia**; retry do chamador do motor | CT-28…CT-33, CT-43, CT-45, CT-47 |
| **T**ime | expiração é **fronteira de instante**; fuso do app × do banco; virada do dia; concorrência de dois consumos; a **janela** entre validar e aplicar; reentrada (cupom expirado editado volta a valer). **DST não se aplica**: o app roda em `UTC` e o Brasil não tem horário de verão desde 2019 — declarado, não esquecido | CT-13, CT-14, CT-18, CT-21, CT-24, CT-37 |

Nenhuma dimensão vazia. A única dispensa é o DST, com o motivo escrito.

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — os campos numéricos do cadastro só são gravados dentro do domínio, e o do `valor` depende do **tipo** | A1 (completo) | RQ-03, RQ-04, RQ-06 | tabela de decisão (tipo × valor) + BVA 3-valores nos dependentes | CT-01…CT-03, CT-42 |
| **R2** — toda restrição do cadastro vale de novo na **edição**, e a edição não colide consigo mesma | A1 (completo) | RQ-02…RQ-06, RQ-14 | EP nos três pontos + armadilhas da edição + decisão com o discriminador variando | CT-04…CT-07, CT-40 |
| **R3** — o código é **único por organização** e **normalizado** em qualquer via de escrita | A1 (completo) | RQ-02, RQ-14 | normalização + unicidade | CT-08, CT-09, CT-11, CT-12 |
| **R4** — a validade só é gravável **no futuro** | A1+A3 (completo) | RQ-05, RQ-10 | BVA 3-valores (incremento 1 s) | CT-13, CT-14 |
| **R5** — o desconto percentual é `valor`% do total, **truncado para baixo** | A2 (padrão) | RQ-04, RQ-12 | BVA 3-valores + exemplos discriminantes (escalada) | CT-15 |
| **R6** — o desconto fixo é o próprio valor em centavos, e o total final **nunca fica negativo** | A2 (padrão) | RQ-04, RQ-12 | EP + BVA no piso zero | CT-16 |
| **R7** — só o cupom que **existe**, está **na validade** e tem **uso disponível** é aceito | A3 (completo) | RQ-09, RQ-10, RQ-11 | tabela de decisão (3 condições) + BVA no instante e no contador | CT-17…CT-21 |
| **R8** — aplicar consome **exatamente um** uso, e o limite não é furado sob disputa | A3 (completo) | RQ-11, RQ-13 | rastreio de efeito + concorrência | CT-22…CT-24 |
| **R9** — toda aplicação registra **quem** e **quando**, uma vez, e nunca sem o consumo | A3 (completo) | RQ-15 | rastreio de efeito (4 cenários — atomicidade importa) + 2-switch no uso | CT-25…CT-27, CT-41 |
| **R10** — só quem tem permissão de escrita **cria, edita e exclui**; os demais **apenas listam** | A4 (padrão) | RQ-07, RQ-08 | matriz papel × ação, com os três verbos disparados | CT-28…CT-30, CT-45, CT-47 |
| **R11** — cupom de outra organização não é visto, não é aplicado, **não bloqueia o código** e não recebe escrita | A4 (padrão) | RQ-14 (P-04) | IDOR / autorização horizontal nas duas direções + unicidade escopada | CT-31…CT-33, CT-43 |
| **R12** — quem não escreve vê **só os ativos**, e a situação exibida deriva da validade e do limite | A5 (mínimo) | RQ-08 (P-03) | EP **exaustiva** do enum de situação (escalada) | CT-34, CT-35, CT-44 |
| **R13** — cupom **excluído** deixa de funcionar em toda operação, e cada operação tem um caminho válido | A3+A5 (completo) | RQ-01, RQ-07, RQ-15 | tabela **estado × operação** + ciclo de volta 2-switch | CT-36…CT-39, CT-46, CT-48 |

**Cobertura das cláusulas** — toda `RQ` do `00` gerou regra:

| RQ | Regra(s) | RQ | Regra(s) |
|---|---|---|---|
| RQ-01 | R1, R2, R13 | RQ-09 | R7 |
| RQ-02 | R2, R3 | RQ-10 | R4, R7 |
| RQ-03 | R1 | RQ-11 | R7, R8 |
| RQ-04 | R1, R5, R6 | RQ-12 | R5, R6 |
| RQ-05 | R2, R4 | RQ-13 | R8 |
| RQ-06 | R2, R7 | RQ-14 | R3, R11 |
| RQ-07 | R10 | RQ-15 | R9, R13 |
| RQ-08 | R10, R12 | | |

**Leitura do mapa antes de seguir**: 8 perguntas vermelhas novas (abaixo), nenhuma delas
bloqueando a maioria das regras — o requisito está maduro no **uso** e imaturo na **gravação e na
exclusão**, que é exatamente o padrão que a regra "criação ≠ edição ≠ uso" prevê. Nenhuma regra
ficou sem exemplo; nenhum exemplo ficou sem regra.

---

## Fronteira com o Plano

> O que veio do `01-plano-acao.md` e foi **recusado como oráculo**. Sem esta lista, metade dos
> cenários vira teste do PRD sem ninguém perceber.

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| nomes de método (`valido()`, `aplicarEm()`, `descontoSobre()`, `situacao()`, `scopeAtivos()`) | escolha de implementação | detalhe do cenário |
| nomes de tabela e coluna (`cupons`, `cupom_usos`, `expira_em`, `limite_de_usos`, `usos`, `valor_original`, `valor_desconto`) | escolha de implementação | detalhe do cenário (o `Então` afirma **o fato**: "existe um registro de uso com o autor e o instante"; o requisito determina o fato, o PRD só deu o nome) |
| channel de log `cupom` e as três mensagens `[Cupom@…]` | o requisito **não pede log nenhum** | **nenhum `Então` desta especificação afirma sobre log.** RQ-15 pede registro **persistido e consultável**, que é a trilha — não a linha de log. Log é apoio de diagnóstico |
| `intdiv`, `DB::transaction`, mutator vs observer, `->increment()` do Query Builder | arquitetura | detalhe do cenário |
| rótulos da tela ("Válido até", "Percentual de desconto", "Valor do desconto (centavos)") | comportamento **visível** que o requisito não determina | **pergunta** (Q-05). Os CT-B afirmam que o rótulo **muda com o tipo**, não qual é o texto |
| texto da mensagem de erro de código duplicado | idem | **pergunta** (Q-05) |
| `defaultSort('expira_em','desc')` e as cores do badge | idem | **pergunta** (Q-06) |
| precedência `Esgotado` > `Expirado` no rótulo | idem | **pergunta** (Q-04); cenário marcado `@premissa` |
| `->minDate(now())` no campo de validade | idem — e é a **premissa central de R4** | **pergunta** (Q-01); cenários marcados `@premissa` |
| `nullOnDelete` em quem aplicou / `cascadeOnDelete` na trilha | comportamento visível **contra** RQ-15 ("auditar depois") | **perguntas** (Q-03 e Q-07); cenários marcados `@premissa` |
| `Heroicon::OutlinedTicket`, `BadgeContagemNavegacao`, `LOG_CUPOM_LEVEL` | cosmético / configuração | fora de escopo de CT |

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` desta feature vive em `wikis/specs/exp-a/` e está sendo
> usado como **linha de base de comparação** — é somente leitura para esta derivação. As perguntas
> abaixo estão em bloco pronto para colagem na seção `## Ambiguidades e Perguntas Abertas` do `00`.
> Elas **continuam bloqueando** o que delas depende; o que muda é só o arquivo onde estão escritas.

```markdown
### A-10 — Cupom com validade já vencida pode ser **cadastrado**?

RQ-05 dá ao cupom uma data de validade e RQ-10 valida a validade **na aplicação**. Nada é dito
sobre gravar. **Premissa (P-10)**: a validade é gravável só estritamente no futuro, na criação
**e** na edição — um cupom nascido vencido é um registro que nunca poderá ser usado, e aceitá-lo
transforma o cadastro em depósito de lixo. Bloqueia **R4**.

### A-11 — Quando o desconto fixo excede o total, o **desconto registrado** é o nominal ou o concedido?

P-07 diz que o resultado é limitado em zero, e não diz o que a trilha de RQ-15 guarda. Cupom de
R$ 50,00 num total de R$ 30,00: a trilha registra 5.000 ou 3.000 centavos? **Premissa (P-11)**: o
desconto registrado é o **efetivamente concedido** (3.000) — a trilha existe para responder
"quanto se deu de desconto", e o nominal responde outra pergunta. Bloqueia **R6** e **R9**.

### A-12 — A aplicação pode ocorrer **sem usuário identificado**?

RQ-15 exige registrar **quem** aplicou. Se o motor aceita ser chamado por job, comando ou rota
pública sem usuário, a trilha nasce anônima e RQ-15 fica cumprida só no caminho da tela.
**Premissa (P-12)**: a aplicação exige um usuário identificado; não existe registro de uso sem
autor. Bloqueia **R9** (a lacuna L-03).

### A-13 — Esgotado **e** expirado ao mesmo tempo: qual rótulo o usuário vê?

RQ-08 fala de "cupons ativos" e o card nunca enumera os inativos. **Premissa (P-13)**: `Esgotado`
vence `Expirado`, porque um cupom que esgotou cumpriu o seu papel e o operador precisa saber
disso. Bloqueia uma linha de **R12**.

### A-14 — Os **textos visíveis** (rótulos, mensagens de erro, ordem da listagem) são de quem?

O rótulo do campo `valor` é o único lugar que declara a unidade (centavos × pontos percentuais), e
o requisito não determina texto nenhum. **Premissa (P-14)**: os CT afirmam que o rótulo **muda
conforme o tipo**, nunca qual é o texto. Se o texto importa para o negócio, ele é requisito e
precisa ser escrito.

### A-15 — A exclusão do cupom é **física** ou **lógica**?

RQ-07 dá ao admin o direito de excluir. Se a exclusão é lógica, o código continua ocupando o
índice único de RQ-14 e não pode ser recadastrado. **Premissa (P-15)**: exclusão física, e o
código volta a ficar livre. Bloqueia **R13** (CT-38).

### A-16 — Excluir o cupom apaga a **trilha de uso**?

RQ-15 pede registro "pra gente conseguir auditar **depois**". Se a exclusão do cupom leva a trilha
junto, RQ-15 é cumprida só enquanto ninguém excluir — e a evidência desaparece exatamente quando
alguém tem motivo para apagar o cupom. **Premissa (P-16)**: a trilha sobrevive à exclusão do
cupom. Bloqueia **R13** (CT-39). **É a pergunta de maior consequência desta lista.**

### A-17 — Existe **teto** para o desconto fixo?

O card não dá teto, e um `valor` fixo acima do range da coluna inteira faz a gravação estourar em
erro de banco em vez de recusar com mensagem. Sem resposta, o mutante M29 fica **sem matador**.

### A-19 — O papel `admin` da instalação alcança a tela de cupons? **O `00` se contradiz aqui**

A defesa da premissa P-02 usa, como terceiro argumento, que *"`master_global` e o papel `admin`
continuam alcançando a tela por herança do `Gate::before`"*. Mas o acesso a painel se decide pelo
painel declarado no papel, e só o papel global atravessa pelo gate — o `admin` tem painel próprio e
não alcança o painel de negócio. Se o argumento estiver errado, **P-02 fica com dois argumentos, e
RQ-07 nomeia literalmente o papel que a premissa excluiu**. **Premissa (P-17)**: `admin` não
alcança a tela de cupons. Bloqueia uma linha de **R10** (CT-28).

### A-18 — O total do pedido é **idempotente** sob dupla aplicação?

Consequência direta de A-01 (o `Pedido` não existe). Sem o agregado, "aplicar o mesmo cupom duas
vezes deixa o total igual" é **inexpressável**: só há o cupom, e afirmar sobre o contador dele
prova contabilidade, não idempotência. Ver a lacuna **L-01**.
```

**Resumo das perguntas e do que elas bloqueiam:**

| # | Pergunta | Bloqueia | Premissa adotada |
|---|---|---|---|
| Q-01 | A-10 — validade vencida é gravável? | R4 (CT-13, CT-14) | P-10 — não |
| Q-02 | A-11 — desconto registrado nominal ou concedido? | R6, R9 (CT-16, CT-25) | P-11 — concedido |
| Q-03 | A-12 — aplicação sem usuário? | R9 (L-03) | P-12 — não |
| Q-04 | A-13 — esgotado × expirado | R12 (CT-34) | P-13 — esgotado vence |
| Q-05 | A-14 — textos visíveis | CT-B02 | P-14 — CT afirmam a mudança, não o texto |
| Q-06 | — ordem default da listagem | nenhum CT | não derivado (sem oráculo) |
| Q-07 | A-15/A-16 — exclusão física? trilha sobrevive? | R13 (CT-38, CT-39) | P-15, P-16 |
| Q-08 | A-17 — teto do desconto fixo | M29 sem matador | nenhuma |
| **Q-09** | **A-19 — o papel `admin` alcança a tela? O `00` se contradiz** | R10 (CT-28, linha `admin`) | P-17 — não alcança |

---

## Setup Global

### Personas

| Persona | Como criar | Suíte |
|---|---|---|
| `admin_organizacao` — quem cadastra cupom no modo multi-tenant | `papelNaOrganizacao(usuario('ana@example.com'), 'admin_organizacao', $acme)` | `Tenancy` |
| `panel_user` — quem apenas lê | `usuarioComPapel('panel_user', $acme)` (Tenancy) / `usuarioDoKit('panel_user')` (Kit) | ambas |
| `master_global` — quem escreve no modo single-tenant, pelo `Gate::before` | `usuarioDoKit('master_global')` | `Kit` |
| `admin` da instalação — **não alcança** o `/app` | `usuarioDoKit('admin')` | ambas |
| `infra` — idem | `usuarioDoKit('infra')` | `Tenancy` |
| o comprador que aplica o cupom | `usuario('rui@example.com')` — sem papel; aplicar não é operação de painel | `Kit` |

> **`papelNaOrganizacao()` e não `assignRole()` direto**: papel gravado em
> `Tenant::CONTEXTO_GLOBAL` fica invisível dentro do `/app` (o `wherePivot` do spatie filtra pelo
> team do request). Helper de `tests/Pest.php:323`.
>
> **`noPainelDa($tenant)` antes de todo cenário de componente** (`tests/Pest.php:210`): teste de
> Livewire não passa pelo middleware do painel, e sem `setTenant` + `setPermissionsTeamId` o
> cenário mede o ramo fail-closed em vez da regra.

### Fixtures

- `Cupom::factory()` — cupom ativo, percentual, com validade futura e limite folgado.
- `Cupom::factory()->expirado()` — validade no passado.
- `Cupom::factory()->esgotado()` — contador igual ao limite. **Atenção de arnês**: o contador de
  usos está fora do `$fillable` (é ele que RQ-13 move), então `state(['usos' => …])` é **descartado
  em silêncio** — o state precisa de `afterCreating()` + `forceFill()`. Um cenário de esgotamento
  escrito com `state()` fica **verde provando nada**.
- `Cupom::factory()->fixo(int $centavos)` — tipo fixo.
- `tenant('Acme','acme')` / `tenant('Globex','globex')` — `tests/Pest.php:170`.

### Fakes

- **Nenhum** `Mail::fake()`, `Queue::fake()` ou `Notification::fake()`: a feature não envia e-mail,
  não enfileira e não notifica (declarado fora de escopo no `00`). Cenário que "prova" que nada foi
  enviado numa feature que nada envia é tautologia.
- `Http::fake()` não se aplica — nenhuma chamada externa.
- Log: **não é oráculo** (ver `## Fronteira com o Plano`). Se algum cenário precisar silenciar o
  channel, o precedente é `Mockery::spy(LoggerInterface::class)` +
  `Log::shouldReceive('channel')->with('cupom')` (molde de `espiarAutenticacao()`).

### Estratégia de DB

`RefreshDatabase` global, ligado por `tests/Pest.php` em `Kit`, `Tenancy`, `Browser` e
`BrowserTenancy`. SQLite `:memory:` (`phpunit.xml`). Todo arquivo que dependa de permissão abre com
`$this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class])` **nesta ordem** — Resource novo
nasce sem permission e a tela responde 403 para todo mundo que não seja `master_global`
(`.ai/rules/filament.md:33-38`).

### Arquivos de teste

| Arquivo | Suíte | O que recebe |
|---|---|---|
| `tests/Kit/CupomTest.php` | `Kit` (single-tenant, grupo `kit`) | cálculo, validação, consumo, trilha, unicidade fora do formulário, fuso |
| `tests/Tenancy/CupomTenancyTest.php` | `Tenancy` (grupo `kit`) | formulário por componente, matriz papel × ação, isolamento, listagem |
| `tests/BrowserTenancy/CupomTest.php` | `Browser` | os 2 CT-B |

---

## Regra R1 — O cupom só é gravado com `valor` dentro do domínio do **seu tipo**

> `RQ-03`, `RQ-04` · área A1 · perfil **completo** · técnica: **tabela de decisão (tipo × valor)**
> + **BVA 3-valores** no campo dependente (incremento **1**, inteiro)
> `@premissa P-05` — o requisito dá dois tipos e **um** `valor`, e não diz a unidade de nenhum.

> **Domínio condicionado, não domínio único.** Tratar `valor` como um domínio só faz o teto de 100%
> desaparecer sem que ninguém note, porque os cenários "cobrem o campo `valor`". A tabela é:
>
> | `tipo` | domínio de `valor` | fronteiras |
> |---|---|---|
> | porcentagem | 1…100 pontos percentuais | **0, 1, 100, 101** |
> | fixo | ≥ 1 centavo, sem teto | **0, 1** (e 101 **válido** — é a célula que prova a ausência do teto) |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Os campos numéricos do cadastro só são gravados dentro do seu domínio, e o domínio
         do valor depende do tipo escolhido

    Esquema do Cenário: [CT-01] o domínio de valor depende do tipo escolhido
      Dado que a administradora da organização preenche um cupom novo do tipo "<tipo>"
      E informa <valor> no valor do desconto
      Quando ela submete o formulário de criação
      Então o resultado é "<resultado>"
      E a organização tem <total> cupons, e o cupom gravado (quando houver) tem tipo "<tipo>"
        e valor <valor>

      Exemplos:
        | tipo        | valor | resultado | total | # fronteira                            |
        | porcentagem | -5    | recusado  | 0     | abaixo do mínimo, negativo             |
        | porcentagem | 0     | recusado  | 0     | borda−1 do mínimo                      |
        | porcentagem | 1     | aceito    | 1     | borda do mínimo                        |
        | porcentagem | 100   | aceito    | 1     | borda do máximo — 100% é desconto total|
        | porcentagem | 101   | recusado  | 0     | borda+1 do máximo                      |
        | fixo        | -1    | recusado  | 0     | abaixo do mínimo, negativo             |
        | fixo        | 0     | recusado  | 0     | borda−1 do mínimo                      |
        | fixo        | 1     | aceito    | 1     | borda do mínimo — 1 centavo            |
        | fixo        | 101   | aceito    | 1     | **o teto de 100 NÃO vale para o fixo** |

    Esquema do Cenário: [CT-42] o limite de usos também tem domínio, na criação e na edição
      Dado que a administradora da organização informa <limite> no limite de usos
      Quando ela grava o cupom pela via "<via>"
      Então o resultado é "<resultado>"
      E o limite persistido é <persistido>

      Exemplos:
        | via     | limite | resultado | persistido | # fronteira                                  |
        | criação | -1     | recusado  | —          | abaixo do mínimo, negativo                   |
        | criação | 0      | recusado  | —          | borda−1: cupom que nasce sem nenhum uso      |
        | criação | 1      | aceito    | 1          | borda do mínimo                              |
        | edição  | 0      | recusado  | 3          | **a mesma regra vale no salvamento**         |
        | edição  | 5      | aceito    | 5          | célula válida da edição                      |

    Cenário: [CT-02] o cupom criado pela tela grava os cinco campos que o requisito exige
      Dado que a administradora da organização preenche o código "promo29", o tipo porcentagem,
        o valor 29, a validade em 30/09/2026 23:59 e o limite de 3 usos
      Quando ela submete o formulário de criação
      Então existe na organização dela um cupom com código "PROMO29", tipo porcentagem,
        valor 29, validade 30/09/2026 23:59 e limite 3
      E o contador de usos desse cupom é 0

    Esquema do Cenário: [CT-03] cada um dos cinco campos é obrigatório
      Dado que a administradora da organização preenche um cupom novo sem informar "<campo>"
      Quando ela submete o formulário de criação
      Então o resultado é recusado com erro no campo "<campo>"
      E nenhum cupom novo existe na organização dela

      Exemplos:
        | campo          | # partição      |
        | codigo         | ausente (RQ-02) |
        | tipo           | ausente (RQ-03) |
        | valor          | ausente (RQ-04) |
        | expira_em      | ausente (RQ-05) |
        | limite_de_usos | ausente (RQ-06) |
```

> **Por que CT-02 não é caminho feliz redundante**: ele é o **gate de tela de escrita** da rota
> `create` (`.ai/rules/testes.md` → *"uma tela aberta não é uma tela que grava"*), e o `Então`
> confere os cinco campos, não a chave primária. `assertDatabaseHas` só com a PK passa com todos os
> outros campos errados. O valor 29 e o limite 3 não são decorativos: são os mesmos que
> discriminam R5 e R7 mais adiante.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | teto de 100 aplicado a **qualquer** tipo (o `valor` tratado como domínio único) | CT-01 (linha `fixo` / 101) |
| M2 | teto de 100 **ausente** (nada barra 101%) | CT-01 (linha `porcentagem` / 101) |
| M3 | mínimo `>= 0` em vez de `>= 1` (cupom de desconto zero é gravável) | CT-01 (linhas `porcentagem`/0 e `fixo`/0) |
| M4 | um dos cinco campos não é gravado — o formulário salva e o campo fica no default | CT-02 |
| M5 | campos sem obrigatoriedade: o cupom nasce sem tipo ou sem limite | CT-03 |
| M65 | o limite de usos não tem domínio: cupom de limite 0 é gravável e nasce inutilizável | CT-42 (linhas de criação) |
| M66 | o domínio do limite existe na criação e some no salvamento | CT-42 (linha `edição` / 0) |

---

## Regra R2 — Toda restrição do cadastro vale de novo na **edição**, e a edição não colide consigo mesma

> `RQ-02`…`RQ-06`, `RQ-14` · área A1 · perfil **completo** · técnica: **EP nos três pontos**
> (criação, edição, uso) + as **duas armadilhas próprias da edição**

> O requisito descreve o ponto de **uso** ("na hora de aplicar…") e não diz uma palavra sobre
> editar. É a omissão mais cara: normalização, unicidade, autorização e domínio costumam existir
> no `create` e sumir no `save`, e **nenhum cenário que só cria enxerga isso**.
>
> As duas armadilhas que não existem na criação:
> 1. **unicidade contra si mesmo** — salvar sem alterar o código deve **passar**; a validação
>    ingênua acusa colisão do registro com ele próprio → **CT-04**
> 2. **validação que só roda no `create`** — regra escrita na criação e esquecida no `save` é
>    invisível para quem só cria → **CT-05**, **CT-14**

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: A edição revalida tudo o que a criação valida, e não colide com o próprio registro

    Cenário: [CT-04] salvar a edição sem alterar o código passa
      Dado um cupom "PROMO29" da organização, com limite de 3 usos
      Quando a administradora da organização salva a edição com o mesmo código e limite 5
      Então o formulário não acusa erro no código
      E o cupom continua com o código "PROMO29" e passa a ter limite 5
      E existe **um** único cupom com o código "PROMO29" na organização

    Esquema do Cenário: [CT-05] o domínio do valor é revalidado no salvamento
      Dado um cupom do tipo "<tipo>" da organização, com valor <valor_atual>
      Quando a administradora da organização salva a edição com o valor <valor_novo>
      Então o resultado é "<resultado>"
      E o valor persistido do cupom é <valor_persistido>

      Exemplos:
        | tipo        | valor_atual | valor_novo | resultado | valor_persistido | # fronteira                    |
        | porcentagem | 29          | 101        | recusado  | 29               | borda+1 do máximo, na edição   |
        | porcentagem | 29          | 0          | recusado  | 29               | borda−1 do mínimo, na edição   |
        | porcentagem | 29          | 100        | aceito    | 100              | borda do máximo, na edição     |
        | fixo        | 1000        | 101        | aceito    | 101              | sem teto no fixo, na edição    |

    Cenário: [CT-06] editar o código para o de outro cupom é recusado, mesmo em caixa diferente
      Dado dois cupons da mesma organização, "PROMO29" e "BLACKFRIDAY"
      Quando a administradora da organização salva o segundo com o código " promo29 "
      Então o formulário acusa erro no código
      E o segundo cupom continua com o código "BLACKFRIDAY"
      E o primeiro cupom continua existindo, com valor e limite inalterados

    Cenário: [CT-07] o contador de usos não é alterável pelo formulário
      Dado um cupom da organização com limite de 3 usos e 3 usos já feitos
      Quando a administradora da organização salva a edição enviando também o contador de usos
        com o valor 0
      Então o contador de usos persistido continua 3
      E o cupom continua com 3 de 3 usos, sem uso disponível

    Esquema do Cenário: [CT-40] mudar o tipo revalida o valor contra o domínio do tipo novo
      Dado um cupom da organização do tipo "<tipo_atual>" com valor <valor_atual>
      Quando a administradora da organização salva a edição trocando o tipo para "<tipo_novo>",
        sem mexer no valor
      Então o resultado é "<resultado>"
      E o cupom persistido tem tipo "<tipo_final>" e valor <valor_final>

      Exemplos:
        | tipo_atual  | valor_atual | tipo_novo   | resultado | tipo_final  | valor_final | # célula                                        |
        | fixo        | 1000        | porcentagem | recusado  | fixo        | 1000        | **1000% seria gravável se o teto olhasse o tipo antigo** |
        | fixo        | 50          | porcentagem | aceito    | porcentagem | 50          | dentro do domínio do tipo novo — a célula válida |
        | porcentagem | 50          | fixo        | aceito    | fixo        | 50          | o sentido inverso, sem teto no destino          |
```

> **CT-07 é o cenário de mass assignment desta feature, e ele deriva do requisito** — não do
> plano: se o contador é gravável pela tela, o limite de RQ-11 deixa de ser limite. Qualquer pessoa
> com acesso à edição zera o contador e resgata o cupom para sempre. O `Então` afirma os **dois**
> lados: o dado persistido **e** a consequência de comportamento.
>
> **CT-06 usa `" promo29 "` e não `PROMO29X`** porque o valor tem de ser discriminante: espaço nas
> bordas + caixa minúscula distinguem uma unicidade normalizada de uma unicidade byte a byte.
> `PROMO29` × `BLACKFRIDAY` não distinguiria nada.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6 | validação de domínio declarada só na criação; o `save` aceita qualquer valor | CT-05 |
| M7 | unicidade sem ignorar o próprio registro — salvar sem mudar o código acusa colisão | CT-04 |
| M8 | unicidade comparando byte a byte, sem normalizar o valor digitado | CT-06 |
| M9 | contador de usos dentro dos campos de escrita em massa | CT-07 |
| M67 | o teto do valor é resolvido pelo tipo **já persistido** e não pelo submetido: trocar o tipo para percentual mantendo o valor grava um cupom de 1000% | CT-40 (primeira linha) |

> **M67 é o achado mais grave da revisão adversarial, e ele existe porque CT-05 mantinha o `tipo`
> constante nas quatro linhas.** A coluna do discriminador estava lá e nunca mudava — a forma mais
> silenciosa de um `Exemplos:` parecer cobrir um domínio condicionado sem cobrir. Um cupom de 1000%
> sobre 10.000 centavos devolve um total de **−90.000**, e a única coisa entre isso e produção era
> um cenário que ninguém tinha escrito. A lição vale além desta feature: **quando o domínio é
> condicionado, o discriminador tem de variar em pelo menos um cenário de edição.**

---

## Regra R3 — O código é **único por organização** e **normalizado** em qualquer via de escrita

> `RQ-02`, `RQ-14` · área A1 · perfil **completo** · técnica: **normalização** (caixa, espaços nas
> bordas, acento, unicode) + **unicidade** · `@premissa P-04` (escopo da unicidade)

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O código é único dentro da organização e é gravado normalizado

    Esquema do Cenário: [CT-08] o código é gravado em maiúsculas e sem espaços nas bordas
      Dado um cupom "OUTRO29" já cadastrado na organização, usado só pelas linhas de edição
      E que a administradora da organização informa o código "<digitado>"
      Quando ela grava o cupom pela via "<via>"
      Então o código persistido é "PROMO29"

      Exemplos:
        | via     | digitado    | # partição                        |
        | criação | promo29     | caixa mínima                      |
        | criação | " promo29 " | espaços nas duas bordas           |
        | criação | Promo29     | caixa mista                       |
        | edição  | promo29     | **a normalização vale no save**   |
        | edição  | " PROMO29 " | espaços nas bordas, no save       |

    Esquema do Cenário: [CT-09] o código não se repete dentro da organização
      Dado um cupom "PROMO29" já cadastrado na organização
      Quando a administradora cadastra um segundo cupom com o código "<segundo>"
      Então o resultado é "<resultado>"
      E a organização tem <total> cupons

      Exemplos:
        | segundo     | resultado | total | # partição                                   |
        | PROMO29     | recusado  | 1     | idêntico                                     |
        | promo29     | recusado  | 1     | difere só na caixa — o discriminante         |
        | " PROMO29 " | recusado  | 1     | difere só nos espaços das bordas             |
        | BLACKFRIDAY | aceito    | 2     | **célula válida**: código diferente entra    |

    Esquema do Cenário: [CT-11] o código aceita texto humano e o limite é medido em caracteres
      Dado que a administradora da organização informa o código "<digitado>"
      Quando ela submete o formulário de criação
      Então o resultado é "<resultado>"
      E o código persistido é "<persistido>", e a organização não ganha cupom nenhum
        quando o resultado é "recusado"

      Exemplos:
        | digitado                                   | resultado | persistido                                 | # partição                                          |
        | cupão10                                    | aceito    | CUPÃO10                                    | acento — `strtoupper` devolveria `CUPãO10`          |
        | promo🎉                                    | aceito    | PROMO🎉                                    | emoji, 4 bytes em UTF-8                             |
        | `A` × 40                                   | aceito    | `A` × 40                                   | borda do tamanho, em ASCII                          |
        | `A` × 41                                   | recusado  | —                                          | borda+1 do tamanho                                  |
        | `Ã` × 40                                   | aceito    | `Ã` × 40                                   | **borda em caracteres × bytes**: 80 bytes em UTF-8  |
        | `Ã` × 41                                   | recusado  | —                                          | borda+1 acentuada                                   |
        | "      "                                   | recusado  | —                                          | só espaços: vira vazio depois do trim               |

    Cenário: [CT-12] o código duplicado é barrado mesmo fora do formulário
      Dado um cupom "PROMO29" já gravado na instalação, sem passar pela tela
      Quando o sistema grava um segundo cupom com o código "PROMO29" pela mesma via
      Então a segunda gravação falha
      E existe exatamente um cupom com o código "PROMO29"
```

> **CT-12 existe porque RQ-14 não diz "na tela".** A unicidade que vive só na validação do
> formulário é furada pelo primeiro seeder, comando, job ou import — e no **modo single-tenant**,
> que é o default do kit, uma unicidade composta com a organização **nula** não barra nada na
> maioria dos bancos (dois `NULL` não são iguais). CT-12 roda em `tests/Kit`, que é justamente a
> suíte single-tenant, e é o único cenário que separa "unicidade de verdade" de "aviso na tela".
>
> **`cupão10` é o valor discriminante de CT-11**: `strtoupper('cupão10')` devolve `CUPãO10` em PHP.
> Nenhum código sem acento distingue as duas funções.
>
> **As linhas `Ã × 40` e `Ã × 41` entraram pela revisão adversarial**, e fecham a pergunta que os
> placeholders `{40 caracteres}` escondiam: **o limite é medido em caracteres ou em bytes?** Um
> limite em bytes (`varchar(40)` sem charset multibyte, ou `strlen`) aceita as duas linhas ASCII e
> **recusa** um código de 40 caracteres acentuados, que ocupa 80 bytes. Sem essas duas linhas, um
> código legítimo em português seria rejeitado em produção e nenhum cenário acusaria — e o
> `Exemplos:` continuaria parecendo cobrir a borda, porque a borda estava lá.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M10 | `strtoupper` em vez da variante multibyte | CT-11 (linha `cupão10`) |
| M11 | normalização sem remover os espaços das bordas | CT-08 (linhas com espaços) e CT-09 (linha `" PROMO29 "`) |
| M12 | normalização aplicada só na criação | CT-08 (linhas `via = edição`) |
| M13 | unicidade sensível a caixa (índice sobre o valor cru) | CT-09 (linha `promo29`) |
| M14 | limite de 40 caracteres ausente | CT-11 (linha `A × 41`) |
| M15 | unicidade **só** na validação do formulário, sem barreira na gravação | CT-12 |
| M68 | o limite de tamanho é medido em **bytes**: código de 40 caracteres acentuados é recusado | CT-11 (linha `Ã × 40`) |

---

## Regra R4 — A validade só é gravável **no futuro**

> `RQ-05`, `RQ-10` · áreas A1+A3 · perfil **completo** · técnica: **BVA 3-valores**, incremento
> **1 segundo** (o campo guarda instante, não dia) · `@premissa P-10` — **bloqueada por Q-01**

> Arnês: `freezeTime()` antes de montar os valores. Sem tempo congelado, `agora` deixa de ser um
> valor e a fronteira do instante vira flake.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: A validade gravada está estritamente no futuro

    Esquema do Cenário: [CT-13] a fronteira da validade na criação é o instante, não o dia
      Dado o tempo congelado em 15/09/2026 12:00:00
      E que a administradora da organização informa a validade "<validade>"
      Quando ela submete o formulário de criação
      Então o resultado é "<resultado>"
      E a validade persistida é exatamente "<persistida>", ao segundo

      Exemplos:
        | validade            | resultado | persistida          | # fronteira                     |
        | 15/09/2026 11:59:59 | recusado  | —                   | borda−1 (1 segundo no passado)  |
        | 15/09/2026 12:00:00 | recusado  | —                   | borda exata @premissa P-10      |
        | 15/09/2026 12:00:01 | aceito    | 15/09/2026 12:00:01 | borda+1 (1 segundo no futuro)   |
        | 15/09/2026 23:59:59 | aceito    | 15/09/2026 23:59:59 | fim do dia — o segundo sobrevive|

    Cenário: [CT-14] editar um cupom para validade no passado é recusado
      Dado o tempo congelado em 15/09/2026 12:00:00
      E um cupom da organização válido até 30/09/2026 23:59:00
      Quando a administradora da organização salva a edição com a validade 14/09/2026 23:59:00
      Então o formulário acusa erro na validade
      E a validade persistida continua 30/09/2026 23:59:00, ao segundo
```

> A linha `borda exata` está marcada `@premissa` porque o requisito não diz se "dentro da
> validade" inclui o instante gravado. Se a resposta a Q-01 for "inclui", **muda apenas essa
> linha** — e é por isso que ela está isolada em vez de diluída no cenário.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M16 | validade no passado aceita na criação | CT-13 (linhas borda−1 e dia anterior) |
| M17 | validade no passado aceita **só** no salvamento (regra só no `create`) | CT-14 |
| M18 | `>=` em vez de `>` na fronteira: o instante exato de expiração é aceito | CT-13 (linha borda exata) `@premissa` |
| M19 | o campo guarda **dia** e não instante: 23:59:59 vira meia-noite e a validade encurta | CT-13 (linhas de 23:59:59) e CT-21 |

---

## Regra R5 — O desconto percentual é `valor`% do total, **truncado para baixo**

> `RQ-04`, `RQ-12` · área A2 · perfil **padrão** · técnica **escalada**: **BVA 3-valores + exemplos
> discriminantes de representação** · `@premissa P-05` (pontos percentuais inteiros) e `P-06`
> (truncar)

> **Todo valor deste `Exemplos:` foi escolhido para discriminar, e a coluna diz contra o quê.**
> Dinheiro em centavos inteiros, nunca `float`.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O desconto percentual é a fração inteira do total, truncada para baixo

    Esquema do Cenário: [CT-15] o desconto percentual trunca a fração de centavo
      Dado um cupom de <percentual>% da organização
      Quando o sistema calcula o desconto sobre um total de <total> centavos
      Então o desconto é <desconto> centavos
      E o total com desconto é <final> centavos

      Exemplos:
        | percentual | total | desconto | final | # o que este valor discrimina                       |
        | 29         | 10000 | 2900     | 7100  | inteiro × `float`: `(int)(10000*0.29)` daria **2899** |
        | 10         | 9999  | 999      | 9000  | truncar × arredondar: `round` daria **1000**         |
        | 5          | 50    | 2        | 48    | truncar × arredondar em valor pequeno: daria **3**   |
        | 29         | 1049  | 304      | 745   | **ordem das operações**: dividir antes daria **290** |
        | 1          | 99    | 0        | 99    | borda inferior do resultado: trunca a **zero**       |
        | 100        | 10000 | 10000    | 0     | borda do máximo: 100% zera o total                  |
        | 100        | 1     | 1        | 0     | **piso do ramo percentual**: nunca devolve negativo  |
```

> **Como cada linha foi escolhida, e uma que foi rejeitada.** O primeiro rascunho deste `Exemplos:`
> tinha `33% de 10.001` na linha da ordem das operações. Ela **não discrimina**: `10001 × 33 = 330033`
> e `intdiv(330033,100) = 3300`; dividir antes (`intdiv(10001,100) = 100`, `× 33 = 3300`) dá o mesmo
> número. Nem a primeira linha discrimina a ordem — com total múltiplo de 100 as duas ordens
> coincidem sempre. A ordem só é discriminável com **total não múltiplo de 100 cujo resto interage
> com o percentual**: `29% de 1.049` dá `intdiv(1049*29,100) = 304` contra `intdiv(1049,100)*29 = 290`.
> Foi por isso que a linha de `33/10001` saiu e a de `29/1049` entrou. Um `Exemplos:` de valores
> redondos parece cobrir e não cobre.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M20 | percentual calculado em `float` e convertido depois | CT-15 (linha 29 / 10000 → 2899) |
| M21 | arredondar em vez de truncar | CT-15 (linhas 10/9999 e 5/50) |
| M22 | dividir por 100 **antes** de multiplicar pelo percentual | CT-15 (linha 29 / 1049 → 290) |
| M23 | teto de 100 aplicado ao **desconto** (limitado a 100 centavos) em vez de ao percentual | CT-15 (linhas 29/10000 e 100/10000) |
| M69 | o piso zero existe só no ramo de valor fixo; o ramo percentual pode devolver negativo | CT-15 (linha 100 / 1) e CT-40 (o caminho que produziria percentual > 100) |

> **O piso do ramo percentual foi um achado da revisão adversarial.** O enunciado de R6 fala do
> desconto *fixo*, e o piso só era exercitado lá — o ramo percentual ficava sem piso em cenário
> nenhum. Ele só é alcançável com percentual acima de 100, que é exatamente o que M67 permitia
> gravar: os dois defeitos são **um par**, e por isso um cenário sozinho não bastava.

---

## Regra R6 — O desconto fixo é o próprio valor em centavos, e o total final **nunca fica negativo**

> `RQ-04`, `RQ-12` · área A2 · perfil **padrão** · técnica: **EP** (ramo `fixo`) + **BVA** no piso
> zero, incremento **1 centavo** · `@premissa P-05` (centavos), `P-07` (piso zero), `P-11`
> (desconto registrado = concedido) — **bloqueada por Q-02**

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O desconto fixo é o valor em centavos e o total final nunca é negativo

    Esquema do Cenário: [CT-16] o desconto fixo é limitado pelo total do pedido
      Dado um cupom de valor fixo de <valor> centavos
      Quando o sistema calcula o desconto sobre um total de <total> centavos
      Então o desconto concedido é <desconto> centavos
      E o total com desconto é <final> centavos

      Exemplos:
        | valor | total | desconto | final | # o que este valor discrimina                                    |
        | 1000  | 12990 | 1000     | 11990 | centavos × reais: em reais daria 12890 (R$10) ou 2990 (÷100)      |
        | 2999  | 3000  | 2999     | 1     | borda−1 do piso: sobra **1 centavo**                             |
        | 3000  | 3000  | 3000     | 0     | borda do piso: total exatamente zerado                           |
        | 5000  | 3000  | 3000     | 0     | borda+1: desconto maior que o total → piso zero `@premissa P-07` |
        | 1     | 3000  | 1        | 2999  | borda do mínimo do valor                                         |
```

> A coluna `desconto` da linha `5000 / 3000` é onde vive **Q-02**: o desconto **concedido** é 3.000
> e não 5.000. Sob a premissa P-11 é esse número que a trilha de RQ-15 guarda (ver CT-25). Se a
> resposta a Q-02 for "o nominal", muda essa célula **e** uma linha de CT-25 — e nada mais.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M24 | piso zero ausente: o total final fica **negativo** | CT-16 (linha 5000 / 3000) |
| M25 | valor fixo interpretado em reais (multiplicado ou dividido por 100) | CT-16 (linha 1000 / 12990) |
| M26 | piso com comparação trocada: o total é zerado já quando o desconto **iguala** o total menos um | CT-16 (linhas 2999 e 3000) |
| M27 | o ramo `fixo` cai no cálculo percentual (o `match` sem os dois ramos) | CT-16 (linha 1000 / 12990 → 129) |
| M28 | **o motor acumula desconto sobre uma aplicação anterior do mesmo pedido** (dupla aplicação reduz o total duas vezes) | ⚠️ **sem matador** — ver lacuna **L-01** |
| M29 | valor fixo acima do range da coluna inteira estoura erro de banco em vez de recusar | ⚠️ **sem matador** — ver lacuna **L-02** |

---

## Regra R7 — Só o cupom que **existe**, está **na validade** e tem **uso disponível** é aceito

> `RQ-09`, `RQ-10`, `RQ-11` · área A3 · perfil **completo** · técnicas: **tabela de decisão** (3
> condições) + **BVA 3-valores** no instante (incremento 1 s) e no contador (incremento 1)

**Tabela de decisão** — 3 condições, 8 combinações; 3 colapsam porque quando o cupom não existe as
outras duas não são avaliáveis. Cinco regras sobrevivem:

| # | existe | na validade | uso disponível | resultado |
|---|---|---|---|---|
| D1 | não | — | — | recusado |
| D2 | sim | não | sim | recusado |
| D3 | sim | sim | não | recusado |
| D4 | sim | não | não | recusado |
| D5 | sim | sim | sim | **aceito** |

> D4 combina duas partições inválidas, o que a skill normalmente proíbe — e aqui **não** mascara
> nada, porque o oráculo é apenas "recusado", nunca **qual** motivo disparou. Se algum dia o motivo
> for devolvido ao chamador, D4 tem de virar dois cenários.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Só o cupom existente, dentro da validade e com uso disponível é aceito

    Esquema do Cenário: [CT-17] as três validações valem juntas, e todas são necessárias
      Dado um cupom "PROMO29" da organização do tipo "<tipo>" no estado "<estado>"
      Quando o comprador informa o código "<codigo>"
      Então o resultado é "<resultado>"
      E o cupom devolvido é o "PROMO29" da organização quando o resultado é "aceito"

      Exemplos:
        | # D | tipo        | estado              | codigo    | resultado | # regra da tabela       |
        | D1  | porcentagem | —                   | NAOEXISTE | recusado  | não existe              |
        | D2  | porcentagem | expirado, com uso   | PROMO29   | recusado  | fora da validade        |
        | D3  | porcentagem | válido, esgotado    | PROMO29   | recusado  | sem uso disponível      |
        | D4  | porcentagem | expirado e esgotado | PROMO29   | recusado  | as duas recusas juntas  |
        | D5  | porcentagem | válido, com uso     | PROMO29   | aceito    | **a célula válida**     |
        | D2  | fixo        | expirado, com uso   | PROMO29   | recusado  | **o ramo fixo valida a validade** |
        | D3  | fixo        | válido, esgotado    | PROMO29   | recusado  | **o ramo fixo valida o limite**   |
        | D5  | fixo        | válido, com uso     | PROMO29   | aceito    | célula válida do ramo fixo        |

    Esquema do Cenário: [CT-18] a validade é conferida no instante, não no dia
      Dado o tempo congelado em 15/09/2026 12:00:00
      E um cupom da organização com uso disponível e validade "<validade>"
      Quando o comprador informa o código do cupom
      Então o resultado é "<resultado>"
      E o contador de usos do cupom continua 0, e nenhum registro de uso existe

      Exemplos:
        | validade            | resultado | # fronteira                     |
        | 15/09/2026 12:00:01 | aceito    | borda+1 (1 segundo de validade) |
        | 15/09/2026 12:00:00 | recusado  | borda exata @premissa P-10      |
        | 15/09/2026 11:59:59 | recusado  | borda−1 (expirou há 1 segundo)  |

    Esquema do Cenário: [CT-19] o limite de usos é exclusivo no valor do limite
      Dado um cupom válido da organização com limite de 3 usos e <ja_usado> usos já feitos
      Quando o comprador informa o código do cupom
      Então o resultado é "<resultado>"
      E o contador de usos continua <ja_usado>, e nenhum registro de uso novo existe

      Exemplos:
        | ja_usado | resultado | # fronteira                          |
        | 2        | aceito    | borda−1                              |
        | 3        | recusado  | borda — o terceiro uso foi o último  |
        | 4        | recusado  | borda+1: distingue `==` de `>=`, e `==` recusaria o cupom só no valor exato |

    Esquema do Cenário: [CT-20] o código informado é interpretado normalizado, e o vazio recusa
      Dado os cupons válidos "PROMO29" e "CUPÃO10" da organização
      Quando o comprador informa o código "<informado>"
      Então o resultado é "<resultado>"
      E nenhum registro de uso é criado

      Exemplos:
        | informado   | resultado | # partição                                              |
        | (ausente)   | recusado  | argumento não informado                                 |
        | (nulo)      | recusado  | nulo explícito                                          |
        | ""          | recusado  | string vazia                                            |
        | "   "       | recusado  | só espaços                                              |
        | NAOEXISTE   | recusado  | código inexistente                                      |
        | " promo29 " | aceito    | a normalização de caixa e bordas vale na leitura        |
        | " cupão10 " | aceito    | **a normalização da leitura é multibyte** — o discriminante |

    Cenário: [CT-21] a validade é medida no fuso do aplicativo, não no do banco
      Dado o aplicativo no fuso "America/Sao_Paulo" e o banco gravando em UTC
      E um cupom da organização válido até 15/09/2026 23:59:59 no fuso do aplicativo
      Quando o comprador informa o código às 20:00:00 de 15/09/2026 no fuso do aplicativo
      Então o resultado é aceito
```

> **CT-21 não é lacuna de arnês, é cenário — e isso foi verificado antes de escrever.** O arnês
> permite: `config(['app.timezone' => 'America/Sao_Paulo'])` faz o app divergir do `UTC` de
> `config/app.php:68`, e `travelTo()` fixa o instante (precedente de uso em `tests/Kit/*`). A
> comparação ingênua — instante do banco lido como se fosse hora local — recusaria o cupom 3 horas
> antes do fim da validade. Declarar isto "impossível de testar" sem tentar seria a lacuna que a
> skill manda evitar.
>
> **CT-20 cobre `ausente ≠ nulo ≠ vazio`** com semântica declarada: as três recusam, e a
> semântica é a mesma — não há campo opcional aqui.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M30 | `>=` em vez de `>` na validade: o instante exato de expiração é aceito | CT-18 (linha borda exata) |
| M31 | `<=` em vez de `<` no contador: o uso além do limite passa | CT-19 (linha borda) |
| M32 | as três condições ligadas por "ou" em vez de "e" (basta uma passar) | CT-17 (linhas D2 e D3) |
| M33 | a conferência de limite ausente na validação (só a validade é olhada) | CT-17 (linha D3) e CT-19 |
| M34 | o código informado é comparado sem normalizar (só a escrita normaliza) | CT-20 (linha `" promo29 "`) |
| M35 | a validade comparada com o **dia** corrente em vez do instante, ou lida no fuso errado | CT-18, CT-21 |
| M70 | a normalização da **leitura** usa a função não-multibyte: o cupom com acento nunca é aplicável | CT-20 (linha `" cupão10 "`) |
| M71 | o ramo de valor fixo pula uma das três validações (atalho no `match`) | CT-17 (linhas `fixo` / D2 e D3) |

> **M70 e M71 vieram da revisão adversarial e são a mesma falha de método**: o valor discriminante
> (`cupão10`) e a partição do discriminador (`fixo`) existiam no conjunto, mas **só na via de
> escrita**. Uma partição exercitada em um ponto e ausente nos outros dá a sensação de cobertura
> mais cara que existe — o item fica ✅ no checklist e o defeito atravessa pelo ponto que ninguém
> replicou.

---

## Regra R8 — Aplicar consome **exatamente um** uso, e o limite não é furado sob disputa

> `RQ-11`, `RQ-13` · área A3 · perfil **completo** · técnica: **rastreio de efeito** (consumo do
> contador) + **concorrência**. **Esta regra consome o teto inteiro** — três cenários obrigatórios
> é o custo declarado da técnica, não estouro.

> **O tipo do cupom é coluna dos três cenários, e isso não é enfeite.** O tipo particiona o
> domínio *e o comportamento*: um atalho no ramo de valor fixo — que ignore validade, limite ou
> trilha — fica **verde em qualquer conjunto que só use cupom de porcentagem**. É por isso que
> `tipo` aparece em `Exemplos:` de CT-22, CT-23, CT-24 e CT-25, e não em um cenário só.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Aplicar um cupom consome exatamente um uso, e o limite nunca é ultrapassado

    Esquema do Cenário: [CT-22] aplicar um cupom ativo consome um uso e devolve o total com desconto
      Dado um cupom válido da organização do tipo "<tipo>" com valor <valor>, limite de 3 usos
        e 0 usos feitos
      Quando o comprador Rui aplica o cupom sobre um total de 10000 centavos
      Então o total devolvido é <final> centavos
      E o contador de usos persistido do cupom é 1

      Exemplos:
        | tipo        | valor | final | # partição do discriminador                          |
        | porcentagem | 29    | 7100  | ramo percentual                                      |
        | fixo        | 3000  | 7000  | ramo de valor fixo — **final distinto do percentual** |

    Esquema do Cenário: [CT-23] aplicar um cupom esgotado não consome nada
      Dado um cupom válido da organização do tipo "<tipo>" com limite de 3 usos e 3 usos feitos
      Quando o comprador Rui tenta aplicar o cupom sobre um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos persistido continua 3
      E nenhum registro de uso novo existe para esse cupom

      Exemplos:
        | tipo        | # partição do discriminador |
        | porcentagem | ramo percentual             |
        | fixo        | ramo de valor fixo          |

    Esquema do Cenário: [CT-24] a aplicação que partiu de leitura obsoleta é recusada
      Dado um cupom válido da organização do tipo "<tipo>" com limite de **1** uso, já aplicado
        uma vez, e uma referência ao cupom lida **antes** dessa aplicação
      Quando o comprador aplica o cupom por essa referência obsoleta
      Então a aplicação é recusada
      E o contador de usos persistido continua 1
      E existe exatamente **um** registro de uso para esse cupom

      Exemplos:
        | tipo        | # partição do discriminador |
        | porcentagem | ramo percentual             |
        | fixo        | ramo de valor fixo          |
```

> **Arnês de CT-24, e o que ele prova e não prova.** A técnica disponível neste projeto é a mesma
> de `tests/Tenancy/ConviteUsuarioExistenteTest.php:201` — as duas chamadas usam a **mesma
> instância em memória**, que é o que simula a segunda requisição que já passou pelo próprio
> `if` com um `usos` obsoleto. Isso **falsifica** um consumo do tipo ler-comparar-salvar.
> **Não** falsifica um consumo que só é atômico em transação real com duas conexões — ver lacuna
> **L-03** e o mutante M41.
>
> `limite = 1` e não 3 porque com limite 1 a diferença entre "consumiu uma vez" e "consumiu duas"
> é observável **no próprio limite**; com limite 3 as duas implementações caberiam dentro dele e o
> cenário provaria contabilidade em vez da barreira.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M36 | o incremento do contador nunca acontece | CT-22 |
| M37 | o contador é incrementado **antes** de validar: cupom esgotado também consome | CT-23 |
| M38 | consumo por ler-comparar-salvar, com leitura obsoleta | CT-24 |
| M39 | a barreira de limite existe só na validação prévia, e não no consumo | CT-24, CT-23 |
| M40 | o ramo de valor fixo não consome uso (atalho no `match`) | CT-22, CT-23, CT-24 (linhas `fixo`) |
| M41 | consumo atômico **só** em transação otimista: duas conexões reais simultâneas passam as duas | ⚠️ **sem matador** — ver lacuna **L-03** |

---

## Regra R9 — Toda aplicação registra **quem** e **quando**, uma vez, e nunca sem o consumo

> `RQ-15` · área A3 · perfil **completo** · técnica: **rastreio de efeito** — aconteceu / não
> aconteceu quando não devia / **atomicidade importa**, então o quarto cenário existe.
> **Consome o teto inteiro.** `@premissa P-11` (o desconto registrado é o concedido) e `P-12`
> (não há aplicação anônima) — **bloqueada por Q-02 e Q-03**

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Toda aplicação bem-sucedida deixa registrado quem aplicou, quando, e quanto de desconto

    Esquema do Cenário: [CT-25] a aplicação registra o autor, o instante, o total e o desconto
      Dado um cupom válido da organização do tipo "<tipo>" com valor <valor> e limite de 3 usos,
        criado às 12:00:00 de 15/09/2026
      E que o tempo avançou para 15/09/2026 14:30:00
      Quando o comprador Rui aplica o cupom sobre um total de <total> centavos
      Então existe exatamente um registro de uso desse cupom, com o autor Rui,
        o instante **14:30:00** de 15/09/2026, o total original <total> e o desconto <desconto>

      Exemplos:
        | tipo        | valor | total | desconto | # partição × efeito                                   |
        | porcentagem | 29    | 10000 | 2900     | trilha no ramo percentual                             |
        | fixo        | 3000  | 10000 | 3000     | trilha no ramo fixo — **desconto distinto do percentual** |
        | fixo        | 5000  | 3000  | 3000     | trilha do desconto **concedido**, não do nominal `@premissa P-11` |

    Esquema do Cenário: [CT-26] a recusa não registra uso nenhum
      Dado um cupom expirado da organização do tipo "<tipo>", com uso disponível
      Quando o comprador Rui tenta aplicar o cupom sobre um total de 10000 centavos
      Então a aplicação é recusada
      E não existe nenhum registro de uso para esse cupom
      E o contador de usos do cupom continua 0

      Exemplos:
        | tipo        | # partição do discriminador |
        | porcentagem | ramo percentual             |
        | fixo        | ramo de valor fixo          |

    Esquema do Cenário: [CT-27] falha ao registrar a trilha desfaz o consumo do uso
      Dado um cupom válido da organização do tipo "<tipo>", com limite de 3 usos e 0 usos feitos
      E que a gravação do registro de uso está impedida de concluir
      Quando o comprador Rui aplica o cupom sobre um total de 10000 centavos
      Então a aplicação falha
      E o contador de usos persistido continua 0

      Exemplos:
        | tipo        | # partição do discriminador |
        | porcentagem | ramo percentual             |
        | fixo        | ramo de valor fixo          |

    Cenário: [CT-41] o segundo uso do mesmo comprador também é consumido e registrado
      Dado o tempo em 15/09/2026 12:00:00 e um cupom válido da organização com limite de 3 usos,
        já aplicado uma vez pelo comprador Rui
      E que o tempo avançou para 15/09/2026 14:30:00
      Quando o comprador Rui aplica o mesmo cupom de novo, sobre um total de 10000 centavos
      Então o contador de usos persistido é 2, e resta um uso até o limite
      E existem **dois** registros de uso desse cupom, ambos com o autor Rui,
        um às 12:00:00 e outro às 14:30:00
```

> **CT-27 falha DEPOIS do ponto de efeito, e é isso que o torna um cenário de atomicidade.**
> Afirmar "nada foi registrado" num caminho de **pré-validação** — cupom expirado, código vazio —
> parece cobrir atomicidade e não distingue implementação nenhuma, porque ali nada seria registrado
> de qualquer forma. Esse falso ✅ é o cenário CT-26, que existe para outra coisa (o não-efeito na
> recusa) e **não** conta como atomicidade.
>
> Arnês de CT-27, tentado antes de escrever: derrubar a tabela da trilha (`Schema::drop`) depois de
> montar o cupom faz a inserção estourar **depois** do consumo, que é exatamente o ponto
> necessário. Alternativas equivalentes: `DB::statement` criando uma constraint que a inserção
> viola, ou um `Model::creating` que lança. Nenhuma delas depende de mock do produto.
>
> **A ausência de um cenário de "aplicação anônima"** é deliberada: RQ-15 exige "quem", e sem a
> resposta a Q-03 não se sabe se o motor **recusa** a chamada sem usuário ou **grava sem autor**.
> Escrever "aplicar sem usuário registra autor nulo" seria inventar requisito; escrever "recusa"
> seria inventar o outro. Registrado como lacuna **L-04**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M42 | o registro de uso nunca é criado (a chamada de gravação da trilha some) | CT-25 |
| M43 | a trilha é gravada antes de validar, então a recusa também registra | CT-26 |
| M44 | a trilha é gravada **fora** da transação do consumo | CT-27 |
| M45 | o autor não é gravado (fica sempre nulo) | CT-25 |
| M46 | o desconto registrado é o **valor nominal** do cupom, não o concedido | CT-25 (linha 5000 / 3000) |
| M47 | o ramo de valor fixo não escreve a trilha | CT-25, CT-26, CT-27 (linhas `fixo`) |
| M72 | a trilha é gravada com "primeiro registro por cupom e usuário": o **segundo** uso do mesmo comprador consome e não registra | CT-41 |
| M73 | o instante registrado é o da criação do cupom, ou o do início do teste, e não o da aplicação | CT-25 (o tempo avança entre o `Dado` e o `Quando`), CT-41 |

> **M72 é o segundo achado mais grave da revisão.** Nenhum cenário do conjunto original executava
> **duas aplicações bem-sucedidas**: todos os estados de contador maior que zero chegavam por
> fixture, nunca pela operação. Um "evitar linha duplicada" na trilha — que é uma coisa razoável
> de um dev escrever — deixaria RQ-15 cumprida só no primeiro uso de cada pessoa. **Estado
> alcançado por fixture não exercita a transição que o produziu.**
>
> **M73 é a mesma armadilha do tempo congelado**: com o cupom, o usuário e a aplicação todos no
> mesmo instante, gravar o instante *errado* é indistinguível de gravar o certo. O tempo precisa
> **avançar** entre o setup e a ação para o "quando" de RQ-15 virar oráculo.

---

## Regra R10 — Só quem tem permissão de escrita **cria, edita e exclui**; os demais **apenas listam**

> `RQ-07`, `RQ-08` · área A4 · perfil **padrão** · técnica: **matriz papel × ação**, com a ação
> destrutiva obrigatória · `@premissa P-02` e `P-09` (o "admin" de RQ-07 é o administrador da
> organização, no painel de negócio)

**Matriz papel × ação** — cinco papéis do kit × cinco ações:

| Papel | listar | ver | criar | editar | excluir | origem |
|---|---|---|---|---|---|---|
| `master_global` | ✅ | ✅ | ✅ | ✅ | ✅ | atravessa tudo pelo `Gate::before`, sem permission no banco |
| `admin_organizacao` | ✅ | ✅ | ✅ | ✅ | ✅ | matriz inteira do painel de negócio (**só existe com tenancy ligada**) |
| `panel_user` | ✅ | ✅ | ❌ | ❌ | ❌ | **é a célula que RQ-07 e RQ-08 pedem juntas** |
| `admin` (instalação) | ❌ | ❌ | ❌ | ❌ | ❌ | não alcança o painel de negócio |
| `infra` | ❌ | ❌ | ❌ | ❌ | ❌ | idem |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Só quem tem permissão de escrita cria, edita e exclui cupom

    Esquema do Cenário: [CT-28] a matriz de papéis dá escrita só a quem administra
      Dado um usuário com o papel "<papel>" na organização
      Quando o sistema verifica as permissões de cupom desse usuário
      Então a permissão de listar é "<listar>"
      E as permissões de criar, editar e excluir são "<escrita>"

      Exemplos:
        | papel             | listar    | escrita   | # célula                                     |
        | admin_organizacao | concedida | concedida | administra a organização                     |
        | panel_user        | concedida | negada    | **a célula central de RQ-07/RQ-08**          |
        | admin             | negada    | negada    | papel de outro painel `@premissa P-17` — **contradiz o `00`, ver Q-09** |
        | infra             | negada    | negada    | papel de outro painel                        |

    Cenário: [CT-29] o usuário comum que dispara a criação é barrado, não só privado do botão
      Dado um usuário comum da organização
      Quando ele abre diretamente a tela de criação de cupom
      Então o acesso é recusado com 403
      E nenhum cupom novo existe na organização

    Cenário: [CT-30] o usuário comum que dispara a exclusão é barrado e o cupom permanece
      Dado um usuário comum da organização e um cupom "PROMO29" existente
      Quando ele dispara a ação de excluir esse cupom por chamada direta ao componente,
        sem passar pelo botão
      Então a ação é recusada
      E o cupom "PROMO29" continua existindo, com o mesmo valor e o mesmo limite

    Cenário: [CT-47] o usuário comum que abre a edição de um cupom da própria organização é barrado
      Dado um usuário comum da organização e um cupom "PROMO29" da mesma organização
      Quando ele abre a tela de edição desse cupom
      Então o acesso é recusado com 403
      E o cupom "PROMO29" continua com o mesmo código, valor, validade e limite

    Cenário: [CT-45] no modo de instalação única, quem administra a instalação cadastra cupom
      Dado um usuário com o papel de administrador global, sem papel de organização,
        no modo de instalação única
      Quando ele submete o formulário de criação de um cupom "PROMO29"
      Então o cupom "PROMO29" existe, com o tipo, o valor, a validade e o limite informados
      E a listagem de cupons é acessível para ele
```

> **CT-29, CT-30 e CT-47 existem porque afirmar `can()` não é afirmar autorização.** Uma policy
> correta que a página **nunca consulta** passa em todo cenário de permissão e reprova em produção.
> Os três **disparam** a operação — criar, excluir e editar, que são exatamente os três verbos de
> RQ-07 — e é o que os separa de CT-28. A revisão adversarial pegou os dois buracos aqui: CT-30
> afirmava a **ausência do botão** (que é `can()` com outro nome, e passa com a rota aberta), e
> `editar` só existia como permissão consultada.
>
> **`master_global` ganhou cenário próprio (CT-45), e ele não é cerimônia.** Esse papel não tem
> permission no banco — o acesso vem do gate que atravessa tudo — então ele é invisível para
> qualquer cenário de permissão. E, com a tenancy desligada (**o default do kit**), ele é o **único**
> papel que escreve cupom, porque o `admin_organizacao` só é criado no modo multi-organização.
> Sem CT-45, o caminho de escrita do modo default não tinha nenhum cenário de autorização.
>
> ### Achado: a linha `admin` contradiz um argumento do próprio `00-requisito.md`
>
> O `00` defende a premissa P-02 dizendo, como terceiro dos seus três argumentos, que
> *"`master_global` e o papel `admin` continuam alcançando a tela por herança do `Gate::before`"*.
> Se isso for verdade, `admin` **escreve** cupom e a linha acima está errada. Se for falso — e a
> matriz de painéis do kit indica que é, porque o acesso a painel se decide pelo painel declarado
> no papel e só o papel global atravessa pelo gate —, então **um dos três argumentos que sustentam
> a leitura de RQ-07 no `00` não se sustenta**, e a premissa P-02 fica com dois.
>
> Não é uma questão de detalhe: RQ-07 diz literalmente *"só quem é **admin**"*, e existe um papel
> chamado exatamente `admin` que a premissa P-02 decidiu **não** ser o destinatário da cláusula. A
> derivação **não pode escolher** — vira a pergunta **Q-09**, e a linha fica `@premissa P-17`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M48 | o usuário comum recebe a matriz inteira do painel: cria e exclui cupom | CT-28 (linha `panel_user`), CT-29, CT-30 |
| M49 | o recorte subtrai a **entidade inteira** e o usuário comum perde também a listagem | CT-28 (linha `panel_user`, coluna listar) |
| M50 | autorização implementada só na visibilidade do botão; a rota e o componente continuam abertos | CT-29, CT-30, CT-47 |
| M51 | a exclusão sobra para o usuário comum (só criação e edição foram recortadas) | CT-30 |
| M74 | a **edição** sobra para o usuário comum (o recorte pegou criar e excluir, e esqueceu o verbo do meio) | CT-47 |
| M75 | o recorte de escrita é aplicado por papel e alcança também quem administra a instalação: no modo de instalação única **ninguém** cadastra cupom | CT-45 |

---

## Regra R11 — Cupom de outra organização não é visto, não é aplicado e **não bloqueia o código**

> `RQ-14` · área A4 · perfil **padrão** · técnica: **IDOR / autorização horizontal** + unicidade
> escopada · `@premissa P-04`

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O cupom pertence a uma organização e não atravessa a fronteira dela

    Cenário: [CT-31] duas organizações podem ter o mesmo código
      Dado um cupom "BLACKFRIDAY" na organização Globex
      Quando a administradora da organização Acme cadastra um cupom "BLACKFRIDAY"
      Então o cadastro é aceito
      E a Acme tem um cupom "BLACKFRIDAY" e a Globex continua com o dela
      E a listagem da Acme mostra apenas o cupom da Acme

    Cenário: [CT-32] o código de outra organização não é aplicável
      Dado um cupom válido "DAGLOBEX" na organização Globex, com 0 usos
      Quando o comprador da organização Acme informa o código "DAGLOBEX"
      Então o resultado é recusado
      E o contador de usos do cupom da Globex continua 0
      E nenhum registro de uso existe para esse cupom

    Cenário: [CT-33] a tela de edição não alcança o cupom de outra organização pela URL
      Dado um cupom "DAGLOBEX" na organização Globex
      Quando a administradora da organização Acme abre a URL de edição desse cupom
      Então a página responde 404
      E o cupom da Globex continua com o mesmo código, valor e limite

    Cenário: [CT-43] o vínculo com a organização não vem do formulário
      Dado que a administradora da organização Acme preenche um cupom "PROMO29"
      Quando ela submete o formulário enviando também o identificador da organização Globex
      Então o cupom "PROMO29" pertence à Acme
      E a Globex continua com a mesma quantidade de cupons de antes
```

> CT-32 e CT-33 são o par de IDOR: **dois usuários de duas organizações no setup**, um pedindo o
> recurso do outro. CT-33 monta a URL com o identificador público do registro (o `uuid`, não o id
> sequencial — `TemUuid::getRouteKeyName()`), que é o que o `{record}` das rotas do Resource usa.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M52 | unicidade **global** do código, sem escopo de organização | CT-31 |
| M53 | validação de unicidade que não passa pelo Eloquent e por isso ignora o escopo | CT-31 |
| M54 | a busca do código na aplicação consulta sem o escopo da organização | CT-32 |
| M55 | o vínculo da rota resolve o registro sem escopo: a edição alcança a outra organização | CT-33 |
| M76 | o vínculo com a organização é campo de escrita em massa: um payload forjado cria cupom **dentro da organização alheia** | CT-43 |

> **Estouro do teto declarado**: R11 é perfil `padrão` (teto 3) e tem 4 cenários. CT-43 entrou pela
> revisão adversarial e o gate vence o teto. O motivo de ele ter escapado é instrutivo: o conjunto
> tinha três cenários de isolamento — ler, aplicar e editar — **todos na direção da leitura**. O
> único cenário de escrita em massa (CT-07) forjava o contador de usos. Isolamento testado só na
> leitura deixa a escrita aberta, e é a direção em que o dano é maior: não é ver o dado do vizinho,
> é **plantar** dado dentro dele.

---

## Regra R12 — Quem não escreve vê **só os ativos**, e a situação exibida deriva da validade e do limite

> `RQ-08` · área A5 · perfil **mínimo** · técnica **escalada** a **EP exaustiva do enum de
> situação** · `@premissa P-03` ("ativo" é derivado, não é interruptor) e `P-13` (precedência) —
> **bloqueada por Q-04**

> Quando o usuário vê um rótulo derivado de estado, **toda partição é obrigatória** — não se
> amostra. As quatro combinações de contador × validade estão nas quatro linhas.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: A situação exibida deriva da validade e do limite, e o usuário comum vê só os ativos

    Esquema do Cenário: [CT-34] as quatro combinações de contador e validade, para quem só lê
      Dado o tempo congelado em 15/09/2026 12:00:00
      E um cupom da organização com limite de 3 usos, <ja_usado> usos feitos
        e validade "<validade>"
      Quando o usuário comum abre a listagem de cupons
      Então o cupom "<visivel>" na listagem

      Exemplos:
        | ja_usado | validade            | visivel     | # partição / fronteira                        |
        | 2        | 15/09/2026 12:00:01 | aparece     | com uso e 1 segundo de validade — borda+1     |
        | 2        | 15/09/2026 11:59:59 | não aparece | com uso, expirou há 1 segundo — **borda−1**   |
        | 3        | 15/09/2026 23:59:59 | não aparece | limite atingido, validade folgada             |
        | 3        | 15/09/2026 11:59:59 | não aparece | as duas causas juntas                         |

    Esquema do Cenário: [CT-44] o rótulo da situação usa a mesma fronteira de instante que a aplicação
      Dado o tempo congelado em 15/09/2026 12:00:00
      E um cupom da organização com limite de 3 usos, <ja_usado> usos feitos
        e validade "<validade>"
      Quando a administradora da organização abre a listagem de cupons
      Então a situação exibida desse cupom é "<situacao>"

      Exemplos:
        | ja_usado | validade            | situacao | # partição do enum                                  |
        | 2        | 15/09/2026 12:00:01 | Ativo    | com uso e 1 segundo de validade                     |
        | 2        | 15/09/2026 11:59:59 | Expirado | **expirou há 1 segundo, e o rótulo já sabe disso**  |
        | 3        | 15/09/2026 23:59:59 | Esgotado | limite atingido — borda do contador                 |
        | 3        | 15/09/2026 11:59:59 | Esgotado | esgotado **e** expirado: precedência `@premissa P-13`|

    Cenário: [CT-35] quem pode editar vê também os cupons inativos
      Dado uma organização com um cupom ativo, um expirado e um esgotado
      Quando a administradora da organização abre a listagem de cupons
      Então os três cupons aparecem na listagem
```

> **Estouro do teto declarado**: o perfil `mínimo` prevê 1 cenário por regra, e esta tem 2. CT-35
> é o que separa "a listagem esconde os inativos de quem não escreve" de "a listagem esconde os
> inativos de todo mundo" — o segundo quebra RQ-01, porque a administradora perderia o acesso aos
> cupons que ela precisa corrigir, e **CT-34 fica inteiramente verde nas duas**. [O gate do passo 6
> vence o teto](#): mutante vivo é pior que cenário a mais.
>
> As duas primeiras linhas de CT-34 usam **2 e 3** contra um limite de 3, e não 1 e 10: é a
> diferença entre discriminar `>=` de `>` e não discriminar nada.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M56 | o recorte de listagem é aplicado a **todos**, inclusive a quem escreve | CT-35 |
| M57 | recorte ausente: o usuário comum vê expirado e esgotado | CT-34 (linhas `não aparece`) |
| M58 | a situação deriva só da validade: o esgotado aparece como "Ativo" | CT-44 (linha 3 / 23:59:59) |
| M59 | `>` em vez de `>=` na comparação do contador: o limite exato exibe "Ativo" | CT-44 (linha 3 / 23:59:59) |
| M77 | a listagem e o rótulo comparam **dia** enquanto a aplicação compara instante: o cupom vencido hoje de manhã fica "Ativo" na tela o dia inteiro e é recusado na aplicação | CT-34 e CT-44 (linhas de 11:59:59) |
| M78 | a precedência é a inversa (a expiração é testada primeiro) e o cupom esgotado-e-expirado é rotulado "Expirado" | CT-44 (última linha) |

> **M77 e M78 foram os achados da revisão nesta regra, e os dois vinham do mesmo defeito de
> derivação: `futuro` e `passado` não são valores.** Com dias de distância entre as partições,
> uma listagem que compara dia e uma aplicação que compara instante concordam em todos os
> cenários — e divergem exatamente no dia em que um cupom vence, que é o único dia que importa.
> É a divergência de "duas fontes de verdade" que a premissa P-03 do `00` foi escrita para
> impedir, e o conjunto não a teria pego.
>
> **M78 estava vivo por um `Então` que se autodesligava**: CT-34 dizia *"a situação exibida é
> `<situacao>` **quando ele aparece**"* — e as três linhas com rótulo não-trivial eram justamente
> as que não apareciam. A cláusula condicional esvaziava o oráculo nas únicas linhas que o
> exerciam. Separar a visibilidade (CT-34, persona que só lê) do rótulo (CT-44, persona que vê
> tudo) resolve: cada cenário tem uma persona para a qual o seu `Então` é sempre verificável.

---

## Regra R13 — Cupom **excluído** deixa de funcionar em toda operação, e cada operação tem um caminho válido

> `RQ-01`, `RQ-07`, `RQ-15` · áreas A3+A5, herda **completo** · técnica: **tabela estado ×
> operação** · `@premissa P-15` (exclusão física) e `P-16` (a trilha sobrevive) — **bloqueada por
> Q-07**

**Tabela estado × operação** — as colunas são **todas** as operações, não só a leitura. Toda célula
tem um CT, e cada coluna tem **ao menos uma célula válida exercitada**:

| Estado \ Operação | aplicar | editar | excluir | listar (usuário comum) |
|---|---|---|---|---|
| **Ativo** | ✅ CT-22 | ✅ CT-04 | ✅ CT-38 (linha `ativo`) | ✅ CT-34 |
| **Expirado** | ❌ CT-17 (D2) | ✅ **CT-37** | ✅ CT-38 (linha `expirado`) | ❌ CT-34 |
| **Esgotado** | ❌ CT-17 (D3) | ✅ **CT-46** | ✅ CT-38 (linha `esgotado`) | ❌ CT-34 |
| **Excluído** | ❌ CT-36 | ❌ CT-48 | ❌ CT-48 | ❌ CT-48 |

> Três células desta tabela estavam apoiadas em alegação de semelhança, e a revisão adversarial as
> derrubou: `Esgotado × editar` dizia "CT-37 (mesma via)" — e CT-37 edita um cupom **expirado**;
> `Expirado × excluir` e `Esgotado × excluir` apontavam para um CT-38 que exercitava só um cupom
> **ativo**. **"Mesma via" não é cenário.** As três viraram CT-46 e as linhas novas de CT-38.

> **A metade que quase sempre escapa é a de baixo à direita e a coluna `editar`.** "Toda célula
> vazia vira cenário negativo" deixaria a coluna `editar` com três recusas e **nenhuma edição que
> funciona** — e a armadilha da unicidade contra o próprio registro (CT-04) passaria inteira. A
> célula válida de `editar` está em CT-04 (estado Ativo) e em CT-37 (estado Expirado); a de
> `excluir`, em CT-38.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cupom excluído deixa de funcionar em toda operação

    Esquema do Cenário: [CT-36] o cupom excluído não é aplicável por via nenhuma
      Dado um cupom "PROMO29" da organização que já foi excluído
      Quando o comprador aplica o cupom "<via>"
      Então a aplicação é recusada
      E nenhum registro de uso é criado para esse cupom

      Exemplos:
        | via                     | # célula                                                    |
        | informando o código     | o código não é mais encontrado                              |
        | pela referência em mãos | **quem já tinha o cupom carregado não passa pela busca**    |

    Esquema do Cenário: [CT-48] o cupom excluído não responde às operações de tela
      Dado um cupom "PROMO29" da organização que já foi excluído
      Quando a administradora da organização executa a operação "<operacao>"
      Então o resultado é "<resultado>"

      Exemplos:
        | operacao                        | resultado | # célula                                 |
        | abrir a tela de edição pela URL | 404       | rota do registro inexistente             |
        | excluir de novo                 | 404       | segunda exclusão não estoura em erro     |
        | abrir a listagem                | o cupom "PROMO29" não aparece | some para quem vê tudo |

    Cenário: [CT-37] o cupom cuja validade foi corrigida é aplicável, e o consumo anterior conta
      Dado um cupom da organização expirado, com limite de 3 usos e 2 usos já feitos
      E que a administradora da organização já corrigiu a validade para 30/09/2026 23:59
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então a aplicação é aceita
      E o contador de usos persistido é 3, e não resta nenhum uso até o limite

    Cenário: [CT-46] elevar o limite de um cupom esgotado o devolve ao uso sem zerar o contador
      Dado um cupom válido da organização com limite de 3 usos e 3 usos já feitos
      E que a administradora da organização já elevou o limite para 5
      Quando o comprador aplica o cupom sobre um total de 10000 centavos
      Então a aplicação é aceita
      E o contador de usos persistido é 4, e resta **um** uso até o limite

    Esquema do Cenário: [CT-38] excluir o cupom libera o código, em qualquer estado
      Dado um cupom "PROMO29" da organização no estado "<estado>", já usado uma vez
      Quando a administradora da organização exclui o cupom
      Então o cupom "PROMO29" não existe mais na organização
      E cadastrar um cupom novo com o código "PROMO29" é aceito

      Exemplos:
        | estado   | # célula da coluna `excluir` |
        | ativo    | estado corrente              |
        | expirado | fora da validade             |
        | esgotado | sem uso disponível           |

    Cenário: [CT-39] excluir o cupom não apaga a trilha de quem o usou
      Dado um cupom da organização com um registro de uso do comprador Rui
      Quando a administradora da organização exclui o cupom
      Então o registro de uso do Rui continua existindo, com o autor, o instante e o desconto
```

> **CT-37 é o cenário de ciclo de volta (2-switch) desta feature.** Um cupom expirado editado
> reentra no estado aplicável, e o defeito mora no que o ciclo novo herda: uma implementação que
> "reativa" o cupom zerando o contador devolve **três** usos a quem já gastou dois. Cobrir a
> transição `expirado → editado` sozinha não vê isso; o oráculo tem de ser sobre o **segundo
> giro** — quantos usos restam depois da correção.
>
> **CT-39 é o cenário de maior consequência desta regra, e ele está `@premissa`.** RQ-15 pede
> registro "pra gente conseguir auditar **depois**". Se a exclusão do cupom leva a trilha junto, a
> evidência desaparece exatamente quando alguém tem motivo para apagar o cupom. Se a resposta a
> Q-07 for "a trilha vai junto", este cenário inverte — e RQ-15 precisa ser reescrita, porque
> "auditar depois" deixa de ser verdade.
>
> **A linha `aplicar pela referência em mãos` de CT-36** é a que distingue uma barreira no banco de
> uma barreira na consulta por código: quem já carregava o cupom em memória não passa pela busca, e
> um consumo que só confere o código continua funcionando sobre um registro que não existe mais.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M60 | o consumo não confere a existência do registro: a referência em mãos ainda aplica | CT-36 (linha `pela referência em mãos`) |
| M61 | a segunda exclusão estoura em erro de servidor em vez de responder 404 | CT-48 (linha `excluir de novo`) |
| M62 | a edição da validade **zera o contador de usos** ("reativar" o cupom) | CT-37 |
| M63 | a exclusão do cupom apaga a trilha de uso | CT-39 |
| M64 | a exclusão é lógica e o código continua bloqueado no índice único | CT-38 |
| M79 | elevar o limite de um cupom esgotado **zera o contador** — o segundo giro devolve 5 usos a quem já gastou 3 | CT-46 |

> **CT-37 e CT-46 são o par de ciclo de volta (2-switch), e a revisão mostrou que um só não
> bastava.** São **duas** portas de reentrada distintas — corrigir a validade e elevar o limite —
> e cada uma tem o seu próprio jeito de "reativar" o cupom zerando o que o ciclo anterior deixou.
> M62 morria só pela primeira; M79 vivia inteiro. Os dois cenários também foram reescritos para
> pôr o **segundo evento** no `Quando`: antes a correção era o `Quando` e a aplicação vinha
> escondida dentro do `Então` ("o cupom passa a ser aceito na aplicação"), que é um segundo
> `Quando` disfarçado de asserção — e que não afirma quantos usos restam.

---

## Lacunas Declaradas

| # | Lacuna | O que foi tentado | Destino |
|---|---|---|---|
| **L-01** | **Idempotência do total do pedido** (mutante M28). O agregado que sofre o efeito é o pedido, e ele **não existe** neste projeto (premissa P-01 do `00`). Afirmar sobre o **contador do cupom** provaria contabilidade, não idempotência; afirmar sobre o **valor devolvido** por duas chamadas independentes passa **por construção**, porque o cálculo é uma função do total informado — o mutante "acumula" não é sequer expressável ali | ancorar no cupom (rejeitado: prova contabilidade); ancorar no retorno de duas chamadas (rejeitado: tautológico); procurar um agregado persistido no escopo (não existe — nenhuma coluna monetária no projeto) | **cenário NÃO escrito.** Pergunta **Q-08 / A-18**. Idempotência que não se pode ancorar não é lacuna do conjunto: é consequência de uma decisão de escopo que alguém precisa confirmar |
| **L-02** | **Teto do desconto fixo** (mutante M29). Um valor fixo além do range da coluna inteira estoura em erro de banco em vez de recusar com mensagem, e o requisito não dá teto nenhum | escrever a fronteira superior do `fixo` (impossível: não há fronteira definida). Escrever "estoura" como oráculo seria testar a implementação | pergunta **Q-08 / A-17** |
| **L-03** | **Concorrência real com duas conexões** (mutante M41). CT-24 falsifica o consumo por leitura obsoleta, mas não uma implementação atômica só dentro de uma transação otimista | duas conexões sobre SQLite `:memory:` (o banco de teste é privado ao processo e não sustenta a segunda conexão); transação aninhada (não simula a disputa); a técnica da instância obsoleta (adotada — cobre o caso que importa e é o precedente do projeto em `ConviteUsuarioExistenteTest.php:201`) | **lacuna declarada.** Fechá-la exigiria banco de teste com conexão real (MySQL em CI) — decisão de infra, fora do escopo desta feature |
| **L-04** | **Aplicação sem usuário identificado.** RQ-15 exige "quem"; o requisito não diz se a chamada sem usuário é recusada ou gravada sem autor | derivar o cenário nas duas direções (cada uma inventaria requisito diferente) | pergunta **Q-03 / A-12** |

---

## Checklist de Taxonomia

> Resposta válida: **um ID de cenário**, **`não se aplica: {motivo}`** ou **`lacuna declarada:
> {o que foi tentado}`**. Nunca "sim", nunca "parcialmente coberto".

| Item | Cenário que mata |
|---|---|
| **IDOR / autorização horizontal** (recurso de outro usuário por `{id}`) | leitura CT-32, CT-33 · **escrita CT-43** |
| **Autorização exercida na ação**, não só verificada por permissão | criar CT-29 · excluir CT-30 · **editar CT-47** — os três verbos de RQ-07 |
| **Idempotência ancorada no agregado persistido** | **lacuna declarada L-01**: o agregado (pedido) está fora de escopo por P-01. Tentado ancorar no cupom (prova contabilidade), no retorno de duas chamadas (tautológico) e num agregado persistido alternativo (não existe). Pergunta Q-08. *A dupla submissão do formulário foi retirada daqui pela revisão adversarial: ela mata o mesmo mutante que CT-09 e não é idempotência* |
| **Concorrência** (contador, limite) | CT-24 (leitura obsoleta) · **lacuna declarada L-03** para duas conexões reais: tentado `:memory:` com segunda conexão e transação aninhada |
| **Fronteira no ponto de entrada** (gravação, não só uso) | CT-01, CT-03, CT-05, CT-11, CT-13, CT-14, CT-42 |
| **Domínio condicionado** (tipo × valor) | CT-01 (criação) · CT-05 (edição do dependente) · **CT-40 (edição do discriminador)** |
| **Criação ≠ edição ≠ uso** — as três derivações existem **em cada eixo** | domínio: CT-01/CT-42 · CT-05/CT-40/CT-42 · CT-15…CT-17 — normalização: CT-08 (criação) · CT-08 (edição) · **CT-20 (uso)** — unicidade: CT-09 · CT-06 · não se aplica ao uso — autorização: CT-29 · CT-47 · CT-30 |
| **Unicidade contra o próprio registro** (armadilha só da edição) | CT-04 |
| **Validação que só roda na criação** (armadilha só da edição) | CT-05, CT-14, CT-42 (linha `edição`) |
| **Estado × operação de escrita** (o excluído ainda funciona?) | CT-36 (aplicar), CT-48 (tela) |
| **Célula válida por coluna da matriz de estados** | aplicar CT-22 · editar CT-04 (ativo), **CT-37 (expirado), CT-46 (esgotado)** · excluir **CT-38, nos três estados** · listar CT-34 |
| **Ciclo de volta / 2-switch** | CT-37 (reentrada por validade) · **CT-46 (reentrada por limite)** · **CT-41 (segundo uso bem-sucedido)** |
| **Estado exibido: partição exaustiva do enum** | **CT-44** — 4 de 4 combinações, com a persona que enxerga **todos** os estados, para o `Então` não se autodesligar nas linhas invisíveis. CT-34 cobre a visibilidade, que é outra pergunta |
| **Ausente ≠ nulo ≠ vazio** | CT-20 (as três, com semântica declarada: todas recusam — não há campo opcional) · CT-03 (ausência na gravação) |
| **Paginação** | `não se aplica: RQ-08 pede "listar"; o requisito não menciona volume, página nem quantidade por página, e a área A5 é perfil mínimo. Se aparecer requisito de volume, a linha vira cenário` |
| **Ordenação por coluna** | `não se aplica: a ordem default é escolha do plano e foi recusada como oráculo (pergunta Q-06). Coluna inexistente por injeção não é alcançável pela superfície desta entrega — não há parâmetro de ordenação em rota` |
| **Timezone / virada de dia / DST** | CT-21 (fuso do app × banco), CT-13 e CT-18 (fronteira de instante na gravação e no uso), **CT-34 e CT-44 (a mesma fronteira na listagem e no rótulo)** · DST: `não se aplica: app em UTC e o Brasil não tem horário de verão desde 2019` |
| **`date` comparado com `datetime`** | gravação CT-13 (linhas de 23:59:59) · uso CT-18 · **estado derivado CT-34, CT-44 (linhas de 11:59:59)** — o item era verdadeiro só na gravação até a revisão |
| **Unicode / acento / limite de tamanho** | escrita CT-11 (acento, emoji de 4 bytes, borda de 40 e 41 em ASCII **e acentuada**, só espaços) · **leitura CT-20 (linha `" cupão10 "`)** |
| **Espaços nas bordas** | CT-08, CT-09, CT-11, CT-20 |
| **Unicidade + exclusão** (criar → excluir → recriar) | CT-38, nos três estados |
| **CRUD combinado** (ler/editar/excluir inexistente; excluir duas vezes; editar sem alterar nada) | CT-48 (inexistente e dupla exclusão), CT-04 (editar sem alterar nada) |
| **Mass assignment** (campo não previsto no payload) | CT-07 (contador de usos) · **CT-43 (vínculo com a organização)** — o item cobria só o primeiro até a revisão |
| **Upload** | `não se aplica: a feature não tem arquivo` |
| **Precisão monetária** (centavos inteiros, nunca `float`; arredondamento na borda de centavo) | CT-15 (29% de 10.000 distingue inteiro de `float`; 10% de 9.999 e 5% de 50 distinguem truncar de arredondar; 29% de 1.049 distingue a ordem das operações; 100% de 1 exercita o piso do ramo percentual), CT-16 (centavos × reais, piso zero) |
| **Efeito colateral: aconteceu / não aconteceu / uma só vez / atômico** | aconteceu CT-22, CT-25 · não aconteceu CT-23, CT-26 · uma só vez CT-24 · **repetido, e ainda registrado, CT-41** · atômico CT-27 |
| **Partição do discriminador × cada efeito rastreado** | consumo CT-22, CT-23, CT-24 · trilha CT-25, CT-26, CT-27 · **validação CT-17 (linhas `fixo`)** — a revisão mostrou que R7 inteiro rodava só com cupom percentual |
| **Estado alcançado pela operação, não só por fixture** | CT-41 (segundo uso), CT-37 e CT-46 (reentrada). *Todos os estados de contador > 0 chegavam por fixture antes da revisão — e transição que nenhum cenário percorre é transição que ninguém testou* |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|---|---|---|---|---|---|---|
| CT-01 | domínio de `valor` por tipo, na criação | R1 | decisão + BVA | componente | `tests/Tenancy/CupomTenancyTest.php` | M1, M2, M3 |
| CT-02 | criação grava os cinco campos (**gate de tela de escrita**) | R1 | EP | componente | idem | M4 |
| CT-03 | os cinco campos são obrigatórios | R1 | EP | componente | idem | M5 |
| CT-04 | salvar sem alterar o código passa | R2 | armadilha da edição | componente | idem | M7 |
| CT-05 | domínio revalidado no salvamento | R2 | EP na edição | componente | idem | M6 |
| CT-06 | código duplicado na edição, em caixa diferente | R2 | normalização | componente | idem | M8 |
| CT-07 | contador não é alterável pelo formulário | R2 | mass assignment | componente | idem | M9 |
| CT-08 | código normalizado na criação e na edição | R3 | normalização | componente | idem | M11, M12 |
| CT-09 | código não se repete na organização | R3 | unicidade | componente | idem | M11, M13 |
| CT-11 | acento, emoji e limite de 40 em caracteres × bytes | R3 | normalização + BVA de string | componente | idem | M10, M14, M68 |
| CT-12 | duplicata barrada fora do formulário | R3 | unicidade | Feature | `tests/Kit/CupomTest.php` | M15 |
| CT-13 | fronteira da validade na criação | R4 | BVA 1 s | componente | `tests/Tenancy/CupomTenancyTest.php` | M16, M18, M19 |
| CT-14 | validade no passado recusada na edição | R4 | EP na edição | componente | idem | M17 |
| CT-15 | percentual truncado (7 exemplos discriminantes) | R5 | BVA + discriminância | Feature | `tests/Kit/CupomTest.php` | M20, M21, M22, M23 |
| CT-16 | fixo em centavos e piso zero | R6 | EP + BVA | Feature | idem | M24, M25, M26, M27 |
| CT-17 | as três validações juntas (tabela de decisão) | R7 | decisão | Feature | idem | M32, M33 |
| CT-18 | validade no instante | R7 | BVA 1 s | Feature | idem | M30, M35 |
| CT-19 | limite exclusivo na borda | R7 | BVA 1 | Feature | idem | M31 |
| CT-20 | código ausente, nulo, vazio, inexistente, normalizado | R7 | EP | Feature | idem | M34 |
| CT-21 | validade no fuso do app × banco em UTC | R7 | tempo | Feature | idem | M35 |
| CT-22 | aplicar consome um uso (2 tipos) | R8 | rastreio de efeito | Feature | idem | M36, M40 |
| CT-23 | esgotado não consome (2 tipos) | R8 | rastreio de efeito | Feature | idem | M37, M39, M40 |
| CT-24 | disputa consome um uso só (2 tipos) | R8 | concorrência | Feature | idem | M38, M39, M40 |
| CT-25 | trilha com autor, instante, total e desconto (3 linhas) | R9 | rastreio de efeito | Feature | idem | M42, M45, M46, M47 |
| CT-26 | recusa não registra uso | R9 | rastreio de efeito | Feature | idem | M43 |
| CT-27 | falha na trilha desfaz o consumo (**atomicidade**) | R9 | rastreio de efeito | Feature | idem | M44 |
| CT-28 | matriz papel × ação | R10 | matriz | Feature | `tests/Tenancy/CupomTenancyTest.php` | M48, M49 |
| CT-29 | criação disparada pelo usuário comum é barrada | R10 | matriz | componente | idem | M48, M50 |
| CT-30 | exclusão disparada pelo usuário comum é barrada | R10 | matriz | componente | idem | M48, M51 |
| CT-31 | mesmo código em duas organizações | R11 | unicidade escopada | componente | idem | M52, M53 |
| CT-32 | código de outra organização não é aplicável | R11 | IDOR | Feature | idem | M54 |
| CT-33 | URL de edição não alcança outra organização | R11 | IDOR | componente | idem | M55 |
| CT-34 | 4 combinações de situação × visibilidade | R12 | EP exaustiva | componente | idem | M57, M58, M59 |
| CT-35 | quem escreve vê os inativos | R12 | EP | componente | idem | M56 |
| CT-36 | cupom excluído não é aplicável por via nenhuma | R13 | estado × operação | Feature | idem | M60 |
| CT-37 | corrigir a validade não zera o contador (**2-switch**) | R13 | estado × operação | Feature | idem | M62 |
| CT-38 | excluir libera o código, nos três estados | R13 | unicidade + exclusão | componente | idem | M64 |
| CT-39 | excluir não apaga a trilha | R13 | estado × operação | Feature | `tests/Kit/CupomTest.php` | M63 |
| **CT-40** | trocar o tipo revalida o valor contra o domínio novo | R2 | decisão na edição | componente | `tests/Tenancy/CupomTenancyTest.php` | **M67** |
| **CT-41** | o segundo uso também é consumido e registrado (**2-switch no uso**) | R9 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | **M72, M73** |
| **CT-42** | domínio do limite de usos, na criação e na edição | R1 | BVA 1 | componente | `tests/Tenancy/CupomTenancyTest.php` | **M65, M66** |
| **CT-43** | o vínculo com a organização não vem do formulário | R11 | IDOR de escrita | componente | idem | **M76** |
| **CT-44** | o rótulo da situação na mesma fronteira de instante | R12 | EP exaustiva | componente | idem | **M58, M59, M77, M78** |
| **CT-45** | administrador global cadastra no modo de instalação única | R10 | matriz papel × ação | componente | `tests/Kit/CupomTest.php` | **M75** |
| **CT-46** | elevar o limite de um esgotado não zera o contador (**2-switch**) | R13 | estado × operação | Feature | `tests/Tenancy/CupomTenancyTest.php` | **M79** |
| **CT-47** | edição disparada pelo usuário comum é barrada | R10 | matriz papel × ação | componente | idem | **M74, M50** |
| **CT-48** | cupom excluído nas operações de tela | R13 | estado × operação | componente | idem | **M61** |

> **CT-36/CT-48 e CT-37/CT-46 foram separados por camada** na revisão: as operações de tela (404,
> listagem) são de componente, as de aplicação são de Feature. Antes estavam num cenário só, com
> um `Então` comum ("nenhum registro de uso é criado") que era **vazio por construção** nas linhas
> de tela — três linhas em que o oráculo não afirmava nada.

### Cogitado e cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| "o desconto devolvido é um inteiro" | tautologia: o tipo já é garantido pela linguagem. É a assertion que a skill lista como proibida como oráculo único |
| "aplicar não envia e-mail / não enfileira job" | a feature não envia nem enfileira (fora de escopo declarado no `00`). Cenário que prova a ausência de um efeito que não existe fica verde para sempre |
| "o log registra o motivo da recusa" | log foi recusado como oráculo (ver `## Fronteira com o Plano`) |
| "33% de 10.001" como exemplo de ordem das operações | **não discrimina** — as duas ordens dão 3.300. Substituído por 29% de 1.049 |
| **CT-10 — "submeter o formulário de criação duas vezes cria um cupom só"** | cortado **pela revisão adversarial**. Mata o mesmo mutante que CT-09 (o índice único), tem duas ações num `Quando`, e o `Então` não diz o que a segunda submissão devolve. Estava sendo usado como âncora do item "idempotência" do checklist — um falso ✅, porque idempotência de escrita contra um índice único é a própria unicidade com outro nome. O item virou `lacuna declarada L-01`, que é a verdade |
| "1% de 100 → 1" no `Exemplos:` de CT-15 | divisão exata sobre total múltiplo de 100: não separa ordem de operações nem truncamento. A linha `1% de 99 → 0` faz o trabalho sozinha |
| "validade em 14/09 23:59:59" no `Exemplos:` de CT-13 | mesma partição da linha `11:59:59`, sem fronteira nova |
| "o tipo aceita só dois valores" | garantido pelo tipo do enum, não por comportamento derivável do requisito. Um terceiro valor não é alcançável pela superfície |
| "listar 0, 1 e muitos cupons" (paginação) | perfil mínimo em A5, requisito sem menção a volume. Registrado como `não se aplica` no checklist, com o gatilho de reavaliação |
| "editar o cupom de outra organização pelo componente, sem URL" | mata o mesmo mutante que CT-33, que é o caminho real |

## Fechamento do Ciclo com Mutation Testing

```bash
composer require pestphp/pest-plugin-mutate --dev   # hoje é só transitivo — ver divergência 3
vendor/bin/pest tests/Kit/CupomTest.php --mutate --path=app/Models --min=70
```

- Exige driver de cobertura. O ambiente **não tem PCOV** (`.ai/rules/testes-browser.md`), então é
  Xdebug com `XDEBUG_MODE=coverage`, escopado ao arquivo — mutar o projeto inteiro aqui não termina.
- `--path=` e não `--class=`: o filtro por classe não casa de forma confiável.
- **O score não responde por omissão.** Os mutantes que mais importam nesta feature — validade
  gravável no passado (M16, M17), trilha apagada na exclusão (M63), contador zerado na edição
  (M62) — são **comportamentos ausentes**: não há linha para mutar, e o score não cai. Quem
  responde por eles é a rastreabilidade `RQ` → regra → cenário deste arquivo.
- Mutante sobrevivente vira lacuna de derivação e cenário novo, não "ajuste de teste".
