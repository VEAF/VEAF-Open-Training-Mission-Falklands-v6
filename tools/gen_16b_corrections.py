"""Lot 16b : la ligne du front du Chili (lot 16) est redessinée sur la frontière relevée sur le tracé OpenStreetMap des
zooms (le 52e parallèle sud entre 71°54' et 70° O, le cap Vierges, le méridien 68°36' O de Terre de Feu) : le premier
tracé, à vol d'oiseau de Rio Turbio au cap Vierges, s'en écartait de 30 km. Seul le trait change ; son étiquette reste."""
from gen_16_dessins import BROWN, FRONT_CHILI, RED, b as drawing
from lib import Batch, xy

if __name__ == "__main__":
    b = Batch()
    b.act("edit_map_drawing", layer="Common", name="Front du Chili", remove=True)
    b.act("add_map_drawing", layer="Common", shape="line", name="Front du Chili", points=[xy(q) for q in FRONT_CHILI],
          color=RED, thickness=6)
    b.save("16b-corrections.json")
