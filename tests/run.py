"""Regressões da coletânea, sem API, Laravel ou dependências Python externas.

Uso: python tests/run.py [--root checkout] [--report resultado.json]
As fixtures vivem em diretórios temporários. --root permite medir outro checkout
com exatamente o mesmo instrumento, sem editar o baseline.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH = os.environ.get("SKILLS_BASH") or (
    "C:/Program Files/Git/bin/bash.exe" if os.name == "nt" else shutil.which("bash")
)


def run(args, cwd, stdin=None):
    return subprocess.run(args, cwd=cwd, input=stdin, text=True, encoding="utf-8",
                          errors="replace", capture_output=True, timeout=60)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-regression-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.wiki = self.work / "wikis/specs/feature/demo"
        self.wiki.mkdir(parents=True)

    def write(self, path, content):
        target = self.work / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

    def script(self, skill, script, *args, stdin=None):
        path = ROOT / ".ai/skills" / skill / "scripts" / script
        result = run([BASH, str(path), *map(str, args)], self.work, stdin)
        return result

    def assert_exit(self, result, code):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)

    def git(self, *args):
        result = run(["git", *args], self.work)
        self.assert_exit(result, 0)
        return result

    def init_git(self):
        self.git("init", "-b", "main")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.write("app/Models/Demo.php", "<?php // baseline\n")
        self.git("add", ".")
        self.git("commit", "-m", "fixture")

    def trace_fixture(self):
        self.write("wikis/specs/feature/demo/00-requisito.md", """# Requisito
| ID | Cláusula | Estado |
|---|---|---|
| RQ-01 | Total exato | fechada |
""")
        self.write("wikis/specs/feature/demo/01-plano-acao.md", """## Cobertura do Requisito
| RQ | Passo | Observação |
|---|---|---|
| RQ-01 | 1 | |
## Estrutura de Implementação
### 1. Total
**Atende**: RQ-01
""")
        self.write("wikis/specs/feature/demo/04-casos-de-teste.md", """## Mapa de Regras
| Regra | Origem |
|---|---|
| R1 | RQ-01 |
## Índice de Cenários
| ID | Regra |
|---|---|
| CT-01 | R1 |

```gherkin
Cenário: [CT-01] total exato
  Dado um total de 10
  Quando consulto o total
  Então recebo 10
```
""")

    def test_trace_complete(self):
        self.trace_fixture()
        self.assert_exit(self.script("feature-wiki", "rastreabilidade.sh", self.wiki), 0)

    def test_trace_missing_scenario(self):
        self.trace_fixture()
        path = self.wiki / "04-casos-de-teste.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| CT-01 | R1 |", "| CT-02 | R2 |"), encoding="utf-8")
        result = self.script("feature-wiki", "rastreabilidade.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("RQ-01 sem CT", result.stdout)

    def manual_fixture(self, decision="sim", expected="O total exibido é 10", origin="RQ-01, P-01, CT-01, CT-B01"):
        self.write("wikis/specs/feature/demo/00-requisito.md", """# Requisito
## Decomposição em Cláusulas
| ID | Cláusula | Estado |
|---|---|---|
| RQ-01 | Total exato | fechada |
## Premissas
| ID | Premissa | Estado |
|---|---|---|
| P-01 | Exibir o total | vigente |
""")
        self.write("wikis/specs/feature/demo/03-progresso.md",
                   f"# Progresso\n\n- **Roteiro manual**: {decision} — fluxo pelo terminal\n")
        self.write("wikis/specs/feature/demo/04-casos-de-teste.md", """```gherkin
Cenário: [CT-01] total exato
  Então recebo 10
```
""")
        self.write("wikis/specs/feature/demo/05-casos-de-teste-browser.md", "## CT-B01: Consultar total\n")
        self.write("wikis/specs/feature/demo/08-roteiro-teste-manual.md", f"""# Roteiro de teste manual
## Fluxos
### RM-01 — Consultar total · Via: terminal
**Origem**: CT-01, CT-B01

| # | Ação | Resultado esperado | Origem |
|---|---|---|---|
| 1 | Consultar total | {expected} | {origin} |
""")

    def test_manual_valid(self):
        self.manual_fixture()
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 0)
        self.assertEqual(result.stdout + result.stderr, "")

    def test_manual_yes_without_script(self):
        self.manual_fixture()
        (self.wiki / "08-roteiro-teste-manual.md").unlink()
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("03-progresso.md:3: Roteiro manual: sim", result.stdout)

    def test_manual_no_with_script(self):
        self.manual_fixture(decision="não")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("03-progresso.md:3: Roteiro manual: não", result.stdout)

    def test_manual_empty_expected_result(self):
        self.manual_fixture(expected=" ")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("08-roteiro-teste-manual.md:8: Resultado esperado vazio", result.stdout)

    def test_manual_origin_without_id(self):
        self.manual_fixture(origin="fluxo principal")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("08-roteiro-teste-manual.md:8: Origem sem ID", result.stdout)

    def test_manual_unknown_ct(self):
        self.manual_fixture(origin="CT-99")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("CT-99 citado no 08, sem cenário", result.stdout)

    def test_manual_obsolete_ct(self):
        for definition in ("@obsoleto\nCenário: [CT-01] total antigo\n",
                           "| ~~CT-01~~ | R1 |\n", "| CT-01 | fundido em CT-02 |\n"):
            with self.subTest(definition=definition):
                self.manual_fixture()
                self.write("wikis/specs/feature/demo/04-casos-de-teste.md", definition)
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, 1)
                self.assertIn("CT-01 citado no 08, mas o cenário está @obsoleto/riscado/fundido", result.stdout)

    def test_manual_obsolete_browser_title(self):
        self.manual_fixture()
        self.write("wikis/specs/feature/demo/05-casos-de-teste-browser.md",
                   "@obsoleto\n## CT-B01: Consultar total antigo\n")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("CT-B01 citado no 08, mas o cenário está @obsoleto/riscado/fundido", result.stdout)

    def test_manual_commented_ct_is_not_definition(self):
        for filename, definition, identifier in (
                ("04-casos-de-teste.md", "Cenário: [CT-01] total", "CT-01"),
                ("05-casos-de-teste-browser.md", "## CT-B01: Consultar total", "CT-B01")):
            with self.subTest(identifier=identifier):
                self.manual_fixture()
                self.write(f"wikis/specs/feature/demo/{filename}", f"<!--\n{definition}\n-->\n")
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, 1)
                self.assertIn(f"{identifier} citado no 08, sem cenário", result.stdout)

    def test_manual_duplicate_rm(self):
        self.manual_fixture()
        path = self.wiki / "08-roteiro-teste-manual.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n### RM-01 — Repetido\n", encoding="utf-8")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("RM-01 duplicado — definido antes na linha 3", result.stdout)

    def test_manual_legacy_without_decision_or_script(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", "# Progresso legado\n")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 0)
        self.assertEqual(result.stdout + result.stderr, "")

    def test_manual_missing_wiki(self):
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.work / "ausente"), 2)

    def test_manual_usage(self):
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh"), 2)
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki, "extra"), 2)

    def test_manual_last_decision_wins(self):
        for previous, current in (("não", "sim"), ("sim", "não")):
            with self.subTest(previous=previous, current=current):
                self.manual_fixture()
                self.write("wikis/specs/feature/demo/03-progresso.md",
                           f"Roteiro manual: {previous} — decisão anterior\n\n"
                           f"Roteiro manual: {current} — pedido tardio\n")
                if current == "não":
                    (self.wiki / "08-roteiro-teste-manual.md").unlink()
                self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_manual_comments_and_examples_are_not_decisions(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", """Roteiro manual: não — sem necessidade
## Verificação Final
<!-- só com roteiro manual: sim -->
<!-- Exemplo:
Roteiro manual: sim
-->
```markdown
Roteiro manual: sim — exemplo
```
""")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 0)
        self.assertEqual(result.stdout + result.stderr, "")

    def test_manual_missing_php(self):
        path = ROOT / ".ai/skills/feature-wiki/scripts/roteiro-manual.sh"
        result = subprocess.run([BASH, str(path), str(self.wiki)], cwd=self.work,
                                env=dict(os.environ, PATH=str(self.work)),
                                text=True, encoding="utf-8", capture_output=True, timeout=60)
        self.assert_exit(result, 2)
        self.assertIn("php não está no PATH", result.stderr)

    def test_manual_scenario_definition_formats(self):
        for definition in ("Esquema do Cenário: [CT-01] total\n", "| CT-01 | R1 |\n"):
            with self.subTest(definition=definition):
                self.manual_fixture()
                self.write("wikis/specs/feature/demo/04-casos-de-teste.md", definition)
                self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_manual_ct_in_prose_must_exist(self):
        self.manual_fixture()
        path = self.wiki / "08-roteiro-teste-manual.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nFora deste roteiro: CT-B99.\n", encoding="utf-8")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("CT-B99 citado no 08, sem cenário", result.stdout)

    def test_manual_rq_and_p_need_definition_in_correct_section(self):
        self.manual_fixture(origin="RQ-99, P-99")
        self.write("wikis/specs/feature/demo/00-requisito.md", """## Decomposição em Cláusulas
| ID | Cláusula |
|---|---|
| RQ-01 | Total |
| P-99 | Premissa fora da seção |
## Perguntas ao Solicitante
| ID | Afeta |
|---|---|
| RQ-99 | Só menção, não definição |
""")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("RQ-99 citado no 08, sem definição na decomposição do 00", result.stdout)
        self.assertIn("P-99 citado no 08, sem definição em ## Premissas do 00", result.stdout)

    def test_manual_commented_rq_and_p_are_not_definitions(self):
        self.manual_fixture()
        self.write("wikis/specs/feature/demo/00-requisito.md", """## Decomposição em Cláusulas
<!--
| ID | Cláusula | Estado |
|---|---|---|
| RQ-01 | Total exato | fechada |
-->
## Premissas
<!--
| ID | Premissa | Estado |
|---|---|---|
| P-01 | Exibir o total | vigente |
-->
""")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertIn("RQ-01 citado no 08, sem definição na decomposição do 00", result.stdout)
        self.assertIn("P-01 citado no 08, sem definição em ## Premissas do 00", result.stdout)

    def test_manual_rq_from_addendum(self):
        self.manual_fixture(origin="RQ-02")
        path = self.wiki / "00-requisito.md"
        path.write_text(path.read_text(encoding="utf-8") + """
## Adendo 1 — 2026-10-20
### Texto Original
> Aceitar o total.
### Decomposição
| ID | Cláusula | Substitui |
|---|---|---|
| RQ-02 | Aceitar total | — |
""", encoding="utf-8")
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_manual_escaped_pipe_and_no_command_execution(self):
        self.manual_fixture(expected="A saída é 10 \\| total")
        path = self.wiki / "08-roteiro-teste-manual.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n```bash\ntouch executou-comando\n```\n",
                        encoding="utf-8")
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)
        self.assertFalse((self.work / "executou-comando").exists())

    def test_manual_noncurrent_rq(self):
        for state in ("substituída por RQ-02 (Adendo 1)", "decomposta em RQ-02, RQ-03"):
            with self.subTest(state=state):
                self.manual_fixture()
                path = self.wiki / "00-requisito.md"
                path.write_text(path.read_text(encoding="utf-8").replace("fechada", state), encoding="utf-8")
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, 1)
                self.assertEqual(len(result.stdout.splitlines()), 1)
                self.assertIn("RQ-01 citado no 08, mas não vigente", result.stdout)

    def test_manual_noncurrent_p(self):
        for state in ("substituída por P-02", "promovida a RQ-02 (Adendo 1)", "revogada — sem efeito"):
            with self.subTest(state=state):
                self.manual_fixture()
                path = self.wiki / "00-requisito.md"
                path.write_text(path.read_text(encoding="utf-8").replace("vigente", state), encoding="utf-8")
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, 1)
                self.assertEqual(len(result.stdout.splitlines()), 1)
                self.assertIn("P-01 citado no 08, mas não vigente", result.stdout)

    def test_manual_open_rq_is_reading_only(self):
        self.manual_fixture()
        path = self.wiki / "00-requisito.md"
        path.write_text(path.read_text(encoding="utf-8").replace("fechada", "aberta — Q1"), encoding="utf-8")
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_manual_addendum_replaces_rq(self):
        for replacement, code in (("RQ-01", 1), ("RQ-01 (parcial)", 0)):
            with self.subTest(replacement=replacement):
                self.manual_fixture()
                path = self.wiki / "00-requisito.md"
                path.write_text(path.read_text(encoding="utf-8") + f"""
## Adendo 1 — 2026-10-20
### Decomposição
| ID | Cláusula | Substitui |
|---|---|---|
| RQ-02 | Novo total | {replacement} |
""", encoding="utf-8")
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, code)
                if code:
                    self.assertIn("RQ-01 citado no 08, mas não vigente", result.stdout)

    def test_manual_struck_decision_below_current_is_history(self):
        for current, old in (("sim", "não"), ("não", "sim")):
            with self.subTest(current=current):
                self.manual_fixture()
                self.write("wikis/specs/feature/demo/03-progresso.md",
                           f"Roteiro manual: {current}\n~~Roteiro manual: {old}~~\n")
                if current == "não":
                    (self.wiki / "08-roteiro-teste-manual.md").unlink()
                self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_manual_ids_in_comments_and_fences_are_ignored(self):
        self.manual_fixture()
        path = self.wiki / "08-roteiro-teste-manual.md"
        path.write_text(path.read_text(encoding="utf-8") + """
<!-- RQ-99 P-99 CT-99 CT-B99 -->
<!--
### RM-01 — Exemplo comentado CT-98
| Resultado esperado | Origem |
|-|-|
| | |
-->
```markdown
RQ-97 P-97 CT-97 CT-B97
### RM-01 — Exemplo cercado
| Resultado esperado | Origem |
|-|-|
| | |
```
~~~text
RQ-96 P-96 CT-96 CT-B96
~~~
````markdown
```text
RQ-95 P-95 CT-95 CT-B95
```
~~~~
RQ-94 P-94 CT-94 CT-B94
````
""", encoding="utf-8")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 0)
        self.assertEqual(result.stdout + result.stderr, "")

    def test_manual_header_prefixes(self):
        self.manual_fixture(expected=" ")
        path = self.wiki / "08-roteiro-teste-manual.md"
        path.write_text(path.read_text(encoding="utf-8").replace("Resultado esperado | Origem",
                        "Resultado esperado (Então) | Origem (CT/RQ)"), encoding="utf-8")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertEqual(len(result.stdout.splitlines()), 1)
        self.assertIn("Resultado esperado vazio", result.stdout)

    def test_manual_single_dash_separator(self):
        self.manual_fixture(expected=" ")
        self.write("wikis/specs/feature/demo/08-roteiro-teste-manual.md",
                   "| Resultado esperado | Origem |\n|-|-|\n| | RQ-01 |\n")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertEqual(len(result.stdout.splitlines()), 1)
        self.assertIn("Resultado esperado vazio", result.stdout)

    def test_manual_table_decision_without_08(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", "| Roteiro manual | sim |\n")
        result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
        self.assert_exit(result, 1)
        self.assertEqual(len(result.stdout.splitlines()), 1)
        self.assertIn("Roteiro manual: sim, mas 08-roteiro-teste-manual.md não existe", result.stdout)

    def test_manual_08_without_decision(self):
        for progress in ("# Progresso\n", None):
            with self.subTest(progress=progress):
                self.manual_fixture()
                path = self.wiki / "03-progresso.md"
                if progress is None:
                    path.unlink()
                else:
                    path.write_text(progress, encoding="utf-8")
                result = self.script("feature-wiki", "roteiro-manual.sh", self.wiki)
                self.assert_exit(result, 1)
                self.assertEqual(len(result.stdout.splitlines()), 1)
                self.assertIn("08 existe, mas não há decisão Roteiro manual no 03", result.stdout)

    def test_manual_template_03_model_is_not_decision(self):
        template = (ROOT / ".ai/skills/feature-wiki/references/template-03-progresso.md").read_text(encoding="utf-8")
        body = template.split("```markdown\n", 1)[1].rsplit("```", 1)[0]
        self.assertRegex(body, r"(?s)<!--(?:(?!-->).)*Roteiro manual:.*?-->")
        self.write("wikis/specs/feature/demo/03-progresso.md", body)
        self.assert_exit(self.script("feature-wiki", "roteiro-manual.sh", self.wiki), 0)

    def test_checkbox_evidence(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", "- [x] Teste — comando: exit 0\n")
        self.assert_exit(self.script("feature-wiki", "checkbox-sem-evidencia.sh", self.wiki), 0)

    def test_checkbox_missing_evidence(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", "- [x] Teste\n")
        self.assert_exit(self.script("feature-wiki", "checkbox-sem-evidencia.sh", self.wiki), 1)

    def test_ids_match(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php it('[CT-01] total', function () {});\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 0)

    def test_ids_comment_is_not_test(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php // [CT-01] ainda não implementado\n")
        result = self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php")
        self.assert_exit(result, 1)
        self.assertIn("CT-01 sem teste", result.stdout)

    def test_ids_unknown(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php it('[CT-99] total', function () {});\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 1)

    def test_ids_fixture_string_is_not_test(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php $fixture = '[CT-01]'; it('outro', function () {});\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 1)

    def test_ids_method_is_not_test(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php $fixture->test('[CT-01]');\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 1)

    def test_ids_constructor_is_not_test(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php new test('[CT-01]'); testdox('[CT-01]');\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 1)

    def test_ids_attribute_is_not_test(self):
        self.trace_fixture()
        self.write("tests/Feature/Demo/Test.php", "<?php #[Example, test('[CT-01] dado')] function fixture() {}\n")
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 1)

    def test_dark_inline_media(self):
        self.write("resources/views/demo.blade.php", "<style>@media (prefers-color-scheme: dark) { body {color: white} }</style>\n")
        result = self.script("feature-quality-gate", "dark-mode.sh", "--mecanismo")
        self.assert_exit(result, 1)
        self.assertIn("prefers-color-scheme", result.stdout)

    def test_ids_empty_glob(self):
        self.trace_fixture()
        self.assert_exit(self.script("feature-wiki", "ids-ct.sh", self.wiki, "tests/**/*.php"), 2)

    def rules_fixture(self):
        self.write("wikis/specs/feature/demo/03-progresso.md", "## Conformidade com Rules\n")
        self.write(".ai/rules/models.md", "---\npaths:\n  - app/Models/*.php\n---\n# Regra\n")
        self.init_git()

    def test_rules_clean(self):
        self.rules_fixture()
        self.assert_exit(self.script("feature-wiki", "conformidade-rules.sh", self.wiki, "main"), 0)

    def check_rules_change(self, mode):
        self.rules_fixture()
        path = "app/Models/Novo.php" if mode == "untracked" else "app/Models/Demo.php"
        self.write(path, "<?php // alteração\n")
        if mode == "staged":
            self.git("add", path)
        elif mode == "committed":
            self.git("switch", "-c", "feature")
            self.git("add", path)
            self.git("commit", "-m", "change")
        result = self.script("feature-wiki", "conformidade-rules.sh", self.wiki, "main")
        self.assert_exit(result, 1)
        self.assertIn("models.md casa", result.stdout)

    def test_rules_unstaged(self):
        self.check_rules_change("unstaged")

    def test_rules_staged(self):
        self.check_rules_change("staged")

    def test_rules_untracked(self):
        self.check_rules_change("untracked")

    def test_rules_committed(self):
        self.check_rules_change("committed")

    def test_weak_oracle(self):
        path = self.write("tests/Weak.php", "<?php it('abre', function () { $this->get('/')->assertOk(); });\n")
        self.assert_exit(self.script("feature-quality-gate", "k1-oraculo-fraco.sh", path), 1)

    def test_strong_oracle(self):
        path = self.write("tests/Strong.php", "<?php it('total', function () { expect(10)->toBe(10); });\n")
        self.assert_exit(self.script("feature-quality-gate", "k1-oraculo-fraco.sh", path), 0)

    def test_tickets_explicit_codex(self):
        path = ROOT / ".ai/skills/feature-tickets/agents/openai.yaml"
        self.assertTrue(path.is_file(), "Codex precisa de política explícita própria")
        self.assertRegex(path.read_text(encoding="utf-8"), r"allow_implicit_invocation:\s*false\b")

    def test_codex_roles(self):
        roles = list(ROOT.glob(".ai/skills/*/agents/codex/*.toml"))
        self.assertEqual(len(roles), 5)
        names = set()
        for path in roles:
            config = tomllib.loads(path.read_text(encoding="utf-8"))
            for key in ("name", "description", "developer_instructions"):
                self.assertTrue(config.get(key), f"{path}: {key}")
            self.assertNotIn(config["name"], names)
            names.add(config["name"])
            self.assertNotIn("model", config, "Não fixar provedor/modelo nas rotas portáveis")
            self.assertIn(config["sandbox_mode"], ("read-only", "workspace-write"))


HOOK_CASES = [
    ("revisor-diff", 2, "Read", {"file_path": "wikis/specs/b/f/01-plano-acao.md"}),
    ("revisor-diff", 0, "Read", {"file_path": "app/Models/X.php"}),
    ("revisor-diff", 2, "Bash", {"command": "git diff main...HEAD"}),
    ("revisor-diff", 0, "Bash", {"command": "git diff main...HEAD -- . ':(exclude)wikis'"}),
    ("adversario-ct", 0, "Read", {"file_path": "wikis/specs/b/f/00-requisito.md"}),
    ("adversario-ct", 2, "Read", {"file_path": "app/Models/X.php"}),
    ("executor-ct", 2, "Edit", {"file_path": "app/Models/X.php"}),
    ("executor-ct", 0, "Edit", {"file_path": "tests/Feature/X.php"}),
    ("executor-ctb", 2, "Write", {"file_path": "database/migrations/x.php"}),
    ("qa-gate", 0, "Read", {"file_path": "wikis/specs/b/f/03-progresso.md"}),
    ("qa-gate", 2, "Bash", {"command": "git stash"}),
    ("desconhecido", 2, "Read", {"file_path": "app/Models/X.php"}),
]


def add_generated_tests():
    for number, (profile, expected, tool, data) in enumerate(HOOK_CASES, 1):
        def test(self, profile=profile, expected=expected, tool=tool, data=data):
            result = self.script("feature-wiki", "guarda-subagente.sh", profile,
                                 stdin=json.dumps({"tool_name": tool, "tool_input": data}))
            self.assert_exit(result, expected)
        setattr(CollectionTests, f"test_hook_{number:02d}_{profile}", test)
    for path in ROOT.glob(".ai/skills/*/scripts/*.sh"):
        def test(self, path=path):
            self.assertNotIn(b"\r", path.read_bytes(), "Bash exige LF")
            self.assert_exit(run([BASH, "-n", str(path)], self.work), 0)
        setattr(CollectionTests, "test_syntax_" + path.stem.replace("-", "_"), test)


class Result(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed.append(test.id().rsplit(".", 1)[-1])


def metrics():
    skills = {}
    for path in sorted(ROOT.glob(".ai/skills/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        front, body = text.split("---", 2)[1:]
        match = re.search(r"description:\s*>[^\n]*\n((?:[ \t]+[^\n]*\n)+)", front)
        description = " ".join(line.strip() for line in match[1].splitlines()) if match else ""
        skills[path.parent.name] = {"body_lines": len(body.strip().splitlines()),
                                    "description_chars": len(description), "bytes": path.stat().st_size}
    return skills


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path)
    options = parser.parse_args()
    ROOT = options.root.resolve()
    if not BASH or not Path(BASH).is_file() or not shutil.which("php"):
        parser.error("Instale Bash e PHP no PATH; no Windows use Git Bash ou SKILLS_BASH.")
    add_generated_tests()
    started = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CollectionTests))
    report = {"root": str(ROOT), "instrument_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "tests": result.testsRun, "passed": sorted(result.passed),
              "failed": [{"test": test.id().rsplit(".", 1)[-1], "traceback": detail}
                         for test, detail in result.failures + result.errors],
              "skipped": result.skipped, "seconds": round(time.monotonic() - started, 3),
              "skills": metrics()}
    if options.report:
        options.report.parent.mkdir(parents=True, exist_ok=True)
        options.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(not result.wasSuccessful())
