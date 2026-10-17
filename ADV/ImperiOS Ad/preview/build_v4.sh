#!/usr/bin/env bash
# Campaña v4 (3 ganchos × 2 duraciones). Uso: ./build_v4.sh <largo|corto> <A|B|C>
# Necesita timeline-v4-<dur>-<V>.json y out/v4/vo-<dur>-<V>.wav (los crea build_timeline_v4.py).
set -euo pipefail
cd "$(dirname "$0")"
DUR="$1"; V="$2"; TAG=$DUR-$V
export TL=timeline-v4-$TAG.json PAGE=src/reel-v4.html VARIANT=$V
O=out/v4/$TAG; mkdir -p $O
ffmpeg -hide_banner -loglevel error -y -i out/v4/vo-$TAG.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/v4/imperios-v4-$DUR-gancho$V\_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x4" -frames:v 1 out/v4/contact-sheet-$TAG.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE $TAG
