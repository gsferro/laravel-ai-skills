<?php

namespace App\Filament\App\Resources\SolicitacoesCompra\Schemas;

use Filament\Infolists\Components\RepeatableEntry;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

class SolicitacaoCompraInfolist
{
    public static function configure(Schema $schema): Schema
    {
        return $schema->components([
            Section::make('Solicitação')->columnSpanFull()->schema([
                TextEntry::make('descricao')->label('Descrição'), TextEntry::make('valor')->label('Valor')->money('BRL'),
                TextEntry::make('centroCusto.nome')->label('Centro de custo'), TextEntry::make('solicitante.name')->label('Solicitante'), TextEntry::make('situacao')->label('Situação')->badge(),
            ]),
            Section::make('Histórico de aprovação')->columnSpanFull()->schema([
                RepeatableEntry::make('etapas')->label('Etapas')->schema([
                    TextEntry::make('etapa')->label('Etapa'), TextEntry::make('decisao')->label('Decisão'), TextEntry::make('decididoPor.name')->label('Quem decidiu'),
                    TextEntry::make('created_at')->label('Quando')->dateTime('d/m/Y H:i'), TextEntry::make('justificativa')->label('Justificativa')->placeholder('—'),
                ]),
            ]),
        ]);
    }
}
