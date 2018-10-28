# line for chin will be indicies 0-17 exclusive
# line for left eyebrow will be 17-22 exclusive
# line for right eyebrow will be 22-27
# line for nose will be 27-36
# line for left eye will be 36-42
# line for right eye will be 42-48
# lips will be the rest, 48:

# if we want to connect it to the first, just use the first x,y coords

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
file = 'ID129_vid5.csv'
path_to_csv = '/Users/MichaelSmith/Desktop/CSVs/ANIM_CSVs/' + file
facePts = np.genfromtxt(path_to_csv, delimiter=',')

savepath = '/Users/MichaelSmith/Desktop/CSVs/Animations/' + file[:-4]


numLines = 10
numLinesEyes = 4
numLinesNose = 1
numLinesMouth = 4

x_cols = facePts[:, 0::2]
y_cols = facePts[:, 1::2]

x_min = np.nanmin(x_cols)-20
x_max = np.nanmax(x_cols)+20
y_min = np.nanmin(y_cols)-5
y_max = np.nanmax(y_cols)+5

Writer = animation.writers['ffmpeg']
FPS = 29.97 # formally 9.99

writer = Writer(fps=29.97, metadata=dict(artist='Me'), bitrate=16000)

####################################################################
#					HERE BEGINS THE FULL FACE 					   #
####################################################################

fullFig = plt.figure(1)
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
line, = ax.plot([], [], ms=2)

plt.gca().invert_yaxis()
plt.axis('off')

lines = []
for i in range(numLines):
	lobj = ax.plot([], [], ms=2)[0]
	lines.append(lobj)

# initialization function: plot the background of each frame
def init():
	for line in lines:
		line.set_data([], [])
	return lines

# animation function.  This is called sequentially
def animate(i):

	cutOffPts = [0, 17, 22, 27, 36, 42, 48, 60, 68, 0, 0]

	x = facePts[:, 2*i]
	y = facePts[:, 2*i + 1]

	if 'X' in x or 'Y' in y:
		for lnum, line in enumerate(lines):
			line.set_data([], [])
	else:
		for lnum, line in enumerate(lines):
			arrX = x[cutOffPts[lnum]:cutOffPts[lnum+1]]
			arrY = y[cutOffPts[lnum]:cutOffPts[lnum+1]]

			if lnum in set([4,5,6,7]):
				line.set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))
			elif lnum == 8:
				line.set_data(np.append(x[48], x[60]), np.append(y[48], y[60]))
			elif lnum == 9:
				line.set_data(np.append(x[54], x[64]), np.append(y[54], y[64]))
			else:
				line.set_data(arrX, arrY)

		for i in range(len(lines)):
			lines[i].set_color('black')
		# face_color = lines[6].get_color()
		# lines[7].set_color(face_color)
		# lines[8].set_color(face_color)
		# lines[9].set_color(face_color)


	return lines


####################################################################
#						HERE BEGINS THE MOUTH  					   #
####################################################################

mouthFig = plt.figure(2)
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
line, = ax.plot([], [], ms=2)

plt.gca().invert_yaxis()
plt.axis('off')

linesMouth = []
for i in range(numLinesMouth+1):
	lobj = ax.plot([], [], ms=2)[0]
	linesMouth.append(lobj)

def init_mouth():
	for line in linesMouth:
		line.set_data([], [])
	return linesMouth

def animate_mouth(i):
	cutOffPts = [48, 60, 68, 0, 0, 17]

	x = facePts[:, 2*i]
	y = facePts[:, 2*i + 1]

	if 'X' in x or 'Y' in y:
		for lnum, line in enumerate(linesMouth):
			line.set_data([], [])
	else:
		for lnum, line in enumerate(linesMouth):
			arrX = x[cutOffPts[lnum]:cutOffPts[lnum+1]]
			arrY = y[cutOffPts[lnum]:cutOffPts[lnum+1]]

			if lnum in set([0, 1]):
				line.set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))
			elif lnum == 2:
				line.set_data(np.append(x[48], x[60]), np.append(y[48], y[60]))
			elif lnum == 3:
				line.set_data(np.append(x[54], x[64]), np.append(y[54], y[64]))
			else:
				line.set_data(arrX, arrY)

		for i in range(len(linesMouth)):
			linesMouth[i].set_color('black')
		# face_color = linesMouth[0].get_color()
		# linesMouth[1].set_color(face_color)
		# linesMouth[2].set_color(face_color)
		# linesMouth[3].set_color(face_color)


	return linesMouth


####################################################################
#						HERE BEGINS THE NOSE  					   #
####################################################################

noseFig = plt.figure(3)
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
line, = ax.plot([], [], ms=2)

plt.gca().invert_yaxis()
plt.axis('off')

linesNose = []
for i in range(numLinesNose):
	lobj = ax.plot([], [], ms=2)[0]
	linesNose.append(lobj)

# initialization function: plot the background of each frame
def init_nose():
	for line in linesNose:
		line.set_data([], [])
	return linesNose

def animate_nose(i):
	cutOffPts = [27, 36]

	x = facePts[:, 2*i]
	y = facePts[:, 2*i + 1]

	if 'X' in x or 'Y' in y:
		for lnum, line in enumerate(linesNose):
			line.set_data([], [])
	else:
		for lnum, line in enumerate(linesNose):
			arrX = x[cutOffPts[lnum]:cutOffPts[lnum+1]]
			arrY = y[cutOffPts[lnum]:cutOffPts[lnum+1]]

			line.set_data(arrX, arrY)

		for i in range(len(linesNose)):
			linesNose[i].set_color('black')

	return linesNose


####################################################################
#						HERE BEGIN THE EYES  					   #
####################################################################

eyesFig = plt.figure(4)
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
line, = ax.plot([], [], ms=2)

plt.gca().invert_yaxis()
plt.axis('off')

linesEyes = []
for i in range(numLinesEyes):
	lobj = ax.plot([], [], ms=2)[0]
	linesEyes.append(lobj)

def init_eyes():
	for line in linesEyes:
		line.set_data([], [])
	return linesEyes

def animate_eyes(i):

	cutOffPtsBrows = [17, 22, 27] # eyebrows
	cutOffPtsEyes = [36, 42, 48] # eyes + needs corrections...

	x = facePts[:, 2*i]
	y = facePts[:, 2*i + 1]

	if 'X' in x or 'Y' in y:
		for lnum, line in enumerate(linesEyes):
			line.set_data([], [])
	else:
		

		# line.set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))
		# this is important for the eyesies

		# brows
		arrX = x[cutOffPtsBrows[0]:cutOffPtsBrows[1]]
		arrY = y[cutOffPtsBrows[0]:cutOffPtsBrows[1]]
		linesEyes[0].set_data(arrX, arrY)

		arrX = x[cutOffPtsBrows[1]:cutOffPtsBrows[2]]
		arrY = y[cutOffPtsBrows[1]:cutOffPtsBrows[2]]
		linesEyes[1].set_data(arrX, arrY)

		#eyes
		arrX = x[cutOffPtsEyes[0]:cutOffPtsEyes[1]]
		arrY = y[cutOffPtsEyes[0]:cutOffPtsEyes[1]]
		linesEyes[2].set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))

		arrX = x[cutOffPtsEyes[1]:cutOffPtsEyes[2]]
		arrY = y[cutOffPtsEyes[1]:cutOffPtsEyes[2]]
		linesEyes[3].set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))

		for i in range(len(linesEyes)):
			linesEyes[i].set_color('black')
		# brow_color = linesEyes[0].get_color()
		# linesEyes[1].set_color(brow_color)
		# linesEyes[2].set_color(brow_color)
		# linesEyes[3].set_color(brow_color)


	return linesEyes


####################################################################
#					HERE BEGIN THE EYES w/JAW  					   #
####################################################################

eyesJawFig = plt.figure(5)
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
line, = ax.plot([], [], ms=2)

plt.gca().invert_yaxis()
plt.axis('off')

linesEyesJaw = []
for i in range(numLinesEyes+1):
	lobj = ax.plot([], [], ms=2)[0]
	linesEyesJaw.append(lobj)

def init_eyes_jaw():
	for line in linesEyesJaw:
		line.set_data([], [])
	return linesEyesJaw

def animate_eyes_jaw(i):

	cutOffPtsBrows = [17, 22, 27] # eyebrows
	cutOffPtsEyes = [36, 42, 48] # eyes + needs corrections...

	x = facePts[:, 2*i]
	y = facePts[:, 2*i + 1]

	if 'X' in x or 'Y' in y:
		for lnum, line in enumerate(linesEyesJaw):
			line.set_data([], [])
	else:
		

		# line.set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))
		# this is important for the eyesies

		# brows
		arrX = x[cutOffPtsBrows[0]:cutOffPtsBrows[1]]
		arrY = y[cutOffPtsBrows[0]:cutOffPtsBrows[1]]
		linesEyesJaw[0].set_data(arrX, arrY)

		arrX = x[cutOffPtsBrows[1]:cutOffPtsBrows[2]]
		arrY = y[cutOffPtsBrows[1]:cutOffPtsBrows[2]]
		linesEyesJaw[1].set_data(arrX, arrY)

		#eyes
		arrX = x[cutOffPtsEyes[0]:cutOffPtsEyes[1]]
		arrY = y[cutOffPtsEyes[0]:cutOffPtsEyes[1]]
		linesEyesJaw[2].set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))

		arrX = x[cutOffPtsEyes[1]:cutOffPtsEyes[2]]
		arrY = y[cutOffPtsEyes[1]:cutOffPtsEyes[2]]
		linesEyesJaw[3].set_data(np.append(arrX, arrX[0]), np.append(arrY, arrY[0]))

		# jaw
		arrX = x[0:17]
		arrY = y[0:17]
		linesEyesJaw[4].set_data(arrX, arrY)

		for i in range(len(linesEyesJaw)):
			linesEyesJaw[i].set_color('black')
		# brow_color = linesEyes[0].get_color()
		# linesEyes[1].set_color(brow_color)
		# linesEyes[2].set_color(brow_color)
		# linesEyes[3].set_color(brow_color)


	return linesEyes



####################################################################
#					HERE BEGIN THE ANIMATIONS					   #
####################################################################


num_frames = facePts.shape[1]/2
# call the animator.  blit=True means only re-draw the parts that have changed.
animFace = animation.FuncAnimation(fullFig, animate, init_func=init,
                               frames=num_frames, interval=num_frames/9.99, blit=True)

animMouth = animation.FuncAnimation(mouthFig, animate_mouth, init_func=init_mouth,
								frames=num_frames, interval=num_frames/9.99, blit=True)

animNose = animation.FuncAnimation(noseFig, animate_nose, init_func=init_nose,
								frames=num_frames, interval=num_frames/9.99, blit=True)

animEyes = animation.FuncAnimation(eyesFig, animate_eyes, init_func=init_eyes,
								frames=num_frames, interval=num_frames/9.99, blit=True)

animEyesJaw = animation.FuncAnimation(eyesJawFig, animate_eyes_jaw, init_func=init_eyes_jaw,
								frames=num_frames, interval=num_frames/9.99, blit=True)


animFace.save(savepath + '_animV2_face_nosound.mp4', writer=writer)
animMouth.save(savepath + '_animV2_mouth_nosound.mp4', writer=writer)
animNose.save(savepath + '_animV2_nose_nosound.mp4', writer=writer)
animEyes.save(savepath + '_animV2_eyes_nosound.mp4', writer=writer)
animEyesJaw.save(savepath + '_animV2_eyes_jaw_nosound.mp4', writer=writer)


#plt.show()