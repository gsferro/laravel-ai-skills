<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class EtapaAprovacao extends Model
{
    protected $table = 'etapas_aprovacao_compra';

    protected $fillable = ['etapa', 'decisao', 'decidido_por_id', 'justificativa'];

    public function solicitacao(): BelongsTo
    {
        return $this->belongsTo(SolicitacaoCompra::class, 'solicitacao_compra_id');
    }

    public function decididoPor(): BelongsTo
    {
        return $this->belongsTo(User::class, 'decidido_por_id');
    }
}
