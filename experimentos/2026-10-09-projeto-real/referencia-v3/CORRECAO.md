# Correção da referência v3

Data: 2026-10-09. Escopo: unidade e limite do valor no formulário de cupom.

Requisito: P-05 do `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md:165` define valor fixo em centavos e percentual inteiro entre 1 e 100, conforme o tipo. O formulário deve comunicar essa unidade e aplicar seu limite correspondente.

Causa confirmada por leitura do vendor instalado:

- `vendor/filament/forms/src/Components/Concerns/HasOptions.php:24`: `options(TipoDeDesconto::class)` registra a classe como enum do campo.
- `vendor/filament/forms/src/Components/Select.php:1709` e `vendor/filament/forms/src/Components/Field.php:105`: o select instala `EnumStateCast` nos casts de estado.
- `vendor/filament/schemas/src/Components/Utilities/Get.php:45`: o Get devolve `component->getState()` quando encontra o campo.
- `vendor/filament/schemas/src/Components/Concerns/HasState.php:946` e `vendor/filament/schemas/src/Components/StateCasts/EnumStateCast.php:17`: o valor escalar `fixo` ou `porcentagem` é convertido para um caso de enum.
- Os dois callbacks em `CupomResource::form()` comparavam esse objeto enum com `Fixo->value` ou `Porcentagem->value`, strings. Ambas as comparações estritas eram falsas: o label permanecia percentual e o teto de 100 não era aplicado ao percentual.

Patch: somente `app/Filament/App/Resources/Cupons/CupomResource.php`. Ambos os callbacks usam `Get::enum('tipo', TipoDeDesconto::class)` e comparam casos de enum. O helper oficial, definido em `Get.php:161`, aceita tanto enum já convertido quanto seu valor escalar. Não há alteração de opções, transporte Livewire, unidade armazenada, API de aplicação ou expectativas dos controles próprios.

Validação desta correção: revisão textual da cadeia de chamadas e dos dois callbacks. Nenhuma aplicação, Pest, Artisan ou browser foi executado, conforme coordenação serial da root. A observação DOM comunicada pela root é compatível com essa causa, mas não substitui a execução pós-patch. A v3 ainda precisa comprovar a troca visual entre os dois labels e o limite percentual no formulário real. A data ISO não foi investigada nem alterada nesta correção.

Cobertura própria existente: o controle Livewire cria cupom percentual com valor 10; o smoke browser verifica listagem e histórico. Esses controles não afirmam a unidade dinâmica do label nem a rejeição de percentual acima de 100. Nenhuma nova expectativa foi incorporada, e nenhum teste comparativo foi consultado.

Limites: leitura restrita à implementação própria pertinente, enum próprio, 00 de cupons e fontes Filament instaladas. Nenhum conjunto, catálogo, especificação derivada, veredito ou resultado comparativo foi consultado. Vendor, ambiente, configurações, arnês e testes foram preservados. O filesystem é irrestrito; a seleção explícita de caminhos não constitui prova de isolamento técnico.
