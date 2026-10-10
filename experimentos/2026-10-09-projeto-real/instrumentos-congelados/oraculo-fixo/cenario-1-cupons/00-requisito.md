# Requisito — FERRO-812: Cupons de desconto

## Fonte

- **Origem**: card **FERRO-812**, colado verbatim no chat pelo usuário ao invocar a skill `feature-wiki`
- **Data**: 2026-08-14
- **Autor / solicitante**: não declarado no card — o texto chegou pelo usuário do kit, sem assinatura
  de área de negócio
- **Fidelidade**: **alta** — texto escrito, transcrito abaixo sem alteração

## Texto Original

<!-- IMUTÁVEL. Não editar, não corrigir ortografia, não resumir, não reordenar. -->

> CARD FERRO-812 — Cupons de desconto
>
> Criar cupons de desconto no painel. O cupom tem um código, um tipo (porcentagem ou
> valor fixo), o valor do desconto, uma data de validade e um limite de quantas vezes
> pode ser usado.
>
> Só quem é admin pode criar, editar e excluir cupom. Os outros usuários podem apenas
> listar os cupons ativos.
>
> Na hora de aplicar no pedido, o sistema valida se o cupom existe, se ainda está dentro
> da validade e se não estourou o limite de usos. Se estiver tudo certo, aplica o desconto
> no valor total do pedido e incrementa o contador de usos.
>
> O código do cupom não pode se repetir.
>
> Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois.

## Decomposição em Cláusulas

| ID | Cláusula | Trecho literal de origem | Tipo |
|----|----------|--------------------------|------|
| RQ-01 | Existe um CRUD de cupons de desconto operável por tela de painel | "Criar cupons de desconto no painel." | funcional |
| RQ-02 | O cupom tem um **código** | "O cupom tem um código" | funcional |
| RQ-03 | O cupom tem um **tipo**, que é `porcentagem` **ou** `valor fixo` — os dois únicos | "um tipo (porcentagem ou valor fixo)" | funcional |
| RQ-04 | O cupom tem o **valor do desconto** | "o valor do desconto" | funcional |
| RQ-05 | O cupom tem uma **data de validade** | "uma data de validade" | funcional |
| RQ-06 | O cupom tem um **limite de quantas vezes pode ser usado** | "um limite de quantas vezes pode ser usado" | funcional |
| RQ-07 | Só quem é **admin** pode criar, editar e excluir cupom | "Só quem é admin pode criar, editar e excluir cupom." | autorização |
| RQ-08 | Os demais usuários podem **apenas listar**, e apenas os cupons **ativos** | "Os outros usuários podem apenas listar os cupons ativos." | autorização |
| RQ-09 | Ao aplicar, o sistema valida que o cupom **existe** | "o sistema valida se o cupom existe" | funcional |
| RQ-10 | Ao aplicar, valida que ainda está **dentro da validade** | "se ainda está dentro da validade" | funcional |
| RQ-11 | Ao aplicar, valida que **não estourou o limite de usos** | "e se não estourou o limite de usos" | funcional |
| RQ-12 | Passando as três validações, **aplica o desconto no valor total do pedido** | "aplica o desconto no valor total do pedido" | funcional |
| RQ-13 | Passando as três validações, **incrementa o contador de usos** | "e incrementa o contador de usos" | funcional |
| RQ-14 | O **código não pode se repetir** | "O código do cupom não pode se repetir." | restrição |
| RQ-15 | Registrar **quem** aplicou o cupom e **quando**, para auditoria posterior | "Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois." | funcional |

## Ambiguidades e Perguntas Abertas

> **Condição desta execução**: o usuário não está disponível para responder. Cada item abaixo
> registra a pergunta que **deveria** ter sido feita e a **premissa assumida** para seguir. Toda
> premissa está marcada como tal, nomeia a cláusula que ela resolve e aponta a ADR onde a escolha é
> defendida. Nenhuma delas foi convertida em fato no PRD sem esta marcação.

### A-01 — **Não existe "pedido" neste projeto.** É a ambiguidade mais cara do card

RQ-09 a RQ-13 falam de *"aplicar no pedido"* e de *"desconto no valor total do pedido"*. Verificado
antes de planejar, por `Grep` amplo em `app/`, `database/migrations/` e `database/seeders/`:

- **Não existe** model, migration ou tabela de `Pedido`, `Order`, `Venda`, `Compra`, `Checkout` ou
  `Carrinho`.
- **Não existe nenhuma coluna monetária** em lugar nenhum do projeto. Os models de negócio são
  `Tenant`, `User`, `Convite`, `Role`, `AgenteIa` e `Projeto` (este último, uma demo de tenancy).

Ou seja: o card pressupõe um agregado que o sistema não tem. O cupom tem onde existir; o pedido em
que ele se aplica, não.

**Pergunta que ficaria para o usuário**: *o `Pedido` faz parte desta entrega, ou já existe em outro
sistema/serviço que vai chamar esta regra?*

**Premissa assumida (P-01)**: entregar o **motor do cupom**, não o pedido. A regra de negócio recebe
o valor total como argumento e devolve o valor com desconto:

```php
Cupom::aplicarEm(int $valorTotalEmCentavos, User $aplicadoPor): int
```

RQ-09 a RQ-13 ficam **integralmente cobertas e testáveis** — validação de existência, de validade, de
limite, cálculo do desconto e consumo do uso — sem inventar uma entidade `Pedido` que o requisito não
descreve (não diz o que um pedido tem, quem o cria, nem em que estado ele aceita cupom). Criar um
`Pedido` a partir de uma frase subordinada seria escrever requisito no lugar de quem pediu.

O ponto de integração fica declarado no PRD (`## Ponto de Integração`) e coberto por CT unitário. Ver
**ADR-01**.

### A-02 — "admin" é ambíguo neste kit: há **três** papéis que a palavra descreve

RQ-07 diz *"só quem é admin"*. Em `database/seeders/PapeisSeeder.php` existem cinco papéis, e três
deles cabem na palavra:

| Papel | Painel (`roles.painel`) | O que é |
|---|---|---|
| `master_global` | `null` | dono da instalação; entra em tudo pelo `Gate::before` |
| `admin` | `admin` | administra a **instalação** (organizações, usuários, papéis) |
| `admin_organizacao` | `app` | administra **uma organização**, dentro do painel de negócio |
| `panel_user` | `app` | usuário comum do negócio |
| `infra` | `infra` | observabilidade |

**Pergunta que ficaria para o usuário**: *cupom é dado da instalação (cadastrado uma vez, valendo para
todos) ou de cada organização (cada cliente cria os seus)?*

**Premissa assumida (P-02)**: cupom é **dado de negócio de uma organização**, e o "admin" de RQ-07 é o
**`admin_organizacao`**, no painel `/app`. Três razões, todas verificáveis:

1. Desconto é decisão comercial de quem vende, e quem vende no kit é a organização — o `/app` é o
   painel do negócio, o `/admin` é a operação da instalação.
2. Toda model de negócio do kit usa `App\Traits\BelongsToTenant` (`wikis/convencoes.md` → "Model de
   negócio pertence a um tenant"). Cupom global seria a primeira exceção, e ela precisaria de motivo.
3. `master_global` e o papel `admin` continuam alcançando a tela por herança do `Gate::before`
   (`app/Providers/KitServiceProvider.php` → `configureGates()`), então a leitura estrita de RQ-07
   ("só quem é admin") **não** é violada por esta escolha — ela é a leitura mais restritiva possível.

Ver **ADR-02**.

### A-03 — "cupons ativos" não está definido

RQ-08 fala em *"listar os cupons ativos"*. O card nunca menciona um interruptor de ligar/desligar; ele
menciona **validade** (RQ-05) e **limite de usos** (RQ-06). "Ativo" pode ser:

1. uma coluna `ativo` booleana, como o kit faz em catálogo (`agentes_ia`, ver `wikis/convencoes.md` →
   "Exclusão de configuração é lógica"); ou
2. um **estado derivado**: dentro da validade **e** com usos disponíveis.

**Pergunta que ficaria para o usuário**: *"ativo" é um botão que o admin liga e desliga, ou é
consequência da validade e do limite?*

**Premissa assumida (P-03)**: **estado derivado**, sem coluna nova. O card não pede interruptor, e uma
coluna `ativo` ao lado de `expira_em` e `limite_de_usos` cria **três fontes de verdade para uma
pergunta só** — exatamente a divergência que `Convite::situacao()` foi escrito para evitar
(`wikis/convencoes.md` → tabela "Armadilhas já resolvidas", linha da tabela de convites). O estado
vira `Cupom::situacao()` e o escopo `Cupom::scopeAtivos()`, com uma definição só, num lugar só.

Ver **ADR-03**.

### A-04 — "não pode se repetir" **onde**? Instalação inteira ou dentro da organização?

RQ-14 diz *"O código do cupom não pode se repetir"*, sem escopo.

**Pergunta que ficaria para o usuário**: *duas organizações diferentes podem ter, cada uma, um cupom
`BLACKFRIDAY`?*

**Premissa assumida (P-04)**: unicidade **por organização** — `unique(['tenant_id', 'codigo'])`.

O contrário (unique global) tem consequência que o card não pode ter pretendido: o primeiro cliente a
cadastrar `BEMVINDO` **impede todos os outros** de usarem a palavra, e a mensagem de erro
("código já em uso") revela a existência de um cupom de outro cliente. É vazamento de informação entre
tenants por canal lateral, num kit cujo motivo de existir é o isolamento.

**Consequência obrigatória**: no formulário, `->scopedUnique(ignoreRecord: true)` e **nunca**
`->unique()` — a regra `unique` do Laravel não passa pelo Eloquent e ignora o escopo de tenant
(`wikis/convencoes.md` → "Validação em resource com tenancy"). Ver **ADR-04**.

### A-05 — a mesma coluna `valor` guarda duas grandezas diferentes

RQ-03 dá dois tipos e RQ-04 dá **um** valor. `10` significa "10%" num cupom e "R$ 10,00" no outro. O
card não diz a unidade de nenhum dos dois, e não existe precedente monetário no projeto para herdar.

**Perguntas que ficariam para o usuário**: *o desconto percentual aceita fração (12,5%)? O valor fixo é
em reais ou em centavos?*

**Premissa assumida (P-05)**: uma coluna `valor`, do tipo `unsignedInteger`, cuja **unidade é decidida
pelo `tipo`**:

- `tipo = fixo` → **centavos** (`1000` = R$ 10,00). Dinheiro em `integer` de centavos é a única forma
  que não perde centavo em arredondamento de ponto flutuante.
- `tipo = porcentagem` → **pontos percentuais inteiros**, de 1 a 100 (`10` = 10%). Sem fração, porque o
  card escreveu "porcentagem" e não deu nenhum exemplo fracionário — e admitir fração aqui exigiria
  decidir a escala (décimos? centésimos?) sem ninguém para perguntar.

Ver **ADR-05**, que também registra o gatilho de reavaliação: **no dia em que aparecer um desconto de
12,5%, a coluna vira pontos-base** e a migration é de uma linha.

### A-06 — arredondamento do desconto percentual não foi definido

10% de R$ 99,99 são 999,9 centavos. O card não diz para onde vai a fração.

**Premissa assumida (P-06)**: **truncar** (`intdiv`), o que arredonda o desconto **para baixo**. É
determinístico, nunca concede mais desconto do que o cupom promete, e não depende do modo de
arredondamento do PHP. **É uma escolha de negócio tomada por falta de resposta** e está listada como
pergunta aberta abaixo.

### A-07 — desconto maior que o total não foi previsto

Cupom de R$ 50,00 fixo aplicado a um total de R$ 30,00 daria valor final negativo.

**Premissa assumida (P-07)**: o resultado é **limitado em zero** — nunca negativo. Valor final negativo
não é desconto, é crédito, e crédito é feature que ninguém pediu. Coberto por CT.

### A-08 — "registrar quem aplicou" pode parecer já resolvido pela auditoria, e **não está**

O projeto já tem `owen-it/laravel-auditing` com a trait `App\Traits\AuditsFillables`, e a tentação de
economizar a tabela nova é legítima: a trilha de `/infra/audits` já grava usuário e horário de cada
alteração.

Ela **não** serve aqui, por dois motivos independentes — e o segundo é fatal:

1. `AuditsFillables::getAuditInclude()` devolve o `$fillable`. O contador de usos **não é** campo
   editável pelo usuário e fica fora do `$fillable` pela mesma regra que mantém `Convite::$token` fora
   (`wikis/convencoes.md` → "Armadilhas já resolvidas"). Fora do `$fillable`, fora da trilha.
2. O consumo do uso é feito por **`UPDATE` condicional atômico** (ADR-06), que passa pelo Query Builder
   e **não dispara eventos de model** — logo não gera registro de auditoria nenhum. A trilha ficaria
   silenciosamente vazia, e o buraco só apareceria no dia em que alguém precisasse auditar.

**Premissa assumida (P-08)**: tabela própria `cupom_usos`. Ver **ADR-07**.

### A-09 — o card não diz onde a tela vive nem quem a chama

*"Criar cupons de desconto no painel"* (RQ-01) — o kit tem **três** painéis (`/app`, `/admin`,
`/infra`).

**Premissa assumida (P-09)**: painel **`/app`**, por decorrência direta de P-02. Registrada aqui e não
só na ADR porque é a premissa que, se estiver errada, invalida mais passos do PRD do que qualquer
outra: muda a policy, muda a matriz de permissões, muda a suíte de teste e muda o CT-B.

### Perguntas abertas que ficam para o usuário (nenhuma bloqueia o início)

1. **A-01** — o `Pedido` entra nesta entrega ou o chamador é externo? *(afeta o escopo, não o plano)*
2. **A-05** — o desconto percentual precisa aceitar fração? *(afeta o tipo da coluna `valor`)*
3. **A-06** — truncar ou arredondar a fração do desconto percentual? *(decisão de negócio)*
4. **A-02** — "admin" é o `admin_organizacao` do `/app` ou o `admin` da instalação?
5. **RQ-10** — a validade expira **no início** ou **no fim** do dia escolhido? Assumido: `expira_em` é
   `timestamp` e a comparação é `> now()`, então a validade termina no instante gravado. Se a tela
   oferecer só a data, o valor gravado é `23:59:59` do dia — é o que a pessoa espera ao digitar uma
   data de validade.

## Fora de Escopo (declarado)

<!-- O que o requisito NÃO pede, para o quality gate não acusar omissão indevida. -->

- **Entidade `Pedido`, carrinho, checkout ou qualquer fluxo de venda** — o card os menciona como
  contexto ("na hora de aplicar no pedido"), nunca como coisa a construir. Ver A-01.
- **Tela de aplicação do cupom pelo cliente final** — o card diz que "o sistema valida", não que existe
  uma tela onde alguém digita o código. A superfície de UI desta entrega é o CRUD de RQ-01.
- **Cupom por produto, por categoria ou por cliente** — o card não segmenta nada; o cupom vale para o
  valor total.
- **Cupom de uso único por usuário** (limite por pessoa) — RQ-06 define limite **do cupom**, não por
  usuário. A tabela `cupom_usos` torna essa evolução barata, mas ela não é entregue.
- **Empilhamento de cupons** (dois cupons no mesmo pedido) — não pedido, e não decidível sem regra de
  precedência.
- **Cupom com valor mínimo de pedido, frete grátis ou primeira compra** — nenhum aparece no card.
- **Notificação, e-mail ou relatório de uso de cupom** — RQ-15 pede o **registro**, não a exibição.
- **Desativar cupom manualmente** — ver A-03: o card não pede interruptor.
