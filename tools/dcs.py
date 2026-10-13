"""Exécute du Lua dans DCS par le pont dcs-serve (la mission d'arpentage ou de test tourne, dcs-serve est lancé).

La clé est lue dans le dcs-serve.yaml indiqué par DCS_SERVE_YAML (par défaut celui du balayage guidé, dans
~/.veaf/clear-ground/dcs-serve/) ; elle part dans un en-tête, jamais affichée.
"""
import json
import os
import urllib.request
from pathlib import Path

import yaml

CFG = Path(os.environ.get("DCS_SERVE_YAML", Path.home() / ".veaf" / "clear-ground" / "dcs-serve" / "dcs-serve.yaml"))


def exec_lua(code, timeout=60):
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    req = urllib.request.Request(
        f"http://{cfg.get('http_host', '127.0.0.1')}:{cfg.get('http_port', 8080)}/api/exec",
        data=json.dumps({"code": code, "timeout": timeout}).encode(),
        headers={"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout + 30) as r:
        body = json.loads(r.read().decode("utf-8"))
    return body.get("result", body)


if __name__ == "__main__":
    print(exec_lua("return tostring(land.getHeight({x = 73318, y = 47169}))"))
