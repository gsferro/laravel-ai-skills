Entregue: [04-casos-de-teste.md](D:/PROJECTS/SKILLS/blind-20261020/proj-05b17d/wikis/specs/saida-c1/cupons-de-desconto/04-casos-de-teste.md).

- Skills: `feature-wiki` **4.2.0**; `feature-test-design` **1.17.4**.
- Host: **Codex/Windows**. Modelo: **GPT-6**, variante exata não exposta.
- Perfis pelo passo 0, nenhum imposto: cadastro **completo (9)**; motor/auditoria **completo (9)**; autorização/isolamento **completo (9)**; interface **padrão (4)**. Três áreas com Impacto 3.
- Resultado: **16 regras, 55 CT, 72 mutantes previstos, 0 CT-B**.
- `05` rascunhado e retirado: o requisito não exige comportamento exclusivo de navegador.
- Revisão adversarial obrigatória executada em contexto novo: rota `fw-adversario-ct`, modelo herdado GPT-6.
- Duas rodadas: **9 + 3 achados**. Fechamentos: **5 cenários novos, 6 correções de oráculo/tabela, 1 lacuna declarada**. Detalhamento por achado no arquivo.
- Teto de duas rodadas respeitado; ajustes finais tiveram checagem documental, sem terceira revisão.
- `02` **ausente**. `03` não criado. `00`/`01` preservados, com hashes conferidos.
- Degradações: vendor/Boost indisponíveis; inventário Livewire incompleto; leitura do revisor limitada por contrato; controle de integridade parcial na segunda rodada.
- Pest/browser/mutação não executados. Validação documental passou: IDs, índice, estrutura e tabelas.

Referências abertas em `feature-wiki/references/`:

- `hosts-e-subagentes.md`, `ponytail-caveman.md`, `delegacao-casos-de-teste.md`;
- `roteamento-e-despacho.md`, `template-03-progresso.md`, `citacoes-de-codigo.md`.

Referências abertas em `feature-test-design/references/`:

- `template-04.md`, `escolha-de-camada.md`, `tecnicas-por-regra.md`;
- `taxonomia-de-defeito.md`, `gherkin.md`, `armadilhas-de-api.md`;
- `mutation-testing.md`, `revisao-adversarial.md`;
- `pest-plugin-browser.md`, `template-05.md`.

Arquivo final escrito somente na pasta de saída indicada.