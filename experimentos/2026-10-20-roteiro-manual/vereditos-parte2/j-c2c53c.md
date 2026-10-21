Avaliei os **26 passos com “Resultado esperado”**, respeitando os recortes declarados. Preparação isolada não comprova a pós-condição do CT.

| RM | Passo | Classe | Citação do roteiro | Citação da origem (se não FIEL) |
|---|---:|---|---|---|
| RM-01 | 1 | FIEL | “Formulário contém código, tipo, valor, validade e limite” | — |
| RM-01 | 2 | FIEL | “Exatamente um cupom com os cinco campos; usos 0 e nenhuma linha de aplicação” | — |
| RM-01 | 3 | PARCIAL | “Tipo fixo e valor 101 centavos persistidos; não aplicar teto percentual de 100” | CT-02: “Então existe exatamente um NOVO no contexto corrente com esses cinco campos e usos 0”; “E não existe linha de aplicação para NOVO”. Omite unicidade, demais campos e ausência de consumo/trilha. |
| RM-01 | 4 | FIEL | “Valores originais, identidade única, nenhum erro de duplicidade e nenhum uso criado” | — |
| RM-02 | 1 | PARCIAL | “Usos 1 e uma linha de uso anterior identificável” | CT-03: “Então o mesmo cupom tem os cinco novos valores persistidos”; “E usos permanece 1 e a única linha de uso anterior permanece idêntica”. Afirma somente preparação. |
| RM-02 | 2 | FIEL | “Mesmo registro com os cinco novos valores; usos 1 e linha anterior idêntica” | — |
| RM-02 | 3 | PARCIAL | “Valor inteiro em centavos, sem transformar fixo em percentual nem aplicar teto de cem” | CT-50: “Então o schema representa tipo fixo, valor 101 centavos e permite salvar essa combinação”; “E o registro persistido tem tipo fixo e valor 101, sem aplicar teto percentual de cem”. Perde o valor exato determinado pelo CT. |
| RM-03 | 1 | PARCIAL | “Cada alvo está no estado descrito e OUTRO não tem usos” | CT-55: “Então o alvo deixa de existir no cadastro e na listagem”. Afirma preparação, sem a pós-condição de exclusão. |
| RM-03 | 2 | PARCIAL | “Cada alvo some do cadastro; OUTRO preserva campos e usos” | CT-55: “Então o alvo deixa de existir no cadastro e na listagem”; “E OUTRO preserva os cinco campos, organização, contador e linhas de uso”. Omite retirada da listagem e preservação explícita da organização/trilha do vizinho. |
| RM-04 | 1 | FIEL | “Erro no campo retirado; nenhuma criação ou alteração de campos, contador e trilha” | — |
| RM-04 | 2 | PARCIAL | “Nenhum terceiro tipo gravado; erro de tipo se submetido” | CT-09: “Então há erro de tipo, e nenhum cupom novo ou alteração de campos é persistido”; “E contador e trilha de aplicação permanecem iguais”. Omite preservação dos demais campos, contador e trilha. |
| RM-04 | 3 | PARCIAL | “Inválidos recusados no campo valor; controles válidos persistidos exatamente; sem consumo” | CT-11: “E se recusado há erro só em valor, nenhum novo cupom e nenhum campo, uso ou trilha alterado”. Não exige explicitamente preservação dos campos e da trilha. |
| RM-04 | 4 | PARCIAL | “Erro no campo correspondente, sem persistir coerção nem alterar contador/trilha” | CT-14: “E cadastro, contador e trilha permanecem iguais ao estado anterior”. Proibir coerção não exige preservar todo o cadastro. |
| RM-04 | 5 | PARCIAL | “Erro em codigo; só o original usa o código; campos, uso anterior e trilha de OUTRO preservados” | CT-18: “Então há erro em codigo e existe apenas o PROMO10 original com seus cinco campos”; “E usos e trilha do original não mudam”. Preserva explicitamente OUTRO, mas não todos os campos e efeitos do original. |
| RM-05 | 1 | PARCIAL | “Conjunto esperado da leitura comum contém somente ativos” | CT-45: “Então \<resultado>, e Globex está sempre ausente”; “E nenhum campo, contador ou linha de uso é alterado”. Omite isolamento e ausência de alterações. |
| RM-05 | 2 | PARCIAL | “Todos e somente os ativos aparecem uma vez; nenhum consumo ou alteração” | CT-45, resultado do exemplo ativo: “presente com código e tipo corretos”. Afirma composição e cardinalidade, sem exigir correção desses dados apresentados. |
| RM-05 | 3 | PARCIAL | “Cada verbo recusado; cadastro, contador e trilha intactos; retornar à lista continua possível” | CT-24: “Então a página alcançável mostra PROMO10 com código e tipo corretos sem novo redirecionamento à tela recusada”. Alcançar a lista afirma menos que conferir conteúdo e ausência do redirecionamento. |
| RM-05 | 4 | PARCIAL | “Infra recusado; master_global e admin aceitos conforme os Exemplos do CT” | CT-21: “Então \<resultado> e, se aceito, a operação produz os campos ou remoção solicitados”; “E se recusado não cria cupom, não muda os cinco campos, não remove PROMO10 nem altera contador/trilha”. Omite efeitos concretos e preservações. |
| RM-06 | 1 | PARCIAL | “Primeiro total 9000; um uso e uma linha” | CT-39: “Então o total é 9000 e o contador relido é exatamente 2”; “E há exatamente duas linhas de uso, preservada a anterior e criada só uma com cupom e autor atuais”. É preparação para esse resultado, concluído no passo seguinte; não é contradição temporal. |
| RM-06 | 2 | FIEL | “Total 9000, usos 2, duas linhas, anterior idêntica; autor A, não B, e instante da aplicação” | — |
| RM-07 | 1 | PARCIAL | “Código desconhecido/null/vazio não encontra cupom nem consome” | CT-29: “E na recusa PROMO10 continua com usos 0 e sem linha de aplicação”. “Nem consome” não exige explicitamente ausência de linha para essas recusas. |
| RM-08 | 1 | FIEL | “Instância antiga é recusada; contador e três linhas ficam iguais.” | — |
| RM-09 | 1 | FIEL | “sem persistir valor inválido. Alterações recusadas preservam estado anterior.” | — |
| RM-10 | 1 | PARCIAL | “Organizações distintas podem ter cada uma o código; original permanece intacto.” | CT-20: “Então \<resultado> e as identidades, organizações e cinco campos preexistentes permanecem corretos”; “E a tentativa não altera usos nem linhas de aplicação”. Preservar apenas o original não explicita preservar OUTRO e seus efeitos. |
| RM-11 | 1 | FIEL | “Cadastro, usos e trilha permanecem intactos.” | — |
| RM-12 | 1 | FIEL | “omitir autor ou passar null recusa a chamada sem total descontado, usos 0 e nenhuma linha de aplicação.” | — |

**Totais**

| Classe | Passos |
|---|---:|
| FIEL | 10 |
| PARCIAL | 16 |
| DIVERGENTE | 0 |
| SEM RESPALDO | 0 |
| ORIGEM ERRADA | 0 |
| **Total** | **26** |

**FIEL + PARCIAL: 100% (26/26).** FIEL isoladamente: **38,46%**. As divergências D1–D5 relatadas são entre observado e esperado; não constituem divergência documental do esperado.

**Cobertura por RQ**

“Coberta” indica existência de passo previsto que exercita a cláusula, sem afirmar execução ou cobertura integral.

| RQ | Situação | Evidência no roteiro |
|---|---|---|
| RQ-01 | coberta | RM-01: criação; RM-02: edição; RM-03: exclusão |
| RQ-02 | coberta | RM-01/2; RM-04/1; RM-09/1 |
| RQ-03 | coberta | RM-01/2–3; RM-04/2; RM-09/1 |
| RQ-04 | coberta | RM-01/2–3; RM-04/3–4; RM-09/1 |
| RQ-05 | coberta | RM-01/2; RM-02/2; RM-04/1 e 4 |
| RQ-06 | coberta | RM-01/2; RM-02/2; RM-09/1 |
| RQ-07 | coberta | RM-05/3–4; RM-11/1 |
| RQ-08 | coberta | RM-05/1–3; RM-11/1 |
| RQ-09 | coberta | RM-07/1 |
| RQ-10 | coberta | RM-08/1: cupom vencido |
| RQ-11 | coberta | RM-08/1: último uso e tentativa excedente |
| RQ-12 | coberta | RM-06/1–2: total descontado nos dois tipos |
| RQ-13 | coberta | RM-06/2; RM-08/1 |
| RQ-14 | coberta | RM-04/5; RM-10/1 |
| RQ-15 | coberta | RM-06/2: autor e instante; RM-12/1: autoria obrigatória |

**15 cobertas; 0 declaradas integralmente fora; 0 omitidas.** Há recortes excluídos com motivo, como concorrência, precisão e isolamento multi-tenant. Existem negativos de permissão: **RM-05/3–4 e RM-11/1**.

**Segurança e honestidade documental**

- Comando destrutivo sem aviso de banco descartável: **nenhum**. A preparação restringe os comandos à cópia descartável.
- Credencial aparentemente real: **nenhuma**. Os usuários usam `manual.example.test`; nenhuma senha foi transcrita.
- Incompatibilidade entre conferência e preenchimento: **nenhuma**. RM-01–05 têm resultados vazios; RM-06–12 têm resultados preenchidos.
- Contagem incompatível: **nenhuma**. São 12 RM, 7 conferidos, com 4 declarados conformes e 3 divergentes.

O roteiro parece derivado predominantemente da especificação. Mantém recusas exigidas pelos CT mesmo quando relata aceitação pelo app, e declara recortes sem execução. As fragilidades encontradas são reduções dos esperados e passos de preparação apresentados isoladamente. Esses indícios sustentam derivação documental, mas não comprovam o processo de autoria.