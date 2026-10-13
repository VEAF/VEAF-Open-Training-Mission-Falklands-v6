"""FARP Torres del Paine : 128.5 MHz est la fréquence de la tour de Franco Bianco (VHF, relevée dans DCS le
13/10/2026) ; le FARP passe à 129.5. Aucune action MCP ne règle la fréquence d'une hélistation après coup (add_farp
la pose à la création) : chargement de la table, modification, réécriture. Idempotent."""
import paths
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

FREQ = {"FARP Torres del Paine": "129.5"}


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


mission = load_folder_mission(paths.ROOT)
n = 0
for s in mission.mission_content["coalition"].values():
    for c in seq(s.get("country")):
        for g in seq((c.get("static") or {}).get("group")):
            if g["name"] in FREQ:
                seq(g["units"])[0]["heliport_frequency"] = FREQ[g["name"]]
                n += 1
assert n == len(FREQ)
save_folder_mission(mission, paths.ROOT)
print(n, "FARP changé(s)")
