> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de escrever o `03-progresso.md`) e ao preencher `## Despachos`, `## Conformidade com Rules` e `## Quality Gate`. Fonte única de: template do `03-progresso.md`.

# Template do `03-progresso.md`

A regra da evidência inline, as duas seções que só existem para os steps 7 e 8 e a validação de
espelho ficam no corpo do `SKILL.md`, seção *Arquivo 03*.

**Template `03-progresso.md`**:
```markdown
# Progresso — {Card}

## {Seção 1 do Plano}
- [ ] {Item 1}
- [ ] {Item 2}

## {Seção 2 do Plano}
- [ ] {Item 1}

## Testes
- [ ] `{NomeDoTesteTest}` — CT-01, CT-02, CT-03
- [ ] `tests/Browser/{Nome}Test.php` — CT-B01, CT-B02 <!-- só se houver 05-*-browser.md -->

## Verificação Final
- [ ] `/ponytail:ponytail-review` no diff (validar contra over-engineering)
- [ ] `vendor/bin/pint --dirty`
- [ ] `vendor/bin/pest --filter={Feature} --compact`
- [ ] `vendor/bin/pest tests/Browser --filter={Feature}` <!-- se houver CT-B -->
- [ ] `vendor/bin/pest --parallel --tia` — nada mais no suite quebrou além da **baseline** de `{base}` (falhas pré-existentes por nome)
- [ ] `pest --mutate --path={classe}` — {score} em {duração}, {n} sobreviventes listados (no Windows, via lançador `.cmd`)
- [ ] **Custo medido** — queries do caminho principal × do caminho filtrado, contra o `## Modelo de Execução`, com N acima da página
- [ ] **`/code-review high {base}...HEAD` + passe de eixos (step 6.5)** — antes da reconciliação; achados fechados ou rejeitados com motivo
- [ ] Roteiro "Desenhado × Implementado" do `05-*-browser.md` preenchido <!-- se houver CT-B -->
- [ ] Desvios propagados ao `01`/`02`/`04`/`05` de origem, marcados `*(alterado em …)*`
- [ ] Citações `arquivo:símbolo:linha` reverificadas — {n}/{n} ok (saída do script colada)
- [ ] IDs `[CT-nn]` do teste ⊆ `04`/`05` e vice-versa
- [ ] Falsificabilidade dos CTs novos — {n} de {m} falham sem o fix; os demais "não falsificável nesta pilha", com motivo
- [ ] Docs pt/en, CHANGELOG e README reconciliados com o comportamento final
- [ ] `git commit`

<!-- Cada [x] acima leva " — {evidência}, {data}". Ex.: `- [x] composer test:kit — 677/677, 2026-09-05`
     Evidência com NÚMERO leva o comando que o gerou (`grep -c …`, saída do script). Degradação
     declarada ("sem PCOV", "plugin ausente") leva a PROVA NEGATIVA (`php -m`, `ls vendor/…`).
     Número sem comando e ausência sem prova foram os dois achados que o juiz cego devolveu
     CONTRA A SESSÃO em 2026-09-21 (QA-03, QA-04). -->

## Conformidade com Rules

<!-- Uma linha por rule de .ai/rules/index.md cujo glob casa com um arquivo do diff. "violada" = blocker do PR. -->

| Rule | Glob que casou | Aplicada / n.a. / violada | Evidência |
|---|---|---|---|
| `auth.md` — cobrir `fi-auth-layout` em par | `app/Filament/Pages/Auth/**` | aplicada | CT-07 + CT-38 |

## Quality Gate

<!-- Preenchido no step 8. Enquanto vazio, a feature NÃO está concluída e o PR não abre. -->

- **Ciclo**: {n} · **Veredito**: {APROVADO | APROVADO COM DÉBITO | REPROVADO → destino} · **Data**: {YYYY-MM-DD}
- **Relatório**: `06-relatorio-qa.md`

## Auditoria Pré-Implementação
<!-- Saída dos steps 5 e 6, ANTES de escrever código. Não confundir com "Desvios do Plano",
     que é pós-implementação. -->

### Revisão profunda (step 5) — premissas do plano contra o código real
| Premissa do plano | O código real diz | Correção aplicada na wiki |
|---|---|---|
| {"adicionar import X"} | {já existe em `Arquivo.php:12`} | passo 3 reescrito |

### Auditoria Ponytail (step 6)
| # | Sugestão de corte | Aplicada? | Onde |
|---|---|---|---|
| 1 | {…} | sim / recusada: {motivo} | `01`, passo 4 |

## Despachos

<!-- Claude Code: uma linha por disparo de sub-agente, com o modelo, o que ele NÃO recebeu e a
     auditoria do retorno. Host sem sub-agente: uma linha "Sem despacho — host sem sub-agente".
     Tarefa que rodou em linha por exceção: "Sem despacho — {motivo}".
     Auditoria REPROVADA também é linha (com o redespacho ao lado); fallback para general-purpose
     por agente fw-* indisponível vai na coluna Modelo. -->

| # | Step | Agente / tarefa | Modelo | Não recebeu | Resultado | Auditoria do retorno |
|---|---|---|---|---|---|---|
| 1 | 3 | `mecanico` — Superfície Livewire | haiku | — | tabela, 7 linhas | 2/7 conferidas por grep |
| 2 | 6.5 | `fw-revisor-diff` — eixos sobre `main...HEAD` | opus | `01`, `03` | 3 achados, 1 rejeitado | 3/3 reproduzidos |
| 3 | 8 | `fw-qa-gate` — quality gate | opus | conversa | `06` gravado verbatim, APROVADO COM DÉBITO | `git status` limpo antes/depois |

## Blockers
<!-- Impedimentos encontrados durante implementação -->
- [ ] {Blocker 1}: {descrição + o que está sendo feito para resolver}

## Desvios do Plano
<!-- Onde a implementação divergiu do PRD e por quê -->
- {Passo X alterado}: {motivo}

## Notas de Implementação
<!-- Descobertas durante o código que não estavam no plano -->
- {Descoberta 1}: {impacto e onde foi documentado}

## Retrospectiva
<!-- O que funcionou bem no planejamento e o que faltou -->
- **Funcionou bem**: {ponto positivo}
- **Faltou no plano**: {ponto de melhoria para próxima wiki}
```
