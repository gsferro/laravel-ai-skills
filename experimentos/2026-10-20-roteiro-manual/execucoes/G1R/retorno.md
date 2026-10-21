`metadata.version`: **4.2.0**. Host: **Codex**. Modelo: **GPT-6**, variante não exposta.

Arquivo: [08-roteiro-teste-manual.md](D:/PROJECTS/SKILLS/blind-20261020-p2/proj-273d38/wikis/specs/saida-g1/cupons-de-desconto/08-roteiro-teste-manual.md).

**24 RM; 12 conferidos:** seis aderentes e seis divergentes. Outros 12 dependem de navegador, indisponível; fluxos multi-tenant também ficaram sem servidor alinhado.

Divergências reproduzidas:

- CT-22: leitor cria, edita e exclui diretamente.
- CT-20: código duplicado aceito com tenant nulo.
- CT-12: percentual 101 persistido.
- CT-16: limite 1.5 persistido, apresentado como 1.
- CT-27: consulta sem contexto retorna cupons de todos os tenants.
- CT-52: admin da Acme altera/exclui referência da Globex.

Achados registrados no `08`, com saídas literais em `validation/`. Esperados preservados; nenhuma correção aplicada. Retorno aos steps 9/10 ficou pendente pelas restrições. **Step 11 não executado.**

`roteiro-manual.sh`: **stdout/stderr vazios; exit 0**.

References abertas: `hosts-e-subagentes.md`, `template-08-roteiro-manual.md` e `ponytail-caveman.md`.

Desvios/degradações: registros concentrados no `08`, pois `03` é imutável; sem Git/commit, Boost ou navegador. Migrate aninhado exigiu ajuste de invocação; preparação corrigida e reexecutada. Snapshot do RM-15 corrigido e reconferido.

**283 arquivos preexistentes monitorados intactos**, incluindo código e documentos anteriores da wiki.