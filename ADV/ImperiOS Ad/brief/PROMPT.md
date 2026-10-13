# ImperiOS — Spec Ad v6 · Brief (PASO 1 · revisión 5)

> Estado: **BORRADOR r5, pendiente de tu OK.** No se ha construido el vídeo ni se han gastado créditos. Los SFX originales ya están generados (`assets_in/sfx/`).
> Referencia de estilo: el spec ad «Shopify — First Sale» de tu vídeo `video-demostracion-saas_1.mp4`, analizado en la sección 10 (contact sheet en `brief/ref/`).
> Fuente de marca: `assets_in/brand-kit/`. Datos de producto: tus respuestas del 13/10/2026.

---

## 0. Decisiones cerradas

| # | Tema | Decisión |
|---|---|---|
| 1 | Estética | **Marca ImperiOS primero, referencia después.** La superficie es la de imperios.app: fondo claro `#F5F5F5` con la cuadrícula de 40 px, tarjetas `#FAFAFA` con borde fino y paneles oscuros `#0A0A0A` (patrón «alternar claro y oscuro» del kit). De la referencia tomo **solo la gramática de movimiento**: UI que flota en 3D, foco por filas, contadores, kinetic type palabra a palabra y transiciones por transformación. El amarillo `#FFD500` va **solo en detalles** (punto, subrayado, chip, línea de match, CTA), nunca en grandes bloques. Tipografía: Manrope. |
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

Los tiempos son provisionales: cuando tenga la toma elegida, **re-temporizo la imagen a la voz**. Cada beat lleva la etiqueta de sección del kit (`01 · CAPTACIÓN`, `02 · PANEL`…) en Manrope 700 con tracking amplio, y el contador `01 / 06`.

| Tiempo | Beat | Escenario | Imagen / motion | Movimiento propio |
|---|---|---|---|---|
| 0.00–0.60 | Hook | Claro `#F5F5F5` | La cuadrícula de 40 px aparece con una onda desde el centro. El cuadrado amarillo de la «i» del logo cae y late una vez. | **Pixel heartbeat**: el cuadrado de la «i» es el hilo conductor |
| 0.60–3.30 | 1 · Captación | Claro | Tres chips de origen del kit (Portales, Campañas, Web) flotan a distintas profundidades. El que nombra la voz se enfoca. De cada uno salen mini tarjetas de lead hacia el centro, con la flecha amarilla del kit. | **Depth-pull** sincronizado con la palabra |
| 3.30–6.60 | 2 · Un solo panel + campañas | Claro, con panel oscuro | Las tarjetas aterrizan como filas en el **panel oscuro del kit** («Un panel para todo el equipo», con el punto amarillo). Al lado entra una tarjeta clara «Campañas» con una curva que se dibuja y un contador de leads por campaña. | **Stack-land** + **curve draw** |
| 6.60–10.00 | 3 · Match con IA | **Oscuro** (beat de alternancia) | El panel crece hasta llenar el plano. Etiqueta amarilla del kit «MATCH CON IA». Kinetic type «zona · tipo · presupuesto», con la palabra que suena subrayada en amarillo. Cada palabra gira como un dial y encaja en una tarjeta de inmueble abstracta (pin sobre mapa de líneas, icono de tipo, barra de presupuesto). | **Combination-dial** |
| 10.00–12.80 | 4 · Reactivar | Oscuro | El cuadrado amarillo se estira hasta formar la notificación «Match · 3 clientes encajan con Ático en Chamberí». La fila de un lead dormido se enciende y un botón «Reactivar» (amarillo `#FFD500`, hover `#E6C000`) se pulsa con un micro-rebote. | **Pixel-stretch notification** + **wake pulse** |
| 12.80–16.30 | 5 · Operativa | Oscuro → claro | El escenario vuelve a claro con un barrido. Una agenda semanal en tarjeta clara se ensambla en 3D: los bloques de visita caen en sus huecos, aparecen chips de recordatorio y avatares de agentes con su insignia de rol. Órbita de cámara de 10°. | **Calendar cascade** + **orbit reveal** |
| 16.30–18.60 | 6 · Titular | Claro | Titular de la landing, palabra a palabra: «Todo conectado.» (700, `#0A0A0A`) / «De principio a fin.» (500 cursiva). Debajo, la línea amarilla del kit. | **Underline sweep** |
| 18.60–21.00 | Logo + CTA | Claro | El cuadrado amarillo vuela a su sitio como la «i» y completa el **logo horizontal del kit**. Debajo aparece `IMPERIOS.APP ↗`. Último acorde. | **Pixel-home**: la «i» vuelve a su sitio en el logo |

**Capa permanente:** cuadrícula de 40 px con deriva lenta, sombras suaves y profundidad de campo en lo que no habla, motion blur fuerte en cada movimiento y un dolly lento continuo. En el beat oscuro, el círculo amarillo tenue de las plantillas del kit deriva en una esquina.
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
| Barrido oscuro → claro / pixel-home | `whoosh_low_wipe` |
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
| Escenario casi negro con **un único brillo verde** de marca, difuso, desde abajo o el centro | **No se copia.** ImperiOS es claro (`#F5F5F5`), con un único beat oscuro y el amarillo solo en detalles |
| **Logo al principio** (icono → wordmark) y al final | Solo al final. Al principio va el cuadrado de la «i» como semilla |
| **UI recreada flotando en 3D** (lista de productos, Live View con tarjetas y contadores) | Lista de leads, tarjeta de campañas, tarjeta de inmueble, agenda |
| **Rack focus por filas**: una fila nítida y elevada, el resto desenfocado | Depth-pull en las fuentes y foco en la fila del lead que se reactiva |
| Contadores que suben ($0.00 → valor) y tarjetas que entran escalonadas | Contador de leads por campaña y bloques de agenda en cascada |
| **Kinetic type centrado, pequeño, palabra a palabra**, con la palabra clave en color y subrayada | Mismo principio con Manrope 700/500 y amarillo |
| Pastilla con contorno brillante → **notificación** («Order #1001») | La notificación nace del cuadrado amarillo (pixel-stretch), no de una pastilla |
| Punto de luz → icono → wordmark, y fundido a negro | El cuadrado amarillo vuelve a su sitio como la «i» del logo horizontal, más `IMPERIOS.APP ↗` |
| Ritmo: ~20 s, un plano nuevo cada 1,5–3 s y casi sin cortes secos (todo es transformación) | Igual: transiciones por transformación, sin cortes secos |

## 11. Branding ImperiOS aplicado (fuente: kit generado desde la landing de imperios.app)

| Elemento de la web / kit | Uso en el anuncio |
|---|---|
| Fondo `#F5F5F5` + cuadrícula sutil de 40 px | Escenario base |
| Tarjetas `#FAFAFA` con borde fino, radios 10–24 px | Tarjetas de campañas, inmueble y agenda |
| Panel oscuro `#0A0A0A` / `#1C1C1C`, texto blanco | Panel de leads y beat del Match con IA |
| Amarillo `#FFD500` solo en detalles | Punto, flecha, subrayado, etiqueta «MATCH CON IA», botón «Reactivar», CTA |
| Manrope 700 en titulares, 500 cursiva para el énfasis, −0.035em | Todo el kinetic type |
| Etiquetas en mayúsculas con tracking amplio + numeración `01 / 06` | Etiqueta de sección y contador por beat |
| Titular de Producto «Todo conectado. / De principio a fin.» | Cierre |
| Logo horizontal del kit sobre claro (sin deformar) | Logo final |
| `IMPERIOS.APP ↗` | CTA final |

**No he podido abrir imperios.app desde esta sesión** (la red del entorno lo bloquea). El branding sale del kit, que según su README se generó desde la landing real (`src/styles/global.css` y `public/logo-imperios*`). Si en la web hay algo más que deba aparecer (ilustraciones, iconos, otra sección o un CTA distinto), mándame capturas o añade `imperios.app` a *Allowed domains* junto con `api.elevenlabs.io`.
