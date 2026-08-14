---
name: requirement-to-rule
version: 1.0.0
description: >
  Transforma decisões e restrições de um requisito em Project Rules do Laravel Boost
  (.ai/rules/). Invoque quando uma decisão precisar valer para agentes futuros em
  qualquer sessão — não só na wiki da feature atual. Valida cada candidato contra
  4 gates (durável, escopável por path, não-inferível, não-redundante), deduplica
  contra o index existente, exige aprovação explícita do usuário e grava sempre via
  a tool MCP record-rule do Boost. Complementa a feature-wiki (step 8) e o
  infer-conventions do Boost: aquele varre o código existente, este parte do requisito.
---

# Requirement → Rule — Decisão do Requisito Vira Regra Durável

## Glossário

| Sigla | Significado |
|-------|-------------|
| **Rule** | Project Rule do Boost — arquivo em `.ai/rules/*.md` escopado por glob de path |
| **ADR** | Architecture Decision Record — decisão registrada na wiki da feature |
| **PRD** | Product Requirements Document — plano de ação da feature |
| **Guideline** | Instrução do Boost sobre o **ecossistema** (Laravel, Livewire, Pest), carregada upfront |
| **Skill** | Módulo de conhecimento carregado on-demand por tarefa |

## As três camadas — não confundir

| Camada | Ensina | Carregamento | Quem mantém |
|--------|--------|--------------|-------------|
| **Guidelines** (`.ai/guidelines/`) | como escrever **Laravel** | upfront, sempre | Boost (`boost:update`) |
| **Skills** (`.ai/skills/`) | padrões de um **domínio/tarefa** | on-demand | Boost + você |
| **Rules** (`.ai/rules/`) | como escrever **a sua aplicação** | por glob, quando o arquivo casa | **você**, versionado no git |

> **Regra de ouro**: conhecimento de ecossistema **nunca** vira rule. O Boost já cobre e atualiza isso via `boost:update`; a sua rule apodreceria na próxima versão do framework. Rule é só o que é **específico da sua aplicação**.

## Quando Invocar

- Step 8 da skill `feature-wiki` identificou candidatos a rule e o usuário aprovou
- O usuário disse explicitamente "isso vira rule", "lembre disso para sempre", "todo agente precisa saber disso"
- Uma ADR foi aceita e a consequência dela vale para código futuro fora da feature
- Uma armadilha foi descoberta em implementação e outro agente cairia nela

### Quando NÃO Invocar

- **Decisão de uma feature só**: fica na ADR. Rule é para o que atravessa features.
- **Conhecimento de framework**: "usar Form Request para validação" — já está nas guidelines do Boost.
- **Coisa que linter resolve**: formatação, ordem de imports, tipos faltando → Pint, Rector, PHPStan.
- **Varredura de convenções do código existente**: usar o skill `infer-conventions` do Boost, que foi feito para isso.
- **Preferência pessoal de sessão**: memória do agente, não rule (rule é artefato de equipe, versionado).
- **Fato volátil**: número de versão, nome de sprint, URL de ambiente temporário.

---

## Os 4 Gates

Candidato só vira rule se passar em **todos**. Registrar o veredito de cada gate na apresentação ao usuário.

### Gate 1 — Durável

> Vale além desta feature e desta sprint?

- ✅ "Valores monetários são `integer` em centavos, nunca `float`"
- ❌ "Nesta feature o status inicial é `pending`" — regra de negócio de um fluxo, vai na ADR

### Gate 2 — Escopável por path

> Dá para expressar em glob?

Rules são carregadas por casamento de glob. Se não se consegue nomear os paths onde a regra se aplica, **não é rule** — é ADR ou guideline interna.

- ✅ `app/Models/**`, `app/Http/Controllers/Api/**`, `database/migrations/**`
- ❌ "vale para o projeto todo" → glob `**` é anti-padrão: carrega em cada edição e vira ruído permanente

**Preferir o glob mais estreito que cobre o caso.** Uma rule em `app/Models/Enrollment.php` é melhor que a mesma rule em `app/**`.

### Gate 3 — Não-inferível

> Um agente competente, lendo o código ao redor, erraria?

Este é o gate que mais elimina candidatos. Se o padrão é evidente nos arquivos vizinhos, o agente acerta sozinho e a rule só consome contexto.

- ✅ "`Enrollment::find()` aplica scope global de tenant — usar `withoutGlobalScopes()` para busca administrativa": invisível no arquivo, consequência silenciosa
- ❌ "Controllers ficam em `app/Http/Controllers`": o agente vê isso na primeira listagem

### Gate 4 — Não-redundante

> Não é default do framework, não é coberto por ferramenta, não duplica rule existente?

Checar, nesta ordem:

1. `Read .ai/rules/index.md` → alguma rule já cobre este glob? Se sim, **atualizar** aquela rule em vez de criar nova
2. Está em `pint.json` / `rector.php` / `phpstan.neon`? → é enforcement automático, não rule
3. É comportamento default do Laravel/Livewire/Pest? → guideline do Boost cobre
4. Existe teste de arquitetura que já garante? → aponte a rule para o teste, não repita a regra

---

## Fluxo de Execução

### 1. Coletar candidatos

**Se vindo da feature-wiki**: ler `01-plano-acao.md`, `02-decisoes-arquiteturais.md` e a seção "Notas de Implementação" do `03-progresso.md`.

**Se vindo de um requisito solto** (card, ticket, conversa): extrair as afirmações normativas — frases com "sempre", "nunca", "todo", "deve", "não pode".

### 2. Verificar o estado atual das rules

```bash
# existe o diretório de rules?
ls .ai/rules/
```

- `Read .ai/rules/index.md` — mapa glob → arquivo
- `Read` as rules dos globs que o candidato tocaria
- Se `.ai/rules/` não existe: Boost provavelmente não está instalado ou as rules estão desativadas (`BOOST_RULES_ENABLED=false`). Ver "Fallback" abaixo.

### 3. Aplicar os 4 gates

Descartar candidato que falhe em qualquer gate, **dizendo qual gate falhou**. Não silenciar descarte — o usuário precisa saber que o candidato foi considerado e por que caiu.

### 4. Preferir enforcement automático (escada de rules)

Antes de escrever prosa, subir esta escada:

1. **Teste de arquitetura** (`pest --arch`) resolve? → escrever o teste; rule fica em 1 linha apontando para ele
2. **PHPStan / Larastan** pega? → configurar a regra; sem rule em prosa
3. **Rector** pode reescrever automaticamente? → adicionar a regra ao `rector.php`
4. **Pint** normaliza? → configurar o preset
5. **Só então**: rule em prosa

> Exemplo: "Controllers devem estender `BaseController`" é um `pest --arch` de uma linha:
> `arch()->expect('App\Http\Controllers')->toExtend('App\Http\Controllers\BaseController');`
> A rule então diz: *"Enforçado em `tests/Arch/ControllersTest.php` — não contornar."*

### 5. Apresentar ao usuário e ESPERAR decisão

**Nunca gravar sem aprovação explícita.** Formato:

```text
Candidato 1 — [origem: ADR-02 / Nota de implementação / requisito]
  Título:    {título curto, imperativo}
  Glob:      {glob mais estreito que cobre}
  Regra:     {uma frase — a restrição}
  Por quê:   {consequência de ignorar — é isto que faz o agente obedecer}
  Evidência: {arquivo:linha ou seção da wiki}
  Gates:     durável ✅ | escopável ✅ | não-inferível ✅ | não-redundante ✅
  Enforcement: {prosa | pest --arch em tests/Arch/X.php | phpstan | rector}

Descartados:
  - {candidato}: falhou no gate {N} — {motivo}

Gravar? (número, "todos", "nenhum")
```

### 6. Gravar via `record-rule` (obrigatório)

Gravar **sempre** pela tool MCP `record-rule` do Boost, passando `glob`, `title` e `note`. A doc do Boost é explícita:

> "You should always record rules using the `record-rule` tool rather than creating rule files by hand. Boost regenerates `.ai/rules/index.md` as part of recording a rule, and agents rely on that index to discover which rules apply to the file they are working on. A rule file that is added manually will not be discovered until the index is next regenerated."

Ou, em linguagem natural para o agente com Boost ativo:

```text
Remember that all money values are stored as integer cents, never as floats.
```

### 7. Verificar e commitar

- Confirmar que o `.ai/rules/index.md` foi regenerado com a linha nova
- `Read` o arquivo de rule gravado e checar se o `note` ficou fiel ao aprovado
- **Commitar `.ai/rules/`** — rules são artefato de equipe, versionado (diferente de `.mcp.json` e `CLAUDE.md`, que o Boost regenera)
- Commit sugerido: `:memo: rules: {título da rule}` com corpo citando a origem (ADR / wiki / card)

---

## Modelo Base do Conteúdo da Rule

O `record-rule` recebe `glob`, `title` e `note`. O modelo abaixo é a **forma do `note`** — e também o formato final do arquivo gravado em `.ai/rules/{area}.md`:

```markdown
---
paths:
  - app/Models/**
  - app/Services/Billing/**
---

# Models

## Valores monetários são inteiros em centavos

Todo campo monetário é persistido como `integer` representando centavos — nunca
`float` ou `decimal`. Converter na borda (Form Request na entrada, cast na saída).
Usar `float` introduz erro de arredondamento que se acumula em relatórios de
fechamento e não é detectado pelos testes unitários de cada operação isolada.

Enforçado parcialmente por `tests/Arch/MoneyTest.php`. Origem: ADR-02 de
`wikis/specs/ferro/579/cobranca-lote/02-decisoes-arquiteturais.md`.
```

### Anatomia obrigatória do `note`

| Parte | Regra | Por quê |
|---|---|---|
| **Título (`##`)** | imperativo, curto, uma restrição só | O agente varre títulos; título vago não é aplicado |
| **Restrição** | 1-2 frases, afirmativa, sem hedge ("deve preferencialmente" → não) | Ambiguidade vira desvio |
| **Consequência** | o que quebra se ignorar, concretamente | **A parte mais importante.** É a consequência que faz o agente obedecer em vez de "otimizar" |
| **Escape hatch** | quando a regra **não** se aplica, se houver | Rule sem exceção declarada é contornada em silêncio |
| **Enforcement / Origem** | teste, ferramenta, ou ADR de origem | Rastreabilidade e prova de que não é opinião solta |

### Regras de escrita

1. **Uma rule = uma restrição.** Duas restrições = dois blocos `##`.
2. **Escrever o porquê, não só o quê.** O exemplo oficial do Boost termina em consequência: *"will leak data across tenants"*. Copiar essa disciplina.
3. **Presente do indicativo, afirmativo.** "Todo controller estende `BaseController`" vence "não deveria estender o controller do framework".
4. **Nomes totalmente qualificados** para classes (`App\Http\Controllers\BaseController`).
5. **Sem número de versão volátil** no corpo — apodrece.
6. **Prosa normal, não terse.** Rules são boundary do Caveman: ambiguidade aqui se propaga para todo agente futuro.
7. **Máximo ~10 linhas por rule.** Rule longa é guideline disfarçada e não será lida por inteiro.

---

## Áreas Sugeridas para Agrupar Rules

O Boost arquiva a rule "under the matching area". Manter poucas áreas, com globs estreitos:

| Arquivo | Glob típico | O que vive nele |
|---|---|---|
| `.ai/rules/models.md` | `app/Models/**` | invariantes de dados, scopes globais, casts obrigatórios |
| `.ai/rules/controllers.md` | `app/Http/Controllers/**` | base class, autorização, formato de resposta |
| `.ai/rules/requests.md` | `app/Http/Requests/**` | padrão de validação, mensagens |
| `.ai/rules/jobs.md` | `app/Jobs/**` | idempotência, retries, channel de log |
| `.ai/rules/migrations.md` | `database/migrations/**` | convenções de nome, FK, seeder-em-migration, guard de environment |
| `.ai/rules/testing.md` | `tests/**` | estratégia de DB, factories obrigatórias, o que precisa CT-B |
| `.ai/rules/livewire.md` | `app/Livewire/**` | padrão de `fail()`, log de validação |
| `.ai/rules/filament.md` | `app/Filament/**` | resources, policies, `data-test` obrigatório |

---

## Fallback — Boost ausente ou rules desativadas

Se `record-rule` não estiver disponível (`BOOST_RULES_ENABLED=false`, Boost não instalado, agente sem MCP):

1. **Avisar o usuário** de que a gravação manual não é o caminho recomendado pela doc do Boost
2. Criar/editar `.ai/rules/{area}.md` com o frontmatter `paths:` e o corpo no modelo acima
3. **Adicionar a linha correspondente à tabela do `.ai/rules/index.md`** — sem isso a rule não é descoberta
4. Registrar no commit que a rule foi gravada manualmente, para reconciliar quando o Boost voltar

Para agentes sem suporte a `.ai/rules` (Windsurf, Cursor, Cline), espelhar o conteúdo no formato do agente (`.windsurf/rules/`, `.cursor/rules/`), mantendo `.ai/rules/` como fonte da verdade.

---

## Anti-padrões

| Anti-padrão | Por que é ruim |
|---|---|
| Glob `**` ou `app/**` | Carrega em quase toda edição; vira imposto permanente de contexto |
| Rule sem consequência | O agente trata como sugestão e "otimiza" por cima |
| Rule que repete guideline do Boost | Duplicação que apodrece na próxima versão do framework |
| Rule que o Pint/Rector/PHPStan já garante | Prosa onde a máquina já resolve; viola a escada |
| Gravar sem aprovação do usuário | Rules são artefato de equipe; entram no git e afetam todos |
| Escrever o arquivo à mão com Boost ativo | O `index.md` não é regenerado e a rule fica invisível |
| Mais de 3 rules por feature | Inflação: quanto mais rules, menos cada uma é respeitada |
| Rule contando história ("decidimos em reunião que...") | Isso é ADR. Rule é imperativa e atemporal |

---

## Checklist Final

- [ ] Candidatos coletados de fonte concreta (ADR, nota de implementação, requisito) com evidência `arquivo:linha`
- [ ] `.ai/rules/index.md` lido; rules dos globs afetados lidas
- [ ] Cada candidato avaliado nos 4 gates, com veredito registrado
- [ ] Descartados comunicados ao usuário com o gate que falhou
- [ ] Escada de enforcement subida — automação preferida à prosa quando possível
- [ ] Atualização de rule existente preferida à criação de nova
- [ ] Glob é o mais estreito que cobre o caso (nunca `**`)
- [ ] `note` contém restrição + consequência + origem
- [ ] Aprovação explícita do usuário obtida
- [ ] Gravado via `record-rule` (ou fallback documentado no commit)
- [ ] `.ai/rules/index.md` regenerado e conferido
- [ ] `.ai/rules/` commitado com gitmoji `:memo: rules:`
- [ ] Teto de 3 rules por feature respeitado

## Skills Companheiras

| Skill | Relação |
|---|---|
| `feature-wiki` | Produz as fontes (ADR, notas, PRD). O step 8 dela invoca esta skill |
| `infer-conventions` (Boost) | Caminho inverso: varre o **código existente** para bootstrapar rules. Rodar uma vez, no início do projeto; esta skill é o incremento contínuo |
| `ponytail` | A escada de enforcement é a escada de simplicidade aplicada a rules: automação antes de prosa, nada antes de automação desnecessária |
| `pest-testing` | Materializa o enforcement em `pest --arch` quando o gate 4 aponta para automação |

> **Caveman**: arquivos de rule são **boundary** — prosa normal. A rule é lida por todo agente futuro; compressão aqui multiplica ambiguidade.
