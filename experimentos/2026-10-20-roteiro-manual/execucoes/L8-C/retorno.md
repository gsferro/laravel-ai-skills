Nenhum achado L8 confirmado. Skill local lida integralmente: `metadata.version: 1.9.0`.

`roteiro-manual.sh` terminou com **exit 0**, sem stdout/stderr. A leitura dos 12 RM confirmou decisão/presença coerentes, referências vigentes e esperados fiéis aos CT/RQ. Perguntas abertas não receberam respostas inventadas.

**RM executados nesta revisão**

| RM | Resultado observado | Evidência no `08` |
|---|---|---|
| RM-06 | Conforme: ambos retornaram `[9000,9000]`; usos 2, linhas 2, autoria e preservação confirmadas | linhas 151–167 |
| RM-08 | Conforme: último consumo permitido; tentativas posteriores e expirados recusados, sem alterar trilha | linhas 253–272 |
| RM-09 | Reproduziu D1–D3: código vazio, percentuais inválidos e limite fracionário foram persistidos | linha 285 |
| RM-10 | Reproduziu D4: duplicidade aceita com tenant nulo; recusada nos tenants A/B | linha 323 |
| RM-12 | Conforme: quatro combinações de autoria ausente/nula recusadas, usos e linhas 0 | linha 395 |

Todos terminaram com exit `0`. As divergências de RM-09/RM-10 são comportamentais e já estão descritas corretamente no roteiro; **não constituem achados L8**.

**RM não executados**

- **RM-01, RM-02, RM-04 e RM-05:** sem navegador disponível; inventário CUA retornou `apps:[]`, `browsers:[]`.
- **RM-03:** sem navegador e contém exclusão.
- **RM-07 e RM-11:** contêm chamadas `delete()`; excluídos pela restrição da L8 a comandos destrutivos.

**Comandos de conferência**

```powershell
& 'C:/Program Files/Git/bin/bash.exe' '.ai/skills/feature-wiki/scripts/roteiro-manual.sh' 'wikis/specs/saida-g1/cupons-de-desconto'
php -v
composer show --direct
php artisan route:list --path=cupons --no-interaction
php artisan list --raw --no-interaction
php artisan help tinker --no-interaction
php artisan migrate --no-interaction
php artisan tinker --no-interaction --execute $preparacao
php artisan tinker --no-interaction --execute $manualCode
php artisan serve --host=127.0.0.1 --port=18427 --no-reload --no-interaction
```

Os blocos `$manualCode` foram extraídos do `08`, sem alteração. As três rotas de cupons existem. `/up` respondeu HTTP `200`. Versões confirmadas: PHP **8.4.10**, Laravel **13.25.0**, Filament **5.7.6**, Pest **5.1.1**.

**Limites**

- Somente L8 executada; nenhum veredito global da feature.
- Reprodução com `KIT_TENANCY=false`; RM-10 não comprova autorização multi-tenant.
- Execução histórica declarada no `08` não foi certificada integralmente.
- Sem Boost MCP e sem `.git`; `git status --porcelain` falhou antes/depois.
- Comparação SHA-256: **282 arquivos protegidos, zero alterações**.
- Artefatos novos ficaram em `validation/`, incluindo SQLite e saídas da reprodução. `.env` e wiki preservados; `06` não criado.
- Caminhos proibidos não foram lidos. Servidores iniciados nesta revisão foram encerrados.