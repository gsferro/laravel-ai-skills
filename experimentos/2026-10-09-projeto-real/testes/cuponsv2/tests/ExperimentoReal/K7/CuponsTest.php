<?php

use App\Models\Cupom;
use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Database\QueryException;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use PHPUnit\Framework\Assert;

// Primeira tradução de K7: sem execução; fontes e limites no mapa de materialização.
beforeEach(function () {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $this->acmeK7 = tenant('Acme', 'acme');
    $this->anaK7 = usuarioComPapel('admin_organizacao', $this->acmeK7, 'ana-k7@example.test');
    $this->betoK7 = usuarioComPapel('panel_user', $this->acmeK7, 'beto-k7@example.test');
    $this->acmeK7->users()->attach([$this->anaK7->id, $this->betoK7->id]);
    noPainelDa($this->acmeK7);
    $this->actingAs($this->anaK7);
    $this->travelTo(Carbon::parse('2026-10-10T12:34:53Z'));

    $this->novoCupomK7 = function (string $tipo, int $valor, int $usos = 0, int $limite = 3, ?Carbon $expira = null, string $codigo = 'PROMO'): Cupom {
        $cupom = Cupom::factory()->create([
            'tenant_id' => $this->acmeK7->id,
            'codigo' => $codigo,
            'tipo' => $tipo,
            'valor' => $valor,
            'expira_em' => $expira ?? Carbon::parse('2026-11-10T12:34:56Z'),
            'limite_de_usos' => max($limite, $usos + 1),
            'usos' => 0,
        ]);
        for ($i = 0; $i < $usos; $i++) {
            $cupom->aplicarEm(10000, $this->anaK7);
        }
        // A linha limite+1 é legado do CT-28; não prova aceite dessa edição.
        $cupom->forceFill(['limite_de_usos' => $limite])->saveQuietly();

        return $cupom->refresh();
    };
    $this->trilhaK7 = static fn (Cupom $cupom): array => DB::table('cupom_usos')
        ->where('cupom_id', $cupom->id)->orderBy('id')->get()
        ->map(static fn ($linha): array => (array) $linha)->all();
    $this->recusaK7 = static function (callable $operacao): void {
        try {
            $operacao();
        } catch (Throwable $erro) {
            if ($erro instanceof Error || $erro instanceof QueryException) {
                throw $erro;
            }

            return;
        }
        Assert::fail('K7 exige recusa sem retorno de total com desconto.');
    };
});

afterEach(function () {
    $this->travelBack();
});

it('CT-31 [K7] percentual inteiro trunca a fração do desconto', function (int $percentual, int $total, int $final) {
    $cupom = ($this->novoCupomK7)('porcentagem', $percentual);

    expect($cupom->aplicarEm($total, $this->betoK7))->toBe($final);
    expect($cupom->refresh()->usos)->toBe(1);
    $trilha = ($this->trilhaK7)($cupom);
    expect($trilha)->toHaveCount(1);
    expect($trilha[0]['aplicado_por_id'])->toBe($this->betoK7->id);
})->with([
    '29 / 10000' => [29, 10000, 7100],
    '29 / 100' => [29, 100, 71],
    '10 / 9999' => [10, 9999, 9000],
    '5 / 50' => [5, 50, 48],
    '1 / 100' => [1, 100, 99],
    '100 / 9999' => [100, 9999, 0],
]);

it('CT-32 [K7] desconto fixo conserva piso zero', function (int $valor, int $total, int $final) {
    $cupom = ($this->novoCupomK7)('fixo', $valor);

    expect($cupom->aplicarEm($total, $this->betoK7))->toBe($final);
    expect($cupom->refresh()->usos)->toBe(1);
    $trilha = ($this->trilhaK7)($cupom);
    expect($trilha)->toHaveCount(1);
    expect($trilha[0]['aplicado_por_id'])->toBe($this->betoK7->id);
})->with([
    '1000 / 999' => [1000, 999, 0],
    '1000 / 1000' => [1000, 1000, 0],
    '1000 / 1001' => [1000, 1001, 1],
    '1 / 1' => [1, 1, 0],
    '1000 / 0' => [1000, 0, 0],
]);

it('CT-25 [K7] segundo exato da expiração recusa com controle anterior aceito', function (string $tipo, int $offset, ?int $final, int $usos, int $novas) {
    $expira = Carbon::parse('2026-10-10T12:34:56Z');
    $cupom = ($this->novoCupomK7)($tipo, $tipo === 'fixo' ? 1000 : 10, 2, 3, $expira);
    $antes = ($this->trilhaK7)($cupom);
    $this->travelTo($expira->copy()->addSeconds($offset));

    if ($final === null) {
        ($this->recusaK7)(fn () => $cupom->aplicarEm(10000, $this->betoK7));
    } else {
        expect($cupom->aplicarEm(10000, $this->betoK7))->toBe($final);
    }

    expect($cupom->refresh()->usos)->toBe($usos);
    $depois = ($this->trilhaK7)($cupom);
    expect($depois)->toHaveCount(count($antes) + $novas);
    expect(array_values(array_filter($depois, static fn (array $linha): bool => in_array($linha['id'], array_column($antes, 'id'), true))))->toBe($antes);
})->with([
    'porcentagem T-1s' => ['porcentagem', -1, 9000, 3, 1],
    'porcentagem T' => ['porcentagem', 0, null, 2, 0],
    'porcentagem T+1s' => ['porcentagem', 1, null, 2, 0],
    'fixo T-1s' => ['fixo', -1, 9000, 3, 1],
    'fixo T' => ['fixo', 0, null, 2, 0],
    'fixo T+1s' => ['fixo', 1, null, 2, 0],
]);

it('CT-28 [K7] limite atingido recusa com último uso disponível aceito', function (string $tipo, int $antes, ?int $final, int $usos, int $novas) {
    $cupom = ($this->novoCupomK7)($tipo, $tipo === 'fixo' ? 1000 : 10, $antes);
    $trilhaAntes = ($this->trilhaK7)($cupom);

    if ($final === null) {
        ($this->recusaK7)(fn () => $cupom->aplicarEm(10000, $this->betoK7));
    } else {
        expect($cupom->aplicarEm(10000, $this->betoK7))->toBe($final);
    }

    expect($cupom->refresh()->usos)->toBe($usos);
    $trilhaDepois = ($this->trilhaK7)($cupom);
    expect($trilhaDepois)->toHaveCount(count($trilhaAntes) + $novas);
    expect(array_values(array_filter($trilhaDepois, static fn (array $linha): bool => in_array($linha['id'], array_column($trilhaAntes, 'id'), true))))->toBe($trilhaAntes);
})->with([
    'porcentagem 2 / 3' => ['porcentagem', 2, 9000, 3, 1],
    'porcentagem 3 / 3' => ['porcentagem', 3, null, 3, 0],
    'porcentagem 4 / 3 legado' => ['porcentagem', 4, null, 4, 0],
    'fixo 2 / 3' => ['fixo', 2, 9000, 3, 1],
    'fixo 3 / 3' => ['fixo', 3, null, 3, 0],
    'fixo 4 / 3 legado' => ['fixo', 4, null, 4, 0],
]);

it('CT-35 [K7] aplicação incrementa uma vez e mantém as duas linhas anteriores', function (string $tipo) {
    $cupom = ($this->novoCupomK7)($tipo, $tipo === 'fixo' ? 1000 : 10, 2, 5);
    $antes = ($this->trilhaK7)($cupom);

    expect($cupom->aplicarEm(10000, $this->betoK7))->toBe(9000);
    expect($cupom->refresh()->usos)->toBe(3);
    $depois = ($this->trilhaK7)($cupom);
    expect($depois)->toHaveCount(3);
    expect(array_slice($depois, 0, 2))->toBe($antes);
    expect($depois[2]['aplicado_por_id'])->toBe($this->betoK7->id);
})->with(['porcentagem' => ['porcentagem'], 'fixo' => ['fixo']]);

it('CT-36 [K7] argumento aplicadoPor identifica Beto e o instante com guard ausente igual ou distinto', function (string $tipo, string $guard) {
    $cupom = ($this->novoCupomK7)($tipo, $tipo === 'fixo' ? 1000 : 10);
    if ($guard === 'ausente') {
        Auth::logout();
        expect(Auth::check())->toBeFalse();
    } else {
        $this->actingAs($guard === 'Beto' ? $this->betoK7 : $this->anaK7);
    }
    $instante = Carbon::parse('2026-10-10T12:34:56Z');
    $this->travelTo($instante);

    expect($cupom->aplicarEm(10000, $this->betoK7))->toBe(9000);
    expect($cupom->refresh()->usos)->toBe(1);
    $linhas = ($this->trilhaK7)($cupom);
    expect($linhas)->toHaveCount(1);
    expect($linhas[0]['cupom_id'])->toBe($cupom->id);
    expect($linhas[0]['aplicado_por_id'])->toBe($this->betoK7->id);
    expect(Carbon::parse($linhas[0]['created_at'])->getTimestamp())->toBe($instante->getTimestamp());
})->with([
    'porcentagem / ausente' => ['porcentagem', 'ausente'],
    'porcentagem / Beto' => ['porcentagem', 'Beto'],
    'porcentagem / Ana' => ['porcentagem', 'Ana'],
    'fixo / ausente' => ['fixo', 'ausente'],
    'fixo / Beto' => ['fixo', 'Beto'],
    'fixo / Ana' => ['fixo', 'Ana'],
]);

it('CT-37 [K7] somente B ganha a aplicação de Beto preservando A e a história anterior', function (string $tipo) {
    $a = ($this->novoCupomK7)('fixo', 3000, 0, 5, null, 'A');
    $b = ($this->novoCupomK7)($tipo, $tipo === 'fixo' ? 1000 : 10, 0, 5, null, 'B');
    $instante = Carbon::parse('2026-10-10T12:34:56Z');
    $this->travelTo($instante->copy()->subSeconds(2));
    $a->aplicarEm(10000, $this->anaK7);
    $this->travelTo($instante->copy()->subSecond());
    $b->aplicarEm(10000, $this->anaK7);
    $atributosA = (array) DB::table('cupons')->where('id', $a->id)->first();
    $trilhaA = ($this->trilhaK7)($a);
    $trilhaB = ($this->trilhaK7)($b);
    expect(Cupom::query()->firstOrFail()->getKey())->toBe($a->getKey());
    Auth::logout();
    expect(Auth::check())->toBeFalse();
    $this->travelTo($instante);

    expect($b->aplicarEm(10000, $this->betoK7))->toBe(9000);
    expect($b->refresh()->usos)->toBe(2);
    $depoisB = ($this->trilhaK7)($b);
    expect($depoisB)->toHaveCount(2);
    expect($depoisB[0])->toBe($trilhaB[0]);
    expect($depoisB[0]['aplicado_por_id'])->toBe($this->anaK7->id);
    expect(Carbon::parse($depoisB[0]['created_at'])->getTimestamp())->toBe($instante->getTimestamp() - 1);
    expect($depoisB[1]['cupom_id'])->toBe($b->id);
    expect($depoisB[1]['aplicado_por_id'])->toBe($this->betoK7->id);
    expect(Carbon::parse($depoisB[1]['created_at'])->getTimestamp())->toBe($instante->getTimestamp());
    expect((array) DB::table('cupons')->where('id', $a->id)->first())->toBe($atributosA);
    expect($a->refresh()->usos)->toBe(1);
    expect(($this->trilhaK7)($a))->toBe($trilhaA);
    expect($trilhaA)->toHaveCount(1);
    expect($trilhaA[0]['aplicado_por_id'])->toBe($this->anaK7->id);
    expect(Carbon::parse($trilhaA[0]['created_at'])->getTimestamp())->toBe($instante->getTimestamp() - 2);
})->with(['porcentagem' => ['porcentagem'], 'fixo' => ['fixo']]);
