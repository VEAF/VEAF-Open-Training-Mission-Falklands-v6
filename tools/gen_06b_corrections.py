"""Lot 06b : le radar d'alerte de Puerto Santa Cruz (lot 06) était à 476 m du centre de la zone Z11 (port de Puerto
Santa Cruz) : un groupe dans le cercle d'une zone est capturé par la géométrie. Il est repris à 9 km au
sud-ouest de l'aérodrome (relevé 200°), hors du cercle."""
from lib import AIRFIELDS, RED, Batch, interp_unit, land, spot, xy

if __name__ == "__main__":
    b = Batch()
    b.act("remove_group", group_name="EWR Santa Cruz")
    p = spot(AIRFIELDS["Puerto Santa Cruz"], 200, 9000, "EWR Santa Cruz", margin=300)
    land(p, "EWR Santa Cruz", margin=300)
    b.act("add_group", **RED, category="vehicle", name="EWR Santa Cruz", position=xy(p), keep_position=True,
          units=[interp_unit("-ewr, hdg 0", "55G6 EWR", "EWR-Santa-Cruz")])
    b.save("06b-corrections.json")
