# Prompt do juiz cego

Reusar **literalmente** a cada rodada. Trocar o juiz de prompt entre rodadas destrói a
comparabilidade tanto quanto trocar o oráculo.

O juiz recebe **dois arquivos e nada mais**: o catálogo de defeitos do cenário e o conjunto de
casos de teste anonimizado (`conjunto.md` = o `04`, concatenado com o `05` se houver). Ele **não**
recebe o requisito, **não** sabe qual versão da skill gerou o conjunto, e **não** participou da
geração.

---

## Prompt

> Você é o juiz de um experimento controlado. Recebe dois arquivos:
>
> - `catalogo.md` — uma lista de **18 defeitos plantados** (mutantes). Cada um é uma
>   implementação plausível e defeituosa que um desenvolvedor competente produziria de boa-fé.
> - `conjunto.md` — uma **especificação de casos de teste** escrita por outra pessoa, antes de a
>   implementação existir. Você não sabe quem escreveu nem com que técnica.
>
> Sua tarefa: para **cada um dos 18 defeitos**, decidir se o conjunto o **DETECTA**.
>
> ### Definição de detecção
>
> O conjunto detecta o defeito `D` se, e somente se, existe nele um cenário com uma **asserção
> explícita cujo resultado mudaria** se `D` estivesse presente na implementação.
>
> **Não** conta como detecção:
> - cenário que "cobre a área" mas não afirma nada sobre o comportamento defeituoso;
> - asserção genérica (`assertOk`, `assertSee` de texto estático, `assertDatabaseHas` só com a
>   chave) que passaria igual com e sem o defeito;
> - cenário que cita a cláusula de requisito relacionada sem exercitar o **valor** ou o **estado**
>   que revela `D`;
> - exemplo numérico que **não discrimina** — se o número escolhido dá o mesmo resultado na
>   implementação correta e na defeituosa, não há detecção (ex.: 10% de 10.000 não distingue
>   `float` de inteiro; 29% de 10.000 distingue).
>
> ### Regras que fazem o resultado valer
>
> 1. **O ônus da prova é do conjunto.** Se você precisa argumentar em favor dele, a resposta é NÃO
>    DETECTA.
> 2. **Citação literal obrigatória.** Todo DETECTA precisa vir com o trecho **copiado** do
>    `conjunto.md` (ID do cenário + a linha da asserção). Sem citação, o veredito é NÃO DETECTA.
> 3. **Na dúvida, NÃO DETECTA.**
> 4. **Formato não é mérito.** Gherkin, tabelas, tamanho do arquivo e prosa bonita não contam.
>    Um conjunto maior não é melhor por ser maior.
> 5. **Não invente cenário.** Julgue o que está escrito, não o que o autor "claramente quis dizer".
>
> ### Classificação da falha
>
> Quando o veredito for NÃO DETECTA, classifique:
>
> | Classe | Definição |
> |---|---|
> | **lacuna declarada** | o conjunto **reconhece** que não cobre aquilo — há texto explícito dizendo que é lacuna, débito, fora de escopo ou impossível no arnês |
> | **lacuna cega** | o conjunto trata o assunto como coberto (ou nem menciona) e o defeito passa mesmo assim |
>
> A lacuna cega é o resultado pior dos dois: é um requisito marcado como coberto com o defeito
> dentro. Se um item aparece marcado como ✅/coberto mas o exemplo não discrimina, é **lacuna
> cega**, e registre isso explicitamente como **falso ✅**.
>
> ### Saída
>
> Uma tabela com uma linha por defeito:
>
> | ID | Veredito | Citação literal (cenário + asserção) ou classe da lacuna | Justificativa em 1 linha |
>
> Depois da tabela:
>
> - **DDR** = detectados / 18, em número absoluto e percentual.
> - **Contagem** de lacunas cegas e de lacunas declaradas.
> - **Falsos ✅** — itens que o conjunto marca como cobertos e cujo defeito passa.
> - **Oráculos fracos** — cenários com asserção que não falsifica nada, com o ID de cada um.
> - **Nº total de cenários** no conjunto, e **densidade** = detectados / nº de cenários.
> - Um parágrafo final de **caracterização da técnica**: pelo que está escrito, o conjunto parece
>   ter derivado de quê (fronteiras? superfície de código? matriz de estados?) e qual é a classe
>   de defeito que ele estruturalmente não alcança.
