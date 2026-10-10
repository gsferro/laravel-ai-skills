# Revisão independente — manutenção e evidências do projeto real

Revisor: contexto independente de manutenção, família GPT-6, esforço ultra solicitado; deployment exato não exposto. Data: 2026-10-09. Esta revisão não é um braço de derivação nem um juiz cego. Recebeu o escopo da auditoria e leu os artefatos arquivados, inclusive conjuntos e vereditos.

O filesystem é irrestrito. A restrição de leitura foi contratual: seleção explícita dos arquivos da coletânea e dos artefatos arquivados. Não houve acesso ao ambiente original, `.env`, bancos ou logs originais; nenhum arquivo externo do runtime foi necessário. Não houve execução de Laravel, Artisan, Pest, servidor ou navegador. Na fase inicial de revisão, a única escrita foi este relatório; as verificações de scripts usaram fixtures temporárias e mocks. Depois de aceitar os achados, a sessão principal delegou as correções específicas abaixo. Essa fase de implementação é distinta da revisão inicial e não constitui uma segunda revisão independente das próprias correções. Nenhuma dessas restrições constitui isolamento técnico.

## Achados concretos

### RI-01 — P2: obrigações universais ainda dependem de ferramentas/modelos Claude

**Localização observada:** `.ai/skills/feature-test-design/SKILL.md:689`, `:696`, `:701`; `references/revisao-adversarial.md:55`; `.ai/skills/feature-wiki/SKILL.md:569`, `:1326`, `:1329`. As linhas correspondem à leitura antes das correções da sessão principal.

**Prova:** o corpo da feature-test-design exige fallback `general-purpose` com `model: opus` explícito, enquanto o contrato compartilhado `feature-wiki/references/hosts-e-subagentes.md:19` proíbe passar aliases Claude ao Codex e permite herança do modelo. O checklist final da feature-wiki exige `ls .claude/agents/fw-*.md` sem condição de host. Ambos os SKILLs afirmam categoricamente que subagente não despacha subagente, embora o contrato portável precise definir responsabilidade do fechamento, e não inventar indisponibilidade de uma ferramenta do host.

**Efeito:** um consumidor Codex recebe obrigações incompatíveis com a própria seção de capacidades e pode interromper a revisão independente ou procurar uma rota inexistente. A inconsistência permanece no procedimento obrigatório mesmo com o README corrigido.

**Correção:** preservar revisão por quem não derivou, contexto novo, entradas limitadas, fechamento pela sessão principal e declaração de revisão não feita quando faltar independência. Remeter escolha de rota/modelo e instalação ao adaptador efetivo. Condicionar checks `.claude` e fallback `general-purpose` ao Claude. Descrever a propriedade de orquestração sem proibição universal de aninhamento. Não alterar os ZIP dos tratamentos medidos.

### RI-02 — P2: promessa de cegueira excede o controle do hook

**Localização observada:** `.ai/skills/feature-test-design/SKILL.md:696`; `.ai/skills/feature-wiki/SKILL.md:36`, `:149`; `.ai/skills/feature-wiki/README.md:297`, `:379`; `feature-wiki/scripts/guarda-subagente.sh:2`.

**Prova:** os textos ainda usam “cego por construção” ou “cegueira por construção”, ao passo que o contrato compartilhado declara que hook por padrões não prova isolamento. O próprio adaptador registra vias não cobertas, como MCP e leitura por outros caminhos. Comparação de conteúdo/hashes detecta mudanças nos arquivos selecionados; não prova ausência de leitura.

**Efeito:** o relato de independência pode certificar uma propriedade que o mecanismo não estabelece. Esse problema é diferente da escolha legítima de aliases no adaptador Claude: a promessa de cegueira continua excessiva mesmo nesse host.

**Correção:** descrever negativas nas ferramentas e padrões efetivamente cobertos, ferramentas disponíveis, contexto inicial e vias restantes. Substituir a promessa de cegueira por restrição de ferramentas com limites declarados. Manter hook, entradas e auditoria de alterações; não apresentar `read-only`, hook ou `git status` como isolamento.

### RI-03 — P2: duas linhas de referência contradizem a correção de perguntas parciais

**Localização observada:** `.ai/skills/feature-test-design/references/tecnicas-por-regra.md:232` e `:281`.

**Prova:** a linha “direção da premissa” ainda diz “a RQ fica aberta”; a linha “de comportamento” determina que uma pergunta transforma a RQ em `aberta — Qn`. Mais abaixo, e no SKILL/template/agente 1.17.2, a nova regra exige bloquear somente o recorte dependente da resposta e conservar obrigações determinadas. O texto percentual inserido entre as linhas também separou “direção da premissa” da tabela à qual pertence.

**Efeito:** a referência obrigatória do passo 3 pode reintroduzir o bloqueio integral demonstrado pela revisão da aprovação de compra, contrariando o comportamento que a 1.17.2 pretende corrigir.

**Correção:** nas duas linhas, bloquear a direção/recorte indecidido; reservar a RQ inteira aberta ao caso em que toda ela depende da resposta. Preservar invariantes e CT de partes determinadas. Recolocar a linha dentro da tabela e deixar a explicação numérica após a tabela. Não responder às perguntas do solicitante nem inventar seus limites.

### RI-04 — P2: a tradução negativa por componente ainda não comprova a recusa do campo alvo

**Localização:** `testes/cuponsv1/tests/ExperimentoReal/M4/CuponsTest.php:206`; `execucao-mutantes/m4v2/resultado.json`, operador `c1-negative-fixed-input`.

**Prova:** a tradução de CT-07 chama `assertHasFormErrors()` sem identificar `valor`. O mutante que permite fixo −1 preservou exit code 0; CT-07 registrou cinco assertions e nenhuma falha. O controle desse conjunto também está verde e aponta o manifesto da referência v2. No K7, o mesmo operador também retorna 0, sem CT negativo correspondente. Esses resultados chegaram depois da conferência inicial da tradução.

**Efeito:** um erro em outro atributo satisfaz a assertion genérica; banco vazio tampouco identifica o motivo da recusa. A sobrevivência é factual, mas a causa ainda precisa ser classificada: pode haver bloqueio técnico, oracle fraco ou uma barreira legítima em outra camada. Não se pode declarar detecção física do negativo só porque a especificação contém a linha correta.

**Correção:** investigar o erro real de formulário e exigir a recusa do campo `valor`, com controle de aceitação proveniente dos Examples literais do mesmo CT. Preservar primeira tradução, logs, JUnit e resultado do mutante sobrevivente; arquivar eventual tradução corrigida em nova etapa e repetir o recorte. Não preencher o CT ausente do K7 com o oráculo M4, nem reclassificar automaticamente a sobrevivência como equivalência. A sessão principal manteve esse diagnóstico como tarefa separada; o revisor não alterou os testes do experimento.

## Correções decididas pela sessão principal

Após a entrega da revisão inicial, a sessão aceitou RI-01/02/03 e delegou sua implementação restrita. Foram alterados:

- feature-test-design: `SKILL.md`, `references/revisao-adversarial.md` e `references/tecnicas-por-regra.md`;
- feature-wiki: `SKILL.md`, `README.md` e somente o comentário inicial de `scripts/guarda-subagente.sh`.

Rotas/modelos Claude ficaram condicionados ao adaptador; os demais hosts usam capacidades e modelo efetivamente disponíveis. Contexto novo, autoria distinta, fechamento principal e declaração de revisão não feita foram preservados. Aninhamento depende de autorização e capacidade. O hook continua com o mesmo algoritmo e agora é descrito por padrões cobertos, sem promessa de isolamento. As duas linhas das técnicas bloqueiam o recorte; a linha da direção voltou à tabela e a nota matemática ficou depois dela.

O implementador dessa correção não alterou versões, CHANGELOG, README raiz, perfis, tratamentos, conjuntos, implementação Laravel ou traduções. Versionamento e reconciliação documental ficaram com a sessão principal. `git diff --check` passou. Os achados iniciais e sua prova foram mantidos acima; a implementação deles não certifica nova eficácia comportamental.

## Verificações realizadas

- Leitura do SKILL/README da feature-test-design, técnicas por regra, template 04, contrato adversarial e resumo; confronto com README/CHANGELOG da coletânea. Varredura das cinco skills limitada aos termos de portabilidade, garantia de cegueira e proibição absoluta de aninhamento. Aliases em blocos explicitamente condicionados ao Claude não foram tratados como defeito.
- Os ZIP arquivados correspondem integralmente aos hashes de `tratamentos/manifest.json` e às entradas de `preparacao.json`: baseline com 64 arquivos e feature-test-design 1.16.0; candidata com 71 arquivos e feature-test-design 1.17.0. Correções 1.17.1/1.17.2 da fonte não estão nesses tratamentos.
- Conferidos os 15 hashes de `instrumentos.json`, incluindo os quatro prompts dos braços e o prompt histórico do juiz. `freeze.py` lê o prompt em `instrumentos-congelados/`, não o prompt v2 do protocolo atual. A fixture confirmou essa origem e a escrita do hash sobre os bytes da cópia anônima.
- Nos dois conjuntos de cupons então congelados, os hashes de 04/05 conferem. `audit_verdict.audit()` aplicado a cópias temporárias dos vereditos brutos confirmou 18 IDs ordenados por juiz, citações literais para DETECTA e 53/47 declarações únicas de cenários. Essa conferência não certifica a discriminação semântica de cada decisão nem inventa resultados dos juízes de aprovação de compra.
- Os hashes anônimos históricos desses dois conjuntos descrevem o texto normalizado para LF, enquanto os arquivos arquivados têm CRLF. As auditorias registram `metadata_describes_bytes: false`, hash real e justificativa; os metadados originais foram preservados. A versão atual do congelador escreve LF e calcula o hash do arquivo efetivamente escrito. O desvio histórico não foi tratado como hash de bytes correto.
- Os seis arquivos de `testes/cuponsv1/sha256.json` conferem byte a byte. Os recortes materializados e seus Examples foram confrontados com os CT correspondentes dos conjuntos completos. M4 preserva os retornos de CT-10/11/12 sem copiar o contador/trilha de K7; a linha fixa negativa vem literalmente de CT-07 M4 e está ausente de CT-08 K7. O contrato global K7 fornece a conservação das linhas anteriores na recusa. Os CT-B estão explicitamente parciais: seleção/unidade no DOM, com gravação omitida. Não se certifica o cenário de gravação por um teste de console.
- Conferidos 41 arquivos arquivados da implementação v1 e 41 da referência v2 contra seus manifestos. `.env.example` consta dos manifestos e foi deliberadamente excluído dos arquivos integrais; esta revisão não o abriu. A v2 altera somente assinatura de Cupom, três chamadores próprios e contrato público. A v1 permanece arquivada e tem seu próprio manifesto, patch e controles.
- O controle inicial M4 falha nas duas linhas CT-41 porque a implementação v1 aceita ator nulo. Isso é falha de negócio no controle, não morte de mutante. A correção v2 retorna à assinatura `User` obrigatória do 00, que prevalece sobre o `?User = null` do plano. O `TypeError` é admitido somente nesse CT de recusa explícita de null; os helpers gerais relançam `Error` e `QueryException`. Erros técnicos restantes exigem triagem, e exit code sozinho não prova detecção.
- O arquivo `execucao-derivada/referenciav2/resultado.json` registra controle real verde da referência corrigida. É validação da implementação, não DDR nem resultado dos testes comparativos. Resultados futuros devem apontar o manifesto da referência v2, sem rebatizar os controles v1.
- `run_mutants.py` preserva controle, logs, JUnit, timeout e restauração byte a byte; exige controle verde, não vazio e com assertion. Não rotula automaticamente falha como mutante morto. A seleção inicial de sete operadores é exploratória, pois nasceu após a derivação; o oitavo, criação fixa negativa, é confirmação posterior aos vereditos de cupons e deve permanecer separado. Não há MSI do catálogo completo.
- `regressoes-coletanea-final.json` e `regressoes-adicionais.json` registram 45 checks e 13 testes auxiliares, respectivamente. A regressão numérica adicional é instrumento novo; 58 checks atuais não são uma repetição dos 57 checks da comparação mecânica anterior. Não derive melhora pela diferença entre essas contagens.

## Checks isolados de scripts

Executados em Python, sem aplicação e com diretórios temporários removidos ao terminar:

1. Self-check de `audit_verdict`: rejeita citação inventada e ID duplicado; aceita citação literal.
2. Self-check de `run_mutants`: timeout conserva stdout/stderr parcial e não vira exit code de detecção.
3. `freeze.main`: utiliza prompt original da fixture, registra hash dos bytes, recusa substituir conjunto congelado e recusa revisão pendente.
4. `archive_verdict.main`: arquiva o veredito bruto byte a byte e relaciona o conjunto congelado.
5. `freeze_translation.main`: conserva exatamente bytes CRLF do teste e registra hash correspondente.
6. `run_mutants.main` com execução mockada: uma exceção durante o mutante restaura os bytes originais e conserva o resultado de controle.
7. `verify_integrity.main` sobre laboratório fictício: aceita arquivos preservados e rejeita implementação alterada.
8. Após a correção de `freeze.py` pela sessão principal: aceita revisão explicitamente CONCLUÍDA com materialização/execução pendentes, preserva a dívida e o hash real; rejeita status de revisão PENDENTE e ausência de fechamento explícito. A fixture anterior de overwrite/prompt/bytes foi executada antes dessa alteração; a nova fixture exercita especificamente o guard corrigido.

As fixtures substituem `ROUND`, `LAB` e `RUNTIME` por pastas temporárias; o subprocesso Pest nunca foi chamado. Os checks acima provam esses invariantes dos scripts, não isolamento de leitura, qualidade da derivação ou mortes reais de mutantes.

Após as correções delegadas, foram executados `python tests/run.py` (45 testes, exit code 0) e `python -m unittest discover -s tests -p 'test_*.py'` (13 testes, exit code 0). Essa descoberta executou também a regressão da expressão percentual via PHP, fora de qualquer aplicação. São 58 verificações atuais; não correspondem ao instrumento anterior de 57. A sessão principal deve repetir os checks se alterar fontes após essa execução.

## Limites desta revisão

As suítes gerais foram repetidas após as correções específicas acima. A sessão principal mantém a obrigação de executar os checks após alterações finais posteriores. Não houve nova execução de aplicação; as chamadas PHP dos checks da coletânea usam expressão numérica ou fixtures.

A rodada continuava produzindo artefatos durante a revisão. A auditoria de conteúdo e hashes acima cobre os arquivos que já estavam arquivados nesse momento. Não certifica quatro vereditos, fechamento final do cenário de aprovação, execuções futuras dos testes derivados, matrizes completas, MSI completo, SMTP, disputa multiprocesso, variância, tokens/custo, equivalência entre hosts ou carregamento nativo de perfis TOML. Não há autorização ou evidência de publicação externa nesta revisão.
