<p align="center">
  <img src="art/banner.png" alt="Laravel AI Skills Collection" width="100%">
</p>

# Laravel AI Skills Collection 🚀

Uma coletânea de diretrizes de inteligência artificial (Skills) personalizadas para o ecossistema Laravel, focada em boas práticas de arquitetura de software e design patterns.

Estas skills servem para instruir agentes de IA e IDEs avançadas (como Claude Code, Cursor e Copilot) a gerarem códigos exatamente de acordo com os padrões definidos neste repositório.

## 📚 Skills desta coletânea

| Skill | Versão | O que faz | Quando é invocada |
|---|---|---|---|
| **[feature-wiki](.ai/skills/feature-wiki/README.md)** | 2.10.0 | Cria a wiki da feature antes de implementar: requisito bruto, PRD, ADR, progresso e casos de teste (backend e browser), com padrão de log | ao iniciar qualquer feature nova |
| **[feature-quality-gate](.ai/skills/feature-quality-gate/README.md)** | 1.0.0 | **QA no agente**: confronta requisito × plano × app rodando, detecta omissão silenciosa e roteia cada achado para especificação, implementação ou teste | step 8 da `feature-wiki`, após os testes passarem |
| **[requirement-to-rule](.ai/skills/requirement-to-rule/README.md)** | 1.1.0 | Transforma decisão/restrição do requisito em **Project Rule** do Laravel Boost (`.ai/rules/`), com aprovação do usuário | step 9 da `feature-wiki` ou sob pedido |

O ciclo completo: **planejar** (`feature-wiki`) → **executar** (Ponytail) → **comunicar** (Caveman) → **testar** (Pest 5 + CT-B) → **validar** (`feature-quality-gate`) → **memorizar** (`requirement-to-rule`).

### Onde está cada documentação

Cada skill tem **dois arquivos com públicos diferentes** — o `README.md` explica para a pessoa; o `SKILL.md` instrui o agente. Procedimento não é duplicado entre eles.

| Skill | Para você ler | Para o agente seguir |
|---|---|---|
| feature-wiki | [README](.ai/skills/feature-wiki/README.md) — requisito, CT-B, Pest 5, `search-docs`, dependências | [SKILL.md](.ai/skills/feature-wiki/SKILL.md) |
| feature-quality-gate | [README](.ai/skills/feature-quality-gate/README.md) — uso + **estudo de viabilidade** (pesquisa de mercado, lacuna verificada, critério eliminatório) | [SKILL.md](.ai/skills/feature-quality-gate/SKILL.md) |
| requirement-to-rule | [README](.ai/skills/requirement-to-rule/README.md) — 4 gates, escada de enforcement, índice de rules | [SKILL.md](.ai/skills/requirement-to-rule/SKILL.md) |

> Histórico de evolução das skills: [CHANGELOG.md](CHANGELOG.md)

---

## 🏗️ Estrutura do Repositório (Como criar novas Skills)

Para que o Laravel Boost e o Claude Code consigam detectar suas habilidades automaticamente, elas **devem** seguir rigorosamente a estrutura de pastas abaixo dentro do repositório:

```text
.ai/
└── skills/
    ├── nome-da-sua-skill/
    │   ├── SKILL.md      ← obrigatório: instruções para o agente
    │   └── README.md     ← opcional: explicação para a pessoa
    └── outra-skill/
        └── SKILL.md
```

**Convenção desta coletânea**: cada skill tem os dois arquivos, com públicos distintos.

| Arquivo | Público | Conteúdo | Custo de contexto |
|---|---|---|---|
| `SKILL.md` | **agente** | procedimento, gates, templates, comandos, proibições | carregado on-demand pelo agente |
| `README.md` | **pessoa** | por que existe, vantagens, escopo, dependências, limitações | **zero** — o Boost e o Claude Code leem só o `SKILL.md` |

A regra que evita duplicação: **procedimento vive apenas no `SKILL.md`**. O `README.md` explica o *porquê* e o *quando*, nunca repete o *como*.

### Regras importantes para o arquivo `SKILL.md`:
Todo arquivo `SKILL.md` precisa começar obrigatoriamente com um cabeçalho **YAML** delimitado por `---`. É isso que descreve a habilidade para a inteligência artificial.

**Exemplo prático de um arquivo `SKILL.md`:**
```markdown
---
name: Form Requests Padronizados
description: Diretrizes para validação de dados usando Form Requests isolados no domínio do projeto.
---

# Diretrizes da Skill
- Sempre utilize o comando `php artisan make:request`.
- Nunca faça validações diretamente dentro das Controllers.
- Adicione mensagens de erro customizadas no método `messages()`.
```

---

## ⚙️ Como Instalar no Laravel Boost 2.0

Para instalar **todas as skills de uma vez**, sem prompt de seleção, execute na raiz do seu projeto Laravel:

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills --all
```

Isso baixa as três skills para o diretório `.ai/skills/` do seu projeto. Em seguida, para que o Boost processe as atualizações locais:

```bash
php artisan boost:update
```

### Instalação seletiva

Sem o `--all`, o comando abre um prompt para você escolher quais skills instalar:

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills
```

Ou escolha direto pelo nome (o `--skill` aceita repetição):

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills \
  --skill=feature-wiki --skill=feature-quality-gate
```

> **Atenção**: as três skills são encadeadas. A `feature-quality-gate` **exige** a `feature-wiki` ≥ 2.10.0, porque depende do `00-requisito.md` que ela cria. Instalar só a `feature-quality-gate` não funciona.

### Todas as opções do `boost:add-skill`

| Opção | O que faz |
|---|---|
| `--all` | instala todas as skills do repositório, sem prompt |
| `--list` | apenas lista as skills disponíveis, sem instalar |
| `--skill=NOME` | instala skills específicas (repetível) |
| `--force` | sobrescreve skills já existentes |
| `--skip-audit` | pula a auditoria de segurança do Boost |

Assinatura completa:

```text
php artisan boost:add-skill [--list] [--all] [--skill [SKILL]] [--force] [--skip-audit] [--] [<repo>]
```

> Após instalar, veja [Padrão de Commit](#-padrão-de-commit-ao-instalaratualizar-skills).    

---

## 🤖 Como Instalar no Claude Code

Você pode disponibilizar e carregar essas diretrizes no **Claude Code** através de três abordagens diferentes:

### Opção 1: Uso Local por Projeto (Recomendado)
Se você já executou o comando do Laravel Boost acima no seu projeto, basta criar um espelho das configurações para que o Claude Code dê prioridade a elas no repositório local:

```bash
mkdir -p .claude/skills/
cp -R .ai/skills/* .claude/skills/
```

### Opção 2: Instalação Global no Sistema
Para que o Claude Code use estas regras de arquitetura em **qualquer diretório** que você abrir na sua máquina, instale a pasta de skills diretamente no seu perfil de usuário:

* **Linux / macOS:**
  ```bash
  mkdir -p ~/.claude/skills/
  # Clone o repositório e mova o conteúdo para a pasta global
  cp -R .ai/skills/* ~/.claude/skills/
  ```
* **Windows (PowerShell):**
  ```powershell
  New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills"
  Copy-Item -Path ".\.ai\skills\*" -Destination "$HOME\.claude\skills" -Recururse
  ```

### Opção 3: Via Gerenciador de Plugins (Prompt Interativo)
Se você estiver executando o Claude Code em modo interativo de terminal, pode registrar o repositório como um marketplace de plugins:

```text
/plugin marketplace add gsferro/laravel-ai-skills
/plugin install
```

---

## 📌 Padrão de Commit ao Instalar/Atualizar Skills

Ao baixar ou atualizar skills deste repositório no seu projeto, use o padrão de commit abaixo para manter o histórico rastreável:

### Instalação (primeira vez)

```
:package: skills: instala {nome-da-skill} do laravel-ai-skills

- Origem: https://github.com/gsferro/laravel-ai-skills
- Versão/commit: {sha-curto ou tag}
```

### Atualização

```
:arrow_up: skills: atualiza {nome-da-skill} do laravel-ai-skills

- Origem: https://github.com/gsferro/laravel-ai-skills
- De: {sha-anterior} → Para: {sha-novo}
- Mudanças relevantes: {resumo em 1 linha}
```

### Exemplos

```
:package: skills: instala feature-wiki do laravel-ai-skills
:arrow_up: skills: atualiza feature-wiki do laravel-ai-skills
```

> Instalando/atualizando várias skills de uma vez, use o escopo `skills` no plural
> e liste cada uma no corpo do commit.

Ajustes possíveis: se quiser manter só os gitmojis do seu padrão interno (sem :package:/:arrow_up:), troque por :sparkles: (instala) e :recycle: (atualiza).


---
## 🐴 Integração com Ponytail + 🦴 Caveman (Planejar → Executar → Comunicar com Mínimo Esforço)

### O que é o Ponytail?

**Ponytail** ([github.com/DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)) é uma skill de execução que faz o agente de IA pensar como o **dev sênior mais preguiçoso da sala** — no bom sentido. Antes de escrever qualquer código, o agente sobe uma "escada de simplicidade":

1. **Isso precisa existir?** (YAGNI) → se não, skip
2. **Já existe no codebase?** → reutiliza, não reescreve
3. **A stdlib faz?** → usa
4. **Feature nativa da plataforma cobre?** → usa (`<input type="date">` em vez de lib de datepicker)
5. **Dependência já instalada resolve?** → usa
6. **Pode ser uma linha?** → uma linha
7. **Só então:** o mínimo de código que funciona

O Ponytail **nunca** corta validação de input em fronteiras de confiança, tratamento de erros que previne perda de dados, segurança ou acessibilidade. Preguiça na solução, nunca na leitura do problema.

### O que é o Caveman?

**Caveman** ([github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)) é uma skill de comunicação que corta ~75% dos tokens na prosa do agente — removendo artigos, fillers, pleasantries e hedging — mantendo precisão técnica. Tem níveis de intensidade (lite/full/ultra) e regras de Auto-Clarity que desativam o modo terse em situações críticas.

O próprio Ponytail recomenda o pareamento: *"Ponytail governs what you build, not how you talk (pair with Caveman for terse prose)"*.

- **Caveman** → prosa. Corta fluff da comunicação.
- **Ponytail** → código. Corta over-engineering da solução.

### Por que feature-wiki, Ponytail e Caveman trabalham bem juntas

A integração é natural porque as três skills operam em **camadas complementares** do ciclo de desenvolvimento:

| Camada | Skill | Responsabilidade | Boundary |
|--------|-------|------------------|----------|
| **Comunicação** (agent ↔ usuário) | Caveman | Prosa terse — corta fluff, artigos, fillers | **NÃO aplica em arquivos wiki** (00-06), código, commits, PRs |
| **Planejamento** (documentação) | feature-wiki | Define o **o quê** e o **porquê**: PRD, ADR, CTs, tracking, padrão de log, channel por feature | Arquivos wiki são detalhados por design — compressão cria ambiguidade |
| **Execução** (código) | Ponytail | Define o **como**: mínimo código possível, sem over-engineering, reutilização antes de criação | Não corta validação, segurança, tratamento de erros |
| **Revisão** (diff) | Ponytail (`/ponytail:ponytail-review`) | Valida o diff contra over-engineering: o que cortar, o que substituir por stdlib | — |

O Ponytail diz *"leia o problema completamente antes de escolher o rung mais preguiçoso"*. A feature-wiki **é** essa leitura profunda — ela força o agente a pesquisar o codebase, validar premissas, inspecionar APIs e escrever casos de teste **antes** de tocar em código. Quando o Ponytail assume a execução, o agente já tem contexto completo da wiki e pode aplicar a escada de simplicidade com confiança, sem risco de "preguiça que pula compreensão". O Caveman mantém a comunicação terse durante toda a sessão — mas respeita o boundary dos arquivos wiki.

Sem a feature-wiki, o Ponytail pode escolher o rung errado por falta de contexto. Sem o Ponytail, a feature-wiki pode produzir um plano detalhado que o agente super-engineering na implementação. Sem o Caveman, a sessão perde tokens com fluff na prosa. Juntas: **planejamento minucioso + execução minimalista + comunicação terse**.

### Boundary do Caveman em arquivos wiki

O Caveman tem Auto-Clarity que desativa o modo terse em situações críticas. Mas a feature-wiki torna explícito:

> **Arquivos wiki são boundary do Caveman.**
>
> - `01-plano-acao.md` — PRD precisa ser "minucioso o suficiente para um agente implementar sem ambiguidade". Compressão destrói essa propriedade.
> - `02-decisoes-arquiteturais.md` — ADR é argumentativo por natureza. Fragmentos perdem o raciocínio.
> - `03-progresso.md` — Checklists e descrições de blockers/desvios precisam de clareza.
> - `04-casos-de-teste.md` — CTs já são estruturados, mas a prosa explicativa não deve ser comprimida.
> - `05-casos-de-teste-browser.md` — o roteiro de CT-B é seguido passo a passo por humano ou agente; ambiguidade aqui invalida a auditoria.
> - `05-*.md` — Arquivos extras (rollback, performance, security) são críticos e não podem ser ambíguos.

**Onde Caveman é bem-vindo**: conversa agent ↔ usuário, resumos de progresso, perguntas e confirmações, respostas a dúvidas rápidas.

### Passo a Passo da Integração

#### 1. Instalar as skills desta coletânea no seu projeto

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills --all
php artisan boost:update
```

Isso baixa `feature-wiki`, `feature-quality-gate` e `requirement-to-rule` para `.ai/skills/` no seu projeto Laravel.

#### 2. Instalar o Ponytail e o Caveman no seu agente de IA

Escolha **uma** das opções abaixo conforme o agente que você usa:

**Claude Code:**
```text
/plugin marketplace add DietrichGebert/ponytail
```
Depois, em um segundo prompt:
```text
/plugin install ponytail@ponytail
```

**Windsurf / Cursor / Cline:**
Copie o arquivo de regras do Ponytail para a pasta do seu agente:
```bash
# Windsurf
curl -o .windsurf/rules/ponytail.md https://raw.githubusercontent.com/DietrichGebert/ponytail/main/.windsurf/rules/ponytail.md

# Cursor
curl -o .cursor/rules/ponytail.md https://raw.githubusercontent.com/DietrichGebert/ponytail/main/.cursor/rules/ponytail.mdc

# Cline
curl -o .clinerules/ponytail.md https://raw.githubusercontent.com/DietrichGebert/ponytail/main/.clinerules/ponytail.md
```

**GitHub Copilot (editor):**
```bash
curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/DietrichGebert/ponytail/main/.github/copilot-instructions.md
```

**AGENTS.md (universal — CodeWhale, Codex, VS Code):**
```bash
curl -o AGENTS.md https://raw.githubusercontent.com/DietrichGebert/ponytail/main/AGENTS.md
```

**Caveman — Claude Code:**
```text
/plugin marketplace add JuliusBrussee/caveman
```
Depois, em um segundo prompt:
```text
/plugin install caveman@caveman
```

**Caveman — Windsurf / Cursor / Cline:**
```bash
# Windsurf
curl -o .windsurf/rules/caveman.md https://raw.githubusercontent.com/JuliusBrussee/caveman/main/.windsurf/rules/caveman.md

# Cursor
curl -o .cursor/rules/caveman.md https://raw.githubusercontent.com/JuliusBrussee/caveman/main/.cursor/rules/caveman.mdc

# Cline
curl -o .clinerules/caveman.md https://raw.githubusercontent.com/JuliusBrussee/caveman/main/.clinerules/caveman.md
```

#### 3. Espelhar a skill feature-wiki para o Claude Code (se aplicável)

Se você usa Claude Code junto com Laravel Boost:

```bash
mkdir -p .claude/skills/
cp -R .ai/skills/* .claude/skills/
```

#### 4. Fluxo de trabalho integrado

A partir de agora, para cada feature nova:

```
┌─────────────────────────────────────────────────────┐
│  1. PLANEJAR (feature-wiki)                         │
│  ─────────────────────────────────                  │
│  • Invocar feature-wiki ao iniciar a feature        │
│  • Criar wikis/specs/{branch}/{feature}/ com 5 arqs  │
│  • 00-requisito.md       → requisito bruto IMUTÁVEL  │
│    - Decomposição em cláusulas RQ-##                │
│    - Ambiguidades = pergunta, não suposição         │
│  • 01-plano-acao.md      → PRD detalhado            │
│    - Natureza da wiki + Cobertura do Requisito      │
│    - Autorização, Rotas, Env, Eventos, Jobs         │
│    - Impacto, Rollback, Dependências, Riscos        │
│    - Logs em todas as etapas (channel + padrão)     │
│  • 02-decisoes-arquiteturais.md → formato ADR       │
│  • 03-progresso.md       → checklist + Blockers     │
│  • 04-casos-de-teste.md  → CTs antes do código      │
│    - CTs de log, autorização, data providers        │
│  • 05-casos-de-teste-browser.md → CT-B (se tem UI)  │
│    - Gate: ## Superfície de UI no 01 + JS/multi-tela│
│    - + roteiro Desenhado × Implementado             │
│  • Revisão profunda pós-escrita                     │
│  • Auditoria da wiki: /ponytail:ponytail-review     │
│  • Confirmar plano com usuário                      │
│  ⚠️ Caveman OFF nos arquivos wiki                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. EXECUTAR (Ponytail)                             │
│  ─────────────────────────────────                  │
│  • Ponytail ativo em modo full (padrão)             │
│  • Caveman ativo (ultra) na comunicação c/ usuário  │
│  • Seguir o 01-plano-acao.md passo a passo          │
│  • Aplicar a escada de simplicidade em cada passo:  │
│    - Reutilizar antes de criar                      │
│    - Stdlib antes de código custom                  │
│    - Feature nativa antes de dependência            │
│    - Uma linha quando possível                      │
│  • Marcar atalhos com `ponytail:` comment           │
│  • Atualizar 03-progresso.md em tempo real          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. REVISAR (Ponytail-review)                       │
│  ─────────────────────────────────                  │
│  • /ponytail:ponytail-review no diff atual           │
│  • Receber lista de cortes: delete, stdlib, native, │
│    yagni, shrink                                    │
│  • Aplicar cortes sugeridos                         │
│  • /ponytail:ponytail-audit se quiser varrer o repo  │
│  • /ponytail:ponytail-debt para coletar atalhos      │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  4. TESTAR E COMMITAR                               │
│  ─────────────────────────────────                  │
│  • Rodar testes dos CTs (04-casos-de-teste.md)      │
│  • vendor/bin/pint --dirty                          │
│  • vendor/bin/pest --filter={Feature} --compact     │
│  • vendor/bin/pest tests/Browser (se houver CT-B)   │
│  • vendor/bin/pest --tia → confirma impacto real    │
│  • Commit com gitmoji + escopo                      │
│  • :memo: wiki: atualiza 03-progresso.md            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  5. PÓS-IMPLEMENTAÇÃO (feature-wiki)                │
│  ─────────────────────────────────                  │
│  • Atualizar 03-progresso.md (checkboxes + data)    │
│  • CT-B via sub-agente em loop (máx. 3 iterações)   │
│    - Preencher Desenhado × Implementado             │
│  • Documentar desvios do plano e notas              │
│  • Linkar wiki no PR                                │
│  • Retrospectiva breve                              │
│  • Ajustar channel de log (level ou remoção)        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  6. VALIDAR (feature-quality-gate)                  │
│  ─────────────────────────────────                  │
│  • Confronta 00-requisito × PRD × app rodando       │
│  • Audita ambiguidades do requisito PRIMEIRO        │
│  • Matriz de Rastreabilidade → omissão silenciosa   │
│  • 10 dimensões (perfil por risco: mín/padrão/full) │
│  • Roteia achado: especificação | código | teste    │
│  • Escreve 06-relatorio-qa.md + veredito            │
│  ⚠️ NÃO corrige nada · teto de 3 ciclos             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  7. MEMORIZAR (requirement-to-rule)                 │
│  ─────────────────────────────────                  │
│  • Varrer ADRs + Notas + PRD por candidatos a rule  │
│  • Aplicar os 4 gates: durável, escopável,          │
│    não-inferível, não-redundante                    │
│  • Preferir enforcement (pest --arch) à prosa       │
│  • APRESENTAR ao usuário — decisão é dele           │
│  • Se aprovado: gravar via record-rule (Boost)      │
│  • Commitar .ai/rules/ (artefato de equipe)         │
│  ⚠️ Teto: 3 rules por feature                       │
└─────────────────────────────────────────────────────┘
```

#### 5. Referenciar o Ponytail e o Caveman no PRD da feature-wiki

Ao escrever o `01-plano-acao.md`, incluir uma nota de filosofia de implementação:

```markdown
## Filosofia de Implementação

> **Ponytail ativo em modo `full`** durante toda a implementação.
> Cada passo deve aplicar a escada de simplicidade:
> 1. Reutilizar código existente antes de criar novo
> 2. Usar stdlib do PHP/Laravel antes de código custom
> 3. Usar features nativas (ex: `input[type=date]`) antes de dependências
> 4. Uma linha quando possível
> 5. Mínimo código que funciona
>
> Atalhos deliberados devem ser marcados com `ponytail:` comment.
> Após implementação, rodar `/ponytail:ponytail-review` no diff.
>
> **Caveman ativo em modo `ultra`** (padrão) na comunicação agent ↔ usuário.
> Arquivos wiki (00-06) são boundary do Caveman — escrever em prosa normal.
> Código, commits e PRs também são boundary do Caveman.
```

#### 6. Comandos do Ponytail e Caveman durante a implementação

| Comando | Quando usar |
|---------|-------------|
| `/ponytail:ponytail` | Verificar modo ativo ou alternar intensidade |
| `/ponytail:ponytail full` | Modo padrão — escada enforced, stdlib primeiro |
| `/ponytail:ponytail ultra` | YAGNI extremo — para features simples ou refactors agressivos |
| `/ponytail:ponytail lite` | Constrói o pedido mas sugere alternativa mais simples |
| `/ponytail:ponytail-review` | Revisar o diff atual por over-engineering |
| `/ponytail:ponytail-audit` | Auditar o repo inteiro por complexidade |
| `/ponytail:ponytail-debt` | Coletar todos os `ponytail:` comments em um ledger |
| `/caveman:caveman ultra` | **Modo padrão** — compressão máxima da prosa |
| `/caveman:caveman lite\|full\|ultra` | Alternar intensidade da prosa terse |
| `/caveman:caveman off` / `stop caveman` | Desativar Caveman temporariamente |

> ⚠️ **Namespace obrigatório no Claude Code**: comandos vindos de plugin exigem o prefixo `{plugin}:` — `/caveman:caveman` e `/ponytail:ponytail`. Sem o namespace (`/caveman`, `/ponytail-review`) o comando não é encontrado.
>
> Os READMEs upstream documentam `/caveman` e `/ponytail` sem prefixo porque cobrem também a instalação via arquivo de regras (Windsurf / Cursor / Cline), onde não existe namespace de plugin. Se você instalou via `/plugin install caveman@caveman`, use sempre `/caveman:caveman`. O mesmo vale para os demais comandos do plugin: `/caveman:caveman-review`, `/caveman:caveman-stats`, `/caveman:caveman-init`.

#### 7. Configurar modo padrão do Ponytail (opcional)

Defina o modo padrão para todas as sessões novas:

**Variável de ambiente:**
```bash
export PONYTAIL_DEFAULT_MODE=full
```

**Arquivo de config:**
- **Linux/macOS:** `~/.config/ponytail/config.json`
- **Windows:** `%APPDATA%\ponytail\config.json`

```json
{ "defaultMode": "full" }
```

### Resumo da Integração

```
feature-wiki (v2.10.0)   Ponytail              Caveman
─────────────────        ─────────────────     ─────────────────
Planejamento minucioso   Execução minimalista  Comunicação terse
00-requisito (oráculo)    Escada de simplicidade  Corta fluff da prosa
PRD + ADR + CTs           /ponytail:ponytail-review  Auto-Clarity ativa
CT-B (browser, se UI)     /ponytail:ponytail-debt    Boundary: wiki/code
Padrão de log                                    /commits = prosa normal
Revisão pós-escrita
Pest 5: --parallel --tia
03-progresso.md tracking

feature-quality-gate (v1.0.0)      requirement-to-rule (v1.1.0)
─────────────────                  ─────────────────
Requisito × plano × app rodando    Decisão da wiki → .ai/rules/
Omissão silenciosa (Matriz)        4 gates + aprovação do usuário
10 dimensões, perfil por risco     Gravado via record-rule (Boost)
Roteia: spec | código | teste      Índice .ai/rules/index.md
Não corrige · teto de 3 ciclos
         │                    │                      │
         └────────────┬───────┴──────────────────────┘
                      ▼
          Código correto + enxuto + comunicado com terseza
          Planejado com detalhe,
          executado com o mínimo necessário,
          comunicado sem fluff
```

---

## 📖 Documentação detalhada

Este README é o índice da coletânea. O detalhe de cada skill vive com ela:

| Documento | O que você encontra |
|---|---|
| [**feature-wiki**](.ai/skills/feature-wiki/README.md) | como informar o requisito (card colado, `.pdf`/`.docx`/`.md`), os 6 arquivos da wiki, testes de browser com Pest + Playwright, o que o Pest 5 trouxe (`--parallel --tia`, `--agent`), Playwright MCP como observação, `search-docs` e suas lacunas, dependências e limitações conhecidas |
| [**feature-quality-gate**](.ai/skills/feature-quality-gate/README.md) | uso da skill (omissão silenciosa, 10 dimensões, roteamento de 5 destinos) **e** o estudo de viabilidade completo: pesquisa de mercado, lacuna verificada, achados técnicos e critério eliminatório |
| [**requirement-to-rule**](.ai/skills/requirement-to-rule/README.md) | as três camadas (guidelines × skills × rules), os 4 gates, escada de enforcement, índice `.ai/rules/index.md`, modelo base da rule e anti-padrões |
| [**CHANGELOG.md**](CHANGELOG.md) | histórico de evolução das três skills, com versionamento independente e convenção de tags |

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
