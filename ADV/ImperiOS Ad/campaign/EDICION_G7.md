# Edición del vídeo G7 «Horas que no venden» — instrucciones para el montaje en local (13/11/2026)

Documento de traspaso para la sesión de Claude Code en el ordenador de Brian, que tiene los vídeos grabados.
Contexto completo: `GUION_BRIAN_CAMARA.md` (guion), `CAMPANA.md` (campaña y guía de estilo v4),
`docs/GUIA-PRODUCCION-REELS-SAAS.md` (pipeline de vídeo de la marca).

## 1. Qué hay que entregar

Un anuncio de Meta (Reels / Stories) con Brian hablando a cámara, ~29 s:

- **1080×1920 (9:16)**, H.264 (crf 14–16) + AAC 320k, MP4 con `+faststart`. 30 fps (la grabación es a 30 fps).
- Audio a **−14 LUFS / −1 dBTP**, voz limpia, música por debajo (~22 dB bajo la voz, con ducking).
- Nombre: `preview/out/brian/imperios-g7-horas_9x16.mp4` + hoja de contacto `contact-sheet-g7.png`.
- Es el tercer anuncio de la campaña junto a `imperios-v4-corto-ganchoA-asesoria` y `imperios-reel-r11-falso-interes-asesoria`.

## 2. Guion final (lo que Brian dice)

| Bloque | Texto |
|---|---|
| 1 · Gancho | «Si diriges una inmobiliaria, tu equipo está perdiendo horas cada semana en tareas que no venden.» |
| 2 · Qué tareas | «Revisar uno a uno los leads que te entran de cada portal inmobiliario, buscar qué piso encaja con cada cliente, recordarle a cada uno su visita…» |
| 3 · Solución | «ImperiOS, nuestro CRM automatizado, lo hace solo. Te ahorra más de 30 horas a la semana. Horas que tu equipo dedica a lo que importa: vender.» |
| 4 · Para ti | «Y tú lo tienes todo en una sola herramienta, para ver qué funciona… y qué no.» (gira el móvil a cámara) |
| 5 · Cierre | «Déjame tus datos y revisamos tu caso. Gratis y sin compromiso.» |

Brian grabó por bloques, con varias tomas seguidas y sin parar la cámara (frase, ~2 s de silencio, repetición),
y al final una toma entera. Cámara: DJI Osmo Pocket 3, vertical, 4K/30 fps (comprobar con `ffprobe`).

## 3. Pasos

1. **Inventario:** `ffprobe` de cada archivo (resolución, fps, rotación, duración, audio). No modificar los originales;
   trabajar en `preview/out/brian/` (los vídeos fuente fuera del repo o en una carpeta ignorada por git: pesan GB).
2. **Proxies** a 1080 de ancho para revisar rápido; el corte final se hace desde el 4K original.
3. **Transcripción con tiempos por palabra** de cada archivo (faster-whisper/WhisperX en local, o Scribe de ElevenLabs).
   Guardar `[[palabra, inicio, fin], …]` como en `assets_in/vo/starter/*.words.json`.
4. **Elegir la mejor toma de cada bloque** (frase completa, sin trabas, buena energía; el gancho es lo más importante)
   y **enseñar la selección a Brian antes de montar** (bloque → archivo → inicio/fin). Guardar la selección en un JSON
   (EDL) para que el montaje sea reproducible.
5. **Corte:** recortar cada tramo con ffmpeg sobre el 4K (cortes en el silencio entre palabras, fundido de audio
   de 10–20 ms), escalar/recortar a 1080×1920 y concatenar. Cortes secos, sin transiciones.
   **Punch-in** (zoom ~1,15–1,2 centrado en la cara) en bloques alternos (p. ej. 2 y 4) para que los saltos parezcan
   intencionados; aprovecha el 4K. Sin silencios muertos: entre bloques, ≤ 0,15 s.
6. **Capa gráfica** (estilo v4: Manrope, `#F7F7F3` / `#0A0A0A`, amarillo `#FFD500` solo en detalles, brillos `#FFC000`
   con transparencia, tokens en `assets_in/brand-kit/tokens.json`), sincronizada con las palabras de la transcripción:
   - **Gancho:** el texto del gancho visible **desde el primer fotograma** (sin animación de entrada), subrayado
     amarillo en **horas**. Rótulo pequeño «Brian · fundador de ImperiOS» los primeros ~2 s.
   - **Bloque 2:** las tres tareas aparecen al decirlas y se tachan una tras otra.
   - **Bloque 3:** «+30 h / semana» grande al decir «30 horas»; subrayado amarillo en **vender**.
   - **Bloque 4:** inserto del panel de la **cuenta demo** (datos simulados) cuando Brian gira el móvil, con etiquetas
     que entran una tras otra: captación · clientes · propiedades · visitas · campañas.
   - **Cierre:** logo `assets_in/brand-kit/assets/logo-imperios-navbar.svg` + botón «Déjanos tus datos» +
     «ASESORAMIENTO GRATUITO · SIN COMPROMISO» (≥ 2,5 s en pantalla), como en los anuncios v4/R11 de asesoría.
   - **Subtítulos** palabra a palabra (mucha gente ve sin sonido), dentro de la zona segura de Reels
     (ver `preview/out/v4/prueba-zona-segura.png`): nada importante en los ~250 px de abajo ni en el lateral derecho.
   - Implementación sugerida: una página HTML nueva (derivada de `preview/src/reel-v4.html`) con **fondo transparente**,
     renderizada con `preview/render.js` (screenshots con `omitBackground: true`) a PNG con alfa o a ProRes 4444,
     y compuesta encima del vídeo con `ffmpeg overlay`. Brian tiene que ocupar al menos 2/3 del vídeo; los insertos
     a pantalla completa, de 1–2 s.
7. **Audio:** voz con `highpass=f=80`, reducción de ruido suave (`afftdn` o `arnndn`), compresor como en
   `build_v4.sh` (`acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2`) y de-esser si hace falta.
   Música y SFX con `preview/audio_mix.py` (generados en código, sin licencias externas), ~22 dB bajo la voz con ducking.
   Master con `preview/master_vo.sh` → −14 LUFS / −1 dBTP.
8. **Exportar**, generar la hoja de contacto (mismo comando que en `build_v4.sh`) y **enseñársela a Brian** junto al vídeo.
   Iterar con sus cambios.
9. Commit + push de scripts, EDL, transcripciones y el MP4 final (no los vídeos fuente).

## 4. Reglas

- Nada de datos reales de clientes: las pantallas son de la cuenta demo con datos simulados. Credenciales de la demo
  solo por variables de entorno (`IMPERIOS_DEMO_URL`, `IMPERIOS_DEMO_EMAIL`, `IMPERIOS_DEMO_PASSWORD`), nunca en el repo.
- No alterar la cara ni la voz de Brian con IA (ni lip-sync ni frases generadas). Mejorar audio, color y encuadre sí.
- Fondo: si se cambia o desenfoca, que sea creíble; si se usa un fondo generado por IA, avisar a Brian (ver la nota
  de política de IA en `GUION_BRIAN_CAMARA.md`).
- La cifra de 30 h debe estar justificada (Brian guarda cómo se calculó). Sin testimonios ni otras cifras.
- Sin marcas de portales ni de otros CRM.

## 5. Dependencias en el ordenador

- ffmpeg (con libx264), Node 18+ y Python 3.11+.
- `cd "ADV/ImperiOS Ad/preview" && npm install && npx playwright install chromium` (render.js usa `playwright-core`;
  si Chromium no está en la ruta por defecto, `CHROMIUM_PATH=<ruta>`).
- `pip install -r "ADV/ImperiOS Ad/preview/requirements.txt"` (numpy, scipy) y, para transcribir en local,
  `pip install faster-whisper` (modelo `large-v3` o `medium`, idioma `es`, `word_timestamps=True`).
