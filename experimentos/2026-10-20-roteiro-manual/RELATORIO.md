# Relatório — roteiro de teste manual opcional (2026-10-20)

[Pré-registro](PLANO.md) · [prompt do braço do step 4](instrumentos/PROMPT-BRACO-STEP4.md) ·
[cenário 3](instrumentos/cenario-3-requisito.md) · [laboratório](lab.py) ·
[tratamentos e hashes](tratamentos/manifest.json)

## Resumo

| Parte | Pergunta | Resultado |
|---|---|---|
| **R** — regressão do `04` | A inclusão do roteiro na `feature-wiki` piora a derivação de CT? | **Sem regressão** no critério estrito: conjuntos de detecção idênticos em C1 e C2 |
| **P** — pergunta do step 4 | A sessão pergunta na raia certa, recomenda pelo sinal da feature, respeita instrução explícita e registra só no `03`? | **B reprovado em P1** (justificativa copiada do exemplo); **B' aprovado** na reexecução única pré-registrada |

O que foi publicado é B'. A Parte R mediu B; B' muda só `references/entrevista-tres-raias.md`,
que nenhum braço da Parte R abriu (conferido nos logs), então a conclusão de R vale para B'.

## Tratamentos e ambiente

- **A** = `git archive 27f89eb .ai/skills` (feature-wiki 4.1.1, feature-test-design 1.17.3,
  feature-quality-gate 1.8.0). **B** = working tree sobre `27f89eb` depois da revisão independente
  (4.2.0 / 1.17.4 / 1.9.0). **B'** = B + correção da semente da entrevista.
- Os dois tratamentos foram normalizados para os bytes do blob (LF). Sem isso, `core.autocrlf=true`
  faria a working tree e o `git archive` diferirem em todos os arquivos por fim de linha. Depois da
  normalização, A × B difere em 14 arquivos alterados e 2 novos; o corpo do `SKILL.md` da
  `feature-test-design` difere só em `metadata.version`.
- Host: Codex CLI 0.162.1, `codex exec --dangerously-bypass-approvals-and-sandbox`, modelo
  `gpt-6.1-sol`, esforço `high`, `multi_agent` ativo. Mesmo modelo e esforço nos 12 braços e nos
  4 juízes. O deployment efetivo por trás do nome do modelo não é exposto.
- Uma cópia descartável do kit `demo-r8` por braço, com rótulo aleatório, sem `vendor/`,
  `node_modules/`, `.git`, `.env` de origem, configurações de agente, wikis `exp-*` e testes `Exp*`.

## Parte R — regressão do `04`

Instrumentos literais do protocolo: `PROMPT-BRACO.md` e `PROMPT-JUIZ-CEGO.md` versão 2 (hash em
[`congelamento.json`](congelamento.json)); oráculo `protocolo/oraculo-fixo/` sem `02`. Conjuntos
anonimizados (paths e versões redigidos) e varridos por IDs do catálogo antes do juiz.

| Cenário | Braço | Juiz anônimo | Detectados / 18 | DDR | Cenários no `04` | CT-B | Cegas | Declaradas |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Cupons | A | j-915f76 | 14 | 77,78% | 58 | 0 | 0 | 4 |
| Cupons | B | j-7d4f81 | 14 | 77,78% | 55 | 0 | 0 | 4 |
| Aprovação | A | j-19f129 | 15 | 83,33% | 75 | 2 | 2 (E08, E12) | 1 |
| Aprovação | B | j-6fcfc8 | 15 | 83,33% | 69 | 1 | 2 (E08, E12) | 1 |

- Em cada cenário, B detecta **o mesmo conjunto** de defeitos que A: nenhum perdido, nenhum
  ganho, nenhuma lacuna cega nova. Critério "sem regressão" do `PROTOCOLO.md` cumprido.
- As 58 citações literais dos DETECTA foram encontradas nos conjuntos que os juízes receberam
  ([`auditoria-citacoes.json`](auditoria-citacoes.json), [`audit_citations.py`](audit_citations.py)).
  Isso prova proveniência textual; não reavalia o mérito semântico.
- Revisão adversarial rodou nos quatro braços, por sub-agente de contexto novo, em duas rodadas.
- O gate de evolução do protocolo (DDR ≥ 0,85 em dois cenários) continua não atingido, em A e em B.
  Esta rodada não mede melhoria da derivação; mede só que a mudança não a piorou nesta amostra.
- N = 1 por célula. Igualdade exata não prova ausência de efeito; prova que esta amostra não
  mostrou regressão.

## Parte P — pergunta do roteiro no step 4

Critérios do pré-registro: (1) pergunta e recomendação com sinal; (2) linha de decisão no `03`;
(3) nada sobre roteiro no `00`; (4) nada além do step 4; (5) `roteiro-manual.sh`. Saídas
mecânicas em [`criterios-parte-p.json`](criterios-parte-p.json); wikis completas em
[`conjuntos/`](conjuntos/).

| Célula | Card / instrução | Pergunta e recomendação | Decisão no `03` | 1 | 2 | 3 | 4 | 5 | Veredito |
|---|---|---|---|---|---|---|---|---|---|
| P1 | cupons | Q17 desenho, ➡️ sim — "há UI e aceite humano na feature" | `não — sem resposta a Q17` | ❌ | ✅ | ✅ | ✅ | ✅ exit 0 | **reprovado** |
| P2 | aprovação | Q19 desenho, ➡️ sim — mesmo texto | `não — sem resposta a Q19` | ✅ ressalva | ✅ | ✅ | ✅ | ✅ exit 0 | aprovado |
| P3 | PII configurável | Q3 desenho, ➡️ não — "sem UI nova; backend cobre…" | `não — sem resposta a Q3` | ✅ | ✅ | ✅ | ✅ ¹ | ✅ exit 0 | aprovado |
| P4 | cupons + "gere também o roteiro" | nenhuma | `sim — instrução explícita` | ✅ | ✅ | ✅ ² | ✅ | ✅ exit 1 esperado | aprovado com desvio |
| P5 | aprovação + "não quero roteiro" | nenhuma | `não — instrução explícita` | ✅ | ✅ | ✅ | ✅ | ✅ exit 0 | aprovado |
| **P1-B'** | cupons | Q1 desenho, ➡️ sim — "RQ-01 pede cadastro no painel; há superfície de UI a conferir" | `não — sem resposta a Q1` | ✅ | ✅ | ✅ | ✅ | ✅ exit 0 | **aprovado** |

- **P1 (B)**: a justificativa é cópia literal do exemplo da semente em `entrevista-tres-raias.md`
  e afirma "aceite humano" num card que não o tem. A recomendação certa com sinal inventado
  reprova o critério 1. Em P2 o mesmo texto copiado por acaso é verdadeiro (aprovações humanas):
  aprovado com ressalva de que não demonstra raciocínio sobre o sinal.
- **Correção (B')**: o exemplo virou placeholder `{sim | não} — {sinal achado no requisito ou no
  código, ou "nenhum sinal"}`, com regra de citar o sinal desta feature e a cláusula onde aparece.
  Reexecução única de P1, em cópia nova: aprovada. A primeira tentativa de P1-B' foi interrompida
  pelo host por falta de memória e está arquivada em [`interrompidas/`](interrompidas/); a
  reexecução partiu de pasta de wiki limpa.
- ¹ **P3** criou `05-security.md`, extra do step 4 previsto em `estrutura-criada.md` para PII. O
  critério 4 do pré-registro dizia "nenhum `05`" querendo dizer o `05` de browser: erro de redação
  do pré-registro, declarado aqui, não reinterpretado como acerto silencioso.
- ² **P4** escreveu no `## Fonte` do `00` que a instrução "está registrada somente no `03`". Não é
  pergunta, RQ nem premissa (critério 3 literal cumprido), mas polui o `00` com meta-processo. B'
  passou a proibir qualquer menção no `00`; **essa correção não foi reexecutada em P4**.
- Controles A (P1-A, P2-A): nenhuma pergunta nem registro sobre roteiro manual, como esperado da
  4.1.1. Sem critério de aprovação e sem afirmação causal.

## Isolamento e contaminação

- Leitura de filesystem **não** isolada tecnicamente. Varredura dos comandos executados
  ([`varredura-comandos.json`](varredura-comandos.json)): nenhum braço leu outra cópia,
  `experimentos/`, catálogos, `demo-r8` ou o repositório da coletânea. Os padrões `Exp*`/`exp-*`
  aparecem apenas em globs de exclusão. A primeira varredura textual
  ([`varredura-isolamento.json`](varredura-isolamento.json)) só achou links do próprio pacote.
- Buscas web: só documentação de Laravel, Filament, Livewire, Pest, PHP e laravel-auditing.
- **P3** leu `~/.codex/skills/ai-sdk-development/SKILL.md` e `~/.agents/skills/...`, skills globais
  do host, relacionadas ao tema de IA do card. Contaminação de host comum a todos os braços, não
  removida pela cópia; não toca o roteiro manual.
- Juízes: diretório só com `catalogo.md` e `conjunto.md`; o filesystem também não estava isolado.

## O que esta rodada não mede

- Qualidade do `08` gerado, fidelidade dos resultados esperados, execução honesta e a L8 do gate
  (Parte 2 do desenho, não autorizada).
- Desenvolvedor disponível respondendo; P4 com a correção de B'; variância entre gerações (N = 1).
- Outros hosts e modelos (Claude Code em especial); custo de tokens; efeito em pessoas.
