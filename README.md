# AnimateTheFace

This repo contains the structure needed to animate the face using a 68 (x, y) facial landmark detector from OpenFace 2.0, given videos of any person with their face headed toward the camera. This project initially began out of a curiosity to know if we could see emotion in an animation of 68 (x, y) points drawn from a video of a storyteller's face.


[![Example Animation--Click for Video!](https://img.youtube.com/vi/yC4847qwE80/0.jpg)](https://www.youtube.com/watch?v=yC4847qwE80) Click picture for video!

### Most Recent Version

###### Creation of Animation Videos

Seeing difficulties with Dlib's linear facial landmark detector (linear models have trouble when subjects look off to the side), and wanting to improve the efficiency of translating a video into a CSV of facial landmark points, I chose to use OpenFace 2.0's deep learning-based facial landmark model. To do so, I created a linux vm instance on GCP (as I had trouble getting it working on my Mac) and installed it. In addition to the 68 (x, y) facial landmarks, OpenFace 2.0 gave several other features (e.g. action units, eye gaze vectors) that I found useful for a project in emotion prediction for my class CS221. I wrote OF_CSVtoCSV.py to create CSV's in the format I needed for multLinesFace.py (the script I wrote to take the CSV and translate that into an animated video of the original storyteller's video). Click the picture above to see a video of what this looks like!

###### Further Processing of Data, Hypothesis Testing: Cleaning, Averaging, Correlations

After I created the animation videos, my lab and I ran experiments where MTurkers continuously rated the valence on a 0 (most negative) to 100 (most positive) scale for the duration of the video. We did this for three animated conditions (the full face, the eyes and jaw, and mouth and jaw). This gave me CSVs of dimension (number of raters x duration of video), which I needed to clean in order to remove raters who did not change their ratings frequently enough.

For this step, look at animation_correlations.ipynb. It's a Jupyter notebook (which I love for informational purposes) that shows my strategy for determining the correlations between an animation and its respective original video, as well as a few other correlations. In addition, look at cleanavgcorr.py, which contains the ParticipantResults class I wrote to manage the collective ratings of each animation video.

### Previous Version
I initally began by using a library called Dlib, which had a linear facial detection model that could work on pictures (not videos). So, I wrote video_division.py to split a video into its composite frames and store those in its respective folder. I stored every 3rd frame for space reasons. I also wrote a couple methods to divide a video into several parts. Using a folder of images, I would execute loop_frames.sh, which would iterate sequentially on the images using extractFacialPoints.py. This would create a CSV file of shape 68 x (2 x numFrames in folder). Given the CSV file, I would execute multLinesFace.py, which makes animations of the full face, the eyes and jaw, and mouth and jaw conditions. 


# Requirements: 
OpenFace 2.0 -- I installed this on a Ubuntu 18.04 virtual machine instead of Mac (I had trouble with that).
NumPy
Pandas
Matplotlib
OpenCV
ffmpeg
Dlib (if you want an understanding of how linear facial detection algorithms perform versus deep learning/convolutional methods)
