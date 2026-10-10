"""Freeze complete arm outputs and produce identity-redacted copies for judges.

Run only after the independent adversarial review has been closed for that arm.
The original files remain archived; no scenario, assertion or debt is removed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

ROUND = Path(__file__).resolve().parent
LAB = Path(r"D:\PROJECTS\SKILLS\blind-20261009")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", choices=["project-71", "project-26"])
    parser.add_argument("scenario", type=int, choices=[1, 2])
    parser.add_argument("anonymous_id")
    args = parser.parse_args()
    assert re.fullmatch(r"[a-z][a-z0-9-]+", args.anonymous_id), "Unsafe output identifier"
    feature = "cupons-de-desconto" if args.scenario == 1 else "aprovacao-de-compra"
    source = LAB / args.project / f"wikis/specs/saida-c{args.scenario}" / feature
    files = [source / "04-casos-de-teste.md"]
    browser = source / "05-casos-de-teste-browser.md"
    if browser.is_file():
        files.append(browser)
    assert all(p.is_file() for p in files), "Missing complete specification"
    raw = "\n\n".join(p.read_text(encoding="utf-8-sig") for p in files)
    assert not re.search(r"__COUNT_|Revisão adversarial: PENDENTE", raw), "Arm is not closed"
    review_sections = re.findall(r"(?mi)^## Revisão adversarial[^\n]*\n([\s\S]*?)(?=^## |\Z)", raw)
    assert review_sections, "Independent review closure must be present"
    # Execution debt can remain pending after independent review closes; inspect review status only.
    assert any(re.search(r"(?im)(?:Status da revisão:\s*\*{0,2}|^\s*\*{0,2})CONCLUÍDA", section) for section in review_sections), "Independent review closure is missing"
    assert not re.search(r"(?i)(?:Status da revisão:|Revisão adversarial:)\s*\*?\*?PENDENTE", raw), "Independent review is pending"
    assert not re.search(r"\b[DE](?:0[1-9]|1[0-8])\b", raw), "Catalog ID in arm output"
    archive = ROUND / "conjuntos" / f"{args.project}-c{args.scenario}"
    assert not archive.exists(), "Refuse to replace a frozen arm"
    shutil.copytree(source, archive)
    replacements = []
    redacted = raw
    patterns = [
        (re.escape(str(LAB / args.project)), "[PROJETO]"),
        (r"\b(?:feature-wiki|feature-test-design)\s+(?:v)?\d+\.\d+\.\d+\b", "[SKILL — VERSÃO ANONIMIZADA]"),
        (r"\b(?:4\.0\.0|4\.1\.0|1\.16\.0|1\.17\.0)\b", "[VERSÃO ANONIMIZADA]"),
        (r"\bproject-(?:71|26)\b", "[PROJETO]"),
        (r"/root/(?:blind|adversarial)_[a-z0-9_]+", "[EXECUTOR]"),
    ]
    for pattern, replacement in patterns:
        redacted, count = re.subn(pattern, replacement, redacted)
        if count:
            replacements.append({"pattern": pattern, "replacement": replacement, "count": count})
    judge = LAB / "judges" / args.anonymous_id
    judge.mkdir(parents=True, exist_ok=False)
    (judge / "conjunto.md").write_text(redacted, encoding="utf-8", newline="\n")
    assert (judge / "conjunto.md").read_bytes() == redacted.encode("utf-8"), "Anonymous byte hash must describe the written file"
    instruments = ROUND / "instrumentos-congelados"
    shutil.copyfile(instruments / f"cenario-{args.scenario}-catalogo-defeitos.md", judge / "catalogo.md")
    prompt = (instruments / "PROMPT-JUIZ-CEGO.md").read_text(encoding="utf-8").split("## Prompt\n", 1)[1]
    prompt = "\n".join(re.sub(r"^> ?", "", line) for line in prompt.strip().splitlines())
    # Prompt is stored separately so the judge's data directory contains exactly two files.
    (LAB / "judges" / f"{args.anonymous_id}-prompt.md").write_text(prompt, encoding="utf-8")
    audit = {"project": args.project, "scenario": args.scenario, "anonymous_id": args.anonymous_id,
             "redactions": replacements, "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
             "anonymous_sha256": hashlib.sha256((judge / "conjunto.md").read_bytes()).hexdigest()}
    (archive / "freeze.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copyfile(judge / "conjunto.md", archive / "conjunto-anonimizado.md")
    print(json.dumps({"judge_directory": str(judge), "sha256": audit["anonymous_sha256"]}))


if __name__ == "__main__":
    main()
