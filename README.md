# Laravel AI Skills Collection 🚀

Uma coletânea de diretrizes de inteligência artificial (Skills) personalizadas para o ecossistema Laravel, focada em boas práticas de arquitetura de software e design patterns.

Estas skills servem para instruir agentes de IA e IDEs avançadas (como Claude Code, Cursor e Copilot) a gerarem códigos exatamente de acordo com os padrões definidos neste repositório.

---

## 🏗️ Estrutura do Repositório (Como criar novas Skills)

Para que o Laravel Boost e o Claude Code consigam detectar suas habilidades automaticamente, elas **devem** seguir rigorosamente a estrutura de pastas abaixo dentro do repositório:

```text
.ai/
└── skills/
    ├── nome-da-sua-skill/
    │   └── SKILL.md
    └── outra-skill/
        └── SKILL.md
```

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

Para adicionar as habilidades deste repositório diretamente no seu projeto Laravel atual, execute o comando abaixo no terminal da raiz do seu projeto:

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills
```

Isso fará o download automático de todas as pastas de habilidades para o diretório `.ai/skills/` do seu projeto. Para garantir que as atualizações locais sejam processadas, você pode rodar:

```bash
php artisan boost:update
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
| **Comunicação** (agent ↔ usuário) | Caveman | Prosa terse — corta fluff, artigos, fillers | **NÃO aplica em arquivos wiki** (01-05), código, commits, PRs |
| **Planejamento** (documentação) | feature-wiki | Define o **o quê** e o **porquê**: PRD, ADR, CTs, tracking, padrão de log, channel por feature | Arquivos wiki são detalhados por design — compressão cria ambiguidade |
| **Execução** (código) | Ponytail | Define o **como**: mínimo código possível, sem over-engineering, reutilização antes de criação | Não corta validação, segurança, tratamento de erros |
| **Revisão** (diff) | Ponytail (`/ponytail-review`) | Valida o diff contra over-engineering: o que cortar, o que substituir por stdlib | — |

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
> - `05-*.md` — Arquivos extras (rollback, performance, security) são críticos e não podem ser ambíguos.

**Onde Caveman é bem-vindo**: conversa agent ↔ usuário, resumos de progresso, perguntas e confirmações, respostas a dúvidas rápidas.

### Passo a Passo da Integração

#### 1. Instalar a skill feature-wiki no seu projeto

```bash
php artisan boost:add-skill gsferro/laravel-ai-skills
php artisan boost:update
```

Isso baixa a skill para `.ai/skills/feature-wiki/` no seu projeto Laravel.

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
│  • Criar wikis/{branch}/{feature}/ com 4 arquivos   │
│  • 01-plano-acao.md      → PRD detalhado            │
│    - Autorização, Rotas, Env, Eventos, Jobs         │
│    - Impacto, Rollback, Dependências, Riscos        │
│    - Logs em todas as etapas (channel + padrão)     │
│  • 02-decisoes-arquiteturais.md → formato ADR       │
│  • 03-progresso.md       → checklist + Blockers     │
│  • 04-casos-de-teste.md  → CTs antes do código      │
│    - CTs de log, autorização, data providers        │
│  • Revisão profunda pós-escrita                     │
│  • Confirmar plano com usuário                      │
│  ⚠️ Caveman OFF nos arquivos wiki                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. EXECUTAR (Ponytail)                             │
│  ─────────────────────────────────                  │
│  • Ponytail ativo em modo full (padrão)             │
│  • Caveman ativo na comunicação agent ↔ usuário    │
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
│  • /ponytail-review no diff atual                   │
│  • Receber lista de cortes: delete, stdlib, native, │
│    yagni, shrink                                    │
│  • Aplicar cortes sugeridos                         │
│  • /ponytail-audit se quiser varrer o repo inteiro  │
│  • /ponytail-debt para coletar atalhos `ponytail:`  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  4. TESTAR E COMMITAR                               │
│  ─────────────────────────────────                  │
│  • Rodar testes dos CTs (04-casos-de-teste.md)      │
│  • vendor/bin/pint --dirty                          │
│  • php artisan test --compact --filter={Feature}    │
│  • Commit com gitmoji + escopo                      │
│  • :memo: wiki: atualiza 03-progresso.md            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  5. PÓS-IMPLEMENTAÇÃO (feature-wiki)                │
│  ─────────────────────────────────                  │
│  • Atualizar 03-progresso.md (checkboxes + data)    │
│  • Documentar desvios do plano e notas              │
│  • Linkar wiki no PR                                │
│  • Arquivar wiki para wikis/archive/{branch}/       │
│  • Retrospectiva breve                              │
│  • Ajustar channel de log (level ou remoção)        │
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
> Após implementação, rodar `/ponytail-review` no diff.
>
> **Caveman ativo em modo `full`** na comunicação agent ↔ usuário.
> Arquivos wiki (01-05) são boundary do Caveman — escrever em prosa normal.
> Código, commits e PRs também são boundary do Caveman.
```

#### 6. Comandos do Ponytail e Caveman durante a implementação

| Comando | Quando usar |
|---------|-------------|
| `/ponytail` | Verificar modo ativo ou alternar intensidade |
| `/ponytail full` | Modo padrão — escada enforced, stdlib primeiro |
| `/ponytail ultra` | YAGNI extremo — para features simples ou refactors agressivos |
| `/ponytail lite` | Constrói o pedido mas sugere alternativa mais simples |
| `/ponytail-review` | Revisar o diff atual por over-engineering |
| `/ponytail-audit` | Auditar o repo inteiro por complexidade |
| `/ponytail-debt` | Coletar todos os `ponytail:` comments em um ledger |
| `/caveman lite\|full\|ultra` | Alternar intensidade da prosa terse |
| `stop caveman` / `normal mode` | Desativar Caveman temporariamente |

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
feature-wiki (v2.1.0)    Ponytail              Caveman
─────────────────        ─────────────────     ─────────────────
Planejamento minucioso   Execução minimalista  Comunicação terse
PRD + ADR + CTs           Escada de simplicidade  Corta fluff da prosa
Padrão de log             /ponytail-review      Auto-Clarity ativa
Channel por feature       /ponytail-debt ledger  Boundary: wiki/code
Revisão pós-escrita                              /commits = prosa normal
Pós-implementação + archive
03-progresso.md tracking
         │                    │                      │
         └────────────┬───────┴──────────────────────┘
                      ▼
          Código correto + enxuto + comunicado com terseza
          Planejado com detalhe,
          executado com o mínimo necessário,
          comunicado sem fluff
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
