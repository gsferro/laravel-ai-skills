# Revisão adversarial independente — rodada 1

- Projeto exclusivo: `D:\PROJECTS\SKILLS\blind-20261009\project-71`.
- Entradas: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`, `04-casos-de-teste.md` e `05-casos-de-teste-browser.md` desta saída. Glossário local ausente, confirmado somente por existência do caminho autorizado.
- Contrato utilizado: corpo de `.ai/skills/feature-test-design/agents/fw-adversario-ct.md` e `references/revisao-adversarial.md`. Frontmatter, hooks e modelo Claude foram ignorados conforme o despacho.
- Host/rota: Codex, subagente independente, contexto novo. Família GPT-6; esforço ultra solicitado; identificador exato do deployment não exposto.
- Restrição efetiva: filesystem irrestrito, cegamento por contrato de caminhos. Sem whitelist mecânica ou hook executado. `login:false` em todas as chamadas de shell; nenhum `git status` ou rótulo read-only foi tomado como prova de isolamento.
- Escopo lido: conjunto inteiro, 64 CT e 2 CT-B, mapas, matrizes e tabelas de mutantes. As citações `04:n` abaixo são linhas do arquivo recebido.
- Resultado: **11 achados únicos**, ADV-01…ADV-11. IDs retomados nas sondas são remissões, não achados adicionais. A quota histórica de cinco não foi usada como critério.
- Nada de aplicação, Artisan, Pest, browser, mutation, SMTP ou medição comportamental foi executado. Costuras ainda propostas são limite de materialização; o relatório não confirma APIs nem inventa pontos de acesso.

## Implementações erradas que passam

Cada implementação abaixo pode conservar os demais comportamentos especificados. A prova de sobrevivência considera também o 05, não somente os CT da regra local.

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | Recusar envio sem gestor silenciosamente, sem mensagem na tela e sem warning no log. CT-13 verifica recusa, rascunho, decisões e e-mails (`04:418–423`), mas nenhum cenário observa mensagem ou log desse ramo. O descarte genérico de logs em `04:155` não elimina a obrigação explícita de A-10. Os CT-B só exercitam rejeição com gestor existente. | RQ-04, esclarecida por A-10: falha fechado **com mensagem na tela e warning no log**. | Rastreio de efeito positivo na falha; domínio × componente. | Dado um rascunho cujo centro não tem gestor, Quando o solicitante tenta enviá-lo pela tela, Então recebe mensagem de recusa e há warning da falha, enquanto estado, decisões e avisos permanecem sem alteração. |
| ADV-02 | O domínio recusa edição fora do rascunho, mas o componente autoriza o dono e salva campos diretamente sem conferir o estado. CT-26 cobre o domínio; CT-07/08 cobrem somente rascunho; CT-33 usa pessoa diferente da dona (`04:326–335;636–655;754–765`). Assim Sofia ainda consegue alterar sua própria compra aprovada pela superfície de edição, sem falhar em qualquer cenário recebido. | RQ-02 e RQ-10/A-05: editar somente rascunho; aprovada terminal. | Estado × operação na superfície de escrita do componente. | Dado uma compra aprovada de Sofia com campos e histórico capturados, Quando Sofia força sua edição pelo componente, Então a operação é recusada e todos os campos, estado, decisões e avisos permanecem iguais. |
| ADV-03 | A coluna de status reutiliza a situação do primeiro registro da página em todas as linhas. CT-45 consulta um registro por partição; CT-47 usa vários registros, todos em rascunho (`04:981–1017`); CT-64 também só requer uma compra própria em rascunho. O detalhe pode continuar correto. Todos passam, mas uma página com estados distintos mostra status errado. | RQ-12/A-12: situação atual na listagem de cada solicitação. | Partição de composição: registros heterogêneos na mesma página. | Dado duas solicitações de Sofia, uma em rascunho e outra aprovada, Quando Sofia consulta a mesma página da listagem, Então cada ID aparece com sua própria situação e nenhum recebe a situação da outra linha. |
| ADV-04 | Recusar exclusão de rascunho quando já existe alguma decisão histórica, por uma proteção indiscriminada do histórico. CT-09/10/11 usam rascunho inicial conforme o setup; as exclusões com história de CT-27 são de estados proibidos (`04:188;193;357–384;657–668`). Nenhum cenário exclui legitimamente o rascunho que resultou de rejeição. | RQ-03 e RQ-08: o solicitante pode excluir enquanto estiver em rascunho, inclusive o rascunho produzido pela rejeição. | Estado × evento, distinguindo origem do rascunho; histórico 0/N. | Dado a solicitação de Sofia voltou ao rascunho por rejeição real e possui histórico, Quando Sofia a exclui, Então a exclusão é permitida e a solicitação deixa de ser utilizável, sem novo aviso de aprovação. |
| ADV-05 | O edit do centro persiste gestor, mas ignora toda alteração de nome. CT-54 envia sempre o mesmo nome “Projetos”; CT-53 apenas o carrega; CT-55 testa alteração de nome somente por usuária sem autorização (`04:1088–1101;1123–1133`). As demais verificações não fazem alteração positiva de nome. | RQ-01/RQ-04, esclarecidas por A-01/A-08: CentroCusto com nome e CRUD mínimo pela administração. | Partição de campo editável; rastreio da gravação com valor diferente. | Dado Ana administra um centro Projetos com Paula gestora, Quando Ana altera seu nome para Operações mantendo Paula, Então o mesmo centro persiste Operações e Paula, sem criar outro registro. |
| ADV-06 | Impedir toda exclusão de centro, inclusive de centro próprio sem solicitações por administradora autorizada. As únicas tentativas de excluir centro são negativas: usuária comum em CT-55 e organização estrangeira em CT-59 (`04:1123–1133;1181–1190`). Create e edit continuam funcionando, portanto o conjunto inteiro passa. | RQ-01/RQ-04, esclarecidas por A-01/A-08: CRUD mínimo da entidade de administração. | Matriz papel × operação: exclusão positiva; referência zero. | Dado Ana administra um centro de Acme sem solicitações vinculadas, Quando Ana exclui esse centro, Então ele deixa de ser utilizável e os outros centros permanecem iguais. |
| ADV-07 | Recalcular a necessidade de diretor quando o valor diminui, mas conservar a dispensa anterior quando ele aumenta. As correções positivas de valor são todas de 8000.01 para 4999.99 em CT-05/07/22 (`04:299–311;326–330;565–570`); compras originalmente altas continuam corretas em CT-15/17. Logo todos passam, enquanto uma compra corrigida de baixa para alta termina somente com gestor. | RQ-02, RQ-05 e RQ-09: a solicitação corrigida acima da alçada continua exigindo diretor depois do gestor. | Transição de partição baixa → alta; 2-switch após correção. | Dado Sofia criou uma compra de 4999.99 e a corrigiu em rascunho para 5000.01, Quando Geraldo aprova o envio corrigido, Então ela aguarda diretor com uma decisão de gestor e aviso para os diretores da organização. |
| ADV-08 | Conservar decisões antigas no banco, mas renderizar somente o ciclo novo depois do reenvio. CT-21/22 verificam a conservação persistida; CT-49 mostra o histórico depois da rejeição e **antes** do reenvio; CT-48/50 mostram aprovação do primeiro ciclo (`04:553–570;1038–1057`). Nenhum cenário consulta o histórico depois de reiniciar o ciclo. O mutante pode manter o histórico visível em rascunho e ocultá-lo apenas depois do reenvio, passando por todos. | RQ-13/A-12: histórico de etapas com quem decidiu, quando e justificativa; não substituir a conservação persistida por prova de exibição. | Rastreio de efeito de apresentação no 2-switch rejeitar → reenviar. | Dado houve aprovação de gestor e rejeição de diretor com autores, instantes e justificativa conhecidos, Quando Sofia consulta o detalhe depois do reenvio, Então essas duas decisões anteriores continuam visíveis com seus dados íntegros. |
| ADV-09 | Acrescentar `ou é admin_organizacao` à autorização de aprovação/rejeição da compra no tenant corrente. Todos os atores negativos de CT-35/36/37 são comuns, gestores ou diretores sem o papel de administração; CT-34 também não combina administração (`04:767–778;799–838`). Os cenários de Ana tratam somente centro de custo. Mantendo a barreira de tenant, esse bypass passa inclusive CT-58/59, mas permite decidir etapa sem ser seu gestor/diretor. | RQ-04, RQ-05 e RQ-06, esclarecidas por A-02/A-03/A-08: administração do centro não substitui identidade do gestor nem papel diretor. | Acumulação de papéis, pares com administração; tabela de decisão de autoridade. | Dado o ator acumula administração com solicitante, gestor ou diretor, sem a autoridade da etapa corrente, Quando tenta aprovar ou rejeitar essa etapa, Então a decisão é recusada e estado, histórico e avisos ficam iguais. |

Não se propõe apagar histórico em ADV-04 nem definir cascata, soft delete ou retenção de centro em ADV-06: os oráculos afirmam somente a operação autorizada e a inutilização da entidade. Os demais comportamentos desses mecanismos não estão decididos no 00.

## Oráculos fracos

| ID | CT | Por que passa com defeito | O que o “Então” precisa afirmar |
|---|---|---|---|
| ADV-10 | CT-08 / M-08; também CT-07 | M-08 promete matar binding de outro registro, mas CT-08 não cria outro registro (`04:332–335;345`). Um componente que verifica autorização do ID pedido e depois carrega/salva sempre a primeira solicitação do dono devolve os valores esperados quando só existe aquela solicitação. CT-07 também parte de uma só; as outras edições de compra são de domínio ou tentativas não autorizadas. Essa implementação passa pelo conjunto inteiro e viola RQ-02 ao editar a segunda compra de Sofia. | Usar duas compras distintas do mesmo dono, consultar/editar a segunda e afirmar seus valores e ID, mais a conservação da primeira. A distinção precisa estar no Dado; os valores concretos atuais, sozinhos, não discriminam M-08. |
| ADV-11 | CT-18 / ramo de mínimo de M-22 | M-22 declara “exigir um tamanho mínimo não pedido” como mutante morto, mas “Sem verba” tem 9 caracteres (`04:496–507;540`). Um mínimo de 8 caracteres preserva esse texto e o Unicode usado e não diverge em CT-18, nem nos outros cenários positivos de rejeição, que usam esses mesmos textos. Os negativos vazios/brancos continuam recusados. É uma falha da demonstração de M-22 ligada a RQ-07/A-07, não uma autorização para decidir o mínimo que falta no requisito. | Especificar o mutante concreto realmente discriminado pelo texto existente, por exemplo um mínimo que rejeite “Sem verba”, ou registrar dependência de especificação. Não afirmar que CT-18 elimina toda a família de mínimos e não inventar um novo tamanho válido para corrigir a tabela. |

Os CT restantes possuem Então explícito com conteúdo, valores, estado, identidade, cardinalidade ou não-efeitos pertinentes à ação. Isso não transfere cobertura às partições ou superfícies ausentes dos ADV-01…ADV-09. Os demais mutantes M-01…M-67 e MB-01…MB-03 foram confrontados com os cenários indicados; não há outro caso comprovado de asserção que permaneça igual sob o erro específico anunciado.

## Cenários malformados

Nenhum ADV nesta categoria. Os 64 CT e os 2 CT-B têm Então explícito e uma linha Quando por cenário/esquema. Retry, decisões concorrentes e abertura/submit da mesma modal aparecem como ação composta deliberada; não há dois passos Quando independentes no texto recebido.

## RQ sem cenário discriminante

Nenhuma RQ está inteiramente sem cenário: RQ-01…RQ-14 têm ao menos um discriminante no 04/05. Há cobertura parcial, não fechamento integral:

- RQ-01: CT-01…04. O CRUD da premissa A-01 deixa os comportamentos positivos de ADV-05/06 sem prova.
- RQ-02: CT-05…08, CT-26 e CT-32/33. ADV-02/07/10 delimitam lacunas de estado, direção da correção e seleção do registro.
- RQ-03: CT-09…11, CT-27 e CT-32/33. Falta a origem pós-rejeição de ADV-04.
- RQ-04: CT-12…14, CT-35 e CT-41. Os efeitos expressos em A-10 faltam em ADV-01; administração não foi combinada em ADV-09.
- RQ-05: CT-15…17, CT-34…36 e CT-42. ADV-07/09 apontam partições ausentes.
- RQ-06: CT-15/17/18, CT-35/37 e CT-B01. ADV-09 delimita autoridade acumulada.
- RQ-07: CT-19/20 e CT-B02. ADV-11 delimita a alegação sobre o mínimo, sem criar regra nova.
- RQ-08: CT-18 e CT-B01.
- RQ-09: CT-21…23 e correções de CT-05/07. ADV-07 é uma direção ainda não discriminada.
- RQ-10: CT-26…31 no domínio. Falta a superfície positiva da dona fora do rascunho em ADV-02.
- RQ-11: CT-24/25/31/32/33 e CT-43, respeitando A-06.
- RQ-12: CT-45…47 e CT-57. ADV-03 é a composição heterogênea ausente.
- RQ-13: CT-48…50 e CT-57. ADV-08 não se confunde com prova de existência no banco.
- RQ-14: CT-41…44, CT-38 e ramos sem aviso; canal/destinatário/quantidade são previstos, entrega externa não medida.

O 00 é legado: não possui coluna Estado nem IDs P-nn. As premissas A-01…A-12 foram tratadas como vigentes, conforme a entrada; as frases históricas “pergunta em aberto” de A-06/A-09 não foram usadas para reabrir as decisões dadas. Portanto não há RQ com Estado aberta exigindo a linha “sem cenário até a resposta”.

## Sondas 6–8

| ID | Sonda | Par, recorte ou campo | Lacuna / evidência | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| — | 6 — par de papéis | solicitante × gestor; solicitante × diretor; gestor × diretor | Os três pares operacionais estão explícitos nas quatro linhas de CT-34; a segunda etapa permanece uma decisão própria. Sem novo ADV para esses pares. | — |
| Remissão ADV-09 | 6 — par de papéis | solicitante × administração; gestor × administração; diretor × administração | Os três pares com o papel de A-08 estão ausentes. O bypass administrativo comprovado em ADV-09 passaria. O papel panel_user é a permissão de base, não um quarto aprovador; não foi inventada segregação entre os papéis. | Dado Sofia solicitante/admin sem ser gestora, Geraldo gestor/admin sem ser diretor ou Daniela diretora/admin antes do gestor, Quando o ator tenta decidir a etapa sem sua autoridade específica, Então a tentativa é recusada sem efeitos. |
| — | 7 — participante histórico e link | consulta depois da decisão; destino de e-mail | CT-50 consulta por Geraldo após a etapa com permissão conservada. O 00 não define um recorte de visibilidade nem obriga link no e-mail; não há contrato para conceder/reter permissão de consulta ou escolher destino após revogação. Nenhum ADV foi fabricado para essas decisões ausentes. A exibição depois do reenvio é ADV-08, distinta de uma política de acesso. | — |
| — | 8 — teto de texto | descrição, nome do centro e justificativa | O 00 não fornece n. A lacuna está declarada no 04; não existe oráculo para aceitar n e recusar n+1 no model. Isso permanece não especificado e não medido, sem importar os números do plano. ADV-11 é somente a alegação não discriminante de M-22. | — |

## Áreas e regras percorridas

- **Dados de entrada — R1:** criação direta/componente, obrigatórios, valor textual, referências e Unicode.
- **Ciclo e alçada — R2…R9/R12:** edição, exclusão, envio, limite literal/default/configurado, aprovar/rejeitar, justificativa, correção/reenvio, cancelamento, cinco estados × oito operações, entidade removida, retry, concorrência e falha durante persistência.
- **Autorização e contexto — R10/R11/R17/R18:** dono, gestor certo/outro, diretor antes/depois, papel por organização, ator sem autoridade, papéis acumulados, administração, identificação estrangeira, filha histórica, payload protegido e tenant nulo.
- **E-mail — R13:** gestor, diretores 1/N, destinatários fora da organização, ocorrências positivas/negativas, canal mail, contagem e mensagem capturada. Zero diretores, link e falha após entrega permanecem sem política no 00.
- **Apresentação — R14/R15:** listagem/detalhe nos cinco estados, paginação 0/1/10/11, autores/instantes/justificativa, história após rejeição e consulta por participante com permissão. Mistura de estados e história depois do reenvio não foram inferidas como já cobertas.
- **Cadastro de centro — R16/R17:** visitas create/edit, gravação de nome/gestor, troca de gestor e edição sem alteração, bloqueio comum e centro estrangeiro. As operações positivas ausentes estão em ADV-05/06.
- **Browser — R6 / CT-B01…02:** abertura real, modal/campo visíveis, submit real, recusa vazia, erro ligado ao campo e não-efeitos persistidos. Localizadores continuam candidatos; nenhum DOM ou execução foi observado.
- **Oito tarefas:** implementações sobreviventes, força dos Então e dos matadores, formação dos cenários, rastreio de todas as RQ/premissas, conjunto inteiro, pares de papéis, história/link e teto de textos.

## Leituras negadas

Nenhuma ferramenta negou leitura. Não foram solicitados 01, implementação, testes, raciocínio/retorno da derivação, catálogos, experimentos, outra saída, outro projeto ou outro cenário. A ausência de negações **não comprova isolamento mecânico**: as restrições foram contratuais, com filesystem irrestrito.

## Limites da conclusão

A revisão é documental e demonstra lacunas dos oráculos propostos; não constata defeitos de uma implementação que não foi lida. Somente este relatório foi escrito. Nenhum cenário foi alterado. Não foram executadas as suítes de manutenção do repositório, por serem proibidas neste despacho de cegamento e execução. Tokens, custo, DDR, economia e equivalência entre hosts continuam não medidos.

