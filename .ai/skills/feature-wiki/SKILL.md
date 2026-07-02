---
name: feature-wiki
description: >
  Cria estrutura de documentação wiki para uma feature antes de implementá-la.
  Invoque SEMPRE ao iniciar implementação de qualquer feature nova.
  Cria pasta em wikis/{branch} com 4 arquivos obrigatórios: plano de ação (PRD),
  decisões arquiteturais, tracking de progresso e casos de teste. O plano de ação
  deve ser minucioso o suficiente para um agente implementar sem ambiguidade.
---

# Feature Wiki — Documentação Antes de Implementar

## Quando Invocar

- Sempre que o usuário pedir para implementar uma feature nova
- Ao iniciar qualquer card/ticket/task de desenvolvimento
- Antes de qualquer `php artisan make:*` ou criação de código

## Fluxo de Execução

### 1. Descobrir Branch e Estrutura de Pasta

```bash
git rev-parse --abbrev-ref HEAD
```

Branch `ferro/501` → pasta base: `wikis/ferro/501/`
Branch `feature/user-auth` → pasta base: `wikis/feature/user-auth/`
Branch `fix/boleto-juros` → pasta base: `wikis/fix/boleto-juros/`

### 2. Definir Nome da Feature

Perguntar ao usuário (ou derivar do contexto):
- Nome deve ser `kebab-case`
- Deve descrever a feature, não o ticket
- Exemplos: `envio-progresso`, `unico-jobs-progress-tracking`, `api-webhook-payments`

Pasta final: `wikis/{branch}/{feature-name}/`

### 3. Pesquisa e Contexto (OBRIGATÓRIO antes de escrever)

Antes de escrever qualquer documento:
- Usar `database-schema` se a feature envolve novas tabelas ou alterações
- Usar `search-docs` para tecnologias envolvidas (Filament, Livewire, Queue, etc.)
- Ler arquivos existentes relevantes com `Read` ou `Grep`
- Executar `php artisan model:show ModelName` para models relacionados
- Examinar padrões existentes com `Glob "**/[padrão]/**/*.php"`
- **Inspecionar APIs de terceiros** antes de escrever CTs — verificar vendor source ou docs oficiais para confirmar nomes de métodos, assinaturas e restrições de schema
- Para features médias/grandes: delegar o mapeamento amplo a um agent `Explore` e depois **confirmar os trechos críticos com `Read` direto** (linhas exatas, imports, assinaturas) — não confiar apenas no resumo do agent
- **Validar dados fornecidos pelo usuário** (CSV, listas, IDs) contra o banco via `database-query` — detectar divergências de título/chave, escolher chave estável (ID) para mapeamentos e documentar as divergências no plano
- **Verificar existência de factories** (`Glob "database/factories/{Model}*"`) e states disponíveis antes de escrever CTs; se não houver factory, especificar `Model::create([...])` no Setup Global
- **Confirmar padrões internos citados** no plano com grep/read (ex: seeder-em-migration, guards de environment, `$casts` property vs `casts()`) — citar `arquivo:linha` de referência no plano

### 4. Criar os Arquivos

Criar os **4 arquivos obrigatórios** + extras se necessário.

### 5. Revisão Profunda Pós-Escrita (OBRIGATÓRIO)

Após escrever os 4 arquivos, **re-validar cada premissa do plano contra o código real** antes de apresentar ao usuário:

- Reler os pontos exatos citados no plano: imports dos arquivos a editar, assinaturas de métodos, relações de models, padrão das migrations-referência, factories/states usados nos CTs
- **Corrigir a wiki imediatamente** quando a revisão contradisser o plano (ex: plano diz "adicionar import X" → import já existe; plano cita guard genérico → padrão real é `! app()->environment('testing')`)
- Só então apresentar ao usuário para aprovação / iniciar implementação

> Exemplo real (feature/implementar-carga-horaria): a revisão pós-escrita detectou que o import `MbaTrack` já existia no arquivo a editar e confirmou o padrão exato do guard de environment nas migrations com seeder — ambos corrigidos na wiki antes da implementação.

---

## Arquivo 01: Plano de Ação (PRD)

**Path**: `wikis/{branch}/{feature}/01-plano-acao.md`

**Propósito**: PRD completo — deve ser detalhado o suficiente para um agente implementar sem ambiguidade.

**Obrigatório incluir**:
- Objetivo claro em 1-2 parágrafos
- Contexto e problema que resolve
- Análise dos arquivos/código existente que será tocado
- Passos de implementação numerados com:
  - Path exato de cada arquivo a criar/modificar
  - Assinatura de classes, métodos, interfaces
  - Lógica de negócio detalhada
  - Campos de DB com tipos, nullable, índices, constraints
  - Mapeamentos de campos (ex: API → DB)
  - Tratamento de erros esperados
- Skills a invocar em cada passo (ver lista abaixo)
- Referência ao `04-casos-de-teste.md` (não duplicar cenários aqui)
- Passos de verificação (pint, tests, artisan commands)
- Passos de commit (gitmoji + escopo + mensagem)

**Skills disponíveis para referenciar no PRD**:
```
- laravel-best-practices   → qualquer código PHP Laravel
- eloquent-best-practices  → models, queries, relacionamentos
- laravel-specialist       → Sanctum, queues, Livewire, API resources
- laravel-11-12-app-guidelines → features, bugs, UI
- pest-testing             → escrever/editar testes Pest
- tailwindcss-development  → qualquer Tailwind/Blade/UI
- livewire-development     → componentes Livewire
- ponytail                 → execução minimalista (escada de simplicidade)
```

> **Integração com Ponytail**: Após a wiki ser aprovada, o Ponytail deve ser a skill de execução ativa durante toda a implementação. Ele garante que cada passo do plano seja executado com o mínimo de código necessário (reutilização → stdlib → feature nativa → uma linha → mínimo que funciona). Após implementar, rodar `/ponytail-review` no diff para validar contra over-engineering. Atalhos deliberados devem ser marcados com `ponytail:` comment. Ver o README do repositório para o passo a passo completo da integração.

**Template `01-plano-acao.md`**:
```markdown
# Plano de Ação — {Card}: {Título da Feature}

## Objetivo

{1-2 parágrafos descrevendo o que será implementado e por quê}

## Contexto

{Problema atual, limitações, por que essa feature é necessária}

## Análise dos Arquivos Existentes

### {NomeDoArquivo}
- {Descrição do que existe e como será afetado}

## Estrutura de Implementação

### 1. {Nome do Passo}

> Skills: `laravel-best-practices`, `pest-testing`

- **Path**: `app/...`
- {Detalhes de implementação}

### 2. {Nome do Passo}
...

## Filosofia de Implementação

> **Ponytail ativo em modo `full`** durante toda a implementação.
> Cada passo deve aplicar a escada de simplicidade:
> 1. Reutilizar código existente antes de criar novo
> 2. Usar stdlib do PHP/Laravel antes de código custom
> 3. Usar features nativas antes de dependências
> 4. Uma linha quando possível
> 5. Mínimo código que funciona
>
> Atalhos deliberados devem ser marcados com `ponytail:` comment.
> Após implementação, rodar `/ponytail-review` no diff.

## Mapeamentos

{Tabelas de mapeamento de campos, status, etc. — quando aplicável}

## Testes

> Ver `04-casos-de-teste.md` para especificação completa dos cenários.

## Verificação Final
- [ ] `/ponytail-review` no diff (validar contra over-engineering)
- [ ] `vendor/bin/pint --dirty`
- [ ] `php artisan test --compact --filter={Feature}`
- [ ] {outros comandos de verificação específicos}

## Commits
- `{gitmoji} {escopo}: {mensagem}`
- `:memo: {escopo}: wiki da feature {nome}`
```

---

## Arquivo 02: Decisões Arquiteturais

**Path**: `wikis/{branch}/{feature}/02-decisoes-arquiteturais.md`

**Propósito**: Registrar o "porquê" das escolhas — não o "o quê".

**Incluir**:
- Cada decisão não-óbvia com justificativa
- Alternativas consideradas e por que foram descartadas
- Trade-offs aceitos
- Restrições externas (APIs, limites de parceiros, compliance)
- Padrões reutilizados de outras partes do sistema

**Template `02-decisoes-arquiteturais.md`**:
```markdown
# Decisões Arquiteturais — {Card}

## 1. {Título da Decisão}

{Explicação da decisão e justificativa. Por que essa abordagem e não outra?}

## 2. {Título da Decisão}
...
```

---

## Arquivo 03: Progresso / Tracking

**Path**: `wikis/{branch}/{feature}/03-progresso.md`

**Propósito**: Checklist de implementação para rastrear o que foi feito e retomar de onde parou.

**Estrutura**: Seções com checkboxes `- [ ]` agrupadas pelos mesmos passos do `01-plano-acao.md`. Atualizar os checkboxes **em tempo real** durante a implementação — não em lote no final.

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

## Verificação Final
- [ ] `/ponytail-review` no diff (validar contra over-engineering)
- [ ] `vendor/bin/pint --dirty`
- [ ] `php artisan test --compact --filter={Feature}`
- [ ] `git commit`
```

---

## Arquivo 04: Casos de Teste (CT)

**Path**: `wikis/{branch}/{feature}/04-casos-de-teste.md`

**Propósito**: Especificação completa de cada caso de teste — setup, mocks, dados de entrada e assertions esperadas. Deve ser detalhado o suficiente para um agente escrever os testes sem ambiguidade.

**Por que este arquivo existe**: Escrever os CTs *antes* da implementação força a pesquisa das APIs envolvidas (métodos reais, restrições de schema, contratos de terceiros) na fase de planejamento — não na fase de debug. Previne surpresas como nomes de método incorretos, FKs obrigatórias em fixtures ou restrições de schema de bibliotecas externas.

**Obrigatório incluir por cenário**:
- ID único (`CT-01`, `CT-02`, ...)
- Tipo: `Feature` ou `Unit`
- Path do arquivo de teste
- Nome do método `it()`
- Precondições (estado do DB, factories, mocks ativos)
- Dados de entrada (payload, CSV row, argumentos)
- Resultado esperado (assertions específicas)

**Setup Global**: documentar uma vez as factories/mocks comuns a vários CTs.

**Template `04-casos-de-teste.md`**:
```markdown
# Casos de Teste — {Card}: {Título da Feature}

## Setup Global

### Factories / Fixtures
- `{Model}::factory()->{state}()->create([...])` — {descrição}
- ...

### Estratégia de Mock
- `{ExternalService}`: Mockery via `app()->instance()` — métodos: `{método}()`
- `Queue::fake()` — verificar dispatch de `{JobClass}`
- `Http::fake()` — endpoints: `{url}`

---

## CT-01: {Nome do Cenário — Happy Path}

**Tipo**: `Feature` | `Unit`
**Arquivo**: `tests/{Feature|Unit}/{Path}/{NomeTest}.php`
**Método**: `it('{descrição legível}')`

### Precondições
- {O que deve existir no DB antes — model + estado}
- {Mocks a configurar}

### Dados de Entrada
```
{input: payload, CSV row, argumentos de método, etc.}
```

### Resultado Esperado
- `{Model}` criado/atualizado com `{campo}` = `{valor}`
- `{Job}` despachado com `{argumento}` = `{valor}`
- `{Relacionamento}` existe com `{n}` registros

---

## CT-02: {Nome do Cenário — Falha / Edge Case}

**Tipo**: `Feature`
**Arquivo**: `tests/Feature/...`
**Método**: `it('{descrição}')`

### Precondições
- {Estado inicial que causa a falha}

### Dados de Entrada
```
{input inválido ou condição de borda}
```

### Resultado Esperado
- Lança `{ExceptionClass}` com mensagem `"{texto}"`
- `{Model}` NÃO criado (`{Model}::count()` = 0)
- `{Job}` NÃO despachado

---

## Índice de Casos

| ID | Cenário | Tipo | Arquivo |
|----|---------|------|---------|
| CT-01 | {happy path} | Feature | `tests/...` |
| CT-02 | {falha X} | Feature | `tests/...` |
| CT-03 | {edge case Y} | Unit | `tests/...` |
```

---

## Arquivos Extras (conforme necessidade)

Criar apenas quando a feature exige:

| Arquivo | Quando criar |
|---------|-------------|
| `05-design.md` | Feature com UI significativa (Filament, Livewire, Blade) |
| `05-api-contract.md` | Feature com API externa (payloads, endpoints, autenticação) |
| `05-db-schema.md` | Feature com schema complexo (múltiplas tabelas, migrations em cadeia) |
| `05-fluxo.md` | Feature com fluxo multi-etapas (queues + jobs + callbacks) |

---

## Checklist Final da Skill

Antes de encerrar a invocação:

- [ ] Branch lida e estrutura de pasta criada
- [ ] Nome da feature confirmado com usuário
- [ ] Pesquisa feita (`search-docs`, `database-schema`, leitura de arquivos)
- [ ] APIs de terceiros inspecionadas (vendor source ou docs) — métodos e schema confirmados
- [ ] Dados fornecidos pelo usuário validados contra o DB (quando aplicável)
- [ ] Factories confirmadas (existência + states) para todos os CTs
- [ ] `01-plano-acao.md` escrito com passos numerados + skills referenciadas
- [ ] `02-decisoes-arquiteturais.md` escrito com justificativas
- [ ] `03-progresso.md` escrito com checkboxes espelhando o plano
- [ ] `04-casos-de-teste.md` escrito com todos os CTs identificados
- [ ] Arquivos extras (`05-*`) criados se necessário
- [ ] Revisão profunda pós-escrita executada — premissas do plano re-validadas contra o código
- [ ] Filosofia de Implementação (Ponytail) incluída no PRD
- [ ] Confirmar com usuário se o plano está correto antes de implementar

## Exemplo de Estrutura Criada

```
wikis/
└── ferro/
    └── 579/
        └── relatorio-mba-lote/
            ├── 01-plano-acao.md
            ├── 02-decisoes-arquiteturais.md
            ├── 03-progresso.md
            ├── 04-casos-de-teste.md          ← novo obrigatório
            └── 05-api-contract.md            ← extra quando necessário
```
