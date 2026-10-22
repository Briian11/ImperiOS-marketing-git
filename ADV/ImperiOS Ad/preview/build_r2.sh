#!/usr/bin/env bash
# Reel orgánico R2 «3 errores que te hacen perder leads». Uso: ./build_r2.sh
# Voz con licencia (plan Starter, eleven_v4, Cristina) en assets_in/vo/starter/reel-r2-*.mp3 + tiempos de Scribe.
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
O=out/reels/r2; mkdir -p $O
export TL=timeline-r2.json PAGE=src/reel-r2.html VARIANT=A
# cierre (22/10/2026): «¿Cuál de los tres te pasa más? Cuéntamelo en comentarios. Imperios evita los tres. Comenta demo…»,
# empalmado tras «…el piso que busca» con tools/empalmar_vo.py
python3 ../tools/empalmar_vo.py $L/reel-r2-v2.wav $L/reel-r2-v2.words.json $L/reel-r2-errores.mp3 $L/reel-r2-errores.words.json 66 0.5 \
  $L/reel-r2-cierre-1.mp3 $L/reel-r2-cierre-1.words.json -1 0.35 $L/reel-r2-cierre-2.mp3 $L/reel-r2-cierre-2.words.json -1 0
python3 build_timeline_r2.py $L/reel-r2-v2.words.json $L/reel-r2-v2.wav $TL $O/vo.wav
ffmpeg -hide_banner -loglevel error -y -i $O/vo.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/reels/imperios-reel-r2-3-errores_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x4" out/reels/contact-sheet-r2.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r2
