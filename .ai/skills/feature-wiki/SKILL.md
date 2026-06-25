---
name: feature-wiki
description: >
  Cria estrutura de documentação wiki para uma feature antes de implementá-la.
  Invoque SEMPRE ao iniciar implementação de qualquer feature nova.
  Cria pasta em wikis/{branch} com 3 arquivos obrigatórios: plano de ação (PRD),
  decisões arquiteturais e tracking de progresso. O plano de ação deve ser minucioso
  o suficiente para um agente implementar sem ambiguidade.
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

### 4. Criar os Arquivos

Criar os 3 arquivos obrigatórios + extras se necessário.

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
- Testes a escrever (nome do arquivo, cenários)
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
```

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

## Mapeamentos

{Tabelas de mapeamento de campos, status, etc. — quando aplicável}

## Testes

### {NomeDoTesteTest}
- {cenário 1}
- {cenário 2}

## Verificação Final
- [ ] `vendor/bin/pint --dirty`
- [ ] `php artisan test --compact --filter={Feature}`
- [ ] {outros comandos de verificação específicos}

## Commits
- `{gitmoji} {escopo}: {mensagem}`
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

**Estrutura**: Seções com checkboxes `- [ ]` agrupadas pelos mesmos passos do `01-plano-acao.md`.

**Template `03-progresso.md`**:
```markdown
# Progresso — {Card}

## {Seção 1 do Plano}
- [ ] {Item 1}
- [ ] {Item 2}

## {Seção 2 do Plano}
- [ ] {Item 1}

## Testes
- [ ] `{NomeDoTesteTest}`

## Verificação Final
- [ ] `vendor/bin/pint --dirty`
- [ ] `php artisan test --compact --filter={Feature}`
- [ ] `git commit`
```

---

## Arquivos Extras (conforme necessidade)

Criar apenas quando a feature exige:

| Arquivo | Quando criar |
|---------|-------------|
| `04-design.md` | Feature com UI significativa (Filament, Livewire, Blade) |
| `04-api-contract.md` | Feature com API externa (payloads, endpoints, autenticação) |
| `04-db-schema.md` | Feature com schema complexo (múltiplas tabelas, migrations em cadeia) |
| `04-fluxo.md` | Feature com fluxo multi-etapas (queues + jobs + callbacks) |

---

## Checklist Final da Skill

Antes de encerrar a invocação:

- [ ] Branch lida e estrutura de pasta criada
- [ ] Nome da feature confirmado com usuário
- [ ] Pesquisa feita (`search-docs`, `database-schema`, leitura de arquivos)
- [ ] `01-plano-acao.md` escrito com passos numerados + skills referenciadas
- [ ] `02-decisoes-arquiteturais.md` escrito com justificativas
- [ ] `03-progresso.md` escrito com checkboxes espelhando o plano
- [ ] Arquivos extras criados se necessário
- [ ] Confirmar com usuário se o plano está correto antes de implementar

## Exemplo de Estrutura Criada

```
wikis/
└── ferro/
    └── 501/
        ├── envio-progresso/
        │   ├── 01-plano-acao.md
        │   ├── 02-decisoes-arquiteturais.md
        │   └── 03-progresso.md
        └── jobs-progress-tracking/
            ├── 01-plano-acao.md
            ├── 02-decisoes-arquiteturais.md
            ├── 03-progresso.md
            └── 04-api-contract.md  ← extra quando necessário
```
