<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Pages;

use App\Filament\App\Resources\SolicitacoesCompra\SolicitacaoCompraResource;
use Asmit\ResizedColumn\HasResizableColumn;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListSolicitacoesCompra extends ListRecords
{
    use HasResizableColumn;

    protected static string $resource = SolicitacaoCompraResource::class;

    protected function getHeaderActions(): array
    {
        return [
            CreateAction::make(),
        ];
    }
}
