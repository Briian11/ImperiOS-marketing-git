#!/usr/bin/env bash
# Reel R6 «Antes / después» con planos de vídeo de Higgsfield (versión anuncio, con CTA). Uso: ./build_r6h.sh
# Voz con licencia (plan Starter, eleven_v4, Cristina): gancho + frases nuevas (reel-r6h-frases) + DESPUÉS y cierre de las tomas del R6.
# Planos: assets_in/higgsfield/R6/*.mp4 (Seedance 2.0) → prep_r6h_clips.sh → src/r6h/<tramo>/*.jpg
set -euo pipefail
cd "$(dirname "$0")"
L=../assets_in/vo/starter
O=out/reels/r6h; mkdir -p $O
export TL=timeline-r6h.json PAGE=src/reel-r6h.html VARIANT=A PW=${PW:-playwright}
./prep_r6h_clips.sh
# voz: gancho | ANTES nuevo (0,9 s para el caos→orden) | DESPUÉS del R6 (1,3 s: respiro sobre el plano 4) | «Menos caos…» | «¿Tu inmobiliaria…» | CTA
python3 ../tools/empalmar_vo.py $L/reel-r6h.wav $L/reel-r6h.words.json \
  $L/reel-r6-gancho.mp3 $L/reel-r6-gancho.words.json -1 0.35 \
  $L/reel-r6h-frases.mp3 $L/reel-r6h-frases.words.json 0:16 0.9 \
  $L/reel-r6-antes-despues.mp3 $L/reel-r6-antes-despues.words.json 52:115 1.3 \
  $L/reel-r6h-frases.mp3 $L/reel-r6h-frases.words.json 17:25 0.45 \
  $L/reel-r6-antes-despues.mp3 $L/reel-r6-antes-despues.words.json 116:121 0.35 \
  $L/reel-r6-cierre.mp3 $L/reel-r6-cierre.words.json -1 0
python3 build_timeline_r6h.py $L/reel-r6h.words.json $L/reel-r6h.wav $TL $O/vo.wav
ffmpeg -hide_banner -loglevel error -y -i $O/vo.wav -af "highpass=f=80,acompressor=threshold=0.035:ratio=3:attack=3:release=80:knee=4:makeup=2.2" -ac 1 -c:a pcm_f32le $O/vo_proc.wav
VO=$O/vo_proc.wav VO_OFFSET=$(python3 -c "import json;print(json.load(open('$TL'))['vo_offset'])") python3 audio_mix.py $O/audio
./master_vo.sh $O/audio
node render.js video $O/_silent.mp4 3
F=out/imperios-r6-higgsfield_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $F
ffmpeg -hide_banner -loglevel error -y -i $F -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x5" -frames:v 1 out/contact-sheet-r6-higgsfield.png
# portada: el primer fotograma (plano 1 con el gancho, logo y titular dentro del recorte 3:4 de la cuadrícula)
node render.js stills $O/portada 0 && cp $O/portada/t_00.00.png out/portada-r6-higgsfield.png
ffprobe -v error -show_entries format=duration -of csv=p=0 $F
echo BUILD_DONE r6h
