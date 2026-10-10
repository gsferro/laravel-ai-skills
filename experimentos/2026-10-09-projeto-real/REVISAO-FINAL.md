# Revisão final independente — calibração e evidências

Data: 2026-10-09. Revisor em contexto independente de manutenção; não é derivador, implementador nem juiz cego. Família GPT-6, esforço ultra solicitado; deployment exato não exposto. Aplicou-se a revisão Ponytail com achados concretos, sem quota. Nenhuma fonte, tradução, referência executável ou resultado foi corrigido por este revisor; a única escrita persistente é este relatório.

O filesystem e o shell permanecem irrestritos. As restrições foram contratuais, com seleção explícita de caminhos, `login:false` e Python `-B`: sem ambiente original demo-r8, `.env`, banco ou logs originais; sem PHP, Laravel, Artisan, Pest, servidor ou navegador. Foram lidas as alterações pertinentes das cinco skills, seus contratos e artefatos arquivados nesta rodada. Fontes oficiais de APIs fixadas por versão foram consultadas pela web. Fixtures Python foram temporárias e removidas. Esses controles não provam isolamento técnico de leitura.

## Achados e fechamento

**Nenhum P1/P2/P3 permanece aberto nos recortes conferidos.** Quatro achados adicionais foram comunicados à sessão principal, corrigidos por ela e relidos sem edição pelo revisor:

1. **RF-01 — P2, encerrado: formato integral ainda aplicado a perguntas parciais.** A feature-wiki mandava atualizar toda pergunta devolvida como `RQ-nn — aberta (Qn)`; técnicas da feature-test-design repetiam o formato integral, apesar da regra de cobertura parcial. A situação concreta é uma dúvida sobre o teto da justificativa suspender também sua obrigatoriedade literal. A correção agora preserva CT/passos determinados, identifica o recorte bloqueado e usa RQ inteira aberta somente quando toda a cláusula depende da resposta. Conferidos os trechos de entrevista, captura do 00, despacho do step 7 e a antiga formulação equivalente em `feature-wiki/SKILL.md:942`, além das referências obrigatórias de delegação, entrevista, template 00 e técnicas. Renumeração de Q e referências ao Estado formal já aberto não foram tratados como novos bloqueios.

2. **RF-02 — P3, encerrado: símbolo de API inexistente na referência.** `armadilhas-de-api.md` e o relatório histórico da referência v3 citavam `EnumStateCast::cast`. A [fonte oficial Filament 5.7.6](https://github.com/filamentphp/filament/blob/v5.7.6/packages/schemas/src/Components/StateCasts/EnumStateCast.php) define `get(mixed $state)`, que retorna o caso enum. A fonte atual cita `EnumStateCast::get`; `referencia-v3/CORRECAO.md` foi preservado e `referencia-v3/ERRATA.md` registra a correção factual separada. O patch e os hashes da referência não mudaram.

3. **RF-03 — P3, encerrado: tabela de dependências do README divergia dos metadados atuais.** O README raiz apresentava a tabela como `metadata.requires` vigente, mas mantinha as cinco versões anteriores e os mínimos FW 4.0.0/FTD 1.16.0/FQG 1.7.0. A sessão principal reconciliou as linhas 516–520. Uma conferência literal independente confirmou versão e expressão `requires` idênticas aos cinco SKILLs atuais. A menção histórica à renumeração dos steps em 4.0.0 foi preservada.

4. **RF-04 — P3, encerrado: sujeito invertido na descrição do mutante.** `VALIDADE-INSTRUMENTO.md:116` dizia que o operador enum “matou a tradução M4”. A leitura final confirma “foi morto pela tradução M4 e sobreviveu à K7”, coerente com os brutos e `RELATORIO.md:108`. Nenhum resultado, tradução ou operador mudou por essa correção documental.

Os RI-01/02 anteriores foram conferidos: rotas, aliases e checks `.claude` ficaram condicionados ao adaptador; autoria distinta/contexto novo e fechamento pela sessão principal continuam exigidos. Hook por padrões, prompt, restrição de escrita e hashes não são apresentados como prova de isolamento de leitura. O RI-03 foi conferido com o complemento RF-01 acima. A interpretação inicial de RI-04 precisava da triagem do operador; seu histórico foi preservado.

## Integridade e instrumentos

- ZIP baseline: **64 arquivos**, todos correspondentes aos hashes individuais da preparação; candidata: **71 arquivos**, mesma conferência integral. Os hashes dos ZIP e dos **15 instrumentos arquivados** conferem. Os tratamentos continuam FW 4.0.0/FTD 1.16.0 e FW 4.1.0/FTD 1.17.0. As fontes atuais FW 4.1.1/FTD 1.17.3 não representam outra derivação medida.
- Os quatro pares 04/05 correspondem aos hashes dos congelamentos. As cópias anônimas preservadas são as entradas auditadas. K7/M4 têm o erro histórico de metadado LF versus bytes CRLF explicitado; H2/V9 descrevem os bytes reais. Nenhum hash histórico foi rebatizado como correto.
- Traduções `cuponsv1`, `cuponsv2` e `comprasv1`: respectivamente **6, 7 e 4 arquivos** conferidos byte a byte. Referências v1/v2/v3: **41 arquivos integrais** de cada referência conferidos; o `.env.example` constante dos manifestos não foi aberto. A v2 altera somente modelo Cupom, contrato público e controles próprios; a v3 somente CupomResource.
- Self-checks de `audit_verdict` rejeitaram citações inventadas/IDs duplicados. A conferência dos quatro resultados primários e dos dois pareados usou cópias temporárias, confirmou 18 IDs ordenados, declarações Gherkin únicas, citações literais e hashes dos arquivos brutos/auditorias.
- Fixtures de `compare()` comprovaram que empate no total não esconde perda de um ID; `condensed()` recusa DETECTA sem citação literal. O `main()` executado somente com ROUND/JUDGES temporários rejeitou par secundário incompleto e arquivo bruto alterado, e manteve o secundário `post_hoc` separado do primário. Não foi executado contra os diretórios reais.
- Fixtures de `capture_reference_v2 --version 3` comprovaram cópia exata, preservação da v2, recusa de overwrite e rejeição de alteração adicional do modelo. Uma primeira fixture foi corrigida porque sua própria comparação ignorava a conversão de newline do Windows; a execução corrigida passou. Não houve subprocesso PHP.

## Julgamentos documentais preservados

| Resultado | Baseline | Candidata | Natureza |
|---|---:|---:|---|
| Cupons, primário | K7: 13/18; NCT 53 | M4: 14/18; NCT 47 | Juízes separados do protocolo original |
| Compras, primário | H2: 15/18; NCT 78 | V9: 12/18; NCT 61 | Juízes separados do protocolo original |
| Compras, pareado | H2: 16/18; NCT 78 | V9: 14/18; NCT 61 | Conferência secundária posterior por um juiz exposto aos dois conjuntos |

As contagens foram refeitas; o denominador continua **18**, sem quota de achados nem DDR ajustado. A literalidade das citações não prova equivalência semântica dos critérios:

| Item | Primário H2/V9 | Pareado H2/V9 | Limite concreto |
|---|---|---|---|
| E06 | DETECTA / NÃO DETECTA | DETECTA / DETECTA | H2 distingue conservar histórico de reutilizar aval; V9 primário exige retirar as aprovações anteriores. O pareado adota não reutilizar nos dois. |
| E08 | DETECTA / NÃO DETECTA | DETECTA / DETECTA | A-09 do oráculo permite solicitante também gestor. H2 primário aceita recusa do solicitante sem autoridade; V9 exige segregação irrestrita do catálogo. O pareado usa somente a primeira interpretação. |
| E12 | NÃO DETECTA / NÃO DETECTA | DETECTA / NÃO DETECTA | O catálogo diz alteração 4000→6000 após envio. Os primários exigem alteração em trânsito; o pareado aceita correção após rejeição/reenvio e outros valores que cruzam o limiar. Isso é mudança de interpretação, não resultado original corrigido. |

Os brutos primários são dados do instrumento original, não arbitragem de negócio. O pareado posterior informa sensibilidade ao juiz e não os substitui. Na interpretação pareada continuam perdas da candidata em E12/E15; portanto ela não estabelece não regressão do cenário 2.

## APIs, traduções e resultados já arquivados

A correção de `Http::fake`, callbacks afterCommit e limpeza de Carbon está apoiada nas fontes fixadas do Laravel 12.0.0: [Factory](https://github.com/laravel/framework/blob/v12.0.0/src/Illuminate/Http/Client/Factory.php), [manager de testes](https://github.com/laravel/framework/blob/v12.0.0/src/Illuminate/Foundation/Testing/DatabaseTransactionsManager.php) e [lifecycle](https://github.com/laravel/framework/blob/v12.0.0/src/Illuminate/Foundation/Testing/Concerns/InteractsWithTestCaseLifecycle.php). A versão de outro projeto exige conferência própria. A [documentação oficial do Pest](https://pestphp.com/docs/browser-testing) confirma paralelismo de browser, color scheme de `inDarkMode()` e `assertScript()`; não garante isolamento de workers, tema por classe ou aparência completa. [Mutation testing](https://pestphp.com/docs/mutation-testing) documenta cache/paralelismo: duração não é igualdade N × duração da suíte.

Na cadeia Filament 5.7.6, [options(enum)](https://github.com/filamentphp/filament/blob/v5.7.6/packages/forms/src/Components/Concerns/HasOptions.php) configura o enum; [Field](https://github.com/filamentphp/filament/blob/v5.7.6/packages/forms/src/Components/Field.php) instala o cast; [Get](https://github.com/filamentphp/filament/blob/v5.7.6/packages/schemas/src/Components/Utilities/Get.php) obtém estado convertido e seu helper enum aceita caso ou escalar. Isso sustenta a equivalência do primeiro `c1-negative-fixed-input` sobre v2: a comparação estrita enum/string continuava falsa e **não liberava −1**. Seus resultados verdes permanecem arquivados, mas não são sobrevivência válida de uma entrada defeituosa liberada.

O operador reparado `c1-negative-fixed-input-enum` é outro instrumento exploratório posterior. Nos resultados já completos `k7v3`/`m4v3`, os cinco operadores iniciais falham por assertions pertinentes em ambos os recortes; o operador enum retorna 0 no K7 e falha no M4 CT-07 em `assertHasFormErrors(['valor'])`, com **Component has no errors**. Não é falha de bootstrap. A ausência do negativo literal no CT-08 K7 continua ausência; não se emprestou CT-07 M4.

M4 mantém em CT-10/11/12 apenas retorno/desconto exigidos, sem importar os efeitos de K7. Cuponsv2 restringe a recusa ao campo `valor` e exige os demais campos sem erro. Os mapas de compras contêm **139 blocos de assertions literais** — 78 H2 e 61 V9 — presentes no conjunto correspondente. H2 testa vazio/whitespace/null/omissão conforme seus Examples; V9 CT-44 conserva omissão do argumento, sem importar o teste de string vazia. Essa diferença não deve desaparecer na síntese executável.

Foram lidos resultados e JUnit arquivados, sem reexecutá-los: controle v3 **32 casos/127 assertions**, controle independente enum **1/21**, Chromium K7 **2/8** e M4 **1/4**, todos verdes. Os CT-B continuam parciais: seleção real, unidade em labels associados ao campo e predicates DOM/JS; sem gravação. Os atributos visible/disabled/readOnly não certificam um fluxo completo de digitação/submit. O probe DOM/console é instrumentação diagnóstica separada, sem CT nem cobertura.

A v1 aceitou ator null e falhou no controle M4 CT-41; a v2 restaurou User obrigatório do 00. Falha do controle não vira morte de mutante. O primeiro controle H2 de compras (`h2v3`) tem **30 erros SQL NOT NULL solicitante_id**, exit 2 e **zero mutantes**; não produz detecção. A montagem foi encaminhada ao materializador original. Esse era o limite do primeiro fechamento; a conferência adicional abaixo cobre os resultados posteriores já arquivados.

## Conferência documental final e compras v2

A sessão principal autorizou a conferência posterior de `RELATORIO.md`, README raiz/central/da rodada, README e CHANGELOG afetados, `VALIDADE-INSTRUMENTO.md`, `resultado-executavel.json` e `integridade-final.json`. Não houve execução da aplicação pelo revisor. Os números e o alcance descritos nesses documentos conferem com os arquivos primários já arquivados.

`resultado-executavel.json` referencia corretamente o SHA do manifesto v3 e os SHA dos quatro resultados de braços e quatro controles adicionais. As contagens foram refeitas pelas listas de casos e assertions dos brutos; commands, exit codes, timeouts, hashes de origem/mutação e cada falha resumida também correspondem literalmente. Os JUnit de compras confirmam ausência de erros de bootstrap e as falhas abaixo:

| Tradução | Controle verde: casos/assertions | Operadores iniciais | Operador enum posterior |
|---|---:|---|---|
| K7 cupons v2 sobre referência v3 | 33/166 | 5 mortos por assertions pertinentes | Sobrevive à seleção |
| M4 cupons v2 sobre referência v3 | 29/103 | 5 mortos por assertions pertinentes | Morto pelo CT-07, campo `valor` |
| H2 compras v2 sobre referência v3 | 30/236 | Alçada: 1 falha; conteúdo vazio: 6 falhas | Não aplicável |
| V9 compras v2 sobre referência v3 | 17/145 | Alçada: 1 falha; conteúdo vazio: verde | Não aplicável |

Assim, a seleção inicial de sete operadores produz A 7/7 e B 6/7. Isso é um resultado físico do recorte traduzido, não MSI completo nem cobertura de todo o catálogo ou conjunto. A sobrevivência de conteúdo vazio no V9 pertence **somente à seleção executada**: CT-44 omite o argumento e verifica `ArgumentCountError`, enquanto CT-45 de formulário não foi materializado. O operador enum é exploratório posterior e separado; o primeiro operador ineficaz continua excluído da contagem de sobreviventes válidos.

A comparação PHP compras v1→v2 muda somente o comentário de versão e os helpers de criação de fixture: `new` + `forceFill` + `save`, com `tenant_id` e `solicitante_id` das pessoas/tenants já definidos pelo próprio braço. Assertions, Examples e ações reais de envio/aprovação/rejeição permaneceram iguais. Gold, contrato e implementação de negócio não foram alterados para resolver a montagem. Conferidos os quatro hashes de `comprasv2` e os dois do controle enum, completando **23 arquivos frozen** nas cinco traduções. Os mapas congelados registram o estado ainda não executado do materializador; as execuções posteriores estão nos resultados próprios, sem reescrever esse histórico.

A síntese documental foi reproduzida **exatamente** pelo comparador atual com cópias temporárias dos quatro conjuntos, quatro vereditos primários e dois pareados. Uma corrupção adicional da cópia arquivada secundária foi recusada com `Raw paired verdict archive mismatch`, sem produzir saída. O primário continua com perdas E06/E08/E15 em compras; o secundário continua posterior, com perdas E12/E15 e mudança de critério E12 explicitada. A gate primária calculada continua **false**: exige não regressão por ID e lacuna cega, DDR candidata de pelo menos 85% e NCT inferior ao dobro, nos dois cenários. As candidatas ficam em 14/18 e 12/18 e há regressão em compras; o pareado não substitui essa decisão.

Os **250 destinos de links locais** dos dez documentos de síntese conferem, excluídos blocos/inline code e anchors; não foi feita verificação de fragmentos. `integridade-final.json` registra v3 restaurada, 64/71 arquivos de tratamento e 42 do manifesto da implementação. O revisor conferiu os arquivos arquivados nos limites já descritos; não leu o runtime para repetir a prova de restauração. Integridade de bytes não comprova isolamento de leitura ou correção de negócio.

Foram lidos `regressoes-coletanea-final.json` (**45/45**, sem falhas/skips) e `regressoes-adicionais-final.json`/log (**13 testes, OK, exit 0**), executados pela sessão principal. Essas regressões não foram reexecutadas aqui. O artefato de validação adicional registra 15 instrumentos, 23 traduções, 11 scripts Python compilados, cinco TOML parseados e os links conferidos. Parsing não é carregamento nativo do host. A exposição do materializador ao contrato público inteiro e aos dois braços permanece expressa como limitação; não foi promovida a prova de cegamento.

## Limites do fechamento

Este relatório cobre o estado arquivado acima, as correções relidas e a conferência documental final autorizada. Não certifica resultados futuros. Não foram repetidos `python tests/run.py` ou unittest discovery por este revisor, pois podem chamar PHP; os checks gerais finais e a execução serial da aplicação foram realizados pela sessão principal, com os registros lidos acima.

Não medidos por esta revisão: nova derivação com as fontes 4.1.1/1.17.3, MSI completo, SMTP real, concorrência multiprocesso, variância, economia de tokens/custo, equivalência entre hosts ou carregamento nativo dos TOML. Resultados exploratórios selecionados e interpretação pareada posterior não ampliam essas provas.
