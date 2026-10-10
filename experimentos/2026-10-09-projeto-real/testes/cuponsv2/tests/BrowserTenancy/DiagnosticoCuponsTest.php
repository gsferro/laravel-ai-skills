<?php

use Database\Seeders\PapeisSeeder;
use Database\Seeders\ShieldPermissionsSeeder;
use Illuminate\Support\Carbon;

pest()->browser()->inChrome();

beforeEach(function () {
    $this->seed([ShieldPermissionsSeeder::class, PapeisSeeder::class]);
    $acme = tenant('Acme', 'acme');
    $administradora = usuarioComPapel('admin_organizacao', $acme, 'diagnostico-cupons@example.test');
    $acme->users()->attach($administradora->id);
    noPainelDa($acme);
    $this->actingAs($administradora);
    $this->travelTo(Carbon::parse('2026-10-09T12:00:00Z'));
});

afterEach(function () {
    $this->travelBack();
});

// Instrumentação separada: não é CT comparativo nem prova de unidade/cobertura.
it('probe DOM do campo valor depois de selecionar fixo em Chromium', function () {
    $snapshot = <<<'JS'
function () {
    const tipo = document.querySelector('select[id$=".tipo"]');
    const valor = document.querySelector('input[id$=".valor"]');
    const visivel = elemento => elemento !== null
        && elemento.getClientRects().length > 0
        && getComputedStyle(elemento).display !== 'none'
        && getComputedStyle(elemento).visibility !== 'hidden';
    const atributos = elemento => elemento
        ? Object.fromEntries(Array.from(elemento.attributes, atributo => [atributo.name, atributo.value]))
        : null;
    const wrapper = valor?.closest('[data-field-wrapper]') ?? valor?.closest('.fi-fo-field') ?? valor?.parentElement;
    const labels = valor ? Array.from(document.querySelectorAll('label'))
        .filter(label => label.htmlFor === valor.id)
        .map(label => ({texto: label.innerText, textoDOM: label.textContent, visivel: visivel(label), html: label.outerHTML})) : [];
    return {
        path: window.location.pathname,
        select: tipo ? {id: tipo.id, value: tipo.value, visivel: visivel(tipo), atributos: atributos(tipo), html: tipo.outerHTML} : null,
        valor: valor ? {id: valor.id, visivel: visivel(valor), disabled: valor.disabled, readOnly: valor.readOnly, atributos: atributos(valor)} : null,
        labels,
        wrapper: wrapper ? {textoVisivel: wrapper.innerText, html: wrapper.outerHTML} : null
    };
}
JS;
    $pagina = null;
    $relatorio = [];
    try {
        $pagina = visit('/app/acme/cupons/create');
        $pagina->assertPathIs('/app/acme/cupons/create');
        $pagina->select('select[id$=".tipo"]', 'porcentagem');
        $relatorio['porcentagem_apos_select'] = $pagina->script($snapshot);
        $pagina->select('select[id$=".tipo"]', 'fixo');
        $relatorio['fixo_apos_select'] = $pagina->script($snapshot);
        $pagina->waitForEvent('networkidle');
        $relatorio['fixo_apos_networkidle'] = $pagina->script($snapshot);
    } catch (Throwable $erro) {
        $relatorio['falha_do_probe'] = ['classe' => $erro::class, 'mensagem' => $erro->getMessage()];
        throw $erro;
    } finally {
        if ($pagina !== null) {
            foreach ([
                'snapshot_final' => fn () => $pagina->script($snapshot),
                'javascript_errors' => fn () => $pagina->page()->javaScriptErrors(),
                'console_logs' => fn () => $pagina->page()->consoleLogs(),
            ] as $chave => $coletar) {
                try {
                    $relatorio[$chave] = $coletar();
                } catch (Throwable $erroDeColeta) {
                    $relatorio['falhas_de_coleta'][$chave] = [
                        'classe' => $erroDeColeta::class,
                        'mensagem' => $erroDeColeta->getMessage(),
                    ];
                }
            }
        }
        $json = json_encode($relatorio, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE | JSON_PARTIAL_OUTPUT_ON_ERROR);
        fwrite(STDERR, 'CUPOM_DOM_PROBE '.($json === false ? '{"falha_serializacao":true}' : $json).PHP_EOL);
    }
})->group('diagnostico-cupons');
