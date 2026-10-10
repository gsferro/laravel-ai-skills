<?php

namespace App\Filament\App\Resources\CentrosCusto\Pages;

use App\Filament\App\Resources\CentrosCusto\CentroCustoResource;
use Asmit\ResizedColumn\HasResizableColumn;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListCentrosCusto extends ListRecords
{
    use HasResizableColumn;

    protected static string $resource = CentroCustoResource::class;

    protected function getHeaderActions(): array
    {
        return [
            CreateAction::make(),
        ];
    }
}
