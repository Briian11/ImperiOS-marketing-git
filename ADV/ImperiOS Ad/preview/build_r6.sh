#!/usr/bin/env bash
# Reel orgánico R6 «Antes / después». Uso: ./build_r6.sh
# Voz con licencia (plan Starter, eleven_v4, Cristina) en assets_in/vo/starter/reel-r6-antes-despues.mp3 + tiempos de Scribe.
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
O=out/reels/r6; mkdir -p $O
export TL=timeline-r6.json PAGE=src/reel-r6.html VARIANT=A
# gancho (25/10/2026): «Así se pierde un cliente… y así se gana.» delante de «Antes: …»
python3 ../tools/empalmar_vo.py $L/reel-r6-v2.wav $L/reel-r6-v2.words.json $L/reel-r6-gancho.mp3 $L/reel-r6-gancho.words.json -1 0.45 \
  $L/reel-r6-antes-despues.mp3 $L/reel-r6-antes-despues.words.json -1 0
python3 build_timeline_r6.py $L/reel-r6-v2.words.json $L/reel-r6-v2.wav $TL $O/vo.wav
ffmpeg -hide_banner -loglevel error -y -i $O/vo.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/reels/imperios-reel-r6-antes-despues_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x5" -frames:v 1 out/reels/contact-sheet-r6.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r6
