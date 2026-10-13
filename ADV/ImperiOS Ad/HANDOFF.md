# Handoff — ImperiOS Spec Ad v6

Estado a 13/10/2026:

- **Brief r5 aprobado.** Guion aprobado tal cual (`brief/VO_SCRIPT.txt`). Estilo: el del storyboard (`storyboard/storyboard-contact-sheet.png`).
- **Listo:** kit de marca (`assets_in/brand-kit/`), 29 SFX originales (`assets_in/sfx/`, `tools/sfx_synth.py`), storyboard de 8 fotogramas (`storyboard/storyboard.html`).
- **Siguiente:**
  1. `python3 tools/vo_generate.py --dry-run` para comprobar la voz y los créditos (~780); después, sin `--dry-run`, generar las 2 tomas.
  2. El usuario elige toma → PREVIEW v1 9:16 a 60 fps + contact sheet, con la imagen re-temporizada a la voz (`*.alignment.json`).
- **Reglas:** sin end card; amarillo `#FFD500` solo en detalles; Manrope; UI recreada, sin capturas del CRM; música en código ≥15 dB por debajo de la VO; master a −14 LUFS / −1 dBTP.
