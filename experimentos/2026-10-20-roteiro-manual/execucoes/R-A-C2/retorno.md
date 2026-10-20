Entrega concluída: **24 regras, 75 CT e 2 CT-B**. Gate registra 99 mutantes previstos, um sem matador.

- Skills locais: `feature-wiki` **4.1.1**; `feature-test-design` **1.17.3**.
- Host: **Codex baseado em GPT-6**; variante/esforço não expostos.
- Perfis pelo passo 0, nenhum imposto: cadastro **padrão (6)**; apresentação **padrão (4)**; fluxo, autorização, concorrência e e-mails **completo (9)**. Há Impacto 3.
- Revisão independente obrigatória executada: **2 rodadas**, rota `fw-adversario-ct`, agentes `adversario_ct_1/2`, GPT-6 herdado, contexto novo.
- Rodada 1: **10 achados**; ADV-01/02/09 geraram CT-73/74/75; sete geraram oráculos reescritos.
- Rodada 2: **5 achados**, todos fechados por reescrita. Fechamentos finais sem terceira revisão, conforme teto.
- `02` **ausente**; inventário Livewire incompleto declarado. `00/01` preservados por SHA-256; nenhum `03` criado.
- Degradações: Boost indisponível, vendor vazio e pasta sem Git. Sem execução Pest/mutate. Warning de A-10 preservado por precedência da instrução.
- Checagens estruturais passaram: IDs únicos, índice completo e matriz com **40 células**.

Referências abertas, em `references/` das respectivas skills:

- **feature-wiki:** `hosts-e-subagentes.md`, `delegacao-casos-de-teste.md`, `ponytail-caveman.md`, `roteamento-e-despacho.md`, `citacoes-de-codigo.md`, `template-03-progresso.md`.
- **feature-test-design:** `template-04.md`, `escolha-de-camada.md`, `tecnicas-por-regra.md`, `taxonomia-de-defeito.md`, `gherkin.md`, `armadilhas-de-api.md`, `mutation-testing.md`, `revisao-adversarial.md`, `pest-plugin-browser.md`, `template-05.md`.

Arquivos escritos:

- [04-casos-de-teste.md](D:/PROJECTS/SKILLS/blind-20261020/proj-5f7c81/wikis/specs/saida-c2/aprovacao-de-compra/04-casos-de-teste.md)
- [05-casos-de-teste-browser.md](D:/PROJECTS/SKILLS/blind-20261020/proj-5f7c81/wikis/specs/saida-c2/aprovacao-de-compra/05-casos-de-teste-browser.md)