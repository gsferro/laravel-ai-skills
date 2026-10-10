<?php

namespace App\Models;

use App\Enums\TipoDeDesconto;
use App\Traits\AuditsFillables;
use App\Traits\BelongsToTenant;
use App\Traits\TemUuid;
use Database\Factories\CupomFactory;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use InvalidArgumentException;
use OwenIt\Auditing\Contracts\Auditable;
use RuntimeException;

class Cupom extends Model implements Auditable
{
    use AuditsFillables, BelongsToTenant, TemUuid;

    /** @use HasFactory<CupomFactory> */
    use HasFactory;

    protected $table = 'cupons';

    protected $fillable = ['codigo', 'tipo', 'valor', 'expira_em', 'limite_de_usos'];

    protected function casts(): array
    {
        return ['tipo' => TipoDeDesconto::class, 'expira_em' => 'datetime', 'valor' => 'integer', 'usos' => 'integer', 'limite_de_usos' => 'integer'];
    }

    protected function codigo(): Attribute
    {
        return Attribute::set(fn (string $valor): string => mb_strtoupper(trim($valor)));
    }

    public function scopeAtivos(Builder $query): Builder
    {
        return $query->where('expira_em', '>', now())->whereColumn('usos', '<', 'limite_de_usos');
    }

    public function situacao(): string
    {
        return match (true) {
            $this->usos >= $this->limite_de_usos       => 'Esgotado',
            $this->expira_em->lessThanOrEqualTo(now()) => 'Expirado',
            default                                    => 'Ativo',
        };
    }

    public static function valido(?string $codigo): ?self
    {
        $cupom = blank($codigo) ? null : static::query()->where('codigo', mb_strtoupper(trim($codigo)))->ativos()->first();
        if ($cupom === null) {
            Log::channel('cupom')->info('[Cupom@valido] Código recusado', ['codigo' => $codigo, 'motivo' => blank($codigo) ? 'codigo_vazio' : 'nao_encontrado']);
        }

        return $cupom;
    }

    public function descontoSobre(int $valorTotalEmCentavos): int
    {
        if ($valorTotalEmCentavos < 0) {
            throw new InvalidArgumentException('O total não pode ser negativo.');
        }

        return match ($this->tipo) {
            TipoDeDesconto::Porcentagem => intdiv($valorTotalEmCentavos, 100) * $this->valor + intdiv(($valorTotalEmCentavos % 100) * $this->valor, 100),
            TipoDeDesconto::Fixo        => $this->valor,
        };
    }

    public function aplicarEm(int $valorTotalEmCentavos, ?User $aplicadoPor = null): int
    {
        $this->descontoSobre($valorTotalEmCentavos);

        return DB::transaction(function () use ($valorTotalEmCentavos, $aplicadoPor): int {
            $consumido = static::query()->whereKey($this->getKey())->ativos()->increment('usos');
            if ($consumido !== 1) {
                Log::channel('cupom')->warning('[Cupom@aplicarEm] Consumo recusado no UPDATE atômico', ['cupom_id' => $this->getKey(), 'motivo' => 'esgotado_ou_expirado']);
                throw new RuntimeException('Este cupom não está mais disponível.');
            }
            $this->refresh();
            $desconto = $this->descontoSobre($valorTotalEmCentavos);
            CupomUso::create(['cupom_id' => $this->getKey(), 'aplicado_por_id' => $aplicadoPor?->getKey(), 'valor_original' => $valorTotalEmCentavos, 'valor_desconto' => $desconto]);
            Log::channel('cupom')->info('[Cupom@aplicarEm] Desconto aplicado', ['cupom_id' => $this->getKey(), 'tenant_id' => $this->tenant_id, 'codigo' => $this->codigo, 'tipo' => $this->tipo->value, 'valor_original' => $valorTotalEmCentavos, 'valor_desconto' => $desconto, 'aplicado_por' => $aplicadoPor?->getKey(), 'usos_apos' => $this->usos, 'limite_de_usos' => $this->limite_de_usos]);

            return max(0, $valorTotalEmCentavos - $desconto);
        });
    }
}
