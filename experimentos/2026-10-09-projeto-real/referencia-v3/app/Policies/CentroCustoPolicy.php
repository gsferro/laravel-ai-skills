<?php

declare(strict_types=1);

namespace App\Policies;

use App\Models\CentroCusto;
use Illuminate\Auth\Access\HandlesAuthorization;
use Illuminate\Foundation\Auth\User as AuthUser;

class CentroCustoPolicy
{
    use HandlesAuthorization;

    public function viewAny(AuthUser $authUser): bool
    {
        return $authUser->can('ViewAny:CentroCusto');
    }

    public function view(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('View:CentroCusto');
    }

    public function create(AuthUser $authUser): bool
    {
        return $authUser->can('Create:CentroCusto');
    }

    public function update(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('Update:CentroCusto');
    }

    public function delete(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('Delete:CentroCusto');
    }

    public function deleteAny(AuthUser $authUser): bool
    {
        return $authUser->can('DeleteAny:CentroCusto');
    }

    public function restore(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('Restore:CentroCusto');
    }

    public function forceDelete(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('ForceDelete:CentroCusto');
    }

    public function forceDeleteAny(AuthUser $authUser): bool
    {
        return $authUser->can('ForceDeleteAny:CentroCusto');
    }

    public function restoreAny(AuthUser $authUser): bool
    {
        return $authUser->can('RestoreAny:CentroCusto');
    }

    public function replicate(AuthUser $authUser, CentroCusto $registro): bool
    {
        return $authUser->can('Replicate:CentroCusto');
    }

    public function reorder(AuthUser $authUser): bool
    {
        return $authUser->can('Reorder:CentroCusto');
    }
}
