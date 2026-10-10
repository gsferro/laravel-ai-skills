"""Read-only checks of frozen treatments, instruments and the independent implementation."""
import argparse
import hashlib
import json
from pathlib import Path


ROUND = Path(__file__).resolve().parent
LAB = Path(r"D:\PROJECTS\SKILLS\blind-20261009")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-manifest", type=Path,
                        default=ROUND / "execucao-controle/manifest-implementacao.json")
    args = parser.parse_args()
    manifest_path = args.implementation_manifest.resolve()
    assert manifest_path.is_relative_to(ROUND.resolve()) and manifest_path.is_file(), "Reference manifest must be archived in this round"
    preparation = json.loads((ROUND / "preparacao.json").read_text(encoding="utf-8-sig"))
    treatments = {}
    for project in ["project-71", "project-26"]:
        files = preparation[project]["files"]
        for relative, expected in files.items():
            assert digest(LAB / project / relative) == expected, f"Treatment changed: {project}/{relative}"
        treatments[project] = len(files)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    for relative, expected in manifest.items():
        assert digest(LAB / "runtime" / relative) == expected, f"Independent implementation changed: {relative}"
    result = {"verified_treatment_files": treatments, "verified_implementation_files": len(manifest),
              "implementation_manifest": str(manifest_path),
              "implementation_restored": True, "treatments_unchanged": True,
              "limitation": "Hashes verify file integrity, not read isolation or behavioral correctness."}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
