"""Summarize frozen primary verdicts; keep a paired secondary adjudication separate."""
import hashlib
import json
from pathlib import Path

from audit_verdict import audit, self_check

ROUND = Path(__file__).resolve().parent
JUDGES = Path(r"D:\PROJECTS\SKILLS\blind-20261009\judges")


def compare(before, after):
    old = set(before["detected"])
    new = set(after["detected"])
    old_blind = {row["id"] for row in before["rows"] if row["gap"] == "cega"}
    new_blind = {row["id"] for row in after["rows"] if row["gap"] == "cega"}
    lost = sorted(old - new)
    new_gaps = sorted(new_blind - old_blind)
    return {"gained": sorted(new - old), "lost": lost, "new_blind_gaps": new_gaps,
            "non_regression": not lost and not new_gaps,
            "nct_ratio": after["nct"] / before["nct"],
            "candidate_ddr_at_least_85_percent": len(new) / 18 >= .85,
            "candidate_nct_less_than_double": after["nct"] < 2 * before["nct"]}


def condensed(result):
    assert result["all_detected_have_literal_quotes"], "Non-literal DETECTA cannot support the summary"
    return {key: result[key] for key in (
        "anonymous_id", "scenario", "verdict_filename", "verdict_sha256", "source_sha256", "detected", "nct"
    )} | {"ddr_denominator": 18, "ddr": len(result["detected"]) / 18,
          "blind_gaps": [row["id"] for row in result["rows"] if row["gap"] == "cega"],
          "declared_gaps": [row["id"] for row in result["rows"] if row["gap"] == "declarada"],
          "density": len(result["detected"]) / result["nct"]}


def main():
    self_check()
    old = {"detected": ["D01"], "rows": [{"id": "D02", "gap": "cega"}], "nct": 3}
    same_total = {"detected": ["D02"], "rows": [{"id": "D01", "gap": "cega"}], "nct": 2}
    check = compare(old, same_total)
    assert check["lost"] == ["D01"] and not check["non_regression"], "Aggregate tie must not hide lost coverage"
    results = {"treatments": {"baseline": "FW4.0.0/FTD1.16.0", "candidate": "FW4.1.0/FTD1.17.0"},
               "primary": {}, "secondary_paired_c2": None,
               "limits": ["One generation per treatment/scenario", "Documentary DDR is not executed mutation score",
                          "Source corrections after treatment freeze are not measured by these verdicts"]}
    for scenario, first, second in ((1, "conjunto-k7", "conjunto-m4"), (2, "conjunto-h2", "conjunto-v9")):
        before = audit(JUDGES / first, scenario)
        after = audit(JUDGES / second, scenario)
        for result in (before, after):
            archived = ROUND / "vereditos" / f'{result["anonymous_id"]}.md'
            assert hashlib.sha256(archived.read_bytes()).hexdigest() == result["verdict_sha256"], "Raw verdict archive mismatch"
        results["primary"][f"scenario_{scenario}"] = {
            "baseline": condensed(before), "candidate": condensed(after), "comparison": compare(before, after)}
    paired = [JUDGES / name / "veredito-pareado.md" for name in ("conjunto-h2", "conjunto-v9")]
    assert all(path.exists() for path in paired) or not any(path.exists() for path in paired), "Do not summarize an incomplete secondary pair"
    if all(path.exists() for path in paired):
        before = audit(paired[0].parent, 2, paired[0].name)
        after = audit(paired[1].parent, 2, paired[1].name)
        for result in (before, after):
            archived = ROUND / "vereditos-pareados" / f'{result["anonymous_id"]}.md'
            assert hashlib.sha256(archived.read_bytes()).hexdigest() == result["verdict_sha256"], "Raw paired verdict archive mismatch"
        results["secondary_paired_c2"] = {"post_hoc": True, "baseline": condensed(before),
                                          "candidate": condensed(after), "comparison": compare(before, after)}
    results["primary_preregistered_gate_passed"] = all(
        arm["comparison"]["non_regression"] and arm["comparison"]["candidate_ddr_at_least_85_percent"]
        and arm["comparison"]["candidate_nct_less_than_double"] for arm in results["primary"].values())
    output = ROUND / "comparacao-documental.json"
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({"result": str(output), "primary_gate_passed": results["primary_preregistered_gate_passed"]}))


if __name__ == "__main__":
    main()
