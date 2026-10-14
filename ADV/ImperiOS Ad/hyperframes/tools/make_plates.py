"""Recorta las «placas» de UI real a partir de las capturas a 2x de la cuenta demo (capture/out).

Los recortes dejan fuera lo que no debe salir en el anuncio: nombre y email del usuario (pie del menú),
botón flotante de ajustes (x > 1935 en la vista a 2000 px), columna de emails @demo.ficticio, referencias TEST-00x / «de prueba»,
el aviso rojo de Meta y las notificaciones de error. Coordenadas en píxeles de la captura 2880×1800.
Uso: python3 tools/make_plates.py  (desde la carpeta hyperframes/)
"""
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parents[2] / "capture" / "out"
DST = Path(__file__).resolve().parents[1] / "assets" / "plates"

S = 1.44  # las coordenadas se tomaron sobre la vista a 2000 px de ancho → ×1.44 = píxeles reales

PLATES = {
    # 01 · Contactos: cabecera, columna de nombres y columnas Fuente/Temperatura/Estado (sin email, teléfono ni ref.)
    "leads-title":   ("01-leads", (382, 112, 700, 200)),
    "leads-names":   ("01-leads", (392, 318, 690, 913)),
    "leads-source":  ("01-leads", (1414, 318, 1830, 913)),
    # 02 · Métricas: gráfica de leads por procedencia / Marketing: cabecera y KPIs (sin el aviso de Meta)
    "metrics-chart": ("02-campanas", (390, 243, 1934, 812)),
    "mkt-title":     ("02b-marketing", (382, 112, 1040, 200)),
    "mkt-kpis":      ("02b-marketing", (388, 446, 1934, 702)),
    # 03 · Coincidencias: cabecera, pestañas y tarjeta de Raúl (sin la línea del email)
    "match-title":   ("03-match", (382, 112, 980, 200)),
    "match-tabs":    ("03-match", (390, 230, 1957, 330)),
    "card-top":      ("03-match", (1449, 433, 1956, 610)),
    "card-name":     ("03-match", (1522, 658, 1930, 687)),
    "card-prop":     ("03-match", (1449, 718, 1956, 880)),
    "card-cta":      ("03-match", (1449, 905, 1956, 1022)),
    # 04 · Notificaciones: campana con contador y la fila «Nueva coincidencia» (sin el subtítulo de prueba)
    "bell":          ("04-aviso-match", (1905, 14, 1968, 64)),
    "notif-head":    ("04-aviso-match", (1514, 84, 1955, 136)),
    "notif-match":   ("04-aviso-match", (1518, 290, 1952, 321)),
    # 05 · Calendario completo del mes
    "calendar":      ("05-agenda", (382, 112, 1934, 1207)),
}

DST.mkdir(parents=True, exist_ok=True)
for name, (shot, box) in PLATES.items():
    im = Image.open(SRC / f"{shot}@2x.png").convert("RGB")
    crop = im.crop(tuple(round(v * S) for v in box))
    crop.save(DST / f"{name}.png", optimize=True)
    print(f"{name}.png {crop.size[0]}×{crop.size[1]}")
