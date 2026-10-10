# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Runtime: pest-plugin-browser 5.0.1 / Playwright. O plugin sobe o próprio servidor in-process.
> Costura: `browser`, grupo **Unidade e reação no navegador**, confirmada no 04.
> Derivado de RQ-01/03/04, P-05/09; o plano fornece somente rotas, campos e a interação de trocar tipo.
> Revisão adversarial: rodada 1 executada junto ao 04, sem achado específico nos dois CT-B; rodada 2 PENDENTE pelos três CT novos no 04. Nenhum CT-B foi implementado ou executado nesta entrega.
> Arquivo futuro: `tests/BrowserTenancy/CupomTest.php`.
> Comando posterior: `vendor/bin/pest --testsuite=Browser --filter=Cupom` — **em série**, rule local `.ai/rules/testes-browser.md`.

## Gate e limite

O 05 existe porque o navegador deve executar a troca do Select e receber a atualização da unidade no DOM **sem recarregar a página**. Uma assertion no estado PHP do componente não prova que o cliente executou essa reação. Duas telas da Superfície de UI do 01, create e edit, recebem o observable de JS. Validação, gravação, listagem, permissão e ações permanecem no 04; este arquivo não duplica sua matriz.

Perfil completo da área de interação JavaScript: 1 happy path e 1 erro visível, sem estouro. Os textos exatos do rótulo, do erro e do botão não são novos critérios do 01; o oráculo é a **unidade coerente com P-05**, erro de valor visível e registro concreto. Não há critério de cor, tema, pixel ou acessibilidade inventado.

## Pré-requisitos e setup

- [ ] Na materialização, executar `npm run build`; manifest existente foi observado, mas build não foi executado nesta cópia.
- [x] `.gitignore` inclui `/tests/Browser/Screenshots` — `rg -n 'Screenshots' .gitignore`, linha 27, 2026-10-09.
- [x] Suíte Browser confirmada — `rg -n '<testsuite name="Browser"' phpunit.xml`, linha 32, 2026-10-09.
- [x] Arnês BrowserTenancy e timeout 20.000 ms lidos no tests/Pest.php, 2026-10-09.
- [ ] Na execução, criar Acme, Ana admin_organizacao e seu vínculo/team real; semear permissões pelo padrão existente, na ordem ShieldPermissionsSeeder → PapeisSeeder.
- [ ] `$this->actingAs($ana)` **antes** de visit; `noPainelDa($acme)`/fronteiraDeRequest conforme troca de contexto. Não fazer login pelo formulário.
- Relógio fixado em `2026-10-09T12:00:00Z`, validade futura `2026-10-10T18:00:00Z`, limite 3.
- Não criar servidor, ajustar APP_URL ou usar wait de segundos. Assertions esperam o estado até o teto.
- Uma navegação exige assertPathIs antes de conteúdo. O 01 diz retorno à lista; o vendor padrão permite redirecionar à edição. O destino exato não é comportamento do requisito: antes de materializar, resolver o destino configurado do projeto e usar seu path próprio como espera técnica. Não forçar volta à lista se o fluxo confirmado usa edição.
- Seletores abaixo são propostas a confirmar quando o Resource existir. Nenhuma página de Cupom foi lida. APIs assertScript, assertValue, assertVisible, select, fill e assertPathIs foram conferidas no vendor instalado; não usar waitForText/waitForSelector inventados.

## Seletores

| Elemento | Seletor proposto | Evidência/limite |
|---|---|---|
| Código | `#data\.codigo` | CreateRecord/EditRecord usam statePath('data'); confirmar ID do Resource futuro |
| Tipo | `#data\.tipo` ou label/combobox acessível do mesmo campo | Select é native por default no vendor; se a UI optar por Select custom, usar seu locator acessível real |
| Valor | `#data\.valor` | ID previsto pela state path; preferir label associado se estável |
| Unidade do valor | `label[for="data.valor"]` no wrapper do campo | Verificar que o texto da unidade está visível, não só no DOM |
| Validade | `#data\.expira_em` | Valor date/datetime-native e ID serão confirmados; não impor formato de texto do 01 |
| Limite | `#data\.limite_de_usos` | Campo de contagem, demais dados válidos |
| Erro do valor | `[data-field-wrapper]:has(#data\.valor) [data-validation-error]` | Atributos data-field-wrapper/data-validation-error conferidos na view field-wrapper do Filament; ID pendente |
| Botões criar/salvar | texto/role traduzido real | Confirmar texto; a mensagem exata não é oráculo |

Não acrescentar data-testid nesta rodada. O executante confirma o selector final e registra a mudança de mecanismo, sem alterar o resultado esperado. O erro precisa pertencer ao wrapper do valor; um aviso qualquer da página não serve.

## CT-B01: A criação atualiza a unidade do tipo sem recarregar

**Por que browser:** executa a mudança do Select e verifica o label **visível** atualizado pelo cliente antes da gravação, além de uma âncora de persistência. `fillForm` no servidor poderia passar com o cliente preso no texto inicial.

```gherkin
# language: pt
Funcionalidade: Operação do campo de desconto
  Regra: A unidade exibida acompanha o tipo que a pessoa está configurando
    Cenário: [CT-B01] O administrador vê centavos ao criar um cupom fixo
      Dado Ana administradora da Acme, formulário create carregado com tipo porcentagem explicitamente selecionado e unidade percentual visível
      Quando Ana configura e grava um cupom NOVO de tipo fixo e valor 150 centavos, sem recarregar a página durante a troca de tipo
      Então antes de gravar o campo valor indica centavos de forma visível e não percentual, mantendo o valor digitável
      E existe exatamente um NOVO da Acme de tipo fixo, valor 150, validade futura, limite 3 e contador 0
```

**Roteiro executável após o Resource existir**

| # | Ação | API Pest/critério | Resultado |
|---|---|---|---|
| 1 | Autenticar e visitar create | `$this->actingAs($ana); visit('/app/acme/cupons/create')->assertPathIs('/app/acme/cupons/create')` | Formulário específico, cinco campos |
| 2 | Fixar a partição inicial | `->select($tipo, 'porcentagem')` e `assertScript` no label do valor | Label visível indica percentual, sem pressupor default do 01 |
| 3 | Trocar tipo no cliente | `->select($tipo, 'fixo')` | O navegador processa a atualização Livewire; nenhuma visita/reload intermediário |
| 4 | Aguardar unidade final | `->assertScript($unidadeVisivelEhCentavos, true)` | Label associado visível contém significado centavos, e não percentual |
| 5 | Gravar dados válidos | `->fill($codigo, 'NOVO')->fill($valor, '150')->fill($validade, $dataNativaFutura)->fill($limite, '3')->press($botaoCriar)` | Uma criação efetiva |
| 6 | Esperar navegação configurada | `->assertPathIs($destinoProprioConfirmado)` antes de conteúdo; `->assertNoJavaScriptErrors()` | Destino próprio sem erro de JS |
| 7 | Uma âncora persistida | DB: único NOVO com tenant Acme, tipo fixo, valor 150, validade do Dado, limite 3, usos 0 | O dado tem a unidade que a tela informou |

O script da unidade deve consultar o label associado ao elemento real, testar que possui retângulos de layout e não está com display:none/visibility:hidden, e comparar o significado da unidade. Não basta assertSee('centavos') no layout. Locators e `$destinoProprioConfirmado` são variáveis de mecanismo a fixar pela implementação real, não helpers inventados da API.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M47 | Select altera tipo no servidor, mas cliente continua com unidade percentual | CT-B01 | Antes do submit, label visível associado ao valor significa centavos sem reload; persistência NOVO fixo 150 |

## CT-B02: A edição troca unidade e mostra o erro da nova partição

**Por que browser:** confere a reação de JS na segunda tela e a apresentação do erro no campo correspondente depois de trocar o discriminador. A recusa de porcentagem 101 já está em CT-08/09; este cenário afirma que o cliente recebe e exibe a resposta, permanecendo operável.

```gherkin
# language: pt
Funcionalidade: Operação do campo de desconto
  Regra: A unidade exibida acompanha o tipo que a pessoa está configurando
    Cenário: [CT-B02] O administrador vê percentual e erro de valor após trocar um fixo na edição
      Dado Ana administradora da Acme, cupom ativo FIXO de valor 150 centavos com contador 1 e uma trilha, e edit carregado com unidade centavos visível
      Quando Ana troca o tipo para porcentagem e tenta salvar valor 101 sem recarregar a página durante a troca
      Então o valor passa a indicar percentual de forma visível e recebe um erro visível associado a esse campo, com o formulário ainda operável
      E a linha persistida continua fixo 150, contador 1 e a mesma trilha anterior, sem novo registro de aplicação
```

**Roteiro executável após o Resource existir**

| # | Ação | API Pest/critério | Resultado |
|---|---|---|---|
| 1 | Autenticar e visitar edit do UUID próprio | `visit('/app/acme/cupons/'.$cupom->uuid.'/edit')->assertPathIs($pathEdit)` | Registro FIXO de 150, unidade centavos visível |
| 2 | Trocar tipo real | `->select($tipo, 'porcentagem')` e `->assertScript($unidadeVisivelEhPercentual, true)` | Label muda sem reload e deixa de significar centavos |
| 3 | Enviar valor inválido isolado | `->fill($valor, '101')->press($botaoSalvar)` | Validade/limite/código continuam válidos; nenhum segundo erro mascara o valor |
| 4 | Esperar o estado final | `->assertPathIs($pathEdit)->assertVisible($erroDoValor)->assertScript($campoContinuaOperavel, true)` | Erro não vazio associado ao campo, input visível e habilitado |
| 5 | Console como apoio | `->assertNoJavaScriptErrors()` | Complementa o erro e o label; nunca oráculo único |
| 6 | Uma âncora de persistência | Linha FIXO continua tipo fixo, valor 150, validade/limite antigos, contador 1; comparar trilha anterior por ID/autor/instante | O submit recusado não mudou dados nem aplicação |

O erro visível deve estar no wrapper do valor e ter conteúdo não vazio. A condição operável testa campo/botão habilitados e visíveis; não introduz um segundo submit no Cenário. Se o erro terminar numa página HTTP de recusa, a operação divergiu do domínio esperado; CT-01/38 já especificam a saída para a lista própria.

#### Mutantes previstos

| # | Implementação errada plausível | Cenário que mata | Asserção que mata |
|---|---|---|---|
| M48 | Edit usa a unidade original depois de selecionar porcentagem | CT-B02 | Label visível passa a percentual antes do submit, sem reload |
| M49 | JS não apresenta validação retornada ou deixa input travado | CT-B02 | Erro visível não vazio no wrapper de valor, campo e ação operáveis; registro ainda fixo 150 |

## Roteiro de Validação: Desenhado × Implementado

| Linha da UI do 01 | O que cabe validar | Prova | Implementado / evidência |
|---|---|---|---|
| CuponsTable | Lista, busca, cardinalidade, ações e escopo | CT-33/35/38/39 no 04 | não executado; implementação fora desta rodada |
| CupomForm criar | Visita e gravação; unidade reativa no DOM | CT-01/02/07 e CT-B01 | não executado |
| CupomForm editar | Visita e gravação; troca de unidade e erro apresentado | CT-01/03/08 e CT-B02 | não executado |
| DeleteAction | Ação efetiva e autorização, não somente presença de modal | CT-31/33/34/35 no 04 | não executado; modal não ganhou requisito novo |

## Cogitado e cortado

| Candidato | Destino |
|---|---|
| CRUD inteiro por browser | Componentes CT-02/03/33; navegador não acrescentaria oráculo necessário para persistência |
| Busca, paginação, ativo/inativo em browser | CT-38/39 mais baratos |
| Autorização só pela ausência de botão no navegador | CT-31/32 exercitam ação; ausência visual não prova segurança |
| Abrir modal delete/cancelar como cenário extra | O card não determina animação/modal; ação de exclusão já CT-33, sem mutante de requisito adicional |
| Dark mode/acessibilidade/screenshots | Não há critério correspondente no requisito fixo; não ampliados nesta rodada |

## Estado

**Somente especificação.** Browser, selectors finais e persistência não foram executados. Não há medição de MSI, DDR, tokens ou equivalência entre hosts. Referências lidas para este arquivo: template-05.md e pest-plugin-browser.md, além das referências de Gherkin/API/camada já declaradas no retorno.

## Fechamento da revisão 1 e próxima rodada

A revisão independente `/root/adversarial_26_c1` percorreu CT-B01/02 e M47–M49 sem achado específico. Os sete achados e seus destinos estão no 04. A reação de JS, o erro visível e as âncoras de persistência continuam nos dois CT-B; código novo, validade preservada, papéis acumulados, leitura vedada e histórico de aplicação são provados mais barato no 04. Não foi acrescentado cenário de browser. O índice do 04 aponta o mesmo destino futuro deste arquivo, `tests/BrowserTenancy/CupomTest.php`. A rodada 2 segue pendente porque CT-43/44/45 são novos; ausência de achado de browser na rodada 1 não conclui essa próxima revisão.
