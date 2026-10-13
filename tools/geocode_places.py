"""Géocode une fois les lieux réels dont la mission a besoin → tools/places.json (x/y DCS).

Relancer ajoute seulement les lieux absents. Chaque point est à relire : l'outil peut tomber sur un
homonyme (osm_type et nom affiché sont gardés pour ça).
"""
import json
import sys

from paths import ROOT  # noqa: F401  (met aussi le code VMCT sur sys.path)
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
PLACES = [
    # Îles Falkland, Est : cordon de Stanley (1982 : les crêtes)
    "Stanley, Falkland Islands", "Mount Longdon, Falkland Islands", "Wireless Ridge, Falkland Islands",
    "Mount Tumbledown, Falkland Islands", "Mount William, Falkland Islands", "Two Sisters, Falkland Islands",
    "Mount Harriet, Falkland Islands", "Sapper Hill, Falkland Islands", "Mount Kent, Falkland Islands",
    "Mount Challenger, Falkland Islands", "Goose Green, Falkland Islands", "Darwin, Falkland Islands",
    "Fitzroy, Falkland Islands", "Bluff Cove, Falkland Islands", "San Carlos, Falkland Islands",
    "Port San Carlos, Falkland Islands", "Mount Usborne, Falkland Islands", "Volunteer Point, Falkland Islands",
    "Cape Pembroke, Falkland Islands", "Port Louis, Falkland Islands", "Camilla Creek, Falkland Islands",
    "Teal Inlet, Falkland Islands", "Estancia, Falkland Islands", "Salvador, Falkland Islands",
    # Îles Falkland, Ouest et îles
    "Pebble Island, Falkland Islands", "Fox Bay, Falkland Islands", "Port Howard, Falkland Islands",
    "Hill Cove, Falkland Islands", "Port Stephens, Falkland Islands", "Weddell Island, Falkland Islands",
    "Sea Lion Island, Falkland Islands", "Carcass Island, Falkland Islands", "Saunders Island, Falkland Islands",
    "Mount Adam, Falkland Islands", "Chartres, Falkland Islands", "Dunnose Head, Falkland Islands",
    "Port Egmont, Falkland Islands", "Keppel Island, Falkland Islands",
    # Patagonie argentine
    "Rio Gallegos, Argentina", "Rio Turbio, Argentina", "El Calafate, Argentina",
    "Comandante Luis Piedrabuena, Argentina", "Puerto Santa Cruz, Argentina", "San Julian, Argentina",
    "Gobernador Gregores, Argentina", "Rio Grande, Tierra del Fuego, Argentina", "Tolhuin, Argentina",
    "Ushuaia, Argentina", "Cullen, Tierra del Fuego", "San Sebastian, Tierra del Fuego Argentina",
    "Cabo Virgenes, Argentina", "Lago Argentino, Argentina", "Perito Moreno Glacier", "Lago Viedma, Argentina",
    "El Chalten, Argentina", "Monte Fitz Roy", "Estancia La Anita, Argentina", "28 de Noviembre, Argentina",
    "Cerro Dorotea, Argentina", "Rio Grande Naval Air Station", "Puerto Almanza, Argentina",
    "Isla de los Estados", "Estrecho de Le Maire",
    # Chili austral
    "Punta Arenas, Chile", "Puerto Natales, Chile", "Porvenir, Chile", "Puerto Williams, Chile",
    "Torres del Paine", "Cerro Paine Grande", "Grey Glacier, Chile", "Lago Grey, Chile", "Villa O'Higgins",
    "Cabo de Hornos", "Isla Hornos", "Cerro Sombrero, Chile", "Estrecho de Magallanes", "Bahia Inutil, Chile",
    "Puerto Harris, Chile", "Pali Aike", "Cerro Castillo, Chile", "Cabo Froward", "Isla Navarino",
    "Canal Beagle", "Wollaston Islands",
]
out_path = ROOT / "tools" / "places.json"
places = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
cat = ActionCatalog()
register_default_actions(cat)
for q in PLACES:
    if q in places:
        continue
    try:
        r = cat.run_action("geocode", {"mission_path": str(ROOT), "query": q})
    except Exception as e:  # noqa: BLE001
        print("ERREUR", q, e)
        continue
    if not r.get("found"):
        print("INTROUVABLE", q)
        continue
    places[q] = {"x": round(r["xy"]["x"]), "y": round(r["xy"]["y"]), "osm": r.get("osm_type"), "name": r["display_name"][:90]}
    print(f"{q:28} {places[q]['x']:>8} {places[q]['y']:>8}  {places[q]['osm']:<14} {places[q]['name']}")
    out_path.write_text(json.dumps(places, indent=1, ensure_ascii=False), encoding="utf-8")
