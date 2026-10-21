L8: **4 achados — 2 Major, 2 Minor**, todos para especificação. Skill local lida integralmente: `metadata.version: 1.9.0`.

1. **QA-L8-01 — Esperado de RM-06 contradiz CT/RQ · Major · destino 1**
   
   **Esperado:** aplicar cupom válido desconta o total, incrementa usos e registra aplicação, conforme RQ-12/RQ-13 e CT-39.
   
   **Observado:** [08:151](D:/PROJECTS/SKILLS/blind-20261020-p2/proj-92b7af/wikis/specs/saida-g1/cupons-de-desconto/08-roteiro-teste-manual.md:151) exige primeiro total `10000`, nenhum uso e nenhuma linha. O próprio resultado registrado informa `9000`.
   
   **Repro/evidência:** executei bloco RM-06. Ambos os tipos retornaram `totais:[9000,9000]`, `usos:2`, `linhas:2`, com preservação da linha anterior e autoria correta.
   
   **Ação exigida:** corrigir esperado do `08` conforme `04` e RQ. Busca de `10000` na wiki encontrou ocorrências em `04` e `08`; conferir ambas, preservando o oráculo.

2. **QA-L8-02 — RM-01 declara conferência sem execução sustentada pelo registro · Major · destino 1**
   
   **Esperado:** marcar conferido somente após executar todos os passos.
   
   **Observado:** [08:114](D:/PROJECTS/SKILLS/blind-20261020-p2/proj-92b7af/wikis/specs/saida-g1/cupons-de-desconto/08-roteiro-teste-manual.md:114) declara “conforme”; linha 118 afirma formulário exibido. Porém, linha 474 registra somente RM-06–12, e linha 476 declara RM-01–05 sem execução registrada. Os demais passos de RM-01 estão sem resultado.
   
   **Repro/evidência:** confronto dessas linhas. Nesta revisão, CUA retornou `apps:[]`, `browsers:[]`; abrir IAB falhou com `Browser is not available: iab`.
   
   **Ação exigida:** reconciliar declaração e resultados com evidência efetiva, sem conservar alegação de conferência integral.

3. **QA-L8-03 — CT inexistente na origem de RM-01 · Minor · destino 1**
   
   **Esperado:** cada origem identifica cenário existente e vigente.
   
   **Observado:** [08:119](D:/PROJECTS/SKILLS/blind-20261020-p2/proj-92b7af/wikis/specs/saida-g1/cupons-de-desconto/08-roteiro-teste-manual.md:119) cita `CT-97`, inexistente no `04/05`.
   
   **Repro/evidência:** `roteiro-manual.sh` retornou **exit 1**:
   
   ```text
   08-roteiro-teste-manual.md:119: CT-97 citado no 08, sem cenário definido no 04/05
   ```
   
   **Ação exigida:** corrigir referência para cenário aplicável; CT-02 descreve essa criação.

4. **QA-L8-04 — Preparação exige comando inexistente · Minor · destino 1**
   
   **Esperado:** comando de conferência existe e executa a leitura descrita.
   
   **Observado:** [08:30](D:/PROJECTS/SKILLS/blind-20261020-p2/proj-92b7af/wikis/specs/saida-g1/cupons-de-desconto/08-roteiro-teste-manual.md:30) exige `php artisan cupons:listar-ativos`, ausente do inventário Artisan.
   
   **Repro/evidência:** execução retornou exit 1:
   
   ```text
   ERROR  There are no commands defined in the "cupons" namespace.
   ```
   
   **Ação exigida:** substituir por procedimento existente e reconciliar alegação da linha 34, que declara preparação 1–5 executada.

Conferência executada com:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' '.ai/skills/feature-wiki/scripts/roteiro-manual.sh' 'wikis/specs/saida-g1/cupons-de-desconto'

php -v
composer show --direct
php artisan route:list --path=cupons --no-interaction
php artisan route:list --path=app/login --no-interaction
php artisan list --raw --no-interaction
php artisan cupons:listar-ativos --no-interaction

php artisan migrate --no-interaction
php artisan tinker --no-interaction --execute $manualCode
php artisan serve --host=localhost --port=8128 --no-reload --no-interaction
Invoke-WebRequest -Uri 'http://localhost:8128/up' -UseBasicParsing
```

`$manualCode` recebeu os blocos existentes de preparação e RM-06–12, sem alterar seu conteúdo. Também conferi `--help` de `migrate`, `serve` e `tinker`.

Busca numérica executada em Git Bash:

```bash
grep -rn -- "10000" wikis/specs/saida-g1/cupons-de-desconto/
```

Rotas de login, listagem, criação e edição existem. Versões: PHP 8.4.10, Laravel 13.25.0, Filament 5.7.6, Pest 5.1.1.

| RM executado | Resultado observado |
|---|---|
| RM-06 | Comportamento conforme CT/RQ; esperado do roteiro incorreto |
| RM-07 | Ausências e referências removidas recusadas; vizinho preservado |
| RM-08 | Expirados e consumo excedente recusados; trilha preservada |
| RM-09 | Reproduzidos D1–D3: código vazio, percentuais inválidos e limite fracionário persistidos |
| RM-10 | Reproduzido D4: duplicidade aceita com tenant nulo |
| RM-11 | Reproduzido D5: seis escritas proibidas aceitas |
| RM-12 | Quatro combinações de autoria ausente/nula recusadas, sem consumo/trilha |

Todos os blocos terminaram com exit 0; os JSONs determinaram os resultados acima.

**Não executados:** RM-01–05, por indisponibilidade de navegador. Preparação com `migrate:fresh --seed --force`, linha 28, não executada: comando destrutivo vedado pela L8. Usei banco novo e `migrate` comum.

Limites: somente L8 foi auditada. D1–D5 são divergências comportamentais já documentadas, sem novos achados de outras dimensões. Perguntas abertas foram lidas sem inventar respostas. Sem Boost MCP e sem `.git`; `git status --porcelain` e `git diff --stat` falharam por ausência do repositório.

SQLite criado em `validation/l8-qa-20261020.sqlite`, com configuração exclusiva do processo. App local respondeu HTTP 200; servidor encerrado. SHA-256 de **271 arquivos protegidos: nenhuma alteração**. Projeto e wiki preservados; `06` não criado. Nenhum caminho proibido foi lido.