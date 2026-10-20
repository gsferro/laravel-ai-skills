# Casos de Teste — FERRO-812: Cupons de desconto

> Derivado do **requisito**, não do plano. Não foi lida a implementação de cupons.
> Fonte normativa: `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md`.
> O `01` foi lido conforme solicitado; dele só entram nomes, paths, rotas e superfície de UI.
> Data: 2026-10-20. Host: Codex via API, Windows/PowerShell. Modelo informado: GPT-6; variante e esforço efetivos não expostos.
> Skills locais: feature-wiki **4.1.1**, feature-test-design **1.17.3**.
> Entrada no **step 7** da feature-wiki atual; corresponde à etapa de derivação mencionada na solicitação.
> Revisão adversarial: duas rodadas independentes; 3 + 3 achados fechados. Teto atingido; CT-57/58 novos após rodada 2 não receberam terceira revisão.
> Estado: especificação; nenhum teste Pest, código de aplicação ou mutation score foi executado/produzido.

## Perfil de Derivação

Todos os perfis foram **decididos pelo passo 0**; nenhum foi imposto pela rodada.

| Área | P | I | P×I | Perfil | Motivo |
|---|---|---|---|---|---|
| A — Cadastro e identidade | 3 | 3 | 9 | completo | Tipo condiciona domínio; unicidade depende da organização; parâmetros determinam dinheiro |
| B — Autorização e isolamento | 3 | 3 | 9 | completo | Papéis, contexto e fronteiras combinados; dados de terceiro e autorização |
| C — Cálculo monetário | 3 | 3 | 9 | completo | Duas grandezas, truncamento, centavos e piso zero; dinheiro |
| D — Aplicação, consumo e auditoria | 3 | 3 | 9 | completo | Concorrência, tempo e efeitos conjuntos; dinheiro e trilha |
| E — Operação da interface | 2 | 2 | 4 | padrão | Integração com componente de painel; erro exige retrabalho |

Há **Impacto 3** em A, B, C e D: revisão adversarial obrigatória do conjunto inteiro.
Regra que cruza E e A/B/D herda **completo**. Passos 1–7 integrais nas áreas completas; área E executa 1–7, sem pairwise, BVA 2-valores onde aplicável. BVA das áreas completas usa três valores e incremento de 1 unidade inteira ou 1 segundo. EP inválida é isolada por linha de dataset.
Cenários: 58 · Regras: 18 · Mutantes previstos: 83 · Sem matador: 1.
Cada Esquema conta um cenário; suas linhas continuam obrigatórias.

## Entradas, limites e degradações

- O `00` não tem coluna Estado nem seção formal de Premissas. As quinze RQ são tratadas como vigentes; P-01 a P-09 estão explicitamente assumidas em A-01 a A-09. A pergunta final da validade fixa comparação estrita `expira_em > agora`. As perguntas antigas não suspendem essas premissas dadas pelo usuário.
- **02 ausente**: `Test-Path wikis/specs/oraculo/cupons-de-desconto/02-decisoes-arquiteturais.md` = False. Nenhum 02 foi criado. Inventário da Superfície Livewire não foi reconstruído lendo implementação. Cobertura completa dessa superfície permanece **lacuna declarada**.
- `wikis/glossario.md` ausente; vocabulário é o do 00.
- `composer show --direct`: **No dependencies installed. Try running composer install or update.** `Test-Path vendor` = False. PHP CLI **8.4.10**, Xdebug **3.4.4**.
- `composer.lock`: Laravel **13.25.0**, Filament **5.7.6**, Livewire **4.4.0**, Pest **5.1.1**, browser plugin **5.0.1**, mutate plugin **5.0.2**, Boost **2.5.3**. São versões travadas, **não instalações verificadas**. `package.json`: Playwright `^1.62.1`. Não houve instalação ou alteração de dependências.
- Busca nas ferramentas expostas por `search.?docs|laravel|boost` retornou lista vazia. Boost/search-docs indisponível nesta sessão. Nenhuma API nova de pacote é afirmada como verificada; a especificação usa comportamento declarativo e convenções observadas nos testes irmãos.
- `pestphp/pest-plugin-mutate` está no lock, mas não declarado diretamente no composer.json. Não editar o PRD imutável; registrar para posterior reconciliação a necessidade de dependência direta autorizada antes de medir mutantes.
- O escopo termina na especificação. O gate do passo 6 é **falsificabilidade prevista**, não medição de mutação. Execução, sincronização real, validade dos helpers no vendor e prova sem correção continuam pendentes.
- Nenhum `03` será criado. Despachos, referências e degradações ficam neste arquivo e no retorno, por instrução expressa.
- Aplicação não é automaticamente atribuída a panel_user: “apenas listar” torna o ator da aplicação uma questão separada (Q7). Os cenários de sucesso usam administrador legitimado.
- P-02 afirma acesso de master_global **e admin da instalação** ao cupom, além de admin_organizacao. A matriz conflitante do PRD não substitui essa premissa. Os cenários preservam P-02; a divergência deve ser reconciliada antes da implementação.

## Varredura SFDIPOT

| Dimensão | Varredura anterior aos cenários | Recorte a provar |
|---|---|---|
| Structure | Cupom, CupomUso, enum, campos, índice por organização, policy e Resource; nomes do 01 são endereços, não oráculos | Gravação, identidade, limites e trilha |
| Function | Criar, ler/listar, editar, excluir, localizar, aplicar desconto, consumir e registrar autoria/instante | Cada verbo próprio; nenhuma autorização herdada do verbo irmão |
| Data | Código obrigatório, dois tipos, grandezas inteiras, timestamps, contadores, duplicata, nulos e dado estrangeiro | EP, BVA, tipo × valor, duas organizações |
| Interfaces | Painel /app; componentes de criar/editar/listar/excluir; motor chamado fora da UI por P-01 | Pares visita/gravação e barreiras fora do componente |
| Platform | PHP 8.4; DB com transações e relógios; single e multi-tenant; colação e NULL em unicidade | Mesma identidade no modo sem tenant; prova de corrida em DB compartilhado |
| Operations | Administrações distintas, usuário comum, infra, pessoa sem papel; acúmulo de papéis e troca de organização | Matriz papel × ação; contexto da ação |
| Time | Instante exato de expiração, virada de dia, snapshots velhos, simultaneidade, horário de auditoria | BVA de segundo; fuso divergente e rollback |

Nenhuma dimensão foi dispensada. Upload, notificações e jobs não são obrigações do 00; não são acrescentados à entrega.

## Estados e operações — matriz única anterior às regras

Estados não são inventados a partir do PRD: P-03 define ativo por validade e disponibilidade; o 00 permite exclusão.
**A**: existente, expira no futuro, usos abaixo do limite.
**V**: existente, expirado (inclui igualdade), com usos disponíveis.
**E**: existente, válido no tempo, esgotado.
**VE**: existente, expirado e esgotado.
**X**: excluído por operação real ou identidade inexistente. Uma fixture excluída sempre teve registro antes.

Operações sobre uma identidade: **consultar/localizar**, **listar**, **editar**, **excluir**, **aplicar**.
São **5 estados × 5 operações = 25 células**. Cadastro nasce sem identidade e é coberto à parte; não é estado omitido.
Legenda: ✅ executa e afirma valor/registro; ❌ executa e afirma todos os não-efeitos da coluna; L = lacuna explícita. A coluna editar inclui código e os campos que decidem cálculo/validade/limite, sem fixar só um campo inofensivo.

| Estado | Consultar/localizar | Listar, usuário comum | Editar, admin | Excluir, admin | Aplicar, admin |
|---|---|---|---|---|---|
| A | ✅ CT-37 | ✅ CT-29, CT-30 | ✅ CT-17, CT-11 | ✅ CT-18 | ✅ CT-38, CT-48 |
| V | ❌ CT-37, CT-39 | ❌ CT-29, CT-30 | L Q3; invariante CT-20 | ✅ CT-18, sem usos prévios | ❌ CT-38, CT-40 |
| E | ❌ CT-37 | ❌ CT-29, CT-30 | L Q4; invariante CT-20 | L Q5, possui trilha | ❌ CT-38, CT-42 |
| VE | ❌ CT-37 | ❌ CT-29, CT-30 | L Q3/Q4; invariante CT-20 | L Q5, possui trilha | ❌ CT-38 |
| X | ❌ CT-37 | ❌ CT-29 | ❌ CT-19 | ❌ CT-19 | ❌ CT-21 |

Contagem: **6 válidas, 14 inválidas, 5 lacunas = 25**. Lacuna de editar não afirma aceitação nem recusa; CT-20 prova somente preservação do contador/trilha já devidos por RQ-13/15.
Não-efeitos por coluna: consultar/listar não consomem nem criam trilha; editar recusado não altera nenhum dos cinco campos nem contador/trilha; excluir recusado não remove cupom nem seus usos; aplicar recusado não devolve total descontado, não incrementa, não cria/remove/altera uso anterior.
Persona e campo são dimensões adicionais: R8–R10 exercitam cada escrita como usuário comum, R12 usa outra organização e contexto ausente. Cada célula resolvida deve executar seu próprio verbo; não é cobertura emprestada da listagem.

## Mapa de Regras

| Regra | Área / perfil herdado | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — Todo cupom gravado tem código | A / completo | RQ-02 | EP de presença, criação e edição | CT-01, CT-02 |
| R2 — O tipo obrigatório pertence aos dois tipos do requisito | A / completo | RQ-03, P-05 | EP de enum e tipo; criar, editar e usar | CT-03, CT-04 |
| R3 — Valor respeita unidade e domínio condicionado pelo tipo | A/C / completo | RQ-04/12, P-05/P-07 | EP; BVA 3-valores; tabela tipo × valor | CT-05, CT-06, CT-07 |
| R4 — Validade e limite de usos são dados obrigatórios | A / completo | RQ-05/06 | EP de presença e representação; criação ≠ edição | CT-08, CT-09 |
| R5 — Código não se repete no mesmo contexto e pode repetir entre organizações | A/B / completo | RQ-14, P-04 | EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade | CT-10, CT-11, CT-12, CT-13, CT-57 |
| R6 — Cadastro e edição operam pela tela do painel | E/A / completo | RQ-01–06, P-05/P-09 | Par visita × gravação; EP dos dois tipos; edição após uso | CT-14, CT-15, CT-16, CT-17, CT-20 |
| R7 — Exclusão e identidade inexistente não deixam cupom utilizável | A/D / completo | RQ-01/07/09/13/15, P-01/P-08 | Estado × operação; exclusão real; CRUD combinado | CT-18, CT-19, CT-21 |
| R8 — Somente os administradores dados por P-02 podem criar | B / completo | RQ-07/08, P-02/P-09 | Matriz papel × criar; execução fora do componente e pela UI | CT-22, CT-23, CT-24 |
| R9 — Somente administradores podem editar, inclusive com papéis acumulados | B / completo | RQ-07/08, P-02 | Matriz papel × editar; pares de papéis; estado/campo discriminante | CT-25, CT-26, CT-56 |
| R10 — Somente administradores podem excluir | B / completo | RQ-07/08, P-02 | Matriz papel × excluir; verbo destrutivo independente | CT-27, CT-28 |
| R11 — Usuário comum lista somente cupons ativos | B/E / completo | RQ-08, P-03 | Tabela de decisão completa; EP de estado; cardinalidade e paginação | CT-29, CT-30, CT-31, CT-55, CT-58 |
| R12 — Toda operação mantém a fronteira da organização | B / completo | RQ-01/07/08/12–15, P-02/P-04/P-08 | IDOR; mass assignment; contexto nulo; troca de tenant | CT-32, CT-33, CT-34, CT-35, CT-36 |
| R13 — A aplicação depende de existência, validade e disponibilidade juntas | D / completo | RQ-09–13, P-01/P-03 | EP de existência; tabela de decisão completa com restrições | CT-37, CT-38 |
| R14 — Validade termina no instante gravado, inclusive após leitura anterior | D / completo | RQ-05/10, pergunta final de validade do 00 | BVA 3-valores de segundo; tempo de uso; fuso e DST | CT-39, CT-40, CT-41 |
| R15 — Limite global não é ultrapassado por snapshot nem corrida | D / completo | RQ-06/11/13, P-01 | BVA 3-valores; concorrência real; snapshots distintos | CT-42, CT-43, CT-44 |
| R16 — Desconto usa inteiros, trunca porcentagem e limita o total em zero | C / completo | RQ-12, P-01/P-05/P-06/P-07 | EP dos tipos; BVA monetária de centavo; exemplos discriminantes | CT-45, CT-46 |
| R17 — Cada aplicação aceita consome um uso e somente o seu cupom | D / completo | RQ-11/13, P-01/P-05 | Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa | CT-47, CT-48, CT-49, CT-50 |
| R18 — Cada uso aceito registra autor e instante com consumo e trilha consistentes | D / completo | RQ-13/15, P-01/P-08 | Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito | CT-51, CT-52, CT-53, CT-54 |

Todas as quinze RQ geram regras. P-01: R7/R13–R18; P-02: R8–R12; P-03: R11/R13; P-04: R5/R12; P-05: R2/R3/R6/R16; P-06/P-07: R16; P-08: R7/R12/R18; P-09: R6/R8.
Cobertura parcial: RQ-02/14 normalização e teto Q1; RQ-04/12 domínios residuais Q2; RQ-05 cadastro temporal Q3; RQ-06 redução/zero Q4; RQ-07/15 retenção Q5; RQ-12/13 idempotência no Pedido Q6; RQ-08 aplicação por usuário comum Q7 e leitura de outros perfis Q11; RQ-01 apresentação Q8; RQ-15 exposição da trilha Q9; RQ-08 paginação concorrente Q10. Nenhuma RQ é suspensa por inteiro.

## Costuras de Teste — decisão antes do passo 5

Decididas e **confirmadas pela sessão em 2026-10-20**, sob autorização desta tarefa e convenções reais de `tests/Pest.php`.
Não há escolha material de arnês a devolver ao usuário. Os testes citados são destinos **propostos**, não arquivos criados.

| Grupo | Regras | Costura | Existente ou nova | Por quê esta camada | Confirmada |
|---|---|---|---|---|---|
| G1 — Domínio nos dois modos | R1–R5, R7–R18 | Pest feature HTTP | existente: tests/Kit e tests/Tenancy | DB, autorização, cálculo e efeitos; TestCase ou TenancyTestCase conforme pasta | sessão, 2026-10-20 |
| G2 — Componentes nos dois modos | R1–R12 | componente Livewire/Filament | existente: AdminDaOrganizacaoTest nas duas suítes | Campos, gravação e ações reais; sem navegador | sessão, 2026-10-20 |
| G3 — Visitas HTTP | R6, R8–R12 | Pest feature HTTP | existente: testes HTTP em tests/Kit e tests/Tenancy | Rota e conteúdo específico; par da gravação por componente | sessão, 2026-10-20 |
| G4 — Concorrência | R5, R15 | Pest feature HTTP | nova dentro de tests/Tenancy | DB compartilhado, duas conexões/processos e disputa de identidade/consumo; memória privada não prova disputa | sessão, 2026-10-20 |

G4 não exige criar infraestrutura agora. É uma premissa **de mecanismo**, não dispensa CT-44. Na materialização, usar banco descartável compartilhado, commits reais e barreira dentro da janela leitura→escrita, imediatamente antes da primeira escrita real de consumo de cada executor. Instrumentar a fronteira de conexão no teste, sem duplicar a regra de consumo nem editar produção. Confirmar que ambos concluíram as leituras antes de liberar as escritas; registrar autores, resultados e persistência por terceira conexão. Se indisponível, CT-44 fica **não executado**, nunca substituído por CT-43.
Não há costura unit de regra: tests/Unit não recebe TestCase no Pest.php; P-01 aplica, persiste e recebe User. Não se inventa predicado puro só para baratear teste.
Não há costura browser: decisão detalhada em “Sem CT-B”.

## Fronteira com o Plano

| Item visto no PRD | Uso permitido ou recusa como oráculo | Destino |
|---|---|---|
| aplicarEm, valido, nomes dos models, campos e páginas | Nomes/endereço para materializar a regra do 00; não exigir retorno null, classe de exceção ou algoritmo SQL específico | Detalhe de execução |
| Total inteiro, tipos, truncar e piso zero | Também estão em P-01/P-05/P-06/P-07; origem é o 00 | R3, R16 |
| scopedUnique, ignoreRecord | P-04 exige unicidade por organização; provar resultado, inclusive salvar a própria identidade | R5 |
| Código com 40 caracteres, uppercase e trim | Limite e equivalência não foram decididos pelo 00 | Q1; sem aceitação/recusa inventada |
| Fixo mínimo 1, validade mínima agora, limite mínimo 1 | O 00 não determina todos esses domínios de cadastro | Q2–Q4; cenários da parte determinada preservados |
| aplicadoPor opcional/null | Contradiz assinatura obrigatória de P-01 e autoria de RQ-15 | R18 recusa ausência; não legitimar trilha anônima |
| cascade ao excluir trilha e nullOnDelete de autor | RQ-15 pede auditoria; política de retenção não está no 00 | Q5; não certificar perda de auditoria |
| Rótulos reativos, sufixo, badge, precedência Esgotado/Expirado e cores | Comportamento visível só do PRD; P-03 determina ativo, não esses textos/cores | Q8; não criar CT-B para certificar escolha do plano |
| “Sim, depende de JS” e fluxo entre telas | Não tornam necessária uma asserção exclusiva de navegador | Costura de componente |
| Logs, contagem de permissions, número antigo de CT, comandos de commit | Não são cláusulas de desconto | Não gerar CT |
| Admin da instalação fora do /app | Conflita com acesso afirmado em P-02 | P-02 prevalece; registrar divergência |
| Ausência de endpoint de CupomUso | Sem 02/vendor não prova ausência de fronteira pública | Q9 e lacuna de IDOR/mass assignment da tabela filha |

## Perguntas para o 00-requisito.md

**Desvio autorizado:** 00 imutável e usuário indisponível. Bloco pronto para colagem; nenhuma recomendação abaixo é resposta assumida. Q1–Q11 são novos IDs, pois o 00 só tem A-01…A-09 e perguntas numeradas sem prefixo Q. A ausência de 02/03 impede auditar sequência fora dos insumos autorizados.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | Código ignora caixa/espaços? Quais caracteres e comprimento máximo aceita? | RQ-02/14, P-04; apenas equivalência e teto textual | Definir normalização única e limite antes de gravar; recusar entradas que não possam ser representadas sem perda | aberta |
| Q2 | Valor fixo zero é válido? Qual teto de valor e quais totais de entrada são admitidos, inclusive negativo/zero? | RQ-04/12, P-05/07; domínio não definido | Falhar fechado para negativos e valores sem representação; confirmar zero e teto; nunca devolver total negativo | aberta |
| Q3 | Pode criar/editar cupom com validade no passado ou exatamente agora? | RQ-05/10; somente gravação, não recusa no uso | Recusar na gravação, pois o mesmo requisito o considera inaplicável no uso | aberta |
| Q4 | Qual domínio do limite? Pode zerar ou reduzir abaixo dos usos já feitos? | RQ-06/11/13/15; gravação/redução | Recusar limite não positivo ou inferior aos usos; preservar contador e trilha | aberta |
| Q5 | Como excluir cupom já usado sem perder auditoria? O que ocorre se autor for excluído? | RQ-07/15, P-08; retenção | Preservar evidência de autoria/instante; bloquear remoção destrutiva até existir retenção definida | aberta |
| Q6 | Aplicar novamente ao mesmo pedido é idempotente? Qual identidade persistida representa essa intenção? | RQ-12/13, P-01 | Falhar fechado para reaplicação duplicada no futuro agregado; manter lacuna enquanto Pedido estiver fora de escopo | aberta |
| Q7 | “Apenas listar” veda ao panel_user também o motor de aplicação? | RQ-08/12/15, P-01 | Negar aplicação sem autorização definida; cenários atuais de uso usam administrador | aberta |
| Q8 | A UI deve atualizar unidade visível ao trocar tipo? Quais rótulos/status são aceitos? | RQ-01/03/04/08, P-03/05; apresentação | Exibir unidade inequívoca e coerente com o tipo antes de gravar; confirmar obrigação e textos | aberta |
| Q9 | Há acesso direto ou gravação independente na trilha CupomUso? Quais atores podem consultar ou alterar? | RQ-15, P-02/08; tabela filha | Negar leitura/escrita fora da organização e criação/alteração manual da trilha; inventariar superfície antes de liberar | aberta |
| Q10 | Qual garantia de ordenação/paginação durante inserção concorrente? | RQ-08; consistência da navegação | Ordenação total determinística, sem perder cupons ativos; não certificar snapshot sem decisão | aberta |
| Q11 | Como infra e pessoa sem papel alcançam a leitura, e como acumular papéis de painéis diferentes? | RQ-08, P-02; acesso ao painel | Negar acesso sem vínculo/autorização de leitura explícita; preservar leitura de panel_user já determinada | aberta |

Formato da entrevista, sem despacho de perguntas ao usuário:
- ❓ Q1–Q11 · raia: requisito · afeta: IDs da tabela · depende de: —.
- ➡️ Recomendação: coluna correspondente; toda decisão de aceitar/recusar desconhecida recomenda falha fechado.
- Perguntas não reabrem RQ inteiras: somente os recortes indicados ficam sem cenário direcional.
- Invariantes independentes continuam obrigatórios: expirado não se aplica; total final nunca negativo; tentativa de editar não corrige contador nem apaga trilha.


CT-57 amplia G4 para a gravação de identidade: sincronizar após as duas verificações de unicidade e antes das escritas reais de criação/renomeação, sem mudar produção. Usar commits reais e reler por terceira conexão nos dois modos. Restrição de índice com NULL não é desculpa para duplicação válida.

## Técnicas formais — execução do passo 3

### Decisão completa de elegibilidade
Existência, tempo e disponibilidade são os três fatores críticos. Foi usada decisão completa, mais forte que reduzir a pairwise.

| Existe | expira_em > agora | usos < limite | Resultado | Evidência |
|---|---|---|---|---|
| não | irrelevante | irrelevante | recusa | CT-37 |
| sim | sim | sim | aceita | CT-38 |
| sim | não | sim | recusa | CT-38 |
| sim | sim | não | recusa | CT-38 |
| sim | não | não | recusa | CT-38 |

São oito combinações booleanas brutas, colapsadas em cinco linhas: as quatro inexistentes têm tempo/contador sem objeto. As três linhas negativas com objeto são exercitadas separadamente e a interseção negativa é adicional, não substitui as recusas isoladas. Percentual e fixo repetem cada direção de contador/trilha.
Estado derivado é observado como elegibilidade/presença, não como strings de badge inventadas no PRD.
Não se aplica 2-switch de workflow com aprovações: o 00 não define esse ciclo. A possível reativação por edição está aberta em Q3/Q4; o invariante de história é CT-20.

### Tipo × valor e bordas
Porcentagem: mínimo 1 e máximo 100 de P-05; BVA **0/1/2** e **99/100/101** em criar e editar (CT-05); uso de dado inválido isolado em CT-07.
Fixo: inteiro de centavos por P-05; **1000** deve poder ser gravado mesmo acima do teto percentual. Borda de aplicação **999/1000/1001** contra desconto 1000 em CT-46. Não inventar mínimo comercial 1 nem teto físico como requisito: zero e teto estão em Q2.
Validade: unidade de timestamp **1 segundo**, tanto lookup quanto aplicação (CT-39), inclusive igualdade e relógio que avança (CT-40).
Contador: **2/3/4**, limite 3 (CT-42); caso 4 é corrupção isolada, não autorização para gravar limite inválido.
Na gravação de data e limite, fronteiras comerciais não decididas ficam Q3/Q4. Presença e representação já são determinadas e testadas por CT-08/09.
Texto: ausência/null/vazio têm cenários próprios em Exemplos; teto, unicode/normalização e espaços ficam Q1, pois 40/uppercase/trim só estão no plano.

### Matriz papel × ação e independência
| Papel simples | Criar | Editar | Excluir | Listar |
|---|---|---|---|---|
| master_global | CT-22/24, aceita | CT-25, aceita | CT-27, aceita | CT-55, acesso próprio |
| admin | CT-22/24, aceita por P-02 | CT-25, aceita por P-02 | CT-27, aceita por P-02 | acesso por P-02; conflito do PRD registrado |
| admin_organizacao | CT-22/24, aceita em multi-tenant | CT-25, aceita | CT-27, aceita | acesso próprio; CT-33 não é autorização alheia |
| panel_user | CT-22/23, recusa | CT-25/26, recusa | CT-27/28, recusa | CT-29/30/31/55, só ativos |
| infra | CT-22, recusa | CT-25, recusa | CT-27, recusa | Acesso à tela Q11; nenhum inativo pela consulta direta em CT-58 |
| sem papel | CT-22, recusa | CT-25, recusa | CT-27, recusa | Pessoa autenticada: acesso Q11; nenhum inativo em CT-58; não supor acesso anônimo |

Cada escrita executa o verbo; uma asserção can() ou uma consulta a permission não substitui execução.
CT-25 inclui todos os pares dos cinco papéis: master_global+admin, master_global+admin_organizacao, master_global+panel_user, master_global+infra, admin+admin_organizacao, admin+panel_user, admin+infra, admin_organizacao+panel_user, admin_organizacao+infra, panel_user+infra. Os nove primeiros permitem editar por haver administrador; o último recusa com valor 10. Contextos de papéis são respeitados; admin_organizacao só no modo com tenancy.
As matrizes de papéis e estados são completas nos seus recortes. Não se usa pairwise para descartar célula de autorização ou estado. Para integração, executar criação, edição e exclusão com as duas partições válidas de tipo nos dois modos de tenancy: porcentagem 10 e fixo 1234, expiração futura, código livre por linha. Restrição: admin_organizacao só existe com tenancy. É expansão 3-a-3 de modo × tipo × autorização nos grupos críticos, sem mesclar campos inválidos.

### Rastreio de efeito e exemplo discriminante
- Contador e trilha: aconteceu CT-48/51, não aconteceu CT-49/52, uma vez CT-48/51, rollback CT-53/54.
- Cada direção é repetida nos **dois tipos**, incluindo corrupção/recusa, corrida e exclusão após captura.
- Auditoria é o registro de uso exigido em RQ-15; nenhuma linha de log vira oráculo.
- Mundo não vazio: os casos de recusa têm cupom, autor real, usos/trilha anteriores ou cupom testemunha real. A identidade inexistente usa testemunha aplicável.
- Contraexemplo confirmado neste PHP: `php -r 'var_export([100 - intdiv(100 * 29, 100), 100 - (int) (100 * 0.29)]);'` devolveu **[71, 72]**. CT-45 discrimina o float plausível.
- CT-41 fixa o instante dentro da janela de divergência de fuso; não usa um horário em que UTC/local produziriam a mesma resposta.
- Toda ausência é comparada ao snapshot persistido antes da ação, por chave, autor e instante, não somente por count.

## Setup Global

### Personas e contexto
Reutilizar `usuarioCom()`, `usuarioDoKit()`, `usuarioComPapel()`, `papelNaOrganizacao()`, `noPainelDa()` e `fronteiraDeRequest()` de tests/Pest.php. Helpers compartilhados futuros pertencem somente a esse arquivo; nenhum helper será escrito nesta entrega.
Semeação segue o TestCase existente, com ShieldPermissionsSeeder antes de PapeisSeeder. Não semear permissões fictícias para fazer a expectativa passar. Nos testes de modelo sem Resource, usar a verdadeira operação chamável; **não inserir Gate::authorize() no corpo do teste como se fosse barreira do produto**. Se não existir ponto protegido fora da UI, manter cenário vermelho/divergência, não substituí-lo por can().
Ana, Bruno e Carla são pessoas distintas. Cada tenant tem cupom testemunha e autoria própria. Pessoa que pertence a dois tenants não recebe autorização na Globex só porque administra Acme.
Antes de cada teste de componente: autenticar o ator; painel app; tenant e permissions team fixados com helper real. Não usar master_global para testar autorização de panel_user.

### Fixtures e relógio
UserFactory e TenantFactory existem, com states observados `unverified()` e `comIdentidadeVisual()`. CupomFactory **não existe no snapshot recebido**; é só endereço proposto pelo 01. Materialização deve criar cupons pela criação real com os cinco campos; não depender de factory não instalada.
Base: código PROMO10, porcentagem 10 ou fixo 1234, expiração 2026-11-20T15:00:00Z, limite 3, relógio em 2026-10-20T15:00:00Z; demais dados variam somente quando o cenário diz.
Fixtures com uso anterior nascem por aplicações reais, com autor e relógio explícitos. Esgotado nasce repetindo aplicação legítima até o limite; expirado nasce avançando relógio após cadastro; excluído nasce chamando a exclusão real. Não gravar situacao à força.
Dado legado inválido de CT-04/07/42 é a exceção explícita: inserir ou alterar **somente** a coluna inválida no arnês de teste, conferir o valor relido antes da ação e manter os demais campos válidos. Se o banco/cast recusar ou coerir o valor, registrar a prova de pré-condição inexprimível nessa pilha; não dizer que o caso matou o mutante. Migrar o caso para driver compatível ou testar a entrada antes da coerção. Não usar essa exceção nas fixtures positivas.
CT-20 usa trilha existente: tentativa de reduzir limite nunca autoriza regravar contador nem apagar usos.
Restaurar relógio/fuso entre os exemplos. CT-41 escreve e relê o mesmo instante absoluto, conferindo app, conexão e timezone do dado; se a pilha em memória não expuser offset/DST, tentar driver com timezone de sessão, registrar tentativa e manter prova pendente.
Aplicar usa o contrato obrigatório `Cupom::aplicarEm(int, User): int` de P-01. Não assumir a versão opcional do PRD.

### Persistência, camadas e falhas
tests/Kit usa TestCase+RefreshDatabase; tests/Tenancy usa TenancyTestCase+RefreshDatabase antes das migrations de teams. Não mudar flag num beforeEach depois do bootstrap.
Destinos propostos: `tests/Kit/CupomTest.php` e `tests/Tenancy/CupomTenancyTest.php`; CT-44 somente no arnês compartilhado da segunda suíte. Nada foi criado em tests/.
CT-15 materializa fillForm→create; CT-17 fillForm→save, com record pela chave real de rota uuid e asserções dos cinco campos. Não exigir redirect da edição. CT-14/16 são suas visitas irmãs.
Os nomes de helpers vistos nos testes irmãos, como loadTable e assertCanSeeTableRecords, são convenção observada; verificar vendor da versão travada antes da execução. Não usar helpers deprecated.
CT-53 injeta falha da persistência da trilha **depois** da escrita do contador; verificar que o ponto foi atingido. CT-54 injeta falha **depois do INSERT da trilha e antes do commit**. Preferir hook/observador de teste sobre a conexão ou evento de persistência, removido no teardown. Um erro na pré-validação não é evidência de rollback.
Reler DB após falha, sem confiar no objeto em memória nem em transação externa que mascare o commit. Nenhum fake global de eventos antes das fixtures: isso impediria uuid e transições reais.
Recusas de domínio não exigem mensagem/classe de exceção que só o PRD nomeia. Recusas HTTP devem ter seu destino posterior exercitado por CT-55. Se um componente não permite montar a ação proibida, prova de mount recusado não substitui a execução direta externa.


## Regra R1 — Todo cupom gravado tem código

> Origem: RQ-02 · área A · perfil **completo** · técnica: **EP de presença, criação e edição**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Todo cupom gravado tem código

    Esquema do Cenário: [CT-01] Código obrigatório na criação e na edição
      Dado o administrador autorizado e os demais campos válidos de um cupom ativo, com outro cupom testemunha
      Quando o administrador tenta <operacao> pelo formulário com código <entrada>
      Então há erro especificamente em codigo e nenhum cupom novo é gravado
      E na edição todos os campos, contador e trilha do cupom original permanecem iguais
      Exemplos:
        | operacao | entrada | particao |
        | criar | ausente | ausência |
        | criar | null | nulo |
        | criar | "" | vazio |
        | editar | ausente | ausência |
        | editar | null | nulo |
        | editar | "" | vazio |

    Esquema do Cenário: [CT-02] O domínio recusa ausência de código fora do componente
      Dado o administrador autorizado, dados restantes válidos e um cupom ativo existente para a edição
      Quando o administrador tenta <operacao> diretamente na via de domínio com codigo <entrada>
      Então a gravação é recusada por codigo e não nasce cupom sem código
      E os campos, o contador e a trilha do cupom existente não mudam
      Exemplos:
        | operacao | entrada | particao |
        | criar | ausente | ausência |
        | criar | null | nulo |
        | criar | "" | vazio |
        | editar | null | nulo |
        | editar | "" | vazio |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Obrigatoriedade só no create | CT-01 | editar/null recusa e preserva código anterior |
| M-02 | Obrigatoriedade só no formulário | CT-02 | chamada direta criar/null não persiste cupom |
| M-03 | String vazia passa por checagem apenas de null | CT-02 | criar/"" recusa sem inserir |

## Regra R2 — O tipo obrigatório pertence aos dois tipos do requisito

> Origem: RQ-03, P-05 · área A · perfil **completo** · técnica: **EP de enum e tipo; criar, editar e usar**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: O tipo obrigatório pertence aos dois tipos do requisito

    Esquema do Cenário: [CT-03] O formulário grava somente os dois tipos definidos
      Dado o administrador autorizado e cupom ativo com valor 10, código livre, expiração futura e limite 3
      Quando o administrador tenta <operacao> pelo formulário com tipo <entrada>
      Então o resultado é <resultado> e o tipo persistido é <persistido>
      E uma recusa acusa tipo, não altera campos/contador/trilha e não cria cupom
      Exemplos:
        | operacao | entrada | resultado | persistido | particao |
        | criar | porcentagem | aceito | porcentagem | válido |
        | criar | fixo | aceito | fixo | válido |
        | editar | fixo | aceito | fixo | válido |
        | criar | null | recusado | nenhum | nulo |
        | editar | "" | recusado | tipo anterior | vazio |
        | criar | cashback | recusado | nenhum | fora do domínio |
        | editar | cashback | recusado | tipo anterior | fora do domínio |
        | criar | [] | recusado | nenhum | tipo errado |
        | editar | [] | recusado | tipo anterior | tipo errado |

    Esquema do Cenário: [CT-04] Tipo inválido não ganha validade pela chamada direta
      Dado um administrador, valores restantes válidos e um cupom existente ativo para os casos de edição e uso
      Quando o administrador tenta <operacao> fora da UI com tipo <entrada>
      Então a operação é recusada por tipo e nenhum total com desconto é entregue
      E nenhum campo ou contador é alterado e nenhuma linha de uso é criada ou removida
      Exemplos:
        | operacao | entrada | particao |
        | criar | cashback | fora do domínio |
        | editar | cashback | fora do domínio |
        | criar | ausente | ausência |
        | criar | null | nulo |
        | editar | "" | vazio |
        | usar legado isolado | cashback | fora do domínio |
        | usar legado isolado | [] | tipo errado |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-04 | Tipo não reconhecido tratado como fixo | CT-04 | usar legado/cashback recusa sem desconto nem uso |
| M-05 | Enum validado só no formulário | CT-04 | criar/cashback não persiste |
| M-06 | Editar conserva tipo antigo ignorando seleção | CT-03 | editar/fixo persiste fixo |

## Regra R3 — Valor respeita unidade e domínio condicionado pelo tipo

> Origem: RQ-04/12, P-05/P-07 · área A/C · perfil **completo** · técnica: **EP; BVA 3-valores; tabela tipo × valor**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Valor respeita unidade e domínio condicionado pelo tipo

    Esquema do Cenário: [CT-05] Bordas do percentual são validadas na gravação do componente
      Dado o administrador e dados válidos de cupom ativo, alterando somente tipo e valor
      Quando o administrador tenta <operacao> pelo formulário com tipo <tipo> e valor <valor>
      Então a operação tem resultado <resultado> e, se aceita, persiste exatamente tipo e valor informados
      E a recusa acusa valor e preserva campos, contador e trilha anteriores
      Exemplos:
        | operacao | tipo | valor | resultado | particao |
        | criar | porcentagem | 0 | recusado | mínimo−1 |
        | criar | porcentagem | 1 | aceito | mínimo |
        | criar | porcentagem | 2 | aceito | mínimo+1 |
        | criar | porcentagem | 99 | aceito | máximo−1 |
        | criar | porcentagem | 100 | aceito | máximo |
        | criar | porcentagem | 101 | recusado | máximo+1 |
        | editar | porcentagem | 0 | recusado | mínimo−1 |
        | editar | porcentagem | 1 | aceito | mínimo |
        | editar | porcentagem | 2 | aceito | mínimo+1 |
        | editar | porcentagem | 99 | aceito | máximo−1 |
        | editar | porcentagem | 100 | aceito | máximo |
        | editar | porcentagem | 101 | recusado | máximo+1 |
        | criar | fixo | 1000 | aceito | centavos, teto percentual não se aplica |
        | editar | fixo | 1000 | aceito | centavos, teto percentual não se aplica |

    Esquema do Cenário: [CT-06] A gravação direta aplica o domínio do valor
      Dado o administrador e dados restantes válidos de um cupom ativo
      Quando o administrador tenta <operacao> diretamente com tipo <tipo> e valor <entrada>
      Então a gravação é recusada especificamente pelo valor
      E nenhum cupom é inserido e campos, contador e trilha existentes permanecem iguais
      Exemplos:
        | operacao | tipo | entrada | particao |
        | criar | porcentagem | ausente | ausência |
        | criar | porcentagem | null | nulo |
        | editar | porcentagem | "" | vazio |
        | criar | porcentagem | 0 | mínimo−1 |
        | editar | porcentagem | 101 | máximo+1 |
        | criar | porcentagem | 12.5 | fração não admitida |
        | editar | porcentagem | 12.5 | fração não admitida |
        | criar | fixo | -1 | unsigned, abaixo de zero |
        | editar | fixo | -1 | unsigned, abaixo de zero |
        | criar | fixo | 10.5 | fração de centavo |
        | editar | fixo | [] | tipo errado |

    Esquema do Cenário: [CT-07] Valor legado inválido não produz desconto aplicável
      Dado um cupom existente, válido no tempo, com uso disponível, um administrador real e somente valor legado <valor> inválido
      Quando o administrador tenta aplicar o cupom de tipo <tipo> ao total 10000 por chamada direta
      Então nenhum total com desconto é entregue
      E o contador permanece igual e não nasce linha de uso nem se altera a trilha anterior
      Exemplos:
        | tipo | valor | particao |
        | porcentagem | 0 | mínimo−1 |
        | porcentagem | 101 | máximo+1 |
        | porcentagem | 12.5 | fração |
        | fixo | -1 | unsigned |
        | fixo | 10.5 | fração de centavo |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-07 | Teto 100 aplicado também a fixo | CT-05 | fixo/1000 grava 1000 em criar e editar |
| M-08 | Comparação escalar com state enum perde teto percentual | CT-05 | porcentagem/101 é recusado em criar e editar |
| M-09 | Percentual aceita fração e a trunca silenciosamente | CT-06 | porcentagem/12.5 é recusado; não vira 12 |
| M-10 | Validação existe só no create | CT-06 | editar/porcentagem/101 recusa fora da UI |
| M-11 | Uso confia no dado legado sem validar domínio | CT-07 | 101 não entrega desconto nem consome |
| M-12 | Valor decimal de centavo é coercido para inteiro | CT-06 | fixo/10.5 recusa sem arredondar |

## Regra R4 — Validade e limite de usos são dados obrigatórios

> Origem: RQ-05/06 · área A · perfil **completo** · técnica: **EP de presença e representação; criação ≠ edição**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Validade e limite de usos são dados obrigatórios

    Esquema do Cenário: [CT-08] Validade e limite obrigatórios no formulário
      Dado o administrador e um cupom ativo para edição, com todos os campos válidos exceto o campo visado
      Quando o administrador tenta <operacao> com campo <campo> contendo <entrada> pelo componente
      Então o erro pertence a <campo> e não há gravação parcial
      E o contador e a trilha permanecem iguais e não nasce cupom sem o campo
      Exemplos:
        | operacao | campo | entrada | particao |
        | criar | expira_em | ausente | ausência |
        | criar | expira_em | null | nulo |
        | editar | expira_em | "" | vazio |
        | criar | expira_em | "nao-e-data" | domínio temporal inválido |
        | editar | expira_em | [] | tipo errado |
        | criar | limite_de_usos | ausente | ausência |
        | criar | limite_de_usos | null | nulo |
        | editar | limite_de_usos | "" | vazio |
        | editar | limite_de_usos | [] | tipo errado |

    Esquema do Cenário: [CT-09] Obrigatoriedade sobrevive à gravação fora da UI
      Dado o administrador e dados restantes válidos, com registro ativo e trilha testemunha quando há edição
      Quando o administrador tenta <operacao> diretamente com apenas <campo> igual a <entrada>
      Então a gravação é recusada pelo campo visado
      E os dados do cupom, contador e linhas de uso não mudam
      Exemplos:
        | operacao | campo | entrada | particao |
        | criar | expira_em | null | nulo |
        | editar | expira_em | "nao-e-data" | domínio |
        | criar | limite_de_usos | null | nulo |
        | editar | limite_de_usos | [] | tipo errado |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-13 | Expiração exigida só no formulário | CT-09 | criar/expira_em/null não grava |
| M-14 | Limite omitido recebe valor ilimitado | CT-09 | criar/limite_de_usos/null recusa |
| M-15 | Edição transforma data inválida em data atual | CT-09 | editar/nao-e-data recusa e preserva timestamp |
| M-16 | Validação acusa campo errado e mascara o alvo | CT-08 | erro é do único campo inválido |

## Regra R5 — Código não se repete no mesmo contexto e pode repetir entre organizações

> Origem: RQ-14, P-04 · área A/B · perfil **completo** · técnica: **EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Código não se repete no mesmo contexto e pode repetir entre organizações

    Esquema do Cenário: [CT-10] A UI impede colisão literal no mesmo contexto
      Dado PROMO10 existente, não excluído, no estado <estado>, e OUTRO ativo no mesmo contexto, com administrador autorizado
      Quando o administrador tenta <operacao> com codigo PROMO10 pelo componente e os demais campos válidos
      Então há erro em codigo e continua existindo exatamente uma identidade PROMO10
      E PROMO10 e OUTRO conservam todos os campos, contadores e linhas de aplicação anteriores
      Exemplos:
        | operacao | estado | particao |
        | criar novo | ativo | identidade existente |
        | editar OUTRO | ativo | identidade existente |
        | criar novo | expirado | unicidade independe da validade |
        | editar OUTRO | expirado | unicidade independe da validade |
        | criar novo | esgotado | unicidade independe do saldo |
        | editar OUTRO | esgotado | unicidade independe do saldo |
        | criar novo | expirado e esgotado | identidade ainda existe |
        | editar OUTRO | expirado e esgotado | identidade ainda existe |

    Cenário: [CT-11] Editar sem mudar código não colide consigo mesmo
      Dado o administrador e cupom ativo PROMO10, já editado legitimamente de valor 10 para 11 com os demais campos preservados
      Quando o administrador repete o salvamento pelo componente com os mesmos cinco campos, inclusive codigo PROMO10 e valor 11
      Então a mesma identidade persiste com codigo PROMO10 e valor 11
      E continua existindo um cupom PROMO10, com contador e trilha anteriores intactos

    Esquema do Cenário: [CT-12] Unicidade não depende do formulário nem de tenant_id não nulo
      Dado PROMO10 no estado <estado>, criado legitimamente com os mesmos dados da intenção repetida, e OUTRO ativo no <modo>
      Quando o administrador tenta <operacao> diretamente para gravar outro PROMO10 no mesmo contexto
      Então a gravação é recusada e permanece uma única identidade PROMO10
      E PROMO10, OUTRO, contadores e linhas de uso mantêm seus valores anteriores
      Exemplos:
        | modo | operacao | estado | particao |
        | single-tenant, tenant_id null | criar | ativo | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | criar | expirado | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | criar | esgotado | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | criar | expirado e esgotado | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | editar OUTRO | ativo | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | editar OUTRO | expirado | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | editar OUTRO | esgotado | mesmo contexto, identidade não excluída |
        | single-tenant, tenant_id null | editar OUTRO | expirado e esgotado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | criar | ativo | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | criar | expirado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | criar | esgotado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | criar | expirado e esgotado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | editar OUTRO | ativo | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | editar OUTRO | expirado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | editar OUTRO | esgotado | mesmo contexto, identidade não excluída |
        | multi-tenant Acme | editar OUTRO | expirado e esgotado | mesmo contexto, identidade não excluída |

    Esquema do Cenário: [CT-13] Uma organização não reserva código para as demais
      Dado Acme e Globex, cada uma com administrador e com dados distintos, e PROMO10 ativo somente na Acme
      Quando o administrador da Globex <operacao> pela UI um cupom de código PROMO10
      Então a Globex grava PROMO10 com seus próprios tipo, valor, validade e limite
      E a Acme conserva sua identidade PROMO10 e nenhum contador ou uso é movido
      Exemplos:
        | operacao | particao |
        | cria | mesmo código, tenant diferente |
        | edita OUTRO para | colisão só no tenant alheio |

    Esquema do Cenário: [CT-57] Código livre disputado não gera duas identidades iguais
      Dado dois administradores do mesmo <modo>, código RACE livre e duas conexões/processos sobre o mesmo banco de teste compartilhado
      E na edição há dois cupons distintos ORIGINAL1 e ORIGINAL2 sem usos, e uma barreira confirma ambas as verificações de ausência antes de liberar as escritas reais
      Quando ambos tentam <operacao> simultaneamente para gravar codigo RACE, com os demais campos válidos
      Então somente uma chamada é aceita e uma única identidade RACE persiste após os commits, com <quantidade> cupons no conjunto disputado
      E o perdedor não grava cupom parcial nem altera seus campos originais, e nenhum contador ou registro de aplicação é criado ou movido
      Exemplos:
        | modo | operacao | quantidade | particao |
        | single-tenant com tenant_id null | criar | 1 | duas criações no contexto global |
        | multi-tenant Acme | criar | 1 | duas criações no mesmo tenant |
        | single-tenant com tenant_id null | editar seus respectivos originais | 2 | duas renomeações para código livre |
        | multi-tenant Acme | editar seus respectivos originais | 2 | duas renomeações no tenant |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-17 | Unique global consulta outra organização | CT-13 | Globex grava PROMO10 apesar do registro da Acme |
| M-18 | Unique de edição não ignora próprio registro | CT-11 | salvar PROMO10 com valor 11 funciona na mesma identidade |
| M-19 | Índice composto com NULL é a única barreira | CT-12 | single-tenant/create continua com uma identidade |
| M-20 | Unicidade só é checada no create | CT-10 | editar OUTRO para PROMO10 recusa |
| M-77 | Unicidade consulta somente cupons ativos | CT-10, CT-12 | Colisão com expirado/esgotado recusa na UI e fora dela — revisão adversarial ADV-02 |
| M-80 | Check de unicidade sem barreira atômica permite duas gravações do mesmo código | CT-57 | Só uma aceita e uma identidade RACE persiste, inclusive com tenant_id null — ADV2-01 |

## Regra R6 — Cadastro e edição operam pela tela do painel

> Origem: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, P-05, P-09 · área E/A · perfil **completo** · técnica: **Par visita × gravação; EP dos dois tipos; edição após uso**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cadastro e edição operam pela tela do painel

    Esquema do Cenário: [CT-14] A rota de criação oferece os cinco dados do cupom
      Dado o administrador autorizado no <modo>
      Quando o administrador visita a rota de criação de cupons do painel app
      Então o conteúdo inclui os campos de código, tipo, valor, validade e limite de usos
      E as opções de tipo correspondem a porcentagem e valor fixo
      Exemplos:
        | modo | particao |
        | single-tenant | /app/cupons/create |
        | multi-tenant Acme | /app/acme/cupons/create |

    Esquema do Cenário: [CT-15] O formulário cria um cupom completo com unidades corretas
      Dado o administrador autorizado e nenhum cupom NOVO no contexto corrente
      Quando o administrador cria pelo componente NOVO com <tipo>, valor <valor>, validade 2026-11-20T15:00:00Z e limite 3
      Então uma identidade NOVO persiste com exatamente esses cinco campos e organização corrente
      E o contador inicial é 0 e nenhuma linha de aplicação foi criada
      Exemplos:
        | tipo | valor | particao |
        | porcentagem | 29 | pontos percentuais inteiros |
        | fixo | 1234 | centavos |

    Cenário: [CT-16] A rota de edição apresenta os valores do registro correto
      Dado o administrador, um cupom ativo ALVO fixo de 1234 centavos e outro cupom TESTEMUNHA com 29%
      Quando o administrador visita a rota de edição pelo uuid de ALVO
      Então os campos do cupom ALVO exibem código, tipo fixo, valor 1234, sua validade e seu limite
      E os valores de TESTEMUNHA não aparecem como estado do formulário

    Esquema do Cenário: [CT-17] Editar grava todos os campos e mantém a identidade
      Dado o administrador e cupom ativo ORIGINAL com tipo <anterior>, 0 usos e sem aplicação anterior
      Quando o administrador salva pelo componente codigo EDITADO, tipo <novo>, valor <valor>, validade 2026-12-01T03:00:00Z e limite 4
      Então a mesma identidade persiste com os cinco novos campos e sem duplicar o registro
      E a organização, o contador 0 e a ausência de trilha permanecem iguais
      Exemplos:
        | anterior | novo | valor | particao |
        | porcentagem | fixo | 1234 | muda unidade para centavos |
        | fixo | porcentagem | 29 | muda unidade para pontos percentuais |

    Esquema do Cenário: [CT-20] Uma edição não reescreve consumo nem história
      Dado o administrador e cupom em <estado>, com <usos> usos reais e a mesma quantidade de linhas de aplicação
      Quando o administrador tenta salvar pelo componente somente <alteracao>
      Então o contador continua <usos> e as identidades, autores e instantes das linhas anteriores permanecem iguais
      E na partição ativa com uso prévio a edição é aceita e codigo RENOMEADO persiste na mesma identidade
      Exemplos:
        | estado | usos | alteracao | particao |
        | ativo com uso prévio | 1 | codigo para RENOMEADO | muda campo fora do estado inicial |
        | expirado com uso prévio | 1 | expira_em para futuro | Q3, sem afirmar reativação |
        | esgotado no limite 3 | 3 | limite_de_usos para 2 | Q4, sem afirmar aceitação |
        | expirado e esgotado | 3 | valor de 10 para 11 | Q3/Q4, preservação da história |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-21 | Create salva somente código e default nos demais campos | CT-15 | tipo/valor/data/limite exatos persistem |
| M-22 | Save de edição insere outro cupom | CT-17 | mesma identidade e contagem não aumenta |
| M-23 | Dados exibidos são de outro uuid | CT-16 | ALVO contém fixo/1234 e sua própria validade |
| M-24 | Troca do tipo não grava o novo valor | CT-17 | fixo→porcentagem grava 29, não 1234 |
| M-25 | Salvar formulário zera contador ou recria trilha | CT-20 | usos 3 e identidades de trilha anteriores permanecem |
| M-26 | Página abre sem opções/valor hidratado | CT-14 | cinco campos e as duas opções estão presentes |
| M-79 | Formulário recusa toda edição após primeiro uso | CT-20 | Ativo com uso prévio grava RENOMEADO na mesma identidade — revisão adversarial ADV-01; exceção ao teto |

## Regra R7 — Exclusão e identidade inexistente não deixam cupom utilizável

> Origem: RQ-01/07/09/13/15, P-01/P-08 · área A/D · perfil **completo** · técnica: **Estado × operação; exclusão real; CRUD combinado**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Exclusão e identidade inexistente não deixam cupom utilizável

    Esquema do Cenário: [CT-18] Administrador exclui cupom sem histórico de aplicação
      Dado o administrador e cupom <estado> SEMUSO, com contador 0 e sem linhas de uso, além de TESTEMUNHA ativo
      Quando o administrador confirma a ação de excluir SEMUSO no componente
      Então SEMUSO não é mais um cupom disponível para consulta ou listagem
      E TESTEMUNHA permanece com todos os campos e contador inalterados
      Exemplos:
        | estado | particao |
        | ativo | exclusão a partir de estado válido |
        | expirado com limite disponível | exclusão sem auditoria a reter |

    Esquema do Cenário: [CT-19] Identidade inexistente e exclusão repetida não alteram outros cupons
      Dado um administrador, ALVO antes existente e realmente excluído sem usos e TESTEMUNHA ativo intacto
      Quando o administrador tenta <operacao> usando a identidade removida ou inexistente <id>
      Então a operação é recusada por ausência do registro, sem criar, editar ou remover TESTEMUNHA
      E seus cinco campos, contador e trilha permanecem iguais e nenhum registro removido é recriado
      Exemplos:
        | operacao | id | particao |
        | ler edição | uuid nunca existente | identidade inexistente |
        | salvar edição | uuid de ALVO excluído | registro removido |
        | excluir | uuid de ALVO excluído | segunda exclusão |
        | excluir | uuid nunca existente | identidade inexistente |

    Esquema do Cenário: [CT-21] Snapshot de um cupom excluído não pode ser consumido
      Dado um administrador, um cupom antes ativo de <tipo> capturado em memória e depois excluído pela operação real, além de TESTEMUNHA existente
      Quando o administrador aplica esse snapshot ao total 10000
      Então nenhum total com desconto é entregue e o cupom removido não é recriado
      E não nasce linha de uso e o contador e a trilha de TESTEMUNHA não mudam
      Exemplos:
        | tipo | particao |
        | porcentagem | removido após leitura |
        | fixo | removido após leitura |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-27 | Excluir apenas some com linha da tabela, não com elegibilidade | CT-21 | snapshot removido não devolve desconto |
| M-28 | Ação sem whereKey remove todos os cupons | CT-18 | TESTEMUNHA permanece intacto |
| M-29 | Edição de identidade ausente faz upsert | CT-19 | save removido não recria ALVO |

## Regra R8 — Somente os administradores dados por P-02 podem criar

> Origem: RQ-07/08, P-02/P-09 · área B · perfil **completo** · técnica: **Matriz papel × criar; execução fora do componente e pela UI**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Somente os administradores dados por P-02 podem criar

    Esquema do Cenário: [CT-22] A criação direta respeita cada papel
      Dado o ator <papel> no contexto válido, com dados de cupom NOVO inteiramente válidos
      Quando o ator tenta criar NOVO pela via de domínio fora do Resource
      Então o resultado é <resultado> e a contagem de NOVO é <quantidade>
      E qualquer recusa não cria cupom, contador nem linha de aplicação
      Exemplos:
        | papel | resultado | quantidade | particao |
        | master_global | aceito | 1 | administrador global |
        | admin | aceito | 1 | P-02 afirma acesso |
        | admin_organizacao, multi-tenant | aceito | 1 | administrador da organização |
        | panel_user | recusado | 0 | usuário comum |
        | infra | recusado | 0 | outro perfil |
        | sem papel | recusado | 0 | sem autorização |

    Cenário: [CT-23] Forçar criação no componente não contorna autorização
      Dado um panel_user legítimo com acesso à lista e dados de NOVO inteiramente válidos
      Quando o usuário força a operação de criação do componente sem depender da visibilidade do botão
      Então a criação é recusada e nenhum cupom NOVO é persistido
      E não nasce contador nem registro de aplicação

    Esquema do Cenário: [CT-24] Administradores alcançam a criação e a lista permanece uma saída válida
      Dado um ator <papel> autenticado com contexto corrente e um cupom ativo TESTEMUNHA
      Quando o ator acessa a rota de criar cupom no painel app
      Então obtém <resultado> e a obrigação de conteúdo/saída é <observavel>
      E TESTEMUNHA permanece intacto, sem aplicações novas
      Exemplos:
        | papel | resultado | observavel | particao |
        | master_global | acesso | os cinco campos de cupom | administrador |
        | admin | acesso | os cinco campos de cupom | P-02, conflito do PRD |
        | admin_organizacao | acesso | os cinco campos de cupom | multi-tenant |
        | panel_user | recusa de autorização | saída CT-30 permanece alcançável | usuário comum |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-30 | Recorte por entidade retira também leitura do usuário comum | CT-24 | após recusa, CT-30 ainda lista TESTEMUNHA |
| M-31 | Permissão de criar é herdada por panel_user | CT-22 | panel_user gera 0 NOVO |
| M-32 | Apenas botão oculto protege a criação | CT-23 | chamada forçada recusa sem inserir |

## Regra R9 — Somente administradores podem editar, inclusive com papéis acumulados

> Origem: RQ-07/08, P-02 · área B · perfil **completo** · técnica: **Matriz papel × editar; pares de papéis; estado/campo discriminante**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Somente administradores podem editar, inclusive com papéis acumulados

    Esquema do Cenário: [CT-25] Edição direta exerce permissão e acúmulo de papéis
      Dado um ator com <papeis> e cupom ativo ALVO de 10%, com uso prévio e trilha real preservada
      Quando o ator tenta mudar diretamente o valor de ALVO para 11 sem passar pela UI
      Então a operação resulta em <resultado> e o valor persistido é <valor>
      E o código, validade, limite, contador e trilha permanecem iguais
      Exemplos:
        | papeis | resultado | valor | particao |
        | master_global | aceito | 11 | global |
        | admin | aceito | 11 | P-02 |
        | admin_organizacao | aceito | 11 | organização |
        | panel_user | recusado | 10 | comum |
        | infra | recusado | 10 | infra |
        | sem papel | recusado | 10 | ausência |
        | admin_organizacao + panel_user no mesmo tenant | aceito | 11 | acúmulo |
        | master_global + panel_user | aceito | 11 | acúmulo |
        | admin + panel_user | aceito | 11 | acúmulo |
        | master_global + admin | aceito | 11 | acúmulo |
        | master_global + admin_organizacao | aceito | 11 | acúmulo multi-tenant |
        | master_global + infra | aceito | 11 | acúmulo |
        | admin + admin_organizacao | aceito | 11 | acúmulo multi-tenant |
        | admin + infra | aceito | 11 | acúmulo |
        | admin_organizacao + infra | aceito | 11 | acúmulo multi-tenant |
        | panel_user + infra | recusado | 10 | dois papéis sem administração |

    Cenário: [CT-26] Edição forçada de usuário comum preserva o valor gravado
      Dado um panel_user e ALVO ativo de 10%, com 1 uso real, limite 3 e uma linha de trilha
      Quando o usuário força salvar o componente de edição com valor 11 e os outros campos válidos
      Então a escrita é recusada e ALVO continua com valor 10
      E todos os outros campos, contador 1 e a identidade/autoria/instante da trilha permanecem iguais

    Esquema do Cenário: [CT-56] Usuário comum não abre edição de cupom pelo endereço direto
      Dado um panel_user no seu contexto, cupom ALVO <estado> com cinco campos conhecidos e TESTEMUNHA ativo que o usuário pode listar
      Quando o usuário visita diretamente a rota de edição pelo uuid de ALVO
      Então o acesso é recusado por autorização ou ausência do recurso, sem expor os valores de ALVO como formulário de edição
      E ALVO mantém campos, contador e trilha anteriores; a lista própria continua alcançável pelo par CT-55
      Exemplos:
        | estado | particao |
        | ativo | apenas listar, não editar |
        | expirado com usos disponíveis | inativo |
        | esgotado válido no tempo | inativo |
        | expirado e esgotado | inativo |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-33 | Update é autorizado pela mesma regra de View | CT-25 | panel_user mantém valor 10 |
| M-34 | Autorizar apenas no mount permite save forjado | CT-26 | save forçado não grava 11 |
| M-35 | Papel comum acumulado sobrepõe papel administrador | CT-25 | admin_organizacao+panel_user grava 11 |
| M-78 | Mount permite ler formulário de edição embora save recuse | CT-56 | panel_user não recebe campos de ALVO em nenhum estado — revisão adversarial ADV-03 |

## Regra R10 — Somente administradores podem excluir

> Origem: RQ-07/08, P-02 · área B · perfil **completo** · técnica: **Matriz papel × excluir; verbo destrutivo independente**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Somente administradores podem excluir

    Esquema do Cenário: [CT-27] A exclusão direta verifica o próprio verbo
      Dado um ator <papel>, ALVO ativo sem uso prévio e outro cupom TESTEMUNHA
      Quando o ator tenta excluir ALVO diretamente fora da UI
      Então o resultado é <resultado> e ALVO fica <estado>
      E TESTEMUNHA permanece intacto e não é criada linha de aplicação
      Exemplos:
        | papel | resultado | estado | particao |
        | master_global | aceito | indisponível | global |
        | admin | aceito | indisponível | P-02 |
        | admin_organizacao | aceito | indisponível | organização |
        | panel_user | recusado | ativo com todos os campos originais | comum |
        | infra | recusado | ativo com todos os campos originais | infra |
        | sem papel | recusado | ativo com todos os campos originais | sem permissão |

    Cenário: [CT-28] Chamada forçada de excluir não depende do botão oculto
      Dado um panel_user e ALVO ativo sem uso, que seria removível por administrador
      Quando o usuário força a ação de excluir ALVO pelo componente
      Então a ação é recusada e ALVO permanece com os mesmos cinco campos e contador 0
      E não nasce nem é removida linha de uso

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-36 | Delete sem verificação, embora update seja protegido | CT-27 | panel_user não remove ALVO |
| M-37 | UI esconde botão mas handler executa | CT-28 | ALVO persiste após chamada forçada |
| M-38 | Papel admin_organizacao fica sem Delete apesar de Create/Update | CT-27 | admin_organizacao exclui ALVO sem uso |

## Regra R11 — Usuário comum lista somente cupons ativos

> Origem: RQ-08, P-03 · área B/E · perfil **completo** · técnica: **Tabela de decisão completa; EP de estado; cardinalidade e paginação**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Usuário comum lista somente cupons ativos

    Cenário: [CT-29] A listagem resolve todas as combinações de atividade
      Dado um panel_user, relógio congelado e cupons próprios A com validade agora+1 segundo, V com agora−1 segundo, B com validade exatamente agora, E esgotado válido, VE expirado/esgotado e X realmente excluído
      Quando o usuário carrega a listagem pelo componente
      Então os IDs listados contêm A e não contêm V, B, E, VE ou X
      E os contadores e linhas de aplicação de todos os cupons permanecem iguais; A, V e B têm usos disponíveis

    Cenário: [CT-30] Consulta da lista fora do componente aplica o mesmo recorte
      Dado um panel_user autenticado, relógio congelado e cupons próprios A com validade agora+1 segundo, V com agora−1 segundo, B com validade exatamente agora, E esgotado e VE expirado/esgotado
      Quando o usuário executa a consulta de listagem pública usada pelo painel, fora do componente
      Então a coleção contém exatamente A, excluindo V, B, E e VE, e essa lista própria permanece alcançável após recusas de escrita
      E nenhum contador ou registro de aplicação é alterado; A, V e B têm usos disponíveis

    Esquema do Cenário: [CT-31] Paginar não perde os ativos de um conjunto estável
      Dado um panel_user e <n> cupons ativos únicos no seu contexto, além de expirados e de outra organização
      Quando o usuário percorre as páginas da listagem com tamanho efetivo p sem inserções entre elas
      Então a união dos IDs listados é exatamente o conjunto dos <n> ativos autorizados, sem duplicação
      E nenhum expirado, esgotado ou cupom alheio aparece em qualquer página
      Exemplos:
        | n | particao |
        | 0 | lista vazia |
        | 1 | um registro |
        | p | borda da página |
        | p+1 | além da página |

    Esquema do Cenário: [CT-55] Recusa no painel tem saída para uma lista alcançável
      Dado o ator legítimo no próprio contexto, TESTEMUNHA ativo e recusa anterior <origem> produzida pela operação real
      Quando o ator visita a listagem de cupons do seu próprio painel
      Então a rota responde com a lista contendo TESTEMUNHA e os dados próprios do cupom, sem repetir a recusa nem entrar em ciclo de redirects
      E contador e trilha de TESTEMUNHA não mudam
      Exemplos:
        | origem | ator | particao |
        | criar sem permissão | panel_user | saída do 403 |
        | editar sem permissão | panel_user | saída do 403 |
        | excluir sem permissão | panel_user | saída da recusa de ação |
        | editar uuid inexistente | administrador | saída do 404 |
        | editar uuid da Globex pela Acme | administrador Acme | saída da fronteira de tenant |

    Esquema do Cenário: [CT-58] Nenhum perfil não administrador recebe inativos pela consulta direta
      Dado ator <papel> autenticado no próprio contexto, A ativo e cupons próprios V expirado, B com validade exatamente agora, E esgotado e VE expirado/esgotado
      Quando o ator chama diretamente a consulta pública de listagem usada pelo painel
      Então nenhum ID, código ou atributo de V, B, E ou VE é divulgado, seja a resposta uma lista autorizada ou uma recusa de acesso sem esses dados
      E todos os contadores e linhas de aplicação permanecem iguais, sem concluir a decisão aberta Q11 sobre acesso à tela
      Exemplos:
        | papel | particao |
        | panel_user | usuário comum explicitamente autorizado a listar ativos |
        | infra | perfil autenticado não administrador |
        | sem papel | pessoa autenticada sem papel |
        | panel_user + infra | dois papéis sem administração |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-39 | Ativo usa validade OU limite disponível | CT-29 | V e E não aparecem |
| M-40 | Escopo só na primeira página | CT-31 | p+1 não inclui expirado ou alheio em página posterior |
| M-41 | Recorte vive apenas na UI | CT-30 | consulta fora do componente devolve exatamente A |
| M-42 | A recusa redireciona para rota que devolve à mesma recusa | CT-55 | lista própria alcança TESTEMUNHA sem ciclo |
| M-81 | Listagem aceita expira_em igual a agora embora o consumo recuse | CT-29, CT-30 | B com usos disponíveis não aparece na UI nem na consulta direta — ADV2-02 |
| M-82 | Filtra ativos só para panel_user e revela inativos a infra ou pessoa sem papel | CT-58 | Nenhum ID/código/atributo de V/B/E/VE é divulgado — ADV2-03 |

## Regra R12 — Toda operação mantém a fronteira da organização

> Origem: RQ-01, RQ-07, RQ-08, RQ-12, RQ-13, RQ-14, RQ-15, P-02, P-04, P-08 · área B · perfil **completo** · técnica: **IDOR; mass assignment; contexto nulo; troca de tenant**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Toda operação mantém a fronteira da organização

    Esquema do Cenário: [CT-32] Snapshot estrangeiro não pode ser aplicado no contexto errado
      Dado Ana administradora só da Acme, Bruno da Globex e um cupom ativo da Globex capturado antes da troca para Acme
      Quando Ana tenta <operacao> fora da UI na Acme usando o cupom da Globex
      Então nenhum total descontado é entregue nem cupom estrangeiro é obtido como elegível
      E contador, cinco campos e trilha da Globex e da Acme permanecem iguais
      Exemplos:
        | operacao | particao |
        | localizar pelo código exclusivo da Globex | busca de identidade estrangeira |
        | aplicar snapshot da Globex ao total 10000 | instância já resolvida, sem consulta protetora da UI |

    Esquema do Cenário: [CT-33] Editar e excluir por uuid alheio não atravessam o tenant
      Dado Ana administradora da Acme, Bruno da Globex e cupom ALHEIO ativo da Globex com 10%, além de PROPRIO na Acme
      Quando Ana tenta <operacao> usando uuid de ALHEIO no painel da Acme
      Então a operação é recusada por ausência ou autorização sem expor valores de ALHEIO
      E ALHEIO mantém valor 10 e todos os campos, contador e trilha; PROPRIO não é alterado
      Exemplos:
        | operacao | particao |
        | abrir edição | route binding |
        | salvar edição com valor 11 | escrita |
        | excluir pelo componente | ação destrutiva |

    Esquema do Cenário: [CT-34] Tenant ausente não abre o escopo em modo multi-tenant
      Dado tenancy ligada, um operador de Acme, cupons da Acme e Globex e um registro legado com tenant nulo
      Quando o operador tenta <operacao> com tenant corrente ausente
      Então nenhum cupom é listado, encontrado ou aplicado como pertencente ao operador
      E nenhum contador nem registro de uso de qualquer contexto, inclusive o legado global, é alterado
      Exemplos:
        | operacao | particao |
        | consultar lista pública | discriminante nulo na leitura |
        | localizar código | discriminante nulo no lookup |
        | aplicar snapshot previamente lido | discriminante nulo na escrita |

    Esquema do Cenário: [CT-35] Campos de posse e consumo não são aceitos do payload
      Dado Ana administradora da Acme, Globex existente e ALVO ativo da Acme com 1 uso real e trilha correspondente
      Quando Ana tenta <operacao> diretamente com payload contendo apenas o campo protegido <campo> forjado
      Então <observavel>
      E os registros da Globex e a trilha anterior não mudam, e não nasce linha de aplicação
      Exemplos:
        | operacao | campo | observavel | particao |
        | criar cupom NOVO | tenant_id=Globex | NOVO não pertence à Globex; se criado pertence à Acme | posse |
        | editar ALVO | tenant_id=Globex | ALVO continua na Acme com todos os cinco campos originais | posse |
        | criar cupom NOVO | usos=99 | se criado NOVO tem usos 0 | contador |
        | editar ALVO | usos=0 | ALVO continua com usos 1 | contador |

    Esquema do Cenário: [CT-36] Código igual em duas organizações aplica só o cupom corrente
      Dado Carla com admin_organizacao na Acme e panel_user na Globex, e PROMO10 em ambas com <valor_acme> e <valor_globex>
      Quando Carla aplica na Acme o PROMO10 corrente ao total 10000
      Então o total é <total> e somente o contador da Acme aumenta em 1
      E nasce uma linha de uso ligada ao cupom da Acme com Carla e instante corrente, sem mudar contador ou trilha da Globex
      Exemplos:
        | tipo | valor_acme | valor_globex | total | particao |
        | porcentagem | 10 | 20 | 9000 | código homônimo |
        | fixo | 1234 | 2345 | 8766 | código homônimo |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-43 | Consulta por código esquece tenant | CT-36 | retorna 9000/8766, não desconto da Globex |
| M-44 | Instância já resolvida ignora tenant no consumo | CT-32 | snapshot estrangeiro não entrega desconto |
| M-45 | Tenant nulo remove scope ou inclui globais | CT-34 | lista vazia e nenhum consumo inclusive do legado nulo |
| M-46 | Payload altera tenant ou zera contador | CT-35 | Acme continua dona e usos 1 persiste |
| M-47 | Leitura/gravação direta de CupomUso aceita cupom_id estrangeiro | ⚠️ **sem matador** — Q9 / superfície ausente | — (lacuna declarada: 02 ausente e fronteira de CupomUso não definida, Q9) |
| M-48 | Escopo protege só a lista, deixando binding e ações por uuid abertos | CT-33 | editar/excluir ALHEIO recusa e Globex mantém valor 10 |

## Regra R13 — A aplicação depende de existência, validade e disponibilidade juntas

> Origem: RQ-09, RQ-10, RQ-11, RQ-12, RQ-13, P-01, P-03 · área D · perfil **completo** · técnica: **EP de existência; tabela de decisão completa com restrições**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: A aplicação depende de existência, validade e disponibilidade juntas

    Esquema do Cenário: [CT-37] O localizador só oferece cupom existente e ativo
      Dado administrador, TESTEMUNHA ativo e cupom ALVO existente com <tempo> e <usos> usos de limite 3
      Quando o administrador consulta a elegibilidade do código <codigo>
      Então a identidade oferecida é <elegivel>, sem entregar total descontado por uma consulta
      E contadores e trilhas de ALVO e TESTEMUNHA permanecem exatamente iguais
      Exemplos:
        | codigo | tempo | usos | elegivel | particao |
        | INEXISTENTE | futuro | 2 | nenhuma | código não existente |
        | null | futuro | 2 | nenhuma | ausência |
        | "" | futuro | 2 | nenhuma | vazio |
        | ALVO | futuro | 2 | ALVO | existente e ativo |
        | ALVO | passado | 2 | nenhuma | expirado com saldo |
        | ALVO | futuro | 3 | nenhuma | esgotado válido no tempo |
        | ALVO | passado | 3 | nenhuma | expirado e esgotado |

    Esquema do Cenário: [CT-38] Cada condição de elegibilidade pode impedir o consumo
      Dado um administrador e cupom existente de <tipo>, valor <valor>, com <tempo> e <usos> usos de limite 3
      Quando o administrador tenta aplicar esse cupom ao total 10000
      Então o resultado é <resultado>, o total entregue é <total> e o contador persistido é <contador>
      E a variação de linhas de aplicação é <linhas>, preservando todas as linhas anteriores
      Exemplos:
        | tipo | valor | tempo | usos | resultado | total | contador | linhas | particao |
        | porcentagem | 10 | futuro | 2 | aceito | 9000 | 3 | +1 | todas verdadeiras |
        | porcentagem | 10 | passado | 2 | recusado | nenhum | 2 | 0 | só tempo inválido |
        | porcentagem | 10 | futuro | 3 | recusado | nenhum | 3 | 0 | só limite inválido |
        | porcentagem | 10 | passado | 3 | recusado | nenhum | 3 | 0 | ambas inválidas, célula da decisão |
        | fixo | 1234 | futuro | 2 | aceito | 8766 | 3 | +1 | todas verdadeiras |
        | fixo | 1234 | passado | 2 | recusado | nenhum | 2 | 0 | só tempo inválido |
        | fixo | 1234 | futuro | 3 | recusado | nenhum | 3 | 0 | só limite inválido |
        | fixo | 1234 | passado | 3 | recusado | nenhum | 3 | 0 | ambas inválidas, célula da decisão |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-49 | Código não encontrado cai no primeiro cupom | CT-37 | INEXISTENTE não oferece TESTEMUNHA |
| M-50 | Atividade usa OR entre tempo e disponibilidade | CT-38 | passado/2 e futuro/3 recusam ambos |
| M-51 | Consumo ocorre antes da decisão de elegibilidade | CT-38 | recusado mantém contador 2 ou 3 e delta de trilha 0 |
| M-83 | Localizador confere existência mas oferece expirado ou esgotado | CT-37 | ALVO com passado/2, futuro/3 e passado/3 não é oferecido; consultar não empresta prova de aplicar |

## Regra R14 — Validade termina no instante gravado, inclusive após leitura anterior

> Origem: RQ-05/10, pergunta final de validade do 00 · área D · perfil **completo** · técnica: **BVA 3-valores de segundo; tempo de uso; fuso e DST**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Validade termina no instante gravado, inclusive após leitura anterior

    Esquema do Cenário: [CT-39] A borda temporal é estrita no lookup e no consumo
      Dado um administrador, cupom existente de cada tipo com limite disponível e validade em 2026-10-21T03:00:00Z
      Quando o administrador <operacao> no instante <agora>
      Então a elegibilidade é <resultado>, com total <total_percentual> para 10% ou <total_fixo> para 1234 centavos sobre 10000
      E o delta do contador e da trilha é <delta>, sem mudar linhas anteriores
      Exemplos:
        | operacao | agora | resultado | total_percentual | total_fixo | delta | particao |
        | localiza | 2026-10-21T02:59:59Z | elegível | não aplicado | não aplicado | 0 | borda−1 segundo |
        | localiza | 2026-10-21T03:00:00Z | inelegível | nenhum | nenhum | 0 | borda |
        | localiza | 2026-10-21T03:00:01Z | inelegível | nenhum | nenhum | 0 | borda+1 segundo |
        | aplica snapshot | 2026-10-21T02:59:59Z | aceito | 9000 | 8766 | +1 | borda−1 segundo |
        | aplica snapshot | 2026-10-21T03:00:00Z | recusado | nenhum | nenhum | 0 | borda |
        | aplica snapshot | 2026-10-21T03:00:01Z | recusado | nenhum | nenhum | 0 | borda+1 segundo |

    Esquema do Cenário: [CT-40] Leitura antes da expiração não autoriza consumo depois dela
      Dado um administrador e snapshot de cupom <tipo> validado um segundo antes da validade, com contador 1 e trilha real
      Quando o administrador aplica o snapshot exatamente no instante de validade ao total 10000
      Então a aplicação é recusada e nenhum valor descontado é entregue
      E o contador permanece 1 e nenhuma linha de uso é criada, alterada ou removida
      Exemplos:
        | tipo | particao |
        | porcentagem | expira entre localizar e aplicar |
        | fixo | expira entre localizar e aplicar |

    Esquema do Cenário: [CT-41] O mesmo instante absoluto não muda de validade conforme o fuso
      Dado o administrador, cupom existente de cada tipo, validade absoluta <expira>, usos 0 de limite 3 e app em <fuso> com banco em UTC
      Quando o administrador aplica o cupom no instante absoluto <agora>
      Então o resultado é <resultado>, com 9000 para 10% ou 8766 para fixo 1234 no sucesso
      E só o sucesso incrementa para 1 e cria uma linha no instante absoluto de agora, enquanto recusa preserva contador 0 e trilha vazia
      Exemplos:
        | fuso | expira | agora | resultado | particao |
        | America/Sao_Paulo | 2026-10-21T03:00:00Z | 2026-10-21T02:59:59Z | aceito | 23:59:59 local, janela de divergência UTC |
        | America/Sao_Paulo | 2026-10-21T03:00:00Z | 2026-10-21T03:00:00Z | recusado | meia-noite local, igualdade |
        | America/Sao_Paulo | 2026-10-21T03:00:00Z | 2026-10-21T03:00:01Z | recusado | depois da borda |
        | America/New_York | 2026-11-01T06:30:00Z | 2026-11-01T05:30:00Z | aceito | 01:30 EDT, hora repetida antes do fim |
        | America/New_York | 2026-11-01T06:30:00Z | 2026-11-01T06:30:00Z | recusado | 01:30 EST, mesmo relógio local e outro instante |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-52 | Compara validade por >= em vez de > | CT-39 | igualdade recusa no lookup e no consumo |
| M-53 | Só localizador verifica validade | CT-40 | snapshot validado antes recusa na igualdade |
| M-54 | Compara apenas data, encerrando no começo do dia | CT-39 | segundo anterior à meia-noite local ainda aplica |
| M-55 | Compara strings locais com relógio UTC sem conversão | CT-41 | 02:59:59Z equivale a 23:59:59 local e ainda aceita |
| M-56 | Hora local repetida perde offset no DST | CT-41 | 05:30Z aceita e 06:30Z recusa apesar de ambas serem 01:30 local |

## Regra R15 — Limite global não é ultrapassado por snapshot nem corrida

> Origem: RQ-06/11/13, P-01 · área D · perfil **completo** · técnica: **BVA 3-valores; concorrência real; snapshots distintos**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Limite global não é ultrapassado por snapshot nem corrida

    Esquema do Cenário: [CT-42] O último uso disponível é aceito e o próximo é recusado
      Dado um administrador e cupom de cada tipo válido no tempo, limite 3 e <antes> usos persistidos
      Quando o administrador aplica o cupom ao total 10000
      Então o resultado é <resultado>, o contador fica <depois> e a variação de linhas de uso é <linhas>
      E só no sucesso recebe 9000 para 10% ou 8766 para fixo 1234, preservando toda trilha anterior
      Exemplos:
        | antes | resultado | depois | linhas | particao |
        | 2 | aceito | 3 | +1 | limite−1 |
        | 3 | recusado | 3 | 0 | limite |
        | 4 | recusado | 4 | 0 | limite+1, legado inválido isolado |

    Esquema do Cenário: [CT-43] Duas leituras antigas não dão dois últimos usos
      Dado dois snapshots distintos de cupom <tipo> válido com contador 2 de limite 3, e primeiro uso real feito por outro administrador após as leituras
      Quando o segundo administrador aplica o snapshot antigo ao total 10000
      Então a segunda aplicação é recusada, sem total descontado
      E o contador persistido permanece 3 e existe somente a linha criada pelo primeiro consumo, além da trilha anterior
      Exemplos:
        | tipo | particao |
        | porcentagem | snapshot com usos defasados |
        | fixo | snapshot com usos defasados |

    Esquema do Cenário: [CT-44] Dois consumidores simultâneos disputam um único saldo
      Dado cupom <tipo> válido com 2 usos de limite 3, dois administradores distintos e duas conexões/processos sobre o mesmo banco descartável
      E ambos têm leitura elegível anterior e uma barreira libera as duas primeiras escritas de consumo depois dessas leituras
      Quando os dois administradores aplicam simultaneamente esse cupom ao total 10000
      Então exatamente uma chamada entrega <total> e a outra recusa sem valor descontado
      E após ambos terminarem, nova conexão lê contador 3 e exatamente uma linha nova de uso com o autor vencedor
      Exemplos:
        | tipo | total | particao |
        | porcentagem | 9000 | concorrência percentual |
        | fixo | 8766 | concorrência fixa |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-57 | Condição usos <= limite concede um uso extra | CT-42 | antes 3 recusa e continua 3 |
| M-58 | Atualização usa contador do snapshot | CT-43 | segundo snapshot não obtém desconto e contador permanece 3 |
| M-59 | Check-then-act sem condição atômica na escrita | CT-44 | somente uma resposta aceita e uma linha nova após commits |
| M-60 | Atualização é atômica, mas sucesso é devolvido a perdedor | CT-44 | uma chamada obrigatoriamente recusa, não bastando contador 3 |

## Regra R16 — Desconto usa inteiros, trunca porcentagem e limita o total em zero

> Origem: RQ-12, P-01/P-05/P-06/P-07 · área C · perfil **completo** · técnica: **EP dos tipos; BVA monetária de centavo; exemplos discriminantes**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Desconto usa inteiros, trunca porcentagem e limita o total em zero

    Esquema do Cenário: [CT-45] Percentual inteiro trunca a fração do desconto
      Dado um administrador e cupom percentual válido com <percentual> pontos inteiros e uso disponível
      Quando o administrador aplica o cupom ao total <original> em centavos
      Então o total devolvido é exatamente <final> inteiro em centavos
      E há um uso consumido e uma única aplicação com o administrador e o instante corrente
      Exemplos:
        | percentual | original | final | particao |
        | 29 | 100 | 71 | float 0.29 pode perder um centavo |
        | 10 | 9999 | 9000 | resto 9, truncar desconto 999 |
        | 5 | 50 | 48 | metade do centavo, não arredondar para 3 |
        | 1 | 99 | 99 | desconto abaixo de um centavo |
        | 100 | 9999 | 0 | teto percentual literal 100 |

    Esquema do Cenário: [CT-46] Valor fixo é centavos e não produz total negativo
      Dado um administrador e cupom fixo válido de <fixo> centavos com uso disponível
      Quando o administrador aplica o cupom ao total <original> em centavos
      Então devolve exatamente <final> inteiro em centavos
      E há exatamente um uso consumido e uma aplicação com autor e instante correntes, inclusive quando o total final é zero
      Exemplos:
        | fixo | original | final | particao |
        | 1000 | 999 | 0 | desconto−1 centavo |
        | 1000 | 1000 | 0 | desconto exato |
        | 1000 | 1001 | 1 | desconto+1 centavo |
        | 1234 | 10000 | 8766 | centavos, não reais |
        | 5000 | 3000 | 0 | piso zero de P-07 |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | Porcentagem calculada via float e cast antes de subtrair | CT-45 | 29% de 100 devolve 71, não 72 |
| M-62 | Arredonda desconto em vez de truncar | CT-45 | 5% de 50 devolve 48, não 47 |
| M-63 | Trunca total final, em vez do desconto | CT-45 | 10% de 9999 devolve 9000, não 8999 |
| M-64 | Valor fixo tratado como reais e multiplicado por 100 | CT-46 | fixo 1234 sobre 10000 devolve 8766 |
| M-65 | Resultado negativo quando fixo excede total | CT-46 | 5000 sobre 3000 devolve 0 |
| M-66 | Contador só é movido se total final for positivo | CT-46 | total zero ainda consome exatamente um uso |

## Regra R17 — Cada aplicação aceita consome um uso e somente o seu cupom

> Origem: RQ-11/13, P-01/P-05 · área D · perfil **completo** · técnica: **Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cada aplicação aceita consome um uso e somente o seu cupom

    Esquema do Cenário: [CT-47] Consumo não altera outro cupom do mesmo tenant
      Dado o administrador e dois cupons ativos no mesmo contexto, ALVO com 1 uso e TESTEMUNHA com 2, ambos com limite 5
      Quando o administrador aplica ALVO de <tipo> ao total 10000
      Então ALVO passa a 2 usos com total <total>, e TESTEMUNHA permanece com 2
      E nasce só uma linha de aplicação ligada a ALVO, sem qualquer mudança da trilha de TESTEMUNHA
      Exemplos:
        | tipo | total | particao |
        | porcentagem | 9000 | valor 10 |
        | fixo | 8766 | valor 1234 |

    Esquema do Cenário: [CT-48] Um sucesso move o contador exatamente uma vez
      Dado o administrador e cupom ativo de <tipo> com 1 uso de limite 3 e uma linha anterior de aplicação
      Quando o administrador aplica o cupom ao total 10000
      Então o total devolvido é <total> e uma nova leitura do banco encontra usos 2
      E existem exatamente duas linhas de aplicação, preservando intacta a anterior
      Exemplos:
        | tipo | total | particao |
        | porcentagem | 9000 | efeito no percentual 10 |
        | fixo | 8766 | efeito no fixo 1234 |

    Esquema do Cenário: [CT-49] Recusa não consome nem apaga aplicação anterior
      Dado o administrador real e cupom <tipo> <estado>, com <usos> usos reais e suas linhas de aplicação
      Quando o administrador tenta aplicar esse cupom ao total 10000
      Então nenhum total com desconto é entregue e o contador continua <usos>
      E nenhuma linha de aplicação é criada, removida ou alterada
      Exemplos:
        | tipo | estado | usos | particao |
        | porcentagem | expirado com limite 3 | 1 | não-efeito no percentual |
        | fixo | expirado com limite 3 | 1 | não-efeito no fixo |
        | porcentagem | esgotado no limite 3 | 3 | recusa de limite |
        | fixo | esgotado no limite 3 | 3 | recusa de limite |

    Esquema do Cenário: [CT-50] Usos válidos repetidos pelo mesmo autor contam no limite global
      Dado o administrador e cupom ativo <tipo> com limite 3, já aplicado legitimamente uma vez por esse mesmo autor
      Quando o administrador faz uma segunda aplicação independente do cupom ao total 10000
      Então recebe <total> e nova leitura encontra contador 2
      E existem duas aplicações distintas com o mesmo autor, preservando a primeira
      Exemplos:
        | tipo | total | particao |
        | porcentagem | 9000 | sem limite de uma vez por pessoa |
        | fixo | 8766 | sem limite de uma vez por pessoa |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-67 | Incrementa em 2 no sucesso | CT-48 | contador 1 passa a 2, não 3 |
| M-68 | UPDATE sem chave afeta todos os cupons do tenant | CT-47 | TESTEMUNHA permanece com 2 |
| M-69 | Contador é incrementado antes de recusar | CT-49 | expirado mantém 1 e esgotado mantém 3 |
| M-70 | Deduplica usos pelo autor, criando limite individual | CT-50 | mesmo autor obtém segundo desconto e contador 2 |

## Regra R18 — Cada uso aceito registra autor e instante com consumo e trilha consistentes

> Origem: RQ-13/15, P-01/P-08 · área D · perfil **completo** · técnica: **Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito**.

```gherkin
# language: pt
Funcionalidade: Cupons de desconto

  Regra: Cada uso aceito registra autor e instante com consumo e trilha consistentes

    Esquema do Cenário: [CT-51] A trilha identifica autor passado ao contrato e instante da aplicação
      Dado Ana e Bruno administradores distintos, sessão autenticada como Ana e cupom ativo <tipo> com uma aplicação anterior legítima de Ana em 2026-10-20T14:00:00Z
      Quando o chamador aplica o cupom por Bruno conforme P-01 em 2026-10-20T15:00:00Z ao total 10000
      Então uma única linha nova da trilha persistida identifica esse cupom, Bruno e 2026-10-20T15:00:00Z
      E o contador passa de 1 a 2 e a linha anterior de Ana conserva identidade, autor e instante
      Exemplos:
        | tipo | particao |
        | porcentagem | autoria do argumento, não sessão |
        | fixo | autoria do argumento, não sessão |

    Esquema do Cenário: [CT-52] Contrato sem autor não cria uso anônimo
      Dado Ana autenticada, um cupom <tipo> ativo, contador 1 e sua linha de aplicação real anterior
      Quando o chamador tenta aplicar ao total 10000 com <autor>
      Então a chamada é recusada sem entregar total com desconto
      E contador 1, cupom e linha anterior permanecem iguais, sem aplicação nova anônima ou atribuída por fallback
      Exemplos:
        | tipo | autor | particao |
        | porcentagem | argumento omitido | ausência, contrato P-01 |
        | fixo | argumento omitido | ausência, contrato P-01 |
        | porcentagem | null | tipo/autor inválido |
        | fixo | null | tipo/autor inválido |

    Esquema do Cenário: [CT-53] Falha ao registrar aplicação desfaz consumo já iniciado
      Dado administrador real, cupom <tipo> ativo, contador 1, uma aplicação anterior real e falha injetada na inserção da trilha depois da escrita de consumo
      Quando o administrador aplica ao total 10000
      Então a chamada falha sem devolver total com desconto e uma conexão nova lê contador 1
      E nenhuma linha nova de uso persiste, mantendo íntegra a linha anterior e os cinco campos do cupom
      Exemplos:
        | tipo | particao |
        | porcentagem | rollback após contador |
        | fixo | rollback após contador |

    Esquema do Cenário: [CT-54] Falha após inserir a trilha desfaz ambos os efeitos
      Dado administrador real, cupom <tipo> ativo, contador 1 e trilha anterior real, com falha injetada após a inserção da nova linha e antes do commit
      Quando o administrador aplica ao total 10000
      Então a chamada falha sem entregar desconto e a leitura após o rollback encontra contador 1
      E somente a linha anterior permanece com identidade, autor e instante originais
      Exemplos:
        | tipo | particao |
        | porcentagem | rollback após trilha |
        | fixo | rollback após trilha |

```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-71 | Autoria vem da sessão e ignora argumento obrigatório | CT-51 | nova linha identifica Bruno, não Ana |
| M-72 | Instante usa criação do cupom ou cópia da trilha anterior | CT-51 | linha nova é 15:00Z e anterior continua 14:00Z |
| M-73 | Uso é gravado só pela auditoria genérica que não registra consumo | CT-51 | linha de uso existe com cupom/Bruno/15:00Z |
| M-74 | Fixo não grava trilha embora percentual grave | CT-51 | linha fixo tem mesmo autor e instante corretos |
| M-75 | Autor omitido vira null ou usuário da sessão | CT-52 | ausência/null recusa e não consome |
| M-76 | Contador e trilha ficam em commits separados | CT-53 | falha posterior ao consumo devolve contador a 1; CT-54 também desfaz trilha |


## Checklist de Taxonomia — passo 4 inteiro

| Gatilho/item | Cenário ou lacuna declarada | Grupo |
|---|---|---|
| IDOR / ação com identidade de cupom | CT-32, CT-33, CT-19; atores e organizações distintos | G1, G2 |
| Autorização executada em cada verbo | CT-22/23 criar, CT-25/26 editar, CT-27/28 excluir; chamadas diretas e forçadas | G1, G2 |
| Idempotência de criar | CT-12: criação real anterior e repetição do código no mesmo contexto não duplicam identidade; não inventar chave de pedido | G1 |
| Idempotência de editar | CT-11: primeira edição concluída no Dado, mesmo salvamento repetido preserva identidade, valor e efeitos | G2 |
| Idempotência de excluir | CT-19: exclusão real anterior, segunda intenção não remove outro registro nem recria o removido | G2 |
| Idempotência de aplicar, ancorada no agregado | lacuna declarada: P-01 retira Pedido persistido; foi tentado formular pelo retorno/contador, mas isso mede consumo e não idempotência do mesmo pedido. Não escrever cenário tautológico; Q6 | G1 |
| Domínio condicionado tipo × valor | CT-05/06/07/45/46; nenhum teto percentual imposto ao fixo | G1, G2 |
| Fronteiras na gravação, por campo e entrada | CT-01/02 código-presença; CT-03/04 tipo; CT-05/06 valor; CT-08/09 validade e limite. Lacuna: teto textual Q1, fixo/total Q2, validade de cadastro Q3 e limite Q4. Recusa no uso não fecha cadastro | G1, G2 |
| Concorrência de saldo/limite e identidade | CT-44 consumo; CT-57 criação/renomeação única nos dois modos; conexões e barreiras reais. CT-43 só prova snapshot antigo | G4 |
| Efeito com destinatários 0/1/N | CT-51/52: autor obrigatório (0 recusado), um autor por aplicação, histórico de N autores distintos. Não é fan-out de notificação | G1 |
| Ausente ≠ null ≠ vazio | CT-01/02/04/06/08/09/37/52; semântica de presença explicitada por campo. Campos comerciais não são opcionais por conveniência do PRD | G1, G2 |
| Paginação 0/1/p/p+1 | CT-31; p é tamanho efetivo do componente | G2 |
| Inserção entre páginas | lacuna declarada: Q10; sem contrato de snapshot/ordenação, foi separado o conjunto estável do concorrente, sem prometer estabilidade inexistente | G2 |
| Ordenação: coluna inexistente/tipo errado | lacuna declarada: 02 ausente, nenhum consumo de tableSortColumn inventariado; revisar enum/lista fechada após inventário | G2 |
| Ordenação: nullable e empate | lacuna declarada: 00 não determina colunas de ordenação/desempate; Q10. Não emprestar CT-31 como teste de estabilidade | G2 |
| Data/hora: timezone, meia-noite e DST | CT-39/40/41; se driver impedir demonstrar a divergência, a materialização registra tentativa, sem selo de cobertura executada | G1 |
| Texto: acento, emoji, teto, espaços e normalização | lacuna declarada: Q1; 40/trim/uppercase são só do PRD. Ausência/null/vazio já têm CT-01/02; a lacuna não suspende unicidade literal | G1, G2 |
| Unicidade + SoftDeletes | lacuna declarada: mecanismo de exclusão não confirmado no 02; CT-18/21 exercitam remoção real, mas recriar código após exclusão depende da política de retenção Q5/Q1 | G1, G2 |
| Removido/desativado ainda funciona | CT-21 aplica snapshot removido; CT-38/40/42 aplicam expirado/esgotado. Não afirmar que exclusão física dispensa barreira | G1 |
| CRUD: ler/editar/excluir ID inexistente, excluir duas vezes, editar sem mudar | CT-19, CT-11 | G2 |
| Mass assignment por tabela — cupons | CT-35 tenant_id e usos, criar e editar; um campo protegido por linha | G1 |
| Mass assignment por tabela — cupom_usos | lacuna declarada: superfície independente/allowlist não fornecida, Q9; CT-35 do pai não é matador desta tabela | G1 |
| IDOR por tabela — cupons | CT-32/33; consumo direto e ações por uuid | G1, G2 |
| IDOR por tabela — cupom_usos | lacuna declarada: faltam pontos de leitura/escrita do 02; Q9. CT-36/51 provam vínculo da trilha criada, não impedem consulta arbitrária da tabela filha | G1 |
| Upload | não se aplica ao requisito: não há arquivo/campo de upload no 00 nem na superfície de UI admitida. Isso não é prova de que o vendor não tenha upload; inventário de superfícies continua pendente | — |
| Precisão monetária | CT-45/46, inteiro em centavos, 29% de 100, metade de centavo e piso zero | G1 |
| Superfície Livewire: linha a linha, domínio e tipo errado | lacuna declarada: 02 ausente. CT-03/08 têm entradas fora do domínio/tipo errado em campos conhecidos, mas não representam inventário completo de métodos/propriedades do cliente | G2 |
| Estado público do framework: índice, parse, coluna, operador | lacuna declarada: 02 ausente; não presumir validação de filters/pageFilters/tableFilters/tableSearch/tableSortColumn | G2 |
| Método público chamável por wire | lacuna declarada: 02 ausente; não inventar lista de ações nem afirmar que o retorno não vaza | G2 |
| Discriminante de escopo nulo | CT-34 com Acme, Globex e legado nulo reais; sem tenant não se torna acesso global | G1 |
| Saída de erro 4xx/redirect | CT-55 visita lista própria após criar/editar/excluir recusados, identidade inexistente e IDOR; par de CT-19/23/24/26/28/33 | G3 |
| Rastreio de auditoria / não-efeito não vazio | CT-48/49/51/52; autor e trilha prévios reais, campos comparados por identidade | G1 |
| Atomicidade dos efeitos nas duas direções | CT-53/54, erro depois do contador ou depois da trilha; os dois tipos exercitados | G1 |

Nenhuma negativa acima dispensa controle por suposta propriedade do framework. Onde seria necessário provar ausência de entrada ou controle pelo vendor, a resposta permanece **lacuna**, porque vendor e 02 estão ausentes. Não foi alegado “o filho já está protegido pelo pai”.

## Sem CT-B

**Nenhuma costura browser; 05 não criado.** A superfície do PRD existe, mas “depende de JS = sim” não basta.
Gravação, validação, listagem, ação e autorização são observáveis por componente: CT-01/03/05/08/10/11/13/15/17/18/19/20/23/26/28/29/31/33.
Rótulo dinâmico, sufixo, badge e cor foram recusados como oráculo por serem comportamento só do plano (Q8). Não há cláusula independente sobre pixel, acessibilidade ou execução de JS. Se Q8 tornar obrigatória a reação no navegador, derivar CT-B específico; não antecipar resposta.

## Cogitado e cortado — poda do passo 7

| Candidato | Destino/motivo |
|---|---|
| Browser para criar/editar/excluir e confirmar DB | Cortado; CT-15/17/18 provam por componente a menor custo |
| Browser apenas sem erros de console | Cortado; não afirma um resultado de RQ |
| Texto exato de rótulo reativo, cor de badge e precedência de situações | Q8; só o PRD determina |
| “Unit” chamando método puro de desconto do PRD | Cortado; costura não existe no arnês verificado, contrato P-01 já persiste |
| Duas chamadas independentes de aplicar retornam mesmo total, logo idempotência | Cortado; Pedido fora de escopo e nenhum agregado persistido comum. Lacuna Q6 |
| Chamadas sequenciais apresentadas como concorrência | Cortado; CT-43 fica identificado como snapshot; CT-44 exige disputa real |
| Adicionar vários mutantes de apagar método/retornar sempre null | Cortado; não são erros humanos plausíveis para inflar gate |
| Testar texto de log, channel e mensagens | Cortado; RQ-15 exige registro de uso, não linha de log |
| Só can() no lugar de tentar criação/edição/exclusão | Cortado; não prova que a ação exerce a barreira |
| Unique global, cascata da trilha e normalização silenciosamente assumidas | Cortado; respectivamente contrariam P-04 ou dependem de Q5/Q1 |

As duas camadas das validações/autorização não são duplicação: componente prova entrada/gravação da tela; domínio falsifica regra que vive só na tela. Os dois pontos de falha de CT-53/54 falsificam persistência parcial em ordens diferentes. Testes sem mutante exclusivo só permanecem quando um gate exige o observável adicional, como visitas CT-14/16 e ações de fronteira CT-33.

## Gate de Falsificabilidade — resultado da especificação

- Cada regra possui de 3 a 6 mutantes plausíveis; R6 tem sete porque M-79 veio de ADV-01 e não conta no teto, conforme exceção adversarial da skill.
- Um mutante sem matador da **tabela filha** permanece marcado explicitamente; a ausência de superfície não é razão para declarar o controle desnecessário.
- Todos os cenários têm Então e um único Quando. A aplicação de cada linha de Exemplos é independente.
- Toda fixture positiva fixa estado, ator e contexto. Cada negativa tem registro/autor/testemunha real e declara contador, cupom e trilha que não podem mudar.
- A matriz de 25 células discrimina elegibilidade e operações; as cinco células abertas são declarações de requisito pendente, não cobertas.
- Todos os cenários ficam na costura mínima **existente** que prova o observável; concorrência exige arnês novo explicitado.
- Passos 0–7 executados como derivação; **gate parcialmente fechado**, com lacunas declaradas. Não confundir “sem matador previsto” com mutante sobrevivente executado.
- Medição após implementação: instalar dependências somente com autorização; conferir plugin direto, driver, launcher Windows pestw.cmd e execução dos subprocessos, com duração e sobreviventes. Não rodar mutate agora contra código não entregue.
- A rule local testes-browser.md prevalece sobre a sugestão genérica de paralelismo da skill: navegador em série; não aplicar --parallel ao browser. Não foi presumida ausência de PCOV nesta máquina a partir da medição antiga da rule.

## Registro da sessão — substitui o 03 por instrução do usuário

Sem despacho da derivação: execução direta da feature-test-design pedida nesta sessão; a sessão não escreveu o PRD recebido.
Revisão adversarial: primeira rodada concluída com três achados fechados. A sessão principal despachou contexto novo somente com 00 e este 04 e contrato do revisor; sem 01, código ou raciocínio de derivação. Ferramentas do host não fornecem sandbox de leitura por path; limite será contratual, sem chamar isso de isolamento técnico.
Auditoria por hashes cobre os dois insumos imutáveis e arquivos de contexto lidos; não prova ausência de leitura em outros caminhos.


## Índice de Cenários

Todos os paths abaixo são **propostos; implementação não autorizada nesta tarefa**. Cada cenário/linha de Exemplos deve virar teste antes da aplicação. G1/G2/G3 executam ambos os modos quando a persona/contexto existe; não duplicar fixture do modo errado.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo proposto | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | Código obrigatório na criação e na edição | R1 | EP de presença, criação e edição | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-01 |
| CT-02 | O domínio recusa ausência de código fora do componente | R1 | EP de presença, criação e edição | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-02, M-03 |
| CT-03 | O formulário grava somente os dois tipos definidos | R2 | EP de enum e tipo; criar, editar e usar | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-06 |
| CT-04 | Tipo inválido não ganha validade pela chamada direta | R2 | EP de enum e tipo; criar, editar e usar | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-04, M-05 |
| CT-05 | Bordas do percentual são validadas na gravação do componente | R3 | EP; BVA 3-valores; tabela tipo × valor | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-07, M-08 |
| CT-06 | A gravação direta aplica o domínio do valor | R3 | EP; BVA 3-valores; tabela tipo × valor | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-09, M-10, M-12 |
| CT-07 | Valor legado inválido não produz desconto aplicável | R3 | EP; BVA 3-valores; tabela tipo × valor | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-11 |
| CT-08 | Validade e limite obrigatórios no formulário | R4 | EP de presença e representação; criação ≠ edição | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-16 |
| CT-09 | Obrigatoriedade sobrevive à gravação fora da UI | R4 | EP de presença e representação; criação ≠ edição | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-13, M-14, M-15 |
| CT-10 | A UI impede colisão literal no mesmo contexto | R5 | EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-20, M-77 |
| CT-11 | Editar sem mudar código não colide consigo mesmo | R5 | EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-18 |
| CT-12 | Unicidade não depende do formulário nem de tenant_id não nulo | R5 | EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-19, M-77 |
| CT-13 | Uma organização não reserva código para as demais | R5 | EP; identidade; unicidade criar/editar; normalização pendente Q1; concorrência na identidade | G2 | componente Livewire/Filament | `tests/Tenancy/CupomTenancyTest.php` | M-17 |
| CT-14 | A rota de criação oferece os cinco dados do cupom | R6 | Par visita × gravação; EP dos dois tipos; edição após uso | G3 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-26 |
| CT-15 | O formulário cria um cupom completo com unidades corretas | R6 | Par visita × gravação; EP dos dois tipos; edição após uso | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-21 |
| CT-16 | A rota de edição apresenta os valores do registro correto | R6 | Par visita × gravação; EP dos dois tipos; edição após uso | G3 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-23 |
| CT-17 | Editar grava todos os campos e mantém a identidade | R6 | Par visita × gravação; EP dos dois tipos; edição após uso | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-22, M-24 |
| CT-18 | Administrador exclui cupom sem histórico de aplicação | R7 | Estado × operação; exclusão real; CRUD combinado | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-28 |
| CT-19 | Identidade inexistente e exclusão repetida não alteram outros cupons | R7 | Estado × operação; exclusão real; CRUD combinado | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-29 |
| CT-20 | Uma edição não reescreve consumo nem história | R6 | Par visita × gravação; EP dos dois tipos; edição após uso | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-25, M-79 |
| CT-21 | Snapshot de um cupom excluído não pode ser consumido | R7 | Estado × operação; exclusão real; CRUD combinado | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-27 |
| CT-22 | A criação direta respeita cada papel | R8 | Matriz papel × criar; execução fora do componente e pela UI | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-31 |
| CT-23 | Forçar criação no componente não contorna autorização | R8 | Matriz papel × criar; execução fora do componente e pela UI | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-32 |
| CT-24 | Administradores alcançam a criação e a lista permanece uma saída válida | R8 | Matriz papel × criar; execução fora do componente e pela UI | G3 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-30 |
| CT-25 | Edição direta exerce permissão e acúmulo de papéis | R9 | Matriz papel × editar; pares de papéis; estado/campo discriminante | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-33, M-35 |
| CT-26 | Edição forçada de usuário comum preserva o valor gravado | R9 | Matriz papel × editar; pares de papéis; estado/campo discriminante | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-34 |
| CT-27 | A exclusão direta verifica o próprio verbo | R10 | Matriz papel × excluir; verbo destrutivo independente | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-36, M-38 |
| CT-28 | Chamada forçada de excluir não depende do botão oculto | R10 | Matriz papel × excluir; verbo destrutivo independente | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-37 |
| CT-29 | A listagem resolve todas as combinações de atividade | R11 | Tabela de decisão completa; EP de estado; cardinalidade e paginação | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-39, M-81 |
| CT-30 | Consulta da lista fora do componente aplica o mesmo recorte | R11 | Tabela de decisão completa; EP de estado; cardinalidade e paginação | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-41, M-81 |
| CT-31 | Paginar não perde os ativos de um conjunto estável | R11 | Tabela de decisão completa; EP de estado; cardinalidade e paginação | G2 | componente Livewire/Filament | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-40 |
| CT-32 | Snapshot estrangeiro não pode ser aplicado no contexto errado | R12 | IDOR; mass assignment; contexto nulo; troca de tenant | G1 | Pest feature HTTP | `tests/Tenancy/CupomTenancyTest.php` | M-44 |
| CT-33 | Editar e excluir por uuid alheio não atravessam o tenant | R12 | IDOR; mass assignment; contexto nulo; troca de tenant | G2 | componente Livewire/Filament | `tests/Tenancy/CupomTenancyTest.php` | M-48 |
| CT-34 | Tenant ausente não abre o escopo em modo multi-tenant | R12 | IDOR; mass assignment; contexto nulo; troca de tenant | G1 | Pest feature HTTP | `tests/Tenancy/CupomTenancyTest.php` | M-45 |
| CT-35 | Campos de posse e consumo não são aceitos do payload | R12 | IDOR; mass assignment; contexto nulo; troca de tenant | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-46 |
| CT-36 | Código igual em duas organizações aplica só o cupom corrente | R12 | IDOR; mass assignment; contexto nulo; troca de tenant | G1 | Pest feature HTTP | `tests/Tenancy/CupomTenancyTest.php` | M-43 |
| CT-37 | O localizador só oferece cupom existente e ativo | R13 | EP de existência; tabela de decisão completa com restrições | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-49, M-83 |
| CT-38 | Cada condição de elegibilidade pode impedir o consumo | R13 | EP de existência; tabela de decisão completa com restrições | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-50, M-51 |
| CT-39 | A borda temporal é estrita no lookup e no consumo | R14 | BVA 3-valores de segundo; tempo de uso; fuso e DST | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-52, M-54 |
| CT-40 | Leitura antes da expiração não autoriza consumo depois dela | R14 | BVA 3-valores de segundo; tempo de uso; fuso e DST | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-53 |
| CT-41 | O mesmo instante absoluto não muda de validade conforme o fuso | R14 | BVA 3-valores de segundo; tempo de uso; fuso e DST | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-55, M-56 |
| CT-42 | O último uso disponível é aceito e o próximo é recusado | R15 | BVA 3-valores; concorrência real; snapshots distintos | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-57 |
| CT-43 | Duas leituras antigas não dão dois últimos usos | R15 | BVA 3-valores; concorrência real; snapshots distintos | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-58 |
| CT-44 | Dois consumidores simultâneos disputam um único saldo | R15 | BVA 3-valores; concorrência real; snapshots distintos | G4 | Pest feature HTTP | `tests/Tenancy/CupomTenancyTest.php` | M-59, M-60 |
| CT-45 | Percentual inteiro trunca a fração do desconto | R16 | EP dos tipos; BVA monetária de centavo; exemplos discriminantes | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-61, M-62, M-63 |
| CT-46 | Valor fixo é centavos e não produz total negativo | R16 | EP dos tipos; BVA monetária de centavo; exemplos discriminantes | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-64, M-65, M-66 |
| CT-47 | Consumo não altera outro cupom do mesmo tenant | R17 | Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-68 |
| CT-48 | Um sucesso move o contador exatamente uma vez | R17 | Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-67 |
| CT-49 | Recusa não consome nem apaga aplicação anterior | R17 | Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-69 |
| CT-50 | Usos válidos repetidos pelo mesmo autor contam no limite global | R17 | Rastreio de efeito; EP tipo × efeito; limite global, não por pessoa | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-70 |
| CT-51 | A trilha identifica autor passado ao contrato e instante da aplicação | R18 | Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-71, M-72, M-73, M-74 |
| CT-52 | Contrato sem autor não cria uso anônimo | R18 | Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-75 |
| CT-53 | Falha ao registrar aplicação desfaz consumo já iniciado | R18 | Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-76 |
| CT-54 | Falha após inserir a trilha desfaz ambos os efeitos | R18 | Rastreio de efeito: aconteceu, não aconteceu, uma vez e atomicidade; tipo × efeito | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-76 (segundo ponto de falha) |
| CT-55 | Recusa no painel tem saída para uma lista alcançável | R11 | Tabela de decisão completa; EP de estado; cardinalidade e paginação | G3 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-42 |
| CT-56 | Usuário comum não abre edição de cupom pelo endereço direto | R9 | matriz papel × leitura; EP de estado | G3 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-78 |
| CT-57 | Código livre disputado não gera duas identidades iguais | R5 | concorrência de identidade; criar e editar; dois modos | G4 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php`, arnês compartilhado | M-80 |
| CT-58 | Nenhum perfil não administrador recebe inativos pela consulta direta | R11 | EP de atores × visibilidade | G1 | Pest feature HTTP | `tests/Kit/CupomTest.php + tests/Tenancy/CupomTenancyTest.php` | M-82 |


## Revisão adversarial — fechamento pela sessão principal

Rota efetiva: fw-adversario-ct por collaboration.spawn_agent, fork_turns="none", modelo herdado da sessão (identificador detalhado não exposto). Host Codex. Perfil TOML e contrato Markdown lidos; hooks Claude não executados. Limites de leitura/escrita contratuais, sem isolamento técnico por path.

| Rodada | Agente | Entrada | Achados distintos | Custo | Auditoria |
|---|---|---|---|---|---|
| 1 | /root/adversario_ct_1 | 00 + 04, sem 05 | 3 | não informado pelo host | Formato completo; 18 regras e 55 CT percorridos; hashes dos insumos, contexto e 04 inalterados |
| 2 | /root/adversario_ct_2 | 00 + 04 atualizado, sem 05 | 3 | não informado pelo host | Formato completo; conjunto inteiro de 56 CT percorrido; hashes dos insumos, contexto e 04 inalterados |

| Achado | Origem | Destino | Discriminância |
|---|---|---|---|
| ADV-01 | RQ-01/07, R6 | Oráculo reescrito em CT-20; M-79, exceção ao teto | Recusar edição do cupom ativo já usado deixa de passar: RENOMEADO precisa persistir |
| ADV-02 | RQ-14/P-04, R5 | Oráculos/datasets reescritos em CT-10/12; M-77 | Código de expirado/esgotado ainda existente bloqueia a colisão, na UI e fora dela |
| ADV-03 | RQ-08, R9 | Cenário novo CT-56; M-78, saída CT-55 | Save protegido não basta: ler edição como panel_user não pode expor os campos |

ADV-01 também aparece na seção de oráculos fracos; contado uma vez. Primeira rodada: **dois oráculos reescritos, um cenário novo, nenhuma lacuna nova**.
Amostragem: os três contraexemplos foram conferidos contra o 00 e os trechos do 04 antes da edição. Nenhum arquivo do produto foi usado para fechar achados.
Duas tentativas de patch falharam na conferência de contexto e não gravaram mudança parcial; o fechamento foi reaplicado somente neste 04.

### Fechamento da segunda rodada

| Achado | Origem | Destino | Discriminância |
|---|---|---|---|
| ADV2-01 | RQ-14/P-04, R5 | Cenário novo CT-57 e M-80 | Duas verificações prévias de ausência precedem escritas concorrentes reais; somente uma identidade RACE é aceita, criando ou editando |
| ADV2-02 | RQ-08/10/P-03, R11 | Oráculos reescritos em CT-29/30 e M-81 | A agora+1 aparece; V agora−1 e B exatamente agora não aparecem, em componente e consulta direta |
| ADV2-03 | RQ-08/P-02/P-03, R11 | Cenário novo CT-58 e M-82 | Mesmo sem decidir Q11 sobre entrada no painel, nenhum outro perfil não administrador pode receber inativos |

Rodada 2: **dois cenários novos, um achado convertido em oráculos reescritos, nenhuma lacuna nova**.
Conferência da matriz após fechamento: CT-37 foi reforçado para executar localização de todos os estados existentes; as células consultar V/E/VE agora apontam para o verbo realmente executado. M-83 discrimina esse observável. É correção de rastreabilidade da derivação, sem ler implementação.
**Teto de duas rodadas atingido.** As novas partições estruturais de identidade/visibilidade de R5/R11 foram registradas e fechadas, mas os acréscimos CT-57/58 e os últimos oráculos não tiveram terceiro julgamento independente. Essa limitação fica declarada e é encaminhada ao próximo ciclo de revisão/decomposição, sem perguntar ao usuário indisponível nem afirmar aprovação plena.
O segundo revisor relatou mensagem de inicialização automática do perfil PowerShell na primeira leitura; não solicitou/inspecionou esse conteúdo e usou login=false depois. Nenhum código de produto foi lido.

## Referências abertas

Raiz fw = `.ai/skills/feature-wiki/references/`; raiz td = `.ai/skills/feature-test-design/references/`.
- fw/hosts-e-subagentes.md — início/step 7 e despacho: capacidades e contexto novo.
- fw/ponytail-caveman.md — início: arquivos wiki usam prosa normal.
- fw/delegacao-casos-de-teste.md — step 7: entradas e fronteira do plano.
- fw/template-03-progresso.md — step 7: formato do registro que foi trazido para a saída, sem criar 03.
- fw/citacoes-de-codigo.md — antes de citar contexto: paths/símbolos e limites de prova.
- fw/roteamento-e-despacho.md — revisão: rota e quadro visível.
- td/template-04.md — passos 2/6/7 e escrita: formato, costuras e contagens.
- td/escolha-de-camada.md — passos 2/7: componente entre Feature e Browser.
- td/tecnicas-por-regra.md — passo 3: derivação integral por técnica.
- td/taxonomia-de-defeito.md — passo 4: tabela obrigatória da skill, sem abrir catálogos de experimentos.
- td/gherkin.md — passo 5: estrutura e Exemplos.
- td/armadilhas-de-api.md — passos 5/7: assertions/fakes e estado enum.
- td/mutation-testing.md — passo 6: operadores e limitações da prova.
- td/revisao-adversarial.md — revisão: tarefas e fechamento.

Também foram lidos o contrato `agents/fw-adversario-ct.md` e seu adaptador `agents/codex/fw-adversario-ct.toml`, ambos da feature-test-design; não são arquivos de references.
Não foram abertos template-05/pest-plugin-browser: nenhuma costura browser. Templates dos 00/01/02 e referências dos demais steps não foram abertos porque esta execução entra diretamente na derivação, sem recriá-los. Não foi lida pasta de experimento, conjunto anterior, catálogo ou relatório de rodada.


## Verificação final desta entrega

Conferência executada sobre **somente o 04 desta saída**, por Git Bash:

```bash
p=wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md
grep -cE '^[[:space:]]*(Cenário|Esquema do Cenário): \[CT-[0-9]+\]' "$p"
# 58
grep -cE '^## Regra R[0-9]+' "$p"
# 18
grep -cE '^\| M-?[0-9]+' "$p"
# 83
grep -cE '^\| M-?[0-9]+.*sem matador' "$p"
# 1
```

A conferência estrutural em memória retornou: **58 cenários, 58 IDs únicos, 58 blocos Gherkin analisados, zero blocos sem Então ou com quantidade de Quando diferente de um; 58 linhas no índice, nenhum ID faltante; 18 regras, 83 mutantes**.
Mutantes novos estão nas regras correspondentes: R5 M-77/M-80; R6 M-79; R9 M-78; R11 M-81/M-82; R13 M-83. R6 excede o teto apenas pela exceção adversarial explicitada.
Matriz: **5 × 5 = 25 células; 6 válidas + 14 inválidas + 5 lacunas = 25**. As lacunas de decisão não são marcadas como cobertas.
Integridade por SHA-256 conferida antes/depois de cada revisão e ao final: 00, 01, tests/Pest.php, composer.json/lock e regras lidas conservaram os hashes iniciais. O 04 permaneceu inalterado durante os despachos; as alterações de fechamento foram feitas pela sessão principal depois dos retornos.
Arquivo escrito: **somente wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md**. Nenhum 03/05, código, migration ou teste foi criado.
As contagens e a estrutura foram verificadas programaticamente; **Pest, browser e mutate não foram executados**, pois a entrega é a especificação e vendor está ausente. Não há mutation score certificado nem alegação de execução dos cenários.


