<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Tables;

use App\Enums\SituacaoSolicitacao;
use App\Models\SolicitacaoCompra;
use Closure;
use Filament\Actions\Action;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;
use Filament\Forms\Components\Textarea;
use Filament\Notifications\Notification;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Table;
use Illuminate\Support\Facades\Auth;
use RuntimeException;

class SolicitacoesCompraTable
{
    public static function configure(Table $table): Table
    {
        $enviar   = fn (SolicitacaoCompra $record): bool => $record->situacao === SituacaoSolicitacao::Rascunho && $record->solicitante_id === Auth::id();
        $decidir  = fn (SolicitacaoCompra $record): bool => $record->podeSerDecididaPor(Auth::user());
        $cancelar = fn (SolicitacaoCompra $record): bool => $record->situacao->emTransito() && $record->solicitante_id === Auth::id();

        return $table->columns([
            TextColumn::make('descricao')->label('Descrição')->searchable(), TextColumn::make('valor')->label('Valor')->money('BRL'),
            TextColumn::make('centroCusto.nome')->label('Centro de custo'), TextColumn::make('solicitante.name')->label('Solicitante'), TextColumn::make('situacao')->label('Situação')->badge(),
        ])->filters([SelectFilter::make('situacao')->label('Situação')->options(SituacaoSolicitacao::class)])
            ->recordActions([
                ViewAction::make(), EditAction::make(),
                DeleteAction::make()->using(function (SolicitacaoCompra $record): bool {
                    $record->excluir(Auth::user());

                    return true;
                }),
                Action::make('enviar')->label('Enviar')->requiresConfirmation()->visible($enviar)->authorize($enviar)
                    ->action(fn (SolicitacaoCompra $record, Action $action) => self::executar(fn () => $record->enviar(Auth::user()), $action))->successNotificationTitle('Solicitação enviada'),
                Action::make('aprovar')->label('Aprovar')->requiresConfirmation()->visible($decidir)->authorize($decidir)
                    ->action(fn (SolicitacaoCompra $record, Action $action) => self::executar(fn () => $record->aprovar(Auth::user()), $action))->successNotificationTitle('Etapa aprovada'),
                Action::make('rejeitar')->label('Rejeitar')->color('danger')->modalHeading('Rejeitar solicitação')->schema([Textarea::make('justificativa')->label('Motivo da rejeição')->required()->rows(4)])
                    ->visible($decidir)->authorize($decidir)->action(fn (SolicitacaoCompra $record, array $data, Action $action) => self::executar(fn () => $record->rejeitar(Auth::user(), $data['justificativa']), $action))->successNotificationTitle('Solicitação rejeitada'),
                Action::make('cancelar')->label('Cancelar')->color('danger')->requiresConfirmation()->visible($cancelar)->authorize($cancelar)
                    ->action(fn (SolicitacaoCompra $record, Action $action) => self::executar(fn () => $record->cancelar(Auth::user()), $action))->successNotificationTitle('Solicitação cancelada'),
            ]);
    }

    private static function executar(Closure $operacao, Action $action): void
    {
        try {
            $operacao();
            $action->success();
        } catch (RuntimeException $erro) {
            Notification::make()->danger()->title($erro->getMessage())->send();
            $action->halt();
        }
    }
}
