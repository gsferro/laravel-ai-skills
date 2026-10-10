<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('cupom_usos', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('cupom_id')->constrained('cupons')->cascadeOnDelete();
            $table->foreignId('aplicado_por_id')->nullable()->constrained('users')->nullOnDelete();
            $table->unsignedInteger('valor_original');
            $table->unsignedInteger('valor_desconto');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('cupom_usos');
    }
};
