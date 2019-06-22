#!/bin/sh

palette="/tmp/palette.png"

filters="fps=10,scale=1024:-1:flags=lanczos"

ffmpeg -r 10 -f image2 -s 1920x1080 -i $1 -vcodec libx264 -crf 25  -pix_fmt yuv420p $2
ffmpeg -v warning -i $2 -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i $2 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $3
