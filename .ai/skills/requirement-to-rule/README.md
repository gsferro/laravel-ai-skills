# requirement-to-rule — Decisão da Wiki Vira Regra Durável

> **Skill**: [`SKILL.md`](SKILL.md) · versão **1.3.0** · licença MIT
> Este README fala com a **pessoa**: por que a skill existe, quando usar, o que ela não faz e do que depende. O procedimento que o agente segue (gates, escada de enforcement, índice, modelo da rule, fallback) vive só no `SKILL.md`. Aqui há ponteiros para ele, não cópia.

## Índice

- [Por que existe](#por-que-existe)
- [Quando usar](#quando-usar)
- [Quando não usar](#quando-não-usar)
- [O que ela entrega e onde está o procedimento](#o-que-ela-entrega-e-onde-está-o-procedimento)
- [Limites](#limites)
- [Dependências](#dependências)

---

## Por que existe

**A wiki tem memória, o agente não.** Uma decisão registrada em `02-decisoes-arquiteturais.md` só é lida por quem abrir **aquela** wiki. Na feature seguinte, em outra sessão, o agente não sabe que a decisão existe e repete o erro que a ADR já resolveu.

Uma decisão pode morar em três lugares, e cada um tem outro leitor:

| Camada | Onde fica | Quem lê, e quando | Serve para |
|---|---|---|---|
| **Wiki da feature** | `02-decisoes-arquiteturais.md`, Notas de Implementação do `03` | quem abrir aquela pasta, durante aquela feature | o porquê de uma decisão, com contexto e alternativas |
| **Project Rule** | `.ai/rules/*.md`, escopada por glob de path | todo agente que lê `.ai/rules/`, em qualquer sessão, antes de planejar ou editar arquivo que casa o glob | restrição da **sua aplicação** que atravessa features |
| **Guideline do Boost** | `.ai/guidelines/` e o próprio pacote do Boost | todo agente, carregada no início da sessão | como escrever **Laravel**: o ecossistema, que o Boost mantém atualizado |

A skill leva da primeira camada para a segunda só o que merece, e impede que a segunda vire cópia da terceira. O critério de cada fronteira está no `SKILL.md`, em [As três camadas](SKILL.md#as-três-camadas--não-confundir) e [Os 4 Gates](SKILL.md#os-4-gates).

Um exemplo do que o Boost chama de rule, *"anything you would otherwise need to explain again in every new session"*: o padrão de log `[Classe@Método]` com channel por feature é reescrito em **toda** wiki desde a v1 da `feature-wiki`. É explicação repetida a cada sessão. Como rule, seria escrita uma vez.

## Quando usar

- **Ao fechar uma feature com a [`feature-wiki`](../feature-wiki/README.md).** O step 9 dela procura candidatos a rule na wiki e, com a sua aprovação, invoca esta skill.
- **Quando você pedir.** "Isso vira rule" ou "lembre disso para sempre" disparam a skill fora da `feature-wiki`, a partir de um card, um ticket ou da conversa.
- **Quando uma decisão ou armadilha vale além da feature.** Uma ADR aceita cuja consequência vale para código futuro, ou uma armadilha em que outro agente cairia.

A lista que o agente segue está em [Quando Invocar](SKILL.md#quando-invocar).

## Quando não usar

| Situação | O lugar certo |
|---|---|
| Decisão que só vale para a feature atual | ADR na wiki da feature |
| Como Laravel, Livewire ou Pest funcionam | guideline do Boost |
| Estilo de código, imports, tipagem | Pint, Rector, PHPStan |
| Convenções do código que já existe | skill `infer-conventions` do Boost |
| Preferência sua, de uma sessão | memória do agente |

O critério que o agente aplica está em [Quando NÃO Invocar](SKILL.md#quando-não-invocar).

O `infer-conventions` e esta skill andam em sentidos opostos e se completam:

| | `infer-conventions` (Boost) | `requirement-to-rule` (esta coletânea) |
|---|---|---|
| Direção | **código existente** → rules | **requisito/decisão** → rules |
| Quando rodar | uma vez, ao adotar o Boost num projeto legado | continuamente, a cada feature concluída |
| O que documenta | o que o código **faz** hoje | o que foi **decidido** que o código fará |

Ordem recomendada: rodar `infer-conventions` uma vez para bootstrapar a base, e usar `requirement-to-rule` como incremento a partir daí.

## O que ela entrega e onde está o procedimento

| Você recebe | Procedimento no `SKILL.md` |
|---|---|
| Candidatos com origem e evidência, tirados da wiki ou do requisito | [1. Coletar candidatos](SKILL.md#1-coletar-candidatos) |
| Diagnóstico do que já existe em `.ai/rules/` | [2. Verificar o estado atual das rules](SKILL.md#2-verificar-o-estado-atual-das-rules) |
| Cada candidato julgado nos gates, inclusive os descartados | [Os 4 Gates](SKILL.md#os-4-gates) e [3. Aplicar os 4 gates](SKILL.md#3-aplicar-os-4-gates) |
| Automação no lugar de prosa, quando a máquina alcança | [4. Preferir enforcement automático](SKILL.md#4-preferir-enforcement-automático-escada-de-rules) |
| Uma apresentação para você decidir o que grava | [5. Apresentar ao usuário](SKILL.md#5-apresentar-ao-usuário-e-esperar-decisão) |
| A rule gravada pelo Boost | [6. Gravar via `record-rule`](SKILL.md#6-gravar-via-record-rule-obrigatório) e [Modelo Base do Conteúdo da Rule](SKILL.md#modelo-base-do-conteúdo-da-rule) |
| O índice `.ai/rules/index.md` conferido | [7. Garantir o índice](SKILL.md#7-garantir-o-índice-airulesindexmd) e [Índice de Rules](SKILL.md#índice-de-rules-airulesindexmd) |
| Um commit de `.ai/rules/` | [8. Verificar e commitar](SKILL.md#8-verificar-e-commitar) |
| Caminho para projeto sem Boost, com rules desativadas ou em agente sem MCP | [Fallback](SKILL.md#fallback--boost-ausente-ou-rules-desativadas) |

O que a skill evita está em [Anti-padrões](SKILL.md#anti-padrões); a conferência de saída, em [Checklist Final](SKILL.md#checklist-final).

## Limites

O que a skill **não** faz:

- **Não poda rules.** O único gatilho de revisão é fraco: no passo 1, uma rule que aparece seguidas vezes como `violada` ou `n.a.` na tabela `## Conformidade com Rules` do `03` volta como candidato ([1. Coletar candidatos](SKILL.md#1-coletar-candidatos)). Não há procedimento de remoção, expiração nem dono. O Boost também não oferece tool nem comando de remoção; a única tool é `record-rule`, que grava. Apagar o arquivo da rule fica fora da skill, que só trata das linhas do índice quando uma rule some ([Regras de manutenção do índice](SKILL.md#regras-de-manutenção-do-índice)). Com o tempo, o número de rules tende a crescer.
- **Não prova o enforcement que sugere.** A escada aponta para teste de arquitetura `arch()` do Pest, PHPStan, Rector ou Pint, mas a skill não roda a suíte para mostrar que a verificação pega a violação.
- **O gate 4 depende de MCP.** Ele usa a tool `search-docs` do Boost. Em agente ou sub-agente sem MCP essa verificação não acontece, e o `SKILL.md` não declara alternativa. É o caso da rota `analista` da `feature-wiki`, que julga os gates do step 9 sem MCP.
- **Com a `feature-wiki`, a aprovação é pedida duas vezes.** O step 9 dela já coleta, aplica os gates e pergunta; esta skill coleta de novo, reaplica os gates e pergunta outra vez no passo 5.
- **Só alcança agentes que leem `.ai/rules/`.** Os demais só veem a rule se houver espelho no formato deles (ver [Fallback](SKILL.md#fallback--boost-ausente-ou-rules-desativadas)).
- **Ainda sem execução medida.** Os exemplos vêm da doc do Boost ou são hipotéticos; a skill não tem rodada no protocolo de [`experimentos/`](https://github.com/gsferro/laravel-ai-skills/blob/main/experimentos/README.md).

## Dependências

| Dependência | Versão mínima | Para quê |
|---|---|---|
| `laravel/boost` | **2.4.12** | Project Rules e a tool MCP `record-rule` surgiram nessa versão ([CHANGELOG do laravel/boost](https://github.com/laravel/boost/blob/main/CHANGELOG.md), PR #852); a tool `search-docs` do gate 4 vem no mesmo pacote |
| Agente com MCP | — | `record-rule` e `search-docs` são tools MCP. Sem MCP, a gravação cai no [Fallback](SKILL.md#fallback--boost-ausente-ou-rules-desativadas) e o gate 4 não é verificado (ver [Limites](#limites)) |
| [`feature-wiki`](../feature-wiki/README.md) | 3.1.0, opcional | só quando os candidatos vêm da wiki: o step 9 invoca esta skill desde a 2.10.0, e a tabela `## Conformidade com Rules` do `03` existe desde a 3.1.0 |
| [`feature-test-design`](../feature-test-design/README.md) | qualquer, opcional | o checklist de taxonomia do `04` é fonte de candidato |

```bash
composer require laravel/boost --dev
php artisan boost:install
```

- Doc do Boost, Project Rules: https://laravel.com/framework/docs/13.x/boost#project-rules
- `BOOST_RULES_ENABLED=false` no `.env` remove a tool `record-rule` e tira `.ai/rules/` da gestão do Boost; a skill passa ao [Fallback](SKILL.md#fallback--boost-ausente-ou-rules-desativadas).
- Skills que conversam com esta (Ponytail, `pest-testing` do Boost, `infer-conventions`) estão em [Skills Companheiras](SKILL.md#skills-companheiras); nenhuma é obrigatória.
