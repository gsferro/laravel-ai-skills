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
| 8 | 2026-08-15 | C1, C2 | Cascade · Claude Sonnet 4 | 15/18 e 18/18 — `2026-08-15-rodada-8-cascade/vereditos.md` |
| 9 | 2026-08-15 | C1, C2 | Cascade · GLM 5.2 High | 15/18 e 18/18 — `2026-08-15-rodada-9-glm5.2-high/vereditos.md` |
| 10 | 2026-08-16 | C1, C2 | Cascade · Kimi K3 High | 15/18 e 18/18 — `2026-08-16-rodada-10-kimi-k3-high/vereditos.md` |
| 11 | 2026-08-16 | C1, C2 | Cascade · Gemini 3.7 Flash High | 15/18 e 18/18 — `2026-08-16-rodada-11-gemini/vereditos.md` |
| 12 | 2026-08-16 | C1, C2 | Cascade · GPT‑5 High Thinking | 15/18 e 18/18 — `2026-08-16-rodada-12-gpt5-high-thinking/vereditos.md` |
| 13 | 2026-08-16 | C1, C2 | Cascade · DeepSeek V4 Pro Max | 15/18 e 18/18 — `2026-08-16-rodada-13-deepseek-v4-pro-max/vereditos.md` |

**Convergência entre famílias (R7–R13):** 6 famílias de modelos (Anthropic, Zhipu, Moonshot,
Google, OpenAI, DeepSeek) produziram o mesmo DDR em ambos os cenários. A skill é o fator
dominante; o modelo influencia apenas eficiência (volume e densidade dos CTs), não eficácia
(detecção de defeitos). Modelos 2025+ convergem em 0 iterações para fechar C2.

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

## Prompt Reutilizável — Rodada Nova em Qualquer Agente/Modelo

> Copie o bloco abaixo e cole como primeira mensagem em um chat **novo** (sem contexto de
> rodadas anteriores). Substitua `{N}` pelo número da rodada e `{MODELO}` pelo nome do modelo.

```
Você é um agente de derivação de casos de teste executando a skill `feature-test-design` 1.9.0
no contexto da skill `feature-wiki` 3.0.0.

## Tarefa

Gerar os arquivos `04-casos-de-teste.md` e `05-casos-de-teste-browser.md` para DOIS cenários
independentes, usando exclusivamente os oráculos fixos fornecidos.

## Oráculos fixos (NÃO modificar — são a fonte da verdade)

### Cenário 1 — Cupons de desconto (FERRO-812)

- Requisito: `experimentos/protocolo/oraculo-fixo/cenario-1-cupons/00-requisito.md`
- Plano de ação: `experimentos/protocolo/oraculo-fixo/cenario-1-cupons/01-plano-acao.md`

### Cenário 2 — Aprovação de solicitação de compra (FERRO-830)

- Requisito: `experimentos/protocolo/oraculo-fixo/cenario-2-aprovacao/00-requisito.md`
- Plano de ação: `experimentos/protocolo/oraculo-fixo/cenario-2-aprovacao/01-plano-acao.md`

## Regras inegociáveis

1. **Derive do requisito (00), não do código.** O PRD (01) fornece nomes de métodos, rotas e
   superfície de UI — use-o como contexto, não como oráculo.
2. **Não leia os catálogos de defeitos** (`cenario-1-catalogo-defeitos.md`,
   `cenario-2-catalogo-defeitos.md`) nem os vereditos de rodadas anteriores.
3. **Não leia os arquivos `04`/`05` de rodadas anteriores** — cada rodada é independente.
4. **Aplique o pipeline completo** da `feature-test-design`:
   - Perfil de esforço por risco (P×I)
   - Varredura SFDIPOT
   - Mapa de regras (Example Mapping)
   - Técnicas formais: EP, BVA 3-valores, tabela de decisão, matriz estado × operação,
     pairwise, rastreio de efeito
   - Checklist de taxonomia de defeito
   - Cenários em Gherkin pt-BR
   - Gate de falsificabilidade (cada CT mata pelo menos um mutante plausível)
   - Alocação de camada (Unit / Feature / Browser)
5. **Matriz estado × operação em produto cartesiano fechado** para C2: 5 estados × 6 operações
   = 30 células. Toda célula inválida deve ter um CT que afirma recusa + não-efeito.
6. **Use "exatamente" nos oráculos monetários** (ex: "desconto é exatamente 2.900 centavos").
7. **Declare lacunas** quando o arnês impedir a falsificação (timezone, soft-delete, Pedido).
8. **Gherkin em pt-BR**, com `Dado`, `Quando`, `Então`, `E`, `Esquema do Cenário`, `Exemplos`.

## Saída esperada

Para cada cenário, crie os arquivos no diretório `wikis/specs/exp-{N}/{feature}/`:

- `02-decisoes-arquiteturais.md` (resumo das ADRs do PRD)
- `03-progresso.md` (checklist)
- `04-casos-de-teste.md` (casos de teste unitários e de feature)
- `05-casos-de-teste-browser.md` (casos de teste de interface)

## Contexto técnico

- Projeto Laravel 13 com Filament 5, Pest 5, multi-tenancy.
- `admin_organizacao` = papel de administrador da organização no painel `/app`.
- `panel_user` = usuário comum do negócio, sem escrita.
- Cupons: sem entidade `Pedido` — o motor recebe total em centavos e devolve total com desconto.
- Aprovação: gestor é FK (`centros_custo.gestor_id`); diretor é papel (todos notificados,
  primeira decisão resolve). Solicitante-gestora do próprio centro pode aprovar (A-09).
- Limite do diretor: R$ 5.000,00 com comparação estrita `>` (A-04).
```

### Instruções para o juiz cego (avaliação)

```
Você é um juiz cego avaliando um conjunto de casos de teste contra um catálogo de defeitos.

## Regras

1. Você recebe APENAS o catálogo de defeitos e o conjunto de CTs. Não recebe o requisito nem
   sabe qual modelo/agente gerou os CTs.
2. Um CT DETECTA um defeito se existe uma asserção explícita que MUDARIA se o defeito estivesse
   presente. Não basta "cenário genérico que passaria na mesma situação".
3. Citação literal obrigatória: cada DETECTA deve citar o CT e a asserção exata.
4. Na dúvida, NÃO DETECTA. O ônus da prova é do conjunto.
5. Classifique falhas como "lacuna declarada" (o conjunto reconhece que não cobre) ou
   "lacuna cega" (o conjunto não percebeu a omissão).
6. Output: tabela de vereditos, DDR, contagem de lacunas, falsos ✅, oráculos fracos,
   número de cenários, densidade, e caracterização da técnica.

## Catálogos de defeitos

- Cenário 1: `experimentos/protocolo/cenario-1-catalogo-defeitos.md` (18 mutantes)
- Cenário 2: `experimentos/protocolo/cenario-2-catalogo-defeitos.md` (18 mutantes)

## Conjuntos a avaliar

- Cenário 1: `experimentos/.../conjuntos/cenario-1-conjunto.md`
- Cenário 2: `experimentos/.../conjuntos/cenario-2-conjunto.md`
```

---

## Execução Local com Ollama + OpenCode

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

### Comando para rodar com OpenCode

```bash
# No diretório do projeto-cobaia (demo-r8)
opencode run \
  --model ollama/qwen2.5-coder:32b \
  --prompt-file experimentos/protocolo/PROMPT-AGENTE.md \
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

### Expectativa de DDR com modelos locais

Com base nos resultados das 7 rodadas (skill domina, modelo influencia eficiência):

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
  de qualidade de assertion, nunca prova de cobertura de requisito.
- **`covers(X::class)` restringe o que conta como coberto** — mutante em classe fora do
  `covers()` vira `uncovered` e derruba o score a 0%, mesmo com os testes executando o código.
- **`--class=` não casa de forma confiável**; o filtro que funciona é `--path=`, e exige
  `XDEBUG_MODE=coverage`.
- **Lacuna cega × lacuna declarada é mais informativa que a taxa de detecção.** Fechar uma
  lacuna declarada com um cenário que não discrimina é **piorar**: troca dívida conhecida por ✅
  falso, e ninguém volta a olhar.
