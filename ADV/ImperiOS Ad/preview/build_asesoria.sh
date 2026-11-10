#!/usr/bin/env bash
# Versiones de anuncio con el cierre «Déjanos tus datos y revisamos tu caso para asesorarte gratis, sin compromiso.»
# (formulario de Meta + llamada de Brian). Uso: ./build_asesoria.sh [v4|r11]   (sin argumento: las dos)
# Voz: assets_in/vo/starter/cierre-asesoria.mp3 (eleven_v4, Cristina, ImperiOS's Workspace, 10/11/2026) + tiempos de Scribe,
# empalmada con tools/empalmar_vo.py tras «Imperios.» (v4 corto) y tras «¿…falso interés?» (R11).
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
LBL='Déjanos tus datos'
SUB='ASESORAMIENTO GRATUITO<br>SIN COMPROMISO'
if [ "${1:-v4}" = v4 ]; then
  python3 ../tools/empalmar_vo.py $L/cuerpo-corto-asesoria.wav $L/cuerpo-corto-asesoria.words.json \
    $L/cuerpo-corto.mp3 $L/cuerpo-corto.words.json 28 0.15 $L/cierre-asesoria.mp3 $L/cierre-asesoria.words.json -1 0
  CTA_LBL="$LBL" CTA_SUB="$SUB" python3 build_timeline_v4.py corto $L/gancho-A.words.json $L/gancho-A.mp3 \
    $L/cuerpo-corto-asesoria.words.json $L/cuerpo-corto-asesoria.wav timeline-v4-corto-A-asesoria.json out/v4/vo-corto-A-asesoria.wav
  SUF=-asesoria ./build_v4.sh corto A
fi
if [ "${1:-r11}" = r11 ]; then
  python3 ../tools/empalmar_vo.py $L/reel-r11-asesoria.wav $L/reel-r11-asesoria.words.json \
    $L/reel-r11-falso-interes.mp3 $L/reel-r11-falso-interes.words.json 89 0.25 $L/cierre-asesoria.mp3 $L/cierre-asesoria.words.json -1 0
  CTA_LBL="$LBL" CTA_SUB="$SUB" ./build_r11.sh asesoria
fi
