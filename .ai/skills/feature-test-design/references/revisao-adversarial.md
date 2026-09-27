> Referência da feature-test-design 1.15.0. Lida em: revisão adversarial (ao montar o despacho do
> sub-agente — o que entra, o que não entra, as oito tarefas). Fonte única de: o resumo do contrato
> adversarial; a fonte do contrato em si é `agents/fw-adversario-ct.md`.

# Revisão adversarial — resumo do contrato

Disparo, rota, dono do fechamento, host sem sub-agente e o que fazer com os achados estão no
`SKILL.md` §Revisão Adversarial.

O contrato completo e a fonte da verdade é `agents/fw-adversario-ct.md`;
o resumo abaixo não o substitui:

```text
Entrada: 00-requisito.md + 04-casos-de-teste.md (e 05, se houver)
NÃO receber: o PRD, o código, nem o raciocínio de quem derivou

Tarefa: PROVAR que este conjunto deixa passar um defeito.
  1. Escreva 5 implementações erradas plausíveis que passariam por TODOS os cenários
  2. Para cada uma, aponte a regra afetada e a técnica de derivação que faltou
  3. Aponte todo cenário cujo "Então" é fraco — isto é, que passaria com a
     implementação defeituosa (assertOk sozinho, assertSee de layout,
     assertDatabaseHas só com a chave, ausência de assertion sobre o valor)
  4. Aponte todo cenário sem nenhum "Então" e todo cenário com mais de um "Quando"
  5. Para cada PAR de papéis do requisito, pergunte: o conjunto tem cenário em que a mesma
     pessoa acumula os dois? (solicitante × aprovador; aprovador da etapa 1 × aprovador da
     etapa 2). Par sem cenário é lacuna
  6. Para cada recorte de visibilidade, pergunte: quem JÁ PARTICIPOU continua vendo? e o link
     de toda notificação leva a um destino que o destinatário ainda vê?
  7. Para cada texto livre do requisito, pergunte: há cenário no teto (n, n+1) — no model, não
     só no formulário?
  8. Aponte toda RQ do 00 sem cenário que a discrimine

Saída: lista de lacunas, cada uma com a regra, a técnica faltante e o cenário sugerido,
       + a lista de áreas/regras percorridas (a revisão cobre o conjunto inteiro, não só
       a área que a disparou — achado em outra área é achado válido)
PROIBIDO: elogiar o conjunto, reescrever os cenários, dizer "está bom".
```

## Não autorrevisar — por quê (regra: Proibição 9)

> **Não autorrevisar.** Modelos de linguagem são comprovadamente melhores em **gerar** oráculos
> do que em **classificar** se um oráculo está correto — o mesmo agente conferindo o próprio
> conjunto reproduz o viés que o gerou.
