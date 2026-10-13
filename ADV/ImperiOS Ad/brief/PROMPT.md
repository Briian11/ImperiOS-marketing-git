# ImperiOS — Spec Ad v6 · Brief (PASO 1 · revisión 3)

> Estado: **BORRADOR r3, pendiente de tu OK.** No se ha construido el vídeo ni se han gastado créditos. Los SFX originales ya están generados (`assets_in/sfx/`).
> Referencia de estilo: https://www.instagram.com/reel/Dd9g2AbR9P_/ (no se puede abrir desde la sesión en la nube; ver sección 9).
> Fuente de marca: `assets_in/brand-kit/`. Datos de producto: tus respuestas del 13/10/2026.

---

## 0. Decisiones cerradas

| # | Tema | Decisión |
|---|---|---|
| 1 | Estética | **Fusión**: escenario base **blanco cálido** con brillo amarillo a la deriva. Los beats de producto (match y operativa) pasan a un **escenario oscuro `#0A0A0A`**, con acabado Apple/Spotify y mucho motion blur. Tipografía: **Manrope** en todo (la de la marca). |
| 2 | Amarillo | **`#FFD500`** en todo, el mismo de la «i» del logo. Interacción: `#E6C000`. |
| 3 | Formato | **Reel 9:16, 1080×1920 a 60 fps** como maestro y como preview. 16:9 solo si lo pides después. |
| 4 | End card | **Sin end card.** El anuncio termina en el logo, y el último acorde suena ~1,5 s sobre él. |
| 5 | Voz | Española, la más natural. Candidata: **Cristina — Premium Spanish Female (PVC)**, la que ya usaste. |
| 6 | Producto | Datos confirmados por ti (sección 2). Sin capturas del CRM real; la UI es abstracta y está hecha con los componentes del kit. |
| 7 | VO | **Guion nuevo** grabado con Cristina por ElevenLabs. Las tomas v5 quedan solo como referencia de timbre. |
| 8 | v5 | Queda como referencia de seguridad. Los movimientos de abajo son nuevos. |
| 9 | SFX | **Originales, sintetizados en código** (sustituye a la regla «solo de mi biblioteca»). 29 efectos en `assets_in/sfx/`. |
| 10 | Fotos | **Ninguna foto de interior.** La tarjeta de inmueble es UI abstracta: pin de zona en un mapa de líneas, icono de tipo y barra de presupuesto. Sin fotos de stock. |

---

## 1. Concepto — «Todo llega al mismo sitio»

Los leads entran desde los bordes del encuadre: portales, campañas y web. Un campo magnético los atrae hacia un único panel, y las campañas muestran su rendimiento al llegar. El escenario pasa a negro: la IA cruza zona, tipo y presupuesto con la cartera, y una línea amarilla une cliente e inmueble. Después la operativa (agenda de visitas, recordatorios, agentes con su cartera y permisos) se acopla al panel como módulos que encajan. Vuelta al blanco y cierre con el titular de la landing y el logo.

Mensajes en orden: **captación (+ campañas medidas) → match con IA → operativa centralizada.**

---

## 2. Guion (español de España · ~19 s)

Frases completas y claras para altavoz de móvil. Son 52 palabras, a ~2,8 palabras/s.

| # | Locución | Texto en pantalla | Dato que lo respalda |
|---|---|---|---|
| 1 | «Tus contactos llegan de portales, campañas y tu web.» | **Portales** · **Campañas** · **Web** | Captación multicanal |
| 2 | «Con Imperios, todos entran en un solo panel, y ves qué campaña funciona.» | *Un solo panel.* + mini gráfico de rendimiento sin cifras | Campañas conectadas con su rendimiento y estadísticas |
| 3 | «La inteligencia artificial cruza zona, tipo y presupuesto con tu cartera.» | **Match con IA** · Zona · Tipo · Presupuesto | Match con IA (preferencias ↔ propiedades) |
| 4 | «Y cuando hay match, reactivas al cliente con una oportunidad real.» | **Reactivar** | Reactivación de contactos por coincidencia |
| 5 | «Visitas, recordatorios y agentes, coordinados desde la misma agenda.» | **Visitas** · **Recordatorios** · **Agentes** | Agenda compartida, recordatorios automáticos, carteras y permisos por rol |
| 6 | «Imperios. Todo conectado, de principio a fin.» | **Todo conectado.** *De principio a fin.* + logo | Titular de la landing |

- **Pronunciación:** en el texto que va a ElevenLabs escribo «Imperios» (im-pe-rios). En pantalla siempre aparece el logo o «ImperiOS».
- **Sin cifras** de resultados ni testimonios. El gráfico de campañas es una forma animada, sin números inventados.

---

## 3. Beat sheet (9:16 · 60 fps)

Los tiempos son provisionales: cuando elijas la toma, **re-temporizo la imagen a la voz**.

| Tiempo | Beat | Escenario | Imagen / motion | Movimiento nuevo |
|---|---|---|---|---|
| 0.00–0.40 | Hook | Blanco | La cuadrícula de 40 px del kit se enciende en onda radial. Un punto `#FFD500` cae y rebota una vez. | **Grid ignition** |
| 0.40–3.30 | 1 · Captación | Blanco | Tres chips de origen entran desde 3 bordes con overshoot y estela. Kinetic type con máscara vertical por palabra. | **Edge-slingshot** |
| 3.30–6.60 | 2 · Panel + campañas | Blanco → panel negro | Campo magnético: los chips se convierten en tarjetas de lead dentro de un panel que se despliega desde una línea. Del chip «Campañas» sale una curva de rendimiento que se dibuja y brilla. | **Magnetic funnel** + **line-to-panel unfold** + **curve draw** |
| 6.60–10.00 | 3 · Match con IA | **Negro** | Un wipe circular pasa el escenario a negro. Tres «llaves» (Zona, Tipo, Presupuesto) giran como un dial y encajan en una tarjeta de inmueble abstracta (pin en un mapa de líneas, icono de tipo, barra de presupuesto; sin foto). | **Combination-dial** |
| 10.00–12.80 | 4 · Reactivar | Negro | La tarjeta del cliente, que estaba gris y dormida, se ilumina en amarillo y una línea Bézier la une al inmueble, con partículas. «Reactivar» con tracking-in. | **Wake pulse** + **bezier snap** |
| 12.80–16.30 | 5 · Operativa | Negro → blanco | La cámara se aleja: los módulos Visitas, Recordatorios y Agentes se acoplan al panel, que rota 8° y encaja. Una agenda compartida se rellena en cascada. | **Dock & lock** + **calendar cascade** |
| 16.30–19.00 | 6 · Cierre | Blanco | Todo colapsa a un punto `#FFD500` que se abre en iris y revela el titular (700 / 500 cursiva, −0.035em) y el logo del kit. | **Dot-iris reveal** |
| 19.00–20.50 | Cola | Blanco | Logo quieto con el brillo a la deriva; el acorde final suena hasta el final. | — |

**Capa permanente de motion graphics:** brillo `#FFD500` difuso a la deriva, partículas finas, contador `01 / 06` por beat (patrón del kit) y una línea guía de 2 px que hilvana todos los beats.
**Zona segura Reels:** el contenido clave queda dentro de 1080×1420 centrado.

---

## 4. Voz (ElevenLabs)

- Voz: **Cristina (PVC, español de España)**, `eleven_multilingual_v2`. Parto de los ajustes de tus tomas: stability 0.50, similarity 0.75, speed 1.00.
- **2 tomas en una sola llamada.**
- Estimación: el guion tiene ~370 caracteres → **~750 créditos** por las 2 tomas.

## 5. Música (hecha en código)

- Original, ~100 BPM, Re mayor / Si menor: pluck con sidechain, pad cálido y sub suave. En los beats oscuros (3–5) se oscurece con filtro y gana pulso.
- **≥15 dB por debajo de la VO** mientras habla, con automatización por palabra y sin limitador sobre la voz.
- Silencio de ~300 ms antes de «Imperios» → acorde final abierto que suena sobre el logo.

## 6. Plan de SFX (originales, sintetizados en código · `assets_in/sfx/INDEX.md`)

| Momento | Categoría |
|---|---|
| Cada palabra/título | `whoosh_short_01–04` (HPF 300 Hz, por debajo de la voz) |
| Cada aterrizaje | `hit_soft_01–03` |
| Grid ignition | `riser_grid` + `shimmer_glow` |
| Magnetic funnel / curve draw | `whoosh_long_01/02` + `suck_reverse` + `ticks_granular_curve` |
| Wipe a negro | `whoosh_low_wipe` |
| Combination-dial | `click_mech_dial_1–3` (pitch ascendente) |
| Wake pulse + bezier snap | `glitch_wake` + `shimmer_glow` + `hit_metal_01/02` |
| Dock & lock ×3 | `pop_dock_01–03` + `click_ui_01–03`, en estéreo izq./dcha./centro |
| Calendar cascade | `ticks_granular_calendar` |
| Dot-iris + logo | `sub_drop` + `logo_sting` (acorde de Re mayor, mismo tono que la música) |

Master a **−14 LUFS / −1 dBTP**.

## 7. Lista de assets

| Asset | Fuente | Licencia | Estado |
|---|---|---|---|
| Logo, Manrope, componentes UI | Kit de marca | ImperiOS / SIL OFL 1.1 | ✅ en `assets_in/brand-kit/` |
| Tomas VO v5 (Cristina ×2) | Tus descargas de ElevenLabs | Tu plan | ✅ en `assets_in/vo/` (solo referencia) |
| SFX (29) | Sintetizados en código, `tools/sfx_synth.py` | Originales | ✅ en `assets_in/sfx/` |
| VO nueva (Cristina, 2 tomas) | ElevenLabs | Tu plan | ⏳ **bloqueada**: ver sección 9 |

## 8. Entregables

1. PREVIEW v1 9:16 + contact sheet → iteramos.
2. Final 9:16 1080×1920 a 60 fps (H.264 alta calidad + ProRes 422 HQ), stems (VO / música / SFX) y README.
3. Solo si lo pides: proyecto completo de DaVinci Resolve.

## 9. Bloqueos de la sesión en la nube

- **ElevenLabs:** la política de red del entorno bloquea `api.elevenlabs.io` y no hay clave configurada. Hay dos formas de desbloquearlo:
  - **A.** Añadir `api.elevenlabs.io` a *Allowed domains* y la clave como variable de entorno `ELEVENLABS_API_KEY`, en la configuración del entorno. Después hay que abrir una sesión nueva para que tome los cambios.
  - **B.** Generarlo tú en ElevenLabs con el texto de `brief/VO_SCRIPT.txt`: voz Cristina, multilingual v2, stability 0.50, similarity 0.75, speed 1.00, 2 tomas. Después subes los mp3.
- **Reel de referencia:** `www.instagram.com` también está bloqueado y requiere sesión. Descarga el vídeo y súbelo aquí para que pueda analizar ritmo, transiciones y tipografía.
