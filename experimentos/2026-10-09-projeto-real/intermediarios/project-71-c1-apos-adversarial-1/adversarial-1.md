## Implementações erradas que passam

Revisão independente de especificação: 11 achados distintos, ADV-01–ADV-11. A prova de sobrevivência abaixo confronta cada implementação proposta com os observáveis descritos nos 47 CT e nos 2 CT-B; não é execução da aplicação. A exceção é a microprova aritmética de ADV-01, executada em PHP com expressões autocontidas. Nenhum cenário foi reescrito.

| ID | Implementação errada | RQ / regra | Técnica que faltou | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-01 | O motor calcula o desconto percentual por `(int)(($percentual / 100) * $total)`. Todos os exemplos percentuais fornecidos devolvem os valores esperados, inclusive 29/10000 → 7100. Entretanto, 29/100 → 72, quando o contrato inteiro exige 71. Os demais comportamentos podem permanecer corretos. | RQ-12, P-05/P-06, R10; 04:777–789 e M-34 em 04:810. | Exemplo discriminante comprovado para precisão monetária. | Dado cupom ativo de 29%, Quando aplicado a 100 centavos, Então o retorno é exatamente 71 centavos e há exatamente um consumo e um registro. |
| ADV-02 | O formulário grava limite 3 em todo create/save, descartando o limite informado; as fixtures e o motor mantêm leitura correta dos limites persistidos. CT-02 envia 3; CT-03 envia 5, mas exige apenas atividade com 2 usos, também satisfeita por limite 3. Os demais casos de CRUD não afirmam o limite gravado; os limites distintos dos casos de aplicação vêm de fixtures. | RQ-06, R1; 04:170–185. A pergunta sobre o domínio permitido não elimina a necessidade de guardar o limite válido informado. | Rastreio de efeito sobre cada atributo; valor persistido após edição. | Dado cupom com limite 3 e dois usos, Quando a administradora grava limite 5, Então o limite recarregado é exatamente 5 e contador e trilha permanecem iguais. |
| ADV-03 | O formulário oferece apenas data e grava 00:00:00 daquele dia. O 00 determina, nessa condição, 23:59:59. CT-02/03 pedem validade futura sem afirmar o timestamp persistido, e CT-27 prepara diretamente um timestamp correto: o motor pode estar certo enquanto a conversão da tela está errada. | RQ-05/RQ-10, R1/R8; 00, pergunta aberta 5 com premissa explícita; 04:172–185 e 683–693. | Fronteira entre entrada de data, persistência e instante efetivo de validade. | Dado formulário que aceita somente data, Quando a administradora informa 2026-10-10, Então a validade persistida corresponde a 2026-10-10 23:59:59 no fuso da aplicação. |
| ADV-04 | Excluir cupom apaga em cascata seus registros de cupom_usos. CT-04 inclui cupom com dois usos reais, mas afirma apenas ausência do cupom e integridade de SENTINELA; nenhum caso consulta a trilha desse cupom depois da exclusão. CT-36–39 verificam história antes dessa transição. Assim, a operação autorizada elimina a prova de quem aplicou e quando. | RQ-01/RQ-15, P-08, R1/R13/R14; 04:194–205, 929–958 e lacuna L6 em 1154. | Estado × evento e rastreio do efeito histórico após exclusão. Não é necessário inventar prazo de retenção para distinguir a perda imediata provocada pela própria operação entregue. | Dado cupom usado por Ana em T com registro auditável, Quando a administradora exclui o cupom, Então a aplicação de Ana em T continua recuperável para auditoria. |
| ADV-05 | A admissão às telas do /app permite admin_organizacao, mas recusa admin e master_global; a via direta do domínio autoriza corretamente os três papéis. Todas as visitas, operações de componente e CT-B autorizados usam a administradora da organização. CT-15 e CT-17 exercitam os outros administradores somente fora do componente. | P-02 afirma expressamente que admin e master_global continuam alcançando a tela; RQ-01/RQ-07, R1/R5. 04:159–168, 430–504. | Matriz papel × superfície, incluindo as células positivas do painel. | Dado admin ou master_global no contexto Acme, Quando visita as telas de criação e edição no /app, Então alcança o formulário administrativo e pode concluir a escrita autorizada. |
| ADV-06 | A escrita direta verifica apenas 1 ≤ percentual ≤ 100 e converte uma fração para inteiro, aceitando 12,5 como 12; o formulário rejeita frações corretamente. CT-08/09 cobrem a fração no formulário, mas CT-10 testa a via direta apenas com 0 e 101. CT-34 testa o uso de percentuais legados também apenas com esses extremos. | P-05, R3/R11; 04:299, 318, 322–333 e 842–851. | Partição não inteira em cada fronteira de escrita. | Dado a administradora e demais atributos válidos, Quando cria ou edita diretamente com percentual 12,5, Então a escrita é recusada sem novo cupom nem mudança no registro, contador ou trilha existentes. |
| ADV-07 | Sem contexto tenant, a criação direta insere silenciosamente um quarto cupom com tenant_id nulo, sem consultar nem alterar os três alvos preparados. As demais operações sem contexto fecham corretamente. CT-21 afirma somente leitura/alteração dos cupons Acme, Globex e do registro global preexistente e preservação de seus efeitos; não afirma ausência de uma nova linha. CT-42/43 usam contexto Acme. | P-02, R6; CT-21 em 04:553–566 e M-23 em 575. | Não-efeito global da operação de criação; cardinalidade e discriminante nulo. | Dado tenancy ligada sem organização corrente e um snapshot de todos os cupons, Quando se tenta criar um cupom, Então a criação é recusada e nenhuma nova linha de cupom ou cupom_usos existe em contexto algum. |
| ADV-08 | A listagem considera ativo quando expira_em ≥ agora, enquanto o motor usa corretamente expira_em > agora. CT-22 distingue somente futuro/passado; CT-25/26 cobrem a igualdade exclusivamente na aplicação. Todas as consultas de listagem e busca fornecem datas futuras ou passadas. | RQ-08, P-03, regra temporal assumida para RQ-10, R7/R8; 04:589–604 e 654–680. | BVA no consumidor de visibilidade, além do motor. | Dado usuária comum e cupom com saldo cuja expiração é T, Quando lista em T, Então esse cupom não pertence ao conjunto visível. |
| ADV-09 | A listagem filtra disponibilidade por usos ≠ limite, enquanto o motor usa corretamente usos < limite. CT-22 usa somente 2 e 3 para limite 3; CT-28 inclui o legado 4, mas apenas na aplicação. Um cupom legado com usos 4/limite 3 aparece como ativo sem quebrar qualquer cenário de listagem. | RQ-08, P-03, R7/R9; 04:596–604 e 723–728. | BVA limite+1 na consulta; partição legada de saldo indisponível. | Dado usuária comum e cupom futuro legado com usos 4 e limite 3, Quando lista os ativos, Então o cupom não pertence ao resultado e a leitura não altera contador nem trilha. |

Os defeitos acima podem ser restritos à camada indicada, preservando todas as outras regras. Por exemplo, os timestamps e limites preparados diretamente para G-A não passam pelo formulário defeituoso de ADV-02/03; a query defeituosa de ADV-08/09 não altera o motor correto. Essa separação explica a sobrevivência ao conjunto inteiro, e não apenas ao cenário citado.

## Oráculos fracos

Os IDs ADV-01 e ADV-07 abaixo referenciam achados já contados; ADV-10 e ADV-11 são achados adicionais do gate. Ausência de assertOk/assertSee isolado no texto não substitui a análise de divergência.

| ID | CT | Por que passa com defeito | O que o "Então" precisa afirmar |
|---|---|---|---|
| ADV-01 | CT-31 / M-34 | A asserção 29% de 10000 → 7100 permanece verdadeira com a implementação float descrita. Os outros quatro exemplos de CT-31 e o caso padrão 10% de 10000 também permanecem verdadeiros. A alegação de divergência 7101 não se confirmou na microprova PHP. | Usar pelo menos um valor que de fato diverge: 29% de 100 centavos deve devolver 71, não 72, conservando os efeitos corretos. |
| ADV-07 | CT-21 / M-23, linha criar | Preservar os três alvos não distingue recusa de criação de inserção de uma quarta linha global. O oráculo declarado por M-23 repete a preservação dos alvos e também não diverge nessa implementação. | A criação foi recusada e a cardinalidade/conjunto de cupons de todos os contextos permaneceu inalterado. |
| ADV-10 | CT-19 / M-67 | O Quando visita expressamente a listagem após uma tentativa recusada. Um redirect da recusa de volta à escrita proibida pode continuar errado; um GET manual posterior da listagem ainda apresenta ACME10 e leitura utilizável. CT-14/16/18 não afirmam o destino da saída da recusa. A asserção de M-67 confunde essa visita independente com o destino produzido pela recusa. | Se M-67 permanecer como mutante, observar o destino efetivamente produzido/seguido depois da recusa, sem abrir manualmente outra rota, e afirmar que é um destino alcançável pela usuária. Isso é correção do gate; o 00 não determina uma URL literal. |
| ADV-11 | CT-17 / M-19 | Todos os pares com administrador são escritos com esse papel primeiro; o único par sem administrador é panel_user+infra. Uma implementação que escolhe o primeiro papel passa com fixtures anexadas na ordem da tabela. O conjunto não fixa uma ordem em que panel_user antecede admin_organizacao nem exige independência da ordem; por isso a asserção positiva citada em M-19 não garante divergência sob o próprio algoritmo de primeiro papel. | Para o mesmo par administrativo, afirmar a mesma autorização e efeito persistido com ambas as ordens de atribuição/retorno, incluindo panel_user primeiro. Nenhuma regra deve depender da posição do papel. |

Microprova executada, sem carregar bootstrap ou código do projeto:

```php
$flutuante = ($p / 100) * $total;
$finalFloat = $total - (int) $flutuante;
$finalInteiro = $total - intdiv($total * $p, 100);
```

| Percentual | Total | Desconto float, %.17g | Final float | Final inteiro |
|---|---|---|---|---|
| 29 | 10000 | 2900 | 7100 | 7100 |
| 10 | 9999 | 999.90000000000009 | 9000 | 9000 |
| 5 | 50 | 2.5 | 48 | 48 |
| 1 | 100 | 1 | 99 | 99 |
| 100 | 9999 | 9999 | 0 | 0 |
| 10 | 10000 | 1000 | 9000 | 9000 |
| 29 | 100 | 28.999999999999996 | 72 | 71 |

Percorridas todas as 67 linhas M-01–M-67 do 04, além das três linhas repetidas no 05. Não identifiquei outra asserção que permanecesse verdadeira sob o defeito específico de seu mutante. Para M-19, a sobrevivência demonstrada é a ordem plausível da própria tabela, não execução de fixtures materializadas.

## Cenários malformados

- Nenhum CT/CT-B sem Então ou com mais de um Quando. Conferência determinística dos blocos Gherkin: 47 cenários no 04 e 2 no 05, todos com exatamente um Quando e pelo menos um Então; IDs únicos em cada conjunto. Os ciclos de CT-B02 foram verificados também pelo roteiro: ele exige observação intermediária antes da correção.
- O check acima verifica a estrutura solicitada; não executa um parser Gherkin externo nem valida a implementação dos cenários.

## RQ sem cenário discriminante

- Nenhuma das RQ-01–RQ-15 ou P-01–P-09 está inteiramente ausente do rastreio do conjunto. Isso não elimina as sub-regras sem discriminante: limite válido gravado (ADV-02); conversão da data oferecida pela UI (ADV-03); histórico depois da exclusão (ADV-04); admissão dos administradores herdados no painel (ADV-05); fração na escrita direta (ADV-06); criação sem tenant (ADV-07); bordas da atividade na listagem (ADV-08/09).
- RQ-12/P-05/P-06 têm cenários de cálculo, mas o exemplo anunciado como matador de precisão não discrimina o algoritmo float proposto (ADV-01).
- O 00 não contém coluna Estado nem RQ marcadas aberta — Qn. O 04 cria Q1–Q4 e escreve RQ-02/04/05/06 como abertas em 04:79–82. As perguntas novas realmente não têm resposta para teto textual, zero/máximo do fixo, validade passada no cadastro e domínio do limite. Essa ausência de resposta não torna indeterminados o limite válido digitado, a validade efetivamente gravada, a unidade inteira de P-05 ou a regra temporal já assumida no próprio 00. As lacunas de domínio pendentes não foram convertidas em cenários inventados nesta revisão.
- Não encontrei cenário que imponha teto 40, normalização de caixa/espaços, mínimo 1 do fixo, recusa obrigatória de validade passada no cadastro ou regra de redução do limite não decidida pelo 00. Os valores positivos de fixtures não afirmam essas decisões abertas.

## Sondas 6–8

| ID | Sonda (6 par de papéis / 7 participante histórico e link / 8 teto de texto) | Par, recorte ou campo | Lacuna | Cenário sugerido (Gherkin, 1 linha) |
|---|---|---|---|---|
| ADV-11 (referência) | 6 — par de papéis | admin_organizacao × panel_user, com usuário comum primeiro | Todos os dez pares aparecem, com os três verbos; falta discriminar a dependência da ordem usada pelo algoritmo descrito em M-19. | Dado a mesma pessoa com panel_user atribuído antes de admin_organizacao, Quando executa uma escrita administrativa, Então recebe autorização e o efeito correto, como na ordem inversa. |

- Sonda 6: verificados master_global×admin, master_global×admin_organizacao, master_global×panel_user, master_global×infra, admin×admin_organizacao, admin×panel_user, admin×infra, admin_organizacao×panel_user, admin_organizacao×infra e panel_user×infra. CT-17 contém os dez pares × criar/editar/excluir, total de 30 linhas. Não há par ausente.
- Sonda 7: o 00 não define fluxo de decisão, aprovador histórico ou notificação com link; notificações estão expressamente fora de escopo. Os recortes de visibilidade são organização e atividade derivada. Quem aplicou um cupom não ganha, no 00, uma exceção para listar cupons esgotados/expirados; não inventei essa exceção. A preservação de auditoria histórica após exclusão foi revisada separadamente e produziu ADV-04.
- Sonda 8: código é o único campo de texto livre do requisito. Não existe n informado no 00; Q1 reconhece essa decisão pendente. Não é possível escrever n/n+1 no model sem inventar o teto. A falta de resposta é registrada como pendência de requisito, não como implementação defeituosa comprovada. Tipo é enum; valor, data e limite não são texto livre.

## Áreas e regras percorridas

- CRUD, R1/R14: visitas create/edit, persistência dos dois tipos, edição dos quatro estados, exclusão dos quatro estados, chave removida, objeto retido e SENTINELA; CT-01–04/40/41.
- Validação, R2–R4/R11: presença e domínio do tipo, domínio condicionado tipo×valor, inteiro percentual, limites 0/1/2/99/100/101, fração, unidades, colisão local/externa/nula, edição contra si, escrita direta, inexistência e legado; CT-05–13/33/34/47.
- Autorização, R5/R6/R15/R16: cinco papéis, dez pares, três verbos, revogação entre requests, matriz painel×domínio, IDOR, tenant nulo, objetos carregados, campos protegidos, ordenação/busca e identidade de record; CT-14–21/42–45.
- Visibilidade e elegibilidade, R7–R9: validade×saldo para ambos os tipos, 0/1/9/10/11 registros, busca, removido, igualdade temporal, horário local/UTC, objeto antigo, limite−1/limite/limite+1 e concorrência com histórico; CT-22–30/46.
- Cálculo, R10: porcentagem inteira em centavos, truncamento do desconto, piso zero, diferença entre tipos, bordas do fixo, precisão float; CT-31/32 e todos os retornos numéricos dos demais casos de aplicação.
- Auditoria e consumo, R12/R13: zero/um/N efeitos, incremento uma vez, autoria do chamador sem guard, timestamps concretos, conservação de aplicações, rollback antes/depois da trilha e exclusão posterior; CT-33–39/04/41.
- Navegador, R17: troca real de tipo nos dois sentidos, indicação de unidade visível, retirada do teto percentual no fixo, recusa visível, não-efeito intermediário e correção pelo mesmo formulário; CT-B01/B02. Verificados os roteiros e os mutantes M-61/62/63.
- Foram confrontadas todas as RQ-01–RQ-15 e todas as P-01–P-09 de A-01–A-09; os quatro tópicos Q1–Q4 do 04 foram mantidos como perguntas sem resposta, sem importar decisões do plano.
- Execução efetiva: leitura dos três documentos de entrada e do corpo do contrato; sondagem de existência de wikis/glossario.md (inexistente); contagem estrutural dos blocos Gherkin/IDs/mutantes; microprova PHP de sete pares percentual/total; gravação exclusiva deste relatório. Não executados aplicação, Pest, browser, concorrência ou pest --mutate.
- Controle efetivo: comandos disponíveis com filesystem irrestrito (danger-full-access), cwd explícito D:/PROJECTS/SKILLS/blind-20261009/project-71. A lista de leitura e a escrita exclusiva são obrigações por contrato, sem sandbox mecânico de leitura. Frontmatter Claude de tools/model/hooks não se aplica neste host. Não tratei prompt, read-only, hook, git status ou este relato como prova de isolamento. Revisão despachada independentemente, com esforço ultra solicitado; não recebi dados comparativos nem resultados de outras execuções.

## Leituras negadas

- Nenhuma. Não houve tentativa de leitura fora da lista autorizada. Não foram lidos 01, implementação, referências extras, outros projetos/conjuntos, catálogo, relatórios ou conversa de derivação. Nenhum hook de guarda foi executado neste host.
