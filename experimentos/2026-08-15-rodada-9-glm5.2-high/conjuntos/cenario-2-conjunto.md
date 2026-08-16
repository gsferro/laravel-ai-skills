# Conjunto — Cenário 2: Aprovação de solicitação de compra (FERRO-830)

> Rodada 9 — GLM 5.2 High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r9/aprovacao-de-compra/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — BVA no valor (Esquema)
- **Dado** que o solicitante Ana cria uma solicitação com valor "<valor>"
- **Então** o resultado é "<resultado>"

| valor | resultado |
|---|---|
| -0.01 | recusado |
| 0.00 | recusado |
| 0.01 | aceito |

## CT-02 — Criar solicitação em rascunho
- **Dado** que Ana é solicitante
- **Quando** cria solicitação com descrição "Notebooks", valor 4.000,00 e centro "TI"
- **Então** a solicitação fica em rascunho
- E o histórico de etapas está vazio

## CT-03 — Editar em rascunho é aceito
- **Dado** que Ana tem solicitação em rascunho com valor 4.000,00
- **Quando** edita o valor para 3.500,00
- **Então** a gravação é aceita
- E o valor gravado é 3.500,00

## CT-04 — Excluir em rascunho é aceito
- **Dado** que Ana tem solicitação em rascunho
- **Quando** exclui a solicitação
- **Então** a solicitação não existe mais

## CT-05 — Enviar vai para aguardando_gestor
- **Dado** que Ana tem solicitação em rascunho no centro "TI" com gestor Rui
- **Quando** Ana envia
- **Então** a situação é aguardando_gestor
- E o histórico tem 0 etapas
- E Rui recebe notificação por e-mail

## CT-06 — Enviar sem gestor é recusado
- **Dado** que Ana tem solicitação em rascunho no centro "RH" sem gestor
- **Quando** Ana tenta enviar
- **Então** o envio é recusado
- E a situação permanece rascunho

## CT-06b — Aprovar em rascunho é recusado
- **Dado** que Ana tem solicitação em rascunho
- **Quando** Rui tenta aprovar
- **Então** a aprovação é recusada
- E a situação permanece rascunho
- E o histórico está vazio

## CT-07 — BVA no limite do diretor (Esquema)
- **Dado** que Ana tem solicitação em rascunho com valor "<valor>"
- **Quando** envia e o gestor aprova
- **Então** a situação é "<situacao>"

| valor | situacao |
|---|---|
| 4999.99 | aprovada |
| 5000.00 | aprovada |
| 5000.01 | aguardando_diretor |

## CT-08 — Editar em trânsito é recusado
- **Dado** que Ana tem solicitação em aguardando_gestor com valor 4.000,00
- **Quando** Ana tenta editar o valor para 6.000,00
- **Então** a edição é recusada
- E o valor gravado permanece 4.000,00

## CT-08b — Excluir em trânsito é recusado
- **Dado** que Ana tem solicitação em aguardando_gestor
- **Quando** Ana tenta excluir
- **Então** a exclusão é recusada
- E a solicitação permanece aguardando_gestor

## CT-09 — Editar em aprovada é recusado
- **Dado** que a solicitação está aprovada
- **Quando** Ana tenta editar
- **Então** a edição é recusada
- E a situação permanece aprovada

## CT-09b — Excluir em aprovada é recusado
- **Dado** que a solicitação está aprovada
- **Quando** Ana tenta excluir
- **Então** a exclusão é recusada

## CT-09c — Editar em cancelada é recusado
- **Dado** que a solicitação está cancelada
- **Quando** Ana tenta editar
- **Então** a edição é recusada

## CT-10 — Gestor aprova solicitação abaixo do limite
- **Dado** que a solicitação de Ana está em aguardando_gestor com valor 4.000,00
- **Quando** Rui (gestor do centro) aprova
- **Então** a situação é aprovada
- E o histórico tem 1 etapa: gestor/aprovada/Rui
- E nenhuma notificação é enviada (estado final)

## CT-11 — Rejeitar com justificativa vazia é recusado
- **Dado** que a solicitação está em aguardando_gestor
- **Quando** Rui tenta rejeitar com justificativa ""
- **Então** a rejeição é recusada
- E a situação permanece aguardando_gestor
- E o histórico está vazio

## CT-12 — Rejeitar com justificativa volta para rascunho
- **Dado** que a solicitação está em aguardando_gestor
- **Quando** Rui rejeita com justificativa "Fora do orçamento"
- **Então** a situação é rascunho
- E o histórico tem 1 etapa: gestor/rejeitada/Rui/"Fora do orçamento"

## CT-13 — Cancelar em aguardando_gestor é aceito
- **Dado** que a solicitação está em aguardando_gestor
- **Quando** Ana cancela
- **Então** a situação é cancelada
- E o histórico permanece como estava

## CT-14 — Cancelar em aprovada é recusado
- **Dado** que a solicitação está aprovada
- **Quando** Ana tenta cancelar
- **Então** o cancelamento é recusado
- E a situação permanece aprovada

## CT-15 — Gestor aprova acima do limite vai para diretor
- **Dado** que a solicitação de Ana está em aguardando_gestor com valor 6.000,00
- **Quando** Rui aprova
- **Então** a situação é aguardando_diretor
- E o histórico tem 1 etapa: gestor/aprovada/Rui
- E Dora (diretora) recebe notificação por e-mail

## CT-16 — Diretor aprova e finaliza
- **Dado** que a solicitação está em aguardando_diretor
- **Quando** Dora (diretora) aprova
- **Então** a situação é aprovada
- E o histórico tem 2 etapas: gestor/aprovada e diretor/aprovada/Dora
- E nenhuma notificação é enviada (estado final)

## CT-17 — Diretor rejeita com justificativa
- **Dado** que a solicitação está em aguardando_diretor
- **Quando** Dora rejeita com justificativa "Excede o orçamento trimestral"
- **Então** a situação é rascunho
- E o histórico tem 2 etapas: gestor/aprovada e diretor/rejeitada/Dora

## CT-18 — Diretor tenta aprovar antes do gestor
- **Dado** que a solicitação está em aguardando_gestor
- **Quando** Dora tenta aprovar
- **Então** a aprovação é recusada
- E a situação permanece aguardando_gestor

## CT-19 — Gestor de outro centro não aprova
- **Dado** que a solicitação está em aguardando_gestor no centro "TI"
- **Quando** Carla (gestora do centro "RH") tenta aprovar
- **Então** a aprovação é recusada

## CT-20 — Solicitante é gestor do próprio centro
- **Dado** que Ana é gestora do centro "Marketing" e tem solicitação em aguardando_gestor
- **Quando** Ana tenta aprovar
- **Então** a aprovação é recusada
- E a situação permanece aguardando_gestor

## CT-21 — Rejeitado pelo diretor, reenviado volta para gestor
- **Dado** que a solicitação foi rejeitada pelo diretor e voltou para rascunho
- E o histórico tem 2 etapas do ciclo anterior
- **Quando** Ana corrige e envia de novo
- **Então** a situação é aguardando_gestor
- E o histórico ainda tem as 2 etapas do ciclo anterior
- E nenhuma etapa do novo ciclo foi gravada ainda

## CT-22 — Duas aprovações simultâneas do gestor
- **Dado** que a solicitação está em aguardando_gestor
- **Quando** duas requisições simultâneas de Rui tentam aprovar
- **Então** uma é aceita e a outra é recusada
- E o histórico tem exatamente 1 etapa

## CT-23 — Dois diretores aprovam simultaneamente
- **Dado** que a solicitação está em aguardando_diretor
- E existem dois diretores: Dora e Eva
- **Quando** Dora e Eva tentam aprovar simultaneamente
- **Então** uma é aceita e a outra é recusada
- E o histórico tem exatamente 1 etapa de diretor

## CT-24 — Notificação vai só para o próximo aprovador
- **Dado** que a solicitação de valor 6.000,00 está em aguardando_gestor
- **Quando** Rui aprova
- **Então** Dora recebe notificação por e-mail
- E Rui não recebe notificação
- E Ana não recebe notificação

## CT-25 — Aprovação final não notifica ninguém
- **Dado** que a solicitação está em aguardando_diretor
- **Quando** Dora aprova
- **Então** nenhuma notificação é enviada

## CT-26 — Editar valor em trânsito é recusado e valor gravado permanece
- **Dado** que a solicitação está em aguardando_gestor com valor 4.000,00
- **Quando** Ana tenta editar valor para 6.000,00
- **Então** a edição é recusada
- E o valor gravado permanece 4.000,00

## CT-27 — Trocar centro de custo em trânsito é recusado
- **Dado** que a solicitação está em aguardando_gestor no centro "TI"
- **Quando** Ana tenta trocar para centro "RH"
- **Então** a edição é recusada
- E o centro gravado permanece "TI"
- E o aprovador continua sendo Rui (gestor de TI)

## CT-28 — Aprovação falha depois da notificação
- **Dado** que a solicitação está em aguardando_gestor
- E o gestor Rui existe e seria notificado no caminho feliz
- E a gravação da etapa falha após o ponto de notificação
- **Quando** Rui tenta aprovar
- **Então** a situação permanece aguardando_gestor
- E o histórico está vazio
- E nenhuma notificação é entregue

## CT-29 — Excluir em estados de trânsito (Esquema)
- **Dado** que a solicitação está em "<situacao>"
- **Quando** Ana tenta excluir
- **Então** a exclusão é recusada
- E a situação permanece "<situacao>"
- E o histórico é preservado

| situacao |
|---|
| aguardando_gestor |
| aguardando_diretor |

## CT-30 — Partição exaustiva do enum de situação (Esquema)
- **Dado** que a solicitação está em "<situacao>"
- **Quando** a tela de visualização é carregada
- **Então** o rótulo exibido é "<rotulo>"

| situacao | rotulo |
|---|---|
| rascunho | Rascunho |
| aguardando_gestor | Aguardando gestor |
| aguardando_diretor | Aguardando diretor |
| aprovada | Aprovada |
| cancelada | Cancelada |

## CT-31 — Histórico completo de aprovação com diretor
- **Dado** que a solicitação foi aprovada com valor 6.000,00
- **Então** o histórico tem 2 etapas
- E a primeira etapa mostra: gestor, aprovada, Rui, data/hora
- E a segunda etapa mostra: diretor, aprovada, Dora, data/hora

## CT-B01 — Badge muda conforme a situação
- **Dado** que existem solicitações em rascunho, aguardando_gestor, aguardando_diretor, aprovada e cancelada
- **Quando** o solicitante acessa a listagem
- **Então** cada solicitação exibe um badge com rótulo distinto para cada situação

## CT-B02 — Solicitante não vê "Aprovar"
- **Dado** que Ana tem solicitação em aguardando_gestor
- **Quando** Ana acessa a visualização da solicitação
- **Então** vê a situação "Aguardando gestor"
- E não vê botão "Aprovar"
- E não vê botão "Rejeitar"

## CT-B03 — Gestor vê "Aprovar" e "Rejeitar"
- **Dado** que Rui é gestor do centro "TI"
- E a solicitação de Ana está em aguardando_gestor no centro "TI"
- **Quando** Rui acessa a visualização da solicitação
- **Então** vê a situação "Aguardando gestor"
- E vê botão "Aprovar"
- E vê botão "Rejeitar"

## CT-B04 — Modal de rejeição exige justificativa
- **Dado** que Rui está na visualização da solicitação em aguardando_gestor
- **Quando** clica em "Rejeitar"
- **Então** um modal aparece com campo de justificativa
- E o botão de confirmar está desabilitado enquanto a justificativa estiver vazia

## CT-B05 — Histórico mostra quem decidiu cada etapa
- **Dado** que a solicitação foi aprovada por gestor e diretor
- **Quando** a visualização da solicitação é carregada
- **Então** o histórico mostra 2 etapas
- E a primeira etapa mostra "Gestor", "Aprovada", nome do gestor e data
- E a segunda etapa mostra "Diretor", "Aprovada", nome do diretor e data
