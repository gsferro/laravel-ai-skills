"""Confere se o trecho citado em cada DETECTA existe no conjunto anonimizado que o juiz recebeu.

Normaliza escapes de Markdown/HTML que os juízes introduzem ao citar (`\\<`, `&lt;`, crases).
Prova proveniência textual da citação; não reavalia o mérito semântico do veredito.
"""
import html
import json
from pathlib import Path
import re

ROUND = Path(__file__).resolve().parent


def norm(s):
    s = html.unescape(s).replace("\\<", "<").replace("\\>", ">").replace("\\|", "|")
    for ch in "`*_\\":
        s = s.replace(ch, "")
    return re.sub(r"\s+", " ", s).strip()


audit = json.loads((ROUND / "congelamento.json").read_text(encoding="utf-8"))
out = {}
for cell, v in audit["sets"].items():
    conj = norm((ROUND / "conjuntos" / cell / "conjunto-anonimizado.md").read_text(encoding="utf-8"))
    verdict = (ROUND / "vereditos" / f"{v['anon']}.md").read_text(encoding="utf-8")
    bad, n = [], 0
    for line in verdict.splitlines():
        m = re.match(r"\|\s*\**([DE]\d\d)\**\s*\|\s*\**DETECTA\**\s*\|(.*)", line)
        if not m:
            continue
        n += 1
        cite = m.group(2).split(" | ")[0]
        ids = re.findall(r"CT-B?\d+", cite)
        quotes = [norm(q) for g in re.findall(r"“([^”]{15,})”|\"([^\"]{15,})\"", cite) for q in g if q]
        if not quotes:
            frag = norm(re.sub(r"^[^:]*:", "", cite, count=1))
            quotes = [frag[:60]] if len(frag) > 25 else []
        missing = [q[:70] for q in quotes if q.rstrip(".…")[:45] not in conj]
        missing_ids = [i for i in ids if i not in conj]
        if missing or missing_ids or not ids:
            bad.append({"id": m.group(1), "ids": ids, "ids_ausentes": missing_ids, "trechos_ausentes": missing})
    out[cell] = {"detecta": n, "problemas": bad}
    print(cell, "DETECTA", n, "problemas", len(bad))
    for b in bad:
        print("   ", b)
(ROUND / "auditoria-citacoes.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
