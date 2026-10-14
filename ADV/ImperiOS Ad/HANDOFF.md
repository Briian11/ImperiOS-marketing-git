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

### Estado de la siguiente fase (14/10/2026)

- Variables `IMPERIOS_DEMO_URL`, `IMPERIOS_DEMO_EMAIL` e `IMPERIOS_DEMO_PASSWORD`: **definidas**.
- Red: **bloqueada**. El proxy de la sesión devuelve `403` al conectar con `prueba.imperios.app` (también con `imperios.app`). Hay que añadir el host en *Allowed domains* del entorno y **abrir una sesión nueva** (la lista se aplica al arrancar el contenedor).
- HyperFrames clonado en `/home/user/heygen-com/hyperframes` (commit `9c11715`).
- Script de captura listo: `capture/capture.mjs` + `capture/screens.json` (probado contra un login simulado en local, no contra el CRM):
  ```bash
  cd "ADV/ImperiOS Ad/capture" && npm install
  node capture.mjs explore     # login + mapa del menú → out/explore.json + out/00-home@2x.png
  # ajustar "nav" o "path" de cada pantalla en screens.json según explore.json
  node capture.mjs shots       # out/<id>@2x.png (2880×1800) + <id>-full@2x.png
  node capture.mjs record      # out/<id>.mp4 (2880×1800, 60 fps)
  ```
  El login se hace en un contexto sin vídeo; la sesión se guarda en `/tmp` (fuera del repo) y las credenciales se redactan en los logs. Cualquier elemento que muestre el email de la cuenta sale tapado (magenta) en las capturas; para tapar más cosas, añadir selectores en `"mask"`.
  `capture/out/` está en `.gitignore`: **las capturas no se suben hasta que el usuario las revise** (paso 2).
