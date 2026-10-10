# Casos de Teste — FERRO-830: aprovação de solicitação de compra

> Derivado do **requisito**, não do plano. Fonte: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md` inteiro; do `01`, somente paths, rotas, nomes e `## Superfície de UI` admitidos como insumos.
> feature-wiki **4.1.0** · feature-test-design **1.17.0** · 2026-10-09.
> Revisão adversarial: **CONCLUÍDA — duas rodadas independentes**. Rodada 1: 10 achados; rodada 2: 11 achados; todos receberam fechamento documentado. **Dívida: novos CT e alterações do fechamento final não foram reavaliados independentemente após o teto 2; cobertura não aprovada.** Execução de testes pendente e separada do status da revisão. Nenhuma autorrevisão. Costuras são propostas do subagente; `Confirmada` fica vazia para a sessão principal.

## Contrato de execução e limites efetivos

Leituras deliberadas restritas a `D:\PROJECTS\SKILLS\blind-20261009\project-26`, ao prompt-c2, às duas skills e referências condicionais, ao `00` e à superfície/path do `01`, convenções e arnês permitidos. Entradas de fechamento autorizadas: próprios `adversarial-1.md` e `adversarial-2.md`; o 00 vigente foi relido na segunda rodada e continuou sendo o único oráculo. Sem leitura de saída-c1, outros conjuntos, catálogo, experimentos, resultados de outros braços, outra cópia ou testes Exp. Escrita do derivador somente nesta pasta, em `04` e `retorno-c2.md`; relatórios independentes preservados.

Filesystem **irrestrito**: contrato de caminhos não é isolamento técnico. A primeira execução com login padrão acionou automaticamente `C:\Users\CASA\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`, fora do contrato de caminhos; as seguintes usaram `login:false`. O perfil automático é um limite efetivo registrado. Host Codex; família GPT-6 herdada; ultra solicitado; deployment exato não exposto.

`02` ausente (`Test-Path .../02-decisoes-arquiteturais.md -> False`); não criado. Sem execução de Artisan, Pest, navegador, mutation testing ou instalação. `00`/`01` imutáveis e não alterados. Entrada legada sem coluna Estado ou P-nn: A-01…A-12 são premissas dadas pelo prompt, não novas respostas. A tentativa de gravação por comando longo foi recusada antes de iniciar o processo pelo limite de tamanho do Windows; a escrita passou a usar patches.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Fundamento |
|---|---|---|---|---|---|
| Autorização e fluxo | 3 | 3 | 9 | completo | identidade, dinheiro, estados e interleaving concorrente |
| Alçada e domínios de entrada | 3 | 3 | 9 | completo | dinheiro, limiar e combinação de papéis; partes abertas |
| Notificações e recorte organizacional | 3 | 3 | 9 | completo | integração externa e dados da organização; partes abertas |
| Administração de centros | 2 | 3 | 6 | padrão | integração ao painel; escalada pela troca do gestor |
| Interface de operações e apresentação | 2 | 2 | 4 | padrão | componentes existentes; leitura incorreta causa retrabalho |

Perfis decididos pelo **passo 0**, nenhum imposto. Há Impacto 3. Passos 1–7 percorridos; regras que atravessam áreas herdam o maior perfil. BVA 3-valores aplicada à alçada definida em A-04; os limites numéricos ausentes continuam lacunas. Pairwise não reduz estado/identidade: as tabelas críticas são integrais; combinações materiais não decididas ficam em Q?3. A primeira revisão mostrou que perguntas pendentes não revogam obrigações expressas do 00: o mapa abaixo separa a parte determinada da direção ainda sem resposta.

Cenários: 61 · Regras: 24 · Mutantes previstos: 88 · Sem matador: 0. Contagens estruturais derivadas por regex equivalentes aos quatro grep -c do template; nenhum resultado de execução inferido.

Contagem estrutural, não detecção medida. Esquema conta uma vez, sem inflação pelo número de exemplos. Uma direção sem resposta não conta como coberta; não suspende o núcleo já determinado. Histórico da preliminar: 37 CT, 11 regras, 42 mutantes previstos; as revisões são registradas ao final.

## Varredura SFDIPOT

| Dimensão | Inventário anterior aos cenários | Saída |
|---|---|---|
| S | solicitação, centro, decisões de etapa, diretor; Resources/forms nomeados pelo 01 | R1–R24; inventário Livewire ausente |
| F | criar, corrigir, excluir, enviar, aprovar, rejeitar, cancelar, apresentar, notificar | CT-01…CT-61; perguntas/lacunas |
| D | descrição, decimal, centro, gestor nulo, justificativa, instante conhecido, autores históricos, diretores 0/1/N, outra organização | CT-01/02/14/18/22/38/40/41/43/44/45/48/49/50/52–61; domínios/recortes pendentes |
| I | componente e chamada direta fora da UI; sem API/job/comando novo pedido | Domínio e Componentes; 02 faltante |
| P | Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1, browser 5.0.1, mutate 5.0.2 | lock e arnês lidos; nenhuma execução |
| O | solicitante, gestor por centro, diretor por organização, administração, papéis acumulados | matrizes; CT-19; Q?3 |
| T | ordem, rejeitar→corrigir→reenviar, retries, primeira decisão e snapshot antigo | CT-15/23/24/31/41/42/51/56/58; SLA/expiração fora de escopo |

## Matriz única estado × operação

Montada antes das regras: **5 estados × 10 operações = 50 células**. Os estados são os do `00` (A-05/A-06), sem leitura do enum da implementação. Aprovar/rejeitar têm persona/etapa próprias; listar e detalhar são operações distintas. Criação não parte de solicitação existente e fica no gate aberto de RQ-01.

Legenda: ✅ operação válida executada; ❌ operação recusada, preservando situação, campos e histórico de decisões, sem novo e-mail a destinatários reais; L = lacuna declarada. A edição fora do rascunho afirma valores persistidos. Cada decisão afirma ausência de nova decisão; verbo irmão não herda chamada. As recusas comparam o histórico existente, não um mundo vazio.

| Estado | editar/S | excluir/S | enviar/S | aprovar/G | rejeitar/G | aprovar/D | rejeitar/D | cancelar/S | listar | detalhar |
|---|---|---|---|---|---|---|---|---|---|---|
| rascunho | ✅ CT-01/05 | ✅ CT-06 | ✅ CT-11 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-21 | ❌ CT-29 | L Q?5 | L Q?5 |
| aguardando_gestor | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ✅ CT-16 | ✅ CT-20 | ❌ CT-26 | ❌ CT-22 | ✅ CT-28 | L Q?5 | L Q?5 |
| aguardando_diretor | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-22 | ✅ CT-42 | ✅ CT-20 | ✅ CT-28 | L Q?5 | L Q?5 |
| aprovada | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-27 | ❌ CT-29 | L Q?5 | L Q?5 |
| cancelada | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-21 | ❌ CT-29 | L Q?5 | L Q?5 |

9 escritas válidas e 31 inválidas possuem cenários propostos; 10 células continuam lacunas do recorte de leitura por persona. CT-16/19 agora afirmam aprovação final na faixa inferior; CT-41 discrimina as três bordas e CT-42 exerce a célula válida do diretor com S/G/D distintos. CT-46/47 exercem todas as situações na listagem e no detalhe para acesso explicitamente autorizado. Não fecham as 10 células de recorte pendentes Q?5: os observáveis são status por superfície, sem decidir quem recebe acesso. Criação no estado inicial sem solicitação agora tem CT-38/40.

Personas distintas S/G/D/H/U nos negativos; S=G dado por A-09 tem CT-19. S=D e G=D ficam em Q?3. CT-01 altera descrição, valor e centro em rascunho; CT-02 tenta os três fora dele e exige os valores antigos persistidos.

## Mapa de Regras

| Regra | Área/perfil herdado | Origem | Técnica | CT |
|---|---|---|---|---|
| R1 edição do rascunho | autorização/fluxo completo | RQ-02 | papel×ação, estado×operação, EP | CT-01…05 |
| R2 exclusão do rascunho | autorização/fluxo completo | RQ-03 | papel×ação, estado×operação, EP | CT-06…10 |
| R3 envio primeiro ao gestor | autorização/fluxo completo | RQ-04; A-02/A-10 | estado×operação, identidade, EP | CT-11…15 |
| R4 aprovação do gestor | autorização/fluxo completo | RQ-06; A-02/A-09 | papel×ação, estado×operação | CT-16…19 |
| R5 rejeição da etapa | autorização/fluxo completo | RQ-06/RQ-08; A-03/A-07 | estado×operação, identidade | CT-20…22 |
| R6 corrigir e reenviar | autorização/fluxo completo | RQ-09/RQ-04 | 2-switch, estado×operação | CT-23…25 |
| R7 imutabilidade/ordem | autorização/fluxo completo | RQ-10/RQ-04; A-03/A-05 | estado×operação, identidade | CT-26/27 e células terminais anteriores |
| R8 cancelamento | autorização/fluxo completo | RQ-11; A-06 | estado×operação, identidade, interleaving | CT-28…31 |
| R9 administração | administração padrão | RQ-04; A-08 | papel×ação, ação efetiva | CT-32/33 |
| R10 affordance/gravação | interface padrão | RQ-02/03/04/06/08/11; A-07 | decisão, EP por persona/estado | CT-34…36 |
| R11 removido não funciona | autorização/fluxo completo | RQ-03/04/06/11 | EP por operação, identidade do agregado | CT-37 |
| R12 criação válida | alçada/domínios completo | RQ-01; A-01 | EP positiva e gravação | CT-38…40 |
| R13 alçada e decisão final | alçada/fluxo completo | RQ-05; A-03/A-04 | BVA 3-valores, decisão, discriminante configurável | CT-41…43; CT-16/19 reforçados |
| R14 justificativa obrigatória | autorização/fluxo completo | RQ-07; A-07 | EP ausência/presença, não-efeito | CT-44/45 |
| R15 status apresentado | interface padrão | RQ-12; A-12 | EP exaustiva por situação e superfície | CT-46/47 |
| R16 identidades na visualização | interface padrão | RQ-13; A-12 | rastreio da decisão à apresentação | CT-48 |
| R17 próximo aprovador por e-mail | notificações completo | RQ-14; A-02/A-03/A-11 | efeito exato, 1/N, ausência e uma vez | CT-49…51; não-efeitos existentes |
| R18 CRUD administrativo válido | administração padrão | A-01/A-08; RQ-01/RQ-04 | papel×operação positiva | CT-52 |
| R19 formulários administrativos válidos | administração/UI padrão | A-01/A-08; RQ-01/RQ-04 | visita e gravação por operação | CT-53/54 |
| R20 diretoria plural e primeiro decisor | autorização/fluxo completo | A-03/A-05/A-07; RQ-05/RQ-06/RQ-10 | identidade em N; estado×evento stale | CT-55/56 |
| R21 conteúdo histórico | apresentação padrão | A-12; RQ-12/RQ-13 | estado/quantidade, instante, autoria histórica | CT-48/57/58 |
| R22 ausência de gestor fora da UI | autorização/fluxo completo | A-10; RQ-04 | partição ausente; superfície; efeitos | CT-14/59 |
| R23 decisões pelo componente | autorização/fluxo completo | RQ-05/RQ-06/RQ-08; A-03/A-07/A-11 | etapa×valor×verbo | CT-60/61 |
| R24 destinatário corrigido e callback | notificações completo | RQ-04/RQ-09/RQ-14; A-02/A-11 | destinatário×etapa×superfície | CT-23/36 |

- RQ-01: criação válida determinada e coberta por R12; limites/normalização e retry seguem abertos Q?1/Q?7, sem cenário direcional até resposta.
- RQ-05: duas etapas, ordem, comparação estrita e configurabilidade dadas, cobertas por R13; S=D/G=D e zero diretores seguem abertos Q?3/Q?4, sem cenário da direção indecidida.
- RQ-07: ausência de justificativa já viola a obrigatoriedade, coberta por R14; teto/espaços/normalização de texto seguem Q?2, sem resposta inventada.
- RQ-12: status atual em lista/detalhe dado e coberto por R15 para acesso autorizado; quem vê continua Q?5.
- RQ-13: mostrar identidades das etapas no detalhe dado e coberto por R16 para acesso autorizado; recorte histórico de participantes continua Q?5.
- RQ-14: e-mail ao gestor e a todos os diretores da organização, quando existem, dado e coberto por R17; zero diretores e link continuam Q?4/Q?6.

Não há Estado aberta — Qn no 00. As perguntas devolvidas não alteraram o requisito. Esta delimitação fecha ADV-01…06 sem atribuir ao solicitante nenhuma resposta nova.

## Costuras de Teste

| Grupo | Regras | Costura | Existente/nova | Por quê | Confirmada |
|---|---|---|---|---|---|
| Domínio | R1–R8/R11–R14/R17/R20/R22/R24 | Pest feature HTTP | existente: TestCase/RefreshDatabase de Feature | persistência e chamada direta sem UI | |
| Componentes | R1/R3/R10/R12/R14–R16/R21–R24 | componente Livewire/Filament | existente: EditUser de tests/Kit/PaginasInfraTest.php | campos/actions/DOM, histórico e gravação | |
| Administração | R9/R18 | Pest feature HTTP | existente: convenção de AdminDaOrganizacaoTest; novos testes fora do kit | escrita administrativa positiva e recusada fora da tela | |
| Administração UI | R9/R19 | componente Livewire/Filament | existente: arnês do painel | visita e gravação autorizadas; recusa de panel_user | |
| Alçada e domínios pendentes | RQ abertas | Pest feature HTTP | proposta nova no arnês Feature | BVA e domínio na gravação | |
| Recorte organizacional e mensagens | R17/CT-50; direções pendentes | Pest feature HTTP | nova FeatureTenancy não registrada | diretoria da organização exige teams antes das migrations; sem mudar arnês nesta rodada | |
| Apresentação pendente | recorte de acesso Q?5 | componente Livewire/Filament | existente: arnês de componente | acesso histórico por participante ainda sem resposta | |

Costuras novas não criadas nem confirmadas. Nenhuma costura browser.

## Fronteira com o Plano

| Item do 01 | Recusado como oráculo / tratamento | Destino |
|---|---|---|
| Paths dos Resources/páginas e rotas /app[/tenant] | localização permitida, não resultado esperado | índice/gate |
| Nomes enviar/aprovar/rejeitar/cancelar | mecanismo/nome, não determina o resultado | materialização futura |
| Gate antigo JS=Sim + personas → 05 | diverge do gate instalado: DOM/action já prováveis por componente | Sem CT-B |
| minValue/maxLength, DB/fillable/locks/UPDATE | domínio e fronteira não confirmados no 00 | Q?1/Q?2; 02 ausente |
| Mensagem exata, cores e link/corpo do e-mail | comportamento visível não determinado no card | pergunta; sem texto inventado |
| logs/comandos e CT antigos citados no 01 | não são oráculo; testes antigos não lidos; warning vem expressamente do 00/A-10 | CT-14/59 afirmam esse warning; sem execução |

## Perguntas para o 00-requisito.md

Desvio: 00 imutável; perguntas aqui prontas para colagem, com IDs provisórios. Sem respostas e nenhuma recomendação assumida como aprovação. Premissas A-01…A-12 dadas não revogadas. Após ADV-01…06, afeta identifica a parte indecidida da cláusula, não autorização para retirar as obrigações expressas. As perguntas originais permanecem abaixo como histórico; criação válida, obrigatoriedade e apresentação/envio positivos são as partes já dadas.

❓ Q?1 · raia: requisito · afeta: RQ-01 · depende de: —
Quais domínios/limites de descrição e nome do centro, mínimo/máximo monetário, escala/regra de centavo e semânticas de ausente/null/vazio/espaços na criação, edição e uso?
➡️ Recomendação: falhar fechado em entradas sem conteúdo ou fora do domínio acordado; obter limites literais antes de n/n+1, sem adotar 120/255/0,01 do plano.

❓ Q?2 · raia: requisito · afeta: RQ-07 · depende de: —
Qual teto da justificativa e tratamento de só espaços, bordas, null e campo ausente? A obrigatoriedade está dada, o domínio completo não.
➡️ Recomendação: falhar fechado sem conteúdo e fora do teto acordado; definir n/n+1 no domínio. Não inventar mínimo de caracteres.

❓ Q?3 · raia: requisito · afeta: RQ-05 · depende de: —
Além de S=G dado por A-09, S=D e G=D são permitidos? A mesma pessoa pode decidir as duas etapas em decisões distintas?
➡️ Recomendação: falhar fechado na combinação não decidida e preservar duas decisões/ordem; o solicitante decide se as identidades também precisam ser distintas.

❓ Q?4 · raia: requisito · afeta: RQ-05, RQ-14 · depende de: —
Com zero diretores na organização, qual estado/saída após o aval do gestor acima da alçada, e quem recebe o aviso? A-10 responde apenas zero gestores.
➡️ Recomendação: falhar fechado sem aprovação final automática; pendência/recusa e destino alcançável precisam ser decididos pelo solicitante.

❓ Q?5 · raia: requisito · afeta: RQ-12, RQ-13 · depende de: —
Quem lista/detalha solicitação e histórico por estado/organização? Gestor/diretor que já participou continua vendo após devolução, cancelamento e aprovação?
➡️ Recomendação: falhar fechado fora do recorte autorizado; decidir acesso histórico. Listagem e detalhe não herdam evidência um do outro.

❓ Q?6 · raia: requisito · afeta: RQ-14 · depende de: Q?5
O e-mail precisa de link? Qual destino e visibilidade ao abri-lo fora do request do painel ou depois da mudança de etapa?
➡️ Recomendação: link, se confirmado, para destino alcançável no tenant correto; falhar fechado contra exposição entre organizações, com saída alcançável.

❓ Q?7 · raia: requisito · afeta: RQ-01 · depende de: —
Repetição da criação deve produzir duas solicitações iguais ou reconhecer retry? Há identidade de idempotência acordada?
➡️ Recomendação: falhar fechado contra duplicação involuntária, sem inventar chave/protocolo; conteúdo igual pode representar compras distintas e exige decisão.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q?1 | Domínio/limites de entrada | RQ-01 | falha fechado; limites a confirmar | aberta |
| Q?2 | Teto/vazio da justificativa | RQ-07 | falha fechado; sem mínimo inventado | aberta |
| Q?3 | S=D e G=D | RQ-05 | preservar ordem; combinação a confirmar | aberta |
| Q?4 | Zero diretores | RQ-05/RQ-14 | sem aprovação automática; saída a confirmar | aberta |
| Q?5 | Visibilidade atual/histórica | RQ-12/RQ-13 | recorte autorizado, lista/detalhe próprios | aberta |
| Q?6 | Link/destino do e-mail | RQ-14 | destino autorizado e alcançável | aberta |
| Q?7 | Retry da criação | RQ-01 | direção/identidade a confirmar | aberta |

❓ Q?8 · raia: desenho · afeta: RQ-03 · depende de: —
A exclusão é física ou usa soft delete?
➡️ Proposta: exclusão física nos CT-06/09/10/37 marcados @premissa; sessão confirma/rederiva. Soft delete permanece lacuna de mecanismo, sem dispensar escrita sobre registro removido.

## Técnicas preparadas nas áreas abertas

| Técnica | Preparação | Limite |
|---|---|---|
| BVA 3-valores da alçada | CT-41: "4999.99", "5000.00", "5000.01", incremento "0.01"; fábrica efetiva 5000.00 sem override/env de teste; CT-43 varia para 7000.00 | combinações de papéis e zero diretores Q?3/Q?4, não os destinos já dados |
| BVA de textos | n−1/n/n+1 em caracteres, acento/emoji, criação/edição/domínio externo | n ausente Q?1/Q?2 |
| EP dinheiro | decimal literal, nunca float; inválidos separados | positividade/teto/escala/arredondamento Q?1 |
| decisão dos papéis | pares S×G/S×D/G×D; CT-19 para S×G | outros pares Q?3 |
| rastreio exato de efeito | CT-49/50 mail/gestor singular/diretores 1/N; CT-51 uma vez; CT-16/19/20/28 não-efeito com destinatários reais | zero diretores Q?4; link Q?6; transporte/atomicidade não medidos |
| tenant/discriminante nulo | duas organizações e contexto nulo inventariados | Q?5 e 02 ausente; não arbitrar single-tenant/nulo |
| atomicidade | propor falha depois do despacho com G/D reais | direção/arnês e execução pendentes; pré-validação não prova atomicidade |

## Setup Global

- Stack confirmado no composer.lock por JSON: Laravel v13.25.0, Filament v5.7.6, Livewire v4.4.0, Pest v5.1.1, browser v5.0.1, mutate v5.0.2. Mutate não declarado diretamente em require-dev do composer.json. Nenhuma instalação; driver/runner não inspecionados, sem alegação de ausência.
- tests/Pest.php liga TestCase/RefreshDatabase a Feature, não a Unit. Tenancy usa TenancyTestCase antes das migrations; FeatureTenancy é proposta nova, não registrada, sem CT de negócio inserido em kit.
- S solicitante, G gestor C1, H gestor C2, D diretor e U terceiro são distintos salvo CT-19. Helpers reais `usuario`, `usuarioComPapel`, `noPainelDa` e `papelNaOrganizacao` de tests/Pest.php. Diretor é premissa A-03, não papel cuja instalação foi executada nesta rodada.
- Factories de compra/centro ausentes (`Test-Path -> False`). Materialização futura por Model::create com campos acordados; nenhuma factory/state inventada. Preparo de fixture não certifica criação aberta de RQ-01.
- Helper futuro `solicitacaoEm(...)` em tests/Pest.php monta situações por **transições reais**, nunca gravando situação à força. Caminhos diretor/final com pessoas distintas e diretor existente estão dados em A-03/A-04; continuam sem materialização/execução. Q?3/Q?4 só limitam combinações/ausência ainda não decididas.
- Capturar campos/histórico, ativar observação de efeitos após preparo e consultar o agregado novamente depois do Quando. Snapshot em memória não é oráculo.
- Notification::fake após fixtures captura canais/destinatários; positivos afirmam mail explicitamente. Fake não prova transporte SMTP. A-10 exige warning correspondente à tentativa sem gestor: CT-14/59 observam esse efeito com coleta/spy de log restrito ao intervalo da ação; um warning alheio não satisfaz a asserção. A poda anterior de CT de warning foi removida por contrariar esse efeito expresso do 00.
- APIs confirmadas no vendor: fillForm, assertHasFormErrors/NoFormErrors, assertSchemaStateSet; callAction(TestAction::make(string)->table(record)), assertActionVisible/Hidden. Gravação: fillForm + call('save') + assertDatabaseHas com campos completos, não só ID. Sem helper deprecated.
- Dois testes de convenção lidos: tests/Kit/AdminDaOrganizacaoTest.php e PaginasInfraTest.php. Rules testes.md/filament.md reforçam ação direta e visita/gravação; auth.md não adiciona comportamento desta feature. tests-browser.md fica para condição futura de browser.

## Gate de telas de escrita

| Rota/path do 01 | Visita | Gravação por componente | Limite |
|---|---|---|---|
| SolicitacoesCompra/create | CT-39 | CT-40 | positivo determinado; domínios/retry Q?1/Q?7 |
| SolicitacoesCompra/{record}/edit | CT-04 | CT-05 | inválidos de domínio Q?1 |
| CentrosCusto/create | CT-53 | CT-54 | dados válidos de administrador autorizado; domínios Q?1 |
| CentrosCusto/{record}/edit | CT-53; recusa CT-33 | CT-54; recusa CT-33 | correção positiva de nome/gestor; domínios Q?1 |

Visita e gravação positivas estão descritas para as quatro telas de escrita. Limites de domínio continuam lacunas Q?1/Q?2 e o gate não é execução nem cobertura aprovada. Nenhum GET foi apresentado como gravação, nem o requisito alterado para fechar o gate.

## Regra R1 — Somente o solicitante edita o rascunho

> RQ-02 · completo · matriz papel×ação, estado×operação, EP.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Somente o solicitante edita o rascunho
    Esquema do Cenário: [CT-01] A correção do rascunho persiste o campo alterado
      Dado um rascunho de S com descrição "Notebook", valor "3000.00" e centro C1
      Quando S altera diretamente <campo> para <novo>
      Então a consulta nova encontra <campo> igual a <novo>, mantendo S e rascunho
      Exemplos:
        | campo | novo | # partição |
        | descrição | Monitor com acento ç e emoji 🛒 | texto |
        | valor | 3000.01 | decimal |
        | centro | C2 | outro centro da mesma organização |
        | descrição | Notebook | edição sem alteração |

    Esquema do Cenário: [CT-02] Editar fora do rascunho preserva os três campos
      Dado solicitação de S em <situação>, com "Notebook", "3000.00", C1, histórico e G/D reais
      Quando S tenta diretamente trocar descrição por "Monitor", valor por "6000.01" e centro por C2
      Então a edição é recusada e a consulta nova conserva "Notebook", "3000.00", C1, situação e histórico; G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | aguardando_gestor | trânsito 1 |
        | aguardando_diretor | trânsito 2 |
        | aprovada | terminal |
        | cancelada | sem reabertura no escopo |

    Esquema do Cenário: [CT-03] Outra identidade não edita o rascunho de S
      Dado rascunho de S com "Notebook", "3000.00", C1 e G/D distintos disponíveis
      Quando <ator> tenta diretamente substituir descrição por "Alterada"
      Então a edição é recusada e a consulta conserva os três campos, rascunho e histórico; G/D não recebem e-mail
      Exemplos:
        | ator | # partição |
        | U | outro solicitante |
        | G | gestor sem posse |
        | D | diretor sem posse |

    Cenário: [CT-04] A edição apresenta os dados do rascunho ao dono
      Dado rascunho de S com "Notebook", "3000.00" e C1
      Quando S monta a página edit da solicitação
      Então o formulário apresenta "Notebook", "3000.00" e C1, com ação de salvar disponível

    Cenário: [CT-05] Salvar pelo componente grava a correção
      Dado rascunho de S com "Notebook", "3000.00" e C1
      Quando S salva pelo componente descrição "Monitor", valor "3000.01" e centro C2
      Então a consulta nova contém "Monitor", "3000.01", C2, solicitante S e rascunho
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | editar se é dono OU rascunho | CT-02, CT-03 | CT-02 conserva 3000.00 em trânsito; CT-03 conserva Notebook para U; o OR grava alterações |
| M-02 | barreira somente no formulário | CT-02, CT-03 | chamada direta deve preservar campos; o mutante grava 6000.01/Alterada |
| M-03 | correção grava descrição mas ignora valor/centro | CT-01, CT-05 | valor 3000.01 e C2 exigidos na consulta; o mutante mantém 3000.00/C1 |
| M-04 | formulário edit sem preencher dados do registro | CT-04 | os três valores do rascunho precisam constar; o mutante apresenta campo vazio/default |

## Regra R2 — Somente o solicitante exclui o rascunho

> RQ-03 · completo · matriz papel×ação, estado×operação, EP.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Somente o solicitante exclui o rascunho
    @premissa_mecanismo_exclusao
    Cenário: [CT-06] Excluir rascunho retira a solicitação das consultas
      Dado um rascunho de S e G/D reais disponíveis
      Quando S exclui a solicitação diretamente
      Então a consulta normal não encontra a solicitação e G/D não recebem e-mail

    Esquema do Cenário: [CT-07] Excluir fora do rascunho não apaga a solicitação
      Dado solicitação de S em <situação>, com campos, histórico e G/D reais disponíveis
      Quando S tenta excluí-la diretamente
      Então a operação é recusada; a consulta nova encontra a mesma situação, descrição, valor, centro e histórico; G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | aguardando_gestor | trânsito 1 |
        | aguardando_diretor | trânsito 2 |
        | aprovada | terminal |
        | cancelada | sem reabertura |

    Esquema do Cenário: [CT-08] Outra identidade não exclui o rascunho
      Dado rascunho de S com campos/histórico capturados e G/D distintos disponíveis
      Quando <ator> tenta excluir o rascunho diretamente
      Então a operação é recusada; a solicitação continua em rascunho com os mesmos campos/histórico; G/D não recebem e-mail
      Exemplos:
        | ator | # partição |
        | U | outro solicitante |
        | G | gestor |
        | D | diretor |

    @premissa_mecanismo_exclusao
    Esquema do Cenário: [CT-09] Editar ID ausente não recria solicitação
      Dado ID <alvo> sem solicitação alcançável, S autenticado, G/D reais e V em rascunho de S com Notebook/3000.00/C1 e histórico capturado, editável por S
      Quando S tenta editar diretamente esse ID para descrição "Intrusão"
      Então a operação é recusada; o ID continua ausente, V conserva Notebook/3000.00/C1, rascunho e histórico, não surgem decisões para o alvo e G/D não recebem e-mail
      Exemplos:
        | alvo | # partição |
        | removido por S em rascunho | excluído |
        | nunca existente | inexistente |

    @premissa_mecanismo_exclusao
    Esquema do Cenário: [CT-10] Excluir ID ausente não toca outro agregado
      Dado ID <alvo> sem solicitação alcançável, S autenticado, G/D reais e V em rascunho de S com campos/histórico capturados, excluível por S
      Quando S tenta excluir diretamente esse ID
      Então V continua alcançável com os mesmos campos/histórico, o alvo segue ausente, não surgem decisões para ele e G/D não recebem e-mail
      Exemplos:
        | alvo | # partição |
        | removido por S em rascunho | segunda exclusão |
        | nunca existente | inexistente |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-05 | excluir rascunho de qualquer usuário | CT-08 | registro de S permanece consultável para U; o mutante remove |
| M-06 | proteger edit depois do envio, esquecer delete | CT-07 | registro continua consultável em cada estado; o mutante o retira |
| M-07 | edição recria ID ausente | CT-09 | ID permanece ausente; o mutante recria com Intrusão; fallback para V editável gravaria Intrusão e também falha |
| M-08 | resolver delete ausente para primeiro registro disponível | CT-10 | V rascunho de S continua consultável; o mutante encontra V excluível pelo mesmo S e a remove |
| M-09 | excluir retorna sucesso sem retirar o registro | CT-06 | consulta normal não encontra o alvo; o mutante o devolve |

## Regra R3 — Enviar rascunho do solicitante inicia pelo gestor do centro

> RQ-04; A-02/A-10 · completo · estado×operação, identidade, EP.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Enviar rascunho do solicitante inicia pelo gestor do centro
    Esquema do Cenário: [CT-11] Primeiro envio chega ao gestor nas duas faixas
      Dado rascunho de S com valor <valor>, centro C1 cujo gestor é G e D distinto disponível
      Quando S envia diretamente
      Então a consulta nova mostra aguardando_gestor com o mesmo valor/centro, sem aprovação atribuída a D
      Exemplos:
        | valor | # partição |
        | 3000.00 | abaixo do limite literal |
        | 6000.00 | acima do limite literal |

    Esquema do Cenário: [CT-12] Enviar fora do rascunho não reinicia o fluxo
      Dado solicitação de S em <situação>, campos/histórico capturados e G/D reais disponíveis
      Quando S tenta enviar diretamente
      Então o envio é recusado; situação/campos persistidos e histórico ficam iguais; G/D não recebem novo e-mail
      Exemplos:
        | situação | # partição |
        | aguardando_gestor | envio repetido |
        | aguardando_diretor | próxima etapa |
        | aprovada | terminal |
        | cancelada | sem reabertura |

    Esquema do Cenário: [CT-13] Outra identidade não envia o rascunho de S
      Dado rascunho de S com campos/histórico capturados e G/D distintos disponíveis
      Quando <ator> tenta enviá-lo diretamente
      Então o envio é recusado; a consulta mantém rascunho e os campos/histórico; G/D não recebem e-mail
      Exemplos:
        | ator | # partição |
        | U | outro solicitante |
        | G | gestor |
        | D | diretor |

    Cenário: [CT-14] Centro sem gestor conserva o rascunho e informa a recusa
      Dado rascunho de S cujo centro está sem gestor, campos/histórico capturados, S/D reais disponíveis e coleta de e-mail/log iniciada após o preparo
      Quando S aciona enviar pelo componente
      Então continua em rascunho com campos/histórico iguais, há mensagem visível de recusa e warning correspondente à tentativa de envio dessa solicitação sem gestor, e S/D não recebem e-mail

    Cenário: [CT-15] Instância antiga não envia outra vez
      Dado solicitação persistida em aguardando_gestor após envio real por S, outra instância ainda com rascunho antigo, histórico capturado e G/D reais
      Quando S tenta enviar pela instância antiga
      Então a consulta nova continua aguardando_gestor com campos/histórico iguais e G/D não recebem e-mail adicional
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-10 | enviar compra alta diretamente ao diretor | CT-11 | linha 6000.00 exige aguardando_gestor; o mutante chega ao diretor |
| M-11 | checar só snapshot em memória antes do envio | CT-15 | sem histórico/e-mail adicional; o snapshot antigo produz segundo efeito |
| M-12 | enviar mesmo sem gestor | CT-14, CT-59 | componente conserva rascunho/mensagem e chamada direta também recusa; a variante com barreira só na UI põe em trânsito em CT-59 |
| M-13 | identidade só na action UI | CT-13 | envio direto por U conserva rascunho; o mutante avança |
| M-14 | permitir reenviar uma solicitação já em trânsito | CT-12 | linha aguardando_diretor conserva estado/histórico, sem novo aviso; o mutante reinicia |

## Regra R4 — Somente o gestor da etapa pendente aprova nela

> RQ-06; A-02/A-09 · completo · papel×ação, estado×operação.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Somente o gestor da etapa pendente aprova nela
    Cenário: [CT-16] O gestor decide sua etapa corrente
      Dado limite efetivo 5000.00, solicitação em aguardando_gestor com valor 3000.00 e gestor G distinto de S/D, todos disponíveis
      Quando G aprova diretamente
      Então a consulta nova mostra aprovada com exatamente uma decisão de aprovação da etapa de gestor atribuída a G, sem etapa pendente de diretor e sem e-mail para S/G/D

    Esquema do Cenário: [CT-17] Gestor não aprova fora da sua etapa
      Dado solicitação em <situação>, campos/histórico capturados e G/D reais disponíveis
      Quando G tenta aprovar diretamente como gestor
      Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | rascunho | antes do envio |
        | aguardando_diretor | gestor já decidiu |
        | aprovada | terminal |
        | cancelada | sem reabertura |

    Esquema do Cenário: [CT-18] Aprovar exige a identidade do gestor do centro
      Dado solicitação em aguardando_gestor, dono S, gestor G e diretor D distintos, H gestor de outro centro e histórico capturado
      Quando <ator> tenta aprovar diretamente a etapa de gestor
      Então a operação é recusada; permanece aguardando_gestor com campos/histórico iguais; G/D não recebem e-mail
      Exemplos:
        | ator | # partição |
        | S | dono não gestor |
        | H | gestor de outro centro |
        | D | diretor antecipado |
        | U | terceiro |

    Cenário: [CT-19] Solicitante que também é gestor decide a própria etapa
      Dado limite efetivo 5000.00, solicitação de valor 3000.00 em aguardando_gestor cujo solicitante S é gestor do centro, e D é outra pessoa disponível
      Quando S aprova diretamente como gestor
      Então a consulta nova mostra aprovada com exatamente uma decisão de aprovação da etapa de gestor atribuída a S, sem etapa pendente de diretor e sem e-mail para S/D
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-15 | autorizar qualquer gestor sem comparar centro | CT-18 | H conserva pendência/histórico; o mutante grava aprovação de H |
| M-16 | dar aprovação ao dono só pela posse | CT-18 | S distinto de G recebe recusa; o mutante registra S |
| M-17 | inventar segregação e proibir S=G | CT-19 | decisão atribuída a S; o mutante recusa A-09 dada |
| M-18 | aprovação só retorna sucesso sem persistir decisão | CT-16 | decisão persistida de G exigida, não só retorno |
| M-19 | aprovar como gestor em qualquer situação | CT-17 | rascunho/diretor/finais ficam iguais, sem decisão; o mutante grava aprovação |

## Regra R5 — Rejeição pelo aprovador corrente devolve para rascunho

> RQ-06/RQ-08; A-03/A-07/A-11 · completo · estado×operação, papel×ação.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Rejeição pelo aprovador corrente devolve para rascunho
    Esquema do Cenário: [CT-20] Rejeitar a etapa corrente devolve para correção
      Dado solicitação em <situação> com Notebook, 6000.00, C1, aprovador <ator> e S/G/D reais
      Quando <ator> rejeita diretamente com justificativa "Sem verba"
      Então a consulta mostra rascunho, conserva Notebook/6000.00/C1 e registra rejeição de <ator> com "Sem verba"; S/G/D não recebem e-mail
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | G | gestor |
        | aguardando_diretor | D | diretor por A-07 |

    Esquema do Cenário: [CT-21] Sem etapa pendente, rejeitar não altera o agregado
      Dado solicitação em <situação>, <ator> como G ou D, campos/histórico capturados e S/G/D reais
      Quando <ator> tenta rejeitar diretamente com "Sem verba"
      Então a operação é recusada; situação/campos persistidos e histórico ficam iguais; S/G/D não recebem e-mail
      Exemplos:
        | situação | ator | # partição |
        | rascunho | G | sem etapa / gestor |
        | rascunho | D | sem etapa / diretor |
        | aprovada | G | terminal / gestor |
        | aprovada | D | terminal / diretor |
        | cancelada | G | cancelada / gestor |
        | cancelada | D | cancelada / diretor |

    Esquema do Cenário: [CT-22] Cada verbo de rejeição exige o aprovador corrente
      Dado solicitação de C1 em <situação>, dono S, gestor G de C1, H gestor de C2, diretor D e U distintos, campos/histórico capturados
      Quando <ator> tenta rejeitar diretamente com "Sem verba"
      Então a operação é recusada; situação/campos e histórico permanecem iguais; S/G/D não recebem e-mail
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | S | dono não gestor |
        | aguardando_gestor | U | terceiro |
        | aguardando_gestor | H | gestor de outro centro, sem poder rejeitar C1 |
        | aguardando_gestor | D | diretor antecipado |
        | aguardando_diretor | S | dono não diretor |
        | aguardando_diretor | U | terceiro |
        | aguardando_diretor | G | anterior sem papel diretor |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-20 | conferir ator em aprovar, esquecer ou ampliar a identidade em rejeitar | CT-22 | U em ambas as etapas e H em aguardando_gestor conservam pendência/histórico; o mutante devolve ao rascunho |
| M-21 | rejeição vira estado terminal próprio | CT-20 | rascunho nas duas linhas; o mutante fica rejeitada |
| M-22 | só gestor rejeita, esquecer A-07 | CT-20 | D em aguardando_diretor devolve ao rascunho; o mutante recusa |
| M-23 | notificar S ao rejeitar por conveniência | CT-20 | nenhum e-mail para S real; o mutante envia aviso extra contrário a A-11 |
| M-24 | rejeitar mesmo sem pendência | CT-21 | rascunho/finais e histórico ficam iguais; o mutante cria decisão |

## Regra R6 — O reenvio corrigido começa nova passagem pelo gestor

> RQ-09/RQ-04 · completo · 2-switch, estado×operação.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: O reenvio corrigido começa nova passagem pelo gestor
    Cenário: [CT-23] Corrigir o centro e reenviar usa o gestor atual
      Dado solicitação em rascunho após rejeição real de G, S corrigiu descrição para Monitor e centro para C2 cujo gestor é H, S/G/H/D são distintos e reais, e a coleta de e-mail da nova etapa começa após esse preparo
      Quando S envia novamente diretamente
      Então a consulta nova mostra aguardando_gestor, Monitor e C2, e o identificador do gestor da etapa corrente é H, não G; H recebe exatamente um aviso mail dessa solicitação pela nova etapa e G/S/D não recebem aviso dessa ação

    Cenário: [CT-24] Reenvio após rejeição de diretor não reutiliza o aval antigo
      Dado solicitação em rascunho após enviar, aprovação real de G e rejeição real de D, corrigida por S para Monitor com valor persistido 6000.00
      Quando S envia novamente diretamente
      Então a consulta nova mostra aguardando_gestor, Monitor e 6000.00; o aval antigo de G não a deixa em aguardando_diretor nem aprovada

    Cenário: [CT-25] Corrigir não se transfere ao aprovador que rejeitou
      Dado solicitação em rascunho após rejeição real de G, pertence a S, descrição Notebook, histórico da rejeição e G/D distintos disponíveis
      Quando G tenta corrigir diretamente a descrição para Monitor
      Então a operação é recusada; a consulta mantém Notebook, rascunho e histórico da rejeição; G/D não recebem e-mail
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-25 | reutilizar aval de G no novo ciclo após rejeição de D | CT-24 | aguardando_gestor, não diretor/aprovada |
| M-26 | usar gestor do primeiro envio após mudar centro | CT-23 | identificador corrente H, não G; centro corrigido C2 |
| M-27 | permitir correção ao aprovador que devolveu | CT-25 | Notebook permanece; o mutante grava Monitor por G |

## Regra R7 — Aprovação final impede nova decisão e antecipação do diretor

> RQ-10/RQ-04; A-03/A-05 · completo · estado×operação, papel×ação.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Aprovação final impede nova decisão e antecipação do diretor
    Esquema do Cenário: [CT-26] Diretor não aprova antes do gestor nem depois do encerramento
      Dado solicitação em <situação>, S/G/D distintos disponíveis e campos/histórico capturados
      Quando D tenta aprovar diretamente
      Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | rascunho | antes do envio |
        | aguardando_gestor | gestor primeiro |
        | aprovada | terminal final |
        | cancelada | sem reabertura |

    Cenário: [CT-27] Diretor não rejeita solicitação já aprovada
      Dado solicitação em aprovada após transições reais, com S/G/D reais e campos/histórico capturados
      Quando D tenta rejeitar diretamente com "Sem verba"
      Então a operação é recusada; a consulta nova continua aprovada com os mesmos campos/histórico; S/G/D não recebem e-mail
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-28 | conferir papel diretor sem conferir etapa | CT-26 | linha aguardando_gestor fica inalterada; o mutante decide antes de G |
| M-29 | impedir edit depois de aprovada, permitir rejeitar | CT-27 | aprovada/histórico ficam iguais; o mutante volta ao rascunho |
| M-30 | aprovar outra vez porque papel continua válido | CT-17, CT-26 | linha aprovada exige histórico igual; o mutante adiciona aprovação |

## Regra R8 — Só o solicitante cancela enquanto há etapa pendente

> RQ-11; A-06 · completo · estado×operação, identidade, interleaving.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Só o solicitante cancela enquanto há etapa pendente
    Esquema do Cenário: [CT-28] O solicitante cancela em cada etapa de trânsito
      Dado solicitação de S em <situação>, campos/histórico capturados e G/D reais disponíveis
      Quando S cancela diretamente
      Então a consulta nova mostra cancelada com os mesmos campos/histórico e S/G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | aguardando_gestor | antes do gestor |
        | aguardando_diretor | antes da aprovação final |

    Esquema do Cenário: [CT-29] Cancelar fora do trânsito conserva a situação
      Dado solicitação de S em <situação>, campos/histórico capturados e G/D reais
      Quando S tenta cancelar diretamente
      Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; S/G/D não recebem e-mail
      Exemplos:
        | situação | # partição |
        | rascunho | A-06 usa excluir |
        | aprovada | aprovação final |
        | cancelada | cancelamento repetido |

    Esquema do Cenário: [CT-30] Aprovador e terceiro não cancelam solicitação de S
      Dado solicitação de S em <situação>, campos/histórico capturados e G/D distintos disponíveis
      Quando <ator> tenta cancelar diretamente
      Então a operação é recusada; a consulta mantém situação/campos e histórico; S/G/D não recebem e-mail
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | G | gestor |
        | aguardando_gestor | D | diretor |
        | aguardando_gestor | U | terceiro |
        | aguardando_diretor | G | anterior |
        | aguardando_diretor | D | corrente |
        | aguardando_diretor | U | terceiro |

    Cenário: [CT-31] Decisão carregada antes do cancelamento não desfaz o estado persistido
      Dado G carregou solicitação em aguardando_gestor, depois S cancelou por transição real; consulta atual mostra cancelada, com campos/histórico capturados e G/D reais
      Quando G rejeita diretamente usando a instância antiga e justificativa "Sem verba"
      Então a operação é recusada; consulta nova continua cancelada com os mesmos campos/histórico; S/G/D não recebem e-mail
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-31 | cancelar rascunho por leitura literal sem A-06 | CT-29 | linha rascunho exige rascunho, não cancelada |
| M-32 | permitir cancelar por qualquer aprovador | CT-30 | situação permanece pendente para G/D; o mutante cancela |
| M-33 | conferir só estado carregado e sobrescrever concorrente | CT-31 | cancelada persistida; o mutante volta a rascunho com rejeição |
| M-34 | permitir cancelar somente enquanto aguarda gestor | CT-28 | linha aguardando_diretor exige cancelada; o mutante recusa |

## Regra R9 — Usuário comum não administra centros de custo

> RQ-04; A-08 · padrão · papel×ação e ação efetiva.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Usuário comum não administra centros de custo
    Esquema do Cenário: [CT-32] panel_user não grava administração fora da tela
      Dado U com apenas panel_user, C1 existente com gestor G, H real e solicitação de S usando C1
      Quando U tenta diretamente <operação> com gestor pretendido H
      Então a operação é recusada; C1 conserva nome/gestor G, nenhum centro adicional é criado ou removido e a solicitação conserva C1 e os campos
      Exemplos:
        | operação | # partição |
        | criar centro novo | create administrativo |
        | editar gestor de C1 para H | escalada no edit |
        | excluir C1 | delete administrativo |

    Cenário: [CT-33] Componente não permite panel_user mudar o gestor
      Dado U com apenas panel_user, C1 chamado Tecnologia com gestor G e H real
      Quando U tenta salvar gestor H pela página edit de C1
      Então acesso/gravação é recusado; consulta nova mantém Tecnologia e G, sem centro adicional
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-35 | entregar permissões de todos os Resources novos ao panel_user | CT-32, CT-33 | C1.gestor continua G, não H |
| M-36 | ocultar menu sem barrar ação de escrita | CT-32 | ação direta recusada; o mutante grava H |
| M-37 | remover create/edit, esquecer delete administrativo | CT-32 | linha excluir conserva C1; o mutante remove |

## Regra R10 — A tela oferece as operações fechadas de quem pode agir

> RQ-02/03/04/06/08/11; A-07 · padrão · decisão e EP estado/persona.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: A tela oferece as operações fechadas de quem pode agir
    Esquema do Cenário: [CT-34] Affordance segue identidade e situação
      Dado solicitação em <situação>, S/G/D distintos e painel configurado para <ator>
      Quando <ator> monta a listagem da solicitação
      Então a ação <ação> está <visibilidade> para o registro
      Exemplos:
        | situação | ator | ação | visibilidade | # partição |
        | rascunho | S | editar | visível | dono/rascunho |
        | rascunho | S | excluir | visível | dono/rascunho |
        | rascunho | S | enviar | visível | dono/rascunho |
        | rascunho | G | editar | oculta | sem posse |
        | rascunho | G | excluir | oculta | sem posse |
        | rascunho | G | enviar | oculta | sem posse |
        | aguardando_gestor | G | aprovar | visível | corrente |
        | aguardando_gestor | G | rejeitar | visível | corrente |
        | aguardando_gestor | S | aprovar | oculta | dono não gestor |
        | aguardando_gestor | S | rejeitar | oculta | dono não gestor |
        | aguardando_gestor | S | cancelar | visível | dono/trânsito 1 |
        | aguardando_gestor | D | cancelar | oculta | outro ator |
        | aguardando_diretor | S | cancelar | visível | dono/trânsito 2 |
        | aguardando_diretor | D | rejeitar | visível | A-07 |
        | aguardando_diretor | G | rejeitar | oculta | participante anterior sem papel diretor |
        | aprovada | S | editar | oculta | terminal |
        | aprovada | S | excluir | oculta | terminal |
        | aprovada | S | cancelar | oculta | terminal |
        | cancelada | S | enviar | oculta | sem reabertura |

    Cenário: [CT-35] Rejeitar pelo componente devolve para correção
      Dado solicitação em aguardando_gestor, S/G/D distintos reais, Notebook, 3000.00 e C1
      Quando G confirma rejeitar pelo componente com "Sem verba"
      Então consulta nova mostra rascunho, Notebook/3000.00/C1 e rejeição de G com "Sem verba"; S/G/D não recebem e-mail

    Esquema do Cenário: [CT-36] Confirmar envio/cancelamento grava a transição correspondente
      Dado solicitação de S em <inicial>, com campos/histórico capturados, G gestor do centro, S/G/D/H distintos e reais e coleta de e-mail iniciada depois do preparo
      Quando S confirma <ação> pelo componente
      Então consulta nova mostra <final> com descrição/valor/centro/solicitante originais, e os e-mails dessa confirmação satisfazem <avisos>, sem aviso para S/D/H
      Exemplos:
        | inicial | ação | final | avisos | # partição |
        | rascunho | enviar | aguardando_gestor | G recebe exatamente um mail dessa solicitação | envio |
        | aguardando_gestor | cancelar | cancelada | G não recebe aviso | etapa 1 |
        | aguardando_diretor | cancelar | cancelada | G não recebe aviso | etapa 2 |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-38 | visibilidade verifica só estado, não identidade | CT-34 | editar/excluir/enviar ocultos para G em rascunho; aprovar/rejeitar ocultos para S pendente |
| M-39 | action retorna sucesso sem chamar transição | CT-35, CT-36 | rascunho/aguardando_gestor/cancelada persistidos exigidos; mutante conserva inicial |

## Regra R11 — Solicitação removida não volta a funcionar em transições

> RQ-03/04/06/11 · completo · EP por operação, identidade do agregado.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Solicitação removida não volta a funcionar em transições
    @premissa_mecanismo_exclusao
    Esquema do Cenário: [CT-37] Transições sobre ID removido não produzem efeitos em outro registro
      Dado alvo de S excluído ainda em rascunho por transição real, V de S em <situação_V> com C1/G e campos/histórico capturados, G/D reais e <ator> autorizado a executar <operação> em V
      Quando <ator> tenta <operação> diretamente no ID removido
      Então a operação é recusada; alvo continua ausente, V conserva situação/campos/histórico, nenhuma decisão é criada para o alvo e G/D não recebem e-mail
      Exemplos:
        | operação | situação_V | ator | # partição |
        | enviar | rascunho | S | V seria enviada a G |
        | aprovar como gestor | aguardando_gestor | G | V de 3000.00 seria aprovada com limite 5000.00 |
        | rejeitar como gestor com Sem verba | aguardando_gestor | G | V voltaria ao rascunho com rejeição |
        | rejeitar como diretor com Sem verba | aguardando_diretor | D | V voltaria ao rascunho com rejeição |
        | cancelar | aguardando_gestor | S | V seria cancelada |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-40 | objeto antigo removido cria decisão órfã | CT-37 | alvo ausente e sem decisão após cada transição; mutante grava efeito órfão |
| M-41 | ID ausente resolve para primeiro registro da lista | CT-37 | V é alterável pelo mesmo ator em cada linha; o mutante envia/aprova/rejeita/cancela V, divergindo da situação/histórico capturados |
| M-42 | notificar antes de descobrir que registro foi removido | CT-37 | destinatários reais G/D não recebem e-mail; mutante envia antes de recusar |

## Regra R12 — O solicitante cria solicitação com os três dados válidos

> RQ-01; A-01 · completo · EP positiva e rastreio da gravação. Limites inválidos e retry permanecem Q?1/Q?7.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: O solicitante cria solicitação com os três dados válidos
    Cenário: [CT-38] Criação válida fora do componente persiste os dados de S
      Dado S autorizado a solicitar e C1 existente na organização com gestor G, sem solicitação resultante ainda criada
      Quando S cria pela operação do solicitante fora do componente, com descrição Notebook, valor 3000.00 e centro C1
      Então uma consulta nova encontra a solicitação criada com solicitante S, Notebook, 3000.00, C1 e rascunho

    Cenário: [CT-39] A tela de criação oferece os três campos ao solicitante
      Dado S autorizado a solicitar e centro C1 existente, sem solicitação a editar
      Quando S monta a página create da solicitação
      Então o formulário apresenta descrição, valor e centro de custo, com a operação de criar disponível

    Cenário: [CT-40] Criar pelo componente grava todos os dados válidos
      Dado S autorizado a solicitar e centro C1 existente com gestor G, sem solicitação resultante ainda criada
      Quando S preenche Notebook, 3000.00 e C1 e confirma criar pelo componente
      Então a consulta nova encontra a solicitação criada com solicitante S, Notebook, 3000.00, C1 e rascunho
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-43 | operação de criação sempre recusa, mas fixture Model::create funciona | CT-38, CT-40 | a operação real deve produzir registro de S com os três dados, não apenas o preparo |
| M-44 | criação persiste outro solicitante ou já põe a compra em trânsito | CT-38, CT-40 | S e rascunho persistidos são exigidos, não outro dono/situação |
| M-45 | componente ignora valor ou centro no create | CT-40 | 3000.00 e C1 na consulta nova; o mutante usa default/null |
| M-46 | página create não oferece um dos campos necessários | CT-39 | os três campos e operação de criar precisam estar disponíveis |

## Regra R13 — Acima da alçada configurada exige diretor depois do gestor

> RQ-05; A-03/A-04 · completo · BVA 3-valores, decisão e variação do discriminante. Pessoas distintas e diretor existente; combinações/zero diretores não respondidos.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Acima da alçada configurada exige diretor depois do gestor
    Esquema do Cenário: [CT-41] A fronteira literal decide o destino após o gestor
      Dado configuração de fábrica efetivamente lida em 5000.00 sem override nem chave do ambiente de teste, S/G/D distintos e solicitação de <valor> em aguardando_gestor
      Quando G aprova diretamente
      Então a consulta nova mostra <destino>, conserva <valor> e registra exatamente uma aprovação de gestor por G; a etapa pendente de diretor é <pendência>
      Exemplos:
        | valor | destino | pendência | # borda |
        | 4999.99 | aprovada | ausente | borda−0.01 |
        | 5000.00 | aprovada | ausente | borda literal |
        | 5000.01 | aguardando_diretor | presente | borda+0.01 |

    Cenário: [CT-42] O diretor encerra a segunda etapa depois do gestor
      Dado limite efetivo 5000.00 e solicitação de 6000.00 em aguardando_diretor obtida por envio e aprovação reais de G, com S/G/D distintos e D diretor dessa organização
      Quando D aprova diretamente
      Então a consulta nova mostra aprovada, conserva 6000.00 e contém uma aprovação de gestor por G seguida de uma aprovação de diretor por D, sem etapa pendente e sem e-mail para S/G/D

    Cenário: [CT-43] A mudança de configuração muda a faixa que exige diretor
      Dado kit.compras.limite_diretor efetivamente lido em 7000.00, solicitação de 6000.00 em aguardando_gestor e S/G/D distintos disponíveis
      Quando G aprova diretamente
      Então a consulta nova mostra aprovada com aprovação de gestor por G, sem etapa pendente de diretor e sem e-mail para S/G/D
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-47 | comparar valor >= limite em vez de > | CT-41 | 5000.00 deve terminar aprovada sem diretor; o mutante aguarda diretor |
| M-48 | encerrar sempre após o gestor | CT-41 | 5000.01 exige aguardando_diretor com pendência; o mutante aprova final |
| M-49 | aprovação de diretor grava decisão mas mantém pendência | CT-42 | aprovada e nenhuma pendência, além de G/D em ordem; o mutante conserva aguardando_diretor |
| M-50 | ignorar configuração e comparar sempre com literal 5000.00 | CT-43 | 6000.00 com limite 7000.00 termina aprovada; literal errado aguarda diretor |
| M-51 | aprovação de gestor grava decisão sem mudar o estado na faixa inferior | CT-16, CT-19, CT-41 | consulta nova deve mostrar aprovada para 3000.00 e para bordas inferiores; decisão sozinha não basta |

## Regra R14 — Sem justificativa não existe rejeição válida

> RQ-07; A-07 · completo · EP ausência/presença e rastreio de não-efeito. A ausência é a parte determinada; teto/espaços/normalização não respondidos.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Sem justificativa não existe rejeição válida
    Esquema do Cenário: [CT-44] Ausência de justificativa é recusada fora do formulário
      Dado solicitação em <situação> para seu aprovador corrente <ator>, situação/campos/histórico capturados e S/G/D reais disponíveis
      Quando <ator> tenta rejeitar pela operação de domínio sem fornecer justificativa
      Então a rejeição é recusada; situação/campos persistidos e histórico continuam iguais, sem nova decisão de rejeição e sem e-mail para S/G/D
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | G | ausência na etapa de gestor |
        | aguardando_diretor | D | ausência na etapa de diretor |

    Esquema do Cenário: [CT-45] O formulário de rejeição não grava sem justificativa
      Dado solicitação em <situação> para seu aprovador <ator>, campos/histórico capturados e S/G/D reais disponíveis
      Quando <ator> confirma rejeitar no componente sem preencher justificativa
      Então o formulário indica falta de justificativa, situação/campos persistidos e histórico continuam iguais, sem nova rejeição e sem e-mail para S/G/D
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | G | formulário/gestor |
        | aguardando_diretor | D | formulário/diretor |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-52 | obrigatoriedade somente na UI | CT-44 | chamada de domínio sem justificativa conserva situação/histórico; o mutante rejeita |
| M-53 | gestor rejeita mesmo sem justificativa | CT-44, CT-45 | linha gestor mantém aguardando_gestor e nenhuma rejeição nova |
| M-54 | conferir justificativa do gestor, esquecer diretor | CT-44, CT-45 | linha diretor mantém aguardando_diretor e nenhuma rejeição nova |

## Regra R15 — A listagem e o detalhe mostram o status atual

> RQ-12; A-12 · padrão · EP exaustiva por situação em cada superfície. Acesso explicitamente autorizado no Dado, sem decidir quem tem acesso.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: A listagem e o detalhe mostram o status atual
    Esquema do Cenário: [CT-46] A listagem apresenta a situação da solicitação
      Dado uma solicitação em <situação> por transições reais e observador O com acesso autorizado a ela
      Quando O monta a listagem pelo componente
      Então a linha dessa solicitação apresenta o status atual <situação>, sem substituí-lo pelo de outra etapa
      Exemplos:
        | situação | # partição |
        | rascunho | estado inicial |
        | aguardando_gestor | primeira etapa |
        | aguardando_diretor | segunda etapa |
        | aprovada | aprovação final |
        | cancelada | cancelamento |

    Esquema do Cenário: [CT-47] O detalhe apresenta a situação da solicitação
      Dado uma solicitação em <situação> por transições reais e observador O com acesso autorizado a ela
      Quando O monta o detalhe pelo componente
      Então o detalhe dessa solicitação apresenta o status atual <situação>, sem substituí-lo pelo de outra etapa
      Exemplos:
        | situação | # partição |
        | rascunho | estado inicial |
        | aguardando_gestor | primeira etapa |
        | aguardando_diretor | segunda etapa |
        | aprovada | aprovação final |
        | cancelada | cancelamento |
```

Asserção sobre o significado concreto da situação da solicitação; nomes internos localizam os estados, não impõem markup/cor/rótulo incidental do PRD. Os dois cenários montam a operação correspondente, sem transferir evidência de lista para detalhe.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-55 | retirar status da listagem ou do detalhe | CT-46, CT-47 | status da solicitação deve estar apresentado em cada superfície; ausência falha |
| M-56 | apresentar Aprovada quando ainda falta o diretor | CT-46, CT-47 | linha aguardando_diretor exige pendência de diretor, não aprovação final |
| M-57 | detalhe apresenta rascunho fixo apesar das transições | CT-47 | estados gestor/diretor/finais devem constar concretamente; rascunho fixo falha |

## Regra R16 — O histórico da visualização identifica quem aprovou cada etapa

> RQ-13; A-12 · padrão · rastreio de decisão até apresentação. Acesso autorizado dado, recorte histórico ainda Q?5.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: O histórico da visualização identifica quem aprovou cada etapa
    Cenário: [CT-48] O detalhe atribui as duas etapas aos respectivos aprovadores
      Dado solicitação aprovada de 6000.00 com limite 5000.00, aprovações reais de G na etapa de gestor e D distinto na etapa de diretor, posterior mudança administrativa autorizada do gestor atual do centro para H distinto de G/D, e acesso autorizado de O
      Quando O monta o detalhe pelo componente
      Então o histórico dessa solicitação apresenta G na aprovação histórica de gestor e D na aprovação de diretor, com ambas as etapas, sem atribuir a mesma pessoa às duas e sem atribuir a H uma aprovação que ele não decidiu
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-58 | persistir decisões mas omitir histórico visual | CT-48 | G/gestor e D/diretor precisam ser apresentados, não só gravados |
| M-59 | mostrar o último aprovador D como autor das duas etapas | CT-48 | gestor exige G distinto de D; o mutante mostra D para ambos |
| M-60 | apresentar só a aprovação mais recente | CT-48 | ambas as etapas com seus autores são exigidas; só D não basta |

## Regra R17 — O próximo aprovador existente recebe e-mail dessa etapa

> RQ-14; A-02/A-03/A-11 · completo · rastreio do efeito exato, destinatários 1/N, ausência e uma vez. Sem decidir link, transporte SMTP ou zero diretores.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: O próximo aprovador existente recebe e-mail dessa etapa
    Esquema do Cenário: [CT-49] Enviar notifica somente o gestor pelo canal e-mail
      Dado rascunho de S com valor <valor>, C1 cujo gestor é G, e S/H/D distintos reais além de G, com efeitos observados após o preparo
      Quando S envia diretamente
      Então consulta nova mostra aguardando_gestor e G recebe exatamente uma notificação dessa solicitação pelo canal mail; S/H/D não recebem aviso dessa etapa
      Exemplos:
        | valor | # partição |
        | 3000.00 | abaixo do limite |
        | 6000.00 | acima do limite, ainda gestor primeiro |

    Esquema do Cenário: [CT-50] O aval do gestor notifica todos os diretores da organização
      Dado limite 5000.00, solicitação de 6000.00 em aguardando_gestor na organização A, S/G distintos, diretores <diretores_A> em A e diretor X real apenas na organização B
      Quando G aprova diretamente
      Então consulta nova mostra aguardando_diretor e cada usuário de <diretores_A> recebe exatamente uma notificação dessa solicitação pelo canal mail; S/G/X não recebem aviso dessa etapa
      Exemplos:
        | diretores_A | # partição |
        | D1 | cardinalidade 1 |
        | D1 e D2 | cardinalidade N |

    Cenário: [CT-51] Retry de envio mantém uma só notificação ao gestor
      Dado a mesma solicitação já persistida em aguardando_gestor após envio real por S, exatamente um aviso mail capturado para G, instância antiga ainda com rascunho e S/G/H/D reais
      Quando S repete enviar pela instância antiga
      Então a consulta nova continua aguardando_gestor com campos/histórico iguais, G mantém exatamente um aviso mail dessa solicitação no total e S/H/D continuam sem aviso
```

Mecanismo de teste: Notification::fake registra também canais; materializar as contagens por solicitação/destinatário e canal mail. Não basta assertar que qualquer notificação foi capturada. O fake prova a intenção de despacho, sem declarar SMTP entregue ou morte de mutantes medida. A operação sem próximo aprovador continua coberta pelos não-efeitos CT-16/19/20/28, com pessoas reais no Dado; ausência de diretor Q?4 não substitui essas fixtures.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | não despachar o aviso ao gestor ou ao diretor | CT-49, CT-50 | exatamente um aviso mail por destinatário corrente, não zero |
| M-62 | notificar somente por database em vez de e-mail | CT-49, CT-50 | canal mail exigido, não captura genérica |
| M-63 | avisar apenas o primeiro diretor da coleção | CT-50 | linha N exige um mail para D1 e um para D2 |
| M-64 | duplicar aviso ou reenviar no retry stale | CT-49, CT-51 | G recebe/mantém exatamente um aviso total; duplicação produz dois |
| M-65 | buscar diretores globalmente sem organização | CT-50 | X real de B recebe zero, D1/D2 de A recebem um cada |

## Regra R18 — A administração autorizada mantém centros válidos

**Perfil:** padrão (administração 2×3). **Origem:** A-01/A-08, RQ-01/RQ-04. **Técnica formal:** partição positiva papel×operação, CRUD criar/editar/excluir. A possui autorização de administração do app na organização T, conforme A-08; o teste não escolhe um nome de papel novo. Valores válidos de nome e gestor não resolvem teto nem domínio de Q?1. Exclusão usa centro sem dependências e afirma ausência na consulta normal, sem impor armazenamento físico.

```gherkin
  Funcionalidade: Administração autorizada de centros
    Esquema do Cenário: [CT-52] CRUD administrativo válido funciona fora do formulário
      Dado A autorizado à administração do app em T, G/H usuários de T, outro centro Estoque com gestor G em T e <preparo> sem solicitação associada, distinto de Estoque
      Quando A executa <operação> de centro fora do formulário com <dados>
      Então a consulta nova satisfaz <resultado>
      Exemplos:
        | preparo | operação | dados | resultado | # partição |
        | nenhum centro Tecnologia cadastrado | criar | nome Tecnologia e gestor G | existe centro Tecnologia com gestor G pertencente a T | criação |
        | centro Tecnologia com gestor G pertencente a T | editar | nome Infra e gestor H | o mesmo centro tem nome Infra, gestor H e continua pertencendo a T | correção |
        | centro Tecnologia com gestor G pertencente a T | excluir | ID desse centro | esse centro não aparece na consulta normal e Estoque permanece com gestor G em T | exclusão |
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-66 | recusar toda criação administrativa mesmo com autorização | CT-52, CT-54 | centro Tecnologia/G/T deve existir após a criação real |
| M-67 | edição administrativa ignora mudança de nome ou gestor | CT-52, CT-54 | consulta exige Infra/H no mesmo ID, conservando T |
| M-68 | exclusão administrativa retorna sem remover centro sem dependências | CT-52, CT-54 | alvo deixa a consulta normal; o mutante mantém o alvo |

## Regra R19 — As telas administrativas permitem visita e gravação válidas

**Perfil:** padrão (UI/administração 2×3). **Origem:** A-01/A-08, RQ-01/RQ-04. **Técnica formal:** partição criar/editar na visita, criar/editar/excluir na gravação. Grupo Administração UI; costura proposta de componente Livewire/Filament já existente. Não exige browser. Confirmada vazia.

```gherkin
  Funcionalidade: Superfície administrativa de centros
    Esquema do Cenário: [CT-53] Administrador visita os formulários de centro
      Dado A autorizado à administração do app em T, G usuário de T e <preparo>
      Quando A monta o formulário de <operação> de centro pelo componente
      Então encontra campos de nome e gestor e a confirmação da operação, com <conteúdo>
      Exemplos:
        | preparo | operação | conteúdo | # partição |
        | centro ainda não criado | criar | controles disponíveis para informar nome e gestor | criação |
        | centro Tecnologia com gestor G em T | editar | nome Tecnologia e gestor G carregados | edição |

    Esquema do Cenário: [CT-54] Confirmar CRUD de centro no painel persiste o efeito
      Dado A autorizado à administração do app em T, G/H usuários de T, outro centro Estoque com gestor G em T e <preparo> sem solicitação associada, distinto de Estoque
      Quando A confirma <operação> de centro pelo componente com <dados>
      Então a consulta nova satisfaz <resultado>
      Exemplos:
        | preparo | operação | dados | resultado | # partição |
        | nenhum centro Tecnologia cadastrado | criar | nome Tecnologia e gestor G | existe centro Tecnologia com gestor G pertencente a T | criação |
        | centro Tecnologia com gestor G pertencente a T | editar | nome Infra e gestor H | o mesmo centro tem nome Infra, gestor H e continua pertencendo a T | edição |
        | centro Tecnologia com gestor G pertencente a T | excluir | ID desse centro | esse centro não aparece na consulta normal e Estoque permanece com gestor G em T | exclusão |
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-69 | omitir campos de nome/gestor no formulário de criar ou editar | CT-53 | visita exige controles presentes e os dados existentes na edição |
| M-70 | callback de criar/editar retorna sucesso sem gravar centro | CT-54 | criação/edição exigem consulta nova com dados concretos |
| M-71 | callback de excluir apenas fecha a confirmação | CT-54 | centro sem dependências deve deixar a consulta normal |

## Regra R20 — Qualquer diretor elegível decide e a primeira decisão resolve

**Perfil:** completo (autorização/fluxo 3×3). **Origem:** RQ-05/RQ-06/RQ-10, A-03/A-05/A-07. **Técnica formal:** partição de identidade dentro de cardinalidade N; estado×evento com snapshot antigo. S/G/D1/D2 distintos; D1 e D2 possuem papel diretor em T. D1 ocupa a primeira posição na coleção preparada para a sonda e D2 não; isso discrimina seleção indevida de uma só pessoa, sem estabelecer ordenação de produto. A corrida física não foi executada: CT-56 discrimina a leitura de snapshot antigo após decisão real persistida.

```gherkin
  Funcionalidade: Diretoria plural e primeira decisão
    Esquema do Cenário: [CT-55] Diretor além do primeiro decide a etapa corrente
      Dado compra de S em T de 6000.00 com limite 5000.00 em aguardando_diretor após envio e aprovação reais de G, e D1/D2 diretores distintos com D2 fora da primeira posição da coleção preparada
      Quando D2 executa <operação> diretamente, informando Sem verba na rejeição
      Então a consulta nova mostra <final>, preserva os campos da compra e a aprovação de G, grava exatamente uma decisão da etapa diretor de autoria D2 com <conteúdo>, não grava decisão de D1 e não envia e-mail a S/G/D1/D2
      Exemplos:
        | operação | final | conteúdo | # partição |
        | aprovar como diretor | aprovada | aprovação | elegibilidade da segunda pessoa |
        | rejeitar como diretor | rascunho | rejeição com Sem verba | rejeição elegível da segunda pessoa |

    Esquema do Cenário: [CT-56] Snapshot de outro diretor não decide etapa já resolvida
      Dado compra de S em T de 6000.00 com limite 5000.00 em aguardando_diretor após aprovação real de G, D1/D2 diretores elegíveis de T distintos de S/G, D2 carregou essa etapa elegível e depois D1 realizou <primeira_decisão>, com consulta nova em <final> e campos/histórico capturados após D1
      Quando D2 tenta <segunda_decisão> pela instância antiga, informando Sem verba na rejeição
      Então a operação é recusada, a consulta permanece em <final> com campos/histórico capturados, conserva apenas a decisão de diretor de D1 sem decisão de D2 e S/G/D1/D2 não recebem e-mail dessa tentativa
      Exemplos:
        | primeira_decisão | final | segunda_decisão | # partição |
        | aprovar como diretor | aprovada | aprovar como diretor | nova aprovação após aprovação |
        | aprovar como diretor | aprovada | rejeitar como diretor | nova rejeição após aprovação |
        | rejeitar como diretor com Sem verba | rascunho | aprovar como diretor | nova aprovação após devolução |
        | rejeitar como diretor com Sem verba | rascunho | rejeitar como diretor | nova rejeição após devolução |
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-72 | só primeiro diretor da coleção pode aprovar | CT-55 | D2 deve aprovar e ser autor, embora não seja o primeiro |
| M-73 | só primeiro diretor da coleção pode rejeitar | CT-55 | D2 deve devolver ao rascunho com sua rejeição e Sem verba |
| M-74 | decisão elegível de D2 fica atribuída a D1 | CT-55 | identidade da decisão de diretor é D2, sem decisão de D1 |
| M-75 | aprovação de diretor valida apenas estado do snapshot | CT-56 | segunda aprovação stale é recusada sem nova decisão de D2 |
| M-76 | rejeição de diretor valida apenas estado do snapshot | CT-56 | segunda rejeição stale conserva estado e histórico resolvidos por D1 |

## Regra R21 — O histórico apresenta o conteúdo e a autoria histórica dados no 00

**Perfil:** padrão (apresentação 2×2). **Origem:** RQ-12/RQ-13, A-12. **Técnica formal:** partição por estado/quantidade de etapas e rastreio do instante e justificativa conhecidos; identidade histórica contra papel atual. CT-48 reescrito integra esta regra transversal com R16. Acesso de O dado como autorizado; Q?5 continua sem resposta. O instante é comparado por significado na apresentação configurada, sem exigir um formato ou fuso específico não dados no 00.

```gherkin
  Funcionalidade: Conteúdo do histórico autorizado
    Esquema do Cenário: [CT-57] Aprovação única é visível antes ou ao final do fluxo
      Dado compra de S com valor <valor> e limite 5000.00 após envio e aprovação reais de G, em <situação>, D distinto disponível sem decisão e O com acesso autorizado
      Quando O monta o detalhe pelo componente
      Então o histórico apresenta G como autor da aprovação da etapa gestor dessa solicitação e não inventa uma aprovação de diretor inexistente
      Exemplos:
        | valor | situação | # partição |
        | 6000.00 | aguardando_diretor | aprovação de gestor enquanto aguarda diretor |
        | 3000.00 | aprovada | aprovação final somente do gestor |

    Esquema do Cenário: [CT-58] Rejeição apresentada conserva autor, instante e justificativa
      Dado S/G/D distintos, G gestor do centro, D diretor da organização e compra de S após <preparo> e rejeição real de <ator> na etapa <etapa> com Sem verba no instante conhecido 2026-10-09T15:30:00Z, em rascunho, com histórico persistido desse instante e O com acesso autorizado
      Quando O monta o detalhe pelo componente
      Então o histórico da etapa <etapa> apresenta <ator>, Sem verba e o instante correspondente a 2026-10-09T15:30:00Z na apresentação configurada, e não omite nem substitui esses dados da decisão
      Exemplos:
        | ator | etapa | preparo | # partição |
        | G | gestor | envio real de S à etapa gestor | devolução pelo gestor |
        | D | diretor | envio real de S e aprovação real de G acima da alçada | devolução após aprovação real de G |
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-77 | mostrar histórico apenas com duas aprovações finais | CT-57 | aprovação de G é visível tanto no trânsito ao diretor quanto no final com uma etapa |
| M-78 | omitir instante ou justificativa da rejeição na visualização | CT-58 | Sem verba e o instante conhecido são apresentados, não só persistidos |
| M-79 | autor do histórico vem do gestor atual do centro | CT-48 | após mudança autorizada para H, aprovação histórica permanece de G e não de H |

## Regra R22 — Ausência de gestor falha fechado também fora do formulário

**Perfil:** completo (fluxo 3×3). **Origem:** RQ-04, A-10. **Técnica formal:** partição gestor ausente, fronteiras componente/operação e rastreio de efeitos. CT-14 reescrito mantém mensagem da superfície e exige warning; CT-59 acrescenta a barreira fora do formulário. Coleta de log observa o intervalo da tentativa e o motivo ausência de gestor, sem impor texto exato, driver ou formato de payload. Warning sem relação com a tentativa não serve de matador.

```gherkin
  Funcionalidade: Envio sem gestor na operação
    Cenário: [CT-59] Chamada direta sem gestor conserva rascunho e registra recusa
      Dado rascunho de S com descrição Notebook, valor 3000.00 e centro C1 sem gestor, campos/histórico capturados, S/D reais e coleta de e-mail/log iniciada após o preparo
      Quando S chama a operação de envio fora do formulário
      Então o envio é recusado, a consulta nova conserva rascunho e todos os campos/histórico capturados, não há etapa nem decisão nova de aprovação, há warning correspondente à tentativa sem gestor e S/D não recebem e-mail
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-80 | validar gestor ausente apenas no componente | CT-59 | chamada direta deve recusar e manter rascunho, sem pôr em trânsito |
| M-81 | recusar envio sem gestor mas remover warning | CT-14, CT-59 | warning correspondente à tentativa recusada deve ser observado |
| M-82 | sem gestor, pular sua etapa e aprovar ou encaminhar ao diretor | CT-59 | permanece rascunho sem etapa/decisão nova e sem aviso a D |

## Regra R23 — Cada decisão válida pelo componente grava sua etapa

**Perfil:** completo (fluxo 3×3, herdado pela regra de decisão). **Origem:** RQ-05/RQ-06/RQ-08, A-03/A-07/A-11. **Técnica formal:** tabela de decisão etapa×valor×verbo na superfície. Usa os mesmos papéis distintos e transições reais do domínio; confirmação é executada no componente. CT-35 já cobre rejeição válida de gestor. Esses cenários não decidem acúmulo de papéis Q?3.

```gherkin
  Funcionalidade: Confirmação de decisões no painel
    Esquema do Cenário: [CT-60] Aprovar pelo componente grava decisão e destino
      Dado compra de S no valor <valor> com limite 5000.00 em <inicial>, preparada por transições reais, G gestor do centro e D diretor da organização distintos de S, com coleta de e-mail iniciada após o preparo
      Quando <ator> confirma aprovação da etapa <etapa> pelo componente
      Então a consulta nova mostra <final>, conserva descrição/valor/centro/solicitante e apresenta <decisões>, com <avisos>
      Exemplos:
        | valor | inicial | ator | etapa | final | decisões | avisos | # partição |
        | 3000.00 | aguardando_gestor | G | gestor | aprovada | exatamente uma aprovação de G e nenhuma de D | nenhum mail para S/G/D | aprovação final de gestor |
        | 6000.00 | aguardando_gestor | G | gestor | aguardando_diretor | exatamente uma aprovação de G e nenhuma de D | exatamente um mail a D dessa etapa e nenhum para S/G | avanço ao diretor |
        | 6000.00 | aguardando_diretor | D | diretor | aprovada | aprovação anterior de G e exatamente uma aprovação de D | nenhum mail para S/G/D | aprovação final de diretor |

    Cenário: [CT-61] Diretor rejeita com justificativa válida pelo componente
      Dado compra de S de 6000.00 com limite 5000.00 em aguardando_diretor após envio e aprovação reais de G, D diretor da organização distinto de S/G, campos/histórico capturados e coleta de e-mail iniciada após o preparo
      Quando D confirma rejeição de diretor pelo componente com Sem verba
      Então a consulta nova mostra rascunho com os campos originais, conserva histórico capturado e acrescenta rejeição da etapa diretor por D com Sem verba, sem aviso mail para S/G/D
```

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-83 | aprovação de gestor visível, callback não decide | CT-60 | linhas de gestor exigem decisão de G e estado final correspondente ao valor |
| M-84 | aprovação de diretor visível, callback retorna sem decidir | CT-60 | confirmação de D exige aprovada e sua decisão, preservando a de G |
| M-85 | rejeição válida de diretor no componente não devolve ao rascunho | CT-61 | rascunho e rejeição de D com Sem verba devem ser persistidos |

## Regra R24 — E-mails acompanham a nova etapa e a confirmação da superfície

**Perfil:** completo (notificações 3×3). **Origem:** RQ-04/RQ-09/RQ-14, A-02/A-11. **Técnica formal:** tabela de destinatário por etapa/ação e partição de superfície. Cenários existentes reescritos CT-23 (R6) e CT-36 (R10) são os matadores desta regra transversal; não são contados como novos CT. Efeitos são capturados depois do preparo para não confundir aviso da primeira etapa com o do reenvio/cancelamento.

| Mutante | Defeito plausível | CT que mata | Asserção divergente |
|---|---|---|---|
| M-86 | reenvio corrigido persiste C2/H mas notifica antigo gestor G | CT-23 | H recebe exatamente um mail da nova etapa; G/S/D recebem zero nessa ação |
| M-87 | callback de envio muda estado sem enviar e-mail | CT-36 | linha enviar exige exatamente um mail da solicitação para G |
| M-88 | callback de cancelamento envia aviso extra | CT-36 | ambas as linhas cancelar exigem zero aviso para S/G/D/H reais |

## Checklist de Taxonomia

| Gatilho | CT / lacuna / não se aplica | Grupo |
|---|---|---|
| IDOR/autorização horizontal | CT-03/08/13/18/22/30; cross-tenant lacuna Q?5, sem recorte dado | Domínio; Recorte organizacional e mensagens pendentes |
| Autorização declarada | CT-03/08/13/18/22/30/32 chamam escrita fora da UI; CT-33/34 no componente; CT-22 inclui gestor de outro centro; CT-52/53/54 exercem administração autorizada e CT-55/56 diretoria plural | Domínio; Administração; Administração UI; Componentes |
| Idempotência de toda escrita | CT-01 sem alteração; CT-10 segunda exclusão; CT-12/15 retry envio; CT-17/21 decisões fora de etapa; CT-29 repetir cancelamento; CT-51 não duplica e-mail após envio; criação lacuna Q?7 | Domínio; Alçada e domínios pendentes |
| Domínio condicionado | CT-41 distingue abaixo/igual/acima de 5000.00; CT-43 muda configuração para 7000.00; pares de papéis e diretoria vazia permanecem Q?3/Q?4 | Domínio; Alçada e domínios pendentes |
| Limites na criação/edição/uso | CT-38/40 criam dados válidos; CT-44/45 recusam rejeição sem justificativa; tetos, escala e normalização continuam Q?1/Q?2; nenhum limite copiado do plano | Domínio; Componentes; Alçada e domínios pendentes |
| Concorrência/limite | CT-15/31/51 usam snapshot antigo; CT-56 exige primeira decisão de diretor preservada contra outro snapshot elegível; corrida simultânea física não executada; Q?3/Q?4 continuam sem resposta | Domínio; Alçada e domínios pendentes |
| Destinatários 0/1/N | CT-14 gestor 0, sem provar atomicidade; CT-49 gestor 1; CT-50 diretores 1/N da organização e terceiro real de outra organização; diretoria 0 segue Q?4 e link Q?6 | Domínio; Recorte organizacional e mensagens |
| Opcional ausente/null/vazio | justificativa não fornecida CT-44/45; gestor nulo no uso CT-14; null/vazio/espaços e demais domínios continuam Q?1/Q?2 | Domínio; Componentes; Alçada e domínios pendentes |
| Paginação 0/1/limite/+1/inserção | sem requisito de paginação; CT-46 prova status em lista autorizada, sem decidir recorte Q?5 ou fronteiras de página | Componentes; Apresentação pendente |
| Ordenação inválida/nulo/empate | lacuna: 02 ausente, colunas/estado público não inventariados; CT-46/47 não certificam ordenação | Apresentação pendente |
| Timezone/DST/data | CT-58 afirma o instante conhecido e a justificativa da decisão na apresentação; formato/fuso e DST não dados; CT-48/57/58 preservam recorte Q?5 | Componentes; Apresentação pendente |
| Texto/acento/emoji/teto/espaços | CT-01 texto válido com acento/emoji; teto/normalização/espaços lacuna Q?1/Q?2 | Domínio; Alçada e domínios pendentes |
| Unicidade + soft delete | lacuna: unicidade não dada no 00; domínio Q?1, mecanismo Q?8 | Alçada e domínios pendentes |
| Removido ainda funciona? | CT-09/10/37 exercitam escrita no alvo removido; físico proposto @premissa, soft delete não certificado | Domínio |
| CRUD inexistente/sem alteração/dupla exclusão | CT-01/09/10; leitura de inexistente lacuna Q?5 | Domínio; Apresentação pendente |
| Mass assignment: solicitação | CT-38/40 provam criação válida, sem certificar payload extra; lacunas Q?1/Q?7 e 02 ausente; fillable não inferido da implementação | Alçada e domínios pendentes |
| Mass assignment: centro | lacuna RQ-01/A-01 Q?1; CT-32 prova autoridade, não payload extra | Administração; Alçada e domínios pendentes |
| Mass assignment: decisões | lacuna 02 ausente; entrada/fronteira não inventariadas; pai não prova filho | Domínio |
| IDOR: solicitação | CT-03/08/13/18/22/30 horizontal; tenant/lista/detalhe lacuna Q?5 | Domínio; Apresentação pendente |
| IDOR: centro | CT-32/33 administrativo; referência cross-tenant na gravação lacuna Q?1/Q?5 | Administração; Recorte organizacional e mensagens pendentes |
| IDOR: decisões | lacuna entrada própria desconhecida sem 02; recorte histórico Q?5 | Recorte organizacional e mensagens pendentes |
| Upload | não se aplica: anexos explicitamente fora de escopo no 00; dispensa de feature, não de guarda de vendor | — |
| Precisão monetária | CT-01/02/05 persistem decimais concretos; CT-41 aplica fronteira monetária da alçada; escala/arredondamento de entradas seguem Q?1 | Domínio; Alçada e domínios pendentes |
| Livewire por linha: inválido e tipo errado | lacuna 02 inexistente; implementação não lida para inventar superfície | Componentes |
| Estado framework: índice/parse/coluna/operador | lacuna 02 ausente; leitura de vendor confirmou arnês, não consumidores | Componentes |
| Método público chamável | lacuna 02 ausente; nenhum método presumido dispensado de barreira | Componentes |
| Discriminante nulo | lacuna tenancy opcional, Q?5 e 02 ausente; nem abertura nem fechamento certificados | Recorte organizacional e mensagens pendentes |
| Saída após erro | CT-14 conserva rascunho/editável (CT-04/05); outras recusas não fixam 4xx/5xx/redirect; destino de HTTP/link futuro lacuna Q?6 | Componentes; Recorte organizacional e mensagens pendentes |

Nenhuma dispensa de fronteira baseada em pai, query UI, hook, prompt ou git status. Negativas que precisariam de prova ficaram em lacuna, sem alegação de vendor não verificado removendo controle.

## Gate de falsificabilidade e poda

Passo 6 de derivação aplicado às regras fechadas: cada mutante tem CT e asserção/valor divergente; tabelas são **previstas**, sem morte medida. Situação consta nos Dados. Recusas de transição afirmam situação/campos, histórico e e-mails com destinatários reais. CT-14/59 são cardinalidade gestor zero e exigem o warning do 00, sem provar atomicidade de entrega. Campos não inventados fora da origem fechada. **O fechamento da rodada 2 não passou por nova revisão independente: estes enunciados são o desenho proposto, não cobertura aprovada.**

Regras completas têm 3–5 mutantes, padrão 2–3. Teto completo ≤5 CT por regra e padrão ≤3 respeitado. As linhas dos esquemas são classes da operação/estado/persona, não CT novos. Componentes CT-05/35/36/40/45 acrescentam gravação/action/recusa na superfície; CT-39/46/47/48 provam apresentação; externos provam regra fora do formulário. CT-49/50 exigem envio pelo canal de e-mail e destinatários concretos; CT-51 mantém contagem exata no retry. Lacunas não foram convertidas em matadores falsos.

| Cogitado | Cortado/adiado por quê |
|---|---|
| Browser do fluxo entre personas | componente prova DOM/ação/persistência; sem observável adicional JS/pixel do 00 |
| Browser da modal de justificativa | CT-35 prova action e gravação; CT-45 prova recusa por ausência; nenhum observável exclusivamente browser dado; teto/espaços continuam Q?2 |
| GET da listagem afirmando só 200 | nenhum mutante discriminado; CT-46/47 afirmam o status concreto; recorte continua Q?5 |
| Qualquer warning como prova de A-10 | um log alheio não discrimina; CT-14/59 exigem warning correspondente à tentativa recusada sem gestor |
| BVA 255/256 e mínimo monetário 0,01 | limites do PRD, sem fonte no 00; Q?1/Q?2 |
| Avisos de rejeição/final/cancelamento | fora de escopo A-11; CT-20/28 afirmam ausência com destinatários reais |
| Override de config em todos os BVA | CT-41 preserva fábrica efetiva 5000.00; CT-43 varia deliberadamente para 7000.00 e discrimina literal embutido |
| Atomicidade com mundo sem destinatário/falha antes do efeito | não discrimina; lacuna até direção e arnês permitido |

## Índice de Cenários

Todos os paths abaixo são propostas, não arquivos de testes materializados. Confirmada permanece vazia; FeatureTenancy exige registro prévio antes de execução futura. Esquemas contam uma vez. Mutantes são associados globalmente, incluindo M-12/51 e as regras transversais R21/R22/R24. CT-52–61 e reescritas/vínculos do fechamento final não foram reavaliados independentemente após o teto 2; cobertura não aprovada.

| CT | Cenário | Regra | Técnica | Grupo | Camada | Path proposto | Mutantes previstos |
|---|---|---|---|---|---|---|---|
| CT-01 | A correção do rascunho persiste o campo alterado | R1 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-03 |
| CT-02 | Editar fora do rascunho preserva os três campos | R1 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-01, M-02 |
| CT-03 | Outra identidade não edita o rascunho de S | R1 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-01, M-02 |
| CT-04 | A edição apresenta os dados do rascunho ao dono | R1 | EP; estado/identidade | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-04 |
| CT-05 | Salvar pelo componente grava a correção | R1 | EP; estado/identidade | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-03 |
| CT-06 | Excluir rascunho retira a solicitação das consultas | R2 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-09 |
| CT-07 | Excluir fora do rascunho não apaga a solicitação | R2 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-06 |
| CT-08 | Outra identidade não exclui o rascunho | R2 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-05 |
| CT-09 | Editar ID ausente não recria solicitação | R2 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-07 |
| CT-10 | Excluir ID ausente não toca outro agregado | R2 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-08 |
| CT-11 | Primeiro envio chega ao gestor nas duas faixas | R3 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-10 |
| CT-12 | Enviar fora do rascunho não reinicia o fluxo | R3 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-14 |
| CT-13 | Outra identidade não envia o rascunho de S | R3 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-13 |
| CT-14 | Centro sem gestor conserva o rascunho e informa a recusa | R3/R22 | EP; estado/identidade | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-12, M-81 |
| CT-15 | Instância antiga não envia outra vez | R3 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-11 |
| CT-16 | O gestor decide sua etapa corrente | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-18, M-51 |
| CT-17 | Gestor não aprova fora da sua etapa | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-19, M-30 |
| CT-18 | Aprovar exige a identidade do gestor do centro | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-15, M-16 |
| CT-19 | Solicitante que também é gestor decide a própria etapa | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-17, M-51 |
| CT-20 | Rejeitar a etapa corrente devolve para correção | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-21, M-22, M-23 |
| CT-21 | Sem etapa pendente, rejeitar não altera o agregado | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-24 |
| CT-22 | Cada verbo de rejeição exige o aprovador corrente | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-20 |
| CT-23 | Corrigir o centro e reenviar usa o gestor atual | R6/R24 | 2-switch | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-26, M-86 |
| CT-24 | Reenvio após rejeição de diretor não reutiliza o aval antigo | R6 | 2-switch | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-25 |
| CT-25 | Corrigir não se transfere ao aprovador que rejeitou | R6 | 2-switch | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-27 |
| CT-26 | Diretor não aprova antes do gestor nem depois do encerramento | R7 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-28, M-30 |
| CT-27 | Diretor não rejeita solicitação já aprovada | R7 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-29 |
| CT-28 | O solicitante cancela em cada etapa de trânsito | R8 | estado/identidade; interleaving | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-34 |
| CT-29 | Cancelar fora do trânsito conserva a situação | R8 | estado/identidade; interleaving | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-31 |
| CT-30 | Aprovador e terceiro não cancelam solicitação de S | R8 | estado/identidade; interleaving | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-32 |
| CT-31 | Decisão carregada antes do cancelamento não desfaz o estado persistido | R8 | estado/identidade; interleaving | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-33 |
| CT-32 | panel_user não grava administração fora da tela | R9 | papel×ação | Administração | Pest feature HTTP | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-35, M-36, M-37 |
| CT-33 | Componente não permite panel_user mudar o gestor | R9 | papel×ação | Administração UI | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-35 |
| CT-34 | Affordance segue identidade e situação | R10 | decisão; EP | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-38 |
| CT-35 | Rejeitar pelo componente devolve para correção | R10 | decisão; EP | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-39 |
| CT-36 | Confirmar envio/cancelamento grava a transição correspondente | R10/R24 | decisão; EP | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-39, M-87, M-88 |
| CT-37 | Transições sobre ID removido não produzem efeitos em outro registro | R11 | EP por operação | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-40, M-41, M-42 |
| CT-38 | Criação válida fora do componente persiste os dados de S | R12 | EP positiva; visita/gravação | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-43, M-44 |
| CT-39 | A tela de criação oferece os três campos ao solicitante | R12 | EP positiva; visita/gravação | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-46 |
| CT-40 | Criar pelo componente grava todos os dados válidos | R12 | EP positiva; visita/gravação | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-43, M-44, M-45 |
| CT-41 | A fronteira literal decide o destino após o gestor | R13 | BVA 3-valores; estado; config | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-47, M-48, M-51 |
| CT-42 | O diretor encerra a segunda etapa depois do gestor | R13 | BVA 3-valores; estado; config | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-49 |
| CT-43 | A mudança de configuração muda a faixa que exige diretor | R13 | BVA 3-valores; estado; config | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-50 |
| CT-44 | Ausência de justificativa é recusada fora do formulário | R14 | EP ausência; estado×etapa | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-52, M-53, M-54 |
| CT-45 | O formulário de rejeição não grava sem justificativa | R14 | EP ausência; estado×etapa | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-53, M-54 |
| CT-46 | A listagem apresenta a situação da solicitação | R15 | EP estado×superfície | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-55, M-56 |
| CT-47 | O detalhe apresenta a situação da solicitação | R15 | EP estado×superfície | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-55, M-56, M-57 |
| CT-48 | O detalhe atribui as duas etapas aos respectivos aprovadores | R16/R21 | identidade×etapa | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-58, M-59, M-60, M-79 |
| CT-49 | Enviar notifica somente o gestor pelo canal e-mail | R17 | destinatários 1/N; retry | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-61, M-62, M-64 |
| CT-50 | O aval do gestor notifica todos os diretores da organização | R17 | destinatários 1/N; retry | Recorte organizacional e mensagens | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/NotificacoesTest.php` | M-61, M-62, M-63, M-65 |
| CT-51 | Retry de envio mantém uma só notificação ao gestor | R17 | destinatários 1/N; retry | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-64 |
| CT-52 | CRUD administrativo válido funciona fora do formulário | R18 | EP papel×operação; CRUD | Administração | Pest feature HTTP | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-66, M-67, M-68 |
| CT-53 | Administrador visita os formulários de centro | R19 | visita/gravação; operação | Administração UI | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-69 |
| CT-54 | Confirmar CRUD de centro no painel persiste o efeito | R19 | visita/gravação; operação | Administração UI | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-66, M-67, M-68, M-70, M-71 |
| CT-55 | Diretor além do primeiro decide a etapa corrente | R20 | identidade em N; estado×evento stale | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-72, M-73, M-74 |
| CT-56 | Snapshot de outro diretor não decide etapa já resolvida | R20 | identidade em N; estado×evento stale | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-75, M-76 |
| CT-57 | Aprovação única é visível antes ou ao final do fluxo | R21 | estado/etapa; instante; autoria histórica | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-77 |
| CT-58 | Rejeição apresentada conserva autor, instante e justificativa | R21 | estado/etapa; instante; autoria histórica | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-78 |
| CT-59 | Chamada direta sem gestor conserva rascunho e registra recusa | R22 | EP gestor ausente; superfície; efeitos | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-12, M-80, M-81, M-82 |
| CT-60 | Aprovar pelo componente grava decisão e destino | R23 | etapa×valor×verbo; componente | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-83, M-84 |
| CT-61 | Diretor rejeita com justificativa válida pelo componente | R23 | etapa×valor×verbo; componente | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-85 |

## Sem CT-B

Nenhuma costura browser. Status/histórico e operações determinados são observáveis por componente. JS=Sim no 01 não basta para exigir execução JS, pixel ou acessibilidade como oráculo. Não criado 05; **CT-B: 0**. Template-05/pest-plugin-browser não abertos porque a condição não ocorreu. Se surgir CT-B, rule local testes-browser.md proíbe paralelo e prevalece sobre paralelo condicional da skill.

## Revisão adversarial e fechamento

Rodada 1 executada por revisor independente, despachado pela sessão principal; relatório preservado em `adversarial-1.md`. Cobriu integralmente a preliminar CT-01–37, R1–R11 e M-01–42 e registrou 10 contraexemplos textuais. Sem execução da aplicação ou dos testes, portanto nenhuma morte de mutante foi medida. Família GPT-6/Codex herdada; esforço ultra solicitado; ID exato do deployment não exposto. O derivador leu somente esse relatório como nova entrada semântica no fechamento, usando o 00 já lido, sem implementação nem outros conjuntos.

| Achado | Destino e fechamento | Estado |
|---|---|---|
| ADV-01 | cenários novos CT-38/39/40, R12, M-43–46: operação real de criação, tela e persistência dos três campos e solicitante; Q?1/Q?7 preservadas | fechado |
| ADV-02 | cenários novos CT-41/42, R13, M-47–49: 4999.99/5000.00/5000.01, ordem gestor→diretor e aprovação final; Q?3/Q?4 preservadas | fechado |
| ADV-03 | cenários novos CT-44/45, R14, M-52–54: ausência de justificativa recusada no domínio e componente, nas duas etapas, sem efeitos; Q?2 preservada | fechado |
| ADV-04 | cenários novos CT-46/47, R15, M-55–57: status concreto na lista e detalhe autorizados para os cinco estados; Q?5 preservada | fechado |
| ADV-05 | cenário novo CT-48, R16, M-58–60: visualização de G na etapa gestor e D na etapa diretor, distintos; Q?5 preservada | fechado |
| ADV-06 | cenários novos CT-49/50/51, R17, M-61–65: e-mail para gestor, todos os diretores da organização, canal e contagens exatos e retry sem duplicação; Q?4/Q?6 preservadas | fechado |
| ADV-07 | oráculo/fixture de CT-22 reescritos: H, gestor de outro centro, tenta rejeitar a etapa gestor de C1; M-20 discrimina a autorização indevida | fechado |
| ADV-08 | oráculos/fixtures de CT-16/19 reescritos: valor 3000.00, limite 5000.00, estado final aprovada, decisão exata e nenhuma etapa/e-mail para diretor; M-51 também vinculado | fechado |
| ADV-09 | fixtures/oráculos de CT-09/10/37 reescritos: V é operável pela mesma identidade em cada verbo e situação, conservado após ação sobre ID removido; M-07/08/41 discriminam fallback | fechado |
| ADV-10 | cenário novo CT-43, R13, M-50: limite configurado 7000.00 e compra 6000.00 terminam após gestor, sem etapa de diretor | fechado |

Fechamento da rodada 1: 10 achados aceitos e fechados, sendo 7 com cenários novos e 3 com oráculos/fixtures reescritos; 14 CT novos, CT-38–51. Histórico da preliminar preservado; nenhuma pergunta recebeu resposta inventada e 00/01 permaneceram imutáveis. Não se afirma cobertura de todas as direções lacunosas.

Rodada 2 executada por outro revisor independente em contexto novo, despachado pela sessão principal; relatório preservado em `adversarial-2.md`. Leitura integral de CT-01–51, R1–R17 e M-01–65, com 00 vigente como único oráculo. Registrou 11 contraexemplos textuais e nenhuma cláusula RQ inteira sem núcleo discriminante. As sondas sem ID registram perguntas indecididas, sem achados adicionais. A conferência estrutural do relatório encontrou 51 cenários com Então e um Quando; nenhuma aplicação ou teste foi executado. Rota Codex/GPT-6 herdado, ultra solicitado, deployment exato não exposto; cegamento por contrato em filesystem irrestrito.

| Achado da rodada 2 | Destino e fechamento final | Estado |
|---|---|---|
| ADV-01 | cenários novos CT-52/53/54, R18/R19, M-66–71: administrador autorizado realiza CRUD válido fora da UI e pelo painel; visita create/edit; Q?1 preservada | fechado textualmente |
| ADV-02 | cenário novo CT-55, R20, M-72–74: D2 além do primeiro diretor aprova ou rejeita sua etapa e aparece como autor | fechado textualmente |
| ADV-03 | cenário novo CT-56, R20, M-75/76: D2 antes elegível usa snapshot depois da decisão real de D1; estado/histórico e autoria originais permanecem sem segunda decisão/e-mail | fechado textualmente |
| ADV-04 | cenário novo CT-57, R21, M-77: histórico de G visível em aguardando_diretor e em aprovação final de uma etapa, para acesso autorizado; Q?5 preservada | fechado textualmente |
| ADV-05 | cenário novo CT-58, R21, M-78: autor, Sem verba e instante conhecido aparecem no detalhe das rejeições de G/D; formato/fuso e acesso não inventados | fechado textualmente |
| ADV-06 | oráculo reescrito CT-14, com CT-59 complementar, R22, M-81: warning da tentativa recusada sem gestor é observado; poda anterior de warning removida | fechado textualmente |
| ADV-07 | cenários novos CT-60/61, R23, M-83–85: confirmações válidas de G/D gravam aprovação, destino e rejeição de D no componente | fechado textualmente |
| ADV-08 | cenário novo CT-59, R22, M-80/82 e vínculo M-12: sem gestor, envio direto recusa, conserva rascunho/campos/histórico, registra warning e não encaminha ao diretor | fechado textualmente |
| ADV-09 | oráculo reescrito CT-23, R24, M-86: depois da correção para C2, H recebe exatamente um mail da nova etapa e G/S/D recebem zero | fechado textualmente |
| ADV-10 | oráculo reescrito CT-36, R24, M-87/88: confirmação de envio avisa G uma vez; ambas as confirmações de cancelamento não avisam S/G/D/H reais | fechado textualmente |
| ADV-11 | fixture/oráculo reescritos CT-48, R21 transversal, M-79: após mudar gestor atual para H, detalhe conserva G como autor da aprovação histórica | fechado textualmente |

Fechamento final: 11 achados aceitos e tratados, nenhum rejeitado; 10 CT novos (CT-52–61), quatro CT anteriores reescritos (CT-14/23/36/48), sete regras e 23 mutantes previstos adicionados. Histórico preservado: preliminar 37/11/42; após rodada 1, 51/17/65; fechamento final 61/24/88 (CT/regras/mutantes previstos). Perguntas Q?1–Q?8 continuam indecididas no seu recorte, sem respostas ou alterações no 00/01.

**Status da revisão: CONCLUÍDA — duas rodadas independentes realizadas, teto atingido.** Nenhuma terceira rodada ou autorrevisão. **Dívida explícita: CT-52–61, reescritas CT-14/23/36/48, novos vínculos/mutantes e demais alterações do fechamento final não foram reavaliados independentemente após o teto 2. Não se declara cobertura aprovada.** A materialização e execução dos testes, Pest/Artisan/browser/mutation e validação do transporte continuam **pendentes**, separadas do status concluído das duas revisões. Conjunto entregue para congelamento e juiz cego pela sessão principal.

## Referências lidas

- feature-wiki/references/hosts-e-subagentes.md — host/step 7.
- feature-wiki/references/delegacao-casos-de-teste.md — step 7.
- feature-wiki/references/roteamento-e-despacho.md — rota step 7/revisão pendente.
- feature-wiki/references/citacoes-de-codigo.md — formato de evidência, sem citar implementação da feature.
- feature-test-design/references/template-04.md — passos 2/6/7 e arquivo 04.
- feature-test-design/references/escolha-de-camada.md — passos 2/7.
- feature-test-design/references/tecnicas-por-regra.md — passo 3.
- feature-test-design/references/taxonomia-de-defeito.md — passo 4, tabela inteira.
- feature-test-design/references/gherkin.md — passo 5.
- feature-test-design/references/armadilhas-de-api.md — passos 5/7.
- feature-test-design/references/mutation-testing.md — passo 6, operadores; nenhum experimento externo aberto.
- feature-test-design/references/revisao-adversarial.md — preparação da etapa independente.

Entrada no step 7: templates 00–03/pesquisa/implementação/reconciliação não são etapas executadas. Catálogo, experimentos, casos-medidos, conjuntos anteriores/resultados não abertos. Registros que iriam ao 03 estão neste 04/retorno conforme prompt; 03 não criado.

Leituras de fechamento: relatórios próprios `adversarial-1.md` e `adversarial-2.md`, autorizados pela sessão principal; 00 vigente relido na rodada 2. Sem código/implementação, catálogo, outras versões ou outros conjuntos. Conferência de contagens/indexação é mecânica, sem nova revisão adversarial.
