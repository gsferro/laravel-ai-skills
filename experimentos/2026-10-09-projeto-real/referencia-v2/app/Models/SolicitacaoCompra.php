<?php

namespace App\Models;

use App\Enums\SituacaoSolicitacao;
use App\Notifications\AprovacaoPendente;
use App\Traits\AuditsFillables;
use App\Traits\BelongsToTenant;
use App\Traits\TemUuid;
use Database\Factories\SolicitacaoCompraFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Notification;
use OwenIt\Auditing\Contracts\Auditable;
use RuntimeException;
use Spatie\Permission\PermissionRegistrar;

class SolicitacaoCompra extends Model implements Auditable
{
    use AuditsFillables, BelongsToTenant, TemUuid;

    /** @use HasFactory<SolicitacaoCompraFactory> */
    use HasFactory;

    protected $table = 'solicitacoes_compra';

    protected $fillable = ['descricao', 'valor', 'centro_custo_id'];

    protected $attributes = ['situacao' => 'rascunho'];

    protected function casts(): array
    {
        return ['valor' => 'decimal:2', 'situacao' => SituacaoSolicitacao::class];
    }

    protected static function booted(): void
    {
        static::updating(function (self $registro): void {
            $registro->exigirRascunhoPersistido('editar');
        });
        static::deleting(function (self $registro): void {
            $registro->exigirRascunhoPersistido('excluir');
        });
    }

    public function solicitante(): BelongsTo
    {
        return $this->belongsTo(User::class, 'solicitante_id');
    }

    public function centroCusto(): BelongsTo
    {
        return $this->belongsTo(CentroCusto::class, 'centro_custo_id');
    }

    public function etapas(): HasMany
    {
        return $this->hasMany(EtapaAprovacao::class, 'solicitacao_compra_id')->orderBy('created_at')->orderBy('id');
    }

    public function exigeDiretor(): bool
    {
        return (float) $this->valor > (float) config('kit.compras.limite_diretor', 5000.00);
    }

    public function etapaPendente(): ?string
    {
        return match ($this->situacao) {
            SituacaoSolicitacao::AguardandoGestor => 'gestor', SituacaoSolicitacao::AguardandoDiretor => 'diretor', default => null,
        };
    }

    public function podeSerDecididaPor(?User $user): bool
    {
        return $user !== null && $this->aprovadoresDaVez()->contains(fn (User $aprovador): bool => $aprovador->getKey() === $user->getKey());
    }

    public function aprovadoresDaVez(): Collection
    {
        if ($this->etapaPendente() === 'gestor') {
            $gestor = $this->centroCusto?->gestor;

            return collect($gestor ? [$gestor] : []);
        }
        if ($this->etapaPendente() !== 'diretor') {
            return collect();
        }
        $registrar = app(PermissionRegistrar::class);
        $anterior  = $registrar->getPermissionsTeamId();
        try {
            $registrar->setPermissionsTeamId($this->tenant_id ?? Tenant::CONTEXTO_GLOBAL);

            return User::role('diretor')->get();
        } finally {
            $registrar->setPermissionsTeamId($anterior);
        }
    }

    public function enviar(User $autor): void
    {
        $this->exigirSolicitante($autor, 'enviar');
        $this->exigirSituacao(SituacaoSolicitacao::Rascunho, 'enviar');
        if ($this->centroCusto?->gestor_id === null) {
            $this->recusar('enviar', 'centro_sem_gestor', 'O centro de custo precisa de um gestor para enviar.');
        }
        $this->transicionar(SituacaoSolicitacao::Rascunho, SituacaoSolicitacao::AguardandoGestor, 'enviar');
        $this->notificarProximaEtapa();
        Log::channel('compras')->info('[SolicitacaoCompra@enviar] Solicitação enviada para aprovação', ['solicitacao_id' => $this->id, 'tenant_id' => $this->tenant_id, 'solicitante_id' => $this->solicitante_id, 'centro_custo_id' => $this->centro_custo_id, 'valor' => $this->valor, 'exige_diretor' => $this->exigeDiretor(), 'de' => 'rascunho', 'para' => $this->situacao->value, 'aprovadores' => $this->aprovadoresDaVez()->pluck('id')->all()]);
    }

    public function aprovar(User $aprovador): void
    {
        $this->exigirAprovador($aprovador, 'aprovar');
        $etapa = $this->etapaPendente();
        $de    = $this->situacao;
        $para  = $etapa === 'gestor' && $this->exigeDiretor() ? SituacaoSolicitacao::AguardandoDiretor : SituacaoSolicitacao::Aprovada;
        DB::transaction(function () use ($de, $para, $etapa, $aprovador): void {
            $this->transicionar($de, $para, 'aprovar');
            $this->etapas()->create(['etapa' => $etapa, 'decisao' => 'aprovada', 'decidido_por_id' => $aprovador->getKey(), 'justificativa' => null]);
        });
        $this->notificarProximaEtapa();
        Log::channel('compras')->info('[SolicitacaoCompra@aprovar] Etapa aprovada', ['solicitacao_id' => $this->id, 'tenant_id' => $this->tenant_id, 'etapa' => $etapa, 'decidido_por_id' => $aprovador->id, 'de' => $de->value, 'para' => $para->value, 'final' => $para === SituacaoSolicitacao::Aprovada]);
    }

    public function rejeitar(User $aprovador, string $justificativa): void
    {
        $this->exigirAprovador($aprovador, 'rejeitar');
        if (blank($justificativa)) {
            $this->recusar('rejeitar', 'justificativa_vazia', 'Informe a justificativa da rejeição.');
        }
        $etapa = $this->etapaPendente();
        $de    = $this->situacao;
        DB::transaction(function () use ($de, $etapa, $aprovador, $justificativa): void {
            $this->transicionar($de, SituacaoSolicitacao::Rascunho, 'rejeitar');
            $this->etapas()->create(['etapa' => $etapa, 'decisao' => 'rejeitada', 'decidido_por_id' => $aprovador->getKey(), 'justificativa' => trim($justificativa)]);
        });
        Log::channel('compras')->warning('[SolicitacaoCompra@rejeitar] Solicitação devolvida ao rascunho', ['solicitacao_id' => $this->id, 'etapa' => $etapa, 'decidido_por_id' => $aprovador->id, 'justificativa_tamanho' => mb_strlen($justificativa), 'de' => $de->value, 'para' => 'rascunho']);
    }

    public function cancelar(User $autor): void
    {
        $this->exigirSolicitante($autor, 'cancelar');
        if (! $this->situacao->emTransito()) {
            $this->recusar('cancelar', 'situacao_invalida', 'Só é possível cancelar uma solicitação em aprovação.');
        }
        $de = $this->situacao;
        $this->transicionar($de, SituacaoSolicitacao::Cancelada, 'cancelar');
        Log::channel('compras')->warning('[SolicitacaoCompra@cancelar] Solicitação cancelada', ['solicitacao_id' => $this->id, 'autor_id' => $autor->id, 'de' => $de->value, 'para' => 'cancelada']);
    }

    public function editar(array $dados, User $autor): void
    {
        $this->exigirSolicitante($autor, 'editar');
        $this->exigirSituacao(SituacaoSolicitacao::Rascunho, 'editar');
        $this->fill($dados);
        $mudou = static::query()->whereKey($this->id)->where('solicitante_id', $autor->id)->where('situacao', 'rascunho')->update([...array_intersect_key($this->getDirty(), array_flip($this->getFillable())), 'updated_at' => now()]);
        if ($mudou !== 1) {
            $this->recusar('editar', 'situacao_mudou', 'Esta solicitação já mudou de situação. Recarregue a tela.');
        }
        $this->refresh();
    }

    public function excluir(User $autor): void
    {
        $this->exigirSolicitante($autor, 'excluir');
        $this->exigirSituacao(SituacaoSolicitacao::Rascunho, 'excluir');
        $excluiu = static::query()->whereKey($this->id)->where('solicitante_id', $autor->id)->where('situacao', 'rascunho')->delete();
        if ($excluiu !== 1) {
            $this->recusar('excluir', 'situacao_mudou', 'Esta solicitação já mudou de situação. Recarregue a tela.');
        }
        $this->exists = false;
    }

    private function transicionar(SituacaoSolicitacao $de, SituacaoSolicitacao $para, string $metodo): void
    {
        $mudou = static::query()->whereKey($this->id)->where('situacao', $de->value)->update(['situacao' => $para->value, 'updated_at' => now()]);
        if ($mudou !== 1) {
            $this->recusar($metodo, 'situacao_mudou', 'Esta solicitação já mudou de situação. Recarregue a tela.');
        }
        $this->refresh();
    }

    private function exigirRascunhoPersistido(string $metodo): void
    {
        $atual = $this->fresh();
        if ($atual === null) {
            $this->recusar($metodo, 'situacao_mudou', 'Esta solicitação não está disponível neste contexto.');
        }
        $atual->exigirSituacao(SituacaoSolicitacao::Rascunho, $metodo);
    }

    private function exigirSolicitante(User $autor, string $metodo): void
    {
        if ($this->solicitante_id !== $autor->getKey()) {
            $this->recusar($metodo, 'nao_e_solicitante', 'Somente o solicitante pode fazer esta operação.');
        }
    }

    private function exigirSituacao(SituacaoSolicitacao $esperada, string $metodo): void
    {
        if ($this->situacao !== $esperada) {
            $this->recusar($metodo, 'situacao_invalida', 'Esta operação não está disponível nesta situação.');
        }
    }

    private function exigirAprovador(User $aprovador, string $metodo): void
    {
        if (! $this->podeSerDecididaPor($aprovador)) {
            $this->recusar($metodo, 'nao_e_aprovador', 'Somente o aprovador da etapa atual pode decidir.');
        }
    }

    private function notificarProximaEtapa(): void
    {
        if (($etapa = $this->etapaPendente()) !== null) {
            Notification::send($this->aprovadoresDaVez(), new AprovacaoPendente($this, $etapa));
        }
    }

    private function recusar(string $metodo, string $motivo, string $mensagem): never
    {
        Log::channel('compras')->warning("[SolicitacaoCompra@{$metodo}] Operação recusada", ['solicitacao_id' => $this->id, 'tenant_id' => $this->tenant_id, 'motivo' => $motivo, 'situacao' => $this->situacao->value]);
        throw new RuntimeException($mensagem);
    }
}
