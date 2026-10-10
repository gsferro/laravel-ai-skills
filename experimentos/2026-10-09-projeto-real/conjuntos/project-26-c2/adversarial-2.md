# Revisão adversarial independente — rodada 2

Revisão textual do conjunto inteiro: CT-01–51, R1–R17 e M-01–65. O único oráculo foi o `00-requisito.md` vigente, incluindo as premissas A-01–A-12 nele escritas. Esse 00 legado não possui coluna Estado nem P-nn. As perguntas Q?1–Q?8 do 04 não constituem respostas nem revogam as partes determinadas do 00.

Foram lidos somente o corpo de `agents/fw-adversario-ct.md`, `references/revisao-adversarial.md`, o 00 e o 04 integral. `05-casos-de-teste-browser.md` e `wikis/glossario.md` não existem. Houve exposição incidental autorizada às notas e à tabela de fechamento da rodada 1 contidas no próprio 04; o relatório externo `adversarial-1.md` não foi aberto. Frontmatter, hooks e aliases Claude não foram usados como controles.

Contexto novo, agente Codex colaborativo, família GPT-6 herdada e esforço ultra solicitado; deployment exato não exposto. Filesystem irrestrito, sem whitelist ou hook efetivo: o cegamento foi contratual, não isolamento de leitura. Todas as chamadas de shell desta revisão usaram `login:false`.

Os 11 achados abaixo são contraexemplos ao conjunto descrito, não resultados de execução da aplicação. Nenhum teste Pest, Artisan, browser, transporte de e-mail ou mutante foi executado. A única verificação executável foi a leitura estrutural do Gherkin do 04, descrita na seção de cenários malformados. Nenhum CT foi editado.

## Implementações erradas que passam

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | Recusar toda operação administrativa de centro, inclusive de pessoa autorizada. CT-32/33 só exercitam recusas de `panel_user`; os centros dos demais CT são dados de preparo, não resultados de CRUD. Portanto todos os CT passam mesmo que ninguém consiga cadastrar ou manter um centro no painel. Q?1 sobre limites não suspende o CRUD mínimo válido determinado em A-01. | RQ-01/RQ-04; A-01/A-08; R9/R12. | Partição positiva de papel × operação; visita e gravação. | Dado administrador autorizado e dados válidos de centro, Quando cadastra pelo painel o centro Tecnologia com gestor G, Então consulta nova encontra Tecnologia, G e a organização correta; sondas equivalentes discriminam editar e excluir um centro sem dependências. |
| ADV-02 | Notificar todos os diretores, mas autorizar decisão apenas pelo primeiro da coleção. CT-50 tem D1/D2 somente como destinatários; CT-20/42 decidem com um único D. Nenhum CT faz o diretor que não é o primeiro decidir. A implementação preserva todas as asserções e contraria “qualquer pessoa com o papel pode aprovar”. | RQ-05/RQ-06; A-03/A-07; R5/R13/R17. | Partição de identidade dentro da cardinalidade N. | Dado D1 e D2 diretores da mesma organização e etapa de diretor pendente, Quando D2, que não é o primeiro da coleção, aprova, Então a solicitação fica aprovada e a decisão de diretor pertence a D2. |
| ADV-03 | Conferir somente o estado da instância carregada ao aprovar como diretor: depois de D1 resolver a etapa, D2 com snapshot antigo grava outra decisão. CT-26/27 recebem estados atuais; CT-31 testa rejeição de G após cancelamento, e CT-15/51 testam envio antigo. Uma falha restrita à aprovação de diretor não altera nenhum desses CT. O primeiro decisor deixa de resolver definitivamente a etapa. | RQ-05/RQ-10; A-03/A-05; R7/R13. | Estado × evento com instância antiga; rastreio de decisão. | Dado D2 carregou a etapa pendente e depois D1 a aprovou por transição real, Quando D2 aprova pela instância antiga, Então a consulta mantém a aprovação original, sem segunda decisão de diretor nem novo e-mail. |
| ADV-04 | Apresentar o histórico apenas quando a solicitação terminou com duas aprovações. CT-48 usa exatamente essa condição; CT-46/47 exigem só o status. O gestor que já aprovou fica invisível em `aguardando_diretor`, e a aprovação única de compra abaixo da alçada também desaparece, sem divergência em qualquer CT. O acesso pode ser dado como autorizado, sem responder Q?5. | RQ-13; A-12; R16. | Partição de estado e quantidade de etapas na apresentação. | Dado compra em aguardando_diretor com aprovação real de G e observador autorizado, Quando monta o detalhe, Então vê G atribuído à etapa de gestor já aprovada; repetir a sonda para aprovação final somente de gestor. |
| ADV-05 | Omitir da visualização o momento das decisões e a justificativa das rejeições. CT-20/35 exigem justificativa persistida, e CT-48 exige identidades das duas aprovações, mas nenhum CT afirma esses dois dados apresentados. A-12 determina “quem decidiu, quando e a justificativa”; Q?5 não suspende esse conteúdo para acesso autorizado, e desconhecer formato/fuso não impede afirmar o significado do instante conhecido. | RQ-12/RQ-13; A-12; R15/R16. | Rastreio da persistência à apresentação dos valores. | Dado rejeição real de G em instante conhecido com justificativa Sem verba e observador autorizado, Quando monta o detalhe, Então o histórico apresenta G, o instante daquela decisão e Sem verba. |
| ADV-06 | Recusar corretamente o envio sem gestor e exibir a mensagem, mas não registrar nenhum warning. CT-14 afirma estado, campos, histórico, mensagem e ausência de e-mail; o setup e a poda do 04 explicitamente deixam o warning sem CT. Todos passam sem o efeito que A-10 expressamente determina. | RQ-04; A-10; R3. | Rastreio de efeito exigido pela premissa. | Dado centro sem gestor e rascunho de S, Quando S tenta enviar, Então mantém o rascunho, apresenta a recusa e registra warning correspondente à tentativa recusada. |
| ADV-07 | Manter as ações visíveis, mas fazer os callbacks de aprovação pelo componente retornarem sem decidir; de forma equivalente, fazer a rejeição de diretor com justificativa válida não transitar. CT-34 só monta a listagem; CT-35 executa rejeição de G; CT-45 exige recusa sem justificativa. CT-16/20/42 executam decisões fora do componente. Portanto esses defeitos restritos à superfície passam por todo o conjunto. | RQ-05/RQ-06/RQ-08; A-07; R10/R13. | Partição por operação e superfície; efeito persistido de cada confirmação válida. | Dado etapa de gestor pendente abaixo da alçada, Quando G confirma aprovar pelo componente, Então a consulta mostra aprovada e decisão de G; sondas correspondentes precisam executar aprovação e rejeição válidas de D pelo componente. |

## Oráculos fracos

| ID | CT | Por que passa com defeito | O que o "Então" precisa afirmar |
|---|---|---|---|
| ADV-08 | CT-14; matador de M-12. | RQ-04/A-10 exigem recusa de envio sem gestor. Uma barreira somente no componente faz CT-14 recusar antes de chamar a operação defeituosa; fora do formulário ela aceita o centro sem gestor e põe a compra em trânsito. CT-11/15/49/51 usam gestor existente. Assim essa instância plausível de M-12 não diverge no matador indicado. | Uma chamada de envio fora do formulário com gestor ausente deve conservar rascunho/campos/histórico e produzir recusa, sem aprovação nem aviso a diretor. CT-14 conserva a prova da mensagem na superfície; não prova sozinho a barreira fora dela. |
| ADV-09 | CT-23. | RQ-04/RQ-14 e A-02/A-11: persistir corretamente C2 e o gestor corrente H, mas endereçar o e-mail do reenvio ao antigo gestor G, satisfaz o Então de CT-23. CT-49 verifica primeiro envio a G em C1; CT-50 verifica diretores; CT-51 repete o primeiro envio. Nenhum deles discrimina o destinatário depois da correção de centro. | Depois do reenvio de CT-23, H recebe exatamente um aviso mail daquela solicitação, e G/S/D não recebem aviso da nova etapa. A consulta deve manter C2 e H como já exigido. |
| ADV-10 | CT-36. | RQ-14/A-11: o componente pode gravar `aguardando_gestor` sem avisar G, ou gravar `cancelada` e enviar aviso extra de cancelamento. CT-36 exige somente situação e quatro campos. CT-49/50/51 e CT-28 exercitam chamadas diretas; o defeito restrito ao callback do componente conserva seus resultados. | Na linha de envio, G recebe exatamente um mail da solicitação e os demais não; nas duas linhas de cancelamento, nenhum destinatário real recebe aviso. Os efeitos precisam ser observados após o preparo e na própria confirmação pelo componente. |
| ADV-11 | CT-48. | RQ-13/A-12: renderizar o gestor atual do centro como autor da decisão, em vez da identidade histórica que aprovou, passa quando G continua sendo o gestor, como no Dado de CT-48. Nenhum CT monta o histórico após mudança administrativa do gestor. Mesmo com ambas as etapas visíveis, o histórico pode atribuir a aprovação a H que nunca decidiu. | Com aprovação real de G e posterior gestor atual H distinto, o detalhe autorizado deve continuar atribuindo aquela aprovação a G e não a H. O dado esperado é a identidade da decisão histórica, não a função atual. |

## Cenários malformados

- Nenhum encontrado em CT-01–51: todos possuem Então e exatamente um Quando. Uma leitura estrutural por Python, restrita aos blocos Gherkin do próprio 04, confirmou 51 cenários e lista vazia de malformados. Isso não executou testes de aplicação nem validou APIs.

## RQ sem cenário discriminante

- RQ-01–RQ-14 possuem ao menos um cenário discriminante para seu núcleo. Não há cláusula com Estado `aberta — Qn` no 00, nem P-nn a conferir. O 04 não pode converter Q?1–Q?8 em suspensão da cláusula inteira.
- Partes vigentes das premissas continuam sem discriminação: CRUD administrativo válido de A-01/A-08 (ADV-01); identidade elegível além do primeiro diretor e primeira decisão definitiva de A-03 (ADV-02/03); warning e recusa fora do componente de A-10 (ADV-06/08); conteúdo e atribuição histórica de A-12 (ADV-04/05/11). Os IDs são os mesmos achados das tabelas, sem dupla contagem.
- As lacunas de efeitos de RQ-14 na correção/reenvio e na confirmação pelo componente são ADV-09/10. Aprovação e rejeição válidas na superfície têm ADV-07. Perguntas sobre limites, diretoria vazia, recortes e link não recebem respostas nesta revisão.

## Sondas 6–8

| ID | Sonda (6 par de papéis / 7 participante histórico e link / 8 teto de texto) | Par, recorte ou campo | Lacuna | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| — | 6 par de papéis | Solicitante × gestor | CT-19 acumula S=G e discrimina a permissão expressa de A-09. | Já existe; nenhum achado adicional comprovado. |
| — | 6 par de papéis | Solicitante × diretor | Nenhum CT acumula S=D. Q?3 registra a ausência de decisão no 00; esta revisão não decide segregação nem aprovação própria do diretor. | Após resposta, dado S também diretor, Quando decide a etapa de diretor, Então afirmar a permissão ou recusa determinada e seus efeitos. |
| — | 6 par de papéis | Gestor × diretor | Nenhum CT acumula G=D. Q?3 registra a mesma lacuna de requisito. Não se inventa identidade distinta obrigatória nem colapso das etapas. | Após resposta, dado G também diretor e a primeira etapa já decidida, Quando decide a segunda etapa, Então afirmar a direção acordada e a ordem das decisões. |
| — | 7 participante histórico | Gestor/diretor que já decidiu, após devolução, cancelamento e aprovação | Quem tem acesso não está determinado pelo 00; Q?5 conserva essa pendência. CT-46/47/48 pressupõem acesso autorizado. ADV-04/05/11 tratam do conteúdo para quem já possui acesso, sem decidir o recorte. | Depende de resposta sobre acesso histórico; não há Então de autorização justificável a inventar. |
| — | 7 destino de link | E-mail ao próximo gestor/diretor | RQ-14/A-11 exigem e-mail, mas não exigem link. Q?6 pergunta se existe e qual destino; ausência de CT de link não comprova violação do 00. | Se o link for exigido, definir o destino e sua autorização no 00 antes de afirmar alcançabilidade. |
| — | 8 teto de texto | Descrição; nome do centro; justificativa | Nenhum teto n está escrito no 00. O 04 registra Q?1/Q?2 e não possui n/n+1 no domínio/model. É lacuna de especificação explícita; não se impõe 120, 255 ou outro valor. | Após definição de cada n, dado texto no teto ou um caractere além, Quando grava fora do formulário, Então afirmar persistência integral em n e recusa sem efeitos em n+1. |

As linhas com ID — são o registro das sondas e das direções indeterminadas, não achados de implementação comprovados nem novos ADV. Não se contabiliza falta de resposta como mutante morto ou violação já demonstrada.

## Áreas e regras percorridas

- Criação e dados válidos: RQ-01, A-01, R12, CT-38–40; limites e retry não definidos.
- Edição, exclusão e alvo inexistente/removido: RQ-02/03/10, A-05, R1/R2/R11, CT-01–10/37; mecanismo físico versus soft delete não decidido.
- Envio, autorização por centro, ausência de gestor e instância antiga: RQ-04, A-02/A-10, R3, CT-11–15.
- Aprovação/rejeição, justificativa, retorno, correção e reenvio: RQ-06–09, A-03/A-07/A-09, R4–R6/R14, CT-16–25/44–45.
- Alçada, limite literal/configurável, ordem, etapa final e imutabilidade: RQ-05/10, A-03–A-05, R7/R13, CT-26–27/41–43 e linhas terminais dos esquemas.
- Cancelamento, identidades e snapshot após outra transição: RQ-11, A-06, R8, CT-28–31.
- Administração de centros e execução no componente: A-01/A-08, R9/R10, CT-32–36; criação, edição e rejeição também conferidas em CT-04/05/14/39/40/45.
- Apresentação de status e histórico, atribuição, momento e justificativa: RQ-12/13, A-12, R15/R16, CT-46–48.
- E-mail, gestor singular, diretores 1/N, organização, não-efeitos, retry e reenvio corrigido: RQ-14, A-02/A-03/A-11, R17, CT-49–51 e os Então de efeito/ausência nas demais regras.
- Todas as 65 linhas de mutantes previstos foram confrontadas com o cenário e o matador indicado. M-12 tem o contraexemplo ADV-08; não se comprovou outra asserção indicada que deixe de divergir sob seu próprio mutante. Os demais ADV descrevem variantes não discriminadas pelo conjunto, não mortes medidas desses 65 mutantes.
- Sondas par a par, participante histórico/destino de link e tetos de todos os textos livres foram percorridas; direções sem suporte no 00 estão registradas acima.

## Leituras negadas

- Nenhuma. Não havia controle efetivo que negasse leitura; somente os caminhos autorizados foram deliberadamente abertos. O primeiro retorno agrupado sofreu truncamento de saída; as partes do 00/04 foram relidas em trechos, incluindo as linhas restantes da taxonomia, até a leitura integral. Não se usou essa restrição de saída como prova de cegamento.

Não conferidos: implementação, testes existentes, transporte SMTP, execução de mutantes e comportamento real. Os achados dependem de materialização dos cenários; o relatório não mede detecção nem equivalência entre hosts.
