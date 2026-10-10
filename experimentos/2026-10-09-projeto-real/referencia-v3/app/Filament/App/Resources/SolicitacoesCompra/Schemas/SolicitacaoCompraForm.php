<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Schemas;

use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

class SolicitacaoCompraForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema->components([
            TextInput::make('descricao')->label('Descrição')->required()->maxLength(255),
            TextInput::make('valor')->label('Valor')->required()->numeric()->minValue(0.01)->maxValue(9999999999.99)->rules(['decimal:0,2'])->prefix('R$'),
            Select::make('centro_custo_id')->label('Centro de custo')->relationship('centroCusto', 'nome')->required()->searchable()->preload(),
        ]);
    }
}
