<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('etapas_aprovacao_compra', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('solicitacao_compra_id')->constrained('solicitacoes_compra')->cascadeOnDelete();
            $table->string('etapa', 20);
            $table->string('decisao', 20);
            $table->foreignId('decidido_por_id')->constrained('users');
            $table->text('justificativa')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('etapas_aprovacao_compra');
    }
};
