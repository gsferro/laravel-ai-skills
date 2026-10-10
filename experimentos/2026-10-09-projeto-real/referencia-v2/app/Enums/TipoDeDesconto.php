<?php

namespace App\Enums;

use Filament\Support\Contracts\HasLabel;

enum TipoDeDesconto: string implements HasLabel
{
    case Porcentagem = 'porcentagem';
    case Fixo        = 'fixo';

    public function getLabel(): string
    {
        return match ($this) {
            self::Porcentagem => 'Porcentagem', self::Fixo => 'Valor fixo'
        };
    }
}
