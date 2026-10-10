# Materialização de cupons — M4

Primeira tradução, **sem execução**, preparada para congelamento pela sessão orquestradora. Status integral/parcial = tradução dos observáveis e Examples, nunca resultado verde. Executor: família GPT-6; esforço ultra solicitado; deployment exato não exposto.

## Entradas e restrições efetivas

- Domínio: somente `judges/conjunto-m4/conjunto.md`, lido integralmente. Saída anônima; nenhuma identidade de versão foi recebida.
- `runtime/contrato-publico.md` usado somente para nomes de classes/APIs, schema e fixtures. Não foi usado como critério de negócio, inclusive nos parâmetros opcionais do motor.
- Técnica: `tests/Pest.php`, `tests/TestCase.php`, `tests/TenancyTestCase.php`, `phpunit.xml` e vendor instalado de Laravel, Filament e pest-plugin-browser. Não foram abertos código da feature, testes do implementador, logs, catálogos, vereditos, prompts de juiz, requisitos/planos externos ou repositório de skills.
- Filesystem irrestrito e shell `login:false`; cegamento por contrato, sem sandbox mecânico/whitelist. Prompt ou ausência de edições não demonstram isolamento de leitura.
- Arnês existente `TenancyTestCase` + `RefreshDatabase`; não alterados aplicação/Pest.php. Artefatos próprios: `tests/ExperimentoReal/M4/CuponsTest.php`, `tests/BrowserTenancy/ComparacaoM4Test.php` e este mapa.
- Zero Artisan, Pest, browser, servidor, build ou mutation testing. As previsões internas da entrada integral não são operadores executados; nenhum operador real foi recebido/antecipado. Não há DDR, tokens, equivalência de host ou mortes medidos.

## Mecanismos e limites

Backend chama o motor real com ator explícito e consulta banco real. Ana autenticada/contextualizada cria as fixtures válidas; Beto é outro usuário real da mesma organização. Os dados de história são aplicações reais. O legado usos4/limite3 é preparado após a história real com `forceFill(...)->saveQuietly()`; isso não afirma aceite da redução de limite no cadastro/edição. Seeders, papéis, membership e tenancy usam as APIs existentes. Relógio volta em `afterEach`.

A recusa é chamada sem retorno aceito, com exceção e conservação dos efeitos literais. Nenhuma mensagem ou classe de exceção de negócio foi escolhida. `Error`/`QueryException` são relançadas para não registrar falha técnica como recusa; demais exceções ainda exigem classificação do executor. CT-41 admite também `TypeError` para a recusa do argumento null, sem exigir esse mecanismo. A pessoa de controle é Beto autenticado, e o argumento passado ao motor é literalmente null. O teste não substitui esse argumento pelo guard nem inventa um requisito de ator opcional.

Browser configura Chrome/Chromium via API instalada `inChrome`, faz `select` real e usa `assertScript` sobre labels associados por `htmlFor`, com retângulo e estilos visíveis. Propostas de seletores: `select[id$=".tipo"]` e `input[id$=".valor"]`, baseadas em state path do vendor e nomes públicos. Native select/IDs finais não foram conferidos: ausência exige classificar bloqueio técnico e ajustar somente mecanismo, sem editar o esperado. Não há reload entre seleções, `wait` fixo, fake de JS ou servidor externo. Persistência do CT-B foi omitida antes do congelamento porque submit e destino finais não foram conferidos.

## CT → testes e literais traduzidos

Arquivo backend: `tests/ExperimentoReal/M4/CuponsTest.php`; nomes usam CT original e `[M4]`.

| CT | Teste / status da tradução | Literal traduzido | Omitido |
|---|---|---|---|
| CT-10 | percentual conserva o inteiro de centavos do Example — integral | retorno exatamente o inteiro final de cada linha | nenhum observável do CT; não acrescentados contador/trilha |
| CT-11 | borda de meio centavo mantém desconto efetivo de dois centavos — integral | desconto efetivo2 e retorno final dos três Examples | nenhum observável do CT; não acrescentados contador/trilha |
| CT-12 | fixo de mil centavos conserva o piso do total — integral | retorno inteiro exatamente final em999/1000/1001 | nenhum observável do CT; não acrescentados contador/trilha |
| CT-13 | segundo exato da expiração recusa e segundo anterior aceita — integral | resultado/9000 quando aceito; contador e trilhas; recusa sem retorno e história idêntica | nenhum observável do CT no modo tenancy |
| CT-22 | último uso aceita e limite atingido ou ultrapassado recusa — integral | retorno9000 quando aceito, contador e trilhas dos Examples; recusa sem retorno e conservação exata de linhas anteriores | nenhum observável do CT no modo tenancy |
| CT-26 | motor registra Beto e o instante sem atribuir a Ana ou autor nulo — integral | retorno9000, contador1, exatamente uma linha cupom/Beto no instante18:00Z; nenhuma autoria Ana/nula | nenhum observável do CT |
| CT-28 | aplicação de Carla acrescenta só sua linha e preserva Beto — integral | retorno9000, contador2; exatamente Beto/18:00Z e Carla/18:00:01Z; primeira linha idêntica e nenhuma terceira | nenhum observável do CT |
| CT-41 | pessoa aplicadora nula recusa sem consumir nem criar trilha — integral | null recusado sem retorno descontado, contador0 e zero nova linha | nenhum observável do CT |
| CT-07 | seleção posterior ao julgamento recusa criação por componente de fixo negativo — parcial, seleção exploratória posterior | criação fixo−1 pelo componente recusada; nenhum cupom ou uso criado | os outros9 Examples não traduzidos |
| CT-B01 | `tests/BrowserTenancy/ComparacaoM4Test.php`: Chromium seleciona fixo e mostra centavos com campo operável; gravação omitida — parcial | porcentagem inicial explícita com unidade visível; troca real para fixo sem reload; centavos visíveis sem percentual e input visível/habilitado/digitável | enviar valor150, validade e limite3; existência exata de NOVO na Acme fixo150/contador0; destino depois de criar |

DOM admite semântica percentual por `%`/porcentagem/percentual, e centavos por texto associado, sem exigir uma frase do plano. Console é somente apoio. Os literais de efeitos de CT-26/28 não foram transportados para CT-10/11/12.

## Examples selecionados e omitidos

**Executados: nenhum (0).** Linhas abaixo são somente tradução pendente. Todos os dados esperados vêm deste conjunto.

| CT | Linhas traduzidas | Quantidade | Omitidos |
|---|---|---:|---|
| CT-10 | valor/total/final:1/9999/9900;29/10000/7100;29/100/71;100/9999/0 | 4/4 | nenhum |
| CT-11 | total/final:49/47;50/48;51/49; desconto efetivo2 em todos | 3/3 | nenhum |
| CT-12 | total/final:999/0;1000/0;1001/1; valor fixo1000 | 3/3 | nenhum |
| CT-13 | porcentagem e fixo × 2026-10-09T17:59:59Z→aceito9000/usos2/trilhas2;18:00:00Z→recusa/usos1/trilha1;18:00:01Z→recusa/usos1/trilha1 | 6/6 | nenhum; expiração2026-10-09T18:00:00Z |
| CT-22 | porcentagem e fixo × antes2→aceito/depois3;antes3→recusado/depois3;antes4 legado→recusado/depois4; trilhas iguais ao contador final | 6/6 | nenhum |
| CT-26 | porcentagem10 e fixo1000; Beto/2026-10-09T18:00:00Z, Ana criadora | 2/2 | nenhum |
| CT-28 | porcentagem10 e fixo1000; Beto18:00:00Z seguido de Carla18:00:01Z | 2/2 | nenhum |
| CT-41 | porcentagem e fixo; argumento aplicadoPor null | 2/2 | nenhum |
| CT-07, posterior | fixo/−1/recusado | 1/10 | porcentagem0/1/100/101/string12.5; fixo100/101/102/string12.5 |
| CT-B01 | cenário único porcentagem→fixo/centavos; não possui tabela de Examples | 1 cenário parcial | gravação NOVO fixo150, validade futura, limite3, contador0 não executada/traduzida |

São 28 invocações backend do recorte inicial, 1 invocação exploratória posterior de CT-07 e 1 invocação browser parcial; **zero executadas**. Modo tenancy somente; destinos singletenant do índice não foram materializados neste piloto.

## Seleção exploratória posterior ao julgamento

A sessão orquestradora solicitou depois do julgamento o recorte de criação por componente com fixo negativo, condicionando à presença literal. Ele consta em CT-07, Example `fixo | -1 | recusado | inteiro negativo viola P-05`. O teste está separado e não inclui edição, escrita direta ou outras linhas de validador. A seleção não altera o conjunto derivado nem inventa CT novo. Não foi lido resultado/veredito para escolher a asserção.

## Inventário completo

Status integral/parcial se refere à tradução; nenhum cenário está certificado executado. Não selecionado = fora do recorte, não dispensa. Bloqueado seria entrada/API sem expressão possível; os seletores do CT-B parcial permanecem pendentes, com eventual bloqueio técnico na execução.

| CT | Status | Motivo / referência |
|---|---|---|
| CT-01 | não selecionado | rotas de CRUD/recuperação fora do recorte |
| CT-02 | não selecionado | cadastro positivo fora do recorte |
| CT-03 | não selecionado | edição de campos fora do recorte |
| CT-04 | não selecionado | obrigatórios no create fora do recorte |
| CT-05 | não selecionado | obrigatórios no edit fora do recorte |
| CT-06 | não selecionado | escrita direta fora do recorte |
| CT-07 | parcial | 1/10 Examples; fixo−1 por componente, seleção posterior ao julgamento |
| CT-08 | não selecionado | edição de domínio, inclusive negativos, fora do recorte |
| CT-09 | não selecionado | validação direta fora do recorte |
| CT-10 | integral | 4 Examples de retorno traduzidos |
| CT-11 | integral | 3 Examples de desconto/retorno traduzidos |
| CT-12 | integral | 3 Examples de fixo/piso zero traduzidos |
| CT-13 | integral | 6 Examples e seus efeitos traduzidos |
| CT-14 | não selecionado | objeto validado antes da expiração fora do recorte |
| CT-15 | não selecionado | fusos/DST fora do recorte |
| CT-16 | não selecionado | unicidade na criação fora do recorte |
| CT-17 | não selecionado | unicidade na edição fora do recorte |
| CT-18 | não selecionado | unicidade direta/singletenant fora do recorte |
| CT-19 | não selecionado | identidade inexistente fora do recorte |
| CT-20 | não selecionado | objeto removido fora do recorte |
| CT-21 | não selecionado | save removido/inexistente fora do recorte |
| CT-22 | integral | 6 Examples e seus efeitos traduzidos |
| CT-23 | não selecionado | consumo stale fora do recorte |
| CT-24 | não selecionado | concorrência multiprocesso fora do recorte; não simulada com sequência |
| CT-25 | não selecionado | payload contador/limite fora do recorte |
| CT-26 | integral | 2 Examples de autor/instante e efeitos traduzidos |
| CT-27 | não selecionado | matriz geral de recusas fora do recorte |
| CT-28 | integral | 2 Examples de história e autoria traduzidos |
| CT-29 | não selecionado | rollback tardio fora do recorte |
| CT-30 | não selecionado | matriz de papéis×verbos fora do recorte |
| CT-31 | não selecionado | escrita vedada por componente fora do recorte |
| CT-32 | não selecionado | escrita direta vedada fora do recorte |
| CT-33 | não selecionado | exclusão positiva fora do recorte |
| CT-34 | não selecionado | exclusão de ausente fora do recorte |
| CT-35 | não selecionado | IDOR administrativo fora do recorte |
| CT-36 | não selecionado | aplicar objeto estrangeiro fora do recorte |
| CT-37 | não selecionado | payload de tenant fora do recorte |
| CT-38 | não selecionado | partições da listagem fora do recorte |
| CT-39 | não selecionado | busca/paginação fora do recorte |
| CT-40 | não selecionado | fonte pública de listagem fora do recorte |
| CT-41 | integral | 2 Examples de argumento null/recusa e conservação traduzidos |
| CT-42 | não selecionado | tenant corrente nulo fora do recorte |
| CT-43 | não selecionado | código novo/validade hidratada no edit fora do recorte |
| CT-44 | não selecionado | leitura de edit vedada fora do recorte |
| CT-45 | não selecionado | participante histórico na listagem fora do recorte |
| CT-B01 | parcial | seleção/unidade/operabilidade; gravação omitida e seletores finais pendentes |
| CT-B02 | não selecionado | troca/erro no edit fora do recorte |

A conferência estática Python dos próprios artefatos leu o conjunto e verificou 47 IDs inventariados, únicos, com nomes de teste contidos no conjunto; passou. Esse script não carregou PHP ou aplicação.

Não foram executados lint PHP, suítes, servidor, browser ou comandos do repositório de skills. Risco restante: tradução, classe de página e seletores não validados; a sessão que congelará/executará serialmente deve distinguir falhas técnicas e divergências do CT, sem alterar os oráculos após resultados.
