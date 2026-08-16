# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`  
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| Cálculo do desconto | 3 | 3 | 9 | completo |
| Validação de domínio (criação/edição) | 3 | 3 | 9 | completo |
| Aplicação do cupom | 3 | 3 | 9 | completo |
| Autorização | 3 | 3 | 9 | completo |
| Listagem / escopo de leitura | 2 | 2 | 4 | padrão |
| Trilha de auditoria | 3 | 2 | 6 | padrão |
| Concorrência | 3 | 3 | 9 | completo |

- Técnicas aplicadas: EP, BVA 3-valores, tabela de decisão, matriz papel × ação, rastreio de efeito.
- Cenários: 60 · Regras: 12 · Mutantes previstos: 38 · Sem matador: 5 (todos declarados como lacunas).

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| S | model `Cupom`, model `CupomUso`, enum `TipoDeDesconto`, resource Filament, policy, seeder | CT-01…CT-10 |
| F | CRUD, cálculo de desconto, validação na aplicação, consumo atômico, trilha de uso | CT-11…CT-40 |
| D | código, tipo, valor, expira_em, limite_de_usos, usos, tenant_id, cupom_usos | CT-01…CT-40 |
| I | painel `/app`, formulário Filament, rota HTTP, método `aplicarEm()` chamável | CT-41…CT-50 |
| P | Filament 5, Pest 5, SQLite em teste, `pest-plugin-browser` disponível | — |
| O | admin_organizacao cria/gerencia; panel_user lista; usuário anônimo sem acesso | CT-41…CT-50 |
| T | validade, limite de usos, concorrência, timezone, trilha temporal | CT-27, CT-30, CT-31, CT-57 |

## Mapa de Regras

| Regra | Área | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| R1 — Código é obrigatório, normalizado e único por organização | criação/edição | RQ-02, RQ-14 | EP + normalização | CT-01, CT-02, CT-03, CT-04, CT-13, CT-24, CT-51, CT-53 |
| R2 — Tipo só aceita `porcentagem` ou `valor fixo` | criação/edição | RQ-03 | EP | CT-05, CT-07 |
| R3 — Valor é `unsignedInteger`, com fronteiras condicionadas ao tipo | criação/edição/uso | RQ-04 | BVA 3-valores + domínio condicionado | CT-05, CT-06, CT-07, CT-08, CT-11, CT-12, CT-16, CT-33, CT-56 |
| R4 — Validade é futura na criação e borda exata no uso | criação/uso | RQ-05, RQ-10 | BVA 3-valores (data/hora) | CT-09, CT-12, CT-27, CT-57 |
| R5 — Limite de usos é ≥1 e a borda é inclusiva | criação/uso | RQ-06, RQ-11 | BVA 3-valores | CT-10, CT-30, CT-31, CT-36 |
| R6 — Aplicação recusa cupom inexistente, expirado ou esgotado | uso | RQ-09, RQ-10, RQ-11 | tabela de decisão | CT-25, CT-26, CT-28, CT-29, CT-32, CT-37 |
| R7 — Desconto percentual nunca excede o total; fixo limita em zero | uso | RQ-12 | BVA / oráculo exato | CT-32, CT-33, CT-34, CT-56 |
| R8 — Uso bem-sucedido consome exatamente um uso e grava trilha | uso | RQ-13, RQ-15 | rastreio de efeito | CT-35, CT-36, CT-38, CT-39, CT-40 |
| R9 — Usuário comum só lista cupons ativos | listagem | RQ-08 | matriz papel × ação | CT-20, CT-21, CT-22, CT-23, CT-52 |
| R10 — Só admin cria, edita e exclui | autorização | RQ-07 | matriz papel × ação | CT-41…CT-50 |
| R11 — Concorrência não furra o limite de usos | concorrência | RQ-11, RQ-13 | heurística de race | CT-05, CT-31 |
| R12 — Trilha de auditoria registra quem e quando | auditoria | RQ-15 | rastreio de efeito | CT-35, CT-39, CT-40, CT-49 |

## Fronteira com o Plano

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| Nome dos métodos `aplicarEm()`, `descontoSobre()`, `valido()` | escolha de implementação | detalhe do cenário |
| Nome da tabela `cupom_usos` | escolha de implementação | detalhe do cenário |
| Texto exato de mensagens de erro | comportamento visível que o requisito não determina | pergunta ao usuário |
| `intdiv` como modo de arredondamento percentual | escolha de implementação (P-06) | detalhe do cenário — o oráculo é o valor observável |

**Perguntas em aberto** (replicadas do `00-requisito.md`):
- A-05/A-06 — percentual fracionário e direção de arredondamento: premissa adotada = inteiro 1..100, truncamento (CT-33 com 29%).
- A-01 — entidade `Pedido` fora de escopo; idempotência no agregado `Pedido` fica como lacuna declarada (CT-58).

## Setup Global

### Personas
- **Marta** — `admin_organizacao` da Acme (cria, edita, exclui cupons).
- **Carlos** — `panel_user` da Acme (só lista cupons ativos).
- **Dona** — `master_global` (super-admin, entra em tudo).
- **Zeca** — `panel_user` da Globex (outra organização).

### Fixtures
- `Cupom::factory()`, `User::factory()`, `Tenant::factory()`.
- Estados nomeados: `expirado()`, `esgotado()`, `fixo($centavos)`.

### Fakes
- `Queue::fake()` / `Mail::fake()` / `Notification::fake()` quando pertinente.
- `Log::spy()` para conferir mensagens de recusa.

### Estratégia de DB
- `RefreshDatabase` global no `tests/Pest.php`.

---

## Regra R1 — Código é obrigatório, normalizado e único por organização

> `RQ-02`, `RQ-14` · perfil **completo** · técnica: **EP + normalização**

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O código do cupom é obrigatório, fica em maiúsculas e sem espaços nas bordas, e não se repete dentro da mesma organização

    Cenário: [CT-01] código vazio ou só com espaços é recusado na criação
      Dado que Marta está no painel /app da Acme
      Quando ela tenta criar um cupom com código "   "
      Então a gravação falha
      E o cupom não existe no banco

    Cenário: [CT-02] código com 41 caracteres é recusado
      Dado que Marta está no painel /app da Acme
      Quando ela tenta criar um cupom com código "PROMO10PROMO10PROMO10PROMO10PROMO10PROMO10X"
      Então a gravação falha

    Cenário: [CT-03] código com acento é normalizado para versão sem acento ou recusado
      Dado que Marta está no painel /app da Acme
      Quando ela cria um cupom com código "PROMÇ10"
      Então o cupom gravado tem código sem acento OU a gravação é recusada

    Cenário: [CT-04] duas organizações diferentes podem ter o mesmo código
      Dado que Marta criou o cupom "BLACKFRIDAY" na Acme
      E Zeca é usuário da Globex
      Quando Zeca cria o cupom "BLACKFRIDAY" na Globex
      Então a gravação na Globex é aceita
      E a Acme continua com exatamente 1 cupom "BLACKFRIDAY"

    Esquema do Cenário: [CT-13] normalização de código na criação e na edição
      Dado que Marta criou o cupom "PROMO10" na Acme
      Quando ela <ação> com código "<entrada>"
      Então <resultado>

      Exemplos:
        | ação          | entrada      | resultado                                              |
        | cria um cupom | "  promo10 " | a gravação é recusada por duplicidade                  |
        | cria um cupom | "PROMO 10"   | o cupom gravado é "PROMO 10"                           |
        | edita o cupom | "  PROMO10 " | a edição é aceita e o cupom continua "PROMO10"         |
        | edita o cupom | "PROMO20"    | a edição é aceita e o cupom passa a ser "PROMO20"      |
        | edita o cupom | "  promo20 " | a edição é recusada porque "PROMO20" já existe         |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `unique('codigo')` sem `tenant_id` → código de outra org bloqueia | CT-04 |
| M2 | normalização só na criação, não na edição | CT-13 linha "edita" com espaços |
| M3 | normalização em caixa baixa → `PROMO10` ≠ `promo10` coexistem | CT-13 |
| M4 | `mb_strtoupper` não aplica → acentos geram códigos distintos | CT-03 |
| M5 | `trim` não aplica → `" PROMO10"` vira cupom diferente | CT-13, CT-24, CT-51, CT-53 |

---

## Regra R2 — Tipo só aceita `porcentagem` ou `valor fixo`

> `RQ-03` · perfil **completo** · técnica: **EP**

```gherkin
  Regra: O tipo do cupom só pode ser `porcentagem` ou `valor fixo`

    Cenário: [CT-05] tipo inválido é recusado
      Dado que Marta está no painel /app da Acme
      Quando ela tenta criar um cupom com tipo "desconto_direto"
      Então a gravação falha

    Esquema do Cenário: [CT-07] tipo e valor na criação e na edição
      Dado que Marta <estado>
      Quando ela <ação> com tipo "<tipo>" e valor <valor>
      Então <resultado>

      Exemplos:
        | estado                        | ação          | tipo        | valor | resultado                                          |
        | está no painel /app da Acme   | cria um cupom | porcentagem | 10    | o cupom é gravado com tipo porcentagem e valor 10  |
        | está no painel /app da Acme   | cria um cupom | fixo        | 1000  | o cupom é gravado com tipo fixo e valor 1000       |
        | tem um cupom do tipo fixo     | edita o cupom | porcentagem | 50    | a edição é aceita e o cupom passa a ser porcentagem |
        | tem um cupom do tipo fixo     | edita o cupom | fixo        | 1000  | a edição é aceita e o valor continua em centavos   |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6 | validação do tipo só existe no `create`, não no `save` | CT-07 linha "edita" com tipo inválido |
| M7 | terceiro tipo é aceito silenciosamente | CT-05 |

---

## Regra R3 — Valor é `unsignedInteger`, com fronteiras condicionadas ao tipo

> `RQ-04` · perfil **completo** · técnica: **BVA 3-valores + domínio condicionado**

```gherkin
  Regra: O valor do desconto respeita o tipo: porcentagem de 1 a 100; fixo em centavos, positivo

    Esquema do Cenário: [CT-06] fronteiras de valor na criação
      Dado que Marta está no painel /app da Acme
      Quando ela cria um cupom do tipo "<tipo>" com valor <valor>
      Então <resultado>

      Exemplos:
        | tipo        | valor | resultado                |
        | porcentagem | 0     | a gravação falha         |
        | porcentagem | 1     | a gravação é aceita      |
        | porcentagem | 100   | a gravação é aceita      |
        | porcentagem | 101   | a gravação falha         |
        | porcentagem | 150   | a gravação falha         |
        | fixo        | 0     | a gravação falha         |
        | fixo        | 1     | a gravação é aceita      |
        | fixo        | -1    | a gravação falha         |

    Cenário: [CT-11] valor percentual acima de 100 é recusado na edição
      Dado que Marta criou um cupom com tipo porcentagem e valor 10
      Quando ela edita o cupom para valor 150
      Então a gravação falha
      E o cupom continua com valor 10

    Cenário: [CT-12] valor fixo negativo é recusado na edição
      Dado que Marta criou um cupom com tipo fixo e valor 1000
      Quando ela edita o cupom para valor -1
      Então a gravação falha
      E o cupom continua com valor 1000

    Esquema do Cenário: [CT-16] valor percentual acima de 100 não pode existir nem ser aplicado
      Dado que um cupom com tipo porcentagem e valor <percentual> foi inserido direto no banco
      Quando o sistema aplica o cupom em um total de 10000 centavos
      Então <resultado>

      Exemplos:
        | percentual | resultado                                             |
        | 101        | a aplicação é recusada OU o desconto limitado a 10000 |
        | 150        | a aplicação é recusada OU o desconto limitado a 10000 |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M8 | teto de 100% não existe | CT-06, CT-11, CT-16 |
| M9 | valor 0 ou negativo aceito | CT-06, CT-11, CT-12 |
| M10 | validação do valor só no `create` | CT-11, CT-12 |

---

## Regra R4 — Validade é futura na criação e borda exata no uso

> `RQ-05`, `RQ-10` · perfil **completo** · técnica: **BVA 3-valores (data/hora)**

```gherkin
  Regra: A validade é futura na criação e a borda é comparada com o instante exato

    Cenário: [CT-09] validade no passado é recusada na criação
      Dado que o instante atual é 15/08/2026 12:00:00
      Quando Marta cria um cupom com expira_em "15/08/2026 11:59:59"
      Então a gravação falha

    Esquema do Cenário: [CT-27] borda exata da validade na aplicação
      Dado que o instante atual é <agora>
      E existe um cupom ativo com expira_em "15/08/2026 12:00:00" e limite 10 usos
      Quando o cupom é aplicado em um total de 10000 centavos
      Então <resultado>

      Exemplos:
        | agora                   | resultado                                               |
        | 15/08/2026 11:59:59     | a aplicação é aceita e o desconto é concedido           |
        | 15/08/2026 12:00:00     | a aplicação é recusada (cupom expirado)                 |
        | 15/08/2026 12:00:01     | a aplicação é recusada (cupom expirado)                 |

    Esquema do Cenário: [CT-57] validade no passado recusada por fora da tela
      Dado que um cupom com expira_em "15/08/2026 11:59:59" foi inserido direto no banco
      Quando o sistema aplica o cupom em um total de 10000 centavos
      Então <resultado>

      Exemplos:
        | agora                   | resultado                                  |
        | 15/08/2026 12:00:00     | a aplicação é recusada                     |
        | 15/08/2026 11:59:58     | a aplicação é recusada                     |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11 | `expira_em > now()` usa `<` em vez de `<=` → cupom morre 1 dia antes | CT-27 (borda exata) |
| M12 | validação de data futura só no formulário; inserção direta aceita | CT-57 |
| M13 | comparação `expira_em > now()` ignora hora/minuto/segundo | CT-27 (instante) |

---

## Regra R5 — Limite de usos é ≥1 e a borda é inclusiva

> `RQ-06`, `RQ-11` · perfil **completo** · técnica: **BVA 3-valores**

```gherkin
  Regra: O limite de usos é pelo menos 1 e o cupom aceita o último uso

    Cenário: [CT-10] limite de usos menor que 1 é recusado
      Dado que Marta está no painel /app da Acme
      Quando ela cria um cupom com limite_de_usos 0
      Então a gravação falha

    Esquema do Cenário: [CT-30] borda do limite de usos na aplicação
      Dado que existe um cupom com limite <limite> usos e <ja_usado> usos já feitos
      Quando o cupom é aplicado em um total de 10000 centavos
      Então <resultado>

      Exemplos:
        | limite | ja_usado | resultado                                  |
        | 3      | 1        | aceito, contador vai para 2                |
        | 3      | 2        | aceito, contador vai para 3                |
        | 3      | 3        | recusado, contador continua 3              |
        | 3      | 4        | recusado, contador continua 4              |

    Cenário: [CT-31] duas aplicações simultâneas disputam o último uso
      Dado que existe um cupom com limite 1 uso e 0 usos feitos
      Quando duas requisições aplicam o cupom ao mesmo tempo
      Então exatamente uma é aceita
      E a trilha de cupom_usos tem exatamente 1 linha
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M14 | limite 0 aceito | CT-10 |
| M15 | `<` em vez de `<=` no limite → permite 1 uso além | CT-30 (linha ja_usado=3, limite=3) |
| M16 | duas requisições simultâneas ultrapassam o limite | CT-31 |

---

## Regra R6 — Aplicação recusa cupom inexistente, expirado ou esgotado

> `RQ-09`, `RQ-10`, `RQ-11` · perfil **completo** · técnica: **tabela de decisão**

```gherkin
  Regra: O sistema recusa a aplicação de cupom inexistente, expirado ou esgotado

    Esquema do Cenário: [CT-25] condições de recusa na aplicação
      Dado <condicao>
      Quando o cupom "<codigo>" é aplicado em um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom não muda

      Exemplos:
        | condicao                                              | codigo      |
        | que o cupom "PROMO10" não existe na Acme              | PROMO10     |
        | que o cupom "PROMO10" está vencido                    | PROMO10     |
        | que o cupom "PROMO10" esgotou o limite de usos        | PROMO10     |

    Cenário: [CT-26] aplicar cupom de outra organização é recusado
      Dado que existe um cupom "PROMO10" na Globex
      E Zeca é usuário da Acme
      Quando Zeca aplica "PROMO10" na Acme
      Então a aplicação é recusada

    Cenário: [CT-28] aplicar cupom com limite excedido direto no banco é recusado
      Dado que um cupom com limite 1 e usos 1 foi inserido direto no banco
      Quando o cupom é aplicado em um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos continua 1

    Cenário: [CT-29] aplicar cupom vencido direto no banco é recusado
      Dado que um cupom com expira_em no passado foi inserido direto no banco
      Quando o cupom é aplicado em um total de 10000 centavos
      Então a aplicação é recusada
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M17 | cupom de outro tenant é encontrado | CT-26 |
| M18 | limite excedido não é verificado na aplicação | CT-28 |
| M19 | validade não é verificada na aplicação | CT-29 |
| M20 | contador é incrementado mesmo na recusa | CT-25, CT-28, CT-29, CT-37 |

---

## Regra R7 — Desconto percentual nunca excede o total; fixo limita em zero

> `RQ-12` · perfil **completo** · técnica: **BVA / oráculo exato**

```gherkin
  Regra: O desconto percentual é limitado ao total; o fixo limita o final em zero

    Esquema do Cenário: [CT-32] desconto percentual na borda de 100%
      Dado um cupom ativo do tipo porcentagem com valor <percentual>
      Quando o cupom é aplicado em um total de <total> centavos
      Então o total devolvido é <final> centavos

      Exemplos:
        | percentual | total | final  |
        | 100        | 5000  | 0      |
        | 101        | 5000  | 0      |
        | 150        | 10000 | 0      |

    Esquema do Cenário: [CT-33] precisão do desconto percentual
      Dado um cupom ativo do tipo porcentagem com valor <percentual>
      Quando o cupom é aplicado em um total de 10000 centavos
      Então o total devolvido é <final> centavos
      E o desconto registrado na trilha é <desconto> centavos

      Exemplos:
        | percentual | final | desconto |
        | 29         | 7100  | 2900     |
        | 1          | 9900  | 100      |
        | 50         | 5000  | 5000     |
        | 33         | 6700  | 3300     |

    Cenário: [CT-34] desconto fixo maior que o total limita em zero
      Dado um cupom ativo do tipo fixo com valor 5000 centavos
      Quando o cupom é aplicado em um total de 3000 centavos
      Então o total devolvido é 0 centavos
      E o desconto registrado na trilha é 3000 centavos

    Esquema do Cenário: [CT-56] percentual acima de 100 ou fixo negativo não passam
      Dado que um cupom com tipo "<tipo>" e valor <valor> foi inserido direto no banco
      Quando o cupom é aplicado em um total de 10000 centavos
      Então <resultado>

      Exemplos:
        | tipo        | valor | resultado                                           |
        | porcentagem | 150   | a aplicação é recusada OU o total devolvido é 0     |
        | fixo        | -1    | a aplicação é recusada                              |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M21 | percentual > 100 gera desconto maior que o total | CT-32, CT-56 |
| M22 | fixo maior que o total gera total negativo | CT-34 |
| M23 | arredondamento percentual em `float` perde centavo | CT-33 (29%) |
| M24 | truncamento errado: arredonda para cima em vez de para baixo | CT-33 (29%) |

---

## Regra R8 — Uso bem-sucedido consome exatamente um uso e grava trilha

> `RQ-13`, `RQ-15` · perfil **completo** · técnica: **rastreio de efeito**

```gherkin
  Regra: A aplicação bem-sucedida consome exatamente um uso e grava a trilha

    Cenário: [CT-35] aplicação grava quem e quando
      Dado um cupom ativo com limite 10 usos e 0 usos feitos
      Quando o cupom é aplicado por Carlos em um total de 5000 centavos
      Então o contador de usos do cupom é 1
      E a trilha cupom_usos tem 1 linha atribuída a Carlos
      E a trilha registra o instante da aplicação
      E a trilha registra o valor original 5000 e o desconto aplicado

    Esquema do Cenário: [CT-36] consumo de uso para diferentes tipos e totais
      Dado um cupom ativo do tipo "<tipo>" com valor <valor> e limite <limite> usos
      Quando o cupom é aplicado em um total de 10000 centavos
      Então o contador de usos do cupom é <usos_apos>
      E a trilha tem <usos_apos> linha(s)

      Exemplos:
        | tipo        | valor | limite | usos_apos |
        | porcentagem | 10    | 10     | 1         |
        | fixo        | 1000  | 10     | 1         |

    Cenário: [CT-37] cupom inválido não consome uso nem gera trilha
      Dado um cupom esgotado com 1 uso de limite 1
      Quando o cupom é aplicado em um total de 10000 centavos
      Então a aplicação é recusada
      E o contador de usos do cupom continua 1
      E a trilha do cupom continua com 1 linha
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M25 | contador incrementado **antes** da validação → cupom inválido consome uso | CT-37 |
| M26 | contador **não** incrementado no sucesso | CT-35, CT-36 |
| M27 | trilha grava o usuário autenticado no request em vez de quem aplicou | CT-35, CT-49 |
| M28 | trilha não grava o valor original/desconto | CT-35, CT-36 |

---

## Regra R9 — Usuário comum só lista cupons ativos

> `RQ-08` · perfil **padrão** · técnica: **matriz papel × ação**

```gherkin
  Regra: O usuário comum do painel /app só vê cupons ativos

    Cenário: [CT-20] usuário comum vê apenas ativos
      Dado que existem os cupons: ATIVO (válido, com uso), VENCIDO (expirado), CHEIO (esgotado), VENCIDO_E_CHEIO (expirado e esgotado)
      Quando Carlos acessa a listagem de cupons no /app da Acme
      Então o cupom ATIVO aparece na lista
      E os cupons VENCIDO, CHEIO e VENCIDO_E_CHEIO não aparecem na lista

    Cenário: [CT-21] admin vê todos os cupons
      Dado que existem os cupons: ATIVO, VENCIDO, CHEIO
      Quando Marta acessa a listagem de cupons no /app da Acme
      Então a lista tem 3 registros

    Cenário: [CT-22] usuário de outra organização não vê cupons da Acme
      Dado que existe o cupom "PROMO10" na Acme
      Quando Zeca acessa a listagem de cupons na Globex
      Então a lista da Globex não contém "PROMO10"

    Cenário: [CT-23] convite sem painel não acessa a rota
      Dado que existe um cupom ativo na Acme
      Quando um usuário anônimo acessa /app/{tenant}/cupons
      Então a resposta é 302 para login ou 403
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M29 | `panel_user` vê cupons expirados/inativos | CT-20 |
| M30 | escopo de tenant não aplica na listagem | CT-22 |
| M31 | rota de listagem não exige autenticação | CT-23 |

---

## Regra R10 — Só admin cria, edita e exclui

> `RQ-07` · perfil **completo** · técnica: **matriz papel × ação**

```gherkin
  Regra: Só quem tem permissão de escrita pode criar, editar e excluir cupons

    Esquema do Cenário: [CT-41] operações de escrita por persona
      Dado que existe um cupom "PROMO10" na Acme
      Quando <ator> tenta <operacao>
      Então <resultado>

      Exemplos:
        | ator            | operacao              | resultado                                  |
        | Carlos          | editar o cupom        | a operação é recusada com 403              |
        | Carlos          | excluir o cupom       | a operação é recusada com 403              |
        | Marta           | editar o cupom        | a edição é aceita                          |
        | Marta           | excluir o cupom       | a exclusão é aceita                        |
        | Dona            | excluir o cupom       | a exclusão é aceita                        |

    Cenário: [CT-42] usuário comum não consegue criar cupom por fora do formulário
      Dado que Carlos está autenticado na Acme
      Quando ele faz um POST direto para /app/{tenant}/cupons com dados válidos
      Então a resposta é 403
      E nenhum cupom é criado

    Cenário: [CT-43] usuário comum não edita cupom por fora do formulário
      Dado que existe o cupom "PROMO10" na Acme
      E Carlos está autenticado
      Quando ele faz um PUT/PATCH direto para a rota de edição com valor 9999
      Então a resposta é 403
      E o cupom continua com o valor original
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M32 | policy aplicada só no Filament; request direto passa | CT-42, CT-43 |
| M33 | `panel_user` tem `Update:Cupom` | CT-41 linha Carlos/editar |

---

## Regra R11 — Concorrência não furra o limite de usos

> `RQ-11`, `RQ-13` · perfil **completo** · técnica: **heurística de race**

```gherkin
  Regra: Duas aplicações simultâneas não ultrapassam o limite de usos

    Cenário: [CT-05] concorrência pelo último uso
      Dado que existe um cupom com limite 1 uso e 0 usos feitos
      Quando duas requisições aplicam o cupom simultaneamente
      Então exatamente uma é aceita
      E o contador final é 1
      E a trilha tem exatamente 1 linha

    Cenário: [CT-31] disputa pelo último uso com total maior
      Dado que existe um cupom com limite 1 uso e 0 usos feitos
      Quando duas requisições aplicam o cupom a totais de 10000 e 5000 centavos
      Então exatamente uma é aceita
      E a outra é recusada
      E a trilha tem exatamente 1 linha
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M34 | leitura-soma-gravação em vez de UPDATE atômico | CT-05, CT-31 |

---

## Regra R12 — Trilha de auditoria registra quem e quando

> `RQ-15` · perfil **padrão** · técnica: **rastreio de efeito**

```gherkin
  Regra: A trilha de uso registra quem aplicou, quando e os valores

    Cenário: [CT-38] trilha sobrevive à alteração do cupom
      Dado um cupom com 1 uso gravado
      Quando Marta edita o valor do cupom
      Então a trilha do cupom continua com a linha original

    Cenário: [CT-39] trilha registra o usuário que aplicou, não o dono do request
      Dado um cupom ativo
      Quando o sistema aplica o cupom em nome de Carlos
      Então a linha da trilha está atribuída a Carlos

    Cenário: [CT-40] trilha registra instante e valores corretos
      Dado um cupom ativo do tipo fixo com valor 1000 centavos
      Quando o cupom é aplicado em um total de 5000 centavos
      Então a trilha registra valor_original 5000, valor_desconto 1000, e created_at no instante da aplicação

    Cenário: [CT-49] trilha não nasce com usuário nulo quando há aplicador
      Dado um cupom ativo
      Quando o cupom é aplicado por um usuário autenticado
      Então aplicado_por_id na trilha não é nulo
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M35 | trilha fica com aplicado_por_id nulo | CT-39, CT-49 |
| M36 | trilha grava o usuário errado | CT-39 |
| M37 | trilha não registra o instante | CT-40 |

---

## Cenários de lacuna declarada

```gherkin
  Cenário: [CT-58] idempotência no agregado Pedido
      Dado que a entidade Pedido não existe neste escopo
      Quando o mesmo cupom é aplicado duas vezes ao mesmo identificador de pedido
      Então o cenário não pode ser ancorado no agregado Pedido
      E é registrado como lacuna declarada (D18)

  Cenário: [CT-59] timezone do app vs banco
      Dado que o app está configurado em UTC
      Quando tentamos configurar o app em America/Sao_Paulo e o banco em UTC
      Então o arnês não consegue produzir uma diferença observável na trilha
      E é registrado como lacuna declarada (D14)

  Cenário: [CT-60] exclusão lógica / soft-delete
      Dado que o mecanismo de exclusão é físico
      Quando um cupom é "desativado" por exclusão lógica
      Então o cenário não se aplica ao mecanismo assumido
      E é registrado como lacuna declarada (D15)
```

## Checklist de Taxonomia

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | CT-26, CT-42, CT-43 |
| Autorização exercida na ação (não só `can()`) | CT-42, CT-43 |
| Idempotência (ancorada no agregado) | CT-58 — lacuna declarada (Pedido fora de escopo) |
| Concorrência | CT-05, CT-31 |
| Fronteira no ponto de entrada (gravação) | CT-06, CT-09, CT-10, CT-11, CT-12, CT-57 |
| Domínio condicionado (tipo × valor) | CT-06, CT-07, CT-11, CT-12, CT-16, CT-32, CT-56 |
| Estado × operação de escrita (excluído ainda funciona?) | CT-60 — lacuna declarada (mecanismo físico) |
| Ausente ≠ null ≠ vazio | CT-01, CT-13, CT-24, CT-51, CT-53 |
| Paginação / ordenação | CT-20, CT-21 |
| Timezone / DST | CT-59 — lacuna declarada |
| Unicode / limite de varchar | CT-02, CT-03, CT-13, CT-17 |
| Unicidade + soft delete | CT-60 — lacuna declarada |
| CRUD combinado | CT-41, CT-42, CT-43 |
| Mass assignment | — (não se aplica: campos de controle fora do fillable) |
| Precisão monetária | CT-33, CT-34 |

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | código vazio/space | R1 | EP | Livewire | CupomCrudTest | M2, M5 |
| CT-02 | código muito longo | R1 | BVA | Livewire | CupomCrudTest | — |
| CT-03 | acento no código | R1 | EP | Feature | CupomCrudTest | M4 |
| CT-04 | unicidade por tenant | R1 | EP | Feature | CupomTenancyTest | M1 |
| CT-05 | concorrência no último uso | R11 | race | Feature | CupomTest | M16, M34 |
| CT-06 | fronteiras de valor na criação | R3 | BVA 3-valores | Livewire | CupomCrudTest | M8, M9 |
| CT-07 | tipo e valor na edição | R2/R3 | EP + BVA | Livewire | CupomCrudTest | M6, M7, M10 |
| CT-08 | valor mínimo aceito | R3 | BVA | Livewire | CupomCrudTest | — |
| CT-09 | validade no passado recusada | R4 | BVA | Livewire | CupomCrudTest | M12 |
| CT-10 | limite < 1 recusado | R5 | BVA | Livewire | CupomCrudTest | M14 |
| CT-11 | percentual > 100 na edição | R3 | BVA | Livewire | CupomCrudTest | M8, M10 |
| CT-12 | fixo negativo na edição | R3 | BVA | Livewire | CupomCrudTest | M9, M10 |
| CT-13 | normalização na criação e edição | R1 | normalização | Feature | CupomTenancyTest | M2, M3, M5 |
| CT-16 | percentual > 100 inserido direto | R3 | BVA | Feature | CupomTest | M21 |
| CT-20 | usuário comum só vê ativos | R9 | matriz | Feature | CupomTest | M29 |
| CT-21 | admin vê todos | R9 | matriz | Feature | CupomTest | — |
| CT-22 | isolamento por tenant na listagem | R9 | IDOR | Feature | CupomTenancyTest | M30 |
| CT-23 | anônimo não acessa listagem | R9 | autorização | Feature | CupomTest | M31 |
| CT-24 | código com espaços é recusado | R1 | normalização | Feature | CupomTest | M5 |
| CT-25 | recusas: inexistente/vencido/esgotado | R6 | tabela de decisão | Feature | CupomTest | M17, M18, M19, M20 |
| CT-26 | cupom de outra org não é encontrado | R6 | IDOR | Feature | CupomTenancyTest | M17 |
| CT-27 | borda exata da validade | R4 | BVA 3-valores | Feature | CupomTest | M11, M13 |
| CT-28 | limite excedido direto no banco | R6 | BVA | Feature | CupomTest | M18 |
| CT-29 | vencido direto no banco | R6 | BVA | Feature | CupomTest | M19 |
| CT-30 | borda do limite de usos | R5 | BVA 3-valores | Feature | CupomTest | M15 |
| CT-31 | duas requisições disputam último uso | R11 | race | Feature | CupomTest | M34 |
| CT-32 | percentual acima de 100 | R7 | BVA | Feature | CupomTest | M21 |
| CT-33 | precisão do percentual | R7 | oráculo exato | Unit | CupomTest | M23, M24 |
| CT-34 | fixo maior que o total | R7 | BVA | Feature | CupomTest | M22 |
| CT-35 | aplicação grava quem e quando | R8/R12 | rastreio de efeito | Feature | CupomTest | M26, M27, M28, M35, M36, M37 |
| CT-36 | consumo para tipos e totais | R8 | rastreio | Feature | CupomTest | M26 |
| CT-37 | cupom inválido não consome uso | R8 | tabela de decisão | Feature | CupomTest | M25, M27 |
| CT-38 | trilha sobrevive à edição do cupom | R12 | rastreio | Feature | CupomTest | — |
| CT-39 | trilha registra o usuário correto | R12 | rastreio | Feature | CupomTest | M27, M36 |
| CT-40 | trilha registra instante e valores | R12 | rastreio | Feature | CupomTest | M37 |
| CT-41 | operações de escrita por persona | R10 | matriz | Livewire | CupomCrudTest | M32, M33 |
| CT-42 | POST direto recusado | R10 | autorização | Feature | CupomTest | M32 |
| CT-43 | PUT/PATCH direto recusado | R10 | autorização | Feature | CupomTest | M32 |
| CT-49 | aplicado_por_id não é nulo | R12 | rastreio | Feature | CupomTest | M35 |
| CT-51 | código com espaço no início | R1 | normalização | Feature | CupomTest | M5 |
| CT-52 | listagem sem itens inativos | R9 | matriz | Feature | CupomTest | M29 |
| CT-53 | código com espaço no fim | R1 | normalização | Feature | CupomTest | M5 |
| CT-56 | percentual/fixo inválido inserido direto | R3/R7 | BVA | Feature | CupomTest | M21, M22 |
| CT-57 | validade no passado inserida direto | R4 | BVA | Feature | CupomTest | M12 |
| CT-58 | idempotência no Pedido | — | — | — | — | D18 — lacuna declarada |
| CT-59 | timezone do app vs banco | — | — | — | — | D14 — lacuna declarada |
| CT-60 | exclusão lógica | — | — | — | — | D15 — lacuna declarada |
# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Runtime: `pest-plugin-browser` (Playwright). O plugin sobe o próprio servidor.  
> Comando: `vendor/bin/pest --testsuite=Browser` (em série — nunca `--parallel`)

## Pré-requisitos

- [ ] `npm run build` executado
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por `$this->actingAs($user)`

## Seletores

| Elemento | Seletor | Já existe? |
|---|---|---|
| Select de tipo | `select[name="data.tipo"]` | — |
| Campo valor | `input[name="data.valor"]` | — |
| Rótulo do campo valor | `label[for="data.valor"]` | — |
| Botão Salvar | `button[type="submit"]` | — |

---

## CT-B01 — O rótulo/sufixo do campo `valor` muda conforme o tipo

**Por que browser e não Livewire**: a asserção depende do DOM atualizado por JS após o `Select ->live()`; o HTML inicial é idêntico para os dois tipos.

```gherkin
# language: pt
  Cenário: [CT-B01] criar cupom percentual e depois fixo
    Dado que Marta está autenticada no /app da Acme
    Quando ela visita /app/{tenant}/cupons/create
    E escolhe "Valor fixo" no Select de tipo
    Então o rótulo do campo valor contém "centavos"
    E o campo valor não aceita um valor acima de 999.999

    Quando ela escolhe "Porcentagem" no Select de tipo
    Então o rótulo do campo valor contém "Percentual"
    E o campo valor não aceita o valor 101
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | abrir create | `visit('/app/acme/cupons/create')` | formulário carrega |
| 2 | escolher fixo | `->select('data.tipo', 'fixo')` | label mostra "Valor do desconto (centavos)" |
| 3 | escolher porcentagem | `->select('data.tipo', 'porcentagem')` | label mostra "Percentual de desconto" |
| 4 | tentar 101 | `->type('data.valor', '101')->press('Salvar')` | mensagem de validação de máximo |

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M38 | `->live()` não aplicado → rótulo não muda | CT-B01 |
| M39 | validação de máximo 100% só no backend | CT-B01 linha 4 |

---

## CT-B02 — Usuário comum só vê cupons ativos na listagem

**Por que browser e não Livewire**: a asserção é sobre a renderização da tabela com filtro implícito de escopo, dependendo do estado do usuário logado no navegador.

```gherkin
# language: pt
  Cenário: [CT-B02] panel_user não vê cupons vencidos/esgotados
    Dado que existem os cupons: ATIVO, VENCIDO, CHEIO
    E Carlos está autenticado no /app da Acme
    Quando ele visita /app/{tenant}/cupons
    Então ele vê "ATIVO" na listagem
    E não vê "VENCIDO" na listagem
    E não vê "CHEIO" na listagem
    E não vê o botão "Novo cupom"
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | actingAs(Carlos) | `$this->actingAs(Carlos)` | autenticado |
| 2 | visitar listagem | `visit('/app/acme/cupons')` | tabela carrega |
| 3 | ver conteúdo | `->assertSee('ATIVO')` | ATIVO aparece |
| 4 | ver ausência | `->assertDontSee('VENCIDO')` | VENCIDO não aparece |
| 5 | ver botão ausente | `->assertDontSee('Novo cupom')` | sem permissão de criação |

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M40 | `getEloquentQuery()` não aplica `ativos()` para panel_user | CT-B02 |
| M41 | botão de criação visível para panel_user | CT-B02 |

---

## Roteiro de Validação: Desenhado × Implementado

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | Select de tipo com `->live()` | a implementar | — | — |
| 2 | Rótulo muda com o tipo | a implementar | — | — |
| 3 | panel_user só vê ativos | a implementar | — | — |
