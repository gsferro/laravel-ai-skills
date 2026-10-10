<?php

use App\Models\CentroCusto;
use App\Models\SolicitacaoCompra;
use App\Models\User;
use App\Notifications\AprovacaoPendente;
use Illuminate\Support\Facades\Notification;
use Spatie\Permission\PermissionRegistrar;

// Oráculo: somente os CT indicados de conjunto-h2/conjunto.md; tradução ainda não executada.
beforeEach(function () {
    Notification::fake();
    $this->acmeH2 = tenant('Acme', 'h2-acme');
    noPainelDa($this->acmeH2);
    $roleClass = app(PermissionRegistrar::class)->getRoleClass();
    foreach (['panel_user', 'diretor'] as $papel) {
        $roleClass::findOrCreate($papel, 'web')->forceFill(['painel' => 'app'])->save();
    }
    foreach (['Sofia' => 'panel_user', 'Geraldo' => 'panel_user', 'Paula' => 'panel_user', 'Daniela' => 'diretor'] as $nome => $papel) {
        $this->{$nome} = usuarioComPapel($papel, $this->acmeH2, strtolower($nome).'@h2.test');
        $this->{$nome}->forceFill(['name' => $nome])->save();
        $this->acmeH2->users()->attach($this->{$nome});
    }
    $this->actingAs($this->Sofia);
    $this->operacoesH2 = CentroCusto::create(['nome' => 'Operações', 'gestor_id' => $this->Geraldo->id]);
    $this->projetosH2 = CentroCusto::create(['nome' => 'Projetos', 'gestor_id' => $this->Paula->id]);
});

function h2Compra(string $valor = '8000.01'): SolicitacaoCompra
{
    test()->actingAs(test()->Sofia);
    return SolicitacaoCompra::create([
        'descricao' => 'Notebook',
        'valor' => $valor,
        'centro_custo_id' => test()->operacoesH2->id,
    ]);
}

function h2NaEtapa(string $origem, string $valor = '8000.01'): SolicitacaoCompra
{
    $compra = h2Compra($valor);
    $compra->enviar(test()->Sofia);
    if ($origem === 'aguardando_diretor') {
        test()->actingAs(test()->Geraldo);
        $compra->aprovar(test()->Geraldo);
    }
    test()->actingAs(test()->Sofia);

    return $compra;
}

function h2Historico(SolicitacaoCompra $compra): array
{
    return $compra->etapas()->orderBy('id')->get()->map(fn ($etapa) => $etapa->getAttributes())->all();
}

function h2Decisao(array $decisao, string $etapa, string $resultado, User $autor, ?string $justificativa = null): void
{
    expect($decisao['etapa'])->toBe($etapa)
        ->and($decisao['decisao'])->toBe($resultado)
        ->and($decisao['decidido_por_id'])->toBe($autor->id);
    if ($justificativa !== null) {
        expect($decisao['justificativa'])->toBe($justificativa);
    }
}

function h2Aviso(User $destinatario, SolicitacaoCompra $compra, string $etapa, int $quantidade = 1): void
{
    expect(Notification::sent(
        $destinatario,
        AprovacaoPendente::class,
        fn (AprovacaoPendente $aviso, array $canais) => $aviso->solicitacao->is($compra)
            && $aviso->etapa === $etapa && in_array('mail', $canais, true),
    ))->toHaveCount($quantidade);
    Notification::assertSentToTimes($destinatario, AprovacaoPendente::class, $quantidade);
}

function h2SemEmails(array $destinatarios): void
{
    foreach ($destinatarios as $destinatario) {
        expect(Notification::sent(
            $destinatario,
            AprovacaoPendente::class,
            fn (AprovacaoPendente $aviso, array $canais) => in_array('mail', $canais, true),
        ))->toHaveCount(0);
    }
}

function h2RecusaNegocio(Closure $acao): void
{
    try {
        $acao();
    } catch (RuntimeException $erro) {
        expect($erro::class)->toBe(RuntimeException::class);

        return;
    }
    test()->fail('A operação de negócio não foi recusada.');
}

function h2LimiteLiteral(): void
{
    expect((string) config('kit.compras.limite_diretor'))->toBeIn(['5000', '5000.0', '5000.00']);
}

test('H2 CT-12/CT-41: envio começa no gestor e envia somente seu mail', function (string $valor) {
    $compra = h2Compra($valor);
    Notification::fake();
    $compra->enviar($this->Sofia);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and(h2Historico($compra))->toBe([]);
    h2Aviso($this->Geraldo, $compra, 'gestor');
    h2SemEmails([$this->Sofia, $this->Paula, $this->Daniela]);
    Notification::assertSentTimes(AprovacaoPendente::class, 1);
})->with([
    '4999.99 — abaixo' => ['4999.99'],
    '5000.00 — igualdade' => ['5000.00'],
    '5000.01 — acima' => ['5000.01'],
]);

test('H2 CT-15: o centavo determina a etapa depois do gestor', function (string $valor, string $destino, int $emails) {
    h2LimiteLiteral();
    $compra = h2NaEtapa('aguardando_gestor', $valor);
    Notification::fake();
    $this->actingAs($this->Geraldo);
    $compra->aprovar($this->Geraldo);

    expect($compra->fresh()->situacao->value)->toBe($destino);
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount(1);
    h2Decisao($historico[0], 'gestor', 'aprovada', $this->Geraldo);
    if ($emails === 1) {
        h2Aviso($this->Daniela, $compra, 'diretor');
    } else {
        h2SemEmails([$this->Daniela]);
    }
})->with([
    '4999.99' => ['4999.99', 'aprovada', 0],
    '5000.00' => ['5000.00', 'aprovada', 0],
    '5000.01' => ['5000.01', 'aguardando_diretor', 1],
]);

test('H2 CT-16: a configuração 7000.00 dispensa diretor para 6000.01', function () {
    config(['kit.compras.limite_diretor' => '7000.00']);
    expect((string) config('kit.compras.limite_diretor'))->toBe('7000.00');
    $compra = h2NaEtapa('aguardando_gestor', '6000.01');
    Notification::fake();
    $this->actingAs($this->Geraldo);
    $compra->aprovar($this->Geraldo);

    expect($compra->fresh()->situacao->value)->toBe('aprovada');
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount(1);
    h2Decisao($historico[0], 'gestor', 'aprovada', $this->Geraldo);
    h2SemEmails([$this->Daniela]);
});

test('H2 CT-17: diretor encerra depois da decisão real do gestor', function () {
    papelNaOrganizacao($this->Paula, 'diretor', $this->acmeH2);
    $compra = h2NaEtapa('aguardando_diretor');
    Notification::fake();
    $this->actingAs($this->Daniela);
    $compra->aprovar($this->Daniela);

    expect($compra->fresh()->situacao->value)->toBe('aprovada');
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount(2);
    h2Decisao($historico[0], 'gestor', 'aprovada', $this->Geraldo);
    h2Decisao($historico[1], 'diretor', 'aprovada', $this->Daniela);
    h2SemEmails([$this->Sofia, $this->Geraldo, $this->Daniela, $this->Paula]);
});

test('H2 CT-18: rejeição preserva texto e histórico e volta a rascunho', function (string $origem, string $ator, int $antes, string $texto) {
    $compra = h2NaEtapa($origem);
    $anterior = h2Historico($compra);
    expect($anterior)->toHaveCount($antes);
    Notification::fake();
    $this->actingAs($this->{$ator});
    $compra->rejeitar($this->{$ator}, $texto);

    expect($compra->fresh()->situacao->value)->toBe('rascunho');
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount($antes + 1)
        ->and(array_slice($historico, 0, $antes))->toBe($anterior);
    h2Decisao($historico[$antes], $origem === 'aguardando_gestor' ? 'gestor' : 'diretor', 'rejeitada', $this->{$ator}, $texto);
    h2SemEmails([$this->Sofia, $this->Geraldo, $this->Daniela]);
})->with([
    'gestor — Sem verba' => ['aguardando_gestor', 'Geraldo', 0, 'Sem verba'],
    'diretor — Sem verba' => ['aguardando_diretor', 'Daniela', 1, 'Sem verba'],
    'gestor — Unicode' => ['aguardando_gestor', 'Geraldo', 0, 'Não há orçamento 🔧'],
]);

test('H2 CT-19: justificativa sem conteúdo não grava rejeição', function (string $origem, string $entrada) {
    $compra = h2NaEtapa($origem);
    $anterior = h2Historico($compra);
    $ator = $origem === 'aguardando_gestor' ? $this->Geraldo : $this->Daniela;
    Notification::fake();
    $this->actingAs($ator);
    if ($entrada === 'ausente') {
        expect(fn () => $compra->rejeitar($ator))->toThrow(ArgumentCountError::class);
    } elseif ($entrada === 'null') {
        expect(fn () => $compra->rejeitar($ator, null))->toThrow(TypeError::class);
    } else {
        $texto = match ($entrada) {
            'vazia' => '',
            'espacos' => '   ',
            'tab-quebra' => "\t\n",
        };
        h2RecusaNegocio(fn () => $compra->rejeitar($ator, $texto));
    }

    expect($compra->fresh()->situacao->value)->toBe($origem)
        ->and(h2Historico($compra))->toBe($anterior);
    h2SemEmails([$this->Sofia, $this->Geraldo, $this->Daniela]);
})->with([
    'gestor — vazia' => ['aguardando_gestor', 'vazia'],
    'gestor — três espaços' => ['aguardando_gestor', 'espacos'],
    'gestor — U+0009 U+000A' => ['aguardando_gestor', 'tab-quebra'],
    'gestor — null' => ['aguardando_gestor', 'null'],
    'gestor — ausente' => ['aguardando_gestor', 'ausente'],
    'diretor — vazia' => ['aguardando_diretor', 'vazia'],
    'diretor — três espaços' => ['aguardando_diretor', 'espacos'],
    'diretor — U+0009 U+000A' => ['aguardando_diretor', 'tab-quebra'],
    'diretor — null' => ['aguardando_diretor', 'null'],
    'diretor — ausente' => ['aguardando_diretor', 'ausente'],
]);

test('H2 CT-21: reenvio após qualquer rejeição reinicia no gestor e conserva decisões', function (string $etapa, int $decisoes) {
    $compra = h2NaEtapa($etapa === 'gestor' ? 'aguardando_gestor' : 'aguardando_diretor');
    $this->actingAs($etapa === 'gestor' ? $this->Geraldo : $this->Daniela);
    $compra->rejeitar($etapa === 'gestor' ? $this->Geraldo : $this->Daniela, 'Sem verba');
    $anterior = h2Historico($compra);
    expect($anterior)->toHaveCount($decisoes);
    Notification::fake();
    $this->actingAs($this->Sofia);
    $compra->enviar($this->Sofia);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and(h2Historico($compra))->toBe($anterior);
    h2Aviso($this->Geraldo, $compra, 'gestor');
    h2SemEmails([$this->Daniela]);
})->with([
    'gestor — uma decisão' => ['gestor', 1],
    'diretor — duas decisões' => ['diretor', 2],
]);

test('H2 CT-22: correção de alta para baixa muda a alçada do novo ciclo', function () {
    $compra = h2NaEtapa('aguardando_diretor');
    $this->actingAs($this->Daniela);
    $compra->rejeitar($this->Daniela, 'Sem verba');
    $anterior = h2Historico($compra);
    $this->actingAs($this->Sofia);
    $compra->editar(['valor' => '4999.99'], $this->Sofia);
    $compra->enviar($this->Sofia);
    Notification::fake();
    $this->actingAs($this->Geraldo);
    $compra->aprovar($this->Geraldo);

    expect($compra->fresh()->situacao->value)->toBe('aprovada')
        ->and($compra->fresh()->valor)->toBe('4999.99');
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount(3)
        ->and(array_slice($historico, 0, 2))->toBe($anterior);
    h2Decisao($historico[2], 'gestor', 'aprovada', $this->Geraldo);
    h2SemEmails([$this->Daniela]);
});

test('H2 CT-35 parcial: diretor não decide antes do gestor', function (string $operacao) {
    $compra = h2NaEtapa('aguardando_gestor');
    $anterior = h2Historico($compra);
    $rui = usuarioComPapel('panel_user', $this->acmeH2, 'rui@h2.test');
    Notification::fake();
    $this->actingAs($this->Daniela);
    h2RecusaNegocio(fn () => $operacao === 'aprovar'
        ? $compra->aprovar($this->Daniela)
        : $compra->rejeitar($this->Daniela, 'Sem verba'));

    expect($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and(h2Historico($compra))->toBe($anterior);
    h2SemEmails([$this->Sofia, $this->Geraldo, $this->Paula, $this->Daniela, $rui]);
})->with([
    'diretor antes do gestor — aprovar' => ['aprovar'],
    'diretor antes do gestor — rejeitar' => ['rejeitar'],
]);

test('H2 CT-42: todos os diretores de Acme recebem uma vez e Globex não recebe', function (int $quantidade) {
    $globex = tenant('Globex', 'h2-globex');
    noPainelDa($globex);
    $roleClass = app(PermissionRegistrar::class)->getRoleClass();
    $roleClass::findOrCreate('diretor', 'web')->forceFill(['painel' => 'app'])->save();
    $rui = usuarioComPapel('diretor', $globex, 'rui@h2.test');
    papelNaOrganizacao($this->Daniela, 'diretor', $globex);
    noPainelDa($this->acmeH2);
    $diretores = [$this->Daniela];
    if ($quantidade === 2) {
        papelNaOrganizacao($this->Paula, 'diretor', $this->acmeH2);
        $diretores[] = $this->Paula;
    }
    $compra = h2NaEtapa('aguardando_gestor');
    Notification::fake();
    $this->actingAs($this->Geraldo);
    $compra->aprovar($this->Geraldo);

    expect($compra->fresh()->situacao->value)->toBe('aguardando_diretor');
    foreach ($diretores as $diretor) {
        h2Aviso($diretor, $compra, 'diretor');
    }
    Notification::assertSentTimes(AprovacaoPendente::class, $quantidade);
    h2SemEmails([$rui, $this->Sofia, $this->Geraldo]);
})->with([
    'um — Daniela' => [1],
    'dois — Daniela e Paula' => [2],
]);

test('H2 CT-70: correção de baixa para alta exige diretor e conserva a rejeição antiga', function () {
    h2LimiteLiteral();
    papelNaOrganizacao($this->Paula, 'diretor', $this->acmeH2);
    $compra = h2NaEtapa('aguardando_gestor', '4999.99');
    $id = $compra->id;
    $this->actingAs($this->Geraldo);
    $compra->rejeitar($this->Geraldo, 'Sem verba');
    $anterior = h2Historico($compra);
    $this->actingAs($this->Sofia);
    $compra->editar(['valor' => '5000.01'], $this->Sofia);
    $compra->enviar($this->Sofia);
    Notification::fake();
    $this->actingAs($this->Geraldo);
    $compra->aprovar($this->Geraldo);

    expect($compra->fresh()->id)->toBe($id)
        ->and($compra->fresh()->valor)->toBe('5000.01')
        ->and($compra->fresh()->situacao->value)->toBe('aguardando_diretor');
    $historico = h2Historico($compra);
    expect($historico)->toHaveCount(2)
        ->and($historico[0])->toBe($anterior[0]);
    h2Decisao($historico[1], 'gestor', 'aprovada', $this->Geraldo);
    h2Aviso($this->Daniela, $compra, 'diretor');
    h2Aviso($this->Paula, $compra, 'diretor');
    h2SemEmails([$this->Sofia, $this->Geraldo]);
});

test('H2 CT-76: terceiro envio após duas rejeições conserva ambas e avisa somente gestor', function () {
    papelNaOrganizacao($this->Paula, 'diretor', $this->acmeH2);
    $compra = h2NaEtapa('aguardando_gestor');
    $id = $compra->id;
    $this->actingAs($this->Geraldo);
    $compra->rejeitar($this->Geraldo, 'Sem verba');
    $this->actingAs($this->Sofia);
    $compra->enviar($this->Sofia);
    $this->actingAs($this->Geraldo);
    $compra->rejeitar($this->Geraldo, 'Sem verba');
    $anterior = h2Historico($compra);
    expect($anterior)->toHaveCount(2)
        ->and($anterior[0]['id'])->not->toBe($anterior[1]['id']);
    Notification::fake();
    $this->actingAs($this->Sofia);
    $compra->enviar($this->Sofia);

    expect($compra->fresh()->id)->toBe($id)
        ->and($compra->fresh()->situacao->value)->toBe('aguardando_gestor')
        ->and(h2Historico($compra))->toBe($anterior);
    h2Aviso($this->Geraldo, $compra, 'gestor');
    Notification::assertSentTimes(AprovacaoPendente::class, 1);
    h2SemEmails([$this->Sofia, $this->Daniela, $this->Paula]);
});
