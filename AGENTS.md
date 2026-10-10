# Manutenção da coletânea

Este repositório contém skills, referências, agentes e experimentos. Não é uma aplicação Laravel.
Não crie uma wiki de feature Laravel para editar as próprias skills.

- A fonte das skills é `.ai/skills/`. Leia o `SKILL.md` da skill alterada e somente as referências pertinentes.
- Preserve a separação: README para pessoas; SKILL para obrigações; references para procedimentos condicionais; scripts para verificações determinísticas.
- O contrato de processo deve funcionar em qualquer host. Comandos e controles específicos ficam no adaptador do host.
- Autorização e instruções explícitas do usuário prevalecem sobre confirmações padronizadas da skill.
- Para revisões amplas, delegue investigações independentes com contexto mínimo. Revisores não editam; a sessão decide as correções.
- Nunca trate prompt, `read-only`, hook heurístico ou `git status` como prova de isolamento de leitura. Registre as restrições efetivas.
- Antes de concluir alterações, rode `python tests/run.py` e `python -m unittest discover -s tests -p 'test_*.py'`. Regressões usam fixtures temporárias.
- `experimentos/protocolo/` define a medição comportamental. Não exponha catálogos e resultados aos braços. Não declare DDR, economia de tokens ou equivalência entre hosts sem executar a medição correspondente.
- Atualize README, instruções afetadas, versões e CHANGELOG. Identifique o que foi executado e o que continua não medido.

Perfis Codex distribuíveis estão em `.ai/skills/*/agents/codex/`; a instalação do README os copia para `.codex/agents/` do projeto consumidor.
