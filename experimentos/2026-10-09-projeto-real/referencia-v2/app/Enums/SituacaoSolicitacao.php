<?php

namespace App\Enums;

use Filament\Support\Contracts\HasColor;
use Filament\Support\Contracts\HasLabel;

enum SituacaoSolicitacao: string implements HasColor, HasLabel
{
    case Rascunho          = 'rascunho';
    case AguardandoGestor  = 'aguardando_gestor';
    case AguardandoDiretor = 'aguardando_diretor';
    case Aprovada          = 'aprovada';
    case Cancelada         = 'cancelada';

    public function getLabel(): string
    {
        return match ($this) {
            self::Rascunho          => 'Rascunho', self::AguardandoGestor => 'Aguardando gestor',
            self::AguardandoDiretor => 'Aguardando diretor', self::Aprovada => 'Aprovada', self::Cancelada => 'Cancelada',
        };
    }

    public function getColor(): string
    {
        return match ($this) {
            self::Rascunho => 'gray', self::AguardandoGestor, self::AguardandoDiretor => 'warning',
            self::Aprovada => 'success', self::Cancelada => 'danger',
        };
    }

    public function emTransito(): bool
    {
        return in_array($this, [self::AguardandoGestor, self::AguardandoDiretor], true);
    }
}
