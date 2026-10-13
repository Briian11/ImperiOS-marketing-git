#!/usr/bin/env bash
# Versión de campaña con VO (gancho A): imagen re-temporizada a la voz + mezcla con VO + máster + corte corto.
set -euo pipefail
cd "$(dirname "$0")"
O=out/campaign-vo; mkdir -p $O
export TL=timeline-campaign-vo.json
VARIANT=A node render.js video $O/_A_silent.mp4 3
ffmpeg -hide_banner -loglevel error -y -i $O/_A_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $O/imperios-campana-v3-voz-A_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/imperios-campana-v3-voz-A_9x16.mp4 -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x3" -frames:v 1 $O/contact-sheet-campana-voz-A.png
echo "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/imperios-campana-v3-voz-A_9x16.mp4)"
echo BUILD_DONE
