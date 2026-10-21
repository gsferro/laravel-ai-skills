# Roteiro de Teste Manual — FERRO-830: Aprovação de solicitação de compra

> **Para quem**: desenvolvedor, revisor do PR e QA humano em homologação local.
> **Requisito/Casos**: [00-requisito.md](00-requisito.md) · [04-casos-de-teste.md](04-casos-de-teste.md) · [05-casos-de-teste-browser.md](05-casos-de-teste-browser.md).
> **Base**: snapshot local, sem metadados Git · 2026-10-20. `git rev-parse --short HEAD` não é possível: esta cópia não contém `.git`.
> **Identificação do código**: SHA256 de `app/Models/SolicitacaoCompra.php`: `220DF322367A15469597A8C5EEAACA968481D135DB685D256EAA5E77536581A4`. Manifesto mais amplo em `validation/manual-before-hashes.json`.
> **Vias**: terminal e aplicação; somente terminal executado nesta sessão.
> **Conferência**: 10 de 18 roteiros executados pela sessão; 9 sem divergência no recorte executado, 1 com divergência de implementação.
> **Auditoria**: pendente — próximo ciclo do quality gate. Step 11 não executado.
> **Sessão**: host Codex, modelo GPT-6; variante e esforço efetivos não informados pelo host.
> O resultado esperado vem do CT/CT-B/RQ citado; o código só decide como chegar lá. Conferido significa executado, não aprovado.

## Preparação do ambiente

A decisão vigente já é `sim` no `03-progresso.md`; os steps 9 e 10 estão registrados como concluídos.
Este documento atende ao pedido de roteiro posterior ao step 10, sem reexecutar esses steps.
O achado D-01 abaixo impede tratar esta conferência como aceite integral da feature.

Execute somente nesta cópia SQLite descartável, autorizada pelo desenvolvedor. Os comandos abaixo
gravam dados sintéticos. Não use produção, banco compartilhado ou credenciais reais.
Mantenha `.env`, código, testes, migrations e arquivos 00–07 intactos.

| # | Ação | Comando ou caminho | Como confirmar |
|---|---|---|---|
| 1 | Entrar na raiz e definir banco de arquivo apenas no processo | Bloco PowerShell abaixo | DB_DATABASE termina em validation/manual.sqlite; nenhuma edição de .env |
| 2 | Aplicar migrations existentes sem apagar tabelas | `php artisan migrate --no-interaction` | Comando termina com sucesso |
| 3 | Criar pessoas, centros e permissões locais controladas | Bloco de preparação de dados abaixo | Acme manual; Ana/Bruno/Carlos; Diana/Elisa diretoras; Fernanda administradora |
| 4 | Carregar contexto dos comandos de cada RM | Variável PowerShell $contexto, abaixo | Os comandos usam o mesmo banco, tenant e transporte array |
| 5 | Conferir caminhos registrados | `php artisan route:list --path=solicitacoes-de-compra --no-interaction` | Existem index, create, view e edit; chave de rota é UUID |
| 6 | Servir a aplicação, apenas para os RM por aplicação | Em outro terminal com o mesmo DB_DATABASE: `$env:MAIL_MAILER='log'; php artisan serve --host=localhost --port=8013 --no-interaction` | Acesso local ao painel e autenticação real; não foi executado nesta conferência |

```powershell
Set-Location 'D:\PROJECTS\SKILLS\blind-20261020-p2\proj-9794e2'
New-Item -ItemType Directory -Path 'validation' -Force | Out-Null
$env:DB_CONNECTION = 'sqlite'
$env:DB_DATABASE = Join-Path $PWD 'validation/manual.sqlite'
$env:MAIL_MAILER = 'array'
$env:QUEUE_CONNECTION = 'sync'
if (-not (Test-Path -LiteralPath $env:DB_DATABASE)) {
    New-Item -ItemType File -Path $env:DB_DATABASE | Out-Null
}
php artisan migrate --no-interaction
```

O transporte `array` compõe o e-mail real em memória dentro de cada comando; nenhuma mensagem
sai para a rede. Não foram usados Notification::fake ou Queue::fake. O array não sobrevive a outro
processo/request: por isso o servidor futuro deve usar `MAIL_MAILER=log` e a conferência humana
deve observar destinatários e corpo no log local. Limpar a observação com flush() não apaga dados
nem envia mensagens.

### Preparação de dados reproduzível

No mesmo PowerShell, execute uma vez em banco dedicado. A criação usa factories existentes.
As permissões são fixtures controladas; não são prova da matriz gerada pelos seeders.
Não foi executado ShieldPermissionsSeeder: sua geração pode escrever policies ausentes,
o que está fora da autorização desta tarefa.

```powershell
$preparo = @'
$tenant = App\Models\Tenant::where("slug", "acme-manual")->first()
    ?? App\Models\Tenant::factory()->create(["nome" => "Acme manual", "slug" => "acme-manual"]);
Filament\Facades\Filament::setCurrentPanel(Filament\Facades\Filament::getPanel("app"));
Filament\Facades\Filament::setTenant($tenant, isQuiet: true);
$users = [];
foreach (["Ana", "Bruno", "Carlos", "Diana", "Elisa", "Fernanda"] as $name) {
    $email = strtolower($name)."@manual.example.test";
    $users[$name] = App\Models\User::where("email", $email)->first()
        ?? App\Models\User::factory()->create(["name" => $name, "email" => $email]);
    $tenant->users()->syncWithoutDetaching([$users[$name]->id]);
}
$permissions = [];
foreach (["ViewAny", "View", "Create", "Update", "Delete"] as $verb) {
    $permissions[] = Spatie\Permission\Models\Permission::findOrCreate($verb.":SolicitacaoCompra", "web");
}
$role = App\Models\Role::firstOrCreate(["name" => "panel_user", "guard_name" => "web"], ["painel" => "app"]);
$role->syncPermissions($permissions);
$director = App\Models\Role::firstOrCreate(["name" => "diretor", "guard_name" => "web"], ["painel" => "app"]);
$director->syncPermissions($permissions);
foreach ($users as $user) {
    $user->assignRole($role);
}
$users["Diana"]->assignRole($director);
$users["Elisa"]->assignRole($director);
foreach (["Compras" => "Bruno", "Viagens" => "Carlos", "Sem gestor" => null] as $nome => $gestor) {
    if (! App\Models\CentroCusto::where("nome", $nome)->exists()) {
        App\Models\CentroCusto::factory()->create([
            "tenant_id" => $tenant->id, "nome" => $nome,
            "gestor_id" => $gestor === null ? null : $users[$gestor]->id,
        ]);
    }
}

$permissions = [];
foreach (["ViewAny", "View", "Create", "Update", "Delete"] as $verb) {
    $permissions[] = Spatie\Permission\Models\Permission::findOrCreate($verb.":CentroCusto", "web");
}
$admin = App\Models\Role::firstOrCreate(["name" => "admin_organizacao", "guard_name" => "web"], ["painel" => "app"]);
$admin->syncPermissions(array_merge($permissions, Spatie\Permission\Models\Permission::where("name", "like", "%:SolicitacaoCompra")->get()->all()));
App\Models\User::where("email", "fernanda@manual.example.test")->firstOrFail()->assignRole($admin);
echo "Fernanda: admin_organizacao; Ana/Bruno/Carlos: panel_user; Diana/Elisa: diretor.".PHP_EOL;
'@
php artisan tinker --no-interaction --execute $preparo
```

### Contexto para os RM de terminal

Execute este bloco PowerShell para definir `$contexto`. Cada RM concatena seu trecho PHP
ao contexto e inicia um processo novo. Os exemplos devem rodar em série.
O helper `$nova` cria somente a partida legítima; o comportamento é exercitado pelos métodos
reais. Situações posteriores são obtidas por enviar/aprovar/rejeitar/cancelar.
Os helpers exibem fatos; compare-os ao resultado esperado da tabela, sem derivar o esperado do código.

```powershell
$contexto = @'
$tenant = App\Models\Tenant::where("slug", "acme-manual")->firstOrFail();
$ana = App\Models\User::where("email", "ana@manual.example.test")->firstOrFail();
$bruno = App\Models\User::where("email", "bruno@manual.example.test")->firstOrFail();
$carlos = App\Models\User::where("email", "carlos@manual.example.test")->firstOrFail();
$diana = App\Models\User::where("email", "diana@manual.example.test")->firstOrFail();
$elisa = App\Models\User::where("email", "elisa@manual.example.test")->firstOrFail();
Illuminate\Support\Facades\Auth::setUser($ana);
Filament\Facades\Filament::setCurrentPanel(Filament\Facades\Filament::getPanel("app"));
Filament\Facades\Filament::setTenant($tenant);
$compras = App\Models\CentroCusto::where("nome", "Compras")->firstOrFail();
$viagens = App\Models\CentroCusto::where("nome", "Viagens")->firstOrFail();
$semGestor = App\Models\CentroCusto::where("nome", "Sem gestor")->firstOrFail();
$mail = Illuminate\Support\Facades\Mail::mailer()->getSymfonyTransport();
$nova = function (string $descricao, string $valor = "5000.01", ?App\Models\CentroCusto $centro = null) use ($tenant, $ana, $compras) {
    return App\Models\SolicitacaoCompra::factory()->create(["tenant_id" => $tenant->id, "solicitante_id" => $ana->id, "centro_custo_id" => ($centro ?? $compras)->id, "descricao" => $descricao, "valor" => $valor]);
};
$mostrar = function (App\Models\SolicitacaoCompra $s, string $passo) use ($mail) {
    $atual = $s->fresh();
    $mensagens = $mail->messages()->map(function ($sent) {
        $email = $sent->getOriginalMessage();
        return ["para" => array_map(fn ($address) => $address->getAddress(), $email->getTo()), "assunto" => $email->getSubject(), "corpo" => trim(preg_replace("/\s+/u", " ", strip_tags($email->getTextBody() ?? $email->getHtmlBody() ?? "")))];
    })->all();
    echo json_encode(["passo" => $passo, "compra" => $atual?->only(["id", "descricao", "valor", "centro_custo_id", "solicitante_id", "situacao"]), "historico" => $atual?->etapas()->get(["id", "etapa", "decisao", "decidido_por_id", "justificativa", "created_at"])->toArray(), "emails" => $mensagens], JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES).PHP_EOL;
};
$tentar = function (string $acao, Closure $operacao) {
    try { $operacao(); echo $acao.": ACEITA".PHP_EOL; }
    catch (Throwable $erro) { echo $acao.": RECUSADA ".get_class($erro)." ".$erro->getMessage().PHP_EOL; }
};
'@
```

## Dados e usuários de teste

| Papel | Como obter | Estado necessário |
|---|---|---|
| Solicitante Ana | User::factory no preparo; ana@manual.example.test | panel_user, membro de Acme; somente ela é dona das compras criadas pelos trechos |
| Gestor Bruno | bruno@manual.example.test | Gestor específico de Compras; não diretor |
| Outro gestor Carlos | carlos@manual.example.test | Gestor de Viagens; não dono das compras de Ana |
| Diretoras Diana e Elisa | diana@manual.example.test e elisa@manual.example.test | Papel diretor, painel app; duas pessoas distintas |
| Administradora Fernanda | fernanda@manual.example.test | admin_organizacao, permissões de CentroCusto e SolicitacaoCompra; sem elegibilidade automática para aprovar |
| Centros | Factories do preparo | Compras/Bruno, Viagens/Carlos e Sem gestor/null, todos em Acme |
| Compras | $nova em cada RM | Dados sintéticos e partida rascunho; valor default 5000.01 |
| Credencial de login futuro | Default de UserFactory desta cópia | Senha sintética `password`, exclusivamente para estas pessoas @manual.example.test |

Nesta execução, Acme tem id 1; Ana 1, Bruno 2, Carlos 3, Diana 4, Elisa 5 e Fernanda 6;
os centros são Compras 1, Viagens 2 e Sem gestor 3. Os comandos buscam por chaves legíveis,
não dependem desses números para serem repetidos. Os números foram obtidos no preparo, em
`validation/manual-setup.txt`.

A configuração efetiva desta cópia é `KIT_TENANCY=false`, `permission.teams=false`, alçada
5000.00. O contexto Acme do terminal é fixado explicitamente pelo Filament.
Isso não prova que um request HTTP recebe esse contexto.
Os RM por aplicação exigem contexto de organização legítimo no app; não contorne falha de
contexto por injeção no navegador. O RM-18 exige homologação com tenancy e papéis por tenant
previamente configurados, ausente nesta cópia. Não execute `kit:tenancy`: ele altera configuração
e recria banco.

## Roteiros

### RM-01 — Criar, corrigir e excluir o próprio rascunho · Via: terminal

**Origem**: RQ-01 · RQ-02 · RQ-03 · CT-01 · CT-04 · CT-08 · CT-43
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar um rascunho de Ana. | Trecho PHP RM-01 abaixo | Rascunho de Ana com descrição RM01 Café, valor 4999.99 e centro Compras; zero decisões e e-mails. | RQ-01 · RQ-02 · RQ-03 · CT-01 · CT-04 · CT-08 · CT-43 | Registro 17 criado com os três dados; histórico e e-mails vazios. |
| 2 | Corrigir descrição, valor e centro; salvar novamente sem alteração. | Trecho PHP RM-01 abaixo | O mesmo rascunho contém Café e açúcar ☕, 5000.01 e Viagens; salvar sem mudança não duplica nem falha. | RQ-01 · RQ-02 · RQ-03 · CT-01 · CT-04 · CT-08 · CT-43 | Registro 17 manteve os dados nas duas gravações; zero decisões e e-mails. |
| 3 | Excluir o rascunho como Ana. | Trecho PHP RM-01 abaixo | Registro indisponível para uso, sem nova decisão ou e-mail. | RQ-01 · RQ-02 · RQ-03 · CT-01 · CT-04 · CT-08 · CT-43 | fresh() retornou null; nenhum e-mail. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-01.txt`.

```powershell
$trecho = @'
$s = $nova("RM01 Café", "4999.99"); $mostrar($s, "criar"); $s->editar(["descricao" => "RM01 Café e açúcar ☕", "valor" => "5000.01", "centro_custo_id" => $viagens->id], $ana); $mostrar($s, "editar"); $s->editar(["descricao" => $s->descricao, "valor" => $s->valor, "centro_custo_id" => $s->centro_custo_id], $ana); $mostrar($s, "salvar sem mudar"); $s->excluir($ana); $mostrar($s, "excluir");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-02 — Encerrar aprovação pelo gestor até R$ 5.000 · Via: terminal

**Origem**: RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-12 · CT-17 · CT-41 · CT-43 · CT-67
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar separadamente os valores 4999.99 e 5000.00. | Trecho PHP RM-02 abaixo | Cada compra aguarda gestor, sem decisões; somente Bruno recebe uma mensagem de gestor com corpo da compra. | RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-12 · CT-17 · CT-41 · CT-43 · CT-67 | Registros 18 e 19: aguardando_gestor; uma mensagem composta para Bruno em cada envio. |
| 2 | Aprovar cada compra como Bruno, observando somente mensagens novas. | Trecho PHP RM-02 abaixo | Cada compra termina aprovada com uma decisão de gestor por Bruno e zero e-mails novos. | RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-12 · CT-17 · CT-41 · CT-43 · CT-67 | Ambas aprovadas; uma decisão de Bruno por compra; nenhum aviso de diretor. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-02.txt`.

```powershell
$trecho = @'
foreach (["4999.99", "5000.00"] as $valor) { $s = $nova("RM02 Fronteira ".$valor, $valor); $mail->flush(); $s->enviar($ana); $mostrar($s, "enviar ".$valor); $mail->flush(); $s->aprovar($bruno); $mostrar($s, "aprovar ".$valor); }
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-03 — Exigir diretor acima da alçada e identificar quem decidiu · Via: terminal

**Origem**: RQ-04 · RQ-05 · RQ-06 · RQ-13 · RQ-14 · CT-12 · CT-17 · CT-19 · CT-67
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar compra de 5000.01. | Trecho PHP RM-03 abaixo | Aguarda gestor; zero decisões; um e-mail para Bruno, nenhum para diretoras. | RQ-04 · RQ-05 · RQ-06 · RQ-13 · RQ-14 · CT-12 · CT-17 · CT-19 · CT-67 | Registro 20 aguardando_gestor; mensagem real composta no transporte array para Bruno. |
| 2 | Aprovar como Bruno. | Trecho PHP RM-03 abaixo | Aguarda diretor; uma decisão de gestor; uma mensagem de diretor para Diana e outra para Elisa, sem outros destinatários. | RQ-04 · RQ-05 · RQ-06 · RQ-13 · RQ-14 · CT-12 · CT-17 · CT-19 · CT-67 | Uma aprovação de Bruno; duas mensagens compostas, para Diana e Elisa. |
| 3 | Aprovar como Elisa. | Trecho PHP RM-03 abaixo | Aprovada com duas decisões em ordem: gestor Bruno e diretora Elisa; nenhum e-mail novo. | RQ-04 · RQ-05 · RQ-06 · RQ-13 · RQ-14 · CT-12 · CT-17 · CT-19 · CT-67 | Registro 20 aprovado; autores 2 e 5 nas etapas corretas; zero mensagens novas. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-03.txt`.

```powershell
$trecho = @'
$s = $nova("RM03 Duas etapas ☕"); $s->enviar($ana); $mostrar($s, "envio"); $mail->flush(); $s->aprovar($bruno); $mostrar($s, "gestor"); $mail->flush(); $s->aprovar($elisa); $mostrar($s, "diretora Elisa");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-04 — Corrigir e reenviar após rejeição do diretor · Via: terminal

**Origem**: RQ-05 · RQ-07 · RQ-08 · RQ-09 · RQ-13 · RQ-14 · CT-24 · CT-29 · CT-30 · CT-69
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar, aprovar como Bruno e rejeitar como Diana com Sem verba. | Trecho PHP RM-04 abaixo | Rascunho com aprovação de Bruno e rejeição de Diana preservadas; zero e-mails da rejeição. | RQ-05 · RQ-07 · RQ-08 · RQ-09 · RQ-13 · RQ-14 · CT-24 · CT-29 · CT-30 · CT-69 | Registro 21 retornou a rascunho; duas decisões, justificativa Sem verba; zero mensagens novas. |
| 2 | Corrigir para Viagens e reenviar como Ana. | Trecho PHP RM-04 abaixo | Aguarda gestor; histórico anterior idêntico; somente Carlos recebe novo aviso de gestor. | RQ-05 · RQ-07 · RQ-08 · RQ-09 · RQ-13 · RQ-14 · CT-24 · CT-29 · CT-30 · CT-69 | Centro 2; histórico preservado; uma mensagem para Carlos. |
| 3 | Aprovar como Carlos e depois Elisa. | Trecho PHP RM-04 abaixo | Nova etapa de diretor após Carlos; decisão de Elisa encerra o segundo ciclo; três decisões anteriores íntegras e zero e-mails da final. | RQ-05 · RQ-07 · RQ-08 · RQ-09 · RQ-13 · RQ-14 · CT-24 · CT-29 · CT-30 · CT-69 | Quatro decisões ordenadas: Bruno aprova, Diana rejeita, Carlos aprova, Elisa aprova. Final aprovada; mensagens de diretor somente após Carlos. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-04.txt`.

```powershell
$trecho = @'
$s = $nova("RM04 Novo ciclo"); $s->enviar($ana); $s->aprovar($bruno); $mail->flush(); $s->rejeitar($diana, "Sem verba"); $mostrar($s, "rejeicao diretor"); $s->editar(["descricao" => "RM04 Corrigida", "centro_custo_id" => $viagens->id], $ana); $s->enviar($ana); $mostrar($s, "reenvio"); $mail->flush(); $s->aprovar($carlos); $mostrar($s, "novo gestor"); $mail->flush(); $s->aprovar($elisa); $mostrar($s, "diretor segundo ciclo");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

## Casos negativos e permissões

### RM-05 — Recusar justificativa vazia e aceitar rejeição justificada · Via: terminal

**Origem**: RQ-06 · RQ-07 · RQ-08 · CT-24 · CT-25 · CT-43
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar e tentar rejeitar com texto vazio e com espaços. | Trecho PHP RM-05 abaixo | Ambas recusadas; compra aguarda gestor; dados e histórico intactos; zero e-mails novos. | RQ-06 · RQ-07 · RQ-08 · CT-24 · CT-25 · CT-43 | Duas RuntimeException; registro 6 aguardando_gestor, sem decisões ou mensagens. |
| 2 | Rejeitar como Bruno com Não há orçamento 🛒. | Trecho PHP RM-05 abaixo | Rascunho com uma rejeição de gestor por Bruno e justificativa Unicode íntegra; nenhum aviso novo. | RQ-06 · RQ-07 · RQ-08 · CT-24 · CT-25 · CT-43 | Uma rejeição, autor 2, justificativa exata; zero e-mails. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-05.txt`.

```powershell
$trecho = @'
$s = $nova("RM05 Justificativa"); $s->enviar($ana); $mail->flush(); $tentar("justificativa vazia", fn () => $s->rejeitar($bruno, "")); $tentar("justificativa espacos", fn () => $s->rejeitar($bruno, "   ")); $mostrar($s, "apos recusas"); $s->rejeitar($bruno, "Não há orçamento 🛒"); $mostrar($s, "rejeicao gestor");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-06 — Cancelar antes de cada aprovação possível · Via: terminal

**Origem**: RQ-11 · CT-31 · CT-43
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar uma compra e cancelar como Ana antes do gestor. | Trecho PHP RM-06 abaixo | Cancelada; mantém os três dados, nenhuma decisão nova e nenhum e-mail de cancelamento. | RQ-11 · CT-31 · CT-43 | Registro 7 cancelado; zero decisões e mensagens novas. |
| 2 | Enviar outra, aprovar como Bruno e cancelar como Ana antes do diretor. | Trecho PHP RM-06 abaixo | Cancelada; aprovação de Bruno e dados preservados, sem decisão ou mensagem nova. | RQ-11 · CT-31 · CT-43 | Registro 8 cancelado; mesma decisão 10 por Bruno; zero mensagens novas. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-06.txt`.

```powershell
$trecho = @'
foreach (["gestor", "diretor"] as $etapa) { $s = $nova("RM06 Cancelar ".$etapa); $s->enviar($ana); if ($etapa === "diretor") { $s->aprovar($bruno); } $mail->flush(); $mostrar($s, "antes ".$etapa); $s->cancelar($ana); $mostrar($s, "cancelada ".$etapa); }
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-07 — Recusar ações de pessoas sem elegibilidade · Via: terminal

**Origem**: RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-11 · CT-06 · CT-10 · CT-13 · CT-21 · CT-22 · CT-32
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como Carlos, Bruno e Diana, tentar editar, excluir e enviar o rascunho de Ana. | Trecho PHP RM-07 abaixo | Todas as tentativas recusadas; rascunho, dono e dados preservados; zero decisões e mensagens. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-11 · CT-06 · CT-10 · CT-13 · CT-21 · CT-22 · CT-32 | Nove recusas; registro 9 manteve rascunho e dados. |
| 2 | Após envio, tentar aprovar/rejeitar como Ana, Carlos e Diana; tentar cancelar como Bruno. | Trecho PHP RM-07 abaixo | Só o gestor específico decide; só Ana cancela. Tentativas não mudam a compra nem enviam e-mail. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-11 · CT-06 · CT-10 · CT-13 · CT-21 · CT-22 · CT-32 | Sete recusas; aguardando_gestor com histórico vazio. |
| 3 | Após aprovação legítima de Bruno, repetir aprovar/rejeitar como Ana, Bruno e Carlos; cancelar como Diana. | Trecho PHP RM-07 abaixo | Somente diretora elegível decide a etapa corrente; tentativas recusadas e estado/histórico preservados. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-11 · CT-06 · CT-10 · CT-13 · CT-21 · CT-22 · CT-32 | Sete recusas; aguardando_diretor, mesma decisão 11; zero mensagens novas. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-07.txt`.

```powershell
$trecho = @'
$s = $nova("RM07 Identidade"); $mail->flush(); foreach ([$carlos, $bruno, $diana] as $ator) { $tentar($ator->name." editar", fn () => $s->editar(["descricao" => "Indevida"], $ator)); $tentar($ator->name." excluir", fn () => $s->excluir($ator)); $tentar($ator->name." enviar", fn () => $s->enviar($ator)); } $mostrar($s, "rascunho protegido"); $s->enviar($ana); $mail->flush(); foreach ([$ana, $carlos, $diana] as $ator) { $tentar($ator->name." aprovar gestor", fn () => $s->aprovar($ator)); $tentar($ator->name." rejeitar gestor", fn () => $s->rejeitar($ator, "Sem verba")); } $tentar("Bruno cancelar alheia", fn () => $s->cancelar($bruno)); $mostrar($s, "etapa gestor protegida"); $s->aprovar($bruno); $mail->flush(); foreach ([$ana, $bruno, $carlos] as $ator) { $tentar($ator->name." aprovar diretor", fn () => $s->aprovar($ator)); $tentar($ator->name." rejeitar diretor", fn () => $s->rejeitar($ator, "Sem verba")); } $tentar("Diana cancelar alheia", fn () => $s->cancelar($diana)); $mostrar($s, "etapa diretor protegida");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-08 — Manter compras aprovadas e canceladas imutáveis · Via: terminal

**Origem**: RQ-10 · RQ-11 · CT-05 · CT-09 · CT-14 · CT-20 · CT-26 · CT-33
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Produzir uma aprovada e uma cancelada por transições reais; fotografar dados e decisões. | Trecho PHP RM-08 abaixo | Preparação atinge os dois estados sem fabricar situação persistida. | RQ-10 · RQ-11 · CT-05 · CT-09 · CT-14 · CT-20 · CT-26 · CT-33 | Registros 10 e 11 atingiram aprovada e cancelada. |
| 2 | Em cada uma, tentar editar, excluir, enviar, aprovar, rejeitar e cancelar. | Trecho PHP RM-08 abaixo | Seis ações recusadas por estado; dados, existência e histórico permanecem idênticos, sem novos e-mails. | RQ-10 · RQ-11 · CT-05 · CT-09 · CT-14 · CT-20 · CT-26 · CT-33 | Doze recusas; registros e decisões idênticos antes/depois; zero mensagens novas. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-08.txt`.

```powershell
$trecho = @'
foreach (["aprovada", "cancelada"] as $destino) { $s = $nova("RM08 Terminal ".$destino); $s->enviar($ana); if ($destino === "aprovada") { $s->aprovar($bruno); $s->aprovar($diana); } else { $s->cancelar($ana); } $mail->flush(); $mostrar($s, "antes ".$destino); $tentar("editar", fn () => $s->editar(["descricao" => "Indevida"], $ana)); $tentar("excluir", fn () => $s->excluir($ana)); $tentar("enviar", fn () => $s->enviar($ana)); $tentar("aprovar", fn () => $s->aprovar($diana)); $tentar("rejeitar", fn () => $s->rejeitar($diana, "Sem verba")); $tentar("cancelar", fn () => $s->cancelar($ana)); $mostrar($s, "depois ".$destino); }
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

### RM-09 — Recusar envio sem gestor e manter rascunho · Via: terminal

**Origem**: RQ-04 · CT-15
**Conferência**: conferido pela sessão em 2026-10-20 — sem divergência no recorte abaixo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar no centro Sem gestor e tentar enviar como Ana. | Trecho PHP RM-09 abaixo | Recusa identifica ausência de gestor; mantém dados e rascunho; zero decisões/e-mails; warning da recusa. | RQ-04 · CT-15 | Registro 12 continuou rascunho; RuntimeException sobre gestor; zero decisões/e-mails. |
| 2 | Localizar warning da mesma compra no channel compras. | Trecho PHP RM-09 abaixo; busca no log local | Warning correspondente ao envio recusado por ausência de gestor, conforme A-10 do requisito e CT-15. | RQ-04 · CT-15 | storage/logs/compras-2026-10-20.log contém local.WARNING, solicitacao_id 12, motivo centro_sem_gestor. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-09.txt`.

```powershell
$trecho = @'
$s = $nova("RM09 Sem gestor", "5000.01", $semGestor); $mail->flush(); echo "SOLICITACAO_ID=".$s->id.PHP_EOL; $tentar("enviar sem gestor", fn () => $s->enviar($ana)); $mostrar($s, "recusa sem gestor");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

```powershell
Select-String -Path 'storage/logs/compras-*.log' -Pattern 'centro_sem_gestor'
```

Correlacione `solicitacao_id` com SOLICITACAO_ID impresso pelo comando desta execução, não com um warning antigo.

### RM-10 — Recusar descrição vazia também por fora do formulário · Via: terminal

**Origem**: RQ-01 · RQ-02 · CT-02
**Conferência**: conferido pela sessão em 2026-10-20 — divergência D-01, sem aprovação.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Criar diretamente pelo model com descrição vazia, dono Ana e referências legítimas. | Trecho PHP RM-10 abaixo | Criação recusada por descrição; nenhuma compra nova e nenhum e-mail ou decisão. | RQ-01 · RQ-02 · CT-02 | DIVERGIU: save() aceitou descrição vazia; registro 15 criado em rascunho. |
| 2 | Criar rascunho válido e editar sua descrição para vazio como Ana. | Trecho PHP RM-10 abaixo | Edição recusada; descrição original, valor, centro e histórico preservados; zero e-mails novos. | RQ-01 · RQ-02 · CT-02 | DIVERGIU: editar() aceitou descrição vazia; registro 16 perdeu a descrição original; zero decisões/e-mails. |

Execute o bloco completo; a saída literal desta sessão está em `validation/RM-10.txt`.

```powershell
$trecho = @'
$mail->flush(); $s = new App\Models\SolicitacaoCompra(["descricao" => "", "valor" => "5000.01", "centro_custo_id" => $compras->id]); $s->solicitante_id = $ana->id; $tentar("criar descricao vazia", fn () => $s->save()); $mostrar($s, "criacao invalida"); $edicao = $nova("RM10 Descricao original"); $tentar("editar descricao vazia", fn () => $edicao->editar(["descricao" => ""], $ana)); $mostrar($edicao, "edicao invalida");
'@
php artisan tinker --no-interaction --execute ($contexto + [Environment]::NewLine + $trecho)
```

## Roteiros pela aplicação — conferência pendente

### RM-11 — Gravar, corrigir e excluir pelo formulário · Via: aplicação

**Origem**: RQ-01 · RQ-02 · RQ-03 · CT-03 · CT-07 · CT-08 · CT-60 · CT-65
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Ana autenticada no painel app, contexto Acme legítimo e centros Compras/Viagens disponíveis. Use descrição única MANUAL-UI-11.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Abrir criação e gravar MANUAL-UI-11, valor 5000.01 e centro Compras. | Menu Solicitações de compra; Criar; campos Descrição, Valor e Centro de custo. | Uma compra de Ana em rascunho com os três dados; nenhum erro de formulário, decisão ou e-mail. | RQ-01 · RQ-02 · RQ-03 · CT-03 · CT-07 · CT-08 · CT-60 · CT-65 | |
| 2 | Editar para descrição MANUAL-UI-11 corrigida e centro Viagens; salvar novamente sem mudar. | Ação Editar da própria linha; Salvar nas duas visitas. | O mesmo registro mantém correções, sem erro, duplicação ou e-mail; histórico anterior íntegro. | RQ-01 · RQ-02 · RQ-03 · CT-03 · CT-07 · CT-08 · CT-60 · CT-65 | |
| 3 | Excluir o próprio rascunho e confirmar. | Ação Excluir da linha. | Compra deixa de estar disponível; nenhuma decisão ou mensagem nova. | RQ-01 · RQ-02 · RQ-03 · CT-03 · CT-07 · CT-08 · CT-60 · CT-65 | |

### RM-12 — Recusar formulário sem os dados obrigatórios · Via: aplicação

**Origem**: RQ-01 · CT-02 · CT-03 · CT-07
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Ana autenticada com criação e edição autorizadas; um rascunho válido de controle. D-01 é uma falha do domínio e não deve ser escondida por eventual validação da tela.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Tentar criar sem descrição, depois sem valor e depois sem centro, uma falta por tentativa. | Formulário de criação da solicitação. | A gravação é recusada por cada dado obrigatório; nenhuma compra, decisão ou e-mail novo. | RQ-01 · CT-02 · CT-03 · CT-07 | |
| 2 | Editar o rascunho de controle e apagar a descrição; tentar salvar. | Formulário de edição da própria compra. | Gravação recusada; os dados originais permanecem e nenhum e-mail novo é enviado. | RQ-01 · CT-02 · CT-03 · CT-07 | |

### RM-13 — Aprovar pela interface nas duas alçadas · Via: aplicação

**Origem**: RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-17 · CT-19 · CT-65 · CT-67
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Criar MANUAL-UI-13 baixo por 5000.00 e MANUAL-UI-13 alto por 5000.01 como Ana. Usar usuários separados, sem master_global. Observar mensagens no log do servidor desde cada ação.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Enviar ambas como Ana e confirmar. | Listagem, ação Enviar de cada compra. | Ambas aguardam gestor; somente Bruno recebe uma mensagem de gestor por compra; zero decisões. | RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-17 · CT-19 · CT-65 · CT-67 | |
| 2 | Sair e entrar como Bruno; aprovar cada compra e confirmar. | Listagem, ação Aprovar. | Compra de 5000.00 termina aprovada; a de 5000.01 aguarda diretor, com uma decisão de Bruno e um aviso para cada diretora. | RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-17 · CT-19 · CT-65 · CT-67 | |
| 3 | Entrar como Elisa e aprovar a compra alta. | Listagem, ação Aprovar da compra alta. | Compra alta aprovada; duas etapas, Bruno antes de Elisa; nenhum e-mail novo da conclusão. | RQ-04 · RQ-05 · RQ-06 · RQ-14 · CT-17 · CT-19 · CT-65 · CT-67 | |

### RM-14 — Abrir, validar e submeter a modal de rejeição · Via: aplicação

**Origem**: RQ-07 · RQ-08 · CT-27 · CT-28 · CT-B01
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Bruno autenticado, compra de Ana MANUAL-UI-14 por 5000.01 em aguardando_gestor, Diana/Elisa diretoras. Criar a partida por criação e envio reais; delimitar no log os avisos anteriores ao clique. Filtrar a listagem pela descrição para haver uma única compra alvo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Acionar Rejeitar da linha e observar o diálogo aberto. | Ação Rejeitar; diálogo Rejeitar solicitação; campo Motivo da rejeição. | Diálogo realmente visível e campo editável com JavaScript executado. | RQ-07 · RQ-08 · CT-27 · CT-28 · CT-B01 | |
| 2 | Submeter vazio. | Botão de submissão do diálogo. | Erro na justificativa, compra continua aguardando gestor, histórico idêntico e ação corrigível sem tela de erro ou aviso novo. | RQ-07 · RQ-08 · CT-27 · CT-28 · CT-B01 | |
| 3 | Na mesma modal, preencher Sem verba e submeter. | Campo Motivo da rejeição e botão de submissão. | Própria linha passa a rascunho; banco tem uma rejeição de gestor por Bruno com Sem verba, histórico anterior preservado e zero e-mails novos. | RQ-07 · RQ-08 · CT-27 · CT-28 · CT-B01 | |

### RM-15 — Cancelar pela interface e limitar ações por pessoa e estado · Via: aplicação

**Origem**: RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-10 · RQ-11 · CT-58 · CT-59 · CT-65
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Compras distintas de Ana em rascunho, aguardando_gestor, aguardando_diretor, aprovada e cancelada, produzidas por transições reais. Bruno não é diretor; Diana é diretora. Cada login usa a própria pessoa.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como Ana, comparar ações e cancelar uma compra em cada estado de espera. | Listagem das compras identificadas; ação Cancelar com confirmação. | Rascunho oferece editar/excluir/enviar; cada espera oferece cancelar; ambos cancelamentos mantêm dados/histórico e não enviam e-mail. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-10 · RQ-11 · CT-58 · CT-59 · CT-65 | |
| 2 | Como Bruno e depois Diana, comparar as etapas elegíveis. | Mesmas compras em estados de espera antes do cancelamento, usando cópias distintas. | Bruno aprova/rejeita somente aguardando_gestor; Diana aprova/rejeita somente aguardando_diretor; diretor não pula gestor. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-10 · RQ-11 · CT-58 · CT-59 · CT-65 | |
| 3 | Entrar como Carlos; tentar acessar edição alheia por endereço conhecido. Conferir terminais como Ana. | Caminho edit gerado pelo Resource para rascunho alheio; linhas aprovada/cancelada. | Carlos não grava nem exclui a compra de Ana; terminais não oferecem as seis ações de escrita. Dados e histórico permanecem íntegros. | RQ-02 · RQ-03 · RQ-04 · RQ-05 · RQ-06 · RQ-10 · RQ-11 · CT-58 · CT-59 · CT-65 | |

### RM-16 — Ver situação e autores reais em listagem e histórico · Via: aplicação

**Origem**: RQ-12 · RQ-13 · CT-55 · CT-56 · CT-57 · CT-61
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Leitor autorizado; partidas reais para os cinco estados. Use compra concluída por Elisa, outra com aprovação de Bruno, rejeição de Diana e aprovação de Carlos no segundo ciclo. Consulte instantes persistidos, sem inventar formato/fuso normativo.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Abrir listagem e detalhe de cada estado. | Solicitações de compra; ação Visualizar, não um id numérico inventado. | Cada compra informa sua própria situação: rascunho, aguardando gestor, aguardando diretor, aprovada ou cancelada; espera de diretor nunca aparece como final. | RQ-12 · RQ-13 · CT-55 · CT-56 · CT-57 · CT-61 | |
| 2 | Abrir histórico da compra concluída por Elisa e da compra em segundo ciclo. | Detalhe; Histórico de aprovação; Etapas. | Gestor associado a Bruno e diretora a Elisa na primeira; na segunda, Bruno, Diana e Carlos permanecem em ordem, com decisão, instante e Sem verba na rejeição. | RQ-12 · RQ-13 · CT-55 · CT-56 · CT-57 · CT-61 | |
| 3 | Filtrar para coleção vazia; depois verificar registro cancelado além da primeira página. | Busca por descrição sem correspondência; depois paginação com L+1 compras e a última cancelada. | Coleção vazia não inventa estado; página 2 associa a compra alvo a cancelada, sem copiar situação de outra linha. | RQ-12 · RQ-13 · CT-55 · CT-56 · CT-57 · CT-61 | |

### RM-17 — Administrar centro de custo sem promover usuário comum · Via: aplicação

**Origem**: RQ-01 · RQ-04 · CT-48 · CT-49 · CT-50 · CT-64
**Conferência**: não executado — Playwright MCP não exposto nesta sessão. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Fernanda com permissões administrativas legítimas de centros; Bruno/Carlos membros de Acme. Ana/Carlos conservam permissão de solicitar compra, sem permissão administrativa. As permissões sintéticas do preparo permitem o fluxo, mas não atestam o seeder de produção.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como Fernanda, criar um centro MANUAL-UI-17 com gestor Bruno. | Centros de custo; Criar; Nome e Gestor. | Um único centro de Acme com Bruno; nenhum erro, compra, decisão ou aviso de aprovação. | RQ-01 · RQ-04 · CT-48 · CT-49 · CT-50 · CT-64 | |
| 2 | Trocar gestor para Carlos; salvar; salvar novamente sem alterar. | Editar o mesmo centro. | Mesmo centro conserva organização e nome; gestor Carlos persistido nas duas gravações, sem erro ou efeito de aprovação. | RQ-01 · RQ-04 · CT-48 · CT-49 · CT-50 · CT-64 | |
| 3 | Como Carlos, tentar criar, editar e excluir centro sem autorização; voltar como Fernanda e excluir somente o centro sem dependências. | Listagem e caminho edit do centro conhecido; depois ação Excluir como administradora. | Carlos não consegue se nomear gestor nem excluir; mantém permissão de criar compra. Fernanda exclui o centro de teste sem afetar Compras/Viagens. | RQ-01 · RQ-04 · CT-48 · CT-49 · CT-50 · CT-64 | |

### RM-18 — Recusar acesso a compras e centros de outra organização · Via: aplicação

**Origem**: RQ-01 · RQ-04 · CT-47 · CT-51 · CT-66
**Conferência**: não executado — Playwright MCP não exposto nesta sessão; ambiente atual sem tenancy e sem papéis por tenant. A conferência de domínio por terminal não atesta esta UI.

**Partida**: Somente em homologação local já configurada com tenancy e papéis por tenant antes das migrations: Acme e Globex, atores próprios, compra e centro em ambas, UUID estrangeiro conhecido e registro local de controle. Esta cópia não satisfaz essa partida. Não ligar tenancy nesta tarefa.

| # | Ação | Comando / tela | Resultado esperado | Origem | Resultado obtido |
|---|---|---|---|---|---|
| 1 | Como leitor somente de Acme, listar compras e abrir detalhe conhecido de Globex. | Listagem do Resource e caminho view gerado sob o painel com tenancy. | Coleção não contém compra estrangeira; detalhe recusa acesso sem expor dados; compra local continua acessível. | RQ-01 · RQ-04 · CT-47 · CT-51 · CT-66 | |
| 2 | Como administradora somente de Acme, tentar editar e excluir centro de Globex. | Caminho edit e ação de registro do centro estrangeiro. | Operações recusadas; nome, organização e gestor estrangeiros intactos; centro local permanece acessível; nenhuma compra, decisão ou mensagem nova. | RQ-01 · RQ-04 · CT-47 · CT-51 · CT-66 | |

## Divergências encontradas e encaminhamento

### D-01 — Descrição obrigatória não validada no domínio

- **Fonte do esperado**: RQ-01 e CT-02; na edição, também RQ-02. O CT exige recusa e preservação
  dos dados por fora da UI. Nenhuma expectativa foi inferida do formulário ou do PRD.
- **Reprodução efetiva**: RM-10, usando `new SolicitacaoCompra([...])->save()` com
  `descricao = ""`, solicitante Ana e centro legítimo, seguido de `editar(["descricao" => ""], $ana)`
  sobre outro rascunho válido. A criação inválida não usou factory nem mass assignment de controle.
- **Obtido**: criação aceitou e gravou registro 15 sem descrição; edição aceitou e apagou a descrição
  do registro 16. Ambos permaneceram em rascunho, com zero decisões/e-mails. Saída literal em
  `validation/RM-10.txt`: `criar descricao vazia: ACEITA` e `editar descricao vazia: ACEITA`.
- **Destino**: implementação. Já há RQ e CT para o comportamento, portanto não cabe inventar P-nn,
  alterar o esperado ou criar Adendo. Depois de autorizada a correção, materializar/reutilizar
  a regressão CT-02 antes do fix; retomar o roteamento do step 9 e repetir o step 10 antes de
  considerar o roteiro reconciliado com código corrigido.
- **Nesta tarefa**: nenhum fix, teste ou alteração nos arquivos 00–07. O contrato restritivo do
  desenvolvedor prevalece sobre atualizar o 03 ou reiniciar a esteira. D-01 permanece aberto
  neste 08. O RM-10 está conferido e divergente, sem selo de aceite.

Não foi encontrado resultado esperado cuja única fonte fosse o código. Por isso nenhum comportamento
observado foi promovido a novo oráculo. A leitura de componente, policy, enum e notificação serviu
para localizar operações e apresentação. Não houve conferência visual; não se conclui que UI,
isolamento entre organizações ou todos os exemplos dos CT estejam corretos.

### Defasagem documental constatada

O `03` registra implementação, revisão e reconciliação concluídas. Entretanto, `04` e `05`
ainda dizem “somente especificação”, citam paths de testes propostos e apontam para
`wikis/specs/oraculo/`. Na cópia atual, `vendor` está instalado, há implementação e manifest
de frontend; `tests/Feature/AprovacaoCompra` e `tests/Browser/AprovacaoCompra` não existem.
A pasta desta wiki também não contém `02-decisoes-arquiteturais.md`.
São limitações documentais observadas, sem afirmar execução prévia dos CT ou revisão do step 10.
Os vínculos deste 08 apontam aos arquivos locais; as fontes antigas ficaram intactas por instrução.
Não foram acessadas as pastas de experimentos vedadas.

## Limpeza

Preserve `validation/manual.sqlite`, `validation/RM-01.txt` a `validation/RM-10.txt`,
`validation/manual-setup.txt` e o manifesto de hashes enquanto D-01 precisar ser reproduzido.
Os registros inválidos 15/16 pertencem somente a esse banco descartável; não os trate como dados
de homologação aprovados. As primeiras tentativas e repetições também deixaram dados sintéticos
nesse mesmo arquivo.

Ao terminar uma futura conferência de UI, encerre o processo iniciado por `artisan serve`.
Fechar o PowerShell descarta as variáveis de ambiente do processo, sem editar `.env`.
Não foi aberto servidor nesta sessão.

Não há comando destrutivo neste roteiro. Não use `migrate:fresh`, `db:wipe`, truncate ou
`kit:tenancy` para “limpar”. O quality gate não deve executar limpeza destrutiva.
O arquivo SQLite pode ser descartado posteriormente pelo responsável depois de preservar as evidências.

## Fora deste roteiro

| CT / recorte | Motivo ou prova que continua necessária |
|---|---|
| CT-38, CT-39 | Concorrência exige dois processos/conexões, barreiras e leitura final independente; clique sequencial não prova interleaving. |
| CT-40 | Falha tardia antes do commit exige instrumentação controlada e observação real de rollback/entrega. |
| CT-01, CT-17, CT-18 — precisão e matriz monetária completa | RM-02/03 observam os valores de alçada; precisão e todos os limites configurados continuam sendo prova automatizada. Não há mutation score inferido. |
| CT-35, CT-36, CT-37 | Retries, instâncias antigas e unicidade exigem comparação automatizada das decisões e efeitos; não cobertos pela execução feliz. |
| CT-44, CT-45, CT-46, CT-52, CT-53, CT-54 | Chamadas diretas cross-tenant e payloads forjados exigem arnês de segurança e matriz automatizada. RM-18 cobre somente a superfície humana quando houver ambiente compatível. |
| CT-23 — todos os acúmulos de funções | Matriz completa de papéis permanece automatizada; os usuários distintos desta conferência não a provam. |
| CT-63 | Ausência de diretor e seus recortes ainda abertos no 04 exigem preservar o invariante especificado; não foi removido papel para simular fluxo nesta sessão. |
| Mutantes previstos no 04 e no 05 | Exigem mutação e asserções falsificáveis; não foram executados. |
| CT-B01 | Está representado pelo RM-14, não executado. Roteiro humano não substitui teste Pest browser versionado. |
| Perguntas Q1–Q9 do 04 | Não foram respondidas pelo desenvolvedor ausente. Não transformar faixa, teto, visibilidade, retenção, fuso ou desempate pendentes em esperado deste roteiro. |
| Matriz efetiva dos seeders | Fixtures concederam apenas permissões necessárias. Esta conferência não atesta geração/recorte de papéis de produção. |

## Registro de execução

| Data | Quem | Ambiente | Commit | RM executados | Resultado | Observações |
|---|---|---|---|---|---|---|
| 2026-10-20 | Sessão Codex / GPT-6; variante e esforço não informados | PowerShell; PHP 8.4.10; SQLite validation/manual.sqlite; mail array, fila sync; contexto Acme explícito | Indisponível nesta cópia sem .git; snapshot SHA256 no cabeçalho | RM-01 a RM-10 | 9 sem divergência no recorte; RM-10 divergente | Todas as etapas desses RM foram executadas, inclusive consulta do warning do RM-09. RM-11 a RM-18 não executados; não há linha de execução para eles. |

As saídas literais estão nos arquivos `validation/RM-*.txt`. Os processos de terminal finalizaram
com exit 0; o exit do Tinker não é veredito de comportamento. As exceções esperadas foram capturadas
somente para imprimir o resultado e continuar a observação. D-01 foi identificado comparando
a persistência real com CT-02, embora o processo tenha terminado com sucesso.

## Desvios e degradações

- **Sem despacho**: esta etapa manda a sessão escrever em linha. Não houve subagente ou alegação
  de revisão independente.
- **Somente 08 na wiki**: saída do script e referências estão neste arquivo, em lugar do 03.
  O desenvolvedor proibiu expressamente alterações em 00–07.
- **Boost e Playwright MCP ausentes**: inventário das ferramentas expostas não contém search-docs,
  database-query, get-absolute-url nem ferramentas Playwright MCP. Não houve instalação,
  alteração de dependências ou ativação de perfil de navegador persistente. Os localizadores
  vêm dos Resources e de route:list; não se atestam links navegados.
- **Aplicação pendente**: RM-11 a RM-18 não executados por falta do Playwright MCP.
  Não foi usado navegador alternativo sem confirmação de isolamento. RM-18 tem também
  pré-requisito de tenancy/teams ausente; RM-17 não atesta matriz real dos seeders.
- **Git ausente**: `Test-Path .git` retornou False e `git status --short` retornou
  `fatal: not a git repository (or any of the parent directories): .git`.
  A base é snapshot; o manifesto permite comparar conteúdos, não provar ausência de leitura.
- **Preparo corrigido**: tentativa inicial de setTenant antes de usuário gerou TypeError
  em TenantSet. O preparo usou isQuiet; os comandos de conferência usam Auth::setUser antes de
  setTenant, sem fingir login HTTP. Nenhuma mudança no app foi necessária.
- **Reexecução controlada**: a primeira rodada de RM-01 a RM-04 deixou processos simultâneos
  por retorno assíncrono da ferramenta; RM-02 mostrou warning de rename em views compiladas.
  Todos foram aguardados e os quatro foram repetidos em série, sem esse warning.
  As saídas RM-01 a RM-04 preservadas são as da repetição; não houve mudança no código.
- **D-01 sem correção**: roteiro preserva o resultado esperado e documenta o retorno necessário
  aos steps 9/10. Step 11 não foi executado e nenhum veredito de QA foi atribuído.

## Referências abertas

Referências da skill `.ai/skills/feature-wiki` efetivamente abertas nesta invocação:

- `references/hosts-e-subagentes.md` — adaptação ao host e execução de scripts no Windows.
- `references/template-08-roteiro-manual.md` — etapa entre os steps 10 e 11; template, conferência e segurança.
- `references/playwright-mcp.md` — capacidade de observação, isolamento e limites quando MCP não está exposto.
- `references/ponytail-caveman.md` — fronteira de estilo; a wiki usa prosa normal.

A skill local foi lida inteira; `metadata.version = "4.2.0"`. Não foi aberta pasta inteira de
references, nem reinvocadas as skills de derivação de testes ou quality gate.

## Verificação final desta etapa

A instrução genérica manda colar a saída em Verificação Final do 03. Nesta invocação, o 03 é
somente leitura por ordem expressa do desenvolvedor; este registro fica no 08.

Comando executado na raiz, por Git Bash, em 2026-10-20:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' '.ai/skills/feature-wiki/scripts/roteiro-manual.sh' 'wikis/specs/saida-g2/aprovacao-de-compra'
```

Saída literal do script: vazia (stdout e stderr). Exit: **0**.
O script verifica vínculos estáticos, não aprova D-01 nem a UI pendente.

Contagens executadas com rg sobre este arquivo: `^### RM-` = **18**;
`^\*\*Conferência\*\*: conferido` = **10**;
`^\*\*Conferência\*\*: não executado` = **8**.
Comparação SHA256 com o manifesto inicial: **269 arquivos protegidos, 0 alterados**.
O conjunto inclui app, database, config, routes, resources, arquivos de configuração da raiz
e os arquivos 00–07 existentes desta wiki. Nenhum teste foi editado ou executado nesta etapa.

