# Pré-registro — roteiro de teste manual opcional (2026-10-20)

Escrito **antes** de qualquer braço rodar. Critérios, células e regras de decisão não mudam
depois de ver resultado; desvio entra no relatório como desvio.

## Tratamentos

| Braço | Conteúdo de `.ai/skills/` | Identificação |
|---|---|---|
| **A** | `git archive 27f89eb .ai/skills` — feature-wiki 4.1.1, feature-test-design 1.17.3, feature-quality-gate 1.8.0 | commit |
| **B** | working tree não commitada sobre `27f89eb`, congelada depois da revisão independente — feature-wiki 4.2.0, feature-test-design 1.17.4, feature-quality-gate 1.9.0 | ZIP + sha256 por arquivo em `tratamentos/manifest.json` |

A diferença que alcança a derivação de CT é só de texto: o corpo da `feature-test-design` é
idêntico entre A e B (muda apenas `metadata.version`); a `feature-wiki` ganha a pergunta do step 4,
a etapa do roteiro entre os steps 10 e 11, itens de checklist e a reference nova.

## Parte R — regressão do `04` (protocolo existente, sem mudança de instrumento)

- Cenários 1 (cupons) e 2 (aprovação), oráculo `protocolo/oraculo-fixo/` (sem `02`, como em todas
  as séries até aqui), `PROMPT-BRACO.md` literal, perfil `o que o passo 0 da skill decidir`.
- Juiz: `PROMPT-JUIZ-CEGO.md` versão 2, hash registrado, mesmo modelo e esforço nos quatro.
  Conjunto anonimizado (versões e paths redigidos) + catálogo do cenário, e nada mais na pasta.
- **Sem regressão**, por cenário (critério do `PROTOCOLO.md`): detectados B ≥ detectados A;
  nenhum defeito detectado por A vira NÃO DETECTA em B; nenhuma lacuna cega nova em B.
- Uma geração por célula. A rodada de 2026-10-09 mostrou variação de juiz em E06/E08/E12:
  reprovação estrita é registrada como reprovação. Para cada defeito perdido, o relatório
  examina se a causa toca texto alterado (step 4, etapa do roteiro, checklist) ou não; sem esse
  vínculo, o resultado é "regressão não descartada, sem mecanismo identificado", nunca "ruído"
  declarado como prova. Não haverá réplica pós-hoc para virar o resultado.

## Parte P — pergunta do roteiro manual no step 4 (instrumento novo)

Prompt: [`instrumentos/PROMPT-BRACO-STEP4.md`](instrumentos/PROMPT-BRACO-STEP4.md). O braço executa
os steps 0 a 4 da `feature-wiki` a partir do texto bruto do card e para antes do step 5. O
desenvolvedor não está disponível: toda pergunta dirigida a ele vai para o retorno, e a sessão
segue o que a skill manda sem resposta. **O prompt não menciona roteiro manual**, exceto nas
células com instrução explícita do desenvolvedor, onde a frase entra como instrução dele.

| Célula | Braço | Card | Instrução do desenvolvedor | Esperado |
|---|---|---|---|---|
| P1 | B | cenário 1 (cupons — painel, permissões) | nenhuma | pergunta presente, `➡️ sim` |
| P2 | B | cenário 2 (aprovação — telas, aprovação humana, e-mail) | nenhuma | pergunta presente, `➡️ sim` |
| P3 | B | cenário 3 (padrões de PII configuráveis — interno, sem tela) | nenhuma | pergunta presente, `➡️ não` |
| P4 | B | cenário 1 | "gere também o roteiro de teste manual" | sem pergunta; decisão `sim`, fonte = instrução |
| P5 | B | cenário 2 | "não quero roteiro de teste manual nesta feature" | sem pergunta; decisão `não`, fonte = instrução, apesar dos sinais |
| P1-A | A | cenário 1 | nenhuma | controle descritivo |
| P2-A | A | cenário 2 | nenhuma | controle descritivo |

Critérios por célula B (todos obrigatórios; conferência mecânica + leitura do auditor):

1. **Pergunta**: P1–P3 — existe pergunta ao desenvolvedor sobre o roteiro manual, na raia
   desenho, com a recomendação esperada e o sinal que a justifica. P4–P5 — nenhuma pergunta sobre
   roteiro manual.
2. **Registro**: o `03` contém exatamente uma linha de decisão que casa
   `^\s*(?:-\s+)?Roteiro manual\s*:\s*(sim|não)` com data, quem/fonte e sinal/motivo.
   P1–P3 (sem resposta): `não`, com a ausência de resposta como fonte. P4: `sim`. P5: `não`.
3. **Raia**: nenhuma menção a roteiro manual em `## Perguntas ao Solicitante` do `00`; o `00`
   não ganha RQ nem premissa sobre o roteiro.
4. **Momento**: nenhum `08-roteiro-teste-manual.md`, `04` ou `05` criado; nada além do step 4.
5. **Script**: `roteiro-manual.sh` sobre a wiki — exit 0 em P1, P2, P3, P5; exit 1 com a linha
   "sim, mas 08 … não existe" em P4 (estado esperado antes da etapa do roteiro).

Controles A: descrevem nº de perguntas por raia e presença espontânea de algo equivalente ao
roteiro. Não têm critério de aprovação e não sustentam afirmação causal (N = 1).

**Decisão da Parte P**: aprovada só se as cinco células B cumprirem os cinco critérios. Célula
reprovada: a causa é corrigida no texto da skill, a célula é reexecutada **uma vez** com o
tratamento corrigido, rotulada `B'`, e o relatório mantém a reprovação de B. B' não retroage para
a Parte R se o texto alterado tocar algo que a derivação lê; nesse caso a Parte R fica declarada
como medição de B, não de B'.

## Execução e isolamento

- Host: Codex CLI 0.162.1, `codex exec --dangerously-bypass-approvals-and-sandbox`, modelo e
  esforço registrados por execução; `multi_agent` habilitado (sub-agente para revisão adversarial).
- Uma cópia descartável do kit `demo-r8` por braço, sem `vendor/`, `node_modules/`, `.git`,
  `.env` de origem, `storage`, configurações de agente, wikis `exp-*` e testes `Exp*` (mesma regra
  de `2026-10-09-projeto-real/prepare.py`). Nenhuma cópia contém `experimentos/`.
- Filesystem **não** isolado tecnicamente: o braço com `--yolo` poderia ler qualquer caminho. Os
  controles são procedimentais (cópia, prompt, contexto novo). Depois de cada braço, o log do
  Codex é varrido por leitura de caminhos fora da cópia; achado anula a célula.
- Antes do juiz, o conjunto é varrido por IDs do catálogo (`\b[DE](0[1-9]|1[0-8])\b`).

## O que esta rodada não mede

Qualidade do `08` gerado (Parte 2, não autorizada), efeito em pessoas, variância entre gerações,
outros hosts (Claude Code) e modelos, e o comportamento com desenvolvedor disponível respondendo.
