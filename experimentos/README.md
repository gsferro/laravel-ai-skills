# Experimentos — medição empírica das skills

Esta pasta guarda **as medições** que motivaram as versões das skills desta coletânea, e o
material necessário para **repetir a medição** a cada evolução relevante.

> Regra da casa: skill não evolui por releitura de escrivaninha. Evolui por defeito que
> atravessou os dois braços de um experimento cego. Cada versão publicada precisa ter um
> gatilho medido nesta pasta.

## Estrutura

```
experimentos/
├── protocolo/                      # o que se reusa a cada rodada
│   ├── PROTOCOLO.md                # a definição do experimento e das métricas
│   ├── cenario-1-requisito.md      # card FERRO-812 (cálculo/valor — cupons)
│   ├── cenario-1-catalogo-defeitos.md   # 18 mutantes + 9 ambiguidades plantadas
│   ├── cenario-2-requisito.md      # card FERRO-830 (máquina de estados — aprovação)
│   ├── cenario-2-catalogo-defeitos.md   # 18 mutantes + 9 ambiguidades plantadas
│   └── oraculo-fixo/               # 00-requisito.md e 01-plano-acao.md congelados
│       ├── cenario-1-cupons/
│       └── cenario-2-aprovacao/
├── 2026-08-14-defeitos-plantados/  # rodadas 1 a 4
│   ├── relatorio.html              # o relatório completo (abrir no navegador)
│   ├── anexo-correcoes-factuais.md
│   └── conjuntos/                  # os arquivos 04 julgados em cada rodada
└── 2026-08-15-rodada-5/            # rodada 5 — ver o README de lá
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

Dois cenários bastam para não superajustar: um de **cálculo/valor** e um de **máquina de
estados** — eles falham por motivos diferentes.

## Ambiente

Projeto-cobaia descartável criado com `composer create-project gsferro/starter-kit-easy`
(Laravel 13 · Filament 5 · Pest 5 com browser e mutate · Xdebug em modo `coverage`).
Em 2026-08-14/15 ficou em `D:\PROJECTS\SKILLS\demo-wiki`, com as rodadas em
`wikis/specs/exp-a` … `exp-e`.

O kit é a cobaia certa por dois motivos: já traz as skills em `.ai/skills/`, e traz **wikis
reais** em `wikis/specs/` produzidas pela própria `feature-wiki` em produção — o que permite
auditoria forense da saída real, não só teste sintético.

## Histórico

| Rodada | Data | Cenários | Versões medidas | Resultado |
|---|---|---|---|---|
| Baseline | 2026-08-14 | C1, C2 | `feature-wiki` 2.10.0 (sem skill de derivação) | 7/18 e 11/18 |
| 1 | 2026-08-14 | C1, C2 | `feature-test-design` 1.0.0 | 12/18 e 17/18 |
| 3 | 2026-08-14 | C1 | 1.3.0 | 16/18 |
| 4 | 2026-08-15 | C1, C2 | 1.5.0 | ver `2026-08-14-defeitos-plantados/relatorio.html` |
| 5 | 2026-08-15 | C1, C2 | `feature-wiki` 3.0.0 · `feature-test-design` 1.7.0 | 14/18 e 17/18 — `2026-08-15-rodada-5/vereditos.md` |
| 6 | 2026-08-15 | C1, C2 | `feature-wiki` 3.0.0 · `feature-test-design` 1.8.0 | 16/18 e 17/18 — `2026-08-15-rodada-6/vereditos.md` |
| 7 | 2026-08-15 | C1, C2 | `feature-wiki` 3.0.0 · `feature-test-design` 1.9.0 | 15/18 e 18/18 — `2026-08-15-rodada-7/vereditos.md` |

Na rodada 5, as quatro regras que ainda não tinham sido medidas (1.4.0 a 1.7.0) mataram cada uma
o defeito que a originou. O que sobrou foi **deslocamento de orçamento**: três lacunas cegas
novas, em dois cenários e dois juízes independentes, todas na mesma assinatura — o conjunto
esgota os eixos **valor** e **ator** e assume o eixo **mecanismo/estado**.

## Como repetir

1. Recriar (ou reaproveitar) o projeto-cobaia e **sincronizar `.ai/skills/` com as versões do
   repo** — é o que está sendo medido.
2. Copiar `protocolo/oraculo-fixo/{cenario}/00-requisito.md` e `01-plano-acao.md` para uma pasta
   nova `wikis/specs/exp-{n}/{feature}/`. **Nunca** regerar o `00` — ele é o oráculo fixo, e
   trocá-lo faz a rodada deixar de ser comparável com as anteriores.
3. Rodar um agente por cenário, sem contexto compartilhado, entrando no **step 4** da
   `feature-wiki`. O agente **não pode** ver o catálogo de defeitos nem as pastas `exp-*` das
   rodadas anteriores.
4. Tirar o recorte do `04`/`05` **só depois** que o agente concluir — inclusive depois da
   revisão adversarial. Recorte tirado antes contamina a medição para menos (aconteceu nas
   rodadas 2 e 3).
5. Rodar um juiz cego por cenário, com o catálogo e o conjunto anonimizado.
6. Defeito que atravessa **os dois** braços vira regra nova na skill. Defeito que só um braço
   perdeu é variância, não lacuna.

## O que já se aprendeu sobre o próprio instrumento

- **Mutation score é cego à omissão.** Duas suítes com qualidade muito diferente (7 × 12
  defeitos detectados) marcaram **100% cada** no `pest --mutate`. A técnica só muta código que
  existe, e os defeitos que separam as suítes são comportamentos **ausentes**. Score alto é piso
  de qualidade de assertion, nunca prova de cobertura de requisito.
- **`covers(X::class)` restringe o que conta como coberto** — mutante em classe fora do
  `covers()` vira `uncovered` e derruba o score a 0%, mesmo com os testes executando o código.
- **`--class=` não casa de forma confiável**; o filtro que funciona é `--path=`, e exige
  `XDEBUG_MODE=coverage`.
- **Lacuna cega × lacuna declarada é mais informativa que a taxa de detecção.** Fechar uma
  lacuna declarada com um cenário que não discrimina é **piorar**: troca dívida conhecida por ✅
  falso, e ninguém volta a olhar.
