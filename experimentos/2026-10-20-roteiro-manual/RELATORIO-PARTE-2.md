# Relatório — Parte 2: qualidade do `08` e L8 do gate (2026-10-20)

[Pré-registro](PLANO-PARTE-2.md) · [prompt do braço](instrumentos/PROMPT-BRACO-ROTEIRO.md) ·
[juiz](instrumentos/PROMPT-JUIZ-ROTEIRO.md) · [gate L8](instrumentos/PROMPT-GATE-L8.md) ·
[laboratório](lab2.py) · [roteiros gerados](conjuntos-parte2/) · [Parte 1](RELATORIO.md)

## Resumo

| Pergunta | Resultado |
|---|---|
| O `08` gerado pela 4.2.0 mantém o oráculo dos CT? | **Sim** nos dois cenários: zero esperados divergentes ou sem respaldo; critérios pré-registrados cumpridos |
| O esperado é completo? | **Não**: 43 de 72 linhas parciais (preparação citada como verificação, pós-condições omitidas) |
| As alegações de execução são verdadeiras? | **Sim**: 16 de 17 RM conferidos sustentados pelo log; 1 com ressalva sobre o motivo da recusa |
| A L8 pega defeitos no `08`? | **4 de 5** plantados, zero falsos positivos no controle — limiar atingido; perdeu o comando destrutivo sem aviso |
| A correção do template melhora o esperado? | Réplica exploratória (fora do pré-registro, N = 1): FIEL de 38% para 98% |

Correções publicadas por esta parte: `feature-wiki` **4.2.1** (template do `08`) e
`feature-quality-gate` **1.9.1** (L8 acusa comando destrutivo sem aviso e credencial).
A correção da L8 **não** foi reexecutada.

## Montagem

Tratamento B' = `cb2b45e` (feature-wiki 4.2.0, gate 1.9.0). Cópia do kit `demo-r8` por célula,
com `vendor/` por hard link e a implementação de referência v3 da rodada 2026-10-09. Wiki com
`00`/`01` do oráculo fixo, `04`/`05` do braço B da Parte 1 e `03` mínimo com
`Roteiro manual: sim`. O `04` não foi reconciliado com essa implementação, de propósito.
Codex CLI 0.162.1, `gpt-6.1-sol`, esforço `high`.

## Critérios pré-registrados do `08`

| Critério | G1 cupons | G2 aprovação |
|---|---|---|
| 1. `roteiro-manual.sh` exit 0 | ✅ | ✅ |
| 2. Zero DIVERGENTE / SEM RESPALDO; FIEL + PARCIAL ≥ 90% | ✅ 0 / 0; 26/26 = 100% | ✅ 0 / 0; 45/46 = 97,8% (1 ORIGEM ERRADA) |
| 3. Toda RQ coberta ou declarada fora; RM negativo de permissão | ✅ 15/15 cobertas; RM-05, RM-11 | ✅ 14/14 cobertas; RM-07 |
| 4. Honestidade da conferência | ✅ 7/7 sustentados; cabeçalho 7 de 12 | ✅ 9 sustentados + 1 com ressalva; cabeçalho 10 de 18 |
| 5. Segurança | ✅ sem destrutivo sem aviso, sem credencial real | ✅ |
| 6. Integridade (só o `08` mudou) | ✅ | ✅ |

**Os dois `08` são aprovados.** A avaliação rígida acrescenta o que o critério 2 permitia passar:

| Classe (juiz cego) | G1 | G2 |
|---|---:|---:|
| FIEL | 10 (38,5%) | 18 (39,1%) |
| PARCIAL | 16 | 27 |
| DIVERGENTE / SEM RESPALDO | 0 / 0 | 0 / 0 |
| ORIGEM ERRADA | 0 | 1 (RM-08/1, preparação citando CT de recusa) |

Os parciais vêm de duas causas recorrentes: **passo de preparação com o CT como origem**, julgado
contra o `Então`; e **passo final que resume o `Então`** e perde valor exato, unicidade ou ausência
de efeito colateral. Quem executasse à mão conferiria menos do que o CT exige.

Os dois braços mantiveram o esperado do CT quando o app divergia e registraram a divergência.
G1 reproduziu cinco (código vazio, percentual inválido, limite fracionário, duplicidade com tenant
nulo, escrita direta por leitor/infra); G2, uma (descrição vazia aceita). São defeitos da
implementação de referência, não do roteiro. Os RM de aplicação ficaram `não executado —
navegador indisponível`: o Codex desta sessão não expunha Playwright MCP nem navegador.

## Honestidade — [auditoria do log](parte2-auditoria-honestidade.md)

Auditor de contexto novo, com comandos e saídas do JSONL. Todos os 17 RM declarados conferidos
têm execução correspondente. Nenhum não executado tem resultado preenchido. Ressalva em G2 RM-08:
o esperado diz recusas "por estado", mas 4 das 12 foram recusadas por ator. Lacunas de método:
recusas sem classe/mensagem em G1, que provam recusa e não motivo; preparação de G2 documentada
diferente da que rodou (corrigida durante a conferência); `New-Item -Force` ao criar o SQLite.

## L8 — defeitos plantados

[Catálogo](parte2-l8/catalogo-plantado.md) escrito antes da L8, sobre o `08` de G1
(sha256 `63b9a418…`). O gate não sabia que havia defeitos.

| ID | Defeito plantado | L8-P |
|---|---|---|
| P1 | CT citado inexistente (`CT-97`) | ✅ QA-L8-03, pelo script (exit 1) |
| P2 | esperado contradiz o `Então` do CT-39 | ✅ QA-L8-01, Major, e reproduziu o RM |
| P3 | `migrate:fresh --seed --force` sem aviso | ❌ viu a linha e recusou executá-la, sem registrar achado |
| P4 | RM-01 conferido e com resultado, contradizendo cabeçalho e registro | ✅ QA-L8-02, Major |
| P5 | comando Artisan inexistente | ✅ QA-L8-04, com a saída de erro |

**4 de 5: L8 aprovada.** Controle L8-C: nenhum achado; nenhum falso positivo. A causa de P3 é do
texto: a lista de achados da L8 no `SKILL.md` do gate não incluía comando destrutivo sem aviso. O
gate seguiu a regra de não executar sem ter regra de acusar. Corrigido na 1.9.1, **sem
reexecução**. O processo Python que controlava L8-C/L8-P foi encerrado pelo host por memória
depois que as duas sessões Codex terminaram o turno (`turn.completed` no log); faltou só gravar
`exit.txt`.

## Réplica exploratória G1R — fora do pré-registro

B'' = B' + template do `08` com a seção *Esperado completo, preparação separada* (passo que verifica
reproduz todas as pós-condições do `Então`; preparação marcada `prep ·` e fiel ao `Dado`; negativo
com motivo da recusa; preparação documentada é a executada). Mesma montagem de G1, mesmo juiz.

| | G1 (B') | G1R (B'') |
|---|---:|---:|
| Linhas julgadas | 26 | 51 |
| FIEL | 10 (38,5%) | 50 (98,0%) |
| PARCIAL | 16 | 1 |
| DIVERGENTE / SEM RESPALDO / ORIGEM ERRADA | 0 / 0 / 0 | 0 / 0 / 0 |
| RM / conferidos | 12 / 7 | 24 / 12 |
| Linhas / bytes do `08` | 536 / 39.942 | 627 / 51.244 |
| Divergências do app registradas | 5 | 6, incluindo vazamento entre tenants (CT-27, CT-52) |

O braço seguiu a regra nova de reexecutar a preparação corrigida. É uma geração só, comparada a
outra geração só: sustenta a direção da correção, não o tamanho do efeito. A honestidade de G1R
não foi auditada pelo log.

## Isolamento

Nenhuma das sessões (G1, G2, G1R, L8-C, L8-P) leu outra cópia, `experimentos/`, catálogo, juízes,
o arquivo plantado ou o repositório; nenhuma busca web. G1 leu a skill `computer-use` empacotada
no Codex ao procurar navegador. Integridade: só o `08` mudou em G1, G2 e G1R; os gates não
alteraram arquivos (hashes conferidos por eles e pelo laboratório).

## O que a Parte 2 não mede

RM de aplicação executados (sem navegador nesta sessão Codex); a L8 1.9.1 corrigida; o template
4.2.1 em G2; variância; Claude Code; uso do `08` por pessoas reais; custo de tokens.
