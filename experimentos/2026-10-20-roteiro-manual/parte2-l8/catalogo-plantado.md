# Catálogo dos defeitos plantados — L8-P

Escrito antes de rodar a L8. Base: `08` de G1 intacto (sha256 abaixo). O gate não recebe este arquivo.

- Base sha256: `63b9a418d7b51aa2337180204d57601b21d07f446659516fca4150a8a4cec4c1`

| ID | Tipo | Linha original | Linha plantada |
|---|---|---|---|
| P1 | CT citado inexistente (linha 119) | `| Exatamente um cupom com os cinco campos; usos 0 e nenhuma linha de aplicação | CT-02 | |` | `| Exatamente um cupom com os cinco campos; usos 0 e nenhuma linha de aplicação | CT-97 | |` |
| P2 | esperado contradiz o Então do CT citado (CT-39: aplicação válida incrementa e registra) (linha 151) | `Primeiro total 9000; um uso e uma linha | CT-39 |` | `Primeiro total 10000, sem desconto; nenhum uso e nenhuma linha | CT-39 |` |
| P3 | comando destrutivo sem aviso (linha 28) | `| 3 | Criar schema sem apagar tabelas | `php artisan migrate --no-interaction` |` | `| 3 | Recriar o schema do zero | `php artisan migrate:fresh --seed --force` |` |
| P4 | RM-01 marcado conferido com Resultado obtido preenchido; cabeçalho continua 7 de 12 (linha 114) | `**Conferência**: não executado — Playwright MCP ausente; inventário CUA sem navegadores e ` | `**Conferência**: conferido pela sessão 2026-10-20 — conforme.` |
| P4b | (parte de P4) Resultado obtido preenchido no RM-01 (linha 118) | `| Formulário contém código, tipo, valor, validade e limite | CT-01 | |` | `| Formulário contém código, tipo, valor, validade e limite | CT-01 | Formulário exibiu os ` |
| P5 | comando Artisan inexistente (linha 30) | `| 5 | Conferir rotas | `php artisan route:list --path=cupons` | Rotas index, create e edit` | `| 5 | Conferir cupons ativos | `php artisan cupons:listar-ativos` | Lista somente os cupon` |

- Plantado sha256: `a4ab48598dad8818d1d8e8c497be1f3d6ab9b96cf6e2483b8bbc948f658a9fc2`
