# Casos de Teste — FERRO-812: Cupons de desconto

> Gerado pela skill `feature-test-design` v1.9.0 a partir do `00-requisito.md`.
> O `01-plano-acao.md` entra apenas para paths e superfície de UI.

## Perfil de esforço por risco

| Área | Probabilidade | Impacto | Perfil |
|---|---|---|---|
| Cálculo de desconto | 3 | 3 | completo |
| Validação de cadastro | 2 | 3 | completo |
| Concorrência / limite de usos | 3 | 3 | completo |
| Autorização e listagem | 2 | 3 | padrão |
| Auditoria de uso | 2 | 2 | padrão |
| Normalização de código | 2 | 2 | padrão |

## SFDIPOT

| Dimensão | O que existe | Vazio? |
|---|---|---|
| Structure | `Cupom`, `CupomUso`, `CupomResource`, `PapeisSeeder`, `config/logging.php` | — |
| Function | CRUD, cálculo de desconto, consumo atômico, listagem com escopo, auditoria | — |
| Data | código (`string` 40), tipo (`enum`), valor (`unsignedInteger`), expira_em (`timestamp`), limite/usos, trilha de uso | — |
| Interfaces | Filament painel `/app`, método `Cupom::aplicarEm()` chamável por código | — |
| Platform | PHP 8.3+, Laravel 13, Filament 5, Pest 5, SQLite em teste, `APP_TIMEZONE=UTC` | — |
| Operations | admin cadastra; panel_user lista ativos; chamadores consomem cupom | — |
| Time | expira_em, contador atômico, timezone como contexto do teste | Parcial: DST não aplica |

## Mapa de Regras

| Regra | RQs | Técnica |
|---|---|---|
| R1 — Criação de cupom exige campos válidos | RQ-01 a RQ-06 | EP + BVA |
| R2 — Código é normalizado e único por organização | RQ-02, RQ-14 | Normalização + EP |
| R3 — Valor obedece limites por tipo | RQ-03, RQ-04 | BVA + tabela de decisão |
| R4 — Validade futura no cadastro | RQ-05 | BVA 3-valores |
| R5 — Só admin cria/edita/exclui | RQ-07 | Matriz papel × ação |
| R6 — Usuário comum só vê cupons ativos | RQ-08 | Matriz estado × visibilidade |
| R7 — Aplicação recusa cupom inexistente, expirado ou esgotado | RQ-09 a RQ-11 | Tabela de decisão |
| R8 — Aplicação calcula e limita desconto | RQ-12 | BVA + aritmética exata |
| R9 — Consumo incrementa contador e trilha atômica | RQ-13, RQ-15 | Rastreio de efeito + concorrência |

## Fronteira com o Plano

- Nome de método `valido()`, `aplicarEm()`, `descontoSobre()` vem do PRD e é **detalhe de cenário**, não oráculo.
- Unidade de `valor` (centavos/pontos percentuais) e truncamento vêm das premissas P-05 e P-06 do `00` — são oráculo.
- O agregado `Pedido` está fora de escopo (P-01); idempotência de reaplicação no mesmo pedido não é ancorável → **lacuna declarada L-05**.
- Mecanismo de exclusão é físico (P-?? no 01) → cupom desativado/soft-deleted fora do arnês → **lacuna declarada L-04**.
- `config('app.timezone')` é `UTC` no projeto; teste de fuso só é falsificável com arnês de timezone configurável → **lacuna declarada L-03**.

---

## Cenários

### Funcionalidade: cadastro de cupom

#### Regra: R1 — Criação de cupom exige campos válidos

```gherkin
@CT-01 @frontend
Cenário: criação de cupom com dados mínimos válidos
  Dado um usuário logado como admin no painel /app
  Quando ele acessa "/app/cupons/create"
    E preenche "codigo" com "PROMO10"
    E preenche "tipo" com "porcentagem"
    E preenche "valor" com "10"
    E preenche "expira_em" com "2030-01-01 12:00:00"
    E preenche "limite_de_usos" com "100"
    E confirma a gravação
  Então a resposta é 200
    E o banco contém um cupom com codigo "PROMO10", tipo "porcentagem", valor 10, expira_em "2030-01-01 12:00:00" e limite_de_usos 100
    E o campo "usos" do cupom é 0
```

#### Regra: R3 — Valor obedece limites por tipo

```gherkin
@CT-02 @backend @BVA
Esquema do Cenário: valor fora do domínio é recusado na criação
  Dado um admin autenticado
  Quando ele chama o cadastro de cupom com tipo <tipo>, valor <valor>, expira_em futura e limite 1
  Então a gravação falha
    E o banco NÃO contém um cupom com codigo <codigo>

  Exemplos:
    | CT  | tipo         | valor | codigo   | nota                                 |
    | 02a | porcentagem  | 0     | ZERO-PCT | D11: valor 0 recusado                |
    | 02b | porcentagem  | 101   | ACIMA100 | D01: percentual acima de 100 recusado |
    | 02c | porcentagem  | -5    | NEG-PCT  | D11: valor negativo recusado         |
    | 02d | fixo         | 0     | ZERO-FIX | D11: valor 0 recusado                |
    | 02e | fixo         | -100  | NEG-FIX  | D11: valor negativo recusado         |
```

```gherkin
@CT-03 @backend @BVA
Esquema do Cenário: percentual nas fronteiras é aceito
  Dado um admin autenticado
  Quando ele cadastra um cupom "<codigo>" do tipo "porcentagem" com valor <valor>
  Então a gravação é aceita
    E o cupom gravado tem valor <valor>

  Exemplos:
    | CT  | codigo | valor | nota                   |
    | 03a | PCT-1  | 1     | menor percentual válido |
    | 03b | PCT-99 | 99    | um abaixo de 100       |
    | 03c | PCT-100| 100   | percentual máximo      |
```

#### Regra: R4 — Validade futura no cadastro

```gherkin
@CT-04 @backend @BVA-3-valores
Esquema do Cenário: validade na fronteira do instante atual é recusada ou aceita
  Dado o relógio congelado em "2026-08-15 12:00:00"
    E um admin autenticado
  Quando ele tenta cadastrar um cupom com expira_em "<expira_em>"
  Então <resultado>

  Exemplos:
    | CT  | expira_em           | resultado                                       | nota |
    | 04a | 2026-08-15 11:59:59 | a gravação falha                                | D12: no passado |
    | 04b | 2026-08-15 12:00:00 | a gravação falha                                | D12: agora (off-by-one) |
    | 04c | 2026-08-15 12:00:01 | a gravação é aceita e expira_em é o informado   | um segundo depois |
```

> CT-04b detecta D03: se `expira_em > now()` for implementado com `>=`, a gravação de um cupom com expira_em igual ao instante atual passaria, e o CT-04b falharia.

#### Regra: R2 — Código é normalizado e único por organização

```gherkin
@CT-05 @backend @normalizacao
Cenário: código com espaços e caixa é normalizado
  Dado uma organização "Acme" com um cupom "PROMO10" já cadastrado
  Quando um admin cadastra um cupom com codigo " promo10 
  Então a gravação falha
    E o banco continua com exatamente 1 cupom com codigo "PROMO10" na Acme
```

> Detecta D05 (case-sensitive) e D17 (espaços não normalizados). Se a implementação não fizer `mb_strtoupper(trim($codigo))`, " promo10 " passaria como outro cupom.

```gherkin
@CT-06 @backend @tenancy
Cenário: unicidade do código é por organização
  Dado a organização "Acme" com cupom "BLACKFRIDAY"
    E a organização "Globex" sem cupons
  Quando um admin da Globex cadastra um cupom "BLACKFRIDAY"
  Então a gravação é aceita
    E a Globex tem exatamente 1 cupom "BLACKFRIDAY"
    E a Acme continua com 1 cupom "BLACKFRIDAY"
```

> Detecta vazamento de unicidade global. Se `unique` for usado sem tenant, o cadastro na Globex falha.

```gherkin
@CT-07 @backend
Cenário: edição mantém unicidade contra si mesma
  Dado um cupom "PROMO10" na Acme
  Quando o admin edita o cupom sem alterar o codigo
  Então a gravação é aceita
    E o banco continua com 1 cupom "PROMO10" na Acme
```

> Detecta edição ingênua que acusa colisão do registro com ele próprio.

### Funcionalidade: aplicação do cupom

#### Regra: R7 — Aplicação recusa cupom inexistente, expirado ou esgotado

```gherkin
@CT-08 @backend @BVA-3-valores
Esquema do Cenário: validade na fronteira muda o resultado
  Dado o relógio congelado em "2026-08-15 12:00:00"
    E um cupom "PROMO10" de porcentagem 10%, limite 1 e expira_em "<expira_em>"
  Quando se aplica o cupom em um total de 10.000 centavos
  Então <resultado>

  Exemplos:
    | CT  | expira_em           | resultado                                         | nota |
    | 08a | 2026-08-15 11:59:59 | a aplicação é recusada                            | D03: expirado (off-by-one) |
    | 08b | 2026-08-15 12:00:00 | a aplicação é recusada                            | D03: exatamente agora |
    | 08c | 2026-08-15 12:00:01 | a aplicação é aceita e o total devolvido é 9.000  | D03: válido por 1s |
```

> Detecta D03 off-by-one. Se `expira_em > now()` for `<`, o cupom no instante 12:00:01 seria recusado.

```gherkin
@CT-09 @backend
Esquema do Cenário: limite de usos nas fronteiras
  Dado um cupom "PROMO10" de porcentagem 10% e limite <limite>
    E o cupom já foi usado <usos> vezes
  Quando se aplica o cupom em 10.000 centavos
  Então <resultado>
    E <contador_final>

  Exemplos:
    | CT  | limite | usos | resultado                              | contador_final                  | nota |
    | 09a | 3      | 2    | a aplicação é aceita e total é 9.000   | o contador de usos do cupom é 3 | um abaixo do limite |
    | 09b | 3      | 3    | a aplicação é recusada                 | o contador de usos do cupom é 3 | D04: exatamente no limite |
    | 09c | 3      | 4    | a aplicação é recusada                 | o contador de usos do cupom é 4 | D04: estourado |
```

> Detecta D04 (off-by-one no limite). Se `usos < limite` for `<=`, o uso com `usos == limite` seria aceito.

```gherkin
@CT-10 @backend
Cenário: cupom inexistente é recusado
  Dado nenhum cupom cadastrado
  Quando se aplica o codigo "INEXISTENTE" em 10.000 centavos
  Então a aplicação é recusada
    E nenhuma trilha de uso é criada
```

#### Regra: R8 — Aplicação calcula e limita desconto

```gherkin
@CT-11 @backend @BVA
Esquema do Cenário: cálculo de desconto percentual
  Dado um cupom "<codigo>" de porcentagem <valor>%
  Quando se aplica o cupom em <total> centavos
  Então o total devolvido é <final> centavos
    E o desconto registrado na trilha é <desconto> centavos

  Exemplos:
    | CT   | codigo | valor | total | final | desconto | nota |
    | 11a  | PCT-10 | 10    | 10000 | 9000  | 1000     | divisão exata |
    | 11b  | PCT-29 | 29    | 10000 | 7100  | 2900     | D16: 29% distingue float de inteiro |
    | 11c  | PCT-5  | 5     | 50    | 48    | 2        | D16: resto → truncar vs arredondar |
    | 11d  | PCT-1  | 1     | 10000 | 9900  | 100      | mínimo percentual |
    | 11e  | PCT-50 | 50    | 9999  | 5000  | 4999     | D16: metade com resto |
```

> Detecta D16 (percentual em float perde centavo). 29% de 10000 = 2900 em inteiro, 2899 em `floor(float)`. 5% de 50 = 2 em `intdiv(50*5,100)` (250/100=2), mas 2.5 em float.

```gherkin
@CT-12 @backend
Esquema do Cenário: cálculo de desconto fixo e piso zero
  Dado um cupom "<codigo>" de valor fixo <valor> centavos
  Quando se aplica o cupom em <total> centavos
  Então o total devolvido é <final> centavos
    E o desconto registrado na trilha é <desconto> centavos

  Exemplos:
    | CT  | codigo | valor | total | final | desconto | nota |
    | 12a | FIX-10 | 1000  | 5000  | 4000  | 1000     | caminho feliz |
    | 12b | FIX-50 | 5000  | 3000  | 0     | 3000     | D02: desconto maior que total zera |
    | 12c | FIX-1  | 1     | 100   | 99    | 1        | mínimo fixo |
```

> Detecta D02 (desconto maior que total resulta em negativo em vez de zero). O oráculo é `max(0, total - desconto)`.

#### Regra: R9 — Consumo incrementa contador e trilha atômica

```gherkin
@CT-13 @backend
Cenário: aplicação bem-sucedida incrementa contador e trilha
  Dado um cupom "PROMO10" de porcentagem 10%, limite 3 e usos 1
    E um usuário "Marina" autenticado
  Quando se aplica o cupom em 10.000 centavos
  Então a aplicação é aceita
    E o total devolvido é 9.000 centavos
    E o contador de usos do cupom é 2
    E a trilha do cupom tem 1 linha, com cupom_id, aplicado_por_id apontando para "Marina" e created_at não nulo
```

> Detecta D07 (contador não incrementa) e D13 (auditoria não grava quem aplicou).

```gherkin
@CT-14 @backend
Cenário: cupom inválido não consome uso nem gera trilha
  Dado um cupom "PROMO10" expirado com limite 1 e usos 0
  Quando se aplica o cupom em 10.000 centavos
  Então a aplicação é recusada
    E o contador de usos do cupom continua 0
    E a trilha do cupom continua vazia
```

> Detecta D06 (contador incrementado antes da validação). Se o contador aumentar antes da validação, após recusa ficaria 1.

```gherkin
@CT-15 @backend @concorrencia
Cenário: duas aplicações simultâneas respeitam o limite
  Dado um cupom "PROMO10" de porcentagem 10% e limite 1
  Quando duas requisições aplicam o cupom em 10.000 centavos ao mesmo tempo
  Então uma aplicação é aceita e devolve 9.000 centavos
    E a outra aplicação é recusada
    E o contador de usos do cupom é exatamente 1
    E a trilha do cupom tem exatamente 1 linha
```

> Detecta D08 (dois pedidos simultâneos estouram limite). O oráculo é `UPDATE ... WHERE usos < limite` atômico.

### Funcionalidade: autorização e listagem

#### Regra: R5 — Só admin cria/edita/exclui

```gherkin
@CT-16 @backend @autorizacao
Esquema do Cenário: ações administrativas requerem permissão
  Dado um usuário "Carlos" com papel "<papel>" no painel /app
    E um cupom "PROMO10" existente
  Quando ele tenta <acao> via requisição direta
  Então <resultado>

  Exemplos:
    | CT   | papel             | acao            | resultado                                   | nota |
    | 16a  | admin_organizacao | criar cupom     | a ação é aceita                             | admin escreve |
    | 16b  | panel_user        | criar cupom     | a ação é recusada com 403                   | D09: usuário comum não cria |
    | 16c  | panel_user        | editar cupom    | a ação é recusada com 403                   | D09: usuário comum não edita |
    | 16d  | panel_user        | excluir cupom   | a ação é recusada com 403                   | D09: usuário comum não exclui |
    | 16e  | master_global     | excluir cupom   | a ação é aceita                             | master_global herda tudo |
```

> Detecta D09 (policy só no form; request direto passa).

#### Regra: R6 — Usuário comum só vê cupons ativos

```gherkin
@CT-17 @backend @listagem
Cenário: listagem filtra cupons ativos para usuário comum
  Dado uma organização com os cupons:
    | codigo  | expira_em           | usos | limite | situacao   |
    | ATIVO   | 2030-01-01 12:00:00 | 0    | 10     | Ativo      |
    | VENCIDO | 2020-01-01 12:00:00 | 0    | 10     | Expirado   |
    | CHEIO   | 2030-01-01 12:00:00 | 10   | 10     | Esgotado   |
  Quando um panel_user lista os cupons
  Então a lista contém 1 registro
    E o cupom "ATIVO" aparece
    E os cupons "VENCIDO" e "CHEIO" não aparecem
```

> Detecta D10 (usuário comum enxerga cupons expirados/inativos).

```gherkin
@CT-18 @backend @listagem
Cenário: admin vê todos os cupons
  Dado os mesmos cupons do CT-17
  Quando um admin_organizacao lista os cupons
  Então a lista contém 3 registros
```

### Funcionalidade: cenários de transformação de estado

#### Regra: R2/R3 — Edição mantém validações

```gherkin
@CT-19 @backend
Cenário: edição para percentual 101 é recusada
  Dado um cupom "PROMO10" do tipo fixo e valor 1.000
  Quando o admin edita o tipo para porcentagem e o valor para 101
  Então a gravação falha
    E o cupom continua do tipo fixo com valor 1.000
```

> Detecta D01 e D11 no ponto de edição.

```gherkin
@CT-20 @backend
Cenário: edição para validade no passado é recusada
  Dado um cupom "PROMO10" com expira_em "2030-01-01 12:00:00"
    E o relógio congelado em "2026-08-15 12:00:00"
  Quando o admin edita a expira_em para "2026-08-14 12:00:00"
  Então a gravação falha
    E o cupom continua com expira_em "2030-01-01 12:00:00"
```

> Detecta D12 no ponto de edição.

### Lacunas declaradas

| ID | Defeito | Motivo |
|---|---|---|
| L-03 | D14 — timezone | `config('app.timezone')` é `UTC` no arnês. Falsificar exige alterar o fuso do app e confrontar o banco, o que o ambiente de teste não permite sem mutar configuração global. |
| L-04 | D15 — soft-delete | O mecanismo de exclusão assumido no plano é físico; não existe coluna `ativo` nem `deleted_at` para cupom. |
| L-05 | D18 — idempotência no pedido | O agregado `Pedido` está fora de escopo (P-01); não é possível aplicar o mesmo cupom duas vezes ao mesmo pedido e ancorar no estado dele. |

---

## Resumo

- **Perfil**: completo para cálculo e validação; padrão para autorização.
- **Técnicas usadas**: BVA 3-valores, EP, tabela de decisão, rastreio de efeito, normalização, matriz papel × ação, concorrência.
- **Cenários backend**: 20 (CT-01 a CT-20).
- **Lacunas declaradas**: 3 (L-03, L-04, L-05).
