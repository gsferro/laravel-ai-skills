"""Archive byte-identical translations and maps before a selected execution attempt."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from run_mutants import ROUND, RUNTIME


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    assert args.stage.isalnum(), "Use a bounded archive stage identifier"
    sources = []
    for relative in args.files:
        source = (RUNTIME / relative).resolve()
        assert source.is_relative_to(RUNTIME.resolve()) and source.is_file(), "Missing runtime file"
        assert source.is_relative_to((RUNTIME / "tests").resolve()) or source.is_relative_to((RUNTIME / "validation").resolve()), "Only tests and materialization maps may be archived"
        sources.append(source)
    output = ROUND / "testes" / args.stage
    output.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for source in sources:
        relative = source.relative_to(RUNTIME)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert source.read_bytes() == target.read_bytes(), "Translation copy changed bytes"
        hashes[str(relative)] = hashlib.sha256(target.read_bytes()).hexdigest()
    (output / "sha256.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"stage": str(output), "files": len(hashes)}))


if __name__ == "__main__":
    main()
