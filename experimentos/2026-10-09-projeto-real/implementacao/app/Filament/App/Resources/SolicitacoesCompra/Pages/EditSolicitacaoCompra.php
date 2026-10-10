<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Pages;

use App\Filament\App\Resources\SolicitacoesCompra\SolicitacaoCompraResource;
use Filament\Actions\ViewAction;
use Filament\Resources\Pages\EditRecord;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Auth;

class EditSolicitacaoCompra extends EditRecord
{
    protected static string $resource = SolicitacaoCompraResource::class;

    protected function handleRecordUpdate(Model $record, array $data): Model
    {
        $record->editar($data, Auth::user());

        return $record;
    }

    protected function getHeaderActions(): array
    {
        return [ViewAction::make()];
    }
}
