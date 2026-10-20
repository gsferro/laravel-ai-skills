# Casos de Teste — FERRO-830: aprovação de solicitação de compra

> Derivado do **requisito**, não do plano. Fonte: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`.
> Plano consultado integralmente conforme a rodada, mas utilizado somente para paths, rotas, stack e Superfície de UI.
> Nenhuma implementação desta feature, conjunto anterior ou relatório de rodada foi consultado.
> Skills: feature-wiki **[VERSÃO ANONIMIZADA]**, step **7**; feature-test-design **[VERSÃO ANONIMIZADA]**, passos **0–7**.
> Host: **Codex**, modelo da sessão **GPT-6** (identidade informada pelo host; variante e esforço não expostos).
> Data: **2026-10-20**. Entrega: especificação; testes, mutação e execução da aplicação **não realizados**.
> **02 ausente no oráculo**: Superfície Livewire sem inventário autoritativo. Nenhum 02 ou 03 foi criado.
> Revisão adversarial: **2 rodadas independentes, 10 + 5 achados fechados; encerramento da rodada 2 pela sessão, sem terceira revisão pelo teto**.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Decisão do passo 0 |
|---|---|---|---|---|---|
| Cadastro e correção dos dados | 2 | 3 | 6 | padrão | Formulário + persistência; valor monetário. |
| Fluxo, alçada, rejeição e reenvio | 3 | 3 | 9 | completo | Muitas condições, dinheiro e estados terminais. |
| Identidade, administração e isolamento por organização | 3 | 3 | 9 | completo | Autorização, associação de dados e escalada de privilégio. |
| Retry, concorrência e atomicidade | 3 | 3 | 9 | completo | Leituras concorrentes e decisões incompatíveis. |
| Notificação por e-mail | 3 | 3 | 9 | completo | Integração externa e destinatários de organizações distintas. |
| Status, histórico e listagem | 2 | 2 | 4 | padrão | Componente existente, retrabalho por informação errada. |

Todos os perfis foram **decididos pelo passo 0**, nenhum foi imposto. Há **Impacto 3**; revisão adversarial obrigatória sobre o conjunto inteiro.
Regra que atravessa áreas herda o maior perfil. Áreas padrão: passos 1–7 sem pairwise, BVA 2-valores quando houver limite decidido.
Áreas completas: passos 1–7 integrais, BVA 3-valores, decisão completa e todas as células inválidas de estado.
Não há três parâmetros independentes de configuração decididos: papel e estado se condicionam; tabela de decisão completa substitui pairwise.
Limites de texto e domínio monetário não decididos ficam como lacunas Q1/Q2/Q7, sem valores inventados.

Cenários: 75 · Regras: 24 · Mutantes previstos: 99 · Sem matador: 1
CT-B: 2. Esquemas contam uma vez; suas linhas são obrigações executáveis distintas.

## Varredura SFDIPOT

| Letra | Levantamento anterior aos cenários | Cobertura ou lacuna |
|---|---|---|
| S | Solicitação, centro de custo, histórico, permissões e Resources do app; tabelas identificadas pelo plano apenas como endereços. | R1–R5, R17–R22. |
| F | Criar, editar, excluir, enviar, aprovar, rejeitar, cancelar, consultar e notificar; administrar o gestor muda autoridade. | R1–R24. |
| D | Descrição, valor decimal, centro, solicitante, gestor, diretores 0/1/N, justificativa, participantes históricos e outra organização. | R7, R9, R14, R16, R19, R20; limites abertos Q1/Q2/Q7. |
| I | Páginas Filament e chamadas diretas do domínio. Nenhuma API/job de compra foi pedida; chamadas diretas representam esses possíveis consumidores sem criar endpoints. | Costuras G1–G6; Superfície Livewire incompleta, L1. |
| P | PHP 8.4.10; lock Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1, browser 5.0.1, mutate 5.0.2; SQLite em memória no arnês existente. | Validação estática; vendor vazio, nenhuma execução. Concorrência real requer DB compartilhado, CT-41. |
| O | Usuário comum, gestor específico, diretores da organização, administrador; pessoas distintas por padrão e sobrepostas nas sondas. | R4, R8, R18, R19, R23. Volumetria de listagem em CT-50. |
| T | Ordem gestor/diretor, reenvio, repetição, leitura obsoleta, corrida e persistência histórica. Sem SLA, vencimento ou calendário de aprovação no 00. | R10–R13, R16; fuso de apresentação aberto Q10, sem inventar DST como regra de aprovação. |

## Matriz única de estado × operação

Montada antes do mapa de regras, a partir dos cinco estados previstos como nomes de superfície e dos oito verbos da solicitação.
**5 estados × 8 operações = 40 células: 19 válidas e 21 inválidas.** As três edições de campos são dimensões da coluna editar.
Criar não atua sobre registro existente; fica em R1, fora do produto. Exclusão física é ausência do registro, coberta separadamente em R22.
Consultar inclui **listagem e detalhe**, cada qual realmente executado nos CT-48/49; não se empresta evidência de uma tela à outra.
Cancelar em rascunho é inválido por **A-06 dada**, sem reabrir essa premissa.

| Estado de partida | editar | excluir | enviar | aprovar | rejeitar | cancelar | listar | detalhar |
|---|---|---|---|---|---|---|---|---|
| rascunho | V CT-05/06 | V CT-09/10 | V CT-17/18 | I CT-26 | I CT-27 | I CT-37 | V CT-48 | V CT-49 |
| aguardando_gestor | I CT-14 | I CT-15 | I CT-19 | V CT-22/25 | V CT-30/31/33 | V CT-36 | V CT-48 | V CT-49 |
| aguardando_diretor | I CT-14 | I CT-15 | I CT-19 | V CT-25 | V CT-30/31/33 | V CT-36 | V CT-48 | V CT-49 |
| aprovada | I CT-14 | I CT-15 | I CT-19 | I CT-26 | I CT-27 | I CT-37 | V CT-48 | V CT-49 |
| cancelada | I CT-14 | I CT-15 | I CT-19 | I CT-26 | I CT-27 | I CT-37 | V CT-48 | V CT-49 |

Legenda auditada: **V** executa a operação elegível e afirma o resultado persistido; **I** executa a própria operação e recusa.
Todo I preserva situação, descrição, valor, centro, solicitante e organização persistidos. Por operação:
- editar: afirma os três campos anteriores, inclusive valor e centro em trânsito; sem novo histórico ou e-mail;
- excluir: registro e histórico anteriores permanecem; nenhum e-mail;
- enviar: situação anterior, histórico intacto e **nenhum e-mail ao gestor existente**;
- aprovar: situação e histórico intactos, **nenhum e-mail aos diretores existentes**;
- rejeitar: situação e histórico intactos, sem e-mail aos participantes existentes;
- cancelar: situação e histórico intactos, sem e-mail aos participantes existentes.
Os fakes são reiniciados **depois** das transições de preparação. A ausência não é contagem total que inclui o setup.

A matriz fixa atores elegíveis para isolar o estado. R4/R8 variam identidade e operação separadamente; CT-14 varia os campos fora do rascunho.
Não se usa a autorização de aprovar como prova da autorização de rejeitar, nem editar como prova de excluir.

## Mapa de Regras

| Regra | Área/perfil herdado | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — Criar solicitação com os dados de compra | Cadastro (padrão) | RQ-01; A-01 | EP e gravação por entrada | CT-01, CT-02, CT-03, CT-04 |
| R2 — Corrigir dados somente em rascunho | Cadastro (padrão) | RQ-01/02/09 | EP criação ≠ edição; campos e salvamento | CT-05, CT-06, CT-07, CT-08 |
| R3 — Excluir rascunho pelo solicitante | Identidade (completo) | RQ-03; A-05/A-06 | Estado × operação; identidade; ação destrutiva | CT-09, CT-10, CT-11 |
| R4 — As ações do solicitante conferem sua identidade | Identidade (completo) | RQ-02/03/04/11; fora de escopo de edição do aprovador | Matriz papel × ação completa e par UI/domínio | CT-12, CT-13 |
| R5 — Dados e existência ficam congelados fora do rascunho | Fluxo (completo) | RQ-02/03/10; A-05; fora de escopo da reabertura de cancelada | Matriz estado × operação, campo e persona | CT-14, CT-15, CT-16 |
| R6 — Enviar encaminha somente ao gestor do centro escolhido | Fluxo (completo) | RQ-04; A-02/A-10/A-11 | EP, estado × operação e destinatário 0/1 | CT-17, CT-18, CT-19, CT-20, CT-21 |
| R7 — Alçada usa comparação estrita e o limite configurável | Fluxo (completo) | RQ-05; A-04 | BVA 3-valores em centavos; criação/edição/uso | CT-22, CT-23, CT-24 |
| R8 — Somente o aprovador da etapa corrente decide | Identidade (completo) | RQ-04/05/06/10; A-02/A-03/A-05/A-07 | Tabela de decisão completa; estado × evento; papel × verbo | CT-25, CT-26, CT-27, CT-28, CT-29, CT-74 |
| R9 — Toda rejeição exige justificativa no domínio | Fluxo (completo) | RQ-07/08; A-07/A-12 | EP de ausência e tipo; BVA no mínimo de conteúdo existente | CT-30, CT-31, CT-32 |
| R10 — Rejeição permite corrigir e recomeçar sem apagar decisões anteriores | Fluxo (completo) | RQ-08/09/13; A-12 | 2-switch e domínio condicionado pela correção | CT-33, CT-34, CT-35 |
| R11 — Somente o solicitante cancela antes da decisão final | Fluxo (completo) | RQ-11; A-05/A-06/A-11 | Estado × operação e identidade | CT-36, CT-37, CT-38 |
| R12 — Repetir uma intenção elegível não duplica o efeito da transição | Retry (completo) | RQ-02/03/04/05/06/07/08/10/11/13/14 | Idempotência no agregado persistido; retry sequencial e leitura obsoleta | CT-39, CT-40 |
| R13 — Uma decisão vence a corrida e a escrita composta é atômica | Retry (completo) | RQ-04/05/06/08/10/11/13/14 | Concorrência real e rastreio de atomicidade | CT-41, CT-42 |
| R14 — E-mail alcança o próximo aprovador uma única vez | Notificação (completo) | RQ-14; A-02/A-03/A-04/A-10/A-11 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | CT-43, CT-44, CT-45, CT-46, CT-47 |
| R15 — Listagem e detalhe mostram a situação corrente | Apresentação (padrão) | RQ-12; A-12 | EP exaustiva de estado; paginação | CT-48, CT-49, CT-50 |
| R16 — O histórico exibe as pessoas e preserva os ciclos | Apresentação (padrão) | RQ-13/09; A-12 | Rastreio histórico e EP de 0/1/N decisões | CT-51, CT-52 |
| R17 — Administrar centro de custo grava o gestor que define o fluxo | Identidade (completo) | RQ-01/04; A-01/A-02/A-08 | CRUD, par visita/gravação, criação ≠ edição | CT-53, CT-54, CT-55, CT-56 |
| R18 — Usuário comum não administra quem aprova | Identidade (completo) | RQ-01/04; A-03/A-08 | Papel × ação e autorização fora da UI | CT-57, CT-58, CT-59 |
| R19 — Nenhuma organização lê ou altera compras e centros de outra | Identidade (completo) | RQ-01/04/05/12/13/14; A-01/A-03 | IDOR por entidade e fronteira de associação na gravação | CT-60, CT-61, CT-62, CT-63, CT-73 |
| R20 — O cliente não escolhe identidade, organização ou decisões históricas | Identidade (completo) | RQ-01/04/05/10/13; A-01/A-02/A-03 | Mass assignment por tabela e fronteira de gravação | CT-64, CT-65 |
| R21 — Entradas públicas do componente preservam fronteiras com valor ou tipo inválido | Identidade (completo) | RQ-01/04/12/13; A-01/A-08 | Domínio inválido e tipo errado por entrada conhecida; discriminante nulo | CT-66, CT-67 |
| R22 — Registro removido e identificador inexistente não recebem escrita | Identidade (completo) | RQ-02/03/04; A-05 | Estado removido × operação; CRUD inexistente e saída de erro | CT-68, CT-69 |
| R23 — Papéis acumulados não eliminam etapas | Identidade (completo) | RQ-04/05/06; A-03/A-09 | Tabela de decisão e sondas par a par | CT-05, CT-09, CT-17, CT-25, CT-31, CT-36, CT-70, CT-71, CT-72, CT-75 |
| R24 — A interação JavaScript torna as ações e seus erros operáveis | Fluxo (completo) | RQ-04/07/08/12; A-10/A-12 | Interação JS e erro visível | CT-B01/CT-B02 (05) |

RQ-01–RQ-14 têm partes determinadas e CT. O 00 é anterior ao template atual: não tem coluna Estado nem seção P-nn.
As premissas **A-01–A-12** são dadas pela rodada e tratadas como decisões vigentes, inclusive A-06/A-09.
Nenhuma RQ inteira foi reaberta. Recortes não determinados estão listados em Q1–Q11 (exceto Q5, encerrada pela premissa A-03) e no checklist; a cobertura é parcial nesses recortes.

## Costuras de Teste

Propostas após o mapa e **confirmadas pela sessão principal em 2026-10-20**, usando a autorização desta rodada e o arnês existente.
A confirmação é de desenho do teste; não resolve perguntas de comportamento.

| Grupo | Regras | Costura | Existente ou nova | Por que prova | Confirmada |
|---|---|---|---|---|---|
| G1 Domínio | R1–R14, R17–R23 | Pest feature HTTP | Existente: TestCase/RefreshDatabase e chamadas diretas, molde tests/Kit/ConviteUsuarioExistenteTest.php | Persistência, autorização e efeitos por fora da UI. | sessão, 2026-10-20 |
| G2 Componente | R1–R11, R15–R21 | componente Livewire/Filament | Existente: Livewire::test e fillForm, tests/Kit/PaginasInfraTest.php | Formulário, gravação, tabela, ação e infolist. | sessão, 2026-10-20 |
| G3 Organização domínio | R8, R14, R18–R20 | Pest feature HTTP | Nova alocação em FeatureTenancy; reutiliza TenancyTestCase, noPainelDa e papelNaOrganizacao | permission.teams precisa existir antes das migrations; sem grupo kit. | sessão, 2026-10-20; registro do arnês ainda pendente |
| G4 Organização componente | R18–R21 | componente Livewire/Filament | Nova alocação em FeatureTenancy; mesmo arnês de tests/Tenancy/AdminDaOrganizacaoTest.php | IDOR e gravação forjada no contexto real da organização. | sessão, 2026-10-20; registro do arnês ainda pendente |
| G5 Concorrência | R13 | Pest feature HTTP | Nova variante do arnês com banco compartilhado e conexões/processos independentes | SQLite :memory: não representa duas conexões concorrentes. | sessão, 2026-10-20; execução futura obrigatória |
| G6 Interação JS | R24 | browser | Existente: tests/Browser, TestCase/RefreshDatabase, actingAs e plugin browser | Abertura real de modal, binding Alpine/Livewire e erro visível após submit. | sessão, 2026-10-20 |

Todos os cenários do 04 têm grupo e costura no índice. G6 torna o **05 obrigatório**.
A presença de “JS: Sim” no plano, sozinha, não fundamenta Browser: visibilidade, gravação e validação continuam em G2/G4.

## Fronteira com o Plano

| Item do 01 | Tratamento | Motivo |
|---|---|---|
| Paths de models, Resources, notification e tabelas; nomes de métodos e rotas | Usados apenas como endereço técnico, a confirmar na materialização. | Não são comportamento esperado. |
| Referências a CT-04, CT-11, CT-14, CT-18 e ordem do conjunto antigo | Recusadas como fonte de casos e IDs. | Esta derivação tem numeração própria. |
| descricao max 255, nome max 120, valor mínimo 0.01, decimal(12,2) | Não viram limites de aceite. Q1/Q2/Q7. | Nenhum desses limites foi decidido no 00. |
| Nome único por organização e normalização do nome | Q7; sem cenários direcionais de duplicidade. | Escolha do plano que muda aceitação de cadastro. |
| E-mail com corpo, valor formatado, botão e URL | Q3; CT de envio prova canal/destinatários, sem inventar conteúdo obrigatório. | O 00 pede e-mail, sem definir link ou texto. |
| Cores do badge e rótulos de erro literais | Não são oráculos. | RQ-12 afirma situação semanticamente correta, sem paleta. |
| Filtro e ordenação padrão | Sem funcionalidade nova de filtro; entrada forjada tem só invariantes de isolamento e integridade. | Só o plano decide o filtro. |
| Gate antigo “duas telas + duas personas” | Substituído pelo gate da skill atual. | Browser precisa de observável exclusivo de navegador. |
| Logs do plano, SQL condicional, transações, traits e ShouldQueue | Mecanismos, não resultados exigidos, exceto warning expressamente dado em A-10. | CT-20 observa esse warning da premissa; nenhum texto/channel do 01 é imposto. |
| Tabela de etapas sem tenant/uuid porque “filha protegida pelo pai” | Não aceita como dispensa de controle. | 02/vendor ausentes; CT-63/65 tentam violar o histórico pelo cliente; acesso direto da filha permanece lacuna L1. |

## Perguntas para o 00-requisito.md

**Desvio autorizado:** o 00 é imutável; perguntas ficam aqui, prontas para colagem. Não foram enviadas ao usuário indisponível.
Não convertem uma recomendação em cenário esperado. O invariante já determinado continua testado.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | ❓ raia: requisito · Quais mínimo, máximo e política para valor zero, negativo, não numérico ou com mais de duas casas, na criação, edição e envio? | RQ-01/05 | ➡️ Recusar valores monetários sem representação válida; confirmar bordas e arredondamento antes de aceitar. O limiar 5000.00/5000.01 já está decidido. | aberta, só recorte de domínio não definido |
| Q2 | ❓ raia: requisito · Quais tetos para descrição e justificativa, e qual tratamento de espaços nas bordas e descrição só de espaços? | RQ-01/07 | ➡️ Definir limites explícitos e recusar excesso; justificativa ausente/vazia permanece recusada por RQ-07. Não adotar 255 do plano. | aberta |
| Q3 | ❓ raia: requisito · Quem consulta solicitações da mesma organização, incluindo ex-gestor/participante histórico, e o e-mail terá link para qual destino? | RQ-12/13/14 | ➡️ Restringir ao recorte autorizado, preservar consulta de quem precisa agir e definir destino autorizado do link. Sem link ou escopo inventado. | aberta apenas para público adicional e contrato do e-mail |
| Q4 | ❓ raia: requisito · O que ocorre se não houver diretor no encaminhamento de valor alto? | RQ-05/14 | ➡️ Falhar fechado com explicação, sem aprovação final automática; decisão de recusar encaminhamento ou aguardar cadastro continua pendente. | aberta |
| Q5 | ❓ raia: requisito · A acumulação de solicitante/diretor ou gestor/diretor muda autoridade? | RQ-05/06; A-03/A-07/A-09 | ➡️ Encerrada pela premissa dada: qualquer diretor da organização decide; nenhuma exceção de segregação foi estabelecida. CT-75 cobre os dois pares e verbos. | encerrada — A-03 já vigente, ADV-09 |
| Q6 | ❓ raia: requisito · Troca de gestor durante etapa pendente usa gestor atual ou o do envio? | RQ-04/06 | ➡️ Não aceitar decisão de pessoa sem vínculo validado; definir referência temporal antes de permitir substituição. | aberta |
| Q7 | ❓ raia: requisito · Qual teto e normalização do nome do centro? É único por organização e pode ser recriado depois de excluído? | RQ-01/04, A-01 | ➡️ Definir colisão e teto; recusar ambiguidades de identidade até haver contrato. | aberta |
| Q8 | ❓ raia: requisito · A página de compra sem tenant corrente deve negar acesso ou redirecionar para seleção? | RQ-01/12, A-01 | ➡️ Falhar fechado na fronteira do painel. A consulta global fora de request é convenção deliberada e não deve ser confundida com vazamento de UI. | aberta só para resposta/saída exatas |
| Q9 | ❓ raia: requisito · Criação repetida tem chave de intenção ou cria duas solicitações legítimas? | RQ-01 | ➡️ Definir chave e prazo de deduplicação antes de prometer idempotência de criação; não deduplicar compras distintas por descrição/valor. | aberta |
| Q10 | ❓ raia: requisito · Qual fuso e formato de exibição de “quando” no histórico? | RQ-13, A-12 | ➡️ Definir o fuso explicitamente e conservar o instante; sem converter isso em SLA ou validade de aprovação. | aberta |
| Q11 | ❓ raia: requisito · Alterar o limite configurável durante tramitação usa valor do envio ou da decisão? | RQ-05, A-04 | ➡️ Não dispensar segunda aprovação por mudança silenciosa; confirmar a política temporal. | aberta |

## Setup Global

### Arnês e personas

- Usar os termos do 00: solicitante **Sofia (S)**, gestor do centro **Guilherme (G)**, diretor **Dora (D1)**, diretor **Davi (D2)**, outro gestor **Gustavo (G2)** e usuário comum **Otávio (O)**. Pessoas distintas, salvo CT-70–72.
- Administradora **Alice** tem `admin_organizacao`; não usar `master_global` para provar permission.
- Organizações **Acme (A)** e **Globex (B)**. Vincular membros pela relação de tenants e atribuir papéis com `papelNaOrganizacao()`, não sync de pivot. G/G2 são gestores de centros distintos, não papel global de gestor.
- `User::factory()` e `Tenant::factory()` existem; states verificados: User `unverified()`, Tenant `comIdentidadeVisual()` e `inativo()`. Não usar state de compra inventado.
- Não há factory de CentroCusto/SolicitacaoCompra nas factories inspecionadas. Preparar centro por `CentroCusto::create()` autorizado; criar solicitação pelo mesmo ponto de domínio autorizado usado em produção, com defaults reais de rascunho/solicitante. Nomes novos do helper são proposta de materialização, não API existente.
- Helper futuro `solicitacaoEm($situacao, $dados)` em `tests/Pest.php`: nasce em rascunho e chama transições **reais** `enviar`, `aprovar` e `cancelar`. Nunca grava status de fixture à força. Para `aguardando_diretor`, usar 6000.00, enviar e aprovar como G; para aprovada, concluir rota legal; para cancelada, enviar e cancelar.
- Guardar baseline de campos e tuplas históricas **após** montar a partida; depois instalar/limpar fakes. Não contar e-mails nem etapas do setup como efeitos do Quando.
- Padrão `tests/Feature`: TestCase + RefreshDatabase. `tests/Unit` não recebe TestCase da aplicação; nenhum cenário de persistência foi empurrado para Unit.
- G3/G4: planejar `tests/FeatureTenancy/AprovacaoCompra/` com TenancyTestCase antes das migrations e entrada própria no Pest.php/phpunit.xml, fora de kit. Ainda não está registrado no projeto. Reutilizar `noPainelDa()` para painel, tenant e PermissionRegistrar; limpar relações de papéis ao alternar organização.
- Especificação não modifica esses arquivos. Caminhos do índice são **destinos propostos, ainda sem testes**, não evidência de execução.

### Observáveis e APIs

- Domínio: chamar o ponto público de escrita **sem Livewire**, com ator explícito/autenticado conforme contrato futuro. Para editar/excluir, não criar um service artificial só para satisfazer o CT. Usar a escrita pública real; se só houver Eloquent, executar save/delete direto e detectar guarda ausente.
- Componentes: `Livewire::test()`, autenticação antes, `fillForm()` e `call('create')` / `call('save')`, depois conferir **todos** os campos persistidos. Edição não exige redirect.
- Ações: `callAction(TestAction::make('enviar')->table($registro))`, equivalentes para outros verbos; `assertActionVisible`/`assertActionHidden`. Não usar helpers deprecated `callTableAction`/`assertFormSet`.
- `Notification::fake()` prova destinatário, solicitação, etapa e **canal mail** com callback inspecionando canais; contagem exata por destinatário e total. Não basta classe de notification. Para prova de fila/atomicidade, não combinar um fake que impeça justamente o efeito observado.
- Autorização/validação: recusa pode ser exceção de domínio, validação ou resposta controlada. Não cravar classe/mensagem não decidida. Assertar recusa e não-efeitos concretos; erro em campo de formulário deve nomear o campo visado.
- Recusas com HTTP 403/404 ou redirects têm cenário irmão CT-59/69 que alcança uma página autorizada. Resposta 200, por si só, nunca é oráculo.
- Inteiros monetários dos exemplos são strings decimais (`'4999.99'`), jamais floats. Precisão e normalização além do contrato permanecem Q1.

### Decisões de mecanismo e evidência do ambiente

- D1, `@premissa`: exclusão da solicitação é física, usando a superfície prevista; CT-68 prova escrita após remoção. Soft delete é alternativa não adotada, não dispensa a prova.
- D2, `@premissa`: limite de fábrica de A-04 será testado em bootstrap com variável KIT_COMPRAS_LIMITE_DIRETOR ausente, sem config injetada, confirmando leitura efetiva **5000.00**. Não confiar em phpunit.xml/.env.testing; estes não podem sobrepor a chave neste caso. CT-23 varia limite deliberadamente; CT-22 fixa o literal do requisito.
- D3, `@premissa`: corrida real CT-41 usa duas conexões/processos no mesmo DB de teste descartável, barreira de sincronização após ambas as leituras elegíveis e antes das gravações, sem RefreshDatabase invólucro que esconda fixtures entre conexões. Estado obsoleto CT-40 **não** é concorrência simultânea.
- Provas negativas locais: `composer show --direct` respondeu **“No dependencies installed”**; `vendor/autoload.php=False`, `vendor/composer/installed.json=False`; a pasta vendor existe vazia. `git status` respondeu **“not a git repository”**.
- Versões acima são do **composer.lock**, não instalação comprovada. Mutate está no lock transitivamente pelo Pest, **não** no require-dev do composer.json. Não alterar dependências nesta rodada.
- `php -v`: 8.4.10; `php -m` contém **pcov, xdebug, pdo_sqlite, pdo_mysql e pdo_pgsql**. Não alegar falta de driver.
- Boost `search-docs` não consta nas ferramentas expostas. Fallback: documentação oficial de [testes Filament 5](https://filamentphp.com/docs/5.x/testing/testing-resources), [ações Filament 5](https://filamentphp.com/docs/5.x/testing/testing-actions), [Livewire 4](https://livewire.laravel.com/docs/4.x/testing), [notificações Laravel 13](https://laravel.com/framework/docs/13.x/notifications#testing) e [Pest browser](https://pestphp.com/docs/browser-testing). API foi especificada por essas fontes e convenções lidas; inspeção exata de vendor/deprecations fica pendente, sem fingir que ocorreu.
- Fontes do projeto: .ai/rules/index.md, testes.md, testes-browser.md, filament.md; wikis/convencoes.md; tests/Pest.php, TestCase.php, TenancyTestCase.php, phpunit.xml; moldes PaginasInfraTest, AdminDaOrganizacaoTest e PerfisTest. Glossário não existe; usar vocabulário literal do 00.

**Precedência declarada:** A-10 do 00 exige warning na recusa sem gestor. A instrução da rodada de respeitar as premissas dadas prevalece sobre a proibição genérica de derivar CT de logs. CT-20 verifica somente esse nível/motivo, sem importar formato ou channel do PRD.

D6, @premissa de mecanismo: para CT-51/52, controlar o relógio antes de cada transição real, com criação e decisões em dias distintos. Fixture temporal em UTC; restaurar relógio/contexto ao sair do cenário. Comparar instantes literais por evento sem reaproveitar o formatter de produção como oráculo. Isso não decide o fuso/formato geral de Q10.

## Regra R1 — Criar solicitação com os dados de compra

> Origem: RQ-01; A-01 · perfil **padrão** · técnica: **EP e gravação por entrada**.

Quatro cenários excedem teto padrão de três: gate de validação externa e gate de gravação/erro do formulário provam falhas diferentes. BVA de limites não decididos permanece Q1/Q2.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Criar solicitação com os dados de compra

    Cenário: [CT-01] Persistir os três dados e o solicitante autenticado
      Dado Sofia autorizada e o centro Acme com Guilherme como gestor
      Quando Sofia cria fora da UI uma solicitação com descrição "Teclado ergonômico 🛒", valor "123.45" e esse centro
      Então existe uma solicitação em rascunho com exatamente essa descrição, valor "123.45", centro, solicitante Sofia e organização Acme
      E não existe etapa de aprovação nem e-mail emitido por essa criação
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Criar solicitação com os dados de compra

    Cenário: [CT-02] O formulário de criação grava os dados de compra
      Dado Sofia autorizada na página create, sem solicitação anterior com descrição "Monitor"
      Quando Sofia grava pelo componente descrição "Monitor", valor "5000.01" e o centro Acme
      Então o banco contém esses três valores, situação rascunho e solicitante Sofia na Acme
      E nenhum e-mail ao gestor existente ou aos diretores existentes foi enviado
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Criar solicitação com os dados de compra

    Esquema do Cenário: [CT-03] A ausência de um dado obrigatório é recusada também fora da UI
      Dado Sofia autorizada com payload válido e nenhum registro a alterar
      Quando Sofia cria fora da UI substituindo somente <campo> por <entrada>
      Então a criação é recusada por <campo>, não existe solicitação parcial e não existe etapa
      E nenhum e-mail é enviado ao gestor e aos diretores existentes
      
      Exemplos:
        | campo           | entrada | partição          |
        | descricao       | ausente | descrição omitida |
        | descricao       | null    | descrição nula    |
        | descricao       | ""      | descrição vazia   |
        | valor           | ausente | valor omitido     |
        | valor           | null    | valor nulo        |
        | centro_custo_id | ausente | centro omitido    |
        | centro_custo_id | null    | centro nulo       |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Criar solicitação com os dados de compra

    Esquema do Cenário: [CT-04] O formulário identifica isoladamente o dado obrigatório ausente
      Dado Sofia autorizada no create com todos os outros dados válidos
      Quando Sofia grava omitindo apenas <campo>
      Então o componente mostra erro em <campo> e nenhuma solicitação ou etapa é persistida
      E não há e-mail ao gestor e aos diretores existentes
      
      Exemplos:
        | campo           | partição         |
        | descricao       | sem descrição    |
        | valor           | sem valor        |
        | centro_custo_id | sem centro       |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Aceitar descrição ausente na criação do domínio | CT-03 | Recusa específica de descricao e contagem de solicitações permanece zero. |
| M-02 | Tornar só o formulário obrigatório, sem validação no ponto de escrita | CT-03, CT-04 | CT-03 recusa sem componente; CT-04 identifica cada campo na UI. |
| M-03 | Gravar valor na escala errada ou esquecer centro na criação | CT-01, CT-02 | descricao, valor decimal literal e centro exatos no registro, não só PK. |

## Regra R2 — Corrigir dados somente em rascunho

> Origem: RQ-01/02/09 · perfil **padrão** · técnica: **EP criação ≠ edição; campos e salvamento**.

Quatro cenários: estouro padrão justificado por validação fora da UI e no save, mais gravação de campos que decidem o fluxo. Repetição não decorativa da criação. As linhas sem alteração de CT-05/53 afirmam integridade, não prometem sucesso de no-op nem são citadas como matadoras de uma recusa segura.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Corrigir dados somente em rascunho

    Esquema do Cenário: [CT-05] Cada campo editável muda no rascunho pelo domínio
      Dado solicitação de Sofia em rascunho com "Teclado", "4999.99", centro de Guilherme e papel adicional de Sofia <adicional>
      Quando Sofia altera fora da UI somente <campo> para <novo>
      Então o valor de <campo> persistido é <novo> e os outros dois dados permanecem anteriores
      E situação rascunho, solicitante e organização permanecem iguais, sem nova etapa ou e-mail
      
      Exemplos:
        | campo           | novo                   | adicional           | partição                |
        | descricao       | Teclado revisão 2      | nenhum              | descrição               |
        | valor           | 5000.01                | nenhum              | valor decisivo          |
        | centro_custo_id | centro de Gustavo      | nenhum              | centro decisivo         |
        | descricao       | Teclado                | nenhum              | sem alteração           |
        | valor           | 5000.01                | admin_organizacao   | solicitante mais admin  |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Corrigir dados somente em rascunho

    Cenário: [CT-06] A edição do formulário persiste valor e centro novos
      Dado solicitação de Sofia em rascunho com "Teclado", "4999.99" e centro de Guilherme
      Quando Sofia salva pelo componente "Tela", "5000.01" e o centro de Gustavo
      Então o mesmo registro contém "Tela", "5000.01" e centro de Gustavo, ainda em rascunho
      E não se criou outra solicitação, etapa ou e-mail; solicitante e organização foram preservados
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Corrigir dados somente em rascunho

    Esquema do Cenário: [CT-07] A edição não contorna dados obrigatórios fora da UI
      Dado solicitação de Sofia em rascunho com dados válidos e snapshot persistido
      Quando Sofia salva fora da UI somente <campo> como <entrada>
      Então a escrita é recusada pelo campo indicado e todos os dados persistidos continuam no snapshot
      E histórico e e-mails não ganham entradas para gestor e diretores existentes
      
      Exemplos:
        | campo           | entrada | partição           |
        | descricao       | null    | descrição nula     |
        | descricao       | ""      | descrição vazia    |
        | valor           | null    | valor nulo         |
        | centro_custo_id | null    | centro nulo        |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Corrigir dados somente em rascunho

    Esquema do Cenário: [CT-08] O save valida novamente os dados obrigatórios
      Dado solicitação de Sofia em rascunho aberta no edit com outros campos válidos
      Quando Sofia salva pelo componente somente <campo> como null
      Então há erro específico em <campo> e o registro conserva os três dados anteriores
      E situação, histórico e e-mails aos aprovadores existentes não mudam
      
      Exemplos:
        | campo           | partição        |
        | descricao       | descrição nula  |
        | valor           | valor nulo      |
        | centro_custo_id | centro nulo     |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-04 | Aplicar obrigatoriedade somente na criação | CT-07, CT-08 | Save recusa individualmente os campos nulos sem alterar o registro. |
| M-05 | Atualizar descrição e esquecer valor ou centro | CT-05, CT-06 | Novo valor 5000.01 e novo centro persistem no mesmo registro. |
| M-06 | Implementar edição como criação de outro registro | CT-05, CT-06 | A PK original recebe os novos valores; contagem não cresce e nenhum registro substituto é criado. |

## Regra R3 — Excluir rascunho pelo solicitante

> Origem: RQ-03; A-05/A-06 · perfil **completo** · técnica: **Estado × operação; identidade; ação destrutiva**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Excluir rascunho pelo solicitante

    Esquema do Cenário: [CT-09] O solicitante exclui seu rascunho por fora do componente
      Dado solicitação de Sofia em rascunho de origem <origem>, papel adicional de Sofia <adicional>, outra solicitação de Otávio com histórico identificável e aprovadores reais
      Quando Sofia exclui diretamente seu rascunho
      Então o registro de Sofia deixa de existir e o de Otávio conserva todos os dados e tuplas históricas
      E não são enviados e-mails aos gestores e diretores existentes
      
      Exemplos:
        | origem                     | adicional         | partição                         |
        | criação inicial            | nenhum            | rascunho sem decisão             |
        | rejeição real pelo gestor  | nenhum            | rascunho com rejeição G           |
        | rejeição real pelo diretor | nenhum            | rascunho com aprovação G e rejeição D |
        | rejeição real pelo diretor | admin_organizacao | solicitante administrador com histórico |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Excluir rascunho pelo solicitante

    Cenário: [CT-10] Excluir pela ação remove o rascunho correto
      Dado dois rascunhos de Sofia exibidos na tabela e registro alvo com descrição "Excluir este"
      Quando Sofia executa a ação excluir do componente para o alvo
      Então somente "Excluir este" deixa de existir e a outra solicitação permanece
      E nenhum e-mail é enviado aos aprovadores existentes
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Excluir rascunho pelo solicitante

    Esquema do Cenário: [CT-11] Pessoa diferente não exclui o rascunho alheio
      Dado rascunho de Sofia, atores com acesso ao painel e solicitante Sofia distinto de <ator>
      Quando <ator> tenta excluí-lo diretamente fora da UI
      Então a exclusão é recusada e o registro conserva todos os campos
      E nenhuma etapa é removida ou acrescentada e não há e-mail aos aprovadores existentes
      
      Exemplos:
        | ator                    | partição             |
        | Otávio                  | outro solicitante    |
        | Guilherme               | gestor               |
        | Dora                    | diretora             |
        | Alice                   | administração        |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-07 | Excluir sem conferir dono do registro | CT-11 | Cada ator diferente é recusado e o rascunho de Sofia existe. |
| M-08 | Esconder exclusão na UI, permitindo delete direto | CT-09, CT-11 | Delete próprio funciona e delete alheio direto conserva a linha. |
| M-09 | Vincular DeleteAction ao registro errado da tabela | CT-10 | Só o alvo some; outro rascunho com mesma dona permanece. |
| M-90 | Impedir excluir rascunho devolvido porque já possui histórico | CT-09 | As duas partidas após rejeição real também deixam de existir; compra de contraste conserva histórico. |

## Regra R4 — As ações do solicitante conferem sua identidade

> Origem: RQ-02/03/04/11; fora de escopo de edição do aprovador · perfil **completo** · técnica: **Matriz papel × ação completa e par UI/domínio**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: As ações do solicitante conferem sua identidade

    Esquema do Cenário: [CT-12] Nem papel de aprovador nem administração substituem o solicitante
      Dado solicitação de Sofia em <partida>, ator <ator> distinto de Sofia e aprovadores reais
      Quando <ator> executa diretamente <operacao>
      Então a operação é recusada e situação, descrição, valor, centro e existência do registro ficam iguais ao snapshot
      E não há etapa nova ou removida nem e-mail ao gestor e aos diretores
      
      Exemplos:
        | partida           | operacao                | ator       | partição      |
        | rascunho          | editar valor para 1.00   | Otávio     | outro dono    |
        | rascunho          | editar valor para 1.00   | Guilherme  | gestor        |
        | rascunho          | editar valor para 1.00   | Dora       | diretora      |
        | rascunho          | editar valor para 1.00   | Alice      | admin         |
        | rascunho          | enviar                  | Otávio     | outro dono    |
        | rascunho          | enviar                  | Guilherme  | gestor        |
        | rascunho          | enviar                  | Dora       | diretora      |
        | rascunho          | enviar                  | Alice      | admin         |
        | aguardando_gestor | cancelar                | Otávio     | outro dono    |
        | aguardando_gestor | cancelar                | Guilherme  | gestor        |
        | aguardando_gestor | cancelar                | Dora       | diretora      |
        | aguardando_gestor | cancelar                | Alice      | admin         |
        | aguardando_diretor| cancelar                | Otávio     | outro dono    |
        | aguardando_diretor| cancelar                | Guilherme  | gestor        |
        | aguardando_diretor| cancelar                | Dora       | diretora      |
        | aguardando_diretor| cancelar                | Alice      | admin         |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: As ações do solicitante conferem sua identidade

    Esquema do Cenário: [CT-13] A UI não oferece ação do solicitante a outra pessoa
      Dado solicitação de Sofia em <partida> e <ator> autorizado a consultar esse registro para a fixture
      Quando <ator> monta e tenta disparar pelo componente a ação <acao> sobre o registro de Sofia
      Então a ação não é oferecida e a tentativa não muda nenhum dado nem a existência do registro
      E histórico e e-mails aos aprovadores existentes permanecem no snapshot
      
      Exemplos:
        | partida            | ator      | acao     | partição       |
        | rascunho           | Guilherme | editar   | gestor         |
        | rascunho           | Guilherme | excluir  | gestor         |
        | rascunho           | Otávio    | enviar   | outro dono     |
        | aguardando_gestor  | Dora      | cancelar | diretora       |
        | aguardando_diretor | Guilherme | cancelar | antigo gestor  |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-10 | Autorizar dono OU permission genérica em vez de identidade | CT-12 | Alice e aprovadores são recusados mesmo com acesso ao painel. |
| M-11 | Conferir dono no envio e esquecer no cancelamento | CT-12 | Cancelar em ambas as etapas pelo não solicitante não muda estado. |
| M-12 | Conferir identidade apenas em policy ou apenas ocultar a ação | CT-12, CT-13 | Chamada direta e tentativa de ação não persistem; ação está oculta. |

## Regra R5 — Dados e existência ficam congelados fora do rascunho

> Origem: RQ-02/03/10; A-05; fora de escopo da reabertura de cancelada · perfil **completo** · técnica: **Matriz estado × operação, campo e persona**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Dados e existência ficam congelados fora do rascunho

    Esquema do Cenário: [CT-14] Nem o dono altera campo decisivo depois do envio
      Dado solicitação de Sofia em <partida>, dados "Teclado", "6000.00" e centro de Guilherme, e histórico anterior
      Quando Sofia tenta fora da UI editar somente <campo> para <novo>
      Então a edição é recusada, preservando "Teclado", "6000.00", centro de Guilherme e <partida> no banco
      E histórico anterior e e-mails aos gestores e diretores existentes ficam sem acréscimos
      
      Exemplos:
        | partida            | campo           | novo               | partição            |
        | aguardando_gestor  | descricao       | Texto novo         | trânsito descrição  |
        | aguardando_gestor  | valor           | 1.00               | trânsito valor      |
        | aguardando_gestor  | centro_custo_id | centro de Gustavo  | trânsito centro     |
        | aguardando_diretor | descricao       | Texto novo         | trânsito descrição  |
        | aguardando_diretor | valor           | 1.00               | trânsito valor      |
        | aguardando_diretor | centro_custo_id | centro de Gustavo  | trânsito centro     |
        | aprovada           | descricao       | Texto novo         | final descrição     |
        | aprovada           | valor           | 1.00               | final valor         |
        | aprovada           | centro_custo_id | centro de Gustavo  | final centro        |
        | cancelada          | descricao       | Texto novo         | terminal descrição  |
        | cancelada          | valor           | 1.00               | terminal valor      |
        | cancelada          | centro_custo_id | centro de Gustavo  | terminal centro     |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Dados e existência ficam congelados fora do rascunho

    Esquema do Cenário: [CT-15] Nem o dono exclui solicitação em trânsito ou terminal
      Dado solicitação de Sofia em <partida>, histórico conhecido e aprovadores reais
      Quando Sofia tenta excluí-la fora da UI
      Então a exclusão é recusada e a solicitação conserva existência, situação e todos os dados
      E nenhuma etapa histórica é removida ou criada e nenhum e-mail é enviado
      
      Exemplos:
        | partida            | partição             |
        | aguardando_gestor  | pendente de gestor   |
        | aguardando_diretor | pendente de diretor  |
        | aprovada           | aprovação terminal   |
        | cancelada          | cancelamento terminal|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Dados e existência ficam congelados fora do rascunho

    Esquema do Cenário: [CT-16] O componente não permite editar nem excluir fora do rascunho
      Dado solicitação de Sofia em <partida> com histórico conhecido
      Quando Sofia tenta a ação <acao> pelo componente
      Então a ação não é oferecida e a tentativa conserva existência, valor, centro, descrição e situação persistidos
      E não altera histórico nem envia e-mails aos aprovadores existentes
      
      Exemplos:
        | partida            | acao    | partição         |
        | aguardando_gestor  | editar  | gestor edit      |
        | aguardando_gestor  | excluir | gestor delete    |
        | aguardando_diretor | editar  | diretor edit     |
        | aguardando_diretor | excluir | diretor delete   |
        | aprovada           | editar  | aprovada edit    |
        | aprovada           | excluir | aprovada delete  |
        | cancelada          | editar  | cancelada edit   |
        | cancelada          | excluir | cancelada delete |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-13 | Travar somente descricao deixando valor e centro editáveis | CT-14 | Valor 6000.00 e centro original persistem inclusive nas duas etapas pendentes. |
| M-14 | Usar condição só para aprovada e permitir delete em trânsito | CT-15 | Registro e histórico sobrevivem em cada partida não rascunho. |
| M-15 | Política de formulário protege a UI mas save/delete direto ignora estado | CT-14, CT-15, CT-16 | Chamadas diretas recusam; ações do componente também não escrevem. |

## Regra R6 — Enviar encaminha somente ao gestor do centro escolhido

> Origem: RQ-04; A-02/A-10/A-11 · perfil **completo** · técnica: **EP, estado × operação e destinatário 0/1**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Enviar encaminha somente ao gestor do centro escolhido

    Esquema do Cenário: [CT-17] Envio direto deixa pendente do gestor específico
      Dado rascunho de Sofia em <centro>, papel adicional de Sofia <adicional>, Guilherme e Gustavo gestores de centros diferentes e Dora diretora
      Quando Sofia envia diretamente a solicitação
      Então a situação persistida é aguardando_gestor e há exatamente um e-mail mail ao <gestor>
      E não há decisão histórica, e o outro gestor, Sofia e Dora não recebem e-mail
      
      Exemplos:
        | centro              | gestor    | adicional         | partição                |
        | centro de Guilherme | Guilherme | nenhum            | primeiro centro         |
        | centro de Gustavo   | Gustavo   | nenhum            | segundo centro          |
        | centro de Guilherme | Guilherme | admin_organizacao | solicitante mais admin  |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Enviar encaminha somente ao gestor do centro escolhido

    Cenário: [CT-18] Enviar pela ação usa o registro e o centro corretos
      Dado rascunho de Sofia no centro de Gustavo e outro rascunho no centro de Guilherme
      Quando Sofia confirma a ação enviar do primeiro registro no componente
      Então somente esse registro passa a aguardando_gestor e Gustavo recebe um e-mail mail
      E o outro rascunho permanece rascunho, sem decisão histórica ou e-mail a Guilherme
      E a linha alvo no mesmo componente que executou a ação mostra aguardando_gestor após a resposta, sem recarga; a outra linha continua rascunho
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Enviar encaminha somente ao gestor do centro escolhido

    Esquema do Cenário: [CT-19] Reenvio fora de rascunho não encaminha novamente
      Dado solicitação de Sofia em <partida>, gestor Guilherme e diretores Dora e Davi existentes
      Quando Sofia chama enviar diretamente
      Então a chamada é recusada e o banco conserva a situação <partida> e os dados anteriores
      E histórico fica intacto e não há e-mail para Guilherme, Dora, Davi ou Sofia
      
      Exemplos:
        | partida            | partição        |
        | aguardando_gestor  | envio duplicado |
        | aguardando_diretor | pular gestor    |
        | aprovada           | reabrir final   |
        | cancelada          | reabrir cancelada|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Enviar encaminha somente ao gestor do centro escolhido

    Cenário: [CT-20] Sem gestor o envio falha fechado
      Dado rascunho de Sofia no centro sem gestor, outro centro com Gustavo e diretores reais Dora e Davi
      Quando Sofia tenta enviar diretamente
      Então o envio é recusado e a solicitação persiste em rascunho com os mesmos dados
      E não há decisão histórica ou e-mail a Gustavo, Sofia, Dora ou Davi
      E a recusa emite um registro no nível warning por falta de gestor, sem exigir texto ou channel do plano
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Enviar encaminha somente ao gestor do centro escolhido

    Cenário: [CT-21] O envio sem gestor apresenta recusa e mantém a solicitação corrigível
      Dado rascunho de Sofia no centro sem gestor aberto na listagem, com outro centro administrado existente
      Quando Sofia tenta enviar pela ação do componente
      Então a UI apresenta a razão de falta de gestor e o registro continua em rascunho
      E editar continua disponível a Sofia, sem nova etapa ou e-mail aos usuários existentes
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-16 | Resolver gestor por papel global em vez do centro da solicitação | CT-17, CT-18 | Centro de Gustavo notifica apenas Gustavo; outro registro não muda. |
| M-17 | Enviar sem validar o estado de partida | CT-19 | Quatro estados conservam situação e não notificam Guilherme existente. |
| M-18 | Pular aprovação ou enviar para gestor de outro centro quando não há gestor | CT-20, CT-21 | Rascunho é mantido; UI explica falta de gestor; Gustavo não é notificado. |
| M-19 | Apresentar situação anterior no componente após envio bem-sucedido | CT-18 | Na própria instância que executou enviar, a linha alvo mostra aguardando_gestor sem recarga. |
| M-91 | Omitir o warning da recusa sem gestor decidido explicitamente em A-10 | CT-20 | A tentativa sem gestor emite warning, além de manter rascunho e mostrar a recusa. |

## Regra R7 — Alçada usa comparação estrita e o limite configurável

> Origem: RQ-05; A-04 · perfil **completo** · técnica: **BVA 3-valores em centavos; criação/edição/uso**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Alçada usa comparação estrita e o limite configurável

    Esquema do Cenário: [CT-22] O valor literal de fábrica separa 5000.00 de 5000.01
      Dado limite efetivo de fábrica lido como "5000.00", sem override do teste ou ambiente, e solicitação de Sofia aguardando_gestor com <valor>
      Quando Guilherme aprova diretamente a etapa do gestor
      Então a situação persistida é <destino> com uma decisão aprovada de Guilherme na etapa gestor
      E os e-mails aos diretores reais Dora e Davi têm contagem <cada_diretor>, sem e-mail a Sofia ou ao gestor
      
      Exemplos:
        | valor   | destino             | cada_diretor | partição   |
        | 4999.99 | aprovada            | 0            | borda−0.01|
        | 5000.00 | aprovada            | 0            | borda     |
        | 5000.01 | aguardando_diretor  | 1            | borda+0.01|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Alçada usa comparação estrita e o limite configurável

    Esquema do Cenário: [CT-23] A configuração realmente muda a alçada
      Dado limite deliberadamente configurado em <limite> e solicitação aguardando_gestor com <valor>
      Quando Guilherme aprova diretamente
      Então a situação é <destino>, com uma aprovação de gestor e sem decisão de diretor
      E Dora e Davi recebem cada um <emails> e-mails mail
      
      Exemplos:
        | limite  | valor   | destino            | emails | partição                   |
        | 3000.00 | 2999.99 | aprovada           | 0      | limite reduzido borda−0.01|
        | 3000.00 | 3000.00 | aprovada           | 0      | limite reduzido borda     |
        | 3000.00 | 3000.01 | aguardando_diretor | 1      | limite reduzido borda+0.01|
        | 7000.00 | 6999.99 | aprovada           | 0      | limite aumentado borda−0.01|
        | 7000.00 | 7000.00 | aprovada           | 0      | limite aumentado borda     |
        | 7000.00 | 7000.01 | aguardando_diretor | 1      | limite aumentado borda+0.01|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Alçada usa comparação estrita e o limite configurável

    Esquema do Cenário: [CT-24] Centavos gravados na criação e na correção chegam íntegros à decisão
      Dado solicitação de Sofia em rascunho obtida por <entrada> com valor <valor>, relida do banco e enviada realmente ao gestor
      Quando Guilherme aprova esse valor persistido
      Então o banco conserva valor <valor> e a solicitação termina em <destino>
      E há uma aprovação de gestor; Dora e Davi existentes recebem cada um <emails> e-mails mail
      
      Exemplos:
        | entrada                         | valor   | destino            | emails | partição                |
        | criação direta                  | 4999.99 | aprovada           | 0      | criação abaixo          |
        | criação direta                  | 5000.00 | aprovada           | 0      | criação borda           |
        | criação direta                  | 5000.01 | aguardando_diretor | 1      | criação acima           |
        | edição direta de valor 6000.00   | 4999.99 | aprovada           | 0      | edição abaixo           |
        | edição direta de valor 6000.00   | 5000.00 | aprovada           | 0      | edição borda            |
        | edição direta de valor 4999.99   | 5000.01 | aguardando_diretor | 1      | edição acima            |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-20 | Comparar >= em vez de > | CT-22, CT-23 | 5000.00/7000.00 terminam aprovada e não notificam diretor. |
| M-21 | Truncar centavos antes da comparação | CT-22, CT-24 | 5000.01 permanece aguardando_diretor, não aprovada. |
| M-22 | Fixar 5000 no código ignorando configuração | CT-23 | 6999.99 e 7000.00 dispensam diretor com limite 7000.00. |
| M-23 | Persistir como centavos ou descartar valor corrigido | CT-24 | Valor decimal exato relido e destino correspondem a cada linha de criação/edição. |
| M-24 | Default diferente do literal do requisito mascarado por config de teste | CT-22 | Dado verifica leitura efetiva de fábrica 5000.00; teste não injeta esse valor. |
| M-96 | Usar max(5000, limite configurado) impedindo reduzir a alçada | CT-23 | Com limite 3000.00, 3000.01 exige diretor; o mutante aprovaria sem diretor. |

## Regra R8 — Somente o aprovador da etapa corrente decide

> Origem: RQ-04/05/06/10; A-02/A-03/A-05/A-07 · perfil **completo** · técnica: **Tabela de decisão completa; estado × evento; papel × verbo**.

Tabela completa: nas etapas pendentes, casos positivos CT-25/31 e negativos CT-28 cobrem os seis atores-base em ambos os verbos; fora delas, CT-26/27. Limite não altera identidade; só altera destino. Papéis acumulados ficam R23. Seis cenários excedem teto completo de cinco após ADV-02: CT-74 distingue papel no tenant errado de alvo no tenant errado; o gate de falsificabilidade vence o teto.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-25] Cada aprovação válida produz sua etapa e seu destino
      Dado solicitação em <partida> com <valor>, Guilherme gestor, Dora diretora, aprovadores distintos da solicitante e papel adicional do ator <adicional>
      Quando <ator> aprova diretamente a etapa corrente
      Então o estado persistido é <destino> e foi acrescentada exatamente uma etapa <etapa> aprovada por <ator>, sem justificativa
      E histórico anterior continua igual; diretores existentes recebem cada um <emails> e-mails mail
      
      Exemplos:
        | partida            | valor   | ator      | etapa   | destino            | emails | adicional         | partição       |
        | aguardando_gestor  | 1000.00 | Guilherme | gestor  | aprovada           | 0      | nenhum            | alçada baixa   |
        | aguardando_gestor  | 6000.00 | Guilherme | gestor  | aguardando_diretor | 1      | nenhum            | alçada alta    |
        | aguardando_diretor | 6000.00 | Dora      | diretor | aprovada           | 0      | nenhum            | segunda etapa  |
        | aguardando_gestor  | 1000.00 | Guilherme | gestor  | aprovada           | 0      | admin_organizacao | gestor admin baixa |
        | aguardando_gestor  | 6000.00 | Guilherme | gestor  | aguardando_diretor | 1      | admin_organizacao | gestor admin alta |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-26] Aprovação em estado sem etapa pendente é recusada
      Dado solicitação em <partida>, Guilherme seu gestor e Dora e Davi diretores reais
      Quando <ator> tenta aprová-la diretamente
      Então a solicitação conserva <partida>, todos os campos e todas as etapas anteriores
      E não surge decisão nova ou e-mail aos diretores, gestor ou solicitante
      
      Exemplos:
        | partida  | ator      | partição          |
        | rascunho | Guilherme | gestor sem envio  |
        | rascunho | Dora      | diretora sem envio|
        | aprovada | Guilherme | gestor terminal   |
        | aprovada | Dora      | diretora terminal |
        | cancelada| Guilherme | gestor cancelada  |
        | cancelada| Dora      | diretora cancelada|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-27] Rejeição em estado sem etapa pendente é recusada
      Dado solicitação em <partida>, gestor e diretores reais, e justificativa válida "Sem verba"
      Quando <ator> tenta rejeitá-la diretamente com essa justificativa
      Então a solicitação conserva <partida>, todos os dados e etapas anteriores
      E não há rejeição nova ou e-mail aos participantes
      
      Exemplos:
        | partida  | ator      | partição           |
        | rascunho | Guilherme | gestor sem envio   |
        | rascunho | Dora      | diretora sem envio |
        | aprovada | Guilherme | gestor terminal    |
        | aprovada | Dora      | diretora terminal  |
        | cancelada| Guilherme | gestor cancelada   |
        | cancelada| Dora      | diretora cancelada |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-28] Identidade errada falha separadamente em aprovar e rejeitar
      Dado solicitação em <partida>, dono Sofia, gestor Guilherme, diretora Dora e todos os outros dados válidos
      Quando <ator> executa diretamente <verbo>, usando "Sem verba" se for rejeitar
      Então a decisão é recusada e situação, dados e histórico persistidos continuam iguais
      E nenhum e-mail é enviado aos diretores existentes, ao gestor ou à solicitante
      
      Exemplos:
        | partida            | verbo    | ator      | partição                |
        | aguardando_gestor  | aprovar  | Sofia     | dono não gestor         |
        | aguardando_gestor  | rejeitar | Sofia     | dono não gestor         |
        | aguardando_gestor  | aprovar  | Gustavo   | gestor de outro centro  |
        | aguardando_gestor  | rejeitar | Gustavo   | gestor de outro centro  |
        | aguardando_gestor  | aprovar  | Dora      | diretora antecipada     |
        | aguardando_gestor  | rejeitar | Dora      | diretora antecipada     |
        | aguardando_gestor  | aprovar  | Otávio    | usuário comum           |
        | aguardando_gestor  | rejeitar | Otávio    | usuário comum           |
        | aguardando_gestor  | aprovar  | Alice     | administração           |
        | aguardando_gestor  | rejeitar | Alice     | administração           |
        | aguardando_diretor | aprovar  | Sofia     | dono não diretor        |
        | aguardando_diretor | rejeitar | Sofia     | dono não diretor        |
        | aguardando_diretor | aprovar  | Guilherme | gestor já decidiu       |
        | aguardando_diretor | rejeitar | Guilherme | gestor já decidiu       |
        | aguardando_diretor | aprovar  | Gustavo   | outro gestor            |
        | aguardando_diretor | rejeitar | Gustavo   | outro gestor            |
        | aguardando_diretor | aprovar  | Otávio    | usuário comum           |
        | aguardando_diretor | rejeitar | Otávio    | usuário comum           |
        | aguardando_diretor | aprovar  | Alice     | administração           |
        | aguardando_diretor | rejeitar | Alice     | administração           |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-29] Ações de decisão correspondem à etapa e gravam decisão real
      Dado solicitação em <partida> e <ator> com consulta autorizada na fixture
      Quando <ator> tenta executar <verbo> pelo componente com justificativa válida quando exigida
      Então a ação tem disponibilidade <disponivel> e o estado persistido é <destino>
      E a variação de histórico é <delta>, com ator e etapa corretos; e-mails só vão ao próximo aprovador se houver
      
      Exemplos:
        | partida            | ator      | verbo    | disponivel | destino            | delta | partição         |
        | aguardando_gestor  | Guilherme | aprovar  | sim        | aguardando_diretor | 1     | gestor válido    |
        | aguardando_gestor  | Guilherme | rejeitar | sim        | rascunho           | 1     | gestor válido    |
        | aguardando_gestor  | Dora      | aprovar  | não        | aguardando_gestor  | 0     | diretor precoce  |
        | aguardando_gestor  | Dora      | rejeitar | não        | aguardando_gestor  | 0     | diretor precoce  |
        | aguardando_diretor | Dora      | aprovar  | sim        | aprovada           | 1     | diretor válido   |
        | aguardando_diretor | Dora      | rejeitar | sim        | rascunho           | 1     | diretor válido   |
        | aguardando_diretor | Guilherme | aprovar  | não        | aguardando_diretor | 0     | gestor antigo    |
        | aguardando_diretor | Guilherme | rejeitar | não        | aguardando_diretor | 0     | gestor antigo    |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o aprovador da etapa corrente decide

    Esquema do Cenário: [CT-74] Ser diretor somente em outra organização não autoriza decidir na atual
      Dado compra da Acme aguardando_diretor, Davi membro comum da Acme mas diretor somente na Globex, Dora diretora da Acme e histórico baseline
      Quando Davi tenta diretamente <verbo> na Acme com justificativa válida se for rejeitar
      Então a decisão é recusada, a compra continua aguardando_diretor e todas as tuplas e dados permanecem anteriores
      E Dora, Davi, gestor e solicitante existentes não recebem novos e-mails nem decisão histórica dessa tentativa
      
      Exemplos:
        | verbo    | partição                     |
        | aprovar  | papel em contexto estrangeiro|
        | rejeitar | papel em contexto estrangeiro|
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-25 | Usar gestor OU diretor sem verificar etapa | CT-28, CT-29 | Dora não decide enquanto aguarda gestor; Guilherme não decide enquanto aguarda diretor. |
| M-26 | Proteger aprovar e esquecer identidade em rejeitar | CT-27, CT-28 | Mesmo ator errado recusado nos dois verbos, com histórico inalterado. |
| M-27 | Aceitar decidir em rascunho ou estado terminal | CT-26, CT-27 | Nenhuma etapa acrescentada para ambos os verbos em três estados inválidos. |
| M-28 | Registrar ator autenticado errado ou substituir decisão anterior | CT-25, CT-29 | Nova tupla tem etapa e ator exatos, histórico anterior permanece. |
| M-29 | Concluir direto na aprovação do gestor para valor alto | CT-25 | 6000.00 resulta aguardando_diretor, com apenas etapa gestor aprovada. |
| M-93 | Consultar papel de diretor em qualquer organização na autorização da decisão | CT-74 | Membro legítimo da Acme com diretor só na Globex é recusado em aprovar e rejeitar sobre compra da própria Acme. |

## Regra R9 — Toda rejeição exige justificativa no domínio

> Origem: RQ-07/08; A-07/A-12 · perfil **completo** · técnica: **EP de ausência e tipo; BVA no mínimo de conteúdo existente**.

Não existe teto de justificativa no 00: Q2 mantém BVA superior como lacuna. TypeError pode recusar argumento impossível na API PHP; não se atribui ao domínio uma regra de normalização ainda aberta.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Toda rejeição exige justificativa no domínio

    Esquema do Cenário: [CT-30] Justificativa ausente ou vazia não devolve ao rascunho
      Dado solicitação em <partida>, <ator> elegível, justificativa como única entrada inválida e participantes reais
      Quando <ator> tenta rejeitar diretamente com <justificativa>
      Então a entrada é recusada e situação, dados e histórico anteriores ficam intactos
      E nenhum e-mail é enviado ao gestor, diretores ou solicitante
      
      Exemplos:
        | partida            | ator      | justificativa | partição          |
        | aguardando_gestor  | Guilherme | ausente       | argumento omitido |
        | aguardando_gestor  | Guilherme | null          | nulo              |
        | aguardando_gestor  | Guilherme | ""            | vazio             |
        | aguardando_gestor  | Guilherme | "   "         | somente espaços   |
        | aguardando_gestor  | Guilherme | array         | tipo errado       |
        | aguardando_diretor | Dora      | ausente       | argumento omitido |
        | aguardando_diretor | Dora      | null          | nulo              |
        | aguardando_diretor | Dora      | ""            | vazio             |
        | aguardando_diretor | Dora      | "   "         | somente espaços   |
        | aguardando_diretor | Dora      | array         | tipo errado       |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Toda rejeição exige justificativa no domínio

    Esquema do Cenário: [CT-31] Uma razão presente permite rejeitar na etapa corrente
      Dado solicitação em <partida>, <ator> elegível com papel adicional <adicional> e justificativa <texto>
      Quando <ator> rejeita diretamente com esse texto
      Então a situação persistida é rascunho e há uma nova decisão rejeitada de <ator> na etapa <etapa> contendo <texto>
      E histórico anterior é preservado e nenhum e-mail é enviado aos participantes reais
      
      Exemplos:
        | partida            | ator      | etapa   | texto           | adicional         | partição            |
        | aguardando_gestor  | Guilherme | gestor  | X               | nenhum            | 1 caractere presente|
        | aguardando_gestor  | Guilherme | gestor  | Não há verba 💰 | nenhum            | acento e4 bytes     |
        | aguardando_diretor | Dora      | diretor | X               | nenhum            | 1 caractere presente|
        | aguardando_diretor | Dora      | diretor | Não há verba 💰 | nenhum            | acento e4 bytes     |
        | aguardando_gestor  | Guilherme | gestor  | Rever compra    | admin_organizacao | gestor mais admin   |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Toda rejeição exige justificativa no domínio

    Esquema do Cenário: [CT-32] O modal de rejeição aponta somente o erro da justificativa
      Dado solicitação em <partida> aberta pelo aprovador elegível
      Quando ele submete rejeição pelo componente com justificativa vazia
      Então o formulário indica justificativa obrigatória e conserva <partida> e histórico
      E nenhum e-mail é enviado aos participantes reais
      
      Exemplos:
        | partida            | partição         |
        | aguardando_gestor  | formulário gestor|
        | aguardando_diretor | formulário diretor|
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-30 | Confiar apenas no required do formulário | CT-30, CT-32 | CT-30 chama fora da UI e recusa vazio, sem alteração persistida. |
| M-31 | Aceitar string de espaços como justificativa | CT-30 | Linha somente espaços mantém situação e contagem histórica anteriores. |
| M-32 | Inventar comprimento mínimo ou perder conteúdo Unicode | CT-31 | X e Não há verba 💰 são aceitos, persistidos e atribuídos à etapa correta. |
| M-33 | Validar só a rejeição do gestor | CT-30, CT-31, CT-32 | A etapa diretor exige razão e volta ao rascunho com razão presente. |

## Regra R10 — Rejeição permite corrigir e recomeçar sem apagar decisões anteriores

> Origem: RQ-08/09/13; A-12 · perfil **completo** · técnica: **2-switch e domínio condicionado pela correção**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Rejeição permite corrigir e recomeçar sem apagar decisões anteriores

    Esquema do Cenário: [CT-33] Após rejeição o novo envio recomeça pelo gestor
      Dado solicitação de Sofia em rascunho após rejeição real na <etapa_anterior>, com tuplas históricas e aprovadores reais
      Quando Sofia envia novamente a solicitação
      Então o estado persistido é aguardando_gestor, todas as tuplas anteriores permanecem iguais e nenhuma nova decisão foi criada
      E somente o gestor recebe exatamente um e-mail mail; diretores não recebem e aprovação antiga não conclui o novo ciclo
      
      Exemplos:
        | etapa_anterior | partição               |
        | gestor         | volta do primeiro nível|
        | diretor        | volta do segundo nível |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Rejeição permite corrigir e recomeçar sem apagar decisões anteriores

    Esquema do Cenário: [CT-34] O novo ciclo considera a correção de valor e centro
      Dado solicitação rejeitada realmente pelo diretor, corrigida em rascunho por Sofia para <valor> e centro de Gustavo, enviada novamente e aguardando_gestor
      Quando Gustavo aprova a etapa do novo ciclo
      Então o destino é <destino> e há nova aprovação de gestor por Gustavo sem alterar as tuplas do ciclo anterior
      E Dora e Davi recebem cada um <emails> e-mails mail; a decisão antiga de Guilherme não substitui a de Gustavo
      
      Exemplos:
        | valor   | destino            | emails | partição          |
        | 4999.99 | aprovada           | 0      | corrigido abaixo  |
        | 5000.00 | aprovada           | 0      | corrigido na borda|
        | 5000.01 | aguardando_diretor | 1      | corrigido acima   |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Rejeição permite corrigir e recomeçar sem apagar decisões anteriores

    Cenário: [CT-35] Rejeição do componente mostra o rascunho com a razão e libera correção
      Dado solicitação de Sofia aguardando_diretor, aprovação real de Guilherme já registrada e Dora elegível
      Quando Dora rejeita pelo componente com justificativa "Rever o centro"
      Então o banco contém rascunho e nova rejeição de Dora com "Rever o centro", preservando a aprovação de Guilherme
      E Sofia encontra a razão no detalhe e pode editar o rascunho; nenhum e-mail vai aos participantes existentes
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-34 | Reenvio após rejeição do diretor retorna direto ao diretor | CT-33 | Destino do segundo envio é aguardando_gestor nas duas linhas. |
| M-35 | Limpar etapas anteriores ao reenviar ou corrigir | CT-33, CT-34, CT-35 | IDs e conteúdo das tuplas históricas sobrevivem sem alteração. |
| M-36 | Reaproveitar aprovação antiga ou valor antigo no ciclo seguinte | CT-34 | Gustavo grava nova decisão e os três valores corrigidos seguem a borda atual. |
| M-37 | Deixar rejeitada como estado que impede nova edição | CT-35 | Situação é rascunho e Sofia tem correção disponível. |

## Regra R11 — Somente o solicitante cancela antes da decisão final

> Origem: RQ-11; A-05/A-06/A-11 · perfil **completo** · técnica: **Estado × operação e identidade**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o solicitante cancela antes da decisão final

    Esquema do Cenário: [CT-36] Cancelar nas duas etapas preserva o registro e as decisões já feitas
      Dado solicitação de Sofia em <partida> com <historico>, papel adicional de Sofia <adicional> e participantes reais
      Quando Sofia cancela diretamente
      Então a solicitação existe em cancelada com os mesmos descrição, valor, centro e histórico anterior
      E não surge decisão de aprovador nem e-mail ao gestor, diretores ou Sofia
      
      Exemplos:
        | partida            | historico              | adicional         | partição          |
        | aguardando_gestor  | nenhuma decisão        | nenhum            | antes do gestor   |
        | aguardando_diretor | aprovação de Guilherme | nenhum            | antes do diretor  |
        | aguardando_gestor  | nenhuma decisão        | admin_organizacao | solicitante admin antes gestor |
        | aguardando_diretor | aprovação de Guilherme | admin_organizacao | solicitante admin antes diretor |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o solicitante cancela antes da decisão final

    Esquema do Cenário: [CT-37] Cancelar em rascunho ou estado terminal é recusado
      Dado solicitação de Sofia em <partida>, snapshot histórico e participantes reais
      Quando Sofia tenta cancelar diretamente
      Então a solicitação conserva existência, dados e situação <partida>
      E o histórico permanece igual e não há e-mail a qualquer participante
      
      Exemplos:
        | partida  | partição                  |
        | rascunho | verbo é excluir por A-06  |
        | aprovada | aprovação final           |
        | cancelada| cancelamento terminal     |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o solicitante cancela antes da decisão final

    Esquema do Cenário: [CT-38] A ação cancelar produz estado cancelada na UI
      Dado solicitação de Sofia em <partida> aberta no componente e aprovadores reais
      Quando Sofia confirma cancelar
      Então o mesmo registro existe com situação cancelada e dados anteriores
      E histórico não ganha decisão e não há e-mail aos participantes
      
      Exemplos:
        | partida            | partição          |
        | aguardando_gestor  | antes do gestor   |
        | aguardando_diretor | antes do diretor  |
      E a linha desse registro na listagem já montada mostra cancelada após a resposta da ação, sem remontar o componente ou recarregar a página
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-38 | Permitir cancelar depois da aprovação final | CT-37 | Aprovada permanece aprovada com todas as decisões anteriores. |
| M-39 | Permitir cancelar só antes do gestor | CT-36, CT-38 | Aguardando_diretor também termina cancelada por Sofia. |
| M-40 | Apagar a solicitação ou inventar decisão ao cancelar | CT-36, CT-38 | Registro existe cancelada; histórico tem exatamente as tuplas anteriores. |
| M-97 | Cancelar no banco mas manter badge da pendência anterior no componente montado | CT-38 | Após a ação, a própria linha apresenta cancelada antes de qualquer recarga. |

## Regra R12 — Repetir uma intenção elegível não duplica o efeito da transição

> Origem: RQ-02/03/04/05/06/07/08/10/11/13/14 · perfil **completo** · técnica: **Idempotência no agregado persistido; retry sequencial e leitura obsoleta**.

Não exige resposta específica do segundo chamado: recusa controlada ou resultado idempotente são aceitáveis se o agregado e efeitos são únicos. Criação de solicitação/centro não tem chave de intenção definida: Q9, sem promessa de deduplicação inventada.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Repetir uma intenção elegível não duplica o efeito da transição

    Esquema do Cenário: [CT-39] Uma execução válida seguida de retry tem um único efeito
      Dado solicitação na <partida>, ator elegível, payload válido e histórico baseline, com gestores e diretores reais
      Quando o ator executa a mesma intenção <intencao> duas vezes sequencialmente sobre a mesma solicitação
      Então o agregado persistido termina em <destino>, com <novas_etapas> novas etapas e dados correspondentes à intenção uma só vez
      E o total de novos e-mails é <emails>, distribuído somente aos próximos aprovadores
      
      Exemplos:
        | partida            | intencao                    | destino            | novas_etapas | emails | partição              |
        | rascunho           | enviar                     | aguardando_gestor  | 0            | 1      | retry envio           |
        | aguardando_gestor  | aprovar valor 1000.00       | aprovada           | 1            | 0      | retry gestor baixo    |
        | aguardando_gestor  | aprovar valor 6000.00       | aguardando_diretor | 1            | 2      | retry gestor alto     |
        | aguardando_diretor | aprovar                    | aprovada           | 1            | 0      | retry diretor         |
        | aguardando_gestor  | rejeitar com Sem verba     | rascunho           | 1            | 0      | retry rejeição gestor |
        | aguardando_diretor | rejeitar com Sem verba     | rascunho           | 1            | 0      | retry rejeição diretor|
        | aguardando_gestor  | cancelar                   | cancelada          | 0            | 0      | retry cancelar gestor |
        | aguardando_diretor | cancelar                   | cancelada          | 0            | 0      | retry cancelar diretor|
        | rascunho           | excluir                    | ausente            | 0            | 0      | retry excluir         |
        | rascunho           | editar descricao para Tela | rascunho           | 0            | 0      | retry editar          |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Repetir uma intenção elegível não duplica o efeito da transição

    Esquema do Cenário: [CT-40] Duas cópias elegíveis não tornam a decisão repetível
      Dado solicitação em <partida> carregada em duas instâncias antes de qualquer escrita, ator elegível e aprovadores reais
      Quando o ator aplica <intencao> na primeira instância e repete na segunda instância obsoleta
      Então o registro relido termina em <destino> com <etapas> novas decisões e sem sobrescrever histórico anterior
      E o total de novos e-mails permanece <emails>, sem repetição do destinatário
      
      Exemplos:
        | partida            | intencao                 | destino            | etapas | emails | partição                |
        | rascunho           | enviar                   | aguardando_gestor  | 0      | 1      | envio obsoleto          |
        | aguardando_gestor  | aprovar valor 1000.00     | aprovada           | 1      | 0      | gestor baixo obsoleto   |
        | aguardando_gestor  | aprovar valor 6000.00     | aguardando_diretor | 1      | 2      | gestor alto obsoleto    |
        | aguardando_diretor | aprovar                  | aprovada           | 1      | 0      | diretor obsoleto        |
        | aguardando_gestor  | rejeitar com Sem verba   | rascunho           | 1      | 0      | rejeição gestor obsoleta|
        | aguardando_diretor | rejeitar com Sem verba   | rascunho           | 1      | 0      | rejeição diretor obsoleta|
        | aguardando_gestor  | cancelar                 | cancelada          | 0      | 0      | cancelar obsoleto       |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-41 | Validar somente a instância em memória e repetir a escrita | CT-40 | Uma decisão nova e cardinalidade exata de e-mails após duas cópias. |
| M-42 | Desduplicar só aprovação de diretor e duplicar a de gestor | CT-39, CT-40 | Aprovação de gestor alto produz uma etapa e exatamente dois e-mails, um por diretor. |
| M-43 | Enviar e-mail antes de detectar retry da transição | CT-39, CT-40 | Envio duplicado gera um único e-mail ao gestor existente. |
| M-44 | Rejeitar ou cancelar novamente altera histórico/situação | CT-39, CT-40 | Duas chamadas preservam uma rejeição ou zero decisões de cancelamento. |

## Regra R13 — Uma decisão vence a corrida e a escrita composta é atômica

> Origem: RQ-04/05/06/08/10/11/13/14 · perfil **completo** · técnica: **Concorrência real e rastreio de atomicidade**.

CT-41 é especificação de corrida, não cobertura já medida. Nunca substituir por duas chamadas em memória. Sem vendor/DB configurado, a prova do arnês compartilhado é pendente L3; tentativa real limitada ao inventário pdo_* e configuração :memory:, sem alegar impossibilidade. CT-42 exige falha posterior à escrita; CT-46 cobre falha posterior ao ponto de efeito.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Uma decisão vence a corrida e a escrita composta é atômica

    Esquema do Cenário: [CT-41] Duas escritas realmente simultâneas não vencem a mesma etapa
      Dado solicitação em <partida> no banco de teste compartilhado, com duas conexões/processos e leituras elegíveis sincronizadas por barreira antes das gravações
      Quando as intenções <a> e <b> são liberadas simultaneamente
      Então somente uma intenção vence; o estado e a decisão persistidos correspondem integralmente a essa vencedora
      E o incremento de histórico e os e-mails por destinatário correspondem uma única vez à vencedora, sem efeito da perdedora
      
      Exemplos:
        | partida            | a                         | b                          | partição                |
        | rascunho           | Sofia enviar              | Sofia enviar               | dois envios             |
        | aguardando_gestor  | Guilherme aprovar 6000.00  | Guilherme aprovar 6000.00   | dois cliques do gestor  |
        | aguardando_diretor | Dora aprovar              | Davi aprovar               | dois diretores          |
        | aguardando_gestor  | Guilherme rejeitar        | Guilherme aprovar          | decisões opostas gestor |
        | aguardando_diretor | Dora rejeitar             | Davi aprovar               | decisões opostas diretor|
        | aguardando_gestor  | Sofia cancelar            | Guilherme aprovar          | cancelar versus gestor  |
        | aguardando_diretor | Sofia cancelar            | Dora aprovar               | cancelar versus diretor |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Uma decisão vence a corrida e a escrita composta é atômica

    Esquema do Cenário: [CT-42] Falha depois da primeira escrita não deixa estado sem decisão correspondente
      Dado solicitação em <partida>, ator elegível, histórico baseline e diretores reais, com falha determinística programada após a primeira escrita persistente e antes do commit
      Quando o ator executa <intencao> e a falha interrompe a unidade de decisão
      Então a leitura nova do banco conserva a situação e todas as tuplas históricas do baseline
      E nenhum e-mail comprometido com essa tentativa é entregue aos aprovadores existentes
      
      Exemplos:
        | partida            | intencao                    | partição                   |
        | aguardando_gestor  | aprovar valor 6000.00        | estado e aprovação gestor  |
        | aguardando_diretor | aprovar                     | estado e aprovação diretor |
        | aguardando_gestor  | rejeitar com Sem verba      | estado e rejeição gestor   |
        | aguardando_diretor | rejeitar com Sem verba      | estado e rejeição diretor  |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-45 | Check-then-act sem trava ou escrita condicional | CT-41 | Após barreira real, um só vencedor, nunca duas etapas da mesma pendência. |
| M-46 | Gravar histórico antes da corrida sem rollback da perdedora | CT-41 | Não há tupla adicional da intenção perdedora. |
| M-47 | Atualizar estado e histórico em unidades independentes | CT-42 | Falha após primeira escrita restaura ambas as partes ao baseline. |
| M-48 | Aceitar cancelamento e aprovação final da mesma pendência | CT-41 | Estado final e histórico refletem uma vencedora, sem combinação contraditória. |

## Regra R14 — E-mail alcança o próximo aprovador uma única vez

> Origem: RQ-14; A-02/A-03/A-04/A-10/A-11 · perfil **completo** · técnica: **Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade**.

Cardinalidade zero de gestor é CT-20; zero diretores é Q4, sem inventar destino. Atomicidade CT-46 exige observador de transporte/fila que não engula o ponto de efeito: revalidar lançador/transações na materialização. Registro de fake antes da transação não é prova de e-mail externo. Falta de execução é L3, sem MSI certificado.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail alcança o próximo aprovador uma única vez

    Cenário: [CT-43] Envio entrega somente e-mail ao gestor escolhido
      Dado rascunho de Sofia no centro de Guilherme, outro gestor Gustavo e diretores Dora e Davi existentes
      Quando Sofia envia a solicitação
      Então existe exatamente uma notificação dessa solicitação e etapa gestor para Guilherme pelo canal mail
      E Sofia, Gustavo, Dora e Davi não recebem notificação desta tentativa
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail alcança o próximo aprovador uma única vez

    Esquema do Cenário: [CT-44] Encaminhamento alto avisa todos os diretores atuais
      Dado solicitação aguardando_gestor de "6000.00", <diretores> diretores na organização e pessoas fora desse papel existentes
      Quando Guilherme aprova
      Então a solicitação fica aguardando_diretor e cada diretor dessa organização recebe exatamente um e-mail mail dessa solicitação e etapa diretor
      E o total é <diretores>, sem e-mail a Sofia, Guilherme, usuários comuns ou diretores de outra organização
      
      Exemplos:
        | diretores | partição |
        | 1         | um       |
        | 3         | vários   |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail alcança o próximo aprovador uma única vez

    Esquema do Cenário: [CT-45] Não há avisos quando não existe próxima etapa pedida
      Dado solicitação em <partida>, ator elegível e Sofia, Guilherme, Dora e Davi realmente notificáveis
      Quando o ator executa <intencao>
      Então o estado e histórico correspondem à intenção válida e nenhum desses usuários recebe e-mail
      E nenhuma notificação por outro canal é criada para substituí-lo
      
      Exemplos:
        | partida            | intencao                    | partição              |
        | aguardando_gestor  | aprovar valor 5000.00        | final pelo gestor     |
        | aguardando_diretor | aprovar                     | final pelo diretor    |
        | aguardando_gestor  | rejeitar com Sem verba      | rejeição gestor       |
        | aguardando_diretor | rejeitar com Sem verba      | rejeição diretor      |
        | aguardando_gestor  | cancelar por Sofia          | cancelamento gestor   |
        | aguardando_diretor | cancelar por Sofia          | cancelamento diretor  |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail alcança o próximo aprovador uma única vez

    Esquema do Cenário: [CT-46] Falha no commit após o ponto de notificação não produz aviso fantasma
      Dado solicitação em <partida> com <destinatarios> reais e um ponto controlado que falha no commit após o caminho alcançar o despacho/registro do efeito
      Quando a intenção <intencao> é executada e o commit falha nesse ponto
      Então situação e histórico persistidos continuam no baseline e não existe entrega ou job durável dessa tentativa aos destinatários
      E a observação comprova que a falha ocorreu depois do ponto de efeito, não numa pré-validação
      
      Exemplos:
        | partida           | intencao                    | destinatarios | partição             |
        | rascunho          | Sofia enviar                | Guilherme     | aviso de gestor      |
        | aguardando_gestor | Guilherme aprovar 6000.00    | Dora e Davi   | aviso dos diretores  |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail alcança o próximo aprovador uma única vez

    Cenário: [CT-47] Diretor de outra organização não recebe e-mail desta
      Dado compra de Sofia na Acme aguardando_gestor de "6000.00", Dora diretora na Acme e Davi diretor somente na Globex, com papéis e contexto reais
      Quando Guilherme aprova na Acme
      Então o banco da Acme fica aguardando_diretor e Dora recebe exatamente um e-mail mail com a compra da Acme
      E Davi não recebe aviso, nenhum dado da Globex é alterado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-49 | Enviar pelo canal database no lugar de mail | CT-43, CT-44 | Canais efetivos incluem mail e notification corresponde à solicitação e etapa. |
| M-50 | Notificar só o primeiro diretor ou repetir destinatário | CT-44 | N=3 tem um e-mail por ID e exatamente três no total. |
| M-51 | Avisar participantes em final/rejeição/cancelamento sem pedido | CT-45 | Zero e-mails apesar de todos os destinatários reais existirem. |
| M-52 | Despachar antes do commit sem impedir entrega em rollback | CT-46 | Falha posterior ao efeito não deixa job durável ou e-mail fantasma. |
| M-53 | Resolver papel diretor no contexto global ou de outro tenant | CT-47 | Somente Dora da Acme recebe a compra; papel da Globex não vale aqui. |
| M-54 | Avisar solicitante ou gestor de outro centro no envio | CT-43 | Exatamente Guilherme recebe um mail, com ausências nominais. |

## Regra R15 — Listagem e detalhe mostram a situação corrente

> Origem: RQ-12; A-12 · perfil **padrão** · técnica: **EP exaustiva de estado; paginação**.

Inserção entre páginas e política de ordenação/desempate não são especificadas pelo 00: L2/Q3, sem inventar garantia de snapshot estável entre requests. CT-50 mede páginas em fixture estável e não é citado para fechar esse recorte.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Listagem e detalhe mostram a situação corrente

    Esquema do Cenário: [CT-48] Cada estado aparece associado à solicitação correta na listagem
      Dado solicitação identificável de Sofia em <partida> por transições reais e outro registro em estado diferente
      Quando Sofia consulta a listagem pelo componente
      Então a linha da solicitação mostra semanticamente <partida> e a outra linha mostra seu próprio estado
      E a leitura não altera dados, histórico ou e-mails aos participantes reais
      
      Exemplos:
        | partida            | partição          |
        | rascunho           | estado inicial    |
        | aguardando_gestor  | primeiro nível    |
        | aguardando_diretor | segundo nível     |
        | aprovada           | final aprovada    |
        | cancelada          | final cancelada   |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Listagem e detalhe mostram a situação corrente

    Esquema do Cenário: [CT-49] Cada estado aparece no detalhe do registro correspondente
      Dado solicitação de Sofia em <partida> por transições reais e outra solicitação em estado diferente
      Quando Sofia consulta o detalhe da primeira pelo componente
      Então o detalhe vincula a situação <partida> ao identificador da primeira solicitação
      E não apresenta dados ou histórico da segunda nem altera o banco
      
      Exemplos:
        | partida            | partição          |
        | rascunho           | estado inicial    |
        | aguardando_gestor  | primeiro nível    |
        | aguardando_diretor | segundo nível     |
        | aprovada           | final aprovada    |
        | cancelada          | final cancelada   |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Listagem e detalhe mostram a situação corrente

    Esquema do Cenário: [CT-50] A situação é correta também nas bordas da paginação
      Dado uma listagem autorizada com <quantidade> solicitações de situações variadas, tamanho real de página L e fixture estabilizada por identificador
      Quando Sofia consulta a página <pagina> pelo componente
      Então os IDs previstos para essa página e o status de cada ID correspondem aos registros persistidos, sem troca ou duplicação de linhas
      E todos os IDs da fixture estável são alcançáveis nas páginas cabíveis
      
      Exemplos:
        | quantidade | pagina  | partição              |
        | 0          | 1       | vazio                 |
        | 1          | 1       | uma linha             |
        | L          | 1       | limite                |
        | L+1        | 2       | além do limite        |
        | L+1        | 1 e 2   | ID/status nas páginas |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-55 | Reusar rótulo aprovado quando estado é aguardando_diretor | CT-48, CT-49 | Segundo nível continua pendente em ambas as superfícies. |
| M-56 | Usar status da primeira linha ou do componente no detalhe de outro registro | CT-48, CT-49 | Estado é correlacionado por ID, com registro de contraste. |
| M-57 | Pular a primeira linha da página 2 ou trocar associação status/ID | CT-50 | L+1º registro aparece com seu próprio status; união estável não perde IDs. |

## Regra R16 — O histórico exibe as pessoas e preserva os ciclos

> Origem: RQ-13/09; A-12 · perfil **padrão** · técnica: **Rastreio histórico e EP de 0/1/N decisões**.

Acesso do ex-gestor ao registro e destino de link de e-mail permanecem Q3; CT-52 prova preservação/exibição para Sofia autorizada, sem inventar público de consulta. Fuso/formato exatos são Q10. Os instantes são controlados no relógio de teste antes de cada transição real. Na fixture temporal, app, DB e usuário usam UTC; a asserção semântica dos valores não impõe formato/fuso geral, ainda Q10. Não usar o formatter de produção para calcular o esperado.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O histórico exibe as pessoas e preserva os ciclos

    Esquema do Cenário: [CT-51] O detalhe mostra quem decidiu cada etapa e não o cadastro atual
      Dado solicitação de Sofia criada em 2026-10-18T09:00:00Z com <caminho> real, aprovação de Guilherme em 2026-10-20T12:00:00Z e decisão de Dora em 2026-10-22T15:00:00Z quando presentes
      Quando Sofia consulta o histórico no detalhe
      Então aparecem exatamente as decisões de <esperado>, com etapa, pessoa, razão quando rejeitada e instante persistido/exibido correspondente à respectiva decisão, não à criação
      E Guilherme tem instante 2026-10-20T12:00:00Z e Dora 2026-10-22T15:00:00Z quando essas decisões existem; pessoa só notificada nunca figura como quem aprovou
      
      Exemplos:
        | caminho                                    | esperado                     | partição         |
        | rascunho sem decisões                      | nenhuma decisão              | zero             |
        | gestor aprovou 1000.00                     | Guilherme                    | uma aprovação    |
        | gestor e Dora aprovaram 6000.00            | Guilherme e Dora              | duas aprovações  |
        | gestor aprovou e Dora rejeitou 6000.00      | Guilherme e Dora com razão    | decisão rejeitada|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O histórico exibe as pessoas e preserva os ciclos

    Cenário: [CT-52] Participantes de ciclos diferentes continuam identificáveis
      Dado compra de Sofia criada em 2026-10-18T09:00:00Z, com aprovação de Guilherme em 20/10 às 12:00Z, rejeição de Dora em 22/10 às 15:00Z, correção/reenvio e aprovações de Gustavo em 24/10 às 10:00Z e Davi em 26/10 às 16:00Z, todas reais em 2026
      Quando Sofia consulta seu detalhe
      Então o histórico contém as quatro tuplas distintas: Guilherme/gestor/aprovada/2026-10-20T12:00:00Z, Dora/diretor/rejeitada/2026-10-22T15:00:00Z, Gustavo/gestor/aprovada/2026-10-24T10:00:00Z e Davi/diretor/aprovada/2026-10-26T16:00:00Z
      E cada instante persistido e exibido representa sua decisão; razão de Dora e nomes antigos continuam associados às tuplas originais, sem usar criação ou instante da consulta
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-58 | Exibir nome do gestor atual em toda aprovação histórica | CT-51, CT-52 | Guilherme permanece na etapa antiga e Gustavo apenas na nova. |
| M-59 | Mostrar só a decisão mais recente de cada etapa | CT-52 | Quatro tuplas de dois ciclos aparecem, incluindo rejeição de Dora. |
| M-60 | Confundir pessoa notificada com pessoa que decidiu | CT-51 | Só ator que realmente decidiu aparece como aprovador. |
| M-98 | Gravar ou exibir a data de criação da compra como instante de todas as decisões | CT-51, CT-52 | Instantes distintos de 20,22,24 e26/10/2026 coincidem com cada decisão real e diferem da criação em18/10. |

## Regra R17 — Administrar centro de custo grava o gestor que define o fluxo

> Origem: RQ-01/04; A-01/A-02/A-08 · perfil **completo** · técnica: **CRUD, par visita/gravação, criação ≠ edição**.

R17 herda completo por mudar autoridade de aprovação. Unicidade/nome obrigatório/teto, exclusão de centro utilizado e referência temporal do gestor não são arbitrados: Q6/Q7 e L2. Gate de escrita: CT-02/06/54/55, pareados às quatro visitas CT-56. A representação física/lógica da exclusão do centro não é oráculo.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Administrar centro de custo grava o gestor que define o fluxo

    Esquema do Cenário: [CT-53] Administração autorizada cria, edita e exclui centro não utilizado
      Dado Alice administradora da Acme, centro <partida>, outro centro de contraste Financeiro da Acme e usuários Guilherme e Gustavo membros da Acme
      Quando Alice executa fora do componente <operacao>
      Então o banco contém exatamente <esperado> e nenhuma solicitação ou decisão alheia é modificada
      E Financeiro preserva existência, nome e gestor anteriores, e a operação não envia e-mail aos gestores ou diretores reais
      
      Exemplos:
        | partida                 | operacao                          | esperado                          | partição    |
        | inexistente             | criar TI com Guilherme            | centro TI da Acme com Guilherme   | criação     |
        | TI com Guilherme        | editar gestor para Gustavo        | mesmo centro TI com Gustavo       | edição      |
        | TI com Guilherme        | salvar TI e Guilherme sem mudança | mesmo centro TI com Guilherme     | sem mudança |
        | TI sem solicitação      | excluir                           | centro indisponível para nova compra             | exclusão    |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Administrar centro de custo grava o gestor que define o fluxo

    Cenário: [CT-54] Criar centro pelo componente persiste o vínculo de gestor
      Dado Alice autorizada no create de centro, Guilherme membro da Acme e nenhum centro chamado "Pesquisa"
      Quando Alice grava "Pesquisa" com gestor Guilherme pelo componente
      Então existe centro "Pesquisa" da Acme com gestor exatamente Guilherme
      E ele pode ser escolhido numa solicitação da Acme, sem e-mail gerado pelo cadastro
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Administrar centro de custo grava o gestor que define o fluxo

    Cenário: [CT-55] Editar centro pelo componente persiste um gestor diferente
      Dado Alice autorizada no edit de centro "Pesquisa" da Acme com gestor Guilherme
      Quando Alice salva pelo componente o nome "Pesquisa revisada" e gestor Gustavo da Acme
      Então o mesmo centro contém "Pesquisa revisada" e Gustavo, preservando organização Acme
      E não se cria outro centro nem se envia e-mail aos usuários existentes
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Administrar centro de custo grava o gestor que define o fluxo

    Esquema do Cenário: [CT-56] As quatro páginas de escrita apresentam os campos da operação
      Dado <ator> autorizado e registro em rascunho quando a página é de edição de solicitação
      Quando <ator> visita a rota <pagina>
      Então a página contém os campos <campos> e identifica a operação/registro correto, além de responder com sucesso
      E a visita não grava centro ou solicitação
      
      Exemplos:
        | ator  | pagina                        | campos                         | partição             |
        | Sofia | solicitação create            | descrição, valor, centro       | visita criação compra|
        | Sofia | solicitação edit do rascunho   | descrição, valor, centro       | visita edição compra |
        | Alice | centro create                 | nome, gestor                   | visita criação centro|
        | Alice | centro edit                   | nome, gestor                   | visita edição centro |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | Salvar nome do centro mas não gestor | CT-53, CT-54, CT-55 | Gestor ID exato persiste na criação e edição. |
| M-62 | Criar outro centro no save do formulário | CT-55 | A mesma PK tem nome/gestor novos e contagem não cresce. |
| M-63 | Registrar rota create/edit mas renderizar schema errado | CT-56 | Cada rota apresenta seus campos e registro da operação, além de status. |
| M-64 | Excluir centro errado ou bloquear toda exclusão | CT-53 | Centro não utilizado fica indisponível para nova compra; demais centros permanecem. |

## Regra R18 — Usuário comum não administra quem aprova

> Origem: RQ-01/04; A-03/A-08 · perfil **completo** · técnica: **Papel × ação e autorização fora da UI**.

Contexto de diretor deve ser semeado para app conforme A-03. CT-59 Dora usa uma solicitação própria criada legitimamente; não assume que todo diretor vê todas as compras. A autoridade do seeder é conferida por ações, sem contagem de permissions copiada do PRD.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Usuário comum não administra quem aprova

    Esquema do Cenário: [CT-57] Panel user não cria, altera ou exclui centro nem se nomeia gestor
      Dado Otávio panel_user da Acme, centro da Acme com gestor Guilherme, permissions reais semeadas e acesso de negócio existente
      Quando Otávio tenta fora do componente <operacao> no ponto de entrada autorizado da aplicação
      Então a escrita é recusada, não há novo centro e o centro existente mantém nome, gestor e existência
      E Otávio continua autorizado a criar sua solicitação, sem etapa ou e-mail indevido
      
      Exemplos:
        | operacao                            | partição        |
        | criar centro e indicar a si mesmo    | criar           |
        | mudar gestor para Otávio             | auto nomeação   |
        | excluir centro                      | excluir         |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Usuário comum não administra quem aprova

    Esquema do Cenário: [CT-58] O componente aplica a recusa administrativa em cada ação
      Dado Otávio panel_user da Acme e centro com gestor Guilherme, sem permission de administração
      Quando Otávio tenta a ação <acao> pelo componente de centro
      Então a ação não é oferecida e não há criação, edição ou exclusão persistida
      E o gestor do centro continua Guilherme e não há efeitos em compras ou e-mails
      
      Exemplos:
        | acao    | partição  |
        | criar   | create    |
        | editar  | save      |
        | excluir | delete    |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Usuário comum não administra quem aprova

    Esquema do Cenário: [CT-59] Após recusa o usuário conserva uma página de negócio alcançável
      Dado <ator> membro da Acme com seu papel real e uma solicitação própria identificável em rascunho
      Quando <ator> acessa a listagem autorizada de solicitações depois de recusa de <origem>
      Então a página é alcançada sem ciclo de redirect e exibe a solicitação identificável com situação rascunho
      E permite a operação de negócio autorizada sem oferecer administração do centro
      
      Exemplos:
        | ator   | origem                           | partição          |
        | Otávio | rota de administração de centro   | saída de 403      |
        | Sofia  | registro de outra organização     | saída de 404      |
        | Dora   | decisão antes da etapa do diretor | diretora no painel|
        | Sofia  | UUID inexistente de compra         | saída de inexistente|
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-65 | Esquecer centros na subtração de permissions do panel_user | CT-57, CT-58 | Operações administrativas reais falham; não basta can() ou lista de roles. |
| M-66 | Esconder menu mas aceitar escrita pelo componente/fora dele | CT-57, CT-58 | Gestor não muda para Otávio em nenhuma entrada. |
| M-67 | Retirar todas as permissions do panel_user ou diretor para evitar escalada | CT-59 | Listagem de negócio e solicitação própria estão acessíveis aos papéis legítimos. |
| M-68 | Redirecionar recusas para rota que devolve à mesma recusa | CT-59 | Destino autorizado mostra o registro em vez de loop. |

## Regra R19 — Nenhuma organização lê ou altera compras e centros de outra

> Origem: RQ-01/04/05/12/13/14; A-01/A-03 · perfil **completo** · técnica: **IDOR por entidade e fronteira de associação na gravação**.

CT-63 é tentativa concreta pelos pontos conhecidos da UI; não prova que inexiste uma rota direta para EtapaAprovacao. Como o 02 está ausente, acesso direto da filha é lacuna L1 e não dispensa de controle. Não ler implementação para fechar essa negativa.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Nenhuma organização lê ou altera compras e centros de outra

    Esquema do Cenário: [CT-60] Contexto errado não dá autoridade mesmo a pessoa com vínculo legítimo no outro
      Dado Acme e Globex, ator legitimamente elegível no registro da Globex e também membro da Acme, mas operando agora na Acme
      Quando o ator tenta diretamente <operacao> sobre <alvo> da Globex
      Então a operação é recusada, os dados da Globex permanecem no snapshot e nenhum dado aparece como pertencente à Acme
      E histórico e e-mails aos aprovadores reais das duas organizações não recebem efeitos dessa tentativa
      
      Exemplos:
        | alvo                         | operacao                     | partição                |
        | solicitação rascunho          | editar valor                 | compra edit outro tenant|
        | solicitação rascunho          | excluir                      | compra delete           |
        | solicitação rascunho          | enviar                       | compra envio            |
        | solicitação aguardando_gestor | aprovar como gestor          | gestor no contexto errado|
        | solicitação aguardando_gestor | rejeitar como gestor         | rejeição contexto errado|
        | solicitação aguardando_diretor| aprovar como diretor         | papel em outro contexto |
        | solicitação aguardando_diretor| rejeitar como diretor        | rejeição diretor contexto|
        | solicitação aguardando_gestor | cancelar como solicitante    | cancelar contexto errado|
        | centro                       | editar como administrador    | centro edit             |
        | centro sem solicitações      | excluir como administrador   | centro delete           |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Nenhuma organização lê ou altera compras e centros de outra

    Esquema do Cenário: [CT-61] Route binding e componente recusam IDs da outra organização
      Dado Sofia membro só da Acme, solicitação própria em rascunho e <alvo> real na Globex
      Quando Sofia usa o identificador real da Globex na entrada <entrada> da Acme
      Então nenhum nome, valor, situação ou histórico da Globex é revelado e nenhuma escrita é aplicada
      E a solicitação própria e o histórico da Globex permanecem intactos; saída autorizada é coberta por CT-59
      
      Exemplos:
        | alvo        | entrada                          | partição               |
        | solicitação | URL view                         | detalhe por UUID       |
        | solicitação | URL edit                         | editar por UUID        |
        | solicitação | ação de tabela enviar            | ID cliente             |
        | centro      | URL edit como Alice da Acme       | centro por UUID        |
        | centro      | ação excluir como Alice da Acme   | centro ID cliente      |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Nenhuma organização lê ou altera compras e centros de outra

    Esquema do Cenário: [CT-62] A gravação rejeita relação com entidade de outra organização
      Dado ator autorizado na Acme, rascunho próprio válido e somente <relacao> apontando para objeto existente da Globex
      Quando o ator grava por fora do componente na operação <operacao>
      Então a associação estrangeira é recusada e os registros das duas organizações conservam os vínculos anteriores
      E não há solicitação parcial, etapa ou e-mail aos gestores e diretores reais
      
      Exemplos:
        | operacao                | relacao                        | partição                  |
        | criar solicitação       | centro_custo_id da Globex       | compra criação            |
        | editar rascunho         | centro_custo_id da Globex       | compra edição             |
        | criar centro como Alice | gestor_id só membro da Globex  | centro criação            |
        | editar centro como Alice| gestor_id só membro da Globex  | centro edição             |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Nenhuma organização lê ou altera compras e centros de outra

    Esquema do Cenário: [CT-63] A entrada cliente não alcança histórico estrangeiro pela solicitação atual
      Dado solicitação da Acme aberta por ator autorizado e histórico real da Globex com decisão de Dora identificável
      Quando o ator injeta <payload> na entrada de escrita <entrada> do componente
      Então nenhuma tupla da Globex é lida, alterada, apagada ou reatribuída à solicitação da Acme
      E ambas as solicitações conservam dados e histórico; e-mails não são enviados por essa tentativa forjada
      
      Exemplos:
        | entrada           | payload                              | partição                 |
        | salvar rascunho   | etapas com ID de etapa da Globex      | filho ID numérico        |
        | decidir etapa     | solicitacao_compra_id da Globex       | pai forjado              |
        | exibir detalhe    | identificador histórico da Globex     | leitura filha forjada    |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Nenhuma organização lê ou altera compras e centros de outra

    Esquema do Cenário: [CT-73] Com tenant presente a listagem não inclui registros de outra organização
      Dado <ator> autorizado nas duas organizações, operando na Acme não nula, com <entidade> identificável na Acme e na Globex, rascunho quando for compra
      Quando <ator> consulta a listagem <entrada> da Acme pelo componente em todas as suas páginas
      Então aparecem os IDs permitidos da Acme e nenhum ID, nome, valor, situação ou histórico identificável da Globex
      E nenhum dado, histórico ou e-mail das duas organizações é alterado
      
      Exemplos:
        | ator  | entidade             | entrada                 | partição              |
        | Sofia | solicitação própria  | solicitações de compra  | compra com tenant     |
        | Alice | centro de custo      | centros de custo        | centro com tenant     |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-69 | Remover filtro de tenant da gravação aceitando model pré-carregado | CT-60 | Mesmo ator legítimo na Globex é recusado quando opera na Acme. |
| M-70 | Escopar listagem mas não route binding ou ação por ID | CT-61 | UUID real da Globex não revela campos nem sofre alteração. |
| M-71 | Validar exists global em centro/gestor | CT-62 | Objeto existe, mas vínculo fora da organização é recusado na criação e edição. |
| M-72 | Confiar no pai para filho aceitando ID de etapa do cliente | CT-63 | Tupla identificável da Globex nunca muda nem aparece no detalhe da Acme. |
| M-73 | Permitir consulta direta de etapa por ID sem conferir organização | ⚠️ **sem matador** — L1 | — (lacuna declarada L1: 02 ausente; entrada direta da entidade filha não inventariada). |
| M-92 | Proteger detalhe e escrita mas deixar listagem global com tenant presente | CT-73 | Em todas as páginas da Acme, nenhum identificador/dado conhecido da Globex aparece, apesar de o mesmo ator ter vínculo nas duas. |

## Regra R20 — O cliente não escolhe identidade, organização ou decisões históricas

> Origem: RQ-01/04/05/10/13; A-01/A-02/A-03 · perfil **completo** · técnica: **Mass assignment por tabela e fronteira de gravação**.

O invariante aceita duas políticas seguras: ignorar a entrada protegida e processar os dados legítimos, ou recusar integralmente sem escrita parcial. Nenhum CT reprova a recusa integral por si só. A mutação direta autônoma de EtapaAprovacao permanece lacuna L1; não foi inventada uma API.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O cliente não escolhe identidade, organização ou decisões históricas

    Esquema do Cenário: [CT-64] Payload externo não troca campos de autoridade
      Dado ator autorizado na Acme, operação legítima <operacao> e um único campo protegido <campo> forjado
      Quando o ator grava fora do componente com <campo> igual a <forjado>
      Então a operação recusa integralmente mantendo o snapshot, ou aceita os dados legítimos com o campo protegido igual a <esperado>
      E nenhuma identidade, organização, decisão ou e-mail é alterado pelo campo forjado; recusa não deixa escrita parcial
      
      Exemplos:
        | operacao                     | campo          | forjado               | esperado             | partição          |
        | criar solicitação como Sofia | solicitante_id | Otávio                | Sofia                | compra dono       |
        | criar solicitação como Sofia | tenant_id      | Globex                | Acme                 | compra tenant     |
        | criar solicitação como Sofia | situacao       | aprovada              | rascunho             | compra estado     |
        | editar rascunho de Sofia      | solicitante_id | Otávio                | Sofia                | editar dono       |
        | editar rascunho de Sofia      | situacao       | aprovada              | rascunho             | editar estado     |
        | criar centro como Alice      | tenant_id      | Globex                | Acme                 | centro tenant     |
        | editar centro como Alice     | tenant_id      | Globex                | Acme                 | centro editar     |
        | editar rascunho de Sofia      | tenant_id      | Globex                | Acme                 | compra tenant na edição |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O cliente não escolhe identidade, organização ou decisões históricas

    Esquema do Cenário: [CT-65] Payload do componente não fabrica aprovação nem altera autoria da etapa
      Dado solicitação da Acme em <partida>, ator elegível e histórico baseline com nomes distintos
      Quando o ator executa a operação legítima <operacao> com o payload adicional <forjado> no componente
      Então há recusa integral sem escrita parcial, ou o resultado legítimo persiste com autoridade derivada do ator e transição reais
      E campos protegidos e decisões anteriores permanecem íntegros; se a operação foi aceita, só o próximo aprovador legítimo recebe mail
      
      Exemplos:
        | partida           | operacao                     | forjado                               | partição             |
        | inexistente       | Sofia criar rascunho         | solicitante_id Otávio                  | compra dono UI       |
        | inexistente       | Sofia criar rascunho         | situacao aprovada                     | compra estado UI     |
        | inexistente       | Alice criar centro Acme      | tenant_id Globex                      | centro tenant UI     |
        | aguardando_gestor | Guilherme aprovar 6000.00    | decidido_por_id Dora                  | etapa ator           |
        | aguardando_gestor | Guilherme aprovar 6000.00    | etapa diretor                         | etapa papel          |
        | aguardando_gestor | Guilherme aprovar 6000.00    | decisao rejeitada                     | etapa decisão        |
        | rascunho          | Sofia salvar descrição nova  | etapas com aprovação inventada        | etapa adicional      |
        | rascunho          | Sofia salvar descrição nova  | tenant_id Globex                      | compra tenant na edição UI |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-74 | Aceitar solicitante_id ou tenant_id do cliente por fillable | CT-64, CT-65 | Criação/edição conserva Sofia e Acme mesmo com campo forjado. |
| M-75 | Aceitar status aprovada durante create/save | CT-64, CT-65 | A solicitação criada/salva continua rascunho, sem decisão fabricada. |
| M-76 | Preencher etapa histórica usando array do cliente | CT-65 | Aprovação real tem Guilherme/gestor/aprovada; nenhuma decisão injetada. |
| M-77 | Persistir parte dos dados e só depois recusar o campo protegido sem rollback | CT-64, CT-65 | Na recusa integral todos os dados e contagens ficam no snapshot; não se admite escrita parcial seguida de recusa. |

## Regra R21 — Entradas públicas do componente preservam fronteiras com valor ou tipo inválido

> Origem: RQ-01/04/12/13; A-01/A-08 · perfil **completo** · técnica: **Domínio inválido e tipo errado por entrada conhecida; discriminante nulo**.

L1: a lista é parcial e nasce das entradas explicitadas na UI e dos arrays comuns do framework, não de um 02 inventado. O contrato exato de propriedades públicas/Locked, métodos públicos, montagens de ações e demais consumos de parse/índice não foi conferido no vendor. Um 500 sem vazamento pode passar pelo invariante CT-66: robustez de resposta é lacuna declarada, não mutante morto por esse CT. Mutantes acima só contam quando produzem o vazamento/escrita descritos; não se atribui controle de tipo completo a essa evidência.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Entradas públicas do componente preservam fronteiras com valor ou tipo inválido

    Esquema do Cenário: [CT-66] IDs e estado do framework forjados não atravessam a fronteira
      Dado usuário autorizado na Acme, rascunho próprio válido e registro de contraste existente na Globex
      Quando o cliente envia <entrada> com <valor> ao componente
      Então nenhum dado da Globex é exposto ou escrito e a solicitação própria conserva seus dados e histórico
      E não surge decisão, centro, solicitação ou e-mail aos aprovadores das duas organizações
      
      Exemplos:
        | entrada                         | valor                    | partição                       |
        | ID de registro em ação enviar    | UUID inexistente         | ID fora de domínio             |
        | ID de registro em ação enviar    | array                    | tipo ID errado                 |
        | campo centro_custo_id no create  | ID inexistente           | relação fora de domínio        |
        | campo centro_custo_id no create  | array                    | relação tipo errado            |
        | tableFilters.situacao            | estado_inexistente       | enum fora de domínio           |
        | tableFilters.situacao            | array aninhado           | enum tipo errado               |
        | tableSearch                     | array                    | busca tipo errado              |
        | tableSortColumn                 | coluna_que_nao_existe    | coluna fora de domínio         |
        | tableSortColumn                 | array                    | coluna tipo errado             |
        | payload da ação rejeitar         | justificativa array      | formulário tipo errado         |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Entradas públicas do componente preservam fronteiras com valor ou tipo inválido

    Cenário: [CT-67] Perder o tenant no painel não abre a instalação
      Dado Sofia autorizada na Acme e dados reais de Acme e Globex, com tenant corrente retirado antes da consulta do componente do painel
      Quando Sofia consulta a listagem ou detalhe de compra nessa fronteira sem tenant
      Então nenhum registro ou histórico das duas organizações é exposto pela UI nem sofre alteração
      E nenhum e-mail é disparado; resposta e destino exatos continuam bloqueados por Q8
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-78 | Usar coluna/operador vindo do cliente sem limitar o escopo | CT-66 | Valores forjados não revelam registro estrangeiro nem alteram a compra. |
| M-79 | Aceitar estrutura array como ID ou enum e usá-la na query sem guarda | CT-66 | Tipos errados não produzem leitura/escrita estrangeira ou efeito. |
| M-80 | Tratar tenant ausente no painel como autorização global | CT-67 | UI com tenant nulo não retorna nenhum dado das duas organizações. |

## Regra R22 — Registro removido e identificador inexistente não recebem escrita

> Origem: RQ-02/03/04; A-05 · perfil **completo** · técnica: **Estado removido × operação; CRUD inexistente e saída de erro**.

A única partida legalmente removível é rascunho; ela é usada para não mascarar a remoção com rejeição prévia de estado pendente. Mecanismo @premissa D1. Se a materialização optar por soft delete, rederivar preservando o observável de indisponibilidade, sem apagar a prova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Registro removido e identificador inexistente não recebem escrita

    Esquema do Cenário: [CT-68] Cópia de rascunho excluído não revive ou encaminha compra
      Dado rascunho de Sofia carregado em uma cópia, excluído por Sofia no domínio e destinatários reais Guilherme, Dora e Davi
      Quando Sofia usa a cópia obsoleta para <operacao>
      Então o registro continua ausente, sem nova solicitação substituta ou decisão histórica
      E nenhum e-mail é enviado a Guilherme, Dora ou Davi
      
      Exemplos:
        | operacao                       | partição             |
        | salvar valor 5000.01            | edição após remoção  |
        | enviar                         | envio após remoção   |
        | excluir novamente              | exclusão após remoção|
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Registro removido e identificador inexistente não recebem escrita

    Esquema do Cenário: [CT-69] ID inexistente falha sem prender a navegação autorizada
      Dado Sofia autorizada com rascunho próprio identificável e nenhum registro no UUID solicitado
      Quando Sofia tenta <entrada> com esse UUID
      Então a tentativa é recusada e nenhum registro ou histórico é criado, alterado ou excluído
      E nenhum e-mail é produzido; o destino autorizado após a recusa é exercitado pelo cenário irmão CT-59
      
      Exemplos:
        | entrada           | partição          |
        | detalhe           | leitura ausente   |
        | edição            | edição ausente    |
        | ação excluir      | exclusão ausente  |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-81 | Save da cópia apagada vira insert silencioso | CT-68 | Contagem da compra continua zero depois de editar. |
| M-82 | Enviar cópia apagada notifica mesmo com zero linhas alteradas | CT-68 | Registro ausente e zero e-mails ao gestor existente. |
| M-83 | Erro de ID ausente cria registro ou envia para navegação em loop | CT-69 | Nenhum registro substituto e listagem própria alcançável. |

## Regra R23 — Papéis acumulados não eliminam etapas

> Origem: RQ-04/05/06; A-03/A-09 · perfil **completo** · técnica: **Tabela de decisão e sondas par a par**.

Os três pares têm ambos os verbos: S×G CT-70, S×D e G×D CT-75. CT-71/72 também provam que a acumulação não pula ordem nem resolve duas etapas num ato só. Q5 foi encerrada por leitura de A-03 já vigente, sem decisão nova de segregação. Acumulação com administrador não cria autoridade de domínio (CT-12/28). Administração acumulada tem partições positivas em CT-05/09/17/36 (solicitante), CT-25/31 (gestor) e CT-75 (diretor). CT-12/28 são apenas controle negativo de administrador sem vínculo, não prova dessas acumulações.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Papéis acumulados não eliminam etapas

    Esquema do Cenário: [CT-70] Solicitante que é gestor pode aprovar ou rejeitar sua primeira etapa
      Dado Sofia solicitante e gestora do seu centro por A-09, compra aguardando_gestor de <valor> e Dora diretora distinta
      Quando Sofia executa <verbo> como gestora, com "Rever compra" se rejeitar
      Então há uma nova etapa gestor <decisao> por Sofia e situação persistida <destino>, com razão somente na rejeição
      E Dora recebe <emails> e-mails mail; não existe proibição inventada de decisão do solicitante gestor
      
      Exemplos:
        | valor   | verbo    | decisao   | destino            | emails | partição           |
        | 5000.00 | aprovar  | aprovada  | aprovada           | 0      | própria baixa      |
        | 5000.01 | aprovar  | aprovada  | aguardando_diretor | 1      | própria alta       |
        | 5000.00 | rejeitar | rejeitada | rascunho           | 0      | própria rejeição baixa |
        | 5000.01 | rejeitar | rejeitada | rascunho           | 0      | própria rejeição alta |
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Papéis acumulados não eliminam etapas

    Cenário: [CT-71] Ser diretor não permite ao solicitante pular o gestor
      Dado Sofia solicitante e diretora, Guilherme gestor distinto e sua compra de "6000.00" em rascunho
      Quando Sofia envia
      Então a situação persistida é aguardando_gestor, nenhuma aprovação é registrada e somente Guilherme recebe um e-mail mail
      E a condição de diretora de Sofia não conclui nem antecipa uma decisão; a decisão posterior de Sofia como diretora está especificada em CT-75
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Papéis acumulados não eliminam etapas

    Cenário: [CT-72] Gestor que também é diretor não conclui dois níveis num único ato
      Dado Guilherme gestor e diretor da Acme, Dora outra diretora e compra de Sofia de "6000.00" aguardando_gestor
      Quando Guilherme aprova uma vez
      Então a solicitação fica aguardando_diretor com exatamente uma nova aprovação de etapa gestor por Guilherme
      E Guilherme e Dora recebem cada um um e-mail mail da próxima etapa; a segunda decisão em ato separado por Guilherme é especificada em CT-75
```

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Papéis acumulados não eliminam etapas

    Esquema do Cenário: [CT-75] Qualquer diretor da organização resolve sua etapa inclusive com papéis acumulados
      Dado compra de Sofia de "6000.00" aguardando_diretor por transições reais, com aprovação do gestor preservada e <ator> diretor da organização que acumula <par>
      Quando <ator> executa <verbo> como diretor, com "Rever compra" se rejeitar
      Então o destino persistido é <destino> e há exatamente uma nova etapa diretor <decisao> por <ator>, com razão somente na rejeição
      E a aprovação de gestor anterior permanece idêntica e não há e-mail a solicitante, gestor ou diretores existentes
      
      Exemplos:
        | ator      | par                     | verbo    | destino  | decisao   | partição                     |
        | Sofia     | solicitante e diretor   | aprovar  | aprovada | aprovada  | S×D aprovação                |
        | Sofia     | solicitante e diretor   | rejeitar | rascunho | rejeitada | S×D rejeição                 |
        | Guilherme | gestor e diretor        | aprovar  | aprovada | aprovada  | G×D segundo ato separado     |
        | Guilherme | gestor e diretor        | rejeitar | rascunho | rejeitada | G×D rejeição como diretor    |
        | Alice     | administrador e diretor | aprovar  | aprovada | aprovada  | admin×D aprovação           |
        | Alice     | administrador e diretor | rejeitar | rascunho | rejeitada | admin×D rejeição            |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-84 | Proibir sempre solicitante igual ao gestor | CT-70 | A-09 permite; etapa gestor de Sofia é persistida nas duas alçadas. |
| M-85 | Solicitante diretor envia direto à sua própria etapa | CT-71 | Destino é aguardando_gestor e nenhuma decisão é criada. |
| M-86 | Gestor diretor satisfaz ambos os níveis com uma única aprovação | CT-72 | Uma única aprovação deixa pendência de diretor, sem etapa diretor gravada. |
| M-94 | Proibir decisão de diretor porque ele é solicitante ou decidiu a etapa gestor | CT-75 | A-03 aceita qualquer diretor da organização: segundo ato separado resolve a etapa em ambos os verbos, mantendo aprovação anterior. |
| M-95 | Permitir autoaprovação do gestor mas proibir somente sua própria rejeição | CT-70 | Sofia gestora e solicitante rejeita com razão nas duas alçadas e grava rejeição de gestor em rascunho. |
| M-99 | Recusar ação elegível apenas porque o solicitante, gestor ou diretor acumula administração | CT-05, CT-09, CT-17, CT-25, CT-31, CT-36, CT-75 | Administração somada ao vínculo legítimo não impede editar/excluir/enviar/cancelar próprios ou aprovar/rejeitar a etapa elegível. |

## Regra R24 — A interação JavaScript torna as ações e seus erros operáveis

> Origem: RQ-04/07/08/12; A-10/A-12 · perfil **completo** · técnica: **Interação JS e erro visível**.

Especificação G6 no 05. Browser acrescenta execução real de JS; não duplica matriz de autorização ou a cobertura completa de validação do domínio. Dois CT-B cabem no teto completo: um caminho feliz e um erro visível.

Os cenários CT-B01/CT-B02 estão no 05, grupo G6.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-87 | Renderizar Enviar mas perder o listener que abre/submete a confirmação | CT-B01 | Modal aparece por clique real e, após confirmar, estado visível muda para aguardando_gestor. |
| M-88 | Erro de justificativa existe no servidor mas Alpine fecha modal sem mostrá-lo | CT-B02 | Modal continua visível com erro junto à justificativa, sem mudar a compra. |
| M-89 | Associar o erro à instância errada de modal e deixar o formulário rejeitado sem mensagem | CT-B02 | A mensagem fica visível junto ao campo justificativa da solicitação alvo. |

## Checklist de Taxonomia

Checklist percorrido integralmente uma vez (passo 4), depois confrontado com os cenários e mutantes (passo 6).
CT significa cenário especificado, **não** teste executado. Lacuna indica exatamente a parte que o cenário citado não prova.

| Gatilho | Resposta e limite de cobertura | Grupo |
|---|---|---|
| IDOR / autorização horizontal | CT-11/12/28/60/61; pessoas e registros de contraste realmente existentes. | G1/G3/G4 |
| Autorização na ação, não só can() | CT-12/28/57 fora da UI; CT-13/29/58 pelo componente. | G1/G2/G3/G4 |
| Idempotência de cada escrita | CT-39/40 para enviar, aprovar gestor baixo/alto, aprovar diretor, rejeitar gestor/diretor, cancelar e excluir/editar. Criação sem chave de intenção: lacuna Q9. Idempotência de criar centro também depende dessa definição. | G1 |
| Domínio condicionado | CT-22/23/24/34: valor × destino, antes/depois de correção; CT-30/31: justificativa × rejeição nas duas etapas. | G1 |
| Fronteira de cada campo em cada entrada | CT-03/04/07/08 para presença na criação/edição, CT-22/24 para limiar monetário no uso e valor persistido. Mínimo/máximo/precisão monetária Q1 e tetos de texto Q2/Q7 são lacunas declaradas; não há BVA inventado. | G1/G2 |
| Concorrência | CT-41 exige processos/conexões e barreira reais; CT-40 é somente snapshot obsoleto. Lacuna de execução L3. | G5 |
| Destinatário 0/1/N | CT-20 zero gestor com warning de A-10; CT-43 um gestor; CT-44 um/vários diretores. Zero diretores: lacuna Q4. Zero destinatários não é evidência de não-efeito. | G1 |
| Ausente ≠ null ≠ "" | CT-03/30 separam ausência, null e vazio; campo opcional gestor aceita falta segundo A-10, mas semântica de "" na FK é lacuna Q7. | G1 |
| Paginação | CT-50: 0,1,L,L+1 e status correlacionado a IDs. Inserção entre páginas: lacuna L2/Q3, política de ordenação/consistência não determinada; não declarada coberta. | G2 |
| Ordenação / coluna inválida / empate | CT-66 tenta coluna fora de domínio/tipo errado com invariante de isolamento. Política nullable/empate e resposta de robustez são lacunas L1/L2; nenhum CT afirma ordenação não pedida. | G4 |
| Data/hora, timezone e DST | CT-51/52 fixam criação e decisões em dias/instantes UTC diferentes e verificam os valores persistidos/exibidos. Lacuna Q10 para política geral de fuso/formato/virada de dia. Sem SLA ou validade temporal de compra no 00. | G2 |
| Texto livre / Unicode / espaços / teto | CT-30/31: justificativa vazia, espaços, X, acento e emoji. Descrição Unicode no cadastro pode usar os dados literais CT-01. Teto n/n+1 e normalização: lacunas Q2/Q7, inclusive no domínio. | G1/G2 |
| Unicidade + SoftDeletes | Lacuna declarada Q7: identidade por nome e reuso após exclusão não decididos. Não assumir unicidade do plano como requisito. | G1 |
| Removido/desativado ainda escreve | CT-68: cópia real de rascunho excluído tenta editar/enviar/excluir. Não substituído por teste de ausência na tabela. | G1 |
| CRUD combinado | CT-05/53 salvam sem mudança; CT-39 repete exclusão; CT-69 recebe ID inexistente. Centro inexistente/uso de centro excluído: lacuna Q7/L2, sem comportamento arbitrável. | G1/G2 |
| Mass assignment solicitação | CT-64/65: solicitante_id, tenant_id, situacao, criação e edição com um campo forjado por linha. | G3/G4 |
| Mass assignment centro | CT-64/65: tenant_id na criação/edição por administrador legítimo; mudança de gestor por usuário comum recusada CT-57/58. | G3/G4 |
| Mass assignment etapa | CT-65: decidido_por_id, etapa, decisao e coleção etapas forjados. Acesso direto autônomo da filha: lacuna L1; não fechado pelo teste do pai. | G4 |
| Upload | não se aplica: nenhum upload consta no 00 ou na tabela de UI. Nenhum controle de upload é dispensado em superfície existente; implementar upload seria aumento de escopo. | — |
| Precisão monetária | CT-22/24 usam strings e centavo discriminante 5000.01; política de terceira casa, máximo e arredondamento: lacuna Q1. Nenhum mutante float é dito morto sem contraexemplo discriminante. | G1 |
| Superfície Livewire inteira | CT-63/65/66 para entradas conhecidas e tipo/domínio errados; lacuna L1: 02 ausente impede inventário por linha, inclusive public methods/properties e Locked. | G2/G4 |
| Estado do framework em índice/parse/coluna | CT-66 para filtros/busca/coluna conhecidos; consumos específicos de parse/índice em widgets não inventariados: lacuna L1. Não há afirmação de que inexiste widget ou método público. | G4 |
| Método público chamável por $wire | Lacuna L1: falta tabela do 02 e vendor; CT-66 não é prova de todos os métodos. | G4 |
| IDOR por tabela: solicitacoes_compra | CT-60/61/73 para gravação, rota, ação e listagem com tenant presente; CT-74 para papel diretor em contexto errado. | G3/G4 |
| IDOR por tabela: centros_custo | CT-60/61/62/73 para registro, ação, associação e listagem com tenant presente. | G3/G4 |
| IDOR por tabela: etapas_aprovacao_compra | CT-63 tenta entidade filha pelos pontos cliente conhecidos; **lacuna L1 para entrada direta**. Mutante sem matador explícito em R19. | G4 |
| Escopo com discriminante nulo | CT-67 prova invariante no painel; resposta/destino exatos Q8. Não se altera a consulta global deliberada de BelongsToTenant fora de request. | G4 |
| Saída do erro | CT-59 pareia recusas de autorização/ID; CT-69 aponta CT-59; CT-21 mantém rascunho corrigível. Tenant nulo: lacuna de destino Q8. Nenhum 5xx é aceite de negócio. | G2/G3/G4 |
| Canal/tipo do efeito | CT-43/44/47 afirmam mail e solicitação/etapa, não apenas notification existente. | G1/G3 |
| Não-efeito e atomicidade | CT-19/26/27/30/45 têm destinatários reais; CT-42 falha após escrita; CT-46 falha após ponto de efeito. Prova prática ainda L3. | G1 |
| Acumulação de papéis | CT-70 cobre S×G nos dois verbos; CT-75 cobre S×D/G×D/admin×D. CT-05/09/17/36 e CT-25/31 variam administração com vínculo legítimo de solicitante/gestor. Q5 encerrada por A-03; CT-71/72 preservam ordem. | G1 |
| Histórico / link do e-mail | CT-51/52 preservam e exibem a Sofia as pessoas históricas. Público adicional e contrato/link do e-mail: lacuna Q3. | G2 |

## Gate de falsificabilidade e poda

- Cada regra tem de dois a cinco mutantes em padrão, três a seis em completo; achado adversarial poderá exceder teto, identificado pela origem.
- A tabela de cada regra registra o valor/asserção divergente. IDs abaixo são de especificação; **não houve execução de mutantes**.
- Todos os CT têm situação de partida (ou ausência de registro para criação) e não-efeitos nomeados. Exemplos separam uma entrada inválida por linha; estado válido é fixado ao testar identidade/justificativa.
- A matriz tem 40 células efetivamente resolvidas por operação, com 21 inválidas; edição cruza os três campos em cada estado fora do rascunho.
- O gate foi **executado com lacuna declarada**: acesso direto da entidade filha não inventariado, mutante de R19 sem matador. Isso não é aprovação integral do gate.
- As técnicas que dependem de decisão inexistente estão bloqueadas no recorte, sem apagar CT de partes determinadas. Não há equivalência presumida para justificar mutante vivo.

| Cogitado e cortado | Motivo / alternativa |
|---|---|
| Reproduzir todo fluxo entre três personas em Browser | Estado, destinatário e histórico são falsificáveis por G1/G2; G6 fica só com JS. |
| Browser para autorização/visibilidade de cada botão | CT-13/16/29/58 provam isso no componente. |
| Unit de predicado imaginado exigeDiretor | RQ-05 afirma decisão persistida, não contrato de função pura; G1 é a camada existente adequada. |
| CT dos logs info/warning definidos somente no plano | Nenhuma origem no 00 para esses logs. Exceção explícita: warning de A-10 no CT-20, após ADV-08. |
| Min 0.01, max descricao 255, nome 120 e unique do plano | Comportamento não decidido no 00; perguntas Q1/Q2/Q7. |
| Teste “duas chamadas” como prova de simultaneidade | CT-40 mede leitura obsoleta; CT-41 exige barreira e conexões reais. |
| Mutante “usar float” morto por valor redondo | Sem contraexemplo executado não há prova; usar apenas perda concreta de centavo em CT-22/24. |
| Teste só can() para administração de centros | CT-57/58 disparam escrita real e detectam ligação ausente da policy. |
| GET de criação como única prova de formulário | Visitas CT-56 pareadas às gravações CT-02/06/54/55. |
| Tema/cor/axe sem requisito de aparência | Não criar contrato visual novo; CT-B afirma modal/erro visíveis. |
| Prometer deduplicação da criação sem chave de intenção | Q9; não confundir dois pedidos legítimos com retry identificado. |

## Índice de Cenários

Arquivos abaixo são **alocação proposta**, não arquivos implementados. A costura e o grupo são confirmados para a materialização futura.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo proposto | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | Persistir os três dados e o solicitante autenticado | R1 | EP e gravação por entrada | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-03 |
| CT-02 | O formulário de criação grava os dados de compra | R1 | EP e gravação por entrada | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-03 |
| CT-03 | A ausência de um dado obrigatório é recusada também fora da UI | R1 | EP e gravação por entrada | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-01, M-02 |
| CT-04 | O formulário identifica isoladamente o dado obrigatório ausente | R1 | EP e gravação por entrada | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-02 |
| CT-05 | Cada campo editável muda no rascunho pelo domínio | R2, R23 | EP criação ≠ edição; campos e salvamento | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-05, M-06, M-99 |
| CT-06 | A edição do formulário persiste valor e centro novos | R2 | EP criação ≠ edição; campos e salvamento | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-05, M-06 |
| CT-07 | A edição não contorna dados obrigatórios fora da UI | R2 | EP criação ≠ edição; campos e salvamento | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-04 |
| CT-08 | O save valida novamente os dados obrigatórios | R2 | EP criação ≠ edição; campos e salvamento | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-04 |
| CT-09 | O solicitante exclui seu rascunho por fora do componente | R3, R23 | Estado × operação; identidade; ação destrutiva | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-08, M-90, M-99 |
| CT-10 | Excluir pela ação remove o rascunho correto | R3 | Estado × operação; identidade; ação destrutiva | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-09 |
| CT-11 | Pessoa diferente não exclui o rascunho alheio | R3 | Estado × operação; identidade; ação destrutiva | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-07, M-08 |
| CT-12 | Nem papel de aprovador nem administração substituem o solicitante | R4 | Matriz papel × ação completa e par UI/domínio | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-10, M-11, M-12 |
| CT-13 | A UI não oferece ação do solicitante a outra pessoa | R4 | Matriz papel × ação completa e par UI/domínio | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-12 |
| CT-14 | Nem o dono altera campo decisivo depois do envio | R5 | Matriz estado × operação, campo e persona | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-13, M-15 |
| CT-15 | Nem o dono exclui solicitação em trânsito ou terminal | R5 | Matriz estado × operação, campo e persona | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-14, M-15 |
| CT-16 | O componente não permite editar nem excluir fora do rascunho | R5 | Matriz estado × operação, campo e persona | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-15 |
| CT-17 | Envio direto deixa pendente do gestor específico | R6, R23 | EP, estado × operação e destinatário 0/1 | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-16, M-99 |
| CT-18 | Enviar pela ação usa o registro e o centro corretos | R6 | EP, estado × operação e destinatário 0/1 | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-16, M-19 |
| CT-19 | Reenvio fora de rascunho não encaminha novamente | R6 | EP, estado × operação e destinatário 0/1 | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-17 |
| CT-20 | Sem gestor o envio falha fechado | R6 | EP, estado × operação e destinatário 0/1 | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-18, M-91 |
| CT-21 | O envio sem gestor apresenta recusa e mantém a solicitação corrigível | R6 | EP, estado × operação e destinatário 0/1 | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-18 |
| CT-22 | O valor literal de fábrica separa 5000.00 de 5000.01 | R7 | BVA 3-valores em centavos; criação/edição/uso | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-20, M-21, M-24 |
| CT-23 | A configuração realmente muda a alçada | R7 | BVA 3-valores em centavos; criação/edição/uso | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-20, M-22, M-96 |
| CT-24 | Centavos gravados na criação e na correção chegam íntegros à decisão | R7 | BVA 3-valores em centavos; criação/edição/uso | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-21, M-23 |
| CT-25 | Cada aprovação válida produz sua etapa e seu destino | R8, R23 | Tabela de decisão completa; estado × evento; papel × verbo | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-28, M-29, M-99 |
| CT-26 | Aprovação em estado sem etapa pendente é recusada | R8 | Tabela de decisão completa; estado × evento; papel × verbo | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-27 |
| CT-27 | Rejeição em estado sem etapa pendente é recusada | R8 | Tabela de decisão completa; estado × evento; papel × verbo | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-26, M-27 |
| CT-28 | Identidade errada falha separadamente em aprovar e rejeitar | R8 | Tabela de decisão completa; estado × evento; papel × verbo | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-25, M-26 |
| CT-29 | Ações de decisão correspondem à etapa e gravam decisão real | R8 | Tabela de decisão completa; estado × evento; papel × verbo | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-25, M-28 |
| CT-30 | Justificativa ausente ou vazia não devolve ao rascunho | R9 | EP de ausência e tipo; BVA no mínimo de conteúdo existente | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-30, M-31, M-33 |
| CT-31 | Uma razão presente permite rejeitar na etapa corrente | R9, R23 | EP de ausência e tipo; BVA no mínimo de conteúdo existente | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-32, M-33, M-99 |
| CT-32 | O modal de rejeição aponta somente o erro da justificativa | R9 | EP de ausência e tipo; BVA no mínimo de conteúdo existente | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-30, M-33 |
| CT-33 | Após rejeição o novo envio recomeça pelo gestor | R10 | 2-switch e domínio condicionado pela correção | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-34, M-35 |
| CT-34 | O novo ciclo considera a correção de valor e centro | R10 | 2-switch e domínio condicionado pela correção | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-35, M-36 |
| CT-35 | Rejeição do componente mostra o rascunho com a razão e libera correção | R10 | 2-switch e domínio condicionado pela correção | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-35, M-37 |
| CT-36 | Cancelar nas duas etapas preserva o registro e as decisões já feitas | R11, R23 | Estado × operação e identidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-39, M-40, M-99 |
| CT-37 | Cancelar em rascunho ou estado terminal é recusado | R11 | Estado × operação e identidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-38 |
| CT-38 | A ação cancelar produz estado cancelada na UI | R11 | Estado × operação e identidade | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-39, M-40, M-97 |
| CT-39 | Uma execução válida seguida de retry tem um único efeito | R12 | Idempotência no agregado persistido; retry sequencial e leitura obsoleta | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-42, M-43, M-44 |
| CT-40 | Duas cópias elegíveis não tornam a decisão repetível | R12 | Idempotência no agregado persistido; retry sequencial e leitura obsoleta | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-41, M-42, M-43, M-44 |
| CT-41 | Duas escritas realmente simultâneas não vencem a mesma etapa | R13 | Concorrência real e rastreio de atomicidade | G5 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/ConcorrenciaTest.php` | M-45, M-46, M-48 |
| CT-42 | Falha depois da primeira escrita não deixa estado sem decisão correspondente | R13 | Concorrência real e rastreio de atomicidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-47 |
| CT-43 | Envio entrega somente e-mail ao gestor escolhido | R14 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-49, M-54 |
| CT-44 | Encaminhamento alto avisa todos os diretores atuais | R14 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-49, M-50 |
| CT-45 | Não há avisos quando não existe próxima etapa pedida | R14 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-51 |
| CT-46 | Falha no commit após o ponto de notificação não produz aviso fantasma | R14 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-52 |
| CT-47 | Diretor de outra organização não recebe e-mail desta | R14 | Rastreio do canal, destinatário, 0/1/N, não-efeito e atomicidade | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-53 |
| CT-48 | Cada estado aparece associado à solicitação correta na listagem | R15 | EP exaustiva de estado; paginação | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-55, M-56 |
| CT-49 | Cada estado aparece no detalhe do registro correspondente | R15 | EP exaustiva de estado; paginação | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-55, M-56 |
| CT-50 | A situação é correta também nas bordas da paginação | R15 | EP exaustiva de estado; paginação | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-57 |
| CT-51 | O detalhe mostra quem decidiu cada etapa e não o cadastro atual | R16 | Rastreio histórico e EP de 0/1/N decisões | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-58, M-60, M-98 |
| CT-52 | Participantes de ciclos diferentes continuam identificáveis | R16 | Rastreio histórico e EP de 0/1/N decisões | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-58, M-59, M-98 |
| CT-53 | Administração autorizada cria, edita e exclui centro não utilizado | R17 | CRUD, par visita/gravação, criação ≠ edição | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-61, M-64 |
| CT-54 | Criar centro pelo componente persiste o vínculo de gestor | R17 | CRUD, par visita/gravação, criação ≠ edição | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-61 |
| CT-55 | Editar centro pelo componente persiste um gestor diferente | R17 | CRUD, par visita/gravação, criação ≠ edição | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-61, M-62 |
| CT-56 | As quatro páginas de escrita apresentam os campos da operação | R17 | CRUD, par visita/gravação, criação ≠ edição | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-63 |
| CT-57 | Panel user não cria, altera ou exclui centro nem se nomeia gestor | R18 | Papel × ação e autorização fora da UI | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-65, M-66 |
| CT-58 | O componente aplica a recusa administrativa em cada ação | R18 | Papel × ação e autorização fora da UI | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-65, M-66 |
| CT-59 | Após recusa o usuário conserva uma página de negócio alcançável | R18 | Papel × ação e autorização fora da UI | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-67, M-68 |
| CT-60 | Contexto errado não dá autoridade mesmo a pessoa com vínculo legítimo no outro | R19 | IDOR por entidade e fronteira de associação na gravação | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-69 |
| CT-61 | Route binding e componente recusam IDs da outra organização | R19 | IDOR por entidade e fronteira de associação na gravação | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-70 |
| CT-62 | A gravação rejeita relação com entidade de outra organização | R19 | IDOR por entidade e fronteira de associação na gravação | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-71 |
| CT-63 | A entrada cliente não alcança histórico estrangeiro pela solicitação atual | R19 | IDOR por entidade e fronteira de associação na gravação | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-72 |
| CT-64 | Payload externo não troca campos de autoridade | R20 | Mass assignment por tabela e fronteira de gravação | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-74, M-75, M-77 |
| CT-65 | Payload do componente não fabrica aprovação nem altera autoria da etapa | R20 | Mass assignment por tabela e fronteira de gravação | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-74, M-75, M-76, M-77 |
| CT-66 | IDs e estado do framework forjados não atravessam a fronteira | R21 | Domínio inválido e tipo errado por entrada conhecida; discriminante nulo | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-78, M-79 |
| CT-67 | Perder o tenant no painel não abre a instalação | R21 | Domínio inválido e tipo errado por entrada conhecida; discriminante nulo | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-80 |
| CT-68 | Cópia de rascunho excluído não revive ou encaminha compra | R22 | Estado removido × operação; CRUD inexistente e saída de erro | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-81, M-82 |
| CT-69 | ID inexistente falha sem prender a navegação autorizada | R22 | Estado removido × operação; CRUD inexistente e saída de erro | G2 | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-83 |
| CT-70 | Solicitante que é gestor pode aprovar ou rejeitar sua primeira etapa | R23 | Tabela de decisão e sondas par a par | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-84, M-95 |
| CT-71 | Ser diretor não permite ao solicitante pular o gestor | R23 | Tabela de decisão e sondas par a par | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-85 |
| CT-72 | Gestor que também é diretor não conclui dois níveis num único ato | R23 | Tabela de decisão e sondas par a par | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-86 |
| CT-73 | Com tenant presente a listagem não inclui registros de outra organização | R19 | IDOR por entidade e fronteira de associação na gravação | G4 | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-92 |
| CT-74 | Ser diretor somente em outra organização não autoriza decidir na atual | R8 | Tabela de decisão completa; estado × evento; papel × verbo | G3 | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` | M-93 |
| CT-75 | Qualquer diretor da organização resolve sua etapa inclusive com papéis acumulados | R23 | Tabela de decisão e sondas par a par | G1 | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` | M-94, M-99 |

## Limitações, desvios e registros destinados ao 03

Nenhum 03 foi criado, por instrução da rodada. Este registro e o retorno substituem somente o local do registro, não a evidência que falta.

| ID | Limitação / desvio | Tratamento e efeito |
|---|---|---|
| L1 | 02 ausente; nenhuma Superfície Livewire autoritativa e vendor vazio. | Inventário parcial declarado, sem criar 02; um mutante de IDOR da filha sem matador. Não afirmar proteção herdada pelo pai nem ausência de entrada direta. |
| L2 | Requisito não decide tetos, política de ordenação, exclusão de centro usado, consulta adicional e normalizações. | Perguntas no próprio 04; partes determinadas preservadas. Nenhuma recomendação tomada como resposta do usuário. |
| L3 | Sem dependências instaladas ou execução da feature; G3/G4 ainda não registrados e G5 sem DB compartilhado preparado. | Nenhum teste, MSI, corrida ou rollback declarado provado. Inventário de drivers e TestCase feito; não declarar “arnês impossível” sem tentativa na materialização autorizada. |
| L4 | Boost search-docs ausente nas ferramentas. | Docs oficiais e moldes do projeto; inspeção da versão exata de vendor/deprecations permanece pendente. |
| L5 | Código não deve ser implementado e nenhum arquivo fora da saída pode mudar. | Sem Pest/migration/model/service; não registrar rule, não instalar dependência nem alterar Pest.php/phpunit.xml. |
| L6 | 00/01 imutáveis e formato antigo do 00 sem Estado/P-nn. | A-01–A-12 aceitas como dadas; perguntas novas aqui, sem editar origens. |
| L7 | Host Codex não aplica hooks Claude nem impõe leitura por path ao subagente. | Revisão em contexto novo por fork_turns=none, contrato de leitura, hashes antes/depois; isso não é sandbox de leitura. |
| L8 | Pasta sem .git. | Auditoria de integridade por hashes dos arquivos relevantes, não git status como prova. |
| L9 | Apenas etapa de derivação pedida. | Não executar steps 0–6 anteriores ou 8–12 da feature-wiki nem revisão de código/QA da implementação. |
| L10 | Segunda rodada trouxe achado estrutural de acumulação administrativa; teto de duas rodadas. | Partições e oráculos reforçados pela sessão. Escalonamento registrado ao futuro implementador/QA: conferir a matriz ampliada; não há selo de terceira revisão independente dos fechamentos finais. |

### Revisão adversarial e despachos

A revisão foi disparada pela sessão principal após as costuras confirmadas. Modelo informado pelo adversário: **Codex baseado em GPT-6**, herdado; variante/esforço não expostos.
Entradas de artefato: somente 00, 04 e 05. Contrato/perfil de rota lidos como instrução. Sem PRD, código, conjuntos anteriores ou conversa.
Ferramentas de leitura por shell foram permitidas apenas por contrato; hooks Claude e sandbox de leitura por path não se aplicam. Nenhuma leitura negada ou violação reportada.
Hashes de 00/01/04/05, Pest.php, TestCase.php, TenancyTestCase.php e phpunit.xml foram comparados antes/depois: **8/8 iguais em cada rodada**.
Leitura integral reportada pelo adversário, percorrendo R1–R24 e todas as áreas; amostrados ADV-01, ADV-02 e ADV-09 contra seus CT e A-03/A-10.

| # | Rota / agente | Contexto/modelo | Dependência | Resultado | Custo reportado |
|---|---|---|---|---|---|
| 1 | fw-adversario-ct via collaboration.spawn_agent, adversario_ct_1 | fork_turns=none; GPT-6 herdado | costuras confirmadas | 10 achados, todos fechados abaixo; nenhum arquivo alterado pelo revisor | — |
| 2 | fw-adversario-ct via collaboration.spawn_agent, adversario_ct_2 | fork_turns=none; GPT-6 herdado | novos CT-73/74/75 após rodada 1 | 5 achados fechados por reescrita; nenhum arquivo alterado pelo revisor | — |

Sem despacho para contagens e confirmação de costuras: checagens determinísticas locais e decisão da sessão previstas no contrato de hosts.
Derivação feita pela sessão com a feature-test-design invocada, a partir do 00; a sessão não escreveu o plano da linha de base.

| Rodada | Achado | Destino do fechamento | Evidência discriminante |
|---|---|---|---|
| 1 | ADV-01 — listagem global com tenant presente | cenário novo CT-73; M-92 | Mesmo ator possui vínculo nas duas organizações; Acme não mostra identificadores reais da Globex nas duas entidades. |
| 1 | ADV-02 — papel diretor de outro tenant | cenário novo CT-74; M-93 | Compra e contexto são Acme; membro válido tem diretor só na Globex; aprovar e rejeitar recusados. |
| 1 | ADV-03 — tenant_id forjado no save de compra | oráculo reescrito CT-64/65, linhas específicas de edição | Mesmo rascunho deve permanecer na Acme ou sofrer recusa integral sem escrita parcial. |
| 1 | ADV-04 — excluir rascunho devolvido com histórico | oráculo reescrito CT-09 e M-90 | Dataset inclui rejeições reais de gestor e diretor; exclusão própria deve funcionar com histórico. |
| 1 | ADV-05 — no-op não discrimina recusa | alegação/oráculo de M-06 reescrito | M-06 limita-se agora à criação indevida de registro no save; linhas no-op não afirmam sucesso não decidido. |
| 1 | ADV-06 — exclusão em massa de centros | oráculo reescrito CT-53 | Centro Financeiro de contraste preserva existência, nome e gestor após excluir somente o alvo. |
| 1 | ADV-07 — obrigação inventada de aceitar payload forjado | oráculos CT-64/65 e M-77 reescritos | Recusa integral é permitida; corrupção ou escrita parcial seguida de recusa continua proibida. |
| 1 | ADV-08 — warning decidido no próprio 00 | oráculo reescrito CT-20; M-91 | Warning por falta de gestor observado por A-10; exceção à proibição genérica da skill declarada. |
| 1 | ADV-09 — Q5 suspende o que A-03 já decidiu | cenário novo CT-75; M-94; Q5 encerrada por premissa dada | S×D e G×D resolvem etapa diretor em ato separado, aprovando e rejeitando. |
| 1 | ADV-10 — S×G só tinha aprovação | oráculo reescrito CT-70; M-95 | Solicitante gestor também rejeita com razão em ambas as alçadas. |

Rodada 1: **3 cenários novos e 7 fechamentos por reescrita de oráculo**, nenhuma descoberta encerrada apenas como lacuna.
Lacunas previamente declaradas, especialmente acesso direto da filha e limites de texto, continuam declaradas; não foram “fechadas” por associação.
Rodada 2 foi executada em novo contexto. O adversário confirmou que os dez contraexemplos da primeira rodada já são discriminados. Foram encontrados cinco novos achados, fechados abaixo.

| Rodada | Achado | Destino do fechamento | Evidência discriminante |
|---|---|---|---|
| 2 | R2-ADV-01 — alçada só aumenta | oráculo reescrito CT-23; M-96 | Limite 3000.00, com 2999.99/3000.00/3000.01, distingue max(5000,config). |
| 2 | R2-ADV-02 — cancelamento deixa badge obsoleto | oráculo reescrito CT-38; M-97 | A própria listagem já montada mostra cancelada após a ação, sem reload. |
| 2 | R2-ADV-03 — instante histórico sem valor esperado | oráculos CT-51/52 reescritos; M-98 | Criação em18/10 e decisões reais em20/22/24/26 de outubro têm instantes literais diferentes, persistidos e exibidos. |
| 2 | R2-ADV-04 — M-19 apontava matadores que não divergiam | oráculo CT-18 e matador de M-19 reescritos | Após envio, a mesma instância do componente mostra aguardando_gestor; CT-21 saiu da atribuição. |
| 2 | R2-ADV-05 — administração acumulada sem caso elegível | oráculos/datasets CT-05/09/17/25/31/36/75 reescritos; M-99 | Papel administrativo adicional não barra ação de solicitante, gestor ou diretor legitimamente elegível. |

Rodada 2: **0 IDs de cenário novos; 5 fechamentos por reescrita de oráculo/dataset**, nenhuma descoberta encerrada apenas como lacuna.
Total: **15 achados fechados**, com três CT novos na primeira rodada e doze fechamentos por reescrita nas duas rodadas.
A segunda rodada percorreu R1–R24, confirmou os dez fechamentos e leu 00/04/05 integralmente. Amostrados os valores de CT-23, o componente de CT-18/38 e os pares administrativos de CT-75.
Leitura negada: nenhuma. Um path relativo inicial de perfil retornou inexistente; o agente leu o perfil no caminho permitido da skill, sem contornar uma negativa de política.
**Teto atingido:** não houve terceira revisão. Achado estrutural de acumulação administrativa foi tratado ampliando as partições da matriz de identidade, sem novo ID e sem extrapolar seis mutantes de R23. O fechamento final é da sessão e deve ser conferido na materialização/QA (L10); isso não é nova aprovação independente.

## Referências Abertas

Abertas somente as referências mandadas pela etapa em execução; nenhuma pasta references foi lida em lote.

- `.ai/skills/feature-wiki/references/hosts-e-subagentes.md` — step 7, adaptação do host antes dos despachos.
- `.ai/skills/feature-wiki/references/delegacao-casos-de-teste.md` — step 7, contrato de entrada e saída.
- `.ai/skills/feature-wiki/references/ponytail-caveman.md` — início da invocação, fronteira da prosa.
- `.ai/skills/feature-wiki/references/roteamento-e-despacho.md` — step 7, antes de despachar revisão.
- `.ai/skills/feature-wiki/references/citacoes-de-codigo.md` — step 7, antes de registrar citações.
- `.ai/skills/feature-wiki/references/template-03-progresso.md` — step 7, formato do registro substituído no retorno.
- `.ai/skills/feature-test-design/references/template-04.md` — passos 2/6/7 e escrita do 04.
- `.ai/skills/feature-test-design/references/escolha-de-camada.md` — passos 2/7, costuras e alocação.
- `.ai/skills/feature-test-design/references/tecnicas-por-regra.md` — passo 3, técnicas formais.
- `.ai/skills/feature-test-design/references/taxonomia-de-defeito.md` — passo 4, checklist inteiro.
- `.ai/skills/feature-test-design/references/gherkin.md` — passo 5, antes dos cenários.
- `.ai/skills/feature-test-design/references/armadilhas-de-api.md` — passos 5/7, antes de nomear helpers.
- `.ai/skills/feature-test-design/references/mutation-testing.md` — passo 6, operadores e gate previsto.
- `.ai/skills/feature-test-design/references/revisao-adversarial.md` — revisão, antes do primeiro despacho.
- `.ai/skills/feature-test-design/references/pest-plugin-browser.md` — gate e escrita do 05.
- `.ai/skills/feature-test-design/references/template-05.md` — escrita do 05.

## Verificação desta especificação

Conferências determinísticas finais em **2026-10-20**, somente na pasta de saída:

```text
grep -cE '^[[:space:]]*(Cenário|Esquema do Cenário): \[CT-[0-9]+\]' 04-casos-de-teste.md
75
grep -cE '^## Regra R[0-9]+' 04-casos-de-teste.md
24
grep -cE '^\| M-?[0-9]+' 04-casos-de-teste.md
99
grep -cE '^\| M-?[0-9]+.*sem matador' 04-casos-de-teste.md
1
grep -cE '^[[:space:]]*Cenário: \[CT-B[0-9]+\]' 05-casos-de-teste-browser.md
2
```

No PowerShell, grep foi executado pelo binário `C:\Program Files\Git\usr\bin\grep.exe`, com esses padrões e paths explícitos.
Conferência programática por regex sobre os arquivos gravados:
- 75 definições de CT e 75 linhas de índice, diferença entre conjuntos **0**.
- IDs de CT duplicados **0**, IDs de mutantes duplicados **0**.
- Gherkin sem Então, com quantidade de Quando diferente de um ou mais de nove passos: **0**.
- Regras fora do piso/teto de mutantes do perfil: **0**.
- Matriz: **19 células válidas + 21 inválidas = 40**.
- SHA-256 de 00, 01 e das duas skills: **4/4 iguais** aos valores anteriores à escrita. Nas duas revisões, **8/8 hashes monitorados iguais** antes/depois.
- Só 04 e 05 foram escritos na pasta autorizada. Nenhum arquivo de teste ou de aplicação foi criado.
- Cenários e mutantes são especificação; **Pest, Browser e --mutate não foram executados**. O mutante sem matador de L1 permanece explícito.

### Materialização e mutação futuras

Executar somente após implementação autorizada, fora desta rodada:
- Registrar FeatureTenancy com TenancyTestCase antes das migrations; materializar todo Então com assertions específicas, inclusive datasets.
- Completar 02/Superfície Livewire por inventário real antes de declarar L1 fechada. Não apagar a linha sem matador para “passar”.
- Confirmar helpers atuais e deprecations no vendor instalado. Mutate consta só transitivamente: registrar declaração direta como ação futura sujeita à autorização de dependências.
- Rodar somente os arquivos afetados; browser em série segundo .ai/rules/testes-browser.md, após build. A rule local vence a permissão genérica de paralelismo da skill.
- Mutação no Windows pelo lançador .cmd da feature-wiki, com escopo da classe efetivamente implementada e covered-only; conferir opções no help, subprocessos reais, duração, sobreviventes e um mutante conhecido. Nenhum comando --mutate foi executado nesta entrega.
- Triar equivalentes com prova e transformar sobreviventes de comportamento acordado em CT antes de corrigir código. Score não substitui rastreabilidade e omissão de requisito.



# Casos de Teste de Browser — FERRO-830: aprovação de compra

> Fonte normativa: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`; regra R24 do 04.
> Runtime proposto: pest-plugin-browser 5.0.1 / Playwright, conforme lock. Nenhuma execução nesta rodada.
> Costura: **browser**, grupo **G6 Interação JS**, confirmado pela sessão em **2026-10-20**.
> Arquivo futuro: `tests/Browser/AprovacaoCompra/InteracaoTest.php`.
> Comando futuro: `vendor/bin/pest --testsuite=Browser --filter=AprovacaoCompra`, **em série**.
> A suíte Browser existe no phpunit.xml. O filtro exige os nomes dos testes com AprovacaoCompra.
> Os demais cenários permanecem no componente/domínio. Dois CT-B: um caminho feliz e um erro visível.

## Pré-requisitos

- [ ] Dependências do lock instaladas e assets produzidos com `npm run build`; não realizados aqui.
- [ ] PHP/Pest/browser funcionais; vendor está vazio nesta cópia. Playwright só foi confirmado em package.json.
- [ ] Usar TestCase + RefreshDatabase já ligados a tests/Browser; fixture single-tenant para isolar JS.
- [ ] Autenticar por `$this->actingAs($ator)` antes de `visit()`; não gastar este CT com login pela tela.
- [ ] Construir situação com transições reais conforme Setup Global do 04; limpar fakes depois do setup.
- [ ] Conferir exclusão de `tests/Browser/Screenshots` do versionamento antes de produzir screenshots; nenhum screenshot criado.
- [ ] Confirmar seletores reais no primeiro build. Não usar ref transitório do MCP ou classe CSS visual.
- [ ] Nenhum servidor externo: o plugin sobe HTTP in-process em porta aleatória; sem artisan serve ou APP_URL.
- [ ] Não usar esperas fixas. Assertions repetem até timeout existente de 20.000 ms.
- [ ] Toda navegação: `assertPathIs()` antes de conteúdo. `assertNoJavaScriptErrors()` é apenas apoio.

Convenção local .ai/rules/testes-browser.md **proíbe --parallel**, mesmo que a skill genérica permita depois de provar isolamento.
MCP/browser manual não é cobertura. Nenhuma observação de UI foi feita nesta rodada.

## Seletores

A UI de compra não foi lida nem implementada. Os seletores abaixo são **contratos de materialização propostos**, não locators comprovados.

| Elemento | Preferência de seletor | Situação |
|---|---|---|
| Página | rota de resource `/app/solicitacoes-de-compra` | Endereço do 01, contexto single-tenant de teste. |
| Ação de registro | texto traduzido Enviar/Rejeitar, com só uma solicitação elegível na fixture | Evitar selecionar ação de outro registro. |
| Modal ativo | `[role="dialog"]` se confirmado no DOM; senão locator acessível real do Filament | Não substituir visibilidade por presença do texto no DOM. |
| Confirmar | botão traduzido dentro do modal ativo | Resolver locator após render; não assumir que todo botão é type=submit. |
| Justificativa | rótulo acessível do campo mostrado no modal | Rótulo exato do 01 não é requisito; usar o que a UI renderizar. |
| Erro da justificativa | elemento visível associado ao campo/aria-describedby | Não afirmar só existência de erro genérico em outro campo. |
| Situação da solicitação | conteúdo associado ao ID/descrição única da fixture | Não aceitar outro badge da página como resultado. |

API de `press`, `assertVisible`, `assertSeeIn`, `assertScript`, `assertPathIs` e console conferida na [documentação oficial do Pest](https://pestphp.com/docs/browser-testing).
Quando o seletor ainda não existe, o roteiro diz como resolvê-lo; não inventa método de espera ou helper de escopo.

## CT-B01: Confirmar envio opera o modal com JavaScript real

**Origem:** RQ-04/12, A-12 · R24 · perfil completo.
**Por que Browser:** listener do botão, abertura efetiva de modal e sincronização visual após request não são executados pelo teste de componente.
A modal é mecanismo da Superfície de UI; o oráculo de negócio continua sendo pendência do gestor.

```gherkin
# language: pt
Funcionalidade: Interação com ações da solicitação de compra
  Regra: A ação de envio é operável no navegador
    Cenário: [CT-B01] Modal e envio funcionam com JavaScript executado
      Dado Sofia autenticada e uma única solicitação própria em rascunho no centro de Guilherme
      Quando Sofia aciona Enviar e confirma a mesma intenção no modal visível
      Então o modal realmente abriu e a linha da solicitação passa visivelmente a aguardando gestor
      E o banco contém aguardando_gestor para essa solicitação, preservando dados e solicitante
```

**Roteiro executável na materialização:**

| # | Ação | API Pest / preparação | Resultado |
|---|---|---|---|
| 1 | Autenticar e abrir listagem | `actingAs(Sofia)`; `visit('/app/solicitacoes-de-compra')->assertPathIs('/app/solicitacoes-de-compra')` | Registro único identificado, estado rascunho visível. |
| 2 | Acionar envio | `->press('Enviar')` | Modal ativo deve satisfazer `assertVisible(locatorDoModal)`. |
| 3 | Confirmar no modal | `->click(locatorDoBotaoConfirmar)`, locator acessível resolvido e único | Request Livewire concluído pelo estado visível, sem wait(n). |
| 4 | Conferir resultado | Assertion de situação ligada à solicitação; se houver navegação, path primeiro | Estado visível aguardando gestor; modal fechado; console sem erro JS. |
| 5 | Uma âncora no banco | assertDatabaseHas com ID, situacao, descricao, valor, centro e solicitante anteriores | Mesmo agregado passou a aguardando_gestor. |

Não repetir assertions completas de e-mails do CT-43: esse não é o valor adicional do Browser.

## CT-B02: Justificativa vazia mantém erro visível no modal correto

**Origem:** RQ-07/08, A-07/A-12 · R24 · perfil completo.
**Por que Browser:** pode existir erro no servidor e o modal fechar, ficar invisível ou perder sua associação com o campo em Alpine.

```gherkin
# language: pt
Funcionalidade: Interação com ações da solicitação de compra
  Regra: A recusa por justificativa ausente permanece visível ao aprovador
    Cenário: [CT-B02] Rejeição vazia mostra o erro sem fechar silenciosamente o modal
      Dado Guilherme autenticado e solicitação de Sofia aguardando_gestor por envio real, com justificativa vazia no modal de rejeição aberto
      Quando Guilherme confirma a rejeição sem justificativa
      Então o modal permanece visível e o erro de obrigatoriedade aparece associado à justificativa
      E o banco conserva aguardando_gestor e o histórico anterior, sem rejeição gravada
```

**Roteiro executável na materialização:**

| # | Ação | API Pest / preparação | Resultado |
|---|---|---|---|
| 1 | Preparar pendência real e autenticar | Transição enviar no setup; limpar fakes; `actingAs(Guilherme)` | Ator é gestor, único erro possível é justificativa. |
| 2 | Abrir listagem e modal | `visit(...)->assertPathIs(...)`, `->press('Rejeitar')`, `->assertVisible(locatorDoModal)` | Modal da solicitação correta, campo vazio. |
| 3 | Submeter vazio | `->click(locatorDoBotaoConfirmarRejeicao)` | Validação ocorre no fluxo real de JS. |
| 4 | Conferir erro operável | `assertVisible(locatorDoModal)` e `assertVisible(locatorDoErro)`; texto obrigatório no contêiner do campo | Não basta assertSee genérico; não fixar redação de mensagem ausente no 00. |
| 5 | Uma âncora no agregado | Leitura com situação e tuplas históricas comparadas ao snapshot | Aguardando_gestor e histórico original; nenhuma rejeição. Console sem erro JS. |

O preenchimento válido completo já é provado em CT-29/35. Não juntar uma segunda intenção de rejeição neste CT-B.

## Mutantes previstos de R24

Fonte única no 04; esta cópia deve permanecer sincronizada.

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-87 | Renderizar Enviar mas perder o listener que abre/submete a confirmação | CT-B01 | Modal aparece por clique real e, após confirmar, estado visível muda para aguardando_gestor. |
| M-88 | Erro de justificativa existe no servidor mas Alpine fecha modal sem mostrá-lo | CT-B02 | Modal continua visível com erro junto à justificativa, sem mudar a compra. |
| M-89 | Associar o erro à instância errada de modal e deixar o formulário rejeitado sem mensagem | CT-B02 | A mensagem fica visível junto ao campo justificativa da solicitação alvo. |

## Roteiro de Validação: Desenhado × Implementado

**Não executado**: escopo desta entrega é somente especificação. A coluna Implementado não foi inferida pelo plano.

| # | Superfície desenhada | Prova prevista | Implementado | Evidência |
|---|---|---|---|---|
| 1 | Listagem com situação e ações | CT-48/50 e CT-B01 | não verificado | nenhuma execução |
| 2 | Form create/edit | CT-02/06, visitas CT-56 | não verificado | nenhuma execução |
| 3 | Detalhe e histórico | CT-49/51/52 | não verificado | nenhuma execução |
| 4 | Modal Rejeitar | CT-29/32/35 e CT-B02 | não verificado | nenhuma execução |
| 5 | Modal Enviar/Cancelar | CT-18/38 e CT-B01 para JS de envio | não verificado | nenhuma execução |
| 6 | Centros, nome e gestor | CT-53/54/55/56 | não verificado | nenhuma execução |

Modal de Cancelar como CT-B foi cogitada e cortada: transição CT-38 no componente e mesmo mecanismo geral de modal de confirmação do CT-B01.
Se a implementação trouxer JS específico de cancelamento que esses CT não exercitem, reabrir o gate com mutante próprio; não declarar prova por semelhança de código.

## Limitações

As lacunas do 04 continuam vigentes, especialmente L1 (02 ausente), L3 (sem execução) e Q3 (visibilidade histórica/link).
Nenhum teste de tema foi criado com assertSee, nenhum baseline de screenshot foi certificado como aparência correta.

