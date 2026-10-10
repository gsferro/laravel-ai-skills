# Controle suplementar do teto percentual da referência v3

Origem exclusiva do comportamento: P-05 de `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md:165`, que define percentual inteiro de 1 a 100. O controle usa a fronteira superior válida 100 e seu vizinho inválido 101.

Arquivo novo: `tests/ExperimentoReal/ControleReferencia/CupomEnumTest.php`. Um único teste de formulário, sem alterar os 42 arquivos da referência v3, o registro Pest ou qualquer arnês.

Fixture: seeds Shield/Papeis da implementação própria, tenant real, administrador da organização atribuído pelo helper `usuarioComPapel`, associação ao tenant e `noPainelDa`. A permissão de criação é afirmada. O prefixo ExperimentoReal já está registrado em `tests/Pest.php` com `TenancyTestCase` e `RefreshDatabase` antes das migrations.

Asserções: com código, tipo, validade futura e limite de usos válidos, 101 exige erro da regra `max` especificamente em `valor`, ausência de erros nos demais campos e zero cupons persistidos. Os mesmos dados com 100 exigem ausência de erros e um único cupom com valor inteiro 100, tipo enum Porcentagem, usos zero, código exato e tenant correto. Os nomes das APIs `fillForm`, `assertHasFormErrors` e `assertHasNoFormErrors` foram conferidos em `vendor/filament/forms/src/Testing/TestsForms.php`; a regra identificada é verificada pelo suporte de validação instalado do Livewire.

Limites: nenhuma execução PHP, aplicação, Pest, Artisan ou browser foi feita nesta entrega; a root executará serialmente após restaurar e congelar a fonte. Este controle não prova a mudança visual do label, outras fronteiras percentuais ou valor fixo. Não é CT de um braço nem medição DDR. Nenhum catálogo, conjunto, CT derivado, veredito, log ou resultado comparativo foi lido. A fonte Resource e os models em mutação não foram lidos. Apenas 00, controles próprios, fixture própria, tests/Pest e vendor pertinente foram consultados. Restrições de leitura por seleção explícita de caminhos, sem isolamento técnico do filesystem.
