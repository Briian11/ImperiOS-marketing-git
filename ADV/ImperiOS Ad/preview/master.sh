#!/usr/bin/env bash
# Premezcla (música + SFX) y máster a -14 LUFS / -1 dBTP. Uso: ./master.sh <dir_audio>
set -euo pipefail
D="$1"
ffmpeg -hide_banner -loglevel error -y -i "$D/music.wav" -i "$D/sfx.wav" -filter_complex "[0][1]amix=inputs=2:weights='1 1.3':normalize=0,acompressor=threshold=0.08:ratio=2.2:attack=8:release=120:makeup=1,alimiter=limit=0.6:attack=3:release=60:level=disabled" -c:a pcm_f32le "$D/premix.wav"
J=$(ffmpeg -hide_banner -i "$D/premix.wav" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g() { echo "$J" | grep "\"$1\"" | grep -oE '\-?[0-9.]+' | head -1; }
ffmpeg -hide_banner -loglevel error -y -i "$D/premix.wav" -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le "$D/master.wav"
ffmpeg -hide_banner -i "$D/master.wav" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
