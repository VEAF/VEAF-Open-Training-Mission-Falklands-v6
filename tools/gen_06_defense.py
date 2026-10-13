"""Lot 06 : défense aérienne permanente des bases et des arrières (#veafInterpreter).

Porteur = le lanceur que génère l'alias (l'éditeur montre son cercle de portée), nom unique.
Portées DCS (list_unit_types, threat_range_m) : Patriot 54 nm, SA-10 65 nm, SA-11 27 nm, Hawk 24 nm, SA-6 13,5 nm,
SA-15 6,5 nm, NASAMS 8,1 nm, Rapier 3,7 nm. Aucune ne doit couvrir une base adverse avec slots :
  - Falkland : Port Stanley (rouge, sans slots) est à 26,6 nm de Mount Pleasant : SA-6 et SA-15 seulement à
    Stanley (SA-11 : 27 nm, il toucherait la base) ; Patriot à Mount Pleasant ;
  - Chili : Rio Gallegos (rouge, slots) est à 102 nm de Punta Arenas, Rio Grande à 70 nm de Puerto Williams :
    Hawk à Williams, Patriot à Punta Arenas (54 nm) ; côté rouge SA-10 à Rio Gallegos (65 nm < 102 nm) et
    SA-11 à Rio Grande (27 nm < 70 nm) ;
  - Puerto Natales et Puerto Williams ont un terrain rouge sans slots à 12 et 24 nm (Rio Turbio, Ushuaia) : SA-15
    seulement de ce côté.
Le contrôle des distances est check_portees.py. Chaque emplacement est ramené sur la terre ferme (grille DCS).
"""
from lib import AIRFIELDS, BLUE_CL, BLUE_UK, PLACES, RED, Batch, interp_unit, land, ll, spot, xy

A = AIRFIELDS

# (camp, nom de groupe, centre, relèvement, distance (m), alias, type du porteur, cap)
SITES = [
    # ── Bleu, Falkland : Mount Pleasant (base mère), Goose Green, Gull Point, San Carlos ──
    (BLUE_UK, "AD Mount Pleasant Patriot", A["Mount Pleasant"], 200, 4500, "-patriot", "Patriot ln", 90),
    (BLUE_UK, "AD Mount Pleasant Rapier", A["Mount Pleasant"], 20, 2500, "-rapier", "rapier_fsa_launcher", 90),
    (BLUE_UK, "AD Mount Pleasant Avenger", A["Mount Pleasant"], 110, 2500, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE_UK, "AD Goose Green Hawk", A["Goose Green"], 270, 3500, "-hawk", "Hawk ln", 90),
    (BLUE_UK, "AD Goose Green Rapier", A["Goose Green"], 90, 1800, "-rapier", "rapier_fsa_launcher", 90),
    (BLUE_UK, "AD Gull Point NASAMS", A["Gull Point"], 180, 2500, "-nasams", "NASAMS_LN_C", 90),
    (BLUE_UK, "AD Gull Point Avenger", A["Gull Point"], 0, 1800, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE_UK, "AD San Carlos Hawk", A["San Carlos FOB"], 0, 3500, "-hawk", "Hawk ln", 90),
    (BLUE_UK, "AD San Carlos Avenger", A["San Carlos FOB"], 180, 1800, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu, Chili : Punta Arenas, Porvenir, Almirante Schroeders (Magellan) ──
    (BLUE_CL, "AD Punta Arenas Patriot", A["Punta Arenas"], 270, 4000, "-patriot", "Patriot ln", 90),
    (BLUE_CL, "AD Punta Arenas Hawk", A["Punta Arenas"], 180, 4500, "-hawk", "Hawk ln", 90),
    (BLUE_CL, "AD Punta Arenas Avenger", A["Punta Arenas"], 90, 2500, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE_CL, "AD Porvenir Hawk", A["Porvenir"], 90, 3500, "-hawk", "Hawk ln", 90),
    (BLUE_CL, "AD Porvenir Avenger", A["Porvenir"], 270, 1800, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE_CL, "AD Schroeders NASAMS", A["Almirante Schroeders"], 180, 2500, "-nasams", "NASAMS_LN_C", 90),
    (BLUE_CL, "AD Schroeders Avenger", A["Almirante Schroeders"], 0, 1800, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu, Chili : Puerto Natales (front nord), Puerto Williams (Beagle) ──
    (BLUE_CL, "AD Natales Hawk", A["Puerto Natales"], 180, 3500, "-hawk", "Hawk ln", 90),
    (BLUE_CL, "AD Natales NASAMS", A["Puerto Natales"], 270, 2500, "-nasams", "NASAMS_LN_C", 90),
    (BLUE_CL, "AD Natales Avenger", A["Puerto Natales"], 0, 1800, "-avenger_squad", "M1097 Avenger", 0),
    (BLUE_CL, "AD Williams Hawk", A["Puerto Williams"], 180, 3500, "-hawk", "Hawk ln", 90),
    (BLUE_CL, "AD Williams NASAMS", A["Puerto Williams"], 90, 2000, "-nasams", "NASAMS_LN_C", 90),
    (BLUE_CL, "AD Williams Avenger", A["Puerto Williams"], 270, 1800, "-avenger_squad", "M1097 Avenger", 0),
    # ── Bleu : guet, derrière les lignes ──
    (BLUE_UK, "EWR Mount Usborne", PLACES["Mount Usborne"], 0, 1500, "-blue_ewr", "FPS-117 Dome", 0),
    (BLUE_UK, "EWR Mount Adam", PLACES["Mount Adam"], 0, 1500, "-blue_ewr", "FPS-117 Dome", 0),
    (BLUE_CL, "EWR Punta Arenas", A["Punta Arenas"], 220, 9000, "-blue_ewr", "FPS-117 Dome", 0),
    (BLUE_CL, "EWR Natales", PLACES["Puerto Natales"], 200, 8000, "-blue_ewr", "FPS-117 Dome", 0),
    (BLUE_CL, "EWR Navarino", PLACES["Isla Navarino"], 0, 4000, "-blue_ewr", "FPS-117 Dome", 0),
    # ── Rouge : Port Stanley (enclave), Rio Gallegos, Rio Grande, San Julian ──
    (RED, "AD Port Stanley SA-6", A["Port Stanley"], 60, 4000, "-sa6", "Kub 2P25 ln", 270),
    (RED, "AD Port Stanley SA-15", A["Port Stanley"], 330, 2000, "-sa15", "Tor 9A331", 0),
    (RED, "AD Rio Gallegos SA-10", A["Rio Gallegos"], 60, 6000, "-sa10", "S-300PS 5P85C ln", 270),
    (RED, "AD Rio Gallegos SA-15", A["Rio Gallegos"], 200, 2000, "-sa15", "Tor 9A331", 0),
    (RED, "AD Rio Grande SA-11", A["Rio Grande"], 60, 5000, "-sa11", "SA-11 Buk LN 9A310M1", 270),
    (RED, "AD Rio Grande SA-15", A["Rio Grande"], 200, 2000, "-sa15", "Tor 9A331", 0),
    (RED, "AD San Julian SA-11", A["San Julian"], 270, 5000, "-sa11", "SA-11 Buk LN 9A310M1", 90),
    (RED, "AD San Julian SA-15", A["San Julian"], 90, 2000, "-sa15", "Tor 9A331", 0),
    # ── Rouge : terrains sans slots, courte portée seulement près du front ──
    (RED, "AD Rio Turbio SA-15", A["Rio Turbio"], 90, 1800, "-sa15", "Tor 9A331", 0),
    (RED, "AD Ushuaia SA-15", A["Ushuaia"], 90, 1800, "-sa15", "Tor 9A331", 0),
    (RED, "AD Piedrabuena SA-10", A["Comandante Luis Piedrabuena"], 0, 5000, "-sa10", "S-300PS 5P85C ln", 270),
    (RED, "AD Piedrabuena SA-15", A["Comandante Luis Piedrabuena"], 180, 2000, "-sa15", "Tor 9A331", 0),
    (RED, "AD Santa Cruz SA-11", A["Puerto Santa Cruz"], 0, 4000, "-sa11", "SA-11 Buk LN 9A310M1", 270),
    (RED, "AD Tolhuin SA-15", A["Tolhuin"], 0, 1800, "-sa15", "Tor 9A331", 0),
    # ── Rouge : guet ──
    (RED, "EWR Port Stanley", A["Port Stanley"], 90, 6000, "-ewr", "55G6 EWR", 0),
    (RED, "EWR Rio Gallegos", A["Rio Gallegos"], 20, 5000, "-ewr", "55G6 EWR", 0),
    (RED, "EWR Rio Grande", A["Rio Grande"], 20, 5000, "-ewr", "55G6 EWR", 0),
    (RED, "EWR San Julian", A["San Julian"], 20, 5000, "-ewr", "55G6 EWR", 0),
    (RED, "EWR Santa Cruz", A["Puerto Santa Cruz"], 90, 7000, "-ewr", "55G6 EWR", 0),
]

if __name__ == "__main__":
    b = Batch()
    for side, name, c, brg, dist, alias, carrier, hdg in SITES:
        p = spot(c, brg, dist, name, margin=300)
        land(p, name, margin=300)
        tag = name.replace("AD ", "").replace("EWR ", "EWR-").replace(" ", "-")
        cmd = f"{alias}, hdg {hdg}" + {"UK": ", country uk", "Chile": ", country chile"}.get(side["country_name"], "")
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p), keep_position=True,
              units=[interp_unit(cmd, carrier, tag)])
        print(f"{name:30} {round(p[0]):>8} {round(p[1]):>8}")
    b.save("06-defense.json")
