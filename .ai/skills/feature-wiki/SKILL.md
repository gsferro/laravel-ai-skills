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
- **Channel de log da feature** (ver seção "Padrão de Log" abaixo)
- Passos de implementação numerados com:
  - Path exato de cada arquivo a criar/modificar
  - Assinatura de classes, métodos, interfaces
  - Lógica de negócio detalhada
  - **Logs em todas as etapas de execução** — cada passo que executa lógica deve especificar quais logs emitir (ver seção "Padrão de Log" abaixo)
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

## Padrão de Log — `[Classe@Método] mensagem`

### Por que este padrão

O formato `[Classe@Método] mensagem` é obrigatório em **todos os logs** do projeto. Ele resolve três problemas:

1. **Rastreabilidade**: ao ler um log, sabe-se imediatamente qual classe e método o gerou — sem precisar buscar no código
2. **Filtragem**: permite `grep` por classe ou método para isolar fluxos específicos
3. **Consistência**: padroniza a leitura em qualquer nível (info, warning, error) e em qualquer channel

### Formato Obrigatório

```
[{Classe}@{Método}] {mensagem descritiva} | {parâmetro principal}: {valor} - {contexto adicional}
```

### Anatomia da Mensagem

| Parte | Descrição | Exemplo |
|-------|-----------|---------|
| `{Classe}` | Nome da classe (sem namespace) | `AddUserToClassJob` |
| `{Método}` | Nome do método que está logando | `processAddUserToClass` |
| `{mensagem}` | Descrição clara da ação executada | `Membro associado com sucesso` |
| `{parâmetro}` | ID, status, ou valor principal manipulado | `enrollment: 280114` |
| `{contexto}` | Informação adicional relevante (opcional) | `evento: enrollment.requested` |

### Regras de Escrita

1. **Prefixo sempre entre colchetes**: `[Classe@Método]` — sem espaços dentro dos colchetes
2. **Mensagem em português**: descrever a **ação executada**, não o estado (use "Membro associado com sucesso" em vez de "Membro foi associado")
3. **Pipe `|` como separador**: entre a mensagem e os parâmetros/contexto
4. **Hífen `-` como separador secundário**: entre múltiplos parâmetros de contexto
5. **Incluir parâmetro principal sempre que possível**: IDs, slugs, status — valores que identificam o registro manipulado
6. **Nível de log apropriado**:
   - `debug` → detalhe intermediário para rastreabilidade
   - `info` → sucesso de operação esperada
   - `notice` → evento significativo mas normal (ex: queue retry agendado)
   - `warning` → condição anormal mas não fatal — **usar em `fail()` de Livewire**, fallback, retry, dado ausente
   - `error` → falha que interrompe o fluxo — **usar em `catch` de exceptions** que quebram a execução
   - `critical` → erro de sistema que exige intervenção imediata (ex: DB inacessível, API crítica fora do ar)
   - `emergency` → sistema indisponível, intervenção humana urgente
7. **Máximo de contexto estruturado**: SEMPRE passar o segundo parâmetro `array $context` do Laravel com todos os dados relevantes — IDs, payloads, snapshots de estado, dados do modelo (ver seção "Contexto Estruturado" abaixo)
8. **Exceptions no contexto**: ao logar uma exception, incluir `'exception' => $e` no array de contexto — o Laravel serializa automaticamente stack trace, mensagem e código
9. **Nível do log = severidade da ação**: `fail()` → `warning`; `catch` de exception que interrompe → `error`; `catch` de exception tratada/ignorada → `warning`

### Contexto Estruturado (array `$context`)

O Laravel aceita um segundo parâmetro `array $context` em todos os métodos de log. **Sempre usar** — é onde vai o máximo de informação estruturada para debug e auditoria.

#### O que incluir no context

- **IDs**: todos os IDs relacionados ao fluxo (`user_id`, `enrollment_id`, `turma_id`, `job_id`)
- **Payloads**: dados de entrada que dispararam a ação (`payload`, `request_data`, `webhook_data`)
- **Snapshots de estado**: valores antes/depois de alterações (`before`, `after`)
- **Dados do modelo**: atributos relevantes do model manipulado (`attributes`, `changes`)
- **Exception**: `'exception' => $e` — o Laravel serializa stack trace, mensagem e código automaticamente
- **Contexto de execução**: `queue`, `attempt`, `connection` em jobs; `route`, `ip` em controllers
- **Decisões de fluxo**: `reason`, `condition`, `skip_reason` para branches tomados

#### Exemplo de context rico

```php
Log::channel('feature-name')->info(
    '[AddUserToClassJob@processAddUserToClass] Membro associado com sucesso | enrollment: 280114',
    [
        'enrollment_id' => 280114,
        'user_id'       => 123,
        'turma_id'      => 456,
        'evento'        => 'enrollment.requested',
        'payload'       => $request->all(),
        'attributes'    => $enrollment->getAttributes(),
        'changes'       => $enrollment->getChanges(),
    ]
);
```

> **Regra de ouro**: se a informação pode ajudar a reproduzir ou diagnosticar o problema, vai no `context`. Melhor ter informação demais que de menos.

### Exemplos Práticos

```php
// Início de processamento
Log::channel('feature-name')->info('[AddUserToClassJob@handle] Iniciando adição do usuário | user_id: 123 - turma_id: 456', [
    'user_id'  => 123,
    'turma_id' => 456,
    'attempt'  => 1,
    'queue'    => 'default',
]);

// Sucesso com contexto
Log::channel('feature-name')->info('[AddUserToClassJob@processAddUserToClass] Membro associado com sucesso | enrollment: 280114 - evento: enrollment.requested', [
    'enrollment_id' => 280114,
    'user_id'       => 123,
    'turma_id'      => 456,
    'evento'        => 'enrollment.requested',
    'changes'       => $enrollment->getChanges(),
]);

// Criação de recurso externo
Log::channel('feature-name')->info('[CreateCurseducaUserJob@createCurseducaAccount] Conta criada com sucesso | aluno_id: 789', [
    'aluno_id'        => 789,
    'external_id'     => $response->json('id'),
    'response_status' => $response->status(),
]);

// Webhook recebido
Log::channel('feature-name')->info('[UnicoWebhookController@handle] Webhook recebido | evento: enrollment.requested', [
    'evento'  => 'enrollment.requested',
    'payload' => $request->all(),
    'ip'      => $request->ip(),
    'route'   => $request->path(),
]);

// Condição de fluxo — warning (dado ausente, fallback, retry)
Log::channel('feature-name')->warning('[ProcessCurseducaAccountCreationJob@handle] Usuário já existe, pulando criação | aluno_id: 789', [
    'aluno_id'   => 789,
    'skip_reason'=> 'user_already_exists',
    'existing_id'=> $existingUser->id,
]);

// fail() de Livewire — warning (fluxo interrompido pelo usuário, não é erro de sistema)
Log::channel('feature-name')->warning('[CreateEnrollmentForm@submit] Validação falhou | user_id: 123', [
    'user_id'    => 123,
    'errors'     => $this->getErrorBag()->toArray(),
    'input'      => $this->form->toArray(),
]);

// catch de exception que interrompe o fluxo — error
Log::channel('feature-name')->error('[AddUserToClassJob@processAddUserToClass] Falha ao associar membro | enrollment: 280114', [
    'enrollment_id' => 280114,
    'exception'     => $e,  // Laravel serializa stack trace + mensagem + código
    'attempt'       => $this->attempts(),
    'payload'       => $this->payload,
]);

// catch de exception tratada/ignorada — warning (não quebra o fluxo)
Log::channel('feature-name')->warning('[SyncEnrollmentsJob@handle] Erro ao sincronizar um item, continuando | enrollment: 280114', [
    'enrollment_id' => 280114,
    'exception'     => $e,
    'will_retry'    => true,
]);

// Erro crítico de sistema — critical
Log::channel('feature-name')->critical('[ProcessCurseducaAccountCreationJob@handle] API Curseduca indisponível | tentativa: 3', [
    'attempt'       => 3,
    'exception'     => $e,
    'api_endpoint'  => config('services.curseduca.url'),
    'queue'         => 'default',
]);
```

### Como Implementar no Plano

Para **cada passo de implementação** no PRD, especificar:

1. **Quais métodos terão logs** — listar cada método e os pontos exatos (início, sucesso, falha, decisão de fluxo, catch de exception, fail de validação)
2. **Qual channel usar** — `Log::channel('{feature-name}')` em todos os logs da feature
3. **Qual nível** — debug/info/notice/warning/error/critical conforme a regra de severidade:
   - `fail()` de Livewire → `warning`
   - `catch` de exception que **interrompe** o fluxo → `error`
   - `catch` de exception **tratada/ignorada** → `warning`
   - Sistema/API indisponível → `critical`
4. **Qual mensagem** — já escrever a string completa no plano, seguindo o formato
5. **Qual context** — listar o array de contexto com todos os campos relevantes (IDs, payloads, snapshots, `exception`)

> **Anti-padrão**: NUNCA usar `Log::info('...')` sem channel — sempre especificar o channel da feature.
> **Anti-padrão**: NUNCA usar mensagens genéricas como "Processando..." ou "Erro ocorrido" — sempre incluir `[Classe@Método]` e parâmetro principal.
> **Anti-padrão**: NUNCA logar apenas em `catch` — logar também no sucesso e nos pontos de decisão de fluxo.
> **Anti-padrão**: NUNCA passar context vazio — incluir o máximo de informação estruturada possível (IDs, payloads, snapshots, exception).
> **Anti-padrão**: NUNCA usar `error` para `fail()` de validação — `fail()` é uma condição esperada de interrupção, usar `warning`.
> **Anti-padrão**: NUNCA usar `info` para exceptions — exceptions são anomalias, usar no mínimo `warning` (tratada) ou `error` (interrompe).

### Trait UnicoLogging (se aplicável)

Se o projeto possuir uma trait de logging (ex: `UnicoLogging`), verificar:

- `Grep` por `trait UnicoLogging` ou `trait.*Logging` em `app/`
- Se existir, usar a trait nos classes da feature — ela formata automaticamente o prefixo `[Classe@Método]`
- Se não existir, implementar o formato manualmente via `Log::channel(...)->info('[Classe@metodo] ...')`
- Documentar no plano qual abordagem será usada

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
- [ ] `01-plano-acao.md` escrito com passos numerados + skills referenciadas + logs em todas as etapas
- [ ] `02-decisoes-arquiteturais.md` escrito com justificativas
- [ ] `03-progresso.md` escrito com checkboxes espelhando o plano
- [ ] `04-casos-de-teste.md` escrito com todos os CTs identificados
- [ ] Arquivos extras (`05-*`) criados se necessário
- [ ] Channel de log da feature verificado/criado e referenciado em todos os passos do PRD
- [ ] Padrão de log `[Classe@Método] mensagem` especificado em cada passo de execução do PRD
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
