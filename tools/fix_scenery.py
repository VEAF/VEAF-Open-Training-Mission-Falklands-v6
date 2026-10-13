"""Déplace au plus près les véhicules et statiques que DCS dit dans l'eau, ou bloqués (arbres, bâtiments).

Même sonde que probe_scenery.py (Disposition.getSimpleZones, petite question : 5 m libres à moins de 20 m ; surface
« eau » = type 3), sur les positions de la mission, sans unité vivante. Pour chaque unité en défaut : anneaux
de 25 m (100 m pour un FARP) autour de sa position jusqu'à `--max` mètres (400 par défaut), premier point que DCS
dit libre et hors de l'eau. Le déplacement est celui de l'unité seule ; un FARP (hélistation, dépôt de munitions,
décor) bouge d'un bloc. DCS tourne, dcs-serve est lancé, la mission d'arpentage est chargée.

python fix_scenery.py [--apply] [--max 400] [--only NOM]   (sans --apply : rapport seulement)
Un « blocked » n'est pas toujours un arbre (limitation disposition-small-query-blocks-open-grass) : relire le rapport.
"""
import math
import sys

import paths
from dcs import exec_lua
from veaf_mission_mcp.mission_folder import load_folder_mission, save_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
CHUNK = 40
JUDGE = """local pts = %s
local out = {}
local function free(p)
  local ok, c = pcall(Disposition.getSimpleZones, p, 20, 5, 10)
  return ok and type(c) == "table" and #c > 0
end
for _, q in ipairs(pts) do
  local x, z = q[2], q[3]
  local p = {x = x, y = land.getHeight({x = x, y = z}), z = z}
  local verdict
  if land.getSurfaceType({x = x, y = z}) == 3 then verdict = "water"
  elseif free(p) then verdict = "clear" else verdict = "blocked" end
  out[#out + 1] = q[1] .. "=" .. verdict
end
return table.concat(out, ";")"""
SEARCH = """local jobs = %s
local out = {}
local function free(p)
  local ok, c = pcall(Disposition.getSimpleZones, p, 20, 5, 10)
  return ok and type(c) == "table" and #c > 0
end
for _, j in ipairs(jobs) do
  local id, x0, z0, maxr, step, clr = j[1], j[2], j[3], j[4], j[5], j[6]
  local found
  local r = step
  while r <= maxr and not found do
    local n = math.max(8, math.floor(2 * math.pi * r / step))
    for i = 0, n - 1 do
      local a = 2 * math.pi * i / n
      local x, z = x0 + r * math.cos(a), z0 + r * math.sin(a)
      local dry = land.getSurfaceType({x = x, y = z}) ~= 3
      for k = 0, 7 do
        local b = k * math.pi / 4
        if land.getSurfaceType({x = x + clr * math.cos(b), y = z + clr * math.sin(b)}) == 3 then dry = false end
      end
      if dry and free({x = x, y = land.getHeight({x = x, y = z}), z = z}) then
        found = {x, z}
        break
      end
    end
    r = r + step
  end
  out[#out + 1] = id .. "=" .. (found and string.format("%%.0f,%%.0f", found[1], found[2]) or "none")
end
return table.concat(out, ";")"""


def seq(v):
    return [v[k] for k in sorted(v, key=int)] if isinstance(v, dict) else list(v or [])


def lua_list(rows):
    return "{" + ",".join("{" + ",".join(str(v) for v in r) + "}" for r in rows) + "}"


def run(template, rows):
    out = {}
    for i in range(0, len(rows), CHUNK):
        res = exec_lua(template % lua_list(rows[i:i + CHUNK]), timeout=120)
        out.update(kv.split("=", 1) for kv in res.split(";"))
    return out


def main():
    apply = "--apply" in sys.argv
    maxr = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 400
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    mission = load_folder_mission(paths.ROOT)
    m = mission.mission_content
    units = []   # (index, catégorie, groupe, unité)
    for side in m["coalition"].values():
        for c in seq(side.get("country")):
            for cat in ("vehicle", "static"):
                for g in seq((c.get(cat) or {}).get("group")):
                    for u in seq(g["units"]):
                        if only and only not in g["name"]:
                            continue
                        units.append((len(units) + 1, cat, g, u))
    verdict = run(JUDGE, [(n, round(u["x"]), round(u["y"])) for n, cat, g, u in units if cat == "vehicle"] +
                  [(n, round(u["x"]), round(u["y"])) for n, cat, g, u in units if cat == "static"])
    bad = [(n, cat, g, u) for n, cat, g, u in units
           if verdict.get(str(n)) == "water" or (cat == "vehicle" and verdict.get(str(n)) == "blocked")]
    print(f"{len(units)} unités sondées, {len(bad)} en défaut")
    farp_names = {g["name"] for n, cat, g, u in bad if g["name"].startswith("FARP ") and not g["name"].endswith(" - Ammo")}
    jobs = []
    for n, cat, g, u in bad:
        step = 100 if g["name"].startswith("FARP ") else 25
        jobs.append((n, round(u["x"]), round(u["y"]), 2500 if g["name"].startswith("FARP ") else maxr, step,
                     200 if g["name"].startswith("FARP ") else 15))
    found = run(SEARCH, jobs) if jobs else {}
    moved = 0
    done_farps = set()
    for n, cat, g, u in bad:
        res = found.get(str(n), "none")
        label = f"{g['name']} / {u['name'][:40]} ({verdict[str(n)]})"
        if res == "none":
            print(f"  AUCUN POINT : {label}")
            continue
        x, y = (float(v) for v in res.split(","))
        d = math.hypot(x - u["x"], y - u["y"])
        print(f"  {label} -> {x:.0f},{y:.0f} ({d:.0f} m)")
        if apply:
            dx, dy = x - u["x"], y - u["y"]
            if g["name"].startswith("FARP "):
                # tout le FARP bouge d'un bloc : les statiques dont le nom commence par « FARP <nom> »
                base = g["name"].replace(" - Ammo", "")
                if base in done_farps:
                    continue
                done_farps.add(base)
                for side in m["coalition"].values():
                    for c in seq(side.get("country")):
                        for gg in seq((c.get("static") or {}).get("group")):
                            if gg["name"].startswith(base):
                                gg["x"] += dx
                                gg["y"] += dy
                                for uu in seq(gg["units"]):
                                    uu["x"] += dx
                                    uu["y"] += dy
            else:
                u["x"], u["y"] = x, y
                if len(seq(g["units"])) == 1:
                    g["x"], g["y"] = x, y
                for p in seq(g.get("route", {}).get("points"))[:1]:
                    p["x"], p["y"] = x, y
            moved += 1
    if apply:
        print(save_folder_mission(mission, paths.ROOT)["mission_file"], moved, "déplacements")
    else:
        print("rapport seulement (--apply pour écrire)")


if __name__ == "__main__":
    main()
