> Referência da feature-wiki 3.6.0. Lida em: step 4 (antes de decidir os arquivos extras). Fonte única de: arquivos extras `05-*` e exemplo de árvore criada.

# Estrutura criada

## Arquivos Extras (conforme necessidade)

Criar apenas quando a feature exige:

| Arquivo | Quando criar |
|---------|-------------|
| `05-casos-de-teste-browser.md` | Feature que passa no gate de CT-B — ver [Arquivos 04 e 05](../SKILL.md#arquivos-04-e-05-casos-de-teste--delegados-à-feature-test-design) |
| `05-design.md` | Feature com UI significativa (Filament, Livewire, Blade) |
| `05-api-contract.md` | Feature com API externa (payloads, endpoints, autenticação) |
| `05-db-schema.md` | Feature com schema complexo (múltiplas tabelas, migrations em cadeia) |
| `05-fluxo.md` | Feature com fluxo multi-etapas (queues + jobs + callbacks) |
| `05-rollback.md` | Feature com migrations destrutivas ou mudanças de schema irreversíveis |
| `05-performance.md` | Feature com volume alto (batch processing, relatórios, imports de CSV) |
| `05-security.md` | Feature com dados sensíveis (PII, pagamentos, autenticação, LGPD) |

## Exemplo de Estrutura Criada

```text
wikis/
└── specs/
    └── ferro/
        └── 579/
            └── relatorio-mba-lote/
                ├── 00-requisito.md                  ← requisito bruto imutável + RQ-##
                ├── 01-plano-acao.md
                ├── 02-decisoes-arquiteturais.md      ← formato ADR
                ├── 03-progresso.md                   ← + Blockers, Desvios, Retrospectiva
                ├── 04-casos-de-teste.md              ← backend: + CTs de autorização
                ├── 05-casos-de-teste-browser.md      ← CT-B + roteiro desenhado × implementado
                ├── 05-api-contract.md                ← extra quando necessário
                ├── 05-rollback.md                    ← extra quando necessário
                └── 06-relatorio-qa.md                ← saída do feature-quality-gate
```
