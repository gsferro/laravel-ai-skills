<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('cupons', function (Blueprint $table): void {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->foreignId('tenant_id')->nullable()->constrained()->cascadeOnDelete();
            $table->string('codigo', 40);
            $table->string('tipo', 20);
            $table->unsignedInteger('valor');
            $table->timestamp('expira_em');
            $table->unsignedInteger('limite_de_usos');
            $table->unsignedInteger('usos')->default(0);
            $table->timestamps();
            // shortcut: NULL tenant_id não impõe unicidade em singletenant; revisar ao aceitar criação concorrente fora do formulário.
            $table->unique(['tenant_id', 'codigo']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('cupons');
    }
};
