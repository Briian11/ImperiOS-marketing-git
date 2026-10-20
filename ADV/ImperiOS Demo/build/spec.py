"""Guion visual del vídeo demo: por escena, qué estado del CRM se ve, cámara, cursor, clics y focos.
Cada acción se ancla a una palabra de la locución (at(escena, 'palabra', ocurrencia, desfase)).
Coordenadas en px CSS de documento (las de capture/out/states/*.json); la página mide 1920 de ancho.
"""


def actions(scenes, states, at):
    S = {s["id"]: s for s in scenes}
    A = []

    def box(st, name, pad=0):
        b = states[st]["boxes"].get(name)
        if not b:
            raise KeyError(f"falta la caja {name} en {st}")
        return [b["x"] - pad, b["y"] - pad, b["w"] + 2 * pad, b["h"] + 2 * pad]

    def union(*rs):
        x0 = min(r[0] for r in rs); y0 = min(r[1] for r in rs)
        x1 = max(r[0] + r[2] for r in rs); y1 = max(r[1] + r[3] for r in rs)
        return [x0, y0, x1 - x0, y1 - y0]

    def clip(r, maxh):
        return [r[0], r[1], r[2], min(r[3], maxh)]

    def center(r):
        return [r[0] + r[2] / 2, r[1] + r[3] / 2]

    full = lambda y=0: [0, y, 1920, 1080]  # noqa: E731
    scene = lambda sid, dark=False: A.append({"t": "scene", "id": sid, "label": S[sid]["label"], "n": S[sid]["n"], "at": S[sid]["start"], "dark": dark})  # noqa: E731
    state = lambda img, t, fade=0.35: A.append({"t": "state", "img": img, "at": t, "dur": fade})  # noqa: E731
    cam = lambda t, rect, dur=0.9, zmax=1.9: A.append({"t": "cam", "at": t, "dur": dur, "rect": rect, "zmax": zmax})  # noqa: E731
    cur = lambda t, pt, click=True, dur=0.7: A.append({"t": "cursor", "at": t, "dur": dur, "to": pt, "click": click})  # noqa: E731
    ring = lambda t, rect, hold, spot=True: A.append({"t": "ring", "at": t, "hold": hold, "rect": rect, "spot": spot})  # noqa: E731
    sfx = lambda name, t, gain=1.0: A.append({"t": "sfx", "name": name, "at": t, "gain": gain})  # noqa: E731

    # 0 · Intro: logo → ventana con el Dashboard
    s = S["intro"]
    scene("intro")
    state("01-dashboard", 0.0, 0.01)
    cam(0.0, full(), 0.01)
    A.append({"t": "intro", "at": 0.0, "window": at(s, "Te", 0, -0.3)})

    # 1 · Dashboard
    s = S["dashboard"]
    scene("dashboard")
    kpis = union(box("01-dashboard", "kpi1"), box("01-dashboard", "kpi4"))
    cam(at(s, "propiedades", 0, -0.3), union(kpis, [280, 100, 10, 10]), 1.0)
    ring(at(s, "propiedades"), kpis, at(s, "citas") - at(s, "propiedades") - 0.3)
    cam(at(s, "contactos", 0, -0.2), union(box("01-dashboard", "sinAtender"), box("01-dashboard", "citas")), 1.0)
    ring(at(s, "contactos", 0, 0.4), box("01-dashboard", "sinAtender", 6), at(s, "próximas") - at(s, "contactos") - 0.6)
    ring(at(s, "próximas"), box("01-dashboard", "citas", 6), 1.8)

    # 2 · Contactos: columna Fuente → filtro → Idealista
    s = S["contactos"]
    scene("contactos")
    state("02a-contactos", s["start"])
    cam(s["start"], full(), 0.01)
    col = clip(box("02a-contactos", "colFuente", 4), 760)
    ring(at(s, "Idealista"), col, at(s, "entra") - at(s, "Idealista"))
    cam(at(s, "Idealista", 0, -0.2), union(col, [900, 140, 1000, 300]), 0.9, 1.5)
    cam(at(s, "Contactos,", 0, -0.2), full(), 0.8)
    filtro = box("02a-contactos", "filtro")
    cur(at(s, "filtras", 0, -0.75), center(filtro))
    state("02b-contactos-filtro", at(s, "filtras", 0, 0.05), 0.2)
    sfx("click_ui_01", at(s, "filtras", 0, -0.05))
    cam(at(s, "filtras", 0, 0.1), union(filtro, box("02b-contactos-filtro", "opcion"), [1200, 120, 700, 420]), 0.7, 1.8)
    cur(at(s, "clic.", 0, -0.55), center(box("02b-contactos-filtro", "opcion")))
    state("02c-contactos-idealista", at(s, "clic.", 0, 0.15), 0.25)
    sfx("click_ui_02", at(s, "clic.", 0, 0.05))
    cam(at(s, "clic.", 0, 0.5), full(), 0.9)
    ring(at(s, "clic.", 0, 0.9), clip(box("02c-contactos-idealista", "colFuente", 4), 760), 1.4)

    # 3 · Chat
    s = S["chat"]
    scene("chat")
    state("03a-chat", s["start"])
    cam(s["start"], full(), 0.01)
    ring(at(s, "todos"), box("03a-chat", "lista", 6), at(s, "con", 0) - at(s, "todos") - 0.4)
    lead = box("03a-chat", "lead")
    cur(at(s, "WhatsApp", 0, -0.6), center(lead))
    state("03b-chat-conversacion", at(s, "WhatsApp", 0, 0.1), 0.25)
    sfx("click_ui_03", at(s, "WhatsApp"))
    conv = [650, 200, 1250, 330]
    cam(at(s, "propiedad", 0, -0.4), union(conv, box("03b-chat-conversacion", "propiedad", 10)), 1.0, 1.7)
    ring(at(s, "propiedad"), box("03b-chat-conversacion", "propiedad", 10), 1.6)
    cam(at(s, "asistente", 0, -0.3), full(), 0.9)
    ring(at(s, "asistente"), [650, 200, 1250, 800], 2.2, False)

    # 4 · Ficha de cliente
    s = S["cliente"]
    scene("cliente")
    state("04-cliente", s["start"])
    cam(s["start"], full(), 0.01)
    prefs = box("04-cliente", "prefs", 6)
    cam(at(s, "busca", 0, -0.3), prefs, 1.0, 1.5)
    ring(at(s, "presupuesto"), prefs, at(s, "junto") - at(s, "presupuesto"))
    cam(at(s, "junto", 0, -0.2), union(box("04-cliente", "citas"), box("04-cliente", "origen")), 1.0, 1.6)
    ring(at(s, "citas", 0), box("04-cliente", "citas", 6), 1.6)

    # 5 · Propiedades → ficha → Publicaciones
    s = S["propiedades"]
    scene("propiedades")
    state("05a-propiedades", s["start"])
    cam(s["start"], full(), 0.01)
    cam(at(s, "cartera", 0, -0.4), [270, 220, 1300, 560], 1.2, 1.4)
    fila = box("05a-propiedades", "fila")
    cur(at(s, "Cada", 0, -0.7), [fila[0] + 300, fila[1] + fila[3] / 2])
    state("05b-propiedad-ficha", at(s, "Cada", 0, 0.05), 0.3)
    sfx("click_ui_01", at(s, "Cada", 0, -0.05))
    cam(at(s, "Cada", 0, 0.1), full(), 0.01)
    req = box("05b-propiedad-ficha", "requisitos", 6)
    cam(at(s, "falta", 0, -0.4), union(req, box("05b-propiedad-ficha", "foto")), 1.0, 1.5)
    ring(at(s, "falta"), req, at(s, "Publicaciones") - at(s, "falta") - 0.4)
    state("05c-publicaciones", at(s, "Publicaciones", 0, -0.2), 0.4)
    cam(at(s, "Publicaciones", 0, -0.2), full(), 0.01)
    portales = union(box("05c-publicaciones", "web"), box("05c-publicaciones", "idealista"))
    ring(at(s, "anunciado"), union(portales, clip(box("05c-publicaciones", "tabla"), 360)), 1.6)

    # 6 · Coincidencias IA (escenario oscuro)
    s = S["ia"]
    scene("ia", dark=True)
    state("06a-coincidencias", s["start"])
    cam(s["start"], full(), 0.01)
    tarjeta = box("06a-coincidencias", "tarjeta", 6)
    cam(at(s, "cruza", 0, -0.3), union(tarjeta, box("06a-coincidencias", "tabs")), 1.0, 1.6)
    ring(at(s, "puntúa"), tarjeta, at(s, "sepas") - at(s, "puntúa"))
    pp = box("06a-coincidencias", "porPropiedad")
    cam(at(s, "sepas", 0, -0.2), full(), 0.8)
    cur(at(s, "quién", 0, -0.4), center(pp))
    state("06b-coincidencias-propiedad", at(s, "llamar", 0, 0.05), 0.3)
    sfx("click_ui_02", at(s, "llamar", 0, -0.05))

    # 7 · Agenda: calendario mes → semana → tareas
    s = S["agenda"]
    scene("agenda")
    state("07a-calendario", s["start"])
    cam(s["start"], full(), 0.01)
    sem = box("07a-calendario", "semana")
    cur(at(s, "Calendario", 0, -0.7), center(sem))
    state("07b-calendario-semana", at(s, "Calendario", 0, 0.05), 0.3)
    sfx("click_ui_01", at(s, "Calendario", 0, -0.05))
    cam(at(s, "Calendario", 0, 0.3), [280, 380, 1620, 700], 1.0, 1.4)
    state("07c-tareas", at(s, "tareas", 0, -0.2), 0.4)
    cam(at(s, "tareas", 0, -0.2), full(), 0.01)
    ring(at(s, "tablero"), union(box("07c-tareas", "pendiente"), [280, 164, 1608, 700]), 1.6, False)

    # 8 · Marketing: KPI → campañas → campaña → conjunto/anuncios → leads (arrastre real)
    s = S["marketing"]
    scene("marketing")
    state("08a-marketing", s["start"])
    cam(s["start"], full(), 0.01)
    kp = union(box("08a-marketing", "inversion"), box("08a-marketing", "cpl"))
    ring(at(s, "inviertes"), kp, at(s, "campaña:") - at(s, "inviertes"))
    camp = box("08a-marketing", "campanas", 6)
    cam(at(s, "campaña:", 0, -0.3), camp, 1.0, 1.4)
    ring(at(s, "impresiones"), camp, at(s, "Puedes") - at(s, "impresiones") - 0.2)
    c1 = box("08a-marketing", "campana1")
    cur(at(s, "conjunto", 0, -0.75), [c1[0] + 260, c1[1] + c1[3] / 2])
    state("08b-campana", at(s, "conjunto", 0, 0.05), 0.3)
    sfx("click_ui_03", at(s, "conjunto", 0, -0.05))
    cam(at(s, "conjunto", 0, 0.1), union(box("08b-campana", "embudo"), box("08b-campana", "conjuntos")), 0.8, 1.4)
    k1 = box("08b-campana", "conjunto1")
    cur(at(s, "anuncio", 0, -0.6), [k1[0] + 260, k1[1] + k1[3] / 2])
    state("08c-conjunto", at(s, "anuncio", 0, 0.15), 0.3)
    sfx("click_ui_01", at(s, "anuncio", 0, 0.05))
    cam(at(s, "anuncio", 0, 0.2), box("08c-conjunto", "anuncios", 8), 0.9, 1.5)
    ring(at(s, "funciona"), box("08c-conjunto", "mejor", 4), at(s, "Y") - at(s, "funciona"))
    state("08d-leads-antes", at(s, "Y", 0, -0.1), 0.4)
    cam(at(s, "Y", 0, -0.1), full(), 0.01)
    card0 = box("08d-leads-antes", "tarjeta")
    tgt = box("08e-leads-despues", "movida")
    cam(at(s, "tablero", 0, -0.3), [280, 150, 1400, 560], 1.0, 1.6)
    cur(at(s, "cambias", 0, -0.8), [card0[0] + 120, card0[1] + 30])
    A.append({"t": "drag", "at": at(s, "cambias", 0, -0.05), "dur": 1.1, "from": card0, "to": tgt, "img": "08d-leads-antes", "after": "08e-leads-despues"})
    sfx("click_ui_02", at(s, "cambias", 0, -0.05))
    sfx("pop_dock_03", at(s, "cambias", 0, 1.05), 0.6)
    ring(at(s, "controlados", 0, -0.2), tgt, 1.8)

    # 9 · Rendimiento por propiedad
    s = S["rendimiento"]
    scene("rendimiento")
    state("09a-rendimiento", s["start"])
    sec = box("09a-rendimiento", "seccion", 6)
    cam(s["start"], [sec[0], sec[1] - 40, sec[2], 1000], 0.01)
    cols = union(box("09a-rendimiento", "contactos"), box("09a-rendimiento", "ofertas"))
    ring(at(s, "rendimiento"), cols, at(s, "propiedad,") - at(s, "rendimiento") - 0.6)
    f1 = box("09a-rendimiento", "fila1")
    cur(at(s, "entras", 0, -0.5), [f1[0] + 160, f1[1] + f1[3] / 2])
    state("09b-metricas-propiedad", at(s, "propiedad,", 0, 0.05), 0.3)
    sfx("click_ui_03", at(s, "propiedad,", 0, -0.05))
    cam(at(s, "propiedad,", 0, 0.05), full(), 0.01)
    k = lambda n: box("09b-metricas-propiedad", n, 4)  # noqa: E731
    cam(at(s, "personas", 0, -0.5), union(k("preguntado"), k("canceladas"), k("contactosPor")), 1.0, 1.5)
    ring(at(s, "personas"), k("preguntado"), at(s, "portal") - at(s, "personas") - 0.2)
    ring(at(s, "portal", 0, -0.1), k("contactosPor"), at(s, "cuántas", 1) - at(s, "portal") - 0.1)
    ring(at(s, "visitas", 0), k("visitas"), at(s, "cuántas", 2) - at(s, "visitas"))
    ring(at(s, "cuántas", 2), k("ofertar"), at(s, "Incluso") - at(s, "cuántas", 2))
    cam(at(s, "Incluso", 0, -0.3), union(k("descartan"), k("cancelaron")), 1.0, 1.5)
    ring(at(s, "descartan"), k("descartan"), at(s, "cancelaron") - at(s, "descartan"))
    ring(at(s, "cancelaron"), k("cancelaron"), 1.4)

    # 10 · Dirección: reporte → metas → facturado
    s = S["direccion"]
    scene("direccion")
    state("10a-direccion-reporte", s["start"])
    cam(s["start"], full(), 0.01)
    emb = box("10a-direccion-reporte", "embudo", 6)
    cam(at(s, "embudo", 0, -0.3), union(emb, box("10a-direccion-reporte", "tabla")), 1.0, 1.3)
    ring(at(s, "embudo"), emb, at(s, "llamadas") - at(s, "embudo") - 0.1)
    ring(at(s, "llamadas", 0, -0.1), box("10a-direccion-reporte", "tabla", 6), at(s, "metas") - at(s, "llamadas"))
    state("10b-direccion-metas", at(s, "metas", 0, -0.35), 0.35)
    cam(at(s, "metas", 0, -0.35), union(box("10b-direccion-metas", "comparativa"), box("10b-direccion-metas", "tabla")), 0.01)
    ring(at(s, "metas", 0, 0.1), box("10b-direccion-metas", "tabla", 6), at(s, "facturado") - at(s, "metas") - 0.5)
    state("10c-direccion-facturado", at(s, "facturado", 0, -0.35), 0.35)
    cam(at(s, "facturado", 0, -0.35), full(), 0.01)
    ring(at(s, "facturado", 0, 0.1), union(box("10c-direccion-facturado", "cobrado"), box("10c-direccion-facturado", "pendiente")), 1.6)

    # 11 · Cierre
    s = S["cierre"]
    scene("cierre")
    A.append({"t": "outro", "at": s["start"]})
    sfx("logo_sting", s["vo"][0] - 0.2, 0.35)

    # Transición de escena: barrido suave
    for sc in scenes[1:]:
        sfx("whoosh_short_04", sc["start"] - 0.05, 0.35)
    return A
