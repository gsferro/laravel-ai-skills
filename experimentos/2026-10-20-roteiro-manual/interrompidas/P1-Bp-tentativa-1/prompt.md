Você é a sessão de um desenvolvedor num projeto Laravel real (Laravel 13 + Filament 5 + Pest 5).
Trabalhe integralmente em `D:\PROJECTS\SKILLS\blind-20261020\proj-a46afe`.

O desenvolvedor colou o card abaixo, que veio do solicitante, e pediu para planejar a feature
com a skill `feature-wiki`.

```text
CARD FERRO-812 — Cupons de desconto

Criar cupons de desconto no painel. O cupom tem um código, um tipo (porcentagem ou
valor fixo), o valor do desconto, uma data de validade e um limite de quantas vezes
pode ser usado.

Só quem é admin pode criar, editar e excluir cupom. Os outros usuários podem apenas
listar os cupons ativos.

Na hora de aplicar no pedido, o sistema valida se o cupom existe, se ainda está dentro
da validade e se não estourou o limite de usos. Se estiver tudo certo, aplica o desconto
no valor total do pedido e incrementa o contador de usos.

O código do cupom não pode se repetir.

Precisa registrar quem aplicou o cupom e quando, pra gente conseguir auditar depois.
```



## O que fazer

1. Leia `D:\PROJECTS\SKILLS\blind-20261020\proj-a46afe\.ai\skills\feature-wiki\SKILL.md` inteira e anote o `metadata.version`.
   Quando a skill mandar abrir um arquivo de `references/` ou outra skill, abra; não leia pastas
   inteiras por conta própria — a rodada mede a skill do jeito que ela está empacotada.
2. Execute os steps **0 a 4** da skill, nessa ordem, e **pare antes do step 5**. O texto do card
   acima é o requisito, do jeito que o solicitante escreveu.
3. O projeto não tem `.git`: no step 1, use `saida-p1-bp` como pasta de branch. A wiki fica em
   `D:\PROJECTS\SKILLS\blind-20261020\proj-a46afe\wikis\specs\saida-p1-bp\{nome da feature que o step 2 definir}\`.
4. O desenvolvedor **não está disponível** durante a execução e o solicitante também não. Toda
   pergunta que a skill mandar fazer ao desenvolvedor, escreva no retorno, no formato da skill,
   e siga o que a skill manda fazer quando não há resposta. Perguntas ao solicitante vão para
   onde a skill manda.

## Regras duras

- Não leia nenhuma pasta `wikis/specs/exp-*` nem `tests/Feature/Exp*`. As wikis de produção em
  `wikis/specs/main/` e `wikis/specs/feature/` e o resto do projeto são leitura permitida.
- Não implemente nada: nenhuma migration, model, service, resource, config ou teste.
- Não altere nenhum arquivo fora da pasta da wiki desta feature.
- Não execute steps posteriores ao 4, nem crie arquivos que a skill só cria em steps posteriores.

## Retorno

Resumo curto (máx. 40 linhas):

- o `metadata.version` de cada skill que você leu, e o host e o modelo desta sessão;
- os arquivos escritos, com path;
- **todas** as perguntas ao desenvolvedor, no formato da skill, com a raia e a recomendação;
  depois, quantas perguntas ficaram no `00` para o solicitante, por raia;
- o que você registrou por falta de resposta;
- os arquivos de `references/` que você abriu; desvios e degradações declarados.