#!/usr/bin/env bash
# Reel orgánico R11 «Falso interés» (calificación con IA). Uso: ./build_r11.sh [asesoria]
# Con «asesoria»: versión de anuncio con el cierre «Déjanos tus datos…» (voz empalmada por build_asesoria.sh).
# Voz con licencia (plan Starter, eleven_v4, Cristina) en assets_in/vo/starter/reel-r11-falso-interes.mp3 + tiempos de Scribe.
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
if [ "${1:-}" = asesoria ]; then
  SUF=-asesoria; VW=$L/reel-r11-asesoria.words.json; VA=$L/reel-r11-asesoria.wav
else
  SUF=; VW=$L/reel-r11-falso-interes.words.json; VA=$L/reel-r11-falso-interes.mp3
fi
O=out/reels/r11$SUF; mkdir -p $O
export TL=timeline-r11$SUF.json PAGE=src/reel-r11.html VARIANT=A
python3 build_timeline_r11.py $VW $VA $TL $O/vo.wav
ffmpeg -hide_banner -loglevel error -y -i $O/vo.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/reels/imperios-reel-r11-falso-interes$SUF\_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x4" -frames:v 1 out/reels/contact-sheet-r11$SUF.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r11$SUF
