"""Lot 07d : corrections des zones de tourisme du lot 07 (recouvrements trouvés par check_overlap.py).

Les zones d'une famille capturent par la géométrie tout groupe dans leur cercle : la balise EGM (2 138 m du centre de
Port Egmont) et le NASAMS de Puerto Williams (932 m du centre de la zone du cap Horn) y auraient été détruits puis
recréés. Les trois zones passent à 1 500 m de rayon, la zone du cap Horn à 6 km à l'est-nord-est de la base.
"""
from gen_07_entrainement import T2
from lib import Batch, spot, xy

if __name__ == "__main__":
    b = Batch()
    b.act("edit_zone", zone_name="combatZone_Paine", radius=1500)
    b.act("edit_zone", zone_name="combatZone_PortEgmont", radius=1500)
    p = spot(T2, 0, 0, "T2")
    b.act("edit_zone", zone_name="combatZone_CapHorn", position=xy(p), radius=1500)
    b.act("set_group_properties", group_name="combatZone_CapHorn-4x4", move_to=xy(spot(p, 60, 500, "4x4")))
    b.save("07d-corrections.json")
