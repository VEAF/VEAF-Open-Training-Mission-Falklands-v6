"""Lot 10 : sanctuaires, arène AirQuake, groupes des missions scénarisées.
(Les slots sur les ponts viennent avec les porte-avions, lot 05b.)

Sanctuaires (cercles tirés de zones de déclenchement) :
  - bleu « Falkland » : 50 km autour de (70 km, 25 km), centré entre Mount Pleasant, Goose Green, Gull Point et San
    Carlos FOB ; ni Stanley (71 km du centre) ni les zones de combat (Z01 à 58 km) ne sont dedans ;
  - bleu « Magellan » : 45 km autour de Punta Arenas, Porvenir et Almirante Schroeders ;
  - rouge « San Julian » : 30 km autour de la base rouge du nord, loin de toute zone.
  Ni Rio Gallegos, ni Rio Grande, ni Puerto Natales n'en ont : leurs zones de combat sont à côté.
Arène AirQuake : Atlantique sud, au sud des Falkland, centre (-220 000, -150 000), 40 nm de rayon, loin de tout
(les ravitailleurs sont à 200 km, Isla de los Estados à 180 km) ; emports AirQuake de la v5 de l'OT Golfe
Persique (FOX1 = AIM-7M / Super 530D, FOX3 = AIM-120C / AIM-54C), départ en vol au FL250. Les bleus au nord
(cap 180), les rouges au sud (cap 0), F-14B rouges sous l'Iran, comme au Golfe Persique.
"""
import json

from lib import AIRFIELDS, BLUE, RED, ROOT, Batch, ll, xy

V5 = json.loads((ROOT / "tools/loadouts-arene.json").read_text(encoding="utf-8"))
RED_IR = dict(coalition="red", country_id=34, country_name="Iran")

SANCTUARIES = [
    ("Sanctuaire Falkland", "SANCT-Falkland", (70000, 25000), 50000, "BLUE"),
    ("Sanctuaire Magellan", "SANCT-Magellan", (-175000, -765000), 45000, "BLUE"),
    ("Sanctuaire San Julian", "SANCT-SanJulian", AIRFIELDS["San Julian"], 30000, "RED"),
]

ARENA = ((-220000, -150000), 74000)   # centre, rayon (40 nm)
ARENA_SLOTS = [
    # nom v6, groupe AirQuake de la v5, camp, position (nord = bleu, sud = rouge)
    ("Arène bleue F-14B Fox 3", "BLUE F-14B AirQuake FOX3", BLUE, (-170000, -190000)),
    ("Arène bleue F-14B Fox 1", "F-14B AirQuake FOX1 BLUE", BLUE, (-170000, -180000)),
    ("Arène bleue F/A-18C Fox 3", "BLUE F/A-18C AirQuake FOX3", BLUE, (-170000, -170000)),
    ("Arène bleue F/A-18C Fox 1", "F/A-18C AirQuake FOX1 BLUE", BLUE, (-170000, -160000)),
    ("Arène bleue M-2000C Fox 1", "M2000C AirQuake FOX1 BLUE", BLUE, (-170000, -150000)),
    ("Arène rouge F-14B Fox 3", "RED F-14B AirQuake FOX3", RED_IR, (-270000, -190000)),
    ("Arène rouge F-14B Fox 1", "RED F-14B AirQuake FOX1", RED_IR, (-270000, -180000)),
    ("Arène rouge F/A-18C Fox 3", "RED F/A-18C AirQuake FOX3", RED, (-270000, -170000)),
    ("Arène rouge F/A-18C Fox 1", "RED F/A-18C AirQuake FOX1", RED, (-270000, -160000)),
    ("Arène rouge M-2000C Fox 1", "RED M2000C AirQuake FOX1", RED, (-270000, -150000)),
]

MOUNT_PLEASANT = AIRFIELDS["Mount Pleasant"]
RIO_GRANDE = AIRFIELDS["Rio Grande"]
CABO_VIRGENES = ll(-52.33, -68.36)
# Missions scénarisées : groupes en activation différée (combat_missions: de mission.yaml)
SCENARIO = [
    # nom, camp, type, nombre, départ, altitude ft, kt, tâche, emport, points suivants
    ("SC-Defense-MountPleasant-SEAD", RED, "Su-24M", 2, (95000, 170000), 18000, 480, "SEAD",
     {"payload": "Kh31P*2_Kh25ML*2_L-081"}, [(85000, 100000), MOUNT_PLEASANT]),
    ("SC-Defense-MountPleasant-Bombers", RED, "Su-34", 4, (98000, 175000), 20000, 450, "Ground Attack",
     {"payload": "FAB-500*8,R-73*2,ECM"}, [(88000, 105000), MOUNT_PLEASANT]),
    ("SC-Defense-MountPleasant-Escort", RED, "Su-30", 2, (96000, 172000), 24000, 450, "Escort",
     {"payload": "R-73*4,R-77*4,R-27ER*2"}, [(88000, 105000), MOUNT_PLEASANT]),
    ("SC-Intercept-VIP-Il76", RED, "IL-76MD", 1, AIRFIELDS["Rio Gallegos"], 22000, 350, "Transport",
     {}, [CABO_VIRGENES, RIO_GRANDE]),
    ("SC-Intercept-VIP-Escort", RED, "MiG-29S", 2, (AIRFIELDS["Rio Gallegos"][0] + 2000, AIRFIELDS["Rio Gallegos"][1] + 2000),
     24000, 350, "Escort", {"payload": "R-73*2,R-60M*2,R-27R*2,Fuel-1500"}, [CABO_VIRGENES, RIO_GRANDE]),
]

if __name__ == "__main__":
    b = Batch()
    for name, zone, c, r, side in SANCTUARIES:
        b.act("add_trigger_zone", name=zone, position=xy(c), radius=r)
    b.act("add_trigger_zone", name="Arene", position=xy(ARENA[0]), radius=ARENA[1])
    for name, v5name, side, p in ARENA_SLOTS:
        g = V5[v5name]
        hdg = 180 if side is BLUE else 0
        b.act("add_air_group", **side, name=name, unit_type=g["type"], count=2, start="air",
              position=xy(p), altitude_ft=25000, speed_kt=450, heading_deg=hdg, skill="Client",
              task="CAP", pylons=g["pylons"])
    for name, side, typ, n, p, alt, kt, task, loadout, route in SCENARIO:
        b.act("add_air_group", **side, name=name, unit_type=typ, count=n, start="air", position=xy(p),
              altitude_ft=alt, speed_kt=kt, task=task, skill="High", late_activation=True, **loadout)
        for q in route:
            b.act("edit_route", group_name=name, operation="add", position=xy(q), altitude_ft=alt, speed_kt=kt)
    b.act("edit_route", group_name="SC-Defense-MountPleasant-Bombers", operation="add_task", index=3, task="bombing",
          task_params={"position": xy(MOUNT_PLEASANT), "expend": "All", "attack_qty": 1})
    for esc, target in [("SC-Defense-MountPleasant-Escort", "SC-Defense-MountPleasant-Bombers"),
                        ("SC-Intercept-VIP-Escort", "SC-Intercept-VIP-Il76")]:
        b.act("edit_route", group_name=esc, operation="add_task", index=1, task="escort",
              task_params={"group_name": target, "engagement_distance_nm": 30})
    b.save("10-joueurs.json")
