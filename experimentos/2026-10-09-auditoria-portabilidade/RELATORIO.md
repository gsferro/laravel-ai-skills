# Auditoria integral, portabilidade e regressões — 2026-10-09

## Avaliação sincera

A coletânea tem uma base metodológica forte: requisito original imutável, testes derivados do
requisito, separação entre plano e oráculo, rastreabilidade, revisão adversarial e experimentos com
catálogo oculto. Isso é mais consistente que instruções genéricas de “escreva bons testes”. Os
históricos também declaram limites e medições ausentes, o que permite discutir qualidade com evidência.

Antes desta revisão, a portabilidade era sobretudo conceitual: tiers eram portáveis, mas comandos,
descoberta, despacho, aliases e alguns contratos ainda pressupunham Claude Code. Havia falsos
verdes nos scripts e regras que incentivavam certeza artificial: quota de achados, fórmula de
duração, silêncio do detector tratado como ausência e intermitência descartada automaticamente.
Esses problemas reduziam a confiança dos gates, apesar da boa intenção da metodologia.

Depois, há um contrato comum por capacidades, cinco perfis Codex distribuíveis, política de tickets
explícita nos dois hosts e regressões reproduzíveis dos defeitos corrigidos. Revisão e QA registram
controles efetivos; autorizações existentes dispensam checkpoints repetidos. A melhora operacional
é demonstrável. **Ainda não está demonstrado que a versão nova produz CT melhores, custa menos
tokens ou funciona tão bem no Codex quanto no Claude em uma feature real.** Esse veredito exige o
protocolo comportamental, não uma nota subjetiva ou porcentagem de smoke tests.

O principal débito restante é custo de contexto: três corpos continuam acima da recomendação de
500 linhas. Encurtar descrições melhora descoberta; não reduz automaticamente o custo de executar
as skills. Não removi regras derivadas de medições nem reescrevi os corpos para obter uma economia
aparente sem medir regressão de comportamento.

## Escopo e método

- Baseline: commit `6e9222c0f12769795dd4321e4f47f6509dbc2d9e`, extraído por `git archive` para pasta temporária.
- Candidata: árvore de trabalho desta revisão; versões 4.1.0 / 1.17.0 / 1.8.0 / 1.5.0 / 1.1.0.
- Lidos: as cinco SKILL.md e READMEs, todas as referências e agentes originais, todos os scripts,
  workflow de CI, README raiz, protocolo experimental e estudos pertinentes. Históricos de rodada
  são evidência anterior; não foram re-julgados como se fossem resultados desta revisão.
- Três investigações por recorte, com contexto mínimo e `reasoning_effort: ultra`; revisão
  independente adicional do diff, scripts, perfis e métricas, sem histórico da sessão principal.
- Ambiente: Windows/PowerShell, Git Bash, PHP 8.4 e Python 3.11; CLI observado `codex-cli 0.162.0`.
- Nenhuma chamada real ao GitHub, aplicação Laravel, navegador de aplicação, publicação ou release.

O esforço máximo foi solicitado e usado nos despachos de subagentes. `.codex/config.toml` contém
a preferência `ultra` para clientes/modelos compatíveis. Configuração em disco não altera o turno
principal em andamento; não há ferramenta nesta conversa para confirmar ou mudar seu esforço efetivo.

## Antes e depois medidos

| Instrumento | Antes | Depois | O que demonstra |
|---|---:|---:|---|
| `tests/run.py` | 34/45 | 45/45 | scripts, fixtures, IDs, rules, tema, hook e distribuição Codex |
| tickets + cobertura XML (`test_tickets.py`, `test_arch.py`) | 3/11 | 11/11 | estados, origem de CT, idempotência simulada e seleção XML |
| callback publicado de expand-contract (`test_expand.py`) | 0/1 método; 4/5 casos | 1/1 método; 5/5 casos | conflito de escrita dupla rejeitado antes da persistência simulada |
| Total de métodos/testes | **37/57** | **57/57** | cumprimento desses casos específicos; não é cobertura geral |
| Descrições, soma de caracteres | 4.668 | 1.188 | **−74,55%** de texto de descoberta; não é contagem de tokens |
| Perfis Codex distribuídos | 0 | 5 | arquivos TOML com contratos e sandbox declarado |
| Campos essenciais das cinco skills | válidos no validador existente | válidos | formato Agent Skills; não prova comportamento |

Duas das falhas anteriores representam capacidades novas (perfis e política Codex); as demais
reproduzem defeitos nos casos exercitados. Contagem de métodos não multiplica os subtestes. As
durações estão nos JSON, mas esta rodada não controla aquecimento/cache/carga da máquina e não
suporta conclusão de desempenho.

Evidências completas:
[runner antes](antes.json), [runner depois](depois.json),
[auxiliares antes](aux-antes.json), [auxiliares depois](aux-depois.json),
[callback antes](expand-antes.json), [callback depois](expand-depois.json).
Os pares usam os mesmos hashes dos instrumentos. Falhas do baseline são preservadas, não “corrigidas” no relatório.

## Achados corrigidos

| Prioridade | Antes / caso concreto | Depois / evidência |
|---|---|---|
| Alta | `request->all`, atributos de model e exceções brutas eram recomendados em logs | allowlist de IDs internos/metadados; exemplos PHP lintados; formatter JSON suportado |
| Alta | rules ignorava staged, unstaged e arquivos novos | união das camadas Git; três regressões antes vermelhas agora verdes |
| Alta | ID em comentário/fixture/método/construtor/atributo satisfazia CT sem teste real | tokenização de chamadas Pest com nome literal; cinco negativos falsificáveis |
| Alta | prova `arch()` ignorava suffix/exclude XML e declarava teste coberto pelo CI | seleção do arquivo real por suíte; cinco testes de XML com Pest simulado |
| Alta | Status recuado passava no índice, mas espelho não gravava Issue e duplicava criação | gravação compatível, falha explícita e rerun idempotente com gh simulado |
| Alta | retirada de `app/` por stash afetava trabalho anterior e não isolava a correção | cópia descartável; retirar somente patch da correção mantendo o CT; prova impossível fica pendente |
| Alta | dupla escrita aceitava as duas colunas dirty com valores distintos | rejeição explícita e preservação do estado persistido, comprovada no callback extraído do exemplo |
| Média | enum por prefixo aceitava `prontooo`; CT sem regra/origem escapava da alocação | enum completo e validação de origem, com regressões |
| Média | tema CSS inline passava como ausência; silêncio era prova de não aplicável | detecção inline e confirmação adicional por configuração/vendor/UI |
| Média | intermitência após três runs era infra/não-defeito automaticamente | investigar race/timing/estado; severidade segue consequência comprovada |
| Média | fallback QA e cobertura por CT/CT-B se contradiziam | fallback completo conta; camada mais barata que prova; independência ausente é débito |
| Média | todos sobreviventes viravam defeito/CT e duração seguia fórmula fixa | equivalência comprovada, cache/paralelismo e triagem; observabilidade sem RQ vai à dimensão D |
| Média | adversário precisava “achar cinco”; revisor era suspeito sem rejeição | zero achados/rejeições é válido com escopo percorrido; não inventar defeitos |
| Média | contrato repetia modelo `opus` mesmo no perfil Codex | modelo efetivo do host ou “não informado”; aliases ficam no adaptador Claude |
| Média | CT-B só buscava paths Claude e browser paralelo era proibido universalmente | raiz efetiva por host; execução serial conservadora, paralelo condicionado a isolamento/capacidade |
| Média | `Http::fake()` amplo tornava `preventStrayRequests()` ineficaz | fake por padrões restritos e fatos de framework versionados, com fontes primárias |
| Média | regras sobre afterCommit/relógio tratavam comportamento de framework como absoluto | conferir implementação e versão do vendor; exemplos corrigidos para baseline documentada |
| Média | grep Livewire encontrava só a declaração nullable do exemplo | 1/3 antes, 3/3 depois no self-check; atributo Locked exige leitura de contexto |
| Média | confirmações rotineiras interrompiam trabalho já autorizado | perguntar só por informação material ou nova autorização necessária |
| Média | instalação sugeria sobrescrever `AGENTS.md` | baixar referência separada e mesclar somente instruções pertinentes |

As provas documentais não foram convertidas artificialmente em testes que só procuram a frase
nova. Correções de procedimento e framework tiveram revisão de fontes/contratos; scripts e
callback executável têm regressões que falham no baseline.

## Limites e próximos experimentos

1. **DDR/MSI e experiência real de feature:** não executados. O repositório não contém aplicação,
   vendor ou banco do kit. Seguir [PROTOCOLO.md](../protocolo/PROTOCOLO.md) no projeto isolado;
   mesma versão de kit, oráculo, prompt e juiz, sem catálogo acessível aos braços.
2. **Paridade Claude/Codex:** TOML analisado e campos essenciais conferidos; contratos revisados
   contra [documentação oficial](https://learn.chatgpt.com/docs/agent-configuration/subagents).
   Falta uma execução real dos cinco agentes nativos e uma feature equivalente nos dois hosts.
3. **Isolamento:** prompts, sandbox declarado e hook não garantem todas as restrições. Contexto
   novo reduz contaminação inicial; acesso por shell/MCP e overrides efetivos devem ser registrados.
   `git status` sozinho não detecta nova edição num arquivo já modificado.
4. **CI Linux/Windows:** os testes rodaram localmente com Git Bash/PHP Windows. Workflow atualizado,
   mas a execução hospedada após push não foi observada nesta sessão.
5. **Simuladores:** gh simulado não prova GitHub Projects real; runner Pest simulado não prova
   seleção real de uma versão de PHPUnit; stub do model não prova ciclo de persistência Laravel.
6. **Contexto:** três SKILL.md extensos permanecem. Próxima redução deve mover procedimentos
   condicionais com benchmark pareado, preservando cláusulas e oráculos, não apagar regras por tamanho.

README raiz, READMEs das cinco skills, instruções, referências, perfis e CHANGELOG foram reconciliados.
Versões são locais e não publicadas. Nenhuma tag, commit, PR ou release foi criada.
