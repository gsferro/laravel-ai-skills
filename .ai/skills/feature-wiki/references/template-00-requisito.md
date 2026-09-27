> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de escrever o `00-requisito.md`) e ao registrar um Adendo (pedido novo durante a implementação ou achado confirmado do step 6.5). Fonte única de: template do `00-requisito.md` e do `## Adendo N`.

# Template do `00-requisito.md`

Os regimes das seções (Texto Original e Adendo imutáveis, Decomposição revisável), o que é
obrigatório incluir e o procedimento do Adendo ficam no corpo do `SKILL.md`, seção *Arquivo 00*.

**Template `00-requisito.md`**:
```markdown
# Requisito — {Card}: {Título}

## Fonte

- **Origem**: {card FERRO-579 colado no chat | docs/requisitos/RF-231.pdf, p. 3-4 | conversa com {quem}}
- **Data**: {YYYY-MM-DD}
- **Autor / solicitante**: {nome ou área}
- **Fidelidade**: alta (texto escrito) | **baixa** (descrição verbal — confirmar antes de implementar)

## Texto Original

<!-- IMUTÁVEL. Não editar, não corrigir ortografia, não resumir, não reordenar. -->

> {texto colado verbatim, ou trechos literais citados da fonte}

## Decomposição em Cláusulas

| ID | Cláusula | Trecho literal de origem | Tipo |
|----|----------|--------------------------|------|
| RQ-01 | {o que deve acontecer, em uma frase} | "{citação literal}" | funcional |
| RQ-02 | {…} | "{…}" | autorização |
| RQ-03 | {…} | "{…}" | não-funcional |

## Ambiguidades e Perguntas Abertas

<!-- Cláusula que não dá para testar como está. Perguntar ANTES de implementar.
     Perguntas OBRIGATÓRIAS quando o requisito tem papéis, visibilidade, notificação ou texto livre
     (as quatro que o juiz cego fez em 2026-09-21 e a sessão não fez):
     1. Acumulação de papéis, PAR A PAR: quem é X pode também ser Y? (solicitante × aprovador,
        aprovador × aprovador de outra etapa). Uma pergunta por par, não uma genérica
     2. Recorte de visibilidade: quem VÊ agora × quem JÁ PARTICIPOU. O participante histórico
        continua vendo? O que vê quem perdeu a corrida?
     3. Toda notificação tem link: para ONDE leva, e o destino ainda existe e está visível para o
        destinatário quando ele clica?
     4. Todo texto livre tem teto — no model, não só no formulário? -->

- **RQ-03**: "{precisa ser rápido}" — sem número não é testável. Qual SLA?
- **RQ-05**: conflita com RQ-02 — {descrever o conflito}

## Fora de Escopo (declarado)

<!-- O que o requisito explicitamente NÃO pede, para o quality gate não acusar omissão indevida. -->

- {item explicitamente fora}
```

## Template do Adendo

**Template**:

```markdown
## Adendo 1 — 2026-09-05

- **Fonte**: pedido do solicitante no chat, durante a implementação do passo 9
- **Fidelidade**: alta (texto escrito)

### Texto Original

<!-- IMUTÁVEL, mesmo regime do Texto Original acima. -->

> {texto verbatim do pedido novo}

### Decomposição

| ID | Cláusula | Trecho literal | Tipo | Substitui |
|----|----------|----------------|------|-----------|
| RQ-09 | {…} | "{…}" | funcional | — |
| RQ-10 | {…} | "{…}" | restrição | RQ-04 (parcial) |
```
