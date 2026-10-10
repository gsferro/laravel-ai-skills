# Casos de Teste — FERRO-812: Cupons de desconto

> Requisito: `../../oraculo/cupons-de-desconto/00-requisito.md` · Plano: `../../oraculo/cupons-de-desconto/01-plano-acao.md`.
> **Derivado do requisito, não do plano.** A implementação desta feature não foi lida.
> feature-wiki **4.0.0** · feature-test-design **1.16.0** · Codex / GPT-6 (ultra), 2026-10-09.
> **Revisão adversarial: CONCLUÍDA — duas rodadas independentes, 11 + 5 achados com destinos registrados.**
> Débito D-01: CT-51 e alterações do fechamento final não receberam nova avaliação independente; teto de duas rodadas atingido. Não há declaração de cobertura aprovada.
> Entrega de especificação; nenhum cenário, concorrência, browser ou mutation score foi executado.

## Perfil de Derivação

| Área | P | I | P×I | Perfil | Fundamentação |
|---|---|---|---|---|---|
| CRUD | 2 | 2 | 4 | padrão | integra formulário/painel; falha exige retrabalho |
| Validação | 3 | 3 | 9 | completo | domínio condicionado, unicidade e dado de outra organização |
| Autorização | 3 | 3 | 9 | completo | papel, ação, organização, nulo e reidratação; autorização |
| Elegibilidade | 3 | 3 | 9 | completo | condições combinadas e consumo concorrente; dinheiro |
| Cálculo | 2 | 3 | 6 | padrão | regra integrada ao motor; dinheiro |
| Auditoria e consumo | 3 | 3 | 9 | completo | efeitos e falhas transacionais; rastreabilidade e dinheiro |
| UI no navegador | 2 | 2 | 4 | padrão | tipo altera formulário reativo; retrabalho |

Perfis **decididos pelo passo 0**, nenhum imposto. Impacto 3 em validação, autorização, elegibilidade, cálculo e auditoria/consumo. Revisão de todo o conjunto obrigatória. Todas as áreas percorrem 1–7; completo usa BVA 3-valores, decisão completa e células inválidas da matriz. Cálculo escala BVA de 2 para **3 valores**: a borda de centavo precisa distinguir truncamento, arredondamento e piso zero. Pairwise não reduz a decisão de atividade nem a matriz de autorização: células críticas inteiras. SFDIPOT e taxonomia foram percorridos antes da escrita; mapa e costuras precedem os cenários.

Cenários: 51 · Regras: 17 · Mutantes previstos: 77 · Sem matador: 0. Contagens por `rg --count` com as quatro expressões do template-04; “Esquema” conta 1. CT-B são contados separadamente no 05. O padrão “sem matador” teve zero correspondências; as seis lacunas do requisito e da prova continuam declaradas, além do débito de revisão D-01. São matadores previstos na especificação, não mutantes executados ou medidos.

## Varredura SFDIPOT

| Letra | Dimensão desta feature | Cenários / destino |
|---|---|---|
| S | Cupom, enum, CupomUso, resource e permissões; duas entidades persistidas | CT-01–17, CT-36–43, CT-48–51; falta 02 declarada |
| F | CRUD, restrição administrativa, listar ativos, aplicar, contar e registrar autoria/instante | R1–R17 |
| D | centavos, inteiro percentual, organização, código exato, tipos inválidos, dados legados, 0/1/10/11 registros | CT-05–13, CT-22–24, CT-31–34 |
| I | GET de painel, create/save/action Livewire e motor chamado diretamente; sem endpoint de checkout | CT-01–21, CT-25–45 |
| P | Laravel/Filament/Livewire/Pest instalados; SQLite em memória do arnês não compartilha concorrência | CT-30 exige DB temporário compartilhado; APIs conferidas no vendor |
| O | cinco papéis, pares acumulados, dois tenants, revogação, uso abusivo e troca de contexto | CT-14–24, CT-42–45 |
| T | segundo da expiração, fuso local/UTC, objeto antigo, concorrência, rollback e histórico anterior | CT-25–30, CT-37–41 |

Nenhuma dimensão foi descartada silenciosamente. DST de outro fuso, volumes de produção e custo de query não têm regra de aceitação neste requisito; não foram medidos.

## Matriz única de estado × operação

Montada a partir do estado **derivado** P-03 e das operações efetivamente expostas, antes do mapa de regras. Não há coluna `situacao` a forçar. Cinco estados × quatro operações = **20 células**: 10 positivas e 10 negativas. Ausência na listagem é leitura sem ocorrência, não erro HTTP. Persona: listagem `panel_user`; demais colunas administradora da organização. A matriz papel×ação de R5 adiciona a dimensão persona, inclusive todos os pares. A dimensão campo fora do estado inicial é `valor`, junto de validade/limite válidos em CT-03. No estado removido a edição conserva SENTINELA/10.

| Estado de partida | Listar usuário comum | Editar administradora | Excluir administradora | Aplicar motor |
|---|---|---|---|---|
| ativo | ✅ CT-22/23 | ✅ CT-03 | ✅ CT-04 | ✅ CT-25/28/35 |
| expirado, ainda com saldo | ❌ CT-22 | ✅ CT-03 | ✅ CT-04 | ❌ CT-25/33 |
| esgotado, ainda no prazo | ❌ CT-22 | ✅ CT-03 | ✅ CT-04 | ❌ CT-28/33 |
| expirado e esgotado | ❌ CT-22 | ✅ CT-03 | ✅ CT-04 | ❌ CT-33, linha adicional abaixo |
| removido | ❌ CT-04 (consultar por código após excluir) | ❌ CT-40 | ❌ CT-40 | ❌ CT-41 |

Auditoria da legenda: aplicar recusado conserva contador e cada linha de cupom_usos e não devolve desconto; editar recusado conserva atributos/contador/trilha e não recria; excluir repetido não elimina SENTINELA nem cria aplicação. Consulta ausente conserva dados. Sucesso de edição altera valor e rederiva atividade sem consumir; exclusão impede uso por objeto retido. Excluir um cupom usado não destrói imediatamente a possibilidade de auditar suas aplicações: CT-49, RQ-15. Prazo futuro de retenção e exclusão de usuário continuam lacuna L6, sem oráculo inventado.

A célula removido×listar deve executar efetivamente `ListCupons`, não herdar a busca do CT-04: ver CT-46 em R7. A célula duplamente inválida×aplicar é CT-47 em R11; esses cenários são exigidos pela matriz e não por partição inválida isolada. A técnica EP continua isolando inválidos nas demais linhas.

## Mapa de Regras

| Regra | Área (perfil herdado) | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — O painel permite cadastrar, editar e excluir cupons | CRUD (padrão) | RQ-01, RQ-05, RQ-06, P-02, P-09; premissa temporal do 00 | EP; par visita/gravação; conversão data→instante | CT-01, CT-02, CT-03, CT-04, CT-50 |
| R2 — O tipo admite exclusivamente porcentagem e fixo | Validação (completo) | RQ-03, P-05 | EP em criação, edição e domínio | CT-05, CT-06, CT-07 |
| R3 — Percentual é inteiro de 1 a 100 e fixo usa centavos | Validação (completo) | P-05 | EP; BVA 3-valores; domínio condicionado | CT-08, CT-09, CT-10 |
| R4 — O mesmo código exato é único no contexto de negócio | Validação (completo) | RQ-14, P-04 | Identidade; criação/edição/uso; BVA cardinalidade | CT-11, CT-12, CT-13 |
| R5 — Somente administradores executam cada operação de escrita | Autorização (completo) | RQ-07, RQ-08, P-02 | Matriz papel×ação×superfície; papel acumulado×ordem; revogação | CT-14, CT-15, CT-16, CT-17, CT-48 |
| R6 — O contexto de organização limita leitura e escrita | Autorização (completo) | RQ-01, RQ-07, RQ-08, RQ-12, RQ-13, RQ-15, P-01, P-02, P-04 | IDOR; discriminante nulo; identidade×contexto no sucesso | CT-18, CT-19, CT-20, CT-21, CT-51 |
| R7 — O usuário comum lista somente cupons ativos do seu contexto | Elegibilidade (completo) | RQ-08, P-03, P-02 | Tabela de decisão completa; EP; paginação | CT-22, CT-23, CT-24, CT-46 |
| R8 — A validade é conferida no instante efetivo da aplicação | Elegibilidade (completo) | RQ-10, P-03, P-01 | BVA 3-valores; tempo; TOCTOU | CT-25, CT-26, CT-27 |
| R9 — O limite é respeitado na leitura, no uso e na concorrência | Elegibilidade (completo) | RQ-11, RQ-13, P-01 | BVA 3-valores; TOCTOU; concorrência | CT-28, CT-29, CT-30 |
| R10 — O retorno representa o total após desconto em centavos | Cálculo (padrão) | RQ-12, P-01, P-05, P-06, P-07 | EP; BVA 3-valores escalado; exemplo discriminante | CT-31, CT-32 |
| R11 — Existe cupom válido e coerente antes de qualquer efeito | Elegibilidade (completo) | RQ-09, RQ-10, RQ-11, RQ-12, RQ-13, RQ-15, P-05 | EP isolada; defesa no uso; não-efeito | CT-33, CT-34, CT-47 |
| R12 — Cada aplicação aceita consome exatamente um uso | Auditoria e consumo (completo) | RQ-13, P-01 | Rastreio de efeito por partição | CT-35 |
| R13 — A trilha própria identifica a pessoa e o instante reais | Auditoria e consumo (completo) | RQ-15, P-08, P-01 | Rastreio: acontece; não acontece; uma vez; atomicidade; alvo×não-alvo; guard×argumento; uso→exclusão | CT-36, CT-37, CT-38, CT-39, CT-49 |
| R14 — O cupom removido não volta a funcionar por objeto antigo | Elegibilidade (completo) | RQ-01, RQ-07, RQ-09, P-03 | Estado×operação; chave inexistente; 2-switch | CT-40, CT-41 |
| R15 — Payload não escolhe organização, identidade nem contador | Autorização (completo) | RQ-07, RQ-13, P-02, P-08 | Mass assignment por entidade; criação/edição | CT-42, CT-43 |
| R16 — O estado do framework não reabre a consulta do usuário | Autorização (completo) | RQ-08, P-02, P-03 | Superfície Livewire; domínio e tipo inválidos | CT-44, CT-45 |
| R17 — O navegador mostra a unidade e a correção da seleção de tipo | UI no navegador (padrão) | RQ-01, RQ-03, P-05 | EP do discriminador; reatividade observável | CT-B01, CT-B02 |

Recortes com decisão ainda não determinada na entrada somente leitura. O 00 não marcou nenhuma RQ inteira aberta; os estados abaixo registram perguntas desta derivação somente para o recorte citado. O restante da cláusula e as premissas dadas continuam fechados, com os invariantes discriminados:

- **RQ-02 — aberta (Q1), sem cenário até a resposta**, apenas no recorte de teto e domínio textual; códigos concretos são fixtures das regras fechadas de identidade e gravação do código informado.
- **RQ-04 — aberta (Q4), sem cenário até a resposta**, apenas no recorte de mínimo/máximo do fixo; persistir o valor válido informado continua fechado. P-05 continua vigente e independente, com percentual inteiro 1–100 e centavos.
- **RQ-05 — aberta (Q2), sem cenário até a resposta**, apenas no recorte de aceitar validade passada na gravação. Persistir a validade válida informada e converter uma entrada somente data em 23:59:59 são invariantes fechados: CT-50. RQ-10 permanece fechada, com recusa no uso e borda `> now()` dada pelo 00.
- **RQ-06 — aberta (Q3), sem cenário até a resposta**, apenas no recorte de limites 0/negativo/fracionário ou abaixo dos usos na gravação. Guardar exatamente o limite válido informado é fechado: CT-02/03. RQ-11/RQ-13 permanecem fechadas, com comparação de disponibilidade e contador preservado.

Desvio explícito: o 00 não possui coluna Estado nem seção Premissas do template atual; esta execução toma P-01–P-09 de A-01–A-09 como dadas. Não reabre as cinco perguntas originais já resolvidas por premissa. As novas perguntas ficam aqui, sem alterar o oráculo imutável. Nenhum cenário afirma uma direção das decisões Q1–Q4. RQ-05/06 são origem apenas dos invariantes fechados de gravação, não dos domínios pendentes. Todas as RQ fechadas aparecem no mapa e todas as P vigentes são rastreadas: P-01 R8–R13; P-02 R1/R5–R7/R15–R16; P-03 R7/R8/R14; P-04 R4/R6; P-05 R2/R3/R10/R11/R17; P-06/P-07 R10; P-08 R13/R15; P-09 R1.

## Costuras de Teste

| Grupo | Regras | Costura | Existente ou nova | Por quê | Confirmada |
|---|---|---|---|---|---|
| G-C | R1–R7, R14–R16 | componente Livewire/Filament | existente — testes de edição e tenancy | campos, gravação, ação e recorte são observáveis pelo componente | proposta da derivação; usuário indisponível |
| G-D | R2–R6, R13, R15 | Pest feature HTTP | existente — chamadas diretas na suíte Kit/Tenancy | prova autorização/validação além do formulário e conservação imediata da auditoria na exclusão | proposta da derivação; usuário indisponível |
| G-A | R6, R8–R14 | Pest feature HTTP | existente — container/DB no arnês Kit/Tenancy | aplicarEm é o contrato dado em P-01 e persiste efeitos | proposta da derivação; usuário indisponível |
| G-X | R9 | Pest feature HTTP | nova para concorrência real; memória não é compartilhada | duas conexões/processos e banco temporário comum; barreira observável | proposta da derivação; usuário indisponível |
| G-B | R17 | browser | existente — BrowserTenancy | unidade/erro visíveis depois de alteração real em JS | proposta da derivação; usuário indisponível |

**Não confirmadas por desenvolvedor**: não simular aprovação. O prompt manda avançar sem perguntar; desenho proposto como `@premissa` de arnês. O orquestrador deverá confirmar as costuras antes da materialização. Gate do 05 satisfeito por G-B e pelas telas create/edit da Superfície de UI. A técnica de cálculo fica em Feature: `tests/Unit` não recebe TestCase/container e o único contrato do 00 é `aplicarEm`, com escrita. Não inventar uma função pura só para baixar camada.

## Fronteira com o Plano

| Item lido no 01 | Uso permitido / recusado como oráculo | Destino |
|---|---|---|
| paths Cupom, CupomUso, TipoDeDesconto e Pages; rotas `/app/{tenant}/cupons`, create/edit; UUID | localização/superfície, sem behavior derivado | setup e índice |
| tipos de testes Kit/Tenancy/BrowserTenancy | escolha de arquivo | índice, pendentes de materialização |
| `descontoSobre()`, nullable User e retorno null de `valido()` | escolhas do plano; não são o contrato normativo do 00 | sem cenário exclusivo; não assumir autor opcional |
| código em maiúsculas, trim, maxLength 40 | 00 não estabelece canonicalização/teto | Q1; não usar 40 como aceite |
| minValue 1 para fixo/limite; minDate no create/save | comportamentos que 00 não determina | Q2–Q4 |
| prioridade dos badges Esgotado/Expirado e textos de erro | rótulos/ordem do plano não são norma | não afirmar literais nem prioridade |
| logs e channel cupom | RQ-15 pede registro, não linha de log | fora dos CT; trilha própria por P-08 |
| cascadeOnDelete da trilha e nullOnDelete da autoria | não autorizam perder prova de auditoria; exclusão imediata do cupom é CT-49 por RQ-15 | L6 só para prazo futuro e remoção de usuário |
| `getEloquentQuery()` / filtro do Resource | localização, não prova de proteção do motor/child | CT-20/21/43 e lacuna do 02 |
| rótulos concretos do valor no formulário | seletores são detalhe; oráculo semântico é a unidade de P-05 | CT-B01 verifica percentual/centavos, sem impor frase do PRD |

## Perguntas para o 00-requisito.md

Bloco para colagem; 00 imutável nesta rodada. Não perguntar ao usuário nesta execução.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | Qual teto e quais caracteres definem o código; caixa, espaços nas bordas e Unicode mudam sua identidade? | RQ-02 | Definir contrato textual explícito e validação na gravação e no uso; não assumir o 40/trim/maiúsculas do PRD | aberta |
| Q2 | Cadastrar ou editar validade já passada/no instante atual é permitido? | RQ-05 | Recusar por falha fechado; independentemente disso RQ-10 recusa cupom vencido no uso | aberta |
| Q3 | Limite 0, negativo, fracionário ou redução abaixo dos usos reais podem ser gravados? | RQ-06 | Recusar por falha fechado; contador e trilha não são corrigidos/truncados, qualquer que seja a resposta | aberta |
| Q4 | O fixo admite zero e qual o domínio máximo de centavos/total? | RQ-04 | Definir limites e recusar fora deles; não assumir minValue 1 ou largura do banco como negócio | aberta |

❓ Q1 · raia: requisito · afeta: RQ-02 · depende de: — → tabela acima.
➡️ Recomendação: especificar o domínio antes do teste de n/n+1; o teto do plano não vira requisito.
❓ Q2 · raia: requisito · afeta: RQ-05 · depende de: — → tabela acima.
➡️ Recomendação: recusar por falha fechado; CT-25/26/33 provam o invariante do uso.
❓ Q3 · raia: requisito · afeta: RQ-06 · depende de: — → tabela acima.
➡️ Recomendação: recusar por falha fechado; não alterar contabilidade histórica.
❓ Q4 · raia: requisito · afeta: RQ-04 · depende de: — → tabela acima.
➡️ Recomendação: definir e validar a faixa; não conceder crédito negativo nem truncar valor fracionário.

## Setup Global

- **Stack instalado**, de `vendor/composer/installed.json`: Laravel 13.25.0, Filament 5.7.6, Livewire 4.4.0, Pest 5.1.1, browser 5.0.1, mutate 5.0.2. `composer.json` declara browser; mutate existe no vendor mas não é dependência direta: degradação de distribuição, sem instalar pacote nesta execução.
- `tests/Pest.php` liga TestCase+RefreshDatabase em Feature/Kit e TenancyTestCase+RefreshDatabase em Tenancy/BrowserTenancy. `phpunit.xml` declara Browser, SQLite :memory:; browser timeout 20000ms. A rule testes-browser vence o comando genérico `--parallel --tia`: futuras execuções separam backend e browser em série.
- Personas por `usuarioComPapel()`, `papelNaOrganizacao()`, `usuarioDoKit()`, `noPainelDa()`; Acme/Globex distintos, usuários Ana/Beto distintos, attach de membership. Seeder de permissões antes do de papéis na futura materialização; **nenhum Artisan executado nesta cópia**.
- P-02 do 00 concede herança administrativa também ao papel admin. A tabela do 01 que o exclui do /app não é oráculo; CT-15 e CT-48 seguem o 00, no domínio e no painel. Não apagar essa divergência para reproduzir o plano.
- TenantFactory/UserFactory existem; **CupomFactory não existe** nesta entrada. Criar fixture Cupom com dados válidos na futura suíte, sem inventar factory instalada. Helper compartilhado novo, se necessário, viverá em tests/Pest.php conforme rule; nesta entrega nenhum helper é criado.
- Estado ativo: cadastro com expiração futura e saldo. Esgotado: aplicações reais até o limite. Expirado: avanço controlado do relógio, não status gravado. Expirado/esgotado: consumo real e avanço. Removido: exclusão real. A transição prepara contador/trilha; snapshot é tomado **depois do setup**, antes da ação.
- Entradas legadas fora do domínio (usos > limite, percentual 0/101, tenant nulo) são fixtures inválidas deliberadas inseridas por via técnica para testar leitura/uso; não afirmam que o cadastro aceita esses valores. Tipo “campo ausente”, null, "" e array são valores de payload, não strings literais correspondentes.
- Percentual válido de aplicação é 10 e fixo 1000, salvo linhas que fixam outros números. Todas as aplicações recusadas têm ator, alvo e trilha anteriores reais quando o cupom existe. Total sempre inteiro em centavos.
- A fração percentual `12,5` nos exemplos usa notação pt-BR para o número 12.5. CT-10 fornece essa fração numérica (ou a string numérica `12.5`) à escrita direta, não texto não numérico com vírgula: a única invalidade é não ser inteiro, ainda estando entre 1 e 100. No formulário, usar a representação aceita pelo campo da aplicação. Nenhum exemplo monetário usa float.
- G-D resolve a mesma escrita de domínio usada pelo CRUD, chama create/update/delete diretamente com ator/contexto autenticado e afirma o banco; **não usar Gate::allows/can sozinho**. Se a aplicação não tiver uma via capaz de expressar esse contrato, registrar lacuna em vez de construir um wrapper de teste que reaplique a regra.
- CT-17 usa os mesmos dois papéis reais em ambas as ordens, em execuções com snapshots independentes. O arnês deve conferir a ordem efetivamente enumerada ao consumidor de autorização; inverter somente attach sem conferir a ordem não prova o cenário. Se necessário, reordenar a relação carregada com os mesmos objetos de papéis reais, sem fakear Gate, policy ou permissões. Esse mecanismo de arnês não altera o comportamento esperado.
- Clock com `travelTo()` em closure/`travelBack()`. Não usar Event::fake global antes das fixtures; não fingir aplicação para preparar os estados. Não fakear a tabela auditada. Falhas CT-38/39 por callback de inserção/created de CupomUso ou constraint controlada: verificar que alcançaram o ponto indicado antes de aceitar o não-efeito.
- G-X requer duas execuções e conexões próprias, fixture commitada em banco descartável compartilhado, barreira antes do consumo, coleta de ambos retornos e releitura por conexão independente. Banco apenas em memória e duas chamadas sequenciais **não provam concorrência**. Mecanismo proposto, não tentado nesta rodada sem implementação.
- CT-23, CT-37 e CT-51 controlam a posição discriminante dos registros no arnês. A ordem de criação isolada pode não ser a ordem da consulta, especialmente com UUID: comprovar a configuração real indicada antes da ação. O controle da fixture/ordem não é requisito novo de ordenação de negócio nem substitui o recorte da aplicação.
- APIs conferidas: `Livewire::test`, `fillForm`, `call('create'|'save')`, `assertHasFormErrors`, `loadTable`, `assertCanSeeTableRecords`, `callAction(TestAction::make('delete')->table($record))`, `assertSchemaStateSet`. `assertFormSet`, `callTableAction`, `assertTableActionExists` são deprecated nos stubs; não usar.
- Evidências de superfície conferidas no vendor: `vendor/filament/tables/src/Concerns/CanSortRecords.php:sortTable():11`; `vendor/filament/tables/src/Concerns/CanSearchRecords.php:getTableSearch():207`; `vendor/filament/filament/src/Resources/Pages/CreateRecord.php:create():92`; `vendor/filament/filament/src/Resources/Pages/EditRecord.php:save():159`; `vendor/filament/filament/src/Resources/Pages/Concerns/InteractsWithRecord.php:$record:17` sob #[Locked] na linha anterior. CT-45 testa como se a trava faltasse, sem usar a negativa para dispensar cenário.
- **02 ausente**: não foi criado. Esses greps não substituem o inventário obrigatório da superfície final; métodos/propriedades/filtros do código novo e de todos os vendors consumidos continuam lacuna L5.

## Regra R1 — O painel permite cadastrar, editar e excluir cupons

> Origem: RQ-01, RQ-05, RQ-06, P-02, P-09; premissa temporal expressa no 00 · CRUD (padrão) · técnica: **EP; par visita/gravação; conversão data→instante**. Q2/Q3 não impedem conferir a persistência de valores válidos.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O painel permite cadastrar, editar e excluir cupons

    Esquema do Cenário: [CT-01] As telas de escrita oferecem o tipo e a unidade do valor
      Dado a administradora da organização Acme e um cupom ativo PERCENT10 existente
      Quando a administradora visita a tela de <operacao>
      Então o formulário oferece seleção dos dois tipos e valor na unidade definida por P-05
      E os dados do cupom existente não são modificados pela visita

      Exemplos:
        | operacao | # partição |
        | criar    | cadastro   |
        | editar   | edição     |

    Esquema do Cenário: [CT-02] O formulário de criação persiste os dois tipos
      Dado a administradora da Acme e nenhum cupom com o código NOVO na Acme
      Quando a administradora cadastra NOVO pelo formulário com tipo <tipo>, valor <valor>, validade futura e limite 3
      Então existe exatamente um NOVO da Acme com tipo <tipo>, valor <valor> e limite persistido exatamente 3
      E o contador persistido começa em 0 e a operação não cria linha em cupom_usos

      Exemplos:
        | tipo        | valor | # partição |
        | porcentagem | 29    | percentual |
        | fixo        | 1000  | centavos   |

    Esquema do Cenário: [CT-03] O formulário de edição grava sem consumir uso
      Dado a administradora da Acme e um cupom <estado> de valor 10 com 2 usos reais e 2 linhas de cupom_usos
      Quando a administradora salva o formulário com valor 29, validade futura e limite 5
      Então o mesmo cupom conserva código e organização e tem valor persistido 29, limite persistido exatamente 5 e volta a ser localizado como ativo
      E os 2 usos e as 2 linhas de cupom_usos permanecem inalterados

      Exemplos:
        | estado            | # partição                 |
        | ativo             | futuro e limite 3          |
        | expirado          | passado e limite 3         |
        | esgotado          | futuro e limite 2          |
        | expirado_esgotado | passado e limite 2         |

    Esquema do Cenário: [CT-04] A exclusão autorizada remove o cupom
      Dado a administradora da Acme, um cupom <estado> pertencente à Acme e um SENTINELA ativo de valor 10
      Quando a administradora confirma a exclusão do cupom na ação da tabela
      Então o cupom não é mais localizado por código nem por sua chave
      E SENTINELA permanece com valor 10 e contador 0

      Exemplos:
        | estado            | # partição                            |
        | ativo             | futuro e usos 0 de 3                  |
        | expirado          | passado e usos 0 de 3                 |
        | esgotado          | futuro e 2 usos reais de limite 2      |
        | expirado_esgotado | passado e 2 usos reais de limite 2     |

    Esquema do Cenário: [CT-50] A entrada somente data persiste a validade no fim do dia escolhido
      Dado a administradora da Acme, o relógio em 2026-10-09T12:00:00-03:00 e formulário de <operacao> que oferece validade somente como data
      E o fuso da aplicação é America/Sao_Paulo e o alvo da edição tem validade 2026-10-12T23:59:59-03:00, contador 1 e sua linha anterior de cupom_usos
      Quando a administradora grava os demais dados válidos com a data de validade 2026-10-10
      Então o cupom recarregado tem validade exatamente 2026-10-10T23:59:59-03:00, o mesmo instante de 2026-10-11T02:59:59Z
      E a gravação conserva contador e trilha anteriores na edição ou mantém contador 0 e nenhuma aplicação na criação

      Exemplos:
        | operacao | # fronteira |
        | criar    | data da tela → instante persistido |
        | editar   | substituição da data → instante persistido |
```

CT-50 tem guarda explícita na entrada: aplica-se quando a superfície materializada oferece somente data, como a premissa do 00 determina. Se a UI oferecer data e hora, não a obrigar a ocultar a hora nem marcar CT-50 verde por omissão: registrar não aplicável e conferir a gravação do instante válido informado no par CT-02/03. O valor futuro em CT-50 não responde Q2.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Criar aceita os campos mas descarta tipo ou valor | CT-02 | NOVO persiste com porcentagem/29 ou fixo/1000, não com defaults |
| M-02 | Salvar executa apenas a validação e não atualiza o registro | CT-03 | O valor persistido muda de 10 para 29 |
| M-03 | A ação de exclusão só retira a linha da tabela | CT-04 | A busca persistida pela chave e pelo código não encontra o cupom |
| M-66 | As Pages existem mas as rotas create/edit não são registradas | CT-01 | GET das duas rotas apresenta o formulário, não uma página inexistente |
| M-68 — revisão adversarial ADV-02 | A gravação substitui qualquer limite informado por 3 | CT-03 | O limite recarregado é exatamente 5, não 3; contador e duas aplicações anteriores permanecem |
| M-70 — revisão adversarial ADV-03 | A entrada somente data é convertida para 00:00:00 | CT-50 | A validade recarregada é 23:59:59 no dia escolhido/fuso da aplicação, não 00:00:00 |

---

## Regra R2 — O tipo admite exclusivamente porcentagem e fixo

> Origem: RQ-03, P-05 · Validação (completo) · técnica: **EP em criação, edição e domínio**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O tipo admite exclusivamente porcentagem e fixo

    Esquema do Cenário: [CT-05] A criação recusa cada tipo inválido isoladamente
      Dado a administradora da Acme e os demais atributos válidos de NOVO
      Quando a administradora envia a criação com tipo <tipo>
      Então há recusa de validação do tipo e não existe NOVO persistido
      E não há consumo de uso nem nova linha em cupom_usos

      Exemplos:
        | tipo             | # partição             |
        | frete_gratis     | terceiro tipo          |
        | null             | tipo nulo              |
        | ""               | tipo vazio             |
        | campo ausente    | tipo ausente           |

    Esquema do Cenário: [CT-06] A edição recusa cada tipo inválido sem alterar o cupom
      Dado um cupom ativo porcentagem/29 da Acme com 1 uso e 1 linha de cupom_usos e a administradora da Acme
      Quando a administradora salva o formulário com tipo <tipo> e os demais atributos válidos
      Então o tipo persistido continua porcentagem e o valor continua 29
      E a edição é recusada e o contador 1 e a linha de cupom_usos permanecem

      Exemplos:
        | tipo          | # partição       |
        | frete_gratis  | terceiro tipo    |
        | null          | nulo             |
        | ""            | vazio            |
        | campo ausente | ausente          |

    Esquema do Cenário: [CT-07] O domínio não grava terceiro tipo fora do formulário
      Dado a administradora da Acme e um cupom ativo porcentagem/29 para edição
      Quando a administradora executa diretamente a escrita de <operacao> com tipo frete_gratis e demais atributos válidos
      Então a escrita é recusada sem persistir tipo frete_gratis
      E o cupom anterior, seu contador e suas linhas de cupom_usos permanecem iguais

      Exemplos:
        | operacao | # partição |
        | criar    | cadastro   |
        | editar   | edição     |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-04 | A lista aceita um terceiro tipo por validação apenas de presença | CT-05 | frete_gratis é recusado e NOVO não existe |
| M-05 | A restrição do tipo só é aplicada no cadastro | CT-06 | Após salvar frete_gratis o registro continua porcentagem/29 |
| M-06 | A restrição existe apenas no Select | CT-07 | A escrita direta recusa frete_gratis e não armazena o valor inválido |

---

## Regra R3 — Percentual é inteiro de 1 a 100 e fixo usa centavos

> Origem: P-05 · Validação (completo) · técnica: **EP; BVA 3-valores; domínio condicionado**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: Percentual é inteiro de 1 a 100 e fixo usa centavos

    Esquema do Cenário: [CT-08] O cadastro respeita a fronteira específica do tipo
      Dado a administradora da Acme e os demais atributos válidos de NOVO
      Quando a administradora cadastra NOVO com tipo <tipo> e valor <valor>
      Então o resultado é <resultado> e o valor persistido é <persistido>
      E o contador permanece 0 e nenhuma linha de cupom_usos é criada

      Exemplos:
        | tipo        | valor | resultado | persistido   | # partição       |
        | porcentagem | 0     | recusa    | nenhum NOVO  | borda inferior−1 |
        | porcentagem | 1     | aceita    | 1            | borda inferior   |
        | porcentagem | 2     | aceita    | 2            | borda inferior+1 |
        | porcentagem | 99    | aceita    | 99           | borda superior−1 |
        | porcentagem | 100   | aceita    | 100          | borda superior   |
        | porcentagem | 101   | recusa    | nenhum NOVO  | borda superior+1 |
        | porcentagem | 12,5  | recusa    | nenhum NOVO  | não inteiro      |
        | fixo        | 1     | aceita    | 1            | um centavo       |
        | fixo        | 101   | aceita    | 101          | teto % não se aplica |
        | fixo        | 1000  | aceita    | 1000         | mil centavos     |

    Esquema do Cenário: [CT-09] A edição revalida tipo e valor em conjunto
      Dado a administradora da Acme e um cupom ativo <tipo_inicial>/<valor_inicial> com 1 uso e sua linha de cupom_usos
      Quando a administradora salva o cupom com tipo <tipo_final> e valor <valor_final>
      Então o resultado é <resultado> e o registro persiste como <gravado>
      E contador e linha de cupom_usos permanecem iguais ao Dado

      Exemplos:
        | tipo_inicial | valor_inicial | tipo_final  | valor_final | resultado | gravado         | # partição |
        | porcentagem  | 29            | porcentagem | 0           | recusa    | porcentagem/29  | inferior−1 |
        | porcentagem  | 29            | porcentagem | 1           | aceita    | porcentagem/1   | inferior   |
        | porcentagem  | 29            | porcentagem | 2           | aceita    | porcentagem/2   | inferior+1 |
        | porcentagem  | 29            | porcentagem | 99          | aceita    | porcentagem/99  | superior−1 |
        | porcentagem  | 29            | porcentagem | 100         | aceita    | porcentagem/100 | superior   |
        | porcentagem  | 29            | porcentagem | 101         | recusa    | porcentagem/29  | superior+1 |
        | porcentagem  | 29            | porcentagem | 12,5        | recusa    | porcentagem/29  | fracionário |
        | fixo         | 1000          | porcentagem | 1000        | recusa    | fixo/1000       | teto reativado |
        | porcentagem  | 29            | fixo        | 1000        | aceita    | fixo/1000       | teto removido |

    Esquema do Cenário: [CT-10] O percentual inválido é recusado também na escrita direta
      Dado a administradora da Acme e um cupom ativo porcentagem/29 existente com 1 uso e sua linha de cupom_usos
      Quando a administradora executa diretamente a escrita de <operacao> com percentual <valor> e os demais atributos válidos
      Então a escrita é recusada sem gravar o percentual inválido e sem acrescentar qualquer cupom
      E o cupom anterior conserva valor 29, contador 1 e a linha de cupom_usos

      Exemplos:
        | operacao | valor | # partição       |
        | criar    | 0     | inferior−1       |
        | criar    | 101   | superior+1       |
        | criar    | 12,5  | fração não inteira, demais atributos válidos |
        | editar   | 0     | inferior−1       |
        | editar   | 101   | superior+1       |
        | editar   | 12,5  | fração não inteira, demais atributos válidos |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-07 | Usa <100 e recusa o desconto total | CT-08 | porcentagem/100 é aceito e persiste 100 |
| M-08 | Aplica teto 100 também ao fixo | CT-08 | fixo/101 é aceito e persiste 101 |
| M-09 | Aceita 0 ou 101 como percentual | CT-08 | 0 e 101 recusados com ausência de NOVO |
| M-10 | Aceita decimal e o converte silenciosamente para inteiro | CT-09 | 12,5 é recusado e o valor anterior 29 permanece |
| M-11 | A regra do percentual só existe no formulário | CT-10 | Escrita direta de 0 ou 101 não persiste |
| M-71 — revisão adversarial ADV-06 | O domínio aceita percentual fracionário entre 1 e 100 e o converte em inteiro | CT-10 | Criar/editar diretamente com 12,5 recusa, não cria cupom e mantém o valor anterior 29 e seus efeitos |

---

## Regra R4 — O mesmo código exato é único no contexto de negócio

> Origem: RQ-14, P-04 · Validação (completo) · técnica: **Identidade; criação/edição/uso; BVA cardinalidade**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O mesmo código exato é único no contexto de negócio

    Esquema do Cenário: [CT-11] A criação distingue colisão local e código de outra organização
      Dado a administradora da Acme e PROMO10 ativo já cadastrado em <contexto_existente>
      Quando a administradora cadastra outro PROMO10 na Acme com demais atributos válidos
      Então o resultado é <resultado> e há <quantidade_acme> PROMO10 persistidos na Acme
      E o registro existente e suas linhas de cupom_usos permanecem inalterados

      Exemplos:
        | contexto_existente | resultado | quantidade_acme | # partição      |
        | Acme               | recusa    | 1               | colisão local   |
        | Globex             | aceita    | 1               | tenant diferente |
        | instalação sem tenancy | recusa | 1             | tenant_id nulo no modo single |

    Esquema do Cenário: [CT-12] A edição ignora o próprio código e recusa código de outro cupom local
      Dado a administradora da Acme, PROMO10 ativo na Acme e OUTRO ativo em <contexto_outro>
      Quando a administradora salva PROMO10 com código <novo_codigo> e valor 29
      Então o resultado é <resultado> e o mesmo registro persiste como <gravado>
      E o registro OUTRO conserva seu código, valor, contador e suas linhas de cupom_usos

      Exemplos:
        | contexto_outro | novo_codigo | resultado | gravado       | # partição        |
        | Acme           | PROMO10     | aceita    | PROMO10/29    | contra si mesmo   |
        | Acme           | OUTRO       | recusa    | PROMO10/10    | colisão local     |
        | Globex         | OUTRO       | aceita    | OUTRO/29      | outra organização |

    Esquema do Cenário: [CT-13] A unicidade impede duplicata pela via direta
      Dado a administradora e PROMO10 ativo no <modo>, além de OUTRO ativo para edição
      Quando a administradora executa diretamente <operacao> para gravar PROMO10 novamente no mesmo contexto
      Então a escrita é recusada e existe exatamente um PROMO10 nesse contexto
      E OUTRO e todos os contadores e registros de cupom_usos permanecem inalterados

      Exemplos:
        | modo         | operacao | # partição |
        | multi-tenant | criar    | criação local |
        | multi-tenant | editar   | edição local  |
        | single-tenant | criar   | chave com tenant nulo |
        | single-tenant | editar  | edição com tenant nulo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-12 | Valida o código globalmente em vez de por organização | CT-11 | Código da Globex não impede um PROMO10 na Acme |
| M-13 | Não ignora o próprio registro na edição | CT-12 | Salvar PROMO10 como PROMO10 com valor 29 é aceito |
| M-14 | Deixa duplicata com tenant_id NULL fora da tela | CT-13 | Single-tenant direto mantém exatamente um PROMO10 |
| M-15 | Aplica unicidade só na criação | CT-12 | Renomear para OUTRO da Acme é recusado e conserva PROMO10/10 |

---

## Regra R5 — Somente administradores executam cada operação de escrita

> Origem: RQ-07, RQ-08, P-02 · Autorização (completo) · técnica: **Matriz papel×ação; papel acumulado; revogação**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: Somente administradores executam cada operação de escrita

    Esquema do Cenário: [CT-14] O usuário comum e o perfil infra não escrevem por componente
      Dado um cupom ativo da Acme de valor 10, contador 1 e sua linha de cupom_usos e o ator <papel> na Acme
      Quando o ator tenta <acao> por chamada direta do componente
      Então a ação é negada sem novo cupom, sem mudar o valor 10 e sem remover o cupom alvo
      E o contador 1 e a linha de cupom_usos permanecem inalterados

      Exemplos:
        | papel      | acao   | # célula |
        | panel_user | criar  | usuário/criar |
        | panel_user | editar | usuário/editar |
        | panel_user | excluir | usuário/excluir |
        | infra      | criar  | infra/criar |
        | infra      | editar | infra/editar |
        | infra      | excluir | infra/excluir |

    Esquema do Cenário: [CT-15] O domínio aplica a matriz de autorização em cada verbo
      Dado o ator <papel> no contexto Acme e um cupom ativo de valor 10 com contador 1 e uma linha de cupom_usos
      Quando o ator executa diretamente <acao> pela via de escrita do domínio sem montar componente
      Então o resultado é <resultado> com <persistencia>
      E a operação não consome usos e não cria aplicação em cupom_usos

      Exemplos:
        | papel              | acao    | resultado | persistencia | # célula |
        | admin_organizacao  | criar   | aceita    | novo cupom com valor 29 | admin/criar |
        | admin_organizacao  | editar  | aceita    | alvo com valor 29      | admin/editar |
        | admin_organizacao  | excluir | aceita    | alvo ausente           | admin/excluir |
        | master_global      | criar   | aceita    | novo cupom com valor 29 | master/criar |
        | master_global      | editar  | aceita    | alvo com valor 29      | master/editar |
        | master_global      | excluir | aceita    | alvo ausente           | master/excluir |
        | admin              | criar   | aceita    | novo cupom com valor 29 | P-02 admin/criar |
        | admin              | editar  | aceita    | alvo com valor 29      | P-02 admin/editar |
        | admin              | excluir | aceita    | alvo ausente           | P-02 admin/excluir |
        | panel_user         | criar   | recusa    | nenhum novo cupom      | comum/criar |
        | panel_user         | editar  | recusa    | alvo com valor 10      | comum/editar |
        | panel_user         | excluir | recusa    | alvo existente valor 10 | comum/excluir |
        | infra              | criar   | recusa    | nenhum novo cupom      | infra/criar |
        | infra              | editar  | recusa    | alvo com valor 10      | infra/editar |
        | infra              | excluir | recusa    | alvo existente valor 10 | infra/excluir |

    Esquema do Cenário: [CT-16] A autorização é refeita depois da revogação
      Dado um componente de <acao> montado para a administradora da Acme e um cupom ativo de valor 10, contador 1 e sua linha de cupom_usos
      E o papel administrativo foi revogado antes do request da ação
      Quando a antiga administradora dispara <acao>
      Então a ação é negada sem criação, sem alterar valor 10 e sem excluir o alvo
      E contador e linha de cupom_usos permanecem como no Dado

      Exemplos:
        | acao    | # célula |
        | criar   | create depois de revogar |
        | editar  | save depois de revogar   |
        | excluir | delete depois de revogar |

    Esquema do Cenário: [CT-17] Papéis acumulados não anulam a autorização administrativa
      Dado o ator que acumula <par> na Acme, com os papéis efetivamente enumerados ao consumidor de autorização na ordem <ordem>
      E existe ALVO ativo local de valor 10, limite 3, contador 1 e uma aplicação real anterior, sem NOVO na Acme
      Quando o ator executa diretamente <acao> com dados válidos de NOVO ou ALVO porcentagem/29 e limite 3
      Então o resultado é <resultado> e o banco recarregado apresenta exatamente <efeito>
      E cada aplicação anterior permanece recuperável e uma recusa conserva também identidade e organização do ALVO

      Exemplos:
        | par | ordem | acao | resultado | efeito |
        | master_global+admin | master_global→admin | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+admin | master_global→admin | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+admin | master_global→admin | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+admin | admin→master_global | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+admin | admin→master_global | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+admin | admin→master_global | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+admin_organizacao | master_global→admin_organizacao | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+admin_organizacao | master_global→admin_organizacao | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+admin_organizacao | master_global→admin_organizacao | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+admin_organizacao | admin_organizacao→master_global | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+admin_organizacao | admin_organizacao→master_global | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+admin_organizacao | admin_organizacao→master_global | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+panel_user | master_global→panel_user | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+panel_user | master_global→panel_user | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+panel_user | master_global→panel_user | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+panel_user | panel_user→master_global | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+panel_user | panel_user→master_global | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+panel_user | panel_user→master_global | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+infra | master_global→infra | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+infra | master_global→infra | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+infra | master_global→infra | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | master_global+infra | infra→master_global | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | master_global+infra | infra→master_global | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | master_global+infra | infra→master_global | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+admin_organizacao | admin→admin_organizacao | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+admin_organizacao | admin→admin_organizacao | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+admin_organizacao | admin→admin_organizacao | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+admin_organizacao | admin_organizacao→admin | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+admin_organizacao | admin_organizacao→admin | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+admin_organizacao | admin_organizacao→admin | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+panel_user | admin→panel_user | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+panel_user | admin→panel_user | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+panel_user | admin→panel_user | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+panel_user | panel_user→admin | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+panel_user | panel_user→admin | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+panel_user | panel_user→admin | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+infra | admin→infra | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+infra | admin→infra | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+infra | admin→infra | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin+infra | infra→admin | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin+infra | infra→admin | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin+infra | infra→admin | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin_organizacao+panel_user | admin_organizacao→panel_user | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin_organizacao+panel_user | admin_organizacao→panel_user | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin_organizacao+panel_user | admin_organizacao→panel_user | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin_organizacao+panel_user | panel_user→admin_organizacao | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin_organizacao+panel_user | panel_user→admin_organizacao | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin_organizacao+panel_user | panel_user→admin_organizacao | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin_organizacao+infra | admin_organizacao→infra | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin_organizacao+infra | admin_organizacao→infra | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin_organizacao+infra | admin_organizacao→infra | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | admin_organizacao+infra | infra→admin_organizacao | criar | aceita | NOVO porcentagem/29, limite 3, usos 0 |
        | admin_organizacao+infra | infra→admin_organizacao | editar | aceita | mesmo ALVO valor 29, limite 3, usos 1 |
        | admin_organizacao+infra | infra→admin_organizacao | excluir | aceita | ALVO ausente; auditoria anterior recuperável |
        | panel_user+infra | panel_user→infra | criar | recusa | sem NOVO; ALVO valor 10, usos 1 |
        | panel_user+infra | panel_user→infra | editar | recusa | sem NOVO; ALVO valor 10, usos 1 |
        | panel_user+infra | panel_user→infra | excluir | recusa | sem NOVO; ALVO valor 10, usos 1 |
        | panel_user+infra | infra→panel_user | criar | recusa | sem NOVO; ALVO valor 10, usos 1 |
        | panel_user+infra | infra→panel_user | editar | recusa | sem NOVO; ALVO valor 10, usos 1 |
        | panel_user+infra | infra→panel_user | excluir | recusa | sem NOVO; ALVO valor 10, usos 1 |

    Esquema do Cenário: [CT-48] Cada administrador herdado alcança e opera as superfícies de escrita do painel
      Dado o ator de papel <papel> no contexto Acme, ALVO porcentagem/10 ativo com limite 3, contador 1 e sua aplicação anterior, e nenhum NOVO
      Quando o ator executa <operacao> na superfície real do painel /app da Acme
      Então o acesso administrativo é autorizado e a superfície apresenta exatamente <resultado>
      E a operação não consome uso nem destrói a recuperabilidade da aplicação anterior

      Exemplos:
        | papel              | operacao                       | resultado |
        | admin_organizacao  | visitar a rota de criar         | formulário de criação; sem NOVO; ALVO valor 10 |
        | admin_organizacao  | visitar a rota de editar ALVO   | formulário de edição com valor 10 |
        | admin_organizacao  | criar NOVO porcentagem/29, limite 3, validade futura por componente | NOVO persistido porcentagem/29, limite 3 e usos 0 |
        | admin_organizacao  | salvar ALVO com valor 29 pelo componente | mesmo ALVO persistido com valor 29, limite 3 e usos 1 |
        | admin_organizacao  | excluir ALVO pela ação da tabela | ALVO não localizado por chave nem código |
        | admin              | visitar a rota de criar         | formulário de criação; sem NOVO; ALVO valor 10 |
        | admin              | visitar a rota de editar ALVO   | formulário de edição com valor 10 |
        | admin              | criar NOVO porcentagem/29, limite 3, validade futura por componente | NOVO persistido porcentagem/29, limite 3 e usos 0 |
        | admin              | salvar ALVO com valor 29 pelo componente | mesmo ALVO persistido com valor 29, limite 3 e usos 1 |
        | admin              | excluir ALVO pela ação da tabela | ALVO não localizado por chave nem código |
        | master_global      | visitar a rota de criar         | formulário de criação; sem NOVO; ALVO valor 10 |
        | master_global      | visitar a rota de editar ALVO   | formulário de edição com valor 10 |
        | master_global      | criar NOVO porcentagem/29, limite 3, validade futura por componente | NOVO persistido porcentagem/29, limite 3 e usos 0 |
        | master_global      | salvar ALVO com valor 29 pelo componente | mesmo ALVO persistido com valor 29, limite 3 e usos 1 |
        | master_global      | excluir ALVO pela ação da tabela | ALVO não localizado por chave nem código |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-16 | Só esconde os botões de escrita do usuário comum | CT-14 | Chamada da ação não cria, não edita nem exclui |
| M-17 | Autoriza só criação, esquecendo edição/exclusão | CT-15 | As três linhas panel_user são recusadas com estado persistido intacto |
| M-18 | Guarda a permissão do mount e não confere no request | CT-16 | Nenhuma escrita ocorre após revogação |
| M-19 | Escolhe o primeiro papel e deixa panel_user sobrepor admin | CT-17 | Com enumeração panel_user→admin_organizacao, criar/editar/excluir são autorizados e gravam os mesmos efeitos da ordem inversa |
| M-20 | Permite escrita fora do formulário sem autorização | CT-15 | Via direta recusa cada verbo de panel_user/infra |
| M-69 — revisão adversarial ADV-05 | O domínio aceita admin/master_global, mas o painel bloqueia sua admissão | CT-48 | Ambos alcançam create/edit e concluem create/save/delete pelo painel, com efeitos persistidos exatos |

---

## Regra R6 — O contexto de organização limita leitura e escrita

> Origem: RQ-01, RQ-07, RQ-08, RQ-12, RQ-13, RQ-15, P-01, P-02, P-04 · Autorização (completo) · técnica: **IDOR; discriminante nulo; identidade×contexto no sucesso**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O contexto de organização limita leitura e escrita

    Esquema do Cenário: [CT-18] UUID de outra organização não permite editar nem excluir
      Dado a administradora da Acme e um cupom ativo da Globex de valor 10, contador 1 e sua linha de cupom_usos
      Quando a administradora tenta <acao> usando a chave do cupom da Globex no contexto Acme
      Então o acesso é negado sem revelar os atributos do cupom da Globex
      E valor 10, contador 1, existência do cupom e a linha de cupom_usos da Globex permanecem inalterados

      Exemplos:
        | acao                | # superfície       |
        | abrir edição por URL | route binding UUID |
        | salvar edição       | componente         |
        | excluir pela tabela | ação com chave     |

    Cenário: [CT-19] A saída efetiva da recusa leva a leitura alcançável
      Dado a usuária comum da Acme, seu cupom ativo ACME10 e um cupom ativo da Globex
      Quando a usuária tenta criar um cupom pela ação administrativa e acompanha a saída efetivamente produzida pela recusa
      Então a criação é recusada sem novo cupom e a saída leva a uma página de leitura autorizada que apresenta ACME10 e nenhum cupom da Globex
      E o destino não volta à escrita recusada nem produz ciclo de recusa

    Cenário: [CT-20] Um objeto de outra organização não é aplicável pelo chamador local
      Dado a administradora da Acme e um objeto Cupom ativo da Globex carregado antes da fixação do contexto Acme
      E o cupom da Globex tem valor 10, contador 1, limite 3 e sua linha de cupom_usos
      Quando a administradora aplica diretamente esse objeto a 10000 centavos no contexto Acme
      Então a aplicação é recusada sem total com desconto
      E o contador 1 e cada linha de cupom_usos da Globex permanecem iguais

    Esquema do Cenário: [CT-21] Sem organização corrente o modo multi-tenant fecha
      Dado tenancy ligada, cupons reais ativos na Acme e Globex e um registro legado com tenant_id nulo
      E a administradora está autenticada sem organização corrente e há snapshot não escopado de todas as linhas de cupons e cupom_usos
      Quando a administradora executa diretamente <operacao>
      Então a operação não lê nem altera cupons da Acme, da Globex ou do registro global
      E a criação é recusada e o snapshot não escopado de todas as linhas permanece exatamente igual, sem cupom novo com tenant_id nulo nem em outra organização

      Exemplos:
        | operacao | # fronteira |
        | consultar por código | leitura |
        | criar cupom | escrita |
        | editar cupom da Acme | escrita |
        | excluir cupom da Globex | escrita |
        | aplicar cupom global | consumo |

    Cenário: [CT-51] Aplicar o objeto local mantém identidade e organização quando o código também existe fora
      Dado Beto no contexto Acme, PROMO fixo/3000 da Globex inserido primeiro e PROMO porcentagem/10 da Acme inserido depois, ambos ativos com limite 3, contador 1 e uma aplicação real anterior distinta
      E o arnês comprova que a consulta global por PROMO resolveria Globex primeiro e captura os atributos, contadores e trilhas dos dois cupons com relógio em 2026-10-10T12:34:56Z
      Quando Beto aplica explicitamente o objeto PROMO da Acme a 10000 centavos no contexto Acme
      Então o retorno é exatamente 9000, o contador da Acme passa a 2 e somente o cupom da Acme ganha uma aplicação vinculada a Beto em 2026-10-10T12:34:56Z
      E a aplicação anterior da Acme permanece igual e todos os atributos, contador 1 e trilha da Globex permanecem exatamente no snapshot
```

CT-51 exercita sucesso com o objeto permitido, não uma recusa de objeto estrangeiro. Seu setup confirma o primeiro resultado da consulta técnica sem escopo que caracteriza M-75; não substitui a consulta/código da aplicação por um fake. É específico de tenancy ligada com duas organizações: no modo single, a duplicidade entre organizações não é configuração do domínio; CT-37 continua discriminando duas identidades locais sem colisão de código. A leitura técnica global é só do arnês e não autorização concedida ao ator.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-21 | Escopa apenas a lista, mas resolve qualquer UUID na escrita | CT-18 | Editar/excluir chave Globex não modifica o alvo |
| M-22 | Objeto Eloquent já carregado conserva acesso cruzado | CT-20 | Contador Globex permanece 1 e não surge aplicação |
| M-23 | Tenant nulo deixa consulta ou escrita aberta, incluindo inserir um novo registro global | CT-21 | Nenhum alvo é lido/alterado e o snapshot não escopado inteiro é idêntico; criar não acrescenta uma quarta linha nula |
| M-67 | A saída da recusa redireciona de volta à escrita proibida | CT-19 | O destino realmente produzido e seguido pela recusa apresenta leitura autorizada/ACME10 sem nova recusa; nenhum GET manual substitui esse destino |
| M-75 — revisão adversarial rodada 2 ADV-01 | Confere o objeto local, mas recarrega globalmente por código e consome o primeiro cupom de outra organização | CT-51 | Retorno 9000 e incremento/trilha somente Acme; Globex permanece no snapshot. O mutante devolve 7000 e consome/registra Globex |

CT-19 observa a resposta da tentativa real. O arnês acompanha o redirect ou segue o link de saída oferecido pela própria recusa; se a resposta for inline, observa a leitura que ela preserva. Não navegar manualmente a uma rota conhecida nem exigir uma URL literal que o 00 não fixa. Falta de saída alcançável é uma lacuna de UX de erro, não sucesso por um GET independente. Feature HTTP/componente basta para observar resposta, destino e acesso, sem browser.

---

## Regra R7 — O usuário comum lista somente cupons ativos do seu contexto

> Origem: RQ-08, P-03, P-02 · Elegibilidade (completo) · técnica: **Tabela de decisão completa; EP; paginação**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O usuário comum lista somente cupons ativos do seu contexto

    Esquema do Cenário: [CT-22] Ativo requer validade futura e uso disponível
      Dado a usuária comum da Acme e um cupom <tipo> com validade <validade>, usos <usos> e limite 3
      Quando a usuária lista os cupons da Acme
      Então a presença desse cupom é <presenca>
      E a leitura conserva contador e cada linha de cupom_usos

      Exemplos:
        | tipo        | validade | usos | presenca | # decisão |
        | porcentagem | futura   | 2    | presente | V e U |
        | porcentagem | passada  | 2    | ausente  | não V e U |
        | porcentagem | futura   | 3    | ausente  | V e não U |
        | porcentagem | passada  | 3    | ausente  | não V e não U |
        | fixo        | futura   | 2    | presente | V e U |
        | fixo        | passada  | 2    | ausente  | não V e U |
        | fixo        | futura   | 3    | ausente  | V e não U |
        | fixo        | passada  | 3    | ausente  | não V e não U |
        | porcentagem | T−1s     | 2    | ausente  | borda temporal inferior, relógio T |
        | porcentagem | T        | 2    | ausente  | igualdade temporal, relógio T |
        | porcentagem | T+1s     | 2    | presente | borda temporal superior, relógio T |
        | fixo        | T−1s     | 2    | ausente  | borda temporal inferior, relógio T |
        | fixo        | T        | 2    | ausente  | igualdade temporal, relógio T |
        | fixo        | T+1s     | 2    | presente | borda temporal superior, relógio T |
        | porcentagem | futura   | 4    | ausente  | legado limite+1, não U |
        | fixo        | futura   | 4    | ausente  | legado limite+1, não U |

    Esquema do Cenário: [CT-23] A listagem mantém o recorte em 0, 1 e mais de uma página
      Dado a usuária comum da Acme com <quantidade> cupons ativos locais A01 em diante, um Z_EXPIRADO local e um Z_GLOBEX ativo da Globex
      E a página comporta 10 registros e a ordem estável controlada pelo arnês coloca os códigos A antes dos Z, comprovando para quantidade 11 os dois proibidos na segunda página da consulta sem filtros
      Quando a usuária percorre as páginas da listagem
      Então são apresentados exatamente os <quantidade> cupons locais ativos sem repetição no conjunto estável
      E o expirado local e o ativo da Globex não aparecem em página alguma

      Exemplos:
        | quantidade | # borda |
        | 0          | vazio |
        | 1          | singleton |
        | 9          | página−1 |
        | 10         | página |
        | 11         | página+1 |

    Cenário: [CT-24] A busca não reabre o recorte de atividade e tenant
      Dado a usuária comum da Acme, PROMO ativo na Acme, PROMO expirado com código distinto PROMO_VELHO na Acme e PROMO ativo na Globex
      Quando a usuária pesquisa PROMO na tabela
      Então apenas o PROMO ativo local pertence ao resultado
      E contadores e cada linha de cupom_usos dos três cupons permanecem inalterados

    Cenário: [CT-46] O cupom removido não aparece na listagem do componente
      Dado a usuária comum da Acme, um REMOVIDO excluído por exclusão real e um SENTINELA ativo local
      Quando a usuária lista os cupons no componente ListCupons
      Então SENTINELA pertence ao conjunto visível e REMOVIDO não pertence
      E o contador e cada linha de cupom_usos de SENTINELA permanecem inalterados
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-24 | Usa OR entre validade e disponibilidade | CT-22 | As duas linhas em que apenas uma condição é válida permanecem ausentes |
| M-25 | Filtra só a primeira página | CT-23 | Na linha quantidade 11, a consulta sem filtros teria Z_EXPIRADO e Z_GLOBEX na página 2; a listagem efetiva devolve exatamente A01–A11 e nenhum Z em qualquer página |
| M-26 | A busca substitui a query protegida por uma consulta global | CT-24 | A busca retorna somente PROMO ativo local |
| M-64 | A tabela conserva a linha removida no conjunto exibido | CT-46 | ListCupons não apresenta REMOVIDO e apresenta SENTINELA |
| M-72 — revisão adversarial ADV-08 | A consulta considera válido expira_em igual ao instante da listagem | CT-22 | Com relógio T, validade T e saldo 2/3 não pertencem ao resultado, nos dois tipos |
| M-73 — revisão adversarial ADV-09 | A consulta usa usos diferente do limite em vez de usos menor que limite | CT-22 | O legado futuro com usos 4/limite 3 não aparece, nos dois tipos, sem alterar seus efeitos |

As linhas T−1s/T/T+1s de CT-22 fixam o relógio em T = 2026-10-10T12:34:56Z durante a consulta, além da aplicação coberta por CT-25. A linha usos 4/limite 3 é legado técnico preparado com trilha anterior real; não permite gravar limite abaixo dos usos no formulário nem responde Q3.

Controle de CT-23 (rodada 2 ADV-04): a ordem do arnês para a linha 11 é `[A01, …, A11, Z_EXPIRADO, Z_GLOBEX]`, com páginas de 10. Comprovar que o componente usa essa mesma ordem estável e que a consulta diagnóstica sem filtros coloca os dois proibidos nas posições 12 e 13. Usar ordenação válida disponível na superfície ou controle de arnês que preserve a query sob teste; não mockar o recorte. Se a configuração não conseguir garantir isso, declarar a prova de M-25 inviável, em vez de marcar CT-23 verde com proibidos apenas na página 1. O Então compara o conjunto, não impõe ao produto uma ordem de negócio.

---

## Regra R8 — A validade é conferida no instante efetivo da aplicação

> Origem: RQ-10, P-03, P-01 · Elegibilidade (completo) · técnica: **BVA 3-valores; tempo; TOCTOU**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: A validade é conferida no instante efetivo da aplicação

    Esquema do Cenário: [CT-25] O instante exato da expiração já é inválido
      Dado um cupom <tipo> da Acme com usos 2, limite 3 e expiração no instante T
      E a aplicadora da Acme existe e o relógio está em <instante>
      Quando a aplicadora tenta aplicar diretamente o cupom a 10000 centavos
      Então o resultado é <resultado> e o contador persistido é <contador>
      E a quantidade de novas linhas em cupom_usos é <novas_linhas>

      Exemplos:
        | tipo        | instante | resultado | contador | novas_linhas | # borda |
        | porcentagem | T−1s     | 9000      | 3        | 1            | antes |
        | porcentagem | T        | recusa    | 2        | 0            | exata |
        | porcentagem | T+1s     | recusa    | 2        | 0            | depois |
        | fixo        | T−1s     | 9000      | 3        | 1            | antes |
        | fixo        | T        | recusa    | 2        | 0            | exata |
        | fixo        | T+1s     | recusa    | 2        | 0            | depois |

    Esquema do Cenário: [CT-26] Uma consulta válida anterior não autoriza um cupom que expirou
      Dado a aplicadora da Acme e o cupom <tipo> ativo consultado em T−1s, com contador 2, limite 3 e expiração T
      E a aplicadora mantém o objeto e o relógio avança para T
      Quando a aplicadora chama aplicarEm nesse objeto com 10000 centavos
      Então a aplicação é recusada e não devolve total com desconto
      E o contador permanece 2 e nenhuma linha de cupom_usos é acrescentada

      Exemplos:
        | tipo        | # partição |
        | porcentagem | percentual |
        | fixo        | centavos   |

    Esquema do Cenário: [CT-27] A comparação usa o mesmo instante entre fuso local e UTC
      Dado um cupom porcentagem/10 da Acme, usos 0, limite 3 e expiração 2026-10-10 23:59:59 America/Sao_Paulo
      E o armazenamento representa esse instante como 2026-10-11 02:59:59 UTC e o relógio está em <agora_utc>
      Quando a aplicadora da Acme aplica diretamente o cupom a 10000 centavos
      Então o resultado é <resultado>, contador <contador> e novas linhas em cupom_usos <novas_linhas>
      E o horário da aplicação aceita corresponde ao instante do relógio, não à data truncada

      Exemplos:
        | agora_utc            | resultado | contador | novas_linhas | # janela discriminante |
        | 2026-10-11 02:30:00  | 9000      | 1        | 1            | ainda 23:30 no app |
        | 2026-10-11 02:59:59  | recusa    | 0        | 0            | borda local |
        | 2026-10-11 03:00:00  | recusa    | 0        | 0            | virada local |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-27 | Usa >= now e permite o instante T | CT-25 | Em T a recusa deixa contador 2 e cria 0 linhas |
| M-28 | Confere validade apenas em valido() | CT-26 | Objeto consultado antes de T é recusado em T |
| M-29 | Compara data ou UTC ingênuo com horário local | CT-27 | Às 02:30 UTC / 23:30 local retorna 9000; na borda local recusa |

---

## Regra R9 — O limite é respeitado na leitura, no uso e na concorrência

> Origem: RQ-11, RQ-13, P-01 · Elegibilidade (completo) · técnica: **BVA 3-valores; TOCTOU; concorrência**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O limite é respeitado na leitura, no uso e na concorrência

    Esquema do Cenário: [CT-28] O limite autoriza somente usos ainda disponíveis
      Dado um cupom <tipo> da Acme com validade futura, limite 3 e usos <usos>
      Quando a aplicadora da Acme aplica diretamente o cupom a 10000 centavos
      Então o resultado é <resultado> e o contador persistido é <contador>
      E o número de novas linhas em cupom_usos é <novas_linhas>

      Exemplos:
        | tipo        | usos | resultado | contador | novas_linhas | # borda |
        | porcentagem | 2    | 9000      | 3        | 1            | limite−1 |
        | porcentagem | 3    | recusa    | 3        | 0            | limite |
        | porcentagem | 4    | recusa    | 4        | 0            | limite+1 legado |
        | fixo        | 2    | 9000      | 3        | 1            | limite−1 |
        | fixo        | 3    | recusa    | 3        | 0            | limite |
        | fixo        | 4    | recusa    | 4        | 0            | limite+1 legado |

    Esquema do Cenário: [CT-29] O objeto desatualizado não ultrapassa o último uso
      Dado a aplicadora Ana e o cupom <tipo> ativo da Acme carregado com usos 2 e limite 3
      E Beto já consumiu o último uso por uma aplicação real depois desse carregamento
      Quando Ana aplica diretamente seu objeto antigo a 10000 centavos
      Então Ana recebe recusa e o contador persistido permanece 3
      E só permanece a linha da aplicação de Beto, sem nova linha de Ana

      Exemplos:
        | tipo        | # partição |
        | porcentagem | percentual |
        | fixo        | centavos   |

    Esquema do Cenário: [CT-30] Duas aplicações simultâneas disputam a última unidade
      Dado Ana e Beto da Acme, um cupom <tipo> ativo com usos <iniciais> e limite <limite> e duas conexões independentes ao mesmo banco
      E ambas execuções carregaram o cupom e aguardam a mesma barreira antes de consumir
      Quando Ana e Beto aplicam simultaneamente o cupom a 10000 centavos
      Então exatamente uma aplicação retorna 9000 e a outra é recusada por indisponibilidade
      E o contador persistido é <limite> e há exatamente uma nova linha de cupom_usos com o vencedor e seu instante

      Exemplos:
        | tipo        | iniciais | limite | # partição |
        | porcentagem | 0        | 1      | primeira/última unidade |
        | porcentagem | 2        | 3      | última unidade com histórico |
        | fixo        | 0        | 1      | primeira/última unidade |
        | fixo        | 2        | 3      | última unidade com histórico |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-30 | Usa <= limite e concede o quarto uso | CT-28 | Na borda usos=3 a aplicação recusa e conserva contador 3 |
| M-31 | Lê disponibilidade apenas do objeto carregado | CT-29 | Ana não consome depois do uso real de Beto |
| M-32 | Faz check-then-act e duas execuções usam a última unidade | CT-30 | Exatamente um sucesso, um uso novo e uma linha nova |
| M-33 | Usa incremento não atômico e perde atualização | CT-30 | A contagem de sucessos é 1; contador e trilha concordam |

---

## Regra R10 — O retorno representa o total após desconto em centavos

> Origem: RQ-12, P-01, P-05, P-06, P-07 · Cálculo (padrão) · técnica: **EP; BVA 3-valores escalado; exemplo discriminante**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O retorno representa o total após desconto em centavos

    Esquema do Cenário: [CT-31] O percentual inteiro trunca apenas a fração do desconto
      Dado a aplicadora da Acme e um cupom porcentagem/<percentual> ativo com contador 0 e limite 3
      Quando a aplicadora aplica diretamente o cupom ao total de <total> centavos
      Então o total devolvido é exatamente <final> centavos
      E o contador persistido passa a 1 e há uma linha de cupom_usos da aplicadora

      Exemplos:
        | percentual | total | final | # partição |
        | 29         | 10000 | 7100  | valor integral; não discrimina o float de M-34 |
        | 29         | 100   | 71    | discriminante PHP: float trunca 28,999999999999996 para 28 |
        | 10         | 9999  | 9000  | 999,9 centavos truncados |
        | 5          | 50    | 48    | desconto 2,5 truncado |
        | 1          | 100   | 99    | mínimo % |
        | 100        | 9999  | 0     | máximo % |

    Esquema do Cenário: [CT-32] O desconto fixo nunca produz total negativo
      Dado a aplicadora da Acme e um cupom fixo/<valor> ativo com contador 0 e limite 3
      Quando a aplicadora aplica diretamente o cupom ao total de <total> centavos
      Então o total devolvido é exatamente <final> centavos
      E o contador persistido passa a 1 e há uma linha de cupom_usos da aplicadora

      Exemplos:
        | valor | total | final | # borda |
        | 1000  | 999   | 0     | valor−1 |
        | 1000  | 1000  | 0     | valor |
        | 1000  | 1001  | 1     | valor+1 |
        | 1     | 1     | 0     | um centavo |
        | 1000  | 0     | 0     | total zero |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-34 | Calcula desconto como (int)(($percentual / 100) * $total) | CT-31 | 29% de 100 devolve exatamente 71; esse mutante devolve 72 na microprova PHP do adversário |
| M-35 | Arredonda o desconto em vez de truncar | CT-31 | 5% de 50 devolve 48, e não 47 |
| M-36 | Trunca o total final em vez do desconto | CT-31 | 10% de 9999 devolve 9000, e não 8999 |
| M-37 | Interpreta 1000 fixo como reais | CT-32 | 1000 fixo sobre total 1001 devolve 1 |
| M-38 | Subtrai sem piso zero | CT-32 | 1000 fixo sobre total 999 devolve 0 |

Correção ADV-01: 29%/10000 não distinguia M-34. O adversário executou expressões PHP autocontidas e constatou 29%/100 → final float 72 versus inteiro 71. Este executor incorporou o discriminante sem executar a aplicação ou adotar float como valor monetário de fixture.

---

## Regra R11 — Existe cupom válido e coerente antes de qualquer efeito

> Origem: RQ-09, RQ-10, RQ-11, RQ-12, RQ-13, RQ-15, P-05 · Elegibilidade (completo) · técnica: **EP isolada; defesa no uso; não-efeito**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: Existe cupom válido e coerente antes de qualquer efeito

    Esquema do Cenário: [CT-33] A inexistência e cada condição inválida recusam sem efeitos
      Dado a aplicadora real da Acme e o alvo <alvo> de tipo <tipo> com contador <contador> e histórico anterior preservado
      E todas as condições distintas de <invalidade> são válidas
      Quando a aplicadora tenta aplicar o cupom a 10000 centavos pelo motor
      Então a aplicação é recusada sem total com desconto
      E o contador <contador> e cada linha anterior de cupom_usos permanecem inalterados e não há nova linha

      Exemplos:
        | alvo           | tipo        | contador | invalidade | # partição |
        | código INEXISTENTE | porcentagem | 0     | não existe | existência |
        | cupom persistido  | porcentagem | 2     | expirado   | tempo |
        | cupom persistido  | porcentagem | 3     | esgotado limite 3 | uso |
        | cupom persistido  | fixo        | 2     | expirado   | tempo |
        | cupom persistido  | fixo        | 3     | esgotado limite 3 | uso |

    Esquema do Cenário: [CT-34] Percentual inválido persistido por outra via não é consumido
      Dado a aplicadora da Acme e um cupom porcentagem/<percentual> importado inválido com validade futura, contador 1, limite 3 e sua linha anterior de cupom_usos
      Quando a aplicadora aplica diretamente esse cupom a 10000 centavos
      Então a aplicação é recusada sem total com desconto
      E o contador permanece 1 e a linha anterior de cupom_usos é conservada sem acréscimo

      Exemplos:
        | percentual | # partição |
        | 0          | abaixo do domínio P-05 |
        | 101        | acima do domínio P-05 |

    Esquema do Cenário: [CT-47] Expirado e esgotado juntos também recusam a aplicação
      Dado a aplicadora real da Acme e um cupom <tipo> expirado e esgotado com contador 3, limite 3 e três linhas anteriores de cupom_usos
      Quando a aplicadora aplica diretamente o cupom a 10000 centavos
      Então a aplicação é recusada sem total com desconto
      E o contador permanece 3 e as três linhas anteriores de cupom_usos permanecem sem acréscimo

      Exemplos:
        | tipo        | # decisão |
        | porcentagem | não V e não U |
        | fixo        | não V e não U |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-39 | Cupom inexistente usa um default e concede desconto | CT-33 | INEXISTENTE é recusado sem valor descontado e sem linha de uso |
| M-40 | Incrementa o contador antes de decidir a recusa | CT-33 | Cupom expirado conserva o contador 2 |
| M-41 | Confia no formulário para o domínio percentual do uso | CT-34 | Percentual legado 101 é recusado e não consome |
| M-42 | Registra tentativa recusada como aplicação efetiva | CT-33 | Após cada recusa há zero linhas novas de cupom_usos |
| M-65 | Recusa apenas quando uma condição é inválida, com XOR entre expirado e esgotado | CT-47 | As duas condições inválidas juntas recusam, contador 3 e zero linhas novas |

---

## Regra R12 — Cada aplicação aceita consome exatamente um uso

> Origem: RQ-13, P-01 · Auditoria e consumo (completo) · técnica: **Rastreio de efeito por partição**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: Cada aplicação aceita consome exatamente um uso

    Esquema do Cenário: [CT-35] Ambos os tipos incrementam uma vez o contador persistido
      Dado a aplicadora da Acme e um cupom <tipo> ativo com contador 2, limite 5 e duas linhas anteriores de cupom_usos
      Quando a aplicadora aplica diretamente o cupom a 10000 centavos
      Então o retorno é 9000 e o contador recarregado do banco é 3
      E as duas linhas anteriores permanecem e existe exatamente uma nova linha da aplicadora

      Exemplos:
        | tipo        | # partição |
        | porcentagem | valor 10 |
        | fixo        | valor 1000 |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-43 | Calcula o desconto mas não persiste o incremento | CT-35 | Contador recarregado é 3, não 2 |
| M-44 | Soma duas vezes em uma aplicação | CT-35 | Contador é 3, não 4, e existe uma linha nova |
| M-45 | Só incrementa no ramo porcentagem | CT-35 | Linha fixo também passa de 2 para 3 |

---

## Regra R13 — A trilha própria identifica a pessoa e o instante reais

> Origem: RQ-15, P-08, P-01 · Auditoria e consumo (completo) · técnica: **Rastreio: acontece; não acontece; uma vez; atomicidade; guard×argumento; alvo×não-alvo**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: A trilha própria identifica a pessoa e o instante reais

    Esquema do Cenário: [CT-36] A aplicação registra pessoa e instante sem depender de eventos do cupom
      Dado Beto da Acme como argumento aplicadoPor do motor, Ana como pessoa real distinta e um cupom <tipo> ativo com contador 0 e limite 3
      E o guard HTTP está <guard> e o relógio está fixado em 2026-10-10T12:34:56Z
      Quando Beto aplica diretamente o cupom a 10000 centavos
      Então cupom_usos contém exatamente uma nova linha vinculada ao cupom, à chave de Beto e ao instante 2026-10-10T12:34:56Z
      E o retorno é 9000 e o contador persistido é 1

      Exemplos:
        | tipo        | guard                 | # partição |
        | porcentagem | ausente               | valor 10; sem identidade HTTP |
        | porcentagem | autenticado como Beto | valor 10; argumento e guard iguais |
        | porcentagem | autenticado como Ana  | valor 10; argumento e guard distintos |
        | fixo        | ausente               | valor 1000; sem identidade HTTP |
        | fixo        | autenticado como Beto | valor 1000; argumento e guard iguais |
        | fixo        | autenticado como Ana  | valor 1000; argumento e guard distintos |

    Esquema do Cenário: [CT-37] Aplicações distintas preservam toda a história e autoria
      Dado A fixo/3000 como primeiro cupom elegível da Acme e B <tipo> como segundo, ambos com limite 5, com aplicações reais de Ana em T−2s para A e T−1s para B
      E Beto existe, o guard está ausente, o relógio está em T e o arnês capturou o snapshot de A e comprovou A como primeiro resultado da consulta do contexto
      Quando Beto aplica explicitamente o cupom B a 10000 centavos
      Então o retorno é 9000 e somente B contém a linha anterior de Ana em T−1s e uma nova linha de Beto em T, exatamente duas aplicações ligadas a B e contador 2
      E A conserva integralmente seu snapshot, contador 1 e a única linha de Ana em T−2s, sem nova aplicação de Beto

      Exemplos:
        | tipo        | # partição |
        | porcentagem | valor 10 |
        | fixo        | valor 1000 |

    Esquema do Cenário: [CT-38] Falha ao inserir a trilha desfaz o consumo anterior
      Dado a aplicadora da Acme e um cupom <tipo> ativo com contador 1, limite 3 e uma linha anterior de cupom_usos
      E o arnês falha somente na inserção de cupom_usos, depois de observar o incremento do contador dentro da transação
      Quando a aplicadora tenta aplicar o cupom a 10000 centavos
      Então há falha sem retorno de total com desconto e o contador recarregado volta a 1
      E só permanece a linha anterior de cupom_usos, sem nova linha da aplicadora

      Exemplos:
        | tipo        | # partição |
        | porcentagem | valor 10 |
        | fixo        | valor 1000 |

    Esquema do Cenário: [CT-39] Falha depois da trilha desfaz também o registro
      Dado a aplicadora da Acme e um cupom <tipo> ativo com contador 1, limite 3 e sua linha anterior de cupom_usos
      E o arnês lança uma falha depois de observar a inserção da nova linha de cupom_usos e antes do commit
      Quando a aplicadora tenta aplicar o cupom a 10000 centavos
      Então há falha sem retorno de total com desconto e o contador recarregado volta a 1
      E a linha anterior de cupom_usos permanece e a linha observada durante a transação não permanece no banco

      Exemplos:
        | tipo        | # partição |
        | porcentagem | valor 10 |
        | fixo        | valor 1000 |

    Esquema do Cenário: [CT-49] Excluir cupom usado conserva imediatamente a prova de autoria e instante
      Dado a administradora da Acme e um cupom <tipo> com uma aplicação real de Ana em 2026-10-10T12:34:56Z, registrada na trilha própria e vinculada inequivocamente ao cupom
      E a aplicação e a pessoa Ana foram recarregadas e suas identidades e instante foram capturados antes da exclusão
      Quando a administradora executa diretamente a exclusão autorizada do cupom
      Então o cupom deixa de ser localizado para uso e a releitura imediata dos registros persistidos ainda recupera exatamente a aplicação de Ana no instante capturado, atribuída ao mesmo cupom
      E nenhuma aplicação anterior desaparece nem muda de pessoa ou de instante e nenhuma aplicação nova é criada

      Exemplos:
        | tipo        | # partição |
        | porcentagem | valor 10 |
        | fixo        | valor 1000 |
```

CT-49 deriva do invariante fechado de RQ-15: a própria exclusão entregue por RQ-01 não pode apagar imediatamente o que se registrou para auditar depois. O oráculo é a recuperabilidade persistida de cupom/pessoa/instante, sem exigir tela ou relatório, soft delete, prazo infinito de retenção ou mecanismo específico de FK. O prazo futuro e a exclusão da pessoa permanecem L6. Se o responsável quiser que excluir cupom também elimine sua prova histórica, isso exige decisão de requisito explícita; não está autorizado pelo cascade do plano.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-46 | Depende apenas da auditoria por evento de Cupom e não grava cupom_usos | CT-36 | Tabela própria contém cupom, Beto e instante concreto |
| M-47 | Obtém pessoa apenas de Auth e perde autoria em job/chamada direta | CT-36 | Sem guard HTTP a chave gravada é a de Beto |
| M-48 | Faz upsert e substitui a aplicação anterior | CT-37 | Ana/T−1s continua e Beto/T acrescenta segunda linha |
| M-49 | Consome uso fora da transação da trilha | CT-38 | Após falhar a inserção o contador volta a 1 |
| M-50 | A trilha é gravada em conexão/transação separada | CT-39 | A linha inserida antes da falha não permanece |
| M-51 | Grava tentativas inválidas como aplicações | CT-33 | Recusa acrescenta 0 linhas, em cada tipo |
| M-74 — revisão adversarial ADV-04 | Excluir cupom usado apaga em cascata seus registros de aplicação | CT-49 | Depois da exclusão ainda se recuperam a mesma aplicação, identidade do cupom, Ana e instante capturado; o mutante deixa zero aplicações recuperáveis |
| M-76 — revisão adversarial rodada 2 ADV-02 | Prefere o usuário do guard quando existe e usa aplicadoPor somente como fallback | CT-36 | Guard Ana com argumento Beto grava somente Beto/T nos dois tipos; nenhuma aplicação atribuída a Ana |
| M-77 — revisão adversarial rodada 2 ADV-03 | Calcula e consome B, mas vincula a nova aplicação ao primeiro cupom local A | CT-37 | B ganha Beto/T e fica com duas aplicações; snapshot de A continua com sua única linha anterior, sem Beto/T |

---

## Regra R14 — O cupom removido não volta a funcionar por objeto antigo

> Origem: RQ-01, RQ-07, RQ-09, P-03 · Elegibilidade (completo) · técnica: **Estado×operação; chave inexistente; 2-switch**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O cupom removido não volta a funcionar por objeto antigo

    Esquema do Cenário: [CT-40] A chave inexistente não gera edição nem nova exclusão
      Dado a administradora da Acme, a chave de um cupom que já foi excluído e um SENTINELA ativo de valor 10
      Quando a administradora executa <acao> sobre a chave excluída
      Então o cupom excluído não é recriado e SENTINELA permanece com valor 10
      E nenhum contador é consumido e nenhuma linha de cupom_usos é acrescentada

      Exemplos:
        | acao              | # célula |
        | abrir edição por URL | leitura inexistente |
        | salvar edição        | edição inexistente |
        | excluir novamente    | exclusão repetida |

    Esquema do Cenário: [CT-41] Excluir e aplicar por objeto retido recusa a aplicação
      Dado a administradora da Acme, um objeto <tipo> carregado enquanto ativo e seu cupom excluído por uma exclusão real
      E a aplicadora existe e há um cupom SENTINELA com contador 0 e sua linha de cupom_usos preservada
      Quando a aplicadora chama aplicarEm no objeto retido com 10000 centavos
      Então a aplicação é recusada sem total com desconto e o cupom excluído não reaparece
      E SENTINELA continua com contador 0 e não há nova linha de cupom_usos para a chave excluída

      Exemplos:
        | tipo        | # partição |
        | porcentagem | percentual |
        | fixo        | centavos |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-52 | Salvar um objeto removido recria o cupom silenciosamente | CT-40 | Depois de salvar a chave excluída continua ausente |
| M-53 | Calcula e devolve desconto de objeto cujo UPDATE não encontrou linha | CT-41 | Objeto removido é recusado sem valor com desconto |
| M-54 | Dupla exclusão alcança o próximo registro por chave errada | CT-40 | SENTINELA permanece com valor 10 |

---

## Regra R15 — Payload não escolhe organização, identidade nem contador

> Origem: RQ-07, RQ-13, P-02, P-08 · Autorização (completo) · técnica: **Mass assignment por entidade; criação/edição**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: Payload não escolhe organização, identidade nem contador

    Esquema do Cenário: [CT-42] Campos protegidos enviados pelo formulário não alteram a fronteira
      Dado a administradora da Acme e um cupom ativo da Acme com UUID U, contador 1 e sua linha de cupom_usos
      Quando a administradora envia <operacao> com os dados válidos e apenas o campo protegido <campo>=<valor_falso>
      Então a gravação não usa <valor_falso> para escolher a organização, o UUID ou o contador
      E o cupom existente conserva UUID U, organização Acme e contador 1 e sua linha de cupom_usos permanece

      Exemplos:
        | operacao | campo     | valor_falso | # ataque isolado |
        | criar    | tenant_id | Globex      | fronteira |
        | criar    | usos      | 99          | consumo   |
        | editar   | tenant_id | Globex      | fronteira |
        | editar   | usos      | 0           | consumo   |
        | editar   | uuid      | UUID Globex | identidade |

    Esquema do Cenário: [CT-43] A escrita direta também protege organização e contador
      Dado a administradora da Acme e um cupom ativo local com UUID U, contador 1 e sua linha de cupom_usos
      Quando a administradora executa diretamente a escrita de edição com valor 29 e apenas <campo>=<valor_falso> no payload
      Então o cupom persiste na Acme com UUID U e contador 1
      E a linha anterior de cupom_usos permanece e não é criada uma aplicação

      Exemplos:
        | campo     | valor_falso | # ataque isolado |
        | tenant_id | Globex      | organização |
        | usos      | 0           | contador |
        | uuid      | UUID Globex | identidade |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-55 | Aceita tenant_id do cliente no create ou save | CT-42 | Organização persistida é Acme, nunca Globex |
| M-56 | Deixa o cliente zerar usos | CT-43 | Contador persistido continua 1 |
| M-57 | Protege UUID somente no componente | CT-43 | Escrita direta conserva UUID U |

---

## Regra R16 — O estado do framework não reabre a consulta do usuário

> Origem: RQ-08, P-02, P-03 · Autorização (completo) · técnica: **Superfície Livewire; domínio e tipo inválidos**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto
  Regra: O estado do framework não reabre a consulta do usuário

    Esquema do Cenário: [CT-44] Ordenação e busca adulteradas conservam o recorte
      Dado a usuária comum da Acme, um ACME ativo local, um expirado local e um GLOBEX ativo de outra organização
      Quando a usuária envia diretamente ao componente <entrada>=<valor>
      Então a entrada é recusada ou normalizada sem revelar o expirado nem GLOBEX e sem executar coluna arbitrária
      E os três cupons conservam os valores, contadores e cada linha de cupom_usos

      Exemplos:
        | entrada     | valor                | # ataque isolado |
        | tableSort   | coluna_inexistente:asc | domínio de coluna |
        | tableSort   | codigo:drop_table     | domínio de direção |
        | tableSort   | array                 | tipo errado |
        | tableSearch | array                 | tipo errado |
        | tableSearch | "' OR 1=1 --"         | busca adversarial |

    Cenário: [CT-45] Trocar a identidade do registro entre requests não muda o alvo
      Dado EditCupom montado para a administradora da Acme sobre o cupom ACME e um cupom real GLOBEX de valor 10, contador 1 e sua linha de cupom_usos
      Quando a administradora envia a troca da propriedade record para a chave GLOBEX entre requests
      Então a troca é recusada e nenhum atributo de GLOBEX é devolvido nem modificado
      E GLOBEX conserva valor 10, contador 1 e cada linha anterior de cupom_usos
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-58 | Usa tableSort como coluna SQL livre | CT-44 | coluna_inexistente não é executada e não há registros fora do recorte |
| M-59 | Estado de busca faz consulta global sem ativo/tenant | CT-44 | GLOBEX e o expirado não são devolvidos |
| M-60 | Confia no record enviado pelo cliente e troca o alvo da edição | CT-45 | A troca é recusada e a resposta não contém atributos de GLOBEX; conservar valor 10/contador 1 isoladamente não mataria o vazamento |

---

## Regra R17 — O navegador mostra a unidade e a correção da seleção de tipo

> Origem: RQ-01, RQ-03, P-05 · UI no navegador (padrão) · técnica: **EP do discriminador; reatividade observável**.

Cenários na costura browser: CT-B01 e CT-B02, no 05.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | O Select não envia alteração reativa e o campo conserva unidade antiga | CT-B01 | Após porcentagem→fixo a indicação visível informa centavos; após fixo→porcentagem informa percentual |
| M-62 | O erro de valor fica oculto e bloqueia o formulário sem recuperação | CT-B02 | O erro 101 é visível; após corrigir para 100 o formulário grava porcentagem/100 |
| M-63 | A troca de tipo mantém teto percentual para o valor fixo | CT-B01 | Após selecionar fixo o valor 1000 pode ser gravado |


## Checklist de Taxonomia

| Item / gatilho | Cenário que mata ou lacuna | Grupo |
|---|---|---|
| IDOR / autorização horizontal | CT-18, CT-20; CT-51 mantém identidade/tenant também no sucesso com código duplicado entre organizações | G-C, G-A |
| Autorização na ação, cada verbo e por fora da UI | CT-14–17; CT-48 para todos os administradores no painel; CT-17 fixa ambas as ordens de cada par | G-C, G-D |
| Idempotência no agregado persistido | **lacuna L1**: Pedido fora de escopo P-01; retorno de duas chamadas não prova agregado. Não criar Pedido nem chamar duas vezes e marcar idempotente. Confirmação de escopo já dada; contrato de retry da futura integração permanece não especificado | G-A |
| Domínio condicionado tipo×valor | CT-08–10, CT-34 | G-C, G-D, G-A |
| Limites na criação e edição | CT-08–13; CT-02/03 guardam o limite válido exato e CT-50 a conversão temporal. **Lacuna L2**: recortes de RQ-02/04/05/06 abertos Q1–Q4 para teto textual, fixo mínimo/máximo, validade passada, limite 0/baixo/fracionário; não copiar regras do formulário para o oráculo | G-C, G-D |
| Contador/limite concorrente | CT-28–30; G-X proposto e não executado | G-X |
| Cardinalidade do efeito | CT-21 recusa criação sem alterar snapshot global; CT-33, CT-35–39: 0 novas linhas na recusa com alvo real, 1 no sucesso, N preservadas; CT-37/51 discriminam alvo/não-alvo; CT-49 conserva trilha na exclusão. CT-36 fixa argumento Beto com guard ausente/igual/distinto | G-A, G-D |
| Ausente ≠ null ≠ vazio | CT-05/06 para tipo; **lacuna L2** nos campos de RQ abertas; não afirmar semântica de campo omitido da edição sem requisito | G-C |
| Paginação 0/1/limite/além | CT-23 controla os proibidos na página 2 da consulta sem filtros; **lacuna L3**: inserção entre páginas tem ordenação/snapshot não especificados, não garantir estabilidade concorrente inventada | G-C |
| Ordenação inválida, nullable e empate | CT-44; **lacuna L3**: ordenação/nullable/tie-break não especificados no 00. O vendor possui defaultKeySort, mas não serve como oráculo de negócio | G-C |
| Timezone app×DB×usuário / meia-noite | CT-25–27 e CT-50 para fim do dia ao converter entrada somente data; **lacuna L4**: DST/fuso pessoal fora de America/Sao_Paulo não definidos; nenhum arnês foi executado | G-A, G-C |
| Texto livre, Unicode, espaços, n/n+1 | **lacuna L2**: RQ-02 aberta Q1; não assumir 40, maiúsculas ou trim do PRD | G-D |
| Unicidade + SoftDeletes | **lacuna L5**: ausência da implementação e do 02 impede confirmar mecanismo. CT-04/41 provam removido em mecanismo observável, mas não afirmam recriação do código após remover | G-C |
| Removível/desativável × escrita | CT-40/41/47 e matriz única | G-C, G-A |
| CRUD ID inexistente, excluir duas vezes, editar sem alterar código | CT-12, CT-40 | G-C |
| Mass assignment cupons | CT-42/43 | G-C, G-D |
| IDOR por entidade — cupons | CT-18/20/21/51, incluindo sucesso local sem consumir cupom estrangeiro do mesmo código | G-C, G-A, G-D |
| IDOR por entidade — cupom_usos | **lacuna L5**: 02 ausente, sem inventário de entradas diretas da tabela-filho; CT-20 prova o motor, não uma consulta/ação direta do filho. Não alegar proteção herdada só por cupom_id | G-D |
| Mass assignment por entidade — cupom_usos | **lacuna L5**: falta inventário de quem recebe payload para o filho; CT-36 prova autoria no motor, não ignorar aplicado_por_id/cupom_id em uma superfície ainda não descrita. Não inventar endpoint ou chamar constructor como prova de segurança | G-D |
| Upload | não se aplica: nenhum upload é pedido no 00 nem exposto nas quatro linhas de Superfície de UI. Isso delimita este requisito; não afirma que algum vendor é incapaz de upload | — |
| Precisão monetária | CT-31/32, inteiro de centavos; 29% de 100 distingue o float específico de M-34 (microprova independente); 5% de 50 distingue arredondamento | G-A |
| Superfície Livewire: público, propriedade, framework | CT-16, CT-44/45; **lacuna L5**: 02 ausente, cobertura não pode ser declarada exaustiva | G-C |
| Estado framework consumido em índice/parse/coluna/operador | CT-44 para coluna/direção/busca; **lacuna L5**: consumidores restantes do componente novo desconhecidos sem 02 | G-C |
| Método público com argumento fora do domínio e tipo errado | CT-05–10/44; **lacuna L5**: argumentos e métodos de todos os componentes não inventariados. Não tomar set/call ou #[Locked] como isolamento total | G-C |
| Escopo com discriminante nulo | CT-21, com registros de ambos tenants e legado global reais e igualdade do snapshot não escopado global depois da recusa | G-D |
| Estado de erro com saída | CT-19 acompanha a saída realmente produzida pela recusa; não a substitui por GET manual de uma listagem. Falhas de motor são resposta ao chamador, sem rota de checkout por P-01 | G-C |
| Auditoria após remoção do cupom/usuário | CT-49 prova recuperabilidade imediatamente após a exclusão do cupom usado, por RQ-15. **Lacuna L6**: prazo futuro de retenção, expurgo e exclusão/anonimização da pessoa não estão determinados; sem cenário afirmando uma dessas políticas | G-D |

**Lacunas não são cenários verdes nem medições.** L1 está ancorada em P-01 aceita; L2 depende de perguntas novas; L3/L4 são comportamento adicional não decidido; L5 é uma entrada obrigatória ausente; L6 é prazo futuro e remoção da pessoa, que não se inferirão da FK do PRD. L6 não dispensa a prova fechada de CT-49. Nenhuma dispensa de fronteira usa uma negativa sobre o vendor sem evidência.

## Gate de falsificabilidade e poda

Cada regra tem tabela com implementações erradas plausíveis, matador e valor que diverge. Os mutantes são **de especificação**, não execução de pest --mutate. BVA usa 1 ponto percentual, 1 centavo, 1 uso e 1 segundo. EP inválida é isolada; CT-47 exercita a combinação necessária à decisão completa. Mundo com alvo/trilha real em toda recusa que pretende provar não-efeito. CT-38 falha depois do incremento; CT-39 depois da trilha. Falha anterior ao efeito não satisfaz esses cenários.

R1 tem 5 cenários no perfil padrão (teto 3): visita de cada rota, gravação create/save, exclusão e conversão da entrada temporal são observáveis diferentes; o gate de tela de escrita e M-01/02/03/66/70 justificam o estouro. CT-50 veio de ADV-03 da rodada 1. R5 tem 5 cenários com CT-48 de ADV-05 da rodada 1; a matriz de admissão no painel é distinta da chamada direta. R6 tem 5 com CT-51 de ADV-01 da rodada 2, distinguindo sucesso e não-alvo estrangeiro. G-B tem 2 CT-B (padrão prevê 1 happy path): o erro/reparo visível de CT-B02 é o único matador de M-62; o gate vence o teto. R13 tem 5 cenários com CT-49 de ADV-04 da rodada 1; CT-36/37 agora discriminam fonte de autoria e identidade do alvo. R1 tem 6 mutantes (teto padrão 5) e R13 tem 9 (teto completo 6): M-68/M-70, M-74 e M-76/77 vieram das revisões independentes, exceção explícita do passo 6. O crescimento de R13 sugere futura separação de identidade/autoria e atomicidade; o achado estrutural foi escalado em D-01, sem renumerar a rastreabilidade só para satisfazer um teto.

| Cogitado e cortado | Por que foi cortado |
|---|---|
| CT-B de todo o CRUD só para conferir persistência | CT-02/03/04 provam a gravação/ação no componente |
| CT-B de listagem ativa e matriz de autorização | CT-14–24 e CT-46 fazem isso em camada mais barata |
| Unit do método descontoSobre do plano | método não é contrato do 00; Unit sem container e motor já observável em G-A |
| Campo com 40/41 caracteres | teto só do plano; Q1 e lacuna L2 |
| Gravar vencido e exigir aceitação ou recusa inventada | Q2; invariante do uso CT-25/26/33 |
| Limite 0 e redução abaixo dos usos como regra de formulário | Q3; não substituir usos/histórico para “corrigir” a fixture |
| Idempotência por igualdade dos retornos de duas chamadas | sem agregado persistido por P-01, tautologia; L1 |
| Assertions de log no channel cupom | log do plano não é RQ; registro RQ-15 está em CT-36–39 |
| Teste de badge literal e precedência esgotado/expirado | texto e precedência só do PRD |
| Dark mode por assertSee e primeiro screenshot como baseline | não prova legibilidade; nenhuma aceitação de tema no 00 |

## Índice de Cenários

Arquivos são **propostos e ainda inexistentes**. A rule do projeto mantém par de modos; não rodar a mesma rota tenant na suíte single. Grupo define a costura, não a pasta física. CT-51 é específico de duas organizações com o mesmo código; não transportar essa configuração inválida para o modo single. A identidade entre dois cupons locais do modo single continua discriminada em CT-37.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | As telas de escrita oferecem o tipo e a unidade do valor | R1 | EP; par visita/gravação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-66 |
| CT-02 | O formulário de criação persiste os dois tipos | R1 | EP; par visita/gravação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-01 |
| CT-03 | O formulário de edição grava sem consumir uso | R1 | EP; par visita/gravação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-02, M-68 |
| CT-04 | A exclusão autorizada remove o cupom | R1 | EP; par visita/gravação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-03 |
| CT-05 | A criação recusa cada tipo inválido isoladamente | R2 | EP em criação, edição e domínio | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-04 |
| CT-06 | A edição recusa cada tipo inválido sem alterar o cupom | R2 | EP em criação, edição e domínio | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-05 |
| CT-07 | O domínio não grava terceiro tipo fora do formulário | R2 | EP em criação, edição e domínio | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-06 |
| CT-08 | O cadastro respeita a fronteira específica do tipo | R3 | EP; BVA 3-valores; domínio condicionado | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-07, M-08, M-09 |
| CT-09 | A edição revalida tipo e valor em conjunto | R3 | EP; BVA 3-valores; domínio condicionado | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-10 |
| CT-10 | O percentual inválido é recusado também na escrita direta | R3 | EP; BVA 3-valores; domínio condicionado | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-11, M-71 |
| CT-11 | A criação distingue colisão local e código de outra organização | R4 | Identidade; criação/edição/uso; BVA cardinalidade | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-12 |
| CT-12 | A edição ignora o próprio código e recusa código de outro cupom local | R4 | Identidade; criação/edição/uso; BVA cardinalidade | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-13, M-15 |
| CT-13 | A unicidade impede duplicata pela via direta | R4 | Identidade; criação/edição/uso; BVA cardinalidade | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-14 |
| CT-14 | O usuário comum e o perfil infra não escrevem por componente | R5 | Matriz papel×ação; papel acumulado; revogação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-16 |
| CT-15 | O domínio aplica a matriz de autorização em cada verbo | R5 | Matriz papel×ação; papel acumulado; revogação | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-17, M-20 |
| CT-16 | A autorização é refeita depois da revogação | R5 | Matriz papel×ação; papel acumulado; revogação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-18 |
| CT-17 | Papéis acumulados não anulam a autorização administrativa | R5 | Matriz papel×ação; papel acumulado; revogação | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-19 |
| CT-18 | UUID de outra organização não permite editar nem excluir | R6 | IDOR; discriminante nulo; troca de contexto | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-21 |
| CT-19 | A saída efetiva da recusa leva a leitura alcançável | R6 | IDOR; erro com saída; destino efetivo | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-67 |
| CT-20 | Um objeto de outra organização não é aplicável pelo chamador local | R6 | IDOR; discriminante nulo; troca de contexto | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-22 |
| CT-21 | Sem organização corrente o modo multi-tenant fecha | R6 | IDOR; discriminante nulo; troca de contexto | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-23 |
| CT-22 | Ativo requer validade futura e uso disponível | R7 | Tabela de decisão completa; BVA temporal/uso; paginação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-24, M-72, M-73 |
| CT-23 | A listagem mantém o recorte em 0, 1 e mais de uma página | R7 | Tabela de decisão completa; EP; paginação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-25 |
| CT-24 | A busca não reabre o recorte de atividade e tenant | R7 | Tabela de decisão completa; EP; paginação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-26 |
| CT-46 | O cupom removido não aparece na listagem do componente | R7 | Tabela de decisão completa; EP; paginação | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-64 |
| CT-25 | O instante exato da expiração já é inválido | R8 | BVA 3-valores; tempo; TOCTOU | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-27 |
| CT-26 | Uma consulta válida anterior não autoriza um cupom que expirou | R8 | BVA 3-valores; tempo; TOCTOU | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-28 |
| CT-27 | A comparação usa o mesmo instante entre fuso local e UTC | R8 | BVA 3-valores; tempo; TOCTOU | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-29 |
| CT-28 | O limite autoriza somente usos ainda disponíveis | R9 | BVA 3-valores; TOCTOU; concorrência | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-30 |
| CT-29 | O objeto desatualizado não ultrapassa o último uso | R9 | BVA 3-valores; TOCTOU; concorrência | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-31 |
| CT-30 | Duas aplicações simultâneas disputam a última unidade | R9 | BVA 3-valores; TOCTOU; concorrência | G-X | Pest feature HTTP | tests/Kit/CupomTest.php (arnês isolado; proposto) | M-32, M-33 |
| CT-31 | O percentual inteiro trunca apenas a fração do desconto | R10 | EP; BVA 3-valores escalado; exemplo discriminante | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-34, M-35, M-36 |
| CT-32 | O desconto fixo nunca produz total negativo | R10 | EP; BVA 3-valores escalado; exemplo discriminante | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-37, M-38 |
| CT-33 | A inexistência e cada condição inválida recusam sem efeitos | R11 | EP isolada; defesa no uso; não-efeito | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-39, M-40, M-42, M-51 |
| CT-34 | Percentual inválido persistido por outra via não é consumido | R11 | EP isolada; defesa no uso; não-efeito | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-41 |
| CT-47 | Expirado e esgotado juntos também recusam a aplicação | R11 | EP isolada; defesa no uso; não-efeito | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-65 |
| CT-35 | Ambos os tipos incrementam uma vez o contador persistido | R12 | Rastreio de efeito por partição | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-43, M-44, M-45 |
| CT-36 | A aplicação registra pessoa e instante sem depender de eventos do cupom | R13 | Rastreio; guard×argumento | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-46, M-47, M-76 |
| CT-37 | Aplicações distintas preservam toda a história e autoria | R13 | Rastreio; alvo×não-alvo local | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-48, M-77 |
| CT-38 | Falha ao inserir a trilha desfaz o consumo anterior | R13 | Rastreio: acontece; não acontece; uma vez; atomicidade | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-49 |
| CT-39 | Falha depois da trilha desfaz também o registro | R13 | Rastreio: acontece; não acontece; uma vez; atomicidade | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-50 |
| CT-40 | A chave inexistente não gera edição nem nova exclusão | R14 | Estado×operação; chave inexistente; 2-switch | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-52, M-54 |
| CT-41 | Excluir e aplicar por objeto retido recusa a aplicação | R14 | Estado×operação; chave inexistente; 2-switch | G-A | Pest feature HTTP | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php (propostos) | M-53 |
| CT-42 | Campos protegidos enviados pelo formulário não alteram a fronteira | R15 | Mass assignment por entidade; criação/edição | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-55 |
| CT-43 | A escrita direta também protege organização e contador | R15 | Mass assignment por entidade; criação/edição | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-56, M-57 |
| CT-44 | Ordenação e busca adulteradas conservam o recorte | R16 | Superfície Livewire; domínio e tipo inválidos | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-58, M-59 |
| CT-45 | Trocar a identidade do registro entre requests não muda o alvo | R16 | Superfície Livewire; domínio e tipo inválidos | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-60 |
| CT-48 | Cada administrador herdado alcança e opera as superfícies de escrita do painel | R5 | Matriz papel×ação×superfície | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-69 |
| CT-49 | Excluir cupom usado conserva imediatamente a prova de autoria e instante | R13 | Rastreio de efeito; uso→exclusão | G-D | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php + tests/Kit/CupomTest.php (propostos) | M-74 |
| CT-50 | A entrada somente data persiste a validade no fim do dia escolhido | R1 | Conversão; criação/edição; fim do dia | G-C | componente Livewire/Filament | tests/Tenancy/CupomTenancyTest.php + par Kit (propostos) | M-70 |
| CT-51 | Aplicar o objeto local mantém identidade e organização quando o código também existe fora | R6 | Identidade×contexto no sucesso; alvo×não-alvo | G-A | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (proposto; específico multi-tenant) | M-75 |
| CT-B01 | Unidade reativa do valor | R17 | EP do tipo | G-B | browser | tests/BrowserTenancy/CupomTest.php (proposto) | M-61, M-63 |
| CT-B02 | Erro visível corrigível | R17 | EP/BVA do percentual | G-B | browser | tests/BrowserTenancy/CupomTest.php (proposto) | M-62 |

## Revisão adversarial

**CONCLUÍDA — duas rodadas independentes, teto atingido.** Rodada 1: `/root/adversarial_71_c1`; rodada 2: `/root/adversarial_71_c1_r2`. Ambos em Codex/contexto novo, família GPT-6 herdada, esforço ultra solicitado; IDs exatos das implantações não expostos. Rota com corpo do contrato instalado `agents/fw-adversario-ct.md`, adaptando a rota Claude/opus da skill. Entradas autorizadas apenas 00 + 04 + 05; sem PRD, implementação, conversa de derivação ou dados de outros conjuntos. Relatórios `adversarial-1.md` e `adversarial-2.md` nesta pasta. Nenhuma autorrevisão.

Rodada 1: **11 achados distintos**, todos fechados abaixo pelo executor por orientação do orquestrador. **3 cenários novos** e **8 reforços de oráculo existente**. Há 7 mutantes novos provenientes da revisão e 4 mutantes existentes corrigidos; a primeira microprova aritmética foi executada pelo adversário em expressões PHP autocontidas, sem bootstrap da aplicação. O relatório conferiu estrutura e todas as 67 linhas originais do gate; isso não é execução de CT, browser ou mutation testing.

| Achado | Resolução | Evidência e limite |
|---|---|---|
| ADV-01 | Oráculo reescrito: CT-31/M-34 | 29% de 100 deve devolver 71; float específico devolve 72 na microprova independente. Retirada a falsa divergência 7101 do exemplo 29%/10000 |
| ADV-02 | Oráculo reescrito: CT-02/03; M-68 novo | Create afirma limite exato 3; save afirma limite exato 5, além de valor e preservação dos efeitos. Q3 só deixa aberto o domínio não decidido |
| ADV-03 | Cenário novo CT-50; M-70 novo | Entrada somente data persiste 23:59:59 no fuso da aplicação, em create/edit. Guarda condicional dada pelo 00; se houver data e hora, conferir o instante informado, sem impor formato de UI |
| ADV-04 | Cenário novo CT-49; M-74 novo; L6 delimitada | A própria exclusão do cupom não destrói imediatamente a aplicação registrada para auditoria posterior. Prazo futuro/remoção de usuário continuam lacuna, sem inventar política |
| ADV-05 | Cenário novo CT-48; M-69 novo | admin_organizacao, admin e master_global visitam create/edit e concluem create/save/delete nas superfícies reais do painel. A via direta de CT-15 continua separada |
| ADV-06 | Oráculo reescrito: CT-10; M-71 novo | Fração 12,5 recusada em create/edit direto, sem cupom novo nem mutação do alvo/histórico. P-05 já fixa percentual inteiro |
| ADV-07 | Oráculo reescrito: CT-21/M-23 | Snapshot global não escopado de cupons/aplicações permanece igual; recusa de criação não admite quarto cupom nulo |
| ADV-08 | Oráculo reescrito: CT-22; M-72 novo | Listagem nos dois tipos em T−1s/T/T+1s, com relógio T; igualdade não aparece |
| ADV-09 | Oráculo reescrito: CT-22; M-73 novo | Legado futuro usos 4/limite 3 não aparece em nenhum tipo; consulta preserva contador/trilha |
| ADV-10 | Oráculo reescrito: CT-19/M-67 | A saída realmente produzida pela recusa é seguida/observada e não volta à escrita proibida; removido GET manual que mascarava o destino |
| ADV-11 | Oráculo reescrito: CT-17/M-19 | Dez pares × três verbos × duas ordens efetivamente enumeradas = 60 linhas; panel_user primeiro continua autorizado quando acumula administrador |

Rodada 2: **5 achados distintos**, todos fechados abaixo. **1 cenário novo** e **4 reforços de oráculo/matador existente**. São 3 mutantes novos (M-75–77) e 2 matadores existentes corrigidos (M-25/M-60). Não houve nova microexecução aritmética, aplicação, Pest, browser ou mutação nesta revisão.

| Achado (rodada 2) | Resolução | Evidência e limite |
|---|---|---|
| ADV-01 | Cenário novo CT-51; M-75 novo | Objeto Acme permitido com código também presente em Globex; consulta global discriminante resolveria Globex primeiro. Espera 9000, consumo/trilha Acme e snapshot Globex intacto, contra 7000/efeitos Globex |
| ADV-02 | Oráculo reforçado CT-36; M-76 novo | Guard ausente, Beto ou Ana × dois tipos; argumento aplicadoPor é Beto em todas as linhas e a aplicação registra somente Beto/T |
| ADV-03 | Oráculo reforçado CT-37; M-77 novo | A local é primeiro e B é o alvo; somente B ganha Beto/T, sem alterar contador/trilha/snapshot de A. Mantida também a história anterior de B |
| ADV-04 | Fixture/oráculo reforçados CT-23/M-25 | Linha 11 comprova Z_EXPIRADO/Z_GLOBEX nas posições 12/13 da consulta sem filtros e na página 2; listagem real devolve só A01–A11. Não cria regra de ordenação de negócio |
| ADV-05 | Matador M-60 reescrito; CT-45 mantido | A asserção discrimina recusa da troca e ausência de atributos GLOBEX na resposta, como o Então já exigia; preservação do banco isolada foi retirada como matador suficiente |

Não há ADV da rodada 1 ou 2 sem destino nem fechamento aguardando decisão. As seis lacunas L1–L6 continuam delimitadas pelo requisito ou entrada ausente; não são achados deixados sem resolução. A revisão terminou por seu teto obrigatório, sem declaração de cobertura aprovada.

**Débito D-01 — alterações finais sem nova revisão independente.** CT-51 nasceu no fechamento da rodada 2; os reforços finais de CT-23/36/37 e M-25/M-60, além de M-75–77, também não foram reexaminados por adversário depois da edição. Não haverá terceira rodada nem autorrevisão para substituir essa limitação. Escalado ao orquestrador: R13 cresceu para 9 mutantes, com identidade/autoria e atomicidade como eixos distintos; futura manutenção deve avaliar separar essas regras, preservando as referências. A conferência deste executor verifica apenas consistência mecânica das edições, IDs, contagens e índice.

Restrição efetiva deste executor e declarada pelos adversários: ferramentas com filesystem irrestrito (`danger-full-access`), cwd explícito project-71 e contratos de leitura/escrita por instrução; nenhum sandbox mecânico de leitura. Os adversários não receberam catálogo ou resultados comparativos, não leram plano/código e não tentaram leitura fora da lista. Na rodada 2, o fechamento da rodada 1 incorporado ao 04 foi exposto incidentalmente; não foi aberto o relatório da rodada 1 nem o retorno. Essa exposição limita a cegueira informacional e não é ocultada como isolamento perfeito. O frontmatter Claude de tools/model/hooks não se aplica neste host. Prompt, hook heurístico e git status não são prova de isolamento.

## Execução futura, separada da revisão

Nenhum CT Pest, browser, disputa concorrente ou pest --mutate foi executado por este executor ou pelos revisores. A única microexecução foi a prova PHP autocontida de constantes na rodada 1. A materialização futura deverá conferir costuras, posições discriminantes, seletores, transações e efeitos reais, executar as suítes nos modos pertinentes e medir mutação pelo procedimento Windows. Não há MSI, DDR, evidência de feature verde ou driver de cobertura confirmado nesta entrega.

## Verificação de entrega

- Especificação somente: não criado teste Pest, app, migration, model, 02 ou 03.
- Não lidas pastas de outras execuções nem catálogos/relatórios; references/casos-medidos não aberto por restrição do prompt.
- Conferir contagens/IDs/seções/exemplos por leitura determinística desta saída. Nenhuma claim de DDR, MSI, equivalência de host, economia de tokens ou comportamento verde.
- Pós-implementação deverá medir Pest, browser, concorrência real e mutation pelo lançador Windows, duração e sobreviventes. Driver de cobertura não foi investigado; não declarar ausente. Referências abertas e despachos serão registrados no retorno-c1.md (03 proibido).

