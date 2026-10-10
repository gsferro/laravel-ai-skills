<?php

use App\Filament\App\Resources\Cupons\Pages\CreateCupom;
use App\Models\Cupom;
use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Database\QueryException;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\DB;
use Livewire\Livewire;
use PHPUnit\Framework\Assert;

// Primeira tradução de M4: sem execução; fontes e limites no mapa de materialização.
beforeEach(function () {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $this->acmeM4 = tenant('Acme', 'acme');
    $this->anaM4 = usuarioComPapel('admin_organizacao', $this->acmeM4, 'ana-m4@example.test');
    $this->betoM4 = usuarioComPapel('panel_user', $this->acmeM4, 'beto-m4@example.test');
    $this->carlaM4 = usuarioComPapel('panel_user', $this->acmeM4, 'carla-m4@example.test');
    $this->acmeM4->users()->attach([$this->anaM4->id, $this->betoM4->id, $this->carlaM4->id]);
    noPainelDa($this->acmeM4);
    $this->actingAs($this->anaM4);
    $this->travelTo(Carbon::parse('2026-10-09T12:00:00Z'));

    $this->novoCupomM4 = function (string $tipo, int $valor, int $usos = 0, int $limite = 3, ?Carbon $expira = null): Cupom {
        $cupom = Cupom::factory()->create([
            'tenant_id' => $this->acmeM4->id,
            'codigo' => 'PROMO-A',
            'tipo' => $tipo,
            'valor' => $valor,
            'expira_em' => $expira ?? Carbon::parse('2026-10-10T18:00:00Z'),
            'limite_de_usos' => max($limite, $usos + 1),
            'usos' => 0,
        ]);
        for ($i = 0; $i < $usos; $i++) {
            $cupom->aplicarEm(10000, $this->betoM4);
        }
        // CT-22 contém legado acima do limite; isto prepara a fixture, não valida edição.
        $cupom->forceFill(['limite_de_usos' => $limite])->saveQuietly();

        return $cupom->refresh();
    };
    $this->trilhaM4 = static fn (Cupom $cupom): array => DB::table('cupom_usos')
        ->where('cupom_id', $cupom->id)->orderBy('id')->get()
        ->map(static fn ($linha): array => (array) $linha)->all();
    $this->recusaM4 = static function (callable $operacao): void {
        try {
            $operacao();
        } catch (Throwable $erro) {
            if ($erro instanceof Error || $erro instanceof QueryException) {
                throw $erro;
            }

            return;
        }
        Assert::fail('M4 exige recusa sem retorno de total com desconto.');
    };
});

afterEach(function () {
    $this->travelBack();
});

it('CT-10 [M4] percentual conserva o inteiro de centavos do Example', function (int $valor, int $total, int $final) {
    $cupom = ($this->novoCupomM4)('porcentagem', $valor);
    $this->actingAs($this->betoM4);

    expect($cupom->aplicarEm($total, $this->betoM4))->toBe($final);
})->with([
    '1 / 9999' => [1, 9999, 9900],
    '29 / 10000' => [29, 10000, 7100],
    '29 / 100' => [29, 100, 71],
    '100 / 9999' => [100, 9999, 0],
]);

it('CT-11 [M4] borda de meio centavo mantém desconto efetivo de dois centavos', function (int $total, int $final) {
    $cupom = ($this->novoCupomM4)('porcentagem', 5);
    $this->actingAs($this->betoM4);

    $resultado = $cupom->aplicarEm($total, $this->betoM4);

    expect($resultado)->toBe($final);
    expect($total - $resultado)->toBe(2);
})->with(['49' => [49, 47], '50' => [50, 48], '51' => [51, 49]]);

it('CT-12 [M4] fixo de mil centavos conserva o piso do total', function (int $total, int $final) {
    $cupom = ($this->novoCupomM4)('fixo', 1000);
    $this->actingAs($this->betoM4);

    expect($cupom->aplicarEm($total, $this->betoM4))->toBe($final);
})->with(['999' => [999, 0], '1000' => [1000, 0], '1001' => [1001, 1]]);

it('CT-13 [M4] segundo exato da expiração recusa e segundo anterior aceita', function (string $tipo, string $agora, bool $aceito, int $usos, int $trilhas) {
    $cupom = ($this->novoCupomM4)($tipo, $tipo === 'fixo' ? 1000 : 10, 1, 3, Carbon::parse('2026-10-09T18:00:00Z'));
    $antes = ($this->trilhaM4)($cupom);
    $this->actingAs($this->betoM4);
    $this->travelTo(Carbon::parse($agora));

    if ($aceito) {
        expect($cupom->aplicarEm(10000, $this->betoM4))->toBe(9000);
    } else {
        ($this->recusaM4)(fn () => $cupom->aplicarEm(10000, $this->betoM4));
    }

    expect($cupom->refresh()->usos)->toBe($usos);
    $depois = ($this->trilhaM4)($cupom);
    expect($depois)->toHaveCount($trilhas);
    expect(array_values(array_filter($depois, static fn (array $linha): bool => in_array($linha['id'], array_column($antes, 'id'), true))))->toBe($antes);
})->with([
    'porcentagem antes' => ['porcentagem', '2026-10-09T17:59:59Z', true, 2, 2],
    'porcentagem borda' => ['porcentagem', '2026-10-09T18:00:00Z', false, 1, 1],
    'porcentagem depois' => ['porcentagem', '2026-10-09T18:00:01Z', false, 1, 1],
    'fixo antes' => ['fixo', '2026-10-09T17:59:59Z', true, 2, 2],
    'fixo borda' => ['fixo', '2026-10-09T18:00:00Z', false, 1, 1],
    'fixo depois' => ['fixo', '2026-10-09T18:00:01Z', false, 1, 1],
]);

it('CT-22 [M4] último uso aceita e limite atingido ou ultrapassado recusa', function (string $tipo, int $antes, int $depois, bool $aceito) {
    $cupom = ($this->novoCupomM4)($tipo, $tipo === 'fixo' ? 1000 : 10, $antes);
    $trilhaAntes = ($this->trilhaM4)($cupom);
    $this->actingAs($this->betoM4);

    if ($aceito) {
        expect($cupom->aplicarEm(10000, $this->betoM4))->toBe(9000);
    } else {
        ($this->recusaM4)(fn () => $cupom->aplicarEm(10000, $this->betoM4));
    }

    expect($cupom->refresh()->usos)->toBe($depois);
    $trilhaDepois = ($this->trilhaM4)($cupom);
    expect($trilhaDepois)->toHaveCount($depois);
    expect(array_values(array_filter($trilhaDepois, static fn (array $linha): bool => in_array($linha['id'], array_column($trilhaAntes, 'id'), true))))->toBe($trilhaAntes);
})->with([
    'porcentagem 2 / 3' => ['porcentagem', 2, 3, true],
    'porcentagem 3 / 3' => ['porcentagem', 3, 3, false],
    'porcentagem 4 / 3 legado' => ['porcentagem', 4, 4, false],
    'fixo 2 / 3' => ['fixo', 2, 3, true],
    'fixo 3 / 3' => ['fixo', 3, 3, false],
    'fixo 4 / 3 legado' => ['fixo', 4, 4, false],
]);

it('CT-26 [M4] motor registra Beto e o instante sem atribuir a Ana ou autor nulo', function (string $tipo) {
    $cupom = ($this->novoCupomM4)($tipo, $tipo === 'fixo' ? 1000 : 10);
    $this->actingAs($this->betoM4);
    $instante = Carbon::parse('2026-10-09T18:00:00Z');
    $this->travelTo($instante);

    expect($cupom->aplicarEm(10000, $this->betoM4))->toBe(9000);
    expect($cupom->refresh()->usos)->toBe(1);
    $linhas = ($this->trilhaM4)($cupom);
    expect($linhas)->toHaveCount(1);
    expect($linhas[0]['cupom_id'])->toBe($cupom->id);
    expect($linhas[0]['aplicado_por_id'])->toBe($this->betoM4->id);
    expect($linhas[0]['aplicado_por_id'])->not->toBe($this->anaM4->id)->not->toBeNull();
    expect(Carbon::parse($linhas[0]['created_at'])->getTimestamp())->toBe($instante->getTimestamp());
})->with(['porcentagem' => ['porcentagem'], 'fixo' => ['fixo']]);

it('CT-28 [M4] aplicação de Carla acrescenta só sua linha e preserva Beto', function (string $tipo) {
    $cupom = ($this->novoCupomM4)($tipo, $tipo === 'fixo' ? 1000 : 10);
    $instante = Carbon::parse('2026-10-09T18:00:00Z');
    $this->actingAs($this->betoM4);
    $this->travelTo($instante);
    $cupom->aplicarEm(10000, $this->betoM4);
    $antes = ($this->trilhaM4)($cupom);
    $this->actingAs($this->carlaM4);
    $this->travelTo($instante->copy()->addSecond());

    expect($cupom->aplicarEm(10000, $this->carlaM4))->toBe(9000);
    expect($cupom->refresh()->usos)->toBe(2);
    $depois = ($this->trilhaM4)($cupom);
    expect($depois)->toHaveCount(2);
    expect($depois[0])->toBe($antes[0]);
    expect($depois[0]['aplicado_por_id'])->toBe($this->betoM4->id);
    expect(Carbon::parse($depois[0]['created_at'])->getTimestamp())->toBe($instante->getTimestamp());
    expect($depois[1]['aplicado_por_id'])->toBe($this->carlaM4->id);
    expect(Carbon::parse($depois[1]['created_at'])->getTimestamp())->toBe($instante->getTimestamp() + 1);
})->with(['porcentagem' => ['porcentagem'], 'fixo' => ['fixo']]);

it('CT-41 [M4] pessoa aplicadora nula recusa sem consumir nem criar trilha', function (string $tipo) {
    $cupom = ($this->novoCupomM4)($tipo, $tipo === 'fixo' ? 1000 : 10);
    $this->actingAs($this->betoM4);

    $recusada = false;
    try {
        $cupom->aplicarEm(10000, null);
    } catch (Throwable $erro) {
        if (($erro instanceof Error && ! ($erro instanceof TypeError)) || $erro instanceof QueryException) {
            throw $erro;
        }
        $recusada = true;
    }

    expect($recusada)->toBeTrue();
    expect($cupom->refresh()->usos)->toBe(0);
    expect(($this->trilhaM4)($cupom))->toHaveCount(0);
})->with(['porcentagem' => ['porcentagem'], 'fixo' => ['fixo']]);

// Seleção exploratória posterior ao julgamento: apenas a linha literal fixo/-1 de CT-07.
it('CT-07 [M4] seleção posterior ao julgamento recusa criação por componente de fixo negativo', function () {
    Livewire::test(CreateCupom::class)->fillForm([
        'codigo' => 'NOVO',
        'tipo' => 'fixo',
        'valor' => -1,
        'expira_em' => '2026-10-10T18:00:00Z',
        'limite_de_usos' => 3,
    ])->call('create')->assertHasFormErrors();

    expect(DB::table('cupons')->count())->toBe(0);
    expect(DB::table('cupom_usos')->count())->toBe(0);
});
