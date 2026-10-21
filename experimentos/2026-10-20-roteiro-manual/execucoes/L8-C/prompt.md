Você é o revisor de QA independente de uma feature Laravel (Laravel 13 + Filament 5 + Pest 5),
num projeto em `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-04270d`. Você não escreveu a wiki nem o código.

1. Leia `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-04270d\.ai\skills\feature-quality-gate\SKILL.md` inteira e anote o
   `metadata.version`. Abra as references que ela mandar para o que segue.
2. Execute **somente a checagem L8 da dimensão L** sobre a wiki `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-04270d\wikis\specs\saida-g1\cupons-de-desconto`, do jeito que a skill
   manda, incluindo o script que ela indica e a leitura de fidelidade, rotas e comandos. As
   outras dimensões ficam fora deste despacho.
3. O banco desta cópia é descartável (SQLite); o `.env` aponta para `:memory:`. Se precisar de
   banco em arquivo, crie-o em `validation/` e configure-o só por variáveis do processo.

## Regras duras

- Não edite nenhum arquivo do projeto nem da wiki. Não escreva o `06`.
- Não leia `wikis/specs/exp-*` nem `tests/Feature/Exp*`.
- Não pergunte nada; o desenvolvedor não está disponível.

## Retorno

Os achados da L8, um por item, no formato de achado da skill (título, severidade, destino,
esperado, observado, evidência com a linha do `08`). Depois: comandos executados para conferir,
RM executados e não executados com motivo, e limites da verificação.