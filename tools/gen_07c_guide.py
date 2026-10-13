"""Écrit les guides touristiques dans src/scripts/mission-script.lua (bloc entre deux marqueurs, réécrit à chaque
passage : ce script se rejoue sans doublon).

Toutes les 2 s, le guide regarde les appareils des joueurs des deux camps ; quand l'un passe à moins de 1 500 ft
sol et à moins du rayon d'un site, son groupe reçoit le texte du site (une fois par appareil et par site, puis à
nouveau après 10 min). Positions : tools/places.json (geocode OSM) et coordonnées géographiques (ll).
Textes : connaissances générales, chiffres arrondis et « environ » — à relire (sources à citer : articles
Wikipédia en français de chaque site).
Les rayons restent sous la moitié de l'écart entre deux sites voisins : un seul message à la fois.
Chaque site a un indicatif en morse (`code`) et une fréquence FM (`mhz`) pour sa balise (gen_07b_tourisme.py) ;
l'excursion du Perito Moreno n'a pas de balise.
"""
from lib import M, PLACES, ll

P = PLACES

SITES = [
    # ── T1 : Torres del Paine (Chili) ──
    dict(key="torres", zone="Paine", code="TOR", mhz=30.0, name="Las Torres", pos=ll(-50.942, -72.963), r=1500,
         text="Las Torres, les tours du Paine : trois aiguilles de granit qui dominent la steppe de la région de "
              "Magallanes, entre 2 500 et 2 800 m environ selon les sources. Elles sont au cœur du parc national "
              "Torres del Paine, créé en 1959 et classé réserve de biosphère par l'UNESCO en 1978."),
    dict(key="cuernos", zone="Paine", code=None, mhz=None, name="Les Cuernos", pos=ll(-51.000, -73.010), r=1500,
         text="Les Cuernos del Paine, les cornes : un sommet de granit clair coiffé de roche sédimentaire sombre, "
              "à environ 2 600 m, façonné par l'érosion et les glaciers."),
    dict(key="paine_grande", zone="Paine", code="PAI", mhz=31.0, name="Cerro Paine Grande", pos=P["Cerro Paine Grande"],
         r=2000, text="Cerro Paine Grande, le point culminant du massif : environ 2 884 m."),
    dict(key="grey", zone="Paine", code="GRE", mhz=32.0, name="Glaciar Grey", pos=P["Grey Glacier"], r=3000,
         text="Glaciar Grey : une langue de la grande calotte glaciaire de Patagonie, qui se jette dans le lac Grey "
              "par un front d'environ 6 km de large et une trentaine de mètres de haut. Des morceaux de glace "
              "détachés flottent sur le lac."),
    dict(key="perito_moreno", zone="Paine", code=None, mhz=None, name="Glaciar Perito Moreno",
         pos=P["Perito Moreno Glacier"], r=3000,
         text="Glaciar Perito Moreno, côté argentin, dans le parc national Los Glaciares : environ 30 km de long, un "
              "front d'environ 5 km et 60 m au-dessus du lac Argentino, longtemps resté stable alors que presque "
              "tous les glaciers de la région reculent. Vous êtes en territoire rouge : aucune défense permanente "
              "n'y est posée."),
    # ── T2 : le bout du monde (Chili) ──
    dict(key="beagle", zone="CapHorn", code="BEA", mhz=33.0, name="Canal Beagle", pos=ll(-54.97, -67.62), r=3000,
         text="Le canal Beagle, environ 240 km entre l'Atlantique et le Pacifique, au pied de l'île Navarino. Il est "
              "nommé d'après le HMS Beagle, dont les voyages de 1826 à 1836 l'ont fait connaître ; Charles Darwin "
              "était à bord du second."),
    dict(key="wollaston", zone="CapHorn", code="WOL", mhz=34.0, name="Îles Wollaston", pos=ll(-55.72, -67.37), r=5000,
         text="L'archipel Wollaston, inhabité, au sud de l'île Navarino : les dernières terres avant le cap Horn."),
    dict(key="horn", zone="CapHorn", code="HRN", mhz=35.0, name="Cap Horn", pos=P["Cabo de Hornos"], r=3000,
         text="Le cap Horn, falaise d'environ 425 m à l'extrémité sud de l'île Hornos : le dernier cap des Amériques. "
              "Les navigateurs néerlandais Schouten et Le Maire l'ont franchi les premiers en 1616 et l'ont nommé "
              "d'après la ville de Hoorn."),
    # ── T3 : Falkland occidentales (Royaume-Uni) ──
    dict(key="pebble", zone="Egmont", code="PEB", mhz=36.0, name="Pebble Island", pos=P["Pebble Island"], r=4000,
         text="Pebble Island : environ 35 km de long, au nord de la Falkland occidentale. Pendant la guerre des "
              "Malouines, le 15 mai 1982, un détachement du SAS y a détruit onze avions argentins sur la piste, "
              "lors d'un raid de nuit."),
    dict(key="egmont", zone="Egmont", code="EGM", mhz=37.0, name="Port Egmont", pos=P["Port Egmont"], r=1500,
         text="Port Egmont, sur l'île Saunders : le premier établissement britannique des Falkland. Le capitaine "
              "John McBride y bâtit un fort en 1766 ; les Espagnols en chassèrent les Britanniques en 1770, qui y "
              "revinrent en 1771 avant de partir en 1774 en laissant une plaque."),
    dict(key="carcass", zone="Egmont", code="CAR", mhz=38.0, name="Carcass Island", pos=P["Carcass Island"], r=2500,
         text="Carcass Island, nommée d'après le HMS Carcass qui l'a visitée en 1766. Réputée pour ses oiseaux, elle "
              "accueille des manchots de Magellan et des caracaras."),
]

BEGIN = "-- >>> guides touristiques (écrit par tools/gen_07c_guide.py, ne pas éditer à la main)"
END = "-- <<< guides touristiques"


def lua_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def block():
    rows = []
    for s in SITES:
        x, y = s["pos"]
        rows.append(f"    {{ x = {x}, z = {y}, r = {s['r']}, text = {lua_str(s['text'])} }},")
    return "\n".join([
        BEGIN,
        "do",
        "  veafTourGuide = { seen = {} }",
        "  veafTourGuide.monuments = {",
        *rows,
        "  }",
        "  veafTourGuide.maxAgl = 457      -- 1 500 ft",
        "  veafTourGuide.repeatAfter = 600 -- s",
        "  function veafTourGuide.check()",
        "    local now = timer.getTime()",
        "    for _, side in pairs({ coalition.side.BLUE, coalition.side.RED }) do",
        "      for _, unit in pairs(coalition.getPlayers(side) or {}) do",
        "        if unit and unit:isExist() and unit:inAir() then",
        "          local p = unit:getPoint()",
        "          local agl = p.y - land.getHeight({ x = p.x, y = p.z })",
        "          if agl < veafTourGuide.maxAgl then",
        "            for i, m in ipairs(veafTourGuide.monuments) do",
        "              local dx, dz = p.x - m.x, p.z - m.z",
        "              if dx * dx + dz * dz < m.r * m.r then",
        "                local key = unit:getName() .. '#' .. i",
        "                local last = veafTourGuide.seen[key]",
        "                if not last or now - last > veafTourGuide.repeatAfter then",
        "                  veafTourGuide.seen[key] = now",
        "                  trigger.action.outTextForGroup(unit:getGroup():getID(), m.text, 25)",
        "                end",
        "              end",
        "            end",
        "          end",
        "        end",
        "      end",
        "    end",
        "    return now + 2",
        "  end",
        "  timer.scheduleFunction(function(_, t) local ok, nxt = pcall(veafTourGuide.check) "
        "if ok then return nxt end env.error('veafTourGuide: ' .. tostring(nxt)) return t + 10 end, nil, "
        "timer.getTime() + 10)",
        "end",
        END,
    ])


if __name__ == "__main__":
    path = f"{M}/src/scripts/mission-script.lua"
    t = open(path, encoding="utf-8").read()
    if BEGIN in t:
        t = t[:t.index(BEGIN)] + t[t.index(END) + len(END):].lstrip("\n")
    t = t.rstrip("\n") + "\n\n" + block() + "\n"
    open(path, "w", encoding="utf-8").write(t)
    print(len(SITES), "sites écrits dans", path)
