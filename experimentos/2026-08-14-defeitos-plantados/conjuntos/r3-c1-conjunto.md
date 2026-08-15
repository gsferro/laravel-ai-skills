# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `../../exp-a/cupons-de-desconto/00-requisito.md` · Plano: `../../exp-a/cupons-de-desconto/01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação:
> `app/Models/Cupom.php`, `app/Services/*`, `app/Enums/*`, as migrations de cupom e as suítes
> `tests/Feature/ExpA` / `tests/Feature/ExpB` **não foram abertos**. Do projeto foram lidos apenas
> `tests/Pest.php`, `tests/Kit/PaineisTest.php`, `tests/Kit/ConviteUsuarioExistenteTest.php`,
> `tests/BrowserTenancy/IdentidadeVisualTest.php` e `.ai/rules/*` — para herdar **convenção de
> teste** (helpers, traits, seletores), nunca comportamento esperado.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| Cálculo do desconto (RQ-03, RQ-04, RQ-12) | 3 — regra com muitas condições: tipo × valor, arredondamento, teto em zero | 3 — dinheiro | **9** | **completo** |
| Aplicação: validação + consumo do uso (RQ-09 a RQ-13) | 3 — concorrência, dado temporal | 3 — dinheiro, irreversível | **9** | **completo** |
| Autorização (RQ-07, RQ-08) | 3 — integra com Shield + recorte compartilhado do `PapeisSeeder` | 3 — autorização | **9** | **completo** |
| Ciclo de vida do cupom (estado × operação) | 3 — quatro estados × quatro operações | 3 — dinheiro, irreversível | **9** | **completo** |
| Cadastro / CRUD (RQ-01 a RQ-06, RQ-14) | 2 — integra com Filament e com o escopo de organização | 3 — o cadastro errado é dinheiro errado | **6** | **padrão** |
| Trilha de auditoria (RQ-15) | 2 — integra com o consumo atômico | 3 — compliance, evidência | **6** | **padrão** |
| Listagem (RQ-08, recorte de visibilidade) | 2 — integra com `getEloquentQuery` + permission | 2 — retrabalho manual | **4** | **padrão** |

- Técnicas aplicadas: EP, BVA 3-valores, tabela de decisão, tabela **estado × operação**, matriz
  papel × ação, rastreio de efeito, normalização, idempotência ancorada no agregado.
- **Cenários: 41 · Regras: 14 · Mutantes previstos: 62 · Sem matador: 1** (M48 — ver R10).
- CT-B: **2**, especificados em `05-casos-de-teste-browser.md` (gate passou — ver lá).

### Técnica escalada acima do perfil da área (permitido; rebaixar não)

| Regra | Área (perfil) | Técnica usada | Por quê |
|---|---|---|---|
| R3 | cadastro (padrão) | tabela de decisão **tipo × valor** + BVA 3-valores | domínio condicionado: o teto de `valor` só existe quando `tipo = porcentagem`. BVA 2-valores sobre `valor` isolado faz o teto de 100 desaparecer sem ninguém notar |
| R10 | cadastro (padrão) | BVA 3-valores no **ponto de gravação** | RQ-05 e RQ-06 só falam do ponto de uso. Sem BVA na entrada, "cupom nasce expirado" e "cupom nasce esgotado" atravessam a suíte inteira |
| R7 | cadastro (padrão) | normalização + unicidade | RQ-14 é restrição de identidade; EP sozinho não distingue `PROMO10` de `promo10` |

### Divergência entre esta skill e as Project Rules (a rule vence)

`feature-test-design` sugere `pest --parallel --tia` como padrão de execução.
**`.ai/rules/testes-browser.md` vence**: mede que `--parallel` derruba 4 dos 11 CT-B e que, sem
PCOV, o `--tia` em série com Xdebug **não termina** (abortado após 35 min). Os comandos desta
feature são dois, em série no browser:

```bash
vendor/bin/pest --parallel --group=kit    # CT-01 a CT-41
vendor/bin/pest --testsuite=Browser       # CT-B01, CT-B02 — nunca --parallel
```

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | Entidade `Cupom` (código, tipo, valor, validade, limite, contador de usos); trilha de uso (quem/quando); tela de CRUD no painel; policy + permissões do papel; migration | CT-23, CT-24, CT-40, CT-41 |
| **F**unction | Cadastrar/editar/excluir; listar; validar (existe, na validade, com uso disponível); calcular o desconto; consumir um uso; registrar o uso | CT-01 a CT-19 |
| **D**ata | Dinheiro em **centavos inteiros** (nunca `float`); percentual inteiro 1..100; datetime de validade; contador `>= 0`; código texto livre normalizado; **dado de outra organização**; código ausente/`null`/`""` | CT-01 a CT-06, CT-10, CT-20 a CT-22, CT-29 a CT-31 |
| **I**nterfaces | Tela do painel (criar/editar/excluir/listar) **e** chamada direta do motor por quem fecha o pedido — duas portas para a mesma regra, e só a segunda existe hoje para RQ-09..RQ-13 | CT-07 a CT-15, CT-23 a CT-28 |
| **P**latform | SQLite `:memory:` nos testes (não compartilhado entre conexões — decide o que dá para provar sobre concorrência); MySQL em produção (colação decide se `promo10` = `PROMO10` no índice, e é por isso que a normalização não pode depender do banco); fuso do app × do banco | CT-14, CT-20, CT-21; **lacuna declarada** de fuso em M48 |
| **O**perations | Duas personas na tela (quem administra a organização × usuário comum) e uma terceira sem tela (o serviço que fecha o pedido). Uso indevido esperado: duplo clique/retry no fechamento; usuário comum tentando emitir desconto | CT-23 a CT-28, CT-36, CT-37 |
| **T**ime | Validade é instante, não dia — vira meia-noite, borda de 1 segundo, cupom que expira **entre** a validação e o consumo; ordem entre duas aplicações simultâneas | CT-09, CT-14, CT-29, CT-32 |

Nenhuma dimensão vazia. **P** é a única cuja consequência é uma lacuna, e ela está declarada em M48.

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — O desconto percentual incide sobre o total e a fração de centavo é truncada para baixo | cálculo (**completo**) | RQ-03, RQ-04, RQ-12 | BVA 3-valores (1 centavo) + EP | CT-01, CT-02 |
| **R2** — O desconto fixo subtrai o valor gravado e o total resultante nunca é negativo | cálculo (**completo**) | RQ-03, RQ-04, RQ-12 | BVA 3-valores (1 centavo) | CT-03, CT-04 |
| **R3** — O domínio válido de `valor` depende do `tipo`: 1..100 em porcentagem, 1..∞ em fixo | cadastro (padrão, técnica escalada) | RQ-03, RQ-04 | tabela de decisão **tipo × valor** + BVA | CT-05, CT-06 |
| **R4** — O cupom só é aplicável se existe, está dentro da validade e tem uso disponível | aplicação (**completo**) | RQ-09, RQ-10, RQ-11 | tabela de decisão + BVA (1 s, 1 uso) | CT-07 a CT-11 |
| **R5** — A aplicação bem-sucedida consome exatamente um uso, e o limite nunca é ultrapassado | aplicação (**completo**) | RQ-11, RQ-13 | rastreio de efeito + concorrência + BVA | CT-12 a CT-15 |
| **R6** — Toda aplicação deixa registrado quem aplicou e quando, e o registro não se separa do consumo | trilha (padrão) | RQ-15, RQ-13 | rastreio de efeito | CT-16 a CT-19 |
| **R7** — O código identifica o cupom sem depender de caixa nem de espaços, e não se repete | cadastro (padrão, técnica escalada) | RQ-02, RQ-14 | normalização + unicidade | CT-20 a CT-22 |
| **R8** — Só quem administra cria, edita e exclui cupom | autorização (**completo**) | RQ-07 | matriz papel × ação | CT-23 a CT-26 |
| **R9** — O usuário comum lista, e lista somente os cupons ativos | listagem (padrão) | RQ-08 | tabela de decisão + matriz papel × ação | CT-27, CT-28 |
| **R10** — O cadastro recusa validade já vencida e limite de usos abaixo de 1 | cadastro (padrão, técnica escalada) | RQ-05, RQ-06 | BVA 3-valores **na gravação** | CT-29 a CT-31 |
| **R11** — Cupom expirado, esgotado ou excluído deixa de ser aplicável, e a trilha sobrevive ao cupom | ciclo de vida (**completo**) | RQ-07, RQ-10, RQ-11, RQ-15 | tabela **estado × operação** | CT-32 a CT-35 |
| **R12** — Reaplicar o mesmo cupom ao mesmo total devolve o mesmo total; desconto não acumula | aplicação (**completo**) | RQ-12 | idempotência ancorada no agregado | CT-36, CT-37 |
| **R13** — O tipo do cupom admite exatamente dois valores, e um terceiro nunca concede desconto | cadastro (padrão) | RQ-03 | EP | CT-38, CT-39 |
| **R14** — O formulário grava apenas os campos do cupom: contador e organização não vêm do payload | cadastro (padrão) | RQ-06, RQ-13 | EP / mass assignment | CT-40, CT-41 |

**Cobertura das cláusulas** — toda `RQ` do `00` gerou regra:

| RQ | Regra(s) |
|---|---|
| RQ-01 | R8 (a tela é o veículo; CT-26 é a gravação pela tela), R14 |
| RQ-02 | R7 |
| RQ-03 | R1, R2, R3, R13 |
| RQ-04 | R1, R2, R3 |
| RQ-05 | R4 (uso), R10 (entrada) |
| RQ-06 | R4 (uso), R10 (entrada), R14 |
| RQ-07 | R8, R11 |
| RQ-08 | R9 |
| RQ-09 | R4 |
| RQ-10 | R4, R11 |
| RQ-11 | R4, R5, R11 |
| RQ-12 | R1, R2, R12 |
| RQ-13 | R5, R14 |
| RQ-14 | R7 |
| RQ-15 | R6, R11 |

---

## Fronteira com o Plano

O `01-plano-acao.md` foi lido **apenas** para paths, rotas, `## Superfície de UI`, stack e versões.
O que ele determina e o requisito não, foi recusado como oráculo:

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| `Cupom::valido()`, `aplicarEm()`, `descontoSobre()`, `scopeAtivos()`, `situacao()` | escolha de implementação — nome de método | detalhe do cenário; o `Então` fala do **resultado**, não do método |
| `UPDATE ... WHERE usos < limite_de_usos` (consumo atômico) | escolha de implementação — o requisito pede que o limite não estoure, não *como* | detalhe; CT-14 falsifica o **efeito**, não a instrução SQL |
| Tabela `cupom_usos`, colunas `valor_original` / `valor_desconto` | escolha de implementação — o requisito pede "quem e quando" | CT-16 assere **quem** e **quando** como oráculo; os dois valores entram como asserção de apoio |
| Rótulos `"Valor do desconto (centavos)"` / `"Percentual de desconto"` | comportamento **visível** que o requisito não determina | **pergunta** (Q-05) — e CT-B02 usa o rótulo como âncora, marcado `@premissa` |
| Textos de badge `Ativo` / `Expirado` / `Esgotado` | comportamento visível que o requisito não determina | **pergunta** (Q-06); nenhum `Então` do `04` depende deles |
| `intdiv` (truncar) | o requisito **não** determina; a premissa P-06 do `00` sim, e ela está declarada como premissa | CT-01 marcado `@premissa` |
| `max(0, ...)` (piso em zero) | idem — premissa P-07 do `00` | CT-03 marcado `@premissa` |
| Unidade centavos × pontos percentuais | idem — premissa P-05 do `00` | CT-01, CT-03, CT-05, CT-06 marcados `@premissa` |
| `unique(['tenant_id','codigo'])` | idem — premissa P-04 do `00` | CT-22 marcado `@premissa` |
| Painel `/app`, papel `admin_organizacao` | idem — premissas P-02 e P-09 do `00` | R8 inteira marcada `@premissa` |
| `cascadeOnDelete` de `cupom_usos` | **conflita com RQ-15** (auditar depois). Não é oráculo; é achado | **pergunta bloqueante** (Q-01) + CT-35, derivado do requisito e não do plano |
| Channel de log `cupom` e as três mensagens | comportamento não pedido pelo card | fora do `04` — nenhum `Então` afirma sobre log. Se o time quiser log como contrato, é requisito novo |
| Contagem de 38 permissions do painel `app` | número medido do kit, não do requisito | detalhe de manutenção de `tests/Kit/PaineisTest.php`; nenhum CT afirma o número |

### Achado central da derivação

**CT-35 nasceu do requisito e contradiz o plano.** RQ-15 pede registrar quem aplicou "pra gente
conseguir auditar **depois**"; o plano apaga a trilha junto com o cupom (`cascadeOnDelete`). Um
conjunto derivado do plano nunca escreveria esse cenário, porque o plano é internamente coerente.
É a diferença entre validar a interpretação e validar o requisito.

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` desta feature vive em `wikis/specs/exp-a/` e está
> **fechado para edição** — é a linha de base de comparação desta execução. As perguntas abaixo
> ficam aqui, **em bloco pronto para colagem** em `## Ambiguidades e Perguntas Abertas`, e
> continuam bloqueando o que dependem delas. O usuário não está disponível: cada uma tem premissa
> declarada e cenário marcado `@premissa`.

```markdown
### Q-01 — A trilha de uso sobrevive à exclusão do cupom? **(bloqueante)**

RQ-15 pede o registro "pra gente conseguir auditar depois"; RQ-07 dá ao admin o direito de excluir
o cupom. As duas juntas não decidem o que acontece com a trilha de um cupom excluído — e apagá-la
esvazia RQ-15 exatamente no caso em que alguém audita (o cupom suspeito é o primeiro a sumir).
**Premissa (P-10)**: a trilha sobrevive; excluir o cupom não apaga quem usou nem quando.
Bloqueia R11. Cenário `@premissa`: CT-35.

### Q-02 — A validade termina **no** instante gravado ou **depois** dele?

RQ-10 diz "dentro da validade". No instante exato de `expira_em` o cupom ainda vale?
**Premissa (P-11)**: o instante gravado é o último em que **não** vale (comparação estrita).
Bloqueia R4. Cenário `@premissa`: CT-09, linha "exatamente no instante".

### Q-03 — O cadastro pode gravar validade já vencida e limite 0?

RQ-05 e RQ-06 descrevem os campos e RQ-10/RQ-11 descrevem o uso deles. Nenhuma das quatro diz se o
cadastro aceita gravar um cupom que já nasce inaplicável.
**Premissa (P-12)**: não aceita — validade tem de ser futura e o limite, no mínimo 1.
Bloqueia R10. Cenários `@premissa`: CT-29, CT-30, CT-31.

### Q-04 — Reenvio da mesma aplicação (duplo clique, retry) consome um segundo uso?

RQ-13 manda incrementar o contador a cada aplicação, mas não distingue "segunda aplicação" de
"mesma aplicação reenviada". Sem chave de idempotência no contrato, as duas são indistinguíveis.
**Premissa (P-13)**: consome — o contrato não tem chave de requisição, e o oráculo verificável é
o **total devolvido**, que não muda. Bloqueia R12. Cenário `@premissa`: CT-36.

### Q-05 — Qual é o texto que declara a unidade do campo de valor na tela?

A mesma coluna guarda porcentagem e centavos (A-05). O requisito não determina nenhum rótulo, e a
tela é o único lugar onde a pessoa descobre a unidade.
**Premissa (P-14)**: o rótulo do campo muda com o tipo escolhido. Bloqueia CT-B02.

### Q-06 — O que a listagem mostra como situação do cupom?

RQ-08 fala em "cupons ativos" e A-03 resolve o conceito, mas nenhum texto de tela é determinado.
**Premissa (P-15)**: nenhum `Então` do `04` depende do texto; só a presença/ausência da linha.

### Q-07 — Aplicação sem usuário identificado é permitida?

RQ-15 pede registrar **quem** aplicou. Um job, um comando ou um webhook não têm usuário.
**Premissa (P-16)**: é permitida, e a trilha grava o instante com autor vazio — mas isso enfraquece
RQ-15 e precisa de resposta. Nenhum cenário desta entrega exercita a via sem usuário; se a resposta
for "não é permitida", falta um CT negativo.
```

---

## Setup Global

### Ligações reais do `tests/Pest.php` — o que decide a camada

Confirmado antes de alocar (`tests/Pest.php:22-145`):

| Pasta | `pest()->extend()` | Consequência para a alocação |
|---|---|---|
| `tests/Unit` | **nenhuma** — a pasta tem testsuite em `phpunit.xml:8-10` e **não** tem binding no `Pest.php` | um caso ali roda **sem o container**: `now()`, `config()`, cast de enum e Eloquent não resolvem. **A camada `Unit` não existe neste arnês** — o degrau mais barato real é `tests/Kit` |
| `tests/Kit` | `TestCase` + `RefreshDatabase`, grupo `kit` | single-tenant; é onde vive a regra de negócio |
| `tests/Tenancy` | `TenancyTestCase` + `RefreshDatabase`, grupo `kit` | multi-tenant fixado antes das migrations |
| `tests/BrowserTenancy` | `TenancyTestCase` + `RefreshDatabase`, grupo `browser` | CT-B com `/app/{tenant}` |

**Por isso nenhum cenário deste arquivo é alocado em `Unit`**, nem mesmo os de cálculo puro. Não é
escolha de rigor: é o degrau mais barato que o arnês sustenta.

### Distribuição por arquivo

| Arquivo | TestCase | Modo | Cenários |
|---|---|---|---|
| `tests/Kit/CupomTest.php` | `Tests\TestCase` | single-tenant | CT-01 a CT-19, CT-32 a CT-39 |
| `tests/Tenancy/CupomTenancyTest.php` | `Tests\TenancyTestCase` | multi-tenant | CT-11, CT-20 a CT-31, CT-40, CT-41 |
| `tests/BrowserTenancy/CupomTest.php` | `Tests\TenancyTestCase` | browser | CT-B01, CT-B02 |

### Personas

- `usuarioDoKit('master_global')` — `tests/Pest.php:229`. Quem administra em modo single-tenant
  (entra pelo `Gate::before`).
- `usuarioComPapel('admin_organizacao', $organizacao)` — `tests/Pest.php:255`. Quem administra a
  organização, no painel `/app`. **Só existe com a tenancy ligada** (daí morar em `tests/Tenancy`).
- `usuarioCom('panel_user')` / `usuarioComPapel('panel_user', $organizacao)` — o usuário comum.
- `usuarioCom(null)` — sem papel; não alcança painel nenhum.
- `tenant('Acme', 'acme')` e `tenant('Globex', 'globex')` — `tests/Pest.php:170`.
- `noPainelDa($organizacao)` — `tests/Pest.php:210`. **Obrigatório** antes de qualquer
  `Livewire::test()` nos casos de `tests/Tenancy`: sem ele o recorte cai no ramo fail-closed.

### Fixtures

- `Cupom::factory()` — padrão: porcentagem, valor 10, validade `+30 dias`, limite 100, `usos` 0.
- `Cupom::factory()->fixo($centavos)` · `->expirado()` · `->esgotado()`.
- **Armadilha do estado `esgotado()`**: `usos` fica fora do `$fillable` (é contador). `state(['usos'
  => …])` seria **descartado em silêncio** e o cenário passaria pelo motivo errado — o estado
  precisa de `afterCreating` com `forceFill`. Vale para CT-10, CT-27 e CT-33.

### Fakes

- **Nenhum fake de fila, mail ou notificação**: a feature não dispara nenhum dos três (o card não
  pede notificação; ver `## Fora de Escopo` do `00`).
- `travelTo()` / `freezeTime()` nos cenários temporais (CT-09, CT-14, CT-29, CT-32). **Sempre em
  closure ou com `travelBack()`** — `travel()` solto vaza para os testes seguintes.
- Nenhum `Event::fake()`. Se algum dia entrar, tem de vir **depois** das factories, senão o `uuid`
  gerado no `creating` some e a fixture nasce quebrada.

### Estratégia de DB

`RefreshDatabase`, herdado do `tests/Pest.php` para as três pastas. Não há escolha: o modo de
tenancy muda o schema e `Tests\TestCase::setUp()` invalida `RefreshDatabaseState::$migrated` quando
o modo troca.

### Seeders no `beforeEach` (obrigatório nos casos de autorização)

```php
beforeEach(function (): void {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
});
```

Sem o primeiro não existe permission no banco e **CT-23 passaria pelo motivo errado** — o usuário
comum não teria `Create:Cupom` porque ninguém tem, e não porque o recorte funciona. É a diferença
entre provar a regra e provar o vazio.

---

## Regra R1 — O desconto percentual incide sobre o total e a fração de centavo é truncada para baixo

> `RQ-03`, `RQ-04`, `RQ-12` · perfil **completo** · técnica: **BVA 3-valores** (fronteira: a fração
> de centavo; granularidade **1 centavo**) + **EP** sobre o percentual.
> `@premissa` P-05 (unidade) e P-06 (truncar) — ver Q do `00`; a direção do arredondamento é
> premissa, não requisito.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O desconto percentual é o percentual do total, com a fração de centavo truncada para baixo

    @premissa
    Esquema do Cenário: [CT-01] a fração de centavo do desconto percentual é descartada
      Dado um cupom de <percentual>% dentro da validade e com uso disponível
      Quando o serviço que fecha o pedido aplica o cupom a um total de <total> centavos
      Então o total com desconto é <final> centavos

      Exemplos:
        | percentual | total | final | # borda                                    |
        | 10         | 10000 | 9000  | divisão exata                              |
        | 10         | 9999  | 9000  | fração 0,9 descartada (borda−1 do centavo) |
        | 10         | 9990  | 8991  | divisão exata no centavo vizinho           |
        | 50         | 1     | 1     | fração 0,5 descartada — desconto é zero    |

    @premissa
    Cenário: [CT-02] o percentual máximo zera o total
      Dado um cupom de 100% dentro da validade e com uso disponível
      Quando o serviço que fecha o pedido aplica o cupom a um total de 12990 centavos
      Então o total com desconto é 0 centavos
```

**Camada**: `tests/Kit/CupomTest.php` — Feature (o arnês não sustenta `Unit`; ver Setup Global).
Valores sempre inteiros em centavos; nenhum `float` em nenhum exemplo.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | arredondar em vez de truncar (`round`) | CT-01 (linha "fração 0,9": 9000 × 8999) |
| M2 | arredondar para cima (`ceil`) | CT-01 (linha "fração 0,5": final 1 × 0) |
| M3 | devolver o **desconto** em vez do total com desconto | CT-01 (linha exata: 9000 × 1000) |
| M4 | esquecer a divisão por 100 (`total * percentual`) | CT-01 (linha exata) |
| M5 | tratar 100% como "sem desconto" (guarda `< 100`) | CT-02 |

---

## Regra R2 — O desconto fixo subtrai o valor gravado e o total resultante nunca é negativo

> `RQ-03`, `RQ-04`, `RQ-12` · perfil **completo** · técnica: **BVA 3-valores** (fronteira:
> `desconto` × `total`; granularidade **1 centavo**).
> `@premissa` P-05 (centavos) e P-07 (piso em zero).

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O desconto de valor fixo subtrai o valor gravado, e o total nunca fica negativo

    @premissa
    Esquema do Cenário: [CT-03] o total com desconto tem piso em zero
      Dado um cupom de valor fixo de 5000 centavos dentro da validade e com uso disponível
      Quando o serviço que fecha o pedido aplica o cupom a um total de <total> centavos
      Então o total com desconto é <final> centavos

      Exemplos:
        | total | final | # borda                              |
        | 5001  | 1     | borda−1 — desconto menor que o total |
        | 5000  | 0     | borda — desconto igual ao total      |
        | 4999  | 0     | borda+1 — desconto maior que o total |

    @premissa
    Cenário: [CT-04] o desconto fixo não cresce com o total
      Dado um cupom de valor fixo de 1000 centavos dentro da validade e com uso disponível
      Quando o serviço que fecha o pedido aplica o cupom a um total de 100000 centavos
      Então o total com desconto é 99000 centavos
```

**Camada**: `tests/Kit/CupomTest.php` — Feature.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6 | piso em zero ausente — total negativo | CT-03 (linha borda+1: 0 × −1) |
| M7 | `min` no lugar de `max` no piso | CT-03 (linha borda−1: 1 × 0) |
| M8 | valor fixo tratado como percentual | CT-04 (99000 × 0) |
| M9 | off-by-one no piso (`max(1, …)`) | CT-03 (linha borda: 0 × 1) |
| M10 | valor fixo interpretado em reais e multiplicado por 100 | CT-04 (99000 × 0) |

---

## Regra R3 — O domínio válido de `valor` depende do `tipo`

> `RQ-03`, `RQ-04` · área cadastro (padrão) · técnica **escalada**: **tabela de decisão
> `tipo × valor`** + **BVA 3-valores** (granularidade 1 unidade).
> É o ponto de **entrada** (gravação), não o de uso: `valor` isolado tem "um domínio"; cruzado com
> `tipo`, tem **dois**, e só um deles tem teto.
> `@premissa` P-05.

| `tipo` | mínimo | máximo | fronteiras testadas |
|---|---|---|---|
| porcentagem | 1 | **100** | −5, 0, 1, 100, 101 |
| fixo | 1 | — (sem teto) | 0, 1, **101** |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O valor do desconto tem domínio próprio para cada tipo de cupom

    @premissa
    Esquema do Cenário: [CT-05] em porcentagem, o valor vai de 1 a 100
      Dado que o administrador da organização preenche um cupom do tipo porcentagem
      Quando ele grava o cupom com o valor <valor>
      Então a gravação é <resultado>

      Exemplos:
        | valor | resultado | # borda                      |
        | -5    | recusada  | negativo                     |
        | 0     | recusada  | borda−1 do mínimo            |
        | 1     | aceita    | borda do mínimo              |
        | 100   | aceita    | borda do teto                |
        | 101   | recusada  | borda+1 do teto              |

    @premissa
    Esquema do Cenário: [CT-06] em valor fixo, o teto de 100 não existe
      Dado que o administrador da organização preenche um cupom do tipo valor fixo
      Quando ele grava o cupom com o valor <valor>
      Então a gravação é <resultado>

      Exemplos:
        | valor | resultado | # borda                                     |
        | 0     | recusada  | borda−1 do mínimo                           |
        | 1     | aceita    | borda do mínimo                             |
        | 101   | aceita    | acima do teto percentual — aqui é permitido |
```

**Camada**: Livewire (formulário Filament) — `tests/Tenancy/CupomTenancyTest.php`.
`fillForm([...])->call('create')->assertHasFormErrors(['valor'])` nas linhas recusadas;
`assertHasNoFormErrors()` + `assertDatabaseHas('cupons', ['codigo' => …, 'valor' => …, 'tipo' =>
…])` nas aceitas — **nunca `assertDatabaseHas` só pela chave primária**.
As linhas recusadas assertam também `assertDatabaseCount('cupons', 0)`: erro exibido com o registro
gravado é o defeito que o `assertHasFormErrors` sozinho não pega.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11 | teto de 100 aplicado aos **dois** tipos | CT-06 (linha 101 recusada) |
| M12 | teto ausente na porcentagem | CT-05 (linha 101) |
| M13 | mínimo 0 em vez de 1 | CT-05 e CT-06 (linha 0) |
| M14 | teto comparado com `<` (aceita até 99) | CT-05 (linha 100) |
| M15 | domínio conferido só no rótulo `live()` da tela, e o valor grava assim mesmo | CT-05 (linha 101, pelo `assertDatabaseCount(0)`) |

---

## Regra R4 — O cupom só é aplicável se existe, está dentro da validade e tem uso disponível

> `RQ-09`, `RQ-10`, `RQ-11` · perfil **completo** · técnica: **tabela de decisão** (3 condições) +
> **BVA 3-valores** (validade: 1 segundo; usos: 1 uso).

**Tabela de decisão** — a linha "validade vencida **e** sem uso" foi colapsada, e o motivo está
escrito: a ação (recusa) é a mesma, e o cenário combinado misturaria duas partições inválidas,
mascarando qual validação disparou.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O cupom só é aplicável se existe, está dentro da validade e ainda tem uso disponível

    Esquema do Cenário: [CT-07] as três condições precisam valer ao mesmo tempo
      Dado um código de cupom que <existe>
      E cuja validade está <validade>
      E cujo limite de usos <limite>
      Quando o serviço que fecha o pedido aplica o cupom a um total de 10000 centavos
      Então a aplicação é <resultado>

      Exemplos:
        | existe    | validade | limite            | resultado |
        | não existe| —        | —                 | recusada  |
        | existe    | no futuro| ainda tem folga   | aceita    |
        | existe    | vencida  | ainda tem folga   | recusada  |
        | existe    | no futuro| já foi atingido   | recusada  |

    @premissa
    Esquema do Cenário: [CT-08] a validade termina no instante gravado
      Dado um cupom cuja validade é <quando> em relação ao instante da aplicação
      Quando o serviço que fecha o pedido aplica o cupom a um total de 10000 centavos
      Então a aplicação é <resultado>

      Exemplos:
        | quando            | resultado | # borda  |
        | 1 segundo depois  | aceita    | borda−1  |
        | exatamente no instante | recusada | borda |
        | 1 segundo antes   | recusada  | borda+1  |

    Esquema do Cenário: [CT-09] o limite de usos é atingido, não ultrapassado
      Dado um cupom com limite de 3 usos e <ja_usado> usos já feitos
      Quando o serviço que fecha o pedido aplica o cupom a um total de 10000 centavos
      Então a aplicação é <resultado>

      Exemplos:
        | ja_usado | resultado | # borda  |
        | 1        | aceita    | dentro   |
        | 2        | aceita    | borda−1  |
        | 3        | recusada  | borda    |
        | 4        | recusada  | borda+1  |

    Esquema do Cenário: [CT-10] código ausente, nulo e vazio são todos recusados
      Dado que existe um cupom ativo na organização
      Quando o serviço que fecha o pedido aplica um código <codigo>
      Então a aplicação é recusada
      E nenhum uso é consumido

      Exemplos:
        | codigo              | # semântica |
        | ausente             | argumento não informado |
        | nulo                | null explícito          |
        | vazio               | string vazia            |
        | só espaços          | "   "                   |

    Cenário: [CT-11] o código de outra organização não é encontrado
      Dado um cupom ativo com o código "BLACKFRIDAY" na organização Globex
      E que o serviço está fechando um pedido da organização Acme
      Quando ele aplica o código "BLACKFRIDAY" a um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom da Globex continua em 0
```

**Camada**: CT-07 a CT-10 em `tests/Kit/CupomTest.php` (Feature); **CT-11 em
`tests/Tenancy/CupomTenancyTest.php`** — é o único que precisa de duas organizações.
CT-08 usa `travelTo()` em closure, congelando o instante — sem congelar, o "exatamente no instante"
é uma corrida contra o relógio e o cenário vira flake.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M16 | `<=` no lugar de `<` no limite de usos (aceita no limite) | CT-09 (linha borda) |
| M17 | `>=` no lugar de `>` na validade (aceita no instante exato) | CT-08 (linha borda) — `@premissa` Q-02 |
| M18 | `||` no lugar de `&&` entre validade e limite | CT-07 (linhas 3 e 4) |
| M19 | guarda de código vazio ausente — a consulta devolve o primeiro cupom | CT-10 (linhas vazio e só espaços) |
| M20 | consulta sem o recorte de organização | CT-11 |
| M21 | validade conferida na busca mas não no consumo, e o cupom expira entre as duas | CT-14 (R5) |

---

## Regra R5 — A aplicação bem-sucedida consome exatamente um uso, e o limite nunca é ultrapassado

> `RQ-11`, `RQ-13` · perfil **completo** · técnica: **rastreio de efeito** (aconteceu / não
> aconteceu quando não devia / uma só vez) + **concorrência** + BVA.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cada aplicação bem-sucedida consome exatamente um uso, e o limite nunca é ultrapassado

    Cenário: [CT-12] a aplicação bem-sucedida consome um único uso
      Dado um cupom de 10% com limite de 5 usos e nenhum uso feito
      Quando o serviço que fecha o pedido aplica o cupom a um total de 10000 centavos
      Então o total com desconto é 9000 centavos
      E o contador de usos do cupom passa a ser 1

    Cenário: [CT-13] a aplicação recusada não consome uso
      Dado um cupom de 10% já vencido, com limite de 5 usos e 2 usos feitos
      Quando o serviço que fecha o pedido tenta aplicar o cupom a um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom continua em 2

    Cenário: [CT-14] duas aplicações partindo da mesma leitura não furam o limite
      Dado um cupom com limite de 3 usos e 2 usos feitos
      E duas leituras do cupom feitas antes de qualquer consumo
      Quando as duas leituras são usadas para aplicar o cupom ao mesmo total
      Então apenas uma das duas aplicações é aceita
      E o contador de usos do cupom é 3

    Cenário: [CT-15] o último uso disponível esgota o cupom
      Dado um cupom com limite de 1 uso e nenhum uso feito
      Quando o serviço que fecha o pedido aplica o cupom duas vezes seguidas
      Então a primeira aplicação é aceita e a segunda é recusada
      E o contador de usos do cupom é 1
```

**Camada**: `tests/Kit/CupomTest.php` — Feature.

**CT-14 e a hipótese do arnês** (regra: *impossibilidade de arnês é hipótese, não conclusão*).
Paralelismo real foi **tentado antes de declarar lacuna**:

| Tentativa | Resultado |
|---|---|
| dois processos (`pcntl_fork`) | indisponível no ambiente (Windows) |
| segunda conexão PDO para o mesmo banco | `DB_DATABASE=:memory:` é **por conexão**: a segunda enxerga um banco vazio, e o cenário passaria por motivo errado |
| SQLite em arquivo temporário + segunda conexão | funciona, mas troca o modo de banco de toda a suíte (`phpunit.xml:53-54`) e ainda serializa por lock de arquivo — não reproduz interleaving |
| **duas instâncias do model lidas antes do consumo** | **adotado** — reproduz exatamente a janela que o defeito explora (ler o contador, decidir, escrever) sem depender de threads |

**Lacuna residual declarada**: interleaving verdadeiro no nível do banco não é reproduzível neste
arnês. CT-14 mata o `check-then-act` em PHP, que é o defeito plausível; um defeito que só apareça
sob concorrência real do SGBD ficaria vivo.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M22 | o contador nunca é incrementado | CT-12 |
| M23 | o contador é incrementado antes de validar (ou também na recusa) | CT-13 |
| M24 | incremento duplicado (contador vai a 2 numa aplicação) | CT-12 |
| M25 | `check-then-act`: lê o contador em memória, compara e salva | CT-14 |
| M26 | o consumo é tentado mas o resultado não é conferido — o desconto é concedido mesmo sem consumir | CT-15 |

---

## Regra R6 — Toda aplicação deixa registrado quem aplicou e quando, e o registro não se separa do consumo

> `RQ-15`, `RQ-13` · área trilha (padrão) · técnica: **rastreio de efeito** — três cenários
> obrigatórios (aconteceu / não aconteceu quando não devia / uma só vez) e um quarto para a
> inseparabilidade.
> **Estouro do teto justificado**: o perfil padrão dá 3 cenários por regra; M31 só morre com CT-19,
> e o gate vence o teto.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Toda aplicação de cupom fica registrada com quem aplicou e quando

    Cenário: [CT-16] a aplicação registra o autor e o instante
      Dado um cupom de 10% ativo
      E uma compradora identificada
      Quando o serviço que fecha o pedido aplica o cupom a um total de 10000 centavos em nome dela
      Então existe exatamente um registro de uso desse cupom
      E esse registro aponta a compradora como autora
      E o instante registrado é o instante da aplicação

    Cenário: [CT-17] a aplicação recusada não deixa registro
      Dado um cupom de 10% já vencido
      Quando o serviço que fecha o pedido tenta aplicar o cupom a um total de 10000 centavos
      Então não existe registro de uso nenhum para esse cupom

    Cenário: [CT-18] cada aplicação deixa o seu próprio registro
      Dado um cupom de 10% com limite de 5 usos
      Quando o serviço que fecha o pedido aplica o cupom três vezes
      Então existem três registros de uso desse cupom
      E o contador de usos do cupom é 3

    Cenário: [CT-19] uso consumido sem registro não acontece
      Dado um cupom de 10% ativo
      E que a gravação do registro de uso está impedida de acontecer
      Quando o serviço que fecha o pedido tenta aplicar o cupom a um total de 10000 centavos
      Então a aplicação falha
      E o contador de usos do cupom continua em 0
```

**Camada**: `tests/Kit/CupomTest.php` — Feature.
CT-16 congela o tempo (`freezeTime()`) e assere o instante gravado contra ele — "existe um
`created_at`" não é oráculo; o valor concreto é.
**CT-19 é o cenário que a hipótese do arnês liberou**: em vez de declarar "não dá para forçar a
falha da gravação", o arnês foi mudado — `Schema::drop('cupom_usos')` dentro do caso torna a
gravação impossível de verdade, e o oráculo passa a ser observável (`usos` continua 0). Sem
transação, o contador anda e o cenário fica vermelho.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M27 | a gravação do registro é esquecida | CT-16 |
| M28 | o registro é gravado também na recusa | CT-17 |
| M29 | o autor não é gravado (fica vazio) | CT-16 |
| M30 | o instante gravado é o da criação do cupom, não o da aplicação | CT-16 |
| M31 | o registro é gravado **fora** da transação do consumo | CT-19 |

---

## Regra R7 — O código identifica o cupom sem depender de caixa nem de espaços, e não se repete

> `RQ-02`, `RQ-14` · área cadastro (padrão), técnica **escalada**: **normalização** (caixa, espaços
> nas bordas) + **unicidade**.
> `@premissa` P-04 (o escopo da unicidade é a organização).

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O código identifica o cupom independentemente de caixa e de espaços, e não se repete

    Esquema do Cenário: [CT-20] a grafia do código não muda o cupom que ele encontra
      Dado um cupom cadastrado com o código "  promo10  "
      Quando o serviço que fecha o pedido aplica o código <digitado> a um total de 10000 centavos
      Então a aplicação é aceita
      E o código guardado no cupom é "PROMO10"

      Exemplos:
        | digitado    | # variação          |
        | "PROMO10"   | canônica            |
        | "promo10"   | caixa baixa         |
        | "Promo10"   | caixa mista         |
        | "  PROMO10 "| espaços nas bordas  |

    Cenário: [CT-21] o mesmo código não é cadastrado duas vezes na organização
      Dado um cupom cadastrado com o código "PROMO10" na organização Acme
      Quando o administrador da Acme tenta cadastrar outro cupom com o código "promo10"
      Então o cadastro é recusado
      E a organização Acme continua com um único cupom de código "PROMO10"

    @premissa
    Cenário: [CT-22] organizações diferentes podem usar o mesmo código
      Dado um cupom com o código "BLACKFRIDAY" na organização Globex
      Quando o administrador da Acme cadastra um cupom com o código "BLACKFRIDAY"
      Então o cadastro é aceito
      E cada organização passa a ter o seu próprio cupom "BLACKFRIDAY"
```

**Camada**: Livewire — `tests/Tenancy/CupomTenancyTest.php` (CT-21 e CT-22 precisam de duas
organizações; CT-20 fica junto por partilhar a fixture).
CT-21 assere o efeito (`assertDatabaseCount` do código na organização), e o erro de campo entra
como asserção de apoio — o requisito determina que não se repete, não *como* a tela reclama.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M32 | normalização aplicada na leitura e não na gravação | CT-20 (o código guardado) e CT-21 |
| M33 | caixa normalizada mas espaços nas bordas mantidos | CT-20 (linha "espaços nas bordas") |
| M34 | unicidade global (a primeira organização reserva a palavra) | CT-22 |
| M35 | unicidade validada sem passar pelo recorte de organização | CT-22 |

---

## Regra R8 — Só quem administra cria, edita e exclui cupom

> `RQ-07` · perfil **completo** · técnica: **matriz papel × ação** — ação destrutiva é obrigatória.
> `@premissa` P-02 e P-09: "admin" é quem administra a **organização**, no painel de negócio.

| Papel | listar | ver | criar | editar | **excluir** |
|---|---|---|---|---|---|
| quem administra a organização | ✅ | ✅ | ✅ | ✅ | ✅ |
| usuário comum | ✅ | ✅ | ❌ | ❌ | ❌ |
| papéis de outros painéis | não alcançam a tela |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Só quem administra a organização cria, edita e exclui cupom

    @premissa
    Cenário: [CT-23] o usuário comum não recebe as permissões de escrita, e mantém as de leitura
      Dado um usuário comum do painel de negócio
      Quando as permissões do papel dele são consultadas
      Então ele não pode criar, editar nem excluir cupom
      E ele pode listar e ver cupom

    @premissa
    Cenário: [CT-24] o usuário comum não consegue criar cupom nem chamando a ação
      Dado um usuário comum do painel de negócio
      Quando ele dispara a criação de um cupom com dados válidos
      Então a criação é negada
      E a organização continua sem nenhum cupom

    @premissa
    Cenário: [CT-25] o usuário comum não consegue excluir um cupom existente
      Dado um cupom ativo na organização
      E um usuário comum do painel de negócio
      Quando ele dispara a exclusão desse cupom
      Então a exclusão é negada
      E o cupom continua cadastrado

    @premissa
    Cenário: [CT-26] quem administra a organização cadastra o cupom pela tela
      Dado o administrador da organização Acme na tela de cadastro de cupom
      Quando ele grava um cupom de 15% válido por 30 dias com limite de 50 usos
      Então o cupom passa a existir na organização Acme com esses cinco valores
```

**Camada**: CT-23 é `Feature` (matriz de permissões, no molde de `tests/Kit/PaineisTest.php:142`).
CT-24, CT-25 e CT-26 são **Livewire** — `livewire(CreateCupom::class)->fillForm([...])
->call('create')`, `assertForbidden()` / `assertActionHidden(TestAction::make(DeleteAction::class)
->table())`, todos em `tests/Tenancy/CupomTenancyTest.php`, precedidos de `noPainelDa($acme)`.

> **CT-24 e CT-25 existem porque `can()` não é oráculo suficiente.** Uma policy correta que a tela
> nunca consulta passa em CT-23 e reprova aqui. É a mesma armadilha catalogada em
> `.ai/rules/filament.md` → "Asserção de identidade vive no model".

> **Gate de tela de escrita**: as rotas `create` e `edit` da `## Superfície de UI` exigem gravação
> por componente. `create` está em CT-26; `edit` está em **CT-33** (R11).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M36 | a entidade nova é esquecida no recorte, e o usuário comum herda a escrita | CT-23 |
| M37 | o recorte casa por pedaço do nome e tira também a leitura | CT-23 (metade positiva) |
| M38 | autorização só na tela: o botão some, a ação continua respondendo | CT-24, CT-25 |
| M39 | a exclusão fica liberada a todos (a única ação esquecida) | CT-25 |
| M40 | o recorte é aplicado também a quem administra | CT-26 |

---

## Regra R9 — O usuário comum lista, e lista somente os cupons ativos

> `RQ-08` · área listagem (padrão) · técnica: **tabela de decisão** (situação derivada) + matriz
> papel × ação.
> `@premissa` P-03: "ativo" é estado derivado (dentro da validade **e** com uso disponível), não
> interruptor.

| validade | usos | situação | usuário comum vê? | quem administra vê? |
|---|---|---|---|---|
| futura | abaixo do limite | ativo | ✅ | ✅ |
| futura | no limite | esgotado | ❌ | ✅ |
| vencida | abaixo do limite | expirado | ❌ | ✅ |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O usuário comum enxerga apenas os cupons ativos; quem administra enxerga todos

    @premissa
    Cenário: [CT-27] a listagem do usuário comum esconde expirado e esgotado
      Dado três cupons na organização: um ativo, um vencido e um no limite de usos
      Quando o usuário comum abre a listagem de cupons
      Então ele vê o cupom ativo
      E não vê o cupom vencido nem o cupom no limite de usos

    @premissa
    Cenário: [CT-28] a busca por código não devolve cupom inativo ao usuário comum
      Dado um cupom vencido de código "PROMO10" na organização
      Quando o usuário comum busca por "PROMO10" na listagem
      Então nenhum cupom é listado
```

**Camada**: Livewire — `assertCanSeeTableRecords` / `assertCanNotSeeTableRecords` e `searchTable`,
em `tests/Tenancy/CupomTenancyTest.php`. A metade "quem administra vê os três" entra como asserção
do mesmo CT-27, com a segunda persona.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M41 | "ativo" considera só a validade, e o esgotado continua listado | CT-27 |
| M42 | "ativo" considera só o limite, e o vencido continua listado | CT-27 |
| M43 | o recorte é aplicado a todo mundo, inclusive a quem administra | CT-27 (metade do administrador) |
| M44 | o recorte vive só na tabela e não na consulta base — busca e link direto escapam | CT-28 |

---

## Regra R10 — O cadastro recusa validade já vencida e limite de usos abaixo de 1

> `RQ-05`, `RQ-06` · área cadastro (padrão), técnica **escalada** a **BVA 3-valores no ponto de
> gravação** (validade: 1 minuto — o campo não oferece segundos; limite: 1 uso).
> **É o ponto de entrada, e o requisito só descreve o de uso.** `@premissa` P-12 / Q-03.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O cadastro não aceita um cupom que já nasce inaplicável

    @premissa
    Esquema do Cenário: [CT-29] a validade gravada tem de ser futura
      Dado que o administrador da organização preenche um cupom válido em tudo o mais
      Quando ele grava a validade <quando>
      Então a gravação é <resultado>

      Exemplos:
        | quando              | resultado | # borda |
        | daqui a 1 minuto    | aceita    | borda−1 |
        | há 1 minuto         | recusada  | borda+1 |
        | ontem               | recusada  | partição inválida |

    @premissa
    Esquema do Cenário: [CT-30] o limite de usos gravado começa em 1
      Dado que o administrador da organização preenche um cupom válido em tudo o mais
      Quando ele grava o limite de usos como <limite>
      Então a gravação é <resultado>

      Exemplos:
        | limite | resultado | # borda           |
        | -1     | recusada  | negativo          |
        | 0      | recusada  | borda−1           |
        | 1      | aceita    | borda do mínimo   |

    @premissa
    Cenário: [CT-31] a edição também recusa validade já vencida
      Dado um cupom ativo cadastrado na organização
      Quando o administrador edita esse cupom pondo a validade em ontem
      Então a alteração é recusada
      E a validade do cupom continua sendo a original
```

**Camada**: Livewire — `tests/Tenancy/CupomTenancyTest.php`. As linhas recusadas conferem também
`assertDatabaseCount('cupons', 0)` (CT-29, CT-30) e o valor original preservado (CT-31).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M45 | validade sem piso: o cupom nasce vencido | CT-29 |
| M46 | limite com mínimo 0: o cupom nasce esgotado | CT-30 (linha 0) |
| M47 | o piso existe na criação e não na edição | CT-31 |
| M48 | o piso da validade compara o instante do app com o do banco em fusos diferentes, e o cupom criado "para hoje" é recusado | ⚠️ **sem matador — lacuna declarada** (abaixo) |

**Lacuna declarada M48 — o que foi tentado antes de declará-la** (a impossibilidade de arnês é
hipótese, não conclusão):

| Tentativa | Resultado |
|---|---|
| `config(['app.timezone' => 'UTC'])` em `beforeEach` | ineficaz: `Tests\TestCase::createApplication()` já executou o bootstrap que fixa o fuso do processo; mudar a config depois não re-registra nada |
| `travelTo()` na virada da meia-noite | funciona, e **já está coberto** — é o mecanismo de CT-08; mas prova a borda do relógio, não a divergência app × banco |
| `DB::statement` para mudar o fuso da conexão | SQLite não tem fuso de sessão; o comportamento medido seria do arnês, não do produto |
| um `TestCase` próprio fixando o fuso **antes** de `createApplication()` | **viável** — é exatamente o que `Tests\TenancyTestCase` faz com `permission.teams`. Custo: um terceiro `TestCase` e uma **quarta pasta** de testes (o Pest não aceita dois TestCases na mesma pasta), para cobrir um cenário que o kit hoje nem expõe (não existe fuso por usuário) |

**Declarada, não resolvida**: o custo é infraestrutura de teste nova, e a decisão de pagá-lo
depende de Q-02 e da existência de fuso por usuário. Enquanto isso, M48 fica vivo e **registrado**.

---

## Regra R11 — Cupom expirado, esgotado ou excluído deixa de ser aplicável, e a trilha sobrevive ao cupom

> `RQ-07`, `RQ-10`, `RQ-11`, `RQ-15` · perfil **completo** · técnica: **tabela estado × operação**
> — as colunas são **todas** as operações, não só a de leitura.

| Estado | **aplicar** | listar (usuário comum) | **editar** | **excluir** |
|---|---|---|---|---|
| ativo | aceita — CT-12 | aparece — CT-27 | permite — CT-31 | permite — CT-25 (negada ao comum) |
| expirado | **recusa** — CT-07 | não aparece — CT-27 | **permite estender** — CT-32 | permite |
| esgotado | **recusa** — CT-09 | não aparece — CT-27 | permite | permite |
| **excluído** | **recusa** — CT-33 | não aparece — CT-33 | **404** — CT-34 | **404 na segunda vez** — CT-34 |

A célula que escapa é *excluído × aplicar*: os cenários provam que o cupom some da lista, e ninguém
prova que ele **deixou de funcionar**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O cupom só funciona enquanto está ativo e existe; a trilha de uso sobrevive a ele

    Cenário: [CT-32] o cupom expirado volta a valer quando a validade é estendida
      Dado um cupom vencido ontem na organização
      Quando o administrador estende a validade dele para daqui a 30 dias
      Então o cupom volta a ser aceito na aplicação

    Cenário: [CT-33] o cupom excluído deixa de ser aplicável
      Dado um cupom ativo de código "PROMO10" na organização
      Quando o administrador exclui esse cupom
      Então a aplicação do código "PROMO10" é recusada
      E o código "PROMO10" não aparece na listagem de ninguém

    Cenário: [CT-34] operar um cupom que não existe mais não estoura
      Dado um cupom que já foi excluído
      Quando o administrador tenta abrir a edição desse cupom
      Então a resposta é "não encontrado"
      E uma segunda exclusão do mesmo cupom também responde "não encontrado"

    @premissa
    Cenário: [CT-35] a trilha de uso sobrevive à exclusão do cupom
      Dado um cupom de código "PROMO10" que já foi aplicado duas vezes
      Quando o administrador exclui esse cupom
      Então os dois registros de uso continuam existindo
      E cada um continua apontando quem aplicou e quando
```

**Camada**: CT-32, CT-33 e CT-35 em `tests/Kit/CupomTest.php` (Feature, a exclusão pelo model);
CT-34 em Livewire (`tests/Tenancy/CupomTenancyTest.php`) — é a resposta da rota que importa.
CT-33 assere as **duas** metades: a aplicação recusada e a ausência na listagem. Provar só a
segunda é exatamente o defeito que esta tabela existe para pegar.

> **CT-35 é `@premissa` P-10 e conflita com o plano** (`cascadeOnDelete`). Ele foi derivado de
> RQ-15 — "pra gente conseguir auditar **depois**" — e não do desenho. Ver Q-01: é a pergunta
> bloqueante desta feature.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M49 | a exclusão apenas esconde da listagem, e o código continua sendo aceito | CT-33 |
| M50 | a exclusão apaga a trilha junto (é o que o plano desenhou) | CT-35 |
| M51 | id inexistente responde erro de servidor em vez de "não encontrado" | CT-34 |
| M52 | segunda exclusão do mesmo registro estoura | CT-34 |
| M53 | cupom vencido é bloqueado para edição, e não há como estendê-lo | CT-32 |

---

## Regra R12 — Reaplicar o mesmo cupom ao mesmo total devolve o mesmo total; desconto não acumula

> `RQ-12` · perfil **completo** · técnica: **idempotência ancorada no agregado afetado**.
> O oráculo é **o total do pedido**, nunca o contador do cupom: ancorar no recurso consumido prova
> contabilidade e não prova idempotência.
> `@premissa` P-13 / Q-04.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Reaplicar o mesmo cupom ao mesmo total devolve o mesmo total com desconto

    @premissa
    Cenário: [CT-36] a segunda aplicação devolve o mesmo total com desconto
      Dado um cupom de 10% com limite de 5 usos
      Quando o serviço que fecha o pedido aplica o cupom duas vezes ao total de 10000 centavos
      Então as duas aplicações devolvem 9000 centavos

    Cenário: [CT-37] a aplicação recusada não altera o total do pedido
      Dado um cupom de 10% já esgotado
      E um pedido de 10000 centavos
      Quando o serviço que fecha o pedido tenta aplicar o cupom
      Então o total do pedido continua sendo 10000 centavos
```

**Camada**: `tests/Kit/CupomTest.php` — Feature.

> **O que estes dois cenários não resolvem, e está registrado como Q-04**: o contrato não tem chave
> de requisição, então "retry" e "segunda aplicação legítima" são indistinguíveis. O agregado
> (o total) é idempotente; o recurso (o contador) não é. Se a resposta a Q-04 for "retry não
> consome", falta um cenário e a assinatura precisa de uma chave.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M54 | o desconto acumula sobre o total já descontado (9000 → 8100) | CT-36 |
| M55 | o total devolvido depende do contador (desconto proporcional ao que sobrou) | CT-36 |
| M56 | a recusa devolve 0 em vez de deixar o total intacto | CT-37 |

---

## Regra R13 — O tipo do cupom admite exatamente dois valores, e um terceiro nunca concede desconto

> `RQ-03` · área cadastro (padrão) · técnica: **EP** — as duas partições válidas e a inválida
> isolada.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O tipo do cupom é porcentagem ou valor fixo, e nada mais

    Esquema do Cenário: [CT-38] só os dois tipos são graváveis
      Dado que o administrador da organização preenche um cupom válido em tudo o mais
      Quando ele grava o tipo <tipo>
      Então a gravação é <resultado>

      Exemplos:
        | tipo          | resultado | # partição      |
        | porcentagem   | aceita    | válida          |
        | valor fixo    | aceita    | válida          |
        | frete grátis  | recusada  | inválida        |
        | vazio         | recusada  | ausente         |

    Cenário: [CT-39] um tipo desconhecido nunca concede desconto em silêncio
      Dado um cupom cujo tipo gravado não é nenhum dos dois conhecidos
      Quando o serviço que fecha o pedido tenta aplicar esse cupom a um total de 10000 centavos
      Então a aplicação falha de forma visível
      E nenhum uso é consumido
```

**Camada**: CT-38 em Livewire (`tests/Tenancy/CupomTenancyTest.php`); **CT-39 em
`tests/Kit/CupomTest.php`**.

> **CT-39 é o segundo cenário que a hipótese do arnês liberou.** A conclusão fácil era "com o tipo
> garantido no cadastro, um terceiro valor é inalcançável e o mutante fica vivo". O arnês foi
> mudado: gravar o tipo inválido **direto na tabela**, por baixo do cadastro (é o mesmo recurso que
> a factory usa para mover o contador, que também está fora do `$fillable`). O cenário passa a ser
> executável, e o mutante "tratar o desconhecido como valor fixo" morre.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M57 | o tipo é texto livre e qualquer palavra é gravável | CT-38 (linha "frete grátis") |
| M58 | um dos dois tipos não é oferecido | CT-38 (linhas válidas) |
| M59 | o cálculo trata o tipo desconhecido como valor fixo, em silêncio | CT-39 |

---

## Regra R14 — O formulário grava apenas os campos do cupom: contador e organização não vêm do payload

> `RQ-06`, `RQ-13` · área cadastro (padrão) · técnica: **EP / mass assignment** — enviar campo não
> previsto e provar que é ignorado.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Só os campos do cupom vêm do formulário; contador e organização não

    Cenário: [CT-40] o contador de usos não pode ser definido pelo formulário
      Dado o administrador da organização na tela de cadastro de cupom
      Quando ele grava um cupom válido enviando junto um contador de 99 usos
      Então o cupom nasce com 0 usos

    Cenário: [CT-41] a organização do cupom não vem do formulário
      Dado o administrador operando a organização Acme
      Quando ele grava um cupom válido enviando junto a organização Globex
      Então o cupom nasce na organização Acme
```

**Camada**: Livewire — `tests/Tenancy/CupomTenancyTest.php`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M60 | o contador entra na lista de campos preenchíveis | CT-40 |
| M61 | a organização entra na lista de campos preenchíveis | CT-41 |
| M62 | nenhuma restrição de preenchimento em massa | CT-40, CT-41 |

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| **IDOR / autorização horizontal** (recurso de outra organização) | **CT-11** — o código da Globex não é encontrado pela Acme; e **CT-41**, que prova que o payload não muda a dona |
| **Autorização exercida na ação** (não só `can()`) | **CT-24**, **CT-25** — a ação disparada, não a permissão consultada |
| **Idempotência (ancorada no agregado afetado)** | **CT-36** — o oráculo é o total devolvido; o contador é o recurso consumido e **não** serve de oráculo aqui |
| **Concorrência** (contador, limite) | **CT-14** — duas leituras anteriores ao consumo. Paralelismo real: lacuna residual declarada em R5, com as quatro tentativas listadas |
| **Fronteira no ponto de entrada (gravação)** | **CT-05**, **CT-06**, **CT-29**, **CT-30**, **CT-31** — valor, validade e limite, todos na gravação |
| **Domínio condicionado (tipo × valor)** | **CT-05** e **CT-06** — o teto de 100 existe num tipo e não existe no outro |
| **Estado × operação de escrita** (o excluído ainda funciona?) | **CT-33** (excluído × aplicar), **CT-34** (excluído × editar/excluir), **CT-32** (expirado × editar) |
| **Ausente ≠ `null` ≠ `""`** | **CT-10** — quatro linhas, com a semântica de cada uma declarada |
| **Paginação** | não se aplica: a listagem não é comportamento pedido pelo card além de "listar os ativos" (RQ-08); volume de cupons por organização é de dezenas. Se a paginação virar requisito, faltam 4 cenários (0, 1, limite, além) |
| **Ordenação por coluna** | não se aplica: RQ-08 não determina ordem nenhuma. A ordem escolhida pelo plano é detalhe recusado como oráculo |
| **Timezone / DST** | **lacuna declarada (M48)**: tentado `config(['app.timezone'])` em `beforeEach` (ineficaz — bootstrap já rodou), `travelTo` na virada (cobre a borda do relógio, não a divergência), fuso de sessão no SQLite (inexistente) e um `TestCase` próprio antes de `createApplication()` (viável, custo = quarta pasta de testes). Virada de meia-noite **está** coberta por CT-08 |
| **Unicode / limite de varchar / texto livre** | **CT-20** cobre caixa e espaços nas bordas. Acento, emoji e o limite exato do campo: **lacuna declarada** — o requisito não determina o comprimento máximo do código (só o plano o faz, com 40), e testar contra 40 seria testar o PRD. Vira cenário no dia em que Q sobre o formato do código for respondida |
| **Unicidade + soft delete** | não se aplica: o requisito não pede exclusão lógica de cupom, e nenhuma cláusula sugere recuperação. **CT-33 + CT-21** cobrem o par excluir → recadastrar o mesmo código, que é o risco real |
| **CRUD combinado** (id inexistente, excluir duas vezes, editar sem alterar) | **CT-34** (inexistente e duas exclusões). "Editar sem alterar nada": **não se aplica** — nenhuma cláusula do requisito depende de `updated_at` ou de contagem de alterações |
| **Mass assignment** | **CT-40**, **CT-41** |
| **Upload** | não se aplica: a feature não tem arquivo |
| **Precisão monetária** | **CT-01**, **CT-03** — centavos inteiros em todos os exemplos, borda de centavo em ambas as direções, **nenhum `float`** em nenhum cenário |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | fração de centavo do percentual é descartada | R1 | BVA 3-val | Feature | `tests/Kit/CupomTest.php` | M1, M2, M3, M4 |
| CT-02 | percentual máximo zera o total | R1 | EP borda | Feature | `tests/Kit/CupomTest.php` | M5 |
| CT-03 | total com desconto tem piso em zero | R2 | BVA 3-val | Feature | `tests/Kit/CupomTest.php` | M6, M7, M9 |
| CT-04 | desconto fixo não cresce com o total | R2 | EP | Feature | `tests/Kit/CupomTest.php` | M8, M10 |
| CT-05 | porcentagem vai de 1 a 100 | R3 | decisão + BVA | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M12, M13, M14, M15 |
| CT-06 | em fixo o teto de 100 não existe | R3 | decisão + BVA | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M11, M13 |
| CT-07 | as três condições valem juntas | R4 | tabela de decisão | Feature | `tests/Kit/CupomTest.php` | M18 |
| CT-08 | validade termina no instante gravado | R4 | BVA 1 s | Feature | `tests/Kit/CupomTest.php` | M17 |
| CT-09 | limite é atingido, não ultrapassado | R4 | BVA 1 uso | Feature | `tests/Kit/CupomTest.php` | M16 |
| CT-10 | ausente ≠ nulo ≠ vazio | R4 | EP | Feature | `tests/Kit/CupomTest.php` | M19 |
| CT-11 | código de outra organização não é encontrado | R4 | IDOR | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M20 |
| CT-12 | consome um único uso | R5 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M22, M24 |
| CT-13 | recusa não consome uso | R5 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M23 |
| CT-14 | duas leituras não furam o limite | R5 | concorrência | Feature | `tests/Kit/CupomTest.php` | M21, M25 |
| CT-15 | último uso esgota o cupom | R5 | BVA | Feature | `tests/Kit/CupomTest.php` | M26 |
| CT-16 | registra autor e instante | R6 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M27, M29, M30 |
| CT-17 | recusa não deixa registro | R6 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M28 |
| CT-18 | uma aplicação, um registro | R6 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | — (guarda de contagem; ver poda) |
| CT-19 | uso consumido sem registro não acontece | R6 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M31 |
| CT-20 | grafia não muda o cupom encontrado | R7 | normalização | Tenancy | `tests/Tenancy/CupomTenancyTest.php` | M32, M33 |
| CT-21 | código não se repete na organização | R7 | unicidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M32 |
| CT-22 | organizações diferentes repetem o código | R7 | unicidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M34, M35 |
| CT-23 | usuário comum sem escrita, com leitura | R8 | matriz papel×ação | Feature | `tests/Tenancy/CupomTenancyTest.php` | M36, M37 |
| CT-24 | criação negada ao usuário comum | R8 | matriz papel×ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M38 |
| CT-25 | exclusão negada ao usuário comum | R8 | matriz papel×ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M38, M39 |
| CT-26 | administrador cadastra pela tela | R8 | gate de tela de escrita | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M40 |
| CT-27 | listagem esconde expirado e esgotado | R9 | decisão | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M41, M42, M43 |
| CT-28 | busca não devolve inativo | R9 | decisão | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M44 |
| CT-29 | validade gravada tem de ser futura | R10 | BVA entrada | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M45 |
| CT-30 | limite gravado começa em 1 | R10 | BVA entrada | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M46 |
| CT-31 | edição também recusa validade vencida | R10 | BVA entrada | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M47 |
| CT-32 | expirado volta a valer se estendido | R11 | estado × operação | Feature | `tests/Kit/CupomTest.php` | M53 |
| CT-33 | excluído deixa de ser aplicável | R11 | estado × operação | Feature | `tests/Kit/CupomTest.php` | M49 |
| CT-34 | operar cupom inexistente não estoura | R11 | estado × operação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M51, M52 |
| CT-35 | trilha sobrevive à exclusão | R11 | estado × operação | Feature | `tests/Kit/CupomTest.php` | M50 |
| CT-36 | segunda aplicação devolve o mesmo total | R12 | idempotência | Feature | `tests/Kit/CupomTest.php` | M54, M55 |
| CT-37 | recusa não altera o total | R12 | idempotência | Feature | `tests/Kit/CupomTest.php` | M56 |
| CT-38 | só os dois tipos são graváveis | R13 | EP | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M57, M58 |
| CT-39 | tipo desconhecido não concede desconto | R13 | EP | Feature | `tests/Kit/CupomTest.php` | M59 |
| CT-40 | contador não vem do formulário | R14 | mass assignment | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M60, M62 |
| CT-41 | organização não vem do formulário | R14 | mass assignment | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M61, M62 |

---

## Cogitado e Cortado

| Cenário cogitado | Por que foi cortado |
|---|---|
| percentual de 1% sobre total pequeno | mata o mesmo mutante de truncamento que a linha "fração 0,5" de CT-01 |
| desconto fixo muito acima do total (R$ 50 sobre R$ 30) | mata o mesmo mutante que a linha borda+1 de CT-03 |
| "o total devolvido é o total com desconto, não o desconto" como cenário próprio | já é o `Então` de CT-01; cenário separado não mata mutante novo |
| combinação "validade vencida **e** sem uso disponível" | duas partições inválidas no mesmo cenário: a primeira validação mascara a segunda, e o cenário provaria menos do que aparenta. Colapso declarado na tabela de decisão de R4 |
| "em modo single-tenant quem administra é o papel global" | é consequência das premissas P-02/P-09, não do requisito; CT-23 já roda em single-tenant e cobre o efeito observável |
| cupom que expira **entre** a validação e o consumo, como cenário próprio | o efeito observável é o de CT-13 (recusa sem consumir); M21 já morre em CT-14 |
| listagem paginada com 0, 1 e além do limite | paginação não é comportamento pedido — ver checklist de taxonomia |
| asserção sobre as mensagens de log do channel `cupom` | log não é pedido pelo card; afirmar sobre ele é testar o PRD |
| **CT-18 (uma aplicação, um registro)** | **mantido, mas sob revisão**: não é o único matador de nenhum mutante (M31 morre em CT-19, M27 em CT-16). Fica como guarda de contagem 1:1 entre contador e trilha, que é a invariante de RQ-13 + RQ-15 juntas. É o primeiro candidato a corte se o conjunto precisar encolher |

---

## Fechamento do Ciclo com Mutation Testing

Depois de implementar, o passo 6 deixa de prever e passa a medir:

```bash
vendor/bin/pest --mutate --covered-only --class="App\\Models\\Cupom"
```

- Exige `covers(Cupom::class)` ou `mutates(Cupom::class)` no arquivo de teste **e** driver de
  cobertura. `pest()->mutate()` no `Pest.php` não existe — não inventar.
- **O ambiente não tem PCOV** (`.ai/rules/testes-browser.md`), então este comando roda com Xdebug e
  é lento. Escopar por `--class` não é otimização: é a diferença entre rodar e não rodar.
- Cada mutante sobrevivente volta como lacuna de derivação: `>`→`>=` pede borda; `&&`→`||` pede
  linha de tabela de decisão; chamada removida pede cenário de rastreio de efeito.
- **Nunca usar cobertura de linha como meta.** O indicador é o mutation score.

---

## Revisão Adversarial

Perfil completo em quatro áreas ⇒ revisão obrigatória por sub-agente que **não** derivou os
cenários, com o contrato da skill (entrada: `00` + `04` + `05`; sem o PRD, sem o código, sem o
raciocínio de quem derivou). Resultado registrado em `## Resultado da Revisão Adversarial`, ao fim
deste arquivo.
