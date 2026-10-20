Entregues **19 regras, 69 CT, 1 CT-B e 106 mutantes previstos**.

- Skills: `feature-wiki` **4.2.0**; `feature-test-design` **1.17.4**.
- Host: **Codex**; família **GPT-6**. Modelo exato/esforço não expostos.
- Perfis decididos pelo passo 0, sem imposição:
  - **Completo, 3×3=9:** Fluxo, Autorização e Efeitos.
  - **Padrão:** Cadastro, 2×3=6; Apresentação e Interface, 2×2=4.
  - Impacto 3: Cadastro, Fluxo, Autorização e Efeitos.
- Revisão obrigatória executada em contextos novos, rota `adversário-ct`, modelo herdado: `adversario_ct_1` e `adversario_ct_2`.
- Rodada 1: **15 achados**; 5 cenários novos e 10 oráculos revistos.
- Rodada 2: **7 achados**; 2 cenários novos e 5 oráculos revistos.
- Todos receberam fechamento individual no 04. CT-68/69 permanecem sem terceira revisão pelo teto de duas rodadas; sinais estruturais registrados.
- `02` **ausente**; não criado. `00`/`01` preservados; `03` não criado.
- Degradações: Boost/vendor ausentes, diretório sem repositório Git, mutate apenas transitivo e runtime não executado. Perguntas e lacunas declaradas.
- Validação estrutural passou; **244 arquivos protegidos mantiveram seus hashes**.

References abertas, sob `.ai/skills/`:

- `feature-wiki/references/`: `hosts-e-subagentes.md`, `delegacao-casos-de-teste.md`, `ponytail-caveman.md`, `roteamento-e-despacho.md`, `citacoes-de-codigo.md`.
- `feature-test-design/references/`: `template-04.md`, `escolha-de-camada.md`, `tecnicas-por-regra.md`, `taxonomia-de-defeito.md`, `gherkin.md`, `armadilhas-de-api.md`, `mutation-testing.md`, `revisao-adversarial.md`, `pest-plugin-browser.md`, `template-05.md`.

Arquivos escritos somente na saída solicitada:

- [04-casos-de-teste.md](D:/PROJECTS/SKILLS/blind-20261020/proj-641a92/wikis/specs/saida-c2/aprovacao-de-compra/04-casos-de-teste.md)
- [05-casos-de-teste-browser.md](D:/PROJECTS/SKILLS/blind-20261020/proj-641a92/wikis/specs/saida-c2/aprovacao-de-compra/05-casos-de-teste-browser.md)