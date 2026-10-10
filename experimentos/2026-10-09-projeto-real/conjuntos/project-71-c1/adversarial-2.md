# Revisão adversarial — rodada 2 (última)

Revisor independente: `/root/adversarial_71_c1_r2`, contexto novo, host Codex, família GPT-6, esforço ultra solicitado; implantação exata não exposta. Data: 2026-10-09. Foram percorridos os 50 CT do 04, os 2 CT-B do 05, as 17 regras e todas as tabelas de mutantes. Resultado: **5 achados distintos** — 3 implementações erradas não discriminadas e 2 problemas em matadores previstos. A quota antiga de cinco implementações não foi usada para criar achados adicionais.

Entradas lidas: corpo de `.ai/skills/feature-test-design/agents/fw-adversario-ct.md`, `references/revisao-adversarial.md`, `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md` e 04/05 desta pasta. `wikis/glossario.md` não existe. A seção de fechamento da primeira rodada está incorporada ao 04 autorizado e foi exposta incidentalmente na leitura inicial; **não** foi aberto `adversarial-1.md`, o retorno da derivação ou qualquer outra entrada externa. As conclusões abaixo vêm dos cenários e dos contraexemplos, não da resolução anterior.

## Implementações erradas que passam

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | O motor confirma que o objeto recebido é da organização corrente, mas depois recarrega o cupom por código numa consulta global e aplica/consome o primeiro resultado, sem manter o recorte de organização. | P-02/P-04; RQ-12/RQ-13/RQ-15; R4/R6/R10/R12/R13 | Identidade × contexto no sucesso; rastreio do alvo e do não-alvo | Dado PROMO de 10% na Acme e PROMO fixo de 3000 na Globex inserido antes, ambos ativos, Quando a aplicadora da Acme aplica o objeto local a 10000, Então recebe 9000 e somente o cupom local recebe um uso e sua aplicação registrada. |
| ADV-02 | A autoria é `usuário do guard HTTP, se existir; senão o argumento aplicadoPor`, em vez de usar o argumento definido pelo contrato do motor. | RQ-15/P-01; R13 | Partição de fontes de identidade: guard ausente, igual e distinto do argumento | Dado Ana autenticada e Beto como aplicadoPor no motor da Acme, Quando o cupom é aplicado com Beto no instante T, Então a única aplicação registra Beto e T, sem atribuição a Ana. |
| ADV-03 | O cálculo e o contador usam o cupom recebido, mas a linha de cupom_usos é ligada ao primeiro cupom do contexto, obtido por uma relação/consulta sem identidade do alvo. | RQ-15/P-08/P-01; R13 | Rastreio da identidade do efeito com dois alvos locais discriminantes | Dado dois cupons ativos locais A e B com A inserido antes e trilhas distintas, Quando B é aplicado no instante T por Beto, Então somente B ganha a nova aplicação de Beto/T e toda a trilha de A permanece igual. |

**Prova ADV-01.** CT-11 e CT-12 distinguem códigos iguais ou reutilizáveis entre organizações somente na gravação; não aplicam o cupom nessa configuração. CT-20 recusa um objeto que já pertence à Globex: a guarda inicial do mutante também o recusa. CT-21 fecha o contexto nulo; CT-26/29/41 podem continuar relendo a linha única correta e recusando tempo, saldo ou remoção. Nenhum sucesso do motor exige dois cupons de organizações diferentes com o mesmo código e atributos discriminantes. No contraexemplo acima, o mutante devolve **7000**, incrementa Globex e liga a trilha a Globex; o contrato local exige **9000**, consumo Acme e Globex inalterada. Não se exige aplicar cupom de outra organização: o argumento é o objeto válido da Acme.

**Prova ADV-02.** CT-36:1011–1016 exige explicitamente guard HTTP ausente, portanto o fallback grava Beto e satisfaz todo o oráculo. CT-37:1023–1028 distingue Ana/Beto entre aplicações, mas não fixa um guard autenticado distinto do argumento da segunda chamada. Nenhum outro CT impõe essa divergência. Todos os cenários podem ser executados com guard vazio nas chamadas diretas ou igual ao aplicadoPor, e o mutante passa. Com Ana no guard e Beto no argumento contratual de P-01, ele grava **Ana**; o mesmo contrato exige **Beto**. Isso é uma variante de M-47, não a variante já morta de depender exclusivamente de Auth.

**Prova ADV-03.** CT-36/37 exigem vínculo ao cupom e identidade/instante concretos, mas exercitam sucessos com um único cupom alvo local. Nenhum sucesso auditado obriga o alvo a ser o segundo de dois cupons elegíveis no mesmo contexto. Os cenários que têm SENTINELA e aplicações de preparação admitem o alvo criado/aplicado primeiro, antes da sentinela; os CT de listagem e CRUD não aplicam um segundo alvo como ação sob teste. Logo todas as fixtures podem respeitar a entrada existente e fazer o primeiro cupom coincidir com o alvo. No contraexemplo A/B, o retorno e o contador de B estão certos, porém a aplicação Beto/T aparece em **A**, impedindo auditar corretamente o uso de B. O defeito é distinto de ADV-01: consulta, cálculo e consumo permanecem locais e corretos; só a identidade persistida na trilha está errada.

## Oráculos fracos

| ID | CT | Por que passa com defeito | O que o "Então" precisa afirmar |
|---|---|---|---|
| ADV-04 | CT-23:693–705 / M-25:726 — RQ-08/P-02/P-03, R7 | M-25 promete matar a consulta que filtra só a primeira página, mas a fixture não garante um registro proibido além da primeira página da consulta sem filtros. É possível que todos os proibidos sejam removidos na primeira página; a página seguinte fica só com ativos locais e a asserção passa. | Conservar o conjunto exato já exigido, com um discriminante de fixture que garanta ao menos um expirado local e um ativo da outra organização na página seguinte da consulta sem os filtros. Isso é controle da prova, não uma nova regra de ordenação de negócio. |
| ADV-05 | Matador M-60:1214 de CT-45 — RQ-08/P-02, R16 | A asserção da tabela é somente “GLOBEX permanece com valor 10 e contador 1”. Trocar record para GLOBEX e devolver seus atributos na resposta não edita o banco; sob o próprio mutante, valor 10 e contador 1 continuam iguais. | O matador precisa incluir a recusa da troca e a ausência de atributos de GLOBEX na resposta, como o Então de CT-45:1204 já exige. O cenário completo tem esse oráculo; o matador declarado o omite. |

**Prova ADV-04.** Considere a ordem estável da consulta sem filtros `[EXPIRADO_ACME, ATIVO_GLOBEX, A01, …, A11]`, com página de 10. O mutante pagina essa consulta e aplica o filtro apenas à primeira página: ela devolve A01–A08; a segunda devolve A09–A11 sem filtro. O conjunto observado é exatamente os 11 ativos locais, sem repetição e sem proibidos em qualquer página: passa o Então/E de CT-23 e a asserção de M-25. O mesmo vale para as quantidades 0/1/9/10 da tabela, mantendo os dois proibidos no início. CT-22/24/44/46 não percorrem uma página posterior com proibidos nela, e podem continuar protegidos na primeira página. O mutante falha quando um proibido fica na segunda página, configuração que o conjunto atual não obriga. A falta não é a quantidade de registros, mas a posição discriminante dos proibidos na consulta defeituosa.

**Prova ADV-05.** A ação de CT-45 é a troca de propriedade entre requests, sem save posterior. O mutante pode aceitar a chave e resolver/devolver GLOBEX com seus atributos existentes; nenhum UPDATE ocorre. Portanto a comparação de valor/contador da tabela não diverge. Não se propõe reescrever CT-45: seu Então completo discrimina o vazamento/aceitação, e deve ser o matador descrito.

## Cenários malformados

Nenhum achado. A varredura textual dos 50 CT e 2 CT-B encontrou um Quando e um Então por cenário/esquema. CT-B02 especifica um único ciclo recusa→correção, com observação intermediária explícita antes da segunda submissão; não tem dois passos Quando nem depende somente do registro final.

## RQ sem cenário discriminante

Nenhuma RQ inteira fechada ou P vigente ficou totalmente sem cenário discriminante: RQ-01–15 e P-01–09 têm pelo menos um discriminante. Isso não elimina as combinações ausentes de ADV-01–03.

O 00 não possui coluna Estado e assume P-01–09 nas ambiguidades; foram tratadas como vigentes. O 04 registra Q1–Q4 e lista RQ-02/04/05/06 como abertas **somente nos recortes não decididos**, preservando cenários dos invariantes fechados. Não foi identificado cenário que imponha teto textual, normalização de código, aceitação/recusa de validade passada no cadastro, limites 0/negativos/fracionários ou fixo mínimo/máximo não decididos. Não transformei essas perguntas em novos requisitos nem em ADV.

## Sondas 6–8

| ID | Sonda (6 par de papéis / 7 participante histórico e link / 8 teto de texto) | Par, recorte ou campo | Lacuna | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|

Sem ADV adicional nas sondas:

- **6 — acumulação de papéis:** os cinco papéis nomeados por P-02 geram dez pares. CT-17 enumera todos eles, cada um nas duas ordens e nos três verbos: 60 linhas. Não há par ausente. Não foram inventados papéis de aprovação que o 00 não contém.
- **7 — participante histórico e links:** o requisito não tem aprovação/decisão nem notificação com link. Os recortes existentes são organização e atividade; uso anterior não cria direito de listar cupom expirado/esgotado contrário a RQ-08/P-03. CT-49 cobre a recuperabilidade imediata da aplicação após exclusão; prazo futuro e remoção da pessoa seguem sem decisão. CT-19 observa o destino efetivo de recusa já especificado no conjunto, sem inferir notificações. A colisão de código no sucesso foi registrada em ADV-01.
- **8 — teto de texto:** código é o único texto livre pedido. O 00 não define n; Q1 e L2 declaram essa decisão ausente, inclusive caixa/espaços/Unicode. Não há como definir n/n+1 sem criar requisito. O teto textual do plano não foi adotado nem consultado. Não há outro texto livre no requisito.

## Áreas e regras percorridas

- **CRUD — R1:** visitas create/edit, persistência de ambos os tipos, edição nos quatro estados, exclusão e guarda da conversão de entrada somente data; CT-01–04/50 e M-01/02/03/66/68/70.
- **Validação — R2–R4:** tipos exclusivos; percentual inteiro 1–100, fração, fixo em centavos; criação/edição/escrita direta; unicidade local, outra organização e tenant nulo; CT-05–13 e suas tabelas.
- **Autorização — R5/R6/R15/R16:** cinco papéis, todos os pares/ordens/verbos, herança administrativa no painel, revogação, UUID de outro tenant, objeto retido, contexto nulo, campos protegidos e estado adulterado do framework; CT-14–21/42–45/48. Achados ADV-01/05.
- **Elegibilidade — R7–R9/R11/R14:** tabela completa validade×saldo, igualdade temporal, usos acima do limite, páginas/busca/removido, fuso local/UTC, objeto desatualizado, disputa da última unidade, inexistência, condições inválidas isoladas/combinadas e exclusão seguida de uso; CT-22–30/33–34/40–41/46–47. Achado ADV-04.
- **Cálculo — R10:** percentual com truncamento, inteiro de centavos, discriminantes de float/arredondamento/truncamento final e piso zero; CT-31/32 e M-34–38. Valores conferidos por raciocínio sobre constantes; nenhuma microexecução matemática nova foi necessária.
- **Auditoria e consumo — R12/R13:** incremento persistido exatamente uma vez, vínculo cupom/pessoa/instante, guard ausente, história, rollback antes/depois de inserir a trilha e recuperação imediata após excluir cupom; CT-35–39/49 e M-43–51/74. Achados ADV-01–03.
- **Navegador — R17:** unidade visível nas duas transições, retirada do teto percentual no fixo, recusa de 101 e correção para 100 no mesmo fluxo; CT-B01/B02 e M-61–63. Nenhum seletor foi confirmado por execução.
- **Cobertura transversal:** todas as 74 linhas de mutantes previstas foram lidas, além do índice, matriz de estado×operação, taxonomia e lacunas L1–L6. Ausência de requisito sobre retry/idempotência do pedido, domínio textual, domínio monetário máximo, ordenação concorrente, DST pessoal, inventário da implementação e retenção futura não foi convertida em regra nova.

## Leituras negadas

- **Nenhuma tentativa de leitura negada.** Não foi tentado abrir 01, código, testes de aplicação, relatório da primeira rodada, retorno de derivação, catálogo, experimentos ou outro projeto/conjunto.
- **Restrição efetiva:** filesystem irrestrito; cegamento por contrato explícito de paths e cwd `D:\PROJECTS\SKILLS\blind-20261009\project-71`. Não há whitelist mecânica de leitura. Frontmatter/model/hooks Claude foram ignorados conforme despacho; nenhum hook foi tratado como prova de isolamento. Todas as chamadas de shell usaram `login:false`, sem perfil PowerShell.
- **Escrita autorizada e realizada:** somente `wikis/specs/saida-c1/cupons-de-desconto/adversarial-2.md`. Nenhum cenário foi editado.

## Limites e execução

Foram executadas somente leituras dos arquivos autorizados, consulta de existência do glossário, busca textual nesses mesmos 04/05 e escrita deste relatório. Não houve Artisan, Pest, browser, inspeção de código, concorrência real, mutation testing ou medição comportamental. As provas são contraexemplos da especificação; não afirmam defeito presente na implementação, mutante realmente sobrevivente, DDR, economia de tokens ou equivalência entre hosts. A exposição incidental do fechamento anterior dentro do 04 limita a cegueira informacional e está registrada acima.
