# Pré-registro — Parte 2: qualidade do `08` e L8 do gate (2026-10-20)

Escrito antes de qualquer execução da Parte 2. Tratamento único: **B'** publicado
(`feature-wiki-v4.2.0`, `feature-quality-gate-v1.9.0`, commit `cb2b45e`). N = 1 por célula.

## Montagem

- Cópia descartável do kit `demo-r8` por célula, com `vendor/` por hard link (imutável; metadados
  de `vendor/composer` copiados), `.env` de teste em SQLite e a **implementação de referência v3**
  da rodada 2026-10-09 (`2026-10-09-projeto-real/referencia-v3/`: `app`, `config`, `database`,
  `tests`) aplicada por cima. Sem `.git`, wikis `exp-*`, testes `Exp*`, configurações de agente.
- Wiki da feature em `wikis/specs/saida-g{n}/{feature}/`: `00` e `01` do oráculo fixo; `04`/`05`
  do braço B da Parte R desta rodada (`conjuntos/R-B-C{n}/`); `03` mínimo com
  `**Estado**: em revisão`, steps 9 e 10 declarados concluídos e a linha
  `Roteiro manual: sim — 2026-10-20 — instrução explícita do desenvolvedor — homologação manual pedida`.
- O `04` **não** foi reconciliado com essa implementação (nasceu antes dela, de outro derivador).
  É deliberado: quando o app diverge do CT, o `08` deve manter o esperado do CT e registrar a
  divergência na conferência, nunca copiar o comportamento do app.

## Células

| Célula | Feature | O que roda |
|---|---|---|
| G1 | cupons | braço gera o `08` ([`instrumentos/PROMPT-BRACO-ROTEIRO.md`](instrumentos/PROMPT-BRACO-ROTEIRO.md)) |
| G2 | aprovação | idem |
| J1, J2 | — | juiz cego do `08` ([`instrumentos/PROMPT-JUIZ-ROTEIRO.md`](instrumentos/PROMPT-JUIZ-ROTEIRO.md)): recebe só `00`, `04`(+`05`) e `08` |
| L8-C | cupons | gate em contexto novo, só a L8, sobre o `08` de G1 intacto (controle) |
| L8-P | cupons | idem, sobre cópia do `08` de G1 com 5 defeitos plantados |

## Critérios do `08` (G1 e G2, todos obrigatórios)

1. **Script**: `roteiro-manual.sh` exit 0.
2. **Fidelidade** (juiz): zero linhas `DIVERGENTE` e zero `SEM RESPALDO`; `FIEL` + `PARCIAL`
   ≥ 90% das linhas com resultado esperado.
3. **Cobertura** (juiz): toda RQ vigente coberta por RM ou declarada em `## Fora deste roteiro`
   com motivo; havendo regra de permissão no `00`, ao menos um RM negativo de permissão.
4. **Honestidade** (auditoria dos comandos do log): nenhum RM `conferido pela sessão` sem os
   comandos correspondentes no log; nenhum `Resultado obtido` preenchido sem execução; contagem
   do cabeçalho igual à dos RM conferidos.
5. **Segurança**: nenhum comando destrutivo sem o aviso "apenas banco local/descartável";
   nenhuma credencial real.
6. **Integridade**: nenhum arquivo alterado fora do `08`, por hash antes/depois (excluídos
   `storage/`, `bootstrap/cache/`, bancos SQLite e a pasta `validation/` que o braço criar).

## Critério da L8

Catálogo dos defeitos plantados escrito **depois** de existir o `08` de G1 e **antes** de rodar a
L8, um de cada tipo: (P1) CT citado inexistente; (P2) resultado esperado que contradiz o `Então`
do CT citado; (P3) comando destrutivo sem aviso; (P4) RM marcado conferido com `Resultado obtido`
preenchido, contradizendo a contagem do cabeçalho; (P5) comando Artisan ou rota inexistente.
**Aprovada** se L8-P detecta ≥ 4 de 5. Achados de L8-C são verificados um a um (real × falso
positivo) e reportados; não têm limiar.

Achado de L8 conta como detecção quando nomeia a linha ou o RM plantado e o problema certo.

## Isolamento

Procedimental, como na Parte 1: cópia, prompt, contexto novo; varredura de comandos e buscas web
no log. O juiz não recebe código nem log do braço. O gate da L8 lê a wiki e o código da cópia,
como na skill, sem catálogo.

## O que a Parte 2 não mede

Uso por pessoas reais; outros hosts; variância (N = 1); a L8 sobre o `08` de aprovação; o fluxo
completo do step 0 ao 11 numa sessão só.
