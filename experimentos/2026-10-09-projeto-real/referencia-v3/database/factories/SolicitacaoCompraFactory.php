<?php

namespace Database\Factories;

use App\Enums\SituacaoSolicitacao;
use App\Models\CentroCusto;
use App\Models\SolicitacaoCompra;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/** @extends Factory<SolicitacaoCompra> */
class SolicitacaoCompraFactory extends Factory
{
    protected $model = SolicitacaoCompra::class;

    public function definition(): array
    {
        return ['descricao' => 'Aquisição de equipamento', 'valor' => '100.00', 'centro_custo_id' => CentroCusto::factory(), 'tenant_id' => fn (array $dados): int => CentroCusto::query()->findOrFail($dados['centro_custo_id'])->tenant_id, 'solicitante_id' => User::factory(), 'situacao' => SituacaoSolicitacao::Rascunho];
    }
}
