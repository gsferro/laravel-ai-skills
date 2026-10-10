# Materialização de cupons — K7

Primeira tradução, **sem execução**, preparada para congelamento pela sessão orquestradora. O status integral/parcial abaixo descreve a tradução dos observáveis e Examples, nunca resultado verde. Executor: família GPT-6; esforço ultra solicitado; deployment exato não exposto.

O registro inicial abaixo descreve o momento anterior ao congelamento em `testes/cuponsv1/`. A seção final registra o diagnóstico técnico posterior autorizado; as afirmações iniciais de ausência de execução/leitura de logs pertencem à primeira tradução.

## Entradas e restrições efetivas

- Domínio: somente `judges/conjunto-k7/conjunto.md`, lido integralmente. O conjunto é anônimo; nenhuma identidade de versão foi recebida.
- `runtime/contrato-publico.md` foi usado somente para nomes de classes/APIs, schema e factories/helpers. Seus resultados e regras não foram usados como oráculo.
- Técnica: `tests/Pest.php`, `tests/TestCase.php`, `tests/TenancyTestCase.php`, `phpunit.xml` e vendor instalado de Laravel, Filament e pest-plugin-browser. Não foram abertos código da feature, testes do implementador, catálogos, vereditos, prompts de juiz, requisitos/planos externos, logs ou repositório de skills.
- Filesystem irrestrito; cegamento por contrato de leitura, sem sandbox mecânico ou whitelist. Todas as chamadas de shell desta tradução usaram `login:false`. Prompt e ausência de edições não provam isolamento de leitura.
- `TenancyTestCase` + `RefreshDatabase` já registrados no arnês; nenhum arquivo do arnês ou da aplicação foi alterado. Novos artefatos deste conjunto: `tests/ExperimentoReal/K7/CuponsTest.php`, `tests/BrowserTenancy/ComparacaoK7Test.php` e este mapa.
- Não houve Artisan, Pest, browser, servidor, build ou mutation testing. As tabelas de previsões contidas na entrada integral não são operadores executados; nenhum operador real foi recebido/antecipado. DDR, tokens, host e mortes continuam não medidos.

## Costura e leitura dos resultados futuros

O backend chama `Cupom::aplicarEm` com ator explícito e compara banco real. Histórias anteriores são aplicações reais; o legado 4/3 é preparado depois dessas aplicações com `forceFill(...)->saveQuietly()`, sem afirmar que edição do limite é aceita. Seeder Shield precede Papeis; Acme, papéis, membership e contexto reais usam os helpers existentes. O relógio é restaurado em `afterEach`.

Recusa significa chamada sem retorno aceito, com exceção e conservação dos efeitos exigidos. Nenhuma mensagem ou classe de exceção de negócio é imposta. `Error` e `QueryException` são relançadas para não converter falha técnica em recusa de negócio; outros erros precisam de classificação da sessão executora. Não há endpoint HTTP inventado.

O CT-37 comprova `A` como primeiro resultado de `Cupom::query()->firstOrFail()` antes do Quando. Se essa precondição falhar, o cenário é bloqueio de fixture/arnês; não é uma prova de identidade bem-sucedida.

Browser usa `pest()->browser()->inChrome()` e as APIs instaladas `visit`, `select`, `assertPathIs`, `assertScript`, `assertNoJavaScriptErrors`. O mecanismo proposto localiza o select/input pelos IDs terminados em `.tipo`/`.valor` e o label associado por `htmlFor`, com retângulo e estilos visíveis. Native select e IDs finais **não conferidos**: ausência deles deve ser classificada como bloqueio técnico e pode exigir ajuste de seletor, preservando o oráculo. O teste não recarrega/navega entre as duas seleções. Não existe `wait` fixo nem fake de DOM/Livewire.

## CT → testes e asserções literais traduzidas

Arquivo backend: `tests/ExperimentoReal/K7/CuponsTest.php`. Cada nome começa com CT original e `[K7]`.

| CT | Teste / status de tradução | Literal de aceitação traduzido | Omitido |
|---|---|---|---|
| CT-31 | percentual inteiro trunca a fração do desconto — integral | total devolvido exatamente final; contador persistido 1; uma linha da aplicadora | nenhum observável do CT no modo tenancy |
| CT-32 | desconto fixo conserva piso zero — integral | total devolvido exatamente final; contador persistido 1; uma linha da aplicadora | nenhum observável do CT no modo tenancy |
| CT-25 | segundo exato da expiração recusa com controle anterior aceito — integral | retorno/recusa, contador e número de novas linhas dos Examples; história real preservada | nenhum observável do CT no modo tenancy |
| CT-28 | limite atingido recusa com último uso disponível aceito — integral | retorno/recusa, contador e novas linhas de cada Example; linhas anteriores preservadas | nenhum observável do CT no modo tenancy |
| CT-35 | aplicação incrementa uma vez e mantém as duas linhas anteriores — integral | retorno 9000, contador 3, duas linhas anteriores idênticas e exatamente uma nova da aplicadora | nenhum observável do CT no modo tenancy |
| CT-36 | argumento aplicadoPor identifica Beto e o instante com guard ausente igual ou distinto — integral | exatamente uma linha para cupom/Beto em T; retorno 9000 e contador 1 | nenhum observável do CT no modo tenancy |
| CT-37 | somente B ganha a aplicação de Beto preservando A e a história anterior — integral | retorno 9000; B contador 2, Ana/T−1 e Beto/T; A atributos/contador 1/trilha Ana/T−2 iguais ao snapshot | nenhum observável do CT; precondição de primeiro resultado depende do runtime |
| CT-B01 | `tests/BrowserTenancy/ComparacaoK7Test.php`: Chromium troca tipo e mostra a nova unidade sem reload; gravação omitida — parcial | select real inicial→final; indicação associada ao valor visível na unidade final e sem a anterior; ambos os sentidos | concluir formulário; NOVO na Acme com tipo/valor 1000 ou 29; confirmação de destino após gravação |

Asserções de DOM aceitam semântica percentual (`%`, porcentagem ou percentual) e centavos, sem frase literal do PRD. Console é apenas apoio. CT-B01 não foi substituído por um smoke de console nem considerado integral.

## Examples selecionados e omitidos

**Executados: nenhum (0).** Linhas abaixo estão traduzidas e pendentes de execução. Nenhuma linha de um rival foi acrescentada.

| CT | Linhas traduzidas | Quantidade | Linhas omitidas |
|---|---|---:|---|
| CT-31 | percentual/total/final: 29/10000/7100; 29/100/71; 10/9999/9000; 5/50/48; 1/100/99; 100/9999/0 | 6/6 | nenhuma |
| CT-32 | valor/total/final: 1000/999/0; 1000/1000/0; 1000/1001/1; 1/1/0; 1000/0/0 | 5/5 | nenhuma |
| CT-25 | para porcentagem e fixo: T−1→9000/contador3/nova1; T→recusa/contador2/nova0; T+1→recusa/contador2/nova0 | 6/6 | nenhuma; T fixado em 2026-10-10T12:34:56Z |
| CT-28 | para porcentagem e fixo: usos2→9000/3/nova1; usos3→recusa/3/nova0; legado usos4→recusa/4/nova0 | 6/6 | nenhuma |
| CT-35 | porcentagem10 e fixo1000, contador2/limite5→contador3 e uma nova linha | 2/2 | nenhuma |
| CT-36 | porcentagem10 e fixo1000 × guard ausente/Beto/Ana; argumento sempre Beto; instante 2026-10-10T12:34:56Z | 6/6 | nenhuma |
| CT-37 | B porcentagem10 e B fixo1000; A fixo3000 em ambos | 2/2 | nenhuma |
| CT-B01 | porcentagem→fixo/centavos e fixo→porcentagem/pontos percentuais | 2/2 para seleção/unidade | parte de gravação dos dois Examples: valores 1000 e29 não submetidos nem persistidos |

São 33 invocações backend e 2 invocações browser traduzidas, **zero executadas**. Apenas o modo tenancy foi materializado; os pares singletenant propostos no índice original não entram neste piloto.

## Seleção exploratória posterior ao julgamento

A sessão orquestradora pediu posteriormente o recorte de criação por componente de fixo negativo, somente se literal na entrada. CT-08 de K7 contém fixo1, fixo101 e fixo1000; **não contém fixo−1**. Não foi criado teste negativo, CT novo, expectativa de recusa nem transferência do conjunto rival. CT-08 continua não selecionado. Esta ausência é documental, sem execução da feature.

## Inventário completo

Integral/parcial = tradução; não selecionado = fora do recorte; bloqueado = tradução inviável por entrada/API insuficiente. Nenhum CT está certificado executado. O CT-B parcial tem dívida técnica de seletores e gravação. CT sem direção de oráculo não virou cenário novo.

| CT | Status | Motivo / referência |
|---|---|---|
| CT-01 | não selecionado | visita de CRUD fora do recorte |
| CT-02 | não selecionado | criação de CRUD fora do recorte |
| CT-03 | não selecionado | edição de CRUD fora do recorte |
| CT-04 | não selecionado | exclusão fora do recorte |
| CT-05 | não selecionado | validação de tipo fora do recorte |
| CT-06 | não selecionado | validação de tipo na edição fora do recorte |
| CT-07 | não selecionado | escrita direta fora do recorte |
| CT-08 | não selecionado | domínio na criação; fixo negativo ausente da entrada |
| CT-09 | não selecionado | domínio na edição fora do recorte |
| CT-10 | não selecionado | validação direta fora do recorte |
| CT-11 | não selecionado | unicidade fora do recorte |
| CT-12 | não selecionado | unicidade na edição fora do recorte |
| CT-13 | não selecionado | unicidade direta fora do recorte |
| CT-14 | não selecionado | matriz de autorização fora do recorte |
| CT-15 | não selecionado | matriz de escrita direta fora do recorte |
| CT-16 | não selecionado | revogação fora do recorte |
| CT-17 | não selecionado | papéis acumulados fora do recorte |
| CT-18 | não selecionado | IDOR fora do recorte |
| CT-19 | não selecionado | saída de erro administrativo fora do recorte |
| CT-20 | não selecionado | objeto estrangeiro fora do recorte |
| CT-21 | não selecionado | tenant nulo fora do recorte |
| CT-22 | não selecionado | listagem fora do recorte; não é CT-28 |
| CT-23 | não selecionado | paginação fora do recorte |
| CT-24 | não selecionado | busca fora do recorte |
| CT-25 | integral | 6 Examples e observáveis traduzidos |
| CT-26 | não selecionado | objeto anteriormente validado fora do recorte |
| CT-27 | não selecionado | fuso local/UTC fora do recorte |
| CT-28 | integral | 6 Examples e observáveis traduzidos |
| CT-29 | não selecionado | consumo stale fora do recorte |
| CT-30 | não selecionado | concorrência multiprocesso fora do recorte; não substituída por sequência |
| CT-31 | integral | 6 Examples e observáveis traduzidos |
| CT-32 | integral | 5 Examples e observáveis traduzidos |
| CT-33 | não selecionado | existência/inatividade genérica fora do recorte |
| CT-34 | não selecionado | percentual legado inválido fora do recorte |
| CT-35 | integral | 2 Examples e observáveis traduzidos |
| CT-36 | integral | 6 Examples guard×argumento e instante traduzidos |
| CT-37 | integral | 2 Examples, histórias e alvo/não-alvo traduzidos |
| CT-38 | não selecionado | falha transacional antes da trilha fora do recorte |
| CT-39 | não selecionado | falha depois da trilha fora do recorte |
| CT-40 | não selecionado | chave removida/escrita fora do recorte |
| CT-41 | não selecionado | aplicar removido fora do recorte |
| CT-42 | não selecionado | mass assignment de formulário fora do recorte |
| CT-43 | não selecionado | mass assignment direto fora do recorte |
| CT-44 | não selecionado | estado de tabela fora do recorte |
| CT-45 | não selecionado | propriedade record fora do recorte |
| CT-46 | não selecionado | listagem de removido fora do recorte |
| CT-47 | não selecionado | combinação expirado/esgotado fora do recorte |
| CT-48 | não selecionado | admissão/escrita no painel fora do recorte |
| CT-49 | não selecionado | auditoria após exclusão fora do recorte |
| CT-50 | não selecionado | conversão de data no CRUD fora do recorte |
| CT-51 | não selecionado | colisão de código entre tenants fora do recorte |
| CT-B01 | parcial | 2 Examples de seleção/DOM; gravação e seletores finais pendentes |
| CT-B02 | não selecionado | ciclo de erro/correção fora do recorte |

A conferência estática Python dos próprios artefatos leu o conjunto e verificou 53 IDs inventariados, únicos, com nomes de teste contidos no conjunto; passou. Esse script não carregou PHP ou aplicação.

Não foram executados lint PHP, suítes, servidor, browser ou comandos do repositório de skills. Risco restante: tradução e seletores ainda não validados; falhas técnicas devem ser separadas de divergências de comportamento pela sessão que congelará e executará serialmente.

## Diagnóstico técnico posterior ao congelamento — sem execução por este braço

A sessão autorizou leitura de `control.log` e `resultado.json` de `D:/PROJECTS/SKILLS/laravel-ai-skills/experimentos/2026-10-09-projeto-real/execucao-derivada/browserk7v1/` e da pasta equivalente `browserm4v1/`, exclusivamente para diagnosticar seletor/unidade. Nenhum outro log ou artefato de execução foi lido. A primeira tradução congelada não foi aberta nem alterada. O filesystem permanece irrestrito e o cegamento continua contratual; as leituras técnicas permaneceram nos próprios arquivos e vendor instalado, com `login:false`.

No log K7, os dois Examples browser falharam no predicado que exige centavos: na troca porcentagem→fixo e no estado inicial fixo. O mecanismo instalado `AwaitableWebpage` já repete as expectativas, e o log registra a falha depois do limite de repetição. Isso não determina se a causa está na sincronização, no seletor, no DOM ou no comportamento da aplicação. As duas expectativas e os seletores do CT-B01 permanecem inalterados; nenhum label alternativo passou a ser aceito. O backend e a seleção de Examples K7 também permanecem inalterados.

Foi criado, por autorização específica da sessão, `tests/BrowserTenancy/DiagnosticoCuponsTest.php`, separado dos CT comparativos. Ele usa a fixture pública de Acme/admin, seleciona porcentagem e depois fixo em Chromium e emite em STDERR `CUPOM_DOM_PROBE` com os snapshots após as seleções, após `waitForEvent('networkidle')` e no encerramento. Coleta `select.value`, atributos, HTML do select, estado do input, labels associados por `htmlFor`, texto/outerHTML do wrapper `[data-field-wrapper]` e mensagens de console/erros JavaScript pelas APIs vendor. O estado de rede é apenas um marco técnico; não prova atualização semântica do campo. O probe não contém asserção de unidade, não cria CT, não salva cupom e não conta como execução/cobertura comparativa. Sua execução está pendente da sessão orquestradora.

O vendor de screenshot resolve a pasta `runtime/tests/Browser/Screenshots/` e acrescenta `.png`. Foi conferida somente a existência do caminho exato `D:/PROJECTS/SKILLS/blind-20261009/runtime/tests/Browser/Screenshots/it_CT_B01__K7__Chromium_troca_tipo_e_mostra_a_nova_unidade_sem_reload__gravação_omitida.png`: ausente no momento da conferência. Nenhuma screenshot foi aberta e nenhuma pasta de resultados foi percorrida.

Nenhum Artisan, Pest, browser, servidor ou lint PHP foi executado por este braço neste ajuste. As falhas acima são evidência restrita dos logs de execução da sessão; não certificam controle verde, causa da falha ou cobertura. O inventário e seus status de tradução continuam os mesmos; CT-B01 permanece parcial, com gravação omitida e diagnóstico de unidade pendente.

Uma revisão independente leu somente o probe próprio e as APIs vendor pertinentes, confirmou as assinaturas e levou à proteção individual das coletas finais: falha em uma coleta é registrada sem descartar snapshots anteriores ou substituir a exceção principal. Limitação de processo relatada pelo revisor: seu primeiro comando iniciou o perfil padrão do PowerShell e exibiu erro PSReadLine; os seguintes usaram `login:false`. As chamadas deste materializador continuaram com `login:false`, mas não se afirma essa configuração para toda a revisão. Não houve execução PHP/app/browser na revisão nem evidência de isolamento mecânico de leitura.
