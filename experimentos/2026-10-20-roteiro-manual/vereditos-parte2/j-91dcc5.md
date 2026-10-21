Avaliação dos **46 passos de 18 RM**, somente pelos três arquivos. As premissas estão identificadas como **A-01–A-12**, sem IDs P-nn.

Comparei cada ação ao recorte correspondente dos CT. Exemplos não percorridos não geram penalização; pós-condições omitidas geram **PARCIAL**. “DIVERGIU” em resultado obtido não torna o esperado divergente.

| RM | Passo | Classe | Citação do roteiro | Citação da origem (se não FIEL) |
|---|---|---|---|---|
| RM-01 | 1 | FIEL | “Rascunho de Ana com descrição RM01 Café, valor 4999.99 e centro Compras; zero decisões e e-mails.” | — |
| RM-01 | 2 | PARCIAL | “O mesmo rascunho contém Café e açúcar ☕, 5000.01 e Viagens; salvar sem mudança não duplica nem falha.” | CT-04: “E as decisões históricas permanecem idênticas e nenhum e-mail novo é enviado”. Omite ambos os efeitos. |
| RM-01 | 3 | FIEL | “Registro indisponível para uso, sem nova decisão ou e-mail.” | — |
| RM-02 | 1 | FIEL | “Cada compra aguarda gestor, sem decisões; somente Bruno recebe uma mensagem de gestor com corpo da compra.” | — |
| RM-02 | 2 | FIEL | “Cada compra termina aprovada com uma decisão de gestor por Bruno e zero e-mails novos.” | — |
| RM-03 | 1 | PARCIAL | “Aguarda gestor; zero decisões; um e-mail para Bruno, nenhum para diretoras.” | CT-67: “com corpo não vazio que identifica esta solicitação e sua etapa pendente”; “E nenhum outro destinatário recebe mensagem”. Omite conteúdo e exclusão dos demais destinatários. |
| RM-03 | 2 | PARCIAL | “uma mensagem de diretor para Diana e outra para Elisa, sem outros destinatários.” | CT-67: “com corpo não vazio que identifica esta solicitação e sua etapa pendente”. Omite esse conteúdo obrigatório. |
| RM-03 | 3 | PARCIAL | “Aprovada com duas decisões em ordem: gestor Bruno e diretora Elisa; nenhum e-mail novo.” | CT-19: “E a decisão de Bruno fica idêntica”. Conserva autoria e ordem, mas não exige integridade da decisão anterior. |
| RM-04 | 1 | PARCIAL | “Rascunho com aprovação de Bruno e rejeição de Diana preservadas; zero e-mails da rejeição.” | CT-24: “com \<justificativa> íntegra”; “E os três dados e decisões anteriores permanecem idênticos”. Omite justificativa persistida e preservação dos três dados. |
| RM-04 | 2 | PARCIAL | “Aguarda gestor; histórico anterior idêntico; somente Carlos recebe novo aviso de gestor.” | CT-29: “Então a mesma solicitação fica em aguardando_gestor sem nova decisão e todas as decisões anteriores permanecem idênticas”. Preservar decisões antigas não exclui decisões novas. |
| RM-04 | 3 | PARCIAL | “Nova etapa de diretor após Carlos; decisão de Elisa encerra o segundo ciclo; três decisões anteriores íntegras e zero e-mails da final.” | CT-30: “E os diretores recebem \<emails> e não há decisão de diretor no ciclo atual”; exemplo: “um novo e-mail por diretor”. Omite os avisos exigidos após Carlos. |
| RM-05 | 1 | FIEL | “Ambas recusadas; compra aguarda gestor; dados e histórico intactos; zero e-mails novos.” | — |
| RM-05 | 2 | PARCIAL | “Rascunho com uma rejeição de gestor por Bruno e justificativa Unicode íntegra; nenhum aviso novo.” | CT-24: “E os três dados e decisões anteriores permanecem idênticos”. Omite preservação dos dados e do histórico anterior. |
| RM-06 | 1 | FIEL | “Cancelada; mantém os três dados, nenhuma decisão nova e nenhum e-mail de cancelamento.” | — |
| RM-06 | 2 | FIEL | “Cancelada; aprovação de Bruno e dados preservados, sem decisão ou mensagem nova.” | — |
| RM-07 | 1 | FIEL | “Todas as tentativas recusadas; rascunho, dono e dados preservados; zero decisões e mensagens.” | — |
| RM-07 | 2 | PARCIAL | “Tentativas não mudam a compra nem enviam e-mail.” | CT-21: “com os três dados e o histórico anteriores”; CT-32: “nenhuma decisão nova é criada”. A expressão genérica não explicita preservação do histórico nem ausência de decisões novas. |
| RM-07 | 3 | PARCIAL | “tentativas recusadas e estado/histórico preservados.” | CT-22: “com os três dados e exatamente o histórico anterior”; “E nenhum e-mail novo é enviado aos destinatários existentes”. Omite dados e e-mails. |
| RM-08 | 1 | ORIGEM ERRADA | “Preparação atinge os dois estados sem fabricar situação persistida.” | CT-20: “Quando \<ator> tenta aprovar diretamente”; “Então o banco mantém \<situacao>, os três dados e exatamente o histórico anterior”. Os CT citados tratam de operações recusadas em estados existentes, não das transições positivas que produzem a partida. |
| RM-08 | 2 | PARCIAL | “Seis ações recusadas por estado; dados, existência e histórico permanecem idênticos, sem novos e-mails.” | CT-14: “Então a situação persistida continua \<situacao> e os três dados permanecem idênticos”. Omite a manutenção explícita da situação. |
| RM-09 | 1 | FIEL | “Recusa identifica ausência de gestor; mantém dados e rascunho; zero decisões/e-mails; warning da recusa.” | — |
| RM-09 | 2 | FIEL | “Warning correspondente ao envio recusado por ausência de gestor, conforme A-10 do requisito e CT-15.” | — |
| RM-10 | 1 | FIEL | “Criação recusada por descrição; nenhuma compra nova e nenhum e-mail ou decisão.” | — |
| RM-10 | 2 | FIEL | “Edição recusada; descrição original, valor, centro e histórico preservados; zero e-mails novos.” | — |
| RM-11 | 1 | FIEL | “Uma compra de Ana em rascunho com os três dados; nenhum erro de formulário, decisão ou e-mail.” | — |
| RM-11 | 2 | PARCIAL | “O mesmo registro mantém correções, sem erro, duplicação ou e-mail; histórico anterior íntegro.” | CT-07: “Então o mesmo registro em rascunho contém \<dados>”. Omite permanência em rascunho. |
| RM-11 | 3 | PARCIAL | “Compra deixa de estar disponível; nenhuma decisão ou mensagem nova.” | CT-65: “a compra de controle não muda e não há erro da ação”. Omite essas pós-condições da exclusão pela interface. |
| RM-12 | 1 | FIEL | “A gravação é recusada por cada dado obrigatório; nenhuma compra, decisão ou e-mail novo.” | — |
| RM-12 | 2 | PARCIAL | “Gravação recusada; os dados originais permanecem e nenhum e-mail novo é enviado.” | CT-02: “E as decisões anteriores permanecem idênticas”. Omite preservação do histórico. |
| RM-13 | 1 | PARCIAL | “Ambas aguardam gestor; somente Bruno recebe uma mensagem de gestor por compra; zero decisões.” | CT-67: “com corpo não vazio que identifica esta solicitação e sua etapa pendente”. Omite conteúdo dos e-mails. |
| RM-13 | 2 | PARCIAL | “Compra de 5000.00 termina aprovada; a de 5000.01 aguarda diretor, com uma decisão de Bruno e um aviso para cada diretora.” | CT-17: “E os diretores recebem \<emails> e Ana e Bruno recebem zero e-mails novos”; exemplo de 5000.00: “zero e-mails”. Omite ausência de avisos na compra baixa e aos destinatários indevidos. |
| RM-13 | 3 | PARCIAL | “Compra alta aprovada; duas etapas, Bruno antes de Elisa; nenhum e-mail novo da conclusão.” | CT-19: “E a decisão de Bruno fica idêntica”; CT-65: “a compra de controle não muda e não há erro da ação”. Omite essas garantias. |
| RM-14 | 1 | FIEL | “Diálogo realmente visível e campo editável com JavaScript executado.” | — |
| RM-14 | 2 | FIEL | “Erro na justificativa, compra continua aguardando gestor, histórico idêntico e ação corrigível sem tela de erro ou aviso novo.” | — |
| RM-14 | 3 | FIEL | “Própria linha passa a rascunho; banco tem uma rejeição de gestor por Bruno com Sem verba, histórico anterior preservado e zero e-mails novos.” | — |
| RM-15 | 1 | PARCIAL | “Rascunho oferece editar/excluir/enviar; cada espera oferece cancelar; ambos cancelamentos mantêm dados/histórico e não enviam e-mail.” | CT-65: “Então a compra alvo fica \<destino>”; exemplos de cancelamento: “cancelada”. Omite o estado resultante dos cancelamentos. |
| RM-15 | 2 | PARCIAL | “Bruno aprova/rejeita somente aguardando_gestor; Diana aprova/rejeita somente aguardando_diretor; diretor não pula gestor.” | CT-58: “Então estão disponíveis exatamente \<acoes> entre editar, excluir, enviar, aprovar, rejeitar e cancelar”; “E as outras ações de escrita não estão visíveis ou montáveis”. Omite exclusão das demais ações. |
| RM-15 | 3 | PARCIAL | “Carlos não grava nem exclui a compra de Ana; terminais não oferecem as seis ações de escrita. Dados e histórico permanecem íntegros.” | CT-59: “a situação, os três dados e o histórico persistidos permanecem idênticos”; “nenhum e-mail novo é enviado”. Omite situação preservada e ausência de e-mails. |
| RM-16 | 1 | FIEL | “Cada compra informa sua própria situação: rascunho, aguardando gestor, aguardando diretor, aprovada ou cancelada; espera de diretor nunca aparece como final.” | — |
| RM-16 | 2 | PARCIAL | “Gestor associado a Bruno e diretora a Elisa na primeira; na segunda, Bruno, Diana e Carlos permanecem em ordem, com decisão, instante e Sem verba na rejeição.” | CT-56: “Então o detalhe associa etapa gestor a Bruno e etapa diretor a \<autora> com suas decisões e instantes”. Na primeira compra, omite decisões e instantes. |
| RM-16 | 3 | PARCIAL | “Coleção vazia não inventa estado; página 2 associa a compra alvo a cancelada, sem copiar situação de outra linha.” | CT-61, exemplo L+1: “somente a compra P2 em cancelada, sem qualquer compra da primeira página”. Omite cardinalidade e exclusão dos registros da primeira página. |
| RM-17 | 1 | PARCIAL | “Um único centro de Acme com Bruno; nenhum erro, compra, decisão ou aviso de aprovação.” | CT-48: “Então existe um único centro chamado "Compras ☕" de Acme associado a Bruno”. Adaptado o nome da fixture para MANUAL-UI-17, falta exigir sua persistência. |
| RM-17 | 2 | PARCIAL | “Mesmo centro conserva organização e nome; gestor Carlos persistido nas duas gravações, sem erro ou efeito de aprovação.” | CT-49: “E nenhuma solicitação ou decisão é criada e nenhum e-mail de aprovação é enviado”. Omite ausência de novas solicitações. |
| RM-17 | 3 | PARCIAL | “Carlos não consegue se nomear gestor nem excluir; mantém permissão de criar compra. Fernanda exclui o centro de teste sem afetar Compras/Viagens.” | CT-50: “nenhum centro novo é criado”; “Carlos continua sem permissões de administrar centros”; CT-64: “E nenhuma solicitação ou decisão é criada e nenhum e-mail de aprovação é enviado”. Omite essas garantias. |
| RM-18 | 1 | PARCIAL | “Coleção não contém compra estrangeira; detalhe recusa acesso sem expor dados; compra local continua acessível.” | CT-47: “recebe 403 ou 404”; “os dados e decisões de Globex não mudam”. Omite resposta determinada e preservação dos registros estrangeiros. |
| RM-18 | 2 | PARCIAL | “Operações recusadas; nome, organização e gestor estrangeiros intactos; centro local permanece acessível; nenhuma compra, decisão ou mensagem nova.” | CT-51: “Então a ação é recusada sem expor ou mudar nome, organização e gestor do centro estrangeiro”. Exige integridade, mas omite ausência de exposição. |

Totais:

| Classe | Passos |
|---|---:|
| FIEL | 18 |
| PARCIAL | 27 |
| DIVERGENTE | 0 |
| SEM RESPALDO | 0 |
| ORIGEM ERRADA | 1 |
| **Total** | **46** |

**FIEL + PARCIAL: 45/46 = 97,83%.** FIEL isoladamente: **39,13%**.

Cobertura significa presença de passos que exercitam a cláusula. Não significa execução comprovada nem cobertura integral dos CT.

| RQ vigente | Situação | Passos que a exercitam |
|---|---|---|
| RQ-01 | coberta | RM-01/1; RM-11/1; RM-12/1 |
| RQ-02 | coberta | RM-01/2; RM-07/1; RM-11/2 |
| RQ-03 | coberta | RM-01/3; RM-07/1; RM-11/3 |
| RQ-04 | coberta | RM-02/1; RM-03/1; RM-09/1 |
| RQ-05 | coberta | RM-02/2; RM-03/2–3; RM-13/2–3 |
| RQ-06 | coberta | RM-02/2; RM-05/2; RM-07/2 |
| RQ-07 | coberta | RM-05/1–2; RM-14/2–3 |
| RQ-08 | coberta | RM-04/1; RM-05/2; RM-14/3 |
| RQ-09 | coberta | RM-04/2–3 |
| RQ-10 | coberta | RM-08/2; RM-15/3 |
| RQ-11 | coberta | RM-06/1–2; RM-07/2–3 |
| RQ-12 | coberta | RM-16/1 e 3 |
| RQ-13 | coberta | RM-16/2 |
| RQ-14 | coberta | RM-02/1–2; RM-03/1–3; RM-13/1–3 |

**14 cobertas; zero declaradas fora; zero omitidas.** Existe negativo de permissão: **RM-07**, com tentativas por pessoas inelegíveis. RM-17/3 e RM-18 acrescentam negativos ainda não executados.

Segurança e honestidade documental:

- **Comando destrutivo sem aviso:** nenhum. O roteiro exige “somente nesta cópia SQLite descartável” e proíbe limpeza destrutiva.
- **Credencial aparentemente real:** nenhuma. E-mails usam `@manual.example.test`; a senha `password` está declarada sintética.
- **Conferência incompatível com resultado obtido:** nenhuma. Os 24 passos dos 10 RM conferidos estão preenchidos; os 22 passos dos oito não executados estão vazios.
- **Contagem incompatível com cabeçalho:** nenhuma. Há 18 RM: 10 conferidos e oito não executados, conforme declarado.

O roteiro parece derivado predominantemente da especificação, com perda de pós-condições ao resumir os CT. O indício mais forte é RM-10: mantém a recusa como esperado e registra a aceitação observada como divergência. Isso preserva o oráculo documental. Os três arquivos não permitem comprovar como o autor produziu o roteiro nem validar suas alegações sobre execução.