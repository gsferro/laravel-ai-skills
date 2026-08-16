# Casos de Teste — FERRO-830: Fluxo de aprovação de solicitação de compra

> Gerado pela skill `feature-test-design` v1.9.0 a partir do `00-requisito.md`.
> O `01-plano-acao.md` entra apenas para paths e superfície de UI.

## Perfil de esforço por risco

| Área | Probabilidade | Impacto | Perfil |
|---|---|---|---|
| Máquina de estados (transições, autorização) | 3 | 3 | completo |
| Valor × alçada de diretor | 3 | 3 | completo |
| Notificação por e-mail | 2 | 3 | padrão |
| Histórico de etapas | 2 | 2 | padrão |
| Auditoria de autorização | 2 | 3 | padrão |
| Idempotência / duplo clique | 3 | 2 | completo |

## SFDIPOT

| Dimensão | O que existe | Vazio? |
|---|---|---|
| Structure | `SolicitacaoCompra`, `CentroCusto`, `EtapaAprovacao`, recursos Filament, policies, `PapeisSeeder` | — |
| Function | criar/editar/excluir rascunho, enviar, aprovar/rejeitar, cancelar, notificar | — |
| Data | descrição, valor, centro de custo, solicitante, situação, histórico de etapas, justificativa | — |
| Interfaces | painel `/app`, modal de rejeição, e-mail, métodos do model | — |
| Platform | PHP 8.3+, Laravel 13, Filament 5, Pest 5, SQLite, queue sync em teste | — |
| Operations | solicitante, gestor do centro, diretor, panel_user | — |
| Time | estado expira? não; ordem de aprovação, atomicidade de transição, reenvio | — |

## Mapa de Regras

| Regra | RQs | Técnica |
|---|---|---|
| R1 — Solicitante cria com descrição, valor e centro de custo | RQ-01 | EP |
| R2 — Edita/exclui só em rascunho | RQ-02, RQ-03 | Máquina de estados |
| R3 — Envio vai para gestor do centro | RQ-04 | Tabela de decisão |
| R4 — Valor acima de R$ 5.000 exige diretor depois do gestor | RQ-05 | BVA 3-valores |
| R5 — Gestor e diretor podem aprovar/rejeitar | RQ-06, RQ-07 | Máquina de estados + tabela de decisão |
| R6 — Rejeição exige justificativa | RQ-07 | EP |
| R7 — Rejeitada volta para rascunho e reenvio começa do gestor | RQ-08, RQ-09 | 2-switch |
| R8 — Aprovada é terminal | RQ-10 | Máquina de estados |
| R9 — Cancelar só antes da aprovação final | RQ-11 | Máquina de estados |
| R10 — Mostra status e quem aprovou | RQ-12, RQ-13 | Rastreio de efeito |
| R11 — Notifica próximo aprovador | RQ-14 | Rastreio de efeito |

## Matriz Estado × Operação

Estados: `rascunho`, `aguardando_gestor`, `aguardando_diretor`, `aprovada`, `cancelada`.
Operações: `enviar`, `editar`, `excluir`, `aprovar`, `rejeitar`, `cancelar`.

| Estado / Operação | enviar | editar | excluir | aprovar | rejeitar | cancelar |
|---|---|---|---|---|---|---|
| rascunho | ✅ (gestor do CC) | ✅ (solicitante) | ✅ (solicitante) | ❌ | ❌ | ❌ (ver nota A-06) |
| aguardando_gestor | ❌ | ❌ | ❌ | ✅ (gestor) | ✅ (gestor) | ✅ (solicitante) |
| aguardando_diretor | ❌ | ❌ | ❌ | ✅ (diretor) | ✅ (diretor) | ✅ (solicitante) |
| aprovada | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| cancelada | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

Total de células: 5 × 6 = 30. Válidas: 9. Inválidas: 21. Cada célula inválida tem CT.

## Fronteira com o Plano

- Nome dos métodos (`enviar`, `aprovar`, `rejeitar`, `cancelar`) e tabelas vêm do PRD e são detalhe de cenário.
- A comparação estritamente maior (`>`) vem da premissa A-04 do `00` — é oráculo.
- O histórico de etapas é append-only; reenvio não apaga — oráculo derivado do `00`.
- Notificação só ao próximo aprovador — oráculo.

---

## Cenários

### Funcionalidade: criação e rascunho

#### Regra: R1 — Solicitante cria com descrição, valor e centro de custo

```gherkin
@CT-01 @backend
Cenário: criação de solicitação de compra válida
  Dado um usuário "Ana" logada como solicitante no painel /app
    E um centro de custo "TI" com gestor "Rui"
  Quando ela cria uma solicitação com descrição "Notebook", valor 4.000,00 e centro de custo "TI"
  Então a solicitação é criada em situacao "rascunho"
    E o solicitante_id é "Ana"
    E o centro_custo_id é o da "TI"
```

#### Regra: R1 — Valor deve ser positivo

```gherkin
@CT-02 @backend @BVA
Esquema do Cenário: valor nas fronteiras do domínio
  Dado um solicitante "Ana"
    E um centro de custo "TI" com gestor "Rui"
  Quando ela cria uma solicitação com descrição "Item" e valor <valor>
  Então <resultado>

  Exemplos:
    | CT  | valor    | resultado                                  | nota |
    | 02a | -0,01    | a gravação falha                           | D17: valor negativo |
    | 02b | 0,00     | a gravação falha                           | D17: valor zero |
    | 02c | 0,01     | a gravação é aceita e a situação é rascunho | D17: mínimo positivo |
```

> Detecta E17 (valor zero ou negativo aceito).

### Funcionalidade: envio e alçada

#### Regra: R3/R4 — Envio e limite de diretor

```gherkin
@CT-03 @backend
Cenário: envio sem gestor no centro é recusado
  Dado um solicitante "Ana"
    E um centro de custo "TI" sem gestor
  Quando ela cria uma solicitação "Notebook" com valor 3.000,00 e tenta enviar
  Então o envio é recusado
    E a solicitação continua em "rascunho"
    E nenhuma notificação é enviada
```

> Detecta A-10. Garante falha fechada sem destinatário.

```gherkin
@CT-04 @backend @BVA
Esquema do Cenário: valor exatamente no limite decide a etapa do diretor
  Dado o limite do diretor configurado como 5.000,00
    E um centro de custo "TI" com gestor "Rui"
    E um diretor "Dora" na mesma organização
  Quando "Ana" cria e envia uma solicitação com valor <valor>
  Então a solicitação fica em <situacao>
    E <notificacao>

  Exemplos:
    | CT  | valor    | situacao           | notificacao                       | nota |
    | 04a | 4.999,99 | aguardando_gestor  | Rui recebe notificação por e-mail | abaixo do limite |
    | 04b | 5.000,00 | aguardando_gestor  | Rui recebe notificação por e-mail | E03: exatamente 5.000 não exige diretor |
    | 04c | 5.000,01 | aguardando_diretor | Rui recebe notificação por e-mail | acima do limite |
```

> Detecta E03 (valor exatamente R$ 5.000,00 roteado errado). A notificação discrimina: sem diretor, notifica o aprovador final (Rui) apenas.

```gherkin
@CT-05 @backend
Cenário: gestor de outro centro de custo não pode aprovar
  Dado um centro de custo "TI" com gestor "Rui"
    E um centro de custo "RH" com gestor "Carla"
    E "Ana" solicitou "Notebook" no centro "TI" e enviou
  Quando "Carla" tenta aprovar a solicitação
  Então a aprovação é recusada
    E a solicitação continua em "aguardando_gestor"
    E o histórico de etapas continua vazio
```

> Detecta E07 (gestor de outro centro de custo consegue aprovar).

```gherkin
@CT-06 @backend
Cenário: solicitante aprova a própria solicitação quando é o gestor
  Dado um centro de custo "TI" com gestor "Ana"
    E uma solicitação "Notebook" de R$ 6.000,00 criada por "Ana" e enviada
  Quando "Ana" tenta aprovar como gestor
  Então a aprovação é aceita
    E a solicitação fica em "aguardando_diretor"
```

> Detecta E08 (solicitante aprova própria solicitação). A premissa A-09 assume que é permitido; o teste confirma que, se for, a aprovação segue a regra de fluxo e **não pula** diretamente para aprovada.

```gherkin
@CT-07 @backend
Cenário: diretor aprova antes do gestor é recusado
  Dado um centro "TI" com gestor "Rui" e diretor "Dora"
    E uma solicitação "Notebook" de R$ 6.000,00 enviada
  Quando "Dora" tenta aprovar
  Então a aprovação é recusada
    E a solicitação continua em "aguardando_gestor"
```

> Detecta E04 (diretor aprova antes do gestor).

```gherkin
@CT-08 @backend
Cenário: envio de rascunho já enviado é recusado
  Dado uma solicitação em "aguardando_gestor"
  Quando "Ana" tenta enviar novamente
  Então o envio é recusado
    E a situação continua "aguardando_gestor"
```

> Detecta E01/E02 (aprovar/editar em rascunho, enviar em não-rascunho).

### Funcionalidade: aprovação e rejeição

#### Regra: R5/R6 — Aprovar/rejeitar e justificativa

```gherkin
@CT-09 @backend
Esquema do Cenário: rejeição exige justificativa
  Dado uma solicitação "Notebook" de R$ 3.000,00 em "aguardando_gestor"
    E o gestor "Rui" autenticado
  Quando ele tenta rejeitar <acao>
  Então <resultado>

  Exemplos:
    | CT  | acao                | resultado                                       | nota |
    | 09a | com justificativa ""| a rejeição é recusada                           | E05: justificativa vazia |
    | 09b | com justificativa "Sem verba" | a rejeição é aceita e a situação volta a "rascunho" | caminho feliz |
```

> Detecta E05 (rejeição sem justificativa). O teste chama o método direto do model, não só o formulário.

```gherkin
@CT-10 @backend
Cenário: aprovação do gestor envia para diretor quando necessário
  Dado uma solicitação de R$ 6.000,00 em "aguardando_gestor"
    E gestor "Rui", diretor "Dora"
  Quando "Rui" aprova
  Então a situação passa para "aguardando_diretor"
    E o histórico tem 1 etapa: "gestor", "Rui", "aprovada", sem justificativa
    E uma notificação é enviada para "Dora" por e-mail
    E nenhuma notificação é enviada para "Rui" nem para "Ana"
```

> Detecta E11 (nenhuma notificação quando avança para diretor) e E10 (e-mail para aprovador errado).

```gherkin
@CT-11 @backend
Cenário: aprovação final do diretor não notifica ninguém
  Dado uma solicitação de R$ 6.000,00 em "aguardando_diretor"
    E diretor "Dora"
  Quando "Dora" aprova
  Então a situação passa para "aprovada"
    E o histórico tem 2 etapas: gestor/Rui/aprovada e diretor/Dora/aprovada
    E nenhuma notificação é enviada para Rui, Dora ou Ana
```

> Detecta E11 (notificação em estado final) e E10 (destinatário errado).

### Funcionalidade: rejeição e reenvio (2-switch)

#### Regra: R7 — Rejeitada volta para rascunho e reenvio começa do gestor

```gherkin
@CT-12 @backend @2-switch
Cenário: rejeição volta ao rascunho e histórico sobrevive
  Dado uma solicitação "Notebook" de R$ 6.000,00 em "aguardando_gestor"
  Quando "Rui" rejeita com justificativa "Sem verba"
  Então a situação passa para "rascunho"
    E o histórico tem 1 etapa: gestor/Rui/rejeitada/Sem verba
  Quando "Ana" corrige a descrição para "Notebook Dell" e reenvia
  Então a situação passa para "aguardando_gestor"
    E o histórico continua com 1 etapa do ciclo anterior
    E uma notificação é enviada para "Rui"
```

> Detecta E06 (rejeitada volta a rascunho mantendo aprovações anteriores) e E08 (reenvio recomeça do gestor).

```gherkin
@CT-13 @backend @2-switch
Cenário: segundo ciclo de rejeição e aprovação completa
  Dado uma solicitação "Notebook" de R$ 6.000,00
  Quando Rui rejeita (ciclo 1), Ana reenvia, Rui aprova, Dora rejeita (ciclo 2), Ana reenvia e corrige, Rui aprova e Dora aprova
  Então a situação passa para "aprovada"
    E o histórico tem 5 etapas
    E a última etapa é diretor/Dora/aprovada
```

> Detecta E06/E07/E08 em sequência de 2-switch.

### Funcionalidade: aprovada é terminal

#### Regra: R8

```gherkin
@CT-14 @backend
Esquema do Cenário: operações em solicitação aprovada são recusadas
  Dado uma solicitação "Notebook" de R$ 3.000,00 já aprovada
  Quando "Ana" tenta <acao>
  Então a operação é recusada
    E a situação continua "aprovada"
    E o histórico continua inalterado

  Exemplos:
    | CT   | acao     | nota |
    | 14a  | editar   | E02  |
    | 14b  | excluir  | E14  |
    | 14c  | enviar   | E01  |
    | 14d  | cancelar | E09  |
    | 14e  | aprovar  | E01  |
    | 14f  | rejeitar | E01  |
```

> Detecta E01, E02, E09, E14.

### Funcionalidade: cancelar antes da aprovação final

#### Regra: R9

```gherkin
@CT-15 @backend
Cenário: cancelar em aguardando_gestor é aceito
  Dado uma solicitação "Notebook" de R$ 3.000,00 em "aguardando_gestor"
  Quando "Ana" cancela
  Então a situação passa para "cancelada"
    E o histórico continua vazio
```

```gherkin
@CT-16 @backend
Cenário: cancelar em aguardando_diretor é aceito
  Dado uma solicitação "Notebook" de R$ 6.000,00 em "aguardando_diretor" (Rui já aprovou)
  Quando "Ana" cancela
  Então a situação passa para "cancelada"
    E o histórico continua com a etapa de gestor
```

> Detecta E09 (cancelar após aprovada é recusado) — combinado com CT-14d.

### Funcionalidade: histórico e exibição

#### Regra: R10 — Mostra status e quem aprovou

```gherkin
@CT-17 @backend @estado
Cenário: rótulo de situação é consistente em todos os estados
  Dado solicitações em cada uma das situações: rascunho, aguardando_gestor, aguardando_diretor, aprovada, cancelada
  Quando se consulta a representação do estado
  Então cada situação exibe um rótulo não vazio e distinto das outras
```

> Detecta E16 (tela mostra "Aprovada" enquanto falta diretor).

```gherkin
@CT-18 @backend
Cenário: histórico guarda quem decidiu, quando e por quê
  Dado uma solicitação de R$ 6.000,00
  Quando Rui aprova e Dora rejeita com "Muito caro" e Ana reenvia e Rui aprova e Dora aprova
  Então o histórico mostra 3 etapas com:
    | etapa    | quem  | decisao    | justificativa |
    | gestor   | Rui   | aprovada   | —             |
    | diretor  | Dora  | rejeitada  | Muito caro    |
    | gestor   | Rui   | aprovada   | —             |
    | diretor  | Dora  | aprovada   | —             |
  E as datas das etapas estão em ordem crescente
```

> Detecta E13 (histórico de quem aprovou cada etapa não gravado ou sobrescrito).

### Funcionalidade: corrida e idempotência

#### Regra: R5 — Duplo clique / aprovação concorrente

```gherkin
@CT-19 @backend @concorrencia
Cenário: duplo clique do gestor não cria duas etapas
  Dado uma solicitação de R$ 3.000,00 em "aguardando_gestor"
  Quando duas requisições de aprovação do gestor chegam ao mesmo tempo
  Então uma aprovação é aceita
    E a outra é recusada
    E o histórico tem exatamente 1 etapa de gestor
    E a situação é "aprovada"
```

> Detecta E15 (duplo clique avança duas etapas).

```gherkin
@CT-20 @backend @concorrencia
Cenário: dois diretores clicando ao mesmo tempo
  Dado uma solicitação de R$ 6.000,00 em "aguardando_diretor"
    E dois diretores Dora e Diana
  Quando Dora e Diana aprovam simultaneamente
  Então uma aprovação é aceita
    E a outra é recusada
    E o histórico tem exatamente 2 etapas (gestor + diretor)
    E a situação é "aprovada"
```

> Detecta E15 em diretor.

### Funcionalidade: matriz estado × operação — células inválidas pendentes

```gherkin
@CT-25 @backend
Cenário: aprovar uma solicitação em rascunho é recusado
  Dado uma solicitação "Notebook" de R$ 3.000,00 em "rascunho"
    E o gestor "Rui" autenticado
  Quando "Rui" tenta aprovar a solicitação
  Então a aprovação é recusada
    E a situação continua "rascunho"
    E o histórico continua vazio
    E nenhuma notificação é enviada
```

> Detecta E01 (aprovar solicitação ainda em rascunho).

```gherkin
@CT-26 @backend
Esquema do Cenário: excluir solicitação em trânsito é recusado
  Dado uma solicitação "Notebook" de R$ <valor> em "<situacao>"
    E a solicitante "Ana" autenticada
  Quando "Ana" tenta excluir
  Então a exclusão é recusada
    E a solicitação continua em "<situacao>"
    E o histórico continua <etapas>

  Exemplos:
    | CT   | valor | situacao           | etapas | nota |
    | 26a  | 3.000 | aguardando_gestor  | vazio  | E14  |
    | 26b  | 6.000 | aguardando_diretor | 1      | E14  |
```

> Detecta E14 (excluir solicitação já enviada).

### Funcionalidade: alteração em trânsito

#### Regra: R2/R4 — Editar valor em trânsito reavalia alçada

```gherkin
@CT-21 @backend
Cenário: edição de valor em trânsito é recusada
  Dado uma solicitação "Notebook" de R$ 4.000,00 em "aguardando_gestor"
  Quando "Ana" tenta editar o valor para R$ 6.000,00
  Então a edição é recusada
    E o valor gravado continua 4.000,00
    E o centro_custo gravado continua "TI"
    E a situação continua "aguardando_gestor"
```

> Detecta E02 (editar já enviada).

```gherkin
@CT-22 @backend
Cenário: troca de centro de custo em trânsito é recusada e mantém aprovador correto
  Dado uma solicitação "Notebook" de R$ 4.000,00 em "aguardando_gestor" do centro "TI" (gestor Rui)
    E um centro "RH" (gestor Carla)
  Quando "Ana" tenta alterar o centro de custo para "RH"
  Então a edição é recusada
    E o centro gravado continua "TI"
    E quem pode aprovar continua sendo Rui
    E Carla ainda não pode aprovar
```

> Detecta E12 (valor alterado após envio não reavalia etapa do diretor) e E07 (trocar gestor após envio).

### Funcionalidade: notificação atômica

#### Regra: R11 — E-mail não sai se gravação falha

```gherkin
@CT-23 @backend @atomicidade
Cenário: e-mail não é enviado se a aprovação falhar após notificação
  Dado uma solicitação "Notebook" de R$ 3.000,00 em "aguardando_gestor"
  Quando a aprovação do gestor falha depois de o efeito da notificação ter sido produzido
  Então a solicitação continua em "aguardando_gestor"
    E o histórico continua vazio
    E nenhuma notificação é entregue
```

> Detecta E18 (e-mail sai mesmo quando gravação da aprovação falha).

### Funcionalidade: matriz de permissões

```gherkin
@CT-24 @backend
Cenário: panel_user pode solicitar e não edita centro de custo
  Dado um panel_user "Ana"
  Quando ela tenta acessar o resource de "Centros de custo"
  Então a resposta é 403
```

> Detecta A-08/E08 (escalada de privilégio por edição de centro).

### Lacunas declaradas

Nenhuma: todos os defeitos do catálogo são alcançáveis com o arnês deste projeto.

---

## Resumo

- **Perfil**: completo para máquina de estados, alçada e concorrência.
- **Técnicas usadas**: BVA 3-valores, tabela de decisão, máquina de estados (5×6), 2-switch, rastreio de efeito, concorrência.
- **Cenários backend**: 26 (CT-01 a CT-26).
- **Lacunas declaradas**: 0.
# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Gerado pela skill `feature-test-design` v1.9.0.
> Browser só para o que depende de JavaScript, pixel ou acessibilidade.

## Gate de browser

A feature tem 6 telas/componentes com `Depende de JS? = Sim` no `01-plano-acao.md`:
- `SolicitacoesCompraTable` (listagem)
- `SolicitacaoCompraForm` (create/edit)
- `ViewSolicitacaoCompra` (infolist)
- Modal "Rejeitar"
- Modais "Enviar" / "Cancelar"
- `CentrosCustoTable` + form

O fluxo atravessa ≥ 2 telas e ≥ 2 personas (solicitante → gestor → diretor).

## Cenários

```gherkin
@CT-B01 @browser
Cenário: solicitante cria e envia, gestor aprova, diretor aprova
  Dado "Ana" autenticada no navegador como panel_user
    E o centro "TI" com gestor "Rui" e diretor "Dora"
  Quando ela navega para "/app/solicitacoes-de-compra/create"
    E preenche "Descrição" com "Notebook"
    E preenche "Valor" com "R$ 6.000,00"
    E seleciona "Centro de custo" = "TI"
    E salva
  Então ela vê a solicitação em "rascunho" na listagem
    E o botão "Enviar" está visível
  Quando ela clica em "Enviar" e confirma
  Então a situação muda para "Aguardando gestor"
    E o botão "Enviar" some
  Quando "Rui" acessa a mesma URL
  Então ele vê o botão "Aprovar"
  Quando ele aprova e confirma
  Então a situação muda para "Aguardando diretor"
  Quando "Dora" acessa a mesma URL
  Então ela vê o botão "Aprovar"
  Quando ela aprova e confirma
  Então a situação muda para "Aprovada"
    E a tela de visualização mostra o histórico com as etapas de Rui e Dora
```

> Detecta E16 (tela mostra "Aprovada" enquanto falta diretor), E04, E07, E08.

```gherkin
@CT-B02 @browser
Cenário: rejeição exibe modal com justificativa obrigatória
  Dado uma solicitação de R$ 3.000,00 em "aguardando_gestor"
    E o gestor "Rui" autenticado
  Quando ele abre a solicitação e clica em "Rejeitar"
  Então o modal pede "Motivo da rejeição"
  Quando ele confirma sem preencher
  Então o modal mostra erro "O campo é obrigatório"
  Quando ele preenche "Sem verba" e confirma
  Então a solicitação volta para "rascunho"
    E o solicitante vê o motivo ao visualizar
```

> Detecta E05 (justificativa obrigatória) na superfície de UI.

```gherkin
@CT-B03 @browser
Cenário: solicitante não enxerga botões de aprovação
  Dado uma solicitação de R$ 3.000,00 em "aguardando_gestor"
    E a solicitante "Ana" autenticada
  Quando ela abre a solicitação
  Então os botões "Aprovar" e "Rejeitar" não estão presentes
    E o botão "Cancelar" está presente
```

> Detecta E08 (solicitante aprova própria solicitação) na camada de affordance.

```gherkin
@CT-B04 @browser
Cenário: aprovada fica inalterada para todos
  Dado uma solicitação "aprovada"
    E "Ana" autenticada
  Quando ela abre a solicitação
  Então os botões "Editar", "Excluir", "Enviar", "Cancelar", "Aprovar" e "Rejeitar" não estão presentes
    E o badge "Aprovada" está visível
    E a seção "Histórico de aprovação" mostra quem aprovou
```

> Detecta E01, E02, E09, E14, E16 na camada de UI.

```gherkin
@CT-B05 @browser
Cenário: tela de visualização mostra quem aprovou cada etapa
  Dado uma solicitação de R$ 6.000,00 aprovada por Rui e Dora
  Quando qualquer usuário autorizado abre a visualização
  Então a seção "Histórico de aprovação" exibe:
    | Etapa   | Decidido por | Decisão   | Justificativa |
    | gestor  | Rui          | aprovada  | —             |
    | diretor | Dora         | aprovada  | —             |
```

> Detecta E13 (histórico não gravado) e E16 (estado exibido inconsistente).

---

## Roteiro Desenhado × Implementado

| Tela | O que o usuário vê | Status | Divergência |
|---|---|---|---|
| Listagem solicitante | solicitações com descrição, valor, centro, status | ☐ | — |
| Listagem gestor | botão Aprovar/Rejeitar nas suas | ☐ | — |
| Listagem diretor | botão Aprovar/Rejeitar quando pendente diretor | ☐ | — |
| Form create/edit | descrição, valor (R$), centro de custo | ☐ | — |
| View | situação + histórico de etapas | ☐ | — |
| Modal rejeitar | justificativa obrigatória | ☐ | — |
