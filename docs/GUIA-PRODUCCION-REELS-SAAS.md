# Guía de producción: Reels SaaS con motion graphics hechos en código

> Documento técnico y de proceso, paso a paso, de cómo se produjo el spec ad / campaña de **ImperiOS** (CRM inmobiliario) en octubre de 2026.
> Está escrito para que **otra persona u otra IA** pueda reproducir vídeos del mismo estilo en otro proyecto sin haber visto la conversación original.
> Todo lo descrito existe en este repo, en `ADV/ImperiOS Ad/`.
> **Nota 21/10/2026:** los vídeos v2/v3/v6 y las voces sin licencia comercial se borraron del repo (sus hojas de contacto
> están en `ADV/ImperiOS Ad/referencia-versiones-anteriores/`). Los comandos que citan `assets_in/vo/campana-toma-*` o
> `out/campaign*` sirven como receta, pero esos archivos ya no existen. Versión vigente: campaña v4 (`campaign/CAMPANA.md`).

---

## Índice

0. [Qué se consigue con este método](#0-qué-se-consigue-con-este-método)
1. [Visión general del pipeline](#1-visión-general-del-pipeline)
2. [Herramientas, versiones e instalación](#2-herramientas-versiones-e-instalación)
3. [Estructura de carpetas](#3-estructura-de-carpetas)
4. [Fase 1 — Brief](#4-fase-1--brief)
5. [Fase 2 — Kit de marca](#5-fase-2--kit-de-marca)
6. [Fase 3 — Análisis del vídeo de referencia](#6-fase-3--análisis-del-vídeo-de-referencia)
7. [Fase 4 — Storyboard](#7-fase-4--storyboard)
8. [Fase 5 — Motor de animación (`reel.html`)](#8-fase-5--motor-de-animación-reelhtml)
9. [Fase 6 — Render a vídeo (`render.js`)](#9-fase-6--render-a-vídeo-renderjs)
10. [Fase 7 — Efectos de sonido sintetizados](#10-fase-7--efectos-de-sonido-sintetizados)
11. [Fase 8 — Música original en código](#11-fase-8--música-original-en-código)
12. [Fase 9 — Voz con ElevenLabs](#12-fase-9--voz-con-elevenlabs)
13. [Fase 10 — Sincronizar la imagen a la voz](#13-fase-10--sincronizar-la-imagen-a-la-voz)
14. [Fase 11 — Mezcla y máster](#14-fase-11--mezcla-y-máster)
15. [Fase 12 — Versiones de campaña (ganchos A/B/C, CTA, corte corto)](#15-fase-12--versiones-de-campaña)
16. [Control de calidad (QA)](#16-control-de-calidad-qa)
17. [Problemas reales encontrados y su solución](#17-problemas-reales-encontrados-y-su-solución)
18. [Cómo reutilizarlo en otro proyecto](#18-cómo-reutilizarlo-en-otro-proyecto)
19. [Prompt plantilla para otra IA](#19-prompt-plantilla-para-otra-ia)
20. [Costes y tiempos reales](#20-costes-y-tiempos-reales)
21. [Inventario de archivos](#21-inventario-de-archivos)
22. [Chuleta de comandos](#22-chuleta-de-comandos)

---

## 0. Qué se consigue con este método

- Reel **9:16, 1080×1920, 60 fps**, de 21–28 s, con estética SaaS: UI recreada flotando en 3D, kinetic type palabra a palabra, foco por filas, contadores, transiciones por transformación y sin cortes secos.
- **Todo generado por código**: la imagen es una página HTML/CSS/JS que se fotografía fotograma a fotograma; la música y los efectos se sintetizan en Python. Solo la voz viene de un servicio externo (ElevenLabs).
- **Motion blur real**, por submuestreo temporal: se renderizan 3 subfotogramas por fotograma y se promedian.
- **La imagen se re-temporiza a la voz**, no al revés: cada palabra en pantalla aparece cuando se pronuncia, según los tiempos por palabra de una transcripción.
- **Audio a estándar de plataforma**: −14 LUFS integrados y pico ≤ −1 dBTP, con la música ≥15 dB por debajo de la voz mientras habla y sin aplastar la voz con el limitador.
- **Versiones de campaña** desde el mismo motor: 3 ganchos para test A/B, llamada a la acción (CTA) final y un corte corto.

Resultado de este proyecto: `ADV/ImperiOS Ad/preview/out/` (los `.mp4` y los contact sheets).

---

## 1. Visión general del pipeline

```
 BRIEF ──► KIT DE MARCA ──► ANÁLISIS DE REFERENCIA ──► STORYBOARD (HTML estático, 8 fotogramas)
                                                             │
                                                             ▼
                                   MOTOR DE ANIMACIÓN  reel.html  (render(t) = función pura del tiempo)
                                                             │
     timeline.json (beats + tiempos de palabra) ────────────┤
                                                             ▼
                          render.js: Chromium headless → JPEG por subfotograma → ffmpeg (tmix → 60 fps, x264)
                                                             │  vídeo mudo
 GUION ──► ElevenLabs (TTS, 2 tomas) ──► Scribe (tiempos por palabra) ──► build_timeline_vo.py ──┘
                 │
                 ▼
   VO procesada (HPF + compresor 3:1) ─┐
   sfx_synth.py → 29 SFX ──► cues ─────┼──► audio_mix.py (música en código + SFX + ducking) ──► master_vo.sh (−14 LUFS / −1 dBTP)
   música sintetizada ─────────────────┘                                                              │
                                                                                                      ▼
                                                             ffmpeg mux vídeo + audio ──► MP4 final + contact sheet
```

Orden de trabajo que se siguió, con validación del usuario en cada paso:

1. Brief → OK del usuario (5 revisiones: r1…r5).
2. Lista de assets → OK antes de descargar nada.
3. Storyboard estático → OK del estilo.
4. PREVIEW v1 sin voz (tiempos provisionales), con música y SFX.
5. Versión de campaña: gancho, 3 variantes, CTA y corte corto.
6. Voz → el usuario elige voz y toma → re-temporizado a la voz → mezcla final.
7. Variantes B/C con voz y corte corto con voz.

---

## 2. Herramientas, versiones e instalación

### 2.1 Software (versiones exactas usadas)

| Herramienta | Versión | Para qué |
|---|---|---|
| Node.js | 22.22.0 | Ejecutar `render.js` |
| `playwright-core` (npm) | 1.56.1 | Controlar Chromium sin interfaz |
| Chromium | build 1194 (el de Playwright) | Renderizar `reel.html` fotograma a fotograma |
| ffmpeg | 6.1.1 | Codificar vídeo, `tmix` (motion blur), mezcla, medición EBU R128, loudness, contact sheets |
| Python | 3.13 | SFX, música, mezcla, timelines |
| numpy / scipy | 2.5.3 / 1.18.1 | Síntesis y DSP |
| Fuente | Manrope Variable (woff2, OFL 1.1) | Tipografía de la marca |

No se usaron After Effects, DaVinci ni bibliotecas de stock. Todo es código y ffmpeg.

### 2.2 Instalación

```bash
cd "ADV/ImperiOS Ad/preview"
npm install                       # instala playwright-core 1.56.1 (package.json)
pip install -r requirements.txt   # numpy + scipy
# Chromium: render.js busca, por orden:
#   1) $CHROMIUM_PATH  (cualquier Chrome/Chromium instalado)
#   2) /opt/pw-browsers/chromium-1194/chrome-linux/chrome  (contenedor de Claude Code)
#   3) el Chromium por defecto de Playwright (npx playwright install chromium)
export CHROMIUM_PATH="/ruta/a/chrome"   # en macOS p. ej. "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### 2.3 Servicios externos

| Servicio | Uso | Cómo se conectó |
|---|---|---|
| **ElevenLabs** | TTS (voz) y Scribe (transcripción con tiempos por palabra) | **Conector MCP de ElevenLabs** en Claude (herramientas `creative_list_voices`, `creative_generate_speech`, `creative_get_flow_run_status`, `creative_add_flow_asset_node`, `creative_transcribe_audio`). Alternativa sin MCP: `tools/vo_generate.py` con la API REST y `ELEVENLABS_API_KEY`. |
| **GitHub** | Guardar el trabajo | Conectar GitHub en claude.ai para poder hacer `git push` desde la sesión en la nube. |

### 2.4 Restricciones de una sesión en la nube (Claude Code web)

- La **red sale por un proxy con lista blanca**: `api.elevenlabs.io`, `imperios.app`, `instagram.com` y HuggingFace estaban **bloqueados**. Por eso:
  - el reel de referencia lo descargó el usuario y lo subió;
  - la web de la marca no se pudo abrir y se usó el kit de marca, generado desde la landing;
  - no se pudo transcribir con Whisper local; los modelos no se pueden descargar. Para la transcripción se usó Scribe de ElevenLabs vía MCP.
- Sin conectar GitHub, `git push` devuelve **403**: se trabaja en commits locales hasta conectarlo.
- `sleep` largos en primer plano están bloqueados: los renders largos se lanzan en segundo plano y se espera con un `until …; do sleep N; done` en segundo plano.

---

## 3. Estructura de carpetas

```
ADV/ImperiOS Ad/
├── HANDOFF.md                  # estado y siguiente paso (para retomar en otra sesión)
├── brief/
│   ├── PROMPT.md               # brief r5 (concepto, guion, beat sheet, voz, música, SFX, assets)
│   ├── VO_SCRIPT.txt           # guion de la versión sin gancho
│   └── ref/referencia-shopify-contact-sheet.png
├── campaign/
│   ├── CAMPANA.md              # piezas, montaje del test A/B en Meta, textos del anuncio
│   └── VO_SCRIPT_campana_A.txt
├── assets_in/
│   ├── CREDITS.md              # procedencia y licencia de cada asset
│   ├── brand-kit/              # kit de marca entregado por el cliente (tokens, logo, Manrope)
│   ├── sfx/                    # 29 SFX sintetizados + INDEX.md + _preview_all.mp3
│   └── vo/                     # tomas de voz (mp3) + tiempos por palabra (*.words.json)
├── tools/
│   ├── sfx_synth.py            # sintetizador de la biblioteca de SFX
│   └── vo_generate.py          # alternativa: TTS por API REST (sin MCP)
├── storyboard/
│   ├── storyboard.html         # 8 fotogramas clave estáticos
│   └── storyboard-contact-sheet.png
└── preview/
    ├── src/
    │   ├── reel.html           # MOTOR DE ANIMACIÓN
    │   ├── logo-noaccent.svg   # logo sin la «i» amarilla (para el «pixel-home»)
    │   └── manrope-latin-variable.woff2
    ├── render.js               # render fotograma a fotograma + motion blur
    ├── package.json / requirements.txt
    ├── timeline*.json          # beats y tiempos de palabra por versión
    ├── build_timeline_vo.py    # tiempos de palabra → timeline sincronizado
    ├── audio_mix.py            # música + colocación de SFX + ducking con VO
    ├── master.sh / master_vo.sh
    ├── build_campaign.sh       # campaña sin voz (A completo + ganchos B/C empalmados + corte)
    ├── build_vo_version.sh     # una versión con una VO concreta (todo el pipeline)
    ├── build_cut10.sh          # corte corto con voz
    ├── finish.sh               # mux + contact sheet de la preview v1
    └── out/                    # entregables (mp4, contact sheets, stems)
```

---

## 4. Fase 1 — Brief

### 4.1 Entradas que se pidieron al cliente

- Marca y producto; kit de marca (logo, colores, tipografía).
- Vídeo de referencia de estilo.
- Mensaje o idea (aquí: «captación, match con IA y toda la operativa centralizada»).
- Guion (propio o redactado por la IA), voz y duración.
- Qué evitar (aquí: no enseñar el CRM real, no usar etiquetas de relleno).

### 4.2 Contenido del brief (`brief/PROMPT.md`)

1. **Decisiones cerradas**: una tabla con estética, color, formato, CTA, voz, SFX, fotos y UI.
2. **Concepto**: se propusieron 3 ideas y se eligió una («Todo llega al mismo sitio»).
3. **Guion**: una tabla con columnas *locución · texto en pantalla · dato que lo respalda*. Cada frase lleva un dato confirmado por el cliente, sin cifras inventadas.
4. **Beat sheet**: tiempo, beat, escenario, imagen/motion y nombre del movimiento.
5. **Voz**: proveedor, voz, modelo, ajustes y créditos estimados.
6. **Música**: tempo, tonalidad, capas y relación con la voz.
7. **Plan de SFX**: momento → archivo de SFX.
8. **Assets**: fuente, licencia y estado de cada uno.
9. **Entregables.**

### 4.3 Conflictos que conviene detectar y preguntar en el primer brief

Hubo conflictos reales entre las «reglas fijas» del usuario y la marca. Se resolvieron preguntando una sola vez y en tabla:

| Conflicto | Resolución |
|---|---|
| Reglas: «escenario oscuro + SF Pro» vs. marca: «blanco cálido + Manrope» | **Manda la marca**. Escenario claro `#F5F5F5`, un tramo oscuro de alternancia y Manrope. |
| Amarillo `#FEBE08` (usuario) vs. `#FFD500` (kit, web y logo) | `#FFD500`, para que coincida con la «i» del logo. |
| PREVIEW en 16:9 vs. pieza Reel | Preview directamente en 9:16. |
| End card de otro autor («riccardo bosso», en la referencia) | Se quitó: la pieza es de la marca. |
| Voces en inglés para un guion en español | Voz nativa española (Cristina, PVC). |
| «Producto real» vs. «no enseñar el CRM real» | **UI recreada** con los componentes del kit y datos de ejemplo genéricos (iniciales, zonas de Madrid, rangos de precio). Nunca cifras de resultados. |
| SFX de una biblioteca en un SSD local (inaccesible desde la nube) | SFX **sintetizados en código**, a petición del usuario. |

### 4.4 Reglas de guion que funcionaron

- Frases completas, cortas y entendibles en el altavoz de un móvil. Unas 2,6–2,8 palabras por segundo.
- **Respelling** para el TTS: la marca «ImperiOS» se escribe **«Imperios»** en el texto de la voz, para que se pronuncie como la palabra española; en pantalla se mantiene el logo o «ImperiOS».
- Cada claim, respaldado por un dato del cliente. Prohibido publicar cifras o testimonios sin fuente.

### 4.5 Lección clave de la iteración del brief (r4 → r5)

Al analizar la referencia (Shopify, fondo negro con brillo verde) se copió primero su **look**. El usuario corrigió: «hay que adaptarlo al branding de mi marca». La regla resultante es:

> **De la referencia se toma solo la gramática de movimiento. La superficie (colores, tipografía, componentes, logo) sale siempre del kit de marca.**

---

## 5. Fase 2 — Kit de marca

El cliente entregó un ZIP (`ImperiOS-social-kit`) con `tokens.json`, `tipografia.css`, componentes SVG, plantillas, logo SVG/PNG y Manrope. Se copió a `assets_in/brand-kit/`.

Tokens usados en todo el motor:

```css
--ink-950:#0A0A0A; --ink-900:#1C1C1C; --ink-800:#333; --ink-700:#4A4A4A; --ink-600:#727272;
--ink-500:#B0B0B0; --ink-400:#C0C0C0; --ink-300:#D4D4D4; --ink-200:#EBEBEB; --ink-100:#F5F5F5; --ink-50:#FAFAFA;
--y:#FFD500;  /* acento, solo en detalles; hover #E6C000 */
```

Reglas de marca aplicadas, sacadas del README del kit:

- Fondo claro `#F5F5F5` con **cuadrícula de 40 px**; tarjetas `#FAFAFA` con borde de 1,5 px y radios de 10–28 px; paneles oscuros `#0A0A0A`.
- Amarillo **solo en detalles**: punto, subrayado, chip, línea de match, botón CTA. Nunca en bloques grandes.
- Manrope 700 para titulares y 500 cursiva para el énfasis, con tracking −0.035em.
- Etiquetas en mayúsculas con tracking amplio y numeración `01 / 06`.
- El logo horizontal va sobre fondo claro y no se deforma.

**Variante del logo sin acento** (`preview/src/logo-noaccent.svg`). El SVG del kit tiene dos grupos: el logo recortado sin la «i» (`clip-path="url(#rest)"`) y la «i» recoloreada en amarillo (`clip-path="url(#accent)"`, rectángulo `x=107 y=40 w=57 h=64` en un viewBox de `1280×410`). Se eliminó el segundo grupo para que el cuadrado amarillo animado «aterrice» en esa posición exacta:

```python
s = open("assets_in/brand-kit/assets/logo-imperios-navbar.svg").read()
i = s.index('<g clip-path="url(#accent)"'); j = s.index('</g>', i) + 4
open("preview/src/logo-noaccent.svg", "w").write(s[:i] + s[j:])
```

---

## 6. Fase 3 — Análisis del vídeo de referencia

El reel de Instagram no se podía abrir desde la nube, así que el usuario subió una grabación de pantalla de 37 s (1290×2796 a 60 fps). El análisis se hizo con ffmpeg:

```bash
# 1) Ficha técnica
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate ref.mp4
# 2) Detección de cortes de escena
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -oE "pts_time:[0-9.]+"
# 3) Contact sheet general (1 fotograma cada 1,5 s)
ffmpeg -i ref.mp4 -vf "fps=1/1.5,scale=258:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=16:fontcolor=red:box=1:boxcolor=white" -frames:v 26 f_%02d.png
ffmpeg -framerate 1 -i f_%02d.png -vf "tile=9x3:padding=4:color=gray" -frames:v 1 sheet.png
# 4) Recorte de la zona del anuncio (el monitor dentro de la grabación), 2 fps
ffmpeg -i ref.mp4 -t 21.5 -vf "fps=2,crop=1000:520:145:1130,scale=330:-1" c_%02d.png
ffmpeg -framerate 1 -i c_%02d.png -vf "tile=6x7:padding=3:color=white" -frames:v 1 crop_sheet.png
```

Gramática de movimiento extraída, la parte que **sí** se adopta:

| Rasgo | Aplicación |
|---|---|
| UI recreada flotando en 3D (perspective, rotateX/Y) | Lista de leads, tarjeta de campañas, tarjeta de inmueble, agenda |
| Foco por filas: una nítida y elevada, el resto desenfocado | Depth-pull en las fuentes; fila del lead que se reactiva |
| Contadores que suben y tarjetas que entran escalonadas | Contador «24 leads», bloques de agenda en cascada |
| Kinetic type centrado, palabra a palabra, con la palabra clave en color | Manrope y subrayado amarillo que viaja de palabra en palabra |
| Transiciones por transformación, sin cortes secos | Barridos circulares (clip-path) y elementos que se convierten en otros |
| ~20 s, un plano nuevo cada 1,5–3 s | Beats de unos 3 s |

Lo que **no** se copia: fondo negro con brillo de color grande, pastilla que pasa a notificación, punto que pasa a icono y wordmark. Se sustituyen por movimientos propios (sección 8.6).

---

## 7. Fase 4 — Storyboard

`storyboard/storyboard.html`: **8 secciones `<section class="f">` de 1080×1920**, estáticas, una por beat, con el CSS de marca. Sirve para aprobar el look antes de animar. Se fotografía cada sección con Playwright y se monta un contact sheet:

```js
// shot.js
const { chromium } = require('playwright-core');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  for (let i = 1; i <= 8; i++) await (await p.$('#f' + i)).screenshot({ path: `${out}/frame_${i}.png` });
  await b.close();
})();
```

```bash
ffmpeg -y -i frame_%d.png -vf "scale=360:-1,pad=iw+12:ih+12:6:6:color=0x0A0A0A,tile=4x2" -frames:v 1 storyboard-contact-sheet.png
```

Lecciones del storyboard:

- Para subrayar texto que puede partirse en varias líneas, usa `text-decoration` (`text-decoration-color`, `-thickness: 8px`, `text-underline-offset: 14px`, `text-decoration-skip-ink: none`), **no** un `::after` absoluto: el `::after` se rompe al cambiar de línea.
- Con `line-height` de 1,06 el subrayado pisa la línea siguiente. Usa 1,16.
- Ajusta el tamaño de los titulares para que no quede una palabra sola en la última línea. Por ejemplo, 100 px en lugar de 118 px para «Todo conectado.»

---

## 8. Fase 5 — Motor de animación (`reel.html`)

### 8.1 Principio fundamental

**`render(t)` es una función pura del tiempo.** Recibe `t` en segundos y deja el DOM exactamente como debe verse en ese instante, sin estado acumulado. Gracias a eso:

- se puede renderizar cualquier instante suelto (`stills`) para revisar sin generar el vídeo;
- se pueden renderizar subfotogramas (para el motion blur) y tramos parciales (para empalmar variantes);
- re-temporizar es solo cambiar números en un JSON.

API expuesta a `render.js`:

```js
window.ready        // Promise: fuentes cargadas + logo cargado
window.setBeats(b)  // fusiona el objeto beats del timeline.json en B
window.setVariant(v)// 'A' | 'B' | 'C' → reconstruye el texto del gancho
window.render(t)    // dibuja el instante t
```

### 8.2 Estructura del DOM (capas, de abajo arriba)

```
#stage (1080×1920, overflow hidden)
 ├── #lightbg   fondo claro + #lgrid (cuadrícula de 40 px) + #lglow (brillo amarillo radial) + viñeta
 ├── #dark      escenario oscuro completo; se revela con clip-path: circle(r at x y)
 │               └── #dgrid + #dglowA (círculo amarillo tenue a la deriva) + viñeta oscura
 ├── #scH       gancho de campaña (solo si B.hook > 0)
 ├── #sc0       hook del cuadrado (anillos)
 ├── #sc1…#sc6  escenas: captación, panel, match, reactivar, operativa, titular
 ├── #sc7       logo + CTA
 ├── #ul        subrayado amarillo compartido (viaja de palabra en palabra)
 └── #px        EL CUADRADO AMARILLO (hilo conductor, z-index 50)
```

Cada escena es un `div.scene` a pantalla completa. Su visibilidad se controla con `display` según `t` (cada escena se muestra solo entre su beat y un poco después del siguiente), y lleva un **dolly** sutil: `transform: scale(1 + .03 * progreso)`.

### 8.3 Utilidades de animación (copiables tal cual)

```js
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const E = {                             // curvas de easing
  lin: p => p,
  oc:  p => 1 - Math.pow(1 - p, 3),                 // ease-out cubic
  ic:  p => p * p * p,                              // ease-in cubic
  ioc: p => p < .5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2,
  oe:  p => p === 1 ? 1 : 1 - Math.pow(2, -10 * p), // ease-out expo
  ob:  p => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3*Math.pow(p-1,3) + c1*Math.pow(p-1,2); }, // back
  ob2: p => { const c1 = 2.4,     c3 = c1 + 1; return 1 + c3*Math.pow(p-1,3) + c1*Math.pow(p-1,2); }, // back fuerte (pops)
};
// progreso normalizado y con easing de t entre t0 y t1:
const k = (t, t0, t1, e = E.oc) => e(clamp((t - t0) / (t1 - t0)));
```

Patrón de cualquier animación: `const p = k(tLocal, inicio, fin, E.curva);` y después `opacity: p`, `transform: translateY(${(1-p)*N}px) scale(...)` y `filter: blur(${(1-p)*X}px)`. El **desenfoque proporcional a lo que falta** de la animación imita el desenfoque de cámara y de movimiento.

### 8.4 Kinetic type

```js
words(el, lineas)              // crea un <span class="w"> por palabra (inline-block, white-space: pre)
revealWords(ws, t, tiempos)    // cada palabra entra en .38 s: opacity 0→1, translateY 46→0 px, blur 10→0 px
exitBlock(el, t, t0, dur=.32)  // salida del bloque: sube 60 px, blur 0→14, opacity 1→0 (ease-in)
underlineTo(t, [[tiempo, palabra], …])  // el subrayado #ul crece (scaleX) bajo la 1.ª palabra
                                        // y se desliza (ease-in-out .35 s) a las siguientes; mide con getBoundingClientRect
```

Los **tiempos por palabra** de cada bloque viven en el timeline (`B.wt.kt2`, `B.wt.kt3`…), relativos al inicio de su escena. Si no hay voz, se usan los valores por defecto del objeto `DEF`. Ese es el gancho que permite sincronizar con la voz sin tocar el motor (sección 13).

### 8.5 Escenario oscuro con barrido circular

```js
// abre: círculo que crece desde el centro del panel (540,760) entre s3-.3 y s3+.35
// cierra: círculo que encoge hacia el botón «Reactivar» (860,1010) entre s5-.15 y s5+.45
$('#dark').style.clipPath = `circle(${radio}px at ${x}px ${y}px)`;
```

### 8.6 Movimientos propios (los «nombres» del beat sheet)

| Movimiento | Implementación |
|---|---|
| **Pixel heartbeat** | El cuadrado `#px` (60×68 px, `#FFD500`) cae (ease-in) o, en la campaña, aparece con *back*. Se aplasta al aterrizar (`scale(1+sq*.25, 1-sq*.2)`), late una vez y dos anillos se expanden con *ease-out expo*. |
| **Depth-pull** | Chips a distintas profundidades. El que nombra la voz pasa de `blur(6px)`/opacity .55 a nítido, escala ×1,14 y borde más marcado. |
| **Stack-land** | Las filas caen desde −60 px con *back* y un retardo de .09 s entre ellas. Cada fila tiene su blur base (`data-b`) para simular profundidad de campo. |
| **Line-to-panel unfold** | Panel con `rotateX(14°+(1-p)*30°) scaleY(.02→1)` desde una línea. |
| **Curve draw** | `stroke-dasharray/dashoffset` en un path SVG y un punto amarillo que aparece al final con *back*. |
| **Combination-dial** | Tres anillos que giran 220°→0° con *back* y se bloquean (borde amarillo y check dibujado con dashoffset) justo cuando la voz dice cada palabra. |
| **Pixel-stretch notification** | El cuadrado aparece y la notificación crece de 60 a 888 px de ancho con *ease-out expo*. Es amarilla mientras es estrecha y luego pasa a `#FAFAFA`. |
| **Wake pulse** | La fila dormida se enciende: borde amarillo, `box-shadow` con halo amarillo, avatar gris→amarillo y escala ×1,04. Después, botón con pop, pulsación (`1-.08*sin`) y onda (ripple). |
| **Calendar cascade + orbit** | Tarjeta de agenda con `rotateY` de −10° a −4° a lo largo de la escena (órbita lenta). Los bloques caen escalonados (.14 s) con blur de movimiento. |
| **Underline sweep** | El subrayado amarillo bajo «conectado.» |
| **Pixel-home** | El **subrayado se transforma en el cuadrado** y vuela en arco (`- sin(p·π)·120 px`) hasta el hueco exacto de la «i» del logo sin acento. Rebota y se revela el logo con `clip-path: inset(0 X% 0 0)` y blur. |
| **CTA** | El logo sube 230 px y escala ×0,88. El botón amarillo «Pide tu demo →» aparece con pop y un anillo de pulso cada 1,2 s; la flecha empuja. |

Detalle importante del **pixel-home**: el cuadrado vive fuera de `#sc7`, pero la escena del logo se transforma (dolly y subida del CTA). Para que aterrice exacto, el destino se calcula aplicando **la misma transformación** (`logoT(t)` devuelve `{s, dy}`, con origen en `540px 864px`):

```js
const LOGO = { x: 150 + 107*780/1280, y: 780 + 40*780/1280, w: 57*780/1280, h: 64*780/1280 };
const T = logoT(t), O = { x: 540, y: 864 };
const destino = { x: O.x + (LOGO.x-O.x)*T.s, y: O.y + (LOGO.y-O.y)*T.s + T.dy, w: LOGO.w*T.s, h: LOGO.h*T.s };
```

### 8.7 Capa permanente

- Deriva lenta de la cuadrícula: `background-position: ${-t*6}px ${-t*9}px`.
- Brillo amarillo radial que se mueve con senos y cosenos.
- HUD por escena: `01 · CAPTACIÓN` y `01 / 06`. En las escenas oscuras, el número va en amarillo.
- **Zona segura de Reels**: el contenido clave se mantiene entre y≈290 y y≈1600; el CTA, por encima de ~1300.

### 8.8 Gancho de campaña (`#scH`) y variantes

- Etiqueta oscura «CRM PARA INMOBILIARIAS», visible desde el fotograma 0.
- Pregunta grande (92 px), palabra a palabra. Las variantes están en el objeto `HOOKS`:
  - A: `¿Tus leads se pierden entre portales, WhatsApp y Excel?`
  - B: `¿Cuántos clientes se te escapan cada mes?`
  - C: `Toda tu inmobiliaria, en un solo panel.`
- Seis chips desordenados (Portales, WhatsApp, Excel, Email, Llamadas, Web) con badges, temblor (`sin(t*9+i)`) y profundidades distintas.
- En los últimos `B.hookCol` segundos (.55 por defecto; .32 con voz) **colapsan al centro** y aparece el cuadrado. El «caos al orden» enlaza con el cuerpo del anuncio.
- Con `B.hook > 0` todo el cuerpo se desplaza: el motor usa `th = t - B.hook` para el hook interno, y la cuadrícula no hace la «ignición».

### 8.9 Parámetros del timeline que entiende el motor

```jsonc
{
  "fps": 60, "duration": 28.2, "vo_offset": 0.2,
  "beats": {
    "hook": 3.86,   // fin del gancho de campaña / nacimiento del cuadrado (0 = sin gancho)
    "s1": 4.46, "s2": 5.0, "s3": 8.55, "s4": 12.95, "s5": 16.95, "s6": 21.55,  // inicio de cada escena
    "logo": 24.95,  // el subrayado vuela al logo
    "cta": 25.65,   // opcional: logo sube + botón CTA
    "end": 28.2,
    "hookCol": 0.32,   // duración del colapso del gancho
    "hideKt1": true,   // oculta el texto de captación (con voz no se dice)
    "wt": {            // tiempos de palabra por bloque (relativos a su escena; ktH absoluto)
      "ktH": [...], "kt2": [...], "kt3": [...], "kt3b": [...], "kt4": [...], "kt5": [...], "kt6": [...]
    }
  }
}
```

### 8.10 Cómo añadir o cambiar una escena

1. Añade su `<div class="scene" id="scN">` con el HTML de la UI (usa las clases `.card`, `.panel`, `.chip`, `.row`, `.av`, `.tag` y `.kt`).
2. Añade su beat en `B` y en el timeline JSON.
3. En `render(t)`: calcula `const sN = t - B.sN`, controla el `display` por rango, el dolly, la entrada y salida del HUD y cada elemento con `k()`.
4. Si tiene texto, crea `WN = words(...)` y añade sus tiempos en `DEF.ktN` y en `wt`.
5. Revisa con `stills` antes de lanzar el render completo.

---

## 9. Fase 6 — Render a vídeo (`render.js`)

### 9.1 Cómo funciona

1. Lanza Chromium sin interfaz con viewport 1080×1920 y abre `src/reel.html` (file://).
2. Espera `window.ready` e inyecta `setBeats(timeline.beats)` y `setVariant(VARIANT)`.
3. Para cada **subfotograma** `i` a `fps × sub` (60 × 3 = 180 por segundo): `render(i/fps)`, captura JPEG al 94 % y la escribe en el `stdin` de ffmpeg (`image2pipe`, respetando el back-pressure con `drain`).
4. ffmpeg: `tmix=frames=3:weights='1 1 1'` promedia cada 3 subfotogramas, que es el **motion blur** (obturador de 360°). Después `fps=60`, `libx264 -preset slow -crf 14 -pix_fmt yuv420p`.

```bash
TL=timeline-campaign-vo.json VARIANT=A node render.js video out/x.mp4 3        # completo
TL=timeline-campaign.json VARIANT=B node render.js video out/hookB.mp4 3 0 2.6  # solo 0–2,6 s
TL=timeline-campaign-vo.json node render.js stills /tmp/st 1.5 3.4 8.0 25.3     # PNG sueltos para revisar
```

### 9.2 Rendimiento observado

- Unos 8–9 fotogramas por segundo de captura: 21 s × 180 = 3780 subfotogramas → **~8,5 min**; 28 s → **~14 min**.
- No lances renders ni la síntesis de audio en paralelo con otro render: compiten por CPU y el progreso parece «parado».

### 9.3 Empalmar variantes sin re-renderizar todo (versión sin voz)

Si dos variantes solo difieren en el gancho y el resto es idéntico a partir de cierto instante, se renderiza la variante B solo en `0–2,6 s` y se concatena con A desde 2,6 s:

```bash
ffmpeg -i _B_hook.mp4 -ss 2.6 -i _A_silent.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 60 _B_silent.mp4
```

Con voz **no** vale: cada gancho dura distinto y desplaza todo el timeline, así que cada variante se renderiza completa.

### 9.4 Contact sheet (QA visual)

```bash
ffmpeg -i video.mp4 -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x3" -frames:v 1 contact.png
```

---

## 10. Fase 7 — Efectos de sonido sintetizados

`tools/sfx_synth.py` → 29 WAV estéreo de 48 kHz en float32, normalizados a −3 dBFS, más `INDEX.md` y `_preview_all.wav/mp3`. Semilla fija (`default_rng(6)`), así que es reproducible.

```bash
python3 tools/sfx_synth.py assets_in/sfx
```

| Generador | Técnica |
|---|---|
| `whoosh(dur, f0, f1, …)` | Ruido blanco filtrado con un **paso banda que barre** de f0 a f1 (48 bloques con crossfade), envolvente `sin(π·pos^0.7)^shape` y paneo dinámico |
| `ui_thud` | Seno con caída de pitch (`f·(1+1.6e^{-40t})`), click de ruido paso alto y reverb corta |
| `metal_hit` | Parciales inarmónicos (ratios 1, 2.76, 5.40, 8.93, 13.34) con decays distintos y reverb |
| `tick` / `mech_click` | Senos agudos con decay muy rápido; doble golpe a 22 ms y cuerpo grave para lo mecánico |
| `pop` | Seno con pitch descendente rápido |
| `riser` | Barrido de ruido 400→9000 Hz más tonos que suben dos octavas, con envolvente creciente |
| `shimmer` | Acorde de Re (Re6, Fa#6, La6, Re7) con trémolo y reverb larga |
| `granular_ticks` | 18–26 ticks con densidad creciente |
| `glitch` | Segmentos de onda cuadrada cuantizada aleatoria |
| `sub_drop` | Seno 142→32 Hz con saturación `tanh` |
| `logo_sting` | Campana aditiva en Re mayor abierto + sub_drop + shimmer + reverb de 2 s |

Detalles técnicos que importan:

- **Reverb** por convolución con un impulso de ruido con decay exponencial y paso bajo de 7 kHz. Cuidado: `fftconvolve` devuelve `len(x)+n-1` muestras; hay que rellenar 1 muestra antes de sumar con la señal seca.
- **Ensanche estéreo compatible con mono** (mid/side): `side = HPF700(mid retrasado 13 ms)·0.35·amount`, con `L = mid + side` y `R = mid − side`. **No** mezcles un canal con su propia copia retrasada: eso produce un filtro peine, desequilibra L/R y algunos efectos se quedaron con correlación 0,07, que en mono desaparecen.
- Verificación tras generar: pico por canal y correlación L/R. Ninguno debe bajar de unos 0,85, salvo los paneos intencionados.

---

## 11. Fase 8 — Música original en código

Dentro de `audio_mix.py → music()`. Todo se sincroniza con el mismo timeline que la imagen.

- **Tempo** de 100 BPM (pulso de 0,6 s; compás de 2,4 s). El primer compás arranca en `B.s1`.
- **Armonía** (Re mayor / Si menor), un acorde por compás: `D – Bm – G – A – Bm – G – Em – Asus`. Acorde final: **Re add9 abierto** (MIDI 38, 50, 57, 62, 64, 66, 69, 76).
- **Capas:**
  - **Pad**: tres sierras desafinadas (±0,08 semitonos) por nota, ADSR lento y paso bajo variable. Corte a 2400 Hz, que baja a **1100 Hz en el tramo oscuro** (s3→s5) y se abre al entrar.
  - **Pluck**: arpegio en corcheas con un patrón de 8 notas sobre el acorde, mezcla de sierra y cuadrada, filtro con envolvente brillante al ataque y velocidad alterna (.9/.65).
  - **Kick** suave en negras, de `s2` a `s6 + .6`; también genera la curva de **sidechain** (`1 − .55·e^{−7t}`) que se aplica a pad, pluck y sub.
  - **Sub**: seno en la fundamental del acorde, mientras suena el groove.
  - **Hats** en contratiempo, solo en el tramo oscuro, para dar más pulso.
  - **Acorde final**: campana aditiva desde `logo + .55` que suena hasta el final.
- Estéreo: pad con 12 ms de retardo en R y pluck algo más presente en R. Fundido de los últimos 0,5 s.

---

## 12. Fase 9 — Voz con ElevenLabs

### 12.1 Con el conector MCP (como se hizo)

```text
1. creative_list_voices(search="Cristina", languages=["es"])
   → voice_id 1CeqBeXMOqCleeQjfYfO  «Cristina – Premium Spanish Female» (peninsular, publicidad)
2. creative_generate_speech(estimate_only=true, model_id="eleven_v4", voice_id=…, generations_count=2, prompt=GUION)
   → 796 créditos para 2 tomas de ~390 caracteres (~1 crédito por carácter)
3. creative_generate_speech(… sin estimate_only, flow_id=<mismo flujo>)  → session_ids
4. creative_get_flow_run_status(flow_id, session_ids)  → repetir hasta all_completed (~30–40 s)
   → content_url de cada toma (URL firmada de Google Storage, caduca en 2 h) → curl -o
5. creative_add_flow_asset_node(generation_id=<toma elegida>)  → node_id
6. creative_transcribe_audio(model_id="eleven_scribe_v1", connect_from=[node_id])  → words[] con start/end
   (0 créditos en esta cuenta)
```

- Usa siempre **un único flujo** (`flow_id`) para que los nodos se puedan conectar.
- **Nunca repitas** una llamada de generación «para reintentar»: cobra de nuevo.
- Guarda los tiempos como `[[palabra, inicio, fin], …]` en `assets_in/vo/<toma>.words.json`.

Voces probadas:

| Voz | voice_id | Resultado |
|---|---|---|
| Cristina – Premium Spanish Female | `1CeqBeXMOqCleeQjfYfO` | **Elegida.** Cálida y de anuncio premium. Toma 1: 25,5 s |
| Gala – Fresh, Energetic & Spontaneous | `Wi5NZQRxyOb3Jx4r0hrI` | Alternativa guardada. Más enérgica. Toma 1: 25,0 s |

### 12.2 Sin MCP (API REST)

`tools/vo_generate.py`: busca la voz por nombre, estima créditos (`--dry-run`) y llama a `/v1/text-to-speech/{voice}/with-timestamps` (modelo, `stability 0.50`, `similarity_boost 0.75`, `speed 1.0`, `seed` por toma). Guarda el MP3 y el `alignment` por carácter. Necesita `ELEVENLABS_API_KEY` y acceso de red a `api.elevenlabs.io`.

### 12.3 ⚠️ Cuenta y licencia

- Con el plan gratuito, ElevenLabs bloqueó una generación con *«Unusual activity… Free Tier access has been disabled… use of a proxy or VPN»*. Las peticiones salen de un servidor en la nube, y eso basta para disparar el aviso.
- Para **anuncios de pago** hace falta un plan con licencia comercial (Starter o superior, según sus condiciones vigentes). Compruébalo antes de publicar.
- Si la cuenta se bloquea a mitad de trabajo, los tiempos de palabra de frases cortas se pueden estimar sin transcribir (sección 13.3).

---

## 13. Fase 10 — Sincronizar la imagen a la voz

### 13.1 `build_timeline_vo.py <words.json> <offset> <out.json>`

1. Suma el `offset` (0,2 s: la voz empieza 0,2 s después del primer fotograma, para dar margen visual) a todos los tiempos.
2. Busca la primera palabra **«Con»** («Con Imperios, …»), que marca el fin del gancho. El gancho puede tener cualquier número de palabras (índice `H`; desplazamiento `D = H − 9` respecto a la toma original).
3. Ancla cada beat a una palabra hablada:

| Beat | Regla |
|---|---|
| `hook` | inicio de «Con» − 0,10 s (el cuadrado nace justo antes) |
| `s1` | hook + 0,6 |
| `s2` | inicio de «todos» + 0,08 |
| `s3` | inicio de «La (inteligencia…)» − 0,13 |
| `s4` | inicio de «Y (cuando hay match)» − 0,13 |
| `s5` | inicio de «Visitas» − 0,13 |
| `s6` | inicio de «Imperios.» − 0,13 |
| `logo` | fin de «fin.» + 0,03 |
| `cta` | inicio de «demo» + 0,33 |
| `end` | fin de «demo.» + 2,4 (cola con el acorde y el CTA en pantalla) |

4. Genera `wt`: el inicio real de cada palabra en pantalla, relativo a su escena. En el match, las tres «llaves» (zona, tipo y presupuesto) usan los tiempos exactos de esas palabras, y de ellas dependen el pin, los chips, los diales y el rango de presupuesto.
5. Activa `hideKt1`: el texto «Tus contactos llegan…» no se dice en la campaña, así que se oculta.
6. Después se añade `hookCol: 0.32`, para que el colapso del gancho no se coma la última palabra de la pregunta.

**Adaptación de textos en pantalla:** si la locución dice algo distinto del texto, adapta el texto a la voz. Aquí la locución dice «coordinados desde la misma agenda» y en pantalla pone «agentes, **desde** la misma agenda», para que quepa en 2 líneas dentro de la zona segura. La palabra «desde» se sincroniza con su tiempo real.

### 13.2 Comprobación

```bash
TL=timeline-campaign-vo.json node render.js stills /tmp/vo 1.5 3.4 3.8 4.3 … 27.5
# tile y revisión visual: cada palabra en pantalla debe coincidir con lo que se oye en ese instante
```

### 13.3 Ganchos B/C con voz (frase nueva + cuerpo de la toma A)

1. Se graba solo la frase de gancho (2,3–2,6 s, ~40 créditos por toma).
2. Se compone el audio: `[gancho hasta fin_habla + 0,3 s] + [toma A desde 3,70 s]`, justo antes de «Con».

```bash
ffmpeg -i gancho.mp3 -i campana-toma-1.mp3 -filter_complex \
 "[0]atrim=0:CUT,apad=whole_dur=CUT,asetpts=PTS-STARTPTS[a];[1]atrim=start=3.70,asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1" out.mp3
```

3. Tiempos de palabra del gancho, **estimados sin transcripción**: los límites del habla salen de `silencedetect` (`-40 dB`, 0,1 s) y la duración se reparte entre las palabras **proporcionalmente a sus sílabas** (grupos vocálicos). Si hay una pausa interna (la coma de «inmobiliaria,»), se reparte por tramos. Los tiempos del cuerpo se desplazan con el mismo corte.
4. `build_timeline_vo.py` funciona igual (detecta «Con»).

---

## 14. Fase 11 — Mezcla y máster

### 14.1 Cadena de la voz (antes de mezclar)

```bash
ffmpeg -i toma.mp3 -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2,aresample=48000" -ac 1 -c:a pcm_f32le vo_proc.wav
```

Paso alto a 80 Hz y compresor suave 3:1. **Sin limitador en la voz.**

### 14.2 `audio_mix.py` (con `VO`, `VO_OFFSET` y `TL`)

```bash
TL=timeline-campaign-vo.json VO=out/campaign-vo/vo_proc.wav VO_OFFSET=0.2 python3 audio_mix.py out/campaign-vo/audio
```

1. Sintetiza la música (sección 11) y la baja 3 dB.
2. Coloca los SFX con la lista de **cues** `(tiempo, sfx, ganancia dB, pan, HPF)`, todos relativos a los beats. Así, al re-temporizar se mueven solos. Hay 96 cues en la versión de campaña con voz: un whoosh a cada palabra o título, un golpe en cada aterrizaje, clicks de dial en la escena del match, pops en las entradas, y sub_drop más sting en el logo. Los whooshes llevan paso alto de 300–400 Hz para no tapar la voz.
3. **Ducking dinámico de la música:**
   - Se calcula el RMS de la voz `rv` y de la música `rm` en ventanas de 400 ms.
   - En las zonas con voz (`rv > max·−24 dB`): `need = clip(rv·10^(−20/20) / rm, 0.02, 1)`, es decir, la música queda 20 dB por debajo de la voz.
   - `minimum_filter1d(need, 0.3 s)`: el ducking se adelanta y se mantiene sin bombear.
   - `uniform_filter1d(need, 0.12 s)`: sin escalones.
   - `music *= need`.
4. **SFX −4 dB** mientras hay voz.
5. Escribe los stems `music.wav`, `sfx.wav`, `vo.wav` y `mix_premaster.wav`, **todos a la misma escala**, de modo que sumados dan exactamente el premaster.
6. Imprime la métrica de control: `VO vs música con voz: mediana X dB, percentil 5 Y dB`.

Resultado: mediana de **22 dB** y percentil 5 de **19,3 dB** (requisito: ≥ 15 dB).

### 14.3 `master_vo.sh <dir>`

```bash
# 1) bus música + SFX: compresor suave y limitador PROPIO (los picos de golpes y sub se controlan aquí, no sobre la voz)
[music][sfx] amix weights='1 1.3' → acompressor thr=0.05 ratio=2.5 → alimiter limit=0.12  = [bed]
# 2) [bed] + [vo] → premix.wav
# 3) ganancia lineal para llegar a −14 LUFS → resample a 192 kHz → alimiter limit=0.85 (≈ −1.4 dBFS) → 48 kHz
```

El resample a 192 kHz alrededor del limitador hace que los picos que se controlan sean **true peak** (entre muestras). Resultado: **−14,0 LUFS / −1,4 dBTP**.

### 14.4 Verificación del limitador (cuánto toca la voz)

Compara `premix × ganancia` con `master` en ventanas de 50 ms, **después de alinear las dos señales por correlación cruzada** (el limitador introduce unas 48 muestras de latencia):

- Sin alinear, la medida dio un falso «13,9 dB de reducción».
- Alineada: **máximo 2,8 dB, p95 de 0,3 dB, >1 dB en solo el 0,7 % de las ventanas con voz.** El limitador no aplasta la voz.

### 14.5 Mezcla sin voz (preview y campaña v2)

`master.sh`: amix música+SFX (×1,3) → compresor → `alimiter 0.6` → `loudnorm` en **dos pasadas y modo lineal** (medir y luego aplicar `measured_*`) → −14,0 LUFS / −1,1 dBTP.

### 14.6 Mux final

```bash
ffmpeg -i video_mudo.mp4 -i master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart final.mp4
```

---

## 15. Fase 12 — Versiones de campaña

### 15.1 Por qué

La primera preview era una buena pieza de marca, pero no estaba pensada para captar en frío. Cambios para la campaña:

1. **Gancho en el primer segundo** con el problema, en texto grande.
2. Decir **para quién es** («CRM PARA INMOBILIARIAS») desde el fotograma 0.
3. **CTA explícito** («Pide tu demo →») de 2,5 s o más, dentro de la zona segura.
4. **3 ganchos** con el mismo cuerpo, para que el test A/B mida solo el gancho.
5. **Corte corto** para Stories y retargeting.

### 15.2 Piezas producidas

| Archivo (`preview/out/…`) | Duración | Notas |
|---|---|---|
| `imperios-reel-v6-preview-v1_9x16.mp4` | 21 s | Preview sin voz |
| `campaign/imperios-campana-v2-gancho-{A,B,C}_9x16.mp4` | 25 s | Campaña sin voz |
| `campaign/imperios-campana-v2-corte-10s_9x16.mp4` | 10,7 s | Corte sin voz |
| `campaign-vo/imperios-campana-v3-voz-A_9x16.mp4` | 28,2 s | **Cristina, gancho A** |
| `campaign-vo-cristina-B/…-B_9x16.mp4` | 27,0 s | Cristina, gancho B |
| `campaign-vo-cristina-C/…-C_9x16.mp4` | 27,2 s | Cristina, gancho C |
| `campaign-vo/imperios-campana-v3-voz-corte-11s_9x16.mp4` | 11,1 s | Corte con voz |
| `campaign-vo-gala/imperios-campana-v3-voz-gala-A_9x16.mp4` | 27,7 s | Alternativa con Gala |

### 15.3 Corte corto con voz (`build_cut10.sh`)

Se eligen tramos que **empiezan y terminan en silencios de la voz**, mirando los tiempos de palabra:

- `0–3,90` (pregunta completa);
- `12,98–17,06` («Y cuando hay match… oportunidad real.»);
- `24,90–28,2` («Pide tu demo» + logo + CTA).

Se unen con `xfade` de 0,12 s en vídeo y `acrossfade` de 0,06–0,08 s en audio. Los huecos entre palabras son de solo 50–80 ms, así que los fundidos deben ser muy cortos. Resultado: 11,1 s a −14,0 LUFS.

### 15.4 CTA

Opciones según cómo vende el cliente: «Pide tu demo», «Pruébalo gratis», «Escríbenos por WhatsApp», «Reserva 15 minutos», «Empieza hoy» o «Descubre…». **Solo se promete lo que existe.** Para cambiarla hay que tocar el texto de `#ctaLbl` en `reel.html` y regrabar la última frase de la voz.

### 15.5 Test A/B (en `campaign/CAMPANA.md`)

- Una campaña con un conjunto de anuncios y los 3 ganchos como anuncios distintos (o Dynamic Creative), en Reels y Stories.
- Métricas para decidir: retención a 3 s (*hook rate*), ThruPlay, CTR y coste por lead o demo.
- Se apaga el gancho más flojo y el mejor se combina con el corte corto.

---

## 16. Control de calidad (QA)

Comprobar antes de entregar:

- [ ] **Contact sheet** a 1 fps: ningún texto se pisa, ninguna palabra queda sola, nada fuera de la zona segura.
- [ ] **Stills en las transiciones** (los ±0,2 s alrededor de cada beat): no asoman elementos de la escena anterior.
- [ ] Cada palabra en pantalla aparece cuando se pronuncia (revisar sobre los `words.json`).
- [ ] `ffprobe`: h264 a 60/1 fps, 1080×1920, AAC, duración esperada.
- [ ] `ebur128=peak=true`: **I = −14,0 LUFS**, **pico ≤ −1,0 dBTP**.
- [ ] Música bajo la voz ≥ 15 dB (salida de `audio_mix.py`).
- [ ] Reducción del limitador sobre la voz medida con alineación (sección 14.4).
- [ ] SFX: correlación L/R razonable (compatibilidad mono) y sin clipping.
- [ ] Pronunciación de la marca correcta en la transcripción.
- [ ] Ninguna cifra o testimonio sin fuente. Datos de ejemplo genéricos.
- [ ] `CREDITS.md` actualizado: voz (proveedor, voice_id, modelo, fecha, créditos), fuentes y SFX.
- [ ] Commit y push.

---

## 17. Problemas reales encontrados y su solución

| Síntoma | Causa | Solución |
|---|---|---|
| `fftconvolve`: «operands could not be broadcast (33600,) (33599,)» | La convolución mide `len+n−1` | Rellenar 1 muestra antes de sumar |
| SFX con L/R desequilibrado y correlación ~0,07 | Mezclar un canal con su copia retrasada (filtro peine) | Ensanche mid/side compatible con mono |
| Subrayado roto en texto de 2 líneas | `::after` absoluto en un inline que se parte | `text-decoration` con color, grosor y offset |
| Subrayado que pisa la línea siguiente | `line-height` 1,06 | 1,16 |
| Texto de captación visible aunque debía ocultarse | `exitBlock()` ponía `opacity:1` después de ocultarlo | Ocultar **después** de `exitBlock` |
| Un render «parado» en el fotograma 900 | La síntesis de audio en paralelo le quitaba CPU (y el `ps \| head` escondía ffmpeg) | No paralelizar; mirar el log, no `ps` truncado |
| `pkill` devolvió exit 144 | Mató la propia shell que lo lanzó | Lanzar renders con `nohup … &` y matarlos por PID |
| Ruta de Chromium fija | Solo existía en el contenedor | `CHROMIUM_PATH` + detección + fallback |
| Música solo 14,2 dB bajo la voz | Ducking constante calculado con el RMS medio | Ducking dinámico por ventana (sección 14.2) |
| «13,9 dB de reducción» del limitador | Medida sin alinear (48 muestras de latencia) | Alinear por correlación: 2,8 dB reales |
| El limitador final aplastaba los golpes | Los transitorios de SFX y sub llegaban al limitador del máster | Limitar el bus música+SFX por separado antes de sumar la voz |
| −13,8 LUFS en lugar de −14 | Margen de +0,2 en la ganancia | Ajustar el margen a 0 |
| 403 al hacer `git push` | GitHub no conectado a la sesión | Conectar GitHub en claude.ai; mientras tanto, commits locales |
| Sin acceso a ElevenLabs, Instagram, web de la marca ni HuggingFace | Proxy con lista blanca | Conector MCP de ElevenLabs; el usuario sube la referencia; kit de marca en lugar de la web |
| Whisper local imposible | No se pueden descargar modelos | Scribe de ElevenLabs (MCP) o estimación por sílabas |
| Generación de ElevenLabs fallida | Plan gratuito marcado por «actividad inusual» (proxy) | Plan de pago (también necesario por licencia comercial) |
| La primera versión se parecía demasiado a la referencia | Se copió su look | Regla: de la referencia, solo el movimiento |
| Cortes de audio que se comen palabras | Huecos de 50–80 ms entre palabras | Cortar sobre los `words.json` y fundidos de 60–80 ms |

---

## 18. Cómo reutilizarlo en otro proyecto

1. **Copia** `ADV/ImperiOS Ad/` a `ADV/<Marca> Ad/`, o solo `preview/`, `tools/` y `storyboard/`.
2. **Kit de marca:**
   - Sustituye los tokens CSS (`:root`) en `reel.html` y `storyboard.html`.
   - Cambia la fuente `@font-face` y el logo.
   - Genera `logo-noaccent.svg`, o adapta el «pixel-home» al elemento de acento de tu logo, y recalcula `LOGO` (x, y, w, h) en `render()`.
3. **Brief:** reutiliza la estructura de `brief/PROMPT.md` y pregunta los conflictos de la sección 4.3 en una sola tabla.
4. **Referencia:** análisis con los comandos de la sección 6. Extrae la gramática, no el look.
5. **Storyboard:** un `<section>` por beat → aprobación.
6. **Motor:** sustituye el HTML de cada escena (la UI de tu producto, recreada) y su bloque en `render(t)`. Mantén las utilidades (`k`, `E`, `words`, `revealWords`, `exitBlock`, `underlineTo`), el escenario oscuro con clip-path y el cuadrado como hilo conductor, o cámbialo por otro elemento de tu marca.
7. **Timeline:** `timeline.json` con los beats provisionales → `stills` → render de la preview sin voz.
8. **Sonido:**
   - `python3 tools/sfx_synth.py assets_in/sfx` (ajusta tonalidades si cambias la de la música);
   - edita `CHORDS`, `FINAL` y `BEAT` en `audio_mix.py`;
   - reescribe `cues()` con los momentos de tu animación (relativos a los beats).
9. **Voz:** guion con respelling de la marca → estimar créditos → 2 tomas → elegir → transcribir → `*.words.json`.
10. **Sincronizar:** adapta en `build_timeline_vo.py` las **palabras ancla** de cada beat (aquí «Con», «todos», «La», «Y», «Visitas», «Imperios.», «fin.», «demo.») y los índices de los bloques `kt*`.
11. **Build:** `./build_vo_version.sh <tag> <vo.mp3> <timeline.json> <variante>`.
12. **QA** con la lista de la sección 16 → commit y push.

---

## 19. Prompt plantilla para otra IA

> Copia, rellena los corchetes y pégalo junto con este documento y el kit de marca.

```text
Vamos a producir un Reel publicitario estilo SaaS para [MARCA / PRODUCTO], siguiendo EXACTAMENTE el método
de docs/GUIA-PRODUCCION-REELS-SAAS.md (léelo entero antes de empezar).

Entradas:
- Kit de marca: [ruta o ZIP] (tokens de color, tipografía, logo SVG, componentes).
- Vídeo de referencia de estilo: [ruta] → extrae SOLO la gramática de movimiento; el look sale del kit de marca.
- Mensaje / funciones a mostrar: [3–5 funciones reales confirmadas].
- Público y CTA real: [público] · [CTA que exista de verdad].
- Voz: [proveedor + voice_id o descripción] · idioma [es-ES] · respelling de la marca: [«…»].
- Duración objetivo: [20–28 s] · formato 9:16 1080×1920 60 fps (+ [4:5 / 16:9] si se pide).
- Prohibido: [no enseñar el producto real / no cifras sin fuente / no fotos de stock / …].

Orden de trabajo (pide mi OK en cada paso):
1. Brief (concepto, guion con dato que respalda cada frase, beat sheet, voz, música, SFX, assets) + tabla de conflictos.
2. Storyboard estático (8 fotogramas HTML) → contact sheet.
3. Preview v1 sin voz: motor reel.html (render(t) puro), render.js con motion blur (sub=3, tmix), música y SFX en código,
   máster −14 LUFS / −1 dBTP.
4. Voz: estima créditos, 2 tomas en una llamada, transcribe con tiempos por palabra.
5. Re-temporiza la IMAGEN a la VOZ (build_timeline_vo.py), mezcla con ducking dinámico (música ≥15 dB bajo la voz,
   sin limitador sobre la voz), verifica con las métricas del documento.
6. Campaña: gancho de problema en el 1.er segundo + «[CATEGORÍA] PARA [PÚBLICO]» + CTA, 3 variantes de gancho, corte de ~10 s.
7. QA con la checklist, CREDITS.md, commit y push.
```

---

## 20. Costes y tiempos reales

| Concepto | Valor |
|---|---|
| Voz, guion completo (~390 caracteres), 2 tomas | 796 créditos ElevenLabs (~0,08 $) por voz |
| Frase de gancho (~40 caracteres), 2 tomas | ~80 créditos |
| Transcripción Scribe | 0 créditos en esta cuenta |
| Total de voz del proyecto (Cristina, Gala y ganchos) | ≈ 1 750 créditos |
| Render de 21 s a 60 fps con sub=3 | ~8,5 min |
| Render de 28 s a 60 fps con sub=3 | ~14 min |
| Síntesis de música + SFX + mezcla | ~50–70 s |
| Generar la biblioteca de SFX | < 1 min |

---

## 21. Inventario de archivos

| Archivo | Rol |
|---|---|
| `preview/src/reel.html` | Motor de animación (≈660 líneas): CSS de marca, DOM de escenas, utilidades, `render(t)` |
| `preview/render.js` | Chromium sin interfaz → JPEG por subfotograma → ffmpeg (`tmix`, x264) |
| `preview/timeline.json` | Preview v1 sin voz (21 s) |
| `preview/timeline-campaign.json` | Campaña sin voz (25 s, gancho de 1,9 s) |
| `preview/timeline-campaign-vo*.json` | Campaña con voz: A (Cristina), B, C y Gala |
| `preview/build_timeline_vo.py` | `words.json` → timeline sincronizado |
| `preview/audio_mix.py` | Música en código, cues de SFX, ducking con voz, stems |
| `preview/master.sh` | Máster sin voz (loudnorm en 2 pasadas, lineal) |
| `preview/master_vo.sh` | Máster con voz (bus limitado aparte + ganancia + limitador true peak) |
| `preview/build_campaign.sh` | Campaña sin voz: A completo, B/C empalmados, corte |
| `preview/build_vo_version.sh` | Pipeline completo de una versión con voz |
| `preview/build_cut10.sh` | Corte corto con voz |
| `preview/finish.sh` | Mux y contact sheet de la preview v1 |
| `tools/sfx_synth.py` | 29 SFX sintetizados |
| `tools/vo_generate.py` | TTS por API REST (alternativa al MCP) |
| `storyboard/storyboard.html` | 8 fotogramas clave estáticos |
| `assets_in/vo/*.words.json` | Tiempos por palabra (Scribe o estimados) |
| `assets_in/CREDITS.md` | Procedencia y licencias |
| `brief/PROMPT.md` | Brief r5 |
| `campaign/CAMPANA.md` | Plan de test y textos del anuncio |
| `HANDOFF.md` | Estado para retomar en otra sesión |

---

## 22. Chuleta de comandos

```bash
cd "ADV/ImperiOS Ad"

# SFX
python3 tools/sfx_synth.py assets_in/sfx

# Revisar instantes sueltos
cd preview
TL=timeline-campaign-vo.json node render.js stills /tmp/st 3.8 8.0 12.6 25.3

# Preview sin voz
node render.js video out/x_silent.mp4 3
python3 audio_mix.py out/audio && ./master.sh out/audio && ./finish.sh

# Timeline desde la voz
python3 build_timeline_vo.py ../assets_in/vo/campana-toma-1.words.json 0.2 timeline-campaign-vo.json

# Versión con voz completa (voz → mezcla → máster → render → mux → contact sheet)
./build_vo_version.sh cristina-A ../assets_in/vo/campana-toma-1.mp3 timeline-campaign-vo.json A

# Corte corto con voz
./build_cut10.sh

# Medidas
ffmpeg -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
ffmpeg -i vo.mp3 -af silencedetect=n=-40dB:d=0.15 -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+"
```
