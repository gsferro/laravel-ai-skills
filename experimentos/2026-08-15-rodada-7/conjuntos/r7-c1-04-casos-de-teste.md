# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação — ela
> ainda não existe. O `01-plano-acao.md` entrou apenas para paths, rotas, suítes e a tabela
> `## Superfície de UI`; o que foi recusado como oráculo está em [Fronteira com o Plano](#fronteira-com-o-plano).
>
> **Este arquivo passou por uma rodada de revisão adversarial** (sub-agente independente, que recebeu
> só o `00`, o `04` e o `05` — nunca o PRD, o código ou o raciocínio de quem derivou). Ela produziu
> **35 achados**, e o que virou cada um está em [Revisão Adversarial](#revisão-adversarial).
> **Cinco mapeamentos de mutante eram falsos** e foram corrigidos; **três auditorias que o documento
> fazia de si mesmo estavam erradas** e foram refeitas.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Justificativa da nota |
|---|---|---|---|---|---|
| A1 — cálculo do desconto | 3 | 3 | **9** | **completo** | domínio condicionado (`tipo` decide a unidade de `valor`), truncamento, piso em zero; impacto é **dinheiro** |
| A2 — consumo do uso e limite | 3 | 3 | **9** | **completo** | contador com corrida entre duas escritas; impacto é dinheiro e **irreversível** (uso consumido não volta) |
| A3 — autorização | 3 | 3 | **9** | **completo** | altera `database/seeders/PapeisSeeder.php`, que é **infra compartilhada** dos cinco papéis; impacto é autorização |
| A4 — validade temporal | 2 | 3 | 6 | **padrão** | integra com o relógio da aplicação; impacto é dinheiro (cupom vencido aceito) |
| A5 — cadastro (código, tipo, domínios, unicidade) | 2 | 3 | 6 | **padrão** | integra com o Filament e com o escopo de tenant; unicidade errada **vaza a existência de cupom de outro cliente** |
| A6 — trilha de auditoria (RQ-15) | 2 | 3 | 6 | **padrão** | efeito colateral em transação; impacto é compliance/auditoria |
| A7 — listagem e rótulo exibido | 1 | 2 | 2 | **mínimo** | leitura de dezenas de linhas; erro custa retrabalho manual, não dinheiro |

- **Técnica escalada acima do perfil da área** (permitido; rebaixar não é):
  - **A4** (`padrão`, previa BVA 2-valores) → **BVA 3-valores** em `expira_em`. Motivo: com dois valores
    não se distingue `>` de `>=` no instante exato de expiração, e essa é a única fronteira que o
    requisito nomeia para a validade.
  - **A6** (`padrão`) → **rastreio de efeito completo (4 direções, com atomicidade)**. Motivo: a trilha
    é gravada dentro da mesma transação do contador, e a direção "atomicidade" é a única que separa
    *contador movido com trilha* de *contador movido sem trilha*.
- Técnicas aplicadas: EP, BVA 3-valores, tabela de decisão, **matriz estado × operação** (produto
  cartesiano fechado), matriz papel × verbo, rastreio de efeito, normalização, 2-switch.
- **Cenários: 58** no `04` (CT-00…CT-57, sem buraco de numeração) + **2** no `05` · **Regras: 13** ·
  **Mutantes previstos: 105** (97 no `04` + 8 no `05`) · **Perguntas abertas: 12** (Q-01…Q-12) ·
  **Lacunas declaradas ativas: 6** (L-02…L-07 — a **L-01 foi fechada**, virando CT-53)
- **Um único mutante previsto está sem cenário matador**: **M6.3** (recorte de permissão por
  substring atingindo uma entidade futura) → **L-06**. Os outros 104 têm matador nomeado. As demais
  lacunas são de **arnês** (L-02, L-03), de **mecanismo descartado** (L-04), de **escopo** (L-05) ou
  **estruturais** (L-07) — nenhuma é mutante previsto órfão.
- Contagens **conferidas por varredura do arquivo**, não estimadas: 58 IDs `CT-` distintos, 58 linhas
  no [Índice de Cenários](#índice-de-cenários), nenhum cenário fora do índice, nenhuma linha de
  índice sem cenário e nenhuma referência `CT-nn` apontando para cenário inexistente.
  > *Histórico deste cabeçalho, porque ele é o oráculo que o documento oferece para se auditar: a
  > 1ª versão declarava **54** mutantes e **4** lacunas; a 1ª rodada adversarial mostrou que os dois
  > erravam **para menos** e a recontagem disse **88**; a 2ª rodada mostrou que **a recontagem também
  > estava errada** (93) e que a correção das lacunas **nunca chegara ao texto**. Os números acima
  > são os primeiros produzidos por contagem mecânica.*
- **Revisão adversarial**: obrigatória (três áreas em perfil `completo`) e **executada**. Ver
  [Revisão Adversarial](#revisão-adversarial).

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | models `Cupom` e `CupomUso`; migrations `cupons` e `cupom_usos`; enum `TipoDeDesconto`; `CupomResource` + `ListCupons`/`CreateCupom`/`EditCupom`; `CupomPolicy`; `CupomFactory`; channel de log `cupom`; **`PapeisSeeder`, que é infra compartilhada** | CT-01, CT-02, CT-17, CT-21 |
| **F**unction | cadastrar / editar / excluir cupom; listar; localizar por código; calcular o desconto; consumir um uso; registrar a trilha; recortar a listagem por permissão | CT-01…CT-16, CT-33…CT-43, CT-48…CT-55 |
| **D**ata | `codigo` (string 40 — caixa, espaços nas bordas, acento, emoji, comprimento); `tipo` (2 valores, **e é editável** — ver CT-48); `valor` (`unsignedInteger`, **unidade decidida pelo `tipo`**); `expira_em` (`timestamp`); `limite_de_usos`; `usos` (contador, fora do `$fillable`); `tenant_id` (nullable — dado de **outra organização**); `aplicado_por_id` (nullable — **e não é o usuário autenticado**, ver CT-49) | CT-03, CT-06…CT-16, CT-22, CT-24, CT-33…CT-35, CT-42, CT-48, CT-49, CT-51 |
| **I**nterfaces | tela Filament no painel `/app` (3 rotas); **chamada direta ao model** por controller, job, comando ou Livewire futuro (`## Ponto de Integração` do PRD); seeder/tinker. **Não há rota HTTP pública de aplicação** — declarada fora de escopo no `00` | CT-08, CT-10, CT-18, CT-24…CT-43, CT-49, CT-53, CT-54 |
| **P**latform | PHP 8.3+; **SQLite `:memory:` em teste × MySQL em produção** — três consequências medidas: (a) SQLite **não considera dois `NULL` iguais**, então `unique(['tenant_id','codigo'])` **não barra nada em modo single-tenant** → **CT-53**; (b) conexão única em `:memory:` impede dois *writers* reais → **L-02**; (c) SQLite não tem `enum` de banco → **CT-54**. Playwright + `npm run build` para o `05` | CT-53, CT-54, CT-31 (+ L-02) |
| **O**perations | cinco papéis (`master_global`, `admin`, `admin_organizacao`, `panel_user`, `infra`); **dois modos** do kit (`KIT_TENANCY` default **`false`** — e é o modo em que RQ-07 quase ficou sem cenário positivo, ver CT-55); uso indevido = usuário comum emitindo desconto | CT-17…CT-22, CT-50, CT-55 |
| **T**ime | `expira_em` vs `now()`; virada de dia dentro do mesmo dia; **duas aplicações disputando o último uso**; ordem *validar → aplicar* com expiração no meio; reentrada de estado; `created_at` da trilha | CT-27…CT-32, CT-40, CT-52 |

**Nenhuma dimensão ficou vazia.**

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — o cupom se cadastra e se edita pela tela do painel, com os cinco campos | A5 (padrão) | RQ-01, RQ-02, RQ-04, RQ-05, RQ-06 | EP + gate de tela de escrita | CT-01…CT-03 |
| **R2** — `tipo` admite exatamente `porcentagem` e `fixo` | A5 (padrão) | RQ-03 | EP exaustiva do enum | CT-04, CT-05, **CT-54** |
| **R3** — o domínio válido de `valor` depende do `tipo` | A1 (completo) | RQ-03 × RQ-04 | tabela de decisão + BVA 3-valores | CT-06…CT-08, **CT-48** |
| **R4** — validade e limite têm domínio próprio **na gravação** | A4+A5 (padrão, escalada) | RQ-05, RQ-06 | BVA 3-valores + falha fechado | CT-09…CT-12, **CT-52** |
| **R5** — o código é único dentro da organização e normalizado | A5 (padrão) | RQ-14, RQ-02 | normalização + EP | CT-13…CT-16, **CT-51**, **CT-53** |
| **R6** — só o admin cria, edita e exclui | A3 (completo) | RQ-07 | matriz papel × verbo + fora da UI | CT-17…CT-19, **CT-50**, **CT-55** |
| **R7** — os demais usuários apenas listam, e só os ativos | A3+A7 (completo) | RQ-08 | matriz + EP exaustiva do estado exibido | CT-20…CT-23 |
| **R8** — a aplicação recusa código que não existe | A2 (completo) | RQ-09 | EP (ausente ≠ null ≠ vazio) + matriz `validar` | CT-24…CT-26 |
| **R9** — a aplicação recusa cupom fora da validade | A4 (padrão, escalada) | RQ-10 | BVA 3-valores no instante | CT-27…CT-29 |
| **R10** — a aplicação recusa cupom com o limite esgotado | A2 (completo) | RQ-11 | BVA 3-valores + concorrência + 2-switch | CT-30…CT-32 |
| **R11** — aplicada, a operação desconta o valor calculado do total | A1 (completo) | RQ-12 | BVA + tabela de decisão por tipo | CT-33…CT-35 |
| **R12** — aplicada, a operação consome **exatamente um** uso | A2 (completo) | RQ-13 | rastreio de efeito (4 direções) | CT-36…CT-39 |
| **R13** — aplicada, a operação registra **quem** aplicou e **quando** | A6 (padrão, escalada) | RQ-15 | rastreio de efeito (4 direções) | CT-40…CT-43, **CT-49** |
| *(matriz)* | — | — | matriz estado × operação — colunas `editar` e `excluir` | CT-44…CT-47 |

Os cenários em **negrito** nasceram da revisão adversarial.

### Sinais de leitura do mapa

- **Nenhuma regra ficou sem exemplo**; **nenhum exemplo ficou sem regra.**
- **Perguntas vermelhas: 12.** Em
  [Perguntas para o `00-requisito.md`](#perguntas-para-o-00-requisitomd). Onze não bloqueiam a
  derivação — foram resolvidas por **falha fechado** com o invariante afirmado junto, ou já vinham
  marcadas como premissa no `00`. **Q-12 bloqueia**: sem ela, RQ-08 fica sem cenário no modo default
  do kit (lacuna estrutural **L-07**).
- **Gerar regra não é gerar falsificador.** A tabela acima prova rastreabilidade de **cobertura**; a
  que prova rastreabilidade de **falsificação** é a
  [Rastreabilidade `RQ` → falsificador](#rastreabilidade-rq--falsificador). São coisas diferentes, e
  confundi-las foi um dos achados da revisão.

---

## Fronteira com o Plano

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| nomes `Cupom::valido()`, `aplicarEm()`, `descontoSobre()`, `scopeAtivos()`, `situacao()` | escolha de implementação | **detalhe do cenário.** Os cenários falam de "localizar o cupom pelo código" e "aplicar o cupom a um total"; os nomes só aparecem na coluna *Arquivo* do índice |
| `UPDATE … WHERE usos < limite_de_usos` (consumo atômico) | **premissa de mecanismo** — o requisito pede que o limite não seja estourado, não *como* | fixa **em que mecanismo** CT-31 é escrito; **não dispensa o cenário**. O mecanismo descartado (ler-comparar-salvar) é o mutante M10.2 |
| **a forma observável da recusa de `aplicarEm()`** (exceção) | só o PRD determina | **premissa de mecanismo + pergunta Q-10.** Ver [O que "recusada" significa](#o-que-recusada-significa) — a revisão adversarial mostrou que sem fixar isso o conjunto inteiro aceita "devolve o total sem desconto" como recusa |
| tabela `cupom_usos` e o par `valor_original` / `valor_desconto` | mecanismo, quanto à tabela; as **duas colunas de valor** só o PRD determina | mecanismo → CT-40…CT-43 escritos nele. As colunas → **Q-03** |
| rótulos `"Percentual de desconto"` / `"Valor do desconto (centavos)"` | **comportamento visível que o requisito não determina** | **Q-04.** CT-B01 afirma que o rótulo **muda** e que o gravado corresponde ao exibido; o texto exato é detalhe |
| `->defaultSort('expira_em', 'desc')` | ordem que o requisito não determina | **Q-05.** Nenhum cenário afirma ordem |
| cores dos badges | cor que o requisito não determina | **Q-06.** É a razão de o `05` não ter CT-B de cor |
| channel `cupom`, formato `[Cupom@metodo]`, níveis | **nenhuma cláusula `RQ` pede log** | ver [Nota sobre os CT de log](#nota-sobre-os-ct-de-log) |
| paths das suítes | path é autoridade do PRD | adotados — ver [a nota sobre a suíte](#por-que-testskit-e-não-testsfeature) |
| unidade de `valor`, painel `/app`, papel `admin_organizacao`, unicidade por organização | **premissas P-02, P-04, P-05, P-09 declaradas no `00`** | respeitadas **como dadas**. Exceção declarada: **Q-09** registra uma contradição factual interna à defesa de P-02 que a revisão encontrou — registrada como achado, não corrigida |

### Vocabulário de recusa — forma observável fixada para **cada** operação

A primeira rodada mostrou que `Então a aplicação é recusada`, sem forma observável, é satisfeito por
uma implementação que **devolve o total sem desconto em silêncio**. A segunda rodada mostrou que a
correção fora aplicada **a uma operação só**, e que os cenários novos tinham quatro verbos de recusa
igualmente vagos — *"a gravação falha"*, *"a ação é recusada"*, *"não consegue cadastrar"*. É uma
**regra sobre o vocabulário deste arquivo**, não um parágrafo sobre um método:

| Frase usada no `Então` | Significa exatamente | Onde aparece |
|---|---|---|
| **"a aplicação é recusada"** | a chamada **não devolve um total**; sinaliza a falha de forma **distinguível de um desconto de zero** | CT-10, CT-29, CT-31, CT-37, CT-38 |
| **"a gravação é recusada com erro no campo X"** | a validação do formulário reprova, **nomeando o campo X**; nenhuma outra reprovação satisfaz | CT-05, CT-06, CT-07, CT-09, CT-11, CT-12, CT-48, CT-51, CT-52 |
| **"a gravação falha"** (por fora da tela) | a escrita **não persiste**, e o `Então` seguinte afirma **o total de registros**, para que uma falha por motivo alheio (NOT NULL noutro campo) não satisfaça a frase | CT-53, CT-54, CT-56, CT-57 |
| **"a ação é recusada"** | a resposta é **403** — e **não** "a ação estava escondida". Barreira que vive só na visibilidade **não** satisfaz esta frase | CT-50 |
| **"a resposta é 403 / 404"** | literal, no código HTTP | CT-18, CT-22, CT-47 |

> **Por que "a ação é recusada" precisou de 403 explícito**: com a barreira só em `->visible()`, o
> arnês **recusa a chamada porque a ação está escondida**, e a frase vaga ficaria verde — CT-50 viraria
> uma cópia cara de CT-19 e o mutante M6.4 sobreviveria. Este é o achado nº 4 da segunda rodada.
>
> **Invariante que vale em qualquer resposta a Q-10**: *quem chama consegue separar "recusado" de
> "aplicado com desconto zero"* — as duas levam a cobranças diferentes. (Mecanismo do PRD: exceção.)

### Critérios de aceitação de **todo** `Então` deste arquivo

A segunda rodada apontou que as correções da primeira foram aplicadas **por instância** e nunca
promovidas a regra — e por isso os cenários irmãos repetiram o mesmo defeito (log genérico corrigido
em CT-26 e repetido em CT-37; `audit.console` corrigido em CT-45 e repetido em CT-51; ação escondida
no `Então` corrigida em CT-18/19/22 e reintroduzida em CT-55). A lista abaixo é o critério aplicado a
**todos os 58 cenários**, novos e velhos:

1. **Toda asserção de ausência tem âncora positiva no mesmo `Então`** — "não aparece" vem acompanhado
   de "e o total é N", senão passa com a consulta devolvendo nada.
2. **Toda asserção sobre `audits` tem `audit.console` ligada e uma linha preexistente no `Dado`.**
3. **Todo `Então` de recusa usa uma das frases da tabela acima** — nenhuma paráfrase nova.
4. **Todo `Então` afirma valor concreto**, nunca uma frase descritiva do comportamento
   ("o contador não é reescrito pelo payload" é prosa, não asserção).
5. **Nenhuma ação e nenhuma persona nova dentro do `Então`** — se precisa de duas, é `Esquema`.
6. **Todo `Dado` de entidade com ciclo de vida fixa a situação de partida**, e ela é **diferente de
   zero** sempre que o `Então` afirmar que algo "continua" naquele número.
7. **Todo `Esquema` cujo `Então` cita um motivo/rótulo tem esse motivo como coluna**, não como texto
   fixo que uma string genérica satisfaria.
8. **Nenhum cenário cita papel do kit** — só as personas da tabela de realização.

### Nota sobre os CT de log

A `feature-wiki` exige "CTs de log no `04`". A `feature-test-design` proíbe o PRD como fonte de
comportamento. **Nenhuma das quinze `RQ` menciona log.** Resolução declarada:

> A asserção de log entra como **`E` secundário** de cenários que já têm oráculo vindo do requisito
> (CT-26, CT-37), **nunca** como único `Então`, e **nenhum CT existe só para o log**.

Verificado que os três motivos de recusa (RQ-09, RQ-10, RQ-11) **continuam separadamente
falsificáveis sem o log**, pela situação de partida de cada linha de CT-26.

### Por que `tests/Kit` e não `tests/Feature`

`wikis/convencoes.md` manda pôr o teste do negócio em `tests/Feature`. A escolha do PRD é **forçada
pelo arnês**: `tests/Pest.php` liga `Tests\TenancyTestCase` **apenas** a `tests/Tenancy` e
`tests/BrowserTenancy` (`tests/Pest.php:67-70, 142-145`), e é esse `TestCase` que fixa
`permission.teams` **antes** das migrations. Não existe suíte multi-tenant fora de `tests/Tenancy`.
Manter o par single-tenant em `tests/Kit` os deixa no mesmo grupo (`kit`) e no mesmo comando.

---

## Divergências declaradas

| Instrução | Quem vence | Por quê |
|---|---|---|
| skill sugere `pest --parallel --tia` na Verificação Final | **`.ai/rules/testes-browser.md`** | a rule mediu: `--parallel` com browser derruba 4 de 11 cenários, e sem **PCOV** o `--tia` em série não termina (abortado após 35 min). Comandos: `vendor/bin/pest --parallel --group=kit` e `vendor/bin/pest --testsuite=Browser`, em série |
| skill afirma que `waitForText`/`waitForSelector`/`waitUntil` **não existem** | **o vendor instalado** | conferido em `vendor/pestphp/pest-plugin-browser/src/Api/`: **`waitForText`, `wait`, `waitForEvent`, `waitForKey`, `pressAndWaitFor` existem**; `waitForSelector` e `waitUntil` **não**. A orientação de fundo é seguida: **nenhum CT-B usa espera por segundos fixos** |
| skill assume `Unit` como a camada mais barata | **o arnês do projeto** | `tests/Pest.php` **não liga `Tests\TestCase` a `tests/Unit`** (só `Feature`, `Kit`, `Tenancy`, `Browser`, `BrowserTenancy`). Caso em `tests/Unit` roda **sem container**: `now()`, cast de enum, `config()` e Eloquent não resolvem. **A camada mais barata que este arnês sustenta é `Kit`/`Feature`** — 0 cenários em `Unit`, e não por preguiça de camada |
| skill manda rodar `pest --mutate` no fechamento | **parcialmente inviável hoje** | `pestphp/pest-plugin-mutate` está em `vendor/` **como dependência transitiva** — **não** está em `composer.json`, e some num `composer update`. Passo obrigatório: `composer require pestphp/pest-plugin-mutate --dev`. Sem PCOV, herda o custo que inviabilizou o `--tia` |

---

## Setup Global

### Personas — **papel no cenário**, não papel do kit

A segunda rodada da revisão adversarial achou um defeito que atravessava **26 cenários**: o índice
arquiva em `tests/Kit` (single-tenant) casos cujo `Dado` nomeia *Helena* e a *organização Acme* — e
no modo single-tenant **não existe `admin_organizacao` nem organização**. Ou eles eram
immaterializáveis onde estavam, ou seriam materializados com outra persona, medindo outra
autorização.

Resolução: as personas dos cenários são **papéis narrativos**, e cada suíte os **realiza** com o que
o modo dela tem. O cenário nunca cita papel do kit — quem cita é esta tabela.

| Persona no `Dado` | O que ela é na narrativa | Realização em `tests/Kit` (single-tenant) | Realização em `tests/Tenancy` (multi-tenant) |
|---|---|---|---|
| **Helena** | quem **administra** e opera o cadastro | `usuarioDoKit('master_global')` — é quem administra o `/app` no modo default | `usuarioComPapel('admin_organizacao', $acme)` |
| **Caio** | o **usuário comum** do negócio | `usuarioCom('panel_user')` | `usuarioComPapel('panel_user', $acme)` |
| **Marina** | a **compradora**, a quem o desconto é atribuído | `usuarioCom('panel_user')`, e-mail próprio | `usuarioComPapel('panel_user', $acme, 'marina@…')` |
| **Marta** | quem **administra a instalação** e **não** tem o papel de organização | `usuarioDoKit('master_global')` | `usuarioComPapel('master_global')`, **sem** `admin_organizacao` |
| **Bianca** | administradora de **outra** organização | *(não existe neste modo)* | `usuarioComPapel('admin_organizacao', $globex)` |
| *a organização Acme* | o contexto corrente | **o contexto único da instalação** | `tenant('Acme', 'acme')` + `noPainelDa($acme)` |
| *a organização Globex* | a **outra** organização | *(não existe — os cenários que a citam rodam só em `tests/Tenancy`)* | `tenant('Globex', 'globex')` |

- **`noPainelDa($acme)` antes de todo teste de componente** em `tests/Tenancy`
  (`tests/Pest.php:225-230`) — sem ele o escopo não é fixado e o `syncRoles()` grava em
  `Tenant::CONTEXTO_GLOBAL`.
- **Cenários que citam a Globex** (CT-15, CT-22, CT-25) **só existem em `tests/Tenancy`** — é o que a
  coluna *Arquivo* do índice registra.

> **Personas distintas em todos os eixos, não só no de autorização.** A primeira rodada achou a
> persona **colapsada no eixo de RQ-15**: quem chamava a aplicação e quem era passado como "quem
> aplicou" eram a mesma pessoa, e `auth()->id()` no lugar do argumento passava em todos os cenários.
> **CT-49 fecha isso.** A segunda rodada achou **Marta** faltando: com Helena e Caio, *nome do papel*
> e *permissão* **coincidem**, então `hasRole('admin_organizacao')` e `can('Update:Cupom')` produzem
> o mesmo resultado e o mutante do recorte por **nome de papel** atravessa. **Marta é a persona que
> desacopla os dois** — ela administra e **não** tem o papel de organização.

### Seeders (obrigatório em todo arquivo)

```php
beforeEach(function (): void {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
});
```

Sem os dois, **não existe permission nenhuma no banco** e todo cenário de autorização mede outra
coisa. `Tests\TestCase::seed()` usa `Artisan::call` de propósito (`tests/TestCase.php:158-169`) — o
`seed()` do Laravel grava **zero** linhas aqui.

### Fixtures

`database/factories/CupomFactory.php` **não existe** — é o passo 9 do PRD e **pré-requisito** destes
cenários.

| State | Estado |
|---|---|
| `Cupom::factory()` | `porcentagem`, valor 10, `expira_em` +30 d, limite 100, usos 0 → **E1 Ativo** |
| `->expirado()` | `expira_em` no passado → **E2** |
| `->esgotado()` | `usos === limite_de_usos` → **E3** |
| `->expirado()->esgotado()` | → **E4** |
| `->fixo(int $centavos)` | `tipo = fixo` |
| `->comUsos(int $n)` | `usos = $n`, para as situações de partida diferentes de 0 |

> **Armadilha do state**: `usos` fica **fora do `$fillable`**, então `state(['usos' => …])` é
> **descartado em silêncio**. Precisa de
> `->afterCreating(fn (Cupom $c) => $c->forceFill(['usos' => …])->save())`. Sem isso, CT-30, CT-32,
> CT-37 e CT-45 ficariam **verdes medindo um cupom ativo**. **CT-00 existe só para isso.**

**CT-00 — guarda da fixture** (não é caso de negócio; é o cinto do arnês):

```gherkin
    Esquema do Cenário: [CT-00] o state da factory produz a situação que promete
      Dado um cupom criado com o state "<state>"
      Quando a operadora lê a situação e o contador do registro recarregado do banco
      Então a situação é "<situacao>"
      E o contador de usos é <usos>

      Exemplos:
        | state                 | situacao | usos | # partição             |
        | (nenhum)              | Ativo    | 0    | E1                     |
        | expirado              | Expirado | 0    | E2                     |
        | esgotado              | Esgotado | 100  | E3 — o forceFill pegou |
        | expirado + esgotado   | Esgotado | 100  | E4 — precedência       |
        | comUsos(2)            | Ativo    | 2    | partida diferente de 0 |
```

### Fakes

- **`Queue::fake()` / `Mail::fake()` / `Notification::fake()`: não se aplicam.** A feature não
  enfileira, não envia e-mail e não notifica. Fake sem destinatário seria asserção de vácuo.
- **Espião de log**: `espiarCupom()`, no molde literal de `espiarAutenticacao()`
  (`tests/Pest.php:253-261`):

  ```php
  function espiarCupom(): LoggerInterface
  {
      $canal = Mockery::spy(LoggerInterface::class);
      Log::partialMock()->shouldReceive('channel')->with('cupom')->andReturn($canal);
      return $canal;
  }
  ```

  **Vive em `tests/Pest.php`**, porque é usado por dois arquivos — helper cruzado estoura
  `Call to undefined function` sob `--parallel`, `--tia` ou arquivo isolado (`.ai/rules/testes.md`,
  enforçado por `tests/Kit/HelpersDeTesteTest.php`).

### Auditoria — **pré-condição de qualquer asserção sobre `audits`**

`config('audit.console')` é **`false`** (`config/audit.php:203`) e **teste roda em console**. Sem
ligá-la, *nenhuma* linha de auditoria é gravada — e toda asserção sobre `audits` passaria **num mundo
sem destinatário**.

> Todo cenário que afirma **presença ou ausência** de linha em `audits` começa com
> `config(['audit.console' => true])` **e** prova, no `Dado`, que o mundo grava: uma operação anterior
> deixou **1** linha para aquele cupom. Vale para **CT-12, CT-43, CT-44, CT-45, CT-48, CT-50, CT-51 e
> CT-52** — oito cenários, e a lista é conferida contra o texto, não de memória.
>
> *A primeira rodada achou **CT-45** com o setup ligado e **sem a asserção** — setup morto. A segunda
> achou o **mesmo defeito reproduzido em CT-51**, e três cenários novos (CT-48, CT-51, CT-52) **fora
> desta lista**, que existe justamente para protegê-los. Os dois corrigidos.*

### Tempo

`$this->freezeTime()` (`Illuminate\Foundation\Testing\Concerns\InteractsWithTime:18`) em **todo**
cenário cujo `Dado` ou `Então` fale de instante — inclusive CT-44, que a revisão pegou usando a
palavra `futuro` como se fosse um valor. `config('app.timezone')` é **`UTC`** (`config/app.php:68`).

### Estratégia de DB

`RefreshDatabase` global em todas as suítes; SQLite `:memory:` (`phpunit.xml:53-54`).

---

## Matriz Estado × Operação

Montada **antes** das regras, do estado derivado e da lista de verbos — **não** do mapa de regras.

### Estados

"Ativo" não tem coluna (premissa **P-03**): é derivado de **duas** condições booleanas
independentes, logo **quatro** estados. O quarto existe **porque a implementação o colapsa**, e é
exatamente isso que precisa de célula:

| # | Estado | `expira_em` | `usos` vs `limite_de_usos` | Rótulo exibido |
|---|---|---|---|---|
| **E1** | Ativo | futuro | `<` | `Ativo` |
| **E2** | Expirado | passado | `<` | `Expirado` |
| **E3** | Esgotado | futuro | `>=` | `Esgotado` |
| **E4** | Expirado **e** esgotado | passado | `>=` | `Esgotado` (esgotado vence) |

### Operações

`listar` · `editar` · `excluir` · `validar` (localizar pelo código) · `aplicar` (consumir o uso)

### Contagem — refeita depois da revisão adversarial

A contagem anterior dizia *"20 células, 14 aceitam, 6 recusam"* **e**, três linhas acima, *"a coluna
`listar` tem 8 observações"*. As duas eram incompatíveis, e o colapso escolhido escondia justamente
**as três recusas de RQ-08**. Contagem honesta, nos dois níveis:

> **Nível da célula: 4 estados × 5 operações = 20 células. 20 resolvidas, 0 sem resolução.**
>
> **Nível da observação: 34** — contadas **da matriz renderizada abaixo**, célula a célula:
>
> | Coluna | Dimensão extra | Observações na matriz | Aceitam | Recusam |
> |---|---|---|---|---|
> | `listar` | **persona** — 3 personas × E1, 3 × E2/E3/E4 | 8 | 5 | **3** |
> | `editar` | **campo alterado** (`valor`, `tipo`, `codigo`, `expira_em`, `limite_de_usos`) | 8 | 4 | **4** |
> | `excluir` | **persona** — admin nos 4 estados, comum em E1 e E3 | 6 | 4 | **2** |
> | `validar` | — | 4 | 1 | **3** |
> | `aplicar` | **autor informado** (E1 ganha CT-49) | 5 | 2 | **3** |
> | **total** | | **31** | **16** | **14** |
>
> **Fora da matriz, declaradas aqui para não somarem em silêncio**: `validar` × **organização do
> ator** (CT-25) e `listar`/`editar`/`excluir` × **modo do kit** (CT-55) são observações reais que
> **não têm célula** nesta matriz bidimensional. São **3** observações extras → **34 no total**.

> **Onde a contagem anterior errava**: ela declarava 31/16/15 somando `excluir` como 5 e `validar`
> como 5. A matriz renderizada mostrava **6** para `excluir` e **4** para `validar` — e o `+1`
> fantasma de uma cancelava o `−1` da outra, de modo que **o total batia pelo motivo errado**. A
> quinta observação de `validar` era a dimensão "organização", que **não estava renderizada em célula
> nenhuma**. Achado nº 28 da segunda rodada.

**Critério para abrir uma dimensão**: abre-se quando **uma cláusula `RQ` distingue os valores dela**.
`listar` e `excluir` ganham **persona** (RQ-07, RQ-08); `editar` ganha **campo alterado** (RQ-03,
RQ-05, RQ-06, RQ-14); `aplicar` ganha **autor** (RQ-15).

**Aplicação declaradamente parcial, e por quê.** A segunda rodada apontou que o critério não era
aplicado uniformemente: `listar` abre persona nos 4 estados, `excluir` em 2, `aplicar` autor em 1.
As células ausentes **não são acidente e não são todas iguais**:

| Ausência | Situação |
|---|---|
| `excluir` × comum em **E2** e **E4** | **poda deliberada**: CT-50 já exercita a barreira em dois estados (E1 e E3), e a autorização não depende da situação do cupom. Se dependesse, seria o defeito que a linha E1 de CT-50 pega |
| `aplicar` × autor em **E2/E3/E4** | **não se aplica**: a operação recusa antes de registrar autor; não há observável a distinguir |
| **modo do kit** em todas as colunas | **lacuna estrutural declarada L-07** — ver [Achados estruturais escalados](#achados-estruturais-escalados) |

**A dimensão `campo alterado` inclui `tipo` e `codigo`.** A versão anterior a povoava só com os três
campos inócuos, e a revisão mostrou que **os dois campos perigosos** — o discriminador que decide a
unidade do dinheiro e o campo único — **nunca eram editados em cenário nenhum**. CT-48 e CT-51
fecham isso.

### Legenda — **é uma asserção, e foi reauditada célula a célula**

| Operação | Efeitos no caminho feliz | O que um `❌` desta coluna obriga a afirmar |
|---|---|---|
| `listar` | nenhum (leitura) | o registro **não** está na lista, **um cupom ativo está**, e o **total de registros** da lista — sem os três, a asserção passa com a lista vazia |
| `editar` | grava os campos + 1 linha em `audits` | o valor **lido do banco** é o antigo (número, não "não mudou") **e** `audits` na contagem anterior, com `audit.console` **ligada** |
| `excluir` | remove de `cupons` + remove `cupom_usos` em cascata + 1 linha em `audits` | o cupom **continua**, a trilha **continua com N linhas**, `audits` na contagem anterior |
| `validar` | nenhum (leitura); emite log `info` de recusa | **nada é devolvido** **e** o log saiu **com o motivo daquela situação** (efeito **positivo**) |
| `aplicar` | incrementa `usos` + insere 1 linha em `cupom_usos` + emite log | `usos` **no número exato** de antes, `cupom_usos` com **N** linhas (N > 0 no `Dado`), e o log saiu **com o motivo daquela situação** |

> **As duas linhas de log dizem a mesma coisa de propósito.** A versão anterior exigia "o motivo" de
> `validar` e só "o log de recusa saiu" de `aplicar` — duas exigências diferentes para a mesma classe
> de asserção, sem justificativa, e um log único `"recusa do consumo"` satisfazia as três linhas de
> CT-37. Achado nº 31 da segunda rodada; **CT-37 ganhou a coluna `motivo`**.

**Reauditoria, coluna a coluna** — a anterior deu ✔ para duas colunas que violavam a legenda:

| Coluna | Célula de recusa | Afirma tudo o que a legenda exige? |
|---|---|---|
| `listar` | **CT-20** | ✔ **agora sim** — a versão anterior tinha `inativos = (nenhum)`, que materializado é `assertCanSeeTableRecords([])`, asserção sobre conjunto vazio. **A prosa afirmava os dois lados e o Gherkin não os continha.** Reescrito com a frase de ausência **e** o total de registros |
| `editar` | **CT-12, CT-48, CT-51, CT-52** | ✔ — as quatro afirmam o valor lido do banco **e** `audits`. *A 2ª rodada achou **CT-51 sem a asserção de `audits`** enquanto esta mesma linha declarava "as quatro afirmam" — a prosa auditando o que o Gherkin não continha, pela quarta vez. Corrigido.* |
| `excluir` | **CT-50** | ✔ **agora existe, e no estado certo.** A versão anterior descrevia um `❌` que **não existia na matriz** (as quatro células eram `✅`) e auditava a linha com CT-45, que **executa a operação oposta**. Depois, CT-50 cobria só **E3** enquanto a matriz o citava também em **E1** — cenário certo, estado errado. CT-50 virou `Esquema` com as duas situações |
| `validar` | **CT-26** | ✔ — o **motivo** virou coluna do `Esquema`; antes era um `E` condicional que um log único `"cupom inválido"` satisfazia |
| `aplicar` | **CT-37** | ✔ — `usos`, `cupom_usos` e **o motivo**, agora como coluna |

### A matriz

| | `listar` | `editar` | `excluir` | `validar` | `aplicar` |
|---|---|---|---|---|---|
| **E1 Ativo** | ✅ Helena · ✅ Marta · ✅ Caio — **CT-20** | ✅ **CT-02** *(`valor`)* · ❌ **CT-48** *(`tipo`)* · ❌ **CT-51** *(`codigo`)* · ❌ **CT-52** *(`expira_em`)* | ✅ **CT-45** · ❌ Caio **CT-50** *(linha `ativo`)* | ✅ **CT-26** | ✅ **CT-36** · ✅ autor **CT-49** |
| **E2 Expirado** | ✅ Helena/Marta · ❌ Caio — **CT-20** | ✅ **CT-44** *(`expira_em` → reativa)* | ✅ **CT-45** | ❌ **CT-26** | ❌ **CT-37** |
| **E3 Esgotado** | ✅ Helena/Marta · ❌ Caio — **CT-20** | ✅ **CT-44** *(`limite_de_usos` ↑ → reativa)* · ❌ **CT-12** *(`limite_de_usos` ↓)* | ✅ **CT-45** *(trilha em cascata)* · ❌ Caio **CT-50** *(linha `esgotado`)* | ❌ **CT-26** | ❌ **CT-37** |
| **E4 Exp.+Esg.** | ✅ Helena/Marta · ❌ Caio — **CT-20** | ✅ **CT-44** *(`expira_em` → **não** reativa)* | ✅ **CT-45** | ❌ **CT-26** | ❌ **CT-37** |

**Cada coluna tem ao menos uma célula válida exercitada e ao menos uma de recusa.**

**Ciclo de volta (2-switch)**: `E3 ──editar(limite 3→5)──▶ E1 ──aplicar──▶ ?` — o `Então` de
**CT-32** é sobre o **destino do segundo giro** (`usos` vai a **4**, não a 1) e sobre **quais
registros do ciclo anterior ainda contam** (trilha com **4** linhas). **CT-44**, linha E4, prova que
reabrir **uma** dimensão não reabre a outra.

---

## Regra R1 — o cupom se cadastra e se edita pela tela do painel, com os cinco campos

> `RQ-01`, `RQ-02`, `RQ-04`, `RQ-05`, `RQ-06` · área A5 · perfil **padrão** · técnica: **EP** +
> **gate de tela de escrita**

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: o cupom se cadastra e se edita pela tela do painel, com código, tipo, valor, validade e limite

    Cenário: [CT-01] o cadastro grava os cinco campos do cupom
      Dado o relógio congelado em 15/08/2026 12:00:00
      E que a organização Acme não tem nenhum cupom cadastrado
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela preenche o formulário de novo cupom com código "BEMVINDO", tipo porcentagem, valor 15, validade em 30/09/2026 23:59 e limite de 200 usos
      Então existe um cupom com código "BEMVINDO", tipo porcentagem, valor 15, validade 30/09/2026 23:59:00 e limite 200
      E o contador de usos desse cupom é 0

    Cenário: [CT-02] a edição grava a alteração do valor do desconto
      Dado um cupom ativo "BEMVINDO", de porcentagem, com valor 15, limite de 200 usos e 0 usos feitos
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela altera o valor do desconto para 25 e salva
      Então o valor gravado do cupom "BEMVINDO" é 25
      E o tipo gravado continua porcentagem
      E o limite gravado continua 200

    Esquema do Cenário: [CT-03] campo fora do formulário não altera o registro
      Dado a organização Globex já existente, além da Acme
      E um cupom ativo "BEMVINDO" com 7 usos feitos, pertencente à organização Acme
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela salva a edição enviando também "<campo>" igual a "<valor_forjado>"
      Então o valor gravado de "<campo>" continua <valor_anterior>
      E o cupom "BEMVINDO" continua sendo o único da Acme

      Exemplos:
        | campo     | valor_forjado  | valor_anterior | # partição |
        | usos      | 0              | 7              | contador   |
        | tenant_id | (id da Globex) | (id da Acme)   | posse      |
```

- **CT-02 altera `valor`** e **fixa o limite 200 no próprio `Dado`** — a versão anterior herdava o
  200 de CT-01, e a revisão apontou: materializado, ou a factory (limite 100) derruba o cenário sem
  defeito, ou o materializador rebaixa a asserção. É a única célula **E1 × `editar` aceita** da
  matriz e precisa fechar sozinha.
- **CT-03 virou `Esquema` de duas linhas.** Antes era um envio único com os dois campos forjados — e
  combinar duas partições inválidas num cenário faz a primeira validação mascarar a segunda:
  **M1.3 e M1.4 não eram separadamente falsificáveis.**

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1.1 | a tela abre e o `save`/`create` não persiste (`GET` verde com o salvamento quebrado) | **CT-01, CT-02** |
| M1.2 | `expira_em` gravado como `date` — a hora se perde | **CT-01** (afirma `23:59:00`) |
| M1.3 | `usos` dentro do `$fillable` | **CT-03** (linha `usos`) |
| M1.4 | `tenant_id` dentro do `$fillable` | **CT-03** (linha `tenant_id`) |
| M1.5 | `usos` inicializado com o limite (default trocado) | **CT-01** |

---

## Regra R2 — `tipo` admite exatamente `porcentagem` e `fixo`

> `RQ-03` · área A5 · perfil **padrão** · técnica: **EP exaustiva do enum** — os dois valores são o
> domínio inteiro; não se amostra

```gherkin
    Esquema do Cenário: [CT-04] cada tipo do requisito é gravável e volta como foi gravado
      Dado que a administradora Helena opera o painel de negócio da Acme
      Quando ela cadastra um cupom "<codigo>" do tipo "<tipo>" com valor <valor>
      Então o cupom "<codigo>" tem o tipo "<tipo>"
      E a listagem mostra o cupom "<codigo>" com o rótulo de tipo "<rotulo>"

      Exemplos:
        | codigo   | tipo        | valor | rotulo      | # partição               |
        | PCT10    | porcentagem | 10    | Porcentagem | um dos dois do requisito |
        | FIXO1000 | fixo        | 1000  | Valor fixo  | o outro                  |

    Cenário: [CT-05] tipo fora dos dois do requisito é recusado pela tela
      Dado que a administradora Helena opera o painel de negócio da Acme
      E que a organização Acme não tem nenhum cupom cadastrado
      Quando ela tenta cadastrar um cupom "BRINDE" com o tipo "brinde"
      Então a gravação é recusada com erro no campo tipo
      E o número de cupons da Acme continua 0

    Cenário: [CT-54] tipo fora dos dois é recusado também por fora da tela
      Dado a organização Acme com 1 cupom válido já cadastrado
      Quando o sistema tenta gravar, sem passar pela tela, um cupom com código, valor, validade e limite válidos e o tipo "brinde"
      Então a gravação falha
      E a Acme continua com exatamente 1 cupom
```

- **CT-54 é o cenário por fora do componente de UI** que o gate de camada exige para toda regra de
  **validação de domínio** — R2 não tinha nenhum, e a revisão adversarial não chegou a nomear isso,
  mas o gate o exige. Se os dois valores forem garantidos só por `->options()` do `Select`, **CT-05
  fica verde e CT-54 vermelho**.
- **CT-05 é a partição inválida isolada**: o único campo inválido do envio é `tipo`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M2.1 | um terceiro valor é aceito (coluna `string` sem enum no cast) | **CT-54** |
| M2.2 | o `fixo` é gravado e volta como `porcentagem` (mapeamento invertido) | **CT-04** (linha `FIXO1000`) |
| M2.3 | o rótulo da tela vem de um array duplicado que diverge do enum | **CT-04** (coluna `rotulo`) |
| M2.4 | os dois valores existem só nas opções do `Select` | **CT-54** |

---

## Regra R3 — o domínio válido de `valor` depende do `tipo`

> `RQ-03` × `RQ-04` · área A1 · perfil **completo** · técnica: **tabela de decisão** (discriminador ×
> dependente) + **BVA 3-valores** (incremento **1**)

| `tipo` | domínio de `valor` (premissa **P-05**) | fronteiras |
|---|---|---|
| `porcentagem` | pontos percentuais inteiros, 1–100 | **0, 1, 100, 101** |
| `fixo` | centavos, ≥ 1 | **0, 1**, sem teto superior |

```gherkin
    Esquema do Cenário: [CT-06] o valor do desconto respeita a fronteira do seu tipo, na criação
      Dado que a administradora Helena opera o painel de negócio da Acme
      E que a organização Acme não tem nenhum cupom cadastrado
      Quando ela tenta cadastrar um cupom do tipo "<tipo>" com valor <valor>
      Então a gravação é "<resultado>"
      E o número de cupons da Acme é <total>

      Exemplos:
        | tipo        | valor | resultado | total | # borda                   |
        | porcentagem | 0     | recusada  | 0     | borda inferior            |
        | porcentagem | 1     | aceita    | 1     | borda inferior + 1        |
        | porcentagem | 100   | aceita    | 1     | borda superior            |
        | porcentagem | 101   | recusada  | 0     | borda superior + 1        |
        | fixo        | 0     | recusada  | 0     | borda inferior            |
        | fixo        | 1     | aceita    | 1     | borda inferior + 1        |
        | fixo        | 20000 | aceita    | 1     | acima de 100 — e é VÁLIDO |

    Esquema do Cenário: [CT-07] a mesma fronteira vale na edição do valor
      Dado um cupom ativo "PROMO" do tipo "<tipo>" com valor 10 e 0 usos
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta alterar o valor do desconto para <valor>
      Então a gravação é "<resultado>"
      E o valor gravado do cupom "PROMO" é <valor_final>
      E o tipo gravado continua "<tipo>"

      Exemplos:
        | tipo        | valor | resultado | valor_final | # borda            |
        | porcentagem | 101   | recusada  | 10          | borda superior + 1 |
        | porcentagem | 100   | aceita    | 100         | borda superior     |
        | porcentagem | 0     | recusada  | 10          | borda inferior     |
        | fixo        | 0     | recusada  | 10          | borda inferior     |
        | fixo        | 20000 | aceita    | 20000       | sem teto no fixo   |

    Esquema do Cenário: [CT-48] trocar o tipo revalida o valor contra o domínio do tipo NOVO
      Dado a auditoria de console ligada
      E um cupom ativo "MUDA" do tipo "<tipo_antigo>" com valor <valor_antigo>, e 1 linha na auditoria dele
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela altera o tipo para "<tipo_novo>" e o valor para <valor_enviado> no mesmo salvamento
      Então a gravação é "<resultado>"
      E o tipo gravado do cupom "MUDA" é "<tipo_final>"
      E o valor gravado do cupom "MUDA" é <valor_final>
      E a auditoria desse cupom passa a ter <auditoria> linhas

      Exemplos:
        | tipo_antigo | valor_antigo | tipo_novo   | valor_enviado | resultado                          | tipo_final  | valor_final | auditoria | # direção                                    |
        | fixo        | 20000        | porcentagem | (não tocado)  | recusada com erro no campo valor   | fixo        | 20000       | 1         | fixo → porcentagem: 20000 não cabe em 1..100 |
        | porcentagem | 10           | fixo        | 20000         | aceita                             | fixo        | 20000       | 2         | porcentagem → fixo: 20000 é VÁLIDO em fixo   |
        | fixo        | 20000        | porcentagem | 50            | aceita                             | porcentagem | 50          | 2         | troca legítima, com o valor ajustado junto   |

    @premissa
    Cenário: [CT-56] percentual acima de 100 é barrado também por fora da tela
      Dado a organização Acme com 1 cupom válido já cadastrado
      Quando o sistema tenta gravar, sem passar pela tela, um cupom de porcentagem com valor 150 e os demais campos válidos
      Então a gravação falha
      E a Acme continua com exatamente 1 cupom

    @premissa
    Cenário: [CT-08] percentual acima de 100, se existir no banco, nunca desconta mais que o total
      Dado um cupom de porcentagem com valor 150, validade futura, limite de 5 usos e 0 linhas na trilha, gravado com as validações do model contornadas
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 3.000 centavos
      Então o total devolvido é 0 centavos
      E o desconto registrado na trilha é exatamente 3.000 centavos
      E o desconto registrado nunca excede o valor original registrado
```

- **CT-48 nasceu da revisão adversarial**, e é o achado mais caro dela. Todo cenário do conjunto
  anterior mantinha `tipo` **fixo** e variava o dependente: `tipo` **nunca era editado**. Um dev
  competente escreve a regra do teto como `rules(fn (Get $get) => $get('tipo') === 'porcentagem' ?
  ['max:100'] : [])` no `create`, e no `save` revalida `valor` só se o **campo `valor`** for tocado.
  Resultado: um cupom `fixo` de R$ 200,00 vira **20000%** ao trocar o tipo. **M3.6 estava mapeado
  para CT-07, e CT-07 não o mata** — no `Dado` de CT-07 o tipo já é o final e nunca muda dentro do
  cenário. Mapeamento corrigido.
- **CT-06 e CT-07 são o mesmo BVA em dois pontos de entrada** — validação escrita no `create` e
  esquecida no `save` é invisível para quem só cria. A linha `fixo / 20000` mata o teto de 100
  aplicado ao campo errado.
- **CT-08 é `@premissa` de comportamento**, direção por **falha fechado** (CT-06/CT-07 recusam 101 —
  a barreira nunca se assume ausente), e o **invariante afirmado junto** vale qualquer que seja a
  resposta. O `Então` agora usa **igualdade** (`exatamente 3.000`) e não desigualdade: a revisão
  mostrou que `não excede 3.000` deixa passar uma trilha que grava `0` ou `1`.
  **Se negado**: CT-06/CT-07 perdem as linhas `101`; **CT-08 não muda**.
- **CT-08 é o cenário por fora do componente** que o gate exige para R3.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M3.1 | o teto de 100 é aplicado a `valor` **sem olhar o tipo** | **CT-06** (linha `fixo / 20000`) |
| M3.2 | `>` no lugar de `>=` no teto: 101 passa | **CT-06, CT-07** |
| M3.3 | `minValue` ausente: 0 é aceito e o cupom não desconta nada | **CT-06, CT-07** |
| M3.4 | a fronteira existe no `create` e não no `save` | **CT-07** |
| M3.5 | a fronteira vive só no formulário; outra via de gravação passa | **CT-56** *(corrigido — antes apontava CT-08, cujo `Dado` **pressupõe** este mutante em vez de matá-lo)* |
| M3.6 | trocar o `tipo` não revalida o `valor` já gravado | **CT-48** *(corrigido — antes apontava CT-07, que não o mata)* |
| M3.7 | a revalidação acontece e **converte** o valor sozinha (20000 → 100) em vez de recusar | **CT-48** (afirma `valor` **e** `tipo` lidos do banco) |
| M3.8 | a revalidação lê o **`tipo` antigo** (`getOriginal`) e recusa a troca legítima para `fixo` com valor alto | **CT-48** (linha `porcentagem → fixo`) |

---

## Regra R4 — validade e limite têm domínio próprio **na gravação**

> `RQ-05`, `RQ-06` · áreas A4+A5 · perfil **padrão** com **técnica escalada a BVA 3-valores** ·
> incremento **1 segundo** e **1** · **teto de 3 estourado (5 cenários) — justificado abaixo**

```gherkin
    @premissa
    Esquema do Cenário: [CT-09] a validade gravada tem de estar no futuro, na criação
      Dado o relógio congelado em 15/08/2026 12:00:00
      E que a organização Acme não tem nenhum cupom cadastrado
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta cadastrar um cupom "PRAZO" com validade em <validade>
      Então a gravação é "<resultado>"
      E o número de cupons da Acme é <total>

      Exemplos:
        | validade            | resultado | total | # borda     |
        | 15/08/2026 11:59:59 | recusada  | 0     | borda − 1 s |
        | 15/08/2026 12:00:00 | recusada  | 0     | borda exata |
        | 15/08/2026 12:00:01 | aceita    | 1     | borda + 1 s |

    @premissa
    Esquema do Cenário: [CT-52] a mesma fronteira de validade vale na edição
      Dado a auditoria de console ligada
      E o relógio congelado em 15/08/2026 12:00:00
      E um cupom ativo "PRAZO" com validade em 30/09/2026 23:59:00 e 1 linha na auditoria dele
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta alterar a validade para <validade>
      Então a gravação é "<resultado>"
      E a validade gravada do cupom "PRAZO" é <validade_final>
      E a auditoria desse cupom passa a ter <auditoria> linhas

      Exemplos:
        | validade            | resultado                            | validade_final      | auditoria | # borda     |
        | 15/08/2026 11:59:59 | recusada com erro no campo validade  | 30/09/2026 23:59:00 | 1         | borda − 1 s |
        | 15/08/2026 12:00:00 | recusada com erro no campo validade  | 30/09/2026 23:59:00 | 1         | borda exata |
        | 15/08/2026 12:00:01 | aceita                               | 15/08/2026 12:00:01 | 2         | borda + 1 s |

    @premissa
    Cenário: [CT-57] validade no passado é barrada também por fora da tela
      Dado o relógio congelado em 15/08/2026 12:00:00
      E a organização Acme com 1 cupom válido já cadastrado
      Quando o sistema tenta gravar, sem passar pela tela, um cupom com validade em 14/08/2026 12:00:00 e os demais campos válidos
      Então a gravação falha
      E a Acme continua com exatamente 1 cupom

    @premissa
    Cenário: [CT-10] cupom com validade no passado, se existir no banco, não é aplicável
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PASSADO" com validade em 14/08/2026 12:00:00, limite de 5 usos, 2 usos feitos e 2 linhas na trilha, gravado com as validações do model contornadas
      E a compradora Marina identificada, que seria registrada na trilha no caminho feliz
      Quando o sistema aplica esse cupom a um total de 10.000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom continua 2
      E a trilha do cupom continua com 2 linhas

    @premissa
    Esquema do Cenário: [CT-11] o limite de usos gravado tem de permitir ao menos um uso
      Dado que a organização Acme não tem nenhum cupom cadastrado
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta cadastrar um cupom "LIMITE" com limite de <limite> usos
      Então a gravação é "<resultado>"
      E o número de cupons da Acme é <total>

      Exemplos:
        | limite | resultado | total | # borda   |
        | 0      | recusada  | 0     | borda     |
        | 1      | aceita    | 1     | borda + 1 |
        | 2      | aceita    | 1     | dentro    |

    @premissa
    Cenário: [CT-12] reduzir o limite abaixo dos usos já feitos é recusado, e nada é reescrito
      Dado a auditoria de console ligada
      E um cupom ativo "PROMO" com limite de 10 usos e 7 usos já feitos
      E que a trilha desse cupom tem 7 linhas e a auditoria dele tem 1 linha
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta alterar o limite de usos para 5
      Então a gravação é recusada com erro no campo limite de usos
      E o limite gravado do cupom "PROMO" continua 10
      E o contador de usos do cupom continua 7
      E a trilha do cupom continua com 7 linhas
      E a auditoria desse cupom continua com 1 linha
```

- **CT-52 nasceu da revisão adversarial.** **M4.6** estava mapeado para "CT-07 + CT-44 (linha E2)" —
  CT-07 fala de `valor`, não de `expira_em`, e CT-44 E2 grava um valor **válido**. Nenhum dos dois
  podia observar a ausência da regra no `save`. **Mapeamento falso, corrigido.**
- **CT-10 foi reescrito.** A versão anterior tinha `Quando o sistema tenta **localizar** esse
  código`, com `0 usos` e `0 linhas` de partida — e a própria legenda da matriz declara que `validar`
  **não tem efeito no caminho feliz**. Os dois `Então` de não-efeito eram **verdadeiros em qualquer
  implementação**: falso ✅ duplo, num mundo sem saldo. Pior: o invariante que CT-10 deve sustentar é
  *"não é **aplicável**"*, e o cenário testava *"não é **localizável**"*. Agora a operação é
  **aplicar**, a partida é **2 usos / 2 linhas**, e a compradora existe.
- **Estouro do teto (5 > 3), justificado**: três premissas de comportamento distintas (validade
  passada, limite zero, limite abaixo dos usos), cada uma com invariante próprio, mais o cenário por
  fora da UI que o gate exige, mais o segundo ponto de entrada da validade.
- **Direção das três premissas — falha fechado:**

| Premissa | Direção | Cláusula que já trata o estado como inválido | Invariante afirmado junto |
|---|---|---|---|
| cadastrar/editar para validade vencida? | **recusa** | RQ-10 já trata o vencido como inválido **no uso** | **CT-10**: gravado por qualquer via, **não é aplicável** |
| limite 0? | **recusa** | RQ-11 já trata `usos >= limite` como esgotado — limite 0 nasce esgotado | **CT-30** (linhas `limite 1`): o cupom aceito de limite 1 aceita **exatamente um** uso |
| reduzir o limite abaixo dos usos? | **recusa** | cria `usos > limite`, que a comparação de uso já trata como esgotado | **CT-12**: o contador **não** é corrigido e a trilha **não** é truncada |

> A revisão apontou que o invariante de CT-11 apontava para **CT-30 com limite 3** em todas as
> linhas — o invariante prometido (*limite 1 aceita um uso*) **não estava lá**, e existia só por
> acidente em CT-31. **CT-30 recebeu duas linhas de `limite 1`**, e o invariante passou a ter cenário
> próprio para onde recuar se Q-11 for respondida ao contrário.

- **Se negado**: CT-09 e CT-52 perdem as linhas de recusa (**CT-10 permanece**); CT-11 perde a linha
  `0` (**as linhas `limite 1` de CT-30 permanecem**); CT-12 inverte o `Então` da recusa (**as três
  linhas de invariante permanecem**).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M4.1 | `>=` no lugar de `>` na validade mínima, **na criação** | **CT-09** (borda exata) |
| M4.1b | `>=` no lugar de `>` na validade mínima, **na edição** | **CT-52** (borda exata) — *a versão anterior tinha um valor só e se dizia BVA 3-valores* |
| M4.2 | o `minDate` existe no formulário e em lugar nenhum além dele | **CT-57** *(corrigido — antes apontava CT-10, cujo `Dado` **pressupõe** este mutante)* |
| M4.3 | limite 0 aceito — o cupom nasce esgotado | **CT-11** |
| M4.4 | a redução do limite é aceita e o código "conserta" o contador | **CT-12** |
| M4.5 | a redução é aceita e as linhas excedentes da trilha são apagadas | **CT-12** |
| M4.6 | a validação de validade roda no `create` e não no `save` | **CT-52** *(corrigido — antes apontava CT-07/CT-44)* |
| M4.7 | a edição recusa mas grava a validade nova antes de recusar | **CT-52** (afirma o valor lido do banco) |

---

## Regra R5 — o código é único dentro da organização e normalizado

> `RQ-14`, `RQ-02` · área A5 · perfil **padrão** · técnica: **normalização** + **EP** ·
> **teto de 3 estourado (6 cenários) — justificado abaixo**

```gherkin
    Esquema do Cenário: [CT-13] o código é normalizado antes de ser comparado, na criação
      Dado um cupom ativo já cadastrado com o código "PROMO10"
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta cadastrar um segundo cupom com o código "<digitado>"
      Então a gravação é "<resultado>"
      E o número de cupons da Acme é <total>

      Exemplos:
        | digitado    | resultado | total | # partição                     |
        | promo10     | recusada  | 1     | mesma palavra, caixa diferente |
        | " PROMO10 " | recusada  | 1     | espaços nas bordas             |
        | PrOmO10     | recusada  | 1     | caixa misturada                |
        | PROMO11     | aceita    | 2     | palavra realmente diferente    |

    Esquema do Cenário: [CT-51] a mesma unicidade e normalização valem na edição do código
      Dado dois cupons ativos cadastrados, "PROMO10" e "PROMO11"
      E a auditoria de console ligada, com 1 linha na auditoria do cupom "PROMO11"
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta alterar o código do cupom "PROMO11" para "<digitado>"
      Então a gravação é "<resultado>"
      E o código gravado desse cupom é "<gravado>"
      E o número de cupons da Acme continua 2
      E a auditoria desse cupom passa a ter <auditoria> linhas

      Exemplos:
        | digitado    | resultado                          | gravado | auditoria | # partição                  |
        | promo10     | recusada com erro no campo código  | PROMO11 | 1         | colide, caixa diferente     |
        | " PROMO10 " | recusada com erro no campo código  | PROMO11 | 1         | colide, espaços nas bordas  |
        | promo12     | aceita                             | PROMO12 | 2         | não colide, e é normalizado |

    Cenário: [CT-14] salvar a edição sem mudar o código não acusa colisão consigo mesmo
      Dado um cupom ativo "PROMO10" com limite de 50 usos
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela altera apenas o limite de usos para 80 e salva
      Então a gravação é aceita
      E o limite gravado do cupom "PROMO10" é 80
      E o número de cupons da Acme continua 1

    Cenário: [CT-15] duas organizações podem ter, cada uma, um cupom com o mesmo código
      Dado a organização Acme com um cupom ativo "BLACKFRIDAY"
      E que a administradora Bianca opera o painel da organização Globex
      Quando ela cadastra um cupom "BLACKFRIDAY" na Globex
      Então a gravação é aceita
      E a Globex tem 1 cupom com o código "BLACKFRIDAY"
      E a Acme continua com 1 cupom com o código "BLACKFRIDAY"

    Esquema do Cenário: [CT-16] o código aceita o comprimento e o alfabeto do requisito
      Dado que a administradora Helena opera o painel de negócio da Acme
      Quando ela tenta cadastrar um cupom com o código "<digitado>"
      Então a gravação é "<resultado>"
      E o código gravado é "<gravado>"

      Exemplos:
        | digitado            | resultado | gravado        | # partição             |
        | (40 caracteres "A") | aceita    | (os mesmos 40) | limite do varchar      |
        | (41 caracteres "A") | recusada  | —              | limite + 1             |
        | ação10              | aceita    | AÇÃO10         | acento — mb_strtoupper |
        | 🎁10                 | aceita    | 🎁10           | emoji, 4 bytes         |
        | "   "               | recusada  | —              | só espaços             |

    Cenário: [CT-53] o código duplicado é barrado mesmo quando a escrita não passa pela tela
      Dado a organização Acme com um cupom ativo "BLACKFRIDAY"
      Quando o sistema tenta gravar, sem passar pela tela, um segundo cupom " blackfriday " com valor, validade e limite válidos
      Então a gravação falha
      E a Acme continua com exatamente 1 cupom
      E o código gravado desse cupom é "BLACKFRIDAY"
```

- **CT-51 nasceu da revisão adversarial.** O campo `codigo` **nunca era alterado em cenário algum**:
  CT-13 e CT-16 criam, CT-15 cria em outro tenant, CT-46 cria depois de excluir, e CT-14 é
  explicitamente *"salvar **sem mudar** o código"*. A linha do checklist
  *"Criação ≠ edição ≠ uso | CT-13 × CT-14"* era **falsa** — CT-14 é o caso de auto-colisão, não o
  lado-edição da unicidade. Corrigida.
- **CT-53 nasceu da revisão adversarial e fecha a lacuna L-01.** A versão anterior usava a premissa
  ("a barreira real em single-tenant é o formulário") **para não escrever um cenário perfeitamente
  escrevível** — que é exatamente o que a skill proíbe: premissa de mecanismo fixa **qual** cenário
  escrever, nunca **se** ele existe. CT-53 é também o **cenário por fora do componente de UI** que o
  gate de camada exige para R5, e que a regra não tinha.
  > **Este cenário pode nascer vermelho contra o desenho atual do PRD**, e isso é resultado válido:
  > em modo single-tenant `tenant_id` é `NULL`, e a maioria dos bancos (SQLite inclusive) **não
  > considera dois `NULL` iguais** — o índice `unique(['tenant_id','codigo'])` não barra nada ali.
  > RQ-14 diz que *"o código do cupom não pode se repetir"*, sem ressalva de modo. Vermelho aqui é a
  > divergência entre requisito e desenho, e vai para "Desvios do Plano", **não** para um
  > relaxamento da asserção. → **Q-08**.
- **Estouro do teto (6 > 3), justificado**: dois pontos de entrada (criação e edição) × duas
  camadas (tela e fora da tela), mais o alfabeto/comprimento, mais a auto-colisão.
- **CT-13 não usa `PROMO10` × `BLACKFRIDAY`**: palavras diferentes não discriminam normalização.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M5.1 | a normalização vive no formulário e não no model | **CT-53** *(antes: "CT-13 parcial + lacuna")* |
| M5.2 | `strtoupper` no lugar de `mb_strtoupper` | **CT-16** (linha `ação10`) |
| M5.3 | `trim` esquecido | **CT-13, CT-51, CT-53** |
| M5.4 | unicidade **global** em vez de por organização | **CT-15** |
| M5.5 | unicidade sem `ignoreRecord` — auto-colisão | **CT-14** |
| M5.6 | `maxLength` só no formulário; a coluna trunca em silêncio | **CT-16** (linha de 41) |
| M5.7 | a regra de unicidade é aplicada só na página de criação | **CT-51** |

---

## Regra R6 — só o admin cria, edita e exclui

> `RQ-07` · área A3 · perfil **completo** · técnica: **matriz papel × verbo** + **cenário por fora do
> componente de UI**

```gherkin
    Esquema do Cenário: [CT-17] a permissão de escrita de cupom existe só para quem administra
      Dado a matriz de papéis do kit semeada
      Quando se verifica se o papel "<papel>" tem a permissão "<verbo>:Cupom"
      Então o resultado é "<tem>"

      Exemplos:
        | papel             | verbo   | tem | # observação                                       |
        | panel_user        | Create  | não | RQ-07                                              |
        | panel_user        | Update  | não | RQ-07 — verbo irmão, falsificado separadamente     |
        | panel_user        | Delete  | não | RQ-07 — verbo irmão, falsificado separadamente     |
        | panel_user        | ViewAny | sim | RQ-08 — a subtração não pode levar a leitura junto |
        | admin_organizacao | Create  | sim | multi-tenant                                       |
        | admin_organizacao | Update  | sim | multi-tenant                                       |
        | admin_organizacao | Delete  | sim | multi-tenant                                       |
        | admin             | ViewAny | não | painel admin — não alcança o /app. Ver Q-09        |
        | infra             | ViewAny | não | painel infra — não alcança o /app                  |

    Esquema do Cenário: [CT-18] as telas de escrita respondem por URL direta só para quem administra
      Dado a organização Acme com um cupom ativo "PROMO10"
      Quando "<quem>" pede a URL de "<rota>" de cupom da Acme
      Então a resposta é <codigo>

      Exemplos:
        | quem                    | rota    | codigo | # o que a linha prova                          |
        | o operador Caio         | criação | 403    | RQ-07, verbo criar, por fora do componente     |
        | o operador Caio         | edição  | 403    | RQ-07, verbo editar, por fora do componente    |
        | a administradora Helena | criação | 200    | RQ-01 — a tela existe **no painel**, e responde |
        | a administradora Helena | edição  | 200    | RQ-01 — idem                                    |

    Esquema do Cenário: [CT-19] as ações de escrita aparecem só para quem administra
      Dado a organização Acme com um cupom ativo "PROMO10"
      Quando "<quem>" abre a listagem de cupons da Acme
      Então a ação de criar cupom "<visibilidade>" na página
      E a ação de excluir "<visibilidade>" para o cupom "PROMO10"

      Exemplos:
        | quem                    | visibilidade | # persona |
        | o operador Caio         | não existe   | só lê     |
        | a administradora Helena | existe       | escreve   |

    Esquema do Cenário: [CT-50] o usuário comum não consegue excluir nem contornando a visibilidade da ação
      Dado a auditoria de console ligada
      E a organização Acme com o cupom "PROMO10" na situação "<situacao>", com <usos> usos feitos, <usos> linhas na trilha e 1 linha na auditoria
      E o operador Caio, usuário comum do negócio da Acme
      Quando ele dispara a ação de exclusão desse cupom contornando a visibilidade dela
      Então a ação é recusada
      E o cupom "PROMO10" continua existindo
      E a trilha desse cupom continua com <usos> linhas
      E a auditoria desse cupom continua com 1 linha

      Exemplos:
        | situacao | usos | # célula da matriz    |
        | ativo    | 1    | E1 × excluir × comum  |
        | esgotado | 3    | E3 × excluir × comum  |

    Esquema do Cenário: [CT-55] em instalação sem organizações, só quem administra a instalação cadastra
      Dado a instalação em modo single-tenant, com a matriz de papéis semeada
      E que não existe nenhum cupom cadastrado
      Quando "<quem>" tenta cadastrar um cupom "BEMVINDO" pelo painel de negócio
      Então o resultado é "<resultado>"
      E o número de cupons da instalação é <total>

      Exemplos:
        | quem              | resultado | total | # persona                         |
        | a operadora Marta | aceito    | 1     | administra a instalação           |
        | o operador Caio   | 403       | 0     | usuário comum — RQ-07 no default  |
```

- **CT-50 nasceu da revisão adversarial**, e fecha o buraco de **um dos três verbos de RQ-07**.
  `excluir` **não tem rota** — é ação de tabela —, então CT-18 (que entra pelas rotas de criação e
  edição) **não o cobre**. CT-17 consulta a **string de permissão no seeder** e CT-19 prova
  **affordance** (o botão some). Nenhum dos três **dispara a exclusão** como usuário comum. O item
  do checklist *"Autorização exercida na ação (não só `can()`) → CT-18"* era **falso para `excluir`**.
  **M6.4 remapeado.**
- **CT-55 nasceu da revisão adversarial.** A versão anterior **declarava em prosa** que a variante
  single-tenant tinha "uma linha própria no mesmo `Esquema`" de CT-17 — e ela **não existia**. O
  Setup Global nomeava `$mestre` como *"quem cria cupom neste modo"* e **nenhum cenário afirmava que
  ele podia**. Em modo single-tenant — o **default do kit** — RQ-07 ficava **sem cenário positivo
  nenhum**.
- **CT-18, CT-19 e CT-22 viraram `Esquema`.** A revisão apontou ações escondidas **dentro do
  `Então`** (uma segunda requisição HTTP, uma segunda persona, um segundo render): pior que um
  segundo `Quando`, porque não são declaradas e, na falha, não se sabe qual metade quebrou.
  Parametrizadas, cada uma volta a ter **um único `Quando`**.
- **CT-17 falsifica cada verbo separadamente** — verbo irmão não herda evidência.
- **Achado registrado, não corrigido (Q-09)**: o `00`, item A-02, defende P-02 dizendo que
  *"`master_global` **e o papel `admin`** continuam alcançando a tela por herança do `Gate::before`"*.
  A linha `admin / ViewAny / não` de CT-17 afirma o contrário. **As duas não podem estar certas**, e
  se `admin` não alcança o `/app`, a terceira razão que sustenta P-02 é falsa e a premissa
  **restringe** RQ-07 em vez de preservá-la. O `00` é imutável nesta execução: registrado como
  pergunta, com o cenário que a resolve.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6.1 | o Resource entra na subtração **inteira** — o comum perde `ViewAny:Cupom` | **CT-17** (linha `ViewAny`) + **CT-21** |
| M6.2 | o Resource fica **fora** de qualquer subtração | **CT-17, CT-18, CT-50** |
| M6.3 | o recorte é por substring do nome e atinge um `CupomUsoResource` futuro | **lacuna declarada L-06** |
| M6.4 | a barreira vive só no `->visible()` da ação de excluir | **CT-50** *(corrigido — antes apontava CT-18, que não cobre `excluir`)* |
| M6.5 | o recorte cobre `Create` e esquece `Delete` | **CT-17** (linha `Delete`) + **CT-50** |
| M6.6 | as ações continuam visíveis para quem não pode usá-las | **CT-19** |
| M6.7 | a policy de exclusão devolve sempre `true`, e a única barreira é a permissão do papel | **CT-50** |
| M6.8 | em single-tenant ninguém consegue criar cupom (o painel fica inerte) | **CT-55** |

---

## Regra R7 — os demais usuários apenas listam, e só os ativos

> `RQ-08` · áreas A3+A7 · perfil **completo** · técnica: **matriz (coluna `listar`)** + **EP exaustiva
> do estado exibido**

```gherkin
    Esquema do Cenário: [CT-20] a listagem esconde os inativos de quem não pode editar
      Dado a organização Acme com quatro cupons — "ATIVO", "VENCIDO", "CHEIO" e "VENCIDO-E-CHEIO" —, um em cada situação
      Quando "<quem>" abre a listagem de cupons da Acme
      Então o cupom "ATIVO" aparece na lista
      E os cupons "VENCIDO", "CHEIO" e "VENCIDO-E-CHEIO" "<visibilidade>" na lista
      E a lista tem <total> registros

      Exemplos:
        | quem                    | visibilidade | total | # persona                                          |
        | a administradora Helena | aparecem     | 4     | escreve — nome do papel e permissão coincidem      |
        | o operador Caio         | não aparecem | 1     | só lê — nome do papel e permissão coincidem        |
        | a operadora Marta       | aparecem     | 4     | escreve **sem** o papel de organização — desacopla |

    Cenário: [CT-21] o usuário comum continua enxergando a entidade cupom
      Dado a matriz de papéis do kit semeada
      E a organização Acme com o cupom ativo "PROMO10"
      E o operador Caio, usuário comum do negócio da Acme
      Quando ele abre a listagem de cupons da Acme
      Então o cupom "PROMO10" aparece na lista
      E a lista tem 1 registro

    Esquema do Cenário: [CT-22] o cupom de outra organização não é alcançável por via nenhuma
      Dado a organização Acme com o cupom ativo "SOMENTE-ACME"
      E a organização Globex com o cupom ativo "SOMENTE-GLOBEX"
      E a administradora Helena, que administra as duas organizações
      Quando ela tenta alcançar o cupom "SOMENTE-GLOBEX" pela "<via>", dentro do painel da Acme
      Então "<resultado>"
      E o cupom "SOMENTE-GLOBEX" continua existindo na Globex

      Exemplos:
        | via           | resultado                                                                          | # via      |
        | listagem      | o cupom "SOMENTE-GLOBEX" não aparece na lista, que tem 1 registro — "SOMENTE-ACME" | tabela     |
        | URL de edição | a resposta é 404                                                                   | route bind |

    Esquema do Cenário: [CT-23] a situação exibida cobre todas as combinações do estado derivado
      Dado um cupom com validade "<validade>" e <usos> usos feitos de um limite de 3
      Quando a administradora Helena abre a listagem de cupons
      Então a situação exibida desse cupom é "<situacao>"

      Exemplos:
        | validade | usos | situacao | # estado                     |
        | futura   | 0    | Ativo    | E1                           |
        | passada  | 0    | Expirado | E2                           |
        | futura   | 3    | Esgotado | E3                           |
        | passada  | 3    | Esgotado | E4 — esgotado vence expirado |
```

- **CT-20 foi reescrito, e era o pior cenário do conjunto anterior.** A versão antiga tinha
  `inativos = (nenhum)` na linha do operador — materializado, isso é
  `assertCanSeeTableRecords([])`: **asserção sobre conjunto vazio**. Em lugar nenhum do conjunto
  existia a frase "não aparece na lista" para um cupom inativo, e ainda assim a prosa deste arquivo
  afirmava *"o `Então` afirma os dois lados"*. **A prosa auditava um cenário que não fora escrito.**
  Agora há a frase de ausência **e** o total de registros — porque só a frase de ausência ainda
  passaria com uma consulta que devolve nada para todo mundo.
- **CT-21 perdeu o `Então` `"a página responde com sucesso"`** — `Então` sem valor concreto que dava
  aparência de oráculo. Ficou o que discrimina.
- **CT-23 é partição exaustiva**, não amostra. A linha **E4** fixa a **precedência**.
- **CT-22 é o item IDOR**, com dois usuários e duas organizações no `Dado`, e afirma o terceiro lado.
  A administradora opera as duas de propósito — sem isso mediria o barramento, não o recorte.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M7.1 | o recorte de "ativos" é aplicado a **todo mundo** | **CT-20** (linha da administradora, `total = 4`) |
| M7.2 | o recorte não é aplicado a ninguém | **CT-20** (linha do operador — *corrigido: a versão anterior não o matava*) |
| M7.3 | o recorte olha o **nome do papel**, não a permissão | **CT-20** (linha da **Marta**) — *a versão anterior tinha só Helena e Caio, em que nome de papel e permissão **coincidem**: `hasRole()` e `can()` davam o mesmo resultado nas duas linhas e o mutante atravessava* |
| M7.4 | "ativo" considera só a validade e ignora o limite | **CT-20** (`CHEIO` visível ao operador) + **CT-23** |
| M7.5 | a ordem do `match` inverte: expirado vence esgotado | **CT-23** (linha E4) |
| M7.6 | o recorte de organização vive só na tabela e não no route binding | **CT-22** (linha `URL de edição`) |
| M7.7 | o recorte de escrita leva `ViewAny` junto e a listagem devolve 403 | **CT-21** |
| M7.8 | a listagem devolve **nada** para todo mundo | **CT-20** (as duas linhas afirmam o total) |

---

## Regra R8 — a aplicação recusa código que não existe

> `RQ-09` · área A2 · perfil **completo** · técnica: **EP (ausente ≠ `null` ≠ vazio)** + a coluna
> `validar` da matriz

```gherkin
    Esquema do Cenário: [CT-24] só um código realmente cadastrado é localizado
      Dado a organização Acme com o cupom ativo "PROMO10"
      Quando o sistema tenta localizar o código "<entrada>"
      Então "<resultado>"

      Exemplos:
        | entrada   | resultado                   | # partição          |
        | PROMO10   | o cupom PROMO10 é devolvido | válida              |
        | promo10   | o cupom PROMO10 é devolvido | válida, normalizada |
        | NAOEXISTE | nada é devolvido            | inexistente         |
        | (ausente) | nada é devolvido            | ausente             |
        | ""        | nada é devolvido            | vazio               |
        | "   "     | nada é devolvido            | só espaços          |

    Cenário: [CT-25] o código de outra organização não é encontrado
      Dado a organização Acme sem nenhum cupom
      E a organização Globex com o cupom ativo "SOMENTE-GLOBEX"
      E que o contexto corrente é o da organização Acme
      Quando o sistema tenta localizar o código "SOMENTE-GLOBEX"
      Então nada é devolvido
      E o cupom "SOMENTE-GLOBEX" continua ativo na Globex

    Esquema do Cenário: [CT-26] localizar o código só devolve cupom ativo, e o motivo da recusa distingue as três cláusulas
      Dado um cupom "PROMO10" na situação "<situacao>"
      Quando o sistema tenta localizar o código "PROMO10"
      Então "<resultado>"
      E o registro de operação do sistema traz o motivo "<motivo>"

      Exemplos:
        | situacao            | resultado                   | motivo              | # estado |
        | ativo               | o cupom PROMO10 é devolvido | (nenhum registro)   | E1       |
        | expirado            | nada é devolvido            | expirado            | E2       |
        | esgotado            | nada é devolvido            | esgotado            | E3       |
        | expirado e esgotado | nada é devolvido            | esgotado            | E4       |
```

- **CT-26 teve o `E` do log parametrizado.** A versão anterior dizia *"traz o motivo da recusa
  **quando há recusa**"* — condicional, e com "o motivo" fora do `Esquema`: um log único
  `"cupom inválido"` satisfazia E2, E3 e E4, e a legenda da coluna `validar` prometia mais do que
  entregava. Agora `motivo` é **coluna**, e a linha E4 fixa também a **precedência** no motivo.
  A asserção continua **secundária** — o oráculo é o cupom devolvido ou não, e RQ-09/10/11
  continuam falsificáveis sem ela pela situação de partida de cada linha.
- **CT-26 resolve a coluna `validar` inteira** — quatro estados, quatro linhas, cada uma com
  situação de partida declarada.
- **CT-25 é isolamento, não validação** — daí afirmar o terceiro lado.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M8.1 | código vazio cai numa consulta que devolve o **primeiro** cupom | **CT-24** (linhas vazio e só espaços) |
| M8.2 | a busca não normaliza | **CT-24** (linha `promo10`) |
| M8.3 | a busca ignora o escopo de organização | **CT-25** |
| M8.4 | a busca localiza e **as três validações ficam para quem chama** | **CT-26** (E2, E3, E4) |
| M8.5 | os filtros de situação são ligados por `OR` sem agrupamento e escapam dos demais | **CT-26** (E4 — a única linha em que os dois falham juntos) |
| M8.6 | o motivo registrado é o mesmo para as três recusas | **CT-26** (coluna `motivo`) |

---

## Regra R9 — a aplicação recusa cupom fora da validade

> `RQ-10` · área A4 · perfil **padrão** com **técnica escalada a BVA 3-valores** · incremento
> **1 segundo**

```gherkin
    Esquema do Cenário: [CT-27] a validade termina no instante gravado
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PRAZO" com validade em <validade>, 0 usos de um limite de 5
      Quando o sistema tenta localizar o código "PRAZO"
      Então "<resultado>"

      Exemplos:
        | validade            | resultado                 | # borda     |
        | 15/08/2026 11:59:59 | nada é devolvido          | borda − 1 s |
        | 15/08/2026 12:00:00 | nada é devolvido          | borda exata |
        | 15/08/2026 12:00:01 | o cupom PRAZO é devolvido | borda + 1 s |

    Cenário: [CT-28] a validade é comparada por instante, não por dia
      Dado o relógio congelado em 15/08/2026 14:00:00
      E um cupom "PRAZO" que venceu em 15/08/2026 10:00:00, com 0 usos de um limite de 5
      Quando o sistema tenta localizar o código "PRAZO"
      Então nada é devolvido

    Cenário: [CT-29] o cupom que vence entre a validação e o consumo não é consumido
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PRAZO" com validade em 15/08/2026 12:00:30, 2 usos de um limite de 5 e 2 linhas na trilha
      E a compradora Marina identificada
      E que o sistema já localizou o cupom "PRAZO" com sucesso
      Quando o relógio avança para 15/08/2026 12:01:00 e o sistema aplica esse cupom a um total de 10.000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom continua 2
      E a trilha do cupom continua com 2 linhas
```

- **CT-28 é o cenário discriminante do item *timezone / virada de dia***: o parâmetro livre é o
  **instante da observação**. Vencido às 10:00 e observado às 14:00 **do mesmo dia** é a única janela
  em que `where('expira_em','>', now())` e `whereDate('expira_em','>=', today())` divergem. Observar
  no dia **seguinte** não discriminaria nada.
- **CT-29** parte de **2 usos e 2 linhas** — não de zero — para que os dois `Então` de não-efeito
  tenham alvo real.
- **Lacuna L-03 (fuso do app × fuso de quem digita)**: `config('app.timezone')` é `UTC`. **Tentado**:
  (a) `config(['app.timezone' => 'America/Sao_Paulo'])` em teste — tarde, o
  `date_default_timezone_set()` já rodou no bootstrap; (b) `date_default_timezone_set()` junto — o
  SQLite grava e lê no mesmo fuso do processo, então **app e banco continuam concordando** e o
  mutante some; (c) `visit()->withTimezone(...)` — muda o **navegador**, não o banco. **Não é
  falsificável neste arnês**; o que a decide é **Q-07**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M9.1 | `>=` no lugar de `>`: vale no instante em que vence | **CT-27** (borda exata) |
| M9.2 | comparação por dia em vez de por instante | **CT-28** |
| M9.3 | a validade é conferida só ao localizar e não ao consumir | **CT-29, CT-10** |
| M9.4 | o filtro compara com uma data fixa em vez de `now()` | **CT-27** (as três linhas divergem) |
| M9.5 | a coluna é gravada como `date` e a hora se perde | **CT-27, CT-28, CT-01** |

---

## Regra R10 — a aplicação recusa cupom com o limite esgotado

> `RQ-11` · área A2 · perfil **completo** · técnica: **BVA 3-valores** + **concorrência** +
> **2-switch**

```gherkin
    Esquema do Cenário: [CT-30] o limite é inclusivo no último uso disponível
      Dado um cupom "LIMITE" válido, com limite de <limite> usos e <ja_usado> usos já feitos
      Quando o sistema tenta localizar o código "LIMITE"
      Então "<resultado>"

      Exemplos:
        | limite | ja_usado | resultado                  | # borda                       |
        | 3      | 1        | o cupom LIMITE é devolvido | dentro                        |
        | 3      | 2        | o cupom LIMITE é devolvido | borda − 1                     |
        | 3      | 3        | nada é devolvido           | borda                         |
        | 3      | 4        | nada é devolvido           | borda + 1                     |
        | 1      | 0        | o cupom LIMITE é devolvido | invariante de CT-11: limite 1 |
        | 1      | 1        | nada é devolvido           | invariante de CT-11: consumido |

    Cenário: [CT-31] duas aplicações disputando o último uso não estouram o limite
      Dado um cupom "ULTIMO" válido, de porcentagem com valor 29, com limite de 1 uso, 0 usos feitos e 0 linhas na trilha
      E dois compradores identificados, cada um com a sua leitura do mesmo cupom feita antes da primeira aplicação
      Quando os dois aplicam esse cupom a um total de 10.000 centavos, um depois do outro
      Então a primeira aplicação devolve 7.100 centavos
      E a segunda aplicação é recusada
      E o contador de usos do cupom é 1
      E a trilha do cupom tem exatamente 1 linha

    Cenário: [CT-32] o cupom que volta a ter limite continua contando de onde parou
      Dado um cupom "VOLTA" válido, com limite de 3 usos, 3 usos já feitos e 3 linhas na trilha
      E que a administradora Helena opera o painel de negócio da Acme
      E a compradora Marina identificada
      Quando Helena aumenta o limite para 5 e Marina aplica o cupom a um total de 10.000 centavos
      Então a aplicação é aceita
      E o contador de usos do cupom é 4
      E a trilha do cupom tem 4 linhas
```

- **CT-31 teve o `Então` corrigido.** A versão anterior dizia *"a primeira aplicação devolve 10.000
  **menos o desconto**"* — não é um número, é a fórmula comparada consigo mesma, e **qualquer**
  desconto (inclusive zero) a satisfazia. O `Dado` também não fixava `tipo` nem `valor`. Agora o
  cupom é `porcentagem 29` e o `Então` é **7.100**: um `aplicarEm` que não desconta nada mas
  incrementa o contador passava no cenário inteiro.
- **O que torna CT-31 discriminante é o `Dado`**: as duas leituras são feitas **antes** da primeira
  aplicação, ou seja, a segunda opera sobre um registro **obsoleto em memória**. *Ler-comparar-salvar*
  vê `usos = 0` na sua cópia, passa e grava — o contador fica em 1 **e a trilha ganha 2 linhas**. É a
  contagem da trilha que separa as duas implementações.
- **CT-30 ganhou as duas linhas de `limite 1`** — é onde o invariante de CT-11 passou a viver.
- **Lacuna L-02 — o que CT-31 *não* prova**: a barreira contra **leitura obsoleta**, sim; o
  comportamento sob dois *writers* de processos diferentes, não. **Tentado**: (a) `:memory:` dá uma
  conexão só; (b) arquivo SQLite + segunda conexão esbarra na transação do `RefreshDatabase`;
  (c) `--parallel` distribui **arquivos**, não cenários. Só observável em MySQL.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M10.1 | `<=` no lugar de `<` — um uso a mais | **CT-30** (linhas borda) |
| M10.2 | ler `usos`, comparar e salvar `usos + 1` (*check-then-act*) | **CT-31** |
| M10.3 | o limite é lido do cupom e nunca comparado | **CT-30** |
| M10.4 | aumentar o limite **zera** o contador | **CT-32** |
| M10.5 | aumentar o limite apaga a trilha anterior | **CT-32** |
| M10.6 | a comparação usa `usos` da memória em vez do banco | **CT-31, CT-32** |
| M10.7 | a primeira aplicação consome o uso e **não desconta nada** | **CT-31** (afirma 7.100) |

---

## Regra R11 — aplicada, a operação desconta o valor calculado do total

> `RQ-12` · área A1 · perfil **completo** · técnica: **BVA** + **tabela de decisão por tipo** ·
> **valores escolhidos por discriminância**

```gherkin
    Esquema do Cenário: [CT-33] o desconto calculado sobre o total é exato em centavos
      Dado um cupom válido do tipo "<tipo>" com valor <valor>, limite de 5 usos e 0 usos feitos
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de <total> centavos
      Então o total devolvido é <final> centavos
      E o desconto registrado na trilha é <desconto> centavos

      Exemplos:
        | tipo        | valor | total | desconto | final | # o que este valor discrimina                 |
        | porcentagem | 29    | 10000 | 2900     | 7100  | inteiro × float: (int)(10000*0.29) daria 2899 |
        | porcentagem | 10    | 9999  | 999      | 9000  | truncar × arredondar: arredondar daria 1000   |
        | porcentagem | 5     | 50    | 2        | 48    | truncar × arredondar em valor pequeno (2,5)   |
        | fixo        | 1000  | 12990 | 1000     | 11990 | o fixo não é percentual do total              |
        | fixo        | 1000  | 1000  | 1000     | 0     | desconto igual ao total — o zero legítimo     |

    @premissa
    Cenário: [CT-34] o desconto nunca deixa o total negativo
      Dado um cupom válido do tipo fixo com valor 5.000 centavos, limite de 5 usos e 0 usos feitos
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 3.000 centavos
      Então o total devolvido é 0 centavos
      E o desconto registrado na trilha é exatamente 3.000 centavos
      E o desconto registrado nunca excede o valor original registrado

    Cenário: [CT-35] o desconto de 100% zera o total
      Dado um cupom válido do tipo porcentagem com valor 100, limite de 5 usos e 0 usos feitos
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 12.990 centavos
      Então o total devolvido é 0 centavos
      E o desconto registrado na trilha é 12.990 centavos
```

- **Nenhum exemplo de CT-33 é redondo.** `10% de 10.000` daria 1.000 nas duas implementações e seria
  decorativo. As três primeiras linhas foram escolhidas **calculando onde as implementações
  divergem**.
- **CT-33 exercita as duas partições do `tipo`** — o discriminador particiona também o **cálculo**.
- **CT-34 usa igualdade, não desigualdade.** A versão anterior dizia *"o desconto registrado **não é
  maior** que o valor original"* — e a revisão apontou: Q-02 já **decidiu** a direção (registra o
  **concedido**), então o número é conhecido, e `<=` deixa passar uma trilha que grava `0` ou `1`. A
  desigualdade ficou como **invariante adicional**, que é o seu papel.
- **CT-34 é `@premissa`** quanto ao valor registrado. Direção por **falha fechado**: a trilha existe
  para auditar, e registrar mais do que foi dado **mente para quem audita** → registra **3.000**.
  **Invariante que vale nas duas leituras**: *o total devolvido é 0, nunca negativo, e o desconto
  registrado nunca excede o valor original*. **Se negado, só o segundo `E` inverte.** → **Q-02**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11.1 | percentual calculado em `float` e convertido para inteiro | **CT-33** (linha `29 / 10000`) |
| M11.2 | arredondar em vez de truncar | **CT-33** (linhas `9999` e `50`) |
| M11.3 | o desconto fixo é tratado como percentual (ou vice-versa) | **CT-33** (linhas `fixo`) |
| M11.4 | o desconto é **somado** ao total em vez de subtraído | **CT-33** (o `final` é afirmado) |
| M11.5 | sem piso: total final negativo | **CT-34** |
| M11.6 | a divisão por 100 guarda fração numa coluna inteira | **CT-33** (linha `50`) |
| M11.7 | a trilha registra o desconto **prometido** e não o concedido | **CT-34** (igualdade em 3.000) |

---

## Regra R12 — aplicada, a operação consome **exatamente um** uso

> `RQ-13` · área A2 · perfil **completo** · técnica: **rastreio de efeito**. **As quatro direções
> consomem o teto inteiro da regra**; ela não divide o teto com cenários de fronteira (R10).

```gherkin
    Cenário: [CT-36] a aplicação bem-sucedida consome um uso
      Dado um cupom "PROMO10" válido, com limite de 5 usos, 2 usos já feitos e 2 linhas na trilha
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 10.000 centavos
      Então o contador de usos do cupom é 3
      E a trilha do cupom tem 3 linhas

    Esquema do Cenário: [CT-37] a aplicação recusada não move o contador nem a trilha
      Dado um cupom "PROMO10" na situação "<situacao>", com limite de 3 usos, <usos> usos feitos e <usos> linhas na trilha
      E a compradora Marina identificada, que seria registrada na trilha no caminho feliz
      Quando o sistema tenta aplicar esse cupom a um total de 10.000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom continua <usos>
      E a trilha do cupom continua com <usos> linhas
      E o registro de operação do sistema traz o motivo "<motivo>"

      Exemplos:
        | situacao            | usos | motivo   | # estado |
        | expirado            | 1    | expirado | E2       |
        | esgotado            | 3    | esgotado | E3       |
        | expirado e esgotado | 3    | esgotado | E4       |

    Cenário: [CT-38] o contador não anda se a trilha não puder ser gravada
      Dado um cupom "PROMO10" válido, com limite de 5 usos, 2 usos já feitos e 2 linhas na trilha
      E a compradora Marina identificada
      E que a gravação da trilha vai falhar por violação de restrição do banco
      Quando o sistema tenta aplicar esse cupom a um total de 10.000 centavos
      Então a aplicação falha
      E o contador de usos do cupom continua 2
      E a trilha do cupom continua com 2 linhas

    Esquema do Cenário: [CT-39] o consumo acontece nos dois tipos de cupom
      Dado um cupom válido do tipo "<tipo>" com valor <valor>, limite de 5 usos, 1 uso feito e 1 linha na trilha
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 10.000 centavos
      Então o total devolvido é <final> centavos
      E o contador de usos do cupom é 2
      E a trilha do cupom tem 2 linhas

      Exemplos:
        | tipo        | valor | final | # partição do discriminador |
        | porcentagem | 29    | 7100  | um ramo                     |
        | fixo        | 1000  | 9000  | o outro ramo                |
```

- **As quatro direções, e por que nenhuma é decorativa**:
  - *aconteceu* → **CT-36**, partindo de `usos = 2` e não de 0: partir de zero não distingue
    "incrementou" de "gravou 1".
  - *não aconteceu quando não devia* → **CT-37**. **O mundo tem destinatário**: o cupom existe, a
    compradora existe, e a trilha já tem linhas que o caminho feliz aumentaria.
  - *aconteceu uma só vez* → **CT-31** (a disputa) e **CT-39** (o incremento é de 1, não do valor do
    desconto).
  - *atomicidade* → **CT-38**, com a falha injetada **depois** do ponto do efeito: o contador já foi
    movido quando a gravação da trilha estoura. Afirmar ausência numa **pré-validação**, onde nada
    seria gravado de qualquer forma, seria a mesma falha pelo outro lado.
- **CT-39 é a linha mais cara de esquecer**: com todos os cenários de consumo usando cupom de
  porcentagem, um atalho no ramo `fixo` — ignorando limite, validade e trilha — ficaria **verde no
  conjunto inteiro**. Nenhum par *(partição do discriminador, efeito rastreado)* fica sem cenário.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M12.1 | o incremento some (chamada removida) | **CT-36, CT-39** |
| M12.2 | o incremento acontece **antes** de validar | **CT-37** |
| M12.3 | o incremento soma o valor do desconto em vez de 1 | **CT-36** |
| M12.4 | o incremento e a trilha ficam **fora** da mesma transação | **CT-38** |
| M12.5 | o ramo `fixo` não consome uso | **CT-39** (linha `fixo`) |
| M12.6 | a recusa acontece **depois** do incremento | **CT-37** |
| M12.7 | a recusa devolve o total sem desconto em silêncio, sem sinalizar falha | **CT-37** (ver [o que "recusada" significa](#o-que-recusada-significa)) |

---

## Regra R13 — aplicada, a operação registra **quem** aplicou e **quando**

> `RQ-15` · área A6 · perfil **padrão** com **técnica escalada a rastreio de efeito completo** ·
> **teto de 3 estourado (5 cenários) — o custo declarado da técnica**

```gherkin
    Cenário: [CT-40] a aplicação registra quem aplicou e o instante em que aplicou
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PROMO10" válido de porcentagem com valor 29, limite de 5 usos e 0 linhas na trilha, criado neste instante
      E a compradora Marina identificada
      Quando o relógio avança para 15/08/2026 15:30:00 e o sistema aplica esse cupom a um total de 10.000 centavos
      Então a trilha do cupom tem 1 linha, atribuída à Marina e datada de 15/08/2026 15:30:00
      E essa linha registra o valor original de 10.000 centavos e o desconto de 2.900 centavos

    Esquema do Cenário: [CT-49] a trilha registra quem o sistema informou, nunca quem está autenticado
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PROMO10" válido, com limite de 5 usos e 0 linhas na trilha
      E a administradora Helena autenticada, operando o sistema
      E a compradora Marina, que não está autenticada
      Quando o sistema aplica esse cupom a um total de 10.000 centavos informando "<autor>" como quem aplicou
      Então a trilha do cupom tem 1 linha
      E essa linha está atribuída a "<atribuida>"
      E nenhuma linha da trilha está atribuída à Helena

      Exemplos:
        | autor      | atribuida | # partição do argumento                                  |
        | Marina     | Marina    | autor informado, diferente do autenticado                |
        | (ninguém)  | ninguém   | autor ausente — o ramo que jobs e comandos exercitam     |

    Esquema do Cenário: [CT-41] cada aplicação gera exatamente uma linha de trilha, em qualquer tipo
      Dado um cupom válido do tipo "<tipo>" com limite de 5 usos e 0 linhas na trilha
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom duas vezes, a totais de 10.000 e 20.000 centavos
      Então a trilha do cupom tem 2 linhas
      E as duas linhas estão atribuídas à Marina
      E os valores originais registrados são 10.000 e 20.000 centavos

      Exemplos:
        | tipo        | # partição do discriminador |
        | porcentagem | um ramo                     |
        | fixo        | o outro ramo                |

    Cenário: [CT-42] a trilha sobrevive ao desaparecimento de quem aplicou
      Dado o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PROMO10" válido, com limite de 5 usos
      E que a compradora Marina já aplicou esse cupom a um total de 10.000 centavos
      Quando a conta da Marina é excluída
      Então a trilha do cupom continua com 1 linha
      E essa linha não aponta mais para nenhuma pessoa
      E essa linha continua datada de 15/08/2026 12:00:00, com o valor original de 10.000 centavos

    Cenário: [CT-43] a trilha do uso não depende da auditoria genérica do kit
      Dado a auditoria de console ligada
      E um cupom "PROMO10" válido, com limite de 5 usos e 0 linhas na trilha
      E que uma edição anterior desse cupom deixou 1 linha na auditoria do kit
      E a compradora Marina identificada
      Quando o sistema aplica esse cupom a um total de 10.000 centavos
      Então a trilha do cupom tem 1 linha, atribuída à Marina
      E a auditoria do kit continua com 1 linha para esse cupom
```

- **CT-49 nasceu da revisão adversarial**, e fecha a **persona colapsada no eixo que RQ-15 nomeia**.
  Em CT-40…CT-43 a compradora era simultaneamente o argumento e o ator autenticado, e a implementação
  `'aplicado_por_id' => auth()->id()` (ou `$aplicadoPor?->getKey() ?? auth()->id()`) passava em
  todos. Em produção, um job, comando ou webhook sem sessão grava `NULL` — ou pior, **atribui o
  desconto ao operador logado em vez de a quem comprou**, que é exatamente o defeito de auditoria que
  o card pediu para prevenir. **M13.3 cobria só o caso `NULL`**; a atribuição à pessoa **errada** não
  tinha matador.
- **CT-42 perdeu o duplo `Quando`**: a aplicação foi para o `Dado` e o `Quando` ficou só com a
  exclusão da conta.
- **CT-43 torna a premissa P-08 do `00` falsificável.** O `Dado` **põe destinatário no mundo**: a
  auditoria de console está **ligada** e há **1 linha preexistente** provando que o mundo grava. Sem
  essas duas linhas, o `Então` passaria com a auditoria desligada — o falso ✅ mais fácil de cometer
  neste projeto.
- **CT-40 não afirma só a existência da linha** — afirma a **pessoa**, o **instante congelado** e os
  **dois valores**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M13.1 | a gravação da trilha some | **CT-40, CT-41** |
| M13.2 | a trilha grava sempre o mesmo total | **CT-41** (dois totais diferentes) |
| M13.3 | `aplicado_por_id` fica sempre nulo | **CT-40** |
| M13.4 | `created_at` não é gravado | **CT-40, CT-42** |
| M13.4b | `created_at` da trilha **copia o carimbo do cupom** (ou um instante capturado no início) em vez de `now()` | **CT-40** — *o relógio agora **avança** entre a criação e a aplicação; antes os dois instantes eram o mesmo número e a asserção não os distinguia* |
| M13.5 | excluir o usuário apaga a trilha (`cascadeOnDelete`) | **CT-42** |
| M13.6 | a trilha é substituída pela auditoria genérica — e nasce vazia | **CT-43** |
| M13.7 | `aplicado_por_id` vem de `auth()->id()` em vez do argumento | **CT-49** (linha `Marina`) |
| M13.8 | `aplicado_por_id` usa `$autor?->getKey() ?? auth()->id()` — o **fallback** que só produção exercita | **CT-49** (linha `(ninguém)`) — *a versão anterior sempre informava o autor, então o ramo do `??` nunca era executado* |

---

## Matriz — as colunas `editar` e `excluir`

Cenários que existem **por causa da matriz**, não de uma regra: são as células que nenhuma cláusula
`RQ` menciona junto daquela operação — e é por isso que somem quando a matriz é decomposta por regra.

```gherkin
    Esquema do Cenário: [CT-44] editar um cupom inativo produz o estado que a alteração determina
      Dado a auditoria de console ligada
      E o relógio congelado em 15/08/2026 12:00:00
      E um cupom "PROMO10" na situação "<situacao>", com limite de 3 usos e 1 linha na auditoria dele
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela altera "<campo>" para "<novo_valor>" e salva
      Então a gravação é aceita
      E o valor gravado de "<campo>" é "<novo_valor>"
      E a situação do cupom passa a ser "<situacao_final>"
      E a auditoria desse cupom passa a ter 2 linhas

      Exemplos:
        | situacao            | campo          | novo_valor          | situacao_final | # estado e por que esta linha existe        |
        | expirado            | expira_em      | 30/09/2026 23:59:00 | Ativo          | E2 — reentrada: a validade estendida reativa |
        | esgotado            | limite_de_usos | 5                   | Ativo          | E3 — reentrada: o limite aumentado reativa   |
        | expirado e esgotado | expira_em      | 30/09/2026 23:59:00 | Esgotado       | E4 — reabrir UMA dimensão não reabre a outra |

    Esquema do Cenário: [CT-45] excluir o cupom leva a trilha dele junto, e só a dele
      Dado a auditoria de console ligada
      E um cupom "ALVO" na situação "<situacao>", com <usos> usos feitos, <usos> linhas na trilha e 1 linha na auditoria
      E um segundo cupom ativo "VIZINHO", com 2 usos feitos e 2 linhas na trilha
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela exclui o cupom "ALVO"
      Então o cupom "ALVO" não existe mais
      E não existe nenhuma linha de trilha do cupom "ALVO"
      E o cupom "VIZINHO" continua existindo, com as suas 2 linhas de trilha
      E a auditoria do kit passa a ter 2 linhas para o cupom "ALVO"

      Exemplos:
        | situacao            | usos | # estado |
        | ativo               | 1    | E1       |
        | expirado            | 1    | E2       |
        | esgotado            | 3    | E3       |
        | expirado e esgotado | 3    | E4       |

    Cenário: [CT-46] o código de um cupom excluído volta a ficar disponível, sem herdar a trilha dele
      Dado um cupom ativo "BLACKFRIDAY" com 2 usos feitos e 2 linhas na trilha
      E que a administradora Helena já excluiu esse cupom
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela cadastra um novo cupom com o código "BLACKFRIDAY"
      Então a gravação é aceita
      E existe exatamente 1 cupom com o código "BLACKFRIDAY"
      E o contador de usos desse cupom é 0
      E esse cupom tem 0 linhas na trilha

    Cenário: [CT-47] operar sobre um cupom que não existe não encontra nada
      Dado a organização Acme com o cupom ativo "PROMO10"
      E que a administradora Helena opera o painel de negócio da Acme
      Quando ela pede a URL de edição de um identificador de cupom que não existe
      Então a resposta é 404
```

- **CT-44 foi reescrito com instantes concretos.** A versão anterior usava `novo_valor = "futuro"`, e
  o `Então` afirmava literalmente `expira_em === 'futuro'` — sem relógio congelado e sem instante, o
  materializador inventa o valor e "o gravado é o que eu acabei de mandar" vira **tautologia**.
  Comparado com CT-09, que já fazia certo, era inconsistência dentro do próprio arquivo.
- **CT-44 exercita a dimensão do *campo alterado* fora do estado inicial.** A linha **E4** prova que
  reabrir a validade **não** reabre o limite.
- **CT-45 foi reescrito em três pontos**: (a) o `Dado` passou a ter **um segundo cupom com trilha**,
  porque *"as linhas de trilha dos outros cupons continuam existindo"* era asserção sobre conjunto
  vazio — `CupomUso::truncate()` no `deleting` passava; (b) a linha **E1** passou de `usos = 0` para
  `usos = 1`, porque partir de zero e terminar em zero é vácuo; (c) o `audit.console` estava ligado
  no `Dado` **sem nenhuma asserção sobre `audits`** — setup morto, e a legenda da coluna `excluir`
  contava com ela. **M14.4 remapeado.**
- **CT-46 perdeu o duplo `Quando`** (a exclusão foi para o `Dado`) e **ganhou a asserção da trilha
  órfã**: um cupom novo que reaproveite o `id` do excluído nasceria com histórico alheio.
- **CT-46 é o item *unicidade + exclusão***. A exclusão física é **premissa de mecanismo** — fixa
  **como** escrever o cenário, não dispensa escrevê-lo. O mecanismo descartado (exclusão lógica, em
  que o registro apagado continuaria ocupando o código e podendo ser aplicado) é **L-04**.
- **CT-47 perdeu o `E o número de cupons continua 1`**: nenhuma implementação plausível de um `GET`
  cria ou apaga cupom — asserção decorativa. O mesmo corte foi feito em CT-18.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M14.1 | a situação derivada olha só a validade | **CT-44** (linha E4) |
| M14.2 | a edição é bloqueada em cupom inativo, e não há como renovar nada | **CT-44** (as três linhas) |
| M14.3 | a exclusão falha por restrição de chave estrangeira no cupom já usado | **CT-45** (E2, E3, E4) |
| M14.4 | a cascata apaga a trilha de **todos** os cupons | **CT-45** (o cupom `VIZINHO` — *corrigido: a versão anterior não o matava*) |
| M14.5 | o índice de unicidade não libera o código após a exclusão | **CT-46** |
| M14.6 | identificador inexistente devolve o primeiro registro | **CT-47** |
| M14.7 | a exclusão deixa `cupom_usos` órfã e o cupom novo herda o histórico | **CT-46** |
| M14.8 | a edição de cupom inativo não gera linha de auditoria | **CT-44** |

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | **CT-22**, **CT-25** |
| Autorização exercida na ação (não só `can()`) | **CT-18** (criar, editar) · **CT-50** (excluir) — *os três verbos, cada um por si* |
| ≥1 cenário por fora do componente de UI, por regra de **autorização** | **CT-18** (R6) |
| ≥1 cenário por fora do componente de UI, por regra de **validação de domínio** | **CT-54** (R2) · **CT-56** (R3) · **CT-57** (R4) · **CT-53** (R5) — *a 2ª rodada mostrou que R3 e R4 tinham a etiqueta sem o cenário: CT-08 e CT-10 são cenários de **invariante**, e o `Dado` de cada um **pressupõe** que a via alternativa aceita o valor inválido. Um cenário não mata o mutante cuja existência ele assume* |
| Invariante da premissa exercido mesmo se a barreira existir | **CT-08** (R3) · **CT-10** (R4) — com a fixture gravando **com as validações do model contornadas**, para não pressupor a ausência da barreira |
| Idempotência (ancorada no agregado **persistido**) | **lacuna declarada L-05** |
| Concorrência | **CT-31** (leitura obsoleta) + **lacuna declarada L-02** (dois *writers* reais) |
| Fronteira no ponto de entrada — **gravação** | **CT-06, CT-09, CT-11** |
| **Criação ≠ edição ≠ uso** | valor: **CT-06 × CT-07** · tipo: **CT-04 × CT-48** · validade: **CT-09 × CT-52** (as duas com BVA 3-valores) · código: **CT-13 × CT-51** · limite: **CT-11 × CT-12** — *a 1ª versão citava CT-13 × CT-14, que é auto-colisão, não o lado-edição; a 2ª tinha CT-52 com **um valor só** chamando-se BVA 3-valores* |
| Ausente ≠ `null` ≠ vazio, **no argumento de autoria** | **CT-49** (linha `(ninguém)`) — *antes o autor era sempre informado, e o ramo do fallback `?? auth()->id()`, que é o único que produção exercita, nunca era executado* |
| Domínio condicionado (`tipo` × `valor`) | **CT-06, CT-07, CT-33, CT-48** |
| Estado × operação de escrita (o inativo ainda funciona?) | **CT-37** (aplicar), **CT-44** (editar), **CT-45** (excluir) |
| Estado exibido — partição exaustiva do enum | **CT-23** (4 de 4) |
| Ciclo de volta (2-switch) | **CT-32**, **CT-44** (linha E4) |
| Ausente ≠ `null` ≠ vazio | **CT-24** (código), **CT-42** (quem aplicou) |
| Cardinalidade do destinatário (0 / 1 / N) | **CT-42** (0 — e **não** é citado como prova de não-efeito), **CT-40** (1), **CT-41** (N) |
| Paginação | **não se aplica**: o requisito não determina paginação → **Q-05** |
| Ordenação | **não se aplica como oráculo**: `defaultSort` só o PRD determina → **Q-05**. Nenhum cenário afirma ordem |
| Timezone / DST | **CT-28** (dia × instante) + **lacuna declarada L-03** (três tentativas registradas) |
| Unicode / limite de `varchar` | **CT-16** |
| Unicidade + exclusão | **CT-46**; mecanismo lógico descartado → **L-04** |
| CRUD combinado (inexistente, editar sem alterar, excluir) | **CT-47**, **CT-14**, **CT-45** |
| Mass assignment | **CT-03** (duas linhas, uma por campo) |
| Upload | **não se aplica**: a feature não recebe arquivo |
| Precisão monetária | **CT-33** (`29/10000`, `10/9999`, `5/50` — as três discriminam), **CT-34** |
| Efeito colateral — canal/destinatário exato | **não se aplica**: a feature não envia e-mail, não notifica e não enfileira |

### Lacunas declaradas

| # | O que fica sem matador | O que foi tentado | Pergunta |
|---|---|---|---|
| ~~L-01~~ | ~~unicidade em single-tenant~~ | **FECHADA pela revisão adversarial** → **CT-53**. A premissa estava sendo usada para não escrever um cenário **escrevível**, e o cenário pode nascer vermelho contra o desenho atual — o que é resultado válido | Q-08 |
| **L-02** | concorrência de **dois processos escritores reais** | (a) `:memory:` dá uma conexão só; (b) arquivo SQLite + segunda conexão esbarra na transação do `RefreshDatabase`; (c) `--parallel` distribui arquivos, não cenários. Só observável em MySQL | — |
| **L-03** | divergência entre o fuso do app e o de quem digita a validade | (a) `config(['app.timezone'])` em teste — tarde; (b) `date_default_timezone_set()` junto — app e SQLite passam a concordar e o mutante some; (c) `visit()->withTimezone()` — muda o navegador, não o banco | Q-07 |
| **L-04** | o cupom "removido" continuar aplicável, no mecanismo de **exclusão lógica** | a premissa é exclusão física; o cenário no mecanismo descartado exigiria uma coluna que não existe. Escrito no mecanismo assumido (CT-45, CT-46) | Q-01 |
| **L-05** | **idempotência** — "a mesma requisição duas vezes não cobra duas vezes" | o agregado que sofreria o efeito (o **pedido**) está fora de escopo por **P-01**. Ancorar no **cupom** provaria contabilidade; ancorar no **retorno** de duas chamadas seria tautológico numa função sem estado. **Inexpressável** | **Q-01** |
| **L-06** | o recorte de permissão feito por **substring** atingir um `CupomUsoResource` futuro | a entidade futura não existe; criar um Resource fantasma só para o teste mudaria a matriz de permissões do painel e quebraria `PaineisTest`. Mitigação é revisão de código, não cenário | — |
| **L-07** | **RQ-08 no modo single-tenant** — o default do kit. "Os demais usuários apenas listam os ativos" não tem cenário nenhum ali | o par observável **existe** (dono da instalação × usuário comum), mas exige decidir se o recorte de "ativos" vale para quem administra a instalação, e **o requisito não decide**. **Lacuna estrutural**, escalada em vez de fechada por decisão de teto de rodadas | **Q-12** |

> **L-05 não é falha do conjunto** — é consequência de uma decisão de escopo (P-01) que alguém precisa
> confirmar. É a única cuja resolução depende de resposta, não de arnês.

---

## Rastreabilidade `RQ` → falsificador

A tabela do [Mapa de Regras](#mapa-de-regras) prova que toda `RQ` **gerou regra**. Isto aqui prova o
que interessa: que ela **tem falsificador**. A revisão adversarial mostrou que o documento usava a
primeira como prova da segunda — e que **cinco cláusulas** tinham falsificação parcial.

| `RQ` | Antes da revisão | Agora | Falsificador |
|---|---|---|---|
| RQ-01 | **"no painel" não falsificado** | falsifica | CT-01, CT-02, CT-45 (gravação por componente) **+ CT-18, linhas de Helena** — *os três primeiros são testes de **componente** e passam com o Resource **não registrado no painel**; quem prova a metade "no painel" é a rota respondendo 200* |
| RQ-02 | falsifica | falsifica | CT-13, CT-16, **CT-51** |
| RQ-03 | falsifica | falsifica | CT-04, CT-05, **CT-54**, **CT-48** |
| RQ-04 | falsifica | falsifica | CT-01, CT-06, CT-07 |
| RQ-05 | **só criação** | falsifica | CT-09 (criação), **CT-52** (edição), CT-10 (uso) |
| RQ-06 | falsifica | falsifica | CT-11, CT-30, CT-12 |
| RQ-07 | **`excluir` só mencionado** | falsifica | CT-18 (criar, editar), **CT-50** (excluir), **CT-55** (o lado positivo em single-tenant) |
| RQ-08 | **metade sem oráculo** | falsifica **no modo multi-tenant**; **sem cenário no modo default** | **CT-20 reescrito** (asserção de ausência + total + a persona **Marta**, que desacopla nome de papel e permissão), CT-21, CT-23 — todos em `tests/Tenancy`. **Modo single-tenant: lacuna estrutural L-07 → Q-12** |
| RQ-09 | falsifica | falsifica | CT-24, CT-25, CT-26 |
| RQ-10 | falsifica | falsifica | CT-27, CT-28, CT-29, CT-10 |
| RQ-11 | falsifica | falsifica | CT-30, CT-31, CT-37 |
| RQ-12 | falsifica | falsifica | CT-33 (valores discriminantes), CT-34, CT-35 |
| RQ-13 | falsifica | falsifica | CT-36, CT-39, CT-31 |
| RQ-14 | **só criação** | falsifica | CT-13, CT-15 (criação), **CT-51** (edição), **CT-53** (fora da tela) |
| RQ-15 | **"quem" só contra `NULL`** | falsifica | **CT-40** (o **quando**, com o relógio **avançando** entre a criação e a aplicação), **CT-49** (o **quem**, contra a pessoa errada **e** contra o fallback do autenticado), CT-41, CT-42 |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-00 | o state da factory produz a situação que promete | *(arnês)* | EP | Feature | `tests/Kit/CupomTest.php` | guarda de fixture |
| CT-01 | o cadastro grava os cinco campos | R1 | EP | componente | `tests/Kit/CupomTest.php` | M1.1, M1.2, M1.5, M9.5 |
| CT-02 | a edição grava a alteração do valor | R1 | EP | componente | `tests/Kit/CupomTest.php` | M1.1 |
| CT-03 | campo fora do formulário não altera o registro | R1 | mass assignment | componente | `tests/Tenancy/CupomTenancyTest.php` | M1.3, M1.4 |
| CT-04 | cada tipo é gravável e volta como gravado | R2 | EP exaustiva | componente | `tests/Kit/CupomTest.php` | M2.2, M2.3 |
| CT-05 | tipo fora dos dois é recusado pela tela | R2 | EP inválida | componente | `tests/Kit/CupomTest.php` | — |
| CT-54 | tipo fora dos dois é recusado por fora da tela | R2 | **fora do componente** | Feature | `tests/Kit/CupomTest.php` | M2.1, M2.4 |
| CT-06 | fronteira de `valor` por tipo, na criação | R3 | BVA + decisão | componente | `tests/Kit/CupomTest.php` | M3.1, M3.2, M3.3 |
| CT-07 | a mesma fronteira na edição do valor | R3 | BVA | componente | `tests/Kit/CupomTest.php` | M3.4 |
| CT-48 | trocar o tipo revalida o valor contra o domínio novo | R3 | decisão (discriminador livre, 2 direções) | componente | `tests/Kit/CupomTest.php` | M3.6, M3.7, M3.8 |
| CT-56 | percentual acima de 100 barrado por fora da tela | R3 | **fora do componente** | Feature | `tests/Kit/CupomTest.php` | M3.5 |
| CT-08 | 150% no banco nunca desconta mais que o total | R3 | falha fechado + invariante | Feature | `tests/Kit/CupomTest.php` | — (invariante) |
| CT-09 | a validade gravada tem de estar no futuro | R4 | BVA (1 s) | componente | `tests/Kit/CupomTest.php` | M4.1 |
| CT-52 | a mesma fronteira de validade na edição | R4 | BVA 3-valores (1 s) | componente | `tests/Kit/CupomTest.php` | M4.1b, M4.6, M4.7 |
| CT-57 | validade no passado barrada por fora da tela | R4 | **fora do componente** | Feature | `tests/Kit/CupomTest.php` | M4.2 |
| CT-10 | validade passada no banco não é aplicável | R4 | invariante | Feature | `tests/Kit/CupomTest.php` | M9.3 |
| CT-11 | o limite gravado permite ao menos um uso | R4 | BVA | componente | `tests/Kit/CupomTest.php` | M4.3 |
| CT-12 | reduzir o limite abaixo dos usos é recusado | R4 | falha fechado + invariante | componente | `tests/Kit/CupomTest.php` | M4.4, M4.5 |
| CT-13 | o código é normalizado, na criação | R5 | normalização | componente | `tests/Kit/CupomTest.php` | M5.3 |
| CT-51 | a mesma unicidade e normalização na edição | R5 | normalização (2º ponto) | componente | `tests/Kit/CupomTest.php` | M5.3, M5.7 |
| CT-14 | salvar sem mudar o código não acusa colisão | R5 | EP (edição) | componente | `tests/Kit/CupomTest.php` | M5.5 |
| CT-15 | duas organizações, o mesmo código | R5 | EP + escopo | componente | `tests/Tenancy/CupomTenancyTest.php` | M5.4 |
| CT-16 | comprimento e alfabeto do código | R5 | EP + unicode | componente | `tests/Kit/CupomTest.php` | M5.2, M5.6 |
| CT-53 | código duplicado barrado por fora da tela | R5 | **fora do componente** | Feature | `tests/Kit/CupomTest.php` | M5.1 |
| CT-17 | a permissão de escrita só para quem administra | R6 | matriz papel × verbo | Feature | `tests/Tenancy/CupomTenancyTest.php` | M6.1, M6.2, M6.5 |
| CT-18 | as telas de escrita por URL, por persona | R6 + RQ-01 | **fora do componente** | Feature (HTTP) | `tests/Tenancy/CupomTenancyTest.php` | M6.2 |
| CT-19 | as ações de escrita só para quem administra | R6 | affordance | componente | `tests/Tenancy/CupomTenancyTest.php` | M6.6 |
| CT-50 | o comum não exclui nem contornando a visibilidade | R6 | **ação disparada** | componente | `tests/Tenancy/CupomTenancyTest.php` | M6.4, M6.5, M6.7 |
| CT-55 | em single-tenant, quem cria é o dono da instalação | R6 | matriz papel × modo | componente | `tests/Kit/CupomTest.php` | M6.8 |
| CT-20 | a listagem esconde os inativos de quem não edita | R7 | matriz `listar` × persona | componente | `tests/Tenancy/CupomTenancyTest.php` | M7.1, M7.2, M7.3, M7.4, M7.8 |
| CT-21 | o comum continua enxergando a entidade | R7 | matriz | componente | `tests/Tenancy/CupomTenancyTest.php` | M6.1, M7.7 |
| CT-22 | o cupom de outra organização não é alcançável | R7 | IDOR | Feature + componente | `tests/Tenancy/CupomTenancyTest.php` | M7.6 |
| CT-23 | a situação exibida cobre as quatro combinações | R7 | EP exaustiva do enum | componente | `tests/Kit/CupomTest.php` | M7.5 |
| CT-24 | só um código cadastrado é localizado | R8 | EP (ausente/null/vazio) | Feature | `tests/Kit/CupomTest.php` | M8.1, M8.2 |
| CT-25 | o código de outra organização não é encontrado | R8 | escopo | Feature | `tests/Tenancy/CupomTenancyTest.php` | M8.3 |
| CT-26 | localizar só devolve cupom ativo, com o motivo | R8/R9/R10 | matriz `validar` | Feature | `tests/Kit/CupomTest.php` | M8.4, M8.5, M8.6 |
| CT-27 | a validade termina no instante gravado | R9 | BVA (1 s) | Feature | `tests/Kit/CupomTest.php` | M9.1, M9.4, M9.5 |
| CT-28 | a validade é por instante, não por dia | R9 | valor discriminante de contexto | Feature | `tests/Kit/CupomTest.php` | M9.2 |
| CT-29 | o cupom que vence entre validar e consumir | R9 | ordem de eventos | Feature | `tests/Kit/CupomTest.php` | M9.3 |
| CT-30 | o limite é inclusivo no último uso | R10 | BVA | Feature | `tests/Kit/CupomTest.php` | M10.1, M10.3 |
| CT-31 | duas aplicações disputando o último uso | R10 | concorrência | Feature | `tests/Kit/CupomTest.php` | M10.2, M10.6, M10.7 |
| CT-32 | o cupom que volta a ter limite conta de onde parou | R10 | 2-switch | componente + Feature | `tests/Kit/CupomTest.php` | M10.4, M10.5 |
| CT-33 | o desconto calculado é exato em centavos | R11 | BVA + decisão | Feature | `tests/Kit/CupomTest.php` | M11.1…M11.4, M11.6 |
| CT-34 | o desconto nunca deixa o total negativo | R11 | falha fechado + invariante | Feature | `tests/Kit/CupomTest.php` | M11.5, M11.7 |
| CT-35 | o desconto de 100% zera o total | R11 | BVA (borda superior) | Feature | `tests/Kit/CupomTest.php` | M11.1, M11.2 |
| CT-36 | a aplicação bem-sucedida consome um uso | R12 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M12.1, M12.3 |
| CT-37 | a recusada não move contador nem trilha | R12/R13 | efeito + matriz `aplicar` | Feature | `tests/Kit/CupomTest.php` | M12.2, M12.6, M12.7 |
| CT-38 | o contador não anda se a trilha não gravar | R12 | atomicidade | Feature | `tests/Kit/CupomTest.php` | M12.4 |
| CT-39 | o consumo acontece nos dois tipos | R12 | partição × efeito | Feature | `tests/Kit/CupomTest.php` | M12.5 |
| CT-40 | registra quem aplicou e o instante em que aplicou | R13 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M13.1, M13.3, M13.4, M13.4b |
| CT-49 | registra quem o sistema informou, nunca o autenticado | R13 | persona distinta + EP no argumento | Feature | `tests/Kit/CupomTest.php` | M13.7, M13.8 |
| CT-41 | uma linha por aplicação, em qualquer tipo | R13 | partição × efeito | Feature | `tests/Kit/CupomTest.php` | M13.2 |
| CT-42 | a trilha sobrevive ao sumiço de quem aplicou | R13 | cardinalidade 0 | Feature | `tests/Kit/CupomTest.php` | M13.5 |
| CT-43 | a trilha não depende da auditoria genérica | R13 | não-efeito com destinatário | Feature | `tests/Kit/CupomTest.php` | M13.6 |
| CT-44 | editar um cupom inativo produz o estado determinado | matriz | matriz `editar` × campo | componente | `tests/Kit/CupomTest.php` | M14.1, M14.2, M14.8 |
| CT-45 | excluir leva a trilha junto, e só a dele | matriz | matriz `excluir` | componente | `tests/Kit/CupomTest.php` | M14.3, M14.4 |
| CT-46 | o código excluído volta a ficar disponível, sem herdar trilha | matriz | unicidade + exclusão | componente | `tests/Kit/CupomTest.php` | M14.5, M14.7 |
| CT-47 | operar sobre cupom inexistente não encontra nada | matriz | CRUD | Feature (HTTP) | `tests/Kit/CupomTest.php` | M14.6 |

**Distribuição por camada** — a escada foi aplicada com o teto real do arnês:

| Camada | Cenários | Observação |
|---|---|---|
| `Unit` | **0** | `tests/Unit` não tem `Tests\TestCase` ligado em `tests/Pest.php` — roda sem container |
| Feature (model direto) | 28 | inclui os **4 cenários por fora do componente** que o gate de validação de domínio exige (CT-53, CT-54, CT-56, CT-57) |
| Feature (HTTP) | 2 | CT-18 e CT-47 — inclui o cenário por fora do componente do gate de **autorização** |
| componente Livewire/Filament | 26 | validação, gravação, listagem, ação de tabela, autorização na tela |
| mistos (componente + Feature no mesmo cenário) | 2 | CT-22 e CT-32 |
| **total no `04`** | **58** | |
| Browser | 2 | ver `05-casos-de-teste-browser.md` |

**Por suíte**: 48 em `tests/Kit/CupomTest.php` (single-tenant) e 10 em
`tests/Tenancy/CupomTenancyTest.php` (multi-tenant). *A distribuição anterior declarava 27/29 —
número que **nenhuma leitura do índice produzia**, nem contando os mistos dos dois lados. Fechava por
compensação. Esta foi contada mecanicamente a partir das colunas do índice.*

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` está **fechado para edição** nesta execução. A skill manda
> replicar as perguntas em `## Ambiguidades` do `00`; como isso não é possível, o bloco abaixo está
> **pronto para colagem**. **As perguntas continuam bloqueando o que dependem delas** — nenhuma morreu
> por o arquivo de destino estar travado.

```markdown
### A-10 — vindas da derivação dos casos de teste (`04-casos-de-teste.md`)

- **Q-01 (RQ-12, RQ-13)** — aplicar o mesmo cupom duas vezes para o **mesmo pedido** consome dois
  usos, ou a segunda chamada é um *retry* que não cobra de novo?
  - **Assumido**: nada. O agregado que tornaria a pergunta observável (`Pedido`) está fora de escopo
    por P-01, e o cenário é **inexpressável** (lacuna L-05).
  - **Se respondido "é retry"**: nasce uma regra nova (chave de idempotência) e pelo menos dois
    cenários; L-05 deixa de ser lacuna.

- **Q-02 (RQ-15)** — quando o desconto excede o total, a trilha registra o desconto **prometido** ou
  o **concedido**?
  - **Assumido**: o **concedido** (falha fechado — trilha que registra mais do que foi dado mente
    para quem audita).
  - **Se negado**: o segundo `E` de CT-08 e de CT-34 inverte; os demais permanecem.

- **Q-03 (RQ-15)** — a trilha guarda o **valor sobre o qual o desconto incidiu** e o **desconto
  concedido**, ou só quem e quando?
  - **Assumido**: guarda os dois. **Se negado**: CT-40 e CT-41 perdem os `E` de valor.

- **Q-04 (RQ-03, RQ-04)** — qual o texto que declara a **unidade** do campo de valor em cada tipo?
  - **Assumido**: os rótulos do PRD. CT-B01 afirma que o rótulo **muda** e que o gravado corresponde
    ao exibido; o texto exato é detalhe.

- **Q-05 (RQ-01)** — a listagem tem ordem e paginação definidas pelo negócio?
  - **Assumido**: não. **Nenhum cenário afirma ordem nem paginação** — os itens do checklist estão
    "não se aplica" por esta razão, não por esquecimento.

- **Q-06 (RQ-08)** — as cores da situação na listagem são requisito?
  - **Assumido**: não. É a razão de **não** existir CT-B de cor.

- **Q-07 (RQ-10)** — a validade digitada é interpretada no fuso de quem digita ou no do servidor? O
  app roda em `UTC` (`config/app.php:68`).
  - **Assumido**: fuso do servidor. Lacuna L-03, com três tentativas de arnês.

- **Q-08 (RQ-14)** — em instalação **single-tenant**, a unicidade do código deve ser garantida pelo
  banco?
  - **Assumido**: RQ-14 não faz ressalva de modo, então **sim, o código não pode se repetir em
    nenhum modo** — e **CT-53** afirma isso. Como o índice composto não barra dois `NULL`, este
    cenário **pode nascer vermelho** contra o desenho atual, e o vermelho é a resposta.

- **Q-09 (RQ-07)** — **contradição encontrada no próprio `00`.** O item A-02 defende P-02 dizendo que
  *"`master_global` e o papel `admin` continuam alcançando a tela por herança do `Gate::before`"*.
  Mas `roles.painel` do papel `admin` é `'admin'`, e quem entra por `Gate::before` é só o
  `master_global`. Se `admin` **não** alcança o `/app`, a terceira razão que sustenta P-02 é falsa e
  a premissa **restringe** RQ-07 em vez de preservá-la.
  - **Assumido**: `admin` **não** alcança o `/app` — é o que **CT-17** afirma.
  - **Se negado**: a linha `admin / ViewAny` de CT-17 inverte, e a defesa de P-02 volta a fechar.

- **Q-10 (RQ-09…RQ-11)** — qual a **forma observável** da recusa ao aplicar? Exceção, retorno nulo,
  objeto de resultado?
  - **Assumido**: o mecanismo do PRD (exceção). **Invariante que vale em qualquer resposta**: quem
    chama consegue **separar "recusado" de "aplicado com desconto zero"** — as duas levam a cobranças
    diferentes. Sem fixar isso, o conjunto inteiro aceitaria "devolve o total sem desconto" como
    recusa.

- **Q-11 (RQ-06)** — limite de usos igual a 0 é permitido?
  - **Assumido**: **não** (falha fechado — um cupom de limite 0 nasce esgotado). Invariante em
    CT-30, linhas `limite 1`.

- **Q-12 (RQ-08)** — **em instalação single-tenant, que é o modo default do kit, o recorte "só os
  ativos" vale para quem administra a instalação?** No modo default os únicos papéis com acesso ao
  painel de negócio são o dono da instalação (que atravessa tudo por gate) e o usuário comum — então
  o par observável existe, mas quem é "os outros usuários" de RQ-08 ali depende desta resposta.
  - **Assumido**: nada. **RQ-08 fica sem cenário no modo default** → **lacuna estrutural L-07**.
  - **Se respondido**: R6 e R7 provavelmente viram duas regras cada, com `modo` como dimensão da
    matriz — ver *Achados estruturais escalados*.
```

---

## Revisão Adversarial

**Executada** por sub-agente independente, que recebeu **somente** o `00-requisito.md`, o `04` e o
`05` — nunca o PRD, o código, nem o raciocínio de quem derivou (conforme a proibição de
autorrevisão). Contrato: *provar que o conjunto deixa passar defeito*.

**35 achados.** Nenhum foi descartado. Destino de cada grupo:

| # | Achado | Virou |
|---|---|---|
| 1 | `tipo` editável sem revalidar `valor` (cupom `fixo` de R$ 200 vira **20000%**) | **CT-48** + M3.6 remapeado |
| 2 | `aplicado_por_id` de `auth()->id()` em vez do argumento — persona colapsada no eixo de RQ-15 | **CT-49** + M13.7 |
| 3, 6 | CT-20 sem o lado da ausência: `inativos = (nenhum)` é `assertCanSeeTableRecords([])` | **CT-20 reescrito** + M7.2 remapeado |
| 4 | `excluir` sem barreira **exercida** — CT-18 só cobre rotas, e `excluir` é ação de tabela | **CT-50** + M6.4 remapeado |
| 5 | unicidade e normalização só na criação; o campo `codigo` nunca era editado | **CT-51** |
| 5-bis | validade no passado validada só no `create` | **CT-52** + M4.6 remapeado |
| 7, 8 | CT-10 com não-efeito em mundo de saldo zero, e testando `localizar` quando o invariante fala de `aplicar` | **CT-10 reescrito** (operação `aplicar`, partida 2 usos / 2 linhas) |
| 9, 10 | CT-45 sem segundo cupom, com E1 partindo de zero, e `audit.console` ligado sem asserção | **CT-45 reescrito** + M14.4 remapeado |
| 11 | CT-31 com `Então` autorreferente ("10.000 menos o desconto") e sem `tipo`/`valor` no `Dado` | **CT-31 reescrito** (7.100) + M10.7 |
| 12 | CT-02 herdando o limite 200 de CT-01 | **`Dado` de CT-02 fechado** |
| 13 | CT-44 com `novo_valor = "futuro"` — tautologia | **CT-44 reescrito** com instantes concretos |
| 14 | CT-08 e CT-34 com desigualdade onde a igualdade é conhecida | **igualdade** + a desigualdade como invariante |
| 15 | CT-26 com o `E` do log condicional e o motivo fora do `Esquema` | **`motivo` virou coluna** + M8.6 |
| 16 | "a aplicação é recusada" sem forma observável | fixado em [O que "recusada" significa](#o-que-recusada-significa) + **Q-10** + M12.7 |
| 17 | CT-21 com `"a página responde com sucesso"` | asserção trocada pela que discrimina |
| 18 | CT-18 e CT-47 com não-efeito decorativo depois de um `GET` | asserções **removidas** |
| 19 | CT-46 sem afirmar a trilha órfã | **CT-46 reescrito** + M14.7 |
| 20 | ações escondidas **dentro do `Então`** em CT-18, CT-19, CT-22 | os três viraram **`Esquema`**, com um único `Quando` |
| 21 | duplo `Quando` injustificado em CT-42 e CT-46; CT-03 combinando duas partições inválidas | primeira ação movida para o `Dado`; **CT-03 virou `Esquema`** |
| 22 | contagem `20/14/6` incompatível com "8 observações" — e o colapso escondia as três recusas de RQ-08 | **contagem refeita nos dois níveis** (20 células, 31 observações, 15 recusas) |
| 23 | a legenda de `excluir` descrevia um `❌` que não existia, e era auditada por CT-45, que faz a operação **oposta** | **CT-50** deu à coluna a sua célula de recusa; **reauditoria refeita** |
| 24 | a legenda de `listar` auditada ✔ contra um cenário sem a asserção | corrigido junto com CT-20 |
| 25 | `excluir` obrigava `audits` e nenhuma célula afirmava | CT-45 e CT-50 afirmam |
| 26 | célula E1 × `editar` com `Dado` que não fecha | CT-02 corrigido |
| 27 | a dimensão "campo alterado" povoada só com os campos inócuos | **`tipo` e `codigo` entraram** (CT-48, CT-51) |
| 28 | critério de quando abrir dimensão não declarado | **declarado** na contagem da matriz |
| 29 | cabeçalho com "54 mutantes" (reais: 88) e "sem matador: 4" (reais: 5 lacunas) | **recontado** |
| 30 | direção das seis premissas por falha fechado — **nada a corrigir** | mantido |
| 31 | o invariante de CT-11 apontava CT-30, que só tinha `limite 3` | **duas linhas `limite 1`** em CT-30 |
| 32 | o invariante de CT-09 apontava CT-10, que executava outra operação | resolvido com a reescrita de CT-10 |
| 33 | **L-01 era premissa usada para não escrever cenário escrevível** | **CT-53**; L-01 **fechada** |
| 34 | contradição entre a defesa de P-02 no `00` e a linha `admin` de CT-17 | **Q-09** — achado registrado, `00` não editado |
| 35 | a linha single-tenant de CT-17 era declarada em prosa e **não existia** | **CT-55** |

**Padrão comum aos achados 3, 23, 24 e 35**: *a prosa afirmava a asserção que o Gherkin não continha.*
É a forma de falso ✅ mais difícil de ver, porque quem materializa lendo as tabelas de auditoria — e
não os `Então` — produz uma suíte verde com o defeito dentro.

### Segunda rodada

O fechamento da primeira criou **8 cenários novos** (CT-48…CT-55), e a skill manda re-revisar uma
única vez quando isso acontece, porque cenário novo introduz **superfície nova**. Executada por um
**segundo sub-agente independente**, com o mesmo isolamento de entrada e o alvo apontado para os
cenários novos e reescritos. **35 achados.** Os pontuais foram fechados:

| # | Achado | Virou |
|---|---|---|
| 1, 2 | **o gate "por fora do componente" estava etiquetado sem cenário em R3 e R4**: o `Dado` de CT-08 e CT-10 *pressupõe* que a via alternativa aceita o valor inválido — um cenário não mata o mutante cuja existência ele assume | **CT-56** e **CT-57**; CT-08 e CT-10 viraram cenários de **invariante puro**, com a fixture gravando *"com as validações do model contornadas"*. M3.5 e M4.2 remapeados |
| 3 | M7.3 (recorte por **nome do papel**) não era morto: Helena e Caio têm nome de papel e permissão **coincidentes** | **persona Marta** — administra **sem** o papel de organização — como terceira linha de CT-20 |
| 4 | `"a ação é recusada"` sem forma observável: com a barreira só em `->visible()`, o arnês recusa a chamada **porque a ação está escondida**, e CT-50 fica verde | [vocabulário de recusa](#vocabulário-de-recusa--forma-observável-fixada-para-cada-operação) fixado para **as cinco operações**; CT-50 exige **403** |
| 5 | CT-40 não falsificava o **"quando"** de RQ-15: o relógio congelado fazia o instante de criação do cupom e o da aplicação serem o **mesmo número** | **o relógio avança** entre o `Dado` e o `Quando` em CT-40 + **M13.4b** |
| 6 | CT-49 fechava metade do eixo: o autor era **sempre** informado, e o ramo `?? auth()->id()` — o único que produção exercita — nunca rodava | **CT-49 virou `Esquema`** com a linha `(ninguém)` + **M13.8** |
| 7, 8 | **CT-51 com `audit.console` ligado e sem asserção** (o defeito de CT-45 reproduzido num cenário novo), e três cenários novos fora da lista de pré-condição que existe para protegê-los | asserção de `audits` em CT-51; **lista refeita com os oito cenários** |
| 9, 10 | CT-54 e CT-53 com `Dado` de zero cupons — qualquer falha por motivo alheio (NOT NULL noutro campo) satisfazia *"a gravação falha"* | os dois partem de **1 cupom já cadastrado**, declaram os demais campos válidos, e CT-53 afirma **o código gravado** |
| 11 | CT-55 com segunda ação e segunda persona dentro do `Então` — o achado 20 da 1ª rodada reintroduzido | **CT-55 virou `Esquema`** |
| 13 | CT-52 chamado de BVA 3-valores com **um valor só** | **CT-52 virou `Esquema`** de 3 linhas + **M4.1b** |
| 14 | CT-48 abria uma direção do discriminador e deixava a inversa sem cenário — a troca legítima para `fixo` seria recusada por engano, sem matador | **CT-48 virou `Esquema`** de 3 linhas, com as duas direções + **M3.8** |
| 15 | CT-03 com `Então` em prosa (*"o contador não é reescrito pelo payload"*) e sem a Globex no `Dado` — podia ficar verde por FK inexistente | `Então` com **valor concreto por linha**; Globex no `Dado`; cenário movido para `tests/Tenancy` |
| 21, 22, 23, 25 | **as quatro contagens do documento erradas**: mutantes (declarava 96, real 101 → agora 105), lacunas (declarava 4, reais 5), perguntas (10 → 11), distribuição por camada (27/29, número que nenhuma leitura produzia) | todas **recontadas mecanicamente** a partir do próprio texto |
| 26 | a seção "Segunda rodada", **referenciada e inexistente**, declarando *executada* a rodada que ainda não rodara | esta seção |
| 27 | a matriz citava CT-50 na célula **E1 × excluir × comum**, e o `Dado` de CT-50 era **E3** — cenário certo, estado errado | **CT-50 virou `Esquema`** com `ativo` e `esgotado` |
| 28 | a contagem por coluna não batia com a matriz e **só fechava em 31 por dois erros que se cancelavam** (`excluir` +1 fantasma, `validar` −1 não renderizado) | contagem refeita **da matriz renderizada**; as 3 observações sem célula agora somam **fora** dela, declaradas |
| 29 | o critério de abrir dimensão era aplicado de forma inconsistente e as células ausentes não estavam declaradas | cada ausência classificada em **poda deliberada**, **não se aplica** ou **lacuna L-07** |
| 31 | a legenda exigia "o motivo" de `validar` e só "o log saiu" de `aplicar` — um log genérico satisfazia as três linhas de CT-37 | **coluna `motivo` em CT-37**; as duas linhas da legenda igualadas |
| 32 | RQ-01 ("CRUD **no painel**") era dado como falsificado por três testes de **componente**, que passam com o Resource não registrado no painel | **CT-18 ganhou as linhas positivas** (Helena → 200 nas duas rotas) |
| 12, 33, 34, 35 | modo do kit, RQ-08 e RQ-15 | ver [Achados estruturais escalados](#achados-estruturais-escalados) |

### Achados estruturais escalados

A skill fixa **teto de 2 rodadas** e é explícita: *"se a segunda rodada ainda trouxer achado
estrutural, o problema não é o conjunto — é a regra, que provavelmente deveria ser duas. Registrar e
escalar."* A segunda rodada trouxe **quatro**. Três foram absorvidos; **um é escalado sem correção**,
porque corrigi-lo é redesenhar o eixo de regras e isso é decisão de quem tem o requisito.

| # | Achado estrutural | Situação |
|---|---|---|
| **E1** | **o modo do kit (`single-tenant` × `multi-tenant`) é uma dimensão real que a matriz nunca abriu.** `admin_organizacao` não existe no modo **default**, e mesmo assim 26 cenários arquivados em `tests/Kit` nomeavam personas e organizações que só existem no outro modo — ou eram immaterializáveis, ou seriam materializados com outra persona, medindo outra autorização | **parcialmente absorvido**: as personas viraram [papéis narrativos com tabela de realização por suíte](#personas--papel-no-cenário-não-papel-do-kit), o que torna os 26 materializáveis. **O que fica aberto e é escalado: R6 e R7 deveriam ser duas regras cada** (*"quem escreve/lê em organização"* × *"quem escreve/lê em instalação única"*), com `modo` como coluna da matriz e do índice. Hoje **RQ-08 só tem cenário no modo multi-tenant**, e o default do kit é o outro → **lacuna L-07** |
| **E2** | **as correções da 1ª rodada foram aplicadas por instância, nunca promovidas a regra** — e por isso os cenários irmãos repetiram o mesmo defeito quatro vezes (log genérico, `audit.console` morto, ação escondida no `Então`, `Então` em prosa) | **absorvido**: virou os [critérios de aceitação de todo `Então`](#critérios-de-aceitação-de-todo-então), aplicados aos 58 cenários. É o item que impede a terceira rodada de achar a quinta ocorrência |
| **E3** | **"recusada" foi definido para uma operação e o buraco continuou aberto nas outras quatro** | **absorvido**: o vocabulário de recusa passou a ser tabela sobre **todas** as operações |
| **E4** | **o gate "por fora do componente" foi lido como "existe um cenário fora do componente" quando exige "a regra é exercida fora do componente"** | **absorvido**: CT-56 e CT-57 |

**L-07 — lacuna estrutural declarada.** *RQ-08 ("os demais usuários apenas listam os cupons ativos")
não tem cenário no modo single-tenant, que é o **default** do kit.* Tentado: os cenários de listagem
exigem duas personas com permissões diferentes no painel `/app`, e no modo default os únicos papéis
com acesso são `master_global` (que atravessa tudo pelo `Gate::before`) e `panel_user` — o que
**torna o par observável**, mas exige decidir se o recorte de "ativos" deve valer para o
`master_global`, e **o requisito não decide**. Vira a **pergunta Q-12**, e a resposta muda se R6/R7
viram duas regras. **Não fechado nesta invocação, por decisão de teto.**

> **Terceira rodada não foi executada, e é deliberado.** O teto da skill é 2. Rodar uma terceira sem
> antes redesenhar o eixo de regras encontraria a mesma classe de achado, porque a causa é o eixo, não
> os cenários.

---

## Ordem de execução recomendada

1. **CT-00** — sem a fixture correta, CT-30, CT-32, CT-37 e CT-45 medem um cupom ativo.
2. **CT-31** (consumo sob leitura obsoleta) — o PRD já registra que ele vem antes de qualquer CT-B:
   sem a barreira de consumo de pé, todo cenário de tela mede a coisa errada.
3. O restante do `04`.
4. O `05`, por último, e **em série**.

## Comandos

```bash
vendor/bin/pest --parallel --group=kit              # CT-00…CT-55 + a regressão de PaineisTest
vendor/bin/pest --testsuite=Browser                 # CT-B01, CT-B02 — em série, nunca --parallel
composer require pestphp/pest-plugin-mutate --dev   # antes do fechamento por mutação
```

> `--parallel --tia` **não entra**: `.ai/rules/testes-browser.md` vence a skill aqui.

## Fechamento por mutação (pós-implementação)

```bash
vendor/bin/pest tests/Kit/CupomTest.php --mutate --path=app/Models/Cupom.php
```

> **O que este número não responde**: mutation testing só muta **código que existe**. Se uma cláusula
> `RQ` nunca virou código — não há `if` de teto percentual para mutar —, **nenhum mutante é gerado e o
> score não cai**. Medido em experimento controlado: duas suítes com **100% de mutation score** na
> mesma classe detectaram **7** e **12** defeitos plantados. Quem responde por omissão aqui é a
> [Rastreabilidade `RQ` → falsificador](#rastreabilidade-rq--falsificador) e o gate de mutantes **de
> especificação** deste arquivo, que nasceram do requisito e por isso enxergam o que não foi escrito.
> **Não usar cobertura de linha como critério de suficiência.**
