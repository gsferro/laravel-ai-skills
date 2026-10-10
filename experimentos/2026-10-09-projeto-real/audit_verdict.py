"""Check blind verdict IDs, quoted text and scenario counts without rewriting verdicts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile


def audit(directory, scenario, verdict_filename="veredito.md"):
    source = (directory / "conjunto.md").read_text(encoding="utf-8-sig")
    assert verdict_filename in {"veredito.md", "veredito-pareado.md"}, "Unsupported verdict artifact"
    verdict_path = directory / verdict_filename
    verdict = verdict_path.read_text(encoding="utf-8-sig")
    prefix = "D" if scenario == 1 else "E"
    rows = []
    for line in verdict.splitlines():
        match = re.match(r"^\|\s*(" + prefix + r"\d{2})\s*\|", line)
        if not match:
            continue
        columns = re.split(r"(?<!\\)\|", line)
        decision = columns[2].replace("*", "").strip()
        assert decision in {"DETECTA", "NÃO DETECTA"}, "Unknown verdict"
        quotes = re.findall(r"“([^”]+)”", columns[3])
        checks = []
        for quote in quotes:
            quote = quote.replace(r"\|", "|")
            checks.append({"quote": quote, "literal_in_source": quote in source})
        gap = re.search(r"(?i)lacuna\s+(cega|declarada)", columns[3])
        assert decision == "DETECTA" or gap, "Missing gap class for a non-detection"
        rows.append({"id": match[1], "decision": decision,
                     "gap": gap[1].lower() if decision == "NÃO DETECTA" else None,
                     "ct": re.findall(r"\bCT-(?:B)?\d+\b", columns[3]), "quotes": checks,
                     "valid_quote": bool(checks) and all(q["literal_in_source"] for q in checks)})
    assert [row["id"] for row in rows] == [f"{prefix}{i:02}" for i in range(1, 19)], "Missing/duplicate/out-of-order catalog row"
    # Count Gherkin declarations only; Examples, the index and references are not new scenarios.
    declarations = re.findall(r"(?m)^\s*(?:Esquema do Cenário|Cenário):\s*\[(CT-(?:B)?\d+)\]", source)
    assert declarations and len(declarations) == len(set(declarations)), "Missing/duplicate Gherkin IDs"
    detected = [row["id"] for row in rows if row["decision"] == "DETECTA"]
    return {"anonymous_id": directory.name, "scenario": scenario,
            "verdict_filename": verdict_filename,
            "verdict_sha256": hashlib.sha256(verdict_path.read_bytes()).hexdigest(),
            "source_sha256": hashlib.sha256((directory / "conjunto.md").read_bytes()).hexdigest(),
            "rows": rows, "detected": detected, "ddr_denominator": 18,
            "scenario_declarations": declarations, "nct": len(declarations),
            "all_detected_have_literal_quotes": all(row["valid_quote"] for row in rows if row["decision"] == "DETECTA")}


def self_check():
    with tempfile.TemporaryDirectory(prefix="verdict-audit-") as temporary:
        folder = Path(temporary)
        (folder / "conjunto.md").write_text("Cenário: [CT-01] exemplo\nEntão valor 1\n", encoding="utf-8")
        table = "\n".join(f'| D{i:02} | DETECTA | CT-01: “Então valor 2” | errado |' for i in range(1, 19))
        (folder / "veredito.md").write_text(table, encoding="utf-8")
        assert not audit(folder, 1)["all_detected_have_literal_quotes"]
        (folder / "veredito.md").write_text(table.replace("valor 2", "valor 1"), encoding="utf-8")
        result = audit(folder, 1)
        assert result["all_detected_have_literal_quotes"] and result["nct"] == 1
        (folder / "veredito.md").write_text(table.replace("D18", "D17"), encoding="utf-8")
        try:
            audit(folder, 1)
        except AssertionError:
            pass
        else:
            raise AssertionError("Duplicate catalog IDs accepted")
        (folder / "veredito-pareado.md").write_text(table.replace("DETECTA", "NÃO DETECTA").replace("CT-01: “Então valor 2”", "lacuna cega"), encoding="utf-8")
        result = audit(folder, 1, "veredito-pareado.md")
        assert result["detected"] == [] and all(row["gap"] == "cega" for row in result["rows"])


def main():
    self_check()
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("scenario", type=int, choices=[1, 2])
    args = parser.parse_args()
    print(json.dumps(audit(args.directory, args.scenario), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
