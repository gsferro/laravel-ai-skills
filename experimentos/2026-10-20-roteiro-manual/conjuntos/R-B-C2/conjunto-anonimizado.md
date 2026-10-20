# Casos de Teste — FERRO-830: Aprovação de solicitação de compra

> Requisito: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`.
> Plano: `wikis/specs/oraculo/aprovacao-de-compra/01-plano-acao.md`, usado apenas para localizar paths, rotas e superfície.
> **Derivado do requisito, não do plano.** Nenhum código da implementação da feature foi lido.
> Data: 2026-10-20. feature-wiki **[VERSÃO ANONIMIZADA]**, step **7**; feature-test-design **[VERSÃO ANONIMIZADA]**, passos 0–7.
> Host: Codex, família GPT-6; identificador exato de modelo/esforço não exposto nesta sessão.
> **Revisão adversarial: RODOU — duas rodadas independentes, 15 + 7 achados fechados. Teto de duas rodadas atingido; CT-68/69 foram acrescentados no fechamento final e não receberam terceira revisão.**
> **02 ausente:** não foi criado. A falta da Superfície Livewire limita a completude da taxonomia; ver L1–L4.

## Perfil de Derivação

Perfis decididos pelo **passo 0**, sem perfil imposto pela rodada. Regra que atravessa áreas herda o maior rigor. Toda área abaixo executou passos 1–7; nenhuma caiu em mínimo. A revisão cobre todas as áreas, inclusive padrão.

| Área | P | I | P×I | Perfil | Fundamento |
|---|---|---|---|---|---|
| Cadastro | 2 | 3 | 6 | padrão | Gravação integrada ao formulário e referências; valor monetário |
| Fluxo | 3 | 3 | 9 | completo | Estado, alçada, reentrada e ordem de aprovação; dinheiro |
| Autorização | 3 | 3 | 9 | completo | Identidade, função, organização e tentativas fora da UI |
| Efeitos | 3 | 3 | 9 | completo | E-mail, múltiplos diretores, retries e concorrência |
| Apresentação | 2 | 2 | 4 | padrão | Integração com listagem e detalhe; informação errada causa retrabalho |
| Interface | 2 | 2 | 4 | padrão | Modal de rejeição e JavaScript; falha impede completar a tarefa |

- Há **Impacto 3** em Cadastro, Fluxo, Autorização e Efeitos.
- Técnicas: EP, BVA 3-valores com centavo, decisão completa, papel × ação, estado × operação, 2-switch, rastreio de efeito e concorrência.
- Não há parâmetro independente de configuração com domínio determinado que justifique pairwise: estado, ator e alçada são condições dependentes. Foram usados os produtos críticos completos, sem substituir regra de autorização por amostragem.
- Cenários: 69 · Regras: 19 · Mutantes previstos: 106 · Sem matador: 0.
- A contagem de cenários é de blocos no 04; um esquema conta uma vez. CT-B: 1 no 05. As linhas de exemplos são execuções independentes.
- Mutantes do 04 incluem os de R19, cujos matadores estão no 05. A cópia de referência no 05 não se soma outra vez.
- Gate de especificação não equivale a testes executados nem a mutation score medido.

## Entrada, precedência e limites

O 00 tem 14 RQ, sem coluna Estado e sem seção P-nn. As premissas vigentes estão em **A-01–A-12**, inclusive A-09 aninhada após A-08. São decisões dadas pelo usuário: não foram reabertas por esta derivação. A-06 prevalece sobre a leitura literal de cancelar no rascunho; A-07 autoriza rejeição pelo diretor. Nenhuma RQ inteira foi marcada aberta. Perguntas novas bloqueiam apenas seus recortes.

Foram lidos 00 e 01 inteiros conforme a tarefa; somente o 00 forneceu comportamento esperado. Do 02 não houve leitura porque o arquivo não existe. Não há `wikis/glossario.md`; os termos seguem o 00.

As rules `.ai/rules/index.md`, `testes.md`, `filament.md` e `testes-browser.md` foram consideradas. Busca complementar: `rg -n -i 'teste|gherkin|wiki|compra|aprova|document|specs' .ai/rules`. A regra de browser **proíbe --parallel** neste projeto e prevalece sobre a referência genérica que o permite sob condições. Helpers compartilhados pertencem a `tests/Pest.php`.

Evidência do ambiente: `composer show --direct` retornou **No dependencies installed**; `Test-Path vendor` retornou **False**. `composer show --locked --direct` e leitura de `composer.lock` confirmaram Laravel **13.25.0**, Filament **5.7.6**, Livewire **4.4.0**, Pest **5.1.1**, browser **5.0.1**, mutate **5.0.2**. São versões **travadas**, não instalação executável. PHP CLI **8.4.10**, Xdebug **3.4.4**. Playwright declarado `^1.62.1`; instalação efetiva de Node/browser não foi certificada.

O plugin mutate está no lock como dependência transitiva e **não** em require-dev de `composer.json`; não foi alterado. A futura implementação deverá resolver sua declaração com autorização para dependências. Não há `pestphp/pest-plugin-livewire` no lock: o padrão existente usa `Livewire\\Livewire::test()`, sem depender do helper Pest\\Livewire.

Boost `search-docs`/schema não aparecem nas ferramentas expostas. O fallback foi documentação oficial: [recursos Filament 5](https://filamentphp.com/docs/5.x/testing/testing-resources), [ações Filament 5](https://filamentphp.com/docs/5.x/testing/testing-actions), [notificações Laravel 13](https://laravel.com/framework/docs/13.x/notifications#testing) e [browser Pest](https://pestphp.com/docs/browser-testing). A inspeção de `@deprecated` no vendor não pôde ocorrer. Não se usam helpers antigos nem se declara API local verificada por execução.

`git status --short` retornou **fatal: not a git repository**. A integridade será conferida por hashes dos arquivos relevantes; não há diff Git a certificar. Nenhum arquivo de produção ou teste Pest será escrito. Não se executam etapas 8–12, QA, implantação, instalação ou mutation testing nesta entrega de especificação.

## Varredura SFDIPOT

| Letra | O que existe nesta feature | Destino |
|---|---|---|
| S | Solicitação, centro, decisões de etapas, UI e e-mail; três entidades persistidas | R1–R19; IDOR/MA por tabela no checklist |
| F | Criar, editar, excluir, enviar, decidir, devolver, reenviar, cancelar, exibir | Matriz única abaixo; CT-01–CT-62 |
| D | Dinheiro em decimal, limiar 5000, justificativa, FK, identidade, organização, histórico | R1, R5, R7, R8, R13–R16; Q1/Q2 |
| I | Chamada direta do domínio, páginas de resource, ações Livewire e modal JS | Grupos confirmados abaixo; CT-B01; L1/L2 |
| P | PHP 8.4; stack travada; SQLite :memory: no arnês; concorrência exige DB compartilhado | Setup; CT-38–40 com execução futura pendente |
| O | Solicitante, gestor por centro, diretores 1/N; administração; acúmulos; retries | R4, R6, R10, R12, R14 |
| T | Ordem gestor/diretor, ciclos e decisões concorrentes; instantes do histórico | R5, R8, R10, R16; Q6. SLA, expiração e DST de prazo não se aplicam: fora do 00 |

## Matriz única de estado × operação

**Inventário sem ler implementação:** o enum planejado não está materializado como entrada de comportamento. Os cinco valores são os estados nomeados nas premissas do 00 e necessários ao fluxo. Rejeitada é evento que devolve a rascunho. Não se criou sexto estado. Criar parte da inexistência e é coberto por CT-01/03; registro excluído é pós-condição de remoção e é coberto por CT-11/62, fora do enum.

**5 estados × 8 operações = 40 células: 19 válidas e 21 inválidas.** Todas as 21 inválidas de escrita têm execução direta; leituras são de um leitor já autorizado, sem decidir Q4. A face de persona/campo é ampliada por CT-05/06/10/13/21/22/23/32/44/46 e CT-58/59.

| Estado | editar | excluir | enviar | aprovar | rejeitar | cancelar | listar | visualizar |
|---|---|---|---|---|---|---|---|---|
| rascunho | V CT-04/07 | V CT-08 | V CT-12 | X CT-20 | X CT-26 | X CT-33 | V CT-55 lista | V CT-55 detalhe |
| aguardando_gestor | X CT-05 | X CT-09 | X CT-14 | V CT-17 | V CT-24 | V CT-31 | V CT-55 lista | V CT-55 detalhe |
| aguardando_diretor | X CT-05 | X CT-09 | X CT-14 | V CT-19 | V CT-24 | V CT-31 | V CT-55 lista | V CT-55 detalhe |
| aprovada | X CT-05 | X CT-09 | X CT-14 | X CT-20 | X CT-26 | X CT-33 | V CT-55 lista | V CT-55 detalhe |
| cancelada | X CT-05 | X CT-09 | X CT-14 | X CT-20 | X CT-26 | X CT-33 | V CT-55 lista | V CT-55 detalhe |

Legenda auditada por operação:
- **V editar:** mesmos registro e rascunho, dados novos efetivos; zero decisão/e-mail novo. **X:** mesmos dados, situação, existência e histórico, zero decisão/e-mail novo.
- **V excluir:** indisponível para uso, sem decisão/e-mail novo. **X:** registro, dados, situação e histórico intactos, zero e-mail.
- **V enviar:** aguardando_gestor, sem decisão nova, um e-mail ao gestor certo. **X:** estado/dados/histórico intactos e zero e-mail novo.
- **V aprovar:** decisão da etapa e autor corretos, destino segundo alçada; um e-mail por diretor somente ao abrir a segunda etapa. **X:** estado/dados/histórico intactos e zero e-mail novo.
- **V rejeitar:** rascunho e decisão rejeitada com autor/justificativa; zero e-mail. **X:** estado/dados/histórico intactos e zero e-mail.
- **V cancelar:** cancelada, sem decisão nova, sem e-mail. **X:** existência, estado/dados/histórico intactos e zero e-mail.
- **V listar/visualizar:** conteúdo da própria compra com situação correta; listagem não substitui evidência de detalhe.

## Tabela de decisão e matriz de pessoas

Condições colapsadas apenas quando não mudam o resultado: fora do rascunho, editar/excluir/enviar são recusados independentemente da alçada; fora de trânsito, cancelar é recusado independentemente do ator. Os esquemas de estados executam cada caso.

| Situação / intenção | Ator e condições | Resultado | Evidência |
|---|---|---|---|
| rascunho / editar, excluir, enviar | solicitante; gestor existe para enviar | permitido | CT-04,08,12 |
| rascunho / editar, excluir, enviar | outro usuário da mesma organização | recusado, verbo a verbo | CT-06,10,13 |
| rascunho / enviar | solicitante; gestor ausente | recusa, mantém rascunho | CT-15 |
| aguardando_gestor / aprovar | gestor específico; valor ≤ limite | aprovada, uma etapa | CT-17/18 |
| aguardando_gestor / aprovar | gestor específico; valor > limite; 1/N diretores | aguardando_diretor, uma etapa | CT-17/18/42 |
| aguardando_gestor / aprovar | gestor específico; valor > limite; zero diretores | recorte aberto Q3; aprovação final sem diretor continua vedada | CT-63 para o invariante; destino pendente Q3 |
| aguardando_gestor / rejeitar | gestor específico; justificativa com conteúdo | rascunho, uma rejeição | CT-24 |
| aguardando_diretor / aprovar ou rejeitar | diretor da organização; justificativa válida na rejeição | aprovada ou rascunho | CT-19/24 |
| qualquer etapa / rejeitar | ator correto; justificativa sem conteúdo | recusa sem efeitos | CT-25 |
| etapa pendente / aprovar ou rejeitar | gestor errado, etapa errada ou usuário sem papel contextual | recusa em ambos os verbos | CT-21/22/46 |
| trânsito / cancelar | solicitante | cancelada | CT-31 |
| trânsito / cancelar | outro usuário | recusa | CT-32 |
| etapas pendentes / decidir | solicitante+gestor, solicitante+diretor, gestor+diretor elegível | decide só a etapa corrente | CT-23 |
| qualquer estado / mutação estrangeira | identidade só de outra organização | recusa | CT-44 |
## Mapa de Regras

| Regra | Área (perfil herdado) | Origem | Técnica | Cenários |
|---|---|---|---|---|
| R1 — A solicitação nasce em rascunho com os três dados obrigatórios | Cadastro (padrão) | RQ-01; A-01 | EP; BVA 3-valores escalada para preservação de centavos | CT-01, CT-02, CT-03 |
| R2 — Somente o solicitante edita, e somente em rascunho | Autorização (completo) | RQ-02; RQ-09; RQ-10; A-05 | estado × operação; papel × ação; EP | CT-04, CT-05, CT-06, CT-07 |
| R3 — Somente o solicitante exclui o rascunho | Autorização (completo) | RQ-03; RQ-10; A-05 | estado × operação; papel × ação; rastreio de efeito | CT-08, CT-09, CT-10, CT-11 |
| R4 — O envio do solicitante encaminha ao gestor do centro de custo | Fluxo (completo) | RQ-04; RQ-09; A-02; A-10 | estado × operação; papel × ação; rastreio de efeito | CT-12, CT-13, CT-14, CT-15, CT-16, CT-68 |
| R5 — A aprovação do gestor respeita a alçada estrita e antecede o diretor | Fluxo (completo) | RQ-05; RQ-06; A-03; A-04 | BVA 3-valores; tabela de decisão; estado × operação | CT-17, CT-18, CT-19, CT-20, CT-63 |
| R6 — Cada verbo de decisão exige a identidade da etapa corrente | Autorização (completo) | RQ-04; RQ-05; RQ-06; A-02; A-03; A-07; A-09 | matriz papel × ação; tabela de decisão completa | CT-21, CT-22, CT-23 |
| R7 — A rejeição justificada devolve ao rascunho | Fluxo (completo) | RQ-06; RQ-07; RQ-08; A-07; A-11 | EP; estado × operação; rastreio de efeito | CT-24, CT-25, CT-26, CT-27, CT-28 |
| R8 — A correção inicia novo ciclo pelo gestor sem reaproveitar aprovação anterior | Fluxo (completo) | RQ-09; RQ-05; RQ-13; A-12 | 2-switch; EP × rastreio de efeito | CT-29, CT-30, CT-69 |
| R9 — O solicitante cancela somente enquanto aguarda aprovação | Autorização (completo) | RQ-11; RQ-10; A-05; A-06 | estado × operação; papel × ação; rastreio de efeito | CT-31, CT-32, CT-33, CT-34 |
| R10 — Uma etapa elegível admite uma única decisão persistida | Efeitos (completo) | RQ-05; RQ-06; RQ-08; RQ-11; RQ-13; RQ-14; A-03 | idempotência no agregado; concorrência real | CT-35, CT-36, CT-37, CT-38, CT-39 |
| R11 — Estado, histórico e encaminhamento não ficam parcialmente confirmados | Efeitos (completo) | RQ-05; RQ-06; RQ-08; RQ-13; RQ-14 | rastreio de efeito com falha após o ponto do efeito | CT-40 |
| R12 — E-mail vai a todos e somente aos aprovadores da próxima etapa | Efeitos (completo) | RQ-14; RQ-04; RQ-05; A-03; A-11 | EP × rastreio de efeito; cardinalidade 0/1/N | CT-41, CT-42, CT-43, CT-67 |
| R13 — As referências de organização não permitem operar compras de terceiros | Autorização (completo) | RQ-01; RQ-02; RQ-03; RQ-04; RQ-05; RQ-06; RQ-11; A-01; A-03 | IDOR; matriz papel × ação; EP por fronteira | CT-44, CT-45, CT-46, CT-47, CT-66 |
| R14 — O cadastro do centro de custo pertence à administração da organização | Autorização (completo) | RQ-01; RQ-04; A-01; A-02; A-08 | papel × ação; EP; gravação por componente | CT-48, CT-49, CT-50, CT-51, CT-64 |
| R15 — Payload do cliente não pode forjar posse, situação ou decisões | Autorização (completo) | RQ-01; RQ-02; RQ-04; RQ-05; RQ-10; RQ-13; A-01; A-08 | mass assignment por entidade; EP | CT-52, CT-53, CT-54 |
| R16 — A tela informa a situação corrente e os autores das etapas | Apresentação (padrão) | RQ-12; RQ-13; A-12 | EP exaustiva de estados; rastreio de histórico | CT-55, CT-56, CT-57 |
| R17 — A interface oferece somente ações permitidas para a persona e a situação | Autorização (completo) | RQ-02; RQ-03; RQ-04; RQ-05; RQ-06; RQ-11; A-06; A-08; A-09 | matriz papel × ação × situação | CT-58, CT-59, CT-65 |
| R18 — As páginas e coleções mostram os registros corretos e têm saída de erro | Apresentação (padrão) | RQ-01; RQ-02; RQ-12; RQ-13; A-01; A-12 | EP; cardinalidade; CRUD | CT-60, CT-61, CT-62 |
| R19 — A modal de rejeição funciona com JavaScript executado | Interface (padrão) | RQ-07; RQ-08; A-07; superfície de UI: Modal Rejeitar | rastreio de interação real | CT-B01 (05) |

As 14 RQ têm partes determinadas discriminadas. RQ-01: R1/R2; RQ-02: R2; RQ-03: R3; RQ-04: R4/R6; RQ-05: R5/R6/R8; RQ-06: R5/R6/R7; RQ-07: R7/R19; RQ-08: R7; RQ-09: R2/R8; RQ-10: R2/R3/R4/R5/R7/R9; RQ-11: R9/R10; RQ-12: R16/R18; RQ-13: R5/R7/R8/R10/R11/R16; RQ-14: R4/R5/R8/R10/R11/R12.

| Premissa vigente do 00 | Destino discriminante |
|---|---|
| A-01 — entidade centro por organização | R1, R13–R15; CT-45/48/49/51/53 |
| A-02 — um gestor específico por centro | R4/R6; CT-12/21/22 |
| A-03 — diretores da organização, todos avisados, primeira decisão resolve | R6/R10/R12; CT-23/36/38/42/46 |
| A-04 — >5000 e limite configurável | R5; CT-17/18 |
| A-05 — aprovada terminal | Matriz de estados; CT-05/09/14/20/26/33 |
| A-06 — cancela em trânsito, no rascunho exclui | R3/R9/R17; CT-08/31/33/58 |
| A-07 — diretor também rejeita | R6/R7; CT-22/24/25 |
| A-08 — centro é administração, fora do panel_user | R14; CT-48–51 |
| A-09 — solicitante pode ser gestor | R6; CT-23 |
| A-10 — sem gestor, envio falha fechado | R4; CT-15 |
| A-11 — somente próximo aprovador é notificado | R12; CT-41–43 |
| A-12 — situação na lista/detalhe e histórico com autor/instante/justificativa | R16; CT-55–57 |

## Costuras de Teste

Confirmadas pela **sessão principal em 2026-10-20**, sob autorização expressa para derivar sem perguntas e seguindo o arnês existente. “Existente” qualifica a modalidade e helpers; arquivos de compra são destinos novos, não testes implementados. Confirmação de costura não certifica runtime.

| Grupo | Regras | Costura | Existente ou nova | Por que esta camada | Confirmada |
|---|---|---|---|---|---|
| Domínio e persistência | R1–R12, R14, R15, R18 | Pest feature HTTP | Existente: tests/Feature com TestCase; chamadas diretas como convenção de tests/Kit | Banco, ator e efeitos; aplicação inicializada; prova fora da UI | Sessão principal, 2026-10-20 |
| Formulários e leitura | R1, R2, R4, R7, R14, R16–R18 | componente Livewire/Filament | Existente: Livewire::test, painel e RefreshDatabase em testes irmãos | Estado do formulário, gravação, tabela, infolist e ações | Sessão principal, 2026-10-20 |
| Fronteiras por organização | R12, R13, R15 | Pest feature HTTP | Nova ligação em tests/FeatureTenancy, reutilizando TenancyTestCase e helpers existentes | TestCase normal não liga tenancy antes das migrations; testes de negócio não vão para grupo kit | Sessão principal, 2026-10-20; bootstrap futuro pendente |
| Componentes por organização | R13, R14, R15 | componente Livewire/Filament | Mesma nova ligação FeatureTenancy; padrão de tests/Tenancy/AdminDaOrganizacaoTest.php | Escrita de centros e payload de filha no contexto real | Sessão principal, 2026-10-20; bootstrap futuro pendente |
| Concorrência compartilhada | R10 | Pest feature HTTP | Nova, necessária: banco/fixtures compartilhados por dois workers com barreira | Arnês de testes sequenciais com SQLite :memory: não prova concorrência | Sessão principal, 2026-10-20; execução futura pendente |
| Modal JS | R19 | browser | Existente: tests/Browser, TestCase e browser timeout do projeto | Prova abertura, edição e submissão no JS do navegador | Sessão principal, 2026-10-20 |

## Fronteira com o Plano

| Item do PRD | Tratamento | Destino |
|---|---|---|
| Paths de Models/Resources, páginas e rotas | Localizadores permitidos, sem inferir comportamento da implementação | Setup, índice e roteiro do 05 |
| Campos/tabela/nomes de métodos | Detalhes para prender o teste, nunca fonte do resultado | Then vem de RQ/A vigente |
| varchar 255/120, minValue(0.01), unique no nome | Política não determinada pelo 00; recusada como oráculo | Q1/Q2; unicidade precisa de requisito antes de CT direcional |
| Enums, cores, HasColor, prefixo de moeda e mensagens literais | Escolhas de implementação/apresentação não prometidas literalmente | Não gerar teste de API nem pixel a partir delas |
| Obrigação de criar 05 porque várias telas usam JS | Gate antigo do PRD não decide esta derivação | 05 existe somente pelo observável JS de R19 |
| URL no e-mail e visibilidade por permission pura | O 00 não exige link nem recorte de leitores completo | Q4; não certificar link que ainda não é contrato |
| UPDATE condicional, DB::transaction, ShouldQueue e append-only como estrutura | Não são o oráculo; contam somente seus efeitos observáveis determinados | R8/R10/R11; mecanismo de commit pendente |
| CT-xx citados nos textos antigos do 00/01 | Não importados como cenários nem IDs deste conjunto | Numeração abaixo é própria desta saída |
| Auditoria técnica/logs e contagem exata de permissions | Não importar exigências só do PRD | Sem CT autônomo de logger; CT-15 verifica warning explicitamente dado em A-10; sem números de permissão copiados |
## Perguntas para o 00-requisito.md

**Desvio autorizado:** o 00 é imutável e o usuário indisponível. As perguntas ficam neste bloco pronto para reconciliação futura, sem editar o 00 nem criar o 03. A-01–A-12 continuam vigentes. Recomendações não são respostas assumidas.

| ID | Pergunta | Afeta | Recomendação | Estado |
|---|---|---|---|---|
| Q1 | Quais limites de valor, escala decimal e tratamento de zero, negativo e fração de centavo valem na criação, edição e envio? | RQ-01, RQ-04; R1 | Falhar fechado para valor sem representação monetária válida; definir mínimo, máximo e escala antes de derivar seus BVA. Não importar 0,01 do plano como política | aberta — somente faixas/escala |
| Q2 | Quais tetos de caracteres e tratamento de espaços nas bordas valem para descrição, nome do centro e justificativa, em todas as entradas? | RQ-01, RQ-07; A-01 | Definir tetos explícitos; recusar excesso sem truncar. Após resposta, cobrir n−1/n/n+1 diretamente e no formulário. Não importar 255/120 do PRD | aberta — somente teto/normalização |
| Q3 | Sem diretor atribuído, a aprovação do gestor acima da alçada é recusada ou a compra aguarda diretor a atribuir? | RQ-05, RQ-14; A-03 | Falhar fechado quanto à aprovação final e informar ausência; preferir recusar a passagem sem destinatário até definição. Jamais aprovar definitivamente sem diretor | aberta — somente zero diretores |
| Q4 | Quem consulta compras de outros solicitantes da mesma organização? Participantes anteriores continuam leitores? A notificação deve ter link, e para qual destino autorizado? | RQ-12, RQ-13, RQ-14; A-12 | Manter somente acesso explicitamente autorizado até definir recorte; se houver link, garantir destino autorizado para o destinatário. Não inventar acesso geral ou retenção de permissão histórica | aberta — somente visibilidade/link |
| Q5 | O gestor deve ser membro atual da organização? Trocar/remover gestor durante uma solicitação enviada altera a pessoa elegível? | RQ-04; A-01, A-02 | Falhar fechado para referência sem vínculo válido; decidir se o responsável é atual ou congelado no envio. Os CT definidos usam gestor estável e válido | aberta — somente vínculo/troca em trânsito |
| Q6 | Qual fuso e formato devem ser exibidos nos instantes das etapas? | RQ-13; A-12 | Definir explicitamente; até lá provar autor, instante correspondente e ordem, sem fixar apresentação por fuso | aberta — somente apresentação temporal |
| Q7 | Falha de transporte depois de confirmar a decisão exige retry, erro ao usuário ou outra recuperação? | RQ-14 | Nunca afirmar entrega inexistente; definir recuperação sem duplicar decisão nem aviso. Não exigir rollback de compra já confirmada por uma escolha de implementação | aberta — somente falha pós-commit |
| Q8 | Exclusão de rascunho é física ou lógica? Qual retenção do histórico de um rascunho excluído? | RQ-03; RQ-13 | Manter indisponível para escrita em qualquer mecanismo; preservar histórico até decisão explícita de retenção. Não usar mecanismo para eliminar CT-11 | aberta — desenho/retencão |
| Q9 | Há ordem estável, tamanho de página contratual e semântica para inserção entre páginas? | RQ-12; A-12 | Definir desempate estável e expectativa de paginação antes de afirmar posição exata sob inserção | aberta — somente política da coleção |
| Q10 | Como distinguir retry de criação de uma segunda solicitação intencional idêntica? | RQ-01 | Não eliminar compra legítima por igualdade de campos; decidir chave da intenção e política antes do cenário de duplicidade de criação | aberta — somente idempotência da criação |

Formato de entrevista preservado para encaminhamento:

❓ Q1 · raia: requisito · afeta: RQ-01, RQ-04 (faixas e escala) · depende de: —
Quais são os limites monetários e o tratamento de valores sem centavo exato?
➡️ Recomendação: falhar fechado para valores fora do domínio acordado; não inventar aceitação nem BVA com limite do plano.

❓ Q2 · raia: requisito · afeta: RQ-01, RQ-07, A-01 (tetos e normalização) · depende de: —
Quais tetos e normalizações valem para os três textos livres?
➡️ Recomendação: tetos explícitos e excesso recusado; manter já coberta a obrigatoriedade sem conteúdo.

❓ Q3 · raia: requisito · afeta: RQ-05, RQ-14 (zero diretores) · depende de: —
Como proceder sem diretor atribuído?
➡️ Recomendação: falhar fechado quanto à aprovação final e tornar a ausência visível.

❓ Q4 · raia: requisito · afeta: RQ-12, RQ-13, RQ-14 (recorte de leitores e link) · depende de: —
Quem pode ler e qual destino do eventual link?
➡️ Recomendação: nenhum acesso além do explicitamente autorizado enquanto faltar a decisão.

❓ Q5 · raia: requisito · afeta: RQ-04 (mudança/vínculo do gestor) · depende de: —
O aprovador é congelado no envio ou é o gestor atual?
➡️ Recomendação: falhar fechado quando a referência não for válida; decidir a política de troca.

❓ Q6 · raia: requisito · afeta: RQ-13, A-12 (fuso/formato) · depende de: —
Qual é a apresentação temporal esperada?
➡️ Recomendação: especificar fuso e formato sem substituir a prova já determinada de autor/ordem.

❓ Q7 · raia: requisito · afeta: RQ-14 (falha após commit) · depende de: —
Qual recuperação é exigida quando o transporte falha depois da confirmação?
➡️ Recomendação: registrar entrega pendente e permitir recuperação sem duplicar decisão ou e-mail.

❓ Q8 · raia: requisito · afeta: RQ-03, RQ-13 · depende de: —
Qual mecanismo de exclusão e retenção será adotado?
➡️ Recomendação: preservar indisponibilidade efetiva; retenção não decidida não autoriza apagar histórico silenciosamente.

❓ Q9 · raia: requisito · afeta: RQ-12 (ordenação e paginação) · depende de: —
Qual contrato da coleção sob inserção concorrente?
➡️ Recomendação: desempate estável sem afirmar posição que o requisito não determina.

❓ Q10 · raia: requisito · afeta: RQ-01 (identidade da criação) · depende de: —
Qual identidade de intenção distingue retry de nova compra?
➡️ Recomendação: definir chave antes de rejeitar compras iguais; nenhuma asserção de deduplicação foi inventada.

Não há mudança de Estado no 00. A rastreabilidade das partes determinadas permanece no mapa; cada lacuna cita seu recorte.

## Setup Global

### Arnês e personas

- Reutilizar `Tests\\TestCase` + `RefreshDatabase` de `tests/Feature`; `tests/Unit` não tem TestCase de aplicação. Nenhum observável deste conjunto é só cálculo puro: todos dependem de persistência, identidade, UI ou efeitos; portanto nenhum caso foi forçado a Unit.
- Reutilizar `Tests\\TenancyTestCase`, `noPainelDa()`, `papelNaOrganizacao()` e `pivotDePapeis()` de `tests/Pest.php`. O modo tenancy precisa ser fixado antes das migrations. A pasta `tests/FeatureTenancy` e sua ligação/suíte ainda são uma costura nova proposta pelo path do plano, não arquivo de teste já existente.
- Cenários sem tenancy usam banco do modo padrão; cenários de fronteira usam Acme e Globex, com pessoas e compras reais em ambas.
- Ana: solicitante, `panel_user`. Bruno: gestor específico de Compras, sem papel diretor. Carlos: outro solicitante/gestor de Viagens. Diana e Elisa: diretoras de Acme. Um diretor exclusivo de Globex torna o vazamento observável.
- Nomes são distintos e os atores não se confundem, exceto CT-23/58, que exercitam o acúmulo explicitamente. Diretores são atribuídos no contexto da organização.
- Autenticar antes de todo teste de painel. Definir painel e contexto de permissões nos componentes; os componentes não executam automaticamente o middleware de um request de página.
- Reutilizar factories existentes de `User` e `Tenant`. Seus states confirmados incluem `unverified()`, `comIdentidadeVisual()` e `inativo()`, que não são necessários a este domínio.
- Não existem factories das três entidades de compra no inventário `database/factories`. O futuro setup usará a entrada real de criação do domínio (ou `Model::create` com dados legítimos, após autorização da entrada), sem inventar factory ou state. Não criar models nesta entrega.

### Estados por transições reais

Prever helper compartilhado `solicitacaoEm(string $situacao, array $dados = [])` **em tests/Pest.php**, ainda não escrito:
1. Criar rascunho legítimo com identidade e contexto corretos.
2. Para aguardando_gestor, chamar o envio real por Ana.
3. Para aguardando_diretor, criar valor acima da alçada, enviar e aprovar realmente como Bruno.
4. Para aprovada, seguir o caminho de uma ou duas etapas indicado no Dado.
5. Para cancelada, enviar e cancelar realmente como Ana.
6. Para rascunho reentrado, enviar e rejeitar com justificativa real; para segundo ciclo, corrigir e reenviar por chamadas reais.

Nunca `forceFill(['situacao' => ...])` para fabricar a partida. Retenção de instâncias antigas é deliberada nos retries; conferir com `fresh()` o agregado persistido. Guardar fotografia das decisões anteriores por identidade, compra, etapa, decisão, autor, instante e justificativa, não apenas contagem.

### Observação de efeitos

- Em cenários comuns, exceto CT-40/67, ativar `Notification::fake()` após as fixtures e limpar a observação após cada setup de transições. Confirmar destinatários exatos, canais `['mail']`, identidade da solicitação e etapa. Não usar `Mail::assertSent` para uma Notification enfileirada.
- Nos cenários de retry, observar desde a primeira intenção, sem limpar entre as duas chamadas. Nos ciclos, limpar apenas os avisos do ciclo anterior e declarar que o oráculo se refere a e-mails **novos**.
- Não aplicar `Event::fake()` antes de criar pessoas, organizações e compras: os eventos podem produzir UUID.
- CT-40 observa transporte e fila de teste de verdade ou spies restritos que preservem a semântica de commit. Fake que conta intenção antes do commit não é prova de entrega nem rollback.
- Não há CT autônomo de log derivado do PRD. A-10, premissa normativa dada pelo usuário, exige warning e ele é efeito auxiliar do CT-15. Não foram inventados job, evento ou contador de negócio.

CT-67 usa o transporte mail array e fila sync, sem Notification::fake nem Queue::fake: os dois tipos de aviso precisam chegar compostos ao transporte de teste, com destinatários e identidade da solicitação corretos. Limpar mensagens após o setup, antes da única ação medida. Não há envio externo real.

### Concorrência e confirmação

CT-38/39 exigem banco de teste compartilhado, duas conexões/processos independentes, fixtures confirmadas antes de iniciar workers, barreira depois das leituras elegíveis e releitura final por terceira conexão. Isolar por solicitação para não misturar rodadas. Não copiar SQLite `:memory:` independente para cada processo. O mecanismo exato será escolhido ao materializar testes; a especificação não afirma que foi executado.

No par aprovação de gestor × cancelamento, ambos podem ser válidos em ordem serial: gestor abre etapa de diretor, solicitante cancela antes da final. Conferir estado final cancelada, zero ou uma aprovação de gestor conforme o vencedor, e avisos correspondentes. Não confundir essa ordem válida com duplicação da mesma decisão.

CT-40 injeta falha tardia antes de confirmar a unidade de escrita, com destinatários existentes. Se a implementação agenda o e-mail depois do commit, a falha precisa acontecer depois de registrar esse agendamento e antes de commit, não antes da operação. Exigir prova dessa localização ao executar; ela está pendente, sem alegação de impossibilidade do arnês.

### APIs e arquivos futuros

`Livewire\\Livewire::test()`, `fillForm()`, `call('create')`, `call('save')` e `callAction(TestAction::make('nome')->table($registro))` seguem os testes irmãos e documentação oficial Filament 5. `record` recebe a chave de rota da entidade. Na edição, não exigir redirect. Asserções de banco verificam os campos relevantes, nunca só a chave. Não usar `assertFormSet`, `callTableAction` ou `assertTableActionExists`.

Toda API de domínio citada como enviar/aprovar/rejeitar/cancelar representa o verbo acordado; assinaturas e classes do plano são localizadores, não o oráculo. Na materialização, confirmar a API real sem alterar o Então.

Os paths do índice são **destinos propostos, não testes existentes**. Nenhum teste foi criado/executado. As ligações novas de FeatureTenancy, concorrência compartilhada e pontos de escrita administrativa precisam ser resolvidas antes de certificar execução.

## Lacunas declaradas

| ID | Recorte | O que foi verificado/tentado | Consequência |
|---|---|---|---|
| L1 | Superfície Livewire completa | `Test-Path` do 02 deu False; vendor também ausente. Não foi lida implementação para reconstruir a tabela | Não é possível enumerar todos os métodos/propriedades/tipos e consumos do framework; cobertura completa desta superfície não foi declarada |
| L2 | IDOR e escrita direta de etapas | O 00 exige histórico; 01 só localiza o pai e a UI; 02 não inventaria filhos. CT-54 tenta falsificar filha pelo pai | A proteção indireta tem cenário; pontos diretos de filha continuam não inventariados. Não presumir que ausência de Resource elimina entrada pública |
| L3 | Discriminante nulo e estado do framework | Sem 02/vendor, não há inventário de queries públicas nem filtros consumidos como índice/coluna/parse | Não fixar fail-closed de todo Model::query: a convenção permite consulta global em job sem tenant. Consultas públicas sem contexto exigem inventário e cenário específico |
| L4 | Entrada de domínio para administração de centros | Testes irmãos têm actions/policies, mas nenhuma API desta feature foi lida; CT-50 exige escrita fora da UI | Costura ainda a materializar. Esconder menu ou testar can() isoladamente não fecha o gate |
| L5 | Faixas, textos, zero diretores, visibilidade, tempo, recuperação e criação repetida | Perguntas Q1–Q10 registradas sem modificar a linha de base | Somente os recortes indecididos ficam sem oráculo direcional; as 14 RQ mantêm seus CT determinados |
| L6 | Prova de runtime, concorrência, commit e mutação | vendor ausente; nenhum teste Pest autorizado nesta tarefa | Gate de falsificabilidade é de especificação. CT-38–40 e score não foram certificados por execução |


## Regra R1 — A solicitação nasce em rascunho com os três dados obrigatórios

> Origem: RQ-01; A-01. Perfil **padrão**. Técnica: **EP; BVA 3-valores escalada para preservação de centavos**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A solicitação nasce em rascunho com os três dados obrigatórios

    Esquema do Cenário: [CT-01] O solicitante cria um rascunho completo
      Dado Ana autenticada com papel <papel>, o centro Compras de Acme com gestor Bruno, dois diretores e nenhuma solicitação
      Quando Ana cria por fora da UI uma solicitação com descrição "Aquisição de café ☕", valor decimal <valor> e centro Compras
      Então existe uma única solicitação em rascunho de Ana em Acme com exatamente essa descrição, valor <valor> e centro
      E existem zero decisões de etapa e zero e-mails para Bruno, diretores e Ana

      Exemplos:
        | papel | valor | # borda de representação |
        | panel_user | "4999.99" | limiar−0,01 preservado na criação |
        | panel_user | "5000.00" | limiar preservado na criação |
        | panel_user | "5000.01" | limiar+0,01 preservado na criação |
        | admin_organizacao | "5000.01" | administrador também solicitante |

    Esquema do Cenário: [CT-02] Cada dado obrigatório é validado na criação e na edição por fora da UI
      Dado Ana e o centro Compras com Bruno e dois diretores, e <partida> com descrição "Café", valor "5000.01" e centro Compras
      Quando Ana tenta <operacao> por fora da UI alterando somente <campo> para <entrada>
      Então a operação é recusada pelo dado <campo> e <persistencia>
      E as decisões anteriores permanecem idênticas e nenhum e-mail novo chega a Bruno, diretores ou Ana

      Exemplos:
        | partida | operacao | campo | entrada | persistencia | # partição |
        | nenhuma solicitação | criar | descricao | ausente | nenhuma solicitação é criada | descrição ausente |
        | nenhuma solicitação | criar | descricao | null | nenhuma solicitação é criada | descrição nula |
        | nenhuma solicitação | criar | descricao | "" | nenhuma solicitação é criada | descrição vazia |
        | nenhuma solicitação | criar | descricao | "   " | nenhuma solicitação é criada | descrição sem conteúdo |
        | nenhuma solicitação | criar | valor | ausente | nenhuma solicitação é criada | valor ausente |
        | nenhuma solicitação | criar | valor | null | nenhuma solicitação é criada | valor nulo |
        | nenhuma solicitação | criar | valor | "abc" | nenhuma solicitação é criada | valor não monetário |
        | nenhuma solicitação | criar | centro_custo_id | ausente | nenhuma solicitação é criada | centro ausente |
        | nenhuma solicitação | criar | centro_custo_id | null | nenhuma solicitação é criada | centro nulo |
        | nenhuma solicitação | criar | centro_custo_id | identificador inexistente | nenhuma solicitação é criada | centro inexistente |
        | solicitação em rascunho | editar | descricao | null | os três dados originais permanecem | descrição nula na edição |
        | solicitação em rascunho | editar | descricao | "" | os três dados originais permanecem | descrição vazia na edição |
        | solicitação em rascunho | editar | descricao | "   " | os três dados originais permanecem | descrição em branco na edição |
        | solicitação em rascunho | editar | valor | null | os três dados originais permanecem | valor nulo na edição |
        | solicitação em rascunho | editar | valor | "abc" | os três dados originais permanecem | valor inválido na edição |
        | solicitação em rascunho | editar | centro_custo_id | null | os três dados originais permanecem | centro nulo na edição |
        | solicitação em rascunho | editar | centro_custo_id | identificador inexistente | os três dados originais permanecem | centro inexistente na edição |

    Cenário: [CT-03] O formulário de criação grava os dados e o rascunho do solicitante
      Dado Ana autenticada na página create, centro Compras com Bruno e dois diretores, e nenhuma solicitação
      Quando Ana grava pelo componente descrição "Aquisição de café ☕", valor "5000.01" e centro Compras
      Então o banco contém exatamente uma solicitação de Ana em rascunho com esses três dados e organização Acme
      E a criação não deixa erros de formulário, não cria decisão e não envia e-mail a nenhum dos destinatários existentes
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-01 | Aceitar um dos três dados obrigatórios sem conteúdo | CT-02 | Nas linhas ausente/null/vazio, zero criações ou os três dados antigos intactos; o mutante grava. |
| M-02 | Validar os dados somente no formulário de criação | CT-02 | A edição direta com valor "abc" é recusada; o mutante persiste entrada inválida. |
| M-03 | Converter valor monetário para inteiro ao gravar | CT-01, CT-03 | O valor persistido é "5000.01", não "5000.00". |
| M-04 | Criar pelo formulário com solicitante ou situação não inicial incorretos | CT-03 | O registro pertence a Ana e está em rascunho, sem decisões. |
| M-87 | Impedir criação por quem também administra a organização — revisão adversarial ADV-13 | CT-01 | Ana admin_organizacao cria seu rascunho legítimo com os três dados, sem veto pelo papel. |

Faixas numéricas e tetos de texto não determinados pelo 00 ficam em Q1/Q2; não se importam 0,01/255 do PRD. Omissão em edição significa manter campo quando há atualização parcial; não é teste de obrigatoriedade.

## Regra R2 — Somente o solicitante edita, e somente em rascunho

> Origem: RQ-02; RQ-09; RQ-10; A-05. Perfil **completo**. Técnica: **estado × operação; papel × ação; EP**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o solicitante edita, e somente em rascunho

    Esquema do Cenário: [CT-04] A correção direta pode trocar cada dado determinante e salvar sem alteração
      Dado uma solicitação de Ana em rascunho <origem>, com descrição "Café", valor "4999.99", centro Compras, gestor Bruno e diretores reais
      Quando Ana edita por fora da UI <alteracao>
      Então a mesma solicitação permanece em rascunho com <dados> e a quantidade de solicitações não muda
      E as decisões históricas permanecem idênticas e nenhum e-mail novo é enviado

      Exemplos:
        | origem | alteracao | dados | # partição |
        | inicial | descrição para "Café e açúcar ☕" | descrição "Café e açúcar ☕", valor "4999.99", centro Compras | descrição |
        | inicial | valor para "4999.99" | descrição "Café", valor "4999.99", centro Compras | valor abaixo da alçada |
        | inicial | valor para "5000.00" | descrição "Café", valor "5000.00", centro Compras | valor igual à alçada |
        | inicial | valor para "5000.01" | descrição "Café", valor "5000.01", centro Compras | valor cruza alçada |
        | após rejeição | centro para Viagens com gestor Carlos | descrição "Café", valor "4999.99", centro Viagens | centro troca aprovador |
        | após rejeição | os mesmos três dados | descrição "Café", valor "4999.99", centro Compras | edição sem mudança |

    Esquema do Cenário: [CT-05] Dados ficam imutáveis fora de rascunho
      Dado a solicitação de Ana em <situacao>, descrição "Café", valor "5000.01", centro Compras, gestor Bruno, gestor Carlos de Viagens e diretores reais
      Quando Ana tenta editar por fora da UI somente <campo> para <novo>
      Então a edição é recusada e o banco mantém <situacao>, descrição "Café", valor "5000.01" e centro Compras
      E a solicitação não é excluída, as decisões anteriores ficam idênticas e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | campo | novo | # partição |
        | aguardando_gestor | descricao | "Alterada" | trânsito/descrição |
        | aguardando_gestor | valor | "4999.99" | trânsito/alçada |
        | aguardando_gestor | centro_custo_id | Viagens | trânsito/gestor |
        | aguardando_diretor | descricao | "Alterada" | segunda etapa/descrição |
        | aguardando_diretor | valor | "4999.99" | segunda etapa/alçada |
        | aguardando_diretor | centro_custo_id | Viagens | segunda etapa/gestor |
        | aprovada | descricao | "Alterada" | terminal/descrição |
        | aprovada | valor | "4999.99" | terminal/alçada |
        | aprovada | centro_custo_id | Viagens | terminal/gestor |
        | cancelada | descricao | "Alterada" | cancelada/descrição |
        | cancelada | valor | "4999.99" | cancelada/alçada |
        | cancelada | centro_custo_id | Viagens | cancelada/gestor |

    Esquema do Cenário: [CT-06] Nenhum aprovador ou terceiro edita o rascunho de outro solicitante
      Dado o rascunho de Ana com valor "5000.01", centro Compras com gestor Bruno, diretora Diana e Carlos como outro panel_user de Acme
      Quando <ator> tenta editar diretamente o valor para "4999.99"
      Então a edição é recusada e o banco mantém solicitante Ana, rascunho, valor "5000.01", descrição e centro originais
      E a solicitação não é excluída, o histórico fica idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | ator | # partição |
        | Carlos | terceiro da mesma organização |
        | Bruno | gestor específico não solicitante |
        | Diana | diretora não solicitante |

    Esquema do Cenário: [CT-07] O formulário de edição salva correções e uma edição sem mudança
      Dado Ana autenticada na página edit do seu rascunho após rejeição, centro Compras com Bruno, centro Viagens com Carlos e diretores reais
      Quando Ana salva pelo componente <alteracao>
      Então o mesmo registro em rascunho contém <dados>, sem erros de formulário nem nova solicitação
      E o histórico da rejeição permanece idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | alteracao | dados | # partição |
        | descrição "Café novo", valor "5000.01" e centro Viagens | descrição "Café novo", valor "5000.01", centro Viagens | correção completa |
        | manter descrição, valor e centro atuais | os três dados originais | edição sem mudança |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-05 | Permitir editar depois do envio | CT-05 | Em cada estado não inicial, valor continua "5000.01" e centro continua Compras. |
| M-06 | Conferir apenas situação, sem identidade | CT-06 | Carlos não muda o rascunho de Ana nem seu valor. |
| M-07 | Bloquear todo rascunho que já foi rejeitado | CT-04, CT-07 | A correção pós-rejeição persiste os novos dados no mesmo registro. |
| M-08 | Validar contra o próprio registro como se fosse outro | CT-04, CT-07 | Salvar os mesmos dados é aceito sem duplicação nem erro. |
| M-09 | Formulário salvar valor e perder centro de custo | CT-07 | O registro contém centro Viagens e valor "5000.01" juntos. |
| M-88 | Permitir exceção de edição ao gestor específico do centro — revisão adversarial ADV-05 | CT-06 | Bruno, mesmo gestor correto, não altera valor nem dados do rascunho de Ana. |

## Regra R3 — Somente o solicitante exclui o rascunho

> Origem: RQ-03; RQ-10; A-05. Perfil **completo**. Técnica: **estado × operação; papel × ação; rastreio de efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Somente o solicitante exclui o rascunho

    Esquema do Cenário: [CT-08] O solicitante exclui um rascunho inicial ou devolvido
      Dado Ana com sua solicitação em rascunho <origem>, gestor Bruno e diretores reais
      Quando Ana exclui a solicitação por fora da UI
      Então a solicitação deixa de ser um registro disponível para leitura e escrita de negócio
      E nenhuma decisão nova é registrada nem e-mail novo é enviado

      Exemplos:
        | origem | # partição |
        | inicial | antes do primeiro envio |
        | após rejeição justificada | rascunho reentrado |

    Esquema do Cenário: [CT-09] A exclusão é recusada em cada situação não editável
      Dado a solicitação de Ana em <situacao> com valor "5000.01", histórico conhecido, gestor Bruno e diretores reais
      Quando Ana tenta excluir diretamente a solicitação
      Então a solicitação continua existente em <situacao> com os três dados e o histórico idênticos
      E nenhuma decisão nova é gravada e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | # partição |
        | aguardando_gestor | trânsito inicial |
        | aguardando_diretor | trânsito final |
        | aprovada | terminal |
        | cancelada | terminal cancelado |

    Esquema do Cenário: [CT-10] Nem gestor, diretor ou terceiro excluem o rascunho alheio
      Dado o rascunho de Ana com centro Compras, gestor Bruno, diretora Diana e Carlos como outro usuário da mesma organização
      Quando <ator> tenta excluí-lo por fora da UI
      Então o rascunho continua existente com Ana como solicitante e os três dados originais
      E seu histórico permanece idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | ator | # partição |
        | Carlos | terceiro sem poder de decisão |
        | Bruno | gestor específico não solicitante |
        | Diana | diretora não solicitante |

    Esquema do Cenário: [CT-11] A exclusão não permite reutilizar instância removida
      Dado a solicitação de Ana que foi excluída legitimamente do rascunho, uma instância anterior retida, gestor Bruno e diretores reais
      Quando <ator> tenta <operacao> diretamente pela instância retida
      Então a solicitação não reaparece nem muda dados e não existe solicitação ativa com a identidade removida
      E nenhuma decisão nova é criada e nenhum e-mail novo é enviado

      Exemplos:
        | ator | operacao | # partição |
        | Ana | excluir novamente | repetição da intenção |
        | Ana | editar valor para "5000.01" | escrita depois da exclusão |
        | Ana | enviar | envio depois da exclusão |
        | Ana | cancelar | cancelamento depois da exclusão |
        | Bruno | aprovar | decisão depois da exclusão |
        | Bruno | rejeitar com "Sem verba" | rejeição depois da exclusão |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-10 | Excluir sem conferir o solicitante | CT-10 | O rascunho de Ana continua existente após a tentativa de Carlos. |
| M-11 | Proteger update, mas deixar delete livre fora do rascunho | CT-09 | Cada registro não inicial continua existente com seus dados e decisões. |
| M-12 | Impedir excluir rascunho devolvido | CT-08 | O registro pós-rejeição deixa de estar disponível para uso. |
| M-13 | Recriar registro removido ao salvar instância antiga | CT-11 | A identidade removida não reaparece, inclusive após editar/enviar. |
| M-101 | Dar ao gestor ou diretor exceção para excluir rascunho alheio — revisão adversarial ADV2-01 | CT-10 | Bruno e Diana, embora aprovadores, não excluem o rascunho de Ana. |

Mecanismo de exclusão não é decidido pelo 00. O oráculo afirma indisponibilidade efetiva; DELETE versus marcação permanece Q8, sem apagar os cenários de escrita após remoção.

## Regra R4 — O envio do solicitante encaminha ao gestor do centro de custo

> Origem: RQ-04; RQ-09; A-02; A-10. Perfil **completo**. Técnica: **estado × operação; papel × ação; rastreio de efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O envio do solicitante encaminha ao gestor do centro de custo

    Esquema do Cenário: [CT-12] Todo envio começa pelo gestor correto
      Dado o rascunho de Ana com papel <papel> de valor <valor> no centro Viagens com gestor Carlos, outro centro com Bruno e dois diretores reais
      Quando Ana envia a solicitação por fora da UI
      Então o banco contém a mesma solicitação em aguardando_gestor sem decisão de aprovação
      E Carlos recebe exatamente um e-mail desta etapa; Bruno, diretores e Ana recebem zero

      Exemplos:
        | papel | valor | # partição |
        | panel_user | "4999.99" | abaixo da alçada |
        | panel_user | "5000.00" | igual à alçada |
        | panel_user | "5000.01" | acima da alçada |
        | admin_organizacao | "5000.01" | administrador também solicitante |

    Esquema do Cenário: [CT-13] Nem aprovador nem terceiro envia o rascunho alheio
      Dado o rascunho de Ana com gestor Bruno, diretoras Diana e Elisa, e Carlos como outro panel_user da mesma organização
      Quando <ator> tenta enviar diretamente a solicitação
      Então o banco mantém rascunho, Ana e os três dados originais
      E nenhuma decisão nova é criada e nenhum e-mail novo chega a Bruno, diretoras ou Ana

      Exemplos:
        | ator | # partição |
        | Carlos | terceiro |
        | Bruno | gestor específico não solicitante |
        | Diana | diretora não solicitante |

    Esquema do Cenário: [CT-14] Enviar não reabre situações já enviadas ou terminais
      Dado a solicitação de Ana em <situacao> com valor "5000.01", histórico conhecido, gestor Bruno e diretores reais
      Quando Ana tenta enviá-la diretamente
      Então a situação persistida continua <situacao> e os três dados permanecem idênticos
      E o histórico fica idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | # partição |
        | aguardando_gestor | já enviada |
        | aguardando_diretor | segunda etapa |
        | aprovada | terminal |
        | cancelada | terminal cancelado |

    Cenário: [CT-15] Centro sem gestor impede o envio
      Dado o rascunho de Ana no centro Compras sem gestor, com dois diretores de Acme e Bruno gestor de outro centro
      Quando Ana tenta enviar diretamente a solicitação
      Então o banco mantém rascunho e os três dados, e a recusa informa ausência de gestor sem fixar sua frase literal
      E existe warning correspondente ao envio recusado por ausência de gestor, nenhuma decisão é criada e nenhum e-mail chega aos diretores, a Bruno ou a Ana

    Cenário: [CT-16] Repetir o mesmo envio não duplica o encaminhamento
      Dado o rascunho de Ana com gestor Bruno e diretores, e duas instâncias lidas ainda em rascunho
      Quando Ana executa a mesma intenção de enviar duas vezes, primeiro por uma instância e depois pela outra
      Então há uma única solicitação em aguardando_gestor com os mesmos três dados e zero decisões
      E Bruno recebeu exatamente um e-mail da etapa, e diretores e Ana receberam zero

    Cenário: [CT-68] A interface informa a recusa de envio por ausência de gestor
      Dado Ana autenticada na listagem com seu rascunho no centro sem gestor, Bruno gestor de outro centro e diretoras Diana e Elisa reais
      Quando Ana aciona Enviar da compra alvo pelo componente
      Então a tela apresenta informação visível que identifica a ausência de gestor, sem afirmar sucesso, e o banco mantém rascunho com os três dados originais
      E existe warning correspondente à recusa, nenhuma decisão nova é criada e nenhum e-mail novo chega a Ana, Bruno, Diana ou Elisa
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-14 | Encaminhar valores altos diretamente ao diretor | CT-12 | Mesmo "5000.01" termina em aguardando_gestor e só Carlos recebe e-mail. |
| M-15 | Selecionar qualquer gestor da organização | CT-12 | Somente Carlos, gestor de Viagens, recebe um e-mail. |
| M-16 | Omitir a barreira de solicitante no envio | CT-13 | O rascunho de Ana não é enviado por Carlos. |
| M-17 | Aceitar envio em situação diferente de rascunho | CT-14 | Cada situação e histórico permanecem iguais; zero novos e-mails. |
| M-18 | Sem gestor, pular etapa ou deixar aguardando_gestor | CT-15 | Situação continua rascunho; nenhuma decisão nem e-mail. |
| M-19 | Verificar estado apenas na instância antiga e reenviar | CT-16 | Total persistido é uma solicitação e total de e-mails ao gestor é um. |
| M-89 | Recusar centro sem gestor sem produzir warning — revisão adversarial ADV-01 | CT-15 | A tentativa recusada registra warning sobre ausência de gestor, exigência explícita de A-10. |
| M-90 | Proibir envio por administrador que também é solicitante — revisão adversarial ADV-13 | CT-12 | Ana admin_organizacao envia seu rascunho e só Carlos recebe um e-mail. |
| M-102 | Dar ao gestor ou diretor exceção para enviar rascunho alheio — revisão adversarial ADV2-01 | CT-13 | Bruno/Diana não enviam o rascunho de Ana nem disparam aviso ao gestor. |
| M-103 | Capturar recusa de envio na action e exibir sucesso ou silêncio — revisão adversarial ADV2-04 | CT-68 | A tela identifica ausência de gestor e não mostra sucesso; o estado persistido continua rascunho. |

CT-15 cobre cardinalidade zero, mas não é prova de atomicidade nem de ausência de e-mail ao gestor inexistente. O warning do CT-15 vem expressamente de A-10, premissa normativa dada pelo usuário, e não dos logs do PRD. É verificação auxiliar do mesmo cenário de recusa; não se criou CT autônomo a partir de logger. Estouro de mutantes originado em ADV-01/13, permitido pela exceção da revisão. CT-68 eleva R4 para seis blocos: estouro justificado pelo gate de falsificabilidade, pois mensagem visível de A-10 exige componente e a recusa direta não a prova. Não se fundiram duas costuras no mesmo CT. Os mutantes adicionais são ADV2-01/04.

## Regra R5 — A aprovação do gestor respeita a alçada estrita e antecede o diretor

> Origem: RQ-05; RQ-06; A-03; A-04. Perfil **completo**. Técnica: **BVA 3-valores; tabela de decisão; estado × operação**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A aprovação do gestor respeita a alçada estrita e antecede o diretor

    Esquema do Cenário: [CT-17] O limite literal de fábrica distingue os três centavos da fronteira
      Dado uma solicitação de Ana em aguardando_gestor de valor <valor>, Bruno gestor, dois diretores reais e a configuração de compras carregada sem override do teste nem da variável de ambiente
      Quando Bruno aprova por fora da UI
      Então o limite efetivo carregado é decimal "5000.00" e a situação persistida é <destino>, com uma única decisão aprovada por Bruno na etapa gestor
      E os diretores recebem <emails> e Ana e Bruno recebem zero e-mails novos

      Exemplos:
        | valor | destino | emails | # borda |
        | "4999.99" | aprovada | zero e-mails | borda−0,01 |
        | "5000.00" | aprovada | zero e-mails | borda |
        | "5000.01" | aguardando_diretor | um e-mail por diretor | borda+0,01 |

    Esquema do Cenário: [CT-18] Uma alçada configurada substitui o default
      Dado uma solicitação de Ana em aguardando_gestor com valor <valor>, gestor Bruno, dois diretores e limite efetivo configurado como decimal <limite>
      Quando Bruno aprova diretamente
      Então a situação persistida é <destino> e existe exatamente uma decisão de gestor aprovada por Bruno
      E os diretores recebem <emails>, sem e-mail novo para Ana ou Bruno

      Exemplos:
        | limite | valor | destino | emails | # borda |
        | "7000.00" | "6999.99" | aprovada | zero e-mails | limite maior/borda−0,01 |
        | "7000.00" | "7000.00" | aprovada | zero e-mails | limite maior/borda |
        | "7000.00" | "7000.01" | aguardando_diretor | um e-mail por diretor | limite maior/borda+0,01 |
        | "3000.00" | "2999.99" | aprovada | zero e-mails | limite menor/borda−0,01 |
        | "3000.00" | "3000.00" | aprovada | zero e-mails | limite menor/borda |
        | "3000.00" | "3000.01" | aguardando_diretor | um e-mail por diretor | limite menor/borda+0,01 |

    Cenário: [CT-19] Um diretor conclui depois da aprovação do gestor
      Dado a solicitação de Ana de valor "5000.01" em aguardando_diretor após aprovação real de Bruno, com diretores Diana e Elisa
      Quando Diana aprova por fora da UI
      Então a solicitação fica aprovada e há exatamente duas decisões aprovadas, gestor Bruno antes de diretor Diana
      E a decisão de Bruno fica idêntica e nenhum e-mail novo chega a Ana, Bruno, Diana ou Elisa

    Esquema do Cenário: [CT-20] Aprovar não cria uma etapa em situações sem decisão pendente
      Dado a solicitação de Ana em <situacao> de valor "5000.01", gestor Bruno e diretores Diana e Elisa, com histórico conhecido
      Quando <ator> tenta aprovar diretamente
      Então o banco mantém <situacao>, os três dados e exatamente o histórico anterior
      E nenhum e-mail novo chega a Ana, Bruno, Diana ou Elisa

      Exemplos:
        | situacao | ator | # partição |
        | rascunho | Bruno | aprovação antes de enviar |
        | rascunho | Diana | diretor antes do envio |
        | aprovada | Diana | terminal aprovado |
        | cancelada | Diana | terminal cancelado |

    Cenário: [CT-63] Ausência de diretor nunca dispensa a aprovação adicional
      Dado a solicitação de Ana em aguardando_gestor de valor "5000.01", limite efetivo "5000.00", gestor Bruno, zero diretores de Acme e Elisa diretora apenas de Globex
      Quando Bruno tenta aprovar diretamente a etapa de gestor
      Então a solicitação não fica aprovada e não existe decisão de diretor inventada, nem uma decisão atribuída a Elisa
      E os três dados e decisões anteriores permanecem íntegros, e Ana e Elisa não recebem e-mail de conclusão ou de etapa indevida
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-20 | Comparar o limite com >= em vez de > | CT-17, CT-18 | Em "5000.00" e "7000.00" o destino é aprovada e zero e-mails de diretor. |
| M-21 | Truncar o valor para reais inteiros antes da comparação | CT-17, CT-18 | Em "5000.01"/"7000.01" o destino é aguardando_diretor. |
| M-22 | Usar sempre o número literal 5000 ignorando configuração | CT-18 | Com limite "7000.00" e valor "6999.99" o destino é aprovada. |
| M-23 | Default errado ficar mascarado pelo ambiente de testes | CT-17 | O limite efetivo, lido da configuração original sem override, deve ser "5000.00". |
| M-24 | Finalizar etapa de diretor sem registrar quem aprovou | CT-19 | Existem duas decisões com Bruno e Diana nas etapas corretas. |
| M-25 | Permitir aprovação em qualquer situação | CT-20 | Rascunho, aprovada e cancelada mantêm situação e histórico idênticos. |
| M-91 | Sem diretor cadastrado, dispensar a etapa e finalizar — revisão adversarial ADV-02 | CT-63 | Valor "5000.01" não chega a aprovada nem ganha aprovação fictícia de diretor. |
| M-92 | Usar max(5000, limiteConfigurado) — revisão adversarial ADV-03 | CT-18 | Limite "3000.00" com valor "3000.01" deve aguardar diretor e avisá-lo. |

Dinheiro é decimal textual ou centavos inteiros; incremento do BVA é 0,01. CT-17 exige retirar override de ambiente em processo isolado e carregar a config original, sem trocar seu default por código do teste. CT-63 prova somente o invariante fechado das duas leituras de Q3; não fixa se a tentativa mantém aguardando_gestor ou passa a aguardando_diretor, nem impõe contagem da aprovação do gestor. O mutante produz aprovada e diverge em ambas as leituras. Estouro de mutantes: ADV-02/03.

## Regra R6 — Cada verbo de decisão exige a identidade da etapa corrente

> Origem: RQ-04; RQ-05; RQ-06; A-02; A-03; A-07; A-09. Perfil **completo**. Técnica: **matriz papel × ação; tabela de decisão completa**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Cada verbo de decisão exige a identidade da etapa corrente

    Esquema do Cenário: [CT-21] Aprovar exige o gestor específico ou um diretor da organização
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno, outro gestor Carlos e diretores Diana e Elisa de Acme e Fernanda administradora de Acme sem função de gestor nem papel diretor
      Quando <ator> tenta aprovar por fora da UI
      Então a tentativa é recusada e a situação persistida continua <situacao> com os três dados e o histórico anteriores
      E nenhum e-mail novo é enviado aos destinatários existentes

      Exemplos:
        | situacao | ator | # partição |
        | aguardando_gestor | Ana sem papel diretor | solicitante não gestor |
        | aguardando_gestor | Carlos gestor de outro centro | gestor errado |
        | aguardando_gestor | Diana | diretor antes do gestor |
        | aguardando_diretor | Ana sem papel diretor | solicitante não diretor |
        | aguardando_diretor | Bruno sem papel diretor | gestor não diretor |
        | aguardando_diretor | Carlos sem papel diretor | terceiro não diretor |
        | aguardando_gestor | Fernanda | administração sem elegibilidade na etapa de gestor |
        | aguardando_diretor | Fernanda | administração sem elegibilidade na etapa de diretor |

    Esquema do Cenário: [CT-22] Rejeitar tem a mesma barreira de identidade, exercitada separadamente
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno, outro gestor Carlos e diretores Diana e Elisa de Acme e Fernanda administradora de Acme sem função de gestor nem papel diretor
      Quando <ator> tenta rejeitar diretamente com justificativa válida "Sem verba"
      Então a rejeição é recusada e a situação persistida continua <situacao> com os três dados e exatamente o histórico anterior
      E nenhum e-mail novo é enviado aos destinatários existentes

      Exemplos:
        | situacao | ator | # partição |
        | aguardando_gestor | Ana sem papel diretor | solicitante não gestor |
        | aguardando_gestor | Carlos gestor de outro centro | gestor errado |
        | aguardando_gestor | Diana | diretor antes do gestor |
        | aguardando_diretor | Ana sem papel diretor | solicitante não diretor |
        | aguardando_diretor | Bruno sem papel diretor | gestor não diretor |
        | aguardando_diretor | Carlos sem papel diretor | terceiro não diretor |
        | aguardando_gestor | Fernanda | administração sem elegibilidade na etapa de gestor |
        | aguardando_diretor | Fernanda | administração sem elegibilidade na etapa de diretor |

    Esquema do Cenário: [CT-23] Acumular funções não cria aprovação automática nem veto inventado
      Dado a solicitação em <situacao> com valor "5000.01", aprovador elegível <ator>, acúmulo <acumulo> e diretores reais
      Quando <ator> executa diretamente <operacao> na etapa corrente
      Então o banco contém <resultado> e exatamente uma nova decisão da etapa com a identidade de <ator>
      E o histórico anterior permanece idêntico e os únicos e-mails novos são <emails>

      Exemplos:
        | situacao | ator | acumulo | operacao | resultado | emails | # partição |
        | aguardando_gestor | Ana | solicitante e gestor | aprovar | aguardando_diretor | um por diretor | solicitante×gestor/aprovar |
        | aguardando_gestor | Ana | solicitante e gestor | rejeitar com "Sem verba" | rascunho | zero | solicitante×gestor/rejeitar |
        | aguardando_diretor | Ana | solicitante e diretor | aprovar | aprovada | zero | solicitante×diretor/aprovar |
        | aguardando_diretor | Ana | solicitante e diretor | rejeitar com "Sem verba" | rascunho | zero | solicitante×diretor/rejeitar |
        | aguardando_gestor | Bruno | gestor e diretor | aprovar | aguardando_diretor | um por diretor, incluindo Bruno | gestor×diretor/etapa inicial |
        | aguardando_diretor | Bruno | gestor e diretor que aprovou antes | aprovar | aprovada | zero | gestor×diretor/etapa final |
        | aguardando_diretor | Bruno | gestor e diretor que aprovou antes | rejeitar com "Sem verba" | rascunho | zero | gestor×diretor/rejeitar |
        | aguardando_gestor | Bruno | administrador da organização e gestor | aprovar | aguardando_diretor | um por diretor | administração×gestor/aprovar |
        | aguardando_gestor | Bruno | administrador da organização e gestor | rejeitar com "Sem verba" | rascunho | zero | administração×gestor/rejeitar |
        | aguardando_diretor | Diana | administradora da organização e diretora | aprovar | aprovada | zero | administração×diretor/aprovar |
        | aguardando_diretor | Diana | administradora da organização e diretora | rejeitar com "Sem verba" | rascunho | zero | administração×diretor/rejeitar |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-26 | Usar papel genérico de gestor em vez da FK do centro | CT-21, CT-22 | Carlos não aprova nem rejeita a etapa do centro de Bruno. |
| M-27 | Checar identidade apenas no verbo aprovar | CT-22 | Rejeição por Carlos/Diana fora da sua etapa não muda situação nem histórico. |
| M-28 | Permitir diretor pular o gestor | CT-21, CT-22 | Diana em aguardando_gestor não cria decisão de diretor. |
| M-29 | Proibir solicitante que também é o gestor | CT-23 | Ana elegível decide a etapa de gestor, conforme A-09. |
| M-30 | Uma pessoa com os dois papéis aprovar as duas etapas de uma vez | CT-23 | Primeira decisão de Bruno gestor+diretor termina aguardando_diretor com uma nova decisão, não aprovada. |
| M-31 | Exigir pessoas diferentes mesmo quando A-03 permite qualquer diretor | CT-23 | Bruno diretor pode decidir a segunda etapa após atuar como gestor. |
| M-93 | Vetar decisão de gestor que também administra centros — revisão adversarial ADV-14 | CT-23 | Bruno administrador+gestor decide sua etapa e registra exatamente uma decisão com sua identidade. |
| M-94 | Vetar decisão de diretor que também administra centros — revisão adversarial ADV-15 | CT-23 | Diana administradora+diretora decide a segunda etapa com sua identidade. |
| M-104 | Autorizar decisão por administração sem elegibilidade de etapa — revisão adversarial ADV2-02 | CT-21, CT-22 | Fernanda administradora não aprova nem rejeita em nenhuma das duas etapas sem ser gestor/diretor. |

Os pares de administração com solicitante estão também em CT-01/12. Os pares de administração com gestor/diretor estão no CT-23. Estouro de mutantes deriva de ADV-14/15, sem criar veto de segregação não previsto.

## Regra R7 — A rejeição justificada devolve ao rascunho

> Origem: RQ-06; RQ-07; RQ-08; A-07; A-11. Perfil **completo**. Técnica: **EP; estado × operação; rastreio de efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A rejeição justificada devolve ao rascunho

    Esquema do Cenário: [CT-24] Gestor e diretor rejeitam com justificativa curta ou Unicode
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno e diretores Diana e Elisa
      Quando <ator> rejeita por fora da UI com <justificativa>
      Então o banco contém rascunho e exatamente uma nova decisão rejeitada da etapa <etapa> por <ator>, com <justificativa> íntegra
      E os três dados e decisões anteriores permanecem idênticos e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | ator | etapa | justificativa | # partição |
        | aguardando_gestor | Bruno | gestor | "X" | fronteira de um caractere |
        | aguardando_gestor | Bruno | gestor | "Sem verba" | curta válida |
        | aguardando_gestor | Bruno | gestor | "Não há orçamento 🛒" | acento e emoji |
        | aguardando_diretor | Diana | diretor | "X" | um caractere no diretor |
        | aguardando_diretor | Diana | diretor | "Sem verba" | diretor também rejeita |
        | aguardando_diretor | Diana | diretor | "Não há orçamento ☕" | Unicode no diretor |

    Esquema do Cenário: [CT-25] Justificativa sem conteúdo nunca passa pela chamada direta
      Dado a solicitação de Ana em <situacao> com aprovador elegível <ator>, valor "5000.01", gestor Bruno e diretores Diana e Elisa
      Quando <ator> tenta rejeitar por fora da UI com justificativa <entrada>
      Então a chamada não conclui rejeição e o banco mantém <situacao>, os três dados e exatamente o histórico anterior
      E nenhum e-mail novo chega aos destinatários existentes

      Exemplos:
        | situacao | ator | entrada | # partição |
        | aguardando_gestor | Bruno | ausente | argumento ausente |
        | aguardando_gestor | Bruno | null | nula |
        | aguardando_gestor | Bruno | "" | vazia |
        | aguardando_gestor | Bruno | "   " | espaços |
        | aguardando_diretor | Diana | ausente | argumento ausente no diretor |
        | aguardando_diretor | Diana | null | nula no diretor |
        | aguardando_diretor | Diana | "" | vazia no diretor |
        | aguardando_diretor | Diana | "   " | espaços no diretor |

    Esquema do Cenário: [CT-26] Rejeitar em situação sem etapa pendente é recusado
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno e diretores Diana e Elisa, com histórico conhecido
      Quando <ator> tenta rejeitar diretamente com "Sem verba"
      Então o banco mantém <situacao>, os três dados e exatamente o histórico anterior
      E nenhum e-mail novo chega aos destinatários existentes

      Exemplos:
        | situacao | ator | # partição |
        | rascunho | Bruno | antes do envio |
        | aprovada | Diana | terminal |
        | cancelada | Diana | terminal cancelado |

    Cenário: [CT-27] O componente recusa a justificativa vazia e permite corrigir a mesma modal
      Dado Bruno autenticado na listagem com a solicitação de Ana em aguardando_gestor e diretores reais
      Quando Bruno submete a ação Rejeitar com justificativa ""
      Então o componente mostra erro especificamente na justificativa e mantém a solicitação em aguardando_gestor com histórico idêntico
      E a ação continua disponível para correção sem navegar para erro, e nenhum e-mail novo é enviado

    Cenário: [CT-28] A gravação da modal registra a rejeição do aprovador
      Dado Bruno autenticado na listagem com a solicitação de Ana em aguardando_gestor e diretores reais
      Quando Bruno grava a ação Rejeitar pelo componente com "Sem verba"
      Então o banco contém rascunho e uma nova decisão rejeitada de gestor por Bruno com justificativa "Sem verba"
      E o histórico anterior fica idêntico e nenhum e-mail novo é enviado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-32 | Validar justificativa apenas na modal | CT-25 | Chamada direta sem conteúdo não grava rejeição nem muda situação. |
| M-33 | Aceitar justificativa composta só por espaços | CT-25 | As duas linhas de espaços mantêm situação e histórico anteriores. |
| M-34 | Criar situação rejeitada em vez de devolver a rascunho | CT-24, CT-28 | Situação persistida é rascunho após cada rejeição válida. |
| M-35 | Exigir mínimo inventado de oito caracteres na justificativa — revisão adversarial ADV-10 | CT-24 | Nas duas etapas, "X" é aceito e registrado integralmente; mínimo oito recusaria. Unicode de quatro bytes também é preservado no cenário. |
| M-36 | Permitir rejeição após aprovação final | CT-26 | Aprovada mantém situação e histórico. |
| M-37 | A modal não mostra o erro da justificativa e fecha como sucesso | CT-27 | Justificativa vazia mostra erro no campo, mantém a ação corrigível e não muda estado/histórico. |

## Regra R8 — A correção inicia novo ciclo pelo gestor sem reaproveitar aprovação anterior

> Origem: RQ-09; RQ-05; RQ-13; A-12. Perfil **completo**. Técnica: **2-switch; EP × rastreio de efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A correção inicia novo ciclo pelo gestor sem reaproveitar aprovação anterior

    Esquema do Cenário: [CT-29] Reenvio após rejeição volta ao gestor do centro corrigido
      Dado a solicitação de Ana em rascunho após <rejeicao>, corrigida para centro Viagens com gestor Carlos e valor <valor>, com Bruno e diretores reais e cópia do histórico anterior
      Quando Ana envia novamente por fora da UI
      Então a mesma solicitação fica em aguardando_gestor sem nova decisão e todas as decisões anteriores permanecem idênticas
      E Carlos recebe exatamente um novo e-mail de gestor, e Bruno, diretores e Ana recebem zero

      Exemplos:
        | rejeicao | valor | # partição |
        | gestor Bruno rejeitou com "Sem verba" | "4999.99" | retorno do gestor abaixo da alçada |
        | gestor Bruno rejeitou com "Sem verba" | "5000.01" | retorno do gestor acima |
        | diretor Diana rejeitou após aprovação de Bruno | "4999.99" | retorno do diretor abaixo |
        | diretor Diana rejeitou após aprovação de Bruno | "5000.01" | retorno do diretor acima |

    Esquema do Cenário: [CT-30] A aprovação do novo gestor não herda a conclusão do ciclo anterior
      Dado a solicitação de Ana em aguardando_gestor no segundo ciclo, após rejeição de Diana e novo envio real, com valor <valor>, gestor Carlos e dois diretores
      Quando Carlos aprova diretamente a etapa deste ciclo
      Então a solicitação fica <destino>, com uma nova aprovação de gestor por Carlos e com todas as decisões do primeiro ciclo idênticas
      E os diretores recebem <emails> e não há decisão de diretor no ciclo atual

      Exemplos:
        | valor | destino | emails | # partição |
        | "5000.01" | aguardando_diretor | um novo e-mail por diretor | alçada alta |
        | "4999.99" | aprovada | zero e-mails novos | valor corrigido abaixo |

    Esquema do Cenário: [CT-69] O diretor decide normalmente no segundo ciclo
      Dado a solicitação de Ana de valor "5000.01" em aguardando_diretor no segundo ciclo após aprovação de Bruno, rejeição de Diana com "Sem verba", correção para centro Viagens de Carlos, novo envio e aprovação real de Carlos, com Diana e Elisa diretoras elegíveis
      Quando <ator> executa diretamente <operacao> na etapa diretor atual
      Então a solicitação fica <destino> e existe exatamente uma nova decisão de diretor <decisao> por <ator>, sem reutilizar a rejeição anterior
      E as três decisões anteriores permanecem íntegras, a justificativa "X" é preservada na nova rejeição quando houver e nenhum e-mail novo chega a Ana, Bruno, Carlos, Diana ou Elisa

      Exemplos:
        | ator | operacao | destino | decisao | # partição |
        | Diana | aprovar | aprovada | aprovada | mesma diretora aprova novo ciclo |
        | Elisa | aprovar | aprovada | aprovada | outra diretora aprova novo ciclo |
        | Diana | rejeitar com "X" | rascunho | rejeitada | mesma diretora rejeita novo ciclo |
        | Elisa | rejeitar com "X" | rascunho | rejeitada | outra diretora rejeita novo ciclo |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-38 | Pular gestor no reenvio porque ele aprovou no ciclo anterior | CT-29 | Segundo envio termina aguardando_gestor e só Carlos é notificado. |
| M-39 | Reutilizar a rejeição antiga de diretor como resolução da etapa atual — revisão adversarial ADV-12 | CT-30 | O Dado contém rejeição anterior de Diana, não aprovação; valor "5000.01" termina aguardando_diretor e a rejeição antiga não resolve o ciclo atual. |
| M-40 | Apagar ou sobrescrever histórico ao reenviar | CT-29, CT-30 | Cada decisão anterior conserva identidade, etapa, autor, instante e justificativa. |
| M-41 | Calcular a alçada do segundo ciclo usando o valor antigo | CT-30 | Novo valor "4999.99" termina aprovada e zero e-mails novos aos diretores. |
| M-105 | Bloquear toda decisão de diretor por existir decisão histórica de diretor — revisão adversarial ADV2-03 | CT-69 | Diana e Elisa podem aprovar ou rejeitar a etapa do segundo ciclo, com exatamente uma decisão nova e três anteriores íntegras. |

M-39 foi corrigido após ADV-12: aprovação final antiga seguida de reabertura é inalcançável sob A-05. O mutante atual usa a rejeição realmente presente no Dado do CT-30 e diverge por reutilizar resolução de ciclo anterior.

## Regra R9 — O solicitante cancela somente enquanto aguarda aprovação

> Origem: RQ-11; RQ-10; A-05; A-06. Perfil **completo**. Técnica: **estado × operação; papel × ação; rastreio de efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O solicitante cancela somente enquanto aguarda aprovação

    Esquema do Cenário: [CT-31] O solicitante cancela nas duas situações em trânsito
      Dado a solicitação de Ana em <situacao> com valor "5000.01", gestor Bruno, diretores Diana e Elisa e histórico conhecido
      Quando Ana cancela por fora da UI
      Então a mesma solicitação fica cancelada com os três dados e exatamente o histórico anterior
      E nenhuma decisão nova é criada e nenhum e-mail novo chega aos destinatários existentes

      Exemplos:
        | situacao | # partição |
        | aguardando_gestor | antes da primeira decisão |
        | aguardando_diretor | antes da decisão final |

    Esquema do Cenário: [CT-32] Outro usuário não cancela a solicitação alheia
      Dado a solicitação de Ana em <situacao>, com gestor Bruno e diretores Diana e Elisa
      Quando <ator> tenta cancelar diretamente
      Então o banco mantém <situacao>, Ana, os três dados e exatamente o histórico anterior
      E nenhuma decisão nova é criada e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | ator | # partição |
        | aguardando_gestor | Bruno | gestor não solicitante |
        | aguardando_gestor | Carlos outro panel_user | terceiro |
        | aguardando_diretor | Diana | diretor não solicitante |
        | aguardando_diretor | Bruno | gestor após sua etapa |

    Esquema do Cenário: [CT-33] Rascunho e situações terminais não aceitam cancelamento
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno, diretores Diana e Elisa e histórico conhecido
      Quando Ana tenta cancelar diretamente
      Então o banco mantém <situacao> e os três dados sem excluir o registro
      E o histórico fica idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | # partição |
        | rascunho | exceção vigente A-06 |
        | aprovada | aprovação final já ocorreu |
        | cancelada | terminal cancelado |

    Cenário: [CT-34] O cancelamento repetido não reabre a solicitação
      Dado a solicitação de Ana em aguardando_diretor com histórico conhecido, gestor Bruno e diretores, e duas instâncias lidas antes do cancelamento
      Quando Ana repete a mesma intenção de cancelar pelas duas instâncias em sequência
      Então a solicitação persistida está cancelada, com os mesmos três dados e exatamente o histórico anterior
      E nenhuma decisão nova foi criada e nenhum e-mail novo foi enviado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-42 | Permitir ao aprovador cancelar em lugar do solicitante | CT-32 | Bruno/Diana não mudam a situação da solicitação de Ana. |
| M-43 | Aplicar a leitura literal de qualquer momento sem a exceção A-06 | CT-33 | Rascunho permanece rascunho e não é excluído. |
| M-44 | Permitir cancelamento depois da aprovação final | CT-33 | Aprovada continua aprovada com suas decisões. |
| M-45 | Registrar cancelamento como decisão de aprovação ou emitir aviso extra | CT-31, CT-34 | Histórico fica idêntico e os destinatários existentes recebem zero e-mails novos. |
| M-46 | Reaplicar cancelamento de instância antiga altera o histórico | CT-34 | Depois das duas intenções, o histórico é exatamente o anterior. |

## Regra R10 — Uma etapa elegível admite uma única decisão persistida

> Origem: RQ-05; RQ-06; RQ-08; RQ-11; RQ-13; RQ-14; A-03. Perfil **completo**. Técnica: **idempotência no agregado; concorrência real**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Uma etapa elegível admite uma única decisão persistida

    Esquema do Cenário: [CT-35] Retry do gestor não duplica aprovação nem aviso da próxima etapa
      Dado a solicitação de Ana em aguardando_gestor com valor <valor>, gestor Bruno sem papel diretor, dois diretores e duas instâncias lidas antes da decisão
      Quando Bruno repete em sequência a mesma intenção de aprovar pelas duas instâncias
      Então a situação persistida é <destino> e existe exatamente uma decisão de gestor aprovada por Bruno
      E os diretores recebem <emails>, sem e-mail novo para Ana ou Bruno

      Exemplos:
        | valor | destino | emails | # partição |
        | "4999.99" | aprovada | zero e-mails | gestor final |
        | "5000.01" | aguardando_diretor | um por diretor | gestor intermediário |

    Cenário: [CT-36] Primeiro diretor resolve a etapa também no retry sequencial
      Dado a solicitação de Ana em aguardando_diretor de valor "5000.01", aprovação anterior de Bruno, diretores Diana e Elisa e instâncias lidas antes da decisão
      Quando Diana e Elisa executam em sequência a mesma intenção de aprovar a etapa
      Então a solicitação persistida fica aprovada com uma única decisão de diretor por Diana e a decisão anterior de Bruno idêntica
      E nenhum e-mail novo é enviado

    Esquema do Cenário: [CT-37] Retry de rejeição não duplica a decisão nem destrói histórico
      Dado a solicitação de Ana em <situacao>, valor "5000.01", aprovador elegível <ator>, gestor Bruno, diretores reais e duas instâncias lidas antes da decisão
      Quando <ator> repete em sequência a mesma intenção de rejeitar com "Sem verba" pelas duas instâncias
      Então o banco contém rascunho e exatamente uma nova decisão rejeitada da etapa por <ator>, com texto "Sem verba"
      E todo o histórico anterior permanece idêntico e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | ator | # partição |
        | aguardando_gestor | Bruno | retry do gestor |
        | aguardando_diretor | Diana | retry do diretor |

    Esquema do Cenário: [CT-38] Duas decisões simultâneas não vencem a mesma etapa
      Dado uma solicitação em <situacao> com valor "5000.01", gestor Bruno, diretores Diana e Elisa, e dois workers com conexões reais que já leram a mesma etapa elegível
      Quando os workers liberados por barreira executam simultaneamente <intencoes>
      Então apenas uma decisão da etapa é persistida e a situação é exatamente a consequência dessa decisão vencedora, sem perder decisões anteriores
      E se venceu aprovação do gestor há um e-mail por diretor; em rejeição ou decisão de diretor há zero e-mails novos

      Exemplos:
        | situacao | intencoes | # partição |
        | aguardando_gestor | Bruno aprova / Bruno aprova | duplo clique gestor |
        | aguardando_gestor | Bruno aprova / Bruno rejeita com "Sem verba" | duas decisões gestor |
        | aguardando_diretor | Diana aprova / Elisa aprova | dois diretores |
        | aguardando_diretor | Diana aprova / Elisa rejeita com "Sem verba" | decisões divergentes diretor |

    Esquema do Cenário: [CT-39] Cancelamento e decisão concorrentes preservam um histórico serial válido
      Dado uma solicitação de Ana em <situacao> com valor "5000.01", aprovador <ator>, gestor Bruno, diretores e dois workers em conexões reais já elegíveis antes da barreira
      Quando Ana tenta cancelar e <ator> tenta <decisao> simultaneamente a mesma etapa de partida
      Então o resultado persistido é um dos pares <pares>, correspondente a uma ordem serial válida das duas operações
      E o histórico anterior permanece idêntico e os e-mails novos são exatamente os do vencedor, sem duplicação

      Exemplos:
        | situacao | ator | decisao | pares | # partição |
        | aguardando_gestor | Bruno | aprovar | cancelada/zero decisão nova ou cancelada/uma aprovação de Bruno | cancelar×aprovar gestor |
        | aguardando_gestor | Bruno | rejeitar com "Sem verba" | cancelada/zero decisão nova ou rascunho/uma rejeição de Bruno | cancelar×rejeitar gestor |
        | aguardando_diretor | Diana | aprovar | cancelada/zero decisão nova ou aprovada/uma aprovação de Diana | cancelar×aprovar diretor |
        | aguardando_diretor | Diana | rejeitar com "Sem verba" | cancelada/zero decisão nova ou rascunho/uma rejeição de Diana | cancelar×rejeitar diretor |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-47 | Na aprovação final, confiar apenas no estado em memória | CT-36 | Diana e Elisa em sequência produzem uma única decisão final de Diana. |
| M-48 | Impedir duplicação só na etapa diretor | CT-35 | O gestor grava uma decisão e os diretores recebem um aviso cada. |
| M-49 | Persistir decisão antes de conferir quem venceu a transição | CT-38, CT-39 | Existe uma única decisão vencedora; cancelamento vencedor tem zero decisão nova. |
| M-50 | Permitir dois diretores decidirem por leitura seguida de escrita sem proteção | CT-38 | Duas conexões reais elegíveis produzem uma decisão de diretor, não duas. |
| M-51 | Aceitar aprovação FINAL depois de o cancelamento vencer | CT-39 | Na linha aguardando_diretor, cancelada tem zero decisão nova de diretor; aprovada tem uma, nunca ambos os efeitos. |
| M-52 | No verbo rejeitar, checar estado apenas no objeto antigo | CT-37 | A rejeição repetida produz exatamente uma decisão, tanto de gestor quanto de diretor. |

Concorrência não será certificada por duas instâncias sequenciais. Usar banco compartilhado por conexões reais e barreira após leitura; SQLite :memory: de cada processo é inadequado. Se não houver esse arnês, CT-38/39 ficam pendentes de execução, sem alegar cobertura medida. Corrida da etapa gestor que permitir cancelamento posterior exige distinguir as intenções originalmente concorrentes: o teste fixa a etapa de partida e impede uma segunda operação nova após a primeira conclusão. Na corrida gestor aprova × solicitante cancela, a aprovação intermediária seguida de cancelamento ainda antes da final é válida: cancelada pode conservar uma aprovação de gestor e seus avisos. Não exigir vencedor único nessa combinação; exigir serialização válida. Nos demais pares, a etapa terminal/rascunho impede a segunda intenção.

## Regra R11 — Estado, histórico e encaminhamento não ficam parcialmente confirmados

> Origem: RQ-05; RQ-06; RQ-08; RQ-13; RQ-14. Perfil **completo**. Técnica: **rastreio de efeito com falha após o ponto do efeito**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Estado, histórico e encaminhamento não ficam parcialmente confirmados

    Esquema do Cenário: [CT-40] Falha antes da confirmação não deixa decisão ou e-mail fantasma
      Dado a solicitação de Ana em <situacao>, valor "5000.01", gestor Bruno, diretores Diana e Elisa, histórico conhecido e falha controlada na confirmação depois de registrar a intenção de efeitos
      Quando o aprovador elegível executa diretamente <operacao> e a falha interrompe a confirmação
      Então a situação persistida e os três dados são os do Dado e todas as decisões anteriores permanecem idênticas, sem decisão nova confirmada
      E nenhum e-mail da tentativa falha fica entregue ou pendente de envio para os destinatários reais

      Exemplos:
        | situacao | operacao | # partição |
        | aguardando_gestor | aprovar como Bruno | próximo aprovador existente |
        | aguardando_gestor | rejeitar como Bruno com "Sem verba" | decisão de rejeição |
        | aguardando_diretor | aprovar como Diana | aprovação final |
        | aguardando_diretor | rejeitar como Diana com "Sem verba" | rejeição final |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-53 | Confirmar mudança de estado apesar de falhar a gravação da decisão | CT-40 | Após falha o estado e a lista de decisões são os anteriores. |
| M-54 | Registrar decisão fora da unidade de confirmação da transição | CT-40 | Nenhuma decisão nova confirmada sobrevive à falha. |
| M-55 | Enviar ou enfileirar e-mail antes da confirmação sem possibilidade de reversão | CT-40 | Na linha aprovação de gestor, Diana e Elisa existem e zero avisos da tentativa ficam entregues/pendentes. |

@premissa de mecanismo: falha injetada em callback de confirmação, depois de a operação alcançar o ponto de agendamento do efeito, não em pré-validação. Observar também o transporte/fila real de teste, sem usar Notification::fake como única prova de rollback. Sem vendor e aplicação executável nesta entrega, o ponto de injeção e o comportamento afterCommit ficam pendentes; não há alegação de atomicidade medida. Falha de transporte depois de commit é outro recorte, Q7, não é este teste.

## Regra R12 — E-mail vai a todos e somente aos aprovadores da próxima etapa

> Origem: RQ-14; RQ-04; RQ-05; A-03; A-11. Perfil **completo**. Técnica: **EP × rastreio de efeito; cardinalidade 0/1/N**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: E-mail vai a todos e somente aos aprovadores da próxima etapa

    Esquema do Cenário: [CT-41] O primeiro encaminhamento usa mail para o gestor do centro
      Dado o rascunho de Ana com valor <valor>, centro Compras com Bruno, outro centro com Carlos e diretores Diana e Elisa
      Quando Ana envia diretamente a solicitação
      Então Bruno recebe exatamente uma notificação referente a esta solicitação e etapa gestor pelos canais exatamente ["mail"]
      E Carlos, Ana, Diana e Elisa recebem zero notificações novas, e a situação persistida é aguardando_gestor sem decisão

      Exemplos:
        | valor | # partição |
        | "4999.99" | não exigirá diretor |
        | "5000.01" | exigirá diretor depois |

    Esquema do Cenário: [CT-42] A etapa diretor notifica o conjunto completo da organização
      Dado a solicitação de Ana em aguardando_gestor por Bruno com valor "5000.01", <diretores> diretores distintos em Acme, um diretor apenas de Globex e contexto de permissões de Acme
      Quando Bruno aprova diretamente a solicitação
      Então ela fica aguardando_diretor com uma nova aprovação de gestor, e cada diretor de Acme recebe exatamente um aviso da etapa diretor pelos canais exatamente ["mail"]
      E o conjunto completo de destinatários é exatamente o de Acme, sem Ana, Bruno não diretor nem diretor exclusivo de Globex

      Exemplos:
        | diretores | # partição |
        | 1 | um destinatário |
        | 3 | N destinatários |

    Esquema do Cenário: [CT-43] Operações sem próximo aprovador não geram e-mail
      Dado uma solicitação de Ana em <situacao> com valor <valor>, gestor Bruno, diretores Diana e Elisa, histórico conhecido e caixa de observação limpa após o setup
      Quando o ator elegível executa diretamente <operacao>
      Então a solicitação fica <destino> e o histórico tem <historico>
      E nenhum e-mail novo é enviado a Ana, Bruno, Diana ou Elisa

      Exemplos:
        | situacao | valor | operacao | destino | historico | # partição |
        | rascunho | "5000.01" | Ana edita a descrição | rascunho | exatamente as decisões anteriores | edição |
        | rascunho | "5000.01" | Ana exclui | indisponível para uso | nenhuma decisão nova | exclusão |
        | aguardando_gestor | "4999.99" | Bruno aprova | aprovada | uma nova aprovação de gestor | final sem diretor |
        | aguardando_gestor | "5000.00" | Bruno aprova | aprovada | uma nova aprovação de gestor | final na borda |
        | aguardando_gestor | "5000.01" | Bruno rejeita com "Sem verba" | rascunho | uma nova rejeição de gestor | rejeição gestor |
        | aguardando_diretor | "5000.01" | Diana rejeita com "Sem verba" | rascunho | uma nova rejeição de diretor | rejeição diretor |
        | aguardando_diretor | "5000.01" | Diana aprova | aprovada | uma nova aprovação de diretor | final diretor |
        | aguardando_gestor | "5000.01" | Ana cancela | cancelada | exatamente as decisões anteriores | cancelar antes gestor |
        | aguardando_diretor | "5000.01" | Ana cancela | cancelada | exatamente as decisões anteriores | cancelar antes diretor |

    Esquema do Cenário: [CT-67] Os dois tipos de aviso compõem e encaminham e-mail de verdade no transporte de teste
      Dado a solicitação de Ana em <situacao> com valor "5000.01", gestor Bruno, diretoras Diana e Elisa e transporte mail array com fila sync sem Notification::fake e sem Queue::fake
      Quando <ator> executa diretamente <operacao>
      Então a situação persistida é <destino> e o transporte de teste recebeu exatamente <mensagens> mensagens endereçadas ao conjunto <destinatarios>, com corpo não vazio que identifica esta solicitação e sua etapa pendente
      E nenhum outro destinatário recebe mensagem e o histórico contém exatamente <historico>

      Exemplos:
        | situacao | ator | operacao | destino | mensagens | destinatarios | historico | # partição |
        | rascunho | Ana | enviar | aguardando_gestor | 1 | Bruno | nenhuma decisão nova | mail de gestor |
        | aguardando_gestor | Bruno | aprovar | aguardando_diretor | 2 | Diana e Elisa | uma nova aprovação de gestor por Bruno | mail de diretores |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-56 | Trocar o canal mail por database | CT-41, CT-42 | Canais são exatamente ["mail"], além de conferir destinatário e solicitação. |
| M-57 | Notificar diretor antes de o gestor decidir | CT-41 | Diana/Elisa recebem zero no primeiro envio, mesmo com valor alto. |
| M-58 | Notificar somente o primeiro diretor encontrado | CT-42 | Na linha N os três diretores distintos recebem um aviso cada. |
| M-59 | Resolver diretores fora do contexto da organização | CT-42 | O conjunto exato exclui o diretor exclusivo de Globex. |
| M-60 | Mandar confirmação final/rejeição/cancelamento não pedida | CT-43 | Zero e-mails novos nos nove caminhos, com todos os possíveis destinatários presentes. |
| M-95 | Compor aviso com toMail quebrado ou sem encaminhar ao transporte — revisão adversarial ADV-11 | CT-67 | O transporte array recebe mensagens compostas, com corpo e destinatários reais, nos dois tipos de aviso; intenção capturada pelo fake não basta. |

Cardinalidade zero de gestor tem CT-15. O invariante de zero diretores tem CT-63. O destino exato permanece Q3: o requisito exige a etapa adicional, mas não decide recusar a aprovação do gestor versus aguardar a atribuição de diretor. Não se inventa esse destino. CT-67 evita o falso positivo do fake: limpar o transporte somente depois das transições de setup e observar desde a ação medida.

## Regra R13 — As referências de organização não permitem operar compras de terceiros

> Origem: RQ-01; RQ-02; RQ-03; RQ-04; RQ-05; RQ-06; RQ-11; A-01; A-03. Perfil **completo**. Técnica: **IDOR; matriz papel × ação; EP por fronteira**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: As referências de organização não permitem operar compras de terceiros

    Esquema do Cenário: [CT-44] Conhecer a identidade de outra compra não autoriza agir nela
      Dado a solicitação de Ana em Acme em <situacao>, com gestor Bruno e diretores de Acme, e Carlos autenticado apenas em Globex com permissões de negócio equivalentes
      Quando Carlos tenta <operacao> na solicitação de Acme por fora do componente
      Então a tentativa é recusada e a solicitação de Acme mantém solicitante, organização, situação, os três dados e histórico anteriores
      E não há decisão nova, exclusão nem e-mail novo para destinatários de Acme ou Globex

      Exemplos:
        | situacao | operacao | # partição |
        | rascunho | editar valor para "4999.99" | IDOR update |
        | rascunho | excluir | IDOR delete |
        | rascunho | enviar | IDOR enviar |
        | aguardando_gestor | aprovar | IDOR aprovar gestor |
        | aguardando_gestor | rejeitar com "Sem verba" | IDOR rejeitar gestor |
        | aguardando_gestor | cancelar | IDOR cancelar |
        | aguardando_diretor | aprovar com papel diretor só em Globex | IDOR aprovar diretor |
        | aguardando_diretor | rejeitar com papel diretor só em Globex e "Sem verba" | IDOR rejeitar diretor |

    Esquema do Cenário: [CT-45] Centro de outra organização não é uma referência válida
      Dado Ana autenticada em Acme, centro Compras de Acme com Bruno, centro Viagens de Globex com Carlos, diretores de ambas e <partida>
      Quando Ana tenta <operacao> usando centro_custo_id de Viagens por fora da UI
      Então a escrita é recusada e <persistencia>
      E não há decisão nova nem e-mail novo para Bruno, Carlos ou diretores de qualquer organização

      Exemplos:
        | partida | operacao | persistencia | # partição |
        | nenhuma solicitação | criar solicitação completa | nenhuma solicitação nova | FK estrangeira na criação |
        | seu rascunho em Compras com valor "5000.01" | editar só o centro | rascunho mantém Compras e valor "5000.01" | FK estrangeira na edição |

    Esquema do Cenário: [CT-46] Diretor só de outra organização não decide a segunda etapa
      Dado a solicitação de Ana em Acme em aguardando_diretor, aprovação de Bruno, Diana diretora só de Acme e Elisa diretora só de Globex, com Elisa membro comum também de Acme
      Quando Elisa tenta diretamente <operacao> no contexto Acme
      Então a solicitação continua aguardando_diretor com a aprovação de Bruno idêntica e sem nova decisão
      E nenhum e-mail novo é enviado

      Exemplos:
        | operacao | # partição |
        | aprovar | papel contextual na aprovação |
        | rejeitar com "Sem verba" | papel contextual na rejeição |

    Esquema do Cenário: [CT-47] A tela não expõe o detalhe de compra de outra organização
      Dado Ana autenticada somente em Acme, compra de Carlos em Globex em <situacao>, gestores e diretores reais, e um rascunho visível de Ana em Acme
      Quando Ana solicita o detalhe da compra de Globex pelo UUID conhecido no contexto Acme
      Então recebe 403 ou 404 sem descrição, valor, centro ou nomes das decisões da compra de Globex
      E o rascunho de Ana continua alcançável na listagem de Acme, e os dados e decisões de Globex não mudam

      Exemplos:
        | situacao | # partição |
        | rascunho | detalhe inicial |
        | aguardando_gestor | detalhe em trânsito |
        | aguardando_diretor | detalhe segunda etapa |
        | aprovada | detalhe terminal |
        | cancelada | detalhe cancelado |

    Cenário: [CT-66] A coleção da organização não contém compras estrangeiras
      Dado Ana autorizada em Acme com uma compra própria em rascunho, cinco compras reais de Globex cobrindo as cinco situações, gestores e diretores reais e tamanho de página maior que a coleção inteira
      Quando Ana carrega a listagem pelo componente no contexto Acme
      Então a coleção completa contém somente as identidades autorizadas de Acme e não contém nenhuma das cinco identidades, descrições, valores vinculados ou nomes de decisões de Globex
      E a linha da compra própria informa rascunho e nenhuma compra, decisão ou e-mail é criado ou alterado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | Confiar na permissão genérica sem conferir a compra e seu solicitante | CT-44 | Carlos não edita, exclui, envia ou cancela a compra de Ana. |
| M-62 | Validar existência da FK globalmente, sem organização | CT-45 | Viagens de Globex não pode ser vinculada na criação nem na edição em Acme. |
| M-63 | Consultar papel diretor globalmente ou usar cache do tenant anterior | CT-46 | Elisa com papel diretor só em Globex não aprova nem rejeita em Acme. |
| M-64 | Escopar somente a listagem e deixar detalhe acessível pelo UUID | CT-47 | Nenhum dos cinco detalhes estrangeiros expõe dados. |
| M-96 | Escopar o detalhe, mas deixar listagem retornar todas as organizações — revisão adversarial ADV-06 | CT-66 | A coleção inteira exclui as cinco compras de Globex em todos os estados, com N abaixo da página para tornar vazamento observável. |

O CT-47 especifica dois requests no executor para provar a saída do erro: o Quando é a única tentativa negada; o último Então exige um request independente à listagem autorizada. O 00 não define visibilidade horizontal entre leitores da MESMA organização; Q4 preserva esse recorte.

## Regra R14 — O cadastro do centro de custo pertence à administração da organização

> Origem: RQ-01; RQ-04; A-01; A-02; A-08. Perfil **completo**. Técnica: **papel × ação; EP; gravação por componente**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: O cadastro do centro de custo pertence à administração da organização

    Cenário: [CT-48] Administrador cria um centro com seu gestor pelo componente
      Dado administrador da organização autenticado em Acme na página create de centros, Bruno membro de Acme e nenhuma centro chamado "Compras ☕"
      Quando o administrador grava nome "Compras ☕" e gestor Bruno pelo componente
      Então existe um único centro chamado "Compras ☕" de Acme associado a Bruno, sem erro de formulário
      E nenhuma solicitação, decisão de aprovação ou e-mail de aprovação é criado

    Esquema do Cenário: [CT-49] Administrador salva o gestor e também pode manter os mesmos dados
      Dado administrador autenticado na página edit do centro Compras de Acme com gestor Bruno e Carlos como outro membro de Acme
      Quando o administrador salva pelo componente <alteracao>
      Então o mesmo centro mantém organização Acme e nome <nome>, com gestor <gestor> e sem erro de formulário
      E nenhuma solicitação ou decisão é criada e nenhum e-mail de aprovação é enviado

      Exemplos:
        | alteracao | nome | gestor | # partição |
        | trocar Bruno por Carlos | Compras | Carlos | mudança de destinatário |
        | manter nome e gestor atuais | Compras | Bruno | salvar sem mudança |
        | trocar somente nome para Viagens | Viagens | Bruno | mudança de nome |

    Esquema do Cenário: [CT-50] O usuário comum não ganha poder para se nomear gestor
      Dado Carlos panel_user de Acme, centro Compras com gestor Bruno e permissões de solicitar compra, sem autorização administrativa
      Quando Carlos tenta pela entrada de domínio protegida <operacao>
      Então a tentativa é recusada, o centro Compras mantém Bruno e nenhum centro novo é criado
      E Carlos continua sem permissões de administrar centros e com permissão de criar solicitações, sem decisão ou e-mail de aprovação novo

      Exemplos:
        | operacao | # partição |
        | cadastrar um centro com Carlos gestor | criação administrativa |
        | trocar gestor de Compras para Carlos | escalada por edição |
        | excluir centro Compras | exclusão administrativa |

    Esquema do Cenário: [CT-51] Administração de uma organização não alcança centro de outra
      Dado Carlos administrador só de Acme, centro Compras de Globex com gestor Bruno, centro Local de Acme e diretores reais
      Quando Carlos tenta pelo componente <operacao> no centro Compras de Globex usando identidade conhecida
      Então a ação é recusada sem expor ou mudar nome, organização e gestor do centro estrangeiro
      E o centro Local continua acessível, nenhuma solicitação ou decisão é criada e nenhum e-mail de aprovação é enviado

      Exemplos:
        | operacao | # partição |
        | carregar e salvar página edit | IDOR centro update |
        | excluir pela ação de registro | IDOR centro delete |

    Cenário: [CT-64] Administrador exclui um centro local sem dependências
      Dado administrador autenticado de Acme, centro Compras de Acme com gestor Bruno e nenhuma solicitação vinculada, centro Viagens preservado e diretoras Diana e Elisa reais
      Quando o administrador exclui Compras pela entrada administrativa protegida por fora da UI
      Então Compras deixa de estar disponível para uso de negócio e Viagens mantém nome, organização e gestor originais
      E nenhuma solicitação ou decisão é criada e nenhum e-mail de aprovação é enviado
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-65 | Incluir centros de custo na matriz do panel_user | CT-50 | Carlos não cadastra, altera gestor nem exclui; permission administrativa continua ausente. |
| M-66 | Esconder o menu, mas permitir a entrada de domínio ao usuário comum | CT-50 | As tentativas efetivas fora da UI são recusadas e Bruno permanece gestor. |
| M-67 | Formulário de edição do centro não persistir a troca de gestor | CT-49 | Centro editado aponta para Carlos, no mesmo registro. |
| M-68 | Conferir somente admin_organizacao sem conferir de qual organização | CT-51 | Compras de Globex permanece intacto e não expõe dados para admin de Acme. |
| M-69 | Formulário de criação do centro omitir o gestor ao gravar | CT-48 | O centro criado aponta para Bruno. |
| M-97 | Recusar toda exclusão de centro, inclusive a legítima — revisão adversarial ADV-07 | CT-64 | Compras local sem dependências deixa de estar disponível ao administrador legítimo. |
| M-98 | Ignorar mudança de nome do centro no formulário — revisão adversarial ADV-08 | CT-49 | O mesmo centro passa a Viagens e conserva Bruno como gestor. |

A entrada protegida de cadastro/alteração fora da UI é uma costura de domínio a materializar, não uma API existente confirmada. Não chamar CentroCusto::create e supor autorização automática do Eloquent. A ausência de ponto seguro no desenho é uma lacuna de integração L4, com CT-50 obrigatório para a futura implementação. A exclusão positiva do CT-64 não decide retenção nem exclusão de centro com dependências. Estouro de mutantes: ADV-07/08.

## Regra R15 — Payload do cliente não pode forjar posse, situação ou decisões

> Origem: RQ-01; RQ-02; RQ-04; RQ-05; RQ-10; RQ-13; A-01; A-08. Perfil **completo**. Técnica: **mass assignment por entidade; EP**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: Payload do cliente não pode forjar posse, situação ou decisões

    Esquema do Cenário: [CT-52] Compra não aceita colunas de controle enviadas pelo cliente
      Dado Ana autenticada em Acme, Bruno gestor de Compras, diretores reais e <partida>
      Quando Ana tenta <operacao> enviando os três dados válidos e somente o campo extra <campo> com <valor_forjado>
      Então <resultado> e o campo extra não muda solicitante Ana, organização Acme ou a situação legítima rascunho
      E nenhuma decisão é criada e nenhum e-mail de aprovação é enviado

      Exemplos:
        | partida | operacao | campo | valor_forjado | resultado | # partição |
        | nenhuma solicitação | criar por fora da UI | solicitante_id | Carlos | ou recusa integral ou cria rascunho de Ana com dados válidos | compra/solicitante |
        | nenhuma solicitação | criar por fora da UI | tenant_id | Globex | ou recusa integral ou cria rascunho de Ana em Acme | compra/organização |
        | nenhuma solicitação | criar por fora da UI | situacao | aprovada | ou recusa integral ou cria rascunho de Ana | compra/situação |
        | seu rascunho | editar por fora da UI | solicitante_id | Carlos | dados de controle e rascunho permanecem legítimos | editar/solicitante |
        | seu rascunho | editar por fora da UI | tenant_id | Globex | dados de controle e rascunho permanecem legítimos | editar/organização |
        | seu rascunho | editar por fora da UI | situacao | aprovada | rascunho não é aprovado | editar/situação |

    Esquema do Cenário: [CT-53] Centro não muda de organização por campo injetado
      Dado administrador de Acme, centro Compras de Acme com gestor Bruno, centro Viagens de Globex e diretores reais
      Quando o administrador tenta <operacao> um centro em Acme enviando tenant_id de Globex junto dos dados válidos
      Então nenhum centro de Acme é transferido para Globex nem sobrescreve Viagens, e todo centro eventualmente criado pertence a Acme
      E nenhum dado de solicitação ou decisão muda e nenhum e-mail de aprovação é enviado

      Exemplos:
        | operacao | # partição |
        | criar | mass assignment na criação |
        | editar | mass assignment na edição |

    Esquema do Cenário: [CT-54] Payload do pai não permite forjar ou reatribuir uma decisão filha
      Dado Ana em Acme com seu rascunho, uma compra aprovada de Globex com decisão real de Elisa, Bruno gestor e diretores de ambas as organizações
      Quando Ana salva o formulário de sua solicitação injetando somente <payload>
      Então seu registro continua rascunho de Ana em Acme sem decisão nova e a decisão de Globex mantém identidade, compra, etapa, decisão, autor e justificativa originais
      E nenhuma compra estrangeira muda e nenhum e-mail de aprovação é enviado

      Exemplos:
        | payload | # partição |
        | etapas com id da decisão de Globex e solicitacao_compra_id do rascunho | filha/reatribuição por identidade |
        | etapas com nova aprovação de diretor e decidido_por_id de Elisa | filha/falsificação de aprovação |
        | etapas com decisão existente e justificativa alterada | filha/alteração de histórico |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-70 | Permitir mass assignment de solicitante/situação/tenant na compra | CT-52 | Todos os campos de controle continuam legítimos e rascunho não vira aprovada. |
| M-71 | Permitir tenant_id gravável no centro | CT-53 | Nenhum centro é transferido para Globex. |
| M-72 | Gravar coleção de etapas recebida no formulário do pai | CT-54 | Nenhuma decisão nova e a filha estrangeira permanece byte a byte igual. |
| M-73 | Confiar no id da filha sem conferir a compra proprietária | CT-54 | A decisão de Globex conserva solicitacao_compra_id e autor originais. |

Recusar payload integralmente ou ignorar apenas a chave extra são mecanismos aceitos pelo invariante; dados legítimos não podem ser corrompidos. Em CT-53 executar duas linhas independentes (criação e edição), não as duas escritas no mesmo cenário materializado. IDOR direto da tabela de etapas fora do payload do pai continua L2, pois o 02 não inventariou seus pontos de entrada.

## Regra R16 — A tela informa a situação corrente e os autores das etapas

> Origem: RQ-12; RQ-13; A-12. Perfil **padrão**. Técnica: **EP exaustiva de estados; rastreio de histórico**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A tela informa a situação corrente e os autores das etapas

    Esquema do Cenário: [CT-55] Listagem e detalhe informam cada uma das cinco situações
      Dado leitor autorizado em Acme e uma solicitação identificável de Ana em <situacao> construída por transições reais
      Quando o leitor carrega o componente de <superficie> dessa solicitação
      Então a própria linha ou detalhe dessa compra informa <situacao> e não informa outra situação no lugar dela
      E aguardando_diretor nunca é apresentado como aprovação final

      Exemplos:
        | situacao | superficie | # partição |
        | rascunho | listagem | inicial/lista |
        | aguardando_gestor | listagem | gestor/lista |
        | aguardando_diretor | listagem | diretor/lista |
        | aprovada | listagem | final/lista |
        | cancelada | listagem | cancelada/lista |
        | rascunho | detalhe | inicial/detalhe |
        | aguardando_gestor | detalhe | gestor/detalhe |
        | aguardando_diretor | detalhe | diretor/detalhe |
        | aprovada | detalhe | final/detalhe |
        | cancelada | detalhe | cancelada/detalhe |

    Esquema do Cenário: [CT-56] O detalhe associa cada etapa ao autor correto
      Dado leitor autorizado e a solicitação de Ana aprovada por Bruno como gestor às 10:00 e <autora> como diretora às 10:01, com Diana cadastrada antes de Elisa e <outra> como diretora que não decidiu
      Quando o leitor carrega o detalhe dessa solicitação
      Então o detalhe associa etapa gestor a Bruno e etapa diretor a <autora> com suas decisões e instantes, sem atribuir a decisão a <outra>
      E a situação exibida é aprovada e a aprovação do gestor aparece antes da aprovação do diretor

      Exemplos:
        | autora | outra | # partição |
        | Diana | Elisa | primeira diretora decide |
        | Elisa | Diana | segunda diretora decide |

    Cenário: [CT-57] O histórico da rejeição e dos ciclos não é substituído pelo aprovador atual
      Dado leitor autorizado e a solicitação de Ana em aguardando_diretor no segundo ciclo, com aprovação antiga de Bruno às 09:00, rejeição anterior por Diana às 09:01 com "Sem verba" e aprovação nova de Carlos como gestor às 10:00
      Quando o leitor carrega o detalhe dessa solicitação
      Então o detalhe contém as identidades, etapas, decisões e ordem dos registros de Bruno, Diana e Carlos, incluindo "Sem verba" e os respectivos instantes 09:00, 09:01 e 10:00, sem omitir o instante da rejeição
      E a situação é aguardando_diretor e a decisão antiga de Diana não aparece como aprovação final do ciclo atual
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-74 | Exibir status fixo ou derivado só da existência de aprovação do gestor | CT-55, CT-57 | As duas superfícies informam as cinco situações, em particular aguardando_diretor. |
| M-75 | Mostrar aprovador atual em vez do autor persistido | CT-56, CT-57 | A etapa antiga continua atribuída a Bruno/Diana, e a nova a Carlos. |
| M-76 | Mostrar somente o último registro ou omitir justificativa | CT-56, CT-57 | CT-56 mostra as duas etapas individualmente; CT-57 mostra também a justificativa histórica exata "Sem verba" associada à rejeição de Diana, além dos demais registros. |
| M-99 | Mostrar instante somente de aprovação e omitir o de rejeição — revisão adversarial ADV-09 | CT-57 | A rejeição por Diana exibe o instante correspondente 09:01, sem depender de decidir o formato/fuso de Q6. |
| M-106 | Mostrar o primeiro diretor atual como autor da decisão — revisão adversarial ADV2-05 | CT-56 | Na linha autora Elisa, a decisão é de Elisa e não de Diana, que foi cadastrada primeiro. |

Asserção de situação não usa getLabel() do mesmo enum como único esperado: mapear semanticamente os cinco valores do requisito ao conteúdo da própria compra. Caixa, cor e frase literal não definidas pelo 00 não são oráculos. Formato/fuso dos instantes permanece Q6; aqui são instantes distintos e ordem, não representação de timezone.

## Regra R17 — A interface oferece somente ações permitidas para a persona e a situação

> Origem: RQ-02; RQ-03; RQ-04; RQ-05; RQ-06; RQ-11; A-06; A-08; A-09. Perfil **completo**. Técnica: **matriz papel × ação × situação**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: A interface oferece somente ações permitidas para a persona e a situação

    Esquema do Cenário: [CT-58] Ações disponíveis correspondem à etapa e ao dono
      Dado a solicitação de Ana em <situacao> com Bruno gestor, Diana diretora e persona <persona> autenticada
      Quando a persona carrega o componente de ações do registro
      Então estão disponíveis exatamente <acoes> entre editar, excluir, enviar, aprovar, rejeitar e cancelar
      E as outras ações de escrita não estão visíveis ou montáveis

      Exemplos:
        | situacao | persona | acoes | # partição |
        | rascunho | Ana | editar, excluir, enviar | dono inicial |
        | rascunho | Bruno | nenhuma | gestor antes do envio |
        | aguardando_gestor | Ana | cancelar | solicitante em trânsito |
        | aguardando_gestor | Bruno | aprovar, rejeitar | gestor elegível |
        | aguardando_gestor | Diana | nenhuma | diretor antecipado |
        | aguardando_diretor | Ana | cancelar | solicitante antes da final |
        | aguardando_diretor | Bruno sem papel diretor | nenhuma | gestor já decidiu |
        | aguardando_diretor | Diana | aprovar, rejeitar | diretor elegível |
        | aprovada | Ana | nenhuma | terminal dono |
        | aprovada | Diana | nenhuma | terminal diretor |
        | cancelada | Ana | nenhuma | terminal cancelado |
        | aguardando_gestor | Ana também gestora | cancelar, aprovar, rejeitar | acúmulo permitido |

    Esquema do Cenário: [CT-59] Forçar ação escondida não contorna a autorização
      Dado a solicitação de Ana em <situacao>, Bruno gestor, Diana e Elisa diretoras e Carlos outro panel_user da mesma organização
      Quando Carlos tenta montar e executar pelo componente a ação <acao> apesar de não vê-la
      Então a tentativa não conclui a ação e a situação, os três dados e o histórico persistidos permanecem idênticos
      E o registro não é excluído e nenhum e-mail novo é enviado

      Exemplos:
        | situacao | acao | # partição |
        | rascunho | editar | escrita horizontal |
        | rascunho | excluir | exclusão horizontal |
        | rascunho | enviar | envio horizontal |
        | aguardando_gestor | aprovar | aprovação horizontal |
        | aguardando_gestor | rejeitar com "Sem verba" | rejeição horizontal |
        | aguardando_gestor | cancelar | cancelamento horizontal |
        | aguardando_diretor | aprovar | aprovação final horizontal |
        | aguardando_diretor | rejeitar com "Sem verba" | rejeição final horizontal |

    Esquema do Cenário: [CT-65] Cada ação elegível da interface executa sua operação
      Dado a solicitação de Ana em <situacao> com valor <valor>, ator elegível <ator> autenticado, gestor Bruno, diretoras Diana e Elisa reais e outra solicitação de controle
      Quando <ator> executa pelo componente a ação <acao> da compra alvo
      Então a compra alvo fica <destino>, com <historico> e exatamente <emails> e-mails novos aos aprovadores certos
      E os três dados não alterados pela intenção e o histórico anterior ficam íntegros, a compra de controle não muda e não há erro da ação

      Exemplos:
        | situacao | valor | ator | acao | destino | historico | emails | # partição |
        | rascunho | "5000.01" | Ana | Enviar | aguardando_gestor | zero decisões novas | 1 para Bruno, zero para diretoras | envio pela UI |
        | aguardando_gestor | "4999.99" | Bruno | Aprovar | aprovada | uma aprovação de gestor por Bruno | zero | aprovação final de gestor pela UI |
        | aguardando_gestor | "5000.01" | Bruno | Aprovar | aguardando_diretor | uma aprovação de gestor por Bruno | 1 para Diana e 1 para Elisa | aprovação intermediária pela UI |
        | aguardando_diretor | "5000.01" | Diana | Aprovar | aprovada | uma aprovação de diretor por Diana | zero | aprovação final pela UI |
        | aguardando_diretor | "5000.01" | Diana | Rejeitar com "X" | rascunho | uma rejeição de diretor por Diana com "X" | zero | rejeição do diretor pela UI |
        | aguardando_gestor | "5000.01" | Ana | Cancelar | cancelada | zero decisões novas | zero | cancelamento antes do gestor |
        | aguardando_diretor | "5000.01" | Ana | Cancelar | cancelada | zero decisões novas | zero | cancelamento antes do diretor |
        | rascunho | "5000.01" | Ana | Excluir | indisponível para uso | zero decisões novas | zero | exclusão pela UI |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-77 | Usar somente situação para mostrar botão sem conferir pessoa | CT-58, CT-59 | Bruno vê aprovar/rejeitar em sua etapa; Carlos não executa nenhum dos verbos. |
| M-78 | Usar visible como única autorização da ação | CT-59 | A chamada forçada não grava decisão nem muda situação. |
| M-79 | Esconder ações corretas de todos para evitar autorização | CT-58 | Ana vê editar/excluir/enviar no rascunho; aprovadores veem ambas as decisões. |
| M-80 | Oferecer Cancelar em rascunho ou em aprovada | CT-58 | A lista exata de ações nesses estados não contém cancelar. |
| M-100 | Expor uma action elegível com callback sem efeito — revisão adversarial ADV-04 | CT-65 | Cada uma das oito linhas executa a própria action e confere seu resultado no alvo; callback vazio deixa estado/existência/histórico incorretos. |

R17 é integração da UI das regras R2/R3/R4/R6/R9/R14, cujos CT diretos satisfazem o gate fora do componente; não é uma autorização independente que exista apenas na tela.

## Regra R18 — As páginas e coleções mostram os registros corretos e têm saída de erro

> Origem: RQ-01; RQ-02; RQ-12; RQ-13; A-01; A-12. Perfil **padrão**. Técnica: **EP; cardinalidade; CRUD**.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra

  Regra: As páginas e coleções mostram os registros corretos e têm saída de erro

    Esquema do Cenário: [CT-60] Cada página de escrita abre com os campos corretos
      Dado ator autorizado e <preparo>, com gestores e diretores reais
      Quando o ator solicita por HTTP a página <pagina>
      Então a resposta contém o formulário de <entidade> e <conteudo>, além de sucesso HTTP
      E a visita não cria nem altera compra, centro, decisão ou e-mail de aprovação

      Exemplos:
        | preparo | pagina | entidade | conteudo | # partição |
        | Ana sem solicitação | create de solicitação | solicitação | campos descrição, valor e centro | visita create solicitação |
        | rascunho de Ana "Café", "5000.01", Compras | edit de solicitação | solicitação | dados "Café", "5000.01", Compras | visita edit solicitação |
        | administrador de Acme sem centro novo | create de centro | centro | campos nome e gestor | visita create centro |
        | administrador de Acme com Compras e Bruno | edit de centro | centro | nome Compras e gestor Bruno | visita edit centro |

    Esquema do Cenário: [CT-61] Situação continua correta em coleções vazias e paginadas
      Dado leitor autorizado em Acme e <quantidade> solicitações distintas com situações conhecidas, ordenação determinística escolhida no arnês, tamanho de página efetivo L maior ou igual a 2, compras que couberem na primeira página em rascunho e, se existir, compra de identidade P2 além delas em cancelada
      Quando o leitor carrega pelo componente a coleção ou a página <pagina>
      Então a página contém exatamente <esperado> e cada linha associa sua própria identidade à situação correta, em particular P2 a cancelada e nunca ao rascunho de outra linha
      E a coleção vazia não inventa solicitação nem situação

      Exemplos:
        | quantidade | pagina | esperado | # partição |
        | 0 | 1 | zero registros | cardinalidade zero |
        | 1 | 1 | o único registro | cardinalidade um |
        | L | 1 | os L registros ordenados | limite |
        | L+1 | 2 | somente a compra P2 em cancelada, sem qualquer compra da primeira página | além do limite discriminante |

    Esquema do Cenário: [CT-62] Identidades inexistentes não criam registros por acidente
      Dado Ana autorizada com seu rascunho visível, administrador autorizado para centros, identidades de compra e centro inexistentes e gestores e diretores reais
      Quando o ator autorizado tenta <operacao> com a identidade inexistente correspondente
      Então a operação informa ausência do alvo sem criar compra, centro ou decisão nem alterar os registros existentes
      E a listagem autorizada do ator continua alcançável e nenhum e-mail de aprovação é enviado

      Exemplos:
        | operacao | # partição |
        | ler detalhe de compra por HTTP | leitura de ausente |
        | editar compra por entrada direta | update de ausente |
        | excluir compra por entrada direta | delete de ausente |
        | editar centro por entrada protegida | centro update de ausente |
        | excluir centro por entrada protegida | centro delete de ausente |
```

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-81 | Registrar rota de criação/edição sem renderizar os dados e campos corretos | CT-60 | Cada uma das quatro páginas contém seu próprio formulário e valores, não só HTTP 200. |
| M-82 | Renderizar a situação de outra linha ao paginar | CT-61 | Na página 2, a identidade P2 tem estado cancelada; todas as compras da primeira página estão em rascunho, logo copiar seu estado diverge. |
| M-83 | Converter update de identidade ausente em inserção | CT-62 | Zero compra/centro/decisão nova após operação sobre alvo inexistente. |

O par visita/gravação fecha as quatro páginas: CT-60 com CT-03, CT-07, CT-48 e CT-49. Inserção entre páginas e desempate de ordenação não têm política no 00: Q9 mantém esse recorte explícito, sem copiar ordenação do PRD.

## Regra R19 — A modal de rejeição funciona com JavaScript executado

> Origem: RQ-07; RQ-08; A-07; superfície de UI: Modal Rejeitar. Perfil **padrão**. Técnica: **rastreio de interação real**.

O cenário **CT-B01** está especificado somente em `05-casos-de-teste-browser.md`. Não há duplicação do cenário no 04.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-84 | A ação existe no servidor, mas o gatilho Alpine não abre a modal | CT-B01 | O diálogo torna-se visível e o campo de justificativa pode ser preenchido no navegador. |
| M-85 | Modal abre, mas o handler JavaScript não submete a decisão | CT-B01 | Após submeter "Sem verba", o banco registra rascunho e uma rejeição de Bruno. |
| M-86 | Submissão fecha modal sem atualizar o estado visível | CT-B01 | A própria compra passa a informar rascunho na página após a rejeição. |

Cenário CT-B01 vive somente no 05. A origem comportamental é RQ-07/08; a linha do PRD identifica a modal. A existência de JS na stack, sozinha, não cria CT-B.


## Checklist de Taxonomia

| Gatilho / item percorrido | Cenário que mata ou lacuna | Grupo |
|---|---|---|
| IDOR / autorização horizontal da solicitação | CT-06/10/13/21/22/32/44/47 | Domínio e persistência; Fronteiras por organização |
| Policy/permission exercitada na ação, fora da UI | CT-06/10/13/21/22/32/50/64; integração CT-59/65 | Domínio e persistência; Formulários e leitura |
| Idempotência por intenção de escrita | CT-04 edição sem mudança; CT-11 exclusão repetida; CT-16 envio repetido; CT-35 gestor; CT-36 diretor; CT-37 rejeição; CT-34 cancelamento; criação sem identidade de intenção: lacuna Q10 | Domínio e persistência |
| Domínio condicionado | CT-17/18: valor × destino após gestor; CT-23: função acumulada × etapa | Domínio e persistência |
| Todos os campos / todos os pontos de gravação | CT-01/02/04/05/07; lacuna declarada Q1/Q2 para faixas e tetos; criação/edição de centros CT-48/49 e limites Q2 | Domínio e persistência; Formulários e leitura |
| Concorrência | CT-38/39; execução real pendente, conforme L6 | Concorrência compartilhada |
| Efeito com destinatário variável, 0/1/N | CT-15 zero gestor; CT-41 um gestor; CT-42 um/N diretores; CT-63 invariante com zero diretores, destino ainda em Q3 | Domínio e persistência; Fronteiras por organização |
| Campo opcional: ausente ≠ null ≠ "" | Justificativa é obrigatória na rejeição: CT-25. Gestor ausente no uso: CT-15; equivalência das três entradas de cadastro de centro: lacuna Q5, não presumida | Domínio e persistência |
| Listagem 0/1/L/L+1 e inserção entre páginas | CT-61 para cardinalidade/página, com estados discriminantes rascunho/cancelada; lacuna Q9 para inserção e posição contratual | Formulários e leitura |
| Ordenação: chave inexistente, nullable e empate | Lacuna L1/L3 para consumo de chave pública e Q9 para desempate; não se inventou coluna ou parâmetro de filtro | Formulários e leitura |
| Data/hora: app × banco × usuário, meia-noite, DST | CT-56/57 para instantes de aprovações e rejeições e sua ordem; lacuna Q6 para formato/fuso. Não se aplica a prazo/DST de expiração: nenhum prazo foi requerido | Formulários e leitura |
| Texto livre: acento/emoji, espaços, varchar | CT-01/04/24 preservam Unicode; CT-02/25 recusam conteúdo vazio; tetos e espaços nas bordas: lacuna Q2 | Domínio e persistência |
| Unicidade + soft delete | Não se aplica como contrato de unicidade: 00 não exige nome/descrição única nem escolhe SoftDeletes. Q8 registra mecanismo; CT-11 mantém prova de não uso | — |
| Registro removido ainda funciona | CT-11 executa os seis verbos sobre referência removida | Domínio e persistência |
| CRUD: inexistente, excluir duas vezes, editar sem mudar | CT-62, CT-11, CT-04/07/49 | Domínio e persistência; Formulários e leitura |
| Mass assignment de formulário/payload | CT-52/53/54, uma fronteira por entidade | Domínio e persistência; Fronteiras por organização; Componentes por organização |
| Upload | Não se aplica: anexos explicitamente fora do escopo do 00 | — |
| Precisão monetária | CT-01/04/17/18; centavo preservado e comparado como decimal; escala além de centavo fica Q1 | Domínio e persistência |
| Superfície Livewire completa: fora do domínio e tipo errado por ponto | Lacuna L1: 02 ausente, sem inventário. CT-54/59 cobrem payload/ações determinados, não toda superfície | Componentes por organização; Formulários e leitura |
| Estado do framework como índice, parse, coluna ou operador | Lacuna L3: consumo não inventariado; não se transfere suposta proteção da página a widgets | Formulários e leitura |
| Método público chamável via $wire | CT-59 chama ações indevidas conhecidas; demais métodos/argumentos fora da lista e tipos errados: lacuna L1 | Formulários e leitura |
| IDOR por tabela: solicitacoes_compra | CT-44 (escrita direta), CT-47 (detalhe), CT-66 (coleção) | Fronteiras por organização |
| Mass assignment por tabela: solicitacoes_compra | CT-52 para solicitante_id, tenant_id e situacao na criação e edição | Domínio e persistência |
| IDOR por tabela: centros_custo | CT-51 para update/delete estrangeiros; leitura direta adicional depende de L1 | Componentes por organização |
| Mass assignment por tabela: centros_custo | CT-53 para tenant_id, criação e edição independentes | Fronteiras por organização |
| IDOR por tabela: etapas_aprovacao_compra | CT-54 para filha alcançada pelo pai; lacuna L2 para ponto direto da filha, não coberto pelo CT do pai | Componentes por organização |
| Mass assignment por tabela: etapas_aprovacao_compra | CT-54 tenta id, vínculo, autor, decisão e justificativa; entrada direta da filha: lacuna L2 | Componentes por organização |
| Discriminante nulo fecha ou abre | Lacuna L3: distinguir consulta global legítima em job da consulta pública sem contexto. Nenhuma dispensa de controle foi presumida | Fronteiras por organização |
| Saída de 4xx/5xx/redirect | CT-47/51/62 exigem listagem própria alcançável depois da recusa; CT-27 mostra correção dentro da modal; CT-68 mostra mensagem de ausência de gestor na tela | Fronteiras por organização; Componentes por organização; Domínio e persistência; Formulários e leitura |
| Autorização do verbo irmão | CT-21 e CT-22 separados; CT-06 e CT-10 separados; CT-13 e CT-32 separados | Domínio e persistência |
| Atomicidade depois do ponto do efeito com destinatário real | CT-40; ponto de falha e execução ainda pendentes, não substituídos por CT-15 sem gestor | Domínio e persistência |
| Acumulação de papéis par a par | CT-23: solicitante×gestor, solicitante×diretor, gestor×diretor, administração×gestor, administração×diretor; CT-01/12: administração×solicitante | Domínio e persistência |
| Participante histórico / link da notificação | CT-57 preserva conteúdo histórico para leitor autorizado; direito de leitura histórica e eventual link: lacuna Q4 | Formulários e leitura |
| Teto de cada texto livre no domínio | Lacuna Q2 para descrição, nome do centro e justificativa; não marcar como coberto por validação de formulário | Domínio e persistência |

## Gate de falsificabilidade e poda

Cada regra lista mutantes plausíveis com cenário e asserção discriminante. O teto original era 2–5 no padrão e 3–6 no completo. R4/R5/R6/R14 superam seis somente por mutantes trazidos pela revisão adversarial, identificados por ADV-nn, conforme a exceção expressa do passo 6. R1 escalou BVA para três centavos de fronteira apesar do perfil padrão: truncamento precisa ser falsificado também na gravação. Nenhum mutante foi declarado morto por execução. A coluna “Cenário que mata” é a previsão falsificável; L1–L6 e Q1–Q10 não são fechados por essa previsão.

- Todos os cenários de ciclo de vida fixam a situação de partida, inclusive os positivos.
- Recusas afirmam situação, dados, histórico/decisão, existência quando relevante e e-mail. O Dado inclui os destinatários reais.
- Partições inválidas estão isoladas; dados não visados permanecem válidos. Omissão de parâmetro/null que produz erro de tipo é aceito como recusa sem efeitos, sem exigir API ou mensagem específica.
- O estado e os efeitos são relidos no banco. Retorno de uma chamada ou contagem genérica não substitui o agregado persistido.
- Todas as colunas da matriz têm célula válida exercitada e toda célula inválida tem o verbo correspondente. Campo valor e centro foram tentados também em trânsito e no terminal.
- A camada foi revista pelo observável. Autorização e validação têm cenário direto; componente prova gravação/renderização adicional. R17 integra as mesmas autorizações já exercitadas diretamente.
- Padrão até 3 blocos por regra; completo até 5, exceto **R4 com 6** após ADV2-04. CT-68 é o único teste da informação de erro na interface; manter só a chamada direta deixaria o mutante vivo. Estouro justificado pelo gate do passo 6. Esquemas contam uma vez. R19 tem um happy path de browser.
- As tabelas de decisão registram expressamente as linhas cujo comportamento ainda depende de resposta; nenhuma condição indecidida foi colapsada como se fosse equivalente.
- CT-38/39 não são substituídos por CT-35–37; concorrência e retry sequencial são observáveis diferentes.

### Cogitado e cortado

| Candidato | Decisão e motivo |
|---|---|
| Fazer fluxo inteiro solicitante→gestor→diretor no browser | Cortado como duplicação: CT-12/17/19 e componentes provam estado/atores; somente a interação JS da modal fica em CT-B01 |
| Browser só para testar required, listagem, ações ocultas ou HTTP 200 | Cortado: CT-02/27/55/58/59 usam camada mais barata com oráculo específico |
| Testar cor do badge, dark mode e acessibilidade como requisito de compras | Não derivado: 00 não define cor/tema/layout nem critério específico de acessibilidade desta feature |
| CT autônomo de log de compras vindo só do plano | Cortado: não deriva do 00. O warning explicitamente dado em A-10 foi incorporado ao CT-15 após ADV-01 |
| BVA de 255/120 e mínimo 0,01 copiados do PRD | Recusado como oráculo; Q1/Q2 preservam a lacuna |
| Testar somente dois diretores em sequência como “corrida” | Cortado como prova de concorrência; CT-36 permanece retry sequencial e CT-38 exige sincronização real |
| Duplicar cadastro idêntico e exigir uma compra só | Não derivado até Q10: igualdade de dados não identifica intenção |
| Um cenário genérico que testa aprovar e presume rejeitar protegido | Cortado; os verbos têm CT-21 e CT-22 separados |
| Cortar CT-03/07/48/49 porque há persistência direta | Mantidos: provam a gravação de cada página, exigida pelo gate da tela de escrita |
| Cortar visita porque componente salva | CT-60 mantido: prova rota/formulário de cada uma das quatro páginas, complementando a gravação |

## Revisão adversarial e fechamento

**Rodada 1 executada** pela rota `adversário-ct` via `collaboration.spawn_agent`, tarefa `adversario_ct_1`, `fork_turns="none"`. Modelo herdado da sessão, família GPT-6; identificador exato/esforço não expostos. Custo (tokens/duração): não exposto.

Entrada: somente 00 + 04 + 05 e os dois contratos de revisão. Não recebeu PRD, código nem conversa. Controles: contexto inicial novo e contrato de leitura/sem escrita; sandbox e ferramentas do host não isolam paths tecnicamente. Não houve hook Claude no Codex. Não houve leitura negada. O agente declarou leitura completa das seis áreas, R1–R19, 14 RQ, A-01–A-12 e todos os CT/CT-B.

Auditoria: hashes SHA-256 dos quatro documentos de entrada/linha de base ficaram idênticos durante a rodada. Conferência por amostragem: CT-18 só elevava alçada; CT-57 não afirmava instante da rejeição; CT-30 tinha rejeição antiga, não aprovação final. Os três achados foram confirmados diretamente na entrada. Revisão não alterou arquivos.

**15 achados distintos; 5 cenários novos e 10 oráculos reescritos; zero achado encerrado sem destino.** IDs repetidos em seções diferentes do relatório contam uma única vez.

| Achado | Destino | Fechamento |
|---|---|---|
| ADV-01 | Oráculo reescrito | CT-15: warning explicitamente requerido por A-10 incorporado como efeito auxiliar, sem cenário autônomo de logger. |
| ADV-02 | Cenário novo | CT-63: invariante de não aprovação final sem diretor; Q3 continua sem resposta direcional. |
| ADV-03 | Oráculo reescrito | CT-18: limites configurados 3000 e 7000, cada um com b−0,01/b/b+0,01. |
| ADV-04 | Cenário novo | CT-65: cada action elegível executada positivamente pelo componente com estado, histórico e e-mails exatos. |
| ADV-05 | Oráculo reescrito | CT-06: incluir gestor específico e diretor como não solicitantes em escrita direta. |
| ADV-06 | Cenário novo | CT-66: listagem e coleção excluem explicitamente identidades e dados estrangeiros. |
| ADV-07 | Cenário novo | CT-64: administrador exclui centro local sem dependências. |
| ADV-08 | Oráculo reescrito | CT-49: alterar nome, preservando gestor e identidade do mesmo centro. |
| ADV-09 | Oráculo reescrito | CT-57: rejeição e demais decisões mostram os respectivos instantes conhecidos. |
| ADV-10 | Oráculo reescrito | CT-24: justificativa de um caractere "X" em ambas as etapas; M-35 refinado para mínimo oito. |
| ADV-11 | Cenário novo | CT-67: composição e encaminhamento reais de cada tipo de e-mail no transporte de teste, sem Notification::fake. |
| ADV-12 | Oráculo reescrito | M-39 corrigido: reaproveitar a rejeição antiga de diretor como resolução da etapa atual. Aprovação final antiga seguida de novo ciclo seria inalcançável sob A-05. |
| ADV-13 | Oráculo reescrito | CT-01/12: administrador também solicitante cria e envia sem veto de papel. |
| ADV-14 | Oráculo reescrito | CT-23: administrador também gestor aprova/rejeita sua etapa. |
| ADV-15 | Oráculo reescrito | CT-23: administrador também diretor aprova/rejeita sua etapa. |

CT-63 discrimina finalização indevida sem responder Q3; CT-64 discrimina veto a exclusão administrativa válida; CT-65 discrimina callback de action vazio; CT-66 discrimina escopo só no detalhe; CT-67 discrimina composição/envio que o fake não executa. As cinco fixtures tornam observável o defeito apontado.

**Rodada 2 executada:** rota `adversário-ct`, tarefa `adversario_ct_2`, `collaboration.spawn_agent` com `fork_turns="none"`, modelo herdado, identificador/esforço não expostos. Não recebeu PRD, código ou conversa. Leu integralmente 00/04/05, inclusive o fechamento já escrito no próprio 04; não leu relatório externo. Percorreu Cadastro, Fluxo, Autorização, Efeitos, Apresentação e Interface, R1–R19, RQ-01–14, A-01–A-12 e todos os cenários/mutantes. Nenhuma leitura negada e nenhuma edição.

Auditoria: os quatro hashes de entrada permaneceram idênticos durante a rodada. Amostras confirmadas no documento: CT-13 tinha apenas Carlos, CT-56 sempre atribuía o diretor a Diana e CT-61 não fixava diferença de estado entre páginas.

**7 achados distintos; 2 cenários novos e 5 oráculos reescritos.** Todos têm destino abaixo.

| Achado | Destino | Fechamento |
|---|---|---|
| ADV2-01 | Oráculo reescrito | CT-10 e CT-13 agora executam diretamente com Carlos, gestor específico Bruno e diretora Diana, em verbos separados. |
| ADV2-02 | Oráculo reescrito | CT-21 e CT-22 incluem administradora Fernanda sem elegibilidade de gestor/diretor, nas duas etapas e em ambos os verbos. |
| ADV2-03 | Cenário novo | CT-69 conclui o segundo ciclo como Diana/Elisa, aprovando ou rejeitando, sem reutilizar resolução anterior. |
| ADV2-04 | Cenário novo | CT-68 exercita Enviar sem gestor pelo componente e exige mensagem visível de ausência de gestor, sem efeitos de envio. |
| ADV2-05 | Oráculo reescrito | CT-56 alterna Diana e Elisa como autoras reais, com a outra diretora presente e sem decisão. |
| ADV2-06 | Oráculo reescrito | Asserção de M-76 nomeia expressamente "Sem verba" e sua associação à rejeição de Diana no CT-57. |
| ADV2-07 | Oráculo reescrito | CT-61 fixa página 1 em rascunho e a compra P2 da página 2 em cancelada; M-82 compara identidade P2 e estado cancelada. |

Os matadores novos discriminam por observáveis adicionais: CT-68 exige feedback real da interface, não só recusa do domínio; CT-69 exige uma decisão legítima **depois** de reentrar na etapa diretor, não apenas chegar até ela. As ampliações de persona mantêm dados e estado válidos e variam somente quem chama.

**Convergência e escalonamento:** teto de **duas rodadas** respeitado. As omissões papel × verbo e continuação do ciclo são sinais estruturais registrados para revisão futura da granularidade de R4/R6/R8. Os achados concretos foram fechados, mas o conjunto alterado no fechamento final, especialmente CT-68/69, não foi reavaliado por uma terceira rodada. Essa parcela permanece **débito de revisão**, não selo de completude. Como o usuário está indisponível e 00/01/02 são imutáveis, o escalonamento segue neste registro e no retorno, sem abrir 03 ou editar a linha de base.

## Execução posterior, fora desta entrega

Não há teste Pest, Pint ou mutation score para rodar sobre uma especificação Markdown. Os comandos futuros são direcionados aos arquivos do índice após materialização e instalação autorizada do ambiente. Mutation testing exigirá ler a referência pest-5 da feature-wiki antes do primeiro --mutate e usar o lançador Windows validado. Driver Xdebug está presente na CLI, mas subprocesso e cobertura não foram certificados. Plugin mutate está somente transitivo no lock; isto é uma dependência a resolver, não “plugin ausente”.

O fechamento pós-implementação deve verificar cada CT com/sem o defeito correspondente, triando mutantes equivalentes e omissões separadamente. Não serão executados todos os testes existentes, porque não há código novo nem ambiente vendor e há proibição expressa de implementar.

## Índice de Cenários

Todos os arquivos abaixo são **propostos — ainda não materializados**.

| ID | Cenário | Regra | Técnica | Grupo | Costura | Arquivo | Mata |
|---|---|---|---|---|---|---|---|
| CT-01 | O solicitante cria um rascunho completo | R1 | EP; BVA 3-valores escalada para preservação de centavos | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-03, M-87 |
| CT-02 | Cada dado obrigatório é validado na criação e na edição por fora da UI | R1 | EP; BVA 3-valores escalada para preservação de centavos | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-01, M-02 |
| CT-03 | O formulário de criação grava os dados e o rascunho do solicitante | R1 | EP; BVA 3-valores escalada para preservação de centavos | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-03, M-04 |
| CT-04 | A correção direta pode trocar cada dado determinante e salvar sem alteração | R2 | estado × operação; papel × ação; EP | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-07, M-08 |
| CT-05 | Dados ficam imutáveis fora de rascunho | R2 | estado × operação; papel × ação; EP | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-05 |
| CT-06 | Nenhum aprovador ou terceiro edita o rascunho de outro solicitante | R2 | estado × operação; papel × ação; EP | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-06, M-88 |
| CT-07 | O formulário de edição salva correções e uma edição sem mudança | R2 | estado × operação; papel × ação; EP | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-07, M-08, M-09 |
| CT-08 | O solicitante exclui um rascunho inicial ou devolvido | R3 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-12 |
| CT-09 | A exclusão é recusada em cada situação não editável | R3 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-11 |
| CT-10 | Nem gestor, diretor ou terceiro excluem o rascunho alheio | R3 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-10, M-101 |
| CT-11 | A exclusão não permite reutilizar instância removida | R3 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-13 |
| CT-12 | Todo envio começa pelo gestor correto | R4 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-14, M-15, M-90 |
| CT-13 | Nem aprovador nem terceiro envia o rascunho alheio | R4 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-16, M-102 |
| CT-14 | Enviar não reabre situações já enviadas ou terminais | R4 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-17 |
| CT-15 | Centro sem gestor impede o envio | R4 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-18, M-89 |
| CT-16 | Repetir o mesmo envio não duplica o encaminhamento | R4 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-19 |
| CT-68 | A interface informa a recusa de envio por ausência de gestor | R4 | estado × operação; papel × ação; rastreio de efeito | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-103 |
| CT-17 | O limite literal de fábrica distingue os três centavos da fronteira | R5 | BVA 3-valores; tabela de decisão; estado × operação | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-20, M-21, M-23 |
| CT-18 | Uma alçada configurada substitui o default | R5 | BVA 3-valores; tabela de decisão; estado × operação | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-20, M-21, M-22, M-92 |
| CT-19 | Um diretor conclui depois da aprovação do gestor | R5 | BVA 3-valores; tabela de decisão; estado × operação | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-24 |
| CT-20 | Aprovar não cria uma etapa em situações sem decisão pendente | R5 | BVA 3-valores; tabela de decisão; estado × operação | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-25 |
| CT-63 | Ausência de diretor nunca dispensa a aprovação adicional | R5 | BVA 3-valores; tabela de decisão; estado × operação | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-91 |
| CT-21 | Aprovar exige o gestor específico ou um diretor da organização | R6 | matriz papel × ação; tabela de decisão completa | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-26, M-28, M-104 |
| CT-22 | Rejeitar tem a mesma barreira de identidade, exercitada separadamente | R6 | matriz papel × ação; tabela de decisão completa | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-26, M-27, M-28, M-104 |
| CT-23 | Acumular funções não cria aprovação automática nem veto inventado | R6 | matriz papel × ação; tabela de decisão completa | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-29, M-30, M-31, M-93, M-94 |
| CT-24 | Gestor e diretor rejeitam com justificativa curta ou Unicode | R7 | EP; estado × operação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-34, M-35 |
| CT-25 | Justificativa sem conteúdo nunca passa pela chamada direta | R7 | EP; estado × operação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-32, M-33 |
| CT-26 | Rejeitar em situação sem etapa pendente é recusado | R7 | EP; estado × operação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-36 |
| CT-27 | O componente recusa a justificativa vazia e permite corrigir a mesma modal | R7 | EP; estado × operação; rastreio de efeito | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-37 |
| CT-28 | A gravação da modal registra a rejeição do aprovador | R7 | EP; estado × operação; rastreio de efeito | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-34 |
| CT-29 | Reenvio após rejeição volta ao gestor do centro corrigido | R8 | 2-switch; EP × rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-38, M-40 |
| CT-30 | A aprovação do novo gestor não herda a conclusão do ciclo anterior | R8 | 2-switch; EP × rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-39, M-40, M-41 |
| CT-69 | O diretor decide normalmente no segundo ciclo | R8 | 2-switch; EP × rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-105 |
| CT-31 | O solicitante cancela nas duas situações em trânsito | R9 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-45 |
| CT-32 | Outro usuário não cancela a solicitação alheia | R9 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-42 |
| CT-33 | Rascunho e situações terminais não aceitam cancelamento | R9 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-43, M-44 |
| CT-34 | O cancelamento repetido não reabre a solicitação | R9 | estado × operação; papel × ação; rastreio de efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-45, M-46 |
| CT-35 | Retry do gestor não duplica aprovação nem aviso da próxima etapa | R10 | idempotência no agregado; concorrência real | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-48 |
| CT-36 | Primeiro diretor resolve a etapa também no retry sequencial | R10 | idempotência no agregado; concorrência real | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-47 |
| CT-37 | Retry de rejeição não duplica a decisão nem destrói histórico | R10 | idempotência no agregado; concorrência real | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-52 |
| CT-38 | Duas decisões simultâneas não vencem a mesma etapa | R10 | idempotência no agregado; concorrência real | Concorrência compartilhada | Pest feature HTTP | `tests/Feature/AprovacaoCompra/ConcorrenciaTest.php` (proposto) | M-49, M-50 |
| CT-39 | Cancelamento e decisão concorrentes preservam um histórico serial válido | R10 | idempotência no agregado; concorrência real | Concorrência compartilhada | Pest feature HTTP | `tests/Feature/AprovacaoCompra/ConcorrenciaTest.php` (proposto) | M-49, M-51 |
| CT-40 | Falha antes da confirmação não deixa decisão ou e-mail fantasma | R11 | rastreio de efeito com falha após o ponto do efeito | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-53, M-54, M-55 |
| CT-41 | O primeiro encaminhamento usa mail para o gestor do centro | R12 | EP × rastreio de efeito; cardinalidade 0/1/N | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-56, M-57 |
| CT-42 | A etapa diretor notifica o conjunto completo da organização | R12 | EP × rastreio de efeito; cardinalidade 0/1/N | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-56, M-58, M-59 |
| CT-43 | Operações sem próximo aprovador não geram e-mail | R12 | EP × rastreio de efeito; cardinalidade 0/1/N | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-60 |
| CT-67 | Os dois tipos de aviso compõem e encaminham e-mail de verdade no transporte de teste | R12 | EP × rastreio de efeito; cardinalidade 0/1/N | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-95 |
| CT-44 | Conhecer a identidade de outra compra não autoriza agir nela | R13 | IDOR; matriz papel × ação; EP por fronteira | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-61 |
| CT-45 | Centro de outra organização não é uma referência válida | R13 | IDOR; matriz papel × ação; EP por fronteira | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-62 |
| CT-46 | Diretor só de outra organização não decide a segunda etapa | R13 | IDOR; matriz papel × ação; EP por fronteira | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-63 |
| CT-47 | A tela não expõe o detalhe de compra de outra organização | R13 | IDOR; matriz papel × ação; EP por fronteira | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-64 |
| CT-66 | A coleção da organização não contém compras estrangeiras | R13 | IDOR; matriz papel × ação; EP por fronteira | Componentes por organização | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` (proposto) | M-96 |
| CT-48 | Administrador cria um centro com seu gestor pelo componente | R14 | papel × ação; EP; gravação por componente | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-69 |
| CT-49 | Administrador salva o gestor e também pode manter os mesmos dados | R14 | papel × ação; EP; gravação por componente | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-67, M-98 |
| CT-50 | O usuário comum não ganha poder para se nomear gestor | R14 | papel × ação; EP; gravação por componente | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-65, M-66 |
| CT-51 | Administração de uma organização não alcança centro de outra | R14 | papel × ação; EP; gravação por componente | Componentes por organização | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` (proposto) | M-68 |
| CT-64 | Administrador exclui um centro local sem dependências | R14 | papel × ação; EP; gravação por componente | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-97 |
| CT-52 | Compra não aceita colunas de controle enviadas pelo cliente | R15 | mass assignment por entidade; EP | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-70 |
| CT-53 | Centro não muda de organização por campo injetado | R15 | mass assignment por entidade; EP | Fronteiras por organização | Pest feature HTTP | `tests/FeatureTenancy/AprovacaoCompra/FronteirasTest.php` (proposto) | M-71 |
| CT-54 | Payload do pai não permite forjar ou reatribuir uma decisão filha | R15 | mass assignment por entidade; EP | Componentes por organização | componente Livewire/Filament | `tests/FeatureTenancy/AprovacaoCompra/ComponentesTest.php` (proposto) | M-72, M-73 |
| CT-55 | Listagem e detalhe informam cada uma das cinco situações | R16 | EP exaustiva de estados; rastreio de histórico | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-74 |
| CT-56 | O detalhe associa cada etapa ao autor correto | R16 | EP exaustiva de estados; rastreio de histórico | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-75, M-76, M-106 |
| CT-57 | O histórico da rejeição e dos ciclos não é substituído pelo aprovador atual | R16 | EP exaustiva de estados; rastreio de histórico | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-74, M-75, M-76, M-99 |
| CT-58 | Ações disponíveis correspondem à etapa e ao dono | R17 | matriz papel × ação × situação | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-77, M-79, M-80 |
| CT-59 | Forçar ação escondida não contorna a autorização | R17 | matriz papel × ação × situação | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-77, M-78 |
| CT-65 | Cada ação elegível da interface executa sua operação | R17 | matriz papel × ação × situação | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-100 |
| CT-60 | Cada página de escrita abre com os campos corretos | R18 | EP; cardinalidade; CRUD | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-81 |
| CT-61 | Situação continua correta em coleções vazias e paginadas | R18 | EP; cardinalidade; CRUD | Formulários e leitura | componente Livewire/Filament | `tests/Feature/AprovacaoCompra/ComponentesTest.php` (proposto) | M-82 |
| CT-62 | Identidades inexistentes não criam registros por acidente | R18 | EP; cardinalidade; CRUD | Domínio e persistência | Pest feature HTTP | `tests/Feature/AprovacaoCompra/DominioTest.php` (proposto) | M-83 |
| CT-B01 | Modal abre e submete rejeição com JS | R19 | interação real | Modal JS | browser | `tests/Browser/AprovacaoCompra/ModalRejeicaoTest.php` (proposto; cenário no 05) | M-84, M-85, M-86 |

## Referências abertas e registro substitutivo do 03

- `.ai/skills/feature-wiki/references/hosts-e-subagentes.md` — host e despacho do step 7.
- `.ai/skills/feature-wiki/references/delegacao-casos-de-teste.md` — step 7.
- `.ai/skills/feature-wiki/references/ponytail-caveman.md` — fronteira de escrita no início.
- `.ai/skills/feature-wiki/references/roteamento-e-despacho.md` — step 7 / despacho.
- `.ai/skills/feature-wiki/references/citacoes-de-codigo.md` — convenção de citação.
- `.ai/skills/feature-test-design/references/template-04.md` — passos 2, 6 e 7 / escrita do 04.
- `.ai/skills/feature-test-design/references/escolha-de-camada.md` — passos 2 e 7.
- `.ai/skills/feature-test-design/references/tecnicas-por-regra.md` — passo 3.
- `.ai/skills/feature-test-design/references/taxonomia-de-defeito.md` — passo 4.
- `.ai/skills/feature-test-design/references/gherkin.md` — passo 5.
- `.ai/skills/feature-test-design/references/armadilhas-de-api.md` — passos 5 e 7.
- `.ai/skills/feature-test-design/references/mutation-testing.md` — passo 6.
- `.ai/skills/feature-test-design/references/revisao-adversarial.md` — revisão independente.
- `.ai/skills/feature-test-design/references/pest-plugin-browser.md` — gate/escrita do 05.
- `.ai/skills/feature-test-design/references/template-05.md` — escrita do 05.

Também foi lido o contrato `feature-test-design/agents/fw-adversario-ct.md` e o perfil Codex correspondente; não são arquivos de references. Não se abriu casos-medidos, catálogo de defeitos, relatório de rodada nem conjuntos anteriores. Templates de 00–03, implementação, QA e mutation runtime não foram abertos porque essas etapas não integram a tarefa.

Sem despacho para a derivação: a sessão principal invocou e seguiu a feature-test-design local, sem escrever o plano nem implementar. A revisão adversarial é despachada separadamente, sem histórico da derivação. Registros que a skill remeteria ao 03 serão reportados no retorno, conforme instrução expressa de não criar esse arquivo.

## Conferência final da especificação

Conferências mecânicas executadas em 2026-10-20, após fechar as duas rodadas:

| Verificação | Resultado observado |
|---|---|
| grep canônico: cenários, regras, mutantes, sem matador | 69, 19, 106, 0 |
| grep de CT-B do 05 | 1 |
| Um Quando e um Então por bloco Gherkin | 70 blocos; zero erro |
| Variáveis de esquema e colunas de exemplos | zero erro |
| Cenários do 04 e índice | 69 IDs únicos; zero diferença |
| Mutantes | 106 IDs únicos |
| Matriz única | 19 válidas + 21 inválidas = 40 células |
| Placeholders | zero |
| Fechamentos individuais | 15 da rodada 1 e 7 da rodada 2 |
| Saída | somente 04-casos-de-teste.md e 05-casos-de-teste-browser.md |
| Hashes SHA-256 antes/depois | 244 arquivos protegidos iguais, sem novo/alterado nesse inventário; inclui 00/01 imutáveis |

Comandos canônicos, executados com Git Bash na pasta desta saída:

```bash
grep -cE '^[[:space:]]*(Cenário|Esquema do Cenário): \[CT-[0-9]+\]' 04-casos-de-teste.md
grep -cE '^## Regra R[0-9]+' 04-casos-de-teste.md
grep -cE '^\| M-?[0-9]+' 04-casos-de-teste.md
grep -cE '^\| M-?[0-9]+.*sem matador' 04-casos-de-teste.md
grep -cE '^[[:space:]]*Cenário: \[CT-B[0-9]+\]' 05-casos-de-teste-browser.md
```

O grep sem ocorrências imprime 0 e pode sair com código 1. A validação estrutural não transforma matadores previstos em mutantes executados. Não foram criados scripts de verificação, testes Pest, migrations, models ou outros artefatos.




# Casos de Teste de Browser — FERRO-830: Aprovação de solicitação de compra

> Derivado do 00, com a modal localizada na Superfície de UI do 01.
> Costura **browser**: grupo **Modal JS**, regra **R19** do 04.
> Runtime previsto: Pest browser 5.0.1 / Playwright; o plugin serve a aplicação.
> **CT-B: 1. Execução: não realizada; esta entrega contém somente especificação.**
> Comando futuro, depois da materialização: `php artisan test --compact tests/Browser/AprovacaoCompra/ModalRejeicaoTest.php`, em série.
> A suíte Browser está declarada no phpunit.xml. A rule local proíbe --parallel, prevalecendo sobre a referência genérica.

## Pré-requisitos

- [ ] Dependências PHP instaladas de forma autorizada; hoje vendor não existe.
- [ ] Browser e Playwright efetivamente instalados; hoje só foram conferidas declaração e versões travadas.
- [ ] `npm run build` executado antes do run. Não abrir servidor externo, Herd ou artisan serve.
- [ ] Seeders de permissions e papéis aplicados na ordem do projeto.
- [ ] Fixtures reais e autenticação por `$this->actingAs($bruno)` antes de `visit()`; sem login manual neste CT-B.
- [ ] A solicitação de Ana é a única linha da coleção e está em **aguardando_gestor**, valor decimal **"5000.01"**, com Bruno gestor e Diana/Elisa diretoras reais.
- [ ] O setup fez envio real e depois limpou somente o observador de e-mails, conforme o 04.
- [ ] Conferir seletores contra a UI implementada e ignorar screenshots não autorizados de dado sensível.
- [ ] Não executar `wait(n)`. Aguardar assertions sobre estado final dentro do timeout já definido no projeto.

O gate passa pela linha **Modal Rejeitar** da Superfície de UI e pelo observável **abrir, editar e submeter o diálogo através de JavaScript executado**. Não passa pelo simples fato de Filament usar JS. Validação de domínio, ação indevida, regra de justificativa e gravação server-side continuam CT-24–28/59 no 04.

## Seletores

| Elemento | Seletor proposto | Situação |
|---|---|---|
| Compra alvo na listagem | Única solicitação da fixture, identificada pela descrição "Aquisição de café ☕" | Fixture específica; não aceitar texto genérico de layout |
| Gatilho da rejeição | Texto traduzido Rejeitar na linha da compra | Localizado no 01; confirmar na implementação futura |
| Diálogo aberto | `[role="dialog"]` | Proposta sem inspeção da UI; confirmar atributo acessível real |
| Justificativa | `[role="dialog"] textarea` | A modal localizada tem um campo de texto; confirmar seletor |
| Submissão | `[role="dialog"] button[type="submit"]` | Proposta; confirmar marcação real, sem inventar data-testid |
| Situação final | Texto/elemento da própria compra que informa rascunho | Conferir tradução da UI; o oráculo é o estado semântico, não frase escolhida pelo PRD |

Não foram inspecionados DOM nem código da feature. Seletores são **propostos**, não “verificados”. Ajuste futuro de seletor não pode alterar o resultado de negócio exigido.

## CT-B01 — A modal abre e submete a rejeição pelo JavaScript

**Origem:** RQ-07, RQ-08; A-07. **Regra:** R19, perfil padrão. **Grupo:** Modal JS.

**Por que browser:** um componente pode executar a ação PHP mesmo com o gatilho Alpine ou o handler de submissão quebrado. Este cenário exige o diálogo visível, campo editável e retorno visual após interação real.

```gherkin
# language: pt
Funcionalidade: Aprovação de solicitação de compra
  Regra: A modal de rejeição funciona com JavaScript executado
    Cenário: [CT-B01] O gestor rejeita pela modal interativa
      Dado Bruno autenticado na listagem com a única solicitação de Ana em aguardando_gestor, valor "5000.01", Diana e Elisa como diretoras reais
      Quando Bruno usa o gatilho e a modal da própria compra para rejeitar com justificativa "Sem verba"
      Então o diálogo foi visível e editável antes da submissão e a própria compra passa a informar rascunho após a submissão
      E o banco contém uma nova rejeição da etapa gestor por Bruno com "Sem verba", preserva o histórico anterior e registra zero e-mails novos
```

**Roteiro executável futuro** — uma intenção do usuário, rejeitar. Os passos mecânicos não se tornam cenários de domínio adicionais.

| # | Ação | Forma Pest prevista | Oráculo |
|---|---|---|---|
| 1 | Autenticar Bruno e definir painel app no modo padrão | `$this->actingAs($bruno)` antes de visit | Pessoa distinta de Ana, papel e gestor corretos |
| 2 | Abrir a listagem gerada pelo Resource | `visit($path)->assertPathIs($path)` | Depois conferir descrição da única compra e situação aguardando gestor |
| 3 | Acionar Rejeitar na linha | `$page->press('Rejeitar')->assertVisible('[role="dialog"]')` | Diálogo fica de fato visível; HTML escondido não basta |
| 4 | Escrever a justificativa no campo da modal | `$page->fill('[role="dialog"] textarea', 'Sem verba')` | Campo aceita a edição no diálogo aberto |
| 5 | Submeter pelo botão da modal | `$page->click($seletorSubmit)->assertPathIs($path)` | Aguardar estado rascunho na própria linha, sem wait fixo |
| 6 | Conferir UI, banco e ausência de efeito extra | `assertNoJavaScriptErrors()` como apoio; asserções da compra/decisão/e-mails do 04 | Estado rascunho, uma rejeição de Bruno, justificativa exata, histórico prévio íntegro, zero avisos novos |

O executor deve conferir a forma de `press/click/fill` e os seletores na versão instalada antes de codificar. As APIs de visibilidade, caminho e assertions foram consultadas na [documentação oficial do Pest](https://pestphp.com/docs/browser-testing). Não usar console limpo como único oráculo; não exigir assertNoSmoke de todos os plugins da tela.

#### Mutantes previstos

Os IDs são os mesmos de R19 no 04, sem duplicar a contagem do conjunto.

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-84 | A ação existe no servidor, mas o gatilho Alpine não abre a modal | CT-B01 | O diálogo torna-se visível e o campo de justificativa pode ser preenchido no navegador. |
| M-85 | Modal abre, mas o handler JavaScript não submete a decisão | CT-B01 | Após submeter "Sem verba", o banco registra rascunho e uma rejeição de Bruno. |
| M-86 | Submissão fecha modal sem atualizar o estado visível | CT-B01 | A própria compra passa a informar rascunho na página após a rejeição. |

## Roteiro de Validação: Desenhado × Implementado

Não houve implementação nem execução autorizada. Todas as linhas continuam **não verificadas**.

| Linha da superfície do 01 | Prova alocada | Implementado | Confere? | Evidência |
|---|---|---|---|---|
| Listagem e ações | CT-55/58/59/61 no 04 | Não inspecionado | Não verificado | Somente especificação |
| Formulário create/edit de compra | CT-03/07/60 no 04 | Não inspecionado | Não verificado | Somente especificação |
| Detalhe e histórico | CT-55/56/57 no 04 | Não inspecionado | Não verificado | Somente especificação |
| Modal Rejeitar | CT-27/28 no 04; CT-B01 para JS | Não inspecionado | Não verificado | Somente especificação |
| Confirmações Enviar/Cancelar | Regras R4/R9 e integração CT-58/59; browser redundante cortado | Não inspecionado | Não verificado | Não confundir modal existente com JS certificado |
| Centro de custo create/edit | CT-48/49/50/51/60 no 04 | Não inspecionado | Não verificado | Somente especificação |

