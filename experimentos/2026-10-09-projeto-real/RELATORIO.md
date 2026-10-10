# Avaliação em projeto Laravel real — resultado não aprovado

A revisão tornou a coletânea mais portátil, explícita e verificável. Esta rodada **não comprovou
melhora geral na derivação de testes**. A candidata melhorou no cenário de cupons e perdeu
cobertura no cenário de aprovação de compras. O gate pré-registrado permanece reprovado;
reduzir o número de cenários não compensa perder uma obrigação discriminante.

As métricas consolidadas estão no [README dos experimentos](../README.md#projeto-laravel-real--2026-10-09).
Este relatório explica sua interpretação, suas evidências e seus limites. Nenhum resultado
desfavorável foi descartado, nenhum denominador foi reduzido e nenhuma release foi publicada.

## O que foi comparado

O baseline A é o commit `6e9222c0f12769795dd4321e4f47f6509dbc2d9e`, com feature-wiki 4.0.0 e
feature-test-design 1.16.0. A candidata B é o snapshot da auditoria de portabilidade, com
feature-wiki 4.1.0 e feature-test-design 1.17.0. Os [ZIP completos](tratamentos/manifest.json)
e os hashes individuais preservam as instruções realmente usadas. As alterações posteriores
FW4.1.1 e FTD1.17.1/1.17.2/1.17.3 **não receberam a pontuação de B**.

O projeto é uma cópia descartável do kit existente `gsferro/starter-kit-easy`, localizado em
`demo-r8`. São dependências e infraestrutura reais: PHP 8.4.10, Laravel 13.25.0, Filament 5.7.6,
Livewire 4.4.0, SQLite, Pest e Chromium. Composer identifica Pest 5.1.1, enquanto a CLI informa
5.0.5; essa divergência não foi escondida. As features são experimentais no kit: não representam
validação de uma entrega em produção. Ambiente, banco, logs e credenciais originais não foram usados.

Houve uma geração por versão e cenário. Cada derivador leu seu próprio tratamento e o requisito
fixo; não recebeu catálogo, conjunto rival ou implementação. As perguntas permaneceram explícitas:
não se inventaram respostas para atingir a meta de cobertura. Revisores adversariais receberam
00 + 04/05, sem plano, código ou catálogo. Os derivadores originais fecharam os achados em até
duas rodadas, preservando os estágios. A revisão do delta final continua dívida declarada;
o teto de rodadas não transforma essa dívida em cobertura aprovada.

O implementador independente recebeu 00/01, sem conjuntos ou catálogos. Juízes receberam o
prompt histórico completo, o catálogo e o conjunto inteiro anonimizado, incluindo perguntas,
lacunas e relatório adversarial. A auditoria conferiu citações literais, IDs, denominador,
NCT e integridade dos arquivos. Isso prova proveniência textual; não automatiza a qualidade
do julgamento semântico.

Os despachos solicitaram esforço `ultra` na família GPT-6. O deployment exato não é exposto.
Os agentes usaram ferramentas de colaboração disponíveis; não se mediu carregamento nativo
dos perfis TOML. Filesystem irrestrito: contexto novo e contratos de caminhos restringem o
procedimento, sem provar isolamento técnico de leitura. O envelope comum permitiu zero achados
comprovados, portanto não se isolou causalmente o efeito de remover quotas do baseline.

## Julgamento cego e conferência do critério

Os [quatro vereditos primários](vereditos/) permanecem brutos e completos. Cupons preservou as
detecções anteriores e acrescentou D11, com o caso de criação de desconto fixo negativo.
A aprovação de compras perdeu cobertura na comparação primária. Entretanto, os dois juízes
originais aplicaram critérios diferentes em E06 e E08: reiniciar a elegibilidade foi confundido
com apagar histórico; autoaprovação foi confundida com uma segregação proibida pelo próprio
requisito, que permite solicitante = gestor.

Após os vereditos, o [plano de adjudicação](PLANO-ADJUDICACAO.md) definiu uma conferência
secundária em um contexto novo. O juiz recebeu ambos os conjuntos anônimos completos e os
mesmos instrumentos, sem placares anteriores ou identificação dos tratamentos. Os
[vereditos pareados](vereditos-pareados/) aplicaram critérios comuns e continuam separados
dos primários. Não são novas gerações nem um substituto conveniente para o resultado original.

Nessa conferência, ambos detectam E06/E08 sob o mesmo critério. O baseline detecta E12 por
rejeição, edição de valor e reenvio; a candidata mantém valor alto no seu exemplo e não cruza
a alçada. A leitura de E12 mudou em relação aos juízes primários, que exigiam edição durante
uma etapa em andamento. Essa mudança interpretativa é declarada, sem reescrever o catálogo.
Em E15, o baseline exige repetição da mesma aprovação válida do gestor com preservação do
histórico e da notificação. A candidata testa outras situações e a decisão do diretor,
sem discriminar essa repetição do gestor. Essa perda permanece sob o critério comum.

O gate exigia B atingir a meta nos dois cenários, sem perda por defeito, novas lacunas cegas
ou explosão de NCT. Ele falhou sob as leituras primária e secundária. Não se atribui a diferença
inteira às skills: geração única, revisão adversarial e variação de juiz impedem estimativa
estatística ou causal geral. Também não se ajusta o DDR retirando E08, D18 ou outros itens
problemáticos. A [validade do instrumento](VALIDADE-INSTRUMENTO.md) expõe essas contradições.

## Prova executável sobre a mesma referência

As traduções comparativas foram congeladas antes de sua execução. Cada cenário teve um
materializador novo com ambos os conjuntos anônimos, o contrato público e dependências de
teste. Ele não recebeu código da feature, controles do implementador, catálogo ou vereditos.
O contrato público continha texto comportamental, embora o despacho mandasse usá-lo apenas
como API: essa exposição limita a cegueira do materializador. A auditoria confrontou as
asserções com seus CT literais. Inventários registram todos os CT e Examples, inclusive
os omitidos. Não se emprestou uma expectativa do braço rival para completar uma lacuna.

As [traduções de cupons](testes/cuponsv2/) e [de compras](testes/comprasv2/) usam a referência
final v3. Todos os controles derivados passaram. Pest exercitou cálculo, validade, limite,
incremento, autoria, estados, alçada, ordem, histórico e notificações nas seleções literais.
Chromium executou os recortes de seleção, unidade e operabilidade do CT-B01; esses testes
**não gravam o cupom** e não cobrem todo o 05. O cenário de compras não teve tradução browser.
Os controles próprios do implementador e do kit têm finalidade separada: não contam como
detecção produzida pelas skills.

O [resultado executável](resultado-executavel.json) liga cada classificação aos logs integrais,
JUnit, comando e hashes. Os sete operadores inicialmente selecionados são um subestudo
exploratório pré-registrado antes dos vereditos, não o catálogo completo. Alterações físicas
foram executadas em série, uma expressão por vez, com controle verde e restauração byte a byte.
Não foi medido um MSI completo nem apresentado um resultado de `pest --mutate` para todo o catálogo.

Ambos os conjuntos detectaram os cinco operadores iniciais de cupons e a alçada incorreta de
compras. No operador que remove a recusa de justificativa vazia, H2 falhou na asserção de negócio;
V9 passou. O CT-44 de V9 omite o argumento e recebe `ArgumentCountError` da assinatura, sem
exercitar o guard de conteúdo vazio. Seu CT-45 de formulário está no inventário, mas não foi
materializado. **A sobrevivência pertence à tradução selecionada**, não prova que o conjunto
inteiro seja incapaz de detectar qualquer forma desse defeito. Também demonstra que DETECTA
documental não garante matar o operador concreto por qualquer implementação da frase.

Após os vereditos, foi acrescentada separadamente a seleção de criação de fixo negativo,
somente onde existia CT literal. O operador corrigido `c1-negative-fixed-input-enum` sobreviveu
em K7 e foi morto pelo CT-07 de M4, com erro específico do campo e demais dados válidos.
É uma confirmação física delimitada do ganho D11, condicionada à seleção posterior.
Ao juntar essas seleções, cada braço deixou sobreviver um operador diferente; isso não
estabelece superioridade geral. A tabela central mantém seleção inicial e adição posterior separadas.

## Falhas preservadas e correções da referência

1. **Referência v1:** M4 encontrou duas falhas de ator nulo. O requisito exige `User`, apesar da
   assinatura nullable sugerida no plano. O implementador original recebeu somente esse
   conflito 00/01, sem CT ou resultado rival, e corrigiu o modelo e suas chamadas. A
   [referência v2](referencia-v2/) foi capturada antes dos novos testes, mantendo as expectativas.
2. **Chromium:** os dois braços encontraram rótulo incorreto depois da seleção de tipo.
   Um probe DOM separado confirmou a seleção e o rótulo incorreto, sem erro de JavaScript.
   A análise independente do vendor comprovou que `Get` retorna enum nesse campo. Comparar
   com string fazia falhar rótulo e teto percentual. A [referência v3](referencia-v3/) corrige
   somente o Resource; os CT-B continuam iguais. Um controle próprio adicional verifica
   rejeição de 101 e aceitação de 100, sem entrar na comparação entre skills.
3. **Operador ineficaz:** a primeira alteração do mínimo negativo repetiu a comparação
   enum/string incorreta e não liberava a entrada. Seus verdes não são mutante sobrevivente
   válido. O operador novo tem nome e resultados separados; os anteriores não foram apagados.
4. **Tradução técnica:** o primeiro controle H2 falhou na montagem por `solicitante_id` nulo,
   antes de qualquer operador. O materializador original corrigiu somente a fixture usando
   `forceFill` conforme a API, mantendo casos, datasets e asserções. V9 teve a mesma correção
   estática, sem alegar execução anterior. [comprasv1](testes/comprasv1/) e seus logs permanecem.
5. **Fortalecimento da tradução de cupom:** o CT-07 passou a verificar erro de `valor` e
   ausência de erro nos demais campos; a adaptação técnica da data permanece registrada.
   Não foi provado que o formato de data causava o primeiro verde. Não se usou esse verde
   para declarar oracle fraco nem para atribuir um ganho artificial à candidata.

A [integridade final](integridade-final.json) confirma os tratamentos inalterados e todos os
arquivos da referência v3 restaurados. Ela não prova correção de negócio ou isolamento de leitura.
O metadado LF/CRLF dos primeiros congelamentos está explicitado na auditoria: o texto dado ao
juiz coincide byte a byte com o arquivo arquivado, mas o primeiro SHA normalizado não descrevia
os bytes gravados. O histórico original foi mantido.

## O que mudou nas skills depois da medição

- FTD1.17.1 corrige o contraexemplo percentual não discriminante. A expressão publicada é
  executada em PHP e tem regressão; o prompt novo não foi usado para julgar estes braços.
- FTD1.17.2 preserva partes determinadas de uma RQ quando uma pergunta afeta apenas um recorte.
- FW4.1.1 e FTD1.17.3 alinham entrevista, templates e retorno de delegação a essa distinção,
  condicionam rotas Claude ao host e removem alegações de isolamento por hooks heurísticos.
- A taxonomia exige intenção válida repetida por tipo de decisão. As armadilhas de API
  registram casts enum do Filament e asserções de erro específicas para evitar controles enganosos.

Essas correções têm evidência factual ou documental e regressões mecânicas. **Sua eficácia em
nova derivação está não medida.** Os braços antigos permanecem congelados. Não se repetiu a
derivação após conhecer o catálogo até obter uma nota agradável; uma próxima estimativa exigiria
novos requisitos, catálogo reservado, repetições e critério de julgamento calibrado previamente.

## Avaliação sincera antes e depois

**Antes:** a coletânea já tinha uma estrutura forte de requisito, decisão, teste e revisão.
Entretanto, exemplos falsos, aliases específicos de Claude em caminhos universais, promessas
excessivas de hooks e bloqueio integral de regras parcialmente determinadas diminuíam sua
confiabilidade. Muitos cenários e mutantes previstos no documento não eram prova executável.

**Depois:** contratos de host, instalação Codex, instruções de delegação e verificações
determinísticas ficaram mais claros. A execução real trouxe rastreabilidade completa e encontrou
defeitos tanto na referência quanto nos instrumentos. Há um ganho concreto em cupons, mas
perdas temporais e de repetição na aprovação; a seleção física também expôs um guard não
exercitado pela tradução da candidata. A coletânea ficou mais auditável. Não há evidência
suficiente para chamá-la de universalmente melhor, nem para afirmar que o gate comportamental passou.

A [revisão independente inicial](REVISAO-INDEPENDENTE.md) e a
[revisão final](REVISAO-FINAL.md) declaram seus escopos, achados, correções e limites.
Regressões mecânicas são verificadas separadamente pelos comandos do [README](README.md).
Não se confundem com a medição de derivação, tokens ou custo.

Permanecem fora da prova: variância entre gerações, comparação executada Claude/Codex, carregamento
nativo de todos os perfis, pipeline completo das cinco skills, toda a matriz de permissões,
concorrência real com conexões separadas, entrega SMTP, fluxo browser completo, MSI do catálogo,
economia de tokens e eficácia das correções posteriores. As omissões estão documentadas;
não receberam status de aprovadas.
