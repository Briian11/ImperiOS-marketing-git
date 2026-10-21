#!/usr/bin/env bash
# Vídeos v4 con las voces con licencia comercial (plan Starter, eleven_multilingual_v2, generadas por frases).
# Uso: ./build_licencia.sh <largo|corto> <A|B|C>
# Ensambla las frases de assets_in/vo/licencia/, estima los tiempos de palabra y monta el vídeo con build_v4.sh.
set -euo pipefail
cd "$(dirname "$0")"
DUR="$1"; V="$2"
L=../assets_in/vo/licencia
E=../tools/ensamblar_vo.py
P=0.35   # pausa entre frases
HOOK_A="¿Tus leads se pierden entre portales, WhatsApp y Excel?"
HOOK_B="¿Cuántos clientes se le escapan cada mes a tu inmobiliaria?"
HOOK_C="¿Cansado de usar diferentes herramientas para gestionar tu inmobiliaria?"
declare -A HOOK=([A]="$HOOK_A" [B]="$HOOK_B" [C]="$HOOK_C")
python3 $E $L/gancho-$V.wav $L/gancho-$V.words.json $L/gancho-$V.mp3 "${HOOK[$V]}" 0
if [ "$DUR" = largo ]; then
  python3 $E $L/cuerpo-largo.wav $L/cuerpo-largo.words.json \
    $L/largo-1.mp3 "Con Imperios, lo centralizas absolutamente todo." $P \
    $L/largo-2.mp3 "Todos tus leads entran en un solo sitio: portales inmobiliarios, tu web, campañas publicitarias y WhatsApp." 0.4 \
    $L/largo-3.mp3 "Y ves qué campañas y qué propiedades te traen más clientes." 0.4 \
    $L/largo-4a.mp3 "La inteligencia artificial cruza las características de tus propiedades con lo que busca cada cliente," 0.12 \
    $L/largo-4b.mp3 "y le envía automáticamente por WhatsApp las que encajan." 0.4 \
    $L/largo-5.mp3 "Visitas, agentes y recordatorios automáticos, coordinados desde la misma agenda." $P \
    $L/largo-6.mp3 "Imperios. Todo conectado, de principio a fin. Pide tu demo gratis, sin compromiso." 0
else
  python3 $E $L/cuerpo-corto.wav $L/cuerpo-corto.words.json \
    $L/corto-1.mp3 "Con Imperios, todos tus leads entran en un solo sitio: portales, web, campañas y WhatsApp." 0.4 \
    $L/corto-2.mp3 "La inteligencia artificial envía a cada cliente, por WhatsApp, las propiedades que encajan." $P \
    $L/corto-3.mp3 "Imperios. Pide tu demo gratis, sin compromiso." 0
fi
CTA_SUB='GRATIS, SIN COMPROMISO<br>IMPERIOS.APP ↗' python3 build_timeline_v4.py $DUR \
  $L/gancho-$V.words.json $L/gancho-$V.wav $L/cuerpo-$DUR.words.json $L/cuerpo-$DUR.wav \
  timeline-v4-$DUR-$V.json out/v4/vo-$DUR-$V.wav
./build_v4.sh $DUR $V
