# Roteiro de Teste Manual — FERRO-812: Cupons de desconto

> **Para quem**: desenvolvedor, revisor do PR e QA humano na homologação.
> **Requisito/Casos**: [00-requisito.md](00-requisito.md) · [04-casos-de-teste.md](04-casos-de-teste.md).
> **Base**: cópia fornecida, sem metadados Git (`git rev-parse` falha); 2026-10-20. Integridade: `validation/integrity-before.json`.
> **Vias**: terminal e aplicação.
> **Conferência**: 12 de 24 roteiros executados pela sessão — 6 aderentes e 6 divergentes. Os 12 roteiros de aplicação não foram executados.
> **Auditoria**: pendente — próximo ciclo do quality gate. O step 11 não foi executado nesta sessão.
> **Sessão**: Codex em Windows/PowerShell; modelo GPT-6, variante e esforço efetivos não informados pelo host.
> **Skill**: `.ai/skills/feature-wiki/SKILL.md`, `metadata.version: "4.2.0"`, lida integralmente.
> O resultado esperado vem do CT/RQ citado; o código somente determina como chegar à operação.

## Preparação do ambiente

Esta cópia e seus dados são descartáveis, conforme autorização explícita do desenvolvedor. Não utilize estes comandos em produção.
Não altere `.env`, código, configuração ou os arquivos 00–07. O `.env` original continua apontando para `:memory:`.
Use PowerShell na raiz `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-273d38`.

| # | Ação | Comando ou caminho | Como confirmar |
|---|---|---|---|
| 1 | Selecionar banco descartável em arquivo | `. ./validation/manual-env.ps1` | `DB_DATABASE` aponta para `validation/manual-single.sqlite`; `KIT_TENANCY=false`; cache de configuração e rotas aponta para arquivos inexistentes de `validation/` |
| 2 | Criar schema no arquivo novo | `php artisan migrate --no-interaction` | Migrations terminam sem erro. Não utilizar `migrate:fresh` |
| 3 | Gerar apenas permissões e papéis | Bloco PREP-SINGLE abaixo, em `php artisan tinker --no-interaction` | Nenhuma policy gerada; permissões e papéis existem no banco |
| 4 | Preparar personas e cupons para as telas | Continuação de PREP-SINGLE | PROMO10 e OUTRO ativos, usos 0; autor e administrador distintos; leitor sem escrita |
| 5 | Para os RM de aplicação, servir o banco escolhido | `php artisan serve --host=127.0.0.1 --port=8000 --no-interaction`, em outro terminal com o mesmo ambiente | Login local responde; `php artisan route:list --path=cupons --except-vendor --no-interaction` mostra as três rotas do Resource |
| 6 | Para os RM de duas organizações, selecionar schema próprio | PREP-TENANCY abaixo | `KIT_TENANCY=true` antes do boot; teams configurado antes das migrations; Acme e Globex existem |

Não usar `kit:tenancy`: esse comando reescreve configuração em disco. A preparação multi-tenant abaixo ajusta somente o processo.
Boost/search-docs/get-absolute-url/database-query não estão expostos nesta sessão. As rotas e APIs locais foram conferidas via Artisan e vendor/código instalado.
O endereço local acima corresponde ao comando de servidor documentado, não a uma URL resolvida pelo Boost.
Versões instaladas confirmadas por `composer show`: Laravel 13.25.0, Filament 5.7.6 e Pest 5.1.1; PHP CLI 8.4.10.

### PREP-SINGLE — executar no banco novo, uma vez

Cole este bloco em Tinker. A primeira configuração impede que o Shield escreva policies; não execute o seeder sem essa proteção nesta cópia.

```php
config(["filament-shield.policies.generate" => false]);
Illuminate\Support\Facades\Artisan::call("db:seed", ["--class" => Database\Seeders\ShieldPermissionsSeeder::class, "--no-interaction" => true]);
echo Illuminate\Support\Facades\Artisan::output();
Illuminate\Support\Facades\Artisan::call("db:seed", ["--class" => Database\Seeders\PapeisSeeder::class, "--no-interaction" => true]);
echo Illuminate\Support\Facades\Artisan::output();
$admin = App\Models\User::factory()->create(["name" => "Admin manual", "email" => "manual-admin@example.test"]);
$admin->assignRole("master_global");
$autor = App\Models\User::factory()->create(["name" => "Autor manual", "email" => "manual-autor@example.test"]);
$autor->assignRole("master_global");
$leitor = App\Models\User::factory()->create(["name" => "Leitor manual", "email" => "manual-leitor@example.test"]);
$leitor->assignRole("panel_user");
$infra = App\Models\User::factory()->create(["name" => "Infra manual", "email" => "manual-infra@example.test"]);
$infra->assignRole("infra");
Illuminate\Support\Facades\Auth::login($admin);
App\Models\Cupom::factory()->create(["codigo" => "PROMO10", "valor" => 10, "limite_de_usos" => 3, "expira_em" => "2026-11-01 15:00:00"]);
App\Models\Cupom::factory()->create(["codigo" => "OUTRO", "valor" => 10, "limite_de_usos" => 3, "expira_em" => "2026-11-01 15:00:00"]);
dump(App\Models\User::where("email", "like", "manual-%@example.test")->pluck("email"));
dump(App\Models\Cupom::get(["codigo", "tipo", "valor", "expira_em", "limite_de_usos", "usos"])->toArray());
```

As senhas vêm da factory existente (`password`), exclusivamente para contas fictícias locais. Não há credencial real neste documento.
O relógio do app é UTC. Nas telas single-tenant, `2026-11-01T12:00:00-03:00` corresponde a `2026-11-01 15:00:00`.
Campos de data devem preservar o instante, não apenas os números da hora do exemplo.

### PREP-TENANCY — processo independente, banco próprio

No PowerShell, carregue `manual-env.ps1`, depois defina `$env:KIT_TENANCY='true'` e
`$env:DB_DATABASE=Join-Path (Get-Location) 'validation/manual-tenancy.sqlite'`.
O arquivo deve existir e estar vazio na primeira preparação. Em seguida abra Tinker e cole:

```php
config(["permission.teams" => true, "filament-shield.tenant_model" => App\Models\Tenant::class, "filament-shield.policies.generate" => false]);
app()->forgetInstance(Spatie\Permission\PermissionRegistrar::class);
app(Spatie\Permission\PermissionRegistrar::class)->setPermissionsTeamId(App\Models\Tenant::CONTEXTO_GLOBAL);
Illuminate\Support\Facades\Artisan::call("migrate", ["--force" => true]);
echo Illuminate\Support\Facades\Artisan::output();
Illuminate\Support\Facades\Artisan::call("db:seed", ["--class" => Database\Seeders\ShieldPermissionsSeeder::class, "--no-interaction" => true]);
echo Illuminate\Support\Facades\Artisan::output();
Illuminate\Support\Facades\Artisan::call("db:seed", ["--class" => Database\Seeders\PapeisSeeder::class, "--no-interaction" => true]);
echo Illuminate\Support\Facades\Artisan::output();
$acme = App\Models\Tenant::factory()->create(["nome" => "Acme manual", "slug" => "acme-manual"]);
$globex = App\Models\Tenant::factory()->create(["nome" => "Globex manual", "slug" => "globex-manual"]);
$admin = App\Models\User::factory()->create(["email" => "manual-admin@example.test"]);
$admin->assignRole("master_global");
$admin->tenants()->attach([$acme->id, $globex->id]);
dump(config("kit.tenancy.enabled"), config("permission.teams"), $acme->slug, $globex->slug);
```

Para os RM de tela multi-tenant, use um processo que alinhe as mesmas chaves de teams antes de servir a aplicação.
Nesta sessão não houve tal servidor nem navegação multi-tenant: esses RM permanecem não executados.
Não use o banco com teams em servidor cujo `permission.teams` continue falso.
O `migrate` aninhado no Tinker rejeitou a opção global `--no-interaction` nesta instalação. A invocação externa de Tinker mantém `--no-interaction`; o migrate interno usa `--force` no arquivo descartável confirmado e não solicita resposta. A preparação corrigida foi reexecutada antes de conferir os RM dependentes.

## Dados e usuários de teste

| Papel/dado | Como obter | Estado necessário |
|---|---|---|
| Admin/operador B | PREP-SINGLE, `manual-admin@example.test`, master_global | Escrita autorizada no contexto single-tenant |
| Aplicador A | PREP-SINGLE, `manual-autor@example.test`, master_global | ID distinto de B; autor informado explicitamente ao motor |
| Leitor | PREP-SINGLE, `manual-leitor@example.test`, panel_user | Lista ativos; criação, edição e exclusão proibidas |
| Infra | PREP-SINGLE, `manual-infra@example.test`, infra | Não recebe autoridade de admin de cupons |
| PROMO10 / OUTRO | PREP-SINGLE | Porcentagem 10, limite 3, validade 2026-11-01 15:00 UTC, usos 0 e nenhuma aplicação |
| Organizações | PREP-TENANCY | Acme e Globex distintas, com schema de teams consistente |
| Pedido | Não existe nesta entrega | Motor recebe total em centavos. Não procurar uma tela de checkout |

### Convenção para os blocos de terminal

Cada RM de terminal roda isoladamente: abra Tinker com o ambiente e banco selecionados, cole o PRELÚDIO,
cole o bloco do RM e finalize com o ENCERRAMENTO. A transação permite observar gravações reais e desfaz somente os dados dessa execução.
Não trocar uma falha por aceite no esperado. Conferido significa executado, inclusive quando diverge do CT.

PRELÚDIO (também pode compor uma única chamada `php artisan tinker --no-interaction --execute '...'`):

```php
use App\Models\Cupom;
use App\Models\CupomUso;
use App\Models\User;
use App\Models\Tenant;
use Filament\Facades\Filament;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Date;
use Carbon\CarbonImmutable;
Date::setTestNow(CarbonImmutable::parse("2026-10-20T17:00:00Z"));
DB::beginTransaction();
$admin = User::where("email", "manual-admin@example.test")->firstOrFail();
Auth::setUser($admin);
```

Para RM-23 e RM-24, antes do PRELÚDIO, no processo com `KIT_TENANCY=true`, cole:

```php
config(["permission.teams" => true, "filament-shield.tenant_model" => App\Models\Tenant::class]);
app()->forgetInstance(Spatie\Permission\PermissionRegistrar::class);
app(Spatie\Permission\PermissionRegistrar::class)->setPermissionsTeamId(App\Models\Tenant::CONTEXTO_GLOBAL);
```

ENCERRAMENTO, inclusive após erro (na execução via `--execute`, usar `try/finally`):

```php
DB::rollBack();
Date::setTestNow();
Filament::setTenant(null, isQuiet: true);
```

Nos RM de tela, antes de cada fluxo, fotografe o estado pelo terminal local, sem screenshot de dados pessoais:
`Cupom::get()->toArray()` e `DB::table("cupom_usos")->orderBy("id")->get()->toArray()`.
Use um snapshot separado por cenário; registros de outros RM não entram na contagem da tentativa.
Depois de uma edição, compare os cinco campos, identidade e organização; compare usos e cada linha da trilha antes/depois.

## Roteiros

### RM-01 — Cadastrar os dois tipos · Via: aplicação

**Origem**: RQ-01 · RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · CT-01 · CT-02
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Entrar como admin e abrir criação | Login local; rota `filament.app.resources.cupons.create`, `/app/cupons/create` | Formulário apresenta código, tipo, valor, validade e limite | CT-01 | |
| 2 | Criar NOVO porcentagem 29, validade 01/11/2026 15:00 UTC, limite 3 | Preencher e clicar no botão de criação; reler registro no terminal | Exatamente um NOVO no contexto, com os cinco campos informados, usos 0 e nenhuma linha de aplicação | CT-02 · RQ-01 | |
| 3 | Repetir em fixture independente com NOVO, tipo fixo e valor 101 | Novo cenário sem NOVO preexistente | Exatamente um NOVO de tipo fixo, valor 101 centavos, mesma validade e limite 3; usos 0 e nenhuma aplicação | CT-02 | |

### RM-02 — Editar sem consumir uso · Via: aplicação

**Origem**: RQ-01 · CT-01 · CT-03
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar PROMO10 com um consumo real e copiar a trilha | Tinker: `$c=Cupom::where("codigo","PROMO10")->firstOrFail(); $c->aplicarEm(10000,$admin);` | Estado de partida: PROMO10 porcentagem 10, usos 1 e uma linha de uso identificada | prep · CT-03 | |
| 2 | Abrir edição pelo UUID | Rota `filament.app.resources.cupons.edit`, `/app/cupons/{uuid}/edit` | Cinco campos correspondem ao persistido; abertura não altera usos nem cria linha | CT-01 | |
| 3 | Salvar NOVO, fixo, 1001, validade 02/11/2026 18:00 UTC, limite 4 | Formulário de edição; reler DB | Mesma identidade com os cinco valores novos; usos permanece 1 e a única linha anterior permanece idêntica | CT-03 | |

### RM-03 — Salvar o próprio código · Via: aplicação

**Origem**: RQ-01 · RQ-14 · CT-05
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Salvar edição de PROMO10 ativo sem mudar nenhum campo | `/app/cupons/{uuid}/edit`, admin, Salvar | Um único PROMO10 com os mesmos valores e identidade; nenhum erro de duplicidade, nenhum uso criado e contador inalterado | CT-05 · RQ-14 | |

### RM-04 — Excluir cadastro ativo e inativo · Via: aplicação

**Origem**: RQ-01 · RQ-07 · CT-04 · CT-55
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar OUTRO ativo e alvo independente para cada estado | Ativo; esgotado por três aplicações reais; expirado por avançar relógio após cadastro; ambos por consumo seguido de tempo | Estado inicial correspondente à linha de Exemplos; copiar todos os campos e trilha de OUTRO antes de excluir | prep · CT-04 · CT-55 | |
| 2 | Excluir alvo ativo pela ação da listagem | Admin, `/app/cupons`, Excluir e confirmação | Alvo ausente do cadastro e listagem; OUTRO preserva todos os campos, usos 0 e trilha vazia | CT-04 | |
| 3 | Excluir cada um dos três alvos inativos em fixtures independentes | Ação Excluir como admin da Acme | Alvo ausente do cadastro e listagem; OUTRO preserva cinco campos, organização, contador e linhas de uso | CT-55 | |

### RM-05 — Listar somente ativos da organização · Via: aplicação

**Origem**: RQ-08 · CT-45 · CT-46
**Conferência**: não executado — navegador ausente; servidor multi-tenant com teams alinhado não foi preparado.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar leitor da Acme, histórico prévio e dois tipos em cada estado | PREP-TENANCY; vínculo e papel panel_user na Acme; ativo com saldo, expirado, esgotado, ambos, removido; ativo na Globex | Estado de partida do CT; esgotamento por aplicações reais e expiração por relógio, sem forjar contador | prep · CT-45 | |
| 2 | Abrir lista como leitor da Acme | `/app/acme-manual/cupons` | Somente ativos da Acme presentes, com código e tipo corretos; quatro estados inelegíveis e Globex ausentes; campos, contador e trilha inalterados | CT-45 · RQ-08 | |
| 3 | Repetir em fixture com p+1 ativos; percorrer todas as páginas | p é tamanho observado da página; anotar UUIDs da primeira à última | União dos UUIDs exatamente igual aos p+1 ativos da Acme, sem repetidos/inativos/Globex; nenhum campo, uso ou linha alterado | CT-46, exemplo p+1 | |

### RM-06 — Aplicar novamente e registrar uma só vez · Via: terminal

**Origem**: RQ-12 · RQ-13 · RQ-15 · CT-39
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-06.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar fixture para cada tipo, consumir uma vez e guardar linha anterior | Primeira parte do bloco abaixo | Cupom de limite 3 com um uso real e uma linha identificada | prep · CT-39 | Dois tipos criados, cada um com um uso real e linha anterior copiada. |
| 2 | Aplicar novamente a 10000 centavos e reler | Segunda parte do bloco abaixo | Para cada tipo: total 9000, contador exatamente 2, exatamente duas linhas; anterior idêntica, só uma nova com cupom e autor atuais | CT-39 · RQ-12 · RQ-13 · RQ-15 | Porcentagem e fixo: total 9000, usos 2, duas linhas com cupom/autor corretos; anterior_identica=true. |

```php
foreach (["porcentagem", "fixo"] as $tipo) {
    $c = Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    $c->aplicarEm(10000, $admin);
    $antes = DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toArray();
    $total = $c->aplicarEm(10000, $admin);
    $linhas = DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toArray();
    dump(["tipo" => $tipo, "total" => $total, "usos" => $c->fresh()->usos, "linhas" => $linhas, "anterior_identica" => $antes[0] == $linhas[0]]);
}
```

### RM-07 — Registrar autor explícito e instante da aplicação · Via: terminal

**Origem**: RQ-15 · CT-42 · CT-44
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-07.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | B cadastrar cada tipo às 14h -03 e manter sessão B; A é distinto | Bloco abaixo até a troca do relógio | Cupom ativo criado por B, usos 0; A é aplicador autorizado explicitamente informado | prep · CT-42 · CT-44 | B=id 1; A=id 2; cadastro às 17:00:00 UTC, sessão B mantida. |
| 2 | A aplicar às 23:30:17 -03 sobre 10000 | Restante do bloco; inspecionar linha | Total 9000, usos 1 e uma única linha com cupom correto, aplicado_por_id de A e instante 2026-10-21T02:30:17Z; não atribuir a B nem usar instante do cadastro | CT-42 · CT-44 · RQ-15 | Ambos os tipos: total 9000, usos 1, uma linha com aplicado_por_id=2 e created_at=2026-10-21 02:30:17 UTC; sessão B=id 1. |

```php
$a = User::where("email", "manual-autor@example.test")->firstOrFail();
foreach (["porcentagem", "fixo"] as $tipo) {
    Date::setTestNow(CarbonImmutable::parse("2026-10-20T14:00:00-03:00"));
    $c = Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    Date::setTestNow(CarbonImmutable::parse("2026-10-20T23:30:17-03:00"));
    $total = $c->aplicarEm(10000, $a);
    dump(["tipo" => $tipo, "sessao_B" => Auth::id(), "autor_A" => $a->id, "total" => $total, "usos" => $c->fresh()->usos, "linhas" => DB::table("cupom_usos")->where("cupom_id", $c->id)->get()->toArray()]);
}
```

## Casos negativos e permissões

### RM-08 — Consultar inexistente, null e vazio · Via: terminal

**Origem**: RQ-09 · CT-29
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-08.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Usar PROMO10 ativo com usos 0 e limite 3 | PREP-SINGLE | Fixture do Dado; não existe DESCONHECIDO | prep · CT-29 | PROMO10 ativo, usos 0, limite 3; DESCONHECIDO ausente. |
| 2 | Consultar cada entrada, aplicar somente se encontrada | Bloco abaixo; três exemplos de recusa | Nenhum cupom nem total descontado; PROMO10 com cinco campos preservados, usos 0 e nenhuma linha de aplicação | CT-29 · RQ-09 | Três consultas retornaram null e nenhum total; campos_identicos=true, usos=0, linhas=0. Log observado: Código recusado; motivo nao_encontrado para DESCONHECIDO e codigo_vazio para null/vazio. |

```php
$p = Cupom::where("codigo", "PROMO10")->firstOrFail();
$antes = $p->getRawOriginal();
foreach (["DESCONHECIDO", null, ""] as $codigo) {
    $c = Cupom::valido($codigo);
    dump(["codigo" => $codigo, "encontrado" => $c?->id, "total" => $c?->aplicarEm(10000, $admin)]);
}
dump(["campos_identicos" => $antes === $p->fresh()->getRawOriginal(), "usos" => $p->fresh()->usos, "linhas" => DB::table("cupom_usos")->where("cupom_id", $p->id)->count()]);
```

### RM-09 — Recusar quarta aplicação · Via: terminal

**Origem**: RQ-11 · RQ-13 · RQ-15 · CT-41
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-09.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Consumir três vezes cada tipo de limite 3 | Primeiro trecho do bloco | Esgotado por três aplicações reais, três linhas de uso | prep · CT-41 | Dois tipos atingiram usos 3 por três aplicações reais, com três linhas anteriores. |
| 2 | Tentar quarta aplicação e registrar motivo da recusa | `aplicarEm`, catch e releitura | Nenhum total descontado, contador 3, três linhas anteriores idênticas e nenhuma quarta; recusa por falta de saldo | CT-41 · RQ-11 | Ambos: RuntimeException: Este cupom não está mais disponível.; sem total; usos=3, linhas=3 e trilha_identica=true. |

```php
foreach (["porcentagem", "fixo"] as $tipo) {
    $c = Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    for ($i = 0; $i < 3; $i++) { $c->aplicarEm(10000, $admin); }
    $antes = DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toJson();
    try { dump(["total_indevido" => $c->aplicarEm(10000, $admin)]); }
    catch (Throwable $e) { dump(["recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
    dump(["tipo" => $tipo, "usos" => $c->fresh()->usos, "linhas" => DB::table("cupom_usos")->where("cupom_id", $c->id)->count(), "trilha_identica" => $antes === DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toJson()]);
}
```

### RM-10 — Referência removida não aplica nem reaparece · Via: terminal

**Origem**: RQ-09 · CT-30 · CT-48
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-10.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Guardar OUTRO ativo e carregar/remover um alvo de cada tipo como admin | Primeiro trecho do bloco | Referência em memória para alvo já removido; OUTRO sem uso | prep · CT-30 · CT-48 | Referência ativa carregada e removida como admin para cada tipo; OUTRO fotografado. |
| 2 | Consultar novamente código e aplicar referência removida | Restante do bloco | Consulta ausente; aplicação recusada por identidade indisponível, sem total descontado, recriação ou uso para identidade removida; OUTRO preserva campos, usos 0 e trilha vazia | CT-30 · CT-48 | Ambos: consulta=null; RuntimeException: Este cupom não está mais disponível.; recriado=false, linhas_alvo=0; outro_identico=true, usos_outro=0 e linhas_outro=0. |

```php
$outro = Cupom::where("codigo", "OUTRO")->firstOrFail();
$antes = $outro->getRawOriginal();
foreach (["porcentagem", "fixo"] as $tipo) {
    $c = Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    $id = $c->id; $codigo = $c->codigo;
    Cupom::findOrFail($id)->delete();
    dump(["tipo" => $tipo, "consulta" => Cupom::valido($codigo)?->id]);
    try { dump(["total_indevido" => $c->aplicarEm(10000, $admin)]); }
    catch (Throwable $e) { dump(["recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
    dump(["recriado" => Cupom::whereKey($id)->exists(), "linhas_alvo" => DB::table("cupom_usos")->where("cupom_id", $id)->count()]);
}
dump(["outro_identico" => $antes === $outro->fresh()->getRawOriginal(), "usos_outro" => $outro->fresh()->usos, "linhas_outro" => DB::table("cupom_usos")->where("cupom_id", $outro->id)->count()]);
```

### RM-11 — Leitor não escreve diretamente pelo model · Via: terminal

**Origem**: RQ-07 · RQ-08 · CT-22
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-11.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Selecionar panel_user, payload válido e PROMO10 ativo | PREP-SINGLE; subtransação independente por verbo no bloco | Ator sem permissão; cadastro e trilha fotografados | prep · CT-22 | panel_user autenticado no contexto do terminal; subtransação e snapshot por verbo. |
| 2 | Criar, editar e excluir diretamente sem Gate manual | Três verbos do bloco; comparar antes de rollback | Cada verbo recusado por autorização; nenhum cadastro criado, nenhum dos cinco campos alterado, PROMO10 não removido, contador e trilha inalterados | CT-22, linhas panel_user single-tenant · RQ-07 | DIVERGÊNCIA: três verbos ACEITA, sem exceção; criar delta +1, editar mudou original, excluir delta -1; trilha permaneceu igual. |

```php
$leitor = User::where("email", "manual-leitor@example.test")->firstOrFail();
Auth::setUser($leitor);
foreach (["criar", "editar", "excluir"] as $acao) {
    DB::beginTransaction();
    $p = Cupom::where("codigo", "PROMO10")->firstOrFail();
    $antes = $p->getRawOriginal(); $quantidade = Cupom::count(); $trilha = DB::table("cupom_usos")->orderBy("id")->get()->toJson();
    try {
        if ($acao === "criar") { Cupom::factory()->create(["codigo" => "DIRETO", "valor" => 10, "limite_de_usos" => 3]); }
        if ($acao === "editar") { $p->update(["valor" => 20]); }
        if ($acao === "excluir") { $p->delete(); }
        dump(["acao" => $acao, "resultado" => "ACEITA"]);
    } catch (Throwable $e) { dump(["acao" => $acao, "recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
    $depois = Cupom::find($p->id);
    dump(["delta_cadastro" => Cupom::count() - $quantidade, "original_preservado" => $depois?->getRawOriginal() === $antes, "trilha_identica" => $trilha === DB::table("cupom_usos")->orderBy("id")->get()->toJson()]);
    DB::rollBack();
}
```

### RM-12 — Duplicidade direta com tenant nulo · Via: terminal

**Origem**: RQ-14 · CT-20
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-12.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Selecionar PROMO10 original, sem uso | Início do bloco, single-tenant | Código já ocupado no contexto nulo | prep · CT-20 | PROMO10 original selecionado com usos 0 e trilha fotografada. |
| 2 | Criar outro PROMO10 diretamente | `Cupom::factory()->create`, sem formulário | Recusa por duplicidade; somente um PROMO10; identidade e cinco campos preexistentes preservados; contador e linhas inalterados | CT-20, criar single-tenant nulo · RQ-14 | DIVERGÊNCIA: criação aceita sem exceção; quantidade_PROMO10=2; original preservado, usos 0 e trilha idêntica. |

```php
$p = Cupom::where("codigo", "PROMO10")->firstOrFail(); $antes = $p->getRawOriginal();
$trilha = DB::table("cupom_usos")->orderBy("id")->get()->toJson();
try { $novo = Cupom::factory()->create(["codigo" => "PROMO10", "valor" => 10, "limite_de_usos" => 3]); dump(["criado" => $novo->id]); }
catch (Throwable $e) { dump(["recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
dump(["quantidade_PROMO10" => Cupom::where("codigo", "PROMO10")->count(), "original_preservado" => $antes === $p->fresh()->getRawOriginal(), "usos" => $p->fresh()->usos, "trilha_identica" => $trilha === DB::table("cupom_usos")->orderBy("id")->get()->toJson()]);
```

### RM-13 — Rejeitar percentual 101 fora do formulário · Via: terminal

**Origem**: RQ-04 · CT-12
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-13.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Admin criar por model com demais dados válidos, porcentagem 101 | Bloco abaixo | Recusa pelo valor fora do domínio; nenhum cupom novo ou alteração de cadastro preexistente, consumo ou linha de uso | CT-12, porcentagem 101 criar | DIVERGÊNCIA: criação aceita sem exceção, valor_persistido=101; cadastro_identico=false; trilha_identica=true. |

```php
$antes = Cupom::orderBy("id")->get()->toJson(); $trilha = DB::table("cupom_usos")->orderBy("id")->get()->toJson();
try { $c = Cupom::factory()->create(["tipo" => "porcentagem", "valor" => 101, "limite_de_usos" => 3]); dump(["criado" => $c->id, "valor_persistido" => $c->fresh()->valor]); }
catch (Throwable $e) { dump(["recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
dump(["cadastro_identico" => $antes === Cupom::orderBy("id")->get()->toJson(), "trilha_identica" => $trilha === DB::table("cupom_usos")->orderBy("id")->get()->toJson()]);
```

### RM-14 — Rejeitar limite fracionário fora do formulário · Via: terminal

**Origem**: RQ-06 · CT-16
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-14.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Admin criar com limite 1.5 e demais dados válidos | Bloco abaixo, exemplo fração/criar | Recusa pela contagem fracionária, sem persistir limite convertido; cadastro anterior, contador e trilha preservados | CT-16 | DIVERGÊNCIA: criação aceita sem exceção; limite_DB=1.5 e limite_model=1; cadastro alterado e trilha idêntica. |

```php
$antes = Cupom::orderBy("id")->get()->toJson(); $trilha = DB::table("cupom_usos")->orderBy("id")->get()->toJson();
try { $c = Cupom::factory()->create(["valor" => 10, "limite_de_usos" => 1.5]); dump(["criado" => $c->id, "limite_model" => $c->fresh()->limite_de_usos, "limite_DB" => DB::table("cupons")->where("id", $c->id)->value("limite_de_usos")]); }
catch (Throwable $e) { dump(["recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
dump(["cadastro_identico" => $antes === Cupom::orderBy("id")->get()->toJson(), "trilha_identica" => $trilha === DB::table("cupom_usos")->orderBy("id")->get()->toJson()]);
```

### RM-15 — Recusar consumo sem autor · Via: terminal

**Origem**: RQ-15 · CT-54
**Conferência**: conferido pela sessão 2026-10-20 — aderente ao recorte do CT. Saída literal: `validation/RM-15.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar cada tipo com usos 0 e limite 3 | Início de cada iteração | Cupom e autor real existentes, sem aplicação | prep · CT-54 | Quatro fixtures independentes, dois tipos e duas formas de ausência; snapshots relidos do DB. |
| 2 | Omitir autor e passar null, em fixtures independentes | Duas entradas por tipo no bloco | Recusa sem total descontado; campos e contador 0 preservados, nenhuma linha anônima ou atribuída por default | CT-54 · RQ-15 | Ausente: ArgumentCountError (exactly 2 expected). Null: TypeError (must be of type App\Models\User, null given). Quatro casos: campos_identicos=true, usos=0 e linhas=0. |

```php
foreach (["porcentagem", "fixo"] as $tipo) {
    foreach (["ausente", "null"] as $autoria) {
        $c = Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3])->fresh(); $antes = $c->getRawOriginal();
        try { $total = $autoria === "ausente" ? $c->aplicarEm(10000) : $c->aplicarEm(10000, null); dump(["total_indevido" => $total]); }
        catch (Throwable $e) { dump(["tipo" => $tipo, "autoria" => $autoria, "recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
        dump(["campos_identicos" => $antes === $c->fresh()->getRawOriginal(), "usos" => $c->fresh()->usos, "linhas" => DB::table("cupom_usos")->where("cupom_id", $c->id)->count()]);
    }
}
```

### RM-16 — Campos obrigatórios em criação e edição · Via: aplicação

**Origem**: RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · CT-06 · CT-07
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar com um único campo vazio; repetir pelos cinco campos | Admin, `/app/cupons/create`, demais campos válidos | Erro especificamente no campo vazio; nenhum cupom novo, consumo ou linha de aplicação | CT-06, exemplos vazio | |
| 2 | Editar PROMO10 com uso real e apagar um campo por tentativa | Admin, `/app/cupons/{uuid}/edit`; snapshot independente | Erro especificamente no campo; cinco valores originais preservados, usos 1 e linha anterior idêntica | CT-07, exemplos vazio | |

### RM-17 — Valor percentual e representação de limite inválidos · Via: aplicação

**Origem**: RQ-04 · RQ-06 · CT-11 · CT-14
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Tentar porcentagem 101 em criação e edição, demais campos válidos | Formulários como admin, fixture independente por verbo | Recusado com erro só em valor, nenhum cupom novo e nenhum campo, uso ou trilha alterado | CT-11, 101 criar/editar | |
| 2 | Tentar limite três e 1.5 em criação e edição | Campo Limite de usos | Erro especificamente em limite_de_usos; cadastro, contador e trilha iguais ao estado anterior | CT-14, texto/fração criar/editar | |

### RM-18 — Duplicidade no formulário · Via: aplicação

**Origem**: RQ-14 · CT-18 · CT-19
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar PROMO10 quando já existe | Admin, criação no mesmo contexto | Erro em codigo; só original com cinco campos, usos e trilha iguais | CT-18 · RQ-14 | |
| 2 | Preparar OUTRO com um uso real | Tinker `aplicarEm(10000,$admin)` e snapshot | OUTRO tem usos 1 e uma linha identificada | prep · CT-19 | |
| 3 | Renomear OUTRO para PROMO10 | Editar OUTRO no mesmo contexto | Erro em codigo; dois códigos e campos originais preservados, usos de OUTRO 1 e linha anterior idêntica | CT-19 | |

### RM-19 — Leitor e infra sem escrita na tela; saída após recusa · Via: aplicação

**Origem**: RQ-07 · RQ-08 · CT-21 · CT-24
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como leitor, tentar criar, editar e excluir PROMO10 | Rotas diretas e ação de listagem; um verbo por tentativa | Recusa por autorização em cada verbo; nenhum cupom criado/removido, cinco campos originais, contador e trilha inalterados | CT-21, panel_user single-tenant | |
| 2 | Como infra, repetir os três verbos | Rotas do Resource; confirmar recusa por perfil sem admin | Mesmas ausências de efeitos: nenhum cadastro, edição, exclusão, incremento ou linha de uso | CT-21, infra global | |
| 3 | Como leitor da Acme, sair da recusa e abrir a lista | `/app/acme-manual/cupons` | Lista alcançável mostra PROMO10 com código e tipo corretos, sem retornar à tela recusada; campos, usos 0 e trilha vazia preservados | CT-24 | |

### RM-20 — UUID alheio e inexistente · Via: aplicação

**Origem**: RQ-01 · RQ-07 · RQ-09 · CT-25 · CT-49
**Conferência**: não executado — navegador ausente; fluxo multi-tenant não servido.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar admin apenas da Acme e OUTRO de Globex com um uso real | PREP-TENANCY; atribuir admin_organizacao no team Acme, sem master_global | Snapshot do cadastro/trilha de ambos; ator sem autoridade em Globex | prep · CT-25 | |
| 2 | Usar UUID de Globex na edição/ação da Acme | `/app/acme-manual/cupons/{uuid-globex}/edit`; tentar abrir, salvar valor 20 e excluir | Cada operação recusada sem expor cinco campos alheios; organização, valor, identidades, contadores e todas as linhas preservados; nenhum cadastro criado/apagado | CT-25 | |
| 3 | Como admin, abrir edição de UUID nunca existente | `/app/cupons/{uuid-inexistente}/edit`, fixture single-tenant com OUTRO | Não recria identidade nem altera OUTRO; cinco campos de OUTRO, usos 0 e trilha vazia preservados; listagem autorizada continua como saída | CT-49, abrir edição inexistente | |

### RM-21 — Mudar tipo para fixo e preservar centavos · Via: aplicação

**Origem**: RQ-03 · RQ-04 · CT-13 · CT-50
**Conferência**: não executado — navegador conectado e Playwright MCP ausentes.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Partir de porcentagem 29 em criação e edição, trocar para fixo 101 e salvar | Formulários como admin, fixtures independentes | Schema representa fixo 101 centavos e permite salvar; registro tem fixo e valor 101 sem teto percentual; gravação não cria aplicação nem incrementa usos | CT-50 · CT-13, 101 criar/editar | |

### RM-22 — Mesmo código em organizações distintas · Via: aplicação

**Origem**: RQ-14 · CT-51
**Conferência**: não executado — navegador ausente; servidor multi-tenant com teams alinhado não preparado.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar PROMO10 da Acme e OUTRO da Globex | PREP-TENANCY; admin local da Globex e snapshots de ambas | Cinco campos corretos e identidade de OUTRO conhecida | prep · CT-51 | |
| 2 | Criar PROMO10 na Globex; em fixture independente renomear OUTRO | `/app/globex-manual/cupons/create` e edição de OUTRO | Um PROMO10 em cada organização; edição preserva identidade de OUTRO; cinco campos, contador e todas as linhas de uso da Acme iguais ao snapshot | CT-51 · RQ-14 | |

### RM-23 — Tenancy sem contexto deve fechar consulta · Via: terminal

**Origem**: RQ-09 · CT-27
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-23.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar ativos de Acme/Globex e legado nulo | PREP-TENANCY, bloco abaixo; ambos os contextos reais | Três cupons ativos distintos, sem usos; tenancy ligada | prep · CT-27 | Acme tenant 1, Globex tenant 2, legado tenant null; tenancy e teams true. |
| 2 | Remover contexto e consultar código diretamente | `Filament::setTenant(null)` e `Cupom::valido` | Nenhum dos três cupons retornado nem consumido; campos, contadores e linhas das três origens iguais | CT-27, consultar código diretamente | DIVERGÊNCIA: os três códigos retornaram seus IDs sem recusa; campos_identicos=true, usos=[0,0,0], linhas=0. |

```php
$acme = Tenant::where("slug", "acme-manual")->firstOrFail(); $globex = Tenant::where("slug", "globex-manual")->firstOrFail();
$cupons = [];
foreach ([$acme, $globex, null] as $tenant) {
    Filament::setTenant($tenant, isQuiet: true);
    $cupons[] = Cupom::factory()->create(["valor" => 10, "limite_de_usos" => 3]);
}
$antes = array_map(fn ($c) => $c->fresh()->getRawOriginal(), $cupons);
Filament::setTenant(null, isQuiet: true);
foreach ($cupons as $c) { dump(["tenant" => $c->tenant_id, "codigo" => $c->codigo, "retornado" => Cupom::valido($c->codigo)?->id]); }
dump(["campos_identicos" => $antes === array_map(fn ($c) => $c->fresh()->getRawOriginal(), $cupons), "usos" => array_map(fn ($c) => $c->fresh()->usos, $cupons), "linhas" => DB::table("cupom_usos")->whereIn("cupom_id", array_map(fn ($c) => $c->id, $cupons))->count()]);
```

### RM-24 — Referência alheia não pode ser editada ou excluída · Via: terminal

**Origem**: RQ-07 · CT-52
**Conferência**: conferido pela sessão 2026-10-20 — divergente do CT. Saída literal: `validation/RM-24.txt`; processo exit 0, que não significa aceite do cenário.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar admin somente da Acme e referência carregada na Globex com uso real | PREP-TENANCY e bloco abaixo | Registro alheio com cinco campos, organização, identidade, contador 1 e linha conhecida | prep · CT-52 | Admin local somente na Acme; alvo de Globex com um consumo real, snapshot por verbo. |
| 2 | Trocar para Acme e editar/excluir referência, sem Gate manual | Duas subtransações independentes do bloco | Cada tentativa recusada por organização; cinco campos, identidade, organização, contador e todas as linhas de uso da Globex preservados | CT-52 | DIVERGÊNCIA: editar e excluir ACEITA, sem exceção; registro_identico=false em ambos; trilha idêntica na edição e removida na exclusão. |

```php
$acme = Tenant::where("slug", "acme-manual")->firstOrFail(); $globex = Tenant::where("slug", "globex-manual")->firstOrFail();
$local = User::factory()->create(); $local->tenants()->attach($acme->id);
app(Spatie\Permission\PermissionRegistrar::class)->setPermissionsTeamId($acme->id);
$local->assignRole("admin_organizacao");
foreach (["editar", "excluir"] as $acao) {
    DB::beginTransaction();
    Filament::setTenant($globex, isQuiet: true); Auth::setUser($admin);
    $c = Cupom::factory()->create(["valor" => 10, "limite_de_usos" => 3]); $c->aplicarEm(10000, $admin);
    $antes = $c->fresh()->getRawOriginal(); $trilha = DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toJson();
    Filament::setTenant($acme, isQuiet: true); Auth::setUser($local);
    try {
        if ($acao === "editar") { $c->update(["valor" => 20]); }
        else { $c->delete(); }
        dump(["acao" => $acao, "resultado" => "ACEITA"]);
    } catch (Throwable $e) { dump(["acao" => $acao, "recusa" => get_class($e), "mensagem" => $e->getMessage()]); }
    Filament::setTenant($globex, isQuiet: true);
    dump(["registro_identico" => $antes === $c->fresh()?->getRawOriginal(), "trilha_identica" => $trilha === DB::table("cupom_usos")->where("cupom_id", $c->id)->orderBy("id")->get()->toJson()]);
    DB::rollBack();
}
```

## Limpeza

- Os blocos de terminal encerram com rollback da sua própria transação, incluindo quando há divergência. Não desfazer a transação antes de observar o resultado.
- Parar apenas o servidor que o executor tiver iniciado nesta validação. Esta sessão não deixou servidor de aplicação.
- Preservar `validation/manual-single.sqlite`, `validation/manual-tenancy.sqlite` e os logs até a revisão das divergências; não executar wipe, truncate ou fresh.
- Para repetir a preparação completa, escolher novos arquivos SQLite dentro de `validation/` e ajustar somente o ambiente do processo. Não reutilizar a criação de personas em banco já preparado.
- Não enviar e-mails reais; `MAIL_MAILER=log`. Não criar/alterar senhas reais nem acessar integrações de produção.

## Fora deste roteiro

| CT / recorte | Motivo de ser só automatizado ou ficar pendente |
|---|---|
| CT-36 | Disputa simultânea exige duas conexões, barreira e controle do interleaving; não é demonstrada por cliques sequenciais |
| CT-31 · CT-32 · CT-33 | Fronteiras de segundos e representação de fuso exigem relógio controlado; não esperar o relógio da tela |
| CT-37 · CT-38 | Precisão e arredondamento em todos os exemplos exigem asserções numéricas automatizadas; RM-06 não pretende cobrir essas bordas |
| CT-40 · CT-43 | Injeção de falhas antes/depois do INSERT e prova de rollback ficam na automação; não alterar código para simulá-las |
| CT-35 | Referência obsoleta após último uso precisa controle de duas instâncias e snapshot; RM-09 cobre somente esgotamento sequencial |
| CT-08 · CT-09 · CT-10 · CT-15 · CT-17 | Estruturas inválidas, casts e equivalência exata de instante não são conferidos por este roteiro de tela; permanecem no contrato automatizado |
| CT-23 | Combinação exaustiva de papéis pertence à matriz automatizada; personas manuais não demonstram todos os pares |
| CT-26 · CT-28 · CT-53 | Payload forjado e consumo com mudança de contexto são cenários de chamada controlada; os RM de isolamento não os substituem |
| CT-47 | Dupla inelegibilidade nos dois tipos e duas entradas exige fixtures independentes; não inferir do esgotamento isolado |
| CT-46 | RM-05 seleciona apenas o exemplo p+1; 0, 1, p e 2p+1 continuam automatizados |
| Mutantes | Mutação de implementação e MSI pertencem à automação; nenhum código foi modificado nesta sessão |
| Questões Q1–Q10 do 04 | Não transformar normalização, teto, renovação, retenção da trilha, ordem/rótulos ou outros recortes abertos em novos esperados |

O 05 está ausente porque o 04 declara `Sem CT-B`. Isso não elimina a utilidade do roteiro humano de tela.
Não foi criada entidade Pedido, tela de aplicação ou expectativa de retenção após excluir cupom com histórico.

## Registro de execução

| Data | Quem | Ambiente | Commit | RM executados | Resultado | Observações |
|---|---|---|---|---|---|---|
| 2026-10-20 | sessão Codex, GPT-6 (variante não exposta) | SQLite local descartável, Artisan/Tinker; dois bancos em validation/ | indisponível, cópia sem .git | RM-06–RM-15, RM-23 e RM-24 | 12 executados: 6 aderentes, 6 divergentes | Saídas validation/RM-*.txt. Nenhuma execução de telas; nenhum veredito de QA |

A contagem deriva dos cabeçalhos RM e das linhas Conferência, não de quantidade de comandos. Cada RM executado teve todos os seus passos rodados.
O bootstrap de single-tenant foi executado integralmente; o de multi-tenant foi corrigido após a rejeição da opção global do migrate e reexecutado integralmente.
RM-15 teve sua observação corrigida: o snapshot do model recém-criado diferia da releitura pelos defaults/casts. O snapshot agora usa fresh(); o bloco foi reexecutado e confirmou quatro recusas, sem mudança de dados. Não era defeito da aplicação.
A autenticação de terminal usa Auth::setUser, mantendo o ator no guard sem simular uma navegação de login. A preparação single-tenant executou Auth::login conforme documentado.

## Divergências e encaminhamento

| ID | RM / CT / origem | Divergência reproduzida | Encaminhamento |
|---|---|---|---|
| D-01 | RM-11 · CT-22 · RQ-07 | panel_user criou, editou e excluiu pelo model sem autorização; cada operação chegou ao banco | Implementação: retornar ao step 9 com CT existente; provar regressão antes de corrigir |
| D-02 | RM-12 · CT-20 · RQ-14 | Dois PROMO10 com tenant_id nulo; banco aceitou a duplicata | Implementação: unicidade single-tenant; não trocar a expectativa por duplicidade aceita |
| D-03 | RM-13 · CT-12 · RQ-04 | Porcentagem 101 persistida por model | Implementação: validação de domínio fora do formulário |
| D-04 | RM-14 · CT-16 · RQ-06 | Limite fracionário 1.5 persistido; leitura pelo model apresentou 1 | Implementação: impedir contagem inválida, sem conversão silenciosa |
| D-05 | RM-23 · CT-27 · RQ-09 | Tenancy ligada sem tenant retornou ativos de Acme, Globex e legado nulo | Implementação: fechar consulta quando falta contexto; não declarar sucesso com base no snapshot preservado |
| D-06 | RM-24 · CT-52 · RQ-07 | Admin somente da Acme editou e excluiu referência da Globex; exclusão apagou também a linha de uso | Implementação: proteger escrita direta pelo contexto; a remoção de trilha aqui é efeito colateral observado de operação proibida, sem decidir Q7 sobre retenção de exclusão autorizada |

Todos os efeitos foram observados antes do rollback. Esperados permaneceram conforme os CT existentes; não se alterou aplicação, teste ou 00–07.
Os seis achados estão abertos. Este 08 está entregue como roteiro com divergências, não como aprovação da feature.
Um achado de implementação coberto por RQ/CT existentes não será transformado em premissa nova.
O retorno ao step 9 e a repetição do step 10, quando necessários, ficarão pendentes para uma sessão autorizada.

## Verificação estática e desvios de processo

Comando exigido: `& 'C:\Program Files\Git\bin\bash.exe' '.ai/skills/feature-wiki/scripts/roteiro-manual.sh' 'wikis/specs/saida-g1/cupons-de-desconto'`.
Execução em 2026-10-20:

```text
stdout: (vazia)
stderr: (vazia)
exit: 0
```

Esse resultado valida os vínculos estáticos, não aprova os comportamentos divergentes.
Contagem por expressão regular sobre este arquivo: `^### RM-\d+` = 24; linhas de Conferência com `conferido pela sessão` = 12; com `não executado` = 12.
Manifesto SHA256: 283 arquivos preexistentes conferidos, 0 alterações/remoções; único arquivo novo nas áreas protegidas monitoradas: este 08.
Comando de integridade: reler cada `Path` de `validation/integrity-before.json` com `Get-FileHash -Algorithm SHA256` e comparar `Hash`; comparar também o inventário atual das mesmas áreas, excluindo somente o novo 08 permitido. Resultado em `validation/integrity-changes.txt`: vazio.

- A instrução do usuário proíbe editar 03. Por isso, saída do script, referências abertas, host, conferência e desvios são registrados somente neste 08 e no retorno da sessão.
- Sem despacho — esta etapa manda a sessão escrever o 08 em linha. Não houve revisão independente nem execução do step 11.
- Sem Git, a base não pode citar commit. Hashes locais detectam alterações; não demonstram ausência de leitura.
- Playwright MCP ausente no catálogo de ferramentas; `cua.getState()` retornou `apps: []` e `browsers: []`. Não houve execução de UI nem substituição por teste de componente apresentado como navegação.
- Sem edição PHP de aplicação ou testes, não executar Pint sobre arquivos protegidos. A verificação programática do documento é o script exigido pela etapa.
- A preparação multi-tenant precisou do ajuste de invocação do migrate descrito acima. Não foi editado arquivo de configuração; as flags de teams existem somente nos processos de Tinker.
- O ciclo de correção do step 9 e a reconciliação do step 10 não foram reabertos: o usuário proíbe alterações nos seus artefatos. Os seis achados ficam registrados para encaminhamento, sem modificar o oráculo ou inventar premissas.

## Referências abertas

- `.ai/skills/feature-wiki/references/hosts-e-subagentes.md` — contrato do host na etapa de roteiro manual.
- `.ai/skills/feature-wiki/references/template-08-roteiro-manual.md` — template e conferência da etapa entre 10 e 11.
- `.ai/skills/feature-wiki/references/ponytail-caveman.md` — fronteira entre comunicação concisa e artefatos completos; nenhuma ativação de implementação.

Também foi lido o SKILL.md de computer-use disponível no host para detectar o recurso; nenhuma referência de Windows foi necessária, pois não houve app ou navegador conectado.


