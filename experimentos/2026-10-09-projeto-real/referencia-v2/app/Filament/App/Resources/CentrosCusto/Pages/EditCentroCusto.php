<?php

namespace App\Filament\App\Resources\CentrosCusto\Pages;

use App\Filament\App\Resources\CentrosCusto\CentroCustoResource;
use Filament\Actions\DeleteAction;
use Filament\Resources\Pages\EditRecord;

class EditCentroCusto extends EditRecord
{
    protected static string $resource = CentroCustoResource::class;

    protected function getHeaderActions(): array
    {
        return [
            DeleteAction::make(),
        ];
    }
}
