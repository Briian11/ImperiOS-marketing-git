#!/usr/bin/env bash
# Vídeos v4 con las voces con licencia comercial: ImperiOS's Workspace (plan Starter), eleven_v4, voz Cristina.
# Uso: ./build_licencia.sh <largo|corto> <A|B|C>
# Cada gancho y cada cuerpo es una sola toma de assets_in/vo/starter/, con sus tiempos de palabra de Scribe
# (<toma>.words.json). Monta el timeline y el vídeo con build_v4.sh.
set -euo pipefail
cd "$(dirname "$0")"
DUR="$1"; V="$2"
L=../assets_in/vo/starter
CTA_SUB='GRATIS, SIN COMPROMISO<br>IMPERIOS.APP ↗' python3 build_timeline_v4.py $DUR \
  $L/gancho-$V.words.json $L/gancho-$V.mp3 $L/cuerpo-$DUR.words.json $L/cuerpo-$DUR.mp3 \
  timeline-v4-$DUR-$V.json out/v4/vo-$DUR-$V.wav
./build_v4.sh $DUR $V
