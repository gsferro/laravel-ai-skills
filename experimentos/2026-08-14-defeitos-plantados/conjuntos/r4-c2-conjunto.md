# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `wikis/specs/exp-a/aprovacao-de-compra/00-requisito.md` ·
> Plano: `wikis/specs/exp-a/aprovacao-de-compra/01-plano-acao.md`
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação —
> o `01` entrou só para paths, rotas, `## Superfície de UI` e stack, e o que foi **recusado**
> como oráculo está listado em [Fronteira com o Plano](#fronteira-com-o-plano).

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| **A** — máquina de estados (transições, terminais, reenvio, corrida) | 3 | 3 | 9 | **completo** |
| **B** — alçada por valor (limite do diretor) | 3 | 3 | 9 | **completo** |
| **C** — autorização e identidade (policy, barreira no model, matriz de papéis, isolamento por organização) | 3 | 3 | 9 | **completo** |
| **D** — notificação do próximo aprovador | 3 | 3 | 9 | **completo** |
| **E** — gravação da solicitação (criar, editar, excluir) | 2 | 3 | 6 | padrão |
| **F** — leitura na tela (situação + histórico de etapas) | 2 | 3 | 6 | padrão |
| **G** — centro de custo (cadastro e gestor) | 2 | 3 | 6 | padrão |

**Justificativa dos extremos.** `D` recebe `I = 3` e não `2` porque o destinatário do e-mail é
**dado de terceiro**: o papel `diretor` resolvido no contexto errado manda a descrição e o valor de
uma compra da organização A para o diretor da organização B (A-03, ADR-08) — vazamento, não atraso.
`E` recebe `I = 3` porque `situacao` e `solicitante_id` gravados pelo formulário pulariam o fluxo
inteiro (auto-aprovação por mass assignment). `G` recebe `I = 3` porque quem edita o gestor do
centro de custo se nomeia aprovador (A-08).

- **Técnicas aplicadas**: EP, BVA 3-valores (incremento R$ 0,01), tabela de decisão, tabela
  **estado × operação** completa, **2-switch** (e um 3-switch), matriz papel × ação, rastreio de
  efeito com injeção de falha em duas direções, normalização de identidade.
- **Regras**: 13 · **Cenários**: 63 (`04`) + 2 (`05`) · **Mutantes previstos**: 90 (`04`) + 8 (`05`)
  = **98** · **Sem matador**: 3 (todos vinculados a pergunta aberta ou a limite de arnês).
- **Matriz estado × operação**: 35 células — **14 válidas**, **21 inválidas**, 100% cobertas, mais
  uma matriz própria de `CentroCusto` (4 células) e a terceira dimensão **persona** declarada.

> **12 dos 63 cenários (CT-52…CT-63) nasceram da revisão adversarial**, e não da primeira
> derivação. Estão marcados `(rev)` no [Índice](#índice-de-cenários), e o que cada um fecha está em
> [Achados e fechamento](#achados-e-fechamento). Eles são o motivo de seis regras estourarem o teto
> do perfil — **o gate vence o teto**: mutante vivo é pior que cenário a mais.

### Técnica escalada acima do perfil da área — declarado

| Regra | Área (perfil) | Técnica do perfil | Técnica usada | Por quê |
|---|---|---|---|---|
| R1 | E (padrão) | EP, BVA 2-valores | **BVA 3-valores** no `valor` | é dinheiro; 2 valores não distinguem `<` de `<=` no mínimo |
| R2 | E+C (completo herdado) | — | estado × operação completa | R2 atravessa C, e regra que atravessa duas áreas herda o **maior** perfil |
| R9 | F (padrão) | EP amostrada | **EP exaustiva do enum** | rótulo de estado não se amostra: cobrir 3 de 5 permite a tela dizer "Aprovada" faltando uma etapa |
| R13 | G+C (completo herdado) | — | normalização + unicidade contra si mesmo | a armadilha da edição não existe na criação, e `nome` é o único campo único da entrega |

### Divergências declaradas

1. **Project Rule vence a skill.** A skill sugere `pest --parallel --tia` como padrão; `.ai/rules/testes-browser.md:29-40` mediu que `--parallel` derruba 4 dos 11 CT-B e que, sem **PCOV**, o `--tia` em série com Xdebug não termina (abortado após 35 min). **Vale a rule**: dois comandos, `vendor/bin/pest --parallel` para o backend e `vendor/bin/pest --testsuite=Browser` em série.
2. **`pestphp/pest-plugin-mutate` está só em `vendor/`, não em `composer.json`.** Confirmado: `vendor/pestphp/pest-plugin-mutate/` existe, e o `require-dev` do `composer.json:68-82` não o declara — é dependência transitiva do Pest 5. O `--mutate` funciona **por acidente da árvore de dependências** e some num `composer update`. Passo obrigatório antes do [fechamento do ciclo](#fechamento-do-ciclo-com-mutation-testing): `composer require pestphp/pest-plugin-mutate --dev`.
3. **`tests/Unit` não tem `TestCase` ligado.** `phpunit.xml` declara a testsuite `Unit`, mas `tests/Pest.php` liga `Tests\TestCase` apenas a `Feature`, `Kit`, `Tenancy`, `Browser` e `BrowserTenancy` (`tests/Pest.php:22`, `:43`, `:67`, `:101`, `:142`) — **nada** em `Unit`. Um caso ali roda sem container: `config('kit.compras.limite_diretor')` volta `null` e o cast de `SituacaoSolicitacao` não existe. **Nenhum CT desta feature é alocado em `Unit`**; a escada real do projeto começa em `Feature`. Ligar `Unit` seria mudança de arnês fora do escopo desta derivação — registrada como pergunta **P-12**.
4. **O `00-requisito.md` é somente leitura nesta execução** (pertence à pasta `exp-a`, usada como linha de base de comparação). As perguntas novas estão em [Perguntas para o `00-requisito.md`](#perguntas-para-o-00-requisitomd), em bloco pronto para colagem em `## Ambiguidades`. Nenhuma pergunta morreu por causa do arquivo travado, e cada uma bloqueia o que depende dela.

---

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| **S**tructure | 3 tabelas (`centros_custo`, `solicitacoes_compra`, `etapas_aprovacao_compra`), 1 enum de 5 casos, 3 models, 2 policies, 1 notification, 2 Resources no painel `app`, papel `diretor`, chave de config do limite, channel de log, suíte de teste nova | CT-01, CT-34, CT-47 |
| **F**unction | criar / editar / excluir rascunho; enviar; aprovar (1 ou 2 níveis); rejeitar com justificativa; cancelar; exibir situação e histórico; notificar o próximo aprovador; decidir a alçada. **Função escondida**: a subtração do `panel_user` — nada na UI a revela e nada acusa quando falta | CT-01…CT-33, CT-47, CT-48 |
| **D**ata | `descricao` (texto livre), `valor` `decimal(12,2)`, `centro_custo_id`, `situacao` (5 valores), `justificativa` (nullable, texto livre escrito por uma pessoa sobre outra), `etapa`/`decisao` (strings). **Cardinalidade**: 0, 1 e N etapas por solicitação; N diretores por organização; `gestor_id` **nullable**. **Dado de outro tenant**: solicitação e centro de custo de outra organização. **Dado temporal**: `created_at` das etapas ordena o histórico | CT-03, CT-07, CT-11, CT-13, CT-14, CT-22, CT-35, CT-36, CT-44…CT-46, CT-51 |
| **I**nterfaces | tela (table actions, form, infolist, modal de justificativa); rotas `GET` do painel `app`; **os métodos públicos do model chamados direto** — o chamador que a policy não vê (job, comando, seeder, rota de API futura); fila (notificação `ShouldQueue`); seeders de permissão | CT-04, CT-12, CT-18, CT-19, CT-25, CT-31, CT-47 |
| **P**latform | PHP 8.3; **SQLite `:memory:` em teste × MySQL/Postgres em produção** — `decimal:2` volta do banco como **string** no PHP, e comparação de string com float é onde a alçada erra em silêncio; `QUEUE_CONNECTION=sync` em teste (`phpunit.xml`) × `database` em produção — sem worker o e-mail não sai, e isso **não** é defeito da feature; `MAIL_MAILER=array` em teste; Vite build obrigatório para o `05`; ausência de PCOV inviabiliza `--tia` | CT-13, CT-14, CT-39 |
| **O**perations | 5 personas: solicitante, gestor do centro, diretor, `panel_user` sem vínculo, `master_global` (entra por `Gate::before`). **Uso indevido**: auto-aprovação, aprovar solicitação de outro centro, editar `gestor_id` para se nomear aprovador, mandar `situacao` no payload. **Volume**: unidades de etapas por solicitação | CT-04, CT-08, CT-17, CT-20, CT-47, CT-48 |
| **T**ime | duas decisões simultâneas (dois diretores, duas abas, duplo clique); **ordem** gestor → diretor; **reentrada** de `rascunho` depois da rejeição (2-switch); a notificação roda **fora do request**, onde o contexto de organização do `permission.teams` não existe; `created_at` **empatado** entre duas etapas gravadas na mesma transação torna a ordem do histórico indeterminada. **Sem timezone, sem DST, sem expiração, sem agendamento** — nenhuma cláusula do requisito fala de prazo (confirmado: RQ-01…RQ-14 não mencionam tempo; SLA está em Fora de Escopo) | CT-26…CT-29, CT-36, CT-39, CT-42, CT-43, CT-46 |

---

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| **R1** — a solicitação nasce em `rascunho`, com descrição, valor e centro de custo; a situação e o solicitante não vêm do formulário | E (padrão) | RQ-01 | EP + BVA 3-valores + mass assignment | CT-01…CT-04 |
| **R2** — em `rascunho`, e só nela, **o próprio solicitante** edita e exclui a solicitação | E + C (completo) | RQ-02, RQ-03, RQ-10 | estado × operação (`editar`, `excluir`) + criação ≠ edição + IDOR | CT-05…CT-09 |
| **R3** — enviar leva `rascunho` → `aguardando_gestor`, e é recusado se o centro de custo não tem gestor | A (completo) | RQ-04 | estado × operação (`enviar`) + EP (gestor presente/ausente) | CT-10…CT-12 |
| **R4** — valor **acima** do limite exige a aprovação do diretor, **depois** da do gestor; até o limite, a do gestor é final | B (completo) | RQ-05 | BVA 3-valores (R$ 0,01) + tabela de decisão | CT-13…CT-15 |
| **R5** — **só o aprovador da etapa corrente** aprova ou rejeita, e a recusa vale para quem chama o model direto | C (completo) | RQ-06 | matriz papel × ação + estado × operação (`aprovar`) | CT-16…CT-20 |
| **R6** — rejeitar exige justificativa não vazia, devolve a solicitação a `rascunho` e grava quem decidiu e por quê | A (completo) | RQ-06, RQ-07, RQ-08 | EP (justificativa) + recusa com não-efeito | CT-21…CT-25 |
| **R7** — a solicitação rejeitada é reenviada e **recomeça pelo gestor**; o histórico do ciclo anterior sobrevive e as aprovações dele não contam | A (completo) | RQ-08, RQ-09 | **estado × evento 2-switch** (e um 3-switch) | CT-26…CT-29 |
| **R8** — o solicitante cancela **em trânsito**; `aprovada` e `cancelada` não aceitam nenhuma escrita | A (completo) | RQ-10, RQ-11 | estado × operação (`cancelar`) + idempotência no agregado | CT-30…CT-33 |
| **R9** — a tela mostra a situação corrente de **toda** solicitação e, no detalhe, quem decidiu cada etapa, em ordem | F (padrão) | RQ-12, RQ-13 | **EP exaustiva do enum** + ordenação com empate | CT-34…CT-36 |
| **R10** — cada transição que cria uma etapa pendente notifica por e-mail **exatamente** os aprovadores dela, **uma só vez**, e nada é notificado quando a transição não se completa | D (completo) | RQ-14 | **rastreio de efeito** (aconteceu / não aconteceu / uma vez / atomicidade × 2 direções) | CT-37…CT-41 |
| **R11** — duas decisões simultâneas sobre a mesma etapa gravam **uma** decisão | A (completo) | RQ-06, RQ-13 (*"quem aprovou cada etapa"* — singular) + taxonomia | concorrência + idempotência ancorada no agregado | CT-42, CT-43 |
| **R12** — solicitação e centro de custo de uma organização não são vistos nem operados por outra, e o aprovador é resolvido na organização corrente | C (completo) | SFDIPOT **D**/**T** + invariante de `wikis/convencoes.md` | isolamento + IDOR entre tenants | CT-44…CT-46 |
| **R13** — cadastrar centro de custo (e portanto escolher o gestor) é ação de **administração da organização**; o nome é único dentro dela | G + C (completo) | RQ-04, A-08 | matriz papel × ação + normalização + unicidade contra si mesmo | CT-47…CT-51 |

### Rastreabilidade `RQ` → regra

| RQ | Regra(s) | RQ | Regra(s) |
|---|---|---|---|
| RQ-01 | R1 | RQ-08 | R6, R7 |
| RQ-02 | R2 | RQ-09 | R7 |
| RQ-03 | R2 | RQ-10 | R2, R8 |
| RQ-04 | R3, R13 | RQ-11 | R8 |
| RQ-05 | R4 | RQ-12 | R9 |
| RQ-06 | R5, R6, R11 | RQ-13 | R9, R11 |
| RQ-07 | R6 | RQ-14 | R10 |

**Nenhuma `RQ` ficou sem regra.** R12 é a única regra sem `RQ` de origem: ela nasce da dimensão
**D** da varredura (*dado de outro tenant*) e do invariante de `wikis/convencoes.md` que A-01 já
invoca ao declarar `CentroCusto` como `BelongsToTenant`. Está declarada como tal para que ninguém
a leia como cláusula do card.

### Leitura do mapa antes de seguir

- **12 perguntas vermelhas** para 14 cláusulas. É muito, e a causa é conhecida e declarada no
  próprio `00`: *"o usuário não estava disponível para responder nesta execução"*. As 12 têm
  premissa escrita e cenário `@premissa`; **três delas deixam mutante vivo** (P-04, P-05, P-08) e
  estão marcadas como tal no gate.
- **A décima segunda (P-13) só apareceu na revisão adversarial**, e é a de maior impacto de todas:
  *quem enxerga a solicitação de quem, dentro da mesma organização*. Ela não estava nas 12
  ambiguidades do `00` nem nas 11 que esta wiki acrescentou, e a sua resposta errada esvazia a tela
  de todo aprovador. Está em **A-23** e é fixada por **CT-61**.
- **Nenhuma regra sem exemplo.** R12 ganhou o seu exemplo para `CentroCusto` em CT-60 e CT-49
  (a asserção de organização); antes ela falava de "solicitação **e** centro de custo" e nenhum dos
  três cenários de tenancy tocava o centro de custo.
- **Nenhum exemplo sem regra.** Os dois candidatos — a contagem de permissions do painel e o
  conteúdo do e-mail — foram recusados como oráculo na [Fronteira com o Plano](#fronteira-com-o-plano).

---

## Fronteira com o Plano

<!-- O que veio do 01-plano-acao.md e foi RECUSADO como oráculo, para o cenário não virar
     teste do PRD. Item que só o PRD determina e é visível ao usuário vira pergunta. -->

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| nomes `enviar()`, `aprovar()`, `rejeitar()`, `cancelar()`, `exigeDiretor()`, `podeSerDecididaPor()`, `transicionar()` | escolha de implementação | **detalhe** do cenário — o `Então` fala de situação e de registro, não de método |
| nomes de tabela e coluna (`solicitacoes_compra.situacao`, `etapas_aprovacao_compra.decisao`) | escolha de implementação | detalhe do cenário |
| `App\Enums\SituacaoSolicitacao` e os cinco valores em `snake_case` | escolha de implementação **do formato**; o **conjunto** de estados é derivável do requisito ("rascunho", "vai para o gestor", "aprovação do diretor", "aprovada", "cancelar") | os estados viram oráculo; os *valores literais* não |
| **a ausência do estado `rejeitada`** (ADR-01) | o requisito **também** o determina: *"solicitação rejeitada volta para rascunho"* | **vira `Então`** — CT-21, CT-23, CT-24, CT-26 |
| limite em `config/kit.php` / `KIT_COMPRAS_LIMITE_DIRETOR` | escolha de implementação; o requisito determina **R$ 5.000**, não onde ele mora | detalhe do cenário (os CT usam `config()->set()` para não cravar o número duas vezes) |
| `TextInput::minValue(0.01)` no campo `valor` | **só o PRD** determina, e é comportamento visível | **pergunta P-01** — CT-03/CT-07 marcados `@premissa` |
| `maxLength(255)` na descrição | só o PRD, visível ao usuário | **pergunta P-11** |
| texto `"Esta solicitação já mudou de situação. Recarregue a tela."` e as demais mensagens de recusa | só o PRD, visível ao usuário | **pergunta P-10** — nenhum cenário afirma texto de erro |
| cores do badge (`gray`, `warning`, `success`, `danger`) | só o PRD, visível ao usuário | **pergunta P-04** — deixa **M9-4 sem matador**, declarado |
| corpo do e-mail (quem solicitou, descrição, valor em R$, etapa) | só o PRD, visível ao usuário | **pergunta P-05** — deixa **M10-6 sem matador**, declarado |
| channel de log `compras`, formato `[Classe@Método]`, tabela de níveis (`info`/`warning`) | escolha de implementação — **o requisito nunca menciona log** | **detalhe**; nenhum cenário usa log como oráculo único. A **única** exceção é o `warning` de `centro_sem_gestor`, que está no **`00`** (A-10) e não no PRD — e mesmo lá é asserção de apoio de CT-11, cujo oráculo é *"fica em rascunho e nada foi notificado"* |
| `SelectFilter::make('situacao')` na listagem | só o PRD; o requisito pede *mostrar* a situação, não filtrar por ela | fora de escopo dos CT — **pergunta P-08** junto de paginação/ordenação |
| contagem de permissions do painel `app` (38 hoje) e o CT de regressão do `PaineisTest` | só o PRD; é invariante do kit, não cláusula do card | **detalhe** — o que **é** derivável de RQ-04 + A-08 é *"o usuário comum não escolhe o gestor"*, e isso virou CT-47/CT-48 sem citar contagem nenhuma |
| suíte `FeatureTenancy`, `phpunit.xml`, ordem dos seeders | infra de teste, não comportamento | pré-requisito de [Setup Global](#setup-global) |
| `RepeatableEntry`, títulos de `Section` ("Histórico de aprovação") | só o PRD, visível | detalhe — CT-35 afirma sobre os **dados** de cada etapa, não sobre o título da seção |

---

## Perguntas para o `00-requisito.md`

> **Desvio declarado**: o `00-requisito.md` desta feature é **somente leitura** nesta execução
> (linha de base de comparação, em `wikis/specs/exp-a/`). O bloco abaixo é para colagem direta em
> `## Ambiguidades e Perguntas Abertas`, no mesmo formato da seção de destino. Cada item bloqueia a
> regra citada, e o cenário correspondente está marcado `@premissa`.

```markdown
### A-13 — o `valor` tem mínimo? (RQ-01)

**Pergunta**: R$ 0,00 e valor negativo são recusados na gravação? O mínimo é R$ 0,01?

**Assumido**: **sim, mínimo R$ 0,01** — uma compra de R$ 0,00 ou negativa não é compra, e o
requisito fala de "valor" no singular positivo ao ligá-lo a um limite de alçada.

**Se negado**: caem as linhas inválidas de CT-03 e CT-07, e a validação de domínio do `valor`
deixa de existir nos dois pontos de gravação.

### A-14 — o `valor` com mais de duas casas decimais (RQ-05)

**Pergunta**: R$ 5.000,004 arredonda, trunca ou é recusado? E a alçada compara o valor
**digitado** ou o **persistido**?

**Assumido**: persiste com **duas casas** e a alçada compara o **persistido** — logo
R$ 5.000,004 vira R$ 5.000,00 e **não** exige diretor. É a leitura que mantém uma verdade só
no sistema: o valor que a tela mostra é o valor que decide a alçada.

**Se negado** (compara o digitado): CT-14 inverte o oráculo, e passa a existir uma solicitação
cuja alçada não se explica pelo número exibido.

### A-15 — a situação tem cor determinada? (RQ-12)

**Pergunta**: "mostrar o status atual" determina cor/badge, ou só o texto?

**Assumido**: **só o texto**. Cor não é requisito.

**Consequência declarada**: o mutante *"a cor não corresponde à situação"* fica **sem matador**
(M9-4). `assertSee` não valida cor — `.ai/rules/testes-browser.md:54-56` — e screenshot de
badge não foi julgado proporcional.

### A-16 — o que o e-mail precisa dizer? (RQ-14)

**Pergunta**: o corpo do e-mail do aprovador tem conteúdo obrigatório (valor, descrição,
solicitante, link)?

**Assumido**: **o requisito determina o destinatário e o canal, não o conteúdo**.

**Consequência declarada**: o mutante *"o e-mail sai sem o valor e sem a descrição"* fica **sem
matador** (M10-6). Afirmar sobre o corpo seria testar o PRD.

### A-17 — se o e-mail falhar, a aprovação é desfeita? (RQ-14)

**Pergunta**: a transição e a notificação são um bloco atômico?

**Assumido**: **sim** — notificar um aprovador de uma etapa que não ficou gravada é pior que não
notificar, porque ele age sobre uma tela que não confirma o que o e-mail diz. CT-40 e CT-41
cobrem as duas direções.

**Se negado**: CT-41 vira o oposto (a transição sobrevive ao e-mail que falhou) e a feature
precisa de reenvio manual, que não está pedido.

### A-18 — a listagem tem paginação e ordenação determinadas? (RQ-12)

**Assumido**: **não** — o requisito exige que a situação apareça, não quantas por página nem em
que ordem.

**Consequência declarada**: o item **paginação/ordenação** do checklist de taxonomia fica como
lacuna declarada, não como ✅.

### A-19 — o nome do centro de custo é único, e como se compara? (RQ-01, RQ-04)

**Pergunta**: "Compras", "compras" e " Compras " são o mesmo centro de custo?

**Assumido**: único **dentro da organização**, com a comparação **do banco** (SQLite e MySQL
`utf8mb4_unicode_ci` são case-insensitive; Postgres não é). Espaços nas bordas são aparados.

**Se negado**: CT-51 muda de oráculo e a normalização passa a ser explícita no model.

### A-20 — o texto de cada recusa é determinado? (RQ-07, RQ-10, RQ-11)

**Assumido**: **não**. Nenhum cenário afirma texto de mensagem de erro; o oráculo de toda recusa
é *o estado não mudou e nada foi gravado nem notificado*.

### A-21 — a descrição tem limite de tamanho? (RQ-01)

**Assumido**: **o requisito não impõe limite**. O cenário de limite de `varchar` fica sem
oráculo e o item de taxonomia correspondente é lacuna declarada.

### A-22 — `tests/Unit` deve ganhar o `TestCase` da aplicação?

Não é pergunta de negócio, e é a que bloqueia a camada mais barata: `phpunit.xml` tem a testsuite
`Unit` e `tests/Pest.php` não liga `Tests\TestCase` a ela. Todo caso "unitário" desta feature foi
alocado em `Feature` por causa disso.

### A-23 — quem enxerga a solicitação de quem, DENTRO da mesma organização? (RQ-12)

**A pergunta que faltava, e que decide se a feature funciona.** RQ-12 diz "mostrar na tela o status
atual" e não diz **para quem**. Se a listagem recortar por solicitante, todo aprovador abre a tela
vazia e o fluxo inteiro morre — sem erro, sem 403, sem log.

**Assumido**: o solicitante vê as próprias; **o aprovador da vez vê também as que dependem dele**.
É o mínimo que faz "o gestor pode aprovar ou rejeitar" (RQ-06) ser executável pela tela.

**Se negado** (cada um só vê as próprias): a feature precisa de uma segunda tela, uma caixa de
entrada de aprovações, que o card não pede. CT-61 é o cenário que fixa a premissa.

```

---

## Setup Global

### Personas

| Persona | Como criar | Por que ela existe |
|---|---|---|
| `solicitante` | `usuarioCom('panel_user')` — `tests/Pest.php:188` | cria, edita, envia, cancela |
| `outroSolicitante` | `usuarioCom('panel_user')` | segundo usuário do **mesmo** tenant — é ele que faz o IDOR de CT-08 existir |
| `gestor` | `usuarioCom('panel_user')` apontado por `centros_custo.gestor_id` | gestor **não é papel**: é uma FK (A-02) |
| `gestorDeOutroCentro` | idem, apontado por um **segundo** `CentroCusto` | mata o mutante "qualquer gestor aprova" (CT-17, CT-37) |
| `diretor`, `outroDiretor` | `usuarioCom('diretor')` — **papel novo**, `roles.painel = 'app'` | A-03: qualquer diretor decide, e **todos** são notificados. Dois, porque um só não distingue "notifica todos" de "notifica o primeiro" |
| `semPapel` | `usuarioCom(null)` | não entra em painel nenhum (`tests/Kit/PaineisTest.php:53-55`) |

> **Papel novo precisa declarar o painel.** `.ai/rules/filament.md:58-62`: `roles.painel` nulo não
> é coringa — um `diretor` semeado sem painel autentica e leva 403 nos três. O `beforeEach` roda
> `ShieldPermissionsSeeder` e depois `PapeisSeeder`, na ordem de `.ai/rules/filament.md:33-38`, como
> `tests/Kit/PaineisTest.php:20-22` já faz.

### Fixtures

Nenhuma factory desta feature existe hoje. As três são pré-requisito dos CT:

- `CentroCusto::factory()` — com `->semGestor()` (para CT-11) e `->comGestor(User $u)`
- `SolicitacaoCompra::factory()` — com um state por situação: `->rascunho()`, `->aguardandoGestor()`,
  `->aguardandoDiretor()`, `->aprovada()`, `->cancelada()`; e `->abaixoDoLimite()` /
  `->acimaDoLimite()`
- `EtapaAprovacao::factory()` — só para montar histórico de ciclo anterior sem passar pelas transições

> **A factory grava `situacao` direto, por desenho.** É o arnês que permite existir uma solicitação
> em `aprovada` sem ter atravessado o fluxo — e sem ele **21 células inválidas da matriz seriam
> inalcançáveis**, porque o único caminho até `aprovada` é o caminho feliz. É o mesmo recurso que a
> skill nomeia em *"impossibilidade de arnês é hipótese"*: factory com estado gravado direto.

### Fakes

- `Notification::fake()` — em todo CT de R3, R5, R6, R7, R8, R10, R11, R12
- **Nunca `Mail::assertSent`**: a notificação é `ShouldQueue`, e o par certo é
  `Notification::fake()` + `assertSentTo` / `assertNotSentTo` / `assertSentTimes` /
  `assertNothingSent`
- **E o canal tem de ser afirmado.** `assertSentTo` sozinho fica verde com a notificação entregue
  **só** por `database` (o sininho do painel) — e RQ-14 diz **"notificar por e-mail"**. O closure de
  `assertSentTo` recebe os canais como segundo argumento, e é ele que fecha isso:
  `assertSentTo($ana, AprovacaoPendente::class, fn ($n, array $canais) => in_array('mail', $canais, true))`.
  Proibir `Mail::assertSent` **não** dispensa afirmar o canal — são coisas diferentes, e confundi-las
  deixa metade de RQ-14 sem oráculo. Usado em **CT-37**
- **Nenhum `Event::fake()`** — ele mataria os eventos de model que geram `uuid` no `creating`
  (`app/Traits/TemUuid.php`), e a fixture nasceria quebrada
- **Nenhum `Http::fake()`** — a feature não chama serviço externo
- Espião de log (só CT-11, como asserção de apoio): no molde de `espiarAutenticacao()`
  (`tests/Pest.php:239-246`), um `espiarCompras()` que devolve o `LoggerInterface` do channel
  `compras` e deixa os outros reais

### Estratégia de DB

- `RefreshDatabase`, já global em `tests/Pest.php` para todas as pastas registradas
- **`config()->set('kit.compras.limite_diretor', 5000.00)` no `beforeEach`** dos CT de R4 — o
  cenário não pode depender do `.env` da máquina de quem roda
- `travelTo()` / `freezeTime()` só em CT-36, onde o **empate** de `created_at` é o ponto

### Helpers compartilhados

`solicitacaoEm(SituacaoSolicitacao $s, ...)` e `espiarCompras()` serão usados por mais de um
arquivo de teste ⇒ **vivem em `tests/Pest.php`**, não num dos arquivos. `.ai/rules/testes.md:3-11`:
helper cruzado entre dois arquivos estoura `Call to undefined function` em `--parallel`, `--tia` ou
arquivo isolado, e é enforçado por `tests/Kit/HelpersDeTesteTest.php`. **Não criar clone com outro
nome** para escapar de colisão.

### Arquivos

| Arquivo | Suíte | Conteúdo |
|---|---|---|
| `tests/Feature/AprovacaoDeCompra/SolicitacaoTest.php` | `Feature` | R1, R2 |
| `tests/Feature/AprovacaoDeCompra/MaquinaDeEstadosTest.php` | `Feature` | R3, R7, R8, R11 |
| `tests/Feature/AprovacaoDeCompra/AlcadaTest.php` | `Feature` | R4 |
| `tests/Feature/AprovacaoDeCompra/AutorizacaoTest.php` | `Feature` | R5, R6, R13 (autorização) |
| `tests/Feature/AprovacaoDeCompra/NotificacaoTest.php` | `Feature` | R10 |
| `tests/Feature/AprovacaoDeCompra/TelasTest.php` | `Feature` (Livewire) | R9 e as metades de tela de R1, R2, R5, R6, R13 |
| `tests/FeatureTenancy/AprovacaoDeCompraTest.php` | `FeatureTenancy` (**nova**) | R12 |
| `tests/Browser/AprovacaoDeCompraTest.php` | `Browser` | CT-B01, CT-B02 |

---

## Matriz Estado × Operação

As colunas são **todas as operações** que a entidade aceita, não apenas a de leitura. 5 estados ×
7 operações = **35 células**: **14 válidas** (`✅`) e **21 inválidas** (`❌`). Toda célula tem
cenário — e **cada coluna tem ao menos uma célula válida exercitada**, que é a metade da regra que
some quando se cobre só as recusas.

| Estado ↓ / Operação → | `editar` | `excluir` | `enviar` | `aprovar` | `rejeitar` | `cancelar` | `visualizar` (lista + detalhe) |
|---|---|---|---|---|---|---|---|
| `rascunho` | ✅ CT-05 | ✅ CT-06, CT-58 | ✅ CT-10 | ❌ CT-16 | ❌ CT-21 | ❌ CT-30 | ✅ CT-34 + CT-35 |
| `aguardando_gestor` | ❌ CT-05 | ❌ CT-06 | ❌ CT-10 | ✅ CT-16 | ✅ **CT-23** | ✅ CT-30 | ✅ CT-34 + CT-61 |
| `aguardando_diretor` | ❌ CT-05 | ❌ CT-06 | ❌ CT-10 | ✅ CT-16 | ✅ **CT-24** | ✅ CT-30 | ✅ CT-34 + CT-36 |
| `aprovada` | ❌ CT-05 | ❌ CT-06 | ❌ CT-10 | ❌ CT-16 | ❌ CT-21 | ❌ CT-30 | ✅ CT-34 + **CT-57** |
| `cancelada` | ❌ CT-05 | ❌ CT-06 | ❌ CT-10 | ❌ CT-16 | ❌ CT-21 | ❌ CT-30 | ✅ CT-34 + CT-32 |

**Contagem por coluna** — válidas / inválidas: `editar` 1/4 · `excluir` 1/4 · `enviar` 1/4 ·
`aprovar` 2/3 · `rejeitar` 2/3 · `cancelar` 2/3 · `visualizar` 5/0. **Total 14/21.**

### As três dimensões que a matriz colapsa, e onde cada uma foi reaberta

Uma matriz bidimensional percorrida com **uma persona fixa** e **um campo representativo** parece
completa e não é. As três dimensões colapsadas, declaradas:

| Dimensão colapsada | O que escapava | Reaberta em |
|---|---|---|
| **persona** — as colunas de escrita são percorridas pelo dono / pelo aprovador da vez | a barreira de **identidade** na escrita (a de **situação** é que era testada) | **CT-54** (`editar`/`excluir` pelo colega), CT-12, CT-31, CT-17 (7 linhas de persona) |
| **qual campo** — `editar` é exercitada pela descrição | `centro_custo_id` é o único dos três campos de RQ-01 que **decide o aprovador**, e nenhuma célula o editava | **CT-56** |
| **qual `rascunho`** — a célula válida de `excluir` usa um rascunho virgem, com 0 etapas | o rascunho **pós-rejeição** carrega etapas: excluir com histórico é o caso que quebra por FK | **CT-58** |

E a coluna `visualizar` não era 5/0: eram 5 células **na listagem** (CT-34) e **uma** na tela de
detalhe. A tabela acima passou a nomear as duas leituras, e a célula que faltava — *ver quem
assinou cada etapa de uma solicitação **aprovada***, que é o coração de RQ-13 — é **CT-57**.

### Matriz de `CentroCusto`

R13 tinha criar, editar e a matriz de permissões, e **nenhuma coluna `excluir`**:

| Estado do centro ↓ / Operação → | `criar` | `editar` (inclusive o gestor) | `excluir` |
|---|---|---|---|
| sem solicitação vinculada | ✅ CT-49 · ❌ CT-62 (persona errada) | ✅ CT-50 · ❌ CT-62 | ✅ CT-59 |
| com solicitação em repouso (`rascunho`) | — | ✅ **CT-55** — trocar o gestor troca quem decide no próximo envio | ❌ CT-59 |
| com solicitação em trânsito | — | ✅ **CT-55** — o aprovador é resolvido na hora da decisão, não congelado no envio | ❌ CT-59 |

> A célula *"editar o gestor com solicitação em trânsito"* é a materialização exata do risco de
> A-08, e o que a fecha é **CT-55**: ele prova que o aprovador da vez é lido **no momento da
> decisão**. Uma implementação que resolve o aprovador nesse momento se comporta igual nas duas
> linhas; uma que o desnormaliza no envio falha em CT-55 e falharia aqui pelo mesmo motivo.

Três leituras que a matriz obriga e o diagrama do PRD esconde:

1. **A coluna `visualizar` é a partição exaustiva do enum.** Suas 5 células válidas *são* a regra
   R9: se o rótulo de `aguardando_diretor` não estiver coberto, a tela pode dizer "Aprovada"
   faltando uma etapa.
2. **As duas linhas terminais têm 6 recusas cada** — e o defeito que elas pegam não é *"a
   solicitação aprovada some da listagem"* (ela **não** some), é *"a solicitação aprovada ainda
   aceita escrita"*. É a célula que mais escapa, e são 12 delas aqui.
3. **`rejeitar` tem duas células válidas, e elas não são a mesma.** O gestor rejeitando e o diretor
   rejeitando levam **ambos** a `rascunho` (e não a `aguardando_gestor`) — CT-23 e CT-24 são
   cenários separados justamente porque o mutante *"a rejeição do diretor devolve à etapa do
   gestor"* só morre no segundo.

---

## Regra R1 — a solicitação nasce em `rascunho`, com descrição, valor e centro de custo

> `RQ-01` · área **E**, perfil **padrão** · técnica: **EP** + **BVA 3-valores** (fronteira: `valor`,
> incremento **R$ 0,01**) + **mass assignment**
> Técnica escalada acima do perfil: BVA 3-valores em vez de 2, porque o campo é dinheiro.

```gherkin
# language: pt
Funcionalidade: Fluxo de aprovação de solicitação de compra

  Regra: a solicitação nasce em rascunho, com descrição, valor e centro de custo, e nem a
         situação nem o solicitante vêm do formulário

    Cenário: [CT-01] o formulário grava a solicitação em rascunho e no nome de quem a criou
      Dado o solicitante autenticado e um centro de custo "Suprimentos"
      Quando ele grava uma solicitação com descrição "Notebook para o time de campo",
             valor R$ 4.999,99 e centro de custo "Suprimentos"
      Então existe uma solicitação com essa descrição, valor R$ 4.999,99 e o centro "Suprimentos"
      E a situação dela é "rascunho"
      E o solicitante dela é o usuário autenticado

    Esquema do Cenário: [CT-02] campo obrigatório ausente, nulo e vazio são recusados na gravação
      Dado o solicitante autenticado e um centro de custo "Suprimentos"
      Quando ele tenta gravar uma solicitação com <campo> igual a <entrada>
      Então o formulário acusa erro em <campo>
      E nenhuma solicitação foi gravada

      Exemplos:
        | campo           | entrada        | # partição            |
        | descricao       | ausente        | ausente               |
        | descricao       | ""             | vazio                 |
        | descricao       | "   "          | só espaços            |
        | valor           | ausente        | ausente               |
        | centro_custo_id | ausente        | ausente               |
        | centro_custo_id | null           | nulo explícito        |

    @premissa  # P-01: o mínimo R$ 0,01 é premissa; o requisito não determina mínimo
    Esquema do Cenário: [CT-03] o domínio do valor é cobrado na CRIAÇÃO
      Dado o solicitante autenticado e um centro de custo "Suprimentos"
      Quando ele tenta gravar uma solicitação com valor <valor>
      Então o resultado é "<resultado>"
      E o número de solicitações gravadas é <gravadas>
      E o valor gravado é <valor_gravado>

      Exemplos:
        | valor       | resultado | gravadas | valor_gravado | # borda   |
        | -0,01       | recusado  | 0        | —             | negativo  |
        | 0,00        | recusado  | 0        | —             | borda−1   |
        | 0,01        | aceito    | 1        | 0,01          | borda     |
        | 0,02        | aceito    | 1        | 0,02          | borda+1   |

    Cenário: [CT-04] situação e solicitante enviados no payload são ignorados
      Dado o solicitante autenticado e um centro de custo "Suprimentos"
      E outro usuário chamado "Vítima"
      Quando ele grava uma solicitação enviando também situação "aprovada" e
             solicitante igual a "Vítima"
      Então a situação da solicitação gravada é "rascunho"
      E o solicitante dela é o usuário autenticado, não "Vítima"
      E nenhuma etapa de aprovação foi gravada

    Cenário: [CT-60] (rev) o centro de custo do payload tem de ser da organização de quem grava
      Dado o solicitante da organização "Acme" autenticado
      E um centro de custo "Compras" pertencente à organização "Globex", com o gestor Caio
      Quando ele grava uma solicitação apontando para o centro de custo da Globex
      Então a gravação é recusada
      E nenhuma solicitação foi gravada
      E Caio não recebe nenhum e-mail de aprovação pendente
```

**Camada**: CT-01, CT-02, CT-03 → componente Livewire (`fillForm` → `->call('create')` →
`assertHasFormErrors` / `assertDatabaseHas`). **CT-01 é o cenário que satisfaz o
[gate de tela de escrita](#gate-de-tela-de-escrita) da rota `create` de solicitação.**
CT-04 e CT-60 → `Feature` (o payload direto é o que a tela não manda). CT-60 vive em
`tests/FeatureTenancy/`, porque só ali existem duas organizações.

**Por que CT-03 afirma o valor gravado, e não só a contagem.** `gravadas = 1` é o mesmo para
`0,01` e `0,02`: sem a coluna `valor_gravado`, uma implementação que **trunca, zera ou arredonda**
o valor na gravação passa nas duas linhas aceitas. O item *"fronteira no ponto de entrada"* do
checklist pede a fronteira **na gravação**, e uma fronteira verificada só pela recusa é meia
fronteira.

**Por que CT-60 é de R1 e não de R12.** A FK do centro de custo é o **terceiro** campo que RQ-01
nomeia, e é o único do formulário que viaja no payload apontando para outra tabela — logo é
mass assignment com consequência de fronteira de organização. CT-04 cobre `situacao` e
`solicitante_id` e **não** cobria a FK: uma solicitação da Acme apontando para um centro da Globex
seria aprovada pelo gestor da Globex, com a descrição e o valor junto. É a mesma consequência que
justifica `I = 3` na área D, por uma porta que nenhuma outra regra fechava.

**Valores discriminantes.** `4.999,99` em CT-01 e não `1.000,00`: é o único valor que também prova
que gravar **abaixo** do limite não pré-decide a alçada. As bordas de CT-03 usam **R$ 0,01**, o
incremento do `decimal(12,2)` — com incremento de R$ 1,00 as linhas `0,00` e `1,00` não distinguem
`>= 0` de `> 0`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1-1 | a situação inicial é `aguardando_gestor` — "criar já é pedir" | CT-01 |
| M1-2 | `solicitante_id` vem do formulário em vez do autenticado | CT-01, CT-04 |
| M1-3 | `""` e `"   "` passam como descrição preenchida (`isset` em vez de `filled`) | CT-02 (linhas vazio e só espaços) |
| M1-4 | `situacao` e `solicitante_id` estão no `$fillable` | **CT-04** — único matador |
| M1-5 | `>= 0` no mínimo do valor, aceitando R$ 0,00 | CT-03 (linha borda−1) |
| M1-6 | o valor é truncado ou arredondado a inteiro na gravação | CT-03 (coluna `valor_gravado`) |
| M1-7 | a FK do centro de custo é aceita sem conferir a organização | **CT-60** — único matador |

---

## Regra R2 — em `rascunho`, e só nela, o próprio solicitante edita e exclui

> `RQ-02`, `RQ-03`, `RQ-10` · área **E + C**, perfil **completo** (herda o maior) ·
> técnica: **estado × operação** (colunas `editar` e `excluir`) + **criação ≠ edição** + **IDOR**

```gherkin
    Esquema do Cenário: [CT-05] editar só vale em rascunho — coluna `editar` da matriz
      Dado uma solicitação do solicitante na situação <situacao>
      Quando o solicitante tenta alterar a descrição para "Notebook i7"
      Então o resultado é "<resultado>"
      E a descrição gravada é "<descricao_final>"
      E a situação continua <situacao>
      E nenhuma etapa de aprovação foi criada

      Exemplos:
        | situacao            | resultado | descricao_final | # célula |
        | rascunho            | aceito    | Notebook i7     | válida   |
        | aguardando_gestor   | recusado  | Notebook        | inválida |
        | aguardando_diretor  | recusado  | Notebook        | inválida |
        | aprovada            | recusado  | Notebook        | inválida |
        | cancelada           | recusado  | Notebook        | inválida |

    Esquema do Cenário: [CT-06] excluir só vale em rascunho — coluna `excluir` da matriz
      Dado uma solicitação do solicitante na situação <situacao>
      Quando o solicitante tenta excluí-la
      Então o resultado é "<resultado>"
      E o número de solicitações que restam é <restam>

      Exemplos:
        | situacao            | resultado | restam | # célula |
        | rascunho            | aceito    | 0      | válida   |
        | aguardando_gestor   | recusado  | 1      | inválida |
        | aguardando_diretor  | recusado  | 1      | inválida |
        | aprovada            | recusado  | 1      | inválida |
        | cancelada           | recusado  | 1      | inválida |

    @premissa  # P-01
    Esquema do Cenário: [CT-07] o domínio do valor é cobrado também na EDIÇÃO
      Dado uma solicitação do solicitante em rascunho com valor R$ 100,00
      Quando o solicitante tenta alterar o valor para <valor>
      Então o resultado é "<resultado>"
      E o valor gravado é <valor_final>

      Exemplos:
        | valor  | resultado | valor_final | # borda  |
        | -0,01  | recusado  | 100,00      | negativo |
        | 0,00   | recusado  | 100,00      | borda−1  |
        | 0,01   | aceito    | 0,01        | borda    |

    Cenário: [CT-08] a tela de edição da solicitação de um colega não abre
      Dado uma solicitação em rascunho do solicitante
      E outro solicitante da mesma organização, autenticado
      Quando o outro solicitante tenta abrir a tela de edição dessa solicitação
      Então o acesso é recusado com status 403

    Cenário: [CT-54] (rev) o colega não GRAVA nem apaga o rascunho alheio, mesmo fora da tela
      Dado uma solicitação em rascunho do solicitante, com descrição "Notebook"
      E outro solicitante da mesma organização
      Quando o outro solicitante altera a descrição para "Notebook i7" chamando o método
             de domínio direto, sem passar pela tela
      Então a alteração é recusada
      E a descrição gravada continua "Notebook"
      E a situação continua "rascunho"
      E o número de solicitações que restam é 1

    Cenário: [CT-58] (rev) excluir um rascunho que carrega o histórico do ciclo anterior
      Dado uma solicitação rejeitada pelo diretor e de volta a "rascunho",
        com 2 etapas no histórico
      Quando o solicitante a exclui
      Então a exclusão é aceita
      E o número de solicitações que restam é 0
      E não sobra nenhuma etapa de aprovação daquela solicitação

    Cenário: [CT-56] (rev) trocar o centro de custo em rascunho troca o aprovador do envio
      Dado uma solicitação em rascunho de R$ 4.000,00 no centro "Suprimentos", cujo gestor é Ana
      E um centro de custo "TI", cujo gestor é Caio
      E que o solicitante alterou o centro de custo dela para "TI"
      Quando o solicitante a envia
      Então o centro de custo gravado é "TI"
      E Caio recebe o e-mail de aprovação pendente
      E Ana não recebe nenhum e-mail

    Esquema do Cenário: [CT-09] operar um registro que não existe não apaga nem altera nada
      Dado uma solicitação em rascunho do solicitante e um uuid que não pertence a nenhuma
      Quando o solicitante <operacao> pelo uuid <alvo>
      Então o resultado é "<resultado>"
      E o número de solicitações que restam é <restam>

      Exemplos:
        | operacao   | alvo         | resultado | restam | # caso                |
        | edita      | inexistente  | 404       | 1      | id inexistente        |
        | exclui     | inexistente  | 404       | 1      | id inexistente        |
        | exclui     | a própria    | aceito    | 0      | primeira exclusão     |
        | exclui     | a própria    | 404       | 0      | excluir duas vezes    |
```

**Camada**: CT-05, CT-06 → **duas camadas, por desenho** — a linha válida por componente Livewire
(`fillForm` → `->call('save')` → `assertDatabaseHas`, satisfazendo o
[gate de tela de escrita](#gate-de-tela-de-escrita) da rota `edit`) e as quatro inválidas por
`Feature` chamando o model direto, porque em `aprovada` a policy esconde o botão e **a tela nunca
alcança a célula**. Cobrir só pela tela é o caminho para a barreira não existir no model. CT-07 →
Livewire. CT-08, CT-09 → `Feature`.

**As duas armadilhas próprias da edição, e onde cada uma está.**
*Validação que só roda na criação*: **CT-07** existe só para isso — CT-03 ficaria verde com a
validação escrita apenas no `create`. *Unicidade contra si mesmo*: **não se aplica à solicitação**,
que não tem campo único; a armadilha vive em `CentroCusto.nome` e está em **CT-50**.

**CT-08 e CT-54 são as duas metades de uma coisa só, e a primeira sozinha não prova nada.** CT-08
é um `GET` recusado — afirmar depois dele que "o registro continua o mesmo" é **vacuamente
verdadeiro**, porque nenhuma escrita foi tentada em implementação alguma. A barreira que RQ-02 e
RQ-03 pedem (*"**ele** pode editar e excluir"*) é de **identidade na escrita**, e ela só é
falsificável chamando o método de domínio direto, como manda `.ai/rules/filament.md:29`. Sem CT-54,
uma implementação com a policy negando `view` e o `save` conferindo **só a situação** passa no
conjunto inteiro — e o primeiro job, comando ou rota de API edita o rascunho alheio.

**Por que a matriz sozinha não alcançava CT-54, CT-56 e CT-58.** A matriz estado × operação é
percorrida **com uma persona fixa** (o dono) e **um campo representativo** (a descrição). As três
lacunas moram nas dimensões que ela colapsa: **persona** (CT-54), **qual campo** (CT-56 — o centro
de custo é o único dos três campos de RQ-01 que decide o aprovador, e nenhum cenário o editava) e
**qual rascunho** (CT-58 — o rascunho pós-rejeição carrega etapas, e excluir com histórico é o caso
que quebra por chave estrangeira). Está declarado na
[Matriz Estado × Operação](#matriz-estado--operação).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M2-1 | a barreira de situação existe só na policy (affordance), não no model | CT-05, CT-06 (linhas inválidas, chamadas direto) |
| M2-2 | `aprovada` barra a edição mas `cancelada` não — só o estado citado no card foi tratado | CT-05, CT-06 (linha `cancelada`) |
| M2-3 | a validação do valor foi escrita no `create` e esquecida no `save` | **CT-07** — único matador |
| M2-4 | a autorização confere a permissão mas não o dono do registro | CT-08 (leitura) + **CT-54** (escrita) |
| M2-5 | excluir usa `delete()` sem conferir se o registro existe, e a segunda exclusão responde 200 | CT-09 (linha "excluir duas vezes") |
| M2-6 | a barreira de dono vive só na policy da tela; o método de domínio confere só a situação | **CT-54** — único matador |
| M2-7 | excluir um rascunho com histórico estoura por FK, ou deixa as etapas órfãs | **CT-58** |
| M2-8 | o centro de custo é editável no formulário mas o aprovador continua sendo o do centro antigo | **CT-56** |

---

## Regra R3 — enviar leva `rascunho` a `aguardando_gestor`, e falha fechado sem gestor

> `RQ-04` · área **A**, perfil **completo** · técnica: **estado × operação** (coluna `enviar`) +
> **EP** (gestor presente / ausente)

```gherkin
    Esquema do Cenário: [CT-10] enviar só vale em rascunho — coluna `enviar` da matriz
      Dado uma solicitação do solicitante na situação <situacao>, cujo centro de custo tem gestor
      Quando o solicitante tenta enviá-la para aprovação
      Então o resultado é "<resultado>"
      E a situação passa a ser <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | situacao            | resultado | situacao_final      | etapas | # célula |
        | rascunho            | aceito    | aguardando_gestor   | 0      | válida   |
        | aguardando_gestor   | recusado  | aguardando_gestor   | 0      | inválida |
        | aguardando_diretor  | recusado  | aguardando_diretor  | 1      | inválida |
        | aprovada            | recusado  | aprovada            | 1      | inválida |
        | cancelada           | recusado  | cancelada           | 0      | inválida |

    @premissa  # A-10 do 00: falha fechado é premissa, não cláusula do card
    Cenário: [CT-11] sem gestor no centro de custo, o envio é recusado e a solicitação fica em rascunho
      Dado uma solicitação em rascunho cujo centro de custo está sem gestor
      Quando o solicitante tenta enviá-la para aprovação
      Então o envio é recusado
      E a situação continua "rascunho"
      E nenhuma etapa de aprovação foi gravada
      E nenhum e-mail de aprovação pendente foi enviado a ninguém

    Cenário: [CT-12] quem não é o solicitante não envia, mesmo chamando o model direto
      Dado uma solicitação em rascunho do solicitante
      Quando o gestor do centro de custo tenta enviá-la
      Então o envio é recusado
      E a situação continua "rascunho"
      E nenhuma etapa de aprovação foi gravada
      E nenhum e-mail de aprovação pendente foi enviado
```

**Camada**: todos `Feature`. CT-12 chama o método do model **direto**, com a pessoa errada — é o
teste que `.ai/rules/filament.md:29` cobra literalmente (*"barreira sem teste direto não é
barreira"*), porque o caso que passa pela tela continuaria verde com a asserção removida.

**Nota sobre CT-11.** O oráculo é o par *situação continua rascunho* + *nada notificado*. O
`warning` com `motivo: 'centro_sem_gestor'` é **asserção de apoio** e vem de A-10 no `00`, não do
PRD — sozinho ele não distingue "recusou" de "recusou depois de gravar". As duas alternativas que o
`00` recusa têm mutante próprio: pular a etapa (M3-3) e enviar para ninguém (M3-4).

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M3-1 | o envio aceita qualquer situação que não seja terminal (`!= aprovada`) | CT-10 (linhas `aguardando_gestor`, `aguardando_diretor`) |
| M3-2 | o envio de uma solicitação já enviada é idempotente e responde sucesso | CT-10 (linha `aguardando_gestor`) |
| M3-3 | sem gestor, o envio **pula** a etapa e vai direto para `aguardando_diretor` ou `aprovada` | **CT-11** |
| M3-4 | sem gestor, a situação avança e a notificação é apenas omitida | **CT-11** (situação continua rascunho) |
| M3-5 | o envio confere a situação mas não a identidade de quem envia | CT-12 |

---

## Regra R4 — acima do limite exige o diretor, depois do gestor

> `RQ-05` · área **B**, perfil **completo** · técnica: **BVA 3-valores** (fronteira R$ 5.000,00,
> incremento **R$ 0,01**) + **tabela de decisão**

```gherkin
    @premissa  # P-02 / A-04: "acima de" lido como estritamente maior
    Esquema do Cenário: [CT-13] o limite do diretor é exclusivo — R$ 5.000,00 exatos não exigem diretor
      Dado uma solicitação de valor <valor> em "aguardando_gestor", recarregada do banco
      Quando o gestor do centro de custo a aprova
      Então a situação passa a ser <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | valor      | situacao_final      | etapas | # borda  |
        | 4.999,98   | aprovada            | 1      | dentro   |
        | 4.999,99   | aprovada            | 1      | borda−1  |
        | 5.000,00   | aprovada            | 1      | borda    |
        | 5.000,01   | aguardando_diretor  | 1      | borda+1  |
        | 5.000,02   | aguardando_diretor  | 1      | borda+2  |

    @premissa  # P-03 / A-14: a alçada compara o valor persistido
    Cenário: [CT-14] o valor digitado com três casas é persistido com duas
      Dado o solicitante autenticado e um centro de custo "Suprimentos"
      Quando ele grava uma solicitação com o valor digitado como R$ 5.000,004
      Então o valor gravado da solicitação é R$ 5.000,00

    @premissa  # P-03 / A-14
    Cenário: [CT-63] (rev) a alçada é decidida sobre o valor persistido, não sobre o digitado
      Dado uma solicitação em "aguardando_gestor" cujo valor foi digitado como R$ 5.000,004
        e cujo valor persistido é R$ 5.000,00, recarregada do banco
      Quando o gestor do centro de custo a aprova
      Então a situação passa a ser "aprovada"
      E nenhum e-mail de aprovação pendente foi enviado a nenhum diretor

    Cenário: [CT-15] o valor editado antes do envio decide a alçada daquele envio
      Dado uma solicitação em rascunho de R$ 4.999,99
      E que o solicitante alterou o valor para R$ 5.000,01
      E que ele a enviou, ficando em "aguardando_gestor"
      Quando o gestor do centro de custo a aprova
      Então a situação passa a ser "aguardando_diretor"
      E o número de etapas de aprovação gravadas é 1

    Cenário: [CT-52] (rev) o limite ENTREGUE é R$ 5.000,00
      Dado a aplicação com a configuração de fábrica, sem nenhum ajuste do teste
      Quando o gestor do centro de custo aprova uma solicitação de R$ 5.000,01
      Então a situação passa a ser "aguardando_diretor"
      E uma solicitação de R$ 5.000,00, aprovada pelo gestor nas mesmas condições,
        passa a ser "aprovada"
```

**Camada**: `Feature` (o `Então` afirma sobre situação persistida e contagem de registros). CT-14 →
Livewire (é gravação por formulário). Não `Unit`: `exigeDiretor()` lê `config()`, e `tests/Unit`
roda sem container neste projeto (ver [Divergências](#divergências-declaradas)).

**"Recarregada do banco" no `Dado` de CT-13 e CT-63 não é enfeite.** A dimensão **P** da varredura
nomeia o risco: `decimal:2` volta do driver como **string**, e comparar string com float é onde a
alçada erra em silêncio. Se a fixture atribui o valor em memória e a decisão acontece na mesma
instância, o tipo comparado é o que o PHP atribuiu — nunca o que o banco devolveu, que é o caminho
de produção. O `Dado` obriga um `->fresh()` antes da decisão; sem ele o risco declarado no SFDIPOT
não é exercitado por cenário nenhum.

**CT-52 é o único cenário do conjunto que exercita o número R$ 5.000.** Todos os outros de R4 rodam
com o limite injetado por `config()->set` no `beforeEach` — o que testa o comportamento
**parametrizado** e deixa o **parâmetro entregue** sem oráculo. Um default gravado em centavos
(`500000`), um zero a mais, ou um nome de chave que diverge entre o `config` e o `.env.example`
libera toda compra até meio milhão com uma assinatura só, e **nenhum outro cenário acusa**. O valor
`5.000` é a única grandeza literal do card: onde ele mora é implementação, quanto ele vale é
cláusula.

**CT-14 e CT-63 eram um cenário só, com dois `Quando` (`"envia e aprova"`).** Foram separados: se
o cenário fundido falhasse, não se saberia se a alçada foi congelada no envio ou avaliada errado na
aprovação. CT-14 afirma a persistência; CT-63 afirma a decisão sobre o que foi persistido.

**Por que estes valores, e não R$ 10.000.** `5.000,00` é o **único** valor que distingue `>` de
`>=` — é a linha que, faltando, deixa a política de alçada errada por um centavo e ninguém relê.
`4.999,98` e `5.000,02` existem para o mutante *"o limite foi lido mas comparado com o valor
errado"* (por exemplo `>= 5000.01`), que sobrevive a um dataset de dois valores. E `5.000,004`
(CT-14) é o valor discriminante de **precisão**: comparado antes de persistir, em `float`, ele
`> 5000` e exige diretor; comparado depois do `decimal(12,2)`, não. Nenhum valor redondo separa as
duas implementações.

> **Nenhum exemplo desta feature usa `float` como tipo do valor.** Os cenários falam em reais com
> centavos e o oráculo é sempre o valor **persistido**. Não há aritmética monetária na feature —
> nenhuma soma, total ou rateio —, só comparação: por isso não há cenário de arredondamento de
> centavo, e a ausência está declarada aqui em vez de virar ✅ silencioso no checklist.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M4-1 | `>=` no lugar de `>` — R$ 5.000,00 exige diretor | **CT-13** (linha borda) |
| M4-2 | `>` com o limite deslocado (`> 5000.01`) | CT-13 (linha borda+1) |
| M4-3 | a alçada é avaliada e **congelada na criação**, ignorando a edição em rascunho | **CT-15** |
| M4-4 | a etapa do diretor vem **antes** da do gestor (ou substitui a dele) | CT-13 (contagem de etapas = 1 em borda+1) e CT-17 |
| M4-5 | o valor é comparado como digitado, em `float`, antes de persistir | **CT-14 + CT-63** |
| M4-6 | acima do limite o fluxo vai direto de `aguardando_gestor` a `aprovada` (o diretor foi esquecido) | CT-13 (linha borda+1) |
| M4-7 | o limite **entregue** está em centavos, ou com um zero a mais, ou a chave do `.env` diverge do `config` | **CT-52** — único matador; todos os demais injetam o limite |
| M4-8 | a comparação é feita sobre o valor em memória e quebra com a string que o banco devolve | CT-13, CT-63 (`Dado` recarregado do banco) |

---

## Regra R5 — só o aprovador da etapa corrente aprova ou rejeita

> `RQ-06` · área **C**, perfil **completo** · técnica: **matriz papel × ação** +
> **estado × operação** (coluna `aprovar`)

```gherkin
    Esquema do Cenário: [CT-16] aprovar só vale em trânsito — coluna `aprovar` da matriz
      Dado uma solicitação de R$ 9.000,00 na situação <situacao>
      Quando <persona> tenta aprová-la
      Então o resultado é "<resultado>"
      E a situação passa a ser <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | situacao            | persona    | resultado | situacao_final      | etapas | # célula |
        | rascunho            | o gestor   | recusado  | rascunho            | 0      | inválida |
        | aguardando_gestor   | o gestor   | aceito    | aguardando_diretor  | 1      | válida   |
        | aguardando_diretor  | o diretor  | aceito    | aprovada            | 2      | válida   |
        | aprovada            | o diretor  | recusado  | aprovada            | 2      | inválida |
        | cancelada           | o gestor   | recusado  | cancelada           | 0      | inválida |

    Esquema do Cenário: [CT-17] a etapa corrente define quem decide, e mais ninguém
      Dado uma solicitação de R$ 9.000,00 na etapa pendente <etapa>, cujo solicitante,
        gestor do centro, gestor de outro centro e diretor são quatro pessoas distintas
      Quando <persona> tenta aprová-la
      Então o resultado é "<resultado>"
      E a situação passa a ser <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>
      E o número de e-mails de aprovação pendente enviados nesta tentativa é <emails>

      Exemplos:
        | etapa    | persona                  | resultado | situacao_final      | etapas | emails | # linha da decisão      |
        | gestor   | o gestor do centro       | aceito    | aguardando_diretor  | 1      | 1      | o aprovador da vez      |
        | gestor   | o diretor                | recusado  | aguardando_gestor   | 0      | 0      | etapa fora de ordem     |
        | gestor   | o gestor de outro centro | recusado  | aguardando_gestor   | 0      | 0      | gestor do centro errado |
        | gestor   | o solicitante            | recusado  | aguardando_gestor   | 0      | 0      | auto-aprovação          |
        | diretor  | o diretor                | aceito    | aprovada            | 2      | 0      | o aprovador da vez      |
        | diretor  | o gestor do centro       | recusado  | aguardando_diretor  | 1      | 0      | já decidiu, não decide  |
        | diretor  | o solicitante            | recusado  | aguardando_diretor  | 1      | 0      | auto-aprovação          |

    Cenário: [CT-53] (rev) cada etapa registra quem de fato decidiu
      Dado uma solicitação de R$ 9.000,00 do solicitante, no centro "Suprimentos" cujo
        gestor é Ana, e com os diretores Bruno e Duda — quatro pessoas distintas
      E que Ana já aprovou a etapa do gestor
      Quando Duda aprova a etapa do diretor
      Então a etapa "gestor" está gravada com decisor Ana, e não com o solicitante
      E a etapa "diretor" está gravada com decisor Duda, e não Ana, nem Bruno, nem o solicitante
      E a situação passa a ser "aprovada"

    Cenário: [CT-18] a barreira do aprovador vale para quem chama o model direto
      Dado uma solicitação de R$ 9.000,00 em "aguardando_gestor"
      Quando o gestor de outro centro de custo aprova a solicitação sem passar pela tela
      Então a aprovação é recusada
      E a situação continua "aguardando_gestor"
      E nenhuma etapa de aprovação foi gravada
      E nenhum e-mail de aprovação pendente foi enviado

    Cenário: [CT-19] na tela, quem não decide a etapa não encontra as ações de decisão
      Dado uma solicitação em "aguardando_gestor" e o solicitante autenticado
      Quando ele abre a listagem de solicitações
      Então as ações "Aprovar" e "Rejeitar" estão ocultas para essa solicitação
      E a ação "Cancelar" está visível

    @premissa  # P-07 / A-09: segregação de funções não foi pedida
    Cenário: [CT-20] o solicitante que é gestor do próprio centro decide a própria solicitação
      Dado um centro de custo cujo gestor é o próprio solicitante
      E uma solicitação de R$ 4.000,00 dele em "aguardando_gestor"
      Quando ele a aprova
      Então a situação passa a ser "aprovada"
      E existe uma etapa "gestor" com decisão "aprovada" decidida por ele
```

**Camada**: CT-16, CT-17, CT-18, CT-20 → `Feature`. CT-19 → componente Livewire
(`assertActionHidden` / `assertActionVisible` sobre `TestAction::make(...)->table($record)` —
confirmado em `vendor/filament/actions/src/Testing/TestAction.php:53` e
`TestsActions.php:217,231`).

> **A autorização é exercida na ação, não afirmada por `can()`.** Nenhum cenário aqui faz
> `expect($user->can(...))`: CT-16 a CT-18 **disparam** a decisão e afirmam sobre a situação e a
> contagem de etapas. Uma policy correta que o Resource nunca consulta passa em todo teste de
> `can()` — e é exatamente o furo que `.ai/rules/filament.md:17-29` descreve.

**CT-53 existe porque contar etapas não é o mesmo que verificar quem as assinou.** Antes dele,
**nenhum** cenário do conjunto afirmava o decisor de uma **aprovação** com pessoas distintas: CT-23
afirma o decisor de uma *rejeição*; CT-35 lê um histórico montado pela factory, não pelo caminho de
escrita; e CT-20 é estruturalmente incapaz de discriminar, porque nele o solicitante **é** o gestor
e os três identificadores coincidem — é o equivalente, em identidade, do valor redondo. Com isso,
a implementação que grava `decidido_por = centroCusto->gestor_id` (reusando o mesmo trecho de onde
saiu *"quem pode decidir"*) registrava a aprovação do diretor no nome do gestor **para sempre**, e
passava nos 51 cenários. RQ-13 diz *"quem aprovou cada etapa"*, e é a metade de escrita dessa
cláusula que CT-53 fecha.

**As quatro personas distintas no `Dado` de CT-17 são parte do oráculo**, pelo mesmo motivo: com
o solicitante e o gestor colapsados na mesma pessoa, as linhas "auto-aprovação" e "gestor do centro
errado" deixam de se distinguir.

**A matriz de estado é bidimensional; a autorização é tridimensional.** CT-16 varia a persona por
linha (o gestor em `rascunho` e `cancelada`, o diretor em `aprovada`), o que estreita o que cada
célula afirma. A terceira dimensão está declarada na
[Matriz Estado × Operação](#matriz-estado--operação), e a célula que mais importava dela —
*o gestor tentando reaprovar a etapa que ele mesmo já decidiu*, que é o chamador mais provável de
um botão que sobrou na tela — é a linha `diretor / o gestor do centro` de CT-17.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M5-1 | qualquer usuário com o papel `diretor` aprova **qualquer** etapa, inclusive a do gestor | CT-17 (linha "etapa fora de ordem") |
| M5-2 | qualquer gestor aprova, sem conferir se é o gestor **daquele** centro | **CT-17** (linha "gestor do centro errado"), CT-18 |
| M5-3 | a barreira vive só no `->visible()` da ação, não no model | **CT-18** |
| M5-4 | o gestor que já decidiu continua podendo decidir a etapa do diretor | CT-17 (linha "já decidiu") |
| M5-5 | a ação de decisão fica visível para o solicitante (affordance sem permissão) | CT-19 |
| M5-6 | aprovar é aceito em situação terminal e grava uma segunda etapa | CT-16 (linha `aprovada`) |
| M5-7 | a etapa é gravada com `decidido_por` = gestor do centro, em vez de quem chamou | **CT-53** — único matador |
| M5-8 | a tentativa recusada grava uma etapa de "tentativa" e só depois nega a transição | CT-17 (coluna `etapas` = 0 nas linhas recusadas) |

---

## Regra R6 — rejeitar exige justificativa e devolve a solicitação a `rascunho`

> `RQ-06`, `RQ-07`, `RQ-08` · área **A**, perfil **completo** · técnica: **EP** (justificativa:
> ausente ≠ nulo ≠ vazio ≠ só espaços) + **cenário de recusa que afirma o não-efeito**

```gherkin
    Esquema do Cenário: [CT-21] rejeitar não vale fora de trânsito — coluna `rejeitar` da matriz
      Dado uma solicitação na situação <situacao>
      Quando <persona> tenta rejeitá-la com a justificativa "Sem verba"
      Então a rejeição é recusada
      E a situação continua <situacao>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | situacao   | persona   | etapas | # célula |
        | rascunho   | o gestor  | 0      | inválida |
        | aprovada   | o diretor | 2      | inválida |
        | cancelada  | o gestor  | 0      | inválida |

    Esquema do Cenário: [CT-22] justificativa ausente, nula, vazia e só com espaços são recusadas
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      Quando o gestor do centro de custo tenta rejeitá-la com justificativa <entrada>
      Então a rejeição é recusada
      E a situação continua "aguardando_gestor"
      E nenhuma etapa de aprovação foi gravada
      E nenhum e-mail foi enviado

      Exemplos:
        | entrada    | # partição     |
        | ausente    | ausente        |
        | null       | nulo           |
        | ""         | vazio          |
        | "   "      | só espaços     |
        | "\n\t"     | só whitespace  |

    Cenário: [CT-23] o gestor rejeita, a solicitação volta a rascunho e o motivo fica registrado
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      Quando o gestor do centro de custo a rejeita com a justificativa "Sem verba no trimestre"
      Então a situação passa a ser "rascunho"
      E existe uma etapa "gestor" com decisão "rejeitada", decidida pelo gestor,
        com a justificativa "Sem verba no trimestre"
      E nenhum e-mail de aprovação pendente foi enviado a ninguém

    @premissa  # A-07: o card só dá a rejeição ao gestor; a do diretor é premissa
    Cenário: [CT-24] o diretor rejeita e a solicitação volta a rascunho, não à etapa do gestor
      Dado uma solicitação de R$ 9.000,00 em "aguardando_diretor", com a etapa do gestor aprovada
      Quando o diretor a rejeita com a justificativa "Fornecedor não homologado"
      Então a situação passa a ser "rascunho"
      E o histórico tem 2 etapas: "gestor/aprovada" e "diretor/rejeitada"
      E a etapa do diretor está gravada com a justificativa "Fornecedor não homologado"
        e com o diretor como decisor
      E nenhum e-mail de aprovação pendente foi enviado a ninguém

    Cenário: [CT-25] a modal de rejeição não submete sem justificativa
      Dado uma solicitação em "aguardando_gestor" e o gestor do centro autenticado
      Quando ele confirma a rejeição sem escrever o motivo
      Então o formulário da ação acusa erro no campo do motivo
      E a situação da solicitação continua "aguardando_gestor"
```

**Camada**: CT-21 a CT-24 → `Feature`. CT-25 → componente Livewire
(`callAction(TestAction::make('rejeitar')->table($record), ['justificativa' => ''])` →
`assertHasFormErrors(['justificativa'])`).

**Por que CT-22 e CT-25 são os dois.** CT-25 prova que a **tela** protege; CT-22 prova que o
**dado** está protegido para o próximo chamador — job, comando ou rota de API — que não passa pela
tela. Com só CT-25, o mutante *"a exigência mora apenas no `->required()` do campo"* fica vivo, e é
o furo que `.ai/rules/filament.md:17-29` nomeia. `"\n\t"` está na tabela porque `trim()` e
`preg_match('/\S/')` divergem de implementações que só comparam com `''`.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6-1 | a justificativa é exigida só pelo formulário, não pelo model | **CT-22** |
| M6-2 | `!== null` no lugar de "não vazia": `""` e `"   "` passam | CT-22 (linhas vazio, só espaços, só whitespace) |
| M6-3 | a rejeição grava a etapa **antes** de validar a justificativa | CT-22 (nenhuma etapa gravada) |
| M6-4 | a rejeição do diretor devolve a solicitação a `aguardando_gestor` | **CT-24** |
| M6-5 | a rejeição apaga o histórico das etapas anteriores | CT-24 (2 etapas) |
| M6-7 | só a rejeição do **gestor** grava a justificativa; a do diretor grava `null` | **CT-24** (a justificativa afirmada, e não só passada no `Quando`) |
| M6-6 | a rejeição notifica alguém (e-mail não pedido — A-11) | CT-23, CT-24 |

---

## Regra R7 — a rejeitada é reenviada e recomeça pelo gestor

> `RQ-08`, `RQ-09` · área **A**, perfil **completo** · técnica: **tabela estado × evento com
> 2-switch** (CT-26, CT-27, CT-29) e um **3-switch** (CT-28)

> **Por que 1-switch não basta.** Cobrir `rejeitar` e `enviar` isoladamente prova as duas
> transições e **nada** sobre o segundo giro, que é onde o ciclo novo herda o que o anterior
> deixou. O `Então` destes cenários é sobre **o destino do segundo envio** e sobre **quais
> aprovações do ciclo anterior ainda contam**.

```gherkin
    Cenário: [CT-26] reenviada depois da rejeição do gestor, volta para o gestor
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      E que o gestor a rejeitou com a justificativa "Sem verba"
      Quando o solicitante a envia de novo
      Então a situação passa a ser "aguardando_gestor"
      E o histórico continua com a etapa "gestor/rejeitada" do ciclo anterior
      E o gestor do centro de custo recebeu 2 e-mails de aprovação pendente no total

    Cenário: [CT-27] rejeitada pelo diretor, o reenvio volta ao GESTOR — a aprovação dele não conta
      Dado uma solicitação de R$ 9.000,00 em "aguardando_diretor", com a etapa do gestor aprovada
      E que o diretor a rejeitou com a justificativa "Fornecedor não homologado"
      Quando o solicitante a envia de novo
      Então a situação passa a ser "aguardando_gestor", e não "aguardando_diretor"
      E o histórico tem as 2 etapas do ciclo anterior: "gestor/aprovada" e "diretor/rejeitada"
      E o gestor do centro de custo recebeu um e-mail de aprovação pendente

    Cenário: [CT-28] no segundo ciclo acima do limite, o diretor volta a ser exigido
      Dado uma solicitação de R$ 9.000,00 rejeitada pelo diretor e reenviada,
        agora em "aguardando_gestor" com 2 etapas no histórico
      Quando o gestor do centro de custo a aprova
      Então a situação passa a ser "aguardando_diretor"
      E o histórico tem 3 etapas, na ordem: "gestor/aprovada", "diretor/rejeitada", "gestor/aprovada"
      E o diretor recebeu um e-mail de aprovação pendente neste ciclo

    Cenário: [CT-29] o valor corrigido entre os ciclos muda a alçada do ciclo novo
      Dado uma solicitação de R$ 9.000,00 rejeitada pelo diretor e de volta a "rascunho"
      E que o solicitante corrigiu o valor para R$ 4.999,99
      E que ele a enviou de novo, ficando em "aguardando_gestor"
      Quando o gestor do centro de custo a aprova
      Então a situação passa a ser "aprovada"
      E o histórico tem 3 etapas, e nenhuma delas é do diretor no ciclo novo
      E nenhum e-mail de aprovação pendente foi enviado a nenhum diretor neste ciclo

    Cenário: [CT-55] (rev) o gestor da vez é o de agora, não o do ciclo anterior
      Dado uma solicitação de R$ 4.000,00 no centro "Suprimentos", cujo gestor é Ana,
        em "aguardando_gestor"
      E que Ana a rejeitou com a justificativa "Sem verba", deixando-a em "rascunho"
      E que o gestor de "Suprimentos" passou a ser Caio
      Quando o solicitante a envia de novo
      Então Caio recebe o e-mail de aprovação pendente
      E Ana não recebe nenhum e-mail
      E a situação passa a ser "aguardando_gestor"
```

**Camada**: todos `Feature`.

**A ação sob teste nunca fica no `Dado`.** Em CT-15 e CT-29 o reenvio estava embutido no arranjo
(*"corrigiu o valor **e a enviou de novo**"*); se ele quebrasse, o cenário erraria no arranjo em vez
de falhar na asserção, e a mensagem apontaria para a alçada em vez do reenvio. Os dois foram
reescritos com o reenvio como passo próprio do `Dado`, separado da correção do valor, e o `Quando`
reservado para a aprovação — que é a transição cujo destino o cenário afirma.

**O que cada um mata que os outros não matam.** CT-26 é o 2-switch barato: mata *"o reenvio
restaura a situação anterior à rejeição"* no caminho de um nível. CT-27 é o caro, e é o que a skill
nomeia: com a etapa do gestor **já aprovada** no histórico, uma implementação que decide o destino
do envio olhando *"existe etapa de gestor aprovada?"* manda a solicitação direto para
`aguardando_diretor`, pulando a aprovação do gestor — e **passa** em CT-26. CT-28 é o terceiro
evento, e prova que a alçada não se dá por satisfeita com a aprovação de diretor do ciclo velho.
CT-29 cruza o 2-switch com a **edição do valor**: é o único cenário em que a alçada do ciclo 2
difere da do ciclo 1. **CT-55 cruza o 2-switch com a mudança da configuração de aprovação** — e é a
dimensão que faltava: os quatro primeiros variam *o valor* entre os giros e mantêm *o gestor* fixo,
o que deixa passar inteira a implementação que desnormaliza o aprovador no primeiro envio.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M7-1 | o reenvio recupera a situação de antes da rejeição (`aguardando_diretor`) | **CT-27** |
| M7-2 | o destino do envio é decidido por *"já existe etapa de gestor aprovada?"* em vez de recomeçar | **CT-27**, CT-28 |
| M7-3 | a rejeição apaga as etapas para "limpar" o ciclo | CT-26, CT-27, CT-28 |
| M7-4 | o segundo ciclo acima do limite não exige mais o diretor (a etapa antiga conta) | **CT-28** |
| M7-5 | a alçada foi congelada no primeiro envio e ignora o valor corrigido | **CT-29** |
| M7-6 | o reenvio não notifica ninguém (a notificação só existe no primeiro envio) | CT-26 (2 e-mails), CT-27 |
| M7-7 | o aprovador é desnormalizado no primeiro envio, e o **ex-gestor** continua decidindo e recebendo o e-mail | **CT-55** — único matador; CT-26…CT-29 mantêm o gestor fixo entre os giros |

---

## Regra R8 — cancelar em trânsito; `aprovada` e `cancelada` não aceitam escrita

> `RQ-10`, `RQ-11` · área **A**, perfil **completo** · técnica: **estado × operação** (coluna
> `cancelar`) + **idempotência ancorada no agregado**

```gherkin
    @premissa  # A-06: em rascunho o verbo é excluir, não cancelar
    Esquema do Cenário: [CT-30] cancelar só vale em trânsito — coluna `cancelar` da matriz
      Dado uma solicitação do solicitante na situação <situacao>
      Quando o solicitante tenta cancelá-la
      Então o resultado é "<resultado>"
      E a situação passa a ser <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | situacao            | resultado | situacao_final      | etapas | # célula |
        | rascunho            | recusado  | rascunho            | 0      | inválida |
        | aguardando_gestor   | aceito    | cancelada           | 0      | válida   |
        | aguardando_diretor  | aceito    | cancelada           | 1      | válida   |
        | aprovada            | recusado  | aprovada            | 1      | inválida |
        | cancelada           | recusado  | cancelada           | 0      | inválida |

    Cenário: [CT-31] quem não é o solicitante não cancela, mesmo chamando o model direto
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      Quando o gestor do centro de custo tenta cancelá-la
      Então o cancelamento é recusado
      E a situação continua "aguardando_gestor"
      E o número de etapas de aprovação gravadas continua 0
      E nenhum e-mail foi enviado

    Cenário: [CT-32] o cancelamento não é decisão de aprovador e não notifica ninguém
      Dado uma solicitação de R$ 9.000,00 em "aguardando_diretor", com a etapa do gestor aprovada
      Quando o solicitante a cancela
      Então a situação passa a ser "cancelada"
      E o histórico continua com 1 etapa, a do gestor
      E nenhum e-mail foi enviado a ninguém

    Cenário: [CT-33] cancelar duas vezes deixa a solicitação no mesmo estado
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      E que o solicitante já a cancelou
      Quando o solicitante a cancela de novo
      Então o segundo cancelamento é recusado
      E a situação persistida continua "cancelada"
      E o número de etapas de aprovação gravadas continua 0
```

**Camada**: todos `Feature`.

> **A idempotência de CT-33 está ancorada no agregado persistido**, não no retorno da chamada: o
> `Então` afirma sobre a situação **recarregada do banco** da mesma solicitação, depois de duas
> chamadas ao **mesmo registro**. Afirmar sobre o valor devolvido por duas chamadas passaria por
> construção e o mutante *"cancelar acumula efeito"* não seria nem expressável.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M8-1 | cancelar vale em `rascunho` também (leitura literal de "a qualquer momento") | CT-30 (linha `rascunho`) |
| M8-2 | cancelar vale em `aprovada` — o "antes da aprovação final" não foi implementado | **CT-30** (linha `aprovada`) |
| M8-3 | cancelar grava uma etapa de decisão | CT-32 |
| M8-4 | o cancelamento não confere a identidade de quem cancela | CT-31 |
| M8-5 | cancelar é idempotente e responde sucesso na segunda vez, avançando algo | CT-33 |

---

## Regra R9 — a tela mostra a situação de toda solicitação e quem decidiu cada etapa

> `RQ-12`, `RQ-13` · área **F**, perfil **padrão** · técnica: **EP exaustiva do enum** (não se
> amostra) + **ordenação com empate**
> Técnica escalada acima do perfil: EP exaustiva em vez de amostrada — cobrir 3 dos 5 valores
> permite exatamente o defeito que importa, a tela dizer "Aprovada" faltando uma etapa.

```gherkin
    Esquema do Cenário: [CT-34] a listagem mostra o rótulo de cada uma das cinco situações
      Dado uma solicitação na situação <situacao>
      Quando o solicitante abre a listagem de solicitações
      Então a solicitação aparece na listagem
      E a situação exibida para ela é "<rotulo>"

      Exemplos:
        | situacao            | rotulo              | # partição do enum |
        | rascunho            | Rascunho            | 1 de 5             |
        | aguardando_gestor   | Aguardando gestor   | 2 de 5             |
        | aguardando_diretor  | Aguardando diretor  | 3 de 5             |
        | aprovada            | Aprovada            | 4 de 5             |
        | cancelada           | Cancelada           | 5 de 5             |

    Cenário: [CT-35] o detalhe mostra quem decidiu cada etapa, quando e por quê
      Dado uma solicitação de R$ 9.000,00 aprovada pelo gestor "Ana" e rejeitada pelo
        diretor "Bruno" com a justificativa "Fornecedor não homologado"
      Quando o solicitante abre o detalhe dessa solicitação
      Então a situação exibida é "Rascunho"
      E o histórico mostra a etapa do gestor decidida por "Ana" com decisão "Aprovada"
      E o histórico mostra a etapa do diretor decidida por "Bruno" com decisão "Rejeitada"
        e a justificativa "Fornecedor não homologado"

    Cenário: [CT-36] o histórico sai na ordem das etapas mesmo com o instante empatado
      Dado o tempo congelado em 2026-08-14 10:00:00
      E uma solicitação de R$ 9.000,00 cuja etapa de DIRETOR foi inserida primeiro
        e cuja etapa de GESTOR foi inserida depois, ambas nesse mesmo instante
      Quando o solicitante abre o detalhe dessa solicitação
      Então a primeira etapa do histórico é a do gestor
      E a segunda é a do diretor

    Cenário: [CT-57] (rev) o detalhe de uma solicitação aprovada mostra as duas assinaturas
      Dado uma solicitação de R$ 9.000,00 aprovada pelo gestor Ana e depois pelo diretor Bruno
      Quando o solicitante abre o detalhe dessa solicitação
      Então a situação exibida é "Aprovada"
      E o histórico mostra a etapa do gestor decidida por "Ana" com decisão "Aprovada"
      E o histórico mostra a etapa do diretor decidida por "Bruno" com decisão "Aprovada"

    Cenário: [CT-61] (rev) o aprovador encontra na listagem a solicitação que não é dele
      Dado uma solicitação do solicitante em "aguardando_gestor", no centro cujo gestor é Ana
      E uma solicitação de outro solicitante, em "rascunho", num centro que Ana não gerencia
      Quando Ana abre a listagem de solicitações
      Então a solicitação em "aguardando_gestor" aparece para Ana
      E a situação exibida para ela é "Aguardando gestor"
```

**Camada**: todos componente Livewire — CT-34 sobre a página de listagem
(`assertCanSeeTableRecords` + `assertTableColumnFormattedStateSet('situacao', ...)`, confirmado em
`vendor/filament/tables/src/Testing/TestsColumns.php:301` e `TestsRecords.php:20`); CT-35 e CT-36
sobre a página `ViewRecord`.

**Nenhum destes cenários usa `assertSee` de texto de layout como oráculo.** CT-34 afirma sobre o
**estado formatado da coluna**, o que passa quando o rótulo está certo e falha quando está errado —
diferente de `assertSee('Solicitações')`, que fica verde em qualquer estado da página.

**CT-36 é o cenário do empate — e a ordem de inserção faz parte do oráculo.** Dois registros com o
**mesmo** `created_at` são o único par que distingue uma ordenação determinística de uma que
depende da ordem física de inserção. Mas isso só discrimina se a fixture inserir a etapa **na ordem
contrária à esperada**: com o gestor inserido primeiro, `orderBy('created_at')` sem desempate
devolve gestor-antes-de-diretor por acidente, e as duas implementações passam. Por isso o `Dado`
insere a etapa do **diretor primeiro** e o `Então` continua exigindo o gestor em primeiro lugar —
é o que torna M9-5 falsificável, e sem essa inversão o item *ordenação* do checklist era um falso ✅.

**CT-57 fecha a coluna `visualizar` na tela de detalhe.** As 5 células de `visualizar` da matriz
estavam todas atribuídas a CT-34, que é a **listagem**. A operação de leitura de um registro é a
rota `.../{record}`, e nela só havia CT-35 (situação final `rascunho`) e CT-36 — ou seja, o caso
central de RQ-13, *ver quem aprovou cada etapa de uma solicitação **aprovada***, não tinha cenário
em lugar nenhum. A matriz agora declara as duas leituras separadamente.

**CT-61 é a resposta à pergunta que ninguém tinha feito (P-13).** Todos os cenários de listagem
eram *"o solicitante abre a listagem"* — das próprias solicitações. Uma implementação que aplique
um recorte por solicitante na consulta base passa em CT-34, CT-19, CT-44 e CT-45 e deixa **todo
aprovador com a tela vazia**: falha total do fluxo, que só apareceria em navegador, num único
cenário, num único estado. RQ-12 diz *"mostrar na tela o status atual"* e não diz para quem; a
premissa adotada está em **P-13**.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M9-1 | o rótulo de `aguardando_diretor` cai no `default` do `match` e sai como "Aprovada" | **CT-34** (linha 3 de 5) |
| M9-2 | o rótulo exibido é o valor bruto do enum (`aguardando_gestor`) | CT-34 |
| M9-3 | o histórico mostra a decisão mas não quem decidiu, ou não mostra a justificativa | **CT-35** |
| M9-4 | a cor do badge não corresponde à situação | ⚠️ **sem matador** — o requisito não determina cor (**P-04**). `assertSee` não valida cor (`.ai/rules/testes-browser.md:54-56`); tentado derivar de RQ-12 e ele só exige o *status*. Screenshot de badge não é proporcional ao risco |
| M9-5 | o histórico sai em ordem arbitrária quando as etapas empatam no `created_at` (`orderBy` sem desempate por chave) | **CT-36** (com a etapa do diretor inserida primeiro) |
| M9-6 | o detalhe de uma solicitação **aprovada** mostra a situação e omite as assinaturas | **CT-57** |
| M9-7 | a consulta base da listagem recorta por solicitante, e o aprovador vê a tela vazia | **CT-61** — único matador |

---

## Regra R10 — a notificação vai a exatamente os aprovadores da etapa pendente, uma só vez

> `RQ-14` · área **D**, perfil **completo** · técnica: **rastreio de efeito** — aconteceu / não
> aconteceu quando não devia / aconteceu uma só vez / **atomicidade em duas direções**

> **O teto do perfil é consumido inteiro por esta regra, e há estouro declarado.** O rastreio de
> efeito já exige quatro cenários; a atomicidade aqui precisa de **dois**, porque uma injeção só
> não distingue as implementações (ver CT-40/CT-41). São 5 cenários com teto 5, e nenhum deles
> divide o teto com fronteira ou partição de domínio: **o discriminador desta regra é
> `com diretor × sem diretor`, e ele aparece como coluna em cada tabela de `Exemplos`** — é assim
> que nenhum par `(partição, efeito)` fica sem cenário sem inflar a contagem.

```gherkin
    Esquema do Cenário: [CT-37] o próximo aprovador é notificado — nos dois ramos da alçada
      Dado dois centros de custo, "Suprimentos" (gestor Ana) e "TI" (gestor Caio),
        e dois diretores, Bruno e Duda
      E uma solicitação de <valor> no centro "Suprimentos"
      Quando <evento>
      Então <notificados> recebem o aviso de aprovação pendente
      E o canal de entrega desse aviso inclui "mail"
      E <nao_notificados> não recebem nenhum aviso

      Exemplos:
        | valor      | evento                        | notificados      | nao_notificados        | # ramo       |
        | 4.999,99   | o solicitante a envia         | Ana              | Caio, Bruno, Duda      | sem diretor  |
        | 5.000,01   | o solicitante a envia         | Ana              | Caio, Bruno, Duda      | com diretor  |
        | 5.000,01   | Ana a aprova                  | Bruno e Duda     | Ana, Caio              | com diretor  |

    Esquema do Cenário: [CT-38] nenhum e-mail quando não há próxima etapa — nos dois ramos
      Dado uma solicitação de <valor> na situação <situacao>
      Quando <evento>
      Então nenhum e-mail de aprovação pendente foi enviado a ninguém
      E a situação passa a ser <situacao_final>

      Exemplos:
        | valor      | situacao            | evento                              | situacao_final | # ramo / efeito              |
        | 4.999,99   | aguardando_gestor   | o gestor a aprova                   | aprovada       | sem diretor, aprovação final |
        | 5.000,01   | aguardando_diretor  | o diretor a aprova                  | aprovada       | com diretor, aprovação final |
        | 4.999,99   | aguardando_gestor   | o gestor a rejeita com motivo       | rascunho       | sem diretor, rejeição        |
        | 5.000,01   | aguardando_diretor  | o diretor a rejeita com motivo      | rascunho       | com diretor, rejeição        |
        | 5.000,01   | aguardando_diretor  | o solicitante a cancela             | cancelada      | com diretor, cancelamento    |

    Esquema do Cenário: [CT-39] a segunda tentativa não manda um segundo e-mail — nos dois ramos
      Dado uma solicitação de <valor> na situação <situacao>
      Quando <persona> repete a mesma ação duas vezes sobre o mesmo registro
      Então o número de e-mails de aprovação pendente enviados é 1
      E a situação persistida é <situacao_final>
      E o número de etapas de aprovação gravadas é <etapas>

      Exemplos:
        | valor      | situacao            | persona          | situacao_final      | etapas | # ramo       |
        | 4.999,99   | rascunho            | o solicitante    | aguardando_gestor   | 0      | sem diretor  |
        | 5.000,01   | rascunho            | o solicitante    | aguardando_gestor   | 0      | com diretor  |
        | 5.000,01   | aguardando_gestor   | o gestor         | aguardando_diretor  | 1      | com diretor  |

    Esquema do Cenário: [CT-40] gravação que falha depois do ponto de notificação não deixa e-mail escapar
      Dado uma solicitação de <valor> na situação <situacao>
      E que a gravação da etapa de aprovação foi instrumentada para falhar
      Quando <persona> a aprova
      Então a operação falha
      E a situação persistida continua <situacao>
      E nenhuma etapa de aprovação foi gravada
      E nenhum e-mail de aprovação pendente foi enviado

      Exemplos:
        | valor      | situacao            | persona    | # ramo       |
        | 4.999,99   | aguardando_gestor   | o gestor   | sem diretor  |
        | 5.000,01   | aguardando_gestor   | o gestor   | com diretor  |
        | 5.000,01   | aguardando_diretor  | o diretor  | com diretor  |

    @premissa  # P-06 / A-17: que o e-mail que falha desfaça a transição é premissa
    Esquema do Cenário: [CT-41] e-mail que falha não deixa a transição aplicada pela metade
      Dado uma solicitação de <valor> na situação <situacao>
      E que o envio de e-mail foi instrumentado para lançar exceção
      Quando <persona> executa <evento>
      Então a operação falha
      E a situação persistida continua <situacao>
      E o número de etapas de aprovação gravadas continua <etapas>

      Exemplos:
        | valor      | situacao            | persona        | evento    | etapas | # ramo       |
        | 4.999,99   | rascunho            | o solicitante  | o envio   | 0      | sem diretor  |
        | 5.000,01   | aguardando_gestor   | o gestor       | a aprovação | 1    | com diretor  |
```

**Camada**: todos `Feature`, com `Notification::fake()`.

**Por que a atomicidade precisa das duas direções — e por que uma só é um falso ✅.**
`assertNothingSent()` num caminho de **pré-validação** (justificativa vazia, situação errada, gente
errada) não prova nada: ali nada seria enviado em nenhuma implementação. A injeção tem de estar
**depois** do ponto de notificação. Mas *"depois"* depende da ordem dos statements, que é
implementação — e é aí que uma injeção só cobre pela metade:

| Ordem real na implementação | CT-40 (falha na gravação da etapa) | CT-41 (falha no e-mail) |
|---|---|---|
| notifica → grava a etapa | **mata** o mutante | falha antes de gravar — mata também |
| grava a etapa → notifica | injeção cai **antes** do e-mail: falso ✅ | **mata** — é o único matador |
| notifica fora da transação, por último | falso ✅ | **mata** |

Escrever só CT-40 deixaria o mutante *"a notificação está fora da transação"* vivo em duas das três
ordens plausíveis. **Arneses tentados e usados**: (a) `EtapaAprovacao::creating(fn () => throw ...)`
— o "evento de model lançando" da lista de arneses da skill; (b) um canal de notificação que lança,
registrado antes da ação. **Arnês tentado e recusado**: `Notification::fake()` +
`assertNothingSent()` sozinho no caminho de justificativa vazia — é pré-validação e não distingue
nada; ele continua em CT-22, mas como asserção de não-efeito de **recusa**, não como prova de
atomicidade.

**Por que dois diretores no setup.** Um só não distingue *"notifica todos os diretores"* de
*"notifica o primeiro que achar"* (A-03 diz **todas** são notificadas). E os dois centros de custo
existem para o mutante *"notifica qualquer gestor"*: sem o gestor Caio no setup, `assertSentTo(Ana)`
fica verde com a implementação que notifica a lista inteira de gestores.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M10-1 | a chamada de notificação foi removida ou nunca escrita no reenvio | CT-37, CT-26 |
| M10-2 | notifica o gestor **e** o diretor já no envio, adiantando a etapa | **CT-37** (linha "com diretor", envio) |
| M10-3 | notifica na aprovação **final** (ninguém é o próximo aprovador) | **CT-38** (linhas de aprovação final, nos dois ramos) |
| M10-4 | notifica na rejeição ou no cancelamento — não pedido (A-11) | CT-38 (linhas de rejeição e cancelamento) |
| M10-5 | notifica **um** diretor em vez de todos, ou notifica todos os gestores | **CT-37** (linha "Bruno e Duda"; `Caio` em não notificados) |
| M10-9 | a notificação é entregue só por `database` (o sininho do painel) e **nunca por e-mail** | **CT-37** (a cláusula do canal). Sem ela, `assertSentTo` fica verde e metade de RQ-14 — *"por e-mail"* — não tem oráculo |
| M10-6 | o e-mail sai sem o valor, sem a descrição e sem o link | ⚠️ **sem matador** — o requisito determina destinatário e canal, não conteúdo (**P-05**). Tentado derivar de RQ-14 e ele para em "notificar o próximo aprovador"; afirmar sobre o corpo seria testar o PRD |
| M10-7 | a notificação é despachada **antes** ou **fora** da transação, e o e-mail sai quando a gravação falha | **CT-40 + CT-41** (as duas direções) |
| M10-8 | o duplo clique manda dois e-mails para a mesma etapa | CT-39 |

---

## Regra R11 — duas decisões simultâneas gravam uma decisão

> `RQ-06`, `RQ-13` (*"quem aprovou cada etapa"* — uma decisão por etapa) + linha **contador/limite**
> do checklist de taxonomia · área **A**, perfil **completo** · técnica: **concorrência** +
> **idempotência ancorada no agregado persistido**

```gherkin
    Cenário: [CT-42] dois diretores decidindo ao mesmo tempo gravam uma decisão só
      Dado uma solicitação de R$ 9.000,00 em "aguardando_diretor"
      E que dois diretores carregaram a solicitação antes de qualquer decisão
      Quando os dois a aprovam sem recarregar
      Então a situação persistida é "aprovada"
      E o número de etapas de decisão do diretor gravadas é 1
      E a segunda aprovação foi recusada

    Esquema do Cenário: [CT-43] entre decisões opostas, vale a que chegou primeiro
      Dado uma solicitação de R$ 4.000,00 em "aguardando_gestor"
      E que o gestor carregou a solicitação em duas abas, antes de qualquer escrita
      Quando ele dispara <primeira> e, sem recarregar, <segunda>
      Então a situação persistida é <situacao_final>
      E o número de etapas de aprovação gravadas é 1
      E a decisão gravada é "<decisao>"
      E a segunda decisão foi recusada

      Exemplos:
        | primeira    | segunda     | situacao_final | decisao   | # ordem            |
        | a aprovação | a rejeição  | aprovada       | aprovada  | aprovar primeiro   |
        | a rejeição  | a aprovação | rascunho       | rejeitada | rejeitar primeiro  |
```

**Camada**: `Feature`.

> **O agregado é a solicitação persistida.** O `Então` afirma sobre a situação **recarregada** e
> sobre a contagem de etapas **do mesmo registro** depois das duas chamadas — não sobre o retorno
> de cada chamada. Duas instâncias carregadas **antes** de qualquer escrita é o que reproduz a
> janela do check-then-act dentro de um processo: uma implementação que compara a situação
> **em memória** e depois grava vê `aguardando_diretor` nas duas instâncias e grava duas etapas.

**A ordem das duas chamadas é parte do oráculo de CT-43.** Antes, o cenário dizia *"aprova numa aba
e rejeita na outra"* e fixava o resultado em `aprovada` — o que só vale se a aprovação for a
primeira. Uma implementação **correta** que processasse a rejeição primeiro devolveria `rascunho` e
falharia o cenário. Com as duas linhas do `Esquema`, o oráculo é *"vale a que chegou primeiro"*, que
é a regra de fato, e a segunda linha mata o mutante *"aprovar sempre vence rejeitar"* — que a
versão anterior não só não matava, como premiava.

**O que estes dois cenários provam, e o que não provam.** Eles falsificam o check-then-act **em
memória, dentro de um processo**: as duas instâncias foram carregadas antes de qualquer escrita, e
a implementação ingênua vê o estado velho nas duas. O que eles **não** provam é o isolamento sob
duas conexões reais — está em **M11-3**, lacuna declarada, com o que foi tentado.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M11-1 | a transição é check-then-act sobre o estado em memória (`if` + `save()`) | **CT-42**, CT-43 |
| M11-2 | a etapa é gravada **antes** de a transição de situação vencer, deixando etapa órfã | CT-42 (1 etapa), CT-43 |
| M11-3 | a transição condicional existe mas não é atômica sob isolamento real de duas conexões | ⚠️ **sem matador** — não expressável neste arnês. Tentado: segundo handle de conexão (`DB::connection()` com `DB_DATABASE=:memory:` abre **outro** banco, não outra sessão do mesmo) e `RefreshDatabase`, que embrulha o caso numa transação e serializa as escritas. O mutante que **é** alcançável (M11-1) está morto por CT-42 |
| M11-4 | a segunda chamada é silenciosamente tratada como sucesso e a situação avança duas casas | CT-42 (situação = `aprovada`, não além) |
| M11-5 | a decisão que vence é sempre a aprovação, independentemente de qual chegou primeiro | **CT-43** (linha "rejeitar primeiro") |

---

## Regra R12 — o dado e o aprovador pertencem à organização corrente

> Origem: dimensões **D** e **T** da varredura + invariante de `wikis/convencoes.md` que A-01
> invoca · área **C**, perfil **completo** · técnica: **isolamento por tenant** + **IDOR entre
> tenants**
> **Suíte `FeatureTenancy`** (`Tests\TenancyTestCase`): `permission.teams` tem de estar ligada em
> `createApplication()`, antes das migrations — `tests/Pest.php:48-65`. Ligar num `beforeEach`
> seria tarde.

```gherkin
    Cenário: [CT-44] a listagem de uma organização não mostra a solicitação de outra
      Dado uma solicitação na organização "Acme" e uma na organização "Globex"
      E o solicitante da Acme autenticado no painel da Acme
      Quando ele abre a listagem de solicitações
      Então a solicitação da Acme aparece
      E a solicitação da Globex não aparece

    Cenário: [CT-45] o identificador de uma solicitação de outra organização não abre
      Dado uma solicitação na organização "Globex"
      E o solicitante da Acme autenticado no painel da Acme
      Quando ele acessa o detalhe pelo identificador da solicitação da Globex
      Então o acesso é recusado com status 404

    Cenário: [CT-46] o diretor notificado é o da organização da solicitação
      Dado um diretor na organização "Acme" e outro na organização "Globex"
      E uma solicitação de R$ 9.000,00 na Acme, em "aguardando_gestor"
      Quando o gestor do centro de custo da Acme a aprova
      Então o diretor da Acme recebe o e-mail de aprovação pendente
      E o diretor da Globex não recebe nenhum e-mail
```

**Camada**: CT-44 → componente Livewire com `noPainelDa($tenant)` antes
(`tests/Pest.php:210-215` — sem `setTenant` o caso cai no ramo fail-closed, sem
`setPermissionsTeamId` o papel é gravado no contexto global). CT-45, CT-46 → `Feature`.

**CT-46 é o cenário mais caro de errar da feature.** Com `permission.teams` ligada, resolver
"quem tem o papel `diretor`" **dentro** da notificação enfileirada devolve os diretores do contexto
que estiver fixado no `PermissionRegistrar` — e quem o fixa é um middleware, que não roda em worker
de fila. Nenhuma das duas falhas possíveis (lista vazia, ou lista da organização errada) move
status HTTP nem gera erro: uma trava o fluxo em silêncio, a outra manda descrição e valor de uma
compra para fora da organização.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M12-1 | a listagem consulta o model direto, sem o recorte por organização | CT-44 |
| M12-2 | o route binding resolve pelo identificador sem recortar por organização (IDOR entre tenants) | **CT-45** |
| M12-3 | os aprovadores são resolvidos dentro da notificação enfileirada, fora do contexto | **CT-46** |
| M12-4 | sem organização no contexto, a consulta falha **aberta** e devolve a base inteira | CT-44, CT-45 |

---

## Regra R13 — centro de custo é administração da organização, e o nome é único nela

> `RQ-04`, A-08 · área **G + C**, perfil **completo** (herda o maior) · técnica: **matriz papel ×
> ação** + **normalização de identidade** + **unicidade contra si mesmo**

```gherkin
    Cenário: [CT-47] o usuário comum não recebe a permissão de mexer em centro de custo
      Dado os papéis semeados
      Quando se lê a matriz de permissões do papel do usuário comum
      Então ela não contém a permissão de criar centro de custo
      E ela não contém a permissão de editar centro de custo
      E ela contém a permissão de criar solicitação de compra

    Esquema do Cenário: [CT-48] o usuário comum é barrado em TODAS as telas de centro de custo
      Dado um usuário comum autenticado e um centro de custo "Suprimentos" já cadastrado
      Quando ele acessa <tela>
      Então o acesso é recusado com status 403

      Exemplos:
        | tela                                | # rota    |
        | a listagem de centros de custo      | index     |
        | a tela de cadastro de centro de custo | create  |
        | a tela de edição de "Suprimentos"   | edit      |

    Cenário: [CT-62] (rev) o usuário comum não GRAVA centro de custo nem se nomeia gestor
      Dado um usuário comum autenticado e um centro de custo "Suprimentos" cujo gestor é Ana
      Quando ele tenta gravar um centro de custo novo apontando a si mesmo como gestor
      Então a gravação é recusada
      E o número de centros de custo continua 1
      E o gestor de "Suprimentos" continua sendo Ana

    Cenário: [CT-49] o formulário grava o centro de custo com o gestor escolhido
      Dado um administrador da organização "Acme" autenticado e uma usuária "Ana" da Acme
      Quando ele grava um centro de custo com nome "Suprimentos" e gestor "Ana"
      Então existe um centro de custo "Suprimentos" cujo gestor é "Ana"
      E esse centro de custo pertence à organização "Acme"

    Esquema do Cenário: [CT-59] (rev) o centro de custo com solicitação vinculada não some em silêncio
      Dado um centro de custo "Suprimentos", cujo gestor é Ana
      E <vinculo>
      Quando o administrador da organização tenta excluí-lo
      Então o resultado é "<resultado>"
      E o número de centros de custo que restam é <restam>
      E o número de solicitações que restam é <solicitacoes>

      Exemplos:
        | vinculo                                            | resultado | restam | solicitacoes | # caso            |
        | nenhuma solicitação nele                            | aceito    | 0      | 0            | sem vínculo       |
        | uma solicitação em "rascunho" nele                  | recusado  | 1      | 1            | vínculo em repouso |
        | uma solicitação em "aguardando_gestor" nele         | recusado  | 1      | 1            | vínculo em trânsito |

    Esquema do Cenário: [CT-50] o nome é único na organização, e salvar o próprio registro passa
      Dado um centro de custo "Suprimentos" na organização "Acme"
      Quando o administrador <acao>
      Então o resultado é "<resultado>"
      E o número de centros de custo chamados "Suprimentos" na Acme é <quantos>

      Exemplos:
        | acao                                                | resultado | quantos | # caso                      |
        | cria outro "Suprimentos" na Acme                     | recusado  | 1       | colisão                     |
        | cria "Suprimentos" na Globex                         | aceito    | 1       | outra organização           |
        | salva o próprio "Suprimentos" trocando só o gestor    | aceito    | 1       | unicidade contra si mesmo   |
        | salva o próprio "Suprimentos" sem alterar nada        | aceito    | 1       | editar sem alterar nada     |
        | exclui "Suprimentos" e cria "Suprimentos" de novo     | aceito    | 1       | criar → excluir → recriar   |

    @premissa  # P-09 / A-19: a comparação é a do banco; o requisito não determina
    Esquema do Cenário: [CT-51] variações de caixa, acento e espaço nas bordas são o mesmo nome
      Dado um centro de custo <existente> na organização "Acme"
      Quando o administrador tenta criar um centro de custo chamado <entrada> na Acme
      Então o resultado é "<resultado>"
      E o nome gravado é <nome_gravado>
      E o número de centros de custo na Acme é <quantos>

      Exemplos:
        | existente      | entrada          | resultado | nome_gravado    | quantos | # variação          |
        | "Suprimentos"  | "suprimentos"    | recusado  | Suprimentos     | 1       | caixa               |
        | "Suprimentos"  | "  Suprimentos " | recusado  | Suprimentos     | 1       | espaços nas bordas  |
        | "Suprimentos"  | "SUPRIMENTOS"    | recusado  | Suprimentos     | 1       | caixa alta          |
        | "Manutenção"   | "MANUTENÇÃO"     | recusado  | Manutenção      | 1       | acento + caixa      |
        | "Suprimentos"  | " Suprimentos TI " | aceito  | Suprimentos TI  | 2       | nome outro, aparado |
```

**Camada**: CT-47 → `Feature` (leitura da matriz depois dos seeders). CT-48 → `Feature` (`GET` →
`assertForbidden`). CT-49, CT-50, CT-51 → componente Livewire — **CT-49 é o cenário que satisfaz o
[gate de tela de escrita](#gate-de-tela-de-escrita) da rota `create` de centro de custo**, e CT-50
o da rota `edit`.

**CT-47, CT-48 e CT-62 são três coisas diferentes, e as duas primeiras sozinhas não bastavam.**
CT-47 lê a matriz — mata *"a entidade não entrou na lista de subtração"*, que é a falha que **não
gera erro nenhum** (`.ai/rules/filament.md:44-56`: os seeders rodam, tudo fica verde, e todo
usuário comum vira administrador da organização). Mas CT-47 é `can()` invertido, e o próprio
documento proíbe `can()` como oráculo único. CT-48 **exerce** a recusa — e antes exercia **uma só
rota**, o `index`: uma implementação que nega `viewAny` e libera `create` passava, que é
exatamente a escalada que A-08 chama de *"real e silenciosa"*, porque **quem cria o centro escolhe
o `gestor_id`**. **CT-62** é a metade de escrita: a ação perigosa disparada pela persona errada,
com o não-efeito afirmado. Sem ele, a ação que A-08 identifica como o risco da entrega não era
exercida por ninguém que não pudesse fazê-la.

**CT-59 fecha a coluna `excluir` de `CentroCusto`, que não existia.** R13 cobria criar, editar e a
matriz de permissões; excluir um centro de custo **com solicitação vinculada** não tinha cenário —
nem a recusa, nem o efeito sobre as solicitações em trânsito daquele centro, que ficariam sem
aprovador. É a mesma classe de defeito de CT-58, do outro lado da FK.

**As duas linhas finais de CT-50 são as armadilhas próprias da edição.** *Unicidade contra si
mesmo*: a validação ingênua acusa colisão do registro com ele próprio, e o gestor nunca mais muda.
*Editar sem alterar nada*: o `save` que não muda campo algum tem de passar. Nenhuma das duas tem
equivalente na criação, e nenhum cenário de `create` as alcança.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M13-1 | a entidade não entra na lista de subtração e o usuário comum herda a permissão | **CT-47** |
| M13-2 | a subtração casa por **substring** e tira também a permissão de solicitação de compra | CT-47 (terceira asserção) |
| M13-3 | a permissão existe correta e a tela não a consulta | **CT-48** |
| M13-4 | a unicidade do nome é **global**, não por organização | CT-50 (linha "outra organização") |
| M13-5 | a unicidade não ignora o próprio registro e o `save` acusa colisão consigo | **CT-50** (linha "unicidade contra si mesmo") |
| M13-6 | a unicidade é validada fora do Eloquent e ignora o recorte por organização | CT-50 (linhas colisão e outra organização) |
| M13-7 | a autorização barra o `index` e libera `create`/`edit` — quem cria o centro escolhe o gestor | **CT-48** (linhas `create` e `edit`) + **CT-62** (o não-efeito) |
| M13-8 | excluir o centro de custo apaga em cascata as solicitações dele, ou as deixa sem aprovador | **CT-59** |
| M13-9 | a unicidade compara byte a byte e `"MANUTENÇÃO"` entra ao lado de `"Manutenção"` | **CT-51** (linha acento + caixa) — a única que separa `NOCASE` do SQLite de uma colação acento-insensível |
| M13-10 | o nome é gravado com os espaços das bordas, e `" Suprimentos TI "` vira um terceiro nome | CT-51 (coluna `nome_gravado`) |

---

## Gate de tela de escrita

Toda rota `create` / `edit` da `## Superfície de UI` do PRD precisa de um cenário de **gravação por
componente** — `fillForm` → `->call('create'|'save')` → asserção sobre os campos que importam.
Tela de escrita coberta só por visita é lacuna de gate, não decisão de escopo
(`.ai/rules/testes.md:13-15`: *"uma tela aberta não é uma tela que grava"*).

| Rota | Cenário de gravação | Cenário de visita |
|---|---|---|
| `/app/solicitacoes-de-compra/create` | **CT-01** | coberto por CT-02/CT-03 (mesmo componente) |
| `/app/solicitacoes-de-compra/{record}/edit` | **CT-05** (linha `rascunho`), **CT-07** | CT-08 (403 de quem não é dono) |
| `/app/solicitacoes-de-compra/{record}` (view) | — (leitura) | **CT-35**, **CT-36** |
| `/app/solicitacoes-de-compra` (index) | — (leitura) | **CT-34**, CT-19, CT-44 |
| `/app/centros-de-custo/create` | **CT-49**, CT-51 | **CT-48** (linha `create`) + **CT-62** (a gravação recusada, com não-efeito) |
| `/app/centros-de-custo/{record}/edit` | **CT-50**, CT-59 | **CT-48** (linha `edit`) + CT-62 |

**Nenhuma célula vazia na coluna de gravação.** As ações de decisão (Enviar, Aprovar, Rejeitar,
Cancelar) não são rotas de escrita, e a sua metade de tela está em CT-19 (affordance) e CT-25
(a modal que exige o motivo).

---

## Checklist de Taxonomia

<!-- Resposta válida: um ID de cenário, "não se aplica: {motivo}", ou
     "lacuna declarada: {o que foi tentado}". NUNCA "sim". -->

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | **CT-08** (leitura, mesmo tenant), **CT-54** (escrita, mesmo tenant), **CT-45** e **CT-60** (entre tenants). CT-08 sozinho era falso ✅: um `GET` recusado torna o "nada mudou" vacuamente verdadeiro |
| Autorização exercida na ação, não só `can()` | **CT-16, CT-17, CT-18** (decisão), **CT-54** (escrita alheia), **CT-48** (as três rotas) e **CT-62** (a gravação pela persona errada). CT-47 lê a matriz e por isso **não** conta sozinho aqui |
| Idempotência, ancorada no agregado persistido | **CT-33** (cancelar 2×), **CT-39** (duplo clique nos dois ramos), **CT-09** (excluir 2×) |
| Concorrência | **CT-42** (duas aprovações), **CT-43** (decisões opostas, com a ordem no oráculo). O que eles provam é o check-then-act **em memória, num processo**; o isolamento sob duas conexões reais é **M11-3, lacuna declarada** |
| Fronteira **no ponto de entrada** (gravação), não só no uso | **CT-03** (criação, com o valor **gravado** afirmado), **CT-07** (edição) — e o ponto de uso em **CT-13**. Sem a coluna `valor_gravado`, CT-03 verificava a fronteira só na recusa, que é meia fronteira |
| Domínio condicionado (um campo cuja fronteira depende de outro) | **CT-13, CT-16, CT-37, CT-38** — o `valor` condiciona o **número de etapas exigidas** e o **conjunto de aprovadores válidos**: acima do limite existe uma etapa de diretor, abaixo a aprovação do gestor é final. Está coberto; a resposta anterior (`não se aplica`) era um falso negativo, que desliga a checagem justamente onde ela cresceria |
| **Estado × operação de escrita** (o terminal deixou de funcionar?) | **CT-05, CT-06, CT-10, CT-16, CT-21, CT-30** — as 12 células das linhas `aprovada` e `cancelada`. A solicitação terminal **não** desaparece da listagem (CT-34 prova que aparece), e nenhuma escrita a alcança |
| Ausente ≠ `null` ≠ `""` | **CT-02** (obrigatórios do formulário), **CT-22** (justificativa: ausente, `null`, `""`, `"   "`, `"\n\t"`) |
| Paginação | lacuna declarada: o requisito não determina paginação (**P-08**). Tentado derivar de RQ-12, que exige apenas que a situação apareça; um oráculo de "20 por página" viria do default do Filament, não do card |
| Ordenação por coluna | **CT-36** cobre o empate na ordenação do histórico (a única ordenação que o requisito determina, por "cada etapa"), **com a etapa do diretor inserida primeiro** — sem essa inversão o cenário não discriminava `orderBy(created_at)` de `orderBy(created_at, id)` e o item era um falso ✅. A ordenação da **listagem** é lacuna declarada, mesma pergunta **P-08** |
| Timezone / DST / `date` × `datetime` | não se aplica: nenhuma cláusula de RQ-01 a RQ-14 depende de instante, prazo, expiração ou agendamento — SLA e lembrete estão em Fora de Escopo no `00`. O único uso de tempo é **ordenar** o histórico, e o caso difícil dele (empate) é **CT-36** |
| Unicode | **CT-51** (linha `"MANUTENÇÃO"` × `"Manutenção"`) — é a única linha que separa o `NOCASE` do SQLite, que é ASCII-only, de uma colação acento-insensível de produção. Sem ela o `Esquema` era todo ASCII e **passava em teste podendo falhar em produção** |
| Limite de `varchar` | lacuna declarada: o requisito não impõe limite de tamanho à descrição (**P-11**), então não há oráculo para "no limite do `varchar`". Tentado derivar de RQ-01, que só nomeia o campo. O que **é** derivável — texto só com espaços não é descrição — está em **CT-02** |
| Unicidade + `SoftDeletes` | **CT-50** (linha criar → excluir → recriar `"Suprimentos"` na Acme) — o caso que o item de fato cobre, aplicado ao único campo único da entrega. A resposta anterior (`não se aplica: nenhum model usa SoftDeletes`) era inválida por construção: afirmava sobre a implementação num documento que recusa implementação como oráculo, e escondia o par criar → excluir → recriar |
| CRUD combinado (ID inexistente, excluir 2×, editar sem alterar) | **CT-09** (inexistente e excluir 2×), **CT-50** (salvar sem alterar nada), **CT-58** e **CT-59** (excluir dos dois lados da FK) |
| Mass assignment | **CT-04** (`situacao`, `solicitante_id`) e **CT-60** (`centro_custo_id` — a única FK do payload, e a que carrega a consequência de organização) |
| Upload | não se aplica: a feature não tem upload. Anexo está em Fora de Escopo no `00` |
| Precisão monetária | **CT-13** (R$ 5.000,00 exatos, o valor que distingue `>` de `>=`), **CT-14 + CT-63** (R$ 5.000,004, que distingue comparar o digitado em `float` de comparar o persistido em `decimal`), **CT-03** (o valor gravado, não só a contagem) e **CT-52** (o limite **entregue**). O `Dado` de CT-13 e CT-63 exige o registro **recarregado do banco**, que é o que exercita o `decimal:2` voltando como string — o risco que a varredura **P** nomeia. Nenhum exemplo usa `float` como tipo do valor, e não há aritmética monetária a arredondar |

---

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | grava em rascunho, no nome de quem criou | R1 | EP | Livewire | `Feature/AprovacaoDeCompra/TelasTest.php` | M1-1, M1-2 |
| CT-02 | obrigatório ausente / vazio / só espaços | R1 | EP | Livewire | `…/TelasTest.php` | M1-3 |
| CT-03 | domínio do valor na **criação** | R1 | BVA 3-valores | Livewire | `…/TelasTest.php` | M1-5 |
| CT-04 | mass assignment de situação e solicitante | R1 | taxonomia | Feature | `…/SolicitacaoTest.php` | M1-4 |
| CT-05 | coluna `editar` da matriz (1 válida + 4 inválidas) | R2 | estado × operação | Livewire + Feature | `…/TelasTest.php` + `…/SolicitacaoTest.php` | M2-1, M2-2 |
| CT-06 | coluna `excluir` da matriz | R2 | estado × operação | Feature | `…/SolicitacaoTest.php` | M2-1, M2-2 |
| CT-07 | domínio do valor na **edição** | R2 | BVA 3-valores | Livewire | `…/TelasTest.php` | M2-3 |
| CT-08 | IDOR no mesmo tenant | R2 | matriz papel × ação | Feature | `…/SolicitacaoTest.php` | M2-4 |
| CT-09 | ID inexistente, excluir 2× | R2 | taxonomia CRUD | Feature | `…/SolicitacaoTest.php` | M2-5 |
| CT-10 | coluna `enviar` da matriz | R3 | estado × operação | Feature | `…/MaquinaDeEstadosTest.php` | M3-1, M3-2 |
| CT-11 | centro sem gestor: falha fechado | R3 | EP | Feature | `…/MaquinaDeEstadosTest.php` | M3-3, M3-4 |
| CT-12 | envio por quem não é o solicitante | R3 | barreira no model | Feature | `…/MaquinaDeEstadosTest.php` | M3-5 |
| CT-13 | limite exclusivo (5 valores em torno de R$ 5.000,00) | R4 | BVA 3-valores | Feature | `…/AlcadaTest.php` | M4-1, M4-2, M4-6 |
| CT-14 | alçada sobre o valor **persistido** | R4 | precisão | Feature | `…/AlcadaTest.php` | M4-5 |
| CT-15 | valor editado antes do envio decide a alçada | R4 | criação ≠ edição ≠ uso | Feature | `…/AlcadaTest.php` | M4-3 |
| CT-16 | coluna `aprovar` da matriz | R5 | estado × operação | Feature | `…/AutorizacaoTest.php` | M5-6, M4-4 |
| CT-17 | etapa corrente × persona (7 linhas) | R5 | tabela de decisão | Feature | `…/AutorizacaoTest.php` | M5-1, M5-2, M5-4 |
| CT-18 | barreira do aprovador chamada direto | R5 | barreira no model | Feature | `…/AutorizacaoTest.php` | M5-3 |
| CT-19 | ações de decisão ocultas para quem não decide | R5 | affordance | Livewire | `…/TelasTest.php` | M5-5 |
| CT-20 | solicitante que é gestor do próprio centro | R5 | EP `@premissa` | Feature | `…/AutorizacaoTest.php` | — (fixa a premissa P-07) |
| CT-21 | coluna `rejeitar` da matriz (3 inválidas) | R6 | estado × operação | Feature | `…/AutorizacaoTest.php` | M6-3 |
| CT-22 | justificativa ausente / nula / vazia / espaços | R6 | EP | Feature | `…/AutorizacaoTest.php` | M6-1, M6-2, M6-3 |
| CT-23 | rejeição do gestor: volta a rascunho com motivo | R6 | célula válida | Feature | `…/AutorizacaoTest.php` | M6-6 |
| CT-24 | rejeição do **diretor**: volta a rascunho | R6 | célula válida | Feature | `…/AutorizacaoTest.php` | M6-4, M6-5 |
| CT-25 | modal de rejeição sem motivo não submete | R6 | validação de tela | Livewire | `…/TelasTest.php` | M6-1 (metade da tela) |
| CT-26 | 2-switch: rejeitada pelo gestor e reenviada | R7 | 2-switch | Feature | `…/MaquinaDeEstadosTest.php` | M7-3, M7-6 |
| CT-27 | 2-switch: rejeitada pelo **diretor**, volta ao gestor | R7 | 2-switch | Feature | `…/MaquinaDeEstadosTest.php` | M7-1, M7-2 |
| CT-28 | 3-switch: o diretor é exigido de novo no ciclo 2 | R7 | 3-switch | Feature | `…/MaquinaDeEstadosTest.php` | M7-4 |
| CT-29 | valor corrigido muda a alçada do ciclo 2 | R7 | 2-switch × edição | Feature | `…/MaquinaDeEstadosTest.php` | M7-5 |
| CT-30 | coluna `cancelar` da matriz | R8 | estado × operação | Feature | `…/MaquinaDeEstadosTest.php` | M8-1, M8-2 |
| CT-31 | cancelamento por quem não é o solicitante | R8 | barreira no model | Feature | `…/MaquinaDeEstadosTest.php` | M8-4 |
| CT-32 | cancelar não grava etapa e não notifica | R8 | rastreio de efeito | Feature | `…/MaquinaDeEstadosTest.php` | M8-3 |
| CT-33 | cancelar 2× (idempotência no agregado) | R8 | idempotência | Feature | `…/MaquinaDeEstadosTest.php` | M8-5 |
| CT-34 | os 5 rótulos do enum na listagem | R9 | EP exaustiva | Livewire | `…/TelasTest.php` | M9-1, M9-2 |
| CT-35 | histórico: quem, quando, decisão, motivo | R9 | EP | Livewire | `…/TelasTest.php` | M9-3 |
| CT-36 | ordem do histórico com `created_at` empatado | R9 | ordenação | Livewire | `…/TelasTest.php` | M9-5 |
| CT-37 | notificou o próximo aprovador, nos 2 ramos | R10 | rastreio de efeito | Feature | `…/NotificacaoTest.php` | M10-1, M10-2, M10-5 |
| CT-38 | não notificou quando não devia, nos 2 ramos | R10 | rastreio de efeito | Feature | `…/NotificacaoTest.php` | M10-3, M10-4 |
| CT-39 | notificou **uma só vez**, nos 2 ramos | R10 | rastreio de efeito | Feature | `…/NotificacaoTest.php` | M10-8 |
| CT-40 | atomicidade — falha na gravação da etapa | R10 | injeção de falha | Feature | `…/NotificacaoTest.php` | M10-7 |
| CT-41 | atomicidade — falha no envio do e-mail | R10 | injeção de falha | Feature | `…/NotificacaoTest.php` | M10-7 |
| CT-42 | dois diretores simultâneos | R11 | concorrência | Feature | `…/MaquinaDeEstadosTest.php` | M11-1, M11-2, M11-4 |
| CT-43 | aprovar e rejeitar em duas abas | R11 | concorrência | Feature | `…/MaquinaDeEstadosTest.php` | M11-1, M11-2 |
| CT-44 | listagem não mostra solicitação de outra organização | R12 | isolamento | Livewire (Tenancy) | `FeatureTenancy/AprovacaoDeCompraTest.php` | M12-1, M12-4 |
| CT-45 | identificador de outra organização dá 404 | R12 | IDOR entre tenants | Feature (Tenancy) | `FeatureTenancy/…` | M12-2, M12-4 |
| CT-46 | o diretor notificado é o da organização certa | R12 | isolamento × efeito | Feature (Tenancy) | `FeatureTenancy/…` | M12-3 |
| CT-47 | usuário comum sem permissão de centro de custo | R13 | matriz papel × ação | Feature | `…/AutorizacaoTest.php` | M13-1, M13-2 |
| CT-48 | usuário comum recebe 403 na tela | R13 | autorização na ação | Feature | `…/AutorizacaoTest.php` | M13-3 |
| CT-49 | gravação do centro de custo com gestor | R13 | gate de tela de escrita | Livewire | `…/TelasTest.php` | — (gate) |
| CT-50 | unicidade por organização e contra si mesmo | R13 | normalização | Livewire | `…/TelasTest.php` | M13-4, M13-5, M13-6 |
| CT-51 | caixa, acento e espaços nas bordas | R13 | normalização `@premissa` | Livewire | `…/TelasTest.php` | M13-6, M13-9, M13-10 |
| **CT-52** | (rev) o limite **entregue** é R$ 5.000,00 | R4 | partição do parâmetro entregue | Feature | `…/AlcadaTest.php` | M4-7 |
| **CT-53** | (rev) cada etapa registra quem de fato decidiu | R5 | papel × ação com 4 personas distintas | Feature | `…/AutorizacaoTest.php` | M5-7 |
| **CT-54** | (rev) o colega não grava nem apaga o rascunho alheio | R2 | barreira de identidade na escrita | Feature | `…/SolicitacaoTest.php` | M2-4, M2-6 |
| **CT-55** | (rev) o gestor da vez é o de agora, não o do ciclo anterior | R7 | 2-switch com mudança de configuração | Feature | `…/MaquinaDeEstadosTest.php` | M7-7 |
| **CT-56** | (rev) trocar o centro de custo troca o aprovador | R2 | coluna `editar` por campo | Feature | `…/MaquinaDeEstadosTest.php` | M2-8 |
| **CT-57** | (rev) detalhe da solicitação **aprovada** com as duas assinaturas | R9 | célula `visualizar × aprovada` (detalhe) | Livewire | `…/TelasTest.php` | M9-6 |
| **CT-58** | (rev) excluir rascunho que carrega histórico | R2 | coluna `excluir` × rascunho pós-rejeição | Feature | `…/SolicitacaoTest.php` | M2-7 |
| **CT-59** | (rev) excluir centro de custo com solicitação vinculada | R13 | matriz de `CentroCusto` | Feature | `…/AutorizacaoTest.php` | M13-8 |
| **CT-60** | (rev) centro de custo de outra organização no payload | R1 | mass assignment de FK | Feature (Tenancy) | `FeatureTenancy/…` | M1-7 |
| **CT-61** | (rev) o aprovador encontra na listagem o que não é dele | R9 | recorte da consulta base `@premissa` | Livewire | `…/TelasTest.php` | M9-7 |
| **CT-62** | (rev) o usuário comum não grava centro de custo | R13 | autorização na ação de escrita | Livewire | `…/TelasTest.php` | M13-7 |
| **CT-63** | (rev) a alçada decide sobre o valor persistido | R4 | precisão + `Quando` único | Feature | `…/AlcadaTest.php` | M4-5, M4-8 |

**63 cenários, 90 mutantes no `04` (+8 no `05`), 3 sem matador** (M9-4, M10-6, M11-3 — todos
declarados, todos vinculados a pergunta aberta ou a limite de arnês, com o que foi tentado escrito).

### Estouro do teto de mutantes — declarado

O gate pede **3 a 6 mutantes por regra** no perfil completo, e o teto existe para impedir que
alguém infle o gate com mutantes triviais para parecer rigoroso. Nove das treze regras passam de 6
depois da revisão adversarial:

| Regra | Mutantes | Leitura |
|---|---|---|
| **R13** (10) | autorização de administração **e** identidade do nome são dois eixos com técnicas diferentes | **candidata legítima a virar duas regras** — R13a (quem pode mexer) e R13b (o nome é único e normalizado). Não foi desdobrada aqui para não renumerar toda a rastreabilidade num fechamento de revisão; fica registrado como a primeira coisa a fazer se esta wiki for evoluída |
| **R10** (9) | idem: o **roteamento** do efeito e a **atomicidade** dele são dois eixos | **candidata a virar duas regras**. A skill já trata a atomicidade como um quarto cenário destacável do rastreio, e aqui ela virou dois (CT-40 e CT-41) |
| R2, R4, R5 (8) · R1, R6, R7, R9 (7) | passam por 1 ou 2 | não são inflação: **todos os excedentes vieram da revisão adversarial**, cada um nomeia uma implementação errada concreta e cada um aponta um matador. Nenhum é do tipo "apagar o método" ou "retornar `null`" |

Nenhum mutante foi cortado para caber no teto. O critério de suficiência da skill é *toda regra tem
seus mutantes previstos mortos* — cortar mutante plausível para respeitar um teto de contagem
inverteria exatamente isso.

**Estouros de teto, e por quê.** R2 (8 cenários), R4 (5), R5 (6), R7 (5), R9 (5) e R13 (7)
ultrapassam o teto do perfil. Todos os excedentes são CT-52…CT-63, e todos são **único matador** de
um mutante previsto — cinco deles de mutantes que a primeira derivação nem previa. É o
[gate do passo 6 vencendo o teto](#fechamento-do-ciclo-com-mutation-testing): deixar mutante vivo
para economizar cenário inverte a razão de existir da derivação. Nenhuma regra precisou virar duas:
os excedentes são células e dimensões da mesma regra, não regras novas.

### Cenários cogitados e cortados

| Cenário cogitado | Por que foi cortado |
|---|---|
| duplo clique em `enviar` como cenário próprio de R11 | já provado por CT-39, que afirma sobre a situação **e** a contagem de e-mails — mataria o mesmo conjunto de mutantes |
| `assertNothingSent()` no caminho de justificativa vazia, como prova de **atomicidade** | é pré-validação: nada seria enviado em nenhuma implementação. A asserção continua em CT-22, mas como não-efeito de recusa |
| um cenário por célula inválida da matriz (21 cenários) | um `Esquema do Cenário` por **coluna** cobre as mesmas 21 células e conta como 1 cenário — é a forma canônica |
| filtro por situação na listagem | só o PRD determina; o requisito pede *mostrar* a situação, não filtrar (**P-08**) |
| asserção sobre o corpo do e-mail | seria teste do PRD; deixa M10-6 declarado como lacuna (**P-05**) |
| asserção sobre a cor do badge | idem, **P-04**; e `assertSee` não valida cor |
| contagem de permissions do painel `app` (regressão do `PaineisTest`) | invariante do kit, não cláusula do card. O que é derivável de RQ-04 + A-08 está em CT-47 |
| `expect($user->can('Approve:SolicitacaoCompra'))` | `can()` sozinho é oráculo proibido: a policy pode estar certa e o Resource nunca consultá-la. Substituído por CT-16 a CT-18, que **disparam** a ação |
| um cenário de `Unit` para `exigeDiretor()` | `tests/Unit` não tem `TestCase` ligado neste projeto: `config()` volta `null`. Ver [Divergências](#divergências-declaradas) |

---

## Fechamento do Ciclo com Mutation Testing

**Antes de rodar**: `composer require pestphp/pest-plugin-mutate --dev` — hoje o plugin está só em
`vendor/`, como transitivo (ver [Divergências](#divergências-declaradas)).

```bash
vendor/bin/pest tests/Feature/AprovacaoDeCompra --mutate --path=app/Models --min=70
vendor/bin/pest tests/Feature/AprovacaoDeCompra --mutate --path=app/Enums
```

- Exige driver de cobertura (**PCOV** ou Xdebug com `XDEBUG_MODE=coverage`); sem PCOV, medir só
  este escopo, nunca o projeto inteiro
- `--path=` é o filtro confiável; `--class=` pode não casar
- **`covers(X::class)` restringe o que conta como coberto**: mutante em classe fora do `covers()`
  é reportado como `uncovered` e o score cai a 0% mesmo com o código sendo executado. Medir
  `SolicitacaoCompra` e `SituacaoSolicitacao` em execuções separadas, ou declarar as duas
- **O score não responde por omissão.** Mutação só muta código que existe: se a coluna `cancelar`
  da matriz nunca virou `if`, nenhum mutante é gerado e o score não cai. Quem responde por omissão
  é a rastreabilidade `RQ` → regra e as 21 células inválidas desta matriz

| Mutante sobreviveu | Lacuna de derivação | O que escrever |
|---|---|---|
| `>` → `>=` no limite | BVA faltando | linha na borda exata (CT-13 já cobre; se sobreviveu, o `Então` está fraco) |
| condição de situação removida | célula da matriz sem cenário | a linha correspondente do `Esquema` da coluna |
| chamada de notificação removida | efeito colateral não verificado | rastreio de efeito no ramo que faltou |
| `refresh()` removido depois da transição | oráculo sobre estado **em memória** em vez de persistido | reescrever o `Então` para afirmar sobre o registro recarregado |

---

## Revisão Adversarial

Executada por sub-agente independente, que recebeu **apenas** o `00-requisito.md`, este `04` e o
`05` — **sem** o PRD, **sem** o código e **sem** o raciocínio de quem derivou, conforme o contrato
da skill. As sete frentes do contrato foram percorridas.

**41 achados. Todos fechados**: 12 viraram cenário novo, 22 viraram oráculo reescrito, 4 viraram
correção de resposta do checklist, 3 viraram lacuna declarada com o que foi tentado. **Nenhum foi
descartado.**

> **O conjunto que entrou na revisão tinha 51 cenários e 59 mutantes previstos, e a revisão provou
> 5 implementações erradas plausíveis que passavam em todos eles.** Nenhuma das cinco era um
> mutante previsto. É a medida do valor deste passo — e a razão de a skill proibir autorrevisão.

### Achados e fechamento

#### Frente 1 — implementações erradas que passavam no conjunto inteiro (estruturais)

| # | Achado | Regra | Técnica que faltava | Virou |
|---|---|---|---|---|
| L1 | **a notificação nunca é e-mail**: `via()` devolvendo `['database']` passa em todos os 16 cenários de notificação, porque `assertSentTo` não olha o canal — e a seção `## Fakes` proibia `Mail::assertSent` com uma justificativa que, lida rápido, dispensava afirmar o canal | R10 | rastreio de efeito **no canal**: as 4 direções foram feitas e a dimensão *qual efeito* ficou de fora | cláusula de canal em **CT-37** + nota nova em `## Fakes` + mutante **M10-9** |
| L2 | **o limite entregue nunca é exercitado**: todo cenário de R4 injeta `config()->set(5000.00)`, então um default em centavos, com um zero a mais ou com a chave divergindo do `.env.example` libera meio milhão com uma assinatura só | R4 | partição sobre o **parâmetro entregue**, distinta do comportamento parametrizado | **CT-52** + **M4-7** |
| L3 | **o decisor da etapa nunca é verificado**: nenhum cenário afirmava quem assinou uma **aprovação** com pessoas distintas — CT-20 colapsa solicitante, gestor e chamador na mesma pessoa (o equivalente, em identidade, do valor redondo), e CT-35 lê um histórico montado pela factory. `decidido_por = centroCusto->gestor_id` registrava a aprovação do diretor no nome do gestor, para sempre | R5, R9 | matriz papel × ação com **exemplo discriminante** + rastreio de efeito sobre o registro de auditoria | **CT-53** + 4 personas distintas no `Dado` de CT-17 + **M5-7** |
| L4 | **a barreira de dono só existe na leitura**: CT-08 é um `GET` recusado, e afirmar depois dele que "nada mudou" é vacuamente verdadeiro. A policy negando `view` + o `save` conferindo só a situação passava, e o primeiro job edita o rascunho alheio | R2 | matriz papel × ação **cruzada** com estado × operação — a matriz era percorrida com persona fixa | **CT-54** + CT-08 reescrito para afirmar só o que prova + **M2-6** |
| L5 | **o aprovador congelado**: desnormalizar `aprovador_atual_id` no envio passa em tudo, porque nenhum cenário mudava o gestor nem o centro de custo entre dois momentos — os 2-switch variavam o **valor** e mantinham a configuração de aprovação fixa | R3, R5, R7, R10 | 2-switch **com mudança de dado entre os giros** + coluna `editar` aplicada a cada campo, não a um representativo | **CT-55**, **CT-56** + **M7-7**, **M2-8** |

#### Frente 2 — `Então` fraco (oráculo reescrito)

| # | Achado | Virou |
|---|---|---|
| L6 | CT-03 afirmava só a **contagem**; `0,01` e `0,02` dão ambos `gravadas = 1`, e truncar/zerar o valor passava | coluna `valor_gravado` no `Esquema` |
| L7 | CT-17 não afirmava não-efeito nas 5 linhas recusadas nem efeito nas 2 aceitas | colunas `etapas` e `emails` + **M5-8** |
| L8 | CT-51 tinha um `Então` de uma cláusula só, e a premissa A-19 ("espaços aparados") não era afirmada em lugar nenhum | colunas `nome_gravado` e `quantos` + **M13-10** |
| L9 | CT-08: não-efeito vacuamente verdadeiro | ver L4 |
| L10 | CT-48 exercia **uma** rota (`index`) e não afirmava não-efeito — negar `viewAny` e liberar `create` é a escalada de A-08, e passava | CT-48 virou `Esquema` de 3 rotas + **CT-62** + **M13-7** |
| L11 | CT-24 passava a justificativa no `Quando` e não a afirmava no `Então`: *"só a rejeição do gestor grava a justificativa"* sobrevivia | cláusula da justificativa e do decisor + **M6-7** |
| L12 | **CT-36 não discriminava**: com o gestor inserido primeiro, `orderBy(created_at)` sem desempate devolve a ordem esperada por acidente | `Dado` invertido — a etapa do **diretor** entra primeiro |
| L13 | CT-B01 usava `assertSee`/`assertDontSee` sobre uma tabela — a assertion que o próprio `05` recusa na seção *Cogitado e cortado* | asserção com **escopo de linha** + dívida de seletor registrada |
| L14 | CT-B02 provava só que a modal não fechou (`assertSee` do **rótulo** do campo): a modal que fica aberta e **não sinaliza nada** passava | asserção sobre o **elemento de erro** do campo |
| L15 | CT-12 e CT-31 recusavam sem afirmar contagem de etapas | cláusulas acrescentadas |
| L16 | CT-49 não afirmava a organização do centro criado, e R12 não tinha exemplo nenhum para `CentroCusto` | cláusula de organização + **CT-60** |
| L17 | a alçada nunca era comparada sobre um registro **recarregado do banco** — o risco que a própria varredura **P** nomeia (`decimal:2` volta como string) não era exercitado | `Dado` de CT-13 e CT-63 exige o registro recarregado + **M4-8** |

#### Frente 3 — cenário sem `Então` / com mais de um `Quando`

| # | Achado | Virou |
|---|---|---|
| L18 | **nenhum cenário sem `Então`** — frente sem achado, e o revisor registrou o porquê: o gargalo do conjunto era a **força** do oráculo, não a ausência | — |
| L19 | CT-14 tinha `Quando` composto (*"envia **e** aprova"*): falhando, não se saberia se a alçada foi congelada no envio ou avaliada errado na aprovação | separado em **CT-14** (persistência) e **CT-63** (decisão) |
| L20 | CT-43 fundia aprovar e rejeitar num `Quando` e fixava `aprovada` — uma implementação **correta** que processasse a rejeição primeiro **falharia** o cenário | virou `Esquema` de 2 linhas com a ordem no oráculo + **M11-5** |
| L21 | CT-15 e CT-29 escondiam o reenvio (a transição de RQ-09) dentro do `Dado`: quebrando, erravam no arranjo em vez de falhar na asserção | reenvio isolado como passo próprio do `Dado`, `Quando` reservado para a aprovação |

#### Frente 4 — células da matriz afirmadas e não cobertas

| # | Achado | Virou |
|---|---|---|
| L22 | a coluna `visualizar` era 5/0 **na listagem** e 1/0 no **detalhe**: `visualizar × aprovada` no detalhe — o coração de RQ-13 — não tinha cenário | **CT-57** + a matriz passou a nomear as duas leituras |
| L23 | a persona variava por linha dentro de CT-16 e CT-21, estreitando o que cada célula afirma; a matriz é bidimensional e a autorização é tridimensional | dimensão **persona** declarada na matriz + a célula que importava (o gestor reaprovando o que já decidiu) explicitada em CT-17 |
| L24 | `rascunho` são dois estados: o virgem e o **pós-rejeição**, que carrega etapas — excluir com histórico nunca era tentado | **CT-58** + dimensão *qual rascunho* declarada |
| L25 | `CentroCusto` não tinha matriz nenhuma, e a coluna `excluir` não existia | **CT-59** + [matriz de `CentroCusto`](#matriz-de-centrocusto) |

#### Frente 5 — cláusulas `RQ` não falsificáveis

| # | Cláusula e metade não falsificável | Virou |
|---|---|---|
| L26 | RQ-05, o **número** R$ 5.000 (a *forma* `>` era falsificável; o valor entregue não) | CT-52 |
| L27 | RQ-14, a metade **"por e-mail"** | cláusula de canal em CT-37 |
| L28 | RQ-13, **"quem aprovou"** no caminho de escrita | CT-53 |
| L29 | RQ-02/RQ-03, o **"ele"** (o solicitante) na escrita | CT-54 |
| L30 | RQ-01, o **centro de custo** como referência válida e da própria organização | CT-60 |
| L31 | RQ-12, as demais situações **no detalhe** | CT-57 |
| L32 | **ambiguidade nunca levantada**: quem enxerga a solicitação de quem dentro da organização. Um recorte por solicitante na consulta base passa em CT-34, CT-19, CT-44 e CT-45 e esvazia a tela de **todo aprovador** | **CT-61** + pergunta **P-13 / A-23** — a de maior impacto da wiki |

#### Frentes 6 e 7 — falsos ✅ no checklist de taxonomia

| # | Item | Virou |
|---|---|---|
| L33 | *IDOR* respondido com CT-08, que é leitura | CT-08 + **CT-54**, com a metade de escrita nomeada |
| L34 | *Ordenação* respondido com CT-36, que não discriminava (ver L12) — **M9-5 estava vivo** | `Dado` de CT-36 invertido; M9-5 volta a ter matador |
| L35 | *Fronteira na gravação* verificada só na recusa | coluna `valor_gravado` (L6) |
| L36 | *Precisão monetária* sem a comparação sobre o valor como o banco devolve, e dependente de uma premissa | CT-03, CT-52 e o `Dado` recarregado somados ao item |
| L37 | *Mass assignment* sem a única FK do payload | CT-60 |
| L38 | *Autorização na ação* respondido com CT-48, que exercia uma rota; e CT-47 é `can()` invertido | CT-48 (3 rotas) + CT-62, e CT-47 explicitamente não conta sozinho |
| L39 | *Unicidade + SoftDeletes* respondido com `não se aplica` **sobre a implementação** — resposta inválida num documento que recusa implementação como oráculo — escondendo o par criar → excluir → recriar | linha nova em CT-50, aplicada ao único campo único da entrega |
| L40 | *Unicode* coberto só em ASCII: `"MANUTENÇÃO"` × `"Manutenção"` divergem entre o `NOCASE` do SQLite e as colações de produção — **passava em teste podendo falhar em produção** | linha de acento em CT-51 + **M13-9**; o item foi separado de *limite de varchar* |
| L41 | *Domínio condicionado* respondido `não se aplica`, e é falso: o `valor` condiciona o número de etapas exigidas e o conjunto de aprovadores válidos | resposta trocada por CT-13, CT-16, CT-37, CT-38 |
| L42 | *Concorrência*: os cenários provam o check-then-act **em memória, num processo**, e o `Então` não distinguia recusa vinda do banco de recusa vinda de um `if` | escopo declarado no corpo de R11, e a lacuna real mantida em **M11-3** |

### Segunda rodada

Executada, porque o fechamento criou **12 cenários novos** — e cenário novo introduz superfície
nova, que é onde mora a lacuna de segunda ordem. Ela devolveu **3 achados, nenhum estrutural**, e
os três foram fechados no mesmo passe:

1. **CT-56 tinha dois `Quando`** (*"altera o centro de custo **e** a envia"*) — a alteração voltou
   para o `Dado`, já que a célula `editar` válida é CT-05 e o que CT-56 afirma é o destino do envio.
2. **CT-56 tinha uma terceira ação no `Então`** (a tentativa de Ana de aprovar) — cortada, porque
   é a linha "gestor do centro errado" de CT-17 e mataria o mesmo mutante.
3. **A célula *"editar o gestor com solicitação em trânsito"* da matriz de `CentroCusto` apontava
   para CT-56**, que é sobre a solicitação e não sobre o centro — reapontada para **CT-55**, com o
   motivo escrito na nota abaixo da matriz.

**Teto de 2 rodadas respeitado.** Nenhum achado estrutural sobreviveu à segunda rodada, e nenhuma
regra precisou ser desdobrada em duas: os 12 cenários novos são células, personas e dimensões das
13 regras existentes, não regras novas.

---

## Casos de Teste de Browser

O gate do `05` **passa**, e passa por pouco: das 6 linhas da `## Superfície de UI`, o que **só o
navegador prova** é a modal de decisão executando Alpine e o console limpo da tela de autoria
própria. Tudo o mais — affordance, validação da modal, rótulo de situação, histórico, gravação —
é componente Livewire e está neste arquivo.

Ver `05-casos-de-teste-browser.md`: **CT-B01** (o gestor aprova pela tela, com JS executado) e
**CT-B02** (o erro visível da justificativa obrigatória). Teto do perfil completo: 1 happy path +
1 erro visível — respeitado exatamente.
