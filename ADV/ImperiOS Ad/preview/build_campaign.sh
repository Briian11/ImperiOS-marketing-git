#!/usr/bin/env bash
# Renderiza la versión de campaña: variante A completa + ganchos B y C empalmados en 2,6 s + corte de ~10 s.
set -euo pipefail
cd "$(dirname "$0")"
O=out/campaign; mkdir -p $O
export TL=timeline-campaign.json
VARIANT=A node render.js video $O/_A_silent.mp4 3
for v in B C; do VARIANT=$v node render.js video $O/_${v}_hook.mp4 3 0 2.6; done
for v in B C; do
  ffmpeg -hide_banner -loglevel error -y -i $O/_${v}_hook.mp4 -ss 2.6 -i $O/_A_silent.mp4 \
    -filter_complex "[0:v][1:v]concat=n=2:v=1[v]" -map "[v]" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 60 $O/_${v}_silent.mp4
done
for v in A B C; do
  ffmpeg -hide_banner -loglevel error -y -i $O/_${v}_silent.mp4 -i $O/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart $O/imperios-campana-v2-gancho-${v}_9x16.mp4
done
# corte de ~10 s: gancho A + match/reactivar + llamada a la acción, con fundidos cortos
F=$O/imperios-campana-v2-gancho-A_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $F -filter_complex "\
[0:v]trim=0:2.3,setpts=PTS-STARTPTS[v1];[0:a]atrim=0:2.3,asetpts=PTS-STARTPTS[a1];\
[0:v]trim=8.45:14.45,setpts=PTS-STARTPTS[v2];[0:a]atrim=8.45:14.45,asetpts=PTS-STARTPTS[a2];\
[0:v]trim=22.2:25,setpts=PTS-STARTPTS[v3];[0:a]atrim=22.2:25,asetpts=PTS-STARTPTS[a3];\
[v1][v2]xfade=transition=fade:duration=0.2:offset=2.1[v12];[v12][v3]xfade=transition=fade:duration=0.25:offset=7.85[v];\
[a1][a2]acrossfade=d=0.2[a12];[a12][a3]acrossfade=d=0.25[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -r 60 -c:a aac -b:a 320k -movflags +faststart $O/imperios-campana-v2-corte-10s_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $O/imperios-campana-v2-gancho-A_9x16.mp4 -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=9x3" -frames:v 1 $O/contact-sheet-campana-A.png
for f in $O/imperios-campana-*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
echo BUILD_DONE
