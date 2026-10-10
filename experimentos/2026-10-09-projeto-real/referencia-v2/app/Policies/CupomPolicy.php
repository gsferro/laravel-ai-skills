<?php

declare(strict_types=1);

namespace App\Policies;

use App\Models\Cupom;
use Illuminate\Auth\Access\HandlesAuthorization;
use Illuminate\Foundation\Auth\User as AuthUser;

class CupomPolicy
{
    use HandlesAuthorization;

    public function viewAny(AuthUser $authUser): bool
    {
        return $authUser->can('ViewAny:Cupom');
    }

    public function view(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('View:Cupom');
    }

    public function create(AuthUser $authUser): bool
    {
        return $authUser->can('Create:Cupom');
    }

    public function update(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('Update:Cupom');
    }

    public function delete(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('Delete:Cupom');
    }

    public function deleteAny(AuthUser $authUser): bool
    {
        return $authUser->can('DeleteAny:Cupom');
    }

    public function restore(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('Restore:Cupom');
    }

    public function forceDelete(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('ForceDelete:Cupom');
    }

    public function forceDeleteAny(AuthUser $authUser): bool
    {
        return $authUser->can('ForceDeleteAny:Cupom');
    }

    public function restoreAny(AuthUser $authUser): bool
    {
        return $authUser->can('RestoreAny:Cupom');
    }

    public function replicate(AuthUser $authUser, Cupom $registro): bool
    {
        return $authUser->can('Replicate:Cupom');
    }

    public function reorder(AuthUser $authUser): bool
    {
        return $authUser->can('Reorder:Cupom');
    }
}
