"""Lot 04 : camp de chaque aérodrome et slots dynamiques.

Bleu avec slots (9) : aux Falkland Mount Pleasant (base mère), Goose Green, Gull Point et San Carlos FOB ; au Chili
Punta Arenas, Porvenir, Puerto Natales, Puerto Williams et Almirante Schroeders.
Bleu sans slots : les autres terrains du Chili austral (Franco Bianco, Pampa Guanaco, O'Higgins).
Rouge avec slots : Rio Gallegos (côte), Rio Grande (Terre de Feu), San Julian (nord) ; tous les autres terrains
argentins rouges sans slots, ainsi que Port Stanley (enclave).
Les FARP viennent avec le lot 05b, une fois la grille d'altitude disponible (contrôle terre ferme).
"""
from lib import BLUE_SLOTS, CHILE_NO_SLOTS, NEUTRAL, RED_NO_SLOTS, RED_SLOTS, UK_NO_SLOTS, Batch

if __name__ == "__main__":
    b = Batch()
    for n in BLUE_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue")
    for n in UK_NO_SLOTS + CHILE_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="blue", dynamic_spawn=False)
    for n in RED_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red")
    for n in RED_NO_SLOTS:
        b.act("set_airbase_coalition", name=n, coalition="red", dynamic_spawn=False)
    for n in NEUTRAL:
        b.act("set_airbase_coalition", name=n, coalition="neutral", dynamic_spawn=False)
    b.save("04-bases.json")
