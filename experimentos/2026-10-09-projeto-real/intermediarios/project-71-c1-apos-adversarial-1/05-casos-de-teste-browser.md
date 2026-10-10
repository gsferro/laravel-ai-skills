# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Derivado do **00-requisito.md** e das premissas dadas, não dos aceites do PRD.
> Costura: **G-B / browser**, R17 do 04. Runtime: pest-plugin-browser 5.0.1 / Playwright.
> Comando futuro: `vendor/bin/pest --testsuite=Browser --filter=Cupom`, em série. Suíte Browser confirmada no phpunit.xml.
> **Cenários: 2** · Especificados, não executados. Rodada adversarial 1 realizada; rodada 2 do conjunto **PENDENTE** por novos CT no 04. Nenhum achado da rodada 1 exigiu alterar os CT-B.
> Um happy path e um erro/reparo visível: excede o teto padrão de um CT-B porque M-62 só é falsificado pela recuperação visível.

## Pré-requisitos

- [ ] Feature materializada e 02 com Superfície Livewire disponível; CT-30 prova concorrência antes do browser.
- [ ] `npm run build` executado; o manifest deve existir antes da suíte.
- [ ] Playwright e browser instalados; playwright ^1.62.1 declarado no package.json. Instalação efetiva do browser não foi testada.
- [ ] Autenticar com `$this->actingAs($user)` antes de visit; helper `usuarioComPapel`, membership e `noPainelDa` do projeto.
- [ ] Screenshots de falha fora do versionamento conforme .gitignore; não foi produzida screenshot nesta rodada.
- [ ] Não usar `--parallel`, `wait(n)` ou servidor externo. O plugin serve a aplicação in-process.
- [ ] Se executar um arquivo isolado com views frias, aplicar o procedimento conhecido do arnês; não ampliar timeout para esconder falha.

O 00 define unidade em pontos percentuais inteiros ou centavos. O texto exato do rótulo é livre; o teste verifica **semântica de unidade visível**, usando o texto do componente materializado como seletor, não elevando a frase do PRD a requisito. A troca pelo navegador é o observável distinto do componente/DB.

## Seletores

| Elemento | Seletor proposto | Já existe? |
|---|---|---|
| Código, tipo, valor, validade, limite | id gerado pelo Schema; confirmar `[id="data.codigo"]`, `[id="data.tipo"]`, `[id="data.valor"]`, `[id="data.expira_em"]`, `[id="data.limite_de_usos"]` | **não confirmados**, a feature ainda não está materializada |
| Unidade | label associado ao campo valor; leitura visível dentro do campo | confirmar no HTML final |
| Salvar/criar | texto traduzido do submit no form da página | confirmar; sem selector por classe de CSS |
| Erro de valor | mensagem associada ao campo; aria-describedby/aria-invalid quando presente | confirmar associação no HTML final |
| Listagem | registro identificado pelo código exato | comportamento comprovado mais barato em CT-22–24 |

Dívida de seleção declarada: o projeto não disponibiliza data-testid segundo a rule local; isso não autoriza criar selector ou atributo fictício. ids de exemplo devem ser substituídos pelos ids **observados** antes de materializar. APIs reais conferidas no vendor: `visit`, `select`, `fill`, `press`, `assertPathIs`, `assertSeeIn`, `assertVisible`, `assertAttribute`, `assertNoJavaScriptErrors`. Sem `waitForText`/helpers inventados. Não usar assertSee de texto de layout como prova de unidade ou visibilidade.

---

## CT-B01: A unidade acompanha a escolha real do tipo

**Origem**: RQ-01, RQ-03 e P-05. **Regra** R17. **Por que browser e não Livewire**: somente o navegador prova que a alteração enviada pelo Select torna a nova indicação visível ao usuário sem reload, com JavaScript real. A gravação é apenas uma âncora do fluxo; domínio e CRUD completos já pertencem ao 04.

```gherkin
# language: pt
Funcionalidade: Cadastro de cupons pelo painel
  Regra: O valor apresentado tem a unidade do tipo escolhido

    Esquema do Cenário: [CT-B01] a unidade muda junto do tipo selecionado
      Dado a administradora da Acme na criação de NOVO com tipo inicial <inicial> e demais atributos válidos
      Quando a administradora seleciona <final> pelo navegador sem recarregar a página
      Então a indicação visível do campo valor expressa <unidade> e não conserva a unidade anterior
      E ao concluir o formulário com valor <valor> NOVO é gravado na Acme com tipo <final> e valor <valor>

      Exemplos:
        | inicial     | final       | unidade                 | valor | # partição |
        | porcentagem | fixo        | centavos                | 1000  | teto percentual removido |
        | fixo        | porcentagem | pontos percentuais      | 29    | unidade percentual restaurada |
```

### Roteiro executável

| # | Ação | Código Pest / conferência | Resultado observável |
|---|---|---|---|
| 1 | preparar administradora/contexto e dados válidos | `$this->actingAs($administradora)`; contexto/membership reais | acesso administrativo Acme |
| 2 | abrir criação | `visit('/app/acme/cupons/create')->assertPathIs('/app/acme/cupons/create')` | formulário de cupom |
| 3 | preencher dados e confirmar tipo inicial | `fill($codigoId, 'NOVO')`, `select($tipoId, $inicial)`; demais campos | indicação inicial visível |
| 4 | escolher outro tipo pela UI | `select($tipoId, $final)` | estado aguardado por assertion, sem wait fixo |
| 5 | conferir associação de label e unidade | `assertVisible($labelValor)`; texto associado expressa percentual ou centavos | unidade nova visível, antiga não indicada |
| 6 | concluir fluxo para uma âncora de persistência | `fill($valorId, $valor)->press($submit)`; se navega, `assertPathIs($destino)` antes de conteúdo | NOVO na Acme com tipo/valor concretos |
| 7 | verificar console de apoio | `assertNoJavaScriptErrors()` | apoio, nunca oráculo único |

Destino após salvar é escolha da página final (listagem ou edição): confirmar antes de materializar e usar **um** destino efetivo; o 00 não exige redirect literal específico. Não exigir assertRedirect em EditCupom. Sem esperar segundos. O oráculo principal é a unidade **visível**, não apenas texto escondido no DOM.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-61 | Select não comunica mudança reativa e conserva indicação antiga | CT-B01 | porcentagem→fixo indica centavos visíveis; fixo→porcentagem indica pontos percentuais |
| M-63 | O campo mantém max=100 depois de mudar para fixo | CT-B01 | fluxo fixo/1000 grava NOVO com valor 1000 |

---

## CT-B02: A recusa de percentual é visível e o formulário permite correção

**Origem**: RQ-01, RQ-03 e P-05. **Regra** R17.
**Por que browser e não Livewire**: CT-08/09 já provam validação e persistência; este caso prova que o navegador **mostra** a recusa, mantém um destino de correção utilizável e consegue retirar o estado de erro após a correção. Componente verde com erro oculto não prova essa saída.

```gherkin
# language: pt
Funcionalidade: Correção do cadastro de cupons
  Regra: Uma recusa visível não encerra a possibilidade de cadastro

    Cenário: [CT-B02] o erro de 101 por cento tem uma saída utilizável
      Dado a administradora da Acme na criação de NOVO com tipo porcentagem e os demais atributos válidos
      Quando a administradora percorre o ciclo de envio com valor 101 seguido de correção para 100
      Então na recusa há erro de valor visível junto ao campo e nenhum NOVO persistido
      E depois da correção existe exatamente um NOVO da Acme com tipo porcentagem e valor 100 sem erro de valor visível
```

Um único comportamento especificado: ciclo recusa→correção; o roteiro observa o estado intermediário **antes** da segunda submissão. Não usar somente o registro final como prova do erro visível.

### Roteiro executável

| # | Ação | Código Pest / conferência | Resultado observável |
|---|---|---|---|
| 1 | autenticar/contextualizar e abrir formulário | `actingAs` antes de `visit`, `assertPathIs` primeiro | criação Acme |
| 2 | enviar percentual 101 com demais atributos válidos | `select($tipoId, 'porcentagem')->fill($valorId, '101')->press($submit)` | recusa no formulário |
| 3 | observar a recusa antes de corrigir | `assertVisible($erroValor)`; conferir associação ao campo e `assertPathIs` se houve navegação | erro visível de valor, não apenas console |
| 4 | verificar não-efeito intermediário | consulta por NOVO no contexto Acme | zero NOVO e zero linhas novas de cupom_usos |
| 5 | corrigir o valor usando o mesmo formulário alcançável | `fill($valorId, '100')->press($submit)` | nova submissão utilizável |
| 6 | esperar destino e conferir estado final | `assertPathIs($destino)` primeiro se navega; ausência visível do erro do campo | exatamente um NOVO porcentagem/100 na Acme |
| 7 | conferir apoio | `assertNoJavaScriptErrors()` | não substitui erro/correção/persistência |

É proibido navegar manualmente para outra criação para “consertar” o fluxo: isso deixa a saída do estado de erro sem prova. O valor 101 é a única partição inválida; validade, código e limite são válidos. A frase literal da mensagem não é oráculo. Recusa não consome contador nem cria cupom_usos.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M-62 | Erro existe apenas no servidor ou permanece bloqueando o formulário depois da correção | CT-B02 | erro intermediário é visível; formulário corrigido grava NOVO porcentagem/100 e remove erro |

## Roteiro de Validação: Desenhado × Implementado

| # | Superfície de UI do 01 | Especificação vinculada | Implementado / confere? | Evidência |
|---|---|---|---|---|
| 1 | CuponsTable/listagem | CT-22–24/46 em componente | não verificado | sem implementação/execução |
| 2 | CupomForm/criar | CT-01/02/05/08/11 + CT-B01/02 | não verificado | sem implementação/execução |
| 3 | CupomForm/editar | CT-01/03/06/09/12 em componente; reatividade de criação não prova edição | não verificado; reatividade da edição é candidata a revisão | sem implementação/execução |
| 4 | DeleteAction/modal | CT-04/14/18/40 em componente | não verificado | sem implementação/execução |

## Revisão e limites

Revisão independente pendente, sem autorrevisão. Seletores, build, browsers, comportamento executado e materialização Pest ainda não conferidos. Cor/tema/acessibilidade não foram acrescentados porque o 00 não estabelece aceites para eles. Nenhum screenshot ou console foi tratado como prova de domínio.

