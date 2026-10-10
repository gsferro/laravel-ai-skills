<?php

use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Support\Carbon;

pest()->browser()->inChrome();

beforeEach(function () {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $acme = tenant('Acme', 'acme');
    $ana = usuarioComPapel('admin_organizacao', $acme, 'browser-m4@example.test');
    $acme->users()->attach($ana->id);
    noPainelDa($acme);
    $this->actingAs($ana);
    $this->travelTo(Carbon::parse('2026-10-09T12:00:00Z'));
});

afterEach(function () {
    $this->travelBack();
});

// CT parcial: unidade/operabilidade antes do submit; NOVO fixo/150 não é gravado aqui.
it('CT-B01 [M4] Chromium seleciona fixo e mostra centavos com campo operável; gravação omitida', function () {
    $pagina = visit('/app/acme/cupons/create')->assertPathIs('/app/acme/cupons/create');
    $pagina->select('select[id$=".tipo"]', 'porcentagem')->assertScript(<<<'JS'
function () {
    const valor = document.querySelector('input[id$=".valor"]');
    if (!valor) return false;
    const labels = Array.from(document.querySelectorAll('label')).filter(label => label.htmlFor === valor.id);
    const visiveis = labels.filter(label => label.getClientRects().length > 0
        && getComputedStyle(label).display !== 'none'
        && getComputedStyle(label).visibility !== 'hidden');
    const texto = visiveis.map(label => label.innerText).join(' ').toLowerCase();
    return /%|porcent|percentual/.test(texto) && !/centavo/.test(texto);
}
JS, true);

    $pagina->select('select[id$=".tipo"]', 'fixo')->assertScript(<<<'JS'
function () {
    const valor = document.querySelector('input[id$=".valor"]');
    if (!valor) return false;
    const labels = Array.from(document.querySelectorAll('label')).filter(label => label.htmlFor === valor.id);
    const visiveis = labels.filter(label => label.getClientRects().length > 0
        && getComputedStyle(label).display !== 'none'
        && getComputedStyle(label).visibility !== 'hidden');
    const texto = visiveis.map(label => label.innerText).join(' ').toLowerCase();
    return /centavo/.test(texto) && !/%|porcent|percentual/.test(texto)
        && valor.getClientRects().length > 0
        && getComputedStyle(valor).display !== 'none'
        && getComputedStyle(valor).visibility !== 'hidden'
        && !valor.disabled && !valor.readOnly;
}
JS, true)->assertNoJavaScriptErrors();
});
