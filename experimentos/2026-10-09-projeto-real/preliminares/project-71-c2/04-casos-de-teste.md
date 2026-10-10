# Casos de Teste — FERRO-830: Aprovação de solicitação de compra

> Requisito: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`.
> Plano: `wikis/specs/oraculo/aprovacao-de-compra/01-plano-acao.md`, somente paths, rotas, stack e Superfície de UI.
> Derivado do **requisito**, não do plano. A implementação da compra não foi lida.
> feature-wiki **4.0.0** · feature-test-design **1.16.0** · entrada no step 7.
> Host: Codex em Windows/PowerShell · modelo exposto: GPT-6; identificador exato da implantação não informado; esforço ultra solicitado.
> **Revisão adversarial: PENDENTE — a sessão principal despachará um agente independente após esta entrega preliminar.**
> **02 ausente:** falta o inventário Superfície Livewire; não foi criado. Glossário ausente: vocabulário literal do 00.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Motivo |
|---|---|---|---|---|---|
| Dados de entrada | 2 | 3 | 6 | padrão | formulário integrado à gravação; valor monetário |
| Ciclo e alçada | 3 | 3 | 9 | completo | muitas condições, reentrada de estados, concorrência e autorização de dinheiro |
| Autorização e contexto | 3 | 3 | 9 | completo | identidade, organização e papéis combinados |
| E-mail | 3 | 3 | 9 | completo | efeito externo e destinatários de terceiros variáveis |
| Apresentação | 2 | 2 | 4 | padrão | duas superfícies de consulta, interpretação errada causa retrabalho |
| Cadastro de centro | 2 | 3 | 6 | padrão | CRUD integrado; o vínculo do gestor decide autoridade |

Perfis **decididos pelo passo 0**, sem perfil imposto. Impacto 3 em todas as áreas exceto apresentação. A adversarial cobre o conjunto inteiro. R16 cruza autorização somente nos cenários de R17, que herda completo. Técnicas: EP, BVA 3-valores na alçada (incremento 0,01), tabela de decisão, matriz papel × ação, matriz estado × operação, 2-switch e rastreio de efeito. Pairwise não se aplica: não há três parâmetros independentes de configuração no 00.

Cenários: 64 · Regras: 18 · Mutantes previstos: 67 · Sem matador: 0
Contagem obtida do arquivo gravado pelos quatro comandos `rg -c` equivalentes aos `grep -c` do template. O comando sem matador retornou exit 1 por zero correspondências, registrado como 0. CT-B são contados separadamente no 05: 2; uma tabela de Exemplos conta como um cenário.

## Autoridade e premissas de entrada

O 00 é uma wiki anterior ao formato com coluna Estado e P-nn. Tem 14 RQ e as premissas A-01…A-12. A rodada manda respeitar essas premissas **como dadas**, inclusive A-06, A-07 e A-09 apesar de frases históricas “pergunta em aberto”. Portanto não se reabre o cancelamento de rascunho, a rejeição pelo diretor ou a acumulação solicitante × gestor. Não há P-nn nessa entrada.

| Premissa vigente | Destino |
|---|---|
| A-01 | R1, R16, R18 — entidade CentroCusto e organização |
| A-02 | R4, R11 — um gestor por centro |
| A-03 | R5, R11, R12, R13, R17 — diretores da organização, primeira decisão resolve |
| A-04 | R5 — estritamente maior; literal e configuração efetiva |
| A-05 | R3, R9 — aprovada terminal |
| A-06 | R8, R9 — cancelar somente nas duas situações em trânsito |
| A-07 | R6, R11 — diretor também rejeita |
| A-08 | R16, R17 — administração do centro fora do usuário comum |
| A-09 | R10 — solicitante pode ser o gestor |
| A-10 | R4 — sem gestor o envio falha fechado |
| A-11 | R8, R13 — sem avisos adicionais |
| A-12 | R6, R7, R14, R15 — status e histórico no detalhe, quem/quando/justificativa |

## Varredura SFDIPOT

| Dimensão | O que foi varrido | Destino |
|---|---|---|
| Structure | solicitação, centro e histórico; enum planejado; resource, formulário e ação; policy/papel; notificação | R1–R18; inventário Livewire ausente declarado |
| Function | criar, corrigir, excluir, enviar, aprovar, rejeitar, cancelar, mostrar situação e autor; administração que muda o gestor | R1–R11, R14–R17 |
| Data | dinheiro textual decimal, descrição/justificativa Unicode, campos ausentes/nulos/vazios, referências reais e estrangeiras, autoria, histórico 0/1/N | R1, R2, R6, R13–R18; tetos de texto não dados no 00 |
| Interfaces | domínio direto, rotas do painel, componentes e modal com JS | todas as costuras abaixo; nenhum endpoint de escrita HTTP inventado |
| Platform | Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1; browser 5.0.1; mutate 5.0.2; SQLite de teste, fila e frontend | APIs confirmadas no vendor; concorrência pede conexões/processos compartilhando banco real |
| Operations | solicitante, gestor, diretor, administração, usuário comum, papéis acumulados; retry; consultas maiores que uma página | R10–R18 |
| Time | ordem gestor→diretor, retorno ao rascunho, instâncias antigas, duas decisões concorrentes e instantes do histórico | R3, R5, R7, R12, R15; sem SLA, expiração ou calendário no 00 |

## Matriz única — estado × operação

A matriz nasce dos cinco estados que o 00 determina (rascunho; as duas etapas de A-06; terminais de A-05 e Fora de Escopo), antes da separação em regras. O enum da compra ainda não existe nesta cópia: `rg ... app/Enums` devolveu “O sistema não pode encontrar o arquivo especificado”. Portanto a conferência mecânica contra o enum implementado é **pendente**, não uma prova já executada.

**5 estados × 8 operações = 40 células: 19 válidas e 21 inválidas**, contadas da tabela estruturada que gerou a matriz. Todas as 21 inválidas têm operação realmente executada e cenário próprio de seu verbo. Criar é operação anterior à existência do agregado, coberta em R1; removida é condição de inexistência, coberta em R3, sem inventar um sexto estado de enum.

✅ = operação executada com ator autorizado; a leitura afirma conteúdo do registro. ❌ = operação executada e recusada, conservando os efeitos nomeados na tabela de efeitos abaixo e os campos do Dado. O ID só cobre a linha de Exemplos correspondente à situação; listagem não herda evidência de detalhe.

| Situação | editar | excluir | enviar | aprovar | rejeitar | cancelar | listar | visualizar |
|---|---|---|---|---|---|---|---|---|
| rascunho | ✅ CT-05, CT-07 | ✅ CT-09 | ✅ CT-12 | ❌ CT-29 | ❌ CT-30 | ❌ CT-31 | ✅ CT-45 | ✅ CT-46 |
| aguardando_gestor | ❌ CT-26 | ❌ CT-27 | ❌ CT-28 | ✅ CT-15 | ✅ CT-18 | ✅ CT-24 | ✅ CT-45 | ✅ CT-46 |
| aguardando_diretor | ❌ CT-26 | ❌ CT-27 | ❌ CT-28 | ✅ CT-17 | ✅ CT-18 | ✅ CT-24 | ✅ CT-45 | ✅ CT-46 |
| aprovada | ❌ CT-26 | ❌ CT-27 | ❌ CT-28 | ❌ CT-29 | ❌ CT-30 | ❌ CT-31 | ✅ CT-45 | ✅ CT-46 |
| cancelada | ❌ CT-26 | ❌ CT-27 | ❌ CT-28 | ❌ CT-29 | ❌ CT-30 | ❌ CT-31 | ✅ CT-45 | ✅ CT-46 |

| Operação recusada | Não-efeitos obrigatórios auditados no cenário |
|---|---|
| editar | descrição, valor e centro não mudam; situação/histórico conservados; nenhum aviso de aprovação |
| excluir | solicitação permanece e decisões associadas permanecem; nenhum aviso |
| enviar | situação/histórico conservados; nenhum aviso para gestor ou diretores reais |
| aprovar | situação conservada; nenhuma nova decisão de aprovação; nenhum aviso da etapa seguinte |
| rejeitar | situação conservada; nenhuma decisão rejeitada nem alteração de justificativa anterior; nenhum aviso |
| cancelar | situação conservada; histórico conservado e nenhuma decisão nova; nenhum aviso |

A dimensão campo de editar percorre descrição, **valor e centro** fora do rascunho (CT-26). A dimensão persona é reaberta pelos quatro verbos do solicitante (CT-32) e pelos **dois** verbos do aprovador (CT-35); papéis acumulados são explícitos em CT-34.

### Decisão de autorização e de alçada

| Estado permite operação? | Identidade permite operação? | Decisão | Evidência |
|---|---|---|---|
| sim | sim | executa | células ✅, CT-34 |
| sim | não | recusa e conserva agregado/efeitos | CT-32, CT-35 |
| não | qualquer | recusa e conserva agregado/efeitos | seis verbos de R9 |

“Qualquer” colapsa a identidade somente onde o próprio estado torna o verbo proibido para todos (RQ-10/A-05; RQ-02/03; A-06). Nas situações válidas, a matriz de atores é completa para dono, gestor correto, gestor de outro centro, diretor antes da etapa, diretor da organização, ex-gestor e pessoa sem autoridade; cada verbo tem suas linhas em CT-35, CT-32 e CT-36.

| Etapa corrente | Valor efetivo | Decisão autorizada | Situação resultante | Evidência |
|---|---|---|---|---|
| gestor | 4999.99 com limite 5000.00 | aprovar | aprovada | CT-15 |
| gestor | 5000.00 com limite 5000.00 | aprovar | aprovada | CT-15 |
| gestor | 5000.01 com limite 5000.00 | aprovar | aguardando_diretor | CT-15 |
| gestor | qualquer valor válido | rejeitar com justificativa | rascunho | CT-18 |
| diretor | acima do limite | aprovar | aprovada | CT-17 |
| diretor | acima do limite | rejeitar com justificativa | rascunho | CT-18 |

## Mapa de Regras

| Regra | Área e perfil | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — A criação grava os dados da solicitação em rascunho | Dados de entrada (padrão) | RQ-01; A-01 | EP; rastreio da gravação | CT-01, CT-02, CT-03, CT-04 |
| R2 — A edição do rascunho conserva o que o solicitante corrigiu | Ciclo e alçada (completo) | RQ-02, RQ-09 | EP de campo; matriz estado × operação | CT-05, CT-06, CT-07, CT-08 |
| R3 — A exclusão do rascunho retira a solicitação das operações de escrita | Ciclo e alçada (completo) | RQ-03; A-05; fora de escopo de reabertura | estado × operação; EP de existência; idempotência no agregado | CT-09, CT-10, CT-11 |
| R4 — O envio do rascunho vai primeiro ao gestor do centro escolhido | Ciclo e alçada (completo) | RQ-04, RQ-05; A-02, A-10 | EP; tabela de decisão; rastreio do destinatário | CT-12, CT-13, CT-14 |
| R5 — A alçada literal exige o diretor estritamente acima de R$ 5.000 e depois do gestor | Ciclo e alçada (completo) | RQ-05, RQ-06; A-03, A-04 | BVA 3-valores (0,01); tabela de decisão | CT-15, CT-16, CT-17 |
| R6 — A rejeição de qualquer etapa exige uma justificativa existente e devolve ao rascunho | Ciclo e alçada (completo) | RQ-06, RQ-07, RQ-08; A-07, A-12 | EP; estado × evento; normalização de branco | CT-18, CT-19, CT-20, CT-B01, CT-B02 |
| R7 — Um novo envio reinicia a aprovação no gestor e conserva o histórico mostrado | Ciclo e alçada (completo) | RQ-09, RQ-12, RQ-13; A-12 | 2-switch; estado × evento; EP de origem | CT-21, CT-22, CT-23 |
| R8 — O solicitante cancela enquanto falta uma aprovação final | Ciclo e alçada (completo) | RQ-11; A-06, A-11 | estado × evento; rastreio do não-efeito | CT-24, CT-25 |
| R9 — Cada operação respeita a situação de partida e os estados terminais | Ciclo e alçada (completo) | RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-08, RQ-10, RQ-11; A-05, A-06 | produto cartesiano estado × operação; EP de campo | CT-26, CT-27, CT-28, CT-29, CT-30, CT-31 |
| R10 — Os verbos do solicitante verificam a identidade de quem chama | Autorização e contexto (completo) | RQ-01, RQ-02, RQ-03, RQ-04, RQ-09, RQ-11; A-09 | matriz papel × ação; tabela de decisão; pares de papéis | CT-32, CT-33, CT-34 |
| R11 — Aprovar e rejeitar verificam o aprovador da etapa corrente | Autorização e contexto (completo) | RQ-04, RQ-05, RQ-06, RQ-07; A-02, A-03, A-07 | matriz papel × ação; tabela de decisão completa | CT-35, CT-36, CT-37 |
| R12 — Cada intenção de transição resolve uma etapa uma única vez | Ciclo e alçada (completo) | RQ-04, RQ-05, RQ-06, RQ-08, RQ-11, RQ-13, RQ-14; A-03 | idempotência no agregado; concorrência; atomicidade da decisão | CT-38, CT-39, CT-40 |
| R13 — Os avisos usam e-mail e alcançam somente o próximo aprovador da organização | E-mail (completo) | RQ-14; A-02, A-03, A-11 | rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N | CT-41, CT-42, CT-43, CT-44 |
| R14 — A listagem e o detalhe mostram a situação atual de cada solicitação | Apresentação (padrão) | RQ-12; A-12 | EP exaustiva dos cinco estados; cardinalidade de listagem | CT-45, CT-46, CT-47 |
| R15 — O histórico mostra os autores das etapas e conserva os dados da decisão | Apresentação (padrão) | RQ-13; A-12 | EP de caminho; rastreio da exibição | CT-48, CT-49, CT-50 |
| R16 — A administração cadastra o centro e mantém o vínculo de um gestor | Cadastro de centro (padrão) | RQ-01, RQ-04; A-01, A-02, A-08 | EP de formulário; rastreio da gravação | CT-51, CT-52, CT-53, CT-54 |
| R17 — Usuário comum não administra centro de custo nem se nomeia gestor | Autorização e contexto (completo) | RQ-04; A-08 | matriz papel × ação; tabela de decisão; ação fora da UI | CT-55, CT-56, CT-57 |
| R18 — A organização e a autoria não podem ser trocadas por identificadores ou payload | Autorização e contexto (completo) | RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-13; A-01, A-03, A-08; convenção de organização | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | CT-58, CT-59, CT-60, CT-61, CT-62, CT-63, CT-64 |

Toda RQ do 00 aparece no mapa. Nenhuma RQ foi recebida com Estado aberta; as perguntas históricas vêm acompanhadas de premissa autorizada pela rodada. Não foram acrescentadas premissas comportamentais sobre limites desconhecidos.

## Costuras de Teste

Proposta da derivação: **Confirmada vazia para a sessão principal preencher antes do despacho adversarial**. O usuário está indisponível e autorizou a execução autônoma; não foi solicitada nova aprovação. Existente significa arnês e API existentes, não arquivo da feature já criado.

| Grupo | Regras | Costura | Existente ou nova | Por quê esta camada | Confirmada |
|---|---|---|---|---|---|
| Domínio da compra | R1–R13 | Pest feature HTTP | existente — tests/Feature ligado a TestCase; padrão de chamada direta em tests/Kit/ConviteUsuarioExistenteTest.php | banco, autorização e efeitos; não precisa de navegador | |
| Componentes da compra | R1, R2, R6, R10, R11, R14, R15 | componente Livewire/Filament | existente — Livewire::test e helpers Filament usados em tests/Kit/PaginasInfraTest.php | controles, gravação, ações e conteúdo de consulta | |
| Administração de centros | R16, R17 | componente Livewire/Filament | existente — mesmo arnês de formulário do painel | create/save e sua autorização real | |
| Autorização de administração | R16, R17 | Pest feature HTTP | existente — HTTP e escrita direta autenticada com TestCase | visitas e barreira por fora do componente | |
| Fronteira da organização | R11–R13, R17, R18 | Pest feature HTTP | nova pasta FeatureTenancy usando TenancyTestCase existente; testes de negócio não entram no grupo kit | contexto de team fixado antes das migrations; efeitos com destinatários reais | |
| Componentes com tenancy | R18 | componente Livewire/Filament | nova pasta FeatureTenancy com o mesmo TestCase; grupo distinto do kit | query de usuário com discriminante nulo | |
| Modal de rejeição com JS | R6 | browser | existente — tests/Browser ligado a TestCase e browser; arquivo de negócio novo | provar abertura e confirmação real da modal e erro visível com JS | |

**Pendência de arnês, não execução feita:** FeatureTenancy não existe, não está em tests/Pest.php e não é testsuite de phpunit.xml nesta cópia. Antes de materializar os CT de tenancy, ligar a nova pasta a TenancyTestCase + RefreshDatabase e registrá-la em phpunit.xml, sem grupo kit. Nada disso foi editado nesta rodada. Não alocar persistência/config/casts a Unit: tests/Unit não tem TestCase Laravel ligado.

## Fronteira com o Plano

O 01 foi lido integralmente por instrução da rodada, mas seus comportamentos e CT históricos não foram usados como oráculo. Foram utilizados nomes de classes/métodos apenas como endereço de execução, e routes/paths/UI para escolher a costura.

| Item do plano recusado | Por quê | Destino |
|---|---|---|
| IDs e ordem de CT antigos no PRD | não são cenários desta derivação | IDs novos do 04/05 |
| 255 para descrição, 120 para nome, mínimo 0.01 e tamanho decimal de coluna | números ausentes do 00; validar schema não confirma política de negócio | lacuna de teto/precisão descrita abaixo |
| cores gray/warning/success/danger, texto literal de erro ou sucesso | só o plano define essas escolhas | não usar como Então |
| gate “seis linhas com JS + duas personas ⇒ browser” do 01 | não é o gate desta versão da skill | browser somente para abertura/submissão JS da modal |
| logs, canais, índices, enum de banco, traits, fillable e algoritmo de UPDATE | escolhas internas, sem cláusula de auditoria/log no card | sem CT de log; mutantes são erros comportamentais |
| nome da notificação AprovacaoPendente e métodos enviar/aprovar/rejeitar/cancelar | nomes de integração, não promessa | endereço de materialização; Então afirma solicitação/etapa/canal/destinatário |
| URL do e-mail | o 00 pede e-mail, mas não determina presença ou destino de um link | lacuna: não criar promessa de link com base só no 01 |
| exclusão física no plano | mecanismo, não dispensa provar que removida não opera | CT-11 marcado @premissa de mecanismo; exclusão lógica alternativa não medida |

### Lacunas de especificação preservadas

- **Limites de texto e domínio numérico:** o 00 não dá n para descrição, nome de centro ou justificativa; não dá máximo monetário nem tratamento de três casas decimais, zero ou valor negativo. Não há oráculo para n/n+1 ou arredondamento na gravação. Foram cobertos presença, tipo monetário, referência, Unicode e a borda **literal conhecida** de alçada. Não foram inventados os tetos do PRD. A-12 pede instante no histórico, mas não define fuso/formato; o CT preserva o instante da decisão sem fixar uma conversão não acordada.
- **Inventário Livewire:** ausência do 02 impede enumerar cada método público, propriedade pública e consumo de filtros com valor inválido/tipo errado. Payload protegido e tenant nulo têm cenários, mas não substituem inventário por ponto. O acesso direto à tabela de histórico em CT-60 é uma sonda requerida: o executor precisa identificar o ponto real de leitura/escrita, sem criar rota fictícia ou filtrar o resultado no teste. Se o ponto não existir, registrar lacuna com a evidência; não atribuir cobertura da filha ao CT do pai.
- **Idempotência da criação:** o 00 não define chave de intenção nem contrato de deduplicação de duas criações com mesmo conteúdo. Não se afirma que duas compras iguais são uma só. Retry das transições, edição sem mudança e exclusão repetida têm agregado persistido como oráculo.
- **Zero diretores:** A-03 determina todos os existentes e primeiro a decidir, mas não diz o que fazer se houver zero diretor depois da aprovação do gestor. Não assumir avançar ou bloquear. Cardinalidade zero do gestor tem A-10 e CT-13; cardinalidades um/N de diretor têm CT-42. Zero diretor não prova não-efeito.
- **Atomicidade de e-mail após envio externo:** CT-40 prova falha depois da escrita de situação e rollback de estado/histórico, com destinatários reais. Não é usado para provar ausência de e-mail diante de falha **depois** do ponto de envio. O 00 não define política de e-mail enviado seguido de falha de commit; nenhuma transação de banco desfaz mensagem já entregue. A sonda de falha após envio/antes do commit e uma garantia outbox/after-commit ficam não medidas, sem algoritmo imposto.
- **Paginação com inserção entre páginas, desempate e ordenação inválida:** cardinalidades 0/1/limite/acima do limite são cobertas; o 00 não define ordem estável ou contrato de snapshot. Consumos públicos de coluna/filtro precisam do inventário ausente. Não alegar cobertura desses casos.
- **Superfícies inexistentes:** não há upload, webhook, importação, SLA, expiração ou configuração pairwise no requisito, e o Fora de Escopo exclui anexos. Não é dispensa de autorização/escopo/trava de uma superfície existente.

## Perguntas para o 00-requisito.md

**Nenhuma pergunta nova formalizada como cláusula vigente nesta derivação.** O 00 é imutável e as doze premissas foram dadas pela rodada. As lacunas acima são extensões não decididas; nenhuma recomendação foi aplicada como requisito de direção nova. O levantamento deverá voltar ao solicitante em outra rodada autorizada antes de cenários direcionais para teto/zero diretores/deduplicação/link/atomicidade externa. Não houve alteração do 00.

## Setup Global

### Pessoas, papéis e organização

Usar User::factory() e Tenant::factory(), existentes. Criar Sofia (solicitante, panel_user), Geraldo (gestor), Paula (outra usuária/gestora/diretora conforme cenário), Daniela (diretora), Rui (usuário sem autoridade), Ana (admin_organizacao). E-mails distintos e não vazios. Gestor é identidade de um centro; não criar papel gestor. Diretor pertence ao painel app e ao contexto indicado.

Helpers reais compartilhados: `noPainelDa()`, `usuarioComPapel()`, `papelNaOrganizacao()` e `fronteiraDeRequest()` em tests/Pest.php. Atribuir memberships e papéis no tenant correto; limpar relação roles ao trocar contexto, como o helper existente faz. Evitar master_global como único ator positivo: ele bypassa permissões. Cada cenário declara explicitamente a acumulação quando necessária; o padrão são pessoas distintas.

### Fixture de estado por transições reais

Ainda não existem factory, model ou enum da compra. Usar o ponto legítimo de criação (Model::create apenas para campos iniciais cuja validação vive nesse ponto, com os dados de servidor definidos pelo domínio), sem inventar factory/state. Centro com nome/gestor da organização criado legitimamente. Propor helper compartilhado **novo** `solicitacaoEm('{situacao}', [...])` em tests/Pest.php, sem implementá-lo nesta rodada:

| Estado pedido | Caminho real da fixture |
|---|---|
| rascunho | criação legítima em nome do solicitante |
| aguardando_gestor | criação em rascunho → enviar pelo solicitante |
| aguardando_diretor | criação com valor acima da alçada → enviar → aprovar pelo gestor |
| aprovada | criação → enviar → aprovar pelo gestor; se alta, aprovar também pelo diretor |
| cancelada | criação → enviar → cancelar pelo solicitante |
| rascunho depois de rejeição | caminho real até a etapa → rejeitar com justificativa |
| removida | criar rascunho → excluir legitimamente; guardar uma instância antes da exclusão |

**Não gravar situacao à força.** Histórico pertence às transições reais. A única fixture corrupta é a referência estrangeira preparada para a partição de uso em CT-61; ela é declarada como corrupção de dado, não caminho feliz. Instantes conhecidos podem ser fixados via viagem de tempo com restauração/closure.

Cada teste parte de uma fixture nova. Montar fixtures **antes** da janela de captura dos e-mails/assertions de delta; registrar conjunto anterior de decisões e destinatários. Assim os avisos legítimos da preparação não são confundidos com efeitos da ação em teste.

### Banco e falhas

RefreshDatabase é ligado a Feature, Kit, Tenancy e Browser no arnês existente; phpunit.xml usa SQLite :memory:. A pasta FeatureTenancy proposta usa o mesmo TenancyTestCase existente, que decide o modo antes das migrations. Cenário de concorrência exige banco temporário compartilhado e duas conexões/processos com barreira real: preferir banco do driver de produção em ambiente de teste isolado. **Duas chamadas sequenciais não são a prova de concorrência.** Nenhum banco, teste ou comando Artisan foi executado.

Em CT-40, o executor escolhe uma falha determinística de persistência depois da escrita de estado (constraint ou gancho de model na gravação da etapa). Se não conseguir posicionar a falha nesse ponto, declarar o experimento tentado e a lacuna; não substituí-la por pré-validação. Não construir fixture de estado reimplementando a máquina no teste.

### Fakes e APIs confirmadas

Notification::fake() depois da fixture e antes da ação medida. A callback de NotificationFake recebe notificação, canais e destinatário; exigir canal mail, solicitação/etapa certas, contagem global e por destinatário. `assertSentToTimes()`, `assertCount()`, `assertNothingSent()` e `assertSentTo()` foram confirmados em vendor. Fake prova despacho e canal; não prova entrega SMTP ou worker real.

Livewire::test(), fillForm(), call('create'), call('save'), assertHasFormErrors(), assertSchemaStateSet(), callAction(TestAction::make('nome')->table($registro)) e assertActionHidden() são APIs presentes. Não usar assertFormSet/callTableAction/assertTableActionExists depreciados. Na escrita por componente: autenticar antes, selecionar painel/contexto, gravar e consultar novamente o banco com campos concretos; edição usa save.

Confirmações locais: `vendor/filament/forms/.stubs.php:fillForm():8`; `vendor/filament/actions/.stubs.php:callAction():24`; `vendor/filament/actions/.stubs.php:assertActionHidden():34`; `vendor/filament/schemas/.stubs.php:assertSchemaStateSet():19`; `vendor/laravel/framework/src/Illuminate/Support/Testing/Fakes/NotificationFake.php:assertSentTo():67`; `vendor/laravel/framework/src/Illuminate/Support/Testing/Fakes/NotificationFake.php:assertSentToTimes():115`. Versões confirmadas também em vendor/composer/installed.json, além de composer.lock.

Mutate está instalado em vendor, **não declarado diretamente** em composer.json: pendência para o projeto consumidor antes da medição. Mutation testing e testes Pest não foram executados; esta entrega é especificação. Nenhum score, DDR, token economizado ou equivalência de hosts foi declarado.

Fechamento pós-implementação planejado: primeiro executar os CT materializados; depois medir `pest --mutate --covered-only --path={escopo efetivo da feature}` pelo lançador `.ai/skills/feature-wiki/scripts/pestw.cmd` no Windows, com driver de cobertura pronto. Exigir duração plausível e lista de sobreviventes antes de aceitar score; cada sobrevivente volta a uma lacuna de derivação e um cenário/asserção que o mata. Não rodar o lançador Unix diretamente e tomar resultado instantâneo como medição. Escopo, covers(), driver, sobreviventes e duração continuam não medidos, por não haver implementação autorizada.

### Teto, poda e escolhas

R1 tem quatro cenários em padrão para conciliar visita, gravação de componente, gravação direta e validação externa. R16 tem quatro em padrão porque create e edit exigem visita **e** gravação. R9 tem seis esquemas em completo para executar os seis verbos e cobrir todas as 21 células inválidas. R18 tem sete cenários em completo porque IDOR é por tabela, além de referência estrangeira, mass assignment, tenant nulo e saída do erro. São estouros justificados por gates, não repetição do mesmo observável. R6 tem três CT e dois CT-B, dentro do teto completo.

| Cogitado | Cortado porque |
|---|---|
| fluxo inteiro repetido no browser por duas ou três personas | estado, autoria e destinatário são provados no domínio/componente; o browser fica na execução JS da modal |
| browser para cada badge/ação oculta/formulário que salva | CT-45, CT-46, CT-03, CT-07, CT-33 e CT-37 já falsificam esses observáveis |
| dark mode, screenshots de cor e acessibilidade sem cláusula | não há obrigação visual correspondente no 00; nenhuma medição disso é reivindicada |
| log por transição | não há RQ de trilha de log; a exibição de histórico tem sua regra própria |
| testes de alçada só como predicado Unit | o requisito afirma a transição persistida e o próximo aprovador; usar somente um predicado imaginado perderia o comportamento real |


## Regra R1 — A criação grava os dados da solicitação em rascunho

Origem: RQ-01; A-01. Área: Dados de entrada (padrão). Técnica: EP; rastreio da gravação. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A criação grava os dados da solicitação em rascunho

    Cenário: [CT-01] A criação conserva descrição, valor e centro escolhidos
      Dado a solicitante Sofia, o gestor Geraldo e a diretora Daniela são pessoas distintas da organização Acme, e ainda não existe a solicitação
      E o centro Operações de Acme pertence a Geraldo e os dados são descrição “Compra de ação 🔧”, valor decimal textual “1299.99” e esse centro
      Quando Sofia cria a solicitação pelo ponto de escrita do domínio, sem componente
      Então existe exatamente uma solicitação de Sofia em rascunho em Acme, com descrição “Compra de ação 🔧”, valor “1299.99” e o ID do centro Operações
      E existem zero decisões de aprovação e zero e-mails de aprovação enviados a Geraldo ou Daniela

    Esquema do Cenário: [CT-02] Um campo obrigatório inválido impede a criação fora da UI
      Dado Sofia de Acme ainda não tem a solicitação e Geraldo e Daniela são destinatários reais disponíveis
      E descrição “Notebook”, valor “1299.99” e centro Operações são válidos, exceto o único <campo> com <entrada>
      Quando Sofia tenta criar a solicitação pelo ponto de escrita do domínio, sem componente
      Então a criação é recusada para <campo> e permanecem zero solicitações, zero decisões de aprovação e zero e-mails de aprovação

      Exemplos:
        | campo | entrada | # partição |
        | descricao | ausente | obrigatória ausente |
        | descricao | null | obrigatória nula |
        | descricao | string vazia | obrigatória vazia |
        | descricao | três espaços | sem descrição |
        | valor | ausente | obrigatório ausente |
        | valor | null | obrigatório nulo |
        | valor | string vazia | obrigatório vazio |
        | valor | texto abc | não monetário |
        | centro_custo_id | ausente | obrigatório ausente |
        | centro_custo_id | null | obrigatório nulo |
        | centro_custo_id | ID inexistente | referência inexistente |

    Cenário: [CT-03] O formulário de criação grava os três campos do solicitante
      Dado Sofia é panel_user em Acme, não existe a solicitação e o centro Operações tem o gestor Geraldo
      Quando Sofia salva pelo componente create a descrição “Notebook”, o valor “1299.99” e o centro Operações
      Então a consulta nova ao banco encontra uma solicitação em rascunho de Sofia em Acme, com exatamente “Notebook”, “1299.99” e o centro Operações
      E há zero decisões de aprovação e zero e-mails de aprovação

    Cenário: [CT-04] A rota de criação oferece os três dados obrigatórios
      Dado Sofia é panel_user em Acme e ainda não existe a solicitação
      Quando Sofia visita a rota create de solicitação autenticada
      Então a resposta permite a criação e contém os controles de descrição, valor e escolha do centro de custo, sem valor, descrição ou centro previamente pertencentes a outra solicitação
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Validar obrigatoriedade só no formulário | CT-02 | cada linha inválida mantém zero solicitações após a escrita direta |
| M-02 | Gravar o valor ou o centro de um default em vez do que Sofia informou | CT-01, CT-03 | valor persistido “1299.99” e centro Operações, iguais aos enviados |
| M-03 | O componente renderiza corretamente mas não persiste os dados enviados | CT-03 | uma nova consulta encontra os três campos e Sofia como solicitante |
| M-04 | A página create omite um dos campos pedidos | CT-04 | os três controles de descrição, valor e centro aparecem no conteúdo da rota |

## Regra R2 — A edição do rascunho conserva o que o solicitante corrigiu

Origem: RQ-02, RQ-09. Área: Ciclo e alçada (completo). Técnica: EP de campo; matriz estado × operação. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A edição do rascunho conserva o que o solicitante corrigiu

    Esquema do Cenário: [CT-05] O solicitante corrige cada campo decisivo em rascunho
      Dado a solicitação de Sofia está em rascunho em Acme, com descrição “Notebook”, valor “8000.01” e centro Operações de Geraldo
      E o centro Projetos com a gestora Paula existe em Acme, e Daniela é diretora
      Quando Sofia grava pelo domínio somente <campo> com <novo>
      Então a nova consulta encontra <campo> igual a <novo>, os demais campos iguais ao Dado e a situação rascunho
      E o histórico de decisões continua vazio e não há e-mail de aprovação para Geraldo, Paula ou Daniela

      Exemplos:
        | campo | novo | # partição |
        | descricao | Monitor de ação 🔧 | texto |
        | valor | 4999.99 | campo que muda a alçada |
        | centro_custo_id | ID do centro Projetos | campo que muda o gestor |
        | descricao | Notebook | edição sem alteração |

    Esquema do Cenário: [CT-06] A obrigatoriedade também é aplicada na correção do rascunho
      Dado a solicitação de Sofia está em rascunho com descrição “Notebook”, valor “1299.99” e centro Operações, com Geraldo e Daniela reais
      Quando Sofia tenta alterar pelo domínio somente <campo> para <entrada>
      Então a escrita é recusada e descrição “Notebook”, valor “1299.99”, centro Operações e situação rascunho permanecem gravados
      E o histórico continua vazio e nenhum e-mail de aprovação é enviado

      Exemplos:
        | campo | entrada | # partição |
        | descricao | string vazia | descrição ausente na edição |
        | valor | null | valor ausente na edição |
        | valor | abc | valor não monetário na edição |
        | centro_custo_id | ID inexistente | centro inexistente na edição |

    Cenário: [CT-07] O formulário edit grava a correção do dono do rascunho
      Dado a solicitação de Sofia está em rascunho com descrição “Notebook”, valor “8000.01” e centro Operações
      E o centro Projetos da gestora Paula existe em Acme
      Quando Sofia salva pelo componente edit descrição “Monitor”, valor “4999.99” e centro Projetos
      Então a nova consulta encontra “Monitor”, “4999.99” e o centro Projetos na mesma solicitação de Sofia em rascunho

    Cenário: [CT-08] A rota edit carrega os dados do rascunho certo
      Dado a solicitação de Sofia está em rascunho com descrição “Notebook”, valor “1299.99” e centro Operações
      Quando Sofia visita a rota edit desse registro autenticada
      Então a resposta contém os controles preenchidos com “Notebook”, “1299.99” e o centro Operações dessa solicitação
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-05 | A edição aceita valor ou referência inválida porque a validação só roda na criação | CT-06 | os campos persistidos continuam exatamente os do Dado |
| M-06 | A edição muda a descrição mas ignora valor ou centro de custo | CT-05, CT-07 | valor “4999.99” e centro Projetos são encontrados no banco |
| M-07 | O componente edit chama a operação de criação ou não salva a correção | CT-07 | o mesmo ID conserva Sofia e passa a ter os três dados corrigidos |
| M-08 | O binding de edit carrega dados de outro registro | CT-08 | os controles têm os três valores concretos do registro de Sofia |

## Regra R3 — A exclusão do rascunho retira a solicitação das operações de escrita

Origem: RQ-03; A-05; fora de escopo de reabertura. Área: Ciclo e alçada (completo). Técnica: estado × operação; EP de existência; idempotência no agregado. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A exclusão do rascunho retira a solicitação das operações de escrita

    Cenário: [CT-09] O solicitante exclui seu rascunho
      Dado a solicitação de Sofia está em rascunho em Acme, com o gestor Geraldo e a diretora Daniela disponíveis
      Quando Sofia exclui o rascunho pelo ponto de escrita do domínio
      Então a solicitação não existe mais entre as solicitações utilizáveis e não permanece decisão de aprovação associada
      E nenhum e-mail de aprovação é enviado a Geraldo ou Daniela

    Cenário: [CT-10] A repetição da exclusão não ressuscita nem afeta outra compra
      Dado Sofia já excluiu pelo domínio a solicitação que estava em rascunho, e outra solicitação de Paula em rascunho permanece gravada em Acme
      E Geraldo e Daniela existem como destinatários de aprovação
      Quando Sofia repete a exclusão do mesmo identificador removido
      Então a primeira solicitação continua inutilizável, a solicitação de Paula mantém todos os campos e não surge decisão de aprovação ou e-mail para Geraldo ou Daniela

    @premissa-exclusao-fisica
    Esquema do Cenário: [CT-11] Uma instância carregada antes da exclusão não continua operando
      Dado Sofia carregou uma solicitação em rascunho de valor “8000.01” e depois a excluiu pelo domínio, mantendo a instância antiga em memória
      E Sofia também é gestora e diretora para isolar a ausência do registro, e Paula e Daniela existem como próximos destinatários possíveis
      Quando Sofia tenta <operacao> nessa instância removida pelo domínio
      Então a operação é recusada e a solicitação não reaparece, não muda a solicitação de Paula e não cria decisão de aprovação
      E nenhum e-mail de aprovação é enviado a Paula ou Daniela

      Exemplos:
        | operacao | # partição |
        | editar o valor para 4999.99 | removida × editar |
        | excluir | removida × excluir |
        | enviar | removida × enviar |
        | aprovar | removida × aprovar |
        | rejeitar com justificativa Sem verba | removida × rejeitar |
        | cancelar | removida × cancelar |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-09 | Excluir só muda a aparência da listagem e deixa a compra utilizável | CT-09, CT-11 | a compra removida não pode operar nem reaparecer |
| M-10 | A segunda exclusão usa um identificador substituto ou atinge a próxima solicitação | CT-10 | a solicitação de Paula e todos seus campos permanecem iguais |
| M-11 | A transição aceita a instância antiga e grava uma etapa depois de zero linhas atualizadas | CT-11 | zero decisões e zero e-mails após a operação na compra removida |

## Regra R4 — O envio do rascunho vai primeiro ao gestor do centro escolhido

Origem: RQ-04, RQ-05; A-02, A-10. Área: Ciclo e alçada (completo). Técnica: EP; tabela de decisão; rastreio do destinatário. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O envio do rascunho vai primeiro ao gestor do centro escolhido

    Esquema do Cenário: [CT-12] Qualquer alçada começa pelo gestor do próprio centro
      Dado a solicitação de Sofia está em rascunho em Acme, no centro Operações de Geraldo, com valor <valor>
      E Paula gere outro centro e Daniela é diretora de Acme, todos com e-mail
      Quando Sofia envia pelo domínio a solicitação
      Então a situação persistida é aguardando_gestor, o histórico de decisões continua vazio e Geraldo recebe um e-mail de aprovação dessa solicitação
      E Paula e Daniela recebem zero e-mails de aprovação desse envio

      Exemplos:
        | valor | # partição |
        | 4999.99 | abaixo da alçada |
        | 5000.00 | na alçada |
        | 5000.01 | acima da alçada |

    Cenário: [CT-13] O centro sem gestor impede o envio e conserva o rascunho
      Dado a solicitação de Sofia está em rascunho no centro Sem gestor de Acme, cujo gestor é null
      E Paula gere outro centro e Daniela é diretora de Acme, ambas disponíveis e com e-mail
      Quando Sofia tenta enviar a solicitação pelo domínio
      Então o envio é recusado, a situação gravada permanece rascunho e não há decisão de aprovação
      E zero e-mails de aprovação são enviados a Paula e Daniela, sem usar outra pessoa como substituta

    Cenário: [CT-14] A correção do centro muda quem recebe a solicitação enviada
      Dado Sofia criou a solicitação em rascunho no centro Operações de Geraldo e a corrigiu em rascunho para o centro Projetos de Paula
      E Geraldo, Paula e a diretora Daniela existem em Acme com e-mail
      Quando Sofia envia pelo domínio a solicitação corrigida
      Então a situação gravada é aguardando_gestor com centro Projetos, Paula recebe exatamente um e-mail de aprovação e Geraldo e Daniela recebem zero
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-12 | Uma compra alta começa na etapa de diretor ou já nasce aprovada | CT-12 | “5000.01” fica aguardando_gestor sem decisão de diretor |
| M-13 | Centro sem gestor usa o gestor de outro centro ou pula a etapa | CT-13 | rascunho permanece e Paula/Daniela não recebem e-mail |
| M-14 | O envio usa o gestor do centro anterior à correção | CT-14 | somente Paula recebe o e-mail, com centro Projetos persistido |

## Regra R5 — A alçada literal exige o diretor estritamente acima de R$ 5.000 e depois do gestor

Origem: RQ-05, RQ-06; A-03, A-04. Área: Ciclo e alçada (completo). Técnica: BVA 3-valores (0,01); tabela de decisão. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A alçada literal exige o diretor estritamente acima de R$ 5.000 e depois do gestor

    Esquema do Cenário: [CT-15] O centavo em torno de cinco mil determina a próxima etapa
      Dado a configuração efetiva lida da aplicação para a alçada é o decimal “5000.00”, sem substituir o limite em config durante este cenário
      E a solicitação de Sofia está aguardando_gestor, com valor <valor>, centro de Geraldo e Daniela diretora real em Acme
      Quando Geraldo aprova pelo domínio a etapa de gestor
      Então o banco contém situação <destino>, uma decisão aprovada de gestor por Geraldo e zero decisões de diretor
      E Daniela recebe <emails_diretora> e-mails de aprovação

      Exemplos:
        | valor | destino | emails_diretora | # borda |
        | 4999.99 | aprovada | 0 | borda−0,01 |
        | 5000.00 | aprovada | 0 | borda |
        | 5000.01 | aguardando_diretor | 1 | borda+0,01 |

    Cenário: [CT-16] A mudança explícita da alçada é usada na decisão
      Dado o limite efetivo foi configurado para o decimal “7000.00”, e a solicitação de Sofia está aguardando_gestor com valor “6000.01”
      E Geraldo é o gestor do centro e Daniela é diretora real de Acme
      Quando Geraldo aprova a solicitação pelo domínio
      Então a situação persistida é aprovada, há uma decisão de gestor por Geraldo e zero decisões de diretor e zero e-mails de aprovação para Daniela

    Cenário: [CT-17] A decisão do diretor encerra a compra alta depois da decisão do gestor
      Dado a solicitação de Sofia de valor “8000.01” está aguardando_diretor após o envio e a aprovação real de Geraldo, com uma decisão de gestor já gravada
      E Daniela tem o papel diretor em Acme e Paula é outra diretora real
      Quando Daniela aprova pelo domínio a etapa pendente de diretor
      Então a situação persistida é aprovada e o histórico contém exatamente gestor aprovado por Geraldo e diretor aprovado por Daniela
      E nenhum e-mail de aprovação é enviado a Sofia, Geraldo, Daniela ou Paula
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-15 | Usar >= no limite | CT-15 | “5000.00” termina aprovada, com zero decisões de diretor |
| M-16 | Arredondar ou truncar o valor antes de comparar e perder o centavo | CT-15 | “5000.01” fica aguardando_diretor, não aprovada |
| M-17 | Fixar 5000 no código e ignorar a configuração acordada | CT-16 | “6000.01” com limite “7000.00” termina aprovada |
| M-18 | Dar aprovação final do gestor a uma compra alta ou exigir gestor novamente depois do diretor | CT-15, CT-17 | compra alta tem aguardando_diretor após gestor e duas decisões corretas ao final |

## Regra R6 — A rejeição de qualquer etapa exige uma justificativa existente e devolve ao rascunho

Origem: RQ-06, RQ-07, RQ-08; A-07, A-12. Área: Ciclo e alçada (completo). Técnica: EP; estado × evento; normalização de branco. CT-B01 e CT-B02 estão no 05; provam a abertura/submissão real com JavaScript e a exibição do erro. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A rejeição de qualquer etapa exige uma justificativa existente e devolve ao rascunho

    Esquema do Cenário: [CT-18] Gestor e diretor rejeitam com uma justificativa curta ou Unicode
      Dado a solicitação de Sofia está <origem> por transições reais, com Geraldo gestor e Daniela diretora real em Acme
      E <ator> é quem decide essa etapa, e há <historico_antes> decisões anteriores
      Quando <ator> rejeita pelo domínio com a justificativa <texto>
      Então a situação persistida é rascunho, as decisões anteriores permanecem e há uma nova decisão rejeitada da etapa corrente, por <ator>, com a justificativa <texto>
      E zero e-mails de aprovação são enviados a Sofia, Geraldo ou Daniela

      Exemplos:
        | origem | ator | historico_antes | texto | # partição |
        | aguardando_gestor | Geraldo | 0 | Sem verba | gestor; curta |
        | aguardando_diretor | Daniela | 1 | Sem verba | diretor; curta |
        | aguardando_gestor | Geraldo | 0 | Não há orçamento 🔧 | Unicode |

    Esquema do Cenário: [CT-19] A escrita direta recusa cada forma de justificativa ausente
      Dado a solicitação de Sofia está <origem> com Geraldo gestor e Daniela diretora real e com o histórico anterior dessa situação guardado
      Quando o aprovador correto tenta rejeitar pelo domínio com justificativa <entrada>
      Então a rejeição é recusada e a situação persistida continua <origem>, com o mesmo conjunto de decisões e justificativas anteriores
      E nenhum e-mail de aprovação é enviado a Sofia, Geraldo ou Daniela

      Exemplos:
        | origem | entrada | # partição |
        | aguardando_gestor | string vazia | vazia; gestor |
        | aguardando_gestor | três espaços | branco; gestor |
        | aguardando_gestor | null | nula; gestor |
        | aguardando_gestor | ausente | ausente; gestor |
        | aguardando_diretor | string vazia | vazia; diretor |
        | aguardando_diretor | três espaços | branco; diretor |
        | aguardando_diretor | null | nula; diretor |
        | aguardando_diretor | ausente | ausente; diretor |

    Cenário: [CT-20] O componente recusa a rejeição sem justificativa e conserva a etapa
      Dado a solicitação de Sofia está aguardando_gestor, Geraldo é o gestor e Daniela é diretora real em Acme
      Quando Geraldo dispara a ação rejeitar pelo componente com justificativa vazia
      Então o campo justificativa tem erro de obrigatoriedade, a situação gravada continua aguardando_gestor e o histórico continua vazio
      E zero e-mails de aprovação são enviados a Sofia, Geraldo ou Daniela
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-19 | Checar somente string vazia e aceitar texto composto só por espaços | CT-19 | linhas “três espaços” mantêm situação e histórico anteriores |
| M-20 | Validar a justificativa somente na modal | CT-19 | a chamada direta recusa justificativa ausente sem nova decisão |
| M-21 | Devolver para rejeitada ou aguardar diretor depois da rejeição | CT-18 | as duas etapas voltam ao valor persistido rascunho |
| M-22 | Exigir um tamanho mínimo não pedido para justificativa ou descartar Unicode | CT-18 | “Sem verba” e “Não há orçamento 🔧” são gravados integralmente |
| M-23 | A modal omite a regra de obrigatoriedade e permite confirmar o campo vazio | CT-20 | o campo justificativa apresenta erro e a compra continua aguardando_gestor sem decisão |

## Regra R7 — Um novo envio reinicia a aprovação no gestor e conserva o histórico mostrado

Origem: RQ-09, RQ-12, RQ-13; A-12. Área: Ciclo e alçada (completo). Técnica: 2-switch; estado × evento; EP de origem. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Um novo envio reinicia a aprovação no gestor e conserva o histórico mostrado

    Esquema do Cenário: [CT-21] A rejeição nas duas etapas reinicia o envio no gestor
      Dado a solicitação de Sofia de “8000.01” voltou a rascunho pela rejeição real em <etapa_anterior>, e o histórico anterior tem <decisoes> decisões com autores identificados
      E Geraldo é gestor, Daniela é diretora real, e a captura de e-mails começou depois da fixture do ciclo anterior
      Quando Sofia envia novamente pelo domínio a solicitação em rascunho
      Então a situação gravada é aguardando_gestor e as <decisoes> decisões do ciclo anterior conservam autores, etapas e justificativas
      E Geraldo recebe exatamente um e-mail de aprovação do reenvio e Daniela recebe zero

      Exemplos:
        | etapa_anterior | decisoes | # partição |
        | gestor | 1 | ciclo após rejeição do gestor |
        | diretor | 2 | ciclo após rejeição do diretor |

    Cenário: [CT-22] A correção depois da rejeição altera a alçada do novo ciclo
      Dado a solicitação de Sofia de “8000.01” foi aprovada por Geraldo e rejeitada por Daniela, voltou a rascunho, foi corrigida para “4999.99” e enviada de novo, estando aguardando_gestor
      E as duas decisões anteriores continuam identificadas e Geraldo e Daniela são pessoas reais distintas
      Quando Geraldo aprova pelo domínio a etapa de gestor do novo ciclo
      Então a situação gravada é aprovada com valor “4999.99”, as duas decisões anteriores permanecem e existe uma terceira decisão aprovada de gestor por Geraldo
      E zero decisões novas de diretor e zero e-mails de aprovação para Daniela são criados

    Cenário: [CT-23] O novo ciclo não conserva autoridade do centro anterior
      Dado a solicitação de Sofia foi rejeitada por Geraldo, voltou a rascunho, mudou do centro Operações para Projetos de Paula e foi reenviada, estando aguardando_gestor
      E a decisão rejeitada por Geraldo permanece e Daniela é diretora real em Acme
      Quando Geraldo tenta aprovar pelo domínio a solicitação do novo ciclo
      Então a operação é recusada e a situação continua aguardando_gestor no centro Projetos, com somente a decisão rejeitada anterior por Geraldo
      E zero e-mails de aprovação são enviados a Paula ou Daniela pela tentativa
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-24 | Reenvio após rejeição do diretor volta direto para o diretor | CT-21 | origem diretor retorna aguardando_gestor e avisa Geraldo |
| M-25 | Usar o valor ou a aprovação de gestor do ciclo anterior para decidir o novo ciclo | CT-22 | valor corrigido “4999.99” encerra com uma nova decisão de gestor |
| M-26 | Apagar ou sobrescrever as decisões antigas no reenvio | CT-21, CT-22 | autores e decisões anteriores permanecem, com nova decisão acrescentada |
| M-27 | Permitir que o gestor anterior aprove depois da troca de centro | CT-23 | Geraldo é recusado; centro Projetos e histórico anterior ficam iguais |

## Regra R8 — O solicitante cancela enquanto falta uma aprovação final

Origem: RQ-11; A-06, A-11. Área: Ciclo e alçada (completo). Técnica: estado × evento; rastreio do não-efeito. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O solicitante cancela enquanto falta uma aprovação final

    Esquema do Cenário: [CT-24] O cancelamento vale antes da decisão do gestor ou do diretor
      Dado a solicitação de Sofia está <origem> por transições reais e tem <decisoes> decisões anteriores
      E Geraldo é gestor e Daniela e Paula são diretoras reais em Acme
      Quando Sofia cancela pelo domínio a solicitação
      Então a situação persistida é cancelada e as <decisoes> decisões anteriores ficam iguais, sem nova decisão de aprovação
      E zero e-mails de aprovação são enviados a Sofia, Geraldo, Daniela ou Paula

      Exemplos:
        | origem | decisoes | # partição |
        | aguardando_gestor | 0 | antes do gestor |
        | aguardando_diretor | 1 | antes do diretor |

    Cenário: [CT-25] A repetição do cancelamento mantém o agregado cancelado
      Dado Sofia cancelou pelo domínio uma solicitação que aguardava diretor após uma decisão de gestor por Geraldo
      E Daniela e Paula são diretoras reais em Acme e o histórico de partida contém somente aquela decisão de Geraldo
      Quando Sofia repete o mesmo cancelamento pelo domínio
      Então a situação gravada permanece cancelada com somente a decisão anterior de Geraldo, sem novo registro de decisão e sem e-mail para Sofia, Geraldo, Daniela ou Paula
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-28 | Permitir cancelar somente aguardando gestor e esquecer a etapa de diretor | CT-24 | linha aguardando_diretor termina cancelada |
| M-29 | Tratar cancelamento como rejeição e voltar ao rascunho | CT-24 | situação gravada é cancelada e não nasce decisão rejeitada |
| M-30 | O retry cria uma decisão ou avisa o aprovador novamente | CT-25 | agregado conserva uma decisão antiga e zero novos e-mails |

## Regra R9 — Cada operação respeita a situação de partida e os estados terminais

Origem: RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-08, RQ-10, RQ-11; A-05, A-06. Área: Ciclo e alçada (completo). Técnica: produto cartesiano estado × operação; EP de campo. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Cada operação respeita a situação de partida e os estados terminais

    Esquema do Cenário: [CT-26] A operação editar não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta editar somente <campo> para <novo> pelo domínio
      Então a operação é recusada e os campos descrição “Notebook”, valor “8000.01” e centro Operações continuam exatamente gravados, com a mesma situação e o mesmo histórico; não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | campo | novo | # partição |
        | aguardando_gestor | descricao | Monitor | aguardando_gestor × descrição |
        | aguardando_gestor | valor | 4999.99 | aguardando_gestor × alçada |
        | aguardando_gestor | centro_custo_id | ID do centro Projetos | aguardando_gestor × gestor |
        | aguardando_diretor | descricao | Monitor | aguardando_diretor × descrição |
        | aguardando_diretor | valor | 4999.99 | aguardando_diretor × alçada |
        | aguardando_diretor | centro_custo_id | ID do centro Projetos | aguardando_diretor × gestor |
        | aprovada | descricao | Monitor | aprovada × descrição |
        | aprovada | valor | 4999.99 | aprovada × alçada |
        | aprovada | centro_custo_id | ID do centro Projetos | aprovada × gestor |
        | cancelada | descricao | Monitor | cancelada × descrição |
        | cancelada | valor | 4999.99 | cancelada × alçada |
        | cancelada | centro_custo_id | ID do centro Projetos | cancelada × gestor |

    Esquema do Cenário: [CT-27] A operação excluir não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta excluir a solicitação pelo domínio
      Então a operação é recusada e o registro continua existindo com a mesma situação, descrição “Notebook”, valor “8000.01”, centro Operações e todas as decisões anteriores; não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | # partição |
        | aguardando_gestor | aguardando_gestor × excluir |
        | aguardando_diretor | aguardando_diretor × excluir |
        | aprovada | aprovada × excluir |
        | cancelada | cancelada × excluir |

    Esquema do Cenário: [CT-28] A operação enviar não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta enviar a solicitação pelo domínio
      Então a operação é recusada e a situação persistida e todas as decisões anteriores permanecem iguais, e não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | # partição |
        | aguardando_gestor | aguardando_gestor × enviar |
        | aguardando_diretor | aguardando_diretor × enviar |
        | aprovada | aprovada × enviar |
        | cancelada | cancelada × enviar |

    Esquema do Cenário: [CT-29] A operação aprovar não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta aprovar a solicitação pelo domínio
      Então a operação é recusada e a situação persistida permanece <origem>, as decisões anteriores ficam iguais, zero decisões de aprovação são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | # partição |
        | rascunho | rascunho × aprovar |
        | aprovada | aprovada × aprovar |
        | cancelada | cancelada × aprovar |

    Esquema do Cenário: [CT-30] A operação rejeitar não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta rejeitar com justificativa “Sem verba” pelo domínio
      Então a operação é recusada e a situação persistida permanece <origem>, as decisões e justificativas anteriores ficam iguais, zero decisões rejeitadas são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | # partição |
        | rascunho | rascunho × rejeitar |
        | aprovada | aprovada × rejeitar |
        | cancelada | cancelada × rejeitar |

    Esquema do Cenário: [CT-31] A operação cancelar não atua nos estados em que é proibida
      Dado a solicitação está <origem> por transições reais, com descrição “Notebook”, valor “8000.01” e centro Operações; o histórico anterior foi guardado
      E Sofia é solicitante, gestora e diretora para isolar a situação; Geraldo, Paula e Daniela são destinatários reais, e o centro Projetos existe em Acme
      Quando Sofia tenta cancelar a solicitação pelo domínio
      Então a operação é recusada e a situação persistida permanece <origem>, as decisões anteriores ficam iguais, zero decisões são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | # partição |
        | rascunho | rascunho × cancelar |
        | aprovada | aprovada × cancelar |
        | cancelada | cancelada × cancelar |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-31 | Autorizar editar ou excluir por identidade sem conferir rascunho | CT-26, CT-27 | em trânsito e nos terminais os três campos e a existência continuam iguais |
| M-32 | A conferência de estado existe em aprovar mas não em rejeitar ou enviar | CT-29, CT-30, CT-28 | cada verbo é chamado e não altera estado, histórico ou e-mails |
| M-33 | Tratar cancelada como estado de reabertura ou permitir cancelar rascunho | CT-31, CT-28, CT-26 | cancelada continua cancelada; rascunho não é cancelado conforme A-06 |
| M-34 | A recusa vem depois de gravar a decisão ou disparar e-mail | CT-29, CT-30, CT-28 | zero novas decisões e zero e-mails, com destinatários reais no Dado |

## Regra R10 — Os verbos do solicitante verificam a identidade de quem chama

Origem: RQ-01, RQ-02, RQ-03, RQ-04, RQ-09, RQ-11; A-09. Área: Autorização e contexto (completo). Técnica: matriz papel × ação; tabela de decisão; pares de papéis. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Os verbos do solicitante verificam a identidade de quem chama

    Esquema do Cenário: [CT-32] Outra pessoa não edita, exclui, envia nem cancela a compra de Sofia
      Dado a solicitação de Sofia está <origem> com “Notebook”, “8000.01”, centro Operações e o histórico real dessa situação
      E Paula é outra panel_user de Acme, Geraldo é gestor e Daniela é diretora, todos com e-mail
      Quando Paula tenta <operacao> pelo domínio, sem componente
      Então a operação é recusada, o registro conserva a situação <origem>, “Notebook”, “8000.01”, centro Operações e todas as decisões anteriores
      E nenhum e-mail de aprovação é enviado a Sofia, Geraldo, Paula ou Daniela

      Exemplos:
        | origem | operacao | # partição |
        | rascunho | editar valor para 4999.99 | outra pessoa × editar |
        | rascunho | excluir | outra pessoa × excluir |
        | rascunho | enviar | outra pessoa × enviar |
        | aguardando_gestor | cancelar | outra pessoa × cancelar antes do gestor |
        | aguardando_diretor | cancelar | outra pessoa × cancelar antes do diretor |

    Esquema do Cenário: [CT-33] Uma ação forjada não ultrapassa a autorização do componente
      Dado a solicitação de Sofia está <origem> com todos os campos e decisões capturados, Geraldo gestor e Daniela diretora real em Acme
      E Paula tem acesso ao painel e à consulta permitida, mas não é solicitante nem aprovadora dessa solicitação
      Quando Paula força <operacao> pelo componente, mesmo sem o botão disponível
      Então a operação é recusada e o registro mantém os campos, a situação <origem> e o histórico capturados, sem e-mail para Geraldo ou Daniela; a ação correspondente permanece oculta ou a página de edição não é acessível a Paula

      Exemplos:
        | origem | operacao | # partição |
        | rascunho | editar valor para 4999.99 | UI editar |
        | rascunho | excluir | UI excluir |
        | rascunho | enviar | UI enviar |
        | aguardando_gestor | cancelar | UI cancelar |

    Esquema do Cenário: [CT-34] Acumular dois papéis não cria aprovação automática nem impede o papel autorizado
      Dado a solicitação de “8000.01” está <origem> por transições reais em Acme, e <ator> acumula <par>
      E Geraldo e Daniela existem como outras personas reais; o histórico anterior tem <antes> decisões
      Quando <ator> aprova pelo domínio somente a etapa <etapa>
      Então a situação persistida é <destino> e o histórico ganhou exatamente uma decisão aprovada da etapa <etapa> por <ator>, conservando as <antes> anteriores

      Exemplos:
        | origem | ator | par | antes | etapa | destino | # partição |
        | aguardando_gestor | Sofia | solicitante e gestor | 0 | gestor | aguardando_diretor | A-09 |
        | aguardando_diretor | Sofia | solicitante e diretor | 1 | diretor | aprovada | diretor é qualquer titular em Acme |
        | aguardando_gestor | Geraldo | gestor e diretor | 0 | gestor | aguardando_diretor | primeira etapa permanece separada |
        | aguardando_diretor | Geraldo | gestor e diretor | 1 | diretor | aprovada | segunda decisão explícita |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-35 | Conferir apenas permission de update/delete, sem o dono do registro | CT-32 | Paula é recusada em editar e excluir na escrita direta |
| M-36 | Conferir identidade só no filtro ou no botão da UI | CT-32, CT-33 | os quatro verbos recusam Paula sem alterar agregado ou e-mails |
| M-37 | Aplicar segregação de funções não acordada ou pular a segunda etapa quando os papéis coincidem | CT-34 | Sofia gestora pode decidir; Geraldo gestor+diretor deixa a primeira decisão aguardando_diretor |

## Regra R11 — Aprovar e rejeitar verificam o aprovador da etapa corrente

Origem: RQ-04, RQ-05, RQ-06, RQ-07; A-02, A-03, A-07. Área: Autorização e contexto (completo). Técnica: matriz papel × ação; tabela de decisão completa. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Aprovar e rejeitar verificam o aprovador da etapa corrente

    Esquema do Cenário: [CT-35] O papel ou a participação anterior não substitui a autoridade da etapa
      Dado a solicitação de Sofia está <origem> por transições reais no centro Operações de Geraldo, com valor “8000.01” e histórico capturado
      E Paula gere outro centro, Daniela é diretora e Rui é panel_user sem autoridade de aprovação em Acme
      Quando <ator> tenta <operacao> pelo domínio, usando justificativa “Sem verba” na rejeição
      Então a operação é recusada e a situação <origem> e todas as decisões e justificativas anteriores permanecem gravadas
      E zero e-mails de aprovação são enviados a Sofia, Geraldo, Paula, Daniela ou Rui

      Exemplos:
        | origem | ator | operacao | # partição |
        | aguardando_gestor | Paula | aprovar | gestor de outro centro × aprovar |
        | aguardando_gestor | Daniela | aprovar | diretor antes do gestor × aprovar |
        | aguardando_gestor | Sofia | aprovar | solicitante sem autoridade × aprovar |
        | aguardando_diretor | Geraldo | aprovar | gestor que já decidiu × aprovar |
        | aguardando_diretor | Rui | aprovar | sem papel diretor × aprovar |
        | aguardando_gestor | Paula | rejeitar | gestor de outro centro × rejeitar |
        | aguardando_gestor | Daniela | rejeitar | diretor antes do gestor × rejeitar |
        | aguardando_gestor | Sofia | rejeitar | solicitante sem autoridade × rejeitar |
        | aguardando_diretor | Geraldo | rejeitar | gestor que já decidiu × rejeitar |
        | aguardando_diretor | Rui | rejeitar | sem papel diretor × rejeitar |

    Esquema do Cenário: [CT-36] Ser diretor em outra organização não autoriza esta decisão
      Dado a solicitação de Sofia em Acme está aguardando_diretor após aprovação real de Geraldo e tem uma decisão de gestor
      E Daniela tem diretor somente em Globex e panel_user em Acme; Paula é diretora real de Acme, e o contexto corrente é Acme
      Quando Daniela tenta <operacao> pelo domínio em Acme, com justificativa “Sem verba” na rejeição
      Então a operação é recusada e a solicitação permanece aguardando_diretor com somente a decisão anterior por Geraldo, sem e-mail para Paula

      Exemplos:
        | operacao | # partição |
        | aprovar | papel fora do contexto × aprovar |
        | rejeitar | papel fora do contexto × rejeitar |

    Esquema do Cenário: [CT-37] Aprovação e rejeição forçadas pelo ator errado continuam recusadas
      Dado a solicitação de Sofia está aguardando_gestor com Geraldo gestor, Daniela diretora e Rui panel_user sem autoridade em Acme
      Quando Rui força a ação <operacao> no componente, com justificativa “Sem verba” na rejeição
      Então a ação não pode ser concluída, a situação persistida continua aguardando_gestor, há zero decisões e zero e-mails para Geraldo ou Daniela; a ação <operacao> permanece oculta para Rui

      Exemplos:
        | operacao | # partição |
        | aprovar | autoridade × aprovar UI |
        | rejeitar | autoridade × rejeitar UI |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-38 | Qualquer gestor aprova um centro, sem comparar a identidade da FK | CT-35 | Paula é recusada nos dois verbos no centro de Geraldo |
| M-39 | Diretor pode decidir na etapa de gestor, ou gestor decide também a segunda etapa sem ser diretor | CT-35 | Daniela não decide antes do gestor; Geraldo não decide depois sem papel diretor |
| M-40 | Conferir autoridade em aprovar e esquecer a mesma guarda em rejeitar | CT-35, CT-37 | todos os pares de ator inválido também disparam rejeitar e conservam o histórico |
| M-41 | Consultar o papel diretor de qualquer organização ou do contexto global | CT-36 | Daniela, diretora somente em Globex, não altera a compra de Acme |

## Regra R12 — Cada intenção de transição resolve uma etapa uma única vez

Origem: RQ-04, RQ-05, RQ-06, RQ-08, RQ-11, RQ-13, RQ-14; A-03. Área: Ciclo e alçada (completo). Técnica: idempotência no agregado; concorrência; atomicidade da decisão. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Cada intenção de transição resolve uma etapa uma única vez

    Esquema do Cenário: [CT-38] O retry da mesma etapa não duplica decisão ou aviso
      Dado a solicitação de Sofia está <origem> com o histórico correspondente, Geraldo gestor e Daniela e Paula diretoras reais de Acme
      E a captura dos e-mails começou depois da fixture e as duas tentativas representam a mesma intenção de etapa, não uma nova decisão da etapa seguinte
      Quando o ator autorizado repete duas vezes <operacao> pelo domínio
      Então a situação persistida é <destino>, o histórico ganhou <novas_decisoes> decisões da intenção e cada destinatário da próxima etapa recebeu exatamente <avisos> e-mails dessa intenção

      Exemplos:
        | origem | operacao | destino | novas_decisoes | avisos | # partição |
        | rascunho | enviar | aguardando_gestor | 0 | 1 | retry de envio |
        | aguardando_gestor | aprovar valor 4999.99 | aprovada | 1 | 0 | retry de aprovação final do gestor |
        | aguardando_gestor | aprovar valor 8000.01 | aguardando_diretor | 1 | 1 | retry da etapa de gestor |
        | aguardando_diretor | aprovar | aprovada | 1 | 0 | retry da etapa de diretor |
        | aguardando_gestor | rejeitar com Sem verba | rascunho | 1 | 0 | retry de rejeição |
        | aguardando_gestor | cancelar | cancelada | 0 | 0 | retry de cancelamento |

    Esquema do Cenário: [CT-39] Duas decisões realmente concorrentes de diretor têm uma única vencedora
      Dado a solicitação de Sofia de “8000.01” está aguardando_diretor com somente a aprovação de Geraldo, e Daniela e Paula são diretoras reais de Acme
      E duas conexões e dois processos carregam essa mesma etapa antes de qualquer escrita, com barreira real de sincronização; Daniela é liberada para confirmar primeiro
      Quando Daniela aprova e Paula tenta <segunda_decisao> concorrentemente a mesma etapa pelo domínio
      Então o agregado persistido fica aprovada, com a decisão anterior de Geraldo e exatamente uma decisão de diretor aprovada por Daniela
      E a tentativa perdedora não grava decisão ou justificativa de Paula, e não há novo e-mail para Sofia, Geraldo, Daniela ou Paula

      Exemplos:
        | segunda_decisao | # partição |
        | aprovar | aprovação × aprovação |
        | rejeitar com Sem verba | aprovação × rejeição |

    Cenário: [CT-40] A decisão e a situação não ficam pela metade quando a gravação do histórico falha
      Dado a solicitação de Sofia de “8000.01” está aguardando_gestor sem decisões, Geraldo é gestor e Daniela e Paula são diretoras reais
      E o arnês provoca falha durante a persistência da decisão, depois de uma escrita de situação já executada e antes de concluir o conjunto de escritas
      Quando Geraldo tenta aprovar pelo domínio a solicitação
      Então a operação falha e a nova consulta encontra aguardando_gestor, zero decisões de gestor ou diretor e zero avisos de aprovação para Daniela e Paula
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-42 | Conferir estado só na instância antiga e duplicar efeito no retry | CT-38 | mesmo agregado tem uma decisão e um aviso por destinatário da próxima etapa |
| M-43 | Fazer check-then-act sem reserva atômica e aceitar os dois diretores | CT-39 | duas conexões produzem exatamente uma decisão de diretor, por Daniela |
| M-44 | Gravar a situação sem rollback se a decisão falha, ou gravar história antes de vencer a corrida | CT-40, CT-39 | falha conserva aguardando_gestor sem decisão; perdedora não acrescenta Paula |

## Regra R13 — Os avisos usam e-mail e alcançam somente o próximo aprovador da organização

Origem: RQ-14; A-02, A-03, A-11. Área: E-mail (completo). Técnica: rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Os avisos usam e-mail e alcançam somente o próximo aprovador da organização

    Esquema do Cenário: [CT-41] O envio produz um e-mail para o gestor certo em cada alçada
      Dado a solicitação de Sofia está em rascunho no centro Operações de Geraldo com valor <valor>, e a captura de notificações está vazia
      E Paula gere outro centro e Daniela é diretora de Acme; todos, inclusive Sofia, têm e-mail real
      Quando Sofia envia pelo domínio a solicitação
      Então Geraldo recebe exatamente uma AprovacaoPendente dessa solicitação para a etapa gestor no canal mail
      E o total de avisos de aprovação é um e Sofia, Paula e Daniela recebem zero

      Exemplos:
        | valor | # partição |
        | 4999.99 | sem etapa extra |
        | 5000.00 | borda literal |
        | 5000.01 | com etapa extra |

    Esquema do Cenário: [CT-42] Todos os diretores da organização recebem uma vez a próxima etapa
      Dado a solicitação de Sofia de “8000.01” em Acme está aguardando_gestor, Geraldo é gestor e Acme tem <diretores_acme> pessoas distintas com papel diretor
      E Rui tem diretor somente em Globex e Daniela, quando presente em Acme, também tem diretor em Globex; a captura de avisos começou após o envio
      Quando Geraldo aprova pelo domínio a etapa de gestor em Acme
      Então a situação persistida é aguardando_diretor e cada diretor de Acme recebe exatamente um aviso dessa solicitação para a etapa diretor no canal mail, total <diretores_acme>
      E Rui, Sofia e Geraldo recebem zero avisos de aprovação

      Exemplos:
        | diretores_acme | # partição |
        | 1 | cardinalidade um; Daniela |
        | 2 | cardinalidade N; Daniela e Paula |

    Esquema do Cenário: [CT-43] Os caminhos sem próxima etapa não enviam novos e-mails
      Dado a solicitação de Sofia está <origem> com o histórico real dessa situação, Geraldo gestor e Daniela e Paula diretoras reais, todos com e-mail
      E a captura de avisos foi iniciada depois da fixture e o valor da compra é <valor>
      Quando o ator autorizado executa <operacao> pelo domínio
      Então o banco contém <destino> e o histórico corresponde somente à decisão ou cancelamento efetuado, com zero novos e-mails de aprovação para Sofia, Geraldo, Daniela e Paula

      Exemplos:
        | origem | valor | operacao | destino | # partição |
        | aguardando_gestor | 4999.99 | aprovar | aprovada | aprovação final baixa |
        | aguardando_gestor | 5000.00 | aprovar | aprovada | aprovação final na borda |
        | aguardando_diretor | 5000.01 | aprovar | aprovada | aprovação final alta |
        | aguardando_gestor | 4999.99 | rejeitar com Sem verba | rascunho | rejeição baixa |
        | aguardando_gestor | 5000.01 | rejeitar com Sem verba | rascunho | rejeição alta pelo gestor |
        | aguardando_diretor | 5000.01 | rejeitar com Sem verba | rascunho | rejeição alta pelo diretor |
        | aguardando_gestor | 4999.99 | cancelar | cancelada | cancelamento baixo |
        | aguardando_gestor | 5000.01 | cancelar | cancelada | cancelamento alto antes do gestor |
        | aguardando_diretor | 5000.01 | cancelar | cancelada | cancelamento alto antes do diretor |

    Cenário: [CT-44] Uma notificação capturada só vale como e-mail se o canal pedido estiver presente
      Dado a solicitação de Sofia está em rascunho em Acme, Geraldo é o gestor do centro e Daniela é diretora real
      Quando Sofia envia pelo domínio a solicitação
      Então o aviso capturado para Geraldo identifica essa solicitação e etapa gestor, sua lista efetiva de canais contém mail e sua mensagem para mail identifica a solicitação correta
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-45 | Enviar uma notificação database em vez do e-mail pedido | CT-44, CT-41 | lista efetiva de canais contém mail e a mensagem identifica a solicitação |
| M-46 | Notificar só o primeiro diretor ou duplicar Daniela por seus papéis em duas organizações | CT-42 | com dois diretores de Acme são dois avisos, um por pessoa |
| M-47 | Resolver diretores no contexto global ou de Globex | CT-42 | Rui recebe zero e os diretores de Acme recebem um cada |
| M-48 | Enviar aviso de rejeição, cancelamento ou aprovação final ao solicitante ou antigo aprovador | CT-43 | zero novos avisos nos nove caminhos sem próxima etapa |
| M-49 | Esquecer o aviso de envio ou usar um gestor qualquer da organização | CT-41 | Geraldo recebe um aviso e Paula recebe zero |

## Regra R14 — A listagem e o detalhe mostram a situação atual de cada solicitação

Origem: RQ-12; A-12. Área: Apresentação (padrão). Técnica: EP exaustiva dos cinco estados; cardinalidade de listagem. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A listagem e o detalhe mostram a situação atual de cada solicitação

    Esquema do Cenário: [CT-45] A listagem representa cada uma das cinco situações atuais
      Dado a solicitação de Sofia está <situacao> construída por transições reais em Acme, e Sofia tem permissão de consulta
      Quando Sofia consulta a listagem pelo componente
      Então a linha dessa solicitação está presente e o status mostrado nessa linha corresponde a <situacao>, sem exibir um status diferente

      Exemplos:
        | situacao | # partição |
        | rascunho | enum rascunho |
        | aguardando_gestor | enum aguardando_gestor |
        | aguardando_diretor | enum aguardando_diretor |
        | aprovada | enum aprovada |
        | cancelada | enum cancelada |

    Esquema do Cenário: [CT-46] O detalhe representa cada uma das cinco situações atuais
      Dado a solicitação de Sofia está <situacao> construída por transições reais em Acme, e Sofia tem permissão de consulta
      Quando Sofia consulta pelo componente o detalhe desse registro
      Então o detalhe identifica a solicitação de Sofia e mostra status correspondente a <situacao>, sem trocar aguardando_diretor por aprovada

      Exemplos:
        | situacao | # partição |
        | rascunho | enum rascunho |
        | aguardando_gestor | enum aguardando_gestor |
        | aguardando_diretor | enum aguardando_diretor |
        | aprovada | enum aprovada |
        | cancelada | enum cancelada |

    Esquema do Cenário: [CT-47] A consulta paginada não perde solicitações nem usa o vazio como prova de status
      Dado Acme tem <quantidade> solicitações de Sofia em rascunho com descrições e identificadores distintos, e o tamanho efetivo da página de teste é 10
      Quando Sofia consulta pelo componente a listagem e as páginas necessárias do mesmo resultado
      Então o conjunto de identificadores retornados nas páginas contém exatamente as <quantidade> solicitações de Acme, cada linha com status rascunho, sem duplicata ou solicitação de Globex

      Exemplos:
        | quantidade | # partição |
        | 0 | vazia |
        | 1 | um registro |
        | 10 | limite da página |
        | 11 | acima do limite |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-50 | Rotular aguardando_diretor como aprovada ou usar o rótulo do estado anterior | CT-45, CT-46 | as duas superfícies mostram a partição aguardando_diretor |
| M-51 | O detalhe usa o status correto e a tabela continua usando outro campo | CT-45 | cada uma das cinco linhas de enum aparece na linha certa |
| M-52 | Retornar somente a primeira página ou perder o último item no limite | CT-47 | 11 IDs distintos são encontrados no conjunto das páginas |

## Regra R15 — O histórico mostra os autores das etapas e conserva os dados da decisão

Origem: RQ-13; A-12. Área: Apresentação (padrão). Técnica: EP de caminho; rastreio da exibição. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O histórico mostra os autores das etapas e conserva os dados da decisão

    Esquema do Cenário: [CT-48] O detalhe mostra quem decidiu cada etapa sem substituir pelo usuário que consulta
      Dado a solicitação de Sofia está aprovada por transições reais no caminho <caminho>, e as decisões foram feitas nos instantes conhecidos e distintos de Geraldo e Daniela
      E Sofia consulta o detalhe com permissão de consulta em Acme
      Quando Sofia abre o detalhe pelo componente
      Então o histórico contém <linhas> linhas de decisão com etapas e autores <autores>, nos respectivos instantes reais, sem atribuir as decisões a Sofia

      Exemplos:
        | caminho | linhas | autores | # partição |
        | valor 4999.99; gestor | 1 | gestor Geraldo | uma etapa |
        | valor 5000.01; gestor e diretor | 2 | gestor Geraldo e diretor Daniela | duas etapas |

    Cenário: [CT-49] A justificativa e os autores do ciclo anterior continuam visíveis após a volta ao rascunho
      Dado a solicitação de Sofia de “8000.01” está em rascunho após a aprovação real de Geraldo e a rejeição real de Daniela com “Não há orçamento 🔧”
      Quando Sofia consulta pelo componente o detalhe desse rascunho
      Então o histórico mostra gestor aprovado por Geraldo e diretor rejeitado por Daniela, com os instantes das duas decisões e a justificativa integral “Não há orçamento 🔧”

    Cenário: [CT-50] Um aprovador com permissão de consulta lê sua decisão depois da etapa
      Dado a solicitação de Sofia está aprovada após decisões reais de Geraldo e Daniela, e Geraldo conserva permissão de consulta em Acme
      Quando Geraldo consulta pelo componente o detalhe dessa solicitação aprovada
      Então o detalhe identifica a solicitação e mostra sua decisão de gestor por Geraldo e a decisão de diretor por Daniela, sem ocultar o registro por não haver etapa pendente
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-53 | Mostrar o usuário que está logado no lugar de quem decidiu | CT-48 | Sofia vê os nomes Geraldo e Daniela, não Sofia como aprovadora |
| M-54 | Limpar ou esconder o histórico ao devolver para rascunho | CT-49 | as duas decisões e a justificativa integral continuam no detalhe |
| M-55 | Filtrar a consulta somente por aprovador pendente e ocultar participantes anteriores | CT-50 | Geraldo vê o registro já aprovado e os dois autores |

## Regra R16 — A administração cadastra o centro e mantém o vínculo de um gestor

Origem: RQ-01, RQ-04; A-01, A-02, A-08. Área: Cadastro de centro (padrão). Técnica: EP de formulário; rastreio da gravação. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A administração cadastra o centro e mantém o vínculo de um gestor

    Cenário: [CT-51] A criação do centro apresenta nome e gestor à administração
      Dado a administradora Ana de Acme ainda não tem o centro Projetos e Paula é uma usuária real da organização
      Quando Ana visita autenticada a rota create de centro de custo
      Então a resposta permite o cadastro e contém os controles de nome e seleção do gestor

    Cenário: [CT-52] O componente create grava o nome e o gestor escolhido
      Dado a administradora Ana de Acme ainda não tem o centro Projetos e Paula é uma usuária real da organização
      Quando Ana salva pelo componente create o centro com nome “Projetos” e gestora Paula
      Então a nova consulta encontra exatamente um centro Projetos de Acme com Paula como gestora

    Cenário: [CT-53] A edição do centro carrega o gestor do registro correto
      Dado o centro Projetos existe em Acme com gestora Paula, e Ana é administradora de Acme
      Quando Ana visita autenticada a rota edit desse centro
      Então a resposta contém nome Projetos e a seleção de Paula para esse registro

    Esquema do Cenário: [CT-54] O componente edit grava a troca de gestor e também salva sem alteração
      Dado o centro Projetos existe em Acme com gestora Paula, Ana é administradora e Geraldo é outra pessoa real de Acme
      Quando Ana salva pelo componente edit o nome “Projetos” e o gestor <gestor>
      Então o mesmo centro de Acme continua com nome “Projetos” e gestor <gestor>, sem criar outro centro ou mudar o centro de outra organização

      Exemplos:
        | gestor | # partição |
        | Geraldo | troca do gestor |
        | Paula | edição sem alteração |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-56 | A tela create abre mas a gravação de gestor é descartada | CT-52 | centro Projetos persistido pertence a Acme e tem Paula como gestora |
| M-57 | O edit grava só nome e ignora a troca de gestor | CT-54 | mesmo centro passa a ter Geraldo na linha de troca |
| M-58 | O edit acusa colisão do próprio registro ou cria uma cópia quando não há alteração | CT-54 | linha Paula mantém o mesmo ID e somente um centro Projetos |
| M-59 | Uma rota de escrita não contém os dados de nome e gestor | CT-51, CT-53 | create tem ambos os controles e edit mostra Projetos/Paula |

## Regra R17 — Usuário comum não administra centro de custo nem se nomeia gestor

Origem: RQ-04; A-08. Área: Autorização e contexto (completo). Técnica: matriz papel × ação; tabela de decisão; ação fora da UI. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Usuário comum não administra centro de custo nem se nomeia gestor

    Esquema do Cenário: [CT-55] O usuário comum não grava administração do centro por fora do componente
      Dado Sofia é panel_user de Acme, o centro Projetos existe com gestora Paula e Ana é administradora, todos pessoas distintas
      Quando Sofia tenta <operacao> pelo ponto de escrita autorizado da administração, sem componente
      Então a operação é recusada, o centro Projetos mantém nome, organização e gestora Paula e não surge novo centro administrado por Sofia

      Exemplos:
        | operacao | # partição |
        | criar centro Operações com Sofia gestora | comum × criar |
        | alterar nome para Operações | comum × editar nome |
        | alterar gestor para Sofia | escalada por identidade |
        | excluir centro Projetos | comum × excluir |

    Cenário: [CT-56] O formulário forjado não permite ao usuário comum trocar gestor
      Dado o centro Projetos de Acme tem gestora Paula, Sofia é panel_user e tem permissão para criar solicitação de compra
      Quando Sofia força pelo componente edit a troca do gestor para Sofia
      Então a escrita é recusada e o centro Projetos continua com Paula como gestora e com o mesmo tenant, sem promover Sofia

    Cenário: [CT-57] O papel diretor acordado abre a compra no painel da sua organização
      Dado a solicitação de Sofia está aguardando_diretor em Acme depois da aprovação real de Geraldo, e Daniela tem somente o papel diretor em Acme
      Quando Daniela visita autenticada a rota de detalhe dessa solicitação no painel app de Acme
      Então a resposta permite a consulta e mostra a solicitação de Sofia, situação aguardando_diretor e a decisão de gestor por Geraldo
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-60 | Incluir CentroCusto na matriz do panel_user e permitir alterar gestor | CT-55, CT-56 | Sofia não troca Paula por Sofia pela escrita direta nem pelo componente |
| M-61 | Excluir a entidade negócio junto com a administração e impedir o usuário comum de solicitar | CT-03 | panel_user Sofia consegue criar a solicitação com os campos persistidos |
| M-62 | Criar diretor sem painel app e dar 403 mesmo à pessoa destinada à etapa | CT-57 | Daniela com somente diretor abre o detalhe de Acme e lê a etapa pendente |

## Regra R18 — A organização e a autoria não podem ser trocadas por identificadores ou payload

Origem: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-13; A-01, A-03, A-08; convenção de organização. Área: Autorização e contexto (completo). Técnica: IDOR por entidade; mass assignment por entidade; EP de referência e discriminante. As partições abaixo são executadas isoladamente; cada linha de Exemplos começa com fixture nova.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A organização e a autoria não podem ser trocadas por identificadores ou payload

    Esquema do Cenário: [CT-58] Uma solicitação de outra organização não pode ser lida ou alterada pelo ID conhecido
      Dado Sofia opera Acme e também pertence legitimamente a Globex; a solicitação de Sofia está <situacao> em Globex e Sofia é dona, gestora do centro e diretora autorizada lá para isolar somente a organização corrente; todos os campos e decisões foram capturados
      E Geraldo e Daniela são aprovadores reais disponíveis em Globex, e os direitos de Sofia permitiriam a operação se o contexto fosse Globex
      Quando Sofia tenta <operacao> com o UUID ou ID conhecido dessa solicitação no contexto de Acme, por HTTP ou pelo ponto de domínio indicado
      Então o resultado é <resultado>, o registro estrangeiro não é entregue e conserva organização Globex, solicitante Sofia, situação <situacao>, valor, centro e decisões capturados
      E zero e-mails de aprovação são enviados aos aprovadores de Globex pela tentativa

      Exemplos:
        | situacao | operacao | resultado | # partição |
        | rascunho | ler detalhe por HTTP | 403 ou 404, sem conteúdo da solicitação | IDOR solicitação × ler |
        | rascunho | editar valor pelo domínio | recusa sem alteração | IDOR solicitação × editar |
        | rascunho | excluir pelo domínio | recusa sem alteração | IDOR solicitação × excluir |
        | rascunho | enviar pelo domínio | recusa sem alteração | IDOR solicitação × enviar |
        | aguardando_gestor | cancelar pelo domínio | recusa sem alteração | IDOR solicitação × cancelar |
        | aguardando_gestor | aprovar pelo domínio | recusa sem alteração | IDOR solicitação × aprovar |
        | aguardando_gestor | rejeitar com Sem verba pelo domínio | recusa sem alteração | IDOR solicitação × rejeitar |

    Esquema do Cenário: [CT-59] O identificador conhecido não torna o centro estrangeiro administrável
      Dado Ana administra legitimamente Acme e Globex, o contexto corrente é Acme e o centro Projetos de Globex tem nome Projetos e gestora Paula, todos os identificadores conhecidos
      Quando Ana tenta <operacao> nesse centro no contexto Acme, por HTTP ou pelo ponto de escrita da administração
      Então o resultado é <resultado>, o centro de Globex não é entregue e mantém nome Projetos, organização Globex e gestora Paula

      Exemplos:
        | operacao | resultado | # partição |
        | ler a rota edit | 403 ou 404 sem conteúdo estrangeiro | IDOR centro × leitura |
        | alterar gestor para Ana por fora do componente | recusa sem alteração | IDOR centro × alteração |
        | excluir por fora do componente | recusa sem alteração | IDOR centro × exclusão |

    Esquema do Cenário: [CT-60] A etapa histórica não ganha acesso independente pelo ID da filha
      Dado Sofia opera Acme, também é membro com direito de consulta em Globex e conhece o ID de uma decisão de gestor por Geraldo na sua solicitação aprovada de Globex
      Quando Sofia tenta <operacao> dessa decisão pelo ponto de acesso de histórico usado pela feature, sem acrescentar filtro de tenant no teste
      Então o resultado é <resultado>, nenhum histórico de Globex é entregue e a decisão permanece ligada à solicitação de Sofia de Globex, com etapa gestor, decisão aprovada e autor Geraldo

      Exemplos:
        | operacao | resultado | # partição |
        | ler pelo ID da decisão | não entrega a decisão estrangeira | IDOR etapa × leitura direta |
        | alterar autor para Sofia pelo ID da decisão | recusa sem alterar autor ou vínculo | filha × escrita não autorizada |

    Esquema do Cenário: [CT-61] Um centro estrangeiro não entra na solicitação por payload válido nos demais campos
      Dado Sofia opera Acme, o centro Projetos de Globex existe com gestora Paula, e Geraldo e Daniela existem como aprovadores reais de Acme
      E a solicitação está <partida> com descrição “Notebook” e valor “1299.99”, sendo o único dado inválido o ID do centro de Globex
      Quando Sofia tenta <operacao> pelo domínio com esse centro estrangeiro
      Então a operação é recusada, zero novas solicitações ou decisões são criadas, e o rascunho já existente quando houver mantém o centro de Acme e os outros campos
      E zero e-mails de aprovação são enviados a Paula, Geraldo ou Daniela

      Exemplos:
        | partida | operacao | # partição |
        | ainda inexistente | criar | referência na criação |
        | rascunho em Acme | editar centro | referência na edição |
        | rascunho com referência histórica estrangeira preparada só como dado corrupto | enviar | referência no uso |

    Esquema do Cenário: [CT-62] Campos do servidor não são escolhidos pelo payload do cliente
      Dado o ator autorizado opera Acme, o centro Projetos de Acme tem gestora Paula, Geraldo decide a etapa de gestor e Daniela é diretora real
      E <alvo> parte de <partida>, os demais dados são válidos e somente o campo protegido <campo> foi incluído como <forjado>
      Quando o ator autorizado solicita <operacao> pelo ponto de entrada indicado, incluindo esse campo extra no payload não confiável
      Então o agregado persistido tem <esperado>, sem adotar <forjado> para o campo protegido nem alterar as entidades de Globex

      Exemplos:
        | alvo | partida | campo | forjado | operacao | esperado | # partição |
        | solicitação | ainda inexistente | situacao | aprovada | criar pelo domínio | rascunho | solicitação × estado |
        | solicitação | ainda inexistente | solicitante_id | ID de Daniela | criar pelo domínio como Sofia | solicitante Sofia | solicitação × autoria |
        | solicitação | rascunho em Acme | tenant_id | ID de Globex | editar pelo domínio como Sofia | organização Acme | solicitação × tenant |
        | centro | ainda inexistente | tenant_id | ID de Globex | criar pelo domínio da administração como Ana | organização Acme | centro × tenant |
        | centro | centro de Acme existente | uuid | UUID do centro Globex | editar pelo domínio da administração como Ana | UUID original | centro × identidade |
        | etapa | solicitação aguardando_gestor | decidido_por_id | ID de Sofia | aprovar pelo domínio como Geraldo | autor Geraldo | etapa × autoria |
        | etapa | solicitação aguardando_gestor | solicitacao_compra_id | ID da compra de Globex | aprovar pelo domínio como Geraldo | pai é a compra de Acme | etapa × pai |
        | etapa | solicitação aguardando_gestor | etapa | diretor | aprovar pelo domínio como Geraldo | etapa gestor | etapa × etapa |

    Cenário: [CT-63] Um componente de usuário sem organização não entrega a base global
      Dado Acme e Globex têm solicitações e centros distintos com decisões históricas reais, Sofia é usuária de Acme e o componente é chamado com tenant corrente null
      Quando Sofia consulta pelo componente a listagem de compra e os dados de centro alcançáveis nesse contexto sem tenant
      Então nenhuma solicitação, centro ou decisão de Acme ou Globex é entregue ao cliente e nenhum dado é gravado ou notificado

    Esquema do Cenário: [CT-64] A recusa de um ID estrangeiro deixa alcançável a consulta legítima do usuário
      Dado Sofia está autenticada em Acme após uma resposta 403 ou 404 à consulta de <alvo> de Globex e sua solicitação própria está em rascunho com descrição “Notebook”
      Quando Sofia navega para a listagem própria de solicitações de Acme
      Então a resposta permite a consulta, contém somente a solicitação de Sofia com “Notebook” e status rascunho e não redireciona de volta ao registro estrangeiro

      Exemplos:
        | alvo | # partição |
        | solicitação | saída de IDOR da compra |
        | centro de custo | saída de IDOR do centro |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-63 | A query ou escrita aceita o ID sem conferir organização, incluindo a tabela filha | CT-58, CT-59, CT-60 | nenhum dado de Globex é entregue ou alterado para o ator de Acme |
| M-64 | O Select filtra centros mas a criação/edição direta aceita FK estrangeira | CT-61 | o ID real de Globex é recusado na criação, edição e uso |
| M-65 | Payload escolhe estado, autor, organização ou vínculo da decisão | CT-62 | cada tabela conserva o valor de servidor explicitado na coluna esperado |
| M-66 | A ausência de tenant é tratada como consulta global no componente do usuário | CT-63 | com dados nas duas organizações o cliente recebe zero dados de ambas |
| M-67 | A recusa redireciona o usuário entre destino inacessível e origem | CT-64 | a listagem própria é alcançada e mostra Notebook em rascunho |

## Checklist de Taxonomia de Defeito

“Lacuna” significa que não foi atribuída cobertura; não equivale a não aplicável. Nenhum item desta tabela substitui o cenário de sua costura. Os grupos D/C/A/P/T/TC são os do índice.

| Item | Cenário que mata ou justificativa/lacuna | Grupo |
|---|---|---|
| IDOR horizontal — dono | CT-32 executa quatro verbos com outra pessoa; CT-58 troca somente o contexto, preservando os direitos no tenant de origem | D, T |
| Autorização de ação fora da UI | CT-32, CT-35 e CT-55 escrevem diretamente; CT-33, CT-37 e CT-56 complementam o componente | D, P, C, A |
| Idempotência de cada escrita | CT-05 edição sem mudança; CT-10 exclusão repetida; CT-25 cancelamento repetido; CT-38 transições repetidas. **Lacuna da criação:** sem chave de intenção especificada | D |
| Condicional de domínio | CT-15 distingue abaixo/igual/acima de 5000.00; CT-16 separa literal do 00 de configuração. Limites do valor válido permanecem lacuna | D |
| Limites de cada campo editável | Presença/tipo/referência em CT-02, CT-06 e CT-19. **Lacuna n/n+1:** o 00 não dá tetos para descrição, nome de centro ou justificativa, nem política numérica | D, P |
| Contador/limite/primeira decisão concorrente | CT-39 usa duas conexões/processos e barreira real para dois diretores; CT-38 mata o retry sequencial, que não substitui concorrência | T, D |
| Efeito externo — ocorre/não ocorre/uma vez | CT-41, CT-42 e CT-44 canal/destinatário; CT-43 ramos sem próxima etapa; CT-38 retry. CT-40 só a falha anterior ao despacho externo | D, T |
| Cardinalidade 0/1/N de terceiros | CT-13 sem gestor, CT-41 um gestor, CT-42 um/N diretores. **Lacuna:** comportamento com zero diretores não dado | D, T |
| Campo opcional ausente/null/vazio | A-10 cobre gestor null em CT-13. O 00 não determina contrato de formulário para omissão/vazio de gestor; lacuna, sem equiparar payload vazio à ausência na entidade | D, A |
| Listagem 0/1/limite/acima | CT-47 compara conjuntos de IDs nas duas páginas e quantidades 0/1/10/11. **Lacuna:** inserção entre páginas e contrato de ordem não dado | C |
| Ordenação e desempate | **Lacuna:** sem ordem no 00 nem inventário de coluna/filtro público no 02; não inventar política só porque o resource pode oferecer sort | C, TC |
| Tempo: instante, fuso e prazo | CT-48 conserva instantes conhecidos das decisões. **Lacuna:** formato/fuso. SLA, expiração e calendário não aplicáveis ao escopo recebido | C |
| Texto Unicode e tamanho | CT-01, CT-05, CT-18 e CT-49 conservam Unicode e justificativa curta. **Lacuna:** máximo e política de truncamento/normalização não dada | D, C |
| Unicidade/soft delete | Não há regra de chave única de negócio ou soft delete no 00. CT-10/CT-11 verificam exclusão, mas não atribuem oráculo a índice ou scope de deletados | D |
| Entidade removida ainda referenciada | CT-11 usa instância carregada antes da exclusão e tenta os seis verbos de escrita | D |
| CRUD: inexistente, excluir dois, editar sem mudança | CT-02/CT-06 referência inexistente; CT-10 duas solicitações e segunda exclusão; CT-05/CT-54 edição sem mudança. **Lacuna:** leitura pelo ID inexistente, que não é a referência inexistente nem o ID estrangeiro | D, A, P |
| Mass assignment | CT-62 tem partições de solicitação, centro e etapa, com estado, autoria, organização, UUID, pai e etapa protegidos. Sem inventário do 02, não afirma exaustividade de todo método/propriedade pública | T |
| Upload | Não aplicável: anexos expressamente fora do escopo no 00; nenhum cenário nem superfície de upload criada | — |
| Dinheiro e precisão decimal | CT-15 usa strings 4999.99/5000.00/5000.01, compara valor persistido e estado; CT-16 testa configuração efetiva. **Lacuna:** três casas, arredondamento, zero/negativo e máximo | D |
| Livewire — propriedade pública/atributo protegido | CT-62 e CT-63 cobrem payload e escopo observável. **Lacuna:** inventário por propriedade pública e campo de servidor, pois 02 ausente | T, TC |
| Framework — consumo de coluna/filtro com entrada inválida | **Lacuna:** não há 02 com superfície que permita listar ponto, tipo inválido e coluna inválida sem olhar implementação da compra | C, TC |
| Método público — argumento inválido/tipo errado | CT-02/CT-06/CT-19 exercem entradas conhecidas do domínio. **Lacuna:** todos os métodos públicos não inventariados; não reivindicar cobertura exaustiva | D, C |
| Por entidade: solicitação — IDOR e atribuição | CT-58 lê/escreve pelo ID estrangeiro; CT-62 protege situação/solicitante/tenant | T |
| Por entidade: centro — IDOR e atribuição | CT-59 lê/escreve com admin apta nos dois tenants; CT-62 protege tenant e UUID | T |
| Por entidade: etapa — IDOR e atribuição | CT-60 sonda o ID direto da filha; CT-62 protege autor/pai/etapa. **Lacuna de endereço:** localizar ponto real sem inventar rota; inexistência do ponto requer registrar a sonda não executada | T |
| Discriminante null no escopo | CT-63 é consulta de usuário pelo componente com dados reais nos dois tenants. O scope global de jobs no projeto não justifica entrega global ao usuário | TC |
| Caminho de saída do erro | CT-64 navega após a recusa do registro estrangeiro e afirma o registro próprio legível; não é só assertStatus. **Lacuna:** fluxo de ID inexistente não especificado | T |

## Índice de Cenários

Arquivos são **destinos planejados, não criados**. Nenhum teste foi materializado ou executado. “Pest feature HTTP” inclui visitas HTTP e chamadas de domínio com o TestCase Laravel/banco, sem inventar controller de escrita. Grupo define a costura; cenário de exibição exige conteúdo concreto do componente, não só status 200.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | A criação conserva descrição, valor e centro escolhidos | R1 | EP; rastreio da gravação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-02 |
| CT-02 | Um campo obrigatório inválido impede a criação fora da UI | R1 | EP; rastreio da gravação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-01 |
| CT-03 | O formulário de criação grava os três campos do solicitante | R1 | EP; rastreio da gravação | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-02, M-03, M-61 |
| CT-04 | A rota de criação oferece os três dados obrigatórios | R1 | EP; rastreio da gravação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-04 |
| CT-05 | O solicitante corrige cada campo decisivo em rascunho | R2 | EP de campo; matriz estado × operação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-06 |
| CT-06 | A obrigatoriedade também é aplicada na correção do rascunho | R2 | EP de campo; matriz estado × operação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-05 |
| CT-07 | O formulário edit grava a correção do dono do rascunho | R2 | EP de campo; matriz estado × operação | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-06, M-07 |
| CT-08 | A rota edit carrega os dados do rascunho certo | R2 | EP de campo; matriz estado × operação | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-08 |
| CT-09 | O solicitante exclui seu rascunho | R3 | estado × operação; EP de existência; idempotência no agregado | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-09 |
| CT-10 | A repetição da exclusão não ressuscita nem afeta outra compra | R3 | estado × operação; EP de existência; idempotência no agregado | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-10 |
| CT-11 | Uma instância carregada antes da exclusão não continua operando | R3 | estado × operação; EP de existência; idempotência no agregado | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-09, M-11 |
| CT-12 | Qualquer alçada começa pelo gestor do próprio centro | R4 | EP; tabela de decisão; rastreio do destinatário | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-12 |
| CT-13 | O centro sem gestor impede o envio e conserva o rascunho | R4 | EP; tabela de decisão; rastreio do destinatário | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-13 |
| CT-14 | A correção do centro muda quem recebe a solicitação enviada | R4 | EP; tabela de decisão; rastreio do destinatário | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-14 |
| CT-15 | O centavo em torno de cinco mil determina a próxima etapa | R5 | BVA 3-valores (0,01); tabela de decisão | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-15, M-16, M-18 |
| CT-16 | A mudança explícita da alçada é usada na decisão | R5 | BVA 3-valores (0,01); tabela de decisão | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-17 |
| CT-17 | A decisão do diretor encerra a compra alta depois da decisão do gestor | R5 | BVA 3-valores (0,01); tabela de decisão | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-18 |
| CT-18 | Gestor e diretor rejeitam com uma justificativa curta ou Unicode | R6 | EP; estado × evento; normalização de branco | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-21, M-22 |
| CT-19 | A escrita direta recusa cada forma de justificativa ausente | R6 | EP; estado × evento; normalização de branco | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-19, M-20 |
| CT-20 | O componente recusa a rejeição sem justificativa e conserva a etapa | R6 | EP; estado × evento; normalização de branco | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-23 |
| CT-21 | A rejeição nas duas etapas reinicia o envio no gestor | R7 | 2-switch; estado × evento; EP de origem | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-24, M-26 |
| CT-22 | A correção depois da rejeição altera a alçada do novo ciclo | R7 | 2-switch; estado × evento; EP de origem | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-25, M-26 |
| CT-23 | O novo ciclo não conserva autoridade do centro anterior | R7 | 2-switch; estado × evento; EP de origem | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-27 |
| CT-24 | O cancelamento vale antes da decisão do gestor ou do diretor | R8 | estado × evento; rastreio do não-efeito | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-28, M-29 |
| CT-25 | A repetição do cancelamento mantém o agregado cancelado | R8 | estado × evento; rastreio do não-efeito | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-30 |
| CT-26 | A operação editar não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-31, M-33 |
| CT-27 | A operação excluir não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-31 |
| CT-28 | A operação enviar não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-32, M-33, M-34 |
| CT-29 | A operação aprovar não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-32, M-34 |
| CT-30 | A operação rejeitar não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-32, M-34 |
| CT-31 | A operação cancelar não atua nos estados em que é proibida | R9 | produto cartesiano estado × operação; EP de campo | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-33 |
| CT-32 | Outra pessoa não edita, exclui, envia nem cancela a compra de Sofia | R10 | matriz papel × ação; tabela de decisão; pares de papéis | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-35, M-36 |
| CT-33 | Uma ação forjada não ultrapassa a autorização do componente | R10 | matriz papel × ação; tabela de decisão; pares de papéis | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-36 |
| CT-34 | Acumular dois papéis não cria aprovação automática nem impede o papel autorizado | R10 | matriz papel × ação; tabela de decisão; pares de papéis | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-37 |
| CT-35 | O papel ou a participação anterior não substitui a autoridade da etapa | R11 | matriz papel × ação; tabela de decisão completa | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-38, M-39, M-40 |
| CT-36 | Ser diretor em outra organização não autoriza esta decisão | R11 | matriz papel × ação; tabela de decisão completa | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-41 |
| CT-37 | Aprovação e rejeição forçadas pelo ator errado continuam recusadas | R11 | matriz papel × ação; tabela de decisão completa | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-40 |
| CT-38 | O retry da mesma etapa não duplica decisão ou aviso | R12 | idempotência no agregado; concorrência; atomicidade da decisão | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-42 |
| CT-39 | Duas decisões realmente concorrentes de diretor têm uma única vencedora | R12 | idempotência no agregado; concorrência; atomicidade da decisão | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-43, M-44 |
| CT-40 | A decisão e a situação não ficam pela metade quando a gravação do histórico falha | R12 | idempotência no agregado; concorrência; atomicidade da decisão | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-44 |
| CT-41 | O envio produz um e-mail para o gestor certo em cada alçada | R13 | rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-45, M-49 |
| CT-42 | Todos os diretores da organização recebem uma vez a próxima etapa | R13 | rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-46, M-47 |
| CT-43 | Os caminhos sem próxima etapa não enviam novos e-mails | R13 | rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-48 |
| CT-44 | Uma notificação capturada só vale como e-mail se o canal pedido estiver presente | R13 | rastreio do efeito (ocorre, não ocorre, uma vez); EP de alçada; cardinalidade 0/1/N | Domínio da compra | Pest feature HTTP | `tests/Feature/AprovacaoCompra/FluxoTest.php` | M-45 |
| CT-45 | A listagem representa cada uma das cinco situações atuais | R14 | EP exaustiva dos cinco estados; cardinalidade de listagem | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-50, M-51 |
| CT-46 | O detalhe representa cada uma das cinco situações atuais | R14 | EP exaustiva dos cinco estados; cardinalidade de listagem | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-50 |
| CT-47 | A consulta paginada não perde solicitações nem usa o vazio como prova de status | R14 | EP exaustiva dos cinco estados; cardinalidade de listagem | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-52 |
| CT-48 | O detalhe mostra quem decidiu cada etapa sem substituir pelo usuário que consulta | R15 | EP de caminho; rastreio da exibição | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-53 |
| CT-49 | A justificativa e os autores do ciclo anterior continuam visíveis após a volta ao rascunho | R15 | EP de caminho; rastreio da exibição | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-54 |
| CT-50 | Um aprovador com permissão de consulta lê sua decisão depois da etapa | R15 | EP de caminho; rastreio da exibição | Componentes da compra | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` | M-55 |
| CT-51 | A criação do centro apresenta nome e gestor à administração | R16 | EP de formulário; rastreio da gravação | Autorização de administração | Pest feature HTTP | `tests/Feature/AprovacaoCompra/PermissoesTest.php` | M-59 |
| CT-52 | O componente create grava o nome e o gestor escolhido | R16 | EP de formulário; rastreio da gravação | Administração de centros | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-56 |
| CT-53 | A edição do centro carrega o gestor do registro correto | R16 | EP de formulário; rastreio da gravação | Autorização de administração | Pest feature HTTP | `tests/Feature/AprovacaoCompra/PermissoesTest.php` | M-59 |
| CT-54 | O componente edit grava a troca de gestor e também salva sem alteração | R16 | EP de formulário; rastreio da gravação | Administração de centros | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-57, M-58 |
| CT-55 | O usuário comum não grava administração do centro por fora do componente | R17 | matriz papel × ação; tabela de decisão; ação fora da UI | Autorização de administração | Pest feature HTTP | `tests/Feature/AprovacaoCompra/PermissoesTest.php` | M-60 |
| CT-56 | O formulário forjado não permite ao usuário comum trocar gestor | R17 | matriz papel × ação; tabela de decisão; ação fora da UI | Administração de centros | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/CentrosCustoTest.php` | M-60 |
| CT-57 | O papel diretor acordado abre a compra no painel da sua organização | R17 | matriz papel × ação; tabela de decisão; ação fora da UI | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-62 |
| CT-58 | Uma solicitação de outra organização não pode ser lida ou alterada pelo ID conhecido | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-63 |
| CT-59 | O identificador conhecido não torna o centro estrangeiro administrável | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-63 |
| CT-60 | A etapa histórica não ganha acesso independente pelo ID da filha | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-63 |
| CT-61 | Um centro estrangeiro não entra na solicitação por payload válido nos demais campos | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-64 |
| CT-62 | Campos do servidor não são escolhidos pelo payload do cliente | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-65 |
| CT-63 | Um componente de usuário sem organização não entrega a base global | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Componentes com tenancy | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` | M-66 |
| CT-64 | A recusa de um ID estrangeiro deixa alcançável a consulta legítima do usuário | R18 | IDOR por entidade; mass assignment por entidade; EP de referência e discriminante | Fronteira da organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/IsolamentoTest.php` | M-67 |

## Revisão Adversarial

**PENDENTE.** Há áreas completas e Impacto 3; a revisão é obrigatória e não foi feita pelo derivador. A sessão principal reservará um contexto novo depois desta entrega preliminar. Não há achados comprovados nem rodadas concluídas nesta etapa; isso não equivale a uma revisão com zero achados.

| Campo | Registro preliminar |
|---|---|
| Host/rota prevista | Codex, sub-agente independente via collaboration; .claude/agents/fw-adversario-ct.md não existe nesta cópia. O roteiro de .ai/skills/feature-test-design/agents/fw-adversario-ct.md foi lido |
| Modelo | mesmo modelo herdado, exposto como GPT-6; ID exato de implantação não informado. Não há rota Claude/Opus neste host |
| Entrada autorizada para o adversário | somente 00 do oráculo, 04 e 05 desta saída. Glossário ausente. Não passar 01, implementação, outra saída ou relatórios |
| Cegueira e restrições efetivas | contexto novo, sem histórico da derivação, por despacho da sessão principal. O ambiente tem ferramentas gerais e acesso de filesystem irrestrito; a restrição de leitura é instrução, não sandbox mecânico. Nenhum hook, read-only ou git status foi usado como prova de isolamento |
| Rodadas / fechamento | 0 concluídas; despacho e achados pendentes. Após o retorno independente, a sessão fecha cada achado como cenário novo, oráculo reescrito, lacuna ou refutado com evidência; confirma o fechamento sem autorrevisão |
| Limite de esforço | ultra solicitado; tokens, custo e DDR não medidos. Nenhuma quota de achados e nenhum achado fabricado |
| 03 | não criado; despachos/degradações ficam neste registro e no retorno-c2.md |

## Referências Abertas

As duas SKILL foram lidas integralmente. Lista de referências efetivamente abertas, com motivo de acionamento; nenhuma pasta references inteira foi varrida por conveniência.

| Skill | Arquivo relativo à pasta da skill | Passo/motivo |
|---|---|---|
| feature-wiki | references/delegacao-casos-de-teste.md | step 7, contrato da delegação CT |
| feature-wiki | references/roteamento-e-despacho.md | step 7, rota e despachos |
| feature-wiki | references/ponytail-caveman.md | contrato de início e esforço da sessão |
| feature-wiki | references/citacoes-de-codigo.md | citações de costura/API |
| feature-wiki | references/template-03-progresso.md | registro de despacho/degradação no retorno, sem criar 03 |
| feature-wiki | references/playwright-mcp.md | planejamento de localizadores; MCP não foi executado |
| feature-test-design | references/template-04.md | passos 2/6/7 e estrutura do 04 |
| feature-test-design | references/escolha-de-camada.md | passos 2/7, camada e custo |
| feature-test-design | references/tecnicas-por-regra.md | passo 3, técnicas formais |
| feature-test-design | references/taxonomia-de-defeito.md | passo 4, checklist por item/entidade |
| feature-test-design | references/gherkin.md | passo 5, exemplos e vocabulário |
| feature-test-design | references/armadilhas-de-api.md | passos 5/7, APIs da stack |
| feature-test-design | references/mutation-testing.md | passo 6, gate e plano de medição |
| feature-test-design | references/revisao-adversarial.md | revisão independente e fechamento |
| feature-test-design | references/template-05.md | gate do browser e estrutura do 05 |
| feature-test-design | references/pest-plugin-browser.md | escrita dos CT-B e limites do plugin |

Leituras adicionais pertinentes: AGENTS.md do projeto; regras de testes/Filament/browser; convenções da wiki; arnês Pest e TestCase/TenancyTestCase; dois testes Kit de referência sem compra; factories User/Tenant; trait de tenancy; manifests, configuração de testes e APIs do vendor. Os arquivos 00/01 são imutáveis. Não foram consultados implementação da compra, Exp*, outras saídas, catálogo, veredito ou relatório de rodada.

## Estado da Entrega

Especificação preliminar completa em conteúdo, com revisão independente pendente. Testes Pest, browser, mutation testing, concorrência, build e Playwright não executados. Nenhuma migration, model, resource, service ou teste foi criado. Nenhum arquivo fora desta pasta de saída foi alterado. As lacunas declaradas não são coberturas alegadas.

