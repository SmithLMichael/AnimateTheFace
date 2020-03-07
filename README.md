# AnimateTheFace

This repo contains the structure needed to animate the face using a 68 (x, y) facial landmark detector from OpenFace 2.0, given videos of any person with their face headed toward the camera. This project initially began out of a curiosity to know if we could see emotion in an animation of 68 (x, y) points drawn from a video of a storyteller's face.


[![Example Animation--Click for Video!](https://img.youtube.com/vi/yC4847qwE80/0.jpg)](https://www.youtube.com/watch?v=yC4847qwE80)


I initally began by using a library called Dlib, which had a linear facial detection model that could work on pictures (not videos). So, I wrote video_division.py to split a video into its composite frames and store those in its respective folder. I stored every 3rd frame for space reasons. I also wrote a couple methods to divide a video into several parts. Using a folder of images, I would execute loop_frames.sh, which would iterate sequentially on the images using extractFacialPoints.py. This would create a CSV file of shape 68 x (2 x numFrames in folder). Given the CSV file, I would execute multLinesFace.py, which makes animations of the full face, the eyes and jaw, and mouth and jaw conditions. 

# Requirements: 
OpenFace 2.0 -- I installed this on a Ubuntu 18.04 virtual machine instead of Mac (I had trouble with that).
NumPy
Pandas
Matplotlib
OpenCV
ffmpeg
Dlib (if you want an understanding of how linear facial detection algorithms perform versus deep learning/convolutional methods)
