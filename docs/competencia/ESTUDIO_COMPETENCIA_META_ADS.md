# Estudio de competencia publicitaria — ImperiOS

**Análisis de anuncios de CRM inmobiliarios en Meta Ads Library (España)**

| | |
|---|---|
| Fecha del corte | 10/11/2026 |
| Fuente | Biblioteca de anuncios de Meta (capturas de pantalla) |
| Registros | 7 anuncios · 5 anunciantes (objetivo: ≥ 20 anuncios) |
| Datos estructurados | [`registro_anuncios_meta.csv`](registro_anuncios_meta.csv) |
| Estado | **v1 — muestra insuficiente.** La estrategia de la sección 6 es preliminar. |

**Leyenda:** **[OBS]** dato observado en la Ads Library · **[DER]** cálculo hecho sobre datos observados · **[HIP]** hipótesis o interpretación que hay que validar.

---

## 1. Ranking por alcance acumulado

| # | Anunciante | Alcance UE [OBS] | Inicio [OBS] | Días activo [DER] | Alcance/día [DER] | Precio u oferta [OBS] | Ángulo |
|---|---|---:|---|---:|---:|---|---|
| 1 | Qobrix | 80.433 | 16/07/2025 | 482 | 167 | No disponible | CRM + web + publicidad |
| 2 | eGO CRM España | 17.614 | 04/11/2026 | 6 | **2.936** | No disponible | CRM dentro de ChatGPT |
| 3 | eGO CRM España | 6.289 | 07/10/2026 | 34 | 185 | Desde 50 €/mes · 15 días gratis | CRM 360° |
| 4 | Grupo Gestyde | 3.023 | 03/11/2026 | 7 | 432 | 45 €/mes · usuarios ilimitados | Precio bajo |
| 5 | Inmovilla | 1.243 | 09/11/2026 | 1 | (1.243) | 569 € + IVA 1.er año + bonos | Promoción |
| 6 | Custom Soft Lab (Diego Álvarez González MKT) | 1.006 | 08/11/2026 | 2 | (503) | No disponible | SaaS a medida |
| 7 | Grupo Gestyde | 173 | 10/11/2026 | 5 horas | No calculable | Pago único 599 € | Sin cuotas |

**Cómo leer el alcance/día [DER]:** es alcance acumulado ÷ días transcurridos hasta el 10/11/2026. El alcance cuenta cuentas únicas, así que no crece de forma lineal: la cifra solo sirve para comparar **intensidad actual de difusión**, no rendimiento. Con 1–2 días de vida (#5, #6) es ruido. Ninguna cifra de esta tabla indica clics, leads, ventas ni rentabilidad.

**Lo que cambia respecto a leer solo el alcance acumulado:**
- Qobrix encabeza el ranking por acumulación de 16 meses, pero hoy difunde a ~167 cuentas/día.
- **eGO / ChatGPT es, con diferencia, la campaña con más empuje ahora** (~2.900 cuentas/día en su primera semana). [HIP] Es la que más presupuesto está recibiendo en este momento.
- Gestyde tiene en marcha a la vez dos modelos de precio (45 €/mes y 599 € de pago único). [HIP] Está probando qué oferta convierte mejor.

## 2. Análisis por anuncio (resumen)

Los textos completos de cada anuncio están en el CSV. Aquí solo va lo que aporta a la decisión.

| # | Propuesta de valor [OBS] | Qué hace bien [HIP] | Hueco que deja [HIP] |
|---|---|---|---|
| 1 Qobrix | «Una plataforma: web, anuncios y CRM». Captura automática de leads. | Promesa de «todo en uno» y de cerrar más operaciones; vídeo con varias versiones. | Mensaje genérico, sin precio y sin explicar qué pasa con el lead después de captarlo. |
| 2 eGO ChatGPT | «El primer CRM inmobiliario en ChatGPT». Consultar el CRM en lenguaje natural. CTA: demo. | Se apoya en una tecnología que todos conocen y lo dice en una frase. | La IA sirve **al agente** (para consultar datos), no **al cliente final** (atención, cualificación). |
| 3 eGO 360° | «Responder antes, organizar mejor, no perder oportunidades». 50 €/mes, 15 días gratis. | Precio de entrada visible y prueba gratuita: poca fricción. | Habla de «responder antes», pero no enseña cómo. |
| 4 Gestyde 45 € | 45 €/mes, sin límite de usuarios, para equipos que crecen. | Precio y argumento claros; enseña la interfaz real. | Compite solo por precio. |
| 5 Inmovilla | CRM + web + IA; 569 € el primer año + bono de Idealista + 3 meses de WhatsApp. | Persona hablando a cámara, urgencia y paquete de regalos. | Su WhatsApp se ofrece como **regalo temporal**, no como automatización de la atención. Fechas de la promo incoherentes con la fecha del anuncio. |
| 6 Custom Soft Lab | SaaS a medida; «el código y los datos son tuyos». | Explota el miedo a depender de un proveedor y a las subidas de precio. | Desarrollo a medida implica más tiempo de puesta en marcha y más coste inicial. |
| 7 Gestyde 599 € | Pago único; «¿sigues entre Excel, WhatsApp y varias herramientas?». | Dolor muy concreto (dispersión) y sin cuotas. | Demasiado reciente para sacar conclusiones. |

## 3. Patrones del mercado

| Patrón | Quién [OBS] | Lectura [HIP] |
|---|---|---|
| **Precio como gancho** | Gestyde (45 €/mes, 599 €), eGO (50 €/mes), Inmovilla (569 €/año) | El rango de referencia que ve el comprador en Meta está entre **45 y 50 €/mes**, o unos **600 € en pago único o primer año**. Si ImperiOS está por encima, tiene que justificarlo con resultados, no con funciones. |
| **«Todo en uno»** | Qobrix, eGO, Inmovilla, Gestyde | Es el mensaje más repetido y por tanto el que menos diferencia. |
| **IA** | eGO (ChatGPT), Inmovilla («CRM, web e IA») | La IA ya aparece en los anuncios, pero como función interna o como etiqueta. Nadie enseña una IA que **atienda y cualifique al cliente**. |
| **Dolor de la dispersión** | Gestyde #7 («Excel, WhatsApp y varias herramientas») | Coincide con los ganchos A y C de la campaña v4 de ImperiOS (ver `ADV/ImperiOS Ad/campaign/GANCHOS_v2.md`). Hay riesgo de sonar igual. |
| **Segmentación amplia** | Los 7: España, 18/20–65+, todos los géneros | Nadie segmenta por intereses visibles en la ficha. [HIP] Dejan que la creatividad filtre al público (decisores inmobiliarios). |
| **Captación** | Demo (eGO), prueba gratuita (eGO), «Descubre el CRM» (Gestyde), promo con fecha límite (Inmovilla) | Solo eGO pide demo de forma explícita. |

**Lo que nadie comunica en la muestra (oportunidad para ImperiOS) [HIP]:**
1. **Velocidad de respuesta automática al lead** por WhatsApp, a cualquier hora.
2. **Cualificación con IA** antes de que intervenga el agente.
3. **Agendamiento de la visita** sin intervención humana.
4. **Control de calidad después de la visita.**
5. **Resultado en visitas**, no en «gestión»: todos venden organización y ninguno vende «más visitas con los mismos leads».

## 4. Posicionamiento recomendado para ImperiOS

> **ImperiOS no solo guarda tus leads: los atiende, los cualifica y te los deja con la visita agendada.**

- **Contra el «todo en uno» (Qobrix, Inmovilla):** no se trata de tener todo en un sitio, sino de que el sistema trabaje mientras el agente vende.
- **Contra la IA de eGO:** su IA responde **al agente**; la de ImperiOS responde **al cliente**. Es la comparación más fuerte que tenemos y se puede comunicar sin citar a eGO.
- **Contra el precio (Gestyde, eGO):** no competir por cuota. Reencuadrar el coste: lo caro es el lead que no se atiende a tiempo. [HIP] Debe sostenerse con datos propios cuando existan; hasta entonces, plantearlo como pregunta y no como cifra.
- **Contra el desarrollo a medida (Custom Soft Lab):** funciona desde el primer día, sin meses de desarrollo. [Pendiente] Confirmar la política de exportación de datos de ImperiOS antes de usarla como argumento.

## 5. Ventaja que solo ImperiOS puede demostrar en el propio anuncio [HIP, alta prioridad]

ImperiOS se integra con los formularios de Meta Ads y atiende por WhatsApp. Por tanto, **el lead de la campaña de ImperiOS puede vivir el producto en primera persona**:

1. La inmobiliaria rellena el formulario instantáneo de Meta.
2. En menos de un minuto recibe un WhatsApp de la IA de ImperiOS, que le hace 2 o 3 preguntas de cualificación.
3. La IA le propone un hueco y deja la demo agendada.
4. En la demo, el comercial abre ese mismo registro: «Esto es lo que acaba de pasarte a ti, y es lo que les pasará a tus clientes».

Gancho asociado: *«Rellena el formulario y mira lo que ImperiOS hace con tus leads en menos de un minuto.»*

Ningún competidor de la muestra puede prometer esto en su anuncio. **Requisitos antes de lanzar:** que el flujo funcione de verdad de principio a fin, que haya consentimiento explícito para WhatsApp en el formulario y que la plantilla de WhatsApp Business esté aprobada. La integración formulario → CRM → WhatsApp puede montarse en n8n si la nativa no cubre algún paso.

## 6. Estrategia preliminar de Meta Ads (v0, a revisar con ≥ 20 registros)

### 6.1 Objetivo y embudo

**Objetivo de negocio:** demos agendadas que de verdad se celebren, no simples leads.

```
Impresión → Hook (3 s) → Clic / apertura del formulario → Lead → Contactado por WhatsApp
  → Cualificado → Demo agendada → Demo celebrada → Cliente
```

Optimizar Meta hacia el lead, pero **devolver a Meta la conversión de calidad** (demo agendada o cualificada) mediante la API de Conversiones, para que el algoritmo aprenda de los leads buenos y no de los baratos.

### 6.2 Estructura de campaña

| Bloque | Objetivo en Meta | Público | Reparto inicial del presupuesto [HIP] |
|---|---|---|---|
| **Prospección – test de ganchos** | Clientes potenciales (formulario instantáneo, «mayor intención») | Amplio: España, 25–65+, sin intereses; la creatividad filtra | 60 % |
| **Prospección – intereses** | Igual | Intereses relacionados: sector inmobiliario, agente inmobiliario, portales inmobiliarios, gestión inmobiliaria | 20 % |
| **Retargeting** | Clientes potenciales o conversiones | Visitantes de imperios.app, personas que vieron ≥ 50 % de un vídeo y quienes interactuaron en Instagram o Facebook (30–90 días) | 20 % |

Exclusiones: clientes actuales y leads de los últimos 30 días. Cuando haya ≥ 100 demos registradas, probar un público similar (lookalike) creado a partir de ellas.

### 6.3 Formulario instantáneo (cualificación)

1. ¿Cuántos agentes tiene tu inmobiliaria? (1 · 2–5 · 6–15 · +15)
2. ¿Cuántos leads recibes al mes, aproximadamente? (< 50 · 50–200 · +200)
3. ¿Con qué gestionas hoy los clientes? (Excel / WhatsApp · otro CRM · nada)
4. Teléfono y casilla de consentimiento para WhatsApp.

Pantalla final: «En un minuto te escribimos por WhatsApp para elegir hora».

### 6.4 Creatividades y ganchos

Se reutilizan las piezas de la campaña v4 (`ADV/ImperiOS Ad/campaign/CAMPANA.md`) y se añaden los ángulos que faltan.

| Ángulo | Gancho propuesto | Formato | Diferencia frente a la competencia | Pieza existente |
|---|---|---|---|---|
| **A. Pérdida** | «¿Cuántos clientes se le escapan cada mes a tu inmobiliaria?» | Reel 20–37 s | Nadie habla de pérdida; casi todos hablan de organización | v4 gancho B ✔ |
| **B. Velocidad** | «Son las 23:40 y un cliente pregunta por tu piso. ¿Quién le contesta?» | Reel 15–20 s con un chat recreado | Ataca el «responder antes» de eGO enseñándolo de verdad | Nueva |
| **C. IA que atiende** | «Hay CRM con IA para consultar tus datos. ImperiOS usa la IA para atender a tus clientes.» | Imagen estática o reel corto | Contraste directo con eGO / ChatGPT sin nombrarlo | Nueva |
| **D. Demo del flujo** | «Lead → WhatsApp → cualificado → visita agendada. Sin tocar nada.» | Reel con la interfaz recreada (guía de estilo v4) | Enseña el resultado, no las funciones | Parcial (v4 largo) |
| **E. Pruébalo en ti** | «Rellena el formulario y mira lo que ImperiOS hace con tus leads en menos de un minuto.» | Reel o estática | Solo lo puede prometer ImperiOS (sección 5) | Nueva |
| **F. Dispersión** | «¿Tus leads se pierden entre portales, WhatsApp y Excel?» | Reel | Ojo: Gestyde #7 usa casi el mismo dolor | v4 gancho A ✔ |
| **G. Persona a cámara** | Fundador o agente contando el problema en 15 s | Vídeo vertical | Inmovilla lo usa; añade confianza humana | Nueva |

Reglas que se mantienen de la guía v4: no usar cifras ni testimonios sin fuente, no usar capturas con datos reales, y decir «gratis» solo si la demo lo es.

### 6.5 Ofertas a probar

| Oferta | Cuándo usarla | Riesgo |
|---|---|---|
| Demo gratuita de 20 minutos con el flujo en directo | Por defecto | Baja fricción, intención media |
| «Diagnóstico de leads perdidos»: revisamos tu tiempo de respuesta actual | Para el ángulo de pérdida | Más intención, pero hay que entregar el diagnóstico |
| Prueba gratuita o primer mes rebajado | Solo si el modelo de negocio lo permite | Atrae curiosos y compite con eGO y Gestyde en su terreno |

**[Pendiente]** Precio de ImperiOS: no consta en el estudio. Hay que decidir si se muestra o no; la competencia ancla en 45–50 €/mes.

### 6.6 Plan de tests A/B (una variable cada vez)

| Test | Variable | Variantes | Hipótesis | Métrica de decisión |
|---|---|---|---|---|
| T1 | Gancho | A pérdida · B velocidad · C IA que atiende | El dolor concreto (B) supera al genérico (A) | Hook rate a 3 s y luego coste por lead |
| T2 | Formato | Reel · imagen estática · persona a cámara | En B2B local, el vídeo humano genera más confianza | Coste por demo agendada |
| T3 | Oferta / CTA | Demo · diagnóstico · «pruébalo en ti» (E) | E consigue mejor tasa de lead → demo | Tasa de lead → demo celebrada |
| T4 | Formulario | Volumen · mayor intención (con preguntas) | Menos leads, pero más baratos por demo | Coste por demo celebrada |
| T5 | Mostrar precio | Con precio · sin precio | Mostrarlo filtra a quien solo busca lo más barato | Coste por demo celebrada |

Orden: T1 → T2 → T3 → T4/T5. Cada test usa el mismo público y el mismo presupuesto por variante. Un ganador se declara con un mínimo acordado de conversiones por variante, no por intuición ni por los primeros días.

### 6.7 Métricas de evaluación

| Nivel | Métrica | Para qué sirve |
|---|---|---|
| Creatividad | Hook rate (reproducciones de 3 s ÷ impresiones), hold rate (ThruPlay ÷ reproducciones de 3 s), CTR | ¿Para el scroll el gancho y se entiende el mensaje? |
| Captación | CPL, tasa de apertura → envío del formulario | ¿Convierte la oferta? |
| Calidad | % de leads cualificados, % contactados en < 5 min, tasa de lead → demo agendada | ¿Atraemos a quien toca? |
| Negocio | Tasa de asistencia a la demo, tasa de demo → cliente, CAC, coste por demo celebrada | ¿Es rentable? |

**CPL máximo admisible** = valor del cliente en sus primeros 12 meses × tasa de demo → cliente × tasa de lead → demo × margen objetivo. Hay que calcularlo con los datos propios de ImperiOS; no se usan benchmarks externos.

Regla para apagar un anuncio [HIP]: si el gasto llega a 2–3 veces el CPL máximo sin ningún lead, o a 2–3 veces el coste máximo por demo sin ninguna demo, se apaga.

## 7. Cómo continuar la investigación (hasta ≥ 20 anuncios)

**Configuración:** https://www.facebook.com/ads/library/ · País: España · Todos los anuncios · Activos.

**Palabras clave:** CRM inmobiliario, software inmobiliario, software para inmobiliarias, IA inmobiliaria, automatización inmobiliaria, gestión inmobiliaria, CRM para agencias inmobiliarias, captación inmobiliaria, WhatsApp inmobiliaria, leads inmobiliarios.

**Marcas a buscar por nombre** (sin verificar si anuncian ahora; solo son candidatas): Witei, Mobilia, Sooprema, Inmoweb, Infocasa, Casafari, Statefox, Idealista Tools, Fotocasa Pro, Clientify y HubSpot (genéricos con vertical inmobiliaria). Revisar también todos los anuncios activos de Qobrix, eGO, Gestyde e Inmovilla: es posible que tengan más de los que aparecen en esta muestra.

**Seguimiento:** volver a capturar los 7 anuncios actuales el 17/11/2026 para calcular el **incremento semanal de alcance** [DER], que es más fiable que el acumulado. Anotar los que se hayan apagado: un anuncio que se apaga pronto suele ser uno que no funcionaba [HIP].

**Datos por anuncio:** las columnas del CSV. Si un dato no se ve, escribir «No disponible». Cada identificador de Meta es un registro; las variantes de una misma ficha se cuentan como versiones, no como anuncios distintos.

## 8. Limitaciones

- El alcance es estimado y acumulado, y cada anuncio lleva un tiempo distinto en circulación.
- No disponible: inversión, CPC, CPL, conversiones y ventas de la competencia.
- Mucho alcance no implica rentabilidad.
- La audiencia configurada no es necesariamente la audiencia real alcanzada.
- Precios y promociones según el anuncio; pueden haber cambiado.
- Fotografía de un momento concreto: 10/11/2026.
- 7 registros no son una muestra representativa; las conclusiones de las secciones 3 a 6 son hipótesis.

## Historial

| Versión | Fecha | Cambios |
|---|---|---|
| v1 | 10/11/2026 | 7 anuncios en el registro. Se añaden el alcance diario [DER], los huecos del mercado, el posicionamiento, la táctica de la sección 5 y la estrategia preliminar v0. |
