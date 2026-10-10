<?php

namespace App\Filament\App\Resources\Cupons;

use App\Enums\TipoDeDesconto;
use App\Filament\App\Resources\Cupons\Pages\CreateCupom;
use App\Filament\App\Resources\Cupons\Pages\EditCupom;
use App\Filament\App\Resources\Cupons\Pages\ListCupons;
use App\Filament\Concerns\BadgeContagemNavegacao;
use App\Models\Cupom;
use BackedEnum;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Forms\Components\DateTimePicker;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Resources\Resource;
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\Auth;

class CupomResource extends Resource
{
    use BadgeContagemNavegacao;

    protected static ?string $model = Cupom::class;

    protected static ?string $slug = 'cupons';

    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedTicket;

    protected static ?string $modelLabel = 'cupom';

    protected static ?string $pluralModelLabel = 'cupons';

    protected static ?string $recordTitleAttribute = 'codigo';

    public static function form(Schema $schema): Schema
    {
        return $schema->components([
            TextInput::make('codigo')->label('Código')->required()->maxLength(40)
                ->mutateStateForValidationUsing(fn (?string $state): string => mb_strtoupper(trim($state ?? '')))
                ->dehydrateStateUsing(fn (?string $state): string => mb_strtoupper(trim($state ?? '')))
                ->scopedUnique(ignoreRecord: true),
            Select::make('tipo')->label('Tipo')->options(TipoDeDesconto::class)->default(TipoDeDesconto::Porcentagem)->required()->live(),
            TextInput::make('valor')->label(fn (Get $get): string => $get('tipo') === TipoDeDesconto::Fixo->value ? 'Valor do desconto (centavos)' : 'Percentual de desconto')
                ->required()->numeric()->rules(['integer'])->minValue(1)->maxValue(fn (Get $get): ?int => $get('tipo') === TipoDeDesconto::Porcentagem->value ? 100 : null),
            DateTimePicker::make('expira_em')->label('Válido até')->required()->seconds(false)->minDate(now())->helperText('Depois deste instante o cupom deixa de ser aceito.'),
            TextInput::make('limite_de_usos')->label('Limite de usos')->required()->numeric()->rules(['integer'])->minValue(1),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->defaultSort('expira_em', 'desc')->columns([
            TextColumn::make('codigo')->label('Código')->searchable()->sortable(),
            TextColumn::make('tipo')->label('Tipo')->badge(),
            TextColumn::make('valor')->label('Desconto')->formatStateUsing(fn (Cupom $record): string => $record->tipo === TipoDeDesconto::Fixo ? 'R$ '.number_format($record->valor / 100, 2, ',', '.') : $record->valor.'%'),
            TextColumn::make('usos')->label('Usos')->formatStateUsing(fn (Cupom $record): string => $record->usos.'/'.$record->limite_de_usos),
            TextColumn::make('expira_em')->label('Válido até')->dateTime('d/m/Y H:i')->sortable(),
            TextColumn::make('situacao')->label('Situação')->badge()->state(fn (Cupom $record): string => $record->situacao())->color(fn (string $state): string => match ($state) {
                'Ativo' => 'success', 'Esgotado' => 'warning', default => 'danger'
            }),
        ])->recordActions([EditAction::make(), DeleteAction::make()]);
    }

    public static function getEloquentQuery(): Builder
    {
        $query = parent::getEloquentQuery();

        return Auth::user()?->can('Update:Cupom') ? $query : $query->ativos();
    }

    public static function getPages(): array
    {
        return ['index' => ListCupons::route('/'), 'create' => CreateCupom::route('/create'), 'edit' => EditCupom::route('/{record}/edit')];
    }
}
