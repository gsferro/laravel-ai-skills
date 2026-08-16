# Conjunto — Cenário 2: Aprovação de solicitação de compra (FERRO-830)

> Rodada 10 — Kimi K3 High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r10/aprovacao-de-compra/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — BVA no valor (Esquema)
- **Quando** Ana cria uma solicitação com valor <valor>
- **Então** o resultado é "<resultado>"

| valor | resultado |
|---|---|
| -0.01 | recusado |
| 0.00 | recusado |
| 0.01 | aceito |

## CT-02 — Criação nasce em rascunho
- **Dado** que Ana é solicitante no centro "TI" (gestor Rui)
- **Quando** cria a solicitação "Notebooks" de 4.000,00
- **Então** a situação é rascunho
- E o histórico está vazio

## CT-03 — Edição em rascunho persiste sem efeito colateral
- **Dado** a solicitação de Ana em rascunho com valor 4.000,00
- **Quando** Ana edita o valor para 3.500,00
- **Então** o valor gravado é 3.500,00
- E a situação continua rascunho
- E nenhuma notificação foi enviada

## CT-04 — Exclusão em rascunho remove o registro
- **Dado** a solicitação de Ana em rascunho
- **Quando** Ana exclui
- **Então** a solicitação não existe mais

## CT-05 — Enviar move para aguardando_gestor e notifica o gestor
- **Dado** a solicitação de Ana em rascunho no centro "TI" (gestor Rui)
- **Quando** Ana envia
- **Então** a situação é aguardando_gestor
- E o histórico continua vazio
- E Rui recebe notificação por e-mail
- E ninguém mais recebe notificação

## CT-06 — Enviar sem gestor falha fechado
- **Dado** a solicitação de Ana em rascunho no centro "RH" sem gestor
- **Quando** Ana tenta enviar
- **Então** o envio é recusado
- E a situação permanece rascunho
- E o histórico continua vazio
- E um warning é registrado no log

## CT-07 — Rascunho não aceita decisão (Esquema)
- **Dado** a solicitação de Ana em rascunho
- **Quando** Rui tenta "<operacao>"
- **Então** a operação é recusada
- E a situação permanece rascunho
- E o histórico continua vazio

| operacao |
|---|
| aprovar |
| rejeitar |

## CT-08 — BVA no limite de alçada (Esquema)
- **Dado** a solicitação de Ana com valor <valor> no centro "TI" (gestor Rui)
- **Quando** Ana envia e Rui aprova
- **Então** a situação é "<situacao>"

| valor | situacao |
|---|---|
| 4999.99 | aprovada |
| 5000.00 | aprovada |
| 5000.01 | aguardando_diretor |

## CT-09 — Editar e excluir em trânsito são recusados (Esquema)
- **Dado** a solicitação de Ana em "<situacao>" com valor 4.000,00 no centro "TI"
- **Quando** Ana tenta "<operacao>"
- **Então** a operação é recusada
- E a situação permanece "<situacao>"
- E o valor gravado permanece 4.000,00
- E o centro gravado permanece "TI"
- E o histórico permanece com <etapas> etapa(s)

| situacao | operacao | etapas |
|---|---|---|
| aguardando_gestor | editar | 0 |
| aguardando_gestor | excluir | 0 |
| aguardando_diretor | editar | 1 |
| aguardando_diretor | excluir | 1 |

## CT-10 — Estados terminais recusam tudo (Esquema)
- **Dado** a solicitação de Ana em "<situacao>"
- **Quando** alguém tenta "<operacao>"
- **Então** a operação é recusada
- E a situação permanece "<situacao>"
- E o histórico permanece intacto

| situacao | operacao |
|---|---|
| aprovada | editar |
| aprovada | excluir |
| aprovada | enviar |
| aprovada | aprovar |
| aprovada | rejeitar |
| cancelada | editar |
| cancelada | excluir |
| cancelada | enviar |

## CT-10b — Reenviar em trânsito é recusado
- **Dado** a solicitação de Ana em aguardando_gestor
- **Quando** Ana tenta enviar novamente
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-11 — Gestor aprova abaixo do limite e encerra o fluxo
- **Dado** a solicitação de 4.000,00 em aguardando_gestor
- **Quando** Rui aprova
- **Então** a situação é aprovada
- E o histórico tem exatamente 1 etapa: gestor / aprovada / Rui / com carimbo de data-hora
- E nenhuma notificação é enviada

## CT-12 — Rejeitar sem justificativa é recusado nas duas etapas (Esquema)
- **Dado** a solicitação em "<situacao>"
- **Quando** "<aprovador>" tenta rejeitar com justificativa ""
- **Então** a operação é recusada
- E a situação permanece "<situacao>"
- E o histórico não ganha etapa

| situacao | aprovador |
|---|---|
| aguardando_gestor | Rui |
| aguardando_diretor | Dora |

## CT-13 — Gestor rejeita com justificativa e a solicitação volta a rascunho
- **Dado** a solicitação em aguardando_gestor
- **Quando** Rui rejeita com justificativa "Fora do orçamento"
- **Então** a situação é rascunho
- E o histórico tem 1 etapa: gestor / rejeitada / Rui / "Fora do orçamento" / com carimbo
- E nenhuma notificação é enviada

## CT-14 — Diretor rejeita com justificativa preservando a etapa do gestor
- **Dado** a solicitação em aguardando_diretor com 1 etapa de gestor no histórico
- **Quando** Dora rejeita com justificativa "Excede o trimestre"
- **Então** a situação é rascunho
- E o histórico tem 2 etapas: a do gestor (intacta) e diretor / rejeitada / Dora / "Excede o trimestre"

## CT-15 — Reenvio após rejeição recomeça pelo gestor sem apagar o ciclo anterior
- **Dado** a solicitação rejeitada pela diretora, em rascunho, com 2 etapas no histórico
- **Quando** Ana corrige e envia de novo
- **Então** a situação é aguardando_gestor
- E as 2 etapas do ciclo anterior continuam no histórico
- E nenhuma etapa nova foi gravada pelo envio

## CT-16 — Cancelar em trânsito é aceito (Esquema)
- **Dado** a solicitação de Ana em "<situacao>"
- **Quando** Ana cancela
- **Então** a situação é cancelada
- E o histórico permanece intacto

| situacao |
|---|
| aguardando_gestor |
| aguardando_diretor |

## CT-17 — Cancelar aprovada é recusado
- **Dado** a solicitação de Ana aprovada
- **Quando** Ana tenta cancelar
- **Então** a operação é recusada
- E a situação permanece aprovada
- E o histórico permanece intacto

## CT-18 — Gestor aprova acima do limite e abre a etapa do diretor
- **Dado** a solicitação de 6.000,00 em aguardando_gestor
- E existem duas diretoras: Dora e Eva
- **Quando** Rui aprova
- **Então** a situação é aguardando_diretor
- E o histórico tem exatamente 1 etapa de gestor
- E Dora recebe notificação por e-mail
- E Eva recebe notificação por e-mail
- E Rui não recebe notificação
- E Ana não recebe notificação

## CT-19 — Diretora aprova e encerra o fluxo
- **Dado** a solicitação em aguardando_diretor
- **Quando** Dora aprova
- **Então** a situação é aprovada
- E o histórico tem 2 etapas: gestor / aprovada / Rui e diretor / aprovada / Dora, cada uma com carimbo
- E nenhuma notificação é enviada

## CT-20 — Diretora não decide antes do gestor
- **Dado** a solicitação em aguardando_gestor
- **Quando** Dora tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor
- E o histórico continua vazio

## CT-21 — Gestora de outro centro não decide
- **Dado** a solicitação em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Carla, gestora do centro "RH", tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-22 — Solicitante sem papel de gestor não decide
- **Dado** a solicitação de Ana em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Ana tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-23 — Solicitante que é gestora do próprio centro decide (A-09)
- **Dado** que Ana é gestora do centro "Marketing"
- E a solicitação de Ana de 6.000,00 está em aguardando_gestor no centro "Marketing"
- **Quando** Ana aprova
- **Então** a situação é aguardando_diretor — não aprovada
- E o histórico tem 1 etapa: gestor / aprovada / Ana

## CT-24 — Duas aprovações simultâneas do gestor gravam uma só etapa
- **Dado** a solicitação em aguardando_gestor
- **Quando** duas requisições simultâneas de Rui tentam aprovar
- **Então** exatamente uma é aceita e a outra é recusada
- E o histórico tem exatamente 1 etapa

## CT-25 — Duas diretoras simultâneas gravam uma só etapa
- **Dado** a solicitação em aguardando_diretor com as diretoras Dora e Eva
- **Quando** Dora e Eva tentam aprovar simultaneamente
- **Então** exatamente uma é aceita e a outra é recusada
- E o histórico tem exatamente 1 etapa de diretor

## CT-26 — Rejeição não notifica ninguém
- **Dado** a solicitação em aguardando_gestor
- **Quando** Rui rejeita com justificativa "Fora do orçamento"
- **Então** nenhuma notificação é enviada — nem a Ana, nem a Dora, nem ao próprio Rui

## CT-27 — Trocar o centro em trânsito não muda o aprovador da vez
- **Dado** a solicitação em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Ana tenta trocar o centro para "RH"
- **Então** a operação é recusada
- E o centro gravado permanece "TI"
- E Carla (gestora do RH) aprovando continua recusada
- E Rui aprovando continua aceito

## CT-28 — Efeito de e-mail não sobrevive a gravação que falha
- **Dado** a solicitação de 6.000,00 em aguardando_gestor
- E Dora existe e seria notificada no caminho feliz
- E a gravação da etapa falha depois do ponto de notificação
- **Quando** Rui tenta aprovar
- **Então** a situação permanece aguardando_gestor
- E o histórico não ganha etapa
- E Dora não recebe notificação

## CT-29 — Cada situação tem rótulo próprio (Esquema)
- **Dado** a solicitação em "<situacao>"
- **Quando** a tela de visualização é carregada
- **Então** o rótulo exibido é "<rotulo>"

| situacao | rotulo |
|---|---|
| rascunho | Rascunho |
| aguardando_gestor | Aguardando gestor |
| aguardando_diretor | Aguardando diretor |
| aprovada | Aprovada |
| cancelada | Cancelada |

## CT-30 — Visualização exibe quem aprovou cada etapa
- **Dado** a solicitação de 6.000,00 aprovada após gestor e diretora
- **Quando** a tela de visualização é carregada
- **Então** o histórico mostra 2 etapas em ordem
- E a primeira exibe "Gestor", "Aprovada", Rui e a data-hora da decisão
- E a segunda exibe "Diretor", "Aprovada", Dora e a data-hora da decisão

## CT-31 — panel_user não altera o gestor de um centro de custo
- **Dado** que Carla é panel_user na organização
- **Quando** Carla tenta editar o gestor do centro "TI" para si mesma, fora da tela
- **Então** a operação é recusada
- E o gestor do centro "TI" permanece Rui

## CT-B01 — A listagem marca cada situação com rótulo distinto
- **Dado** que existem solicitações em rascunho, aguardando_gestor, aguardando_diretor, aprovada e cancelada
- **Quando** a listagem é aberta
- **Então** cada linha exibe um badge com rótulo distinto da sua situação

## CT-B02 — Solicitante não vê ações de decisão na própria solicitação em trânsito
- **Dado** que Ana abriu a visualização da sua solicitação em aguardando_gestor
- **Então** ela vê o status "Aguardando gestor"
- E não vê o botão "Aprovar"
- E não vê o botão "Rejeitar"

## CT-B03 — Gestor da vez vê as ações de decisão
- **Dado** que Rui é gestor do centro "TI" com solicitação aguardando_gestor
- **Quando** abre a visualização da solicitação
- **Então** vê o botão "Aprovar"
- E vê o botão "Rejeitar"

## CT-B04 — O modal de rejeição bloqueia justificativa vazia
- **Dado** que Rui abriu a visualização e clicou em "Rejeitar"
- **Quando** o modal abre
- **Então** existe um campo de justificativa
- E o botão de confirmar permanece desabilitado enquanto o campo estiver vazio

## CT-B05 — A visualização mostra quem decidiu cada etapa
- **Dado** que a solicitação foi aprovada pelo gestor e pela diretora
- **Quando** a visualização é aberta
- **Então** o histórico exibe 2 etapas
- E a primeira mostra "Gestor", "Aprovada", o nome do gestor e a data
- E a segunda mostra "Diretor", "Aprovada", o nome da diretora e a data
