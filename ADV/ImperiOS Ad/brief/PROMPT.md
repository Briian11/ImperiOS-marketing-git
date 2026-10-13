# ImperiOS — Spec Ad v6 · Brief (PASO 1 · revisión 4)

> Estado: **BORRADOR r4, pendiente de tu OK.** No se ha construido el vídeo ni se han gastado créditos. Los SFX originales ya están generados (`assets_in/sfx/`).
> Referencia de estilo: el spec ad «Shopify — First Sale» de tu vídeo `video-demostracion-saas_1.mp4`, analizado en la sección 10 (contact sheet en `brief/ref/`).
> Fuente de marca: `assets_in/brand-kit/`. Datos de producto: tus respuestas del 13/10/2026.

---

## 0. Decisiones cerradas

| # | Tema | Decisión |
|---|---|---|
| 1 | Estética | **Fusión, ajustada a la referencia:** escenario **oscuro `#0A0A0A` con un brillo `#FFD500` difuso** durante casi todo el anuncio, igual que el verde de Shopify. El **blanco cálido `#FAF8F4`** aparece en el cierre: el punto amarillo lo inunda todo y el logo negro del kit aterriza sobre claro, como pide el kit. Tipografía: **Manrope** en todo. |
| 2 | Amarillo | **`#FFD500`** en todo, el mismo de la «i» del logo. Interacción: `#E6C000`. |
| 3 | Formato | **Reel 9:16, 1080×1920 a 60 fps** como maestro y como preview. 16:9 solo si lo pides después. |
| 4 | End card | **Sin end card.** El anuncio termina en el logo, y el último acorde suena ~1,5 s sobre él. |
| 5 | Voz | Española, la más natural. Candidata: **Cristina — Premium Spanish Female (PVC)**, la que ya usaste. |
| 6 | Producto | Datos confirmados por ti (sección 2). Sin capturas del CRM real; la UI es abstracta y está hecha con los componentes del kit. |
| 7 | VO | **Guion nuevo** grabado con Cristina por ElevenLabs. Las tomas v5 quedan solo como referencia de timbre. |
| 8 | v5 | Queda como referencia de seguridad. Los movimientos de abajo son nuevos. |
| 9 | SFX | **Originales, sintetizados en código** (sustituye a la regla «solo de mi biblioteca»). 29 efectos en `assets_in/sfx/`. |
| 10 | Fotos | **Ninguna foto de interior.** La tarjeta de inmueble es UI abstracta: pin de zona en un mapa de líneas, icono de tipo y barra de presupuesto. Sin fotos de stock. |
| 11 | UI de ejemplo | Igual que la referencia recrea Shopify con datos verosímiles, la UI de ImperiOS es **recreada** (no son capturas). Lleva datos de ejemplo realistas y genéricos: iniciales en vez de nombres, zonas reales de Madrid, tipos y rangos de precio. **No son cifras de resultados.** Así se evitan las etiquetas de relleno («Lorem», «Dato por validar»). |

---

## 1. Concepto — «Todo llega al mismo sitio»

Gramática de la referencia, aplicada a ImperiOS: **escenario oscuro, un único brillo de marca, pocos elementos por plano, profundidad de campo marcada y UI recreada que flota en 3D**. La cámara hace foco en una fila cada vez, el kinetic type va palabra a palabra con la palabra clave en amarillo y subrayada, y el cierre va de punto a icono y de icono a wordmark.

Historia: los contactos llegan de portales, campañas y web → aterrizan en una sola lista de leads y se ve qué campaña rinde → la IA cruza zona, tipo y presupuesto con la cartera → aparece el aviso de match y se reactiva al cliente → la agenda compartida se llena de visitas, recordatorios y agentes → «Todo conectado. De principio a fin.» → logo sobre blanco cálido.

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

Los tiempos son provisionales: cuando tenga la toma elegida, **re-temporizo la imagen a la voz**.

| Tiempo | Beat | Imagen / motion | Movimiento propio (no copiado de la referencia) |
|---|---|---|---|
| 0.00–0.60 | Hook | Negro. El brillo amarillo «respira» desde abajo y un cuadrado amarillo (la «i» del logo) late una vez en el centro. | **Pixel heartbeat**: el cuadrado de la «i» es el hilo conductor del anuncio |
| 0.60–3.30 | 1 · Captación | Tres píldoras de origen (Portales, Campañas, Web) flotan a distintas profundidades. La que nombra la voz se enfoca. De cada una salen mini tarjetas de lead que viajan hacia el centro con motion blur. | **Depth-pull**: cada fuente pasa de desenfocada a nítida, sincronizada con la palabra |
| 3.30–6.60 | 2 · Lista + campañas | Las tarjetas aterrizan como filas en una lista «Leads» inclinada en 3D (iniciales, chip de origen, «Piso · Chamberí · 350–400 k€», estado «Nuevo»). Llega una tarjeta «Campañas» con una curva que se dibuja y un contador de leads por campaña. | **Stack-land** (las filas caen apiladas y se asientan) + **curve draw** con brillo en la punta |
| 6.60–10.00 | 3 · Match con IA | Kinetic type, palabra a palabra: «zona · tipo · presupuesto», con la palabra que suena en amarillo. Cada palabra se convierte en una «llave» que gira como un dial y encaja en la tarjeta de inmueble abstracta. | **Combination-dial** |
| 10.00–12.80 | 4 · Reactivar | El cuadrado amarillo se estira hasta formar la notificación «Match · 3 clientes encajan con Ático en Chamberí». La fila de un lead dormido (gris) se ilumina y un botón «Reactivar» se pulsa con un micro-rebote. | **Pixel-stretch notification** + **wake pulse** |
| 12.80–16.30 | 5 · Operativa | Una agenda semanal se ensambla en 3D. Los bloques de visita caen en sus huecos, aparecen chips de recordatorio con campana y avatares de agentes con su insignia de rol. La cámara orbita 10°. | **Calendar cascade** + **orbit reveal** |
| 16.30–18.60 | 6 · Titular | Todo se desenfoca. Kinetic type «Todo conectado.» (700) / «De principio a fin.» (500 cursiva), palabra a palabra, con subrayado amarillo bajo «conectado». | **Underline sweep** |
| 18.60–19.40 | Logo | El cuadrado amarillo crece y el escenario pasa a **blanco cálido**. Se forma el icono iM y luego el wordmark horizontal del kit. | **Pixel-flood** a blanco |
| 19.40–21.00 | Cola | Logo quieto sobre blanco cálido, con una deriva amarilla muy suave. El acorde final suena hasta el final. | — |

**Capa permanente:** brillo `#FFD500` difuso a la deriva (como el verde de la referencia), grano fino, desenfoque de profundidad en todo lo que no habla, motion blur fuerte en cada movimiento y un dolly lento continuo, para que el plano nunca quede quieto.
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
| Pixel heartbeat (hook) | `riser_grid` + `shimmer_glow` + `hit_soft_03` |
| Depth-pull / stack-land / curve draw | `whoosh_long_01/02` + `suck_reverse` + `hit_soft_01/02` + `ticks_granular_curve` |
| Pixel-flood a blanco | `whoosh_low_wipe` |
| Combination-dial | `click_mech_dial_1–3` (pitch ascendente) |
| Pixel-stretch notification + wake pulse | `glitch_wake` + `shimmer_glow` + `hit_metal_01/02` |
| Reactivar (botón) + chips de agenda | `click_ui_01–03` + `pop_dock_01–03`, en estéreo izq./dcha./centro |
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

## 10. Referencia analizada — «Shopify — First Sale» (spec ad de riki.bosso)

Analizada fotograma a fotograma desde tu grabación (`brief/ref/referencia-shopify-contact-sheet.png`). Esto es lo que tomo como **lenguaje**, no como movimientos para copiar:

| Rasgo de la referencia | Cómo lo aplico en ImperiOS |
|---|---|
| Escenario casi negro con **un único brillo verde** de marca, difuso, desde abajo o el centro | Negro `#0A0A0A` + brillo `#FFD500` |
| **Logo al principio** (icono → wordmark) y al final | Solo al final. Al principio va el cuadrado de la «i» como semilla |
| **UI recreada flotando en 3D** (lista de productos, Live View con tarjetas y contadores) | Lista de leads, tarjeta de campañas, tarjeta de inmueble, agenda |
| **Rack focus por filas**: una fila nítida y elevada, el resto desenfocado | Depth-pull en las fuentes y foco en la fila del lead que se reactiva |
| Contadores que suben ($0.00 → valor) y tarjetas que entran escalonadas | Contador de leads por campaña y bloques de agenda en cascada |
| **Kinetic type centrado, pequeño, palabra a palabra**, con la palabra clave en color y subrayada | Mismo principio con Manrope 700/500 y amarillo |
| Pastilla con contorno brillante → **notificación** («Order #1001») | La notificación nace del cuadrado amarillo (pixel-stretch), no de una pastilla |
| Punto de luz → icono → wordmark, y fundido a negro | Punto → **inundación a blanco cálido** → icono → wordmark |
| Ritmo: ~20 s, un plano nuevo cada 1,5–3 s y casi sin cortes secos (todo es transformación) | Igual: transiciones por transformación, sin cortes secos |
