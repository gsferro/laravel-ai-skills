<?php

namespace App\Notifications;

use App\Filament\App\Resources\SolicitacoesCompra\SolicitacaoCompraResource;
use App\Models\SolicitacaoCompra;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class AprovacaoPendente extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(public readonly SolicitacaoCompra $solicitacao, public readonly string $etapa)
    {
        $this->afterCommit();
    }

    public function via(object $notifiable): array
    {
        return ['mail'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)->subject('Solicitação de compra aguardando aprovação')->greeting('Olá, '.$notifiable->name.'!')
            ->line('Etapa de aprovação: '.$this->etapa.'.')
            ->line('Solicitante: '.$this->solicitacao->solicitante->name)
            ->line('Descrição: '.$this->solicitacao->descricao)
            ->line('Valor: R$ '.number_format((float) $this->solicitacao->valor, 2, ',', '.'))
            ->line('Centro de custo: '.$this->solicitacao->centroCusto->nome)
            ->action('Ver solicitação', SolicitacaoCompraResource::getUrl('view', ['record' => $this->solicitacao], panel: 'app', tenant: $this->solicitacao->tenant));
    }
}
