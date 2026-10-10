"""Execute selected concrete mutations with a green control and byte-exact restoration.

This is not a score for the complete 18-defect catalog. Inspect JUnit failures and
the targeted assertions before calling an individual mutant killed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from unittest.mock import patch
import xml.etree.ElementTree as ET


ROUND = Path(__file__).resolve().parent
RUNTIME = Path(r"D:\PROJECTS\SKILLS\blind-20261009\runtime")
MUTANTS = {
    "c1-float": ("app/Models/Cupom.php",
        "intdiv($valorTotalEmCentavos, 100) * $this->valor + intdiv(($valorTotalEmCentavos % 100) * $this->valor, 100)",
        "(int) ($valorTotalEmCentavos * ($this->valor / 100))"),
    "c1-negative": ("app/Models/Cupom.php",
        "return max(0, $valorTotalEmCentavos - $desconto);",
        "return $valorTotalEmCentavos - $desconto;"),
    "c1-no-increment": ("app/Models/Cupom.php", "->increment('usos');", "->increment('usos', 0);"),
    "c1-expiry-inclusive": ("app/Models/Cupom.php", "->where('expira_em', '>', now())", "->where('expira_em', '>=', now())"),
    "c1-limit-inclusive": ("app/Models/Cupom.php", "->whereColumn('usos', '<', 'limite_de_usos')", "->whereColumn('usos', '<=', 'limite_de_usos')"),
    # Selected after the coupon verdicts: report separately from the seven earlier operators.
    "c1-negative-fixed-input": ("app/Filament/App/Resources/Cupons/CupomResource.php",
        "->minValue(1)->maxValue(fn (Get $get): ?int => $get('tipo') === TipoDeDesconto::Porcentagem->value ? 100 : null)",
        "->minValue(fn (Get $get): int => $get('tipo') === TipoDeDesconto::Fixo->value ? -1 : 1)->maxValue(fn (Get $get): ?int => $get('tipo') === TipoDeDesconto::Porcentagem->value ? 100 : null)"),
    # Post-hoc operator repair: v2's scalar comparison never enabled the negative fixed input.
    "c1-negative-fixed-input-enum": ("app/Filament/App/Resources/Cupons/CupomResource.php",
        "->minValue(1)->maxValue(fn (Get $get): ?int => $get->enum('tipo', TipoDeDesconto::class) === TipoDeDesconto::Porcentagem ? 100 : null)",
        "->minValue(fn (Get $get): int => $get->enum('tipo', TipoDeDesconto::class) === TipoDeDesconto::Fixo ? -1 : 1)->maxValue(fn (Get $get): ?int => $get->enum('tipo', TipoDeDesconto::class) === TipoDeDesconto::Porcentagem ? 100 : null)"),
    "c2-director-at-limit": ("app/Models/SolicitacaoCompra.php",
        "return (float) $this->valor > (float) config('kit.compras.limite_diretor', 5000.00);",
        "return (float) $this->valor >= (float) config('kit.compras.limite_diretor', 5000.00);"),
    "c2-empty-rejection": ("app/Models/SolicitacaoCompra.php", "if (blank($justificativa)) {", "if (false) {"),
}


def run(label, tests, output):
    junit = output / f"{label}.xml"
    command = ["php", "vendor/bin/pest", *tests, "--colors=never", "--log-junit", str(junit)]
    started = time.monotonic()
    timed_out = False
    try:
        process = subprocess.run(command, cwd=RUNTIME, capture_output=True, timeout=600)
        stdout, stderr, exit_code = process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired as failure:
        stdout, stderr, exit_code = failure.stdout or b"", failure.stderr or b"", None
        timed_out = True
    (output / f"{label}.log").write_bytes(stdout + b"\nSTDERR\n" + stderr)
    cases = []
    if junit.is_file():
        for case in ET.parse(junit).iter("testcase"):
            failures = [{"kind": node.tag, "type": node.get("type"), "message": node.get("message"),
                         "text": node.text} for node in case if node.tag in {"failure", "error", "skipped"}]
            cases.append({"name": case.get("name"), "class": case.get("classname"),
                          "assertions": int(case.get("assertions", "0")), "problems": failures})
    return {"command": command, "cwd": str(RUNTIME), "exit_code": exit_code, "timed_out": timed_out,
            "duration_seconds": round(time.monotonic() - started, 3), "cases": cases}


def self_check():
    with tempfile.TemporaryDirectory(prefix="mutation-runner-") as temporary:
        output = Path(temporary)
        failure = subprocess.TimeoutExpired(["php"], 600, output=b"partial stdout", stderr=b"partial stderr")
        with patch("subprocess.run", side_effect=failure):
            result = run("timeout", ["tests/example.php"], output)
        assert result["timed_out"] and result["exit_code"] is None and result["cases"] == []
        assert (output / "timeout.log").read_bytes() == b"partial stdout\nSTDERR\npartial stderr"


def main():
    self_check()
    parser = argparse.ArgumentParser()
    parser.add_argument("anonymous_id")
    parser.add_argument("tests", nargs="+")
    parser.add_argument("--mutants", nargs="+", choices=list(MUTANTS), required=True)
    parser.add_argument("--implementation-manifest", type=Path,
                        default=ROUND / "execucao-controle/manifest-implementacao.json")
    args = parser.parse_args()
    assert args.anonymous_id.isalnum(), "Use a bounded anonymous output identifier"
    for test in args.tests:
        path = (RUNTIME / test).resolve()
        assert path.is_relative_to((RUNTIME / "tests").resolve()) and path.exists(), "Test path outside runtime/tests"
    output = ROUND / "execucao-mutantes" / args.anonymous_id
    output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.implementation_manifest.resolve()
    assert manifest_path.is_relative_to(ROUND.resolve()) and manifest_path.is_file(), "Reference manifest must be archived in this round"
    results = {"anonymous_id": args.anonymous_id, "catalog_complete": False,
               "implementation_manifest": str(manifest_path),
               "control": run("control", args.tests, output), "mutants": []}
    result_path = output / "resultado.json"
    result_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    assert results["control"]["exit_code"] == 0 and results["control"]["cases"], "Non-green/empty control: no mutation evidence"
    assert any(not case["problems"] and case["assertions"] > 0 for case in results["control"]["cases"]), "No asserted, executed control case"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    for name in args.mutants:
        relative, before, after = MUTANTS[name]
        path = RUNTIME / relative
        original = path.read_bytes()
        digest = hashlib.sha256(original).hexdigest()
        assert digest == manifest[relative], "Implementation differs from the frozen control"
        text = original.decode("utf-8")
        assert text.count(before) == 1, "Mutation must change exactly one concrete expression"
        try:
            path.write_bytes(text.replace(before, after).encode("utf-8"))
            result = run(name, args.tests, output)
            result.update({"name": name, "file": relative, "before": before, "after": after,
                           "original_sha256": digest, "mutated_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            results["mutants"].append(result)
        finally:
            path.write_bytes(original)
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, "Restoration failed"
            result_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"result": str(result_path), "exit_codes": {m["name"]: m["exit_code"] for m in results["mutants"]}}))


if __name__ == "__main__":
    main()
