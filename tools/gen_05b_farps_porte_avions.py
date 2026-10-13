"""Lot 05b : les quatre FARP, les deux groupes aéronavals, et les slots sur les ponts.

Après le lot 05 (ravitailleurs AVANT porte-avions, sinon les S-3B prennent Texaco11 / Arco11).
FARP (fréquences VHF AM hors des tours, plan radio gen_12_presets.py) :
  - Port Howard : sur la Falkland occidentale, à l'est de la zone hélicoptères H — départ des hélicoptères et du
    tourisme des îles ;
  - Teal Inlet : au nord de Mount Pleasant, dans le sanctuaire bleu, pour les hélicoptères du front de Stanley ;
  - Torres del Paine : sur la steppe au sud-est du parc, pour le tourisme de Patagonie ;
  - Sombrero : en Terre de Feu chilienne, près de Cerro Sombrero, pour les hélicoptères du front de Terre de Feu.
Porte-avions : le Stennis au sud des Falkland, le Roosevelt au large de la Terre de Feu argentine. Toujours Stennis
et Roosevelt (décision du 02/10/2026).
"""
from lib import BLUE, BLUE_CL, BLUE_UK, PLACES, Batch, land, ll, off, sea, xy

FARPS = [
    ("FARP Port Howard", (88000, -32250), 127.5, 1, BLUE_UK),
    ("FARP Teal Inlet", (102500, 43250), 128.0, 2, BLUE_UK),
    ("FARP Torres del Paine", (39927, -960794), 129.5, 3, BLUE_CL),   # 128.5 = tour de Franco Bianco
    ("FARP Sombrero", (-105831, -679874), 129.0, 4, BLUE_CL),
]

CARRIERS = [
    dict(name="CSG-74 Stennis", carrier_type="Stennis", position=(-40000, -140000), heading_deg=270, speed_kt=10,
         tower_mhz=305.0, tacan_channel=74, tacan_callsign="STN", icls_channel=11, link4_mhz=336.0,
         tanker_tacan_channel=56, tanker_tacan_callsign="S74", tanker_frequency_mhz=296.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
    dict(name="CSG-71 Roosevelt", carrier_type="CVN_71", position=(-160000, -330000), heading_deg=0, speed_kt=10,
         tower_mhz=306.0, tacan_channel=71, tacan_callsign="RSV", icls_channel=12, link4_mhz=337.0,
         tanker_tacan_channel=57, tanker_tacan_callsign="S71", tanker_frequency_mhz=297.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
]

DECKS = [
    # porte-avions, nom du groupe, type, nombre, départ
    ("CSG-74 Stennis", "Stennis F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-74 Stennis", "Stennis F/A-18C #2", "FA-18C_hornet", 2, "deck-hot"),
    ("CSG-74 Stennis", "Stennis F-14B #1", "F-14B", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #1", "F-14B", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #2", "F-14B", 2, "deck-hot"),
]

if __name__ == "__main__":
    b = Batch()
    for name, p, f, cs, side in FARPS:
        land(p, name, margin=300)
        b.act("add_farp", name=name, position=xy(p), **side, frequency_mhz=f, callsign_id=cs)
        print(f"{name:22} {round(p[0]):>8} {round(p[1]):>8}")
    for c in CARRIERS:
        c = dict(c)
        p = c.pop("position")
        sea(p, c["name"], margin=8000)
        b.act("add_carrier_group", **BLUE, position=xy(p), **c)
    for carrier, name, typ, n, start in DECKS:
        b.act("add_air_group", **BLUE, name=name, unit_type=typ, count=n, start=start, carrier=carrier,
              skill="Client", task="CAP")
    b.save("05b-farps-porte-avions.json")
