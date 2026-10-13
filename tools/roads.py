"""Point de route le plus proche que DCS donne (land.getClosestPointOnRoads) : python roads.py x,y [x,y ...]"""
import json
import sys
from pathlib import Path

from dcs import exec_lua


def snap(points):
    lua = "local out = {}\nfor _, q in ipairs({" + ",".join("{%d,%d}" % (round(x), round(y)) for x, y in points) + "}) do\n" \
          "  local x, y = land.getClosestPointOnRoads('roads', q[1], q[2])\n" \
          "  out[#out + 1] = string.format('%d,%d', x or -1, y or -1)\nend\nreturn table.concat(out, ';')"
    res = exec_lua(lua)
    return [tuple(int(v) for v in s.split(",")) for s in res.split(";")]


if __name__ == "__main__":
    pts = [tuple(int(v) for v in a.split(",")) for a in sys.argv[1:]]
    for p, q in zip(pts, snap(pts)):
        print(p, "->", q, f"({((p[0]-q[0])**2+(p[1]-q[1])**2)**.5:.0f} m)")


def path(a, b):
    """Chemin par la route (land.findPathOnRoads) de a à b : liste de (x, y), [] si DCS n'en trouve pas."""
    lua = ("local p = land.findPathOnRoads('roads', %d, %d, %d, %d)\nif not p then return '' end\nlocal out = {}\n"
           "for _, q in ipairs(p) do out[#out + 1] = string.format('%%d,%%d', q.x, q.y) end\nreturn table.concat(out, ';')"
           % (a[0], a[1], b[0], b[1]))
    res = exec_lua(lua)
    return [tuple(int(v) for v in s.split(",")) for s in res.split(";")] if res else []


def length(pts):
    return sum(((pts[i][0] - pts[i + 1][0]) ** 2 + (pts[i][1] - pts[i + 1][1]) ** 2) ** .5 for i in range(len(pts) - 1))


ROUTES = Path(__file__).with_name("road_routes.json")


def convoy_route(key, a, b, km0, km1, step_km=4.0):
    """Points d'un convoi : le tronçon km0..km1 du chemin par la route de a à b (relevé dans DCS une fois, gardé dans
    tools/road_routes.json). Tous sur la route ; un point tous les `step_km` environ, premier et dernier compris."""
    cache = json.loads(ROUTES.read_text(encoding="utf-8")) if ROUTES.exists() else {}
    if key not in cache:
        sa, sb = snap([a, b])
        p = path(sa, sb)
        if not p:
            raise SystemExit(f"DCS ne trouve pas de chemin par la route pour {key} : {sa} -> {sb}")
        cache[key] = p
        ROUTES.write_text(json.dumps(cache), encoding="utf-8")
    p = cache[key]
    dist, acc = [0.0], 0.0
    for i in range(len(p) - 1):
        acc += ((p[i][0] - p[i + 1][0]) ** 2 + (p[i][1] - p[i + 1][1]) ** 2) ** .5
        dist.append(acc)
    pts, want = [], km0 * 1000
    while want < km1 * 1000:
        pts.append(tuple(p[min(range(len(p)), key=lambda i: abs(dist[i] - want))]))
        want += step_km * 1000
    pts.append(tuple(p[min(range(len(p)), key=lambda i: abs(dist[i] - km1 * 1000))]))
    return pts
