# Experimentos — medição empírica das skills

Esta pasta guarda **as medições** que motivaram as versões das skills desta coletânea, e o
material necessário para **repetir a medição** a cada evolução relevante.

**Esta página é a fonte única de medição da coletânea.** READMEs, `SKILL.md` e `CHANGELOG.md`
citam o resultado de uma rodada com um link para cá, não com uma cópia do número. Cópia de número
que ainda exista fora daqui é pendência a corrigir, não segunda fonte. As tabelas das entradas
antigas do `CHANGELOG.md` são o registro do dia em que cada versão saiu; onde divergem desta
página, vale esta página, e a divergência está em
[Correções desta tabela](#correções-desta-tabela-2026-09-26).

> Regra da casa: skill não evolui por releitura de escrivaninha. Evolui por defeito que
> atravessou os dois braços de um experimento cego. Cada versão publicada precisa ter um
> gatilho medido nesta pasta.

## Estrutura

```
experimentos/
├── protocolo/                      # o que se reusa a cada rodada
│   ├── PROTOCOLO.md                # a definição do experimento, das métricas e do registro
│   ├── PROMPT-BRACO.md             # prompt do braço (agente que deriva os CTs) — fonte única
│   ├── PROMPT-JUIZ-CEGO.md         # prompt do juiz cego — reusar literalmente
│   ├── cenario-1-requisito.md      # card FERRO-812 (cálculo/valor — cupons)
│   ├── cenario-1-catalogo-defeitos.md   # 18 mutantes + 9 ambiguidades plantadas
│   ├── cenario-2-requisito.md      # card FERRO-830 (máquina de estados — aprovação)
│   ├── cenario-2-catalogo-defeitos.md   # 18 mutantes + 9 ambiguidades plantadas
│   └── oraculo-fixo/               # 00-requisito.md e 01-plano-acao.md congelados
│       ├── cenario-1-cupons/
│       └── cenario-2-aprovacao/
├── 2026-08-14-defeitos-plantados/  # baseline e rodadas 1 a 4 — sem vereditos arquivados
│   ├── relatorio.html              # o relatório das rodadas 1 a 4 (abrir no navegador)
│   ├── anexo-correcoes-factuais.md
│   └── conjuntos/                  # os arquivos 04 julgados (r1-c1, r1-c2, r3-c1, r4-c1, r4-c2)
├── 2026-08-15-rodada-5/            # feature-test-design 1.7.0 — vereditos.md, relatorio.html, conjuntos/
├── 2026-08-15-rodada-6/            # 1.8.0, kit recriado do zero
├── 2026-08-15-rodada-7/            # 1.9.0, Claude Code
├── 2026-08-15-rodada-8-cascade/    # 1.9.0, Cascade · Claude Sonnet 4 (dois conjuntos, os dois citam o catálogo — notas e, i)
├── 2026-08-15-rodada-9-glm5.2-high/           # conjuntos/ em extrato — ver nota g
├── 2026-08-16-rodada-10-kimi-k3-high/         # conjuntos/ em extrato — ver nota g
├── 2026-08-16-rodada-11-gemini/               # conjuntos/ em extrato, paráfrase da 10 — notas g, k
├── 2026-08-16-rodada-12-gpt5-high-thinking/   # conjuntos/ só com resumo — ver nota g
├── 2026-08-16-rodada-13-deepseek-v4-pro-max/  # conjuntos/ só com resumo — ver nota g
└── analise-comparativa-3-rodadas.md   # rodadas 7, 8 e 9 lado a lado
```

## O protocolo, em uma tela

1. **Requisito** curto e realista, com ~9 ambiguidades **plantadas de propósito**.
2. **Catálogo de defeitos** — 18 mutantes plausíveis escritos **antes** de existir qualquer
   conjunto de teste. Cada um é uma implementação que um dev competente escreveria de boa-fé.
3. **Braços independentes** — mesmo requisito, mesmo projeto, o **mesmo** `00-requisito.md`
   como oráculo fixo, agentes sem contexto compartilhado. Isola a técnica de derivação como
   única variável.
4. **Juiz cego** — recebe só o catálogo e o conjunto anonimizado. Ônus da prova é do conjunto;
   **citação literal obrigatória** em cada DETECTA; na dúvida, NÃO DETECTA; formato não é mérito.
5. **Métricas** — DDR (detectados / 18), **lacunas cegas × declaradas** (a distinção mais
   informativa), oráculos fracos, falsos ✅.
6. **Materialização em Pest** contra a **mesma** implementação, escrita por um terceiro agente
   que nunca viu os conjuntos e que **não pode ler a implementação** — só o contrato público.
7. **Registro** — cada rodada arquiva os conjuntos inteiros e um veredito com uma linha por
   defeito e a citação literal. Placar sem essa tabela não é medição auditável
   ([`PROTOCOLO.md`](protocolo/PROTOCOLO.md), *Registro obrigatório*).

Dois cenários bastam para não superajustar: um de **cálculo/valor** e um de **máquina de
estados** — eles falham por motivos diferentes.

## Ambiente

Projeto-cobaia descartável criado com `composer create-project gsferro/starter-kit-easy`
(Laravel 13 · Filament 5 · Pest 5 com browser e mutate · Xdebug em modo `coverage`).
Em 2026-08-14/15 ficou em `D:\PROJECTS\SKILLS\demo-wiki`, com as rodadas em
`wikis/specs/exp-a` … `exp-e`. A rodada 6 recriou o kit do zero; as rodadas 7 e 8 em diante
usaram `demo-r7` e `demo-r8`, criados do mesmo kit.

O kit é a cobaia certa por dois motivos: já traz as skills em `.ai/skills/`, e traz **wikis
reais** em `wikis/specs/` produzidas pela própria `feature-wiki` em produção — o que permite
auditoria forense da saída real, não só teste sintético.

## Histórico

Uma linha por rodada. Cada célula de cenário é **`detectados de 18 · lacunas cegas · lacunas
declaradas`**; entre parênteses, o número de cenários que a fonte reporta (nas rodadas 1 a 4, só
o `04`; da 5 em diante, `04` + `05`) e, no cenário 2, as células inválidas da matriz estado ×
evento executadas, quando o juiz as contou. A coluna **Registro** diz o quanto o placar vale
(ver [Como ler](#como-ler)).
`ftd` = `feature-test-design`; `fw` = `feature-wiki`.

| Rodada | Data | Versões medidas | Braço (host · modelo) | C1 · cupons | C2 · aprovação | Total de 36 | Registro | Fonte |
|---|---|---|---|---|---|---|---|---|
| Baseline | 2026-08-14 | `fw` 2.10.0, sem skill de derivação | não registrado | 7 · 10 · 1 (12 + 2 CT-B) | 11 · 7 · 0 (18 + 3 CT-B; 9 de 21) | 18 | rejulgável | `relatorio.html`; CHANGELOG `ftd` 1.1.0 e 1.2.0; `conjuntos/r1-c*-conjunto-A-baseline.md` |
| 1 | 2026-08-14 | `ftd` 1.0.0 | não registrado | 12 · 2 · 4 (37) | — | — | rejulgável | `relatorio.html`; CHANGELOG `ftd` 1.1.0; `conjuntos/r1-c1-conjunto-B-pipeline.md` |
| 2 | 2026-08-14 | `ftd` 1.1.0 ᵃ | não registrado | — | 15 · 2 · 1 (45; 21 de 21) ᵇ | — | rejulgável | CHANGELOG `ftd` 1.2.0 e 1.7.0; `conjuntos/r1-c2-conjunto-B-pipeline.md` |
| 3 | 2026-08-14 | `ftd` 1.3.0 ᶜ | não registrado | 16 · 1 · 1 (41) ᵇ | — | — | rejulgável | `relatorio.html`; CHANGELOG `ftd` 1.4.0 e 1.6.0; `conjuntos/r3-c1-conjunto.md` |
| 4 | 2026-08-15 | `ftd` 1.5.0 | não registrado | 16 · 1 · 1 (47) | 17 · 1 · 0 (63; 21 de 21) | 33 | rejulgável | CHANGELOG `ftd` 1.6.0 e 1.7.0; `conjuntos/r4-c*-conjunto.md` |
| 5 | 2026-08-15 | `fw` 3.0.0 · `ftd` 1.7.0 | não registrado | 14 · 2 · 2 (51) | 17 · 1 · 0 (63; 17 de 21) | 31 | auditável | [`rodada-5/vereditos.md`](2026-08-15-rodada-5/vereditos.md) |
| 6 | 2026-08-15 | `fw` 3.0.0 · `ftd` 1.8.0 | não registrado; kit recriado (Laravel 13.25 · Filament 5.6 · Pest 5.1) | 16 · 0 · 2 (58) | 17 · 1 · 0 (49; 21 de 21) | 33 | rejulgável ʲ | [`rodada-6/vereditos.md`](2026-08-15-rodada-6/vereditos.md) |
| 7 | 2026-08-15 | `fw` 3.0.0 · `ftd` 1.9.0 | Claude Code · Claude Sonnet 4 ᵈ | **15** · 0 · 3 (60) | 18 · 0 · 0 (58) | 33 | auditável | [`rodada-7/vereditos.md`](2026-08-15-rodada-7/vereditos.md) |
| 8 | 2026-08-15 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · Claude Sonnet 4 ᵈ | 15 · 0 · 3 (24) | 18 · 0 · 0 (31) | 33 | contaminada ⁱ | [`rodada-8-cascade/vereditos.md`](2026-08-15-rodada-8-cascade/vereditos.md) ᵉ |
| 9 | 2026-08-15 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · GLM 5.2 High | 15 · 0 · 3 (22) | 18 · 0 · 0 (36) ᵍ | 33 ᶠ | relato ᵍ | [`rodada-9-glm5.2-high/vereditos.md`](2026-08-15-rodada-9-glm5.2-high/vereditos.md) |
| 10 | 2026-08-16 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · Kimi K3 High | 15 · 0 · 3 (19) | 18 · 0 · 0 (37) | 33 ᶠ | relato ᵍ | [`rodada-10-kimi-k3-high/vereditos.md`](2026-08-16-rodada-10-kimi-k3-high/vereditos.md) |
| 11 | 2026-08-16 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · Gemini 3.7 Flash High | 15 · 0 · 3 (19) | 18 · 0 · 0 (37) | 33 ᶠ | relato ᵍ ᵏ | [`rodada-11-gemini/vereditos.md`](2026-08-16-rodada-11-gemini/vereditos.md) |
| 12 | 2026-08-16 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · GPT‑5 High Thinking | 15 · 0 · 3 (19) | 18 · 0 · 0 (37 ou 36) ᵍ | 33 ᶠ | relato ᵍ | [`rodada-12-gpt5-high-thinking/vereditos.md`](2026-08-16-rodada-12-gpt5-high-thinking/vereditos.md) |
| 13 | 2026-08-16 | `fw` 3.0.0 · `ftd` 1.9.0 | Cascade · DeepSeek V4 Pro Max | 15 · 0 · 3 (19) | 18 · 0 · 0 (36) | 33 ᶠ | relato ᵍ | [`rodada-13-deepseek-v4-pro-max/vereditos.md`](2026-08-16-rodada-13-deepseek-v4-pro-max/vereditos.md) |

**Notas**

- **ᵃ Versão da rodada 2.** A entrada 1.2.0 do CHANGELOG, escrita no dia, rotula a coluna como
  `v1.1.0` e apresenta o cenário 2 como "segundo cenário do experimento"; a entrada 1.1.0 só traz
  o cenário 1. A entrada 1.7.0 e o README da `feature-test-design` até a 1.14.1 rotulam o mesmo
  15 de 18 como `v1.0.0`. O número é o mesmo nas três; o rótulo que bate com a cronologia é
  1.1.0. O arquivo se chama `r1-c2-…` por ser o primeiro conjunto do cenário 2.
- **ᵇ Piso, não medida limpa.** Nas rodadas 2 e 3 o recorte para o juiz saiu **antes** do
  resultado da revisão adversarial: os dois conjuntos prometem a seção de achados "ao fim do
  arquivo" e terminam sem ela. Na rodada 3 a adversarial provou depois mais seis implementações
  erradas (CHANGELOG `ftd` 1.5.0). A partir da rodada 4 o recorte sai depois
  ([Como repetir](#como-repetir), passo 5).
- **ᶜ Versão da rodada 3.** 1.3.0 é a versão vigente na data. O CHANGELOG (entradas 1.4.0 e
  1.6.0) e o README da `feature-test-design` até a 1.14.1 rotulam a coluna como `v1.1.0` — a
  versão cujas regras a rodada media.
- **ᵈ** Os `vereditos.md` das rodadas 7 e 8 não registram o modelo; ele vem de
  [`analise-comparativa-3-rodadas.md`](analise-comparativa-3-rodadas.md).
- **ᵉ Rodada 8 tem dois conjuntos.** O primeiro (`conjuntos/cenario-*-conjunto.md`, julgado em
  [`vereditos-anterior.md`](2026-08-15-rodada-8-cascade/vereditos-anterior.md)) deu o mesmo
  placar com 62 e 61 cenários; o que está na tabela é o segundo (`conjuntos/cupons-de-desconto/`,
  `conjuntos/aprovacao-de-compra/`).
- **ᶠ Prompt do braço não registrado, com pista provável.** Nenhuma das rodadas 8 a 13 registra
  qual prompt o braço recebeu. O prompt que esta página publicou junto com a rodada 13 (commit
  `daecc3f`) trazia pistas tiradas do catálogo e das rodadas anteriores: o tamanho da matriz do
  cenário 2 (30 células), as três lacunas a declarar no cenário 1 (fuso, exclusão lógica,
  `Pedido` — os defeitos D14, D15 e D18), "exatamente" nos oráculos monetários com o valor
  2.900 (o discriminante de D16), e reforçava duas premissas do `00` que apontam defeitos do
  catálogo (A-04 e A-09). As rodadas 9 a 13 mostram marcas compatíveis com ele: matriz de 30
  células "na primeira passagem" e o juiz da 12 citando os discriminantes marcados como
  "exatamente". Os volumes idênticos de 19 e 37 cenários não entram nessa conta: entre a 10 e a
  11 eles vêm de cópia (nota k), e nas 12 e 13 não há conjunto para conferir. É contaminação
  provável, não provada. O placar vale como relato, não como medição cega.
- **ᵍ Relato: o conjunto julgado não está no repositório.**
  - **Rodadas 9 a 11 — extrato.** Os juízes classificam D14, D15 e D18 como `Lacuna declarada
    L-01/L-02/L-03`, citam premissas (`P-01`, `P-03`) e, na 9, a seção `## Fronteira com o
    Plano`. Nenhum desses textos está nos `cenario-1-conjunto.md` arquivados, que também não têm
    perfil, SFDIPOT nem mutantes (o `04` da rodada 7 tem 52 linhas com esses termos). No C2 da
    rodada 9, o arquivado tem 40 cabeçalhos de CT (CT-01…CT-31, mais 06b, 08b, 09b e 09c, e
    CT-B01…CT-B05) e o veredito conta 36 (`31 no 04 + 5 no 05`). A classificação `0 cegas · 3
    declaradas` dessas rodadas não pode ser conferida.
  - **Rodadas 12 e 13 — só o placar.** Os vereditos não têm a tabela por defeito com citação
    literal que o [`PROMPT-JUIZ-CEGO.md`](protocolo/PROMPT-JUIZ-CEGO.md) exige, e o `conjuntos/`
    delas guarda um resumo de 7 a 10 linhas. Na rodada 12 o veredito diz 37 cenários no C2 e o
    resumo lista 36 (CT-01…CT-31 e CT-B01…CT-B05).
- **ⁱ Rodada 8 — o conjunto cita o catálogo.** Os dois conjuntos arquivados trazem os IDs do
  catálogo, e o segundo traz também as descrições. `cupons-de-desconto/04-casos-de-teste.md`
  cita D01 a D18 — por exemplo `D16: 29% distingue float de inteiro` e `Detecta D08 (dois pedidos
  simultâneos estouram limite)`, que é o texto da linha D08 de
  [`cenario-1-catalogo-defeitos.md`](protocolo/cenario-1-catalogo-defeitos.md);
  `aprovacao-de-compra/04-casos-de-teste.md` cita E01 a E18. O primeiro conjunto
  (`cenario-1-conjunto.md`) declara as lacunas como `(D14)`, `(D15)` e `(D18)`. Nenhum conjunto
  de outra rodada tem ID do catálogo (`grep -oE '\b[DE](0[1-9]|1[0-8])\b'`). O braço viu o
  catálogo ou um veredito: o placar da rodada 8 não mede a skill e fica fora de toda contagem.
- **ʲ Rodada 6 sem linha por defeito.** O `vereditos.md` lista os detectados numa linha por
  cenário (`Detectados:` seguido dos IDs; no C2, `E01…E17`) e só dá tabela, com o porquê, para os
  não detectados. Falta a citação literal que o `PROMPT-JUIZ-CEGO.md` exige em cada DETECTA. Há
  evidência parcial no próprio veredito: D15 morto pelo CT-26; D14 pelo CT-29, com
  `config(['app.timezone'])` divergido e o instante `01:30Z`. Os conjuntos `r6-*` estão inteiros:
  a rodada pode ser rejulgada.
- **ᵏ Rodada 11 não é independente da 10.** O conjunto da 11 é uma paráfrase, CT a CT, do da 10:
  os mesmos 19 CTs no C1 e 37 no C2, na mesma ordem e com o mesmo tema, com um `CT-10b` nos
  dois. Os vereditos foram commitados com 7 minutos de diferença (`dc9fc26` às 00:08:06 e
  `05a354d` às 00:15:06), e as duas rodadas usaram o mesmo projeto (`demo-r8`), sem registro de
  que o `exp-r10` tenha sido removido antes da 11. A tabela de exemplos do CT-13 é idêntica nas
  duas, mas também na rodada 9, e sozinha não prova cópia; a estrutura prova. A 11 não conta
  como família à parte.

### Como ler

- **Registro**, pela regra do [`PROTOCOLO.md`](protocolo/PROTOCOLO.md) (*Registro obrigatório*):
  - **auditável** — veredito com uma linha por defeito e citação, e o conjunto julgado inteiro
    no repositório;
  - **rejulgável** — o conjunto inteiro está aqui, mas o veredito não foi arquivado ou não tem a
    tabela por defeito: o placar é relato até um juiz novo julgar o conjunto;
  - **relato** — o conjunto julgado não está no repositório;
  - **contaminada** — o conjunto cita o catálogo; o placar não mede nada.
- **Rodadas 1 a 4 não têm veredito arquivado.** Os juízes julgaram, mas só as contagens foram
  preservadas (ressalva do [`relatorio.html` da rodada 5](2026-08-15-rodada-5/relatorio.html)).
  A fonte delas é o `relatorio.html` das rodadas 1 a 4 e as entradas do CHANGELOG escritas no
  dia; os conjuntos julgados estão em `2026-08-14-defeitos-plantados/conjuntos/` e podem ser
  rejulgados. As rodadas 5 e 7 a 11 têm uma linha por defeito, com citação; a 6 lista os
  detectados sem citação (nota j); a 12 e a 13 trazem só o placar.
- **O baseline é um só**: o do cenário 1 rodou junto com a rodada 1, o do cenário 2 junto com a
  rodada 2.
- **Nenhuma rodada registra o modelo do juiz.** A comparabilidade entre juízes é suposta, não
  conferida. O protocolo passa a exigir o registro.
- **A primeira condição do critério de parada** do [`PROTOCOLO.md`](protocolo/PROTOCOLO.md)
  (DDR ≥ 0,85 nos dois cenários) foi atingida nas rodadas 4 e 6 — as duas rejulgáveis — e deixou
  de ser na rodada 7, com o C1 em 15 de 18 (83,3%). As rodadas 8 a 13 reportam o mesmo C1.

### O que mudou entre as rodadas 5 e 7, defeito a defeito

Só os defeitos que mudaram de veredito. A coluna da rodada 6 vem da lista de detectados do
veredito, sem citação (nota j). Os vereditos das rodadas 8 a 11 repetem a 7 defeito a defeito,
mas não a confirmam (notas g, i e k).

| Defeito | Rodada 5 (1.7.0) | Rodada 6 (1.8.0) | Rodada 7 (1.9.0) |
|---|---|---|---|
| D09 — policy só no form; request direto passa | lacuna cega | detecta | detecta |
| D12 — validade no passado aceita na criação | detecta | lacuna declarada (premissa afirmativa P-B) | detecta |
| D14 — validade em UTC × São Paulo | lacuna declarada | detecta | lacuna declarada |
| D15 — cupom excluído ainda aplicável | lacuna cega | detecta | lacuna declarada |
| D18 — mesmo cupom duas vezes | lacuna declarada | lacuna declarada | lacuna declarada |
| E01 — aprovar solicitação em rascunho | lacuna cega | detecta | detecta |
| E18 — e-mail sai com a gravação falhando | detecta | lacuna cega | detecta |
| **C1 · C2** | **14 · 17** | **16 · 17** | **15 · 18** |

O total igual das rodadas 6 e 7 (33 de 36) escondeu uma troca. Na rodada 7, a 1.9.0 passou a
detectar D12 no C1 e E18 no C2, e deixou de detectar D14 e D15 no C1, que voltaram a lacuna
declarada. **O C1 caiu de 16 para 15**, e isso não estava registrado em lugar nenhum. Os juízes
das rodadas 7 a 13 leram D14 e D15 como débito de arnês; a rodada 6 detectou os dois com o mesmo
starter-kit — D14 com `config(['app.timezone'])` divergido e o instante `01:30Z`, D15 pelo
cenário que a premissa de mecanismo não pode apagar (regra da 1.8.0).

O que isso sustenta é uma observação, não uma regressão atribuída à 1.9.0:

- **Um braço por cenário, de cada lado.** A própria rodada 5 tratou uma queda de 16 para 14 no
  C1 como "dentro do que a variância explicaria sozinha".
- **A ponta da rodada 6 é rejulgável, não auditável** (nota j): a evidência de D14 e D15 é a
  parcial do veredito (CT-29 e CT-26), sem a tabela por defeito.
- **As rodadas 8 a 13 não confirmam a 7.** A 8 viu o catálogo (nota i); as 9 a 11 guardam extrato
  (nota g); e o prompt publicado junto com a 13 mandava *"Declare lacunas quando o arnês impedir a
  falsificação (timezone, soft-delete, Pedido)"* — exatamente D14, D15 e D18 (nota f).

Atribuir a queda à 1.9.0 pede o rejulgamento da rodada 6 e uma rodada de regressão com dois
braços por cenário (o formato da [rodada pendente (a)](#a-item-3--a-release-de-references-sem-regressão)).

### Materialização em Pest (rodada 1, cenário 1)

As duas especificações da rodada 1 viraram suítes Pest contra a **mesma** implementação, escrita
por um terceiro agente que não viu nenhum dos dois `04`.

| | Suíte do baseline | Suíte da `ftd` 1.0.0 |
|---|---|---|
| Defeitos plantados detectados pelo juiz, na especificação | 7 de 18 | 12 de 18 |
| Testes verdes | 22 (55 assertions) | 38 (91 assertions) |
| Defeitos reais encontrados na implementação | 2 | 2 |
| Mutation score em `app/Services` | 100% (24/24) ʰ | 100% (24/24) ʰ |

Os dois defeitos reais foram diferentes (unicidade não imposta com `tenant_id` nulo; borda da
validade com `>=` no lugar de `>`); os dois pegaram a trilha de auditoria sobrescrita. União: três
defeitos reais. A comparação de suítes mede "especificação + quem escreveu o teste"; a do juiz
mede só a especificação.

- **ʰ Não verificado.** A medição foi feita no Windows, com Pest 5.0.5 — o ambiente em que, em
  2026-09-21, o `pest --mutate` foi medido dando 100% falso (o plugin relança `argv[0]`, o `cmd`
  não o executa, e toda saída não-zero conta como mutante morto). O relatório não registra
  `Duration` nem a lista de sobreviventes, que são o que distingue o score real do falso. O
  argumento estrutural — mutação não gera mutante para código que não existe — continua de pé; o
  número 24/24 não.

A auditoria de 9 wikis reais (125 casos) que motivou a `feature-test-design` não é rodada deste
protocolo; ela vive no [README da skill](../.ai/skills/feature-test-design/README.md).

### Convergência entre famílias (rodadas 7 a 13) — o que se sustenta

As sete rodadas com a 1.9.0 reportaram o mesmo placar (15 de 18 e 18 de 18) em seis famílias de
modelo. O que isso sustenta é menos do que esta página dizia:

- **Auditável é uma só: a rodada 7** (Claude Code · Claude Sonnet 4). É a única das sete com
  veredito por defeito com citação, conjunto inteiro no repositório e nenhum ID do catálogo no
  conjunto. A 8 viu o catálogo (nota i); as 9 a 11 guardam extrato (nota g); a 11 é paráfrase da
  10 (nota k); a 12 e a 13 só têm o placar (nota g). Com uma rodada auditável não há comparação
  entre famílias a fazer.
- **O prompt das rodadas 8 a 13 não foi registrado**, e o que esta página publicou junto com a 13
  carregava pistas do catálogo (nota f). Placar idêntico com pista no prompt não separa "a skill
  domina" de "o prompt entregou a resposta".
- **Um braço por modelo, um juiz por cenário, o mesmo oráculo.** Mesmo que as sete fossem
  auditáveis, placar igual seria compatível com "a skill pesa mais que o modelo na eficácia", sem
  provar. O volume reportado variou com o host e o modelo: de 19 a 60 cenários no C1.
- **O placar igual não é o da rodada 6.** Ver a tabela defeito a defeito acima.

Na rodada 5, as quatro regras que ainda não tinham sido medidas (1.4.0 a 1.7.0) mataram cada uma
o defeito que a originou. O que sobrou foi **deslocamento de orçamento**: três lacunas cegas
novas, em dois cenários e dois juízes independentes, todas na mesma assinatura — o conjunto
esgota os eixos **valor** e **ator** e assume o eixo **mecanismo/estado**.

## Correções desta tabela (2026-09-26)

O que esta página dizia antes, e o que os dados brutos sustentam.

1. **Rodada 1 dizia "C1, C2 · 12/18 e 17/18".** O cenário 2 não foi medido na rodada 1. O 17 de
   18 é o C2 da rodada 4 (1.5.0): a tabela *O que a medição devolveu* do `relatorio.html` põe na
   coluna "Pipeline novo" o C1 da rodada 1 (12 de 18) ao lado do C2 da rodada 4, e esta página
   copiou a coluna. A primeira medição do C2 é a rodada 2, com **15 de 18** — CHANGELOG `ftd`
   1.2.0 e 1.7.0 (2 cegas + 1 declarada). Confere com o gatilho da 1.2.0 no relatório ("3
   defeitos comuns · cenário 2") e com "os três defeitos mais teimosos sobreviveram a dois
   conjuntos": com 17 de 18, só um defeito teria escapado. O relatório ganhou uma errata no ponto.
2. **Rodada 2 dizia "sem linha própria".** Ela tem resultado (15 de 18) e é a "medição 2"
   contaminada do `relatorio.html` ("dois cenários, três medições"; "as medições 2 e 3 tiveram
   contaminação conhecida").
3. **Rodada 4 dizia "ver `relatorio.html`".** O relatório traz o C2 da rodada 4 (17 de 18) na
   coluna "Pipeline novo" e no destaque do topo, sem dizer a rodada, e o 16 de 18 do C1 só no
   destaque — número que serve tanto para a rodada 3 quanto para a 4, que deram as duas
   `16 · 1 · 1`. A atribuição por rodada vem das entradas 1.6.0 e 1.7.0 do CHANGELOG, conferidas
   com os conjuntos (47 e 63 cenários).
4. **A queda do C1 de 16 para 15 na 1.9.0** não aparecia em lugar nenhum. Está na tabela
   defeito a defeito, como observação de um braço na rodada 7, sem atribuição à versão.
5. **"Seis famílias produziram o mesmo DDR; a skill é o fator dominante"** foi reescrito: das
   sete rodadas com a 1.9.0, só a 7 é auditável — a 8 viu o catálogo, as 9 a 11 guardam extrato,
   a 11 é paráfrase da 10, a 12 e a 13 só têm placar —, e as rodadas 9 a 13 têm pista provável no
   prompt. Saiu também "modelos 2025+ convergem em 0 iterações para fechar C2": vem dos vereditos
   das rodadas 9 a 13, que são relato.
6. **Baseline com "22 e 27 cenários"** (placar das rodadas 5 e 6): os conjuntos do baseline têm
   12 CT + 2 CT-B no C1 e 18 CT + 3 CT-B no C2. O 22 é o número de testes Pest verdes da suíte
   materializada do baseline C1; o 27 não tem fonte. A densidade do baseline nas rodadas 5 e 6
   (0,32 · 0,41) usa esses denominadores. A conclusão do critério de parada da rodada 6 ("`N_CT`
   mais que dobrou") não muda: contando `04` + `05` dos dois lados, 58 contra 14 e 49 contra 21.
7. **"Expectativa de DDR com modelos locais"** era apresentada "com base nos resultados das 13
   rodadas". Nenhuma rodada com modelo local foi feita: é hipótese, e agora está marcada assim.
8. **"100% (24/24)" do mutation score** passa a constar como não verificado (nota h).
9. **Rodada 8 constava como medição.** Os conjuntos dela citam os IDs e as descrições do
   catálogo (nota i). Sai de toda contagem.
10. **Rodadas 6 e 9 a 11 constavam como medição.** A 6 não tem a tabela por defeito (nota j) e é
    rejulgável; as 9 a 11 guardam extrato do conjunto julgado (nota g) e são relato.

## Rodadas pendentes

Medições que o roteiro do estudo
[`2026-09-26-agentskills-spec-to-spec-to-tickets.md`](../estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md)
(§8) exige e que as sessões das releases não fizeram: elas pedem um projeto Laravel e, as de DDR, os
braços do protocolo. As três primeiras são da release 1 (2026-09-26); de (d) a (g), da release 2
(2026-09-27), que saiu na mesma sessão, antes de qualquer uma delas rodar
([estudo, §9](../estudos/2026-09-26-agentskills-spec-to-spec-to-tickets.md#9-execução-do-roteiro-2026-09-2627)).
Ordem sugerida: (a) → (d), a série de regressão, uma fase por vez; depois (b), (e), (c) e (g). A (f)
é barata e não depende das outras: pode ir primeiro.

**Pré-requisito das rodadas (a) e (b).** O oráculo congelado não tem
`02-decisoes-arquiteturais.md`, e a `feature-test-design` ≥ 1.12 exige a `## Superfície Livewire`
dele quando a feature cria página, widget ou componente — os dois cenários criam. Antes da
primeira rodada da série, gerar o `02` **uma vez** sobre o `00`/`01` congelados, conferir,
commitar em `protocolo/oraculo-fixo/{cenario}/` e usar o mesmo em todos os braços da série — ou
deixá-lo ausente em todos e registrar a ausência. Rodada com `02` e rodada sem `02` não se
comparam na linha de superfície Livewire. A rodada (c) não usa o oráculo congelado: nela o
próprio fluxo gera o `02`.

### (a) Item 3 — a release de `references/` sem regressão

- **Partida**: `feature-wiki-v3.5.2` + `feature-test-design-v1.14.1`.
- **Chegada**: `feature-wiki-v3.6.0` + `feature-test-design-v1.15.0`. As tags da release 1 são
  criadas no commit dela.
- **Montagem**: os dois cenários, um braço por cenário por tag (dois, se o orçamento permitir —
  um braço por cenário não separa regressão de variância, ressalva da rodada 5). Mesmo kit, mesmo
  oráculo, o mesmo [`PROMPT-BRACO.md`](protocolo/PROMPT-BRACO.md) nas duas pontas (mesmo commit),
  o mesmo juiz: mesmo prompt **e** mesmo modelo. Medir a partida com o prompt antigo mudaria duas
  variáveis; compará-la com as rodadas 7 a 13 também (outro prompt, outra versão).
- **Registrar além do usual**: quais arquivos de `references/` cada braço de chegada diz ter
  aberto (o retorno do prompt pede). O risco que a rodada mede é o agente não abrir a referência e
  a regra deixar de valer (estudo, §1.4).
- **Pronto quando** (estudo, §8, item 3): "uma rodada do protocolo de `experimentos/` antes e
  depois, mesmo kit, mesmo juiz; sem regressão em C1/C2". **Sem regressão**, em cada cenário:
  detectados na chegada ≥ detectados na partida; nenhum defeito que a partida detectou vira NÃO
  DETECTA na chegada; nenhuma lacuna cega nova. O total igual não basta — foi assim que a troca
  entre as rodadas 6 e 7 passou.

### (b) Item 7 — primeira rodada do perfil mínimo da `feature-test-design`

Nenhuma rodada mediu o perfil mínimo: o prompt antigo mandava "aplicar o pipeline completo", e os
dois cenários pontuam P×I 6 a 9 na maioria das áreas.

- **Partida**: `feature-test-design-v1.15.0` (o perfil mínimo como é hoje: 1 cenário por regra,
  só partição, gate de mutantes afirmado pelo mesmo agente que derivou).
- **Chegada**: `feature-test-design-v1.16.0` (+ `feature-wiki-v4.0.0`), a release 2, que implementou
  o item 7: coluna `Asserção que mata` obrigatória em todo perfil. Na 1.16.0, `RQ` aberta não gera
  cenário: o braço de chegada precisa do solicitante simulado descrito em (d).
- **Montagem**: marcador `{PERFIL}` do `PROMPT-BRACO.md` = mínimo imposto em todas as áreas,
  declarado no cabeçalho do `04`. Os dois cenários têm áreas de Impacto 3 (dinheiro,
  autorização), então a revisão adversarial dispara pelo Impacto 3 mesmo no mínimo — o que se
  mede é "mínimo com adversarial". O mínimo **sem** adversarial só se mede num cenário 3 de
  Impacto ≤ 2, com requisito e catálogo escritos antes de qualquer conjunto; esse cenário não
  existe ainda. Um braço de controle com o perfil que o passo 0 decidir, mesma tag, dá o custo
  do mínimo.
- **Registrar além do usual**: por mutante do gate, se o `04` aponta a asserção ou o valor do
  cenário que diverge, ou só afirma que o cenário mata. É a medida do gate autocertificado
  (estudo, §7.3).
- **Pronto quando** (estudo, §8, item 7): "rodada com perfil mínimo no protocolo; coluna
  'asserção que mata' obrigatória na tabela de mutantes".

### (c) Item 11 — primeira execução real da `requirement-to-rule`

Três versões e nenhuma execução registrada (estudo, §7.1, T14). Não é rodada de DDR: não há
catálogo de defeitos para rules. É uma execução descrita.

- **Partida**: `requirement-to-rule-v1.3.0` + `feature-wiki-v3.6.0` (o step 9 que a chama).
- **Chegada**: `requirement-to-rule-v1.4.0` + `feature-wiki-v4.0.0`, a release 2, que implementou o
  item 10. Na 4.0.0 o step que chama a skill é o 12 (era o 9), e a skill é a dona única dele. Na
  chegada, registrar também a prova do `arch()` por `scripts/prova-arch.sh`, a linha de retorno
  (`apresentados N · gravados N · …`) e, se houver poda, o índice depois dela.
- **Montagem**: projeto-cobaia com `laravel/boost` ≥ 2.4.12 (a tool MCP `record-rule`, com
  `glob`, `title` e `note`, existe desde essa versão) e uma feature completa, steps 0 a 9 na
  partida (3.x) e 0 a 12 na chegada — a feature de referência de 2026-09-21 no `demo-wiki`, se a
  wiki dela ainda existir, ou o cenário 2 implementado de ponta a ponta. Rodar só em cobaia
  descartável: não existe tool nem comando para remover rule.
- **Registrar**: versões (`metadata.version` das skills, `laravel/boost`); host e modelo;
  candidatos coletados e por quem (o step de rules — 9 na 3.x, 12 na 4.0.0 — ou a skill); por
  candidato, o resultado de cada um dos 4 gates com a evidência — e se o gate 4 (`search-docs`,
  MCP) rodou, em que rota; **quantos prompts de aprovação** o usuário recebeu; as rules gravadas
  por `record-rule` e se o índice regenerado as lista; para rule mecânica, se o `arch()` ou a config que ela cita existe e se a
  suíte roda.
- **Pronto quando** (estudo, §8, itens 10 e 11): "primeira execução real registrada em
  `experimentos/`"; na chegada, "um prompt de aprovação, não dois".

### (d) Release 2 × release 1 — o desenho sem regressão em C1/C2

A release 2 mudou o desenho da derivação: o `04` nasce depois do Ponytail (step 7), com costuras de
teste declaradas, `Asserção que mata` em todo perfil, `RQ` aberta sem cenário e perguntas ao
solicitante. Nenhuma rodada mediu se isso custou detecção.

- **Partida**: `feature-wiki-v3.6.0` + `feature-test-design-v1.15.0` — a chegada de (a). Rodar (a)
  antes isola as duas fases: (a) mede o empacotamento, (d) mede o desenho.
- **Chegada**: `feature-wiki-v4.0.0` + `feature-test-design-v1.16.0`.
- **Montagem**: a de (a) — os dois cenários, o mesmo kit, o mesmo oráculo, o mesmo
  [`PROMPT-BRACO.md`](protocolo/PROMPT-BRACO.md) nas duas pontas e o mesmo juiz (prompt **e** modelo).
  Duas diferenças obrigatórias: (1) um **solicitante simulado**, com as respostas escritas **antes**
  da rodada e iguais nas duas pontas, responde às perguntas de requisito do braço de chegada; sem ele,
  a 1.16.0 deixa sem cenário toda `RQ` ambígua (`RQ-nn — aberta (Qn)`), a detecção dos defeitos
  plantados em ambiguidade cai por construção, e a comparação fica viesada. (2) Na chegada, a revisão
  adversarial roda pelo `fw-adversario-ct` com o hook instalado (`guarda-subagente.sh` em
  `.ai/skills/feature-wiki/scripts/` do projeto-cobaia), ou a rodada declara a degradação.
- **Registrar além do usual**: as perguntas que o braço de chegada fez, por raia, e as respostas
  simuladas usadas; a tabela `## Costuras de Teste` e se o `05` nasceu (costura `browser`); por
  mutante, se a `Asserção que mata` diverge de fato sob ele.
- **Pronto quando** (estudo, §8, itens 5, 6, 7 e 13): **sem regressão** em C1/C2, com a definição de
  (a) — em cada cenário, detectados na chegada ≥ detectados na partida, nenhum defeito que a partida
  detectou vira NÃO DETECTA, nenhuma lacuna cega nova.

### (e) Item 8 — custo do quality gate antes e depois

O item 8 pediu o custo do gate "medido antes/depois em `## Despachos`". A 1.7.0 trocou greps
reescritos por scripts e a dimensão I deixou de repetir o step 9 — a hipótese é que o gate ficou
mais barato —, e acrescentou o teto por cobertura e a L7. Nenhum número foi medido.

- **Partida**: `feature-quality-gate-v1.6.0` + `feature-wiki-v3.6.0` (o gate no step 8 da 3.x).
- **Chegada**: `feature-quality-gate-v1.7.0` + `feature-wiki-v4.0.0` (o gate no step 11).
- **Montagem**: a mesma feature, com a wiki e o diff iguais nas duas pontas e o app servido igual, o
  gate despachado pelo `fw-qa-gate` (`opus`) nas duas, o mesmo perfil de esforço. Host que reporta
  tokens e duração no retorno do sub-agente; sem isso, a coluna `Custo` fica `—` e a rodada não
  conta.
- **Registrar**: tokens e duração (a coluna `Custo` de `## Despachos`, nova na 4.0.0; na partida,
  anotar à mão do retorno), dimensões verificadas e não verificadas com a causa, veredito, número de
  achados por destino, o exit de cada script na chegada. É também a primeira execução do gate com o
  teto por cobertura: registrar se o veredito mudou por ele.
- **Pronto quando** (estudo, §8, item 8): "custo do gate medido antes/depois em `## Despachos`".

### (f) Item 9 — teste ao vivo do hook

O contrato do `guarda-subagente.sh` foi conferido só alimentando o script com JSON de `PreToolUse`
(e o CI repete um smoke test a cada push). Nenhum agente foi despachado com o hook ativo.

- **Partida**: `feature-wiki-v3.6.0` — o `fw-revisor-diff` sem hook, com `Read` sem restrição de
  path (estudo, §7.1 T6). O esperado é a frase do `01` aparecer: é o defeito que o item 9 corrige.
- **Chegada**: `feature-wiki-v4.0.0`, com os cinco agentes copiados de novo para `.claude/agents/`.
- **Montagem**: o procedimento do README da `feature-wiki`,
  [Teste do hook](https://github.com/gsferro/laravel-ai-skills/blob/main/.ai/skills/feature-wiki/README.md#teste-do-hook),
  numa feature com wiki: despachar o `fw-revisor-diff` sobre `{base}...HEAD` e pedir que cite a
  primeira frase do `01-plano-acao.md`; repetir pedindo `cat` do mesmo arquivo pelo `Bash` e um
  `git diff {base}...HEAD` sem a exclusão de `wikis/`; o controle renomeia o script e despacha de novo.
  O hook fica com o primeiro dos três diretórios em que acha o script, então o controle renomeia o
  `guarda-subagente.sh` **em todo lugar onde ele existe** — para achar:
  `ls .ai/skills/feature-wiki/scripts/guarda-subagente.sh .claude/skills/feature-wiki/scripts/guarda-subagente.sh ~/.claude/skills/feature-wiki/scripts/guarda-subagente.sh`.
  Com `.claude/skills/` em symlink, basta renomear em `.ai/skills/`; com cópia ou instalação global,
  renomeado só num lugar, o hook acha outra cópia e o controle não prova nada (reproduzido em fixture
  em 2026-09-27: com a cópia em `.claude/skills/`, o `Read` de `app/` saiu com exit 0, sem
  `nao encontrado`). **Caso Windows sem Git Bash**, numa máquina Windows sem Git Bash (ou com ele fora
  do PATH do Claude Code): o mesmo despacho. A documentação diz que aí os hooks rodam no PowerShell.
  O comando é `exec sh -c '…; exit 2'; exit 2`, e o `exec`, que não existe no PowerShell, leva ao
  `exit 2` do fim — medido com `pwsh -NoProfile -Command` (7.6.6) e `powershell -NoProfile -Command`
  (5.1): exit 2 num `Read` de `app/` que o bash permite. O esperado é o agente negar toda ferramenta
  (falha fechado), parar, e a sessão cair no fallback `general-purpose`. A negação vem com o erro do
  PowerShell (`exec` não reconhecido), não com o `nao encontrado`.
- **Registrar**: a versão do Claude Code, o retorno literal de cada despacho (a linha de negação do
  hook, com o perfil e o motivo), os lugares onde o script existia e onde foi renomeado no controle, o
  resultado do controle e, no caso Windows sem Git Bash: se toda ferramenta voltou negada, a mensagem
  literal da negação, se o agente parou e se a sessão caiu no fallback (a frase do `01` só pode vir
  pelo fallback, que não tem hook).
- **Pronto quando** (estudo, §8, item 9): "despachar o `fw-revisor-diff` com o `01` na pasta e pedir
  que o cite — precisa falhar", com o motivo do hook no retorno; no controle, com o script renomeado em
  todo lugar, toda ferramenta volta com `guarda-subagente.sh nao encontrado` e o agente para; o caso
  Windows sem Git Bash registrado — toda ferramenta negada e o fallback na sessão, ou o que aconteceu
  no lugar disso.

### (g) Item 12 — primeira feature entregue por tickets

- **Partida**: a feature de referência de 2026-09-21 no `demo-wiki` (18 `RQ`, 79 CT no fim, uma
  sessão, 48 despachos, ~4,6 M tokens de sub-agente; registro em
  [*Validado em campo*](https://github.com/gsferro/laravel-ai-skills/blob/main/.ai/skills/feature-wiki/references/casos-medidos.md#validado-em-campo--2026-09-21-feature-completa-no-demo-wiki)).
  É referência de tamanho, não braço de controle: a feature da chegada não é a mesma.
- **Chegada**: `feature-tickets-v1.0.0` + `feature-wiki-v4.0.0` + `feature-test-design-v1.16.0` +
  `feature-quality-gate-v1.7.0`.
- **Montagem**: uma feature que cruze um sinal do step 8 (18 ou mais `RQ` vigentes, 60 ou mais CT,
  compactação antes do step 8, mais de 30 perguntas de requisito ou refatoração larga), fatiada por
  `/feature-tickets {wiki}` e executada em pelo menos duas sessões, cada ticket numa sessão nova
  (`/feature-tickets {wiki} {NN}`), com o quality gate no fim, uma vez, sobre a feature inteira.
- **Registrar**: o sinal do step 8 que disparou; tickets, sessões e despachos; o custo por ticket
  (coluna `Custo` de `## Despachos`); se alguma sessão de ticket compactou (o sinal de ticket grande
  demais); a saída do `indice.sh --check` antes de cada despacho e no fim; a Matriz de
  Rastreabilidade do `06` com a coluna `Ticket`. É também a calibração dos limiares do step 8, que são
  hipótese: a linha `Não fatiado — …` ou `Fatiamento confirmado — …` do `03` guarda os números.
- **Pronto quando** (estudo, §8, item 12): "feature de 2 sessões entregue por tickets, com o gate no
  fim cruzando a coluna *ticket*".

## Como repetir

1. Recriar (ou reaproveitar) o projeto-cobaia com `composer create-project
   gsferro/starter-kit-easy`. A pasta `experimentos/` deste repositório **não** fica acessível ao
   braço. Reaproveitado, o projeto fica sem as pastas `exp-*` e `tests/Feature/Exp*` de outras
   rodadas: apagar antes de cada braço, não só proibir a leitura no prompt (as rodadas 8 a 13
   usaram o mesmo `demo-r8`, e a 11 é paráfrase da 10 — nota k).
2. Instalar as skills da tag medida — é o que está sendo medido:
   `git -C {repo} archive {tag} .ai/skills | tar -x -C {PROJETO}`, depois de apagar as pastas das
   quatro skills no projeto — para não sobrar arquivo de outra versão. **No Claude Code, a skill
   que o braço carrega vem de `.claude/skills/`, não de `.ai/skills/`**, e nas cobaias os
   diretórios de lá são cópias, não links (em 2026-09-26: `demo-wiki` com a `feature-wiki` 3.4.0,
   `demo-r8` com a 2.10.0). Apagar também `{PROJETO}/.claude/skills/<skill>` das quatro e espelhar
   a tag: `cp -R {PROJETO}/.ai/skills/<skill> {PROJETO}/.claude/skills/`, ou o `boost:update` com
   o `enforce_tests` definido (ver o
   [README da coletânea](../README.md#se-o-comando-terminar-com-processtimedoutexception)). No
   Claude Code, copiar os sub-agentes: `cp {PROJETO}/.ai/skills/*/agents/*.md
   {PROJETO}/.claude/agents/`. **Antes do braço**, conferir que
   `grep -Hn '^[[:space:]]*version:' {PROJETO}/.ai/skills/*/SKILL.md {PROJETO}/.claude/skills/*/SKILL.md`
   dá a mesma versão de cada skill nos dois diretórios, e anotar o `metadata.version` de cada
   `SKILL.md` instalado.
3. Copiar `protocolo/oraculo-fixo/{cenario}/` (o `00`, o `01` e, se a série o congelou, o `02`)
   para uma pasta nova `wikis/specs/exp-{n}/{feature}/`. **Nunca** regerar o `00` — ele é o
   oráculo fixo, e trocá-lo faz a rodada deixar de ser comparável com as anteriores.
4. Rodar um agente por cenário com o [`PROMPT-BRACO.md`](protocolo/PROMPT-BRACO.md), sem
   contexto compartilhado. O agente **não pode** ver o catálogo de defeitos nem as pastas `exp-*`
   das rodadas anteriores.
5. Tirar o recorte do `04`/`05` **só depois** que o agente concluir — inclusive depois da
   revisão adversarial. Recorte tirado antes contamina a medição para menos (aconteceu nas
   rodadas 2 e 3).
6. Antes do juiz, conferir o conjunto contra o catálogo:
   `grep -nE '\b[DE](0[1-9]|1[0-8])\b' 04-casos-de-teste.md 05-casos-de-teste-browser.md`.
   ID ou descrição do catálogo no conjunto anula o braço (aconteceu na rodada 8 — nota i).
7. Rodar um juiz cego por cenário com o [`PROMPT-JUIZ-CEGO.md`](protocolo/PROMPT-JUIZ-CEGO.md),
   literal: catálogo + conjunto anonimizado (`04` concatenado com o `05`). Mesmo modelo de juiz
   entre as rodadas que se comparam.
8. Arquivar em `experimentos/AAAA-MM-DD-rodada-N-{rótulo}/`: `vereditos.md` com o cabeçalho que
   o [`PROTOCOLO.md`](protocolo/PROTOCOLO.md) pede e a tabela por defeito, e `conjuntos/` com o
   `04` e o `05` **inteiros**. Resumo não é conjunto.
9. Acrescentar a linha no [Histórico](#histórico) desta página — e só aqui. README e CHANGELOG
   linkam.
10. Defeito que atravessa **os dois** braços vira regra nova na skill. Defeito que só um braço
    perdeu é variância, não lacuna.

## Prompt reutilizável

O prompt do braço vive em um lugar só: [`protocolo/PROMPT-BRACO.md`](protocolo/PROMPT-BRACO.md).
O do juiz, em [`protocolo/PROMPT-JUIZ-CEGO.md`](protocolo/PROMPT-JUIZ-CEGO.md), reusado
literalmente. Os dois servem para qualquer agente e modelo: troque os marcadores (`{PROJETO}`,
`{PASTA_ORACULO}`, `{FEATURE}`, `{PASTA_SAIDA}`, `{PERFIL}`) e cole como primeira mensagem de um
chat novo, sem contexto de rodadas anteriores.

O prompt não fixa versão de skill. A versão medida é a instalada no projeto-cobaia, e o braço
devolve o `metadata.version` de cada `SKILL.md` que leu (até a release de 2026-09-26 o campo era
`version`, no topo do frontmatter). O relatório da rodada registra os dois. O pipeline que o
prompt cobra é o atual: perfil de esforço por área, camada de componente Livewire/Filament,
cenário por fora da UI em regra de autorização e validação, e revisão adversarial obrigatória no
perfil completo ou com Impacto 3, despachada pela sessão principal.

**O bloco que esta seção trazia até 2026-09-26 foi retirado**, por três motivos:

- fixava `feature-test-design` 1.9.0 / `feature-wiki` 3.0.0 e descrevia o pipeline de agosto:
  alocação Unit/Feature/Browser sem a camada de componente Livewire, sem o gatilho de Impacto 3 e
  sem revisão adversarial. **Medir `feature-test-design` ≥ 1.14 com ele não mede a 1.14**;
- carregava pistas do catálogo e das rodadas anteriores (nota f);
- mandava o braço criar `02` e `03`, que o oráculo não tem — uma variável a mais por braço.

O texto dele continua no histórico do git (`git show daecc3f:experimentos/README.md`).

---

## Execução Local com Ollama + OpenCode

> **Nada nesta seção foi medido.** Nenhuma rodada com modelo local foi feita. Os comandos não
> foram conferidos nesta revisão (confira `opencode run --help` antes), e a tabela de expectativa
> é hipótese.

### Setup

```bash
# 1. Instalar Ollama (https://ollama.com)
# 2. Baixar modelos recomendados
ollama pull qwen2.5-coder:32b        # melhor relação qualidade/velocidade para código
ollama pull deepseek-coder-v2:16b    # alternativa MoE eficiente
ollama pull llama3.1:8b              # piso leve para teste de workflow

# 3. Instalar OpenCode (agente de código via CLI)
npm install -g @opencode-ai/cli      # ou pip install opencode-agent
```

### Modelos sugeridos por perfil

| Perfil | Modelo Ollama | Tamanho | Uso sugerido |
|---|---|---|---|
| **Forte (pago-equivalente)** | `qwen2.5-coder:32b` | 32B | Geração da wiki e CTs (qualidade próxima de frontier) |
| **Médio (custo zero)** | `deepseek-coder-v2:16b` | 16B | Revisão adversarial dos CTs |
| **Leve (piso)** | `llama3.1:8b` | 8B | Implementação do código a partir da wiki |
| **Mínimo (teste de degradação)** | `qwen2.5-coder:7b` | 7B | Medir DDR mínimo com modelos muito leves |

A `feature-test-design` manda a revisão adversarial para o modelo **mais forte** disponível.
Rodá-la num modelo local médio é desvio da skill, e a rodada precisa declará-lo.

### Comando para rodar com OpenCode

```bash
# No diretório do projeto-cobaia (demo-r8)
opencode run \
  --model ollama/qwen2.5-coder:32b \
  --prompt-file experimentos/protocolo/PROMPT-BRACO.md \
  --max-turns 50 \
  --output-dir wikis/specs/exp-local-1/
```

### Workflow híbrido sugerido (pago + local)

```
1. Modelo pago (Cascade/GPT/Claude) → gera 00-requisito.md + 01-plano-acao.md
2. Modelo pago (Cascade/GPT/Claude) → gera 04-casos-de-teste.md + 05-casos-de-teste-browser.md
3. Modelo local (Ollama + OpenCode) → implementa o código seguindo 01-plano-acao.md
4. Modelo local (Ollama + OpenCode) → executa revisão adversarial dos CTs
5. Pest executa os testes gerados em (2) contra o código implementado em (3)
```

Esse fluxo mantém a qualidade dos artefatos de design (onde a skill é dominante) e terceiriza
a codificação para modelos locais (onde o custo é zero e a qualidade do insumo já está garantida).

### Expectativa de DDR com modelos locais — hipótese, não medição

Palpite a partir do placar das rodadas 7 a 13, que tem as ressalvas das notas f, g, i e k. Não entra no
Histórico até uma rodada real.

| Modelo local | DDR esperado C1 | DDR esperado C2 | Notas |
|---|---|---|---|
| `qwen2.5-coder:32b` | 83,3% (15/18) | 100% (18/18) | Provável convergência total |
| `deepseek-coder-v2:16b` | 83,3% (15/18) | 94–100% (17–18/18) | Possível lacuna em E18 (atomicidade) |
| `llama3.1:8b` | 72–83% (13–15/18) | 83–94% (15–17/18) | Provável omissão de células da matriz |
| `qwen2.5-coder:7b` | 67–78% (12–14/18) | 78–89% (14–16/18) | Piso; testa se a skill sobrevive à degradação |

## O que já se aprendeu sobre o próprio instrumento

- **Mutation score é cego à omissão.** Duas suítes com qualidade muito diferente (7 × 12
  defeitos detectados) marcaram **100% cada** no `pest --mutate`. A técnica só muta código que
  existe, e os defeitos que separam as suítes são comportamentos **ausentes**. Score alto é piso
  de qualidade de assertion, nunca prova de cobertura de requisito. O 100% dessa medição não está
  verificado (nota h); o argumento não depende dele.
- **`covers(X::class)` restringe o que conta como coberto** — mutante em classe fora do
  `covers()` vira `uncovered` e derruba o score a 0%, mesmo com os testes executando o código.
- **`--class=` não casa de forma confiável**; o filtro que funciona é `--path=`, e exige
  `XDEBUG_MODE=coverage`. `--path=` não consta na referência de CLI do Pest.
- **Lacuna cega × lacuna declarada é mais informativa que a taxa de detecção.** Fechar uma
  lacuna declarada com um cenário que não discrimina é **piorar**: troca dívida conhecida por ✅
  falso, e ninguém volta a olhar.
- **Total igual esconde regressão.** Entre as rodadas 6 e 7 o total ficou em 33 de 36 e o C1
  perdeu dois defeitos para ganhar um. Comparação entre versões é defeito a defeito.
- **Pista no prompt é métrica de rodada anterior com outro nome.** Tamanho de matriz, lista de
  lacunas a declarar e valor discriminante no prompt do braço entregam a resposta que o juiz vai
  procurar. O prompt do braço é versionado e registrado por rodada.
- **Juiz cego não detecta conjunto contaminado.** Na rodada 8 o conjunto citava os IDs e as
  descrições do catálogo, e o juiz pontuou normalmente. A conferência contra o catálogo é um
  passo antes do juiz, não uma tarefa dele.
