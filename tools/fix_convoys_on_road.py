"""Passe les trois convois en « On Road », départ compris, à 12 m/s (43 km/h, 23 kt).

Les points viennent du chemin par la route que DCS donne (roads.convoy_route, relevé en jeu le 13/10/2026) : le
départ et chaque point de passage sont sur une route. create_combat_zone écrit le départ en « Off Road » et la route
à 5,6 m/s (20 km/h), sans le dire (mesuré par l'OT Sinaï, retours VMCT 13) : un convoi de 31 à 60 km y mettrait de 1 h 30 à 3 h.
Aucune action MCP n'écrit l'une ou l'autre : chargement de la table, modification, réécriture. Idempotent.
"""
import sys

import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
SPEED = 12.0


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


mission = load_folder_mission(paths.ROOT)
m = mission.mission_content
done = 0
for s in m["coalition"].values():
    for c in seq(s.get("country")):
        for g in seq((c.get("vehicle") or {}).get("group")):
            if not g["name"].startswith("combatZone_Convoi"):
                continue
            pts = seq(g["route"]["points"])
            for p in pts:
                p["action"] = "On Road"
                p["type"] = "Turning Point"
                p["speed"] = SPEED
            done += 1
            print(f"{g['name']}: {len(pts)} points sur route à {SPEED} m/s")
assert done == 3, done
print(save_folder_mission(mission, paths.ROOT)["mission_file"])
