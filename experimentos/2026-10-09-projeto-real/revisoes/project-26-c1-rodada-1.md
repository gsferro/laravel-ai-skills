# Revisão adversarial independente — cupons de desconto — saída c1

- Data: 2026-10-09.
- Agente independente: família GPT-6; esforço ultra; deployment exato não exposto.
- Escopo percorrido: 42 CT do 04, dois CT-B do 05, 14 regras, 49 mutantes previstos e as oito tarefas do contrato.
- Resultado: sete achados, ADV-01 a ADV-07. Nenhum cenário foi reescrito ou editado.
- Natureza da prova: confronto documental com o requisito e contramodelos que preservam os demais comportamentos. Não é execução de aplicação, Pest, browser, concorrência ou mutation testing.

## Implementações erradas que passam

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | O save valida o código enviado, inclusive colisões, mas descarta `codigo` ao gravar a edição. Uma troca para código novo e disponível é ignorada. | RQ-01/02/07/14, P-04; R1 e R6: edição dos dados do cupom respeitando a unicidade por organização. | Partição de edição: código próprio inalterado × código ocupado × código novo disponível. | Dado um cupom próprio e um código novo disponível, Quando o admin troca o código para esse novo valor, Então a mesma chave possui o novo código e os demais dados, contador e trilha permanecem iguais. |
| ADV-02 | A validação percentual exige inteiro, mas a do fixo aceita `numeric` e converte silenciosamente 12,5 centavos para 12. | RQ-03/04, P-05; R2/R3: `valor` é inteiro e, no fixo, representa centavos. | Partição do tipo de dado condicionada pelo tipo de desconto, também na escrita direta. | Dado os demais campos válidos, Quando o admin envia fixo com valor 12.5 pela criação, edição ou escrita direta, Então a operação recusa o valor fracionário sem persistir nem alterar o cupom. |
| ADV-03 | A lista de Beto filtra ativos e os handlers recusam escrita, mas o GET de edit autoriza pelo acesso à lista e carrega qualquer cupom da Acme, inclusive inativo. | RQ-08, P-03; R10/R13: usuário comum pode apenas listar ativos. | Matriz papel × entrada de leitura × estado; acesso direto por identidade conhecida. | Dado Beto usuário comum e um UUID próprio vencido conhecido, Quando Beto abre diretamente a rota edit desse UUID, Então a leitura é recusada sem dados do cupom e sua lista continua contendo somente os ativos. |

**Provas de sobrevivência ao conjunto:**

- **ADV-01:** CT-03 mantém PROMO-A; CT-17 aceita PROMO-A inalterado ou recusa OUTRO ocupado. CT-18 também testa colisão, e CT-05/06 recusam código inválido. O contramodelo conserva essas validações, cria códigos corretamente e altera os outros campos; nenhum CT afirma a persistência de um código novo disponível numa edição bem-sucedida. As âncoras dos CT-B não acrescentam essa partição.
- **ADV-02:** CT-07/08/09 usam fração somente no tipo porcentagem. Os fixos válidos são 100, 101, 102, 150, 1000 ou 1500, sempre inteiros; os exemplos inválidos gerais não isolam fração no fixo. O contramodelo continua recusando nulo, vazio e texto não numérico, preserva o domínio percentual e calcula corretamente todos os valores fixos usados. Aceitar e truncar 12.5 no fixo permanece invisível. Nenhum teto adicional nem decisão sobre fixo zero é necessário para esse achado.
- **ADV-03:** CT-35 abre edit com Ana admin e UUID estrangeiro, mantendo o isolamento. CT-31/32 afirmam recusa das escritas; CT-38/40 afirmam o recorte da lista. Nenhum deles exige uma recusa de leitura do UUID próprio inativo por Beto. A recuperação depois de uma rota vedada, sem identificar e afirmar essa recusa de conteúdo, não fecha essa entrada. O contramodelo nega as mutações, oculta os botões e mantém todos os resultados das listas.

## Oráculos fracos

| ID | CT | Por que passa com defeito | O que o "Então" precisa afirmar |
|---|---|---|---|
| ADV-04 | CT-30, em contraste com CT-02/03/31/32/33 | RQ-07 e P-02: a consulta de autoridade permite os dez pares, mas o handler real exige exatamente um papel. Os admins isolados continuam escrevendo e todos os testes de operação presentes passam; o admin acumulando panel_user ou infra é recusado ao executar a escrita. O `Então` de CT-30 só observa a resposta da consulta de autoridade. | Em cada acumulação com admin, a criação, edição e exclusão efetivas realizam a alteração esperada; nos pares sem admin, as operações efetivas preservam os dados. Uma resposta de autorização não é esse observável. |
| ADV-05 | CT-01, linha de edit | RQ-01/05: edit mostra código, tipo, valor e limite corretos, mas hidrata a validade com uma data futura padrão em vez do instante persistido. O `Então` pede a presença do campo validade, porém os dados esperados de edit são apenas PROMO-A, porcentagem, 10 e 3. CT-03 envia expressamente outra validade; CT-05 recusa a alteração; CT-08/17 não afirmam a validade após seus aceites; CT-B02 faz um submit recusado. Assim, essa hidratação errada e a gravação involuntária da data em um save válido não divergem dos observáveis descritos. | A tela edit carrega a validade do cupom específico; uma edição válida de outro campo conserva esse instante quando a validade não foi alterada. |
| ADV-06 | CT-10 / M10, incluindo os demais exemplos de cálculo do conjunto | RQ-12, P-01/05/06: para a expressão escrita em M10, `(int)(total * percentual / 100)`, multiplicar 10000 por 29 antes de dividir produz desconto 2900, também em binary64, e retorno 7100. O matador anuncia 7101, mas não diverge desse mutante. Os outros totais percentuais do conjunto também produzem o desconto esperado nessa ordem. | Usar um par de constantes que realmente diverge na expressão escolhida e fixar o retorno inteiro exato; ou descrever outra expressão como mutante e demonstrar sua divergência, sem atribuí-la à expressão atual. |

**Demonstração numérica de ADV-06:**

- M10, tal como escrito, calcula `10000 × 29 / 100 = 2900`; o retorno é `10000 − 2900 = 7100`. Não se deve substituir silenciosamente a expressão por `total × (percentual / 100)` ao avaliar o matador.
- Em um contrato `int` de 64 bits, o total positivo `9007199254740999` e percentual `1` cabem nos tipos de P-01/P-05. O desconto inteiro truncado é `90071992547409` e o retorno é `8917127262193590`. Converter a divisão para binary64 produz desconto truncado `90071992547410` e retorno `8917127262193589`: esse par expõe um centavo perdido pela implementação em float.
- Foram executadas somente expressões autocontidas de constantes, usando Decimal para o controle exato e Double para binary64. Os cinco resultados foram, na ordem: `2900`, `90071992547409`, `90071992547410`, `8917127262193590`, `8917127262193589`. Não foi executado PHP nem lida implementação. O exemplo grande é condicionado a int de 64 bits; não afirma o tamanho do inteiro do host futuro.

As outras 48 linhas de mutantes foram confrontadas com seus observáveis declarados. Não foi encontrada outra demonstração de matador não discriminante. Isso não mede mortes de mutantes. O próprio 04 já limita a parte de CT-25 referente à redução de limite quando a validação recusa a redução antes de executar o ramo; não a converti em uma decisão sobre Q3.

## Cenários malformados

Nenhum achado. Os 42 CT e os dois CT-B têm `Então` e exatamente um `Quando` explícito por cenário ou esquema. Configurar/gravar um formulário, disputar uma vaga em paralelo e enumerar páginas são ações agregadas de seus cenários; não há um segundo `Quando` explícito nem um segundo submit oculto no CT-B02.

## RQ sem cenário discriminante

Nenhuma RQ-01 a RQ-15 ou P-01 a P-09 fica integralmente sem um cenário discriminante. Há aspectos sem discriminação, registrados nos ADV acima e na sonda 7, sem duplicar IDs nesta seção.

| Fonte vigente | Discriminação presente no conjunto |
|---|---|
| RQ-01 | CT-01/02/03/33: visita, criação, edição e exclusão; limites de código e hidratação em ADV-01/05 |
| RQ-02 | CT-02/04/05/06: presença e persistência do código; edição válida incompleta em ADV-01 |
| RQ-03 | CT-04…09: enum e duas partições de tipo |
| RQ-04 | CT-02/07…12: valor, unidade e cálculo; fração no fixo em ADV-02 |
| RQ-05 | CT-02/03/04…06/13…15: persistência e validade; hidratação em ADV-05 |
| RQ-06 | CT-02/04…06/22…25: limite e consumo |
| RQ-07 | CT-02/03/30…35: autorização; operação com papéis acumulados em ADV-04 |
| RQ-08 | CT-31/38…40: só leitura e só ativos; entradas de leitura e histórico em ADV-03/07 |
| RQ-09 | CT-19…21/36: inexistência, remoção e objeto estrangeiro |
| RQ-10 | CT-13…15/27: antes, no instante, depois e fuso |
| RQ-11 | CT-22…24/27: borda, stale, concorrência desenhada e recusas |
| RQ-12 | CT-10…15/22/26/28: retornos exatos; mutante float em ADV-06 |
| RQ-13 | CT-13/22…29: incremento único e ausência de efeito na recusa/falha |
| RQ-14 | CT-16…18: colisão própria, outro tenant e edição sem troca de identidade |
| RQ-15 | CT-26…29/41: pessoa, instante, uma vez, não efeito, falha tardia e autor ausente |
| P-01 | CT-10…29/41: motor recebe total e pessoa; não exige Pedido |
| P-02 | CT-02/03/30…37/42: organização e três autoridades admin |
| P-03 | CT-13/22/38…40: ativo deriva de validade e saldo |
| P-04 | CT-16…18/37: unicidade por organização e identidade do contexto |
| P-05 | CT-07…12 e CT-B01/02: percentual inteiro e fixo em centavos; ADV-02/06 |
| P-06 | CT-10/11: truncamento, incluindo meio centavo; limite do matador em ADV-06 |
| P-07 | CT-12: desconto maior que total, igualdade e sobra de um centavo |
| P-08 | CT-26…29: trilha persistida própria, sem depender da auditoria genérica |
| P-09 | CT-01/02/03 e CT-B01/02: painel /app |

O 00 não contém coluna Estado nem RQ marcada `aberta — Qn`. Suas perguntas históricas coexistem com premissas assumidas explícitas, usadas como vigentes. Q1–Q5 do 04 se referem a extensões ainda sem resposta; não converti suas recomendações em obrigação. Normalização/teto do código, validade passada no cadastro, limite zero/redução, fixo zero, total negativo, retenção depois de excluir e identidade de Pedido continuam sem decisão. Não há cenário impondo cascade, normalização de código ou idempotência de Pedido.

## Sondas 6–8

| ID | Sonda (6 par de papéis / 7 participante histórico e link / 8 teto de texto) | Par, recorte ou campo | Lacuna | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-07 | 7 — participante histórico e visibilidade | RQ-08/15 e P-03: aplicador histórico que continua sendo usuário comum; cupom esgotado ou vencido | CT-38/40 não identificam Beto como autor de uso dos cupons inativos da lista. Uma consulta `ativo OU usado por este usuário` conserva os resultados atuais quando os usos dos inativos pertencem a Carla, fixture compatível com o conjunto, mas revela cupom inativo a Beto depois de seu próprio uso. CT-26/28 têm atores distintos e trilha, porém não listam depois da aplicação/esgotamento. | Dado Beto usuário comum aplicou um cupom que agora está esgotado ou vencido e outro cupom segue ativo, Quando Beto lista os cupons, Então recebe somente o ativo e o cupom usado por ele continua registrado na trilha sem aparecer na lista. |

- **Sonda 6:** CT-30 contém a mesma pessoa em todos os dez pares dos cinco papéis do 00: master_global × admin; master_global × admin_organizacao; master_global × panel_user; master_global × infra; admin × admin_organizacao; admin × panel_user; admin × infra; admin_organizacao × panel_user; admin_organizacao × infra; panel_user × infra. Não há par ausente. A limitação entre consultar autoridade e executar operação foi registrada uma única vez em ADV-04.
- **Sonda 7:** o recorte vigente é usuário comum × ativos da organização. O histórico de aplicação não cria exceção em RQ-08/P-03; portanto ADV-07 espera que o inativo saia da lista, sem alterar sua trilha. Não há aprovação, notificação ou link de notificação no requisito; essas sondas não se aplicam. Retenção depois de excluir cupom/autor é Q4, não foi resolvida nesta revisão.
- **Sonda 8:** o texto livre identificado é o código. O requisito não fixa um teto `n`; Q1 do 04 registra essa ausência e não importa o teto de 40 de outra fonte. Não existe teste `(n, n+1)` no model, mas também não existe RQ/P vigente que determine os dois resultados. Essa é uma lacuna de decisão já declarada, sem ADV nem limite inventado.

## Áreas e regras percorridas

- Cadastro e CRUD: R1/R2, cinco campos, criação e edição, ausente/nulo/vazio/tipo errado, payloads recusados, preservação e alteração por identidade.
- Domínio condicionado e cálculo: R3/R4, percentual 1–100, fixo em centavos, fração, truncamento, meio centavo e piso zero; todos os exemplos e M07–M13.
- Tempo e existência: R5/R7, instante estrito de expiração, objetos stale, offsets/fuso, inexistente, removido e operações sobre identidades ausentes.
- Unicidade: R6, organização própria/estrangeira, colisão consigo/outro, criação/edição direta e modo single-tenant; sem decidir normalização ou teto.
- Contador e trilha: R8/R9, bordas do limite, legado, stale sequencial, concorrência desenhada, contador forjado, uma linha por aplicação, autoria/instante, não efeito e rollback pós-inserção.
- Autorização e isolamento: R10/R11/R12, três admins, demais papéis, dez pares, componente/escrita direta, exclusão, UUID estrangeiro, tenant forjado e contexto nulo; limites de inventário da entidade filha permanecem não demonstrados.
- Listagem e histórico: R13, duas condições de ativo, todos os estados, cardinalidade 0/1/P/P+1, busca, enumeração de páginas e inserção com reinício; não foi presumida ordenação estável sem reinício.
- Interface declarada no conjunto: R14 e os dois CT-B, criação/edição, unidade visível, erro associado, operabilidade e âncora persistida. Não foi confirmada a superfície real, nem exigidos texto exato, cor, screenshots ou critérios adicionais de UI.
- O conjunto inteiro de M01–M49 foi lido, incluindo os três matadores no 05; previsões não foram tomadas como medição.

## Leituras negadas

- Nenhuma ferramenta negou leitura. Nenhuma leitura fora da lista autorizada foi solicitada deliberadamente; não houve tentativa de contornar recusa.
- Arquivos de domínio lidos: `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md`, `wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md` e `05-casos-de-teste-browser.md`. `wikis/glossario.md` não existe; apenas sua existência foi consultada.
- Arquivos de contrato lidos nesta cópia: `.ai/skills/feature-test-design/agents/fw-adversario-ct.md` e `references/revisao-adversarial.md`. Frontmatter, hook e escolha de modelo Claude foram ignorados conforme despacho; referências mencionadas nos CT não foram abertas.
- 01, 02, aplicação, testes, vendor, catálogos, experimentos, outros projetos/conjuntos e retorno externo da derivação não foram lidos. Afirmações do 04 sobre essas fontes não foram verificadas.
- **Controles efetivos:** filesystem irrestrito e ferramenta de shell sem whitelist. Cegamento por contrato; nenhum hook Claude ou sandbox impôs a lista. As primeiras duas leituras iniciaram automaticamente o perfil PowerShell do host e emitiram um diagnóstico PSReadLine; o perfil não foi inspecionado e todas as consultas posteriores usaram `login:false`. Essa inicialização automática impede alegar exclusão técnica de acesso fora da árvore.
- Única escrita autorizada: este `adversarial-1.md`. Nenhum Artisan, Pest, browser, build, script de testes, hook ou aplicação foi executado. A única execução de cálculo foi a expressão de constantes descrita em ADV-06.
- Não foram medidos DDR, MSI/mortes de mutantes, tokens, concorrência real ou equivalência entre hosts. Risco restante: as provas são documentais e condicionadas à futura materialização preservar os oráculos descritos; não certificam o software.
