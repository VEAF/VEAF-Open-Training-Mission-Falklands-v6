"""Lot 15 : date, météo de base, bullseye commun et briefing DCS de la mission.

Le texte est composé depuis les données (fréquences DCS des aérodromes, soutien, zones), pas tapé.
`python gen_15_identite.py [suffixe]` : un lot d'identité se rejoue sans danger (set_* remplacent), d'où le suffixe
de nom de lot pour garder chaque passage.
Météo : une seule, celle de la mission (le serveur VEAF fixe météo et heure de chaque session, décision de David du
12/10/2026) ; une matinée de printemps austral plausible à Mount Pleasant (METAR EGYP du 13/10/2026 : 34022KT CAVOK
05/02 Q1020), avec un vent d'ouest et quelques nuages à 2 500 ft pour que le ciel ne soit pas vide ni au sol.
"""
import json
import math
import sys

from gen_05b_farps_porte_avions import CARRIERS, FARPS
from gen_08_zones import zones as real_zones
from gen_09_qra_cap import QRAS
from gen_10_joueurs import SANCTUARIES
from gen_16_dessins import FRONT_CHILI
from lib import BLUE_SLOTS, BULLSEYE, RED_SLOTS, ROOT, TANKERS, Batch, xy

_t = (ROOT / "tools/airfield_channels.json").read_text(encoding="utf-8")
CH = {a["name"]: a for a in json.loads(_t[_t.index("{"):])["candidates"]}

ZONE_COUNT = len(real_zones())
FRONT_NM = round(sum(math.hypot(FRONT_CHILI[i][0] - FRONT_CHILI[i + 1][0], FRONT_CHILI[i][1] - FRONT_CHILI[i + 1][1])
                     for i in range(len(FRONT_CHILI) - 1)) / 1852)


def base(n):
    a = CH[n]
    f = a["freqs"]
    tac = f", TACAN {a['tacan']}" if a.get("tacan") else ""
    return f"{n} (U{f['uhf']:.2f} / V{f['vhf']:.2f}{tac})"


def carriers():
    out = []
    for c in CARRIERS:
        s = f"{c['name'].split(' ', 1)[1]} U{c['tower_mhz']:.1f}, TACAN {c['tacan_channel']}X, ICLS {c['icls_channel']}"
        if c.get("link4_mhz"):
            s += f", Link 4 {c['link4_mhz']:.1f}"
        out.append(s)
    return " ; ".join(out)


def tankers():
    return ", ".join(f"{n} ({k}) {tac} U{f:.1f} FL{fl}" for n, (ab, fl, tac, f, k) in TANKERS.items())


def qras(side):
    return ", ".join(f"{q['name'].replace('QRA ', '')} ({q['radius'] / 1852:.0f} nm)" for q in QRAS
                     if q["side"]["coalition"] == side)


def farps():
    return ", ".join(f"{n} (V{f:.1f})" for n, p, f, cs, side in FARPS)


SITUATION = f"""VEAF Open Training — Falklands (moderne, octobre 2026).
Une force hostile tient la côte atlantique de la Patagonie et de la Terre de Feu argentines, ainsi que Port Stanley aux Falkland. Le Royaume-Uni (îles) et le Chili, appuyés par les États-Unis et deux groupes aéronavals (Stennis, Roosevelt), la prennent en tenaille. Deux fronts : la frontière chilo-argentine, de Puerto Natales à Puerto Williams (environ {FRONT_NM} nm, tracé approximatif), et le cordon de crêtes à l'ouest de Port Stanley. Bullseye commun : le cap Vierges, à l'entrée atlantique du détroit de Magellan.

BASES BLEUES (slots dynamiques) : {", ".join(base(n) for n in BLUE_SLOTS)}. {farps()}.
PORTE-AVIONS : {carriers()}.
SOUTIEN : AWACS Overlord 1 U282.0 (îles) et Magic 1 U283.0 (Chili). Ravitailleurs : {tankers()} ; S-3B du Stennis 56Y U296.0, du Roosevelt 57Y U297.0. Tous escortés. Drones laser : Reaper 1 (code 1511, FM 35.55) sur le champ de tir d'attaque, Reaper 2 (1512, FM 35.6) sur le front de Rio Turbio.

ENTRAÎNEMENT (menu F10 VEAF, zones) : H Port Howard (hélicoptères), A Mount Adam (attaque), S Port Stephens (SEAD), trois niveaux chacun, sur la Falkland occidentale.
TOURISME : trois circuits hors combat, avec balises FM en morse et un guide qui raconte chaque site survolé bas : Torres del Paine (FARP Torres del Paine), le cap Horn (Puerto Williams) et les Falkland occidentales (FARP Port Howard).
COMBAT : {ZONE_COUNT} zones (front, SEAD, convois, frappes, bases aériennes, antinavire), chacune avec son briefing dans le menu. Missions à la demande : CAP rouges et bleues, raid rouge sur Mount Pleasant, interception d'un transport VIP.
QRA rouges : {qras('red')} ; QRA bleues : {qras('blue')}. Décollage 90 s après l'entrée du premier intrus ; elles ignorent les hélicoptères. Couloirs sans QRA : la Falkland occidentale, la mer entre les deux théâtres, le nord de la Patagonie.
JOUEURS CONTRE JOUEURS : libre hors des sanctuaires. Sanctuaires bleus : les Falkland ({SANCTUARIES[0][3] // 1000} km) et le détroit de Magellan ({SANCTUARIES[1][3] // 1000} km) ; rouge : San Julian ({SANCTUARIES[2][3] // 1000} km). Un intrus y est détruit après 60 s ; un missile tiré sur un défenseur est détruit. Arène AirQuake en Atlantique sud, au sud des Falkland, slots en vol Fox 1 et Fox 3.

Plan radio, cartes et détail de chaque zone : voir les images du briefing et le README de la mission."""

BLUE_TASK = ("Reprendre la côte et les crêtes : s'entraîner sur les champs de tir H, A et S, puis frapper les zones de combat rouges. "
             "Mount Pleasant est la base mère ; Goose Green, Gull Point et San Carlos tiennent les îles, Punta Arenas, Porvenir, "
             "Puerto Natales, Puerto Williams et Almirante Schroeders le Chili ; le Stennis et le Roosevelt croisent dans "
             "l'Atlantique sud.")
RED_TASK = (f"Tenir la Patagonie et Port Stanley. Bases rouges avec slots : {', '.join(base(n) for n in RED_SLOTS)}. "
            "AWACS Wizard 1 U284.0, ravitailleur Shell 1 (IL-78) U294.0 FL200. Arène : AWACS Focus 1 U286.0. "
            "Les sanctuaires bleus des Falkland et du détroit de Magellan détruisent tout appareil rouge qui y entre.")

if __name__ == "__main__":
    b = Batch()
    b.act("set_mission_date", date="2026-10-15", start_time="09:00")
    b.act("set_weather", metar="EGYP 151200Z 27015KT 9999 SCT025 06/02 Q1010")
    for side in ("blue", "red"):
        b.act("set_bullseye", coalition=side, position=xy(BULLSEYE))
    b.act("set_briefing", sortie="VEAF Open Training — Falklands", situation=SITUATION, blue_task=BLUE_TASK,
          red_task=RED_TASK)
    b.save(f"15-identite{('-' + sys.argv[1]) if len(sys.argv) > 1 else ''}.json")
    print(SITUATION)
