"""Check the published float counterexample against the actual PHP interpreter."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def check(root):
    path = Path(root) / ".ai/skills/feature-test-design/references/tecnicas-por-regra.md"
    text = path.read_text(encoding="utf-8-sig")
    row = next(line for line in text.splitlines() if "percentual em `float` em vez de inteiro" in line)
    match = re.search(r"`(\(int\)\((\d+)\*0\.(\d+)\))` = (\d[\d.]*), inteiro dá (\d[\d.]*)", row)
    assert match, "Published example must include a literal, bounded PHP expression and both outputs"
    expression, total, digits, claimed_float, claimed_integer = match.groups()
    command = ["php", "-r", f"echo json_encode(['float'=>{expression},'inteiro'=>intdiv({total}*{int(digits)}, {10 ** len(digits)})]);"]
    process = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert process.returncode == 0, process.stderr
    actual = json.loads(process.stdout)
    claims = {"float": int(claimed_float.replace(".", "")), "inteiro": int(claimed_integer.replace(".", ""))}
    return {"reference": str(path), "reference_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "published_row": row, "command": command, "exit_code": process.returncode,
            "actual": actual, "claimed": claims,
            "valid": actual == claims and actual["float"] != actual["inteiro"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.root), indent=2))
