#!/usr/bin/env bash
# Une imagen + máster de audio y genera el contact sheet de la preview.
set -euo pipefail
cd "$(dirname "$0")"
V=out/imperios-reel-v6-preview-v1_silent.mp4
A=out/audio/master.wav
O=out/imperios-reel-v6-preview-v1_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i "$V" -i "$A" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart "$O"
ffmpeg -hide_banner -loglevel error -y -i "$O" -vf "fps=1,scale=270:-1,drawtext=text='%{pts\:hms}':x=8:y=8:fontsize=16:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=4,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=7x3" -frames:v 1 out/contact-sheet-v1.png
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of default=nw=1 "$O"
