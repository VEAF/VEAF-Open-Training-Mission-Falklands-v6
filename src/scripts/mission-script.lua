-- mission-script.lua
-- Mission-specific Lua code that cannot be generated from mission.yaml.
--
-- This file is loaded AFTER veaf-config.lua (which is generated automatically
-- from mission.yaml by the veaf-tools build command).
--
-- Put here:
--   - Custom shortcuts / aliases  (VeafAlias:new():...)
--   - Custom Lua helper functions
--   - Third-party script setup (CTLD, CSAR, …) that requires Lua code
--
-- Do NOT put here:
--   - Module initialization calls  → use mission.yaml (modules:)
--   - Mission identity             → use mission.yaml (mission:)
--   - QRA definitions              → use mission.yaml (modules.QRA)
--   - Combat/CAP missions          → use mission.yaml (combat_missions: / cap_missions:)
--   - Assets lists                 → use mission.yaml (modules.ASSETS.assets)

-- >>> guides touristiques (écrit par tools/gen_07c_guide.py, ne pas éditer à la main)
do
  veafTourGuide = { seen = {} }
  veafTourGuide.monuments = {
    { x = 49643, z = -970721, r = 1500, text = "Las Torres, les tours du Paine : trois aiguilles de granit qui dominent la steppe de la région de Magallanes, entre 2 500 et 2 800 m environ selon les sources. Elles sont au cœur du parc national Torres del Paine, créé en 1959 et classé réserve de biosphère par l'UNESCO en 1978." },
    { x = 42523, z = -972569, r = 1500, text = "Les Cuernos del Paine, les cornes : un sommet de granit clair coiffé de roche sédimentaire sombre, à environ 2 600 m, façonné par l'érosion et les glaciers." },
    { x = 41869, z = -978021, r = 2000, text = "Cerro Paine Grande, le point culminant du massif : environ 2 884 m." },
    { x = 51974, z = -1001713, r = 3000, text = "Glaciar Grey : une langue de la grande calotte glaciaire de Patagonie, qui se jette dans le lac Grey par un front d'environ 6 km de large et une trentaine de mètres de haut. Des morceaux de glace détachés flottent sur le lac." },
    { x = 85838, z = -998355, r = 3000, text = "Glaciar Perito Moreno, côté argentin, dans le parc national Los Glaciares : environ 30 km de long, un front d'environ 5 km et 60 m au-dessus du lac Argentino, longtemps resté stable alors que presque tous les glaciers de la région reculent. Vous êtes en territoire rouge : aucune défense permanente n'y est posée." },
    { x = -327773, z = -530868, r = 3000, text = "Le canal Beagle, environ 240 km entre l'Atlantique et le Pacifique, au pied de l'île Navarino. Il est nommé d'après le HMS Beagle, dont les voyages de 1826 à 1836 l'ont fait connaître ; Charles Darwin était à bord du second." },
    { x = -408331, z = -502468, r = 5000, text = "L'archipel Wollaston, inhabité, au sud de l'île Navarino : les dernières terres avant le cap Horn." },
    { x = -436216, z = -493109, r = 3000, text = "Le cap Horn, falaise d'environ 425 m à l'extrémité sud de l'île Hornos : le dernier cap des Amériques. Les navigateurs néerlandais Schouten et Le Maire l'ont franchi les premiers en 1616 et l'ont nommé d'après la ville de Hoorn." },
    { x = 129300, z = -27208, r = 4000, text = "Pebble Island : environ 35 km de long, au nord de la Falkland occidentale. Pendant la guerre des Malouines, le 15 mai 1982, un détachement du SAS y a détruit onze avions argentins sur la piste, lors d'un raid de nuit." },
    { x = 121367, z = -63208, r = 1500, text = "Port Egmont, sur l'île Saunders : le premier établissement britannique des Falkland. Le capitaine John McBride y bâtit un fort en 1766 ; les Espagnols en chassèrent les Britanniques en 1770, qui y revinrent en 1771 avant de partir en 1774 en laissant une plaque." },
    { x = 128290, z = -101007, r = 2500, text = "Carcass Island, nommée d'après le HMS Carcass qui l'a visitée en 1766. Réputée pour ses oiseaux, elle accueille des manchots de Magellan et des caracaras." },
  }
  veafTourGuide.maxAgl = 457      -- 1 500 ft
  veafTourGuide.repeatAfter = 600 -- s
  function veafTourGuide.check()
    local now = timer.getTime()
    for _, side in pairs({ coalition.side.BLUE, coalition.side.RED }) do
      for _, unit in pairs(coalition.getPlayers(side) or {}) do
        if unit and unit:isExist() and unit:inAir() then
          local p = unit:getPoint()
          local agl = p.y - land.getHeight({ x = p.x, y = p.z })
          if agl < veafTourGuide.maxAgl then
            for i, m in ipairs(veafTourGuide.monuments) do
              local dx, dz = p.x - m.x, p.z - m.z
              if dx * dx + dz * dz < m.r * m.r then
                local key = unit:getName() .. '#' .. i
                local last = veafTourGuide.seen[key]
                if not last or now - last > veafTourGuide.repeatAfter then
                  veafTourGuide.seen[key] = now
                  trigger.action.outTextForGroup(unit:getGroup():getID(), m.text, 25)
                end
              end
            end
          end
        end
      end
    end
    return now + 2
  end
  timer.scheduleFunction(function(_, t) local ok, nxt = pcall(veafTourGuide.check) if ok then return nxt end env.error('veafTourGuide: ' .. tostring(nxt)) return t + 10 end, nil, timer.getTime() + 10)
end
-- <<< guides touristiques
