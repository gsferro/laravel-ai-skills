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
