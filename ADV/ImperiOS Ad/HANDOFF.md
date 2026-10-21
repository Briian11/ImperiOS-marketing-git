# Handoff — ImperiOS Spec Ad v6

Estado a 13/10/2026:

- **Brief r5 aprobado.** Guion aprobado tal cual (`brief/VO_SCRIPT.txt`). Estilo: el del storyboard (`storyboard/storyboard-contact-sheet.png`).
- **Listo:** kit de marca (`assets_in/brand-kit/`), 29 SFX originales (`assets_in/sfx/`, `tools/sfx_synth.py`), storyboard de 8 fotogramas (`storyboard/storyboard.html`).
- **Siguiente:**
  1. `python3 tools/vo_generate.py --dry-run` para comprobar la voz y los créditos (~780); después, sin `--dry-run`, generar las 2 tomas.
  2. El usuario elige toma → PREVIEW v1 9:16 a 60 fps + contact sheet, con la imagen re-temporizada a la voz (`*.alignment.json`).
- **Reglas:** sin end card; amarillo `#FFD500` solo en detalles; Manrope; UI recreada, sin capturas del CRM; música en código ≥15 dB por debajo de la VO; master a −14 LUFS / −1 dBTP.

## Actualización — campaña con voz (13/10/2026)

- VO generada con el conector de ElevenLabs: 2 tomas (`assets_in/vo/campana-toma-*.mp3`). Se usa la toma 1; tiempos de palabra en `campana-toma-1.words.json`.
- `preview/build_timeline_vo.py` genera `timeline-campaign-vo.json` desde esos tiempos (imagen re-temporizada a la voz, offset 0,2 s).
- Mezcla: `VO=… VO_OFFSET=0.2 TL=timeline-campaign-vo.json python3 audio_mix.py out/campaign-vo/audio` + `./master_vo.sh out/campaign-vo/audio` (ducking dinámico: música ~22 dB bajo la voz; −14 LUFS / −1,4 dBTP).
- Render: `./build_campaign_vo.sh`.
- Pendiente: VO de los ganchos B y C, y confirmar la llamada a la acción.

## Documentación

Proceso completo, reproducible y reutilizable en `docs/GUIA-PRODUCCION-REELS-SAAS.md` (en la raíz del repo).

## Siguiente fase — versión con el producto real en HyperFrames (14/10/2026)

Decisiones ya tomadas:
- Voz: **Cristina** (`1CeqBeXMOqCleeQjfYfO`), toma 1 + ganchos B/C. Gala queda como alternativa guardada.
- Motor nuevo: **HyperFrames** (`github.com/heygen-com/hyperframes`, Apache 2.0, npm `hyperframes`, v0.8.158 verificada).
  Clonar en lectura: `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/heygen-com/hyperframes /home/user/heygen-com/hyperframes`
  Skill de referencia: `skills/product-launch-video/SKILL.md` (su `capture` no hace login → usar script propio de Playwright).
- Imágenes reales del CRM desde la **cuenta demo con datos simulados** (nunca datos de clientes reales).

Entorno (configurado por el usuario; verificar al empezar sin imprimir valores):
- Variables: `IMPERIOS_DEMO_URL` (login), `IMPERIOS_DEMO_EMAIL`, `IMPERIOS_DEMO_PASSWORD`.
- Dominio del CRM añadido en *Allowed domains*.
- Comprobación: `for v in IMPERIOS_DEMO_URL IMPERIOS_DEMO_EMAIL IMPERIOS_DEMO_PASSWORD; do [ -n "${!v}" ] && echo "$v ok"; done` y `curl -o /dev/null -w "%{http_code}" "$IMPERIOS_DEMO_URL"`.

Pasos:
1. Script Playwright de captura (login con las variables; nunca escribirlas en el repo ni en logs): capturas a 2x de cada pantalla
   y grabación de interacciones clave. Pantallas propuestas por beat del guion:
   bandeja de leads con origen · panel de campañas/estadísticas · Match con IA (cliente ↔ inmueble) · aviso de match + reactivar · agenda compartida + agentes.
2. **Enseñar las capturas al usuario antes de usarlas** (revisar que no salga nada sensible).
3. Brief de la versión «producto real»: pantallas reales como base (zoom/foco/resaltado amarillo animados encima) + nuestras animaciones propias para gancho, transiciones y CTA.
4. Portar escenas a HyperFrames (composición HTML con `data-*` + GSAP), reutilizar VO (`assets_in/vo/campana-toma-1.mp3`, tiempos en `campana-toma-1.words.json`), SFX y música; mantener −14 LUFS / −1 dBTP y música ≥15 dB bajo la voz.
5. CTA pendiente de confirmar por el usuario (por defecto «Pide tu demo»).

---

## Estado 21/10/2026 — voces con licencia: RESUELTO

- Conector de ElevenLabs reconectado a **«ImperiOS's Workspace»** (plan Starter, workspace `e02846d04b35418abc483b6a7859ccda`).
  Voces regeneradas allí el 21/10/2026: **eleven_v4** (GA desde 28/09/2026), voz Cristina `1CeqBeXMOqCleeQjfYfO`,
  una sola toma por texto → `assets_in/vo/starter/` (ganchos A/B/C + cuerpos largo y corto) con tiempos de Scribe
  (`*.words.json`). Son las **únicas voces con licencia comercial**.
- `assets_in/vo/licencia*` y todas las tomas anteriores se generaron en la cuenta gratuita («Brian's Workspace»):
  **no usar en anuncios**.
- **Limpieza 21/10/2026:** borrados del repo los vídeos v2/v3/v6 y todas las voces sin licencia (`assets_in/vo/` fuera de
  `starter/`). Quedan sus hojas de contacto en `referencia-versiones-anteriores/` y la guía de estilo en
  `campaign/CAMPANA.md`. Las rutas a `assets_in/vo/campana-toma-*` de las secciones anteriores ya no existen.
- Montaje: `preview/build_licencia.sh <largo|corto> <A|B|C>` (timeline con las tomas de `starter/` + `build_v4.sh`).
  Los 6 vídeos de `preview/out/v4/` se regeneran con estas voces (prioridad: largo C, piloto Meta).
- Requisitos ya aplicados en el motor: paleta #F7F7F3 / #FFD500 / brillos #FFC000, gancho legible desde el primer
  fotograma, «Pide tu demo · Gratis, sin compromiso» ≥2,5 s, 1080×1920 H.264 + AAC.
