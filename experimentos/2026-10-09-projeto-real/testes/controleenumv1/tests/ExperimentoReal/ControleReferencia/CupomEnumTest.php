<?php

use App\Enums\TipoDeDesconto;
use App\Filament\App\Resources\Cupons\Pages\CreateCupom;
use App\Models\Cupom;
use App\Models\Tenant;
use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Filament\Facades\Filament;
use Livewire\Livewire;
use Spatie\Permission\PermissionRegistrar;

it('aplica o teto percentual de P05 recusando 101 e persistindo exatamente 100', function (): void {
    Filament::setTenant(null, isQuiet: true);
    app(PermissionRegistrar::class)->setPermissionsTeamId(Tenant::CONTEXTO_GLOBAL);
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);

    $organizacao = Tenant::factory()->create();
    $admin = usuarioComPapel('admin_organizacao', $organizacao);
    $organizacao->users()->attach($admin->id);
    noPainelDa($organizacao);
    $this->actingAs($admin);

    expect($admin->can('Create:Cupom'))->toBeTrue()
        ->and(Cupom::query()->count())->toBe(0);

    $dados = [
        'codigo' => 'CONTROLEENUMV3',
        'tipo' => TipoDeDesconto::Porcentagem->value,
        'valor' => 100,
        'expira_em' => now()->addDay()->format('Y-m-d H:i:s'),
        'limite_de_usos' => 10,
    ];

    Livewire::test(CreateCupom::class)
        ->fillForm(array_replace($dados, ['valor' => 101]))
        ->call('create')
        ->assertHasFormErrors(['valor' => 'max'])
        ->assertHasNoFormErrors(['codigo', 'tipo', 'expira_em', 'limite_de_usos']);

    expect(Cupom::query()->count())->toBe(0);

    Livewire::test(CreateCupom::class)
        ->fillForm($dados)
        ->call('create')
        ->assertHasNoFormErrors();

    $cupom = Cupom::query()->sole();
    expect($cupom->valor)->toBe(100)
        ->and($cupom->tipo)->toBe(TipoDeDesconto::Porcentagem)
        ->and($cupom->usos)->toBe(0)
        ->and($cupom->codigo)->toBe('CONTROLEENUMV3')
        ->and($cupom->tenant_id)->toBe($organizacao->id);
});
