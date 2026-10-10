<?php

namespace App\Filament\App\Resources\CentrosCusto;

use App\Filament\App\Resources\CentrosCusto\Pages\CreateCentroCusto;
use App\Filament\App\Resources\CentrosCusto\Pages\EditCentroCusto;
use App\Filament\App\Resources\CentrosCusto\Pages\ListCentrosCusto;
use App\Filament\Concerns\BadgeContagemNavegacao;
use App\Models\CentroCusto;
use BackedEnum;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Facades\Filament;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;

class CentroCustoResource extends Resource
{
    use BadgeContagemNavegacao;

    protected static ?string $model = CentroCusto::class;

    protected static ?string $slug = 'centros-de-custo';

    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedBuildingOffice;

    protected static ?string $modelLabel = 'centro de custo';

    protected static ?string $pluralModelLabel = 'centros de custo';

    protected static ?string $recordTitleAttribute = 'nome';

    public static function form(Schema $schema): Schema
    {
        return $schema->components([
            TextInput::make('nome')->label('Nome')->required()->maxLength(120)->scopedUnique(ignoreRecord: true),
            Select::make('gestor_id')->label('Gestor')->relationship('gestor', 'name', modifyQueryUsing: fn (Builder $query): Builder => Filament::getTenant() ? $query->whereHas('tenants', fn (Builder $tenants): Builder => $tenants->whereKey(Filament::getTenant()->getKey())) : $query)->searchable()->preload(),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([TextColumn::make('nome')->label('Nome')->searchable()->sortable(), TextColumn::make('gestor.name')->label('Gestor')])->recordActions([EditAction::make(), DeleteAction::make()]);
    }

    public static function getPages(): array
    {
        return ['index' => ListCentrosCusto::route('/'), 'create' => CreateCentroCusto::route('/create'), 'edit' => EditCentroCusto::route('/{record}/edit')];
    }
}
