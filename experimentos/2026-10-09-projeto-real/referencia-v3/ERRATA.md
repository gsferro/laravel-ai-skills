# Errata da localização da API

O relatório `CORRECAO.md` original e congelado chama a conversão de `EnumStateCast::cast`.
No Filament 5.7.6, o método correto é `EnumStateCast::get(mixed $state)`, linha 17 do vendor
e da [fonte oficial fixada](https://github.com/filamentphp/filament/blob/v5.7.6/packages/schemas/src/Components/StateCasts/EnumStateCast.php).
O método devolve o caso enum e sustenta o diagnóstico; o nome incorreto da API não muda o patch.
Preserva-se o relatório original, com esta correção factual separada. Não há alteração dos 42
arquivos do manifesto da referência nem dos controles e resultados.
