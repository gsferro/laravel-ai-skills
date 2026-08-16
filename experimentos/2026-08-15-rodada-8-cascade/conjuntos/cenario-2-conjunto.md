# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Requisito: `00-requisito.md` · Plano: `01-plano-acao.md`  
> Derivado do **requisito**, não do plano. Nenhum cenário foi escrito olhando implementação.

## Perfil de Derivação

| Área | P | I | P×I | Perfil |
|---|---|---|---|---|
| Máquina de estados | 3 | 3 | 9 | completo |
| Autorização / IDOR | 3 | 3 | 9 | completo |
| Alçada de valor (R$ 5.000) | 3 | 3 | 9 | completo |
| Notificação por e-mail | 3 | 2 | 6 | padrão |
| Histórico de aprovação | 2 | 2 | 4 | padrão |
| Concorrência / idempotência | 3 | 3 | 9 | completo |

- Técnicas aplicadas: EP, BVA 3-valores, tabela de decisão, tabela estado × evento, matriz papel × ação, rastreio de efeito.
- Cenários: 58 · Regras: 10 · Mutantes previstos: 42 · Sem matador: 0.

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Cenários gerados |
|---|---|---|
| S | models `SolicitacaoCompra`, `CentroCusto`, `EtapaAprovacao`; enum `SituacaoSolicitacao`; resources; notification; policy | CT-01…CT-10 |
| F | criação, edição, exclusão, envio, aprovação, rejeição, cancelamento, notificação, histórico | CT-11…CT-40 |
| D | descrição, valor, centro_custo_id, solicitante_id, situacao, gestor_id, etapas | CT-01…CT-40 |
| I | painel `/app`, formulários Filament, métodos do model, rota de notificação | CT-41…CT-50 |
| P | Filament 5, Pest 5, SQLite, queue `sync` em teste | — |
| O | solicitante, gestor, diretor; painel `/app` | CT-41…CT-50 |
| T | transições de estado, concorrência, reenvio após rejeição | CT-12, CT-22, CT-23, CT-46, CT-47 |

## Mapa de Regras

| Regra | Área | Origem (`RQ`) | Técnica | Cenários |
|---|---|---|---|---|
| R1 — Criação em rascunho com descrição, valor e centro de custo | criação | RQ-01 | EP | CT-01, CT-02, CT-54 |
| R2 — Só o solicitante edita/exclui em rascunho | autorização | RQ-02, RQ-03 | matriz papel × ação | CT-03, CT-04, CT-42, CT-43, CT-55 |
| R3 — Enviar vai para gestor do centro; acima de R$ 5.000 vai para diretor depois | fluxo | RQ-04, RQ-05 | BVA 3-valores + máquina de estados | CT-05, CT-06, CT-07, CT-12, CT-13, CT-15, CT-17, CT-44, CT-46, CT-53 |
| R4 — Gestor e diretor aprovam ou rejeitam | decisão | RQ-06, RQ-07 | tabela de decisão | CT-08, CT-11, CT-14, CT-16, CT-18, CT-19, CT-48 |
| R5 — Rejeitada volta para rascunho, sem apagar histórico | máquina de estados | RQ-08, RQ-09 | 2-switch | CT-21, CT-22, CT-23 |
| R6 — Aprovada é terminal; nada mais mexe | máquina de estados | RQ-10 | estado × evento | CT-09, CT-24, CT-25, CT-26, CT-44 |
| R7 — Cancelar antes da aprovação final | máquina de estados | RQ-11 | tabela estado × evento | CT-24, CT-25, CT-26, CT-27 |
| R8 — Status e histórico visíveis | leitura | RQ-12, RQ-13 | tabela de decisão | CT-20, CT-28, CT-29, CT-51 |
| R9 — Notificar o próximo aprovador por e-mail | efeito colateral | RQ-14 | rastreio de efeito | CT-10, CT-14, CT-23, CT-28, CT-30, CT-31 |
| R10 — Concorrência não grava duas etapas | concorrência | RQ-04, RQ-06 | heurística de race | CT-12, CT-15, CT-30 |

## Fronteira com o Plano

| Item do PRD | Recusado como oráculo porque | Destino |
|---|---|---|
| Nome dos métodos `enviar()`, `aprovar()`, `rejeitar()`, `cancelar()` | escolha de implementação | detalhe do cenário |
| Nome da tabela `etapas_aprovacao_compra` | escolha de implementação | detalhe do cenário |
| Texto exato de e-mails e notificações | comportamento visível que o requisito não determina | oráculo: canal `mail` e destinatário |
| Rótulos dos badges (`Rascunho`, `Aguardando gestor`...) | comportamento visível | oráculo: estado interno mapeado |

**Perguntas em aberto** (replicadas do `00-requisito.md`):
- B01 — "acima de R$ 5.000": premissa adotada = estritamente maior (`>`). CT-07 fixa os dois lados.
- B03 — rejeitada descarta aprovações: premissa adotada = não descarta; histórico append-only. CT-22/CT-23.
- B04 — cancelar depois do gesto e antes do diretor: premissa adotada = recusado. CT-24/CT-25.
- B06 — valor alterado após envio reavalia: premissa adotada = recusado e fluxo mantido. CT-46.

## Setup Global

### Personas
- **Beatriz** — solicitante (`panel_user` da Acme).
- **Ana** — gestora do centro de custo TI.
- **Rui** — gestor de outro centro (RH).
- **Dora** — diretora (`diretor` na Acme).
- **Carla** — `panel_user` da Globex.

### Fixtures
- `SolicitacaoCompra::factory()`, `CentroCusto::factory()`, `User::factory()`, `Tenant::factory()`.
- Estados: `rascunho`, `aguardando_gestor`, `aguardando_diretor`, `aprovada`, `cancelada`.

### Fakes
- `Notification::fake()` / `Mail::fake()` para rastrear e-mail.
- `Queue::fake()` quando necessário.
- `DB::statement` para simular falha após ponto do efeito em CT-31.

### Estratégia de DB
- `RefreshDatabase` global.
- Testes de multi-tenancy usam `TenancyTestCase` em `tests/FeatureTenancy`.

---

## Regra R1 — Criação em rascunho com descrição, valor e centro de custo

> `RQ-01` · perfil **completo** · técnica: **EP + BVA**

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O solicitante cria uma solicitação com descrição, valor e centro de custo, e ela nasce em rascunho

    Cenário: [CT-01] criação com campos obrigatórios
      Dado que Beatriz está autenticada no /app da Acme
      E existe o centro de custo TI com gestor Ana
      Quando ela cria uma solicitação com descrição "Notebooks", valor 4000,00 e centro TI
      Então a solicitação existe no banco
      E a situação é "rascunho"
      E a solicitante é Beatriz

    Cenário: [CT-02] campos obrigatórios faltantes são recusados
      Dado que Beatriz está no /app da Acme
      Quando ela tenta criar uma solicitação sem descrição
      Então a gravação falha

    Esquema do Cenário: [CT-54] valor negativo, zero e positivo na criação
      Dado que Beatriz está no /app da Acme
      Quando ela cria uma solicitação com valor <valor>
      Então <resultado>

      Exemplos:
        | valor    | resultado                |
        | -0,01    | a gravação falha         |
        | 0,00     | a gravação falha         |
        | 0,01     | a gravação é aceita      |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M1 | `situacao` não inicia em rascunho | CT-01 |
| M2 | valor 0 ou negativo aceito | CT-54 |
| M3 | descrição vazia aceita | CT-02 |

---

## Regra R2 — Só o solicitante edita/exclui em rascunho

> `RQ-02`, `RQ-03` · perfil **completo** · técnica: **matriz papel × ação**

```gherkin
  Regra: Só o solicitante edita ou exclui a solicitação em rascunho

    Esquema do Cenário: [CT-03] edição/exclusão por persona
      Dado que Beatriz criou uma solicitação em rascunho
      Quando <ator> tenta <operacao>
      Então <resultado>

      Exemplos:
        | ator      | operacao          | resultado                                |
        | Beatriz   | editar a descrição | a edição é aceita e o banco reflete    |
        | Ana       | editar a descrição | a operação é recusada                    |
        | Dora      | excluir            | a operação é recusada                    |
        | Beatriz   | excluir            | a solicitação deixa de existir           |

    Cenário: [CT-04] editar por fora do formulário
      Dado que Beatriz criou uma solicitação em rascunho
      E Ana está autenticada
      Quando Ana faz um PUT direto para a rota de edição com valor 9999
      Então a resposta é 403
      E o valor da solicitação continua 4000,00

    Cenário: [CT-43] excluir por fora do formulário
      Dado que Beatriz criou uma solicitação em rascunho
      E Ana está autenticada
      Quando Ana faz um DELETE direto para a rota de exclusão
      Então a resposta é 403
      E a solicitação continua existindo
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M4 | barreira de identidade só no formulário | CT-04, CT-43 |
| M5 | gestor consegue editar rascunho de outro | CT-03 |

---

## Regra R3 — Enviar vai para gestor; acima de R$ 5.000 vai para diretor depois

> `RQ-04`, `RQ-05` · perfil **completo** · técnica: **BVA 3-valores + máquina de estados**

```gherkin
  Regra: Enviar vai para o gestor do centro; acima de R$ 5.000,0 exige diretor depois do gestor

    Cenário: [CT-05] envio sem gestor no centro é recusado
      Dado que Beatriz criou uma solicitação com centro de custo sem gestor
      Quando ela envia a solicitação
      Então a operação é recusada
      E a situação continua rascunho

    Esquema do Cenário: [CT-06] envio define a próxima etapa conforme o valor
      Dado que Beatriz criou uma solicitação com centro TI e gestor Ana
      Quando ela envia uma solicitação de valor <valor>
      Então a situação passa a ser <situacao>
      E a etapa pendente é <etapa>

      Exemplos:
        | valor      | situacao              | etapa   |
        | 4.999,99   | aguardando_gestor     | gestor  |
        | 5.000,00   | aguardando_gestor     | gestor  |
        | 5.000,01   | aguardando_gestor     | gestor  |

    Cenário: [CT-07] aprovação do gestor decide se vai para diretor
      Dado que Beatriz enviou uma solicitação de valor <valor>
      Quando Ana aprova
      Então <resultado>

      Exemplos:
        | valor      | resultado                                              |
        | 4.999,99   | a situação passa a aprovada                           |
        | 5.000,00   | a situação passa a aprovada                           |
        | 5.000,01   | a situação passa a aguardando_diretor e notifica Dora |

    Cenário: [CT-13] centro de custo sem gestor
      Dado que o centro TI foi criado sem gestor
      Quando Beatriz envia uma solicitação
      Então a operação é recusada
      E a situação continua rascunho

    Cenário: [CT-46] alterar o centro de custo após envio não muda o gestor/a alçada
      Dado que Beatriz criou uma solicitação de valor 6.000,00 com centro TI e gestor Ana
      E ela enviou a solicitação
      Quando ela tenta editar o centro para RH (gestor Rui) e o valor para 100,00
      Então a operação é recusada
      E o centro gravado continua TI
      E o valor gravado continua 6.000,00
      E a etapa pendente continua sendo Ana
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M6 | envio sem gestor é aceito | CT-05, CT-13 |
| M7 | valor 5.000,00 exige diretor | CT-06, CT-07 linha 5.000,00 |
| M8 | etapa do diretor vem antes do gestor | CT-07 |
| M9 | alteração em trânsito muda o fluxo | CT-46 |

---

## Regra R4 — Gestor e diretor aprovam ou rejeitam

> `RQ-06`, `RQ-07` · perfil **completo** · técnica: **tabela de decisão**

```gherkin
  Regra: O gestor e o diretor aprovam ou rejeitam, e a rejeição exige justificativa

    Esquema do Cenário: [CT-08] rejeição sem justificativa é recusada
      Dado que Beatriz enviou uma solicitação para o centro TI
      E a situação é <situacao>
      Quando <ator> tenta rejeitar com justificativa "<justificativa>"
      Então <resultado>

      Exemplos:
        | situacao             | ator | justificativa | resultado                |
        | aguardando_gestor    | Ana  | ""            | a rejeição é recusada    |
        | aguardando_gestor    | Ana  | "Sem verba"   | a rejeição é aceita      |
        | aguardando_diretor   | Dora | ""            | a rejeição é recusada    |
        | aguardando_diretor   | Dora | "Sem verba"   | a rejeição é aceita      |

    Cenário: [CT-11] quem não é aprovador da etapa é recusado
      Dado que Beatriz enviou uma solicitação de 6.000,00 para o centro TI
      Quando Dora tenta aprovar antes de Ana
      Então a operação é recusada
      E a situação continua aguardando_gestor

    Cenário: [CT-14] solicitante não aprova a própria solicitação
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      Quando Beatriz tenta aprovar
      Então a operação é recusada
      E a situação continua aguardando_gestor

    Cenário: [CT-16] gestor de outro centro não aprova
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      E Rui é gestor de RH
      Quando Rui tenta aprovar
      Então a operação é recusada
      E a situação continua aguardando_gestor

    Cenário: [CT-18] justificativa vazia rejeitada no model
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      Quando chama o método `rejeitar()` diretamente com justificativa vazia
      Então uma exceção é lançada
      E a situação continua aguardando_gestor

    Cenário: [CT-19] rejeição é aceita com justificativa válida
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      Quando Ana rejeita com justificativa "Sem verba"
      Então a situação passa a rascunho
      E o histórico tem 1 etapa: gestor/Ana/rejeitada
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M10 | justificativa só é exigida no formulário, não no model | CT-18 |
| M11 | diretor aprova antes do gestor | CT-11 |
| M12 | solicitante aprova a própria solicitação | CT-14 |
| M13 | gestor de outro centro aprova | CT-16 |
| M14 | rejeição sem justificativa é aceita | CT-08 |

---

## Regra R5 — Rejeitada volta para rascunho, sem apagar histórico

> `RQ-08`, `RQ-09` · perfil **completo** · técnica: **2-switch**

```gherkin
  Regra: Rejeitada volta para rascunho, e o solicitante pode corrigir e enviar de novo

    Cenário: [CT-21] rejeição volta ao rascunho
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      E Ana rejeitou com justificativa "Sem verba"
      Quando Beatriz corrige o valor para 3.000,00 e envia de novo
      Então a situação passa a aguardando_gestor
      E o histórico tem duas etapas: a rejeição e o novo envio

    Cenário: [CT-22] ciclo de reenvio preserva as etapas anteriores
      Dado que Beatriz enviou, Ana rejeitou, Beatriz reenviou, Ana aprovou e Dora aprovou
      Quando consulta o histórico
      Então o histórico tem 4 etapas: rejeição, aprovação gestor, aprovação diretor

    Cenário: [CT-23] envio após rejeição notifica o próximo aprovador
      Dado que Beatriz enviou e Ana rejeitou
      Quando Beatriz reenvia
      Então uma notificação é enviada para Ana por e-mail
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M15 | rejeição cria estado `rejeitada` em vez de voltar a rascunho | CT-21 |
| M16 | reenvio apaga o histórico do ciclo anterior | CT-22 |
| M17 | reenvio não notifica | CT-23 |

---

## Regra R6 — Aprovada é terminal

> `RQ-10` · perfil **completo** · técnica: **estado × evento**

```gherkin
  Regra: Depois de aprovada nada mais mexe

    Esquema do Cenário: [CT-09] operações sobre aprovada são recusadas
      Dado que Beatriz enviou uma solicitação de 4.000,00
      E Ana aprovou
      Quando <ator> tenta <operacao>
      Então a operação é recusada
      E a situação continua aprovada
      E o histórico tem 1 etapa

      Exemplos:
        | ator      | operacao         |
        | Beatriz   | editar           |
        | Beatriz   | excluir          |
        | Beatriz   | enviar           |
        | Beatriz   | cancelar         |
        | Ana       | aprovar de novo  |
        | Ana       | rejeitar         |

    Cenário: [CT-24] cancelar após aprovada é recusado
      Dado que a solicitação foi aprovada
      Quando Beatriz tenta cancelar
      Então a operação é recusada
      E a situação continua aprovada
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M18 | aprovada permite edição/exclusão/cancelamento | CT-09, CT-24 |
| M19 | aprovada permite nova aprovação | CT-09 |

---

## Regra R7 — Cancelar antes da aprovação final

> `RQ-11` · perfil **completo** · técnica: **estado × evento**

```gherkin
  Regra: O solicitante pode cancelar enquanto a solicitação está em trânsito

    Esquema do Cenário: [CT-25] cancelar em diferentes estados
      Dado que Beatriz criou uma solicitação
      E ela <estado>
      Quando Beatriz tenta cancelar
      Então <resultado>

      Exemplos:
        | estado                        | resultado                       |
        | não enviou                    | a operação é recusada           |
        | enviou e está aguardando_gestor | a operação é aceita; situação passa a cancelada |
        | Ana aprovou e está aguardando_diretor | a operação é aceita; situação passa a cancelada |
        | Ana e Dora aprovaram          | a operação é recusada           |

    Cenário: [CT-26] só o solicitante cancela
      Dado que Beatriz enviou e está aguardando_gestor
      Quando Ana tenta cancelar
      Então a operação é recusada
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M20 | cancelar em rascunho é aceito | CT-25 |
| M21 | aprovador consegue cancelar | CT-26 |
| M22 | cancelar depois de aprovada é aceito | CT-25 |

---

## Regra R8 — Status e histórico visíveis

> `RQ-12`, `RQ-13` · perfil **padrão** · técnica: **tabela de decisão**

```gherkin
  Regra: A tela mostra o status atual e o histórico de quem aprovou cada etapa

    Esquema do Cenário: [CT-20] badge de situação na listagem
      Dado <estado>
      Quando a solicitação é exibida na listagem
      Então o badge mostra "<rotulo>"

      Exemplos:
        | estado              | rotulo              |
        | rascunho            | Rascunho            |
        | aguardando_gestor   | Aguardando gestor   |
        | aguardando_diretor  | Aguardando diretor  |
        | aprovada            | Aprovada            |
        | cancelada           | Cancelada           |

    Cenário: [CT-28] histórico mostra quem decidiu, quando e a justificativa
      Dado que Beatriz enviou, Ana rejeitou com "Sem verba", Beatriz reenviou e Ana aprovou
      Quando a solicitação é exibida na tela de visualização
      Então o histórico tem duas linhas
      E a primeira linha mostra gestor/Ana/rejeitada/Sem verba
      E a segunda linha mostra gestor/Ana/aprovada

    Cenário: [CT-29] ordem do histórico respeita created_at
      Dado que duas etapas foram gravadas em instantes distintos
      Quando a solicitação é exibida
      Então as etapas aparecem na ordem de criação crescente

    Cenário: [CT-51] tela não mostra "Aprovada" enquanto falta a etapa do diretor
      Dado que Beatriz enviou 6.000,00 e Ana aprovou
      Quando a solicitação é exibida
      Então o badge mostra "Aguardando diretor"
      E não mostra "Aprovada"
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M23 | badge mostra "Aprovada" em aguardando_diretor | CT-51 |
| M24 | histórico não mostra justificativa | CT-28 |
| M25 | histórico é sobrescrito no reenvio | CT-22, CT-28 |

---

## Regra R9 — Notificar o próximo aprovador por e-mail

> `RQ-14` · perfil **padrão** · técnica: **rastreio de efeito**

```gherkin
  Regra: O avanço da solicitação notifica o próximo aprovador por e-mail

    Cenário: [CT-10] envio notifica o gestor
      Dado que Beatriz enviou uma solicitação de 4.000,00 para o centro TI
      Então uma notificação por e-mail é enviada para Ana
      E nem Beatriz nem Dora recebem notificação

    Cenário: [CT-14] aprovação do gestor notifica o diretor
      Dado que Beatriz enviou 6.000,00 para o centro TI
      Quando Ana aprova
      Então uma notificação é enviada para Dora
      E Beatriz não recebe notificação
      E o histórico tem 1 etapa

    Cenário: [CT-23] reenvio notifica o próximo aprovador
      Dado que Beatriz enviou, Ana rejeitou e Beatriz reenviou
      Então uma notificação é enviada para Ana

    Cenário: [CT-30] aprovação final não notifica ninguém
      Dado que Beatriz enviou 6.000,00, Ana aprovou e Dora vai aprovar
      Quando Dora aprova
      Então a situação passa a aprovada
      E nenhuma notificação adicional é enviada para Ana, Rui ou Beatriz

    Cenário: [CT-31] e-mail não sai se a gravação da aprovação falha
      Dado que Beatriz enviou 4.000,00
      Quando Ana aprova e uma falha é forçada após o ponto da notificação
      Então a operação falha
      E a solicitação continua aguardando_gestor
      E Ana não recebe notificação
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M26 | e-mail vai para o aprovador errado | CT-10, CT-14, CT-23 |
| M27 | notificação duplicada | CT-14, CT-23 |
| M28 | aprovação final notifica alguém | CT-30 |
| M29 | e-mail sai mesmo quando a gravação da aprovação falha | CT-31 |

---

## Regra R10 — Concorrência não grava duas etapas

> `RQ-04`, `RQ-06` · perfil **completo** · técnica: **heurística de race**

```gherkin
  Regra: Duas aprovações simultâneas não avançam duas etapas de uma vez

    Cenário: [CT-12] dois diretores aprovam ao mesmo tempo
      Dado que Beatriz enviou 6.000,00, Ana aprovou e a situação é aguardando_diretor
      Quando Dora e outra diretora aprovam simultaneamente
      Então exatamente uma aprovação é aceita
      E a situação passa a aprovada
      E o histórico tem exatamente 2 etapas (gestor e diretor)

    Cenário: [CT-15] duplo clique do gestor não grava duas etapas
      Dado que Beatriz enviou 4.000,00
      Quando duas requisições de Ana aprovar chegam simultaneamente
      Então exatamente uma é aceita
      E o histórico tem 1 etapa
      E a situação é aprovada

    Cenário: [CT-47] reenvio concorrente em rascunho
      Dado que Ana rejeitou e a situação é rascunho
      Quando Beatriz reenvia e simultaneamente edita a solicitação
      Então o envio é aceito ou a edição é aceita, nunca ambos inconsistentes
      E o histórico reflete uma única transição
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M30 | duas aprovações simultâneas gravam duas etapas | CT-12, CT-15 |
| M31 | reenvio concorrente grava histórico duplicado | CT-47 |

---

## Cenários adicionais de fronteira

```gherkin
  Cenário: [CT-27] ordem de etapas com empate no histórico
      Dado que duas etapas do mesmo tipo foram gravadas no mesmo segundo
      Quando a solicitação é exibida
      Então a ordem é determinística (por id ou por created_at secundário)

  Cenário: [CT-44] aprovada não aceita cancelar
      Dado que a solicitação foi aprovada
      Quando Beatriz tenta cancelar
      Então a operação é recusada
      E a situação continua aprovada

  Cenário: [CT-45] rejeição em aguardando_diretor volta ao rascunho
      Dado que Beatriz enviou 6.000,00 e Ana aprovou
      Quando Dora rejeita com justificativa "Acima do orçamento"
      Então a situação passa a rascunho
      E o histórico tem 2 etapas

  Cenário: [CT-48] aprovação final não exige justificativa
      Dado que Beatriz enviou 4.000,00
      Quando Ana aprova
      Então a situação passa a aprovada
      E a etapa gravada tem justificativa nula

  Cenário: [CT-52] gestora do próprio centro (solicitante = gestora) ainda precisa de diretor
      Dado que Beatriz é a gestora do centro TI
      Quando ela envia 6.000,00
      Então a situação é aguardando_gestor
      E quem pode aprovar é Beatriz
      Quando ela aprova
      Então a situação passa a aguardando_diretor
      E Dora pode aprovar

  Cenário: [CT-53] mudança de centro em rascunho recalcula gestor
      Dado que Beatriz criou uma solicitação com centro TI
      Quando ela edita o centro para RH antes de enviar
      Então o gestor a ser notificado no envio é Rui
      E Ana não é notificada
```

## Checklist de Taxonomia

| Item | Cenário que mata |
|---|---|
| IDOR / autorização horizontal | CT-04, CT-16, CT-26, CT-43, CT-52 |
| Autorização exercida na ação (não só `can()`) | CT-04, CT-18, CT-43 |
| Idempotência (ancorada no agregado) | CT-12, CT-15, CT-47 |
| Concorrência | CT-12, CT-15, CT-31, CT-47 |
| Fronteira no ponto de entrada (gravação) | CT-01, CT-02, CT-54 |
| Domínio condicionado (valor × alçada) | CT-06, CT-07 |
| Estado × operação de escrita | CT-09, CT-24, CT-25, CT-44, CT-45 |
| Ausente ≠ null ≠ vazio | CT-08, CT-18 |
| Timezone / DST | — não se aplica: nenhuma data de borda de fuso no requisito |
| Unicode / limite de varchar | CT-02 |
| CRUD combinado | CT-03, CT-04, CT-42, CT-43 |
| Mass assignment | CT-46, CT-53 |
| Precisão monetária | CT-06, CT-07, CT-54 |

## Índice de Cenários

| ID | Cenário | Regra | Técnica | Camada | Arquivo | Mata |
|----|---------|-------|---------|--------|---------|------|
| CT-01 | criação rascunho | R1 | EP | Livewire | SolicitacaoCompraCrudTest | M1 |
| CT-02 | campos obrigatórios | R1 | EP | Livewire | SolicitacaoCompraCrudTest | M3 |
| CT-03 | edição/exclusão por persona | R2 | matriz | Livewire | SolicitacaoCompraCrudTest | M5 |
| CT-04 | edição por fora do form | R2 | autorização | Feature | SolicitacaoCompraTest | M4 |
| CT-05 | envio sem gestor | R3 | BVA | Feature | SolicitacaoCompraTest | M6 |
| CT-06 | envio define etapa | R3 | BVA 3-valores | Feature | SolicitacaoCompraTest | M7 |
| CT-07 | aprovação decide fluxo | R3 | BVA 3-valores | Feature | SolicitacaoCompraTest | M7, M8 |
| CT-08 | rejeição sem justificativa | R4 | tabela de decisão | Feature | SolicitacaoCompraTest | M10, M14 |
| CT-09 | operações sobre aprovada | R6 | estado × evento | Feature | SolicitacaoCompraTest | M18, M19 |
| CT-10 | envio notifica gestor | R9 | rastreio de efeito | Feature | SolicitacaoCompraTest | M26 |
| CT-11 | diretor antes do gestor | R3/R4 | máquina de estados | Feature | SolicitacaoCompraTest | M8 |
| CT-12 | dois diretores aprovam | R10 | race | Feature | SolicitacaoCompraTest | M30 |
| CT-13 | centro sem gestor | R3 | BVA | Feature | SolicitacaoCompraTest | M6 |
| CT-14 | solicitante não aprova | R4 | matriz | Feature | SolicitacaoCompraTest | M12 |
| CT-15 | duplo clique gestor | R10 | race | Feature | SolicitacaoCompraTest | M30 |
| CT-16 | gestor de outro centro | R4 | IDOR | FeatureTenancy | SolicitacaoCompraTenancyTest | M13 |
| CT-17 | diretora de outra org | R4 | IDOR | FeatureTenancy | SolicitacaoCompraTenancyTest | M13 |
| CT-18 | justificativa vazia no model | R4 | rastreio | Feature | SolicitacaoCompraTest | M10 |
| CT-19 | rejeição com justificativa | R4 | tabela | Feature | SolicitacaoCompraTest | M14 |
| CT-20 | badges de situação | R8 | tabela | Livewire | SolicitacaoCompraCrudTest | M23 |
| CT-21 | rejeição volta a rascunho | R5 | 2-switch | Feature | SolicitacaoCompraTest | M15 |
| CT-22 | histórico preserva ciclo anterior | R5 | 2-switch | Feature | SolicitacaoCompraTest | M16, M25 |
| CT-23 | reenvio notifica | R5/R9 | rastreio | Feature | SolicitacaoCompraTest | M17 |
| CT-24 | cancelar em trânsito | R7 | estado × evento | Feature | SolicitacaoCompraTest | M20, M22 |
| CT-25 | cancelar em diferentes estados | R7 | tabela | Feature | SolicitacaoCompraTest | M20, M22 |
| CT-26 | só solicitante cancela | R7 | matriz | Feature | SolicitacaoCompraTest | M21 |
| CT-27 | ordem do histórico | R8 | ordenação | Feature | SolicitacaoCompraTest | — |
| CT-28 | histórico mostra quem/justificativa | R8 | rastreio | Feature | SolicitacaoCompraTest | M24, M25 |
| CT-29 | ordem crescente do histórico | R8 | ordenação | Feature | SolicitacaoCompraTest | — |
| CT-30 | aprovação final não notifica | R9 | rastreio | Feature | SolicitacaoCompraTest | M28 |
| CT-31 | e-mail não sobrevive a falha | R9 | atomicidade | Feature | SolicitacaoCompraTest | M29 |
| CT-42 | criação por fora do form | R2 | autorização | Feature | SolicitacaoCompraTest | M4 |
| CT-43 | exclusão por fora do form | R2 | autorização | Feature | SolicitacaoCompraTest | M4 |
| CT-44 | aprovada não cancela | R6 | estado × evento | Feature | SolicitacaoCompraTest | M18 |
| CT-45 | rejeição em aguardando_diretor | R5/R6 | máquina de estados | Feature | SolicitacaoCompraTest | — |
| CT-46 | alteração em trânsito recusada | R3 | CRUD + autorização | Feature | SolicitacaoCompraTest | M9 |
| CT-47 | reenvio concorrente | R10 | race | Feature | SolicitacaoCompraTest | M31 |
| CT-48 | aprovação final sem justificativa | R4 | tabela | Feature | SolicitacaoCompraTest | — |
| CT-49 | histórico com quem decidiu | R8 | rastreio | Feature | SolicitacaoCompraTest | M24 |
| CT-50 | notificação no envio sem gestor | R3/R9 | rastreio | Feature | SolicitacaoCompraTest | M6, M26 |
| CT-51 | badge não mostra aprovada faltando diretor | R8 | estado × evento | Livewire | SolicitacaoCompraCrudTest | M23 |
| CT-52 | solicitante = gestora precisa de diretor | R4 | matriz | Feature | SolicitacaoCompraTest | M12 |
| CT-53 | mudança de centro em rascunho | R3 | CRUD | Feature | SolicitacaoCompraTest | — |
| CT-54 | valor negativo/zero/positivo | R1 | BVA 3-valores | Livewire | SolicitacaoCompraCrudTest | M2 |
# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Runtime: `pest-plugin-browser` (Playwright). O plugin sobe o próprio servidor.  
> Comando: `vendor/bin/pest --testsuite=Browser` (em série — nunca `--parallel`)

## Pré-requisitos

- [ ] `npm run build` executado
- [ ] `tests/Browser/Screenshots` no `.gitignore`
- [ ] Autenticação por `$this->actingAs($user)`

## Seletores

| Elemento | Seletor | Já existe? |
|---|---|---|
| Listagem de solicitações | `[data-testid="table"]` | — |
| Badge de situação | `[data-testid="situacao-badge"]` | — |
| Botão Enviar | `button:contains("Enviar")` | — |
| Botão Aprovar | `button:contains("Aprovar")` | — |
| Botão Rejeitar | `button:contains("Rejeitar")` | — |
| Modal de justificativa | `textarea[name="data.justificativa"]` | — |
| Botão Cancelar | `button:contains("Cancelar")` | — |

---

## CT-B01 — Fluxo feliz entre três personas na tela

**Por que browser e não Livewire**: o fluxo atravessa múltiplas telas e personas; só o navegador prova que cada persona encontra/exclui os botões corretos.

```gherkin
# language: pt
  Cenário: [CT-B01] solicitante envia, gestor aprova e diretor aprova
    Dado que Beatriz está autenticada no /app da Acme
    E existe o centro TI com gestora Ana
    E Dora tem o papel diretor na Acme
    Quando Beatriz visita /app/acme/solicitacoes-de-compra
    E cria uma solicitação de 6.000,00 para o centro TI
    Então a listagem mostra a situação "Aguardando gestor"
    E Beatriz não vê o botão "Aprovar"

    Quando Ana acessa /app/acme/solicitacoes-de-compra
    Então ela vê o botão "Aprovar" na linha da solicitação
    E ela aprova
    Então a situação passa a "Aguardando diretor"

    Quando Dora acessa /app/acme/solicitacoes-de-compra
    Então ela vê o botão "Aprovar"
    E ela aprova
    Então a situação passa a "Aprovada"
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | Beatriz create | `actingAs(Beatriz)->visit('/app/acme/solicitacoes-de-compra/create')` | formulário carrega |
| 2 | preencher e salvar | `->type('data.descricao','Notebooks')->type('data.valor','6000,00')->select('data.centro_custo_id', $ti->id)->press('Salvar')` | redireciona para listagem |
| 3 | checar badge | `->assertPathIs('/app/acme/solicitacoes-de-compra')->assertSee('Aguardando gestor')` | badge correto |
| 4 | Ana aprova | `actingAs(Ana)->visit('/app/acme/solicitacoes-de-compra')->press('Aprovar')->assertPathIs('/app/acme/solicitacoes-de-compra')` | badge "Aguardando diretor" |
| 5 | Dora aprova | `actingAs(Dora)->visit(...)->press('Aprovar')` | badge "Aprovada" |

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M32 | botão Aprovar visível para o solicitante | CT-B01 passo 3 |
| M33 | aprovação do gestor não muda o badge | CT-B01 passo 4 |
| M34 | badge mostra "Aprovada" em aguardando_diretor | CT-B01 passo 4 |

---

## CT-B02 — Rejeição exige justificativa no modal

**Por que browser e não Livewire**: o modal de justificativa é UI com formulário e confirmação; a validação de campo vazio só se prova no navegador.

```gherkin
# language: pt
  Cenário: [CT-B02] gestor rejeita com e sem justificativa
    Dado que Beatriz criou e enviou uma solicitação de 4.000,00 para o centro TI
    E Ana está autenticada
    Quando ela clica em "Rejeitar"
    Então um modal com campo "Motivo da rejeição" aparece

    Quando ela confirma sem preencher o motivo
    Então a tela mostra erro no campo
    E a situação continua "Aguardando gestor"

    Quando ela preenche "Sem verba" e confirma
    Então a situação passa a "Rascunho"
    E Beatriz vê a justificativa na tela de visualização
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | abrir rejeição | `actingAs(Ana)->visit('/app/acme/solicitacoes-de-compra')->press('Rejeitar')` | modal abre |
| 2 | confirmar vazio | `->press('Rejeitar')` | mensagem de erro |
| 3 | preencher e confirmar | `->type('data.justificativa','Sem verba')->press('Rejeitar')->assertPathIs(...)->assertSee('Rascunho')` | situação muda |

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M35 | modal não exige justificativa | CT-B02 passo 2 |

---

## CT-B03 — Ausência de ação para quem não pode agir

**Por que browser e não Livewire**: affordance (botão visível/invisível) depende de JS e estado do componente.

```gherkin
# language: pt
  Cenário: [CT-B03] diretor não vê ação antes do gestor
    Dado que Beatriz enviou 6.000,00 para o centro TI
    Quando Dora acessa /app/acme/solicitacoes-de-compra
    Então ela não vê o botão "Aprovar" na linha da solicitação

    Quando Ana aprova
    E Dora acessa a listagem novamente
    Então ela vê o botão "Aprovar"
```

**Roteiro executável**

| # | Ação | Código Pest | Resultado visível |
|---|---|---|---|
| 1 | Dora sem ação | `actingAs(Dora)->visit('/app/acme/solicitacoes-de-compra')->assertDontSee('Aprovar')` | botão ausente |
| 2 | Ana aprova (componente) | `actingAs(Ana)->visit(...)->press('Aprovar')` | badge muda |
| 3 | Dora com ação | `actingAs(Dora)->visit(...)->assertSee('Aprovar')` | botão presente |

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata |
|---|---|---|
| M36 | diretor vê Aprovar antes do gestor | CT-B03 passo 1 |

---

## Roteiro de Validação: Desenhado × Implementado

| # | O que o PRD desenhou | O que foi implementado | Confere? | Evidência |
|---|---|---|---|---|
| 1 | Badge reflete situação real | a implementar | — | — |
| 2 | Botões aparecem só para quem pode agir | a implementar | — | — |
| 3 | Modal de rejeição exige justificativa | a implementar | — | — |
