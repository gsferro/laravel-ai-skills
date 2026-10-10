# Prompt do braço (agente executor)

> **Fonte única do prompt do braço.** O [`README.md` de `experimentos/`](../README.md) aponta para
> cá e não mantém cópia. O prompt não fixa versão de skill: a versão medida é a instalada no
> projeto-cobaia, e o braço devolve o `metadata.version` de cada `SKILL.md` que leu (até a release
> de 2026-09-26 o campo era `version`, no topo do frontmatter). **Medir `feature-test-design` ≥
> 1.14 com o prompt antigo** — o bloco que o `README.md` de `experimentos/` trazia até 2026-09-26,
> fixado em 1.9.0 / `feature-wiki` 3.0.0, sem camada Livewire, sem revisão adversarial e sem o
> gatilho de Impacto 3 — **não mede a 1.14.**

Um agente por cenário, **sem contexto compartilhado** entre eles e sem contexto de quem conduz a
rodada. Reusar literalmente, trocando só os marcadores abaixo.

O braço **não** recebe o catálogo de defeitos, **não** recebe as métricas das rodadas anteriores e
**não** pode ler os conjuntos de nenhuma rodada anterior — nem as wikis (`exp-*`), nem as
materializações em Pest (`tests/Feature/Exp*`). Também não recebe pista derivada deles: tamanho da
matriz, lista de lacunas a declarar, valor discriminante, premissa já decidida em rodada anterior.
Pista no prompt é métrica de rodada anterior com outro nome.

| Marcador | O que é |
|---|---|
| `{PROJETO}` | caminho do projeto-cobaia da rodada, com as skills da tag medida em `.ai/skills/` |
| `{PASTA_ORACULO}` | a pasta `exp-*` com o oráculo copiado de `protocolo/oraculo-fixo/{cenario}/` |
| `{FEATURE}` | `cupons-de-desconto` (cenário 1) ou `aprovacao-de-compra` (cenário 2) |
| `{PASTA_SAIDA}` | pasta `exp-*` nova, só deste braço |
| `{PERFIL}` | `o que o passo 0 da skill decidir` — ou o perfil que a rodada impõe (ex.: `mínimo em todas as áreas`, na rodada do perfil mínimo) |

---

## Prompt

> Você vai executar a derivação de casos de teste de uma feature em um projeto Laravel real.
> Trabalhe integralmente em `{PROJETO}` (Laravel 13 + Filament 5 + Pest 5 com browser plugin e
> mutate plugin).
>
> ## O que fazer
>
> 1. Leia `{PROJETO}\.ai\skills\feature-wiki\SKILL.md` inteira. Ela é a skill principal do fluxo.
>    Anote o `metadata.version` do frontmatter dela (se não houver, o campo `version`). Quando uma
>    skill mandar abrir um arquivo de `references/`, abra; não leia a pasta inteira por conta
>    própria — a rodada mede a skill do jeito que ela está empacotada.
> 2. Os arquivos `00-requisito.md` e `01-plano-acao.md` da feature **já existem e são imutáveis** —
>    estão em `{PROJETO}\wikis\specs\{PASTA_ORACULO}\{FEATURE}\`. Leia os dois. Se a mesma pasta
>    tiver `02-decisoes-arquiteturais.md`, ele também é imutável e entra só pela seção
>    `## Superfície Livewire`; se não tiver, **não o crie** e diga no retorno que ele faltou. Você
>    entra no fluxo da `feature-wiki` no step que cria os arquivos `04-casos-de-teste.md` e
>    `05-casos-de-teste-browser.md` (o step 4, até a `feature-wiki` 3.6.0).
> 3. Conforme esse step manda, **invoque a skill `feature-test-design`**
>    (`{PROJETO}\.ai\skills\feature-test-design\SKILL.md`): leia-a inteira, anote o
>    `metadata.version` e **execute o passo 0 e, em cada área, os passos que o perfil dela manda
>    (tabela do passo 0), sem pular nenhum deles**, incluindo o gate de falsificabilidade. Os
>    cenários derivam do `00-requisito.md`; o `01-plano-acao.md` entra só para paths, rotas e a
>    tabela `## Superfície de UI`. Em especial:
>    - **Perfil de esforço (passo 0)**: {PERFIL}. Pontue P×I por área e declare o perfil de cada
>      área no cabeçalho do `04`. Perfil imposto pela rodada é declarado ali como imposto.
>    - **Camada**: onde a skill mandar alocar camada (passo 7 e checklist), a camada mais barata
>      que prova, com o **componente Livewire/Filament** entre `Feature` e `Browser`; e o cenário
>      por fora da UI que a skill exige em toda regra de autorização e de validação.
>    - **Revisão adversarial**: obrigatória se qualquer área tiver perfil **completo** ou
>      **Impacto 3**. Quem despacha é você — a sessão principal —, para um sub-agente que não
>      derivou os cenários: no Claude Code, `fw-adversario-ct` se ele estiver em
>      `{PROJETO}\.claude\agents\`, senão `general-purpose` com `model: opus`. Ele recebe **só** o
>      `00` e o `04` (e o `05`, se houver). Feche os achados como a skill manda. Host sem
>      sub-agente: **não autorrevise** — declare no cabeçalho do `04`
>      `Revisão adversarial: NÃO FEITA — host sem sub-agente`.
>    - Onde a skill mandar registrar algo no `03-progresso.md` (despachos, degradações), registre
>      no retorno. **Não crie o `03`.**
> 4. Escreva a saída em **`{PROJETO}\wikis\specs\{PASTA_SAIDA}\{FEATURE}\04-casos-de-teste.md`** e,
>    se o gate do `05` exigir, em `05-casos-de-teste-browser.md` na mesma pasta. Crie a pasta.
>
> ## Regras duras
>
> - **Não leia nenhuma outra pasta `exp-*`** nem qualquer `04-casos-de-teste.md` /
>   `05-casos-de-teste-browser.md` fora da sua. Eles contêm conjuntos de execuções anteriores desta
>   mesma feature e olhá-los invalida a medição. A única pasta `exp-*` que você pode ler é
>   `{PASTA_ORACULO}`, e dela **somente** o `00-requisito.md`, o `01-plano-acao.md` e, se existir, o
>   `02-decisoes-arquiteturais.md`. O mesmo vale para `tests/Feature/Exp*`, que são
>   materializações de conjuntos anteriores.
> - **Não leia catálogo de defeitos, veredito ou relatório de rodada**, em lugar nenhum.
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
> Resumo curto (máx. 30 linhas). O conteúdo do arquivo é a entrega — não repita os cenários.
>
> - o `metadata.version` de cada skill que você leu, e o host e o modelo desta sessão;
> - o perfil de cada área, se ele foi decidido pelo passo 0 ou imposto, e se alguma área tem
>   Impacto 3;
> - nº de regras mapeadas, nº de cenários no `04`, nº de CT-B no `05`;
> - revisão adversarial: rodou ou não, e por quê; rota e modelo do sub-agente; quantos achados em
>   cada rodada, quantas rodadas, e no que virou cada achado (cenário novo, oráculo reescrito ou
>   lacuna declarada);
> - os arquivos de `references/` que você abriu;
> - `02` presente ou ausente no oráculo; desvios e degradações declarados;
> - os paths escritos.

---

## Por que o braço entra no step 4, e não no step 0

O `00-requisito.md` é o **oráculo fixo** do experimento: ele foi escrito uma vez, no baseline, e
não muda mais. Deixar cada braço capturar o requisito de novo introduziria uma segunda variável —
a qualidade da decomposição em `RQ` e das premissas — e a rodada deixaria de medir a técnica de
derivação isoladamente.

O `01-plano-acao.md` entra pelo mesmo motivo, e é lido só para paths, rotas e superfície de UI —
a fronteira que a própria skill impõe.

O `02-decisoes-arquiteturais.md` segue a mesma lógica. A `feature-test-design` ≥ 1.12 exige a
`## Superfície Livewire` dele quando a feature cria página, widget ou componente — e os dois
cenários criam. O oráculo congelado em agosto não tem `02`. Deixar o braço escrevê-lo faria a
superfície inventariada variar de braço para braço. Por isso o `02` é congelado **uma vez** em
`protocolo/oraculo-fixo/{cenario}/`, antes de uma série de rodadas, e usado por todos os braços
da série — ou fica ausente em todos, e o retorno registra a ausência.
