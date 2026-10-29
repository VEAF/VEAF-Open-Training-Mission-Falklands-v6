---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_OpenTraining_Falklands_ICAO_EGYP"
veaf.config.era = veaf.ERA.MODERN
veaf.silenceAtcOnAllAirbases()
veaf.HideNamesFromSpawnedGroups = true

veaf.config.language = "fr"

-- ── Airfield channels of the mission's radio plan (src/presets.yaml, `bases`) ──────
if veafAirbases then
    veafAirbases.MissionChannels = {
        [1] = { alias = "Base-Port Stanley", title = "Port Stanley", uhf = 250.45, vhf = 118.1, fm = 38.85 },
        [2] = { alias = "Base-Mount Pleasant", title = "Mount Pleasant / 59X", uhf = 250.8, vhf = 133.35, fm = 39.2 },
        [3] = { alias = "Base-San Carlos FOB", title = "San Carlos FOB", uhf = 250.85, vhf = 134.35, fm = 39.25 },
        [5] = { alias = "Base-Rio Gallegos", title = "Rio Gallegos", uhf = 250.9, vhf = 119.1, fm = 39.3 },
        [6] = { alias = "Base-Rio Grande", title = "Rio Grande / 31X", uhf = 250.95, vhf = 118.3, fm = 39.35 },
        [9] = { alias = "Base-Punta Arenas", title = "Punta Arenas", uhf = 251.1, vhf = 118.7, fm = 39.5 },
        [11] = { alias = "Base-San Julian", title = "San Julian", uhf = 250.05, vhf = 118.05, fm = 38.45 },
        [12] = { alias = "Base-Puerto Williams", title = "Puerto Williams", uhf = 250.1, vhf = 118.5, fm = 38.5 },
        [13] = { alias = "Base-Puerto Natales", title = "Puerto Natales", uhf = 250.15, vhf = 128.1, fm = 38.55 },
        [15] = { alias = "Base-Puerto Santa Cruz", title = "Puerto Santa Cruz", uhf = 250.25, vhf = 118.6, fm = 38.65 },
        [16] = { alias = "Base-Comandante Luis Piedrabuena", title = "Comandante Luis Piedrabuena", uhf = 250.3, vhf = 122.1, fm = 38.7 },
        [17] = { alias = "Base-Tolhuin", title = "Tolhuin", uhf = 250.35, vhf = 118.15, fm = 38.75 },
        [18] = { alias = "Base-Porvenir", title = "Porvenir", uhf = 250.4, vhf = 126.7, fm = 38.8 },
        [19] = { alias = "Base-Almirante Schroeders", title = "Almirante Schroeders", uhf = 229.0, vhf = 118.25, fm = 38.6 },
        [24] = { alias = "Base-Goose Green", title = "Goose Green", uhf = 250.65, vhf = 126.0, fm = 39.05 },
        [29] = { alias = "Base-Gull Point", title = "Gull Point", uhf = 234.5, vhf = 126.5, fm = 39.5 },
    }
end

-- ── Global log level ─────────────────────────────────────────────────────────
veaf.ForcedLogLevel = "info"

-- ── CTLD 2 ───────────────────────────────────────────────────────────────────
-- Configuration lives in ctld-config.yaml (edit it with ctld-tools); this only starts it.
veaf.config.manage_airbase_logistics = true
veaf.config.airbase_logistics_radius = 250
veaf.config.airbase_occupation_radius = 2000
veaf.config.airbase_logistics_tick = 30
-- One module's initialisation error must not take the others down (FIX-DEMO-MISSION-FINDINGS 02).
local function veafGuardedInit(name, initialize)
    local ok, err = xpcall(initialize, function(e)
        if debug and debug.traceback then
            return debug.traceback(tostring(e), 2)
        end
        return tostring(e)
    end)
    if not ok then
        veaf.loggers.get(veaf.Id):error("%s init failed: %s", name, err)
    end
end

veafGuardedInit("CTLD", function()
if ctld then
    veaf.ctld_initialize()
end
end)

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

veafGuardedInit("SECURITY", function()
if veafSecurity then
    veafSecurity.initialize()
end
end)

veafGuardedInit("RADIO", function()
if veafRadio then
    veafRadio.initialize(true)
end
end)

veafGuardedInit("SHORTCUTS", function()
if veafShortcuts then
    veafShortcuts.initialize()
end
end)

veafGuardedInit("NAMEDPOINTS", function()
if veafNamedPoints then
    veafNamedPoints.initialize({})
end
end)

veafGuardedInit("SPAWN", function()
if veafSpawn then
    veafSpawn.initialize()
end
end)

-- ── Combat ──

veafGuardedInit("CARRIER", function()
if veafCarrierOperations then
    veafCarrierOperations.initialize(true)
end
end)

veafGuardedInit("CASMISSION", function()
if veafCasMission then
    veafCasMission.initialize()
end
end)

veafGuardedInit("TRANSPORTMISSION", function()
if veafTransportMission then
    veafTransportMission.initialize()
end
end)

veafGuardedInit("COMBATMISSION", function()
if veafCombatMission then
    veafCombatMission.addCapMission("CAP-Santa-Cruz-MiG29", "CAP rouge MiG-29S (Fox 1) — Patagonie sud — FL220", "Deux MiG-29S armés de R-27R, R-73 et R-60 patrouillent entre Rio Gallegos et le cap Vierges, au FL220. Emport : R-73*2,R-60M*2,R-27R*2,Fuel-1500.", false, true)
    veafCombatMission.addCapMission("CAP-Fuego-Su27", "CAP rouge Su-27 (Fox 1, longue portée) — Terre de Feu argentine — FL260", "Deux Su-27 armés de R-27ER et R-73 patrouillent au-dessus de la côte atlantique de la Terre de Feu, au nord-est de Rio Grande, au FL260. Emport : R-73*4,R-27ER*6.", false, true)
    veafCombatMission.addCapMission("CAP-Nord-MiG31", "CAP rouge MiG-31 (intercepteur haut et rapide, R-33) — Patagonie nord — FL380", "Deux MiG-31 armés de R-33 patrouillent haut et vite entre Puerto Santa Cruz et San Julian, au FL380. Emport : R-40R*2,R-33*4.", false, true)
    veafCombatMission.addCapMission("Raid-Tu22M", "Raid rouge Tu-22M3 à intercepter — Pali Aike — FL300", "Deux bombardiers Tu-22M3 chargés de bombes tournent à l'ouest de Rio Gallegos, au FL300, prêts à frapper Punta Arenas : les intercepter. Emport : FAB-500*33.", false, true)
    veafCombatMission.addCapMission("CAP-Falkland-F15", "CAP bleue F-15C (Fox 3) — détroit des Falkland — FL250", "Deux F-15C britanniques couvrent le détroit des Falkland, de San Carlos à Goose Green, au FL250. Emport : AIM-9*4,AIM-120*4,Fuel.", false, true)
    veafCombatMission.addCapMission("CAP-Magellan-F16", "CAP bleue F-16C (Fox 3) — détroit de Magellan — FL220", "Deux F-16C chiliens patrouillent le détroit de Magellan, autour de Punta Arenas, au FL220. Emport : AIM-120C*4,AIM-9M*2,ECM,Fuel*2.", false, true)
    veafCombatMission.addCapMission("CAP-Beagle-F16", "CAP bleue F-16C (Fox 3) — canal Beagle — FL240", "Deux F-16C chiliens patrouillent au-dessus de l'île Navarino et de Puerto Williams, au FL240. Emport : AIM-120C*4,AIM-9M*2,ECM,Fuel*2.", false, true)
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Defense-MountPleasant")
        :setFriendlyName("Défense — raid rouge sur Mount Pleasant")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Deux Su-24M armés de missiles antiradar ouvrent la route à quatre Su-34 chargés de bombes, escortés de deux Su-30, partis de l'est de Port Stanley vers la base de Mount Pleasant, 27 nm plus à l'ouest. Abattez les bombardiers avant le largage.
Échec si la base est bombardée (constaté par vous : la mission ne le vérifie pas).]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("SEAD")
            :setGroups({"SC-Defense-MountPleasant-SEAD"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Bombardiers")
            :setGroups({"SC-Defense-MountPleasant-Bombers"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Defense-MountPleasant-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Interception-VIP")
        :setFriendlyName("Interception — transport VIP de Rio Gallegos à Rio Grande")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Un IL-76 emmène l'état-major rouge de Rio Gallegos vers Rio Grande, escorté par deux MiG-29S, en longeant la côte par le cap Vierges. Interceptez-le avant Rio Grande : la fin de la route est sous la QRA et les défenses de Rio Grande.]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Transport")
            :setGroups({"SC-Intercept-VIP-Il76"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Intercept-VIP-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.initialize()
end
end)

veafGuardedInit("COMBATZONE", function()
if veafCombatZone then
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortHoward_Easy")
        :setFriendlyName("H1 Hélico Port Howard — facile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de la Falkland occidentale, à 6 nm au sud-ouest du FARP Port Howard : cibles inertes (chars, blindés et camions immobiles, tir interdit).
Position : bullseye 078°/323 nm (S51°45.261' W059°42.032'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 67 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 56 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortHoward_Medium")
        :setFriendlyName("H2 Hélico Port Howard — moyen")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de la Falkland occidentale : de l'artillerie antiaérienne légère (ZU-23, parfois un Shilka) en plus des cibles du niveau facile.
Position : bullseye 078°/323 nm (S51°45.261' W059°42.032'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 67 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 56 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortHoward_Hard")
        :setFriendlyName("H3 Hélico Port Howard — difficile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de la Falkland occidentale, avec une défense courte portée réaliste : un SA-13 et une équipe de lance-missiles portatifs SA-18, à guidage infrarouge.
Position : bullseye 078°/323 nm (S51°45.261' W059°42.032'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 67 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 56 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_MountAdam_Easy")
        :setFriendlyName("A1 Attaque Mount Adam — facile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir air-sol à l'ouest de Mount Adam, sur la Falkland occidentale, à 78 nm du front de Stanley : blindés et camions immobiles en tir interdit, dépôt de carburant et poste de commandement. Le drone Reaper 1 tourne au-dessus.
Position : bullseye 076°/307 nm (S51°35.334' W060°11.981'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 77 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 67 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_MountAdam_Medium")
        :setFriendlyName("A2 Attaque Mount Adam — moyen")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de Mount Adam : une compagnie blindée active et de l'artillerie antiaérienne légère en plus des cibles du niveau facile.
Position : bullseye 076°/307 nm (S51°35.334' W060°11.981'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 77 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 67 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_MountAdam_Hard")
        :setFriendlyName("A3 Attaque Mount Adam — difficile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de Mount Adam : un second groupe blindé et une défense courte portée à guidage infrarouge (SA-13 ou SA-9), avec un Shilka.
Position : bullseye 076°/307 nm (S51°35.334' W060°11.981'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 77 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 67 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortStephens_Easy")
        :setFriendlyName("S1 SEAD Port Stephens — facile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD au sud-ouest de la Falkland occidentale, près de Port Stephens, à 33 nm du champ de tir d'attaque : une batterie sol-air moyenne portée, SA-6 ou SA-11 tirée au sort.
Position : bullseye 080°/284 nm (S52°02.229' W060°42.557'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 58 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 52 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortStephens_Medium")
        :setFriendlyName("S2 SEAD Port Stephens — moyen")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD de Port Stephens : la batterie moyenne portée est protégée par une défense courte portée (SA-15, SA-8).
Position : bullseye 080°/284 nm (S52°02.229' W060°42.557'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 58 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 52 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortStephens_Hard")
        :setFriendlyName("S3 SEAD Port Stephens — difficile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD de Port Stephens en réseau Skynet : un radar d'alerte avancée guide les batteries, qui restent éteintes jusqu'au dernier moment.
Position : bullseye 080°/284 nm (S52°02.229' W060°42.557'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 58 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 52 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Paine")
        :setFriendlyName("T1 Tourisme — Torres del Paine")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne de la Patagonie des glaciers, hors combat, au départ du FARP Torres del Paine (3 nm au nord-ouest). Circuit : les tours de granit (Las Torres), les Cuernos et le Paine Grande, puis le lac Grey et son glacier, un front de la grande calotte glaciaire de Patagonie. Une balise radio FM à chaque site ; survolez un site à moins de 1 500 ft sol et un guide vous le raconte. Excursion : le glacier Perito Moreno, de l'autre côté de la frontière, en territoire rouge (aucune défense permanente).
Position : bullseye 285°/189 nm (S50°59.747' W072°52.415').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CapHorn")
        :setFriendlyName("T2 Tourisme — cap Horn")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne du bout du monde, hors combat, au départ de Puerto Williams. Circuit : le canal Beagle, les îles Wollaston et le cap Horn. Une balise radio FM par site ; survolez-les à moins de 1 500 ft sol pour entendre le guide. Le circuit reste côté chilien, à plus de 20 nm de la base argentine d'Ushuaia.
Position : bullseye 160°/159 nm (S54°54.690' W067°32.369').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortEgmont")
        :setFriendlyName("T3 Tourisme — Falkland occidentales")
        :setRadioGroupName("Tourisme")
        :setBriefing([[Visite aérienne des Falkland occidentales, hors combat, au départ du FARP Port Howard (26 nm au nord-ouest). Circuit : Pebble Island, Saunders Island et Port Egmont, Carcass Island. Une balise radio FM par site ; survolez-les à moins de 1 500 ft sol pour entendre le guide.
Position : bullseye 074°/314 nm (S51°22.163' W060°05.025').]])
        :setCompletable(false)
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CretesStanley")
        :setFriendlyName("Z01 Front des îles — crêtes de Mount Longdon et Wireless Ridge")
        :setRadioGroupName("Front")
        :setBriefing([[Les crêtes à l'ouest de Port Stanley, tenues par une brigade mécanisée rouge : chars, blindés et lance-roquettes en position, à 21 nm de Mount Pleasant. Détruire les blindés et l'artillerie ; défense courte portée (SA-15, SA-13) et artillerie antiaérienne, sous la QRA de Port Stanley.
Position : bullseye 079°/388 nm (S51°40.508' W057°57.460'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 80 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 69 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_RioTurbio")
        :setFriendlyName("Z02 Front de Patagonie — frontière de Rio Turbio")
        :setRadioGroupName("Front")
        :setBriefing([[La ligne de défense rouge de Rio Turbio, à 15 nm de Puerto Natales, côté argentin : chars enterrés, blindés et artillerie automotrice. Défense courte portée seulement (SA-13, Shilka) : le drone Reaper 2 la désigne au laser.
Position : bullseye 278°/151 nm (S51°32.940' W072°11.178'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 29 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 51 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_SanSebastian")
        :setFriendlyName("Z03 Front de Terre de Feu — carrefour de San Sebastián")
        :setRadioGroupName("Front")
        :setBriefing([[Le poste frontière de San Sebastián, sur la route de Rio Grande, face au Chili : une brigade mécanisée rouge et ses lance-roquettes. Détruire les blindés et les Grad ; défense SA-8 et artillerie antiaérienne. Aucune QRA ne couvre le secteur (Rio Grande est à 66 nm).
Position : bullseye 188°/31 nm (S52°49.200' W068°36.000'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 149 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 134 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_MountKent")
        :setFriendlyName("Z04 SEAD — site SA-6 du Mount Kent")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site SA-6 perché sur Mount Kent, au-dessus de la vallée de Stanley, relié à un radar d'alerte avancée en réseau Skynet, à 16 nm de Mount Pleasant. Détruire le radar de conduite de tir et les lanceurs ; un Shilka protège le site.
Position : bullseye 079°/383 nm (S51°40.408' W058°06.600'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 78 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 67 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PaliAike")
        :setFriendlyName("Z05 SEAD — site SA-11 de Pali Aike")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site sol-air qui couvre la steppe de Pali Aike, entre Rio Gallegos et la frontière : une batterie SA-11 ou SA-6 tirée au sort, son radar d'alerte avancée et un Shilka. Sous la couverture lointaine du SA-10 de Rio Gallegos.
Position : bullseye 283°/56 nm (S51°58.981' W069°44.932'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 99 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 93 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_RioGrandeSAM")
        :setFriendlyName("Z06 SEAD — site SA-11 de Rio Grande")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site SA-11 au sud-sud-est de Rio Grande, sur la côte atlantique de la Terre de Feu, avec son radar d'alerte avancée en réseau Skynet et un SA-15. Détruire le radar de conduite de tir et les lanceurs.
Position : bullseye 156°/97 nm (S53°52.649' W067°41.041'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 206 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 186 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiStanley")
        :setFriendlyName("Z07 Convoi — Stanley vers Fitzroy")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi de renforts quitte Port Stanley par la route de Fitzroy, vers le sud-ouest. L'arrêter avant Fitzroy, à 9 nm de Mount Pleasant ; il porte sa propre artillerie antiaérienne (ZU-23) et un SA-9.
Position : bullseye 080°/391 nm (S51°41.919' W057°52.770'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 80 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 69 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiRuta3")
        :setFriendlyName("Z08 Convoi — route 3, de Rio Gallegos vers Piedrabuena")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi blindé quitte Rio Gallegos par la route 3 vers Piedrabuena pour renforcer le nord. Le détruire en route ; il est escorté par un SA-13, sous la QRA de Rio Gallegos au départ.
Position : bullseye 309°/58 nm (S51°37.145' W069°23.720'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 115 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 114 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ConvoiTolhuin")
        :setFriendlyName("Z09 Convoi — route 3, de Rio Grande vers Tolhuin")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi de carburant roule de Rio Grande vers Tolhuin, sur la route 3 de Terre de Feu, pour ravitailler le front de San Sebastián et du canal Beagle. Le détruire avant Tolhuin ; il porte sa propre artillerie antiaérienne.
Position : bullseye 155°/93 nm (S53°48.806' W067°38.563'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 205 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 185 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_EtatMajorGallegos")
        :setFriendlyName("Z10 Frappe — état-major de Rio Gallegos")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Le poste de commandement rouge du sud de la Patagonie, dans les faubourgs de Rio Gallegos : bunkers, centre de transmissions, dépôt de carburant. Tout détruire ; défense SA-15 et Shilka, sous la QRA et le SA-10 de Rio Gallegos.
Position : bullseye 314°/54 nm (S51°37.356' W069°13.086'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 122 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 120 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortSantaCruz")
        :setFriendlyName("Z11 Frappe — port de Puerto Santa Cruz")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Le port de Puerto Santa Cruz, au bord de l'estuaire : entrepôts de munitions et de matériel, réservoirs. Tout détruire ; ZU-23 sur place, sous le SA-11 permanent de la ville.
Position : bullseye 349°/140 nm (S50°01.198' W068°31.204'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 191 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 200 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_BaseNavaleUshuaia")
        :setFriendlyName("Z12 Frappe — base navale d'Ushuaia")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[La base navale d'Ushuaia, sur le canal Beagle, à 24 nm de Puerto Williams : entrepôts, dépôts de carburant, poste de commandement. Tout détruire ; défense courte portée seulement (SA-15 permanent de la base, ZU-23), hors de la QRA de Rio Grande (65 nm).
Position : bullseye 170°/150 nm (S54°48.438' W068°18.505'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 225 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 201 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ScudRioChico")
        :setFriendlyName("Z13 Frappe — base de missiles sol-sol de Rio Chico")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Une base de missiles sol-sol à l'ouest de Rio Chico, d'où les Scud menacent Punta Arenas : lanceurs et camions de ravitaillement. Détruire les lanceurs ; défense SA-15 et Shilka.
Position : bullseye 309°/55 nm (S51°39.692' W069°20.202'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 117 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 115 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_PortStanley")
        :setFriendlyName("Z14 OCA — base aérienne de Port Stanley")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[L'aérodrome de Port Stanley, tenu par le rouge à 27 nm de Mount Pleasant : chasseurs-bombardiers au parking, hangars et carburant. Tout détruire au sol ; défense SA-15 et Shilka, sous la QRA de la base.
Position : bullseye 080°/395 nm (S51°41.640' W057°46.679'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 82 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 72 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Piedrabuena")
        :setFriendlyName("Z15 OCA — base aérienne de Piedrabuena")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[L'aérodrome de Comandante Luis Piedrabuena, plateforme rouge du nord de la Patagonie : avions de transport et hélicoptères d'attaque au sol, hangars. Tout détruire au sol ; défense SA-6 et ZU-23, plus le SA-10 et le SA-15 permanents de la base.
Position : bullseye 342°/143 nm (S49°59.750' W068°56.596'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 180 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 191 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_BlocusStanley")
        :setFriendlyName("Z16 Antinavire — corvettes devant Port Stanley")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Trois frégates rouges croisent à l'est de Port Stanley, à 17 nm au large de la baie, pour couvrir l'enclave et couper la route de la flotte bleue. Les couler : frégates à défense courte portée.
Position : bullseye 080°/412 nm (S51°38.059' W057°19.628'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 94 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 84 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_DetroitLeMaire")
        :setFriendlyName("Z17 Antinavire — escadre du détroit de Le Maire")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Le croiseur lance-missiles rouge Moskva et deux frégates croisent dans le détroit de Le Maire, entre la Terre de Feu et l'île des États, pour fermer l'accès à la mer de la Terre de Feu. Les couler : le Moskva porte des missiles sol-air à 40 nm, les frégates à courte portée.
Position : bullseye 132°/194 nm (S54°47.567' W064°54.216'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 214 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 223 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.GetZone("combatZone_PortHoward_Medium"):addZoneElementsFromZoneNamed("combatZone_PortHoward_Easy")
    veafCombatZone.GetZone("combatZone_PortHoward_Hard"):addZoneElementsFromZoneNamed("combatZone_PortHoward_Medium")
    veafCombatZone.GetZone("combatZone_PortHoward_Hard"):addZoneElementsFromZoneNamed("combatZone_PortHoward_Easy")
    veafCombatZone.GetZone("combatZone_MountAdam_Medium"):addZoneElementsFromZoneNamed("combatZone_MountAdam_Easy")
    veafCombatZone.GetZone("combatZone_MountAdam_Hard"):addZoneElementsFromZoneNamed("combatZone_MountAdam_Medium")
    veafCombatZone.GetZone("combatZone_MountAdam_Hard"):addZoneElementsFromZoneNamed("combatZone_MountAdam_Easy")
    veafCombatZone.GetZone("combatZone_PortStephens_Medium"):addZoneElementsFromZoneNamed("combatZone_PortStephens_Easy")
    veafCombatZone.GetZone("combatZone_PortStephens_Hard"):addZoneElementsFromZoneNamed("combatZone_PortStephens_Medium")
    veafCombatZone.GetZone("combatZone_PortStephens_Hard"):addZoneElementsFromZoneNamed("combatZone_PortStephens_Easy")
    veafCombatZone.initialize()
end
end)

veafGuardedInit("QRA", function()
if veafQraManager then
    veafQraManager.initialize()
    local QRA_Port_Stanley = VeafQRA:new()
        :setName("QRA Port Stanley")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-PortStanley")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-PortStanley-MiG29", "QRA-PortStanley-Su27"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-PortStanley-Su30", "QRA-PortStanley-MiG29x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Port Stanley")
        :start()
    local QRA_Rio_Gallegos = VeafQRA:new()
        :setName("QRA Rio Gallegos")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-RioGallegos")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-RioGallegos-Su27", "QRA-RioGallegos-MiG29"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-RioGallegos-Su30", "QRA-RioGallegos-Su27x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Rio Gallegos")
        :start()
    local QRA_Rio_Grande = VeafQRA:new()
        :setName("QRA Rio Grande")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-RioGrande")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-RioGrande-MiG29", "QRA-RioGrande-Su27"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-RioGrande-Su30", "QRA-RioGrande-MiG29x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Rio Grande")
        :start()
    local QRA_San_Julian = VeafQRA:new()
        :setName("QRA San Julian")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-SanJulian")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-SanJulian-Su27", "QRA-SanJulian-MiG29"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-SanJulian-Su30", "QRA-SanJulian-MiG29x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("San Julian")
        :start()
    local QRA_Mount_Pleasant = VeafQRA:new()
        :setName("QRA Mount Pleasant")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-MountPleasant")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-MountPleasant-F15", "QRA-MountPleasant-F16"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-MountPleasant-F15x4", "QRA-MountPleasant-F16x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Mount Pleasant")
        :start()
    local QRA_Punta_Arenas = VeafQRA:new()
        :setName("QRA Punta Arenas")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-PuntaArenas")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-PuntaArenas-F16", "QRA-PuntaArenas-M2000"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-PuntaArenas-F16x4", "QRA-PuntaArenas-M2000x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Punta Arenas")
        :start()
    local QRA_Puerto_Natales = VeafQRA:new()
        :setName("QRA Puerto Natales")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-PuertoNatales")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-PuertoNatales-F16", "QRA-PuertoNatales-M2000"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-PuertoNatales-F16x4", "QRA-PuertoNatales-M2000x4"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Puerto Natales")
        :start()
end
end)

-- ── Features ──

veafGuardedInit("GRASS", function()
if veafGrass then
    veafGrass.initialize()
end
end)

veafGuardedInit("ASSETS", function()
if veafAssets then
    veafAssets.Assets = {
        {sort = 1, name = "Overlord 1", description = "Overlord 1 (E-3A) — AWACS îles", information = "U282.0 — FL300 — orbite est-ouest à l'ouest de la Falkland occidentale", linked = "Overlord 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 2, name = "Magic 1", description = "Magic 1 (E-3A) — AWACS Chili", information = "U283.0 — FL300 — orbite nord-sud au-dessus de Porvenir et de Punta Arenas", linked = "Magic 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 3, name = "Texaco 1", description = "Texaco 1 (KC-135, perche) — îles", information = "TACAN 50Y TX1 — U290.0 — FL220 — piste nord-sud au sud des Falkland, au large de Gull Point", linked = "Texaco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 4, name = "Arco 1", description = "Arco 1 (KC-135 MPRS, panier) — îles", information = "TACAN 51Y AR1 — U291.0 — FL180 — piste nord-sud au sud des Falkland, plus au large", linked = "Arco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 5, name = "Texaco 2", description = "Texaco 2 (KC-135, perche) — Chili", information = "TACAN 52Y TX2 — U292.0 — FL240 — piste nord-sud à l'ouest de Punta Arenas, au-dessus des fjords", linked = "Texaco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 6, name = "Arco 2", description = "Arco 2 (KC-135 MPRS, panier) — Chili", information = "TACAN 53Y AR2 — U293.0 — FL200 — piste nord-sud au sud-ouest de Puerto Natales", linked = "Arco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 7, name = "CSG-74 Stennis", description = "CVN-74 Stennis — Atlantique sud, au sud des Falkland", information = "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", coalition = coalition.side.BLUE},
        {sort = 8, name = "CSG-71 Roosevelt", description = "CVN-71 Roosevelt — Atlantique sud, au large de la Terre de Feu", information = "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", coalition = coalition.side.BLUE},
        {sort = 9, name = "CSG-74 Stennis S3B-Tanker", description = "S-3B du Stennis (ravitailleur embarqué)", information = "TACAN 56Y S74 — U296.0", coalition = coalition.side.BLUE},
        {sort = 10, name = "CSG-71 Roosevelt S3B-Tanker", description = "S-3B du Roosevelt (ravitailleur embarqué)", information = "TACAN 57Y S71 — U297.0", coalition = coalition.side.BLUE},
        {sort = 11, name = "Darkstar 1", description = "Darkstar 1 (E-3A) — AWACS bleu de l'arène", information = "U285.0 — FL300", coalition = coalition.side.BLUE},
        {sort = 12, name = "Wizard 1", description = "Wizard 1 (A-50) — AWACS rouge", information = "U284.0 — FL300 — orbite est-ouest au large de la Terre de Feu argentine", linked = "Wizard 1 - Escort", coalition = coalition.side.RED},
        {sort = 13, name = "Shell 1", description = "Shell 1 (IL-78M) — ravitailleur rouge", information = "U294.0 — FL200 — orbite nord-sud au large de Rio Gallegos", linked = "Shell 1 - Escort", coalition = coalition.side.RED},
        {sort = 14, name = "Focus 1", description = "Focus 1 (A-50) — AWACS rouge de l'arène", information = "U286.0 — FL300", coalition = coalition.side.RED},
        {sort = 15, name = "Reaper 1", description = "Reaper 1 (drone laser) — champ de tir d'attaque", information = "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir d'attaque (zone A), à l'ouest de la Falkland occidentale.", jtac = 1511, freq = "35.55", mod = "FM", coalition = coalition.side.BLUE},
        {sort = 16, name = "Reaper 2", description = "Reaper 2 (drone laser) — front de Rio Turbio", information = "Laser 1512 — FM 35.6. 3 000 m sol au-dessus de la ligne de Rio Turbio (Z02).", jtac = 1512, freq = "35.6", mod = "FM", coalition = coalition.side.BLUE},
    }
    veafAssets.initialize()
end
end)

veafGuardedInit("MOVE", function()
if veafMove then
    veafMove.initialize()
end
end)

veafGuardedInit("SANCTUARY", function()
if veafSanctuary then
    veafSanctuary.initialize()
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Falkland")
        if zone then
            zone:setName("Sanctuaire Falkland")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Magellan")
        if zone then
            zone:setName("Sanctuaire Magellan")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-SanJulian")
        if zone then
            zone:setName("Sanctuaire San Julian")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
end
end)

veafGuardedInit("WEATHER", function()
if veafWeather then
    veafWeather.initialize()
end
end)

veafGuardedInit("REMOTE", function()
if veafRemote then
    veafRemote.initialize()
end
end)

veafGuardedInit("AIRBASES", function()
if veafAirbases then
    veafAirbases.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("MARKERS", function()
if veafMarkers then
    veafMarkers.initialize()
end
end)

veafGuardedInit("TIME", function()
if veafTime then
    veafTime.initialize()
end
end)

veafGuardedInit("UNITS", function()
if veafUnits then
    veafUnits.initialize()
end
end)

veafGuardedInit("CACHE", function()
if veafCacheManager then
    veafCacheManager.initialize()
end
end)

veafGuardedInit("EVENTS", function()
if veafEventHandler then
    veafEventHandler.initialize()
end
end)

-- ── Core ──

veafGuardedInit("GROUNDAI", function()
if veafGroundAI then
    veafGroundAI.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("COMMANDS", function()
if veafCommands then
    veafCommands.initialize()
end
end)

-- ── Features ──

veafGuardedInit("INTERPRETER", function()
if veafInterpreter then
    veafInterpreter.initialize()
end
end)

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("tum", "enable", false)

-- ── Skynet-IADS ──────────────────────────────────────────────────────────────
veafGuardedInit("SKYNET", function()
if veafSkynet then
    veafSkynet.SpotterNetwork = true
    veafSkynet.SpotterView = "off"
    veafSkynet.initialize(false, false, false, false)
end
end)

-- ── CSAR configuration ───────────────────────────────────────────────────────
-- Note: CSAR.lua must be loaded by mission-script.lua before this block.
veafGuardedInit("CSAR", function()
if csar then
    csar.initialize()
end
end)
