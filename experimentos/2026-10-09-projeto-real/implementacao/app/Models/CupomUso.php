<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CupomUso extends Model
{
    protected $table = 'cupom_usos';

    protected $fillable = ['cupom_id', 'aplicado_por_id', 'valor_original', 'valor_desconto'];
}
