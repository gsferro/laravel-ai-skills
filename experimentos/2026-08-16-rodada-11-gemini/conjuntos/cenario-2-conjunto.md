# Conjunto — Cenário 2: Aprovação de solicitação de compra (FERRO-830)

> Rodada 11 — Gemini 3.7 Flash High — Cascade
> Fonte: `demo-r8/wikis/specs/exp-r11/aprovacao-de-compra/04-casos-de-teste.md` + `05-casos-de-teste-browser.md`

---

## CT-01 — BVA no valor (Esquema)
- **Quando** Ana cria uma solicitação com valor <valor>
- **Então** o resultado é "<resultado>"

| valor | resultado |
|---|---|
| -0.01 | recusado |
| 0.00 | recusado |
| 0.01 | aceito |

## CT-02 — Criação nasce em estado de rascunho
- **Dado** que Ana é solicitante no centro "TI" (gestor Rui)
- **Quando** cria a solicitação "Notebooks" com valor 4.000,00
- **Então** a situação inicial é rascunho
- E o histórico de etapas está vazio

## CT-03 — Edição em rascunho não dispara notificações
- **Dado** a solicitação de Ana em rascunho no valor de 4.000,00
- **Quando** Ana altera o valor para 3.500,00
- **Então** o valor gravado passa a ser 3.500,00
- E a situação permanece rascunho
- E nenhuma notificação por e-mail é enviada

## CT-04 — Exclusão em rascunho remove a solicitação
- **Dado** a solicitação de Ana em rascunho
- **Quando** Ana submete a exclusão
- **Então** a solicitação deixa de existir

## CT-05 — Enviar transiciona para aguardando_gestor e notifica o gestor
- **Dado** a solicitação de Ana em rascunho no centro "TI" (gestor Rui)
- **Quando** Ana envia a solicitação
- **Então** a situação é aguardando_gestor
- E o histórico permanece com 0 etapas
- E Rui recebe notificação por e-mail
- E ninguém mais recebe notificação

## CT-06 — Envio sem gestor no centro de custo falha fechado
- **Dado** a solicitação de Ana em rascunho no centro "RH" que não tem gestor
- **Quando** Ana tenta enviar
- **Então** o envio é recusado
- E a situação permanece rascunho
- E o histórico continua vazio
- E um warning é registrado em log

## CT-07 — Solicitação em rascunho não aceita aprovação ou rejeição (Esquema)
- **Dado a solicitação de Ana em rascunho
- **Quando** Rui tenta "<operacao>"
- **Então** a operação é recusada
- E a situação permanece rascunho
- E o histórico continua vazio

| operacao |
|---|
| aprovar |
| rejeitar |

## CT-08 — BVA na fronteira de alçada de R$ 5.000,00 (Esquema)
- **Dado** a solicitação de Ana com valor <valor> no centro "TI" (gestor Rui)
- **Quando** Ana envia e Rui aprova
- **Então** a situação final é "<situacao>"

| valor | situacao |
|---|---|
| 4999.99 | aprovada |
| 5000.00 | aprovada |
| 5000.01 | aguardando_diretor |

## CT-09 — Edição e exclusão em trânsito são recusadas (Esquema)
- **Dado** a solicitação de Ana em "<situacao>" com valor 4.000,00 no centro "TI"
- **Quando** Ana tenta "<operacao>"
- **Então** a operação é recusada
- E a situação permanece "<situacao>"
- E o valor gravado permanece 4.000,00
- E o centro gravado permanece "TI"
- E o histórico mantém <etapas> etapa(s)

| situacao | operacao | etapas |
|---|---|---|
| aguardando_gestor | editar | 0 |
| aguardando_gestor | excluir | 0 |
| aguardando_diretor | editar | 1 |
| aguardando_diretor | excluir | 1 |

## CT-10 — Estados finais recusam qualquer operação (Esquema)
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

## CT-10b — Reenviar solicitação já em trânsito é recusado
- **Dado** a solicitação de Ana em aguardando_gestor
- **Quando** Ana tenta enviar novamente
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-11 — Gestor aprova valor abaixo do limite e finaliza fluxo
- **Dado** a solicitação de 4.000,00 em aguardando_gestor
- **Quando** Rui aprova
- **Então** a situação é aprovada
- E o histórico possui exatamente 1 etapa: gestor / aprovada / Rui com data-hora
- E nenhuma notificação é enviada

## CT-12 — Rejeição sem justificativa é recusada (Esquema)
- **Dado** a solicitação em "<situacao>"
- **Quando** "<aprovador>" tenta rejeitar com justificativa ""
- **Então** a operação é recusada
- E a situação permanece "<situacao>"
- E nenhuma etapa é adicionada ao histórico

| situacao | aprovador |
|---|---|
| aguardando_gestor | Rui |
| aguardando_diretor | Dora |

## CT-13 — Gestor rejeita com justificativa e retorna para rascunho
- **Dado** a solicitação em aguardando_gestor
- **Quando** Rui rejeita com justificativa "Fora do orçamento"
- **Então** a situação é rascunho
- E o histórico contém 1 etapa: gestor / rejeitada / Rui / "Fora do orçamento" com data-hora
- E nenhuma notificação é enviada

## CT-14 — Diretor rejeita com justificativa preservando etapa anterior
- **Dado** a solicitação em aguardando_diretor com 1 etapa de gestor no histórico
- **Quando** Dora rejeita com justificativa "Excede o trimestre"
- **Então** a situação é rascunho
- E o histórico contém 2 etapas: gestor intacta e diretor / rejeitada / Dora / "Excede o trimestre"

## CT-15 — Reenvio após rejeição recomeça pelo gestor sem apagar histórico anterior
- **Dado** a solicitação rejeitada pelo diretor, em rascunho, com 2 etapas registradas
- **Quando** Ana corrige e submete novo envio
- **Então** a situação é aguardando_gestor
- E as 2 etapas do ciclo anterior permanecem intactas no histórico
- E nenhuma nova etapa é registrada pelo ato de envio

## CT-16 — Cancelamento em trânsito é aceito (Esquema)
- **Dado** a solicitação de Ana em "<situacao>"
- **Quando** Ana solicita o cancelamento
- **Então** a situação é cancelada
- E o histórico permanece intacto

| situacao |
|---|
| aguardando_gestor |
| aguardando_diretor |

## CT-17 — Cancelar solicitação já aprovada é recusado
- **Dado** a solicitação de Ana aprovada
- **Quando** Ana tenta cancelar
- **Então** a operação é recusada
- E a situação permanece aprovada
- E o histórico permanece intacto

## CT-18 — Gestor aprova acima do limite e notifica diretores
- **Dado** a solicitação de 6.000,00 em aguardando_gestor
- E existem duas diretoras cadastradas: Dora e Eva
- **Quando** Rui aprova
- **Então** a situação é aguardando_diretor
- E o histórico contém exatamente 1 etapa do gestor
- E Dora recebe notificação por e-mail
- E Eva recebe notificação por e-mail
- E Rui não recebe notificação
- E Ana não recebe notificação

## CT-19 — Diretora aprova e encerra fluxo
- **Dado** a solicitação em aguardando_diretor
- **Quando** Dora aprova
- **Então** a situação é aprovada
- E o histórico possui 2 etapas: gestor / aprovada / Rui e diretor / aprovada / Dora
- E nenhuma notificação adicional é enviada

## CT-20 — Diretor não pode aprovar antes do gestor
- **Dado** a solicitação em aguardando_gestor
- **Quando** Dora tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor
- E o histórico continua vazio

## CT-21 — Gestora de outro centro não pode aprovar
- **Dado** a solicitação em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Carla, gestora do centro "RH", tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-22 — Solicitante sem cargo de gestor não pode aprovar
- **Dado** a solicitação de Ana em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Ana tenta aprovar
- **Então** a operação é recusada
- E a situação permanece aguardando_gestor

## CT-23 — Solicitante que é gestora do próprio centro pode aprovar etapa de gestor (A-09)
- **Dado** que Ana é gestora do centro "Marketing"
- E Ana possui solicitação de 6.000,00 em aguardando_gestor no centro "Marketing"
- **Quando** Ana aprova
- **Então** a situação avança para aguardando_diretor e não aprovada
- E o histórico registra 1 etapa: gestor / aprovada / Ana

## CT-24 — Aprovações simultâneas do gestor
- **Dado** a solicitação em aguardando_gestor
- **Quando** duas requisições simultâneas de Rui tentam aprovar
- **Então** exatamente uma é aceita e a outra é recusada
- E o histórico registra exatamente 1 etapa

## CT-25 — Aprovações simultâneas de diretores
- **Dado** a solicitação em aguardando_diretor com as diretoras Dora e Eva
- **Quando** Dora e Eva tentam aprovar simultaneamente
- **Então** exatamente uma é aceita e a outra é recusada
- E o histórico registra exatamente 1 etapa de diretor

## CT-26 — Rejeição não envia notificação
- **Dado** a solicitação em aguardando_gestor
- **Quando** Rui rejeita com justificativa "Fora do orçamento"
- **Então** nenhuma notificação por e-mail é enviada

## CT-27 — Tentativa de trocar centro em trânsito não altera aprovador
- **Dado** a solicitação em aguardando_gestor no centro "TI" (gestor Rui)
- **Quando** Ana tenta trocar o centro para "RH"
- **Então** a operação é recusada
- E o centro gravado permanece "TI"
- E Carla (gestora do RH) continua com aprovação recusada
- E Rui continua com aprovação aceita

## CT-28 — Falha de persistência não dispara e-mail
- **Dado** a solicitação de 6.000,00 em aguardando_gestor
- E Dora seria a destinatária no caminho de sucesso
- E a gravação da etapa falha após o ponto de despacho
- **Quando** Rui tenta aprovar
- **Então** a situação permanece aguardando_gestor
- E o histórico não recebe nova etapa
- E Dora não recebe notificação

## CT-29 — Rótulos distintos por situação (Esquema)
- **Dado** a solicitação em "<situacao>"
- **Quando** a tela de visualização é renderizada
- **Então** o rótulo exibido é "<rotulo>"

| situacao | rotulo |
|---|---|
| rascunho | Rascunho |
| aguardando_gestor | Aguardando gestor |
| aguardando_diretor | Aguardando diretor |
| aprovada | Aprovada |
| cancelada | Cancelada |

## CT-30 — Visualização exibe histórico completo
- **Dado** a solicitação de 6.000,00 aprovada por gestor e diretora
- **Quando** a tela de visualização é carregada
- **Então** o histórico exibe 2 etapas ordenadas
- E a primeira exibe "Gestor", "Aprovada", Rui e timestamp
- E a segunda exibe "Diretor", "Aprovada", Dora e timestamp

## CT-31 — panel_user não altera o gestor de centro de custo
- **Dado** que Carla é panel_user na organização
- **Quando** Carla tenta alterar o gestor do centro "TI" diretamente na rota/serviço
- **Então** a operação é recusada
- E o gestor do centro "TI" permanece Rui

## CT-B01 — Listagem exibe badges distintos para cada situação
- **Dado** que existem solicitações em rascunho, aguardando_gestor, aguardando_diretor, aprovada e cancelada
- **Quando** o usuário abre a listagem
- **Então** cada linha exibe um badge com rótulo correspondente à sua situação

## CT-B02 — Solicitante não visualiza ações de aprovação em sua própria solicitação
- **Dado** que Ana acessa a visualização de sua solicitação em aguardando_gestor
- **Então** ela vê o status "Aguardando gestor"
- E não visualiza botão "Aprovar"
- E não visualiza botão "Rejeitar"

## CT-B03 — Gestor da vez visualiza ações de aprovar e rejeitar
- **Dado** que Rui é gestor do centro "TI" com solicitação em aguardando_gestor
- **Quando** abre a visualização da solicitação
- **Então** visualiza o botão "Aprovar"
- E visualiza o botão "Rejeitar"

## CT-B04 — Modal de rejeição impede submissão sem justificativa
- **Dado** que Rui abre a visualização da solicitação e aciona "Rejeitar"
- **Quando** o modal é exibido
- **Então** existe o campo de justificativa
- E o botão de confirmação permanece desabilitado enquanto a justificativa estiver em branco

## CT-B05 — Visualização detalha histórico de quem aprovou cada etapa
- **Dado** que a solicitação foi aprovada por gestor e diretora
- **Quando** a tela de visualização é carregada
- **Então** o histórico apresenta 2 etapas ordenadas
- E a primeira exibe "Gestor", "Aprovada", o nome do gestor e a data
- E a segunda exibe "Diretor", "Aprovada", o nome da diretora e a data
