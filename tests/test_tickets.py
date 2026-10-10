import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(os.environ.get("SKILLS_ROOT", Path(__file__).resolve().parents[1]))
SCRIPTS = REPO / ".ai/skills/feature-tickets/scripts"
BASH = (
    str(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe")
    if os.name == "nt"
    else shutil.which("bash")
)

REQUISITO = """# Requisito
| ID | Cláusula | Estado |
|---|---|---|
| RQ-01 | Fazer X | fechada |
"""
PLANO = """## Cobertura do Requisito
| RQ | Passo | Observação |
|---|---|---|
| RQ-01 | 1 | — |
## Estrutura de Implementação
### 1. Fazer X
**Atende**: RQ-01
"""
CASOS = """## Mapa de Regras
| Regra | Origem | Cenário |
|---|---|---|
| R1 | RQ-01 | CT-01 |
## Costuras de Teste
| Grupo | Costura |
|---|---|
| X | Pest feature HTTP |
## Índice de Cenários
| ID | Regra | Grupo | Costura |
|---|---|---|---|
| CT-01 | R1 | X | Pest feature HTTP |
Cenário: [CT-01] faz X
"""
PROGRESSO = """## Tickets
Fatiamento confirmado: 2026-10-09 — usuário — 1, 1
- [ ] [01](07-tickets/01-faz-x.md) faz X — pronto
"""
TICKET = """# 01: Faz X
**Entrega**: faz X
**RQ cobertas**: RQ-01
**CT que ficam verdes**: CT-01
**CT-B**: —
**Passos do 01 envolvidos**: 1
**Bloqueado por**: —
**Bloqueia**: —
**Prefactoring**: não
**Costura**: X — Pest feature HTTP
**Status**: pronto
"""


class TicketsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BASH or not Path(BASH).is_file() or not shutil.which("php"):
            raise RuntimeError("Os testes dos scripts exigem Bash e PHP no PATH.")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-tickets-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.wiki = self.root / "wikis/specs/b/f"
        (self.wiki / "07-tickets").mkdir(parents=True)
        self.ticket = self.wiki / "07-tickets/01-faz-x.md"
        self.write(self.wiki / "00-requisito.md", REQUISITO)
        self.write(self.wiki / "01-plano-acao.md", PLANO)
        self.write(self.wiki / "04-casos-de-teste.md", CASOS)
        self.write(self.wiki / "03-progresso.md", PROGRESSO)
        self.write(self.ticket, TICKET)

    def write(self, path, content):
        path.write_bytes(content.encode("utf-8"))

    def run_script(self, name, *args, env=None):
        return subprocess.run(
            [BASH, str(SCRIPTS / name), *args],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )

    def check(self):
        return self.run_script("indice.sh", "--check", "wikis/specs/b/f")

    def test_valid_ticket(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")

    def test_status_prefix_is_not_an_enum_value(self):
        for status in ("prontooo", "em execução extra", "em revisãofoo", "concluídofoo"):
            with self.subTest(status=status):
                self.write(self.ticket, TICKET.replace("Status**: pronto", "Status**: " + status))
                result = self.check()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Status fora do enum", result.stdout)
                quadro = self.run_script("indice.sh", "--status", "wikis/specs/b/f")
                self.assertNotIn("fronteira: 01", quadro.stdout)

    def test_progress_status_prefix_is_rejected(self):
        self.write(self.wiki / "03-progresso.md", PROGRESSO.replace("pronto", "prontooo"))
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("ticket 01", result.stdout)

    def test_ct_without_rule_is_rejected(self):
        self.write(self.wiki / "04-casos-de-teste.md", CASOS.replace("| CT-01 | R1 |", "| CT-01 | — |"))
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CT-01 sem origem RQ/P-nn", result.stdout)

    def test_ct_without_requirement_origin_is_rejected(self):
        self.write(self.wiki / "04-casos-de-teste.md", CASOS.replace("| R1 | RQ-01 |", "| R1 | — |"))
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CT-01 sem origem RQ/P-nn", result.stdout)

    def test_mirror_records_issue_once_for_every_accepted_status_format(self):
        fake = self.root / "fake"
        fake.mkdir()
        gh = fake / "gh"
        self.write(gh, """#!/usr/bin/env bash
if [ "$1" = auth ] && [ "$2" = status ]; then exit 0; fi
if [ "$1" = issue ] && [ "$2" = create ]; then
  cat >/dev/null
  printf 'create\n' >> "$FT_TEST_GH_LOG"
  printf 'https://github.com/o/r/issues/41\n'
  exit 0
fi
exit 9
""")
        gh.chmod(0o755)
        env = os.environ.copy()
        env["PATH"] = str(fake) + os.pathsep + env["PATH"]
        log = self.root / "gh-calls"
        env["FT_TEST_GH_LOG"] = log.as_posix()
        for status in ("  **Status**: pronto", "**Status:** pronto", "**Status ** : pronto"):
            for eol in ("\n", "\r\n"):
                with self.subTest(status=status, eol=repr(eol)):
                    self.write(self.ticket, TICKET.replace("**Status**: pronto", status).replace("\n", eol))
                    self.write(log, "")
                    self.assertEqual(self.check().returncode, 0)
                    for _ in range(2):
                        result = self.run_script(
                            "espelho-gh.sh", "wikis/specs/b/f", "--repo", "o/r", "--aplicar", env=env
                        )
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    data = self.ticket.read_bytes()
                    self.assertEqual(data.count(b"**Issue**: o/r#41"), 1)
                    self.assertEqual(log.read_text().splitlines(), ["create"])
                    self.assertEqual(data.count(b"\r\n"), data.count(b"\n") if eol == "\r\n" else 0)


if __name__ == "__main__":
    unittest.main()
