# Plano de Ação — FERRO-845: Padrões de PII configuráveis

> Requisito: `00-requisito.md`. Planejamento inicial dos steps 0–4, em 2026-10-20. Não revisado pelo step 5.

## Natureza da Wiki

- **Tipo**: evolução.
- **Wiki ancestral**: nenhuma wiki de especificação do redator encontrada nas árvores permitidas `wikis/specs/main/` e `wikis/specs/feature/`. O contexto existente está em `wikis/ia.md`; não substitui o requisito deste card.
- **Motivo**: tornar configurável um comportamento existente, preservando o contrato padrão.
- **Toca infra compartilhada?**: sim, configuração e redator usados pela camada de IA. Exige regressão dessa camada, especialmente `tests/Kit/IaTest.php`.
- **Limite desta sessão**: somente documentação; a autorização recebida não permite implementar, instalar dependências ou avançar ao step 5.

## Cobertura do Requisito

| RQ | Cláusula | Passo(s) que atende(m) | Observação |
|----|----------|------------------------|------------|
| RQ-01 | Padrões ajustáveis pela configuração | 1, 2, 3 | Caminho completo válido determinado; recortes parcial/vazio e inválido bloqueados por Q1/Q2. |
| RQ-02 | Equivalência do comportamento padrão | 1, 2, 3 | Não aperfeiçoar as regex nem trocar os algoritmos atuais. |
| RQ-03 | Mesmos tipos | 1, 2, 3 | Preservar os nomes existentes; o card não autoriza criar ou remover tipos. |
| RQ-04 | Mesma ordem | 1, 2, 3 | Preservar a prioridade do redator; não ordenar alfabeticamente. |
| RQ-05 | Mesmo marcador | 2, 3 | Preservar `[REDIGIDO:tipo]`. |
| RQ-06 | Defaults quando a configuração não existir | 1, 2, 3 | Ausência de chave é diferente de valor presente inválido. |
| RQ-07 | Sem tela nova | 1, 2, 3 | Somente configuração, classe existente e testes de backend. |

**Bloqueado por**: Q1 — somente o recorte de RQ-01/RQ-03/RQ-06 relativo a mapa presente parcial/vazio.

**Bloqueado por**: Q2 — somente o recorte de RQ-01/RQ-02/RQ-06 relativo a configuração presente inválida.

Não há RQ integralmente aberta. O bloqueio não elimina a configuração completa válida nem os defaults. Recomendações no `00` não autorizam handlers, exceções ou fallback adicionais.

## Objetivo

Permitir que o time ajuste as expressões do redator de PII pela configuração Laravel, mantendo os resultados atuais quando usa os defaults. Preservar os tipos, sua prioridade e o marcador, inclusive quando a chave de configuração estiver ausente.

O escopo é a fonte dos padrões. O pipeline de agentes, o catálogo, o filtro de saída e a interface do redator continuam sendo as referências existentes. A feature não exige uma tela de administração de padrões.

## Contexto

O redator contém um mapa privado de expressões regulares. A substituição e a detecção percorrem esse mesmo mapa, mas de formas diferentes: a primeira transforma progressivamente o texto; a segunda consulta cada regex sobre o texto recebido. Essa diferença precisa sobreviver à extração.

## Análise dos Arquivos Existentes

| Evidência | Fato descoberto e consequência |
|---|---|
| `app/Ai/Guardrails/PiiRedactor.php:PADROES:17` | Mapa atual, na ordem `email`, `token`, `cnpj`, `cartao`, `cpf`, `telefone`, `ip`. Comando: `rg -n "PADROES|=>" app/Ai/Guardrails/PiiRedactor.php`. Copiar literalmente os valores, sem corrigir heurísticas. |
| `app/Ai/Guardrails/PiiRedactor.php:redigir():27` | Assinatura pública `redigir(string $texto): string`; substituições sequenciais com `preg_replace` e `?? $texto`. |
| `app/Ai/Guardrails/PiiRedactor.php:tiposDetectados():41` | Assinatura pública `tiposDetectados(string $texto): array`; `list<string>` sem duplicar o mesmo tipo, em ordem de processamento. Usa `preg_match(...) === 1` sobre o texto recebido. |
| `app/Ai/Guardrails/PiiRedactorMiddleware.php:handle():20` | Usa o redator injetado, mascara antes de chamar o próximo middleware e registra tipos apenas quando o texto muda. Não exige mudança da assinatura nem novo binding. |
| `app/Ai/Guardrails/GuardrailRegistry.php:resolver():38` | Resolve middlewares pelo container. A chave `pii_redactor` já existe no mapa. |
| `app/Ai/Agents/Assistente.php:middleware():61` | Auditoria continua depois dos guardrails. Não alterar essa ordem para extrair a configuração. |
| `config/ai.php:'agente_timeout':33` | Configuração de IA já admite opções da aplicação. Não contém padrões de PII. Reutilizar esse arquivo. |
| `config/logging.php:'ai':85` | Canal `ai` existente, driver `daily`, retenção já configurada. Reutilizar, sem novo canal. |
| `tests/Kit/IaTest.php` | Regressão existente do catálogo e resolução dos guardrails; não contém teste direto de `redigir`/`tiposDetectados`. |
| `tests/Pest.php`, `phpunit.xml` | Feature usa TestCase Laravel com RefreshDatabase; Kit é suíte própria. Há TIA local configurado e timeout de browser de 20.000 ms. |

`rg -n 'trait.*Logging' app` não encontrou trait de logging. Usar a facade e o formato existente. `rg -n -i 'pii|redator|guardrail' wikis/specs/main wikis/specs/feature -g '01-plano-acao.md'` não encontrou plano ancestral específico; busca não alcançou árvores proibidas.

### Versões e fontes consultadas

- PHP executável: 8.4.10, por `php --version`.
- `composer show --direct`: `No dependencies installed. Try running composer install or update.` Não há versões instaladas confirmadas.
- O `composer.lock`, lido como JSON, fixa Laravel v13.25.0, Filament v5.7.6, Livewire v4.4.0, SDK IA v0.10.3, Boost v2.5.3, Pest v5.1.1, plugins Laravel/browser v5.0.1, PHPUnit 13.3.0 e Pint v1.30.5. São versões travadas, não instaladas.
- `package.json` declara Playwright `^1.62.1`; não se confirmou instalação. Não haverá mudança de frontend.
- Boost MCP `search-docs` não está entre as ferramentas expostas. Fallback de leitura oficial, em 2026-10-20: [configuração Laravel 13](https://laravel.com/framework/docs/13.x/configuration#accessing-configuration-values), que confirma acesso com chave pontuada e default para opção ausente; [cache de configuração](https://laravel.com/framework/docs/13.x/configuration#configuration-caching), para ativação operacional; [logs Laravel 13](https://laravel.com/framework/docs/13.x/logging#writing-to-specific-channels), para reutilização do canal.
- [Manual PHP de preg_replace](https://www.php.net/manual/en/function.preg-replace.php): retorno pode ser nulo em erro; regex inválida emite warning. [Documentação Pest](https://pestphp.com/docs/writing-tests): fonte oficial disponível para Pest 5. Não foram derivados CTs nesta etapa.
- A página de `preg_match` falhou por timeout; não se atribui confirmação documental a ela. O uso atual foi lido no código.
- Filament/Livewire não terão API alterada; não há consulta de componentes nem planejamento de CT-B. APIs do SDK permanecem existentes; qualquer teste que construa `AgentPrompt` deverá confirmar a assinatura no vendor da versão realmente instalada antes de escrevê-lo.

## Decisões de Desenho

| # | Decisão | Pergunta | Portão que falta | Quem decidiu, data |
|---|---|---|---|---|
| D1 | Usar `ai.pii.padroes`, dentro de `config/ai.php`, como mapa ordenado tipo → regex. | Escolha rotineira sob autorização para planejar RQ-01; arquivo de IA existente. | Difícil de reverter. | Sessão, 2026-10-20. |
| D2 | Manter `PiiRedactor::PADROES` como fallback de compatibilidade e centralizar a leitura em um método privado do redator. | RQ-06 exige defaults mesmo sem a nova chave. | Difícil de reverter; não exige abstração nova. | Sessão, 2026-10-20. |
| D3 | Ler a configuração por chamada do método privado; não criar singleton, cache estático, service ou provider. | Escolha rotineira, sem novo contrato observável de atualização em tempo real. | Difícil de reverter. | Sessão, 2026-10-20. |
| D4 | Reutilizar `Log::channel('ai')`; manter a mensagem de warning existente do middleware. | Convenção da camada confirmada no step 3. | Difícil de reverter. | Sessão, 2026-10-20. |
| D5 | Propor teste de backend com configuração real do container e sem chamada de IA externa. | Proposta para o step 7; nenhuma costura foi confirmada antecipadamente. | Difícil de reverter. | Sessão, 2026-10-20. |

As políticas de Q1/Q2 são requisito, não desenho. Não foram decididas pelo desenvolvedor nem convertidas em D-nn ou ADR.

## Autorização

Nenhuma policy, gate, guard ou middleware HTTP novo. A leitura ocorre na classe já usada pelos guardrails. O ajuste será feito na configuração da instalação; o card não cria permissão de edição por painel nem persistência por tenant. Foram inspecionados `app/Policies`, `Gate::define` nos providers e `bootstrap/app.php`; não há autorização nova a projetar.

## Rotas

Nenhuma rota nova ou alterada. `routes/web.php` foi lido; `routes/api.php` não existe. `php artisan route:list --except-vendor` falhou por ausência de `vendor/autoload.php`; não se afirma inventário dinâmico completo.

## Superfície de UI

Sem superfície de UI nesta entrega, conforme RQ-07. Nenhuma página, widget ou componente será criado ou editado. O chat existente é consumidor indireto da mesma classe. Sem nova costura que só navegador possa provar; a decisão formal do `05-casos-de-teste-browser.md` pertence ao step 7.

## Variáveis de Ambiente

Nenhuma chave `.env` nova. O mapa ficará em configuração PHP; não serializar regex em JSON de `.env` nem ler `env()` no redator. `.env.example` foi inspecionado para as opções existentes de IA.

Para instalações com cache, a alteração de configuração requer regenerar o cache pelo processo normal de deploy. Isso não promete atualização instantânea de workers ou processos longos; seguir o ciclo operacional Laravel existente. Nenhum comando de cache foi executado nesta sessão.

## Eventos / Listeners / Observers

Nenhum novo ou alterado. A feature não grava models nem altera os eventos do ledger.

## Jobs / Queues

Nenhum job ou configuração de fila novo. Consumidores existentes usam o mesmo redator. Não adicionar polling, invalidação distribuída ou trabalho adiado.

## Modelo de Execução

| Pergunta | Resposta |
|---|---|
| Requests adicionais | Nenhum; execução síncrona dentro do caminho de IA existente. |
| Trabalho adiado | Nenhum. |
| Memoização por request | Nenhuma nova. Ambos os métodos chamam o mesmo resolvedor privado. |
| Cache entre requests | Somente o mecanismo de configuração já usado pelo Laravel; sem cache próprio do redator. |
| Banco e rede | O resolvedor e as regex não precisam de query nem de chamada ao provider. Custos anteriores do restante do pipeline não são atribuídos a esta feature. |
| Processamento | Manter os percursos existentes do mapa. Não fundir detecção e redação: isso mudaria a semântica observada em sobreposições. |

## Impacto em Features Existentes

- Redação do prompt: ordem diferente pode mascarar trechos diferentes nas sobreposições numéricas.
- Tipos para log: a detecção deve usar a mesma configuração, preservando a consulta ao texto original recebido pelo método.
- Resolução de guardrails e assistente: preservar injeção e pipeline; rodar a regressão `tests/Kit/IaTest.php` e a suíte Kit exigida por `wikis/ia.md` numa futura implementação.
- Configuração antiga: ausência da nova chave precisa continuar funcionando. Duplicação entre defaults publicados e fallback é um risco de deriva a provar por teste.
- Filtro de saída sensível: usa regras próprias e não será convertido junto com PII.

## Rollback

Reverter a leitura configurável para o mapa anterior e retirar a nova opção da configuração, regenerando o cache pelo procedimento de deploy existente. Não há migration, dados a reverter nem feature flag. Rollback de código só poderá ocorrer numa futura sessão autorizada, com Git restaurado.

## Dependências

Nenhum pacote novo ou atualização. Antes da implementação, disponibilizar as dependências já travadas e confirmar as versões efetivamente instaladas. A restauração de `vendor` fica fora desta sessão e não foi executada.

`wikis/ia.md` exige `ai-sdk-development` ao mexer na camada. O SKILL.md não foi localizado nos diretórios de skills do projeto nem nas instalações locais consultadas. Não se simulou sua ativação. Para futura edição do pipeline/SDK, resolver essa ausência antes de depender de sua API.

## Riscos

- Configuração parcial/vazia e inválida: Q1/Q2 abertas. Não aplicar merge, desativação, exceção ou fallback não autorizado para esses casos.
- Erro PCRE em runtime: preservar o mecanismo atual no recorte de compatibilidade; Q2 deve esclarecer a política de novos valores inválidos. Não converter a recomendação de bloqueio em implementação.
- Regex válidas, porém muito amplas ou custosas: configuração deve ser revisada como código; não se promete detecção sem falsos positivos nem proteção contra toda expressão patológica.
- Ausência de vendor, MCP e Git: validação executável e baseline não foram produzidas. Não há evidência de testes verdes.

## Channel de Log da Feature

Canal existente: `ai`, confirmado em `config/logging.php:'ai':85` e no middleware. Não criar canal nem alterar `config/logging.php`. Não há trait de logging localizada; usar o formato manual da facade.

Todos os novos logs são metadados seguros: `origem` em lista fechada `configuracao`/`padroes_atuais`, `quantidade_padroes`, `quantidade_tipos` e código de erro controlado, quando aprovado. Não logar texto original, texto mascarado, padrões configurados, chaves arbitrárias, objetos de exceção, mensagem/trace bruto ou credenciais. O tipo só pode aparecer nos logs existentes como nome conhecido do catálogo.

## Estrutura de Implementação

### 1. Publicar a configuração padrão

> Skills futuras: `ponytail`; esta `feature-wiki` mantém o rastro. Nenhuma skill de implementação foi invocada agora.

- **Path a modificar**: `config/ai.php`.
- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-06, RQ-07.
- Adicionar `pii.padroes` com cópia literal do mapa de `PiiRedactor::PADROES`, preservando expressões, delimitadores, modificadores, chaves e ordem.
- A forma determinada é mapa completo com os tipos existentes na ordem atual. Valores são strings PCRE; não introduzir callbacks, nomes de classe ou execução dinâmica.
- Documentar no próprio comentário de configuração que se ajustam padrões, preservando os tipos e a prioridade exigidos. Não criar tela, arquivo de config separado ou chave de ambiente.
- Manter a constante existente como fallback para instalações sem a opção; não usar a constante como valor da configuração, pois isso impediria ajustar as expressões ali.
- **Logs**: nenhum no carregamento do arquivo de config. A leitura e o uso são observados nos pontos do passo 2, em `Log::channel('ai')`; configuração é declaração de dados.

### 2. Compartilhar a resolução entre redação e detecção

> Skills futuras: `ponytail`; resolver a disponibilidade de `ai-sdk-development` caso a execução passe a editar a camada de IA.

- **Path a modificar**: `app/Ai/Guardrails/PiiRedactor.php`.
- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07.
- Preservar as assinaturas públicas `redigir(string $texto): string` e `tiposDetectados(string $texto): array`.
- Acrescentar `private function padroes(): array`, com PHPDoc da forma `array{email: string, token: string, cnpj: string, cartao: string, cpf: string, telefone: string, ip: string}` para os recortes determinados.
- Resolver `config('ai.pii.padroes', self::PADROES)` no caminho determinado. Chave ausente retorna exatamente o mapa legado; mapa completo válido com a mesma ordem é usado por ambos os métodos.
- Não usar `?:`, conversão para array ou `?? self::PADROES` para tratar configuração presente: essas operações decidiriam os recortes Q1/Q2 sem resposta.
- Trocar a fonte dos dois `foreach` para o resolvedor. `redigir` mantém substituição sucessiva, marcador e comportamento do `preg_replace` existente. `tiposDetectados` mantém `preg_match(...) === 1` sobre o texto que recebeu e a lista na ordem atual. Não trocar pela análise do texto já mascarado.
- Preservar os comentários existentes. Acrescentar descrição da resolução sem apagar a explicação da prioridade e das heurísticas.
- **Bloqueado por**: Q1 — qualquer caminho de mapa parcial/vazio. Não escrever sua política nesta fase futura sem Adendo.
- **Bloqueado por**: Q2 — qualquer caminho de estrutura/valor/regex inválido. Não concluir esse handler nem declarar a feature integralmente pronta sem a definição.
- **Logs**: `Log::channel('ai')` em todos os pontos novos; forma manual. Em `padroes`, `debug` de início: `[PiiRedactor@padroes] Iniciando leitura dos padrões | operacao: resolver`, contexto `['operacao' => 'resolver']`; decisão de ausência em `warning`: `[PiiRedactor@padroes] Aplicando padrões atuais por ausência de configuração | origem: padroes_atuais`, contexto `['origem' => 'padroes_atuais']`; resolução normal em `debug`: `[PiiRedactor@padroes] Carregando padrões configurados | origem: configuracao`, contexto `['origem' => 'configuracao']`; sucesso em `debug`: `[PiiRedactor@padroes] Concluindo leitura dos padrões | status: resolvido`, contexto com `quantidade_padroes` e `origem`.
- Em `redigir`, início `debug`: `[PiiRedactor@redigir] Iniciando redação de PII | operacao: redigir`, contexto `['operacao' => 'redigir']`; conclusão `info`: `[PiiRedactor@redigir] Concluindo redação de PII | status: concluido`, contexto `['status' => 'concluido']`.
- Em `tiposDetectados`, início `debug`: `[PiiRedactor@tiposDetectados] Iniciando detecção de tipos | operacao: detectar`, contexto `['operacao' => 'detectar']`; conclusão `debug`: `[PiiRedactor@tiposDetectados] Concluindo detecção de tipos | status: concluido`, contexto com `quantidade_tipos`. Não registrar o conteúdo para distinguir texto com ou sem correspondência.
- Falhas de novos valores configurados: pontos e severidade do handler ficam pendentes de Q2. Se a resposta aprovar interrupção, o plano deverá ser atualizado antes do código, com erro seguro e sem prompt. Não adicionar `catch` que retorne texto cru.
- **Pipeline existente**: `PiiRedactorMiddleware::handle` conserva o warning atual em `ai`, a detecção sobre `$original`, o uso de `revise` e o encaminhamento. Não há edição planejada desse middleware nem do registry.

### 3. Provar compatibilidade e uso da configuração

> Skills futuras: `feature-test-design` somente no step 7; depois `ponytail` na implementação. Não derivar cenários a partir deste plano.

- **Paths previstos**: `tests/Feature/PadroesPiiConfiguraveis/PiiRedactorTest.php` e `tests/Kit/IaTest.php` (regressão existente; editar somente se a especificação do step 7 exigir). Não alterar `tests/Pest.php`.
- **Atende**: RQ-01, RQ-02, RQ-03, RQ-04, RQ-05, RQ-06, RQ-07.
- O `04-casos-de-teste.md` ainda não existe. Ele deve ser derivado do `00` no step 7, após os steps 5 e 6. Não fixar IDs de CT, datasets ou resultados esperados aqui.
- Direção de validação: cobrir equivalência do mapa padrão e fallback, consumo de padrões configurados pelos dois métodos, prioridade e marcador. O teste deve usar uma expectativa independente; não calcular o resultado esperado chamando o próprio redator.
- Proposta de costura: TestCase Laravel para disponibilizar `config()`, com restauração da configuração entre testes e sem rede. Não são necessários models, factories ou novos seeders para testar strings. Factories existentes foram inventariadas; a regressão do catálogo conserva seus seeders existentes.
- Criar o teste por Artisan somente na implementação autorizada, respeitando o nome sem prefixo de suíte e as opções reais de `make:test --help`.
- **Bloqueado por**: Q1 e Q2 somente para os respectivos testes de política ainda não definida; não escrever expectativas que convertam a recomendação em requisito.
- **Logs**: não adicionar logs de teste à aplicação. Conferir no futuro QA os logs do passo 2 no canal `ai`; não criar CT de log sem cláusula de auditoria no requisito.
- Executar os testes afetados e a regressão da camada de IA, registrando saída e baseline. O requisito de `wikis/ia.md` é `composer test:kit` antes de entregar mudanças em `app/Ai/`.

## Filosofia de Implementação

Na futura implementação autorizada, usar Ponytail: reutilizar o arquivo de configuração e a classe existentes, depois as APIs nativas. Não criar interface, service provider, repositório de padrões, cache, tabela, migration ou biblioteca de reconhecimento de entidades.

A wiki usa prosa normal. O host mantém Caveman na conversa por instrução superior; a referência empacotada recomenda `ultra`, mas não altera o modo efetivo desta sessão.

## Mapeamentos

Um mapa tipo → regex alimenta ambos os métodos. `email`, `token`, `cnpj`, `cartao`, `cpf`, `telefone`, `ip` permanecem os tipos e a prioridade determinados pelo legado e pela exigência de preservação. Não há mapeamento de API ou banco.

## Testes

Especificação e confirmação de costuras pertencem ao step 7. Nenhum `04`, CT ou teste executável foi criado nesta sessão. Nenhum CT-B é proposto para uma feature sem UI nova ou alterada.

## Verificação Final

Lista para a futura implementação; nenhum item foi executado nesta sessão:

- [ ] Confirmar versões instaladas e registrar baseline antes do primeiro commit, numa cópia com Git e dependências. Não alegar baseline de `main` a partir desta pasta sem `.git`.
- [ ] Executar `vendor/bin/pint --dirty --format agent` se houver PHP alterado.
- [ ] Rodar `php artisan test --compact tests/Feature/PadroesPiiConfiguraveis/PiiRedactorTest.php`.
- [ ] Rodar `php artisan test --compact tests/Kit/IaTest.php` e `composer test:kit` conforme a orientação da camada de IA.
- [ ] Planejar mutação dirigida após o `04`, usando o lançador Windows da skill; registrar duração e sobreviventes, sem score presumido.
- [ ] Rodar revisão independente do diff no step 9, reconciliação no step 10 e QA no step 11, respeitando os recortes bloqueados.
- [ ] Conferir ausência de query/rede nova no resolvedor. Browser/TIA não foram executados; TIA depende de Git e do ambiente restaurado. Respeitar a rule local de não paralelizar browser.

## Commits

Não há `.git` nesta pasta e nenhum commit será feito nesta sessão. Sugestões para quando houver autorização e repositório: `:memo: pii: planejar padrões configuráveis` e `:sparkles: pii: ler padrões da configuração com fallback legado`.
