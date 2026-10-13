"""Réécrit dans mission.yaml les briefings des CAP à la demande depuis gen_09_qra_cap.py (deux descriptions du lot 09
nommaient des lieux hors de la route : Cullen et l'île Dawson). Aucune action MCP ne modifie une CAP après coup. Idempotent."""
from pathlib import Path

from ruamel.yaml import YAML

from gen_09_qra_cap import CAPS
from lib import M

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096
path = Path(M) / "mission.yaml"
d = yaml.load(path.read_text(encoding="utf-8"))
caps = d["cap_missions"]
n = 0
for entry in caps:
    for name, _t, _n, _side, _a, _b, _fl, _kt, _lo, menu, brief in CAPS:
        if entry.get("group_name") == name:
            entry["briefing"] = brief
            n += 1
assert n == len(CAPS), (n, len(CAPS))
with path.open("w", encoding="utf-8") as f:
    yaml.dump(d, f)
print(n, "CAP réécrites")
