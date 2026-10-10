<?php

namespace App\Filament\App\Resources\SolicitacoesCompra;

use App\Enums\SituacaoSolicitacao;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\CreateSolicitacaoCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\EditSolicitacaoCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\ListSolicitacoesCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\ViewSolicitacaoCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Schemas\SolicitacaoCompraForm;
use App\Filament\App\Resources\SolicitacoesCompra\Schemas\SolicitacaoCompraInfolist;
use App\Filament\App\Resources\SolicitacoesCompra\Tables\SolicitacoesCompraTable;
use App\Filament\Concerns\BadgeContagemNavegacao;
use App\Models\SolicitacaoCompra;
use BackedEnum;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Auth;

class SolicitacaoCompraResource extends Resource
{
    use BadgeContagemNavegacao;

    protected static ?string $model = SolicitacaoCompra::class;

    protected static ?string $slug = 'solicitacoes-de-compra';

    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedShoppingCart;

    protected static ?string $modelLabel = 'solicitação de compra';

    protected static ?string $pluralModelLabel = 'solicitações de compra';

    protected static ?string $recordTitleAttribute = 'descricao';

    public static function form(Schema $schema): Schema
    {
        return SolicitacaoCompraForm::configure($schema);
    }

    public static function infolist(Schema $schema): Schema
    {
        return SolicitacaoCompraInfolist::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return SolicitacoesCompraTable::configure($table);
    }

    public static function canEdit(Model $record): bool
    {
        return $record->situacao === SituacaoSolicitacao::Rascunho && $record->solicitante_id === Auth::id() && parent::canEdit($record);
    }

    public static function canDelete(Model $record): bool
    {
        return $record->situacao === SituacaoSolicitacao::Rascunho && $record->solicitante_id === Auth::id() && parent::canDelete($record);
    }

    public static function getPages(): array
    {
        return ['index' => ListSolicitacoesCompra::route('/'), 'create' => CreateSolicitacaoCompra::route('/create'), 'view' => ViewSolicitacaoCompra::route('/{record}'), 'edit' => EditSolicitacaoCompra::route('/{record}/edit')];
    }
}
