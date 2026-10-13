"""Lot 16 : dessins F10 (add_map_drawing, pour qu'ils survivent au build).

Chaque zone a son contour à son rayon réel ET son étiquette ; lignes de front, sanctuaires, QRA, hippodromes de
soutien, arène, circuit touristique. Étiquettes sur fond clair opaque (sans fond, l'action met du noir à moitié
transparent et le texte sombre devient illisible, Caucase 29/09/2026). Pas de trait en tirets : add_map_drawing
n'écrit que du plein (VMCT FIX-OPEN-TRAINING-CAUCASUS-FINDINGS ticket 03).
Couches : Common pour ce que les deux camps partagent (front, zones, sanctuaires, QRA, arène), Blue / Red pour
les hippodromes de soutien de chaque camp. Adapté de l'OT Golfe Persique.
"""
import gen_07_entrainement as e
import gen_08_zones as z
from gen_05_soutien import SUPPORT
from gen_07b_tourisme import BEACONS
from gen_07c_guide import SITES
from gen_09_qra_cap import QRAS
from gen_10_joueurs import ARENA, SANCTUARIES
from lib import AIRFIELDS, PLACES, Batch, ll, xy

LABEL_BG = "0xffffffe0"
RED, BLUE, ORANGE, GREEN, MAGENTA, BROWN = "0xcc0000ff", "0x0040ccff", "0xe07000ff", "0x008000ff", "0xb000b0ff", "0x8b5a00ff"

# Fronts (approximatifs) : la frontière chilo-argentine, de Puerto Natales à Puerto Williams — relevée sur le tracé
# OpenStreetMap des zooms du briefing (le 52e parallèle sud entre 71°54' et 70° O, puis le cap Vierges et le méridien
# 68°36' O de Terre de Feu jusqu'au canal Beagle) ; l'arc des crêtes à l'ouest de Port Stanley
FRONT_CHILI = [ll(-51.529, -72.439), ll(-51.698, -72.381), ll(-51.83, -72.186), ll(-51.902, -72.05),
               ll(-51.998, -71.895), ll(-52.0, -70.0), ll(-52.154, -69.183), ll(-52.33, -68.36), ll(-52.65, -68.61),
               ll(-54.00, -68.61), ll(-54.88, -68.61)]
FRONT_ILES = [PLACES["Mount Kent"], PLACES["Two Sisters"], PLACES["Mount Longdon"], PLACES["Wireless Ridge"],
              PLACES["Mount Tumbledown"], PLACES["Mount William"], PLACES["Sapper Hill"]]


def above(c, r, gap=800):
    return (c[0] + r + gap, c[1])


b = Batch()


def circle(layer, name, c, r, color, fill="0x00000000", thickness=3):
    b.act("add_map_drawing", layer=layer, shape="circle", name=name, position=xy(c), radius=r, color=color,
          fill_color=fill, thickness=thickness)


def label(layer, name, p, text, color, size=12):
    b.act("add_map_drawing", layer=layer, shape="textbox", name=name, position=xy(p), text=text, color=color,
          fill_color=LABEL_BG, font_size=size)


def build():
    for n, pts, lp, text in [("Front du Chili", FRONT_CHILI, ll(-53.2, -68.9),
                              "FRONT DU CHILI (approximatif) : de Puerto Natales à Puerto Williams"),
                             ("Front des îles", FRONT_ILES, (110000, 80000),
                              "FRONT DES ÎLES (approximatif) : les crêtes à l'ouest de Stanley")]:
        b.act("add_map_drawing", layer="Common", shape="line", name=n, points=[xy(q) for q in pts], color=RED,
              thickness=6)
        label("Common", f"{n} étiquette", lp, text, RED, 14)

    # ── zones d'entraînement : un cercle et une étiquette par famille (niveaux imbriqués sur le même cercle) ──
    for zone, c, r, fname, *_ in e.zones():
        if not zone.endswith("_Easy"):
            continue
        fam = fname.split()[0][0]
        text = {"H": "H1-H3 Entraînement hélicoptères — Port Howard", "A": "A1-A3 Entraînement attaque — Mount Adam",
                "S": "S1-S3 Entraînement SEAD — Port Stephens"}[fam]
        circle("Common", f"Zone {zone[:-5]}", c, r, ORANGE, "0xe0700018")
        label("Common", f"Zone {zone[:-5]} étiquette", above(c, r), text, ORANGE)

    # ── tourisme : les zones, les balises et les circuits ──
    start = {"combatZone_Paine": e.FARP_TORRES, "combatZone_CapHorn": AIRFIELDS["Puerto Williams"],
             "combatZone_PortEgmont": e.FARP_PH}
    zone_key = {"combatZone_Paine": "Paine", "combatZone_CapHorn": "CapHorn", "combatZone_PortEgmont": "Egmont"}
    for zone, c, r, fname, menu, side, groups in e.tourism():
        circle("Common", f"Zone {zone}", c, r, BROWN, "0x8b5a0018")
        label("Common", f"Zone {zone} étiquette", above(c, r), fname, BROWN)
        mine = [bc for bc in BEACONS if bc[3] in {s["key"] for s in SITES if s["zone"] == zone_key[zone]}]
        pts = [xy(start[zone]), xy(c)] + [xy(next(s["pos"] for s in SITES if s["key"] == bc[3])) for bc in mine]
        b.act("add_map_drawing", layer="Blue", shape="line", name=f"Circuit {zone}", points=pts, color=BROWN,
              thickness=2)
        for n, code, mhz, key, side2, sub in mine:
            p = next(s["pos"] for s in SITES if s["key"] == key)
            label("Blue", f"{n} étiquette", (p[0], p[1] + 2500), f"{code} FM {mhz:.1f}", BROWN, 10)

    # ── vraies zones de combat ──
    for zone, c, r, fname, *_ in z.zones():
        circle("Common", f"Zone {zone}", c, r, RED, "0xcc000018")
        label("Common", f"Zone {zone} étiquette", above(c, r), fname, RED, 11)

    # ── QRA ──
    for q in QRAS:
        col = MAGENTA if q["side"]["coalition"] == "red" else BLUE
        circle("Common", f"QRA {q['name']}", q["center"], q["radius"], col, thickness=2)
        label("Common", f"QRA {q['name']} étiquette", (q["center"][0] + q["radius"] - 6000, q["center"][1]),
              f"{q['name']} ({round(q['radius'] / 1852)} nm)", col, 11)

    # ── sanctuaires ──
    for name, tz, c, r, side in SANCTUARIES:
        circle("Common", name, c, r, GREEN, "0x00800018", thickness=2)
        label("Common", f"{name} étiquette", (c[0] - r - 1500, c[1]), name, GREEN, 10)

    # ── arène ──
    circle("Common", "Arène cercle", ARENA[0], ARENA[1], GREEN, thickness=3)
    label("Common", "Arène étiquette", above(ARENA[0], ARENA[1], 3000), "ARÈNE joueurs contre joueurs (slots en vol)",
          GREEN, 14)

    # ── hippodromes de soutien (hors arène) ──
    for n, typ, side, a, bb, fl, kt, f, task, beacon, esc in SUPPORT:
        if n in ("Darkstar 1", "Focus 1"):
            continue
        layer = "Blue" if side["coalition"] == "blue" else "Red"
        col = BLUE if layer == "Blue" else RED
        what = f"TACAN {beacon[0]}Y" if beacon else ("AWACS" if task == "AWACS" else typ)
        b.act("add_map_drawing", layer=layer, shape="line", name=f"Piste {n}", points=[xy(a), xy(bb)], color=col,
              thickness=4)
        label(layer, f"Piste {n} étiquette", ((a[0] + bb[0]) / 2, (a[1] + bb[1]) / 2 + 6000),
              f"{n} — {what} — U{f:.1f} — FL{fl}", col, 10)


if __name__ == "__main__":
    build()
    b.save("16-dessins.json")
