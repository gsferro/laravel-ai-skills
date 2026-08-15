# Requisito — FERRO-830: Fluxo de aprovação de solicitação de compra

## Fonte

- **Origem**: card **FERRO-830**, colado verbatim no chat pelo usuário ao invocar a skill `feature-wiki`
- **Data**: 2026-08-14
- **Autor / solicitante**: não declarado no card — assumido como o time de negócio que abriu o ticket
- **Fidelidade**: **alta** — texto escrito, transcrito abaixo sem alteração

> **Degradação registrada nesta sessão**: as tools MCP do Laravel Boost (`search-docs`, `database-schema`)
> **não estavam disponíveis**. Foi usado o fallback que a própria skill determina: leitura de
> `vendor/` (fonte autoritativa para a versão instalada), `.ai/rules/`, `wikis/convencoes.md` e as
> wikis existentes em `wikis/specs/`. Toda assinatura de API citada no PRD foi confirmada por
> `Read`/`Grep` no vendor deste projeto, com `arquivo:linha`. Nenhuma foi escrita de memória.

## Texto Original

<!-- IMUTÁVEL. Não editar, não corrigir ortografia, não resumir, não reordenar. -->

> CARD FERRO-830 — Fluxo de aprovação de solicitação de compra
>
> O solicitante cria uma solicitação de compra com descrição, valor e centro de custo.
> Enquanto está em rascunho ele pode editar e excluir.
>
> Quando envia, a solicitação vai para o gestor do centro de custo aprovar. Se o valor
> for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor.
>
> O gestor pode aprovar ou rejeitar. Na rejeição a justificativa é obrigatória.
> Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo.
> Depois de aprovada não pode mais mexer.
>
> O solicitante pode cancelar a qualquer momento antes da aprovação final.
>
> Mostrar na tela o status atual e quem aprovou cada etapa.
> Notificar por e-mail o próximo aprovador.

## Decomposição em Cláusulas

| ID | Cláusula | Trecho literal de origem | Tipo |
|----|----------|--------------------------|------|
| RQ-01 | O solicitante cria uma solicitação de compra com **descrição**, **valor** e **centro de custo** | "O solicitante cria uma solicitação de compra com descrição, valor e centro de custo." | funcional |
| RQ-02 | Enquanto a solicitação está em rascunho, o solicitante pode **editá-la** | "Enquanto está em rascunho ele pode editar e excluir." | autorização |
| RQ-03 | Enquanto a solicitação está em rascunho, o solicitante pode **excluí-la** | "Enquanto está em rascunho ele pode editar e excluir." | autorização |
| RQ-04 | Ao enviar, a solicitação vai para **o gestor do centro de custo** aprovar | "Quando envia, a solicitação vai para o gestor do centro de custo aprovar." | funcional |
| RQ-05 | Valor **acima de R$ 5.000** exige também a aprovação do **diretor**, e ela vem **depois** da do gestor | "Se o valor for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor." | funcional |
| RQ-06 | O gestor pode **aprovar ou rejeitar** | "O gestor pode aprovar ou rejeitar." | funcional |
| RQ-07 | Na rejeição, a **justificativa é obrigatória** | "Na rejeição a justificativa é obrigatória." | restrição |
| RQ-08 | Solicitação rejeitada **volta para rascunho** | "Solicitação rejeitada volta para rascunho" | funcional |
| RQ-09 | O solicitante pode **corrigir e enviar de novo** a solicitação rejeitada | "pro solicitante corrigir e enviar de novo" | funcional |
| RQ-10 | Depois de aprovada, **não pode mais mexer** | "Depois de aprovada não pode mais mexer." | restrição |
| RQ-11 | O solicitante pode **cancelar** a qualquer momento **antes da aprovação final** | "O solicitante pode cancelar a qualquer momento antes da aprovação final." | funcional |
| RQ-12 | Mostrar na tela o **status atual** | "Mostrar na tela o status atual" | funcional |
| RQ-13 | Mostrar na tela **quem aprovou cada etapa** | "e quem aprovou cada etapa." | funcional |
| RQ-14 | **Notificar por e-mail** o **próximo aprovador** | "Notificar por e-mail o próximo aprovador." | funcional |

## Ambiguidades e Perguntas Abertas

> **O usuário não estava disponível para responder nesta execução.** Cada item abaixo registra a
> pergunta **e** a premissa adotada para seguir. Toda premissa está marcada em negrito e é
> revisável: se uma delas for negada, o item aponta o que exatamente muda no plano.

### A-01 — "centro de custo" não existe no projeto (RQ-01, RQ-04)

**Pergunta**: centro de custo é uma entidade a cadastrar, ou um campo livre?

O código foi varrido antes de assumir: não há model, migration nem tabela de centro de custo
(`app/Models/` tem `AgenteIa`, `Convite`, `Projeto`, `Role`, `Tenant`, `User`; nenhuma migration
menciona custo). RQ-04 diz "**o gestor do centro de custo**" — texto livre não tem gestor, então a
cláusula seguinte já decide a questão.

**Assumido**: **entidade nova `CentroCusto`**, com nome e **um gestor** (`gestor_id`, FK para
`users`), pertencente à organização (`BelongsToTenant`, como manda `wikis/convencoes.md`). CRUD
mínimo no painel `/app`, tratado como **entidade de administração** — ver A-08.

**Se negado**: cai o passo 8 do PRD (`CentroCustoResource`) e o gestor passa a vir de outro lugar;
o resto do fluxo não muda.

### A-02 — "o gestor" é um por centro de custo, ou um papel? (RQ-04)

**Assumido**: **um gestor por centro de custo**, coluna `gestor_id`. É a leitura literal de "o
gestor **do** centro de custo" — possessivo, singular. Um papel `gestor` global não teria como
responder "gestor de qual centro".

**Se negado** (vários gestores por centro): `gestor_id` vira uma pivot e `proximosAprovadores()`
devolve uma coleção em vez de um usuário — mudança contida no passo 5.

### A-03 — "o diretor" não está ligado a nada (RQ-05)

Ao contrário do gestor, o card **não** diz "o diretor do centro de custo" — diz só "o diretor".

**Assumido**: **papel `diretor`** (`roles.painel = 'app'`, semeado no `PapeisSeeder`), atribuído
dentro da organização. Qualquer pessoa com o papel pode aprovar a etapa de diretor; **todas** são
notificadas e **a primeira que decidir resolve** a etapa.

**Se negado** (diretor por centro de custo): vira uma segunda FK em `centros_custo` e some o papel.

### A-04 — "acima de R$ 5.000" é estritamente maior? E é fixo? (RQ-05)

Duas perguntas numa frase, e a primeira decide um caso de borda real: **R$ 5.000,00 exatos exigem
diretor ou não?**

**Assumido**: **estritamente maior** (`>`). "Acima de" exclui o próprio valor em português corrente,
e a leitura restritiva erra para o lado barato (uma aprovação a menos num valor de fronteira, não
uma a mais). **CT-04 fixa os dois lados do limite** justamente porque essa é a linha que ninguém
relê depois.

**Assumido**: o valor é **configurável** em `config/kit.php` (`kit.compras.limite_diretor`), com
default `5000.00` — cravar `5000` no código faria a próxima mudança de política virar deploy.

### A-05 — "não pode mais mexer" abrange o quê? (RQ-10)

**Assumido**: `aprovada` é **estado terminal**: não edita, não exclui, não envia, não cancela, não
aprova de novo. RQ-11 confirma metade disso ao limitar o cancelamento a "antes da aprovação final".

### A-06 — "cancelar a qualquer momento" inclui o rascunho? (RQ-11)

Literalmente, "a qualquer momento antes da aprovação final" inclui o rascunho. Mas RQ-03 já dá ao
rascunho o verbo **excluir**, e oferecer cancelar **e** excluir na mesma tela seria duas portas para
o mesmo lugar.

**Assumido**: **cancelar vale em `aguardando_gestor` e `aguardando_diretor`**; em `rascunho` o
caminho é excluir. É a leitura que não cria affordance duplicada.

**Pergunta em aberto**: se o negócio quiser preservar o registro cancelado em vez de apagá-lo, o
rascunho também deve cancelar — e aí RQ-03 é que muda de sentido.

### A-07 — o diretor também pode rejeitar? (RQ-06)

O card só diz "**o gestor** pode aprovar ou rejeitar". A etapa do diretor aparece apenas como
"aprovação do diretor".

**Assumido**: **sim, o diretor também rejeita**, com a mesma exigência de justificativa. Uma etapa
de aprovação sem a opção de recusar não é aprovação, é carimbo — e o efeito prático de negar isso
seria um diretor sem saída para uma solicitação que ele considera errada.

### A-08 — quem cadastra centro de custo, e por que isso é uma questão de segurança (RQ-04)

O card não diz. Mas a resposta errada abre uma escalada de privilégio **real e silenciosa**: quem
puder editar `centros_custo.gestor_id` pode se nomear gestor e aprovar as próprias solicitações.

**Assumido**: `CentroCustoResource` é **entidade de administração da organização** e entra em
`PapeisSeeder::permissoesDeAdministracaoDoApp()`, ficando fora do `panel_user`. Esta não é uma
escolha de conveniência: `.ai/rules/filament.md` e `wikis/convencoes.md` documentam que esquecer
essa lista **não gera erro nenhum** e promove todo usuário comum a administrador da organização.
**CT-14 existe só para isso.**

### A-09 — o solicitante pode ser o gestor do próprio centro de custo?

Não tratado pelo card.

**Assumido**: **permitido**, porque o card não veda e inventar uma regra de segregação de funções
seria decidir política de negócio pelo cliente. Registrado como pergunta aberta de maior impacto
desta wiki: se a resposta for "não", é **uma linha** em `SolicitacaoCompra::podeAprovar()` mais um
CT — barato de acrescentar, caro de descobrir em auditoria.

### A-10 — e se o centro de custo não tiver gestor no momento do envio? (RQ-04)

Caso de borda não coberto: `gestor_id` nulo (centro recém-criado, ou gestor removido).

**Assumido**: **falha fechado** — o envio é recusado com mensagem na tela e `warning` no log, e a
solicitação **fica em rascunho**. As duas alternativas são piores: pular a etapa aprovaria sem
aprovador, e enviar para ninguém deixaria a solicitação presa sem sinal. CT-13 cobre.

### A-11 — quem mais é notificado? (RQ-14)

O card nomeia **um** destinatário: "o próximo aprovador".

**Assumido**: só ele. Notificação de rejeição ao solicitante, de aprovação final, de cancelamento ao
aprovador — nada disso foi pedido e nada disso é implementado. Está em Fora de Escopo, para o
`feature-quality-gate` não acusar omissão indevida.

### A-12 — "mostrar na tela" em qual tela? (RQ-12, RQ-13)

**Assumido**: na **listagem** (coluna de situação) **e** na tela de visualização da solicitação
(situação + histórico de etapas com quem decidiu, quando e a justificativa). O plural de RQ-12/RQ-13
("status atual" e "quem aprovou cada etapa") pede as duas leituras: a rápida e a detalhada.

## Fora de Escopo (declarado)

- **Notificações além do próximo aprovador** — ver A-11. Sem e-mail de rejeição, de aprovação final,
  de cancelamento ou de lembrete.
- **Anexos, itens, fornecedores, cotação, ordem de compra, pagamento** — o card descreve um fluxo de
  aprovação, não um módulo de compras.
- **Delegação, substituto e férias do aprovador** — não pedido. Com o gestor ausente a solicitação
  fica parada, e isso é o comportamento especificado.
- **Prazo/SLA de aprovação, escalonamento automático** — não pedido, e A-04 não menciona tempo.
- **Mais de dois níveis de aprovação** — o card descreve exatamente dois (gestor, diretor). A
  generalização para N níveis é a tentação de projeto mais óbvia aqui e está recusada em ADR-04.
- **Faixas de alçada além do único limite de R$ 5.000** — um limite, um nível extra.
- **Edição da solicitação pelo aprovador** — só o solicitante edita, e só em rascunho.
- **Relatórios, dashboards e widgets de compras** — não pedidos.
- **Reabertura de solicitação cancelada** — o card não descreve saída do estado `cancelada`.
