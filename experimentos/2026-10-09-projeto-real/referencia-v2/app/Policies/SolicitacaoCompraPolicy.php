<?php

declare(strict_types=1);

namespace App\Policies;

use App\Enums\SituacaoSolicitacao;
use App\Models\SolicitacaoCompra;
use Illuminate\Auth\Access\HandlesAuthorization;
use Illuminate\Foundation\Auth\User as AuthUser;

class SolicitacaoCompraPolicy
{
    use HandlesAuthorization;

    public function viewAny(AuthUser $authUser): bool
    {
        return $authUser->can('ViewAny:SolicitacaoCompra');
    }

    public function view(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('View:SolicitacaoCompra');
    }

    public function create(AuthUser $authUser): bool
    {
        return $authUser->can('Create:SolicitacaoCompra');
    }

    public function update(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('Update:SolicitacaoCompra')
            && $registro->situacao === SituacaoSolicitacao::Rascunho
            && $registro->solicitante_id === $authUser->getAuthIdentifier();
    }

    public function delete(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('Delete:SolicitacaoCompra')
            && $registro->situacao === SituacaoSolicitacao::Rascunho
            && $registro->solicitante_id === $authUser->getAuthIdentifier();
    }

    public function deleteAny(AuthUser $authUser): bool
    {
        return false;
    }

    public function restore(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('Restore:SolicitacaoCompra');
    }

    public function forceDelete(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('ForceDelete:SolicitacaoCompra');
    }

    public function forceDeleteAny(AuthUser $authUser): bool
    {
        return $authUser->can('ForceDeleteAny:SolicitacaoCompra');
    }

    public function restoreAny(AuthUser $authUser): bool
    {
        return $authUser->can('RestoreAny:SolicitacaoCompra');
    }

    public function replicate(AuthUser $authUser, SolicitacaoCompra $registro): bool
    {
        return $authUser->can('Replicate:SolicitacaoCompra');
    }

    public function reorder(AuthUser $authUser): bool
    {
        return $authUser->can('Reorder:SolicitacaoCompra');
    }
}
