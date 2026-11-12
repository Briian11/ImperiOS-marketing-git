# ImperiOS — Campaña v2 (Reels / Stories 9:16)

Pendiente de confirmar: **llamada a la acción real** (ahora «Pide tu demo») y **público** (ahora: inmobiliarias en general).

## Piezas

| Archivo | Duración | Uso |
|---|---|---|
| `imperios-campana-v2-gancho-A_9x16.mp4` | 25 s | Gancho de dolor: «¿Tus leads se pierden entre portales, WhatsApp y Excel?» |
| `imperios-campana-v2-gancho-B_9x16.mp4` | 25 s | Gancho de pérdida: «¿Cuántos clientes se te escapan cada mes?» |
| `imperios-campana-v2-gancho-C_9x16.mp4` | 25 s | Gancho de beneficio: «Toda tu inmobiliaria, en un solo panel.» |
| `imperios-campana-v2-corte-10s_9x16.mp4` | ~10 s | Gancho A + match con IA + reactivar + CTA, para Stories y retargeting |

Las tres de 25 s comparten el cuerpo; solo cambia el primer 1,9 s. Así el test A/B mide únicamente el gancho.

## Montaje del test en Meta (propuesta)

- Una campaña, un conjunto de anuncios, los 3 ganchos como anuncios distintos (o Dynamic Creative).
- Ubicaciones: Reels + Stories de Instagram y Facebook.
- Métricas para decidir: retención a 3 s (hook rate), ThruPlay, CTR al enlace y coste por lead/demo.
- Pasados unos días con gasto suficiente en cada anuncio, apagar el gancho más flojo y duplicar el mejor con el corte de 10 s.

## Textos del anuncio (borrador)

**Texto principal A:** Portales, campañas, web, WhatsApp… y cada lead en un sitio distinto. ImperiOS los reúne en un solo panel, cruza cada cliente con tu cartera usando IA y coordina las visitas de todo el equipo.

**Texto principal B:** Muchos de tus clientes ya te contactaron una vez. ImperiOS detecta cuándo un inmueble de tu cartera encaja con lo que buscaban y te avisa para reactivarlos.

**Texto principal C:** Captación, match con IA, visitas, recordatorios y agentes. Toda la operativa de tu inmobiliaria, conectada de principio a fin.

**Titular:** CRM para inmobiliarias · **Descripción:** Pide tu demo · **Botón:** Solicitar información / Más información

Sin cifras de resultados ni testimonios hasta tener fuente y aprobación.

---

# Campaña v4 — 3 ganchos × 2 duraciones (voz Cristina)

Mismo estilo recreado (sin pantallas reales del CRM), sin subtítulos aparte: el texto cinético ya sigue a la voz.
Motor: `preview/src/reel-v4.html` · timelines: `preview/build_timeline_v4.py` · build: `preview/build_v4.sh <largo|corto> <A|B|C>`.

Todas con voz con licencia comercial (eleven_v4, Cristina, plan Starter, 21/10/2026).

| Pieza | Gancho | Duración | Archivo |
|---|---|---|---|
| Largo A | ¿Tus leads se pierden entre portales, WhatsApp y Excel? | 37,1 s | `preview/out/v4/imperios-v4-largo-ganchoA_9x16.mp4` |
| Largo B | ¿Cuántos clientes se le escapan cada mes a tu inmobiliaria? | 36,8 s | `preview/out/v4/imperios-v4-largo-ganchoB_9x16.mp4` |
| Corto A | (A) | 19,9 s | `preview/out/v4/imperios-v4-corto-ganchoA_9x16.mp4` |
| Corto B | (B) | 19,5 s | `preview/out/v4/imperios-v4-corto-ganchoB_9x16.mp4` |
| Largo C | ¿Cansado de usar diferentes herramientas para gestionar tu inmobiliaria? | 37,4 s | `preview/out/v4/imperios-v4-largo-ganchoC_9x16.mp4` |
| Corto C | (C) | 20,2 s | `preview/out/v4/imperios-v4-corto-ganchoC_9x16.mp4` |

Escenas del largo: gancho → «Lo centralizas absolutamente todo» (pixel late) → 4 fuentes (portales, web, campañas, WhatsApp) →
panel + ranking «qué campañas y propiedades te traen más clientes» → match con IA → chat: la IA envía las propiedades al cliente
(«Enviado automáticamente») → agenda con recordatorio automático y agentes → «Todo conectado. De principio a fin.» → logo + «Pide tu demo».
El corto: gancho → 4 fuentes → match → chat → logo + «Pide tu demo».

La voz va a atempo 1,07 (sin cambio de tono) para acercar las piezas a 15/30 s. Aun así el guion corto dura ~18 s y el largo ~35 s:
para bajar de ahí hay que recortar texto (p. ej. quitar «Imperios.» antes de «Pide tu demo» en el corto, o «coordinados desde la misma agenda» en el largo).

Para el gancho C, cuando haya voz: guardar la toma como `assets_in/vo/v4-gancho-C-toma-1.mp3`, transcribirla a
`v4-gancho-C-toma-1.words.json` y ejecutar `build_timeline_v4.py` + `build_v4.sh` con C (el texto C ya está en el motor).

**Cierre del gancho C (19/10/2026):** la voz termina con «Pide tu demo gratis, sin compromiso» (frase generada aparte y empalmada
sobre el cuerpo: `assets_in/vo/v4-largo|corto-cierre-gratis.wav`) y bajo el botón aparece «GRATIS · SIN COMPROMISO / IMPERIOS.APP ↗»
(`CTA_SUB` en `build_timeline_v4.py`). Solo usar si la demo es realmente gratuita. Los ganchos A y B siguen con «Pide tu demo».

## Guía de estilo v4 (aprobada 21/10/2026) — referencia para nuevas piezas

- **Formato:** 1080×1920, 60 fps, H.264 (crf 14) + AAC 320k, −14 LUFS / −1 dBTP. Motor: `preview/src/reel-v4.html`.
- **Paleta de redes:** fondo `#F7F7F3`, negro `#0A0A0A`, amarillo sólido `#FFD500` solo en detalles (subrayados, botón, chips
  activos, punto del logo), brillos y sombras `#FFC000` siempre con transparencia. Escenas de IA en fondo negro.
- **Tipografía:** Manrope (variable). Texto cinético palabra a palabra, sincronizado con los tiempos de Scribe de la voz;
  la palabra clave lleva subrayado amarillo.
- **Movimiento:** desenfoque de movimiento real (3 subfotogramas), entradas con blur corto; nada borroso en reposo.
  El gancho se lee **desde el primer fotograma** (sin animación de entrada).
- **UI recreada** (nunca capturas del CRM ni datos reales); chat genérico, no copia de WhatsApp; sin marcas de portales.
- **Estructura:** gancho (pregunta de dolor) → «Lo centralizas todo» → fuentes de leads → panel/ranking → match con IA →
  envío automático → agenda → «Todo conectado» → logo + «Pide tu demo · Gratis, sin compromiso» (≥2,5 s).
- **Voz:** Cristina (`1CeqBeXMOqCleeQjfYfO`), eleven_v4, una sola toma por texto, generada en el plan Starter; atempo 1,07.
- **Audio:** música y SFX generados en código (`preview/audio_mix.py`), música ~22 dB bajo la voz con ducking dinámico.
- **Sin cifras ni testimonios** no verificados.
- Hojas de contacto de las versiones anteriores (v2, v3, v6) en `referencia-versiones-anteriores/`.

---

# Campaña de captación (10/11/2026) — cierre «asesoramiento gratuito»

Objetivo: formulario instantáneo de Meta; Brian llama a cada lead. El cierre dice exactamente eso, sin «Pide tu demo».

| Anuncio | Ángulo | Archivo |
|---|---|---|
| v4 corto gancho A (~25 s) | Captar: los leads se pierden entre canales | `preview/out/v4/imperios-v4-corto-ganchoA-asesoria_9x16.mp4` |
| *(reserva)* v4 largo gancho A (~40 s) | Renovar creatividad o retargeting | `preview/out/v4/imperios-v4-largo-ganchoA-asesoria_9x16.mp4` |
| R11 «Falso interés» (~39 s) | Priorizar: la IA califica a cada contacto | `preview/out/reels/imperios-reel-r11-falso-interes-asesoria_9x16.mp4` |
| Brian a cámara (pendiente de grabar) | Medir: el panel del director | guion en `GUION_BRIAN_CAMARA.md` |

El R13 queda como Reel orgánico (su mensaje lo cuenta Brian a cámara). R9 y R10 quedan de reserva para renovar creatividades.

- **Voz del cierre:** «Déjanos tus datos y revisamos tu caso para asesorarte gratis, sin compromiso.» Cristina, eleven_v4,
  ImperiOS's Workspace (licencia comercial), 10/11/2026 → `assets_in/vo/starter/cierre-asesoria.mp3` + tiempos de Scribe.
  Empalmada con `tools/empalmar_vo.py` tras «Imperios.» (v4) y tras «¿…falso interés?» (R11).
- **En pantalla:** botón «Déjanos tus datos» y debajo «ASESORAMIENTO GRATUITO / SIN COMPROMISO»
  (`CTA_LBL` y `CTA_SUB` en los timelines; los motores v4 y R11 ya aceptan los dos).
- **v4 corto (12/11/2026):** lleva la frase del match del largo («La inteligencia artificial cruza las características de tus
  propiedades con lo que busca cada cliente, y le envía automáticamente por WhatsApp las que encajan»), empalmada de
  `cuerpo-largo.mp3` en lugar de la suya; la escena del match usa los tiempos de esa frase.
- **Build:** `preview/build_asesoria.sh [v4|v4largo|r11]`. Las versiones orgánicas anteriores no cambian.
- **Formulario:** tipo «Mayor intención»; nombre, teléfono, inmobiliaria, nº de comerciales y cómo gestionan hoy los leads.
  Pantalla final: «Brian te llamará personalmente». Botón del anuncio: «Solicitar información».
- Solo decir «sin compromiso» mientras la llamada no obligue a nada.
