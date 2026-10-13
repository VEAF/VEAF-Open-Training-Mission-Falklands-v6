# Outils de la mission

Scripts Python qui ont construit la mission et qui produisent ce qu'on ne tape pas à la main : le briefing, les cartes, la mission de test, les contrôles.
Ils importent le code Python de VMCT : par défaut le dépôt voisin `../VEAF-Mission-Creation-Tools` (branche `develop`), ou le dossier désigné par la variable `VMCT_PY` (le dossier `src/python/veaf-tools` d'un autre checkout).
Ils se lancent depuis `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
$PY = (poetry -C ..\..\VEAF-Mission-Creation-Tools env info -p) + "\Scripts\python.exe"
& $PY gather.py
```

Pipeline repris de l'OT Sinaï v6 (lui-même venu du Golfe Persique puis des Mariannes), adapté aux Falkland.
Données de la carte relevées dans DCS le 13/10/2026 et gardées dans le checkout VMCT, non commitées : la grille d'altitude (`~/.veaf/terrain/Falklands.terrain`, `veaf-tools dcs terrain-sweep Falklands`), les parkings (`veaf_libs/data/parking/Falklands.json`) et les fréquences des tours (`airfield-frequencies.yaml`). Voir `retours-vmct.md`.

## Construction (historique, à ne pas rejouer)

Chaque `gen_NN_*.py` écrit un lot d'actions `veaf-mission-mcp` dans `batches/`, que `mcp.py batch batches/<lot>.json` exécute dans le processus.
**Un lot ne se rejoue pas** : `add_group` ne dédoublonne pas, un second passage crée des doublons (les dessins F10, eux, sont refusés par nom).
Les lots au sol ont besoin de la grille d'altitude Falklands : `lib.spot()`, `lib.land()` et `lib.flat_spot()` ramènent chaque position sur la terre ferme et refusent sans elle.

| Script | Lot |
|---|---|
| `geocode_places.py` | Lieux réels (`places.json`) ; les homonymes hors du théâtre sont remplacés par leurs coordonnées réelles dans `lib.py` |
| `gen_04_bases.py` | Camp des aérodromes, slots dynamiques |
| `gen_05_soutien.py`, `gen_05c_corrections.py` | Ravitailleurs, AWACS, escortes, Reaper 1 ; Overlord 1 et Reaper 1 déplacés |
| `gen_05b_farps_porte_avions.py` | Quatre FARP, deux groupes aéronavals, slots sur les ponts |
| `gen_06_defense.py`, `gen_06b_corrections.py` | Défense aérienne permanente (`#veafInterpreter`) ; un radar déplacé hors d'une zone |
| `gen_07_entrainement.py`, `gen_07d_corrections.py` | Les 3 familles × 3 niveaux d'entraînement, et les trois zones touristiques |
| `gen_07b_tourisme.py` | Balises radio des circuits (sons morse écrits dans `sons/`) |
| `gen_07c_guide.py` | Guides touristiques : bloc Lua de `src/scripts/mission-script.lua` (se rejoue sans doublon) |
| `gen_08_zones.py`, `gen_08b_corrections.py` | Les 17 vraies zones de combat, Reaper 2 ; Z14 ramenée à 800 m |
| `gen_09_qra_cap.py`, `gen_09b_qra_piste.py` | QRA et CAP à la demande ; QRA refaites en départ piste |
| `gen_10_joueurs.py` | Sanctuaires, arène, groupes des missions scénarisées |
| `gen_11_config.py` | `mission.yaml` : identité, profils, ASSETS, SANCTUARY, `combat_missions:`, CTLD (se rejoue) |
| `gen_12_presets.py`, `gen_13_waypoints.py`, `gen_14_slots_dynamiques.py` | `src/presets.yaml`, `src/waypoints.yaml`, `src/dynamic-slot-templates.yaml` |
| `gen_15_identite.py`, `gen_16_dessins.py`, `gen_16b_corrections.py` | Date, météo de base, bullseye, briefing DCS ; dessins F10 ; front du Chili redessiné |
| `inert_targets.py`, `ground_control_roles.py`, `fix_convoys_on_road.py`, `fix_farp_freq.py`, `fix_scenery.py` | Cibles inertes (tir interdit, sans dispersion) ; rôles sans avion à 5 par camp ; convois « On Road » à 12 m/s ; fréquence d'un FARP ; déplacement des unités dans l'eau ou dans les arbres, d'après la sonde DCS |
| `dcs.py`, `roads.py` | Lua dans DCS par le pont ; routes des convois (`land.findPathOnRoads`, gardées dans `road_routes.json`) |

## Après tout changement

| Script | Ce qu'il fait |
|---|---|
| `sync_zones.py` | Réécrit le bloc `COMBATZONE` de `mission.yaml` (noms, menus, inclusions, briefings) depuis `gen_07` et `gen_08`, qui en sont la source |
| `gather.py` | Relève dans la mission tout ce que le briefing affiche → `briefing_data.json` |
| `gen_readme.py` | Écrit `README.md` (le briefing des pilotes) et redessine les cartes par `gen_map.py` |
| `gen_map.py` | Carte générale `docs/carte.jpg` et zooms `docs/cartes/` sur fond OpenStreetMap (tuiles en cache dans `tiles/`), copiés dans `src/mission/l10n/DEFAULT/` et déclarés dans la mission |
| `check_portees.py` | Portée de chaque défense et de chaque zone face à ce qu'elle ne doit pas atteindre → `docs/portees.md` ; ligne `VERDICT` |
| `check_overlap.py` | Aucun groupe étranger dans le cercle d'une zone de combat ; ligne `VERDICT` |
| `check_presets.py` | Plan radio : aucun doublon dans une liste, aucun canal sur une tour ; ligne `VERDICT` |
| `verify.py` | Contrôles du `.miz` construit (noms, slots, soutien, porteurs, images, météo, sécurité) ; ligne `VERDICT` |
| `probe_scenery.py` | Sonde DCS (eau, arbres, bâtiments) sur chaque véhicule ; `probe_zones.py` : niveaux d'entraînement imbriqués et convois qui roulent (mission de test en cours) |
| `make_test_mission.py` | Mission de test locale `bridge/bridge-Falklands-OT.miz` (LOCAL_TEST, game master, A-10C II à Mount Pleasant, dcs-bridge), puis rebuild serveur |

Ordre : `sync_zones.py`, build serveur (`.\veaf-tools.exe mission build`), `gather.py`, `gen_readme.py`, rebuild serveur (les cartes sont dans le `.miz`), `check_portees.py`, `check_overlap.py`, `verify.py`.

Retours sur les outils VMCT : `retours-vmct.md`.
