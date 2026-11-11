# Brief para Claude chat — producción visual con Higgsfield (ImperiOS)

> Pega o adjunta este archivo al empezar el chat (o súbelo al conocimiento del Proyecto).
> Es autosuficiente: no hace falta acceso al repositorio para trabajar con él.

## 1. Contexto

- **ImperiOS** (imperios.app): CRM para inmobiliarias. Reúne en un panel los leads de portales, web, campañas y WhatsApp,
  cruza clientes con la cartera usando IA (Match), califica contactos, coordina visitas y agentes y mide las campañas.
- Fundador: Brian. Cuenta de Instagram: @imperios.app. Público: directores y comerciales de inmobiliarias en España.
- Ya existen: anuncios v4 (3 ganchos × 2 duraciones), Reels R2, R6, R9, R10, R11, R12, R13 y dos carruseles.
  Todos se montan en código (interfaz del CRM **recreada** en HTML, texto cinético, voz Cristina de ElevenLabs).
- **Lo que falta y es para lo que sirve este chat:** imagen y vídeo realistas que el motor en código no puede hacer
  (personas, oficinas, pisos, situaciones del día a día) para usarlos como planos de apoyo, fondos y portadas.

## 2. Prueba ilimitada de Higgsfield

- Cuenta en prueba **Ultra ilimitada del MCP** hasta el **14/11/2026 a las 14:46 (hora de España)**. La renovación
  automática ya está cancelada: no se cobra nada al terminar.
- Las generaciones ilimitadas **solo funcionan desde Claude chat / Cowork**, no desde Claude Code.
- Fuera de la prueba solo hay 10 créditos: **no gastar créditos**. En cada generación, pasar `use_unlim: true`
  (o responder «ilimitadas» cuando la herramienta pregunte). Si un modelo no entra en la prueba, avisar antes de generar.
- Modelos que el catálogo marca como compatibles con ilimitado (comprobar con `models_explore` si hay más):
  - Vídeo: `seedance_2_0` (y probar `seedance_2_5`).
  - Imagen: `nano_banana_pro`, `nano_banana_2`, `nano_banana_2_1`, `gpt_image_2`, `soul_2`.

## 3. Reglas de marca (obligatorias)

- **Formato:** vertical 9:16 (1080×1920) para Reels y Stories; 4:5 o 3:4 (1080×1350) para el feed.
- **Paleta:** fondo crema `#F7F7F3` / gris `#F5F5F5`, negro `#0A0A0A`, amarillo `#FFD500` solo en detalles
  (nunca grandes superficies). Escenas «de IA» en fondo negro.
- **Estilo de imagen:** luz natural, limpio, contemporáneo, oficinas y pisos españoles reales; nada recargado ni «stock» exagerado.
  Para el «antes»: tonos desaturados y grises; para el «después»: luminoso y ordenado.
- **Sin texto dentro de las imágenes y vídeos** (el texto y la interfaz se añaden en el montaje).
- **Prohibido:** logos o marcas de portales inmobiliarios, copias de la interfaz de WhatsApp, capturas o datos reales
  de clientes, cifras de resultados o testimonios inventados, caras de personas reales conocidas.
- **Vídeo:** clips de 5 s, sin audio (`generate_audio: false`): la música y la voz se ponen en el montaje.
  Movimientos de cámara suaves; nada borroso en reposo.

## 4. Lista de planos (prioridad de arriba abajo)

Hacer primero **una imagen fija** de cada plano (barata y rápida), elegirla con Brian y después animarla con
`seedance_2_0` usando esa imagen como `start_image`.

| # | Pieza | Plano | Prompt base (adaptar) |
|---|---|---|---|
| 1 | R6 Antes/después — ANTES | Comercial agobiada en su mesa, móvil vibrando, portátil con muchas ventanas | Agente inmobiliaria de 35 años en una oficina pequeña en España, agobiada, mirando un móvil que no para de vibrar, portátil con muchas ventanas abiertas, pósits por la mesa, luz de tarde, tonos desaturados, plano medio, vertical 9:16, sin texto |
| 2 | R6 — ANTES | Pósit en el monitor | Primer plano de un pósit amarillo pegado en el borde de un monitor, letra a mano ilegible, oficina desordenada desenfocada, tonos grises, vertical, sin texto legible |
| 3 | R6 — ANTES | Visita fallida | Piso vacío en venta en Madrid, salón luminoso pero vacío, una agente esperando de pie junto a la ventana mirando el reloj, nadie llega, tonos fríos, vertical |
| 4 | R6 — DESPUÉS | La misma comercial, tranquila | La misma agente en una oficina ordenada y luminosa, sonriendo mientras revisa el portátil, café, plantas, luz de mañana, detalles amarillos sutiles, vertical |
| 5 | R6 — DESPUÉS | Visita que sí ocurre | Agente inmobiliaria recibiendo a una pareja joven en la puerta de un piso luminoso, apretón de manos, vertical, luz natural |
| 6 | R13 Panel del CEO | Director con el móvil | Director de una inmobiliaria de 45 años, de noche en su despacho, mirando el móvil con expresión de control y calma, ciudad iluminada al fondo, tonos oscuros, vertical |
| 7 | R11 Falso interés | Equipo saturado | Tres comerciales en una oficina inmobiliaria contestando mensajes en el móvil a la vez, ambiente de prisa, tonos neutros, vertical |
| 8 | Portadas / fondos | Interior de piso | Salón luminoso de un piso reformado en Madrid, ventanales, suelo de madera, sin personas, mucho espacio libre arriba para titular, vertical 9:16 |
| 9 | Portadas / fondos | Llaves | Primer plano de unas llaves de casa sobre una mesa de madera clara con un llavero amarillo, fondo crema desenfocado, espacio libre para texto, 4:5 |

Consistencia del personaje de los planos 1, 4 y 5: generar primero un retrato de la agente con `soul_2` y usarlo como
referencia en el resto (o crear un personaje reutilizable si la herramienta lo ofrece).

## 5. Ads Studio (opcional, sin gastar)

`ads_studio_create_brand` con `https://imperios.app` para que Higgsfield lea la web (logo, paleta, tono). Solo lectura.
**No lanzar** `ads_studio_generate` sin presupuesto aprobado: gasta créditos.

## 6. Cómo trabajar

1. Leer este brief. Proponer el orden y empezar por el plano 1.
2. Generar 2–4 variantes por plano y enseñárselas a Brian; no animar nada sin su elección.
3. Guardar todo en un proyecto de Higgsfield llamado **«ImperiOS — Reels nov 2026»** (una carpeta por pieza: R6, R13, R11, Portadas).
4. Al terminar, hacer una lista final: pieza, plano, modelo, job_id y URL de cada resultado elegido.

## 7. Vuelta a Claude Code

Las generaciones quedan en la misma cuenta de Higgsfield. En la sesión de Claude Code del repositorio se recuperan con
`show_generations`, se descargan a `ADV/ImperiOS Ad/assets_in/higgsfield/<pieza>/` y se montan en los motores de cada Reel.
Basta con pasarle la lista final del punto 6.
