## Pour les créateurs de mission

Construite de zéro le 13/10/2026 avec VEAF Mission Creation Tools (`veaf-tools` 6.29.0) et le serveur MCP `veaf-mission-mcp`, d'après le prompt Open Training de VMCT, en s'inspirant de l'Open Training Falklands v5 (`VEAF-Open-Training-Mission-Falklands`, 2025) sans la recopier.
La v5 était un squelette : des modèles de spawn et de slots dynamiques, aucun groupe posé, aucune zone ; elle n'a donc donné que la carte. Ses coordonnées sont dans un ancien repère de la carte (elles tombent en plein Pacifique avec la projection actuelle) et n'ont pas été reprises.
Ce qui est nouveau : les camps (le Royaume-Uni et le Chili bleus, une force hostile rouge sur la côte argentine et à Port Stanley, décision de David du 13/10/2026) ; des slots dynamiques sur 9 bases bleues et 3 rouges ; dix-sept vraies zones de combat ; toutes les batteries posées par alias VEAF (`#veafInterpreter`) ; trois circuits touristiques ; pas de variantes météo (le serveur VEAF fixe météo et heure) ; aucun mod exigé (la v5 en exigeait trois).

### Construire

```powershell
# outils et scripts VEAF installés par l'updater (veaf-tools.exe + published/, hors dépôt)
.\veaf-tools.exe mission validate

# configuration serveur : sécurité active, logs info, une seule mission (la météo est celle du serveur VEAF)
.\veaf-tools.exe mission build

# essais sur un poste : sécurité coupée, logs debug, noms de groupes lisibles
.\veaf-tools.exe mission build --profile LOCAL_TEST
```

Après un build `LOCAL_TEST`, refaire un build serveur avant de committer : le profil réécrit `src/scripts/veaf-config.lua`.

Mission de test locale (game master par camp, A-10C II en slot classique à Mount Pleasant, pont dcs-bridge) : `tools/make_test_mission.py` → `bridge/bridge-Falklands-OT.miz`.
Les slots dynamiques ne marchent qu'en multijoueur.

### Fichiers

| Fichier | Rôle |
|---|---|
| `mission.yaml` | Identité, sécurité, profil `LOCAL_TEST`, modules, zones (niveaux imbriqués par `includes:`), QRA, CAP, missions scénarisées, actifs, sanctuaires |
| `src/mission/` | La mission DCS éclatée (groupes, zones de déclenchement, aérodromes, dessins F10, briefing, sons des balises touristiques) |
| `src/scripts/mission-script.lua` | Les guides touristiques (messages au survol des sites), écrits par `tools/gen_07c_guide.py` |
| `src/presets.yaml` | Plan radio bleu et rouge ; canaux d'aérodromes aux fréquences que DCS donne aux tours |
| `src/waypoints.yaml` | Points de navigation injectés dans les appareils joueurs |
| `src/warehouses.yaml` | Bases qui offrent des slots (`exclude_airports` pour les autres), carburant et munitions illimités |
| `src/dynamic-slot-templates.yaml` | Appareils proposés en slots dynamiques : modernes seulement, sans mods |
| `ctld-config.yaml` | CTLD ; `jtacLaserCodeMax` abaissé pour les codes imposés des drones ; rayon logistique des aérodromes laissé à 250 m |
| `docs/carte.jpg`, `docs/cartes/` | La carte de ce briefing et ses zooms (fond OpenStreetMap) ; les mêmes images sont dans `src/mission/l10n/DEFAULT/` pour le briefing DCS, listées côté bleu et neutre seulement |
| `docs/portees.md` | Tableau des portées : chaque défense et chaque zone face à ce qu'elle ne doit pas atteindre |
| `tools/` | Scripts qui ont construit la mission (lots `gen_*`), et ceux qui produisent briefing, cartes et contrôles (voir `tools/README.md`) |

### Régénérer ce document

Ce README est **généré depuis la mission**. Après tout changement, depuis le dossier `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
python sync_zones.py      # bloc COMBATZONE de mission.yaml (noms, menus, briefings) depuis gen_07 et gen_08
python gather.py          # mission -> tools/briefing_data.json
python gen_readme.py      # ce README, et les cartes (gen_map.py)
python check_portees.py   # tableau docs/portees.md (ligne VERDICT)
python check_overlap.py   # aucun groupe étranger dans le cercle d'une zone de combat (ligne VERDICT)
python verify.py          # contrôles du .miz construit (ligne VERDICT)
```

### Limites connues

- **La carte Falklands n'est pas encore supportée de bout en bout par VMCT** : absente de l'énumération de `scaffold_mission` et de `theatre-defaults.yaml`, sans grille d'altitude, parkings ni fréquences de tours livrés. Ces trois jeux de données ont été relevés dans DCS le 13/10/2026 (balayage au pas de 250 m, 350 places de parking sur 27 aérodromes, fréquences de 26 aérodromes) et ajoutés au checkout VMCT, non commités : voir `tools/retours-vmct.md`.
- **Terre et mer** : les placements au sol sont contrôlés contre la grille d'altitude balayée dans DCS, puis sondés dans DCS (`tools/probe_scenery.py` : eau, arbres, bâtiments). 15 unités déplacées sur 176 véhicules, plus un FARP tombé dans un lac ; les 176 sont libres. Les statiques sont seulement contrôlés contre l'eau. À vérifier en jeu : routes des convois, dessins F10, aspect du ciel.
- **Convois** : leurs routes sont les chemins que DCS donne par la route entre deux lieux (`land.findPathOnRoads`), tous les points en « On Road » à 12 m/s. Leur déroulement en jeu n'est pas mesuré.
- **Les sites du tourisme** : leur présence dans le décor DCS est à confirmer en jeu ; les textes du guide viennent de connaissances générales (chiffres arrondis), à relire.
- Les portées utilisées pour le contrôle des défenses sont le `threat_range_m` de la base d'unités DCS livrée avec VMCT.
- Les missions scénarisées n'ont pas de condition de réussite ou d'échec (le YAML ne sait pas en porter).
- Codes laser des drones : comme sur l'OT Syrie, `jtacLaserCodeMax: 1686` et des Reaper en bas de plage (1511, 1512), sur la fréquence que CTLD en déduit (35.55 et 35.6 FM).
- Le briefing DCS ne montre les cartes qu'aux camps bleu et neutre (un pilote rouge identifié par DCS peut n'en avoir aucune) : sinon un pilote dont DCS ignore le camp les verrait deux fois.
- Les QRA décollent de la piste (parkings capturés) ; leur comportement une fois en l'air est celui du rôle `zone_defense` que le build leur donne.
