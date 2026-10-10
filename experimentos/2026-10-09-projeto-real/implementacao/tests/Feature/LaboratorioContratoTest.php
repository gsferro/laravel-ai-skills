<?php

use App\Enums\SituacaoSolicitacao;
use App\Filament\App\Resources\CentrosCusto\Pages\CreateCentroCusto;
use App\Filament\App\Resources\Cupons\Pages\CreateCupom;
use App\Filament\App\Resources\Cupons\Pages\ListCupons;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\CreateSolicitacaoCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\EditSolicitacaoCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\ListSolicitacoesCompra;
use App\Filament\App\Resources\SolicitacoesCompra\Pages\ViewSolicitacaoCompra;
use App\Models\CentroCusto;
use App\Models\Cupom;
use App\Models\CupomUso;
use App\Models\SolicitacaoCompra;
use App\Models\Tenant;
use App\Models\User;
use App\Notifications\AprovacaoPendente;
use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Filament\Actions\Testing\TestAction;
use Filament\Facades\Filament;
use Illuminate\Support\Facades\Notification;
use Livewire\Livewire;
use Spatie\Permission\Models\Permission;

beforeEach(function (): void {
    Filament::setTenant(null, isQuiet: true);
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    expect(Permission::query()->where('name', 'Create:SolicitacaoCompra')->exists())->toBeTrue();
    $this->organizacao = Tenant::factory()->create();
    noPainelDa($this->organizacao);
    Notification::fake();
});

it('consome percentual truncado e registra ator horario e valores sem exceder o limite', function (): void {
    $ator  = User::factory()->create();
    $cupom = Cupom::factory()->create(['codigo' => ' bemvindo ', 'limite_de_usos' => 1]);
    $copia = Cupom::query()->findOrFail($cupom->id);
    expect(Cupom::valido('bemvindo')?->id)->toBe($cupom->id)
        ->and($cupom->aplicarEm(9999, $ator))->toBe(9000)
        ->and($cupom->fresh()->usos)->toBe(1);
    $uso = CupomUso::query()->sole();
    expect($uso->aplicado_por_id)->toBe($ator->id)->and($uso->valor_original)->toBe(9999)->and($uso->valor_desconto)->toBe(999)->and($uso->created_at)->not->toBeNull();
    expect(fn () => $copia->aplicarEm(9999, $ator))->toThrow(RuntimeException::class);
    expect(CupomUso::query()->count())->toBe(1)->and(Cupom::valido('BEMVINDO'))->toBeNull();
});

it('limita o total em zero e recusa cupons fora da validade', function (): void {
    expect(Cupom::factory()->fixo(5000)->create()->aplicarEm(3000))->toBe(0);
    $expirado = Cupom::factory()->expirado()->create();
    expect(Cupom::valido($expirado->codigo))->toBeNull()->and(Cupom::valido('INEXISTENTE'))->toBeNull();
    expect(fn () => $expirado->aplicarEm(10000))->toThrow(RuntimeException::class);
    expect(fn () => Cupom::factory()->create()->aplicarEm(-1))->toThrow(InvalidArgumentException::class);
});

it('segue gestor e diretor acima do limite preservando ambas identidades no historico', function (): void {
    $gestor      = User::factory()->create(['name' => 'Gestor do contrato']);
    $diretor     = usuarioCom('diretor');
    $centro      = CentroCusto::factory()->create(['gestor_id' => $gestor->id]);
    $solicitacao = SolicitacaoCompra::factory()->create(['centro_custo_id' => $centro->id, 'valor' => '5000.01']);
    $solicitacao->enviar($solicitacao->solicitante);
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::AguardandoGestor);
    Notification::assertSentTo($gestor, AprovacaoPendente::class, fn (AprovacaoPendente $notificacao): bool => $notificacao->etapa === 'gestor');
    $solicitacao->aprovar($gestor);
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::AguardandoDiretor);
    Notification::assertSentTo($diretor, AprovacaoPendente::class, fn (AprovacaoPendente $notificacao): bool => $notificacao->etapa === 'diretor');
    $solicitacao->aprovar($diretor);
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::Aprovada)->and($solicitacao->etapas()->pluck('decidido_por_id')->all())->toBe([$gestor->id, $diretor->id]);
    expect(fn () => $solicitacao->editar(['descricao' => 'Alterada'], $solicitacao->solicitante))->toThrow(RuntimeException::class);
    expect(fn () => $solicitacao->delete())->toThrow(RuntimeException::class);
    expect(fn () => $solicitacao->update(['descricao' => 'Alterada']))->toThrow(RuntimeException::class);
    noPainelDa(Tenant::factory()->create());
    expect(fn () => $solicitacao->update(['descricao' => 'Fora do contexto']))->toThrow(RuntimeException::class);
});

it('aprova no gestor no limite exato e exige justificativa antes de retornar ao rascunho', function (): void {
    $solicitacao = SolicitacaoCompra::factory()->create(['valor' => '5000.00']);
    $autor       = $solicitacao->solicitante;
    $gestor      = $solicitacao->centroCusto->gestor;
    $solicitacao->enviar($autor);
    expect(fn () => $solicitacao->rejeitar($gestor, '  '))->toThrow(RuntimeException::class);
    $solicitacao->rejeitar($gestor, 'Sem verba');
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::Rascunho);
    $solicitacao->editar(['descricao' => 'Correção feita'], $autor);
    $solicitacao->enviar($autor);
    $solicitacao->aprovar($gestor);
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::Aprovada)->and($solicitacao->etapas()->pluck('decisao')->all())->toBe(['rejeitada', 'aprovada']);
});

it('recusa pessoa errada e falta de gestor sem mudar o rascunho e cancela somente antes do final', function (): void {
    $solicitacao = SolicitacaoCompra::factory()->create();
    expect(fn () => $solicitacao->enviar(User::factory()->create()))->toThrow(RuntimeException::class);
    $centro    = CentroCusto::factory()->create(['gestor_id' => null]);
    $semGestor = SolicitacaoCompra::factory()->create(['centro_custo_id' => $centro->id]);
    expect(fn () => $semGestor->enviar($semGestor->solicitante))->toThrow(RuntimeException::class);
    expect($semGestor->fresh()->situacao)->toBe(SituacaoSolicitacao::Rascunho);
    $solicitacao->enviar($solicitacao->solicitante);
    expect(fn () => $solicitacao->aprovar(User::factory()->create()))->toThrow(RuntimeException::class);
    $solicitacao->cancelar($solicitacao->solicitante);
    expect($solicitacao->situacao)->toBe(SituacaoSolicitacao::Cancelada)->and($solicitacao->etapas()->count())->toBe(0);
});

it('grava cupom e centro pela tela e mantem o usuario comum somente na leitura ativa', function (): void {
    $admin  = usuarioCom('master_global');
    $gestor = User::factory()->create();
    $this->organizacao->users()->attach([$admin->id, $gestor->id]);
    $this->actingAs($admin);
    Livewire::test(CreateCupom::class)->fillForm(['codigo' => ' tela10 ', 'tipo' => 'porcentagem', 'valor' => 10, 'expira_em' => now()->addDay()->format('Y-m-d H:i:s'), 'limite_de_usos' => 10])->call('create')->assertHasNoFormErrors();
    $cupom = Cupom::query()->where('codigo', 'TELA10')->sole();
    Livewire::test(CreateCentroCusto::class)->fillForm(['nome' => 'Engenharia', 'gestor_id' => $gestor->id])->call('create')->assertHasNoFormErrors();
    expect(CentroCusto::query()->where('nome', 'Engenharia')->sole()->gestor_id)->toBe($gestor->id);
    $comum = usuarioCom('panel_user');
    $this->actingAs($comum);
    expect($comum->can('ViewAny:Cupom'))->toBeTrue()->and($comum->can('Create:Cupom'))->toBeFalse()->and($comum->can('Update:CentroCusto'))->toBeFalse()->and($comum->can('Create:SolicitacaoCompra'))->toBeTrue();
    $expirado = Cupom::factory()->expirado()->create();
    Livewire::test(ListCupons::class)->call('loadTable')->assertCanSeeTableRecords([$cupom])->assertCanNotSeeTableRecords([$expirado]);
});

it('grava e edita solicitacao pela tela e a acao envia com status e historico visiveis', function (): void {
    $solicitante = usuarioCom('panel_user');
    $gestor      = User::factory()->create(['name' => 'Gestor da tela']);
    $this->organizacao->users()->attach([$solicitante->id, $gestor->id]);
    $centro = CentroCusto::factory()->create(['gestor_id' => $gestor->id]);
    $this->actingAs($solicitante);
    Livewire::test(CreateSolicitacaoCompra::class)->fillForm(['descricao' => 'Compra pela tela', 'valor' => '100.00', 'centro_custo_id' => $centro->id])->call('create')->assertHasNoFormErrors();
    $solicitacao = SolicitacaoCompra::query()->where('descricao', 'Compra pela tela')->sole();
    expect($solicitacao->solicitante_id)->toBe($solicitante->id)->and($solicitacao->situacao)->toBe(SituacaoSolicitacao::Rascunho);
    Livewire::test(EditSolicitacaoCompra::class, ['record' => $solicitacao->uuid])->fillForm(['descricao' => 'Compra corrigida'])->call('save')->assertHasNoFormErrors();
    Livewire::test(ListSolicitacoesCompra::class)->callAction(TestAction::make('enviar')->table($solicitacao))->assertNotified();
    expect($solicitacao->fresh()->situacao)->toBe(SituacaoSolicitacao::AguardandoGestor);
    $solicitacao->refresh()->aprovar($gestor);
    Livewire::test(ViewSolicitacaoCompra::class, ['record' => $solicitacao->uuid])->assertSee('Aprovada')->assertSee('Gestor da tela');
});
