> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de escrever o `01-plano-acao.md`). Fonte única de: template do `01-plano-acao.md` e lista de skills citáveis no PRD.

# Template do `01-plano-acao.md`

O que o PRD é obrigado a incluir fica no corpo do `SKILL.md`, seção *Arquivo 01*; o padrão de log,
na seção *Padrão de Log* e em `references/padrao-de-log.md`.

## Skills disponíveis para referenciar no PRD

**Skills disponíveis para referenciar no PRD**:
```
- laravel-best-practices   → qualquer código PHP Laravel
- eloquent-best-practices  → models, queries, relacionamentos
- laravel-specialist       → Sanctum, queues, Livewire, API resources
- laravel-11-12-app-guidelines → features, bugs, UI
- pest-testing             → escrever/editar testes Pest (backend e browser)
- tailwindcss-development  → qualquer Tailwind/Blade/UI
- livewire-development     → componentes Livewire
- ponytail                 → execução minimalista (escada de simplicidade)
- requirement-to-rule      → transformar decisão da wiki em Project Rule do Boost
- feature-quality-gate     → QA no agente: confronto requisito × plano × app
```

> `laravel-best-practices`, `eloquent-best-practices`, `laravel-specialist`, `laravel-11-12-app-guidelines`, `pest-testing`, `tailwindcss-development` e `livewire-development` são skills do **Laravel Boost**, instaladas pelo `boost:install`; não fazem parte desta coletânea.

## Template

**Template `01-plano-acao.md`**:
```markdown
# Plano de Ação — {Card}: {Título da Feature}

> Requisito: `00-requisito.md`

## Natureza da Wiki

- **Tipo**: nova | evolução | correção | ajuste
- **Wiki ancestral**: `wikis/specs/{branch}/{feature}/` — **obrigatório** se o tipo não for "nova"
- **Motivo**: {o que mudou desde a ancestral}
- **Toca infra compartilhada?**: não | sim → {o quê: seeder de permissões, middleware global, `tests/Pest.php`, config de logging, migration em tabela de outra feature}

> O tipo decide o escopo do `feature-quality-gate`: `nova` valida só a feature; os outros três disparam **regressão** contra os CT/CT-B da wiki ancestral.
>
> **Exceção que o tipo não cobre**: feature `nova` que **altera infra compartilhada** — a matriz
> de papéis, um seeder que outras features consomem, um middleware global, o `tests/Pest.php`.
> Aí o tipo é `nova` e a regressão é **obrigatória** mesmo assim, contra os CT/CT-B das features
> que consomem a infra tocada. Marcar "Toca infra compartilhada? sim" **força a regressão**,
> independente do tipo.

## Cobertura do Requisito

<!-- Toda cláusula do 00-requisito.md precisa aparecer aqui. Cláusula sem passo é omissão. -->

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | {resumo} | 3, 4 | — |
| RQ-02 | {resumo} | 5 | — |
| RQ-03 | {resumo} | — | ⚠️ fora de escopo desta entrega — justificar |

## Objetivo

{1-2 parágrafos descrevendo o que será implementado e por quê}

## Contexto

{Problema atual, limitações, por que essa feature é necessária}

## Análise dos Arquivos Existentes

### {NomeDoArquivo}
- {Descrição do que existe e como será afetado}

## Autorização

- **Policies**: {quais criar/modificar, métodos autorizados}
- **Gates**: {se aplicável}
- **Middleware**: {rotas protegidas por qual middleware}
- **Guards**: {se aplicável}

## Rotas

| Método | URI | Name | Middleware |
|--------|-----|------|------------|
| {GET/POST/...} | {/path} | {route.name} | {auth,can:...} |

## Superfície de UI

<!-- Preencher "Sem superfície de UI" quando a feature for só backend (job, webhook, command) -->

| Tela / Componente | Tipo | Rota | Interação do usuário | Depende de JS? |
|---|---|---|---|---|
| {NomeDoComponente} | Filament \| Livewire \| Blade \| Inertia | {/path} | {o que o usuário faz} | Sim \| Não |

**Gate de CT-B**: esta tabela é o **gatilho**, não o critério. O cenário só vai para o browser
quando afirma sobre algo que **só o navegador prova** — JavaScript executado, console/erro de JS,
acessibilidade, cor/tema, layout. Validação de formulário, gravação, listagem, filtro, ação de
tabela, notificação e autorização na tela são **teste de componente Livewire** e pertencem ao `04`.

**Gate de tela de escrita**: para toda rota `create`/`edit` desta tabela, o `04` precisa ter um
cenário de **gravação por componente** — *uma tela aberta não é uma tela que grava*.

## Variáveis de Ambiente

| Key | Default | Descrição |
|-----|---------|-----------|
| {FEATURE_KEY} | {default} | {o que controla} |

## Eventos / Listeners / Observers

- **Eventos emitidos**: {lista}
- **Listeners**: {lista}
- **Observers**: {model e métodos hooked}

## Jobs / Queues

- **Job**: {nome} → queue: {connection/name}, timeout: {s}, retries: {n}, backoff: {s}

## Modelo de Execução

<!-- Quantas VEZES o caminho principal roda, e o que é compartilhado entre elas.
     Preencher "um request, sem trabalho adiado" quando for o caso — é resposta válida. -->

| Pergunta | Resposta |
|---|---|
| Quantos requests a tela custa? | {1 · ou N, e por quê: widget lazy, tabela adiada, polling, ação assíncrona} |
| O que é adiado, e por qual gatilho? | {`lazy` do Livewire ao entrar na viewport · `deferLoading` da tabela · nenhum} |
| O que é memoizado **por request**? | {e o que isso NÃO alcança quando há N requests} |
| O que é cacheado **entre** requests? | {chave, TTL, quem invalida} |
| Custo do caminho principal | {queries do caminho comum × queries do caminho com filtro/busca} |

**Este bloco existe porque uma ADR pode estar internamente coerente e apoiada numa premissa que
ninguém escreveu.** Caso real (2026-09-17): uma ADR decidiu, com bom argumento, não cachear o
agregado quando há filtro — e assumiu implicitamente *"uma tela = um request"*. Os widgets eram
`lazy`, ou seja **oito requests independentes**, cada um recalculando: 48 queries viraram ~384 por
carga filtrada. O memo por request que o código documentava **não existia**, e não teria ajudado —
memo estático não atravessa request. Nenhum gate da wiki mede custo; declarar o modelo é o que
torna a premissa falsificável na revisão.

## Impacto em Features Existentes

- {Feature X}: {o que pode quebrar e por quê}
- {Feature Y}: {dependência compartilhada}

## Rollback

- **Migration down**: {o que `down()` faz}
- **Feature flag**: {se aplicável, como desativar}
- **Reversão de dados**: {se aplicável, como reverter dados migrados}

## Dependências

- **Composer**: {package} {version}
- **NPM**: {package} {version}

## Riscos

- {Risco 1}: {mitigação}
- {Risco 2}: {mitigação}

## Channel de Log da Feature

### Verificação de Channel Existente

- Buscar em `config/logging.php` por channels já configurados
- Verificar se já existe um channel com nome relacionado à feature (ex: `feature-{nome}`, `{sistema}-{feature}`)
- Usar `Grep` em `config/logging.php` e em `app/` por referências a `Log::channel(`

### Decisão

- **Se channel existe**: referenciar no plano como `Log::channel('{nome}')` em todos os passos
- **Se não existe**: incluir como primeiro passo de implementação a criação do channel em `config/logging.php`, com:
  - Nome: `{feature-name}` (kebab-case, mesmo nome da pasta da feature)
  - Driver: `daily` (rotação automática)
  - Path: `storage/logs/{feature-name}.log`
  - Level: `debug` (para rastreabilidade completa durante desenvolvimento)
  - Exemplo de configuração:
    ```php
    '{feature-name}' => [
        'driver' => 'daily',
        'path' => storage_path('logs/{feature-name}.log'),
        'level' => 'debug',
        'days' => 14,
    ],
    ```

> **Por que agrupar por channel**: Logs de uma feature ficam isolados em arquivo próprio, facilitando debug, auditoria e remoção futura. Evita poluir o log principal do sistema com ruído de uma feature específica.

## Estrutura de Implementação

### 1. {Nome do Passo}

> Skills: `laravel-best-practices`, `pest-testing`

- **Path**: `app/...`
- {Detalhes de implementação}
- **Logs**:
  - `Log::channel('{feature-name}')->info('[{Classe}@{metodo}] {mensagem da ação} | {parametro principal}')`
  - Especificar cada ponto de log: início, sucesso, falha, decisões de fluxo

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
> Após implementação, rodar `/ponytail:ponytail-review` no diff.
>
> **Caveman ativo em modo `ultra`** (padrão) na comunicação agent ↔ usuário.
> Arquivos wiki (00-06) são boundary do Caveman — escrever em prosa normal.
> Código, commits e PRs também são boundary do Caveman.
>
> **Model novo declara `$table`** sempre que o nome da tabela não for o plural inglês que o
> Eloquent infere — com nome em pt-BR é sempre: `centros_custo`, não `centro_custos`. Nasceu como
> defeito (2026-09-21) e é candidato natural a Project Rule no step 9.
>
> **Baseline antes do primeiro commit**: rodar a suíte completa em `{base}` e listar por nome as
> falhas pré-existentes. A `## Verificação Final` compara contra a baseline, não contra zero.

## Mapeamentos

{Tabelas de mapeamento de campos, status, etc. — quando aplicável}

## Testes

> Ver `04-casos-de-teste.md` para especificação completa dos cenários de backend.
> Ver `05-casos-de-teste-browser.md` para os cenários de UI (quando a feature tem superfície de UI).

## Verificação Final
- [ ] `/ponytail:ponytail-review` no diff (validar contra over-engineering)
- [ ] `vendor/bin/pint --dirty`
- [ ] `vendor/bin/pest --filter={Feature} --compact` (CTs de backend)
- [ ] `vendor/bin/pest tests/Browser --filter={Feature}` (CT-B — só se houver `05-*-browser.md`)
- [ ] `vendor/bin/pest --parallel --tia` (Pest 5 — confirma que nada mais no suite quebrou, rodando só o afetado) — comparado à **baseline** de `{base}`
- [ ] `pest --mutate --path={classe de regra}` — score, **duração** e lista de sobreviventes (score sem duração plausível é falso; ver *Pest 5*)
- [ ] **Custo medido** — queries do caminho principal e do caminho com filtro/busca, contra o `## Modelo de Execução`, com N **acima da página**
- [ ] **`/code-review high {base}...HEAD` + passe de eixos (step 6.5)** — antes da reconciliação; o único gate que lê o diff atrás de defeito de correção
- [ ] {outros comandos de verificação específicos}

## Commits
- `{gitmoji} {escopo}: {mensagem}`
- `:memo: {escopo}: wiki da feature {nome}`
```
