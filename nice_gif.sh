#!/bin/sh

# script to turn series of pictures into video and gif
# Use:
# 1) create video and gif from series of pictures. Use arguments: $1 - name for pictures with zeroes padding (e.g. name%04d);
# $2 - name of output mp4 video; $3 - name for output gif
palette="/tmp/palette.png"

filters="fps=10,scale=1024:-1:flags=lanczos"



ffmpeg -r 10 -f image2 -s 1920x1080 -i $1 -vcodec libx264 -crf 25  -pix_fmt yuv420p $2
ffmpeg -v warning -i $2 -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i $2 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse" -y $3
