# Pré-registro — comparação em projeto Laravel real

Registrado antes de receber os conjuntos ou os vereditos desta rodada.

## Pergunta e comparação

As alterações de portabilidade e rigor da auditoria mantêm ou melhoram a detecção de defeitos nas
especificações e em testes executáveis de uma aplicação Laravel? Não se presume que uma auditoria
de instruções melhore DDR; ela pode apenas tornar os limites e a dívida mais explícitos.

- A: skills do commit `6e9222c0f12769795dd4321e4f47f6509dbc2d9e`.
- B: snapshot da árvore de trabalho após a auditoria, antes desta rodada.
- Projeto: cópias descartáveis do `gsferro/starter-kit-easy` local `demo-r8`.
- Cenários: os dois oráculos congelados do protocolo, sem ADR `02` nos dois braços.
- Prompt: bloco `## Prompt` de `protocolo/PROMPT-BRACO.md`, literalmente, apenas com os marcadores
  substituídos. O prompt do juiz será reutilizado literalmente.
- Perfil: decidido pelo passo 0 de cada versão. Essa decisão faz parte do efeito da skill.
- Executor e juiz: agentes Codex em contexto novo, sem histórico compartilhado, com esforço
  solicitado `ultra`; identidade efetiva de modelo registrada conforme informação disponível.
- Uma execução por versão e cenário. A amostra não estima variância nem demonstra superioridade
  estatística, generalização a outras features ou paridade com Claude Code.

## Separação e controles

Braços leem apenas sua cópia, as skills nela instaladas e o oráculo permitido. As cópias não têm
catálogos, resultados antigos, testes `Exp*`, wikis de features anteriores ou `.env` original.
As convenções e regras do projeto são preservadas. Dependências instaladas são disponíveis para
consulta de APIs. Arquivos de ambiente, logs e bancos reais não são copiados.

A implementação é escrita por um terceiro agente, a partir de `00` e `01`, sem acesso aos
conjuntos nem aos catálogos. O materializador dos testes recebe a especificação e o contrato
público, sem ler a implementação da feature. As dependências no runtime usam hardlinks: arquivos
de vendor são imutáveis; metadados Composer locais ficam separados.

O filesystem desta sessão é irrestrito. Cegamento de leitura é um contrato de caminhos com contexto
novo e cópias limpas, não isolamento de segurança. Não se declara isolamento técnico que não existe.
As skills preservam suas referências empacotadas; conhecimento anterior nelas é parte do tratamento,
não evidência de que os executores tiveram acesso ao catálogo desta rodada.

## Ordem e critérios

1. Congelar snapshots, hashes de prompts/oráculos e ambiente.
2. Derivar cada conjunto inteiro e fechar a revisão adversarial por contexto independente.
   Se a capacidade de concorrência impedir despacho imediato, aguardar uma vaga; não substituir
   por autorrevisão. Registrar os retornos e todos os desvios.
3. Arquivar os conjuntos antes do julgamento. Conferir referências explícitas a IDs do catálogo.
   Remover somente identificação de versão/host/autoria na cópia enviada ao juiz; manter as
   asserções, lacunas e evidências substantivas. Registrar qualquer remoção.
4. Juiz em contexto novo por conjunto: catálogo + conjunto anonimizado e nada mais. Uma linha
   por defeito; DETECTA exige cenário e citação literal de asserção discriminante. Na dúvida,
   NÃO DETECTA. Verificar citações e denominadores; resultado inconsistente não é aprovado.
5. Comparar defeito a defeito e cenários separadamente. Critério de não regressão: B detecta todos
   os defeitos detectados por A e não introduz lacuna cega. DDR agregado igual não satisfaz isso.
   Distinguir melhoria de detecção, melhoria de honestidade e mera alteração de volume de CT.
6. Materializar testes Pest na cópia Laravel; executar a mesma implementação para os dois braços.
   Teste que falha no controle correto não serve de prova de detecção sem investigação e registro.
   Defeitos executáveis selecionados precisam de controle positivo e negativo. Catálogo não
   materializado integralmente não gera um mutation score de 18 nem substitui o DDR do juiz.
7. Arquivar comandos, stdout/stderr, códigos de saída, hashes, conjuntos inteiros e vereditos.
   Não esconder bootstrap quebrado, cenários não materializados, testes ignorados ou limites de UI.
8. Publicar avaliação antes/depois e atualizar os READMEs. Uma descoberta não autoriza alterar
   silenciosamente a candidata já medida: correção posterior é nova versão/snapshot e nova rodada.

## Métricas e limites antecipados

DDR de especificação, lacunas cegas/declaradas, falsos cobertos, oráculos fracos, número de cenários
e densidade. Na execução: testes executados/passados/falhos/ignorados, defeitos realmente aplicados
e quais testes os detectaram. Tempo observado inclui ambiente e não será atribuído à skill sem
controle. Não estimar economia de tokens, custo financeiro ou MSI sem instrumento correspondente.

Esta rodada mede principalmente a derivação `feature-wiki` + `feature-test-design` e sua integração
com o host Codex. Ela não mede exaustivamente o fluxo de tickets, publicação de Project Rules,
quality gate completo, todos os scripts ou a integração nativa dos perfis nos clientes.
