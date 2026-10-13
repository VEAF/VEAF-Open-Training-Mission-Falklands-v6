"""Lot 08 : les vraies zones de combat, côté rouge (training: false), et le drone laser Reaper 2.

17 zones : front 3, SEAD 3, convois en mouvement 3, frappes dans la profondeur 4, OCA 2, antinavire 2 ; 7 aux
Falkland (Z01, Z04, Z07, Z14, Z16 et les crêtes), 10 sur le continent.
Lieux réels (tools/places.json, geocode, ou coordonnées géographiques) ; chaque position est ramenée sur la terre
ferme (grille DCS) ; les navires sont contrôlés en pleine mer. Portée des SAM de zone (aucune zone n'est active au
démarrage) : check_portees.py mesure chaque zone contre les bases amies, les FARP, les pistes de ravitailleurs et les
zones d'entraînement. Près de Mount Pleasant (Z01, Z04, Z07, Z14, Z16) : courte portée seulement, SA-6 au plus.
Reaper 2 tourne sur le front de Rio Turbio (Z02), zone sans SAM au-delà de 10 km.
Les routes des convois (Z07, Z08, Z09) sont recalées sur la route par fix_convoys_on_road.py (point que DCS donne par
land.getClosestPointOnRoads), puis passées en « On Road ».
"""
from lib import (AIRFIELDS, BLUE, PLACES, RED, Batch, cmd_unit, land, ll, nm, off, position_text, sea, spot,
                 tankers_text, xy)
from roads import convoy_route

A = AIRFIELDS
P = PLACES


def g_fake(c, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    out = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(c, brg, dist, f"{tagbase}-{i}")
        out.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                    "units": [cmd_unit(alias + ", country russia", carrier, f"{tagbase}-{i}", extra)]})
    return out


def g_native(c, name, brg, dist, units, route=None):
    p = spot(c, brg, dist, name)
    g = {"name": name, "position": xy(p), "keep_position": True, "units": units}
    if route:
        g["route"] = [xy(p)] + [xy(q) for q in route]
    return g


def s_items(c, items):
    """Statiques : (type, relèvement, distance)."""
    return [(typ, spot(c, brg, dist, typ)) for typ, brg, dist in items]


def zones():
    Z = []

    def zone(name, c, r, fname, menu, text, groups, statics=(), side=RED, cat="vehicle", extra=()):
        Z.append((name, c, r, fname, menu, text, side, cat, groups, list(statics), list(extra)))

    # ── Front ────────────────────────────────────────────────────────────────
    C = spot(((P["Mount Longdon"][0] + P["Wireless Ridge"][0]) / 2, (P["Mount Longdon"][1] + P["Wireless Ridge"][1]) / 2),
             0, 0, "crêtes de Stanley")
    zone("combatZone_CretesStanley", C, 2500, "Z01 Front des îles — crêtes de Mount Longdon et Wireless Ridge", "Front",
         "Les crêtes à l'ouest de Port Stanley, tenues par une brigade mécanisée rouge : chars, blindés et "
         f"lance-roquettes en position, à {nm(C, A['Mount Pleasant']):.0f} nm de Mount Pleasant. Détruire les blindés "
         "et l'artillerie ; défense courte portée (SA-15, SA-13) et artillerie antiaérienne, sous la QRA de Port Stanley.",
         g_fake(C, [("-armor, defense 2", "T-72B", 0, 800, ""), ("-armor, defense 1", "T-72B", 120, 900, ""),
                    ("-sa15", "Tor 9A331", 90, 600, "#spawnchance=50"), ("-sa13", "Strela-10M3", 240, 700, ""),
                    ("-zu23", "Ural-375 ZU-23", 300, 1200, "")], "Z01")
         + [g_native(C, "Artillerie", 90, 1300, [{"type": "SAU Msta", "count": 3}])],
         s_items(C, [(".Command Center", 60, 1500), ("Fuel tank", 70, 1700)]))

    C = spot(off(ll(-51.5342, -72.2976), 90, 8000), 0, 0, "Rio Turbio")
    zone("combatZone_RioTurbio", C, 2500, "Z02 Front de Patagonie — frontière de Rio Turbio", "Front",
         f"La ligne de défense rouge de Rio Turbio, à {nm(C, A['Puerto Natales']):.0f} nm de Puerto Natales, côté "
         "argentin : chars enterrés, blindés et artillerie automotrice. Défense courte portée seulement (SA-13, "
         "Shilka) : le drone Reaper 2 la désigne au laser.",
         g_fake(C, [("-armor, defense 1", "T-72B", 30, 800, ""), ("-armor, defense 0", "BMP-2", 150, 900, ""),
                    ("-sa13", "Strela-10M3", 270, 700, ""), ("-shilka", "ZSU-23-4 Shilka", 90, 500, "")], "Z02")
         + [g_native(C, "Artillerie", 210, 1200, [{"type": "SAU Msta", "count": 3}])],
         s_items(C, [("Barracks 2", 330, 1300), ("Barracks 2", 340, 1500)]))

    C = spot(ll(-52.82, -68.60), 0, 0, "San Sebastián")
    zone("combatZone_SanSebastian", C, 2500, "Z03 Front de Terre de Feu — carrefour de San Sebastián", "Front",
         "Le poste frontière de San Sebastián, sur la route de Rio Grande, face au Chili : une brigade mécanisée "
         "rouge et ses lance-roquettes. Détruire les blindés et les Grad ; défense SA-8 et artillerie "
         f"antiaérienne. Aucune QRA ne couvre le secteur (Rio Grande est à {nm(C, A['Rio Grande']):.0f} nm).",
         g_fake(C, [("-armor, defense 2", "T-72B", 330, 800, ""), ("-armor, defense 1", "BMP-2", 90, 900, ""),
                    ("-sa8", "Osa 9A33 ln", 200, 600, ""), ("-zu23", "Ural-375 ZU-23", 30, 1000, "")], "Z03")
         + [g_native(C, "Lance-roquettes", 250, 1300, [{"type": "Grad-URAL", "count": 4}])],
         s_items(C, [("Bunker", 0, 400), ("Bunker", 120, 450), ("Bunker", 240, 420)]))

    # ── SEAD ─────────────────────────────────────────────────────────────────
    C = spot(P["Mount Kent"], 0, 0, "Mount Kent")
    zone("combatZone_MountKent", C, 2000, "Z04 SEAD — site SA-6 du Mount Kent", "SEAD",
         "Le site SA-6 perché sur Mount Kent, au-dessus de la vallée de Stanley, relié à un radar d'alerte avancée "
         f"en réseau Skynet, à {nm(C, A['Mount Pleasant']):.0f} nm de Mount Pleasant. Détruire le radar de conduite "
         "de tir et les lanceurs ; un Shilka protège le site.",
         g_fake(C, [("-sa6", "Kub 2P25 ln", 0, 0, ""), ("-ewr", "55G6 EWR", 90, 1500, ""),
                    ("-shilka", "ZSU-23-4 Shilka", 200, 500, "")], "Z04"))

    C = spot(P["Pali Aike"], 0, 0, "Pali Aike")
    zone("combatZone_PaliAike", C, 2000, "Z05 SEAD — site SA-11 de Pali Aike", "SEAD",
         "Le site sol-air qui couvre la steppe de Pali Aike, entre Rio Gallegos et la frontière : une batterie "
         "SA-11 ou SA-6 tirée au sort, son radar d'alerte avancée et un Shilka. Sous la couverture lointaine du "
         "SA-10 de Rio Gallegos.",
         g_fake(C, [("-sa11", "SA-11 Buk LN 9A310M1", 0, 0, '#spawngroup="Z05MR" #spawncount=1'),
                    ("-sa6", "Kub 2P25 ln", 60, 300, '#spawngroup="Z05MR" #spawncount=1'),
                    ("-ewr", "55G6 EWR", 180, 1200, ""), ("-shilka", "ZSU-23-4 Shilka", 300, 500, "")], "Z05"))

    C = spot(off(A["Rio Grande"], 150, 12000), 0, 0, "Rio Grande SAM")
    zone("combatZone_RioGrandeSAM", C, 2000, "Z06 SEAD — site SA-11 de Rio Grande", "SEAD",
         "Le site SA-11 au sud-sud-est de Rio Grande, sur la côte atlantique de la Terre de Feu, avec son radar "
         "d'alerte avancée en réseau Skynet et un SA-15. Détruire le radar de conduite de tir et les lanceurs.",
         g_fake(C, [("-sa11", "SA-11 Buk LN 9A310M1", 0, 0, ""), ("-ewr", "55G6 EWR", 90, 1500, ""),
                    ("-sa15", "Tor 9A331", 200, 600, "")], "Z06"))

    # ── Convois en mouvement (un groupe natif, route sur route, AAA dans le groupe) ──
    # Routes : tronçon du chemin par la route que DCS donne entre deux lieux (roads.convoy_route, relevé en jeu).
    R = convoy_route("stanley-fitzroy", P["Stanley"], P["Fitzroy"], 2, 33)
    C = R[0]
    zone("combatZone_ConvoiStanley", C, 1500, "Z07 Convoi — Stanley vers Fitzroy", "Convois",
         "Un convoi de renforts quitte Port Stanley par la route de Fitzroy, vers le sud-ouest. L'arrêter avant "
         f"Fitzroy, à {nm(R[-1], A['Mount Pleasant']):.0f} nm de Mount Pleasant ; il porte sa propre artillerie "
         "antiaérienne (ZU-23) et un SA-9.",
         [{"name": "Convoi", "position": xy(C), "keep_position": True,
           "units": [{"type": "BTR-80", "count": 1}, {"type": "Ural-375", "count": 4},
                     {"type": "Ural-375 ZU-23", "count": 1}, {"type": "Strela-1 9P31", "count": 1}],
           "route": [xy(q) for q in R]}])

    R = convoy_route("gallegos-piedrabuena", P["Rio Gallegos"], P["Comandante Luis Piedrabuena"], 10, 60)
    C = R[0]
    zone("combatZone_ConvoiRuta3", C, 1500, "Z08 Convoi — route 3, de Rio Gallegos vers Piedrabuena", "Convois",
         "Un convoi blindé quitte Rio Gallegos par la route 3 vers Piedrabuena pour renforcer le nord. Le détruire "
         "en route ; il est escorté par un SA-13, sous la QRA de Rio Gallegos au départ.",
         [{"name": "Convoi", "position": xy(C), "keep_position": True,
           "units": [{"type": "T-72B", "count": 2}, {"type": "BMP-2", "count": 2}, {"type": "Ural-375", "count": 2},
                     {"type": "Strela-10M3", "count": 1}],
           "route": [xy(q) for q in R]}])

    R = convoy_route("riogrande-tolhuin", P["Rio Grande"], P["Tolhuin"], 8, 60)
    C = R[0]
    zone("combatZone_ConvoiTolhuin", C, 1500, "Z09 Convoi — route 3, de Rio Grande vers Tolhuin", "Convois",
         "Un convoi de carburant roule de Rio Grande vers Tolhuin, sur la route 3 de Terre de Feu, pour ravitailler "
         "le front de San Sebastián et du canal Beagle. Le détruire avant Tolhuin ; il porte sa propre artillerie "
         "antiaérienne.",
         [{"name": "Convoi", "position": xy(C), "keep_position": True,
           "units": [{"type": "BTR-80", "count": 1}, {"type": "ATZ-10", "count": 3},
                     {"type": "Ural-375 ZU-23", "count": 1}],
           "route": [xy(q) for q in R]}])

    # ── Frappes dans la profondeur ───────────────────────────────────────────
    C = spot(P["Rio Gallegos"], 0, 0, "Rio Gallegos")
    zone("combatZone_EtatMajorGallegos", C, 1500, "Z10 Frappe — état-major de Rio Gallegos", "Frappes en profondeur",
         "Le poste de commandement rouge du sud de la Patagonie, dans les faubourgs de Rio Gallegos : bunkers, centre "
         "de transmissions, dépôt de carburant. Tout détruire ; défense SA-15 et Shilka, sous la QRA et le SA-10 "
         "de Rio Gallegos.",
         g_fake(C, [("-sa15", "Tor 9A331", 200, 600, ""), ("-shilka", "ZSU-23-4 Shilka", 60, 400, "")], "Z10")
         + [g_native(C, "PC mobile", 300, 300, [{"type": "SKP-11", "count": 2}, {"type": "Ural-375 PBU", "count": 1}])],
         s_items(C, [(".Command Center", 0, 0), ("Bunker", 90, 200), ("Bunker", 180, 200), ("Bunker", 270, 200),
                     ("Comms tower M", 45, 250), ("Military staff", 135, 250), ("Fuel tank", 225, 300)]))

    C = spot(P["Puerto Santa Cruz"], 0, 0, "Puerto Santa Cruz")
    zone("combatZone_PortSantaCruz", C, 1500, "Z11 Frappe — port de Puerto Santa Cruz", "Frappes en profondeur",
         "Le port de Puerto Santa Cruz, au bord de l'estuaire : entrepôts de munitions et de matériel, réservoirs. "
         "Tout détruire ; ZU-23 sur place, sous le SA-11 permanent de la ville.",
         g_fake(C, [("-zu23", "Ural-375 ZU-23", 0, 300, ""), ("-zu23", "Ural-375 ZU-23", 180, 300, "")], "Z11"),
         s_items(C, [("Warehouse", 30, 150), ("Warehouse", 60, 200), ("Warehouse", 90, 150), ("Tank", 120, 200),
                     ("Tank", 140, 250), ("Electric power box", 240, 120), ("Workshop A", 300, 150)]))

    C = spot(P["Ushuaia"], 0, 0, "Ushuaia")
    zone("combatZone_BaseNavaleUshuaia", C, 1500, "Z12 Frappe — base navale d'Ushuaia", "Frappes en profondeur",
         "La base navale d'Ushuaia, sur le canal Beagle, à 24 nm de Puerto Williams : entrepôts, dépôts de carburant, "
         "poste de commandement. Tout détruire ; défense courte portée seulement (SA-15 permanent de la base, "
         f"ZU-23), hors de la QRA de Rio Grande ({nm(C, A['Rio Grande']):.0f} nm).",
         g_fake(C, [("-zu23", "Ural-375 ZU-23", 0, 300, ""), ("-zu23", "Ural-375 ZU-23", 180, 300, ""),
                    ("-shilka", "ZSU-23-4 Shilka", 90, 400, "")], "Z12"),
         s_items(C, [(".Command Center", 0, 0), ("Warehouse", 90, 200), ("Warehouse", 120, 250), ("Fuel tank", 180, 250),
                     ("Fuel tank", 200, 300), ("Comms tower M", 270, 250), ("Barracks 2", 330, 300)]))

    C = spot(off(A["Rio Chico"], 270, 5000), 0, 0, "Rio Chico")
    zone("combatZone_ScudRioChico", C, 1500, "Z13 Frappe — base de missiles sol-sol de Rio Chico", "Frappes en profondeur",
         "Une base de missiles sol-sol à l'ouest de Rio Chico, d'où les Scud menacent Punta Arenas : "
         "lanceurs et camions de ravitaillement. Détruire les lanceurs ; défense SA-15 et Shilka.",
         [g_native(C, "Lanceurs", 0, 0, [{"type": "Scud_B", "count": 3}, {"type": "Ural-375", "count": 2}])]
         + g_fake(C, [("-sa15", "Tor 9A331", 200, 600, ""), ("-shilka", "ZSU-23-4 Shilka", 60, 400, "")], "Z13"),
         s_items(C, [("Bunker", 300, 300), ("Military staff", 320, 400)]))

    # ── Bases aériennes (OCA) ────────────────────────────────────────────────
    C = spot(off(A["Port Stanley"], 180, 900), 0, 0, "Port Stanley")   # au sud, hors du SA-15 permanent (2 km au nord)
    zone("combatZone_PortStanley", C, 800, "Z14 OCA — base aérienne de Port Stanley", "Bases aériennes",
         "L'aérodrome de Port Stanley, tenu par le rouge à 27 nm de Mount Pleasant : chasseurs-bombardiers au "
         "parking, hangars et carburant. Tout détruire au sol ; défense SA-15 et Shilka, sous la QRA de la base.",
         g_fake(C, [("-sa15", "Tor 9A331", 90, 900, ""), ("-shilka", "ZSU-23-4 Shilka", 270, 700, "")], "Z14"),
         s_items(C, [("Su-24M", 0, 300), ("Su-24M", 15, 340), ("MiG-29S", 40, 300), ("MiG-29S", 50, 340),
                     ("Hangar A", 330, 300), ("Fuel tank", 180, 400)]))

    C = spot(off(A["Comandante Luis Piedrabuena"], 90, 600), 0, 0, "Piedrabuena")
    zone("combatZone_Piedrabuena", C, 1500, "Z15 OCA — base aérienne de Piedrabuena", "Bases aériennes",
         "L'aérodrome de Comandante Luis Piedrabuena, plateforme rouge du nord de la Patagonie : avions de transport "
         "et hélicoptères d'attaque au sol, hangars. Tout détruire au sol ; défense SA-6 et ZU-23, plus le SA-10 "
         "et le SA-15 permanents de la base.",
         g_fake(C, [("-sa6", "Kub 2P25 ln", 90, 1000, ""), ("-zu23", "Ural-375 ZU-23", 270, 600, "")], "Z15"),
         s_items(C, [("IL-76MD", 0, 300), ("IL-76MD", 20, 380), ("Mi-24V", 300, 250), ("Mi-24V", 310, 290),
                     ("Mi-8MT", 330, 250), ("Hangar A", 180, 300), ("Fuel tank", 200, 400)]))

    # ── Antinavire ───────────────────────────────────────────────────────────
    C = (95000, 125000)
    zone("combatZone_BlocusStanley", C, 6000, "Z16 Antinavire — corvettes devant Port Stanley", "Antinavire",
         f"Trois frégates rouges croisent à l'est de Port Stanley, à {nm(C, A['Port Stanley']):.0f} nm au "
         "large de la baie, pour couvrir l'enclave et couper la route de la flotte bleue. Les couler : frégates à "
         "défense courte portée.",
         [{"name": "Frégates", "position": xy(C), "keep_position": True, "patrol": True,
           "units": [{"type": "NEUSTRASH", "count": 1}, {"type": "REZKY", "count": 2}],
           "route": [xy(C), xy((90000, 140000))]}], cat="ship")

    C = (-285000, -360000)
    zone("combatZone_DetroitLeMaire", C, 6000, "Z17 Antinavire — escadre du détroit de Le Maire", "Antinavire",
         "Le croiseur lance-missiles rouge Moskva et deux frégates croisent dans le détroit de Le Maire, entre la "
         "Terre de Feu et l'île des États, pour fermer l'accès à la mer de la Terre de Feu. Les couler : le "
         "Moskva porte des missiles sol-air à 40 nm, les frégates à courte portée.",
         [{"name": "Escadre", "position": xy(C), "keep_position": True, "patrol": True,
           "units": [{"type": "MOSCOW", "count": 1}, {"type": "NEUSTRASH", "count": 1}, {"type": "REZKY", "count": 1}],
           "route": [xy(C), xy((-270000, -350000))]}], cat="ship")
    return Z


if __name__ == "__main__":
    b = Batch()
    for name, c, r, fname, menu, text, side, cat, groups, statics, extra in zones():
        if cat == "ship":
            sea(c, name, margin=1500)
        for g in groups:
            for q in g.get("route") or []:
                (sea if cat == "ship" else land)((q["x"], q["y"]), f"{name} route", 1000 if cat == "ship" else 100)
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": False,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **side,
              category=cat, combat_zone=cz)
        for i, (typ, p) in enumerate(statics, 1):
            b.act("add_group", **side, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
                  position=xy(p), units=[{"type": typ}], for_combat_zone=name, keep_position=True)
        for gname, p, units in extra:
            b.act("add_group", **side, category="vehicle", name=gname, position=xy(p), units=units,
                  for_combat_zone=name, keep_position=True)
        print(f"{fname:70} {round(c[0]):>8} {round(c[1]):>8}  r={r}")
    # Drone laser sur le front de Rio Turbio (SA-13 et Shilka seulement)
    b.act("add_air_group", **BLUE, name="Reaper 2", unit_type="MQ-9 Reaper", count=1, start="air",
          position=xy(spot(off(ll(-51.5342, -72.2976), 90, 8000), 0, 0, "Reaper 2")), altitude_ft=10000, speed_kt=110,
          task="AFAC", skill="High")
    b.save("08-zones.json")
