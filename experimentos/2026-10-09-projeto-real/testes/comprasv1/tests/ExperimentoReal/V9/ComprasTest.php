<?php

use App\Models\CentroCusto;
use App\Models\SolicitacaoCompra;
use App\Models\User;
use App\Notifications\AprovacaoPendente;
use Illuminate\Support\Env;
use Illuminate\Support\Facades\Notification;
use Spatie\Permission\PermissionRegistrar;

// Oráculo: somente os CT indicados de conjunto-v9/conjunto.md; tradução ainda não executada.
beforeEach(function () {
    Notification::fake();
    $this->tenantV9 = tenant('Organização A', 'v9-a');
    noPainelDa($this->tenantV9);
    $roleClass = app(PermissionRegistrar::class)->getRoleClass();
    foreach (['panel_user', 'diretor'] as $papel) {
        $roleClass::findOrCreate($papel, 'web')->forceFill(['painel' => 'app'])->save();
    }
    foreach (['S' => 'panel_user', 'G' => 'panel_user', 'H' => 'panel_user', 'D' => 'diretor'] as $nome => $papel) {
        $this->{$nome} = usuarioComPapel($papel, $this->tenantV9, strtolower($nome).'@v9.test');
        $this->{$nome}->forceFill(['name' => $nome])->save();
        $this->tenantV9->users()->attach($this->{$nome});
    }
    $this->actingAs($this->S);
    $this->c1V9 = CentroCusto::create(['nome' => 'C1', 'gestor_id' => $this->G->id]);
    $this->c2V9 = CentroCusto::create(['nome' => 'C2', 'gestor_id' => $this->H->id]);
});

function v9Compra(string $valor = '6000.00'): SolicitacaoCompra
{
    test()->actingAs(test()->S);
    return SolicitacaoCompra::create([
        'descricao' => 'Notebook',
        'valor' => $valor,
        'centro_custo_id' => test()->c1V9->id,
    ]);
}

function v9NaEtapa(string $origem, string $valor = '6000.00'): SolicitacaoCompra
{
    $compra = v9Compra($valor);
    $compra->enviar(test()->S);
    if ($origem === 'aguardando_diretor') {
        test()->actingAs(test()->G);
        $compra->aprovar(test()->G);
    }
    test()->actingAs(test()->S);

    return $compra;
}

function v9Historico(SolicitacaoCompra $compra): array
{
    return $compra->etapas()->orderBy('id')->get()->map(fn ($etapa) => $etapa->getAttributes())->all();
}

function v9Campos(SolicitacaoCompra $compra): array
{
    return $compra->fresh()->only(['descricao', 'valor', 'centro_custo_id', 'solicitante_id']);
}

function v9Decisao(array $decisao, string $etapa, string $resultado, User $autor): void
{
    expect($decisao['etapa'])->toBe($etapa)
        ->and($decisao['decisao'])->toBe($resultado)
        ->and($decisao['decidido_por_id'])->toBe($autor->id);
}

function v9Aviso(User $destinatario, SolicitacaoCompra $compra): void
{
    expect(Notification::sent(
        $destinatario,
        AprovacaoPendente::class,
        fn (AprovacaoPendente $aviso, array $canais) => $aviso->solicitacao->is($compra) && in_array('mail', $canais, true),
    ))->toHaveCount(1);
    Notification::assertSentToTimes($destinatario, AprovacaoPendente::class, 1);
}

function v9SemEmails(array $destinatarios): void
{
    foreach ($destinatarios as $destinatario) {
        expect(Notification::sent(
            $destinatario,
            AprovacaoPendente::class,
            fn (AprovacaoPendente $aviso, array $canais) => in_array('mail', $canais, true),
        ))->toHaveCount(0);
    }
}

function v9RecusaNegocio(Closure $acao): void
{
    try {
        $acao();
    } catch (RuntimeException $erro) {
        expect($erro::class)->toBe(RuntimeException::class);

        return;
    }
    test()->fail('A operação de negócio não foi recusada.');
}

function v9LimiteLiteral(): void
{
    expect((string) config('kit.compras.limite_diretor'))->toBeIn(['5000', '5000.0', '5000.00']);
}

test('V9 CT-11/CT-49: envio começa no gestor e notifica só G pelo canal mail', function (string $valor) {
    $compra = v9Compra($valor);
    Notification::fake();
    $compra->enviar($this->S);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and($compra->fresh()->valor)->toBe($valor)
        ->and($compra->fresh()->centro_custo_id)->toBe($this->c1V9->id)
        ->and($compra->etapas()->where('etapa', 'diretor')->where('decisao', 'aprovada')->count())->toBe(0);
    v9Aviso($this->G, $compra);
    v9SemEmails([$this->S, $this->H, $this->D]);
})->with([
    '3000.00 — abaixo' => ['3000.00'],
    '6000.00 — acima' => ['6000.00'],
]);

test('V9 CT-16: gestor encerra a compra de 3000.00', function () {
    v9LimiteLiteral();
    $compra = v9NaEtapa('aguardando_gestor', '3000.00');
    Notification::fake();
    $this->actingAs($this->G);
    $compra->aprovar($this->G);

    expect($compra->fresh()->situacao->value)->toBe('aprovada')
        ->and($compra->fresh()->etapaPendente())->toBeNull();
    $historico = v9Historico($compra);
    expect($historico)->toHaveCount(1);
    v9Decisao($historico[0], 'gestor', 'aprovada', $this->G);
    v9SemEmails([$this->S, $this->G, $this->D]);
});

test('V9 CT-20: rejeição da etapa corrente conserva campos e devolve a rascunho', function (string $origem, string $ator) {
    $compra = v9NaEtapa($origem);
    Notification::fake();
    $this->actingAs($this->{$ator});
    $compra->rejeitar($this->{$ator}, 'Sem verba');

    expect($compra->fresh()->situacao->value)->toBe('rascunho')
        ->and($compra->fresh()->descricao)->toBe('Notebook')
        ->and($compra->fresh()->valor)->toBe('6000.00')
        ->and($compra->fresh()->centro_custo_id)->toBe($this->c1V9->id);
    $rejeicao = $compra->etapas()->where('decisao', 'rejeitada')->firstOrFail()->getAttributes();
    expect($rejeicao['decidido_por_id'])->toBe($this->{$ator}->id)
        ->and($rejeicao['justificativa'])->toBe('Sem verba');
    v9SemEmails([$this->S, $this->G, $this->D]);
})->with([
    'aguardando_gestor — G' => ['aguardando_gestor', 'G'],
    'aguardando_diretor — D' => ['aguardando_diretor', 'D'],
]);

test('V9 CT-23: centro corrigido usa H e avisa somente H no reenvio', function () {
    $compra = v9NaEtapa('aguardando_gestor');
    $this->actingAs($this->G);
    $compra->rejeitar($this->G, 'Sem verba');
    $this->actingAs($this->S);
    $compra->editar(['descricao' => 'Monitor', 'centro_custo_id' => $this->c2V9->id], $this->S);
    Notification::fake();
    $compra->enviar($this->S);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and($compra->fresh()->descricao)->toBe('Monitor')
        ->and($compra->fresh()->centro_custo_id)->toBe($this->c2V9->id)
        ->and($compra->fresh()->aprovadoresDaVez()->pluck('id')->all())->toBe([$this->H->id]);
    v9Aviso($this->H, $compra);
    v9SemEmails([$this->G, $this->S, $this->D]);
});

test('V9 CT-24: reenvio após rejeição de diretor começa de novo no gestor', function () {
    $compra = v9NaEtapa('aguardando_diretor');
    $this->actingAs($this->D);
    $compra->rejeitar($this->D, 'Sem verba');
    $this->actingAs($this->S);
    $compra->editar(['descricao' => 'Monitor'], $this->S);
    $compra->enviar($this->S);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and($compra->fresh()->descricao)->toBe('Monitor')
        ->and($compra->fresh()->valor)->toBe('6000.00');
});

test('V9 CT-26 parcial: diretor não aprova antes do gestor', function () {
    $compra = v9NaEtapa('aguardando_gestor');
    $campos = v9Campos($compra);
    $historico = v9Historico($compra);
    Notification::fake();
    $this->actingAs($this->D);
    v9RecusaNegocio(fn () => $compra->aprovar($this->D));

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and(v9Campos($compra))->toBe($campos)
        ->and(v9Historico($compra))->toBe($historico);
    v9SemEmails([$this->G, $this->D]);
});

test('V9 CT-41: fronteira literal decide situação e pendência após gestor', function (string $valor, string $destino, ?string $pendencia) {
    v9LimiteLiteral();
    expect(Env::get('KIT_COMPRAS_LIMITE_DIRETOR'))->toBeNull();
    $compra = v9NaEtapa('aguardando_gestor', $valor);
    $this->actingAs($this->G);
    $compra->aprovar($this->G);

    expect($compra->fresh()->situacao->value)->toBe($destino)
        ->and($compra->fresh()->valor)->toBe($valor)
        ->and($compra->fresh()->etapaPendente())->toBe($pendencia);
    $historico = v9Historico($compra);
    expect($historico)->toHaveCount(1);
    v9Decisao($historico[0], 'gestor', 'aprovada', $this->G);
})->with([
    '4999.99' => ['4999.99', 'aprovada', null],
    '5000.00' => ['5000.00', 'aprovada', null],
    '5000.01' => ['5000.01', 'aguardando_diretor', 'diretor'],
]);

test('V9 CT-42: diretor encerra depois da aprovação real de G', function () {
    v9LimiteLiteral();
    $compra = v9NaEtapa('aguardando_diretor');
    Notification::fake();
    $this->actingAs($this->D);
    $compra->aprovar($this->D);

    expect($compra->fresh()->situacao->value)->toBe('aprovada')
        ->and($compra->fresh()->valor)->toBe('6000.00')
        ->and($compra->fresh()->etapaPendente())->toBeNull();
    $historico = v9Historico($compra);
    expect($historico)->toHaveCount(2);
    v9Decisao($historico[0], 'gestor', 'aprovada', $this->G);
    v9Decisao($historico[1], 'diretor', 'aprovada', $this->D);
    v9SemEmails([$this->S, $this->G, $this->D]);
});

test('V9 CT-43: alçada configurada 7000.00 encerra 6000.00 depois do gestor', function () {
    config(['kit.compras.limite_diretor' => '7000.00']);
    expect((string) config('kit.compras.limite_diretor'))->toBe('7000.00');
    $compra = v9NaEtapa('aguardando_gestor');
    Notification::fake();
    $this->actingAs($this->G);
    $compra->aprovar($this->G);

    expect($compra->fresh()->situacao->value)->toBe('aprovada')
        ->and($compra->fresh()->etapaPendente())->toBeNull();
    $historico = v9Historico($compra);
    expect($historico)->toHaveCount(1);
    v9Decisao($historico[0], 'gestor', 'aprovada', $this->G);
    v9SemEmails([$this->S, $this->G, $this->D]);
});

test('V9 CT-44: omitir argumento justificativa não grava rejeição', function (string $origem, string $ator) {
    $compra = v9NaEtapa($origem);
    $campos = v9Campos($compra);
    $historico = v9Historico($compra);
    Notification::fake();
    $this->actingAs($this->{$ator});
    expect(fn () => $compra->rejeitar($this->{$ator}))->toThrow(ArgumentCountError::class);

    expect($compra->fresh()->situacao->value)->toBe($origem)
        ->and(v9Campos($compra))->toBe($campos)
        ->and(v9Historico($compra))->toBe($historico);
    v9SemEmails([$this->S, $this->G, $this->D]);
})->with([
    'gestor — argumento ausente' => ['aguardando_gestor', 'G'],
    'diretor — argumento ausente' => ['aguardando_diretor', 'D'],
]);

test('V9 CT-50: cada diretor de A recebe um mail e X de B não recebe', function (int $quantidade) {
    v9LimiteLiteral();
    $tenantB = tenant('Organização B', 'v9-b');
    noPainelDa($tenantB);
    $roleClass = app(PermissionRegistrar::class)->getRoleClass();
    $roleClass::findOrCreate('diretor', 'web')->forceFill(['painel' => 'app'])->save();
    $x = usuarioComPapel('diretor', $tenantB, 'x@v9.test');
    noPainelDa($this->tenantV9);
    $diretores = [$this->D];
    if ($quantidade === 2) {
        $d2 = usuarioComPapel('diretor', $this->tenantV9, 'd2@v9.test');
        $this->tenantV9->users()->attach($d2);
        $diretores[] = $d2;
    }
    $compra = v9NaEtapa('aguardando_gestor');
    Notification::fake();
    $this->actingAs($this->G);
    $compra->aprovar($this->G);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_diretor');
    foreach ($diretores as $diretor) {
        v9Aviso($diretor, $compra);
    }
    v9SemEmails([$this->S, $this->G, $x]);
})->with([
    'D1 — cardinalidade um' => [1],
    'D1 e D2 — cardinalidade N' => [2],
]);
