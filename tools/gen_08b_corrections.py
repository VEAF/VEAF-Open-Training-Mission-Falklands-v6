"""Lot 08b : la zone Z14 (OCA de Port Stanley) passe de 1 500 à 800 m de rayon.

Les parkings de la QRA de Port Stanley (lot 09b, départ piste) sont à 1,1 km du centre de la zone : un groupe dans le
cercle d'une zone est capturé par la géométrie, la QRA aurait été détruite puis recréée avec la zone. Les statiques de
la zone sont à 400 m du centre au plus. Le cercle et l'étiquette F10 de la zone (lot 16) sont redessinés."""
import gen_08_zones as z
import gen_16_dessins as g
from lib import Batch, xy

KEY = "combatZone_PortStanley"

if __name__ == "__main__":
    zone = next(t for t in z.zones() if t[0] == KEY)
    c, r = zone[1], zone[2]
    g.b.items.clear()
    b = Batch()
    b.act("edit_zone", zone_name=KEY, radius=r)
    b.act("edit_map_drawing", layer="Common", name=f"Zone {KEY}", remove=True)
    b.act("edit_map_drawing", layer="Common", name=f"Zone {KEY} étiquette", remove=True)
    g.circle("Common", f"Zone {KEY}", c, r, g.RED, "0xcc000018")
    g.label("Common", f"Zone {KEY} étiquette", g.above(c, r), zone[3], g.RED, 11)
    b.items.extend(g.b.items)
    for it in b.items:
        it["params"].setdefault("mission_path", __import__("lib").M)
    b.save("08b-corrections.json")
