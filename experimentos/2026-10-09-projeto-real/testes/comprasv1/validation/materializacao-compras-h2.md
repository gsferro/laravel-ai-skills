# Materialização de compras — H2

Oráculo exclusivo: `judges/conjunto-h2/conjunto.md`, lido integralmente. Seleção exploratória preregistrada: alçada estritamente acima do limite (igualdade quando literal), ausência de justificativa/retorno ao rascunho quando literais, envio, ordem das aprovações, histórico e mail do próximo aprovador quando literal. Endereços de API e montagem vêm do contrato público; suas expectativas não foram adotadas.

**Nenhuma execução de aplicação, Artisan, Pest, browser, SMTP ou mutation nesta materialização.** Os arquivos aguardam congelamento pela sessão principal antes da primeira execução. A palavra materializada identifica tradução, não resultado ou cobertura aprovada.

| Medida estrutural | Quantidade |
|---|---:|
| CT + CT-B inventariados | 78 |
| Selecionados integralmente | 12 |
| Selecionados parcialmente | 1 |
| Não selecionados | 65 |
| Linhas literais de Examples | 207 |
| Examples materializados (não executados) | 28 |
| Examples omitidos deste recorte | 179 |
| Casos únicos selecionados sem Examples | 5 |
| Casos Pest materializados após compartilhar CT sobre o mesmo Quando | 30 |
| Casos executados | 0 |

`runtime/tests/ExperimentoReal/H2/ComprasTest.php` usa o registro já existente de TenancyTestCase + RefreshDatabase em tests/Pest.php. O arnês, contrato, dependências e implementação não foram editados. Fixtures usam helpers existentes; papéis por tenant pelo PermissionRegistrar/model configurado e API do vendor. Gestor é vínculo do centro, sem papel gestor. Pessoas, e-mails, centros e tenants distintos conforme cada CT. Situação e histórico são montados por criar/enviar/aprovar/rejeitar reais, nunca por gravar situação à força.

Notification::fake impede I/O externo durante a montagem. Nos CT com oráculo de mail, uma nova fake depois da fixture abre a janela da ação medida. Capturas do preparo são descartadas. Fakes e consultas novas observam somente efeitos exigidos por esses CT; não certificam SMTP, fila ou atomicidade externa.

Recusas de negócio aceitam exclusivamente RuntimeException de classe exata, declarada pela API de montagem; não existe catch(Throwable), mensagem inventada ou aceitação de falha de banco/boot. TypeError/null e ArgumentCountError/omissão são barreiras tipadas separadas. Positivos elegíveis da mesma família (gestor na sua etapa, diretor depois do gestor e rejeição com Sem verba) estão materializados.

Limites efetivos de leitura: filesystem irrestrito, restrições contratuais, sem whitelist ou prova técnica de cegamento. A primeira chamada usou login padrão e carregou automaticamente o perfil PowerShell fora do contrato; as seguintes usam login:false. O contrato público foi retornado inteiro, expondo comportamento além de nomes/assinaturas/montagem: limitação de exposição registrada; os Então e Examples deste respectivo conjunto continuaram sendo o único oráculo. Leituras deliberadas: dois conjuntos, contrato público, tests/Pest.php, TestCase.php e TenancyTestCase.php, e APIs necessárias do vendor. Nenhum AGENTS/env/banco, código da feature, teste Gold/Kit/Exp, 00/01, catálogo/veredito ou conjunto adicional foi consultado. Os dois braços foram traduzidos na mesma sessão; não foi emprestado o oráculo rival.

Host Codex, família GPT-6; ultra solicitado; identificador exato do deployment não exposto. Não se mediram DDR, custo/tokens, equivalência de hosts ou detecção de mutantes.

Verificações executadas: php -l no próprio ComprasTest.php, sem erro de sintaxe; conferência estática por Python dos 78 IDs únicos, 207 linhas de Examples, 12 definições Pest e 30 casos parametrizados previstos. São verificações de tradução e sintaxe, sem bootstrap da aplicação e sem passagem alegada de testes.

## Inventário completo de CT e CT-B

| ID | Seleção | Cenário literal | Tratamento |
|---|---|---|---|
| CT-01 | não selecionado | A criação conserva descrição, valor e centro escolhidos | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-02 | não selecionado | Um campo obrigatório inválido impede a criação fora da UI | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-03 | não selecionado | O formulário de criação grava os três campos do solicitante | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-04 | não selecionado | A rota de criação oferece os três dados obrigatórios | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-05 | não selecionado | O solicitante corrige cada campo decisivo em rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-06 | não selecionado | A obrigatoriedade também é aplicada na correção do rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-07 | não selecionado | O formulário edit grava a segunda compra e conserva a primeira do mesmo dono | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-08 | não selecionado | A rota edit da segunda compra carrega os dados dela e conserva a primeira | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-09 | não selecionado | O solicitante exclui seu rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-10 | não selecionado | A repetição da exclusão não ressuscita nem afeta outra compra | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-11 | não selecionado | Uma instância carregada antes da exclusão não continua operando | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-68 | não selecionado | O rascunho produzido por rejeição também pode ser excluído | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-12 | selecionado integral | Qualquer alçada começa pelo gestor do próprio centro | Compartilha três execuções futuras com CT-41; situação aguardando_gestor, histórico vazio e destinatários de envio. |
| CT-13 | não selecionado | O centro sem gestor impede o envio e conserva o rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-14 | não selecionado | A correção do centro muda quem recebe a solicitação enviada | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-65 | não selecionado | O envio sem gestor informa a recusa na interface e registra warning | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-15 | selecionado integral | O centavo em torno de cinco mil determina a próxima etapa | Três bordas, configuração efetiva sem override neste CT, decisão de gestor e avisos de Daniela conforme cada linha. |
| CT-16 | selecionado integral | A mudança explícita da alçada é usada na decisão | Override deliberado 7000.00, compra 6000.01, decisão de gestor e nenhum mail de Daniela. |
| CT-17 | selecionado integral | A decisão do diretor encerra a compra alta depois da decisão do gestor | Encerramento por Daniela após aprovação real de Geraldo, duas decisões ordenadas e não-efeitos de mail nomeados. |
| CT-18 | selecionado integral | Gestor e diretor rejeitam com uma justificativa curta ou Unicode | Três linhas integrais: duas etapas, Sem verba e texto Unicode; decisões antigas preservadas. |
| CT-19 | selecionado integral | A escrita direta recusa cada forma de justificativa ausente | Dez linhas integrais. Vazia/três espaços/U+0009 U+000A exigem RuntimeException de classe exata; null TypeError; omissão ArgumentCountError. As duas últimas são barreira tipada, não validação de conteúdo. |
| CT-20 | não selecionado | O componente recusa a rejeição sem justificativa e conserva a etapa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-21 | selecionado integral | A rejeição nas duas etapas reinicia o envio no gestor | Duas origens de rejeição; reenvio ao gestor, histórico integral conservado e mail do reenvio. |
| CT-22 | selecionado integral | A correção depois da rejeição altera a alçada do novo ciclo | Alta para baixa depois de rejeição e novo envio; terceira decisão de gestor, antigas preservadas, nenhum diretor novo/mail. |
| CT-23 | não selecionado | O novo ciclo não conserva autoridade do centro anterior | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-70 | selecionado integral | A correção de baixa para alta passa a exigir o diretor | Baixa para alta após rejeição real; mesmo ID, decisão antiga preservada e mail de cada diretora. |
| CT-76 | selecionado integral | Uma segunda rejeição não consome o direito de enviar novamente | Terceiro envio após duas rejeições reais e IDs de decisão distintos, sem chave de deduplicação inventada. |
| CT-24 | não selecionado | O cancelamento vale antes da decisão do gestor ou do diretor | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-25 | não selecionado | A repetição do cancelamento mantém o agregado cancelado | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-26 | não selecionado | A operação editar não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-27 | não selecionado | A operação excluir não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-28 | não selecionado | A operação enviar não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-29 | não selecionado | A operação aprovar não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-30 | não selecionado | A operação rejeitar não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-31 | não selecionado | A operação cancelar não atua nos estados em que é proibida | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-66 | não selecionado | A dona não consegue editar pela UI uma solicitação fora do rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-75 | não selecionado | O histórico de rejeição não permite decidir de novo antes do reenvio | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-32 | não selecionado | Outra pessoa não edita, exclui, envia nem cancela a compra de Sofia | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-33 | não selecionado | Uma ação forjada não ultrapassa a autorização do componente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-34 | não selecionado | Acumular dois papéis não cria aprovação automática nem impede o papel autorizado | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-73 | não selecionado | A solicitante que é gestora também pode rejeitar a etapa própria | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-35 | selecionado parcial | O papel ou a participação anterior não substitui a autoridade da etapa | Somente duas linhas de Daniela em aguardando_gestor: aprovar e rejeitar. Outros oito Examples omitidos. |
| CT-36 | não selecionado | Ser diretor em outra organização não autoriza esta decisão | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-37 | não selecionado | Aprovação e rejeição forçadas pelo ator errado continuam recusadas | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-72 | não selecionado | Administrar o centro não substitui a autoridade de aprovação da etapa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-74 | não selecionado | Administrar não impede aprovar ou rejeitar quando a autoridade corrente é própria | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-38 | não selecionado | O retry da mesma etapa não duplica decisão ou aviso | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-39 | não selecionado | Duas decisões realmente concorrentes de diretor têm uma única vencedora | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-40 | não selecionado | A decisão e a situação não ficam pela metade quando a gravação do histórico falha | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-41 | selecionado integral | O envio produz um e-mail para o gestor certo em cada alçada | Compartilha três execuções futuras com CT-12; mail, solicitação/etapa/destinatário, total de avisos um. |
| CT-42 | selecionado integral | Todos os diretores da organização recebem uma vez a próxima etapa | Duas cardinalidades; Daniela também diretora de Globex, Rui apenas de Globex e Paula diretora de Acme somente na linha N. |
| CT-43 | não selecionado | Os caminhos sem próxima etapa não enviam novos e-mails | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-44 | não selecionado | Uma notificação capturada só vale como e-mail se o canal pedido estiver presente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-45 | não selecionado | A listagem representa cada uma das cinco situações atuais | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-46 | não selecionado | O detalhe representa cada uma das cinco situações atuais | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-47 | não selecionado | A consulta paginada não perde solicitações nem usa o vazio como prova de status | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-67 | não selecionado | Uma mesma página mostra a situação própria de cada compra | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-48 | não selecionado | O detalhe mostra quem decidiu cada etapa sem substituir pelo usuário que consulta | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-49 | não selecionado | A justificativa e os autores do ciclo anterior continuam visíveis após a volta ao rascunho | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-50 | não selecionado | Um aprovador com permissão de consulta lê sua decisão depois da etapa | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-71 | não selecionado | O detalhe conserva o histórico visível depois do reenvio | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-51 | não selecionado | A criação do centro apresenta nome e gestor à administração | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-52 | não selecionado | O componente create grava o nome e o gestor escolhido | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-53 | não selecionado | A edição do centro carrega o gestor do registro correto | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-54 | não selecionado | O componente edit grava nome, gestor e a edição sem alteração | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-69 | não selecionado | A administradora exclui o centro próprio sem solicitações | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-55 | não selecionado | O usuário comum não grava administração do centro por fora do componente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-56 | não selecionado | O formulário forjado não permite ao usuário comum trocar gestor | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-57 | não selecionado | O papel diretor acordado abre a compra no painel da sua organização | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-58 | não selecionado | Uma solicitação de outra organização não pode ser lida ou alterada pelo ID conhecido | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-59 | não selecionado | O identificador conhecido não torna o centro estrangeiro administrável | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-60 | não selecionado | A etapa histórica não ganha acesso independente pelo ID da filha | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-61 | não selecionado | Um centro estrangeiro não entra na solicitação por payload válido nos demais campos | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-62 | não selecionado | Campos do servidor não são escolhidos pelo payload do cliente | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-63 | não selecionado | Um componente de usuário sem organização não entrega a base global | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-64 | não selecionado | A recusa de um ID estrangeiro deixa alcançável a consulta legítima do usuário | Não selecionado no recorte exploratório preregistrado de domínio; permanece literal no inventário abaixo. |
| CT-B01 | não selecionado | A abertura e o submit com JavaScript executam a rejeição certa | Browser/JS fora do recorte de domínio e sem execução autorizada. |
| CT-B02 | não selecionado | A confirmação vazia mostra o erro no campo e conserva a etapa | Browser/JS fora do recorte de domínio e sem execução autorizada. |

## Lacunas preservadas do próprio conjunto

O conjunto não formaliza perguntas novas vigentes. Permanecem sem direção: tetos/escala/zero ou negativo, zero diretores, link/corpo completo do e-mail, deduplicação de criação, atomicidade externa e inventário Livewire ausente. Não foram criados limites nem respostas. CT-B01/02 foram inventariados, mas browser/JS está fora deste recorte autorizado.

## Asserções literais e todas as linhas de Examples

### CT-01 — A criação conserva descrição, valor e centro escolhidos

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então existe exatamente uma solicitação de Sofia em rascunho em Acme, com descrição “Compra de ação 🔧”, valor “1299.99” e o ID do centro Operações
E existem zero decisões de aprovação e zero e-mails de aprovação enviados a Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-02 — Um campo obrigatório inválido impede a criação fora da UI

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a criação é recusada para <campo> e permanecem zero solicitações, zero decisões de aprovação e zero e-mails de aprovação
```

Cabeçalho literal: `| campo | entrada | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| descricao \| ausente \| obrigatória ausente \|` | omitida deste recorte | omitida |
| E02 | `\| descricao \| null \| obrigatória nula \|` | omitida deste recorte | omitida |
| E03 | `\| descricao \| string vazia \| obrigatória vazia \|` | omitida deste recorte | omitida |
| E04 | `\| descricao \| três espaços \| sem descrição \|` | omitida deste recorte | omitida |
| E05 | `\| valor \| ausente \| obrigatório ausente \|` | omitida deste recorte | omitida |
| E06 | `\| valor \| null \| obrigatório nulo \|` | omitida deste recorte | omitida |
| E07 | `\| valor \| string vazia \| obrigatório vazio \|` | omitida deste recorte | omitida |
| E08 | `\| valor \| texto abc \| não monetário \|` | omitida deste recorte | omitida |
| E09 | `\| centro_custo_id \| ausente \| obrigatório ausente \|` | omitida deste recorte | omitida |
| E10 | `\| centro_custo_id \| null \| obrigatório nulo \|` | omitida deste recorte | omitida |
| E11 | `\| centro_custo_id \| ID inexistente \| referência inexistente \|` | omitida deste recorte | omitida |

### CT-03 — O formulário de criação grava os três campos do solicitante

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a consulta nova ao banco encontra uma solicitação em rascunho de Sofia em Acme, com exatamente “Notebook”, “1299.99” e o centro Operações
E há zero decisões de aprovação e zero e-mails de aprovação
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-04 — A rota de criação oferece os três dados obrigatórios

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a resposta permite a criação e contém os controles de descrição, valor e escolha do centro de custo, sem valor, descrição ou centro previamente pertencentes a outra solicitação
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-05 — O solicitante corrige cada campo decisivo em rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a nova consulta encontra <campo> igual a <novo>, os demais campos iguais ao Dado e a situação rascunho
E o histórico de decisões continua vazio e não há e-mail de aprovação para Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| campo | novo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| descricao \| Monitor de ação 🔧 \| texto \|` | omitida deste recorte | omitida |
| E02 | `\| valor \| 4999.99 \| campo que muda a alçada \|` | omitida deste recorte | omitida |
| E03 | `\| centro_custo_id \| ID do centro Projetos \| campo que muda o gestor \|` | omitida deste recorte | omitida |
| E04 | `\| descricao \| Notebook \| edição sem alteração \|` | omitida deste recorte | omitida |

### CT-06 — A obrigatoriedade também é aplicada na correção do rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a escrita é recusada e o mesmo ID conserva descrição “Notebook”, valor “1299.99”, centro Operações e situação rascunho gravados
E o histórico continua vazio e nenhum e-mail de aprovação é enviado
```

Cabeçalho literal: `| campo | entrada | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| descricao \| string vazia \| descrição ausente na edição \|` | omitida deste recorte | omitida |
| E02 | `\| descricao \| três espaços \| descrição sem conteúdo na edição \|` | omitida deste recorte | omitida |
| E03 | `\| valor \| null \| valor ausente na edição \|` | omitida deste recorte | omitida |
| E04 | `\| valor \| abc \| valor não monetário na edição \|` | omitida deste recorte | omitida |
| E05 | `\| centro_custo_id \| ID inexistente \| centro inexistente na edição \|` | omitida deste recorte | omitida |

### CT-07 — O formulário edit grava a segunda compra e conserva a primeira do mesmo dono

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então B conserva seu ID e Sofia, em rascunho, com “Monitor”, “4999.99” e centro Projetos, e A conserva seu ID, “Teclado”, “199.99”, centro Operações, situação e histórico anteriores
E continuam existindo somente as duas compras, sem nova decisão ou e-mail de aprovação para Geraldo, Paula ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-08 — A rota edit da segunda compra carrega os dados dela e conserva a primeira

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então os controles de B contêm “Notebook”, “1299.99” e centro Operações, sem os valores de A, e ambos os IDs, dados, situações e históricos permanecem iguais aos do Dado
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-09 — O solicitante exclui seu rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a solicitação não existe mais entre as solicitações utilizáveis e não permanece decisão de aprovação associada
E nenhum e-mail de aprovação é enviado a Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-10 — A repetição da exclusão não ressuscita nem afeta outra compra

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a primeira solicitação continua inutilizável, a solicitação de Paula mantém todos os campos e não surge decisão de aprovação ou e-mail para Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-11 — Uma instância carregada antes da exclusão não continua operando

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a solicitação não reaparece, não muda a solicitação de Paula e não cria decisão de aprovação
E nenhum e-mail de aprovação é enviado a Paula ou Daniela
```

Cabeçalho literal: `| operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| editar o valor para 4999.99 \| removida × editar \|` | omitida deste recorte | omitida |
| E02 | `\| excluir \| removida × excluir \|` | omitida deste recorte | omitida |
| E03 | `\| enviar \| removida × enviar \|` | omitida deste recorte | omitida |
| E04 | `\| aprovar \| removida × aprovar \|` | omitida deste recorte | omitida |
| E05 | `\| rejeitar com justificativa Sem verba \| removida × rejeitar \|` | omitida deste recorte | omitida |
| E06 | `\| cancelar \| removida × cancelar \|` | omitida deste recorte | omitida |

### CT-68 — O rascunho produzido por rejeição também pode ser excluído

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a exclusão é permitida e B deixa de estar disponível para uso pelo seu ID, enquanto A conserva ID, campos, situação e histórico
E zero novos e-mails de aprovação são enviados a Geraldo ou Daniela, sem fixar cascata, retenção de histórico ou mecanismo de exclusão
```

Cabeçalho literal: `| etapa | decisoes | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| gestor \| 1 \| rascunho pós-rejeição de gestor \|` | omitida deste recorte | omitida |
| E02 | `\| diretor depois de gestor aprovado \| 2 \| rascunho pós-rejeição de diretor \|` | omitida deste recorte | omitida |

### CT-12 — Qualquer alçada começa pelo gestor do próprio centro

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é aguardando_gestor, o histórico de decisões continua vazio e Geraldo recebe um e-mail de aprovação dessa solicitação
E Paula e Daniela recebem zero e-mails de aprovação desse envio
```

Cabeçalho literal: `| valor | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 4999.99 \| abaixo da alçada \|` | materializada | não executada |
| E02 | `\| 5000.00 \| na alçada \|` | materializada | não executada |
| E03 | `\| 5000.01 \| acima da alçada \|` | materializada | não executada |

### CT-13 — O centro sem gestor impede o envio e conserva o rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o envio é recusado, a situação gravada permanece rascunho e não há decisão de aprovação
E zero e-mails de aprovação são enviados a Paula e Daniela, sem usar outra pessoa como substituta, e a tentativa registra warning referente à recusa por falta de gestor
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-14 — A correção do centro muda quem recebe a solicitação enviada

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação gravada é aguardando_gestor com centro Projetos, Paula recebe exatamente um e-mail de aprovação e Geraldo e Daniela recebem zero
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-65 — O envio sem gestor informa a recusa na interface e registra warning

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a interface apresenta a mensagem de recusa por falta de gestor e a tentativa registra warning dessa falha, sem exigir texto literal ou canal de log não especificado
E o mesmo ID conserva campos, situação rascunho e histórico vazio, e Paula e Daniela recebem zero e-mails de aprovação
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-15 — O centavo em torno de cinco mil determina a próxima etapa

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o banco contém situação <destino>, uma decisão aprovada de gestor por Geraldo e zero decisões de diretor
E Daniela recebe <emails_diretora> e-mails de aprovação
```

Cabeçalho literal: `| valor | destino | emails_diretora | # borda |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 4999.99 \| aprovada \| 0 \| borda−0,01 \|` | materializada | não executada |
| E02 | `\| 5000.00 \| aprovada \| 0 \| borda \|` | materializada | não executada |
| E03 | `\| 5000.01 \| aguardando_diretor \| 1 \| borda+0,01 \|` | materializada | não executada |

### CT-16 — A mudança explícita da alçada é usada na decisão

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é aprovada, há uma decisão de gestor por Geraldo e zero decisões de diretor e zero e-mails de aprovação para Daniela
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-17 — A decisão do diretor encerra a compra alta depois da decisão do gestor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é aprovada e o histórico contém exatamente gestor aprovado por Geraldo e diretor aprovado por Daniela
E nenhum e-mail de aprovação é enviado a Sofia, Geraldo, Daniela ou Paula
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-18 — Gestor e diretor rejeitam com uma justificativa curta ou Unicode

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é rascunho, as decisões anteriores permanecem e há uma nova decisão rejeitada da etapa corrente, por <ator>, com a justificativa <texto>
E zero e-mails de aprovação são enviados a Sofia, Geraldo ou Daniela
```

Cabeçalho literal: `| origem | ator | historico_antes | texto | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| Geraldo \| 0 \| Sem verba \| gestor; curta \|` | materializada | não executada |
| E02 | `\| aguardando_diretor \| Daniela \| 1 \| Sem verba \| diretor; curta \|` | materializada | não executada |
| E03 | `\| aguardando_gestor \| Geraldo \| 0 \| Não há orçamento 🔧 \| Unicode \|` | materializada | não executada |

### CT-19 — A escrita direta recusa cada forma de justificativa ausente

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a rejeição é recusada e a situação persistida continua <origem>, com o mesmo conjunto de decisões e justificativas anteriores
E nenhum e-mail de aprovação é enviado a Sofia, Geraldo ou Daniela
```

Cabeçalho literal: `| origem | entrada | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| string vazia \| vazia; gestor \|` | materializada | não executada |
| E02 | `\| aguardando_gestor \| três espaços \| branco; gestor \|` | materializada | não executada |
| E03 | `\| aguardando_gestor \| tabulação seguida de quebra de linha (U+0009 U+000A) \| branco sem espaço ASCII; gestor \|` | materializada | não executada |
| E04 | `\| aguardando_gestor \| null \| nula; gestor \|` | materializada | não executada |
| E05 | `\| aguardando_gestor \| ausente \| ausente; gestor \|` | materializada | não executada |
| E06 | `\| aguardando_diretor \| string vazia \| vazia; diretor \|` | materializada | não executada |
| E07 | `\| aguardando_diretor \| três espaços \| branco; diretor \|` | materializada | não executada |
| E08 | `\| aguardando_diretor \| tabulação seguida de quebra de linha (U+0009 U+000A) \| branco sem espaço ASCII; diretor \|` | materializada | não executada |
| E09 | `\| aguardando_diretor \| null \| nula; diretor \|` | materializada | não executada |
| E10 | `\| aguardando_diretor \| ausente \| ausente; diretor \|` | materializada | não executada |

### CT-20 — O componente recusa a rejeição sem justificativa e conserva a etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o campo justificativa tem erro de obrigatoriedade, a situação gravada continua aguardando_gestor e o histórico continua vazio
E zero e-mails de aprovação são enviados a Sofia, Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-21 — A rejeição nas duas etapas reinicia o envio no gestor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação gravada é aguardando_gestor e as <decisoes> decisões do ciclo anterior conservam autores, etapas e justificativas
E Geraldo recebe exatamente um e-mail de aprovação do reenvio e Daniela recebe zero
```

Cabeçalho literal: `| etapa_anterior | decisoes | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| gestor \| 1 \| ciclo após rejeição do gestor \|` | materializada | não executada |
| E02 | `\| diretor \| 2 \| ciclo após rejeição do diretor \|` | materializada | não executada |

### CT-22 — A correção depois da rejeição altera a alçada do novo ciclo

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação gravada é aprovada com valor “4999.99”, as duas decisões anteriores permanecem e existe uma terceira decisão aprovada de gestor por Geraldo
E zero decisões novas de diretor e zero e-mails de aprovação para Daniela são criados
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-23 — O novo ciclo não conserva autoridade do centro anterior

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação continua aguardando_gestor no centro Projetos, com somente a decisão rejeitada anterior por Geraldo
E zero e-mails de aprovação são enviados a Paula ou Daniela pela tentativa
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-70 — A correção de baixa para alta passa a exigir o diretor

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o mesmo ID tem valor 5000.01 e situação aguardando_diretor, conserva a decisão rejeitada antiga e acrescenta exatamente uma decisão aprovada de gestor por Geraldo, sem decisão de diretor
E Daniela e Paula recebem exatamente um aviso cada para a etapa diretor dessa compra no canal mail, e Sofia e Geraldo recebem zero novos avisos
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-76 — Uma segunda rejeição não consome o direito de enviar novamente

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o mesmo ID fica aguardando_gestor, conserva integralmente as duas decisões rejeitadas anteriores e não acrescenta decisão de aprovação no envio
E Geraldo recebe exatamente um novo aviso dessa compra para a etapa gestor no canal mail, total um, e Sofia, Daniela e Paula recebem zero; é terceiro envio com duas rejeições reais entre intenções, sem chave de deduplicação inventada
```

Sem tabela de Examples; caso único materializado, não executado.

### CT-24 — O cancelamento vale antes da decisão do gestor ou do diretor

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é cancelada e as <decisoes> decisões anteriores ficam iguais, sem nova decisão de aprovação
E zero e-mails de aprovação são enviados a Sofia, Geraldo, Daniela ou Paula
```

Cabeçalho literal: `| origem | decisoes | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| 0 \| antes do gestor \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| 1 \| antes do diretor \|` | omitida deste recorte | omitida |

### CT-25 — A repetição do cancelamento mantém o agregado cancelado

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação gravada permanece cancelada com somente a decisão anterior de Geraldo, sem novo registro de decisão e sem e-mail para Sofia, Geraldo, Daniela ou Paula
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-26 — A operação editar não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e os campos descrição “Notebook”, valor “8000.01” e centro Operações continuam exatamente gravados, com a mesma situação e o mesmo histórico; não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | campo | novo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| descricao \| Monitor \| aguardando_gestor × descrição \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| valor \| 4999.99 \| aguardando_gestor × alçada \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| centro_custo_id \| ID do centro Projetos \| aguardando_gestor × gestor \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| descricao \| Monitor \| aguardando_diretor × descrição \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| valor \| 4999.99 \| aguardando_diretor × alçada \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_diretor \| centro_custo_id \| ID do centro Projetos \| aguardando_diretor × gestor \|` | omitida deste recorte | omitida |
| E07 | `\| aprovada \| descricao \| Monitor \| aprovada × descrição \|` | omitida deste recorte | omitida |
| E08 | `\| aprovada \| valor \| 4999.99 \| aprovada × alçada \|` | omitida deste recorte | omitida |
| E09 | `\| aprovada \| centro_custo_id \| ID do centro Projetos \| aprovada × gestor \|` | omitida deste recorte | omitida |
| E10 | `\| cancelada \| descricao \| Monitor \| cancelada × descrição \|` | omitida deste recorte | omitida |
| E11 | `\| cancelada \| valor \| 4999.99 \| cancelada × alçada \|` | omitida deste recorte | omitida |
| E12 | `\| cancelada \| centro_custo_id \| ID do centro Projetos \| cancelada × gestor \|` | omitida deste recorte | omitida |

### CT-27 — A operação excluir não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e o registro continua existindo com a mesma situação, descrição “Notebook”, valor “8000.01”, centro Operações e todas as decisões anteriores; não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| aguardando_gestor × excluir \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| aguardando_diretor × excluir \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| aprovada × excluir \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| cancelada × excluir \|` | omitida deste recorte | omitida |

### CT-28 — A operação enviar não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação persistida e todas as decisões anteriores permanecem iguais, e não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| aguardando_gestor × enviar \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| aguardando_diretor × enviar \|` | omitida deste recorte | omitida |
| E03 | `\| aprovada \| aprovada × enviar \|` | omitida deste recorte | omitida |
| E04 | `\| cancelada \| cancelada × enviar \|` | omitida deste recorte | omitida |

### CT-29 — A operação aprovar não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação persistida permanece <origem>, as decisões anteriores ficam iguais, zero decisões de aprovação são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| rascunho × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| aprovada \| aprovada × aprovar \|` | omitida deste recorte | omitida |
| E03 | `\| cancelada \| cancelada × aprovar \|` | omitida deste recorte | omitida |

### CT-30 — A operação rejeitar não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação persistida permanece <origem>, as decisões e justificativas anteriores ficam iguais, zero decisões rejeitadas são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| rascunho × rejeitar \|` | omitida deste recorte | omitida |
| E02 | `\| aprovada \| aprovada × rejeitar \|` | omitida deste recorte | omitida |
| E03 | `\| cancelada \| cancelada × rejeitar \|` | omitida deste recorte | omitida |

### CT-31 — A operação cancelar não atua nos estados em que é proibida

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação persistida permanece <origem>, as decisões anteriores ficam iguais, zero decisões são acrescentadas e não há e-mail para Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| rascunho × cancelar \|` | omitida deste recorte | omitida |
| E02 | `\| aprovada \| aprovada × cancelar \|` | omitida deste recorte | omitida |
| E03 | `\| cancelada \| cancelada × cancelar \|` | omitida deste recorte | omitida |

### CT-66 — A dona não consegue editar pela UI uma solicitação fora do rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a gravação é recusada e a mesma compra conserva ID, solicitante, organização, descrição, valor, centro, situação <origem> e o conjunto anterior de decisões e justificativas
E zero novos e-mails de aprovação são enviados a Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | campo | novo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| descricao \| Monitor \| aguardando_gestor × descrição UI \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| valor \| 4999.99 \| aguardando_gestor × valor UI \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| centro_custo_id \| ID de Projetos \| aguardando_gestor × centro UI \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| descricao \| Monitor \| aguardando_diretor × descrição UI \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| valor \| 4999.99 \| aguardando_diretor × valor UI \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_diretor \| centro_custo_id \| ID de Projetos \| aguardando_diretor × centro UI \|` | omitida deste recorte | omitida |
| E07 | `\| aprovada \| descricao \| Monitor \| aprovada × descrição UI \|` | omitida deste recorte | omitida |
| E08 | `\| aprovada \| valor \| 4999.99 \| aprovada × valor UI \|` | omitida deste recorte | omitida |
| E09 | `\| aprovada \| centro_custo_id \| ID de Projetos \| aprovada × centro UI \|` | omitida deste recorte | omitida |
| E10 | `\| cancelada \| descricao \| Monitor \| cancelada × descrição UI \|` | omitida deste recorte | omitida |
| E11 | `\| cancelada \| valor \| 4999.99 \| cancelada × valor UI \|` | omitida deste recorte | omitida |
| E12 | `\| cancelada \| centro_custo_id \| ID de Projetos \| cancelada × centro UI \|` | omitida deste recorte | omitida |

### CT-75 — O histórico de rejeição não permite decidir de novo antes do reenvio

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a decisão é recusada e o mesmo ID conserva rascunho, descrição, valor, centro, solicitante e o conjunto das <antes> decisões anteriores com seus autores e justificativas
E zero novas decisões ou avisos de aprovação são produzidos para Sofia, Geraldo, Daniela ou Paula
```

Cabeçalho literal: `| etapa_rejeitada | ator | antes | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| gestor \| Geraldo \| 1 \| aprovar \| rascunho pós-rejeição gestor × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| gestor \| Geraldo \| 1 \| rejeitar \| rascunho pós-rejeição gestor × rejeitar \|` | omitida deste recorte | omitida |
| E03 | `\| diretor após aprovação do gestor \| Daniela \| 2 \| aprovar \| rascunho pós-rejeição diretor × aprovar \|` | omitida deste recorte | omitida |
| E04 | `\| diretor após aprovação do gestor \| Daniela \| 2 \| rejeitar \| rascunho pós-rejeição diretor × rejeitar \|` | omitida deste recorte | omitida |

### CT-32 — Outra pessoa não edita, exclui, envia nem cancela a compra de Sofia

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada, o registro conserva a situação <origem>, “Notebook”, “8000.01”, centro Operações e todas as decisões anteriores
E nenhum e-mail de aprovação é enviado a Sofia, Geraldo, Paula ou Daniela
```

Cabeçalho literal: `| origem | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| editar valor para 4999.99 \| outra pessoa × editar \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho \| excluir \| outra pessoa × excluir \|` | omitida deste recorte | omitida |
| E03 | `\| rascunho \| enviar \| outra pessoa × enviar \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_gestor \| cancelar \| outra pessoa × cancelar antes do gestor \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| cancelar \| outra pessoa × cancelar antes do diretor \|` | omitida deste recorte | omitida |

### CT-33 — Uma ação forjada não ultrapassa a autorização do componente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e o registro mantém os campos, a situação <origem> e o histórico capturados, sem e-mail para Geraldo ou Daniela; a ação correspondente permanece oculta ou a página de edição não é acessível a Paula
```

Cabeçalho literal: `| origem | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| editar valor para 4999.99 \| UI editar \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho \| excluir \| UI excluir \|` | omitida deste recorte | omitida |
| E03 | `\| rascunho \| enviar \| UI enviar \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_gestor \| cancelar \| UI cancelar \|` | omitida deste recorte | omitida |

### CT-34 — Acumular dois papéis não cria aprovação automática nem impede o papel autorizado

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é <destino> e o histórico ganhou exatamente uma decisão aprovada da etapa <etapa> por <ator>, conservando as <antes> anteriores
```

Cabeçalho literal: `| origem | ator | par | antes | etapa | destino | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| Sofia \| solicitante e gestor \| 0 \| gestor \| aguardando_diretor \| A-09 \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_diretor \| Sofia \| solicitante e diretor \| 1 \| diretor \| aprovada \| diretor é qualquer titular em Acme \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| Geraldo \| gestor e diretor \| 0 \| gestor \| aguardando_diretor \| primeira etapa permanece separada \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| Geraldo \| gestor e diretor \| 1 \| diretor \| aprovada \| segunda decisão explícita \|` | omitida deste recorte | omitida |

### CT-73 — A solicitante que é gestora também pode rejeitar a etapa própria

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o mesmo ID retorna a rascunho e contém exatamente uma decisão rejeitada de gestor por Sofia, com a justificativa integral Sem verba
E Sofia, Daniela e Paula recebem zero novos avisos de aprovação; gestor é o vínculo do centro, sem criar um papel global gestor
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-35 — O papel ou a participação anterior não substitui a autoridade da etapa

Seleção: **selecionado parcial**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a situação <origem> e todas as decisões e justificativas anteriores permanecem gravadas
E zero e-mails de aprovação são enviados a Sofia, Geraldo, Paula, Daniela ou Rui
```

Cabeçalho literal: `| origem | ator | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| Paula \| aprovar \| gestor de outro centro × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| Daniela \| aprovar \| diretor antes do gestor × aprovar \|` | materializada | não executada |
| E03 | `\| aguardando_gestor \| Sofia \| aprovar \| solicitante sem autoridade × aprovar \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| Geraldo \| aprovar \| gestor que já decidiu × aprovar \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_diretor \| Rui \| aprovar \| sem papel diretor × aprovar \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_gestor \| Paula \| rejeitar \| gestor de outro centro × rejeitar \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_gestor \| Daniela \| rejeitar \| diretor antes do gestor × rejeitar \|` | materializada | não executada |
| E08 | `\| aguardando_gestor \| Sofia \| rejeitar \| solicitante sem autoridade × rejeitar \|` | omitida deste recorte | omitida |
| E09 | `\| aguardando_diretor \| Geraldo \| rejeitar \| gestor que já decidiu × rejeitar \|` | omitida deste recorte | omitida |
| E10 | `\| aguardando_diretor \| Rui \| rejeitar \| sem papel diretor × rejeitar \|` | omitida deste recorte | omitida |

### CT-36 — Ser diretor em outra organização não autoriza esta decisão

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada e a solicitação permanece aguardando_diretor com somente a decisão anterior por Geraldo, sem e-mail para Paula
```

Cabeçalho literal: `| operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aprovar \| papel fora do contexto × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| rejeitar \| papel fora do contexto × rejeitar \|` | omitida deste recorte | omitida |

### CT-37 — Aprovação e rejeição forçadas pelo ator errado continuam recusadas

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a ação não pode ser concluída, a situação persistida continua aguardando_gestor, há zero decisões e zero e-mails para Geraldo ou Daniela; a ação <operacao> permanece oculta para Rui
```

Cabeçalho literal: `| operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aprovar \| autoridade × aprovar UI \|` | omitida deste recorte | omitida |
| E02 | `\| rejeitar \| autoridade × rejeitar UI \|` | omitida deste recorte | omitida |

### CT-72 — Administrar o centro não substitui a autoridade de aprovação da etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a decisão é recusada porque esse ator não tem a autoridade da etapa corrente, e o mesmo ID conserva campos, organização, situação <origem> e todas as decisões e justificativas anteriores
E zero novos avisos de aprovação são enviados a Sofia, Geraldo, Daniela ou Ana
```

Cabeçalho literal: `| origem | ator | papeis | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| Ana \| admin_organizacao \| aprovar \| admin sem autoridade do gestor × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| Ana \| admin_organizacao \| rejeitar \| admin sem autoridade do gestor × rejeitar \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| Ana \| admin_organizacao \| aprovar \| admin sem autoridade do diretor × aprovar \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| Ana \| admin_organizacao \| rejeitar \| admin sem autoridade do diretor × rejeitar \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_gestor \| Sofia \| solicitante e admin_organizacao \| aprovar \| par solicitante × administração × aprovar \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_gestor \| Sofia \| solicitante e admin_organizacao \| rejeitar \| par solicitante × administração × rejeitar \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_diretor \| Geraldo \| gestor e admin_organizacao \| aprovar \| par gestor × administração × aprovar \|` | omitida deste recorte | omitida |
| E08 | `\| aguardando_diretor \| Geraldo \| gestor e admin_organizacao \| rejeitar \| par gestor × administração × rejeitar \|` | omitida deste recorte | omitida |
| E09 | `\| aguardando_gestor \| Daniela \| diretor e admin_organizacao \| aprovar \| par diretor × administração × aprovar \|` | omitida deste recorte | omitida |
| E10 | `\| aguardando_gestor \| Daniela \| diretor e admin_organizacao \| rejeitar \| par diretor × administração × rejeitar \|` | omitida deste recorte | omitida |

### CT-74 — Administrar não impede aprovar ou rejeitar quando a autoridade corrente é própria

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o mesmo ID fica em <destino>, conserva as <antes> decisões anteriores e acrescenta exatamente uma decisão <decisao> da etapa <etapa> por Ana, com Sem verba integral somente se rejeitada
E Daniela e Paula recebem <por_diretora> novo aviso cada, total <total_avisos>, da compra e etapa diretor no canal mail quando houver aviso, e Ana, Sofia e Geraldo recebem zero novos avisos
```

Cabeçalho literal: `| origem | gestor | antes | etapa | operacao | destino | decisao | por_diretora | total_avisos | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| Ana \| 0 \| gestor \| aprovar \| aguardando_diretor \| aprovada \| 1 \| 2 \| admin × gestor autorizado × aprovar \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| Ana \| 0 \| gestor \| rejeitar \| rascunho \| rejeitada \| 0 \| 0 \| admin × gestor autorizado × rejeitar \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| Geraldo \| 1 \| diretor \| aprovar \| aprovada \| aprovada \| 0 \| 0 \| admin × diretor autorizado × aprovar \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| Geraldo \| 1 \| diretor \| rejeitar \| rascunho \| rejeitada \| 0 \| 0 \| admin × diretor autorizado × rejeitar \|` | omitida deste recorte | omitida |

### CT-38 — O retry da mesma etapa não duplica decisão ou aviso

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é <destino>, o histórico ganhou <novas_decisoes> decisões da intenção e cada destinatário da próxima etapa recebeu exatamente <avisos> e-mails dessa intenção
```

Cabeçalho literal: `| origem | operacao | destino | novas_decisoes | avisos | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| enviar \| aguardando_gestor \| 0 \| 1 \| retry de envio \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| aprovar valor 4999.99 \| aprovada \| 1 \| 0 \| retry de aprovação final do gestor \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_gestor \| aprovar valor 8000.01 \| aguardando_diretor \| 1 \| 1 \| retry da etapa de gestor \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_diretor \| aprovar \| aprovada \| 1 \| 0 \| retry da etapa de diretor \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_gestor \| rejeitar com Sem verba \| rascunho \| 1 \| 0 \| retry de rejeição \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_gestor \| cancelar \| cancelada \| 0 \| 0 \| retry de cancelamento \|` | omitida deste recorte | omitida |

### CT-39 — Duas decisões realmente concorrentes de diretor têm uma única vencedora

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o agregado persistido fica aprovada, com a decisão anterior de Geraldo e exatamente uma decisão de diretor aprovada por Daniela
E a tentativa perdedora não grava decisão ou justificativa de Paula, e não há novo e-mail para Sofia, Geraldo, Daniela ou Paula
```

Cabeçalho literal: `| segunda_decisao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aprovar \| aprovação × aprovação \|` | omitida deste recorte | omitida |
| E02 | `\| rejeitar com Sem verba \| aprovação × rejeição \|` | omitida deste recorte | omitida |

### CT-40 — A decisão e a situação não ficam pela metade quando a gravação do histórico falha

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação falha e a nova consulta encontra aguardando_gestor, zero decisões de gestor ou diretor e zero avisos de aprovação para Daniela e Paula
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-41 — O envio produz um e-mail para o gestor certo em cada alçada

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então Geraldo recebe exatamente uma AprovacaoPendente dessa solicitação para a etapa gestor no canal mail
E o total de avisos de aprovação é um e Sofia, Paula e Daniela recebem zero
```

Cabeçalho literal: `| valor | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 4999.99 \| sem etapa extra \|` | materializada | não executada |
| E02 | `\| 5000.00 \| borda literal \|` | materializada | não executada |
| E03 | `\| 5000.01 \| com etapa extra \|` | materializada | não executada |

### CT-42 — Todos os diretores da organização recebem uma vez a próxima etapa

Seleção: **selecionado integral**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a situação persistida é aguardando_diretor e cada diretor de Acme recebe exatamente um aviso dessa solicitação para a etapa diretor no canal mail, total <diretores_acme>
E Rui, Sofia e Geraldo recebem zero avisos de aprovação
```

Cabeçalho literal: `| diretores_acme | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 1 \| cardinalidade um; Daniela \|` | materializada | não executada |
| E02 | `\| 2 \| cardinalidade N; Daniela e Paula \|` | materializada | não executada |

### CT-43 — Os caminhos sem próxima etapa não enviam novos e-mails

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o banco contém <destino> e o histórico corresponde somente à decisão ou cancelamento efetuado, com zero novos e-mails de aprovação para Sofia, Geraldo, Daniela e Paula
```

Cabeçalho literal: `| origem | valor | operacao | destino | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| aguardando_gestor \| 4999.99 \| aprovar \| aprovada \| aprovação final baixa \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| 5000.00 \| aprovar \| aprovada \| aprovação final na borda \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| 5000.01 \| aprovar \| aprovada \| aprovação final alta \|` | omitida deste recorte | omitida |
| E04 | `\| aguardando_gestor \| 4999.99 \| rejeitar com Sem verba \| rascunho \| rejeição baixa \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_gestor \| 5000.01 \| rejeitar com Sem verba \| rascunho \| rejeição alta pelo gestor \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_diretor \| 5000.01 \| rejeitar com Sem verba \| rascunho \| rejeição alta pelo diretor \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_gestor \| 4999.99 \| cancelar \| cancelada \| cancelamento baixo \|` | omitida deste recorte | omitida |
| E08 | `\| aguardando_gestor \| 5000.01 \| cancelar \| cancelada \| cancelamento alto antes do gestor \|` | omitida deste recorte | omitida |
| E09 | `\| aguardando_diretor \| 5000.01 \| cancelar \| cancelada \| cancelamento alto antes do diretor \|` | omitida deste recorte | omitida |

### CT-44 — Uma notificação capturada só vale como e-mail se o canal pedido estiver presente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o aviso capturado para Geraldo identifica essa solicitação e etapa gestor, sua lista efetiva de canais contém mail e sua mensagem para mail identifica a solicitação correta
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-45 — A listagem representa cada uma das cinco situações atuais

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a linha dessa solicitação está presente e o status mostrado nessa linha corresponde a <situacao>, sem exibir um status diferente
```

Cabeçalho literal: `| situacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| enum rascunho \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| enum aguardando_gestor \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| enum aguardando_diretor \|` | omitida deste recorte | omitida |
| E04 | `\| aprovada \| enum aprovada \|` | omitida deste recorte | omitida |
| E05 | `\| cancelada \| enum cancelada \|` | omitida deste recorte | omitida |

### CT-46 — O detalhe representa cada uma das cinco situações atuais

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o detalhe identifica a solicitação de Sofia e mostra status correspondente a <situacao>, sem trocar aguardando_diretor por aprovada
```

Cabeçalho literal: `| situacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| enum rascunho \|` | omitida deste recorte | omitida |
| E02 | `\| aguardando_gestor \| enum aguardando_gestor \|` | omitida deste recorte | omitida |
| E03 | `\| aguardando_diretor \| enum aguardando_diretor \|` | omitida deste recorte | omitida |
| E04 | `\| aprovada \| enum aprovada \|` | omitida deste recorte | omitida |
| E05 | `\| cancelada \| enum cancelada \|` | omitida deste recorte | omitida |

### CT-47 — A consulta paginada não perde solicitações nem usa o vazio como prova de status

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o conjunto de identificadores retornados nas páginas contém exatamente as <quantidade> solicitações de Acme, cada linha com status rascunho, sem duplicata ou solicitação de Globex
```

Cabeçalho literal: `| quantidade | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| 0 \| vazia \|` | omitida deste recorte | omitida |
| E02 | `\| 1 \| um registro \|` | omitida deste recorte | omitida |
| E03 | `\| 10 \| limite da página \|` | omitida deste recorte | omitida |
| E04 | `\| 11 \| acima do limite \|` | omitida deste recorte | omitida |

### CT-67 — Uma mesma página mostra a situação própria de cada compra

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a linha de L1 mostra rascunho, L2 aguardando_gestor, L3 aguardando_diretor, L4 aprovada e L5 cancelada, associando cada situação somente ao seu ID
E os cinco IDs aparecem uma vez cada e o oráculo compara o conteúdo de cada linha, sem usar texto global ou a tela de detalhe
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-48 — O detalhe mostra quem decidiu cada etapa sem substituir pelo usuário que consulta

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico contém <linhas> linhas de decisão com etapas e autores <autores>, nos respectivos instantes reais, sem atribuir as decisões a Sofia
```

Cabeçalho literal: `| caminho | linhas | autores | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| valor 4999.99; gestor \| 1 \| gestor Geraldo \| uma etapa \|` | omitida deste recorte | omitida |
| E02 | `\| valor 5000.01; gestor e diretor \| 2 \| gestor Geraldo e diretor Daniela \| duas etapas \|` | omitida deste recorte | omitida |

### CT-49 — A justificativa e os autores do ciclo anterior continuam visíveis após a volta ao rascunho

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico mostra gestor aprovado por Geraldo e diretor rejeitado por Daniela, com os instantes das duas decisões e a justificativa integral “Não há orçamento 🔧”
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-50 — Um aprovador com permissão de consulta lê sua decisão depois da etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o detalhe identifica a solicitação e mostra sua decisão de gestor por Geraldo e a decisão de diretor por Daniela, sem ocultar o registro por não haver etapa pendente
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-71 — O detalhe conserva o histórico visível depois do reenvio

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o histórico visível desse ID mostra as duas decisões, gestor aprovado por Geraldo no primeiro instante e diretor rejeitado por Daniela no segundo, com a justificativa integral Não há orçamento 🔧
E não esconde as decisões por pertencerem ao ciclo anterior nem substitui autores ou instantes; formato e fuso da apresentação não são fixados pelo teste
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-51 — A criação do centro apresenta nome e gestor à administração

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a resposta permite o cadastro e contém os controles de nome e seleção do gestor
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-52 — O componente create grava o nome e o gestor escolhido

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a nova consulta encontra exatamente um centro Projetos de Acme com Paula como gestora
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-53 — A edição do centro carrega o gestor do registro correto

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a resposta contém nome Projetos e a seleção de Paula para esse registro
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-54 — O componente edit grava nome, gestor e a edição sem alteração

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então esse mesmo ID de centro de Acme tem nome <nome> e gestor <gestor>, sem criar outro centro nem mudar ID, nome, gestor ou organização de Administrativo
```

Cabeçalho literal: `| nome | gestor | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| Projetos \| Geraldo \| troca somente do gestor \|` | omitida deste recorte | omitida |
| E02 | `\| Operações \| Paula \| troca somente do nome \|` | omitida deste recorte | omitida |
| E03 | `\| Projetos \| Paula \| edição sem alteração \|` | omitida deste recorte | omitida |

### CT-69 — A administradora exclui o centro próprio sem solicitações

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a exclusão é permitida e Projetos deixa de estar disponível para uso pelo seu ID, enquanto Operações conserva ID, organização Acme, nome e gestor Geraldo
E não é criada solicitação nem decisão de aprovação, sem decidir o que acontece ao excluir um centro com solicitações
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-55 — O usuário comum não grava administração do centro por fora do componente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada, o centro Projetos mantém nome, organização e gestora Paula e não surge novo centro administrado por Sofia
```

Cabeçalho literal: `| operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| criar centro Operações com Sofia gestora \| comum × criar \|` | omitida deste recorte | omitida |
| E02 | `\| alterar nome para Operações \| comum × editar nome \|` | omitida deste recorte | omitida |
| E03 | `\| alterar gestor para Sofia \| escalada por identidade \|` | omitida deste recorte | omitida |
| E04 | `\| excluir centro Projetos \| comum × excluir \|` | omitida deste recorte | omitida |

### CT-56 — O formulário forjado não permite ao usuário comum trocar gestor

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a escrita é recusada e o centro Projetos continua com Paula como gestora e com o mesmo tenant, sem promover Sofia
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-57 — O papel diretor acordado abre a compra no painel da sua organização

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a resposta permite a consulta e mostra a solicitação de Sofia, situação aguardando_diretor e a decisão de gestor por Geraldo
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-58 — Uma solicitação de outra organização não pode ser lida ou alterada pelo ID conhecido

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o resultado é <resultado>, o registro estrangeiro não é entregue e conserva organização Globex, solicitante Sofia, situação <situacao>, valor, centro e decisões capturados
E zero e-mails de aprovação são enviados aos aprovadores de Globex pela tentativa
```

Cabeçalho literal: `| situacao | operacao | resultado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| rascunho \| ler detalhe por HTTP \| 403 ou 404, sem conteúdo da solicitação \| IDOR solicitação × ler \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho \| editar valor pelo domínio \| recusa sem alteração \| IDOR solicitação × editar \|` | omitida deste recorte | omitida |
| E03 | `\| rascunho \| excluir pelo domínio \| recusa sem alteração \| IDOR solicitação × excluir \|` | omitida deste recorte | omitida |
| E04 | `\| rascunho \| enviar pelo domínio \| recusa sem alteração \| IDOR solicitação × enviar \|` | omitida deste recorte | omitida |
| E05 | `\| aguardando_gestor \| cancelar pelo domínio \| recusa sem alteração \| IDOR solicitação × cancelar \|` | omitida deste recorte | omitida |
| E06 | `\| aguardando_gestor \| aprovar pelo domínio \| recusa sem alteração \| IDOR solicitação × aprovar \|` | omitida deste recorte | omitida |
| E07 | `\| aguardando_gestor \| rejeitar com Sem verba pelo domínio \| recusa sem alteração \| IDOR solicitação × rejeitar \|` | omitida deste recorte | omitida |

### CT-59 — O identificador conhecido não torna o centro estrangeiro administrável

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o resultado é <resultado>, o centro de Globex não é entregue e mantém nome Projetos, organização Globex e gestora Paula
```

Cabeçalho literal: `| operacao | resultado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| ler a rota edit \| 403 ou 404 sem conteúdo estrangeiro \| IDOR centro × leitura \|` | omitida deste recorte | omitida |
| E02 | `\| alterar gestor para Ana por fora do componente \| recusa sem alteração \| IDOR centro × alteração \|` | omitida deste recorte | omitida |
| E03 | `\| excluir por fora do componente \| recusa sem alteração \| IDOR centro × exclusão \|` | omitida deste recorte | omitida |

### CT-60 — A etapa histórica não ganha acesso independente pelo ID da filha

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o resultado é <resultado>, nenhum histórico de Globex é entregue e a decisão permanece ligada à solicitação de Sofia de Globex, com etapa gestor, decisão aprovada e autor Geraldo
```

Cabeçalho literal: `| operacao | resultado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| ler pelo ID da decisão \| não entrega a decisão estrangeira \| IDOR etapa × leitura direta \|` | omitida deste recorte | omitida |
| E02 | `\| alterar autor para Sofia pelo ID da decisão \| recusa sem alterar autor ou vínculo \| filha × escrita não autorizada \|` | omitida deste recorte | omitida |

### CT-61 — Um centro estrangeiro não entra na solicitação por payload válido nos demais campos

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a operação é recusada, zero novas solicitações ou decisões são criadas, e o rascunho já existente quando houver mantém o centro de Acme e os outros campos
E zero e-mails de aprovação são enviados a Paula, Geraldo ou Daniela
```

Cabeçalho literal: `| partida | operacao | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| ainda inexistente \| criar \| referência na criação \|` | omitida deste recorte | omitida |
| E02 | `\| rascunho em Acme \| editar centro \| referência na edição \|` | omitida deste recorte | omitida |
| E03 | `\| rascunho com referência histórica estrangeira preparada só como dado corrupto \| enviar \| referência no uso \|` | omitida deste recorte | omitida |

### CT-62 — Campos do servidor não são escolhidos pelo payload do cliente

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então o agregado persistido tem <esperado>, sem adotar <forjado> para o campo protegido nem alterar as entidades de Globex
```

Cabeçalho literal: `| alvo | partida | campo | forjado | operacao | esperado | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| solicitação \| ainda inexistente \| situacao \| aprovada \| criar pelo domínio \| rascunho \| solicitação × estado \|` | omitida deste recorte | omitida |
| E02 | `\| solicitação \| ainda inexistente \| solicitante_id \| ID de Daniela \| criar pelo domínio como Sofia \| solicitante Sofia \| solicitação × autoria \|` | omitida deste recorte | omitida |
| E03 | `\| solicitação \| rascunho em Acme \| tenant_id \| ID de Globex \| editar pelo domínio como Sofia \| organização Acme \| solicitação × tenant \|` | omitida deste recorte | omitida |
| E04 | `\| centro \| ainda inexistente \| tenant_id \| ID de Globex \| criar pelo domínio da administração como Ana \| organização Acme \| centro × tenant \|` | omitida deste recorte | omitida |
| E05 | `\| centro \| centro de Acme existente \| uuid \| UUID do centro Globex \| editar pelo domínio da administração como Ana \| UUID original \| centro × identidade \|` | omitida deste recorte | omitida |
| E06 | `\| etapa \| solicitação aguardando_gestor \| decidido_por_id \| ID de Sofia \| aprovar pelo domínio como Geraldo \| autor Geraldo \| etapa × autoria \|` | omitida deste recorte | omitida |
| E07 | `\| etapa \| solicitação aguardando_gestor \| solicitacao_compra_id \| ID da compra de Globex \| aprovar pelo domínio como Geraldo \| pai é a compra de Acme \| etapa × pai \|` | omitida deste recorte | omitida |
| E08 | `\| etapa \| solicitação aguardando_gestor \| etapa \| diretor \| aprovar pelo domínio como Geraldo \| etapa gestor \| etapa × etapa \|` | omitida deste recorte | omitida |

### CT-63 — Um componente de usuário sem organização não entrega a base global

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então nenhuma solicitação, centro ou decisão de Acme ou Globex é entregue ao cliente e nenhum dado é gravado ou notificado
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-64 — A recusa de um ID estrangeiro deixa alcançável a consulta legítima do usuário

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a resposta permite a consulta, contém somente a solicitação de Sofia com “Notebook” e status rascunho e não redireciona de volta ao registro estrangeiro
```

Cabeçalho literal: `| alvo | # partição |`.

| Linha | Examples literal | Tradução | Execução |
|---|---|---|---|
| E01 | `\| solicitação \| saída de IDOR da compra \|` | omitida deste recorte | omitida |
| E02 | `\| centro de custo \| saída de IDOR do centro \|` | omitida deste recorte | omitida |

### CT-B01 — A abertura e o submit com JavaScript executam a rejeição certa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a modal e seu campo foram visíveis antes da confirmação e a solicitação persistida está em rascunho
E existe exatamente uma decisão rejeitada de gestor, por Geraldo, com justificativa “Sem verba”, e zero novos e-mails para Sofia, Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

### CT-B02 — A confirmação vazia mostra o erro no campo e conserva a etapa

Seleção: **não selecionado**. Execução real: **não executado**.

Asserções literais do conjunto:

```text
Então a modal permanece visível e mostra um erro visível associado ao campo justificativa
E a solicitação persistida permanece aguardando_gestor, com zero decisões e zero novos e-mails para Sofia, Geraldo ou Daniela
```

Sem tabela de Examples; caso único omitido deste recorte.

