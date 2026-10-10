"""Prepare disposable, symmetric Laravel copies without old experimental outputs.

Dependency files are hard-linked only in the runtime copy and must remain immutable.
No source .env, databases, logs, agent settings or caches are copied.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[2]
ROUND = Path(__file__).resolve().parent
SOURCE = Path(r"D:\PROJECTS\SKILLS\demo-r8")
BASE = Path(r"D:\PROJECTS\SKILLS\blind-20261009")
BASELINE = "6e9222c0f12769795dd4321e4f47f6509dbc2d9e"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ignored(directory, names):
    return {name for name in names if name in {
        "vendor", "node_modules", ".git", ".env", ".env.docker", "storage",
        ".agents", ".claude", ".codex", ".junie", "CLAUDE.md", ".mcp.json",
        "opencode.json", "specs", "skills", "ExpA", "ExpB", "ExpC", "ExpD", "ExpE",
    } or name.startswith("Exp") or name.endswith((".sqlite", ".sqlite3"))
        or (Path(directory).name == "cache" and name.endswith(".php"))}


def main():
    BASE.mkdir(exist_ok=False)
    snapshot = BASE / "snapshots"
    snapshot.mkdir()
    archive = snapshot / "baseline.tar"
    subprocess.run(["git", "archive", BASELINE, "-o", str(archive), ".ai/skills"], cwd=REPO, check=True)
    import tarfile
    with tarfile.open(archive) as tar:
        tar.extractall(snapshot / "old", filter="data")
    shutil.copytree(REPO / ".ai/skills", snapshot / "new/.ai/skills")
    records = {}
    for label, version in (("project-71", "old"), ("project-26", "new")):
        target = BASE / label
        shutil.copytree(SOURCE, target, ignore=ignored)
        shutil.copytree(snapshot / version / ".ai/skills", target / ".ai/skills", dirs_exist_ok=True)
        for sub in ("storage/framework/cache/data", "storage/framework/sessions", "storage/framework/views", "storage/logs", "bootstrap/cache"):
            (target / sub).mkdir(parents=True, exist_ok=True)
        (target / ".env").write_text("APP_ENV=testing\nAPP_KEY=base64:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\nDB_CONNECTION=sqlite\nDB_DATABASE=:memory:\nCACHE_STORE=array\nSESSION_DRIVER=array\nQUEUE_CONNECTION=sync\nMAIL_MAILER=array\nBROADCAST_CONNECTION=null\nPULSE_ENABLED=false\nKIT_TENANCY=false\n", encoding="utf-8")
        for scenario in ("cenario-1-cupons", "cenario-2-aprovacao"):
            feature = "cupons-de-desconto" if scenario.startswith("cenario-1") else "aprovacao-de-compra"
            shutil.copytree(REPO / "experimentos/protocolo/oraculo-fixo" / scenario, target / "wikis/specs/oraculo" / feature)
        records[label] = {"snapshot": version, "files": {str(p.relative_to(target)): digest(p) for p in (target / ".ai/skills").rglob("*") if p.is_file()}}
    runtime = BASE / "runtime"
    shutil.copytree(BASE / "project-26", runtime)
    shutil.copytree(SOURCE / "vendor", runtime / "vendor", copy_function=os.link)
    # Autoload metadata can be regenerated locally; never mutate shared dependencies.
    for p in (runtime / "vendor/composer").iterdir():
        if p.is_file():
            contents = p.read_bytes()
            p.unlink()
            p.write_bytes(contents)
    records["environment"] = {"source": str(SOURCE), "runtime": str(runtime), "composer_lock_sha256": digest(SOURCE / "composer.lock"), "baseline_commit": BASELINE, "read_isolation": "fresh context and explicit path contract; filesystem reads are not sandbox-isolated"}
    ROUND.mkdir(exist_ok=True)
    (ROUND / "preparacao.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"base": str(BASE), "projects": ["project-71", "project-26"], "runtime": str(runtime)}))


if __name__ == "__main__":
    main()
