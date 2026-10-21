"""Parte 2 da rodada 2026-10-20: geração do 08 sobre implementação real, juiz cego e L8.

Uso (na raiz do repositório):
  python experimentos/2026-10-20-roteiro-manual/lab2.py prepare        # G1, G2
  python experimentos/2026-10-20-roteiro-manual/lab2.py run G1 G2
  python experimentos/2026-10-20-roteiro-manual/lab2.py integrity      # hashes antes × depois
  python experimentos/2026-10-20-roteiro-manual/lab2.py judge          # J1, J2
  python experimentos/2026-10-20-roteiro-manual/lab2.py prepare_l8     # L8-C, L8-P (após plantar)
  python experimentos/2026-10-20-roteiro-manual/lab2.py run_l8

Isolamento procedimental; filesystem não isolado. vendor/ por hard link deve permanecer imutável.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tarfile

ROUND = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lab", ROUND / "lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)
REPO, SOURCE, MODEL, EFFORT, CODEX, BASH = lab.REPO, lab.SOURCE, lab.MODEL, lab.EFFORT, lab.CODEX, lab.BASH
LAB = Path(r"D:\PROJECTS\SKILLS\blind-20261020-p2")
TREATMENT = "cb2b45e"
REF = REPO / "experimentos/2026-10-09-projeto-real/referencia-v3"
STATE = ROUND / "parte2-preparacao.json"
CELLS = {"G1": (1, "cupons-de-desconto", "cenario-1-cupons", "FERRO-812 — Cupons de desconto"),
         "G2": (2, "aprovacao-de-compra", "cenario-2-aprovacao", "FERRO-830 — Fluxo de aprovação de solicitação de compra")}
SKIP_HASH = ("vendor/", "node_modules/", "storage/", "bootstrap/cache/", "validation/")


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree_hashes(root):
    out = {}
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and not rel.startswith(SKIP_HASH) and not rel.endswith((".sqlite", ".sqlite3")):
            out[rel] = digest(p)
    return out


def load():
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else {"cells": {}}


def save(s):
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def snapshot():
    snap = LAB / "snapshot"
    if snap.exists():
        return snap
    snap.mkdir(parents=True)
    tar = LAB / "skills.tar"
    subprocess.run(["git", "archive", TREATMENT, "-o", str(tar), ".ai/skills"], cwd=REPO, check=True)
    with tarfile.open(tar) as t:
        t.extractall(snap, filter="data")
    for p in snap.rglob("*"):
        if p.is_file() and p.suffix != ".cmd":
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
    return snap


def make_project(cell, wiki_from=None):
    snap = snapshot()
    label = "proj-" + secrets.token_hex(3)
    target = LAB / label
    shutil.copytree(SOURCE, target, ignore=lab.ignored)
    shutil.copytree(snap / ".ai/skills", target / ".ai/skills", dirs_exist_ok=True)
    for sub in ("app", "config", "database", "tests"):
        shutil.copytree(REF / sub, target / sub, dirs_exist_ok=True)
    for sub in ("storage/framework/cache/data", "storage/framework/sessions", "storage/framework/views",
                "storage/logs", "storage/app/public", "bootstrap/cache"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    for keep in ("main", "feature"):
        shutil.copytree(SOURCE / "wikis/specs" / keep, target / "wikis/specs" / keep)
    shutil.copytree(SOURCE / "vendor", target / "vendor", copy_function=os.link)
    for p in (target / "vendor/composer").iterdir():
        if p.is_file():
            data = p.read_bytes()
            p.unlink()
            p.write_bytes(data)
    (target / ".env").write_text(
        "APP_NAME=Kit\nAPP_ENV=local\nAPP_DEBUG=true\nAPP_URL=http://127.0.0.1:8000\n"
        "APP_KEY=base64:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\nDB_CONNECTION=sqlite\nDB_DATABASE=:memory:\n"
        "CACHE_STORE=array\nSESSION_DRIVER=file\nQUEUE_CONNECTION=sync\nMAIL_MAILER=log\n"
        "BROADCAST_CONNECTION=null\nPULSE_ENABLED=false\nKIT_TENANCY=false\n", encoding="utf-8")
    if wiki_from is not None:
        shutil.copytree(wiki_from, target / "wikis/specs" / wiki_from.parent.name / wiki_from.name)
    return label, target


def write_wiki(target, cell):
    n, feature, oracle, card = CELLS[cell]
    wiki = target / "wikis/specs" / f"saida-g{n}" / feature
    wiki.mkdir(parents=True)
    for name in ("00-requisito.md", "01-plano-acao.md"):
        shutil.copyfile(REPO / "experimentos/protocolo/oraculo-fixo" / oracle / name, wiki / name)
    for p in (ROUND / "conjuntos" / f"R-B-C{n}").glob("0[45]-*.md"):
        shutil.copyfile(p, wiki / p.name)
    (wiki / "03-progresso.md").write_text(
        f"# Progresso — {card}\n\n**Estado**: em revisão\n\n## Auditoria Pré-Implementação\n\n"
        "Roteiro manual: sim — 2026-10-20 — instrução explícita do desenvolvedor — homologação manual pedida\n\n"
        "## Revisão do Diff (step 9)\n\n- [x] Revisão do diff concluída — sem achados abertos, 2026-10-20\n\n"
        "## Verificação Final\n\n- [x] Reconciliação do step 10 concluída — fontes reconciliadas, 2026-10-20\n",
        encoding="utf-8", newline="\n")
    return wiki


def prepare():
    LAB.mkdir(exist_ok=True)
    s = load()
    for cell in CELLS:
        label, target = make_project(cell)
        wiki = write_wiki(target, cell)
        s["cells"][cell] = {"label": label, "wiki": str(wiki.relative_to(target)),
                            "before": tree_hashes(target)}
        print(cell, label)
    s.update({"lab": str(LAB), "treatment": TREATMENT, "reference": str(REF.relative_to(REPO)),
              "skills_sha256": {p.relative_to(LAB / "snapshot").as_posix(): digest(p)
                                for p in (LAB / "snapshot").rglob("*") if p.is_file()}})
    save(s)


def run_one(cell, prompt_file, extra=None):
    s = load()
    c = s["cells"][cell]
    project = LAB / c["label"]
    raw = (ROUND / "instrumentos" / prompt_file).read_text(encoding="utf-8")
    body = raw.split("## Prompt\n", 1)[1]
    text = "\n".join(re.sub(r"^> ?", "", l) for l in body.strip().splitlines())
    text = text.replace("{PROJETO}", str(project)).replace("{WIKI}", str(project / c["wiki"]))
    out = ROUND / "execucoes" / cell
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompt.md").write_text(text, encoding="utf-8")
    with open(out / "eventos.jsonl", "w", encoding="utf-8") as log:
        res = subprocess.run([CODEX, "exec", "--dangerously-bypass-approvals-and-sandbox", "--json",
                              "-m", MODEL, "-c", f'model_reasoning_effort="{EFFORT}"',
                              "-C", str(project), "-o", str(out / "retorno.md"), "-"],
                             input=text, text=True, encoding="utf-8", stdout=log,
                             stderr=subprocess.STDOUT, timeout=4 * 3600)
    (out / "exit.txt").write_text(str(res.returncode), encoding="utf-8")
    return cell, res.returncode


def run(cells, prompt_file="PROMPT-BRACO-ROTEIRO.md"):
    with ThreadPoolExecutor(max_workers=2) as pool:
        for cell, code in pool.map(lambda c: run_one(c, prompt_file), cells):
            print(cell, code, flush=True)


def integrity():
    s = load()
    report = {}
    for cell, c in s["cells"].items():
        project = LAB / c["label"]
        after = tree_hashes(project)
        before = c["before"]
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        report[cell] = changed
        print(cell, changed)
    (ROUND / "parte2-integridade.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def judge(cells=("G1", "G2")):
    s = load()
    raw = (ROUND / "instrumentos/PROMPT-JUIZ-ROTEIRO.md").read_text(encoding="utf-8")
    prompt = "\n".join(re.sub(r"^> ?", "", l) for l in raw.split("## Prompt\n", 1)[1].strip().splitlines())
    jobs = []
    for cell in cells:
        c = s["cells"][cell]
        wiki = LAB / c["label"] / c["wiki"]
        d = LAB / "judges" / ("j-" + secrets.token_hex(3))
        d.mkdir(parents=True)
        shutil.copyfile(wiki / "00-requisito.md", d / "requisito.md")
        casos = [wiki / "04-casos-de-teste.md"] + ([wiki / "05-casos-de-teste-browser.md"]
                                                   if (wiki / "05-casos-de-teste-browser.md").is_file() else [])
        (d / "casos.md").write_text("\n\n".join(p.read_text(encoding="utf-8-sig") for p in casos), encoding="utf-8")
        roteiro = (wiki / "08-roteiro-teste-manual.md").read_text(encoding="utf-8-sig")
        roteiro = roteiro.replace(str(LAB / c["label"]), "[PROJETO]").replace(c["label"], "[PROJETO]")
        roteiro = re.sub(r"\b(?:feature-wiki|feature-test-design|feature-quality-gate)\s+v?\d+\.\d+\.\d+", "[SKILL]", roteiro)
        (d / "roteiro.md").write_text(roteiro, encoding="utf-8")
        c["judge"] = d.name
        c["judge_sha256"] = {p.name: digest(p) for p in d.iterdir()}
        jobs.append((cell, d))
    save(s)
    (ROUND / "instrumentos/prompt-juiz-roteiro-usado.md").write_text(prompt, encoding="utf-8")

    def one(job):
        cell, d = job
        out = ROUND / "vereditos-parte2"
        out.mkdir(exist_ok=True)
        res = subprocess.run([CODEX, "exec", "--dangerously-bypass-approvals-and-sandbox", "--json",
                              "--skip-git-repo-check", "-m", MODEL, "-c", f'model_reasoning_effort="{EFFORT}"',
                              "-C", str(d), "-o", str(out / f"{d.name}.md"), "-"],
                             input=prompt, text=True, encoding="utf-8", capture_output=True, timeout=3 * 3600)
        (out / f"{d.name}-eventos.jsonl").write_text(res.stdout + res.stderr, encoding="utf-8")
        return cell, d.name, res.returncode

    with ThreadPoolExecutor(max_workers=2) as pool:
        for r in pool.map(one, jobs):
            print(*r, flush=True)


def prepare_l8():
    """L8-C: 08 de G1 intacto. L8-P: 08 com defeitos plantados (arquivo preparado à mão antes)."""
    s = load()
    g1 = s["cells"]["G1"]
    wiki_src = LAB / g1["label"] / g1["wiki"]
    planted = ROUND / "parte2-l8" / "08-plantado.md"
    assert planted.is_file(), "plante os defeitos antes"
    for cell, roteiro in (("L8-C", wiki_src / "08-roteiro-teste-manual.md"), ("L8-P", planted)):
        label, target = make_project(cell)
        wiki = target / g1["wiki"]
        shutil.copytree(wiki_src, wiki)
        shutil.copyfile(roteiro, wiki / "08-roteiro-teste-manual.md")
        s["cells"][cell] = {"label": label, "wiki": g1["wiki"], "before": tree_hashes(target),
                            "roteiro_sha256": digest(wiki / "08-roteiro-teste-manual.md")}
        print(cell, label)
    save(s)


def prepare_replica():
    """G1R exploratória (fora do pré-registro): B'' = B' + template-08 corrigido da working tree."""
    global snapshot
    s = load()
    snap_r = LAB / "snapshot-r"
    shutil.copytree(snapshot(), snap_r)
    rel = ".ai/skills/feature-wiki/references/template-08-roteiro-manual.md"
    (snap_r / rel).write_bytes((REPO / rel).read_bytes().replace(b"\r\n", b"\n"))
    original = snapshot
    snapshot = lambda: snap_r
    try:
        label, target = make_project("G1R")
    finally:
        snapshot = original
    wiki = write_wiki(target, "G1")
    s["cells"]["G1R"] = {"label": label, "wiki": str(wiki.relative_to(target)), "before": tree_hashes(target),
                         "treatment": "B'' = B' + template-08 da working tree", "template_sha256": digest(snap_r / rel)}
    save(s)
    print("G1R", label)


def run_l8():
    run(["L8-C", "L8-P"], "PROMPT-GATE-L8.md")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["help"]
    if cmd == "run":
        run(rest)
    elif cmd == "judge" and rest:
        judge(tuple(rest))
    else:
        {"prepare": prepare, "integrity": integrity, "judge": judge,
         "prepare_l8": prepare_l8, "run_l8": run_l8, "prepare_replica": prepare_replica}.get(cmd, lambda: print(__doc__))()
