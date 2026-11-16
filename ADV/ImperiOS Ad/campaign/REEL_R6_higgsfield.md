# Reel R6 · «Antes / después» con planos de Higgsfield — versión anuncio (12/11/2026)

Misma historia que el R6 (`REEL_R6_antes_despues.md`), pero con planos de vídeo realistas en el ANTES y en el cierre.
Voz Cristina (eleven_v4, plan Starter). Duración: ~43 s. CTA «Pide tu demo gratis» (es versión de anuncio).
Montaje: `preview/build_r6h.sh` → `preview/out/imperios-r6-higgsfield_9x16.mp4`.

## Guion (★ = frase nueva grabada el 12/11; el resto viene de las tomas del R6)

| Voz | Plano / escena | En pantalla |
|---|---|---|
| Así se pierde un cliente… | **T1** · plano 1, 0,0–2,1 s (teclea, móvil vibrando). Portada | Logo, «CRM PARA INMOBILIARIAS», gancho completo desde el fotograma 0 |
| …y así se gana. | **T2** · plano 5, 0,0–1,4 s (apretón de manos, a color). Adelanto del final | «gana» subrayado en amarillo |
| ★ Antes: mensajes y llamadas sin parar. | **T3** · plano 1, 2,1–5,0 s (deja el móvil, manos a la cara) | ANTES · «Mensajes y llamadas / sin *parar*.» |
| ★ La visita, apuntada en papel… | **T4** · plano 2, 0,2–2,8 s (agenda tachada) | «La visita, / en *papel*.» |
| ★ …y el cliente no se presenta. | **T5** · plano 3, 0,1–3,3 s (sola en el piso, mira el reloj) + zoom lento | «Y el cliente / no se *presenta*.» + sello «NO SE PRESENTÓ» |
| *(pausa)* | Del caos al orden: los avisos estallan sobre el plano 3, el plano se apaga y todo se recoge en el portátil con ImperiOS | Avisos: llamadas perdidas, WhatsApp, email, chat, portal |
| Después: con Imperios, el cliente entra directo a tu panel. Da igual de qué portal venga: todo centralizado. | Interfaz recreada: panel de clientes | DESPUÉS · «Todo / *centralizado*.» |
| En menos de un minuto, la inteligencia artificial le responde por WhatsApp sobre la propiedad que ha consultado. | Chat con respuesta automática | «Respuesta en / menos de 1 *minuto*.» |
| El cliente no se enfría. | Interés del cliente «caliente» | «El cliente no / se *enfría*.» |
| La conversación y la visita, en el mismo sitio. | Ficha con la visita | «Todo en el / mismo *sitio*.» |
| Y el recordatorio le llega solo, con la ubicación, el día y la hora. | Recordatorio → «Visita confirmada» | «Recordatorio / *automático*.» |
| *(1,3 s de respiro)* ★ Menos caos. | **T6** · plano 4, 0,5–3,7 s (cierra el portátil, coge el café) | DESPUÉS · «Menos *caos*.» |
| ★ Y esta vez, el cliente sí viene. | **T7** · plano 5, 0,55–3,45 s (los invita a pasar) | «Y esta vez, / el cliente sí *viene*.» |
| ¿Tu inmobiliaria sigue en el antes? Pide tu demo gratis y pasa al después. | Cierre: logo, fichas antes/después, CTA | «Pide tu demo gratis →» · «Y pasa al *después*.» · IMPERIOS.APP |

«En menos de un minuto» y «El cliente no se enfría» se mantienen por decisión de Brian (12/11/2026).

## Notas de los planos

- Escalado ×1,5 a 1080×1920 (9:16 exacto, sin bordes). ANTES etalonado en gris frío; DESPUÉS luminoso y cálido (`prep_r6h_clips.sh`).
- Oscurecido solo en la franja superior, donde va el texto.
- Plano 2: de cerca, las notificaciones del móvil salen con palabras inventadas («Llanada parlida»…). Por eso solo se usan
  los primeros 2,6 s, donde manda la agenda escrita a mano y el móvil queda pequeño bajo el titular.
- Plano 5: a partir de 3,5 s el marco de la puerta tapa medio encuadre, así que no se usa.

## Versión orgánica (16/11/2026)

`./build_r6h.sh O` → `preview/out/imperios-r6-higgsfield-organico_9x16.mp4` (~42 s). Mismo montaje, sin CTA: la voz acaba en
«¿Tu inmobiliaria sigue en el antes?» y el cierre es logo + fichas «antes: no se presentó → después: confirmada» + IMPERIOS.APP.
Ni «Pide tu demo» ni «enlace en la bio» en pantalla (regla de feed orgánico).

## Mejoras v2 (16/11/2026, en las dos versiones)

- La pregunta del cierre ya no entra sobre el plano 5 borroso: el plano se funde antes de «¿Tu…».
- Los titulares sobre vídeo cambian justo en el corte; antes desaparecían 0,25 s antes y dejaban fotogramas sin texto.
- Más oscurecido en el adelanto del plano 5 (el más luminoso) y un gris más claro para «pierde»: el gancho se lee mejor.
- La etiqueta ANTES da un golpe de escala al decir «Antes:».
