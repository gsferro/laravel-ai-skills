# Materialização de compras — V9

Oráculo exclusivo: `judges/conjunto-v9/conjunto.md`, lido integralmente. Seleção exploratória preregistrada: alçada estritamente acima do limite (igualdade quando literal), ausência de justificativa/retorno ao rascunho quando literais, envio, ordem das aprovações, histórico e mail do próximo aprovador quando literal. Endereços de API e montagem vêm do contrato público; suas expectativas não foram adotadas.

**Revisão técnica v2, ainda não executada.** V9 continua sem execução de controle. A sessão principal autorizou corrigir a mesma montagem após o controle v1 de H2 falhar com solicitante_id ausente. O materializador não executou aplicação, Artisan, Pest, browser, SMTP ou mutation. Os arquivos v2 aguardam congelamento pela sessão principal antes do primeiro controle de V9. A palavra materializada identifica tradução, não resultado ou cobertura aprovada. Os estados de execução no inventário abaixo referem-se à v2.

| Medida estrutural | Quantidade |
|---|---:|
| CT + CT-B inventariados | 61 |
| Selecionados integralmente | 11 |
| Selecionados parcialmente | 1 |
| Não selecionados | 49 |
| Linhas literais de Examples | 141 |
| Examples materializados (não executados) | 14 |
| Examples omitidos deste recorte | 127 |
| Casos únicos selecionados sem Examples | 5 |
| Casos Pest materializados após compartilhar CT sobre o mesmo Quando | 17 |
| Casos executados desta revisão v2 | 0 |

`runtime/tests/ExperimentoReal/V9/ComprasTest.php` usa o registro já existente de TenancyTestCase + RefreshDatabase em tests/Pest.php. O arnês, contrato, dependências e implementação não foram editados. Fixtures usam helpers existentes; papéis por tenant pelo PermissionRegistrar/model configurado e API do vendor. Gestor é vínculo do centro, sem papel gestor. Pessoas, e-mails, centros e tenants distintos conforme cada CT. Situação e histórico são montados por criar/enviar/aprovar/rejeitar reais, nunca por gravar situação à força.

Notification::fake impede I/O externo durante a montagem. Nos CT com oráculo de mail, uma nova fake depois da fixture abre a janela da ação medida. Capturas do preparo são descartadas. Fakes e consultas novas observam somente efeitos exigidos por esses CT; não certificam SMTP, fila ou atomicidade externa.

Recusas de negócio aceitam exclusivamente RuntimeException de classe exata, declarada pela API de montagem; não existe catch(Throwable), mensagem inventada ou aceitação de falha de banco/boot. TypeError/null e ArgumentCountError/omissão são barreiras tipadas separadas. Positivos elegíveis da mesma família (gestor na sua etapa, diretor depois do gestor e rejeição com Sem verba) estão materializados.

Limites efetivos de leitura: filesystem irrestrito, restrições contratuais, sem whitelist ou prova técnica de cegamento. A primeira chamada usou login padrão e carregou automaticamente o perfil PowerShell fora do contrato; as seguintes usam login:false. O contrato público foi retornado inteiro, expondo comportamento além de nomes/assinaturas/montagem: limitação de exposição registrada; os Então e Examples deste respectivo conjunto continuaram sendo o único oráculo. Leituras deliberadas: dois conjuntos, contrato público, tests/Pest.php, TestCase.php e TenancyTestCase.php, e APIs necessárias do vendor. Nenhum AGENTS/env/banco, código da feature, teste Gold/Kit/Exp, 00/01, catálogo/veredito ou conjunto adicional foi consultado. Os dois braços foram traduzidos na mesma sessão; não foi emprestado o oráculo rival.

Host Codex, família GPT-6; ultra solicitado; identificador exato do deployment não exposto. Não se mediram DDR, custo/tokens, equivalência de hosts ou detecção de mutantes.

Verificações executadas: php -l no próprio ComprasTest.php, sem erro de sintaxe; conferência estática por Python dos 61 IDs únicos, 141 linhas de Examples, 11 definições Pest e 17 casos parametrizados previstos. São verificações de tradução e sintaxe, sem bootstrap da aplicação e sem passagem alegada de testes.

## Correção técnica v2

Autorização da sessão principal antes do primeiro controle de V9. Novas leituras de resultado limitadas a D:/PROJECTS/SKILLS/laravel-ai-skills/experimentos/2026-10-09-projeto-real/execucao-mutantes/h2v3/control.log e resultado.json: H2 teve 30/30 erros SQL pelo solicitante ausente na fixture e nenhum mutante registrado. Não foram lidos outros mutantes, vereditos ou código da feature. A exposição à falha técnica do outro braço foi autorizada exclusivamente para a mesma montagem, sem empréstimo de seu oráculo.

v9Compra() passa a instanciar SolicitacaoCompra e montar a fixture com forceFill/save no mesmo ator literal S, acrescentando somente solicitante_id de S e tenant_id de A aos três campos existentes. Situação não é gravada à força; enviar/aprovar/rejeitar continuam transições reais. Cenários, valores, asserções, perguntas bloqueadas e notificações esperadas foram preservados.

A assinatura pública de AprovacaoPendente expõe as propriedades solicitacao e etapa; as APIs sent/contagens do NotificationFake e forceFill/save foram conferidas no contrato público/vendor, sem leitura da implementação da feature. Nenhuma expectativa de mail foi adicionada ou alterada.

A primeira tradução congelada em testes/comprasv1 e os logs originais foram preservados pela sessão principal e não foram editados nesta correção. Somente os dois ComprasTest.php e seus dois mapas foram editados. A v2 aguarda execução serializada pela sessão principal; nenhum teste aprovado é alegado.

Verificação da correção: php -l nos dois arquivos v2, sem erro de sintaxe. Comparação estática com o conteúdo capturado antes da edição confirmou alteração somente da função de montagem Compra() e do comentário de versão; todos os testes, datasets, asserções, helpers de notificação e demais funções permanecem idênticos. Nenhuma execução comportamental feita pelo materializador.

## Inventário completo de CT e CT-B

| ID | Seleção | Cenário literal | Tratamento |
|---|---|---|---|
| CT-01 | não selecionado | A correção do rascunho persiste o campo alterado | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-02 | não selecionado | Editar fora do rascunho preserva os três campos | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-03 | não selecionado | Outra identidade não edita o rascunho de S | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-04 | não selecionado | A edição apresenta os dados do rascunho ao dono | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-05 | não selecionado | Salvar pelo componente grava a correção | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-06 | não selecionado | Excluir rascunho retira a solicitação das consultas | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-07 | não selecionado | Excluir fora do rascunho não apaga a solicitação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-08 | não selecionado | Outra identidade não exclui o rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-09 | não selecionado | Editar ID ausente não recria solicitação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-10 | não selecionado | Excluir ID ausente não toca outro agregado | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-11 | selecionado integral | Primeiro envio chega ao gestor nas duas faixas | Compartilha duas execuções futuras com CT-49; 3000.00 e 6000.00 começam no gestor, conservando valor/centro e sem aprovação de D. |
| CT-12 | não selecionado | Enviar fora do rascunho não reinicia o fluxo | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-13 | não selecionado | Outra identidade não envia o rascunho de S | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-14 | não selecionado | Centro sem gestor conserva o rascunho e informa a recusa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-15 | não selecionado | Instância antiga não envia outra vez | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-16 | selecionado integral | O gestor decide sua etapa corrente | Compra 3000.00 com alçada efetiva 5000.00: aprovação final do gestor, sem pendência de diretor/mail. |
| CT-17 | não selecionado | Gestor não aprova fora da sua etapa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-18 | não selecionado | Aprovar exige a identidade do gestor do centro | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-19 | não selecionado | Solicitante que também é gestor decide a própria etapa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-20 | selecionado integral | Rejeitar a etapa corrente devolve para correção | Duas etapas rejeitam com Sem verba; campos originais e autoria/justificativa, sem mail nomeado. |
| CT-21 | não selecionado | Sem etapa pendente, rejeitar não altera o agregado | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-22 | não selecionado | Cada verbo de rejeição exige o aprovador corrente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-23 | selecionado integral | Corrigir o centro e reenviar usa o gestor atual | Correção para Monitor/C2 após rejeição real, próximo gestor H e somente seu mail do reenvio. |
| CT-24 | selecionado integral | Reenvio após rejeição de diretor não reutiliza o aval antigo | Após rejeição real de D e correção, novo envio começa em aguardando_gestor com Monitor/6000.00. Não foi acrescentada asserção de retenção do histórico ou mail ausente nesse CT. |
| CT-25 | não selecionado | Corrigir não se transfere ao aprovador que rejeitou | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-26 | selecionado parcial | Diretor não aprova antes do gestor nem depois do encerramento | Somente aguardando_gestor: D tenta aprovar antes de G. Rascunho/aprovada/cancelada omitidos. |
| CT-27 | não selecionado | Diretor não rejeita solicitação já aprovada | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-28 | não selecionado | O solicitante cancela em cada etapa de trânsito | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-29 | não selecionado | Cancelar fora do trânsito conserva a situação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-30 | não selecionado | Aprovador e terceiro não cancelam solicitação de S | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-31 | não selecionado | Decisão carregada antes do cancelamento não desfaz o estado persistido | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-32 | não selecionado | panel_user não grava administração fora da tela | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-33 | não selecionado | Componente não permite panel_user mudar o gestor | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-34 | não selecionado | Affordance segue identidade e situação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-35 | não selecionado | Rejeitar pelo componente devolve para correção | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-36 | não selecionado | Confirmar envio/cancelamento grava a transição correspondente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-37 | não selecionado | Transições sobre ID removido não produzem efeitos em outro registro | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-38 | não selecionado | Criação válida fora do componente persiste os dados de S | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-39 | não selecionado | A tela de criação oferece os três campos ao solicitante | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-40 | não selecionado | Criar pelo componente grava todos os dados válidos | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-41 | selecionado integral | A fronteira literal decide o destino após o gestor | Três bordas, configuração efetiva 5000.00 e precondição da chave de ambiente de teste ausente, sem override neste CT. Não se acrescentou oráculo de notificações. |
| CT-42 | selecionado integral | O diretor encerra a segunda etapa depois do gestor | Aprovação real de G seguida da de D; valor, duas decisões em ordem, sem pendência/mail. |
| CT-43 | selecionado integral | A mudança de configuração muda a faixa que exige diretor | Override deliberado 7000.00, compra 6000.00, aprovação final de G sem pendência/mail. |
| CT-44 | selecionado integral | Ausência de justificativa é recusada fora do formulário | Duas linhas omitem literalmente o argumento justificativa. ArgumentCountError é barreira da assinatura pública; não substitui teste de string vazia/null/espaços e não demonstra validação de conteúdo. |
| CT-45 | não selecionado | O formulário de rejeição não grava sem justificativa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-46 | não selecionado | A listagem apresenta a situação da solicitação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-47 | não selecionado | O detalhe apresenta a situação da solicitação | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-48 | não selecionado | O detalhe atribui as duas etapas aos respectivos aprovadores | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-49 | selecionado integral | Enviar notifica somente o gestor pelo canal e-mail | Compartilha duas execuções futuras com CT-11; um aviso dessa solicitação no canal mail a G, zero a S/H/D. Não se acrescentou campo etapa como expectativa. |
| CT-50 | selecionado integral | O aval do gestor notifica todos os diretores da organização | D1 e D1+D2 de A, X apenas de B; um mail dessa compra por diretor de A, zero a S/G/X. Sem requisito adicional de ordem, papéis acumulados ou cardinalidade zero. |
| CT-51 | não selecionado | Retry de envio mantém uma só notificação ao gestor | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-52 | não selecionado | CRUD administrativo válido funciona fora do formulário | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-53 | não selecionado | Administrador visita os formulários de centro | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-54 | não selecionado | Confirmar CRUD de centro no painel persiste o efeito | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-55 | não selecionado | Diretor além do primeiro decide a etapa corrente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-56 | não selecionado | Snapshot de outro diretor não decide etapa já resolvida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-57 | não selecionado | Aprovação única é visível antes ou ao final do fluxo | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-58 | não selecionado | Rejeição apresentada conserva autor, instante e justificativa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-59 | não selecionado | Chamada direta sem gestor conserva rascunho e registra recusa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-60 | não selecionado | Aprovar pelo componente grava decisão e destino | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-61 | não selecionado | Diretor rejeita com justificativa válida pelo componente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |

## Direções bloqueadas pelas perguntas do próprio conjunto

Nenhum CT positivo fechado foi descartado por uma pergunta ampla: os recortes abaixo continuam indecididos, sem cenário ou resposta inventada.

| Pergunta | Direção não materializada |
|---|---|
| Q?1 | Tetos/domínios, escala/arredondamento, criação/edição com entradas inválidas não especificadas. |
| Q?2 | Teto e tratamento de espaços/bordas/null; ausência literal do argumento está em CT-44. String vazia ou whitespace não foram emprestados de H2. |
| Q?3 | S=D e G=D; S=G dado por A-09 não foi reaberto, apenas seu CT-19 não entrou neste recorte. |
| Q?4 | Zero diretores e saída depois do gestor; as linhas 1/N de CT-50 estão materializadas. |
| Q?5 | Recorte de leitura atual/histórica, cross-tenant de consulta e discriminante nulo. CT de componente com acesso autorizado estão não selecionados por camada. |
| Q?6 | Link/destino do e-mail; nenhuma promessa foi tomada do contrato de montagem. |
| Q?7 | Retry da criação e sua identidade; não foi criada deduplicação. |
| Q?8 | Exclusão física/soft delete; os CT de exclusão não entraram neste recorte. |

## Asserções literais e todas as linhas de Examples

### CT-01 — A correção do rascunho persiste o campo alterado

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova encontra <campo> igual a <novo>, mantendo S e rascunho
```

Cabeçalho literal: `| campo | novo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| descrição \| Monitor com acento ç e emoji 🛒 \| texto \|` | omitida deste recorte | omitida |
| E02 | `\| valor \| 3000.01 \| decimal \|` | omitida deste recorte | omitida |
| E03 | `\| centro \| C2 \| outro centro da mesma organização \|` | omitida deste recorte | omitida |
| E04 | `\| descrição \| Notebook \| edição sem alteração \|` | omitida deste recorte | omitida |

### CT-02 — Editar fora do rascunho preserva os três campos

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a edição é recusada e a consulta nova conserva "Notebook", "3000.00", C1, situação e histórico; G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| trânsito 1 \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| trânsito 2 \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| terminal \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| sem reabertura no escopo \|` | omitida deste recorte | omitida |

### CT-03 — Outra identidade não edita o rascunho de S

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a edição é recusada e a consulta conserva os três campos, rascunho e histórico; G/D não recebem e-mail
```

Cabeçalho literal: `| ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| U \| outro solicitante \|` | omitida deste recorte | omitida |
| E02 | `\| G \| gestor sem posse \|` | omitida deste recorte | omitida |
| E03 | `\| D \| diretor sem posse \|` | omitida deste recorte | omitida |

### CT-04 — A edição apresenta os dados do rascunho ao dono

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o formulário apresenta "Notebook", "3000.00" e C1, com ação de salvar disponível
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-05 — Salvar pelo componente grava a correção

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova contém "Monitor", "3000.01", C2, solicitante S e rascunho
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-06 — Excluir rascunho retira a solicitação das consultas

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta normal não encontra a solicitação e G/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-07 — Excluir fora do rascunho não apaga a solicitação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; a consulta nova encontra a mesma situação, descrição, valor, centro e histórico; G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| trânsito 1 \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| trânsito 2 \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| terminal \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| sem reabertura \|` | omitida deste recorte | omitida |

### CT-08 — Outra identidade não exclui o rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; a solicitação continua em rascunho com os mesmos campos/histórico; G/D não recebem e-mail
```

Cabeçalho literal: `| ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| U \| outro solicitante \|` | omitida deste recorte | omitida |
| E02 | `\| G \| gestor \|` | omitida deste recorte | omitida |
| E03 | `\| D \| diretor \|` | omitida deste recorte | omitida |

### CT-09 — Editar ID ausente não recria solicitação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; o ID continua ausente, V conserva Notebook/3000.00/C1, rascunho e histórico, não surgem decisões para o alvo e G/D não recebem e-mail
```

Cabeçalho literal: `| alvo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| removido por S em rascunho \| excluído \|` | omitida deste recorte | omitida |
| E02 | `\| nunca existente \| inexistente \|` | omitida deste recorte | omitida |

### CT-10 — Excluir ID ausente não toca outro agregado

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então V continua alcançável com os mesmos campos/histórico, o alvo segue ausente, não surgem decisões para ele e G/D não recebem e-mail
```

Cabeçalho literal: `| alvo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| removido por S em rascunho \| segunda exclusão \|` | omitida deste recorte | omitida |
| E02 | `\| nunca existente \| inexistente \|` | omitida deste recorte | omitida |

### CT-11 — Primeiro envio chega ao gestor nas duas faixas

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aguardando_gestor com o mesmo valor/centro, sem aprovação atribuída a D
```

Cabeçalho literal: `| valor | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 3000.00 \| abaixo do limite literal \|` | materializada | não executada |
| E02 | `\| 6000.00 \| acima do limite literal \|` | materializada | não executada |

### CT-12 — Enviar fora do rascunho não reinicia o fluxo

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o envio é recusado; situação/campos persistidos e histórico ficam iguais; G/D não recebem novo e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| envio repetido \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| próxima etapa \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| terminal \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| sem reabertura \|` | omitida deste recorte | omitida |

### CT-13 — Outra identidade não envia o rascunho de S

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o envio é recusado; a consulta mantém rascunho e os campos/histórico; G/D não recebem e-mail
```

Cabeçalho literal: `| ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| U \| outro solicitante \|` | omitida deste recorte | omitida |
| E02 | `\| G \| gestor \|` | omitida deste recorte | omitida |
| E03 | `\| D \| diretor \|` | omitida deste recorte | omitida |

### CT-14 — Centro sem gestor conserva o rascunho e informa a recusa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então continua em rascunho com campos/histórico iguais, há mensagem visível de recusa e warning correspondente à tentativa de envio dessa solicitação sem gestor, e S/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-15 — Instância antiga não envia outra vez

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova continua aguardando_gestor com campos/histórico iguais e G/D não recebem e-mail adicional
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-16 — O gestor decide sua etapa corrente

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aprovada com exatamente uma decisão de aprovação da etapa de gestor atribuída a G, sem etapa pendente de diretor e sem e-mail para S/G/D
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-17 — Gestor não aprova fora da sua etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| antes do envio \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| gestor já decidiu \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| terminal \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| sem reabertura \|` | omitida deste recorte | omitida |

### CT-18 — Aprovar exige a identidade do gestor do centro

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; permanece aguardando_gestor com campos/histórico iguais; G/D não recebem e-mail
```

Cabeçalho literal: `| ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| S \| dono não gestor \|` | omitida deste recorte | omitida |
| E02 | `\| H \| gestor de outro centro \|` | omitida deste recorte | omitida |
| E03 | `\| D \| diretor antecipado \|` | omitida deste recorte | omitida |
| E04 | `\| U \| terceiro \|` | omitida deste recorte | omitida |

### CT-19 — Solicitante que também é gestor decide a própria etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aprovada com exatamente uma decisão de aprovação da etapa de gestor atribuída a S, sem etapa pendente de diretor e sem e-mail para S/D
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-20 — Rejeitar a etapa corrente devolve para correção

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta mostra rascunho, conserva Notebook/6000.00/C1 e registra rejeição de <ator> com "Sem verba"; S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| G \| gestor \|` | materializada | não executada |
| E02 | `\| aguardando_diretor \| D \| diretor por A-07 \|` | materializada | não executada |

### CT-21 — Sem etapa pendente, rejeitar não altera o agregado

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; situação/campos persistidos e histórico ficam iguais; S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| G \| sem etapa / gestor \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho \| D \| sem etapa / diretor \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| G \| terminal / gestor \|` | omitida deste recorte | omitida |
| E04 | `\| aprovada \| D \| terminal / diretor \|` | omitida deste recorte | omitida |
| E05 | `\| cancelada \| G \| cancelada / gestor \|` | omitida deste recorte | omitida |
| E06 | `\| cancelada \| D \| cancelada / diretor \|` | omitida deste recorte | omitida |

### CT-22 — Cada verbo de rejeição exige o aprovador corrente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; situação/campos e histórico permanecem iguais; S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| S \| dono não gestor \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| U \| terceiro \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| H \| gestor de outro centro, sem poder rejeitar C1 \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_gestor \| D \| diretor antecipado \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| S \| dono não diretor \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_diretor \| U \| terceiro \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_diretor \| G \| anterior sem papel diretor \|` | omitida deste recorte | omitida |

### CT-23 — Corrigir o centro e reenviar usa o gestor atual

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aguardando_gestor, Monitor e C2, e o identificador do gestor da etapa corrente é H, não G; H recebe exatamente um aviso mail dessa solicitação pela nova etapa e G/S/D não recebem aviso dessa ação
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-24 — Reenvio após rejeição de diretor não reutiliza o aval antigo

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aguardando_gestor, Monitor e 6000.00; o aval antigo de G não a deixa em aguardando_diretor nem aprovada
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-25 — Corrigir não se transfere ao aprovador que rejeitou

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; a consulta mantém Notebook, rascunho e histórico da rejeição; G/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-26 — Diretor não aprova antes do gestor nem depois do encerramento

Seleção: **selecionado parcial**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| antes do envio \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| gestor primeiro \|` | materializada | não executada |
| E03 | `\| aprovada \| terminal final \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| sem reabertura \|` | omitida deste recorte | omitida |

### CT-27 — Diretor não rejeita solicitação já aprovada

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; a consulta nova continua aprovada com os mesmos campos/histórico; S/G/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-28 — O solicitante cancela em cada etapa de trânsito

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra cancelada com os mesmos campos/histórico e S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| antes do gestor \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| antes da aprovação final \|` | omitida deste recorte | omitida |

### CT-29 — Cancelar fora do trânsito conserva a situação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; situação/campos persistidos e histórico permanecem iguais; S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| A-06 usa excluir \|` | omitida deste recorte | omitida |
| E02 | `\| aprovada \| aprovação final \|` | omitida deste recorte | omitida |
| E03 | `\| cancelada \| cancelamento repetido \|` | omitida deste recorte | omitida |

### CT-30 — Aprovador e terceiro não cancelam solicitação de S

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; a consulta mantém situação/campos e histórico; S/G/D não recebem e-mail
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| G \| gestor \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| D \| diretor \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| U \| terceiro \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| G \| anterior \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| D \| corrente \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_diretor \| U \| terceiro \|` | omitida deste recorte | omitida |

### CT-31 — Decisão carregada antes do cancelamento não desfaz o estado persistido

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; consulta nova continua cancelada com os mesmos campos/histórico; S/G/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-32 — panel_user não grava administração fora da tela

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; C1 conserva nome/gestor G, nenhum centro adicional é criado ou removido e a solicitação conserva C1 e os campos
```

Cabeçalho literal: `| operação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| criar centro novo \| create administrativo \|` | omitida deste recorte | omitida |
| E02 | `\| editar gestor de C1 para H \| escalada no edit \|` | omitida deste recorte | omitida |
| E03 | `\| excluir C1 \| delete administrativo \|` | omitida deste recorte | omitida |

### CT-33 — Componente não permite panel_user mudar o gestor

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então acesso/gravação é recusado; consulta nova mantém Tecnologia e G, sem centro adicional
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-34 — Affordance segue identidade e situação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a ação <ação> está <visibilidade> para o registro
```

Cabeçalho literal: `| situação | ator | ação | visibilidade | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| S \| editar \| visível \| dono/rascunho \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho \| S \| excluir \| visível \| dono/rascunho \|` | omitida deste recorte | omitida |
| E03 | `\| rascunho \| S \| enviar \| visível \| dono/rascunho \|` | omitida deste recorte | omitida |
| E04 | `\| rascunho \| G \| editar \| oculta \| sem posse \|` | omitida deste recorte | omitida |
| E05 | `\| rascunho \| G \| excluir \| oculta \| sem posse \|` | omitida deste recorte | omitida |
| E06 | `\| rascunho \| G \| enviar \| oculta \| sem posse \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_gestor \| G \| aprovar \| visível \| corrente \|` | omitida deste recorte | omitida |
| E08 | `\| aguardando_gestor \| G \| rejeitar \| visível \| corrente \|` | omitida deste recorte | omitida |
| E09 | `\| aguardando_gestor \| S \| aprovar \| oculta \| dono não gestor \|` | omitida deste recorte | omitida |
| E10 | `\| aguardando_gestor \| S \| rejeitar \| oculta \| dono não gestor \|` | omitida deste recorte | omitida |
| E11 | `\| aguardando_gestor \| S \| cancelar \| visível \| dono/trânsito 1 \|` | omitida deste recorte | omitida |
| E12 | `\| aguardando_gestor \| D \| cancelar \| oculta \| outro ator \|` | omitida deste recorte | omitida |
| E13 | `\| aguardando_diretor \| S \| cancelar \| visível \| dono/trânsito 2 \|` | omitida deste recorte | omitida |
| E14 | `\| aguardando_diretor \| D \| rejeitar \| visível \| A-07 \|` | omitida deste recorte | omitida |
| E15 | `\| aguardando_diretor \| G \| rejeitar \| oculta \| participante anterior sem papel diretor \|` | omitida deste recorte | omitida |
| E16 | `\| aprovada \| S \| editar \| oculta \| terminal \|` | omitida deste recorte | omitida |
| E17 | `\| aprovada \| S \| excluir \| oculta \| terminal \|` | omitida deste recorte | omitida |
| E18 | `\| aprovada \| S \| cancelar \| oculta \| terminal \|` | omitida deste recorte | omitida |
| E19 | `\| cancelada \| S \| enviar \| oculta \| sem reabertura \|` | omitida deste recorte | omitida |

### CT-35 — Rejeitar pelo componente devolve para correção

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então consulta nova mostra rascunho, Notebook/3000.00/C1 e rejeição de G com "Sem verba"; S/G/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-36 — Confirmar envio/cancelamento grava a transição correspondente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então consulta nova mostra <final> com descrição/valor/centro/solicitante originais, e os e-mails dessa confirmação satisfazem <avisos>, sem aviso para S/D/H
```

Cabeçalho literal: `| inicial | ação | final | avisos | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| enviar \| aguardando_gestor \| G recebe exatamente um mail dessa solicitação \| envio \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| cancelar \| cancelada \| G não recebe aviso \| etapa 1 \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| cancelar \| cancelada \| G não recebe aviso \| etapa 2 \|` | omitida deste recorte | omitida |

### CT-37 — Transições sobre ID removido não produzem efeitos em outro registro

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada; alvo continua ausente, V conserva situação/campos/histórico, nenhuma decisão é criada para o alvo e G/D não recebem e-mail
```

Cabeçalho literal: `| operação | situação_V | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| enviar \| rascunho \| S \| V seria enviada a G \|` | omitida deste recorte | omitida |
| E02 | `\| aprovar como gestor \| aguardando_gestor \| G \| V de 3000.00 seria aprovada com limite 5000.00 \|` | omitida deste recorte | omitida |
| E03 | `\| rejeitar como gestor com Sem verba \| aguardando_gestor \| G \| V voltaria ao rascunho com rejeição \|` | omitida deste recorte | omitida |
| E04 | `\| rejeitar como diretor com Sem verba \| aguardando_diretor \| D \| V voltaria ao rascunho com rejeição \|` | omitida deste recorte | omitida |
| E05 | `\| cancelar \| aguardando_gestor \| S \| V seria cancelada \|` | omitida deste recorte | omitida |

### CT-38 — Criação válida fora do componente persiste os dados de S

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então uma consulta nova encontra a solicitação criada com solicitante S, Notebook, 3000.00, C1 e rascunho
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-39 — A tela de criação oferece os três campos ao solicitante

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o formulário apresenta descrição, valor e centro de custo, com a operação de criar disponível
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-40 — Criar pelo componente grava todos os dados válidos

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova encontra a solicitação criada com solicitante S, Notebook, 3000.00, C1 e rascunho
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-41 — A fronteira literal decide o destino após o gestor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra <destino>, conserva <valor> e registra exatamente uma aprovação de gestor por G; a etapa pendente de diretor é <pendência>
```

Cabeçalho literal: `| valor | destino | pendência | # borda |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 4999.99 \| aprovada \| ausente \| borda−0.01 \|` | materializada | não executada |
| E02 | `\| 5000.00 \| aprovada \| ausente \| borda literal \|` | materializada | não executada |
| E03 | `\| 5000.01 \| aguardando_diretor \| presente \| borda+0.01 \|` | materializada | não executada |

### CT-42 — O diretor encerra a segunda etapa depois do gestor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aprovada, conserva 6000.00 e contém uma aprovação de gestor por G seguida de uma aprovação de diretor por D, sem etapa pendente e sem e-mail para S/G/D
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-43 — A mudança de configuração muda a faixa que exige diretor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra aprovada com aprovação de gestor por G, sem etapa pendente de diretor e sem e-mail para S/G/D
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-44 — Ausência de justificativa é recusada fora do formulário

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a rejeição é recusada; situação/campos persistidos e histórico continuam iguais, sem nova decisão de rejeição e sem e-mail para S/G/D
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| G \| ausência na etapa de gestor \|` | materializada | não executada |
| E02 | `\| aguardando_diretor \| D \| ausência na etapa de diretor \|` | materializada | não executada |

### CT-45 — O formulário de rejeição não grava sem justificativa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o formulário indica falta de justificativa, situação/campos persistidos e histórico continuam iguais, sem nova rejeição e sem e-mail para S/G/D
```

Cabeçalho literal: `| situação | ator | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| G \| formulário/gestor \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| D \| formulário/diretor \|` | omitida deste recorte | omitida |

### CT-46 — A listagem apresenta a situação da solicitação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a linha dessa solicitação apresenta o status atual <situação>, sem substituí-lo pelo de outra etapa
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| estado inicial \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| primeira etapa \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| segunda etapa \|` | omitida deste recorte | omitida |
| E04 | `\| aprovada \| aprovação final \|` | omitida deste recorte | omitida |
| E05 | `\| cancelada \| cancelamento \|` | omitida deste recorte | omitida |

### CT-47 — O detalhe apresenta a situação da solicitação

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o detalhe dessa solicitação apresenta o status atual <situação>, sem substituí-lo pelo de outra etapa
```

Cabeçalho literal: `| situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| estado inicial \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| primeira etapa \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| segunda etapa \|` | omitida deste recorte | omitida |
| E04 | `\| aprovada \| aprovação final \|` | omitida deste recorte | omitida |
| E05 | `\| cancelada \| cancelamento \|` | omitida deste recorte | omitida |

### CT-48 — O detalhe atribui as duas etapas aos respectivos aprovadores

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico dessa solicitação apresenta G na aprovação histórica de gestor e D na aprovação de diretor, com ambas as etapas, sem atribuir a mesma pessoa às duas e sem atribuir a H uma aprovação que ele não decidiu
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-49 — Enviar notifica somente o gestor pelo canal e-mail

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então consulta nova mostra aguardando_gestor e G recebe exatamente uma notificação dessa solicitação pelo canal mail; S/H/D não recebem aviso dessa etapa
```

Cabeçalho literal: `| valor | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 3000.00 \| abaixo do limite \|` | materializada | não executada |
| E02 | `\| 6000.00 \| acima do limite, ainda gestor primeiro \|` | materializada | não executada |

### CT-50 — O aval do gestor notifica todos os diretores da organização

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então consulta nova mostra aguardando_diretor e cada usuário de <diretores_A> recebe exatamente uma notificação dessa solicitação pelo canal mail; S/G/X não recebem aviso dessa etapa
```

Cabeçalho literal: `| diretores_A | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| D1 \| cardinalidade 1 \|` | materializada | não executada |
| E02 | `\| D1 e D2 \| cardinalidade N \|` | materializada | não executada |

### CT-51 — Retry de envio mantém uma só notificação ao gestor

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova continua aguardando_gestor com campos/histórico iguais, G mantém exatamente um aviso mail dessa solicitação no total e S/H/D continuam sem aviso
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-52 — CRUD administrativo válido funciona fora do formulário

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova satisfaz <resultado>
```

Cabeçalho literal: `| preparo | operação | dados | resultado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| nenhum centro Tecnologia cadastrado \| criar \| nome Tecnologia e gestor G \| existe centro Tecnologia com gestor G pertencente a T \| criação \|` | omitida deste recorte | omitida |
| E02 | `\| centro Tecnologia com gestor G pertencente a T \| editar \| nome Infra e gestor H \| o mesmo centro tem nome Infra, gestor H e continua pertencendo a T \| correção \|` | omitida deste recorte | omitida |
| E03 | `\| centro Tecnologia com gestor G pertencente a T \| excluir \| ID desse centro \| esse centro não aparece na consulta normal e Estoque permanece com gestor G em T \| exclusão \|` | omitida deste recorte | omitida |

### CT-53 — Administrador visita os formulários de centro

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então encontra campos de nome e gestor e a confirmação da operação, com <conteúdo>
```

Cabeçalho literal: `| preparo | operação | conteúdo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| centro ainda não criado \| criar \| controles disponíveis para informar nome e gestor \| criação \|` | omitida deste recorte | omitida |
| E02 | `\| centro Tecnologia com gestor G em T \| editar \| nome Tecnologia e gestor G carregados \| edição \|` | omitida deste recorte | omitida |

### CT-54 — Confirmar CRUD de centro no painel persiste o efeito

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova satisfaz <resultado>
```

Cabeçalho literal: `| preparo | operação | dados | resultado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| nenhum centro Tecnologia cadastrado \| criar \| nome Tecnologia e gestor G \| existe centro Tecnologia com gestor G pertencente a T \| criação \|` | omitida deste recorte | omitida |
| E02 | `\| centro Tecnologia com gestor G pertencente a T \| editar \| nome Infra e gestor H \| o mesmo centro tem nome Infra, gestor H e continua pertencendo a T \| edição \|` | omitida deste recorte | omitida |
| E03 | `\| centro Tecnologia com gestor G pertencente a T \| excluir \| ID desse centro \| esse centro não aparece na consulta normal e Estoque permanece com gestor G em T \| exclusão \|` | omitida deste recorte | omitida |

### CT-55 — Diretor além do primeiro decide a etapa corrente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra <final>, preserva os campos da compra e a aprovação de G, grava exatamente uma decisão da etapa diretor de autoria D2 com <conteúdo>, não grava decisão de D1 e não envia e-mail a S/G/D1/D2
```

Cabeçalho literal: `| operação | final | conteúdo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aprovar como diretor \| aprovada \| aprovação \| elegibilidade da segunda pessoa \|` | omitida deste recorte | omitida |
| E02 | `\| rejeitar como diretor \| rascunho \| rejeição com Sem verba \| rejeição elegível da segunda pessoa \|` | omitida deste recorte | omitida |

### CT-56 — Snapshot de outro diretor não decide etapa já resolvida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada, a consulta permanece em <final> com campos/histórico capturados, conserva apenas a decisão de diretor de D1 sem decisão de D2 e S/G/D1/D2 não recebem e-mail dessa tentativa
```

Cabeçalho literal: `| primeira_decisão | final | segunda_decisão | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aprovar como diretor \| aprovada \| aprovar como diretor \| nova aprovação após aprovação \|` | omitida deste recorte | omitida |
| E02 | `\| aprovar como diretor \| aprovada \| rejeitar como diretor \| nova rejeição após aprovação \|` | omitida deste recorte | omitida |
| E03 | `\| rejeitar como diretor com Sem verba \| rascunho \| aprovar como diretor \| nova aprovação após devolução \|` | omitida deste recorte | omitida |
| E04 | `\| rejeitar como diretor com Sem verba \| rascunho \| rejeitar como diretor \| nova rejeição após devolução \|` | omitida deste recorte | omitida |

### CT-57 — Aprovação única é visível antes ou ao final do fluxo

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico apresenta G como autor da aprovação da etapa gestor dessa solicitação e não inventa uma aprovação de diretor inexistente
```

Cabeçalho literal: `| valor | situação | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 6000.00 \| aguardando_diretor \| aprovação de gestor enquanto aguarda diretor \|` | omitida deste recorte | omitida |
| E02 | `\| 3000.00 \| aprovada \| aprovação final somente do gestor \|` | omitida deste recorte | omitida |

### CT-58 — Rejeição apresentada conserva autor, instante e justificativa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico da etapa <etapa> apresenta <ator>, Sem verba e o instante correspondente a 2026-10-09T15:30:00Z na apresentação configurada, e não omite nem substitui esses dados da decisão
```

Cabeçalho literal: `| ator | etapa | preparo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| G \| gestor \| envio real de S à etapa gestor \| devolução pelo gestor \|` | omitida deste recorte | omitida |
| E02 | `\| D \| diretor \| envio real de S e aprovação real de G acima da alçada \| devolução após aprovação real de G \|` | omitida deste recorte | omitida |

### CT-59 — Chamada direta sem gestor conserva rascunho e registra recusa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o envio é recusado, a consulta nova conserva rascunho e todos os campos/histórico capturados, não há etapa nem decisão nova de aprovação, há warning correspondente à tentativa sem gestor e S/D não recebem e-mail
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-60 — Aprovar pelo componente grava decisão e destino

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra <final>, conserva descrição/valor/centro/solicitante e apresenta <decisões>, com <avisos>
```

Cabeçalho literal: `| valor | inicial | ator | etapa | final | decisões | avisos | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 3000.00 \| aguardando_gestor \| G \| gestor \| aprovada \| exatamente uma aprovação de G e nenhuma de D \| nenhum mail para S/G/D \| aprovação final de gestor \|` | omitida deste recorte | omitida |
| E02 | `\| 6000.00 \| aguardando_gestor \| G \| gestor \| aguardando_diretor \| exatamente uma aprovação de G e nenhuma de D \| exatamente um mail a D dessa etapa e nenhum para S/G \| avanço ao diretor \|` | omitida deste recorte | omitida |
| E03 | `\| 6000.00 \| aguardando_diretor \| D \| diretor \| aprovada \| aprovação anterior de G e exatamente uma aprovação de D \| nenhum mail para S/G/D \| aprovação final de diretor \|` | omitida deste recorte | omitida |

### CT-61 — Diretor rejeita com justificativa válida pelo componente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova mostra rascunho com os campos originais, conserva histórico capturado e acrescenta rejeição da etapa diretor por D com Sem verba, sem aviso mail para S/G/D
```

Sem tabela de Examples; caso único omitido deste recorte.

