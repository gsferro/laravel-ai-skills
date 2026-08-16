# Casos de Teste de Browser — FERRO-830: Fluxo de aprovação de solicitação de compra

> Gerado pela skill `feature-test-design` v1.9.0.
> Browser só para o que depende de JavaScript, pixel ou acessibilidade.

## Gate de browser

A feature tem 6 telas/componentes com `Depende de JS? = Sim` no `01-plano-acao.md`:
- `SolicitacoesCompraTable` (listagem)
- `SolicitacaoCompraForm` (create/edit)
- `ViewSolicitacaoCompra` (infolist)
- Modal "Rejeitar"
- Modais "Enviar" / "Cancelar"
- `CentrosCustoTable` + form

O fluxo atravessa ≥ 2 telas e ≥ 2 personas (solicitante → gestor → diretor).

## Cenários

```gherkin
@CT-B01 @browser
Cenário: solicitante cria e envia, gestor aprova, diretor aprova
  Dado "Ana" autenticada no navegador como panel_user
    E o centro "TI" com gestor "Rui" e diretor "Dora"
  Quando ela navega para "/app/solicitacoes-de-compra/create"
    E preenche "Descrição" com "Notebook"
    E preenche "Valor" com "R$ 6.000,00"
    E seleciona "Centro de custo" = "TI"
    E salva
  Então ela vê a solicitação em "rascunho" na listagem
    E o botão "Enviar" está visível
  Quando ela clica em "Enviar" e confirma
  Então a situação muda para "Aguardando gestor"
    E o botão "Enviar" some
  Quando "Rui" acessa a mesma URL
  Então ele vê o botão "Aprovar"
  Quando ele aprova e confirma
  Então a situação muda para "Aguardando diretor"
  Quando "Dora" acessa a mesma URL
  Então ela vê o botão "Aprovar"
  Quando ela aprova e confirma
  Então a situação muda para "Aprovada"
    E a tela de visualização mostra o histórico com as etapas de Rui e Dora
```

> Detecta E16 (tela mostra "Aprovada" enquanto falta diretor), E04, E07, E08.

```gherkin
@CT-B02 @browser
Cenário: rejeição exibe modal com justificativa obrigatória
  Dado uma solicitação de R$ 3.000,00 em "aguardando_gestor"
    E o gestor "Rui" autenticado
  Quando ele abre a solicitação e clica em "Rejeitar"
  Então o modal pede "Motivo da rejeição"
  Quando ele confirma sem preencher
  Então o modal mostra erro "O campo é obrigatório"
  Quando ele preenche "Sem verba" e confirma
  Então a solicitação volta para "rascunho"
    E o solicitante vê o motivo ao visualizar
```

> Detecta E05 (justificativa obrigatória) na superfície de UI.

```gherkin
@CT-B03 @browser
Cenário: solicitante não enxerga botões de aprovação
  Dado uma solicitação de R$ 3.000,00 em "aguardando_gestor"
    E a solicitante "Ana" autenticada
  Quando ela abre a solicitação
  Então os botões "Aprovar" e "Rejeitar" não estão presentes
    E o botão "Cancelar" está presente
```

> Detecta E08 (solicitante aprova própria solicitação) na camada de affordance.

```gherkin
@CT-B04 @browser
Cenário: aprovada fica inalterada para todos
  Dado uma solicitação "aprovada"
    E "Ana" autenticada
  Quando ela abre a solicitação
  Então os botões "Editar", "Excluir", "Enviar", "Cancelar", "Aprovar" e "Rejeitar" não estão presentes
    E o badge "Aprovada" está visível
    E a seção "Histórico de aprovação" mostra quem aprovou
```

> Detecta E01, E02, E09, E14, E16 na camada de UI.

```gherkin
@CT-B05 @browser
Cenário: tela de visualização mostra quem aprovou cada etapa
  Dado uma solicitação de R$ 6.000,00 aprovada por Rui e Dora
  Quando qualquer usuário autorizado abre a visualização
  Então a seção "Histórico de aprovação" exibe:
    | Etapa   | Decidido por | Decisão   | Justificativa |
    | gestor  | Rui          | aprovada  | —             |
    | diretor | Dora         | aprovada  | —             |
```

> Detecta E13 (histórico não gravado) e E16 (estado exibido inconsistente).

---

## Roteiro Desenhado × Implementado

| Tela | O que o usuário vê | Status | Divergência |
|---|---|---|---|
| Listagem solicitante | solicitações com descrição, valor, centro, status | ☐ | — |
| Listagem gestor | botão Aprovar/Rejeitar nas suas | ☐ | — |
| Listagem diretor | botão Aprovar/Rejeitar quando pendente diretor | ☐ | — |
| Form create/edit | descrição, valor (R$), centro de custo | ☐ | — |
| View | situação + histórico de etapas | ☐ | — |
| Modal rejeitar | justificativa obrigatória | ☐ | — |
