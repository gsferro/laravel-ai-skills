<?php

use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Support\Carbon;

pest()->browser()->inChrome();

beforeEach(function () {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $acme = tenant('Acme', 'acme');
    $administradora = usuarioComPapel('admin_organizacao', $acme, 'browser-k7@example.test');
    $acme->users()->attach($administradora->id);
    noPainelDa($acme);
    $this->actingAs($administradora);
    $this->travelTo(Carbon::parse('2026-10-09T12:00:00Z'));
});

afterEach(function () {
    $this->travelBack();
});

// CT parcial: seleção real e unidade no DOM; a âncora de gravação não foi traduzida.
it('CT-B01 [K7] Chromium troca tipo e mostra a nova unidade sem reload; gravação omitida', function (string $inicial, string $final) {
    $unidade = static function (string $tipo): string {
        $esperada = $tipo === 'fixo' ? 'centavos' : 'percentual';

        return str_replace('__UNIDADE__', $esperada, <<<'JS'
function () {
    const campo = document.querySelector('input[id$=".valor"]');
    if (!campo) return false;
    const visivel = elemento => elemento.getClientRects().length > 0
        && getComputedStyle(elemento).display !== 'none'
        && getComputedStyle(elemento).visibility !== 'hidden';
    const labels = Array.from(document.querySelectorAll('label'))
        .filter(label => label.htmlFor === campo.id && visivel(label));
    const texto = labels.map(label => label.innerText).join(' ').toLowerCase();
    const centavos = /centavo/.test(texto);
    const percentual = /%|porcent|percentual/.test(texto);
    return visivel(campo) && ('__UNIDADE__' === 'centavos'
        ? centavos && !percentual : percentual && !centavos);
}
JS);
    };

    visit('/app/acme/cupons/create')
        ->assertPathIs('/app/acme/cupons/create')
        ->select('select[id$=".tipo"]', $inicial)
        ->assertScript($unidade($inicial), true)
        ->select('select[id$=".tipo"]', $final)
        ->assertScript($unidade($final), true)
        ->assertNoJavaScriptErrors();
})->with([
    'porcentagem para fixo / unidade centavos' => ['porcentagem', 'fixo'],
    'fixo para porcentagem / unidade pontos percentuais' => ['fixo', 'porcentagem'],
]);
