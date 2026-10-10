<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('solicitacoes_compra', function (Blueprint $table): void {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->foreignId('tenant_id')->constrained();
            $table->foreignId('solicitante_id')->constrained('users');
            $table->foreignId('centro_custo_id')->constrained('centros_custo');
            $table->string('descricao', 255);
            $table->decimal('valor', 12, 2);
            $table->string('situacao', 30);
            $table->timestamps();
            $table->index(['tenant_id', 'situacao']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('solicitacoes_compra');
    }
};
