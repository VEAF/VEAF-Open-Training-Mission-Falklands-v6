"""Lot 11 : configuration de mission.yaml — identité, profils, modules, ASSETS, SANCTUARY, missions scénarisées,
réglages CTLD. Se rejoue sans doublon (il écrit des blocs, il n'ajoute pas de groupes).

Un nom partout : nom de groupe = indicatif = libellé de preset = texte ASSETS. Chaque camp ne voit que ses
moyens (coalition). Drones : code laser imposé et fréquence que CTLD calcule pour ce code (35.55 / 35.6 FM,
mesuré sur Syrie v6, limitation ctld-jtac-imposed-code-and-radio), sous un jtacLaserCodeMax abaissé à 1686.
CTLD : rayon logistique des aérodromes laissé à 250 m, la valeur par défaut (décision de David, 13/10/2026).
Météo : pas de variantes (le serveur VEAF fixe météo et heure, décision de David du 12/10/2026) ; une météo de
base plausible est posée par gen_15_identite.py.
"""
import sys
from pathlib import Path

from ruamel.yaml import YAML

from gen_10_joueurs import SANCTUARIES
from lib import AIRFIELDS, M, ROOT, nm

sys.stdout.reconfigure(encoding="utf-8")

ST_MP = nm(AIRFIELDS["Port Stanley"], AIRFIELDS["Mount Pleasant"])

ASSETS = [
    ("Overlord 1", "Overlord 1 (E-3A) — AWACS îles", "BLUE", "U282.0 — FL300 — orbite est-ouest à l'ouest de la Falkland occidentale", "Overlord 1 - Escort"),
    ("Magic 1", "Magic 1 (E-3A) — AWACS Chili", "BLUE", "U283.0 — FL300 — orbite nord-sud au-dessus de Porvenir et de Punta Arenas", "Magic 1 - Escort"),
    ("Texaco 1", "Texaco 1 (KC-135, perche) — îles", "BLUE", "TACAN 50Y TX1 — U290.0 — FL220 — piste nord-sud au sud des Falkland, au large de Gull Point", "Texaco 1 - Escort"),
    ("Arco 1", "Arco 1 (KC-135 MPRS, panier) — îles", "BLUE", "TACAN 51Y AR1 — U291.0 — FL180 — piste nord-sud au sud des Falkland, plus au large", "Arco 1 - Escort"),
    ("Texaco 2", "Texaco 2 (KC-135, perche) — Chili", "BLUE", "TACAN 52Y TX2 — U292.0 — FL240 — piste nord-sud à l'ouest de Punta Arenas, au-dessus des fjords", "Texaco 2 - Escort"),
    ("Arco 2", "Arco 2 (KC-135 MPRS, panier) — Chili", "BLUE", "TACAN 53Y AR2 — U293.0 — FL200 — piste nord-sud au sud-ouest de Puerto Natales", "Arco 2 - Escort"),
    ("CSG-74 Stennis", "CVN-74 Stennis — Atlantique sud, au sud des Falkland", "BLUE", "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", None),
    ("CSG-71 Roosevelt", "CVN-71 Roosevelt — Atlantique sud, au large de la Terre de Feu", "BLUE", "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", None),
    ("CSG-74 Stennis S3B-Tanker", "S-3B du Stennis (ravitailleur embarqué)", "BLUE", "TACAN 56Y S74 — U296.0", None),
    ("CSG-71 Roosevelt S3B-Tanker", "S-3B du Roosevelt (ravitailleur embarqué)", "BLUE", "TACAN 57Y S71 — U297.0", None),
    ("Darkstar 1", "Darkstar 1 (E-3A) — AWACS bleu de l'arène", "BLUE", "U285.0 — FL300", None),
    ("Wizard 1", "Wizard 1 (A-50) — AWACS rouge", "RED", "U284.0 — FL300 — orbite est-ouest au large de la Terre de Feu argentine", "Wizard 1 - Escort"),
    ("Shell 1", "Shell 1 (IL-78M) — ravitailleur rouge", "RED", "U294.0 — FL200 — orbite nord-sud au large de Rio Gallegos", "Shell 1 - Escort"),
    ("Focus 1", "Focus 1 (A-50) — AWACS rouge de l'arène", "RED", "U286.0 — FL300", None),
]
DRONES = [
    ("Reaper 1", "Reaper 1 (drone laser) — champ de tir d'attaque", 1511, "35.55",
     "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir d'attaque (zone A), à l'ouest de la Falkland occidentale."),
    ("Reaper 2", "Reaper 2 (drone laser) — front de Rio Turbio", 1512, "35.6",
     "Laser 1512 — FM 35.6. 3 000 m sol au-dessus de la ligne de Rio Turbio (Z02)."),
]

COMBAT_MISSIONS = [
    {"name": "Defense-MountPleasant", "friendly_name": "Défense — raid rouge sur Mount Pleasant", "secured": False,
     "briefing": "Deux Su-24M armés de missiles antiradar ouvrent la route à quatre Su-34 chargés de bombes, escortés "
                 f"de deux Su-30, partis de l'est de Port Stanley vers la base de Mount Pleasant, {ST_MP:.0f} nm plus à l'ouest. "
                 "Abattez les bombardiers avant le largage.\nÉchec si la base est bombardée (constaté par vous : la "
                 "mission ne le vérifie pas).",
     "elements": [{"name": "SEAD", "groups": ["SC-Defense-MountPleasant-SEAD"], "scalable": False},
                  {"name": "Bombardiers", "groups": ["SC-Defense-MountPleasant-Bombers"], "scalable": False},
                  {"name": "Escorte", "groups": ["SC-Defense-MountPleasant-Escort"], "scalable": True}]},
    {"name": "Interception-VIP", "friendly_name": "Interception — transport VIP de Rio Gallegos à Rio Grande",
     "secured": False,
     "briefing": "Un IL-76 emmène l'état-major rouge de Rio Gallegos vers Rio Grande, escorté par deux MiG-29S, en "
                 "longeant la côte par le cap Vierges. Interceptez-le avant Rio Grande : la fin de la route est sous "
                 "la QRA et les défenses de Rio Grande.",
     "elements": [{"name": "Transport", "groups": ["SC-Intercept-VIP-Il76"], "scalable": False},
                  {"name": "Escorte", "groups": ["SC-Intercept-VIP-Escort"], "scalable": True}]},
]

if __name__ == "__main__":
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    path = Path(M) / "mission.yaml"
    d = yaml.load(path.read_text(encoding="utf-8"))

    if "global_log_level" in d:
        d["global_log_level"] = "info"
    else:
        d.insert(0, "global_log_level", "info")
    mi = d["mission"]
    mi["name"] = "VEAF_OpenTraining_Falklands_ICAO_EGYP"
    mi.yaml_add_eol_comment("EGYP = Mount Pleasant (base mère), METAR vivant vérifié le 13/10/2026", "name")
    mi["era"] = "MODERN"
    mi["language"] = "fr"
    mi["silence_atc_on_all_airbases"] = True
    mi["hide_names_from_spawned_groups"] = True

    mods = d["modules"]
    mods["SKYNET"] = {"enabled": True, "spotter_network": True, "spotter_view": "off"}
    assets = []
    for i, (name, desc, side, info, linked) in enumerate(ASSETS, 1):
        a = {"sort": i, "name": name, "description": desc, "coalition": side, "information": info}
        if linked:
            a["linked"] = linked
        assets.append(a)
    for name, desc, code, freq, info in DRONES:
        assets.append({"sort": len(assets) + 1, "name": name, "description": desc, "coalition": "BLUE",
                       "information": info, "jtac": code, "freq": freq, "mod": "FM"})
    mods["ASSETS"] = {"enabled": True, "assets": assets}
    mods["SANCTUARY"] = {"enabled": True, "sanctuary_zones": [
        {"name": n, "trigger_zone": z, "coalition": side, "delay_warning": 0, "delay_instant": 60,
         "protect_from_missiles": True} for n, z, c, r, side in SANCTUARIES]}

    d["pipeline"] = {"weather": False}
    d.yaml_add_eol_comment("pas de variantes météo : le serveur VEAF fixe météo et heure (David, 12/10/2026)", "pipeline")
    d["profiles"] = {"LOCAL_TEST": {"global_log_level": "debug", "security": {"disabled": True},
                                    "mission": {"hide_names_from_spawned_groups": False}}}
    d["combat_missions"] = COMBAT_MISSIONS
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(d, f)
    print("mission.yaml écrit")

    v = ROOT / "src/versions.yaml"
    if v.exists():
        v.unlink()
        print("src/versions.yaml supprimé (pas de variantes)")

    ctld = Path(M) / "ctld-config.yaml"
    c = ctld.read_text(encoding="utf-8")
    old = "  jtacLaserCodeMax: 1688\n"
    if old in c:
        c = c.replace(old, "  jtacLaserCodeMax: 1686   # codes imposés des drones (1511, 1512) sous le maximum, comme Syrie v6 (limitation ctld-jtac-imposed-code-and-radio)\n")
        ctld.write_text(c, encoding="utf-8")
    assert "jtacLaserCodeMax: 1686" in ctld.read_text(encoding="utf-8")
    print("ctld-config : jtacLaserCodeMax 1686")
