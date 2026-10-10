# Protocolo do Experimento — Eficácia dos CTs gerados pela feature-wiki

> **Instrumento sem versão fixa (2026-09-26).** Este protocolo e o [`PROMPT-BRACO.md`](PROMPT-BRACO.md)
> não fixam versão de skill: cada rodada registra o `metadata.version` de cada skill usada (até a
> release de 2026-09-26 o campo era `version`, no topo do frontmatter). **Medir
> `feature-test-design` ≥ 1.14 com o prompt antigo não mede a 1.14** — o bloco que o
> [`README.md` de `experimentos/`](../README.md) publicava até 2026-09-26 fixava 1.9.0 /
> `feature-wiki` 3.0.0 e não tinha a camada de componente Livewire, a revisão adversarial nem o
> gatilho de Impacto 3.

## Pergunta

Os casos de teste que a `feature-wiki` especifica no `04-casos-de-teste.md` **detectam
defeitos reais**, ou apenas documentam o caminho feliz que o próprio agente imaginou?

## Métrica principal — DDR de especificação

```
DDR = (defeitos do catálogo detectáveis por >= 1 CT) / (total de defeitos do catálogo)
```

Um CT **detecta** o defeito `D` se, e somente se, existe no CT uma assertion explícita
cujo resultado **mudaria** se `D` estivesse presente na implementação.

Não conta como detecção:
- CT que "cobre a área" mas não afirma nada sobre o comportamento defeituoso
- assertion genérica (`assertOk`, `assertSee` de texto estático, `assertDatabaseHas`
  só com a chave) que passa igual com e sem o defeito
- CT que cita o `RQ` relacionado sem exercitar o valor/estado que revela `D`

Isto é **mutation score em nível de especificação**: cada defeito do catálogo é um
mutante plausível, e o CT precisa matá-lo.

## Métricas secundárias

| Métrica | Como medir | Por que importa |
|---|---|---|
| `N_CT` | nº de cenários no `04` + nº de CT-B no `05` (nas rodadas 1 a 4, só o `04`) | custo |
| `DDR / N_CT` | eficiência | evita "escrever 40 CTs" como solução |
| `AMB` | ambiguidades registradas no `00` que estão no catálogo | valor entregue antes do código |
| `TAUT` | CTs sem oráculo falsificável | qualidade de assertion |
| `FALSO_OK` | `RQ` marcado como coberto cujo defeito passa | é a falha que o quality gate não pega hoje |

## Braços

| Braço | Skill |
|---|---|
| **A** — baseline | `feature-wiki` v2.10.0, sem alteração |
| **B** — candidata | `feature-wiki` + técnica nova de derivação de CT |

Mesmo requisito, mesmo projeto, agentes independentes, sem contexto compartilhado.

**Rodada de regressão entre versões** (a partir de 2026-09-26): A = tag de partida, B = tag de
chegada. Mesmo kit, mesmo oráculo (inclusive o `02`, se a série o congelou), o mesmo
`PROMPT-BRACO.md` (mesmo commit) e o mesmo juiz — mesmo prompt **e** mesmo modelo. As duas pontas
rodam com o prompt atual: medir a partida com um prompt e a chegada com outro muda duas variáveis.

**Sem regressão** quer dizer, em cada cenário: detectados de B ≥ detectados de A; nenhum defeito
que A detectou vira NÃO DETECTA em B; nenhuma lacuna cega nova. O total igual não basta — entre as
rodadas 6 e 7 o total ficou em 33 de 36 e o cenário 1 perdeu dois defeitos para ganhar um.

## Cegamento

O agente **juiz** recebe apenas: catálogo de defeitos + arquivo `04` gerado, concatenado com o
`05` se houver.
Não recebe o requisito, não sabe qual braço gerou o arquivo, e não participou da geração.

O **braço** trabalha no projeto-cobaia, onde esta pasta `experimentos/` não existe: não vê
catálogo, veredito, relatório nem pista derivada deles no prompt. O projeto-cobaia também não tem
pastas `exp-*` nem `tests/Feature/Exp*` de outras rodadas: elas são apagadas antes de cada braço,
não só proibidas no prompt.

**Antes do juiz**, o conjunto é conferido contra o catálogo
(`grep -nE '\b[DE](0[1-9]|1[0-8])\b'` no `04` e no `05`). ID ou descrição do catálogo no conjunto
anula o braço — o juiz não detecta contaminação (rodada 8).

## Registro obrigatório de cada rodada

No cabeçalho do `vereditos.md` da rodada:

- data; tag ou commit de cada skill e o `metadata.version` que cada braço devolveu;
- host e modelo de cada braço; modelo do juiz;
- commit do `protocolo/` usado (prompt do braço e do juiz);
- versões do kit (Laravel, Filament, Pest) e se o oráculo tinha `02`;
- perfil imposto, se houver.

Na pasta da rodada: `conjuntos/` com o `04` e o `05` **inteiros**, como o juiz os recebeu — resumo
não é conjunto; e `vereditos.md` com a tabela do `PROMPT-JUIZ-CEGO.md`, uma linha por defeito, com
citação literal. Placar sem essa tabela, ou com o conjunto julgado fora do repositório, entra no
[`README.md` de `experimentos/`](../README.md) como relato, marcado — não como medição.

## Regra de parada do loop

Iterar A → medir → melhorar → B → medir enquanto houver ganho. Encerrar quando:
1. `DDR >= 0,85` em dois cenários distintos, **e**
2. `N_CT` não mais que dobrou em relação ao baseline, **e**
3. o ciclo não produzir achado novo de melhoria.
