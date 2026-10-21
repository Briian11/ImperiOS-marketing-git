"""Campaña v4: monta la VO (gancho + cuerpo) y construye el timeline sincronizado con sus palabras.

Uso: python3 build_timeline_v4.py <largo|corto> <gancho.words.json> <gancho.mp3> <cuerpo.words.json> <cuerpo.mp3> <out.json> <out_vo.wav>
- Los tiempos de palabra vienen de ElevenLabs Scribe (lista [palabra, inicio, fin]).
- La VO se acelera con atempo TEMPO (sin cambiar el tono) para acercar la pieza a 15 s / 30 s; todos los tiempos se escalan igual.
- Cada bloque de texto en pantalla aparece con la palabra hablada; cada escena arranca justo antes de la frase que la narra.
"""
import json
import os
import subprocess
import sys

TEMPO = 1.07
PRE = 0.2      # silencio antes del gancho
GAP = 0.3      # pausa entre el final del gancho y «Con Imperios»
TAIL = 1.8     # cola tras «demo» (botón + acorde final)

kind, hw_path, h_audio, bw_path, b_audio, out, vo_out = sys.argv[1:8]
HW = json.load(open(hw_path))
BW = json.load(open(bw_path))
h_end = HW[-1][2] + .06
BO = PRE + h_end / TEMPO + GAP          # dónde empieza el cuerpo en la línea de tiempo

# VO compuesta: silencio + gancho recortado + pausa + cuerpo, todo a TEMPO, 48 kHz mono
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", h_audio, "-i", b_audio, "-filter_complex",
    f"[0]atrim=0:{h_end:.3f},aresample=48000,aformat=channel_layouts=mono,atempo={TEMPO},apad=pad_dur={GAP}[h];"
    f"[1]aresample=48000,aformat=channel_layouts=mono,atempo={TEMPO}[b];[h][b]concat=n=2:v=0:a=1",
    "-c:a", "pcm_f32le", vo_out], check=True)


def hs(i):
    return PRE + HW[i][1] / TEMPO


def S(i):
    return BO + BW[i][1] / TEMPO


def E(i):
    return BO + BW[i][2] / TEMPO


def find(word, start=0):
    """Índice de la primera palabra que empieza por `word` (sin puntuación) desde `start`."""
    for i in range(start, len(BW)):
        if BW[i][0].strip("¿?¡!.,:;").lower().startswith(word.lower()):
            return i
    raise KeyError(word)


B = {"hook": S(0) - .1, "hookCol": .32}
r = lambda xs, sc: [round(x - B[sc], 3) for x in xs]

if kind == "largo":
    # Con Imperios, lo centralizas absolutamente todo. Todos tus leads … sitio: portales …, tu web, campañas … y WhatsApp.
    # Y ves qué campañas y qué propiedades te traen más clientes. La IA cruza las características de tus propiedades
    # con lo que busca cada cliente, y le envía automáticamente por WhatsApp las que encajan. Visitas, agentes y
    # recordatorios automáticos, coordinados desde la misma agenda. Imperios. Todo conectado, de principio a fin. Pide tu demo.
    lo = find("lo"); tod = find("Todos"); y2 = find("Y", find("WhatsApp") + 1); la = find("La")
    y4 = find("y", find("cliente", la) + 1); vis = find("Visitas"); imp2 = find("Imperios", vis); todo = find("Todo", imp2)
    fin = find("fin", todo); pide = find("Pide", fin); demo = find("demo", pide)
    B["s0"] = B["hook"] + .05
    B["s1"] = S(tod) - .25
    B["s2"] = S(y2) - .13
    B["s3"] = S(la) - .13
    B["s4"] = S(y4) - .13
    B["s5"] = S(vis) - .13
    B["s6"] = S(imp2) - .13
    B["logo"] = E(fin) + .03
    B["cta"] = S(demo) + .33
    end = E(len(BW) - 1) + TAIL       # tras la última palabra (el cierre puede ser más largo que «Pide tu demo»)
    por = find("portales"); web = find("web"); cam = find("campañas"); wa = find("WhatsApp")
    cam2 = find("campañas", y2); pro2 = find("propiedades", y2); car = find("características"); pro3 = find("propiedades", car)
    bus = find("busca", car); cli3 = find("cliente", bus); env = find("envía", y4); aut = find("automáticamente", env)
    wa4 = find("WhatsApp", env); enc = find("encajan", env); age = find("agentes", vis); rec = find("recordatorios", vis)
    wt = {
        "kt0": r([S(i) for i in range(lo, lo + 4)], "s0"),                       # Lo centralizas / absolutamente / todo.
        "kt1": r([S(i) for i in [tod, tod + 1, tod + 2, tod + 4, tod + 5, tod + 6, tod + 7]], "s1"),   # Todos tus leads, en un solo sitio.
        "src": r([S(por), S(web), S(cam), S(wa)], "s1"),
        "kt2": r([S(i) for i in [y2 + 2, cam2, cam2 + 1, pro2, pro2 + 1, pro2 + 2, pro2 + 3, pro2 + 4]], "s2"),  # Qué campañas y propiedades / te traen más clientes.
        "kt3": r([S(pro3 - 1), S(pro3), S(pro3 + 1), S(pro3 + 2), S(pro3 + 3), S(bus), S(bus + 1), S(cli3)], "s3"),  # Tus propiedades / × lo que busca / cada cliente.
        "m3": r([S(car), S(pro3), S(bus)], "s3"),
        "kt4": r([S(y4), S(y4 + 1), (S(y4 + 1) + S(env)) / 2, S(env), S(wa4 - 1), S(wa4)], "s4"),   # Y se las envía / por WhatsApp.
        "s4ev": r([S(aut), S(wa4), S(enc)], "s4"),
        "kt5": r([S(i) for i in [vis, age, age + 1, rec, rec + 1]], "s5"),     # Visitas, agentes y / recordatorios / automáticos.
        "s5ev": r([S(age), S(rec)], "s5"),
        "kt6": r([S(i) for i in range(todo, todo + 6)], "s6"),                  # Todo conectado. / De principio a fin.
    }
else:
    # Con Imperios, todos tus leads entran en un solo sitio: portales, web, campañas y WhatsApp.
    # La IA envía a cada cliente, por WhatsApp, las propiedades que encajan. Imperios. Pide tu demo.
    tod = find("todos"); la = find("La"); env = find("envía", la); cli = find("cliente", env); wa2 = find("WhatsApp", cli)
    pro = find("propiedades", wa2); enc = find("encajan", pro); imp2 = find("Imperios", enc); pide = find("Pide", imp2); demo = find("demo", pide)
    B["s1"] = B["hook"] + .6
    B["s3"] = S(la) - .13
    B["s2"] = B["s3"] - .05
    B["s4"] = S(cli) - .13
    B["logo"] = S(imp2) - .25
    B["s5"] = B["logo"]
    B["s6"] = B["logo"]
    B["cta"] = S(pide) + .2
    B["skip"] = ["s2", "s5", "s6"]
    end = E(len(BW) - 1) + TAIL       # tras la última palabra (el cierre puede ser más largo que «Pide tu demo»)
    por = find("portales"); web = find("web"); cam = find("campañas"); wa = find("WhatsApp")
    d3 = B["s4"] - B["s3"]
    wt = {
        "kt1": r([S(i) for i in [tod, tod + 1, tod + 2, tod + 4, tod + 5, tod + 6, tod + 7]], "s1"),
        "src": r([S(por), S(web), S(cam), S(wa)], "s1"),
        # el texto del match no se dice literalmente en la corta: se reparte por la escena
        "kt3": [round(.4 + i * (d3 - .9) / 7, 3) for i in range(8)],
        "m3": [round(.55, 3), round(.4 + 4 * (d3 - .9) / 7, 3), round(.4 + 6 * (d3 - .9) / 7, 3)],
        "kt4": r([B["s4"] + .15, B["s4"] + .25, B["s4"] + .35, B["s4"] + .45, S(wa2) - .2, S(wa2)], "s4"),
        "s4ev": r([S(wa2), S(pro), S(enc)], "s4"),
    }

B["wt"] = wt
end = max(end, B["cta"] + 3.0)   # el botón aparece en cta+0,3 s: al menos 2,7 s de «Pide tu demo · Gratis, sin compromiso» en pantalla
if os.environ.get("CTA_SUB"):
    B["ctaSub"] = os.environ["CTA_SUB"]   # texto bajo el botón; admite <br>
B = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in B.items()}
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_v4.py {kind}: VO a atempo {TEMPO}; gancho {hw_path}, cuerpo {bw_path}."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k != "wt"}))
