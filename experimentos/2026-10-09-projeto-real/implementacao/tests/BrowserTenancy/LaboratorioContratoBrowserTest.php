<?php

use App\Models\CentroCusto;
use App\Models\Cupom;
use App\Models\SolicitacaoCompra;
use App\Models\Tenant;
use App\Models\User;
use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Support\Facades\Notification;

it('renderiza cupons ativos e o historico com quem aprovou em Chromium real', function (): void {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $tenant      = Tenant::factory()->create();
    $solicitante = usuarioComPapel('panel_user', $tenant);
    $gestor      = User::factory()->create(['name' => 'Gestor visível no histórico']);
    $tenant->users()->attach([$solicitante->id, $gestor->id]);
    noPainelDa($tenant);
    Cupom::factory()->create(['codigo' => 'CUPOMVISIVEL']);
    Cupom::factory()->expirado()->create(['codigo' => 'CUPOMEXPIRADO']);
    $centro      = CentroCusto::factory()->create(['gestor_id' => $gestor->id]);
    $solicitacao = SolicitacaoCompra::factory()->create(['solicitante_id' => $solicitante->id, 'centro_custo_id' => $centro->id]);
    Notification::fake();
    $solicitacao->enviar($solicitante);
    $solicitacao->aprovar($gestor);
    $this->actingAs($solicitante);
    $cupons = '/app/'.$tenant->slug.'/cupons';
    visit($cupons)->assertPathIs($cupons)->assertSee('CUPOMVISIVEL')->assertDontSee('CUPOMEXPIRADO')->assertNoJavaScriptErrors();
    $historico = '/app/'.$tenant->slug.'/solicitacoes-de-compra/'.$solicitacao->uuid;
    visit($historico)->assertPathIs($historico)->assertSee('Aprovada')->assertSee('Gestor visível no histórico')->assertNoJavaScriptErrors();
});
