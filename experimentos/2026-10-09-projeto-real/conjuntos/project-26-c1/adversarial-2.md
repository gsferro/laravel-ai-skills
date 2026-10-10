# Revisão adversarial — rodada 2 de 2 — cupons de desconto

Data: 2026-10-09. Revisor independente `/root/adversarial_26_c1_r2`, família GPT-6, esforço ultra solicitado; deployment exato não exposto. Revisão documental do conjunto inteiro: 45 definições de CT no 04, 2 CT-B no 05 e 55 mutantes previstos. Resultado: **1 achado comprovado, ADV-01**. Os IDs deste relatório começam novamente em ADV-01 e não identificam os achados da rodada anterior.

## Implementações erradas que passam

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | O ramo fixo valida apenas que valor seja inteiro e permite persistir inteiros com sinal, incluindo -1 centavo, na criação ou edição. O ramo percentual continua restrito a 1–100 e as demais regras continuam corretas. | RQ-04 e **P-05**, que fixa a coluna valor como `unsignedInteger`; R2/R3, domínio do valor fixo. | Partição dos inteiros negativos no ramo fixo, incluindo -1 na fronteira anterior a zero, também na escrita direta. | Dado administrador autorizado, demais dados válidos e um cupom fixo existente, Quando cria ou edita por uma entrada de escrita com valor fixo -1, Então a escrita é recusada e não existe cupom novo nem alteração do registro, contador ou trilha anteriores. |

**Prova de ADV-01:** P-05 do 00 declara literalmente “uma coluna `valor`, do tipo `unsignedInteger`”. O sinal negativo viola essa premissa já vigente. CT-07 só exercita fixo 100, 101, 102 e string 12.5; CT-08 exercita fixo 150 e string 12.5; CT-09 exercita fixo 150 e string 12.5. Os outros cenários de cadastro, edição e aplicação usam valores válidos positivos, ausência, nulo, vazio, texto ou fração. Nenhum deles envia um inteiro fixo negativo, consulta a signedness da coluna ou exige recusa desse valor. Uma implementação que preserve todos os comportamentos descritos e admita negativos somente no ramo fixo satisfaz todos os exemplos atuais, inclusive as recusas de fração reforçadas nesta rodada. Se usar o cálculo fixo correto nos demais casos, `max(0, 10000 - (-1))` retorna 10001: o valor indevido aumenta o total em um centavo.

A lacuna não exige decidir se fixo zero é permitido. Q3 do 04 reserva essa pergunta e a de total negativo; a rejeição de **valor fixo negativo** já decorre de P-05. O cenário sugerido deve ser materializado separadamente por entrada e verbo; não define o resultado de zero.

## Oráculos fracos

Nenhum outro achado comprovado. Percorri os Então dos 45 CT e 2 CT-B e as asserções dos 55 mutantes previstos. As âncoras de identidade, valor, contador, autoria e instante discriminam os defeitos descritos nos respectivos exemplos; a reação do navegador exige unidade visível e erro associado ao campo.

Reavaliei M10 diretamente por uma expressão matemática autocontida em JavaScript/V8, sem aplicação: `100 * (29 / 100)` resulta em `28.999999999999996`, truncamento 28 e retorno 72; o cálculo inteiro exato produz desconto 29 e retorno 71. Portanto o exemplo atual de CT-10 diverge sob o mutante descrito. Essa verificação não mede uma morte em PHP/Pest. CT-24 exige execução concorrente real; CT-29 exige alcançar a falha após inserir a trilha. A especificação dessas condições não prova que tenham sido executadas.

## Cenários malformados

Nenhum achado: cada uma das 45 definições de CT e dos 2 CT-B contém um Quando e pelo menos um Então. As linhas de Exemplos são execuções independentes. Não identifiquei definição sem Então ou com dois Quando.

## RQ sem cenário discriminante

Não identifiquei RQ ou P integralmente sem cenário. A obrigação de representação sem sinal em P-05 tem cobertura parcial: a partição negativa do fixo não é discriminada, conforme **ADV-01**, sem duplicar o mesmo defeito em outro ID.

O 00 não contém coluna Estado nem cláusula declarada `aberta — Qn`. As P-01…P-09 são premissas assumidas na fonte e vigentes para esta revisão. Q1…Q5 do 04 registram extensões sem decisão, sem transformar as RQ-01…RQ-15 em cláusulas abertas. Não usei recomendações dessas perguntas como requisitos aceitos.

| Fonte vigente | Cenários discriminantes percorridos |
|---|---|
| RQ-01 e P-09: CRUD no painel /app | CT-01/02/03/33/43; CT-B01/02 |
| RQ-02: código indispensável | CT-04/05/06 e CT-43 |
| RQ-03/04 e P-05: dois tipos, valor e unidade | CT-04…12; CT-B01/02; lacuna de sinal em ADV-01 |
| RQ-05/10: validade e instante de expiração | CT-01/03/04…06/13…15/27/43 |
| RQ-06/11/13: limite, contador e consumo | CT-04…06/22…29 |
| RQ-07 e P-02: autoridade dos administradores | CT-02/03/30…35/44 |
| RQ-08 e P-03: somente listagem dos ativos | CT-31/38…40/44/45 |
| RQ-09: existência no consumo | CT-19/20/36 |
| RQ-12 e P-01/06/07: motor, cálculo inteiro, truncamento e piso zero | CT-10…15/22/26 |
| RQ-14 e P-04: unicidade por organização | CT-16…18/43 |
| RQ-15 e P-08: autoria e instante em trilha própria | CT-26…29/41; preservação em CT-03/43/45 |

## Sondas 6–8

Nenhum ADV adicional comprovado.

| Sonda | Par, recorte ou campo | Verificação e limite |
|---|---|---|
| 6 — acumulação de papéis | master_global × admin; master_global × admin_organizacao; master_global × panel_user; master_global × infra; admin × admin_organizacao; admin × panel_user; admin × infra; admin_organizacao × panel_user; admin_organizacao × infra; panel_user × infra | Os dez pares dos cinco papéis nomeados no 00 estão em CT-30, com create/save/delete em execuções independentes e persistência discriminante. “Nenhum” é ausência de papel, também exercitada separadamente. |
| 7 — participante histórico | Aplicador panel_user diante do recorte de cupons ativos | CT-45 cria uma aplicação real de Beto antes de vencer/esgotar, depois exige apenas CONTROLE na lista, por componente e fonte direta, nos dois tipos; preserva a trilha histórica. CT-44 recusa a leitura direta de edit em cinco estados. |
| 7 — destino de link | Notificação com link | Não se aplica: notificação, e-mail e relatório de uso estão explicitamente fora de escopo no 00. Retenção após exclusão permanece pergunta Q4; não escolhi cascade nem bloqueio de exclusão. |
| 8 — teto de texto livre | Código do cupom | O 00 não fixa n, normalização, domínio Unicode ou outro teto. O 04 declara a lacuna em Q1 e não presume 40. Não é possível provar violação de um teto vigente ou escolher n/n+1; por isso não criei ADV. Ausência/vazio e unicidade literal têm cenários também fora da UI. |

## Áreas e regras percorridas

- **R1/R2/R3/R6 — cadastro, domínio dos cinco campos e identidade:** acesso/hidratação, criação/edição efetivas, código novo, conservação da validade, campos indispensáveis, tipos de dados, partições por unidade, fração e unicidade por organização em formulário e escrita direta; CT-01…09/16…18/43. ADV-01 está nesta área.
- **R4 — cálculo:** centavos, pontos percentuais inteiros, cálculo exato, ordem da expressão de M10, meio centavo, truncamento e piso zero; CT-10…12.
- **R5/R7/R8/R9 — aplicação e efeitos:** segundo exato, objeto stale, offsets, inexistência/remoção, limite abaixo/na/acima da borda, contador forjado, corrida real exigida, autoria distinta do criador, instante, ausência de autor, cardinalidade e rollback tardio; CT-13…15/19…29/41.
- **R10/R11/R12 — autorização e isolamento:** três administradores, usuários sem autoridade, todos os pares de papéis, cada verbo efetivo, leitura direta de edit, exclusão do alvo/identidade ausente, objeto estrangeiro, payload de tenant e contexto nulo; CT-30…37/42/44.
- **R13 — listagem:** validade E saldo, estados ativos/inativos/removido, organização, 0/1/P/P+1, busca, enumeração reiniciada e aplicador histórico; CT-38…40/45.
- **R14 — interação no navegador:** unidade percentual/centavos visível sem reload, mudança do discriminador, erro no campo, operabilidade e âncora persistida; CT-B01/02, M47…M49.
- Li também os índices, matrizes, perguntas, taxonomia, tabela de mutantes e limites do 04/05. Reavaliei os cenários e provas diretamente; os fechamentos anteriores não foram usados como prova.

## Leituras negadas

Nenhuma. Não houve tentativa de leitura fora da lista autorizada nem bloqueio técnico a testar. `wikis/glossario.md` foi consultado apenas quanto à existência e não existe.

## Entradas, exposição incidental e controles efetivos

Entradas lidas nesta cópia: corpo de `.ai/skills/feature-test-design/agents/fw-adversario-ct.md`, `references/revisao-adversarial.md`, `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md`, `wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md` inteiro e `05-casos-de-teste-browser.md` inteiro. A primeira leitura do 04 retornou truncada; li novamente suas faixas sucessivas para percorrer todo o arquivo.

**Exposição incidental autorizada:** o 04 inclui descrições de costura/plano, alegações de verificações locais e a tabela de fechamento dos sete achados anteriores; o 05 inclui o estado da primeira revisão. Esses conteúdos foram vistos ao ler as entradas inteiras autorizadas. Não abri o 01, código, testes, raciocínio/retorno da derivação, `adversarial-1.md`, catálogos, experimentos, outro projeto ou conjunto. As alegações incorporadas aos documentos permanecem alegações da entrada, sem confirmação nesta revisão.

Filesystem irrestrito, shell sem whitelist, nenhum hook Claude ativo e nenhum bloqueio efetivo de leitura por path. O cegamento foi por contrato de paths, não por sandbox, prompt read-only, hook heurístico ou git status. Todas as chamadas de shell desta rodada usaram `login:false`. O frontmatter e seu modelo/hook Claude foram ignorados conforme despacho. A única escrita autorizada e realizada foi este relatório; nenhum cenário foi editado.

## Execução e limites

- Executado: leitura documental do conjunto inteiro, oito tarefas adversariais, consulta de existência do glossário e duas expressões matemáticas autocontidas de constantes (M10 e efeito de valor fixo negativo).
- Não executado: aplicação, Artisan, Pest, browser, testes do repositório, mutation testing, concorrência ou falha transacional real. Nenhuma morte de mutante, DDR, economia de tokens ou equivalência entre hosts foi medida.
- A lacuna de inventário de superfície/entradas, o teto de código e as extensões Q1…Q5 permanecem sem comprovação de implementação. Não inferi novas APIs nem decisões ausentes para convertê-las em achados.
- Esta é a segunda e última rodada. ADV-01 deve ser encaminhado à sessão para decidir a correção do conjunto e registrar o destino; este relatório não corrige cenários nem solicita terceira revisão. O risco documentado é admitir desconto fixo negativo apesar da representação sem sinal de P-05.