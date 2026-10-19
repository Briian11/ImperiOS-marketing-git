# ImperiOS — Vídeo demo del CRM · Guion v1 (propuesta)

**Formato:** 16:9, 1920×1080, 60 fps · **Duración:** ~2:45 · **Tono:** demostración guiada («así se trabaja con ImperiOS»), no anuncio.
**Imagen:** grabaciones reales de la cuenta demo (navegación, filtros, pestañas, fichas) a 1920×1080 nativo, dentro de una ventana de navegador animada.
**Capa propia (HyperFrames + GSAP), mismo lenguaje que el anuncio:** etiqueta de sección («02 · CONTACTOS»), cursor animado con onda de clic, zoom y foco con anillo amarillo `#FFD500` sobre lo que se explica, barrido circular a oscuro en la escena de IA, rótulos cinéticos en Manrope, cierre con logo.
**Voz:** Cristina (ElevenLabs), tono explicativo, ~2.000 caracteres. Subtítulos y música suave opcionales.

| # | Tiempo | Escena | Locución (VO) | Qué se ve / interacción | ¿Modifica datos? |
|---|---|---|---|---|---|
| 0 | 0:00–0:07 | Intro | «Esto es ImperiOS, el CRM pensado para inmobiliarias. Te enseñamos cómo se trabaja con él en el día a día.» | Logo → la ventana del CRM se abre desde el centro | No |
| 1 | 0:07–0:18 | Dashboard | «Nada más entrar, el panel te resume el día: propiedades publicadas, contactos sin atender, clientes activos y las próximas citas de tu equipo.» | Foco en los 4 KPI → «Contactos sin atender» → «Próximas citas» | No |
| 2 | 0:18–0:32 | Contactos | «Cada contacto que llega de Idealista, Fotocasa, WhatsApp o tu web entra solo en Contactos, con su origen, su temperatura y su estado. Y los filtras en un clic.» | Tabla; abrir el filtro «Fuente» → Idealista | No (filtro) |
| 3 | 0:32–0:48 | Chat | «Desde el Chat respondes a todos tus leads de WhatsApp en un mismo sitio, con la propiedad que les interesa siempre a la vista. Y si quieres, el asistente con IA contesta por ti.» | Lista de leads → abrir la conversación de un lead | No (solo abrir) |
| 4 | 0:48–1:01 | Ficha de cliente | «Cuando el contacto pasa a cliente, su ficha guarda lo que busca: operación, presupuesto, zonas y características, además de sus citas y seguimientos.» | Detalle del cliente: preferencias, citas, seguimientos | No |
| 5 | 1:01–1:17 | Propiedades y Publicaciones | «En Propiedades tienes tu cartera completa. Cada ficha te avisa de lo que falta para publicar en cada portal, y en Publicaciones ves dónde está anunciado cada inmueble.» | Listado con fotos → ficha → «Requisitos» por portal → Publicaciones (Web/Fotocasa/Idealista) | No |
| 6 | 1:17–1:33 | Coincidencias IA | «Aquí entra la inteligencia artificial: cruza lo que busca cada cliente con tu cartera y puntúa cada coincidencia, para que sepas a quién llamar primero y con qué propiedad.» | Barrido a oscuro → pestañas Calientes / Por propiedad / Por cliente → tarjeta 100 pts | No · **«Analizar con IA» solo con permiso** |
| 7 | 1:33–1:52 | Calendario, Tareas, Seguimientos | «Las visitas, firmas y valoraciones de todo el equipo están en el Calendario. Las tareas se organizan en un tablero y los seguimientos te recuerdan a quién volver a llamar.» | Calendario Mes → Semana; tablero de tareas; lista de seguimientos | No (cambiar de vista) |
| 8 | 1:52–2:04 | Automatizaciones | «Y por WhatsApp, ImperiOS manda solo los recordatorios de cita, vuelve a contactar a quien lleva días sin responder y pregunta qué tal fue la visita.» | Ajustes → WhatsApp: interruptores de recordatorios 24 h / 2 h, re-contacto, control de calidad (solo mirar) | No |
| 9 | 2:04–2:17 | Documentos | «Las hojas de visita, las propuestas de compra y los encargos de venta se generan desde el CRM y se firman en el momento.» | Documentos → plantillas → previsualización de la Hoja de visita | No |
| 10 | 2:17–2:38 | Dirección y métricas | «Y si diriges la agencia, tienes el embudo de todo el equipo, las metas del mes, lo facturado y qué portales y campañas te traen más clientes.» | Dirección (Reporte comercial, Metas, Facturado) → Métricas (leads por procedencia) → Marketing | No (pestañas) |
| 11 | 2:38–2:48 | Cierre | «ImperiOS. Todo tu negocio inmobiliario, conectado. Pide tu demo en imperios.app.» | Logo + CTA | No |

Módulos vistos y no incluidos en esta versión (se pueden añadir o cambiar por otros): Prospectos, Reporte diario, Email (sin cuenta conectada), Clientes (listado), Agencia y Google Calendar en Ajustes.

## Fuera de cuadro siempre

- Ajustes → **Agente IA** (muestra parte de la clave de API de Anthropic), **Portales** (Publisher ID de Fotocasa) y **Equipo** (email de «Brian AGENTE»).
- Email de la cuenta: se tapa automáticamente en capturas y grabaciones.

## Pendiente antes de grabar

1. **Permitir `images.unsplash.com`** en *Allowed domains* (las fotos de los inmuebles vienen de ahí y ahora no cargan).
2. **Limpieza de la cuenta demo**, ahora que las pantallas salen completas:
   - nombre del usuario del pie del menú («Brian») → p. ej. «Laura · Demo» (o se oculta el pie con CSS al grabar);
   - inmuebles y documentos `TEST-00x` / «de prueba» / «Piso de prueba con campos nuevos»;
   - «MAGNUS REAL ESTATE» y «AGENCIA EXTRAMUROS 2021 S.L.» en descripciones y en la plantilla de la Hoja de visita (¿empresas reales?) → nombre ficticio;
   - títulos con errata «Piso en de …»;
   - notificaciones «Error en IDEALISTA» y aviso rojo de conexión con Meta;
   - textos en inglés: «Settings / Manage your account settings…», migas «Management», «Follow Ups», «Objectives», «Visit Sheet».
   El botón flotante del engranaje se oculta con CSS durante la grabación.
3. **Permiso para acciones que cambian datos** (opcional; el guion v1 funciona sin ellas): «Analizar con IA» (¿consume créditos de API?), agendar una cita, mover una tarea en el tablero. Ninguna acción que envíe WhatsApp o emails.
4. Confirmar voz (Cristina), subtítulos sí/no, música sí/no y CTA final.
