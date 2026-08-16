# Casos de Teste de Browser — FERRO-812: Cupons de desconto

> Gerado pela skill `feature-test-design` v1.9.0.
> Browser só para o que depende de JavaScript, pixel ou acessibilidade.

## Gate de browser

A feature tem 4 telas/componentes com `Depende de JS? = Sim` no `01-plano-acao.md`:
- `CuponsTable` (listagem)
- `CupomForm` (criar)
- `CupomForm` (editar)
- `DeleteAction` na linha

Além disso, o campo `valor` muda de rótulo/sufixo conforme o `Select` de tipo — comportamento que só o navegador prova (HTML inicial é idêntico).

## Cenários

```gherkin
@CT-B01 @browser
Cenário: admin cria cupom e vê na listagem
  Dado um admin_organizacao autenticado no navegador no painel /app
  Quando ele navega para "/app/cupons/create"
    E preenche "Código" com "PROMO10"
    E seleciona "Tipo" = "Porcentagem"
    E preenche "Percentual de desconto" com "10"
    E preenche "Válido até" com "2030-01-01 12:00"
    E preenche "Limite de usos" com "100"
    E salva
  Então o navegador volta para "/app/cupons"
    E a lista contém 1 registro
    E a coluna "Código" mostra "PROMO10"
    E a coluna "Desconto" mostra "10%"
    E a coluna "Situação" mostra "Ativo"
```

```gherkin
@CT-B02 @browser
Cenário: alterar o tipo atualiza o rótulo do campo valor
  Dado um admin_organizacao autenticado no navegador
  Quando ele navega para "/app/cupons/create"
    E seleciona "Tipo" = "Valor fixo"
  Então o rótulo do campo de valor exibe "Valor do desconto (centavos)"
  Quando ele seleciona "Tipo" = "Porcentagem"
  Então o rótulo do campo de valor exibe "Percentual de desconto"
```

> Detecta inconsistência de UI: rótulo "R$" com valor em porcentagem (mutante da tela mentindo).

```gherkin
@CT-B03 @browser
Cenário: panel_user só vê cupons ativos na listagem
  Dado um admin_organizacao que cadastrou os cupons:
    | Código  | Tipo         | Valor | Válido até          | Limite | Usos |
    | ATIVO   | Porcentagem  | 10    | 2030-01-01 12:00:00 | 10     | 0    |
    | VENCIDO | Porcentagem  | 10    | 2020-01-01 12:00:00 | 10     | 0    |
    | CHEIO   | Porcentagem  | 10    | 2030-01-01 12:00:00 | 10     | 10   |
  Quando um panel_user autenticado no navegador navega para "/app/cupons"
  Então a lista contém 1 registro
    E a coluna "Código" mostra "ATIVO"
    E as colunas não mostram "VENCIDO" nem "CHEIO"
```

> Detecta D10 (usuário comum enxerga cupons expirados/inativos) na superfície real.

```gherkin
@CT-B04 @browser
Cenário: panel_user não vê botão de criar/editar/excluir
  Dado um panel_user autenticado no navegador
  Quando ele navega para "/app/cupons"
  Então o botão "Novo cupom" não está presente
    E nenhuma linha da tabela mostra ações "Editar" ou "Excluir"
```

> Detecta D09 na camada de UI (affordance de escrita sumida).

---

## Roteiro Desenhado × Implementado

| Tela | O que o usuário vê | Status | Divergência |
|---|---|---|---|
| Listagem (admin) | todos os cupons com código, tipo, desconto, usos, validade, situação | ☐ | — |
| Listagem (panel_user) | só cupons ativos | ☐ | — |
| Form create/edit | campo `valor` atualiza rótulo com `tipo` | ☐ | — |
| DeleteAction | modal de confirmação | ☐ | — |
