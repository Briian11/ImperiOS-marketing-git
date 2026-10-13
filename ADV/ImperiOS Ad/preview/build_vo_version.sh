#!/usr/bin/env bash
# Versión de campaña con una VO concreta. Uso: ./build_vo_version.sh <tag> <vo.mp3> <timeline.json>
set -euo pipefail
cd "$(dirname "$0")"
TAG="$1"; VOSRC="$2"; export TL="$3"; V="${4:-A}"
O=out/campaign-vo-$TAG; mkdir -p $O
ffmpeg -hide_banner -loglevel error -y -i "$VOSRC" -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2,aresample=48000" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
VARIANT=$V node render.js video $O/_A_silent.mp4 3
ffmpeg -hide_banner -loglevel error -y -i $O/_A_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $O/imperios-campana-v3-voz-${TAG}-${V}_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/imperios-campana-v3-voz-${TAG}-${V}_9x16.mp4 -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x3" -frames:v 1 $O/contact-sheet-$TAG.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $O/imperios-campana-v3-voz-${TAG}-${V}_9x16.mp4
echo BUILD_DONE
