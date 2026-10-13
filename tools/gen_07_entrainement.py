"""Lot 07 : les 3 familles d'entraînement × 3 niveaux (facile ⊂ moyen ⊂ difficile, clé `includes:`), et les trois
zones touristiques.

Les trois champs sont sur la Falkland occidentale (bleue, sans aérodrome : FARP Port Howard), loin du front de
Stanley (plus de 75 nm de Mount Kent pour A, davantage pour S) :
H — hélicoptères, plateau à 17 km (9 nm) du FARP Port Howard ; le difficile s'arrête au SA-13 et aux SA-18.
A — attaque, à l'ouest de Mount Adam, 79 nm de Mount Kent. Le Reaper 1 tourne au-dessus.
S — SEAD, au sud-ouest, à plus de 60 km de A et de tout le reste (SA-11 au plus, 27 nm). Pas de longue portée
    (décision du 01/10/2026).
T — tourisme, hors combat (training, non complétable), trois sites : T1 Torres del Paine depuis le FARP Torres del
    Paine (Chili) ; T2 le cap Horn depuis Puerto Williams ; T3 les Falkland occidentales depuis le FARP Port
    Howard. Les balises radio et les guides (messages au survol) sont permanents (gen_07b, gen_07c).
Toutes les distances des briefings sont calculées ici, pas tapées.

Cibles inertes des niveaux faciles : groupes d'un véhicule nommés « …-Inert-… », rendus chauds, tir interdit
et sans dispersion par tools/inert_targets.py (aucune action MCP ne règle ROE ni dispersion).
"""
from lib import (AIRFIELDS, BLUE_CL, BLUE_UK, PLACES, RED, Batch, cmd_unit, compass, ll, nm, off, position_text,
                 spot, tankers_text, xy)

P = PLACES
H = (78250, -38750)    # centres posés sur du terrain plat (lib.flat_spot, rayon 500 m)
A = (95250, -74000)
S = (43750, -106750)
FARP_PH = (88000, -32250)         # gen_05b
FARP_TORRES = (39927, -960794)    # gen_05b
# Tourisme
T1 = (45094, -963184)             # steppe au pied des Tours, terrain plat (accueil des autocars)
T2 = off(AIRFIELDS['Puerto Williams'], 60, 6000)  # accueil à l'est de la ville, hors de la défense de la base
T3 = (120000, -67000)             # Port Egmont, île Saunders : terrain plat sur la rive
MOUNT_KENT = P["Mount Kent"]


def inert(zone_center, items, prefix):
    """Groupes d'un véhicule, en couronne autour du centre : (type, relèvement, distance)."""
    groups = []
    for i, (typ, brg, dist) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{prefix}{i}")
        groups.append({"name": f"Inert-{typ.split()[0]}-{i}", "position": xy(p), "keep_position": True,
                       "units": [{"type": typ, "count": 1}]})
    return groups


def fake(zone_center, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    groups = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{tagbase}-{i}")
        groups.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                       "units": [cmd_unit(alias + ", country russia", carrier, f"{tagbase}-{i}", extra)]})
    return groups


def zones():
    return [
        # ── H : hélicoptères ──
        ("combatZone_PortHoward_Easy", H, 2500, "H1 Hélico Port Howard — facile", "Entraînement hélicoptères", None,
         inert(H, [("T-72B", 0, 600), ("T-72B", 60, 700), ("BMP-2", 120, 500), ("BMP-2", 180, 800),
                   ("BRDM-2", 240, 600), ("Ural-375", 300, 700), ("Ural-375", 330, 400)], "H1-"),
         f"Champ de tir hélicoptères de la Falkland occidentale, à {nm(H, FARP_PH):.0f} nm au sud-ouest du FARP Port "
         "Howard : cibles inertes (chars, blindés et camions immobiles, tir interdit)."),
        ("combatZone_PortHoward_Medium", H, 2500, "H2 Hélico Port Howard — moyen", "Entraînement hélicoptères",
         "combatZone_PortHoward_Easy",
         fake(H, [("-zu23", "Ural-375 ZU-23", 210, 1200, '#spawngroup="H2AAA" #spawncount=2'),
                  ("-zu23", "Ural-375 ZU-23", 270, 1100, '#spawngroup="H2AAA" #spawncount=2'),
                  ("-zu23", "Ural-375 ZU-23", 150, 1300, '#spawngroup="H2AAA" #spawncount=2'),
                  ("-shilka", "ZSU-23-4 Shilka", 240, 900, "#spawnchance=50")], "H2"),
         "Champ de tir hélicoptères de la Falkland occidentale : de l'artillerie antiaérienne légère (ZU-23, parfois "
         "un Shilka) en plus des cibles du niveau facile."),
        ("combatZone_PortHoward_Hard", H, 2500, "H3 Hélico Port Howard — difficile", "Entraînement hélicoptères",
         "combatZone_PortHoward_Medium",
         fake(H, [("-sa13", "Strela-10M3", 200, 1000, '#spawngroup="H3SR" #spawncount=1'),
                  ("-sa13", "Strela-10M3", 250, 1000, '#spawngroup="H3SR" #spawncount=1'),
                  ("-sa18", "SA-18 Igla manpad", 220, 1500, '#spawngroup="H3MP" #spawncount=1'),
                  ("-sa18", "SA-18 Igla manpad", 180, 1400, '#spawngroup="H3MP" #spawncount=1')], "H3"),
         "Champ de tir hélicoptères de la Falkland occidentale, avec une défense courte portée réaliste : un SA-13 "
         "et une équipe de lance-missiles portatifs SA-18, à guidage infrarouge."),
        # ── A : attaque ──
        ("combatZone_MountAdam_Easy", A, 2500, "A1 Attaque Mount Adam — facile", "Entraînement attaque", None,
         inert(A, [("T-72B", 0, 700), ("T-72B", 40, 900), ("T-72B", 80, 600), ("BMP-2", 120, 800),
                   ("BMP-2", 160, 500), ("BTR-80", 200, 700), ("BTR-80", 240, 900), ("Ural-375", 280, 600),
                   ("Ural-375", 320, 800), ("KAMAZ Truck", 350, 400)], "A1-"),
         f"Champ de tir air-sol à l'ouest de Mount Adam, sur la Falkland occidentale, à {nm(A, MOUNT_KENT):.0f} nm "
         "du front de Stanley : blindés et camions immobiles en tir interdit, dépôt de carburant et poste de "
         "commandement. Le drone Reaper 1 tourne au-dessus."),
        ("combatZone_MountAdam_Medium", A, 2500, "A2 Attaque Mount Adam — moyen", "Entraînement attaque",
         "combatZone_MountAdam_Easy",
         fake(A, [("-armor, defense 0", "T-72B", 220, 1300, ""),
                  ("-zu23", "Ural-375 ZU-23", 60, 1500, '#spawngroup="A2AAA" #spawncount=1'),
                  ("-zu23", "Ural-375 ZU-23", 300, 1400, '#spawngroup="A2AAA" #spawncount=1')], "A2"),
         "Champ de tir de Mount Adam : une compagnie blindée active et de l'artillerie antiaérienne légère en "
         "plus des cibles du niveau facile."),
        ("combatZone_MountAdam_Hard", A, 2500, "A3 Attaque Mount Adam — difficile", "Entraînement attaque",
         "combatZone_MountAdam_Medium",
         fake(A, [("-armor, defense 1", "T-72B", 260, 1600, ""),
                  ("-sa13", "Strela-10M3", 200, 1200, '#spawngroup="A3SR" #spawncount=1'),
                  ("-sa9", "Strela-1 9P31", 320, 1200, '#spawngroup="A3SR" #spawncount=1'),
                  ("-shilka", "ZSU-23-4 Shilka", 250, 800, "")], "A3"),
         "Champ de tir de Mount Adam : un second groupe blindé et une défense courte portée à guidage "
         "infrarouge (SA-13 ou SA-9), avec un Shilka."),
        # ── S : SEAD ──
        ("combatZone_PortStephens_Easy", S, 3000, "S1 SEAD Port Stephens — facile", "Entraînement SEAD", None,
         fake(S, [("-sa6", "Kub 2P25 ln", 0, 0, '#spawngroup="S1MR" #spawncount=1'),
                  ("-sa11", "SA-11 Buk LN 9A310M1", 90, 300, '#spawngroup="S1MR" #spawncount=1')], "S1"),
         f"Site SEAD au sud-ouest de la Falkland occidentale, près de Port Stephens, à {nm(S, A):.0f} nm du champ "
         "de tir d'attaque : une batterie sol-air moyenne portée, SA-6 ou SA-11 tirée au sort."),
        ("combatZone_PortStephens_Medium", S, 3000, "S2 SEAD Port Stephens — moyen", "Entraînement SEAD",
         "combatZone_PortStephens_Easy",
         fake(S, [("-sa15", "Tor 9A331", 45, 1500, '#spawngroup="S2SR" #spawncount=2'),
                  ("-sa8", "Osa 9A33 ln", 165, 1500, '#spawngroup="S2SR" #spawncount=2'),
                  ("-sa15", "Tor 9A331", 285, 1500, '#spawngroup="S2SR" #spawncount=2')], "S2"),
         "Site SEAD de Port Stephens : la batterie moyenne portée est protégée par une défense courte portée "
         "(SA-15, SA-8)."),
        ("combatZone_PortStephens_Hard", S, 3000, "S3 SEAD Port Stephens — difficile", "Entraînement SEAD",
         "combatZone_PortStephens_Medium",
         fake(S, [("-ewr", "55G6 EWR", 120, 2200, "")], "S3"),
         "Site SEAD de Port Stephens en réseau Skynet : un radar d'alerte avancée guide les batteries, qui "
         "restent éteintes jusqu'au dernier moment."),
    ]


# Statiques du niveau facile attaque : ce qui ne vit pas (dépôt, poste de commandement)
A1_STATICS = [("Fuel tank", 100, 1100), ("Fuel tank", 110, 1200), (".Command Center", 20, 1300)]

TOURISM_TEXT = {
    "combatZone_Paine": (
        f"Visite aérienne de la Patagonie des glaciers, hors combat, au départ du FARP Torres del Paine "
        f"({nm(FARP_TORRES, T1):.0f} nm au {compass(FARP_TORRES, T1)}). Circuit : les tours de granit (Las Torres), les "
        "Cuernos et le Paine Grande, puis le lac Grey et son glacier, un front de la grande calotte glaciaire de "
        "Patagonie. Une balise radio FM à chaque site ; survolez un site à moins de 1 500 ft sol et un guide vous "
        "le raconte. Excursion : le glacier Perito Moreno, de l'autre côté de la frontière, en territoire rouge "
        "(aucune défense permanente)."),
    "combatZone_CapHorn": (
        "Visite aérienne du bout du monde, hors combat, au départ de Puerto Williams. Circuit : le canal Beagle, "
        "les îles Wollaston et le cap Horn. Une balise radio FM par site ; survolez-les à moins de 1 500 ft sol pour entendre le guide. Le "
        "circuit reste côté chilien, à plus de 20 nm de la base argentine d'Ushuaia."),
    "combatZone_PortEgmont": (
        f"Visite aérienne des Falkland occidentales, hors combat, au départ du FARP Port Howard "
        f"({nm(FARP_PH, T3):.0f} nm au {compass(FARP_PH, T3)}). Circuit : Pebble Island, Saunders Island et Port Egmont, Carcass "
        "Island. Une balise radio FM par site ; survolez-les à moins de 1 500 ft sol pour entendre le guide."),
}


def tourism():
    """Autocars et 4x4 au point d'accueil, bleus, hors combat."""
    return [
        ("combatZone_Paine", T1, 1500, "T1 Tourisme — Torres del Paine", "Tourisme", BLUE_CL,
         [{"name": "Autocars", "position": xy(spot(T1, 90, 600, "autocars")), "keep_position": True,
           "units": [{"type": "LAZ Bus", "count": 3}]},
          {"name": "4x4", "position": xy(spot(T1, 60, 800, "4x4")), "keep_position": True,
           "units": [{"type": "Land_Rover_101_FC", "count": 2}]}]),
        ("combatZone_CapHorn", T2, 1500, "T2 Tourisme — cap Horn", "Tourisme", BLUE_CL,
         [{"name": "4x4", "position": xy(spot(T2, 60, 500, "4x4")), "keep_position": True,
           "units": [{"type": "Land_Rover_101_FC", "count": 2}]}]),
        ("combatZone_PortEgmont", T3, 1500, "T3 Tourisme — Falkland occidentales", "Tourisme", BLUE_UK,
         [{"name": "4x4", "position": xy(spot(T3, 60, 500, "4x4")), "keep_position": True,
           "units": [{"type": "Land_Rover_101_FC", "count": 3}]}]),
    ]


if __name__ == "__main__":
    b = Batch()
    for zone, c, r, fname, menu, inc, groups, text in zones():
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": True,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        if inc:
            cz["includes"] = [inc]
        b.act("create_combat_zone", zone_name=zone, position=xy(c), radius=r, groups=groups, **RED,
              category="vehicle", combat_zone=cz)
    for i, (typ, brg, dist) in enumerate(A1_STATICS, 1):
        p = spot(A, brg, dist, f"A1-static-{i}")
        b.act("add_group", **RED, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
              position=xy(p), units=[{"type": typ}], for_combat_zone="combatZone_MountAdam_Easy",
              keep_position=True)
    for zone, c, r, fname, menu, side, groups in tourism():
        b.act("create_combat_zone", zone_name=zone, position=xy(c), radius=r, groups=groups, **side,
              category="vehicle", combat_zone={"friendly_name": fname, "radio_group_name": menu, "training": True,
                                               "completable": False,
                                               "briefing": f"{TOURISM_TEXT[zone]}\n{position_text(c)}"})
    b.save("07-entrainement.json")
