"""Outils communs aux générateurs de lots (tools/gen_*.py).

Un générateur écrit un fichier de lot dans tools/batches/ ; `python tools/mcp.py batch <lot>` l'exécute
sur le catalogue d'actions de veaf-mission-mcp (code VMCT de develop). Un lot ne s'exécute qu'une fois.

Scénario (moderne, 2026) : le Royaume-Uni (îles Falkland) et le Chili (Patagonie et Terre de Feu occidentales)
sont bleus, avec deux groupes aéronavals ; une force hostile (pays Russie, que CTLD veut dans le camp rouge)
tient la côte atlantique de la Patagonie et de la Terre de Feu argentines, et Port Stanley. Deux fronts : la
frontière chilo-argentine, de Puerto Natales à Puerto Williams, et le cordon de Port Stanley, à l'est des îles.

Terre / mer : la grille d'altitude Falklands balayée dans DCS (`veaf-tools dcs terrain-sweep Falklands`) ;
tant qu'elle manque, `ground()` refuse et aucun placement au sol ne se génère.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ROOT  # noqa: E402  (met aussi le code VMCT sur sys.path)
from veaf_libs.coordinates import latlon_to_xy, xy_to_latlon  # noqa: E402
from veaf_libs.terrain_elevation import grid_for_theatre  # noqa: E402

M = ROOT.as_posix()
THEATRE = "Falklands"

BLUE = dict(coalition="blue", country_id=2, country_name="USA")
BLUE_UK = dict(coalition="blue", country_id=4, country_name="UK")
BLUE_CL = dict(coalition="blue", country_id=63, country_name="Chile")
RED = dict(coalition="red", country_id=0, country_name="Russia")

# Aérodromes (list_airfields, Falklands : points de référence du terrain)
AIRFIELDS = {
    "Almirante Schroeders": (-209214, -741523), "Comandante Luis Piedrabuena": (208541, -707861),
    "Cullen": (-105290, -618847), "El Calafate": (136357, -922479), "Franco Bianco": (-99216, -683357),
    "Gobernador Gregores": (328115, -817027), "Goose Green": (72565, 11162), "Gull Point": (32794, 20420),
    "Hipico Flying Club": (329967, -823641), "Mount Pleasant": (73318, 47169), "O'Higgins": (328843, -1000896),
    "Pampa Guanaco": (-238408, -623775), "Port Stanley": (89025, 93868), "Porvenir": (-168264, -738641),
    "Puerto Natales": (-24059, -923009), "Puerto Santa Cruz": (210341, -680892),
    "Puerto Williams": (-323519, -531926), "Punta Arenas": (-147785, -779609), "Rio Chico": (19604, -699092),
    "Rio Gallegos": (25718, -703408), "Rio Grande": (-197145, -559488), "Rio Turbio": (-12262, -903420),
    "San Carlos FOB": (107939, 8484), "San Julian": (297478, -636918), "Tolhuin": (-271433, -510005),
    "Ushuaia": (-320587, -576145), "Ushuaia Helo Port": (-318410, -577047),
}
# Bleu : Royaume-Uni (îles) et Chili. Slots : 4 aux îles, 5 au Chili.
UK_SLOTS = ["Mount Pleasant", "Goose Green", "Gull Point", "San Carlos FOB"]
CHILE_SLOTS = ["Punta Arenas", "Porvenir", "Puerto Natales", "Puerto Williams", "Almirante Schroeders"]
BLUE_SLOTS = UK_SLOTS + CHILE_SLOTS
UK_NO_SLOTS = []
CHILE_NO_SLOTS = ["Franco Bianco", "Pampa Guanaco", "O'Higgins"]
# Rouge : Patagonie et Terre de Feu argentines, plus Port Stanley (enclave, sans slots)
RED_SLOTS = ["Rio Gallegos", "Rio Grande", "San Julian"]
RED_NO_SLOTS = ["Port Stanley", "Rio Chico", "Rio Turbio", "El Calafate", "Comandante Luis Piedrabuena",
                "Puerto Santa Cruz", "Gobernador Gregores", "Hipico Flying Club", "Cullen", "Tolhuin", "Ushuaia",
                "Ushuaia Helo Port"]
NEUTRAL = []

_GEO = json.loads((ROOT / "tools/places.json").read_text(encoding="utf-8"))
PLACES = {k.split(",")[0]: (v["x"], v["y"]) for k, v in _GEO.items()}
# Géocodage tombé sur un homonyme ou introuvable : coordonnées géographiques réelles, converties
for _n, (_la, _lo) in {
    "San Julian": (-49.3128, -67.7208), "Porvenir": (-53.2967, -70.3714), "Rio Grande": (-53.7877, -67.7095),
    "Rio Gallegos": (-51.6226, -69.2181),
}.items():
    PLACES[_n] = tuple(round(c) for c in latlon_to_xy(THEATRE, _la, _lo))

# Bullseye commun : le cap Vierges, à l'entrée atlantique du détroit de Magellan, sur la frontière chilo-argentine —
# un repère que les pilotes nomment, au centre du front du continent, sur aucune zone
BULLSEYE = PLACES["Cabo Virgenes"]


def ll(lat, lon):
    """Position DCS (x, y) d'un point géographique."""
    return tuple(round(c) for c in latlon_to_xy(THEATRE, lat, lon))


def nm(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1852


def km(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1000


def off(p, brg, m):
    """Point à `m` mètres de `p`, au relèvement `brg` (degrés vrais, x = nord, y = est)."""
    r = math.radians(brg)
    return (p[0] + m * math.cos(r), p[1] + m * math.sin(r))


def bearing(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def compass(a, b):
    """Rose des vents (« nord-ouest ») dans laquelle se trouve b vu de a."""
    names = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ouest", "ouest", "nord-ouest"]
    return names[int(((bearing(a, b) + 22.5) % 360) // 45)]


def bullseye(p):
    """« 123°/45 nm » depuis le bullseye : cap = atan2(Δy, Δx)."""
    return f"{bearing(BULLSEYE, p):03.0f}°/{nm(BULLSEYE, p):.0f} nm"


def xy(p):
    return {"x": round(p[0]), "y": round(p[1])}


_GRID = None


def ground(x, y):
    global _GRID
    if _GRID is None:
        _GRID = grid_for_theatre(THEATRE)
        if _GRID is None:
            raise SystemExit("pas de grille d'altitude Falklands (veaf-tools dcs terrain-sweep Falklands)")
    return _GRID.elevation_at(x, y)


def _ring(p, r, n=12):
    return [p] + [(p[0] + r * math.cos(2 * math.pi * i / n), p[1] + r * math.sin(2 * math.pi * i / n))
                  for i in range(n)]


def is_land(p, margin=300):
    """Terre ferme : le point et un cercle de `margin` m autour sont au-dessus de 0 m (la mer vaut 0)."""
    return all((ground(*q) or 0) > 0 for q in _ring(p, margin))


def is_sea(p, margin=1000):
    return all((ground(*q) or 0) <= 0 for q in _ring(p, margin, 16))


def land(p, what, margin=300):
    if not is_land(p, margin):
        raise SystemExit(f"PAS SUR LA TERRE FERME (marge {margin} m) : {what} {p}")
    return p


def sea(p, what, margin=1500):
    if not is_sea(p, margin):
        raise SystemExit(f"PAS EN PLEINE MER (marge {margin} m) : {what} {p}")
    return p


def nearest_land(x, y, margin=300, step=100, max_r=6000):
    """Le point à terre le plus proche de (x, y), à `margin` m au moins de l'eau (anneaux croissants)."""
    if is_land((x, y), margin):
        return (x, y)
    r = step
    while r <= max_r:
        n = max(8, int(2 * math.pi * r / step))
        for i in range(n):
            a = 2 * math.pi * i / n
            p = (x + r * math.cos(a), y + r * math.sin(a))
            if is_land(p, margin):
                return (round(p[0]), round(p[1]))
        r += step
    return None


def relief(p, r=500, n=16):
    """Écart d'altitude (m) entre le point le plus haut et le plus bas d'un cercle de rayon r autour de p (centre compris)."""
    e = [ground(p[0] + r * math.cos(2 * math.pi * i / n), p[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    e.append(ground(*p))
    return max(e) - min(e)


def flat_spot(center, search=6000, r=500, step=250, margin=400, what=""):
    """Le point à terre le plus proche de `center` dont le relief sur r mètres est le plus faible (parmi ceux à
    moins de 12 m du minimum trouvé), balayé sur une grille de `step` m dans un rayon `search`."""
    cands = []
    k = int(search // step)
    for i in range(-k, k + 1):
        for j in range(-k, k + 1):
            p = (center[0] + i * step, center[1] + j * step)
            d = math.hypot(i, j) * step
            if d > search or not is_land(p, margin):
                continue
            cands.append((relief(p, r), d, p))
    if not cands:
        raise SystemExit(f"pas de terrain plat près de {what} {center}")
    best = min(c[0] for c in cands)
    ok = [c for c in cands if c[0] <= best + 12]
    return min(ok, key=lambda c: c[1])[2]


def spot(center, brg, dist, what, margin=150):
    """Point à `dist` m de `center` au relèvement `brg`, ramené sur la terre ferme la plus proche."""
    p = off(center, brg, dist)
    q = nearest_land(p[0], p[1], margin=margin)
    if q is None:
        raise SystemExit(f"pas de terre près de {what} {p}")
    return q


class Batch:
    def __init__(self):
        self.items = []

    def act(self, action, **params):
        self.items.append({"name": action, "params": {"mission_path": M, **params}})

    def save(self, name):
        path = ROOT / "tools/batches" / name
        if path.exists():
            raise SystemExit(f"{path.name} existe déjà : un lot ne se régénère pas après exécution (doublons)")
        path.write_text(json.dumps(self.items, indent=1, ensure_ascii=False), encoding="utf-8")
        print(len(self.items), "actions ->", path.relative_to(ROOT))


def cmd_unit(alias_cmd, carrier_type, tag, extra=""):
    """Faux porteur de zone : `#command="<alias ...>"` + balises de tirage + suffixe unique."""
    name = f'#command="{alias_cmd}"'
    if extra:
        name += " " + extra
    return {"type": carrier_type, "name": f"{name} #{tag}"}


def interp_unit(alias_cmd, carrier_type, tag):
    """Porteur permanent : `#veafInterpreter["<alias ...>"]` + suffixe unique."""
    return {"type": carrier_type, "name": f'#veafInterpreter["{alias_cmd}"] #{tag}'}


def seg_nm(p, a, b):
    """Distance (nm) du point p au segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy) / 1852


def ddm(p):
    """« N30°11.051' E032°45.729' » (degrés, minutes décimales : ce que saisissent la plupart des avions)."""
    lat, lon = xy_to_latlon(THEATRE, *p)

    def one(v, pos, neg, w):
        h = pos if v >= 0 else neg
        v = abs(v)
        d = int(v)
        return f"{h}{d:0{w}d}°{(v - d) * 60:06.3f}'"
    return f"{one(lat, 'N', 'S', 2)} {one(lon, 'E', 'W', 3)}"


def position_text(p):
    return f"Position : bullseye {bullseye(p)} ({ddm(p)})."


# Ravitailleurs bleus : extrémités de l'hippodrome, FL, TACAN, MHz, type de ravitaillement (gen_05_soutien.py)
TANKERS = {
    # îles : au sud des Falkland, au large de Gull Point
    "Texaco 1": (((-25000, -40000), (-25000, 25000)), 220, "50Y", 290.0, "perche"),
    "Arco 1": (((-45000, -45000), (-45000, 20000)), 180, "51Y", 291.0, "panier"),
    # Chili : à l'ouest de Punta Arenas et de Puerto Natales
    "Texaco 2": (((-100000, -880000), (-100000, -960000)), 240, "52Y", 292.0, "perche"),
    "Arco 2": (((-60000, -905000), (-60000, -985000)), 200, "53Y", 293.0, "panier"),
}


def tankers_text(p):
    """« Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 12 nm ; Texaco 1 (...) à 30 nm. » — le plus proche de
    chaque type, mesuré jusqu'à sa piste."""
    out = []
    for kind in ("panier", "perche"):
        n, (ab, fl, tacan, f, k) = min(((n, v) for n, v in TANKERS.items() if v[4] == kind),
                                       key=lambda kv: seg_nm(p, *kv[1][0]))
        out.append(f"{n} ({kind}, TACAN {tacan}, {f:.1f}) à {seg_nm(p, *ab):.0f} nm")
    return "Ravitailleurs : " + " ; ".join(out) + "."
