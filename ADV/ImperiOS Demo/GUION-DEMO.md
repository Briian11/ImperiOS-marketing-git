# ImperiOS — Vídeo demo del CRM · Guion v4 (aprobado para producción)

> v2: el punto 10 se divide en rendimiento por propiedad y por comercial.
> v3: escena de Marketing; el rendimiento por propiedad usa la página de métricas de cada inmueble.
> v4: ~3:00. Fuera Automatizaciones y Documentos; ficha de cliente y agenda más cortas; cierre sin CTA; subtítulos y música muy leve; la tarjeta del tablero de leads se mueve de verdad (permiso del usuario).

**Formato:** 16:9, 1920×1080, 60 fps · **Duración:** ~3:00 · **Tono:** demostración guiada, no anuncio.
**Imagen:** pantallas reales de la cuenta demo capturadas a 2x (cada estado de la interacción: antes y después de cada clic), animadas en HyperFrames dentro de una ventana de navegador: cursor con onda de clic, desplazamientos y zoom suaves, foco con anillo amarillo `#FFD500`, etiqueta de sección, barrido a oscuro en la escena de IA, rótulos en Manrope.
**Audio:** voz de Cristina (ElevenLabs) · subtítulos incrustados sincronizados palabra a palabra · música en código muy leve · máster −14 LUFS / −1 dBTP.

| # | Escena | Locución (VO) | Qué se ve / interacción |
|---|---|---|---|
| 0 | Intro | Esto es ImperiOS, el CRM pensado para inmobiliarias. Te enseñamos cómo se trabaja con él en el día a día. | Logo → la ventana del CRM se abre desde el centro con el Dashboard |
| 1 | Dashboard | Nada más entrar, el panel te resume el día: propiedades publicadas, contactos sin atender, clientes activos y las próximas citas de tu equipo. | Foco en los 4 KPI → «Contactos sin atender» → «Próximas citas» |
| 2 | Contactos | Cada contacto que llega de Idealista, Fotocasa, WhatsApp o tu web entra solo en Contactos, con su origen, su temperatura y su estado. Y los filtras en un clic. | Tabla (foco en la columna Fuente) → clic en el filtro «Fuente» → Idealista → tabla filtrada |
| 3 | Chat | Desde el Chat respondes a todos tus leads de WhatsApp en un mismo sitio, con la propiedad que les interesa siempre a la vista. Y si quieres, el asistente con inteligencia artificial contesta por ti. | Lista de leads → clic en el primero → conversación con la propiedad de interés |
| 4 | Ficha de cliente | Cuando un contacto pasa a cliente, su ficha guarda lo que busca: presupuesto, zonas y tipo de inmueble, junto a sus citas y seguimientos. | Detalle del cliente: preferencias y citas |
| 5 | Propiedades y Publicaciones | En Propiedades tienes tu cartera completa. Cada ficha te avisa de lo que falta para publicar en cada portal, y en Publicaciones ves dónde está anunciado cada inmueble. | Listado con fotos → ficha (foto + «Requisitos» por portal) → Publicaciones |
| 6 | Coincidencias IA | Aquí entra la inteligencia artificial: cruza lo que busca cada cliente con tu cartera y puntúa cada coincidencia, para que sepas a quién llamar primero y con qué propiedad. | Barrido a oscuro → tarjetas de coincidencia (100 pts) → pestaña «Por propiedad» |
| 7 | Agenda | Las visitas, firmas y valoraciones de todo el equipo se organizan en el Calendario, y las tareas, en un tablero. | Calendario mes → semana → tablero de tareas |
| 8 | Marketing | Si haces publicidad en Facebook e Instagram, en Marketing ves cuánto inviertes y qué te devuelve cada campaña: impresiones, clics, leads y coste por lead. Puedes bajar hasta cada conjunto y cada anuncio para saber cuál funciona mejor. Y los leads de tus campañas entran al instante en el CRM, en un tablero donde cambias su estado para tenerlos controlados en todo momento. | KPI del periodo → tabla de campañas → campaña («Del anuncio al lead», conjuntos) → conjunto (tabla de anuncios, foco en el mejor CPL) → «Leads de campaña» en tablero → **una tarjeta se arrastra de «Contactado» a «Interesado» (acción real)** |
| 9 | Rendimiento por propiedad | Cada inmueble tiene su propio registro. En Métricas ves el rendimiento de toda tu cartera, y si entras en una propiedad, tienes su historia completa: cuántas personas se han interesado y desde qué portal, cuántas visitas se han realizado y cuántas han querido lanzar una oferta. Incluso por qué la descartan y por qué se cancelaron las visitas. | «Rendimiento por propiedad» (Contactos · Visitas · Ofertas) → clic en una propiedad (periodo «Todo») → KPI → embudo → contactos por semana y portal → visitas → por qué la descartan / cancelaron |
| 10 | Rendimiento por comercial | Y si diriges la agencia, en Dirección tienes el rendimiento de cada comercial: su embudo de la noticia al cierre, sus llamadas y visitas, cómo va frente a sus metas del mes y lo que ha facturado. | Dirección → «Reporte comercial» (embudo + tabla por comercial) → «Metas del mes» → «Facturado» |
| 11 | Cierre | ImperiOS. Todo tu negocio inmobiliario, conectado. | Logo (sin CTA) |

Locución: ~400 palabras, ~2.450 caracteres → ~2:50 de voz + respiraciones entre escenas ≈ 3:00.

## Fuera de cuadro siempre

- Ajustes → Agente IA (clave de API), Portales (Publisher ID de Fotocasa) y Equipo (email de «Brian AGENTE»).
- Email de la cuenta: se oculta automáticamente (texto transparente sobre su propio fondo).
- Botón flotante del engranaje: se oculta al capturar.
- Se evita hacer zoom sobre registros `TEST-00x` / «de prueba», el aviso ámbar de Marketing, «A quién ha llegado» y textos en inglés mientras sigan en la cuenta demo.

## Capturas

`ADV/ImperiOS Ad/capture/demo-shots.mjs` (pantallas sueltas) y `demo-states.mjs` (estados de cada interacción + posiciones de los elementos) guardan en `capture/out/` (fuera de git).
