"""Preserve corrected reference v2/v3 separately; never overwrite earlier evidence."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil

from run_mutants import ROUND, RUNTIME


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, choices=[2, 3], default=2)
    version = parser.parse_args().version
    previous_directory = ROUND / ("implementacao" if version == 2 else "referencia-v2")
    previous_manifest = ROUND / ("execucao-controle/manifest-implementacao.json" if version == 2 else "referencia-v2/manifest.json")
    baseline = json.loads(previous_manifest.read_text(encoding="utf-8-sig"))
    output = ROUND / f"referencia-v{version}"
    output.mkdir(exist_ok=False)
    manifest, changes, patch = {}, [], []
    for relative, previous in baseline.items():
        source = RUNTIME / relative
        current = hashlib.sha256(source.read_bytes()).hexdigest()
        manifest[relative] = current
        if relative == ".env.example":
            assert current == previous, "The environment example is outside this correction"
            continue  # Original environment content is never archived in full.
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert source.read_bytes() == target.read_bytes()
        if current != previous:
            old = previous_directory / relative
            assert old.is_file() and hashlib.sha256(old.read_bytes()).hexdigest() == previous
            changes.append(relative)
            patch.extend(difflib.unified_diff(old.read_text(encoding="utf-8").splitlines(keepends=True),
                                              source.read_text(encoding="utf-8").splitlines(keepends=True),
                                              fromfile="a/" + relative, tofile="b/" + relative))
    expected = ({"app/Models/Cupom.php", "tests/Feature/LaboratorioContratoTest.php", "contrato-publico.md"}
                if version == 2 else {"app/Filament/App/Resources/Cupons/CupomResource.php"})
    assert set(changes) == expected, "Unexpected reference change"
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    (output / "alteracoes.patch").write_text("".join(patch), encoding="utf-8", newline="\n")
    shutil.copyfile(RUNTIME / f"validation/correcao-referencia-v{version}.md", output / "CORRECAO.md")
    reason = ("00 requires User; v1 incorrectly followed the nullable signature from 01." if version == 2 else
              "Filament Get returns enum; scalar comparisons broke the label and percentage maximum.")
    (output / "registro.json").write_text(json.dumps({"version": version, "changed_files": changes,
                                                    "reason": reason,
                                                    "domain_expectations_changed": False,
                                                    "tests_not_yet_run_at_capture": True}, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"reference_manifest": str(output / "manifest.json"), "changed_files": changes}))


if __name__ == "__main__":
    main()
