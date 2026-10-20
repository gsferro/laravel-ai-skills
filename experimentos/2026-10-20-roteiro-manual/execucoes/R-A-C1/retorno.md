Escrito: [04-casos-de-teste.md](D:/PROJECTS/SKILLS/blind-20261020/proj-a6856d/wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md).

- Skills: `feature-wiki` **4.1.1**; `feature-test-design` **1.17.3**.
- Host: Codex/API, Windows. Família informada: GPT-6; identificador exato não exposto.
- Perfis decididos pelo passo 0: cadastro, autorização/isolamento, cálculo e consumo/auditoria **completo — 9**; interface **padrão — 4**. As quatro primeiras têm Impacto 3.
- Entrega: **18 regras, 58 cenários, 83 mutantes previstos, 1 sem matador; 0 CT-B**. Gate dispensou o `05`.
- Revisão adversarial obrigatória executada: **duas rodadas, 3 + 3 achados**. Rota `fw-adversario-ct` via `spawn_agent`, contexto novo, modelo herdado.
- Fechamento: **três achados viraram cenários novos; três reforçaram oráculos**. Destinos individuais registrados no arquivo.
- Teto atingido: CT-57/58 e últimos reforços não receberam terceira revisão.
- `02` ausente. Lacunas de superfície, requisitos e idempotência declaradas. `vendor` e Boost indisponíveis; Pest/mutate não executados.
- Nenhum `03` criado. Somente o `04` foi escrito; hashes dos insumos permaneceram iguais.

Referências abertas em `.ai/skills/feature-wiki/references/`:
`hosts-e-subagentes.md`, `ponytail-caveman.md`, `delegacao-casos-de-teste.md`, `template-03-progresso.md`, `citacoes-de-codigo.md`, `roteamento-e-despacho.md`.

Referências abertas em `.ai/skills/feature-test-design/references/`:
`template-04.md`, `escolha-de-camada.md`, `tecnicas-por-regra.md`, `taxonomia-de-defeito.md`, `gherkin.md`, `armadilhas-de-api.md`, `mutation-testing.md`, `revisao-adversarial.md`.