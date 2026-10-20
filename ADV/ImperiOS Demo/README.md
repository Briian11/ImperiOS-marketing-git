# ImperiOS — Vídeo demo del CRM (16:9)

Demostración guiada del CRM sobre la **cuenta demo** (datos ficticios), ~2:28, 1920×1080 a 60 fps. Guion: `GUION-DEMO.md` (v4).

## Cómo está hecho

1. **Capturas** (`../ImperiOS Ad/capture/demo-states.mjs`): cada estado de cada interacción (antes/después de cada clic) a 2x, con la posición de los elementos clave. Solo navegación, salvo una acción real autorizada: arrastrar una tarjeta de «Contactado» a «Interesado» en *Leads de campaña* (`--drag`). Email de la cuenta oculto; engranaje flotante oculto. Salida fuera de git.
2. **Voz**: ElevenLabs, Cristina (`1CeqBeXMOqCleeQjfYfO`), `eleven_v4`, 2 tomas (4.352 créditos). Se usa la **toma 1** (`vo/demo-toma-1.mp3`, 130,4 s): su transcripción con Scribe coincide palabra por palabra con el guion. Tiempos por palabra en `vo/demo-toma-1.words.json`.
3. **Timeline** (`build/timeline.py` + `build/spec.py`): una escena por párrafo, 1,2 s de aire entre escenas, y cada acción visual (cursor, clic, cambio de estado, cámara, foco, arrastre) anclada a una palabra de la voz. Genera `hyperframes/data.js` y la pista `vo.wav`.
4. **Audio** (`build/audio.py`): música original en código muy leve (pad + arpegio en Re mayor, ~21 dB bajo la voz mientras habla), clics y transiciones discretos, máster −14 LUFS / −1 dBTP.
5. **Composición** (`hyperframes/index.html`): ventana de navegador, cámara (desplazamiento/zoom), cursor con onda de clic, focos amarillos con viñeta, fundidos/deslizamientos entre pantallas, escenario oscuro en la escena de IA, subtítulos palabra a palabra, intro y cierre con logo (sin CTA).

## Construir

```bash
cd "ADV/ImperiOS Demo" && ./build.sh            # QUALITY=delivery ./build.sh para el render final
```

Cambiar algo: textos/tiempos de la cámara y focos en `build/spec.py`; estilo en `hyperframes/index.html`; voz nueva → nuevo `words.json` y `build/timeline.py`.
