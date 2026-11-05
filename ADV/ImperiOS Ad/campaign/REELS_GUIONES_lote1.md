# Reels orgánicos — lote 1: guiones de las 3 piezas animadas (borrador para aprobar)

Mismo estilo que la campaña v4 (guía en `CAMPANA.md`): fondo #F7F7F3, Manrope, texto cinético sincronizado con la voz,
interfaz recreada, voz Cristina (eleven_v4, plan Starter). Todo el texto dentro de la zona segura de Reels.
Sin cifras inventadas ni marcas de portales. Cierre común: «Comenta DEMO» (coherente con las descripciones).

---

## R2 · «3 errores que te hacen perder leads» (~22 s) — formato consejo, para guardar

| Voz | En pantalla |
|---|---|
| Tres errores que te hacen perder leads en tu inmobiliaria. | **3 errores** que te hacen perder leads |
| Uno: contestar tarde. Quien pregunta por un piso muchas veces escribe a varias agencias, y la primera que responde se lleva la conversación. | **01 · Contestar tarde** — reloj corriendo; dos chats, uno responde antes |
| Dos: tener los leads repartidos entre portales, WhatsApp y Excel. Lo que no ves, no lo sigues. | **02 · Leads repartidos** — chips dispersos que se pierden |
| Tres: olvidarte de quien no compró. Hoy no encajaba, pero mañana puede entrar el piso que busca. | **03 · Olvidar a quien no compró** — ficha archivada que se ilumina con un match |
| Guárdalo y compártelo con tu equipo. | Guárdalo 🔖 · logo ImperiOS |

## R6 · «Antes / después» (~12 s) — formato contraste

| Voz | En pantalla |
|---|---|
| Antes: el lead en un portal, la conversación en WhatsApp, la visita en un Excel… y el recordatorio, en tu cabeza. | **ANTES** — pantalla dividida que se llena de ventanas, notas y avisos desordenados |
| Después: todo en un solo sitio. | **DESPUÉS** — todo se ordena en un panel limpio (leads, chat, agenda) |
| Imperios. Comenta DEMO y te lo enseño. | Logo + «Comenta DEMO» |

## R9 · «Lo que tienes que preguntar en el primer mensaje» (~20 s) — formato checklist

| Voz | En pantalla |
|---|---|
| Cuatro preguntas para el primer mensaje con un lead. | **4 preguntas** para el primer mensaje |
| Zona: dónde quiere vivir. | ☐→☑ **Zona** · pin en el mapa |
| Presupuesto: cuánto puede invertir. | ☐→☑ **Presupuesto** · barra de rango |
| Tipo: piso, ático o chalet, y cuántas habitaciones. | ☐→☑ **Tipo y habitaciones** |
| Plazo: cuándo quiere mudarse. | ☐→☑ **Plazo** · calendario |
| Con estas cuatro respuestas ya puedes cruzarlo con tu cartera. Y con Imperios, ese cruce lo hace la IA. | Las 4 casillas se unen en la tarjeta «Match con IA» |
| Guárdalo para tu equipo. | Guárdalo 🔖 · logo ImperiOS |

---

### Producción
- Voz: 3 tomas únicas en el plan Starter (≈1.500 créditos en total de 40.000) + tiempos con Scribe.
- Motor: escenas nuevas en un motor derivado de `preview/src/reel-v4.html` (misma paleta, tipografía y movimiento).
- Portada de cada uno con la plantilla `preview/src/portada-reel.html` (versión clara aprobada).
- Descripción corta + cierre «¿Tienes una inmobiliaria y tu operativa es un caos? Comenta DEMO…».

---

## R9 (nuevo, 27/10/2026) · «¿Y si la vendes antes de publicarla?» — módulo Match, formato radar (~33 s)

Sustituye al R9 «4 preguntas». Formato nuevo, en oscuro: la cartera de clientes como puntos de un radar.

| Voz | En pantalla |
|---|---|
| ¿Y si vendes tu próxima propiedad antes de publicarla en el portal? | Logo + «CRM PARA INMOBILIARIAS»; titular palabra a palabra; el botón «Publicar en el portal» pasa a «Todavía no.» |
| Tienes una cartera de clientes de hace años. Gente que buscaba casa… y no encontró la suya. | Aparecen los anillos y la cartera como puntos; se apagan |
| Hoy te entra una propiedad nueva. | Cae la ficha «Ático · Chamberí · NUEVA» con onda |
| Con el match de Imperios, la inteligencia artificial la cruza con toda tu cartera: zona, presupuesto, tipo y habitaciones. | Barrido del radar con pings; chips de los 4 criterios |
| Y te dice qué clientes encajan. Aunque haga años que no hablas con ellos. | Se encienden 3 clientes en amarillo con «hace 2 años / 8 meses / 3 años» |
| Los reactivas en un clic… y se la ofreces antes que nadie. | Fichas de los 3 + botón «Reactivar a los 3» con clic; «Aún no está publicada en el portal» |
| ¿Cuántos clientes tienes olvidados en tu cartera? Comenta demo y te enseño cómo funciona. | Pregunta + logo blanco + botón «Comenta DEMO» |

Motor `preview/src/reel-r9.html`, tiempos `preview/build_timeline_r9.py`, render `preview/build_r9.sh`.
Música en Fa# menor a 110 BPM con pings de radar (distinta del R2/R6). Subtítulos frase a frase con la palabra clave en amarillo.

---

## R10 (31/10/2026) · «¿Qué campaña te trae clientes?» — módulo de marketing, formato embudos en claro (~30 s)

Funciones confirmadas por Brian: medir campañas (clientes por campaña, ranking), crear y lanzar campañas desde el CRM y
métricas de rendimiento de las campañas de anuncios. No se nombra a la plataforma de anuncios; datos marcados «DATOS DE EJEMPLO».

| Voz | En pantalla |
|---|---|
| ¿Sabes qué campaña te trae clientes… y cuál solo se come tu presupuesto? | Logo + «CRM PARA INMOBILIARIAS»; titular palabra a palabra; lluvia de monedas |
| Tienes tres anuncios funcionando a la vez. Todos gastan. | Tres embudos (Ático · Chamberí, Captación propietarios, Pisos · Retiro) tragando monedas; contadores de gasto |
| Pero no todos traen clientes. | Del primero salen 5 clientes, del tercero 2; por el segundo se escapan las monedas: «✕ 0 clientes» |
| Con Imperios, cada cliente entra con su campaña de origen. Y ves el rendimiento de todas en el mismo panel. | Panel oscuro: clientes con su etiqueta de campaña → tabla de rendimiento (gasto, clientes, coste por cliente) |
| Así sabes cuál funciona… y dónde poner tu presupuesto. | Ranking: «LA MEJOR» / «REVISAR»; las barras de presupuesto se mueven a la campaña buena |
| Y la siguiente campaña, la lanzas desde el propio CRM. | Ficha «Nueva campaña» (Piso · Salamanca) → clic en «Lanzar campaña» → «Campaña activa» |
| ¿Sabes cuál de tus campañas funciona mejor? Comenta demo y te enseño cómo medirlo. | Pregunta + logo + botón negro «Comenta DEMO» |

Motor `preview/src/reel-r10.html`, tiempos `preview/build_timeline_r10.py`, render `preview/build_r10.sh`, portada `preview/src/portada-r10.html`.
Música en Si bemol mayor a 104 BPM con «clinc» de monedas.

## Carrusel · «Las 4 métricas que tienes que mirar en tus campañas» (31/10/2026)

6 diapositivas 1080×1350 (`preview/src/carrusel-metricas.html#1…6` → `preview/out/carruseles/metricas/`):
portada · 01 coste por cliente · 02 clientes por propiedad · 03 del clic al cliente (alcance → clics → clientes) · 04 cuándo apagarla · cierre (ranking + Comenta DEMO).

---

## R11 (01/11/2026) · «Falso interés» — calificación con IA, formato criba en oscuro (~36 s)

Confirmado por Brian: el contacto responde a unas preguntas que le hace la IA para calificarlo. Las preguntas que se ven
(presupuesto, plazo, zona, financiación) son de ejemplo; «20, 30, 50 al día» es la situación del espectador, no un dato de ImperiOS.

| Voz | En pantalla |
|---|---|
| ¿Tu equipo pierde la mañana contestando a gente que solo pregunta por preguntar? | Titular + avisos «Portal · nuevo mensaje» que se apilan |
| Te escriben veinte, treinta, cincuenta personas al día desde los portales. Y muchas, sin intención real de comprar. | Contador 20 → 30 → 50 y avalancha de burbujas («¿Sigue disponible?», «Info»…) que se apagan |
| Tu equipo contesta a todos igual. Y mientras, el que de verdad quiere comprar… espera. | Bandeja sin filtrar, todo «✓ Respondido»; abajo el interesado («Tengo la hipoteca aprobada») con el contador de espera |
| Con Imperios, la inteligencia artificial le hace a cada contacto unas preguntas clave para calificarlo. | 4 capas con las preguntas de la IA; los contactos se quedan en cada capa y solo pasan 3 |
| Así separas a los curiosos de los que están interesados de verdad. | Columnas Curiosos 22 · Templados 5 · Interesados 3 |
| Y tus comerciales saben a quién llamar primero. | «Prioridad de hoy» con 3 clientes y clic en «Llamar» |
| ¿Cuánto tiempo pierde tu equipo con el falso interés? Comenta demo y te enseño cómo filtrarlo. | Pregunta + logo + Comenta DEMO |

Motor `preview/src/reel-r11.html`, tiempos `preview/build_timeline_r11.py`, render `preview/build_r11.sh`, portada `preview/src/portada-r11.html`.

## R12 (01/11/2026) · «Red flags de una inmobiliaria desorganizada» — sin voz, texto al ritmo (~19 s)

Pensado para verse en bucle y generar comentarios («¿Cuántas te pasan? Comenta tu número»). 124 BPM; cada flag 4 tiempos,
fondos negro / amarillo / crema alternos. Flags: Excel que solo entiende uno · «¿Quién tenía la visita de las 17:00?» ·
contestas al día siguiente · notas en un pósit · nadie sabe qué anuncio trae clientes · el comercial se va y sus clientes también.
Cierre «Con ImperiOS, ninguna.» + Comenta DEMO. Motor `preview/src/reel-r12.html`, `build_timeline_r12.py`, `build_r12.sh`.

**R12 v2 (02/11/2026):** mini escena por flag (Excel con #REF!, chat del equipo, «Gracias, ya encontré otro», pósits que caen,
anuncios con «¿?», la cartera de Marcos que se vacía), cinta «RED FLAG» en el título y en cada transición, selector 1–6 en la
pregunta y las 6 banderas que se convierten en ✓ en el cierre.

---

## R13 (02/11/2026) · «El panel del CEO» — Reel + anuncios, oscuro (~47 s; corte de anuncio ~25 s)

Guion aprobado por Brian (con sus cambios: «en qué es mejor cada uno»; campañas publicitarias con inversión, clics en los
anuncios, leads en directo y notificación de cada lead nuevo; reunión de fin de mes con el equipo de marketing).
Gancho: móvil del CEO con notificaciones que saltan alrededor desde el primer fotograma → móvil / tablet / ordenador →
embudo consultas → visitas → ofertas por propiedad → comerciales y «MEJOR EN…» → campañas (gráfica con inversión, clics y leads;
aviso de lead nuevo dentro del panel; reunión tachada) → documentación, facturación y seguimiento → «Si puedes medirlo… puedes escalarlo».
Versiones: `imperios-r13-panel-ceo-A` (Reel, Comenta DEMO), `-B` (anuncio, Pide tu demo), `-corto` (anuncio ~25 s).
Motor `preview/src/reel-r13.html`, tiempos `preview/build_timeline_r13.py`, render `preview/build_r13.sh A|B|corto`.

## Carrusel · «¿Qué nivel de organización tiene tu inmobiliaria?» (05/11/2026)

6 diapositivas 1080×1350 (`preview/src/carrusel-niveles.html#1…6` → `preview/out/carruseles/niveles/`):
portada con la escalera de 4 niveles · nivel 1 «Todo en la cabeza» · nivel 2 «Papeles y chats sueltos» ·
nivel 3 «Excel y mil herramientas» · nivel 4 «Todo conectado y medido» (en negro) · cierre «¿En qué nivel estás tú? Comenta tu número» + Comenta DEMO.
