# ImperiOS — Spec Ad v6 · Brief (PASO 1)

> Estado: **BORRADOR, pendiente de tu OK.** No se ha construido nada, no se ha descargado nada y no se han gastado créditos.
> Fuente de marca: `assets_in/brand-kit/` (copia del ImperiOS-social-kit que me pasaste).

---

## 0. Conflictos que necesito que resuelvas (las demás decisiones las tomo yo)

| # | Conflicto | Mi propuesta |
|---|---|---|
| 1 | Las reglas fijas piden **escenario oscuro + SF Pro Display**. El brief de ImperiOS pide **blanco cálido + #0A0A0A + amarillo + Manrope**. | Manda la marca: **Manrope** y escenario **blanco cálido**. Uso paneles negros `#0A0A0A` como "segundo escenario" en 2 beats, para conservar el contraste Apple/Spotify. |
| 2 | Amarillo: tú dices **`#FEBE08`**. El kit y la web usan **`#FFD500`**, y la «i» del logo del kit está en `#FFD500`. | Usar `#FFD500` en todo para que coincida con el logo. Si prefieres `#FEBE08`, recoloreo la «i» del SVG para que no queden dos amarillos en pantalla. **¿Cuál?** |
| 3 | La regla fija pide la **PREVIEW v1 en 16:9**, pero esto es un **Reel 9:16**. | PREVIEW v1 en **9:16**. El 16:9 se monta como adaptación en el paso de finales. |
| 4 | End card "made by / **riccardo bosso**" (Spotify end card v2). Tú firmas como Brian Torre. | ¿Uso el mismo end card animado con **tu nombre**, mantengo "riccardo bosso" o lo omito en esta pieza de marca? |
| 5 | Voces **Jessica / Lauren / Siren**: son voces de ElevenLabs pensadas para inglés. El guion está en **español de España**. | En el paso 3 te enseño 3 opciones: 1 de esas voces con `eleven_multilingual_v2` y 2 voces nativas de España. |
| 6 | "Producto real", pero también "**no enseñar el CRM real**". | No uso capturas. El producto aparece como **UI abstracta hecha con los componentes del kit** (tarjeta de lead, chip de origen, panel oscuro). Solo muestro textos que dice la voz o nombres reales de funciones. Sin datos inventados. |
| 7 | La biblioteca de SFX (`/Volumes/Extreme Pro/...`) y ElevenLabs **no son accesibles desde esta sesión en la nube**. | Cuando des el OK: copia ~40 SFX del pack (whooshes, hits, clicks de UI, risers, stings) a `assets_in/sfx/` en el repo y añade la API key de ElevenLabs como secreto del entorno. Si no, genero la VO y mezclo en tu Mac. |
| 8 | "Animaciones nuevas cada vez": no tengo el v5 (`premium-v5/...mp4`) en este repo. | Súbelo o lístame sus movimientos para no repetirlos. Los movimientos de abajo se diseñaron sin verlo. |

---

## 1. Concepto — 3 ideas (recomiendo la A)

**A · "Todo llega al mismo sitio" (recomendada)**
Los leads entran desde los bordes del encuadre: portales, campañas y web. Un campo magnético los atrae hacia un único panel. La IA traza una línea amarilla entre cada cliente y su inmueble. Después la operativa (visitas, agentes, seguimiento) se acopla al panel como módulos que encajan. Cierre con logo. Es la más directa y cubre en orden los 3 mensajes: captación → match con IA → operativa centralizada.

**B · "Un día en un panel"**
Un reloj tipográfico avanza de 9:00 a 19:00 y cada hora el panel resuelve una tarea: llega un lead, la IA hace el match, se agenda una visita, se asigna un agente. Narrativa más humana, pero más larga y con más texto en pantalla.

**C · "Del ruido a la señal"**
Arranca con un caos de notificaciones, pestañas y bandejas (abstractas, sin marcas) que colapsa en una sola línea amarilla limpia. Esa línea es el panel de ImperiOS. Muy visual, pero dedica 4–5 s al "problema" y deja menos tiempo para el producto.

---

## 2. Guion (concepto A · español de España · ~18 s + end card)

Son frases completas y cortas, pensadas para entenderse en el altavoz de un móvil. Son 46 palabras, a ~2,6 palabras/s.

| # | Locución | Texto en pantalla (kinetic type) |
|---|---|---|
| 1 | «Los contactos te llegan de portales, campañas y tu web.» | **Portales** · **Campañas** · **Web** |
| 2 | «Con ImperiOS, todos entran en un solo panel.» | Tus leads, *en un solo panel.* |
| 3 | «La inteligencia artificial une a cada cliente con el inmueble que encaja.» | **Match con IA** |
| 4 | «Visitas, agentes y seguimiento: todo en el mismo sitio.» | **Visitas** · **Agentes** · **Seguimiento** |
| 5 | «ImperiOS. Todo conectado, de principio a fin.» | **Todo conectado.** *De principio a fin.* + logo |

- El titular del cierre es el de la landing («Todo conectado. / De principio a fin.»: 700 normal + 500 cursiva, −0.035em), tal como figura en el kit.
- **Hechos a confirmar por ti** (no he podido abrir imperios.app desde aquí): que Match con IA cruza **cliente ↔ inmueble**, y que visitas, agentes y seguimiento son funciones actuales. El kit los menciona como series sugeridas («Qué hace el Match con IA», «Así avanza una visita», «Qué puede ver cada agente»).
- Fuera del guion, según el kit: cifras de resultados (6×, 80 %, 30 s, 60 %) y el testimonio de Magnus.
- Fonética para ElevenLabs: «ImperiOS» → **«Impérios»**. ¿Se dice así o «Imperi-O-Ese»? Confírmalo.

---

## 3. Beat sheet (60 fps · 9:16 maestro 1080×1920 · adaptación 16:9 1920×1080)

Los tiempos son provisionales. Cuando elijas la toma, **re-temporizo la imagen a la voz**.

| Tiempo | Beat | Imagen / motion | Movimiento nuevo |
|---|---|---|---|
| 0.00–0.40 | Hook | Blanco cálido `#FAF8F4` con la cuadrícula de 40 px del kit, que se "enciende" desde el centro. Un punto amarillo cae y rebota una vez. | **Grid ignition** (la cuadrícula se revela en onda radial) |
| 0.40–3.60 | 1 · Captación | Tres chips de origen (estilo `origen-lead.svg`) entran desde 3 bordes distintos con mucho motion blur. Cada palabra de la VO cae como kinetic type con máscara vertical. | **Edge-slingshot**: cada chip entra con overshoot y estela |
| 3.60–6.60 | 2 · Un solo panel | Los chips son atraídos por un campo magnético hacia un panel `#0A0A0A` que se despliega desde una línea. Se convierten en tarjetas de lead (nombre genérico desenfocado, sin datos falsos legibles). Brillo amarillo suave que deriva. | **Magnetic funnel** + **line-to-panel unfold** |
| 6.60–10.60 | 3 · Match con IA | Zoom a una tarjeta de lead. A su derecha aparece una tarjeta de inmueble con silueta de foto fotorreal desenfocada (opcional, ver assets). Una línea amarilla se dibuja entre ambas con partículas y las tarjetas hacen "snap" a la vez. Etiqueta amarilla «MATCH CON IA» (componente `etiqueta.svg`). | **Bezier draw + dual snap**; flash de brillo en el contacto |
| 10.60–14.20 | 4 · Operativa | Cámara hacia atrás: el panel queda en el centro y 3 módulos (Visitas, Agentes, Seguimiento) se acoplan por sus lados como piezas magnéticas. Cada acople lleva un micro-pulso amarillo. | **Dock & lock**: los módulos rotan 8° y encajan |
| 14.20–18.00 | 5 · Cierre | Todo colapsa a un punto amarillo que se expande y revela el titular de la landing en dos líneas (700 / 500 cursiva) y el logo del kit (`logo-imperios-navbar.svg`) sobre fondo claro. Debajo, `IMPERIOS.APP`. | **Dot-iris reveal** + type tracking-in |
| 18.00–20.00 | End card | End card animado (ver conflicto 4), con el último acorde sonando por debajo. | — |

**Capa de motion graphics fija** (para que nunca se quede quieto): brillo amarillo difuso a la deriva (10–14 % de opacidad), partículas de polvo muy finas, contador de sección `01 / 05` que avanza por beat (patrón del kit) y una línea guía de 2 px que conecta todos los beats.
**Zona segura Reels**: el contenido clave queda dentro de 1080×1420 centrado, lejos de los 250 px superiores y los 420 px inferiores.

---

## 4. Voz (ElevenLabs)

- Modelo: `eleven_multilingual_v2`, español de España. Tono cercano, seguro y sin "voz de anuncio".
- **2 tomas en una sola llamada** por voz candidata.
- **Estimación de créditos**: el guion tiene ~300 caracteres. 2 tomas × 3 voces candidatas = ~1.800 créditos. Si eliges directamente una voz: ~600.
- Sin efectos de voz. Si hace falta, solo de-ess suave y EQ.

## 5. Música (hecha en código)

- Original, ~100 BPM, Re mayor/Si menor, con pulso tipo "SaaS limpio": pluck con sidechain, pad cálido, sub suave y kick muy ligero que entra en el beat 2.
- Arreglada alrededor de la voz: **≥15 dB por debajo de la VO** mientras habla (automatización por palabra, no compresor). Sin limitador sobre la voz.
- Hueco de 300 ms antes de «ImperiOS» en el beat 5 → acorde final abierto que **suena bajo el end card** hasta el final.

## 6. Plan de SFX (solo de tu biblioteca FOUR Editors)

| Momento | Categoría |
|---|---|
| Entrada de cada palabra/título | whoosh corto (EQ: HPF 300 Hz, por debajo de la voz) |
| Cada aterrizaje de chip/tarjeta | hit suave / thud de UI |
| Grid ignition (0.0 s) | riser corto + shimmer |
| Magnetic funnel | swoosh doble + "suck" invertido |
| Match con IA | línea: tick granular; snap: hit metálico + glitch fino |
| Dock & lock (×3) | click mecánico + pop, en estéreo izq./dcha./centro |
| Dot-iris + logo | sub-drop + sting/impact de logo |
| End card | whoosh de salida suave |

Colocados y ecualizados, nunca eliminados. Master final a **−14 LUFS / −1 dBTP**.

## 7. Lista de assets (no descargo nada sin tu OK)

| Asset | Fuente | Licencia | Estado |
|---|---|---|---|
| Logo ImperiOS (horizontal + icono, SVG/PNG) | Kit de marca (`assets_in/brand-kit/assets/`) | Propiedad de ImperiOS | ✅ copiado |
| Manrope Variable (woff2) | Kit de marca | SIL OFL 1.1 | ✅ copiado |
| Componentes UI (etiqueta, origen-lead, panel-oscuro) | Kit de marca | Propiedad de ImperiOS | ✅ copiado |
| 1–2 fotos de interior de vivienda (tarjeta de inmueble, beat 3) | Unsplash/Pexels, **opcional** | Unsplash/Pexels License | ⏳ te pido permiso con los enlaces |
| SFX | FOUR Editors Sound Effects | Tu licencia | ⏳ falta copiarlos (conflicto 7) |
| VO | ElevenLabs | Tu plan | ⏳ paso 3 |
| Música | Generada en código | Original | ⏳ |

Todo quedará registrado en `assets_in/CREDITS.md`.

## 8. Entregables

1. PREVIEW v1 9:16 + contact sheet → iteramos.
2. Finales: 9:16 1080×1920 y 16:9 1920×1080 a 60 fps, H.264 alta calidad + ProRes 422 HQ, stems (VO / música / SFX), README.
3. Solo si lo pides: proyecto completo de DaVinci Resolve.

---

**Siguiente paso:** con tu OK al concepto, el guion y los 8 puntos de la sección 0, preparo la lista definitiva de assets para tu aprobación.
