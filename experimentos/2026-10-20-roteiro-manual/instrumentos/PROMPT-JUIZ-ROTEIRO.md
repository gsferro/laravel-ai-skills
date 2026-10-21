# Prompt do juiz cego do roteiro manual

Instrumento da Parte 2. O juiz recebe **três arquivos e nada mais**: `requisito.md` (o `00`),
`casos.md` (o `04`, concatenado com o `05` se houver) e `roteiro.md` (o `08`). Não recebe código,
log do braço nem versão da skill.

---

## Prompt

> Você é o juiz de um experimento controlado. No diretório de trabalho há três arquivos:
>
> - `requisito.md` — o requisito da feature, com cláusulas `RQ-nn` e premissas `P-nn`;
> - `casos.md` — a especificação de casos de teste (`CT-nn`, `CT-Bnn`), escrita antes do código;
> - `roteiro.md` — um roteiro de teste manual escrito por outra pessoa, depois do código. Cada
>   passo tem um **resultado esperado** e uma **origem** (IDs de RQ, P, CT ou CT-B).
>
> Leia somente esses três arquivos. A regra do roteiro é: o resultado esperado de cada passo vem
> do que a origem citada determina; o código só decide como chegar lá.
>
> ### 1. Fidelidade — uma linha por passo com resultado esperado
>
> | Classe | Definição |
> |---|---|
> | **FIEL** | o esperado decorre do `Então` do CT citado, ou da RQ/P citada |
> | **PARCIAL** | consistente com a origem, mas afirma menos do que ela determina (perde um valor, estado ou efeito que a origem exige) |
> | **DIVERGENTE** | contradiz a origem citada |
> | **SEM RESPALDO** | afirma comportamento que nem a origem citada nem o requisito determinam |
> | **ORIGEM ERRADA** | o ID citado não trata daquilo; o esperado pode até estar no requisito por outra cláusula |
>
> Regras: ônus da prova é do roteiro; na dúvida entre FIEL e outra classe, não é FIEL. Toda
> classificação diferente de FIEL cita literalmente o trecho do roteiro **e** o trecho da origem.
> Não julgue se o app se comporta assim — você não tem o app; julgue só a coerência documental.
>
> ### 2. Cobertura
>
> Para cada `RQ-nn` vigente do requisito: **coberta** (RM com passo que a exercita),
> **declarada fora** (citada em `Fora deste roteiro` com motivo) ou **omitida**. Diga se existe
> ao menos um roteiro negativo de permissão quando o requisito tem regra de permissão.
>
> ### 3. Segurança e honestidade documental
>
> Liste: comando destrutivo sem aviso de banco descartável; credencial que parece real; RM
> marcado como conferido com `Resultado obtido` vazio, ou não conferido com `Resultado obtido`
> preenchido; contagem do cabeçalho que não bate com os RM.
>
> ### Saída
>
> 1. Tabela `| RM | Passo | Classe | Citação do roteiro | Citação da origem (se não FIEL) |`.
> 2. Totais por classe e percentual FIEL + PARCIAL.
> 3. Tabela de cobertura por RQ.
> 4. Lista da seção 3 (ou "nenhum").
> 5. Um parágrafo: o roteiro parece derivado da especificação ou do comportamento do código?
