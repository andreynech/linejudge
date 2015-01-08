#! /bin/sh

echo Generating motion data...
./motion.py > motion.dat
echo File motion.dat created
echo Visualising motion data with gnuplot...
./showmotion.gplot

