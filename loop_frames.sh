#!/bin/bash

FILES=/Volumes/SSNL_Psych_Lab/Last11/ID178_vid6_crop_frames/

txt_file="ID178_vid6.txt"
csv_file="/Volumes/SSNL_Psych_Lab/Last11/ID178_vid6.csv"

firstFrame='frame_0.jpg'

echo Working on $firstFrame
python extractFacialPoints.py --shape-predictor shape_predictor_68_face_landmarks.dat \
--image $FILES$firstFrame > $txt_file

for f in `ls $FILES | sort -V`;
do
if [[ "$f" != "frame_0.jpg" ]]; then
	echo Working on $f, $csv_file
	python extractFacialPoints.py --shape-predictor shape_predictor_68_face_landmarks.dat \
	--image $FILES$f > tmp4.txt
	paste $txt_file tmp4.txt | sponge $txt_file
fi
done

tr -s "\\t" "," < $txt_file > $csv_file