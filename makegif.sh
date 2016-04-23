#!/bin/bash
# Reduce filesize of png files to make the gif smaller and to speed up processing.
# Then, use convert to create the gif from the png files.

cwd=plots
todir=smallerplots

shopt -s nullglob
for file in $cwd/*
do
  fname=$(basename $file)
  echo "Making $fname smaller."
  convert $file -resize "10%" $todir/$fname
done

echo "Making gif."
convert -delay 100 -loop 0 $todir/*.png visualization.gif
