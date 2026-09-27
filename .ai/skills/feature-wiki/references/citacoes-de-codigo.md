> Referência da feature-wiki 3.6.0. Lida em: steps 3 e 5 (ao escrever uma citação) e step 7 (ao reverificar todas). Fonte única de: as duas classes de erro de citação, exemplos do formato e o comando de conferência.

# Citações de código — `arquivo:símbolo:linha`

O formato obrigatório, a regra do path curto, o critério de que citação sem símbolo não passa e o
registro na Verificação Final ficam no corpo do `SKILL.md`, seção *Citações de código*.

O step 3 desta skill (e a rule `specs.md` do projeto-cobaia) exige `arquivo:linha` para toda
afirmação sobre vendor ou padrão interno. O formato só com linha falha de dois jeitos distintos,
medidos na mesma feature:

| Classe | Exemplo real | O que pega |
|---|---|---|
| **Errada ao nascer** | `Login.php:165` para `return app(LoginResponse::class)`, que está na 169 — e o `composer.lock` não mudou em nenhum commit da feature | conferir **ao escrever** (step 5) |
| **Deslocada depois** | citações de arquivos da própria app, 3 a 10 linhas fora após Pint e imports novos | conferir **no step 7** |

"Reverificar depois" não pega a primeira classe; "conferir ao escrever" não pega a segunda. São
dois momentos, e o mesmo comando serve aos dois.

## Exemplos do formato

```text
vendor/filament/filament/src/Auth/Pages/Login.php:isUserAllowedToAccessPanel():172
app/Support/DestinoAposLogin.php:urlPara():41-58
config/logging.php:'autenticacao':132
```

## Conferência mecânica

```bash
grep -rhoE "[A-Za-z0-9_./-]+\.php:[A-Za-z_'\"][A-Za-z0-9_'\"]*(\(\))?:[0-9]+" wikis/specs/{branch}/{feature}/ \
  | sort -u | while IFS=: read -r arquivo simbolo linha; do
    simbolo="${simbolo%()}"; simbolo="${simbolo//\'/}"; simbolo="${simbolo//\"/}"
    if sed -n "${linha}p" "$arquivo" 2>/dev/null | grep -q -- "$simbolo"; then echo "ok   $arquivo:$simbolo:$linha"
    else echo "ERRO $arquivo:$simbolo:$linha"; fi
  done
```
