#!/usr/bin/env bash
# R6 «Antes / después» con planos de Higgsfield: recorta cada tramo de los clips (Seedance 2.0, 720×1280, 24 fps),
# lo escala a 1080×1920 sin bordes (9:16 exacto, ×1,5 lanczos + enfoque suave) y lo etalona:
#   ANTES  → gris y algo frío (saturación 0,28)
#   DESPUÉS → luminoso y cálido
# Salida: src/r6h/<tramo>/0001.jpg … (24 fps). La página reel-r6h.html los pinta como fondo.
# Uso: ./prep_r6h_clips.sh   (idempotente; los fotogramas no van al repo, se regeneran desde los mp4)
set -euo pipefail
cd "$(dirname "$0")"
C=../assets_in/higgsfield/R6
O=src/r6h; rm -rf $O; mkdir -p $O
GA="eq=saturation=0.28:contrast=1.06:brightness=-0.03,colorbalance=bs=0.05:bm=0.03"
GD="eq=saturation=1.06:brightness=0.03:gamma=1.04,colorbalance=rs=0.03:rh=0.02"
SC="scale=1080:1920:flags=lanczos,unsharp=5:5:0.45"
# tramo  clip                       desde  duración  etalonaje
T=(
  "t1 plano1-agobiada.mp4        0.00 2.10 A"   # gancho: teclea, el móvil vibra (portada)
  "t2 plano5-visita.mp4          0.00 1.40 D"   # «…y así se gana»: apretón de manos (adelanto)
  "t3 plano1-agobiada.mp4        2.10 2.94 A"   # sigue la misma toma: deja el móvil y se lleva las manos a la cara
  "t4 plano2-agenda.mp4          0.20 2.60 A"   # agenda tachada; el móvil aún pequeño (sus avisos de cerca son ilegibles)
  "t5 plano3-visita-fallida.mp4  0.10 3.20 A"   # sola en el piso, mira el reloj (+ zoom lento en la página)
  "t6 plano4-tranquila.mp4       0.50 3.20 D"   # cierra el portátil y coge el café
  "t7 plano5-visita.mp4          0.55 2.90 D"   # los invita a pasar
)
for row in "${T[@]}"; do
  read -r id clip ss du g <<<"$row"
  [ "$g" = A ] && G=$GA || G=$GD
  mkdir -p $O/$id
  ffmpeg -hide_banner -loglevel error -y -ss "$ss" -i "$C/$clip" -t "$du" -vf "$SC,$G" -q:v 3 -start_number 0 "$O/$id/%04d.jpg"
  echo "$id $(ls $O/$id | wc -l) fotogramas"
done
