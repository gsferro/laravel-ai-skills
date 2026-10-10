<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Pages;

use App\Enums\SituacaoSolicitacao;
use App\Filament\App\Resources\SolicitacoesCompra\SolicitacaoCompraResource;
use App\Models\SolicitacaoCompra;
use Filament\Resources\Pages\CreateRecord;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Auth;

class CreateSolicitacaoCompra extends CreateRecord
{
    protected static string $resource = SolicitacaoCompraResource::class;

    protected function handleRecordCreation(array $data): Model
    {
        $record                 = new SolicitacaoCompra($data);
        $record->solicitante_id = Auth::id();
        $record->situacao       = SituacaoSolicitacao::Rascunho;
        $record->save();

        return $record;
    }
}
