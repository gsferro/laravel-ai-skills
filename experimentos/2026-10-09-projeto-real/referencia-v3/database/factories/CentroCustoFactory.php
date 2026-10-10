<?php

namespace Database\Factories;

use App\Models\CentroCusto;
use App\Models\Tenant;
use App\Models\User;
use Filament\Facades\Filament;
use Illuminate\Database\Eloquent\Factories\Factory;

/** @extends Factory<CentroCusto> */
class CentroCustoFactory extends Factory
{
    protected $model = CentroCusto::class;

    public function definition(): array
    {
        return ['tenant_id' => Filament::getTenant()?->getKey() ?? Tenant::factory(), 'nome' => fake()->unique()->bothify('Centro ???? #####'), 'gestor_id' => User::factory()];
    }
}
