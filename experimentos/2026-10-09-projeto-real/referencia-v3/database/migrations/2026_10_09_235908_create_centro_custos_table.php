<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('centros_custo', function (Blueprint $table): void {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->foreignId('tenant_id')->constrained();
            $table->string('nome', 120);
            $table->foreignId('gestor_id')->nullable()->constrained('users');
            $table->timestamps();
            $table->unique(['tenant_id', 'nome']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('centros_custo');
    }
};
