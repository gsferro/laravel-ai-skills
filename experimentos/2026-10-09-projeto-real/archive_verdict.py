"""Archive unchanged blind verdicts and disclose legacy newline/hash metadata differences."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

from audit_verdict import audit, self_check


ROUND = Path(__file__).resolve().parent
LAB = Path(r"D:\PROJECTS\SKILLS\blind-20261009")


def main():
    self_check()
    parser = argparse.ArgumentParser()
    parser.add_argument("anonymous_id")
    parser.add_argument("scenario", type=int, choices=[1, 2])
    parser.add_argument("--paired", action="store_true", help="Archive the separate post-hoc paired verdict")
    args = parser.parse_args()
    assert re.fullmatch(r"conjunto-[a-z0-9]+", args.anonymous_id), "Unsafe anonymous identifier"
    directory = LAB / "judges" / args.anonymous_id
    verdict_filename = "veredito-pareado.md" if args.paired else "veredito.md"
    result = audit(directory, args.scenario, verdict_filename)
    assert result["all_detected_have_literal_quotes"], "A DETECTA quote does not exist in the source"
    manifests = []
    for path in (ROUND / "conjuntos").glob("*/freeze.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["anonymous_id"] == args.anonymous_id:
            manifests.append((path, data))
    assert len(manifests) == 1, "Anonymous set must map to exactly one frozen arm"
    path, frozen = manifests[0]
    anonymous = directory / "conjunto.md"
    assert anonymous.read_bytes() == (path.parent / "conjunto-anonimizado.md").read_bytes(), "Judge input changed"
    actual = hashlib.sha256(anonymous.read_bytes()).hexdigest()
    normalized = hashlib.sha256(anonymous.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    recorded = frozen["anonymous_sha256"]
    assert recorded in {actual, normalized}, "Frozen metadata does not match bytes or its legacy LF normalization"
    result["freeze_hash_check"] = {"recorded": recorded, "actual_bytes": actual,
                                  "normalized_lf": normalized, "metadata_describes_bytes": recorded == actual,
                                  "legacy_note": None if recorded == actual else
                                  "The first freezer hashed LF text before Windows wrote CRLF. Original metadata is preserved; actual input bytes are identical to the archived anonymous set."}
    output = ROUND / ("vereditos-pareados" if args.paired else "vereditos")
    output.mkdir(exist_ok=True)
    target = output / f"{args.anonymous_id}.md"
    assert not target.exists(), "Do not replace a raw verdict"
    shutil.copyfile(directory / verdict_filename, target)
    (output / f"{args.anonymous_id}-auditoria.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"archived": str(target), "detected": result["detected"], "nct": result["nct"],
                      "literal_quotes": result["all_detected_have_literal_quotes"], "byte_hash_metadata": recorded == actual}))


if __name__ == "__main__":
    main()
