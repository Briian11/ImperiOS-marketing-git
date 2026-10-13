#!/usr/bin/env bash
# Máster con VO a -14 LUFS / -1 dBTP sin aplastar la voz:
#  1) bus música+SFX: compresor suave + limitador propio (los picos de golpes/sub se controlan aquí)
#  2) se suma la VO (ya comprimida 3:1 suave) y se aplica ganancia; el limitador final solo roza picos.
set -euo pipefail
D="$1"
ffmpeg -hide_banner -loglevel error -y -i "$D/music.wav" -i "$D/sfx.wav" -i "$D/vo.wav" -filter_complex "\
[0][1]amix=inputs=2:weights='1 1.3':normalize=0,acompressor=threshold=0.05:ratio=2.5:attack=5:release=120:makeup=1,alimiter=limit=0.12:attack=2:release=60:level=disabled[bed];\
[bed][2]amix=inputs=2:normalize=0" -c:a pcm_f32le "$D/premix.wav"
I=$(ffmpeg -hide_banner -i "$D/premix.wav" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | grep -oE '\-?[0-9.]+')
G=$(python3 -c "print(-14.0 - float('$I') + 0.0)")
ffmpeg -hide_banner -loglevel error -y -i "$D/premix.wav" -af "volume=${G}dB,aresample=192000,alimiter=limit=0.85:attack=1:release=40:level=disabled,aresample=48000" -c:a pcm_s24le "$D/master.wav"
echo "gain ${G} dB"
ffmpeg -hide_banner -i "$D/master.wav" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
