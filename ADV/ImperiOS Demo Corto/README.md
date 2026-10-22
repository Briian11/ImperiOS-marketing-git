# ImperiOS — Vídeo demo corto del CRM (16:9)

Versión de ~50 s del vídeo demo (`../ImperiOS Demo`, 2:37) sobre la **cuenta demo** (datos ficticios), 1920×1080 a 60 fps.
Mismas capturas, música, efectos y estilo; voz nueva más compacta; subtítulos palabra a palabra; cierre con logo y lema (sin CTA).

## Guion (`vo/VO_CORTO.txt`)

| # | Escena | Qué se ve |
|---|---|---|
| — | Intro: «Esto es ImperiOS, el CRM para inmobiliarias.» | Logo → ventana con el panel |
| 01 | Contactos: los leads de portales y web entran solos, con origen y temperatura | Tabla → foco en Fuente y Temperatura |
| 02 | Chat: Idealista, Fotocasa, web y WhatsApp en una bandeja; respondes por WhatsApp | Etiquetas de origen → abrir un lead → caja de respuesta |
| 03 | Coincidencias IA: cruza búsquedas con la cartera y dice a quién llamar | Escenario oscuro, tarjeta de coincidencia → por propiedad |
| 04 | Marketing: qué campaña y qué anuncio traen leads; tablero | Campañas → anuncios → arrastre real de una tarjeta |
| 05 | Métricas: leads por portal, cuántos acaban en visita, rendimiento por propiedad y por comercial | Procedencia → embudo → rendimiento por propiedad → Dirección |
| 06 | Y además: panel del día, ficha de cliente, propiedades publicadas, agenda | Tarjetas de esos módulos, sin entrar en detalle |
| — | Cierre: «ImperiOS. Todo tu negocio inmobiliario, conectado.» | Logo |

## Cómo está hecho

- **Voz**: ElevenLabs, Cristina (`1CeqBeXMOqCleeQjfYfO`), `eleven_v4`, plan con licencia comercial. 2 tomas (724 créditos cada una); se usa `vo/corto-toma-1.mp3` (43,7 s). La transcripción de Scribe coincide palabra por palabra con el guion (`vo/corto-toma-1.words.json`).
- **Timeline** (`build/timeline.py` + `build/spec.py`): la toma se corta por párrafos en el silencio real y se recoloca con 0,5 s de aire entre escenas; cada gesto (cámara, foco, clic, cambio de pantalla, arrastre, tarjetas) va anclado a una palabra.
- **Reutiliza del demo largo**: `../ImperiOS Demo/build/plates.py` y `audio.py` (con este proyecto como argumento) y el motor de `hyperframes/index.html`, al que se añade la escena de tarjetas («Y además»).

## Construir

```bash
cd "ADV/ImperiOS Demo Corto" && ./build.sh       # QUALITY=delivery ./build.sh para el render final
```

Requiere las capturas en `../ImperiOS Ad/capture/out/states` (fuera de git). Si falta `hyperframes/node_modules`, `build.sh` lo instala (o se puede enlazar al de `../ImperiOS Demo/hyperframes`).
