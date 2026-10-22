"""Guion visual del vídeo demo corto: por escena, qué estado del CRM se ve, cámara, cursor, clics y focos.
Mismo lenguaje que el demo largo (../ImperiOS Demo/build/spec.py), con menos gestos por escena y cambios de pantalla
directos (deslizamiento) en vez de clics intermedios. Cada acción se ancla a una palabra de la locución.
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
    cam = lambda t, rect, dur=0.8, zmax=1.9: A.append({"t": "cam", "at": t, "dur": dur, "rect": rect, "zmax": zmax})  # noqa: E731
    cur = lambda t, pt, click=True, dur=0.6: A.append({"t": "cursor", "at": t, "dur": dur, "to": pt, "click": click})  # noqa: E731
    ring = lambda t, rect, hold, spot=True: A.append({"t": "ring", "at": t, "hold": hold, "rect": rect, "spot": spot})  # noqa: E731
    sfx = lambda name, t, gain=1.0: A.append({"t": "sfx", "name": name, "at": t, "gain": gain})  # noqa: E731

    def swap(img, t, rect=None, zmax=1.9):
        """Cambio de pantalla sin clic: la anterior sale, la cámara se recoloca y la nueva entra deslizándose."""
        state(img, t)
        cam(t, rect or full(), 0.01, zmax)

    # 0 · Intro: logo → ventana con el panel
    s = S["intro"]
    scene("intro")
    state("01-dashboard", 0.0, 0.01)
    cam(0.0, full(), 0.01)
    A.append({"t": "intro", "at": 0.0, "window": at(s, "CRM", 0, -0.3)})

    # 1 · Contactos: los leads de portales y web entran solos, con su origen y su temperatura
    s = S["contactos"]
    scene("contactos")
    swap("02a-contactos", s["start"])
    col = lambda n: clip(box("02a-contactos", n, 4), 760)  # noqa: E731
    ring(at(s, "portales"), clip(box("02a-contactos", "tabla", 4), 760), at(s, "origen") - at(s, "portales"), False)
    cam(at(s, "Contactos", 0, -0.2), union(col("colContacto"), col("colTemp")), 0.8, 1.3)
    ring(at(s, "origen"), col("colFuente"), at(s, "temperatura") - at(s, "origen"))
    ring(at(s, "temperatura"), col("colTemp"), 1.3)

    # 2 · Chat: Idealista, Fotocasa, web y WhatsApp en una sola bandeja; se responde por WhatsApp
    s = S["chat"]
    scene("chat")
    swap("03a-chat", s["start"])
    lista = box("03a-chat", "lista", 6)
    cam(at(s, "mensajes", 0, -0.3), lista, 0.8, 2.0)
    for src, w in (("srcIdealista", "Idealista"), ("srcFotocasa", "Fotocasa"), ("srcWeb", "web"), ("srcWhatsApp", "WhatsApp")):
        ring(at(s, w), box("03a-chat", src, 9), 0.6)
    ring(at(s, "llegan"), lista, at(s, "respondes") - at(s, "llegan") - 0.6)
    cam(at(s, "respondes", 0, -0.7), full(), 0.55)
    cur(at(s, "respondes", 0, -0.65), center(box("03a-chat", "lead")), dur=0.55)
    state("03b-chat-conversacion", at(s, "respondes", 0, -0.05), 0.25)
    sfx("click_ui_03", at(s, "respondes", 0, -0.12))
    composer = [645, 1006, 1250, 66]
    cam(at(s, "WhatsApp", 1, -0.35), [640, 640, 1280, 440], 0.7, 1.6)
    ring(at(s, "WhatsApp", 1), composer, 1.3)

    # 3 · Coincidencias IA (escenario oscuro): puntúa cada coincidencia → se entra en una → puntuación, criterio a
    # criterio, y lo que pide el cliente frente a lo que ofrece la propiedad
    s = S["ia"]
    scene("ia", dark=True)
    L, M = "06c-match-lista", "06d-match-detalle"
    swap(L, s["start"])
    tarjeta = box(L, "tarjeta", 6)
    cam(at(s, "cruza", 0, -0.3), tarjeta, 0.9, 1.8)
    ring(at(s, "cliente"), tarjeta, at(s, "puntúa") - at(s, "cliente") - 0.1)
    ring(at(s, "puntúa"), [tarjeta[0] + 12, tarjeta[1] + 50, 300, 84], at(s, "coincidencia") - at(s, "puntúa") + 0.4)
    cam(at(s, "coincidencia", 0, 0.25), full(), 0.5)
    cur(at(s, "coincidencia", 0, 0.3), center(box(L, "ver")), dur=0.55)
    state(M, at(s, "Entras", 0, -0.1), 0.3)
    sfx("click_ui_03", at(s, "Entras", 0, -0.18))
    A.append({"t": "cursorOff", "at": at(s, "Entras", 0, 0.25)})
    d = lambda n, pad=6: box(M, n, pad)  # noqa: E731
    cam(at(s, "Entras", 0, 0.2), union(d("puntuacion"), d("estado")), 0.7, 1.5)
    ring(at(s, "Entras", 0, 0.3), d("puntuacion"), at(s, "criterio") - at(s, "Entras") - 0.6)
    cam(at(s, "criterio", 0, -0.35), d("criterios"), 0.8, 1.5)
    ring(at(s, "criterio"), d("criterios"), at(s, "pide") - at(s, "criterio") - 0.3)
    cam(at(s, "pide", 0, -0.35), union(d("comprador"), d("propiedad")), 0.8, 1.4)
    ring(at(s, "cliente", 1), d("comprador"), at(s, "ofrece") - at(s, "cliente", 1))
    ring(at(s, "ofrece"), d("propiedad"), 1.5)

    # 4 · Marketing: campañas → anuncios → tablero de leads (arrastre real de una tarjeta)
    s = S["marketing"]
    scene("marketing")
    swap("08a-marketing", s["start"])
    camp = box("08a-marketing", "campanas", 6)
    cam(at(s, "Marketing", 0, 0.1), camp, 0.8, 1.4)
    ring(at(s, "campaña"), camp, at(s, "anuncio") - at(s, "campaña") - 0.3)
    swap("08c-conjunto", at(s, "anuncio", 0, -0.3), box("08c-conjunto", "anuncios", 8), 1.5)
    ring(at(s, "anuncio", 0, 0.25), box("08c-conjunto", "mejor", 4), at(s, "leads") - at(s, "anuncio") - 0.3)
    swap("08d-leads-antes", at(s, "leads", 0, -0.15), [280, 150, 1400, 560], 1.6)
    card0 = box("08d-leads-antes", "tarjeta")
    tgt = box("08e-leads-despues", "movida")
    cur(at(s, "mueves", 0, -0.6), [card0[0] + 120, card0[1] + 30], False, 0.5)
    A.append({"t": "drag", "at": at(s, "mueves", 0, -0.05), "dur": 0.9, "from": card0, "to": tgt, "img": "08d-leads-antes", "after": "08e-leads-despues"})
    sfx("click_ui_02", at(s, "mueves", 0, -0.05))
    sfx("pop_dock_03", at(s, "mueves", 0, 0.9), 0.6)
    ring(at(s, "mueves", 0, 0.95), tgt, 1.2)

    # 5 · Métricas: leads por portal → cuántos acaban en visita → rendimiento por propiedad → por comercial
    s = S["metricas"]
    scene("metricas")
    swap("09-metricas-portales", s["start"])
    m = lambda n: box("09-metricas-portales", n, 6)  # noqa: E731
    cam(at(s, "Métricas", 0, -0.1), m("procedencia"), 0.8, 1.3)
    ring(at(s, "llegan"), m("procedencia"), at(s, "cuántos", 1) - at(s, "llegan") - 0.1)
    cam(at(s, "cuántos", 1, -0.3), union(m("agendamiento"), m("embudo")), 0.8, 1.6)
    ring(at(s, "acaban"), m("embudo"), at(s, "visita") - at(s, "acaban"))
    ring(at(s, "visita"), m("agendamiento"), at(s, "rendimiento") - at(s, "visita") - 0.3)
    sec = box("09a-rendimiento", "seccion", 6)
    swap("09a-rendimiento", at(s, "rendimiento", 0, -0.3), [sec[0], sec[1] - 40, sec[2], 1000])
    ring(at(s, "propiedad"), union(box("09a-rendimiento", "contactos"), box("09a-rendimiento", "ofertas")), at(s, "comercial") - at(s, "propiedad") - 0.35)
    r = "10a-direccion-reporte"
    swap(r, at(s, "comercial", 0, -0.35), union(box(r, "embudo"), box(r, "tabla")), 1.3)
    ring(at(s, "comercial", 0, 0.3), box(r, "tabla", 6), 1.4)

    # 6 · Y además: panel, ficha de cliente, propiedades publicadas y agenda, en tarjetas sin entrar en detalle
    s = S["ademas"]
    scene("ademas")
    cards = [("01-dashboard", "Panel del día", "panel"), ("04-cliente", "Ficha de cliente", "ficha"),
             ("05c-publicaciones", "Propiedades y publicaciones", "propiedades"), ("07b-calendario-semana", "Agenda del equipo", "agenda")]
    A.append({"t": "montage", "at": s["start"], "cards": [{"img": img, "label": lab, "at": at(s, w, 0, -0.3)} for img, lab, w in cards]})
    for _, _, w in cards:
        sfx("pop_dock_01", at(s, w, 0, -0.25), 0.45)

    # 7 · Cierre
    s = S["cierre"]
    scene("cierre")
    A.append({"t": "outro", "at": s["start"]})
    sfx("logo_sting", s["vo"][0] - 0.2, 0.35)

    # Transición de escena: barrido suave
    for sc in scenes[1:]:
        sfx("whoosh_short_04", sc["start"] - 0.05, 0.35)
    return A
