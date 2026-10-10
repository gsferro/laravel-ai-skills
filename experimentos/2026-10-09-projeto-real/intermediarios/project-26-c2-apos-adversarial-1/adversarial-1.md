# Revisão adversarial independente — rodada 1

Data: 2026-10-09. Host Codex; família GPT-6; ultra solicitado; deployment exato não exposto. Revisão integral de CT-01…CT-37, R1…R11 e M-01…M-42. **10 achados comprovados por contraexemplo textual**, sem execução da aplicação ou medição de mutantes.

Entradas: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md` e `wikis/specs/saida-c2/aprovacao-de-compra/04-casos-de-teste.md`. `05-casos-de-teste-browser.md` e `wikis/glossario.md` não existem. Foram lidos o corpo de `.ai/skills/feature-test-design/agents/fw-adversario-ct.md` e `references/revisao-adversarial.md` da mesma cópia. Frontmatter, hook e modelo Claude não foram aplicados.

O `00` é legado, sem coluna Estado ou P-nn. As cláusulas literais e as premissas explicitamente assumidas A-01…A-12 permanecem a fonte vigente. As perguntas Q?1…Q?8 do `04` não revogam obrigações já determinadas no `00`. Os achados abaixo usam somente essas partes determinadas; não respondem às perguntas pendentes.

## Implementações erradas que passam

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | A operação de criação de solicitação sempre recusa, mantendo disponível a criação de registros para o preparo das fixtures. Todos os CT começam com solicitações existentes; CT-01/05 corrigem, não criam. O próprio setup distingue `Model::create` para preparo de prova da operação de criação (`04:172`). Nenhuma asserção muda com essa falha. | RQ-01 (`00:41`): o solicitante cria descrição, valor e centro. Q?1/Q?7 deixam limites e retry pendentes, não a existência de criação com dados válidos. | EP positiva e rastreio da gravação. | Dado S e dados válidos Notebook/3000.00/C1, quando S cria uma solicitação pela operação oferecida ao solicitante, então uma consulta nova encontra a solicitação de S com os três valores informados em rascunho. |
| ADV-02 | Usar `valor >= limite` no lugar de `valor > limite`. Com o limite efetivo em 5000.00, uma compra de 5000.00 ganha uma etapa de diretor indevida. Nenhum CT exercita esse valor: CT-11 usa 3000.00/6000.00 e apenas o primeiro envio; CT-16 usa 3000.00 e só afirma a decisão. 4999.99/5000.00/5000.01 aparecem exclusivamente na preparação futura (`04:159`). Os valores efetivamente exercitados não distinguem os comparadores. | RQ-05 e A-04 (`00:45,97`): estritamente maior, default 5000.00. S/G/D distintos e diretor disponível dispensam respostas sobre papéis acumulados ou zero diretores. | BVA da fronteira de alçada e destino após decisão. | Dado limite efetivo 5000.00, S/G/D distintos e solicitação de 5000.00 aguardando G, quando G aprova, então a consulta nova mostra aprovação final sem etapa pendente de diretor. |
| ADV-03 | Aceitar rejeição sem justificativa, persistindo normalmente a justificativa quando informada. CT-20/21/22/27/31/35/37 fornecem sempre Sem verba; nenhum cenário omite a justificativa. Remover a obrigatoriedade conserva todos os resultados exigidos. | RQ-07 (`00:47`) e A-07 (`00:127`): justificativa obrigatória também na rejeição do diretor. Q?2 não impede distinguir ausência de presença. | EP ausente/presente e rejeição sem efeito. | Dado uma etapa pendente para seu aprovador corrente e agregado/efeitos capturados, quando ele rejeita sem informar justificativa, então a rejeição é recusada e situação, campos, histórico e e-mails permanecem iguais. |
| ADV-04 | Renderizar listagem e detalhe sem o status atual. Campos de edição e ações continuam funcionando. CT-34 afirma visibilidade de ações; os demais Então sobre situação consultam persistência, não o status apresentado. A retirada do status de ambas as telas passa por todos os oráculos. | RQ-12 e A-12 (`00:52,172`): status atual na listagem e visualização. O defeito suprime a informação para todos os acessos, independentemente do recorte ainda pendente. | Rastreio do valor apresentado por superfície. | Dado acesso autorizado a uma solicitação em aguardando_gestor, quando a listagem ou o detalhe é montado, então a tela apresenta o status atual aguardando_gestor para essa solicitação. |
| ADV-05 | Omitir da tela o histórico com as identidades de quem aprovou, preservando as decisões no banco. CT-16/19 verificam decisão persistida; CT-34 verifica ações; nenhum Então verifica quem aprovou na visualização. O defeito passa mesmo com histórico corretamente gravado. | RQ-13 e A-12 (`00:53,172`): quem aprovou cada etapa no histórico da visualização. Não é necessário decidir quais outros usuários podem acessar para provar a omissão em todo acesso autorizado. | Rastreio da decisão até a apresentação. | Dado acesso autorizado a uma solicitação com aprovações reais de G e D, quando o detalhe é montado, então o histórico apresenta G na etapa de gestor e D na etapa de diretor dessa solicitação. |
| ADV-06 | Desativar todo despacho de e-mail para o próximo aprovador. As negativas continuam sem e-mail; CT-11/23/24/36 não exigem e-mail no envio, e CT-16/19 não exigem e-mail após aprovação. A observação de efeitos começa depois do preparo, que também não exige entrega. Todas as asserções sobre e-mail são satisfeitas pelo silêncio total. | RQ-14, A-02/A-03/A-11 (`00:54,78,87,164`): e-mail ao próximo aprovador, gestor singular e diretores da organização. Link, zero diretores e transporte SMTP são questões separadas. | Rastreio positivo de efeito, canal e destinatário. | Dado rascunho de S com C1 cujo gestor é G e outras pessoas reais disponíveis, quando S envia, então G recebe uma notificação pelo canal e-mail dessa solicitação e as demais pessoas não recebem o aviso dessa etapa. |
| ADV-07 | Na rejeição da etapa de gestor, autorizar qualquer gestor de centro, mantendo correta a autorização de aprovação e a barreira de estado. H, gestor de outro centro, conseguiria rejeitar a solicitação de C1. CT-18 chama H somente para aprovar; CT-22 testa S/U/D em aguardando_gestor, mas não H; CT-20 usa G correto. Todos os cenários existentes conservam seus resultados. | RQ-04/RQ-06 e A-02 (`00:44,46,78`): o aprovador da etapa de gestor é o gestor daquele centro. | Matriz identidade × verbo: aprovação e rejeição precisam de sondas próprias. | Dado solicitação de C1 aguardando seu gestor G, H gestor de C2 e campos/histórico capturados, quando H rejeita com Sem verba, então a operação é recusada e situação, campos, histórico e e-mails ficam iguais. |

## Oráculos fracos

| ID | CT | Por que passa com defeito | O que o "Então" precisa afirmar |
|---|---|---|---|
| ADV-08 | CT-16; CT-19 tem a mesma limitação de destino, sem fixar valor. Origem: RQ-05/A-04. | Em CT-16, uma aprovação de G que grava exatamente uma decisão correta, mas deixa a compra de 3000.00 em aguardando_gestor, satisfaz integralmente o Então. A persistência da decisão não discrimina a transição de aprovação final exigida para essa faixa. Isto é um contraexemplo ao oráculo de CT-16, não uma alegação de que esse mutante necessariamente passaria pelo preparo de todos os outros CT. | Em CT-16, além da decisão atribuída a G, a consulta nova deve mostrar aprovação final para 3000.00 com limite efetivo 5000.00. Em CT-19, explicitar valor/limite antes de exigir o destino correspondente; não escolher a combinação S=D. |
| ADV-09 | CT-10 / M-08 e CT-37 / M-41; CT-09 também permite o mesmo V sem capacidade de edição. Origem: RQ-03/RQ-04/RQ-06/RQ-11, identidade do agregado alvo. | V é apenas “válida”; estado, dono e capacidade de sofrer cada operação não estão fixados. Contraexemplo permitido: V aprovada por transições reais, pertencente a S. Um resolver defeituoso troca o ID ausente pelo primeiro registro V e, depois, as barreiras corretas do estado aprovado recusam editar/excluir/enviar/aprovar/rejeitar/cancelar. V fica igual, o alvo continua ausente e não há decisões/e-mails. As asserções anunciadas para M-08/M-41 não divergem nesse preparo; por isso não garantem matar esses mutantes. | Preparar V para ser alterável pela mesma identidade e pela operação concreta, sem mudar o alvo ausente. A asserção de preservação só discrimina o resolver errado se executar a operação em V, por engano, produziria um efeito observável. Não basta acrescer outra asserção sobre V terminal. |

Os demais pares M-01…M-42/asserção foram percorridos; não foi comprovada outra asserção não discriminante sob seu próprio mutante. Essa leitura não mede morte de mutantes.

## Cenários malformados

- Nenhum dos CT-01…CT-37 está sem Então ou tem mais de um Quando. Os percursos necessários ao estado inicial aparecem no Dado; não foram contados como ações adicionais do cenário.

## RQ sem cenário discriminante

As referências abaixo retomam os achados das tabelas; ADV-10 registra a parte de configurabilidade ainda não coberta por esses achados.

- RQ-01 — criação com dados válidos: ADV-01. A lacuna de domínio/retry não suspende a operação já pedida.
- RQ-05/A-04 — fronteira estritamente maior que 5000.00: ADV-02; destino da aprovação de gestor na faixa inferior: ADV-08. S=D/G=D e zero diretores permanecem sem resposta, sem resultado inventado.
- RQ-07/A-07 — ausência de justificativa: ADV-03. O `04:79` transforma toda a cláusula em aberta embora `04:118` reconheça que a obrigatoriedade está dada.
- RQ-12/A-12 — status apresentado: ADV-04. Visibilidade por usuário é uma lacuna distinta da supressão global da informação exigida.
- RQ-13/A-12 — identidades dos aprovadores na visualização: ADV-05. Uma decisão persistida não discrimina sua apresentação.
- RQ-14/A-02/A-03/A-11 — e-mail positivo ao próximo aprovador: ADV-06. As recusas sem e-mail não discriminam o envio exigido no sucesso.
- RQ-02, RQ-03, RQ-04, RQ-06, RQ-08, RQ-09, RQ-10 e RQ-11 possuem cenários discriminantes de suas operações principais; os contraexemplos de autorização da rejeição e da tabela de mutantes estão em ADV-07/09.
- A-01/A-02/A-08 — entidade administrativa com um gestor e bloqueio ao panel_user foram percorridos. CT-32/33 discriminam a proibição administrativa; não há gravação positiva de administração. O relatório não escolhe quem administra ou os domínios ainda ausentes.
- A-03/A-04/A-12 — têm partes determinadas não discriminadas, registradas acima; não são integralmente abertas. A-05/A-06/A-07/A-09/A-10/A-11 têm sondas correspondentes de terminalidade, cancelamento no trânsito, rejeição do diretor, S=G, centro sem gestor e ausência de avisos adicionais.
- ADV-10 — RQ-05/A-04, limite configurável (`00:97`): uma implementação que ignora `kit.compras.limite_diretor` e compara sempre com o literal 5000.00 passa os cenários atuais; nenhum varia a configuração, e a única preparação BVA futura fixa o limite efetivo em 5000.00 (`04:159`). Falta variar o discriminante para separar configuração de constante. Oráculo sugerido: Dado limite efetivo 7000.00, S/G/D distintos e solicitação de 6000.00 aguardando G, quando G aprova, então a consulta nova mostra aprovação final sem etapa pendente de diretor. O literal errado produz aguardando_diretor nesse mesmo caso; não depende de resposta sobre papéis ou zero diretores.

Não há RQ com `Estado: aberta — Qn` no `00`, nem P-nn formal. Q?1…Q?8 são perguntas do `04`, não mudanças confirmadas no requisito. Não foi contado como defeito um resultado cuja decisão esteja ausente.

## Sondas 6–8

| ID | Sonda (6 par de papéis / 7 participante histórico e link / 8 teto de texto) | Par, recorte ou campo | Lacuna | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| — | 6 par de papéis | S×G | CT-19 exerce a mesma pessoa nos dois papéis, conforme A-09. O destino insuficiente já consta em ADV-08; não é outro achado. | — |
| — | 6 par de papéis | S×D | Sem cenário de acumulação; Q?3 declara o limite. A-09 responde apenas S=G. Permissão ou vedação de S=D não foi decidida, portanto não há ADV com resultado inventado. | Após decisão do requisito, fixar o resultado permitido ou recusado para a mesma pessoa como solicitante e diretor. |
| — | 6 par de papéis | G×D | Sem cenário de acumulação; Q?3 declara o limite. A-03 define o papel de diretor, mas não decide a acumulação das duas etapas pela mesma pessoa. | Após decisão do requisito, exercitar a mesma pessoa nos dois papéis com o resultado e a ordem que forem determinados. |
| — | 7 participante histórico e link | Gestor/diretor que já decidiu; listagem/detalhe | Q?5 declara acesso histórico pendente; o `00` não define o recorte por participante. CT-34 esconde a ação de rejeitar de G na etapa de diretor, o que não prova nem proíbe o acesso histórico. | Após decisão do recorte, observar separadamente listagem e detalhe do participante anterior em cada estado acordado. |
| — | 7 participante histórico e link | Destino de link de e-mail | RQ-14 exige e-mail, mas não exige link. Q?6 registra a decisão ausente. ADV-06 usa somente o canal/destinatário já exigidos. | Se o requisito confirmar link, observar que seu destinatário alcança o destino autorizado após a mudança de etapa. |
| — | 8 teto de texto | Descrição, justificativa e nome do centro assumido em A-01 | O `00` não fornece nenhum teto n. Q?1/Q?2 declaram a lacuna de domínio; não há n/n+1 no model nem no formulário. A ausência de n impede provar violação de um teto concreto. A obrigatoriedade da justificativa já é determinada e está em ADV-03. | Depois de o requisito fixar n para cada campo, observar aceitação em n e recusa em n+1 na gravação fora do formulário. |

## Áreas e regras percorridas

- Criação e dados: RQ-01; descrição, valor e centro; A-01 e domínios declarados pendentes; edição por campo e pelo componente, CT-01…05/R1.
- Autorização e exclusão: RQ-02/03; solicitante, outro solicitante, gestor próprio, gestor de outro centro, diretor; estados e IDs removidos/inexistentes, CT-01…10/R1–R2. Sensibilidade do registro V em M-08/M-41.
- Encaminhamento e aprovação: RQ-04/05/06; A-02/A-03/A-04/A-09/A-10; envio normal, sem gestor, retry e instância antiga; comparação de alçada, ordem, identidade e decisão, CT-11…19/R3–R4.
- Rejeição e novo ciclo: RQ-06/07/08/09; A-07/A-11; rejeição por etapa, justificativa, troca de centro/gestor, aval antigo e correção do dono, CT-20…25/R5–R6.
- Estado terminal e cancelamento: RQ-10/11; A-05/A-06; recusas em todas as situações tabeladas, cancelamento nas duas etapas, identidade e snapshot anterior ao cancelamento, CT-26…31/R7–R8.
- Administração: A-01/A-08, criação/edição/exclusão administrativas recusadas ao panel_user por chamada direta e componente, CT-32/33/R9.
- Interface: RQ-12/13 e A-12; status e história na tela, formulário preenchido, ações por situação/ator e transições pelo componente, CT-04/05/14/33…36/R10.
- Integração: RQ-14; A-02/A-03/A-11; e-mail positivo, ausência de avisos adicionais, recusas sem efeitos e destinatários reais. Zero diretores, link e transporte permanecem não decididos ou não executados conforme a entrada.
- Agregado removido: operações de CT-37/R11, conservação do outro registro e sensibilidade dos mutantes M-40…42. A costura de exclusão é proposta, sem certificação do mecanismo físico/soft delete.
- Sondas 6–8: todos os pares S×G/S×D/G×D; acesso histórico/lista/detalhe e link; descrição/justificativa/nome do centro. Limites sem decisão ficaram explicitamente sem ADV.

## Leituras negadas

- Nenhuma leitura foi negada por ferramenta; nenhuma tentativa fora dos paths autorizados foi feita.
- Restrições efetivas: filesystem irrestrito, sem whitelist ou isolamento técnico de leitura. O cegamento desta revisão foi contrato de caminhos. Todos os comandos de leitura usaram `login:false`; nenhum perfil PowerShell foi acionado por login deliberado.
- Não foram lidos `01`, código, testes, retorno externo da derivação, catálogo, experimentos, outro projeto ou outro cenário. As referências a esses itens contidas no `04` não foram seguidas.
- Não foram executados Artisan, Pest, navegador, testes Python, app, mutation testing ou expressão matemática. As costuras propostas não foram materializadas nem validadas; não foi inventada API para realizá-las.
- Única escrita: este `adversarial-1.md`, conforme exceção explícita do despacho. Cenários e demais arquivos não foram editados. DDR, economia de tokens, equivalência de hosts e morte de mutantes continuam não medidos.
