# Kit de marca para redes — ImperiOS

Este kit parte de la landing real. La fuente de verdad de colores y tipografía es `src/styles/global.css`; el logotipo procede de `public/logo-imperios*.png`. La referencia antigua `DOCUMENTACION/paleta_colores_tech.html` usa otro amarillo (`#E8D72A`): **para redes usamos el amarillo de la web actual, `#FFD500`**. El logotipo fuente de `public/` tenía un degradado amarillo distinto. En `assets/` hay una variante para redes que conserva su forma y pone la «i» en `#FFD500`; las plantillas usan esta variante. En el kit el acento aparece en detalles y controles, como en la landing, en vez de cubrir grandes bloques.

## Identidad visual

- **Personalidad:** tecnológica, clara y directa; útil para inmobiliarias, sin efectos recargados ni promesas grandilocuentes.
- **Contraste base:** fondo gris muy claro `#F5F5F5` con texto casi negro `#0A0A0A`; alternar con piezas oscuras `#0A0A0A` y texto blanco.
- **Acento:** amarillo `#FFD500` para una palabra, una línea, un punto de flujo o una llamada a la acción. El amarillo de interacción es `#E6C000`.
- **Ritmo visual:** cuadrícula sutil de 40 px, esquinas redondeadas, tarjetas con borde fino, numeración `01 / 05`, etiquetas en mayúsculas y espacios amplios.
- **Motivos del producto:** flujos de portales/campañas/web hacia un panel, tarjetas de datos, paneles oscuros y pequeños indicadores amarillos.
- **Logo:** usar la variante cromática de `assets/logo-imperios-navbar.png` o `.svg` y el icono `assets/logo-imperios.png` o `.svg`. La versión horizontal negra va sobre fondo claro; sobre fondo oscuro, colócala dentro de una placa clara. No deformar el símbolo.

## Paleta exacta de la web

| Token | Hex | Uso sugerido |
| --- | --- | --- |
| ink-950 | `#0A0A0A` | Titulares, fondos oscuros |
| ink-900 | `#1C1C1C` | Tarjetas sobre fondo oscuro |
| ink-800 | `#333333` | Bordes y superficies oscuras |
| ink-700 | `#4A4A4A` | Texto secundario sobre claro |
| ink-600 | `#727272` | Metadatos, etiquetas secundarias |
| ink-500 | `#B0B0B0` | Elementos suaves |
| ink-400 | `#C0C0C0` | Texto secundario sobre oscuro |
| ink-300 | `#D4D4D4` | Bordes claros visibles |
| ink-200 | `#EBEBEB` | Separadores claros |
| ink-100 | `#F5F5F5` | Fondo principal |
| ink-50 | `#FAFAFA` | Tarjetas claras |
| accent-500 | `#FFD500` | Acento principal |
| accent-600 | `#E6C000` | Acento secundario |

El blanco puro `#FFFFFF` se usa como texto sobre negro y, puntualmente, en superficies. La paleta completa también está en `tokens.json`.

## Tipografía

La landing usa **Manrope Variable** para títulos y cuerpo. Incluimos el archivo latino WOFF2 y su licencia OFL en `assets/`. Para piezas en Canva o Figma, selecciona/instala **Manrope**; si importas un SVG y la herramienta reemplaza la fuente, vuelve a asignarla allí.

- Titular: Manrope 700 en la línea principal; énfasis puntual en 500 cursiva. Las plantillas ya siguen esta pauta.
- Texto: Manrope 400–500, frases cortas y legibles en móvil.
- Etiquetas y cifras pequeñas: Manrope 700 con espaciado amplio; en la web algunos números usan una fuente monoespaciada del sistema.
- El **wordmark** es el logo original; no conviene reconstruirlo escribiendo “ImperiOS” con Manrope.

El titular «Todo conectado. / De principio a fin.» de la sección Producto usa Manrope Variable, color `#0A0A0A`, interlineado `1.06` y espaciado `-0.035em`. «Todo conectado.» va en **700 normal**; «De principio a fin.» en **500 cursiva**. Tamaños: **36 px** en móvil, **48 px** desde 640 px y **54 px** desde 1024 px. La fuente incluida solo aporta estilo normal, de modo que el navegador sintetiza esa cursiva. `tipografia.css` reproduce esta configuración para reutilizarla.

## Componentes y plantillas entregados

- `components/etiqueta.svg`: chip amarillo.
- `components/origen-lead.svg`: chip de una fuente de captación.
- `components/tarjeta-dato.svg`: tarjeta de cifra con marcador `XX` para completar solo con datos verificados.
- `components/panel-oscuro.svg`: tarjeta de interfaz reutilizable.
- `templates/instagram-portada.svg`: portada de carrusel vertical claro, 1080 × 1350 px.
- `templates/instagram-interior.svg`: lámina interior oscura, 1080 × 1350 px.
- `templates/vertical-portada.svg`: portada o primer fotograma para Reels/TikTok, 1080 × 1920 px.

Los SVG incluyen la variante del logotipo con la «i» en `#FFD500` y la fuente latina para que puedan abrirse sin rutas externas. El texto y las formas siguen siendo editables. Al importarlos en una herramienta de diseño, verifica la fuente antes de exportar. `exports/` contiene PNG de las tres plantillas para previsualizar o usar directamente; las variantes PNG y SVG del logo están en `assets/`.

## Cómo producir un feed coherente

1. Crea series de 4–6 láminas: portada con una idea, problema real, visual de la solución, beneficio concreto y cierre con CTA.
2. Alterna portadas claras y oscuras, conservando el logo, la numeración, la cuadrícula y el acento amarillo.
3. Usa **una idea principal por lámina**. Evita pantallas cargadas de texto; el detalle va en el copy del post.
4. Para vídeo vertical, usa `vertical-portada.svg` como punto de partida y anima titulares y tarjetas con entradas suaves; mantén el contenido clave lejos de los bordes y controles de la app.
5. Sustituye las frases de ejemplo y exporta PNG/JPG para carruseles o un vídeo para Reels/TikTok. Revisa el recorte final dentro de cada plataforma.

**Primeras series sugeridas:** “Todos tus leads en un lugar”, “Qué hace el Match con IA”, “Así avanza una visita” y “Qué puede ver cada agente”. Evita publicar las cifras de la sección Resultados (`6×`, `80 %`, `30 s`, `60 %`) o el testimonio atribuido a Magnus sin confirmar fuente, periodo y aprobación del cliente.

Los tamaños del kit son lienzos de trabajo. TikTok recomienda 9:16 para vídeo vertical y avisa de zonas cubiertas por la interfaz; Meta recomienda 9:16 y elementos clave dentro de la zona segura para Reels. Las reglas de publicación pueden variar, así que comprueba el recorte al subir cada pieza. Fuentes: https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads?lang=en-GB y https://www.facebook.com/business/ads/facebook-instagram-reels-ads.
