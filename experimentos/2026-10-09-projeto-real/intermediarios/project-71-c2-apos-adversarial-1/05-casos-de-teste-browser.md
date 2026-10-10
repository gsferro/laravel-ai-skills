# Casos de Teste Browser — FERRO-830: Aprovação de solicitação de compra

> Requisito: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md` · Regra R6 do 04.
> feature-wiki 4.0.0 · feature-test-design 1.16.0 · Codex/GPT-6; ID exato não informado; esforço ultra solicitado.
> **Revisão adversarial: rodada 1 recebida; nenhum achado comprovado nos CT-B; rodada 2 PENDENTE — despacho independente pela sessão principal.**
> Dois CT-B projetados, nenhum teste implementado/executado. 02 e glossário ausentes.

## Gate e Camada

A rejeição pede justificativa e deve poder ser confirmada pela ação da UI. CT-18/19 provam a regra no domínio e CT-20 a validação no componente. Esses testes não acionam o botão real com JavaScript nem demonstram que a modal aparece e que seu submit fica conectado à ação correta. CT-B01 cobre esse caminho feliz real; CT-B02 a exibição do erro e permanência na modal. Esta é a única asserção do conjunto que depende do navegador. Não repetir todo o fluxo de aprovação no browser.

Origem: RQ-06, RQ-07, RQ-08; A-07/A-12. Perfil herdado: completo. Camada: browser. Grupo: Modal de rejeição com JS. Destino planejado: `tests/Browser/AprovacaoCompra/ModalRejeicaoTest.php`, não criado. Gherkin usa comportamento do 00; rota e rótulo do botão são endereços da Superfície de UI do 01.

## Pré-requisitos

- [ ] `npm run build` executado nesta rodada — **não executado**; um manifest existente não comprova build desta feature.
- [x] `tests/Browser/Screenshots` consta no .gitignore — leitura local confirmada; nenhum baseline/screenshot gerado.
- [ ] Dependências Node, navegador Playwright e plugin prontos para executar — plugin browser 5.0.1 no vendor; node_modules e instalação local Playwright ausentes nesta cópia.
- [ ] Feature implementada e migrações/fixture prontas — não implementadas por instrução da rodada.
- [ ] Autenticação antes de visit com `$this->actingAs($gestor)` e painel app/contexto do projeto.
- [ ] Uma solicitação de Sofia aguardando_gestor, por criação → enviar reais, valor 1299.99, centro Operações de Geraldo; Daniela diretora real; pessoas distintas e e-mails válidos.
- [ ] Captura Notification::fake() iniciada **depois** da fixture, só para a ação medida; situação/histórico consultados novamente no banco.
- [ ] Inspeção do DOM final para confirmar seletores e o nó de erro; estes são localizadores candidatos, sem evidência de app rodando.

O Pest browser serve HTTP in-process em porta aleatória; não exige Artisan serve, Herd, Vite server ou configuração de APP_URL. Não executar com --parallel. Nenhum comando de execução foi rodado. O futuro filtro restrito é `php artisan test --compact tests/Browser/AprovacaoCompra/ModalRejeicaoTest.php`, após os pré-requisitos, fora desta rodada.

## Seletores

| Alvo | Localizador candidato | Fundamentação e pendência |
|---|---|---|
| Lista | /app/solicitacoes-de-compra | rota da UI do 01; visitar e afirmar assertPathIs antes de conteúdo |
| Ação na única linha da fixture | texto Rejeitar | rótulo de endereço da UI; garantir uma solicitação e um botão correspondente; se houver outros, escopar a linha pelo UUID do registro |
| Modal ativa | form:has(textarea):visible | view genérica do vendor renderiza form com wire:submit e x-show; não pressupor role=dialog que não foi encontrado |
| Justificativa | form:has(textarea):visible textarea | apenas campo dentro da modal ativa; campo real ainda precisa de inspeção |
| Confirmar | form:has(textarea):visible button[type="submit"] | envio real do form, sem callAction backend |
| Erro da justificativa | nó de erro visível associado ao textarea, a confirmar no DOM final | não inventar data-testid, texto de tradução ou classe que não existe; sem esse locator CT-B02 não é executável ainda |

Não há DOM da compra nesta cópia. Os candidatos não foram registrados como seletores validados. Na materialização, usar texto/label/atributo real; não introduzir testid sem necessidade. assertSee isolado pode aceitar texto oculto: o modal/campo/erro precisam de assertVisible. Nenhum wait fixo; o browser espera os elementos. assertNoJavaScriptErrors é complementar, nunca o único oráculo.

## CT-B01: A modal abre e a confirmação real rejeita a solicitação com a justificativa

```gherkin
# language: pt
Funcionalidade: Rejeição da compra pelo navegador

  Regra: A rejeição exige justificativa e devolve a solicitação ao rascunho

    Cenário: [CT-B01] A abertura e o submit com JavaScript executam a rejeição certa
      Dado a solicitação de Sofia está aguardando_gestor em Acme por transições reais, sem decisões, com Geraldo gestor e Daniela diretora real
      Quando Geraldo abre Rejeitar nessa solicitação e confirma a justificativa “Sem verba” pelo formulário real da modal
      Então a modal e seu campo foram visíveis antes da confirmação e a solicitação persistida está em rascunho
      E existe exatamente uma decisão rejeitada de gestor, por Geraldo, com justificativa “Sem verba”, e zero novos e-mails para Sofia, Geraldo ou Daniela
```

Roteiro de materialização: autenticar e escolher contexto antes de visit; `visit('/app/solicitacoes-de-compra')->assertPathIs('/app/solicitacoes-de-compra')`; clicar Rejeitar; afirmar modal ativa e textarea visíveis; preencher “Sem verba”; clicar submit dentro da mesma modal; esperar a conclusão por condição visível, sem sleep; afirmar modal fechada ou estado atualizado no registro, com rota conferida se houver navegação. Consultar banco para o mesmo ID, etapa/autor/justificativa concretos e contagem. Não substituir os dois cliques por callAction. Mensagem literal de toast e cores não são oráculo do 00.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| MB-01 | Botão Rejeitar renderiza mas evento JavaScript não abre a modal | CT-B01 | form ativo e textarea visíveis depois do clique |
| MB-02 | Submit da modal está ligado a outra ação, outra solicitação ou perde o texto | CT-B01 | mesmo ID em rascunho, uma decisão rejeitada de gestor por Geraldo com “Sem verba” |

## CT-B02: O erro de justificativa fica visível e o formulário continua utilizável

```gherkin
# language: pt
Funcionalidade: Rejeição da compra pelo navegador

  Regra: A rejeição exige justificativa e devolve a solicitação ao rascunho

    Cenário: [CT-B02] A confirmação vazia mostra o erro no campo e conserva a etapa
      Dado a solicitação de Sofia está aguardando_gestor em Acme por transições reais, sem decisões, com Geraldo gestor e Daniela diretora real
      Quando Geraldo abre Rejeitar e confirma o formulário real com a justificativa vazia
      Então a modal permanece visível e mostra um erro visível associado ao campo justificativa
      E a solicitação persistida permanece aguardando_gestor, com zero decisões e zero novos e-mails para Sofia, Geraldo ou Daniela
```

Roteiro: mesma autenticação/rota e clique real; afirmar modal/campo visíveis; esvaziar textarea; confirmar pelo submit; afirmar a permanência da modal e **o nó real de erro visível do campo**, sem depender de assertSee global, erro de console ou status HTTP. Depois, consultar o mesmo registro e os não-efeitos. Caso a implementação use validação nativa do navegador antes do servidor, confirmar o indicador real ligado ao campo e conservar os mesmos oráculos; não fingir que o plugin inspecionou um texto inexistente.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| MB-03 | Backend recusa, mas a modal fecha ou não apresenta o erro ao usuário | CT-B02 | modal ainda visível e indicador real de erro associado à justificativa visível |

## Roteiro de Validação: Desenhado × Implementado

| Superfície da UI | Desenhado para provar | Implementado/verificado nesta rodada |
|---|---|---|
| Formulário da solicitação create | CT-04 visita; CT-03 fill/create e persistência | não implementado/não executado |
| Formulário edit | CT-08 visita da segunda compra; CT-07 fill/save de B e conservação de A; CT-66 barreira de estado no componente | não implementado/não executado |
| Listagem com situação e ações | CT-45/47 conteúdo; CT-67 estados distintos por linha; CT-33/37 autorização; CT-65 recusa sem gestor; CT-B01 clique real Rejeitar | não implementado/não executado |
| Detalhe com histórico | CT-46/48/49/50 situação, quem, instante e justificativa; CT-71 conserva exibição depois do reenvio | não implementado/não executado |
| Modal Rejeitar | CT-B01 abertura/submit; CT-B02 erro visível; CT-18/19/20 domínio/componente | não implementado/não executado; DOM ainda não existe |
| Modal Enviar/Cancelar | CT-12/24 domínio; JS de confirmação não tem asserção própria no 00; sem CT-B duplicado | não implementado/não executado; interação browser não coberta por este 05 |
| Cadastro/edição centro de custo | CT-51/52/53/54 visitas e persistência de nome/gestor; CT-69 exclusão positiva sem referências; CT-55/56 autorização | não implementado/não executado |

## Limites e Revisão

Nada executado de build, browser, Pest, mutation ou SMTP. Fakes medem despacho/canal e não entrega real. Não houve Playwright MCP, screenshot, avaliação de tema/cor/acessibilidade nem medição de estabilidade do locator. Os três mutantes MB são previsões e não mutation score. A rodada 1 independente percorreu 00/04/05 e apontou 11 achados do 04, sem achado comprovado nestes dois CT-B. Os CT-B e seus três mutantes foram preservados; o fechamento de todos os ADV consta no 04. Rodada 2 PENDENTE para o conjunto integral 00/04/05, sem autorrevisão. Nenhum navegador foi executado nesta resolução.

