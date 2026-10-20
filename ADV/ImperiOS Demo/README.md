# ImperiOS — Vídeo demo del CRM (16:9)

Demostración guiada del CRM sobre la **cuenta demo** (datos ficticios), ~2:37, 1920×1080 a 60 fps. Guion: `GUION-DEMO.md` (v5).

## Cómo está hecho

1. **Capturas** (`../ImperiOS Ad/capture/demo-states.mjs`): cada estado de cada interacción (antes/después de cada clic) a 2x, con la posición de los elementos clave. Solo navegación, salvo una acción real autorizada: arrastrar una tarjeta de «Contactado» a «Interesado» en *Leads de campaña* (`--drag`). Email de la cuenta oculto; engranaje flotante oculto. Salida fuera de git.
2. **Voz**: ElevenLabs, Cristina (`1CeqBeXMOqCleeQjfYfO`), `eleven_v4`. Toma completa `vo/demo-toma-1.mp3` (130,4 s; 2 tomas, 4.352 créditos) + clips propios de los párrafos reescritos en la v5 (`vo/v5-contactos|chat|rendimiento.mp3`, 851 créditos). Todas las transcripciones de Scribe coinciden palabra por palabra con el guion; tiempos en `vo/*.words.json`.
   - Los párrafos de la toma completa se separan **en el silencio real** (mínimo de energía entre la última palabra de un párrafo y la primera del siguiente), no en los tiempos de Scribe: así no se cuela el arranque de la frase siguiente ni se corta su comienzo.
   - `build/align.py` estima tiempos sin Scribe (plan B), pero es impreciso con frases largas: úsalo solo para pruebas.
3. **Timeline** (`build/timeline.py` + `build/spec.py`): una escena por párrafo, 1,2 s de aire entre escenas, y cada acción visual (cursor, clic, cambio de estado, cámara, foco, arrastre) anclada a una palabra de la voz. Genera `hyperframes/data.js` y la pista `vo.wav`.
4. **Audio** (`build/audio.py`): música original en código muy leve (pad + arpegio en Re mayor, ~21 dB bajo la voz mientras habla), clics y transiciones discretos, máster −14 LUFS / −1 dBTP.
5. **Composición** (`hyperframes/index.html`): ventana de navegador, cámara (desplazamiento/zoom), cursor con onda de clic, focos amarillos con viñeta, fundidos/deslizamientos entre pantallas, escenario oscuro en la escena de IA, subtítulos palabra a palabra, intro y cierre con logo (sin CTA).

## Construir

```bash
cd "ADV/ImperiOS Demo" && ./build.sh            # QUALITY=delivery ./build.sh para el render final
```

Cambiar algo: textos/tiempos de la cámara y focos en `build/spec.py`; estilo en `hyperframes/index.html`; voz nueva → nuevo `words.json` y `build/timeline.py`.
