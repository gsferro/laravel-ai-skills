"""Rodada 2026-10-20: cópias simétricas, prompts, execução Codex, varredura e congelamento.

Uso (na raiz do repositório):
  python experimentos/2026-10-20-roteiro-manual/lab.py prepare     # congela A/B e cria as cópias
  python experimentos/2026-10-20-roteiro-manual/lab.py run [célula ...]
  python experimentos/2026-10-20-roteiro-manual/lab.py scan        # leituras fora da cópia
  python experimentos/2026-10-20-roteiro-manual/lab.py freeze      # arquiva saídas e monta juízes
  python experimentos/2026-10-20-roteiro-manual/lab.py judge
  python experimentos/2026-10-20-roteiro-manual/lab.py check       # critérios mecânicos da Parte P

Isolamento: procedimental (cópia, prompt, contexto novo). O filesystem não é isolado.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import zipfile

REPO = Path(__file__).resolve().parents[2]
ROUND = Path(__file__).resolve().parent
SOURCE = Path(r"D:\PROJECTS\SKILLS\demo-r8")
LAB = Path(r"D:\PROJECTS\SKILLS\blind-20261020")
BASELINE = "27f89eb"
MODEL = "gpt-6.1-sol"
EFFORT = "high"
CODEX = shutil.which("codex") or "codex"
BASH = "C:/Program Files/Git/bin/bash.exe" if os.name == "nt" else shutil.which("bash")

FEATURES = {1: "cupons-de-desconto", 2: "aprovacao-de-compra"}
CARDS = {1: REPO / "experimentos/protocolo/cenario-1-requisito.md",
         2: REPO / "experimentos/protocolo/cenario-2-requisito.md",
         3: ROUND / "instrumentos/cenario-3-requisito.md"}
INSTR = {"P4": "Instrução do desenvolvedor, dada junto com o card: «gere também o roteiro de teste manual»",
         "P5": "Instrução do desenvolvedor, dada junto com o card: «não quero roteiro de teste manual nesta feature»"}
# célula -> (braço, parte, cenário)
CELLS = {"R-A-C1": ("A", "R", 1), "R-A-C2": ("A", "R", 2), "R-B-C1": ("B", "R", 1), "R-B-C2": ("B", "R", 2),
         "P1": ("B", "P", 1), "P2": ("B", "P", 2), "P3": ("B", "P", 3), "P4": ("B", "P", 1),
         "P5": ("B", "P", 2), "P1-A": ("A", "P", 1), "P2-A": ("A", "P", 2)}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ignored(directory, names):
    return {name for name in names if name in {
        "vendor", "node_modules", ".git", ".env", ".env.docker", "storage",
        ".agents", ".claude", ".codex", ".junie", "CLAUDE.md", ".mcp.json",
        "opencode.json", "specs", "skills",
    } or name.startswith("Exp") or name.endswith((".sqlite", ".sqlite3"))
        or (Path(directory).name == "cache" and name.endswith(".php"))}


def state():
    return json.loads((ROUND / "preparacao.json").read_text(encoding="utf-8"))


def prepare():
    LAB.mkdir(exist_ok=False)
    snap = LAB / "snapshots"
    tar = snap / "A.tar"
    snap.mkdir()
    subprocess.run(["git", "archive", BASELINE, "-o", str(tar), ".ai/skills"], cwd=REPO, check=True)
    with tarfile.open(tar) as t:
        t.extractall(snap / "A", filter="data")
    shutil.copytree(REPO / ".ai/skills", snap / "B/.ai/skills", ignore=shutil.ignore_patterns("__pycache__"))
    # core.autocrlf=true deixa CRLF na working tree e no git archive. Normaliza A e B para os
    # bytes do blob (LF), salvo os -text do .gitattributes (pestw.cmd), para A × B diferirem só no conteúdo.
    for p in [*(snap / "A/.ai/skills").rglob("*"), *(snap / "B/.ai/skills").rglob("*")]:
        if p.is_file() and p.suffix != ".cmd":
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
    treat = ROUND / "tratamentos"
    treat.mkdir(exist_ok=False)
    manifest = {}
    for arm in ("A", "B"):
        root = snap / arm
        files = sorted(p for p in (root / ".ai/skills").rglob("*") if p.is_file())
        with zipfile.ZipFile(treat / f"{arm}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(p, p.relative_to(root).as_posix())
        manifest[arm] = {p.relative_to(root).as_posix(): digest(p) for p in files}
    manifest["source"] = {"A": f"git archive {BASELINE} .ai/skills", "B": f"working tree sobre {BASELINE}"}
    (treat / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    labels = {}
    for cell, (arm, part, scen) in CELLS.items():
        label = "proj-" + secrets.token_hex(3)
        target = LAB / label
        shutil.copytree(SOURCE, target, ignore=ignored)
        shutil.copytree(snap / arm / ".ai/skills", target / ".ai/skills", dirs_exist_ok=True)
        for sub in ("storage/framework/cache/data", "storage/framework/sessions",
                    "storage/framework/views", "storage/logs", "bootstrap/cache"):
            (target / sub).mkdir(parents=True, exist_ok=True)
        # specs/ foi ignorada inteira; repõe só as wikis de produção, nunca exp-*.
        for keep in ("main", "feature"):
            shutil.copytree(SOURCE / "wikis/specs" / keep, target / "wikis/specs" / keep)
        if part == "R":
            scen_dir = "cenario-1-cupons" if scen == 1 else "cenario-2-aprovacao"
            shutil.copytree(REPO / "experimentos/protocolo/oraculo-fixo" / scen_dir,
                            target / "wikis/specs/oraculo" / FEATURES[scen])
        assert not list((target / "wikis/specs").glob("exp-*")), "exp-* na cópia"
        assert not (target / "experimentos").exists()
        labels[cell] = label
    (ROUND / "preparacao.json").write_text(json.dumps({
        "lab": str(LAB), "source": str(SOURCE), "baseline": BASELINE, "cells": labels,
        "cell_spec": CELLS, "model": MODEL, "effort": EFFORT,
        "read_isolation": "procedural only: fresh context, prompt contract and copies; filesystem not sandboxed",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(labels, indent=2))


def prompt_for(cell, project):
    arm, part, scen = CELLS[cell]
    if part == "R":
        raw = (REPO / "experimentos/protocolo/PROMPT-BRACO.md").read_text(encoding="utf-8")
        body = raw.split("## Prompt\n", 1)[1].split("\n---\n", 1)[0]
        repl = {"{PROJETO}": str(project), "{PASTA_ORACULO}": "oraculo", "{FEATURE}": FEATURES[scen],
                "{PASTA_SAIDA}": f"saida-c{scen}", "{PERFIL}": "o que o passo 0 da skill decidir"}
    else:
        raw = (ROUND / "instrumentos/PROMPT-BRACO-STEP4.md").read_text(encoding="utf-8")
        body = raw.split("## Prompt\n", 1)[1]
        card = CARDS[scen].read_text(encoding="utf-8").strip()
        repl = {"{PROJETO}": str(project), "{PASTA}": f"saida-{cell.lower()}",
                "{INSTRUCAO_DEV}": INSTR.get(cell, "")}
        # o card entra indentado dentro do bloco citado
        body = body.replace("> {CARD}", "\n".join("> " + l if l else ">" for l in card.splitlines()))
    text = "\n".join(re.sub(r"^> ?", "", line) for line in body.strip().splitlines())
    for k, v in repl.items():
        text = text.replace(k, v)
    assert "{" not in re.sub(r"\{(nome|YYYY)[^}]*\}", "", text) or part == "P", text
    return text


def run_cell(cell):
    s = state()
    project = LAB / s["cells"][cell]
    out = ROUND / "execucoes" / cell
    out.mkdir(parents=True, exist_ok=True)
    prompt = prompt_for(cell, project)
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    with open(out / "eventos.jsonl", "w", encoding="utf-8") as log:
        res = subprocess.run([CODEX, "exec", "--dangerously-bypass-approvals-and-sandbox", "--json",
                              "-m", MODEL, "-c", f'model_reasoning_effort="{EFFORT}"',
                              "-C", str(project), "-o", str(out / "retorno.md"), "-"],
                             input=prompt, text=True, encoding="utf-8", stdout=log,
                             stderr=subprocess.STDOUT, timeout=4 * 3600)
    (out / "exit.txt").write_text(str(res.returncode), encoding="utf-8")
    return cell, res.returncode


def run(cells):
    cells = cells or list(CELLS)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for cell, code in pool.map(run_cell, cells):
            print(cell, code, flush=True)


def scan():
    s = state()
    report = {}
    for cell, label in s["cells"].items():
        log = ROUND / "execucoes" / cell / "eventos.jsonl"
        if not log.is_file():
            continue
        text = log.read_text(encoding="utf-8", errors="replace")
        others = [l for c, l in s["cells"].items() if c != cell]
        hits = []
        for pat in [r"laravel-ai-skills", r"experimentos", r"demo-r8", r"blind-2026100\d",
                    r"catalogo", r"cat[aá]logo-defeitos", r"wikis[\\/]+specs[\\/]+exp-", r"tests[\\/]+Feature[\\/]+Exp"] + others:
            for m in re.finditer(pat, text, re.I):
                hits.append(text[max(0, m.start() - 120): m.end() + 60].replace("\n", " "))
        report[cell] = hits
    (ROUND / "varredura-isolamento.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({c: len(h) for c, h in report.items()}))


def freeze():
    s = state()
    judges = LAB / "judges"
    judges.mkdir(exist_ok=True)
    prompt_raw = (REPO / "experimentos/protocolo/PROMPT-JUIZ-CEGO.md").read_text(encoding="utf-8")
    prompt = "\n".join(re.sub(r"^> ?", "", l) for l in prompt_raw.split("## Prompt\n", 1)[1].strip().splitlines())
    audit = {"judge_prompt_sha256": hashlib.sha256(prompt_raw.encode()).hexdigest(), "sets": {}}
    for cell, label in s["cells"].items():
        arm, part, scen = CELLS[cell]
        project = LAB / label
        archive = ROUND / "conjuntos" / cell
        if part == "P":
            wikis = [p for p in (project / "wikis/specs").iterdir() if p.name.startswith("saida-")]
            if wikis and not archive.exists():
                shutil.copytree(wikis[0], archive)
            continue
        source = project / f"wikis/specs/saida-c{scen}" / FEATURES[scen]
        files = [source / "04-casos-de-teste.md"] + ([source / "05-casos-de-teste-browser.md"]
                                                     if (source / "05-casos-de-teste-browser.md").is_file() else [])
        assert files[0].is_file(), f"{cell}: sem 04"
        raw = "\n\n".join(p.read_text(encoding="utf-8-sig") for p in files)
        assert not re.search(r"\b[DE](?:0[1-9]|1[0-8])\b", raw), f"{cell}: ID de catálogo no conjunto"
        if not archive.exists():
            shutil.copytree(source, archive)
        redacted = raw
        for pat, rep in [(re.escape(str(project)), "[PROJETO]"), (re.escape(label), "[PROJETO]"),
                         (r"\b(?:feature-wiki|feature-test-design|feature-quality-gate)\s+(?:v)?\d+\.\d+\.\d+\b", "[SKILL — VERSÃO ANONIMIZADA]"),
                         (r"\b(?:4\.1\.1|4\.2\.0|1\.17\.3|1\.17\.4|1\.8\.0|1\.9\.0)\b", "[VERSÃO ANONIMIZADA]")]:
            redacted = re.sub(pat, rep, redacted)
        anon = "j-" + secrets.token_hex(3)
        d = judges / anon
        d.mkdir()
        (d / "conjunto.md").write_text(redacted, encoding="utf-8", newline="\n")
        shutil.copyfile(REPO / f"experimentos/protocolo/cenario-{scen}-catalogo-defeitos.md", d / "catalogo.md")
        (judges / f"{anon}-prompt.md").write_text(prompt, encoding="utf-8")
        audit["sets"][cell] = {"anon": anon, "sha256": {p.name: digest(p) for p in files},
                               "anonymous_sha256": digest(d / "conjunto.md")}
        shutil.copyfile(d / "conjunto.md", archive / "conjunto-anonimizado.md")
    (ROUND / "congelamento.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({c: v["anon"] for c, v in audit["sets"].items()}))


def judge_one(item):
    cell, anon = item
    d = LAB / "judges" / anon
    prompt = (LAB / "judges" / f"{anon}-prompt.md").read_text(encoding="utf-8")
    prompt += "\n\nOs dois arquivos estão no diretório de trabalho: `catalogo.md` e `conjunto.md`. Leia somente esses dois."
    out = ROUND / "vereditos"
    out.mkdir(exist_ok=True)
    res = subprocess.run([CODEX, "exec", "--dangerously-bypass-approvals-and-sandbox", "--json",
                          "--skip-git-repo-check", "-m", MODEL, "-c", f'model_reasoning_effort="{EFFORT}"',
                          "-C", str(d), "-o", str(out / f"{anon}.md"), "-"],
                         input=prompt, text=True, encoding="utf-8", capture_output=True, timeout=3 * 3600)
    (out / f"{anon}-eventos.jsonl").write_text(res.stdout + res.stderr, encoding="utf-8")
    return anon, res.returncode


def judge():
    audit = json.loads((ROUND / "congelamento.json").read_text(encoding="utf-8"))
    items = [(c, v["anon"]) for c, v in audit["sets"].items()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for anon, code in pool.map(judge_one, items):
            print(anon, code, flush=True)


def check():
    s = state()
    decision = re.compile(r"^\s*(?:-\s+)?\**Roteiro manual\**\s*:\s*\**\s*(sim|n[ãa]o)\b", re.I | re.M)
    result = {}
    for cell, label in s["cells"].items():
        arm, part, scen = CELLS[cell]
        if part != "P":
            continue
        project = LAB / label
        wikis = sorted(p for p in (project / "wikis/specs").glob("saida-*/*") if p.is_dir())
        r = {"wikis": [str(w.relative_to(project)) for w in wikis]}
        if wikis:
            w = wikis[0]
            names = sorted(p.name for p in w.iterdir())
            r["files"] = names
            p03 = w / "03-progresso.md"
            t03 = p03.read_text(encoding="utf-8") if p03.is_file() else ""
            r["decision_lines"] = [m.group(0).strip() for m in re.finditer(r"(?im)^.*Roteiro manual.*$", t03)]
            r["decision_values"] = [m.group(1).lower() for m in decision.finditer(t03)]
            t00 = (w / "00-requisito.md").read_text(encoding="utf-8") if (w / "00-requisito.md").is_file() else ""
            r["roteiro_no_00"] = [l.strip() for l in t00.splitlines() if re.search(r"roteiro", l, re.I)]
            r["forbidden_files"] = [n for n in names if re.match(r"0[4-8]", n)]
            sh = REPO / ".ai/skills/feature-wiki/scripts/roteiro-manual.sh"
            if (project / ".ai/skills/feature-wiki/scripts/roteiro-manual.sh").is_file():
                sh = project / ".ai/skills/feature-wiki/scripts/roteiro-manual.sh"
            res = subprocess.run([BASH, str(sh), str(w)], capture_output=True, text=True)
            r["script"] = {"exit": res.returncode, "out": (res.stdout + res.stderr).strip()}
        ret = ROUND / "execucoes" / cell / "retorno.md"
        rt = ret.read_text(encoding="utf-8") if ret.is_file() else ""
        r["retorno_roteiro"] = [l.strip() for l in rt.splitlines() if re.search(r"roteiro", l, re.I)]
        result[cell] = r
    (ROUND / "criterios-parte-p.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def prepare_bprime():
    """B' = B + correção pós-reprovação de P1 (entrevista-tres-raias.md). Só a célula P1 reexecuta."""
    s = state()
    snap = LAB / "snapshots"
    shutil.copytree(snap / "B", snap / "Bp")
    rel = ".ai/skills/feature-wiki/references/entrevista-tres-raias.md"
    (snap / "Bp" / rel).write_bytes((REPO / rel).read_bytes().replace(b"\r\n", b"\n"))
    label = "proj-" + secrets.token_hex(3)
    target = LAB / label
    shutil.copytree(SOURCE, target, ignore=ignored)
    shutil.copytree(snap / "Bp" / ".ai/skills", target / ".ai/skills", dirs_exist_ok=True)
    for sub in ("storage/framework/cache/data", "storage/framework/sessions",
                "storage/framework/views", "storage/logs", "bootstrap/cache"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    for keep in ("main", "feature"):
        shutil.copytree(SOURCE / "wikis/specs" / keep, target / "wikis/specs" / keep)
    s["cells"]["P1-Bp"] = label
    s["cell_spec"]["P1-Bp"] = ["Bp", "P", 1]
    (ROUND / "preparacao.json").write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    m = json.loads((ROUND / "tratamentos/manifest.json").read_text(encoding="utf-8"))
    m["Bp"] = {rel: digest(snap / "Bp" / rel), "base": "B"}
    (ROUND / "tratamentos/manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print(label)


CELLS["P1-Bp"] = ("Bp", "P", 1)


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["help"]
    {"prepare": prepare, "prepare_bprime": prepare_bprime, "scan": scan, "freeze": freeze, "judge": judge, "check": check}.get(
        cmd, lambda: run(rest) if cmd == "run" else print(__doc__))() if cmd != "run" else run(rest)
