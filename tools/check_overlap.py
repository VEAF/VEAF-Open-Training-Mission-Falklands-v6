"""Aucun groupe étranger dans le cercle d'une zone de combat (VEAF capture par la géométrie, quelle que soit la
coalition : un groupe permanent, une balise, un FARP ou un ravitailleur dans un cercle serait détruit puis recréé).
python check_overlap.py [lot.json ...] : zones déjà dans la mission + zones des lots donnés (pas encore exécutés)."""
import json
import math
import sys

import paths  # noqa: F401
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


m = load_folder_mission(paths.ROOT).mission_content
zones = {z["name"]: (z["x"], z["y"], z["radius"]) for z in seq(m["triggers"]["zones"])}
for f in sys.argv[1:]:
    for it in json.load(open(f, encoding="utf-8")):
        if it["name"] == "create_combat_zone":
            p = it["params"]
            zones[p["zone_name"]] = (p["position"]["x"], p["position"]["y"], p["radius"])
combat = {n: z for n, z in zones.items() if n.startswith("combatZone_")}
bad = 0
for side in m["coalition"].values():
    for c in seq(side.get("country")):
        for cat in ("plane", "helicopter", "vehicle", "ship", "static"):
            for g in seq((c.get(cat) or {}).get("group")):
                for zn, (zx, zy, zr) in combat.items():
                    fam = zn.rsplit("_", 1)[0] if zn.endswith(("_Easy", "_Medium", "_Hard")) else zn
                    if g["name"].startswith(fam):   # un groupe d'un niveau de la famille est chez lui dans les autres
                        continue
                    u = seq(g["units"])[0]
                    d = math.hypot(u["x"] - zx, u["y"] - zy)
                    if d < zr + 150 and not (cat in ("plane", "helicopter") and u.get("alt", 0) > 500):
                        print(f"  {g['name']} ({cat}) à {d:.0f} m du centre de {zn} (rayon {zr})")
                        bad += 1
# zones de combat qui se recouvrent
names = sorted(combat)
for i, a in enumerate(names):
    for b in names[i + 1:]:
        d = math.hypot(combat[a][0] - combat[b][0], combat[a][1] - combat[b][1])
        fam = lambda n: n.rsplit("_", 1)[0] if n.endswith(("_Easy", "_Medium", "_Hard")) else n
        if fam(a) != fam(b) and d < combat[a][2] + combat[b][2] + 150:
            print(f"  zones {a} et {b} se recouvrent ({d:.0f} m)")
            bad += 1
print(f"VERDICT : {bad} recouvrement(s) sur {len(combat)} zones de combat")
