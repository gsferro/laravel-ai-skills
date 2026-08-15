# Prompt do braço (agente executor)

Um agente por cenário, **sem contexto compartilhado** entre eles e sem contexto de quem conduz a
rodada. Reusar literalmente, trocando só o nome da feature, o caminho do projeto-cobaia da rodada
e a pasta `exp-*` de saída.

O braço **não** recebe o catálogo de defeitos, **não** recebe as métricas das rodadas anteriores e
**não** pode ler os conjuntos de nenhuma rodada anterior — nem as wikis (`exp-*`), nem as
materializações em Pest (`tests/Feature/Exp*`).

---

## Prompt

> Você vai executar a derivação de casos de teste de uma feature em um projeto Laravel real.
> Trabalhe integralmente em `{PROJETO}` (Laravel 13 + Filament 5 + Pest 5 com browser plugin e
> mutate plugin).
>
> ## O que fazer
>
> 1. Leia `{PROJETO}\.ai\skills\feature-wiki\SKILL.md` inteira. Ela é a skill principal do fluxo.
> 2. Os arquivos `00-requisito.md` e `01-plano-acao.md` da feature **já existem e são imutáveis** —
>    estão em `{PROJETO}\wikis\specs\{PASTA_ORACULO}\{FEATURE}\`. Leia os dois. Você entra no fluxo
>    da `feature-wiki` no **step 4**, na parte que cria os arquivos `04-casos-de-teste.md` e
>    `05-casos-de-teste-browser.md`.
> 3. Conforme o step 4 manda, **invoque a skill `feature-test-design`**
>    (`{PROJETO}\.ai\skills\feature-test-design\SKILL.md`): leia-a inteira e **execute o pipeline
>    dela do passo 0 ao passo 7, sem pular nenhum**, incluindo o gate de falsificabilidade (passo 6)
>    e a **revisão adversarial** quando o perfil exigir.  Os cenários derivam do `00-requisito.md`;
>    o `01-plano-acao.md` entra só para paths, rotas e a tabela `## Superfície de UI`.
> 4. Escreva a saída em **`{PROJETO}\wikis\specs\{PASTA_SAIDA}\{FEATURE}\04-casos-de-teste.md`** e,
>    se o gate do `05` exigir, em `05-casos-de-teste-browser.md` na mesma pasta. Crie a pasta.
>
> ## Regras duras
>
> - **Não leia nenhuma outra pasta `exp-*`** nem qualquer `04-casos-de-teste.md` /
>   `05-casos-de-teste-browser.md` fora da sua. Eles contêm conjuntos de execuções anteriores desta
>   mesma feature e olhá-los invalida a medição. A única pasta `exp-*` que você pode ler é
>   `{PASTA_ORACULO}`, e dela **somente** o `00-requisito.md` e o `01-plano-acao.md`. O mesmo vale
>   para `tests/Feature/Exp*`, que são materializações de conjuntos anteriores.
> - Pode e deve ler o restante do projeto (`app/`, `database/`, `tests/`, `config/`, as wikis de
>   convenção em `wikis/*.md`, as regras em `.ai/rules/`) — as wikis de features de produção em
>   `wikis/specs/main/` e `wikis/specs/feature/` são leitura permitida.
> - **Não implemente nada.** Nenhuma migration, model, service, resource ou teste Pest. A entrega é
>   a especificação.
> - Não altere nenhum arquivo fora da sua pasta de saída.
> - Não pergunte nada ao usuário: ele não está disponível. Onde a skill mandar perguntar, siga o
>   procedimento de premissa registrada que a própria skill define. O `00-requisito.md` já traz as
>   premissas assumidas — respeite-as como dadas.
>
> ## Retorno
>
> Resumo curto (máx. 25 linhas): perfil de esforço escolhido, nº de regras mapeadas, nº de cenários
> no `04`, nº de CT-B no `05`, se a revisão adversarial rodou e o que ela achou, e os paths
> escritos. O conteúdo do arquivo é a entrega — não repita os cenários no retorno.

---

## Por que o braço entra no step 4, e não no step 0

O `00-requisito.md` é o **oráculo fixo** do experimento: ele foi escrito uma vez, no baseline, e
não muda mais. Deixar cada braço capturar o requisito de novo introduziria uma segunda variável —
a qualidade da decomposição em `RQ` e das premissas — e a rodada deixaria de medir a técnica de
derivação isoladamente.

O `01-plano-acao.md` entra pelo mesmo motivo, e é lido só para paths, rotas e superfície de UI —
a fronteira que a própria skill impõe.
