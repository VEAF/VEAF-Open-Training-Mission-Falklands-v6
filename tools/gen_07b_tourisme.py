"""Lot 07b : balises radio des circuits touristiques — sons fabriqués ici, émission FM en boucle.

Chaque balise répète son indicatif en morse sur une tonalité de 800 Hz : des fichiers WAV écrits par ce script dans
tools/sons/ (aucun son emprunté), embarqués par add_sound. Fréquences FM 30.0-38.0, hors de la bande des tours (à
confirmer avec check_presets.py).
Les balises sont permanentes : leur nom ne commence pas par celui d'une zone touristique, qui ne les capture donc
pas (elles guident vers les sites avant toute activation).
Les guides (messages au survol des sites) sont du Lua dans src/scripts/mission-script.lua (gen_07c_guide.py).
"""
import math
import struct
import wave

from gen_07c_guide import SITES
from lib import BLUE_CL, BLUE_UK, ROOT, Batch, flat_spot, relief, xy

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
         "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
         "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
         "Y": "-.--", "Z": "--.."}
RATE, TONE, DOT = 8000, 800, 0.1


def morse_wav(code, path):
    """Écrit l'indicatif `code` en morse (point 100 ms, trait 300 ms), suivi de 2 s de silence."""
    samples = []

    def tone(t):
        n = int(RATE * t)
        for i in range(n):
            env = min(1.0, i / 40, (n - i) / 40)   # attaque et relâche de 5 ms : pas de clic
            samples.append(int(12000 * env * math.sin(2 * math.pi * TONE * i / RATE)))

    def silence(t):
        samples.extend([0] * int(RATE * t))

    for letter in code:
        for sym in MORSE[letter]:
            tone(DOT if sym == "." else 3 * DOT)
            silence(DOT)
        silence(2 * DOT)
    silence(2.0)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    return len(samples) / RATE


# nom, indicatif, MHz FM, clé du site (gen_07c_guide.SITES), camp du porteur, sous-titre
BEACONS = [(f"Balise {s['code']}", s["code"], s["mhz"], s["key"], BLUE_CL if s["zone"] != "Egmont" else BLUE_UK,
            f"{s['code']} — {s['name']}") for s in SITES if s.get("code")]

if __name__ == "__main__":
    sons = ROOT / "tools/sons"
    sons.mkdir(exist_ok=True)
    b = Batch()
    for name, code, mhz, key, side, sub in BEACONS:
        wav = sons / f"balise-{code}.wav"
        dur = morse_wav(code, wav)
        pos = next(s["pos"] for s in SITES if s["key"] == key)
        p = flat_spot(pos, search=5000, r=100, step=250, margin=300, what=name)   # au pied du site, sur du plat
        b.act("add_sound", sound_path=wav.as_posix())
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p),
              units=[{"type": "Hummer", "name": name}], keep_position=True)
        b.act("edit_route", group_name=name, operation="add_task", index=1, task="set_frequency",
              task_params={"frequency_mhz": mhz, "modulation": "FM"})
        b.act("edit_route", group_name=name, operation="add_task", index=1, task="transmit_message",
              task_params={"sound": wav.name, "loop": True, "duration_s": math.ceil(dur), "subtitle": sub})
        print(f"{name:12} {mhz} FM  {dur:.1f} s  {round(p[0])} {round(p[1])}  relief {relief(p, 100):.0f} m")
    b.save("07b-tourisme.json")
