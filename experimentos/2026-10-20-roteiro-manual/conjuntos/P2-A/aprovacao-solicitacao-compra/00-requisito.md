# Requisito — FERRO-830: Fluxo de aprovação de solicitação de compra

## Fonte

- **Origem**: card FERRO-830, texto escrito pelo solicitante e colado integralmente no chat pelo desenvolvedor.
- **Data**: 2026-10-20.
- **Autor / solicitante**: solicitante do card; nome e área não informados.
- **Fidelidade**: alta (texto escrito, transcrição literal).

## Texto Original

<!-- IMUTÁVEL. Não editar, corrigir, resumir nem reordenar. -->

```text
CARD FERRO-830 — Fluxo de aprovação de solicitação de compra

O solicitante cria uma solicitação de compra com descrição, valor e centro de custo.
Enquanto está em rascunho ele pode editar e excluir.

Quando envia, a solicitação vai para o gestor do centro de custo aprovar. Se o valor
for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor.

O gestor pode aprovar ou rejeitar. Na rejeição a justificativa é obrigatória.
Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo.
Depois de aprovada não pode mais mexer.

O solicitante pode cancelar a qualquer momento antes da aprovação final.

Mostrar na tela o status atual e quem aprovou cada etapa.
Notificar por e-mail o próximo aprovador.
```

## Decomposição em Cláusulas

A redação das obrigações abaixo está determinada pelo card. O estado aberto registra uma dependência integral de escopo: o domínio de solicitações de compra e centros de custo não foi encontrado no projeto. Q1 precisa estabelecer quem entrega esse domínio antes de qualquer implementação. Isso não transforma obrigações explícitas em opções nem autoriza descartá-las.

| ID | Cláusula | Trecho literal de origem | Tipo | Estado |
|----|----------|--------------------------|------|--------|
| RQ-01 | O solicitante cria solicitação com descrição, valor e centro de custo. | "O solicitante cria uma solicitação de compra com descrição, valor e centro de custo." | funcional | aberta — Q1 |
| RQ-02 | O solicitante pode editar a solicitação em rascunho. | "Enquanto está em rascunho ele pode editar e excluir." | autorização | aberta — Q1 |
| RQ-03 | O solicitante pode excluir a solicitação em rascunho. | "Enquanto está em rascunho ele pode editar e excluir." | autorização | aberta — Q1 |
| RQ-04 | O envio encaminha a solicitação ao gestor do centro de custo para aprovação. | "Quando envia, a solicitação vai para o gestor do centro de custo aprovar." | funcional | aberta — Q1 |
| RQ-05 | Valor acima de R$ 5.000 exige também aprovação do diretor. | "Se o valor<br>for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor." | funcional | aberta — Q1 |
| RQ-06 | Quando a aprovação do diretor é exigida, ela ocorre depois da aprovação do gestor. | "Se o valor<br>for acima de R$ 5.000 precisa também da aprovação do diretor, depois do gestor." | restrição | aberta — Q1 |
| RQ-07 | O gestor pode aprovar a solicitação. | "O gestor pode aprovar ou rejeitar." | autorização | aberta — Q1 |
| RQ-08 | O gestor pode rejeitar a solicitação. | "O gestor pode aprovar ou rejeitar." | autorização | aberta — Q1 |
| RQ-09 | Rejeição exige justificativa. | "Na rejeição a justificativa é obrigatória." | restrição | aberta — Q1 |
| RQ-10 | Solicitação rejeitada volta para rascunho. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | funcional | aberta — Q1 |
| RQ-11 | O solicitante pode corrigir a solicitação que voltou ao rascunho após rejeição. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | autorização | aberta — Q1 |
| RQ-12 | O solicitante pode reenviar solicitação que voltou ao rascunho após rejeição. | "Solicitação rejeitada volta para rascunho pro solicitante corrigir e enviar de novo." | funcional | aberta — Q1 |
| RQ-13 | Solicitação aprovada não pode mais ser alterada. | "Depois de aprovada não pode mais mexer." | restrição | aberta — Q1 |
| RQ-14 | O solicitante pode cancelar a qualquer momento antes da aprovação final. | "O solicitante pode cancelar a qualquer momento antes da aprovação final." | autorização | aberta — Q1 |
| RQ-15 | A tela mostra o status atual. | "Mostrar na tela o status atual e quem aprovou cada etapa." | funcional | aberta — Q1 |
| RQ-16 | A tela mostra quem aprovou cada etapa. | "Mostrar na tela o status atual e quem aprovou cada etapa." | funcional | aberta — Q1 |
| RQ-17 | O próximo aprovador recebe notificação por e-mail. | "Notificar por e-mail o próximo aprovador." | funcional | aberta — Q1 |

O `<br>` representa apenas a quebra de linha do trecho citado; o Texto Original conserva as quebras literais. O limiar é estrito: exatamente R$ 5.000 não satisfaz a condição “acima”. Não presumir limites de texto ou dinheiro, poderes de administrador, rejeição pelo diretor, visibilidade histórica ou reutilização de aprovações.

## Perguntas ao Solicitante

Somente a raia requisito aparece nesta seção. Não houve resposta nem contato com o solicitante. Recomendações não são decisões. As perguntas abaixo têm pré-requisitos suficientes para discussão de negócio na primeira rodada; não dependem de escolher uma implementação. Sua resolução deverá entrar como Adendo, com fonte e texto literal.

| ID | Pergunta | Afeta | Recomendação | Estado |
|----|----------|-------|--------------|--------|
| Q1 | O card inclui criar o domínio ausente de solicitações de compra e centros de custo, com cadastro e vínculos dos aprovadores, ou pressupõe que esse domínio será fornecido por outra entrega? | RQ-01 a RQ-17 | Manter somente o que já existe e aguardar a entrega ou identificação do domínio. Criá-lo exige ampliar o escopo com cadastros e vínculos; esperar impede entregar o fluxo agora, mas evita inventar regras e entidades. | aberta |
| Q2 | De onde vêm os centros de custo, seu gestor e o diretor: cadastro por organização, integração externa ou outra fonte? Quem pode manter esses vínculos? | RQ-01, RQ-04, RQ-05, RQ-17 | Usar fonte explícita e vínculos dentro da mesma organização; não derivar aprovadores de nomes de papéis nem oferecer cadastro indiscriminado. | aberta |
| Q3 | O solicitante pode também atuar como gestor aprovador da própria solicitação? | RQ-04, RQ-07, RQ-08 | Não permitir que aprove ou rejeite a própria solicitação; exigir outro gestor elegível. Falha fechado contra autoaprovação. | aberta |
| Q4 | O solicitante pode também atuar como diretor aprovador da própria solicitação? | RQ-05, RQ-06 | Não permitir autoaprovação na etapa de direção; exigir outro diretor elegível. | aberta |
| Q5 | A mesma pessoa pode cumprir as etapas de gestor e diretor na mesma solicitação? | RQ-05, RQ-06, RQ-16 | Exigir pessoas distintas nas duas etapas. Não considerar uma aprovação como duas. | aberta |
| Q6 | Quem pode listar e consultar solicitações: apenas o solicitante e o aprovador atual, todos os aprovadores do centro, ou outras pessoas? Há separação por organização? | RQ-01, RQ-15, RQ-16 | Restringir ao solicitante e ao aprovador atual, dentro da organização autorizada; esconder de terceiros até definição explícita. | aberta |
| Q7 | Quem já aprovou continua vendo a solicitação após a troca de etapa, de função ou de organização? Quem perde uma corrida de decisão pode consultar o resultado? | RQ-15, RQ-16 | Não conceder acesso apenas por participação histórica; revalidar vínculo e permissão atuais e esconder o registro quando não houver acesso. | aberta |
| Q8 | O que ocorre se faltar gestor ou diretor elegível, ou se o responsável estiver inativo ou sem acesso? | RQ-04, RQ-05, RQ-17 | Bloquear a passagem para a etapa sem aprovador válido e explicar o impedimento; não aprovar automaticamente nem encaminhar para qualquer administrador. | aberta |
| Q9 | Uma troca de gestor ou diretor durante a tramitação transfere a pendência ao novo responsável ou mantém quem foi designado no envio? | RQ-04, RQ-05, RQ-16, RQ-17 | Suspender a decisão e exigir reatribuição explícita; não manter poder de aprovação de pessoa que perdeu a elegibilidade. | aberta |
| Q10 | O diretor também pode rejeitar? Se puder, exige justificativa e devolve ao rascunho como a rejeição do gestor? | RQ-05, RQ-09, RQ-10 | Não expor rejeição pelo diretor enquanto não houver definição; preservar a aprovação sequencial já exigida. Se a rejeição for incluída, especificar justificativa e destino em Adendo. | aberta |
| Q11 | Ao reenviar depois de uma rejeição, as aprovações anteriores perdem validade? A tela deve preservar e distinguir o histórico dos ciclos anteriores? | RQ-10, RQ-11, RQ-12, RQ-16 | Não reutilizar aprovações anteriores no novo envio; manter decisões anteriores identificadas por ciclo, sem apresentá-las como aprovação do ciclo atual. | aberta |
| Q12 | A proibição de mexer começa só na aprovação final? Enquanto aguarda aprovação, inclusive após o gestor aprovar, edição e exclusão ficam proibidas, preservando o cancelamento? | RQ-02, RQ-03, RQ-13, RQ-14 | Permitir edição e exclusão somente em rascunho; manter cancelamento antes da aprovação final, inclusive entre gestor e diretor. Não permitir alteração após aprovação final. | aberta |
| Q13 | Cancelamento é terminal ou permite reabrir? O histórico das etapas já decididas deve continuar disponível para quem tiver acesso? | RQ-14, RQ-15, RQ-16 | Tratar cancelamento como terminal, sem reabertura automática; não apagar decisões já registradas. | aberta |
| Q14 | Qual é o teto da descrição, e o conteúdo é texto simples? | RQ-01, RQ-02, RQ-11 | Usar texto simples com até 2.000 caracteres, validado também na camada de domínio; rejeitar excesso, sem truncar. O teto continua pendente. | aberta |
| Q15 | Qual é o teto da justificativa de rejeição, e texto só com espaços conta como ausência? | RQ-08, RQ-09 | Exigir texto simples não vazio após trim, com até 2.000 caracteres na camada de domínio; rejeitar excesso, sem truncar. O teto continua pendente. | aberta |
| Q16 | Quais valores são válidos: zero, negativos, máximo e casas decimais? Como tratar entrada com frações menores que um centavo? | RQ-01, RQ-02, RQ-05 | Aceitar apenas reais positivos com até duas casas decimais e teto declarado; rejeitar valores fora do domínio, sem arredondamento silencioso. O limiar estritamente acima de R$ 5.000 permanece determinado. | aberta |
| Q17 | Para qual tela leva o link do e-mail do próximo aprovador? O que o destinatário vê se, ao clicar, a etapa terminou ou ele perdeu o acesso? | RQ-15, RQ-16, RQ-17 | Levar ao detalhe autenticado da solicitação, revalidar acesso no clique e esconder dados sem permissão; nunca executar aprovação pelo link. | aberta |
| Q18 | Se a solicitação for cancelada, rejeitada ou mudar de aprovador antes do envio do e-mail enfileirado, o aviso ainda deve sair? Qual garantia de entrega e reenvio é necessária? | RQ-14, RQ-17 | Não enviar aviso de etapa obsoleta nem para destinatário sem acesso; não prometer entrega exatamente uma vez sem requisito e desenho específicos. | aberta |
| Q19 | Administradores e o perfil master_global podem decidir por terceiros ou alterar uma solicitação já aprovada? | RQ-02, RQ-03, RQ-07, RQ-08, RQ-13, RQ-14 | Não conceder poderes de negócio pelo acesso administrativo; manter imutabilidade final e identidade do responsável também na camada de domínio. | aberta |

### Rodada 1 — fronteira de requisito registrada, sem resposta

❓ Q1 · raia: requisito · afeta: RQ-01 a RQ-17 · depende de: —
O card inclui criar o domínio ausente de solicitações de compra e centros de custo, com cadastro e vínculos dos aprovadores, ou pressupõe que esse domínio será fornecido por outra entrega?
➡️ Recomendação: Manter somente o que já existe e aguardar a entrega ou identificação do domínio. Criá-lo exige ampliar o escopo com cadastros e vínculos; esperar impede entregar o fluxo agora, mas evita inventar regras e entidades.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-04, RQ-05, RQ-17 · depende de: —
De onde vêm os centros de custo, seu gestor e o diretor: cadastro por organização, integração externa ou outra fonte? Quem pode manter esses vínculos?
➡️ Recomendação: Usar fonte explícita e vínculos dentro da mesma organização; não derivar aprovadores de nomes de papéis nem oferecer cadastro indiscriminado.

❓ Q3 · raia: requisito · afeta: RQ-04, RQ-07, RQ-08 · depende de: —
O solicitante pode também atuar como gestor aprovador da própria solicitação?
➡️ Recomendação: Não permitir que aprove ou rejeite a própria solicitação; exigir outro gestor elegível. Falha fechado contra autoaprovação.

❓ Q4 · raia: requisito · afeta: RQ-05, RQ-06 · depende de: —
O solicitante pode também atuar como diretor aprovador da própria solicitação?
➡️ Recomendação: Não permitir autoaprovação na etapa de direção; exigir outro diretor elegível.

❓ Q5 · raia: requisito · afeta: RQ-05, RQ-06, RQ-16 · depende de: —
A mesma pessoa pode cumprir as etapas de gestor e diretor na mesma solicitação?
➡️ Recomendação: Exigir pessoas distintas nas duas etapas. Não considerar uma aprovação como duas.

❓ Q6 · raia: requisito · afeta: RQ-01, RQ-15, RQ-16 · depende de: —
Quem pode listar e consultar solicitações: apenas o solicitante e o aprovador atual, todos os aprovadores do centro, ou outras pessoas? Há separação por organização?
➡️ Recomendação: Restringir ao solicitante e ao aprovador atual, dentro da organização autorizada; esconder de terceiros até definição explícita.

❓ Q7 · raia: requisito · afeta: RQ-15, RQ-16 · depende de: —
Quem já aprovou continua vendo a solicitação após a troca de etapa, de função ou de organização? Quem perde uma corrida de decisão pode consultar o resultado?
➡️ Recomendação: Não conceder acesso apenas por participação histórica; revalidar vínculo e permissão atuais e esconder o registro quando não houver acesso.

❓ Q8 · raia: requisito · afeta: RQ-04, RQ-05, RQ-17 · depende de: —
O que ocorre se faltar gestor ou diretor elegível, ou se o responsável estiver inativo ou sem acesso?
➡️ Recomendação: Bloquear a passagem para a etapa sem aprovador válido e explicar o impedimento; não aprovar automaticamente nem encaminhar para qualquer administrador.

❓ Q9 · raia: requisito · afeta: RQ-04, RQ-05, RQ-16, RQ-17 · depende de: —
Uma troca de gestor ou diretor durante a tramitação transfere a pendência ao novo responsável ou mantém quem foi designado no envio?
➡️ Recomendação: Suspender a decisão e exigir reatribuição explícita; não manter poder de aprovação de pessoa que perdeu a elegibilidade.

❓ Q10 · raia: requisito · afeta: RQ-05, RQ-09, RQ-10 · depende de: —
O diretor também pode rejeitar? Se puder, exige justificativa e devolve ao rascunho como a rejeição do gestor?
➡️ Recomendação: Não expor rejeição pelo diretor enquanto não houver definição; preservar a aprovação sequencial já exigida. Se a rejeição for incluída, especificar justificativa e destino em Adendo.

❓ Q11 · raia: requisito · afeta: RQ-10, RQ-11, RQ-12, RQ-16 · depende de: —
Ao reenviar depois de uma rejeição, as aprovações anteriores perdem validade? A tela deve preservar e distinguir o histórico dos ciclos anteriores?
➡️ Recomendação: Não reutilizar aprovações anteriores no novo envio; manter decisões anteriores identificadas por ciclo, sem apresentá-las como aprovação do ciclo atual.

❓ Q12 · raia: requisito · afeta: RQ-02, RQ-03, RQ-13, RQ-14 · depende de: —
A proibição de mexer começa só na aprovação final? Enquanto aguarda aprovação, inclusive após o gestor aprovar, edição e exclusão ficam proibidas, preservando o cancelamento?
➡️ Recomendação: Permitir edição e exclusão somente em rascunho; manter cancelamento antes da aprovação final, inclusive entre gestor e diretor. Não permitir alteração após aprovação final.

❓ Q13 · raia: requisito · afeta: RQ-14, RQ-15, RQ-16 · depende de: —
Cancelamento é terminal ou permite reabrir? O histórico das etapas já decididas deve continuar disponível para quem tiver acesso?
➡️ Recomendação: Tratar cancelamento como terminal, sem reabertura automática; não apagar decisões já registradas.

❓ Q14 · raia: requisito · afeta: RQ-01, RQ-02, RQ-11 · depende de: —
Qual é o teto da descrição, e o conteúdo é texto simples?
➡️ Recomendação: Usar texto simples com até 2.000 caracteres, validado também na camada de domínio; rejeitar excesso, sem truncar. O teto continua pendente.

❓ Q15 · raia: requisito · afeta: RQ-08, RQ-09 · depende de: —
Qual é o teto da justificativa de rejeição, e texto só com espaços conta como ausência?
➡️ Recomendação: Exigir texto simples não vazio após trim, com até 2.000 caracteres na camada de domínio; rejeitar excesso, sem truncar. O teto continua pendente.

❓ Q16 · raia: requisito · afeta: RQ-01, RQ-02, RQ-05 · depende de: —
Quais valores são válidos: zero, negativos, máximo e casas decimais? Como tratar entrada com frações menores que um centavo?
➡️ Recomendação: Aceitar apenas reais positivos com até duas casas decimais e teto declarado; rejeitar valores fora do domínio, sem arredondamento silencioso. O limiar estritamente acima de R$ 5.000 permanece determinado.

❓ Q17 · raia: requisito · afeta: RQ-15, RQ-16, RQ-17 · depende de: —
Para qual tela leva o link do e-mail do próximo aprovador? O que o destinatário vê se, ao clicar, a etapa terminou ou ele perdeu o acesso?
➡️ Recomendação: Levar ao detalhe autenticado da solicitação, revalidar acesso no clique e esconder dados sem permissão; nunca executar aprovação pelo link.

❓ Q18 · raia: requisito · afeta: RQ-14, RQ-17 · depende de: —
Se a solicitação for cancelada, rejeitada ou mudar de aprovador antes do envio do e-mail enfileirado, o aviso ainda deve sair? Qual garantia de entrega e reenvio é necessária?
➡️ Recomendação: Não enviar aviso de etapa obsoleta nem para destinatário sem acesso; não prometer entrega exatamente uma vez sem requisito e desenho específicos.

❓ Q19 · raia: requisito · afeta: RQ-02, RQ-03, RQ-07, RQ-08, RQ-13, RQ-14 · depende de: —
Administradores e o perfil master_global podem decidir por terceiros ou alterar uma solicitação já aprovada?
➡️ Recomendação: Não conceder poderes de negócio pelo acesso administrativo; manter imutabilidade final e identidade do responsável também na camada de domínio.

Os recortes adicionais de Q2–Q19 ficam bloqueados somente naquilo que depende dessas respostas. Se Q1 for respondida, a decomposição deve ser revisada: fechar as obrigações determinadas e manter em aberto apenas o comportamento ainda indecidido. Não liberar toda a RQ apenas porque a existência do domínio foi esclarecida.

## Premissas

Nenhuma premissa de comportamento adotada. Não há autorização para transformar qualquer recomendação de Q1–Q19 em promessa da feature.

A premissa operacional mais estreita para este planejamento é usar somente as capacidades já existentes, sem criar ou adaptar entidades de negócio ausentes. Isso limita o trabalho executável e mantém as RQ bloqueadas; não reduz o requisito nem equivale a entregar um motor de aprovação.

## Fora de Escopo (declarado)

Nenhuma exclusão funcional foi declarada pelo solicitante no card.

A sessão foi autorizada somente a planejar até o step 4. Não foi autorizada a implementar nem a executar etapas posteriores. Essa restrição de execução não elimina nenhuma cláusula do card.

