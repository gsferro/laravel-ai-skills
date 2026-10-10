<?php

namespace App\Models;

use App\Traits\AuditsFillables;
use App\Traits\BelongsToTenant;
use App\Traits\TemUuid;
use Database\Factories\CentroCustoFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use OwenIt\Auditing\Contracts\Auditable;

class CentroCusto extends Model implements Auditable
{
    use AuditsFillables, BelongsToTenant, TemUuid;

    /** @use HasFactory<CentroCustoFactory> */
    use HasFactory;

    protected $table = 'centros_custo';

    protected $fillable = ['nome', 'gestor_id'];

    public function gestor(): BelongsTo
    {
        return $this->belongsTo(User::class, 'gestor_id');
    }
}
