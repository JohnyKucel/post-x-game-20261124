#!/bin/bash
# Assemble post-x-game.mp4 from the PIL frames in frames/ + the make.fun
# referral end card (press pack, used as-is) + referral code jy3a6hm3.
# Run from video/:  bash assemble.sh
set -euo pipefail
cd "$(dirname "$0")"

# 1. Base clip: 720 frames @30fps = 24s (prompt 0-4s, agent 4-12s, game 12-24s)
ffmpeg -y -v error -framerate 30 -i frames/f%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 base.mp4

# 2. Tail: last gameplay frame held 3s, blurred + desaturated, card over it.
#    Card (2.5s) starts at 0.5s so it ends exactly at 3.0s; the field comes to
#    rest 1.433s into the card, so the code is drawn from 1.93s on.
ffmpeg -y -v error -loop 1 -t 3 -i frames/f0719.png -i makefun-card-9x16-transparent.webm \
  -filter_complex "[0:v]gblur=sigma=28,eq=saturation=0.35[bg];[bg][1:v]overlay=0:0:enable='between(t,0.5,3.0)',drawtext=fontfile=/home/hatch/.local/share/fonts/Inter-Variable.ttf:text='jy3a6hm3':fontsize=62:fontcolor=#191419:x=210:y=1232:enable='between(t,1.93,3.0)'[v]" \
  -map "[v]" -t 3 -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 tail.mp4

# 3. Join + silent audio track (X accepts silent MP4; AAC track keeps it standard)
ffmpeg -y -v error -i base.mp4 -i tail.mp4 -f lavfi -t 27 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" -map 2:a \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -shortest \
  -movflags +faststart post-x-game.mp4

ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 post-x-game.mp4
ls -la post-x-game.mp4 base.mp4 tail.mp4
