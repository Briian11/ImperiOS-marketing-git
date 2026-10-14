# Brief — versión «producto real» (HyperFrames)

Mismo guion, voz y mezcla que la campaña con voz (Cristina, toma 1, gancho A), pero la imagen pasa de UI recreada a **pantallas reales de la cuenta demo** del CRM, con zoom, foco y resaltado amarillo animados encima. Gancho, transiciones y cierre siguen siendo animación propia.

- Formato: 1080×1920, 60 fps, 28,2 s. Composición: `index.html` (una sola composición GSAP).
- Audio: `preview/out/campaign-vo/audio/master.wav` tal cual (−14 LUFS / −1 dBTP, música ~22 dB bajo la voz). Los cortes de escena caen en los mismos tiempos que la versión anterior, así que los SFX siguen sincronizados.
- Subtítulo cinético palabra a palabra con los tiempos de `assets_in/vo/campana-toma-1.words.json` (+0,2 s de desfase de la mezcla). Palabras clave con subrayado amarillo.
- CTA: «Pide tu demo» (por defecto, pendiente de confirmar) + `IMPERIOS.APP ↗`.

## Escenas

| Tiempo | Escena | Frase de la VO | Pantalla real (placa) | Animación propia encima |
|---|---|---|---|---|
| 0–3,86 | Gancho | ¿Tus leads se pierden entre portales, WhatsApp y Excel? | — | Texto cinético + fichas de canales que flotan y se absorben |
| 3,86–6,72 | 01 · Un solo panel | Con Imperios, todos entran en un solo panel, | Contactos: nombres + Fuente/Temperatura/Estado | Filas que entran una a una; foco en la columna Fuente |
| 6,72–8,55 | 02 · Campañas | y ves qué campaña funciona. | Métricas (leads por procedencia) + KPIs de Marketing | Zoom al pico de Idealista; tarjeta «Coste por lead −42,2 %» ampliada |
| 8,55–12,95 | 03 · Match con IA | La inteligencia artificial cruza zona, tipo y presupuesto con tu cartera. | Coincidencias: cabecera, pestañas y tarjeta 100 pts | Barrido a oscuro; criterios Zona/Tipo/Presupuesto; anillo en la puntuación |
| 12,95–16,95 | 04 · Reactivar | Y cuando hay match, reactivas al cliente con una oportunidad real. | Campana, «Nueva coincidencia», tarjeta notificada | Campana que vibra; resaltado del aviso; foco en «Notificado» y «Ya se le envió esta propiedad» |
| 16,95–21,55 | 05 · Agenda | Visitas, recordatorios y agentes, coordinados desde la misma agenda. | Calendario del mes | Acercamiento a la semana de hoy; «Recordatorio enviado»; «3 agentes» |
| 21,55–24,95 | 06 · Imperios | Imperios. Todo conectado, de principio a fin. | Miniaturas de las 4 pantallas | Líneas amarillas y nodo central que las conecta |
| 24,95–28,2 | Cierre | Pide tu demo. | — | Logo + botón CTA + URL |

## Qué se deja fuera de cuadro (decisión del usuario: recortes y zoom)

`tools/make_plates.py` recorta las placas de `capture/out/*@2x.png` evitando: nombre y email del usuario (pie del menú), botón flotante de ajustes, columna de emails `@demo.ficticio`, teléfonos y referencias `TEST-00x` / «de prueba», el aviso rojo de conexión con Meta, las notificaciones «Error en IDEALISTA» y el subtítulo «prueba test» de la notificación. El avatar «RD» de la tarjeta se redibuja porque el original queda pegado a la línea del email.

## Construir

```bash
cd "ADV/ImperiOS Ad/hyperframes" && ./build.sh
```

Sale `renders/imperios-producto-real-v1_9x16.mp4` + contact sheet + medición de loudness.
