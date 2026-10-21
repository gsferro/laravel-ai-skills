Você é a sessão de um desenvolvedor num projeto Laravel real (Laravel 13 + Filament 5 + Pest 5).
Trabalhe integralmente em `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-273d38`.

A feature da wiki `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-273d38\wikis\specs\saida-g1\cupons-de-desconto` já foi implementada; os steps 9 e 10 da `feature-wiki` estão
concluídos, como o `03-progresso.md` registra. O desenvolvedor pediu o roteiro de teste manual.

## O que fazer

1. Leia `D:\PROJECTS\SKILLS\blind-20261020-p2\proj-273d38\.ai\skills\feature-wiki\SKILL.md` inteira e anote o `metadata.version`.
   Quando a skill mandar abrir um arquivo de `references/`, abra; não leia pastas inteiras por
   conta própria.
2. Execute a etapa da skill que vem depois do step 10 e antes do step 11, para esta wiki, do
   jeito que a skill manda.
3. O banco desta cópia é descartável (SQLite). O `.env` aponta para `:memory:`; se precisar de um
   banco em arquivo para comandos Artisan, crie-o numa pasta `validation/` da raiz e configure-o
   só por variáveis de ambiente do processo. Não há e-mail real nem credencial real.

## Regras duras

- Não leia nenhuma pasta `wikis/specs/exp-*` nem `tests/Feature/Exp*`.
- Não altere código, testes, configuração, migrations, nem os arquivos `00` a `07` da wiki.
  A única escrita permitida na wiki é o arquivo que a etapa cria. Bancos SQLite, `storage/` e
  `validation/` podem mudar.
- O desenvolvedor não está disponível. Não pergunte nada; siga o que a skill manda quando não
  há resposta.
- Não execute o step 11.

## Retorno

Resumo curto (máx. 30 linhas): `metadata.version` lido, host e modelo; path do arquivo escrito;
quantos RM e quantos foram conferidos por você, com o motivo dos não conferidos; divergências
entre o app e os casos de teste encontradas na conferência e o que você fez com elas; a saída do
script que a etapa manda rodar; references abertas; desvios e degradações.