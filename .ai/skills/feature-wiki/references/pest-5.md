> Referência da feature-wiki 3.6.0. Lida em: step 3 (versão do Pest), implementação (`--tia` e `--agent` a cada passo) e step 7 / Verificação Final (`--tia`, `--mutate`). Fonte única de: instalação, TIA, agent plugin, lançador `.cmd` do Windows e demais recursos do Pest 5.

# Execução de Testes com Pest 5

A detecção da versão e as regras duras (uma suíte por comando, plausibilidade do score do
`--mutate`, forma canônica `--parallel --tia`, nada de `--parallel` com browser, nada de `--tia` no
CI, `--agent` não substitui CT) ficam no corpo do `SKILL.md`, seção *Execução de Testes com Pest 5*.

Instalação/upgrade (conforme a doc oficial — **não existe `php artisan pest:install`**):

```bash
composer remove phpunit/phpunit
composer require pestphp/pest --dev --with-all-dependencies
./vendor/bin/pest --init          # cria tests/Pest.php
```

Vindo de Pest 4: `"pestphp/pest": "^5.0"` no `composer.json` + todos os plugins para `^5.0`.

## `pest --mutate` no Windows — o lançador `.cmd`

- **`pest --mutate` dá 100 % falso no Windows.** O plugin relança `argv[0]` (`vendor/bin/pest`,
  script sh) por Symfony Process; o `cmd` não o executa, o subprocesso sai com código 1 em ~30 ms e
  o plugin conta **qualquer** saída não-zero como mutante morto. Sintoma: *206 mutantes em 3 s*
  para uma suíte de 200 s — e o juiz cego caiu nisso também (*"2 mutantes, 100 %"*). Regra:
  **score só vale com `Duration` compatível com N × tempo dos testes cobridores e com a lista de
  sobreviventes.** No Windows, lançar por um `.cmd` poliglota na raiz do projeto, para que
  `argv[0]` seja executável pelo `cmd`:

  ```
  <?php /*
  @echo off
  php "%~f0" %*
  exit /b %errorlevel%
  */ require __DIR__.'/vendor/pestphp/pest/bin/pest';
  ```

  `XDEBUG_MODE=coverage cmd //c pestw.cmd tests/Feature/{Feature} --mutate --path=app/Models/X.php --covered-only --parallel`
  — medido de verdade na feature de referência: 206 mutantes, 196 mortos, 7 timeout,
  3 sobreviventes (context de log), 98,54 % em 594 s. Timeout conta como morto no score; listar
  os sobreviventes é o que vale

### TIA — Test Impact Analysis (`--tia`)

Roda apenas os testes afetados pelo diff e replica o resultado em cache para o restante. Exige driver de cobertura (**PCOV ou Xdebug**) instalado.


```bash
vendor/bin/pest --parallel --tia    # PADRÃO da skill
vendor/bin/pest --tia               # sozinho funciona (sem ganho de paralelismo)
vendor/bin/pest --tia --fresh       # descarta o grafo e re-grava do zero
vendor/bin/pest --tia --filtered    # carrega no PHPUnit só os arquivos afetados
vendor/bin/pest --no-tia            # desativa em uma execução
vendor/bin/pest --baseline          # imprime o path do storage do grafo
```

> **Replay não é atalho que pula trabalho.** A doc é explícita: cada teste em cache guarda tudo que produziu, **inclusive as linhas e branches cobertos** — um run replayado reporta a mesma cobertura de um run completo. É por isso que o `--tia` pode ser usado na Verificação Final sem perder confiança.


**Onde encaixa no fluxo da skill**:

- **Durante a implementação** (passo a passo do PRD): `--parallel --tia` a cada passo concluído. Feedback em segundos em vez de minutos, o que torna viável rodar o suite **a cada passo** e não só no final.
- **Na Verificação Final**: `--tia` responde "o que mais no sistema meu diff afetou?" — isto é exatamente a seção `## Impacto em Features Existentes` do PRD, agora verificável em vez de especulativa. Divergência entre o previsto no PRD e o que o TIA marcou como afetado → registrar em "Desvios do Plano" do `03-progresso.md`.
- **CT-B**: o TIA mapeia assets de browser. Se o projeto tem CT-B, registrar o watch no `tests/Pest.php`:

  ```php
  pest()->tia()->watch([
      'public/build/**/*' => 'tests/Browser',
  ]);
  ```

- **Ativação sem flag** (recomendado pela doc do Pest): `pest()->tia()->locally()` no `tests/Pest.php` — liga localmente e desliga sozinho em CI.

> Cache fica em `~/.pest/tia/<project-key>/` (caminho via `--baseline`). Edições cosméticas (whitespace, comentários, docblocks) são normalizadas e **não** disparam testes.

### Agent plugin (`--agent`) — verificação pontual durante a implementação

```bash
composer require pestphp/pest-plugin-agent --dev
```

Executa um snippet PHP dentro da configuração real do Pest do projeto e devolve pass/fail definitivo — em vez de o agente "achar" que funcionou:

```bash
# backend
vendor/bin/pest --agent='$u = \App\Models\User::factory()->create(); $this->actingAs($u)->get("/dashboard")->assertOk();'

# UI + backend na mesma verificação (requer pest-plugin-browser)
vendor/bin/pest --agent='visit("/contato")->type("email", "a@b.com")->press("Enviar")->assertSee("Mensagem enviada");'
```

Regras: aspas simples envolvendo o snippet, aspas duplas para strings PHP internas, **classes sempre com FQN** (`\App\Models\User`). Vários `--agent` na mesma chamada rodam isolados.


### Outros recursos do Pest 5 úteis à skill

| Recurso | Comando | Uso na skill |
|---|---|---|
| Sharding por tempo real | `pest --update-shards` / `--shard=1/4` | CI de features grandes com muitos CT-B |
| Profiling | `pest --profile` | Investigar CT lento antes de aceitar o tempo como normal |
| Type coverage | `pest --type-coverage` | Verificação Final em features com muito DTO/enum |
| Mutation testing | `pest --mutate` | Features de regra de negócio crítica (cálculo, cobrança) — ver a armadilha do Windows acima |
| Novos matchers | `toBeEmail()`, `toBeUlid()`, `toBeIpAddress()`, `toBeMacAddress()`, `toBeHostname()`, `toBeDomain()`, `toBeBase64()`, `toBeHexadecimal()` | Substituem regex custom nos CTs — aplicar a escada do Ponytail |
