"""Run a selected real Pest/Chromium translation and retain failed attempts unchanged."""
import argparse
import hashlib
import json

from run_mutants import ROUND, RUNTIME, run, self_check


def main():
    self_check()
    parser = argparse.ArgumentParser()
    parser.add_argument("attempt")
    parser.add_argument("tests", nargs="+")
    args = parser.parse_args()
    assert args.attempt.isalnum(), "Use a bounded attempt identifier"
    hashes = {}
    for relative in args.tests:
        path = (RUNTIME / relative).resolve()
        assert path.is_relative_to((RUNTIME / "tests").resolve()) and path.exists(), "Test path outside runtime/tests"
        for file in ([path] if path.is_file() else sorted(path.rglob("*.php"))):
            hashes[str(file.relative_to(RUNTIME))] = hashlib.sha256(file.read_bytes()).hexdigest()
    output = ROUND / "execucao-derivada" / args.attempt
    output.mkdir(parents=True, exist_ok=False)
    result = run("control", args.tests, output)
    result["test_sha256"] = hashes
    (output / "resultado.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"result": str(output / "resultado.json"), "exit_code": result["exit_code"],
                      "cases": len(result["cases"]), "assertions": sum(case["assertions"] for case in result["cases"]),
                      "problems": [{"test": case["name"], "problems": case["problems"]} for case in result["cases"] if case["problems"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
