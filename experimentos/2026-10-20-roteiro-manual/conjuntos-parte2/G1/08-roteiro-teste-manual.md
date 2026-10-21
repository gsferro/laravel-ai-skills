# Roteiro de Teste Manual — FERRO-812: Cupons de desconto

> **Para quem**: desenvolvedor, revisor do PR e QA humano.
> **Requisito/Casos**: [00-requisito.md](00-requisito.md) · [04-casos-de-teste.md](04-casos-de-teste.md)
> **Base**: cópia local sem `.git`; commit indisponível · 2026-10-20.
> **Vias**: aplicação e terminal.
> **Conferência**: 7 de 12 roteiros executados pela sessão; 4 conformes e 3 com divergências.
> **Auditoria**: pendente — próximo ciclo do quality gate; step 11 não executado.
> **Host/modelo**: Codex, Windows/PowerShell; GPT-6, variante e esforço exatos não expostos.
> **Skill**: `.ai/skills/feature-wiki/SKILL.md`, metadata.version `4.2.0`, lida integralmente.
> O resultado esperado vem do CT/RQ citado; o código só decide como chegar lá.

Decisão vigente: `Roteiro manual: sim`, registrada no `03`. Steps 9 e 10 constam concluídos.
Este documento registra divergências descobertas depois dessa reconciliação. Não declara a feature aprovada.
A conferência de um RM significa execução de todos os seus passos, inclusive quando o resultado diverge.
Não significa execução integral de todos os Exemplos dos CTs citados.

## Preparação do ambiente

**Somente esta cópia local descartável.** Todos os comandos abaixo partem da raiz do projeto.
Não executar em produção nem contra banco compartilhado. Nenhum comando exige credencial real.
O `.env` permanece intacto. Os overrides abaixo valem apenas para o processo PowerShell e seus filhos.

| # | Ação | Comando ou caminho | Como confirmar |
|---|---|---|---|
| 1 | Conferir versões instaladas | `php -v`; `composer show --direct` | Nesta sessão: PHP 8.4.10, Laravel 13.25.0, Filament 5.7.6 e Pest 5.1.1 |
| 2 | Selecionar SQLite em arquivo novo | Bloco PowerShell abaixo | Caminho absoluto dentro de `validation/`; não reaproveitar um banco com dados a preservar |
| 3 | Criar schema sem apagar tabelas | `php artisan migrate --no-interaction` | Migrations concluídas, incluindo `cupons` e `cupom_usos` |
| 4 | Preparar permissões e usuários sintéticos | Bloco de preparação de dados abaixo, via Tinker | Cinco usuários e papéis criados; senha vem da UserFactory local |
| 5 | Conferir rotas | `php artisan route:list --path=cupons` | Rotas index, create e edit do Resource no painel app |
| 6 | Servir para a conferência humana da UI | Na mesma sessão com os overrides: `php artisan serve --host=localhost --port=8128 --no-interaction` | Abrir o endereço local anunciado pelo Artisan; navegar para `/app/login` e `/app/cupons` |
| 7 | Conferir assets antes da UI | `Test-Path public/build/manifest.json` | Nesta cópia: True. Sem manifest, preparar o build pelo fluxo normal do projeto antes da UI |

A sessão executou os passos 1–5 e 7. Não iniciou servidor: a ferramenta de navegador está indisponível.
O Boost MCP, inclusive `get-absolute-url`, não está exposto; os caminhos são relativos e as rotas foram conferidas por Artisan.
Não confundir um endereço sugerido para execução futura com uma aplicação visitada nesta sessão.

```powershell
New-Item -ItemType Directory -Path validation -Force | Out-Null
$manualDatabase = Join-Path $PWD 'validation/cupons-manual.sqlite'
if (Test-Path -LiteralPath $manualDatabase) {
    throw 'Banco já existe. Preserve-o e escolha outro nome novo dentro de validation/.'
}
New-Item -ItemType File -Path $manualDatabase | Out-Null
$env:DB_CONNECTION = 'sqlite'
$env:DB_DATABASE = $manualDatabase
$env:KIT_TENANCY = 'false'
$env:APP_CONFIG_CACHE = 'validation/config-inexistente.php'
$env:APP_ROUTES_CACHE = 'validation/routes-inexistentes.php'
$env:XDEBUG_MODE = 'off'
php artisan migrate --no-interaction
php artisan tinker --no-interaction --execute 'dump(config("database.connections.sqlite.database"), config("kit.tenancy.enabled"));'
```

Para reutilizar o banco **já preparado por esta sessão**, não execute o bloco de criação acima.
Defina somente as variáveis de ambiente com o caminho existente, incluindo os dois caminhos de cache.
Para repetir RM-10, use um banco novo e repita a preparação: seus códigos são deliberadamente fixos.

Em cada bloco abaixo, o PHP fica numa here-string PowerShell com aspas simples.
Não trocar por aspas duplas: elas expandem variáveis PHP no shell.
As transações usadas nos negativos são revertidas **depois** da leitura do estado gravado.
Isso permite observar a escrita indevida sem mantê-la como fixture válida.

### Preparação de dados — executada

A preparação obtém as chaves de permissões do inventário existente e roda somente `PapeisSeeder`.
Não roda `ShieldPermissionsSeeder` nem `shield:generate`, que podem escrever policies.
Essa diferença é necessária para respeitar a proibição de alterar código desta rodada.

```powershell
$manualCode = @'
foreach (["app", "admin", "infra"] as $painel) {
    foreach (App\Support\Paineis::permissoes($painel) as $nome) {
        Spatie\Permission\Models\Permission::findOrCreate($nome, "web");
    }
}
Illuminate\Support\Facades\Artisan::call("db:seed", ["--class" => "Database\\Seeders\\PapeisSeeder", "--no-interaction" => true]);
foreach (["criador" => "master_global", "aplicador" => "master_global", "leitor" => "panel_user", "admin" => "admin", "infra" => "infra"] as $nome => $papel) {
    $usuario = App\Models\User::factory()->create(["name" => "Manual ".$nome, "email" => $nome."@manual.example.test"]);
    $usuario->assignRole($papel);
}
echo json_encode(["usuarios" => App\Models\User::query()->pluck("email"), "roles" => Spatie\Permission\Models\Role::query()->pluck("name")], JSON_UNESCAPED_SLASHES).PHP_EOL;
'@
php artisan tinker --no-interaction --execute $manualCode
```

## Dados e usuários de teste

| Papel | Como obter | Estado necessário |
|---|---|---|
| Criador B | `criador@manual.example.test`, criado pela preparação | `master_global`; distinto de A |
| Aplicador A | `aplicador@manual.example.test`, criado pela preparação | `master_global`; autor explicitamente passado ao motor |
| Usuário comum | `leitor@manual.example.test`, criado pela preparação | somente `panel_user` |
| Admin da instalação | `admin@manual.example.test`, criado pela preparação | somente `admin`; o aceite de escrita é esperado por CT-21 |
| Operador infra | `infra@manual.example.test`, criado pela preparação | somente `infra`; escrita de cupons recusada por CT-21/CT-22 |
| Senhas sintéticas | `database/factories/UserFactory.php` | usar o default de teste da factory; nenhuma senha real foi copiada para este roteiro |
| Cupons do terminal | `Cupom::factory()`, `fixo()` e `expirado()` existentes | 10% ou 1000 centavos, validade futura e limite 3 nos fluxos de aplicação |
| Cupons da UI | Criar pelo RM-01; registrar código, UUID e campos | Usar nomes distintos NOVO-PCT, NOVO-FIXO e OUTRO; conservar OUTRO como sentinela |

Para executar a parte da UI que exige uso anterior, aplique o cupom pelo terminal como A e releia contador e trilha.
Para obter esgotado, realize três aplicações reais num cupom de limite 3; não falsifique `usos`.
Para obter expirado na conferência de listagem/exclusão, a factory `expirado()` é fixture explícita.
O estado expirado não autoriza inferir regras de renovação ou edição de cupom inativo.

A edição manual de datas deve representar o instante do CT. O app desta cópia usa UTC.
Assim, `2026-11-01T12:00:00-03:00` corresponde a `2026-11-01 15:00:00` no formulário UTC.
Não copiar somente a hora local e perder o fuso.

## Roteiros

### RM-01 — Criar os dois tipos e salvar sem alterações · Via: aplicação

**Origem**: RQ-01 · RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · CT-01 · CT-02 · CT-05 · CT-13 · CT-50
**Conferência**: não executado — Playwright MCP ausente; inventário CUA sem navegadores e tentativa de abrir iab recusada.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Entrar como criador B e abrir criação | `/app/cupons/create` | Formulário contém código, tipo, valor, validade e limite | CT-01 | |
| 2 | Criar NOVO-PCT: porcentagem 29, validade 2026-11-01T12:00:00-03:00 e limite 3 | Formulário; ação de criar | Exatamente um cupom com os cinco campos; usos 0 e nenhuma linha de aplicação | CT-02 | |
| 3 | Criar NOVO-FIXO: mudar tipo inicialmente percentual para fixo, valor 101, mesma validade e limite | Nova criação; selecionar tipo fixo antes de salvar | Tipo fixo e valor 101 centavos persistidos; não aplicar teto percentual de 100 | CT-02 · CT-13 · CT-50 | |
| 4 | Abrir a edição de cada registro e salvar sem mudar nada | `/app/cupons/{uuid}/edit`; ação de salvar | Valores originais, identidade única, nenhum erro de duplicidade e nenhum uso criado | CT-01 · CT-05 | |

### RM-02 — Editar todos os campos preservando o uso anterior · Via: aplicação

**Origem**: RQ-01 · CT-03 · CT-50
**Conferência**: não executado — navegador indisponível, conforme RM-01.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar PROMO10 percentual 10 com um uso real e guardar UUID/trilha | Factory e uma chamada `aplicarEm(10000, A)` pelo terminal | Usos 1 e uma linha de uso anterior identificável | CT-03 | |
| 2 | Entrar como B; trocar código para NOVO, tipo para fixo, valor para 1001, validade para 2026-11-02T15:00:00-03:00 e limite para 4 | Edição do UUID original; ação de salvar | Mesmo registro com os cinco novos valores; usos 1 e linha anterior idêntica | CT-03 | |
| 3 | Conferir unidade do valor após mudar tipo | Reabrir a mesma edição | Valor inteiro em centavos, sem transformar fixo em percentual nem aplicar teto de cem | CT-50 | |

### RM-03 — Excluir cupons ativos e inativos sem atingir o vizinho · Via: aplicação

**Origem**: RQ-01 · RQ-07 · CT-04 · CT-55
**Conferência**: não executado — navegador indisponível, conforme RM-01.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar OUTRO ativo e quatro alvos independentes: ativo, expirado com saldo, esgotado ainda válido, expirado e esgotado | Factory e consumo real; guardar campos/UUID de OUTRO | Cada alvo está no estado descrito e OUTRO não tem usos | CT-04 · CT-55 | |
| 2 | Como B, excluir cada alvo pela ação do componente, incluindo confirmação | Ação de excluir na tabela ou edição do UUID | Cada alvo some do cadastro; OUTRO preserva campos e usos; não assumir política de retenção da trilha excluída | CT-04 · CT-55 | |

### RM-06 — Aplicar os dois tipos, consumir uma vez e atribuir a A · Via: terminal

**Origem**: RQ-12 · RQ-13 · RQ-15 · CT-39 · CT-44
**Conferência**: conferido pela sessão 2026-10-20 — conforme nos dois tipos.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como B, criar cupom de cada tipo, aplicar uma vez como A e guardar a linha anterior | Bloco RM-06 abaixo | Primeiro total 9000; um uso e uma linha | CT-39 | Dois tipos retornaram 9000 |
| 2 | Aplicar novamente como A mantendo sessão B; reler estado e trilha | Continuação do mesmo bloco | Total 9000, usos 2, duas linhas, anterior idêntica; autor A, não B, e instante da aplicação | CT-39 · CT-44 · RQ-15 | Totais [9000,9000], usos 2 e linhas 2; três verificações booleanas true nos dois tipos |

```powershell
$manualCode = @'
$criador = App\Models\User::where("email", "criador@manual.example.test")->firstOrFail();
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($criador);
foreach (["porcentagem", "fixo"] as $tipo) {
    $cupom = App\Models\Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    $primeiro = $cupom->aplicarEm(10000, $autor);
    $anterior = App\Models\CupomUso::where("cupom_id", $cupom->id)->firstOrFail()->getAttributes();
    $inicio = now()->toDateTimeString();
    $segundo = $cupom->aplicarEm(10000, $autor);
    $fim = now()->toDateTimeString();
    $linhas = App\Models\CupomUso::where("cupom_id", $cupom->id)->orderBy("id")->get();
    echo json_encode(["tipo" => $tipo, "totais" => [$primeiro, $segundo], "usos" => $cupom->fresh()->usos, "linhas" => $linhas->count(), "anterior_preservada" => $linhas->first()->getAttributes() === $anterior, "autor_explicito" => $linhas->every(fn ($uso) => $uso->aplicado_por_id === $autor->id && $uso->aplicado_por_id !== $criador->id), "instante_atual" => $linhas->last()->created_at->toDateTimeString() >= $inicio && $linhas->last()->created_at->toDateTimeString() <= $fim]).PHP_EOL;
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

## Casos negativos e permissões

### RM-04 — Recusar campos inválidos e códigos duplicados na UI · Via: aplicação

**Origem**: RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-06 · CT-07 · CT-09 · CT-11 · CT-14 · CT-18 · CT-19
**Conferência**: não executado — navegador indisponível, conforme RM-01.

Cada tentativa usa uma fixture independente e somente um campo inválido.
Antes de editar, guardar os cinco campos, contador e linhas de uso.
Os casos de ausência de propriedade e estruturas forjadas ficam para os CTs automatizados.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar sem preencher um campo obrigatório por vez; repetir na edição com null/vazio e um uso anterior | Criar/editar; campos codigo, tipo, valor, expira_em e limite_de_usos | Erro no campo retirado; nenhuma criação ou alteração de campos, contador e trilha | CT-06 · CT-07 | |
| 2 | Conferir que o tipo admite apenas porcentagem e fixo | Campo Tipo; tentativa manual de terceiro tipo se a UI permitir | Nenhum terceiro tipo gravado; erro de tipo se submetido | CT-09 · RQ-03 | |
| 3 | Em criação e edição, tentar percentual 0, 101 e 12,5; controles positivos 1 e 100 | Campo valor; adaptar separador decimal aceito pelo navegador | Inválidos recusados no campo valor; controles válidos persistidos exatamente; sem consumo | CT-11 | |
| 4 | Em criação e edição, tentar fixo -1 ou 1000,5 e limite 1,5; validade textual inválida se o controle permitir entrada | Campos valor, limite e validade | Erro no campo correspondente, sem persistir coerção nem alterar contador/trilha | CT-11 · CT-14 | |
| 5 | Criar com código de outro cupom e renomear OUTRO para o código ocupado | Criar e editar no mesmo contexto; guardar os dois registros antes | Erro em codigo; só o original usa o código; campos, uso anterior e trilha de OUTRO preservados | CT-18 · CT-19 | |

### RM-05 — Listar como leitor e tentar cada verbo proibido · Via: aplicação

**Origem**: RQ-07 · RQ-08 · CT-21 · CT-24 · CT-45 · CT-46
**Conferência**: não executado — navegador indisponível; recorte multi-tenant não preparado nesta cópia single-tenant.

Não interpretar ausência de um botão como prova de autorização. Tentar também abrir criação e edição pelo caminho direto.
O motor para usuário comum não faz parte deste RM: o 04 mantém essa decisão aberta.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Preparar cupons ativos, expirados, esgotados e removidos nos dois tipos; guardar UUIDs | Factory e aplicações reais, em fixtures independentes | Conjunto esperado da leitura comum contém somente ativos | CT-45 | |
| 2 | Entrar como leitor, abrir a lista e percorrer todas as páginas; repetir com 0, 1, p, p+1 e 2p+1 ativos | `/app/cupons`; p é o tamanho de página selecionado | Todos e somente os ativos aparecem uma vez; nenhum consumo ou alteração | CT-45 · CT-46 | |
| 3 | Como leitor, tentar criar, editar valor para 20 e excluir, inclusive por URL direta | `/app/cupons/create` e `/app/cupons/{uuid}/edit`; ações disponíveis | Cada verbo recusado; cadastro, contador e trilha intactos; retornar à lista continua possível | CT-21 · CT-24 | |
| 4 | Repetir os três verbos como infra e, em fixtures novas, como master_global e admin | Sessões separadas dos usuários da preparação | Infra recusado; master_global e admin aceitos conforme os Exemplos do CT, sem copiar matriz divergente do app | CT-21 | |

Os Exemplos multi-tenant de CT-21/CT-45/CT-46 exigem organização Acme/Globex e papéis vinculados antes do boot/migrations.
Não basta trocar `KIT_TENANCY` depois de criar este schema: `permission.teams` e o schema também precisam concordar.
A presente conferência não prepara nem comprova esse ambiente; esse recorte permanece explicitamente fora da execução.

### RM-07 — Recusar código ausente e referência removida · Via: terminal

**Origem**: RQ-09 · CT-29 · CT-30 · CT-48
**Conferência**: conferido pela sessão 2026-10-20 — conforme.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-07 abaixo | Código desconhecido/null/vazio não encontra cupom nem consome; conhecido retorna 9000. Após exclusão autorizada, consulta não encontra, referência antiga não aplica, não recria cupom/uso e preserva OUTRO. | RQ-09 · CT-29 · CT-30 · CT-48 | Ausências true e usos/linhas 0; conhecido retornou 9000; após remoção, cinco verificações true nos dois tipos. |

```powershell
$manualCode = @'
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($autor);
$cupom = App\Models\Cupom::factory()->create(["limite_de_usos" => 3]);
foreach (["DESCONHECIDO", null, ""] as $codigo) {
    $encontrado = App\Models\Cupom::valido($codigo);
    echo json_encode(["codigo" => $codigo, "ausente" => $encontrado === null, "usos" => $cupom->fresh()->usos, "linhas" => App\Models\CupomUso::where("cupom_id", $cupom->id)->count()]).PHP_EOL;
}
$total = App\Models\Cupom::valido($cupom->codigo)->aplicarEm(10000, $autor);
echo json_encode(["existente_total" => $total, "usos" => $cupom->fresh()->usos]).PHP_EOL;
$outro = App\Models\Cupom::factory()->create();
$antes = $outro->fresh()->getAttributes();
foreach (["porcentagem", "fixo"] as $tipo) {
    $removido = App\Models\Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10]);
    $codigo = $removido->codigo;
    $id = $removido->id;
    $removido->delete();
    $recusada = false;
    try { $removido->aplicarEm(10000, $autor); } catch (Throwable $erro) { $recusada = true; }
    echo json_encode(["tipo" => $tipo, "consulta_ausente" => App\Models\Cupom::valido($codigo) === null, "aplicacao_recusada" => $recusada, "sem_recriacao" => ! App\Models\Cupom::whereKey($id)->exists(), "sem_uso" => App\Models\CupomUso::where("cupom_id", $id)->count() === 0, "vizinho_preservado" => $outro->fresh()->getAttributes() === $antes]).PHP_EOL;
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

### RM-08 — Recusar cupom vencido e uso excedente, inclusive com instância antiga · Via: terminal

**Origem**: RQ-10 · RQ-11 · RQ-13 · CT-34 · CT-35 · CT-41
**Conferência**: conferido pela sessão 2026-10-20 — conforme.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-08 abaixo | Com dois usos, último consumo retorna 9000 e leva a 3. Instância antiga é recusada; contador e três linhas ficam iguais. Cupom já expirado não é localizado nem aplicado e permanece sem usos. | RQ-10 · RQ-11 · RQ-13 · CT-34 · CT-35 · CT-41 | Último total 9000, referência antiga recusada, usos 3 e trilha preservada. Expirados recusados, consulta ausente, usos/linhas 0, nos dois tipos. |

```powershell
$manualCode = @'
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($autor);
foreach (["porcentagem", "fixo"] as $tipo) {
    $cupom = App\Models\Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
    $cupom->aplicarEm(10000, $autor);
    $cupom->aplicarEm(10000, $autor);
    $antigo = $cupom->fresh();
    $ultimo = $cupom->aplicarEm(10000, $autor);
    $antes = App\Models\CupomUso::where("cupom_id", $cupom->id)->get()->toArray();
    $recusada = false;
    try { $antigo->aplicarEm(10000, $autor); } catch (Throwable $erro) { $recusada = true; }
    echo json_encode(["tipo" => $tipo, "ultimo_total" => $ultimo, "referencia_antiga_recusada" => $recusada, "usos" => $cupom->fresh()->usos, "consulta_ausente" => App\Models\Cupom::valido($cupom->codigo) === null, "trilha_preservada" => App\Models\CupomUso::where("cupom_id", $cupom->id)->get()->toArray() === $antes]).PHP_EOL;
    $expirado = App\Models\Cupom::factory()->expirado()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10]);
    $recusada = false;
    try { $expirado->aplicarEm(10000, $autor); } catch (Throwable $erro) { $recusada = true; }
    echo json_encode(["tipo" => $tipo, "expirado_recusado" => $recusada, "consulta_ausente" => App\Models\Cupom::valido($expirado->codigo) === null, "usos" => $expirado->fresh()->usos, "linhas" => App\Models\CupomUso::where("cupom_id", $expirado->id)->count()]).PHP_EOL;
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

### RM-09 — Recusar dados inválidos também na escrita direta · Via: terminal

**Origem**: RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · CT-08 · CT-10 · CT-12 · CT-15 · CT-16
**Conferência**: conferido pela sessão 2026-10-20 — divergente — D1, D2 e D3.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-09 abaixo | Em criar e editar, recusar código vazio, tipo cashback, percentual 0/101/12.5, data não válida e limite 1.5, sem persistir valor inválido. Alterações recusadas preservam estado anterior. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · CT-08 · CT-10 · CT-12 · CT-15 · CT-16 | Cashback e data inválida recusados. Código vazio, percentuais 0/101/12.5 e limite 1.5 foram gravados em criar e editar. DB bruto conservou frações; nenhum uso criado. Escritas negativas revertidas depois da observação. |

```powershell
$manualCode = @'
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($autor);
$base = ["codigo" => "DIRETO", "tipo" => "porcentagem", "valor" => 10, "expira_em" => now()->addDays(30), "limite_de_usos" => 3];
$casos = [["codigo", ""], ["tipo", "cashback"], ["valor", 0], ["valor", 101], ["valor", 12.5], ["expira_em", "nao-e-data"], ["limite_de_usos", 1.5]];
foreach ($casos as [$campo, $entrada]) {
    foreach (["criar", "editar"] as $operacao) {
        $cupom = $operacao === "editar" ? App\Models\Cupom::factory()->create($base + []) : null;
        $antes = $cupom?->getAttributes();
        Illuminate\Support\Facades\DB::beginTransaction();
        $recusada = false;
        try {
            if ($operacao === "criar") {
                $dados = $base; $dados[$campo] = $entrada;
                $cupom = App\Models\Cupom::create($dados);
            } else {
                $cupom->update([$campo => $entrada]);
            }
        } catch (Throwable $erro) { $recusada = true; }
        $linha = $cupom ? Illuminate\Support\Facades\DB::table("cupons")->where("id", $cupom->id)->first() : null;
        echo json_encode(["campo" => $campo, "entrada" => $entrada, "operacao" => $operacao, "recusada" => $recusada, "persistido" => $linha?->$campo, "original_preservado" => $operacao === "editar" ? ($linha?->$campo == $antes[$campo]) : null, "linhas_uso" => $cupom ? App\Models\CupomUso::where("cupom_id", $cupom->id)->count() : 0]).PHP_EOL;
        Illuminate\Support\Facades\DB::rollBack();
    }
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

### RM-10 — Impedir duplicidade local inclusive com tenant nulo · Via: terminal

**Origem**: RQ-14 · CT-20
**Conferência**: conferido pela sessão 2026-10-20 — divergente — D4.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-10 abaixo | Criar código duplicado e renomear OUTRO para código ocupado são recusados no mesmo contexto, inclusive tenant nulo. Organizações distintas podem ter cada uma o código; original permanece intacto. | RQ-14 · CT-20 | No contexto nulo, criar e editar aceitaram duplicata e produziram quantidade_codigo 2. Em A e B, ambas recusadas e quantidade 1; código_em_A_e_B 2; original preservado em todas. Somente recorte de unicidade por tenant, sem comprovar autorização multi-tenant. |

```powershell
$manualCode = @'
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($autor);
$a = App\Models\Tenant::factory()->create();
$b = App\Models\Tenant::factory()->create();
foreach ([null, $a, $b] as $tenant) {
    Filament\Facades\Filament::setTenant($tenant, true);
    $original = App\Models\Cupom::factory()->create(["codigo" => "RM10-PROMO10"]);
    $antes = $original->fresh()->getAttributes();
    foreach (["criar", "editar"] as $operacao) {
        $outro = $operacao === "editar" ? App\Models\Cupom::factory()->create(["codigo" => "RM10-OUTRO"]) : null;
        Illuminate\Support\Facades\DB::beginTransaction();
        $recusada = false;
        try {
            if ($operacao === "criar") { App\Models\Cupom::factory()->create(["codigo" => "RM10-PROMO10"]); }
            else { $outro->update(["codigo" => "RM10-PROMO10"]); }
        } catch (Throwable $erro) { $recusada = true; }
        echo json_encode(["tenant" => $tenant?->id, "operacao" => $operacao, "recusada" => $recusada, "quantidade_codigo" => App\Models\Cupom::where("codigo", "RM10-PROMO10")->count(), "original_preservado" => $original->fresh()->getAttributes() === $antes]).PHP_EOL;
        Illuminate\Support\Facades\DB::rollBack();
    }
}
Filament\Facades\Filament::setTenant(null, true);
echo json_encode(["codigo_em_A_e_B" => App\Models\Cupom::where("codigo", "RM10-PROMO10")->whereIn("tenant_id", [$a->id, $b->id])->count()]).PHP_EOL;
'@
php artisan tinker --no-interaction --execute $manualCode
```

### RM-11 — Recusar cada verbo direto de leitor e infra · Via: terminal

**Origem**: RQ-07 · RQ-08 · CT-22
**Conferência**: conferido pela sessão 2026-10-20 — divergente — D5.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-11 abaixo | Para panel_user e infra, chamadas diretas de criar, editar e excluir são recusadas sem Gate manual no roteiro. Cadastro, usos e trilha permanecem intactos. | RQ-07 · RQ-08 · CT-22 | As seis tentativas foram aceitas: recusada false. Criar produziu registro; editar/excluir não preservaram original. Linhas de uso 0; transações revertidas após leitura. |

```powershell
$manualCode = @'
$admin = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
foreach (["leitor", "infra"] as $perfil) {
    $ator = App\Models\User::where("email", $perfil."@manual.example.test")->firstOrFail();
    foreach (["criar", "editar", "excluir"] as $operacao) {
        Illuminate\Support\Facades\Auth::login($admin);
        $cupom = App\Models\Cupom::factory()->create(["limite_de_usos" => 3]);
        $antes = $cupom->fresh()->getAttributes();
        Illuminate\Support\Facades\Auth::login($ator);
        Illuminate\Support\Facades\DB::beginTransaction();
        $recusada = false; $criado = null;
        try {
            if ($operacao === "criar") { $criado = App\Models\Cupom::factory()->create(); }
            elseif ($operacao === "editar") { $cupom->update(["valor" => 20]); }
            else { $cupom->delete(); }
        } catch (Throwable $erro) { $recusada = true; }
        $atual = $cupom->fresh();
        echo json_encode(["perfil" => $perfil, "operacao" => $operacao, "recusada" => $recusada, "criado" => $criado?->exists ?? false, "original_preservado" => $atual?->getAttributes() === $antes, "linhas_uso" => App\Models\CupomUso::where("cupom_id", $cupom->id)->count()]).PHP_EOL;
        Illuminate\Support\Facades\DB::rollBack();
    }
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

### RM-12 — Recusar autoria ausente ou nula · Via: terminal

**Origem**: RQ-15 · CT-54
**Conferência**: conferido pela sessão 2026-10-20 — conforme.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Executar todas as combinações do bloco e ler o estado persistido antes de qualquer rollback | Bloco RM-12 abaixo | Nos dois tipos, omitir autor ou passar null recusa a chamada sem total descontado, usos 0 e nenhuma linha de aplicação. | RQ-15 · CT-54 | Quatro combinações recusadas; usos 0 e linhas 0 em todas. |

```powershell
$manualCode = @'
$autor = App\Models\User::where("email", "aplicador@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::login($autor);
foreach (["porcentagem", "fixo"] as $tipo) {
    foreach (["ausente", "null"] as $autoria) {
        $cupom = App\Models\Cupom::factory()->create(["tipo" => $tipo, "valor" => $tipo === "fixo" ? 1000 : 10, "limite_de_usos" => 3]);
        $recusada = false;
        try {
            if ($autoria === "ausente") { $cupom->aplicarEm(10000); }
            else { $cupom->aplicarEm(10000, null); }
        } catch (Throwable $erro) { $recusada = true; }
        echo json_encode(["tipo" => $tipo, "autoria" => $autoria, "recusada" => $recusada, "usos" => $cupom->fresh()->usos, "linhas" => App\Models\CupomUso::where("cupom_id", $cupom->id)->count()]).PHP_EOL;
    }
}
'@
php artisan tinker --no-interaction --execute $manualCode
```

## Divergências encontradas na conferência

Esperados mantidos conforme o 04. Nenhum aceite indevido foi transformado em resultado correto.
Os CTs abaixo já especificam as recusas: não é necessário inventar regra nova ou responder às perguntas abertas do 04.

| ID | RM / origem | Esperado | Observado | Encaminhamento |
|---|---|---|---|---|
| D1 | RM-09 · CT-08 · RQ-02 | Código vazio recusado na criação/edição direta | `recusada:false`, `persistido:""` em ambas | Implementação: obrigatoriedade no domínio |
| D2 | RM-09 · CT-12 · RQ-04 | Percentual 0, 101 e 12.5 recusado sem gravação | Os três valores foram gravados em criar e editar; fração permaneceu no DB bruto | Implementação: validar domínio antes do cast/escrita; SQLite não fornece essa barreira |
| D3 | RM-09 · CT-16 · RQ-06 | Limite fracionário recusado | `1.5` persistido em criar e editar; cast de leitura inteiro não é recusa | Implementação: validar contagem antes da gravação |
| D4 | RM-10 · CT-20 · RQ-14 | Duplicata recusada também quando tenant é nulo | Criar e renomear geraram duas identidades com mesmo código; tenant não nulo recusou | Implementação: unicidade no contexto nulo; não considerar a constraint composta prova suficiente |
| D5 | RM-11 · CT-22 · RQ-07 · RQ-08 | Leitor e infra não criam, editam ou excluem por entrada direta | Todos os seis verbos foram aceitos no model, apesar dos papéis sem administração | Implementação: barreira de autorização na entrada de domínio; policy da tela não cobre chamada direta |

**Tratamento desta sessão**: achados reproduzidos e registrados somente aqui; escritas negativas em transação foram revertidas.
Não houve correção de app, reescrita de CT, criação de premissa ou alteração do 00–07.
Retorno ao fluxo do step 9 fica pendente para uma sessão autorizada a corrigir: usar o CT existente como oráculo,
corrigir no destino indicado e repetir step 10, reconciliando este roteiro antes do step 11.
A proibição expressa desta rodada impede executar esse retorno agora. Não há afirmação de reconciliação renovada.

Foi corrigido um erro do instrumento de observação, sem mexer no app:
o primeiro snapshot de OUTRO vinha do objeto recém-criado sem defaults do DB e diferia na releitura.
O snapshot passou a usar `fresh()->getAttributes()`; RM-07 foi repetido e confirmou vizinho preservado.
A primeira execução parcial de diagnóstico não foi contada como uma conferência adicional.
RM-10/RM-11 já usaram snapshots relidos.

## Limpeza

- O banco da conferência permanece em `validation/cupons-manual.sqlite`, com usuários sintéticos e fixtures, para reprodução.
- Os RM negativos com transação fazem rollback somente das tentativas observadas. Fixtures de preparação podem permanecer.
- Nenhum `migrate:fresh`, `db:wipe`, truncate ou limpeza de fila foi executado.
- Encerrar eventual servidor futuro com Ctrl+C. Fechar o PowerShell descarta os overrides de ambiente; o `.env` não foi editado.
- Remoção futura do SQLite é destrutiva: **apenas ambiente descartável confirmado; o quality gate não executa**.
  Preservar o banco enquanto os achados precisarem de reprodução; não há comando de remoção automática neste roteiro.
- Manter `validation/integridade-antes.json` e a conferência posterior como evidência local; não são arquivos de produto.

## Fora deste roteiro

| CT / recorte | Motivo de ser só automatizado ou permanecer pendente |
|---|---|
| CT-31 · CT-32 · CT-33 | Fronteira de segundo, referência que vence entre requests e conversão de fuso exigem relógio controlado. RM-08 cobre somente cupom já vencido, por RQ-10 |
| CT-36 | Disputa simultânea exige barreira entre duas conexões e prova do único vencedor |
| CT-37 · CT-38 | Precisão, truncamento e fronteiras de centavo/zero permanecem na prova numérica automatizada; RM-06 usa apenas totais básicos |
| CT-17 · CT-42 | Preservação exata do instante e autoria em horário fixado exigem comparação temporal controlada; RM-06 conferiu autoria e janela atual, sem declarar execução desses CTs inteiros |
| CT-40 · CT-43 | Falhas injetadas antes/depois de inserir a trilha exigem costura de teste; não alterar código para testar manualmente |
| CT-23 | Matriz completa dos dez pares de papéis exige fixtures e isolamento por atribuição; não foi substituída pelos dois perfis simples do RM-11 |
| CT-25 · CT-26 · CT-27 · CT-28 · CT-51 · CT-52 · CT-53 | IDOR, payload forjado, instância alheia, contexto nulo e permissões por organização exigem arnês multi-tenant coerente. Nesta cópia não foi preparado; nenhuma garantia de isolamento foi inferida de RM-10 |
| CT-49 | Salvar/excluir com identidade removida ou nunca existente exige referência de componente inválida controlada; RM-07 só cobre consumo e consulta de referência removida |
| CT-47 | Combinação expirado e esgotado com trilha anterior idêntica exige fixture temporal controlada; RM-08 verifica os estados isolados |
| Exemplos restantes de CT-06–CT-16 · CT-20–CT-22 · CT-34 | RM cobre somente as entradas explicitamente enumeradas. Estruturas forjadas, ausências de propriedades, todos os positivos e demais modos permanecem nos respectivos CTs |
| Mutantes e perguntas abertas do 04 | Mutação não é teste manual. Perguntas abertas não recebem comportamento esperado novo; nenhum limite, normalização, renovação, retenção ou fluxo de Pedido foi inventado |

O 05 não existe e o 04 declara ausência de CT-B; nenhum CT-B foi criado ou reivindicado.
Não existe tela de aplicação ao Pedido neste escopo: o motor é exercitado no terminal.

## Registro de execução

| Data | Quem | Ambiente | Commit | RM executados | Resultado | Observações |
|---|---|---|---|---|---|---|
| 2026-10-20 | sessão Codex / GPT-6, variante não exposta | local; SQLite em validation; via terminal | indisponível, cópia sem .git | RM-06, RM-07, RM-08, RM-09, RM-10, RM-11, RM-12 | 4 conformes: 06/07/08/12; 3 divergentes: 09/10/11 | Contagem de roteiros, não de CTs; os comandos encerraram com exit 0, mas os JSONs negativos revelam D1–D5 |

RM-01 a RM-05 não têm resultado obtido preenchido nem linha de execução.
Prova da limitação: inventário `cua.getState()` retornou `apps:[]`, `browsers:[]`;
`cua.createBrowserTab("iab", ...)` respondeu `Browser is not available: iab`.
Playwright MCP não consta das ferramentas expostas. Não foi instalada dependência nem configuração para contornar a ausência.
Usar o browser plugin Pest como substituto exigiria criar teste, o que foi proibido.

## Desvios e degradações desta etapa

- Sem despacho — o contrato manda a sessão escrever o roteiro em linha; não se executou julgamento independente nem step 11.
- `03-progresso.md` é imutável por instrução do usuário. Host, referências, achados e saída do script ficam neste 08 e no retorno.
  Não foram colados em `03 → Verificação Final`, nem se fechou checkbox adicional.
- Sem `.git`: não há hash de commit nem diff disponível. Integridade verificada por hashes dos arquivos de produto e 00–07.
- Sem Boost MCP: CLI, factories existentes e leitura localizada definiram os caminhos. Nenhum código foi alterado ou documentação de API presumida.
- Sem navegador: cinco RM de aplicação não executados, com motivo em cada um.
- `02-decisoes-arquiteturais.md`, 05 e 07-tickets ausentes, confirmados por listagem/Test-Path; não foram criados.
- O 04 contém notas históricas de uma rodada sem vendor e sem implementação. Nesta sessão `composer show --direct` confirmou dependências instaladas.
  Isso não autoriza alterar as notas antigas nem tratar os CTs como executados.
- Não foram lidas as pastas de wiki ou testes proibidas pelo usuário.
- Conferência manual não substitui Pest, CT-B, revisão do diff ou quality gate. Nenhum veredito do step 11 foi emitido.

## Referências abertas

Todas sob `.ai/skills/feature-wiki/references/`, na etapa entre steps 10 e 11:

- `hosts-e-subagentes.md` — host efetivo, fallback, limites e Bash no Windows.
- `template-08-roteiro-manual.md` — geração, oráculo, conferência, segurança e atualização.
- `playwright-mcp.md` — ausência de MCP e limites da observação em navegador.

Também foi lida a skill de computer-use do host antes da tentativa CUA, sem abrir pastas inteiras de referências.
As demais referências da feature-wiki pertencem a steps não executados nesta invocação.

## Verificação Final desta etapa

Comando executado na raiz, em Git Bash com PHP no PATH:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' '.ai/skills/feature-wiki/scripts/roteiro-manual.sh' 'wikis/specs/saida-g1/cupons-de-desconto'
$LASTEXITCODE
```

Saída literal do script: vazia (stdout e stderr). Exit: `0`.
O wrapper PowerShell imprimiu `roteiro-manual.sh exit 0`.
Esse check comprova vínculos estáticos e estrutura, não ausência das divergências D1–D5.

Contagem programática sobre os cabeçalhos e linhas de conferência do documento:

```text
RM definidos: 12
RM conferidos: 7
```

Comparação SHA-256 com o manifesto capturado antes das migrations e fixtures:

```text
Arquivos protegidos conferidos: 307
Arquivos protegidos alterados: 0
```

Manifestos locais: `validation/integridade-antes.json` e `validation/integridade-depois.json`.
Não foram criados testes nem modificados arquivos PHP; Pint não foi executado para evitar escrita fora do contrato.

