# Casos de Teste — FERRO-830: aprovação de solicitação de compra

> Derivado do **requisito**, não do plano. Fonte: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md` inteiro; do `01`, somente paths, rotas, nomes e `## Superfície de UI` admitidos como insumos.
> feature-wiki **4.1.0** · feature-test-design **1.17.0** · 2026-10-09.
> Revisão adversarial: **PENDENTE — despacho independente pela sessão principal**. Nenhuma autorrevisão. Costuras são propostas do subagente; `Confirmada` fica vazia para a sessão principal.

## Contrato de execução e limites efetivos

Leituras deliberadas restritas a `D:\PROJECTS\SKILLS\blind-20261009\project-26`, ao prompt-c2, às duas skills e referências condicionais, ao `00` e à superfície/path do `01`, convenções e arnês permitidos. Sem leitura de saída-c1, outros conjuntos, catálogo, experimentos, relatório de rodada, outra cópia ou testes Exp. Escrita somente nesta pasta, em `04` e `retorno-c2.md`.

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

Perfis decididos pelo **passo 0**, nenhum imposto. Há Impacto 3. Passos 1–7 percorridos; regras que atravessam áreas herdam o maior perfil. BVA 3-valores preparada nas lacunas, sem converter domínio ausente em resposta. Pairwise não reduz as condições críticas fechadas: estado e identidade são tabelados integralmente; combinações materiais de papéis ainda não decididas ficam em Q?3.

Cenários: 37 · Regras: 11 · Mutantes previstos: 42 · Sem matador: 0. Contagens derivadas por regex equivalentes aos quatro grep -c do template; conferidas por rg -c.

Contagem estrutural, não detecção medida. Esquema conta uma vez, sem inflação pelo número de exemplos. Cláusula aberta não conta como regra coberta.

## Varredura SFDIPOT

| Dimensão | Inventário anterior aos cenários | Saída |
|---|---|---|
| S | solicitação, centro, decisões de etapa, diretor; Resources/forms nomeados pelo 01 | R1–R11; inventário Livewire ausente |
| F | criar, corrigir, excluir, enviar, aprovar, rejeitar, cancelar, apresentar, notificar | CT-01…CT-37; perguntas/lacunas |
| D | descrição, decimal, centro, gestor nulo, justificativa, atores distintos, diretores 0/1/N, outra organização | CT-01/02/14/18/22; domínios/tenant pendentes |
| I | componente e chamada direta fora da UI; sem API/job/comando novo pedido | Domínio e Componentes; 02 faltante |
| P | Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1, browser 5.0.1, mutate 5.0.2 | lock e arnês lidos; nenhuma execução |
| O | solicitante, gestor por centro, diretor por organização, administração, papéis acumulados | matrizes; CT-19; Q?3 |
| T | ordem, rejeitar→corrigir→reenviar, retries e snapshot antigo | CT-15/23/24/31; SLA/expiração fora de escopo |

## Matriz única estado × operação

Montada antes das regras: **5 estados × 10 operações = 50 células**. Os estados são os do `00` (A-05/A-06), sem leitura do enum da implementação. Aprovar/rejeitar têm persona/etapa próprias; listar e detalhar são operações distintas. Criação não parte de solicitação existente e fica no gate aberto de RQ-01.

Legenda: ✅ operação válida executada; ❌ operação recusada, preservando situação, campos e histórico de decisões, sem novo e-mail a destinatários reais; L = lacuna declarada. A edição fora do rascunho afirma valores persistidos. Cada decisão afirma ausência de nova decisão; verbo irmão não herda chamada. As recusas comparam o histórico existente, não um mundo vazio.

| Estado | editar/S | excluir/S | enviar/S | aprovar/G | rejeitar/G | aprovar/D | rejeitar/D | cancelar/S | listar | detalhar |
|---|---|---|---|---|---|---|---|---|---|---|
| rascunho | ✅ CT-01/05 | ✅ CT-06 | ✅ CT-11 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-21 | ❌ CT-29 | L Q?5 | L Q?5 |
| aguardando_gestor | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ✅ CT-16 | ✅ CT-20 | ❌ CT-26 | ❌ CT-22 | ✅ CT-28 | L Q?5 | L Q?5 |
| aguardando_diretor | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-22 | L Q?3 | ✅ CT-20 | ✅ CT-28 | L Q?5 | L Q?5 |
| aprovada | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-27 | ❌ CT-29 | L Q?5 | L Q?5 |
| cancelada | ❌ CT-02 | ❌ CT-07 | ❌ CT-12 | ❌ CT-17 | ❌ CT-21 | ❌ CT-26 | ❌ CT-21 | ❌ CT-29 | L Q?5 | L Q?5 |

8 válidas fechadas exercitadas, 31 inválidas exercitadas, 11 lacunas. CT-16 afirma decisão persistida e **não** destino de alçada enquanto RQ-05 está aberta. A coluna aprovar/D tem célula válida bloqueada; isso é limite explícito.

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

- RQ-01 — aberta (Q?1, Q?7), sem cenário até a resposta: criação/domínio. RQ-02/09 ainda permitem corrigir registros existentes.
- RQ-05 — aberta (Q?3, Q?4), sem cenário até a resposta: direção positiva de diretor e destino de alçada. A ordem inicial pelo gestor é RQ-04 fechada.
- RQ-07 — aberta (Q?2), sem cenário até a resposta: domínio completo da justificativa. RQ-06/08 e A-07 permitem rejeição com a justificativa concreta não vazia usada no preparo.
- RQ-12 — aberta (Q?5), sem cenário até a resposta.
- RQ-13 — aberta (Q?5), sem cenário até a resposta: apresentação. A decisão persistida é observável do verbo aprovar/rejeitar, sem prometer recorte de tela.
- RQ-14 — aberta (Q?4, Q?6), sem cenário até a resposta: positivo, zero diretores e link. A-11 fixa ausência de avisos adicionais; recusas não produzem efeitos do sucesso.

## Costuras de Teste

| Grupo | Regras | Costura | Existente/nova | Por quê | Confirmada |
|---|---|---|---|---|---|
| Domínio | R1–R8/R11 | Pest feature HTTP | existente: TestCase/RefreshDatabase de Feature | persistência e chamada direta sem UI | |
| Componentes | R1/R3/R10 | componente Livewire/Filament | existente: EditUser de tests/Kit/PaginasInfraTest.php | campos/actions/DOM e gravação | |
| Administração | R9 | Pest feature HTTP | existente: convenção de AdminDaOrganizacaoTest; novos testes fora do kit | escrita administrativa fora da tela | |
| Administração UI | R9 | componente Livewire/Filament | existente: arnês do painel | URL/payload direto apesar de menu oculto | |
| Alçada e domínios pendentes | RQ abertas | Pest feature HTTP | proposta nova no arnês Feature | BVA e domínio na gravação | |
| Recorte organizacional e mensagens pendentes | RQ abertas | Pest feature HTTP | nova FeatureTenancy não registrada | teams antes das migrations; sem mudar arnês nesta rodada | |
| Apresentação pendente | RQ-12/13 abertas | componente Livewire/Filament | existente: arnês de componente | status/histórico não exigem JS/pixel | |

Costuras novas não criadas nem confirmadas. Nenhuma costura browser.

## Fronteira com o Plano

| Item do 01 | Recusado como oráculo / tratamento | Destino |
|---|---|---|
| Paths dos Resources/páginas e rotas /app[/tenant] | localização permitida, não resultado esperado | índice/gate |
| Nomes enviar/aprovar/rejeitar/cancelar | mecanismo/nome, não determina o resultado | materialização futura |
| Gate antigo JS=Sim + personas → 05 | diverge do gate instalado: DOM/action já prováveis por componente | Sem CT-B |
| minValue/maxLength, DB/fillable/locks/UPDATE | domínio e fronteira não confirmados no 00 | Q?1/Q?2; 02 ausente |
| Mensagem exata, cores e link/corpo do e-mail | comportamento visível não determinado no card | pergunta; sem texto inventado |
| logs/comandos e CT antigos citados no 01 | não são oráculo; testes antigos não lidos | sem execução nem CT de log |

## Perguntas para o 00-requisito.md

Desvio: 00 imutável; perguntas aqui prontas para colagem, com IDs provisórios. Sem respostas e nenhuma recomendação assumida como aprovação. Premissas A-01…A-12 dadas não revogadas.

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
| BVA 3-valores da alçada | "4999.99", "5000.00", "5000.01", incremento "0.01"; fábrica lida efetivamente em 5000.00 sem override/env de teste | RQ-05 aberta; não inventar destino |
| BVA de textos | n−1/n/n+1 em caracteres, acento/emoji, criação/edição/domínio externo | n ausente Q?1/Q?2 |
| EP dinheiro | decimal literal, nunca float; inválidos separados | positividade/teto/escala/arredondamento Q?1 |
| decisão dos papéis | pares S×G/S×D/G×D; CT-19 para S×G | outros pares Q?3 |
| rastreio exato de efeito | mail, gestor singular, diretores 0/1/N da organização; aconteceu/não/uma vez/atomicidade | RQ-14 aberta; fake genérico não prova transporte |
| tenant/discriminante nulo | duas organizações e contexto nulo inventariados | Q?5 e 02 ausente; não arbitrar single-tenant/nulo |
| atomicidade | propor falha depois do despacho com G/D reais | direção/arnês e execução pendentes; pré-validação não prova atomicidade |

## Setup Global

- Stack confirmado no composer.lock por JSON: Laravel v13.25.0, Filament v5.7.6, Livewire v4.4.0, Pest v5.1.1, browser v5.0.1, mutate v5.0.2. Mutate não declarado diretamente em require-dev do composer.json. Nenhuma instalação; driver/runner não inspecionados, sem alegação de ausência.
- tests/Pest.php liga TestCase/RefreshDatabase a Feature, não a Unit. Tenancy usa TenancyTestCase antes das migrations; FeatureTenancy é proposta nova, não registrada, sem CT de negócio inserido em kit.
- S solicitante, G gestor C1, H gestor C2, D diretor e U terceiro são distintos salvo CT-19. Helpers reais `usuario`, `usuarioComPapel`, `noPainelDa` e `papelNaOrganizacao` de tests/Pest.php. Diretor é premissa A-03, não papel cuja instalação foi executada nesta rodada.
- Factories de compra/centro ausentes (`Test-Path -> False`). Materialização futura por Model::create com campos acordados; nenhuma factory/state inventada. Preparo de fixture não certifica criação aberta de RQ-01.
- Helper futuro `solicitacaoEm(...)` em tests/Pest.php monta situações por **transições reais**, nunca gravando situação à força. Caminhos diretor/final dependem do contrato de RQ-05; testes que precisam dessas fixtures não foram materializados/executados.
- Capturar campos/histórico, ativar observação de efeitos após preparo e consultar o agregado novamente depois do Quando. Snapshot em memória não é oráculo.
- Notification::fake após fixtures captura canais/destinatários; futuro positivo deve afirmar mail explicitamente. Fake não prova transporte SMTP. Nenhum CT de log: não há RQ de auditoria de log; warning de A-10 fica para QA posterior conforme Proibição 12.
- APIs confirmadas no vendor: fillForm, assertHasFormErrors/NoFormErrors, assertSchemaStateSet; callAction(TestAction::make(string)->table(record)), assertActionVisible/Hidden. Gravação: fillForm + call('save') + assertDatabaseHas com campos completos, não só ID. Sem helper deprecated.
- Dois testes de convenção lidos: tests/Kit/AdminDaOrganizacaoTest.php e PaginasInfraTest.php. Rules testes.md/filament.md reforçam ação direta e visita/gravação; auth.md não adiciona comportamento desta feature. tests-browser.md fica para condição futura de browser.

## Gate de telas de escrita

| Rota/path do 01 | Visita | Gravação por componente | Limite |
|---|---|---|---|
| SolicitacoesCompra/create | lacuna RQ-01 | lacuna RQ-01 | Q?1/Q?7 |
| SolicitacoesCompra/{record}/edit | CT-04 | CT-05 | inválidos de domínio Q?1 |
| CentrosCusto/create | lacuna RQ-01/A-01 | lacuna RQ-01/A-01 | Q?1 |
| CentrosCusto/{record}/edit | recusa CT-33 | recusa CT-33 | positivo/domínio Q?1; recusa não fecha gate positivo |

Gate de escrita **parcial, com lacunas**. Nenhum GET foi apresentado como gravação, nem o requisito alterado para fechar o gate.

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
      Dado ID <alvo> sem solicitação alcançável, S autenticado, G/D reais e solicitação V válida com campos/histórico capturados
      Quando S tenta editar diretamente esse ID para descrição "Intrusão"
      Então a operação é recusada; o ID continua ausente, V conserva todos os campos/histórico, não surgem decisões para o alvo e G/D não recebem e-mail
      Exemplos:
        | alvo | # partição |
        | removido por S em rascunho | excluído |
        | nunca existente | inexistente |

    @premissa_mecanismo_exclusao
    Esquema do Cenário: [CT-10] Excluir ID ausente não toca outro agregado
      Dado ID <alvo> sem solicitação alcançável, S autenticado, G/D reais e solicitação V válida com campos/histórico capturados
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
| M-07 | edição recria ID ausente | CT-09 | ID permanece ausente; o mutante recria com Intrusão |
| M-08 | resolver delete ausente para primeiro registro disponível | CT-10 | V continua consultável e inalterada; o mutante remove V |
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
      Dado rascunho de S cujo centro está sem gestor, campos/histórico capturados e D disponível
      Quando S aciona enviar pelo componente
      Então continua em rascunho com campos/histórico iguais, há mensagem visível de recusa e D não recebe e-mail

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
| M-12 | enviar mesmo sem gestor | CT-14 | rascunho e mensagem de recusa; o mutante põe em trânsito |
| M-13 | identidade só na action UI | CT-13 | envio direto por U conserva rascunho; o mutante avança |
| M-14 | permitir reenviar uma solicitação já em trânsito | CT-12 | linha aguardando_diretor conserva estado/histórico, sem novo aviso; o mutante reinicia |

## Regra R4 — Somente o gestor da etapa pendente aprova nela

> RQ-06; A-02/A-09 · completo · papel×ação, estado×operação.

```gherkin
# language: pt
Funcionalidade: aprovação de solicitação de compra
  Regra: Somente o gestor da etapa pendente aprova nela
    Cenário: [CT-16] O gestor decide sua etapa corrente
      Dado solicitação em aguardando_gestor, valor 3000.00, gestor G distinto de S/D
      Quando G aprova diretamente
      Então existe exatamente uma decisão persistida de aprovação da etapa de gestor atribuída a G nessa solicitação

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
      Dado solicitação em aguardando_gestor cujo solicitante S é gestor do centro, e D é outra pessoa
      Quando S aprova diretamente como gestor
      Então existe exatamente uma decisão persistida de aprovação da etapa de gestor atribuída a S nessa solicitação
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
      Dado solicitação em <situação>, dono S, gestor G, diretor D e U distintos, campos/histórico capturados
      Quando <ator> tenta rejeitar diretamente com "Sem verba"
      Então a operação é recusada; situação/campos e histórico permanecem iguais; S/G/D não recebem e-mail
      Exemplos:
        | situação | ator | # partição |
        | aguardando_gestor | S | dono não gestor |
        | aguardando_gestor | U | terceiro |
        | aguardando_gestor | D | diretor antecipado |
        | aguardando_diretor | S | dono não diretor |
        | aguardando_diretor | U | terceiro |
        | aguardando_diretor | G | anterior sem papel diretor |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-20 | conferir ator em aprovar, esquecer em rejeitar | CT-22 | U conserva pendência/histórico em ambas as etapas; o mutante devolve ao rascunho |
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
      Dado solicitação em rascunho após rejeição real de G, S corrigiu descrição para Monitor e centro para C2 cujo gestor é H, e G/H/D existem
      Quando S envia novamente diretamente
      Então a consulta nova mostra aguardando_gestor, Monitor e C2, e o identificador do gestor da etapa corrente é H, não G

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
      Dado solicitação de S em <inicial>, com campos capturados e G/D distintos disponíveis
      Quando S confirma <ação> pelo componente
      Então consulta nova mostra <final> com descrição/valor/centro/solicitante originais
      Exemplos:
        | inicial | ação | final | # partição |
        | rascunho | enviar | aguardando_gestor | envio |
        | aguardando_gestor | cancelar | cancelada | etapa 1 |
        | aguardando_diretor | cancelar | cancelada | etapa 2 |
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
      Dado alvo de S excluído ainda em rascunho por transição real, V válida com situação/campos/histórico capturados e G/D reais disponíveis
      Quando o ator autorizado para <operação> tenta <operação> diretamente no ID removido
      Então a operação é recusada; alvo continua ausente, V conserva situação/campos/histórico, nenhuma decisão é criada para o alvo e G/D não recebem e-mail
      Exemplos:
        | operação | # partição |
        | enviar | S |
        | aprovar como gestor | G |
        | rejeitar como gestor com Sem verba | G |
        | rejeitar como diretor com Sem verba | D |
        | cancelar | S |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-40 | objeto antigo removido cria decisão órfã | CT-37 | alvo ausente e sem decisão após cada transição; mutante grava efeito órfão |
| M-41 | ID ausente resolve para primeiro registro da lista | CT-37 | V conserva situação/campos/histórico; mutante altera V |
| M-42 | notificar antes de descobrir que registro foi removido | CT-37 | destinatários reais G/D não recebem e-mail; mutante envia antes de recusar |

## Checklist de Taxonomia

| Gatilho | CT / lacuna / não se aplica | Grupo |
|---|---|---|
| IDOR/autorização horizontal | CT-03/08/13/18/22/30; cross-tenant lacuna Q?5, sem recorte dado | Domínio; Recorte organizacional e mensagens pendentes |
| Autorização declarada | CT-03/08/13/18/22/30/32 chamam escrita fora da UI; CT-33/34 no componente | Domínio; Administração; Componentes |
| Idempotência de toda escrita | CT-01 sem alteração; CT-10 segunda exclusão; CT-12/15 retry envio; CT-17/21 decisões fora de etapa; CT-29 repetir cancelamento; criação lacuna Q?7 | Domínio; Alçada e domínios pendentes |
| Domínio condicionado | lacuna RQ-05 aberta Q?3/Q?4; BVA preparada sem resultado arbitrado | Alçada e domínios pendentes |
| Limites na criação/edição/uso | lacuna RQ-01/RQ-07 Q?1/Q?2; nenhum limite copiado do plano | Alçada e domínios pendentes |
| Concorrência/limite | CT-15/31 snapshot antigo contra agregado persistido; duas aprovações reais de diretor lacuna RQ-05 e execução futura | Domínio; Alçada e domínios pendentes |
| Destinatários 0/1/N | CT-14 gestor 0, nunca prova geral de não-efeito; gestor 1/diretor 0/1/N positivo lacuna RQ-14 Q?4/Q?6 | Componentes; Recorte organizacional e mensagens pendentes |
| Opcional ausente/null/vazio | lacuna Q?1/Q?2; gestor nulo no uso CT-14 | Alçada e domínios pendentes; Componentes |
| Paginação 0/1/limite/+1/inserção | lacuna RQ-12 aberta Q?5; arnês existe, recorte pendente | Apresentação pendente |
| Ordenação inválida/nulo/empate | lacuna: 02 ausente, colunas/estado público não inventariados, RQ-12 aberta | Apresentação pendente |
| Timezone/DST/data | lacuna: A-12 cita quando, mas RQ-13 aberta Q?5; fuso/formato não dados | Apresentação pendente |
| Texto/acento/emoji/teto/espaços | CT-01 texto válido com acento/emoji; teto/normalização/espaços lacuna Q?1/Q?2 | Domínio; Alçada e domínios pendentes |
| Unicidade + soft delete | lacuna: unicidade não dada no 00; domínio Q?1, mecanismo Q?8 | Alçada e domínios pendentes |
| Removido ainda funciona? | CT-09/10/37 exercitam escrita no alvo removido; físico proposto @premissa, soft delete não certificado | Domínio |
| CRUD inexistente/sem alteração/dupla exclusão | CT-01/09/10; leitura de inexistente lacuna Q?5 | Domínio; Apresentação pendente |
| Mass assignment: solicitação | lacuna RQ-01 aberta Q?1/Q?7 e 02 ausente; fillable não inferido da implementação | Alçada e domínios pendentes |
| Mass assignment: centro | lacuna RQ-01/A-01 Q?1; CT-32 prova autoridade, não payload extra | Administração; Alçada e domínios pendentes |
| Mass assignment: decisões | lacuna 02 ausente; entrada/fronteira não inventariadas; pai não prova filho | Domínio |
| IDOR: solicitação | CT-03/08/13/18/22/30 horizontal; tenant/lista/detalhe lacuna Q?5 | Domínio; Apresentação pendente |
| IDOR: centro | CT-32/33 administrativo; referência cross-tenant na gravação lacuna Q?1/Q?5 | Administração; Recorte organizacional e mensagens pendentes |
| IDOR: decisões | lacuna entrada própria desconhecida sem 02; recorte histórico Q?5 | Recorte organizacional e mensagens pendentes |
| Upload | não se aplica: anexos explicitamente fora de escopo no 00; dispensa de feature, não de guarda de vendor | — |
| Precisão monetária | CT-01/02/05 persistem decimais concretos; escala/arredondamento/BVA lacuna Q?1/RQ-05 | Domínio; Alçada e domínios pendentes |
| Livewire por linha: inválido e tipo errado | lacuna 02 inexistente; implementação não lida para inventar superfície | Componentes |
| Estado framework: índice/parse/coluna/operador | lacuna 02 ausente; leitura de vendor confirmou arnês, não consumidores | Componentes |
| Método público chamável | lacuna 02 ausente; nenhum método presumido dispensado de barreira | Componentes |
| Discriminante nulo | lacuna tenancy opcional, Q?5 e 02 ausente; nem abertura nem fechamento certificados | Recorte organizacional e mensagens pendentes |
| Saída após erro | CT-14 conserva rascunho/editável (CT-04/05); outras recusas não fixam 4xx/5xx/redirect; destino de HTTP/link futuro lacuna Q?6 | Componentes; Recorte organizacional e mensagens pendentes |

Nenhuma dispensa de fronteira baseada em pai, query UI, hook, prompt ou git status. Negativas que precisariam de prova ficaram em lacuna, sem alegação de vendor não verificado removendo controle.

## Gate de falsificabilidade e poda

Passo 6 executado nas regras fechadas: cada mutante tem CT e asserção/valor divergente; tabelas são **previstas**, sem morte medida. Situação consta nos Dados. Recusas de transição afirmam situação/campos, histórico e e-mails com destinatários reais. CT-14 é cardinalidade zero, nunca prova de atomicidade. Campos não inventados fora da origem fechada.

Regras completas têm 3–5 mutantes, padrão 2–3. Teto completo ≤5 CT por regra e padrão ≤3 respeitado. As linhas dos esquemas são classes da operação/estado/persona, não CT novos. Componente CT-05/35/36 acrescenta gravação/action na superfície; externos provam regra fora do formulário. Lacunas não foram convertidas em matadores falsos.

| Cogitado | Cortado/adiado por quê |
|---|---|
| Browser do fluxo entre personas | componente prova DOM/ação/persistência; sem observável adicional JS/pixel do 00 |
| Browser da modal de justificativa | CT-35 prova action e gravação; domínio pendente Q?2 |
| GET da listagem afirmando só 200 | nenhum mutante discriminado; status/recorte Q?5 |
| CT de warning | sem RQ de auditoria de log; Proibição 12 |
| BVA 255/256 e mínimo monetário 0,01 | limites do PRD, sem fonte no 00; Q?1/Q?2 |
| Avisos de rejeição/final/cancelamento | fora de escopo A-11; CT-20/28 afirmam ausência com destinatários reais |
| Override de config em todos os BVA | não prova literal 5000.00; futuro CT lerá fábrica efetiva |
| Atomicidade com mundo sem destinatário/falha antes do efeito | não discrimina; lacuna até direção e arnês permitido |

## Índice de Cenários

Paths são **propostas; nenhum teste criado**. Negócio fora de tests/Kit; FeatureTenancy pendente exige registro do arnês antes da implementação.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo proposto | Mata |
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
| CT-14 | Centro sem gestor conserva o rascunho e informa a recusa | R3 | EP; estado/identidade | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-12 |
| CT-15 | Instância antiga não envia outra vez | R3 | EP; estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-11 |
| CT-16 | O gestor decide sua etapa corrente | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-18 |
| CT-17 | Gestor não aprova fora da sua etapa | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-19 |
| CT-18 | Aprovar exige a identidade do gestor do centro | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-15, M-16 |
| CT-19 | Solicitante que também é gestor decide a própria etapa | R4 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-17 |
| CT-20 | Rejeitar a etapa corrente devolve para correção | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-21, M-22, M-23 |
| CT-21 | Sem etapa pendente, rejeitar não altera o agregado | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-24 |
| CT-22 | Cada verbo de rejeição exige o aprovador corrente | R5 | estado/identidade | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-20 |
| CT-23 | Corrigir o centro e reenviar usa o gestor atual | R6 | 2-switch | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-26 |
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
| CT-36 | Confirmar envio/cancelamento grava a transição correspondente | R10 | decisão; EP | Componentes | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-39 |
| CT-37 | Transições sobre ID removido não produzem efeitos em outro registro | R11 | EP por operação | Domínio | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-40, M-41, M-42 |

## Sem CT-B

Nenhuma costura browser. Status/histórico e operações determinados são observáveis por componente. JS=Sim no 01 não basta para exigir execução JS, pixel ou acessibilidade como oráculo. Não criado 05; **CT-B: 0**. Template-05/pest-plugin-browser não abertos porque a condição não ocorreu. Se surgir CT-B, rule local testes-browser.md proíbe paralelo e prevalece sobre paralelo condicional da skill.

## Revisão adversarial e fechamento

**PENDENTE**. Obrigatória por completo/Impacto 3. Sessão principal despacha contexto novo, sem conversa do derivador, somente 00 e este 04 (05 e glossário inexistentes). Rota proposta: adversário-ct via ferramentas Codex, GPT-6 herdado, deployment exato não exposto; sem alias Claude. Nenhum adversário despachado pelo derivador, nenhuma autorrevisão. Rodadas: 0; achados ainda não avaliados, não “zero comprovado”. Máximo duas rodadas; segunda somente se fechamento criar cenário novo. Sessão decide cada destino: cenário novo, oráculo reescrito, lacuna declarada. Quotas antigas não valem; zero comprovado é válido após revisão integral.

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
