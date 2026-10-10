# Limites identificados antes dos resultados

O coordenador leu os catálogos depois do congelamento dos instrumentos, antes de receber qualquer
conjunto. Os executores e o implementador não receberam esta análise.

## O catálogo não substitui o requisito

O catálogo de aprovação chama autoaprovação de defeito (`E08`). O oráculo fixo, em A-09, assume
expressamente que o solicitante pode ser o gestor do próprio centro de custo. Não se pode exigir
uma segregação de funções que contradiz essa decisão. Um teste que aceita a pessoa legitimamente
gestora não está errado por deixar de proibir aquilo que o catálogo proíbe.

O catálogo de cupons inclui reaplicação no mesmo pedido (`D18`). O oráculo fixo P-01 remove o
agregado Pedido desta entrega e o contrato `aplicarEm(int, User)` não recebe identidade de pedido.
O motor sozinho não pode provar idempotência por pedido. A lacuna deve ficar explícita; implementar
um pedido fictício para matar esse item alteraria o requisito congelado.

O mesmo catálogo menciona cupom desativado ou soft-deleted (`D15`), enquanto o oráculo P-03 não
cria interruptor de ativação. A parte sobre registro excluído pode ser verificável; a parte sobre
desativação manual não autoriza inventar um atributo `ativo`.

O juiz mantém os dois arquivos e o prompt literal do protocolo. O relatório apresentará o DDR
bruto com denominador 18, sem substituir derrotas por vitórias, e distinguirá esses limites da
qualidade dos conjuntos. Não será publicado um DDR ajustado como se fosse o histórico original.

## Instrução comum dos despachos

Além do prompt literal, os despachos indicam a cópia permitida, proíbem executar Artisan nos
braços de especificação, pedem o retorno em arquivo e permitem aguardar vaga para a adversarial.
Também dizem que zero achados comprovados é válido: essa instrução comum de honestidade evita
fabricar defeitos, mas reduz a fidelidade à quota de achados da versão antiga. Portanto a rodada
não mede isoladamente o efeito de remover aquela quota. Toda conclusão fica limitada ao envelope
comum realmente usado.

## Dependências

O CLI Pest imprime `5.0.5`, mas `vendor/composer/installed.json` e `InstalledVersions` declaram
`5.1.1`. Ambas as fontes serão registradas. Uma string da CLI ou uma versão do lock, sozinha,
não resolve essa divergência. Os dois braços executarão as mesmas dependências instaladas.

## Exemplo numérico incorreto compartilhado

Antes do julgamento, o coordenador executou PHP 8.4.10 e confirmou que
`(int) (10000 * 0.29)` resulta em `2900`, igual a `intdiv(10000 * 29, 100)`.
`feature-test-design/references/tecnicas-por-regra.md` afirma erroneamente `2899`; o prompt literal
do juiz também afirma que esse exemplo distingue float de inteiro. As duas versões da referência
foram preservadas no snapshot, e o prompt do juiz não será alterado silenciosamente.

Em contraste, `(int) (100 * (29 / 100))` resulta em `28`, contra `29` no cálculo inteiro.
O defeito depende do operador concreto e da entrada. Uma afirmação genérica de que “usa float”
não prova detecção por qualquer exemplo percentual. O resultado bruto do juiz terá suas citações
e sua discriminação numérica conferidas. Eventual falso DETECTA será identificado na auditoria,
com veredito bruto preservado, sem contar uma assertion não discriminante como ganho real.

Depois de congelar os instrumentos desta rodada, a referência publicada foi corrigida na
feature-test-design 1.17.1 e o prompt publicado recebeu versão 2, com o contraexemplo executado.
Esta rodada continua julgada pelo prompt anterior completo de `instrumentos-congelados/`.
O congelador lê esse arquivo arquivado, não o prompt publicado posteriormente. Assim os
quatro julgamentos permanecem sob o mesmo instrumento; a correção não vira ganho atribuído
à candidata 1.17.0. A regressão da referência publicada verifica os dois resultados no PHP.

## Pergunta parcial tratada como bloqueio integral

Antes dos vereditos, a revisão independente da aprovação de compra comprovou que perguntas
novas no 04 haviam suspendido obrigações já explícitas no 00. O teto da justificativa estava
indecidido, mas sua obrigatoriedade não; os recortes de acesso estavam indecididos, mas a
apresentação de status e histórico em acesso autorizado não. A revisão demonstrou também
ausência de cenários para a alçada literal e para o envio positivo de e-mail.

Esses achados pertencem ao conjunto preliminar, não são ainda resultados finais de DDR.
O derivador original recebe a revisão e fecha os achados antes do congelamento e julgamento,
sem ler o catálogo. A publicação posterior 1.17.2 esclarece que `afeta:` bloqueia somente o
recorte dependente da resposta, e alinha template e contrato adversarial. Nenhum snapshot
de tratamento desta rodada foi alterado. Não se atribui a essa correção posterior um ganho
comportamental que não foi medido em nova derivação.

Evidência original: [revisão independente](revisoes/project-26-c2-rodada-1.md).
## Correção independente da referência executável

A primeira tradução de cupons foi congelada antes da execução. Na referência v1, o conjunto
K7 passou 33 casos; M4 falhou em dois exemplos do CT-41, por aceitar aplicação com ator nulo.
Essas falhas de negócio estão preservadas em `execucao-derivada/m4primeiro/`. Não são falhas de
bootstrap nem mortes de mutantes. O requisito exige argumento `User`; a assinatura nullable
no plano não revoga essa obrigação. O implementador original recebeu apenas esse conflito
entre 00 e 01, sem CT, catálogo, veredito ou log comparativo, e corrigiu a assinatura pública.

A [referência v2](referencia-v2/registro.json) preserva os arquivos v1, o patch exato e os hashes
antes da nova execução. Três arquivos mudaram: modelo Cupom, chamadas dos próprios controles
e contrato público. Expectativas dos testes derivados permaneceram idênticas. O controle
v2 executou 32 casos e 127 asserções, incluindo kit e Chromium. A comparação física dos
mutantes começou com v2 nos dois braços; a comparação final usa v3, descrita abaixo. A recusa nativa de `null` pelo parâmetro tipado é observável
na fronteira da API; não pode ser apresentada como validação completa de atores ou de toda
a autorização do domínio.

## Metadado dos primeiros conjuntos anônimos

Os dois primeiros congelamentos calcularam SHA do texto normalizado em LF, mas gravaram CRLF
no Windows. O arquivo usado pelo juiz é byte a byte igual ao arquivo anônimo arquivado; não
houve troca de conteúdo. O `freeze.json` original permanece intacto. As auditorias dos
vereditos registram tanto o SHA dos bytes reais quanto o SHA normalizado e identificam o erro
do metadado. O congelador foi corrigido para gravar LF explicitamente e calcular SHA dos bytes
gravados nos conjuntos seguintes. Não se declara que o hash histórico descrevia os bytes.

## Referência v3, operador ineficaz e controles de tradução

Chromium encontrou rótulo incorreto após a troca de tipo nos dois braços. O probe DOM confirmou
o tipo selecionado e ausência de erro de JavaScript; ele é diagnóstico, não CT comparativo.
A inspeção independente do vendor comprovou o cast enum de `Get` no Filament 5.7.6. A referência
comparava enum com string em rótulo e teto percentual. A [referência v3](referencia-v3/registro.json)
corrigiu apenas o Resource e foi arquivada antes da execução, sem relaxar asserções dos CT-B.
Sua [errata](referencia-v3/ERRATA.md) corrige o nome de método em uma explicação histórica,
sem alterar os arquivos de implementação ou manifestos preservados.

O primeiro operador `c1-negative-fixed-input` repetia a comparação escalar e não liberava o valor
negativo. Seus verdes não contam como sobrevivência válida. O operador corrigido
`c1-negative-fixed-input-enum` é separado e posterior aos vereditos: foi morto pela tradução M4 e
sobreviveu à K7, sem produzir MSI completo. A primeira tradução alterou também formato técnico
de data e especificidade do erro; não foi provado que a data causava o verde anterior.

O primeiro controle H2 falhou em `solicitante_id` nulo na fixture. Nenhum operador foi aplicado.
O materializador original passou a usar `forceFill`, preservando casos, dados e asserções.
As duas traduções de compras finais passaram sobre v3. A alteração que remove a validação de
justificativa vazia matou H2 e sobreviveu à seleção V9. V9 CT-44 omite um argumento e esbarra
na assinatura; seu CT-45 de formulário não foi materializado. Não se atribui essa sobrevivência
automaticamente ao conjunto inteiro. Esses resultados estão no [relatório](RELATORIO.md).

## Variação de juiz e exposição do materializador

Os juízes primários divergiram no critério de E06/E08. Uma conferência pareada posterior,
[pré-definida em documento separado](PLANO-ADJUDICACAO.md), aplicou o mesmo instrumento em um
contexto novo aos dois conjuntos completos, sem placares anteriores. E12 também recebeu uma
interpretação distinta. Os dois vereditos secundários permanecem separados dos primários;
não substituem a rodada nem eliminam a incerteza do instrumento. Citação literal não garante
critério semântico uniforme. O gate continua reprovado sob ambas as leituras.

Materializadores receberam os dois conjuntos anônimos do próprio cenário e viram texto
comportamental no contrato público, embora instruídos a usá-lo somente como API. Houve leitura
inicial do perfil PowerShell, declarada nos registros, antes de desativá-lo. Asserções foram
conferidas contra os CT literais. Esses controles são procedimentais e não certificam leitura
isolada. Derivadores, implementador original e juízes não receberam os resultados rivais.

Uma geração por versão/cenário não estima variância nem prova causa geral. As correções
posteriores de fonte não foram submetidas a uma nova derivação cega. Não se usa o catálogo
agora conhecido como holdout e não se repete a geração até conseguir um placar favorável.
