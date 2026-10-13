"""Lot 05c : Overlord 1 (et son escorte) déplacé au large du nord de la Falkland occidentale — sa première piste, à
l'ouest, passait à 30 km de la zone SEAD S (SA-11 : 50 km) — et Reaper 1 posé au-dessus du champ de tir d'attaque A
(il avait été placé avant le choix du terrain plat). Les groupes sont retirés puis recréés par gen_05_soutien.py."""
from gen_05_soutien import b as support
from lib import Batch

NAMES = {"Overlord 1", "Overlord 1 - Escort", "Reaper 1"}

if __name__ == "__main__":
    b = Batch()
    for n in ("Overlord 1 - Escort", "Overlord 1", "Reaper 1"):
        b.act("remove_group", group_name=n)
    for it in support.items:
        p = it["params"]
        if p.get("name") in NAMES or p.get("group_name") in NAMES:
            b.items.append(it)
    b.save("05c-corrections.json")
