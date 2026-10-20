# Casos de Teste — FERRO-812: Cupons de desconto

> Derivado do **requisito**, não do plano. Nenhum cenário foi derivado da implementação da feature.
> Fonte: `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md`.
> Plano lido por exigência da rodada; somente paths, rotas e superfície de UI foram admitidos na derivação.
> Skills locais: feature-wiki **[VERSÃO ANONIMIZADA]**, feature-test-design **[VERSÃO ANONIMIZADA]**.
> Data: 2026-10-20. Host: Codex, Windows/PowerShell; modelo informado: GPT-6, variante exata não exposta.
> Revisão adversarial: **duas rodadas independentes**, 9 + 3 achados fechados. Ajustes finais da rodada 2 não tiveram terceira revisão, pelo teto da skill.
> Entrega exclusivamente de especificação; nenhum teste executável ou código de produto será criado.

## Perfil de Derivação

Perfis **decididos pelo passo 0**, nenhum imposto pela rodada.

| Área | P | I | P×I | Perfil | Justificativa |
|---|---|---|---|---|---|
| Cadastro e validação | 3 | 3 | 9 | completo | Tipo condiciona valor; criação e edição afetam dinheiro |
| Motor, consumo e auditoria | 3 | 3 | 9 | completo | Validade, cálculo, disputa pelo último uso e transação financeira |
| Autorização e isolamento | 3 | 3 | 9 | completo | Papéis, organizações, contexto corrente e escrita por múltiplas entradas |
| Operação da interface | 2 | 2 | 4 | padrão | Integração com componentes do painel; erro causa retrabalho |

Há **Impacto 3** nas três primeiras áreas. Regra que cruza áreas herda o maior perfil.
Executados passos 1–7 integrais nas áreas completas; na interface, 1–7 sem pairwise e BVA de dois valores quando aplicável.
BVA financeiro/temporal usa três valores. Nenhum perfil foi rebaixado para caber no teto.
Contagem: Cenários: **55** · Regras: **16** · Mutantes previstos: **72** · Sem matador: **0**. CT-B: **0**.

## Gate de entrada e limites da execução

- O `00` não tem coluna Estado nem uma seção separada chamada Premissas. As P-01–P-09 estão nas ambiguidades. Pela instrução expressa da rodada, valem como dadas; as perguntas históricas não reabrem essas decisões.
- RQ-01–RQ-15 são consideradas determinadas nos limites dessas premissas. Perguntas novas abaixo bloqueiam apenas o recorte não determinado.
- `02-decisoes-arquiteturais.md` **ausente**, confirmado por `Test-Path`. Não criado. Não há inventário autorizado de métodos/propriedades Livewire; cobertura exaustiva dessa superfície é lacuna L-SUP.
- `wikis/glossario.md` ausente. Termos de domínio seguem o `00`.
- `composer show --direct`: “No dependencies installed. Try running composer install or update.”; `Test-Path vendor`: False.
- Versões **travadas**, não instaladas: Laravel 13.25.0; Filament/forms 5.7.6; Livewire 4.4.0; Pest 5.1.1; browser 5.0.1; mutate 5.0.2. PHP CLI 8.4.10, Xdebug 3.4.4.
- Mutate consta do lock, mas não de `require-dev`; não confundir dependência transitiva com declaração direta. Não se alterou dependência.
- Boost/search-docs não está exposto nas ferramentas desta sessão. Nenhum código foi alterado. APIs de teste consultadas em documentação oficial; confirmação pontual no vendor permanece pendente.
- `git status --porcelain` devolveu “fatal: not a git repository (or any of the parent directories): .git”. Integridade será conferida por hashes, sem depender de diff.
- Não houve execução de PHPUnit/Pest, browser ou mutation testing. O passo 6 é previsão falsificável, não MSI medido.

## Varredura SFDIPOT

| Letra | Dimensões levantadas antes dos cenários | Destino |
|---|---|---|
| S | Cupom, registro de uso, enum de tipo, cadastro do painel e permissões; nenhum Pedido novo | R1–R16; L-IDEMP |
| F | Criar, editar, excluir, listar, localizar, aplicar, calcular, consumir e registrar autoria/instante | Mapa e matriz abaixo |
| D | Campos obrigatórios; dois tipos; centavos; duplicidade local; mesmo código em duas organizações; ator diferente do operador da fixture | R2–R8, R12–R14 |
| I | Rotas do Resource, componente e chamadas diretas de domínio; não existe tela de aplicação no escopo | R1, R7–R11 |
| P | SQLite :memory: no arnês; duas conexões reais para disputa; colação e unicidade com tenant nulo; UI validada por componente | R6, CT-36, CT-50 |
| O | admin_organizacao, panel_user, master_global, admin e infra; papéis acumulados; nenhum/um/muitos registros | R7, R8, R15 |
| T | Instante exato de expiração, tempo entre consulta e consumo, objetos obsoletos, meia-noite, fuso, concorrência | R10–R14 |

## Matriz única de estado × operação

Situações são predicados derivados da P-03, não enum ou coluna inventados.
Estados: ativo; expirado com saldo; esgotado com validade futura; expirado e esgotado; removido.
Operações sobre um cupom já identificado: consultar código, aplicar, listar como panel_user, editar como admin da organização, excluir como admin.
Produto fechado: **5 × 5 = 25 células**: 8 válidas, 14 inválidas, 3 lacunas de comportamento.
As duas células “listar” sem registro são negativas de leitura, não recusas de escrita.
Criar não tem registro prévio: suas classes de entrada são cobertas separadamente em R1–R6.
Personas proibidas cruzam os verbos em R7; campos decisivos fora do estado inicial entram em Q4 e CT-35.

| Estado de partida | Consultar código | Aplicar | Listar (panel_user) | Editar (admin) | Excluir (admin) |
|---|---|---|---|---|---|
| Ativo | válida CT-29 | válida CT-31/34 | válida CT-45 | válida CT-03/05 | válida CT-04 |
| Expirado, saldo disponível | inválida CT-31 | inválida CT-31/32 | inválida CT-45 | lacuna Q4 | válida CT-55 |
| Esgotado, validade futura | inválida CT-34 | inválida CT-34/35 | inválida CT-45 | lacuna Q4 | válida CT-55 |
| Expirado e esgotado | inválida CT-47 | inválida CT-47 | inválida CT-45 | lacuna Q4 | válida CT-55 |
| Removido | inválida CT-30 | inválida CT-48 | inválida CT-45 | inválida CT-49 | inválida CT-49 |

Legenda: consultar inválido = nenhum cupom retornado; aplicar inválido = nenhum total descontado, contador e linhas de uso inalterados;
editar inválido = registro não recriado e campos originais de outros cupons preservados; excluir inválido = nenhum outro cupom apagado.
Listar inválido = identidade ausente do conjunto retornado, sem confundir isso com uma tentativa de consumo.
CT-45 executa listagem; CT-47 executa consulta e aplicação em instâncias independentes, como linhas distintas de Exemplos.
As três lacunas não contam como células testadas. Toda coluna tem pelo menos uma operação válida exercitada.
Nenhuma renovação ou alteração de limite em estado vencido/esgotado foi declarada permitida só porque o PRD a permite.

## Tabela de decisão da elegibilidade

| Existe no contexto? | Dentro da validade? | Tem uso disponível? | Resultado | CT |
|---|---|---|---|---|
| não | — | — | recusa sem consumo/trilha | CT-29/30 |
| sim | sim | sim | aplica e registra uma vez | CT-39/42 |
| sim | não | sim | recusa sem consumo/trilha | CT-31 |
| sim | sim | não | recusa sem consumo/trilha | CT-34 |
| sim | não | não | recusa sem consumo/trilha | CT-47 |

Tabela completa das combinações **viáveis**. Para inexistente, validade e contador não têm referente: quatro combinações booleanas seriam artificiais.
Partições inválidas isoladas têm linhas próprias; a linha de dupla inelegibilidade não é usada como prova de cada validação isolada.

## Mapa de Regras

| Regra | Área/perfil herdado | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — CRUD operável | Cadastro/completo | RQ-01–RQ-06, P-09 | EP, estado × operação | CT-01–05 |
| R2 — Campos obrigatórios | Cadastro/completo | RQ-02–RQ-06 | EP por campo e entrada | CT-06–08 |
| R3 — Tipo fechado | Cadastro/completo | RQ-03, P-05 | EP | CT-09–10 |
| R4 — Valor por tipo | Cadastro/completo | RQ-04, P-05 | EP, BVA 3, decisão tipo × valor | CT-11–13, CT-50 |
| R5 — Validade e contagem têm representação válida | Cadastro/completo | RQ-05–RQ-06 | EP, BVA no uso em R10/R11 | CT-14–17 |
| R6 — Identidade única no contexto | Cadastro/isolamento, completo | RQ-14, P-04 | EP local/outro tenant; edição contra si | CT-18–20, CT-51 |
| R7 — Escrita reservada aos admins | Autorização/completo | RQ-07–RQ-08, P-02 | matriz papel × ação, combinação de papéis | CT-21–24 |
| R8 — Organização não atravessa a fronteira | Isolamento/completo | P-02, P-04, RQ-07–RQ-09, RQ-15 | IDOR, mass assignment, contexto nulo | CT-25–28, CT-52–53 |
| R9 — Existência reconferida | Motor/completo | RQ-09, P-01 | EP inexistente/removido | CT-29–30, CT-47 |
| R10 — Validade no instante de aplicação | Motor/completo | RQ-10, RQ-05, definição temporal do 00 | BVA 3 de 1 segundo, contexto temporal | CT-31–33 |
| R11 — Limite resiste a leituras obsoletas e concorrência | Motor/completo | RQ-11, RQ-13 | BVA 3, estado × evento, concorrência | CT-34–36 |
| R12 — Total calculado sem perder centavos | Motor/completo | RQ-12, P-01, P-05–P-07 | EP, BVA 3 de centavo | CT-37–38 |
| R13 — Consumo exato e atômico | Motor/completo | RQ-11–RQ-13, RQ-15 | rastreio de efeito por tipo | CT-39–41 |
| R14 — Autoria e instante auditáveis | Motor/completo | RQ-15, P-08 | rastreio de efeito por tipo e atomicidade | CT-42–44, CT-54 |
| R15 — Leitura restrita aos ativos | Autorização/completo | RQ-08, P-03 | decisão completa, EP 0/1/N, paginação | CT-45–46 |
| R16 — Removido não opera | Cadastro/motor, completo | RQ-01, RQ-07, RQ-09 | estado × operação, CRUD negativo | CT-48–49, CT-55 |

Cada ID existente tem definição e índice. Nenhuma RQ inteira foi reaberta.
R5 reúne somente representação dos dois campos; suas fronteiras de negócio são regras separadas R10/R11.
Pairwise: não usado como redutor de condições de dinheiro/autorização; combinações críticas estão exaustivas nas decisões, nos dois tipos e na matriz papel × verbo.
Teto: R1 tem cinco CT. R8 tem seis CT: exceção explícita pelo gate, para separar IDOR no componente, model, consumo, payload e contexto nulo. Os demais respeitam cinco, contando cada Esquema como um CT. R4 tem sete mutantes: o sétimo veio da revisão adversarial (M-73), exceção explícita ao teto de seis da skill.
Recortes não determinados: RQ-02 Q1/Q2; RQ-04 Q3; RQ-05–06 Q4; RQ-07 Q5/Q8; RQ-08 Q9/Q10; RQ-14 Q2/Q9; RQ-15 Q7/Q8.
As partes determinadas continuam nos CT acima.

## Costuras de Teste

Confirmadas **pela sessão principal em 2026-10-20**, antes dos cenários, com base na autorização expressa da rodada e nas convenções existentes.
Nomes de arquivo abaixo são destinos **propostos**, não arquivos criados.

| Grupo | Regras | Costura | Existente ou nova | Motivo | Confirmada |
|---|---|---|---|---|---|
| DOM | R2–R6, R7, R9–R14, R16 | Pest feature HTTP | existente: arnês tests/Kit | Domínio direto com container, casts, DB e permissões | sessão, 2026-10-20 |
| TEN | R6–R8, R14–R15 | Pest feature HTTP | existente: arnês tests/Tenancy | Contexto antes das migrations e dois tenants reais | sessão, 2026-10-20 |
| CMP | R1–R8, R15–R16 | componente Livewire/Filament | existente: testes de componente em Kit/Tenancy | Formulário, gravação, ações, lista e estado do schema | sessão, 2026-10-20 |
| RACE | R11 | Pest feature HTTP | nova fixture de execução concorrente, usando arnês de app existente | :memory: não compartilha dados entre processos; duas conexões reais no mesmo DB descartável | sessão, 2026-10-20 |

Não alocado Unit: tests/Unit não recebe TestCase/container no Pest.php; o cálculo exposto pela P-01 envolve Cupom, casts e app.
Feature aqui inclui método/model direto, embora os destinos locais sejam tests/Kit e tests/Tenancy.
A componente não substitui os CT diretos de validação e autorização.
Gate do 05 **não satisfeito** após ADV-08: não há requisito que dependa de JS, pixel ou acessibilidade. O 05 do rascunho foi retirado; nenhuma costura é browser.

## Fronteira com o Plano

| Item lido no 01 | Tratamento | Destino |
|---|---|---|
| CupomResource, Pages ListCupons/CreateCupom/EditCupom, cupons/cupom_usos | somente endereços e nomes técnicos | Setup e índice |
| Cupom::valido/aplicarEm/descontoSobre | nomes de acesso; aplicarEm já consta também da P-01 | Detalhes de materialização, nunca retorno inferido do algoritmo do plano |
| código em maiúsculas/trim e teto 40 | 00 não fixa normalização nem teto | Q1/Q2; nenhum esperado copiado |
| mínimo 1 para valor fixo/limite, impedir validade passada ao cadastrar/editar | comportamento do PRD, não determinado no 00 | Q3/Q4; invariantes de aplicação mantidos |
| assinatura com autor opcional | contraria autoria exigida pelo 00 e User da P-01 | R14 testa autor válido; Q8 para ausência, sem copiar nullable como aceite |
| rótulos, sufixo, cor, ordenação default, prioridade Esgotado/Expirado | escolhas visíveis sem oráculo no 00 | Q10; CT-50 prova tipo/valor no componente, sem impor apresentação reativa |
| apagamento em cascata da trilha e nullOnDelete de autor | 00 pede auditoria, sem política de retenção | Q7/Q9; não declarar cascata comportamento correto |
| “unit” para motor e CT-B para todo CRUD | camada decidida pelo observável e arnês real | componente para CRUD; Feature para efeitos; nenhum requisito exclusivo de browser |
| logs técnicos | não são trilha RQ-15 | nenhum CT de log |

## Perguntas para o 00-requisito.md

**Desvio autorizado**: 00 e 01 imutáveis; perguntas ficam aqui, prontas para colagem. Não houve pergunta ao usuário indisponível.
Novas Q1–Q10 são locais desta derivação (o 00 usa A-01–A-09, não Qn); não alteram P-01–P-09 já assumidas.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | Qual teto de caracteres do código, e aceitam-se acentos/emoji? | RQ-02 | Definir domínio explícito e recusar fora dele; não importar 40 do plano | aberta |
| Q2 | Caixa e espaços nas bordas identificam o mesmo código? Qual normalização Unicode? | RQ-14/RQ-02 | Falhar fechado diante de identidade equivalente, com normalização acordada antes de gravar | aberta |
| Q3 | Valor fixo zero é válido? Qual teto de centavos e do total de entrada? | RQ-04/RQ-12 | Sinal negativo já é vedado pela P-05 unsignedInteger (CT-11/12); recusar fora da representação | aberta só para zero/teto |
| Q4 | Pode cadastrar/editar validade passada ou limite zero? Pode reduzir limite abaixo dos usos feitos ou renovar vencido/esgotado? | RQ-05/RQ-06 | Recusar criação de inelegibilidade, manter contador/trilha; aplicação de vencido/esgotado continua recusada | aberta |
| Q5 | A expressão apenas listar impede também aplicar pelo motor para panel_user, ou limita só o CRUD? | RQ-08/P-01 | Recusar aplicação sem autoridade definida; os cenários de motor usam admin e não respondem por esse papel | aberta só para aplicação por não admin |
| Q6 | Onde o futuro Pedido persistido identifica retries da mesma aplicação? | P-01/RQ-12/RQ-13 | Falhar fechado antes de consumo repetido da mesma intenção; não inventar Pedido agora | lacuna de escopo L-IDEMP |
| Q7 | Por quanto tempo o uso e a identidade do autor sobrevivem à exclusão do cupom/usuário? | RQ-15 | Preservar evidência de auditoria; não apagar trilha silenciosamente | aberta |
| Q8 | Como o chamador externo comprova identidade/autorização do autor informado? | RQ-15/P-01/RQ-07 | Recusar identidade não comprovada; ausência/null do argumento já são recusados por P-01, sem depender desta resposta | aberta só para autenticação externa; CT-54 cobre ausência |
| Q9 | Admin pode listar inativos? Código de cupom excluído pode ser reutilizado? | RQ-01/RQ-07/RQ-08/RQ-14 | Manter inativos fora da lista comum e não reutilizar identidade até definir retenção; a exclusão administrativa do cadastro já é determinada | aberta só nos recortes extras |
| Q10 | Qual apresentação de unidade/rótulo, ordenação e desempate? | RQ-01/RQ-03/RQ-04/RQ-08 | Unidade coerente com P-05; ordenação determinística; sem texto/cor inventados | aberta só na apresentação exata |

Formato da raia, aplicável a cada linha:
❓ Q1–Q10 · raia: requisito · afeta: conforme tabela · depende de: —.
➡️ Recomendações acima seguem falha fechado. Não são respostas nem cenários direcionais enquanto abertas.

## Setup Global

- Fontes de convenção lidas: tests/Pest.php, tests/TestCase.php, tests/TenancyTestCase.php, tests/Kit/PaginasInfraTest.php, trecho de tests/Tenancy/TenancyTest.php e tests/BrowserTenancy/IdentidadeVisualTest.php.
- RefreshDatabase já ligado a Kit/Tenancy/BrowserTenancy. TenancyTestCase configura modo antes de boot/migrations; não ligar teams tardiamente.
- User::factory e Tenant::factory existem. Tenant tem inativo/comIdentidadeVisual; User tem unverified. CupomFactory **não existe** na lista de factories observada; usar criação de domínio com campos explícitos até existir factory validada, sem presumir states planejados.
- Semear ShieldPermissionsSeeder e PapeisSeeder pela sobrescrita TestCase::seed existente, somente no ambiente de teste futuro. Nesta rodada não executar seeders que possam gerar arquivos.
- Personas: usuário A e B distintos. Multi-tenant: Acme e Globex, vínculo real; usuarioComPapel/papelNaOrganizacao, noPainelDa, setPermissionsTeamId e limpeza das relações/cache conforme helpers existentes.
- Single-tenant: master_global para escrita autorizada e panel_user para recusa/leitura. P-02 afirma acesso também ao admin da instalação; essa premissa prevalece sobre a matriz contraditória do PRD. O comportamento do motor para panel_user permanece Q5.
- Autenticar antes de Livewire. Filament::setCurrentPanel('app'); selecionar tenant nos testes de componente com noPainelDa. URLs por nome; record usa getRouteKey()/uuid.
- Fixtures normais: codigo PROMO10; porcentagem 10, valor fixo 1000; validade futura; limite 3; usos iniciais 0. Cada teste independente restaura relógio/contexto.
- Estado derivado se constrói por **operações reais**: ativo por cadastro; esgotado por três aplicações válidas; expirado por avançar relógio; removido por exclusão autorizada. Nunca gravar situacao nem simular consumo apenas alterando usos.
- Para usos > limite ou dados legados malformados, usar fixture de corrupção identificada, por DB, após construir registros válidos. Essa exceção testa tolerância de fronteira e não substitui a máquina de estados.
- Helper futuro cupomEm se compartilhado deve morar em tests/Pest.php, somente especificado aqui. Não criar função duplicada em arquivos irmãos.
- Para cada negativa, cupom, usuário aplicador e destino de trilha existem; contagem inicial explícita. “Inalterado” sempre significa comparar os campos e as linhas nomeados antes/depois.
- Nomes de efeitos deste escopo: valor final devolvido; contador de usos persistido; linha cupom_usos com cupom/autor/instante. Não inventar e-mail/job/notificação de aplicação.
- Recusa de cadastro/edição: nenhum novo cupom, campos antigos preservados, usos e cupom_usos preservados. Não fazer assertHasFormErrors genérico: apontar somente campo alvo.
- APIs: Livewire::test, fillForm, call('create'|'save'), assertSchemaStateSet e assertDatabaseHas com campos de negócio; TestAction::make('delete')->table($cupom), callAction. Edição não exige redirect.
- APIs conferidas nas [docs oficiais de recursos Filament 5](https://filamentphp.com/docs/5.x/testing/testing-resources) e [ações](https://filamentphp.com/docs/5.x/testing/testing-actions); browser nas [docs do Pest](https://pestphp.com/docs/browser-testing). Inspeção do vendor 5.7.6 indisponível; evitar helpers depreciados.
- Sem fakes globais de eventos. Falha injetada em R13/R14 só após fixture válida; não bloquear criação de UUID. A transação é requisito de consistência dos efeitos, não assertion sobre número de chamadas SQL.
- RACE: dados commitados em banco descartável compartilhado por duas conexões/processos, sem transação externa que esconda fixture. Barreira faz ambos carregarem saldo antes de liberar consumo; capturar resultados e consultar DB fresco. :memory: em duas conexões não prova disputa. Fixture executável não foi construída nesta rodada.
- Precisão: php -r conferiu no PHP 8.4.10: intdiv(100 * 29, 100) = 29; (int)(100 * 0.29) = 28. O mutante discrimina 71 versus 72 de total; nunca escrever valor monetário de fixture como float.


Atualização parcial direta não equivale a apagar campo: CT-08 exclui omissão na edição; seus null/vazio representam remoção efetiva. Obrigatoriedade não impõe payload integral em updates. Omissão com default que produz entidade válida não é erro por si só.


## Regra R1 — CRUD operável no painel

> Origem: RQ-01–RQ-06, P-09. Perfil: completo. Técnica: EP e estado × operação.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: CRUD operável no painel

    Esquema do Cenário: [CT-01] Visitar criação e edição apresenta os dados do cupom
      Dado o admin autorizado no painel app e um cupom ativo PROMO10 de porcentagem 10, validade futura e limite 3
      Quando o admin visita a rota <tela>
      Então o formulário apresenta código, tipo, valor, validade e limite
      E na edição os valores correspondem exatamente ao cupom persistido, sem alterar usos 0 nem criar uso
      Exemplos:
        | tela | classe |
        | criar | formulário novo |
        | editar UUID de PROMO10 | formulário preenchido |

    Esquema do Cenário: [CT-02] Criar preserva todos os campos para os dois tipos
      Dado o admin autorizado e os campos válidos código NOVO, tipo <tipo>, valor <valor>, validade 2026-11-01T12:00:00-03:00 e limite 3
      Quando o admin cria o cupom pelo componente
      Então existe exatamente um NOVO no contexto corrente com esses cinco campos e usos 0
      E não existe linha de aplicação para NOVO
      Exemplos:
        | tipo | valor | classe |
        | porcentagem | 29 | percentual |
        | fixo | 101 | centavos |

    Cenário: [CT-03] Editar troca os campos decisivos sem consumir uso
      Dado o admin e um cupom ativo PROMO10, porcentagem 10, com um uso real já registrado
      Quando o admin salva pelo componente o código NOVO, tipo fixo, valor 1001, validade 2026-11-02T15:00:00-03:00 e limite 4
      Então o mesmo cupom tem os cinco novos valores persistidos
      E usos permanece 1 e a única linha de uso anterior permanece idêntica

    Cenário: [CT-04] Admin exclui cupom ativo e a lista deixa de retorná-lo
      Dado o admin e dois cupons ativos PROMO10 e OUTRO, sem usos
      Quando o admin executa a ação de exclusão de PROMO10 no componente
      Então PROMO10 deixa de existir na consulta do cadastro e da listagem
      E OUTRO preserva todos os campos e usos 0

    Cenário: [CT-05] Salvar o próprio código sem alteração não colide consigo
      Dado o admin e um cupom ativo PROMO10 com todos os campos válidos
      Quando o admin salva a edição sem mudar campo algum
      Então persiste um único PROMO10 com todos os valores originais
      E a edição não produz erro de duplicidade nem cria uso
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Gravar apenas código e perder tipo/valor/validade/limite | CT-02 | cinco campos persistidos iguais aos enviados, para cada tipo |
| M-02 | Salvar edição como novo cupom | CT-03 | mesma identidade com os cinco campos alterados; não há duplicata |
| M-03 | Filtrar a lista após excluir sem remover o cupom | CT-04 | consulta do cadastro não encontra PROMO10, e OUTRO permanece |
| M-04 | Renderizar só layout e omitir os campos do formulário | CT-01 | criação apresenta os cinco campos; edição também mostra os valores do cupom |
| M-05 | Usar unique que colide com o próprio registro na edição | CT-05 | salvar sem alterações mantém um único PROMO10 e não dá erro |

## Regra R2 — Todo cupom possui os cinco campos obrigatórios

> Origem: RQ-02–RQ-06. Perfil: completo. Técnica: EP por campo e ponto de entrada.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Todo cupom possui os cinco campos obrigatórios

    Esquema do Cenário: [CT-06] Criação recusa um único campo obrigatório ausente
      Dado o admin e um formulário novo com todos os campos válidos exceto <campo> em <entrada>
      Quando o admin solicita criação pelo componente
      Então há erro especificamente em <campo> e nenhum cupom é criado
      E não há consumo nem linha de aplicação
      Exemplos:
        | campo | entrada | classe |
        | codigo | ausente | identificação |
        | codigo | null | identificação |
        | codigo | vazio | identificação |
        | tipo | ausente | tipo |
        | tipo | null | tipo |
        | tipo | vazio | tipo |
        | valor | ausente | desconto |
        | valor | null | desconto |
        | valor | vazio | desconto |
        | expira_em | ausente | validade |
        | expira_em | null | validade |
        | expira_em | vazio | validade |
        | limite_de_usos | ausente | limite |
        | limite_de_usos | null | limite |
        | limite_de_usos | vazio | limite |

    Esquema do Cenário: [CT-07] Edição recusa apagar um campo obrigatório
      Dado o admin e PROMO10 ativo com um uso real, com apenas <campo> alterado para <entrada>
      Quando o admin salva a edição pelo componente
      Então há erro especificamente em <campo> e os cinco campos persistidos continuam originais
      E usos permanece 1 e a linha de uso anterior permanece idêntica
      Exemplos:
        | campo | entrada | classe |
        | codigo | null | identificação |
        | codigo | vazio | identificação |
        | tipo | null | tipo |
        | tipo | vazio | tipo |
        | valor | null | desconto |
        | valor | vazio | desconto |
        | expira_em | null | validade |
        | expira_em | vazio | validade |
        | limite_de_usos | null | limite |
        | limite_de_usos | vazio | limite |

    Esquema do Cenário: [CT-08] Obrigatoriedade vale na escrita direta fora do formulário
      Dado o admin e um payload válido com somente <campo> em <entrada>, para <operacao>, de modo que o valor obrigatório ficaria removido da entidade
      Quando o admin grava pelo model ou pela entrada de domínio sem componente
      Então a escrita é recusada por esse campo sem criar cupom ou alterar os valores originais
      E o contador e as linhas de uso ficam inalterados
      Exemplos:
        | campo | entrada | operacao | classe |
        | codigo | ausente | criar | código |
        | codigo | null | criar | código |
        | codigo | null | editar | código |
        | codigo | vazio | criar | código |
        | codigo | vazio | editar | código |
        | tipo | ausente | criar | tipo |
        | tipo | null | criar | tipo |
        | tipo | null | editar | tipo |
        | tipo | vazio | criar | tipo |
        | tipo | vazio | editar | tipo |
        | valor | ausente | criar | valor |
        | valor | null | criar | valor |
        | valor | null | editar | valor |
        | valor | vazio | criar | valor |
        | valor | vazio | editar | valor |
        | expira_em | ausente | criar | validade |
        | expira_em | null | criar | validade |
        | expira_em | null | editar | validade |
        | expira_em | vazio | criar | validade |
        | expira_em | vazio | editar | validade |
        | limite_de_usos | ausente | criar | limite |
        | limite_de_usos | null | criar | limite |
        | limite_de_usos | null | editar | limite |
        | limite_de_usos | vazio | criar | limite |
        | limite_de_usos | vazio | editar | limite |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-06 | Exigir campos somente na criação | CT-07 | campo e cinco valores originais preservados após save |
| M-07 | Confiar apenas no required do formulário | CT-08 | escrita direta com campo ausente é recusada sem persistência |
| M-08 | Converter campo vazio para default válido | CT-06 | cada vazio gera erro no próprio campo; nenhum cupom novo |

## Regra R3 — Tipo admite somente porcentagem e fixo

> Origem: RQ-03, P-05. Perfil: completo. Técnica: EP.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Tipo admite somente porcentagem e fixo

    Esquema do Cenário: [CT-09] Formulário não grava um terceiro tipo
      Dado o admin e dados válidos de cupom, com apenas tipo igual a <entrada>
      Quando o admin executa <operacao> pelo componente
      Então há erro de tipo, e nenhum cupom novo ou alteração de campos é persistido
      E contador e trilha de aplicação permanecem iguais
      Exemplos:
        | entrada | operacao | classe |
        | cashback | criar | string fora do domínio |
        | cashback | editar | string fora do domínio |
        | 7 | criar | tipo escalar errado |
        | 7 | editar | tipo escalar errado |
        | array com porcentagem | criar | estrutura errada |
        | array com porcentagem | editar | estrutura errada |

    Esquema do Cenário: [CT-10] Tipo inválido não entra pelo model
      Dado o admin e um cupom ativo para edição ou payload novo válido, com somente tipo <entrada>
      Quando o admin solicita <operacao> diretamente ao domínio
      Então a escrita é recusada sem persistir o tipo inválido
      E os campos existentes, contador e linhas de uso permanecem iguais
      Exemplos:
        | entrada | operacao | classe |
        | cashback | criar | domínio inválido |
        | cashback | editar | domínio inválido |
        | 7 | criar | tipo errado |
        | 7 | editar | tipo errado |
        | array com fixo | criar | estrutura errada |
        | array com fixo | editar | estrutura errada |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-09 | Validar enum só na UI | CT-10 | cashback não fica persistido por escrita direta |
| M-10 | Tratar qualquer tipo desconhecido como fixo | CT-09 | cashback produz erro em tipo, não cupom de valor fixo |
| M-11 | Aceitar coerção numérica de tipo | CT-10 | 7 não vira um dos dois tipos persistidos |

## Regra R4 — O tipo determina a unidade e o domínio do valor

> Origem: RQ-04, P-05. Perfil: completo. Técnica: EP, BVA 3 e decisão tipo × valor.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O tipo determina a unidade e o domínio do valor

    Esquema do Cenário: [CT-11] Percentual respeita cada borda em criação e edição
      Dado o admin e os demais campos válidos, com tipo <tipo> e valor <valor>
      Quando o admin executa <operacao> pelo componente
      Então <resultado> e, se aceito, o valor inteiro <valor> fica persistido
      E se recusado há erro só em valor, nenhum novo cupom e nenhum campo, uso ou trilha alterado
      Exemplos:
        | tipo | valor | resultado | operacao | classe |
        | porcentagem | 0 | recusado | criar | mínimo−1 |
        | porcentagem | 0 | recusado | editar | mínimo−1 |
        | porcentagem | 1 | aceito | criar | mínimo |
        | porcentagem | 1 | aceito | editar | mínimo |
        | porcentagem | 2 | aceito | criar | mínimo+1 |
        | porcentagem | 2 | aceito | editar | mínimo+1 |
        | porcentagem | 99 | aceito | criar | máximo−1 |
        | porcentagem | 99 | aceito | editar | máximo−1 |
        | porcentagem | 100 | aceito | criar | máximo |
        | porcentagem | 100 | aceito | editar | máximo |
        | porcentagem | 101 | recusado | criar | máximo+1 |
        | porcentagem | 101 | recusado | editar | máximo+1 |
        | porcentagem | 12,5 | recusado | criar | fração não prevista pela P-05 |
        | porcentagem | 12,5 | recusado | editar | fração não prevista pela P-05 |
        | fixo | 1000,5 | recusado | criar | fração de centavo |
        | fixo | 1000,5 | recusado | editar | fração de centavo |
        | fixo | -1 | recusado | criar | sinal vedado por unsignedInteger da P-05 |
        | fixo | -1 | recusado | editar | sinal vedado por unsignedInteger da P-05 |

    Esquema do Cenário: [CT-12] As bordas percentuais também protegem a escrita direta
      Dado o admin e dados válidos exceto valor <valor> no tipo <tipo>
      Quando o admin executa <operacao> pelo model sem componente
      Então <resultado>, com valor inteiro exato quando aceito
      E uma recusa não persiste cupom, alteração, consumo ou linha de uso
      Exemplos:
        | tipo | valor | resultado | operacao | classe |
        | porcentagem | 0 | recusado | criar | mínimo−1 |
        | porcentagem | 0 | recusado | editar | mínimo−1 |
        | porcentagem | 1 | aceito | criar | mínimo |
        | porcentagem | 1 | aceito | editar | mínimo |
        | porcentagem | 2 | aceito | criar | mínimo+1 |
        | porcentagem | 2 | aceito | editar | mínimo+1 |
        | porcentagem | 99 | aceito | criar | máximo−1 |
        | porcentagem | 99 | aceito | editar | máximo−1 |
        | porcentagem | 100 | aceito | criar | máximo |
        | porcentagem | 100 | aceito | editar | máximo |
        | porcentagem | 101 | recusado | criar | máximo+1 |
        | porcentagem | 101 | recusado | editar | máximo+1 |
        | porcentagem | 12,5 | recusado | criar | fração |
        | porcentagem | 12,5 | recusado | editar | fração |
        | fixo | 1000,5 | recusado | criar | fração de centavo |
        | fixo | 1000,5 | recusado | editar | fração de centavo |
        | fixo | 101 | aceito | criar | fixo não tem teto percentual |
        | fixo | 101 | aceito | editar | fixo não tem teto percentual |
        | fixo | 1000 | aceito | criar | centavos inteiros |
        | fixo | 1000 | aceito | editar | centavos inteiros |
        | fixo | -1 | recusado | criar | sinal vedado por unsignedInteger da P-05 |
        | fixo | -1 | recusado | editar | sinal vedado por unsignedInteger da P-05 |

    Esquema do Cenário: [CT-13] Valor fixo superior a cem continua sendo centavos
      Dado o admin e dados válidos com tipo fixo e valor <valor>
      Quando o admin executa <operacao> pelo componente
      Então o valor persistido é exatamente <valor> centavos e o tipo continua fixo
      E a gravação não cria aplicação nem incrementa usos
      Exemplos:
        | valor | operacao | classe |
        | 1 | criar | centavo |
        | 1 | editar | centavo |
        | 99 | criar | abaixo de cem |
        | 99 | editar | abaixo de cem |
        | 100 | criar | cem |
        | 100 | editar | cem |
        | 101 | criar | acima de cem |
        | 101 | editar | acima de cem |
        | 1000 | criar | dez reais |
        | 1000 | editar | dez reais |

    Esquema do Cenário: [CT-50] Trocar tipo no schema preserva a unidade e o domínio esperado
      Dado admin e formulário <tela> com porcentagem 29, com valor válido e demais campos corretos
      Quando o admin salva pelo componente tipo fixo e valor 101
      Então o schema representa tipo fixo, valor 101 centavos e permite salvar essa combinação
      E o registro persistido tem tipo fixo e valor 101, sem aplicar teto percentual de cem
      Exemplos:
        | tela | classe |
        | criação | novo |
        | edição de cupom ativo | existente |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-12 | Aplicar teto percentual de cem também ao tipo fixo | CT-13 | 101 e 1000 centavos são persistidos sem erro |
| M-13 | Aceitar percentual 101 ou truncar fração 12,5 | CT-11 | 101 e 12,5 são recusados no campo valor |
| M-14 | Restringir valor somente pelo schema de formulário | CT-12 | 0/101/12,5 não são persistidos pela chamada direta |
| M-15 | Usar reais na coluna de valor fixo | CT-13 | 1000 permanece 1000, não 100000 |
| M-64 | Usar comparação escalar incompatível com estado enum e manter regras percentuais no fixo | CT-50 | fixo 101 é persistido no componente |
| M-68 | Truncar centavos fracionários do tipo fixo | CT-12 | 1000,5 centavos é recusado na escrita direta, não persistido como 1000 |
| M-73 | Aceitar valor fixo negativo e aumentar o total | CT-11 | fixo −1 é recusado pelo componente; também CT-12 no domínio |

## Regra R5 — Validade representa um instante e limite representa contagem

> Origem: RQ-05, RQ-06. Perfil: completo. Técnica: EP de representação; fronteiras de negócio nas R10 e R11.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Validade representa um instante e limite representa contagem

    Esquema do Cenário: [CT-14] Componente recusa representação inválida de validade ou contagem
      Dado o admin e um payload válido com apenas <campo> igual a <entrada>
      Quando o admin executa <operacao> pelo componente
      Então a escrita é recusada com erro especificamente em <campo>
      E cadastro, contador e trilha permanecem iguais ao estado anterior
      Exemplos:
        | campo | entrada | operacao | classe |
        | expira_em | não-é-data | criar | conteúdo inválido |
        | expira_em | não-é-data | editar | conteúdo inválido |
        | expira_em | array | criar | tipo errado |
        | expira_em | array | editar | tipo errado |
        | limite_de_usos | três | criar | conteúdo inválido |
        | limite_de_usos | três | editar | conteúdo inválido |
        | limite_de_usos | 1,5 | criar | contagem fracionária |
        | limite_de_usos | 1,5 | editar | contagem fracionária |
        | limite_de_usos | array | criar | tipo errado |
        | limite_de_usos | array | editar | tipo errado |

    Esquema do Cenário: [CT-15] Domínio não persiste uma data que não representa instante
      Dado o admin e dados válidos com somente expira_em em <entrada>
      Quando o admin executa <operacao> diretamente ao domínio
      Então não é persistida uma data arbitrária nem um cupom com a data inválida
      E o estado anterior do cadastro, contador e trilha permanece igual
      Exemplos:
        | entrada | operacao | classe |
        | não-é-data | criar | parse inválido |
        | não-é-data | editar | parse inválido |
        | array | criar | tipo errado |
        | array | editar | tipo errado |

    Esquema do Cenário: [CT-16] Domínio não converte fração de uso em limite inteiro silencioso
      Dado o admin e dados válidos com somente limite_de_usos em <entrada>
      Quando o admin executa <operacao> diretamente ao domínio
      Então a escrita é recusada sem persistir um limite convertido
      E cadastro, contador e trilha permanecem iguais
      Exemplos:
        | entrada | operacao | classe |
        | 1,5 | criar | fração |
        | 1,5 | editar | fração |
        | três | criar | texto inválido |
        | três | editar | texto inválido |
        | array | criar | tipo errado |
        | array | editar | tipo errado |

    Cenário: [CT-17] Instante e limite válidos sobrevivem a gravação e releitura
      Dado o admin, validade 2026-11-01T12:34:56-03:00 e limite 3, com os demais campos válidos
      Quando o admin grava pelo domínio e relê o cupom
      Então o instante é 2026-11-01T15:34:56Z e o limite é exatamente 3
      E usos é 0 e não há linha de aplicação
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-16 | Transformar limite 1,5 em 1 | CT-16 | fração é recusada, não persistida como 1 |
| M-17 | Converter erro de parse em data corrente | CT-15 | data inválida não cria nem altera cupom |
| M-18 | Truncar o timestamp para date durante persistência | CT-17 | instante relido preserva 15:34:56Z |
| M-19 | Validar só data e ignorar representação do limite na tela | CT-14 | limite três/1,5/array dá erro no campo sem gravação |

## Regra R6 — Código identifica um único cupom no contexto

> Origem: RQ-14, P-04. Perfil: completo. Técnica: EP por tenant e edição contra si.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Código identifica um único cupom no contexto

    Esquema do Cenário: [CT-18] Criação duplicada é recusada no mesmo contexto
      Dado o admin e um cupom ativo de código PROMO10 no contexto <modo>
      Quando o admin cria outro PROMO10 pelo componente com todos os campos válidos
      Então há erro em codigo e existe apenas o PROMO10 original com seus cinco campos
      E usos e trilha do original não mudam
      Exemplos:
        | modo | classe |
        | single-tenant, tenant nulo | unicidade sem organização |
        | Acme | unicidade local |

    Cenário: [CT-19] Edição não toma o código de outro cupom
      Dado o admin e os cupons ativos PROMO10 e OUTRO no mesmo contexto, com um uso real em OUTRO
      Quando o admin salva OUTRO com código PROMO10 pelo componente
      Então há erro em codigo e os dois códigos e campos originais permanecem iguais
      E usos de OUTRO permanece 1 e sua linha de uso permanece idêntica

    Esquema do Cenário: [CT-20] Unicidade e separação de organizações valem fora do formulário
      Dado o admin de cada contexto e um PROMO10 existente em <origem>
      Quando o admin grava PROMO10 por <operacao> diretamente em <destino>
      Então <resultado> e as identidades, organizações e cinco campos preexistentes permanecem corretos
      E a tentativa não altera usos nem linhas de aplicação
      Exemplos:
        | origem | destino | operacao | resultado | classe |
        | single-tenant nulo | single-tenant nulo | criar | recusa; só um PROMO10 | nulo não permite duplicado |
        | single-tenant nulo | single-tenant nulo | editar OUTRO | recusa; só um PROMO10 | nulo não permite duplicado |
        | Acme | Acme | criar | recusa; só um PROMO10 | mesmo tenant |
        | Acme | Acme | editar OUTRO | recusa; só um PROMO10 | mesmo tenant |
        | Acme | Globex | criar | aceita; um PROMO10 em cada tenant | tenant distinto |
        | Acme | Globex | editar OUTRO | aceita; um PROMO10 em cada tenant | tenant distinto |
        | Acme | Acme | salvar o próprio PROMO10 | aceita; identidade preservada | contra si |

    Esquema do Cenário: [CT-51] Formulário permite o mesmo código em organizações distintas
      Dado o admin da Globex, PROMO10 ativo da Acme e OUTRO ativo da Globex com os demais campos válidos
      Quando o admin executa <operacao> pelo componente na Globex com código PROMO10
      Então existe exatamente um PROMO10 em cada organização, preservada a identidade de origem na edição
      E os cinco campos, contador e linhas de uso da Acme permanecem iguais
      Exemplos:
        | operacao | classe |
        | criar novo cupom | criação entre tenants |
        | renomear OUTRO | edição entre tenants |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-20 | Confiar em unique composto que aceita NULL duplicado | CT-20 | no single-tenant, só um PROMO10 após escrita direta |
| M-21 | Usar unicidade global e barrar outro cliente | CT-20 | Globex persiste PROMO10 sem alterar o da Acme |
| M-22 | Ignorar o registro errado no unique de edição | CT-19 | OUTRO não toma PROMO10; CT-05 salva o próprio código |
| M-23 | Executar unique apenas no formulário | CT-20 | duplicata direta local é recusada |
| M-24 | Validação de duplicata da UI ignora contexto single-tenant | CT-18 | segundo PROMO10 no tenant nulo é recusado |
| M-67 | Validar unicidade global apenas no formulário | CT-51 | Globex cria e renomeia para PROMO10, sem bloquear pelo código da Acme |

## Regra R7 — Cada verbo de escrita exige admin

> Origem: RQ-07, RQ-08, P-02. Perfil: completo. Técnica: matriz papel × ação e pares de papéis.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cada verbo de escrita exige admin

    Esquema do Cenário: [CT-21] Componente exerce a permissão em cada verbo
      Dado um ator com papel <papel> no contexto <contexto> e cupons ativos desse contexto, incluindo PROMO10 sem usos
      Quando o ator tenta <acao> pelo componente com payload válido
      Então <resultado> e, se aceito, a operação produz os campos ou remoção solicitados
      E se recusado não cria cupom, não muda os cinco campos, não remove PROMO10 nem altera contador/trilha
      Exemplos:
        | papel | contexto | acao | resultado | classe |
        | admin_organizacao | Acme | criar | aceita | administrador local |
        | admin_organizacao | Acme | editar valor para 20 | aceita | administrador local |
        | admin_organizacao | Acme | excluir | aceita | administrador local |
        | master_global | single-tenant | criar | aceita | exceção da P-02 |
        | master_global | single-tenant | editar valor para 20 | aceita | exceção da P-02 |
        | master_global | single-tenant | excluir | aceita | exceção da P-02 |
        | master_global | Acme | criar | aceita | exceção da P-02 |
        | master_global | Acme | editar valor para 20 | aceita | exceção da P-02 |
        | master_global | Acme | excluir | aceita | exceção da P-02 |
        | panel_user | single-tenant | criar | recusa | leitura apenas |
        | panel_user | single-tenant | editar valor para 20 | recusa | leitura apenas |
        | panel_user | single-tenant | excluir | recusa | leitura apenas |
        | panel_user | Acme | criar | recusa | leitura apenas |
        | panel_user | Acme | editar valor para 20 | recusa | leitura apenas |
        | panel_user | Acme | excluir | recusa | leitura apenas |
        | admin | single-tenant | criar | aceita | herança afirmada pela P-02 |
        | admin | single-tenant | editar valor para 20 | aceita | herança afirmada pela P-02 |
        | admin | single-tenant | excluir | aceita | herança afirmada pela P-02 |
        | admin | Acme | criar | aceita | herança afirmada pela P-02 |
        | admin | Acme | editar valor para 20 | aceita | herança afirmada pela P-02 |
        | admin | Acme | excluir | aceita | herança afirmada pela P-02 |
        | infra | global | criar | recusa | sem admin |
        | infra | global | editar valor para 20 | recusa | sem admin |
        | infra | global | excluir | recusa | sem admin |

    Esquema do Cenário: [CT-22] Permissão de escrita vale em chamadas diretas
      Dado o ator <papel> no contexto <contexto>, PROMO10 ativo e payload válido, com snapshot do cadastro e trilha
      Quando o ator executa <acao> pelo model ou entrada de escrita de domínio sem componente e sem Gate manual no teste
      Então <resultado>, com registro efetivamente criado, alterado ou removido se autorizado
      E se recusado não há criação, alteração de valor, exclusão, incremento nem linha de uso
      Exemplos:
        | papel | contexto | acao | resultado | classe |
        | panel_user | single-tenant | criar | recusa | cada verbo isolado |
        | panel_user | single-tenant | editar | recusa | cada verbo isolado |
        | panel_user | single-tenant | excluir | recusa | cada verbo isolado |
        | panel_user | Acme | criar | recusa | cada verbo isolado |
        | panel_user | Acme | editar | recusa | cada verbo isolado |
        | panel_user | Acme | excluir | recusa | cada verbo isolado |
        | admin | single-tenant | criar | aceita | herança da P-02 |
        | admin | single-tenant | editar | aceita | herança da P-02 |
        | admin | single-tenant | excluir | aceita | herança da P-02 |
        | admin | Acme | criar | aceita | herança da P-02 |
        | admin | Acme | editar | aceita | herança da P-02 |
        | admin | Acme | excluir | aceita | herança da P-02 |
        | infra | global | criar | recusa | perfil sem admin |
        | infra | global | editar | recusa | perfil sem admin |
        | infra | global | excluir | recusa | perfil sem admin |
        | admin_organizacao | Acme | criar | aceita | autoridade local |
        | admin_organizacao | Acme | editar | aceita | autoridade local |
        | admin_organizacao | Acme | excluir | aceita | autoridade local |
        | master_global | single-tenant | criar | aceita | autoridade global |
        | master_global | single-tenant | editar | aceita | autoridade global |
        | master_global | single-tenant | excluir | aceita | autoridade global |
        | panel_user na Acme + admin_organizacao somente na Globex | Acme | criar | recusa | concessão do papel pertence ao outro tenant |
        | panel_user na Acme + admin_organizacao somente na Globex | Acme | editar | recusa | concessão do papel pertence ao outro tenant |
        | panel_user na Acme + admin_organizacao somente na Globex | Acme | excluir | recusa | concessão do papel pertence ao outro tenant |

    Esquema do Cenário: [CT-23] Papéis acumulados não apagam a autoridade local nem a exceção global
      Dado o ator com os papéis <par> no contexto Acme e um cupom ativo PROMO10
      Quando o ator executa <acao> diretamente ao domínio
      Então <resultado>, com o registro criado, alterado ou removido se autorizado
      E se recusado não há criação, edição, exclusão ou mudança de contador/trilha; Globex sempre permanece intacta
      Exemplos:
        | par | acao | resultado | classe |
        | master_global + admin | criar | aceita | par de admins globais |
        | master_global + admin | editar | aceita | par de admins globais |
        | master_global + admin | excluir | aceita | par de admins globais |
        | master_global + admin_organizacao | criar | aceita | global e local |
        | master_global + admin_organizacao | editar | aceita | global e local |
        | master_global + admin_organizacao | excluir | aceita | global e local |
        | master_global + panel_user | criar | aceita | global e leitor |
        | master_global + panel_user | editar | aceita | global e leitor |
        | master_global + panel_user | excluir | aceita | global e leitor |
        | master_global + infra | criar | aceita | global e infra |
        | master_global + infra | editar | aceita | global e infra |
        | master_global + infra | excluir | aceita | global e infra |
        | admin + admin_organizacao | criar | aceita | admin global e local |
        | admin + admin_organizacao | editar | aceita | admin global e local |
        | admin + admin_organizacao | excluir | aceita | admin global e local |
        | admin + panel_user | criar | aceita | admin e leitor; P-02 dada |
        | admin + panel_user | editar | aceita | admin e leitor; P-02 dada |
        | admin + panel_user | excluir | aceita | admin e leitor; P-02 dada |
        | admin + infra | criar | aceita | admin e infra; P-02 dada |
        | admin + infra | editar | aceita | admin e infra; P-02 dada |
        | admin + infra | excluir | aceita | admin e infra; P-02 dada |
        | admin_organizacao + panel_user | criar | aceita | local e leitor |
        | admin_organizacao + panel_user | editar | aceita | local e leitor |
        | admin_organizacao + panel_user | excluir | aceita | local e leitor |
        | admin_organizacao + infra | criar | aceita | local e infra |
        | admin_organizacao + infra | editar | aceita | local e infra |
        | admin_organizacao + infra | excluir | aceita | local e infra |
        | panel_user + infra | criar | recusa | dois papéis sem admin |
        | panel_user + infra | editar | recusa | dois papéis sem admin |
        | panel_user + infra | excluir | recusa | dois papéis sem admin |

    Cenário: [CT-24] Usuário comum sai da recusa e alcança sua listagem
      Dado o panel_user da Acme após acesso recusado à criação ou edição de PROMO10, com o cupom ativo ainda existente
      Quando o usuário acessa a listagem de cupons da Acme
      Então a página alcançável mostra PROMO10 com código e tipo corretos sem novo redirecionamento à tela recusada
      E o cupom, usos 0 e trilha vazia permanecem iguais
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-25 | Esconder botão sem autorizar a ação executada | CT-21 | cada ação proibida deixa cadastro/contador/trilha iguais |
| M-26 | Consultar policy somente dentro de Page | CT-22 | panel_user não grava diretamente em nenhum dos três verbos |
| M-27 | Dar escrita a todo papel que tem ViewAny | CT-22 | panel_user continua sem criação/edição/exclusão apesar da leitura |
| M-28 | Comparar um único papel por igualdade e negar admin acumulado | CT-23 | admin_organizacao + panel_user realiza escrita local |
| M-29 | Redirecionar erro de criação para outra página que o manda de volta | CT-24 | listagem é alcançada e mostra PROMO10 após recusa |
| M-74 | Usar admin_organizacao de qualquer tenant para autorizar escrita no atual | CT-22 | panel_user da Acme com admin_organizacao só de Globex não cria, edita ou exclui Acme |

## Regra R8 — Entradas de escrita e leitura preservam organização e identidade

> Origem: P-02, P-04, RQ-07–RQ-09, RQ-15. Perfil: completo. Técnica: IDOR, mass assignment e discriminante nulo.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Entradas de escrita e leitura preservam organização e identidade

    Esquema do Cenário: [CT-25] UUID de outra organização não concede edição nem exclusão
      Dado o admin apenas da Acme, PROMO10 ativo da Acme e OUTRO ativo de Globex, com autores e um uso em OUTRO
      Quando o admin solicita <acao> usando o UUID de OUTRO sob a rota ou componente da Acme
      Então a operação é recusada sem expor os cinco campos de OUTRO nem mudar sua organização ou valor
      E nenhum cupom é apagado ou criado, e os contadores e linhas de uso permanecem iguais
      Exemplos:
        | acao | classe |
        | abrir edição | leitura de registro alheio |
        | salvar edição com valor 20 | escrita alheia |
        | executar delete na tabela | exclusão alheia |

    Esquema do Cenário: [CT-26] Payload não move organização nem altera contador ou identidade
      Dado o admin da Acme e payload válido com apenas <campo> forjado para <valor>, para <operacao>
      Quando o admin grava pelo componente
      Então o cupom permanece na Acme com identidade gerida pelo sistema e contador real
      E cupom e trilha de Globex não mudam nem se cria aplicação fictícia
      Exemplos:
        | campo | valor | operacao | classe |
        | tenant_id | id de Globex | criar | organização |
        | tenant_id | id de Globex | editar | organização |
        | usos | 999 | criar | consumo forjado |
        | usos | 999 | editar | consumo forjado |
        | uuid | UUID de cupom de Globex | criar | identidade forjada |
        | uuid | UUID de cupom de Globex | editar | identidade forjada |

    Esquema do Cenário: [CT-27] Tenancy ligada sem contexto não abre os cupons de ninguém
      Dado tenancy ligada, cupons ativos na Acme e Globex e um registro global legado com tenant nulo
      Quando o chamador sem tenant corrente executa <entrada> no cadastro
      Então nenhum dos três cupons é retornado nem consumido
      E campos, contadores e linhas de uso das três origens permanecem iguais
      Exemplos:
        | entrada | classe |
        | consultar código diretamente | consulta |
        | consultar listagem autorizada do cadastro | lista |

    Cenário: [CT-28] Instância alheia não autoriza consumo fora da UI
      Dado o admin da Acme e uma instância de cupom ativo carregada em Globex antes da troca de contexto, com saldo e autor reais
      Quando o admin da Acme aplica diretamente essa instância a 10000 centavos
      Então a aplicação é recusada e não devolve total descontado
      E o contador do cupom de Globex e suas linhas de uso permanecem iguais

    Esquema do Cenário: [CT-52] Model não permite editar ou excluir instância de outra organização
      Dado o admin somente da Acme e uma instância ativa de Globex carregada antes da troca de contexto, com um uso real e sua trilha
      Quando o admin no contexto da Acme executa <operacao> diretamente nessa instância, sem componente ou Gate manual no teste
      Então a tentativa é recusada e o cupom de Globex permanece com os cinco campos originais
      E organização, identidade, contador e todas as linhas de uso de Globex permanecem iguais
      Exemplos:
        | operacao | classe |
        | editar valor para 20 | escrita direta alheia |
        | excluir | exclusão direta alheia |

    Esquema do Cenário: [CT-53] Contexto nulo também impede consumir referência carregada
      Dado tenancy ligada, admin e cupom ativo <tipo> carregado na Acme com usos 0 e limite 3
      E o tenant corrente foi removido depois do carregamento, mantendo a tenancy ligada
      Quando o chamador aplica diretamente essa referência a 10000 centavos
      Então a aplicação é recusada sem devolver total descontado
      E o cupom da Acme preserva campos, contador 0 e trilha vazia
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-30 | Usar UUID global sem recorte na ação | CT-25 | salvar/excluir OUTRO é recusado e registro de Globex permanece intacto |
| M-31 | Aceitar tenant_id ou usos enviados pelo cliente | CT-26 | organização Acme e contador real não mudam pelo payload |
| M-32 | Desligar filtro ao faltar tenant corrente | CT-27 | nem registro global nulo nem cupons A/B são retornados |
| M-33 | Confiar que uma instância carregada continua no contexto atual | CT-28 | não há consumo/trilha em Globex após aplicação na Acme |
| M-69 | Checar papel admin mas não organização da instância na escrita direta | CT-52 | edição e exclusão diretas de Globex são recusadas, com registro e trilha intactos |
| M-70 | Remover o filtro de tenant no consumo quando contexto fica nulo | CT-53 | referência válida carregada antes não consome após limpar contexto |

## Regra R9 — Aplicação exige cupom que ainda exista

> Origem: RQ-09, P-01. Perfil: completo. Técnica: EP existência.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Aplicação exige cupom que ainda exista

    Esquema do Cenário: [CT-29] Código inexistente é recusado sem efeitos; existente é identificado
      Dado o admin aplicador, PROMO10 ativo com limite 3 e usos 0, sem cupom DESCONHECIDO
      Quando o chamador consulta <codigo> e, apenas se encontrado, solicita aplicação a 10000 centavos
      Então <resultado>
      E na recusa PROMO10 continua com usos 0 e sem linha de aplicação
      Exemplos:
        | codigo | resultado | classe |
        | DESCONHECIDO | nenhum cupom nem total descontado | inexistente |
        | PROMO10 | identidade de PROMO10 e total 9000 | existente |
        | null | nenhum cupom nem total descontado | falta de código |
        | vazio | nenhum cupom nem total descontado | código vazio |

    Cenário: [CT-30] Consulta posterior à remoção não encontra cupom em cache
      Dado o admin e uma referência consultada de PROMO10 ativo, removido por exclusão autorizada antes da consulta atual, com OUTRO ativo
      Quando o chamador consulta novamente o código PROMO10
      Então nenhum cupom é retornado
      E OUTRO preserva seus campos, usos 0 e ausência de aplicação

    Esquema do Cenário: [CT-47] Dupla inelegibilidade também fecha consulta e consumo
      Dado o admin e um cupom <tipo> com três usos reais de limite 3 que depois expirou
      Quando o chamador executa <entrada> a 10000 centavos em fixture independente
      Então não obtém cupom válido nem total descontado
      E o contador permanece 3 e as três linhas anteriores ficam idênticas
      Exemplos:
        | tipo | entrada | classe |
        | porcentagem 10 | consultar código | expirado e esgotado |
        | porcentagem 10 | aplicar direto | expirado e esgotado |
        | fixo 1000 | consultar código | expirado e esgotado |
        | fixo 1000 | aplicar direto | expirado e esgotado |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-34 | Reutilizar último cupom quando a busca falha | CT-29 | DESCONHECIDO não devolve PROMO10 nem total 9000 |
| M-35 | Manter busca positiva em cache após exclusão | CT-30 | nova consulta a PROMO10 retorna ausência |
| M-36 | Tratar ausência de código como cupom padrão | CT-29 | null/vazio não consomem PROMO10 |
| M-37 | Permitir consumo quando dois filtros inválidos se anulam por ramificação | CT-47 | cupom expirado e esgotado não retorna desconto nem produz quarto uso |

## Regra R10 — Validade é estrita no instante de consumo

> Origem: RQ-05, RQ-10 e definição temporal do 00. Perfil: completo. Técnica: BVA 3 de 1 segundo e contexto temporal.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Validade é estrita no instante de consumo

    Esquema do Cenário: [CT-31] Segundo exato de expiração separa aceite e recusa
      Dado o admin e um cupom <tipo> que expira em 2026-10-21T00:00:00-03:00, com limite 3 e usos 0
      Quando o chamador <entrada> às <instante>, sobre total 10000 centavos
      Então <resultado>, com consulta e consumo avaliados em execuções independentes
      E na recusa usos permanece 0 e não há linha de uso; no consumo aceito usos é 1 e há uma linha com o autor
      Exemplos:
        | tipo | entrada | instante | resultado | classe |
        | porcentagem 10 | consultar | 2026-10-20T23:59:59-03:00 | consulta encontra; aplicação retorna 9000 | borda−1s |
        | porcentagem 10 | aplicar direto | 2026-10-20T23:59:59-03:00 | consulta encontra; aplicação retorna 9000 | borda−1s |
        | fixo 1000 | consultar | 2026-10-20T23:59:59-03:00 | consulta encontra; aplicação retorna 9000 | borda−1s |
        | fixo 1000 | aplicar direto | 2026-10-20T23:59:59-03:00 | consulta encontra; aplicação retorna 9000 | borda−1s |
        | porcentagem 10 | consultar | 2026-10-21T00:00:00-03:00 | consulta ausente; aplicação recusada | borda |
        | porcentagem 10 | aplicar direto | 2026-10-21T00:00:00-03:00 | consulta ausente; aplicação recusada | borda |
        | fixo 1000 | consultar | 2026-10-21T00:00:00-03:00 | consulta ausente; aplicação recusada | borda |
        | fixo 1000 | aplicar direto | 2026-10-21T00:00:00-03:00 | consulta ausente; aplicação recusada | borda |
        | porcentagem 10 | consultar | 2026-10-21T00:00:01-03:00 | consulta ausente; aplicação recusada | borda+1s |
        | porcentagem 10 | aplicar direto | 2026-10-21T00:00:01-03:00 | consulta ausente; aplicação recusada | borda+1s |
        | fixo 1000 | consultar | 2026-10-21T00:00:01-03:00 | consulta ausente; aplicação recusada | borda+1s |
        | fixo 1000 | aplicar direto | 2026-10-21T00:00:01-03:00 | consulta ausente; aplicação recusada | borda+1s |

    Esquema do Cenário: [CT-32] Expiração entre consulta e aplicação invalida a referência já carregada
      Dado o admin e um cupom <tipo> consultado válido um segundo antes de expirar, ainda com usos 0 e limite 3
      Quando o chamador aplica essa mesma instância no segundo exato da expiração a 10000 centavos
      Então a aplicação é recusada sem devolver desconto
      E usos continua 0 e nenhuma linha de aplicação é criada
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-33] O mesmo instante não muda com a representação do fuso
      Dado app em America/Sao_Paulo e um cupom de 10% com validade equivalente a 2026-10-21T02:59:59Z
      Quando o admin o aplica no instante <local> equivalente a <utc>, sobre 10000 centavos
      Então <resultado>
      E aceite deixa usos 1 com uma linha de aplicação no instante UTC, enquanto recusa deixa usos 0 e trilha vazia
      Exemplos:
        | local | utc | resultado | classe |
        | 2026-10-20T23:30:00-03:00 | 2026-10-21T02:30:00Z | retorna 9000 | janela de divergência entre dias |
        | 2026-10-20T23:59:59-03:00 | 2026-10-21T02:59:59Z | recusa | expiração exata |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-38 | Usar >= na validade e aceitar o instante final | CT-31 | na borda exata não há retorno descontado/uso/trilha |
| M-39 | Verificar validade só em valido e confiar no objeto | CT-32 | objeto antes válido é recusado ao chegar a expiração |
| M-40 | Comparar só a data e ignorar hora/minuto/segundo | CT-33 | 23:30 local ainda retorna 9000; borda exata recusa |
| M-41 | Interpretar validade UTC como horário local | CT-33 | expiração exata 02:59:59Z recusa, não estende por três horas |

## Regra R11 — Saldo de usos limita cada consumo inclusive sob disputa

> Origem: RQ-11, RQ-13. Perfil: completo. Técnica: BVA 3, estado × evento e concorrência.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Saldo de usos limita cada consumo inclusive sob disputa

    Esquema do Cenário: [CT-34] A contagem persistida decide a borda do limite
      Dado o admin e cupom <tipo> com validade futura, limite 3 e <usos> usos persistidos
      Quando o chamador <entrada> para total 10000 centavos
      Então <resultado>
      E consumo aceito soma exatamente 1 e uma linha; recusa preserva contador e todas as linhas anteriores
      Exemplos:
        | tipo | usos | entrada | resultado | classe |
        | porcentagem 10 | 2 | consultar | consulta encontra; consumo retorna 9000 | borda−1 |
        | porcentagem 10 | 2 | aplicar direto | consulta encontra; consumo retorna 9000 | borda−1 |
        | fixo 1000 | 2 | consultar | consulta encontra; consumo retorna 9000 | borda−1 |
        | fixo 1000 | 2 | aplicar direto | consulta encontra; consumo retorna 9000 | borda−1 |
        | porcentagem 10 | 3 | consultar | consulta ausente; consumo recusa | borda |
        | porcentagem 10 | 3 | aplicar direto | consulta ausente; consumo recusa | borda |
        | fixo 1000 | 3 | consultar | consulta ausente; consumo recusa | borda |
        | fixo 1000 | 3 | aplicar direto | consulta ausente; consumo recusa | borda |
        | porcentagem 10 | 4 | consultar | consulta ausente; consumo recusa | borda+1 legado corrompido |
        | porcentagem 10 | 4 | aplicar direto | consulta ausente; consumo recusa | borda+1 legado corrompido |
        | fixo 1000 | 4 | consultar | consulta ausente; consumo recusa | borda+1 legado corrompido |
        | fixo 1000 | 4 | aplicar direto | consulta ausente; consumo recusa | borda+1 legado corrompido |

    Esquema do Cenário: [CT-35] Instância anterior ao último uso não abre saldo novamente
      Dado dois aplicadores distintos e duas instâncias de um cupom <tipo> válido com limite 3 e dois usos reais
      E o primeiro aplicador já consumiu o último uso pela instância dele
      Quando o segundo aplicador aplica sua instância ainda carregada com dois usos
      Então a tentativa é recusada sem devolver total descontado
      E o contador persistido é 3, com exatamente três linhas de uso, apenas uma referente ao último saldo
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-36] Duas aplicações simultâneas disputam um único saldo
      Dado cupom <tipo> válido de limite 3 e dois usos commitados, dois autores e duas conexões que já leram saldo 2
      Quando a barreira libera simultaneamente os dois consumos a 10000 centavos
      Então exatamente um retorna 9000 e o outro é recusado
      E o contador relido é 3 e existem exatamente três linhas de uso, com só uma linha nova para o vencedor
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-42 | Usar <= e aceitar a quarta aplicação | CT-34 | usos 3 recusa, permanecendo 3 |
| M-43 | Consumir com base no contador do objeto antigo | CT-35 | segundo objeto não recebe desconto; persistido continua 3 |
| M-44 | Implementar check-then-act sem condição/trava atômica | CT-36 | só um sucesso e só uma linha nova após leituras simultâneas |
| M-45 | Impedir concorrência no total mas gravar trilha do perdedor | CT-36 | linha nova pertence apenas ao vencedor |

## Regra R12 — Desconto usa inteiros e devolve total limitado a zero

> Origem: RQ-12, P-01, P-05, P-06, P-07. Perfil: completo. Técnica: EP e BVA 3 de centavo.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Desconto usa inteiros e devolve total limitado a zero

    Esquema do Cenário: [CT-37] Percentual trunca a fração sem perder centavos por float
      Dado o admin e um cupom ativo de porcentagem <percentual>, com usos 0 e limite 3
      Quando o chamador aplica o cupom a <total> centavos
      Então o total devolvido é exatamente <final> centavos
      E o contador persistido é 1 e há uma linha de aplicação com esse autor
      Exemplos:
        | percentual | total | final | classe |
        | 29 | 100 | 71 | float discrimina: mutante devolve 72 |
        | 10 | 9999 | 9000 | fração 999,9 truncada em 999 |
        | 5 | 50 | 48 | fração de meio centavo truncada em 2 |
        | 1 | 100 | 99 | percentual mínimo |
        | 100 | 101 | 0 | percentual máximo |

    Esquema do Cenário: [CT-38] Valor fixo e percentual nunca produzem total negativo
      Dado o admin e cupom ativo <tipo> com valor <valor>, usos 0 e limite 3
      Quando o chamador aplica o cupom a <total> centavos
      Então o total devolvido é exatamente <final> centavos
      E usos é 1 com uma única linha de aplicação
      Exemplos:
        | tipo | valor | total | final | classe |
        | fixo | 1000 | 999 | 0 | total−1 centavo |
        | fixo | 1000 | 1000 | 0 | total igual ao desconto |
        | fixo | 1000 | 1001 | 1 | total+1 centavo |
        | fixo | 1000 | 3000 | 2000 | centavos não são reais |
        | porcentagem | 100 | 1 | 0 | limite percentual |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-46 | Calcular com float e converter para inteiro | CT-37 | 29% de 100 retorna 71, não 72; contraexemplo executado |
| M-47 | Arredondar desconto em vez de truncar | CT-37 | 5% de 50 retorna 48, não 47 |
| M-48 | Subtrair fixo sem limitar resultado a zero | CT-38 | 1000 de desconto sobre 999 retorna 0, não −1 |
| M-49 | Interpretar fixo como percentual ou como reais | CT-38 | 1000 sobre 3000 retorna 2000 |

## Regra R13 — Consumo persiste uma unidade por aplicação e não se separa da trilha

> Origem: RQ-11–RQ-13, RQ-15. Perfil: completo. Técnica: rastreio de efeito: acontece, não acontece, uma vez, atomicidade.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Consumo persiste uma unidade por aplicação e não se separa da trilha

    Esquema do Cenário: [CT-39] Aplicação válida incrementa e registra uma só vez por intenção
      Dado o admin e cupom ativo <tipo> de limite 3 com um uso real e sua linha de uso já existente
      Quando o chamador realiza uma nova aplicação a 10000 centavos
      Então o total é 9000 e o contador relido é exatamente 2
      E há exatamente duas linhas de uso, preservada a anterior e criada só uma com cupom e autor atuais
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-40] Falha ao inserir uso desfaz o contador já consumido
      Dado o admin, cupom ativo <tipo> com um uso real e falha injetada na inserção da nova linha depois do consumo
      Quando o chamador solicita uma nova aplicação a 10000 centavos
      Então a aplicação falha sem devolver total descontado
      E o contador relido continua 1 e existe somente a linha de uso anterior, com os mesmos dados
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-41] Tentativa sem saldo não acrescenta consumo nem registro
      Dado o admin e um cupom <tipo> que ficou esgotado após três aplicações reais e possui três linhas de uso
      Quando o chamador solicita mais uma aplicação a 10000 centavos
      Então não recebe total descontado
      E o contador relido permanece 3 e as três linhas anteriores permanecem idênticas, sem quarta linha
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-50 | Esquecer incremento embora retorne desconto | CT-39 | persistido 2, não 1, após novo sucesso |
| M-51 | Incrementar duas vezes ou inserir duas linhas no sucesso | CT-39 | contador 2 e duas linhas totais, não 3 |
| M-52 | Executar incremento fora da transação da trilha | CT-40 | falha de INSERT deixa contador 1, não 2 |
| M-53 | Registrar tentativa recusada como uso consumido | CT-41 | contador 3 e exatamente três linhas sem nova aplicação |

## Regra R14 — Cada uso aceito identifica autor e instante confiáveis

> Origem: RQ-15, P-08, P-01. Perfil: completo. Técnica: rastreio de efeito, identidade e atomicidade.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cada uso aceito identifica autor e instante confiáveis

    Esquema do Cenário: [CT-42] Trilha própria guarda quem aplicou e quando nos dois tipos
      Dado o admin aplicador A distinto do criador B e cupom ativo <tipo> cadastrado por B em 2026-10-20T14:00:00-03:00
      E o relógio da aplicação está fixado em 2026-10-20T23:30:17-03:00
      Quando A aplica diretamente o cupom a 10000 centavos
      Então existe uma única linha em cupom_usos para o cupom com aplicado_por_id de A e instante 2026-10-21T02:30:17Z
      E o total é 9000 e usos é 1, sem atribuir o uso a B
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-43] Falha posterior à gravação da trilha não deixa uso fantasma
      Dado o admin, cupom ativo <tipo> e falha injetada depois da inserção da trilha e antes de concluir a aplicação
      Quando o chamador aplica diretamente o cupom a 10000 centavos
      Então não recebe total descontado
      E contador relido é 0 e nenhuma linha do uso tentado fica persistida, embora cupom e autor existam
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-44] Sessão e identidade do criador não substituem o autor explícito
      Dado o cupom ativo <tipo>, criador B, sessão autenticada B e aplicador autorizado A explicitamente informado
      Quando a entrada de motor da P-01 aplica o cupom em nome de A a 10000 centavos
      Então o único uso registra A, não B, e o instante atual fixado
      E contador é 1 e o total é 9000
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-54] Argumento de autoria obrigatório não admite consumo anônimo
      Dado o admin, autor real A e cupom ativo <tipo> com usos 0 e limite 3, sem linhas de uso
      Quando o chamador solicita aplicação a 10000 centavos com <autoria> na entrada da P-01
      Então a chamada é recusada sem devolver total descontado
      E o contador permanece 0 e não há linha de aplicação anônima ou atribuída por default a outro usuário
      Exemplos:
        | tipo | autoria | classe |
        | porcentagem 10 | argumento ausente | parâmetro obrigatório |
        | fixo 1000 | argumento ausente | parâmetro obrigatório |
        | porcentagem 10 | null explícito | autor nulo |
        | fixo 1000 | null explícito | autor nulo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-54 | Depender só de eventos de auditoria genérica do contador | CT-42 | cupom_usos tem uma linha concreta após consumo direto |
| M-55 | Usar criador ou sessão em vez do autor recebido | CT-44 | aplicado_por_id é A, embora sessão e criador sejam B |
| M-56 | Usar created_at do cupom como instante do uso | CT-42 | instante da linha é 02:30:17Z da aplicação, não o cadastro anterior |
| M-57 | Inserir trilha fora da transação de aplicação | CT-43 | falha após INSERT não deixa linha fantasma nem contador |
| M-71 | Aceitar null ou omissão do autor e consumir anonimamente | CT-54 | contador continua 0 e não há linha anônima nem retorno descontado |

## Regra R15 — Usuário comum lista somente cupons ativos de sua organização

> Origem: RQ-08, P-03, P-02. Perfil: completo. Técnica: decisão completa, estado × operação e EP de cardinalidade.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Usuário comum lista somente cupons ativos de sua organização

    Esquema do Cenário: [CT-45] Situação derivada concorda com consulta, uso e listagem
      Dado panel_user da Acme que já aplicou o cupom no passado, cupons nos dois tipos em <situacao> e um cupom ativo de Globex
      Quando o usuário lista cupons pelo componente
      Então <resultado>, e Globex está sempre ausente
      E nenhum campo, contador ou linha de uso é alterado
      Exemplos:
        | situacao | resultado | classe |
        | ativo com saldo | presente com código e tipo corretos | ativo |
        | expirado com saldo | ausente | somente tempo inválido |
        | esgotado ainda válido | ausente | somente saldo inválido |
        | expirado e esgotado | ausente | ambos inválidos |
        | removido | ausente | remoção |

    Esquema do Cenário: [CT-46] Listagem completa alcança todos os ativos e nenhum inativo
      Dado panel_user da Acme e <quantidade> cupons ativos, mais expirados, esgotados e cupons de Globex
      Quando o usuário percorre as páginas da listagem até o fim
      Então o conjunto de UUIDs visíveis é exatamente o dos <quantidade> ativos da Acme, sem repetidos
      E nenhum campo, contador ou linha de uso é alterado
      Exemplos:
        | quantidade | classe |
        | 0 | vazio |
        | 1 | unitário |
        | p | limite da página configurada |
        | p+1 | além da página |
        | 2p+1 | várias páginas |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-58 | Combinar validade e saldo com OR na listagem | CT-45 | expirado com saldo e esgotado válido estão ausentes |
| M-59 | Aplicar recorte ativo somente ao código consultado e não à tabela | CT-45 | lista não contém cupons inelegíveis |
| M-60 | Paginar antes de filtrar e perder ativos de páginas seguintes | CT-46 | união tem exatamente todos os ativos, inclusive 2p+1 |

## Regra R16 — Cupom removido não continua recebendo operação

> Origem: RQ-01, RQ-07, RQ-09. Perfil: completo. Técnica: estado × operação e CRUD negativo.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cupom removido não continua recebendo operação

    Esquema do Cenário: [CT-48] Objeto anterior à exclusão não aplica desconto
      Dado admin, cupom antes ativo <tipo> carregado em memória e já removido por exclusão autorizada, com OUTRO ativo
      Quando o admin aplica diretamente a referência removida a 10000 centavos
      Então a operação é recusada sem devolver total descontado
      E não se recria cupom ou uso para a identidade removida e OUTRO preserva campos, contador e trilha
      Exemplos:
        | tipo | classe |
        | porcentagem 10 | percentual |
        | fixo 1000 | fixo |

    Esquema do Cenário: [CT-49] CRUD com identidade inexistente não afeta vizinho
      Dado admin, OUTRO ativo e uma identidade <alvo> que não existe
      Quando o admin executa <operacao> sobre essa identidade
      Então não é criado ou alterado cupom com essa identidade e OUTRO preserva todos os campos
      E OUTRO mantém usos 0 e trilha vazia; a listagem autorizada continua sendo destino de saída
      Exemplos:
        | alvo | operacao | classe |
        | UUID nunca existente | abrir edição | inexistente |
        | UUID nunca existente | salvar edição | inexistente |
        | UUID nunca existente | excluir | inexistente |
        | UUID de cupom já excluído | abrir edição | removido |
        | UUID de cupom já excluído | salvar edição | removido |
        | UUID de cupom já excluído | excluir novamente | removido |

    Esquema do Cenário: [CT-55] Admin exclui do cadastro também os cupons inativos
      Dado o admin da Acme, OUTRO ativo e um cupom alvo <situacao>, construído por usos reais ou passagem do tempo
      Quando o admin executa a exclusão do alvo pelo componente
      Então o alvo deixa de existir no cadastro e na listagem
      E OUTRO preserva os cinco campos, organização, contador e linhas de uso
      Exemplos:
        | situacao | classe |
        | expirado com saldo | validade encerrada |
        | esgotado com validade futura | consumo completo |
        | expirado e esgotado | ambos encerrados |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | Calcular desconto na memória sem reconferir existência | CT-48 | referência removida não retorna total descontado |
| M-62 | Salvar objeto removido como inserção silenciosa | CT-49 | save não recria identidade removida |
| M-63 | Excluir por seleção residual e apagar outro registro | CT-49 | segunda exclusão mantém OUTRO presente com todos os campos |
| M-72 | Permitir DeleteAction apenas para cupom ativo | CT-55 | admin remove também expirado, esgotado e ambos do cadastro |

## Índice de Cenários

Arquivos abaixo são destinos propostos; nenhum teste executável foi criado.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | Visitar criação e edição apresenta os dados do cupom | R1 | EP e estado × operação | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-04 |
| CT-02 | Criar preserva todos os campos para os dois tipos | R1 | EP e estado × operação | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-01 |
| CT-03 | Editar troca os campos decisivos sem consumir uso | R1 | EP e estado × operação | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-02 |
| CT-04 | Admin exclui cupom ativo e a lista deixa de retorná-lo | R1 | EP e estado × operação | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-03 |
| CT-05 | Salvar o próprio código sem alteração não colide consigo | R1 | EP e estado × operação | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-05 |
| CT-06 | Criação recusa um único campo obrigatório ausente | R2 | EP por campo e ponto de entrada | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-08 |
| CT-07 | Edição recusa apagar um campo obrigatório | R2 | EP por campo e ponto de entrada | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-06 |
| CT-08 | Obrigatoriedade vale na escrita direta fora do formulário | R2 | EP por campo e ponto de entrada | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-07 |
| CT-09 | Formulário não grava um terceiro tipo | R3 | EP | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-10 |
| CT-10 | Tipo inválido não entra pelo model | R3 | EP | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-09, M-11 |
| CT-11 | Percentual respeita cada borda em criação e edição | R4 | EP, BVA 3 e decisão tipo × valor | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-13, M-73 |
| CT-12 | As bordas percentuais também protegem a escrita direta | R4 | EP, BVA 3 e decisão tipo × valor | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-14, M-68 |
| CT-13 | Valor fixo superior a cem continua sendo centavos | R4 | EP, BVA 3 e decisão tipo × valor | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-12, M-15 |
| CT-50 | Trocar tipo no schema preserva a unidade e o domínio esperado | R4 | EP, BVA 3 e decisão tipo × valor | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-64 |
| CT-14 | Componente recusa representação inválida de validade ou contagem | R5 | EP de representação; fronteiras de negócio nas R10 e R11 | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-19 |
| CT-15 | Domínio não persiste uma data que não representa instante | R5 | EP de representação; fronteiras de negócio nas R10 e R11 | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-17 |
| CT-16 | Domínio não converte fração de uso em limite inteiro silencioso | R5 | EP de representação; fronteiras de negócio nas R10 e R11 | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-16 |
| CT-17 | Instante e limite válidos sobrevivem a gravação e releitura | R5 | EP de representação; fronteiras de negócio nas R10 e R11 | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-18 |
| CT-18 | Criação duplicada é recusada no mesmo contexto | R6 | EP por tenant e edição contra si | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-24 |
| CT-19 | Edição não toma o código de outro cupom | R6 | EP por tenant e edição contra si | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-22 |
| CT-20 | Unicidade e separação de organizações valem fora do formulário | R6 | EP por tenant e edição contra si | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-20, M-21, M-23 |
| CT-51 | Formulário permite o mesmo código em organizações distintas | R6 | EP por tenant e edição contra si | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-67 |
| CT-21 | Componente exerce a permissão em cada verbo | R7 | matriz papel × ação e pares de papéis | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-25 |
| CT-22 | Permissão de escrita vale em chamadas diretas | R7 | matriz papel × ação e pares de papéis | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-26, M-27, M-74 |
| CT-23 | Papéis acumulados não apagam a autoridade local nem a exceção global | R7 | matriz papel × ação e pares de papéis | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-28 |
| CT-24 | Usuário comum sai da recusa e alcança sua listagem | R7 | matriz papel × ação e pares de papéis | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-29 |
| CT-25 | UUID de outra organização não concede edição nem exclusão | R8 | IDOR, mass assignment e discriminante nulo | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-30 |
| CT-26 | Payload não move organização nem altera contador ou identidade | R8 | IDOR, mass assignment e discriminante nulo | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-31 |
| CT-27 | Tenancy ligada sem contexto não abre os cupons de ninguém | R8 | IDOR, mass assignment e discriminante nulo | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-32 |
| CT-28 | Instância alheia não autoriza consumo fora da UI | R8 | IDOR, mass assignment e discriminante nulo | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-33 |
| CT-52 | Model não permite editar ou excluir instância de outra organização | R8 | IDOR, mass assignment e discriminante nulo | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-69 |
| CT-53 | Contexto nulo também impede consumir referência carregada | R8 | IDOR, mass assignment e discriminante nulo | TEN | Pest feature HTTP | tests/Tenancy/CupomTenancyTest.php (single-tenant em tests/Kit/CupomTest.php) | M-70 |
| CT-29 | Código inexistente é recusado sem efeitos; existente é identificado | R9 | EP existência | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-34, M-36 |
| CT-30 | Consulta posterior à remoção não encontra cupom em cache | R9 | EP existência | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-35 |
| CT-47 | Dupla inelegibilidade também fecha consulta e consumo | R9 | EP existência | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-37 |
| CT-31 | Segundo exato de expiração separa aceite e recusa | R10 | BVA 3 de 1 segundo e contexto temporal | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-38 |
| CT-32 | Expiração entre consulta e aplicação invalida a referência já carregada | R10 | BVA 3 de 1 segundo e contexto temporal | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-39 |
| CT-33 | O mesmo instante não muda com a representação do fuso | R10 | BVA 3 de 1 segundo e contexto temporal | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-40, M-41 |
| CT-34 | A contagem persistida decide a borda do limite | R11 | BVA 3, estado × evento e concorrência | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-42 |
| CT-35 | Instância anterior ao último uso não abre saldo novamente | R11 | BVA 3, estado × evento e concorrência | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-43 |
| CT-36 | Duas aplicações simultâneas disputam um único saldo | R11 | BVA 3, estado × evento e concorrência | RACE | Pest feature HTTP | tests/Kit/CupomConcorrenciaTest.php | M-44, M-45 |
| CT-37 | Percentual trunca a fração sem perder centavos por float | R12 | EP e BVA 3 de centavo | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-46, M-47 |
| CT-38 | Valor fixo e percentual nunca produzem total negativo | R12 | EP e BVA 3 de centavo | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-48, M-49 |
| CT-39 | Aplicação válida incrementa e registra uma só vez por intenção | R13 | rastreio de efeito: acontece, não acontece, uma vez, atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-50, M-51 |
| CT-40 | Falha ao inserir uso desfaz o contador já consumido | R13 | rastreio de efeito: acontece, não acontece, uma vez, atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-52 |
| CT-41 | Tentativa sem saldo não acrescenta consumo nem registro | R13 | rastreio de efeito: acontece, não acontece, uma vez, atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-53 |
| CT-42 | Trilha própria guarda quem aplicou e quando nos dois tipos | R14 | rastreio de efeito, identidade e atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-54, M-56 |
| CT-43 | Falha posterior à gravação da trilha não deixa uso fantasma | R14 | rastreio de efeito, identidade e atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-57 |
| CT-44 | Sessão e identidade do criador não substituem o autor explícito | R14 | rastreio de efeito, identidade e atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-55 |
| CT-54 | Argumento de autoria obrigatório não admite consumo anônimo | R14 | rastreio de efeito, identidade e atomicidade | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-71 |
| CT-45 | Situação derivada concorda com consulta, uso e listagem | R15 | decisão completa, estado × operação e EP de cardinalidade | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-58, M-59 |
| CT-46 | Listagem completa alcança todos os ativos e nenhum inativo | R15 | decisão completa, estado × operação e EP de cardinalidade | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-60 |
| CT-48 | Objeto anterior à exclusão não aplica desconto | R16 | estado × operação e CRUD negativo | DOM | Pest feature HTTP | tests/Kit/CupomTest.php | M-61 |
| CT-49 | CRUD com identidade inexistente não afeta vizinho | R16 | estado × operação e CRUD negativo | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-62, M-63 |
| CT-55 | Admin exclui do cadastro também os cupons inativos | R16 | estado × operação e CRUD negativo | CMP | componente Livewire/Filament | tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php | M-72 |

## Checklist de Taxonomia

Cada linha percorre o gatilho da referência inteira. CT é previsão de cobertura, não execução atestada.

| Item | CT ou lacuna declarada | Grupo |
|---|---|---|
| IDOR por UUID/ação | CT-25; GET e tentativa de salvar/excluir alheio, não só can() | CMP |
| Autorização na ação e fora da UI | CT-21/22; três verbos executados isoladamente | CMP, TEN |
| Idempotência de aplicação | lacuna L-IDEMP: P-01 exclui Pedido persistido; retornos iguais não comprovam retry no mesmo agregado. Q6 | DOM |
| Repetição de cadastro/edição/exclusão | CT-05/18/49; mesma identidade não duplica nem atinge vizinho; não representa idempotência de Pedido | CMP |
| Domínio condicionado tipo × valor | CT-11–13/50; fixo 101 e percentual 101 têm resultados opostos | CMP, DOM |
| Fronteiras de todo campo em toda entrada | CT-06–20/31/34; lacunas Q1/Q2/Q3/Q4 para teto textual, normalização, fixo e restrições de cadastro não determinadas | CMP, DOM |
| Concorrência | CT-36; duas conexões com barreira, não duas chamadas sequenciais; execução pendente por vendor ausente | RACE |
| Efeito com destinatário variável: 0/1/N | CT-42/44 cobre autor real diferente do criador/sessão; 0 autores é recusado em CT-54; N autores de uma aplicação contraria o “quem” singular e não é cardinalidade de notificação | DOM |
| Ausente, null e vazio | CT-06–08, CT-29 em exemplos separados; CT-54 recusa autoria ausente/null como determinado pela P-01 | DOM, CMP |
| Paginação 0/1/p/p+1 | CT-46; inserção entre páginas é lacuna Q10, sem ordem/cursor especificados | CMP |
| Ordenação: coluna inválida, nullable, empate | lacuna L-SUP/Q10: sem 02 não se conhece consumo de tableSortColumn nem contrato de desempate; não se dispensou validação | CMP |
| Timezone, meia-noite, date × datetime | CT-31/33/17; DST e fuso editável do usuário são lacuna L-TZ: nenhum campo de fuso foi determinado; não simular independência de DB sem arnês real | DOM |
| Texto: acento, emoji, teto, espaços | lacuna Q1/Q2: teto 40 e normalização só no PRD; CT-06–08 cobrem obrigatório, não certificam domínio Unicode | DOM, CMP |
| Unicidade + soft delete | CT-18–20/51; lacuna Q9: mecanismo físico/lógico e reutilização não foram dados pelo 00; não se leu implementação para decidir | DOM |
| Removido/desligado ainda escreve? | CT-31/34/47/48; não substituir tentativa de aplicação pela ausência da lista | DOM |
| CRUD combinado: ID inexistente, excluir duas vezes, salvar sem alterar | CT-05/30/48/49 | CMP, DOM |
| Mass assignment do payload | CT-26; contador e organização forjados não mudam o registro | CMP |
| Upload | não se aplica ao requisito: nenhum campo/fluxo de upload aparece no 00 ou superfície de UI autorizada; não é dispensa de controle de fronteira | — |
| Precisão monetária | CT-37/38, incluindo contraexemplo de float executado no PHP alvo | DOM |
| Superfície Livewire por linha do 02: domínio inválido e tipo errado | lacuna L-SUP: 02 ausente; CT-09/14/26 exercitam entradas conhecidas, não inventário completo | CMP |
| Estado do framework usado como índice, parse, coluna ou operador | lacuna L-SUP: tableFilters/tableSortColumn e propriedades não inventariadas; CT-14 não cobre widget nem estado de framework | CMP |
| Método público com argumento fora da lista | lacuna L-SUP: não há lista de métodos; não chamar API presumida como prova | CMP |
| IDOR por entidade: cupons | CT-25/28/52/53, com duas organizações e tentativa real | CMP, TEN |
| IDOR por entidade: cupom_usos | lacuna L-USO-IDOR/Q8: trilha existe, mas nenhum ponto autorizado de leitura/escrita próprio foi inventariado. CT-28 não fecha esta linha | TEN |
| Mass assignment por entidade: cupons | CT-26 | CMP |
| Mass assignment por entidade: cupom_usos | lacuna L-USO-MASS/Q8: nenhum payload público próprio determinado; não assumir proteção por cupom_id | TEN |
| Escopo com discriminante nulo | CT-27: tenancy ligada sem contexto, inclusive registro global nulo, fecha | TEN |
| Saída do erro 4xx/redirect | CT-24 e destino de CT-49; recusa de aplicação não inventa HTTP/rota de checkout | TEN, CMP |

### Limitações de falsificabilidade e perguntas

- **L-SUP**: entrada obrigatória 02 não fornecida. Não se dispensou guarda; não há evidência vendor para afirmar que algum método/propriedade é inalcançável.
- **L-IDEMP**: consequência da P-01. Nenhum CT devolve “idempotência comprovada” por comparar dois retornos ou só contador.
- **L-USO-IDOR/L-USO-MASS**: cupom_usos possui linhas próprias no checklist; “filho já protegido” não foi aceito.
- **L-TZ**: CT-33 especifica janela discriminante, mas app/DB/usuário com fusos independentes e DST não foram executados. Ausência de dependências impede experimentar o arnês agora.
- **L-RACE**: CT-36 especificado para execução real; não alegar cobertura concorrente por CT-35. Não foi tentado instalar dependências ou criar banco, pois a rodada proíbe alterações fora desta pasta.
- Retenção após excluir cupom/autor, texto no teto e decisões de cadastro continuam declaradas, sem suposição direcional.
- Nenhuma negativa de fronteira foi usada para remover controle. Ausência de prova vendor é lacuna, não “não se aplica”.

## Matriz papel × ação

Cada “criar / editar / excluir” dos esquemas se expande em três linhas distintas e três execuções.
Personas não são colapsadas: criador, aplicador, administrador local e usuário de outro tenant são pessoas distintas.

| Papel/contexto | Criar | Editar | Excluir | Listar ativos |
|---|---|---|---|---|
| admin_organizacao, próprio tenant | CT-21/22 | CT-21/22 | CT-21/22 | CT-01 (formulário) não conta como lista; CT-46 usa leitor |
| master_global | CT-21/22 | CT-21/22 | CT-21/22 | não se suspende acesso administrativo; apresentação de inativos é Q9 |
| admin da instalação, herança P-02 | CT-21/22 | CT-21/22 | CT-21/22 | acesso dado pela P-02, não negar por matriz do PRD |
| panel_user | CT-21/22 recusa | CT-21/22 recusa | CT-21/22 recusa | CT-45/46 |
| infra isolado | CT-21/22 recusa | CT-21/22 recusa | CT-21/22 recusa | acesso ao painel depende de perfil; sem cenário inventado de leitura app |
| admin local com alvo de outro tenant | não move posse CT-26 | CT-25 | CT-25 | Globex ausente CT-45 |
| pares dos cinco papéis | CT-23 | CT-23 | CT-23 | recorte de inativos Q9 |

Os dez pares possíveis dos cinco papéis constam de CT-23. Todos usam precedência das premissas do 00, não da matriz do plano.
CT-45 inclui participante histórico agora panel_user: participação anterior não elimina o recorte ativo.
Não há link de notificação no escopo (00 o exclui), nem CT de e-mail.

## Cogitado e cortado

| Cenário cogitado | Decisão e motivo |
|---|---|
| CRUD inteiro no navegador | cortado: CT-01–05/21 provam formulário, persistência e autorização por componente |
| Teste de cálculo em Unit sem aplicação | cortado: arnês Unit sem TestCase e modelo com casts; CT-37/38 em Feature observa o contrato real |
| CT-B de atualização reativa | retirado por ADV-08: requisito não exige reatividade; persistência de tipo/valor fica em CT-50 |
| Teto de 40 e trim/maiúsculas como regra aprovada | não gerado: vêm somente do plano; Q1/Q2 |
| “Segunda aplicação retorna o mesmo total, logo é idempotente” | não gerado: não há Pedido persistido; L-IDEMP/Q6 |
| Apenas duas instâncias sequenciais para concorrência | insuficiente: mantido CT-35 para stale state e CT-36 separado para disputa real |
| Assert de log do canal cupom | cortado: não é RQ; R14 verifica a tabela própria de auditoria |
| Notificação de aplicação | não gerado: explicitamente fora do escopo do 00 |

CT-01 e CT-02 não são duplicação: renderização de campos e gravação têm defeitos diferentes.
CT-39 e CT-42 não são duplicação: contagem exata e autoria/instante diferem.
As tabelas de mutantes abaixo determinam a relação que cada CT precisa falsificar; não há score numérico alegado.

## Gate de falsificabilidade

- Cada regra tem entre três e seis mutantes plausíveis, exceto R4 com sete por M-73 trazido pela revisão adversarial, exceção prevista na skill. Não há regra exclusivamente de interface após retirar o recorte reativo sem oráculo.
- Cada mutante declara observável discriminante. Valores de borda, estado de partida e alvos de ausência estão explícitos.
- Uma linha de Exemplos tem só uma entrada inválida, exceto a combinação dupla de inelegibilidade requerida pela decisão, que tem também suas recusas isoladas.
- Cada “/” encontrado no rascunho foi expandido em linhas independentes antes da gravação; não é instrução para combinar campos inválidos.
- A previsão não certifica falha real. Depois da implementação, usar o lançador Windows da skill e escopo das classes; listar duração, sobreviventes e contraexemplo real.
- Sem vendor não se executou mutate; nenhum MSI foi atribuído. O teste não pode ganhar implementação para “passar” nesta rodada.

## Revisão adversarial

Host Codex, rota fw-adversario-ct via collaboration.spawn_agent, fork_turns=none; modelo herdado GPT-6 (variante não exposta).
Contrato agents/codex/fw-adversario-ct.toml adaptado por prompt, sem hooks Claude; ferramentas disponíveis não bloqueiam leitura por path. Restrição contratual; nenhum isolamento técnico alegado.
Entrada rodada 1: somente 00 e os 04/05 do rascunho; não recebeu 01, código ou raciocínio da derivação.
Rodada 1: nove achados únicos. Rodada 2: três achados únicos, por terem surgido cenários novos no fechamento anterior. Total: duas rodadas, teto atingido.
Custo: tokens e duração do subagente não expostos no retorno.

| Rodada/ID | Achado | Destino do fechamento | Prova discriminante |
|---|---|---|---|
| 1/ADV-01 | unicidade contextual só fora do formulário | cenário novo CT-51, M-67 | formulário da Globex aceita código já existente na Acme |
| 1/ADV-02 | fixo fracionário sem partição | oráculos reescritos CT-11/12, M-68 | fixo 1000,5 é recusado, não truncado para 1000 |
| 1/ADV-03 | IDOR direto de editar/excluir não exercitado | cenário novo CT-52, M-69 | admin local não edita nem remove instância de Globex |
| 1/ADV-04 | consumo sem contexto nulo não exercitado | cenário novo CT-53, M-70 | referência carregada não consome após remover contexto |
| 1/ADV-05 | cadastro e uso podiam ter mesmo instante | oráculo reescrito CT-42/M-56 | cadastro 17:00:00Z difere do uso 02:30:17Z do dia seguinte |
| 1/ADV-06 | pergunta suspendeu autoria obrigatória já determinada | cenário novo CT-54, M-71; Q8 reduzida | ausência/null não cria uso ou incremento anônimo |
| 1/ADV-07 | omissão na atualização confundida com campo apagado | oráculos reescritos CT-07/08 | editar só testa null/vazio que removam valor; payload parcial preservador não é recusado por omissão |
| 1/ADV-08 | reatividade/unidade visível sem reload não consta do 00 | lacuna declarada Q10 e retirada do oráculo inventado | R17/CT-B01/05 retirados; CT-50 realocado em R4; Sem CT-B |
| 1/ADV-09 | exclusão de inativos indevidamente suspensa | cenário novo CT-55, M-72 | três situações inativas são removidas; retenção da trilha continua Q7 |
| 2/ADV-10 | sinal fixo negativo já vedado por P-05 estava suspenso | oráculos reescritos CT-11/12, M-73; Q3 reduzida | fixo −1 não é gravado por componente nem model |
| 2/ADV-11 | concessão de admin em outro tenant não exercitada | oráculo reescrito CT-22, M-74 | papel admin somente em Globex não autoriza nenhum dos três verbos na Acme |
| 2/ADV-12 | regeneração perdeu coluna de implementação errada | tabelas/oráculos restaurados das 16 regras | 72 linhas finais contêm ID, implementação errada, CT e asserção em colunas distintas |

Auditoria da rodada 1: retorno no formato contratado, todas as oito tarefas e áreas percorridas.
Amostra conferida pela sessão: CT-20 só domínio na versão anterior (ADV-01); CT-42 sem criação distinta (ADV-05); P-01 requer User (ADV-06).
Hashes antes/depois da rodada 1, inclusive ambos os rascunhos, idênticos. Rodada 2: hash de entrada do 04 era 111C72CA00A45A898832FF10E9B6D783472C7337215647B61E33A895C267F8B3. O revisor declarou nenhuma escrita; a sessão não capturou outro hash do 04 entre o retorno e sua edição final. Controle de integridade dessa segunda rodada é parcial, sem alegar comparação ausente.
Os dois hashes do oráculo também permanecem iguais aos capturados antes da derivação.
Sem autorrevisão: o fechamento é decisão da sessão sobre achados do revisor independente.
Rodada 2 também percorreu o conjunto inteiro, confirmou ADV-01–09 e declarou a limitação da coluna ausente. Após o retorno, a sessão restaurou as descrições, acrescentou exemplos/asserções a CT existentes e verificou todas as tabelas mecanicamente.
Achado estrutural de contexto da concessão do papel foi registrado em ADV-11 e corrigido em CT-22; pela regra de teto, não houve terceira revisão. Escalonamento registrado como débito: confirmar independentemente os ajustes finais numa etapa posterior, sem pedir resposta nesta rodada indisponível.
CT-50 recebeu salvamento explícito no Quando, atendendo à observação de clareza do segundo retorno, sem ID ADV adicional.
Fechamento total: 5 cenários novos, 6 correções de oráculo/tabela (incluindo ADV-12) e 1 lacuna/apresentação retirada. Nenhum achado ficou oculto.

## Referências abertas

Feature-wiki:
- references/hosts-e-subagentes.md — contrato de host, step 7.
- references/ponytail-caveman.md — início; arquivos wiki em prosa normal.
- references/delegacao-casos-de-teste.md — step 7.
- references/roteamento-e-despacho.md — despacho adversarial.
- references/template-03-progresso.md — step 7; registro substituído pelo retorno, por instrução da rodada.
- references/citacoes-de-codigo.md — formato de citações; nenhum localizador vendor inventado.

Feature-test-design:
- references/template-04.md — passos 2/6/7 e escrita.
- references/escolha-de-camada.md — passos 2/7.
- references/tecnicas-por-regra.md — passo 3.
- references/taxonomia-de-defeito.md — passo 4, tabela inteira.
- references/gherkin.md — passo 5.
- references/armadilhas-de-api.md — passos 5/7.
- references/mutation-testing.md — passo 6, sem execução pós-implementação.
- references/revisao-adversarial.md — revisão.
- references/pest-plugin-browser.md — CT-B.
- references/template-05.md — escrita do 05.

Também lido o contrato agents/fw-adversario-ct.md e seu adaptador agents/codex/fw-adversario-ct.toml.
Não se abriu pasta inteira de references, catálogo de rodada ou outro conjunto 04/05.

## Sem CT-B

Nenhuma costura browser. O CRUD, tipo, valor, listagem, validação e autorização são falsificáveis por componente ou domínio.
O requisito não obriga rótulo reativo, ausência de reload, JS específico, pixel ou acessibilidade. O inventário de UI indica mecanismo, não um resultado a copiar para o Então.
O 05 existiu só como rascunho e foi retirado em ADV-08. Seu conteúdo não é critério de aceitação.

## Verificação documental

Conferência programática por PowerShell e pelos quatro grep -c de template-04.md, sem gravar script ou teste:
- 55 definições CT, 55 IDs únicos e 55 entradas no índice; diferenças entre definição e índice: 0.
- 16 regras, 72 mutantes previstos; nenhum CT matador inexistente e nenhuma asserção vazia.
- Um Quando e um Então em cada cenário; tabelas de Exemplos com largura consistente.
- As 16 tabelas de mutantes têm quatro colunas, com implementação errada presente em cada linha.
- 05 ausente, em consequência do gate; somente este 04 permanece na pasta.
- Oráculo 00 SHA256: 37130A6E4AB8D2EAB76F28F21DCDFDEA65E1D436FF3359A583BDC68086C5B943.
- Oráculo 01 SHA256: 3DDE1F461330527A606273767246CE0EBA9341C2787A05CE272ECD2FF2846C54.
- Hashes do 00/01 idênticos ao início. Não foi criado 02 ou 03 nem alterado arquivo fora da saída.
- As limitações de ambiente, cobertura de superfície e perguntas acima continuam em aberto; checagem documental não é execução de teste.

