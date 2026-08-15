# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação.
> Do `01-plano-acao.md` foram lidos apenas: `## Superfície de UI`, rotas, paths de arquivo e stack.
> Nenhum comportamento esperado deste documento veio do plano — quando o plano e o requisito
> divergem, vale o requisito, e a divergência está registrada em `## Fronteira com o Plano`.

## Perfil de Derivação

| # | Área | P | I | P×I | Perfil | Justificativa do escore |
|---|---|---|---|---|---|---|
| A | Aplicação do cupom: existência, validade, limite e consumo do uso | 3 | 3 | **9** | **completo** | P=3: concorrência declarada no requisito (limite de usos compartilhado) e regra com três condições. I=3: dinheiro e irreversível — uso consumido não volta |
| B | Cálculo do desconto sobre o total | 2 | 3 | **6** | **padrão** | P=2: integra com o tipo do cupom e com a unidade da coluna. I=3: dinheiro |
| C | Autorização — quem cria, edita, exclui e lista | 3 | 3 | **9** | **completo** | P=3: a matriz de papéis é infraestrutura compartilhada e a regra é uma subtração parcial (tira escrita, mantém leitura). I=3: autorização |
| D | Unicidade e normalização do código | 2 | 3 | **6** | **padrão** | P=2: integra com o escopo de organização existente. I=3: colisão entre clientes é dado de terceiro |
| E | CRUD pela tela do painel | 2 | 3 | **6** | **padrão** | P=2: integra com Filament + Shield. I=3: é a tela que define os valores em dinheiro |
| F | Trilha de quem aplicou e quando | 2 | 3 | **6** | **padrão** | P=2: tabela nova, escrita num ponto só. I=3: compliance — trilha ausente só aparece no dia da auditoria |
| G | Isolamento entre organizações | 3 | 3 | **9** | **completo** | P=3: escopo global + índice composto + route binding, três mecanismos que podem divergir. I=3: dado de terceiro |

- **Técnicas aplicadas**: EP, BVA 3-valores (temporal com incremento de 1 s, contagem com incremento
  de 1 uso, monetária com incremento de 1 centavo), tabela de decisão, matriz papel × ação, tabela
  estado × visibilidade, rastreio de efeito colateral, normalização.
- **Regras**: 9 · **Cenários**: 37 · **Mutantes previstos**: 42 · **Sem matador**: 2
- **Escalação declarada de técnica**: a área B é `padrão` (BVA 2-valores), mas o BVA de **CT-06** é de
  3 valores. Motivo escrito: a fronteira é o **resto da divisão**, e com 2 valores é impossível
  distinguir truncar de arredondar — que é exatamente a premissa **P-06**, tomada sem resposta do
  usuário. Um BVA de 2 valores aqui pareceria cobertura e não seria.
- **Estouro de teto declarado**: a regra **R8** (perfil `padrão`, teto 3) tem 4 cenários. Justificado
  em `## Regra R8`.

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | Duas tabelas novas (cupom e registro de uso), a entidade `Cupom` com contador próprio, o tipo de desconto com dois valores, a tela de CRUD no painel de negócio, a policy da entidade e **a matriz de papéis, que é arquivo compartilhado**. O item de risco estrutural não é a entidade nova: é a matriz, que já sustenta cinco papéis e três painéis | CT-21, CT-29…CT-32 |
| **F**unction | Cadastrar; validar (existe / dentro da validade / tem uso); calcular o desconto conforme o tipo; consumir um uso; registrar quem aplicou; listar recortado por perfil. **Função escondida**: o recorte da listagem do usuário comum, que ninguém vê acontecer | CT-01…CT-16, CT-22…CT-25 |
| **D**ata | Entram: código (texto livre, digitado por humano), tipo (2 valores), valor (inteiro cuja **unidade muda com o tipo**), validade (instante), limite de usos (contagem), total do pedido (inteiro vindo de fora, em centavos) e o usuário que aplica (pode ser nulo). Já existem: as organizações e seus usuários. Dado ausente/nulo/vazio no código; dado com acento e emoji; dado **de outra organização**; contador que só o sistema move | CT-03, CT-06…CT-08, CT-27, CT-32, CT-33…CT-37 |
| **I**nterfaces | Três rotas de tela (`/app/{tenant}/cupons`, `…/create`, `…/{record}/edit`) e **uma chamada PHP direta** — o motor de aplicação, que o requisito descreve como "o sistema valida" sem dizer por onde se chega. Não há rota HTTP pública, comando, job, webhook nem import. O código também entra por seeder, tinker e factory, o que faz da normalização uma regra de **escrita**, não de formulário | CT-05, CT-24, CT-29, CT-30, CT-B01, CT-B02 |
| **P**latform | SQLite `:memory:` no teste × MySQL em produção: (a) índice único composto **não** barra duplicata quando a coluna de organização é nula — é o modo single-tenant, e por isso CT-26 precisa rodar **também** na suíte single-tenant, onde o banco não ajuda; (b) colação e sensibilidade a caixa diferem entre os dois bancos, o que torna a normalização do código uma regra de aplicação e não de banco; (c) conexão única em `:memory:` **não reproduz corrida real** — limitação declarada em CT-12. Sem Redis, sem fila, sem storage | CT-12 (ressalva), CT-26, CT-27 |
| **O**perations | Personas reais: administrador da organização (cadastra), usuário comum do negócio (só lê), dono da instalação (atravessa tudo), e o **comprador**, que é quem aplica — e que no modelo do requisito não tem tela. Uso indevido previsível: usuário comum tentando emitir desconto; alguém "corrigindo" o contador pela tela; o mesmo cupom aplicado duas vezes por duplo clique; código de outro cliente digitado por engano | CT-13, CT-17…CT-21, CT-32, CT-33 |
| **T**ime | Expiração é a metade temporal da regra: o cupom vale **até** um instante. Concorrência: dois consumos disputando o último uso. Ordem: entre validar e consumir pode passar a meia-noite. Fuso: o instante gravado, o instante do banco e o instante do app precisam ser o mesmo — e **não há como falsificar a divergência nesta suíte** (lacuna declarada em M05) | CT-01, CT-12, CT-14 |

Nenhuma dimensão ficou vazia. As duas com menos conteúdo (**P** e **T**) são as que produziram as
duas lacunas declaradas do gate — o que é o resultado esperado da varredura, e não um defeito dela.

## Mapa de Regras

| Regra | Origem (`RQ`) | Técnica | Perfil | Cenários |
|---|---|---|---|---|
| **R1** — Um cupom só é aceito quando existe, está dentro da validade e ainda tem uso disponível | RQ-09, RQ-10, RQ-11 | tabela de decisão + BVA 3-valores (temporal, 1 s) | completo | CT-01…CT-05 |
| **R2** — O desconto sai do tipo do cupom e nunca deixa o total negativo | RQ-03, RQ-04, RQ-12 | EP por tipo + BVA 3-valores (1 centavo) | padrão | CT-06…CT-08 |
| **R3** — Cada aplicação aceita consome exatamente um uso, e o total de aplicações nunca passa do limite | RQ-11, RQ-13 | BVA 3-valores (1 uso) + rastreio de efeito + concorrência | completo | CT-09…CT-13 |
| **R4** — Toda aplicação aceita registra quem aplicou e quando | RQ-15 | rastreio de efeito | padrão | CT-14…CT-16 |
| **R5** — Só o admin cria, edita e exclui cupom | RQ-07 | matriz papel × ação | completo | CT-17…CT-21 |
| **R6** — Os demais usuários listam, e só os que estão dentro da validade e com uso disponível | RQ-08 | tabela estado × visibilidade + matriz papel × ação | completo | CT-22…CT-25 |
| **R7** — O código não se repete, e a comparação não distingue caixa nem espaço nas bordas | RQ-02, RQ-14 | normalização + EP | padrão | CT-26…CT-28 |
| **R8** — O cadastro pela tela persiste código, tipo, valor, validade e limite | RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06 | EP + gate de tela de escrita | padrão | CT-29…CT-32 |
| **R9** — Cupom de uma organização não é listado, alcançado nem aplicado por outra | RQ-08, RQ-14 (sob **P-02**/**P-04**) | matriz papel × ação (IDOR) | completo | CT-33…CT-37 |

**Cobertura das cláusulas** — toda `RQ` do `00` gerou regra:

| RQ | Regra(s) | RQ | Regra(s) |
|---|---|---|---|
| RQ-01 | R8 | RQ-09 | R1 |
| RQ-02 | R7, R8 | RQ-10 | R1 |
| RQ-03 | R2, R8 | RQ-11 | R1, R3 |
| RQ-04 | R2, R8 | RQ-12 | R2 |
| RQ-05 | R1, R8 | RQ-13 | R3 |
| RQ-06 | R3, R8 | RQ-14 | R7, R9 |
| RQ-07 | R5 | RQ-15 | R4 |
| RQ-08 | R6, R9 | | |

### Perguntas em aberto

> **Desvio de processo declarado.** A skill manda replicar estas perguntas em
> `00-requisito.md` → `## Ambiguidades`. Elas **não** foram escritas lá: este `04` é o braço `exp-b`
> de um experimento e o `00` é entrada compartilhada com o braço de controle — editá-lo mudaria a
> entrada dos dois lados. As cinco abaixo estão prontas para colagem, e todo cenário que depende de
> uma delas está marcado `@premissa`.

| # | Pergunta | Premissa adotada para seguir | Bloqueia | Cenários `@premissa` |
|---|---|---|---|---|
| Q-01 | Aplicar o mesmo cupom duas vezes seguidas (duplo clique, retry) deve consumir **dois** usos ou é a mesma aplicação? O card fala de limite do cupom e nunca de repetição | **Não é idempotente**: cada aplicação aceita consome um uso e gera um registro. É a leitura literal de RQ-13 ("incrementa o contador"), e a alternativa exigiria uma chave de idempotência que ninguém pediu | R3 | CT-13 |
| Q-02 | No instante **exato** de `expira_em` o cupom ainda vale? (já registrada como pergunta 5 do `00`) | A validade **termina** no instante gravado — no instante exato o cupom já é recusado | R1 | CT-01 (linha "borda") |
| Q-03 | Excluir um cupom já usado apaga a trilha de quem o usou? RQ-07 dá ao admin o direito de excluir e RQ-15 pede trilha "pra auditar depois" — as duas cláusulas se contradizem e o card não resolve | A exclusão do cupom **leva a trilha junto**. É a leitura que mantém RQ-07 sem exceção; a alternativa (trilha órfã sobrevivente) é decisão de retenção que ninguém tomou | R4, R5 | CT-20 |
| Q-04 | O código tem tamanho máximo, ou conjunto de caracteres permitido? O card não diz nada | Sem limite derivável do requisito. **Nenhum cenário de BVA de tamanho foi escrito**, porque o limite de 40 caracteres existe só no plano — derivá-lo seria testar o plano | R7 | — (lacuna declarada) |
| Q-05 | Limite de usos igual a zero é cadastrável? E valor de desconto igual a zero? O card não dá mínimo para nenhum dos dois | Cupom com limite 0 nasce inaplicável, o que é inútil mas não é erro pelo texto do card. **Nenhum cenário afirma recusa**, porque a recusa viria do plano | R8 | — (lacuna declarada) |

## Fronteira com o Plano

Registrado porque três coisas do `01-plano-acao.md` **pareciam** oráculo e não são. Nenhuma virou
`Então` neste documento:

| O que o plano define | Por que não virou asserção |
|---|---|
| `situacao()` devolvendo os rótulos `Ativo` / `Esgotado` / `Expirado`, e a ordem entre eles | O requisito nunca fala em rótulo de situação. O que RQ-08 pede é **quem aparece na lista** — e é isso que CT-22 afirma. Afirmar a string do badge seria fixar a interpretação do plano |
| As colunas `valor_original` e `valor_desconto` na trilha | RQ-15 pede **quem** e **quando**, mais nada. CT-14 afirma esses dois e só. As duas colunas são enriquecimento do plano; se sumirem, o requisito continua atendido |
| As mensagens e o channel de log | O card não menciona log em lugar nenhum. Nenhum cenário assere log — e isso é decisão, não esquecimento |

O plano foi usado, como manda a skill, para: nomes de rota, paths de arquivo de teste, a tabela
`## Superfície de UI` (gate do `05`) e as versões da stack.

## Setup Global

### Versões confirmadas (`composer.json` lido)

Laravel `^13.17` · Filament `^5.6` · Pest `^5.1` · `pest-plugin-browser` `^5.0` ·
`pest-plugin-laravel` `^5.0` · `pest-plugin-mutate` (presente no `composer.lock`) · PHP `^8.3`.

Consequências para a API dos casos: `callAction(TestAction::make(...)->table($record))` — nunca
`callTableAction`; `assertActionDoesNotExist(TestAction::make('delete')->table($record))`;
`assertSchemaStateSet` no lugar de `assertFormSet`. O padrão em uso no projeto está em
`tests/Tenancy/AdminDaOrganizacaoTest.php` e `tests/Kit/ConviteTest.php`.

### Personas (helpers reais de `tests/Pest.php`)

- `o administrador da organização` — `usuarioComPapel('admin_organizacao', $acme)` (suíte `Tenancy`)
- `o dono da instalação` — `usuarioDoKit('master_global')` (suíte `Kit`, modo single-tenant)
- `o usuário comum do negócio` — `usuarioComPapel('panel_user', $acme)` / `usuarioCom('panel_user')`
- `o comprador` — qualquer `User` autenticado que aplica o cupom. **Não tem tela** (fora de escopo
  declarado no `00`); nos casos é o argumento de quem aplicou
- Contexto de painel para teste de componente: `noPainelDa($acme)` — sem ele, todo caso cai no ramo
  fechado da consulta e o resultado mede o arnês

### Fixtures

- `Cupom::factory()->create([...])` — cupom dentro da validade, com uso disponível
- `Cupom::factory()->expirado()` · `->esgotado()` · `->fixo($centavos)`
- **Armadilha de construção do fixture**: o contador de usos não é campo de mass assignment; um state
  que o passe em `state([...])` é **descartado em silêncio** e o cenário passa a medir outra coisa.
  O state precisa gravá-lo fora do mass assignment (`forceFill()` no `afterCreating`)
- Seeders: `ShieldPermissionsSeeder` + `PapeisSeeder`, **nesta ordem**, no `beforeEach` — o par que
  `tests/Kit/PaineisTest.php:20-22` já usa. Sem eles a tela responde 403 e o caso mede o seeder

### Fakes

- **Nenhum `Http::fake()`, `Queue::fake()` ou `Mail::fake()`**: a feature não chama serviço externo,
  não enfileira e não notifica. Declarado para que a ausência não pareça esquecimento
- `freezeTime()` / `travelTo()` nos casos temporais (CT-01, CT-14). `travelTo()` **dentro de
  closure**, ou com `travelBack()`, senão vaza para o caso seguinte e produz flake em `--parallel`
- Nenhum spy de log — ver `## Fronteira com o Plano`

### Estratégia de DB e alocação de suíte

- `RefreshDatabase`, já global em `tests/Pest.php` para `Kit`, `Tenancy`, `Browser` e `BrowserTenancy`
- **`tests/Kit/CupomTest.php`** (single-tenant): regra de negócio pura, cálculo, consumo, trilha,
  normalização e a matriz de permissões
- **`tests/Tenancy/CupomTenancyTest.php`**: tudo que precisa de organização — isolamento, unicidade
  por organização, componentes do painel `/app` e o recorte da listagem
- **`tests/BrowserTenancy/CupomTest.php`**: os CT-B (ver `05-casos-de-teste-browser.md`)
- **Por que nenhum cenário vai para `tests/Unit/`**, mesmo os três de cálculo puro (CT-06…CT-08):
  `tests/Pest.php` **não** liga `Tests\TestCase` a `Unit` — um arquivo lá roda sem o container do
  Laravel, e o cast do tipo do cupom (enum) não resolve. A camada mais barata **que existe neste
  projeto** para eles é a suíte `Kit`. Dívida registrada, não decisão de escopo

---

## Regra R1 — Um cupom só é aceito quando existe, está dentro da validade e ainda tem uso disponível

> `RQ-09`, `RQ-10`, `RQ-11` · perfil **completo** · técnicas: **tabela de decisão** (3 condições) +
> **BVA 3-valores** na fronteira temporal, granularidade **1 segundo** (o instante de validade é um
> `timestamp`, não uma data — comparar com granularidade de dia encurtaria a validade sem ninguém pedir)

### Tabela de decisão

| # | existe | dentro da validade | tem uso disponível | Ação | Cenário |
|---|---|---|---|---|---|
| 1 | não | — | — | recusa | CT-02 |
| 2 | código ausente/nulo/vazio | — | — | recusa | CT-03 |
| 3 | sim | **não** | sim | recusa | CT-01 (bordas 2 e 3) |
| 4 | sim | sim | **não** | recusa | CT-04 |
| 5 | sim | não | não | recusa | **colapsada** — a ação não depende da combinação, e as linhas 3 e 4 já provam cada condição **isolada**. Combiná-las mascararia qual das duas disparou |
| 6 | sim | sim | sim | aceita | CT-05 |

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Um cupom só é aceito quando existe, está dentro da validade e ainda tem uso disponível

    @premissa Q-02
    Esquema do Cenário: [CT-01] a validade é conferida no instante da aplicação
      Dado um cupom com uso disponível cuja validade termina em <validade>
      Quando o comprador aplica o cupom em <momento da aplicação>
      Então o resultado é "<resultado>"

      Exemplos:
        | validade              | momento da aplicação  | resultado | # borda                       |
        | 10:00:01 de hoje      | 10:00:00 de hoje      | aceito    | borda+1 (1 s dentro)          |
        | 10:00:00 de hoje      | 10:00:00 de hoje      | recusado  | borda exata — premissa Q-02   |
        | 09:59:59 de hoje      | 10:00:00 de hoje      | recusado  | borda−1 (1 s fora)            |
        | 23:59:59 de hoje      | 00:00:00 de amanhã    | recusado  | virada de meia-noite          |

    Cenário: [CT-02] código que não existe é recusado
      Dado que a organização tem um cupom de código "PROMO10"
      Quando o comprador aplica o código "PROMO99"
      Então nenhum cupom é devolvido para o código "PROMO99"
      E o total do pedido permanece em 12990 centavos

    Esquema do Cenário: [CT-03] código ausente, nulo ou vazio é recusado
      Dado um cupom "PROMO10" válido e com uso disponível na organização
      Quando o comprador aplica o código <código informado>
      Então nenhum cupom é devolvido
      E o contador de usos de "PROMO10" continua em 0

      Exemplos:
        | código informado | # partição inválida     |
        | (não informado)  | argumento ausente       |
        | (nulo)           | nulo                    |
        | ""               | string vazia            |
        | "   "            | só espaços em branco    |

    Cenário: [CT-04] cupom cujo limite já foi atingido é recusado
      Dado um cupom dentro da validade com limite de 2 usos e 2 usos já feitos
      Quando o comprador aplica o cupom
      Então nenhum cupom é devolvido
      E o contador de usos continua em 2

    Cenário: [CT-05] cupom existente, dentro da validade e com uso disponível é aceito
      Dado um cupom "PROMO10" de 10 por cento, válido até amanhã, com limite de 5 usos e 1 uso feito
      Quando o comprador aplica o cupom sobre um total de 12990 centavos
      Então o total passa a ser 11691 centavos
      E o contador de usos passa a 2
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M01 | `>=` no lugar de `>` na comparação da validade — o cupom continua aceito no instante exato em que expira | CT-01 (linha "borda exata") |
| M02 | A validade é conferida só no cadastro, e não na aplicação — o filtro some da consulta | CT-01 (linhas "borda−1" e "meia-noite") |
| M03 | `\|\|` no lugar de `&&` entre validade e uso disponível: basta uma das duas condições | CT-01 (linha "borda−1", com uso disponível) **e** CT-04 (dentro da validade, sem uso) — as duas são necessárias, cada uma sozinha sobreviveria |
| M04 | Código vazio tratado como "sem filtro": a consulta devolve o primeiro cupom da organização | CT-03 (todas as linhas) |
| M05 | A validade é comparada no fuso do banco, e não no do app | ⚠️ **sem matador** — app e banco rodam no mesmo fuso na suíte inteira (SQLite `:memory:`, mesmo processo). Falsificar exigiria banco com fuso divergente, que o arnês não tem. **Lacuna declarada**; ligada à pergunta 5 do `00` e ao item Timezone do checklist |

---

## Regra R2 — O desconto sai do tipo do cupom e nunca deixa o total negativo

> `RQ-03`, `RQ-04`, `RQ-12` · perfil **padrão** · técnicas: **EP** (uma partição por tipo, e são só
> dois — RQ-03 fecha o domínio) + **BVA 3-valores** com incremento de **1 centavo**
> · premissas **P-05** (unidade decidida pelo tipo), **P-06** (truncar) e **P-07** (nunca negativo)

```gherkin
# language: pt
  Regra: O desconto sai do tipo do cupom e nunca deixa o total negativo

    @premissa P-06
    Esquema do Cenário: [CT-06] o desconto percentual trunca a fração de centavo
      Dado um cupom de <percentual> por cento com uso disponível
      Quando o comprador aplica o cupom sobre um total de <total> centavos
      Então o total passa a ser <total final> centavos

      Exemplos:
        | percentual | total | total final | # borda                                   |
        | 10         | 9999  | 9000        | resto 0,9 — trunca para baixo (999)       |
        | 10         | 10000 | 9000        | resto 0 — divisão exata (1000)            |
        | 10         | 10001 | 9001        | resto 0,1 — trunca (1000, não 1001)       |
        | 50         | 5     | 3           | resto 0,5 — trunca (2), não arredonda (3) |

    @premissa P-05
    Cenário: [CT-07] o desconto de valor fixo subtrai o valor gravado, em centavos
      Dado um cupom de valor fixo de 1000 centavos, com uso disponível
      Quando o comprador aplica o cupom sobre um total de 12990 centavos
      Então o total passa a ser 11990 centavos

    @premissa P-07
    Esquema do Cenário: [CT-08] desconto maior que o total resulta em zero, nunca em negativo
      Dado um cupom de <tipo> no valor de <valor>, com uso disponível
      Quando o comprador aplica o cupom sobre um total de <total> centavos
      Então o total passa a ser <total final> centavos

      Exemplos:
        | tipo        | valor | total | total final | # borda                          |
        | valor fixo  | 3000  | 3001  | 1           | borda+1 — sobra 1 centavo        |
        | valor fixo  | 3000  | 3000  | 0           | borda — zera exatamente          |
        | valor fixo  | 3000  | 2999  | 0           | borda−1 — limitado em zero       |
        | porcentagem | 100   | 2999  | 0           | desconto integral, mesmo teto    |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M06 | Arredondamento (`round`) no lugar de truncamento no desconto percentual | CT-06 (linhas "resto 0,9" e "resto 0,5") |
| M07 | Arredondamento para cima (`ceil`) no desconto percentual | CT-06 (linha "resto 0,1") |
| M08 | Divisor errado (1000 em vez de 100) ou `*` ↔ `/` trocados | CT-06 e CT-07 — as duas afirmam o **valor** final, não só que houve desconto |
| M09 | Limite em zero ausente: total menor que o desconto fixo devolve valor negativo | CT-08 (linha "borda−1") |
| M10 | Os dois ramos do tipo trocados: o cupom de valor fixo é tratado como percentual | CT-07 (1000 como percentual daria 11691, não 11990) |

---

## Regra R3 — Cada aplicação aceita consome exatamente um uso, e o total nunca passa do limite

> `RQ-11`, `RQ-13` · perfil **completo** · técnicas: **BVA 3-valores** com incremento de **1 uso** +
> **rastreio de efeito colateral** (aconteceu / não aconteceu quando não devia / aconteceu uma só
> vez) + **concorrência**

```gherkin
# language: pt
  Regra: Cada aplicação aceita consome exatamente um uso, e o total nunca passa do limite

    Esquema do Cenário: [CT-09] o limite de usos é inclusivo no último uso
      Dado um cupom dentro da validade com limite de 3 usos e <usos feitos> usos já feitos
      Quando o comprador aplica o cupom
      Então o resultado é "<resultado>"

      Exemplos:
        | usos feitos | resultado | # borda                        |
        | 1           | aceito    | dentro da faixa                |
        | 2           | aceito    | borda−1 — o último uso vale    |
        | 3           | recusado  | borda — o limite é atingido    |
        | 4           | recusado  | borda+1 — estado inconsistente |

    Cenário: [CT-10] a aplicação aceita move o contador em exatamente um
      Dado um cupom dentro da validade com limite de 5 usos e 0 usos feitos
      Quando o comprador aplica o cupom uma vez
      Então o contador de usos passa a 1

    Cenário: [CT-11] a aplicação recusada não move o contador
      Dado um cupom expirado ontem, com limite de 5 usos e 0 usos feitos
      Quando o comprador aplica o cupom
      Então nenhum cupom é devolvido
      E o contador de usos continua em 0

    Cenário: [CT-12] duas aplicações simultâneas não furam o limite
      Dado um cupom dentro da validade com limite de 3 usos e 2 usos feitos
      Quando dois compradores aplicam o cupom ao mesmo tempo
      Então exatamente uma das duas aplicações é aceita
      E o contador de usos para em 3

    @premissa Q-01
    Cenário: [CT-13] aplicar o mesmo cupom duas vezes consome dois usos
      Dado um cupom dentro da validade com limite de 5 usos e 0 usos feitos
      Quando o comprador aplica o mesmo cupom duas vezes seguidas
      Então o contador de usos passa a 2
      E existem dois registros de aplicação
```

> **CT-12 — o que ele prova e o que não prova.** A suíte roda SQLite `:memory:` com conexão única:
> duas conexões simultâneas de verdade não existem no arnês. O cenário é escrito como
> **intercalação forçada** — o estado do cupom é levado ao limite entre a decisão e a escrita da
> primeira aplicação, que é exatamente a janela do defeito. Isso mata a implementação
> ler-comparar-salvar, mas **não** prova atomicidade sob carga real. Ver M15.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11 | `<=` no lugar de `<` na comparação com o limite — o cupom aceita um uso a mais que o contratado | CT-09 (linha "borda") |
| M12 | O contador é movido **antes** de validar: a recusa também consome | CT-11 |
| M13 | O contador não é movido no sucesso (chamada removida) | CT-10 |
| M14 | O contador é movido duas vezes por aplicação (efeito duplicado) | CT-10 — afirma o valor exato 1, não "maior que 0" |
| M15 | Consumo por ler-comparar-salvar, com janela entre a leitura e a escrita | CT-12 — ⚠️ **matador parcial**, declarado: mata a versão intercalada do defeito, não a corrida real. Fechar a lacuna exige `pest --mutate` sobre o método de consumo depois de implementado, e um teste de carga fora da suíte |

---

## Regra R4 — Toda aplicação aceita registra quem aplicou e quando

> `RQ-15` · perfil **padrão** · técnica: **rastreio de efeito colateral**, nas três formas
> (aconteceu / não aconteceu quando não devia / a contagem bate)

```gherkin
# language: pt
  Regra: Toda aplicação aceita registra quem aplicou e quando

    Cenário: [CT-14] a aplicação aceita registra o autor e o instante
      Dado um cupom com uso disponível e o comprador "ana@example.com" autenticado
      Quando o comprador aplica o cupom às 14:30:00 de hoje
      Então existe um registro de aplicação atribuído a "ana@example.com"
      E o instante do registro é 14:30:00 de hoje

    Cenário: [CT-15] a aplicação recusada não registra nada
      Dado um cupom esgotado, sem nenhum registro de aplicação
      Quando o comprador aplica o cupom
      Então nenhum registro de aplicação é criado

    Cenário: [CT-16] o contador e a trilha contam a mesma história
      Dado um cupom dentro da validade com limite de 5 usos e 0 usos feitos
      Quando o cupom é aplicado três vezes
      Então o contador de usos é 3
      E existem exatamente três registros de aplicação
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M16 | O registro de aplicação não é criado (chamada removida) | CT-14, CT-16 |
| M17 | O registro é criado também quando a aplicação é recusada | CT-15 |
| M18 | O registro nasce sem o autor (grava sempre nulo) | CT-14 — afirma o autor concreto, não a existência da linha |
| M19 | O registro é gravado fora da transação do consumo: o contador anda e a trilha se perde | CT-16 — é a única asserção que compara os dois números |

---

## Regra R5 — Só o admin cria, edita e exclui cupom

> `RQ-07` · perfil **completo** · técnica: **matriz papel × ação**, com a ação destrutiva
> obrigatória · premissa **P-02** (o "admin" do card é o administrador da organização)

### Matriz papel × ação

| Papel | criar | editar | excluir | listar | Cenário |
|---|---|---|---|---|---|
| administrador da organização | ✅ | ✅ | ✅ | ✅ | CT-20, CT-21, CT-29, CT-30 |
| usuário comum do negócio | ❌ | ❌ | ❌ | ✅ | CT-17, CT-18, CT-19, CT-21, CT-24 |
| dono da instalação | ✅ | ✅ | ✅ | ✅ | CT-21 (é ele quem cumpre RQ-07 no modo single-tenant) |
| admin da instalação / infra | — | — | — | — | não alcançam o painel de negócio; coberto por `tests/Kit/PaineisTest.php`, que já afirma o recorte de painel por papel. Célula dispensada com motivo |

```gherkin
# language: pt
  Regra: Só o admin cria, edita e exclui cupom

    @premissa P-02
    Cenário: [CT-17] o usuário comum não alcança a tela de cadastro de cupom
      Dado um usuário comum do negócio na organização Acme
      Quando ele abre a tela de cadastro de cupom
      Então o acesso é negado

    Cenário: [CT-18] a exclusão não é oferecida ao usuário comum
      Dado um usuário comum do negócio e um cupom cadastrado na organização Acme
      Quando ele lista os cupons
      Então a ação de excluir não é oferecida em nenhuma linha

    Cenário: [CT-19] esconder o botão não é a barreira: a exclusão chamada direto é recusada
      Dado um usuário comum do negócio e um cupom cadastrado na organização Acme
      Quando ele dispara a exclusão do cupom sem passar pelo botão
      Então a exclusão é recusada
      E o cupom continua cadastrado

    @premissa Q-03
    Cenário: [CT-20] o administrador da organização exclui um cupom já usado
      Dado o administrador da organização Acme e um cupom com 2 usos já feitos
      Quando ele exclui o cupom
      Então o cupom deixa de existir
      E os registros de aplicação daquele cupom também deixam de existir

    Esquema do Cenário: [CT-21] a matriz de papéis separa escrita de leitura
      Dado um usuário com o papel <papel>
      Quando a matriz de permissões é consultada
      Então a permissão de criar cupom é "<escrita>"
      E a permissão de listar cupons é "<leitura>"

      Exemplos:
        | papel                        | escrita | leitura | # célula                          |
        | administrador da organização | tem     | tem     | RQ-07 no modo multi-organização   |
        | usuário comum do negócio     | não tem | tem     | RQ-07 e RQ-08 juntas — a célula que o recorte existe para produzir |
        | dono da instalação           | tem     | tem     | RQ-07 no modo single-tenant       |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M20 | A autorização de escrita vive só na tela: o botão some e a ação continua chamável | CT-19 |
| M21 | O recorte tira a entidade inteira do usuário comum, levando a leitura junto | CT-21 (linha "usuário comum", coluna leitura) e CT-24 |
| M22 | O recorte casa por pedaço do nome da permissão e erra o alvo — sobra ou falta permissão | CT-21 (as três linhas juntas: uma só não acusa) |
| M23 | A autorização de criação devolve verdadeiro sem consultar a permissão | CT-17 |
| M24 | A exclusão fica liberada a todo mundo que enxerga a tela | CT-18 **e** CT-19 |

---

## Regra R6 — Os demais usuários listam, e só os que estão dentro da validade e com uso disponível

> `RQ-08` · perfil **completo** · técnicas: **tabela estado × visibilidade** (100% das células, com
> as inválidas explícitas) + **matriz papel × ação** · premissa **P-03** ("ativo" é derivado de
> validade e limite, e não uma coluna de liga-desliga)

### Tabela estado × visibilidade

| Estado do cupom | dentro da validade | tem uso disponível | visível ao usuário comum | visível ao administrador |
|---|---|---|---|---|
| aplicável | sim | sim | ✅ CT-22 | ✅ CT-23 |
| expirado | não | sim | ❌ CT-22 | ✅ CT-23 |
| esgotado | sim | não | ❌ CT-22 | ✅ CT-23 |
| expirado e esgotado | não | não | ❌ CT-22 | ✅ CT-23 |

```gherkin
# language: pt
  Regra: Os demais usuários listam, e só os que estão dentro da validade e com uso disponível

    @premissa P-03
    Esquema do Cenário: [CT-22] o usuário comum só vê o cupom que ainda pode ser aplicado
      Dado um cupom <validade> e <uso> na organização Acme
      Quando o usuário comum do negócio lista os cupons
      Então o cupom "<aparece>" na lista

      Exemplos:
        | validade         | uso                  | aparece    | # célula              |
        | dentro da validade | com uso disponível  | aparece    | única célula positiva |
        | expirado           | com uso disponível  | não aparece| só a validade barra   |
        | dentro da validade | sem uso disponível  | não aparece| só o limite barra     |
        | expirado           | sem uso disponível  | não aparece| as duas barram        |

    Cenário: [CT-23] o recorte não vale para quem administra
      Dado um cupom expirado e um cupom esgotado na organização Acme
      Quando o administrador da organização lista os cupons
      Então os dois cupons aparecem na lista

    Cenário: [CT-24] o usuário comum abre a listagem de cupons
      Dado um usuário comum do negócio e um cupom aplicável na organização Acme
      Quando ele abre a listagem de cupons
      Então a tela responde sem negar o acesso
      E o cupom aplicável aparece na lista

    Cenário: [CT-25] o recorte da lista alcança também a URL direta
      Dado um usuário comum do negócio e um cupom expirado da própria organização Acme
      Quando ele abre a tela desse cupom pela URL direta
      Então o cupom não é encontrado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M25 | O recorte é aplicado a todo mundo: o administrador deixa de ver expirado e esgotado | CT-23 |
| M26 | O recorte olha só a validade e ignora o limite: o esgotado continua listado | CT-22 (linha "só o limite barra") |
| M27 | O recorte olha só o limite e ignora a validade: o expirado continua listado | CT-22 (linha "só a validade barra") |
| M28 | O recorte é escrito só na montagem da tabela, e não na consulta base: a URL direta atravessa | CT-25 |
| M29 | O recorte vira negação de acesso: o usuário comum leva 403 na listagem, contra RQ-08 | CT-24 |

---

## Regra R7 — O código não se repete, e a comparação não distingue caixa nem espaço nas bordas

> `RQ-02`, `RQ-14` · perfil **padrão** · técnicas: **normalização** (caixa, espaços nas bordas,
> acento, unicode) + **EP** · premissa **P-04** (unicidade **por organização**)
> **Sem BVA de tamanho de código** — ver pergunta Q-04: o limite de 40 caracteres é do plano, não do
> requisito, e derivá-lo seria testar o plano

```gherkin
# language: pt
  Regra: O código não se repete, e a comparação não distingue caixa nem espaço nas bordas

    Esquema do Cenário: [CT-26] código repetido na mesma organização é recusado
      Dado um cupom "PROMO10" já cadastrado na organização Acme
      Quando o administrador da organização cadastra um cupom com o código <código novo>
      Então o cadastro é "<resultado>"

      Exemplos:
        | código novo | resultado | # partição                        |
        | "PROMO10"   | recusado  | idêntico                          |
        | "promo10"   | recusado  | mesma palavra, caixa diferente    |
        | " PROMO10 " | recusado  | mesma palavra, espaços nas bordas |
        | "PROMO11"   | aceito    | código diferente                  |

    Esquema do Cenário: [CT-27] o código é gravado normalizado e encontrado em qualquer caixa
      Dado um cupom cadastrado com o código <digitado>
      Quando o comprador aplica o código <aplicado>
      Então o cupom encontrado é o de código <gravado>

      Exemplos:
        | digitado     | aplicado     | gravado    | # normalização           |
        | " promo10 "  | "PROMO10"    | "PROMO10"  | caixa e espaços          |
        | "Promoção"   | "promoção"   | "PROMOÇÃO" | acento                   |
        | "PROMO🎉"    | "promo🎉"    | "PROMO🎉"  | unicode de 4 bytes       |

    Cenário: [CT-28] o código de um cupom excluído pode ser reaproveitado
      Dado um cupom "BEMVINDO" que foi cadastrado e depois excluído na organização Acme
      Quando o administrador da organização cadastra um novo cupom "BEMVINDO"
      Então o cadastro é aceito
```

> **Onde CT-26 precisa rodar, e por quê.** As quatro linhas rodam na suíte de organização; a linha
> "idêntico" roda **também** na suíte single-tenant. Motivo de plataforma: com a organização nula,
> o índice único composto do banco **não** barra a duplicata (a maioria dos bancos não considera
> dois nulos iguais). É lá que a regra de aplicação é a única barreira — e é lá que ela pode faltar
> sem ninguém perceber.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M30 | A unicidade compara sem normalizar: duas linhas com a mesma palavra em caixas diferentes convivem | CT-26 (linha "caixa diferente") |
| M31 | A normalização acontece só na leitura, e o código é gravado como veio | CT-27 (coluna "gravado") |
| M32 | Espaços nas bordas não são removidos: o código com espaço vira um cupom distinto | CT-26 (linha "espaços") e CT-27 (linha "caixa e espaços") |
| M33 | A unicidade barra o recadastro depois da exclusão | CT-28 |

---

## Regra R8 — O cadastro pela tela persiste código, tipo, valor, validade e limite

> `RQ-01` a `RQ-06` · perfil **padrão** · técnicas: **EP** (uma partição inválida por linha) +
> **gate de tela de escrita** (toda rota de criação e de edição precisa de um cenário de **gravação
> por componente**, e não só de visita)
>
> **Estouro de teto declarado** (padrão = 3, aqui 4): CT-32 é o item **mass assignment** do checklist
> de taxonomia. Ele não cabe em R3 sem quebrar o eixo daquela regra (que é sobre consumo) nem em R5
> (que é sobre papel), e a alternativa — deixá-lo fora — é o caso em que o contador vira campo de
> formulário e todo o resto da R3 passa a medir nada. Sinal de que a regra poderia ser duas
> ("o que a tela grava" e "o que a tela **não** pode gravar"); mantida como uma, com o estouro escrito.

```gherkin
# language: pt
  Regra: O cadastro pela tela persiste código, tipo, valor, validade e limite

    Cenário: [CT-29] o cadastro pela tela grava os cinco atributos do cupom
      Dado o administrador da organização Acme na tela de cadastro de cupom
      Quando ele grava um cupom "BLACKFRIDAY", do tipo porcentagem, valor 15, válido até
        31/12/2026 às 23:59 e limite de 200 usos
      Então existe um cupom "BLACKFRIDAY" com tipo porcentagem, valor 15, validade
        31/12/2026 às 23:59 e limite de 200 usos
      E o contador de usos desse cupom começa em 0

    Cenário: [CT-30] a edição pela tela persiste a alteração
      Dado um cupom "BLACKFRIDAY" de 15 por cento com limite de 200 usos na organização Acme
      Quando o administrador da organização altera o limite para 50 pela tela de edição
      Então o cupom passa a ter limite de 50 usos
      E o código continua "BLACKFRIDAY"

    Esquema do Cenário: [CT-31] o cadastro é recusado quando falta um atributo obrigatório
      Dado o administrador da organização Acme na tela de cadastro de cupom
      Quando ele grava um cupom sem informar <atributo omitido>
      Então o cadastro é recusado com erro no campo <atributo omitido>
      E nenhum cupom é criado

      Exemplos:
        | atributo omitido | # partição inválida isolada |
        | o código         | RQ-02                       |
        | o tipo           | RQ-03                       |
        | o valor          | RQ-04                       |
        | a validade       | RQ-05                       |
        | o limite de usos | RQ-06                       |

    Cenário: [CT-32] o contador de usos não é campo de cadastro
      Dado o administrador da organização Acme na tela de cadastro de cupom
      Quando ele grava um cupom informando também um contador de usos igual a 99
      Então o cupom nasce com o contador de usos em 0
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M34 | Um dos cinco atributos fica fora do mass assignment: a tela envia, o valor é descartado **em silêncio** e o registro nasce incompleto sem erro nenhum | CT-29 — afirma os cinco valores, não só a existência do registro |
| M35 | Falta a obrigatoriedade de um dos atributos: o cupom nasce sem validade ou sem limite | CT-31 (uma linha por atributo — uma só não acusa) |
| M36 | A gravação da edição quebra enquanto a tela continua abrindo (o defeito clássico do kit: `GET` verde, `save` quebrado) | CT-30 |
| M37 | O contador entra no mass assignment e vira campo editável pela tela | CT-32 |

---

## Regra R9 — Cupom de uma organização não é listado, alcançado nem aplicado por outra

> `RQ-08`, `RQ-14` sob as premissas **P-02** (cupom é dado da organização) e **P-04** (unicidade por
> organização) · perfil **completo** · técnica: **matriz papel × ação** aplicada à autorização
> horizontal (IDOR) — dois donos diferentes no setup de todo cenário

```gherkin
# language: pt
  Regra: Cupom de uma organização não é listado, alcançado nem aplicado por outra

    @premissa P-02
    Cenário: [CT-33] o código de outra organização não é aceito
      Dado um cupom "BLACKFRIDAY" aplicável na organização Globex
      Quando o comprador da organização Acme aplica o código "BLACKFRIDAY"
      Então nenhum cupom é devolvido
      E o contador de usos do cupom da Globex continua em 0

    @premissa P-04
    Cenário: [CT-34] duas organizações podem ter o mesmo código
      Dado um cupom "BLACKFRIDAY" já cadastrado na organização Globex
      Quando o administrador da organização Acme cadastra um cupom "BLACKFRIDAY"
      Então o cadastro é aceito
      E cada organização passa a ter o seu próprio cupom "BLACKFRIDAY"

    Cenário: [CT-35] a listagem mostra só os cupons da própria organização
      Dado um cupom aplicável em cada uma das organizações Acme e Globex
      Quando o administrador da organização Acme lista os cupons
      Então só o cupom da Acme aparece na lista

    Cenário: [CT-36] o cupom de outra organização não é alcançável pela URL direta
      Dado um cupom da organização Globex
      Quando o administrador da organização Acme abre a tela desse cupom pela URL direta
      Então o cupom não é encontrado

    Cenário: [CT-37] aplicar um cupom não move o contador do homônimo da outra organização
      Dado um cupom "BLACKFRIDAY" em cada uma das organizações Acme e Globex, cada um com 0 usos
      Quando o comprador da organização Acme aplica o cupom "BLACKFRIDAY"
      Então o contador do cupom da Acme passa a 1
      E o contador do cupom da Globex continua em 0
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M38 | A consulta de aplicação não é escopada pela organização: o código do vizinho é aceito | CT-33 |
| M39 | A unicidade é global em vez de por organização — o primeiro cliente a cadastrar a palavra impede todos os outros, e a mensagem de erro revela que o cupom do vizinho existe | CT-34 |
| M40 | A listagem não é escopada: o cupom do vizinho aparece na lista | CT-35 |
| M41 | O route binding resolve o registro sem escopo: a URL direta alcança o cupom do vizinho | CT-36 |
| M42 | O consumo localiza o cupom só pelo código e move o contador do homônimo errado | CT-37 |

---

## Checklist de Taxonomia

Percorrido item a item, uma vez sobre a feature inteira.

| Item | Aplicável? | Cenário / motivo da dispensa |
|---|---|---|
| **IDOR / autorização horizontal** | **sim** | CT-36 (URL direta com o registro de outro dono), CT-33, CT-37. Dois donos no setup dos três |
| **Idempotência** | **sim, com semântica invertida** | CT-13. A repetição **deve** consumir dois usos — a operação não é idempotente por decisão declarada (pergunta Q-01). O cenário existe para fixar a decisão, não para provar idempotência |
| **Concorrência** | **sim** | CT-12, com a limitação de arnês declarada (M15). É o item de maior risco da feature: contador com limite compartilhado |
| **Ausente ≠ nulo ≠ vazio** | **sim** | CT-03 (as quatro formas do código na aplicação) e CT-31 (atributo omitido no cadastro). Semântica declarada: as quatro recusam, e recusam **pelo mesmo motivo** |
| **Paginação** | **não** | Nenhuma cláusula do card fala de volume, tamanho de página ou ordenação. A paginação é do componente de tabela e já é coberta pela suíte do kit. Escrever cenário aqui seria testar o Filament, não o requisito. **Risco residual registrado**: se o recorte de RQ-08 for aplicado só à página visível, CT-22 ainda o pega, porque afirma ausência, não posição |
| **Ordenação por coluna** | **não** | Mesmo motivo. Nenhuma RQ define ordem, e sem ordem definida não há oráculo |
| **Timezone / DST** | **sim, parcialmente coberto** | CT-01 cobre a fronteira de 1 segundo e a virada de meia-noite. A divergência de fuso entre app e banco é **M05, sem matador** — o arnês roda os dois no mesmo fuso |
| **Texto livre (acento, emoji, espaços, limite de tamanho)** | **sim, exceto tamanho** | CT-27 (acento, emoji de 4 bytes, espaços nas bordas) e CT-03 (só espaços). **Sem BVA de tamanho**: o limite de 40 caracteres é do plano, não do requisito — pergunta Q-04 |
| **Unicidade + exclusão** | **sim** | CT-28 (cadastrar → excluir → recadastrar com o mesmo código). A entidade **não** tem exclusão lógica; se ganhar, este é o cenário que muda de resultado primeiro |
| **CRUD combinado (ID inexistente, excluir duas vezes, editar sem alterar)** | **parcialmente** | Registro inexistente e registro de outro dono → CT-25 e CT-36. "Excluir duas vezes" e "editar sem alterar nada" **dispensados**: o resultado seria comportamento do route binding do framework, não do requisito, e nenhuma RQ fala deles |
| **Mass assignment** | **sim** | CT-32 — o contador de usos enviado pelo formulário é ignorado. É o campo mais atraente para o defeito: quem "corrige" um contador pela tela apaga a trilha sem apagar linha nenhuma |
| **Upload** | **não** | A feature não recebe arquivo. Nenhum campo do card é binário |
| **Precisão monetária** | **sim** | CT-06, CT-07, CT-08. **Nenhum exemplo deste documento usa ponto flutuante**: todo valor é inteiro em centavos, e o único ponto de fração (o percentual) é resolvido por truncamento explícito |

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | A validade é conferida no instante da aplicação | R1 | BVA 3-valores (1 s) | Feature | `tests/Kit/CupomTest.php` | M01, M02, M03 |
| CT-02 | Código que não existe é recusado | R1 | tabela de decisão | Feature | `tests/Kit/CupomTest.php` | M02 |
| CT-03 | Código ausente, nulo ou vazio é recusado | R1 | EP (inválidas isoladas) | Feature | `tests/Kit/CupomTest.php` | M04 |
| CT-04 | Cupom cujo limite já foi atingido é recusado | R1 | tabela de decisão | Feature | `tests/Kit/CupomTest.php` | M03 |
| CT-05 | Cupom válido e com uso disponível é aceito | R1 | tabela de decisão (célula positiva) | Feature | `tests/Kit/CupomTest.php` | M02, M08 |
| CT-06 | O desconto percentual trunca a fração de centavo | R2 | BVA 3-valores (1 centavo) | Feature | `tests/Kit/CupomTest.php` | M06, M07, M08 |
| CT-07 | O desconto fixo subtrai o valor em centavos | R2 | EP por tipo | Feature | `tests/Kit/CupomTest.php` | M08, M10 |
| CT-08 | Desconto maior que o total resulta em zero | R2 | BVA 3-valores (1 centavo) | Feature | `tests/Kit/CupomTest.php` | M09 |
| CT-09 | O limite de usos é inclusivo no último uso | R3 | BVA 3-valores (1 uso) | Feature | `tests/Kit/CupomTest.php` | M11 |
| CT-10 | A aplicação aceita move o contador em exatamente um | R3 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M13, M14 |
| CT-11 | A aplicação recusada não move o contador | R3 | rastreio de efeito (negativo) | Feature | `tests/Kit/CupomTest.php` | M12 |
| CT-12 | Duas aplicações simultâneas não furam o limite | R3 | concorrência | Feature | `tests/Kit/CupomTest.php` | M15 (parcial) |
| CT-13 | Aplicar duas vezes consome dois usos | R3 | rastreio de efeito (contagem) | Feature | `tests/Kit/CupomTest.php` | M14 |
| CT-14 | A aplicação aceita registra autor e instante | R4 | rastreio de efeito | Feature | `tests/Kit/CupomTest.php` | M16, M18 |
| CT-15 | A aplicação recusada não registra nada | R4 | rastreio de efeito (negativo) | Feature | `tests/Kit/CupomTest.php` | M17 |
| CT-16 | O contador e a trilha contam a mesma história | R4 | rastreio de efeito (contagem) | Feature | `tests/Kit/CupomTest.php` | M16, M19 |
| CT-17 | O usuário comum não alcança a tela de cadastro | R5 | matriz papel × ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M23 |
| CT-18 | A exclusão não é oferecida ao usuário comum | R5 | matriz papel × ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M24 |
| CT-19 | A exclusão chamada direto é recusada | R5 | matriz papel × ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M20, M24 |
| CT-20 | O administrador exclui um cupom já usado | R5 | matriz papel × ação (destrutiva) | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M24 |
| CT-21 | A matriz de papéis separa escrita de leitura | R5 | matriz papel × ação | Feature | `tests/Kit/CupomTest.php` | M21, M22 |
| CT-22 | O usuário comum só vê o cupom aplicável | R6 | estado × visibilidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M26, M27 |
| CT-23 | O recorte não vale para quem administra | R6 | estado × visibilidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M25 |
| CT-24 | O usuário comum abre a listagem | R6 | matriz papel × ação | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M21, M29 |
| CT-25 | O recorte alcança também a URL direta | R6 | estado × visibilidade | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M28 |
| CT-26 | Código repetido na mesma organização é recusado | R7 | normalização + EP | Livewire | `tests/Tenancy/CupomTenancyTest.php` **e** `tests/Kit/CupomTest.php` (linha "idêntico") | M30, M32 |
| CT-27 | O código é gravado normalizado | R7 | normalização | Feature | `tests/Kit/CupomTest.php` | M31, M32 |
| CT-28 | O código de um cupom excluído é reaproveitável | R7 | EP | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M33 |
| CT-29 | O cadastro pela tela grava os cinco atributos | R8 | gate de tela de escrita | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M34 |
| CT-30 | A edição pela tela persiste a alteração | R8 | gate de tela de escrita | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M36 |
| CT-31 | O cadastro recusa atributo obrigatório faltando | R8 | EP (inválidas isoladas) | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M35 |
| CT-32 | O contador de usos não é campo de cadastro | R8 | mass assignment | Feature | `tests/Kit/CupomTest.php` | M37 |
| CT-33 | O código de outra organização não é aceito | R9 | IDOR | Feature | `tests/Tenancy/CupomTenancyTest.php` | M38 |
| CT-34 | Duas organizações podem ter o mesmo código | R9 | IDOR | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M39 |
| CT-35 | A listagem mostra só os cupons da própria organização | R9 | IDOR | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M40 |
| CT-36 | O cupom de outra organização não é alcançável pela URL | R9 | IDOR | Livewire | `tests/Tenancy/CupomTenancyTest.php` | M41 |
| CT-37 | Aplicar não move o contador do homônimo | R9 | IDOR | Feature | `tests/Tenancy/CupomTenancyTest.php` | M42 |

### Poda aplicada (passo 7)

| O que foi cortado | Motivo |
|---|---|
| Cenário do rótulo de situação (`Ativo` / `Expirado` / `Esgotado`) | Não mata mutante do requisito — o rótulo é do plano. O que RQ-08 pede é a **ausência** da linha na lista, e isso é CT-22 |
| Cenário "a tela de listagem abre para o administrador" | Caminho feliz redundante: CT-23 e CT-35 já montam a mesma tela com asserção sobre conteúdo. Uma tela aberta sem asserção de conteúdo não é oráculo |
| Cenário de log de recusa | Nenhuma cláusula do card menciona log |
| Célula 5 da tabela de decisão de R1 (expirado **e** esgotado) | Duas partições inválidas no mesmo cenário: a primeira validação a disparar mascara a segunda, e as linhas 3 e 4 já provam cada uma isolada |
| Cenário de BVA no tamanho do código | Fronteira que só existe no plano (pergunta Q-04) |

### Cobertura do gate de tela de escrita

| Rota de escrita (`## Superfície de UI` do plano) | Cenário de gravação por componente |
|---|---|
| `/app/{tenant}/cupons/create` | **CT-29** (`fillForm` → `call('create')` → asserção sobre os cinco atributos) |
| `/app/{tenant}/cupons/{record}/edit` | **CT-30** (`fillForm` → `call('save')` → asserção sobre o atributo alterado) |
| Ação de exclusão na linha da tabela | **CT-19**, **CT-20** (`callAction(TestAction::make('delete')->table($record))`) |

Nenhuma tela de escrita está coberta apenas por visita.

## Casos de Teste de Browser

O gate do `05` **passa**. Ver `05-casos-de-teste-browser.md`.

Resumo da decisão: há linhas em `## Superfície de UI` e existe uma asserção que **nenhum teste de
componente consegue falsificar** — o campo de valor muda de rótulo e de unidade conforme o tipo
escolhido, e essa mudança depende de um ciclo de JavaScript. Um teste de componente que preenche o
tipo dispara a atualização no servidor **de qualquer jeito**, com ou sem a ligação reativa: o defeito
"a tela diz R$ e grava porcentagem" passa verde no componente e só morre no navegador.

## Pós-implementação (fechamento do ciclo)

```bash
vendor/bin/pest --mutate --covered-only --class="App\\Models\\Cupom"
vendor/bin/pest --parallel --group=kit      # backend
vendor/bin/pest --testsuite=Browser         # telas, em série — nunca --parallel
```

- O arquivo de teste precisa declarar `covers(Cupom::class)` ou `mutates(Cupom::class)` — sem isso o
  `--mutate` não tem escopo. **Não existe `pest()->mutate()` em `Pest.php`**
- O ambiente não tem PCOV (`.ai/rules/testes-browser.md`): a mutação com Xdebug é lenta, então escopar
  por `--class` não é otimização, é condição de terminar
- Todo mutante sobrevivente volta para este documento como **lacuna de derivação**, com a técnica que
  faltou, e vira cenário novo. Os dois candidatos conhecidos já estão declarados: **M05** (fuso) e
  **M15** (corrida real)

## Revisão Adversarial

Obrigatória — três das nove regras estão no perfil `completo`. **Não executada nesta rodada**: o
contrato da skill exige um sub-agente que **não** derivou os cenários e que **não** receba o plano
nem o raciocínio de quem derivou, e esta execução não tem esse segundo agente disponível.
Registrado como pendência bloqueante antes de a implementação começar, com o contrato pronto:

```text
Entrada: 00-requisito.md + 04-casos-de-teste.md + 05-casos-de-teste-browser.md
NÃO receber: 01-plano-acao.md, código, nem este raciocínio
Tarefa: PROVAR que este conjunto deixa passar um defeito (5 implementações erradas plausíveis
        que passariam por TODOS os cenários; toda asserção fraca; todo cenário sem "Então";
        todo cenário com mais de um "Quando")
PROIBIDO: elogiar, reescrever cenário, dizer "está bom"
```
