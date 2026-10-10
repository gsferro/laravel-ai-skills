# Correção da referência v2

Data: 2026-10-09. Escopo: obrigatoriedade do usuário em `Cupom::aplicarEm`.

Causa confirmada: P-01 do `wikis/specs/oraculo/cupons-de-desconto/00-requisito.md:79` exige `User $aplicadoPor`. A implementação v1 seguiu a assinatura `?User $aplicadoPor = null` do `01-plano-acao.md:626`, contrariando a precedência do requisito e permitindo omitir a identificação do ator. A v2 aplica a assinatura do 00 e remove os acessos nullsafe ao usuário na trilha e no log.

Arquivos alterados:

- `app/Models/Cupom.php`: argumento `User` obrigatório, sem valor padrão.
- `tests/Feature/LaboratorioContratoTest.php`: somente os três chamadores próprios que omitiam o argumento passam um usuário persistido de factory; expectativas preservadas.
- `contrato-publico.md`: assinatura, precedência do 00 e erros nativos para omissão/null documentados; validações anteriores identificadas como v1.
- `validation/correcao-referencia-v2.md`: este registro.

Revisão: conferência textual restrita ao 00/01 de cupons, implementação, contrato público e testes próprios. A assinatura recusa omissão com `ArgumentCountError` e null com `TypeError` antes de executar o método. O schema nullable/nullOnDelete foi preservado para a exclusão posterior do usuário; não foi acrescentada validação de persistência de instâncias User.

Limites: nenhum Pest, Artisan ou browser foi executado nesta correção, por instrução da root que administra a execução serial. Não há novo resultado de aprovação da v2. Especificações derivadas, conjuntos, catálogos, vereditos e logs derivados não foram lidos nem alterados. Vendor, configurações, ambiente, outras features e artefatos v1 foram preservados. O filesystem permanece irrestrito: estas restrições de leitura foram seguidas por seleção explícita de caminhos e não constituem isolamento técnico.
