# Casos de Teste de Browser — FERRO-830: aprovação de compra

> Fonte normativa: `wikis/specs/oraculo/aprovacao-de-compra/00-requisito.md`; regra R24 do 04.
> Runtime proposto: pest-plugin-browser 5.0.1 / Playwright, conforme lock. Nenhuma execução nesta rodada.
> Costura: **browser**, grupo **G6 Interação JS**, confirmado pela sessão em **2026-10-20**.
> Arquivo futuro: `tests/Browser/AprovacaoCompra/InteracaoTest.php`.
> Comando futuro: `vendor/bin/pest --testsuite=Browser --filter=AprovacaoCompra`, **em série**.
> A suíte Browser existe no phpunit.xml. O filtro exige os nomes dos testes com AprovacaoCompra.
> Os demais cenários permanecem no componente/domínio. Dois CT-B: um caminho feliz e um erro visível.

## Pré-requisitos

- [ ] Dependências do lock instaladas e assets produzidos com `npm run build`; não realizados aqui.
- [ ] PHP/Pest/browser funcionais; vendor está vazio nesta cópia. Playwright só foi confirmado em package.json.
- [ ] Usar TestCase + RefreshDatabase já ligados a tests/Browser; fixture single-tenant para isolar JS.
- [ ] Autenticar por `$this->actingAs($ator)` antes de `visit()`; não gastar este CT com login pela tela.
- [ ] Construir situação com transições reais conforme Setup Global do 04; limpar fakes depois do setup.
- [ ] Conferir exclusão de `tests/Browser/Screenshots` do versionamento antes de produzir screenshots; nenhum screenshot criado.
- [ ] Confirmar seletores reais no primeiro build. Não usar ref transitório do MCP ou classe CSS visual.
- [ ] Nenhum servidor externo: o plugin sobe HTTP in-process em porta aleatória; sem artisan serve ou APP_URL.
- [ ] Não usar esperas fixas. Assertions repetem até timeout existente de 20.000 ms.
- [ ] Toda navegação: `assertPathIs()` antes de conteúdo. `assertNoJavaScriptErrors()` é apenas apoio.

Convenção local .ai/rules/testes-browser.md **proíbe --parallel**, mesmo que a skill genérica permita depois de provar isolamento.
MCP/browser manual não é cobertura. Nenhuma observação de UI foi feita nesta rodada.

## Seletores

A UI de compra não foi lida nem implementada. Os seletores abaixo são **contratos de materialização propostos**, não locators comprovados.

| Elemento | Preferência de seletor | Situação |
|---|---|---|
| Página | rota de resource `/app/solicitacoes-de-compra` | Endereço do 01, contexto single-tenant de teste. |
| Ação de registro | texto traduzido Enviar/Rejeitar, com só uma solicitação elegível na fixture | Evitar selecionar ação de outro registro. |
| Modal ativo | `[role="dialog"]` se confirmado no DOM; senão locator acessível real do Filament | Não substituir visibilidade por presença do texto no DOM. |
| Confirmar | botão traduzido dentro do modal ativo | Resolver locator após render; não assumir que todo botão é type=submit. |
| Justificativa | rótulo acessível do campo mostrado no modal | Rótulo exato do 01 não é requisito; usar o que a UI renderizar. |
| Erro da justificativa | elemento visível associado ao campo/aria-describedby | Não afirmar só existência de erro genérico em outro campo. |
| Situação da solicitação | conteúdo associado ao ID/descrição única da fixture | Não aceitar outro badge da página como resultado. |

API de `press`, `assertVisible`, `assertSeeIn`, `assertScript`, `assertPathIs` e console conferida na [documentação oficial do Pest](https://pestphp.com/docs/browser-testing).
Quando o seletor ainda não existe, o roteiro diz como resolvê-lo; não inventa método de espera ou helper de escopo.

## CT-B01: Confirmar envio opera o modal com JavaScript real

**Origem:** RQ-04/12, A-12 · R24 · perfil completo.
**Por que Browser:** listener do botão, abertura efetiva de modal e sincronização visual após request não são executados pelo teste de componente.
A modal é mecanismo da Superfície de UI; o oráculo de negócio continua sendo pendência do gestor.

```gherkin
# language: pt
Funcionalidade: Interação com ações da solicitação de compra
  Regra: A ação de envio é operável no navegador
    Cenário: [CT-B01] Modal e envio funcionam com JavaScript executado
      Dado Sofia autenticada e uma única solicitação própria em rascunho no centro de Guilherme
      Quando Sofia aciona Enviar e confirma a mesma intenção no modal visível
      Então o modal realmente abriu e a linha da solicitação passa visivelmente a aguardando gestor
      E o banco contém aguardando_gestor para essa solicitação, preservando dados e solicitante
```

**Roteiro executável na materialização:**

| # | Ação | API Pest / preparação | Resultado |
|---|---|---|---|
| 1 | Autenticar e abrir listagem | `actingAs(Sofia)`; `visit('/app/solicitacoes-de-compra')->assertPathIs('/app/solicitacoes-de-compra')` | Registro único identificado, estado rascunho visível. |
| 2 | Acionar envio | `->press('Enviar')` | Modal ativo deve satisfazer `assertVisible(locatorDoModal)`. |
| 3 | Confirmar no modal | `->click(locatorDoBotaoConfirmar)`, locator acessível resolvido e único | Request Livewire concluído pelo estado visível, sem wait(n). |
| 4 | Conferir resultado | Assertion de situação ligada à solicitação; se houver navegação, path primeiro | Estado visível aguardando gestor; modal fechado; console sem erro JS. |
| 5 | Uma âncora no banco | assertDatabaseHas com ID, situacao, descricao, valor, centro e solicitante anteriores | Mesmo agregado passou a aguardando_gestor. |

Não repetir assertions completas de e-mails do CT-43: esse não é o valor adicional do Browser.

## CT-B02: Justificativa vazia mantém erro visível no modal correto

**Origem:** RQ-07/08, A-07/A-12 · R24 · perfil completo.
**Por que Browser:** pode existir erro no servidor e o modal fechar, ficar invisível ou perder sua associação com o campo em Alpine.

```gherkin
# language: pt
Funcionalidade: Interação com ações da solicitação de compra
  Regra: A recusa por justificativa ausente permanece visível ao aprovador
    Cenário: [CT-B02] Rejeição vazia mostra o erro sem fechar silenciosamente o modal
      Dado Guilherme autenticado e solicitação de Sofia aguardando_gestor por envio real, com justificativa vazia no modal de rejeição aberto
      Quando Guilherme confirma a rejeição sem justificativa
      Então o modal permanece visível e o erro de obrigatoriedade aparece associado à justificativa
      E o banco conserva aguardando_gestor e o histórico anterior, sem rejeição gravada
```

**Roteiro executável na materialização:**

| # | Ação | API Pest / preparação | Resultado |
|---|---|---|---|
| 1 | Preparar pendência real e autenticar | Transição enviar no setup; limpar fakes; `actingAs(Guilherme)` | Ator é gestor, único erro possível é justificativa. |
| 2 | Abrir listagem e modal | `visit(...)->assertPathIs(...)`, `->press('Rejeitar')`, `->assertVisible(locatorDoModal)` | Modal da solicitação correta, campo vazio. |
| 3 | Submeter vazio | `->click(locatorDoBotaoConfirmarRejeicao)` | Validação ocorre no fluxo real de JS. |
| 4 | Conferir erro operável | `assertVisible(locatorDoModal)` e `assertVisible(locatorDoErro)`; texto obrigatório no contêiner do campo | Não basta assertSee genérico; não fixar redação de mensagem ausente no 00. |
| 5 | Uma âncora no agregado | Leitura com situação e tuplas históricas comparadas ao snapshot | Aguardando_gestor e histórico original; nenhuma rejeição. Console sem erro JS. |

O preenchimento válido completo já é provado em CT-29/35. Não juntar uma segunda intenção de rejeição neste CT-B.

## Mutantes previstos de R24

Fonte única no 04; esta cópia deve permanecer sincronizada.

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-87 | Renderizar Enviar mas perder o listener que abre/submete a confirmação | CT-B01 | Modal aparece por clique real e, após confirmar, estado visível muda para aguardando_gestor. |
| M-88 | Erro de justificativa existe no servidor mas Alpine fecha modal sem mostrá-lo | CT-B02 | Modal continua visível com erro junto à justificativa, sem mudar a compra. |
| M-89 | Associar o erro à instância errada de modal e deixar o formulário rejeitado sem mensagem | CT-B02 | A mensagem fica visível junto ao campo justificativa da solicitação alvo. |

## Roteiro de Validação: Desenhado × Implementado

**Não executado**: escopo desta entrega é somente especificação. A coluna Implementado não foi inferida pelo plano.

| # | Superfície desenhada | Prova prevista | Implementado | Evidência |
|---|---|---|---|---|
| 1 | Listagem com situação e ações | CT-48/50 e CT-B01 | não verificado | nenhuma execução |
| 2 | Form create/edit | CT-02/06, visitas CT-56 | não verificado | nenhuma execução |
| 3 | Detalhe e histórico | CT-49/51/52 | não verificado | nenhuma execução |
| 4 | Modal Rejeitar | CT-29/32/35 e CT-B02 | não verificado | nenhuma execução |
| 5 | Modal Enviar/Cancelar | CT-18/38 e CT-B01 para JS de envio | não verificado | nenhuma execução |
| 6 | Centros, nome e gestor | CT-53/54/55/56 | não verificado | nenhuma execução |

Modal de Cancelar como CT-B foi cogitada e cortada: transição CT-38 no componente e mesmo mecanismo geral de modal de confirmação do CT-B01.
Se a implementação trouxer JS específico de cancelamento que esses CT não exercitem, reabrir o gate com mutante próprio; não declarar prova por semelhança de código.

## Limitações

As lacunas do 04 continuam vigentes, especialmente L1 (02 ausente), L3 (sem execução) e Q3 (visibilidade histórica/link).
Nenhum teste de tema foi criado com assertSee, nenhum baseline de screenshot foi certificado como aparência correta.

