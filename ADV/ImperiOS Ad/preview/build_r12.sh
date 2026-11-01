#!/usr/bin/env bash
# Reel orgánico R12 «Red flags de una inmobiliaria desorganizada» (sin voz). Uso: ./build_r12.sh
set -euo pipefail
cd "$(dirname "$0")"
O=out/reels/r12; mkdir -p $O
export TL=timeline-r12.json PAGE=src/reel-r12.html VARIANT=A
python3 build_timeline_r12.py $TL
python3 audio_mix.py $O/audio
# máster sin voz: ganancia a −14 LUFS y limitador a −1 dBTP
I=$(ffmpeg -hide_banner -i $O/audio/mix_premaster.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | grep -oE '\-?[0-9.]+')
G=$(python3 -c "print(-14.0 - float('$I'))")
ffmpeg -hide_banner -loglevel error -y -i $O/audio/mix_premaster.wav -af "volume=${G}dB,aresample=192000,alimiter=limit=0.85:attack=1:release=40:level=disabled,aresample=48000" -c:a pcm_s24le $O/audio/master.wav
node render.js video $O/_silent.mp4 3
F=out/reels/imperios-reel-r12-red-flags_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x2" -frames:v 1 out/reels/contact-sheet-r12.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r12
