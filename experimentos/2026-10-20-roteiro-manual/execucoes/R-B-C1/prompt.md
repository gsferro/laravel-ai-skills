Você vai executar a derivação de casos de teste de uma feature em um projeto Laravel real.
Trabalhe integralmente em `D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d` (Laravel 13 + Filament 5 + Pest 5 com browser plugin e
mutate plugin).

## O que fazer

1. Leia `D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d\.ai\skills\feature-wiki\SKILL.md` inteira. Ela é a skill principal do fluxo.
   Anote o `metadata.version` do frontmatter dela (se não houver, o campo `version`). Quando uma
   skill mandar abrir um arquivo de `references/`, abra; não leia a pasta inteira por conta
   própria — a rodada mede a skill do jeito que ela está empacotada.
2. Os arquivos `00-requisito.md` e `01-plano-acao.md` da feature **já existem e são imutáveis** —
   estão em `D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d\wikis\specs\oraculo\cupons-de-desconto\`. Leia os dois. Se a mesma pasta
   tiver `02-decisoes-arquiteturais.md`, ele também é imutável e entra só pela seção
   `## Superfície Livewire`; se não tiver, **não o crie** e diga no retorno que ele faltou. Você
   entra no fluxo da `feature-wiki` no step que cria os arquivos `04-casos-de-teste.md` e
   `05-casos-de-teste-browser.md` (o step 4, até a `feature-wiki` 3.6.0).
3. Conforme esse step manda, **invoque a skill `feature-test-design`**
   (`D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d\.ai\skills\feature-test-design\SKILL.md`): leia-a inteira, anote o
   `metadata.version` e **execute o passo 0 e, em cada área, os passos que o perfil dela manda
   (tabela do passo 0), sem pular nenhum deles**, incluindo o gate de falsificabilidade. Os
   cenários derivam do `00-requisito.md`; o `01-plano-acao.md` entra só para paths, rotas e a
   tabela `## Superfície de UI`. Em especial:
   - **Perfil de esforço (passo 0)**: o que o passo 0 da skill decidir. Pontue P×I por área e declare o perfil de cada
     área no cabeçalho do `04`. Perfil imposto pela rodada é declarado ali como imposto.
   - **Camada**: onde a skill mandar alocar camada (passo 7 e checklist), a camada mais barata
     que prova, com o **componente Livewire/Filament** entre `Feature` e `Browser`; e o cenário
     por fora da UI que a skill exige em toda regra de autorização e de validação.
   - **Revisão adversarial**: obrigatória se qualquer área tiver perfil **completo** ou
     **Impacto 3**. Quem despacha é você — a sessão principal —, para um sub-agente que não
     derivou os cenários: no Claude Code, `fw-adversario-ct` se ele estiver em
     `D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d\.claude\agents\`, senão `general-purpose` com `model: opus`. Ele recebe **só** o
     `00` e o `04` (e o `05`, se houver). Feche os achados como a skill manda. Host sem
     sub-agente: **não autorrevise** — declare no cabeçalho do `04`
     `Revisão adversarial: NÃO FEITA — host sem sub-agente`.
   - Onde a skill mandar registrar algo no `03-progresso.md` (despachos, degradações), registre
     no retorno. **Não crie o `03`.**
4. Escreva a saída em **`D:\PROJECTS\SKILLS\blind-20261020\proj-05b17d\wikis\specs\saida-c1\cupons-de-desconto\04-casos-de-teste.md`** e,
   se o gate do `05` exigir, em `05-casos-de-teste-browser.md` na mesma pasta. Crie a pasta.

## Regras duras

- **Não leia nenhuma outra pasta `exp-*`** nem qualquer `04-casos-de-teste.md` /
  `05-casos-de-teste-browser.md` fora da sua. Eles contêm conjuntos de execuções anteriores desta
  mesma feature e olhá-los invalida a medição. A única pasta `exp-*` que você pode ler é
  `oraculo`, e dela **somente** o `00-requisito.md`, o `01-plano-acao.md` e, se existir, o
  `02-decisoes-arquiteturais.md`. O mesmo vale para `tests/Feature/Exp*`, que são
  materializações de conjuntos anteriores.
- **Não leia catálogo de defeitos, veredito ou relatório de rodada**, em lugar nenhum.
- Pode e deve ler o restante do projeto (`app/`, `database/`, `tests/`, `config/`, as wikis de
  convenção em `wikis/*.md`, as regras em `.ai/rules/`) — as wikis de features de produção em
  `wikis/specs/main/` e `wikis/specs/feature/` são leitura permitida.
- **Não implemente nada.** Nenhuma migration, model, service, resource ou teste Pest. A entrega é
  a especificação.
- Não altere nenhum arquivo fora da sua pasta de saída.
- Não pergunte nada ao usuário: ele não está disponível. Onde a skill mandar perguntar, siga o
  procedimento de premissa registrada que a própria skill define. O `00-requisito.md` já traz as
  premissas assumidas — respeite-as como dadas.

## Retorno

Resumo curto (máx. 30 linhas). O conteúdo do arquivo é a entrega — não repita os cenários.

- o `metadata.version` de cada skill que você leu, e o host e o modelo desta sessão;
- o perfil de cada área, se ele foi decidido pelo passo 0 ou imposto, e se alguma área tem
  Impacto 3;
- nº de regras mapeadas, nº de cenários no `04`, nº de CT-B no `05`;
- revisão adversarial: rodou ou não, e por quê; rota e modelo do sub-agente; quantos achados em
  cada rodada, quantas rodadas, e no que virou cada achado (cenário novo, oráculo reescrito ou
  lacuna declarada);
- os arquivos de `references/` que você abriu;
- `02` presente ou ausente no oráculo; desvios e degradações declarados;
- os paths escritos.