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

