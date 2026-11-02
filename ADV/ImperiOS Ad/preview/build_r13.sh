#!/usr/bin/env bash
# Reel / anuncio R13 «El panel del CEO». Uso: ./build_r13.sh [A|B|corto]
#   A: Reel orgánico (Comenta DEMO) · B: anuncio completo (Pide tu demo) · corto: anuncio de ~22 s (gancho, dispositivos, embudo y cierre)
# Voz con licencia (plan Starter, eleven_v4, Cristina) en assets_in/vo/starter/reel-r13-panel-ceo.mp3 + tiempos de Scribe.
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
V=${1:-A}
O=out/reels/r13-$V; mkdir -p $O
export TL=timeline-r13-$V.json PAGE=src/reel-r13.html VARIANT=$([ "$V" = A ] && echo A || echo B)
W=$L/reel-r13-panel-ceo.words.json; AU=$L/reel-r13-panel-ceo.mp3
if [ "$V" = corto ]; then
  # gancho (0–16) · dispositivos (17–24) · embudo y «no se te escapa nada» (25–45) · cierre (115–127)
  python3 ../tools/empalmar_vo.py $L/reel-r13-corto.wav $L/reel-r13-corto.words.json $AU $W 0:16 0.15 $AU $W 17:24 0.3 $AU $W 25:45 0.45 $AU $W 115:127 0
  W=$L/reel-r13-corto.words.json; AU=$L/reel-r13-corto.wav
fi
python3 build_timeline_r13.py $W $AU $TL $O/vo.wav
ffmpeg -hide_banner -loglevel error -y -i $O/vo.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/reels/imperios-r13-panel-ceo-$V\_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x5" -frames:v 1 out/reels/contact-sheet-r13-$V.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r13 $V
