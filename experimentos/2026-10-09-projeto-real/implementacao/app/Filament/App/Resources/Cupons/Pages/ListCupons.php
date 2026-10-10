<?php

namespace App\Filament\App\Resources\Cupons\Pages;

use App\Filament\App\Resources\Cupons\CupomResource;
use Asmit\ResizedColumn\HasResizableColumn;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListCupons extends ListRecords
{
    use HasResizableColumn;

    protected static string $resource = CupomResource::class;

    protected function getHeaderActions(): array
    {
        return [
            CreateAction::make(),
        ];
    }
}
