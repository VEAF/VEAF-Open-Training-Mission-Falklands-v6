"""Lot 09 : QRA (rouges, et bleues puisque le rouge est jouable) et CAP à la demande.

QRA : cercle dans le territoire du camp qui défend, réponse graduée, deux appareils différents par niveau tirés
au sort, délai 90 s, pas de réaction aux hélicoptères, pas de menu radio ouvert à tous. Départ en vol au-dessus de
la base (Falklands n'a pas de données de parking dans VMCT : describe_known_limitations,
no-parking-data-outside-three-theatres) ; refaites en décollage de la piste par le lot 09b si les parkings sont
capturés (`veaf-tools dcs capture-map --parking`).
  - Port Stanley (rouge) : 16 nm autour de l'enclave, décalé à l'est ; Mount Pleasant est à 30 nm du centre.
  - Rio Gallegos, Rio Grande, San Julian (rouges) : 25 nm autour de la base. Punta Arenas est à 102 nm de Rio
    Gallegos, Puerto Williams à 70 nm de Rio Grande.
  - Mount Pleasant, Punta Arenas, Puerto Natales (bleues) : 20 à 25 nm, centrées en retrait de la base, contre
    les joueurs rouges.
  Couloirs libres : tout l'est de la Falkland orientale hors de Stanley, la Falkland occidentale, le nord de la
  Patagonie et la mer entre les deux théâtres.
CAP rouges dans le territoire rouge, CAP bleues dans le territoire bleu.
"""
from lib import AIRFIELDS, BLUE_CL, BLUE_UK, RED, Batch, ll, xy

A = AIRFIELDS
MIG29 = {"payload": "R-73*2,R-60M*2,R-27R*2,Fuel-1500"}
SU27 = {"payload": "R-73*4,R-27ER*6"}
SU30 = {"payload": "R-73*4,R-77*4,R-27ER*2"}
F16 = {"payload": "AIM-120C*4,AIM-9M*2,ECM,Fuel*2"}
M2000 = {"payload": "R 550*2,MICA AR*4,Fuel*3"}
F15 = {"payload": "AIM-9*4,AIM-120*4,Fuel"}
F16UK = {"payload": "AIM-120C*4, AIM-9M*2, Fuel"}

QRAS = [
    dict(name="QRA Port Stanley", side=RED, zone="QRA-PortStanley", center=(89000, 100000), radius=30000,
         airfield="Port Stanley", enemy="BLUE", levels=[
             (1, [("QRA-PortStanley-MiG29", "MiG-29S", 2, MIG29), ("QRA-PortStanley-Su27", "Su-27", 2, SU27)]),
             (3, [("QRA-PortStanley-Su30", "Su-30", 2, SU30), ("QRA-PortStanley-MiG29x4", "MiG-29S", 4, MIG29)])]),
    dict(name="QRA Rio Gallegos", side=RED, zone="QRA-RioGallegos", center=A["Rio Gallegos"], radius=46300,
         airfield="Rio Gallegos", enemy="BLUE", levels=[
             (1, [("QRA-RioGallegos-Su27", "Su-27", 2, SU27), ("QRA-RioGallegos-MiG29", "MiG-29S", 2, MIG29)]),
             (3, [("QRA-RioGallegos-Su30", "Su-30", 2, SU30), ("QRA-RioGallegos-Su27x4", "Su-27", 4, SU27)])]),
    dict(name="QRA Rio Grande", side=RED, zone="QRA-RioGrande", center=A["Rio Grande"], radius=46300,
         airfield="Rio Grande", enemy="BLUE", levels=[
             (1, [("QRA-RioGrande-MiG29", "MiG-29S", 2, MIG29), ("QRA-RioGrande-Su27", "Su-27", 2, SU27)]),
             (3, [("QRA-RioGrande-Su30", "Su-30", 2, SU30), ("QRA-RioGrande-MiG29x4", "MiG-29S", 4, MIG29)])]),
    dict(name="QRA San Julian", side=RED, zone="QRA-SanJulian", center=A["San Julian"], radius=46300,
         airfield="San Julian", enemy="BLUE", levels=[
             (1, [("QRA-SanJulian-Su27", "Su-27", 2, SU27), ("QRA-SanJulian-MiG29", "MiG-29S", 2, MIG29)]),
             (3, [("QRA-SanJulian-Su30", "Su-30", 2, SU30), ("QRA-SanJulian-MiG29x4", "MiG-29S", 4, MIG29)])]),
    dict(name="QRA Mount Pleasant", side=BLUE_UK, zone="QRA-MountPleasant", center=(70000, 30000), radius=37000,
         airfield="Mount Pleasant", enemy="RED", levels=[
             (1, [("QRA-MountPleasant-F15", "F-15C", 2, F15), ("QRA-MountPleasant-F16", "F-16C bl.50", 2, F16UK)]),
             (3, [("QRA-MountPleasant-F15x4", "F-15C", 4, F15), ("QRA-MountPleasant-F16x4", "F-16C bl.50", 4, F16UK)])]),
    dict(name="QRA Punta Arenas", side=BLUE_CL, zone="QRA-PuntaArenas", center=(-155000, -795000), radius=46300,
         airfield="Punta Arenas", enemy="RED", levels=[
             (1, [("QRA-PuntaArenas-F16", "F-16C bl.52d", 2, F16), ("QRA-PuntaArenas-M2000", "Mirage 2000-5", 2, M2000)]),
             (3, [("QRA-PuntaArenas-F16x4", "F-16C bl.52d", 4, F16), ("QRA-PuntaArenas-M2000x4", "Mirage 2000-5", 4, M2000)])]),
    dict(name="QRA Puerto Natales", side=BLUE_CL, zone="QRA-PuertoNatales", center=(-35000, -945000), radius=37000,
         airfield="Puerto Natales", enemy="RED", levels=[
             (1, [("QRA-PuertoNatales-F16", "F-16C bl.52d", 2, F16), ("QRA-PuertoNatales-M2000", "Mirage 2000-5", 2, M2000)]),
             (3, [("QRA-PuertoNatales-F16x4", "F-16C bl.52d", 4, F16), ("QRA-PuertoNatales-M2000x4", "Mirage 2000-5", 4, M2000)])]),
]

# (nom, type, nombre, camp, a, b, FL, kt, emport, menu, briefing)
CAPS = [
    ("CAP-Santa-Cruz-MiG29", "MiG-29S", 2, RED, ll(-51.95, -69.10), ll(-52.10, -68.50), 220, 420, MIG29,
     "CAP rouge MiG-29S (Fox 1) — Patagonie sud — FL220",
     "Deux MiG-29S armés de R-27R, R-73 et R-60 patrouillent entre Rio Gallegos et le cap Vierges, au FL220. "
     "Emport : R-73*2,R-60M*2,R-27R*2,Fuel-1500."),
    ("CAP-Fuego-Su27", "Su-27", 2, RED, ll(-53.70, -67.60), ll(-53.30, -67.00), 260, 450, SU27,
     "CAP rouge Su-27 (Fox 1, longue portée) — Terre de Feu argentine — FL260",
     "Deux Su-27 armés de R-27ER et R-73 patrouillent au-dessus de la côte atlantique de la Terre de Feu, au "
     "nord-est de Rio Grande, au FL260. Emport : R-73*4,R-27ER*6."),
    ("CAP-Nord-MiG31", "MiG-31", 2, RED, ll(-49.60, -68.50), ll(-49.20, -67.50), 380, 520, {"payload": "R-40R*2,R-33*4"},
     "CAP rouge MiG-31 (intercepteur haut et rapide, R-33) — Patagonie nord — FL380",
     "Deux MiG-31 armés de R-33 patrouillent haut et vite entre Puerto Santa Cruz et San Julian, au FL380. "
     "Emport : R-40R*2,R-33*4."),
    ("Raid-Tu22M", "Tu-22M3", 2, RED, ll(-51.9, -70.4), ll(-52.3, -69.9), 300, 450, {"payload": "FAB-500*33"},
     "Raid rouge Tu-22M3 à intercepter — Pali Aike — FL300",
     "Deux bombardiers Tu-22M3 chargés de bombes tournent à l'ouest de Rio Gallegos, au FL300, prêts à frapper "
     "Punta Arenas : les intercepter. Emport : FAB-500*33."),
    ("CAP-Falkland-F15", "F-15C", 2, BLUE_UK, ll(-51.55, -59.70), ll(-51.85, -60.10), 250, 440, F15,
     "CAP bleue F-15C (Fox 3) — détroit des Falkland — FL250",
     "Deux F-15C britanniques couvrent le détroit des Falkland, de San Carlos à Goose Green, au FL250. "
     "Emport : AIM-9*4,AIM-120*4,Fuel."),
    ("CAP-Magellan-F16", "F-16C bl.52d", 2, BLUE_CL, ll(-53.10, -71.20), ll(-52.80, -70.60), 220, 420, F16,
     "CAP bleue F-16C (Fox 3) — détroit de Magellan — FL220",
     "Deux F-16C chiliens patrouillent le détroit de Magellan, autour de Punta Arenas, au FL220. "
     "Emport : AIM-120C*4,AIM-9M*2,ECM,Fuel*2."),
    ("CAP-Beagle-F16", "F-16C bl.52d", 2, BLUE_CL, ll(-55.10, -67.40), ll(-55.00, -68.20), 240, 420, F16,
     "CAP bleue F-16C (Fox 3) — canal Beagle — FL240",
     "Deux F-16C chiliens patrouillent au-dessus de l'île Navarino et de Puerto Williams, au FL240. "
     "Emport : AIM-120C*4,AIM-9M*2,ECM,Fuel*2."),
]

if __name__ == "__main__":
    b = Batch()
    for q in QRAS:
        groups, levels = [], []
        ap = A[q["airfield"]]
        for count, members in q["levels"]:
            names = []
            for i, (gname, typ, n, loadout) in enumerate(members):
                groups.append({"name": gname, "units": [{"type": typ, "count": n}], "start": "air",
                               "position": xy((ap[0] + 1500 * i, ap[1] + 1500 * len(names))), "altitude_ft": 5000,
                               "speed_kt": 350, "airfield": q["airfield"], **loadout})
                names.append(gname)
            levels.append({"enemy_count": count, "groups": names, "random_pick": 1})
        side = q["side"]
        b.act("create_qra", name=q["name"], coalition=side["coalition"], country_id=side["country_id"],
              country_name=side["country_name"], trigger_zone=q["zone"], position=xy(q["center"]), radius=q["radius"],
              groups=groups, enemy_coalitions=[q["enemy"]],
              qra={"groups_by_enemy_count": levels, "delay_before_activating": 90, "delay_before_rearming": 600,
                   "react_on_helicopters": False, "airport_link": q["airfield"]})
    for name, typ, n, side, a, bb, fl, kt, loadout, menu, brief in CAPS:
        b.act("create_cap_mission", mission_name=name, units=[{"type": typ, "count": n}], **side, position=xy(a),
              route=[{**xy(bb), "altitude_ft": fl * 100}], altitude_ft=fl * 100, speed_kt=kt,
              cap={"menu_name": menu, "briefing": brief}, **loadout)
    b.save("09-qra-cap.json")
