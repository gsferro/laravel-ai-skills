<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Pages;

use App\Filament\App\Resources\SolicitacoesCompra\SolicitacaoCompraResource;
use Filament\Actions\EditAction;
use Filament\Resources\Pages\ViewRecord;

class ViewSolicitacaoCompra extends ViewRecord
{
    protected static string $resource = SolicitacaoCompraResource::class;

    protected function getHeaderActions(): array
    {
        return [
            EditAction::make(),
        ];
    }
}
