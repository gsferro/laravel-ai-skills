# Protocolo do Experimento — Eficácia dos CTs gerados pela feature-wiki

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
| `N_CT` | nº de casos no `04` | custo |
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

## Cegamento

O agente **juiz** recebe apenas: catálogo de defeitos + arquivo `04` gerado.
Não recebe o requisito, não sabe qual braço gerou o arquivo, e não participou da geração.

## Regra de parada do loop

Iterar A → medir → melhorar → B → medir enquanto houver ganho. Encerrar quando:
1. `DDR >= 0,85` em dois cenários distintos, **e**
2. `N_CT` não mais que dobrou em relação ao baseline, **e**
3. o ciclo não produzir achado novo de melhoria.
