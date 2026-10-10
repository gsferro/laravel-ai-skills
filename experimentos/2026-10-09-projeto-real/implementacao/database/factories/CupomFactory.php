<?php

namespace Database\Factories;

use App\Enums\TipoDeDesconto;
use App\Models\Cupom;
use Illuminate\Database\Eloquent\Factories\Factory;

/** @extends Factory<Cupom> */
class CupomFactory extends Factory
{
    protected $model = Cupom::class;

    public function definition(): array
    {
        return ['codigo' => fake()->unique()->bothify('CUPOM-????-#####'), 'tipo' => TipoDeDesconto::Porcentagem, 'valor' => 10, 'expira_em' => now()->addDays(30), 'limite_de_usos' => 100];
    }

    public function expirado(): static
    {
        return $this->state(fn (): array => ['expira_em' => now()->subDay()]);
    }

    public function esgotado(): static
    {
        return $this->afterCreating(fn (Cupom $cupom) => $cupom->forceFill(['usos' => $cupom->limite_de_usos])->save());
    }

    public function fixo(int $centavos = 1000): static
    {
        return $this->state(fn (): array => ['tipo' => TipoDeDesconto::Fixo, 'valor' => $centavos]);
    }
}
